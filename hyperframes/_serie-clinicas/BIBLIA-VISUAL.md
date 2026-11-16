# Bíblia visual — sala de espera

Vale para todos os episódios. O que é só do ep. 01 está em `ep01-SPEC.md` (produção) e `ep01-ROTEIRO.md` (aprovação).

**Direção visual v2 (12/11/2026):** a vida dela é uma maquete de mesa com personagens-boneco; o conteúdo dela é real. A decisão e o porquê estão em `DIRECAO-VISUAL-v2.md`; esta bíblia já está atualizada para ela.

---

## 1. Os três mundos

| | **Mundo 1: a noite dela (o problema) · maquete** | **Mundo 2: o vídeo dela (o entregue) · o real** | **Mundo 3: a tarde (a vida resolvida) · maquete** |
|---|---|---|---|
| O que é | o consultório como **maquete de mesa**: uma caixa com duas paredes e o piso, a borda de madeira à vista, sobre uma mesa de madeira; a personagem-boneco mora dentro dela | 3D técnico **realista**: osso de vidro verde-menta, implantes de titânio, prótese com dentes de porcelana | a mesma maquete e a maquete da recepção, com sol de fim de tarde |
| Técnica | 2.5D: **placas da maquete** geradas pela OpenAI **sem a personagem**, mais a personagem como **camada separada, com a mesma luz**, e camadas de profundidade (primeiro plano, maquete, sala em volta) que a câmera do HyperFrames move com parallax (as camadas mais perto andam mais que as de longe). Se a camada dela parecer "colada", a cena é gerada com ela dentro e a profundidade é separada depois. Interface do celular em HTML. | 3D de verdade (Three.js r184) num palco de estúdio. É um projeto à parte, e entra no episódio como **sub-composição** (um arquivo de cena montado dentro do episódio com `data-composition-src`): o 3D é desenhado no próprio render do episódio, sem comprimir o vídeo duas vezes. Plano B: render do vídeo dela em MOV ou MP4 de alta qualidade, tocado num `<video>`. **No ep. 01** (o corte de 10 s e, até o teste mostrar o contrário, o vídeo completo), o Mundo 2 sai de imagens geradas em camadas, alinhadas entre si e animadas no HyperFrames (ver `ep01-SPEC.md`, seções 6 e 9.3); o Three.js fica como evolução, se o teste mostrar que vale a pena. | 2.5D, com as mesmas regras do Mundo 1. Cada lugar à tarde é uma **placa própria** (ver seção 4). |
| Fundo | a maquete do consultório à noite, mais clara do que escura: pretos **nunca abaixo de #2B2224** em área grande; paredes de gesso #72605E a 60% de luz. Em volta, a mesa e a sala de verdade, desfocadas | degradê **vertical**, de #44464B no alto para #2A2C30 embaixo, com grão de 1% só no fundo (o grão evita as faixas que o degradê cria no H.264); **nada de centro claro** | a mesma maquete e a da recepção, com sol baixo entrando pela persiana em miniatura |
| Luz | o abajur da maquete, de 2700 K, **à esquerda do quadro**. A luz dele se espalha suave pela maquete inteira (de 100% à esquerda a 45% à direita), **sem borda de círculo e sem bola de luz desfocada**. A única luz fria é a da tela do celular (#E8EEF2). Depois que o abajur apaga, fica só a luz fria e fraca da rua, pela persiana à esquerda, a 30%: a cena continua visível, **nunca um quadro preto**. | luz principal quente #FFE4CC vinda de cima à esquerda; contraluz laranja #F34500 de trás à direita; 2 a 3 faixas de luz no ambiente; sombra de contato a 0,55 | listras douradas #F28801 da persiana na parede, vindas da esquerda; sombra levemente azulada; abajur apagado |
| Materiais | miniatura com **material de verdade**: madeira pintada, tecido, gesso com textura fina, papel com fibra, vidro do celular; a personagem com pele fosca e jaleco de tecido real. Nunca plástico brilhante, nunca vetor | ver a tabela da seção 7 | os mesmos do Mundo 1 |
| Câmera | **lente macro de maquete**: desfoque forte em cima e embaixo do quadro (o "efeito miniatura", que faz a gente ler a cena como uma maquete de verdade), passeios lentos e aproximações; um pouco acima da maquete nos planos largos (como quem se debruça sobre a mesa), descendo até a altura dela nos planos fechados; empurrão lento de 1,00 a 1,04 por plano; parallax em 3 camadas, com escala própria por camada | equivalente a ~50 mm; mergulha no objeto em vez de girar em volta; nunca sobe ou gira mais de 30° num movimento (no ep. 01, no máximo 25° em 1,4 s); **gira o ambiente, 3 a 5° por segundo, e não o objeto**; o objeto herói ocupa de **40% a 70% da altura** | igual ao Mundo 1, mas a câmera fica parada por mais tempo (calma) |
| Acabamento | grão de 3%, vinheta de 8% (por `npx hyperframes media-treatment`, nunca por filtro CSS). O desfoque de miniatura já vem na placa gerada e é reforçado por camada (a da frente e a do fundo mais desfocadas), nunca por um borrão em faixa sobre o quadro inteiro | sem vinheta; grão de 1% só no fundo; bloom (brilho que estoura o branco) desligado ou só nos 2% mais claros | grão de 3%, vinheta de 6% |

**Objeto herói** ocupa pelo menos 40% da altura do quadro em todo plano (no plano largo, o objeto herói é a própria maquete). Nunca um objeto pequeno solto no escuro.

**Se o dono preferir "escuro de verdade"** (é uma pergunta em aberto): as sombras do Mundo 1 podem descer até #1E1415 e as paredes ficam a 40% de luz. Continua valendo: nada de holofote redondo, nada de bola de luz e nada de quadro preto.

### 1.1 Toques lúdicos (inspirados nas referências, nunca copiados)

- **Etiquetas da maquete:** pequenas etiquetas brancas presas aos objetos por uma linha fina, como as de preço ou de meta num jogo.
  - Só onde substituem a leitura de uma tela ou de um papel que ficou pequeno no quadro (por exemplo, "take 14" no celular visto de longe, "último post · há 47 dias" no perfil dentro da maquete).
  - No máximo **uma por vez**; entra inteira quando o olho chega ao objeto e fica parada (0,5 s + 0,3 s por palavra); conta nas ~20 palavras da tela.
  - Helvetica minúscula, sem ponto final, **nunca laranja** (laranja é da inteligência). Estilo na seção 8.
  - Nunca repete a narração palavra por palavra (a regra da legenda vale para ela).
- **A revelação da maquete:** todo episódio começa perto, num objeto dela (o celular, uma nota, um áudio), e no primeiro recuo a câmera mostra que tudo é uma maquete sobre uma mesa. É a "piada visual" da série.
- **Do brinquedo para o real:** na dobra, a folha (miniatura de papel) sai da maquete e vira a tela; no impacto, o mundo realista acende. O contraste de materiais (papel, madeira e tecido → vidro, titânio e porcelana) é o efeito, e mostra sem dizer o que a inteligência faz com o conhecimento dela.

## 2. A regra fixa: "história" × "vídeo entregue"

> **Maquete com luz quente e personagem-boneco = a vida dela. Estúdio cinza-grafite com 3D realista = o vídeo dela.**
> - O vídeo dela **sempre nasce do fio laranja e da dobra**: é ali que o brinquedo vira o real.
> - **Enquanto é um cartão** (na dobra e quando encolhe para o celular), ele tem a moldura do fio laranja de 4 px, com cantos de 48 px; dentro do celular, cantos de 22 px. **Em tela cheia**, ele fica sem moldura (raio 0, sem fio).
> - Do primeiro ao último quadro, ele carrega a assinatura dela ("dra. Helena Prado · cirurgiã-dentista · CRO-UF 00000") e o selo "ilustração educativa · apoio de IA".
> - No post próprio do vídeo dela, o selo vira uma linha só, que também avisa que é ficção: "exemplo fictício · apoio de IA".
> - A personagem **nunca** entra no estúdio, e o 3D realista **nunca** aparece na maquete.
> - Não existe fusão nem corte seco entre os dois mundos: a passagem é sempre por um objeto (a dobra, a tela do celular).
> - O narrador **não fala** enquanto o vídeo dela roda.

## 3. A regra do laranja

- **O laranja #F34500 é a inteligência.** Nada da vida dela é laranja: roupa, caneta, interface do celular, botões, ponto de gravação, objetos da maquete, etiquetas.
- O primeiro laranja de cada episódio é o fio aparecendo.
- Depois dele, o laranja aparece só:
  - no fio e nas palavras que ele pinta;
  - na moldura e na luz de recorte do vídeo dela;
  - nas linhas-guia dos rótulos;
  - na palavra-chave da frase da virada.
- **Lima #EFFF57:** um único ponto por plano, só dentro do vídeo dela (a ponta do rótulo principal).
- **Fora da história** (no cartão da série), o laranja volta a ser a cor da marca, em "ep. 0X".

## 4. Planta de cena e luz

- **Antes de gerar qualquer imagem**, desenhar a planta de cada plano: onde estão a câmera, a borda da maquete, o celular e ela (corpo inteiro e rosto).
  - A tela com a câmera frontal só aparece para nós se estivermos do lado dela, por cima do ombro.
  - A câmera frontal mostra a imagem espelhada. Por isso, no visor, o lado esquerdo dela (a faixa grisalha) e a luz do abajur aparecem à **esquerda da tela**.
  - Se a tela está virada para nós e ela está atrás do celular, quem a filma é a câmera traseira: a imagem **não** é espelhada, e a faixa grisalha aparece à **direita** da tela, do mesmo lado em que aparece no corpo dela atrás do tripé.
- **A luz principal vem sempre da esquerda do quadro.** Nunca espelhar uma imagem para corrigir um lado trocado: isso inverte a luz. Se o gerador trocar esquerda e direita, gera-se de novo.
- **Escurecer pode, clarear não.** Uma placa (a imagem de fundo de um lugar) pode ser escurecida e esfriada no HyperFrames, mas nunca clareada: clarear sombras multiplica o ruído e as faixas de cor e não cria detalhe (foi o problema do preset "Sabiá dourado", rejeitado). Por isso as placas da noite já são geradas com as sombras abertas.
- **Uma placa base por lugar e por luz + camadas.** Dentro de um plano, o que muda nasce como camada sobre UMA imagem de fundo:
  - o abajur apagando (escurecer a placa e esfriar a cor, sem clarear nada);
  - o brilho da tela;
  - a luz fria da rua (camada feita em código, um degradê frio e desfocado vindo da esquerda, sem listras nítidas).
- **A tarde é uma placa própria.** A C1-tarde é uma edição da C1-noite com `--ref` da noite: "same miniature diorama, same wooden base and table, same camera position and macro lens, same tilt-shift depth of field, same furniture; change ONLY the light: late-afternoon sun through the miniature blinds from the LEFT, lamp OFF; no people, no text" (1440x2560, xhigh, 2 finais). Antes de aprovar, sobrepor as duas placas a 50% e conferir que bancada, cadeira e parede não se deslocam mais de 8 px, porque o fim do episódio é um corte casado com a cena 2. Se deslocarem, gerar de novo. A máscara das listras de luz (para uma sombra só escurecer onde há sol) sai da própria C1-tarde, pelo brilho.
- **Final de placa = edição do rascunho escolhido.** Como na personagem (seção 6), a versão final de cada placa (C1, C2, C3) é uma edição do rascunho escolhido, com `--ref`, nunca uma geração nova do zero.
- **Placa sem personagem, personagem como camada.** As placas da maquete saem sem ninguém dentro; a personagem entra como camada sem fundo, gerada com a mesma luz e o mesmo ângulo da placa (a placa vai como `--ref` da pose). Se a camada parecer "colada" (luz, sombra de contato ou escala erradas), a cena é gerada com ela dentro e a profundidade é separada depois.

## 5. O celular e as telas

- **O aparelho é sempre o mesmo objeto, feito em HTML:**
  - corpo chumbo #303236, cantos de 64 px;
  - sem marca e sem câmera reconhecível;
  - um leve brilho na borda esquerda, vindo do abajur.
- **As imagens geradas só fornecem o que segura o aparelho** (a garra do tripé, um suporte de mesa; na maquete, em miniatura, com o mesmo material dela), com uma placa escura lisa no lugar do celular. No ep. 01 nenhuma mão segura o celular.
  - a placa é gerada **de frente**, sem inclinação; se vier torta, gera-se de novo (a interface nunca é entortada para caber);
  - os 4 cantos da placa são medidos nos pixels, com um script que acha a área escura lisa por limiar de cor (o `locate.mjs` erra cerca de 2%, de 30 a 77 px nessas imagens, e não serve aqui);
  - o que segura o aparelho vira duas camadas: atrás do celular HTML, a imagem inteira; na frente, um recorte só das pontas da garra que cruzam a borda da placa (máscara feita uma vez por imagem);
  - o celular HTML tem exatamente o tamanho medido da placa.
- **As interfaces são genéricas:** nada que imite Instagram, WhatsApp, ChatGPT, Claude ou iPhone. O texto fica em minúsculas, nas cores #F6F4F1, #303236 e #72605E, sem laranja e sem vermelho.
- **A grade do perfil usa retângulos verticais 9:16**, nunca quadrados.

## 6. A personagem principal: dra. Helena Prado

**Estilo: boneco de série animada (B), aprovado em 12/11/2026.** As referências que mandam são `personagens\dra-helena\rascunhos\v2-folha-B-designer-toy-1.png` (a folha) e `v2-capa-B.png` (ela dentro da maquete). Os estilos A (figura de madeira) e C (animação estilizada) ficaram de lado e estão em `referencias-visuais\v2-painel-estilos.png`.

**O que NUNCA muda**
- **Estilo e proporção:** boneco de série animada, lúdico e simpático, mas adulto e profissional. A cabeça mede cerca de **1/3,5 da altura**; corpo compacto, com ombros, cintura e postura de mulher adulta; mãos simples, com cinco dedos curtos.
- **Rosto:** simples e legível:
  - oval, pele morena média de tom quente (≈ #B9825F, conferida na composição);
  - **olhos ovais escuros e pequenos, com pálpebras** (são elas que deixam ela cansada, calma ou surpresa);
  - nariz pequeno e arredondado, **boca em linha fechada**, sobrancelhas escuras e marcadas.
- **Acabamento:** pele fosca com luz suave por dentro (sem brilho de plástico); cabelo em formas esculpidas com sulcos finos; **tecido de verdade** no jaleco; luz e sombra reais, com qualidade de curta-metragem de animação.
- **Cabelo:** castanho quase preto, preso num **coque baixo na nuca**, com **uma faixa grisalha larga que sai da têmpora ESQUERDA dela e vai presa até o coque**.
  - Não há mecha solta: uma mecha solta muda de forma a cada imagem gerada, e a faixa presa fica estável.
- **Roupa:**
  - jaleco branco-osso #F6F4F1, fosco, até o meio da coxa, com **gola padre** (mandarim), botões escondidos e mangas dobradas uma vez;
  - blusa chumbo #303236 de gola alta; calça reta chumbo; sapatos baixos chumbo;
  - relógio fino de couro marrom no **pulso esquerdo**; caneta chumbo no bolso do peito esquerdo;
  - sem óculos, sem brincos, sem joias, sem crachá, sem logo, sem nome bordado. **Nada laranja.**
- **Idade aparente:** 44 anos: mulher adulta de meia-idade, nunca menina.

**O que pode (v2)**
- Aparecer **de corpo inteiro** na maquete: parada, de costas, de perfil, andando. Com o boneco, o risco de "cara de IA" do rosto realista cai, e ver a personagem é parte da graça.
- Fazer uma ação física em **2 ou 3 poses-chave** de corpo inteiro, com corte na ação e borrão de movimento entre elas (seção 9).
- Mostrar a mão-boneca segurando um objeto (caneta, celular) quando a cena pede (no ep. 01, a caneta riscando a data na folha): o assunto do quadro é o objeto, nunca um close só dos dedos.
- **Close de rosto só em poses aprovadas:** no ep. 01, o visor da câmera no começo. Todo close novo é uma pose aprovada antes de entrar no filme.

**Expressões aprovadas (6), feitas pelas pálpebras e sobrancelhas:** cansada (pálpebras a meio, sobrancelhas caídas nas pontas, ombros baixos); olhos fechados (frustração contida); semiaberta (os olhos abrindo); surpresa contida (pálpebras bem abertas, sobrancelhas sobem pouco, boca fechada); sorriso de canto (boca fechada, um canto levantado); tranquila, olhando para baixo.

**Nunca**
- olhos de anime grandes e brilhantes, cílios exagerados, cara de bebê ou de menina, proporção chibi (cabeça maior que no modelo aprovado);
- massinha, plástico brilhante, vinil lustroso, porcelana; foto realista;
- boca aberta falando (sem sincronia labial) ou dentes à mostra; olhar fixo falando para a câmera;
- trocar o penteado, perder a faixa grisalha ou trocar a cor do jaleco;
- pôr laranja nela.

**Como trocar de expressão sem "pular"**
- No boneco, a expressão mora nas **pálpebras e nas sobrancelhas**; a boca fica em linha fechada (só o sorriso de canto levanta um canto).
- Cada estado é gerado como edição ("mude só as pálpebras e as sobrancelhas"), com a cabeça na mesma posição e escala, e recortado com borda suave.
- No vídeo entram **3 estados da região alterada** (por exemplo, pálpebras fechadas, a meio e abertas), colados como camadas sobre a imagem original. Cada troca leva 2 quadros de passagem suave, só dentro do recorte. Olho leva de 3 a 5 quadros para abrir; um estalo de 1 quadro parece defeito.
- A troca é um "take" em 4 tempos: antecipa, comprime, troca as pálpebras e assenta.

### Prompt da folha de personagem (estilo B)

Para `gerar-imagem.mjs`. O texto do pedido fica em inglês porque o modelo responde com mais precisão. Este é o pedido que gerou o rascunho aprovado (`prompts\folha-B-designer-toy.txt`; gpt-image-2.5-flare, low, 1536x864):

```
Character model sheet. STYLE B, DESIGNER TOY: a premium 3D designer-toy character for an animated series; chunky
friendly proportions (head about 1/3.5 of total height, compact body); simple readable face: small dark oval eyes with
eyelids (so she can look tired or calm), small rounded nose, small closed mouth line, subtle eyebrows; soft matte skin
with gentle subsurface light; hair as clean sculpted shapes with fine grooves; real fabric texture on the lab coat;
simple hands with five short fingers. Playful and lovable but professional and adult, never childish. High-end
animated-short quality render, real light and shadow. NOT photoreal, NOT big glossy anime eyes, NOT chibi, NOT clay,
NOT plastic shine.
IDENTITY (keep in every version): a fictional Brazilian dental surgeon, implant specialist, mid-40s woman; warm
medium-brown skin; very dark brown hair pulled back into a LOW BUN at the nape with ONE wide grey streak from her own
LEFT temple swept into the bun; bone-white lab coat (#F6F4F1) with a MANDARIN band collar and hidden buttons, sleeves
folded once; charcoal (#303236) high-neck top, charcoal trousers, low charcoal shoes; thin brown watch on her LEFT
wrist; charcoal pen in the left chest pocket. Nothing orange on her. No glasses, no jewelry, no logo, no text.
Layout: character model sheet, four full-body views side by side at the same scale: front, three-quarter front, left
profile, back. Neutral standing pose. Soft studio light from the upper LEFT, warm off-white seamless background
(#F3EFE8), soft contact shadow under each figure. No text, no labels, no frames, no watermark, no extra people.
```

**Final** (2 opções), **sempre como edição do rascunho aprovado**, nunca do zero (gerar só a partir do texto desenha outra personagem):
`node ferramentas\openai\gerar-imagem.mjs --prompt-arquivo hyperframes\_serie-clinicas\personagens\dra-helena\prompts\folha-final.txt --ref hyperframes\_serie-clinicas\personagens\dra-helena\rascunhos\v2-folha-B-designer-toy-1.png --modelo gpt-image-2.6-sunburst --qualidade xhigh --tamanho 2560x1440 --fundo opaque --n 2 --saida hyperframes\_serie-clinicas\personagens\dra-helena\folha.png`
O `folha-final.txt` começa com: "Image 1 = approved draft. Keep exactly the same character design, face, proportions, sculpted hair, grey streak, low bun, coat, materials, rendering style and layout; only raise finish, detail and resolution." e segue com o pedido acima.

### Prompt da folha de expressões (2048x1152, xhigh, com `--ref` da folha final)

Os bustos são bem maiores que as cabeças da folha de corpo inteiro (~190 px cada), então esta folha também faz o papel da antiga folha de rosto: entra como 2ª `--ref` em toda pose.

```
Image 1 = approved character model sheet (style B: premium 3D designer-toy character for an animated series).
Do not redesign the character.
Expression sheet of the SAME character: six head-and-shoulders busts in a 3x2 grid, same scale, same head size and
position in every bust, same three-quarter front angle, same soft studio light from the upper LEFT, warm off-white
seamless background (#F3EFE8).
The expression lives ONLY in the EYELIDS and EYEBROWS; the mouth stays a small closed line (only bust 5 lifts one
corner).
Top row: (1) tired: upper eyelids half lowered, eyebrows slightly dropped at the outer ends, shoulders a little down;
(2) eyes closed, quiet frustration: eyelids fully shut, eyebrows drawn slightly together; (3) half-open: eyelids
halfway, eyebrows neutral.
Bottom row: (4) restrained surprise: eyelids fully open, eyebrows raised a little, mouth closed; (5) small
closed-mouth half smile, one corner lifted, relaxed eyelids; (6) calm, looking down, eyelids lowered, eyebrows relaxed.
Keep exactly: face shape, small dark oval eyes, small rounded nose, warm medium-brown skin, matte skin with soft inner
light, sculpted hair with fine grooves, one wide grey streak from her own LEFT temple swept into the LOW BUN,
bone-white mandarin-collar lab coat with real fabric texture, charcoal high-neck top, rendering style.
Mouth always closed, no teeth. Nothing orange. NOT photoreal, NOT big glossy anime eyes, NOT baby-faced, NOT chibi,
NOT clay, NOT plastic shine.
No text, no labels, no numbers, no frames, no watermark.
```

### Bloco fixo para toda pose

Toda pose sai de um pedido de edição com `--ref folha.png --ref expressoes.png` e, quando ela vai para dentro de uma placa da maquete, também `--ref` da placa (para a luz, o ângulo e a escala baterem). **A personagem nunca é gerada do zero num plano novo.** As poses saem sem fundo, de corpo inteiro sempre que o plano mostrar o corpo.

```
Image 1 = approved character model sheet. Image 2 = approved expression sheet. (Image 3 = the miniature plate where
she will be placed: match its light, camera angle, lens and scale.)
Do not redesign the character. Change ONLY the pose, framing, expression and light described below.
Keep exactly: style B premium 3D designer-toy character for an animated series (head about 1/3.5 of total height,
compact adult body); face; small dark oval eyes with eyelids; small rounded nose; closed mouth line; matte skin with
soft inner light; sculpted hair with fine grooves; one wide grey streak from her own LEFT temple swept into a LOW BUN;
bone-white lab coat with real fabric texture, mandarin collar, hidden buttons, sleeves folded once; charcoal
high-neck top, charcoal trousers, low charcoal shoes; brown leather watch on her LEFT wrist; charcoal pen in the left
chest pocket; skin tone. NOT photoreal, NOT big glossy anime eyes, NOT baby-faced, NOT chibi, NOT clay, NOT plastic
shine. Nothing orange on her. Mouth closed, no teeth. Five short fingers on each visible hand. No text anywhere.
POSE: <...>
EXPRESSION: <number and name from the expression sheet>
LIGHT: <...>
BACKGROUND: transparent, isolated subject, no floor, no cast shadow
```

**Exemplo 1, de costas apagando o abajur (ep. 01, fim da cena 5 e 1º segundo do corte de 10 s):**
- POSE: *seen from behind and slightly above, as from a camera leaning over the miniature counter; upper body and head; her LEFT arm stretched out to the switch of a small table lamp at the upper LEFT; head slightly bowed; the grey streak shows on the LEFT side of her head, running into the low bun; the watch on her LEFT wrist.* (2ª pose-chave: o mesmo ângulo, com o braço recolhido junto do corpo.)
- EXPRESSION: *not visible (back view).*
- LIGHT: *warm 2700 K table-lamp light from the LEFT, soft and wide; late night; soft lifted shadows, no crushed blacks.*

**Exemplo 2, o visor da cena 1 do ep. 01:**
- POSE: *chest-up, facing the camera, centered, as seen in a phone camera preview; shoulders slightly raised.* Mais uma linha, conforme a planta da cena (ver `ep01-SPEC.md`, seção 2): câmera traseira → *not mirrored: the grey streak appears on the RIGHT side of the image*; câmera frontal → *mirror view: the grey streak appears on the LEFT side of the image*.
- EXPRESSION: *(2) eyes closed, quiet frustration.*
- LIGHT: *warm 2700 K table-lamp light from the LEFT of the image, soft and wide; soft lifted shadows, no crushed blacks; late night.* (Só com a câmera frontal, que deixa a tela virada para ela: *plus a cool bluish phone-screen light on the face from the front*.)

### Pedido de cenário: placa da maquete (modelo)

```
Tabletop miniature diorama: a premium handmade scale model photographed with a macro lens and a strong tilt-shift
(miniature) depth of field: sharp in a horizontal band, softly blurred at the top and bottom of the frame. No people.
The diorama: a small, tasteful dental office at night, built as a cut-away room on a wooden base (two walls and a
floor; the wooden edge of the base visible), standing on a warm wooden table; the real room around the table is
warm, dim and out of focus. Seen from a slightly high three-quarter angle, as if leaning over the table.
Real miniature materials, the same language as the approved character: painted wood, fabric, plaster with fine
texture, paper with fibre, real light bounce. NOT glossy plastic, NOT vector, NOT a flat isometric illustration,
NOT clay, NOT low poly.
LEFT third: a wooden work counter with a small table lamp switched on (warm 2700 K); EMPTY counter surface (no paper,
no objects). A window with horizontal blinds on the back wall, faint cool street light outside.
RIGHT third: a generic, unbranded dental chair in muted warm grey, empty, softly lit.
CENTER: empty floor space (the miniature tripod and the character are added later as separate layers).
The lamp light spreads softly and widely across the whole diorama from the left: soft lifted shadows (deepest tones
around #2B2224), no hard pool or circle of light, no spotlight, no bokeh balls, no other light source.
Nothing orange. No text, no logos, no labels, no screens, no instruments, no people.
```

Para outro lugar ou ângulo (a bancada vista quase de cima, a recepção), troca-se só o miolo (o que fica à esquerda, à direita e no centro, e o ângulo da câmera), mantendo o começo e as duas últimas frases. A versão de tarde de cada placa é sempre edição da de noite (seção 4).

**Antes de aprovar uma imagem:**
- conferir se a transparência veio de verdade (um xadrez desenhado não é transparência);
- plano B da transparência: para a personagem, `npx hyperframes remove-background` (o modelo dele é feito para recortar pessoas; conferir se recorta bem o boneco) e, se falhar, gerar de novo sobre fundo liso #F3EFE8 e recortar por cor num script; para objetos (tripé, garra, suporte, papel), gerar de novo sobre fundo liso #E6E3DF e recortar por cor;
- pôr a camada dela sobre a placa e conferir luz, sombra de contato e escala; se parecer colada, gerar a cena com ela dentro e separar a profundidade depois (seção 4);
- registrar o modelo e a data no `registro.csv`, porque o 2.6 não tem versão congelada.

## 7. Materiais do vídeo dela (3D)

| Peça | Material | Números |
|---|---|---|
| implantes e barra (feitos em código) | titânio acetinado #B9BEC4 | metal 1, aspereza 0,45, ambiente 0,5 |
| dentes da prótese (coroas do modelo escaneado) | porcelana #F6F4F1 | aspereza 0,32, verniz 0,4 |
| base da prótese | resina rosada fosca #E3C3BA, levemente translúcida (nunca porcelana branca) | aspereza 0,6 |
| osso (modelo escaneado) | vidro fosco menta #88D09D | transmissão 0,55; uma **faixa de vidro limpo** que atravessa o osso e limpa o fosco por onde passa (shader próprio, testado no teste técnico) |
| face cortada | chumbo #303236, sólida, com trama de osso esponjoso em menta | tampas pela técnica de stencil do three.js (para o osso cortado não parecer oco), que só funciona em malha fechada; ruído com semente. Se a malha tiver buracos, plano B: um bloco de osso feito em código em volta do implante do meio (cilindro com trama esponjosa menta), com a câmera fechada nele |
| contraluz | laranja #F34500 | de trás à direita |
| destaque | lima #EFFF57 | um ponto de 10 px por plano |

**Orgânico (dente, osso, gengiva) nunca é feito em código:** a coroa do teste `f29.png` virou uma "bolha". Em código entram só peças mecânicas e a base da prótese, e a base só depois de uma imagem parada aprovada pelo dono.

**Os objetos não giram:** quem gira é o ambiente (as luzes e o fundo), de 3 a 5° por segundo. Implante nunca desce, entra, gira ou é parafusado no osso.

**Quando o Mundo 2 é feito com imagens em camadas** (no ep. 01, a começar pelo corte de 10 s): os materiais da tabela valem igual, e a régua de qualidade é `cenarios\rascunhos\estudio-video-dela.png`. As camadas saem como edição desse quadro, alinhadas entre si (osso fosco, osso limpo com os implantes, prótese separada); a faixa de vidro limpo vira uma troca entre o osso fosco e o osso limpo por uma máscara em faixa, e o ambiente que gira vira uma luz que varre a peça parada.

## 8. Tipografia na tela (1080×1920)

**Regras gerais:**
- Helvetica Now Text, letter-spacing −0,05em, line-height 0,9. Regular para o texto, Bold só no destaque.
- Tudo minúsculo, exceto nomes próprios e siglas (Helena, CRO-UF, IA). **Em aberto com o dono:** no carrossel ele passou a usar maiúscula no começo de cada frase; se isso valer para a série, muda nas legendas, títulos e frases (a interface do celular continua em minúsculas).
- Nenhum ponto final.
- **A Megion não entra nos episódios.** Ela só serve para uma palavra realmente sozinha (como CHECKLIST num carrossel), nunca para a palavra-chave de uma frase. Se um dia entrar, usa letter-spacing +0,03em (com −0,05em as letras grudam).
- Texto só entre y=168 e y=1330. Abaixo de y=1000, nada à direita de x=930. Nada para ler com menos de 28 px.
- Nenhum texto dentro das imagens geradas: todo texto é HTML.

| Uso | Fonte | Tamanho | Cor | Posição |
|---|---|---|---|---|
| Legenda da história | Regular; Bold só na palavra-chave (Bold branco, sem laranja) | 60 px, até 2 linhas e 8 palavras | #F6F4F1, sombra local suave (0 2 18 px, #1E1415 a 60%) | x=108, base fixa em y=1220, largura até 760 px |
| Frase da virada | Regular, palavra-chave em Bold #F34500 | 96 px, 1 linha | #F6F4F1 | centro óptico, y≈760; uma por episódio |
| Título do vídeo dela | Regular, uma palavra em Bold | 72 px, até 2 linhas e 7 palavras | #F6F4F1 | topo do bloco em y=300, x=108 |
| Linha de apoio do vídeo dela | Regular | 44 px | #F6F4F1 a 80% | logo abaixo do título |
| Rótulo de peça 3D | Regular | 40 px | #F6F4F1, linha-guia de 2 px #F34500, ponto lima | junto da peça, entre y=500 e y=1100 |
| Assinatura dela (fixa) | Regular | 30 px | #F6F4F1 a 80% | x=108, y=1180 |
| Selo de IA (fixo) | Regular | 28 px | #F6F4F1 a 70% | x=108, y=1290 |
| Aviso de prova interna | Regular | 28 px | #F6F4F1 a 70% | x=108, y=200 ("rascunho · frases em revisão"; nunca sai de `renders\`) |
| Cartela final do vídeo dela | nome em Bold 56 px; demais linhas em Regular 36 px | — | #F6F4F1 | bloco à esquerda, x=108. A assinatura fixa não some: ela sobe e vira o fim da cartela; o bloco termina em y=1180 e o selo continua em y=1290 |
| Folha impressa (objeto de cena) | Regular | 34–48 px efetivos | #303236; palavras pintadas pelo fio em Bold #F34500 | sobre o papel; cada palavra que o fio vai pintar já é composta numa caixa com a largura da versão Bold, para nada andar quando o peso muda |
| Interface do celular | Regular e Bold | 40–60 px efetivos quando o celular é o assunto do quadro; nunca menos de 34 px | #F6F4F1, #303236, #72605E | dentro da tela |
| Etiqueta da maquete | Regular, minúscula | 40 px, 1 linha, até 5 palavras | texto #303236 sobre etiqueta #F6F4F1 (cantos de 8 px); linha fina de 2 px #F6F4F1 a 80% até o objeto; nunca laranja | presa ao objeto, dentro da área de texto (y=168 a y=1330); uma por vez |
| Cartão da série | "sala de espera ·" Regular 72 px + "ep. 01" Bold 72 px #F34500; próximo episódio em Regular 40 px a 80%; aviso em 28 px a 60% | — | #F6F4F1 sobre chumbo #303236 | ícone de 56 px em y=700, título em y=820, próximo em y=960, aviso em y=1290 |

**Quantidade de texto:**
- até 8 palavras por legenda;
- até ~20 palavras legíveis por tela, **contando assinatura e selo**;
- cada linha segura 0,5 s + 0,3 s por palavra, e a última frase do filme segura pelo menos 2 s;
- texto entra inteiro, de uma vez (nada de palavra por palavra, nada de karaokê).

**A legenda complementa a voz:** diz a virada com outras palavras, nunca repete a narração palavra por palavra.

**Teste do mudo:** lendo só o que está na tela, na ordem, a história inteira precisa fazer sentido.

## 9. Movimento

- **Ritmo:**
  - cada evento legível dura de 1 a 3 s, e o resultado fica parado de 1,5 a 2 s;
  - algo novo a cada 2 a 4 s, sem sequência de cortes abaixo de 1 s;
  - um mecanismo de movimento diferente por cena;
  - o truque "um por um" (palavras, balões ou itens acendendo em sequência) em **uma cena só** por episódio.
- **Na batida:** a trilha tem 72 BPM, ou seja, uma batida a cada 25 quadros. A dobra, o impacto e os textos da história depois do impacto caem na batida (dentro do vídeo entregue, as trocas de passo seguem o tempo de leitura, porque a trilha está sustentada); antes do impacto, a voz manda e o texto cai na batida mais próxima quando isso não tira tempo de leitura.
- **Ease por papel:**
  - chegada com cauda longa (`expo.out`);
  - câmera e mudanças de luz nos dois sentidos (`power2.inOut`);
  - atravessar ou sair acelerando (`power3.in`).
  Título pousado fica parado.
- **Transições, sempre com causa na tela, em 5 famílias:**
  1. o movimento contínuo da câmera (com a troca de placa escondida no borrão de movimento, quando o ângulo muda);
  2. o corte pela luz (a luz de uma tela invadindo, uma tela apagando, o abajur apagando);
  3. a troca na mesma tela (desfoque);
  4. o objeto que vira o mundo e o levar junto (a moldura);
  5. o corte seco casado (no máximo um terço das emendas).
- **Ação física** (ela andar, riscar, pegar o celular) nunca é feita com um recorte parado deslizando. Ela é mostrada:
  - pela tela do celular;
  - pela sombra (uma sombra que anda usa pelo menos 2 poses-chave alternando, com desfoque e borrão de movimento);
  - pelo som;
  - ou pela personagem-boneco em 2 ou 3 poses-chave de corpo inteiro, com corte na ação e borrão de movimento entre elas (quando ela anda, cada pose fica parada alguns quadros num ponto novo, como animação de maquete quadro a quadro; nunca uma pose só deslizando).
- **Se o dono disser "rápido demais":** cada resultado ganha +0,5 s parado e cada movimento dura 1,4 vez mais. A voz não muda: os segundos extras entram nas pausas.

## 10. Som (resumo)

- A voz A.Medeiros é o relógio: a voz é gravada primeiro e a imagem se ajusta a ela.
- A trilha começa leve, cresce e tem UM impacto, no fim do 3º tempo da dobra. Ela é alinhada **só pelo golpe** (o impacto dela vai no quadro do impacto do filme); os outros tempos dela (2ª voz do piano, cordas, pulso, acorde final) são aproximados e valem como a trilha escolhida trouxer. A trilha nunca é cortada nem esticada entre a entrada e o golpe.
- **Cada efeito tem causa na tela** e cai 1 quadro depois da imagem.
- No máximo **2 sons de deslocamento de ar** ("sopros") por episódio. As outras transições soam como o material que se move: papel, vidro.
- **Sons de interface** (toque, "enviado", "encaminhado", chegada de mensagem) são toques secos de dedo em vidro, **sem nota musical**.
- Sons repetidos alternam 2 ou 3 tomadas. Os 3 sons de dobra são arquivos fixos da série.
- Nada de tons sintetizados, "plins" ou sinos.

## 11. PROIBIDO (lista nominal)

- **Personagem:**
  - boca mexendo ou fala sincronizada (lip sync); olhar fixo falando para a câmera;
  - olhos de anime grandes e brilhantes, cara de bebê, proporção chibi, pele de borracha;
  - massinha, plástico brilhante, vinil lustroso ou porcelana (o boneco é fosco, com tecido de verdade);
  - personagem com rosto realista (as pessoas da série são bonecos no estilo B; o realista fica só no vídeo dela);
  - rosto diferente entre planos; close de rosto fora das poses aprovadas; close só de mãos e dedos (sem o objeto que elas seguram, seção 6); dedos errados;
  - qualquer laranja nela; mudar o coque, a faixa grisalha ou o jaleco;
  - espelhar uma imagem para corrigir o lado;
  - troca de expressão num estalo de 1 quadro.
- **Estilos:**
  - massinha pastel, ícone 3D fofo, diorama isométrico vetorial, low poly (a maquete da série é miniatura de material real fotografada com lente macro, nunca ilustração vetorial);
  - etiqueta laranja ou mais de uma etiqueta ao mesmo tempo;
  - dente ou alimento falante;
  - robô, cérebro azul, circuitos ou holograma como símbolo de IA;
  - as palavras "Pixar" e "Disney" em qualquer pedido.
- **Luz:**
  - holofote redondo, poça de luz com borda, bola de luz desfocada;
  - degradê radial com centro claro;
  - quadro preto ou quase preto em qualquer momento da história; pretos abaixo de #2B2224 em área grande;
  - clarear uma placa escura (escurecer pode, clarear não).
- **Clichês de vídeo gerado:**
  - vazio escuro com objeto pequeno (menos de 40% do quadro);
  - glow, bloom forte, lens flare, partículas, orbes;
  - degradê roxo ou azul; degradê no fundo escuro sem grão (cria faixas);
  - cards de vidro, três cards em fila, telas lado a lado, logo no canto, molduras decorativas, painel de controle;
  - tudo entrando com "aparece e sobe"; título que continua deslizando depois de pousar; respiração ou flutuação em título e interface;
  - o mesmo truque "um por um" em mais de uma cena;
  - Ken Burns (zoom lento em foto parada) como único movimento;
  - fusão entre mundos;
  - caixa de prompt, cursor de agente ou tela de chat de IA;
  - o mesmo "whoosh" em todo corte;
  - recorte parado deslizando para fazer ação física;
  - texto gerado dentro da imagem.
- **Legenda e texto:**
  - karaokê amarelo com contorno; texto entrando palavra por palavra;
  - repetir a narração palavra por palavra;
  - texto que se mexe enquanto é lido;
  - ponto final;
  - mais de 8 palavras por legenda; mais de ~20 palavras por tela;
  - Megion na palavra-chave de uma frase.
- **Clínico:**
  - sangue, incisão, gengiva aberta, broca ou instrumento; mão operando; boca realista (lábio, língua, saliva);
  - paciente, nem desenhado (a cadeira está sempre vazia);
  - **implante descendo, entrando, girando ou sendo parafusado no osso**; parafuso girando; 4 implantes com os de trás inclinados;
  - prótese descendo e assentando, enquanto o advogado ou o CRO não liberar (até lá, ela aparece já assentada, revelada por uma faixa de luz);
  - antes e depois; sorriso "depois";
  - preço, parcelamento, "avaliação gratuita";
  - "sem dor", "para sempre", "100%", "o melhor", "dentes no mesmo dia"; carga imediata fora de "em alguns casos";
  - "All-on-4"; marca de fabricante (Nobel, Straumann, MSDI); "caso clínico" como nome.
- **Marcas e pessoas:**
  - celular reconhecível;
  - interface que imite Instagram, WhatsApp, ChatGPT ou Claude;
  - nome ou CRO de profissional real;
  - perfil de clínica sem a inscrição da clínica e o responsável técnico (por isso, a série usa o perfil pessoal dela, com o nome do perfil fora do quadro).
- **Tom:**
  - "garantido", "revolucionário", "10x", "feito 100% por IA";
  - slogan dito na narração; pergunta de mentor para quem assiste;
  - "comente X", "manda pra", "link na bio", "fale com a gente";
  - resposta de colega sobre o método ("como você fez isso?");
  - prazo de entrega ("na tarde seguinte", "em um dia"), inclusive escondido: relógio ou data entre o envio e o post;
  - "semana que vem" na narração (a frequência pode mudar);
  - promessa de pacientes ou faturamento.

## 12. Revisão de cada plano (vai para o REVIEW.md)

- [ ] Personagem lado a lado com a folha e a folha de expressões: estilo boneco B (cabeça ~1/3,5 da altura, olhos ovais com pálpebras, pele fosca sem brilho de plástico), coque baixo, faixa grisalha na têmpora **esquerda**, gola padre, relógio no pulso **esquerdo**, cinco dedos, nada laranja.
- [ ] Maquete: borda de madeira e desfoque de miniatura iguais entre os planos; a camada dela com a mesma luz, sombra de contato e escala da placa (não parece colada); no máximo uma etiqueta por vez, nunca laranja.
- [ ] Luz vindo da esquerda; abajur âmbar suave, sem círculo nem bola de luz; única luz fria no celular; pretos ≥ #2B2224; nenhum quadro preto.
- [ ] Nenhuma placa clareada; a tarde é a placa própria.
- [ ] Nenhum texto gerado na imagem; celular de frente, sem inclinação, com as pontas da garra por cima.
- [ ] Laranja só onde a regra permite; no máximo um lima por plano.
- [ ] Até ~20 palavras por tela (contando assinatura e selo); evento de 1 a 3 s, resultado de 1,5 a 2 s; nenhuma sequência de cortes abaixo de 1 s.
- [ ] "Um por um" em uma cena só; um mecanismo diferente por cena.
- [ ] Algo novo a cada 2 a 4 s (`npx hyperframes snapshot --range`).
- [ ] Dobra e impacto na batida (quadros múltiplos de 25 no ep. 01).
- [ ] No máximo 2 sopros; efeitos 1 quadro depois da imagem; sons de interface sem nota musical (`npx hyperframes audio --json`).
- [ ] Teste do mudo aprovado por 3 pessoas que não viram o roteiro.
- [ ] Lista PROIBIDO conferida item por item.
