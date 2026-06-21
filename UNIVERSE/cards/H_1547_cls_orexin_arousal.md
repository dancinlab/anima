# H_1547 — OREXIN/HISTAMINE × CLS: arousal-gated ENCODE↔CONSOLIDATE mode stability

🟠 **AMBER** (R1 numpy DIRECTIONAL · frozen-first · c9 · NO tune-to-green)
`wired: DIRECTIONAL-mirror → §OrexinMode engine R2 (ING h1547-r2-engine-native)`

> The **6th (final core) neurotransmitter** fused into the H_1532 two-store CLS module —
> completes "신경전달물질 모두 융합" (ACh🟢 H_1541 · DA🟢 H_1543 · NE🟢 H_1544 · 5-HT🟠
> H_1545/H_1548 · GABA🧱 H_1546 · **orexin** here). Census H_1542 Rank-7. Sakurai 2007
> (orexin loss = narcolepsy = unstable wake/sleep transitions). `a_no_llm_frame_trap`.

## Claim
Orexin-stabilized mode-gating (HYSTERESIS/dwell on arousal before flipping ENCODE↔CONSOLIDATE)
protects an IN-PROGRESS consolidation that a THRASH controller (flip on every arousal spike)
aborts. Re-framed AWAY from the encode-RATE the census found redundant, toward the
WAKE/SLEEP MODE-TRANSITION STABILITY that is orexin's biological signature.

## Result (3 seeds [11,22,33], best_alt = max(always-complete, abl), MARGIN +0.05)
| arm | seed11 | seed22 | seed33 |
|---|---|---|---|
| **OREXIN-STABLE** | 0.639 | 0.718 | 0.603 |
| THRASH (flip every spike) | 0.167 | 0.282 | 0.231 |
| FIXED-DUTYCYCLE | 0.417 | 0.338 | 0.346 |
| best-alt (always/abl) | 0.514 | 0.451 | 0.462 |
| **SHUFFLE** | 0.611 | 0.521 | **0.654** |
| orexin − best_alt | +0.125 | +0.268 | +0.141 |

## Bars
- **A PRESENCE** ✅ orexin − best_alt = +0.125/+0.268/+0.141 (all ≥ +0.05, 3/3)
- **B DISTINCT** ✅ thrash corrupts (≪ orexin) AND fixed-dutycycle misses data-driven demand
- **C EARNED (ABL)** ✅ hysteresis→0 reverts to thrash/always exactly
- **D SHUFFLE** ❌ permuted arousal does NOT cleanly collapse — seed33 shuffle 0.654 > orexin
  0.603 (the stabilization signal partially survives permutation → not decisively attributable
  to TRUE arousal-boundary timing)
- **E NO-FAB** ✅

→ A∧B∧C∧E ∧ ¬D = **🟠 AMBER**. Orexin's mode-stabilization is PRESENT and beats every
alternative (hysteresis genuinely protects in-progress consolidation), but the shuffle control
does not decisively isolate it to the true arousal boundaries — a fixed-dwell hysteresis on a
permuted arousal stream captures much of the gain. **The fusion law:** orexin adds partial
stabilization but the load-bearing lever is the dwell/hysteresis WIDTH (a schedule knob), not
the arousal SIGNAL — closer to 5-HT-timing 🟠 (re-tune) than to NE-flush 🟢 (state-clear).

## Honesty (c9)
Frozen-first, bars pre-registered in `state/verdicts/1547_cls_orexin_arousal/H_1547_FREEZE.txt`,
NO bar moved, NO tune-to-green. The shuffle failure is reported as the honest discriminator.
DIRECTIONAL (numpy hard-gate-1) → engine §OrexinMode R2 = ING.
