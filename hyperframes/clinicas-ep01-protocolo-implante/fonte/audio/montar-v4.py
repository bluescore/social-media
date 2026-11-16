"""Monta o áudio do EPISÓDIO COMPLETO v4 do ep. 01 (2º pedido do dono, 12/11/2026): 0 a 71,7 s.

v4 = o montar-v3.py com SÓ duas falas trocadas (fonte/PLANO-v4.md, pedidos 4 e 9):
  F  "quarenta e sete dias sem postar nada."  ->  "dezessete dias sem postar nada."  (tomada narracao-v4-novas-c)
  10 "ela mandou o vídeo pra turma."          ->  "ela mandou o vídeo pra Lúcia."    (tomada narracao-v4-novas-a)
Mesmos alvos (F 15,55; 10 53,80), mesmas regras. Todo o resto (música, efeitos, ambientes, as outras 14 falas, o ganho
final) fica IDÊNTICO ao mix-v3.wav. Duas coisas garantem isso:
  - o leito da trilha (o volume dela depois de 46,5 s) fica CONGELADO no valor exato da v3 (PLANO['trilha']['relaxa']
    ['leito_db_fixo']). Ele era calibrado pelas falas 9, 10, 11 e 12; com a fala 10 nova, recalcular mudaria (um
    pouquinho) a música de 46,5 s até o fim. Congelado, só muda o recorte de médias sob F e sob 10 (ele acompanha a
    duração nova das falas);
  - o script confere no fim, com um teste de subtração contra o mix-v3.wav, que fora das janelas de F e de 10 (com
    folga) a diferença é zero.
A v3 continua intacta (montar-v3.py, mix-v3.wav, audio-v3.json e voz-v3.palavras.json não mudam).

O texto abaixo é o cabeçalho da v3, que continua valendo:

É o montar-final.py (v2 aprovada) adaptado à linha do tempo v3 (fonte/PLANO-v3.md). A v2 continua intacta
(montar-final.py e mix-final.wav não mudam).

Linha do tempo v3 (segundos do episódio, 30 quadros por segundo):
  s01 0-9,3 · s03 9,2-15,3 · s04 15,3-18,3 · s04b (NOVA) 18,3-21,6 · s05 21,6-25,9
  virada 25,9-34,733 (IMPACTO em 33,933 = quadro 1018) · s08 34,733-46,7 (o vídeo dela, sem voz)
  s09 46,7-53,5 · s10 53,5-58,5 · s11 58,5-67,5 · s12 66,9-71,7
Em relação à v2: até 18,3 s nada muda de lugar; de s05 até s09 tudo andou +3,3 s (a cena nova s04b); s09 ganhou
+3,3 s no fim, então s10 e s11 andaram +6,6 s.

De 25,9 s em diante (até onde o corte terminava, 36,733 s) os sons da virada são os do corte de 10 s aprovado
(montar-corte10s.py): os mesmos arquivos, recortes, volumes e tempos, só deslocados 25,9 s (1.243.200 amostras).
O script confere isso no fim (teste de "subtração" contra mix-corte10s.wav).

Regras que este script segue (regras do dono, as mesmas da v2):
  - a voz NUNCA é esticada, acelerada, emendada nem limitada: cada fala é recortada da sua tomada só no meio das
    pausas e colocada no seu tempo; se uma fala não cabe antes da próxima, a próxima desliza (o mínimo possível);
  - cada fala recebe UM ganho fixo (o mesmo do começo ao fim dela), calculado para todas ficarem com o mesmo volume
    percebido (LUFS) da fala de referência ("cada linha..."); nada de limitador nem compressor na voz;
  - a trilha NUNCA é esticada nem cortada: ela só é deslocada para o golpe cair em 33,933 s (tempo da música =
    tempo do episódio + 2,744 s) e tem o volume ajustado (curvas lentas). Única exceção, a regra abaixo;
  - a trilha é EMENDADA UMA VEZ SÓ, NO FIM, alinhada no compasso (PLANO['trilha']['emenda_fim']). Por quê: com o
    golpe em 33,933 s e o episódio com 71,7 s, a música acaba antes do vídeo: ela resolve em 60,61 s, some sozinha,
    e a chamada final ("comente CLÍNICA...", 67,65 s) e o cartão (66,9-71,7) ficariam no vazio, com silêncio digital
    de ~70,2 s até o fim. Como: em 61,03-61,45 s a trilha cruza (potência igual) para uma 2ª cópia da MESMA trilha,
    exatamente 2 compassos atrás (6,6685 s), num ponto em que as notas das duas cópias combinam (conferido por
    cromagrama). A batida continua no lugar, nada é esticado, nenhuma música nova entra. Tudo antes da emenda fica
    idêntico (o leito é calibrado sem ela, e o ganho final não pode ser decidido por nada depois dela). Não faça outra
    emenda de música em lugar nenhum do episódio;
  - um ganho fixo final (o mesmo do começo ao fim), o maior possível sem a voz passar de -1,2 dBTP;
  - o limitador (que segura picos) só age na trilha + efeitos, só entre o impacto e o fim do vídeo dela
    (33,913-46,7 s), onde não há voz; a voz é somada depois, então ela nunca passa por ele;
  - fade de 0,25 s só no fim (no mix inteiro; a trilha emendada tem também o seu fade de 0,5 s, 71,2-71,7, que
    chega a zero em 71,7); os efeitos têm só entradas/saídas curtas para não estalar.

Para mudar alguma coisa, mexa no PLANO abaixo e rode de novo (dentro da pasta do episódio):
    python -I fonte/audio/montar-v4.py
    (opcional: --voz-sozinha <arquivo.wav> grava também só a voz já posicionada, para conferir com o Whisper)
Entradas: assets/audio/fontes/*.mp3 (tudo do ElevenLabs), fonte/audio/*.palavras.json (Whisper das tomadas),
          assets/audio/mix-corte10s.wav e assets/audio/mix-v3.wav + audio-v3.json + voz-v3.palavras.json (só para
          conferir)
Saídas:   assets/audio/mix-v4.wav (48 kHz, estéreo, 24 bits, 71,7 s)
          assets/audio/audio-v4.json (cada fala e cada evento: arquivo, tempo, ganho; medições; escolhas)
          assets/audio/voz-v4.palavras.json (tempo de cada palavra de cada fala, em segundos do episódio)
"""
import json
import os
import re
import subprocess
import sys
import unicodedata
from difflib import SequenceMatcher

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.ndimage import minimum_filter1d
from scipy.signal import butter, iirnotch, resample_poly, sosfiltfilt, filtfilt

sys.stdout.reconfigure(encoding='utf-8')
AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(os.path.dirname(AQUI))
AUDIO = os.path.join(PECA, 'assets', 'audio')
FONTES = os.path.join(AUDIO, 'fontes')
SR = 48000
DUR = 71.7
N = int(round(DUR * SR))              # 3.441.600 amostras
BASE_CORTE = 25.9                     # onde o corte de 10 s começa no episódio (a virada)
I0 = int(round(BASE_CORTE * SR))      # 1.243.200 amostras
DUR_CORTE = 10.833
N_CORTE = int(round(DUR_CORTE * SR))
GOLPE_CORTE = 8.033                   # quadro 241 do corte (a mesma conta do corte e da v2)
GOLPE_EP = BASE_CORTE + GOLPE_CORTE   # 33,933 s = quadro 1018 do episódio
TOMADA_A = 'narracao-amedeiros-v4-a.mp3'

# ----------------------------------------------------------------------------------------------------------------
# PLANO
# Tempos "no_ep" = segundos do episódio. Tempos "no_corte" (itens do corte de 10 s) = segundos do corte, copiados
# sem mudança do montar-corte10s.py; eles caem em no_corte + 25,9 s do episódio.
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
# "origem": de onde vem a escolha (v2 no mesmo tempo, v2 deslocado, corte de 10 s, ou novo da v3).
# ----------------------------------------------------------------------------------------------------------------
REF_A = {'f0_hz': 123.8, 'ritmo_silabas_por_s': 6.73, 'plr_max_db': 18.17}
REF_A_V4 = {'f0_hz': 125.2, 'ritmo_silabas_por_s': 6.73, 'plr_max_db': 18.17,
            'obs': 'a altura da tomada A medida de novo com o método da v4 (Praat padrão, mediana); ritmo e PLR iguais'}
PLANO = {
    'voz': {
        'limiar_fala_dbfs': -50.0,      # a fala "existe" onde o volume (janelas de 2 ms) passa disso, na tomada crua
        'pausa_minima_s': 0.25,         # se uma fala não cabe, a próxima começa 0,25 s depois do fim dela
        'entrada_saida_s': 0.015,       # entrada/saída de 15 ms, dentro das pausas (silêncio)
        # IGUALAR: cada fala recebe ganho = ganho_da_referencia + (LUFS da referência - LUFS da fala) + ajuste_db.
        # A referência é a fala do corte ("cada linha..."), que fica com o MESMO ganho do corte aprovado (-7,6 dB);
        # ela e "décima quarta tentativa." são as que têm o pico mais alto para o seu volume (PLR 18,2 dB), então são
        # elas que decidem até onde a voz inteira pode subir. Uma fala nova com PLR maior que isso derrubaria o ganho
        # final de tudo (e a virada deixaria de ser igual ao corte aprovado): por isso a tomada c da fala 14 ficou de fora.
        'referencia': '8',
        'ganho_da_referencia_db': -7.6,
        # de/ate = trecho da tomada (no meio das pausas); alvo = onde a fala deve começar no episódio.
        # Falas antigas: tomada A, os MESMOS trechos da v2 (só o alvo mudou). Falas novas: tomadas narracao-v3-novas.
        # v4: F e 10 vêm das tomadas narracao-v4-novas (as outras 14 falas ficam exatamente como na v3).
        'falas': [
            {'id': '1', 'texto': 'décima quarta tentativa.', 'de': 0.000, 'ate': 2.093, 'alvo': 0.10, 'ajuste_db': 0.0,
             'entrada_s': 0.003, 'obs': 'a tomada começa já falando (0,002 s): entrada de 3 ms'},
            {'id': '2', 'texto': 'e o vídeo não sai.', 'de': 2.217, 'ate': 3.668, 'alvo': 2.32, 'ajuste_db': 0.0},
            {'id': '3', 'texto': 'a doutora Helena explica a prótese protocolo toda semana, paciente por paciente.',
             'de': 3.732, 'ate': 8.950, 'alvo': 3.95, 'ajuste_db': 0.0},
            {'id': '4', 'texto': 'o roteiro sobre implantes está pronto há seis semanas.', 'de': 8.950, 'ate': 12.281,
             'alvo': 9.45, 'ajuste_db': 0.0},
            {'id': '5', 'texto': 'a gravação, não.', 'de': 12.281, 'ate': 13.904, 'alvo': 12.95, 'ajuste_db': 0.0,
             'obs': 'o "não" fica de +0,92 a +1,16 s do começo da fala (13,87-14,11 s); o risco é 13,70-14,05'},
            # ---- v4 (pedido 4 do PLANO-v4): o feed parado há 17 dias (na v3 era "quarenta e sete dias..." da tomada
            # narracao-v3-novas-c, 0-2,847). Tomada v4 c, de 0 (a tomada tem 0,036 s de silêncio antes de "dezessete")
            # até o ponto mais silencioso da pausa entre "nada." e "ela" (2,775 s, -90,7 dBFS; a pausa vai de 2,468 a
            # 2,842 s)
            {'id': 'F', 'texto': 'dezessete dias sem postar nada.', 'arquivo': 'narracao-v4-novas-c.mp3',
             'de': 0.000, 'ate': 2.775, 'alvo': 15.55, 'ajuste_db': 0.0,
             'obs': ('v4: troca de "quarenta e sete" por "dezessete" (pedido 4 do PLANO-v4); a fala dura 2,432 s, '
                     '0,064 s menos que a da v3')},
            # ---- NOVA (pedido 6): a virada antes da 15ª. Tomada c, do ponto mais silencioso (2,847) até o meio da pausa
            # depois de "mudar..." (5,033). Uma fala só: na tomada, "mas" sai colado em "isso" ("ma-zi-sso"); a pausa
            # natural da leitura fica depois de "está" (3,73-3,91 s da tomada, 0,18 s), antes de "prestes a mudar"
            {'id': 'T', 'texto': 'mas isso está prestes a mudar...', 'arquivo': 'narracao-v3-novas-c.mp3',
             'de': 2.847, 'ate': 5.033, 'alvo': 18.60, 'ajuste_db': 0.0},
            {'id': '6', 'texto': 'ela não gravou a décima quinta.', 'de': 13.974, 'ate': 15.813, 'alvo': 21.90,
             'ajuste_db': 0.0},
            {'id': '7', 'texto': 'mandou só o roteiro.', 'de': 15.813, 'ate': 17.090, 'alvo': 24.20, 'ajuste_db': 0.0},
            # a fala do corte de 10 s, exatamente como lá (17,090-19,775 s da tomada; a fala começa em 1,000 do corte)
            {'id': '8', 'texto': 'cada linha que ela escreveu virou uma cena.', 'de': 17.090, 'ate': 19.775,
             'alvo': BASE_CORTE + 1.0, 'ajuste_db': 0.0, 'do_corte': True, 'fala_comeca_no_arquivo': 17.290,
             'fala_comeca_no_corte': 1.000},
            {'id': '9', 'texto': 'o perfil voltou a andar.', 'de': 19.775, 'ate': 21.449, 'alvo': 47.00, 'ajuste_db': 0.0},
            # ---- v4 (pedido 9 do PLANO-v4): ela manda o vídeo para a paciente, não para a turma (na v3 era "ela mandou
            # o vídeo pra turma." da tomada A, 21,449-23,020). Tomada v4 a, do ponto mais silencioso da pausa entre
            # "nada." e "ela" (2,869 s, -90,8 dBFS; a pausa vai de 2,498 a 2,918 s) até o ponto mais silencioso do
            # silêncio do fim (4,463 s, -90,8 dBFS; a fala termina em 4,288 e o arquivo em 4,480)
            {'id': '10', 'texto': 'ela mandou o vídeo pra Lúcia.', 'arquivo': 'narracao-v4-novas-a.mp3',
             'de': 2.869, 'ate': 4.463, 'alvo': 53.80, 'ajuste_db': 0.0,
             'obs': ('v4: troca de "turma" por "Lúcia" (pedido 9 do PLANO-v4); a fala dura 1,370 s, 0,114 s mais que a '
                     'da v3 (uma sílaba a mais: "Lú-ci-a")')},
            # a ANTIGA (aprovada), não a das tomadas novas
            {'id': '11', 'texto': 'o roteiro ela já tinha.', 'de': 23.020, 'ate': 24.466, 'alvo': 58.90, 'ajuste_db': 0.0},
            # ---- NOVAS (pedido 11): o fechamento. 12 começa no ponto mais silencioso da pausa (6,615) e não no meio
            # (6,551), para o trecho não encostar no fim do trecho da fala 11 (os dois são silêncio)
            {'id': '12', 'texto': 'faltava tirar do papel.', 'arquivo': 'narracao-v3-novas-b.mp3', 'de': 6.615,
             'ate': 8.180, 'alvo': 60.40, 'ajuste_db': 0.0},
            {'id': '13', 'texto': 'se você explica isso todo dia no consultório, o seu também já existe.',
             'arquivo': 'narracao-v3-novas-a.mp3', 'de': 8.262, 'ate': 12.967, 'alvo': 62.10, 'ajuste_db': 0.0,
             'obs': 'a pausa da vírgula (depois de "consultório,") é da própria leitura: 0,236 s'},
            # ---- NOVA (pedido 12): a CTA. Tomada b até o meio da última pausa (15,497): depois dela o arquivo termina
            # com um estalo de 2 ms (15,59 s) que fica de fora
            {'id': '14', 'texto': 'comente clínica e a gente te mostra como.', 'arquivo': 'narracao-v3-novas-b.mp3',
             'de': 12.961, 'ate': 15.497, 'alvo': 67.65, 'ajuste_db': 0.0},
        ],
        # Como cada fala nova foi escolhida entre as 3 tomadas (medido com fonte/audio: Praat para a altura da voz,
        # sílabas por segundo de fala sem as pausas, Whisper para a transcrição). Referência = a tomada A inteira:
        # F0 mediana 123,8 Hz, ritmo 6,73 sílabas/s, PLR máximo 18,17 dB ("cada linha..."). Nota = diferença de altura
        # em semitons + diferença de ritmo em % / 10 (10 % de ritmo pesa como 1 semitom); menor é melhor. Fica de fora
        # a tomada com PLR acima de 18,0 dB (o pico dela derrubaria o ganho final de tudo).
        #
        # v4 (falas F e 10, tomadas narracao-v4-novas-a/b/c): as mesmas três medidas, num método só para todas as
        # tomadas, medidas de novo no mesmo script (Praat padrão via parselmouth: to_pitch(), 75-600 Hz, mediana das
        # janelas com voz, no som da fala entre o 1º e o último ponto acima de -50 dBFS; o ritmo e o PLR saem iguais aos
        # da v3, conferidos na F antiga: 5,21 e 15,54). A altura sai 1-2 Hz diferente da v3 (outro ajuste do Praat): por
        # isso a referência de altura foi medida de novo com o mesmo método (tomada A inteira: 125,2 Hz, e não 123,8).
        # Duas notas (menor é melhor; semitons + diferença de ritmo em % / 10, como na v3):
        #   nota_v3 = ritmo comparado com a média da tomada A (6,73), a conta da v3;
        #   nota_v4 = ritmo comparado com a fala APROVADA que a nova substitui, no mesmo lugar (F antiga 5,21; fala 10
        #             antiga 8,76). É a que decide: a fala 10 antiga já era lida rápido (8,76 sílabas/s), então "mais
        #             devagar" não é "mais parecido com a narração" ali.
        # Altura = semitons acima/abaixo da tomada A (125,2 Hz). PLR de todas abaixo de 18,0 dB (o ganho final não muda).
        'escolha_das_tomadas': {
            'F': {'a': {'f0_hz': 136.5, 'semitons': 1.50, 'ritmo': 4.42, 'plr_db': 13.86, 'dur_s': 2.488,
                        'nota_v3': 4.93, 'nota_v4': 3.01},
                  'b': {'f0_hz': 126.5, 'semitons': 0.18, 'ritmo': 4.37, 'plr_db': 13.99, 'dur_s': 2.520,
                        'nota_v3': 3.70, 'nota_v4': 1.80},
                  'c': {'f0_hz': 128.3, 'semitons': 0.42, 'ritmo': 4.52, 'plr_db': 12.80, 'dur_s': 2.432,
                        'nota_v3': 3.70, 'nota_v4': 1.74},
                  'fala_antiga_v3': {'tomada': 'narracao-v3-novas-c', 'f0_hz': 126.9, 'semitons': 0.23,
                                     'ritmo': 5.21, 'plr_db': 15.54, 'dur_s': 2.496},
                  'escolhida': 'c',
                  'por_que': ('b e c empatam nas medidas (nota_v3 3,697 contra 3,702; nota_v4 1,80 contra 1,74: a b tem '
                              'a altura um quarto de semitom mais perto da tomada A, a c o ritmo mais perto da F antiga); '
                              'a c desempata porque é a única com silêncio de verdade antes de "dezessete" (0,036 s, '
                              '-85 a -91 dBFS), então o corte do começo cai numa pausa, como manda a regra (a b já começa '
                              'soando na 1ª amostra do arquivo, e a a em 0,010 s), e tem o menor pico em relação ao '
                              'volume (PLR 12,8 dB); a a fica 1,5 semitom acima. "dezessete" tem 4 sílabas: as 3 tomadas '
                              'leem a frase mais devagar que a F antiga (~4,4 contra 5,2 sílabas/s), mas a duração quase '
                              'não muda (2,43 contra 2,50 s)')},
            '10': {'a': {'f0_hz': 134.0, 'semitons': 1.18, 'ritmo': 8.76, 'plr_db': 14.81, 'dur_s': 1.370,
                         'nota_v3': 4.20, 'nota_v4': 1.18},
                   'b': {'f0_hz': 139.9, 'semitons': 1.92, 'ritmo': 8.67, 'plr_db': 15.64, 'dur_s': 1.384,
                         'nota_v3': 4.80, 'nota_v4': 2.02},
                   'c': {'f0_hz': 138.0, 'semitons': 1.68, 'ritmo': 8.36, 'plr_db': 13.37, 'dur_s': 1.436,
                         'nota_v3': 4.10, 'nota_v4': 2.14},
                   'fala_antiga_v3': {'tomada': 'narracao-amedeiros-v4-a (tomada A)', 'f0_hz': 147.3,
                                      'semitons': 2.81, 'ritmo': 8.76, 'plr_db': 13.58, 'dur_s': 1.256},
                   'escolhida': 'a',
                   'por_que': ('a altura mais perto da tomada A das 3 (1,18 semitom acima, contra 1,68 da c e 1,92 da b; '
                               'a fala antiga ficava 2,8 acima) e o ritmo igual ao da fala 10 aprovada (8,76 contra 8,76 '
                               'sílabas/s), com a duração mais perto dela (1,370 contra 1,256 s; c 1,436); melhor '
                               'nota_v4 com folga (1,18 contra 2,02 e 2,14). Pela conta da v3 a c ficaria 0,1 à frente só '
                               'por ser mais lenta, o que ali afasta da fala aprovada')},
            '_transcricao_v4': ('as 3 tomadas v4 saíram completas no Whisper (fonte/audio/narracao-v4-novas-a/b/c.'
                                'palavras.json); sem dica ele escreve "17" para "dezessete" (2ª passada com a frase como '
                                'dica, só até a pausa depois de "nada.") e "para a" no lugar de "pra" (é o jeito dele '
                                'escrever; o texto e o voz-v4.palavras.json dizem "pra")'),
            '_v3_fala_F_antiga': {'a': {'f0_hz': 127.5, 'ritmo': 4.90, 'plr_db': 15.28, 'nota': 3.23},
                                  'b': {'f0_hz': 120.8, 'ritmo': 5.30, 'plr_db': 15.08, 'nota': 2.55},
                                  'c': {'f0_hz': 124.5, 'ritmo': 5.21, 'plr_db': 15.54, 'nota': 2.36},
                                  'escolhida': 'c', 'obs': 'a escolha da v3 (tomadas narracao-v3-novas), só para registro'},
            'T': {'a': {'f0_hz': 142.8, 'ritmo': 6.01, 'plr_db': 12.63, 'nota': 3.54},
                  'b': {'f0_hz': 162.1, 'ritmo': 5.66, 'plr_db': 14.42, 'nota': 6.26},
                  'c': {'f0_hz': 137.9, 'ritmo': 5.79, 'plr_db': 15.17, 'nota': 3.27},
                  'escolhida': 'c', 'por_que': 'a menos aguda das 3 (a b sobe para 162 Hz, 4,7 semitons acima da tomada '
                                               'A); mesma tomada da fala F, que vem logo antes'},
            '12': {'a': {'f0_hz': 138.7, 'ritmo': 6.91, 'plr_db': 13.50, 'nota': 2.24},
                   'b': {'f0_hz': 122.6, 'ritmo': 7.05, 'plr_db': 13.85, 'nota': 0.64},
                   'c': {'f0_hz': 149.7, 'ritmo': 7.23, 'plr_db': 15.29, 'nota': 4.03},
                   'escolhida': 'b', 'por_que': 'altura quase igual à da tomada A (122,6 Hz); a e c ficam 2 a 3,3 '
                                                'semitons acima'},
            '13': {'a': {'f0_hz': 128.0, 'ritmo': 6.63, 'plr_db': 13.99, 'nota': 0.73},
                   'b': {'f0_hz': 132.0, 'ritmo': 6.70, 'plr_db': 13.21, 'nota': 1.15},
                   'c': {'f0_hz': 128.6, 'ritmo': 6.80, 'plr_db': 13.35, 'nota': 0.76},
                   'escolhida': 'a', 'por_que': 'a melhor nota (a e c quase empatam; as duas leem a vírgula com uma '
                                                'pausa natural de 0,22-0,24 s)'},
            '14': {'a': {'f0_hz': 126.6, 'ritmo': 6.90, 'plr_db': 15.92, 'nota': 0.64},
                   'b': {'f0_hz': 125.2, 'ritmo': 6.81, 'plr_db': 14.79, 'nota': 0.31},
                   'c': {'f0_hz': 126.8, 'ritmo': 6.63, 'plr_db': 18.65, 'nota': None},
                   'escolhida': 'b', 'por_que': 'a melhor nota; a c fica de fora: pico de -3,6 dBFS em "comente" (PLR '
                                                '18,65 dB, maior que o de "cada linha...") baixaria o ganho final 0,5 dB'},
            '_transcricao': ('as 3 tomadas saíram completas no Whisper (sem dica ele escreve "47" para "quarenta e '
                             'sete"); fonte/audio/narracao-v3-novas-a/b/c.palavras.json'),
        },
        # Fronteiras entre palavras MEDIDAS no som (altura da voz, energia e chiado em janelas de 10 ms), em segundos
        # da tomada, para as duas falas que comandam a imagem (o lettering de s04b e a pílula "CLÍNICA" de s12). Nelas o
        # Whisper marca 0,1-0,2 s antes do som (ex.: "isso" em 2,98 s, mas o "i" só começa em 3,175, depois do "s" de
        # "mas", que sai colado). None = o começo real da fala. Cada palavra termina onde a seguinte começa (ou onde
        # começa um silêncio entre elas).
        'fronteiras_medidas': {
            'T': [['mas', None],           # m + a 2,898-3,06; o "s" (chiado) 3,06-3,17
                  ['isso', 3.175],         # o "i" começa (a voz sobe de 103 Hz)
                  ['está', 3.500],         # o "s" de "está" (chiado) depois do "o" de "isso"; "tá" até 3,73
                  ['prestes', 3.912],      # o "p" depois da pausa (3,73-3,91)
                  ['a', 4.325],            # depois do "s" final de "prestes" (4,29-4,32)
                  ['mudar...', 4.405]],    # "mu" (a voz volta a subir); "dar" em 4,57; fim 4,804
            '14': [['comente', None],      # "co-men-te" até o fechamento do "c" de "clínica"
                   ['clínica', 13.560],    # o "c" fecha (13,56-13,60) e solta (13,61)
                   ['e', 14.100],          # a queda depois de "ca" (14,08-14,11)
                   ['a', 14.190],          # "e a" saem numa vogal só (14,12-14,27): metade para cada
                   ['gente', 14.275],      # o "g" ("j", chiado) 14,28
                   ['te', 14.505],         # fechamento do "t" (14,52-14,54)
                   ['mostra', 14.625],     # "m" 14,63
                   ['como.', 15.025]],     # fechamento do "c" (15,03-15,10)
        },
    },
    'trilha': {
        'arquivo': 'trilha-tema-b.mp3',
        'golpe_no_arquivo': 36.677,             # ataque do golpe (medido com 1 ms; ver fonte/audio/golpes.json)
        'entrada': [3.55, 4.55],                # a música começa a soar com o recuo (3,55 s) e chega ao volume em 4,55
        # volume (fator) ao longo do episódio; entre os pontos o volume muda em linha reta (em dB).
        #  - antes do golpe, um fator por frase do piano (uma nota a cada ~3,33 s). Com o golpe 3,3 s mais tarde, a
        #    música andou junto: cada frase da v2 cai agora 3,3 s depois, sobre o MESMO trecho da música. Então os
        #    fatores da v2 seguem as suas frases (os mesmos números, 3,3 s depois), e entra uma frase nova no começo
        #    (3,926-7,256 s, a frase da música que antes ficava antes da entrada). O fator dela (0,055) deixa essa
        #    frase com o volume que a 1ª frase tinha na v2 (-33,2 LUFS, também com a entrada de 1 s), um pouco mais
        #    baixa que a seguinte (ver "trilha_por_frase" no relatório). A mudança de fator é
        #    feita em 0,3 s e termina 20 ms antes de cada nota. As falas 6, 7 e 8 andaram os mesmos 3,3 s, então ficam
        #    sobre a mesma música e o mesmo volume da v2;
        #  - de 25,9 a 33,9 s: EXATAMENTE o envelope do corte de 10 s (0,14 até 29,4; sobe até 0,45 em 33,9);
        #  - de 33,9 a 46,7 s: o auge (0,45), sustentado durante o vídeo dela (os pontos da v2, +3,3 s);
        #  - de 46,5 s em diante: "relaxa" (o leito, ver abaixo).
        'volume': [[3.55, 0.055], [6.936, 0.055], [7.236, 0.05],
                   [10.271, 0.05], [10.571, 0.064], [13.231, 0.064], [13.531, 0.16],
                   [16.941, 0.16], [17.241, 0.075], [20.266, 0.075], [20.566, 0.099], [23.616, 0.099],
                   [23.916, 0.047], [25.9, 0.14],
                   [29.4, 0.14], [33.9, 0.45],
                   # no auge, só um acento da música (40,62 s, no passo 2 do vídeo dela) passaria muito do teto:
                   # ele desce 3 dB por 0,3 s (rampas de 0,1 s), como na v2 (37,2-37,7 + 3,3 s)
                   [40.5, 0.45], [40.6, 0.3186], [40.9, 0.3186], [41.0, 0.45],
                   # o fim do vídeo dela desce devagar (-3,5 dB de 45,7 a 46,5), como na v2 (42,4-43,2 + 3,3 s)
                   [45.7, 0.45], [46.5, 0.30]],
        # o relaxamento: de 46,5 a 47,3 s o volume desce até o leito, rápido no começo (curva power2.out, em dB), para
        # a voz entrar (47,0 s) já com a música quase no leito (a v2 em 43,2-44,0, +3,3 s). O leito é calculado como
        # na v2: a trilha fica em -30,5 LUFS sob as falas que estão sobre a música cheia depois do relaxamento (9, 10,
        # 11 e 12). A 13 e a 14 ficam sobre a 2ª cópia da trilha (emenda_fim, abaixo), com o volume dela ajustado para
        # o mesmo leito. O leito é calculado só com a 1ª cópia e sem a curva do fim, para nada antes da emenda mudar.
        # v4: o leito NÃO é recalculado. Fica o valor exato que a v3 calculou (repr do float do montar-v3.py, conferido
        # rodando uma cópia dele: refez o mix-v3.wav idêntico byte a byte). Recalcular com a fala 10 nova mudaria a
        # música de 46,5 s até o fim (a regra do dono: o resto fica idêntico). O script ainda mede e mostra onde a trilha
        # fica sob as falas 9, 10, 11 e 12 com a fala 10 nova (relatório "leito_medido_v4").
        'relaxa': {'de': 46.5, 'ate': 47.3, 'leito_lufs_sob_a_voz': -30.5, 'falas_de_referencia': ['9', '10', '11', '12'],
                   'leito_db_fixo': -28.82113902675183},
        # suspense (pedido 6, cena nova s04b): a trilha desce 5,5 dB no corte para s04b (18,30-18,56), fica baixa
        # durante "mas" (18,60-18,87) e volta devagar sob "isso está prestes a mudar…" (18,87-20,15), chegando ao
        # volume normal em "mudar" (20,11-20,50), junto com o pico do sopro grave (20,27). Curvas de cosseno, em dB.
        'suspense': {'db': -5.5, 'desce': [18.30, 18.56], 'volta': [18.87, 20.15]},
        # realce (v2: +3 dB no silêncio longo da voz em s11, até o fim): na v3 ele SAIU. Dentro de s11 não há mais
        # silêncio longo (as falas 11, 12 e 13 quase emendam: pausas de 0,43 e 0,56 s, curtas demais para uma subida
        # lenta), e no único silêncio que sobrou (66,38-67,65, o cartão descendo) a música já está acabando sozinha
        # (-50 a -57 LUFS): +3 dB ali não se ouviriam. Para ligar de novo: 'db': 3.0 com 'sobe': [de, até].
        # Depois da emenda do fim, a subida entre as falas e no fim é feita pela curva 'volume_db' da emenda_fim.
        'realce': {'db': 0.0, 'sobe': [66.45, 67.05], 'desce': None},
        # A ÚNICA EMENDA DA TRILHA (ver as regras no topo): o fim, para a CTA e o cartão não ficarem sem música.
        # Medido na música crua: 72,03 BPM (semicolcheia 0,20826 s, compasso 3,3321 s; grade ajustada em 130 ataques
        # de 36,7 a 63,4 s, erro mediano 7 ms). Depois do golpe o ciclo é lá menor -> fá -> dó -> sol, um acorde por
        # compasso (cromagrama de cada compasso); o compasso 8 (63,357 s da música = 60,613 do episódio) é a resolução
        # (sol -> lá menor): o pulso para ~0,4 s depois, o acorde soa e some, com 2 notas de piano no tempo 4 e no
        # compasso seguinte.
        # A emenda: no compasso 8, logo depois da resolução, a trilha cruza para uma 2ª cópia da MESMA trilha atrasada
        # 2 compassos. A 2ª cópia toca dó (o resto do compasso 8) -> sol (63,95-67,27) -> e resolve em lá menor em
        # 67,275 s, entre o cartão chegando (66,9-67,5) e "comente" (67,65). A cauda natural dela (o acorde que some,
        # as notas de piano em 69,78 e 70,61) é o leito da CTA e vai até o fim.
        # Por que 2 compassos e por que ali: semelhança das notas (cromagrama, 0 a 1) entre a 1ª cópia (lá menor da
        # resolução) e a 2ª, semicolcheia a semicolcheia no compasso 8 (60,61 / 60,81 / 61,02 / 61,23 / 61,43 s):
        #   2 compassos atrás (dó): 0,88 / 0,91 / 0,91 / 0,88 / 0,86  <- lá menor e dó têm 2 notas em comum (dó e mi)
        #   3 compassos atrás (fá): 0,83 / 0,73 / 0,73 / 0,70 / 0,65
        #   1 compasso atrás (sol): 0,60 / 0,47 / 0,45 / 0,49 / 0,49
        # (3 compassos levariam a resolução para 70,6 s, depois da CTA; 1 compasso, para 63,95, sob a fala 13, e a CTA
        # ficaria de novo sobre o fim que some.) O cruzamento vai da 3ª semicolcheia do tempo 1 até o tempo 2
        # (61,029-61,446 s, 0,42 s), onde as notas mais combinam e as duas cópias têm o mesmo volume (diferença
        # de 1,2 dB); fica sob o fim de "papel" (a fala 12 termina em 61,544), que esconde a passagem. As duas formas
        # de onda quase não se parecem ali (correlação 0,04), por isso o cruzamento é de potência igual (seno/cosseno).
        # O atraso exato (6,6685 s = 320.088 amostras) é o que melhor alinha os ataques da batida perto da emenda.
        # volume_db: dB somados ao leito depois da emenda (curvas de cosseno entre os pontos; antes do 1º ponto, 0):
        #   +2 sob a fala 13 (a parte de dó/sol da trilha é um pouco mais baixa que a de antes: -32,7 LUFS no leito);
        #   +3 no vão entre as falas 13 e 14, com o cartão e a resolução (realce suave);
        #   sob a fala 14 sobe devagar de +3 a +6, acompanhando a cauda que vai sumindo (fica no mesmo leito);
        #   depois da CTA, +8 (realce suave do fim, para a 2ª nota de piano em 70,61); fade de 0,5 s até zero em 71,7.
        'emenda_fim': {'atraso_s': 6.6685, 'cruzamento': [61.029, 61.446],
                       # revisão (sessão principal, por sugestão do conferente): a voz da CTA e de "consultório" ficava
                       # perto demais da música (3,3 e 4,6 dB). Agora: sob o acorde de sol (63,95-66,4) a trilha fica
                       # 0,5 dB abaixo do leito, e a subida do fim só começa DEPOIS de "como." (69,85).
                       'volume_db': [[61.446, 0.0], [62.05, 2.0], [63.6, 2.0], [63.95, -0.5], [66.40, -0.5],
                                     [66.90, 3.0], [67.45, 3.0], [69.85, 3.0], [70.35, 8.0], [71.2, 8.0]],
                       'fade': [71.2, 71.7]},
        'frases_do_piano': [[3.926, 7.256], [7.256, 10.591], [10.591, 13.551], [13.551, 17.261], [17.261, 20.586],
                            [20.586, 23.936], [23.936, 27.266], [27.266, 30.596], [30.596, 33.933]],
        # recorte de médias (1-4 kHz) na trilha enquanto a voz fala, para abrir espaço para ela (o mesmo do corte)
        'recorte_medias_db': -4.0, 'recorte_folga_s': 0.20, 'recorte_rampa_s': 0.15,
        'recorte_do_corte': [0.80, 3.50],       # a janela da fala do corte, sem mudança (em segundos do corte)
    },
    # os ambientes contínuos ("leitos"): uma gravação repetida com cruzamentos de 0,5 s quando ela não cobre a cena.
    # Cada cópia seguinte começa no ponto do arquivo que mais se parece com o fim da anterior ("busca_emenda_s").
    'leitos': [
        # noite: de 0 a 25,9 s (a v2 ia até 22,6); em 25,9 entra o ambiente do corte de 10 s (o mesmo arquivo, desde o
        # começo), e o leito sai em 40 ms por baixo dele. Mesmo ganho do ambiente do corte.
        {'nome': 'ambiente de consultório à noite (leito de 0 a 25,9 s)', 'arquivo': 'ambiente-noite-b.mp3',
         'de_arquivo': 0.0, 'fim_util': None, 'ini_ep': 0.0, 'fim_ep': BASE_CORTE, 'entrada_s': 0.010,
         'saida_s': 0.040, 'cruzamento_s': 0.5, 'busca_emenda_s': [0.0, 1.5], 'ganho': 'do_corte',
         'origem': 'v2 (o mesmo leito, agora até 25,9 s)'},
        # recepção ao fim de tarde: s09 e s10 se passam na recepção (s10 usa a foto recepcao-tarde-desfocada.jpg), e na
        # v2 o ambiente ia de s09 até o corte para s11. Na v3 isso é 46,7-58,5 s (11,8 s): o arquivo (9 s; usamos
        # até 8,5, como na v2) é repetido 1 vez. Entra em 0,6 s, sai seco no corte para s11. Mesmo ganho da v2.
        {'nome': 'ambiente de recepção ao fim de tarde', 'arquivo': 'ambiente-recepcao-tarde-b.mp3',
         'de_arquivo': 0.0, 'fim_util': 8.5, 'ini_ep': 46.7, 'fim_ep': 58.5, 'entrada_s': 0.60, 'saida_s': 0.02,
         'cruzamento_s': 0.5, 'busca_emenda_s': [1.0, 3.0], 'filtro': {'passa_altas_hz': 100},
         'ganho': {'rms_alvo_db': -55.0, 'trecho_base': [0.0, 8.5]},
         'origem': 'v2 (+3,3 s; agora até 58,5 s, o corte para s11)',
         'obs': 'o filtro tira o ronco grave de trânsito (abaixo de 100 Hz)'},
        # consultório à tarde: s11 (58,5-67,4 s, 8,9 s). O arquivo tem 8 s e sobe devagar no começo (até 0,45) e desce
        # no fim (de 7,3): cada cópia usa de 0,45 a 7,2 s. Entra seco no corte, sai em 0,4 s com o cartão. Ganho da v2.
        {'nome': 'ambiente de consultório à tarde', 'arquivo': 'ambiente-consultorio-tarde-b.mp3',
         'de_arquivo': 0.45, 'fim_util': 7.20, 'ini_ep': 58.5, 'fim_ep': 67.4, 'entrada_s': 0.02, 'saida_s': 0.40,
         'cruzamento_s': 0.5, 'busca_emenda_s': [1.0, 3.0], 'filtro': {'passa_altas_hz': 80},
         'ganho': {'rms_alvo_db': -55.0, 'trecho_base': [0.45, 7.95]},
         'origem': 'v2 (+6,6 s; agora 8,9 s, com 1 emenda)'},
    ],
    'efeitos': [
        # ---------------- s01 a s04: iguais à v2, nos mesmos tempos ----------------
        {'nome': 'toque seco no vidro ("apagar")', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 1.930, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0, 'origem': 'v2'},
        {'nome': 'tique seco do contador (take 14 -> take 15)', 'arquivo': 'tique-contador-a.mp3', 'de': 0.085,
         'ate': 0.135, 'ancora': 'transiente', 'busca': [0.095, 0.110], 'no_ep': 2.650, 'entrada_s': 0.003,
         'saida_s': 0.010, 'pico_alvo_db': -37.0, 'origem': 'v2'},
        {'nome': 'sopro grave do recuo que revela a maquete', 'arquivo': 'sopro-grave-d.mp3', 'de': 0.0, 'ate': 2.56,
         'ancora': 'pico', 'no_ep': 4.700, 'entrada_s': 0.05, 'saida_s': 0.50, 'pico_alvo_db': -38.0, 'origem': 'v2',
         'obs': 'o pico do sopro cai em 4,7 s, o meio do recuo (3,55-5,85 s, mais rápido no meio)'},
        {'nome': 'papel farfalhando de leve (a folha chega)', 'arquivo': 'papel-farfalhando-a.mp3', 'de': 0.0,
         'ate': 0.85, 'ancora': 'inicio', 'no_ep': 9.300, 'entrada_s': 0.01, 'saida_s': 0.20, 'pico_alvo_db': -42.0,
         'origem': 'v2'},
        {'nome': 'risco de caneta em "gravar 06/11"', 'arquivo': 'risco-caneta-c.mp3', 'de': 0.0, 'ate': 0.36,
         'ancora': 'trecho', 'no_ep': 13.700, 'entrada_s': 0.005, 'saida_s': 0.08, 'pico_alvo_db': -43.0,
         'origem': 'v2', 'obs': 'o risco (13,70-14,05 s) cai no "não" de "a gravação, não." (13,87 s)'},
        {'nome': 'toque seco no vidro (abre o perfil)', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 15.370, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0, 'origem': 'v2'},
        {'nome': 'atrito suave da rolagem da tela', 'arquivo': 'rolagem-tela-a.mp3', 'de': 0.30, 'ate': 1.0,
         'ancora': 'trecho', 'no_ep': 15.430, 'entrada_s': 0.03, 'saida_s': 0.25, 'pico_alvo_db': -40.0,
         'origem': 'v2'},
        # ---------------- s04b (NOVA): a virada antes da 15ª ----------------
        {'nome': 'sopro grave suave ("prestes a mudar")', 'arquivo': 'sopro-grave-c.mp3', 'de': 0.0, 'ate': 2.56,
         'ancora': 'pico', 'no_ep': 20.270, 'entrada_s': 0.05, 'saida_s': 0.50, 'pico_alvo_db': -39.0,
         'origem': 'novo (v3)',
         'obs': ('tomada c (ar grave que cresce e some; a e b saíram como estrondo grave, quase uma nota, e a d já é '
                 'o sopro do recuo em 4,7 s). Cresce sob "isso está prestes a" e o pico cai na sílaba forte de '
                 '"mudar" (20,27 s; a palavra vai de 20,11 a 20,51)')},
        {'nome': 'toque bem discreto no vidro (a tela do celular apaga)', 'arquivo': 'toque-vidro-c.mp3',
         'de': 0.088, 'ate': 0.220, 'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 21.150,
         'entrada_s': 0.003, 'saida_s': 0.040, 'pico_alvo_db': -41.0, 'origem': 'novo (v3)',
         'obs': 'o mesmo toque de sempre, 7 dB mais baixo que os outros; s04b 2,85 s (21,15) = a tela começa a apagar'},
        # ---------------- s05: os mesmos sons da v2, +3,3 s ----------------
        {'nome': 'obturador do celular (fecha e reabre)', 'arquivo': 'obturador-a.mp3', 'de': 0.0, 'ate': 0.30,
         'ancora': 'trecho', 'no_ep': 23.200, 'entrada_s': 0.002, 'saida_s': 0.10, 'pico_alvo_db': -37.0,
         'origem': 'v2 (+3,3 s)', 'obs': 'dois estalos (fecha em 23,23 e reabre em 23,31)'},
        {'nome': 'toque seco no vidro ("enviado")', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 23.650, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0, 'origem': 'v2 (+3,3 s)'},
        # ---------------- a virada: do corte de 10 s, sem nenhuma mudança (tempos do corte; caem em +25,9 s) -------
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
        # ---------------- s08: o vídeo dela, os mesmos sons da v2, +3,3 s ----------------
        # Tempos casados com compositions/s08-video-dela.html (s08 começa em 34,733 = quadro 1042): varredura do vidro
        # 37,633-38,633 · plano de corte desce em P3 (40,867) · o osso cresce de 41,467 a 42,667 · faixa de luz de
        # 44,167 a 45,167.
        {'nome': 'atrito seco de vidro fosco (a varredura)', 'arquivo': 'atrito-vidro-fosco-e.mp3', 'de': 0.0,
         'ate': 1.15, 'ancora': 'trecho', 'no_ep': 37.600, 'entrada_s': 0.02, 'saida_s': 0.15,
         'abaixo_trilha_db': 10.0, 'origem': 'v2 (+3,3 s)'},
        {'nome': 'chiado fino de corte', 'arquivo': 'chiado-corte-a.mp3', 'de': 0.0, 'ate': 0.40,
         'ancora': 'inicio', 'no_ep': 40.867, 'entrada_s': 0.005, 'saida_s': 0.10, 'abaixo_trilha_db': 12.0,
         'origem': 'v2 (+3,3 s)'},
        {'nome': 'textura granular do crescimento', 'arquivo': 'textura-granular-b.mp3', 'de': 0.0, 'ate': 1.30,
         'ancora': 'trecho', 'no_ep': 41.467, 'entrada_s': 0.03, 'saida_s': 0.25, 'abaixo_trilha_db': 12.0,
         'origem': 'v2 (+3,3 s)'},
        {'nome': 'faixa de luz, brilho suave e seco', 'arquivo': 'brilho-luz-a.mp3', 'de': 0.0, 'ate': 1.20,
         'ancora': 'inicio', 'no_ep': 44.167, 'entrada_s': 0.02, 'saida_s': 0.15, 'abaixo_trilha_db': 12.0,
         'filtro': {'notch_hz': [1605]}, 'origem': 'v2 (+3,3 s)'},
        # ---------------- s09: o vídeo vira o 1º post; 3 semanas depois, mais posts e os números ----------------
        {'nome': 'sopro suave de levar junto', 'arquivo': 'sopro-levar-d.mp3', 'de': 0.10, 'ate': 1.36,
         'ancora': 'pico', 'no_ep': 47.300, 'entrada_s': 0.02, 'saida_s': 0.30, 'pico_alvo_db': -38.0,
         'origem': 'v2 (+3,3 s)'},
        # 5 tiques bem discretos, um em cada post novo (s09 3,60 / 3,82 / 4,04 / 4,26 / 4,48), alternando a tomada a
        # (o 2º estalo, o mesmo de s01) e a b (a b é uma catraca de 6 estalos: só o 2º, 0,090-0,150 s, de queda curta
        # como o da a)
        *[{'nome': f'tique discreto do post novo {k + 1}',
           'arquivo': 'tique-contador-a.mp3' if k % 2 == 0 else 'tique-contador-b.mp3',
           'de': 0.085 if k % 2 == 0 else 0.090, 'ate': 0.135 if k % 2 == 0 else 0.150, 'ancora': 'transiente',
           'busca': [0.095, 0.110] if k % 2 == 0 else [0.098, 0.112], 'no_ep': t_ep, 'entrada_s': 0.003,
           'saida_s': 0.010, 'pico_alvo_db': -44.0, 'origem': 'novo (v3)'}
          for k, t_ep in enumerate([50.30, 50.52, 50.74, 50.96, 51.18])],
        # um toque suave em cada etiqueta de número (s09 4,80 "+438 seguidores" e 5,10 "21,3 mil visualizações")
        *[{'nome': f'toque suave na etiqueta "{nome_et}"', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088,
           'ate': 0.220, 'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': t_ep, 'entrada_s': 0.003,
           'saida_s': 0.040, 'pico_alvo_db': -40.0, 'origem': 'novo (v3)'}
          for nome_et, t_ep in [('+438 seguidores', 51.50), ('21,3 mil visualizações', 51.80)]],
        # ---------------- s10: ela encaminha para a turma (os mesmos sons da v2, +6,6 s) ----------------
        {'nome': 'toque seco no vidro (abre a conversa)', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 53.900, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0, 'origem': 'v2 (+6,6 s)'},
        {'nome': 'toque seco no vidro ("encaminhado")', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 54.150, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -35.0, 'origem': 'v2 (+6,6 s)'},
        {'nome': 'chegada de mensagem (toque seco duplo)', 'arquivo': 'chegada-mensagem-b.mp3', 'de': 0.0,
         'ate': 0.40, 'ancora': 'transiente', 'busca': [0.015, 0.04], 'no_ep': 55.500, 'entrada_s': 0.003,
         'saida_s': 0.08, 'pico_alvo_db': -36.0, 'origem': 'v2 (+6,6 s)'},
        # ---------------- s11: ela fica parada no consultório: sem passos e sem porta (só o leito, acima) ----------
        # ---------------- s12: o cartão com a CTA ----------------
        {'nome': 'toque suave (a pílula "CLÍNICA" salta)', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088,
         'ate': 0.220, 'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 68.000, 'entrada_s': 0.003,
         'saida_s': 0.040, 'pico_alvo_db': -38.0, 'origem': 'novo (v3)',
         'obs': ('s12 1,10 s (68,00): a pílula salta junto com a palavra "clínica" (começa em ~68,00-68,03 no som); '
                 'um pouco mais baixo que os toques de tela (-34)')},
    ],
    'final': {
        'teto_dbtp': -1.2,                    # teto do pico real (um pouco abaixo de -1 por segurança)
        'janela_limitador_ep': [BASE_CORTE + 8.013, 46.70],  # do impacto ao fim do vídeo dela: sem voz
        'limitador_max_db': 6.0,              # se precisar de mais que isso, o script para (baixe a trilha no auge)
        'fade_fim_s': 0.25,
    },
}

_cache = {}


def ler(nome, canais=2):
    if (nome, canais) not in _cache:
        raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', os.path.join(FONTES, nome), '-ac', str(canais),
                              '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
        _cache[(nome, canais)] = np.frombuffer(raw, np.float32).reshape(-1, canais).astype(np.float64)
    return _cache[(nome, canais)].copy()


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
    """amostra do episódio onde cai um ponto: itens do corte usam a mesma conta do corte + 1.243.200 amostras"""
    if e.get('do_corte') or 'no_corte' in e:
        return I0 + int(round(t_relativo * SR))
    return int(round(t_relativo * SR))


def cosseno(t, a, b):
    """0 antes de a, 1 depois de b, meia-onda de cosseno no meio"""
    return 0.5 - 0.5 * np.cos(np.pi * np.clip((t - a) / (b - a), 0, 1))


medidor = pyln.Meter(SR)


def lufs(x):
    if len(x) < int(0.4 * SR):
        return float('nan')
    v = medidor.integrated_loudness(x if x.ndim == 2 else np.c_[x, x])
    return float(v)


def lufs_sem_portao(x):
    """o mesmo LUFS, mas sem o "portão" (que ignora os trechos 10 LU mais baixos que a média): é a energia média do
    trecho inteiro. Serve onde o trecho tem uma descida de propósito (o portão faria a descida parecer mais alta)"""
    y = (x if x.ndim == 2 else np.c_[x, x]).copy()
    for filtro_k in medidor._filters.values():
        for ch in range(y.shape[1]):
            y[:, ch] = filtro_k.apply_filter(y[:, ch])
    return float(-0.691 + 10 * np.log10((y ** 2).mean(0).sum() + 1e-20))


doc = {'_sobre': ('Áudio do EPISÓDIO COMPLETO v4 do ep. 01 (sala de espera), 2º pedido do dono de 12/11/2026: 0 a 71,7 '
                  's. É o mix-v3.wav com SÓ duas falas trocadas (F "dezessete dias sem postar nada." e 10 "ela mandou '
                  'o vídeo pra Lúcia.", pedidos 4 e 9 do fonte/PLANO-v4.md); fora delas é idêntico ao mix-v3.wav (ver '
                  'final.teste_de_subtracao_contra_o_mix_v3). Tempos em segundos do EPISÓDIO (a virada começa em 25,9 '
                  's; o golpe é o quadro 1018 = 33,933 s). De 25,9 a 36,733 s os sons são os do corte de 10 s aprovado. '
                  'Gerado por fonte/audio/montar-v4.py; para mudar, edite o PLANO no script e rode de novo. A v3 '
                  '(mix-v3.wav, audio-v3.json) não muda.'),
       'duracao_s': DUR, 'amostragem_hz': SR, 'canais': 2, 'virada_comeca_em_s': BASE_CORTE,
       'golpe_no_episodio_s': GOLPE_EP, 'falas': [], 'eventos': []}

# ---------------- voz: cada fala recortada nas pausas da sua tomada, com um ganho fixo por fala ----------------
pv = PLANO['voz']
for f in pv['falas']:
    f['arquivo'] = f.get('arquivo', TOMADA_A)
    tomada = ler(f['arquivo'], 1)[:, 0]
    ev_tomada, _ = env_db(tomada, 2)
    k0, k1 = int(np.ceil(f['de'] / 0.002 - 1e-6)), int(f['ate'] / 0.002 + 1e-6)
    ativo = np.nonzero(ev_tomada[k0:k1] > pv['limiar_fala_dbfs'])[0]
    f['_fala_arq'] = ((k0 + ativo[0]) * 0.002, (k0 + ativo[-1] + 1) * 0.002)
    fa = tomada[int(round(f['_fala_arq'][0] * SR)):int(round(f['_fala_arq'][1] * SR))]
    f['_lufs_cru'] = lufs(fa)
    f['_pico_cru'] = pico_real_db(fa)
ref = next(f for f in pv['falas'] if f['id'] == pv['referencia'])
for f in pv['falas']:
    f['ganho_db'] = round(pv['ganho_da_referencia_db'] + (ref['_lufs_cru'] - f['_lufs_cru']) + f['ajuste_db'], 2)

voz_mono = np.zeros(N)
fim_anterior_ep = -1.0
fim_clip_anterior = -1
for f in pv['falas']:
    tomada = ler(f['arquivo'], 1)[:, 0]
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
    # deslocamento exato do recorte: tempo no episódio = tempo na tomada + desloc
    f['_real'] = dict(comeca=comeca, termina=termina, clip=[i_clip / SR, (i_clip + len(trecho)) / SR],
                      fala_arq=[fala_ini_arq, fala_fim_arq], desloc=i_clip / SR - a_t / SR)
    fim_anterior_ep, fim_clip_anterior = termina, i_clip + len(trecho)
voz = np.c_[voz_mono, voz_mono]
t = np.arange(N) / SR

# ---------------- trilha ----------------
pt = PLANO['trilha']
musica_inteira = ler(pt['arquivo'], 2)
a_mus = int(round((pt['golpe_no_arquivo'] - GOLPE_CORTE) * SR)) - I0   # a mesma conta do corte, menos 25,9 s
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

# ---------------- a ÚNICA emenda da trilha: o fim (ver as regras no topo e PLANO['trilha']['emenda_fim']) --------
# 2ª cópia da mesma trilha, atrasada 2 compassos; ela recebe o mesmo recorte de médias sob a voz, feito separado (o
# filtro sem atraso de fase "olha para a frente", então filtrar as duas juntas mudaria a 1ª cópia antes da emenda)
pe = pt['emenda_fim']
atraso_amostras = int(round(pe['atraso_s'] * SR))
a_mus2 = a_mus - atraso_amostras                 # amostra da música que cai no começo do episódio, na 2ª cópia
mus_cru2 = np.zeros((N, 2))
i_ok = max(0, -a_mus2)                            # antes disso a 2ª cópia ainda não existe (e nem é usada)
pedaco2 = musica_inteira[a_mus2 + i_ok:a_mus2 + N]
mus_cru2[i_ok:i_ok + len(pedaco2)] = pedaco2
banda2 = sosfiltfilt(butter(2, [1000, 4000], 'bandpass', fs=SR, output='sos'), mus_cru2, axis=0)
mus_rec2 = mus_cru2 + banda2 * ((10 ** (pt['recorte_medias_db'] / 20) - 1) * env_rec)[:, None]
cr0, cr1 = pe['cruzamento']
u_cr = np.clip((t - cr0) / (cr1 - cr0), 0, 1)
peso1 = np.where(t < cr0, 1.0, np.cos(np.pi / 2 * u_cr))    # potência igual: cos² + sen² = 1
peso2 = np.where(t < cr0, 0.0, np.sin(np.pi / 2 * u_cr))
mus_rec_emendada = mus_rec * peso1[:, None] + mus_rec2 * peso2[:, None]   # antes de cr0: igual a mus_rec, bit a bit
# curva do fim (dB somados ao leito; 0 antes do 1º ponto) e o fade de 0,5 s até zero em 71,7
fim_db = np.zeros(N)
for (ta_, da_), (tb_, db_) in zip(pe['volume_db'], pe['volume_db'][1:]):
    sel_ = (t >= ta_) & (t < tb_)
    fim_db[sel_] = da_ + (db_ - da_) * cosseno(t[sel_], ta_, tb_)
fim_db[t >= pe['volume_db'][-1][0]] = pe['volume_db'][-1][1]
fim_fade = 1.0 - cosseno(t, *pe['fade'])

# volume: pontos até 46,5 s (em dB, linha reta), entrada suave, suspense em s04b, relaxamento até o leito, realce
pts = np.array(pt['volume'])
vol_db = np.interp(t, pts[:, 0], 20 * np.log10(pts[:, 1]))
e0, e1 = pt['entrada']
x_ent = np.clip((t - e0) / (e1 - e0), 0, 1)
ganho_entrada = np.where(t < e1, np.sin(np.pi / 2 * x_ent), 1.0)
ganho_entrada[t < e0] = 0.0
sus = pt['suspense']
vol_db += sus['db'] * (cosseno(t, *sus['desce']) - cosseno(t, *sus['volta']))
rx = pt['relaxa']
auge_db = 20 * np.log10(pts[-1, 1])
falas_por_id = {f['id']: f for f in pv['falas']}
# o leito: fator constante para a trilha (com recorte) ficar em leito_lufs_sob_a_voz nas falas de referência
idx_ref = np.concatenate([np.arange(int(falas_por_id[k]['_real']['comeca'] * SR),
                                    int(falas_por_id[k]['_real']['termina'] * SR))
                          for k in rx['falas_de_referencia']])
# v4: o leito fica no valor exato da v3 (não é recalibrado; ver PLANO['trilha']['relaxa']['leito_db_fixo'])
leito_db = rx['leito_db_fixo']
realce = pt['realce']


def curva_volume(leito_db_, com_fim=True):
    """com_fim=False: a curva de antes da emenda (é com ela, na 1ª cópia, que o leito é calibrado)"""
    v = vol_db.copy()
    u = np.clip((t - rx['de']) / (rx['ate'] - rx['de']), 0, 1)
    p = 1 - (1 - u) ** 2                                     # power2.out
    depois = t >= rx['de']
    v[depois] = auge_db + (leito_db_ - auge_db) * p[depois]
    if realce['db']:
        sobe = cosseno(t, *realce['sobe'])
        desce = cosseno(t, *realce['desce']) if realce.get('desce') else 0.0
        v += realce['db'] * (sobe - desce)
    if not com_fim:
        return 10 ** (v / 20) * ganho_entrada
    return 10 ** ((v + fim_db) / 20) * ganho_entrada * fim_fade


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
                                   'origem': 'corte de 10 s (sem mudança)' if 'no_corte' in e else e['origem'],
                                   'trecho_do_arquivo_s': [e['de'], e['ate']], 'ancora': e['ancora'],
                                   'ancora_no_arquivo_s': round(e['de'] + anc, 3), 'no_episodio_s': round(no_ep, 3),
                                   'toca_no_episodio_s': [round(i / SR, 3), round((i + len(seg)) / SR, 3)],
                                   'ganho_db': round(ganho, 1), 'referencia_do_ganho': refg,
                                   **({'filtro': e['filtro']} if 'filtro' in e else {}),
                                   **({'obs': e['obs']} if 'obs' in e else {})})
            print(f"{e['nome']:<56} {e['arquivo']:<30} âncora {e['de'] + anc:6.3f} s -> {no_ep:6.3f} s, "
                  f"ganho {ganho:+5.1f} dB")
    return fx_, g_amb


def ganho_rms_como_v2(pl):
    """o mesmo ganho que o ambiente tinha na v2 como evento único: RMS do trecho base (com as mesmas entrada/saída),
    sem os primeiros 0,1 s e sem a saída"""
    g = pl['ganho']
    src = filtrar(ler(pl['arquivo'], 2), pl.get('filtro'))
    seg = src[int(round(g['trecho_base'][0] * SR)):int(round(g['trecho_base'][1] * SR))].copy()
    ne, ns = int(pl['entrada_s'] * SR), int(pl['saida_s'] * SR)
    seg[:ne] *= rampa(ne, 0, 1)[:, None]
    seg[len(seg) - ns:] *= rampa(ns, 1, 0)[:, None]
    medido = 20 * np.log10(np.sqrt((seg[int(0.1 * SR):-ns or None] ** 2).mean()) + 1e-12)
    return g['rms_alvo_db'] - medido, f"RMS {medido:.1f} dBFS -> {g['rms_alvo_db']:.1f} (trecho {g['trecho_base']}, como na v2)"


def leito(pl, g_amb):
    """um ambiente contínuo de ini_ep a fim_ep: o arquivo (de_arquivo até fim_util) repetido com cruzamentos"""
    amb = filtrar(ler(pl['arquivo'], 2), pl.get('filtro'))
    fim_util = int(round(pl['fim_util'] * SR)) if pl['fim_util'] else len(amb)
    amb = amb[:fim_util]
    mono = amb.mean(1)
    nc = int(pl['cruzamento_s'] * SR)
    cauda = mono[len(amb) - nc:]
    melhor, melhor_c = 0, -2.0
    for s in range(int(pl['busca_emenda_s'][0] * SR), int(pl['busca_emenda_s'][1] * SR), 24):
        cab = mono[s:s + nc]
        c = float(np.dot(cauda, cab) / (np.linalg.norm(cauda) * np.linalg.norm(cab) + 1e-12))
        if c > melhor_c:
            melhor, melhor_c = s, c
    comp = int(round((pl['fim_ep'] - pl['ini_ep']) * SR)) + (int(pl['saida_s'] * SR) if pl['ganho'] == 'do_corte' else 0)
    bed = np.zeros((comp, 2))
    pos, ini_arq, copias, emendas = 0, int(round(pl['de_arquivo'] * SR)), 0, []
    fade_out = np.cos(np.linspace(0, np.pi / 2, nc))[:, None]
    fade_in = np.sin(np.linspace(0, np.pi / 2, nc))[:, None]
    while True:
        pedaco = amb[ini_arq:].copy()
        if copias > 0:
            pedaco[:nc] *= fade_in
        ultima = pos + len(pedaco) >= comp
        if not ultima:
            pedaco[-nc:] *= fade_out
        colocar(bed, pedaco, pos)
        copias += 1
        if ultima:
            break
        pos, ini_arq = pos + len(pedaco) - nc, melhor
        emendas.append(round(pl['ini_ep'] + pos / SR, 3))
    na = int(pl['entrada_s'] * SR)
    bed[:na] *= rampa(na, 0, 1)[:, None]
    nsa = int(pl['saida_s'] * SR)
    bed[-nsa:] *= rampa(nsa, 1, 0)[:, None]
    if pl['ganho'] == 'do_corte':
        ganho, refg = g_amb, 'o mesmo ganho do ambiente do corte de 10 s'
    else:
        ganho, refg = ganho_rms_como_v2(pl)
    bed *= 10 ** (ganho / 20)
    out = np.zeros((N, 2))
    i0 = int(round(pl['ini_ep'] * SR))
    colocar(out, bed, i0)
    info = {'nome': pl['nome'], 'arquivo': 'assets/audio/fontes/' + pl['arquivo'], 'origem': pl['origem'],
            'toca_no_episodio_s': [round(i0 / SR, 3), round((i0 + comp) / SR, 3)],
            'entrada_s': pl['entrada_s'], 'saida_s': pl['saida_s'],
            'trecho_usado_do_arquivo_s': [pl['de_arquivo'], round(len(amb) / SR, 3)],
            'copias': copias, 'cruzamento_s': pl['cruzamento_s'], 'emendas_no_episodio_s': emendas,
            'cada_copia_seguinte_comeca_no_arquivo_s': round(melhor / SR, 3),
            'semelhanca_na_emenda_0a1': round(melhor_c, 2), 'ganho_db': round(ganho, 1),
            'referencia_do_ganho': refg, **({'filtro': pl['filtro']} if 'filtro' in pl else {}),
            **({'obs': pl['obs']} if 'obs' in pl else {})}
    return out, info


def todos_os_leitos(g_amb):
    soma = np.zeros((N, 2))
    infos = []
    for pl in PLANO['leitos']:
        o, inf = leito(pl, g_amb)
        soma += o
        infos.append(inf)
    return soma, infos


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


# ---------------- (1) ganho final (o leito já está fixo); (2) mix final ----------------
pf = PLANO['final']
teto = 10 ** (pf['teto_dbtp'] / 20)
j0 = int(round(pf['janela_limitador_ep'][0] * SR))
j1 = int(round(pf['janela_limitador_ep'][1] * SR))
GANHO_FINAL_V3 = 12.318725128886767   # o ganho final exato da v3 (repr do float do montar-v3.py)
# v4: uma passada só (na v3 eram até 4, para acertar o leito; aqui o leito é o da v3)
vol = curva_volume(leito_db)
mus = mus_rec_emendada * vol[:, None]
fx, g_amb = montar_efeitos(mus, registrar=False)
leitos_, _ = todos_os_leitos(g_amb)
fx += leitos_
# o ganho final: o maior possível sem nada FORA da janela do limitador passar do teto (é aí que está a voz)
pre = voz + mus + fx
os_all = np.abs(resample_poly(pre, 4, 1, axis=0)).max(1)
fora = np.ones(len(os_all), bool)
fora[j0 * 4:(j1 + int(0.3 * SR)) * 4] = False
k_pico = int(np.argmax(np.where(fora, os_all, 0)))
ganho_final = pf['teto_dbtp'] - 20 * np.log10(os_all[k_pico] + 1e-12)
t_pico = k_pico / 4 / SR
if t_pico >= cr0 - 0.1:
    raise SystemExit(f'o pico que decide o ganho final ({t_pico:.3f} s) caiu na emenda do fim: baixe a curva '
                     'volume_db da emenda_fim (nada depois da emenda pode mudar o volume do resto do episódio)')
if abs(ganho_final - GANHO_FINAL_V3) > 1e-9:
    raise SystemExit(f'o ganho final mudou ({ganho_final:+.4f} dB, pico em {t_pico:.3f} s; a v3 tinha '
                     f'{GANHO_FINAL_V3:+.4f}, pico em 26,954 s): uma fala nova passou a decidir o pico de tudo. Escolha '
                     'outra tomada (PLR menor) para não mudar o volume do episódio inteiro')
# só relatório: onde a trilha fica sob as falas 9, 10, 11 e 12 com a fala 10 nova (a v3 calibrou -30,5 LUFS aí)
mus_sem_emenda = mus_rec * curva_volume(leito_db, com_fim=False)[:, None]
leito_medido_v4 = lufs(mus_sem_emenda[idx_ref]) + ganho_final
vol = curva_volume(leito_db)
mus = mus_rec_emendada * vol[:, None]
fx, g_amb = montar_efeitos(mus, registrar=True)
leitos_, info_leitos = todos_os_leitos(g_amb)
fx += leitos_
doc['leitos'] = info_leitos
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
saida = os.path.join(AUDIO, 'mix-v4.wav')
sf.write(saida, mix.astype(np.float32), SR, subtype='PCM_24')
if '--voz-sozinha' in sys.argv:
    caminho_voz = sys.argv[sys.argv.index('--voz-sozinha') + 1]
    vz_ = voz * gf
    vz_[-nf:] *= rampa(nf, 1, 0)[:, None] ** 2
    sf.write(caminho_voz, vz_.astype(np.float32), SR, subtype='PCM_24')


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
    esc = pv['escolha_das_tomadas'].get(f['id'])
    doc['falas'].append({'id': f['id'], 'texto': f['texto'], 'tomada': 'assets/audio/fontes/' + f['arquivo'],
                         'fala': ('antiga (tomada A, aprovada)' if f['arquivo'] == TOMADA_A else
                                  'nova (v4)' if 'v4-novas' in f['arquivo'] else 'nova (v3)'),
                         'alvo_s': f['alvo'], 'comeca_s': round(r['comeca'], 3),
                         'termina_s': round(r['termina'], 3), 'deslizou_s': round(r['comeca'] - f['alvo'], 3),
                         'trecho_da_tomada_s': [f['de'], f['ate']],
                         'fala_na_tomada_s': [round(r['fala_arq'][0], 3), round(r['fala_arq'][1], 3)],
                         'clip_no_episodio_s': [round(r['clip'][0], 3), round(r['clip'][1], 3)],
                         'deslocamento_tomada_para_episodio_s': round(r['desloc'], 6),
                         'lufs_na_tomada': round(f['_lufs_cru'], 1),
                         'ganho_db': f['ganho_db'], 'ganho_total_db': round(f['ganho_db'] + ganho_final, 2),
                         'lufs_no_mix': round(lufs(vz[ii:jj]), 1),
                         'pico_real_dbtp': round(pico_real_db(vz[ii:jj]), 2),
                         'trilha_por_baixo_lufs': round(lufs(mz[ii:jj]), 1),
                         **({'escolha': esc} if esc else {}),
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
for lt in doc['leitos']:
    lt['ganho_total_db'] = round(lt['ganho_db'] + ganho_final, 1)
    a_, b_ = lt['toca_no_episodio_s']
    lt['lufs_no_mix'] = round(lufs(fz[int(a_ * SR):int(b_ * SR)]), 1)
trilha_por_frase = {}
for a_, b_ in pt['frases_do_piano'] + [[23.936, 25.9], [25.9, 27.266], [33.933, 36.733], [36.733, 40.3], [40.3, 43.7],
                                      [43.7, 46.7], [47.15, 53.5], [53.5, 58.5], [58.5, 61.26], [61.26, 66.9],
                                      [66.9, 71.7]]:
    trilha_por_frase[f'{a_:g}-{b_:g}'] = [round(lufs(mz[int(a_ * SR):int(b_ * SR)]), 1),
                                          round(lufs_sem_portao(mz[int(a_ * SR):int(b_ * SR)]), 1)]
# volume do mix inteiro por trecho (para ver o desenho do episódio)
por_cena = {}
for nome_c, (a_, b_) in {'s01': (0, 9.3), 's03': (9.3, 15.3), 's04': (15.3, 18.3), 's04b': (18.3, 21.6),
                         's05': (21.6, 25.9), 'virada até o impacto': (25.9, GOLPE_EP),
                         's08 (vídeo dela)': (GOLPE_EP, 46.7), 's09': (46.7, 53.5), 's10': (53.5, 58.5),
                         's11': (58.5, 66.9), 's12': (66.9, 71.7)}.items():
    por_cena[nome_c] = round(lufs(mix[int(a_ * SR):int(b_ * SR)]), 1)

# teste de subtração: a virada (25,94 s até 36,48 s, antes do fade de fim do corte) contra o corte de 10 s aprovado
corte, sr_c = sf.read(os.path.join(AUDIO, 'mix-corte10s.wav'), dtype='float64')
novo = sf.read(saida, dtype='float64')[0][I0:I0 + N_CORTE]
k_amb = int(0.040 * SR)
k_fim = N_CORTE - int(0.25 * SR)
dif = novo[:k_fim] - corte[:k_fim]


def nivel(x):
    return round(float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-15)), 1)


subtracao = {'nivel_do_corte_dbfs': nivel(corte[k_amb:k_fim]),
             'diferenca_25_90_a_25_94_dbfs': nivel(dif[:k_amb]),
             'diferenca_de_25_94_a_36_48_dbfs': nivel(dif[k_amb:]),
             'maior_diferenca_de_25_94_a_36_48_dbfs': round(float(20 * np.log10(np.abs(dif[k_amb:]).max() + 1e-15)), 1),
             'diferenca_por_segundo_dbfs': {f'{BASE_CORTE + s:.1f}': nivel(dif[int(s * SR):int((s + 1) * SR)])
                                            for s in range(0, 10)}}

# ---------------- v4: teste de subtração contra o mix-v3.wav ----------------
# Só podem mudar: a voz de F e de 10 (o clip de cada uma, v3 e v4) e o recorte de médias da trilha sob elas (a janela
# da fala +-0,20 s, com rampas de 0,15 s). Janela de cada fala = a união disso na v3 e na v4, mais FOLGA_SUB de cada lado.
# Fora das duas janelas a diferença tem de ser zero (as mesmas amostras).
FOLGA_SUB = 0.05
TROCADAS = ('F', '10')
v3_doc = json.load(open(os.path.join(AUDIO, 'audio-v3.json'), encoding='utf-8'))
mix_v3 = sf.read(os.path.join(AUDIO, 'mix-v3.wav'), dtype='float64')[0]
mix_v4 = sf.read(saida, dtype='float64')[0]
assert mix_v3.shape == mix_v4.shape, 'o mix-v4 não tem o mesmo tamanho do mix-v3'
clip_v3 = {fl['id']: fl['clip_no_episodio_s'] for fl in v3_doc['falas']}
rec_v3 = dict(zip([fl['id'] for fl in v3_doc['falas']], v3_doc['trilha']['recorte_medias']['janelas_s']))
rec_v4 = dict(zip([f['id'] for f in pv['falas']], janelas_recorte))
# as outras falas não podem ter mudado de lugar nem de recorte
for f in pv['falas']:
    if f['id'] not in TROCADAS:
        assert rec_v4[f['id']] == rec_v3[f['id']], f'o recorte sob a fala {f["id"]} mudou'
        assert [round(x, 3) for x in f['_real']['clip']] == clip_v3[f['id']], f'a fala {f["id"]} mudou de lugar'
dif_v3 = mix_v4 - mix_v3
fora_das_falas = np.ones(N, bool)
janelas_sub = {}
for id_ in TROCADAS:
    fv4 = falas_por_id[id_]['_real']
    a_ = min(clip_v3[id_][0], fv4['clip'][0], rec_v3[id_][0] - rr, rec_v4[id_][0] - rr) - FOLGA_SUB
    b_ = max(clip_v3[id_][1], fv4['clip'][1], rec_v3[id_][1] + rr, rec_v4[id_][1] + rr) + FOLGA_SUB
    janelas_sub[id_] = [round(a_, 3), round(b_, 3)]
    fora_das_falas[int(np.floor(a_ * SR)):int(np.ceil(b_ * SR))] = False
dif_fora = dif_v3[fora_das_falas]
amostras_dif = np.nonzero(np.abs(dif_v3).max(1) > 0)[0]
# o recorte de médias novo, só a trilha (sem a voz): quanto a trilha sob F e 10 mudou por causa da duração nova
env_rec_v3 = np.zeros(N)
for de_, ate_ in v3_doc['trilha']['recorte_medias']['janelas_s']:
    env_rec_v3 = np.maximum(env_rec_v3, np.interp(t, [de_ - rr, de_, ate_, ate_ + rr], [0, 1, 1, 0], left=0, right=0))
mus_rec_v3 = mus_cru + banda * ((10 ** (pt['recorte_medias_db'] / 20) - 1) * env_rec_v3)[:, None]
trilha_v3 = mus_rec_v3 * vol[:, None] * gf        # antes da emenda (F e 10 ficam antes de 61,0 s) e fora do limitador
trilha_v4 = mus_rec * vol[:, None] * gf
recorte_mudou = {}
for id_ in TROCADAS:
    a_, b_ = janelas_sub[id_]
    sl = slice(int(a_ * SR), int(b_ * SR))
    fv4 = falas_por_id[id_]['_real']
    fl3 = next(fl for fl in v3_doc['falas'] if fl['id'] == id_)
    i3, j3 = int(fl3['comeca_s'] * SR), int(fl3['termina_s'] * SR)
    i4, j4 = int(fv4['comeca'] * SR), int(fv4['termina'] * SR)
    d_tr = trilha_v4[sl] - trilha_v3[sl]
    recorte_mudou[id_] = {
        'janela_do_recorte_v3_s': rec_v3[id_], 'janela_do_recorte_v4_s': rec_v4[id_],
        'mudou_no_fim_s': round(rec_v4[id_][1] - rec_v3[id_][1], 3),
        'mudou_no_comeco_s': round(rec_v4[id_][0] - rec_v3[id_][0], 3),
        'trilha_sob_a_fala_lufs_v3': round(lufs(trilha_v3[i3:j3]), 1),
        'trilha_sob_a_fala_lufs_v4': round(lufs(trilha_v4[i4:j4]), 1),
        'diferenca_so_da_trilha_na_janela_dbfs': nivel(d_tr),
        'maior_diferenca_so_da_trilha_dbfs': round(float(20 * np.log10(np.abs(d_tr).max() + 1e-15)), 1),
        'nivel_da_trilha_na_janela_dbfs': nivel(trilha_v4[sl])}
subtracao_v3 = {
    'contra': 'assets/audio/mix-v3.wav',
    'janelas_excluidas_s': janelas_sub, 'folga_s': FOLGA_SUB,
    'diferenca_fora_das_janelas_dbfs': nivel(dif_fora),
    'maior_diferenca_fora_das_janelas_dbfs': round(float(20 * np.log10(np.abs(dif_fora).max() + 1e-15)), 1),
    'amostras_diferentes_fora_das_janelas': int((np.abs(dif_fora).max(1) > 0).sum()),
    'primeira_e_ultima_amostra_diferente_s': ([round(amostras_dif[0] / SR, 4), round(amostras_dif[-1] / SR, 4)]
                                              if len(amostras_dif) else []),
    'trechos_com_diferenca_s': [], 'recorte_de_medias': recorte_mudou,
    '_como_ler': ('-300 dBFS = nenhuma diferença (as mesmas amostras). "trechos_com_diferenca_s" = onde as amostras '
                  'diferem de verdade (juntando buracos de menos de 0,1 s)')}
for k in amostras_dif:
    if subtracao_v3['trechos_com_diferenca_s'] and k - subtracao_v3['trechos_com_diferenca_s'][-1][1] < int(0.1 * SR):
        subtracao_v3['trechos_com_diferenca_s'][-1][1] = k
    else:
        subtracao_v3['trechos_com_diferenca_s'].append([k, k])
subtracao_v3['trechos_com_diferenca_s'] = [[round(a_ / SR, 3), round(b_ / SR, 3)]
                                           for a_, b_ in subtracao_v3['trechos_com_diferenca_s']]
if subtracao_v3['amostras_diferentes_fora_das_janelas']:
    raise SystemExit(f'o mix-v4 difere do mix-v3 FORA das falas F e 10: {subtracao_v3}')

doc['trilha'] = {'arquivo': 'assets/audio/fontes/' + pt['arquivo'], 'candidata': 'B (2ª de 3)',
                 'golpe_no_arquivo_s': pt['golpe_no_arquivo'], 'golpe_no_episodio_s': GOLPE_EP,
                 'deslocamento_s': round(a_mus / SR, 4),
                 'musica_tocada_s': {'copia_1': [round((a_mus + int(e0 * SR)) / SR, 3),
                                                 round((a_mus + int(round(cr1 * SR))) / SR, 3)],
                                     'copia_2': [round((a_mus2 + int(round(cr0 * SR))) / SR, 3),
                                                 round((a_mus2 + N) / SR, 3)]},
                 'entrada_s': pt['entrada'], 'volume_fator_ate_46_5': pt['volume'],
                 'frases_do_piano_s': pt['frases_do_piano'],
                 'suspense_s04b': sus,
                 'relaxa': {**rx, 'leito_fator': round(10 ** (leito_db / 20), 4), 'leito_db': round(leito_db, 2),
                            'leito_medido_v4_lufs': round(leito_medido_v4, 2),
                            '_v4': ('o leito é o da v3 (leito_db_fixo), sem recalcular; com a fala 10 nova a trilha sob '
                                    'as falas 9, 10, 11 e 12 mede leito_medido_v4_lufs (alvo da v3: -30,5)')},
                 'realce': realce,
                 'recorte_medias': {'faixa_hz': [1000, 4000], 'db': pt['recorte_medias_db'],
                                    'janelas_s': janelas_recorte, 'rampa_s': rr},
                 'tratamento': ('sem esticar; deslocada (tempo da música = tempo do episódio + 2,744 s), com entrada '
                                'de 1,0 s e volume em curvas lentas; UMA emenda só, no fim (ver emenda_do_fim)'),
                 'emenda_do_fim': {
                     'por_que': ('sem ela a música resolvia em 60,61 s e sumia sozinha: a CTA (67,65) e o cartão final '
                                 '(66,9-71,7) ficavam quase sem música, com silêncio digital de ~70,2 s até o fim'),
                     'como': ('em 61,029-61,446 s a trilha cruza (potência igual) para uma 2ª cópia da mesma trilha, '
                              '2 compassos atrás; a 2ª cópia toca dó -> sol e resolve em lá menor em 67,275 s; a cauda '
                              'natural dela (notas de piano em 69,78 e 70,61) vai até o fim, com fade de 0,5 s'),
                     'atraso_s': round(atraso_amostras / SR, 5), 'atraso_amostras': atraso_amostras,
                     'compassos': 2, 'compasso_s': 3.3321, 'bpm': 72.03,
                     'cruzamento_no_episodio_s': pe['cruzamento'],
                     'cruzamento_na_copia_1_s': [round(cr0 + a_mus / SR, 3), round(cr1 + a_mus / SR, 3)],
                     'cruzamento_na_copia_2_s': [round(cr0 + a_mus2 / SR, 3), round(cr1 + a_mus2 / SR, 3)],
                     'tempo_da_musica_na_copia_2': f'tempo do episódio {a_mus2 / SR:+.4f} s',
                     'resolucao_da_copia_2_no_episodio_s': round(63.35 - a_mus2 / SR, 3),
                     'notas_de_piano_da_cauda_no_episodio_s': [round(65.855 - a_mus2 / SR, 2),
                                                               round(66.689 - a_mus2 / SR, 2)],
                     'semelhanca_das_notas_no_cruzamento': {'2_compassos_atras (escolhido)': [0.88, 0.91, 0.91, 0.88, 0.86],
                                                            '3_compassos_atras': [0.83, 0.73, 0.73, 0.70, 0.65],
                                                            '1_compasso_atras': [0.60, 0.47, 0.45, 0.49, 0.49],
                                                            '_em': 'semicolcheias 60,61 / 60,81 / 61,02 / 61,23 / 61,43 s'},
                     'volume_db_sobre_o_leito': pe['volume_db'], 'fade_s': pe['fade'],
                     'trilha_lufs': {nome_: round(lufs(mz[int(a_ * SR):int(b_ * SR)]), 1) for nome_, (a_, b_) in
                                     {'fala 13': (62.1, 66.382), 'vão 13-14 (cartão e resolução)': (66.382, 67.65),
                                      'fala 14': (67.65, 69.85), 'depois da fala 14': (69.85, 71.7)}.items()}},
                 # medido na v2 (cromagrama da música crua); os tempos aqui são os da v2 + 3,3 s (a música é a mesma)
                 'harmonia_medida': {
                     'tom': 'lá menor; depois do golpe a trilha B gira lá menor -> fá -> dó -> sol (a cada ~3,3 s) e '
                            'segue no volume cheio, com pulso, até 61,26 s do episódio; não relaxa sozinha',
                     'resolucao_no_episodio_s': 60.61, 'resolucao_na_musica_s': 63.35,
                     'resolucao': 'sol (tensão, de ~57,76 a 60,6 s) -> lá menor (o tom da música), com o salto de '
                                  'volume do acorde em 60,61 s; não existe acorde maior de resolução na trilha B',
                     'falas_sobre_a_resolucao': ('"o roteiro ela já tinha." (58,90) cai sobre o acorde de sol (a '
                                                 'tensão); "faltava tirar do papel." (60,40-61,53) cai sobre a '
                                                 'resolução (60,61)'),
                     'depois': ('sem a emenda, de 61,26 s em diante a música sumia sozinha (fade natural) e não sobrava '
                                'nada sob a CTA. Com a emenda (61,03-61,45), a 2ª cópia toca dó -> sol (tensão, sob '
                                '"o seu também já existe") e resolve de novo em lá menor em 67,275 s, com o cartão; a '
                                'cauda (o acorde sumindo e as notas de piano em 69,78 e 70,61) fica sob "comente '
                                'CLÍNICA..." e termina com o fade de 0,5 s em 71,7')}}
doc['final'] = {'arquivo': 'assets/audio/mix-v4.wav', 'duracao_s': round(info.frames / SR, 4),
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
                             'trilha_sozinha_lufs_por_trecho': trilha_por_frase,
                             '_trilha_por_trecho': ('[LUFS integrado (com portão, como na v2), LUFS sem portão (energia '
                                                    'média do trecho inteiro)]')},
                'teste_de_subtracao_contra_o_corte_de_10s': subtracao,
                'teste_de_subtracao_contra_o_mix_v3': subtracao_v3}
doc['_ganhos'] = ('ganho_db = ganho próprio da fala/evento (antes do ganho fixo final); ganho_total_db = ganho_db + '
                  'ganho fixo final, ou seja, quanto o arquivo de origem foi aumentado/abaixado no mix final.')
doc['escolha_das_tomadas'] = {'referencia_tomada_A': REF_A, 'referencia_tomada_A_v4': REF_A_V4,
                              **pv['escolha_das_tomadas']}


# ---------------- tempos por palavra (para as legendas e o lettering) ----------------
def norm(p):
    p = unicodedata.normalize('NFD', p.lower())
    p = ''.join(c for c in p if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', p)


def alinhar(esperado, ouvido):
    """alinha as palavras do texto com as do Whisper (distância de edição, trocar uma palavra por outra parecida custa
    menos: "pra" casa com "para", não com o "a" seguinte); devolve, para cada palavra do texto, o índice da palavra
    do Whisper que corresponde a ela (ou None se o Whisper não a escreveu)"""
    a, b = [norm(x) for x in esperado], [norm(x) for x in ouvido]
    n, m = len(a), len(b)

    def troca(x, y):
        return 0.0 if x == y else 1.0 - SequenceMatcher(None, x, y).ratio() + 0.05

    d = np.zeros((n + 1, m + 1))
    d[:, 0] = np.arange(n + 1)
    d[0, :] = np.arange(m + 1)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i, j] = min(d[i - 1, j] + 1, d[i, j - 1] + 1, d[i - 1, j - 1] + troca(a[i - 1], b[j - 1]))
    par, i, j = [None] * n, n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and abs(d[i, j] - (d[i - 1, j - 1] + troca(a[i - 1], b[j - 1]))) < 1e-9:
            par[i - 1] = j - 1
            i, j = i - 1, j - 1
        elif i > 0 and abs(d[i, j] - (d[i - 1, j] + 1)) < 1e-9:
            i -= 1
        else:
            j -= 1
    return par


TEXTOS_DA_TOMADA = {   # a ordem das falas dentro de cada tomada (o que foi pedido ao ElevenLabs)
    TOMADA_A: ['décima quarta tentativa.', 'e o vídeo não sai.',
               'a doutora Helena explica a prótese protocolo toda semana, paciente por paciente.',
               'o roteiro sobre implantes está pronto há seis semanas.', 'a gravação, não.',
               'ela não gravou a décima quinta.', 'mandou só o roteiro.', 'cada linha que ela escreveu virou uma cena.',
               'o perfil voltou a andar.', 'ela mandou o vídeo pra turma.', 'o roteiro ela já tinha.',
               'no próximo episódio: o que a recepção mais ouve.'],
    **{f'narracao-v3-novas-{x}.mp3': ['quarenta e sete dias sem postar nada.', 'mas isso está prestes a mudar...',
                                      'o roteiro ela já tinha.', 'faltava tirar do papel.',
                                      'se você explica isso todo dia no consultório, o seu também já existe.',
                                      'comente clínica e a gente te mostra como.'] for x in 'abc'},
    **{f'narracao-v4-novas-{x}.mp3': ['dezessete dias sem postar nada.', 'ela mandou o vídeo pra Lúcia.']
       for x in 'abc'},
}


def palavras_na_tomada(arquivo):
    """para cada fala da tomada, a lista [(palavra do texto, início, fim)] em segundos da tomada (Whisper)"""
    w = json.load(open(os.path.join(AQUI, os.path.splitext(arquivo)[0] + '.palavras.json'), encoding='utf-8'))
    ouvido = [p for p in w['palavras'] if norm(p['palavra'])]
    linhas = TEXTOS_DA_TOMADA[arquivo]
    esperado = [(k, p) for k, ln in enumerate(linhas) for p in ln.split()]
    par = alinhar([p for _, p in esperado], [p['palavra'] for p in ouvido])
    # uma palavra a mais do Whisper (ex.: ele ouve "para a" onde o texto diz "pra") entra no tempo da anterior
    fim_de = {}
    usados = sorted(j for j in par if j is not None)
    for j_, j_prox in zip(usados, usados[1:] + [len(ouvido)]):
        fim_de[j_] = ouvido[j_prox - 1]['fim'] if j_prox - 1 > j_ else ouvido[j_]['fim']
    por_linha = {}
    for (k, p), j in zip(esperado, par):
        por_linha.setdefault(linhas[k], []).append([p, None if j is None else ouvido[j]['inicio'],
                                                    None if j is None else fim_de[j]])
    for ln, lst in por_linha.items():      # palavra que o Whisper não escreveu: divide o espaço das vizinhas
        for q, (p, a_, b_) in enumerate(lst):
            if a_ is None:
                ant = next((x[2] for x in reversed(lst[:q]) if x[2] is not None), None)
                prox = next((x[1] for x in lst[q + 1:] if x[1] is not None), None)
                lst[q][1] = lst[q][2] = ant if ant is not None else prox
    return por_linha


def silabas(palavra):
    """conta as sílabas de uma palavra (aproximado: grupos de vogais; ditongos contam 1)"""
    w = norm(palavra).replace('qu', 'q').replace('gu', 'g')
    k = 0
    for v in re.findall(r'[aeiou]+', w):
        k += 1 if len(v) == 1 or v in ('ai', 'ei', 'oi', 'ou', 'eu', 'au', 'iu', 'ui', 'ao', 'ae', 'oe') else len(v)
    return max(k, 1)


PAUSA_MIN_PALAVRAS = 0.10    # silêncio (< -50 dBFS) de 0,10 s ou mais dentro da fala = fronteira entre palavras
doc_pal = {'_sobre': ('Tempo de cada palavra de cada fala, em segundos do EPISÓDIO v4 (para as legendas e o lettering). '
                      'Gerado por fonte/audio/montar-v4.py junto com o mix-v4.wav. Igual ao voz-v3.palavras.json, menos '
                      'as falas F ("dezessete dias sem postar nada.", tomada narracao-v4-novas-c) e 10 ("ela mandou o '
                      'vídeo pra Lúcia.", tomada narracao-v4-novas-a), que são novas (nelas o Whisper escreve "para a" '
                      'onde a fala diz "pra": aqui fica "pra", o que é falado). Como: o Whisper (large-v3) de cada '
                      'tomada de origem (fonte/audio/*.palavras.json) levado pelo deslocamento exato do recorte de cada '
                      'fala; a 1ª palavra começa no começo real do som da fala e a última termina no fim real (volume '
                      'em janelas de 2 ms acima de -50 dBFS); onde há um silêncio de 0,10 s ou mais dentro da fala, a '
                      'fronteira entre as duas palavras vai para ele (a anterior termina quando o silêncio começa e a '
                      'seguinte começa quando ele acaba). Dentro da fala corrida, a fronteira é a do Whisper (ele '
                      'costuma marcar ~0,1 s antes do som; ver conferência no LEIA-ME), menos nas falas T e 14, que '
                      'comandam a imagem (lettering de s04b, pílula CLÍNICA de s12): nelas as fronteiras foram medidas '
                      'no som (ver fronteiras_medidas no montar-v4.py).'),
           'duracao_s': DUR, 'falas': []}
for f in pv['falas']:
    r = f['_real']
    lst = palavras_na_tomada(f['arquivo'])[f['texto']]
    ini_a, fim_a = r['fala_arq']
    tomada = ler(f['arquivo'], 1)[:, 0]
    ev, _ = env_db(tomada, 2)
    k0, k1 = int(round(ini_a / 0.002)), int(round(fim_a / 0.002))
    sil = ev[k0:k1] <= PLANO['voz']['limiar_fala_dbfs']
    corridas, k = [], 0
    while k < len(sil):
        if sil[k]:
            j = k
            while j < len(sil) and sil[j]:
                j += 1
            if (j - k) * 0.002 >= PAUSA_MIN_PALAVRAS:
                corridas.append(((k0 + k) * 0.002, (k0 + j) * 0.002))
            k = j
        else:
            k += 1
    ws = [[p, max(min(a_, fim_a), ini_a), max(min(b_, fim_a), ini_a)] for p, a_, b_ in lst]
    ws[0][1] = ini_a
    ws[-1][2] = fim_a
    for s0, s1 in corridas:
        # cada silêncio vira uma fronteira: as palavras cujo meio (no Whisper) fica antes do silêncio ficam antes
        # dele; as outras (inclusive uma que o Whisper pôs DENTRO do silêncio: ele costuma "puxar" a palavra seguinte
        # para dentro da pausa) começam depois dele
        meio = [0.5 * (w_[1] + w_[2]) for w_ in ws]
        antes = [q for q in range(len(ws)) if meio[q] < s0]
        if not antes or antes[-1] == len(ws) - 1:
            continue
        q = antes[-1]
        if ws[q][1] < s0:                 # a anterior vai até o silêncio; a seguinte começa quando ele acaba
            ws[q][2] = s0
        ws[q + 1][1] = max(ws[q + 1][1], s1)
    medidas = pv['fronteiras_medidas'].get(f['id'])
    if medidas:                           # fronteiras medidas no som (ver o PLANO): substituem as do Whisper
        assert [m_[0] for m_ in medidas] == [w_[0] for w_ in ws], f'fronteiras_medidas da fala {f["id"]}'
        for q, (_, ini_m) in enumerate(medidas):
            if ini_m is not None:
                ws[q][1] = ini_m
        for q in range(len(ws) - 1):
            fim_q = ws[q + 1][1]
            for s0, s1 in corridas:       # se há um silêncio entre as duas, a palavra termina quando ele começa
                if ws[q][1] < s0 and s1 <= ws[q + 1][1] + 1e-6:
                    fim_q = s0
            ws[q][2] = fim_q
        ws[-1][2] = fim_a
    for q in range(len(ws)):              # sem sobreposição; palavra de duração zero ganha 40 ms
        if q:
            ws[q][1] = max(ws[q][1], ws[q - 1][2])
        ws[q][2] = max(ws[q][2], ws[q][1] + 0.04)
    if not medidas:
        # palavra de 2 sílabas ou mais que o Whisper deixou curta demais (menos de 65 ms por sílaba; ex.: "toda" com
        # 50 ms, porque ele começa a seguinte cedo): ela avança sobre o começo da seguinte, se a seguinte continuar
        # com o mínimo dela
        for q in range(len(ws) - 1):
            min_q = 0.065 * silabas(ws[q][0]) if silabas(ws[q][0]) >= 2 else 0.04
            min_prox = 0.065 * silabas(ws[q + 1][0]) if silabas(ws[q + 1][0]) >= 2 else 0.04
            falta = ws[q][1] + min_q - ws[q][2]
            if falta > 0 and ws[q][2] == ws[q + 1][1]:
                folga = (ws[q + 1][2] - ws[q + 1][1]) - min_prox
                d_ = min(falta, max(folga, 0.0))
                ws[q][2] += d_
                ws[q + 1][1] += d_
    if ws[-1][2] > fim_a:                 # o último ajuste nunca passa do fim real da fala
        ws[-1][2] = fim_a
    dsl = r['desloc']
    doc_pal['falas'].append({'id': f['id'], 'texto': f['texto'], 'comeca': round(r['comeca'], 3),
                             'termina': round(r['termina'], 3),
                             'tomada': 'assets/audio/fontes/' + f['arquivo'],
                             'palavras': [{'palavra': p, 'inicio': round(a_ + dsl, 3), 'fim': round(b_ + dsl, 3)}
                                          for p, a_, b_ in ws]})
# v4: as outras 14 falas têm de sair IGUAIS às do voz-v3.palavras.json (mesmo texto, tempos e palavras)
pal_v3 = {fl['id']: fl for fl in json.load(open(os.path.join(AUDIO, 'voz-v3.palavras.json'), encoding='utf-8'))['falas']}
assert [fl['id'] for fl in doc_pal['falas']] == list(pal_v3), 'a ordem das falas mudou'
for fl in doc_pal['falas']:
    if fl['id'] not in TROCADAS and fl != pal_v3[fl['id']]:
        raise SystemExit(f'a fala {fl["id"]} saiu diferente do voz-v3.palavras.json')
palavras_iguais_v3 = [fl['id'] for fl in doc_pal['falas'] if fl == pal_v3[fl['id']]]
with open(os.path.join(AUDIO, 'voz-v4.palavras.json'), 'w', encoding='utf-8') as fo:
    json.dump(doc_pal, fo, ensure_ascii=False, indent=1)
doc['final']['voz_palavras'] = {'arquivo': 'assets/audio/voz-v4.palavras.json',
                                'falas_iguais_ao_voz_v3': palavras_iguais_v3,
                                'falas_novas': [{'id': fl['id'], 'texto': fl['texto'], 'comeca': fl['comeca'],
                                                 'termina': fl['termina'],
                                                 'palavras': [[w_['palavra'], w_['inicio'], w_['fim']]
                                                              for w_ in fl['palavras']]}
                                                for fl in doc_pal['falas'] if fl['id'] in TROCADAS]}

for f in pv['falas']:
    for k in [k for k in f if k.startswith('_')]:
        f.pop(k)
with open(os.path.join(AUDIO, 'audio-v4.json'), 'w', encoding='utf-8') as fo:
    json.dump(doc, fo, ensure_ascii=False, indent=1)

sys.stdout.reconfigure(encoding='utf-8')
print(f'\nganho fixo final {ganho_final:+.2f} dB (limitado pelo pico real em {t_pico:.3f} s: {quem_pico})')
print(f'leito da trilha depois de 46,5 s: fator {10 ** (leito_db / 20):.4f} ({leito_db:.4f} dB)')
print('emenda do fim:', {k_: doc['trilha']['emenda_do_fim'][k_] for k_ in
                         ('atraso_amostras', 'cruzamento_no_episodio_s', 'cruzamento_na_copia_1_s',
                          'cruzamento_na_copia_2_s', 'resolucao_da_copia_2_no_episodio_s', 'trilha_lufs')})
print(f'limitador (trilha+efeitos, {pf["janela_limitador_ep"]}): {reducao_max:.2f} dB no máximo; '
      f'{doc["final"]["limitador"]["tempo_com_mais_de_1_db_s"]} s com mais de 1 dB, '
      f'{doc["final"]["limitador"]["tempo_com_mais_de_3_db_s"]} s com mais de 3 dB; trechos > 3 dB: {trechos_forte}')
print(f'FINAL: {lufs_i:.1f} LUFS, pico real {tp:.1f} dBTP, LRA {lra} LU, {info.frames / SR:.4f} s, '
      f'{info.samplerate} Hz, {info.channels} canais')
for fl in doc['falas']:
    print(f"  {fl['id']:>2} {fl['comeca_s']:6.3f}-{fl['termina_s']:6.3f} s (alvo {fl['alvo_s']:5.2f}, deslizou "
          f"{fl['deslizou_s']:+.3f}) ganho {fl['ganho_db']:+5.2f} -> {fl['lufs_no_mix']:6.1f} LUFS, pico "
          f"{fl['pico_real_dbtp']:6.2f} dBTP, trilha {fl['trilha_por_baixo_lufs']:6.1f}  {fl['texto']}")
print(f'voz {lufs_voz:.1f} LUFS; trilha sob a voz {lufs_mus_sob:.1f} LUFS ({lufs_voz - lufs_mus_sob:.1f} dB abaixo); '
      f'efeitos sob a voz {lufs_fx_sob:.1f} LUFS')
print('trilha sozinha, LUFS por trecho [com portão, sem portão]:', trilha_por_frase)
print('mix por cena:', por_cena)
print('leitos:', [(lt['nome'], lt['toca_no_episodio_s'], lt['copias'], lt['emendas_no_episodio_s'],
                   lt['semelhanca_na_emenda_0a1'], lt['ganho_db'], lt['lufs_no_mix']) for lt in doc['leitos']])
print(f'golpe no arquivo final: {golpe_real:.3f} s (alvo {GOLPE_EP:.3f})')
print('subtração contra o corte de 10 s:', subtracao)
print(f'leito medido sob 9/10/11/12 com a fala 10 nova: {leito_medido_v4:.2f} LUFS (a v3 calibrou -30,5; o leito ficou '
      'o da v3)')
print('subtração contra o mix-v3.wav:', {k_: v_ for k_, v_ in subtracao_v3.items() if k_ != '_como_ler'})
print('voz-v4.palavras.json: iguais ao voz-v3:', palavras_iguais_v3)
for fl in doc['final']['voz_palavras']['falas_novas']:
    print(f"  {fl['id']} {fl['comeca']:.3f}-{fl['termina']:.3f}", fl['palavras'])
print('->', saida)
