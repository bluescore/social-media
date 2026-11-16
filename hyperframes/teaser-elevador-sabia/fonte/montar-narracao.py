"""Encaixa a narração (voz clonada "Yago-Voice", Higgsfield) no teaser.

A voz NÃO é esticada, acelerada, emendada no meio de frase nem passa por limitador (regra do dono).
O que o script faz:
  1. recorta cada fala da tomada inteira nas pausas (com 15 ms de entrada/saída suave para não estalar);
  2. coloca cada fala no tempo do filme definido em fonte/narracao.json;
  3. ajusta o volume da voz com um ganho fixo (alvo em LUFS) e um ganho fixo próprio por fala ("ganho_db"):
     as primeiras falas mais baixas, para o filme continuar começando leve;
  4. abaixa a música só enquanto a voz fala, o suficiente para a voz ficar ~8 dB acima dela; na fala que vem
     depois do impacto ("abaixar_fixo_db") a música desce uma profundidade fixa, em rampa, sem cortar o eco.

Entrada: fonte/narracao.json, a tomada indicada nele e assets/audio/trilha3.mp3
Saída:   assets/audio/narracao.wav (17 s, a voz já no lugar) e assets/audio/trilha3-narrada.wav (música abaixada)
Uso: python -I fonte/montar-narracao.py
"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf
from scipy.ndimage import maximum_filter1d, uniform_filter1d

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(AQUI)
SR = 48000
DUR = 17.0
cfg = json.load(open(os.path.join(AQUI, 'narracao.json'), encoding='utf-8'))


def ler(caminho, canais):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', caminho, '-ac', str(canais), '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, canais).astype(np.float64)


def lufs(x):
    """Loudness integrado (aprox. BS.1770, sem gate relativo) — bom para comparar trechos de fala."""
    from scipy.signal import lfilter
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1, -1.99004745483398, 0.99007225036621]
    y = lfilter(b2, a2, lfilter(b1, a1, x, axis=0), axis=0)
    z = (y ** 2).mean(0).sum()
    return -0.691 + 10 * np.log10(z + 1e-12)


voz_take = ler(os.path.join(PECA, cfg['tomada']), 1)[:, 0]
N = int(DUR * SR)
t = np.arange(N) / SR
falas = []
for f in cfg['falas']:
    a, b = int(f['de'] * SR), int(f['ate'] * SR)
    trecho = voz_take[a:b].copy()
    r = int(0.015 * SR)
    trecho[:r] *= np.linspace(0, 1, r)
    trecho[-r:] *= np.linspace(1, 0, r)
    i = int(f['no_filme'] * SR)
    sinal = np.zeros(N)
    sinal[i:i + len(trecho)] = trecho[:N - i]
    falas.append({**f, 'sinal': sinal, 'i': i, 'j': min(i + len(trecho), N)})
    print(f"{f['texto']:<34} {f['de']:6.3f}–{f['ate']:6.3f} s da tomada  ->  {f['no_filme']:6.3f}–{f['no_filme'] + (b - a) / SR:6.3f} s do filme")

# 3) ganho fixo da voz inteira (medido só na fala) + um ganho fixo próprio de cada fala (ganho_db).
#    Cada fala continua intacta: o ganho é o mesmo do começo ao fim dela (não é compressão nem limitador).
soma = sum(f['sinal'] for f in falas)
ativo = np.zeros(N)
for f in falas:
    ativo[f['i']:f['j']] = 1
g_voz = cfg.get('voz_lufs', -20.0) - lufs(soma[ativo > 0][:, None])
voz = np.zeros(N)
for f in falas:
    f['sinal'] *= 10 ** ((g_voz + f.get('ganho_db', 0.0)) / 20)
    voz += f['sinal']
print(f'voz: ganho fixo {g_voz:+.1f} dB (+ ganho por fala), pico {20 * np.log10(np.abs(voz).max()):.1f} dBFS')

# 4) música abaixada sob a voz
mus = ler(os.path.join(PECA, 'assets', 'audio', 'trilha3.mp3'), 2)[:N]
mus = np.vstack([mus, np.zeros((N - len(mus), 2))]) if len(mus) < N else mus
jan = int(0.4 * SR)
nivel_mus = 10 * np.log10(uniform_filter1d((mus ** 2).mean(1), jan) + 1e-12)
folga = cfg.get('voz_acima_da_musica_db', 8.0)
reducao = np.zeros(N)
for f in falas:
    if 'abaixar_fixo_db' in f:
        # profundidade fixa, descendo e subindo em rampas suaves (sem "bombear" a cauda do impacto)
        desce, solta = f.get('desce_s', 0.2), f.get('solta_s', 0.4)
        ini, fim = f['i'] / SR, f['j'] / SR
        env = np.interp(t, [ini - desce, ini, fim, fim + solta], [0, 1, 1, 0], left=0, right=0)
        reducao = np.minimum(reducao, f['abaixar_fixo_db'] * env)
        continue
    nivel_f = 10 * np.log10((f['sinal'][f['i']:f['j']] ** 2).mean() + 1e-12)
    zona = np.zeros(N)
    zona[max(f['i'] - int(0.25 * SR), 0):min(f['j'] + int(0.25 * SR), N)] = 1
    r_f = np.minimum(0.0, (nivel_f - folga) - nivel_mus)  # só abaixa, nunca sobe
    r_f = np.maximum(r_f, -cfg.get('reducao_max_db', 9.0)) * zona
    r_f = uniform_filter1d(uniform_filter1d(r_f, int(0.12 * SR)), int(0.12 * SR))  # sem degraus
    reducao = np.minimum(reducao, r_f)
# o golpe do impacto da data nunca é abaixado
imp = cfg.get('impacto_s', 14.833)
reducao[(t > imp - 0.05) & (t < imp + 0.2)] = 0.0
reducao = uniform_filter1d(reducao, int(0.03 * SR))
mus_d = mus * (10 ** (reducao / 20))[:, None]
print(f'música: abaixada no máximo {reducao.min():.1f} dB enquanto a voz fala')

sf.write(os.path.join(PECA, 'assets', 'audio', 'narracao.wav'), voz.astype(np.float32), SR, subtype='FLOAT')
sf.write(os.path.join(PECA, 'assets', 'audio', 'trilha3-narrada.wav'), mus_d.astype(np.float32), SR, subtype='FLOAT')
print('-> assets/audio/narracao.wav e assets/audio/trilha3-narrada.wav')
