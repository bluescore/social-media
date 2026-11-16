"""Monta o áudio do CORTE AMPLIADO do ep. 01: do início do episódio (0 s) até onde termina o corte de 10 s (36,133 s).

O vídeo ampliado tem 36,3 s (1.089 quadros a 30 por segundo); o áudio vai de 0 a 36,133 s e o resto é silêncio.
A partir de 25,3 s este arquivo É o corte de 10 s (montar-corte10s.py), sem mudar nada: os mesmos arquivos, os mesmos
recortes, os mesmos volumes e os mesmos tempos, só deslocados 25,3 s (1.214.400 amostras). Antes disso entram as 7
primeiras falas, a trilha a partir de 4,0 s e os efeitos das cenas 1 a 5. O script confere isso no fim (teste de
"subtração": tira o corte de 10 s de dentro deste arquivo e mede o que sobra).

Regras que este script segue (regras do dono e do SPEC):
  - a voz NUNCA é esticada, acelerada, emendada nem passa por limitador: cada fala é recortada da tomada A só no meio
    das pausas e colocada no seu tempo; se uma fala não cabe antes da próxima, a próxima desliza (o mínimo possível);
  - a trilha NUNCA é esticada nem cortada entre a entrada e o golpe: ela só é deslocada para o golpe cair em 33,333 s
    (quadro 1000) e tem o volume ajustado; a entrada é um fade de 1,0 s;
  - um ganho fixo final (o mesmo do começo ao fim, e o mesmo do corte de 10 s) e o limitador só na janela do impacto;
  - fade de 0,25 s só no fim; os efeitos têm só entradas/saídas curtas para não estalar.

Para mudar alguma coisa, mexa no PLANO abaixo e rode de novo:
    python -I fonte/audio/montar-corte-ampliado.py
Entradas: assets/audio/fontes/*.mp3 (tudo baixado do ElevenLabs) e assets/audio/mix-corte10s.wav (só para conferir)
Saídas:   assets/audio/mix-corte-ampliado.wav (48 kHz, estéreo, 24 bits, 36,133 s)
          assets/audio/audio-corte-ampliado.json (cada fala e cada evento: arquivo, tempo, ganho; medições)
"""
import json
import os
import re
import subprocess

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.ndimage import minimum_filter1d
from scipy.signal import butter, resample_poly, sosfiltfilt

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(os.path.dirname(AQUI))
AUDIO = os.path.join(PECA, 'assets', 'audio')
FONTES = os.path.join(AUDIO, 'fontes')
SR = 48000
DUR = 36.133                      # 0 a 36,133 s do episódio (o corte de 10 s termina aqui)
N = int(round(DUR * SR))
BASE_CORTE = 25.3                 # onde o corte de 10 s começa no episódio
I0 = int(round(BASE_CORTE * SR))  # 1.214.400 amostras
DUR_CORTE = 10.833
N_CORTE = int(round(DUR_CORTE * SR))
GOLPE_CORTE = 8.033               # quadro 241 do corte
GOLPE_EP = BASE_CORTE + GOLPE_CORTE  # 33,333 s = quadro 1000 do episódio

# ----------------------------------------------------------------------------------------------------------------
# PLANO
# Tempos "no_ep" = segundos do episódio. Tempos "no_corte" (itens marcados do_corte) = segundos do corte de 10 s,
# copiados sem mudança do montar-corte10s.py; eles caem em no_corte + 25,3 s do episódio.
# "ancora" diz QUE ponto do arquivo cai nesse tempo:
#   inicio      = onde o som começa (primeiro ponto a 30 dB do pico do trecho usado)
#   trecho      = o começo do trecho usado ("de"), sem procurar nada
#   transiente  = o estalo principal (primeiro ponto a 6 dB do pico dentro de "busca", em segundos do arquivo)
#   pico        = o ponto mais forte (volume em janelas de 20 ms)
#   fim         = o fim do trecho usado
# "de"/"ate" = trecho do arquivo usado (recorte); "pico_alvo_db" = pico (janelas de 1 ms) antes do ganho final.
# ----------------------------------------------------------------------------------------------------------------
PLANO = {
    'voz': {
        'arquivo': 'narracao-amedeiros-v4-a.mp3',
        'limiar_fala_dbfs': -50.0,      # a fala "existe" onde o volume (janelas de 2 ms) passa disso, na tomada crua
        'pausa_minima_s': 0.25,         # se uma fala não cabe, a próxima começa 0,25 s depois do fim dela
                                        # (0,25 s = a menor pausa entre frases que a própria tomada A faz)
        'entrada_saida_s': 0.015,       # entrada/saída de 15 ms, dentro das pausas (silêncio)
        # de/ate = trecho da tomada (no meio das pausas); alvo = onde a fala deve começar no episódio
        'falas': [
            {'texto': 'décima quarta tentativa.', 'de': 0.000, 'ate': 2.093, 'alvo': 0.10, 'ganho_db': -8.0,
             'entrada_s': 0.003, 'obs': 'a tomada começa já falando (0,002 s): entrada de 3 ms; ganho 0,4 dB abaixo '
                                       'das outras para o pico real não passar de -1,2 dBTP'},
            {'texto': 'e o vídeo não sai.', 'de': 2.217, 'ate': 3.668, 'alvo': 2.00, 'ganho_db': -7.6},
            {'texto': 'a doutora Helena explica a prótese protocolo toda semana, paciente por paciente.',
             'de': 3.732, 'ate': 8.950, 'alvo': 4.40, 'ganho_db': -7.6},
            {'texto': 'o roteiro sobre implantes está pronto há seis semanas.', 'de': 8.950, 'ate': 12.281,
             'alvo': 10.10, 'ganho_db': -8.3,
             'obs': 'ganho 0,7 dB abaixo das outras: o "o" de "o roteiro" (10,22 s) somado à trilha passaria de -1,2 dBTP'},
            {'texto': 'a gravação, não.', 'de': 12.281, 'ate': 13.904, 'alvo': 14.50, 'ganho_db': -7.6},
            {'texto': 'ela não gravou a décima quinta.', 'de': 13.974, 'ate': 15.813, 'alvo': 20.90, 'ganho_db': -7.6},
            {'texto': 'mandou só o roteiro.', 'de': 15.813, 'ate': 17.090, 'alvo': 23.40, 'ganho_db': -7.6},
            # a fala do corte de 10 s, exatamente como lá (17,090-19,775 s da tomada; a fala começa em 1,000 do corte)
            {'texto': 'cada linha que ela escreveu virou uma cena.', 'de': 17.090, 'ate': 19.775, 'alvo': 26.30,
             'ganho_db': -7.6, 'do_corte': True, 'fala_comeca_no_arquivo': 17.290, 'fala_comeca_no_corte': 1.000},
        ],
    },
    'trilha': {
        'arquivo': 'trilha-tema-b.mp3',
        'golpe_no_arquivo': 36.677,             # ataque do golpe (medido com 1 ms; ver fonte/audio/golpes.json)
        'entrada': [4.0, 5.0],                  # a música começa a soar em 4,0 s e chega ao 1º volume em 5,0 s (curva suave)
        # volume (fator) ao longo do episódio; entre os pontos o volume muda em linha reta (em dB).
        # De 25,3 s em diante é EXATAMENTE o envelope do corte de 10 s (0,14 até 28,8; sobe até 0,45 em 33,3).
        # Antes de 25,3 s o fator NÃO é 0,14 fixo: a trilha B tem notas fortes entre 6,7 e 12,9 s e em 16,7 e 20,0 s
        # do episódio e fica fraca justo de 25,3 a 28,8 s; com 0,14 fixo ela tocaria até 8,6 dB mais alto antes do
        # corte e cairia 7,4 dB em 25,3 s. Por isso o fator muda uma vez por frase do piano (uma nota a cada 3,33 s),
        # com rampa de 0,3 s que termina 20 ms antes da nota, para o volume de cada frase subir em linha reta de
        # -45,5 LUFS (5 s) a -43,0 LUFS (25,3 s), antes do ganho final, e emendar no corte sem degrau.
        'volume': [[5.0, 0.075], [6.336, 0.075], [6.636, 0.05], [9.671, 0.05], [9.971, 0.064], [12.631, 0.064],
                   [12.931, 0.16], [16.341, 0.16], [16.641, 0.077], [19.666, 0.077], [19.966, 0.103],
                   [23.016, 0.103], [23.316, 0.047], [25.3, 0.14],          # última frase: sobe junto com a nota que cai
                   [28.8, 0.14], [33.3, 0.45], [DUR, 0.45]],
        'frases_do_piano': [[5.0, 6.656], [6.656, 9.991], [9.991, 12.951], [12.951, 16.661], [16.661, 19.986],
                            [19.986, 23.336], [23.336, 25.3], [25.3, 26.666], [26.666, 28.8]],
        # recorte de médias (1-4 kHz) na trilha enquanto a voz fala, para abrir espaço para ela (o mesmo do corte)
        'recorte_medias_db': -4.0, 'recorte_folga_s': 0.20, 'recorte_rampa_s': 0.15,
        'recorte_do_corte': [0.80, 3.50],       # a janela da fala do corte, sem mudança (em segundos do corte)
    },
    # o leito de ambiente de 0 a 25,3 s: a tomada b (5 s, estável) repetida com cruzamentos; em 25,3 s entra o
    # ambiente do corte de 10 s (o mesmo arquivo, desde o começo), e o leito sai em 40 ms por baixo dele.
    'leito_ambiente': {
        'nome': 'ambiente de consultório à noite (leito de 0 a 25,3 s)', 'arquivo': 'ambiente-noite-b.mp3',
        'cruzamento_s': 0.5, 'entrada_s': 0.010, 'fim_ep': BASE_CORTE, 'saida_s': 0.040,
        'busca_emenda_s': [0.0, 1.5],           # onde procurar, no começo da cópia seguinte, o ponto que melhor encaixa
    },
    'efeitos': [
        # ---------------- cenas 1 a 5 (novos) ----------------
        {'nome': 'toque seco no vidro ("apagar")', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 2.230, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0},
        {'nome': 'tique seco do contador (take 14 -> take 15)', 'arquivo': 'tique-contador-a.mp3', 'de': 0.085,
         'ate': 0.135, 'ancora': 'transiente', 'busca': [0.095, 0.110], 'no_ep': 3.100, 'entrada_s': 0.003,
         'saida_s': 0.010, 'pico_alvo_db': -37.0},
        {'nome': 'sopro grave do recuo que revela a maquete', 'arquivo': 'sopro-grave-d.mp3', 'de': 0.0, 'ate': 2.56,
         'ancora': 'pico', 'no_ep': 5.300, 'entrada_s': 0.05, 'saida_s': 0.50, 'pico_alvo_db': -38.0,
         'obs': 'o pico do sopro cai em 5,3 s, a metade do recuo (4,0-6,6 s, power2.inOut = mais rápido no meio)'},
        {'nome': 'papel farfalhando de leve (a folha chega)', 'arquivo': 'papel-farfalhando-a.mp3', 'de': 0.0,
         'ate': 0.85, 'ancora': 'inicio', 'no_ep': 10.300, 'entrada_s': 0.01, 'saida_s': 0.20, 'pico_alvo_db': -42.0},
        {'nome': 'risco de caneta em "gravar 06/11"', 'arquivo': 'risco-caneta-c.mp3', 'de': 0.0, 'ate': 0.36,
         'ancora': 'trecho', 'no_ep': 15.260, 'entrada_s': 0.005, 'saida_s': 0.08, 'pico_alvo_db': -43.0,
         'obs': 'cai no "não" de "a gravação, não." (15,42 s), a fala mais baixa da tomada: fica 8 dB abaixo dela'},
        {'nome': 'toque seco no vidro (abre o perfil)', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 17.270, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0},
        {'nome': 'atrito suave da rolagem da tela', 'arquivo': 'rolagem-tela-a.mp3', 'de': 0.30, 'ate': 1.0,
         'ancora': 'trecho', 'no_ep': 17.330, 'entrada_s': 0.03, 'saida_s': 0.25, 'pico_alvo_db': -40.0,
         'obs': 'trecho a partir de 0,30 s do arquivo (na conferência, era 0,10): o começo do arquivo sobe devagar e, '
                'com 0,10, o atrito só se ouvia em 17,45-17,54 s (4 a 6 quadros depois do dedo) e ficava mais forte '
                'em 17,70. Agora se ouve já em 17,33-17,34, fica mais forte em 17,50 (o começo da rolagem com '
                'inércia, a parte mais rápida) e some por volta de 17,8, enquanto a tela desliza até parar em 18,33. '
                'Mesmo arquivo, mesmo volume (o pico do trecho é o mesmo)'},
        {'nome': 'obturador do celular (fecha e reabre)', 'arquivo': 'obturador-a.mp3', 'de': 0.0, 'ate': 0.30,
         'ancora': 'trecho', 'no_ep': 22.500, 'entrada_s': 0.002, 'saida_s': 0.10, 'pico_alvo_db': -37.0,
         'obs': 'dois estalos (fecha em 22,53 e reabre em 22,61), como a tela que fecha e reabre em 0,15 s; no '
                'volume percebido fica no nível do interruptor do abajur (é o estalo mais brilhante do arquivo)'},
        {'nome': 'toque seco no vidro ("enviado")', 'arquivo': 'toque-vidro-c.mp3', 'de': 0.088, 'ate': 0.220,
         'ancora': 'transiente', 'busca': [0.09, 0.11], 'no_ep': 22.900, 'entrada_s': 0.003, 'saida_s': 0.040,
         'pico_alvo_db': -34.0},
        # ---------------- do corte de 10 s, sem nenhuma mudança (tempos do corte; caem em +25,3 s) ----------------
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
    ],
    'final': {
        'alvo_lufs': -14.0,
        'teto_dbtp': -1.2,                    # teto do pico real fora do impacto (um pouco abaixo de -1 por segurança)
        'janela_impacto_corte': [8.013, 8.85],  # único trecho em que o limitador pode agir (segundos do corte)
        'limitador_max_db': 3.0,
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
    """amostra do episódio onde cai um ponto: itens do corte usam a mesma conta do corte + 1.214.400 amostras"""
    if e.get('do_corte') or 'no_corte' in e:
        return I0 + int(round(t_relativo * SR))
    return int(round(t_relativo * SR))


medidor = pyln.Meter(SR)
doc = {'_sobre': ('Áudio do CORTE AMPLIADO do ep. 01 (sala de espera): do início do episódio (0 s) até 36,133 s, onde '
                  'termina o corte de 10 s. Tempos em segundos do EPISÓDIO (o corte de 10 s começa em 25,300 s; o golpe '
                  'é o quadro 1000 = 33,333 s). De 25,3 s em diante é o corte de 10 s sem mudança. Gerado por '
                  'fonte/audio/montar-corte-ampliado.py; para mudar, edite o PLANO no script e rode de novo.'),
       'duracao_s': DUR, 'duracao_do_video_s': 36.3, 'amostragem_hz': SR, 'canais': 2,
       'corte_de_10s_comeca_em_s': BASE_CORTE, 'falas': [], 'eventos': []}

# ---------------- voz: cada fala recortada nas pausas da tomada A ----------------
pv = PLANO['voz']
tomada = ler(pv['arquivo'], 1)[:, 0]
ev_tomada, hop_v = env_db(tomada, 2)          # grade de 2 ms da tomada inteira
voz = np.zeros(N)
fim_anterior_ep = -1.0
fim_clip_anterior = -1
for f in pv['falas']:
    a_t, b_t = int(round(f['de'] * SR)), int(round(f['ate'] * SR))
    k0, k1 = int(np.ceil(f['de'] / 0.002 - 1e-6)), int(f['ate'] / 0.002 + 1e-6)
    ativo = np.nonzero(ev_tomada[k0:k1] > pv['limiar_fala_dbfs'])[0]
    fala_ini_arq, fala_fim_arq = (k0 + ativo[0]) * 0.002, (k0 + ativo[-1] + 1) * 0.002
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
    colocar(voz, trecho, i_clip)
    termina = comeca + (fala_fim_arq - fala_ini_arq)
    f['_real'] = dict(comeca=comeca, termina=termina, clip=[i_clip / SR, (i_clip + len(trecho)) / SR],
                      fala_arq=[fala_ini_arq, fala_fim_arq])
    fim_anterior_ep, fim_clip_anterior = termina, i_clip + len(trecho)
voz = np.c_[voz, voz]

# ---------------- trilha ----------------
pt = PLANO['trilha']
musica_inteira = ler(pt['arquivo'], 2)
a_mus = int(round((pt['golpe_no_arquivo'] - GOLPE_CORTE) * SR)) - I0   # a mesma conta do corte, menos 25,3 s
mus = musica_inteira[a_mus:a_mus + N].copy()
assert len(mus) == N
t = np.arange(N) / SR
pts = np.array(pt['volume'])
vol = 10 ** (np.interp(t, pts[:, 0], 20 * np.log10(pts[:, 1])) / 20)
e0, e1 = pt['entrada']
x_ent = np.clip((t - e0) / (e1 - e0), 0, 1)
vol = np.where(t < e1, pts[0, 1] * np.sin(np.pi / 2 * x_ent), vol)       # entrada suave (curva seno) de 4,0 a 5,0 s
# recorte de médias sob cada fala (filtro sem atraso de fase = corte limpo)
banda = sosfiltfilt(butter(2, [1000, 4000], 'bandpass', fs=SR, output='sos'), mus, axis=0)
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
mus = mus + banda * ((10 ** (pt['recorte_medias_db'] / 20) - 1) * env_rec)[:, None]
mus *= vol[:, None]

doc['trilha'] = {'arquivo': 'assets/audio/fontes/' + pt['arquivo'], 'candidata': 'B (2ª de 3)',
                 'golpe_no_arquivo_s': pt['golpe_no_arquivo'], 'golpe_no_episodio_s': GOLPE_EP,
                 'deslocamento_s': round(a_mus / SR, 3),
                 'musica_tocada_s': [round((a_mus + int(e0 * SR)) / SR, 3), round((a_mus + N) / SR, 3)],
                 'entrada_s': pt['entrada'], 'volume_fator': pt['volume'],
                 'recorte_medias': {'faixa_hz': [1000, 4000], 'db': pt['recorte_medias_db'],
                                    'janelas_s': janelas_recorte, 'rampa_s': rr},
                 'tratamento': ('sem esticar e sem cortar entre a entrada e o golpe; só deslocada (tempo da música = '
                                'tempo do episódio + 3,344 s), com entrada de 1,0 s e volume')}

# ---------------- efeitos ----------------
fx = np.zeros((N, 2))
ganho_ambiente_corte = None


def montar_evento(e):
    src = ler(e['arquivo'], 2)
    seg = src[int(round(e['de'] * SR)):int(round(e['ate'] * SR))].copy()
    en, h = env_db(seg, 1)
    if e['ancora'] == 'transiente':
        b0, b1 = int((e['busca'][0] - e['de']) * 1000), int((e['busca'][1] - e['de']) * 1000)
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
    if 'rms_alvo_db' in e:
        medido = 20 * np.log10(np.sqrt((seg[int(0.1 * SR):-ns or None] ** 2).mean()) + 1e-12)
        ganho = e['rms_alvo_db'] - medido
        ref = f"RMS {medido:.1f} dBFS -> {e['rms_alvo_db']:.1f}"
    else:
        medido = en.max()
        ganho = e['pico_alvo_db'] - medido
        ref = f"pico 1 ms {medido:.1f} dBFS -> {e['pico_alvo_db']:.1f}"
    seg *= 10 ** (ganho / 20)
    return src, seg, anc, ganho, ref


for e in PLANO['efeitos']:
    src, seg, anc, ganho, ref = montar_evento(e)
    rel = (e['no_corte'] if 'no_corte' in e else e['no_ep']) - anc
    i = posicao(e, rel)
    colocar(fx, seg, i)
    if e['arquivo'].startswith('ambiente') and 'no_corte' in e:
        ganho_ambiente_corte = ganho
    no_ep = BASE_CORTE + e['no_corte'] if 'no_corte' in e else e['no_ep']
    doc['eventos'].append({'nome': e['nome'], 'arquivo': 'assets/audio/fontes/' + e['arquivo'],
                           'origem': 'corte de 10 s (sem mudança)' if 'no_corte' in e else 'novo (cenas 1 a 5)',
                           'trecho_do_arquivo_s': [e['de'], e['ate']], 'ancora': e['ancora'],
                           'ancora_no_arquivo_s': round(e['de'] + anc, 3), 'no_episodio_s': round(no_ep, 3),
                           'toca_no_episodio_s': [round(i / SR, 3), round((i + len(seg)) / SR, 3)],
                           'ganho_db': round(ganho, 1), 'referencia_do_ganho': ref,
                           **({'obs': e['obs']} if 'obs' in e else {})})
    print(f"{e['nome']:<52} {e['arquivo']:<24} âncora {e['de'] + anc:6.3f} s -> {no_ep:6.3f} s, ganho {ganho:+5.1f} dB")

# leito de ambiente de 0 a 25,3 s: a mesma tomada do corte, com o mesmo ganho, repetida com cruzamentos de 0,5 s.
# Em cada emenda, o começo da cópia seguinte é escolhido onde ele mais se parece com o fim da anterior (correlação),
# para o zumbido não "bater" no cruzamento.
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
    ultima = pos + len(pedaco) >= fim_leito          # esta cópia já chega ao fim do leito: sem cruzamento de saída
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
leito *= 10 ** (ganho_ambiente_corte / 20)
colocar(fx, leito, 0)
doc['leito_ambiente'] = {'nome': pl['nome'], 'arquivo': 'assets/audio/fontes/' + pl['arquivo'],
                         'toca_no_episodio_s': [0.0, round(fim_leito / SR, 3)],
                         'saida': f"{pl['saida_s'] * 1000:.0f} ms (25,30-25,34 s), por baixo da entrada do ambiente do corte",
                         'copias': copias, 'cruzamento_s': pl['cruzamento_s'], 'emendas_no_episodio_s': emendas,
                         'cada_copia_seguinte_comeca_no_arquivo_s': round(melhor / SR, 3),
                         'semelhanca_na_emenda_0a1': round(melhor_c, 2),
                         'ganho_db': round(ganho_ambiente_corte, 1),
                         'por_que_repetir': ('a tomada b é estável (nenhum estalo 15 dB acima do resto; o espectro do '
                                             'começo, do meio e do fim difere menos de 2 dB por faixa), então dá para '
                                             'repetir sem gerar uma nova; é o mesmo som que o corte usa a partir de 25,3 s')}
print(f"leito de ambiente: {copias} cópias, emendas em {emendas} s, cópias seguintes começam em "
      f"{melhor / SR:.3f} s do arquivo (semelhança {melhor_c:.2f}), ganho {ganho_ambiente_corte:+.1f} dB")

# ---------------- soma, ganho fixo final e limitador só no impacto ----------------
mix = voz + mus + fx
pf = PLANO['final']
j0 = I0 + int(pf['janela_impacto_corte'][0] * SR)
j1 = I0 + int(pf['janela_impacto_corte'][1] * SR)
# O ganho fixo final é o MESMO do corte de 10 s: calculado com a mesma conta do montar-corte10s.py, sobre o trecho
# do corte (que aqui é idêntico). Assim o trecho de 25,3 s em diante sai com o mesmo volume do corte aprovado.
cp = mix[I0:I0 + N_CORTE]
j0c, j1c = int(pf['janela_impacto_corte'][0] * SR), int(pf['janela_impacto_corte'][1] * SR)
g_lufs_c = pf['alvo_lufs'] - medidor.integrated_loudness(cp)
g_fora_c = pf['teto_dbtp'] - pico_real_db(np.vstack([cp[:j0c], cp[j1c:]]))
g_imp_c = pf['teto_dbtp'] - pico_real_db(cp[j0c:j1c]) + pf['limitador_max_db']
ganho_final = min(g_lufs_c, g_fora_c, g_imp_c)
quem = {g_lufs_c: 'alvo de -14 LUFS (no corte)', g_fora_c: 'pico real da voz do corte ("cada linha...")',
        g_imp_c: 'golpe do impacto (limitador no máximo permitido)'}[ganho_final]
# conferência: com esse ganho, nada antes de 25,3 s pode passar do teto (a voz não pode ser limitada)
antes = mix[:I0] * 10 ** (ganho_final / 20)
os_antes = np.abs(resample_poly(antes, 4, 1, axis=0)).max(1)
p_antes = 20 * np.log10(os_antes.max() + 1e-12)
if p_antes > pf['teto_dbtp'] + 0.01:
    raise SystemExit(f'pico real {p_antes:.2f} dBTP em {np.argmax(os_antes) / 4 / SR:.3f} s passa do teto '
                     f'{pf["teto_dbtp"]} dBTP: baixe o ganho_db dessa fala (ou do efeito) no PLANO')
l0 = medidor.integrated_loudness(mix)
g_lufs = pf['alvo_lufs'] - l0
mix *= 10 ** (ganho_final / 20)

teto = 10 ** (pf['teto_dbtp'] / 20)
os4 = np.abs(resample_poly(mix, 4, 1, axis=0)).max(1)
pico_amostra = os4[:len(os4) // 4 * 4].reshape(-1, 4).max(1)
pico_amostra = np.r_[pico_amostra, np.zeros(N - len(pico_amostra))][:N]
g = np.ones(N)
g[j0:j1] = np.minimum(1.0, teto / (pico_amostra[j0:j1] + 1e-12))
olhar = int(0.0015 * SR)
g = minimum_filter1d(g, size=2 * olhar + 1, mode='nearest')
solta = np.exp(-1.0 / (0.060 * SR))
for i in range(j0, min(j1 + int(0.3 * SR), N)):
    g[i] = min(g[i], 1 - (1 - g[i - 1]) * solta) if i > 0 else g[i]
g[:j0 - olhar] = 1.0
g[min(j1 + int(0.3 * SR), N):] = 1.0
age = np.nonzero(g < 0.99999)[0]
janela_efetiva = [round(age[0] / SR, 3), round(age[-1] / SR, 3)] if len(age) else []
reducao_max = -20 * np.log10(g.min())
mix *= g[:, None]

nf = int(pf['fade_fim_s'] * SR)
mix[-nf:] *= rampa(nf, 1, 0)[:, None] ** 2
mix = mix[:N]
saida = os.path.join(AUDIO, 'mix-corte-ampliado.wav')
sf.write(saida, mix.astype(np.float32), SR, subtype='PCM_24')


# ---------------- medições do arquivo final (ffmpeg ebur128 = medidor padrão) ----------------
def ebur128(caminho):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', caminho, '-af', 'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1])


lufs_i, tp = ebur128(saida)
info = sf.info(saida)
gf = 10 ** (ganho_final / 20)
vz, mz, fz = voz * gf, mus * gf, fx * gf
falando = np.zeros(N, bool)
for f in pv['falas']:
    r = f['_real']
    ii, jj = int(r['comeca'] * SR), int(r['termina'] * SR)
    falando[ii:jj] = True
    lu = medidor.integrated_loudness(vz[ii:jj]) if jj - ii > 0.4 * SR else float('nan')
    doc['falas'].append({'texto': f['texto'], 'alvo_s': f['alvo'], 'comeca_s': round(r['comeca'], 3),
                         'termina_s': round(r['termina'], 3), 'deslizou_s': round(r['comeca'] - f['alvo'], 3),
                         'trecho_da_tomada_s': [f['de'], f['ate']],
                         'fala_na_tomada_s': [round(r['fala_arq'][0], 3), round(r['fala_arq'][1], 3)],
                         'clip_no_episodio_s': [round(r['clip'][0], 3), round(r['clip'][1], 3)],
                         'ganho_db': f['ganho_db'], 'ganho_total_db': round(f['ganho_db'] + ganho_final, 2),
                         'lufs': round(lu, 1), 'pico_real_dbtp': round(pico_real_db(vz[ii:jj]), 2),
                         **({'obs': f['obs']} if 'obs' in f else {}),
                         **({'origem': 'corte de 10 s (sem mudança)'} if f.get('do_corte') else {})})
idx = np.nonzero(falando)[0]
lufs_voz = medidor.integrated_loudness(vz[idx])
lufs_mus_sob = medidor.integrated_loudness(mz[idx])
lufs_fx_sob = medidor.integrated_loudness(fz[idx])
ef, hf = env_db(mix, 1)
k0, k1 = int((GOLPE_EP - 0.083) * 1000), int((GOLPE_EP + 0.267) * 1000)
golpe_real = (k0 + int(np.argmax(ef[k0:k1] >= ef[k0:k1].max() - 12))) * hf / SR
# pico (1 ms) de cada efeito novo no arquivo final
for ev_ in doc['eventos']:
    ev_['ganho_total_db'] = round(ev_['ganho_db'] + ganho_final, 1)
# volume da trilha (sozinha, depois do ganho final) em cada frase do piano: tem de subir aos poucos até o golpe
trilha_por_frase = {}
for a_, b_ in pt['frases_do_piano'] + [[28.8, 30.0], [30.0, 31.5], [31.5, GOLPE_EP], [GOLPE_EP, DUR]]:
    trilha_por_frase[f'{a_:g}-{b_:g}'] = round(float(medidor.integrated_loudness(mz[int(a_ * SR):int(b_ * SR)])), 1)

# teste de subtração: o trecho de 25,3 s em diante contra o corte de 10 s aprovado
corte, sr_c = sf.read(os.path.join(AUDIO, 'mix-corte10s.wav'), dtype='float64')
novo = sf.read(saida, dtype='float64')[0][I0:I0 + N_CORTE]
dif = novo - corte[:len(novo)]


def nivel(x):
    return round(float(20 * np.log10(np.sqrt((x ** 2).mean()) + 1e-15)), 1)


k_amb = int(0.040 * SR)
subtracao = {'nivel_do_corte_dbfs': nivel(corte),
             'diferenca_25_30_a_25_34_dbfs': nivel(dif[:k_amb]),
             'diferenca_de_25_34_ao_fim_dbfs': nivel(dif[k_amb:]),
             'maior_diferenca_de_25_34_ao_fim_dbfs': round(float(20 * np.log10(np.abs(dif[k_amb:]).max() + 1e-15)), 1),
             'leitura': ('de 25,34 s até o fim a diferença é zero (amostra por amostra, é o mesmo arquivo do corte '
                         'aprovado); nos 40 ms de 25,30 a 25,34 s sobra só a saída do leito de ambiente e os 5 ms de '
                         'entrada que o corte fazia na trilha (aqui a trilha já vinha tocando)')}

doc['final'] = {'arquivo': 'assets/audio/mix-corte-ampliado.wav', 'duracao_s': round(info.frames / SR, 4),
                'formato': 'WAV PCM 24 bits', 'amostras': info.frames, 'amostragem_hz': info.samplerate,
                'canais': info.channels, 'ganho_fixo_final_db': round(ganho_final, 2), 'ganho_limitado_por': quem,
                'ganho_que_daria_-14_lufs_db': round(g_lufs, 2),
                'limitador': {'janela_s': [round(j0 / SR, 3), round(j1 / SR, 3)], 'agiu_de_ate_s': janela_efetiva,
                              'reducao_maxima_db': round(reducao_max, 2), 'teto_dbtp': pf['teto_dbtp']},
                'fade_fim_s': pf['fade_fim_s'],
                'medicoes': {'lufs_integrado': lufs_i, 'pico_real_dbtp': tp,
                             'golpe_no_episodio_s': round(golpe_real, 3),
                             'voz_lufs_nas_falas': round(lufs_voz, 1),
                             'trilha_lufs_sob_a_voz': round(lufs_mus_sob, 1),
                             'efeitos_lufs_sob_a_voz': round(lufs_fx_sob, 1),
                             'voz_acima_da_trilha_db': round(lufs_voz - lufs_mus_sob, 1),
                             'trilha_sozinha_lufs_por_frase_do_piano': trilha_por_frase},
                'teste_de_subtracao_contra_o_corte_de_10s': subtracao}
doc['_ganhos'] = ('ganho_db = ganho próprio da fala/evento (antes do ganho fixo final); ganho_total_db = ganho_db + '
                  'ganho fixo final, ou seja, quanto o arquivo de origem foi aumentado/abaixado no mix final.')
for f in pv['falas']:
    f.pop('_real', None)
with open(os.path.join(AUDIO, 'audio-corte-ampliado.json'), 'w', encoding='utf-8') as fo:
    json.dump(doc, fo, ensure_ascii=False, indent=1)

print(f'\nganho fixo final {ganho_final:+.2f} dB (limitado por: {quem}); para -14 LUFS seria {g_lufs:+.2f} dB')
print(f'limitador no impacto: {reducao_max:.2f} dB, agiu de {janela_efetiva} s')
print(f'FINAL: {lufs_i:.1f} LUFS, pico real {tp:.1f} dBTP, {info.frames / SR:.4f} s, {info.samplerate} Hz, {info.channels} canais')
for fl in doc['falas']:
    print(f"  {fl['comeca_s']:6.3f}-{fl['termina_s']:6.3f} s (alvo {fl['alvo_s']:5.2f}, deslizou {fl['deslizou_s']:+.3f}) "
          f"{fl['lufs']:6.1f} LUFS, pico {fl['pico_real_dbtp']:6.2f} dBTP  {fl['texto']}")
print(f'voz {lufs_voz:.1f} LUFS; trilha sob a voz {lufs_mus_sob:.1f} LUFS ({lufs_voz - lufs_mus_sob:.1f} dB abaixo); '
      f'efeitos sob a voz {lufs_fx_sob:.1f} LUFS')
print('trilha sozinha, LUFS por frase do piano:', trilha_por_frase)
print(f'golpe no arquivo final: {golpe_real:.3f} s (alvo {GOLPE_EP:.3f})')
print('subtração contra o corte de 10 s:', subtracao)
print('->', saida)
