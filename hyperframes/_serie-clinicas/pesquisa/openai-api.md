# Pesquisa — openai-api

## Resumo

1) O quadro mudou em 2026. Hoje (11/11/2026) os modelos de imagem atuais da API são gpt-image-2.6-sunburst e gpt-image-2.6-flare, lançados em 04/11/2026, e gpt-image-2.5-sunburst e gpt-image-2.5-flare, lançados em 08/09/2026. O gpt-image-1 foi desligado em 23/10/2026. O gpt-image-1.5, o gpt-image-1-mini e o chatgpt-image-latest saem do ar em 01/12/2026, e o gpt-image-2 em 10/02/2027. Tutoriais de 2025 que usam gpt-image-1 e input_fidelity estão desatualizados.
2) Melhor qualidade: gpt-image-2.6-sunburst, com quality "xhigh" ou "max". O guia oficial manda começar por ele quando detalhe e precisão de edição importam. Mais barato para rascunho: gpt-image-2.5-flare (ou 2.5-sunburst) em "low", cerca de US$ 0,005 por imagem vertical. No 2.6, low e medium custam de 3 a 4 vezes mais que no 2.5.
3) Todos cobram US$ 30 por 1 milhão de tokens de saída (o "token" é a unidade que a OpenAI usa para medir e cobrar). Um quadro vertical de 1152x2048 no 2.6 sai por cerca de US$ 0,042 em high, US$ 0,075 em xhigh e US$ 0,17 em max. Esses valores são só a saída: as imagens de referência entram como custo à parte (US$ 8 por 1 milhão de tokens), e o tamanho real se mede pelo campo usage da resposta.
4) O tamanho 1080x1920 NÃO é aceito, porque os dois lados precisam ser múltiplos de 16. Use 1152x2048 (9:16 exato; reduzindo para 0,9375 vira 1080x1920) ou 1440x2560 (sobra margem para zoom e parallax no HyperFrames). Fundo transparente funciona com background "transparent" e saída png ou webp, o que permite gerar a personagem como camada separada.
5) Consistência de personagem: o método oficial é uma folha da personagem reaproveitada como imagem de entrada em cada cena (endpoint de edição, até 16 referências, cada uma numerada com seu papel no texto do pedido), mais um bloco fixo de "não mudar" repetido em todo pedido. A própria OpenAI avisa que o modelo pode variar em personagens recorrentes. O caminho mais seguro é gerar poucas poses-chave com fundo transparente e fazer o movimento no HyperFrames.
6) Vídeo pela mesma chave não existe mais: Sora 2, Sora 2 Pro e a Videos API foram desligados em 24/09/2026, sem substituto. O 2.6 gera GIF animado de 2 a 16 quadros, que não chega a qualidade premium. Todo o movimento tem de vir do HyperFrames (GSAP e Three.js).
7) Requisitos: talvez seja preciso fazer a verificação de organização (documento de identidade) antes de usar modelos gpt-image. Na faixa Build, o 2.5 permite 20 imagens por minuto. Na chave, use variável de ambiente de usuário OPENAI_API_KEY, um projeto só para isso com limite de gasto rígido, e nunca coloque a chave no HTML do HyperFrames. Para testar a chave sem gastar: GET /v1/models.

## Achados

### Modelos de imagem disponíveis hoje e qual escolher

A página de modelos lista 4 modelos de imagem atuais: gpt-image-2.6-sunburst, que serve para trabalho detalhado e edição precisa; gpt-image-2.6-flare, o mais rápido, para iterar; gpt-image-2.5-sunburst e gpt-image-2.5-flare. O changelog data o 2.6 em 04/11/2026 e o 2.5 em 08/09/2026.

Qualidade (quality): low, medium, high, xhigh, max e auto. O xhigh e o max só existem no 2.5 e no 2.6. O 2.6 traz ainda o campo complexity (low, medium ou high; o padrão é high). Ele controla o quanto o modelo planeja a cena antes de desenhar, não tem custo extra e pode introduzir mudanças indesejadas.

O guia de prompting oficial diz: comece pelo 2.6 Sunburst quando houver exigência de detalhe, layout ou precisão de edição, e pelo 2.6 Flare quando o tempo de resposta importar.

Modelos em fim de vida (página de deprecations):
- gpt-image-1: desligado em 23/10/2026.
- gpt-image-1.5, gpt-image-1-mini e chatgpt-image-latest: saem em 01/12/2026.
- gpt-image-2 e gpt-image-2-2026-04-21: deprecados em 10/11/2026, saem em 10/02/2027.
O substituto recomendado é o 2.6.

Versão fixa (snapshot): o 2.5 tem a versão datada gpt-image-2.5-sunburst-2026-09-08 (e o equivalente do flare). O 2.6 só tem o nome sem data, então não dá para congelar a versão.

Observação: a página do 2.5 Sunburst ainda se descreve como "nosso modelo mais capaz", mas o guia e a página de deprecations mandam migrar para o 2.6. Considero o 2.6 o mais atual.

**O que muda para nós:** - Imagens finais: gpt-image-2.6-sunburst, em high ou xhigh (max só para quadros-chave).
- Rascunhos e testes de enquadramento: gpt-image-2.5-flare em low ou medium.
- Não usar nada da família 1.x nem o gpt-image-2.
- Como o 2.6 não tem versão datada, registrar em cada episódio o modelo e a data em que as imagens foram geradas, porque o resultado pode mudar com o tempo. Se a estabilidade da série virar problema, a versão datada do 2.5 Sunburst serve de âncora.

Fontes: https://developers.openai.com/api/docs/models · https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst · https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst · https://developers.openai.com/api/docs/guides/image-prompting · https://developers.openai.com/api/docs/deprecations · https://developers.openai.com/api/docs/changelog

### Preço: tabela oficial por token e estimativa por imagem

A página de preços oficial (developers.openai.com/api/docs/pricing) cobra por token, não por imagem.

2.6 Sunburst, 2.6 Flare, 2.5 Sunburst, 2.5 Flare e gpt-image-2 têm a mesma tabela:
- texto de entrada: US$ 5 por 1M de tokens (US$ 1,25 em cache);
- imagem de entrada: US$ 8 por 1M (US$ 2 em cache);
- imagem de saída: US$ 30 por 1M.
O modo Batch (processamento em lote) custa metade: US$ 15 por 1M de saída. Ele existe para o 2.5 e o gpt-image-2. O 2.6 não suporta Batch.

O guia oficial não traz tabela por imagem para o 2.5 e o 2.6, só uma calculadora. Reimplementei a fórmula da própria calculadora do site oficial (script em C:\Users\YAGOBI~1\AppData\Local\Temp\claude\2b384691d2ba5125\ac8f9542-8c29-4427-9d2b-a094d0c2255e\scratchpad\calc.mjs). A fórmula confere com a tabela publicada do gpt-image-2 (1024x1024 em low = US$ 0,006). Custo só de saída:

2.6 (Sunburst e Flare):
- 1024x1536: low 0,020 | medium 0,034 | high 0,041 | xhigh 0,074 | max 0,165
- 1152x2048: low 0,020 | medium 0,036 | high 0,042 | xhigh 0,075 | max 0,170
- 1440x2560: low 0,026 | medium 0,047 | high 0,055 | xhigh 0,098 | max 0,221
- 2160x3840: high 0,100 | max 0,400

2.5 (Sunburst e Flare):
- 1024x1536: low 0,005 | medium 0,010 | high 0,041 | xhigh 0,074 | max 0,165
- 1152x2048: low 0,005 | medium 0,011 | high 0,042 | xhigh 0,075 | max 0,170

O texto do pedido e cada imagem de referência somam custo de entrada. O docs não informa quantos tokens uma referência consome no 2.5/2.6 (não confirmado), e isso se mede pelo campo usage.input_tokens_details.image_tokens.

O streaming de imagens parciais acrescenta 100 tokens de saída por parcial.

O mais barato ainda listado é o gpt-image-1-mini (low a partir de US$ 0,005), mas ele sai do ar em 01/12/2026.

**O que muda para nós:** Gerar imagens é barato perto do valor do vídeo. Um episódio com 1 folha de personagem e 20 a 30 quadros em xhigh, no tamanho 1152x2048, custa por volta de US$ 2 a 3 de saída, mais o custo das referências. Isso dá margem para gerar 3 ou 4 variações de cada quadro-chave e escolher a melhor. Para gerar muitas poses de uma vez, o Batch do 2.5 corta o preço pela metade (o resultado pode levar horas).

Fontes: https://developers.openai.com/api/docs/pricing · https://developers.openai.com/api/docs/guides/image-generation · https://developers.openai.com/api/docs/models/gpt-image-2.5-flare

### Tamanhos, vertical 9:16, fundo transparente e formatos

Tamanhos padrão: 1024x1024, 1536x1024 e 1024x1536 (retrato), além de auto.

Tamanho livre, no formato "LARGURAxALTURA":
- os dois lados múltiplos de 16;
- proporção entre 1:3 e 3:1;
- nenhum lado acima de 3840 px;
- total entre 655.360 e 8.294.400 pixels (4K);
- acima de 2560x1440 é "experimental".
A referência da API cita o tamanho livre para o 2 e o 2.5. O guia de prompting do 2.6 repete a mesma regra (múltiplos de 16, proporção de 1:3 a 3:1), e a calculadora oficial aceita tamanho livre no 2.6.

1080x1920 é inválido, porque 1080 não é múltiplo de 16. Alternativas:
- 1152x2048: 9:16 exato; reduzindo para 0,9375 dá 1080x1920 sem cortar nada.
- 1440x2560: 9:16 exato, no limite do não experimental.
- 2160x3840: 4K, experimental.

Fundo transparente: background "transparent" com output_format png ou webp. Está confirmado para o 2.5 (na referência) e para o 2.6 (o guia de prompting diz que os dois suportam). No gpt-image-2 está em preview. O jpeg não aceita transparência. O guia orienta pedir no próprio texto um sujeito isolado e conferir no arquivo se a transparência veio de verdade, porque um xadrez desenhado na imagem não é transparência.

Formatos de saída: png (padrão), jpeg, webp, gif e svg.
- output_compression (0 a 100) vale só para jpeg e webp.
- svg: só no 2.6, só em generations, com n=1, e exige acesso do projeto.
- gif: no 2.6, em generations e edits; frame_count de 2 a 16 (padrão 9), frame_duration_ms de 20 a 2000 (padrão 200); pode exigir acesso ao preview.

O parâmetro n vai de 1 a 10 imagens por pedido. A geração pode levar até 2 minutos.

**O que muda para nós:** - Gerar em 1152x2048 quando o quadro entra inteiro na tela.
- Gerar em 1440x2560 quando houver zoom ou parallax (movimento de câmera com camadas) no HyperFrames, porque a sobra de pixels evita imagem borrada no zoom.
- Personagem e objetos em png transparente, como camadas separadas, e o cenário opaco. Assim o GSAP e o Three.js animam as camadas com profundidade sem gerar uma imagem por quadro do vídeo.

Fontes: https://developers.openai.com/api/docs/guides/image-generation · https://developers.openai.com/api/reference/resources/images/methods/generate · https://developers.openai.com/api/reference/resources/images/methods/edit · https://developers.openai.com/api/docs/guides/image-prompting

### Endpoints e parâmetros exatos (gerar, editar, Responses)

1) POST https://api.openai.com/v1/images/generations, em JSON. Campos:
- model
- prompt: até 32.000 caracteres
- n: 1 a 10
- size, quality
- background: transparent, opaque ou auto
- output_format, output_compression
- moderation: auto (padrão) ou low
- complexity: low, medium ou high
- partial_images (0 a 3) e stream
- safety_identifier (o campo user está deprecado)
- frame_count e frame_duration_ms (só para gif)
- svg (só para svg)

2) POST /v1/images/edits. Aceita multipart, com campos -F "image[]=@arquivo.png" repetidos, mais mask, markup, prompt, model e os mesmos campos de saída. Também aceita JSON, com images: [{image_url ou file_id}].
- Até 16 imagens de entrada.
- No JSON, image_url aceita URL ou data URL base64 de até 20.971.520 caracteres.
- mask: mesmo formato e tamanho da imagem, menos de 50 MB, com canal alfa. Vale para a primeira imagem e é guiada pelo texto do pedido, então não segue o contorno com precisão.
- markup (2.5 e 2.6): PNG transparente com as mesmas dimensões da primeira imagem, até 16.777.216 px e 50 MB. Não combina com mask; as demais imagens viram referência.
- input_fidelity: só funciona no gpt-image-1.5 (high ou low) e no 1-mini (low). No gpt-image-2, 2.5 e 2.6 o campo deve ser OMITIDO, porque toda entrada já é tratada em alta fidelidade (isso também aumenta os tokens de entrada).

3) Responses API: tools: [{ type: "image_generation", model: "gpt-image-2.5-sunburst", action: "auto" | "generate" | "edit", quality, size, background, output_format, output_compression, partial_images, input_image_mask: { file_id } }].
- O model principal do pedido é um modelo de texto, por exemplo gpt-6-astra ou gpt-5.5.
- A saída vem num item image_generation_call, com result (base64), revised_prompt, id e status.
- Dá para editar em várias rodadas usando previous_response_id.
- O preço de entrada em cache só vale aqui.
- O 2.6 NÃO está disponível na Responses: a página do modelo marca "Not supported", e o guia da ferramenta lista só 2.5, 2, 1.5 e 1-mini.

Resposta do Image API:
{ created, background, data: [{ b64_json }], output_format, quality, size, usage: { input_tokens, input_tokens_details: { image_tokens, text_tokens }, output_tokens, output_tokens_details: { image_tokens, text_tokens }, total_tokens }, svg_usage }
Os modelos GPT Image não devolvem url, só base64.

Erros bloqueados pela moderação: error.type = "image_generation_user_error", error.code = "moderation_blocked" e moderation_details { moderation_stage: input | output | unknown, categories: [...] }. A orientação é não repetir automaticamente.

Exemplo mínimo em Node 22 (sintaxe checada com node --check; o arquivo completo, com tratamento de erro e verificação da chave, está em C:\Users\YAGOBI~1\AppData\Local\Temp\claude\2b384691d2ba5125\ac8f9542-8c29-4427-9d2b-a094d0c2255e\scratchpad\exemplo-openai-imagens.mjs):

// GERAR
const r = await fetch('https://api.openai.com/v1/images/generations', { method: 'POST', headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}`, 'Content-Type': 'application/json' }, body: JSON.stringify({ model: 'gpt-image-2.6-sunburst', prompt: '...', size: '1152x2048', quality: 'high', background: 'opaque', output_format: 'png' }) });
const j = await r.json(); if (!r.ok) throw new Error(JSON.stringify(j.error));
await writeFile('quadro.png', Buffer.from(j.data[0].b64_json, 'base64')); console.log(j.usage);

// EDITAR COM 2 REFERÊNCIAS
const f = new FormData();
f.append('model', 'gpt-image-2.6-sunburst'); f.append('prompt', 'Imagem 1 = personagem (não mudar)... Imagem 2 = cenário...'); f.append('size', '1152x2048'); f.append('quality', 'high');
f.append('image[]', new Blob([await readFile('folha.png')], { type: 'image/png' }), 'folha.png');
f.append('image[]', new Blob([await readFile('cenario.png')], { type: 'image/png' }), 'cenario.png');
const r2 = await fetch('https://api.openai.com/v1/images/edits', { method: 'POST', headers: { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` }, body: f });
// não definir Content-Type à mão: o fetch gera o boundary

**O que muda para nós:** Os scripts de geração ficam fora do HTML do HyperFrames: um script Node separado salva os PNG dentro da pasta da peça, e o HTML só lê arquivos locais. Usar o Image API (/images/generations e /images/edits) com o 2.6 para tudo, porque a Responses não tem o 2.6. Gravar o campo usage de cada pedido num log, para saber o custo real por episódio.

Fontes: https://developers.openai.com/api/reference/resources/images/methods/generate · https://developers.openai.com/api/reference/resources/images/methods/edit · https://developers.openai.com/api/docs/guides/image-generation · https://developers.openai.com/api/docs/guides/tools-image-generation · https://developers.openai.com/api/docs/models/gpt-image-2.6-flare

### Exigências: verificação de organização, faixas de uso e limites

Verificação de organização: o guia oficial diz que talvez seja preciso concluir a "API Organization Verification" no painel (platform.openai.com/settings/organization/general) antes de usar modelos GPT Image. Não consegui abrir o artigo de ajuda (help.openai.com 10910291), que retornou HTTP 403.

Pelos trechos da busca e pelo fórum da comunidade (não confirmado em fonte oficial):
- é preciso um documento oficial com foto, físico, de um país suportado, e às vezes uma selfie;
- quem não está verificado recebe 403 com a mensagem "organization must be verified";
- relatos dizem que não há nova tentativa se a verificação falhar;
- relatos dizem que um documento fica preso a uma organização por cerca de 90 dias;
- há relatos de 403 mesmo depois de verificado.

Faixas de uso (guia de rate limits). As faixas pagas sobem sozinhas conforme o total de créditos comprados:
- Free: limite de US$ 100 por mês, em país permitido;
- Build: a partir de US$ 5 comprados, limite de US$ 500 por mês;
- Launch: a partir de US$ 100, limite de US$ 5.000 por mês;
- Grow: a partir de US$ 500, limite de US$ 200.000 por mês.

Limites do 2.5 (Sunburst e Flare, na página do modelo):
- Build: 250 mil tokens por minuto e 20 imagens por minuto;
- Launch: 3 milhões e 150;
- Grow: 8 milhões e 250.
O 2.6 não publica números: a página manda olhar em Settings > Organization > Limits. Se a faixa Free dá acesso a imagem não está confirmado.

O guia lembra que estar numa faixa não garante acesso a um modelo, e que o GET /v1/models com a mesma chave mostra o que ela enxerga.

Limite de gasto rígido (hard spend limit): ao bater o valor, os pedidos recebem erro 429. O alerta de gasto só avisa e não bloqueia.

**O que muda para nós:** Antes do piloto, o dono precisa conferir no painel se a organização está verificada. Se não estiver, verificar com o documento físico e fotos nítidas, porque pode não haver segunda chance. Configurar um limite de gasto rígido mensal no projeto. Os limites da faixa Build bastam para o volume do projeto.

Fontes: https://developers.openai.com/api/docs/guides/image-generation · https://help.openai.com/en/articles/10910291-api-organization-verification · https://developers.openai.com/api/docs/guides/rate-limits · https://developers.openai.com/api/docs/models/gpt-image-2.5-sunburst · https://community.openai.com/t/gpt-images-1-403-what-are-the-conditions-for-requesting-this-model-gpt-image-1/1245846 · https://community.openai.com/t/help-organization-could-not-be-verified/1242608

### Política de conteúdo: o que pode bloquear imagens de clínica

Confirmado nas fontes oficiais:
- Todos os pedidos e todas as imagens geradas passam por filtro conforme a política de uso.
- O parâmetro moderation aceita auto (padrão) ou low (filtro menos restritivo).
- O bloqueio vem como moderation_blocked, com categorias genéricas como harassment, self-harm, sexual e violence.
- No guia de moderação, a categoria violence/graphic cobre conteúdo que mostra morte, violência ou ferimento físico em detalhe gráfico, tanto em texto quanto em imagem.
- Pessoas reais: o guia oficial tem um exemplo, "Insert a person into a scene", que usa a foto de uma pessoa real como entrada para preservar a identidade. Tecnicamente é aceito.
- As imagens carregam sinais de procedência verificáveis pela própria OpenAI (metadados C2PA e marca d'água SynthID). Editar ou converter o arquivo pode remover os metadados.

Não confirmado:
- Não consegui abrir a página da política de uso (openai.com/policies/usage-policies, HTTP 403), então as regras sobre uso da imagem de pessoa real sem consentimento ficaram sem confirmação.
- Que cirurgia, sangue ou gengiva aberta seriam bloqueados é inferência minha a partir da categoria violence/graphic. Não achei regra oficial específica sobre procedimentos médicos.

**O que muda para nós:** - Mostrar o protocolo de implantes de forma limpa e didática: implante, pilar, coroa e osso estilizado, em corte transversal 3D sem sangue. Além de reduzir o risco de bloqueio, isso combina com o acabamento premium que o dono quer.
- Não usar fotos de pacientes nem do dono como referência de rosto.
- Manter as personagens 100% fictícias e estilizadas.
- Tratar moderation_blocked reescrevendo o pedido, nunca repetindo igual.

Fontes: https://developers.openai.com/api/docs/guides/image-generation · https://developers.openai.com/api/docs/guides/moderation · https://developers.openai.com/api/docs/guides/image-prompting · https://developers.openai.com/api/docs/guides/content-provenance · https://openai.com/policies/usage-policies/

### Consistência de personagem 3D estilizada: método oficial e dicas da comunidade

Método oficial (guia de prompting, seção "Keep a character consistent", com exemplos do 2.6):
1. Criar primeiro uma referência reutilizável da personagem, que define aparência, proporções, roupa e tom, em fundo neutro, sem texto.
2. Em cada cena nova, enviar essa imagem como entrada e repetir os traços fixos numa lista chamada "Character Consistency" (mesma roupa, mesmo rosto, mesmas proporções e paleta), com a frase "Do not redesign the character".
3. Dar papel numerado a cada referência: "Imagem 1 = personagem, Imagem 2 = cenário".
4. Separar o que muda do que fica: "mude só X" e a lista do que preservar (identidade, geometria, luz).
5. Iterar com uma mudança por vez, usando a saída anterior como próxima entrada e repetindo as restrições se houver desvio.
6. Omitir input_fidelity, porque 2, 2.5 e 2.6 já tratam toda entrada em alta fidelidade.
7. Para correções locais, usar edição por markup (um traço desenhado em PNG transparente).
8. Se uma parte precisa ficar idêntica pixel a pixel, recortar a edição aprovada e colar sobre o original.

A própria OpenAI lista como limitação que o modelo "pode ocasionalmente" falhar em manter personagens recorrentes consistentes.

Comunidade (terceiros, não oficial):
- folha de giro (turnaround) com frente, perfil e costas em pose neutra e fundo de estúdio, corrigindo um detalhe errado antes de expandir (guia da Dreamina/CapCut);
- reenviar a referência em toda geração e rotular cada imagem (Scenario);
- o gpt-image-2 confunde esquerda e direita em membros (fórum OpenAI);
- uma comparação de maio/2026 coloca o gpt-image-2 em 3º lugar em consistência de personagem, atrás de FLUX.2 e Gemini (techstackups).
Não achei teste independente de consistência do 2.6 com 3D estilizado.

**O que muda para nós:** Montar uma "bíblia da personagem" para a série:
- folha 3/4 + frente + perfil + costas, um close com 4 a 6 expressões e as mãos;
- um bloco de texto fixo com a roupa (jaleco, cabelo, acessórios, cores), copiado igual em todo pedido.

Cada cena usa o endpoint de edição com [folha da personagem, cenário ou objeto] e o mesmo modelo, tamanho e quality.

Para não depender de dezenas de gerações:
- gerar poucas poses-chave com fundo transparente e animar por camadas no HyperFrames (piscar, respirar, parallax);
- nunca pedir texto dentro da imagem: a tipografia da marca entra no HTML;
- não confiar que o modelo acerte o hex exato da marca, e ajustar a cor na composição (inferência, não confirmada).

Fontes: https://developers.openai.com/api/docs/guides/image-prompting · https://developers.openai.com/api/docs/guides/image-generation · https://dreamina.capcut.com/resource/gpt-image-2-for-character-turnaround-sheets · https://help.scenario.com/articles/8473821828-gpt-image-2-the-essentials · https://community.openai.com/t/developing-sprite-sheets-with-gpt-image-2/1379831 · https://techstackups.com/comparisons/gemini-vs-openai-vs-flux-vs-runway-character-consistency-may-2026/

### Vídeo: Sora e a Videos API foram desligados

As páginas oficiais do sora-2 e do sora-2-pro estão marcadas como "Shut down". A Videos API (/v1/videos) e os modelos sora-2, sora-2-pro e suas versões datadas foram desligados em 24/09/2026 (aviso dado em 24/03/2026), e o próprio guia diz que não há API substituta.

Como era antes, só para registro histórico:
- sora-2: US$ 0,10 por segundo em 720x1280;
- sora-2-pro: US$ 0,30 por segundo em 720x1280, US$ 0,50 em 1024x1792 e US$ 0,70 em 1080x1920;
- até 20 segundos (desde 12/03/2026);
- input_reference por multipart ou JSON;
- imagens de entrada com rosto humano eram rejeitadas;
- personagens com aparência humana eram bloqueados por padrão.

O que resta de "movimento" na API é o GIF do 2.6: de 2 a 16 quadros, de 20 a 2000 ms por quadro.

**O que muda para nós:** Não há opção de vídeo pela chave da OpenAI. Todo o motion vem do HyperFrames, com camadas PNG, GSAP, Three.js e câmera 2.5D (camadas planas em profundidade dando sensação de 3D). Os GIFs do 2.6 servem no máximo como rascunho de movimento ou referência, não como peça final, porque o GIF tem paleta limitada a 256 cores.

Fontes: https://developers.openai.com/api/docs/models/sora-2 · https://developers.openai.com/api/docs/models/sora-2-pro · https://developers.openai.com/api/docs/deprecations · https://developers.openai.com/api/docs/guides/video-generation · https://developers.openai.com/api/docs/changelog

### Guardar a chave no Windows 11 e testar sem gastar

Fontes oficiais:
- O quickstart da OpenAI recomenda variável de ambiente; para Windows, mostra setx OPENAI_API_KEY "sua_chave".
- O artigo "Best practices for API key safety" (visto nos resultados de busca) também recomenda variável de ambiente, nunca colocar a chave em navegador nem em repositório, usar chave com validade e rotação, e limite de gasto rígido.
- O guia de chaves pede chave fora de código de navegador, de logs e do controle de versão.

Opções no Windows:
(A) Variável de ambiente de usuário OPENAI_API_KEY. É a mais simples.
- Prefira criar pelo painel "Editar as variáveis de ambiente para sua conta". Digitar a chave no PowerShell a deixa gravada em texto puro no histórico do PSReadLine (%APPDATA%\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt). Esta é observação minha, não da OpenAI.
- Só vale para janelas novas: é preciso reabrir o terminal e o Claude Code.
- Fica em texto puro no perfil do usuário, legível por qualquer programa do usuário.
(B) Arquivo .env. O Node 22 lê sozinho, com node --env-file=.env script.mjs ou process.loadEnvFile().
- Risco: o arquivo ser copiado, compartilhado ou sincronizado junto com a pasta do projeto.
(C) Cofre criptografado: Gerenciador de Credenciais ou os módulos oficiais da Microsoft SecretManagement e SecretStore.
- Na hora de usar: $env:OPENAI_API_KEY = Get-Secret OPENAI_API_KEY -AsPlainText.
- É mais seguro, mas tem mais passos para um iniciante.

Testar a chave sem gastar: GET https://api.openai.com/v1/models com Authorization: Bearer.
- Se responder 200, a chave vale; se responder 401, é inválida.
- A resposta inclui shutdown_date.
- A chamada não gera imagem nem tokens. Que ela seja gratuita é a minha leitura: o docs não diz isso com todas as letras.
- Em PowerShell: Invoke-RestMethod https://api.openai.com/v1/models -Headers @{Authorization="Bearer $env:OPENAI_API_KEY"} | % data | ? id -like 'gpt-image*' | select id
- Limite: ver o modelo na lista não prova que a organização está verificada. O primeiro teste real mais barato é gpt-image-2.5-flare, quality low, 1024x1536, cerca de US$ 0,005.

**O que muda para nós:** Recomendação para este PC pessoal:
- criar no painel da OpenAI um projeto só para "social-media", com chave própria, validade e limite de gasto rígido;
- gravar a chave como variável de usuário pelo painel do Windows, não digitando no terminal, e reiniciar o Claude Code;
- se preferir .env, deixá-lo fora de qualquer pasta sincronizada ou compartilhada.
A chave nunca entra em arquivos HTML do HyperFrames, porque o preview roda no navegador.

Fontes: https://developers.openai.com/api/docs/quickstart · https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety · https://developers.openai.com/api/docs/guides/api-keys · https://developers.openai.com/api/docs/guides/production-best-practices · https://developers.openai.com/api/reference/resources/models/methods/list · https://developers.openai.com/api/docs/guides/rate-limits · https://learn.microsoft.com/en-us/powershell/utility-modules/secretmanagement/get-started/using-secretstore · https://nodejs.org/learn/command-line/how-to-read-environment-variables-from-nodejs

## Referências

- **Guia oficial de geração de imagens (versão .md)** (documentação oficial) — https://developers.openai.com/api/docs/guides/image-generation  
  Guia completo do Image API e da Responses: gerar, editar, markup, mask, tamanhos, formatos, GIF/SVG, moderação, custos e calculadora. Também existe em .md, acrescentando .md ao final do endereço. → *aproveitar:* As regras de tamanho (múltiplos de 16, 1:3 a 3:1, máximo 3840), o formato do erro moderation_blocked, os exemplos curl e SDK de edição com image[] e a fórmula da calculadora de tokens.
- **Guia oficial de prompting de imagem (Image prompting)** (documentação oficial) — https://developers.openai.com/api/docs/guides/image-prompting  
  Técnicas de prompt com exemplos do 2.6 e do 2.5, incluindo "Keep a character consistent", combinar referências, recorte transparente e markup. → *aproveitar:* O modelo de prompt em seções (Character / Scene / Character Consistency / Constraints), a regra "mude só X, preserve Y" e a lista de conferência do resultado.
- **Referência da API: Create image edit** (referência de API) — https://developers.openai.com/api/reference/resources/images/methods/edit  
  Todos os parâmetros do /v1/images/edits, com limites (até 16 imagens, n de 1 a 10) e o esquema da resposta com usage. → *aproveitar:* Os campos exatos (markup, mask, background, complexity, frame_count) e a regra de omitir input_fidelity nos modelos 2.x.
- **Referência da API: Create image** (referência de API) — https://developers.openai.com/api/reference/resources/images/methods/generate  
  Parâmetros do /v1/images/generations e um exemplo de resposta JSON. → *aproveitar:* A lista de modelos aceitos, a regra de fundo transparente por modelo e o formato do campo usage.
- **Página de preços da API (geração de imagem)** (documentação oficial) — https://developers.openai.com/api/docs/pricing  
  Tabela por milhão de tokens de todos os modelos de imagem, nos modos Standard e Batch. → *aproveitar:* Conferir preços antes de orçar. O endereço openai.com/api/pricing retornou 403 para mim, mas esta página tem a mesma tabela.
- **Página do modelo gpt-image-2.6-sunburst** (documentação oficial) — https://developers.openai.com/api/docs/models/gpt-image-2.6-sunburst  
  Ficha do modelo: endpoints suportados (só generations e edits), preço e versões. → *aproveitar:* A confirmação de que o 2.6 não roda na Responses nem no Batch e não tem versão datada.
- **Página do modelo gpt-image-2.5-flare** (documentação oficial) — https://developers.openai.com/api/docs/models/gpt-image-2.5-flare  
  Ficha do 2.5 Flare, com a versão datada 2026-09-08 e os limites por faixa (Build: 20 imagens por minuto). → *aproveitar:* Modelo barato para rascunhos e para o primeiro teste real da chave; aceita Batch com 50% de desconto.
- **Deprecations (OpenAI API)** (documentação oficial) — https://developers.openai.com/api/docs/deprecations  
  Datas de desligamento: gpt-image-1 (23/10/2026), 1.5, 1-mini e chatgpt-image-latest (01/12/2026), gpt-image-2 (10/02/2027) e Sora com a Videos API (24/09/2026). → *aproveitar:* Evitar construir o fluxo sobre modelos que vão sumir.
- **Changelog da API** (documentação oficial) — https://developers.openai.com/api/docs/changelog  
  Histórico datado: 2.6 em 04/11/2026, 2.5 em 08/09/2026, transparência no gpt-image-2 em 20/08/2026 e gpt-image-2 em 21/04/2026. → *aproveitar:* Datar cada recurso e acompanhar mudanças futuras.
- **Guia da ferramenta image_generation (Responses API)** (documentação oficial) — https://developers.openai.com/api/docs/guides/tools-image-generation  
  Uso da ferramenta de imagem dentro da Responses, com edição em várias rodadas e a lista de modelos principais compatíveis. → *aproveitar:* Só se quiser edição conversacional com o 2.5. Para o 2.6 não serve.
- **Guia de rate limits** (documentação oficial) — https://developers.openai.com/api/docs/guides/rate-limits  
  Faixas Free, Build, Launch e Grow, limites de gasto e cabeçalhos x-ratelimit. → *aproveitar:* Configurar o limite de gasto rígido e entender o erro 429.
- **Guia de vídeo com Sora (histórico)** (documentação oficial) — https://developers.openai.com/api/docs/guides/video-generation  
  Guia mantido só como registro, com o aviso de desligamento em 24/09/2026. → *aproveitar:* A confirmação de que não há vídeo pela API da OpenAI.
- **Guia de moderação (categorias)** (documentação oficial) — https://developers.openai.com/api/docs/guides/moderation  
  Definição das categorias, como violence/graphic: morte, violência ou ferimento em detalhe gráfico. → *aproveitar:* Calibrar como mostrar procedimentos de clínica sem bloqueio (sem sangue, em corte didático).
- **Artigo de ajuda: API Organization Verification** (central de ajuda oficial (não consegui abrir, HTTP 403)) — https://help.openai.com/en/articles/10910291-api-organization-verification  
  Passo a passo oficial da verificação de organização exigida para modelos GPT Image. → *aproveitar:* O dono deve ler antes de verificar, porque pode não haver nova tentativa.
- **Artigo de ajuda: Best practices for API key safety** (central de ajuda oficial (visto em busca, não aberto)) — https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety  
  Boas práticas para guardar a chave: variável de ambiente, rotação e limite de gasto. → *aproveitar:* Seguir junto com a configuração da variável OPENAI_API_KEY no Windows.
- **Fórum OpenAI: 403 no gpt-image e verificação** (comunidade) — https://community.openai.com/t/gpt-images-1-403-what-are-the-conditions-for-requesting-this-model-gpt-image-1/1245846  
  Relatos de erro 403 por organização não verificada. → *aproveitar:* Reconhecer o erro e saber que a solução é a verificação no painel.
- **Fórum OpenAI: sprite sheets com gpt-image-2** (comunidade) — https://community.openai.com/t/developing-sprite-sheets-with-gpt-image-2/1379831  
  Experiência prática gerando folhas de poses, com o relato de confusão entre esquerda e direita. → *aproveitar:* Conferir mãos e braços em cada pose da personagem.
- **Microsoft SecretStore (SecretManagement)** (documentação oficial Microsoft) — https://learn.microsoft.com/en-us/powershell/utility-modules/secretmanagement/get-started/using-secretstore  
  Cofre criptografado oficial para PowerShell. → *aproveitar:* Opção mais segura que a variável de ambiente, se o dono quiser.
- **Exemplo Node 22 escrito nesta pesquisa** (arquivo local (rascunho)) — file:///C:/Users/YAGOBI~1/AppData/Local/Temp/claude/2b384691d2ba5125/ac8f9542-8c29-4427-9d2b-a094d0c2255e/scratchpad/exemplo-openai-imagens.mjs  
  Script sem dependências com três modos: checar (GET /v1/models), gerar (JSON) e editar (multipart com 2 image[]). A sintaxe foi checada com node --check, mas ele NÃO foi executado contra a API. → *aproveitar:* Base para o script de geração do projeto, a ser copiado para a pasta da peça.

## Alertas

- Não usar gpt-image-1, que foi desligado em 23/10/2026. Também não usar gpt-image-1.5, 1-mini e chatgpt-image-latest (saem em 01/12/2026) nem gpt-image-2 (sai em 10/02/2027). Tutoriais de 2025 com gpt-image-1, input_fidelity: "high" ou dall-e estão desatualizados.
- Não existe vídeo pela chave da OpenAI: Sora 2, Sora 2 Pro e /v1/videos foram desligados em 24/09/2026, sem substituto. Todo o motion tem de vir do HyperFrames.
- O tamanho 1080x1920 é rejeitado, porque os lados precisam ser múltiplos de 16. Gere em 1152x2048 (reduzir para 0,9375) ou 1440x2560 (reduzir para 0,75). Acima de 2560x1440 é experimental.
- O 2.6 não está na Responses API nem no Batch e não tem versão datada, então o resultado pode mudar com o tempo. Registre modelo e data por episódio. Para a Responses ou para Batch, só o 2.5.
- No 2.6, as qualidades low e medium gastam cerca de 4,2x e 3,3x mais tokens que no 2.5. Para rascunho, use o 2.5 Flare. Os custos por imagem que calculei são só de saída: as imagens de referência acrescentam custo de entrada (US$ 8 por 1 milhão de tokens), em quantidade que o docs não informa. Meça pelo campo usage.
- No 2.x, o campo input_fidelity deve ser omitido. Mandá-lo pode dar erro.
- Não pedir texto dentro das imagens. O modelo ainda erra texto, e a tipografia da marca (Helvetica Now Text e Megion) tem de entrar no HTML do HyperFrames.
- Evitar sangue, cirurgia aberta e ferimentos. A categoria violence/graphic cobre ferimento físico em detalhe gráfico, e o bloqueio para procedimentos médicos é inferência minha, não regra confirmada. Também não usar fotos de pacientes nem do dono como referência de rosto: a política sobre uso da imagem de pessoa real não foi confirmada, porque a página de política retornou 403.
- A verificação de organização pode ser exigida antes do primeiro uso. Segundo a comunidade (não confirmado), uma verificação que falha pode não ter nova tentativa, então use o documento físico e uma foto nítida.
- A consistência da personagem não é garantida. A própria OpenAI lista isso como limitação. Planeje poucas poses-chave reaproveitadas em camadas, em vez de uma geração por quadro do vídeo.
- O GIF e o SVG do 2.6 podem exigir acesso de preview ou de projeto. GIF tem no máximo 16 quadros e paleta limitada a 256 cores, então não serve como entrega premium.
- Cada geração pode levar até 2 minutos. Use timeout longo e não repita automaticamente um erro moderation_blocked: reescreva o pedido.
- Chave: nunca colocar no HTML das peças, porque o preview do HyperFrames roda no navegador, nem em arquivo dentro de pasta compartilhada. Não digitar a chave no PowerShell, porque fica gravada no histórico. Criar projeto com chave própria e limite de gasto rígido (bloqueia com 429; o alerta de gasto só avisa).
- O GET /v1/models confirma que a chave é válida, mas não prova que a organização está verificada. O primeiro teste real deve ser o mais barato: gpt-image-2.5-flare, low, 1024x1536, cerca de US$ 0,005.
- Não confirmado em fonte oficial: o conteúdo do artigo de verificação e o do artigo de segurança da chave (os dois retornaram 403 ou não foram abertos), a velocidade "50% mais rápido" do 2.6 (só em fontes de terceiros) e a quantidade de tokens de entrada por imagem de referência no 2.5 e no 2.6.