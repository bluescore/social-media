# Monta assets\audio\trilha3.mp3 (17,0 s) a partir das gerações do Higgsfield — sem gastar créditos.
#
# Pedido do dono (2026-11-09): a trilha2 era "pesada desde o início"; a nova começa quase em silêncio, vai crescendo
# o tempo todo e tem UM impacto só, na revelação da data (14,833 s, junto com o "plim" do elevador).
#
# Base: fonte\audio\trilha3-a.mp3 (ElevenLabs Music, 100 BPM, cordas em semicolcheias + synth, crescendo natural,
# golpe grave no compasso 7). O que este script faz:
#   1. desloca a música 0,260 s para o golpe dela (14,573 s no arquivo) cair em 14,833 s;
#   2. grave (< 120 Hz) com um "teto" que sobe devagar: o começo fica leve e o "boom" que a música tinha no meio
#      (9,79 s no arquivo -> 10,05 s aqui) vira só o baixo entrando baixinho — o único impacto fica no fim;
#   3. harmônicos do grave (técnica de trilha-celular.py), entrando aos poucos, para o grave aparecer no celular;
#   4. automação de volume: o volume sobe em linha reta (em dB) do começo até o último compasso, ~18 dB no total;
#   5. riser (subida) de 1,55 s antes do golpe: o sopro de riser3-b com um filtro que sobe de 500 Hz a 6 kHz, mais
#      um "eco ao contrário" do impacto; os dois param 20 ms antes do golpe (o respiro faz o golpe bater);
#   6. impacto: golpe grave da própria música + assets\audio\impacto.mp3 (ataque brilhante) com um eco de sala
#      (reverb de 2,2 s) que some até 17,0 s.
# Uso (na pasta do projeto): python -I fonte\montar-trilha3.py [saida.mp3]   (padrão: assets\audio\trilha3.mp3)
import os, sys, subprocess, tempfile
import numpy as np
import soundfile as sf
import pyloudnorm as pyln
from scipy.signal import butter, sosfiltfilt, resample_poly, stft, istft, fftconvolve
from scipy.ndimage import minimum_filter1d, uniform_filter1d

SR = 44100
AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(AQUI, 'audio')
ASSETS = os.path.join(AQUI, '..', 'assets', 'audio')
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ASSETS, 'trilha3.mp3')

DUR = 17.0            # duração final (s)
IMPACTO = 14.833      # ataque do impacto = revelação da data + "plim"
GOLPE_A = 14.573      # ataque do golpe grave em trilha3-a.mp3 (medido)
DESLOC = IMPACTO - GOLPE_A
GOLPE_IMP = 0.0999    # ataque em assets\audio\impacto.mp3 (medido)
SUBIDA = 12.5         # quanto o volume sobe (dB, curto prazo) do começo até o último compasso
                      # (era 18: o começo ficava quase mudo no celular; 12,5 mantém o crescendo e o início leve)
T_INI, T_FIM = 1.2, 14.2   # trecho da rampa de volume
RISER = 1.55          # duração da subida antes do golpe (s)
RESPIRO = 0.020       # silêncio do riser antes do golpe (s)


def ler(caminho, canais=2):
    p = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', caminho, '-ac', str(canais),
                        '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True)
    x = np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)
    return x.reshape(-1, canais) if canais > 1 else x


def salvar(y, caminho, kbps=256):
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, 'x.wav')
        sf.write(w, y.astype(np.float32), SR, subtype='FLOAT')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', w, '-c:a', 'libmp3lame',
                        '-b:a', f'{kbps}k', caminho], check=True)


def n(t):
    return int(round(t * SR))


def rampa(m, sobe=True):
    u = np.linspace(0, 1, m)
    return np.sin(u * np.pi / 2) ** 2 if sobe else np.cos(u * np.pi / 2) ** 2


def curva(pontos, t):
    """Interpola uma curva em dB definida por (tempo, dB)."""
    ts, vs = zip(*pontos)
    return np.interp(t, ts, vs)


def loud_curto(y, janela=1.0, passo=0.05):
    """Volume percebido de curto prazo (LUFS, filtro K, janela centrada) a cada `passo` s."""
    m = pyln.Meter(SR)
    k = y.copy()
    for f in m._filters.values():
        k = f.apply_filter(k)
    ms = (k ** 2).sum(1)
    c = np.concatenate([[0], np.cumsum(ms)])
    ts = np.arange(0, len(y) / SR, passo)
    h = n(janela / 2)
    out = []
    for t in ts:
        a, b = max(0, n(t) - h), min(len(ms), n(t) + h)
        out.append(-0.691 + 10 * np.log10((c[b] - c[a]) / max(1, b - a) + 1e-12))
    return ts, np.array(out)


# ------------------------------------------------------------------ 1) música deslocada
a = ler(os.path.join(FONTE, 'trilha3-a.mp3'))
N = n(DUR)
mus = np.zeros((N, 2))
seg = a[:N - n(DESLOC)]
mus[n(DESLOC):n(DESLOC) + len(seg)] = seg
t = np.arange(N) / SR

# ------------------------------------------------------------------ 2) grave com teto que sobe
lo = sosfiltfilt(butter(4, 120, 'low', fs=SR, output='sos'), mus, axis=0)
hi = mus - lo                                     # soma exata: hi + lo = música original
env = np.sqrt(np.maximum(uniform_filter1d((lo ** 2).mean(1), size=n(0.03)), 1e-14))
teto_db = curva([(0, -60), (3, -58), (9.5, -48), (12.5, -40), (14.6, -33), (IMPACTO - 0.06, -33),
                 (IMPACTO - 0.02, 0), (DUR, 0)], t)
g = np.minimum(1.0, 10 ** (teto_db / 20) / env)
g = minimum_filter1d(g, size=2 * n(0.025) + 1)    # começa a segurar um pouco antes do ataque (sem estalo)
g = uniform_filter1d(g, size=n(0.025))
lo = lo * g[:, None]
reducao = -20 * np.log10(np.maximum(g, 1e-9))
# o ataque desse "boom" também tinha médios ~5 dB acima dos outros acentos: nivela só esse instante (10,0–10,15 s)
# pelo maior acento do compasso anterior, para ele soar como mais uma batida e não como um segundo impacto
eh = np.sqrt(np.maximum(uniform_filter1d((hi ** 2).mean(1), size=n(0.01)), 1e-14))
ref_hi = np.percentile(eh[n(9.0):n(9.98)], 99.5)
gh = np.ones(N)
z = slice(n(9.99), n(10.16))
gh[z] = np.minimum(1.0, ref_hi / eh[z])
gh = uniform_filter1d(minimum_filter1d(gh, size=2 * n(0.01) + 1), size=n(0.01))
hi = hi * gh[:, None]

# ------------------------------------------------------------------ 3) harmônicos do grave (celular)
def harmonicos(x, drive=4.0, even=0.3, hp=220, lp=4000):
    """Cópia saturada do grave, só acima de 220 Hz (o que o alto-falante do celular consegue tocar)."""
    pk = np.abs(x).max()
    u = x / pk
    e = np.sqrt(np.maximum(uniform_filter1d(u ** 2, size=n(0.02), axis=0), 0))
    e = np.maximum(sosfiltfilt(butter(2, 30, 'low', fs=SR, output='sos'), e, axis=0), 0)
    un = u / (e + 0.02 * e.max())
    s = resample_poly(np.tanh(drive * resample_poly(un, 4, 1, axis=0)), 1, 4, axis=0)[:len(un)]
    h = ((1 - even) * s + even * np.abs(s)) * e
    h = sosfiltfilt(butter(4, hp, 'high', fs=SR, output='sos'), h, axis=0)
    h = sosfiltfilt(butter(2, lp, 'low', fs=SR, output='sos'), h, axis=0)
    return h * pk


lo_h = sosfiltfilt(butter(4, 180, 'low', fs=SR, output='sos'), lo, axis=0)
harm = harmonicos(lo_h)
harm *= 10 ** (curva([(0, -60), (9.5, -60), (11.0, 2), (IMPACTO, 10), (DUR, 10)], t) / 20)[:, None]
y = hi + lo + harm

# ------------------------------------------------------------------ 4) automação de volume (crescendo contínuo)
ts, L = loud_curto(y)
alvo_fim = np.interp(T_FIM, ts, L)
alvo = alvo_fim - SUBIDA * (1 - np.clip((ts - T_INI) / (T_FIM - T_INI), 0, 1))
G = np.clip(alvo - L, -16, 3)
G[ts > T_FIM] = np.interp(T_FIM, ts, G)
G[ts < T_INI] = np.interp(T_INI, ts, G)
G = uniform_filter1d(uniform_filter1d(G, size=21, mode='nearest'), size=21, mode='nearest')  # ~1 s, sem degraus
gain = 10 ** (np.interp(t, ts, G) / 20)
y *= gain[:, None]
# entrada: a música nasce do silêncio logo no começo (0,45 s de subida a partir de ~0,3 s)
ini = n(DESLOC + 0.05)
fi = np.ones(N); fi[:ini] = 0; fi[ini:ini + n(0.45)] = rampa(n(0.45))
y *= fi[:, None]

# ------------------------------------------------------------------ 6) impacto (antes do riser, que usa o eco dele)
imp = ler(os.path.join(ASSETS, 'impacto.mp3'), 1)
rng = np.random.default_rng(1611)
ti = np.arange(n(2.6)) / SR
ir = rng.standard_normal((len(ti), 2)) * (10 ** (-3 * ti / 2.2))[:, None]          # RT60 = 2,2 s
ir = sosfiltfilt(butter(2, [200, 6000], 'band', fs=SR, output='sos'), ir, axis=0)
ir[:n(0.01)] *= rampa(n(0.01))[:, None]
ir = np.vstack([np.zeros((n(0.025), 2)), ir])                                       # pré-atraso de 25 ms
imp_hp = sosfiltfilt(butter(2, 150, 'high', fs=SR, output='sos'), imp)
eco = np.stack([fftconvolve(imp_hp, ir[:, c]) for c in range(2)], 1)
eco *= np.sqrt((imp ** 2).sum()) / np.sqrt((eco ** 2).sum() / 2) * 10 ** (-7 / 20)  # eco 7 dB abaixo do golpe
golpe = np.zeros((len(eco), 2))
golpe[:len(imp)] += imp[:, None]
golpe += eco
# nível: o pico do impacto.mp3 igual ao pico do golpe grave da música (já com a automação)
j0 = n(IMPACTO)
pk_mus = np.abs(y[j0:j0 + n(0.12)]).max()
golpe *= pk_mus / np.abs(imp).max()
k0 = j0 - n(GOLPE_IMP)
m = min(len(golpe), N - k0)
y[k0:k0 + m] += golpe[:m]

# ------------------------------------------------------------------ 5) riser antes do golpe
r = ler(os.path.join(FONTE, 'riser3-b.mp3'), 1)[n(1.0):n(1.0 + RISER)]
f, tt, Z = stft(r, fs=SR, nperseg=2048, noverlap=2048 - 256)
u = np.clip(tt / RISER, 0, 1)
fc = 500 * (6000 / 500) ** (u ** 1.2)                                               # filtro sobe 500 Hz -> 6 kHz
lf = np.log2(np.maximum(f, 20))[:, None]
M = 0.04 + 0.96 * np.exp(-0.5 * ((lf - np.log2(fc)[None, :]) / 1.3) ** 2)
M *= (10 ** ((-30 + 30 * u ** 2) / 20))[None, :]                                    # -30 dB -> 0 dB, acelerando
_, rs = istft(Z * M, fs=SR, nperseg=2048, noverlap=2048 - 256)
rs = rs[:len(r)]
rs[:n(0.05)] *= rampa(n(0.05))
# eco ao contrário do impacto (0,7 s), só médios e agudos
rev = eco[n(GOLPE_IMP + 0.025):n(GOLPE_IMP + 0.025 + 0.7)].mean(1)[::-1].copy()   # começo do eco, invertido
rev = sosfiltfilt(butter(2, 300, 'high', fs=SR, output='sos'), rev)
rev *= rampa(len(rev)) ** 1.5
fim = j0 - n(RESPIRO)
# nível: o fim do riser no mesmo volume (médios/agudos) que a música no último compasso
med = lambda s: np.sqrt(np.mean(sosfiltfilt(butter(2, [400, 6000], 'band', fs=SR, output='sos'), s, axis=0) ** 2))
ref = med(y[n(13.6):n(14.4)].mean(1))
rs *= ref / med(rs[-n(0.25):]) * 10 ** (3.0 / 20)
rev *= ref / med(rev[-n(0.15):]) * 10 ** (-4.0 / 20)
for s_ in (rs, rev):
    s_[-n(0.008):] *= rampa(n(0.008), False)
    y[fim - len(s_):fim] += s_[:, None]

# ------------------------------------------------------------------ fim: a cauda some até 17,0 s
y[n(16.25):] *= rampa(N - n(16.25), False)[:, None]
y *= 10 ** (-1.5 / 20) / np.abs(y).max()            # pico em -1,5 dBFS (o impacto)

salvar(y, SAIDA)
print(f'deslocamento {DESLOC:.3f} s; impacto em {IMPACTO} s; redução máx do grave {reducao.max():.1f} dB '
      f'em {t[np.argmax(reducao)]:.2f} s; automação {G.min():+.1f} .. {G.max():+.1f} dB -> {SAIDA}')
