# Como o carrossel funciona no código (para você, Claude; não mostre isto ao dono)

Os carrosséis moram no **único projeto Remotion** do repositório (`remotion\`). Não se cria projeto nem `npm install` por carrossel.

## Pastas

```
remotion\
  src\
    carrossel\                 o MOTOR (comum a todos os carrosséis; só mexa para criar peça nova reaproveitável)
      marca.ts                 temas (escuro, claro, laranja; COR.cartao), FONTE, TAMANHO, MARGEM, TEXTURA, ARRASTE, MARCADORES
      tempo.ts                 8 s, 30 fps, 1080 × 1350, presenca/mola/volta/ciclo/onda/rnd, leitura/naGrade
      contexto.ts              useSlide() (número e total), useTema(), useCor()
      Moldura.tsx Titulo.tsx Camadas.tsx Icones.tsx Som.tsx verbos\*.tsx
      registrar.tsx            transforma cada carrossel em vídeos <nome>-S01, <nome>-S02...
      index.ts                 tudo num import só
    carrosseis\
      index.ts                 a LISTA de carrosséis (acrescente o novo aqui)
      MODELOS.md               carrosséis guardados como modelo
      AAAA-MM-DD_nome\         um carrossel
        ficha.md               a ficha aprovada
        index.ts               pasta, tema, ordem dos slides, sons, trilha
        S01.tsx S02.tsx ...    um arquivo por slide
        sons.json              efeitos de cada slide ("01", "02", ...)
  public\carrossel\sfx\        os efeitos sonoros (batida, whoosh, whoosh_rev, clique, clique_forte, pop, risco, po)
  public\carrossel\fotos\      fotos dos carrosséis (copie de brutos\, nunca use direto de lá)
  scripts\carrossel\           render.mjs, conferir.mjs (+ comum.mjs, png.mjs)
  work\conferencia\<pasta>\    tiras para você olhar (fora do git)
prontos\AAAA-MM-DD_nome\       01.mp4, 01.png, ..., legenda.txt (o que o dono posta)
```

## Comandos (sempre dentro de `remotion\`)

- `npx remotion studio`: prévia no navegador (pasta `carrossel-<nome>` na lista).
- `npm run tsc`: checa erros de digitação no código.
- `npm run carrossel:render -- <nome>` (todos) · `-- <nome> 01` (só a capa) · `-- <nome> 02,05`.
- `npm run carrossel:conferir -- <nome>` (ou `-- <nome> 01`).
- Um momento em tamanho real: `npx remotion still <nome>-S01 <scratchpad>\x.png --frame=75` (75 = 2,5 s).

`<nome>` é o nome curto (depois do `_`) ou a pasta inteira. Os dois scripts aceitam os dois.

## Carrossel novo, passo a passo

1. Crie `src\carrosseis\AAAA-MM-DD_nome\` (nome curto: minúsculas, números e hífen; não pode repetir o de outro carrossel).
2. `index.ts`:
   ```ts
   import { definirCarrossel } from "../../carrossel";
   import { S01 } from "./S01";
   import sons from "./sons.json";

   export default definirCarrossel({
     pasta: "2026-11-20_nome",
     tema: "escuro",
     slides: [S01],
     totalPrevisto: 7, // da ficha: a amostra da capa já sai com "01 / 07"
     sons,
     // trilha: { arquivo: "marca/musicas/x.mp3", inicio: 12, passo: 6, ganho: -11 },
   });
   ```
3. Acrescente em `src\carrosseis\index.ts`: `import nome from "./2026-11-20_nome";` e ponha na lista `CARROSSEIS`.
4. Escreva os slides e o `sons.json`. Quando todos existirem, tire o `totalPrevisto` (ou deixe igual ao número de slides).

O exemplo completo e conferido está em `src\carrosseis\2026-11-06_exemplo\` (capa com círculo à mão e sementes, lista que acende, troca riscada, último slide com ícones e seta).

## Esqueleto de um slide

```tsx
import React from "react";
import { useCurrentFrame } from "remotion";
import { MARGEM, Marca, Moldura, Titulo, presenca, s, useCor } from "../../carrossel";

// Slide 03 · TRANSFORMAR: "piso e pintura" é riscado e vira a lista completa.
export const S03: React.FC = () => {
  const f = useCurrentFrame();
  const COR = useCor();
  const caixa = presenca(f, s(0.5), s(0.4), 2); // entra em 0,5 s, volta no loop
  return (
    <Moldura>
      <Titulo rotulo="ERRO 1" linhas={["Orçar só o", <Marca key="m">acabamento.</Marca>]} sub="A infraestrutura vem antes." />
      <div style={{ position: "absolute", left: MARGEM, right: MARGEM, top: 640, opacity: caixa, background: COR.superficie }}>
        {/* ... o verbo do slide ... */}
      </div>
    </Moldura>
  );
};
```

## Regras do código

- Tudo é função do quadro (`useCurrentFrame()`). Nada de `useState`, `setTimeout`, `transition` ou `@keyframes` do CSS.
- Tempos em segundos com `s(1.5)`. Entradas com `presenca(f, s(em), s(dur), ordem)` ou `mola(f, s(em), ordem)`; elas voltam sozinhas a partir de 5 s. `ordem` maior = volta depois (o primeiro a entrar é o último a voltar: dê a ele a maior `ordem`).
- Movimento contínuo: `ciclo(f, voltas)` / `onda(f, voltas)` com voltas inteiras.
- Aleatório: `rnd(n)`, nunca `Math.random()`.
- Posições em pixels do quadro (1080 × 1350). Camadas de `Seta`, `CirculoMao`, `Holofote` e `Pulso` ocupam o quadro todo: use coordenadas absolutas.
- **Cores só pelo tema**: `const COR = useCor();` dentro do componente, e `COR.destaque`, `COR.texto2`... Fontes por `FONTE.texto` (Helvetica, com `FONTE.espaco` e `FONTE.entrelinha`) e `FONTE.palavra` (Megion, só dentro de `<Palavra>`); pesos `FONTE.pesoTexto` (Regular) / `pesoForte` (Bold). Nunca `#F34500` nem `"Megion"` escrito no slide.
- `useCor()` é um "hook": chame sempre no topo do componente, nunca dentro de `if` ou depois de `??`.
- Imagens: `<Img src={staticFile("carrossel/fotos/x.jpg")} />` ou a peça `Foto`. Arquivo em `remotion\public\`.
- Um slide = um arquivo, com um comentário no topo dizendo o número, o verbo e o que se mexe.
- **O quadro 0 tem conteúdo, não só o título.** O PNG do quadro 0 é a versão parada do slide: deixe visível o "antes" (a frase que vai ser riscada, a lista apagada em ~30%, o gráfico em fantasma tracejado, o cartão do "errado").
- Peças que acompanham um número (blocos, barras, gráfico): use `valorContagem(f, de, ate, inicio, fim)`, a mesma conta do `Contador`.
- `Riscar` e `Troca` riscam UMA linha. Texto de duas linhas: um `Riscar` por linha.
- O `Titulo` não quebra linha sozinho (de propósito): cada item de `linhas` é uma linha. Uma linha pode misturar texto e destaque: `<>faz isso <Destaque>na mão?</Destaque></>`.
- Destaque: `Destaque` (Helvetica Bold na cor de destaque; o tema decide, `estiloDestaque: "cor"`) ou `Marca` (o mesmo, com barra que se desenha). Exemplo da capa modelo: `linhas={["Seu cliente chamou no", <>WhatsApp <Destaque>e desistiu</Destaque></>]}`. `Palavra` (Megion, caixa alta) só para palavra realmente sozinha, como linha própria: `style={{ display: "block", marginTop: 56 }}`.
- Texto com inicial maiúscula no começo da frase e em nome próprio. Ver `identidade.md`.
- Fundos intercalados: no `index.ts`, `tema: ["claro", "laranja"]`.
- Peças comuns de todo slide (`Conversa.tsx`): `Cartao` (cartão grande; ilha clara no slide laranja), `Contato` (avatar + "Cliente" + "online"), `Balao` (`lado` "cliente" ou "empresa", `hora` "10h02"; o "visto" ✓✓ só aparece no lado "empresa", como no WhatsApp), `estiloTexto` e `Puxa` (a frase que fica no ar no pé dos slides do meio, Bold 44 px). Cor do que se destaca: `useCorTrecho()` (laranja no claro, branco no laranja). Também em `Conversa.tsx`: `Avatar` (silhueta do cliente, `tamanho`), `Horas` (o "5h38" da capa: Bold, algarismos de largura fixa, "h" a 62%) e, no `Balao`, `corHora`/`corVisto` (a hora e o visto que acendem em laranja). Ícone `Lua` em `Icones.tsx`. O carrossel modelo `2026-11-09_cliente-whatsapp` (versão 8 s) tem um mecanismo diferente em cada slide: 01 odômetro + caneta, 02 gaveta, 03 mergulho de câmera, 04 foco na grade, 05 lista que reordena, 06 "digitando" que vira painel, 07 palavra que voa. O porquê de cada tempo está no `roteiro-motion.md` da pasta dele.
- `SEGUNDOS` e `BATIDA` (em `tempo.ts`) valem para TODOS os carrosséis. Não mude por causa de um só.
- Tempo de leitura: `leitura(texto, aPartirDe)` devolve o segundo em que a pessoa termina de ler (~4 palavras/s + 0,3 s); use para decidir quando o movimento começa. `naGrade(seg)` arredonda para 0,25 s. O retorno é `VOLTA` (7 s, o último segundo).

## Medidas (para posicionar círculo, seta, sublinhado)

Cartão dos slides do meio (padrão do modelo cliente-whatsapp): começa em y 412 quando o título tem 2 linhas sem rótulo, e em y 478 com rótulo + título de 2 linhas; termina em ~1160 (a frase do pé fica entre ~1220 e 1263). Texto que precisa ser lido no celular (hora que muda, desfecho): no mínimo ~36 px.

Helvetica Regular 88 px (-0.05em): "Seu cliente chamou no" ≈ 857 px (cabe em 864, a largura útil com margem 108); linha a linha 79 px; altura do "l" ≈ 63 px. Com `top={190}` (capa modelo) as letras começam em ~200, a linha de base da 2ª linha fica em ~342 e o apoio (44 px) começa em ~381; cada px a mais no `top` desce tudo junto. Megion caixa alta 156 px (+0.03em): "DESISTIU." ≈ 755 px. Medir antes de escrever: `node` com `opentype.js` (já instalado) e `font.getAdvanceWidth(texto, tamanho)`.
Círculo em volta de palavra comprida encostada na margem passa da margem: ponha o `CirculoMao` no `fundo` da Moldura (fica por baixo das letras e o `conferir` aceita).
`RiscoMao` (risco de caneta embaixo do trecho): `x1`/`x2` = começo e fim do trecho, `y` ≈ linha de base + 18. Na capa modelo: `<RiscoMao x1={524} x2={872} y={360} em={3.0} ordem={0} cor={COR.destaque} />`. Na dúvida, renderize o quadro com `remotion still` e meça na imagem. Anotação à mão (círculo, seta) não pode encostar na palavra vizinha nem na linha de cima.

`CirculoMao` tem `comeco` (graus, onde a caneta começa). Com texto logo acima, use `comeco={27}`: a sobra do traço cai embaixo.

## Peças prontas (import de "../../carrossel")

| Peça | Para | Props principais |
|---|---|---|
| `Moldura` | fundo, granulado, cabeçalho (logo; 01/07 e rodapé só se `MARCADORES`/`ARRASTE` ligados) | `fundo` (camada de foto, sementes ou círculo que passa da margem), `final` + `textoFinal`, `limpo`, `corFundo` |
| `Titulo` | título fixo no quadro 0 | `linhas[]`, `sub`, `rotulo`, `top`, `tamanho`, `alinhar`, `largura` |
| `Marca` / `Destaque` | trecho em Bold na cor de destaque (com barra animada / parado) | `em` |
| `Palavra` | UMA palavra realmente sozinha em Megion caixa alta | `tamanho`, `cor`, `style` |
| `RiscoMao` | APONTAR com risco de caneta embaixo de um trecho | `x1`, `x2`, `y`, `em`, `dur`, `cor` (sem `cor`, segue o trecho-chave), `curva` (ex.: `Easing.bezier(0.33, 0, 0.25, 1)` para a caneta acompanhar a leitura) |
| `Rotulo` | etiqueta "passo 2" | `cheio` |
| `Texto` | texto de corpo com tamanho mínimo garantido | `tamanho`, `cor`, `peso` |
| `Revela` | REVELAR qualquer coisa | `em`, `dur`, `jeito` (sobe, mascara, escala, desfoque, aparece), `ordem` |
| `Lista` | REVELAR itens na batida | `itens[]`, `inicio`, `intervalo`, `jeito` |
| `Contador` | CONTAR número | `ate`, `de`, `inicio`, `fim`, `casas`, `prefixo`, `sufixo`, `tamanho` |
| `Barra` / `Anel` | CONTAR proporção | `valor` (0 a 1), `inicio`, `dur`, `largura` / `raio` |
| `Comparar` | COMPARAR em cartões | `antes`, `depois`, `rotuloAntes`, `rotuloDepois`, `inicio`, `vence`, `top`, `altura`, `empilhado` |
| `Cortina` | COMPARAR com fotos | `antes`, `depois` (camadas), `inicio`, `dur`, `ate` |
| `Riscar` | TRANSFORMAR (risco de caneta) | `em` |
| `Troca` | TRANSFORMAR (risca, sai, entra o novo) | `antes`, `depois`, `risca`, `troca` |
| `Decodificar` | TRANSFORMAR (letras embaralhando) | `linhas[]`, `inicio`, `dur` |
| `Seta` | APONTAR | `de`, `para`, `curva`, `em` |
| `CirculoMao` | APONTAR | `cx`, `cy`, `rx`, `ry`, `em`, `comeco` |
| `Holofote` / `Pulso` | APONTAR | `x`, `y`, `raio`, `em` |
| `Foto` | foto que respira + degradê de leitura | `src`, `zoom`, `leitura` (topo, base, nenhum) |
| `Sementes` | respiro com o grafismo da marca | `x`, `y`, `largura`, `formato` (soltas, cacho), `estilo`, `cor`, `girar` |
| `Flutua` / `Gira` | respiro contínuo | `amplitude` / `voltas`, `balanco` |
| `Particulas` | pó, vapor, poeira | `quantidade`, `direcao`, `area`, `cor`, `tamanho`, `desfoque` |
| `Salvar`, `Enviar`, `Comentar`, `Curtir`, `Check`, `Xis` | ícones de traço | `tamanho`, `cor`, `cheio` |
| `Logo` (de `../../marca/Logo`) | logo da Sabiá em código | `cor` (preto, branco, laranja), `lab`, `largura` |

Peça que não existe? Crie no slide (ou em `src\carrossel\` se for reaproveitar, exportando no `index.ts`), com as mesmas funções de tempo e `useCor()`.

## Padrões que resolvem slides comuns

**Último slide com ícones de ação** (ver `2026-11-06_exemplo\S04.tsx`):
```tsx
<Moldura final textoFinal="SALVE">
  <Titulo linhas={["Salve para", "rever com", <Marca key="m">sua equipe.</Marca>]} sub="E mande para quem cuida da operação." />
  <Revela em={1} jeito="escala" ordem={1} style={{ position: "absolute", left: 300, top: 820 }}><Salvar tamanho={150} /></Revela>
  <Revela em={1.5} jeito="escala" style={{ position: "absolute", left: 600, top: 820 }}><Enviar tamanho={150} /></Revela>
  <Seta de={[170, 720]} para={[285, 850]} curva={-0.3} em={2.5} />
</Moldura>
```

**Lista que acende** (quadro 0 com tudo apagado; ver `S02.tsx` do exemplo): cada item com `opacity: lerp(0.28, 1, presenca(f, s(1 + i), s(0.4), total - 1 - i))`.

**Gráfico que se desenha (APONTAR o ponto):** desenhe o caminho SVG inteiro, revele com `clipPath` (um `rect` cuja largura vai de 0 ao total com `p(f, s(0.5), s(2), LINEAR) * (1 - volta(f, 2, 16))`), deixe um "fantasma" tracejado do gráfico no quadro 0 e use `CirculoMao` no ponto que importa em 2,5 s.

**Foto em camadas:**
```tsx
<Moldura fundo={<Foto src="carrossel/fotos/escritorio.jpg" zoom={0.04} leitura="topo" />}>
  <Titulo linhas={["Seu time pode", <Marca key="m">render mais.</Marca>]} />
</Moldura>
```

## Erros comuns

- **Texto passou da margem:** quebre em mais linhas ou baixe o `tamanho`. O `conferir` acusa. Atenção ao "j" da Megion: o gancho passa uns pixels para a esquerda; evite "j" no começo de linha.
- **"pixels diferentes" no conferir:** algum elemento não volta (falta `presenca`/`volta`/`mola`) ou um `ciclo` tem voltas quebradas.
- **Sem som num slide:** a chave em `sons.json` precisa ser "01", "02"... (com zero) e o arquivo precisa existir em `public\carrossel\sfx\`.
- **Nome repetido:** dois carrosséis com o mesmo nome curto quebram o Studio. Use nomes diferentes.
- **Render lento:** muitas partículas com desfoque ou fotos enormes. Reduza a foto para ~1600 px de altura.
