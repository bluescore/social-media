# Movimentos: os 5 verbos

Se o movimento só enfeita, ele atrapalha. **Todo movimento tem um verbo.** Antes de animar um slide, escolha o verbo dele. Um verbo por slide basta (dois, no máximo, se um for só o "apontar" final).

| Verbo | Para quê | Peças prontas no molde |
|---|---|---|
| **Revelar** | a informação aparece na hora em que importa | `Revela`, `Lista` |
| **Contar** | um número muda na frente da pessoa | `Contador`, `Barra`, `Anel` |
| **Comparar** | antes × depois, errado × certo, lado a lado | `Comparar`, `Cortina` |
| **Transformar** | uma coisa vira outra | `Riscar`, `Troca`, `Decodificar` |
| **Apontar** | leva o olho para o detalhe | `Seta`, `CirculoMao`, `Holofote`, `Pulso`, `Marca` |

As peças são ponto de partida. Quando o slide pede algo que não existe (um gráfico de linha, um mapa, um ícone que se monta), construa no próprio slide seguindo as mesmas regras de tempo e loop.

## Revelar

Quando usar: listas, passos, a resposta depois da pergunta, o detalhe que completa o título.

Jeitos:
- **sobe**: sobe 40 px e acende. O neutro, serve para quase tudo.
- **máscara**: o elemento é "desenhado" da esquerda para a direita. Linhas do tempo, barras, frases de destaque.
- **escala**: cresce com mola. Ícones, selos, números isolados. Não use em blocos de texto.
- **desfoque**: sai do borrado. "O segredo é...", respostas.
- **aparece**: só acende. Quando qualquer deslocamento atrapalharia a leitura.

Ritmo: um item por batida (a cada 0,5 ou 1 s). Lista com mais de 4 itens: 0,5 s entre eles.

## Contar

Quando usar: dado, porcentagem, tempo, quantidade, "de X para Y".
- A contagem é curta: 0,8 a 1,5 s, desacelerando no fim (a curva SAI), e termina com um pulso pequeno e um clique.
- O número final é o que importa: deixe-o parado pelo menos 1,5 s antes do retorno.
- Dígitos com largura fixa (o molde já faz), senão o número treme.
- Só números reais. Número ilustrativo leva a palavra "ilustrativo" no slide.
- Variações: barra que enche (proporção), anel de porcentagem, régua com marcas (0 → 1 s → 3 s), ponteiro.

## Comparar

Quando usar: antes × depois, errado × certo, caro × barato, lento × rápido.
- As duas coisas ficam visíveis ao mesmo tempo. Comparar é ver junto, não em sequência.
- O "vencedor" entra por último e ganha a cor de destaque (borda, selo de certo). O perdedor apaga um pouco e ganha um X discreto.
- Mesmo tamanho, mesma posição relativa, mesma escala. Senão é truque.
- Com fotos (pele, ambiente, design, edição): `Cortina`, a divisória que corre e revela o depois.

## Transformar

Quando usar: o erro que vira a solução, a frase fraca que vira a forte, o rascunho que vira o pronto.
- A pessoa precisa ver o "antes" por pelo menos 0,5 s antes de ele mudar.
- Sequência clássica: aparece → é riscado (caneta, com som de risco) → sai para cima → o novo entra com mola.
- Decodificar (letras embaralhando até acertar) funciona para frases curtas e tom tecnológico. Até ~30 letras.
- Outras transformações: forma que vira outra (quadrado vira gráfico), lista bagunçada que se organiza, cor que muda de "errado" para "certo".

## Apontar

Quando usar: o detalhe que a pessoa não pode perder, o ícone de salvar no último slide, o ponto da queda num gráfico.
- Aponte UMA coisa por slide, e só depois que ela já está na tela.
- Seta curva > seta reta (parece feita à mão, chama mais atenção).
- Círculo à mão: a ponta passa um pouco do começo, como caneta de verdade.
- Holofote: escurece o resto. Bom para prints e telas cheias.
- Pulso: anéis saindo de um ponto. Bom para "toque aqui".
- `Marca`: barra que se desenha embaixo da palavra-chave do título (o "apontar" mais leve, serve em qualquer slide).

## Movimento contínuo (o "respiro")

Para o slide não ficar morto depois que tudo entrou: algo pequeno se mexe sem parar, e fecha o loop sozinho.
- Foto que aproxima devagar (`Foto`, zoom de 3 a 6%).
- Objeto que flutua 10 a 20 px (`Flutua`) ou balança alguns graus (`Gira` com `balanco`).
- Partículas discretas: pó, vapor, poeira de luz (`Particulas`).
- A seta do "arraste" no rodapé (já vem na moldura).
Um respiro por slide. Sutil: se a pessoa percebe o respiro antes do conteúdo, está forte demais.

## Camadas com foto (o teto)

Para produto, comida, ambiente e moda: foto de estúdio (feita ou gerada por IA) + movimento por código.
- A foto dá o acabamento. O código dá o movimento e o tempo exato.
- Separe em camadas: fundo, objeto recortado (PNG sem fundo), partículas, texto. Cada camada se mexe numa velocidade diferente (profundidade).
- Peça as fotos já no formato 4:5, sem texto, com espaço livre no topo para o título.
- Degradê de leitura (`leitura="topo"` na `Foto`) quando o título fica em cima da imagem.
- Recorte: se o dono tiver uma ferramenta de remover fundo, use. Se não, prefira fotos com fundo liso da cor do fundo do slide.

## Curvas e tempos

- **Entrada**: rápida e assentando devagar (curva SAI, 0,35 a 0,5 s). É o padrão de quase tudo.
- **Mola**: para coisas pequenas que "chegam" (selos, ícones, rótulos). Com um leve passar do ponto, nunca quicando três vezes.
- **Linear**: só para coisas que medem tempo (curva de gráfico desenhando, barra de progresso de verdade).
- **Saída** (retorno do loop): curva MEIO, 0,4 a 0,5 s, em ordem inversa da entrada.
- Escalonar (stagger): itens irmãos entram com 3 a 6 quadros de diferença, nunca todos juntos.

## O que nunca fazer

- Tudo se mexendo ao mesmo tempo.
- Título entrando letra por letra ou palavra por palavra na capa (quem arrasta rápido não lê).
- Degradê colorido com brilho, partículas brilhantes por toda parte, lens flare: é a cara do padrão de IA.
- Quicar (bounce) exagerado, girar 360° sem motivo, zoom brusco, tremer a tela.
- Transição "de slide para slide" dentro do vídeo: quem troca de slide é o dedo da pessoa.
- Movimento que esconde o texto enquanto a pessoa lê.
- Texto em movimento contínuo (texto lê-se parado).
