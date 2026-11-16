# Revisão — teaser "Funcionária Digital — em breve"

**Peça (versão atual):** 15 s, 1920 × 1080, 60 fps, MP4 H.264 + AAC, em `prontos\2026-11-05_teaser-sabia-15s.mp4`. Versões anteriores: 10 s (`prontos\2026-11-05_teaser-funcionaria-digital.mp4`) e 20 s (`prontos\2026-11-05_teaser-funcionaria-digital-20s.mp4`). As seções abaixo vão da primeira versão para a atual.
**Ferramenta:** um HTML só (`index.html`), em que cada quadro é calculado a partir do tempo dentro de `window.seek(t)`. O render é feito pelo Playwright + FFmpeg (`render.mjs`). Não é um projeto HyperFrames padrão, porque o pedido trazia um processo próprio de render.

## Decisões
- **Sem roadmap:** nenhum foi enviado. A Funcionária Digital (produto de destaque no `marca.md`) foi tratada como a novidade. Sem datas, sem números e sem promessas além de "responde, organiza, marca reunião".
- **Interface redesenhada, sem prints:** a plataforma conectada tem dados reais de clientes. Todos os nomes do vídeo são inventados (Ana Souza, Carla Dias…).
- **Objeto que atravessa o vídeo:** o balão laranja. Ele passa por ponto final → "digitando…" → resposta → card do funil → evento da agenda → passarinho. É a única coisa laranja além de "em breve".
- **Logo:** passarinho preto de verdade (`icone_preto.png`). O contorno vetorial foi tirado do próprio PNG, para o laranja se transformar exatamente nele. A linha laranja fica só na costa do passarinho, como a luz na referência `logo-animado`.
- **"sabiá"** no cartão final está montado com as proporções do `Logo.tsx` da marca, em branco, porque o fundo é escuro. O resto do texto usa só a Helvetica Now Text.
- **Trilha** feita em código (`audio.html`): 120 BPM, ré menor (Dm | Bb | F | C | Fmaj7). Tem bumbo em toda batida, impacto nas trocas de cena (2, 4, 6 e 8 s), cliques junto com o cursor e um canto curto de sabiá quando o logo se forma.

## Medido / olhado
- Uma imagem por batida e por meia batida (41 imagens), revisadas em três rodadas. Corrigido: tela vazia nas batidas de troca de cena, interface pequena demais, cards do funil se sobrepondo, saídas de texto lentas, cursor tapando o botão "Agendar".
- Bumbo conferido no arquivo de som: há um salto de volume no início de cada uma das 20 batidas.
- Volume: −13,7 LUFS integrado, pico em −1 dBFS.

## Pontos fracos
- Nas batidas de troca de cena (2, 4 e 6 s), o quadro exato mostra a interface ainda abrindo. Em movimento isso funciona, mas parado parece meio vazio.
- Os textos menores da interface (nomes nos cards, horários) ficam pequenos no celular. Dá para ler, mas não são o foco.
- A Helvetica Now Text ainda está com a licença pendente (ver `marca.md`).

## Revisão 2 (pedido do dono, 2026-11-05)
- **De 10 s para 20 s:** a linha do tempo antiga é percorrida na metade da velocidade (`SPEED = 2`), e cada animação fica só 1,3× mais longa (`K = 0,65`). Assim sobra respiro entre os momentos sem deixar o movimento mole. O "carimbo" na agenda continua caindo exatamente na batida forte (12 s).
- **Final só com o logo preto:** a aresta laranja recua até a costa e sai pela cabeça entre 17,2 s e 19,1 s. Conferido no último quadro: nenhum pixel laranja.
- **Slogan no lugar de "Funcionária Digital · em breve":** "Inteligência que participa.", copiando a página 12 do guia (`Downloads\Guia de marca - Blue Score.pdf`), que usa Helvetica oblíqua branca. Aqui é a Helvetica Now Text Regular Italic, 64 px, branca, centralizada.
- **Trilha refeita para 20 s:** um acorde por cena (Dm, Bb, F, C, Fmaj7), impactos em 4, 8, 12 e 16 s, sons nos novos tempos do cursor. Medido: −14,4 LUFS; bumbo nas 40 batidas.

## Revisão 3 (pedido do dono, 2026-11-05) — versão atual
- **15 s** em `prontos\2026-11-05_teaser-sabia-15s.mp4` (as versões de 10 s e 20 s continuam em `prontos\`).
- O ritmo agora é **80 BPM** (1 batida = 0,75 s). Assim cada momento da linha antiga cai numa batida: a linha é percorrida a 1/1,5 da velocidade (`SPEED = 1,5`) e as animações ficam 1,2× mais longas (`K = 0,8`). Trocas de cena em 3, 6, 9 (batida forte) e 12 s.
- **Ícone branco** (`icone_branco.png`, quadrado de 377 px) no lugar do preto. O contorno foi tirado do próprio PNG branco, e a posição segue a variante branca do `Logo.tsx` (caixa do passarinho em 458,1 / 321,2). A transição continua: o branco varre o laranja e deixa a aresta laranja, que depois some. **Últimos ~0,8 s só com o logo**, sem nenhum pixel laranja (conferido em 14,25 s e 15 s).
- **Slogan** em caixa baixa e sem itálico ("inteligência que participa."), Helvetica Now Text Regular, branco, logo abaixo de "sabiá", com a mesma largura do nome (as bordas esquerda e direita alinham).
- Trilha: −14,8 LUFS. O bumbo aparece em 18 de 19 batidas medidas; na de 9 s o som de subida mascara a medida, mas o bumbo está lá.

## Revisão 4 (pedido do dono, 2026-11-05) — versão odontológica
- Arquivo: `prontos\2026-11-05_teaser-sabia-odonto-15s.mp4` (a versão de 15 s genérica continua em `prontos\2026-11-05_teaser-sabia-15s.mp4`).
- Texto com palavras de clínica, sem dizer "odontologia":
  - gancho "Paciente sem resposta";
  - a paciente pede "Oi! Queria agendar uma avaliação." e a resposta automática é "Claro! Quarta às 10h, pode ser?". Esse horário é o mesmo evento que cai depois na agenda (quarta, 10:00);
  - "Funil de pacientes" com as etapas Em conversa → Avaliação → Orçamento;
  - cards com procedimentos (Clareamento, Implante, Ortodontia, Limpeza, Prótese, Lentes de contato, Canal);
  - "Consultas" no lugar de "Agenda", com consultas de Limpeza, Clareamento, Canal, Retorno, Implante e Manutenção;
  - evento "Avaliação · Ana Souza"; legenda "Marca a avaliação".
- Os três títulos grandes terminam com o **ponto laranja redondo** (0,22 em, a mesma proporção do ponto do gancho). O ponto nasce logo depois que a linha pousa, como o ponto que abre o vídeo.
- Slogan sem ponto final: "inteligência que participa".
- Corrigido: "10:00 – 11:00" e "Confirmada" se sobrepunham na troca; o cursor agora segura o card pelo canto e não cobre o texto.
- A trilha é a mesma da versão de 15 s (os tempos não mudaram).

## Revisão 5 (2026-11-05) — versão vertical para celular
- Arquivo: `prontos\2026-11-05_teaser-sabia-odonto-15s-vertical.mp4` (1080 × 1920, 60 fps, 15 s, mesma trilha).
- O mesmo `index.html` gera as duas versões. Com `?v` no endereço ele monta o layout vertical. O render é `VERT=1 node render.mjs full <saída>`.
- O que muda no vertical:
  - gancho em três linhas ("Paciente / sem / resposta");
  - títulos grandes **em cima** de cada tela, alinhados com a borda do chat;
  - câmera reenquadrada para cada momento (tabela própria em `camSetup`);
  - cartão final ocupando cerca de 80% da largura.
- Conferido em uma imagem por batida. Títulos e telas ficam dentro do quadro, e o cartão final fica no centro, longe da área de botões do Instagram (embaixo e à direita). Apenas o passarinho dos 12 s precisou afastar a câmera.
- Ponto fraco: no vertical, o slogan embaixo do nome fica pequeno, cerca de 38 px de altura de letra na tela. Dá para ler no celular, mas não é grande.
