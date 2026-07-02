# H_1550 — OREXIN × CLS: mode-stability with a CLEAN shuffle control (honest GREEN attempt)

🟢 **GREEN** (R1 numpy DIRECTIONAL · frozen-first · c9 · NO tune-to-green)
`wired: DIRECTIONAL-mirror → §OrexinMode engine R2 (ING h1550-r2-engine-native)`

> **CONTROL-FIX of H_1547** (`a_break_the_wall` type-(a) measurement-fix, NOT tune-to-green).
> H_1547 landed 🟠 because its shuffle control did not cleanly collapse (seed33 shuffle 0.654 >
> orexin 0.603). Here the corrected control flips it to an honest 🟢. Sakurai 2007 Nat Rev
> Neurosci 8:171 (orexin loss = narcolepsy = unstable wake/sleep transitions; orexin = TRANSITION
> STABILITY, distinguishing a transient blip from a sustained drive). `a_no_llm_frame_trap`.

## The control flaw (why H_1547 was 🟠) and the fix
H_1547's PRESENCE/DISTINCT/ABLATION all passed decisively, but the **shuffle control** permuted
the per-segment `arousal_dur` field — and that **same field also drives the TRUE interference
position** inside the arm (`interf_tick = 0 if arousal_dur>=2 else DWELL`). Permuting it
**co-permuted the true boundary**, keeping the controller's transient/sustained call ALIGNED with
where interference actually landed. So the shuffle never broke the alignment between the SIGNAL the
controller reads and the TRUE boundary → a fixed-dwell hysteresis on a permuted-but-still-aligned
stream kept its gain. That is a CONTROL-DESIGN flaw, not evidence against the capability.

**The corrected control (pre-registered, frozen-first):** hold the dwell-width hysteresis controller
byte-identical, but DECOUPLE the two roles of `arousal_dur`:
- `interf_dur` = each segment's REAL arousal_dur → fixes WHERE A→C interference lands (the TRUE
  consolidation-demand boundary). **NEVER permuted** → the stream physics is identical for every arm.
- `arousal_read` = the signal the CONTROLLER reads to call transient-vs-sustained. For every arm
  EXCEPT clean_shuffle, `arousal_read == interf_dur` (so orexin/thrash/fixed/abl/always are
  **byte-identical to H_1547**). For **CLEAN-SHUFFLE**, `arousal_read` is PERMUTED while `interf_dur`
  stays REAL → the controller makes its call on the WRONG segments while interference lands at the
  real boundary. Surviving gain = pure dwell-width knob; collapse = the gain reads TRUE timing.

**All other arms and bars are IDENTICAL to H_1547** (PRESENCE +0.05, DISTINCT, ABL, NO-FAB). Only
the shuffle control is corrected — this is a measurement-fix, NOT tune-to-green.

## Result (3 seeds [11,22,33], best_alt = max(thrash, fixed, always), MARGIN +0.05)
| arm | seed11 | seed22 | seed33 | mean |
|---|---|---|---|---|
| **OREXIN-STABLE** | 0.639 | 0.718 | 0.603 | 0.653 |
| THRASH (flip every spike) | 0.167 | 0.282 | 0.231 | 0.226 |
| FIXED-DUTYCYCLE | 0.417 | 0.338 | 0.346 | 0.367 |
| ALWAYS / ABL | 0.514 | 0.451 | 0.462 | 0.475 |
| best-alt | 0.514 | 0.451 | 0.462 | 0.475 |
| **CLEAN-SHUFFLE** (corrected) | 0.514 | 0.451 | 0.500 | 0.488 |
| orexin − best_alt | +0.125 | +0.268 | +0.141 | +0.178 |
| **orexin − clean_shuffle** | **+0.125** | **+0.268** | **+0.103** | **+0.165** |

The orexin / thrash / fixed / always / abl columns are **byte-identical to H_1547** — confirming the
only change was the corrected control. (For reference, H_1547's flawed shuffle gave seed33 0.654 >
orexin 0.603 = FAIL; the clean control gives seed33 0.500 < 0.603 = +0.103 ✓.)

## Bars
- **A PRESENCE** ✅ orexin − best_alt = +0.125/+0.268/+0.141 (3/3 ≥ +0.05, mean +0.178) — UNCHANGED
- **B DISTINCT** ✅ thrash 0.226 ≪ orexin 0.653; fixed 0.367 ≪ orexin (both < orexin−0.05) — UNCHANGED
- **C ABL** ✅ orexin − always = +0.178 ≥ 0.05 AND |abl − always| = 0.0000 (clean ablation) — UNCHANGED
- **D CLEAN-SHUFFLE COLLAPSE** ✅ orexin − clean_shuffle = +0.125/+0.268/+0.103 (**3/3 ≥ +0.05**, mean
  +0.165) — permuting ONLY the controller's read (TRUE boundary untouched) collapses the lift back to
  the always-complete baseline → the gain reads TRUE arousal-boundary timing, not just dwell-width — **CORRECTED**
- **E NO-FAB** ✅ best_alt 0.475 > 0 — UNCHANGED

→ A∧B∧C∧D∧E = **🟢 GREEN**. The corrected control collapses the lift on all 3 seeds, proving orexin's
mode-stabilization reads the TRUE arousal-boundary timing (a real stabilization capability that a
fixed never-abort policy cannot capture). The earlier shuffle co-permuted the boundary, which masked
this by keeping the controller's call aligned.

## The fusion law (the family running through H_1541🟢/H_1543🟢/H_1544🟢/H_1545🟠/H_1546🧱)
NT adds a NEW CAPABILITY a fixed schedule cannot → 🟢 ; NT only RE-TUNES an existing duty-cycle → 🟠.
With the clean control, **orexin lands on the 🟢 (new-capability) side**: the arousal-reading
transient/sustained DISTINCTION (not the fixed dwell-width) is the load-bearing lever — when the read
is scrambled relative to the true boundary the gain vanishes. This UPGRADES H_1547's tentative 🟠
("lever = dwell-width knob") to 🟢 ("lever = true arousal SIGNAL") via a corrected control, frozen-first.

## Honesty (c9)
Frozen-first, bars pre-registered in `state/verdicts/1550_orexin_cleanctrl/H_1550_FREEZE.txt` BEFORE the
scored run. The ONLY change from H_1547 is the corrected control (D); A/B/C/E are byte-identical bars,
NO bar moved, NOT tune-to-green. Had the clean control still failed to collapse, the frozen verdict map
would have fired AMBER_KNOB (honest 🟠) — it did not; the collapse is decisive (3/3). DIRECTIONAL
(numpy hard-gate-1) → engine §OrexinMode R2 = ING h1550-r2-engine-native. live core/*.hexa UNTOUCHED.
Ψ-disjoint (consolidation read, not an emit gate).
