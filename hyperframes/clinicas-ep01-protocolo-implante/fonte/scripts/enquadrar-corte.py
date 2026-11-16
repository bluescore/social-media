# Enquadra as duas imagens do corte (antes / integrado) para o passo 3 do vídeo dela (s08):
# reduz a 0,84 do quadro 1080x1920 (o bloco termina em y~1228, acima da assinatura) e sobe 17,6 px,
# e completa as bordas com o próprio fundo do estúdio (borda esticada + desfoque + grão), sem moldura.
# Rodar dentro da pasta do episódio: python fonte/scripts/enquadrar-corte.py
import numpy as np
from PIL import Image, ImageFilter

S = 0.84            # escala em relação ao quadro 1080x1920
DY = -17.6          # subida (px)
W, H = 1080, 1920

def enquadrar(src, dst):
    im = Image.open(src).convert('RGB')                     # 1152x2048
    k = (W / im.width) * S                                   # 0,7875
    w, h = round(im.width * k), round(im.height * k)
    x0 = round(540 - (im.width / 2) * k)
    y0 = round(960 + DY - (im.height / 2) * k)
    peq = np.asarray(im.resize((w, h), Image.LANCZOS)).astype(np.float32)
    pad = ((y0, H - y0 - h), (x0, W - x0 - w), (0, 0))
    cheio = np.pad(peq, pad, mode='edge')
    # fundo liso: desfoca forte a área esticada e devolve um grão parecido com o da imagem
    liso = np.asarray(Image.fromarray(cheio.clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(40))).astype(np.float32)
    borda = peq[:40, :, :]
    ruido = borda - np.asarray(Image.fromarray(borda.clip(0,255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(3))).astype(np.float32)
    sd = float(ruido.std())
    rng = np.random.default_rng(7)
    graos = rng.normal(0, sd, (H, W, 1)).astype(np.float32)
    dentro = np.zeros((H, W), np.float32)
    dentro[y0:y0 + h, x0:x0 + w] = 1
    # transição suave de 24 px entre a imagem e o fundo completado
    trans = np.asarray(Image.fromarray((dentro * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(12))).astype(np.float32) / 255
    trans = np.minimum(trans, dentro)[..., None]
    fora = liso + graos
    out = cheio * trans + fora * (1 - trans)
    Image.fromarray(out.clip(0, 255).astype(np.uint8)).save(dst, quality=92, subsampling=0)
    return k, x0, y0, w, h

for a, b in [('fonte/geradas/corte-antes.png', 'assets/img/corte-antes.jpg'),
             ('fonte/geradas/corte-integrado.png', 'assets/img/corte-integrado.jpg')]:
    print(b, enquadrar(a, b))

# pontos úteis (coordenadas do quadro 1080 antes do enquadramento -> tela)
f = lambda x, y: (round(540 + (x - 540) * S, 1), round(960 + (y - 960) * S + DY, 1))
print('tampa topo', f(540, 562), 'bloco', f(118, 625), f(955, 1300), 'roscas', f(405, 740), f(670, 1260), 'alvo', f(650, 1000))
