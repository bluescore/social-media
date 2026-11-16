"""Transcreve as tomadas da narração com o Whisper (large-v3, no computador, sem custo) e guarda o tempo de cada palavra.

Serve para duas coisas:
  1. conferir que TODAS as palavras do texto saíram (compara com o texto do SPEC §7);
  2. achar o começo e o fim de cada fala, para cortar só nas pausas.

Uso:   python -I fonte/audio/transcrever.py assets/audio/fontes/narracao-amedeiros-v4-a.mp3 [outra.mp3 ...]
Saída: fonte/audio/<nome>.palavras.json  (palavras com início/fim em segundos) e um resumo no terminal.
"""
import json
import os
import re
import sys
import unicodedata

from faster_whisper import WhisperModel

AQUI = os.path.dirname(os.path.abspath(__file__))

TEXTO = """décima quarta tentativa.
e o vídeo não sai.
a doutora Helena explica a prótese protocolo toda semana, paciente por paciente.
o roteiro sobre implantes está pronto há seis semanas.
a gravação, não.
ela não gravou a décima quinta.
mandou só o roteiro.
cada linha que ela escreveu virou uma cena.
o perfil voltou a andar.
ela mandou o vídeo pra turma.
o roteiro ela já tinha.
no próximo episódio: o que a recepção mais ouve."""


def norm(p):
    p = unicodedata.normalize('NFD', p.lower())
    p = ''.join(c for c in p if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]', '', p)


def comparar(esperado, ouvido):
    """alinhamento simples (distância de edição por palavra) -> lista de erros"""
    a, b = esperado, ouvido
    n, m = len(a), len(b)
    d = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        d[i][0] = i
    for j in range(m + 1):
        d[0][j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    erros, i, j = [], n, m
    while i > 0 or j > 0:
        if i > 0 and j > 0 and d[i][j] == d[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            if a[i - 1] != b[j - 1]:
                erros.append(f'trocou "{a[i - 1]}" por "{b[j - 1]}"')
            i, j = i - 1, j - 1
        elif i > 0 and d[i][j] == d[i - 1][j] + 1:
            erros.append(f'faltou "{a[i - 1]}"')
            i -= 1
        else:
            erros.append(f'sobrou "{b[j - 1]}"')
            j -= 1
    return erros[::-1]


modelo = WhisperModel('large-v3', device='cpu', compute_type='int8')  # a placa de vídeo não tem a cuBLAS instalada
esperado = [norm(p) for p in TEXTO.split() if norm(p)]
for caminho in sys.argv[1:]:
    segs, _ = modelo.transcribe(caminho, language='pt', word_timestamps=True, beam_size=5,
                                vad_filter=False, condition_on_previous_text=False)
    palavras = []
    for s in segs:
        for w in s.words:
            palavras.append({'palavra': w.word.strip(), 'inicio': round(w.start, 3), 'fim': round(w.end, 3),
                             'confianca': round(w.probability, 3)})
    ouvido = [norm(w['palavra']) for w in palavras if norm(w['palavra'])]
    erros = comparar(esperado, ouvido)
    nome = os.path.splitext(os.path.basename(caminho))[0]
    with open(os.path.join(AQUI, nome + '.palavras.json'), 'w', encoding='utf-8') as f:
        json.dump({'arquivo': caminho, 'modelo': 'faster-whisper large-v3', 'erros': erros, 'palavras': palavras},
                  f, ensure_ascii=False, indent=1)
    print(f'\n== {nome}: {len(ouvido)} palavras ouvidas de {len(esperado)}; diferenças: {erros or "nenhuma"}')
    print(' '.join(f"{w['palavra']}[{w['inicio']:.2f}-{w['fim']:.2f}]" for w in palavras))
