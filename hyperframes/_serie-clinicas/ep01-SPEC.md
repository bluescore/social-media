# sala de espera · ep. 01 — "o roteiro parado" · SPEC

Documento de produção, com todos os números. O dono aprova pelo `ep01-ROTEIRO.md` (curto); este arquivo é o que se segue na hora de fazer. Versão de 11/11/2026, depois das duas revisões críticas (`rascunho-sintese\CRITICAS.md`), **atualizada em 12/11/2026 para a direção visual v2** (`DIRECAO-VISUAL-v2.md`: a vida dela é uma maquete com a Helena-boneca; o vídeo dela é realista). Na v2 mudam as imagens, a planta e alguns mecanismos; tempos, narração e textos ficam iguais. As regras gerais da série estão em `BIBLIA-VISUAL.md` e `LINHA-EDITORIAL.md`.

---

## 0. Números-chave

- **Duração:** 69,2 s = 2.076 quadros a 30 por segundo. Vertical 1080×1920, MP4 H.264.
- **Narração:** voz A.Medeiros, 3ª pessoa, **75 palavras** (cerca de 430 caracteres; ~34 s de fala). A voz se cala de 29,9 s a 47,3 s.
- **Trilha:** 72 BPM (batidas por minuto) = **uma batida a cada 25 quadros** (0,833 s). A grade de batidas é contada desde o quadro 0: quadros 0, 25, 50, 75...
- **Impacto único: quadro 975 (32,50 s)**, 39 batidas depois do quadro 0 (a grade conta o quadro 0 como batida 0), no fim do 3º tempo da dobra.
  - Por que 32,5 e não 32,3: a correção da dobra dava ≈32,3 s na linha do tempo antiga. Somando a cena 3 (+1,2 s) e a cena 4 (−1,1 s), cairia em ≈32,43 s (quadro 973). Arredondei para o quadro 975: a grade de batidas fica "a cada 25 quadros desde o quadro 0", fácil de conferir, e a folha ganha 2 quadros para subir antes da 1ª dobra.
- **Como a linha do tempo mudou desde o rascunho (68,0 s):** cena 3 +1,2 s (a 3ª data riscada fica parada 1,6 s) · cena 4 −1,1 s (a fala foi cortada) · cena 6 +0,2 s (as 4 palavras pintadas ficam paradas) · dobra +0,4 s (cada tempo 0,7 s, na batida) · dedicatória +0,5 s → **69,2 s**, dentro do tipo A (60–70 s).

**Eventos na batida** (quadro = múltiplo de 25):

| Quadro | Tempo (s) | Evento |
|---|---|---|
| 900 | 30,00 | dobra 1 começa |
| 925 | 30,83 | dobra 2 começa |
| 950 | 31,67 | giro começa |
| 975 | 32,50 | **IMPACTO** · o vídeo dela começa |
| 1450 | 48,33 | "último post · agora" |
| 1550 | 51,67 | balão "encaminhado" |
| 1600 | 53,33 | "Lúcia: ficou com a sua cara" |
| 1775 | 59,17 | "faltava a forma" pousa |
| 1850 | 61,67 | dedicatória entra |
| 1925 | 64,17 | a imagem começa a escurecer para o cartão |
| 1950 | 65,00 | o cartão é revelado pela máscara |

Antes do impacto, a voz manda: os textos caem na batida mais próxima quando isso não tira tempo de leitura. Dentro do vídeo dela, as trocas de passo seguem o tempo de leitura (a trilha está sustentada, sem acento). Depois de escolhida a tomada da voz, a tabela inteira se ajusta à voz real (`narracao.json`), mantendo o impacto no quadro de uma batida.

---

## 1. A regra visual do episódio

- **A vida dela** é uma **maquete de mesa** com a Helena-boneca dentro, feita em camadas (2.5D: placas da maquete sem personagem + a personagem como camada com a mesma luz, que a câmera move para dar volume), filmada como lente macro, com desfoque de miniatura em cima e embaixo, luz de abajur suave e espalhada (sem holofote, sem círculo, sem bola de luz) e grão. A noite é clara: nenhum preto abaixo de #2B2224 em área grande, e nunca um quadro preto.
- **O vídeo dela** é realista, num estúdio cinza-grafite (degradê de #44464B no alto a #2A2C30 embaixo). No corte de 10 s, ele sai de imagens geradas em camadas (seção 9.3); no completo, as mesmas camadas, com Three.js + modelos do Sketchfab como evolução se o teste mostrar que vale a pena. Enquanto é cartão, tem a moldura do fio laranja; em tela cheia, fica sem moldura. A assinatura e o selo de IA ficam na tela do primeiro ao último quadro.
- **Na dobra, o brinquedo vira o real:** a folha de papel sai da maquete, vira a tela e, no impacto, o material muda (papel, madeira e tecido → vidro, titânio e porcelana).
- Só se passa de um mundo para o outro por um objeto (a dobra, a tela do celular). Nunca há fusão.
- **O laranja #F34500 é a inteligência.** Nada da vida dela é laranja. O primeiro laranja do episódio aparece aos 26,2 s: é o fio.
- **Sem Megion no episódio.** A frase da virada é Helvetica, com a palavra-chave em Bold laranja.
- **O truque "um por um"** aparece só na cena 6 (o fio lendo).
- **Etiquetas da maquete** (no máximo uma por vez, nunca laranja, contam nas ~20 palavras da tela; estilo na BIBLIA, seção 8). No ep. 01 são opcionais e só repetem um texto da interface que ficou pequeno demais na prévia. Candidata: "último post · agora" na cena 9, se o celular do balcão ficar pequeno. Ficam de fora: "take 14" na cena 1 (o "● take 14" da interface já está grande; a direção v2 deixa opcional), "take 15" no fim do recuo (a legenda ocupa até 9,17 s e não sobra o tempo de leitura) e "pronto há 6 semanas" na folha (repetiria a narração da cena 3, o que a regra da legenda proíbe).

## 2. Planta de cena (definida antes de gerar qualquer imagem)

| Cenas | Câmera (nós) | Celular | Ela (Helena-boneca) | Luz |
|---|---|---|---|---|
| 1 (noite) | de frente para o celular, perto, na altura dele (lente macro); ainda não se vê que é maquete | no tripé da maquete, no centro, com a **tela virada para nós**; ocupa de y=300 a y=1400 | no visor, do peito para cima; e atrás e à esquerda do tripé, de corpo inteiro, desfocada a 18 px, olhando para o celular (como em `v2-capa-B.png`) | abajur da maquete à esquerda do quadro; luz suave por toda a largura (100% → 45%) |
| 2 (noite) | recua e sobe até ver a maquete inteira sobre a mesa, um pouco de cima, em 3/4 (como quem se debruça sobre a mesa) | o mesmo, no centro da maquete | de corpo inteiro, ao lado do tripé (à esquerda dele) | a mesma; em volta da maquete, a sala de verdade, quente e desfocada |
| 3, 5 (fim), 6, 7 | sobre a bancada da maquete, quase de cima (15° da vertical) | fora do quadro | na cena 3, só a mão-boneca com a caneta, entrando pela borda de baixo, à direita; no fim da cena 5 (25,3–26,1), de costas e vista de cima (coque com a faixa grisalha, ombro e o braço esquerdo esticado até o abajur), desfocada na borda esquerda de baixo | abajur da esquerda, suave pela folha inteira; depois que ela apaga o abajur (25,5 s), luz fria da rua pela persiana, a 30% |
| 4, 5 | de frente para a tela; a tela ocupa de y=200 a y=1110 | é o quadro | — | luz fria da tela |
| 9, 10 (tarde) | na maquete da recepção, à altura do balcão | num suporte simples sobre o balcão, de frente; nenhuma mão em quadro | de costas, da cintura para cima, desfocada à esquerda | sol baixo pela persiana, vindo da esquerda |
| 11 (tarde) | no mesmo lugar do fim da cena 2 (maquete inteira) | não aparece; o tripé está fechado e encostado na parede | de corpo inteiro, atravessa a maquete andando, da esquerda para a direita, e sai | listras douradas vindas da esquerda; abajur apagado (placa própria C1-tarde) |

**A decidir no quadro 0 (planta da cena 1):** com a tela virada para nós e ela atrás do tripé, quem a filma é a **câmera traseira**: o visor **não** é espelhado (a faixa grisalha aparece à direita, igual ao corpo dela atrás) e a tela não ilumina o rosto dela. Isso contraria o "visor em espelho" da direção v2 (seção 5), que vinha da planta da v1 (nós por cima do ombro dela, câmera frontal). Recomendado: câmera traseira, porque bate com a capa B aprovada e deixa a faixa do mesmo lado no visor e no corpo. Nesse caso, o toque em "apagar" (2,23 s) é dado pela mão-boneca dela, que entra desfocada pela borda esquerda do celular (q60–q75, 2 poses-chave: chegando e tocando), ou fica só na interface e no som se a mão atrapalhar a leitura do painel.

---

## 3. Os primeiros 4 segundos, quadro a quadro

q = quadro; 30 quadros = 1 segundo.

- **q0 (0,00 s): já é a capa.**
  - Um celular genérico em HTML (corpo chumbo #303236, cantos de 64 px, sem marca) está preso pela garra de um tripé, de frente, ocupando **de y=300 a y=1400** (57% da altura; a tela tem ~480 px de largura). As pontas da garra ficam por cima do corpo do celular (camada recortada).
  - A tela mostra a câmera (traseira, sem espelho; ver a nota da seção 2): a Helena-boneca do peito para cima, olhos fechados (expressão 2 da folha), ombros um pouco erguidos, com a luz âmbar do abajur vindo da esquerda da imagem. O rosto ocupa cerca de 19% da altura do quadro; é o único close de rosto do episódio (pose aprovada).
  - Atrás e à esquerda do tripé, a mesma Helena-boneca de corpo inteiro, desfocada a 18 px, olhando para o celular.
  - Um reflexo largo e suave do abajur no vidro fica por cima, a 10% (uma faixa, não uma bola).
  - Na interface: **"● take 14" em Bold 60 px** #F6F4F1 no topo esquerdo da tela, e "23:47" em Regular 40 px no topo direito. O ponto de gravação é branco.
  - Em volta, o consultório desfocado a 18 px (ainda não se vê que é maquete: a revelação é na cena 2), com a luz âmbar do abajur à esquerda, desfocada e sem forma de bola. Grão de 3%, vinheta de 8%.
  - A câmera já se move: empurrão de 1,00 para 1,02 até os 3,8 s, para a capa não parecer congelada.
- **q3 (0,10 s):** a voz entra: "décima quarta tentativa."
- **q0–q11:** dentro da tela, só a respiração dela: escala vertical de 1% na camada dela, num ciclo de 1,6 s (a Helena desfocada atrás do tripé respira junto, com a mesma curva).
- **q12–q21 (0,40–0,70 s): ela abre os olhos**, com 3 estados de pálpebra trocados como camada (borda suave, só dentro do recorte dos olhos e das sobrancelhas):
  - q12: antecipa, com os ombros subindo 1%;
  - pálpebras fechadas até q13; a meio em q14–q15; abertas de q16 em diante (expressão 1, cansada); cada troca com 2 quadros de passagem suave;
  - q18: os ombros afundam 1%; q21: assentam. Olhar cansado, direto para a lente. A Helena desfocada atrás acompanha só os ombros (o desfoque esconde o rosto).
- **q22–q23:** segura.
- **q24–q36 (0,80–1,20 s):** o painel "apagar vídeo?" sobe da base da tela (`expo.out`) só até o meio da tela, com o texto entre y=1050 e y=1250. Painel chumbo a 92%; "apagar vídeo?" em Regular 44 px; os botões "cancelar" e "apagar" em Bold 44 px #F6F4F1.
- **q36–q66 (1,20–2,20 s):** o painel fica parado e legível.
- **q45 (1,50 s):** a voz termina "tentativa".
- **q60 (2,00 s):** a voz segue: "e o vídeo não sai."
- **q66–q69 (2,20–2,30 s):** o botão "apagar" afunda (escala 0,97, 15% mais escuro), com um toque seco de dedo no vidro em **q67 (2,23 s)**. (Com a câmera traseira, a mão-boneca dela entra desfocada pela borda esquerda do celular em q60 e sai em q75, em 2 poses-chave; ver a nota da seção 2.)
- **q69–q75 (2,30–2,50 s):** o painel desce; **em q75 (2,50 s) a prévia ao vivo volta**, com ela de olhos abertos.
- **q90–q99 (3,00–3,30 s):** o contador rola de "take 14" para "take 15" como caça-níquel e para seco; tique seco em q93 (3,10 s).
- **q108 (3,60 s):** a voz termina "sai."

---

## 4. Tabela de cenas

| # | Tempo (s) | O que se vê | Movimento (um mecanismo por cena) | Texto na tela (exato) | Narração (exata · palavras) | Som |
|---|---|---|---|---|---|---|
| 1 | 0,0–4,0 | O celular no tripé da maquete, grande no quadro; na tela, a Helena-boneca de olhos fechados; atrás e à esquerda do tripé, ela mesma de corpo inteiro, desfocada. Ela abre os olhos (0,4–0,7); sobe "apagar vídeo?" (0,8–1,2), parado até 2,2; ela toca em "apagar" (2,23); a prévia volta (2,5); o contador vira "take 15" (3,0–3,3). | **CONTAR**: o número do take rola como caça-níquel de 3,0 a 3,3 s e para seco. Câmera: empurrão 1,00→1,02. | interface: "● take 14" · "23:47" · "apagar vídeo?" · "cancelar" · "apagar" · "take 15" | "décima quarta tentativa." (0,10–1,50) "e o vídeo não sai." (2,00–3,60) **(8)** | Ambiente do consultório à noite (zumbido baixo de aparelho, −40 dB). Toque seco no vidro em 2,23; tique seco do contador em 3,10. Sem música até a trilha entrar (entre 3,5 e 5,0 s; ver cena 2). |
| 2 | 4,0–10,0 | A câmera recua e sobe, e **revela que tudo é uma maquete sobre uma mesa**: uma caixa com duas paredes e o piso, a borda de madeira à vista, a sala de verdade desfocada em volta. Dentro dela, o celular no tripé no meio, ainda mostrando o rosto dela; a Helena-boneca de corpo inteiro ao lado do tripé (à esquerda), olhando para ele; à esquerda, a bancada com o abajur aceso e a folha impressa; à direita, a cadeira odontológica genérica e vazia. De 8,0 a 9,2 s o foco corre do celular para a folha. | **RECUO QUE REVELA A MAQUETE** (4,0–6,6, `power2.inOut`, borrão de movimento ligado): a borda de madeira entra pelas laterais e por baixo por volta de 5,4 s, e é aí que o espectador entende que é uma maquete. Escala de cada camada no começo, em relação ao enquadramento final (1,0 para todas; valores a conferir na prévia): celular e tripé 2,50; Helena 2,40; interior da maquete (bancada, cadeira, parede) 2,08; borda de madeira e mesa 2,20 (mais perto da câmera que o interior); a sala em volta, desfocada, 1,82. O desfoque de miniatura cresce junto (em cima e embaixo do quadro). | legenda (6,67–9,17): "na cadeira, ela explica **de cor**" | "a doutora Helena explica a prótese protocolo toda semana, paciente por paciente." **(12)** · 4,40–9,90 | A trilha entra onde cair, entre 3,5 e 5,0 s, com entrada suave de 1,0 s: uma nota grave de piano a cada 2 batidas, volume 0,10. Sopro grave curto no recuo (sopro 1 de 2). |
| 3 | 10,0–17,2 | **10,0–10,5:** inclinação rápida para baixo, com borrão de movimento vertical de até 24 px: a placa C1 sai por cima, a C2 entra por baixo, e a troca de placa acontece no quadro de maior borrão (10,25). A câmera desacelera até a folha (10,5–11,2, `expo.out`). A folha aparece quase de cima, sobre a bancada da maquete (a madeira em miniatura em volta, com desfoque de miniatura nas bordas de cima e de baixo), ocupando 84% da largura, girada 3°, sob a luz do abajur, que vem da esquerda e cai suave pela folha inteira. Em foco: "roteiro · protocolo sobre implantes" e, na margem, "gravar 23/10" e "gravar 30/10" já riscadas e "gravar 06/11" ainda inteira. As linhas do roteiro ficam em desfoque leve. De 13,8 a 14,6 s a sombra da mão dela chega pela borda de baixo, à direita; de 14,6 a 15,2 a **mão-boneca com a caneta** entra (2 poses-chave com borrão: chegando; caneta pousada no começo da data). **De 15,6 a 17,2 a folha com as três datas riscadas fica parada, sem câmera**; a mão fica parada à direita da data, sem cobrir texto. Em 16,9 a luz fria do celular invade a borda da folha (0,3 s), sem chegar às datas riscadas, que seguem legíveis até o corte. | **RISCAR COM A MÃO-BONECA**: um traço de caneta ondulado (5 px, chumbo, em HTML) atravessa "gravar 06/11" em 0,35 s (15,25–15,60), caindo no "não", enquanto a mão passa por 3 poses-chave (começo, meio e fim da palavra), trocadas a cada 3 quadros com borrão de movimento; nunca uma mão parada deslizando. Câmera: avanço lento de 1,00 a 1,04 (11,2–15,25), depois parada. | só a folha impressa (cerca de 10 palavras em foco, 44–48 px efetivos) | "o roteiro sobre implantes está pronto há seis semanas." (10,10–14,30) "a gravação, não." (14,50–15,80) **(12)** | Papel farfalhando de leve em 10,3 (o som da passagem é o material que chega). A 2ª voz do piano entra perto de 12,5 (aproximado, conforme a trilha). Risco de caneta em 15,26. |
| 4 | 17,2–20,6 | A imagem corta para a tela, de frente. É screenlife: a história contada pela tela do celular. Perfil genérico, sem logo e com o nome fora do quadro: uma grade de posts em retângulos verticais 9:16, em tons apagados (#72605E, #303236, #F6F4F1 a 30%). A tela rola e para no último post. | **ROLAR A TELA**: rolagem com inércia de 1,0 s (17,33–18,33) e parada seca. Entrada: corte pela luz, com a imagem escurecendo 40% por 3 quadros. | interface (18,33–20,6): "último post · há 47 dias" | — (sem fala) | Toque seco no vidro em 17,27; atrito suave da rolagem; as cordas entram perto de 18,3 (aproximado), volume 0,12. |
| 5 | 20,6–26,1 | A mesma tela passa para a câmera traseira: o visor enquadra a folha na bancada, com uma leve oscilação de mão (2 px, só dentro do visor). Clique: a foto vira um balão numa conversa escura (o nome do destinatário fica fora do quadro), com "enviado · 23:52", parado até 25,3. **Em 25,3 a tela do celular apaga** e o quadro corta para a folha na bancada da maquete (C2), ainda sob o abajur, um pouco mais aberta (escala 0,9) para caber o abajur no canto de cima, à esquerda; **a Helena-boneca está de costas**, vista de cima e desfocada na borda esquerda de baixo (coque com a faixa grisalha, ombro), com o braço esquerdo esticado até o abajur (pose 1). **Em 25,5 ela apaga o abajur**: a luz desce a 30% em 0,4 s, e a folha continua visível, em cinza #3A3233, na luz fria e fraca da rua que entra pela persiana. Em 25,9 ela recolhe o braço (pose 2, corte na ação com borrão) e sai pela borda esquerda (26,0–26,1, com borrão); a câmera fecha de 0,9 para 1,0 até 26,2 (`power2.inOut`). | **OBTURADOR + APAGAR O ABAJUR**: a tela fecha de cima e de baixo como um obturador e reabre, em 0,15 s (22,5); a luz desce em 0,4 s (25,5–25,9, `power2.inOut`), nunca até o preto; a mão dela no interruptor é a causa na tela. | interface: "enviado · 23:52" (22,9–25,3) · legenda (23,33–25,3): "**sem** gravar de novo" | "ela não gravou a décima quinta." (20,90–23,00) "mandou só o roteiro." (23,40–25,30) **(10)** | Obturador em 22,5; "enviado" (toque seco) em 22,9; clique do interruptor do abajur em 25,5. Um pulso grave de 72 BPM entra perto de 24 s (aproximado). |
| 6 | 26,1–29,5 | Na luz fria, com a folha inteira visível, um ponto laranja acende no canto da folha (26,2): é o fio, o primeiro laranja do filme. Ele percorre o contorno da folha, e a luz dele revela 30 px de papel em volta (sem brilho estourado). Depois desce pela margem como uma régua de leitura e pinta de Bold laranja 4 palavras-chave; a linha 2 ("tomografia") fica sem pintar. As linhas seguem em desfoque leve, como na cena 3: nítidos, só o título, as datas riscadas e cada palavra pintada (~14 palavras legíveis). As 4 palavras ficam paradas de 28,6 a 29,5 (e continuam visíveis até o giro, em 31,7). | **SUBLINHAR** (o único "um por um" do episódio): contorno em 0,8 s (26,2–27,0); "arcada" 27,0 · "implantes" 27,4 · "osseointegração" 27,8 · "parafusada" 28,2. Cada palavra já está composta numa caixa com a largura da versão Bold: o fio troca só o peso e a cor, e nada em volta anda. | na folha, em laranja: "arcada" · "implantes" · "osseointegração" · "parafusada" | "cada linha que ela escreveu virou uma cena." **(8)** · 26,30–29,90 | Um traço suave no papel por palavra, alternando 2 tomadas. As cordas sobem. |
| 7 | 29,5–33,3 | A folha se descola da bancada e **sai da maquete** ao subir (escala de 1 para 1,06; sombra de 8 para 40 px; 29,5–30,0), enquanto a bancada em miniatura fica para baixo, mais desfocada, e desce até #2B2224 (nunca abaixo). Dobra 1: a lateral esquerda (10% da largura) dobra para trás. Dobra 2: a lateral direita dobra para trás; a folha fica 9:16 e o fio vira a borda, a moldura. Dobra 3: o cartão gira 180° e, no verso, está o estúdio, ainda a meia-luz (nunca abaixo de #2B2224). **Aos 32,5 s, IMPACTO**: a luz do estúdio acende e o brinquedo vira o real (papel e madeira → vidro, titânio e porcelana). O cartão cresce até virar a tela inteira. | **DOBRAR** (a assinatura da série), cada tempo começando numa batida: dobra 1 q900–q921 (30,00–30,70); dobra 2 q925–q946 (30,83–31,53); 4 quadros parados entre um tempo e outro; giro q950–q975 (31,67–32,50, `power3.in`); crescimento q975–q999 (32,5–33,3), com o raio dos cantos indo de 48 para 0 (o objeto vira o mundo). | — | silêncio (a voz termina em 29,9) | Três sons de dobra de papel, arquivos fixos da série, no meio de cada tempo: q911 (30,37) · q936 (31,20) · q963 (32,10). Riser (som que sobe até o golpe) de ~1,53 s (30,95–32,48), com 20 ms de respiro. **IMPACTO em q975**: o golpe da trilha + grave, prato abafado e eco de sala. |
| 8 | 32,5–46,5 | **O VÍDEO DA DRA. HELENA**, trecho de 14 s (seção 6.4). | 4 mecanismos internos: MERGULHAR · VARRER · CORTAR E CRESCER · ENCAIXAR (plano A) ou REVELAR POR LUZ (plano B) | frases do vídeo dela, mais a assinatura e o selo fixos | silêncio | Trilha no auge (volume 0,45) e sustentada. Sons de material: atrito seco de vidro fosco, chiado fino de corte, textura granular; "toc" de porcelana só no plano A. Nenhum outro impacto. |
| 9 | 46,5–50,5 | O vídeo dela, de novo como cartão (moldura do fio, cantos de 48 px), encolhe e pousa como o 1º retângulo vertical da grade do perfil, na tela de um celular num suporte simples sobre o balcão da recepção (de frente, nenhuma mão). O mundo aparece em volta enquanto ele encolhe: a maquete da recepção em luz dourada de fim de tarde, listras de persiana na parede em miniatura, a Helena-boneca de costas, da cintura para cima, desfocada à esquerda. | **LEVAR JUNTO**: escala de 1 para 0,15 em 1,2 s (46,5–47,7, `power2.inOut`), com borrão de até 6 px no meio do movimento; dentro do celular os cantos passam a 22 px. | interface (48,33–50,5): "último post · agora" (sem relógio) | "o perfil voltou a andar." **(5)** · 47,30–49,60 | Sopro de levar junto (sopro 2 de 2). A trilha desce para piano e cordas, a 0,20. Ambiente de recepção ao fim de tarde a −32 dB. |
| 10 | 50,5–56,3 | Mesmo enquadramento. A tela troca para a conversa do grupo; o vídeo dela sobe como um balão "encaminhado"; chega uma resposta só. | **CHEGAR**: o balão "encaminhado" sobe e assenta (51,67, `expo.out`); a resposta entra com troca por desfoque (de 8 para 0 px em 0,15 s) em 53,33 e fica parada até 56,3 (3,0 s). | interface: "turma da especialização" · "encaminhado" (51,67) · "Lúcia: ficou com a sua cara" (53,33) | "ela mandou o vídeo pra turma." **(6)** · 50,90–53,60 | "encaminhado" (toque seco) em 51,67; chegada de mensagem (toque seco em vidro) em 53,33. |
| 11 | 56,3–64,17 | Corte seco para o mesmo enquadramento do fim da cena 2 (a maquete inteira sobre a mesa), agora de tarde (placa C1-tarde): abajur apagado, listras douradas da persiana na parede, bancada vazia, tripé fechado e encostado na parede. De 57,1 a 58,1 s **a Helena-boneca, de corpo inteiro, atravessa a maquete andando**, da esquerda para a direita, passando pelas listras de sol, e sai pela borda direita. Depois pousa "faltava a forma". Em seguida, a dedicatória. | **CORTE CASADO + ELA SAI ANDANDO**: 3 poses-chave de corpo inteiro (passo aberto, pernas cruzando, passo aberto do outro lado), cada uma parada 4 quadros num ponto novo, como animação de maquete quadro a quadro, com borrão leve na troca; nunca uma pose deslizando. A sombra dela na parede acompanha as mesmas poses, desfocada, e só escurece onde há listra de luz (máscara tirada do brilho da C1-tarde). Plano B, se parecer recorte na prévia: um corte na ação entre 2 poses (ainda no meio da sala; já na borda) e a saída termina no som. A frase entra em **POUSO SECO** (aparece inteira e assenta em 2 quadros). | "faltava a **forma**" (59,17–61,4; Helvetica Regular 96 px #F6F4F1, "forma" em Bold #F34500, centro óptico y≈760) · dedicatória (61,67–64,17, inteira de uma vez, legenda de 60 px): "pra quem ainda grava **14 vezes**" | "o roteiro ela já tinha." **(5)** · 56,60–58,90. Depois, a tela fecha o pensamento em silêncio. | Rua distante a −36 dB; passos baixos dela, um por pose (57,1–58,1); porta fechando em 58,4; acorde de resolução perto de 59,2 (aproximado, conforme a trilha; é uma resolução, não um impacto). |
| 12 | 64,17–69,2 | A imagem escurece até o chumbo #303236 (64,17–64,57). Cartão da série: o ícone do sabiá branco (56 px), "sala de espera · ep. 01", o próximo episódio e o aviso. Tudo fica parado até o fim. | **REVELAR POR MÁSCARA**: o cartão aparece inteiro de uma vez, com uma máscara que corre de cima para baixo em 0,6 s (65,0–65,6, `power2.inOut`), na batida; nada se mexe depois. | "sala de espera · **ep. 01**" · "próximo: a pergunta que chega 40 vezes" · "personagens fictícias · feito com apoio de IA" (19 palavras) | "no próximo episódio: o que a recepção mais ouve." **(9)** · 64,50–68,50 | Motivo do tema no piano, 2 notas, perto de 65 s (aproximado). A trilha some de 67,7 a 69,2. |

**Transições usadas**, 5 famílias, todas com causa na tela:
1. movimento contínuo de câmera (1→2 contínuo; 2→3 com a troca de placa escondida no borrão de movimento);
2. corte pela luz (3→4: a luz do celular invade a folha; 5→6: a tela apaga e ela apaga o abajur) e escurecer (11→12);
3. troca na mesma tela (4→5, 9→10);
4. o objeto que vira o mundo e o levar junto (7→8, 8→9);
5. um único corte seco casado (10→11).

**Arquivos de cena** (em `compositions\`): s01-take14 · s02-recuo · s03-folha · s04-perfil · s05a-enviado (20,6–25,3) · s05b-abajur (25,3–26,1) · s06-fio · s07-dobra · s08-video-dela · s09-levar-junto · s10-turma · s11-tarde · s12-cartao. O cartão do vídeo dela é **um elemento só**, de 29,5 a 47,7 s, que leva dentro a sub-composição do vídeo dela: a dobra (s07), a tela cheia (s08) e o encolhimento (s09) animam esse mesmo elemento. A sub-composição é montada a partir de 31,67 s (quando o verso do cartão aparece no giro), com 0,83 s de pré-rolagem (estúdio a meia-luz, nunca abaixo de #2B2224; peça parada); o tempo 0 do vídeo dela é o impacto. Em camadas de imagem (v2), é uma cena 2.5D como as outras; se o Three.js entrar no completo, ela passa a ser a única cena WebGL viva, de 31,67 a 47,7 s.

## 5. Teste do mudo (o que se lê, na ordem, sem som)

"● take 14 · 23:47" → "apagar vídeo? · apagar" → "take 15" → "na cadeira, ela explica de cor" → "roteiro · protocolo sobre implantes", com "gravar 23/10", "30/10" e "06/11" riscadas → "último post · há 47 dias" → a foto da folha + "enviado · 23:52" → "sem gravar de novo" → o abajur apaga e a folha continua visível → o fio pinta 4 palavras da folha → a folha vira tela → "o que é uma prótese protocolo?" … "presa sobre implantes" … "o osso se une ao implante" … "a prótese é parafusada nos implantes" + "dra. Helena Prado · cirurgiã-dentista · CRO-UF 00000" → "último post · agora" → "ficou com a sua cara" → "faltava a forma" → "pra quem ainda grava 14 vezes" → cartão. A história inteira se entende sem áudio.

---

## 6. O "vídeo da dra. Helena", passo a passo

É um projeto HyperFrames próprio, realista (a "parte real" da v2), sem gente e sem narração: os títulos dela carregam a explicação, sobre música e sons de material. **Técnica (v2):** no corte de 10 s, imagens geradas em camadas e alinhadas (seção 9.3); no completo, as mesmas camadas, com Three.js + modelos do Sketchfab como evolução se o teste mostrar que vale a pena. Os passos abaixo valem para as duas técnicas; com camadas, cada ângulo de câmera (45° e 70°) é um conjunto próprio de imagens alinhadas, e a subida de câmera vira uma troca escondida no borrão de movimento. Sai em duas versões, que batem com a folha dela linha por linha:
- **trecho de 14 s**, dentro do episódio: as linhas 1, 3, 4 e 5 da folha;
- **completo, de cerca de 43 s**, como post próprio 2 dias depois: todas as linhas, na ordem clínica.

### 6.1 A folha dela (o que está impresso; em negrito, as palavras que o fio pinta)
```
roteiro · protocolo sobre implantes
1. o que é: prótese fixa da **arcada** inteira
2. antes: exame clínico e tomografia
3. **implantes** no osso: em geral, de 4 a 6
4. **osseointegração**: leva meses, varia
5. prótese **parafusada**: só a dentista remove
fechar: leve sua dúvida para a consulta
```
(Na folha, as palavras pintadas começam em Regular chumbo, na mesma caixa da versão Bold; o fio as troca para Bold #F34500.)

### 6.2 Fixos do primeiro ao último quadro
- **No episódio e no trecho:** "dra. Helena Prado · cirurgiã-dentista · CRO-UF 00000" (30 px, 80%, x=108, y=1180) e o selo "ilustração educativa · apoio de IA" (28 px, 70%, y=1290). São 11 palavras fixas.
- **No post completo:** a mesma assinatura e, no lugar do selo, uma linha só que também avisa que é ficção: **"exemplo fictício · apoio de IA"** (28 px, 70%, y=1290). Também 11 palavras fixas. Nada no topo.
- **Na prova interna (corte de 10 s):** o aviso "rascunho · frases em revisão" no topo (y=200, 28 px, 70%). Esse render nunca sai de `renders\`.

### 6.3 Enquadramento e luz do 3D
- O conjunto mandíbula + prótese vai de **y=480 a y=1240** (40% da altura), com a mandíbula a ~100% da largura e as pontas dos ramos saindo pela borda. A assinatura (y=1180) e o selo (y=1290) ficam sobre a sombra de contato, com a sombra local suave da legenda.
- Fundo: degradê vertical #44464B → #2A2C30, grão de 1% só no fundo, sem centro claro, sem vinheta.
- Luz: principal quente #FFE4CC de cima à esquerda; contraluz laranja #F34500 de trás à direita; 2 a 3 faixas de luz no ambiente; sombra de contato a 0,55. **O ambiente gira 4° por segundo em volta da peça parada**; a peça nunca gira.
- Câmera ~50 mm; elevação de 45° no começo, 70° depois da subida; nunca mais de 25° num movimento.
- Antes de animar: conferir no snapshot que a prótese que paira (140 px acima) não cobre os implantes quando a câmera sobe para 70°; se cobrir, ela fica mais alta desde o passo 1.

### 6.4 Trecho no episódio (32,5–46,5 s)

| Episódio (s) | Vídeo (s) | Passo (linha) | O que se vê | Mecanismo | Texto (entra inteiro) | Som |
|---|---|---|---|---|---|---|
| 32,5–35,6 | 0,0–3,1 | a dúvida (1) | O cartão termina de crescer (0,0–0,8). Mandíbula de vidro fosco menta, sem dentes, vista de 3/4 por cima (45°). O osso ainda fosco esconde os implantes. A prótese (12 coroas de porcelana sobre base de resina rosada fosca) paira 140 px acima, separada, como numa vista explodida. A contraluz laranja recorta a borda direita das peças. | **MERGULHAR**: a câmera avança 6% até 3,1 (`power1.inOut`); o ambiente gira 4°/s, então a peça fica parada e as faixas de luz andam por ela. | "o que é uma prótese **protocolo**?" (pousa em 0,8 = 33,3; parado 2,3 s) | trilha no auge |
| 35,6–39,5 | 3,1–7,0 | onde se apoia (3) | A câmera sobe 25° (de 45° para 70°) e enquadra a parte da frente do osso; a prótese que paira fica acima do quadro. Uma faixa única de vidro limpo atravessa o osso da esquerda para a direita e revela os 5 implantes de titânio juntos, paralelos, **já no lugar**. Nada se mexe depois. | **VARRER**: subida da câmera 3,1–4,5 (`power2.inOut`); faixa 4,5–5,5 (`power2.inOut`); resultado parado 5,5–7,0 (1,5 s). | "presa sobre **implantes**" + "em geral, de 4 a 6" (44 px) — 20 palavras na tela com as fixas | atrito seco de vidro fosco de 1,0 s (4,5–5,5), 6 dB abaixo da trilha |
| 39,5–43,2 | 7,0–10,7 | a cicatrização (4) | Um plano de corte desce pelo implante do meio enquanto a câmera se aproxima dele, num movimento só. A face cortada fica sólida, chumbo, com a trama de osso esponjoso em menta; o implante ocupa 45% da altura. O menta sobe e preenche os vãos da rosca, de baixo para cima. | **CORTAR E CRESCER**: corte + aproximação 7,0–8,0 (`power2.inOut`); crescimento 8,0–9,2; rótulo em 9,2; resultado parado 9,2–10,7 (1,5 s). | "o osso se une ao implante" · rótulo "osseointegração" (9,2), com linha-guia laranja e o ponto lima | chiado fino de corte (como vidro riscado) em 7,0; textura granular baixa durante o crescimento |
| 43,2–46,5 | 10,7–14,0 | a prótese no lugar (5) | O corte se fecha e a câmera recua até a arcada inteira, sem sair dos 70°. **Plano A** (só se o advogado ou o CRO liberar): a prótese desce e assenta sobre os 5 implantes, comprime 0,5% e assenta como uma mola amortecida. **Plano B** (vai ao ar enquanto não houver resposta): a prótese já está assentada, na sombra, e uma faixa de luz a revela da esquerda para a direita. | **ENCAIXAR** (A) ou **REVELAR POR LUZ** (B): recuo 10,7–11,7; A: descida 11,7–12,5; B: faixa 11,5–12,5; parado até 14,0 (1,5 s), e o resultado continua visível enquanto o cartão encolhe na cena 9. | "a prótese é **parafusada** nos implantes" (10,7) | A: "toc" de porcelana em titânio em 12,5, só 3 dB acima da trilha (não é impacto). B: sem "toc". |

Palavras na tela no trecho (com as 11 fixas): 17 · 20 · 18 · 17. Na prova interna, +4 do aviso "rascunho · frases em revisão".

### 6.5 Versão completa (post próprio, 43 s)

Ordem clínica: avaliação e tomografia → implantes → em alguns casos, provisória → osseointegração (alguns meses, varia) → prótese definitiva → cuidados. Cada texto entra inteiro e fica pelo menos 0,5 s + 0,3 s por palavra. Em tela cheia, sem moldura.

| Vídeo (s) | Passo | O que se vê | Mecanismo | Texto na tela (entra inteiro) | Palavras na tela (com as 11 fixas) |
|---|---|---|---|---|---|
| 0,0–5,0 | a dúvida | igual ao trecho; o título já está pousado no quadro 0 (a capa do post) | MERGULHAR | "o que é uma prótese **protocolo**?" (0,0–2,4) → "uma prótese fixa para a arcada inteira" (2,4–5,0) | 17 → 18 |
| 5,0–10,0 | antes de tudo | A mandíbula se separa em 7 fatias horizontais finas, como os cortes de uma tomografia, que se abrem no eixo vertical (5,4–6,6), ficam paradas (6,6–8,1) e voltam a fechar (8,1–9,1). | FATIAR | "antes: exame clínico e **tomografia**" | 16 |
| 10,0–16,5 | onde se apoia | igual ao trecho: a câmera sobe 25° (10,0–11,4) e a faixa de vidro limpo revela os 5 implantes já no lugar (11,4–12,4) | VARRER | "presa sobre **implantes**" · "em geral, de 4 a 6" (10,0–13,5) → "o implante faz o papel da raiz" (13,5–16,5) | 20 → 18 |
| 16,5–20,0 | em alguns casos | Logo depois dos implantes, uma prótese provisória translúcida (contorno branco a 40%) aparece sobre eles (16,7–17,5) e continua na tela, em contorno, durante o passo seguinte. | SOBREPOR | "em alguns casos, uma provisória vem antes" | 18 |
| 20,0–26,0 | a cicatrização | igual ao trecho (corte + aproximação 20,0–21,0; crescimento 21,0–22,2; rótulo em 22,2); a provisória em contorno sai do quadro com a aproximação | CORTAR E CRESCER | "o osso se une ao implante" (20,0–22,8) → no lugar do título, o rodapé "leva alguns meses · varia em cada caso" (22,8–26,0) · rótulo "osseointegração" | 18 → 19 |
| 26,0–31,0 | a prótese no lugar | A câmera recua (26,0–27,0) e a provisória se dissolve (26,6–27,0). A: a definitiva desce e assenta (27,2–28,0). B: já assentada, revelada por uma faixa de luz (27,0–28,0). | ENCAIXAR (A) ou REVELAR POR LUZ (B) | "a prótese é **parafusada** nos implantes" (26,0–28,6) → "**fixa**: não se tira em casa" (28,6–31,0) | 17 → 17 |
| 31,0–36,0 | cuidados | Uma linha branca fina desenha o caminho do fio dental por baixo da prótese, de um implante ao outro (33,5–34,5, junto com "fio específicos"), e fica parada até 36,0. Nenhuma boca, nenhuma mão. | DESENHAR O CAMINHO | "só a dentista remove, nas revisões" (31,0–33,5) → "em casa: escova e fio específicos" (33,5–36,0) | 17 → 17 |
| 36,0–43,0 | fechamento | O ambiente gira 4°/s em volta da peça parada. A cartela entra em blocos inteiros. | CARTELA EM BLOCOS | 36,3: "leve sua dúvida para a consulta". 38,6: a assinatura fixa sobe e vira o fim da cartela: "dra. Helena Prado" (Bold 56 px) / "cirurgiã-dentista · implantodontista" / "CRO-UF 00000" (Regular 36 px), com o bloco terminando em y=1180. A linha "exemplo fictício · apoio de IA" continua em y=1290. Tudo parado até 43,0. | 18 |

Sons do completo: o tema cortado em 43 s; atrito de vidro na varredura; um deslizar baixo de vidro nas fatias; chiado de corte; textura granular; "toc" só no plano A; um traço fino de vidro na linha do fio dental.

### 6.6 Por que cumpre o CFO
- **Nenhum procedimento acontecendo** (Res. 196/2019, art. 3, que proíbe imagens "relativas ao transcurso e/ou à realização dos procedimentos"): os implantes aparecem já posicionados, sem broca, incisão, mão, instrumento, tecido, sangue ou paciente.
- **A prótese descendo e assentando (plano A)** mostra a instalação da prótese, que também é etapa do tratamento. É a mesma zona cinzenta do implante descendo e vai como pergunta nominal ao advogado ou ao CRO. Enquanto não houver resposta, vai o plano B: a vista explodida não fecha; a prótese já aparece assentada e é revelada por uma faixa de luz, sem o "toc".
- **Sem marca, preço, antes e depois ou promessa.** Os cuidados de linguagem: "em geral", "alguns meses", "varia em cada caso", "em alguns casos".
- **5 implantes paralelos.** Nunca 4 com os de trás inclinados, e nunca "All-on-4".
- **Nome, "cirurgiã-dentista" e CRO** (fictício e evidente) visíveis desde o primeiro quadro (art. 4; Código de Ética, art. 43). O selo de IA também.
- **Abre com a dúvida do paciente e fecha de forma educativa** ("leve sua dúvida para a consulta"; art. 44, V).
- **Publicado no perfil pessoal dela**, não num perfil de clínica (que exigiria a inscrição da clínica e a responsável técnica).

### 6.7 O que a implantodontista revisora confere (e assina em `revisao-tecnica.md`)
1. "prótese fixa para a arcada inteira" como definição de protocolo.
2. Exame clínico e tomografia antes do tratamento.
3. "em geral, de 4 a 6"; 5 implantes paralelos na parte da frente da mandíbula como representação aceitável; "o implante faz o papel da raiz".
4. "leva alguns meses · varia em cada caso".
5. Se o passo da provisória fica, se a ordem (implantes → provisória, em alguns casos → osseointegração → definitiva) está certa, e o texto "em alguns casos, uma provisória vem antes".
6. "parafusada", "fixa: não se tira em casa", "só a dentista remove, nas revisões", "escova e fio específicos".
7. A base de resina rosada e a barra como representação esquemática, e 12 dentes até o 1º molar como representação aceitável.

A revisão trava só a versão que vai ao ar. A prova interna de estilo (corte de 10 s) usa as frases como estão, com o aviso "rascunho · frases em revisão", e não sai de `renders\`.

### 6.8 Perguntas ao advogado de saúde ou ao CRO (antes de publicar)
1. A ilustração esquemática 3D (implantes já no lugar, corte transversal do osso) conta como "transcurso ou realização de procedimento"?
2. A prótese descendo e assentando (plano A) conta? Se sim, ou sem resposta, vai o plano B.
3. O perfil pessoal da profissional, com o nome do perfil fora do quadro, dispensa a inscrição da clínica e o responsável técnico na cartela?
4. "implantodontista" na cartela de uma personagem fictícia, com CRO evidentemente falso, tem algum problema?

---

## 7. Narração

**Total: 75 palavras** (8 + 12 + 12 + 10 + 8 + 5 + 6 + 5 + 9), cerca de 34 s de fala a ~2,2 palavras por segundo em 69,2 s. Nenhuma cena passa de 12 palavras.

Texto para a ElevenLabs:
- voz **A.Medeiros** (voice_id `E9hPCbqBRCgB3UEiCUuE`), modelo eleven_v4;
- estabilidade ~55%, similaridade ~75%, estilo de 0 a 10%, velocidade 1,0;
- uma linha em branco entre as falas cria a pausa onde se corta;
- números por extenso.

```
décima quarta tentativa.

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

no próximo episódio: o que a recepção mais ouve.
```

Fala alternativa, gerada na mesma sessão e usada só no teste de gancho (Trial Reels):
```
quase meia-noite. e o vídeo ainda não saiu.
```

- **Custo:** cerca de 430 caracteres por tomada da narração inteira, mais ~45 pela fala alternativa (≈ 470 no total por rodada). A 1 crédito por caractere, são ~470 créditos por rodada; conferir no painel quantos créditos por caractere o eleven_v4 cobra antes de gerar. De 2 a 4 rodadas.
- A voz é o relógio do vídeo: depois de escolhida a tomada, todos os tempos da tabela se ajustam às falas reais (`narracao.json`). O recorte é sempre feito nas pausas, nunca esticando, acelerando ou emendando a voz.

## 8. Trilha e efeitos

### 8.1 Pedido para o ElevenLabs Music
eleven_music_v2_5, instrumental, 3 candidatas:
```
Instrumental, 75 seconds, 72 BPM, steady tempo, calm cinematic. Starts almost silent with one low felt-piano note
every two beats. A second piano voice joins around 0:08, soft low strings around 0:14, a gentle low pulse around 0:20.
Continuous slow crescendo, no drums, no heavy kick. A short riser of about 1.5 s into ONE single cinematic impact
(deep low hit + muffled cymbal + room reverb) around 0:28. After the impact, a sustained driving section of about
14 s (pulse and strings at full level, no second hit), then it relaxes into warm piano and strings and resolves on
a warm major chord around 0:55, followed by a soft two-note piano motif around 1:01 and a slow fade.
```
Se o conector aceitar plano de composição (seções com duração), usar, no tempo da música: 0–28,5 (crescendo, termina no golpe) / 28,5–42,5 (sustentada) / 42,5–55,2 (relaxa até o acorde) / 55,2–75,0 (resolução, motivo de 2 notas e fade).

### 8.2 `montar-trilha.py` (um só nome de script)
- Mede o golpe da candidata escolhida: `npx hyperframes audio <trilha> --only sections,onsets,moments --json`.
- Alinha a música **só pelo golpe**: põe o golpe no quadro 975 (32,5 s). A primeira nota cai onde cair, entre 3,5 e 5,0 s, com entrada suave de 1,0 s. Se o golpe da candidata estiver fora de 27,5–29,0 s de música, a candidata é descartada (ou, se o começo dela for silêncio, corta-se só o silêncio).
- A trilha **nunca é cortada nem esticada** entre a entrada e o golpe.
- Os tempos internos (2ª voz do piano, cordas, pulso, acorde final, motivo de 2 notas) são aproximados: vale o que a música trouxer, medido com o mesmo comando.
- Plano B, só se o acorde cair a mais de 0,5 s do pouso de "faltava a forma" (59,17): montar a trilha em 2 pedaços (até o fim da seção sustentada, alinhado pelo golpe; da resolução em diante, alinhado para o acorde cair em 59,17), emendados por um cruzamento de 1 compasso (3,33 s) entre 50,5 e 53,8 s, onde a trilha está a 0,20.
- Volumes: entrada 0,10; ~0,14 sob a voz, com recorte de frequências para abrir espaço para ela; 0,45 no vídeo dela; 0,20 depois; fade de 67,7 a 69,2.

### 8.3 Efeitos (eleven_text_to_sound_v2, 2 a 3 tomadas de cada; biblioteca da série)
- **Ambientes:** consultório à noite; recepção ao fim de tarde; rua distante.
- **Interface (toques secos de dedo em vidro, sem nota musical):** toque, "enviado", "encaminhado", chegada de mensagem. Tique de contador seco e mecânico.
- **Papel e mesa:** folha farfalhando, risco de caneta, traço no papel, **dobra de papel 1, 2 e 3** (arquivos fixos da série, nunca mudam).
- **Ar:** sopro grave e sopro de levar junto (no máximo 2 por episódio).
- **Luz:** obturador, interruptor de abajur.
- **3D:** impacto (grave + prato abafado + eco), atrito seco de vidro fosco (varredura), chiado de corte, crescimento granular, "toc" de porcelana em titânio (só plano A).
- **Gente fora do quadro:** passos, porta fechando.
- Sem "tink de titânio", sem tela de bloqueio, sem estalo de sensor de luz.
- Se o ElevenLabs não acertar um som, e só com o ok do dono: Pixabay (já vem no fluxo do HyperFrames) ou Openverse (CC0 ou CC BY, com crédito na legenda).
- O custo em créditos da música e dos efeitos é conferido no painel antes de gerar.

---

## 9. Corte de 10 s (etapa 2)

O dono pediu UM corte de 10 s. É sempre um trecho contínuo do piloto, no ritmo real, sem montagem comprimida.

### 9.1 Recomendado: a virada, 25,3 a 35,3 s (q759–q1059)
É o trecho que prova o estilo pedido no briefing e na v2 (a maquete lúdica, o fio, a dobra, o único impacto e o salto para a parte realista "titânio e porcelana") e, na v2, também mostra a Helena-boneca no 1º segundo, de costas, apagando o abajur da maquete. Antes dele, o dono recebe **uma imagem parada do quadro 0** (a capa v2: o celular com ela no visor e atrás do tripé), para julgar a personagem, e **3 quadros parados de luz** (a maquete à noite, o estúdio e a maquete à tarde), para confirmar a luz; o corte só é animado depois desse ok (crítica gost-6). A noite (`v2-capa-B.png`) e o estúdio (`estudio-video-dela.png`) já existem como rascunho, em `referencias-visuais\v2-painel-capas.png`.

| Segundo do corte | Episódio (s) | O que aparece | Som |
|---|---|---|---|
| 0–1 | 25,3–26,3 | A folha na bancada da maquete, ainda sob o abajur (a tela do celular acabou de apagar), e **a Helena-boneca de costas**, vista de cima e desfocada na borda esquerda de baixo, com o braço esquerdo esticado até o abajur. Clique do interruptor (25,5): a luz desce para o azulado da rua (25,5–25,9), e a folha continua visível. Ela recolhe o braço e sai (25,9–26,1); a câmera fecha na folha (até 26,2). O ponto laranja acende no canto da folha (26,2). | interruptor; ambiente à noite; voz "cada linha…" (26,3) |
| 1–3 | 26,3–28,3 | O fio contorna a folha (até 27,0) e desce lendo: "arcada" (27,0), "implantes" (27,4), "osseointegração" (27,8) e "parafusada" (28,2) ficam laranja. | traço no papel por palavra; cordas sobem |
| 3–4 | 28,3–29,3 | "parafusada" termina de pintar e as 4 palavras ficam paradas (a partir de 28,6). | voz "…virou uma cena." |
| 4–6 | 29,3–31,3 | A folha se descola e sai da maquete ao subir (29,5); dobra 1 (30,0) e dobra 2 (30,83), cada uma na batida; o fio vira a moldura. | voz termina (29,9); papel 1 (30,37) e papel 2 (31,20); o riser começa (30,95) |
| 6–7 | 31,3–32,3 | O cartão gira (31,67–32,5), com o estúdio a meia-luz no verso. | papel 3 (32,10) |
| 7–8 | 32,3–33,3 | **IMPACTO (32,5)**: o brinquedo vira o real; a luz do estúdio acende e o cartão cresce até a tela inteira (até 33,3). | **impacto** |
| 8–10 | 33,3–35,3 | A parte realista, **por camadas de imagem**: mandíbula de vidro fosco menta (camada "osso fosco") e a prótese pairando acima (camada própria, sem fundo, com a sombra de contato à parte), sobre o fundo do estúdio. O título "o que é uma prótese protocolo?" pousa (33,3) e fica parado; a câmera avança devagar (MERGULHAR: as camadas crescem 6%, a prótese um pouco mais que o osso, para dar profundidade); **uma luz que varre** (uma faixa clara e suave, em código, recortada pela forma das peças) anda pela peça parada, no lugar do ambiente que gira. Assinatura, selo e o aviso "rascunho · frases em revisão". | trilha no auge |

**Como é montado:** no próprio projeto do episódio. Na fase do corte, a raiz (`index.html`) monta só as cenas s05b a s08, com o tempo deslocado em −25,3 s, e duração de 10 s; a s05b já traz a camada da Helena de costas (2 poses), e a s08 é a sub-composição do vídeo dela em camadas (não usa WebGL no corte). Depois da aprovação 2, a raiz passa a ser o episódio inteiro (a versão do corte fica guardada como `corte-10s.html`). O render do corte vai para `renders\` e não sai de lá.

**Teste da varredura (3 s, junto com o corte, fora dos 10 s):** a camada "osso limpo com implantes" é gerada alinhada à "osso fosco" (≤ 8 px na sobreposição a 50%), e a **varredura de vidro** vira uma troca entre as duas por uma máscara em faixa que anda da esquerda para a direita (o passo 2 do vídeo dela, 35,6–39,5 no episódio). Ela é renderizada à parte, em `renders\`, para o dono ver que o método segura o resto do vídeo dela sem modelos 3D.

**Antes do render:** `npx hyperframes check --json` → `npx hyperframes snapshot --at 0,0.3,0.9,2.9,4.7,5.5,6.6,7.2,8.0,9.9` (tempo do corte) → `npx hyperframes preview` e esperar o ok → render de rascunho (`--quality draft`), cerca de 1 min.

### 9.2 Alternativa (pergunta ao dono): o gancho, 0,0 a 10,0 s
Testa a Helena-boneca abrindo os olhos e a revelação da maquete, mas não prova a parte realista, o fio nem a dobra.

| Segundo | O que aparece | Som |
|---|---|---|
| 0–1 | quadro 0 (a capa); os olhos abrem (0,4–0,7); "apagar vídeo?" sobe (0,8–1,2) | voz "décima quarta tentativa." (0,10); ambiente à noite |
| 1–2 | o painel fica parado e legível | — |
| 2–3 | toque em "apagar" (2,23); a prévia volta (2,5) | toque seco; voz "e o vídeo não sai." (2,00) |
| 3–4 | o contador rola de 14 para 15 (3,0–3,3) e para | tique em 3,10 |
| 4–6 | a câmera recua e revela a maquete sobre a mesa, com ela de corpo inteiro ao lado do tripé | a trilha entra; sopro grave; voz "a doutora Helena…" (4,40) |
| 6–7 | o recuo pousa (6,6); legenda "na cadeira, ela explica de cor" (6,67) | voz segue |
| 7–9 | legenda parada; o foco corre do celular para a folha (8,0–9,2) | — |
| 9–10 | a folha nítida sob o abajur; fim em 10,0 | voz termina (9,9) |

O gancho precisa, além da capa, das pálpebras a meio e abertas do visor (nº 12): cerca de US$ 0,15 a mais em imagens, e dispensa a C2 (nº 7), a pose de costas (nº 8) e as camadas do vídeo dela (nº 11).

### 9.3 O que será produzido para o corte recomendado

**Imagens OpenAI** (`node C:\social-media\ferramentas\openai\gerar-imagem.mjs`). Os finais saem em gpt-image-2.6-sunburst, sempre como edição do rascunho escolhido (`--ref`); os rascunhos em gpt-image-2.5-flare, low, a ~US$ 0,005. A chave já está cadastrada e testada (11/11/2026, 18:15; o primeiro rascunho custou US$ 0,0049). Os pedidos seguem os modelos da BIBLIA (seção 6: folha, expressões, bloco fixo de pose, placa da maquete). **Nenhuma placa tem a personagem dentro**; ela entra sempre como camada sem fundo, gerada com `--ref` da placa onde vai ficar.

| # | Imagem | Uso no corte | Tamanho / fundo | Qualidade | Finais | Custo |
|---|---|---|---|---|---|---|
| 1 | **folha final B** (série toda): edição do rascunho já escolhido, `rascunhos\v2-folha-B-designer-toy-1.png`, 4 vistas, só sobe acabamento e resolução | todas as poses | 2560x1440, opaco | xhigh | 2 | ≈ US$ 0,22 |
| 2 | **folha de expressões B** (série toda): 6 bustos, mudando só pálpebras e sobrancelhas, `--ref` da nº 1 | visor e poses | 2048x1152, opaco (#F3EFE8) | xhigh | 1 (+2 rascunhos) | ≈ US$ 0,10 |
| 3 | **visor**: a Helena-boneca do peito para cima, de frente, olhos fechados (expressão 2), luz do abajur à esquerda da imagem; sem espelho se a planta da cena 1 ficar com a câmera traseira (seção 2). O fundo do visor é um recorte desfocado da nº 6, sem imagem própria | capa | 1152x2048, sem fundo | xhigh | 2 | ≈ US$ 0,15 |
| 4 | **pose ao lado do tripé**: corpo inteiro, de frente em 3/4, olhando para o celular, cansada (expressão 1), `--ref` da nº 6. Vai desfocada atrás do tripé na capa e nítida no fim do recuo | capa (e cena 2) | 1440x2560, sem fundo | xhigh | 2 | ≈ US$ 0,20 |
| 5 | **close do tripé** (T1): o tripé da maquete aberto, em miniatura, com a garra segurando uma placa escura lisa, de frente | capa (e recuo) | 2160x3840, sem fundo (plano B: fundo liso #E6E3DF + recorte por cor) | high | 2 | ≈ US$ 0,20 |
| 6 | **consultório à noite, largo** (C1-noite): a maquete inteira sobre a mesa, sem tripé e sem pessoa, sombras abertas (pedido de cenário da BIBLIA) | quadro de luz da noite; capa (desfocada em volta) | 1440x2560, opaco | xhigh | 2 (+2 rascunhos) | ≈ US$ 0,21 |
| 7 | **bancada de cima** (C2-noite): a bancada da maquete vista quase de cima, com o abajur aceso no canto de cima à esquerda e a superfície vazia (a folha é HTML) | virada, 0–6 s | 1440x2560, opaco | xhigh | 2 (+2 rascunhos) | ≈ US$ 0,21 |
| 8 | **de costas apagando o abajur**: vista de cima, braço esquerdo esticado até o abajur (pose 1) e recolhido (pose 2), `--ref` da nº 7 (exemplo 1 da BIBLIA) | virada, 0–1 s | 1440x2560, sem fundo | xhigh | 2 poses | ≈ US$ 0,20 |
| 9 | papel em macro, sem texto (a folha é HTML) | virada | 2048x2048, opaco | high | 2 | ≈ US$ 0,21 |
| 10 | **consultório à tarde** (C1-tarde): edição da nº 6 com `--ref`, só muda a luz (BIBLIA, seção 4) | quadro de luz da tarde | 1440x2560, opaco | xhigh | 2 | ≈ US$ 0,20 |
| 11 | **camadas do vídeo dela**, todas como edição de `cenarios\rascunhos\estudio-video-dela.png`, no mesmo ângulo (45°) e enquadramento: (a) osso fosco, sem prótese, sobre o fundo do estúdio; (b) osso limpo com os 5 implantes, edição da (a) mudando só o vidro; (c) a prótese sozinha, sem fundo | virada, 8–10 s; teste da varredura | 1152x2048; (a) e (b) opacos, (c) sem fundo | xhigh | 1 de cada | ≈ US$ 0,25 |

- **Custo das imagens do corte:** cerca de US$ 2,15 de saída + ~US$ 0,40 de imagens de referência enviadas ≈ **US$ 2,50** (faixa de US$ 2 a 3 com refações; se for passar de US$ 3, eu aviso antes). Só a virada (nº 7, 8, 9 e 11) custa ≈ US$ 0,90; o resto é a folha, a capa e os quadros de luz.
- Os números reais ficam no `registro.csv`.
- **Sobre o tamanho do tripé:** a nº 5 sai em 2160x3840 (tamanho "experimental" da OpenAI) porque aparece ampliada no quadro 0. Plano B: gerar só a cabeça do tripé como recorte próprio, em 1440x2560.
- **As placas (nº 6, 7 e 10):** eu escolho o rascunho e mostro junto; a folha da personagem já foi escolhida pelo dono (B).
- **Conferências:** as camadas (a) e (b) da nº 11 e as placas nº 6 e 10 são sobrepostas a 50% e não podem se deslocar mais de 8 px; toda pose é posta sobre a placa dela para conferir luz, sombra de contato e escala (se parecer colada, a cena é gerada com ela dentro e a profundidade é separada depois).

**A parte realista (sem modelos 3D):**
- Montada no HyperFrames com as camadas da nº 11: o fundo do estúdio em código (degradê #44464B → #2A2C30 com grão de 1%), o osso fosco, a prótese como camada própria pairando acima (com a sombra de contato à parte) e **uma luz que varre** (faixa clara e suave em código, recortada pela forma das peças) no lugar do ambiente que gira.
- **Varredura de vidro** = troca entre o osso fosco (a) e o osso limpo (b), alinhados, por uma máscara em faixa que anda da esquerda para a direita. Ela não cai dentro dos 10 s; vai num **teste de 3 s** renderizado junto (seção 9.1), que também mede o tempo de render.
- O Three.js com os modelos do Sketchfab (seção 10.2) fica como evolução para o vídeo completo, se o teste mostrar que vale a pena.

**Voz:** a narração inteira já sai na versão final (2 a 4 rodadas). O corte usa a fala "cada linha que ela escreveu virou uma cena.".

**Som:** 3 candidatas de trilha; efeitos do corte: ambiente à noite, interruptor de abajur, traço no papel (2 tomadas), dobra 1, 2 e 3, impacto.

**Prazo:** 2 a 3 dias de trabalho depois do sim. Não depende de o dono baixar modelos (a folha B já está escolhida); depende só do ok nas imagens paradas. Ficam para depois da aprovação 2: o resto das poses, o resto da biblioteca de efeitos, os cortes do tema e o molde da série.

### 9.4 O que o dono julga
Antes do corte (imagens paradas):
1. **A capa (a Helena-boneca no visor e atrás do tripé):** lê como a mesma personagem da folha B, com cara de série animada de qualidade, e não de "boneco de IA" genérico?
2. **A luz dos 3 mundos** (os 3 quadros parados): a noite na maquete está clara o bastante, sem cara de "filme de terror"? A tarde é outra luz, e não a noite clareada?

No corte (aprovação 2):

3. **A parte realista:** vidro menta, titânio e porcelana parecem estúdio ou "bolha"? O salto do brinquedo para o real se sente no impacto? As camadas de imagem seguram o movimento, ou vale ir para o Three.js no completo?
4. **A dobra:** dá tempo de ver cada tempo? Ela cai na batida?
5. **A trilha** crescendo até o único impacto.

**Plano B da capa:** se o rosto no visor não passar, o visor fica desfocado, como se a câmera tivesse "perdido o foco". Vê-se a silhueta dela, o jaleco e a luz, sem detalhe de rosto; a Helena-boneca desfocada atrás do tripé continua, e a interface ("● take 14", "23:47", "apagar vídeo?") carrega a leitura.

---

## 10. Lista de produção do piloto

### 10.1 Imagens OpenAI
As de nº 1 a 11 do corte, mais (todas as poses sem fundo, de corpo inteiro sempre que o plano mostra o corpo, com `--ref` da folha, da folha de expressões e da placa onde vão ficar):

| # | Imagem | Cena | Tamanho / fundo | Qualidade | Finais | Custo |
|---|---|---|---|---|---|---|
| 12 | visor: pálpebras a meio e abertas (expressão 1), edição da nº 3, "mude só as pálpebras e as sobrancelhas" | 1–2 | 1152x2048, sem fundo | xhigh | 2 estados | ≈ US$ 0,15 |
| 13 | mão-boneca direita com a caneta, vista quase de cima: chegando + 3 poses do risco (começo, meio e fim da palavra), `--ref` da nº 7 | 3 | 1440x1440, sem fundo | xhigh | 4 poses | ≈ US$ 0,25 |
| 14 | mão-boneca chegando e tocando a tela (só se a cena 1 ficar com a câmera traseira; vai desfocada) | 1 | 1024x1536, sem fundo | high | 2 poses | ≈ US$ 0,08 |
| 15 | T2: o mesmo tripé em miniatura, fechado e encostado (edição da nº 5) | 11 | 1440x2560, sem fundo | xhigh | 2 | ≈ US$ 0,20 |
| 16 | suporte de mesa em miniatura com placa escura lisa, de frente | 9–10 | 1440x2560, sem fundo | high | 2 | ≈ US$ 0,11 |
| 17 | C3: **recepção à tarde**, a maquete da recepção com listras de persiana, sem pessoas e sem texto (final por edição do rascunho escolhido) | 9–10 | 1440x2560, opaco | xhigh | 3 | ≈ US$ 0,29 |
| 18 | de costas na recepção: da cintura para cima, luz de tarde vinda da esquerda, `--ref` da nº 17 | 9–10 | 1440x2560, sem fundo | xhigh | 2 | ≈ US$ 0,20 |
| 19 | andando: corpo inteiro, de perfil, indo para a direita, em 3 poses-chave (passo aberto, pernas cruzando, passo aberto do outro lado), luz de tarde, `--ref` da nº 10. A sombra na parede usa as mesmas poses, escurecidas e desfocadas | 11 | 1024x1536, sem fundo | xhigh | 3 poses | ≈ US$ 0,25 |

- **Total do piloto:** cerca de 42 imagens finais (contando poses e variações) e cerca de 10 rascunhos novos (os da folha já foram feitos em 12/11/2026).
- **Custo:** ≈ US$ 3,70 de saída + US$ 0,10 de rascunhos + US$ 0,70–1,00 de referências ≈ **US$ 5** (faixa de US$ 4 a 6 com refações).
- **Fora desta lista e deste custo:** as camadas do resto do vídeo dela (o conjunto a 70°, o corte do implante com o osso crescendo, a prótese assentada e, no completo, as fatias, a provisória e o caminho do fio dental). Elas são listadas e orçadas depois da aprovação 2, quando se decide entre camadas e Three.js (seção 6).
- **Do ep. 02 em diante:** caem a folha da personagem e as placas repetidas, e o custo fica em ≈ US$ 1 a 3 por episódio.
- A sombra da mão na cena 3, a luz fria da rua, a grade do perfil, as etiquetas e todas as interfaces são HTML ou código, sem imagem gerada. A máscara das listras de sol sai do brilho da própria C1-tarde (por isso não há uma camada de luz de persiana gerada à parte: ela não bateria com as listras da placa).

### 10.2 Modelos 3D (só para o vídeo completo, como evolução)
O corte de 10 s não usa modelos 3D (seção 9.3). Esta lista vale **só se** o teste das camadas mostrar que o Three.js vale a pena no vídeo completo (pergunta 7 do roteiro). Nesse caso, o dono baixa com o login dele e salva em `brutos\2026-11-12_serie-clinicas-modelos-3d\`; eu copio para dentro do projeto.

| Peça | Fonte | Licença | Uso |
|---|---|---|---|
| mandíbula sem dentes (1ª opção) | "Mandible", de Vikrama Raghuraman (descrita como mandíbula sem dentes, ~270 mil faces); procurar no Sketchfab pelo título e pelo autor | conferir CC BY 4.0 na página, e se é mesmo sem dentes, antes de baixar | osso de vidro menta |
| mandíbula (2ª opção) | "Model Jaw - implant", Ortomesh, ~116 mil faces — https://sketchfab.com/3d-models/model-jaw-implant-173fad1fdf784b5db66ed00010a3a59f | CC BY 4.0 (conferida pela API em 11/11/2026) | só se, aberta, trouxer o osso separado dos dentes e com o topo liso, sem alvéolos (os buracos das raízes). As etiquetas da página citam "teeth" e "nerves", então provavelmente vem com dentes |
| coroas da prótese | "Permanent Dentition", University of Dundee School of Dentistry, ~30 mil faces — https://sketchfab.com/3d-models/permanent-dentition-2f69d7b59c3e4a6a8bcae041bd8e591b | CC BY 4.0 | só as coroas de 12 dentes inferiores (do 1º molar esquerdo ao 1º molar direito), cortadas na junção com a raiz e afundadas 1,5 mm na base rosada; curva e escala da arcada ajustadas à mandíbula escolhida. Isso entra na imagem parada da prótese |
| conferência de proporção | "Implante Dental", drandrescordova — https://sketchfab.com/3d-models/implante-dental-ede1a07475db4236b43a6cd168d1225d | CC BY 4.0 | medidas do parafuso (não aparece na tela) |
| 5 implantes e a barra | código: perfil girado e rosca em hélice, como o parafuso que ficou bom no teste | nossa | genéricos, sem marca |
| base da prótese | código: um perfil arredondado percorrendo a curva da arcada | nossa | só depois da imagem parada aprovada |
| plano B do osso cortado | código: um bloco de osso em volta do implante do meio (cilindro com trama esponjosa menta) | nossa | se a mandíbula não for uma malha fechada |

- **Preparo:**
  - reduzir e limpar com `npx @gltf-transform/cli weld` e `npx @gltf-transform/cli simplify` (sem compressão Draco): tudo abaixo de 150 mil faces, a mandíbula em ~80 mil;
  - conferir com um script se a mandíbula é fechada (zero arestas abertas). Se não for, a tampa do corte falha, e entra o plano B do bloco de osso, com a câmera fechada nele.
- **Planos B da base:** primeiro, enquadrar mais fechado, com a base na sombra. Depois, comprar um modelo pronto (CGTrader, US$ 10 a 50), só com o ok do dono.
- **Proibido:** "UWF11 Edentulous Mandible" (licença NC, que não permite uso comercial) e modelos de fabricante (MSDI).
- **Créditos** em `modelos-3d\odonto\CREDITOS.md` (com o link de cada página) e na legenda do post: "modelos 3D adaptados (cor, corte e redução): 'Mandible', Vikrama Raghuraman; 'Permanent Dentition', University of Dundee School of Dentistry · Sketchfab · licença CC BY 4.0 (creativecommons.org/licenses/by/4.0)". Se a mandíbula da Ortomesh for a usada, trocar por "'Model Jaw - implant', Ortomesh".

### 10.3 Voz
A.Medeiros, eleven_v4. De 2 a 4 rodadas das 75 palavras, mais a fala alternativa (~470 caracteres por rodada; conferir créditos no painel). Nenhuma voz nova é necessária.

### 10.4 Trilha e efeitos
- **Tema da série:** 3 candidatas de 75 s; a escolhida vira o tema e é cortada em 43 s (vídeo dela completo), 45, 65 e 75 s.
- **Biblioteca de efeitos da série:** a lista da seção 8.3.

---

## 11. Passo a passo no HyperFrames

1. **Aprovação 1:** `ep01-ROTEIRO.md` e as perguntas.
2. **Revisão técnica:** a implantodontista revisa e assina as frases do vídeo dela (`revisao-tecnica.md`). A revisão trava só a versão que vai ao ar: a prova interna usa as frases como estão, com "rascunho · frases em revisão", e não sai de `renders\`.
3. **Nomes:** busca rápida na web feita em 11/11/2026, sem coincidência evidente. Antes da primeira imagem, conferência formal nos cadastros públicos (CFO para Helena e Rafael; CFM para Caio; COFFITO para Lia).
4. **Modelos (só se o Three.js for adiante, para o completo):** o dono baixa para `brutos\`; eu copio para `modelos-3d\odonto\originais\`, confiro (sem dentes? malha fechada?), reduzo e escrevo o `CREDITOS.md`.
5. **Personagem:** o rascunho B já foi escolhido (12/11/2026) → 2 finais da folha por edição do `v2-folha-B-designer-toy-1.png` → folha de expressões B. Essa é a aprovação da personagem.
6. **Placas e capa:** C1-noite, C2-noite e C1-tarde da maquete (rascunho escolhido → final por edição), visor, pose ao lado do tripé, T1 e papel (nº 3 a 7, 9 e 10) → pôr cada pose sobre a placa dela e conferir a luz → `npx hyperframes media-treatment` para grão e cor (nunca filtro CSS; escurecer pode, clarear não) → montar o quadro 0 parado e os quadros de luz da noite e da tarde (o do estúdio é a camada "osso fosco" com a prótese, passo 8) → mostrar ao dono e esperar o ok antes de animar o corte.
7. **Voz primeiro:** rodadas → escolha → `montar-narracao.py` → tempos das palavras (`npx hyperframes transcribe`) → `narracao.json`. A tabela se ajusta à voz, mantendo o impacto num quadro de batida.
8. **Parte realista em camadas:** as 3 camadas da nº 11 (osso fosco, osso limpo com implantes, prótese) → quadro parado do estúdio (é também o quadro de luz do estúdio; o dono aprova) + teste da varredura de 3 s (seção 9.1).
9. **Trilha:** 3 candidatas → `montar-trilha.py` (golpe no quadro 975).
10. **Corte de 10 s:** `check` → `snapshot` → `preview` → render de rascunho em `renders\`. **Aprovação 2.**
11. **Restante das imagens** (nº 12 a 19: pálpebras do visor, mão-boneca, poses de corpo inteiro, tripé fechado, suporte, recepção), com `media-treatment`; conferir as transparências e cada pose sobre a placa dela.
12. **Vídeo dela** (projeto próprio `clinicas-ep01-video-dra-helena\`): o completo de 43 s e o trecho de 14 s, em camadas de imagem (com Three.js como evolução, se a aprovação 2 pedir), copiado para o episódio como sub-composição (`data-composition-src="compositions/s08-video-dela.html"`). Plano B: render do trecho em MOV ou MP4 de alta qualidade, tocado num `<video>`.
13. **Montagem:** uma cena por arquivo em `compositions\` (lista na seção 4); `data-motion-blur="on"` na raiz (borrão de movimento).
14. **Som completo:** efeitos 1 quadro depois da imagem; música a ~0,14 sob a voz; `npx hyperframes audio --json` para conferir onde cada som bate.
15. **Revisão:** `check`, `snapshot --review`, `REVIEW.md` com a lista PROIBIDO e a folha da personagem ao lado de cada plano, e o teste do mudo com 3 pessoas. **Aprovação 3.** O advogado ou o CRO vê o episódio e responde as perguntas da seção 6.8.
16. **Render final** em qualidade `delivery` → `normalizar-audio.py` (−14 LUFS, a medida de volume percebido; pico de −1,5 dB fora do impacto). Os arquivos vão para:
    - `prontos\AAAA-MM-DD_sala-de-espera-ep01.mp4`;
    - `prontos\AAAA-MM-DD_video-dra-helena-protocolo.mp4`.
17. **Publicação:**
    - Trial Reels com as 2 primeiras falas;
    - legenda do post com os créditos CC BY, "personagens fictícias · ilustração educativa feita com apoio de IA" e "temporada 1: agenda cheia, feed vazio";
    - rótulo de IA da plataforma ligado;
    - o vídeo dela completo, 2 dias depois.

## 12. Pastas
```
hyperframes\_serie-clinicas\                    (feito uma vez)
  BRIEF.md · STORYLINES.md · LINHA-EDITORIAL.md · BIBLIA-VISUAL.md · REFERENCIAS.md
  ep01-ROTEIRO.md · ep01-SPEC.md · pesquisa\ · rascunho-sintese\
  molde\                     cópia de _molde-sabia + o que a série precisa
    lib\three-0.184.0\ · lib\gsap-3.14.2\        cópias locais (o render não depende da internet)
    compositions\_comum\
      video-camadas.html     vídeo dela em camadas de imagem: fundo do estúdio, luz que varre, varredura de vidro por máscara
      palco-3d.js            (evolução, Three.js) renderizador, luz de estúdio, sombra de contato, corte com tampas, faixa de vidro
      maquete.html           borda da maquete, desfoque de miniatura por camada, etiqueta presa por linha
      fio-e-dobra.html       o fio laranja, a leitura e a dobra em 3 tempos na batida
      celular.html           aparelho genérico em HTML + telas (câmera, perfil, conversa)
      legenda.html · assinatura-e-selo.html · cartao-serie.html
    scripts\placa-cantos.py  mede os 4 cantos da placa lisa por limiar de cor
    package.json             hyperframes@0.8.216 fixo
  personagens\dra-helena\    ficha.md · folha.png · expressoes.png · poses\ · prompts\ · rascunhos\
  personagens\marta\ · caio\ · lia\ · rafael\    (criadas no episódio de estreia de cada um, no mesmo estilo boneco)
  cenarios\consultorio-helena\   (maquete) c1-noite · c1-tarde · c2-bancada-noite · tripe-aberto · tripe-fechado · prompts\
  cenarios\recepcao-helena\      (maquete) c3-tarde · suporte-de-mesa · prompts\
  cenarios\estudio\              camadas do vídeo dela (osso-fosco · osso-limpo · protese) · prompts\
  texturas\papel\
  modelos-3d\odonto\         originais\ (copiados de brutos\) · reduzidos .glb · CREDITOS.md
  som\tema\ · som\sfx\ (dobra-1/2/3 nunca mudam) · som\scripts\ (montar-narracao.py, montar-trilha.py,
                                         normalizar-audio.py, lendo episodio.json)

hyperframes\clinicas-ep01-protocolo-implante\   (o episódio; cópia de molde\)
  SPEC.md (cópia deste) · REVIEW.md · revisao-tecnica.md · episodio.json (duração, impacto q975, tomadas)
  fonte\ (narracao.json, tomadas, trilha.json, prompts das imagens novas) · assets\ (só o novo)
  index.html (episódio) · corte-10s.html (guardado depois da aprovação 2)
  compositions\ (s01-take14 … s12-cartao; s08-video-dela é a sub-composição do vídeo dela) · renders\

hyperframes\clinicas-ep01-video-dra-helena\     (o vídeo dela; realista, em camadas, com Three.js como evolução)
  compositions\ (v0-duvida … v7-cartela) · renders\ (completo-43s.mp4)
```

## 13. Tempo estimado

| Etapa | Tempo |
|---|---|
| Corte de 10 s (virada + capa parada + 3 quadros de luz + teste da varredura) | 2 a 3 dias de trabalho depois do sim; não depende de baixar modelos (a folha B já está escolhida) |
| Piloto completo + o que falta da série (poses, molde, biblioteca de som, vídeo dela de 43 s), depois da aprovação 2 | 4 a 5 dias |
| Próximos episódios | tipo A: 1,5 a 2 dias; tipos B, C e D: cerca de 1 dia |

O render não é gargalo (medido nesta máquina: ~0,1 s por quadro nas cenas 2.5D; as camadas do vídeo dela são medidas no teste da varredura, e o Three.js, se entrar, é mais lento): cerca de 1 min para o corte, 5 a 8 min para os 69 s e 3 a 5 min para o vídeo dela completo.

## 14. O que precisa do dono
1. **Aprovar o roteiro** e responder às perguntas do `ep01-ROTEIRO.md`.
2. **Revisão técnica:** uma implantodontista real lê e assina as frases do vídeo dela antes da versão que vai ao ar.
3. **Baixar do Sketchfab só se o vídeo completo for para o Three.js** (decidido depois da aprovação 2; o corte não precisa): a mandíbula "Mandible" (Vikrama Raghuraman), a "Model Jaw - implant" (Ortomesh, como reserva), a "Permanent Dentition" (Dundee) e a "Implante Dental" (drandrescordova), com o seu login. Salvar em `brutos\2026-11-12_serie-clinicas-modelos-3d\`.
4. **A folha da personagem já está escolhida** (estilo B, 12/11/2026). Falta **aprovar as imagens paradas** (o quadro 0 e os 3 quadros de luz) antes de o corte ser animado.
5. **Antes de publicar:**
   - um advogado de saúde ou o CRO responde as perguntas da seção 6.8;
   - confirmar a licença da Helvetica Now e da Megion;
   - ligar o rótulo de IA na publicação.
6. **Autorizar ou não** a compra de um modelo pronto (US$ 10 a 50) e o uso de sons grátis (Pixabay, Openverse).
7. **A chave da OpenAI já está pronta** (cadastrada e testada em 11/11/2026). Não há nada a fazer.

## 15. Riscos principais e como evitamos

| Risco | Como evitamos |
|---|---|
| **Rosto com cara de IA na capa** (a suspeita de IA corta quase 50% da confiança, segundo a Raptive) | Na v2 ela é um boneco de série animada (estilo B), que não tenta passar por gente de verdade. O close de rosto existe só no visor (~19% da altura), com reflexo no vidro. Folha B e folha de expressões como referência; finais sempre por edição do rascunho escolhido; pele fosca, sem brilho de plástico. A abertura dos olhos tem 3 estados de pálpebra. A capa é julgada como imagem parada antes de qualquer animação; plano B: o visor desfocado. |
| **Personagem "colada" na maquete** | Placas sem personagem e a personagem como camada gerada com `--ref` da placa (mesma luz, ângulo e escala), com sombra de contato. Toda pose é conferida sobre a placa; se parecer colada, a cena é gerada com ela dentro e a profundidade é separada depois. Ação física sempre em 2 ou 3 poses-chave, nunca uma figura deslizando. |
| **Escuro "pesado"** (o dono já reprovou duas vezes) | Noite clara: pretos ≥ #2B2224, luz do abajur espalhada, sem holofote nem bola de luz, nunca um quadro preto; estúdio cinza-grafite. 3 quadros parados de luz antes de animar. Fica como pergunta ao dono. |
| **Parecer slideshow** (sequência de fotos paradas) | Toda imagem tem câmera com causa e camadas com escala própria. O que se move de verdade está na interface, no papel, no fio e no 3D. Ken Burns é proibido. |
| **3D orgânico com cara de "bolha"** | No corte, a parte realista sai de imagens geradas a partir do quadro do estúdio, que é a régua de qualidade, e não de formas feitas em código. Se o completo for para o Three.js: osso e coroas de modelos escaneados, base da prótese só depois de uma imagem parada aprovada, bloom desligado, tampas no corte (ou bloco de osso em código). |
| **Ritmo rápido demais** | Eventos de 1 a 3 s, resultado parado de 1,5 a 2 s, cada tempo da dobra 0,7 s na batida, textos inteiros. 75 palavras em 69 s. Se o dono achar rápido: cada resultado ganha +0,5 s parado e cada movimento dura 1,4 vez mais. |
| **CFO e precisão técnica** | Implantes já no lugar e paralelos. Prótese assentando só com o ok do advogado ou do CRO (plano B pronto). Assinatura, CRO e selo desde o primeiro quadro. Revisão assinada pela dentista. |
| **Venda disfarçada** | Nenhum relógio entre o envio e o post; a colega responde sobre o conteúdo ("ficou com a sua cara"), nunca sobre o método. |
| **Desistência durante o vídeo dela** | O trecho tem só 14 s, 4 mecanismos diferentes e a trilha no auge. Medimos com Trial Reels; o plano B é o narrador ler "nas palavras dela". |

---

## 16. O que mudou desde o rascunho (resumo para sessões futuras)

- Duração 68,0 → 69,2 s; impacto 31,8 → 32,5 s (q975), com a dobra na batida (0,7 s por tempo).
- Narração 82 → 75 palavras: a fala da cena 4 saiu; cena 2 "explica a prótese protocolo toda semana, paciente por paciente"; cena 10 "ela mandou o vídeo pra turma."; cena 12 "no próximo episódio: …".
- Frase da virada "faltava a **forma**" em Helvetica; nenhuma Megion.
- Primeiros 2 s refeitos (celular maior, "take 14" em 60 px, painel parado 1 s, 3 estados de olho).
- Noite clara, sem poça de abajur; abajur apaga para 30% de luz fria (nunca preto); estúdio cinza-grafite sem centro claro; cartão em chumbo #303236.
- Tarde = placa própria (C1-tarde); "escurecer pode, clarear não"; camada de luz de persiana gerada à parte saiu.
- Sem "18:10" e sem tela de bloqueio; uma resposta só ("Lúcia: ficou com a sua cara").
- "Um por um" só na cena 6: implantes por uma faixa de vidro (VARRER); cartão por máscara.
- Vídeo dela completo 36 → 43 s, na ordem clínica certa, com uma linha só de selo e aviso.
- Celular num suporte na recepção (nenhuma mão); silhueta com 2 poses; ombro e coque da tarde gerados à parte.
- Mandíbula: 1ª opção "Mandible" (sem dentes); coroas de 12 dentes da Dundee; gltf-transform; plano B do bloco de osso; crédito CC BY completo.
- Vídeo dela entra como sub-composição, não como sequência PNG.
- Corte de 10 s: UM trecho, a virada (25,3–35,3), + capa parada + 3 quadros de luz; o gancho é a alternativa.
- Conferência final (11/11/2026): a capa e os 3 quadros de luz são aprovados **antes** de animar o corte (gost-6); o verso do cartão mostra o estúdio a meia-luz, nunca abaixo de #2B2224; na cena 6 só ~14 palavras da folha ficam nítidas; "a gravação, não." ganhou 1,3 s; resultados parados de 1,5 s no plano B da prótese, nas fatias e no fio dental do completo; contagem de palavras corrigida (17 → 17); plano da trilha vai até 75 s.
- **v2 (12/11/2026)** (`DIRECAO-VISUAL-v2.md`; roteiro, tempos, narração e textos iguais): a Helena vira boneco de série animada (estilo B, rascunho `v2-folha-B-designer-toy-1.png`), de corpo inteiro, com close de rosto só no visor; a vida dela vira maquete de mesa com lente macro e desfoque de miniatura (placas sem personagem + personagem em camada); cena 2 = recuo que revela a maquete; cena 3 = mão-boneca riscando; cena 5 = ela de costas apagando o abajur; cena 11 = ela sai andando em 3 poses (no lugar da sombra); etiquetas de maquete (opcionais no ep. 01); corte de 10 s com a Helena no 1º segundo e a parte realista por camadas de imagem (osso fosco, osso limpo, prótese; varredura = troca entre os dois ossos; luz que varre), sem modelos 3D; Three.js + Sketchfab só como evolução para o completo; folha de rosto substituída pela folha de expressões; lista de imagens refeita (nº 1–19), corte ≈ US$ 2,50 e piloto ≈ US$ 5. Em aberto: a planta da cena 1 (câmera traseira sem espelho, recomendada, × visor em espelho; seção 2).

**Não aplicado, com motivo:**
- A passagem da cena 2 para a 3 por avanço dentro do papel (crítica gost-16): a emenda na textura do papel exigiria a câmera recuar de novo para mostrar a folha inteira na C2 (um vai e volta). Ficou a inclinação com a troca de placa escondida no borrão (viab-16).
- Duas respostas na cena 10 (viab-22) e linhas do cartão entrando por desfoque (viab-23, parte do cartão): substituídas pelas decisões "uma resposta só" e "cartão revelado por máscara".
- Trilha montada em 2 pedaços como regra (viab-13): ficou só como plano B; a regra é alinhar só pelo golpe.
- Rascunhos "2 com cada acabamento" (gost-14): como porcelana e vinil saíram de vez, os 4 rascunhos variam o nível de estilização (2 discretos, 2 mais perto do real).
- Mandíbula a 90% da largura (viab-32): ficou ~100% com as pontas saindo pela borda (gost-36), que garante os 40% de altura.

### Decisões depois da conferência (11/11/2026, sessão principal)

- **Cena 6, palavras pintadas paradas só 0,9 s** (ponto em aberto do verificador): no corte de 10 s, montar primeiro a versão com a dobra **uma batida depois** (impacto em q1000 = 33,33 s; o resto anda +0,83 s; filme ≈ 70 s), para as 4 palavras ficarem ~1,7 s paradas, como o dono pede. Só voltar para q975 se a prévia parecer lenta.
- **Imagens já geradas para aprovação** (em `referencias-visuais\` e nas pastas `personagens\dra-helena\rascunhos\` e `cenarios\rascunhos\`): 4 folhas "discretas" (folha-1 a 4, quase realistas) + 2 "estilizadas"; capa no visor em 2 versões (realista com --ref folha-4; estilizada com --ref folha-estilizada-2), ambas 2.6-sunburst high 1152x2048 com o consultório à noite como 2ª referência; consultório à noite e estúdio do vídeo dela (2.6-sunburst high). Custo total ≈ US$ 0,26. Observação: mesmo com o prompt "stylized", o 2.6 puxa para o realista; se o dono escolher a estilizada, reforçar a estilização no prompt antes da folha final. *(Superado na v2, 12/11/2026: o dono escolheu o estilo boneco B; essas imagens ficam só como histórico.)*
- **O quadro do estúdio (`cenarios\rascunhos\estudio-video-dela.png`) é a régua de qualidade do 3D.** Se o teste em Three.js com modelos do Sketchfab não chegar a esse nível, plano B: animar imagens geradas em camadas (mandíbula, implantes e prótese como camadas sem fundo, com luz varrendo e câmera em 2.5D). *(Na v2, de 12/11/2026, as camadas viraram o plano A do corte; o Three.js ficou como evolução.)*

### Decisões da sessão principal sobre a v2 (12/11/2026)

- **Planta da cena 1:** câmera **traseira**, com a tela virada para nós e sem espelho. O celular grava a Helena com a câmera de trás, como fazem muitos criadores para ter mais qualidade. O "apagar vídeo?" é a revisão do take logo depois de gravar: a mão-boneca dela entra desfocada pela borda do celular e toca em "apagar" (item 14). Nos próximos prompts, escrever para que lado fica a tela ("screen facing the viewer").
- **Etiquetas:** vale a leitura do redator. No ep. 01 entra no máximo "último post · agora" (cena 9) e só se o celular ficar pequeno. As outras etiquetas sugeridas na v2 repetiriam a narração ou uma tela que já está grande.
- **A "mais uma ref" do dono** (https://www.instagram.com/p/DeU__CpBun8/) é a ref5, Tiago dentista, que já está em `referencias-visuais\instagram\ref5-*` e na tabela da DIRECAO-VISUAL-v2.
- **Dobra uma batida depois** (decisão de 11/11): o corte de 10 s é montado primeiro com essa variante. Se ela entrar, a janela do corte anda +0,83 s (≈ 26,1–36,1 s) para continuar terminando no título do vídeo dela.
