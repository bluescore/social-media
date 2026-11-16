"""Prepara as cenas do elevador para a montagem (versão 2, depois da revisão).

Cena do BOTÃO (fonte/clipes/c5-botao-v1.mp4 -> assets/video/botao.mp4, 2,5 s):
  - Cor: a imagem da IA saiu quente e lavada (aço cor de cobre), e o botão aceso não "estourava" como na referência.
    A imagem fica mais escura e fria, como o aço da referência, e só a luz do botão vai para o laranja da marca #F34500.
  - Tempo (o clipe começa sob o clarão laranja da entrada; a mão já aparece EM MOVIMENTO — o dono achou que o
    começo parecia pausado quando ele era tocado em câmera lenta):
      0,00–0,70 s  a mão avança, encosta e aperta numa velocidade só (1,9x, sem degraus que deem tranco;
                   no original o dedo desliza ~1 s sem nada acontecer)
      0,70 s       o botão ACENDE (cai numa batida da trilha: 8,233–8,267 s do filme)
      0,70–2,6 s   a mão recua e sai (1,45x) e o botão fica aceso sozinho
  - Sai a 30 quadros/s com mistura dos quadros vizinhos (o Kling entrega 24 q/s; sem isso o movimento dá trancos).

Cena da ESPERA (fonte/clipes/c6-espera-v1.mp4 -> assets/video/espera.mp4, 5,0 s):
  - O painel ao lado da porta tinha um triângulo escuro solto em cima e um quadrado aceso vazio embaixo — diferente
    do botão do close. O triângulo de cima é apagado e um triângulo aceso é desenhado dentro do quadrado,
    para ser o mesmo botão (quadrado com o triângulo de subir) da cena anterior.
  - Luz do botão no laranja da marca; 30 q/s com mistura de quadros.

Uso: python -I fonte/corrigir-clipes.py
"""
import os
import subprocess

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(AQUI)
FPS_ORIGEM = 24
FPS = 30
MATIZ_MARCA = 17.0 / 2  # #F34500 em graus/2 (escala do OpenCV)
LARANJA_BGR = np.array([0, 69, 243], np.float32)  # #F34500


def suave(x, a, b):
    return np.clip((x - a) / (b - a), 0, 1)


def mascara_luz(r, v_min, s_min, matiz_max):
    hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1] / 255, hsv[..., 2] / 255
    quente = suave(h, 2, 5) * (1 - suave(h, matiz_max, matiz_max + 4))
    m = quente * suave(v, v_min, v_min + 0.08) * suave(s, s_min, s_min + 0.1)
    return cv2.GaussianBlur(m, (0, 0), 1.1), v


def pintar_luz(r, m, v, miolo, brilho):
    """Pinta a luz (máscara m) no laranja da marca, mantendo o brilho de cada pixel; halo opcional."""
    hsv = cv2.cvtColor(r, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 0] = MATIZ_MARCA
    hsv[..., 1] = 255 * np.where(v > 0.985, miolo, 0.95)
    hsv[..., 2] = np.maximum(hsv[..., 2], 255 * v)
    out = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    res = r.astype(np.float32) * (1 - m[..., None]) + out * m[..., None]
    if brilho > 0:
        halo = cv2.GaussianBlur(m, (0, 0), 7) * brilho
        res = 255 - (255 - res) * (1 - halo[..., None] * LARANJA_BGR / 255)
    return np.clip(res, 0, 255).astype(np.uint8)


def gradear_frio(q, luz=0.82, croma=0.68, frio=2.5):
    """Escurece e esfria a imagem (aço frio como na referência): menos brilho, menos cor, um pouco para o azul."""
    lab = cv2.cvtColor(q, cv2.COLOR_BGR2LAB).astype(np.float32)
    L = lab[..., 0] / 255
    lab[..., 0] = 255 * np.power(L, 1.18) * luz
    lab[..., 1] = 128 + (lab[..., 1] - 128) * croma
    lab[..., 2] = 128 + (lab[..., 2] - 128) * croma - frio
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)


def ler(caminho):
    cap = cv2.VideoCapture(caminho)
    q = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        q.append(f)
    return q


def amostrar(quadros, s):
    """Quadro no tempo s (s) do clipe original, misturando os dois quadros vizinhos (24 -> 30 q/s sem trancos)."""
    f = min(max(s * FPS_ORIGEM, 0), len(quadros) - 1)
    a = int(np.floor(f))
    b = min(a + 1, len(quadros) - 1)
    w = f - a
    if w < 0.02 or a == b:
        return quadros[a].copy()
    if w > 0.98:
        return quadros[b].copy()
    # movimento rápido (a mão saindo): misturar cria um "fantasma" com dois dedos; usa o quadro mais próximo
    pa = cv2.resize(quadros[a], (135, 241), interpolation=cv2.INTER_AREA).astype(np.int16)
    pb = cv2.resize(quadros[b], (135, 241), interpolation=cv2.INTER_AREA).astype(np.int16)
    if np.abs(pa - pb).mean() > 4.0:
        return quadros[a if w < 0.5 else b].copy()
    return cv2.addWeighted(quadros[a], 1 - w, quadros[b], w, 0)


def gravar(quadros, destino):
    h, w = quadros[0].shape[:2]
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-s', f'{w}x{h}',
                          '-r', str(FPS), '-i', '-', '-an', '-c:v', 'libx264', '-crf', '14', '-preset', 'slow',
                          '-pix_fmt', 'yuv420p', '-movflags', '+faststart', destino], stdin=subprocess.PIPE)
    for f in quadros:
        p.stdin.write(f.tobytes())
    p.stdin.close()
    p.wait()
    print(f'{destino}: {len(quadros)} quadros ({len(quadros) / FPS:.2f} s)')


# ======================= BOTÃO =======================
orig = ler(os.path.join(AQUI, 'clipes', 'c5-botao-v1.mp4'))
# (tempo no clipe novo, tempo no original): entre os pontos, velocidade constante
MAPA_BOTAO = [(0.0, 0.13), (0.70, 1.46), (2.6, 1.46 + 1.9 * 1.45)]
ROI_BOTAO = (585, 860, 790, 1080)


def origem_botao(t):
    for (t0, s0), (t1, s1) in zip(MAPA_BOTAO, MAPA_BOTAO[1:]):
        if t <= t1:
            return s0 + (s1 - s0) * (t - t0) / (t1 - t0)
    return MAPA_BOTAO[-1][1]


saida = []
for i in range(int(2.6 * FPS)):
    q = amostrar(orig, origem_botao(i / FPS))
    x0, y0, x1, y1 = ROI_BOTAO
    m, v = mascara_luz(q[y0:y1, x0:x1], v_min=0.76, s_min=0.24, matiz_max=34)
    m = np.clip(m * 1.35, 0, 1)  # anel mais "cheio" (borda mais dura)
    q = gradear_frio(q)
    q[y0:y1, x0:x1] = pintar_luz(q[y0:y1, x0:x1], m, v, miolo=0.93, brilho=0.45)
    saida.append(q)
gravar(saida, os.path.join(PECA, 'assets', 'video', 'botao.mp4'))

# instante em que o botão acende no clipe novo (para alinhar o clique)
x0, y0, x1, y1 = ROI_BOTAO
lum = []
for q in saida:
    h = cv2.cvtColor(q[y0:y1, x0:x1], cv2.COLOR_BGR2HSV)
    lum.append(int(((h[..., 1] > 150) & (h[..., 2] > 170)).sum()))
base, topo = np.median(lum[:20]), max(lum)
acende = next(i for i, n in enumerate(lum) if n > base + 0.5 * (topo - base))
print(f'botão acende no quadro {acende} do clipe novo = {acende / FPS:.3f} s')

# ======================= ESPERA =======================
orig = ler(os.path.join(AQUI, 'clipes', 'c6-espera-v1.mp4'))


def caixa_quadrado(q):
    """Caixa do quadrado aceso do botão (x0, y0, x1, y1) no quadro."""
    h = cv2.cvtColor(q[1300:1560, 900:1076], cv2.COLOR_BGR2HSV)
    m = (h[..., 1] > 120) & (h[..., 2] > 170) & (h[..., 0] < 30)
    ys, xs = np.nonzero(m)
    return np.array([xs.min() + 900, ys.min() + 1300, xs.max() + 900, ys.max() + 1300], np.float32)


# medir e suavizar a posição do botão quadro a quadro (o avanço da câmera é lento e contínuo)
caixas = np.array([caixa_quadrado(q) for q in orig])
tq = np.arange(len(orig)) / FPS_ORIGEM
ajuste = [np.polyfit(tq, caixas[:, k], 2) for k in range(4)]


def caixa_em(s):
    return np.array([np.polyval(a, s) for a in ajuste])


def apagar_triangulo(q, c):
    """Apaga o triângulo escuro solto no alto do painel (fica ~640 px acima do quadrado)."""
    # o triângulo fica em x 988–1075, y 732–818 do começo ao fim do clipe (medido).
    # O painel ali é uma faixa de aço desfocada: cada coluna é refeita ligando a linha de cima (y 700) à de
    # baixo (y 832) do próprio quadro, com um pouco do grão do aço por cima; a borda da emenda é suave.
    ya, yb, xa, xb = 700, 832, 978, 1076
    cima = q[ya - 4:ya + 1, xa:xb].astype(np.float32).mean(0)
    baixo = q[yb:yb + 5, xa:xb].astype(np.float32).mean(0)
    k = np.linspace(0, 1, yb - ya)[:, None, None]
    liso = cima[None] * (1 - k) + baixo[None] * k
    grao_ref = q[900:900 + (yb - ya), xa:xb].astype(np.float32)  # trecho liso do meio do painel
    grao = grao_ref - cv2.GaussianBlur(grao_ref, (0, 0), 3)
    novo = liso + grao * 0.8
    m = np.zeros((yb - ya, xb - xa), np.float32)
    m[12:-10, 6:] = 1
    m = cv2.GaussianBlur(m, (0, 0), 5)[..., None]
    reg = q[ya:yb, xa:xb].astype(np.float32)
    q[ya:yb, xa:xb] = np.clip(reg * (1 - m) + novo * m, 0, 255).astype(np.uint8)
    return q


def desenhar_triangulo(q, c):
    """Triângulo de subir aceso dentro do quadrado (como o botão do close), desfocado como o resto do painel."""
    x0, y0, x1, y1 = c
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 0.02 * (y1 - y0)
    lado = 0.40 * (x1 - x0)
    alt = lado * 0.9
    pts = np.array([[cx, cy - alt / 2], [cx - lado / 2, cy + alt / 2], [cx + lado / 2, cy + alt / 2]])
    esc = 4  # desenha em resolução maior para não serrilhar
    pad = 40
    bx0, by0 = int(x0) - pad, int(y0) - pad
    bx1, by1 = min(int(x1) + pad, q.shape[1]), int(y1) + pad
    h, w = (by1 - by0) * esc, (bx1 - bx0) * esc
    m = np.zeros((h, w), np.float32)
    p = ((pts - [bx0, by0]) * esc).astype(np.int32)
    cv2.polylines(m, [p], True, 1.0, thickness=int(5.0 * esc), lineType=cv2.LINE_AA)
    m = cv2.resize(m, (bx1 - bx0, by1 - by0), interpolation=cv2.INTER_AREA)
    m = cv2.GaussianBlur(m, (0, 0), 1.3)
    reg = q[by0:by1, bx0:bx1].astype(np.float32)
    cor = np.array([40, 110, 255], np.float32)  # o mesmo laranja aceso do anel (medido no quadrado)
    reg = reg * (1 - m[..., None]) + cor * m[..., None]
    halo = cv2.GaussianBlur(m, (0, 0), 5) * 0.6
    reg = 255 - (255 - reg) * (1 - halo[..., None] * LARANJA_BGR / 255)
    q[by0:by1, bx0:bx1] = np.clip(reg, 0, 255).astype(np.uint8)
    return q


saida = []
DUR_ESPERA = (len(orig) - 1) / FPS_ORIGEM
for i in range(int(DUR_ESPERA * FPS)):
    s = i / FPS
    q = amostrar(orig, s)
    c = caixa_em(s)
    q = apagar_triangulo(q, c)
    x0, y0, x1, y1 = 950, 1330, 1076, 1510
    m, v = mascara_luz(q[y0:y1, x0:x1], v_min=0.55, s_min=0.45, matiz_max=22)
    q[y0:y1, x0:x1] = pintar_luz(q[y0:y1, x0:x1], m, v, miolo=0.85, brilho=0.0)
    q = desenhar_triangulo(q, c)
    saida.append(q)
gravar(saida, os.path.join(PECA, 'assets', 'video', 'espera.mp4'))
