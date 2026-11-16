# SPEC — teaser "Esqueça o azul"

GOAL:    quem segue a Blue Score sente que algo grande vem aí e quer saber o nome novo (palpites nos comentários).
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, MP4 H.264.
TIME:    16,8 s x 30 = 504 quadros. Sem música; o relógio é a imagem.
LOOK:    fundos chapados, um por mundo: azul Blue Score #0D79FF → laranja #F34500 → escuro #1E1415 → lima #EFFF57 → escuro #1E1415.
         Títulos: Megion Bold 140–220 px, entrelinha 0,95, alinhados à esquerda em x = 80 ou centralizados (alternando).
         Texto de apoio: Helvetica Now Text Regular 44 px.
         Destaque (acento): uma palavra ou um objeto por cena (o risco laranja, "além" em branco, a palavra do caça-palavra em laranja).
         Textura: só as sementes da marca. Sem brilho, sem partículas, sem degradê.
OBJECTS: logo antigo da Blue Score (arquivo real, em branco); gráfico de barras de BI (5 barras chapadas brancas sobre linha de base);
         tarja de censura lima; passarinho chapado preto gigante (só cabeça e peito); cinco traços laranja = cinco letras escondidas.
MOTION:  chegadas expo.out (longas no fim); inundações de cor power2.inOut 0,6 s; saídas power3.in 0,25 s; chicote com desfoque 20 px.
         Palavras: desfoque 6 px → 0 em 0,13 s, 0,067 s entre elas. Desfoque de movimento ligado no vídeo todo.
SAFE:    todo texto entre y = 168 e y = 1330 (fora da interface do Instagram); nada de texto à direita abaixo de y = 900.

SHOTS:
| Cena | Tempo | Movimento principal | O que se lê | Som | Passa para a próxima |
|---|---|---|---|---|---|
| 1 esqueça | 0,0–2,4 | faixa laranja risca "azul." em 1,1 s | Esqueça o azul. | chicote curto no risco | palavras saem desfocando; o fundo azul fica |
| 2 dados | 2,4–5,2 | 5 barras sobem; a maior fica laranja | Começamos com dados. | chicote longo na inundação | a barra laranja cresce até virar a tela toda |
| 3 além | 5,2–7,8 | linhas entram desfocando; sementes menta abrem | Crescemos além deles. | começa o riser (som crescente) | tudo sobe num chicote vertical |
| 4 inteligência | 7,8–10,6 | caça-palavra gira e uma tarja lima censura a palavra | Inteligência que ███ | tiques + impacto na tarja | a tarja cresce até virar a tela toda (lima) |
| 5 voz | 10,6–13,6 | passarinho gigante entra num chicote da direita | Uma nova voz vai cantar. | 2 pios | círculo escuro abre a partir da ponta do bico |
| 6 em breve | 13,6–16,8 | logo antigo riscado; 5 traços surgem; "Em breve." bate | Em breve. / Ative as notificações | tiques nos traços, impacto no "Em breve." | fim (segura 2 s) |

BANNED: fundo escuro vazio com coisas pequenas no meio; brilho, partículas, degradê azul/roxo; tudo centralizado; tudo surgindo
         com fade + subida; títulos que continuam se mexendo depois de pousar; logo no canto; **o logo e o nome novos (sabiá)**.
QA:      0,0 s (capa: azul + frase legível); 1,3 s (risco completo); 4,9 s (barra virando tela); 6,6 s (três linhas + sementes);
         9,3 s (tarja cobrindo a palavra); 11,6 s (pássaro + frase); 13,45 s (círculo abrindo); 15,5 s (final completo).
