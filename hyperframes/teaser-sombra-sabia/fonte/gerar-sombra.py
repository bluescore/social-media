# Placa de sombra v2 (1080x1920, 30 fps, RGB): pássaro menor, pausa antes da entrada,
# gesto de asa depois do pouso, profundidade (folhagem de cima mais borrada) e sombra azulada.
import sys, os, math
import numpy as np
from PIL import Image, ImageFilter

QUADROS, SAIDA = sys.argv[1], sys.argv[2]
TESTE = [float(x) for x in sys.argv[3].split(',')] if len(sys.argv) > 3 else None
FPS_FONTE = 60000 / 1001
INICIO_FONTE = 16.5
FPS = 30
DURACAO = 8.5
LO, HI = 150.0, 250.0
Y_OFF = -23                      # posição vertical do recorte (ampliado 1,55x) dentro do quadro 1920
TINTA = np.array([0x51, 0x2f, 0x27], np.float32)   # cor da sombra: multiplicada pela parede laranja dá um laranja queimado escuro

# (t_ini, t_fim, fonte_ini, fonte_fim) — vídeo original tocado de trás para frente
TRILHA_A = [
    (0.00, 1.40, 24.55, 24.55),   # galho vazio, calmo
    (1.40, 1.55, 24.55, 24.40),   # entrada rápida (tempo real)
    (1.55, 1.95, 24.40, 24.20),   # freada e toque (câmera lenta 2x)
    (1.95, 2.35, 24.20, 24.00),   # assenta (2x)
    (2.35, 3.55, 24.00, 22.80),   # pousado
]
TRILHA_B = [(3.25, 8.60, 22.15, 16.80)]   # continua mais adiante (inclui o gesto de asa ~3,8 s)
CORTE = (3.25, 3.55)                       # fusão suave entre as duas trilhas

def tempo(trilha, t):
    for a, b, fa, fb in trilha:
        if t <= b:
            return fa + (fb - fa) * (max(t, a) - a) / (b - a)
    a, b, fa, fb = trilha[-1]
    return fa + (fb - fa) * (t - a) / (b - a)

def indice(s):
    return int(round((s - INICIO_FONTE) * FPS_FONTE)) + 1

cache = {}
def matte(i):
    if i not in cache:
        a = np.asarray(Image.open(os.path.join(QUADROS, f"{i:04d}.png")), dtype=np.float32)
        m = np.clip((a - LO) / (HI - LO), 0, 1)          # 1 = parede, 0 = sombra
        tela = np.ones((1920, 1080), np.float32)
        y0 = max(0, Y_OFF); sy = max(0, -Y_OFF)
        h = min(1920 - y0, m.shape[0] - sy)
        tela[y0:y0 + h] = m[sy:sy + h]
        cache[i] = 1 - (1 - tela) * DESBOTA               # some aos poucos embaixo
        if len(cache) > 10:
            cache.pop(next(iter(cache)))
    return cache[i]

def media(trilha, t):
    i0, i1 = indice(tempo(trilha, t)), indice(tempo(trilha, t + 1 / FPS))
    passo = -1 if i1 < i0 else 1
    idx = list(range(i0, i1, passo)) or [i0]
    m = sum(matte(i) for i in idx) / len(idx)
    if len(idx) > 1:   # borrão de movimento só no alto (pássaro); galho nítido
        m = m * ALTO + matte(idx[0]) * (1 - ALTO)
    return m

def quadro(t):
    if t < CORTE[0]:
        m = media(TRILHA_A, t)
    elif t > CORTE[1]:
        m = media(TRILHA_B, t)
    else:
        u = (t - CORTE[0]) / (CORTE[1] - CORTE[0]); u = u * u * (3 - 2 * u)
        m = (1 - u) * media(TRILHA_A, t) + u * media(TRILHA_B, t)
    img = Image.fromarray((m * 255).astype(np.uint8))
    perto = (0.65 * np.asarray(img.filter(ImageFilter.GaussianBlur(7)), np.float32)
             + 0.35 * np.asarray(img.filter(ImageFilter.GaussianBlur(22)), np.float32))
    longe = (0.6 * np.asarray(img.filter(ImageFilter.GaussianBlur(18)), np.float32)
             + 0.4 * np.asarray(img.filter(ImageFilter.GaussianBlur(36)), np.float32))
    s = (perto * (1 - LONGE) + longe * LONGE) / 255.0      # 1 = parede, 0 = sombra
    rgb = s[..., None] * 255 + (1 - s[..., None]) * TINTA
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))

yy = np.arange(1920, dtype=np.float32)[:, None]
xx = np.arange(1080, dtype=np.float32)[None, :]
_u = np.clip((1680 - yy) / 300, 0, 1)
DESBOTA = np.broadcast_to(_u * _u * (3 - 2 * _u), (1920, 1080))                    # base some devagar
ALTO = np.broadcast_to(np.clip((1060 - yy) / 60 + 0.5, 0, 1), (1920, 1080))        # região do pássaro em voo
d = np.sqrt(((xx - 120) / 560) ** 2 + ((yy - 180) / 640) ** 2)
_b = np.clip((yy - 1360) / 320, 0, 1)
LONGE = np.maximum(np.clip(1.25 - d, 0, 1) ** 1.5, _b * _b * (3 - 2 * _b))         # folhagem do alto e base: mais desfocadas

os.makedirs(SAIDA, exist_ok=True)
tempos = TESTE if TESTE else [n / FPS for n in range(int(round(DURACAO * FPS)))]
for n, t in enumerate(tempos):
    nome = f"t{t:05.2f}.png" if TESTE else f"{n:04d}.png"
    quadro(t).save(os.path.join(SAIDA, nome))
print("ok", len(tempos))
