// Render do teaser: Playwright (Chrome do sistema) + FFmpeg.
//   node render.mjs beats            -> uma imagem por batida (e meia batida) em frames/
//   node render.mjs at 3.2 4.75      -> imagens em tempos específicos
//   node render.mjs audio            -> gera audio.wav pelo Web Audio (OfflineAudioContext)
//   node render.mjs full <saida.mp4> -> 60 fps, 3 subquadros por quadro misturados (tmix), com áudio
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { chromium } from 'playwright-core';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const DUR = 15, FPS = 60, SUB = 3, BEAT = 0.75;
const VERT = !!process.env.VERT; // VERT=1 => versão vertical 1080x1920 (index.html?v)
const VW = VERT ? 1080 : 1920, VH = VERT ? 1920 : 1080;
const TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.ttf': 'font/ttf', '.otf': 'font/otf' };

function serve() {
  return new Promise(res => {
    const srv = http.createServer((req, r) => {
      const p = path.join(ROOT, decodeURIComponent(req.url.split('?')[0]));
      if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { r.writeHead(404); r.end(); return; }
      r.writeHead(200, { 'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream' });
      fs.createReadStream(p).pipe(r);
    });
    srv.listen(0, '127.0.0.1', () => res(srv));
  });
}

async function open(srv, page = 'index.html') {
  const browser = await chromium.launch({ channel: 'chrome', headless: true, args: ['--force-color-profile=srgb', '--disable-lcd-text', '--font-render-hinting=none'] });
  const ctx = await browser.newContext({ viewport: { width: VW, height: VH }, deviceScaleFactor: 1 });
  const pg = await ctx.newPage();
  pg.on('console', m => console.log('[page]', m.text()));
  pg.on('pageerror', e => console.log('[page error]', e.message));
  await pg.goto(`http://127.0.0.1:${srv.address().port}/${page}${VERT && page === 'index.html' ? '?v' : ''}`);
  await pg.evaluate(() => window.ready);
  return { browser, pg };
}

async function shot(pg, cdp, t) {
  await pg.evaluate(t => window.seek(t), t);
  const { data } = await cdp.send('Page.captureScreenshot', { format: 'png', optimizeForSpeed: true });
  return Buffer.from(data, 'base64');
}

const mode = process.argv[2] || 'beats';
const srv = await serve();
try {
  if (mode === 'audio') {
    const { browser, pg } = await open(srv, 'audio.html');
    const b64 = await pg.evaluate(() => window.renderAudio());
    fs.writeFileSync(path.join(ROOT, 'audio.wav'), Buffer.from(b64, 'base64'));
    console.log('audio.wav ok');
    await browser.close();
  } else if (mode === 'beats' || mode === 'at') {
    const { browser, pg } = await open(srv);
    const cdp = await pg.context().newCDPSession(pg);
    const dir = path.join(ROOT, 'frames');
    fs.mkdirSync(dir, { recursive: true });
    const times = mode === 'at' ? process.argv.slice(3).map(Number)
      : Array.from({ length: Math.round(DUR / BEAT) + 1 }, (_, i) => i * BEAT);
    for (const t of times) {
      const buf = await shot(pg, cdp, t);
      const name = `t${t.toFixed(2).padStart(5, '0')}.png`;
      fs.writeFileSync(path.join(dir, name), buf);
    }
    console.log('frames:', times.length);
    await browser.close();
  } else if (mode === 'full') {
    const out = path.resolve(process.argv[3] || path.join(ROOT, 'teaser.mp4'));
    const silent = path.join(ROOT, 'video-sem-som.mp4');
    const { browser, pg } = await open(srv);
    const cdp = await pg.context().newCDPSession(pg);
    // cada quadro i junta 3 subquadros em i/60 - 1/180, i/60, i/60 + 1/180
    const ff = spawn('ffmpeg', ['-y', '-v', 'error', '-f', 'image2pipe', '-c:v', 'png', '-framerate', String(FPS * SUB), '-i', '-',
      '-vf', `tmix=frames=${SUB}:weights='1 1 1',select='eq(mod(n\\,${SUB})\\,${SUB - 1})',setpts=N/(${FPS}*TB),scale=out_color_matrix=bt709:out_range=tv,format=yuv420p`,
      '-r', String(FPS), '-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-profile:v', 'high',
      '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-movflags', '+faststart', silent], { stdio: ['pipe', 'inherit', 'inherit'] });
    const total = DUR * FPS * SUB;
    const t0 = Date.now();
    for (let j = 0; j < total; j++) {
      const t = (j - 1) / (FPS * SUB);
      const buf = await shot(pg, cdp, t);
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (j % 180 === 0) console.log(`subquadro ${j}/${total}  ${((Date.now() - t0) / 1000).toFixed(0)} s`);
    }
    ff.stdin.end();
    await new Promise((res, rej) => ff.on('close', c => c === 0 ? res() : rej(new Error('ffmpeg ' + c))));
    await browser.close();
    const wav = path.join(ROOT, 'audio.wav');
    await new Promise((res, rej) => {
      const m = spawn('ffmpeg', ['-y', '-v', 'error', '-i', silent, '-i', wav, '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-t', String(DUR), '-movflags', '+faststart', out], { stdio: 'inherit' });
      m.on('close', c => c === 0 ? res() : rej(new Error('mux ' + c)));
    });
    console.log('pronto:', out);
  }
} finally {
  srv.close();
}
