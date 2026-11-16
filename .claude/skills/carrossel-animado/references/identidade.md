# Identidade: a cara da Sabiá

A identidade já está pronta e não se pergunta de novo: é a da **Sabiá Lab** (`marca\marca.md`). No carrossel ela mora em `remotion\src\carrossel\marca.ts`, que puxa cores e fontes de `remotion\src\marca\marca.ts`. **Nunca digite cor ou fonte num slide**: use `useCor()` (cores do tema), `FONTE`, `TAMANHO`, `MARGEM`.

## Os três temas

Cada carrossel escolhe o tema no seu `index.ts`. Uma lista intercala: `tema: ["claro", "laranja"]` = slide 1 claro, 2 laranja, 3 claro... Um slide pode ter o seu: `slides: [{ slide: S01, tema: "laranja" }, S02, ...]`.

**Padrão do dono (2026-11-09, carrossel modelo "cliente-whatsapp"): fundos intercalados, começando no claro (branco): 01 branco, 02 laranja, 03 branco, e assim por diante.** O fundo preto pesa a leitura. (Antes disso o padrão foi capa laranja e o resto claro; o dono gostou, mas pediu para testar a capa branca com a troca de cor a cada lâmina.) Use o escuro só se o dono pedir.

| Tema | Fundo | Texto | Destaque | Palavra-chave | Logo | Sementes | Quando |
|---|---|---|---|---|---|---|---|
| **laranja** | laranja `#F34500` | branco | `#1E1415` | branca (Bold, mesma cor; risco e rótulo brancos) | branco | menta | slides pares (padrão) |
| **claro** | `#F6F4F1` off-white | `#181818` | laranja `#F34500` | laranja (Bold ou Megion) | preto | laranja | capa e slides ímpares (padrão) |
| **escuro** | `#1E1415` preto amarronzado | branco | laranja `#F34500` | laranja | branco | laranja | só se o dono pedir |

Os dois modelos foram aprovados pelo dono em 2026-11-09 (o branco, com fundos intercalados, e o laranja, da capa v4). O primeiro carrossel completo saiu no branco.

Cartão grande: use a peça `Cartao` (de `Conversa.tsx`), que já resolve os dois casos. Por dentro: fundo `COR.cartao` (no claro é branco puro sobre o off-white, com sombra bem leve: `boxShadow: 0 24px 64px ${hexA(COR.texto, 0.08)}`). Cartão claro sobre um slide laranja: envolva com `<TemaInfo.Provider value={TEMAS.claro}>`; o número de destaque dentro dele fica laranja.

Pares de cor que o guia aprova: fundo escuro com laranja ou branco; laranja com preto ou branco; lima com preto; menta com lima. Lima e menta não entram como destaque de texto (somem no fundo claro e brigam com o laranja); podem aparecer nas sementes.

## Fontes

Pedido do dono (2026-11-09); já está nos tokens de `marca.ts` e nas peças `Titulo`, `Destaque`, `Palavra`, `Texto`:
- **Helvetica Now Text em quase tudo** (título, apoio, rótulos, números): **Regular** no texto, **Bold** no trecho-chave (`<Destaque>`), **na cor do trecho** (`useCorTrecho()`: laranja no fundo claro, branco no fundo laranja, como os dois modelos aprovados). Não use 800: não está carregado.
- Helvetica com **espaço entre letras -50** (`-0.05em`) e **entrelinha 0.9**.
- **Inicial maiúscula** no começo de cada frase (título, apoio, rótulos como "Momento 1 de 3", mensagens de exemplo) e em nome próprio (WhatsApp, Instagram); o resto minúsculo. (Pedido do dono, 2026-11-09; antes era tudo minúsculo.)
- **Sem ponto final** no título e no apoio. (Mensagem de exemplo num balão pode ter "?" e "!".)
- **Diagramação do título** (exemplo do dono, 2026-11-09): 2 linhas de Helvetica Regular 88 px, o trecho-chave em Bold no fim da frase ("Seu cliente chamou no / WhatsApp **e desistiu**", com "e desistiu" em laranja), apoio de 44 px colado embaixo na mesma cor do texto (sem cinza), alinhado à esquerda, margem de 108 px. O exemplo é só referência de diagramação, não de posição.
- **Megion Bold só para uma palavra realmente sozinha, em CAIXA ALTA** (`<Palavra tamanho={...}>checklist</Palavra>`), como a palavra para comentar no último slide. Palavra-chave no meio ou no fim da frase vai em Helvetica Bold, não em Megion. Espaço `+0.03em` (mais justo que isso as letras se colam).
- Com entrelinha 0.9 não cabe círculo à mão em volta de palavra do título: use o risco de caneta (`<RiscoMao cor={COR.destaque}>`) embaixo do trecho em Bold.
- Horário no jeito brasileiro: `10h02`, `15h` (nunca `10:02`).
- Licença da Helvetica Now e da Megion ainda não confirmada (pendência em `marca\marca.md`). Não precisa repetir isso a cada carrossel.

## Preencher o post

Pedido do dono (2026-11-09): **o slide tem que usar o espaço de 1080 × 1350 inteiro**. Nada de faixa vazia grande (ex.: um buraco entre o logo e o título). O título começa uns 80 px abaixo do logo; o que vem embaixo (cartão, comparação, conversa) cresce até uns 90 px do pé. Se sobrar espaço, aumente o cartão, a letra de dentro dele e os números, ou ponha mais uma informação que ajude (uma segunda mensagem, um detalhe real), nunca enfeite. Capa modelo: título em `top={190}`, cartão de 478 a ~1258 px.

## Logo e grafismos

- O cabeçalho já traz o logo (passarinho + "sabiá", sem o LAB, que ficaria pequeno demais), na versão do tema.
- **Sementes** (`<Sementes>`): o grafismo da marca. O dono achou que sobravam pequenas e soltas no meio do slide (2026-11-09). Quando usar: **grande, cortado no canto ou como detalhe**, no `fundo` da Moldura, nunca cobrindo texto. Só se fizer sentido no carrossel; na dúvida, sem.
- **Sem contador "01 / 07", sem barrinhas de progresso e sem "arraste"** (o dono achou que sobravam; desligados em `marca.ts`: `MARCADORES` e `ARRASTE`). O slide do meio puxa o próximo pela frase que fica no ar.
- O nome "sabiá" é sempre minúsculo e na Megion. Não reescreva o logo à mão: use o `Logo` de `remotion\src\marca\Logo.tsx`.
- O slogan "inteligência que participa" (minúsculo, sem ponto, como no fechamento dos teasers) pode entrar no último slide, pequeno, em Helvetica. Só se couber sem brigar com o pedido de ação.

## Tom de voz nos textos

Do `marca\marca.md`:
- **Inteligente sem ser complexo**: termo técnico vem com tradução ("automação: quando o sistema faz sozinho").
- **Próximo sem ser informal demais**: conversa com o dono da empresa, nada de gíria pesada.
- **Seguro sem ser arrogante**: nada de "garantido", "revolucionário", "10x", nem número que não foi confirmado.

## Regras da cara

- Uma cor de destaque. Fundo, texto e destaque; o resto são transparências desses três (`texto2`, `texto3`, `linha`, `superficie`).
- Fundo chapado com granulado leve (`TEXTURA`) em vez de degradê. O degradê da paleta é da marca, mas no carrossel use só se o dono pedir.
- Cantos: 28 a 32 px nas caixas e cartões, em todos os slides.
- Ícones de traço, todos com a mesma espessura.
- Fotos: mesma luz e mesma temperatura de cor em todos os slides. Não aplique "look" de cor sem mostrar antes e depois.
- Sem preço nos slides (a não ser que o dono peça).

## Se o dono trouxer uma referência

Diga o que vai aproveitar (ritmo, tamanho do título, jeito que os elementos entram) e o que **não** vai copiar (textos, marca, fotos, qualquer assinatura de quem fez). O resultado tem que parecer Sabiá, não um clone.
