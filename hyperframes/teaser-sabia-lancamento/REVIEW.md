# REVIEW — teaser-sabia-lancamento

**Peça:** 9 s, 1080 × 1920, 30 fps. Referência: `brutos\teaser-sabia-lancamento\exemplo.mp4`.

## O que foi copiado do exemplo
- Corte seco a cada 0,3 s (9 quadros), medido no exemplo: 26 cortes, todos na grade de 0,3 s.
- Tela em duas faixas: a foto nova entra só numa faixa (em cima ou embaixo) por uma batida e, na seguinte, ocupa a tela toda.
- A linha de divisão muda de altura de foto para foto (entre 880 e 1080 px), como no exemplo.
- O nome da marca aparece primeiro "cortado" (no exemplo, "BLK"; aqui, o "s" e o passarinho) antes de aparecer inteiro.

## Decisões criativas
- Abre com um sabiá de verdade (é a capa do vídeo) e alterna pássaro ↔ pessoas trabalhando ↔ artes da marca.
- Em 1,5 s o sabiá de verdade (em cima) encontra o passarinho da marca (embaixo).
- As duas fotos deitadas (sofá e notebook) ficam só como faixa, nunca na tela inteira, para não perderem qualidade.
- Final: logo vertical (IMG_1933) parado por 1,8 s, aproximando 4 % bem devagar.
- Diferente do exemplo, que termina numa foto qualquer: aqui termina no logo, porque é lançamento.

## Medido / olhado
- `check`: 0 erros. 2 avisos `timeline_track_too_dense` (7 fotos por faixa no mesmo arquivo); mantidos de propósito, porque a montagem é uma sequência só e fica mais fácil de editar num lugar.
- Olhei uma imagem por batida (30 quadros) e recortes em tamanho real das 3 fotos menores.
- **Som (2026-11-05):** a pedido do dono, entrou a mesma música do `exemplo.mp4`, começando em 0 s como no exemplo, para os cortes caírem nos mesmos pontos da música. A original tem 7,97 s e acaba cortada. Para cobrir os 9 s, `musica-referencia-9s.wav` repete, a partir de 7,915 s, o trecho que começa um compasso antes (4,705 s; música a 75 batidas/min), com emenda de 40 ms e sumindo aos poucos de 8,4 a 9 s. Medido: as batidas seguem a cada 0,8 s depois da emenda (7,115 → 7,925 → 8,725), o volume médio é igual ao original (−15 dB) e o pico também (−0,8 dB). **Eu não ouvi o som; só medi.**
- **Direitos da música:** é de terceiros. Postada "colada" no vídeo, o Instagram pode silenciar ou bloquear, principalmente em conta comercial. Alternativa segura: postar sem som e escolher a música na biblioteca do Instagram.

## Tratamento de cor (preset "Sabiá dourado"): TESTADO E RETIRADO em 2026-11-05
- **Situação atual: o vídeo está na primeira versão, sem tratamento.** O dono achou que algumas fotos perderam qualidade e pediu a versão anterior de volta. O tratamento foi removido de todas as fotos com `media-treatment --clear`. Os quadros conferidos ficaram idênticos à primeira versão, pixel por pixel.
- Problema que o teste mostrou: a etapa que escurece só os verdes criou manchas quadriculadas no fundo desfocado das fotos pequenas (o pior caso foi o sabiá com musgo). O contraste extra também deixou a compressão das fotos mais visível. Se for tentar de novo: tirar essa etapa dos verdes e usar fotos maiores.
- Tudo abaixo fica só como registro. O `preset-sabia-dourado.json` continua na pasta, e a comparação está em `comparacao\antes-e-depois.jpg`.
- Referência: `brutos\teaser-sabia-lancamento\pre-set.jpeg` (print de post do Itaú). Medido só o recorte da foto, sem a interface do Instagram.
- Visual do preset: escuro (brilho médio 72 de 255), meios-tons laranja, luzes douradas cor de creme, sombras quase pretas puxando para o verde, cor forte, verdes fechados.
- Aplicado nas 11 fotos (classe `tratada`) pelo `hyperframes media-treatment`, guardado no atributo `data-color-grading` de cada `<img>`.
- **Não aplicado** nas 3 artes da marca (04, 08, 14), para não alterar as cores oficiais.
- Ajustes comuns a todas as fotos (cópia em `preset-sabia-dourado.json`): contraste +0,2; luzes −0,15; sombras −0,1; pretos −0,12; temperatura +0,18; vibração +0,15; rodas de cor com sombras verdes (100°), meios laranja (28°) e luzes douradas (38°); verdes escurecidos e puxados para o oliva.
- Ajuste por foto (como no Lightroom, mesmo preset e brilho acertado em cada uma):

  | Foto | Exposição | Contraste |
  |---|---|---|
  | 01 tordo | −0,45 | 0,42 |
  | 02 post-its | −0,25 | 0,20 |
  | 03 galho | −0,45 | 0,35 |
  | 05 escrita | +0,15 | 0,20 |
  | 06 musgo | −0,30 | 0,32 |
  | 07 mãos/notebook | −0,40 | 0,20 |
  | 09 wikipédia | −0,45 | 0,35 |
  | 10 celular | −0,80 (temp. +0,45, vibração +0,3) | 0,20 |
  | 11 sofá | −0,10 | 0,20 |
  | 12 notebook laranja | −0,10 | 0,20 |
  | 13 tronco | −0,45 | 0,38 |

- Conferido: antes/depois lado a lado com o preset, nas 30 batidas e nas entradas pela metade (o corte continua funcionando com o tratamento). Brilho médio das fotos: 74 a 120, antes era de 47 a 209.

## Pontos fracos
- `13-sabia-tronco.jpg` (original de 342 px de largura) e `05-escrita.jpg` (500 px) ficam um pouco moles em tamanho real. No celular, a 0,3–0,6 s, quase não se nota. Se houver versões maiores, é só trocar os arquivos.
- `03-sabia-galho.jpg` tem a assinatura da fotógrafa (Janice Monnerat) no rodapé. Foi mantida.
- Várias fotos parecem vir da internet (Pinterest, Wikipédia, anúncio da MSI). Confirmar o direito de uso antes de postar.

## Entrega (2026-11-05)
- Arquivo: `C:\social-media\prontos\2026-11-05_teaser-sabia-lancamento.mp4`, com qualidade `delivery`, gerado em 29 s.
- Conferido no arquivo: H.264 High, 1080 × 1920, 30 fps, 9,0 s, áudio AAC estéreo 48 kHz. O comando `hyperframes audio` classifica o som como música, presente do início (0 s) ao fim (8,97 s).
- Uma imagem por batida (30) comparada com a prévia da primeira versão: tudo igual (só a diferença normal de compressão). Sem tratamento de cor, com a música da referência estendida para 9 s.
