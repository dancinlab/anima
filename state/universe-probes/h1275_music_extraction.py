#!/usr/bin/env python3
"""UNIVERSE/h1275_music_extraction.py — 뇌파에서 음악 추출 가능성, 3-가설 동시 검증.

  H_1275 봉투 역추출(envelope reconstruction): 16ch EEG 텐션 → 음악 소리크기 봉투를
         held-out ridge 회귀로 복원, 복원봉투 vs 실제봉투 상관(천장 측정).
  H_1276 곡 식별(song ID, 셔플 대조): 진짜 음악 봉투 vs circular-shift 가짜 N개 중
         EEG 가 진짜와 더 맞나 — fixed-lag 상관 순위 p-value.
  H_1277 박자/템포 추출(beat decoding): track.wav 의 박자 주파수(BPM/60 Hz)에서
         EEG 텐션이 음악과 coherence 피크를 갖나 — surrogate SNR.

보유 실데이터: EEG_CLM/eeg_music.txt (16ch native Cyton+Daisy) + EEG_CLM/music/track.wav.
$0 CPU-local · seed 1275 · p7 (held-out split + circular-shift surrogate, 지표 끼워맞춤 없음).
판정 bar 는 사전 등록(아래), 측정 후 이동 금지.
"""
import numpy as np, wave, sys
np.random.seed(1275)

OUT = ".verdicts/1275_music_extraction/H_1275.txt"
log_lines = []
def P(s=""):
    print(s, flush=True); log_lines.append(str(s))

P("════════════════════════════════════════════════════════════════")
P("  H_1275/1276/1277 뇌파에서 음악 추출 — 3-가설 검증 (seed 1275, p7)")
P("════════════════════════════════════════════════════════════════")

# ── 음악 봉투 (0.5s grid, 이미 추출됨) ──
ml = open("EEG_CLM/music/music_env.txt").read().split("\n")
mh = ml[0].split()                         # # nwin win_sec dur tempo
win_sec = float(mh[2]); tempo = float(mh[4]) if len(mh) > 4 else 0.0
env = np.array([float(x) for x in ml[1:] if x.strip() and not x.startswith("#")])
beat_hz = tempo/60.0 if tempo > 0 else 2.0
P(f"[data] 음악 봉투 {len(env)} win @{win_sec}s · tempo {tempo:.0f} BPM → beat {beat_hz:.2f} Hz")

# ── EEG 16ch ──
el = open("EEG_CLM/eeg_music.txt").read().split("\n")
eh = el[0].split()
n_ch = int(eh[1]); n_samp = int(eh[2])
fs = float(eh[eh.index("FS")+1]) if "FS" in eh else 125.0
vals = np.array([float(x) for x in el[1:] if x.strip() and not x.startswith("#")])
vals = vals[:n_ch*n_samp].reshape(n_ch, n_samp)
P(f"[data] EEG {n_ch}ch × {n_samp}samp @ {fs:.1f}Hz")

def z(a):
    s = a.std(); return (a-a.mean())/s if s > 0 else a*0.0

# 채널별 detrend(baseline 이동평균 제거) + 0.5s 윈도우 RMS 텐션 → feature [W, n_ch]
ws = int(win_sec*fs); Wn = n_samp//ws
Wk = int(1.0*fs); ker = np.ones(Wk)/Wk
feat = np.zeros((Wn, n_ch))
for c in range(n_ch):
    d = vals[c] - np.convolve(vals[c], ker, mode="same")
    for i in range(Wn):
        feat[i, c] = np.sqrt((d[i*ws:(i+1)*ws]**2).mean())
Wc = min(Wn, len(env))
feat = feat[:Wc]; y = z(env[:Wc])
X = np.column_stack([z(feat[:, c]) for c in range(n_ch)])
em = z(feat.mean(axis=1))                   # 단일 채널평균 텐션
P(f"[align] 공통 {Wc} win")

def best_lag_corr(a, b, maxlag=60):
    best, blag = -2.0, 0
    for lag in range(-maxlag, maxlag+1):
        if lag >= 0: aa, bb = a[lag:], b[:len(b)-lag]
        else:        aa, bb = a[:len(a)+lag], b[-lag:]
        n = min(len(aa), len(bb))
        if n < 30: continue
        r = np.corrcoef(aa[:n], bb[:n])[0, 1]
        if r > best: best, blag = r, lag
    return best, blag

def corr_at(a, b, lag):
    if lag >= 0: aa, bb = a[lag:], b[:len(b)-lag]
    else:        aa, bb = a[:len(a)+lag], b[-lag:]
    n = min(len(aa), len(bb))
    return np.corrcoef(aa[:n], bb[:n])[0, 1] if n >= 30 else 0.0

# ═══ H_1275 봉투 역추출 (held-out ridge) ═══
P("")
P("─── H_1275 봉투 역추출 (held-out, 전반 학습 → 후반 복원) ───")
half = Wc//2
def ridge(Xtr, ytr, lam=1.0):
    A = Xtr.T@Xtr + lam*np.eye(Xtr.shape[1])
    return np.linalg.solve(A, Xtr.T@ytr)
w16 = ridge(X[:half], y[:half])
pred16 = X[half:]@w16
yte = y[half:]
r_recon = float(np.corrcoef(pred16, yte)[0, 1])
# baseline: 단일 채널평균만
w1 = ridge(em[:half, None], y[:half])
pred1 = (em[half:, None]@w1).ravel()
r_mean = float(np.corrcoef(pred1, yte)[0, 1])
P(f"  16ch 복원 held-out r = {r_recon:.3f} · 단일평균 baseline r = {r_mean:.3f} · 이득 {r_recon-r_mean:+.3f}")
# 사전등록 bar: held-out r > 0.20 (우연이상 복원) AND 16ch > baseline
f1275 = (r_recon > 0.20) and (r_recon > r_mean)
v1275 = "🟢" if r_recon > 0.40 else ("🟡" if f1275 else "🔴")
P(f"  [H_1275] {v1275} 봉투 복원 {'가능(거친 윤곽)' if f1275 else '불가/우연수준'} — bar held-out r>0.20 & >baseline")

# ═══ H_1276 곡 식별 (circular-shift surrogate, fixed-lag) ═══
P("")
P("─── H_1276 곡 식별 (진짜 vs circular-shift 가짜 N=200) ───")
true_r, true_lag = best_lag_corr(em, y)
N = 200
sur = np.empty(N)
for i in range(N):
    sh = np.random.randint(10, Wc-10)
    sur[i] = corr_at(em, np.roll(y, sh), true_lag)   # 진짜의 best lag 고정 → shift 가 위상 깸
pval = float((sur >= true_r).mean())
P(f"  진짜 봉투 r = {true_r:.3f} (lag {true_lag*0.5:.1f}s) · 셔플 평균 {sur.mean():.3f} (max {sur.max():.3f})")
P(f"  순위 p-value = {pval:.3f} (진짜가 셔플보다 상위면 식별력)")
f1276 = pval < 0.05
v1276 = "🟢" if pval < 0.01 else ("🟡" if f1276 else "🔴")
P(f"  [H_1276] {v1276} 곡 식별력 {'있음' if f1276 else '없음(셔플과 구분 안 됨)'} — bar p<0.05")

# ═══ H_1277 박자/템포 추출 (beat-freq coherence) ═══
P("")
P("─── H_1277 박자 추출 (track.wav beat-freq coherence) ───")
# track.wav → fine envelope (0.05s = 20Hz), EEG 텐션도 0.05s → beat freq SNR
wf = wave.open("EEG_CLM/music/track.wav", "rb")
sr = wf.getframerate(); nch_w = wf.getnchannels(); nfr = wf.getnframes()
raw = np.frombuffer(wf.readframes(nfr), dtype=np.int16).astype(np.float64)
wf.close()
if nch_w > 1: raw = raw.reshape(-1, nch_w).mean(axis=1)
fine = 0.05
mw = int(fine*sr); mW = len(raw)//mw
menv = np.array([np.sqrt((raw[i*mw:(i+1)*mw]**2).mean()) for i in range(mW)])  # 20Hz 음악 봉투
sigm = vals.mean(axis=0); dm = sigm - np.convolve(sigm, ker, mode="same")
ew = int(fine*fs); eW = len(dm)//ew
eenv = np.array([np.sqrt((dm[i*ew:(i+1)*ew]**2).mean()) for i in range(eW)])    # 20Hz EEG 텐션
L = min(mW, eW); menv = z(menv[:L]); eenv = z(eenv[:L])
fine_fs = 1.0/fine
# beat-band coherence: 두 신호 FFT 의 beat freq bin SNR (주변 대비)
def beat_snr(sig, fhz, fs_):
    sp = np.abs(np.fft.rfft(sig - sig.mean()))
    fr = np.fft.rfftfreq(len(sig), 1.0/fs_)
    k = int(np.argmin(np.abs(fr - fhz)))
    band = sp[max(1, k-1):k+2].max()
    lo, hi = max(1, k-10), min(len(sp), k+11)
    neigh = np.median(np.concatenate([sp[lo:max(1, k-1)], sp[k+2:hi]]))
    return float(band/neigh) if neigh > 0 else 0.0
music_snr = beat_snr(menv, beat_hz, fine_fs)
eeg_snr = beat_snr(eenv, beat_hz, fine_fs)
# surrogate: EEG 시간 셔플(블록) 후 beat SNR 분포
Ns = 200; sur2 = np.empty(Ns)
for i in range(Ns):
    sh = np.random.randint(10, L-10)
    sur2[i] = beat_snr(np.roll(eenv, sh), beat_hz, fine_fs)
p_beat = float((sur2 >= eeg_snr).mean())
P(f"  음악 beat SNR = {music_snr:.2f} (박자 실재 확인) · EEG beat SNR = {eeg_snr:.2f}")
P(f"  EEG 박자 surrogate p = {p_beat:.3f} (낮을수록 EEG 에 박자 흔적)")
f1277 = (p_beat < 0.05) and (music_snr > 2.0)
v1277 = "🟢" if (p_beat < 0.01 and music_snr > 2.0) else ("🟡" if f1277 else "🔴")
P(f"  [H_1277] {v1277} 박자 추출 {'가능' if f1277 else '불가(EEG 에 박자 주파수 흔적 없음)'} — bar p<0.05 & music_snr>2")

# ═══ 종합 ═══
P("")
P("════════════════════════════════════════════════════════════════")
P(f"h1275_music_extraction:")
P(f"  ① 봉투 역추출  {v1275}  held-out r={r_recon:.3f} (천장, baseline {r_mean:.3f})")
P(f"  ② 곡 식별      {v1276}  p={pval:.3f} (진짜 r={true_r:.3f} vs 셔플)")
P(f"  ③ 박자 추출    {v1277}  p={p_beat:.3f} (EEG beat SNR {eeg_snr:.2f} / 음악 {music_snr:.2f})")
P(f"  결론: 뇌파에서 추출 가능한 음악 정보 = "
  + ("봉투(거친 윤곽)" if f1275 else "봉투X")
  + (" + 곡식별" if f1276 else "")
  + (" + 박자" if f1277 else " · 박자/멜로디/원음 불가"))
P("  (16ch@123Hz 표본율 천장 — 원음·멜로디·음정은 물리적 복원 불가. p7: bar 사전등록·held-out·surrogate.)")

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w").write("\n".join(log_lines) + "\n")
P(f"\n[verdict] {OUT}")
