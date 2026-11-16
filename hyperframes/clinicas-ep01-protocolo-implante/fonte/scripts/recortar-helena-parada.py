# Recorta a pose nova da Helena (parada, olhando o celular) para a cena 11.
# A imagem da OpenAI já vem com fundo transparente e borda limpa: aqui só cortamos a sobra
# transparente em volta dela (com 8 px de folga) e salvamos em assets/img/.
# Não espelha nada (o relógio fica no pulso ESQUERDO dela).
# Rodar dentro da pasta do episódio: python -I fonte/scripts/recortar-helena-parada.py
import sys
sys.path.append(r"C:\Users\YagoBittencourt\AppData\Roaming\Python\Python313\site-packages")
import numpy as np
from PIL import Image

ORIGEM = "fonte/geradas/helena-parada-celular-1.png"
DESTINO = "assets/img/helena-parada-celular.png"
FOLGA = 8

im = Image.open(ORIGEM).convert("RGBA")
a = np.asarray(im)[..., 3]
ys, xs = np.where(a > 10)
x0, y0 = max(0, xs.min() - FOLGA), max(0, ys.min() - FOLGA)
x1, y1 = min(im.width, xs.max() + 1 + FOLGA), min(im.height, ys.max() + 1 + FOLGA)
corte = im.crop((x0, y0, x1, y1))
# pixels totalmente transparentes ficam pretos e sem cor (evita qualquer "auréola" ao reduzir)
arr = np.asarray(corte).copy()
arr[arr[..., 3] == 0, :3] = 0
Image.fromarray(arr).save(DESTINO, optimize=True)

# medidas úteis para posicionar na cena (em px da imagem recortada)
aa = arr[..., 3]
ys, xs = np.where(aa > 200)
pe = ys.max()
linha_pes = np.where(aa[pe - 40] > 200)[0]
print(f"origem {im.size} corte {corte.size} (x {x0}-{x1}, y {y0}-{y1})")
print(f"figura: x {xs.min()}-{xs.max()}  y {ys.min()}-{pe}")
print(f"pés (40 px acima da sola): x {linha_pes.min()}-{linha_pes.max()}")
