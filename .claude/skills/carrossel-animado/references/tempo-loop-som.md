# Tempo, loop e som

No Reels, você manda no tempo. **No carrossel, quem manda é o dedo da pessoa.** Ela pode arrastar no primeiro segundo ou ficar parada olhando. Tudo aqui sai disso.

## As três regras do tempo

1. **A mensagem principal está legível no primeiro segundo.** O título nasce inteiro no quadro 0. Quem arrasta rápido leva a ideia mesmo assim. (O PNG do quadro 0 é a "versão parada" do slide: ele tem que funcionar sozinho. Por isso o "antes" já está na tela no quadro 0: a frase que vai ser riscada, os itens apagados, o gráfico em fantasma.)
2. **O movimento chega quando o olho chega.** Primeiro a pessoa lê o título; só então acontece o movimento, no lugar para onde ela está olhando, e ele demonstra a ideia que ela acabou de ler. Movimento que começa antes da leitura atropela o texto; movimento que não explica nada é enfeite.
3. **O slide fecha em loop.** O último quadro é IGUAL ao primeiro. Quem fica parado nem percebe onde ele recomeça.

## A linha do tempo de um slide (8 s, 240 quadros)

Lição do carrossel modelo (cliente-whatsapp, 2026-11-09): a primeira versão, com 6 s e detalhes a partir de 0,5 s, foi rejeitada pelo dono. Estava rápida demais ("não dá tempo de ler, quando vê já tem a interação"), tinha texto demais e repetia o mesmo truque em vários slides. A linha do tempo agora parte do **tempo de leitura**, não de um número fixo.

| Tempo | O que acontece |
|---|---|
| 0 s | Título inteiro, cartão, fundo. Tudo parado e sem som: a pessoa está lendo. |
| até `leitura(...)` | Ninguém se mexe enquanto o olho lê o título (e o que ele precisa ler antes do movimento). Um detalhe pequeno é permitido só onde o olho já está (ex.: a caneta que sublinha o trecho-chave no fim da leitura do título). |
| leitura → +1 a 3 s | **O acontecimento**: UM movimento grande, no lugar para onde o olho vai em seguida, que demonstra a ideia do título. |
| depois dele, ≥ 1,5 a 2 s | O resultado fica parado e completo: tempo de ler o que mudou. |
| 7,0 a ~7,8 s | **Retorno**: tudo volta ao estado do quadro 0. Whoosh ao contrário. |
| até 8 s | Parado, idêntico ao quadro 0. |

`leitura(texto, aPartirDe)` (em `tempo.ts`) dá o segundo em que a pessoa termina de ler: ~4 palavras por segundo + 0,3 s para o olho chegar. Some os textos que ela lê antes do movimento (rótulo + título + o balão que importa). `naGrade(seg)` arredonda para 0,25 s.
`SEGUNDOS = 8` em `tempo.ts` vale para todos os carrosséis; `VOLTA` (o retorno) é sempre o último segundo. Todos os slides do carrossel têm a mesma duração.

### Movimento que impressiona (e não atrapalha)

- **Um mecanismo por slide, e nenhum repetido no carrossel.** Exemplos do modelo: odômetro que acelera e trava (contar), gaveta que se abre e mostra o tempo perdido (revelar), câmera que mergulha num detalhe e volta com outra cena (transformar), grade em que tudo afunda menos um (comparar), lista que reordena (transformar), "digitando" que vira painel (revelar), palavra que voa até o destino (apontar).
- **Pouco texto**: ~20 palavras visíveis por slide ou menos. Frase de apoio que não cabe vai para a legenda do post.
- **O movimento é a explicação**: se dá para tirá-lo e o slide diz a mesma coisa, ele é enfeite.
- **Curvas com peso**: entra rápido e assenta devagar; nada de mola em tudo. Velocidade de leitura quando o movimento revela texto (máscara que acompanha o olho).
- **Repouso real**: depois do acontecimento, a imagem fica parada (pixel a pixel) por pelo menos 1,5 s.
- **Sem marrom**: escuro → laranja nunca por mistura de cor nem por duas camadas semitransparentes (passa por marrom). Troca seca num quadro (de preferência no clique) ou máscara/escala nítida mostrando a versão nova por cima.
- **Texto que importa entra já nítido**, nunca desfocado no meio do movimento. Texto que muda e precisa ser lido no celular: ≥ ~36 px.
- **Retorno discreto**: nada de números rodando para trás ou valores intermediários; o estado final some e o inicial reaparece. `whoosh_rev` baixo (−14 dB) quando há frase no pé.

## O gancho para o próximo slide (pedido do dono, 2026-11-11)

Sem um sinal de continuação, "parece que só tem aquele slide e não dá interesse de passar". Não precisa estar em todos: entra onde a pessoa terminou de ver o resultado e pode perder o interesse.
- **Fio que atravessa** (capa → 02): um elemento sai pela borda direita numa altura Y e o slide seguinte começa com ele entrando pela borda esquerda na mesma altura. Ao arrastar, um continua no outro.
- **Espiadinha** (slides do meio): depois do resultado (~5,3 s), o objeto do próximo slide entra num círculo cortado pela borda direita, com o objeto inteiro na metade visível, e dá um toque para a esquerda. Sempre o mesmo som curto (`espia`): vira a assinatura de "tem mais". Junto com a frase do pé (Puxa), que abre uma curiosidade.
- O que passa da borda de propósito vai no `fundo` da Moldura (fica fora do teste de margem).
- Peças prontas em `remotion\src\carrosseis\2026-11-11_paciencia\comum.tsx` (`Espia`, `FIO_Y`).

## Menos silêncio no começo (pedido do dono, 2026-11-11)

Ajuste final do dono (mesmo dia): com o início em ~1 s "ficou um pouco curto". **A animação começa depois do tempo de ler o TÍTULO PRINCIPAL** (`leitura(título)`: 0,3 s + 4 palavras/s, ~1,3 a 2,1 s), não do título + apoio + cartão. Não espere a leitura de tudo, mas dê esse respiro. O acontecimento grande segue logo depois e o resultado ainda fica parado ≥ 1,5 s.

## Como garantir o loop

- Tudo que entra usa `presenca(...)`, `mola(...)` ou `volta(...)`: eles já voltam a zero a partir de `VOLTA` (7 s).
- Movimento contínuo usa `ciclo(f, voltas)` ou `onda(f, voltas)` com **voltas inteiras**: no quadro 0 e no último dão o mesmo valor.
- Nunca use `Math.random()`. Use `rnd(n)`: o mesmo número sempre.
- Nada de animação CSS (`transition`, `@keyframes`): o Remotion só enxerga o quadro atual.
- O `npm run carrossel:conferir` compara o quadro 0 com o último. Tem que dar **0 pixel diferente**. Se der pulo, procure o elemento que não usa `presenca`/`volta`, ou um ciclo com voltas quebradas.

## O som

Muita gente vê o feed no mudo. **O carrossel funciona sem som; o som é o bônus de quem está ouvindo, nunca a explicação.**

Regra simples: **cada acontecimento ganha um som, no quadro em que ele acontece.** Nada de som no quadro 0 (a pessoa está lendo; e o som em t = 0 se repete a cada volta do loop).

| Momento | Efeito (`remotion\public\carrossel\sfx\`) | Volume típico (dB) |
|---|---|---|
| Item de lista / passo / dígito | `clique` | −9 a −15 (mais baixo se forem muitos seguidos) |
| Marca importante do contador, "virada" | `clique_forte` (+ `batida` baixa) | −2 e −10 |
| Ícone, selo, rótulo que chega com mola | `pop` | −3 a −6 |
| Risco de caneta, círculo à mão, seta | `risco` | −4 a −8 |
| Pó, areia, partículas caindo | `po` | −3 a −10 |
| Movimento grande (gaveta, mergulho, voo) | `whoosh` | −8 a −12 |
| Retorno do loop (7 s) | `whoosh_rev` | −9 a −14 |

- Os efeitos de cada slide ficam no `sons.json` da pasta do carrossel, com o segundo exato (`t`). Ponha o `t` no mesmo segundo em que o movimento começa no código.
- Muitos cliques seguidos (contador): baixe o volume (−12 a −15) e espace pelo menos 0,1 s.
- O dono pode trazer efeitos próprios: coloque em `remotion\public\carrossel\sfx\` e use o nome do arquivo: WAV sem extensão (`"s": "pop"`), MP3 com extensão (`"s": "meu.mp3"`).

## A trilha (opcional)

- Uma música baixinha, com batida marcada, que o dono **tenha direito de usar** (biblioteca paga, música própria, banco gratuito com licença). Nunca baixe música de terceiros.
- Configure no `index.ts` do carrossel, em `trilha: { ... }`: `arquivo` (caminho dentro de `remotion\public\`, ex.: `marca/musicas/trilha.mp3`; a pasta `marca\musicas\` ainda está vazia), `inicio` (segundo da música onde começa o slide 1), `passo` (8 = cada slide pega os 8 s seguintes da música) e `ganho` (−14 a −9 dB, por baixo dos efeitos).
- Escolha um `inicio` numa batida forte, depois da introdução, num trecho sem voz.
- O molde mistura a "cauda" dos 0,5 s seguintes no começo de cada slide: quando o vídeo recomeça, a música continua sem emenda.
- **Andamento**: a grade de 0,5 s do molde casa com música de 120 BPM. Se o dono souber o BPM da música, troque `BATIDA` em `remotion\src\carrossel\tempo.ts` (vale para todos os carrosséis) para `60 / BPM` e use `batida(n)` para posicionar as entradas. Se não souber, mantenha 0,5 s: fica bom com a maioria das trilhas de 115 a 125 BPM.

## Exemplo de sons de um slide (a capa do modelo: caneta + odômetro que trava em 5h38)

```json
"01": [
  { "t": 1.55, "s": "risco", "g": -6 },
  { "t": 2.4, "s": "clique", "g": -16 },
  { "t": 2.8, "s": "clique", "g": -16 },
  { "t": 3.33, "s": "whoosh", "g": -12 },
  { "t": 3.67, "s": "clique", "g": -13 },
  { "t": 4.0, "s": "clique", "g": -12 },
  { "t": 4.33, "s": "clique", "g": -11 },
  { "t": 5.2, "s": "clique_forte", "g": -2 },
  { "t": 5.2, "s": "batida", "g": -10 },
  { "t": 7.0, "s": "whoosh_rev", "g": -9 }
]
```
