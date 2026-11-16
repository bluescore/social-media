# Ep. 01 — revisão v4 (2º pedido do dono, 12/11/2026)

A v3 (71,7 s, `renders/ep01-completo-v3.mp4`) é a base. A linha do tempo, as regras e a marca seguem `fonte/PLANO-v3.md`.
O dono pediu mais 10 ajustes. A regra dele continua: **mude SÓ o que foi pedido; o resto fica idêntico.**
A duração (71,7 s) e os tempos de todas as cenas NÃO mudam.

## Os 10 pedidos e onde cada um é feito

| # | Pedido do dono (palavras dele) | O que fazer | Arquivos | Quem |
|---|---|---|---|---|
| 1 | "centralizar a legenda e trabalhar com ela em uma única linha" | toda LEGENDA (faixa de legendas) vira uma linha só, centralizada no quadro; falas longas viram vários pedaços de 1 linha | `fonte/scripts/gerar-legendas.py` → `compositions/legendas.html` | legendas |
| 2 | "priorizar trabalhar com os números em numeral (ex: 14ª)" | na tela: "14ª tentativa", "há 6 semanas", "17 dias", "a 15ª" (a voz continua falando por extenso) | legendas | legendas |
| 3 | "quando mostrar o perfil 3 semanas depois, os posts no perfil devem ser diferentes do 1º vídeo" | as 5 capas novas de s09 (hoje são quadros do vídeo dela) viram imagens novas e variadas | `assets/img/post-novo-1..5.jpg`, `compositions/s09-post.html` (só se precisar) | s09 |
| 4 | "ao invés de 47 dias sem postar, usar 17 dias" | fala F nova: "dezessete dias sem postar nada." + rótulo de s04 "há 17 dias" + legenda "17 dias sem postar nada" | áudio, `s04-perfil.html`, legendas | áudio, s10/s04/s12, legendas |
| 5 | "remover textos 'rascunho, frases em revisão' e 'ilustração educativa... apoio de IA' (vídeo implante)" | sai `#aviso` e `#selo` em s08 E na virada (mesmos ids); o nome "dra. Helena Prado · cirurgiã-dentista · CRO-UF 00000" fica | `s08-video-dela.html`, `virada.html` | s08 |
| 6 | "remover 'sala de espera / ep 01' e substituir pelo logo da Sabiá apenas (chamada final)" | s12: sai o ícone e "sala de espera · ep. 01"; entra só o logo Sabiá (branco, sem LAB: `assets/marca/logo/sabia_branco.png`) | `s12-cartao.html` | s10/s04/s12 |
| 7 | "remover 'personagens... apoio de IA' (chamada final)" | s12: sai o aviso | `s12-cartao.html` | s10/s04/s12 |
| 8 | "o implante na cena 'presa sobre implantes' está muito próximo da borda, diminuir um pouco" | s08: diminuir o objeto 3D (passo 2 e coerente nos outros) | `s08-video-dela.html` | s08 |
| 9 | "no chat do grupo de especialização, substituir o grupo pelo contato da Lúcia, e mostrar as mensagens anteriores como 'Como que funciona a prótese?' algo assim... e após receber o vídeo 'Entendi!' algo assim" | s10: conversa 1 a 1 com "Lúcia" (paciente); antes: "Oi, doutora! Tudo bem?" / "Como funciona a prótese protocolo?"; depois do vídeo: "Entendi! Agora ficou bem claro." A fala 10 muda para "ela mandou o vídeo pra Lúcia." | `s10-turma.html`, áudio, legendas | s10/s04/s12, áudio, legendas |
| 10 | "no vídeo do implante, como vai sobrar um espaço abaixo, pensei em colocarmos uma tela representando a dra. Helena, como se ela estivesse aparecendo em tela dividida explicando, e não só o texto" | s08: tela dividida — em cima o conteúdo 3D (menor), embaixo a Helena (boneca de madeira) explicando com gestos, sem sincronia de boca | `s08-video-dela.html`, imagens novas da Helena, `assets/img/video-dela-final.jpg` (refeito do último quadro novo de s08) | s08 |

## Falas novas (já geradas, A.Medeiros eleven_v4, nó 0PmQSBQPgxTnuxxBlpSh do fluxo MHFvq3M3aRWH1DU1Bimq)

`assets/audio/fontes/narracao-v4-novas-a.mp3`, `-b.mp3`, `-c.mp3` (3 tomadas, 62 créditos cada; gerações a=4VYDeUD0SeigbwRRnLkY, b=bAZ9HX1NUcvyV0WkUOGe, c=CoGtbiWFPn7Lz77q71rG). Texto: "dezessete dias sem postar nada." / "ela mandou o vídeo pra Lúcia." (~2,1 s e ~1,4 s).

| id | texto novo | começa em (ep.) |
|---|---|---|
| F | dezessete dias sem postar nada. | 15,55 (igual) |
| 10 | ela mandou o vídeo pra Lúcia. | 53,80 (igual) |

Todas as outras falas ficam exatamente como na v3.

## O que NÃO muda

Duração 71,7 s; tempos das cenas; s01, s03, s04b, s05, s11 (só os números do bloco TEMPOS podem ser ressincronizados); a música e os efeitos (só a voz de F e de 10 muda); o lettering (letras grandes) de 1, 5, T, 11-14 continua no estilo da v3 (alinhado à esquerda) — o pedido 1 é sobre a LEGENDA.
Os eventos de s10 ficam nos mesmos tempos (o som depende deles): vídeo entra 0,40 · "encaminhado" 0,65 · digitando 1,40-2,00 · resposta 2,00 (locais; s10 começa em 53,5).
