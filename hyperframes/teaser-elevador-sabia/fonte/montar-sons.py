# Monta os sons novos do teaser a partir das gerações do Higgsfield (fonte\audio\) — sem gastar créditos.
#   hall2.mp3     ambiente do hall (hall2-a sem os 3 eventos, com graves cortados e médios/agudos realçados)
#   chegada2.mp3  elevador chegando (cama de chegada2-b subindo de tom + "tics" de chegada2-a acelerando)
#   impacto.mp3   impacto da entrada pela janela (impacto-b recortado, cauda de ~1 s)
#   subir.mp3     acento do "SUBIR" (sopro subindo de subir-c que termina no golpe seco de subir-b)
# Uso: python -I fonte\montar-sons.py [pasta_de_saida]   (padrão: assets\audio)
import os, sys, subprocess, tempfile
import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt, sosfiltfilt

SR = 44100
AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE = os.path.join(AQUI, 'audio')
SAIDA = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AQUI, '..', 'assets', 'audio')


def ler(nome):
    """Decodifica fonte\\audio\\<nome>.mp3 com o ffmpeg (mesmo decodificador do navegador) em mono 44,1 kHz."""
    p = subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i', os.path.join(FONTE, nome + '.mp3'),
                        '-ac', '1', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True)
    return np.frombuffer(p.stdout, dtype=np.float32).astype(np.float64)


def salvar(nome, y, kbps=192):
    with tempfile.TemporaryDirectory() as d:
        w = os.path.join(d, 'x.wav')
        sf.write(w, y.astype(np.float32), SR, subtype='FLOAT')
        subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', w, '-c:a', 'libmp3lame',
                        '-b:a', f'{kbps}k', os.path.join(SAIDA, nome + '.mp3')], check=True)


def trecho(x, a, b):
    return x[int(round(a * SR)):int(round(b * SR))].copy()


def rampa(n, sobe=True):
    t = np.linspace(0, 1, n)
    return np.sin(t * np.pi / 2) if sobe else np.cos(t * np.pi / 2)


def emendar(partes, xf=0.06):
    """Junta trechos de ruído com cruzamento de potência constante (xf segundos)."""
    n = int(xf * SR)
    out = partes[0].copy()
    for p in partes[1:]:
        out[-n:] = out[-n:] * rampa(n, False) + p[:n] * rampa(n, True)
        out = np.concatenate([out, p[n:]])
    return out


def bordas(y, ini=0.02, fim=0.02):
    a, b = int(ini * SR), int(fim * SR)
    if a: y[:a] *= rampa(a, True)
    if b: y[-b:] *= rampa(b, False)
    return y


def shelf_agudo(f0, g_db, S=0.8):
    A = 10 ** (g_db / 40); w0 = 2 * np.pi * f0 / SR; cw, sw = np.cos(w0), np.sin(w0)
    al = sw / 2 * np.sqrt((A + 1 / A) * (1 / S - 1) + 2)
    b0 = A * ((A + 1) + (A - 1) * cw + 2 * np.sqrt(A) * al); b1 = -2 * A * ((A - 1) + (A + 1) * cw)
    b2 = A * ((A + 1) + (A - 1) * cw - 2 * np.sqrt(A) * al)
    a0 = (A + 1) - (A - 1) * cw + 2 * np.sqrt(A) * al; a1 = 2 * ((A - 1) - (A + 1) * cw)
    a2 = (A + 1) - (A - 1) * cw - 2 * np.sqrt(A) * al
    return np.array([[b0 / a0, b1 / a0, b2 / a0, 1, a1 / a0, a2 / a0]])


def realce(f0, g_db, Q=0.7):
    A = 10 ** (g_db / 40); w0 = 2 * np.pi * f0 / SR; al = np.sin(w0) / (2 * Q); cw = np.cos(w0)
    b = [1 + al * A, -2 * cw, 1 - al * A]; a = [1 + al / A, -2 * cw, 1 - al / A]
    return np.array([[b[0] / a[0], b[1] / a[0], b[2] / a[0], 1, a[1] / a[0], a[2] / a[0]]])


def pico(y, alvo_db):
    return y * (10 ** (alvo_db / 20) / np.abs(y).max())


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-12)


# ---------------------------------------------------------------- A) hall2
def hall2():
    x = ler('hall2-a')
    # tira os 4 eventos medidos acima de 700 Hz (2,555 s, 4,197 s, 5,44–5,49 s e o "sopro" de 6,34–6,63 s)
    # e completa ~8 s com o começo
    y = emendar([trecho(x, 0.15, 2.50), trecho(x, 2.62, 4.15), trecho(x, 4.25, 5.40), trecho(x, 5.53, 6.28),
                 trecho(x, 6.72, 8.00), trecho(x, 0.30, 1.60)])
    y = sosfiltfilt(butter(2, 110, 'high', fs=SR, output='sos'), y)       # menos ronco (a trilha já tem grave)
    y = sosfilt(shelf_agudo(700, 12.0), y)                               # chiado do ar e zumbido audíveis no celular
    y = sosfilt(shelf_agudo(5000, -3.0), y)                              # sem ficar áspero lá em cima
    y = bordas(y, 0.02, 0.02)
    return pico(y, -6.0)


# ---------------------------------------------------------------- B) chegada2
def chegada2(lead=1.0, ate_climax=1.55, depois=0.8):
    cama = ler('chegada2-b')
    Tc = lead + ate_climax                         # clímax no arquivo (s)
    n = int((Tc + depois) * SR)
    t = np.arange(n) / SR
    # "motor subindo de tom": a cama é tocada cada vez mais rápido até o clímax (0,80x -> 1,15x) e freia depois
    r = np.where(t <= Tc, 0.72 + 0.53 * (t / Tc) ** 1.5, 1.25 - 0.50 * np.clip((t - Tc) / 0.6, 0, 1))
    pos = 0.50 * SR + np.concatenate([[0], np.cumsum(r[:-1])])
    y = np.interp(pos, np.arange(len(cama)), cama)
    y = sosfiltfilt(butter(2, 90, 'high', fs=SR, output='sos'), y)
    # envelope: aproxima (-12 dB -> 0 dB no clímax, mais forte no fim), depois para (cai 18 dB em 0,35 s e some)
    g = np.where(t <= Tc, 10 ** ((-12 + 12 * (t / Tc) ** 3) / 20),
                 10 ** ((-18 * np.clip((t - Tc) / 0.35, 0, 1)) / 20) * np.clip(1 - (t - Tc - 0.35) / 0.45, 0, 1))
    y = y * g
    # "tic" de cada andar: o tic real de chegada2-a (0,609 s), sem grave, curto
    tic = trecho(ler('chegada2-a'), 0.606, 0.686)
    tic = sosfiltfilt(butter(2, 500, 'high', fs=SR, output='sos'), tic)
    tic = sosfilt(realce(2200, 8.0), tic)                                # o tic aparece também em 1–4 kHz
    tic *= np.exp(-np.arange(len(tic)) / SR / 0.018)
    tic = bordas(tic, 0.001, 0.01)
    tic /= np.abs(tic).max()
    d, k, tempos = 0.32, 0, []
    tk = lead + 0.10
    while tk < Tc - 0.02:
        tempos.append(tk); tk += d * 0.82 ** k; k += 1
    # tics no começo (lead) também, mais espaçados e baixos
    tempos = [lead - 0.62, lead - 0.20] + tempos
    ref = np.abs(y).max()
    for tk in tempos:
        lvl = 10 ** ((-10 + 6 * np.clip((tk - lead) / ate_climax, 0, 1)) / 20) * ref * 0.9
        i = int(tk * SR); y[i:i + len(tic)] += lvl * tic[:len(y) - i]
    y = bordas(y, 0.15, 0.02)
    return pico(y, -3.0), Tc, tempos


# ---------------------------------------------------------------- C) impacto
def impacto(pre=0.10, cauda=1.0):
    x = ler('impacto-b')
    golpe = 1.0846                                  # início do ataque medido em impacto-b
    y = trecho(x, golpe - pre, golpe + cauda)
    t = np.arange(len(y)) / SR - pre
    # cauda curta: segura 0,12 s e cai 36 dB até o fim (~1 s)
    g = np.where(t < 0.12, 1.0, 10 ** ((-36 * np.clip((t - 0.12) / (cauda - 0.12), 0, 1)) / 20))
    y = bordas(y * g, 0.005, 0.05)
    return pico(y, -1.5), pre


# ---------------------------------------------------------------- D) subir
def subir(riser=0.60, pre_golpe=0.003, cauda=0.30, pula=0.019):
    sopro = trecho(ler('subir-c'), 0.55, 0.55 + riser)          # trecho que sobe de 2,0 kHz para 4,4 kHz
    sopro = sosfiltfilt(butter(2, 300, 'high', fs=SR, output='sos'), sopro)
    sopro *= 10 ** ((-18 + 18 * np.linspace(0, 1, len(sopro)) ** 1.5) / 20)  # começa baixo e cresce até o golpe
    sopro = bordas(sopro, 0.06, 0.004)
    b = ler('subir-b')
    # revisão 2026-11-09: o golpe de subir-b tem um ataque fraco em 0,5816 s e o corpo ~25 ms depois; com o estalo
    # por cima do ataque fraco, saíam dois golpes do mesmo nível com 25 ms de distância (golpe duplo). Agora o golpe
    # começa no corpo (0,5816 + 0,019 s), e o estalo cai junto com ele.
    g0 = 0.5816 + pula
    hit = trecho(b, g0 - pre_golpe, g0 + cauda)
    t = np.arange(len(hit)) / SR - pre_golpe
    hit *= np.where(t < 0.04, 1.0, 10 ** ((-40 * np.clip((t - 0.04) / (cauda - 0.04), 0, 1)) / 20))
    hit = bordas(hit, 0.001 if pula == 0 else 0.0005, 0.03)
    if pula:  # o trecho antes do golpe agora é meio do som: entra em rampa para o ataque continuar limpo
        hit[:int(pre_golpe * SR)] *= np.linspace(0, 1, int(pre_golpe * SR)) ** 2
    # estalo seco por cima do ataque: o "crack" de impacto-a (sobe em ~1 ms), só acima de 1,2 kHz
    a = ler('impacto-a')
    crack = trecho(a, 0.2045 - pre_golpe, 0.2045 + 0.06)
    crack = sosfilt(butter(4, 1200, 'high', fs=SR, output='sos'), crack)
    crack *= np.where(np.arange(len(crack)) / SR < pre_golpe, 1.0,
                      np.exp(-(np.arange(len(crack)) / SR - pre_golpe) / 0.012))
    crack = bordas(crack, 0.0005, 0.005)
    agudo = lambda s: np.sqrt(np.mean(sosfilt(butter(4, 1000, 'high', fs=SR, output='sos'), s) ** 2))
    crack *= agudo(hit[:int(0.05 * SR)]) / agudo(crack[:int(0.02 * SR)])      # mesmo nível agudo do golpe
    hit[:len(crack)] += crack
    # o sopro chega ~10 dB abaixo do golpe nos agudos e some 15 ms antes dele (o "respiro" faz o golpe bater)
    sopro *= agudo(hit[:int(0.05 * SR)]) / agudo(sopro[-int(0.1 * SR):]) * 10 ** (-10 / 20)
    corte = int(0.015 * SR)
    sopro[-corte:] = 0
    sopro[-corte - int(0.02 * SR):-corte] *= rampa(int(0.02 * SR), False)
    y = np.zeros(len(sopro) + len(hit) - int(pre_golpe * SR))
    y[:len(sopro)] += sopro
    i = len(sopro) - int(pre_golpe * SR)
    y[i:i + len(hit)] += hit
    return pico(y, -1.5), riser


if __name__ == '__main__':
    os.makedirs(SAIDA, exist_ok=True)
    salvar('hall2', hall2())
    y, tc, tempos = chegada2(); salvar('chegada2', y)
    print('chegada2: clímax no arquivo em', round(tc, 3), 's; tics em', [round(v, 3) for v in tempos])
    y, g = impacto(); salvar('impacto', y); print('impacto: golpe em', g, 's')
    y, g = subir(); salvar('subir', y); print('subir: golpe em', g, 's')
