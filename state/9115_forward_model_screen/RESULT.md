# H_9115 — Screen-B forward-model headroom ($0) — RESULT

**VERDICT: 🟢 HEADROOM-EXISTS — compressed b50=2.20 < raw b50=3.50 at held accuracy (comp_full=1.00 vs raw 1.00) → forward-model lever PHYSICALLY POSSIBLE → engine-native mini justified**

- b50_raw=3.5 · b50_compressed=2.2 · accuracy-hold(full)=1.000 vs 1.000 (HELD)
- mean bytes raw=102.5 · compressed=71.2 (compression 31%)
- receiver=claude-fable-5 (single, $0 DIRECTIONAL screen) · emit FROZEN (H_9111) · tier=DIRECTIONAL

## raw arm (acc vs clue bytes)
  t=full: acc=1.000
  t=8: acc=0.857
  t=6: acc=0.929
  t=4: acc=0.786
  t=3: acc=0.214
  t=2: acc=0.071
## compressed arm
  t=full: acc=1.000
  t=8: acc=1.000
  t=6: acc=1.000
  t=4: acc=0.857
  t=3: acc=0.786
  t=2: acc=0.429

Gate: 🟢 HEADROOM → engine-native mini (lane15 side-loop) justified. 🔴 INERT → forward-model DPI-walled, GPU stop.
