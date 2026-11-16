"""Mede as 2 tomadas de cada efeito para escolher a melhor (sem ouvir, só por números).

O que se mede em cada arquivo:
  - pico (dBFS) e onde o som começa (primeiro ponto a -30 dB do pico);
  - "duração útil": quanto tempo o som fica a menos de 20 dB do pico (toque seco = curto);
  - quantos golpes separados ele tem (para um toque, o ideal é 1);
  - "tom" (0 a 1): quanto o som parece uma nota musical (autocorrelação); toque seco = baixo;
  - brilho (centroide, em Hz) e quanto da energia está no grave (abaixo de 150 Hz);
  - riser: se o volume sobe do começo ao fim (correlação 0 a 1) e se termina no ponto mais alto;
  - ambiente: volume médio e quanto ele oscila (ambiente bom = baixo e estável).

Uso:   python -I fonte/audio/medir-efeitos.py
Saída: fonte/audio/efeitos-medidas.json e a tabela no terminal.
"""
import glob
import json
import os
import subprocess

import numpy as np
from scipy.signal import butter, sosfiltfilt

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(os.path.dirname(AQUI))
FONTES = os.path.join(PECA, 'assets', 'audio', 'fontes')
SR = 48000


def ler(c):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', c, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def env_db(x, ms=5):
    hop = int(SR * ms / 1000)
    n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)), ms / 1000


def tonalidade(y):
    """maior pico de autocorrelação normalizada entre 60 e 1000 Hz, em janelas de 40 ms (média das 5 mais fortes)"""
    w = int(0.04 * SR)
    vals = []
    for i in range(0, len(y) - w, w // 2):
        s = y[i:i + w] - y[i:i + w].mean()
        if np.sqrt((s ** 2).mean()) < 1e-4:
            continue
        ac = np.correlate(s, s, 'full')[w - 1:]
        ac /= ac[0] + 1e-12
        vals.append(ac[SR // 1000:SR // 60].max())
    return float(np.mean(sorted(vals)[-5:])) if vals else 0.0


res = {}
for c in sorted(glob.glob(os.path.join(FONTES, '*.mp3'))):
    nome = os.path.basename(c)
    if nome.startswith(('narracao', 'trilha')):
        continue
    x = ler(c)
    e, dt = env_db(x)
    pk = e.max()
    ini = int(np.argmax(e > pk - 30)) * dt
    util = float((e > pk - 20).sum() * dt)
    # golpes separados: máximos locais a menos de 10 dB do pico, afastados > 80 ms
    idx = [i for i in range(1, len(e) - 1) if e[i] >= e[i - 1] and e[i] >= e[i + 1] and e[i] > pk - 10]
    golpes = []
    for i in idx:
        if not golpes or (i - golpes[-1]) * dt > 0.08:
            golpes.append(i)
    principal = x[int(max(ini - 0.01, 0) * SR):int((ini + max(util, 0.05) + 0.05) * SR)]
    spec = np.abs(np.fft.rfft(principal * np.hanning(len(principal))))
    fr = np.fft.rfftfreq(len(principal), 1 / SR)
    centroide = float((spec * fr).sum() / (spec.sum() + 1e-12))
    grave = float((spec[fr < 150] ** 2).sum() / ((spec ** 2).sum() + 1e-12))
    m = {'pico_dbfs': round(float(20 * np.log10(np.abs(x).max() + 1e-12)), 1), 'comeca_s': round(ini, 3),
         'duracao_util_s': round(util, 3), 'golpes': len(golpes), 'tom_0a1': round(tonalidade(principal), 2),
         'brilho_hz': round(centroide), 'grave_pct': round(100 * grave, 1),
         'ataque_ms': round(1000 * (int(np.argmax(e >= pk - 1)) * dt - ini), 1)}
    if 'riser' in nome:
        ativo = e > pk - 40
        tt = np.arange(len(e))[ativo]
        m['sobe_0a1'] = round(float(np.corrcoef(tt, e[ativo])[0, 1]), 2)
        ult = e[np.nonzero(ativo)[0][-1] - 20:np.nonzero(ativo)[0][-1]]
        m['fim_vs_pico_db'] = round(float(ult.max() - pk), 1)
        m['pico_em_s'] = round(float(np.argmax(e) * dt), 3)
    if 'ambiente' in nome:
        mid = e[int(0.3 / dt):int((len(x) / SR - 0.3) / dt)]
        m['nivel_medio_db'] = round(float(10 * np.log10(np.mean(10 ** (mid / 10)))), 1)
        m['oscila_db'] = round(float(np.percentile(mid, 95) - np.percentile(mid, 5)), 1)
    res[nome] = m
    print(f'{nome:26s} ' + ' '.join(f'{k}={v}' for k, v in m.items()))

with open(os.path.join(AQUI, 'efeitos-medidas.json'), 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
