"""Prepara a fachada para a cena 1.

Entrada (fonte/quadros):
  q1-v1.png        fachada com todas as janelas apagadas (Nano Banana Pro, 4k)
  q1-acesa-v1.png  a mesma fachada com ~100 janelas acesas em laranja (edição da anterior)

Saída:
  assets/img/fachada.jpg            fachada apagada, escurecida para o clima da referência
  assets/img/janelas/jNNN.png       a luz de cada janela, recortada (só o vidro, com borda suave)
  fonte/janelas.json                posição de cada janela na fachada (pixels da imagem 4k)
  fonte/quadros/q1-alvo.png         fachada com só a janela-alvo acesa (base do zoom)
  fonte/quadros/q2-recorte.png      recorte em volta da janela-alvo (referência para o quadro 2)

Uso: python -I fonte/janelas.py   (rodar de dentro da pasta da peça)
"""
import json
import os

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(AQUI)
Q = os.path.join(AQUI, 'quadros')

# janela que fica acesa e onde a câmera entra (centro aproximado, pixels da imagem 4k)
ALVO = (1535, 2407)
# brilho médio desejado da fachada (L de 0 a 100); a referência fica em ~18
BRILHO_ALVO = 19.0

escura = cv2.imread(os.path.join(Q, 'q1-v1.png'))
acesa = cv2.imread(os.path.join(Q, 'q1-acesa-v1.png'))
H, W = escura.shape[:2]

# 1) alinhar a versão acesa com a apagada (a IA desloca ~2 px)
ga = cv2.cvtColor(escura, cv2.COLOR_BGR2GRAY).astype(np.float32)
gb = cv2.cvtColor(acesa, cv2.COLOR_BGR2GRAY).astype(np.float32)
(dx, dy), _ = cv2.phaseCorrelate(ga, gb)
M = np.float32([[1, 0, -dx], [0, 1, -dy]])
acesa = cv2.warpAffine(acesa, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
print(f'deslocamento corrigido: {dx:.2f}, {dy:.2f}')

# 2) achar as janelas acesas (vidro laranja)
hsv = cv2.cvtColor(acesa, cv2.COLOR_BGR2HSV)
h, s, v = hsv[..., 0].astype(np.float32), hsv[..., 1].astype(np.float32), hsv[..., 2].astype(np.float32)
laranja = ((h >= 3) & (h <= 25)).astype(np.float32)
# alfa suave: quão "laranja aceso" é cada pixel
alfa = laranja * np.clip((s - 90) / 80, 0, 1) * np.clip((v - 80) / 70, 0, 1)
alfa = cv2.GaussianBlur(alfa, (0, 0), 1.2)
binaria = (alfa > 0.35).astype(np.uint8)
# junta as duas folhas de uma mesma janela (o caixilho do meio separa)
juntas = cv2.morphologyEx(binaria, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (45, 21)))
n, lab, st, cen = cv2.connectedComponentsWithStats(juntas)

pasta_j = os.path.join(PECA, 'assets', 'img', 'janelas')
os.makedirs(pasta_j, exist_ok=True)
for f in os.listdir(pasta_j):
    os.remove(os.path.join(pasta_j, f))

janelas = []
for i in range(1, n):
    x, y, w, hh, area = st[i]
    if area < 4000:
        continue
    pad = 6
    x0, y0 = max(x - pad, 0), max(y - pad, 0)
    x1, y1 = min(x + w + pad, W), min(y + hh + pad, H)
    a = alfa[y0:y1, x0:x1] * (lab[y0:y1, x0:x1] == i).astype(np.float32)
    a = cv2.dilate(a, np.ones((3, 3), np.uint8))
    a = cv2.GaussianBlur(a, (0, 0), 0.8)
    rgba = np.dstack([acesa[y0:y1, x0:x1], np.clip(a * 255, 0, 255).astype(np.uint8)])
    janelas.append({'x': int(x0), 'y': int(y0), 'w': int(x1 - x0), 'h': int(y1 - y0),
                    'cx': float(cen[i][0]), 'cy': float(cen[i][1]), 'rgba': rgba})

# ordem estável: de cima para baixo, da esquerda para a direita
janelas.sort(key=lambda j: (round(j['cy'] / 100), j['cx']))
alvo_idx = min(range(len(janelas)), key=lambda k: (janelas[k]['cx'] - ALVO[0]) ** 2 + (janelas[k]['cy'] - ALVO[1]) ** 2)
saida = []
for k, j in enumerate(janelas):
    nome = f'j{k:03d}.png'
    cv2.imwrite(os.path.join(pasta_j, nome), j['rgba'])
    saida.append({'id': f'j{k:03d}', 'x': j['x'], 'y': j['y'], 'w': j['w'], 'h': j['h'],
                  'cx': round(j['cx'], 1), 'cy': round(j['cy'], 1), 'alvo': k == alvo_idx})
print(f'{len(saida)} janelas; alvo = j{alvo_idx:03d} em ({janelas[alvo_idx]["cx"]:.0f}, {janelas[alvo_idx]["cy"]:.0f})')

with open(os.path.join(AQUI, 'janelas.json'), 'w', encoding='utf-8') as f:
    json.dump({'largura': W, 'altura': H, 'janelas': saida}, f, indent=1)


# 3) escurecer a fachada até o clima da referência (curva de potência no brilho)
def brilho(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2LAB)[..., 0].mean() * 100 / 255


lo, hi = 1.0, 3.0
base = escura.astype(np.float32) / 255
for _ in range(25):
    g = (lo + hi) / 2
    teste = (np.power(base, g) * 255).astype(np.uint8)
    if brilho(teste) > BRILHO_ALVO:
        lo = g
    else:
        hi = g
gama = (lo + hi) / 2
fachada = (np.power(base, gama) * 255).clip(0, 255).astype(np.uint8)
print(f'gama {gama:.3f}: brilho {brilho(escura):.1f} -> {brilho(fachada):.1f}')
cv2.imwrite(os.path.join(PECA, 'assets', 'img', 'fachada.jpg'), fachada, [cv2.IMWRITE_JPEG_QUALITY, 92])

# 4) fachada com só a janela-alvo acesa, e o recorte para o quadro 2
j = janelas[alvo_idx]
comp = fachada.astype(np.float32)
a = j['rgba'][..., 3:4].astype(np.float32) / 255
reg = comp[j['y']:j['y'] + j['h'], j['x']:j['x'] + j['w']]
comp[j['y']:j['y'] + j['h'], j['x']:j['x'] + j['w']] = reg * (1 - a) + j['rgba'][..., :3] * a
comp = comp.astype(np.uint8)
cv2.imwrite(os.path.join(Q, 'q1-alvo.png'), comp)

# recorte 9:16 com ~3 colunas de janelas, centrado na janela-alvo
RW = 900
RH = int(RW * 16 / 9)
cx, cy = int(j['cx']), int(j['cy'])
x0 = int(np.clip(cx - RW / 2, 0, W - RW))
y0 = int(np.clip(cy - RH / 2, 0, H - RH))
cv2.imwrite(os.path.join(Q, 'q2-recorte.png'), comp[y0:y0 + RH, x0:x0 + RW])
with open(os.path.join(AQUI, 'recortes.json'), 'w', encoding='utf-8') as f:
    json.dump({'q2': {'x': x0, 'y': y0, 'w': RW, 'h': RH}}, f, indent=1)
print(f'recorte q2: x={x0} y={y0} {RW}x{RH}')
