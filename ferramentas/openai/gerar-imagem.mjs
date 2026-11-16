#!/usr/bin/env node
// Gera imagens com a API da OpenAI usando a chave do dono (variável OPENAI_API_KEY).
// É o ÚNICO caminho de geração de imagem deste projeto (nada de Higgsfield ou outros).
//
// Exemplos (rodar dentro de C:\social-media):
//   node ferramentas/openai/gerar-imagem.mjs --prompt "uma xícara laranja em fundo claro" --saida hyperframes/minha-peca/assets/ia/xicara.png
//   node ferramentas/openai/gerar-imagem.mjs --prompt-arquivo prompts/cena1.txt --saida cena1.png --tamanho 1152x2048
//   node ferramentas/openai/gerar-imagem.mjs --prompt "mesma personagem, sentada" --ref personagem.png --fundo transparent --saida pose2.png
//   node ferramentas/openai/gerar-imagem.mjs --rascunho --n 3 --prompt "..." --saida teste.png   (modelo rápido + qualidade baixa, barato)
//
// Opções:
//   --prompt "texto" | --prompt-arquivo caminho.txt   o pedido (arquivo em UTF-8 evita problema de acento)
//   --saida caminho.png       onde salvar (com --n > 1 vira caminho-1.png, caminho-2.png...)
//   --ref imagem.png          imagem de referência (pode repetir); com --ref usa o modo "editar"
//   --tamanho LxA             padrão do config.json; múltiplos de 16, lado máx. 3840 (ex.: 1024x1536, 1152x2048)
//   --qualidade low|medium|high|xhigh|max
//   --fundo transparent|opaque|auto
//   --formato png|webp|jpeg
//   --n N                     quantas variações (padrão 1)
//   --modelo id               força um modelo
//   --rascunho                usa modelo_rascunho + qualidade_rascunho do config.json
//
// Cada imagem ganha um .json ao lado (prompt e parâmetros, para refazer igual) e uma linha em registro.csv (custo estimado).

import { readFileSync, writeFileSync, appendFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, extname, basename, join, resolve } from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const PASTA = dirname(fileURLToPath(import.meta.url));
const config = JSON.parse(readFileSync(join(PASTA, 'config.json'), 'utf8').replace(/^\uFEFF/, ''));
// Preço por milhão de tokens (família gpt-image-2.5/2.6, tabela oficial de 2026-11). Só para estimar.
const PRECO = { saida_imagem: 30, entrada_imagem: 8, entrada_texto: 5 };

function lerArgs(argv) {
  const a = { ref: [] };
  for (let i = 0; i < argv.length; i++) {
    const k = argv[i];
    const v = () => argv[++i];
    switch (k) {
      case '--prompt': a.prompt = v(); break;
      case '--prompt-arquivo': a.promptArquivo = v(); break;
      case '--saida': a.saida = v(); break;
      case '--ref': a.ref.push(v()); break;
      case '--tamanho': a.tamanho = v(); break;
      case '--qualidade': a.qualidade = v(); break;
      case '--fundo': a.fundo = v(); break;
      case '--formato': a.formato = v(); break;
      case '--n': a.n = parseInt(v(), 10); break;
      case '--modelo': a.modelo = v(); break;
      case '--rascunho': a.rascunho = true; break;
      default: throw new Error(`Opção desconhecida: ${k}`);
    }
  }
  return a;
}

function pegarChave() {
  if (process.env.OPENAI_API_KEY) return process.env.OPENAI_API_KEY.trim();
  // A sessão pode ter aberto antes do cadastro: lê direto do registro do usuário no Windows.
  if (process.platform === 'win32') {
    try {
      const out = execFileSync('reg', ['query', 'HKCU\\Environment', '/v', 'OPENAI_API_KEY'], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
      const m = out.match(/OPENAI_API_KEY\s+REG_\w+\s+(\S+)/);
      if (m) return m[1].trim();
    } catch {}
  }
  throw new Error('Chave da OpenAI não encontrada. Rode: powershell -ExecutionPolicy Bypass -File .\\ferramentas\\openai\\cadastrar-chave.ps1');
}

function validarTamanho(t) {
  if (t === 'auto') return;
  const m = /^(\d+)x(\d+)$/.exec(t || '');
  if (!m) throw new Error(`Tamanho inválido: ${t} (use LxA, ex.: 1024x1536)`);
  const [w, h] = [Number(m[1]), Number(m[2])];
  if (w % 16 || h % 16) throw new Error(`Largura e altura precisam ser múltiplos de 16 (${t}). Para vertical use 1024x1536 ou 1152x2048.`);
  if (Math.max(w, h) > 3840) throw new Error('Nenhum lado pode passar de 3840 px.');
  if (Math.max(w / h, h / w) > 3) throw new Error('Proporção máxima é 1:3.');
}

const tipoPorExt = { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp' };

async function main() {
  const a = lerArgs(process.argv.slice(2));
  const prompt = a.promptArquivo ? readFileSync(a.promptArquivo, 'utf8').replace(/^\uFEFF/, '').trim() : a.prompt;
  if (!prompt) throw new Error('Falta o pedido: use --prompt "..." ou --prompt-arquivo arquivo.txt');
  if (!a.saida) throw new Error('Falta --saida caminho.png');

  const modelo = a.modelo || (a.rascunho ? config.modelo_rascunho : config.modelo_final);
  const qualidade = a.qualidade || (a.rascunho ? config.qualidade_rascunho : config.qualidade_final);
  const tamanho = a.tamanho || config.tamanho_padrao;
  const formato = a.formato || (extname(a.saida).slice(1).toLowerCase().replace('jpg', 'jpeg') || 'png');
  const n = a.n || 1;
  validarTamanho(tamanho);
  if (a.fundo === 'transparent' && formato === 'jpeg') throw new Error('Fundo transparente só funciona em png ou webp.');

  const chave = pegarChave();
  const editar = a.ref.length > 0;
  const url = `https://api.openai.com/v1/images/${editar ? 'edits' : 'generations'}`;
  let corpo, headers = { Authorization: `Bearer ${chave}` };

  if (editar) {
    const fd = new FormData();
    fd.append('model', modelo);
    fd.append('prompt', prompt);
    fd.append('size', tamanho);
    fd.append('quality', qualidade);
    fd.append('n', String(n));
    fd.append('output_format', formato);
    if (a.fundo) fd.append('background', a.fundo);
    for (const r of a.ref) {
      if (!existsSync(r)) throw new Error(`Referência não encontrada: ${r}`);
      const tipo = tipoPorExt[extname(r).toLowerCase()];
      if (!tipo) throw new Error(`Referência precisa ser png, jpg ou webp: ${r}`);
      fd.append('image[]', new Blob([readFileSync(r)], { type: tipo }), basename(r));
    }
    corpo = fd;
  } else {
    headers['Content-Type'] = 'application/json';
    const json = { model: modelo, prompt, size: tamanho, quality: qualidade, n, output_format: formato };
    if (a.fundo) json.background = a.fundo;
    corpo = JSON.stringify(json);
  }

  console.log(`Gerando ${n} imagem(ns) com ${modelo} (${qualidade}, ${tamanho}${editar ? `, ${a.ref.length} referência(s)` : ''})... pode levar até 2 minutos.`);
  const t0 = Date.now();
  const resp = await fetch(url, { method: 'POST', headers, body: corpo, signal: AbortSignal.timeout(300000) });
  const dados = await resp.json().catch(() => ({}));
  if (!resp.ok) {
    const e = dados.error || {};
    if (e.code === 'moderation_blocked') throw new Error(`A OpenAI bloqueou o pedido pelo filtro de conteúdo (${JSON.stringify(e.moderation_details || {})}). Reescreva o prompt.`);
    if (resp.status === 401) throw new Error('Chave recusada (401). Rode o cadastro de novo.');
    if (resp.status === 403 || e.code === 'model_not_found') throw new Error(`Modelo ${modelo} indisponível nesta conta (${e.message || resp.status}). Rode o cadastro de novo para escolher outro, ou verifique a organização na OpenAI.`);
    throw new Error(`Erro ${resp.status}: ${e.message || JSON.stringify(dados)}`);
  }

  const imgs = dados.data || [];
  const saidaAbs = resolve(a.saida);
  mkdirSync(dirname(saidaAbs), { recursive: true });
  const base = saidaAbs.slice(0, saidaAbs.length - extname(saidaAbs).length);
  const ext = extname(saidaAbs) || `.${formato}`;
  const arquivos = imgs.map((img, i) => {
    const p = imgs.length > 1 ? `${base}-${i + 1}${ext}` : `${base}${ext}`;
    writeFileSync(p, Buffer.from(img.b64_json, 'base64'));
    return p;
  });

  const u = dados.usage || {};
  const det = u.input_tokens_details || {};
  const custo = ((u.output_tokens || 0) * PRECO.saida_imagem + (det.image_tokens || 0) * PRECO.entrada_imagem + (det.text_tokens || 0) * PRECO.entrada_texto) / 1e6;
  const segundos = ((Date.now() - t0) / 1000).toFixed(0);

  const ficha = { data: new Date().toISOString(), modelo, qualidade, tamanho, formato, fundo: a.fundo || 'auto', n, referencias: a.ref, prompt, arquivos, usage: u, custo_estimado_usd: Number(custo.toFixed(4)), segundos: Number(segundos) };
  writeFileSync(`${base}.json`, JSON.stringify(ficha, null, 2));

  const reg = join(PASTA, 'registro.csv');
  if (!existsSync(reg)) writeFileSync(reg, 'data;modelo;qualidade;tamanho;n;referencias;arquivo;tokens_saida;custo_estimado_usd\n');
  appendFileSync(reg, [ficha.data, modelo, qualidade, tamanho, n, a.ref.length, arquivos[0], u.output_tokens || '', custo.toFixed(4)].join(';') + '\n');

  for (const p of arquivos) console.log(`Salvo: ${p}`);
  console.log(`Tempo: ${segundos} s · custo estimado: US$ ${custo.toFixed(3)}`);
}

main().catch((e) => {
  console.error(`ERRO: ${e.message}`);
  process.exit(1);
});
