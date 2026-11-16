# Teaser "sombra do sabiá"

Vídeo vertical de 8,5 s. A sombra de um sabiá pousa num galho, numa parede de luz suave no laranja da marca (mesma luminosidade do vídeo de referência, que era azul). A luz baixa e fica "em breve".

## Roteiro

| Tempo | O que acontece |
|---|---|
| 0–1,4 s | galho vazio; a luz da parede vai abrindo |
| 1,4 s | o sabiá entra pelo alto, rápido |
| 1,55–2,35 s | freia, toca o galho e assenta (câmera lenta 2x) |
| 3,9 s | abre e fecha a asa e vira a cabeça |
| 5,3–6,7 s | a luz baixa para um laranja queimado profundo (sem ir ao preto) |
| 5,9 s até o fim | "em breve" (Helvetica Now Text, caixa baixa) |

## De onde vem a sombra

- Filmagem real gratuita do Pixabay (licença do Pixabay: uso comercial liberado, sem crédito obrigatório):
  https://pixabay.com/videos/blackbird-tree-pine-fauna-bird-132632/. Cópia em `fonte/pixabay-132632_sabia.mp4`.
- O pássaro é do mesmo gênero do sabiá-laranjeira (*Turdus*; o Pixabay chama de "blackbird", melro), filmado contra um céu branco.
- No vídeo original ele **levanta voo**. Aqui o trecho é tocado **de trás para frente**, o que vira um pouso.

## Como a sombra foi feita (`fonte/gerar-sombra.py`)

1. Recorte vertical do original (x 299–996, altura inteira), ampliado 1,55x e em tons de cinza.
2. O céu (branco) vira parede, e tudo que é escuro (pássaro, galho, folhas) vira sombra em laranja queimado escuro.
3. Rampa de velocidade com o vídeo tocado de trás para frente: galho parado, entrada rápida, freada e pouso em câmera lenta 2x, pousado em tempo real. Uma fusão de 0,3 s aos 3,3 s pula um trecho parado e leva até o gesto de asa.
4. Borrão de movimento só no pássaro; o galho fica nítido, sem "fantasma".
5. Profundidade: a folhagem do alto e a base do galho ficam mais desfocadas, como se estivessem mais longe da parede, e a base some aos poucos.
6. Resultado: `assets/video/sombra-sabia.mp4`. Na cena, esse vídeo é multiplicado sobre a parede em degradê diagonal, com grão de filme suave, pretos levantados (nada fica preto puro) e aproximação lenta da câmera.

Para refazer:
1. Extraia os quadros:
   `ffmpeg -ss 16.5 -i fonte/pixabay-132632_sabia.mp4 -t 8.25 -vf "crop=697:1080:299:0,scale=1080:1674:flags=lanczos,format=gray" -fps_mode passthrough quadros/%04d.png`
2. Gere a sombra: `python fonte/gerar-sombra.py quadros saida`.
3. Junte `saida/%04d.png` num MP4 a 30 fps.
