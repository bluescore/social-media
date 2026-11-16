"""Escreve as <img> de cada janela dentro de compositions/fachada.html (entre as marcas janelas:inicio/fim).

Lê fonte/janelas.json (gerado por fonte/janelas.py). Rode de novo sempre que regenerar as janelas.
Uso: python -I fonte/montar-janelas.py
"""
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(AQUI)
cena = os.path.join(PECA, 'compositions', 'fachada.html')
dados = json.load(open(os.path.join(AQUI, 'janelas.json'), encoding='utf-8'))

linhas = []
for j in dados['janelas']:
    alvo = ' data-alvo="1"' if j['alvo'] else ''
    linhas.append(
        f'      <img id="{j["id"]}" class="janela" data-motion-blur="off" src="assets/img/janelas/{j["id"]}.png" alt=""{alvo} '
        f'style="left: {j["x"]}px; top: {j["y"]}px; width: {j["w"]}px; height: {j["h"]}px" />')

html = open(cena, encoding='utf-8').read()
novo = re.sub(r'(<!-- janelas:inicio -->\n).*?(\s*<!-- janelas:fim -->)',
              lambda m: m.group(1) + '\n'.join(linhas) + m.group(2), html, flags=re.S)
open(cena, 'w', encoding='utf-8').write(novo)
print(f'{len(linhas)} janelas escritas em {cena}')
