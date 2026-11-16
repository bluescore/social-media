# Pesquisa — hyperframes-pipeline

## Resumo

1) O HyperFrames faz 3D de verdade: Three.js roda dentro da cena e cada quadro é desenhado a partir do tempo do vídeo. Já há blocos prontos que carregam modelos GLB, usam luz de estúdio e pós-processamento (desfoque de foco e brilho). A versão fixa recomendada é three@0.184.0, a mesma dos blocos do HyperFrames 0.8.216, com gsap@3.14.2.
2) Medi nesta máquina (Ryzen 7 5700, RTX 4060, 32 GB). 3 s de um implante 3D em 1080×1920, com sombras e pós-processamento, renderizaram em 20,5 s. 3 s de uma cena 2.5D com 4 imagens grandes em parallax levaram 18,1 s. Isso dá cerca de 0,1 s por quadro. A estimativa para um episódio é de 4 a 6 min de render para 60 s e de 6 a 9 min para 90 s; com modelos 3D pesados, até uns 15 min.
3) No teste, o parafuso com rosca e o pilar feitos em código ficaram convincentes. A coroa feita em código virou uma "bolha" amadora, o mesmo problema do pássaro em SVG que o dono reprovou. Formas orgânicas (dente, osso, gengiva) devem vir de modelos escaneados. No Sketchfab há modelos gratuitos com licença CC BY 4.0, que pede crédito: dentes da Universidade de Dundee, um dente em corte e uma mandíbula com implante (Ortomesh, 2025). Não achei implante completo em CC0.
4) Personagens: a melhor rota para "nível estúdio" é 2.5D. A doutora vira imagens em estilo 3D de filme feitas pela OpenAI, com uma folha de referência fixa e em camadas sem fundo. Ela ganha câmera, parallax, troca de pose com causa, piscar e respiração. O 3D de verdade fica reservado para o objeto que explica (dente e implante), que é onde mora a profundidade do conteúdo. Personagem 3D genérico (Quaternius, Mixamo) e Lottie tendem a parecer jogo ou desenho chapado.
5) Interface (celular, roteiro digitado, IA "gerando"): o registro já traz blocos verticais e componentes prontos. Evitar os que imitam marcas reais (Claude, ChatGPT, iPhone).
6) Som: dá para repetir quase tudo do teaser do elevador. São a voz A.Medeiros com recorte nas pausas (montar-narracao.py), a trilha em crescendo com UM impacto (montar-trilha3.py) e o ajuste final de volume (normalizar-audio.py). As gerações que antes passavam pelo Higgsfield agora vêm direto do conector ElevenLabs, que tem música, efeitos e voz.
7) Série: um molde próprio (`_serie-clinicas\molde\`) com personagem, cenários, palco 3D, telas de IA, tema musical e scripts de áudio, feito uma vez. Cada episódio é uma cópia (`hyperframes\clinicas-epNN-tema\`) que troca roteiro, narração, a cena 3D do tema e poucas imagens.

## Achados

### 1. 3D de verdade no HyperFrames: como funciona e o que usar

O render é quadro a quadro: o HyperFrames pausa a página e pede cada instante. Por isso a cena 3D tem de ser uma função do tempo: render(t). Isso vale sem loop próprio (requestAnimationFrame), sem Date.now e sem sorteio sem semente.

O padrão testado é o do bloco product-turntable. Um relógio do GSAP (gsap@3.14.2) chama render(t) no onUpdate; outra forma é escutar o evento hf-seek e desenhar com e.detail.time. A preparação pesada (carregar GLB, preparar a luz de ambiente, compilar shaders) entra em window.__hf.buildReady['chave'], e a linha do tempo é registrada no fim.

No WebGLRenderer use preserveDrawingBuffer:true, setPixelRatio(1), saída de cor SRGB e tone mapping ACES.

Versões fixas: three@0.184.0 (é a que os blocos do HyperFrames 0.8.216 usam; o bloco product-turntable usa GLTFLoader, RoomEnvironment e o próprio three nessa versão). A mais nova no jsDelivr hoje (2026-11-11) é 0.187.0, mas não há motivo para sair da testada. Carregue por import map ('three' e 'three/addons/' em cdn.jsdelivr.net/npm/three@0.184.0/...) ou, melhor, copie os arquivos para a pasta do molde, como fazem os blocos cuboid-carousel e orbit-card ('servido localmente'). Assim o render não depende da internet.

Modelos GLB: GLTFLoader.loadAsync('assets/...glb'). Evite compressão Draco, porque o decodificador vem de um CDN do Google no bloco vfx-iphone-device; prefira reduzir os polígonos.

Luz (references/types/3d.md): luz principal quente, contorno frio, ambiente escuro com 2 ou 3 faixas suaves (o RoomEnvironment com faixas emissivas, como no product-turntable) e uma sombra de contato. A sombra de contato pode ser uma textura radial já pronta, com custo zero por quadro. Metal com aspereza (roughness) a partir de ~0,45 e ambiente em ~0,5. Brilho (bloom) só nos pontos mais claros, e é preciso evitar contas que gerem NaN, que apaga o quadro inteiro.

Pós-processamento: os módulos do próprio three (EffectComposer, RenderPass, BokehPass, UnrealBloomPass, SMAAPass, OutputPass) funcionaram no teste com r184. A biblioteca pmndrs/postprocessing (estável 6.39.6, v7 em beta) é opcional.

Orçamento: cada cena WebGL viva consome ~350 MB; uma de cada vez.

Câmera e história (types/3d.md e explainer.md): um objeto herói, mergulhar nele em vez de girar em volta, cortes e vista explodida com uma frase por capítulo. Interface de produto nunca é inclinada em 3D. Textos ficam em HTML por cima do canvas (fonte da marca nítida), não em geometria 3D.

**O que muda para nós:** Para o 'vídeo da doutora' dentro da história dá para fazer 3D real (implante entrando no osso, corte, vista explodida) sem gerador de vídeo. O molde da série deve trazer um 'palco 3D' pronto (renderizador, luz de estúdio, sombra de contato, pós) com three@0.184.0 copiado localmente, para cada episódio só trocar o modelo e a câmera.

Fontes: C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\types\3d.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\runtimes.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\blocks\product-turntable\product-turntable.html · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\blocks\cuboid-carousel\SKILL.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\blocks\canopy-part-title\SKILL.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\blocks\vfx-iphone-device\vfx-iphone-device.html · https://data.jsdelivr.com/v1/packages/npm/three · https://data.jsdelivr.com/v1/packages/npm/postprocessing

### 2. Custo de render medido nesta máquina e estimativa para 60–90 s

Fiz três renders de teste de 3 s (90 quadros, 1080×1920, 30 q/s, qualidade 'looks', hyperframes@0.8.216). O render usou a GPU (hardware gpu) e escolheu 3 processos de captura sozinho.

- Cena 3D: implante com materiais físicos, sombras suaves 2048 e Bokeh + Bloom + SMAA. Total 20,5 s, sendo preparação 9,7 s e captura 8,3 s.
- A mesma cena com data-motion-blur ligado: 15,3 s (captura 8,1 s). O borrão de movimento não custou nada, porque o canvas não se move como elemento.
- Cena 2.5D: 4 imagens grandes (até 7 MB) em parallax, desfoque animado, texto e motion blur. Total 18,1 s (captura 10,1 s).

Resultado: ~0,09 a 0,11 s de captura por quadro.

Extrapolação (não medida no filme inteiro):
- 60 s (1800 quadros): ~3 min de captura, mais preparação, áudio e montagem, o que dá ~4 a 6 min.
- 90 s (2700 quadros): ~6 a 9 min.
- Modelos escaneados pesados (1 a 2 milhões de faces) ou duas cenas WebGL vivas juntas podem dobrar isso: até ~15 min.
- O corte de 10 s leva ~1 min.

Render em 4K custa ~4× mais e 60 q/s, 2×; os dois são inúteis para Reels (docs/guides/rendering.mdx). O --workers pode ser aumentado (cada um abre um Chrome de ~256 MB; a máquina tem 32 GB), mas não medi o ganho.

**O que muda para nós:** O render não é gargalo: dá para gerar várias prévias por dia. O tempo do episódio vai para roteiro, imagens e som, não para a máquina. Reduzir os modelos 3D para menos de ~150 mil faces e manter uma cena WebGL por vez.

Fontes: C:\Users\YAGOBI~1\AppData\Local\Temp\claude\2b384691d2ba5125\ac8f9542-8c29-4427-9d2b-a094d0c2255e\scratchpad\bench3d\index.html · C:\Users\YAGOBI~1\AppData\Local\Temp\claude\2b384691d2ba5125\ac8f9542-8c29-4427-9d2b-a094d0c2255e\scratchpad\bench3d\out-3d.mp4 · C:\Users\YAGOBI~1\AppData\Local\Temp\claude\2b384691d2ba5125\ac8f9542-8c29-4427-9d2b-a094d0c2255e\scratchpad\bench25d\out-25d.mp4 · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes-cli\references\preview-render.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\docs\guides\rendering.mdx

### 3. Dente com implante em Three.js: o que fica bom feito em código e o que precisa de modelo pronto

No teste montei em código um parafuso com rosca e o resto do implante:
- o núcleo do parafuso é um perfil girado (LatheGeometry);
- a rosca é um tubo em hélice;
- o pilar também é um perfil girado;
- a coroa é uma esfera deformada;
- o osso e a gengiva são cilindros, cortados ao meio por um plano de recorte.

Resultado (quadro f29.png):
- O parafuso e o pilar de titânio ficam convincentes e limpos. Peça mecânica é ótima para fazer em código, e as medidas ficam controláveis.
- A coroa vira uma bolha branca, e com o brilho estoura. Forma orgânica feita em código fica amadora.
- O corte por plano mostra o osso oco por dentro. Para corte sólido é preciso o método das 'tampas' com stencil (exemplo oficial webgl_clipping_stencil do three.js) ou um modelo já cortado.
- O osso precisa de textura de osso esponjoso, que dá para pintar num canvas ou num shader de ruído.

Melhor combinação: parafuso e pilar em código (genéricos, sem marca); coroa, dente vizinho, arcada e osso a partir de escaneamentos CC BY reduzidos; corte com tampas stencil; legendas em HTML sobre o 3D. Pelo explainer.md, cada passo do protocolo tem de ser conferido antes de animar: 'um diagrama bonito e errado é pior que nenhum'.

**O que muda para nós:** Dá para fazer com qualidade, desde que as formas orgânicas venham de escaneamentos e o 3D seja tratado como o objeto que explica. O roteiro técnico do episódio precisa ser revisado por um dentista antes da animação.

Fontes: C:\Users\YAGOBI~1\AppData\Local\Temp\claude\2b384691d2ba5125\ac8f9542-8c29-4427-9d2b-a094d0c2255e\scratchpad\bench3d\f29.png · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\types\explainer.md · https://threejs.org/examples/webgl_clipping_stencil.html

### 4. Modelos 3D gratuitos com licença comercial (dente, implante, arcada)

Conferi a licença de cada um pela API do Sketchfab em 2026-11-11. Todos são CC BY 4.0, que permite uso comercial com crédito.

- 'Mandibular First Molar' e 'Permanent Dentition': University of Dundee, School of Dentistry. Esculpidos em zBrush (a dentição a partir de tomografia), ~28 mil e ~30 mil faces. A série de Dundee tem dezenas de dentes isolados (molares superiores e inferiores, incisivos, caninos).
- 'Inside my Tooth' (R-LAB, 2022, ~56 mil faces): dente em corte, com gengiva e vasos em objetos separados.
- 'Model Jaw - implant' (Ortomesh, 2025, ~116 mil faces): mandíbula transparente com implante e nervos.
- 'Implante Dental' (drandrescordova, 2017, ~19 mil faces): implante para identificar as partes.
- 'MSDI dental implants - Conical' (conta do fabricante MSDI, CC BY): é de marca comercial, melhor evitar.
- A busca também listou escaneamentos Thunk3D de arcadas e parafusos com 0,5 a 2,3 milhões de faces (licença marcada como CC BY na lista, mas não conferi um a um). São pesados demais sem reduzir.

No Poly Pizza (estilo low poly, destoa do acabamento premium): 'Dentist Chair' (davis, CC BY 3.0, glTF) e 'Teeth' (Poly by Google, CC BY).

Não encontrei implante completo (coroa, pilar e parafuso) em CC0. Opções pagas ou com licença própria (não CC): Free3D 'tooth dental implant 8751' (royalty free, tem glb; ler os termos) e pacotes no CGTrader (US$ 10 a 50).

Para a série toda: Quaternius 'Universal Base Characters' é CC0 (agosto de 2025, glTF, rig humanoide).

**O que muda para nós:** O episódio piloto pode usar dente e arcada reais e gratuitos, com crédito na legenda do post (por exemplo: 'Modelo 3D: University of Dundee, CC BY 4.0'). Baixar do Sketchfab exige conta logada: quem baixa é o dono, e eu não crio conta nem digito senha. Guardar tudo em uma pasta de modelos com um CREDITOS.md.

Fontes: https://sketchfab.com/3d-models/mandibular-first-molar-e1c919d6603846eca873154eeededdd6 · https://sketchfab.com/3d-models/permanent-dentition-2f69d7b59c3e4a6a8bcae041bd8e591b · https://sketchfab.com/3d-models/inside-my-tooth-5ebeadf0b40940ca93a4ced5cfe0abb2 · https://sketchfab.com/3d-models/model-jaw-implant-173fad1fdf784b5db66ed00010a3a59f · https://sketchfab.com/3d-models/implante-dental-ede1a07475db4236b43a6cd168d1225d · https://sketchfab.com/3d-models/msdi-dental-implants-conical-42cd398aac8b4e3ba06780fd6aa8d2d3 · https://api.sketchfab.com/v3/search?type=models&q=dental%20implant&downloadable=true&count=24 · https://poly.pizza/m/DXhRgoTcP4 · https://poly.pizza/m/eNR_DPPP1Hp · https://free3d.com/3d-model/tooth-dental-implant-8751.html · https://quaternius.com/packs/universalbasecharacters.html

### 5. Personagens sem gerador de vídeo: comparação das três rotas

(a) Imagens de IA em camadas (2.5D): a doutora, o cenário e um objeto de primeiro plano gerados separadamente pela OpenAI, com a personagem sem fundo.
- Movimento: câmera com parallax, desfoque de profundidade animado, troca de pose ou expressão com causa (um 'take' em 4 tempos: antecipa, comprime, rosto novo, assenta, segundo character.md), respiração (escala vertical de ~1%) e piscar em instantes com semente.
- Prós: a imagem já sai com luz e acabamento de 'filme 3D'; custo de centavos por imagem; render leve (medido 0,11 s por quadro).
- Contras: a personagem pode mudar entre gerações (resolve-se com uma folha de referência fixa sempre enviada com --ref); sem sincronia de boca; vira 'slideshow' se as poses só pipocarem.
- Risco de parecer amador: médio, controlável com câmera e cortes com causa.

(b) Personagem 3D no Three.js.
- De primitivas (esferas, cápsulas): risco alto de cara de brinquedo, como a coroa do teste.
- De GLB com rig (Quaternius CC0; animações Mixamo, que permitem uso comercial sem royalties mas não redistribuir os arquivos): dá para tocar a animação quadro a quadro com AnimationMixer.setTime(t). Mas o visual é de jogo genérico, e personalizar uma 'dentista' exige Blender. Ready Player Me fechou em 31/01/2026.
- Risco: alto, para quem está começando.

(c) Lottie: precisa de After Effects. As animações prontas do mercado são chapadas e genéricas (o bloco lottie-character-walk usa lottie-web@5.12.2; o dotLottie fixa @lottiefiles/dotlottie-web 0.81.0 local).
- Risco: muito alto, é o mesmo 'cartunesco' que o dono reprovou.

Recomendação para 'nível estúdio': (a) para pessoas, mais 3D real (item 1) para o objeto da explicação, mais interface de verdade em HTML.

**O que muda para nós:** Escrever a história para que a doutora não precise falar na câmera: a voz é de narrador (A.Medeiros é masculina, então funciona como narrador) e o que ela diz aparece como texto ou chat. As ações dela são poses com motivo, e o movimento contínuo fica no mundo, na interface e no 3D. Fazer a folha de personagem uma vez e reaproveitar em todos os episódios.

Fontes: C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\types\character.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\motion.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\blocks\lottie-character-walk\lottie-character-walk.html · https://quaternius.com/packs/universalbasecharacters.html · https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html · https://en.wikipedia.org/wiki/Ready_Player_Me

### 6. Gerador de imagens da OpenAI já existe no projeto (e o que conferir antes)

C:\social-media\ferramentas\openai\gerar-imagem.mjs é o único caminho de imagem do projeto. Ele já aceita:
- --ref, com várias imagens, para manter a mesma personagem;
- --fundo transparent, para PNG sem fundo;
- --rascunho, com o modelo rápido e barato;
- --tamanho até 3840 no lado maior (múltiplos de 16).
Cada imagem ganha um .json com o pedido e uma linha de custo em registro.csv.

O config.json está com modelo_final 'gpt-image-2.6-sunburst', mas 'modelos_disponiveis' vazio e 'verificado_em' vazio. Ou seja, a chave pode ainda não ter sido cadastrada e testada: o dono roda cadastrar-chave.ps1, e eu nunca vejo a chave.

Fundo transparente: um post da comunidade OpenAI anuncia transparência 'em preview' no gpt-image-2. Não confirmei para a 2.6. Plano B local e grátis: npx hyperframes remove-background foto.png -o recorte.png (modelo u2net_human_seg, feito para pessoas).

Para aproximar a câmera sem perder nitidez, gerar em 2160×3840 ou 1152×2048 conforme o enquadramento.

**O que muda para nós:** O primeiro passo prático da série é o dono cadastrar a chave e eu gerar a folha de personagem em rascunho (barato) para aprovação. Só depois as poses finais.

Fontes: C:\social-media\ferramentas\openai\LEIA-ME.md · C:\social-media\ferramentas\openai\gerar-imagem.mjs · C:\social-media\ferramentas\openai\config.json · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\media-use\audio\references\remove-background.md · https://community.openai.com/t/transparent-backgrounds-are-now-available-in-preview-for-gpt-image-2-in-the-api/1391541

### 7. Mockups de interface prontos no registro (celular, roteiro digitado, IA gerando)

Blocos verticais 1080×1920:
- ai-chat-reveal (19,3 s): pergunta digitada num teclado que sobe, resposta da IA chegando em rajadas;
- message-thread-reveal (25,8 s): conversa inteira num celular;
- notification-cascade (14 s): notificações empilhando.

Componentes para montar nas cenas:
- notes-typing: título e linhas digitadas no ritmo humano. É o 'roteiro da doutora sendo digitado'.
- typed-prompt, typewriter, streaming-text (resposta de IA em rajadas), typing-indicator, chat-thread, chat-message.
- agent-cursor: uma IA operando a tela, com cursor, passos e um 'ok' no fim. É a 'IA montando o motion'.
- skeleton-reveal, conic-progress-ring, success-check: carregando e pronto.
- segmentation-flood: leitura de máquina sobre uma imagem.
- device-frame-stage: celular como objeto de cena com a tela livre.
- parallax-device-dive: o celular sobe e a câmera atravessa a tela até ela ocupar o quadro. É a transição perfeita para 'o seu conteúdo pode sair assim'.
- screen-flow-carousel, modal-morph, zoom-through-transition, iris-reveal, match-cut, whip-pan-cut.

Câmera e acabamento: camera-rig-depth-stack, focus-rack, light-sweep-pass, camera-shake (perfis de câmera na mão, seguros para render), grain-overlay, vignette.

Evitar: claude-exchange e chatgpt-exchange (imitam produtos reais), vfx-iphone-device e ios26-liquid-glass (iPhone real, horizontal, 'experimental', usam a função HTML-in-canvas do Chrome, que ainda é experimental), instagram-follow (marca de terceiro).

Instalação: npx hyperframes add <nome>; catálogo com npx hyperframes catalog --tag <tag> --json.

**O que muda para nós:** Telas de IA, roteiro digitado e entrega no celular não precisam ser desenhadas do zero: adaptar esses blocos à marca (cores, Helvetica Now, minúsculas) e a uma IA genérica sem marca. A interface fica de frente, sem inclinação em 3D (regra do 3d.md); a profundidade fica com o 3D do implante.

Fontes: C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\blocks\ai-chat-reveal\registry-item.json · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\components\notes-typing\registry-item.json · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\components\parallax-device-dive\registry-item.json · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\components\agent-cursor\registry-item.json · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\components\CATALOG.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\docs\guides\html-in-canvas.mdx

### 8. Regras de motion e história do HyperFrames que batem com o gosto do dono (e um conflito)

Batem com o gosto do dono:
- motion.md: chegada lenta com cauda longa, saída limpa; título pousado fica parado; cada transição tem uma causa na tela; usar 3 a 5 tipos de transição; 'respiração' em título e interface é tique de vídeo gerado (em personagem é atuação).
- explainer.md: comece por uma pessoa e uma pergunta que ela faria; 'o objeto é a explicação'; um diagrama que cresce uma parte por vez.
- story.md: escrever 3 storylines em palavras, o dono escolhe, depois SPEC.md com números.
- spec.md, lista BANNED: vazio escuro com coisas pequenas flutuando, brilho, partículas, três cards em fila, logo no canto.
- film.md: TTS fala ~2,2 palavras/s, então ~19 palavras por cena e até ~155 palavras em 30 a 90 s.

Conflito: vertical.md pede tomadas de 1 a 2 s e algo novo a cada 2 a 4 s, mas o dono reprovou o carrossel por ser 'rápido demais'. Vale o histórico do dono: algo novo a cada 2 a 4 s, sem sequências de cortes abaixo de 1 s, com o movimento chegando quando o olho chega.

Area segura no vertical: nada nos 168 px de cima; texto e produto entre 168 e 1330 px; nada sob a coluna de botões da direita.

**O que muda para nós:** O processo do dono (roteiro, depois 10 s, depois completo) já casa com o do HyperFrames: STORYLINES.md, depois SPEC.md, depois check, snapshot --review e REVIEW.md. A bíblia da série deve fixar ritmo, BANNED e áreas seguras uma vez só.

Fontes: C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\motion.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\story.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\spec.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\film.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\types\vertical.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\review.md

### 9. Áudio: o que já existe nos projetos do dono e dá para repetir

Do teaser do elevador (aprovado na v5; a narração A.Medeiros foi a pedida em 2026-11-11):

- Narração: voz A.Medeiros (biblioteca da ElevenLabs, voice_id E9hPCbqBRCgB3UEiCUuE), modelo eleven_v4, 4 tomadas comparadas.
- Instruções do site da ElevenLabs: Multilingual v2, Stability ~55%, Similarity ~75%, Style 0–10%, Speed 1.0. Texto com linhas em branco para criar pausas de recorte.
- montar-narracao.py: recorta cada fala nas pausas (entrada e saída de 15 ms), põe no tempo do filme pelo narracao.json (de, ate, no_filme, ganho_db), abaixa a música só sob a voz (voz ~8 dB acima) e faz uma descida fixa em rampa na última fala. Nunca estica, acelera ou emenda a voz.
- montar-trilha3.py: desloca a música para o golpe dela cair no momento visual. Também faz:
  - grave com teto que sobe aos poucos;
  - harmônicos do grave para o celular (trilha-celular.py);
  - rampa de volume de +12,5 dB;
  - riser de 1,55 s com 20 ms de respiro antes do golpe;
  - eco de sala no impacto.
- montar-sons.py: monta efeitos a partir de tomadas geradas (corte, equalização, cruzamentos).
- normalizar-audio.py: um ganho fixo para o vídeo inteiro (alvo −14 LUFS, pico −1,5 dB fora do impacto) e limitador só na janela do impacto.
- index.html: cada som é um <audio> com id, data-volume e fades; motion blur ligado na raiz.

Os scripts gerar-audio.ps1, gerar-quadro.ps1 e gerar-clipe.ps1 chamam o Higgsfield: aposentar. O teaser Funcionária Digital usou trilha escrita em código (audio.html, Web Audio) e render próprio (Playwright, 60 q/s com 3 subquadros), mas o padrão atual é o HyperFrames com trilha do ElevenLabs Music.

No HyperFrames:
- envelopes de volume (data-automation);
- cadeia de efeitos (data-fx-chain: passa-alta, equalizador, limitador);
- carve.mjs, que abre espaço só nas frequências da voz;
- grupos de áudio (voz, música, efeitos);
- 21 efeitos embutidos (licença Pixabay, uso comercial liberado);
- busca no Openverse (só CC0 e CC BY, com crédito);
- npx hyperframes normalize-audio, beats e audio <video> --json (confere se o som existe, onde bate e o volume).

**O que muda para nós:** O 'motor de som' da série já existe: copiar montar-narracao.py, montar-trilha3.py, trilha-celular.py e normalizar-audio.py para o molde da série, trocando as constantes fixas (DUR, IMPACTO_S) por um arquivo de configuração por episódio. Regra mantida: construção gradual até UM impacto, que é a revelação do 'vídeo dela'.

Fontes: C:\social-media\hyperframes\teaser-elevador-sabia\fonte\ROTEIRO.md · C:\social-media\hyperframes\teaser-elevador-sabia\fonte\narracao.json · C:\social-media\hyperframes\teaser-elevador-sabia\fonte\montar-narracao.py · C:\social-media\hyperframes\teaser-elevador-sabia\fonte\montar-trilha3.py · C:\social-media\hyperframes\teaser-elevador-sabia\fonte\normalizar-audio.py · C:\social-media\hyperframes\teaser-elevador-sabia\fonte\montar-sons.py · C:\social-media\hyperframes\teaser-elevador-sabia\fonte\prompts\narracao-amedeiros-elevenlabs-site.txt · C:\social-media\hyperframes\teaser-elevador-sabia\index.html · C:\social-media\hyperframes\teaser-funcionaria-digital\REVIEW.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\media-use\references\mixing.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\references\sound.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\media-use\audio\assets\sfx\CREDITS.md

### 10. O conector ElevenLabs substitui o Higgsfield no áudio

Consultei, sem gerar nada, o que o conector ElevenLabs da sessão consegue fazer:
- Voz: eleven_v4, v3, Multilingual v2, Turbo e Flash.
- Efeitos sonoros: eleven_text_to_sound_v2, de 0,5 a 30 s, com opção de loop.
- Música: eleven_music_v2_5, de 3 a 600 s, instrumental.
- Música a partir de um vídeo pronto (eleven_video_to_music_v1).
- Transcrição com tempo de cada palavra (Scribe), útil para legendas e marcas.
- Isolador de voz e efeitos de ambiente.

A trilha do elevador já era um 'ElevenLabs Music', só que pedido pelo Higgsfield; agora vai direto. O mesmo conector também oferece geradores de imagem e vídeo (GPT Image, Nano Banana, Kling, Veo, Seedance etc.), e esses estão PROIBIDOS pela regra do dono.

No media-use do HyperFrames, a música padrão vem da HeyGen e a geração local é MusicGen; nenhum dos dois está na lista de ferramentas liberadas.

**O que muda para nós:** Pipeline de som do episódio: tema da série no ElevenLabs Music (um prompt por duração, como o trilha3-a.txt); efeitos do ElevenLabs SFX gravados uma vez numa biblioteca da série, com 2 ou 3 tomadas de cada som repetido; voz A.Medeiros; Scribe para os tempos das palavras. Confirmar com o dono se as bibliotecas grátis (Pixabay embutida e Openverse) podem entrar, já que não são geradores.

Fontes: C:\social-media\hyperframes\teaser-elevador-sabia\fonte\prompts\trilha3-a.txt · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\media-use\audio\references\bgm.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\media-use\audio\references\sfx.md · creative_get_flow_node_types (conector ElevenLabs, consultado em 2026-11-11)

### 11. Pipeline de um episódio, do roteiro ao MP4

0) Pauta: especialidade, a pergunta do paciente e a fonte técnica, com revisão de um profissional da área.

1) Três storylines em palavras (story.md). O dono escolhe (APROVAÇÃO 1). Depois SPEC.md com números: cores, Helvetica 76 px, câmera, tempos, BANNED e áreas seguras.

2) Roteiro de narração: 60–90 s ≈ 130–155 palavras, ~19 por cena. A frase da tela nunca repete a da voz.

3) Voz primeiro, porque a voz é o relógio. Fazer A.Medeiros no ElevenLabs com 2 a 4 tomadas, escolher uma, recortar nas pausas (montar-narracao.py) e tirar os tempos das palavras com Scribe ou npx hyperframes transcribe.

4) Imagens novas do episódio: poses, cenário e telas, com gerar-imagem.mjs --ref da folha da personagem. Rascunho primeiro e final depois; recorte com --fundo transparent ou remove-background.

5) Cena 3D do tema no palco 3D do molde:
- baixar o modelo CC BY e reduzir para menos de 150 mil faces;
- montar câmera de mergulho, corte e vista explodida;
- conferir com npx hyperframes snapshot --at e keyframes --angle iso.

6) Montagem no HyperFrames, com uma cena por arquivo em compositions\:
- gancho (frame 0 já é a capa);
- a dor;
- o roteiro chegando;
- a IA trabalhando;
- o 'vídeo dela' (o 3D);
- volta para ela;
- frase final;
- assinatura.
Transições com causa (por exemplo, parallax-device-dive para entrar no vídeo dela).

7) Corte de 10 s e render draft (~1 min). APROVAÇÃO 2.

8) Som: trilha cortada para UM impacto na revelação, efeitos com causa na tela, música baixa sob a voz e carve.

9) npx hyperframes check --json, snapshot --review e REVIEW.md. Prévia no Studio (npx hyperframes preview). APROVAÇÃO 3.

10) Render 'looks' ou 'delivery' (~4 a 9 min), depois normalizar-audio.py (−14 LUFS), salvo em prontos\AAAA-MM-DD_clinicas-epNN-tema.mp4.

11) Legenda do post com os créditos CC BY.

**O que muda para nós:** Com o molde pronto, o trabalho por episódio é roteiro, voz, 1 cena 3D e poucas imagens. O render não pesa. As três paradas de aprovação já estão previstas no CLAUDE.md e no BRIEF.md.

Fontes: C:\social-media\CLAUDE.md · C:\social-media\hyperframes\_serie-clinicas\BRIEF.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes\SKILL.md · C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\skills\hyperframes-cli\SKILL.md · C:\social-media\hyperframes\teaser-elevador-sabia\fonte\ROTEIRO.md

### 12. Estrutura de pastas da série: o que é feito uma vez e o que muda por episódio

FEITO UMA VEZ, em C:\social-media\hyperframes\_serie-clinicas\:

- BRIEF.md (já existe).
- BIBLIA.md: formato, estrutura em atos, ritmo, tipografia, paleta, BANNED, áreas seguras, voz e regras de som.
- molde\: cópia do _molde-sabia mais o que a série precisa.
  - lib\: three@0.184.0 com os addons usados e gsap-3.14.2 locais.
  - compositions\_comum\:
    - palco-3d.js (renderizador, luz de estúdio, sombra de contato, pós);
    - tela-ia.html (agent-cursor, streaming-text e progresso adaptados);
    - roteiro-digitado.html (notes-typing);
    - celular-entrega.html (parallax-device-dive);
    - assinatura-serie.html.
  - assets\: fontes e marca; package.json com hyperframes@0.8.216 fixo.
- personagens\dra-<nome>\: ficha.md, folha-de-referencia.png, poses\ e expressoes\ em PNG sem fundo, prompts\, e os .json de cada geração.
- cenarios\: consultório, recepção e mesa, cada um com fundo, primeiro plano e prompts.
- modelos-3d\odonto\ (depois estetica\, dermato\, fisio\): GLBs reduzidos e CREDITOS.md com licença e link.
- som\:
  - tema da série (ElevenLabs Music em 2 ou 3 durações);
  - sfx\ (biblioteca da série com várias tomadas);
  - scripts\ (montar-narracao.py, montar-trilha.py, trilha-celular.py, normalizar-audio.py, lendo um JSON do episódio).

POR EPISÓDIO (uma pasta HyperFrames por peça, como o CLAUDE.md manda): C:\social-media\hyperframes\clinicas-ep01-protocolo-implante\, copiada de molde\, com:
- STORYLINES.md, SPEC.md, ROTEIRO.md e REVIEW.md;
- fonte\ (narracao.json, tomadas de voz, prompts das imagens novas, trilha.json com os tempos do impacto);
- assets\ (só o que é novo, mais cópias da série);
- compositions\ (as cenas do episódio);
- renders\.

O MP4 final vai para prontos\. Se marca\ mudar, recopiar também para _serie-clinicas\molde\assets\.

Muda por episódio: tema, roteiro, voz, a cena 3D (modelo novo), 2 a 6 imagens e o corte da trilha. Repete: personagem, cenários, telas, transições, assinatura, motor de som e regras.

**O que muda para nós:** Episódio novo vira 'copiar o molde, preencher a pauta e trocar o objeto 3D'. A identidade se repete e o custo de imagens cai depois do piloto. A especialidade (estética, dermato, fisio) muda o objeto 3D e o cenário, não o molde.

Fontes: C:\social-media\CLAUDE.md · C:\social-media\hyperframes\_molde-sabia\index.html · C:\social-media\hyperframes\_molde-sabia\compositions\vinheta.html · C:\social-media\hyperframes\teaser-elevador-sabia\package.json · C:\social-media\marca\marca.md

## Referências

- **Bloco product-turntable (HyperFrames)** (arquivo local) — C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\blocks\product-turntable\product-turntable.html  
  Cena Three.js r184 que carrega um GLB num pedestal de estúdio, com relógio GSAP, buildReady e luz de faixas emissivas → *aproveitar:* Esqueleto do 'palco 3D' da série: relógio, carregamento de GLB, ajuste automático de escala, sombra de contato pronta e luz de estúdio
- **Bloco canopy-part-title (HyperFrames)** (arquivo local) — C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\blocks\canopy-part-title\canopy-part-title.html  
  Cena Three.js 0.170 com EffectComposer, BokehPass e mapas de sombra, usando import map → *aproveitar:* Como ligar pós-processamento (desfoque de foco) dentro do protocolo do HyperFrames
- **Componente parallax-device-dive** (arquivo local) — C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\components\parallax-device-dive\registry-item.json  
  Celular sobe na tela e a câmera atravessa a tela até a interface ocupar o quadro → *aproveitar:* Transição 'o seu conteúdo pode sair assim', entrando no vídeo da doutora
- **Componentes notes-typing, agent-cursor e streaming-text** (arquivo local) — C:\Users\YagoBittencourt\.claude\plugins\cache\hyperframes\hyperframes\0.8.216\registry\components\CATALOG.md  
  Texto digitado no ritmo humano, IA operando uma tela e resposta de IA chegando em rajadas → *aproveitar:* Roteiro da doutora sendo digitado e a IA 'gerando o motion', adaptados à marca
- **Teaser do elevador: scripts de som e narração** (arquivo local) — C:\social-media\hyperframes\teaser-elevador-sabia\fonte\ROTEIRO.md  
  Roteiro, narração A.Medeiros e scripts de trilha, voz e volume do teaser aprovado → *aproveitar:* Motor de som da série (montar-narracao.py, montar-trilha3.py, trilha-celular.py, normalizar-audio.py)
- **Gerador de imagens OpenAI do projeto** (arquivo local) — C:\social-media\ferramentas\openai\gerar-imagem.mjs  
  Script único de geração de imagem com a chave do dono (referência, fundo transparente, rascunho, registro de custo) → *aproveitar:* Folha da personagem, poses e cenários, sempre passando a folha de referência com --ref
- **Mandibular First Molar – University of Dundee (Sketchfab)** (modelo 3D, CC BY 4.0) — https://sketchfab.com/3d-models/mandibular-first-molar-e1c919d6603846eca873154eeededdd6  
  Molar inferior esculpido pela Faculdade de Odontologia de Dundee, ~28 mil faces, baixável → *aproveitar:* Coroa e dente com forma anatômica real, no lugar da coroa feita em código (que ficou amadora)
- **Permanent Dentition – University of Dundee (Sketchfab)** (modelo 3D, CC BY 4.0) — https://sketchfab.com/3d-models/permanent-dentition-2f69d7b59c3e4a6a8bcae041bd8e591b  
  Dentição permanente a partir de tomografia, ~30 mil faces → *aproveitar:* Arcada inteira para planos abertos e para mostrar onde fica o implante
- **Inside my Tooth – R-LAB (Sketchfab)** (modelo 3D, CC BY 4.0) — https://sketchfab.com/3d-models/inside-my-tooth-5ebeadf0b40940ca93a4ced5cfe0abb2  
  Dente em corte com gengiva e vasos em objetos separados, ~56 mil faces → *aproveitar:* Cortes anatômicos e camadas que aparecem uma por vez
- **Model Jaw - implant – Ortomesh (Sketchfab)** (modelo 3D, CC BY 4.0) — https://sketchfab.com/3d-models/model-jaw-implant-173fad1fdf784b5db66ed00010a3a59f  
  Mandíbula transparente com implante e nervos (2025), ~116 mil faces → *aproveitar:* Referência de posicionamento do implante no osso e da relação com o nervo
- **Implante Dental – drandrescordova (Sketchfab)** (modelo 3D, CC BY 4.0) — https://sketchfab.com/3d-models/implante-dental-ede1a07475db4236b43a6cd168d1225d  
  Implante didático para identificar as partes, ~19 mil faces → *aproveitar:* Conferir as proporções do parafuso e do pilar feitos em código; uso direto se o acabamento servir
- **Dentist Chair – davis (Poly Pizza)** (modelo 3D, CC BY 3.0) — https://poly.pizza/m/DXhRgoTcP4  
  Cadeira odontológica low poly em glTF → *aproveitar:* Só como objeto de fundo, se combinar; o estilo low poly destoa do acabamento premium
- **Exemplo three.js: clipping stencil** (documentação) — https://threejs.org/examples/webgl_clipping_stencil.html  
  Exemplo oficial de corte por plano com 'tampas' sólidas usando stencil → *aproveitar:* Osso e gengiva em corte sem parecer ocos (o problema que apareceu no teste)
- **Quaternius – Universal Base Characters** (pacote 3D, CC0) — https://quaternius.com/packs/universalbasecharacters.html  
  Personagens base masculinos e femininos com rig humanoide, glTF e FBX (agosto de 2025) → *aproveitar:* Só se um dia a série precisar de figurantes 3D; para a protagonista, a rota 2.5D é melhor
- **Mixamo – perguntas frequentes (Adobe)** (documentação) — https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html  
  Termos de uso das animações e personagens Mixamo → *aproveitar:* Saber que o uso comercial é sem royalties, mas os arquivos não podem ser redistribuídos
- **Fundo transparente no GPT-Image-2 (comunidade OpenAI)** (fórum oficial) — https://community.openai.com/t/transparent-backgrounds-are-now-available-in-preview-for-gpt-image-2-in-the-api/1391541  
  Aviso de que a API aceita background 'transparent' no gpt-image-2, em preview → *aproveitar:* Gerar a personagem já recortada; não confirmei para a versão 2.6 do config
- **Pacote three no jsDelivr** (registro de versões) — https://data.jsdelivr.com/v1/packages/npm/three  
  Lista de versões do three.js (mais nova 0.187.0 em 2026-11-11; 0.184.0 disponível) → *aproveitar:* Fixar three@0.184.0 (a testada pelos blocos e no teste de render) e copiar os arquivos para a pasta local
- **Free3D – tooth dental implant 8751** (modelo 3D, licença royalty free (não CC)) — https://free3d.com/3d-model/tooth-dental-implant-8751.html  
  Dente com implante com arquivo glb, licença própria do site → *aproveitar:* Alternativa se faltar algo; ler os termos antes, porque não é Creative Commons

## Alertas

- Não usar os geradores de imagem e vídeo que o conector ElevenLabs também oferece (GPT Image, Nano Banana, Kling, Veo, Seedance etc.), nem o MCP do Higgsfield, que ainda está instalado. Imagem só por C:\social-media\ferramentas\openai\gerar-imagem.mjs, com a chave do dono. Os scripts gerar-audio.ps1, gerar-quadro.ps1 e gerar-clipe.ps1 dos teasers chamam o Higgsfield e devem ser aposentados.
- O config.json da ferramenta OpenAI está com 'modelos_disponiveis' vazio e sem data de verificação: a chave talvez não esteja cadastrada nem testada. Quem roda cadastrar-chave.ps1 é o dono; eu nunca vejo nem digito a chave.
- Formas orgânicas feitas em código parecem amadoras (no teste, a coroa virou uma 'bolha'), o mesmo erro do pássaro em SVG reprovado. Dente, osso e gengiva devem vir de modelos escaneados; em código, só peças mecânicas (parafuso, pilar).
- Licenças: CC BY exige crédito no post. Modelos do Sketchfab só baixam com conta logada (o dono baixa). Evitar modelos de implante de marca (MSDI), o iPhone real dos blocos vfx-iphone-device e ios26 e as telas que imitam Claude ou ChatGPT. A licença da Helvetica Now continua sem confirmação (marca.md).
- Conteúdo clínico: cada passo do protocolo precisa ser conferido por um dentista antes de animar. As regras de publicidade dos conselhos profissionais ficam com outra frente; não conferi aqui.
- Sem gerador de vídeo não há sincronia de boca: a doutora não deve 'falar' na câmera. Narrador (A.Medeiros) e texto ou chat na tela carregam a fala. A personagem pode mudar entre gerações: travar uma folha de referência e sempre enviá-la.
- O brilho (bloom) estoura superfícies brancas como a coroa (visto no teste). Usar pouco ou nada. A lista BANNED proíbe vazio escuro com objeto pequeno flutuando, brilho e partículas: o fundo escuro da marca (#1E1415) só funciona com o objeto ocupando pelo menos 40% do quadro.
- Contrato do HyperFrames: desfoque, cor, grão e vinheta sobre imagens passam por npx hyperframes media-treatment, não por filtro CSS. Nenhum Math.random sem semente ou relógio real. Uma cena WebGL viva por vez (~350 MB cada). Bibliotecas copiadas para a pasta local, para o render não depender do CDN.
- Ritmo: o guia vertical do HyperFrames pede tomadas de 1 a 2 s, mas o dono reprovou carrossel 'rápido demais'. Valer o gosto do dono, com algo novo a cada 2 a 4 s e o movimento chegando com o olho. Texto só entre 168 e 1330 px de altura, nunca sob os botões da direita.
- As estimativas de render de 60–90 s são extrapoladas de testes de 3 s; não renderizei um episódio inteiro. Render em 4K ou 60 q/s multiplica o tempo sem ganho no Reels. Modelos escaneados de 1 a 2 milhões de faces precisam ser reduzidos.
- Música padrão do HyperFrames (catálogo HeyGen ou MusicGen local) não está na lista de ferramentas liberadas. Bibliotecas grátis de efeitos (Pixabay embutida, Openverse CC0/CC BY) não são geradores, mas confirmar com o dono antes de usar.