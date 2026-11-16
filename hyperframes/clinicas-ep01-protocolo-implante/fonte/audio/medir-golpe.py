"""Mede o golpe (o impacto único) de cada candidata de trilha, sem depender só do "npx hyperframes audio".

Como mede:
  - volume a cada 10 ms em duas faixas: grave (30-150 Hz, onde mora o "boom") e larga (o som inteiro);
  - "salto" = quanto o volume dos 150 ms seguintes passa a média do 1,5 s anterior, em dB;
  - o golpe é o maior salto do grave entre 20 e 40 s; o instante exato é o começo do ataque
    (primeiro ponto em que o grave chega a 50% do pico do ataque, com precisão de 1 ms).
Também imprime o perfil de volume segundo a segundo (para ver o crescendo e se há um 2º golpe).
Atenção: o "maior salto do grave" nem sempre é o golpe. Na candidata B, o 1º lugar (33,35 s) é uma nota grave
longa (só grave); o golpe de verdade é o 2º lugar (36,68 s), que salta em TODAS as faixas, do quase silêncio ao cheio.
O instante exato usado no corte (36,677 s) foi medido com janelas de 1 ms no som inteiro (25% do pico do ataque).

Uso:   python -I fonte/audio/medir-golpe.py assets/audio/fontes/trilha-tema-a.mp3 [...]
Saída: fonte/audio/golpes.json
"""
import json
import os
import subprocess
import sys

import numpy as np
from scipy.signal import butter, sosfiltfilt

AQUI = os.path.dirname(os.path.abspath(__file__))
SR = 48000


def ler(caminho):
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', caminho, '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def env_db(x, hop):
    n = len(x) // hop
    r = np.sqrt((x[:n * hop].reshape(n, hop) ** 2).mean(1) + 1e-12)
    return 20 * np.log10(r)


resultado = {}
for caminho in sys.argv[1:]:
    x = ler(caminho)
    grave = sosfiltfilt(butter(4, [30, 150], 'bandpass', fs=SR, output='sos'), x)
    hop = SR // 100  # 10 ms
    eg, el = env_db(grave, hop), env_db(x, hop)
    t = np.arange(len(eg)) / 100

    def salto(e):
        s = np.full(len(e), -99.0)
        for i in range(150, len(e) - 15):
            antes = 10 * np.log10(np.mean(10 ** (e[i - 150:i] / 10)))
            depois = 10 * np.log10(np.mean(10 ** (e[i:i + 15] / 10)))
            s[i] = depois - antes
        return s

    sg, sl = salto(eg), salto(el)
    janela = (t >= 20) & (t <= 40)
    ordem = np.argsort(-np.where(janela, sg, -99))
    candidatos = []
    for i in ordem:
        if all(abs(i - c) > 100 for c in candidatos):
            candidatos.append(i)
        if len(candidatos) == 4:
            break
    golpes = []
    for i in candidatos:
        # instante fino: na amostra, primeiro ponto em que o grave chega a 50% do pico do ataque
        a, b = int((t[i] - 0.10) * SR), int((t[i] + 0.25) * SR)
        seg = np.abs(grave[a:b])
        pico = seg.max()
        k = np.argmax(seg >= 0.5 * pico)
        seg_l = np.abs(x[a:b])
        kl = np.argmax(seg_l >= 0.5 * seg_l.max())
        golpes.append({'t_grave_s': round(float((a + k) / SR), 3), 't_largo_s': round(float((a + kl) / SR), 3),
                       'salto_grave_db': round(float(sg[i]), 1), 'salto_largo_db': round(float(sl[i]), 1),
                       'pico_grave_dbfs': round(float(20 * np.log10(pico)), 1)})
    perfil = [round(float(10 * np.log10(np.mean(10 ** (el[s * 100:(s + 1) * 100] / 10)))), 1)
              for s in range(int(len(el) / 100))]
    nome = os.path.basename(caminho)
    resultado[nome] = {'duracao_s': round(len(x) / SR, 3), 'golpes_provaveis': golpes, 'volume_por_segundo_db': perfil}
    print(f'\n== {nome} ({len(x) / SR:.2f} s)')
    for g in golpes:
        print('  golpe?', g)
    print('  volume por segundo (dB):', ' '.join(f'{s}:{v:.0f}' for s, v in enumerate(perfil)))

with open(os.path.join(AQUI, 'golpes.json'), 'w', encoding='utf-8') as f:
    json.dump(resultado, f, ensure_ascii=False, indent=1)
