# Teaser helicóptero Sabiá — roteiro

Referência: reel do Bradesco (helicóptero vermelho leva um contêiner da marca pela cidade e termina em "05/11").
Versão Sabiá: helicóptero e contêiner no **laranja intenso (#F34500)**, contêiner só com o **ícone branco** do sabiá,
pouso no **heliponto de uma torre de escritórios**, final em tela preta com **16/11**.

Vertical 1080×1920, ~16 s.

| Tempo | Cena | O que acontece | Câmera |
|---|---|---|---|
| 0–3,5 s | 1. Decolagem | Helicóptero laranja ergue o contêiner laranja do telhado de um prédio, no meio de uma metrópole ao entardecer | drone subindo devagar |
| 3,5–7 s | 2. Voo entre prédios | O helicóptero atravessa os arranha-céus, o contêiner balança de leve no cabo | acompanha de lado |
| 7–10 s | 3. Logo em destaque | O contêiner passa perto da câmera; o ícone branco aparece grande e nítido | de baixo, contra o céu |
| 10–12,5 s | 4. Pouso | O contêiner desce no heliponto no topo de uma torre e toca o chão | de cima, quase vertical |
| 12,5–16 s | 5. Data | Tela preta, "16/11" em branco (Megion), some no fim | — |

## Como as cenas são feitas

1. **Imagens-chave** (Nano Banana Pro, 2 créditos cada): uma imagem parada por cena, com o ícone da referência
   `referencias\icone-branco-sobre-laranja.png` pintado no contêiner. Ficam em `quadros\`.
2. **Animação** (Kling 4.0, imagem → vídeo, 1080p): cada imagem-chave vira um clipe de 5 s. Ficam em `clipes\`.
3. **Montagem** no HyperFrames (`index.html`): corta os melhores trechos, junta, põe som e o final 16/11.

Os textos enviados para a IA (em inglês, porque ela entende melhor) estão em `prompts\`.
