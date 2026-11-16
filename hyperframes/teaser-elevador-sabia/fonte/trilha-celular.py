# trilha2-celular.mp3: a MESMA trilha2.mp3 tratada para aparecer no alto-falante de celular (sem créditos).
# Gera harmônicos do grave (cópia do grave saturada, só acima de 220 Hz) somados por baixo do original,
# +3 dB de brilho acima de 2,5 kHz, e um limitador que segura o pico em -2 dBFS. Filtros de fase zero:
# as batidas ficam nos mesmos instantes; o corte seco em 13,25 s segue o envelope do original.
# Uso (na pasta do projeto):
#   ffmpeg -i assets\audio\trilha2.mp3 -c:a pcm_f32le trilha2.wav
#   python -I fonte\trilha-celular.py trilha2.wav trilha2-celular.wav "{\"hgain_db\":15,\"hgain_main_db\":8,\"drive\":4,\"even\":0.3,\"lp\":4000,\"shelf_db\":3,\"thr\":-2.0}"
#   ffmpeg -i trilha2-celular.wav -c:a libmp3lame -b:a 256k assets\audio\trilha2-celular.mp3
import sys, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt, iirfilter, resample_poly
from scipy.ndimage import minimum_filter1d, uniform_filter1d

def biquad_highshelf(f0, gain_db, fs, S=1.0):
    A = 10**(gain_db/40); w0 = 2*np.pi*f0/fs; cw, sw = np.cos(w0), np.sin(w0)
    alpha = sw/2*np.sqrt((A+1/A)*(1/S-1)+2)
    b0 = A*((A+1)+(A-1)*cw+2*np.sqrt(A)*alpha); b1 = -2*A*((A-1)+(A+1)*cw); b2 = A*((A+1)+(A-1)*cw-2*np.sqrt(A)*alpha)
    a0 = (A+1)-(A-1)*cw+2*np.sqrt(A)*alpha; a1 = 2*((A-1)-(A+1)*cw); a2 = (A+1)-(A-1)*cw-2*np.sqrt(A)*alpha
    return np.array([[b0/a0,b1/a0,b2/a0,1,a1/a0,a2/a0]])

def biquad_peak(f0, gain_db, Q, fs):
    A = 10**(gain_db/40); w0 = 2*np.pi*f0/fs; alpha = np.sin(w0)/(2*Q); cw=np.cos(w0)
    b = [1+alpha*A, -2*cw, 1-alpha*A]; a = [1+alpha/A, -2*cw, 1-alpha/A]
    return np.array([[b[0]/a[0], b[1]/a[0], b[2]/a[0], 1, a[1]/a[0], a[2]/a[0]]])

def limiter(x, sr, thr_db=-2.0, look=0.008):
    thr = 10**(thr_db/20)
    pk = np.abs(x).max(1) if x.ndim==2 else np.abs(x)
    raw = np.minimum(1.0, thr/np.maximum(pk,1e-9))
    L = int(look*sr)
    g = minimum_filter1d(raw, size=2*L+1)
    g = uniform_filter1d(g, size=L)
    g = np.minimum(g, raw)  # safety
    return x*g[:,None], g

def run(src, dst, drive=3.5, even=0.5, hgain_db=0.0, hgain_main_db=None, xf=(7.10,7.235), hp=220, lp=3500, lo_cut=180, shelf_db=3.0, shelf_f=2500, thr=-2.0):
    x, sr = sf.read(src)
    lo = sosfiltfilt(butter(4, lo_cut, 'low', fs=sr, output='sos'), x, axis=0)
    pk = np.abs(lo).max()
    u = lo/pk
    # follow the bass level (20 ms), saturate the level-normalised bass, then give the level back
    env = np.sqrt(np.maximum(uniform_filter1d(u**2, size=int(0.02*sr), axis=0), 0))
    env = sosfiltfilt(butter(2, 30, 'low', fs=sr, output='sos'), env, axis=0); env = np.maximum(env, 0)
    un = u/(env + 0.02*env.max())
    t = resample_poly(np.tanh(drive*resample_poly(un, 4, 1, axis=0)), 1, 4, axis=0)[:len(un)]  # 4x oversampled
    odd = t
    ev = np.abs(t)
    h = ((1-even)*odd + even*ev)*env
    h = sosfiltfilt(butter(4, hp, 'high', fs=sr, output='sos'), h, axis=0)
    h = sosfiltfilt(butter(2, lp, 'low', fs=sr, output='sos'), h, axis=0)
    gcurve = np.full(len(h), 10**(hgain_db/20))
    if hgain_main_db is not None:
        a, b = int(xf[0]*sr), int(xf[1]*sr)
        g2 = 10**(hgain_main_db/20)
        gcurve[a:b] = np.linspace(gcurve[0], g2, b-a); gcurve[b:] = g2
    h = h * pk * gcurve[:,None]
    y = x + h
    # presence: zero-phase high shelf (filtfilt doubles the dB, so design half)
    y = sosfiltfilt(biquad_highshelf(shelf_f, shelf_db/2, sr), y, axis=0)
    # recreate the dry cut: follow the original's envelope after 13.20 s
    n0 = int(13.20*sr); w = int(0.003*sr)
    eo = np.sqrt(np.maximum(uniform_filter1d((x**2).mean(1), size=w),0))
    ey = np.sqrt(np.maximum(uniform_filter1d((y**2).mean(1), size=w),0))
    gate = np.ones(len(x))
    tail = np.minimum(1.0, eo[n0:]/np.maximum(ey[n0:],1e-9))
    gate[n0:] = np.minimum(1.0, tail)
    y = y*gate[:,None]
    y, g = limiter(y, sr, thr)
    grd = -20*np.log10(g)
    for a,b in [(0,7.2),(7.2,13.27)]:
        seg = grd[int(a*sr):int(b*sr)]
        print(f'  GR {a}-{b}s: max {seg.max():.2f} dB, tempo com >1 dB {100*(seg>1).mean():.2f}%')
    sf.write(dst, y.astype(np.float32), sr, subtype='FLOAT')
    gr = -20*np.log10(g)
    return {'max_gr_db': round(float(gr.max()),2), 'pct_gr_gt1db': round(100*float((gr>1).mean()),2), 'h_rms_db': round(float(20*np.log10(np.sqrt((h**2).mean())+1e-12)),1)}

if __name__=='__main__':
    kw = json.loads(sys.argv[3]) if len(sys.argv)>3 else {}
    print(run(sys.argv[1], sys.argv[2], **kw))
