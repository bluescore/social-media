# Imagens com a API da OpenAI

Toda imagem gerada por IA neste projeto sai daqui, com a chave da OpenAI do dono. Não usamos Higgsfield nem outros geradores.

## 1. Cadastrar a chave (uma vez só)

No terminal, dentro de `C:\social-media`:

```
powershell -ExecutionPolicy Bypass -File .\ferramentas\openai\cadastrar-chave.ps1
```

O script pede a chave (ela fica escondida enquanto você cola), testa na OpenAI sem gastar nada, guarda no seu usuário do Windows (variável `OPENAI_API_KEY`) e escolhe o melhor modelo de imagem que a sua conta tem. Nunca cole a chave no chat.

Se aparecer o aviso de "verificação da organização": em platform.openai.com → Settings → Organization → General, clique em Verify Organization. Depois rode o cadastro de novo.

Para trocar a chave, rode o mesmo comando outra vez.

## 2. Gerar uma imagem

```
node ferramentas/openai/gerar-imagem.mjs --prompt "..." --saida caminho/da/imagem.png
```

As opções estão explicadas no topo de `gerar-imagem.mjs`. As principais:

- `--ref imagem.png`: usa uma imagem como referência (por exemplo, para manter a mesma personagem). Pode repetir.
- `--fundo transparent`: PNG sem fundo, para recortar a personagem do cenário.
- `--rascunho`: modelo rápido e qualidade baixa, para testar ideias gastando pouco.
- `--tamanho 1152x2048`: vertical maior (os lados precisam ser múltiplos de 16).

## 3. O que fica registrado

- Ao lado de cada imagem fica um `.json` com o pedido exato e os parâmetros, para refazer igual.
- `registro.csv` (nesta pasta) guarda uma linha por geração, com o custo estimado em dólar.
- `config.json` diz qual modelo usar nas imagens finais e nos rascunhos. O cadastro preenche sozinho.

Preço de referência (tabela oficial da OpenAI, novembro de 2026): US$ 30 por milhão de tokens de imagem gerada. Na prática, uma imagem vertical em qualidade alta custa alguns centavos de dólar; o valor exato de cada uma aparece no terminal e no `registro.csv`.
