#!/usr/bin/env python3
"""EEG_CLM/music_features.py — 음악 wav → 시간축 envelope/비트 (EEG 비교용).

윈도우별 RMS 진폭 envelope 를 뽑아 EEG 와 같은 시간 그리드로 비교 가능하게 저장.
+ envelope 자기상관으로 템포(BPM) 추정.

출력 EEG_CLM/music/music_env.txt:
    # n_win win_sec dur_s tempo_bpm
    <env 0..1>      # 윈도우별 정규화 RMS envelope (시간순)
실행: EEG_CLM/.venv/bin/python EEG_CLM/music_features.py [wav경로] [win_sec]
"""
import sys, wave, struct, math

wav_path = sys.argv[1] if len(sys.argv) > 1 else "EEG_CLM/music/track.wav"
win_sec = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
out = "EEG_CLM/music/music_env.txt"

w = wave.open(wav_path, "rb")
ch, sw, fs, n = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
raw = w.readframes(n); w.close()
dur = n / fs
print(f"[music] {wav_path}: {ch}ch {sw*8}bit {fs}Hz {dur:.1f}s ({n} frames)")

# decode to mono float (16-bit assumed; ffmpeg wav default pcm_s16le)
if sw == 2:
    fmt = "<%dh" % (len(raw) // 2)
    samp = struct.unpack(fmt, raw)
elif sw == 4:
    fmt = "<%di" % (len(raw) // 4)
    samp = struct.unpack(fmt, raw)
else:
    raise SystemExit(f"unsupported sample width {sw}")
# mono mix
if ch > 1:
    mono = [sum(samp[i:i+ch]) / ch for i in range(0, len(samp), ch)]
else:
    mono = list(samp)

# per-window RMS envelope
wlen = int(win_sec * fs)
nwin = len(mono) // wlen
env = []
for i in range(nwin):
    seg = mono[i*wlen:(i+1)*wlen]
    rms = math.sqrt(sum(x*x for x in seg) / len(seg)) if seg else 0.0
    env.append(rms)
mx = max(env) or 1.0
env = [e / mx for e in env]          # normalize [0,1]

# tempo via envelope autocorrelation (beat period in windows → BPM)
# detrend envelope
m = sum(env) / len(env)
d = [e - m for e in env]
best_lag, best_r = 0, -1e30
# beat period 0.3~1.5s → lag in windows
lo = max(1, int(0.3 / win_sec)); hi = int(1.5 / win_sec) + 1
for lag in range(lo, min(hi, len(d)//2)):
    r = sum(d[t]*d[t+lag] for t in range(len(d)-lag))
    if r > best_r:
        best_r, best_lag = r, lag
tempo = 60.0 / (best_lag * win_sec) if best_lag else 0.0

with open(out, "w") as f:
    f.write(f"# {nwin} {win_sec} {dur:.2f} {tempo:.1f}\n")
    for e in env:
        f.write(f"{e:.5f}\n")
print(f"[music] envelope {nwin} win @ {win_sec}s → {out}; tempo≈{tempo:.1f} BPM")
