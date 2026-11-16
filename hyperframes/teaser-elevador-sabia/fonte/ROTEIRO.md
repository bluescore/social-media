# Teaser "e nós queremos subir" — roteiro

Referências (em `referencias\`):
- `ref-janelas.mp4`: fachada azul-escura à noite, janelas piscando em vermelho em grupos, trilha ambiente com graves.
- `ref-elevador.mp4`: close fixo do botão de subir do elevador, a mão aperta e o anel acende; textos sobre fundo preto
  com o "plim" do elevador chegando.

Versão Sabiá: janelas no **laranja da paleta**; a câmera se aproxima até entrar pela única janela que fica acesa; lá
dentro, o detalhe da mão chamando o elevador e o homem esperando; fecha em preto com "em breve" e **"16.11" — só a
data, sem logo** (pedido do dono, 2026-11-09).

Vertical 1080×1920, 30 fps, 17 s.

## Tipografia (regras do dono, 2026-11-09 — valem para todas as peças)

- **Helvetica Now Text**: Regular no texto comum, **Bold só no destaque** ("evolui", "identidade", "16.11").
- Espaçamento entre letras **-50** (`letter-spacing: -0.05em`) e entrelinha **0.9**.
- **Minúsculas** (maiúscula só em nomes próprios).
- **Megion Bold** só para destacar **uma palavra sozinha, em CAIXA ALTA** ("SUBIR").
- Todo texto de apoio com o mesmo tamanho: **76 px**.
- (Regra geral da marca, não usada aqui: quando houver logo no final, sem o LAB e slogan sem ponto.)

## Linha do tempo (cortada na trilha3: 100 BPM, crescendo do quase silêncio até UM impacto na data)

Batidas medidas (ataques): 0,447 / 1,055 / 1,654 / 2,262 / 2,853 / 3,454 / 4,058 / 4,659 / 5,254 / … / 14,833 s
(compassos a cada 4 batidas). Eventos no quadro (30 q/s) mais próximo.

| Tempo | Cena | O que acontece |
|---|---|---|
| 0–5,25 s | Fachada | zoom lento (~7% por segundo); poucas janelas piscando na batida, uma rajada no 2º compasso; "quando a forma de pensar **evolui**" à direita (1,07 s; o destaque cai na batida seguinte); "a **identidade** acompanha" à esquerda (4,07 s) |
| 5,25 s | Fachada | início do 3º compasso: só uma janela acesa |
| 5,25–7,67 s | Mergulho | a câmera acelera até um vidro da janela acesa ocupar a tela; a luz laranja da cortina toma a tela |
| 7,67 s | Passagem | início do 4º compasso: a luz se abre no detalhe do botão (sem impacto: a trilha só cresce) |
| 7,53–10,07 s | Botão | detalhe como a referência: a mão JÁ EM MOVIMENTO chega, aperta, e o botão acende em laranja na batida de 8,267 s (com o clique) |
| 10,07–13,07 s | Espera | início do 5º compasso; o homem de costas, botão aceso ao lado; "e nós queremos" (10,67 s) e **SUBIR** (11,87 s) centralizados |
| 13,07–14,8 s | Preto | "em breve", com o elevador subindo (tics de andar) e o riser da trilha |
| 14,833–17 s | Data | **"16.11"** junto com o ÚNICO impacto da trilha e o "plim"; fica parada e apaga no fim, com o eco |

## Como as imagens são feitas

1. `q1-v1.png` (fachada apagada, Nano Banana Pro 4k) e `q1-acesa-v1.png` (a mesma com ~100 janelas acesas).
2. `python -I fonte\janelas.py` separa a luz de cada janela, escurece a fachada e recorta a região da janela-alvo.
3. `q2-v1.png` (o recorte refeito em alta resolução); `python -I fonte\alinhar.py` encaixa e iguala a cor.
4. `python -I fonte\montar-janelas.py` escreve as janelas em `compositions\fachada.html`.
5. Elevador: quadros `q5-botao-c.png` e `q6-espera-a.png` (Nano Banana Pro, com o hall `q4-v1.png` de referência),
   animados no Kling 4.0 (`clipes\c5-botao-v1.mp4`, `clipes\c6-espera-v1.mp4`).
6. `python -I fonte\corrigir-clipes.py`: luz do botão no laranja #F34500, imagem do close mais escura e fria, tempo do
   aperto (a mão em movimento desde o 1º quadro — câmera lenta no começo parecia "pausado"), o mesmo desenho de botão
   nas duas cenas, e 30 quadros/s sem trancos → `assets\video\botao.mp4` e `espera.mp4`.

O hall aberto (`q4-v1.png` / `c4-v1.mp4`) do teste de 8 s foi substituído pelo detalhe, a pedido do dono.

## Sons (`audio\` → `assets\audio\`)

- Trilha: `trilha3.mp3`, montada por `python -I fonte\montar-trilha3.py` a partir de um candidato do ElevenLabs Music:
  nasce do silêncio, cresce +18 dB sem quedas, riser durante "em breve" e UM impacto em 14,833 s (a data), com cauda.
  A trilha anterior (`trilha2*`, com bumbo desde o início e impacto na janela) foi reprovada pelo dono: "pesada desde o início".
- Efeitos: cidade à noite (`cidade2.mp3`, sem o carro alto do começo e subindo junto), sopro até a janela, clique do
  botão, ambiente do hall (`hall2.mp3`), elevador subindo (`chegada2.mp3`) e o "plim" na data.
- Volume final: `python -I fonte\normalizar-audio.py <bruto.mp4> <final.mp4>` — ganho fixo, limitado pelo pico do
  impacto (o vídeo fica em ~-21 LUFS porque começa quase em silêncio; subir mais achataria o impacto).

## Narração (2026-11-11)

Voz: **Yago-Voice** (voz clonada do dono no Higgsfield, id `af270031-c3d6-4d9a-9f1f-6c4ac3d98bbb`, tipo element).
Texto: "Quando a forma de pensar evolui... a identidade acompanha. E nós queremos... subir. Em breve. Dezesseis de novembro."
Foram geradas tomadas em 3 motores (`fonte/audio/narracao-elevenlabs-v1.mp3`, `narracao-minimax-v2.mp3`,
`narracao-qwen-v2.wav`; comparação em `fonte/audio/narracao-comparacao.mp3`). No vídeo está a **Qwen** (a única em
que todas as falas cabem nos tempos dos textos). Para trocar: em `fonte/narracao.json` mude `tomada` e os tempos
`de`/`ate` de cada fala (medidos na tomada) e rode `python -I fonte/montar-narracao.py`; depois renderize e rode
`fonte/normalizar-audio.py`.

Regras: a voz nunca é esticada, acelerada, emendada no meio de frase nem limitada — cada fala é recortada nas pausas
da tomada e posicionada no tempo do texto; só leva ganho fixo (`ganho_db` por fala: as primeiras mais baixas, para o
filme continuar começando leve). A música desce só sob a voz; sob "dezesseis de novembro" desce -6 dB em rampa, sem
cortar o eco do impacto; o golpe da data nunca é abaixado. O limitador final age só no instante do impacto.

**Atualização (2026-11-11):** o dono não curtiu a Yago-Voice e pediu a voz **A.Medeiros – Clear, Calm & Friendly**
(biblioteca da ElevenLabs, voice_id `E9hPCbqBRCgB3UEiCUuE`). O Higgsfield não acessa vozes da biblioteca da ElevenLabs;
ela foi gerada pelo conector da ElevenLabs (4 tomadas: `fonte/audio/narracao-amedeiros-v4-a/b.mp3` e `-ml2-a/b.mp3`;
comparação em `fonte/audio/narracao-amedeiros-comparacao.mp3`). No vídeo: v4-a. A configuração anterior (Qwen) ficou em
`fonte/narracao-qwen.json`.

**Final (2026-11-11):** o dono aprovou o v7 (narração A.Medeiros, tomada v4-a). Arquivo final:
`prontos\2026-11-11_teaser-elevador-sabia.mp4` (cópia de `renders\completo-v7.mp4`, já com o volume final: -19,3 LUFS,
pico -1,4 dBTP).
