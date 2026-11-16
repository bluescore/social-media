# Ep. 01 — revisão v3 (pedido do dono, 12/11/2026)

A v2 (64 s, `renders/ep01-completo-v2.mp4`) foi aprovada no geral. O dono pediu 12 correções e foi claro:
**mude SÓ o que foi pedido; o resto fica idêntico** (o que já está aprovado não pode mudar sem motivo).

## Os 12 pedidos e onde cada um é feito

| # | Pedido do dono | Onde | Quem |
|---|---|---|---|
| 1-3 | legenda + lettering; tudo o que a locução diz aparece na tela | `compositions/legendas.html` (gerado por `fonte/scripts/gerar-legendas.py`) + lettering dentro de s04b, s11, s12 | agente de legendas |
| 4 | tirar "na cadeira, ela explica de cor" e destacar o que é dito | s01 (FEITO) | sessão principal |
| 5 | locução no feed parado há 47 dias | fala nova F em s04 | áudio |
| 6 | momento de virada antes da 15ª: "mas isso está prestes a mudar…" | cena NOVA `s04b-take15.html` + fala nova T | agente s04b + áudio |
| 7 | ícone e nome do Claude no chat (0:21) | s05 (FEITO) | sessão principal |
| 8 | dados de crescimento do perfil + feed com mais posts | s09 (estendida de 3,5 para 6,8 s) | agente s09 |
| 9 | Lúcia: "Nossa, ficou muito profissional!" | s10 (FEITO) | sessão principal |
| 10 | a boneca não anda: fica parada no consultório | s11 (pose nova parada) | agente s11/s12 |
| 11 | fechamento mais comercial (mantém "o roteiro ela já tinha") | s11: lettering + falas 12-13 | agente s11/s12 + áudio |
| 12 | trocar a chamada do próximo ep. por CTA "comente CLÍNICA" | s12 + fala 14 | agente s11/s12 + áudio |

Também saiu de s05 a legenda "sem gravar de novo" (não é dita; ela batia com a legenda de "mandou só o roteiro").

## Linha do tempo v3 (segundos do episódio, 30 q/s, total 71,7 s) — já está em `index.html`

| cena | início | duração | fim | mudou? |
|---|---|---|---|---|
| s01-maquete | 0 | 9,3 | 9,3 | só tirou a legenda |
| s03-folha | 9,2 | 6,1 | 15,3 | não |
| s04-perfil | 15,3 | 3,0 | 18,3 | não (só ganha a fala F) |
| **s04b-take15 (NOVA)** | 18,3 | 3,3 | 21,6 | nova |
| s05-foto | 21,6 | 4,3 | 25,9 | +3,3 s; Claude no topo; sem "sem gravar de novo" |
| virada | 25,9 | 8,8333 | 34,7333 | +3,3 s; IMPACTO em **33,9333** (quadro 1018) |
| s08-video-dela | 34,7333 | 11,9667 | 46,7 | +3,3 s |
| s09-post | 46,7 | **6,8** | 53,5 | +3,3 s e estendida (0-3,4 igual; 3,4-6,8 novo) |
| s10-turma | 53,5 | 5,0 | 58,5 | +6,6 s; texto da Lúcia |
| s11-tarde | 58,5 | **9,0** | 67,5 | +6,6 s; refeita (parada + fechamento) |
| s12-cartao | 66,9 | **4,8** | 71,7 | refeita (CTA) |
| legendas | 0 | 71,7 | 71,7 | nova, por cima de tudo (z-index 20) |
| som | `assets/audio/mix-v3.wav` | 71,7 | | novo (por enquanto é um provisório) |

## Locução v3 (A.Medeiros, eleven_v4) — onde cada fala começa

Tomada antiga: `assets/audio/fontes/narracao-amedeiros-v4-a.mp3` (aprovada). Tomadas novas (só as falas novas, mesmo nó/voz/ajustes):
`narracao-v3-novas-a.mp3`, `-b.mp3`, `-c.mp3` (texto: F, T, "o roteiro ela já tinha.", 12, 13, 14; ~15,5 s cada).

| id | texto | começa em (ep.) | fonte | dur. aprox. |
|---|---|---|---|---|
| 1 | décima quarta tentativa. | 0,10 | antiga | 1,97 |
| 2 | e o vídeo não sai. | 2,32 | antiga | 1,06 |
| 3 | a doutora Helena explica a prótese protocolo toda semana, paciente por paciente. | 3,95 | antiga | 4,83 |
| 4 | o roteiro sobre implantes está pronto há seis semanas. | 9,45 | antiga | 2,95 |
| 5 | a gravação, não. | 12,95 | antiga | 1,16 |
| **F** | quarenta e sete dias sem postar nada. | **15,55** | nova | ~2,1 |
| **T** | mas isso está prestes a mudar... | **18,60** | nova | ~2,5 (com a pausa depois de "mas") |
| 6 | ela não gravou a décima quinta. | 21,90 | antiga | 1,84 |
| 7 | mandou só o roteiro. | 24,20 | antiga | 1,27 |
| 8 | cada linha que ela escreveu virou uma cena. | 26,90 (virada + 1,0, como no corte aprovado) | antiga | 2,30 |
| 9 | o perfil voltou a andar. | 47,00 | antiga | 1,32 |
| 10 | ela mandou o vídeo pra turma. | 53,80 | antiga | 1,26 |
| 11 | o roteiro ela já tinha. | 58,90 | **antiga** (aprovada) | 1,07 |
| **12** | faltava tirar do papel. | **60,40** | nova | ~1,15 |
| **13** | se você explica isso todo dia no consultório, o seu também já existe. | **62,10** | nova | ~4,3 (pausa na vírgula) |
| **14** | comente clínica e a gente te mostra como. | **67,65** (s12 + 0,75) | nova | ~2,4 |

Saiu: "no próximo episódio: o que a recepção mais ouve."
Os tempos reais (por palavra) saem do áudio em `assets/audio/voz-v3.palavras.json` (feito pelo agente de áudio).

## Eventos planejados nas cenas novas (o áudio usa estes tempos; as cenas DEVEM seguir)

- s04b (18,3): 0,00 corte (luz 40% mais escura por 3 quadros, como s04) · 0,30 "mas" · ~0,95-2,75 "isso está prestes a mudar…" · 2,85-3,05 a tela do celular apaga (ela não grava) · 3,30 corte para s05.
- s09 (46,7): 0-3,4 igual à v2 · 3,40-4,60 a câmera avança de novo para o celular · 3,50 a etiqueta troca para "**3 semanas** depois" · 3,60 / 3,82 / 4,04 / 4,26 / 4,48 entram 5 posts novos (um "tique" cada) · 4,80 etiqueta "+438 seguidores" (conta 0→438 em 1,0 s) · 5,10 etiqueta "21,3 mil visualizações" (conta em 1,0 s) · parado até 6,8.
- s11 (58,5): parada, sem passos nem porta · 0,40 "o roteiro ela já tinha" · 1,90 "faltava tirar do papel" · 3,60 "se você explica isso todo dia no consultório," · ~6,0 "o seu também já existe" · s12 entra por cima em 8,4 (66,9).
- s12 (66,9): 0-0,6 o cartão desce (máscara) · 0,75 "comente" · ~1,3 a pílula "CLÍNICA" salta · ~1,8 "e a gente te mostra como" · parado até 4,8.

## Regras para todo mundo

- Projeto: `C:\social-media\hyperframes\clinicas-ep01-protocolo-implante`. CLI fixa: `npx --yes hyperframes@0.8.216 check` / `snapshot --at 1,2,3`. Antes de editar qualquer composição, carregue a skill `hyperframes:hyperframes`.
- Cada agente mexe SÓ nos seus arquivos (lista no seu pedido). O `check` roda no projeto inteiro: erros em arquivos de outro agente não são seus.
- Marca (Sabiá Lab): Helvetica Now Text (`assets/fonts/`), minúsculas (nomes próprios e "CLÍNICA" à parte), letter-spacing -0,05em, entrelinha 0,9, **Bold** para destaque, sem Megion, sem ponto final no texto da tela. Laranja #F34500 é só da "inteligência" (o fio). Lima #EFFF57 = destaque/selo. Chumbo #303236. Branco quente #f6f4f1.
- Área segura do texto: y 168-1330, x 108-972. Nada de texto sobre texto.
- GSAP: nunca CSS transform em elemento que o GSAP move (estado inicial com `tl.set`); tudo determinístico; nada de `Date.now`/`Math.random`.
- Personagem (dra. Helena, boneca de madeira estilo A): faixa grisalha na têmpora DIREITA dela, relógio no pulso ESQUERDO, jaleco branco com lapela, calça escura. Ficha: `fonte/geradas/folha-A-final.png`.
- CFO 196/2019 (vídeo/posts dela): sem procedimento acontecendo, sem promessa, sem preço, sem antes/depois, nome fictício + CRO-UF 00000.
- Imagens de IA: só `node C:\social-media\ferramentas\openai\gerar-imagem.mjs` (instruções em `ferramentas\openai\LEIA-ME.md`). Voz/áudio: só ElevenLabs.
- Comentários e textos de apoio em português simples.
