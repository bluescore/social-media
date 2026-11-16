# Conferência, entrega e modelo

## Antes de mostrar qualquer coisa ao dono

Rode `npm run carrossel:conferir -- <nome>` (ou `-- <nome> 01` na amostra), dentro de `remotion\`, e **olhe as tiras** em `remotion\work\conferencia\<pasta>\` (no tamanho de celular). Confira:

1. **Dá para ler a ideia em 1 segundo?** O primeiro quadro da tira tem o título inteiro, sem nada cobrindo, em tamanho legível. **E o quadro 0 mostra conteúdo** (o "antes", a lista apagada, o gráfico em fantasma), não uma caixa vazia esperando a animação.
2. **Cada movimento tem um verbo?** Nada se mexendo "só para enfeitar". No máximo um respiro contínuo.
3. **O loop fecha sem pulo?** O conferir tem que dizer "sem pulo" (0 pixel diferente).
4. **O som cai junto com o que entra?** Os `t` do `sons.json` batem com os segundos do código.

E também: nada passa da margem (o `conferir` mede); nenhum texto abaixo de 22 px; a cor de destaque aparece pouco e sempre no que importa; os slides parecem uma série (mesma moldura, mesmo alinhamento, mesmo raio); nenhuma anotação (círculo, seta) encosta em letra vizinha.

Para olhar um momento em tamanho real (ex.: o círculo à mão em 2,5 s):
`npx remotion still <nome>-S01 <scratchpad>\s01.png --frame=75`

Se algo falhar, conserte antes de mostrar. Ao dono, mostre só o que passou.

## Mostrar ao dono

- Diga onde estão os arquivos (`prontos\<pasta>\01.mp4`) e mostre a folha `carrossel.png` (em cima, o quadro 0 de cada slide; embaixo, o 3,5 s).
- Para ver tocando: `cd remotion; npx remotion studio` e abrir a pasta `carrossel-<nome>` na lista da esquerda.
- Pergunte com opções clicáveis: "Aprovado", "Quero ajustar (me diga o quê)".

## Correção localizada

Quando o dono pede um ajuste ("o título demorou", "a seta está estranha"), mude **só aquilo**. Repita o pedido em uma frase, conserte, rode o conferir do slide, mostre de novo. Nada de "aproveitei e melhorei outras coisas".

## Entrega final

Em `prontos\<AAAA-MM-DD_nome>\`:
- `01.mp4` a `NN.mp4`: um vídeo por slide, 1080 × 1350, 8 s, com som.
- `01.png` a `NN.png`: o primeiro quadro de cada um (a versão parada, se um dia precisar).
- `legenda.txt`: legenda sugerida para o post (gancho na primeira linha, o resumo em 2 a 4 linhas, o pedido de ação, 3 a 5 hashtags do nicho). No tom de voz da Sabiá (`marca\marca.md`: inteligente sem ser complexo, próximo sem ser informal demais, seguro sem prometer demais), sem número inventado, sem promessa de resultado, sem travessão. Emoji só se a marca costuma usar, e pouco.

## Como postar (diga ao dono)

1. Mande os arquivos para o celular e **assista lá antes de postar**. A prévia no computador engana: é no celular que se descobre texto pequeno.
2. No Instagram, novo post, escolha os vídeos **na ordem** (01, 02, 03...). Todos têm o mesmo tamanho, então nada é cortado.
3. Cada slide toca, com o som, quando a pessoa chega nele.
4. Se o Instagram oferecer música para o post, deixe sem (o som já está nos vídeos).

Limites do Instagram (realidade de setembro de 2026, confira no app): até 20 itens por carrossel; o formato de todos segue o do primeiro item.

## Guardar como modelo

Todo carrossel já fica guardado em `remotion\src\carrosseis\<pasta>\`. "Guardar como modelo" é só dar nome e escrever o estilo. Quando o dono aprovar, ofereça. Se aceitar:

1. Escreva `ESTILO.md` na pasta do carrossel: tema, tamanhos, como os elementos entram, ritmo, sons, o que NÃO fazer, e qual slide serve de exemplo de cada verbo.
2. Acrescente uma linha em `remotion\src\carrosseis\MODELOS.md`: `- <nome-do-modelo> → <pasta> — <uma linha do que é>`.
3. Se você criou uma peça nova que vale reaproveitar, mova para `remotion\src\carrossel\` (o motor) e exporte no `index.ts` de lá.

No próximo pedido ("usa o modelo X com esse texto novo"): leia `MODELOS.md`, copie a pasta do modelo para a pasta nova (`AAAA-MM-DD_nome-novo`), troque `pasta` no `index.ts`, leia o `ESTILO.md`, monte a ficha nova com o texto novo e siga o caminho normal (amostra da capa primeiro). O modelo dá a cara; o texto e os verbos são novos.
