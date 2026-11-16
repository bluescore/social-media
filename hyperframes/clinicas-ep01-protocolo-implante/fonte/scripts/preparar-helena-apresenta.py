# Prepara as 3 poses da Helena "apresentando" (tela dividida do vídeo dela, cena s08).
# As imagens da OpenAI já vêm com fundo transparente, do mesmo tamanho (1024x1536) e com a cabeça
# no mesmo lugar nas três (conferido: diferença de até 3 px), então NÃO cortamos nem deslocamos nada:
# as três ficam sobrepostas no mesmo lugar e a troca de pose só mexe nos braços.
# Aqui só limpamos a cor dos pixels 100% transparentes (evita "auréola" ao reduzir) e salvamos em assets/img/.
# Não espelha nada (faixa grisalha à esquerda da imagem = têmpora DIREITA dela; relógio à direita da imagem = pulso ESQUERDO dela).
# Rodar dentro da pasta do episódio: python -I fonte/scripts/preparar-helena-apresenta.py
import sys
sys.path.append(r"C:\Users\YagoBittencourt\AppData\Roaming\Python\Python313\site-packages")
import numpy as np
from PIL import Image

for pose in "abc":
    im = Image.open(f"fonte/geradas/helena-apresenta-{pose}.png").convert("RGBA")
    arr = np.asarray(im).copy()
    arr[arr[..., 3] == 0, :3] = 0
    Image.fromarray(arr).save(f"assets/img/helena-apresenta-{pose}.png", optimize=True)
    a = arr[..., 3]
    ys, xs = np.where(a > 128)
    print(f"pose {pose}: {im.size}  figura x {xs.min()}-{xs.max()}  y {ys.min()}-{ys.max()}")
