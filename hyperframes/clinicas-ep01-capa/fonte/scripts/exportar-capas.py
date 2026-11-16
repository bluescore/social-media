# Exporta as 4 capas e as prévias de comparação a partir dos quadros tirados pelo HyperFrames.
# Antes:  npx --yes hyperframes@0.8.216 snapshot --at 0.5,1.5,2.5,3.5 --no-end -o renders/_quadros
# Depois: python fonte/scripts/exportar-capas.py
#   renders/capa-A.png / .jpg, capa-A2..., capa-B..., capa-C...  (1080x1920; o PNG é o quadro sem perda, o JPG é qualidade 95)
#   renders/previa-grade.jpg  = referência do dono + as 4 capas como aparecem na grade (miolo 3:4, y 240-1680)
#   renders/previa-reels.jpg  = referência do dono + as 4 capas inteiras (como na aba de Reels / tela cheia)
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parents[2]
QUADROS = RAIZ / "renders" / "_quadros"
SAIDA = RAIZ / "renders"
REF = RAIZ / "fonte" / "referencia-dono.png"
FONTE = RAIZ / "assets" / "fonts" / "HelveticaNowText-Regular.ttf"
NEGRITO = RAIZ / "assets" / "fonts" / "HelveticaNowText-Bold.ttf"

# letra da capa -> (número do quadro, segundo do snapshot)
QUADRO = {"A": (0, "0.5"), "A2": (1, "1.5"), "B": (2, "2.5"), "C": (3, "3.5")}

capas = {}
for letra, (i, t) in QUADRO.items():
    im = Image.open(QUADROS / f"frame-{i:02d}-at-{t}s.png").convert("RGB")
    assert im.size == (1080, 1920), im.size
    im.save(SAIDA / f"capa-{letra}.png", optimize=True)
    im.save(SAIDA / f"capa-{letra}.jpg", quality=95, subsampling=0)
    capas[letra] = im
    print("capa", letra, "salva")

ref = Image.open(REF).convert("RGB")
rotulos = {
    "ref": ("Referência (Nubank)", "print que o dono mandou"),
    "A": ("A · O vídeo que ela não gravou", "noite · olhos baixos, cansada"),
    "A2": ("A2 · O vídeo que ela não gravou", "noite · olhos abertos, olhando a tela"),
    "B": ("B · Ela apagou a 14ª tentativa", "a foto da A com o título da B"),
    "C": ("C · O vídeo que ela não gravou", "tarde · sorrindo para o celular"),
}
f_rot = ImageFont.truetype(str(NEGRITO), 24)
f_sub = ImageFont.truetype(str(FONTE), 21)
f_nota = ImageFont.truetype(str(FONTE), 22)


def painel(imagens, altura, nome, nota):
    """Coloca as imagens lado a lado na mesma altura, com rótulo embaixo de cada uma."""
    margem, vao, faixa = 40, 28, 92
    redim = []
    for chave, im in imagens:
        w = round(im.width * altura / im.height)
        redim.append((chave, im.resize((w, altura), Image.LANCZOS)))
    largura = margem * 2 + sum(i.width for _, i in redim) + vao * (len(redim) - 1)
    folha = Image.new("RGB", (largura, margem + altura + faixa + 40), (246, 244, 241))
    d = ImageDraw.Draw(folha)
    x = margem
    for chave, im in redim:
        folha.paste(im, (x, margem))
        d.rectangle([x - 1, margem - 1, x + im.width, margem + altura], outline=(210, 205, 200))
        titulo, sub = rotulos[chave]
        d.text((x, margem + altura + 14), titulo, font=f_rot, fill=(24, 24, 24))
        d.text((x, margem + altura + 46), sub, font=f_sub, fill=(110, 100, 98))
        x += im.width + vao
    d.text((margem, margem + altura + faixa), nota, font=f_nota, fill=(110, 100, 98))
    folha.save(SAIDA / nome, quality=92)
    print(nome, folha.size)


ordem = ["A", "A2", "B", "C"]
# grade do perfil: o Instagram mostra o miolo 3:4 da capa 9:16
grade = [("ref", ref)] + [(k, capas[k].crop((0, 240, 1080, 1680))) for k in ordem]
painel(grade, 720, "previa-grade.jpg",
       "Capas como aparecem na grade do perfil (miolo 3:4, y 240-1680). A referência é o print que o dono mandou.")
# aba de Reels / tela cheia: a capa inteira
reels = [("ref", ref)] + [(k, capas[k]) for k in ordem]
painel(reels, 900, "previa-reels.jpg",
       "Capas inteiras (1080x1920), como na aba de Reels e ao abrir o vídeo.")
