"""Encaixa o quadro 2 (close da fachada) dentro da fachada aberta e iguala as cores.

Entrada: fonte/quadros/q2-v1.png, fonte/quadros/q1-alvo.png, fonte/recortes.json
Saída:   assets/img/fachada-close.jpg  (q2 com a cor da fachada aberta)
         fonte/encaixe.json            retângulo do q2 nas coordenadas da fachada 4k

Uso: python -I fonte/alinhar.py
"""
import json
import os

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(AQUI)
Q = os.path.join(AQUI, 'quadros')

rec = json.load(open(os.path.join(AQUI, 'recortes.json'), encoding='utf-8'))['q2']
q1 = cv2.imread(os.path.join(Q, 'q1-alvo.png'))
q2 = cv2.imread(os.path.join(Q, 'q2-v1.png'))
H2, W2 = q2.shape[:2]
crop = q1[rec['y']:rec['y'] + rec['h'], rec['x']:rec['x'] + rec['w']]

# 1) igualar a cor do q2 à da fachada aberta (média e desvio por canal, em Lab),
#    medindo só a fachada: a janela acesa fica de fora da conta
alvo = [j for j in json.load(open(os.path.join(AQUI, 'janelas.json'), encoding='utf-8'))['janelas'] if j['alvo']][0]


def mascara_fora_janela(shape, x, y, w, h):
    m = np.ones(shape[:2], bool)
    m[max(int(y), 0):int(y + h), max(int(x), 0):int(x + w)] = False
    return m


def transferir(src, ref, ms_src, ms_ref):
    s = cv2.cvtColor(src, cv2.COLOR_BGR2LAB).astype(np.float32)
    r = cv2.cvtColor(ref, cv2.COLOR_BGR2LAB).astype(np.float32)
    ms, ss = s[ms_src].mean(0), s[ms_src].std(0)
    mr, sr = r[ms_ref].mean(0), r[ms_ref].std(0)
    o = (s - ms) / (ss + 1e-6) * sr + mr
    return cv2.cvtColor(np.clip(o, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


# janela-alvo: no recorte (coordenadas do recorte) e no q2 (proporcional), com folga
f2 = W2 / rec['w']
jx, jy, jw, jh = alvo['x'] - rec['x'] - 40, alvo['y'] - rec['y'] - 40, alvo['w'] + 80, alvo['h'] + 80
m_ref = mascara_fora_janela(crop.shape, jx, jy, jw, jh)
m_src = mascara_fora_janela(q2.shape, jx * f2, jy * f2, jw * f2, jh * f2)
q2c = transferir(q2, crop, m_src, m_ref)

# o vidro aceso do q2 (cortina) volta para o laranja da marca, mantendo as dobras da cortina
hsv0 = cv2.cvtColor(q2, cv2.COLOR_BGR2HSV).astype(np.float32)
caixa = np.zeros(q2.shape[:2], np.float32)
caixa[int(jy * f2):int((jy + jh) * f2), int(jx * f2):int((jx + jw) * f2)] = 1
quente = ((hsv0[..., 0] <= 25) | (hsv0[..., 0] >= 165)) & (hsv0[..., 1] > 60) & (hsv0[..., 2] > 70)
vidro = cv2.GaussianBlur((quente * caixa).astype(np.float32), (0, 0), 2.0)
sprite = cv2.imread(os.path.join(PECA, 'assets', 'img', 'janelas', alvo['id'] + '.png'), cv2.IMREAD_UNCHANGED)
a_sp = sprite[..., 3] > 200
hsv_sp = cv2.cvtColor(sprite[..., :3], cv2.COLOR_BGR2HSV).astype(np.float32)
mat_alvo, sat_alvo, val_alvo = [float(np.median(hsv_sp[..., c][a_sp])) for c in range(3)]
hsv = cv2.cvtColor(q2c, cv2.COLOR_BGR2HSV).astype(np.float32)
v_orig = hsv0[..., 2]
v_med = float(np.median(v_orig[vidro > 0.5]))
novo = hsv.copy()
novo[..., 0] = mat_alvo
novo[..., 1] = sat_alvo
novo[..., 2] = np.clip(v_orig / v_med * val_alvo, 0, 255)
novo_bgr = cv2.cvtColor(novo.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
q2c = (q2c.astype(np.float32) * (1 - vidro[..., None]) + novo_bgr * vidro[..., None]).astype(np.uint8)
print(f'vidro: matiz {mat_alvo:.0f}, sat {sat_alvo:.0f}, brilho {val_alvo:.0f}')

# 2) achar onde o q2 cai dentro do recorte (SIFT + afim parcial: escala, giro e deslocamento)
pequeno = cv2.resize(q2c, (rec['w'], int(rec['w'] * H2 / W2)), interpolation=cv2.INTER_AREA)
sift = cv2.SIFT_create(4000)
g1 = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
g2 = cv2.cvtColor(pequeno, cv2.COLOR_BGR2GRAY)
k1, d1 = sift.detectAndCompute(g1, None)
k2, d2 = sift.detectAndCompute(g2, None)
pares = cv2.BFMatcher().knnMatch(d2, d1, k=2)
bons = [m for m, n in pares if m.distance < 0.75 * n.distance]
src = np.float32([k2[m.queryIdx].pt for m in bons])
dst = np.float32([k1[m.trainIdx].pt for m in bons])
A, inl = cv2.estimateAffine2D(src, dst, ransacReprojThreshold=3.0)
print(f'{len(bons)} pares, {int(inl.sum())} certos')
print('afim (q2 reduzido -> recorte):\n', A)

# canto e escala do q2 inteiro em coordenadas da fachada 4k
fator = rec['w'] / W2  # q2 -> q2 reduzido
sx = np.hypot(A[0, 0], A[1, 0]) * fator
sy = np.hypot(A[0, 1], A[1, 1]) * fator
x0 = rec['x'] + A[0, 2]
y0 = rec['y'] + A[1, 2]
giro = np.degrees(np.arctan2(A[1, 0], A[0, 0]))
enc = {'x': round(float(x0), 2), 'y': round(float(y0), 2),
       'w': round(float(W2 * sx), 2), 'h': round(float(H2 * sy), 2), 'giro_graus': round(float(giro), 3)}
print('encaixe:', enc)
json.dump(enc, open(os.path.join(AQUI, 'encaixe.json'), 'w', encoding='utf-8'), indent=1)

# 3) conferir: q2 reduzido recolocado sobre o recorte
volta = cv2.warpAffine(pequeno, A, (rec['w'], rec['h']))
erro = np.abs(volta.astype(np.float32) - crop.astype(np.float32)).mean()
print(f'diferença média depois do encaixe: {erro:.1f}')
cv2.imwrite(os.path.join(Q, 'q2-confere.jpg'), np.hstack([crop, volta]))
cv2.imwrite(os.path.join(PECA, 'assets', 'img', 'fachada-close.jpg'), q2c, [cv2.IMWRITE_JPEG_QUALITY, 92])
