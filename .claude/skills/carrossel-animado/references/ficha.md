# Modelo da ficha do carrossel

A ficha junta as quatro decisões num lugar só. Salve como `ficha.md` na pasta do carrossel. É ela que o dono aprova antes de qualquer render, e é ela que vira modelo depois.

```markdown
# FICHA DO CARROSSEL · [nome curto]

## 1. Tema e objetivo
Tema: [do que fala, em uma frase]
Para quem: [público, com o problema dele]
Ação no fim: [salvar / mandar para alguém / comentar uma palavra]
Estrutura: [Erros / Passo a passo / Mito × verdade / ...]

## 2. Slides (texto · verbo do movimento)
01 Capa: "[título, com a palavra-chave entre *asteriscos*]" / "[apoio]" · [VERBO]: [o que se mexe, em uma frase]
02: "[título]" / "[apoio]" · [VERBO]: [...]
...
NN: "[ação]" · APONTAR: [seta para o ícone de salvar/enviar]

## 3. Ritmo e som
8 s por slide, 30 fps. Título inteiro no quadro 0. O movimento de cada slide começa depois do tempo de leitura (`leitura()`), dura de 1 a 3 s e o resultado fica parado pelo menos 1,5 s. De 7,0 a ~7,8 s tudo volta (loop sem pulo).
Sons: whoosh + batida no título, clique em passos e números, pop em ícones, risco em caneta, whoosh ao contrário no retorno.
Trilha: [arquivo em remotion\public\ e BPM, ou "sem trilha"]. Tem que funcionar no mudo.

## 4. Identidade
Sabiá Lab, tema [escuro / claro / laranja] (veja references/identidade.md).
Sementes: [em qual slide, ou "sem sementes"].
Referência: [arquivo ou "nenhuma"]. Aproveitar: [ritmo, título, entradas]. Não copiar: textos, marca, fotos.
Fotos: [arquivos em remotion\public\carrossel\fotos\ ou "sem fotos"].

## 5. Formato
1080 × 1350 (4:5), um MP4 por slide (H.264 com áudio) e um PNG do primeiro quadro de cada um, em prontos\AAAA-MM-DD_nome\ (01.mp4, 01.png..., legenda.txt).
```

## Exemplo preenchido (negócio fictício)

```markdown
# FICHA DO CARROSSEL · orçamento-de-reforma

## 1. Tema e objetivo
Tema: onde o orçamento de reforma estoura (e como prever).
Para quem: quem vai reformar apartamento pela primeira vez.
Ação no fim: salvar e mandar para quem vai reformar junto.
Estrutura: Erros.

## 2. Slides
01 Capa: "Seu orçamento de reforma *estoura* no mesmo lugar." / "E não é na mão de obra." · APONTAR: barra do orçamento enchendo e passando do limite, círculo à mão no ponto em que passa.
02: "O que ninguém põe na planilha." / "Os custos que só aparecem com a obra aberta." · REVELAR: três itens entrando um por batida.
03: "Erro 1: orçar só o acabamento." / "A infraestrutura vem antes." · TRANSFORMAR: "piso e pintura" riscado vira "elétrica, hidráulica, piso e pintura".
04: "Erro 2: sem reserva." / "Separe 15% para o imprevisto." · CONTAR: barra de 0 a 15% com o número subindo.
05: "Erro 3: comprar tudo de uma vez." / "Compre por etapa da obra." · COMPARAR: tudo de uma vez × por etapa.
06: "Salve para a sua obra." / "E mande para quem vai reformar com você." · APONTAR: seta para os ícones de salvar e enviar.

## 3. Ritmo e som
(padrão) · Trilha: sem trilha.

## 4. Identidade
(Exemplo de outro negócio, só para mostrar o preenchimento. Na Sabiá, esta seção é só o tema.)
Sabiá Lab, tema claro. Sementes: só na capa.
Referência: nenhuma. Fotos: sem fotos.

## 5. Formato
(padrão)
```

O "15%" do exemplo é uma faixa de reserva comum em guias de obra, apresentada como recomendação. No carrossel de verdade, número de dado vem do dono ou de fonte confirmada; se não tiver, vire recomendação ("separe uma reserva") ou marque [CONFIRMAR].
