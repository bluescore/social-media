# -*- coding: utf-8 -*-
"""
LEGENDAS E LETTERING do ep. 01 v4 (sala de espera) -> compositions/legendas.html

O que faz: lê o tempo de cada palavra da locução (assets/audio/voz-v4.palavras.json, tempos do EPISÓDIO)
e escreve compositions/legendas.html com todas as legendas já "assadas": tempos fixos no HTML, sem fetch,
sem nada aleatório. Rodar de novo dá o mesmo arquivo.

Como rodar (de qualquer pasta):
    python -I fonte/scripts/gerar-legendas.py

Dois estilos (marca Sabiá Lab: Helvetica Now Text, minúsculas, branco quente #f6f4f1, sem ponto final):
  - LEGENDA  (padrão): 62 px, Regular com 1-2 palavras-chave em Bold. v4 (pedido 1 do dono): SEMPRE UMA LINHA SÓ,
                       CENTRALIZADA no quadro (centro em x 540, largura máx. 864 px). Fala longa = vários pedaços de
                       uma linha, quebrados em grupos de sentido. Cada pedaço entra 0,05 s antes da 1ª palavra
                       (opacidade + sobe 14 px em 0,18 s); as palavras ainda não ditas ficam a 40% e cada uma acende
                       quando é dita (karaokê sutil); sai quando entra o próximo pedaço (troca rápida, 0,08 s, dentro
                       da mesma fala) ou 0,25 s depois da última palavra (o último pedaço da fala).
                       Faixa padrão: embaixo, com o pé do texto em y 1330.
  - LETTERING (destaque): 100 px (o mesmo tamanho do lettering de s04b), palavra por palavra, no alto da área
                       segura, alinhado à esquerda em x 108 (igual à v3), com o véu em degradê no alto do quadro.
Números na tela em algarismos (pedido 2 do dono): 14ª, 6, 17, 15ª. A voz continua falando por extenso
(o mapa ALGARISMOS liga o que aparece às palavras faladas).

Falas que NÃO estão aqui (o lettering delas mora dentro da cena, para não ter texto duplicado):
  T  -> s04b-take15.html · 11, 12, 13 -> s11-tarde.html · 14 -> s12-cartao.html
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PROJETO = os.path.normpath(os.path.join(AQUI, "..", ".."))
ARQ_PALAVRAS = os.path.join(PROJETO, "assets", "audio", "voz-v4.palavras.json")
ARQ_SAIDA = os.path.join(PROJETO, "compositions", "legendas.html")
FONTE_REG = os.path.join(PROJETO, "assets", "fonts", "HelveticaNowText-Regular.ttf")
FONTE_BOLD = os.path.join(PROJETO, "assets", "fonts", "HelveticaNowText-Bold.ttf")

# =====================================================================================================
# PLANO — cada fala -> pedaços. Uma entrada = um pedaço na tela.
#   fala:    id da fala no voz-v4.palavras.json
#   de/ate:  quais palavras da fala entram neste pedaço (índices; ate exclusivo). Sem isso = a fala inteira.
#   estilo:  "legenda" ou "lettering"
#   linhas:  o texto na tela. LEGENDA: exatamente 1 linha (v4). LETTERING: até 2 linhas. **assim** = Bold.
#            Sem ponto final. Números em algarismos (ver ALGARISMOS).
#   pos:     "baixo" (pé do texto em y 1330), "alto" (topo em y 204) ou {"pe": y} / {"topo": y} para um pedaço
#            que precisa fugir do que está na cena (a legenda continua centralizada; só a altura muda).
#   veu:     True = uma sombra escura suave do tamanho do texto, atrás só deste pedaço (fundo claro).
#   sai_ate: (opcional) o pedaço sai no máximo neste tempo do episódio (ex.: junto com um corte da cena).
#   sai_dur: (opcional) duração da saída deste pedaço (padrão 0,15 s).
#   entra_min: (opcional) o pedaço não entra antes deste tempo do episódio (ex.: esperar um texto da cena sair dali).
#   obs:     por que está assim (o que tem na tela embaixo).
# =====================================================================================================
PLANO = [
    dict(fala="1", estilo="lettering", linhas=["**14ª** tentativa"], pos="alto",
         obs="s01: alto, sobre a janela escura desfocada; o celular começa em y~430 e o painel 'apagar vídeo?' fica no "
             "meio da tela. v4: '14ª' em algarismo (antes 'décima quarta / tentativa', 2 linhas); cabe numa linha"),
    dict(fala="2", estilo="legenda", linhas=["e o vídeo **não sai**"], pos="baixo",
         obs="s01: o pé do celular e o tripé"),
    dict(fala="3", de=0, ate=4, estilo="legenda", linhas=["a doutora Helena explica"], pos="baixo", veu=True,
         obs="s01: o recuo que revela a maquete; embaixo passa o jaleco claro dela, desfocado -> sombra atrás"),
    dict(fala="3", de=4, ate=7, estilo="legenda", linhas=["a **prótese protocolo**"], pos="baixo", veu=True,
         obs="s01: o recuo continua; o jaleco claro ainda passa embaixo -> sombra atrás"),
    dict(fala="3", de=7, ate=9, estilo="legenda", linhas=["toda semana,"], pos="baixo",
         obs="s01: a maquete inteira, o chão"),
    dict(fala="3", de=9, ate=12, estilo="legenda", linhas=["**paciente por paciente**"], pos="baixo",
         obs="s01: a maquete inteira, o chão"),
    dict(fala="4", de=0, ate=4, estilo="legenda", linhas=["o roteiro sobre implantes"], pos="baixo", veu=True,
         obs="s03: a parte vazia da folha (papel claro) -> sombra atrás"),
    dict(fala="4", de=4, ate=9, estilo="legenda", linhas=["está **pronto** há 6 semanas"], pos="baixo", veu=True,
         obs="s03: a parte vazia da folha (papel claro) -> sombra atrás; '6' em algarismo (v4)"),
    dict(fala="5", estilo="lettering", linhas=["a gravação, **não**"], pos="alto",
         obs="s03: alto, sobre a bancada; a caneta risca 'gravar 06/11' mais abaixo (y~600)"),
    dict(fala="F", estilo="legenda", linhas=["**17 dias** sem postar nada"], pos={"pe": 920}, veu=True,
         obs="s04: a etiqueta 'último post · há 17 dias' ocupa y 1158-1278 e os textos dos posts sobem com a rolagem "
             "(15,43-16,30) -> a legenda fica em y 861-920, no alto da 2ª linha da grade, onde nenhum texto passa. "
             "v4: fala nova 'dezessete dias' -> '17 dias'"),
    dict(fala="6", estilo="legenda", linhas=["ela **não gravou** a 15ª"], pos="alto", veu=True,
         sai_ate=23.27, sai_dur=0.07,
         obs="s05: embaixo está a cabeça dela (y 1135-1510) -> alto, sobre a bancada; sai junto com o obturador "
             "(fecha 23,20-23,27), porque depois vem a conversa com 'Claude' no alto. v4: '15ª' em algarismo, 1 linha"),
    dict(fala="7", estilo="legenda", linhas=["mandou só o **roteiro**"], pos="baixo",
         obs="s05: a conversa escura; 'enviado · 23:52' fica em y~1135-1180 à direita, acima da legenda"),
    dict(fala="8", de=0, ate=5, estilo="legenda", linhas=["cada linha que ela escreveu"], pos="baixo", veu=True,
         obs="virada: a parte vazia da folha (papel claro) -> sombra atrás; o fio lê as linhas mais acima"),
    dict(fala="8", de=5, ate=8, estilo="legenda", linhas=["virou uma **cena**"], pos="baixo", veu=True,
         obs="virada: a folha começa a dobrar; sombra atrás"),
    dict(fala="9", estilo="legenda", linhas=["o perfil voltou a **andar**"], pos="baixo", veu=True, entra_min=47.05, apagada=0.75,
         obs="s09: o lettering no alto brigava com o título do vídeo dela ('a prótese é parafusada…'), que ainda está "
             "grande e encolhendo no alto entre 47,0 e 47,4 -> legenda embaixo, numa linha; embaixo fica o corpo "
             "escuro do vídeo e depois o suporte claro do celular -> sombra atrás; entra em 47,05 (como na v3)"),
    dict(fala="10", de=0, ate=4, estilo="legenda", linhas=["ela mandou o vídeo"], pos={"pe": 1342},
         obs="s10 v4 (conversa com a Lúcia): o vídeo encaminhado ocupa x 554-884, y 687-1274, bem em cima da faixa; "
             "com o pé em 1330 o acento de 'vídeo' ficava a ~8 px do balão -> pé 12 px mais baixo (1342), ~20 px de folga; "
             "nada mais passa na faixa até 54,90"),
    dict(fala="10", de=4, ate=6, estilo="legenda", linhas=["pra **Lúcia**"], pos={"pe": 1342},
         obs="s10 v4: às 54,90 entram os 3 pontinhos 'digitando' em x 196-316, y 1312-1376 -> a fala foi quebrada aqui "
             "para este pedaço ser curto e centralizado (x ~417-663), sem encostar neles; sai 0,25 s depois de "
             "'Lúcia' (55,42), antes da resposta dela (55,50, y 1312-1452); mesma altura do pedaço anterior"),
]

# números escritos em algarismos na tela: o que aparece -> as palavras faladas
ALGARISMOS = {
    "14ª": ["décima", "quarta"],
    "15ª": ["décima", "quinta"],
    "6": ["seis"],
    "17": ["dezessete"],
}

# ---- medidas e estilo
X = 108           # margem esquerda (lettering) e começo da faixa da legenda
LARGURA_MAX = 864  # a legenda é centralizada nesta faixa: x 108-972, centro em x 540
PE_PADRAO = 1330
TOPO_ALTO = 204
LEG_PX, LEG_ENTRELINHA, LEG_TRACK = 62, 0.95, -0.04
LET_PX, LET_ENTRELINHA, LET_TRACK = 100, 0.9, -0.05
ANTES = 0.05      # o pedaço entra 0,05 s antes da 1ª palavra
DEPOIS = 0.25     # e sai 0,25 s depois da última
ENTRA = 0.18      # duração da entrada da legenda
SAI = 0.15        # duração da saída (último pedaço de cada fala)
TROCA = 0.05      # duração da saída quando o próximo pedaço é da MESMA fala (troca rápida no meio da frase)
APAGADA = 0.4     # opacidade das palavras ainda não ditas (karaokê)
ACENDE = 0.10     # quanto a palavra leva para acender
LET_PALAVRA = 0.22  # cada palavra do lettering entra em 0,22 s, subindo 16 px (como em s04b)


def norm(s):
    s = s.lower()
    for c in ".,;:!?…\"'":
        s = s.replace(c, "")
    return s.replace("...", "").strip()


def tokens_da_linha(linha):
    """'e o vídeo **não sai**' -> [('e',False),('o',False),('vídeo',False),('não',True),('sai',True)]"""
    out, negrito = [], False
    for t in linha.split():
        abre = t.startswith("**")
        if abre:
            t = t[2:]
            negrito = True
        fecha = t.endswith("**")
        if fecha:
            t = t[:-2]
        out.append((t, negrito))
        if fecha:
            negrito = False
    return out


def alinhar(tokens, palavras, rotulo):
    """Casa cada palavra da tela com a(s) palavra(s) faladas, pela POSIÇÃO (nunca pelo texto solto)."""
    tempos, i = [], 0
    for t, _ in tokens:
        alvo = ALGARISMOS.get(norm(t), [norm(t)])
        grupo = palavras[i:i + len(alvo)]
        if [norm(p["palavra"]) for p in grupo] != alvo:
            sys.exit(f"[{rotulo}] a palavra da tela '{t}' não casa com a fala: {[p['palavra'] for p in grupo]}")
        tempos.append((grupo[0]["inicio"], grupo[-1]["fim"]))
        i += len(alvo)
    if i != len(palavras):
        sys.exit(f"[{rotulo}] sobraram palavras faladas sem legenda: {[p['palavra'] for p in palavras[i:]]}")
    return tempos


def medidor():
    """Largura do texto pela própria fonte (avanço de cada letra + o espaçamento negativo), para garantir <= 864 px."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return None
    fontes = {}
    for nome, arq in (("reg", FONTE_REG), ("bold", FONTE_BOLD)):
        f = TTFont(arq)
        fontes[nome] = (f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm)

    def largura(tokens, px, track):
        total = 0.0
        for k, (t, negrito) in enumerate(tokens):
            cmap, hmtx, upm = fontes["bold" if negrito else "reg"]
            texto = t + (" " if k < len(tokens) - 1 else "")
            for ch in texto:
                g = cmap.get(ord(ch))
                adv = hmtx[g][0] if g else upm * 0.5
                total += adv * px / upm + track * px
        return total

    return largura


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def main():
    dados = json.load(open(ARQ_PALAVRAS, encoding="utf-8"))
    falas = {f["id"]: f for f in dados["falas"]}
    largura = medidor()

    # 1) monta os pedaços com os tempos
    pedacos = []
    for n, p in enumerate(PLANO):
        fala = falas[p["fala"]]
        de, ate = p.get("de", 0), p.get("ate", len(fala["palavras"]))
        palavras = fala["palavras"][de:ate]
        linhas = [tokens_da_linha(l) for l in p["linhas"]]
        if p["estilo"] == "legenda" and len(linhas) != 1:
            sys.exit(f"[fala {p['fala']}] a legenda tem de ser UMA linha só (v4); quebre em mais pedaços")
        if len(linhas) > 2:
            sys.exit(f"[fala {p['fala']}] linhas demais")
        planas = [tk for l in linhas for tk in l]
        tempos = alinhar(planas, palavras, f"fala {p['fala']}")
        px = LET_PX if p["estilo"] == "lettering" else LEG_PX
        track = LET_TRACK if p["estilo"] == "lettering" else LEG_TRACK
        larguras = [largura(l, px, track) for l in linhas] if largura else []
        if larguras and max(larguras) > LARGURA_MAX:
            sys.exit(f"[fala {p['fala']}] linha larga demais: {max(larguras):.0f} px > {LARGURA_MAX}")
        pedacos.append(dict(p, n=n, linhas_tk=linhas, tempos=tempos, larguras=larguras,
                            entra=round(max(tempos[0][0] - ANTES, p.get("entra_min", 0)), 3), fim_voz=tempos[-1][1]))
    # 1b) revisão v4: o pedaço seguinte da MESMA fala entra exatamente na 1ª palavra dele (sem os 0,05 s de antes),
    #     para o anterior não começar a sumir antes de a última palavra dele acabar
    for k in range(1, len(pedacos)):
        if pedacos[k]["fala"] == pedacos[k - 1]["fala"]:
            pedacos[k]["entra"] = round(max(pedacos[k]["tempos"][0][0], pedacos[k].get("entra_min", 0)), 3)
    # 2) a saída: 0,25 s depois da última palavra, ou quando entra o próximo pedaço (nunca dois ao mesmo tempo)
    for k, p in enumerate(pedacos):
        sai = p["fim_voz"] + DEPOIS
        mesma_fala = False
        if k + 1 < len(pedacos):
            prox = pedacos[k + 1]
            sai = min(sai, prox["entra"])
            mesma_fala = prox["fala"] == p["fala"]
        if "sai_ate" in p:
            sai = min(sai, p["sai_ate"])
        p["sai"] = round(sai, 3)
        p["sai_dur"] = p.get("sai_dur", TROCA if mesma_fala else SAI)
        if p["sai"] - p["sai_dur"] < p["entra"] + ENTRA:
            sys.exit(f"[fala {p['fala']}] pedaço curto demais")

    # 3) escreve o HTML
    css_pos, html, js = [], [], []
    for p in pedacos:
        pid = f"lg{p['n'] + 1:02d}"
        p["id"] = pid
        let = p["estilo"] == "lettering"
        pos = p["pos"]
        if pos == "baixo":
            regra = f"bottom: {1920 - PE_PADRAO}px;"
        elif pos == "alto":
            regra = f"top: {TOPO_ALTO}px;"
        elif "pe" in pos:
            regra = f"bottom: {1920 - pos['pe']}px;"
        else:
            regra = f"top: {pos['topo']}px;"
        css_pos.append(f"    #{pid} {{ {regra} }}")
        if p.get("apagada"):
            # revisão v4: palavras ainda não ditas mais visíveis neste pedaço (fundo claro/movimentado embaixo)
            css_pos.append(f"    #{pid} .w {{ opacity: {p['apagada']}; }}")

        partes, w = [], 0
        for li, linha in enumerate(p["linhas_tk"]):
            if li:
                partes.append("<br />")
            for k, (t, negrito) in enumerate(linha):
                tag = "b" if negrito else "span"
                partes.append(f'<{tag} id="{pid}-p{w}" class="w">{esc(t)}</{tag}>')
                if k < len(linha) - 1:
                    partes.append(" ")
                w += 1
        texto_tela = " / ".join(" ".join(t for t, _ in l) for l in p["linhas_tk"])
        html.append(f"    <!-- fala {p['fala']} · {p['estilo']} · {p['entra']:.3f}–{p['sai']:.3f} s · {texto_tela} -->")
        if let:
            html.append(f'    <div id="{pid}-veu" class="veu-alto"></div>')
            html.append(f'    <div id="{pid}" class="let">{"".join(partes)}</div>')
        else:
            # legenda: a faixa (x 108-972) centraliza a linha; a sombra fica dentro da linha, do tamanho do texto
            sombra = '<span class="sombra"></span>' if p.get("veu") else ""
            html.append(f'    <div id="{pid}" class="leg"><span class="linha">{sombra}{"".join(partes)}</span></div>')

        js.append(f"      // fala {p['fala']}: \"{texto_tela}\" ({p['estilo']}) — entra {p['entra']:.3f}, sai {p['sai']:.3f}")
        if let:
            js.append(f'      tl.fromTo("#{pid}-veu", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power1.out" }}, {p["entra"]:.3f});')
            for i, (ini, _) in enumerate(p["tempos"]):
                t = ini  # cada palavra entra quando é dita (como nos letterings de s04b, s11 e s12)
                js.append(f'      tl.fromTo("#{pid}-p{i}", {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: {LET_PALAVRA}, ease: "power2.out" }}, {t:.3f});')
            js.append(f'      tl.to("#{pid}", {{ opacity: 0, duration: {p["sai_dur"]}, ease: "power1.in" }}, {p["sai"] - p["sai_dur"]:.3f});')
            js.append(f'      tl.to("#{pid}-veu", {{ opacity: 0, duration: 0.2, ease: "power1.in" }}, {p["sai"] - 0.2:.3f});')
        else:
            js.append(f'      tl.fromTo("#{pid}", {{ opacity: 0, y: 14 }}, {{ opacity: 1, y: 0, duration: {ENTRA}, ease: "power2.out" }}, {p["entra"]:.3f});')
            for i, (ini, _) in enumerate(p["tempos"]):
                js.append(f'      tl.to("#{pid}-p{i}", {{ opacity: 1, duration: {ACENDE}, ease: "none" }}, {ini:.3f});')
            js.append(f'      tl.to("#{pid}", {{ opacity: 0, duration: {p["sai_dur"]}, ease: "power1.in" }}, {p["sai"] - p["sai_dur"]:.3f});')
        js.append(f'      tl.set("#{pid}", {{ visibility: "hidden" }}, {p["sai"]:.3f});')

    saida = MODELO.format(css_pos="\n".join(css_pos), html="\n".join(html), js="\n".join(js),
                          X=X, LMAX=LARGURA_MAX, LEG_PX=LEG_PX, LEG_LH=LEG_ENTRELINHA, LEG_TR=LEG_TRACK,
                          LET_PX=LET_PX, LET_LH=LET_ENTRELINHA, LET_TR=LET_TRACK, APAGADA=APAGADA)
    with open(ARQ_SAIDA, "w", encoding="utf-8", newline="\n") as f:
        f.write(saida)

    # 4) conferência no terminal
    print(f"escrito: {ARQ_SAIDA}")
    for p in pedacos:
        lg = "/".join(f"{x:.0f}" for x in p["larguras"])
        if p["estilo"] == "legenda" and p["larguras"]:
            w = p["larguras"][0]
            faixa_x = f"x {540 - w / 2:.0f}-{540 + w / 2:.0f}"
        else:
            faixa_x = f"x {X}-{X + max(p['larguras'] or [0]):.0f}"
        print(f"  {p['id']} fala {p['fala']:>2} {p['estilo']:<9} entra {p['entra']:6.3f}  sai {p['sai']:6.3f}  "
              f"pos {p['pos']!s:<12} largura {lg} px ({faixa_x})  | {' / '.join(p['linhas'])}")
    # tempos LOCAIS para os blocos // TEMPOS DA LOCUÇÃO das cenas (conferência)
    def ini(fid, i):
        return falas[fid]["palavras"][i]["inicio"]
    print("s04b (fala T, local = ep - 18,3):", [round(w["inicio"] - 18.3, 3) for w in falas["T"]["palavras"]])
    print("s11 (local = ep - 58,5): roteiro", round(ini("11", 0) - 58.5, 3), "papel", round(ini("12", 0) - 58.5, 3),
          "explica", round(ini("13", 0) - 58.5, 3), "existe ('o seu')", round(ini("13", 8) - 58.5, 3))
    print("s12 (local = ep - 66,9): comente", round(ini("14", 0) - 66.9, 3), "clinica", round(ini("14", 1) - 66.9, 3),
          "como ('e a gente')", round(ini("14", 2) - 66.9, 3))


MODELO = """<!-- LEGENDAS E LETTERING da locução (0 a 71,7 s do episódio), por cima de tudo.
     GERADO por fonte/scripts/gerar-legendas.py a partir de assets/audio/voz-v4.palavras.json — não edite à mão:
     mude o PLANO no topo do script e rode de novo (python -I fonte/scripts/gerar-legendas.py).
     LEGENDA (v4): 62 px, UMA linha só, centralizada no quadro; fala longa = vários pedaços de uma linha; cada palavra
     acende quando é dita. LETTERING: 100 px, palavra por palavra, no alto, alinhado à esquerda (como na v3).
     Números em algarismos (14ª, 6, 17, 15ª); a voz fala por extenso.
     A fala T está no lettering de s04b; 11, 12 e 13 no lettering de s11; 14 no cartão de s12 (não se repetem aqui). -->
<template>
  <style>
    @font-face {{
      font-family: "Helvetica Now Text";
      src: url("assets/fonts/HelveticaNowText-Regular.ttf") format("truetype");
      font-weight: 400;
    }}
    @font-face {{
      font-family: "Helvetica Now Text";
      src: url("assets/fonts/HelveticaNowText-Bold.ttf") format("truetype");
      font-weight: 700;
    }}
    #root {{
      position: absolute;
      inset: 0;
      background: transparent;
      pointer-events: none;
      font-family: "Helvetica Now Text", Helvetica, Arial, sans-serif;
    }}
    /* LEGENDA (v4): uma linha, centralizada na faixa x {X}-972 (centro em x 540, largura até {LMAX} px).
       LETTERING: alinhado à esquerda em x {X}, a caixa tem a largura do texto. */
    .leg,
    .let {{
      position: absolute;
      left: {X}px;
      white-space: nowrap;
      color: #f6f4f1;
      font-weight: 400;
      text-shadow: 0 3px 22px rgba(20, 12, 10, 0.75), 0 1px 3px rgba(20, 12, 10, 0.6);
    }}
    .let {{
      width: max-content;
      max-width: {LMAX}px;
      isolation: isolate;
    }}
    .leg {{
      width: {LMAX}px;
      text-align: center;
      font-size: {LEG_PX}px;
      line-height: {LEG_LH};
      letter-spacing: {LEG_TR}em;
      opacity: 0;
    }}
    /* a linha da legenda: caixa do tamanho do texto, centralizada (a sombra fica dentro dela) */
    .linha {{
      position: relative;
      display: inline-block;
      isolation: isolate;
    }}
    .leg .w {{
      opacity: {APAGADA};
    }}
    .let {{
      font-size: {LET_PX}px;
      line-height: {LET_LH};
      letter-spacing: {LET_TR}em;
    }}
    .let .w {{
      display: inline-block;
      opacity: 0;
    }}
    .leg b,
    .let b {{
      font-weight: 700;
    }}
    /* sombra escura suave do tamanho do texto (só nos pedaços sobre fundo claro) */
    .sombra {{
      position: absolute;
      left: -18px;
      right: -18px;
      top: -10px;
      bottom: -10px;
      z-index: -1;
      border-radius: 28px;
      background: rgba(20, 12, 10, 0.36);
      box-shadow: 0 0 44px 26px rgba(20, 12, 10, 0.36);
    }}
    /* véu em degradê no alto do quadro, atrás do lettering (o mesmo de s04b e s11) */
    .veu-alto {{
      position: absolute;
      left: 0;
      right: 0;
      top: 0;
      height: 560px;
      background: linear-gradient(180deg, rgba(36, 26, 22, 0.55) 0%, rgba(36, 26, 22, 0.35) 55%, rgba(36, 26, 22, 0) 100%);
      opacity: 0;
    }}
    /* posição de cada pedaço (pé em y 1330 = bottom 590) */
{css_pos}
  </style>

  <div id="root" data-composition-id="legendas" data-width="1080" data-height="1920">
{html}
  </div>

  <script>
    (function () {{
      const tl = gsap.timeline({{ paused: true }});
{js}
      window.__timelines["legendas"] = tl;
    }})();
  </script>
</template>
"""

if __name__ == "__main__":
    main()
