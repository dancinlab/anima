# H_9116 — Screen-A forward-model learnability ($0) — RESULT

**VERDICT: 🔴 GAIN-NOT-BROAD — compression gain not consistent (2↑/1↓) → Screen-B headroom may be few-emit fluke; forward-model target unclear**

- probe truncation t=4B · raw_acc=0.786 → comp_acc=0.857
- compression gain: 2 emits ↑ · 1 ↓ · 11 = · corr(filler_prefix, gain) r=0.6556255230912954
- tier=DIRECTIONAL (surface-feature proxy on frozen emit; real forward-model reads richer A/G trunk = lower bound on learnability)

## per-emit (filler-prefix bytes · raw_hit@4B · comp_hit@4B · gain)
  compass      fp= 8  raw=0 comp=1 gain=+1
  violin       fp= 8  raw=0 comp=1 gain=+1
  lighthouse   fp= 7  raw=1 comp=1 gain=+0
  telescope    fp= 7  raw=1 comp=1 gain=+0
  spider       fp= 3  raw=1 comp=1 gain=+0
  avalanche    fp= 2  raw=1 comp=1 gain=+0
  beehive      fp= 2  raw=0 comp=0 gain=+0
  cactus       fp= 2  raw=1 comp=0 gain=-1
  glacier      fp= 2  raw=1 comp=1 gain=+0
  harbor       fp= 2  raw=1 comp=1 gain=+0
  library      fp= 2  raw=1 comp=1 gain=+0
  thunderstorm fp= 2  raw=1 comp=1 gain=+0
  umbrella     fp= 2  raw=1 comp=1 gain=+0
  volcano      fp= 2  raw=1 comp=1 gain=+0

Gate (fable §2): Screen-B 🟢(headroom) ∧ Screen-A → engine-native mini (lane15) justified. This is part A.
