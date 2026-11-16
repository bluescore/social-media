"""Monta o áudio do EPISÓDIO COMPLETO do ep. 01 (versão para aprovação, mais ágil): 0 a 64,0 s.

Linha do tempo (segundos do episódio, 30 quadros por segundo):
  s01 0-9,3 · s03 9,2-15,3 · s04 15,3-18,3 · s05 18,3-22,6 · virada 22,6-31,433 (IMPACTO em 30,633 = quadro 919)
  s08 31,433-43,4 (o vídeo dela, sem voz) · s09 43,4-46,9 · s10 46,9-51,9 · s11 51,9-59,3 · s12 59,3-64,0

De 22,6 s em diante (até onde o corte terminava, 33,433 s) os sons da virada são os do corte de 10 s aprovado
(montar-corte10s.py): os mesmos arquivos, recortes, volumes e tempos, só deslocados 22,6 s (1.084.800 amostras).
O script confere isso no fim (teste de "subtração" contra mix-corte10s.wav).

Regras que este script segue (regras do dono):
  - a voz NUNCA é esticada, acelerada, emendada nem limitada: cada fala é recortada da tomada A só no meio das pausas
    e colocada no seu tempo; se uma fala não cabe antes da próxima, a próxima desliza (o mínimo possível);
  - cada fala recebe UM ganho fixo (o mesmo do começo ao fim dela), calculado para todas ficarem com o mesmo volume
    percebido (LUFS); nada de limitador nem compressor na voz;
  - a trilha NUNCA é esticada nem cortada: ela só é deslocada para o golpe cair em 30,633 s (tempo da música =
    tempo do episódio + 6,044 s) e tem o volume ajustado (curvas lentas);
  - um ganho fixo final (o mesmo do começo ao fim), o maior possível sem a voz passar de -1,2 dBTP;
  - o limitador (que segura picos) só age na trilha + efeitos, só entre o impacto e o fim do vídeo dela
    (30,613-43,4 s), onde não há voz; a voz é somada depois, então ela nunca passa por ele;
  - fade de 0,25 s só no fim; os efeitos têm só entradas/saídas curtas para não estalar.

Para mudar alguma coisa, mexa no PLANO abaixo e rode de novo (dentro da pasta do episódio):
    python -I fonte/audio/montar-final.py
Entradas: assets/audio/fontes/*.mp3 (tudo do ElevenLabs) e assets/audio/mix-corte10s.wav (só para conferir)
Saídas:   assets/audio/mix-final.wav (48 kHz, estéreo, 24 bits, 64,0 s)
          assets/audio/audio-final.json (cada fala e cada evento: arquivo, tempo, ganho; medições)
"""
import json
import os
import re
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.ndimage import minimum_filter1d
from scipy.signal import butter, iirnotch, resample_poly, sosfiltfilt, filtfilt

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(os.path.dirname(AQUI))
AUDIO = os.path.join(PECA, 'assets', 'audio')
FONTES = os.path.join(AUDIO, 'fontes')
SR = 48000
DUR = 64.0
N = int(round(DUR * SR))              # 3.072.000 amostras
BASE_CORTE = 22.6                     # onde o corte de 10 s começa no episódio (a virada)
I0 = int(round(BASE_CORTE * SR))      # 1.084.800 amostras
DUR_CORTE = 10.833
N_CORTE = int(round(DUR_CORTE * SR))
GOLPE_CORTE = 8.033                   # quadro 241 do corte
GOLPE_EP = BASE_CORTE + GOLPE_CORTE   # 30,633 s = quadro 919 do episódio

# ----------------------------------------------------------------------------------------------------------------
# PLANO
# Tempos "no_ep" = segundos do episódio. Tempos "no_corte" (itens do corte de 10 s) = segundos do corte, copiados
# sem mudança do montar-corte10s.py; eles caem em no_corte + 22,6 s do episódio.
# "ancora" diz QUE ponto do arquivo cai nesse tempo:
#   inicio      = onde o som começa (primeiro ponto a 30 dB do pico do trecho usado)
#   trecho      = o começo do trecho usado ("de"), sem procurar nada
#   transiente  = o estalo principal (primeiro ponto a 6 dB do pico dentro de "busca", em segundos do arquivo)
#   pico        = o ponto mais forte (volume em janelas de 20 ms)
#   fim         = o fim do trecho usado
# Volume de cada efeito (um dos três, antes do ganho final):
#   pico_alvo_db      = pico em janelas de 1 ms
#   rms_alvo_db       = volume médio (ambientes)
#   abaixo_trilha_db  = quantos LU (unidades de volume percebido) abaixo da trilha naquele mesmo trecho
# "filtro": passa_altas_hz (tira o grave/ronco) e/ou notch_hz (tira uma nota estreita escondida no som).
# ----------------------------------------------------------------------------------------------------------------
PLANO = {
    'voz': {
        'arquivo': 'narracao-amedeiros-v4-a.mp3',
        'limiar_fala_dbfs': -50.0,      # a fala "existe" onde o volume (janelas de 2 ms) passa disso, na tomada crua
        'pausa_minima_s': 0.25,         # se uma fala não cabe, a próxima começa 0,25 s depois do fim dela
        'entrada_saida_s': 0.015,       # entrada/saída de 15 ms, dentro das pausas (silêncio)
        # IGUALAR: cada fala recebe ganho = ganho_da_referencia + (LUFS da referência - LUFS da fala) + ajuste_db.
        # A referência é a fala do corte ("cada linha..."), que fica com o MESMO ganho do corte aprovado (-7,6 dB);
        # ela e "décima quarta tentativa." são as que têm o pico mais alto para o seu volume, então são elas que
        # decidem até onde a voz inteira pode subir.
        'referencia': 'cada linha que ela escreveu virou uma cena.',
        'ganho_da_referencia_db': -7.6,
        # de/ate = trecho da tomada (no meio das pausas); alvo = onde a fala deve começar no episódio
        'falas': [
            {'texto': 'décima quarta tentativa.', 'de': 0.000, 'ate': 2.093, 'alvo': 0.10, 'ajuste_db': 0.0,
             'entrada_s': 0.003, 'obs': 'a tomada começa já falando (0,002 s): entrada de 3 ms'},
            {'texto': 'e o vídeo não sai.', 'de': 2.217, 'ate': 3.668, 'alvo': 2.32, 'ajuste_db': 0.0},
            {'texto': 'a doutora Helena explica a prótese protocolo toda semana, paciente por paciente.',
             'de': 3.732, 'ate': 8.950, 'alvo': 3.95, 'ajuste_db': 0.0},
            {'texto': 'o roteiro sobre implantes está pronto há seis semanas.', 'de': 8.950, 'ate': 12.281,
             'alvo': 9.45, 'ajuste_db': 0.0},
            {'texto': 'a gravação, não.', 'de': 12.281, 'ate': 13.904, 'alvo': 12.95, 'ajuste_db': 0.0,
             'obs': 'o "não" fica de +0,92 a +1,16 s do começo da fala (13,87-14,11 s); o risco é 13,70-14,05'},
            {'texto': 'ela não gravou a décima quinta.', 'de': 13.974, 'ate': 15.813, 'alvo': 18.60, 'ajuste_db': 0.0},
            {'texto': 'mandou só o roteiro.', 'de': 15.813, 'ate': 17.090, 'alvo': 20.90, 'ajuste_db': 0.0},
            # a fala do corte de 10 s, exatamente como lá (17,090-19,775 s da tomada; a fala começa em 1,000 do corte)
            {'texto': 'cada linha que ela escreveu virou uma cena.', 'de': 17.090, 'ate': 19.775, 'alvo': 23.60,
             'ajuste_db': 0.0, 'do_corte': True, 'fala_comeca_no_arquivo': 17.290, 'fala_comeca_no_corte': 1.000},
            # as 4 falas novas: pausas medidas na tomada A (volume abaixo de -50 dBFS), corte no meio de cada pausa
            {'texto': 'o perfil voltou a andar.', 'de': 19.775, 'ate': 21.449, 'alvo': 43.70, 'ajuste_db': 0.0},
            {'texto': 'ela mandou o vídeo pra turma.', 'de': 21.449, 'ate': 23.020, 'alvo': 47.20, 'ajuste_db': 0.0},
            {'texto': 'o roteiro ela já tinha.', 'de': 23.020, 'ate': 24.466, 'alvo': 52.30, 'ajuste_db': 0.0},
            {'texto': 'no próximo episódio: o que a recepção mais ouve.', 'de': 24.466, 'ate': 28.000,
             'alvo': 59.60, 'ajuste_db': 0.0,
             'obs': 'a pausa depois de "episódio:" (25,83-26,15 s da tomada) é da própria leitura; a fala vai até '
                    'o fim da tomada (27,84 s; depois só há 0,16 s de silêncio)'},
        ],
    },
    'trilha': {
        'arquivo': 'trilha-tema-b.mp3',
        'golpe_no_arquivo': 36.677,             # ataque do golpe (medido com 1 ms; ver fonte/audio/golpes.json)
        'entrada': [3.55, 4.55],                # a música começa a soar com o recuo (3,55 s) e chega ao volume em 4,55
        # volume (fator) ao longo do episódio; entre os pontos o volume muda em linha reta (em dB).
        #  - até 22,6 s: um fator por frase do piano (uma nota a cada 3,33 s), os mesmos do corte ampliado (eles
        #    seguem o conteúdo da música, que é a mesma), só que com o tempo novo (-2,7 s); a mudança é feita em
        #    0,3 s e termina 20 ms antes de cada nota. Ajustados para cada frase inteira ficar um pouco mais alta
        #    que a anterior (ver "trilha_por_frase" no relatório) e nunca cair antes do golpe;
        #  - de 22,6 a 30,6 s: EXATAMENTE o envelope do corte de 10 s (0,14 até 26,1; sobe até 0,45 em 30,6);
        #  - de 30,6 a 43,4 s: o auge (0,45), sustentado durante o vídeo dela;
        #  - de 43,4 s em diante: "relaxa" (o leito, ver abaixo).
        'volume': [[3.55, 0.05], [6.971, 0.05], [7.271, 0.064], [9.931, 0.064], [10.231, 0.16],
                   [13.641, 0.16], [13.941, 0.075], [16.966, 0.075], [17.266, 0.099], [20.316, 0.099],
                   [20.616, 0.047], [22.6, 0.14],
                   [26.1, 0.14], [30.6, 0.45],
                   # no auge, só um acento da música (37,32 s, no passo 2 do vídeo dela) passaria muito do teto:
                   # ele desce 3 dB por 0,3 s (rampas de 0,1 s), para o limitador não precisar achatar 5,6 dB ali
                   [37.2, 0.45], [37.3, 0.3186], [37.6, 0.3186], [37.7, 0.45],
                   # 13/11 (sessão principal): o fim do vídeo dela desce devagar (-3,5 dB de 42,4 a 43,2) em vez de
                   # cair de uma vez em 43,4; isso também tira a última onda (43,1–43,5), que era o ponto mais forte do mix
                   [42.4, 0.45], [43.2, 0.30]],
        # o relaxamento: de 43,4 a 43,85 s o volume desce do auge até o leito, rápido no começo (curva power2.out,
        # em dB), para a voz entrar (43,7 s) já com a música quase no leito. O leito é calculado para a trilha ficar
        # em leito_lufs_sob_a_voz nas falas 9, 10 e 11 (com o recorte de médias): -30,5 LUFS, ~11 dB abaixo da
        # voz, entre o que ela fica sob "cada linha..." no corte aprovado (10,5 dB) e no corte ampliado (13,2 dB).
        # O fator 0,20 do SPEC NÃO serve aqui: a trilha B não relaxa sozinha depois do golpe (segue no volume cheio
        # até 57,96 s do episódio), e com 0,20 ela ficaria em ~-17,5 LUFS, mais alta que a própria voz.
        'relaxa': {'de': 43.2, 'ate': 44.0, 'leito_lufs_sob_a_voz': -30.5, 'falas_de_referencia': [8, 9, 10]},
        # realce: no silêncio da voz em s11 ("faltava a forma" e a dedicatória) a trilha sobe 3 dB, com uma rampa
        # lenta, e fica assim até o fim: de 57,96 s em diante a própria música vai sumindo sozinha (fade natural),
        # e sob a última fala ela já está ~20 dB abaixo da voz. 'desce': [de, até] faria voltar ao leito. 0 = sem.
        'realce': {'db': 3.0, 'sobe': [53.6, 54.8], 'desce': None},
        'frases_do_piano': [[3.956, 7.291], [7.291, 10.251], [10.251, 13.961], [13.961, 17.286], [17.286, 20.636],
                            [20.636, 23.966], [23.966, 27.296], [27.296, 30.633]],
        # recorte de médias (1-4 kHz) na trilha enquanto a voz fala, para abrir espaço para ela (o mesmo do corte)
        'recorte_medias_db': -4.0, 'recorte_folga_s': 0.20, 'recorte_rampa_s': 0.15,
        'recorte_do_corte': [0.80, 3.50],       # a janela da fala do corte, sem mudança (em segundos do corte)
    },
    # o leito de ambiente noturno de 0 a 22,6 s: a tomada b (5 s, estável) repetida com cruzamentos; em 22,6 s entra
    # o ambiente do corte de 10 s (o mesmo arquivo, desde o começo), e o leito sai em 40 ms por baixo dele.
    'leito_ambiente': {
        'nome': 'ambiente de consultório à noite (leito de 0 a 22,6 s)', 'arquivo': 'ambiente-noite-b.mp3',
        'cruzamento_s': 0.5, 'entrada_s': 0.010, 'fim_ep': BASE_CORTE, 'saida_s': 0.040,
        'busca_emenda_s': [0.0, 1.5],
    },
    'efeitos': [
        # ---------------- s01 a s05 (as escolhas do corte ampliado, nos tempos novos) ----------------
        {'nome': 'toque seco no vidro ("apagar")', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 1.930, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0},
        {'nome': 'tique seco do contador (take 14 -> take 15)', 'arquivo': 'tique-contador-a.mp3', 'de': 0.085,
         'ate': 0.135, 'ancora': 'transiente', 'busca': [0.095, 0.110], 'no_ep': 2.650, 'entrada_s': 0.003,
         'saida_s': 0.010, 'pico_alvo_db': -37.0},
        {'nome': 'sopro grave do recuo que revela a maquete', 'arquivo': 'sopro-grave-d.mp3', 'de': 0.0, 'ate': 2.56,
         'ancora': 'pico', 'no_ep': 4.700, 'entrada_s': 0.05, 'saida_s': 0.50, 'pico_alvo_db': -38.0,
         'obs': 'o pico do sopro cai em 4,7 s, o meio do recuo (3,55-5,85 s, mais rápido no meio)'},
        {'nome': 'papel farfalhando de leve (a folha chega)', 'arquivo': 'papel-farfalhando-a.mp3', 'de': 0.0,
         'ate': 0.85, 'ancora': 'inicio', 'no_ep': 9.300, 'entrada_s': 0.01, 'saida_s': 0.20, 'pico_alvo_db': -42.0},
        {'nome': 'risco de caneta em "gravar 06/11"', 'arquivo': 'risco-caneta-c.mp3', 'de': 0.0, 'ate': 0.36,
         'ancora': 'trecho', 'no_ep': 13.700, 'entrada_s': 0.005, 'saida_s': 0.08, 'pico_alvo_db': -43.0,
         'obs': 'o risco (13,70-14,05 s) cai no "não" de "a gravação, não." (13,87 s)'},
        {'nome': 'toque seco no vidro (abre o perfil)', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 15.370, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0},
        {'nome': 'atrito suave da rolagem da tela', 'arquivo': 'rolagem-tela-a.mp3', 'de': 0.30, 'ate': 1.0,
         'ancora': 'trecho', 'no_ep': 15.430, 'entrada_s': 0.03, 'saida_s': 0.25, 'pico_alvo_db': -40.0,
         'obs': 'trecho a partir de 0,30 s do arquivo (o ajuste da conferência do corte ampliado): o atrito já se '
                'ouve no começo da rolagem (15,43 s), fica mais forte logo depois e some por volta de 16,1 s'},
        {'nome': 'obturador do celular (fecha e reabre)', 'arquivo': 'obturador-a.mp3', 'de': 0.0, 'ate': 0.30,
         'ancora': 'trecho', 'no_ep': 19.900, 'entrada_s': 0.002, 'saida_s': 0.10, 'pico_alvo_db': -37.0,
         'obs': 'dois estalos (fecha em 19,93 e reabre em 20,01)'},
        {'nome': 'toque seco no vidro ("enviado")', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 20.350, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0},
        # ---------------- a virada: do corte de 10 s, sem nenhuma mudança (tempos do corte; caem em +22,6 s) -------
        {'nome': 'ambiente de consultório à noite', 'arquivo': 'ambiente-noite-b.mp3', 'de': 0.0, 'ate': 1.2,
         'ancora': 'inicio', 'no_corte': 0.000, 'entrada_s': 0.02, 'saida_s': 0.60, 'rms_alvo_db': -56.0},
        {'nome': 'clique do interruptor do abajur', 'arquivo': 'interruptor-b.mp3', 'de': 0.0, 'ate': 0.40,
         'ancora': 'transiente', 'busca': [0.0, 0.15], 'no_corte': 0.200, 'entrada_s': 0.005, 'saida_s': 0.10,
         'pico_alvo_db': -33.0},
        {'nome': 'traço no papel 1 (arcada)', 'arquivo': 'traco-papel-a.mp3', 'de': 0.0, 'ate': 0.32,
         'ancora': 'inicio', 'no_corte': 1.700, 'entrada_s': 0.005, 'saida_s': 0.08, 'pico_alvo_db': -44.0},
        {'nome': 'traço no papel 2 (implantes)', 'arquivo': 'traco-papel-b.mp3', 'de': 0.0, 'ate': 0.32,
         'ancora': 'inicio', 'no_corte': 2.100, 'entrada_s': 0.005, 'saida_s': 0.08, 'pico_alvo_db': -44.0},
        {'nome': 'traço no papel 3 (osseointegração)', 'arquivo': 'traco-papel-a.mp3', 'de': 0.0, 'ate': 0.32,
         'ancora': 'inicio', 'no_corte': 2.500, 'entrada_s': 0.005, 'saida_s': 0.08, 'pico_alvo_db': -44.0},
        {'nome': 'traço no papel 4 (parafusada)', 'arquivo': 'traco-papel-b.mp3', 'de': 0.0, 'ate': 0.32,
         'ancora': 'inicio', 'no_corte': 2.900, 'entrada_s': 0.005, 'saida_s': 0.08, 'pico_alvo_db': -44.0},
        {'nome': 'folha se descolando da mesa', 'arquivo': 'folha-descolando-b.mp3', 'de': 0.0, 'ate': 1.0,
         'ancora': 'inicio', 'no_corte': 5.033, 'entrada_s': 0.03, 'saida_s': 0.25, 'pico_alvo_db': -40.0},
        {'nome': 'dobra de papel 1', 'arquivo': 'dobra-1-a.mp3', 'de': 0.30, 'ate': 0.680,
         'ancora': 'transiente', 'busca': [0.33, 0.45], 'no_corte': 5.900, 'entrada_s': 0.02, 'saida_s': 0.10,
         'pico_alvo_db': -27.0},
        {'nome': 'dobra de papel 2', 'arquivo': 'dobra-2-b.mp3', 'de': 0.26, 'ate': 0.680,
         'ancora': 'transiente', 'busca': [0.28, 0.36], 'no_corte': 6.733, 'entrada_s': 0.02, 'saida_s': 0.10,
         'pico_alvo_db': -27.0},
        {'nome': 'dobra de papel 3 (giro)', 'arquivo': 'dobra-3-a.mp3', 'de': 0.40, 'ate': 0.680,
         'ancora': 'transiente', 'busca': [0.44, 0.52], 'no_corte': 7.633, 'entrada_s': 0.03, 'saida_s': 0.10,
         'pico_alvo_db': -27.0},
        {'nome': 'riser (som que sobe até o golpe)', 'arquivo': 'riser-b.mp3', 'de': 0.47, 'ate': 2.0,
         'ancora': 'fim', 'no_corte': 8.013, 'entrada_s': 0.05, 'saida_s': 0.008, 'pico_alvo_db': -27.0},
        {'nome': 'impacto: grave + eco (reforço do golpe da trilha)', 'arquivo': 'impacto-a.mp3', 'de': 0.0,
         'ate': 3.0, 'ancora': 'inicio', 'no_corte': GOLPE_CORTE, 'entrada_s': 0.001, 'saida_s': 0.40,
         'pico_alvo_db': -23.0},
        # ---------------- s08: o vídeo dela (novos; baixos: 10 a 12 LU abaixo da trilha no auge) ----------------
        # (o chiado é claro, em ~8 kHz, onde a trilha quase não tem som; por isso ele fica mais baixo que o resto)
        # Tempos casados com compositions/s08-video-dela.html (s08 começa em 31,433 = quadro 943; P2 = 2,6;
        # P3 = 184/30; P4 = 277/30): varredura do vidro 2,9-3,9 (34,333-35,333) · plano de corte desce em P3
        # (37,567) · o osso cresce de P3+0,6 a P3+1,8 (38,167-39,367) · faixa de luz de P4+0,2 a P4+1,2
        # (40,867-41,867). Conferência de 12/11: chiado, textura e brilho estavam 0,32 a 0,48 s ANTES da imagem
        # (seguiam um esboço antigo de s08) e foram movidos para estes tempos.
        {'nome': 'atrito seco de vidro fosco (a varredura)', 'arquivo': 'atrito-vidro-fosco-e.mp3', 'de': 0.0,
         'ate': 1.15, 'ancora': 'trecho', 'no_ep': 34.300, 'entrada_s': 0.02, 'saida_s': 0.15,
         'abaixo_trilha_db': 10.0,
         'obs': 'tomada e (3ª rodada): chiado de areia fina que cresce até 0,4 s, fica e some em 1,1 s; sem nota'},
        {'nome': 'chiado fino de corte', 'arquivo': 'chiado-corte-a.mp3', 'de': 0.0, 'ate': 0.40,
         'ancora': 'inicio', 'no_ep': 37.567, 'entrada_s': 0.005, 'saida_s': 0.10, 'abaixo_trilha_db': 12.0,
         'obs': 'tomada a: chiado fino e claro de 0,34 s; a saída de 0,1 s amacia o fim, que no arquivo é seco. '
                'Começa com o plano de corte (P3 = 37,567 s, quadro 1127)'},
        {'nome': 'textura granular do crescimento', 'arquivo': 'textura-granular-b.mp3', 'de': 0.0, 'ate': 1.30,
         'ancora': 'trecho', 'no_ep': 38.167, 'entrada_s': 0.03, 'saida_s': 0.25, 'abaixo_trilha_db': 12.0,
         'obs': 'tomada b: cresce mais devagar (chega ao máximo em 0,55 s), como o osso preenchendo a rosca. '
                'Começa junto com o crescimento do osso (P3 + 0,6 = 38,167 s, quadro 1145; vai até 39,367)'},
        {'nome': 'faixa de luz, brilho suave e seco', 'arquivo': 'brilho-luz-a.mp3', 'de': 0.0, 'ate': 1.20,
         'ancora': 'inicio', 'no_ep': 40.867, 'entrada_s': 0.02, 'saida_s': 0.15, 'abaixo_trilha_db': 12.0,
         'filtro': {'notch_hz': [1605]},
         'obs': 'tomada a: sobe, fica e desce por igual, como uma faixa de luz passando; o filtro tira uma ponta '
                'estreita em 1.605 Hz (15,8 dB acima da vizinhança) para não soar como nota. Começa junto com a '
                'faixa de luz (P4 + 0,2 = 40,867 s, quadro 1226; vai até 41,867)'},
        # ---------------- s09: o vídeo vira o primeiro post (recepção, à tarde) ----------------
        {'nome': 'sopro suave de levar junto', 'arquivo': 'sopro-levar-d.mp3', 'de': 0.10, 'ate': 1.36,
         'ancora': 'pico', 'no_ep': 44.000, 'entrada_s': 0.02, 'saida_s': 0.30, 'pico_alvo_db': -38.0,
         'obs': 'tomada d (2ª rodada): ar claro que cresce, passa (pico no meio do encolhimento, 44,0 s, a parte '
                'mais rápida) e se afasta até ~44,9 s'},
        {'nome': 'ambiente de recepção ao fim de tarde', 'arquivo': 'ambiente-recepcao-tarde-b.mp3', 'de': 0.0,
         'ate': 8.50, 'ancora': 'trecho', 'no_ep': 43.400, 'entrada_s': 0.60, 'saida_s': 0.02,
         'rms_alvo_db': -55.0, 'filtro': {'passa_altas_hz': 100},
         'obs': 'entra em 0,6 s enquanto o mundo aparece em volta do cartão que encolhe; sai seco em 51,9 s, no '
                'corte para s11. O filtro tira o ronco grave de trânsito (abaixo de 100 Hz)'},
        # ---------------- s10: ela encaminha para a turma ----------------
        {'nome': 'toque seco no vidro (abre a conversa)', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 47.300, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0},
        {'nome': 'toque seco no vidro ("encaminhado")', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 47.550, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -35.0},
        {'nome': 'chegada de mensagem (toque seco duplo)', 'arquivo': 'chegada-mensagem-b.mp3', 'de': 0.0,
         'ate': 0.40, 'ancora': 'transiente', 'busca': [0.015, 0.04], 'no_ep': 48.900, 'entrada_s': 0.003,
         'saida_s': 0.08, 'pico_alvo_db': -36.0,
         'obs': 'tomada b: dois toques secos (0,025 e 0,18 s do arquivo, o 2º mais forte), sem nota; a tomada a tem '
                'uma ponta de nota em 4 kHz'},
        # ---------------- s11: a maquete do consultório à tarde ----------------
        {'nome': 'ambiente de consultório à tarde', 'arquivo': 'ambiente-consultorio-tarde-b.mp3', 'de': 0.45,
         'ate': 7.95, 'ancora': 'trecho', 'no_ep': 51.900, 'entrada_s': 0.02, 'saida_s': 0.40,
         'rms_alvo_db': -55.0, 'filtro': {'passa_altas_hz': 80},
         'obs': 'entra seco no corte (51,9 s) e sai em 0,4 s antes do cartão (até 59,4 s); o começo do arquivo '
                '(entrada lenta de 0,45 s) fica de fora'},
        # passos: os 6 passos da tomada b, cada um no seu quadro (a cada 13-14 quadros, ~0,46 s)
        *[{'nome': f'passo {k + 1} (madeira)', 'arquivo': 'passos-madeira-b.mp3', 'de': t_arq - 0.010,
           'ate': t_arq + 0.220, 'ancora': 'transiente', 'busca': [t_arq - 0.006, t_arq + 0.006], 'no_ep': t_ep,
           'entrada_s': 0.003, 'saida_s': 0.12, 'pico_alvo_db': -40.0 - (1.5 if k % 2 else 0.0)}
          for k, (t_arq, t_ep) in enumerate(zip([0.483, 0.846, 1.287, 1.723, 2.197, 2.660],
                                                [52.300, 52.767, 53.233, 53.667, 54.133, 54.600]))],
        {'nome': 'porta fechando suave (fora do quadro)', 'arquivo': 'porta-fechando-a.mp3', 'de': 0.10,
         'ate': 1.20, 'ancora': 'transiente', 'busca': [0.18, 0.26], 'no_ep': 54.750, 'entrada_s': 0.02,
         'saida_s': 0.30, 'pico_alvo_db': -38.0, 'filtro': {'passa_altas_hz': 60},
         'obs': 'tomada a: um "tum" abafado com o trinco, um pouco distante'},
        # s12: nada além da música (e da última fala)
    ],
    'final': {
        'teto_dbtp': -1.2,                    # teto do pico real (um pouco abaixo de -1 por segurança)
        'janela_limitador_ep': [BASE_CORTE + 8.013, 43.40],  # do impacto ao fim do vídeo dela: sem voz
        'limitador_max_db': 6.0,              # se precisar de mais que isso, o script para (baixe a trilha no auge)
        'fade_fim_s': 0.25,
    },
}


def ler(nome, canais=2):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(FONTES, nome), '-ac', str(canais),
                          '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, canais).astype(np.float64)


def env_db(x, ms=1.0):
    """volume (RMS) em janelas de `ms` milissegundos, em dBFS (média dos canais)"""
    hop = max(int(SR * ms / 1000), 1)
    m = x.mean(1) if x.ndim == 2 else x
    n = len(m) // hop
    return 20 * np.log10(np.sqrt((m[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)), hop


def pico_real_db(x):
    return 20 * np.log10(np.abs(resample_poly(x, 4, 1, axis=0)).max() + 1e-12)


def rampa(n, ini, fim):
    return np.linspace(ini, fim, n) if n > 0 else np.zeros(0)


def colocar(destino, trecho, i):
    a, b = max(i, 0), min(i + len(trecho), len(destino))
    if b > a:
        destino[a:b] += trecho[a - i:b - i]


def posicao(e, t_relativo):
    """amostra do episódio onde cai um ponto: itens do corte usam a mesma conta do corte + 1.084.800 amostras"""
    if e.get('do_corte') or 'no_corte' in e:
        return I0 + int(round(t_relativo * SR))
    return int(round(t_relativo * SR))


medidor = pyln.Meter(SR)


def lufs(x):
    if len(x) < int(0.4 * SR):
        return float('nan')
    v = medidor.integrated_loudness(x if x.ndim == 2 else np.c_[x, x])
    return float(v)


doc = {'_sobre': ('Áudio do EPISÓDIO COMPLETO do ep. 01 (sala de espera), versão para aprovação: 0 a 64,0 s. Tempos '
                  'em segundos do EPISÓDIO (a virada começa em 22,6 s; o golpe é o quadro 919 = 30,633 s). De 22,6 a '
                  '33,433 s os sons são os do corte de 10 s aprovado. Gerado por fonte/audio/montar-final.py; para '
                  'mudar, edite o PLANO no script e rode de novo.'),
       'duracao_s': DUR, 'amostragem_hz': SR, 'canais': 2, 'virada_comeca_em_s': BASE_CORTE,
       'golpe_no_episodio_s': GOLPE_EP, 'falas': [], 'eventos': []}

# ---------------- voz: cada fala recortada nas pausas da tomada A, com um ganho fixo por fala ----------------
pv = PLANO['voz']
tomada = ler(pv['arquivo'], 1)[:, 0]
ev_tomada, hop_v = env_db(tomada, 2)
for f in pv['falas']:
    k0, k1 = int(np.ceil(f['de'] / 0.002 - 1e-6)), int(f['ate'] / 0.002 + 1e-6)
    ativo = np.nonzero(ev_tomada[k0:k1] > pv['limiar_fala_dbfs'])[0]
    f['_fala_arq'] = ((k0 + ativo[0]) * 0.002, (k0 + ativo[-1] + 1) * 0.002)
    fa = tomada[int(round(f['_fala_arq'][0] * SR)):int(round(f['_fala_arq'][1] * SR))]
    f['_lufs_cru'] = lufs(fa)
    f['_pico_cru'] = pico_real_db(fa)
ref = next(f for f in pv['falas'] if f['texto'] == pv['referencia'])
for f in pv['falas']:
    f['ganho_db'] = round(pv['ganho_da_referencia_db'] + (ref['_lufs_cru'] - f['_lufs_cru']) + f['ajuste_db'], 2)

voz_mono = np.zeros(N)
fim_anterior_ep = -1.0
fim_clip_anterior = -1
for f in pv['falas']:
    a_t, b_t = int(round(f['de'] * SR)), int(round(f['ate'] * SR))
    fala_ini_arq, fala_fim_arq = f['_fala_arq']
    if f.get('do_corte'):
        assert abs(fala_ini_arq - f['fala_comeca_no_arquivo']) < 0.0015, 'a fala do corte mudou de lugar na tomada'
        inicio_clip_rel = f['fala_comeca_no_corte'] - (f['fala_comeca_no_arquivo'] - f['de'])   # conta do corte
        i_clip = posicao(f, inicio_clip_rel)
        comeca = BASE_CORTE + f['fala_comeca_no_corte']
    else:
        comeca = max(f['alvo'], fim_anterior_ep + pv['pausa_minima_s'])
        i_clip = int(round((comeca - (fala_ini_arq - f['de'])) * SR))
    trecho = tomada[a_t:b_t].copy()
    ne = int(f.get('entrada_s', pv['entrada_saida_s']) * SR)
    ns = int(pv['entrada_saida_s'] * SR)
    trecho[:ne] *= rampa(ne, 0, 1)
    trecho[-ns:] *= rampa(ns, 1, 0)
    trecho *= 10 ** (f['ganho_db'] / 20)
    assert i_clip >= fim_clip_anterior - 2, f'a fala "{f["texto"]}" encostaria na anterior'
    assert i_clip + len(trecho) <= N, f'a fala "{f["texto"]}" passaria do fim do episódio'
    colocar(voz_mono, trecho, i_clip)
    termina = comeca + (fala_fim_arq - fala_ini_arq)
    f['_real'] = dict(comeca=comeca, termina=termina, clip=[i_clip / SR, (i_clip + len(trecho)) / SR],
                      fala_arq=[fala_ini_arq, fala_fim_arq])
    fim_anterior_ep, fim_clip_anterior = termina, i_clip + len(trecho)
voz = np.c_[voz_mono, voz_mono]
t = np.arange(N) / SR

# ---------------- trilha ----------------
pt = PLANO['trilha']
musica_inteira = ler(pt['arquivo'], 2)
a_mus = int(round((pt['golpe_no_arquivo'] - GOLPE_CORTE) * SR)) - I0   # a mesma conta do corte, menos 22,6 s
assert a_mus >= 0 and a_mus + N <= len(musica_inteira), 'a trilha B não cobre o episódio inteiro'
mus_cru = musica_inteira[a_mus:a_mus + N].copy()
# recorte de médias sob cada fala (filtro sem atraso de fase = corte limpo)
banda = sosfiltfilt(butter(2, [1000, 4000], 'bandpass', fs=SR, output='sos'), mus_cru, axis=0)
rr = pt['recorte_rampa_s']
env_rec = np.zeros(N)
janelas_recorte = []
for f in pv['falas']:
    if f.get('do_corte'):
        de, ate = BASE_CORTE + pt['recorte_do_corte'][0], BASE_CORTE + pt['recorte_do_corte'][1]
    else:
        de, ate = f['_real']['comeca'] - pt['recorte_folga_s'], f['_real']['termina'] + pt['recorte_folga_s']
    janelas_recorte.append([round(de, 3), round(ate, 3)])
    env_rec = np.maximum(env_rec, np.interp(t, [de - rr, de, ate, ate + rr], [0, 1, 1, 0], left=0, right=0))
mus_rec = mus_cru + banda * ((10 ** (pt['recorte_medias_db'] / 20) - 1) * env_rec)[:, None]

# volume: pontos até 43,4 s (em dB, linha reta), entrada suave, relaxamento até o leito, realce em s11
pts = np.array(pt['volume'])
vol_db = np.interp(t, pts[:, 0], 20 * np.log10(pts[:, 1]))
e0, e1 = pt['entrada']
x_ent = np.clip((t - e0) / (e1 - e0), 0, 1)
ganho_entrada = np.where(t < e1, np.sin(np.pi / 2 * x_ent), 1.0)
ganho_entrada[t < e0] = 0.0
rx = pt['relaxa']
auge_db = 20 * np.log10(pts[-1, 1])
# o leito: fator constante para a trilha (com recorte) ficar em leito_lufs_sob_a_voz nas falas de referência
idx_ref = np.concatenate([np.arange(int(pv['falas'][k]['_real']['comeca'] * SR), int(pv['falas'][k]['_real']['termina'] * SR))
                          for k in rx['falas_de_referencia']])
# o ganho final ainda não existe aqui: o leito é ajustado em duas passadas (ver mais abaixo, depois do ganho final)
leito_db = -26.0                     # chute inicial; corrigido depois
realce = pt['realce']


def curva_volume(leito_db_):
    v = vol_db.copy()
    u = np.clip((t - rx['de']) / (rx['ate'] - rx['de']), 0, 1)
    p = 1 - (1 - u) ** 2                                     # power2.out
    depois = t >= rx['de']
    v[depois] = auge_db + (leito_db_ - auge_db) * p[depois]
    if realce['db']:
        s0, s1 = realce['sobe']
        sobe = 0.5 - 0.5 * np.cos(np.pi * np.clip((t - s0) / (s1 - s0), 0, 1))
        desce = 0.0
        if realce.get('desce'):
            d0, d1 = realce['desce']
            desce = 0.5 - 0.5 * np.cos(np.pi * np.clip((t - d0) / (d1 - d0), 0, 1))
        v += realce['db'] * (sobe - desce)
    return 10 ** (v / 20) * ganho_entrada


# ---------------- efeitos ----------------
def filtrar(seg, filtro):
    if not filtro:
        return seg
    if filtro.get('passa_altas_hz'):
        seg = sosfiltfilt(butter(2, filtro['passa_altas_hz'], 'highpass', fs=SR, output='sos'), seg, axis=0)
    for nf in filtro.get('notch_hz', []):
        b, a = iirnotch(nf, 8, SR)
        seg = filtfilt(b, a, seg, axis=0)
    return seg


def montar_evento(e, mus_atual):
    src = ler(e['arquivo'], 2)
    seg = src[int(round(e['de'] * SR)):int(round(e['ate'] * SR))].copy()
    seg = filtrar(seg, e.get('filtro'))
    en, h = env_db(seg, 1)
    if e['ancora'] == 'transiente':
        b0, b1 = int((e['busca'][0] - e['de']) * 1000), int((e['busca'][1] - e['de']) * 1000)
        b0 = max(b0, 0)
        anc = (b0 + int(np.argmax(en[b0:b1] >= en[b0:b1].max() - 6))) * h / SR
    elif e['ancora'] == 'inicio':
        anc = int(np.argmax(en >= en.max() - 30)) * h / SR
    elif e['ancora'] == 'trecho':
        anc = 0.0
    elif e['ancora'] == 'pico':
        e20, h20 = env_db(seg, 20)
        anc = (int(np.argmax(e20)) + 0.5) * h20 / SR
    else:
        anc = len(seg) / SR
    ne, ns = int(e['entrada_s'] * SR), int(e['saida_s'] * SR)
    seg[:ne] *= rampa(ne, 0, 1)[:, None]
    seg[len(seg) - ns:] *= rampa(ns, 1, 0)[:, None]
    rel = (e['no_corte'] if 'no_corte' in e else e['no_ep']) - anc
    i = posicao(e, rel)
    if 'rms_alvo_db' in e:
        medido = 20 * np.log10(np.sqrt((seg[int(0.1 * SR):-ns or None] ** 2).mean()) + 1e-12)
        ganho = e['rms_alvo_db'] - medido
        refg = f"RMS {medido:.1f} dBFS -> {e['rms_alvo_db']:.1f}"
    elif 'abaixo_trilha_db' in e:
        medido = lufs(seg)
        trilha_ali = lufs(mus_atual[max(i, 0):i + len(seg)])
        ganho = trilha_ali - e['abaixo_trilha_db'] - medido
        refg = f"LUFS {medido:.1f} -> {trilha_ali - e['abaixo_trilha_db']:.1f} ({e['abaixo_trilha_db']:.0f} LU abaixo da trilha ali)"
    else:
        medido = en.max()
        ganho = e['pico_alvo_db'] - medido
        refg = f"pico 1 ms {medido:.1f} dBFS -> {e['pico_alvo_db']:.1f}"
    seg *= 10 ** (ganho / 20)
    return seg, anc, ganho, refg, i


def montar_efeitos(mus_atual, registrar):
    fx_ = np.zeros((N, 2))
    g_amb = None
    for e in PLANO['efeitos']:
        seg, anc, ganho, refg, i = montar_evento(e, mus_atual)
        colocar(fx_, seg, i)
        if e['arquivo'].startswith('ambiente-noite') and 'no_corte' in e:
            g_amb = ganho
        if registrar:
            no_ep = BASE_CORTE + e['no_corte'] if 'no_corte' in e else e['no_ep']
            doc['eventos'].append({'nome': e['nome'], 'arquivo': 'assets/audio/fontes/' + e['arquivo'],
                                   'origem': ('corte de 10 s (sem mudança)' if 'no_corte' in e else
                                              ('novo (ep. completo)' if no_ep > 33.433 else 'corte ampliado, tempo novo')),
                                   'trecho_do_arquivo_s': [e['de'], e['ate']], 'ancora': e['ancora'],
                                   'ancora_no_arquivo_s': round(e['de'] + anc, 3), 'no_episodio_s': round(no_ep, 3),
                                   'toca_no_episodio_s': [round(i / SR, 3), round((i + len(seg)) / SR, 3)],
                                   'ganho_db': round(ganho, 1), 'referencia_do_ganho': refg,
                                   **({'filtro': e['filtro']} if 'filtro' in e else {}),
                                   **({'obs': e['obs']} if 'obs' in e else {})})
            print(f"{e['nome']:<50} {e['arquivo']:<32} âncora {e['de'] + anc:6.3f} s -> {no_ep:6.3f} s, "
                  f"ganho {ganho:+5.1f} dB")
    return fx_, g_amb


def leito_noturno(g_amb):
    pl = PLANO['leito_ambiente']
    amb = ler(pl['arquivo'], 2)
    mono = amb.mean(1)
    L = len(amb)
    nc = int(pl['cruzamento_s'] * SR)
    cauda = mono[L - nc:]
    melhor, melhor_c = 0, -2.0
    for s in range(int(pl['busca_emenda_s'][0] * SR), int(pl['busca_emenda_s'][1] * SR), 24):
        cab = mono[s:s + nc]
        c = float(np.dot(cauda, cab) / (np.linalg.norm(cauda) * np.linalg.norm(cab) + 1e-12))
        if c > melhor_c:
            melhor, melhor_c = s, c
    fim_leito = int(round(pl['fim_ep'] * SR)) + int(pl['saida_s'] * SR)
    leito = np.zeros((fim_leito, 2))
    pos, ini_arq, copias, emendas = 0, 0, 0, []
    fade_out = np.cos(np.linspace(0, np.pi / 2, nc))[:, None]
    fade_in = np.sin(np.linspace(0, np.pi / 2, nc))[:, None]
    while True:
        pedaco = amb[ini_arq:].copy()
        if copias > 0:
            pedaco[:nc] *= fade_in
        ultima = pos + len(pedaco) >= fim_leito
        if not ultima:
            pedaco[-nc:] *= fade_out
        colocar(leito, pedaco, pos)
        copias += 1
        if ultima:
            break
        pos, ini_arq = pos + len(pedaco) - nc, melhor
        emendas.append(round(pos / SR, 3))
    na = int(pl['entrada_s'] * SR)
    leito[:na] *= rampa(na, 0, 1)[:, None]
    nsa = int(pl['saida_s'] * SR)
    leito[-nsa:] *= rampa(nsa, 1, 0)[:, None]
    leito *= 10 ** (g_amb / 20)
    out = np.zeros((N, 2))
    colocar(out, leito, 0)
    info = {'nome': pl['nome'], 'arquivo': 'assets/audio/fontes/' + pl['arquivo'],
            'toca_no_episodio_s': [0.0, round(fim_leito / SR, 3)],
            'saida': f"{pl['saida_s'] * 1000:.0f} ms (22,60-22,64 s), por baixo da entrada do ambiente do corte",
            'copias': copias, 'cruzamento_s': pl['cruzamento_s'], 'emendas_no_episodio_s': emendas,
            'cada_copia_seguinte_comeca_no_arquivo_s': round(melhor / SR, 3),
            'semelhanca_na_emenda_0a1': round(melhor_c, 2), 'ganho_db': round(g_amb, 1)}
    return out, info


def limitar(bus, j0, j1, teto):
    """limitador com 1,5 ms de antecipação e 60 ms de soltura, só entre j0 e j1 (+0,3 s de soltura)"""
    os4 = np.abs(resample_poly(bus, 4, 1, axis=0)).max(1)
    pico_amostra = os4[:len(os4) // 4 * 4].reshape(-1, 4).max(1)
    pico_amostra = np.r_[pico_amostra, np.zeros(N - len(pico_amostra))][:N]
    g = np.ones(N)
    g[j0:j1] = np.minimum(1.0, teto / (pico_amostra[j0:j1] + 1e-12))
    olhar = int(0.0015 * SR)
    g = minimum_filter1d(g, size=2 * olhar + 1, mode='nearest')
    solta = np.exp(-1.0 / (0.060 * SR))
    fim = min(j1 + int(0.3 * SR), N)
    for i in range(j0, fim):
        g[i] = min(g[i], 1 - (1 - g[i - 1]) * solta) if i > 0 else g[i]
    g[:j0 - olhar] = 1.0
    g[fim:] = 1.0
    return g


# ---------------- duas passadas: (1) ganho final e leito; (2) mix final ----------------
pf = PLANO['final']
teto = 10 ** (pf['teto_dbtp'] / 20)
j0 = int(round(pf['janela_limitador_ep'][0] * SR))
j1 = int(round(pf['janela_limitador_ep'][1] * SR))
ganho_final = 12.32                   # chute inicial (o do corte); recalculado na passada
for passada in range(4):
    vol = curva_volume(leito_db)
    mus = mus_rec * vol[:, None]
    fx, g_amb = montar_efeitos(mus, registrar=False)
    leito_n, _ = leito_noturno(g_amb)
    fx += leito_n
    # o ganho final: o maior possível sem nada FORA da janela do limitador passar do teto (é aí que está a voz)
    pre = voz + mus + fx
    os_all = np.abs(resample_poly(pre, 4, 1, axis=0)).max(1)
    fora = np.ones(len(os_all), bool)
    fora[j0 * 4:(j1 + int(0.3 * SR)) * 4] = False
    k_pico = int(np.argmax(np.where(fora, os_all, 0)))
    ganho_final = pf['teto_dbtp'] - 20 * np.log10(os_all[k_pico] + 1e-12)
    t_pico = k_pico / 4 / SR
    # corrige o leito para a trilha (com recorte, depois do ganho final) ficar no alvo sob as falas de referência
    medido = lufs(mus[idx_ref]) + ganho_final
    erro = rx['leito_lufs_sob_a_voz'] - medido
    leito_db += erro
    if abs(erro) < 0.05:
        break
vol = curva_volume(leito_db)
mus = mus_rec * vol[:, None]
fx, g_amb = montar_efeitos(mus, registrar=True)
leito_n, info_leito = leito_noturno(g_amb)
fx += leito_n
doc['leito_ambiente'] = info_leito
quem_pico = next((f['texto'] for f in pv['falas'] if f['_real']['clip'][0] <= t_pico <= f['_real']['clip'][1]),
                 'não é voz')

gf = 10 ** (ganho_final / 20)
bus = (mus + fx) * gf
g_lim = limitar(bus, j0, j1, teto)
age = np.nonzero(g_lim < 0.99999)[0]
# onde o limitador mais age (trechos com mais de 3 dB)
forte = np.nonzero(g_lim < 10 ** (-3 / 20))[0]
trechos_forte = []
for k in forte:
    if trechos_forte and k - trechos_forte[-1][1] < int(0.05 * SR):
        trechos_forte[-1][1] = k
    else:
        trechos_forte.append([k, k])
trechos_forte = [[round(a / SR, 3), round(b / SR, 3), round(float(-20 * np.log10(g_lim[a:b + 1].min())), 1)]
                 for a, b in trechos_forte]
reducao_max = -20 * np.log10(g_lim.min())
if reducao_max > pf['limitador_max_db']:
    raise SystemExit(f'o limitador precisaria de {reducao_max:.1f} dB (máximo {pf["limitador_max_db"]}): baixe o auge')
bus *= g_lim[:, None]
mix = voz * gf + bus
nf = int(pf['fade_fim_s'] * SR)
mix[-nf:] *= rampa(nf, 1, 0)[:, None] ** 2
mix = mix[:N]
# conferência: nada passa do teto (fora do limitador é a conta do ganho; dentro, o limitador)
os_fin = np.abs(resample_poly(mix, 4, 1, axis=0)).max(1)
p_fin = 20 * np.log10(os_fin.max() + 1e-12)
if p_fin > pf['teto_dbtp'] + 0.02:
    raise SystemExit(f'pico real {p_fin:.2f} dBTP em {np.argmax(os_fin) / 4 / SR:.3f} s passa do teto')
saida = os.path.join(AUDIO, 'mix-final.wav')
sf.write(saida, mix.astype(np.float32), SR, subtype='PCM_24')


# ---------------- medições do arquivo final (ffmpeg ebur128 = medidor padrão) ----------------
def ebur128(caminho):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', caminho, '-af', 'ebur128=peak=true:framelog=quiet', '-f',
                        'null', '-'], capture_output=True, text=True).stderr
    return (float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1]),
            float(re.findall(r'LRA:\s+(-?[\d.]+) LU', e)[-1]))


lufs_i, tp, lra = ebur128(saida)
info = sf.info(saida)
vz, mz, fz = voz * gf, mus * gf * g_lim[:, None], fx * gf * g_lim[:, None]
falando = np.zeros(N, bool)
for f in pv['falas']:
    r = f['_real']
    ii, jj = int(r['comeca'] * SR), int(r['termina'] * SR)
    falando[ii:jj] = True
    doc['falas'].append({'texto': f['texto'], 'alvo_s': f['alvo'], 'comeca_s': round(r['comeca'], 3),
                         'termina_s': round(r['termina'], 3), 'deslizou_s': round(r['comeca'] - f['alvo'], 3),
                         'trecho_da_tomada_s': [f['de'], f['ate']],
                         'fala_na_tomada_s': [round(r['fala_arq'][0], 3), round(r['fala_arq'][1], 3)],
                         'clip_no_episodio_s': [round(r['clip'][0], 3), round(r['clip'][1], 3)],
                         'lufs_na_tomada': round(f['_lufs_cru'], 1),
                         'ganho_db': f['ganho_db'], 'ganho_total_db': round(f['ganho_db'] + ganho_final, 2),
                         'lufs_no_mix': round(lufs(vz[ii:jj]), 1),
                         'pico_real_dbtp': round(pico_real_db(vz[ii:jj]), 2),
                         'trilha_por_baixo_lufs': round(lufs(mz[ii:jj]), 1),
                         **({'obs': f['obs']} if 'obs' in f else {}),
                         **({'origem': 'corte de 10 s'} if f.get('do_corte') else {})})
idx = np.nonzero(falando)[0]
lufs_voz = lufs(vz[idx])
lufs_mus_sob = lufs(mz[idx])
lufs_fx_sob = lufs(fz[idx])
ef, hf = env_db(mix, 1)
k0, k1 = int((GOLPE_EP - 0.083) * 1000), int((GOLPE_EP + 0.267) * 1000)
golpe_real = (k0 + int(np.argmax(ef[k0:k1] >= ef[k0:k1].max() - 12))) * hf / SR
for ev_ in doc['eventos']:
    ev_['ganho_total_db'] = round(ev_['ganho_db'] + ganho_final, 1)
    a_, b_ = ev_['toca_no_episodio_s']
    ev_['lufs_no_mix'] = round(lufs(fz[int(a_ * SR):int(b_ * SR)]), 1) if ev_['nome'].startswith('ambiente') else None
    if ev_['lufs_no_mix'] is None:
        del ev_['lufs_no_mix']
trilha_por_frase = {}
for a_, b_ in pt['frases_do_piano'] + [[20.636, 22.6], [22.6, 23.966], [30.633, 33.433], [33.433, 37.0], [37.0, 40.4],
                                      [40.4, 43.4], [43.85, 47.0], [47.0, 51.9], [51.9, 53.6], [54.8, 57.96],
                                      [57.96, 59.5], [59.6, 62.8], [62.8, 64.0]]:
    trilha_por_frase[f'{a_:g}-{b_:g}'] = round(lufs(mz[int(a_ * SR):int(b_ * SR)]), 1)
# volume do mix inteiro por trecho (para ver o desenho do episódio)
por_cena = {}
for nome_c, (a_, b_) in {'s01': (0, 9.3), 's03': (9.3, 15.3), 's04': (15.3, 18.3), 's05': (18.3, 22.6),
                         'virada até o impacto': (22.6, 30.633), 's08 (vídeo dela)': (30.633, 43.4),
                         's09': (43.4, 46.9), 's10': (46.9, 51.9), 's11': (51.9, 59.3), 's12': (59.3, 64.0)}.items():
    por_cena[nome_c] = round(lufs(mix[int(a_ * SR):int(b_ * SR)]), 1)

# teste de subtração: a virada (22,64 s até 33,18 s, antes do fade de fim do corte) contra o corte de 10 s aprovado
corte, sr_c = sf.read(os.path.join(AUDIO, 'mix-corte10s.wav'), dtype='float64')
novo = sf.read(saida, dtype='float64')[0][I0:I0 + N_CORTE]
k_amb = int(0.040 * SR)
k_fim = N_CORTE - int(0.25 * SR)
dif = novo[:k_fim] - corte[:k_fim]


def nivel(x):
    return round(float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-15)), 1)


subtracao = {'nivel_do_corte_dbfs': nivel(corte[k_amb:k_fim]),
             'diferenca_22_60_a_22_64_dbfs': nivel(dif[:k_amb]),
             'diferenca_de_22_64_a_33_18_dbfs': nivel(dif[k_amb:]),
             'maior_diferenca_de_22_64_a_33_18_dbfs': round(float(20 * np.log10(np.abs(dif[k_amb:]).max() + 1e-15)), 1),
             'diferenca_por_segundo_dbfs': {f'{BASE_CORTE + s:.1f}': nivel(dif[int(s * SR):int((s + 1) * SR)])
                                            for s in range(0, 10)}}

doc['trilha'] = {'arquivo': 'assets/audio/fontes/' + pt['arquivo'], 'candidata': 'B (2ª de 3)',
                 'golpe_no_arquivo_s': pt['golpe_no_arquivo'], 'golpe_no_episodio_s': GOLPE_EP,
                 'deslocamento_s': round(a_mus / SR, 3),
                 'musica_tocada_s': [round((a_mus + int(e0 * SR)) / SR, 3), round((a_mus + N) / SR, 3)],
                 'entrada_s': pt['entrada'], 'volume_fator_ate_43_4': pt['volume'],
                 'relaxa': {**rx, 'leito_fator': round(10 ** (leito_db / 20), 4), 'leito_db': round(leito_db, 2)},
                 'realce_em_s11': realce,
                 'recorte_medias': {'faixa_hz': [1000, 4000], 'db': pt['recorte_medias_db'],
                                    'janelas_s': janelas_recorte, 'rampa_s': rr},
                 'tratamento': ('sem esticar e sem cortar; só deslocada (tempo da música = tempo do episódio + '
                                '6,044 s), com entrada de 1,0 s e volume em curvas lentas'),
                 # medido à parte (cromagrama: quanto de cada nota soa a cada 0,1 s), com a música crua
                 'harmonia_medida': {
                     'tom': 'lá menor; depois do golpe a trilha B gira lá menor -> fá -> dó -> sol (a cada ~3,3 s) e '
                            'segue no volume cheio, com pulso, até 57,96 s do episódio; não relaxa sozinha',
                     'resolucao_no_episodio_s': 57.31, 'resolucao_na_musica_s': 63.35,
                     'resolucao': 'sol (tensão, de ~54,46 a 57,3 s) -> lá menor (o tom da música), com o salto de '
                                  'volume do acorde em 57,31 s; não existe acorde maior de resolução na trilha B',
                     'faltava_a_forma_54_8': 'cai sobre o acorde de sol (a tensão que pede a resolução)',
                     'dedicatoria_56_9': 'a resolução chega 0,41 s depois de a dedicatória pousar',
                     'depois': 'de 57,96 s em diante a música vai sumindo sozinha até o fim (fade natural); duas notas '
                               'de piano em 59,79 e 60,63 s, sob a última fala'}}
doc['final'] = {'arquivo': 'assets/audio/mix-final.wav', 'duracao_s': round(info.frames / SR, 4),
                'formato': 'WAV PCM 24 bits', 'amostras': info.frames, 'amostragem_hz': info.samplerate,
                'canais': info.channels, 'ganho_fixo_final_db': round(ganho_final, 2),
                'ganho_limitado_por': f'pico real em {t_pico:.3f} s ({quem_pico})',
                'limitador': {'so_na_trilha_e_efeitos': True, 'janela_s': pf['janela_limitador_ep'],
                              'agiu_de_ate_s': [round(age[0] / SR, 3), round(age[-1] / SR, 3)] if len(age) else [],
                              'reducao_maxima_db': round(reducao_max, 2),
                              'tempo_com_mais_de_1_db_s': round(float((g_lim < 10 ** (-1 / 20)).sum() / SR), 3),
                              'tempo_com_mais_de_3_db_s': round(float((g_lim < 10 ** (-3 / 20)).sum() / SR), 3),
                              'trechos_com_mais_de_3_db_s_e_db': trechos_forte,
                              'teto_dbtp': pf['teto_dbtp']},
                'fade_fim_s': pf['fade_fim_s'],
                'medicoes': {'lufs_integrado': lufs_i, 'pico_real_dbtp': tp, 'lra_lu': lra,
                             'golpe_no_episodio_s': round(golpe_real, 3),
                             'voz_lufs_nas_falas': round(lufs_voz, 1),
                             'trilha_lufs_sob_a_voz': round(lufs_mus_sob, 1),
                             'efeitos_lufs_sob_a_voz': round(lufs_fx_sob, 1),
                             'voz_acima_da_trilha_db': round(lufs_voz - lufs_mus_sob, 1),
                             'mix_lufs_por_cena': por_cena,
                             'trilha_sozinha_lufs_por_trecho': trilha_por_frase},
                'teste_de_subtracao_contra_o_corte_de_10s': subtracao}
doc['_ganhos'] = ('ganho_db = ganho próprio da fala/evento (antes do ganho fixo final); ganho_total_db = ganho_db + '
                  'ganho fixo final, ou seja, quanto o arquivo de origem foi aumentado/abaixado no mix final.')
for f in pv['falas']:
    for k in [k for k in f if k.startswith('_')]:
        f.pop(k)
with open(os.path.join(AUDIO, 'audio-final.json'), 'w', encoding='utf-8') as fo:
    json.dump(doc, fo, ensure_ascii=False, indent=1)

print(f'\nganho fixo final {ganho_final:+.2f} dB (limitado pelo pico real em {t_pico:.3f} s: {quem_pico})')
print(f'leito da trilha depois de 43,4 s: fator {10 ** (leito_db / 20):.4f} ({leito_db:.1f} dB)')
print(f'limitador (trilha+efeitos, {pf["janela_limitador_ep"]}): {reducao_max:.2f} dB no máximo; '
      f'{doc["final"]["limitador"]["tempo_com_mais_de_1_db_s"]} s com mais de 1 dB, '
      f'{doc["final"]["limitador"]["tempo_com_mais_de_3_db_s"]} s com mais de 3 dB; trechos > 3 dB: {trechos_forte}')
print(f'FINAL: {lufs_i:.1f} LUFS, pico real {tp:.1f} dBTP, LRA {lra} LU, {info.frames / SR:.4f} s, '
      f'{info.samplerate} Hz, {info.channels} canais')
for fl in doc['falas']:
    print(f"  {fl['comeca_s']:6.3f}-{fl['termina_s']:6.3f} s (alvo {fl['alvo_s']:5.2f}, deslizou {fl['deslizou_s']:+.3f}) "
          f"ganho {fl['ganho_db']:+5.2f} -> {fl['lufs_no_mix']:6.1f} LUFS, pico {fl['pico_real_dbtp']:6.2f} dBTP, "
          f"trilha {fl['trilha_por_baixo_lufs']:6.1f}  {fl['texto']}")
print(f'voz {lufs_voz:.1f} LUFS; trilha sob a voz {lufs_mus_sob:.1f} LUFS ({lufs_voz - lufs_mus_sob:.1f} dB abaixo); '
      f'efeitos sob a voz {lufs_fx_sob:.1f} LUFS')
print('trilha sozinha, LUFS por trecho:', trilha_por_frase)
print('mix por cena:', por_cena)
print(f'golpe no arquivo final: {golpe_real:.3f} s (alvo {GOLPE_EP:.3f})')
print('subtração contra o corte de 10 s:', subtracao)
print('->', saida)
