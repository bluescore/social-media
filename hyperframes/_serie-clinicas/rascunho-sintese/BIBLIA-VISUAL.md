# Bíblia visual — sala de espera

Vale para todos os episódios. O que é só do ep. 01 está em `ep01-ROTEIRO.md`.

---

## 1. Os três mundos

| | **Mundo 1: a noite dela (o problema)** | **Mundo 2: o vídeo dela (o entregue)** | **Mundo 3: a tarde (a vida resolvida)** |
|---|---|---|---|
| Técnica | 2.5D: imagens da OpenAI em camadas (fundo, plano médio, primeiro plano) que a câmera do HyperFrames move com parallax (as camadas mais perto andam mais que as de longe). Interface do celular em HTML. | 3D de verdade (Three.js r184) num palco de estúdio. Renderizado num projeto à parte e trazido para o episódio como sequência PNG, ou seja, quadro a quadro sem perda de qualidade. | 2.5D, com as mesmas regras do Mundo 1 |
| Fundo | consultório escuro: sombras #1E1415, paredes #72605E a 40% de luz | degradê **radial**, de #303236 no centro para #1E1415 nas bordas (o degradê linear cria faixas no H.264) | o mesmo consultório e a recepção, com sol baixo entrando pela persiana |
| Luz | abajur de 2700 K **à esquerda do quadro**, poça âmbar #F28801 a 25–40%. A única luz fria é a da tela do celular (#E8EEF2). Sombras longas. | luz principal quente #FFE4CC vinda de cima à esquerda; contraluz laranja #F34500 de trás à direita; 2 a 3 faixas de luz no ambiente; sombra de contato a 0,55 | listras douradas #F28801 da persiana na parede, vindas da esquerda; sombra levemente azulada; abajur apagado |
| Materiais | jaleco de tecido fosco, papel com fibra, vidro do celular | ver a tabela da seção 7 | os mesmos do Mundo 1 |
| Câmera | equivalente a 35 mm, na altura dos olhos; empurrão lento de 1,00 a 1,04 por plano; parallax em 3 camadas a 12/30/60 px | equivalente a ~50 mm; mergulha no objeto em vez de girar em volta (nunca mais de 30°); gira o ambiente, 3 a 5° por segundo, e não o objeto; o objeto herói ocupa de 45% a 70% da altura | igual ao Mundo 1, mas a câmera fica parada por mais tempo (calma) |
| Acabamento | grão de 3%, vinheta de 8% (por `npx hyperframes media-treatment`, nunca por filtro CSS) | **sem grão e sem vinheta**; bloom (brilho que estoura o branco) desligado ou só nos 2% mais claros | grão de 3%, vinheta de 6% |

**Objeto herói** ocupa pelo menos 40% da altura do quadro em todo plano. Nunca um objeto pequeno solto no escuro.

## 2. A regra fixa: "história" × "vídeo entregue"

> **Imagem em camadas com luz quente = a vida dela. Estúdio escuro com 3D real = o vídeo dela.**
> - O vídeo dela **sempre nasce do fio laranja e da dobra**.
> - Ele vive numa **moldura 9:16 com o fio laranja de 4 px na borda**, com cantos de 48 px em tela cheia e de 22 px dentro do celular.
> - Do primeiro ao último quadro, ele carrega a assinatura dela ("dra. Helena Prado · cirurgiã-dentista · CRO-UF 00000") e o selo "ilustração educativa · feita com apoio de IA".
> - A personagem **nunca** entra no estúdio, e o 3D **nunca** aparece no consultório.
> - Não existe fusão nem corte seco entre os dois mundos: a passagem é sempre por um objeto (a dobra, a tela do celular).
> - O narrador **não fala** enquanto o vídeo dela roda.

## 3. A regra do laranja

- **O laranja #F34500 é a inteligência.** Nada da vida dela é laranja: roupa, caneta, interface do celular, botões, ponto de gravação.
- O primeiro laranja de cada episódio é o fio aparecendo.
- Depois dele, o laranja aparece só:
  - no fio e nas palavras que ele pinta;
  - na moldura e na luz de recorte do vídeo dela;
  - nas linhas-guia dos rótulos;
  - na palavra em Megion.
- **Lima #EFFF57:** um único ponto por plano, só dentro do vídeo dela (a ponta do rótulo principal).
- **Fora da história** (no cartão da série), o laranja volta a ser a cor da marca, em "ep. 0X".

## 4. Planta de cena e luz

- **Antes de gerar qualquer imagem**, desenhar a planta de cada plano: onde estão a câmera, o celular e o rosto dela.
  - A tela com a câmera frontal só aparece para nós se estivermos do lado dela, por cima do ombro.
  - A câmera frontal mostra a imagem espelhada. Por isso, no visor, o lado esquerdo dela (a faixa grisalha) e a luz do abajur aparecem à **esquerda da tela**.
- **A luz principal vem sempre da esquerda do quadro.** Nunca espelhar uma imagem para corrigir um lado trocado: isso inverte a luz. Se o gerador trocar esquerda e direita, gera-se de novo.
- **Uma placa base por lugar + camadas de luz.** O que muda dentro de um plano nasce como camada separada sobre UMA imagem de fundo:
  - o abajur apagando;
  - o brilho da tela;
  - as listras do sol.
  A tarde do consultório é a mesma placa da noite, com três ajustes:
  - o abajur e a poça de luz escurecidos por máscara;
  - a cor mais quente e mais aberta;
  - uma camada de luz de persiana (textura de luz gerada isolada) aplicada em modo "tela" sobre a parede.

## 5. O celular e as telas

- **O aparelho é sempre o mesmo objeto, feito em HTML:**
  - corpo chumbo #303236, cantos de 64 px;
  - sem marca e sem câmera reconhecível;
  - um leve brilho na borda esquerda, vindo do abajur.
- **As imagens geradas só fornecem o que segura o aparelho** (a garra do tripé, a mão dela), com uma placa escura lisa no lugar do celular:
  - a placa é gerada **de frente**, sem inclinação;
  - os 4 cantos são medidos com `scripts/locate.mjs`;
  - o HTML cobre a placa por inteiro.
  Se a geração vier torta, gera-se de novo: a interface nunca é entortada para caber.
- **As interfaces são genéricas:** nada que imite Instagram, WhatsApp, ChatGPT, Claude ou iPhone. O texto fica em minúsculas, nas cores #F6F4F1, #303236 e #72605E, sem laranja e sem vermelho.

## 6. A personagem principal: dra. Helena Prado

**O que NUNCA muda**
- **Proporção:** adulta; a cabeça mede 1/7 da altura; mãos de tamanho real, com cinco dedos.
- **Rosto:**
  - oval, pele morena média de tom quente (≈ #B9825F, conferida na composição);
  - sobrancelhas retas e escuras, olhos amendoados de tamanho humano;
  - nariz pequeno e reto, boca sóbria e fechada, poucos traços;
  - acabamento de porcelana ou vinil fosco de colecionador, com a pele levemente translúcida (a luz entra um pouco e ela não parece plástico).
- **Cabelo:** castanho quase preto, preso num **coque baixo na nuca**, com **uma faixa grisalha larga que sai da têmpora ESQUERDA dela e vai presa até o coque**.
  - Não há mecha solta: uma mecha solta muda de forma a cada imagem gerada, e a faixa presa fica estável.
- **Roupa:**
  - jaleco branco-osso #F6F4F1, fosco, até o meio da coxa, com **gola padre** (mandarim), botões escondidos e mangas dobradas uma vez;
  - blusa chumbo #303236 de gola alta; calça reta chumbo; sapatos baixos chumbo;
  - relógio fino de couro marrom no **pulso esquerdo**; caneta chumbo no bolso do peito esquerdo;
  - sem óculos, sem brincos, sem joias, sem crachá, sem logo, sem nome bordado. **Nada laranja.**
- **Idade aparente:** 44 anos.

**Expressões aprovadas (6):** concentrada; cansada (pálpebras pesadas, ombros caídos); olhos fechados de frustração contida; surpresa contida (as sobrancelhas sobem pouco, boca fechada); sorriso de canto de boca fechada; tranquila olhando para baixo.

**Onde ela aparece**
- O rosto em close aparece **só dentro de telas** (o visor da câmera frontal).
- No mundo da história, ela aparece só de três jeitos: por cima do ombro, de costas ou como sombra.
- As mãos aparecem só segurando um objeto, em plano médio. Nunca em close de dedos.

**Nunca**
- boca aberta falando ou dentes à mostra;
- olhar fixo falando para a câmera;
- olhos grandes "de desenho", cabeçorra, cílios exagerados;
- trocar o penteado, perder a faixa grisalha ou trocar a cor do jaleco;
- pôr laranja nela.

**Como trocar de expressão sem "pular"**
- A expressão nova é gerada como edição ("mude só os olhos").
- No vídeo entra **só a região alterada** (olhos ou boca), recortada com borda suave e colada sobre a imagem original.
- A troca é um "take" em 4 tempos: antecipa, comprime, troca o rosto e assenta.

### Prompt da folha de personagem

Para `gerar-imagem.mjs`, em 2560x1440, fundo opaco cinza-claro. O texto do pedido fica em inglês porque o modelo responde com mais precisão.

```
Character model sheet of ONE fictional adult woman: a Brazilian dental surgeon (implant specialist), 44 years old.
Style: premium stylized 3D feature-film character with a matte porcelain / designer-vinyl finish. Soft subsurface skin
(light enters the skin slightly; never plastic shine). Realistic adult proportions: head = 1/7 of body height,
human-sized almond eyes, minimal facial features. NOT cartoon, NOT big-eyed, NOT big-headed, NOT chibi, NOT clay.
Face: oval; warm medium-brown skin; straight dark eyebrows; small straight nose; calm closed mouth, no teeth showing.
Hair: very dark brown, pulled back into a LOW BUN at the nape. ONE wide streak of grey hair starts at her own LEFT
temple and is swept back into the bun (in the front view it appears on the image's RIGHT side). No loose strands.
Outfit: bone-white matte lab coat (#F6F4F1) to mid-thigh with a MANDARIN (band) collar, closed with hidden buttons,
sleeves folded once to the forearm; charcoal (#303236) high-neck top underneath; straight charcoal trousers;
low charcoal shoes; thin brown leather watch on her LEFT wrist; a charcoal pen clipped to the left chest pocket.
Nothing orange on her. No glasses, no earrings, no jewelry, no badge, no logo, no embroidered name, no text.
Layout: four full-body views side by side at the same scale and height: front, three-quarter front, left profile,
back. Neutral standing pose, arms relaxed, five fingers on each hand.
Light: soft even studio light from the upper LEFT; light grey seamless background (#E6E3DF); a soft contact shadow
under each figure, no other shadows between the views.
Character Consistency: same face, same grey streak, same low bun, same coat and collar, same proportions in all views.
Constraints: no text, no labels, no numbers, no frames, no watermark, no extra people, no props besides pen and watch.
```

**Como gerar:**
- **Rascunhos** (4 opções, cerca de US$ 0,005 cada):
  `node ferramentas\openai\gerar-imagem.mjs --prompt-arquivo hyperframes\_serie-clinicas\personagens\dra-helena\prompts\folha.txt --saida hyperframes\_serie-clinicas\personagens\dra-helena\rascunhos\folha.png --rascunho --n 4 --tamanho 1536x864`
- **Final** (2 opções, depois que o dono escolher):
  `... --modelo gpt-image-2.6-sunburst --qualidade xhigh --tamanho 2560x1440 --fundo opaque --n 2`

### Prompt da folha de expressões (2048x1152, com `--ref` da folha aprovada)

```
Image 1 = approved character model sheet. Do not redesign the character.
Expression sheet of the SAME woman: six head-and-shoulders busts in a 3x2 grid, same scale, same three-quarter
front angle, same soft studio light from the upper LEFT, light grey seamless background (#E6E3DF).
Top row: (1) focused; (2) tired, heavy eyelids, shoulders slightly dropped; (3) eyes closed, quiet frustration,
jaw tense. Bottom row: (4) restrained surprise, eyebrows raised slightly, mouth closed; (5) small closed-mouth
half smile; (6) calm, looking down.
Keep exactly: face, grey streak from her LEFT temple into the low bun, mandarin-collar bone-white coat, charcoal
high-neck top, skin tone, matte porcelain/vinyl finish. Mouth always closed, no teeth. Nothing orange.
No text, no labels, no numbers, no frames, no watermark.
```

### Bloco fixo para toda pose

Toda pose sai de um pedido de edição com `--ref folha.png --ref expressoes.png`. **A personagem nunca é gerada do zero num plano novo.**

```
Image 1 = approved character model sheet. Image 2 = approved expression sheet.
Do not redesign the character. Change ONLY the pose, framing and light described below.
Keep exactly: face; one wide grey streak from her own LEFT temple swept into a LOW BUN; bone-white matte lab coat
with mandarin collar and hidden buttons; charcoal high-neck top; brown leather watch on her LEFT wrist; charcoal
pen in the left chest pocket; adult proportions; skin tone; matte porcelain/vinyl finish. Nothing orange on her.
Mouth closed. Five fingers on each visible hand. No text anywhere.
POSE: <...>
LIGHT: <...>
BACKGROUND: transparent, isolated subject, no floor, no cast shadow
```

**Exemplo, o visor da cena 1 do ep. 01:**
- POSE: *chest-up, seen as a phone front-camera selfie preview (mirror view), centered, eyes closed, jaw tense, shoulders slightly raised; in this mirror view the grey streak appears on the LEFT side of the image.*
- LIGHT: *warm 2700 K table-lamp light from the LEFT of the image; cool bluish phone-screen light on the face from the front; deep shadows; late night.*

### Pedido de cenário (modelo)

```
Premium stylized 3D film set, same matte material language as the character. No people.
Dental office at night, seen at eye level from where a person would stand, 35 mm lens.
LEFT third: a work counter with a warm 2700 K table lamp switched on; EMPTY counter surface (no paper, no objects).
RIGHT third: a generic, unbranded dental chair, empty, in shadow. Back wall in deep shadow.
CENTER: empty floor space (a tripod is added later as a separate layer).
Deep shadows, one warm pool of light from the lamp, no other light source.
No text, no logos, no screens, no instruments, no people.
```

**Antes de aprovar uma imagem:**
- conferir se a transparência veio de verdade (um xadrez desenhado não é transparência); plano B: `npx hyperframes remove-background`;
- registrar o modelo e a data, porque o 2.6 não tem versão congelada.

## 7. Materiais do vídeo dela (3D)

| Peça | Material | Números |
|---|---|---|
| implantes e barra (feitos em código) | titânio acetinado #B9BEC4 | metal 1, aspereza 0,45, ambiente 0,5 |
| dentes da prótese (modelo escaneado) | porcelana #F6F4F1 | aspereza 0,32, verniz 0,4 |
| base da prótese | resina rosada fosca #E3C3BA, levemente translúcida (nunca porcelana branca) | aspereza 0,6 |
| osso (modelo escaneado) | vidro fosco menta #88D09D | transmissão 0,55; "janelas" que limpam o fosco localmente |
| face cortada | chumbo #303236, sólida, com trama de osso esponjoso em menta | tampas pela técnica de stencil do three.js (para o osso cortado não parecer oco); ruído com semente |
| contraluz | laranja #F34500 | de trás à direita |
| destaque | lima #EFFF57 | um ponto de 10 px por plano |

**Orgânico (dente, osso, gengiva) nunca é feito em código:** a coroa do teste `f29.png` virou uma "bolha". Em código entram só peças mecânicas, e a base da prótese só depois de uma imagem parada aprovada pelo dono.

## 8. Tipografia na tela (1080×1920)

**Regras gerais:**
- Helvetica Now Text, letter-spacing −0,05em, line-height 0,9.
- Tudo minúsculo, exceto nomes próprios e siglas (Helena, CRO-UF, IA).
- Nenhum ponto final.
- Texto só entre y=168 e y=1330. Abaixo de y=1000, nada à direita de x=930. Nada para ler com menos de 28 px.
- Nenhum texto dentro das imagens geradas: todo texto é HTML.

| Uso | Fonte | Tamanho | Cor | Posição |
|---|---|---|---|---|
| Legenda da história | Regular; Bold só na palavra-chave (Bold branco, sem laranja) | 60 px, até 2 linhas e 8 palavras | #F6F4F1, sombra local suave (0 2 18 px, #1E1415 a 60%) | x=108, base fixa em y=1220, largura até 760 px |
| Palavra em Megion | Megion Bold, CAIXA ALTA | 240 px | #F34500 | centro óptico, y≈760; **uma por episódio** |
| Título do vídeo dela | Regular, uma palavra em Bold | 72 px, até 2 linhas e 7 palavras | #F6F4F1 | topo do bloco em y=300, x=108 |
| Linha de apoio do vídeo dela | Regular | 44 px | #F6F4F1 a 80% | logo abaixo do título |
| Rótulo de peça 3D | Regular | 40 px | #F6F4F1, linha-guia de 2 px #F34500, ponto lima | junto da peça, entre y=500 e y=1100 |
| Assinatura dela (fixa) | Regular | 30 px | #F6F4F1 a 80% | x=108, y=1180 |
| Selo de IA (fixo) | Regular | 28 px | #F6F4F1 a 70% | x=108, y=1290 |
| Cartela final do vídeo dela | nome em Bold 56 px; demais linhas em Regular 36 px | — | #F6F4F1 | bloco à esquerda, base em y=1220 |
| Folha impressa (objeto de cena) | Regular | 34–48 px efetivos | #303236; palavras pintadas pelo fio em Bold #F34500 | sobre o papel |
| Interface do celular | Regular e Bold | 34–44 px efetivos | #F6F4F1, #303236, #72605E | dentro da tela |
| Cartão da série | "sala de espera ·" Regular 72 px + "ep. 01" Bold 72 px #F34500; próximo episódio em Regular 40 px a 80%; aviso em 28 px a 60% | — | #F6F4F1 | ícone de 56 px em y=700, título em y=820, próximo em y=960, aviso em y=1290 |

**Quantidade de texto:**
- até 8 palavras por legenda;
- até ~20 palavras legíveis por tela (contando assinatura e selo);
- cada linha segura 0,5 s + 0,3 s por palavra, e a última frase do filme segura pelo menos 2 s.

**A legenda complementa a voz:** diz a virada com outras palavras, nunca repete a narração palavra por palavra.

**Teste do mudo:** lendo só o que está na tela, na ordem, a história inteira precisa fazer sentido.

## 9. Movimento

- **Ritmo:**
  - cada evento legível dura de 1 a 3 s, e o resultado segura de 1,5 a 2 s;
  - algo novo a cada 2 a 4 s, sem sequência de cortes abaixo de 1 s;
  - um mecanismo de movimento diferente por cena.
- **Ease por papel:**
  - chegada com cauda longa (`expo.out`);
  - câmera e mudanças de luz nos dois sentidos (`power2.inOut`);
  - atravessar ou sair acelerando (`power3.in`).
  Título pousado fica parado.
- **Transições, sempre com causa na tela, em 5 famílias:**
  1. o movimento contínuo da câmera;
  2. o corte pela luz (mergulho na luz, apagão);
  3. a troca na mesma tela (desfoque);
  4. o objeto que vira o mundo e o levar junto (a moldura);
  5. o corte seco casado (no máximo um terço das emendas).
- **Ação física** (ela andar, riscar, pegar o celular) nunca é feita com um recorte parado deslizando. Ela é mostrada:
  - pela tela do celular;
  - pela sombra;
  - pelo som;
  - ou por um corte na ação entre 2 poses-chave com borrão de movimento.
- **Se o dono disser "rápido demais":** cada zoom e movimento de câmera fica 0,7× mais lento, e nada mais muda.

## 10. Som (resumo)

- A voz A.Medeiros é o relógio: a voz é gravada primeiro e a imagem se ajusta a ela.
- A trilha começa leve, cresce e tem UM impacto, na 3ª dobra.
- **Cada efeito tem causa na tela** e cai 1 quadro depois da imagem.
- No máximo **2 sons de deslocamento de ar** ("sopros") por episódio. As outras transições soam como o material que se move: papel, vidro, titânio.
- Sons repetidos alternam 2 ou 3 tomadas. Os 3 sons de dobra são arquivos fixos da série.
- Nada de tons sintetizados, "plins" ou sinos.

## 11. PROIBIDO (lista nominal)

- **Personagem:**
  - boca mexendo ou fala sincronizada (lip sync); olhar fixo falando para a câmera;
  - olhos grandes brilhantes, cabeçorra, pele de borracha;
  - rosto diferente entre planos; close de mãos e dedos; dedos errados;
  - qualquer laranja nela; mudar o coque, a faixa grisalha ou o jaleco;
  - espelhar uma imagem para corrigir o lado.
- **Estilos:**
  - massinha pastel, ícone 3D fofo, diorama isométrico vetorial, low poly;
  - dente ou alimento falante;
  - robô, cérebro azul, circuitos ou holograma como símbolo de IA;
  - as palavras "Pixar" e "Disney" em qualquer pedido.
- **Clichês de vídeo gerado:**
  - vazio escuro com objeto pequeno (menos de 40% do quadro);
  - glow, bloom forte, lens flare, partículas, orbes;
  - degradê roxo ou azul; degradê linear no fundo escuro;
  - cards de vidro, três cards em fila, logo no canto, molduras decorativas, painel de controle;
  - tudo entrando com "aparece e sobe"; título que continua deslizando depois de pousar; respiração ou flutuação em título e interface;
  - Ken Burns (zoom lento em foto parada) como único movimento;
  - fusão entre mundos;
  - caixa de prompt, cursor de agente ou tela de chat de IA;
  - o mesmo "whoosh" em todo corte;
  - recorte parado deslizando para fazer ação física;
  - texto gerado dentro da imagem.
- **Legenda:**
  - karaokê amarelo com contorno;
  - repetir a narração palavra por palavra;
  - texto que se mexe enquanto é lido;
  - ponto final;
  - mais de 8 palavras por legenda.
- **Clínico:**
  - sangue, incisão, gengiva aberta, broca ou instrumento; mão operando; boca realista (lábio, língua, saliva);
  - paciente, nem desenhado (a cadeira está sempre vazia);
  - **implante descendo, entrando ou sendo parafusado no osso**; parafuso girando; 4 implantes com os de trás inclinados;
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
  - prazo de entrega ("na tarde seguinte", "em um dia");
  - promessa de pacientes ou faturamento.

## 12. Revisão de cada plano (vai para o REVIEW.md)

- [ ] Personagem lado a lado com a folha: coque baixo, faixa grisalha na têmpora **esquerda**, gola padre, relógio no pulso **esquerdo**, cinco dedos, nada laranja.
- [ ] Luz vindo da esquerda; abajur âmbar; única luz fria no celular.
- [ ] Nenhum texto gerado na imagem; celular de frente, sem inclinação.
- [ ] Laranja só onde a regra permite; no máximo um lima por plano.
- [ ] Até ~20 palavras por tela; evento de 1 a 3 s, resultado de 1,5 a 2 s; nenhuma sequência de cortes abaixo de 1 s.
- [ ] Algo novo a cada 2 a 4 s (`npx hyperframes snapshot --range`).
- [ ] No máximo 2 sopros; efeitos 1 quadro depois da imagem (`npx hyperframes audio --json`).
- [ ] Teste do mudo aprovado por 3 pessoas que não viram o roteiro.
- [ ] Lista PROIBIDO conferida item por item.
