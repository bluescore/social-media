# Áudio do corte de 10 s — como foi feito e como refazer

O corte é o trecho do episódio 1 que começa em 25,3 s (a "virada"). Ele usa a variante em que a dobra acontece uma batida depois do SPEC: uma batida é 0,833 s a 72 BPM (batidas por minuto). O corte dura **10,833 s** (325 quadros a 30 por segundo).

O arquivo final é `assets\audio\mix-corte10s.wav`. É um WAV (áudio sem compressão), em 48 kHz, estéreo, com 10,833 s exatos.

## O que acontece no som, segundo a segundo (tempo do corte)

| Tempo | Som |
|---|---|
| 0 – 1,2 s | ambiente do consultório à noite, bem baixo, sumindo aos poucos |
| 0,200 s | clique do interruptor do abajur |
| 1,000 – 3,304 s | a voz: "cada linha que ela escreveu virou uma cena." |
| 1,7 · 2,1 · 2,5 · 2,9 s | traço de lápis no papel, um por palavra pintada (baixinho, alternando 2 gravações) |
| 5,033 s | a folha se descolando da mesa (sutil) |
| 5,900 · 6,733 · 7,633 s | dobra de papel 1, 2 e 3 |
| 6,483 – 8,013 s | riser (som que sobe), terminando 20 ms antes do golpe |
| **8,033 s** | **o golpe da trilha** (quadro 241), reforçado por um grave com eco |
| 8,033 – 10,833 s | a trilha no auge; nos últimos 0,25 s, o som some (fade) |

A trilha fica baixa sob a voz, com volume 0,14. Ali ela também perde um pouco das médias (a faixa de 1 a 4 kHz, onde a voz mora), para a voz ficar clara. Depois da fala, o volume sobe até o golpe e fica em 0,45 até o fim.

## As escolhas

- **Voz: tomada A.** As duas tomadas saíram com todas as palavras (o Whisper, que transforma fala em texto, conferiu).
  - Na tomada A, a frase tem um acento só, no começo ("cada"), e vai descendo até "cena". É a leitura mais calma e natural.
  - A tomada B acentua também "linha", com um salto de tom no meio da frase.
  - A fala foi recortada da tomada inteira só nas pausas: de 17,090 a 19,775 s. A fala em si vai de 17,290 a 19,594 s.
  - Nada foi esticado, acelerado, emendado ou passou por limitador.
- **Trilha: candidata B.** O golpe dela está em 36,677 s da música. Para cair em 8,033 s do corte, a música foi só deslocada: o corte usa a música de 28,644 a 39,477 s, inteira, sem esticar e sem cortar no meio.
  - Por que a B: é o golpe mais nítido das três. A música vai do quase silêncio ao som cheio de uma vez, e logo depois vem a parte sustentada, com pulso.
  - Na A e na C, um grave forte cairia em 1,3 a 1,4 s do corte, bem embaixo da voz. Isso seria um "segundo impacto". As medições estão em `golpes.json` e no `audio-corte10s.json`.
- **Efeitos** (2 gravações de cada; a escolhida e o motivo estão em `geracoes-elevenlabs.json`):
  - ambiente b
  - interruptor b
  - traço a e b, alternadas
  - folha b
  - dobra 1 a, dobra 2 b, dobra 3 a
  - riser b
  - impacto a
- **Sons fixos da série:** `assets\audio\dobra-1.wav`, `dobra-2.wav` e `dobra-3.wav` já estão recortados e com volume ajustado. Use sempre os mesmos nos próximos episódios.

## Medições do arquivo final

| Medida | Valor |
|---|---|
| Volume percebido (LUFS integrado) | **-14,8 LUFS** (alvo ~-14) |
| Pico real | **-1,2 dBTP** (limite: -1) |
| Golpe | **8,033 s** (medido no arquivo final; o `npx hyperframes audio` também acha o ponto mais íngreme em 8,032 s) |
| Fala | 1,000 a 3,304 s |
| Voz | -19,4 LUFS |
| Trilha sob a voz | -29,9 LUFS (10,5 dB abaixo da voz) |
| Efeitos sob a voz | -35,7 LUFS |

O Whisper entende as 8 palavras no mix final, com a música e os efeitos por baixo.

- **Ganho fixo final: +12,3 dB.** É o mesmo do começo ao fim. Quem o limita é o pico da voz: ele não pode passar de -1,2 dB.
- **Limitador** (o que segura picos): só age no impacto, entre 8,05 e 9,15 s, e achata no máximo 2,1 dB. Ele nunca toca a voz.

## Como refazer

Tudo roda no terminal, dentro da pasta do episódio:

```
cd C:\social-media\hyperframes\clinicas-ep01-protocolo-implante
```

1. **Mudar volume, tempo ou qual gravação usar:** abra `fonte\audio\montar-corte10s.py` e mexa no bloco `PLANO`, no começo do arquivo. Cada som tem lá o arquivo, onde ele entra no corte (`no_corte`) e o volume (`pico_alvo_db`). Depois rode:
   ```
   python -I fonte/audio/montar-corte10s.py
   ```
   O script refaz o `mix-corte10s.wav` e o `audio-corte10s.json` e mostra no terminal o LUFS, o pico, onde caiu o golpe e onde começa e termina a fala.
2. **Conferir onde cada som bate:**
   ```
   npx hyperframes audio assets/audio/mix-corte10s.wav --only moments,onsets,loudness --json
   ```
3. **Conferir as palavras de uma tomada nova de voz:**
   ```
   python -I fonte/audio/transcrever.py assets/audio/fontes/<arquivo>.mp3
   ```
   O script compara com o texto do SPEC e lista o que faltou ou sobrou. Ele roda no processador, porque a placa de vídeo não tem a biblioteca cuBLAS instalada.
4. **Medir o golpe de uma trilha nova:**
   ```
   python -I fonte/audio/medir-golpe.py assets/audio/fontes/<trilha>.mp3
   ```
   Também dá para usar:
   ```
   npx hyperframes audio <trilha> --only sections,onsets,moments --json
   ```
   Atenção: o "maior salto do grave" nem sempre é o golpe. Confira se o som salta em todas as faixas, do grave ao agudo.
5. **Escolher efeitos novos:**
   ```
   python -I fonte/audio/medir-efeitos.py
   ```
   O script mede todos os efeitos de `assets\audio\fontes\`: duração, quantos estalos, se parece nota musical e, no riser, se sobe até o fim.
6. **Gerar de novo no ElevenLabs:** os pedidos exatos estão em `fonte\audio\prompts\`. O fluxo do ElevenLabs com todos os nós é o `MHFvq3M3aRWH1DU1Bimq` (link em `geracoes-elevenlabs.json`).
   - Use o conector do ElevenLabs desta conta. Nada de Higgsfield.
   - Baixe os arquivos para `assets\audio\fontes\` e troque o nome do arquivo no `PLANO`.

## Créditos do ElevenLabs gastos (12/11/2026)

| Geração | Créditos | US$ |
|---|---|---|
| Narração inteira, 2 tomadas (eleven_v4, 432 cada) | 864 | 0,17 |
| Trilha, 3 candidatas de 75 s (eleven_music_v2_5, 1.125 cada) | 3.375 | 0,68 |
| 9 efeitos × 2 tomadas (ambiente 16,7 · interruptor 2 · traço 2 · folha 3,3 · cada dobra 2,3 · riser 6,7 · impacto 10, cada tomada) | 95,3 | 0,02 |
| **Total** | **4.334** | **0,87** |

A transcrição (Whisper) roda no computador e não custa nada.

## Atenção para o episódio completo

- **O golpe da trilha B está em 36,68 s da música, não em 27,5–29,0 s como pede o SPEC.** Com o impacto no quadro 1000 (33,333 s), o começo da música cairia antes do início do episódio.
  - Para a música entrar entre 3,5 e 5,0 s, seria preciso começar a música B perto de 6,4 s (a primeira nota cairia em ~3,2 s do episódio). Esse começo da B tem notas de piano, não é só silêncio.
  - Se o dono preferir respeitar a regra à risca, é preciso gerar outra trilha.
- **A trilha B tem uma nota grave longa** (só grave, sem ataque) 3,3 s antes do golpe. No corte, ela cai em 4,70 s, logo antes de a folha descolar. Se ela soar como um "segundo impacto", dá para baixar a trilha nesse trecho só com volume.
- **Estilo e velocidade da voz:** o conector do ElevenLabs só deixa ajustar estabilidade (0,55) e similaridade (0,75). Estilo e velocidade ficaram no padrão do modelo (estilo 0, velocidade 1,0), o que bate com o pedido.
- **Todas as candidatas guardadas inteiras:**
  - trilhas: `trilha-tema-a/b/c.mp3`
  - voz: `narracao-amedeiros-v4-a/b.mp3`
  - efeitos: as 2 tomadas de cada

  Para cortar as outras falas da tomada A, os tempos de cada palavra estão em `fonte\audio\narracao-amedeiros-v4-a.palavras.json`. Os tempos do Whisper são aproximados (ele chega a errar uns 0,4 s no começo de uma frase), então confira a pausa pelo volume antes de cortar, como foi feito aqui.

---

# Corte ampliado (0 a 36,133 s) — como foi feito e como refazer

O dono pediu um corte maior, para ver mais da dra. Helena. O corte ampliado começa no **início do episódio (0 s)** e termina onde o corte de 10 s termina. O vídeo tem **36,3 s**; o áudio vai de 0 a **36,133 s** e o resto é silêncio.

O arquivo final é `assets\audio\mix-corte-ampliado.wav` (WAV de 48 kHz, estéreo, 24 bits, 36,133 s exatos). Quem o monta é `fonte\audio\montar-corte-ampliado.py`. Os números de tudo estão em `assets\audio\audio-corte-ampliado.json`.

O corte de 10 s não foi mexido: `montar-corte10s.py` e `mix-corte10s.wav` continuam iguais.

## De 25,3 s em diante é o corte de 10 s, igual

A partir de 25,3 s, o arquivo novo é o corte de 10 s aprovado, amostra por amostra. O script confere isso no fim com um "teste de subtração": tira o corte de 10 s de dentro do arquivo novo e mede o que sobra.

- De 25,34 s até o fim, sobra **zero**. É o mesmo áudio, com o mesmo volume.
- Nos 40 ms entre 25,30 e 25,34 s, a diferença é mínima (-44 dBFS): é o ambiente que vinha de antes saindo por baixo, e a trilha, que aqui já vinha tocando.

O ganho fixo final é o mesmo do corte (+12,32 dB). Ele é calculado com a mesma conta, sobre o trecho do corte.

## O que acontece no som (tempo do episódio)

| Tempo | Som |
|---|---|
| 0 – 25,3 s | ambiente do consultório à noite, bem baixo, sem parar |
| 0,100 – 2,066 s | voz: "décima quarta tentativa." |
| 2,230 s | toque seco no vidro ("apagar") |
| 2,316 – 3,378 s | voz: "e o vídeo não sai." (entrou 0,316 s depois do pedido; veja abaixo) |
| 3,100 s | tique seco do contador (take 14 vira take 15) |
| 4,0 – 5,0 s | a trilha entra, com fade de 1 s |
| 4,4 – 6,9 s | sopro grave do recuo da câmera: cresce, fica mais forte em 5,3 s (o meio do movimento) e some. Na prática, por baixo da voz, ele se ouve de 5,0 a 5,5 s (um sopro curto e discreto no momento mais rápido do recuo) |
| 4,400 – 9,230 s | voz: "a doutora Helena explica a prótese protocolo toda semana, paciente por paciente." |
| 10,100 – 13,054 s | voz: "o roteiro sobre implantes está pronto há seis semanas." |
| 10,300 s | papel farfalhando de leve (a folha chega) |
| 14,500 – 15,664 s | voz: "a gravação, não." |
| 15,26 – 15,62 s | risco de caneta em "gravar 06/11" (cobre o "não", que vai de 15,42 a 15,66 s) |
| 17,270 s | toque seco no vidro (abre o perfil) |
| 17,33 – 18,03 s | atrito suave da rolagem da tela: já se ouve em 17,33 s, fica mais forte em 17,50 s (o começo da rolagem, a parte mais rápida) e some por volta de 17,8 s; a tela continua deslizando até parar em 18,33 s |
| 20,900 – 22,414 s | voz: "ela não gravou a décima quinta." |
| 22,500 s | obturador do celular: fecha (22,53 s) e reabre (22,61 s) |
| 22,900 s | toque seco no vidro ("enviado") |
| 23,400 – 24,368 s | voz: "mandou só o roteiro." |
| 25,3 s em diante | o corte de 10 s: interruptor (25,5), "cada linha que ela escreveu virou uma cena." (26,300 – 28,604), traços (27,0 · 27,4 · 27,8 · 28,2), folha (30,333), dobras (31,2 · 32,033 · 32,933), riser (31,783 – 33,313), **golpe em 33,333 s** |

## As escolhas

- **Voz:** as 8 falas saem da mesma tomada A (`narracao-amedeiros-v4-a.mp3`), cada uma recortada no meio das pausas. Nada foi esticado, acelerado, emendado ou limitado.
  - "décima quarta tentativa." dura 1,97 s e terminaria em 2,07 s, depois do começo pedido para "e o vídeo não sai." (2,00 s). A segunda fala entrou em **2,316 s**: 0,25 s depois do fim da primeira. É a menor pausa entre frases que a própria tomada faz.
  - Duas falas ficaram um pouco mais baixas, só para o pico não passar do limite: "décima quarta tentativa." (-0,4 dB) e "o roteiro sobre implantes..." (-0,7 dB).
  - As outras falas saem no volume em que a tomada foi lida. Por isso algumas soam mais altas que outras.
- **Trilha:** a mesma candidata B. Ela só foi deslocada, para o golpe cair em 33,333 s: o tempo da música é o tempo do episódio + 3,344 s. Ela começa a soar em 4,0 s, com fade de 1 s.
  - O volume **não** ficou em 0,14 fixo. A trilha B tem notas fortes entre 6,7 e 12,9 s e em 16,7 e 20,0 s, e fica fraca justo de 25,3 a 28,8 s.
  - Com 0,14 fixo, a música tocaria até 8,6 dB mais alto (de 6,7 a 10 s) do que logo depois de 25,3 s, e cairia 7,4 dB bem quando o abajur apaga. Isso iria contra a regra de crescer aos poucos até o golpe.
  - Por isso o volume muda uma vez por frase do piano (as notas vêm a cada 3,33 s). A mudança é feita em 0,3 s, logo antes de cada nota. Assim, cada frase fica um pouco mais alta que a anterior: de -33,1 LUFS em 5 s até -30,8 LUFS logo antes de 25,3 s. Daí em diante vem o volume do corte.
  - Os fatores (de 0,047 a 0,16) estão no `PLANO` do script.
  - Sob cada fala, a trilha perde um pouco das médias (1 a 4 kHz, -4 dB), como no corte.
- **Ambiente de 0 a 25,3 s:** não foi gerado de novo. É a mesma gravação do corte (`ambiente-noite-b.mp3`), repetida 7 vezes, com cruzamentos de 0,5 s.
  - Em cada emenda, o script procura o ponto da gravação que mais se parece com o fim da cópia anterior, para o zumbido não "bater".
  - O volume é o mesmo do corte, para não haver degrau em 25,3 s.
- **Efeitos novos** (gerados no ElevenLabs, 2 tomadas de cada; o motivo de cada escolha está em `geracoes-elevenlabs.json`):
  - toque no vidro: tomada c, que é um toque surdo e seco, sem ressonância. A 1ª rodada (a, b) saiu com chiado ou com nota. É o mesmo toque nos 3 lugares.
  - tique do contador: tomada a, só o 2º estalo.
  - sopro grave: tomada d, que é ar grave subindo e sumindo. A 1ª rodada (a, b) saiu como um estrondo grave quase com nota, que pareceria um segundo impacto.
  - papel farfalhando: tomada a.
  - risco de caneta: tomada c, um traço só e seco. A 1ª rodada (a, b) rangia com tom.
  - rolagem: tomada a, usada a partir de 0,30 s do arquivo, porque o começo dela sobe devagar (ver "Conferência", no fim).
  - obturador: tomada a, porque tem dois estalos, como a tela que fecha e reabre.

## Medições do arquivo final

| Medida | Valor |
|---|---|
| Volume percebido (LUFS integrado) | **-17,6 LUFS** (pedido: -14 a -15; veja o ponto a decidir) |
| Pico real | **-1,2 dBTP** (limite: -1) |
| Golpe | **33,333 s** (o `npx hyperframes audio` acha o ponto mais íngreme em 33,332 s) |
| Voz, nas falas | -19,1 LUFS |
| Trilha sob a voz | -32,3 LUFS (13,2 dB abaixo da voz) |
| Efeitos sob a voz | -39,3 LUFS |
| Limitador | só no impacto, de 33,35 a 34,45 s, no máximo 2,1 dB (o mesmo do corte) |

O Whisper entende as 50 palavras das 8 falas no mix final, com a música e os efeitos por baixo. Depois do golpe, onde não há fala, ele "inventa" uma frase sobre a música. Isso é um erro comum do Whisper e pode ser ignorado.

## Ponto a decidir: o volume total

O volume total ficou em -17,6 LUFS, e não em -14. Com as regras de hoje, não dá para subir mais:

- O corte de 10 s chegava a -14,8 porque a parte forte (o golpe e o fim) era um terço dele. No corte ampliado, quase tudo é voz.
- A voz já está no máximo. O pico de "cada linha que ela escreveu..." já está em -1,2 dBTP.
- Para chegar a -14, seria preciso subir tudo mais 3,3 dB. Isso levaria esse pico a +2 dBTP, o que exigiria limitar a voz.

O dono decide entre:
- aceitar -17,6 LUFS nesta prévia de validação;
- ou liberar um limitador leve só em 2 ou 3 picos da voz.

Igualar as falas com um ganho fixo por fala (sem limitador) ajuda pouco: subindo as falas mais baixas até o nível da mais alta, sem nenhum pico passar de -1,2 dBTP, o total chega a cerca de -16,5 LUFS. "décima quarta tentativa." e "o roteiro sobre implantes..." quase não podem subir, porque já estão perto do pico.

## Como refazer

Dentro da pasta do episódio:

```
python -I fonte/audio/montar-corte-ampliado.py
```

O script refaz `mix-corte-ampliado.wav` e `audio-corte-ampliado.json`. No terminal, ele mostra o LUFS, o pico, onde caiu o golpe, onde começa e termina cada fala, o volume da trilha em cada frase do piano e o teste de subtração.

Para mudar volume, tempo ou gravação, mexa no bloco `PLANO`:
- falas: `alvo`, `ganho_db`;
- trilha: `volume`;
- efeitos: `no_ep`, `pico_alvo_db`.

Se alguma fala ou efeito passar do pico permitido, o script para e diz em que segundo isso aconteceu. Aí é só baixar o `ganho_db` dela no `PLANO`. A voz nunca vai para o limitador.

## Créditos do ElevenLabs gastos no corte ampliado (12/11/2026)

| Geração | Créditos |
|---|---|
| 1ª rodada: 7 efeitos × 2 tomadas (toque, tique, sopro, papel, risco, rolagem, obturador) | 44,0 |
| 2ª rodada: toque, sopro e risco refeitos, 2 tomadas cada | 24,0 |
| **Total** | **68,0** (US$ 0,014) |

O resumo de cada execução arredonda cada geração para cima e mostra 72 créditos. Somando tudo do ep. 01 até agora, são 4.402 créditos (US$ 0,88). Os pedidos exatos estão em `fonte\audio\prompts\` (os refeitos têm `-v2` no nome).

## Conferência independente do corte ampliado (12/11/2026)

Uma segunda conferência mediu o arquivo final por conta própria, sem usar os números do script. Para achar cada som, ela procurou o próprio arquivo de origem dentro do mix (correlação: "onde esse som aparece igualzinho").

**Confere:**
- Duração: 36,133 s exatos (1.734.384 amostras), 48 kHz, estéreo, 24 bits. O fade de 0,25 s está só no fim.
- Volume e pico (`ffmpeg ebur128`): -17,6 LUFS integrado e -1,2 dBTP de pico real. Nenhuma amostra estoura. O pico mais alto fica no impacto (33,35 s) e em "cada linha..." (26,35 s).
- Golpe em 33,333 s (o mesmo ponto do corte de 10 s).
- As 8 falas começam nos tempos da tabela acima, com diferença de 0 ms.
  - Cada fala é a tomada A sem mudança: a mesma forma de onda (semelhança de 0,96 a 0,997, com a música por baixo) e o mesmo ganho do começo ao fim (variação de até ±0,3 dB, que é o efeito da música por baixo).
  - Ou seja: nada esticado, acelerado ou limitado.
  - Tirando a voz do mix, não sobra nenhum resto dela.
- O Whisper reconhece as 50 palavras das 8 falas.
- Os pontos de corte da voz caem em silêncio na tomada (-67 a -89 dBFS).
- Sem estalos: tirando a voz, os únicos sons secos são os efeitos pedidos (toques, tique, obturador, interruptor, traços e dobras). Não há nada nas emendas do ambiente, na entrada da trilha nem em 25,3 s.
- Trilha:
  - tempo da música = tempo do episódio + 3,344 s;
  - zero antes de 4,0 s, entrada suave até 5,0 s;
  - menos médias sob as falas.
  - Também confere a conta do relatório: com 0,14 fixo, a música tocaria de -23,9 a -28,4 LUFS em várias frases antes de 25,3 s e cairia para -32,4 em 25,3 s.
- Efeitos dentro de 1 quadro do tempo pedido: toque 2,230 · tique 3,100 · papel 10,300 · risco 15,260 · toque 17,270 · obturador 22,500 (estalos em 22,53 e 22,61) · toque 22,900.
  - O toque c não tem nota: a energia está em 100–300 Hz e some em ~10 ms.
- De 25,34 s ao fim, o arquivo é idêntico ao `mix-corte10s.wav`, amostra por amostra.

**Corrigido:**
- A rolagem da tela. Com o trecho começando em 0,10 s do arquivo, o atrito só se ouvia de 17,45–17,54 s em diante (4 a 6 quadros depois de a tela começar a rolar), e ficava mais forte em 17,70.
- Agora o trecho começa em 0,30 s do arquivo: o atrito já se ouve em 17,34 e fica mais forte em 17,50, o começo da rolagem com inércia, quando ela é mais rápida.
- Mesmo arquivo e mesmo volume. Só o trecho de 17,33 a 18,23 s do mix mudou. O total foi de -17,53 para -17,60 LUFS.

**Mantido (de propósito):**
- O sopro grave dura de 4,37 a 6,93 s, mas, por baixo da voz, só se ouve de 5,0 a 5,5 s, com o pico em 5,26 s.
- É o meio do recuo (`power2.inOut`, mais rápido em 5,3 s), logo antes de a borda da maquete entrar (~5,4 s). Fica um sopro curto e discreto no momento mais rápido do movimento, e não do 4,0 ao 6,6.

---

# Episódio completo (0 a 64,0 s) — versão para aprovação

O dono aprovou o corte ampliado e pediu o episódio inteiro, "só um pouquinho mais rápido". A linha do tempo ficou mais curta (64,0 s em vez de 69,2 s) e todos os sons foram recolocados nos tempos novos.

- Arquivo final: `assets\audio\mix-final.wav` (WAV de 48 kHz, estéreo, 24 bits, 64,0 s exatos = 3.072.000 amostras).
- Quem o monta: `fonte\audio\montar-final.py`.
- Os números de tudo (cada fala, cada som, cada medição): `assets\audio\audio-final.json`.
- Nada dos arquivos antigos mudou: `montar-corte10s.py`, `montar-corte-ampliado.py`, `mix-corte10s.wav`, `mix-corte-ampliado.wav` e os `.json` deles continuam iguais.

## O que mudou em relação ao corte ampliado

- **O golpe** (o "impacto" da música) agora cai em **30,633 s** (quadro 919). A trilha continua a mesma (candidata B), só deslocada: tempo da música = tempo do episódio + 6,044 s.
- **De 22,6 a 33,43 s é o corte de 10 s aprovado**, com os mesmos sons, volumes e tempos (só deslocados 22,6 s). O script confere isso no fim com o "teste de subtração": de 22,64 a 33,18 s a diferença é praticamente zero (-120 dBFS em média; o máximo, -88 dBFS, é inaudível).
- **A voz agora tem o mesmo volume em todas as falas.** Na tomada, as falas variavam 6,6 dB entre si (de -20,7 a -27,4 LUFS). Cada fala recebeu um ganho fixo próprio (o mesmo do começo ao fim dela) para todas ficarem em -19,4 LUFS. Isso não é limitador nem compressor: é só "aumentar ou abaixar o volume" da fala inteira.
- **As cenas 8 a 12 são novas**: o vídeo dela (s08), o post (s09), a turma (s10), a tarde (s11) e o cartão (s12).

## As falas (tomada A, cortadas só nas pausas)

| # | Fala | Pedido | No mix (começa–termina) | Ganho da fala |
|---|---|---|---|---|
| 1 | décima quarta tentativa. | 0,10 | 0,100–2,066 | -7,97 dB |
| 2 | e o vídeo não sai. | 2,32 | 2,320–3,382 | -5,28 dB |
| 3 | a doutora Helena explica a prótese protocolo... | 3,95 | 3,950–8,780 | -7,34 dB |
| 4 | o roteiro sobre implantes está pronto há seis semanas. | 9,45 | 9,450–12,404 | -9,26 dB |
| 5 | a gravação, não. | 12,95 | 12,950–14,114 ("não" em 13,87–14,11) | -4,36 dB |
| 6 | ela não gravou a décima quinta. | 18,60 | 18,600–20,114 | -10,84 dB |
| 7 | mandou só o roteiro. | 20,90 | 20,900–21,868 | -8,34 dB |
| 8 | cada linha que ela escreveu virou uma cena. | 23,60 | 23,600–25,904 | -7,60 dB (a do corte) |
| 9 | o perfil voltou a andar. | 43,70 | 43,700–45,022 | -8,45 dB |
| 10 | ela mandou o vídeo pra turma. | 47,20 | 47,200–48,456 | -10,99 dB |
| 11 | o roteiro ela já tinha. | 52,30 | 52,300–53,366 | -8,52 dB |
| 12 | no próximo episódio: o que a recepção mais ouve. | 59,60 | 59,600–62,742 | -9,41 dB |

- Nenhuma fala precisou deslizar: todas começam exatamente no tempo pedido.
- As 4 falas novas foram cortadas no meio das pausas da tomada (onde o volume fica abaixo de -50 dBFS): 19,775 · 21,449 · 23,020 · 24,466 s. A última vai até o fim da tomada (28,0 s).
- O "ganho da fala" é antes do ganho final (+12,32 dB, o mesmo para tudo). Somando os dois, cada fala sobe de +1,3 a +8,0 dB.
- Quem decide até onde a voz pode subir são "cada linha..." e "décima quarta tentativa.": são as duas que têm o pico mais alto para o seu volume (um "c" e um "d" fortes no começo). Com elas em -1,2 dBTP de pico, todas as falas ficam em -19,4 LUFS.

## O que acontece no som (tempo do episódio)

| Tempo | Som |
|---|---|
| 0 – 22,6 s | ambiente do consultório à noite, bem baixo (a mesma gravação do corte, repetida com cruzamentos) |
| 1,93 · 2,65 | toque seco no vidro ("apagar") · tique do contador |
| 3,55 – 4,55 | a trilha entra, com fade de 1 s, junto com o recuo da câmera |
| 3,77 – 6,33 | sopro grave do recuo, mais forte em 4,70 s (o meio do recuo, 3,55–5,85) |
| 9,30 | papel farfalhando (a folha chega) |
| 13,70 – 14,06 | risco de caneta (cai no "não", 13,87) |
| 15,37 · 15,43 – 16,13 | toque (abre o perfil) · atrito da rolagem |
| 19,90 · 20,35 | obturador (estalos em 19,93 e 20,01) · toque "enviado" |
| 22,6 – 33,43 | **a virada, igual ao corte de 10 s**: interruptor 22,8 · traços 24,3/24,7/25,1/25,5 · folha 27,633 · dobras 28,5/29,333/30,233 · riser 29,083–30,613 · **golpe 30,633** |
| 30,633 – 43,4 | o vídeo dela, sem voz: a trilha no auge |
| 34,30 – 35,45 | atrito seco de vidro fosco (a varredura) |
| 37,567 – 37,97 | chiado fino de corte (começa junto com o plano de corte, quadro 1127) |
| 38,167 – 39,47 | textura granular do crescimento (junto com o osso crescendo, 38,167–39,367) |
| 40,757 – 41,96 | faixa de luz: brilho suave e seco (ouve-se a partir de 40,867, junto com a faixa de luz, 40,867–41,867) |
| 43,4 – 43,85 | a trilha "relaxa" (desce até o leito) |
| 43,77 – 45,03 | sopro suave de levar junto (mais forte em 44,0, a parte mais rápida do encolhimento) |
| 43,4 – 51,9 | ambiente da recepção ao fim de tarde (entra em 0,6 s; sai seco no corte de 51,9) |
| 47,30 · 47,55 · 48,90 | toque (abre a conversa) · toque "encaminhado" · chegada da mensagem (dois toques secos) |
| 51,9 – 59,4 | ambiente do consultório à tarde (entra seco no corte; sai em 0,4 s antes do cartão) |
| 52,300 · 52,767 · 53,233 · 53,667 · 54,133 · 54,600 | os 6 passos de madeira dela (quadros 1569 · 1583 · 1597 · 1610 · 1624 · 1638) |
| 54,75 | porta fechando suave, fora do quadro |
| 53,6 – 54,8 | a trilha sobe 3 dB para o silêncio de "faltava a forma" e da dedicatória |
| 57,31 | a música resolve (volta ao acorde de lá menor) |
| 57,96 – 64,0 | a música vai sumindo sozinha (fade natural); fade de 0,25 s só no último quarto de segundo |

## As escolhas

**A trilha (sempre a mesma, só deslocada e com volume em curvas lentas):**
- Até o golpe, o volume muda uma vez por frase do piano, como no corte ampliado (os mesmos fatores, porque a música é a mesma; só o tempo mudou). Cada frase inteira fica um pouco mais alta que a anterior: -33,2 → -32,3 → -32,0 → -31,7 → -31,5 → -31,3 → -30,3 LUFS. Nunca cai antes do golpe.
  - Dentro da frase de 20,6 a 24,0 s, a nota que soa vai morrendo: a 2ª metade (22,6–24,0) fica 1,7 dB abaixo da 1ª. É o próprio som do piano, igual ao corte aprovado.
- No vídeo dela (30,6–43,4 s), a trilha fica no auge (0,45), sustentada.
  - Um único acento da música, em 37,32 s (no passo 2 do vídeo dela), passaria muito do pico permitido. Ele desce 3 dB por 0,3 s (de 37,2 a 37,7 s, com rampas de 0,1 s).
  - O limitador (o que segura picos) age só na trilha e nos efeitos, só nesse trecho sem voz. Ele achata no máximo 3,9 dB, em estalos de poucos milésimos de segundo (43,15 · 43,22 s). A voz é somada depois, então nunca passa por ele.
- **De 43,4 s em diante a trilha "relaxa"**: desce até o leito em 0,45 s (rápido no começo), para a fala 9 (43,70) já entrar sobre a música baixa.
  - O SPEC pedia 0,20. Esse número não serve aqui: a trilha B **não relaxa sozinha** depois do golpe. Ela segue no volume cheio, com pulso, até 57,96 s do episódio. Com 0,20 ela ficaria em ~-17,5 LUFS, mais alta que a própria voz (-19,4).
  - O leito ficou em 0,0405 (-27,9 dB): a trilha fica em -30,5 LUFS sob as falas 9, 10 e 11, 11 dB abaixo da voz. É entre o que ela fica sob "cada linha..." no corte aprovado (10,5 dB abaixo) e no corte ampliado (13,2 dB).
- Em s11, no silêncio da voz ("faltava a forma" e a dedicatória), a trilha sobe 3 dB (rampa lenta de 53,6 a 54,8 s) e fica assim até o fim. Sob a última fala ela já está ~20 dB abaixo da voz, porque a própria música está sumindo.
- **O acorde de resolução**: a trilha B está em lá menor. Depois do golpe ela gira lá menor → fá → dó → sol, e resolve (volta ao lá menor) em **57,31 s** do episódio. Não é um acorde maior: a trilha B não tem um.
  - "faltava a forma" (54,8) cai sobre o acorde de sol, a tensão que pede a resolução.
  - A resolução chega 0,41 s depois de a dedicatória pousar (56,9).
  - A música não foi cortada nem mexida para isso.
- O fim: a música termina sozinha (de 57,96 s em diante ela vai sumindo), com duas notas de piano em 59,79 e 60,63 s, sob a última fala. Ela acaba em 70 s da música, então cobre o episódio inteiro.

**Os ambientes:**
- noite (0–22,6 s): o mesmo leito do corte ampliado, agora até 22,6 s.
- recepção à tarde (43,4–51,9 s): tomada b, com um filtro passa-altas em 100 Hz (tira o ronco grave de trânsito, abaixo de 100 Hz).
- consultório à tarde (51,9–59,4 s): tomada b, a partir de 0,45 s do arquivo (o começo dela sobe devagar, e o corte é seco), com passa-altas em 80 Hz.
- Os três ficam no mesmo nível baixo (-38 a -40 LUFS no mix). A troca de ambiente em 51,9 s marca o corte seco da imagem.

**Os efeitos novos** (2 tomadas de cada; o motivo de cada escolha está em `geracoes-elevenlabs.json`, em `efeitos_final`; as medidas, em `efeitos-final-medidas.json`):
- atrito de vidro fosco: tomada **e** (3ª rodada). As 4 primeiras (a, b, c, d) saíram com rangido com nota.
- chiado de corte: tomada a.
- textura granular: tomada b.
- brilho/luz: tomada a. Um filtro estreito tira uma ponta em 1.605 Hz que poderia soar como nota.
- sopro de levar junto: tomada **d** (2ª rodada). A 1ª rodada saiu como um estrondo grave, que pareceria um segundo impacto.
- chegada de mensagem: tomada b (dois toques secos, sem nota).
- passos: tomada b. Cada um dos 6 passos foi recortado e posto no seu quadro.
- porta: tomada a.
- Os toques de s10 (47,3 e 47,55) são o mesmo toque-vidro-c de sempre.
- No vídeo dela, os efeitos ficam 10 a 12 LU (unidades de volume percebido) abaixo da trilha. O chiado de corte é o mais baixo, porque ele é claro (~8 kHz), justo onde a trilha quase não tem som.

## Medições do arquivo final

| Medida | Valor |
|---|---|
| Volume percebido (LUFS integrado) | **-15,3 LUFS** (meta: o mais perto de -14 sem limitar a voz) |
| Pico real | **-1,2 dBTP** (nenhuma amostra estoura) |
| Golpe | **30,633 s** (o `npx hyperframes audio` acha o ponto mais íngreme em 30,632 s) |
| Voz, em cada fala | -19,4 LUFS (todas iguais) |
| Trilha sob a voz | -31,5 LUFS (12,0 dB abaixo da voz) |
| Efeitos sob a voz | -38,4 LUFS |
| Ganho fixo final | +12,32 dB (o mesmo do corte de 10 s; quem limita é o pico de "cada linha...") |
| Limitador | só trilha + efeitos, só de 30,613 a 43,4 s: no máximo 3,9 dB; 0,04 s com mais de 3 dB |
| Volume por cena | s01 -19,3 · s03 -19,5 · s04 -29,2 · s05 -21,2 · virada -21,1 · **s08 -11,7** · s09 -20,4 · s10 -23,9 · s11 -25,1 · s12 -19,8 |

## Pontos a decidir

1. **O volume total ficou em -15,3 LUFS, não em -14.** A voz já está no máximo sem limitador. Opções:
   - aceitar -15,3 (o corte ampliado tinha -17,6);
   - deixar "cada linha..." e "décima quarta tentativa." 1 dB abaixo das outras falas: o resto sobe 1 dB e o total chega a **-14,5 LUFS** (testado). Mas aí a virada fica 1 dB mais alta que no corte aprovado e o limitador do vídeo dela passa a achatar até 4,9 dB;
   - limitar a voz (contra a regra).
2. **A queda da trilha em 43,4 s é grande** (cerca de 21 dB em 0,45 s), porque a trilha B não relaxa sozinha. Ela acontece junto com o encolhimento do vídeo e o sopro. Se soar brusca, dá para alongar a descida (mas a fala 9 entraria sobre a música ainda alta) ou começar a descida um pouco antes de 43,4.
3. **A resolução da música cai em 57,31 s**, perto da dedicatória (56,9), e não em "faltava a forma" (54,8). Se o dono quiser o acorde junto de um texto, quem se move é a imagem (por exemplo, a dedicatória pousar em 57,3). A música não deve ser cortada para isso.
4. **Os passos estão em quadros fixos** (1569 · 1583 · 1597 · 1610 · 1624 · 1638), um a cada ~0,46 s. A animação de s11 precisa trocar de pose nesses quadros, e a porta fecha em 54,75 s.

## Como refazer

Dentro da pasta do episódio:

```
python -I fonte/audio/montar-final.py
```

O script refaz `mix-final.wav` e `audio-final.json`. No terminal, ele mostra:
- o LUFS e o pico;
- onde caiu o golpe;
- onde começa e termina cada fala, com o volume e o pico dela;
- o volume da trilha por trecho;
- o teste de subtração contra o corte de 10 s.

Para mudar alguma coisa, mexa no bloco `PLANO`:
- falas: `alvo` e `ajuste_db` (o ganho de cada fala é calculado sozinho para igualar o volume; o `ajuste_db` soma ou tira em cima disso);
- trilha: `volume` (até 43,4 s), `relaxa` (o leito depois de 43,4), `realce` (os 3 dB de s11);
- efeitos: `no_ep`, e o volume em `pico_alvo_db`, `rms_alvo_db` ou `abaixo_trilha_db`.

Se algo passar do pico permitido, o script para e diz em que segundo. A voz nunca vai para o limitador.

Para escolher efeitos novos sem ouvir, só pelos números: `python -I fonte/audio/medir-efeitos-final.py` (grava `efeitos-final-medidas.json`; não mexe no `efeitos-medidas.json` antigo).

## Conferência do episódio completo (12/11/2026)

Conferido no arquivo final, por conta própria (procurando cada som de origem dentro do mix):
- 64,000 s exatos, 48 kHz, estéreo, 24 bits; a última amostra é zero.
- As 12 falas começam no tempo da tabela, com 0 ms de diferença. Cada uma é a tomada A sem mudança (semelhança de 0,97 a 1,00) e com o mesmo ganho do começo ao fim (±0,13 dB): nada esticado, acelerado ou limitado.
- O Whisper ouve as 75 palavras. Ele acrescenta um "e" de 20 ms entre "prótese" e "protocolo"; a fala é a tomada sem mudança, então é um erro do Whisper.
- A trilha está no lugar certo: trechos da música crua achados em 34, 40, 48 e 56 s do episódio, exatamente no tempo esperado (música = episódio + 6,044 s); zero antes de 3,55 s.
- Os efeitos estão nos tempos pedidos (os ambientes e o sopro, que são ruído, não dão para achar assim; os passos sob a fala também não).
- Sem estalos nas emendas (0; 3,55; 22,6; 43,4; 43,85; 51,9; 59,4; 64,0 s).

## 2ª conferência independente do episódio completo (12/11/2026) — e a correção que ela fez

Conferido de novo no arquivo, com medidas próprias:
- **Formato:** 64,000 s (3.072.000 amostras), 48 kHz, estéreo, 24 bits; a primeira e a última amostra são zero. Rodar o script de novo dá um arquivo idêntico, bit a bit.
- **Volume e pico** (`ffmpeg ebur128`): -15,3 LUFS, -1,2 dBTP, LRA 15,7. Nenhuma amostra passa de -1,2 dBFS.
- **Golpe:** 30,633 s (quadro 919). O som do impacto e o golpe da música caem nesse ponto; o `npx hyperframes audio` acha o ponto mais íngreme em 30,632 s.
- **Voz:** as 12 falas estão no lugar, com 0 ms de diferença. Tirando de dentro do mix a tomada A com um ganho só por fala, sobra quase nada (-57 a -85 dB): é a tomada inteira, sem esticar, acelerar, emendar nem limitar. Nos 5 picos mais fortes de cada fala, o ganho é o mesmo do resto da fala (±0,1 dB). Todos os cortes no meio da tomada caem em silêncio (de -67 a -89 dBFS). Só o começo da tomada já sai falando, como no corte aprovado.
- **Whisper**, com o `transcrever.py`: ouve as 75 palavras (só acrescenta o "e" de 20 ms entre "prótese" e "protocolo", que não existe). Ouvindo cada fala sozinha, todas as palavras saem certas.
- **Efeitos:** os 37 sons estão no tempo pedido (±1 ms). Os 3 que se confundem com a voz por cima (sopro grave, 1º traço e 1º passo) foram achados tirando a voz do mix.
- **Estalos:** sem estalo, corte seco ou distorção. Os únicos estalos achados são os sons secos de propósito (toques, tique, interruptor, dobra, porta) e as consoantes da própria voz.
- **Trilha:** a mesma música, deslocada 6,044 s, em todo o episódio (achada em 15 pontos). Antes do golpe, cada frase do piano fica mais alta que a anterior (-33,2 → -32,3 → -32,0 → -31,7 → -31,5 → -31,3 → -30,3 → -24,3 LUFS). Depois do golpe ela fica no auge e, de 43,4 s em diante, relaxa até o leito.

**A correção:** três efeitos do vídeo dela estavam fora da imagem. Eles tinham sido postos num esboço antigo de `compositions/s08-video-dela.html`. Hoje o passo 3 começa em 37,567 s e o passo 4 em 40,667 s. Os sons foram movidos para acompanhar a imagem. São os mesmos arquivos e o mesmo jeito de calcular o volume:

| Som | Antes | Agora | O que acontece na imagem |
|---|---|---|---|
| chiado fino de corte | 37,25 | **37,567** | o plano de corte começa a descer |
| textura granular | 37,80 | **38,167** | o osso começa a preencher a rosca (até 39,367) |
| brilho da faixa de luz | 40,50 | **40,867** | a faixa de luz começa a passar (até 41,867) |

Só o trecho de 37,25 a 42,70 s mudou, onde não há voz. Volume total, pico, golpe, falas e a virada continuam iguais. O limitador agora achata menos: some o pico de 40,67 s, e o máximo continua 3,9 dB, em 43,22 s.

## Créditos do ElevenLabs gastos no episódio completo (12/11/2026)

| Geração | Créditos |
|---|---|
| 1ª rodada: 10 efeitos × 2 tomadas | 183,3 |
| 2ª rodada: atrito e sopro refeitos, 2 tomadas cada | 17,3 |
| 3ª rodada: atrito refeito de novo, 2 tomadas | 8,0 |
| **Total** | **208,7** (US$ 0,04) |

O resumo de cada execução arredonda para cima e mostra 212. Somando tudo do ep. 01 até agora: **4.611 créditos (US$ 0,92)**. Os pedidos exatos estão em `fonte\audio\prompts\` (os refeitos têm `-v2` e `-v3` no nome).

---

# Episódio v3 (0 a 71,7 s) — revisão do dono de 12/11/2026

O dono aprovou a v2 no geral e pediu 12 correções (lista em `fonte\PLANO-v3.md`). No som, isso quer dizer: 5 falas novas, uma cena nova (s04b, a "virada" antes da 15ª tentativa), s09 mais longa, s11 sem passos nem porta, e a chamada final trocada por "comente CLÍNICA".

- Arquivo final: `assets\audio\mix-v3.wav` (WAV de 48 kHz, estéreo, 24 bits, 71,7 s exatos = 3.441.600 amostras).
- Quem o monta: `fonte\audio\montar-v3.py` (cópia do `montar-final.py`, adaptada; as regras do topo são as mesmas).
- Os números de tudo: `assets\audio\audio-v3.json`.
- O tempo de cada palavra (para as legendas e o lettering): `assets\audio\voz-v3.palavras.json`.
- A v2 não mudou: `montar-final.py`, `mix-final.wav` e `audio-final.json` continuam iguais.

## O que ficou igual à v2 (conferido no arquivo)

- **0 a 3,5 s: igual bit a bit à v2** (diferença -300 dBFS, ou seja, nenhuma).
- **A virada (25,9 a 36,7 s) é o corte de 10 s aprovado**: o teste de subtração dá -120 dBFS em média (o maior ponto, -88 dBFS, é inaudível), igual ao da v2.
- **O vídeo dela (s08) é igual bit a bit à v2**, só 3,3 s depois.
- As 11 falas antigas são os mesmos trechos da tomada A, com os mesmos ganhos. Todas com o mesmo volume (-19,4 LUFS).
- O ganho fixo final é o mesmo: +12,32 dB. Quem limita continua sendo "cada linha...".
- Os efeitos antigos são os mesmos arquivos, volumes e recortes. De s05 a s09 eles estão 3,3 s depois; em s10, 6,6 s depois.

O que muda entre 3,5 e 25,9 s é a **música**. O golpe agora cai 3,3 s mais tarde (33,933 s). A música não pode ser esticada nem cortada, então ela começa 3,3 s "mais cedo" dentro da faixa. Debaixo de s01 a s04 toca a frase de piano que vinha antes na faixa. É a mesma música, com o mesmo jeito.

## As falas

| id | Fala | Tomada | No mix (começa–termina) | Ganho da fala |
|---|---|---|---|---|
| 1 | décima quarta tentativa. | A | 0,100–2,066 | -7,97 dB |
| 2 | e o vídeo não sai. | A | 2,320–3,382 | -5,28 dB |
| 3 | a doutora Helena explica a prótese protocolo... | A | 3,950–8,780 | -7,34 dB |
| 4 | o roteiro sobre implantes está pronto há seis semanas. | A | 9,450–12,404 | -9,26 dB |
| 5 | a gravação, não. | A | 12,950–14,114 | -4,36 dB |
| **F** | quarenta e sete dias sem postar nada. | **nova c** | 15,550–18,046 | -6,22 dB |
| **T** | mas isso está prestes a mudar... | **nova c** | 18,600–20,506 | -7,36 dB |
| 6 | ela não gravou a décima quinta. | A | 21,900–23,414 | -10,84 dB |
| 7 | mandou só o roteiro. | A | 24,200–25,168 | -8,34 dB |
| 8 | cada linha que ela escreveu virou uma cena. | A (a do corte) | 26,900–29,204 | -7,60 dB |
| 9 | o perfil voltou a andar. | A | 47,000–48,322 | -8,45 dB |
| 10 | ela mandou o vídeo pra turma. | A | 53,800–55,056 | -10,99 dB |
| 11 | o roteiro ela já tinha. | A (a antiga, aprovada) | 58,900–59,966 | -8,52 dB |
| **12** | faltava tirar do papel. | **nova b** | 60,400–61,544 | -9,89 dB |
| **13** | se você explica isso todo dia no consultório, o seu também já existe. | **nova a** | 62,100–66,382 | -7,98 dB |
| **14** | comente clínica e a gente te mostra como. | **nova b** | 67,650–69,850 | -9,34 dB |

- Saiu "no próximo episódio: o que a recepção mais ouve."
- Nenhuma fala precisou deslizar: todas começam no tempo pedido.
- Todas as falas novas foram cortadas no meio de pausas silenciosas (abaixo de -80 dBFS). Entre "nada." e "mas", o corte está no ponto mais silencioso da pausa (2,847 s da tomada c, -91 dBFS).
- **Como as tomadas foram escolhidas** (sem ouvir, pelas medidas): para cada fala nova, comparamos as 3 tomadas com a tomada A antiga em três coisas:
  - a altura média da voz (a tomada A fica em 123,8 Hz);
  - o ritmo (6,7 sílabas por segundo);
  - o pico em relação ao volume.
  - Uma fala com o pico alto demais derrubaria o volume de tudo. Por isso a tomada c da fala 14 ficou de fora: ela tem um pico de -3,6 dBFS em "comente".
  - As 3 tomadas saíram completas no Whisper.
  - As notas de cada tomada estão em `audio-v3.json` → `escolha_das_tomadas`.

**Atenção, fala T:** na leitura do ElevenLabs, o "mas" sai **colado** em "isso" ("ma-zi-sso"), sem pausa depois dele. A pausa natural fica depois de "está" (0,18 s): "mas isso está… prestes a mudar". Também não existe pausa curta entre "nada." e "mas": a pausa ali é de 0,37 s. A fala T dura 1,91 s (18,60–20,51), não ~2,5 s como o plano estimava. Ninguém esticou nada: é o tempo da própria leitura.

## O que acontece no som (só o que é novo ou mudou de lugar)

| Tempo | Som |
|---|---|
| 0 – 25,9 | ambiente do consultório à noite (o mesmo leito da v2, agora até 25,9) |
| 3,55 – 4,55 | a trilha entra (igual à v2) |
| 15,55 – 18,05 | fala F (o feed parado) |
| 18,30 – 18,56 | **suspense:** a trilha desce 5,5 dB no corte para s04b |
| 18,60 – 18,87 | "mas" com a trilha baixa |
| 18,87 – 20,15 | a trilha volta devagar sob "isso está prestes a mudar…" |
| 19,42 – 21,98 | **sopro grave suave** (tomada c), mais forte em **20,27** (o "dar" de "mudar") |
| 21,15 | **toque bem discreto** quando a tela do celular apaga (-41, 7 dB mais baixo que os toques comuns) |
| 23,20 · 23,65 | obturador · toque "enviado" (v2 + 3,3 s) |
| 25,9 – 36,73 | **a virada, igual ao corte de 10 s**: interruptor 26,1 · traços 27,6/28,0/28,4/28,8 · folha 30,93 · dobras 31,8/32,63/33,53 · riser até 33,913 · **golpe 33,933** |
| 37,6 · 40,867 · 41,467 · 44,167 | os sons do vídeo dela (v2 + 3,3 s) |
| 46,5 – 47,3 | a trilha relaxa até o leito (v2 + 3,3 s) |
| 46,7 – 58,5 | ambiente da recepção (s09 e s10; 1 emenda em 54,7) |
| 47,3 | sopro de levar junto (v2 + 3,3 s) |
| 50,30 · 50,52 · 50,74 · 50,96 · 51,18 | **5 tiques bem discretos** nos posts novos (-44 de pico, alternando tique a e tique b) |
| 51,50 · 51,80 | **toque suave** em cada etiqueta ("+438 seguidores", "21,3 mil visualizações") |
| 53,9 · 54,15 · 55,5 | toques e chegada da mensagem (v2 + 6,6 s) |
| 58,5 – 67,4 | ambiente do consultório à tarde (1 emenda em 64,75; sai em 0,4 s com o cartão). **Sem passos e sem porta** |
| 60,61 | a música resolve, durante "faltava tirar do papel" |
| 61,26 em diante | a música vai sumindo sozinha (fim natural da faixa) |
| 68,20 | **toque suave** quando a pílula "CLÍNICA" salta |

## As escolhas da trilha

- **Mesma música, só deslocada**: tempo da música = tempo do episódio + 2,744 s (a v2 era + 6,044).
- **Antes do golpe**, cada frase do piano da v2 caiu 3,3 s depois sobre o mesmo pedaço da música. Por isso ela levou junto o seu volume. As falas 6, 7 e 8 andaram os mesmos 3,3 s, então ficam sobre a mesma música e o mesmo volume da v2.
- Entrou uma frase nova no começo (3,9–7,3 s). O volume dela é o que a 1ª frase tinha na v2 (-33,2 LUFS, com a mesma entrada de 1 s).
- Volume de cada frase (LUFS): -33,2 → -32,8 → -32,3 → -32,0 → -30,4 (a frase do suspense; ver abaixo) → -31,5 → -31,3 → -30,3 → -24,3 (o riser).
- Sobre o -30,4 da frase do suspense: o medidor de LUFS ignora os trechos baixos. Por isso a descida faz essa frase "parecer" mais alta. Sem a descida ela mediria -31,7, como na v2.
- **Sob as falas antigas, a trilha fica no mesmo patamar da v2**: falas 3, 4 e 5 em -32,1 / -30,3 / -32,3 (na v2: -31,1 / -31,4 / -31,8). As falas 6, 7 e 8 têm exatamente os mesmos números da v2.
- **De 25,9 a 33,9 s**: exatamente o envelope do corte de 10 s.
- **Depois do golpe**: os pontos da v2, 3,3 s depois.
  - O acento do passo 2 vai de 40,5 a 41,0.
  - A descida do fim do vídeo dela vai de 45,7 a 46,5.
  - O relaxamento vai de 46,5 a 47,3.
- **O leito (depois do relaxamento)**: calculado como na v2, para a trilha ficar em -30,5 LUFS sob as falas que estão sobre a música cheia (9, 10, 11 e 12). Deu 0,0362 (-28,8 dB). É 1 dB abaixo da v2, porque a fala 12 cai sobre o acorde mais forte (a resolução).
  - Por fala: 9 em -29,6 · 10 em -30,3 · 11 em -34,1 · 12 em -28,9 LUFS.
- **O "realce" de s11 saiu.** Na v3 não há mais silêncio longo em s11: as falas 11, 12 e 13 quase emendam. No único silêncio que sobrou (66,4–67,65, o cartão descendo), a música já está acabando sozinha. Ali 3 dB não se ouviriam. Ele continua no PLANO com `'db': 0.0`, para ligar de novo se quiser.
- **Sob a CTA (fala 14) não sobra música.** A faixa acaba sozinha (-60 LUFS em s12, inaudível). Isso acontece porque o golpe ficou 3,3 s mais tarde e o episódio ficou 7,7 s mais longo. Na v2 o cartão final ainda tinha a cauda da música (-39 LUFS). Em s12 ficam a voz e o toque da pílula, como pede o plano.

## Os ambientes

- **Noite** (0–25,9): o mesmo leito da v2, com 8 cópias da gravação e o mesmo ganho.
- **Recepção** (46,7–58,5): o mesmo arquivo, filtro e ganho da v2. **Decisão minha:** o pedido dizia "de 46,7 até 53,5" (só s09). Mas s10 também se passa na recepção (usa a foto `recepcao-tarde-desfocada.jpg`), e na v2 esse ambiente ia de s09 até o corte para s11. Mantive como na v2: até 58,5, o corte para s11. Como o arquivo tem só 8,5 s úteis, ele é repetido 1 vez, com cruzamento de 0,5 s em 54,7. Para voltar ao pedido literal, basta trocar `'fim_ep': 58.5` por `53.5` no PLANO.
- **Consultório à tarde** (58,5–67,4): o mesmo arquivo, filtro e ganho da v2. O arquivo não cobre 8,9 s, então ele é repetido 1 vez, com cruzamento de 0,5 s em 64,75 (cada cópia usa 0,45–7,2 s do arquivo, sem a subida lenta do começo e sem a descida do fim).
- Os três ficam no mesmo nível baixo: -39,7 / -38,3 / -40,2 LUFS no mix.

## Medições do arquivo final

| Medida | Valor |
|---|---|
| Volume percebido (LUFS integrado) | **-15,8 LUFS** (meta: -15 a -14; ver "Pontos a decidir") |
| Pico real | **-1,2 dBTP** |
| Golpe | **33,933 s** (quadro 1018) |
| Voz, em cada fala | -19,4 LUFS (todas iguais) |
| Trilha sob a voz | -31,3 LUFS (**11,9 dB abaixo da voz**) |
| Efeitos sob a voz | -38,7 LUFS |
| Ganho fixo final | +12,32 dB (o mesmo da v2 e do corte; quem limita é "cada linha...") |
| Limitador | só trilha + efeitos, só de 33,913 a 46,7 s: no máximo 2,9 dB |
| Volume por cena | s01 -19,3 · s03 -19,4 · s04 -18,9 · s04b -21,2 · s05 -21,2 · virada -21,1 · s08 -11,8 · s09 -25,3 · s10 -23,6 · s11 -19,7 · s12 -19,3 |
| Estalos | nenhum nas emendas (3,55 · 18,3 · 25,9 · 46,5 · 46,7 · 54,7 · 58,5 · 64,75 · 67,4 · 71,7) |

## O tempo de cada palavra (`voz-v3.palavras.json`)

Para cada fala, o arquivo traz:
- `id`, `texto`, `comeca` e `termina` (o som real da fala);
- `palavras`: cada palavra com `inicio` e `fim`, em segundos do episódio.

Como foi feito:
- O Whisper de cada tomada (`narracao-amedeiros-v4-a.palavras.json`, `narracao-v3-novas-a/b/c.palavras.json`) é levado pelo deslocamento exato do recorte de cada fala.
- A 1ª palavra começa no começo real do som e a última termina no fim real.
- Onde há um silêncio de 0,10 s ou mais dentro da fala, a fronteira entre as palavras vai para ele.
- Nas falas **T** e **14**, que comandam a imagem (o lettering de s04b e a pílula de s12), as fronteiras foram **medidas no som**, palavra por palavra. Nelas o Whisper marcava 0,1–0,3 s antes.
- Sem dica, o Whisper escreve "47". As palavras "quarenta", "e" e "sete" vêm de uma 2ª passada dele, com a frase como dica.

**Conferência:** transcrevi de novo só a voz já posicionada (sem música), fala por fala:
- todas as 16 falas saem com todas as palavras;
- ele escreve "47" na F e "para a" na 10, que é o jeito dele escrever "pra";
- nas palavras do meio, a diferença média para o arquivo é de -0,05 s (0,06 s em módulo);
- as diferenças maiores (até 0,32 s) são exatamente onde o arquivo seguiu o som e o Whisper não: depois de pausas e nas falas T e 14.

## Pontos a decidir / avisos

1. **O volume total ficou em -15,8 LUFS, não em -15 a -14.** A voz já está no máximo sem limitador. O episódio tem mais fala que a v2 (-15,3), e por isso o trecho alto (o vídeo dela) pesa menos na média. Subir mais só seria possível baixando "cada linha..." e "décima quarta tentativa." (aí a virada deixa de ser igual ao corte aprovado) ou limitando a voz (contra a regra).
2. **Lettering de s04b**: a cena usa os tempos estimados do plano ("isso" em 0,95, "mudar" em 2,25). Os tempos reais da voz (tempo de s04b) são:
   - "mas" 0,30;
   - "isso" 0,58;
   - "está" 0,90;
   - "prestes" 1,31;
   - "a" 1,73;
   - "mudar…" 1,81, terminando em 2,21.
   Do jeito que está, as palavras entram 0,3–0,45 s depois da voz. Quem cuida de s04b deve usar o `voz-v3.palavras.json`.
3. **Pílula de s12**: a cena faz a pílula saltar em 68,20 (o plano), mas "clínica" começa em **68,00**, e "e a gente te mostra como" em 68,54. Se a pílula for para 68,00, o toque (`no_ep` 68.2 no PLANO) deve ir junto.
4. **Recepção até 58,5** (e não 53,5): ver "Os ambientes" acima.
5. **Sem música sob a CTA**: ver "As escolhas da trilha".

## Como refazer

Dentro da pasta do episódio:

```
python -I fonte/audio/montar-v3.py
```

- O script refaz `mix-v3.wav`, `audio-v3.json` e `voz-v3.palavras.json`.
- No terminal, ele mostra o LUFS e o pico, onde caiu o golpe, cada fala, a trilha por trecho e o teste de subtração.
- Para conferir as palavras com o Whisper, rode com `--voz-sozinha <arquivo.wav>`: ele grava também só a voz já posicionada.
- Para mudar alguma coisa, mexa no `PLANO`. É igual à v2, mais quatro blocos:
  - `suspense` (a descida de s04b);
  - `leitos` (os ambientes contínuos);
  - `escolha_das_tomadas`;
  - `fronteiras_medidas`.

## Créditos do ElevenLabs gastos na v3 (12/11/2026)

| Geração | Créditos |
|---|---|
| Falas novas, 3 tomadas (a, b, c) × 235 | 705 (US$ 0,14) |

Nenhum efeito e nenhuma trilha nova: os sons novos reaproveitam tomadas que já existiam (sopro-grave-c, toque-vidro-c, tique-contador-a/b). Somando tudo do ep. 01 até agora: **5.316 créditos (~US$ 1,06)**. Os detalhes estão em `geracoes-elevenlabs.json`, em `narracao_v3_novas`.

---

# v3 — o fim emendado e o toque da pílula (12/11/2026)

Dois ajustes, e só eles. Quem monta continua sendo `fonte\audio\montar-v3.py` (rode `python -I fonte/audio/montar-v3.py`).

Antes de mexer, guardei uma cópia do mix anterior em `fonte\audio\referencia-mix-v3-antes-do-fim.wav`, para comparar.

## 1. O toque da pílula "CLÍNICA": 68,20 → 68,00 s

A pílula do cartão final agora salta em 68,00 s, junto com a palavra "clínica" (que começa em ~68,00-68,03 no som). O toque foi junto: no PLANO, `no_ep` passou de 68.2 para **68.0**. Mesmo som (toque-vidro-c), mesmo volume (-38 de pico). Isso responde ao ponto 3 dos "Pontos a decidir" da v3.

## 2. Música sob o fechamento e a CTA (a única emenda da trilha)

**O problema.** A trilha B resolve (volta ao acorde de lá menor) em 60,61 s e depois some sozinha. Com o episódio de 71,7 s, a chamada "comente CLÍNICA e a gente te mostra como" (67,65-69,85) e o cartão final (66,9-71,7) ficavam quase sem música, e de ~70,2 s até o fim era silêncio total. O dono pediu um fechamento mais comercial, e uma CTA no vazio fica pobre. Isso responde ao ponto 5 dos "Pontos a decidir" da v3.

**A solução: uma emenda só, no fim, alinhada no compasso.** "Emenda" é juntar dois pedaços de música; aqui, dois pedaços da **mesma** trilha.
- Em **61,029-61,446 s** do episódio, a trilha passa (cruzamento de 0,42 s) para uma **2ª cópia da mesma trilha, 2 compassos atrás** (6,6685 s; a música tem 72 batidas por minuto, e um compasso dura 3,33 s).
- Na 1ª cópia, isso é o trecho 63,773-64,190 s do arquivo `trilha-tema-b.mp3`. Na 2ª, é o 57,105-57,521 s. Na 2ª cópia, tempo da música = tempo do episódio - 3,9245 s.
- O "cruzamento de potência igual" é uma troca suave: uma cópia desce enquanto a outra sobe, de um jeito que o volume total não afunda nem incha no meio.
- A 2ª cópia repete os dois compassos que vêm antes da resolução: **dó** (até 63,95 s, sob "se você explica isso todo dia no consultório,") e **sol** (63,95-67,28, a tensão, sob "o seu também já existe").
- Ela resolve de novo em lá menor em **67,275 s**, entre o cartão chegando (66,9-67,5) e "comente" (67,65).
- Depois vem a cauda natural da própria música: o acorde vai sumindo, com as duas notas de piano em **69,78 s** (no "como") e **70,61 s** (logo depois da fala). Ela termina com um fade de 0,5 s (71,2-71,7), que chega a zero exatamente em 71,7.
- Nada foi esticado e nenhuma música nova entrou. A batida continua no lugar: os ataques das duas cópias caem juntos na emenda, com diferença de até 7-14 ms.

**Por que 2 compassos e por que ali.** O cromagrama mostra quais notas soam em cada instante. Comparei as notas da 1ª cópia (o lá menor da resolução) com as da 2ª cópia, semicolcheia a semicolcheia (uma semicolcheia é 1/4 de batida, 0,21 s). A semelhança vai de 0 a 1:

| 2ª cópia | 60,61 | 60,81 | 61,02 | 61,23 | 61,43 s |
|---|---|---|---|---|---|
| **2 compassos atrás (dó) — escolhida** | 0,88 | 0,91 | 0,91 | 0,88 | 0,86 |
| 3 compassos atrás (fá) | 0,83 | 0,73 | 0,73 | 0,70 | 0,65 |
| 1 compasso atrás (sol) | 0,60 | 0,47 | 0,45 | 0,49 | 0,49 |

- Lá menor e dó têm duas notas em comum (dó e mi). Por isso a passagem não "desafina".
- Com 3 compassos, a resolução cairia em 70,6 s, depois da CTA. Com 1 compasso, ela cairia em 63,95 s, sob a fala 13, e a CTA ficaria de novo sobre a música sumindo.
- O cruzamento vai da 3ª semicolcheia do tempo 1 até o tempo 2 do compasso da resolução. É onde as notas mais combinam e as duas cópias têm quase o mesmo volume (diferença de 1,2 dB). Ele fica sob o fim de "papel" (a fala 12 termina em 61,544), e a voz esconde a passagem.
- As duas formas de onda quase não se parecem ali (correlação 0,04). É por isso que o cruzamento usa potência igual.

**Os níveis depois da emenda** (em dB somados ao leito da trilha; as mudanças são curvas suaves):

| Trecho | Volume | Trilha (LUFS) |
|---|---|---|
| fala 13 (62,10-66,38) | +2 dB (a parte de dó/sol da trilha é um pouco mais baixa) | **-30,7** |
| vão entre 13 e 14, com o cartão e a resolução (66,38-67,65) | +3 dB (realce suave) | -27,1 |
| fala 14, a CTA (67,65-69,85) | sobe devagar de +3 a +6, acompanhando a cauda que some | **-30,3** |
| depois da CTA (69,85-71,2) | +8 dB (realce suave para a 2ª nota de piano) | -34,0 (com o fade) |
| 71,2-71,7 | fade até zero | |

As outras falas da v3 ficam entre -28,9 e -34,1 (o leito é -30,5). Sob as falas 13 e 14, a trilha fica ~11 dB abaixo da voz (-19,4), com o mesmo recorte de médias (1-4 kHz, -4 dB) que o script já faz sob toda fala.

**O que NÃO mudou (regras do script):**
- A voz não mudou nada: os mesmos trechos, ganhos e tempos. O `voz-v3.palavras.json` saiu idêntico, byte a byte.
- O ganho fixo final é o mesmo: **+12,32 dB**. Quem limita continua sendo "cada linha..." (pico em 26,954 s).
- O leito da trilha continua -28,82 dB (fator 0,0362). Ele é calibrado **sem** a emenda (só a 1ª cópia, sem a curva do fim). Assim, nada antes da emenda muda.
- O script para com erro se algum pico depois da emenda passar a decidir o ganho final.
- O limitador continua só na trilha e nos efeitos, só de 33,9 a 46,7 s (no máximo 2,9 dB).
- O pico real continua em -1,2 dBTP. Nada de limitador na voz.

## Conferência (no arquivo final)

- **Teste de subtração** contra `referencia-mix-v3-antes-do-fim.wav` (tirar um arquivo do outro e medir o que sobra): de 0 a 61,029 s, a diferença é **zero**. As amostras são idênticas, ou seja, -300 dBFS, abaixo dos -120 pedidos. A primeira amostra diferente é a 2.929.393 (61,0290 s), o começo exato do cruzamento.
- Tirando a voz da diferença, não sobra nada dela (coeficiente 0,001, quando 1 seria a voz inteira). A voz é a mesma.
- **Notas**, pelo cromagrama da trilha no mix:
  - sol (57,3-60,6);
  - lá menor (60,6-61,0);
  - dó (61,45-63,95);
  - sol (63,95-67,28);
  - lá menor (67,28 em diante).
- Sem estalo: o maior salto de agudos (acima de 8 kHz) no cruzamento é de 3,2 dB em 2 ms. É menor que o de um trecho comum da música (4,7 dB).
- O arquivo tem 71,7 s exatos (3.441.600 amostras), e a última amostra é zero.

## Medições (ffmpeg ebur128)

| | Antes | Depois |
|---|---|---|
| Volume integrado | -15,8 LUFS | **-15,9 LUFS** (o fim, mais baixo que a média, entra na conta) |
| Pico real | -1,2 dBTP | **-1,2 dBTP** |
| LRA | 12,5 LU | 12,2 LU |
| Trilha sob a voz (todas as falas) | -31,3 LUFS (11,9 dB abaixo) | -30,9 LUFS (11,5 dB abaixo) |
| s12 (cartão), o mix inteiro | -19,3 LUFS | -20,1 LUFS |
| Trilha + efeitos no cartão (66,9-71,7) | -46,7 LUFS | **-29,9 LUFS** |

Volume a cada 0,5 s (RMS em dBFS; antes de 61,0 s é tudo idêntico):

| Trecho | Mix antes | Mix depois | Trilha+efeitos antes | Trilha+efeitos depois |
|---|---|---|---|---|
| 61,0-61,5 | -24,4 | -24,5 | -31,4 | -31,6 |
| 61,5-62,0 | -34,0 | -34,4 | -34,3 | -34,7 |
| 62,0-62,5 | -19,8 | -19,8 | -37,0 | -34,6 |
| 62,5-63,0 | -21,7 | -21,6 | -38,8 | -35,2 |
| 63,0-63,5 | -21,1 | -20,9 | -39,8 | -33,1 |
| 63,5-64,0 | -22,0 | -21,8 | -39,9 | -32,6 |
| 64,0-64,5 | -24,3 | -23,1 | -40,2 | -28,7 |
| 64,5-65,0 | -26,0 | -24,8 | -41,5 | -30,5 |
| 65,0-65,5 | -21,6 | -21,3 | -41,9 | -32,7 |
| 65,5-66,0 | -21,1 | -20,8 | -41,3 | -34,1 |
| 66,0-66,5 | -32,3 | -30,0 | -42,4 | -33,4 |
| 66,5-67,0 | -42,5 | -29,3 | -42,5 | -29,3 |
| 67,0-67,5 | -47,6 | -27,7 | -47,6 | -27,7 |
| 67,5-68,0 | -19,6 | -18,8 | -60,3 | -27,5 |
| 68,0-68,5 | -20,6 | -20,2 | -46,6 | -30,0 |
| 68,5-69,0 | -21,7 | -21,4 | -64,4 | -32,7 |
| 69,0-69,5 | -26,2 | -25,6 | -67,7 | -35,1 |
| 69,5-70,0 | -34,3 | -31,9 | -69,9 | -36,1 |
| 70,0-70,5 | -71,7 | -37,3 | -71,7 | -37,3 |
| 70,5-71,0 | -76,2 | -34,0 | -76,2 | -34,0 |
| 71,0-71,5 | -85,0 | -40,1 | -85,0 | -40,1 |
| 71,5-71,7 | -105,9 | -61,9 | -105,9 | -61,9 |

## Para mexer

Tudo da emenda fica em `PLANO['trilha']['emenda_fim']`:
- `atraso_s`: quantos compassos atrás (6,6685 s = 2 compassos; não mude sem refazer o cromagrama);
- `cruzamento`: onde a troca começa e termina, em segundos do episódio;
- `volume_db`: a curva de volume depois da emenda, em dB somados ao leito;
- `fade`: o fade final.

É a única emenda de música do episódio (regra no topo do script).

**Falta ouvir:** os números estão certos, mas ninguém ouviu ainda. Confira na prévia, principalmente a passagem em 61,0-61,5 (sob "papel") e se o realce de +8 dB depois da CTA não ficou alto ou baixo demais.

---

# Episódio v4 (0 a 71,7 s): duas falas trocadas (2º pedido do dono, 12/11/2026)

No som, a v4 muda **só a voz de duas falas** (pedidos 4 e 9 do `fonte\PLANO-v4.md`). Todo o resto é o mix da v3.

- Arquivo final: `assets\audio\mix-v4.wav` (WAV de 48 kHz, estéreo, 24 bits, 71,7 s exatos = 3.441.600 amostras). O `index.html` agora toca este arquivo.
- Quem o monta: `fonte\audio\montar-v4.py` (cópia do `montar-v3.py` com as duas falas novas).
- Os números de tudo: `assets\audio\audio-v4.json`.
- O tempo de cada palavra: `assets\audio\voz-v4.palavras.json`.
- A v3 não mudou: `montar-v3.py`, `mix-v3.wav`, `audio-v3.json` e `voz-v3.palavras.json` continuam iguais (conferido byte a byte).

## As duas falas novas

| id | Antes (v3) | Agora (v4) | Tomada | No mix (começa–termina) | Ganho da fala |
|---|---|---|---|---|---|
| F | quarenta e sete dias sem postar nada. (15,550–18,046) | **dezessete dias sem postar nada.** | nova v4 **c** | 15,550–17,982 | -6,70 dB |
| 10 | ela mandou o vídeo pra turma. (53,800–55,056) | **ela mandou o vídeo pra Lúcia.** | nova v4 **a** | 53,800–55,170 | -9,29 dB |

- As duas começam no tempo pedido (15,55 e 53,80). Nenhuma fala deslizou.
- A F ficou 0,064 s mais curta que a antiga. A 10 ficou 0,114 s mais longa, porque "Lú-ci-a" tem uma sílaba a mais que "tur-ma".
- Nada foi esticado nem emendado. Cada fala tem um ganho fixo, que deixa o volume igual ao das outras (-19,4 LUFS).
- **Os cortes ficam no ponto mais silencioso das pausas.** O "silêncio" ali é o chiado de fundo do arquivo, -91 dBFS.
  - F: de 0 até 2,775 s da tomada c. Antes de "dezessete" a tomada tem 0,036 s de silêncio. O 2,775 fica na pausa entre "nada." e "ela" (2,468–2,842).
  - 10: de 2,869 s até 4,463 s da tomada a. O 2,869 fica na pausa entre "nada." e "ela" (2,498–2,918). O 4,463 fica no silêncio do fim (a fala termina em 4,288).
  - A pausa entre "nada." e "ela" não é tão curta: tem de 0,37 a 0,42 s nas 3 tomadas.

## Como as tomadas foram escolhidas (medido, não ouvido)

O ElevenLabs gerou 3 tomadas, cada uma com as duas frases: `narracao-v4-novas-a/b/c.mp3`. Para cada fala, comparei as 3 tomadas em quatro coisas:

- **altura média da voz**: medida pelo Praat, como a diferença em semitons para a tomada A (um semitom é a menor distância entre duas notas do piano);
- **ritmo**: quantas sílabas por segundo;
- **PLR**: o pico em relação ao volume;
- **transcrição**: o Whisper confere se todas as palavras saíram.

A nota soma a diferença de altura e a diferença de ritmo (10 % de ritmo pesa como 1 semitom). Menor é melhor.

Uma mudança em relação à v3: o ritmo agora é comparado com o da **fala aprovada que a nova substitui**, no mesmo lugar. A v3 comparava com a média da tomada A. A fala 10 antiga já era lida rápido (8,76 sílabas por segundo), então ali "mais devagar" não quer dizer "mais parecida". A nota pela conta da v3 também está no `audio-v4.json`.

| Fala | Tomada | Altura (semitons acima da tomada A) | Ritmo (sílabas/s) | PLR | Duração | Nota |
|---|---|---|---|---|---|---|
| F | a | +1,50 | 4,42 | 13,9 dB | 2,488 s | 3,01 |
| F | b | +0,18 | 4,37 | 14,0 dB | 2,520 s | 1,80 |
| F | **c (escolhida)** | +0,42 | 4,52 | 12,8 dB | 2,432 s | **1,74** |
| F | antiga (v3) | +0,23 | 5,21 | 15,5 dB | 2,496 s | |
| 10 | **a (escolhida)** | +1,18 | 8,76 | 14,8 dB | 1,370 s | **1,18** |
| 10 | b | +1,92 | 8,67 | 15,6 dB | 1,384 s | 2,02 |
| 10 | c | +1,68 | 8,36 | 13,4 dB | 1,436 s | 2,14 |
| 10 | antiga (tomada A) | +2,81 | 8,76 | 13,6 dB | 1,256 s | |

- **F: tomada c.** A b e a c praticamente empatam. A c desempata por dois motivos:
  - é a única com silêncio de verdade antes de "dezessete", então o corte do começo cai numa pausa, como manda a regra (a b já começa soando na primeira amostra do arquivo);
  - tem o menor pico em relação ao volume.

  As 3 tomadas leem a frase um pouco mais devagar que a antiga ("dezessete" tem 4 sílabas), mas a duração quase não muda.
- **10: tomada a.** Tem a altura mais perto da tomada A, o mesmo ritmo da fala aprovada (8,76 contra 8,76) e a duração mais perto dela. Pela conta da v3, a c ficaria 0,1 à frente, só por ser mais lenta.
- O PLR de todas fica bem abaixo dos 18,2 dB de "cada linha...". Por isso o ganho final não muda.
- **Sobre a altura:** do jeito que eu rodei, o Praat dá 1 a 2 Hz a mais que os números da v3 (a tomada A dá 125,2 Hz, e não 123,8). Por isso medi de novo, com o mesmo método, as tomadas novas, as falas antigas e a referência. O ritmo e o PLR saem iguais aos da v3 (conferido na F antiga: 5,21 e 15,54).
- **Transcrição:** as 3 tomadas saíram completas (`fonte\audio\narracao-v4-novas-a/b/c.palavras.json`).
  - Sem dica, o Whisper escreve "17" para "dezessete". As palavras "dezessete" e "dias" vêm de uma 2ª passada dele, com a frase como dica, como na v3.
  - Nas tomadas, ele escreve "para a" onde a voz diz "pra". É o jeito dele escrever. No `voz-v4.palavras.json` fica "pra".

## O que ficou igual à v3 (conferido no arquivo)

- **Teste de subtração contra o `mix-v3.wav`** (tirar um arquivo do outro e medir o que sobra). Fora das janelas das duas falas, a diferença é **zero**: as amostras são idênticas (-300 dBFS).
  - As janelas são 15,15–18,446 s (F) e 53,40–55,57 s (10), já com uma folga de 0,05 s de cada lado.
  - As amostras só diferem em 15,514–18,361 s e em 53,633–55,520 s.
- **O leito da trilha (o volume dela depois de 46,5 s) ficou congelado no valor exato da v3** (-28,8211 dB).
  - Na v3, ele era calibrado pelas falas 9, 10, 11 e 12. Com a fala 10 nova, recalcular mudaria um pouquinho a música de 46,5 s até o fim.
  - Com o leito congelado, a trilha sob essas 4 falas mede -30,57 LUFS. O alvo da v3 era -30,5.
- **O recorte de médias** (a trilha abre espaço para a voz: -4 dB entre 1 e 4 kHz) acompanha a fala, então mudou um pouco:
  - sob a F, termina 0,064 s antes (18,182 em vez de 18,246). Só na trilha, a diferença nessa janela é de -89,5 dBFS em média (no máximo -62);
  - sob a 10, termina 0,114 s depois (55,370 em vez de 55,256). Só na trilha, a diferença é de -75,1 dBFS em média (no máximo -51). Debaixo da voz, isso não se ouve;
  - a trilha sob a F fica em -29,9 LUFS (igual à v3). Sob a 10, fica em -30,6 LUFS (v3: -30,3), porque o trecho medido agora é 0,11 s mais longo.
- **O ganho fixo final é o mesmo: +12,32 dB**, idêntico até a última casa. Quem limita continua sendo "cada linha..." (pico em 26,954 s). O script para com erro se uma fala nova passar a decidir isso.
- **A virada continua igual ao corte de 10 s**: -120,1 dBFS no teste de subtração, o mesmo número da v3.
- **As outras 14 falas do `voz-v4.palavras.json` são idênticas às do `voz-v3.palavras.json`.** O script confere isso e para se não forem.
- **Sem estalo nos cortes.** Na voz sozinha, os 15 ms em volta de cada começo e fim de recorte ficam entre -85 e -91 dBFS. É o chiado de fundo da tomada, já com o ganho.
- **Conferência com o Whisper**: transcrevi de novo só a voz já posicionada.
  - As duas falas saem com todas as palavras. Aqui ele escreve "pra", e "dezessete" só sai por extenso com a dica.
  - Nas palavras do meio, a diferença para o arquivo é de -0,01 a +0,08 s.

## Medições (ffmpeg ebur128)

| | v3 | v4 |
|---|---|---|
| Volume integrado | -15,9 LUFS | **-15,9 LUFS** |
| Pico real | -1,2 dBTP | **-1,2 dBTP** |
| LRA (o quanto o volume varia) | 12,2 LU | 12,1 LU |
| Voz, em cada fala | -19,4 LUFS | -19,4 LUFS |
| Pico real das falas F / 10 no mix | -3,87 / -5,83 dBTP | -6,61 / -4,60 dBTP |
| Trilha sob a voz (todas as falas) | -31,2 LUFS | -31,2 LUFS |
| Mix inteiro de s04 / s10 | -18,9 / -23,6 LUFS | -19,3 / -22,8 LUFS |

## O tempo de cada palavra das falas novas (`voz-v4.palavras.json`, segundos do episódio)

- **F** (15,550–17,982): dezessete 15,550 · dias 16,174 · sem 16,534 · postar 16,814 · nada. 17,254–17,982
- **10** (53,800–55,170): ela 53,800 · mandou 53,930 · o 54,182 · vídeo 54,242 · pra 54,482 · Lúcia. 54,722–55,170

O método é o mesmo da v3: o Whisper, mais os silêncios. Nas palavras do meio, ele costuma marcar ~0,1 s antes do som.

## Como refazer

Dentro da pasta do episódio:

```
python -I fonte/audio/montar-v4.py
```

- O script refaz `mix-v4.wav`, `audio-v4.json` e `voz-v4.palavras.json`, e mostra os testes no terminal.
- Ele para com erro em três casos:
  - se algo fora de F e 10 ficar diferente do mix-v3;
  - se o ganho final mudar;
  - se uma das outras falas sair diferente no `voz-v4.palavras.json`.

## Créditos do ElevenLabs gastos na v4 (12/11/2026)

| Geração | Créditos |
|---|---|
| Falas F e 10, 3 tomadas (a, b, c) × 62 | 186 (~US$ 0,04) |

Somando tudo do ep. 01: **5.502 créditos (~US$ 1,10)**. As tomadas já existiam quando o áudio foi montado: na montagem, nada foi gerado. Os detalhes estão em `geracoes-elevenlabs.json`, em `narracao_v4_novas`.

**Falta ouvir:** os números estão certos, mas ninguém ouviu ainda. Na prévia, confira principalmente as duas falas novas (15,5–18,0 e 53,8–55,2).
