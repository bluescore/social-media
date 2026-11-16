"""Monta o áudio do corte de 10 s (a "virada", na variante com a dobra uma batida depois) num arquivo só.

Regras que este script segue (regras do dono e do SPEC):
  - a voz NUNCA é esticada, acelerada, emendada nem passa por limitador: só é recortada no meio das pausas;
  - a trilha NUNCA é esticada nem cortada entre a entrada e o golpe: ela é só deslocada para o golpe cair
    em 8,033 s do corte (quadro 241 a 30 fps) e tem o volume ajustado (automação de volume);
  - um ganho fixo final (o mesmo do começo ao fim) leva o volume perto de -14 LUFS sem o pico real passar de -1 dBTP;
  - o limitador só age na janela do impacto (perto de 8,033 s), nunca sobre a voz;
  - fade de 0,25 s só no fim; os efeitos têm só entradas/saídas curtas para não estalar.

Para mudar alguma coisa, mexa no PLANO abaixo e rode de novo:
    python -I fonte/audio/montar-corte10s.py
Entradas: assets/audio/fontes/*.mp3 (tudo baixado do ElevenLabs)
Saídas:   assets/audio/mix-corte10s.wav (48 kHz, estéreo, 10,833 s)
          assets/audio/audio-corte10s.json (cada evento: arquivo, tempo no corte, ganho; medições)
          assets/audio/dobra-1.wav, dobra-2.wav, dobra-3.wav (os 3 sons fixos de dobra da série, já recortados)
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
DUR = 10.833                      # 325 quadros a 30 fps
N = int(round(DUR * SR))
GOLPE_CORTE = 8.033               # quadro 241 do corte (= episódio 33,333 s, quadro 1000)

# ----------------------------------------------------------------------------------------------------------------
# PLANO
# tempos "no_corte" em segundos do corte; "ancora" diz QUE ponto do arquivo cai nesse tempo:
#   inicio      = onde o som começa (primeiro ponto a 30 dB do pico do trecho usado)
#   transiente  = o estalo principal (primeiro ponto a 6 dB do pico dentro de "busca", em segundos do arquivo)
#   fim         = o fim do trecho usado
# "de"/"ate" = trecho do arquivo usado (recorte); "pico_alvo_db" = pico (em janelas de 1 ms) antes do ganho final;
# o ganho em dB de cada evento é calculado a partir dele e fica anotado no audio-corte10s.json.
# ----------------------------------------------------------------------------------------------------------------
PLANO = {
    'voz': {
        'arquivo': 'narracao-amedeiros-v4-a.mp3', 'texto': 'cada linha que ela escreveu virou uma cena.',
        'de': 17.090, 'ate': 19.775,            # no meio das pausas (395 ms antes e 370 ms depois da fala)
        'fala_comeca_no_arquivo': 17.290,       # primeiro som da fala (medido em janelas de 2 ms, limiar -50 dBFS)
        'fala_comeca_no_corte': 1.000,
        'ganho_db': -7.6,
    },
    'trilha': {
        'arquivo': 'trilha-tema-b.mp3',
        'golpe_no_arquivo': 36.677,             # ataque do golpe (medido com 1 ms; ver fonte/audio/golpes.json)
        # volume da trilha (fator) ao longo do corte; entre os pontos o volume muda em linha reta (em dB)
        'volume': [[0.0, 0.14], [3.50, 0.14], [8.000, 0.45], [DUR, 0.45]],
        # recorte de médias (1-4 kHz) na trilha enquanto a voz fala, para abrir espaço para ela
        'recorte_medias_db': -4.0, 'recorte_de': 0.80, 'recorte_ate': 3.50, 'recorte_rampa_s': 0.15,
        'por_que_esta': {
            'A': ('descartada: não tem um golpe só; a cada 8 batidas (~6,7 s) entra um acorde forte (7,5 · 14,5 · 21,0 · '
                  '27,75 · 34,47 s). O de 27,75 s não tem grave, e o grave forte de 21,0 s cairia em 1,3 s do corte, sob a voz.'),
            'B': ('escolhida: piano calmo, uma nota grave longa em 33,35 s (só grave, sem ataque no médio/agudo), quase '
                  'silêncio de 35,5 a 36,6 s e o golpe de banda inteira em 36,677 s (salta ~32 dB do silêncio ao cheio), '
                  'com a seção sustentada e o pulso até 64 s. É o golpe mais nítido das 3 e a única sem ataque forte sob a voz.'),
            'C': ('descartada para o corte: tem o crescendo e o riser chegando em 28,18 s, mas dois graves fortes antes '
                  '(8,25 s e 21,56 s); o de 21,56 s é o som mais forte da música e cairia em 1,4 s do corte, embaixo da voz.'),
        },
    },
    'efeitos': [
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
         'pico_alvo_db': -27.0, 'serie': 'dobra-1.wav'},
        {'nome': 'dobra de papel 2', 'arquivo': 'dobra-2-b.mp3', 'de': 0.26, 'ate': 0.680,
         'ancora': 'transiente', 'busca': [0.28, 0.36], 'no_corte': 6.733, 'entrada_s': 0.02, 'saida_s': 0.10,
         'pico_alvo_db': -27.0, 'serie': 'dobra-2.wav'},
        {'nome': 'dobra de papel 3 (giro)', 'arquivo': 'dobra-3-a.mp3', 'de': 0.40, 'ate': 0.680,
         'ancora': 'transiente', 'busca': [0.44, 0.52], 'no_corte': 7.633, 'entrada_s': 0.03, 'saida_s': 0.10,
         'pico_alvo_db': -27.0, 'serie': 'dobra-3.wav'},
        {'nome': 'riser (som que sobe até o golpe)', 'arquivo': 'riser-b.mp3', 'de': 0.47, 'ate': 2.0,
         'ancora': 'fim', 'no_corte': 8.013, 'entrada_s': 0.05, 'saida_s': 0.008, 'pico_alvo_db': -27.0},
        {'nome': 'impacto: grave + eco (reforço do golpe da trilha)', 'arquivo': 'impacto-a.mp3', 'de': 0.0,
         'ate': 3.0, 'ancora': 'inicio', 'no_corte': GOLPE_CORTE, 'entrada_s': 0.001, 'saida_s': 0.40,
         'pico_alvo_db': -23.0},
    ],
    'final': {
        'alvo_lufs': -14.0,
        'teto_dbtp': -1.2,                    # teto do pico real fora do impacto (um pouco abaixo de -1 por segurança)
        'janela_impacto': [8.013, 8.85],      # único trecho em que o limitador pode agir
        'limitador_max_db': 3.0,              # quanto o limitador pode achatar, no máximo, no golpe
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


medidor = pyln.Meter(SR)
doc = {'_sobre': ('Áudio do corte de 10 s do ep. 01 (sala de espera), a virada do episódio a partir de 25,3 s, na '
                  'variante com a dobra uma batida (0,833 s) depois do SPEC. Tempos em segundos do corte '
                  '(0 = 25,300 s do episódio; 8,033 = quadro 241 = episódio 33,333 s). Gerado por '
                  'fonte/audio/montar-corte10s.py; para mudar, edite o PLANO no script e rode de novo.'),
       'duracao_s': DUR, 'amostragem_hz': SR, 'canais': 2, 'eventos': []}

# ---------------- voz ----------------
pv = PLANO['voz']
voz_tomada = ler(pv['arquivo'], 1)[:, 0]
trecho = voz_tomada[int(round(pv['de'] * SR)):int(round(pv['ate'] * SR))].copy()
r = int(0.015 * SR)                                   # 15 ms de entrada/saída, dentro das pausas (silêncio)
trecho[:r] *= rampa(r, 0, 1)
trecho[-r:] *= rampa(r, 1, 0)
trecho *= 10 ** (pv['ganho_db'] / 20)
inicio_clip = pv['fala_comeca_no_corte'] - (pv['fala_comeca_no_arquivo'] - pv['de'])
voz = np.zeros(N)
colocar(voz, trecho, int(round(inicio_clip * SR)))
voz = np.c_[voz, voz]
ev, hop = env_db(voz, 2)
falando = np.nonzero(ev > -50 + pv['ganho_db'])[0]
fala_ini, fala_fim = falando[0] * hop / SR, (falando[-1] + 1) * hop / SR

# ---------------- trilha ----------------
pt = PLANO['trilha']
musica_inteira = ler(pt['arquivo'], 2)
desloc = pt['golpe_no_arquivo'] - GOLPE_CORTE           # segundo do arquivo que cai no 0 do corte
a = int(round(desloc * SR))
mus = musica_inteira[a:a + N].copy()
t = np.arange(N) / SR
pts = np.array(pt['volume'])
vol = 10 ** (np.interp(t, pts[:, 0], 20 * np.log10(pts[:, 1])) / 20)
# recorte de médias sob a voz: subtrai parte da faixa 1-4 kHz (filtro sem atraso de fase = corte limpo)
banda = sosfiltfilt(butter(2, [1000, 4000], 'bandpass', fs=SR, output='sos'), mus, axis=0)
rr = pt['recorte_rampa_s']
env_rec = np.interp(t, [pt['recorte_de'] - rr, pt['recorte_de'], pt['recorte_ate'], pt['recorte_ate'] + rr],
                    [0, 1, 1, 0], left=0, right=0)
mus = mus + banda * ((10 ** (pt['recorte_medias_db'] / 20) - 1) * env_rec)[:, None]
mus *= vol[:, None]
mus[:int(0.005 * SR)] *= rampa(int(0.005 * SR), 0, 1)[:, None]   # 5 ms só para não estalar no primeiro quadro

doc['voz'] = {'arquivo': 'assets/audio/fontes/' + pv['arquivo'], 'tomada': 'A (eleven_v4, 1ª de 2)',
              'texto': pv['texto'], 'trecho_da_tomada_s': [pv['de'], pv['ate']],
              'fala_na_tomada_s': [pv['fala_comeca_no_arquivo'], round(pv['fala_comeca_no_arquivo'] + fala_fim - fala_ini, 3)],
              'clip_no_corte_s': [round(inicio_clip, 3), round(inicio_clip + pv['ate'] - pv['de'], 3)],
              'fala_no_corte_s': [round(fala_ini, 3), round(fala_fim, 3)], 'ganho_db': pv['ganho_db'],
              'tratamento': 'nenhum (sem esticar, acelerar, emendar, comprimir ou limitar); 15 ms de entrada/saída na pausa'}
doc['trilha'] = {'arquivo': 'assets/audio/fontes/' + pt['arquivo'], 'candidata': 'B (2ª de 3)',
                 'golpe_no_arquivo_s': pt['golpe_no_arquivo'], 'golpe_no_corte_s': GOLPE_CORTE,
                 'deslocamento_s': round(desloc, 3),
                 'trecho_do_arquivo_s': [round(desloc, 3), round(desloc + DUR, 3)],
                 'volume_fator': pt['volume'],
                 'recorte_medias': {'faixa_hz': [1000, 4000], 'db': pt['recorte_medias_db'],
                                    'de_s': pt['recorte_de'], 'ate_s': pt['recorte_ate']},
                 'tratamento': 'sem esticar e sem cortar entre a entrada e o golpe; só deslocada e com volume',
                 'candidatas': pt['por_que_esta']}

# ---------------- efeitos ----------------
fx = np.zeros((N, 2))
for e in PLANO['efeitos']:
    src = ler(e['arquivo'], 2)
    seg = src[int(round(e['de'] * SR)):int(round(e['ate'] * SR))].copy()
    en, h = env_db(seg, 1)
    if e['ancora'] == 'transiente':
        b0, b1 = int((e['busca'][0] - e['de']) * 1000), int((e['busca'][1] - e['de']) * 1000)
        k = b0 + int(np.argmax(en[b0:b1] >= en[b0:b1].max() - 6))
        anc = k * h / SR
    elif e['ancora'] == 'inicio':
        anc = int(np.argmax(en >= en.max() - 30)) * h / SR
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
    inicio = e['no_corte'] - anc
    colocar(fx, seg, int(round(inicio * SR)))
    if 'serie' in e:   # som fixo da série: guarda o recorte (sem ganho do corte, normalizado a -3 dBFS de pico)
        cru = src[int(round(e['de'] * SR)):int(round(e['ate'] * SR))].copy()
        cru[:ne] *= rampa(ne, 0, 1)[:, None]
        cru[len(cru) - ns:] *= rampa(ns, 1, 0)[:, None]
        cru *= 10 ** ((-3 - 20 * np.log10(np.abs(cru).max())) / 20)
        sf.write(os.path.join(AUDIO, e['serie']), cru.astype(np.float32), SR, subtype='PCM_24')
    doc['eventos'].append({'nome': e['nome'], 'arquivo': 'assets/audio/fontes/' + e['arquivo'],
                           'trecho_do_arquivo_s': [e['de'], e['ate']], 'ancora': e['ancora'],
                           'ancora_no_arquivo_s': round(e['de'] + anc, 3), 'no_corte_s': e['no_corte'],
                           'toca_no_corte_s': [round(inicio, 3), round(inicio + len(seg) / SR, 3)],
                           'ganho_db': round(ganho, 1), 'referencia_do_ganho': ref,
                           **({'arquivo_fixo_da_serie': 'assets/audio/' + e['serie']} if 'serie' in e else {})})
    print(f"{e['nome']:<50} {e['arquivo']:<24} âncora {e['de'] + anc:6.3f} s -> {e['no_corte']:6.3f} s do corte, "
          f"ganho {ganho:+5.1f} dB")

# ---------------- soma, ganho fixo final e limitador só no impacto ----------------
mix = voz + mus + fx
pf = PLANO['final']
j0, j1 = int(pf['janela_impacto'][0] * SR), int(pf['janela_impacto'][1] * SR)
fora = np.vstack([mix[:j0], mix[j1:]])
p_fora, p_imp = pico_real_db(fora), pico_real_db(mix[j0:j1])
l0 = medidor.integrated_loudness(mix)
g_lufs = pf['alvo_lufs'] - l0
g_fora = pf['teto_dbtp'] - p_fora
g_imp = pf['teto_dbtp'] - p_imp + pf['limitador_max_db']
ganho_final = min(g_lufs, g_fora, g_imp)
quem = {g_lufs: 'alvo de -14 LUFS', g_fora: 'pico real fora do impacto (voz/trilha intactas)',
        g_imp: 'golpe do impacto (limitador no máximo permitido)'}[ganho_final]
mix *= 10 ** (ganho_final / 20)

# limitador de pico real (sobreamostragem 4x, olhar à frente de 1,5 ms, soltura de 60 ms), SÓ dentro da janela
teto = 10 ** (pf['teto_dbtp'] / 20)
os4 = np.abs(resample_poly(mix, 4, 1, axis=0)).max(1)
pico_amostra = os4[:len(os4) // 4 * 4].reshape(-1, 4).max(1)
pico_amostra = np.r_[pico_amostra, np.zeros(N - len(pico_amostra))][:N]
g = np.ones(N)
g[j0:j1] = np.minimum(1.0, teto / (pico_amostra[j0:j1] + 1e-12))
olhar = int(0.0015 * SR)
# mínimo deslizante (olha 1,5 ms à frente e atrás), para o ganho já estar baixo quando o pico chega
g = minimum_filter1d(g, size=2 * olhar + 1, mode='nearest')
solta = np.exp(-1.0 / (0.060 * SR))
for i in range(j0, min(j1 + int(0.3 * SR), N)):
    g[i] = min(g[i], 1 - (1 - g[i - 1]) * solta) if i > 0 else g[i]
g[:j0 - olhar] = 1.0
g[min(j1 + int(0.3 * SR), N):] = 1.0
age = np.nonzero(g < 0.99999)[0]
janela_efetiva = [round(age[0] / SR, 3), round(age[-1] / SR, 3)] if len(age) else []
reducao_max = -20 * np.log10(g.min())
perfil_reducao = {f'{k / 10:.1f}': round(float(-20 * np.log10(g[int(k / 10 * SR):int((k + 1) / 10 * SR)].min())), 2)
                  for k in range(int(pf['janela_impacto'][0] * 10), int(pf['janela_impacto'][1] * 10) + 4)}
mix *= g[:, None]

# fade de 0,25 s só no fim
nf = int(pf['fade_fim_s'] * SR)
mix[-nf:] *= rampa(nf, 1, 0)[:, None] ** 2
mix = mix[:N]
saida = os.path.join(AUDIO, 'mix-corte10s.wav')
sf.write(saida, mix.astype(np.float32), SR, subtype='PCM_24')


# ---------------- medições do arquivo final (ffmpeg ebur128 = medidor padrão) ----------------
def ebur128(caminho):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', caminho, '-af', 'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1])


lufs_i, tp = ebur128(saida)
info = sf.info(saida)
vz = voz * 10 ** (ganho_final / 20)
ii, jj = int(fala_ini * SR), int(fala_fim * SR)
lufs_voz = medidor.integrated_loudness(vz[ii:jj])
lufs_mus_sob = medidor.integrated_loudness((mus * 10 ** (ganho_final / 20))[ii:jj])
lufs_fx_sob = medidor.integrated_loudness((fx * 10 ** (ganho_final / 20))[ii:jj])
tp_voz = pico_real_db(vz)
# onde o golpe caiu de fato no arquivo final (ataque: 1 ms, primeiro ponto a 12 dB do pico entre 7,9 e 8,3 s)
ef, hf = env_db(mix, 1)
k0, k1 = int(7.95 * 1000), int(8.30 * 1000)
golpe_real = (k0 + int(np.argmax(ef[k0:k1] >= ef[k0:k1].max() - 12))) * hf / SR
doc['final'] = {'arquivo': 'assets/audio/mix-corte10s.wav', 'duracao_s': round(info.frames / SR, 4), 'formato': 'WAV PCM 24 bits',
                'amostras': info.frames, 'amostragem_hz': info.samplerate, 'canais': info.channels,
                'ganho_fixo_final_db': round(ganho_final, 2), 'ganho_limitado_por': quem,
                'limitador': {'janela_s': pf['janela_impacto'], 'agiu_de_ate_s': janela_efetiva,
                              'reducao_maxima_db': round(reducao_max, 2),
                              'reducao_por_decimo_de_segundo_db': perfil_reducao,
                              'teto_dbtp': pf['teto_dbtp']},
                'fade_fim_s': pf['fade_fim_s'],
                'medicoes': {'lufs_integrado': lufs_i, 'pico_real_dbtp': tp,
                             'golpe_no_corte_s': round(golpe_real, 3), 'fala_no_corte_s': [round(fala_ini, 3), round(fala_fim, 3)],
                             'voz_lufs_na_fala': round(lufs_voz, 1), 'voz_pico_real_dbtp': round(tp_voz, 2),
                             'trilha_lufs_sob_a_voz': round(lufs_mus_sob, 1),
                             'efeitos_lufs_sob_a_voz': round(lufs_fx_sob, 1),
                             'voz_acima_da_trilha_db': round(lufs_voz - lufs_mus_sob, 1)}}
for ev_ in doc['eventos']:
    ev_['ganho_total_db'] = round(ev_['ganho_db'] + ganho_final, 1)
doc['voz']['ganho_total_db'] = round(pv['ganho_db'] + ganho_final, 2)
doc['trilha']['ganho_total_db_sobre_o_fator'] = round(ganho_final, 2)
doc['_ganhos'] = ('ganho_db = ganho próprio do evento (antes do ganho fixo final); ganho_total_db = ganho_db + ganho fixo '
                  'final, ou seja, quanto o arquivo de origem foi aumentado/abaixado no mix final.')
with open(os.path.join(AUDIO, 'audio-corte10s.json'), 'w', encoding='utf-8') as f:
    json.dump(doc, f, ensure_ascii=False, indent=1)
print(f'\nganho fixo final {ganho_final:+.2f} dB (limitado por: {quem}); limitador no impacto: {reducao_max:.2f} dB, agiu de {janela_efetiva} s')
print('limitador, redução máxima por 0,1 s (dB):', perfil_reducao)
print(f'FINAL: {lufs_i:.1f} LUFS, pico real {tp:.1f} dBTP, {info.frames / SR:.4f} s, {info.samplerate} Hz, {info.channels} canais')
print(f'voz: fala de {fala_ini:.3f} a {fala_fim:.3f} s, {lufs_voz:.1f} LUFS, pico real {tp_voz:.1f} dBTP; '
      f'trilha sob a voz {lufs_mus_sob:.1f} LUFS ({lufs_voz - lufs_mus_sob:.1f} dB abaixo); efeitos sob a voz {lufs_fx_sob:.1f} LUFS')
print(f'golpe no arquivo final: {golpe_real:.3f} s (alvo {GOLPE_CORTE})')
print('->', saida)
