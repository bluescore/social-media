---
name: carrossel-animado
description: Cria carrossel animado da Sabiá Lab para o Instagram (motion graphics feito com código no Remotion deste repositório). Cada slide vira um vídeo curto em loop, com som, na identidade da Sabiá, e sai pronto para postar em prontos\ (um MP4 e um PNG por slide, mais a legenda). Use quando pedirem carrossel animado, carrossel com movimento, carrossel em vídeo, slides que se mexem, "anima esse carrossel", post em carrossel, ou quando quiserem reaproveitar um carrossel salvo como modelo. Traz as regras de hierarquia de informação, os 5 verbos de movimento (revelar, contar, comparar, transformar, apontar), o tempo do dedo, o loop sem pulo, o som e a identidade da marca.
---

# Carrossel animado da Sabiá Lab

Você faz o carrossel animado inteiro: do tema ao MP4 de cada slide, pronto para postar. O dono traz o assunto; você cuida do roteiro dos slides, do movimento, do tempo, do som e do código. O dono está começando em edição de vídeo: não precisa saber programar, nem abrir arquivo, nem entender Remotion.

**Antes da primeira mensagem sobre o carrossel, leia este arquivo inteiro e todos os arquivos de `references/`.** Eles são o método. Sem eles, o resultado volta a ser o padrão genérico que esta skill existe para evitar.

Este método veio do material "carrossel-animado" (Downloads) e foi adaptado em 2026-11-06: o motor do carrossel vive dentro do projeto `remotion\` (não há projeto nem instalação por carrossel) e a identidade é sempre a da Sabiá.

## Como falar com o dono

- Português do Brasil, frases curtas, palavras do dia a dia. Nada de "composição", "frame", "componente", "props": diga "slide", "momento", "a seta", "o título". Termo técnico, só com explicação em uma frase.
- Use a ferramenta de perguntas com opções clicáveis sempre que puder (recomendada primeiro, marcada "(Recomendado)"). Digitar só quando a resposta é texto dele (o tema, o texto dos slides, um ajuste).
- Uma pergunta por vez quando a resposta muda o resto; várias juntas quando são independentes.
- Avise em uma linha quando algo vai demorar (render), para o silêncio não parecer travamento.
- Mostre só o que já passou na sua conferência.

## O caminho

### 0. Preparar

Nada a instalar: o projeto `remotion\` já tem tudo. Se `node_modules\` sumiu, rode `npm install` dentro de `remotion\`. Se o npm mostrar avisos de "vulnerabilities", explique em uma frase que são avisos de pacotes de desenvolvimento, normais, e não rode `npm audit fix --force`.

### 1. Conversa curta

Descubra, em no máximo duas rodadas de perguntas:
- **Tema** e, se o dono já tiver, o texto (ou um carrossel parado, em imagens, para animar).
- **Para quem** é (dono de empresa, gestor, clínica...) e **o que a pessoa deve fazer no fim** (salvar, mandar para alguém, comentar uma palavra).
- **Tema visual**: o padrão do dono é intercalar claro (branco) e laranja, começando no claro (`references/identidade.md`). Não pergunte cores nem fontes: são as da marca.
- **Referência** (opcional): o que aproveitar e o que não copiar.
- **Fotos** (opcional): de `brutos\`, copiadas para `remotion\public\carrossel\fotos\` (nunca altere `brutos\`).
- **Trilha** (opcional): música com direito de uso (a pasta `marca\musicas\` ainda está vazia). Sem trilha, só efeitos; fica ótimo.

Se ele disser só "faz um carrossel sobre X", não trave: proponha você a estrutura, o público provável e a ação final, e siga para a ficha.

### 2. A ficha (PARADA: o dono aprova)

Escreva `ficha.md` em `remotion\src\carrosseis\AAAA-MM-DD_nome\` usando `references/ficha.md`, escolhendo a estrutura em `references/roteiros.md` e aplicando `references/hierarquia.md` (um slide, uma ideia; capa promete; último pede uma ação). Cada slide com o texto e o **verbo** do movimento. Textos no tom de voz da Sabiá (`marca\marca.md`).

Mostre ao dono de forma enxuta (o texto de cada slide e o que se mexe, em uma linha cada) e pergunte: aprovar, ou ajustar. Número de dado que você não tem certeza vira `[CONFIRMAR]` e é perguntado; nunca invente número, depoimento, cliente ou resultado.

### 3. A pasta do carrossel

Crie `index.ts` (pasta, tema, `totalPrevisto` com o número de slides da ficha, sons) e registre o carrossel em `remotion\src\carrosseis\index.ts`. Veja `references/codigo.md`.

### 4. Amostra da capa (PARADA: o dono aprova)

Faça **só o slide 01** primeiro. Valida pequeno, depois aplica no todo.
1. Escreva `S01.tsx` e os sons do "01" no `sons.json` (veja `references/tempo-loop-som.md`).
2. Em `remotion\`: `npm run tsc`, depois `npm run carrossel:conferir -- <nome> 01`.
3. O `conferir` mede o loop e a margem. Depois, abra e **olhe** `remotion\work\conferencia\<pasta>\01.png` e passe as 4 perguntas de `references/conferencia.md`. Se tiver círculo, seta ou sublinhado, olhe também o momento em tamanho real (`npx remotion still`). Conserte o que falhar e repita.
4. Mostre ao dono a tira e a opção de ver tocando no Studio (`cd remotion; npx remotion studio`, pasta `carrossel-<nome>`). Pergunte: aprovar, ou ajustar. Só depois do ok, `npm run carrossel:render -- <nome> 01`.

Ajuste pedido = mude só aquilo (correção localizada).

### 5. Aplicar no resto (PARADA: o dono aprova)

Com a capa aprovada, faça os outros slides no mesmo padrão (mesma moldura, mesmos tamanhos, mesmas curvas), cada um com o seu verbo. Ponha todos na lista `slides` do `index.ts` e os sons de cada um.
Depois: `npm run tsc` e `npm run carrossel:conferir -- <nome>`. Olhe cada tira e a folha `carrossel.png` (em cima, o quadro 0 de cada slide: o carrossel tem que fazer sentido só com essa linha). Conserte e mostre. Com o ok: `npm run carrossel:render -- <nome>` e o `conferir` de novo (ele também confere os MP4).

### 6. Entrega

Em `prontos\AAAA-MM-DD_nome\`: os MP4, os PNG e um `legenda.txt` (veja `references/conferencia.md`). Diga ao dono como postar, em 4 passos curtos, e lembre de **assistir no celular antes de postar**.

### 7. Guardar como modelo (ofereça)

Se o dono gostou, ofereça guardar como modelo (`references/conferencia.md`). No próximo, basta ele dizer "usa o modelo X com esse texto".

## As regras que nunca quebram

1. Um slide, uma ideia. A capa promete, o meio entrega, o último pede uma ação.
2. **Título inteiro e legível no quadro 0.** Nunca anime a entrada do título.
3. Todo movimento tem um verbo. Um verbo por slide. Nada de tudo se mexendo ao mesmo tempo.
4. **O movimento chega quando o olho chega**: começa depois do tempo de leitura (`leitura()`), no lugar para onde a pessoa está olhando, demonstra a ideia e depois fica parado para ser lido. Um mecanismo por slide, nenhum repetido no carrossel; ~20 palavras por slide ou menos.
4b. **Gancho para o próximo slide** onde a pessoa pode parar de arrastar (fio que atravessa a borda ou a espiadinha do próximo objeto, com o som `espia`) e **menos silêncio no começo**: o movimento começa logo depois do tempo de ler o título principal (~1,3 a 2,1 s), sem esperar a leitura de tudo (`references/tempo-loop-som.md`). Carrossel de referência: `remotion\src\carrosseis\2026-11-11_paciencia\`.
5. **Loop sem pulo**: o último quadro é igual ao primeiro (o `conferir` mede; tem que dar 0).
6. Cada entrada importante ganha um som, e o carrossel funciona no mudo.
7. Uma cor de destaque (o laranja da Sabiá, ou o escuro no tema laranja). Nunca o padrão de IA (degradê com brilho, partículas por toda parte, letra por letra).
8. 1080 × 1350, um MP4 por slide, todos com a mesma duração. (É a exceção ao formato vertical 1080 × 1920 do resto do repositório.)
9. Sem número inventado, sem promessa de resultado, sem preço no slide (a não ser que o dono peça), sem música sem direito de uso.
10. Você confere antes de mostrar. O dono só vê o que passou.
11. Cor e fonte só pelo tema e pelos tokens; nunca digitadas no slide. Nunca altere `brutos\` nem `marca\`.

Onde esta skill dá um número (8 s, 4 palavras/s, 108 px), é um padrão que funciona, não uma lei: desvie quando o carrossel pedir, e diga ao dono o porquê em uma frase.

## Arquivos desta skill

- `references/hierarquia.md`: hierarquia e informação (níveis de texto, capa, último slide).
- `references/movimentos.md`: os 5 verbos, o catálogo de animações, curvas, camadas com foto e o que nunca fazer.
- `references/tempo-loop-som.md`: a linha do tempo de 8 s guiada pela leitura, o loop, os efeitos e a trilha.
- `references/roteiros.md`: 8 estruturas de carrossel com o verbo de cada slide.
- `references/identidade.md`: os 3 temas da Sabiá, fontes, logo, sementes e tom de voz.
- `references/ficha.md`: o modelo da ficha e um exemplo preenchido.
- `references/codigo.md`: onde fica cada coisa, como criar um carrossel novo e as peças prontas (para você).
- `references/conferencia.md`: conferência, entrega, como postar e modelos.
- Exemplo completo e conferido: `remotion\src\carrosseis\2026-11-06_exemplo\` (o primeiro, ainda no ritmo antigo).
- **Carrossel modelo** (o padrão a seguir): `remotion\src\carrosseis\2026-11-09_cliente-whatsapp\`, com `roteiro-motion.md` (o roteiro de movimento quadro a quadro, com o porquê de cada tempo). Leia-o antes de planejar o movimento de um carrossel novo.
