"""Ajusta o volume final do vídeo sem mexer na imagem.

Aplica UM ganho fixo no vídeo inteiro (o mesmo do começo ao fim, então a curva da trilha e os acentos ficam iguais).
O ganho é o menor entre:
  - o que leva o vídeo a -14 LUFS (padrão do Reels);
  - o que deixa todo pico FORA do impacto da data em no máximo -1,5 dB (a voz nunca passa por limitador);
  - o que leva o golpe do impacto a -1 dB permitindo no máximo ~3 dB de limitador SÓ nesse instante (transiente curto).
O limitador fica ligado apenas na janela do impacto (IMPACTO_S ± ~0,25 s).
Numa trilha em crescendo (começo quase em silêncio, impacto no fim) o vídeo fica abaixo de -14 LUFS no total, mas o
impacto chega ao máximo sem ser achatado e a voz fica intacta.

Uso: python -I fonte/normalizar-audio.py <entrada.mp4> <saida.mp4>
"""
import re
import subprocess
import sys

import numpy as np
from scipy.signal import resample_poly

ALVO_LUFS = -14.0
TETO_DB = -1.5            # teto de pico fora do impacto e do limitador
IMPACTO_S = 14.833        # golpe da trilha (revelação da data)
JANELA = (IMPACTO_S - 0.08, IMPACTO_S + 0.30)
LIMITE_ACHATAR = 3.0      # dB de limitador permitidos só no golpe do impacto
SR = 48000


def lufs(arquivo):
    e = subprocess.run(['ffmpeg', '-hide_banner', '-i', arquivo, '-af', 'ebur128=peak=true:framelog=quiet', '-f', 'null', '-'],
                       capture_output=True, text=True).stderr
    return float(re.findall(r'I:\s+(-?[\d.]+) LUFS', e)[-1]), float(re.findall(r'Peak:\s+(-?[\d.]+) dBFS', e)[-1])


def pico_real(x):
    """pico com sobreamostragem 4x (aproxima o true peak), em dB"""
    return 20 * np.log10(np.abs(resample_poly(x, 4, 1, axis=0)).max() + 1e-12)


entrada, saida = sys.argv[1], sys.argv[2]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', entrada, '-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'],
                     capture_output=True, check=True).stdout
x = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
a, b = int(JANELA[0] * SR), int(JANELA[1] * SR)
fora = np.vstack([x[:a], x[b:]])
p_fora, p_imp = pico_real(fora), pico_real(x[a:b])
i0, _ = lufs(entrada)
g_lufs = ALVO_LUFS - i0
g_fora = TETO_DB - p_fora
g_imp = (TETO_DB - p_imp) + LIMITE_ACHATAR
ganho = min(g_lufs, g_fora, g_imp)
quem = {g_lufs: 'alvo de -14 LUFS', g_fora: 'pico fora do impacto (voz intacta)', g_imp: 'golpe do impacto'}[ganho]
print(f'antes: {i0:.1f} LUFS | pico fora do impacto {p_fora:.1f} dB | pico no impacto {p_imp:.1f} dB')
lim = 10 ** (TETO_DB / 20)
filtro = (f'volume={ganho:.2f}dB,'
          f"alimiter=limit={lim:.4f}:attack=1:release=40:level=disabled:enable='between(t,{JANELA[0]:.3f},{JANELA[1]:.3f})'")
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', entrada, '-c:v', 'copy', '-af', filtro, '-ar', str(SR),
                '-c:a', 'aac', '-b:a', '256k', '-movflags', '+faststart', saida], check=True)
i, tp = lufs(saida)
print(f'ganho fixo {ganho:+.2f} dB (limitado por: {quem}) -> depois: {i:.1f} LUFS, pico {tp:.1f} dBTP  ->  {saida}')
