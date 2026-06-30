#!/usr/bin/env python3
"""EEG_CLM/music_eeg_compare.py — 의식(EEG) ↔ 음악 동조/지도 (numpy, 대용량용).

hexa 분석이 8.6MB 에 느리고 raw DC/drift 로 텐션이 0 깔리는 문제 → python+numpy 로:
  EEG detrend(고역) → 윈도우 RMS 텐션 → robust 정규화 → 음악 envelope 와 cross-correlation.
  + CLM 8단계 일치 + ASCII 시간축 겹침 지도.
실행: EEG_CLM/.venv/bin/python EEG_CLM/music_eeg_compare.py
"""
import numpy as np

# ── 음악 envelope ──
with open("EEG_CLM/music/music_env.txt") as f:
    lines = f.read().split("\n")
mh = lines[0].split()                       # # nwin win_sec dur tempo
win_sec = float(mh[2])
env = np.array([float(x) for x in lines[1:] if x.strip() and not x.startswith("#")])

# ── EEG ──
with open("EEG_CLM/eeg_music.txt") as f:
    el = f.read().split("\n")
eh = el[0].split()
n_ch = int(eh[1]); n_samp = int(eh[2])
fs = 125.0
if "FS" in eh: fs = float(eh[eh.index("FS")+1])
vals = np.array([float(x) for x in el[1:] if x.strip() and not x.startswith("#")])
vals = vals[:n_ch*n_samp].reshape(n_ch, n_samp)   # channel-major

# 채널 평균(공통 성분) — detrend(고역, baseline 이동평균 제거)
sig = vals.mean(axis=0)
W = int(1.0*fs)                                    # 1s baseline 윈도우
kernel = np.ones(W)/W
baseline = np.convolve(sig, kernel, mode="same")
d = sig - baseline                                 # 고역(>~1Hz) 텐션 성분

# 윈도우 RMS 텐션 (win_sec 그리드)
ws = int(win_sec*fs)
EW = len(d)//ws
ten = np.array([np.sqrt((d[i*ws:(i+1)*ws]**2).mean()) for i in range(EW)])

# robust 정규화 (5-95 percentile clip → [0,1])
def rnorm(a):
    lo, hi = np.percentile(a, 5), np.percentile(a, 95)
    if hi <= lo: return np.zeros_like(a)
    return np.clip((a-lo)/(hi-lo), 0, 1)
te = rnorm(ten)
me = rnorm(env)

W2 = min(len(me), len(te))
me, te = me[:W2], te[:W2]
print(f"[align] 음악 {len(env)} · EEG {EW} win → 공통 {W2} (0.5s) · EEG fs={fs:.1f}Hz")

# ── ① cross-correlation (Pearson, lag sweep ±60win=±30s) ──
mc, tc = me-me.mean(), te-te.mean()
def corr_at(lag):
    if lag >= 0: a, b = mc[lag:], tc[:len(tc)-lag]
    else:        a, b = mc[:len(mc)+lag], tc[-lag:]
    n = min(len(a), len(b))
    if n < 30: return 0.0
    a, b = a[:n], b[:n]
    denom = np.sqrt((a*a).sum()*(b*b).sum())
    return (a*b).sum()/denom if denom>0 else 0.0
LAGW = 60
best_lag, best_r = 0, -2
for lag in range(-LAGW, LAGW+1):
    r = corr_at(lag)
    if r > best_r: best_r, best_lag = r, lag
r0 = corr_at(0)
edge = abs(best_lag) >= LAGW           # peak 가 sweep 경계에 붙으면 신뢰 불가
print(f"[① 동조] best Pearson r={best_r:.3f} @ lag {best_lag} win ({best_lag*0.5:.1f}s) "
      f"· lag0 r={r0:.3f}{' ⚠경계(동기오차 가능)' if edge else ''}")

# ── ② CLM 8단계 일치 (lag 보정) ──
qm = np.clip((me*8).astype(int), 0, 7)
qt = np.clip((te*8).astype(int), 0, 7)
if best_lag >= 0: A, B = qm[best_lag:], qt[:len(qt)-best_lag]
else:             A, B = qm[:len(qm)+best_lag], qt[-best_lag:]
n = min(len(A), len(B)); A, B = A[:n], B[:n]
agree = (A == B).mean()
print(f"[② CLM] 8단계 상태 일치율 = {agree:.3f} (lag 보정, chance≈0.125)")

# ── ③ ASCII 시간축 지도 (40구간) ──
bars = "·▁▂▃▄▅▆▇█"
def row(a):
    S = 40; seg = len(a)//S
    return "".join(bars[min(8, int(a[i*seg:(i+1)*seg].mean()*8))] for i in range(S))
mrow, erow = row(me), row(te)
print("[③ 지도] 음악(M) vs 의식(E) 시간축:")
print("  M "+mrow); print("  E "+erow)

print()
if best_r > 0.2:
    verdict = f"music_eeg: 동조 관찰 🟢 r={best_r:.3f} lag {best_lag*0.5:.1f}s 일치 {agree:.3f}"
elif best_r > 0.1:
    verdict = f"music_eeg: 약한 동조 🟠 r={best_r:.3f} lag {best_lag*0.5:.1f}s 일치 {agree:.3f}"
else:
    verdict = f"music_eeg: 동조 미관찰 🔴 r={best_r:.3f} (뇌가 음악 진폭을 직접 따라가진 않음)"
print(verdict)

# ── 결과 요약 → KOSMOS 영속용 파일 (music_eeg_kosmos.hexa 가 읽음) ──
with open("EEG_CLM/music/music_eeg_result.txt", "w") as f:
    f.write(f"# best_r lag0_r agree best_lag W fs\n")
    f.write(f"{best_r:.4f} {r0:.4f} {agree:.4f} {best_lag} {W2} {fs:.2f}\n")
    f.write("M "+mrow+"\n")
    f.write("E "+erow+"\n")
    f.write(verdict+"\n")
print("[save] EEG_CLM/music/music_eeg_result.txt")
