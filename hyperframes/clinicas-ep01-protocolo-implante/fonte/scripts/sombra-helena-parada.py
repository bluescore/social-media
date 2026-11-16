# Desenha a sombra da Helena parada (cena 11) num PNG transparente, para não depender de degradê em CSS.
# Três camadas suaves:
#   1) o "encosto" escuro e fino que segue o contorno de baixo de cada sapato (é o que faz o pé pisar no chão);
#   2) a sombra de contato, uma mancha oval logo abaixo dos sapatos;
#   3) uma sombra longa e fraca que o sol da janela (ao fundo, à direita) joga para a frente-esquerda.
# O PNG cobre x 400-900, y 1380-1500 do quadro 1080x1920 (é posto nessa posição dentro da câmera da cena).
# A posição dos sapatos vem da própria imagem da Helena e da caixa dela na cena (left 601, top 517, 318x922).
# Rodar dentro da pasta do episódio: python -I fonte/scripts/sombra-helena-parada.py
import sys
sys.path.append(r"C:\Users\YagoBittencourt\AppData\Roaming\Python\Python313\site-packages")
import math
import numpy as np
from PIL import Image

X0, Y0, W, H = 400, 1380, 500, 120
COR = (30, 17, 8)
CAIXA = dict(left=601, top=517, w=318, h=922)   # igual ao CSS de #s11-helena

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
xx += X0 + 0.5
yy += Y0 + 0.5

def mancha(cx, cy, rx, ry, forca, angulo_graus=0.0, queda=3.0):
    """mancha elíptica com queda suave (gaussiana); o ângulo inclina o eixo maior (positivo = ponta esquerda desce)"""
    a = math.radians(angulo_graus)
    ux, uy = -math.cos(a), math.sin(a)
    vx, vy = -uy, ux
    dx, dy = xx - cx, yy - cy
    p = (dx * ux + dy * uy) / rx
    q = (dx * vx + dy * vy) / ry
    return forca * np.exp(-queda * (p * p + q * q))

# 1) contorno de baixo dos sapatos, em px do quadro
hel = np.asarray(Image.open("assets/img/helena-parada-celular.png"))[..., 3]
kx, ky = CAIXA["w"] / hel.shape[1], CAIXA["h"] / hel.shape[0]
baixo = hel.shape[0] - 160                         # só a faixa dos sapatos
pts = []
for c in range(hel.shape[1]):
    col = np.where(hel[baixo:, c] > 128)[0]
    if len(col):
        pts.append((CAIXA["left"] + (c + 0.5) * kx, CAIXA["top"] + (baixo + col.max() + 0.5) * ky))
pts = np.array(pts)
sola_x0, sola_x1 = pts[:, 0].min(), pts[:, 0].max()
sola_y = np.interp(xx[0], pts[:, 0], pts[:, 1], left=np.nan, right=np.nan)   # y da sola em cada coluna do PNG
encosto = np.zeros((H, W), np.float32)
for i in range(W):
    if np.isnan(sola_y[i]):
        continue
    d = yy[:, i] - (sola_y[i] - 1.0)
    # escuro logo na linha da sola, sumindo em ~8 px para baixo (para cima fica escondido pelo sapato)
    encosto[:, i] = 0.78 * np.exp(-0.5 * (d / 4.5) ** 2)
# suaviza as pontas (o encosto não termina de repente nas laterais do sapato)
lado = np.clip(np.minimum(xx[0] - sola_x0, sola_x1 - xx[0]) / 10.0, 0, 1)
encosto *= lado[None, :]

cx = (sola_x0 + sola_x1) / 2
cy = float(np.nanmax(sola_y))
contato = mancha(cx, cy - 2, (sola_x1 - sola_x0) / 2 + 26, 17, 0.62, queda=2.4)
longa = mancha(cx - 140, cy + 14, 190, 30, 0.30, angulo_graus=10)
alfa = 1 - (1 - encosto) * (1 - contato) * (1 - longa)

img = np.zeros((H, W, 4), np.uint8)
img[..., 0], img[..., 1], img[..., 2] = COR
img[..., 3] = np.clip(alfa * 255, 0, 255).astype(np.uint8)
Image.fromarray(img).save("assets/img/sombra-helena-parada.png", optimize=True)
print(f"sola: x {sola_x0:.0f}-{sola_x1:.0f}, y mais baixo {cy:.1f}; alfa máx {img[..., 3].max()}")
