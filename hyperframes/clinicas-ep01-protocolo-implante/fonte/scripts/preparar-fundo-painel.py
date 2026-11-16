"""Fundo do painel da Helena no vídeo dela (s08, tela dividida) — pedido do dono na v5:
"ambientalize o fundo dela pra não ficar só cinza; talvez adicione o próprio cenário da sala da clínica que já temos".

Pega a parede do consultório da maquete (assets/img/consultorio-tarde.jpg: prateleiras com plantas, abajur, janela com
persiana e a cadeira) e desfoca como se a câmera estivesse focada nela (profundidade de campo), um pouco mais escuro
para ela se destacar. Saída: assets/img/fundo-painel-consultorio.jpg (1134 x 882, um pouco maior que o painel 1080 x 840,
para o avanço lento da câmera não mostrar borda).

Feito com o ffmpeg (sem dependências de Python além da biblioteca padrão).
Uso (de dentro da pasta do episódio):  python -I fonte/scripts/preparar-fundo-painel.py
"""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
PECA = os.path.dirname(os.path.dirname(AQUI))
ORIGEM = os.path.join(PECA, 'assets', 'img', 'consultorio-tarde.jpg')
SAIDA = os.path.join(PECA, 'assets', 'img', 'fundo-painel-consultorio.jpg')

LARG, ALT = 1134, 882            # painel 1080 x 840 com 5% de folga
X0, Y0, W, H = 40, 300, 1175, 914  # a parede: plantas, abajur, janela e cadeira (proporção ~1,286, igual à do painel)
DESFOQUE = 9                     # sigma do desfoque gaussiano (px, no tamanho final)
BRILHO = -0.06                   # um pouco mais escuro que a cena original (eq do ffmpeg)
SATURACAO = 0.90

filtro = (f'crop={W}:{H}:{X0}:{Y0},scale={LARG}:{ALT}:flags=lanczos,gblur=sigma={DESFOQUE},'
          f'eq=brightness={BRILHO}:saturation={SATURACAO}')
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', ORIGEM, '-vf', filtro, '-q:v', '2', SAIDA], check=True)
print('->', SAIDA)
