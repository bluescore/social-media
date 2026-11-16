# Social media — edição de vídeo com IA

O dono desta pasta está começando em edição de vídeo agora. Explique tudo em português simples, sem jargão; quando precisar de um termo técnico, explique em uma frase.

## Ferramentas

- **Remotion** (`remotion\`): vídeos em React. Use para reels com a pessoa falando, legenda automática e moldes reaproveitáveis (mesmo vídeo, várias variações).
- **HyperFrames** (`hyperframes\`): vídeos em HTML + CSS + GSAP. Use para peças animadas sem gravação: aberturas, anúncios, explicativos, texto animado.
- **Carrossel animado** (dentro de `remotion\`): post em carrossel do Instagram em que cada slide é um vídeo curto em loop. Sempre pela skill `carrossel-animado` (`.claude\skills\carrossel-animado\`), que traz o método; leia-a inteira antes de começar. Motor em `remotion\src\carrossel\`, cada carrossel em `remotion\src\carrosseis\AAAA-MM-DD_nome\`.
- Se o pedido não disser qual usar, escolha pelo critério acima e diga qual escolheu e por quê.
- **Imagens geradas por IA**: só pela API da OpenAI, com a chave do dono, via `node ferramentas\openai\gerar-imagem.mjs` (instruções em `ferramentas\openai\LEIA-ME.md`). Não use Higgsfield nem outros geradores de imagem. ElevenLabs só para voz/áudio. Se a chave não estiver cadastrada, peça ao dono para rodar `ferramentas\openai\cadastrar-chave.ps1` no terminal; nunca peça a chave no chat.

## Pastas

| Pasta | Quem mexe | O que vai |
|---|---|---|
| `marca\` | dono (uma vez) | `logo\` e `grafismos\` (PNG transparente), `fontes\`, `musicas\`; cores, tom de voz e regras em `marca.md` |
| `brutos\` | dono | vídeos crus, áudios e fotos — uma subpasta por vídeo: `AAAA-MM-DD_nome-do-video\` |
| `remotion\` | Claude | um único projeto Remotion; cada vídeo é uma composição em `src\` |
| `hyperframes\` | Claude | um projeto HyperFrames por peça: `hyperframes\nome-da-peca\` |
| `ferramentas\` | Claude | scripts de apoio; `openai\` = cadastro da chave e gerador de imagens (com `registro.csv` de custos) |
| `prontos\` | Claude salva, dono posta | MP4 finais: `AAAA-MM-DD_nome-do-video.mp4`; carrossel = pasta `AAAA-MM-DD_nome\` com `01.mp4`, `01.png`... e `legenda.txt` |

Regras:
- Nunca altere nem apague arquivos de `brutos\` e `marca\` — copie para dentro do projeto (Remotion: `remotion\public\`; HyperFrames: pasta da peça) antes de usar.
- Formato padrão: vertical 1080×1920, 30 fps, MP4 H.264 — salvo pedido diferente. Carrossel: 1080×1350 (4:5), 6 s por slide.
- Vídeo de iPhone em HEVC/H.265: converta para H.264 com o FFmpeg antes de usar.
- Antes de renderizar a versão final, mostre a prévia (Remotion Studio ou `hyperframes preview`) e espere o ok.

## Marca

- A marca é a **Sabiá Lab** (antiga Blue Score). Cores, fontes, logos, sementes e tom de voz: `marca\marca.md`. Textos dos vídeos seguem o tom de voz de lá.
- Remotion: importe cores e fontes de `src\marca\marca.ts` e o logo de `src\marca\Logo.tsx`; nunca digite cor ou fonte na mão. Arquivos em `remotion\public\marca\`.
- HyperFrames: peça nova = cópia de `hyperframes\_molde-sabia\` (já tem fonte, logos, sementes e a vinheta em `compositions\vinheta.html`).
- Se algo em `marca\` mudar, recopie para `remotion\public\marca\` e para `hyperframes\_molde-sabia\assets\`.

## Comandos

- Remotion — prévia: `cd remotion; npx remotion studio` · render: `npx remotion render <Id> ..\prontos\<arquivo>.mp4`
- HyperFrames — prévia: `cd hyperframes\<peca>; npx hyperframes preview` · render: `npx hyperframes render`
- Carrossel (dentro de `remotion\`) — conferir: `npm run carrossel:conferir -- <nome>` · render: `npm run carrossel:render -- <nome>` (salva em `prontos\<pasta>\`)
