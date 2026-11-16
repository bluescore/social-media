"""Mede as 2 tomadas de cada efeito NOVO do áudio final (ep. 01 completo) para escolher a melhor, só por números.

Mede o mesmo que medir-efeitos.py (pico, começo, duração útil, golpes, "tom" de 0 a 1, brilho, grave) e mais:
  - o desenho do volume ao longo do arquivo (de 50 em 50 ms, em dB abaixo do pico), para ver se o som cresce,
    fica ou some;
  - "nota escondida": a maior concentração de energia numa só frequência (dB acima da mediana do espectro);
    um som sem nota fica abaixo de ~15 dB;
  - nos passos e nos toques: o instante de cada golpe (máximos locais a menos de 14 dB do pico, afastados > 120 ms);
  - nos ambientes: volume médio e quanto ele oscila (ambiente bom = baixo e estável) e estalos (saltos > 12 dB).

Uso:   python -I fonte/audio/medir-efeitos-final.py
Saída: fonte/audio/efeitos-final-medidas.json e a tabela no terminal. Não mexe em nenhum arquivo antigo.
"""
import json
import os
import subprocess

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(os.path.dirname(AQUI))
FONTES = os.path.join(PECA, 'assets', 'audio', 'fontes')
SR = 48000
NOVOS = ['atrito-vidro-fosco', 'chiado-corte', 'textura-granular', 'brilho-luz', 'sopro-levar',
         'ambiente-recepcao-tarde', 'ambiente-consultorio-tarde', 'passos-madeira', 'porta-fechando',
         'chegada-mensagem']


def ler(c):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', c, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def env_db(x, ms=5):
    hop = int(SR * ms / 1000)
    n = len(x) // hop
    return 20 * np.log10(np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)), ms / 1000


def tonalidade(y):
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


def nota_escondida(y):
    spec = np.abs(np.fft.rfft(y * np.hanning(len(y)))) ** 2
    fr = np.fft.rfftfreq(len(y), 1 / SR)
    sel = (fr > 60) & (fr < 8000)
    s = 10 * np.log10(spec[sel] + 1e-20)
    k = int(np.argmax(s))
    return round(float(s[k] - np.median(s)), 1), round(float(fr[sel][k]))


res = {}
for base in NOVOS:
    for tom in ('abcdef' if base == 'atrito-vidro-fosco' else ('abcd' if base == 'sopro-levar' else 'ab')):
        nome = f'{base}-{tom}.mp3'
        x = ler(os.path.join(FONTES, nome))
        e, dt = env_db(x)
        pk = e.max()
        ini = int(np.argmax(e > pk - 30)) * dt
        util = float((e > pk - 20).sum() * dt)
        idx = [i for i in range(1, len(e) - 1) if e[i] >= e[i - 1] and e[i] >= e[i + 1] and e[i] > pk - 14]
        golpes = []
        for i in idx:
            if not golpes or (i - golpes[-1]) * dt > 0.12:
                golpes.append(i)
            elif e[i] > e[golpes[-1]]:
                golpes[-1] = i
        ativo = x[int(ini * SR):int((ini + max(util, 0.05) + 0.05) * SR)]
        spec = np.abs(np.fft.rfft(ativo * np.hanning(len(ativo))))
        fr = np.fft.rfftfreq(len(ativo), 1 / SR)
        e50, _ = env_db(x, 50)
        m = {'duracao_s': round(len(x) / SR, 3), 'pico_dbfs': round(float(20 * np.log10(np.abs(x).max() + 1e-12)), 1),
             'comeca_s': round(ini, 3), 'pico_em_s': round(float(np.argmax(e) * dt), 3),
             'duracao_util_s': round(util, 3), 'golpes': len(golpes),
             'golpes_em_s': [round(g * dt, 3) for g in golpes][:12],
             'tom_0a1': round(tonalidade(ativo), 2), 'nota_escondida_db_hz': nota_escondida(ativo),
             'brilho_hz': round(float((spec * fr).sum() / (spec.sum() + 1e-12))),
             'grave_pct': round(100 * float((spec[fr < 150] ** 2).sum() / ((spec ** 2).sum() + 1e-12)), 1),
             'desenho_50ms_db': [int(round(v - e50.max())) for v in e50]}
        if base.startswith('ambiente'):
            mid = e[int(0.3 / dt):int((len(x) / SR - 0.3) / dt)]
            m['nivel_medio_db'] = round(float(10 * np.log10(np.mean(10 ** (mid / 10)))), 1)
            m['oscila_db'] = round(float(np.percentile(mid, 95) - np.percentile(mid, 5)), 1)
            m['estalos'] = int((np.diff(mid) > 12).sum())
        res[nome] = m
        print(f"{nome:32s} dur {m['duracao_s']:.2f} pico {m['pico_dbfs']:6.1f} começa {m['comeca_s']:.3f} "
              f"pico_em {m['pico_em_s']:.3f} útil {m['duracao_util_s']:.3f} golpes {m['golpes']} "
              f"{m['golpes_em_s']} tom {m['tom_0a1']} nota {m['nota_escondida_db_hz']} brilho {m['brilho_hz']} "
              f"grave {m['grave_pct']}%" + (f" nível {m['nivel_medio_db']} oscila {m['oscila_db']} estalos "
                                          f"{m['estalos']}" if 'oscila_db' in m else ''))
        print('   desenho (50 ms):', ' '.join(str(v) for v in m['desenho_50ms_db']))

with open(os.path.join(AQUI, 'efeitos-final-medidas.json'), 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=1)
