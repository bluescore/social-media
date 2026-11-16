# Prepara as camadas das capas a partir dos ORIGINAIS em alta resolução do episódio 1.
# Só LÊ o projeto do episódio; tudo o que sai vai para assets/img/ desta pasta.
#   - recortes de fundo já no tamanho da área da foto (1080 x 1030) e desfocados (profundidade);
#   - as figuras recortadas (PNG transparente) copiadas como estão (nunca espelhadas).
# Rodar de dentro de clinicas-ep01-capa:  python fonte/scripts/preparar-camadas.py
from pathlib import Path

from PIL import Image, ImageFilter

EP = Path(r"C:\social-media\hyperframes\clinicas-ep01-protocolo-implante\fonte\geradas")
OUT = Path(__file__).resolve().parents[2] / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

FOTO_W, FOTO_H = 1080, 1030  # área da foto na capa (y 890 a 1920)


def fundo(origem, x0, x1, y0, desfoque, nome):
    """Recorta a região (x0..x1, a partir de y0) com a proporção da área da foto, reduz e desfoca."""
    im = Image.open(EP / origem).convert("RGB")
    largura = x1 - x0
    altura = round(largura * FOTO_H / FOTO_W)
    im = im.crop((x0, y0, x1, y0 + altura)).resize((FOTO_W, FOTO_H), Image.LANCZOS)
    if desfoque:
        im = im.filter(ImageFilter.GaussianBlur(desfoque))
    im.save(OUT / nome, quality=95, subsampling=0)
    print(nome, (x0, y0, x1, y0 + altura), "desfoque", desfoque)


def copia_png(origem, nome):
    Image.open(EP / origem).save(OUT / nome, optimize=True)
    print(nome, "copiado")


# Fotos da noite (capas A, A2 e B): a Helena de pé ao lado do tripé, na maquete.
# Recorte x 70-1400 / a partir de y 440: fica de fora a moldura de madeira da maquete (a borda de cima, que fazia a
# mancha escura no canto de cima à esquerda, e os postes dos lados). Assim a emenda com o bloco laranja fica limpa.
fundo("maquete-larga-noite.png", 70, 1400, 440, 12, "fundo-a-noite.jpg")
copia_png("helena-corpo-tripe-v2.png", "helena-noite.png")       # olhos baixos, cansada (A e B)
copia_png("helena-corpo-vira.png", "helena-noite-olha.png")      # mesma cena e luz, olhos abertos, cabeça virada para a esquerda (A2)
copia_png("tripe-celular.png", "tripe-celular.png")

# Foto da tarde (capa C): a Helena parada no consultório, olhando o celular
fundo("consultorio-tarde.png", 100, 1440, 300, 12, "fundo-c-tarde.jpg")
copia_png("helena-parada-celular-1.png", "helena-celular-tarde.png")
