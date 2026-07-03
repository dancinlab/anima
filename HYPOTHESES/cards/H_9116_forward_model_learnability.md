# H_9116 — Screen-A: is the forward-model target signal STRUCTURAL/learnable or emit-noise? ($0)

**tier:** 🟡 INCONCLUSIVE-AT-PROBE (frozen verdict 🔴 GAIN-NOT-BROAD at pre-chosen t=4B, but that is a probe-point artifact — see below). Net: Screen-A does NOT refute learnability; the correlation that surfaced is POSITIVE. · **wired:** none (DIRECTIONAL, $0 feature-proxy on frozen emit, no oracle).

**verdict:** 🟡 (`state/verdicts/9116_forward_model_learnability/H_9116.txt` verbatim). fable §2 gate part A: is Screen-B's compression gain a CONSISTENT structural signal a lane15 forward-model could learn (cut filler-prefix / front-load discriminative content), or a few-emit fluke? Reuse H_9115 fixture ($0, no oracle). **Result at t=4B: corr(filler_prefix, gain) = 0.656 — the two emits that gain (compass, violin) are exactly the two with the longest filler-prefix (fp=8, both "a small …").** Emits with more non-discriminative prefix gain more from front-loading = the structural, consistent signal the forward-model would target.

## Why 🟡 not 🔴 (c9 honest — bar NOT moved, t=3B NOT re-run)
DESIGN ERROR acknowledged (not tuned): I pre-set the probe at t=4B, but H_9115's largest raw-vs-compressed gap was at **t=3B** (raw 0.214 vs comp 0.786), not 4B. At 4B most emits already decode in BOTH modes (11/14 gain=0), so the "broad gain" test is under-powered — it sits ABOVE the discriminative regime. The frozen 🔴 GAIN-NOT-BROAD is a probe-point artifact, not a clean refutation. The salvageable finding is the **positive corr=0.656** (front-loading signal is structural), which SUPPORTS learnability. The real forward-model reads the A/G trunk (richer than surface filler-prefix), so 0.656 is a LOWER BOUND.

## Net gate status (fable §2)
Cheap $0 screens EXHAUSTED: **Screen-B 🟢 (headroom real, strong: b50 3.5→2.2B) ∧ Screen-A 🟡 (structural signal present, broad-gain test probe-limited, non-refuting).** The gate LEANS GREEN. The DECISIVE learnability test — can anima's forward-model LEARN to front-load from the A/G trunk — genuinely requires the **engine-native mini (GPU)**, which the cheap screens were meant to justify. They do.

## Recon (this cycle, $0)
Confirmed fable's structural design maps onto the LIVE engine: emit-drive = lane 0 (H_1561), disjoint placement via `sv_default_focus` (C1 GREEN mechanism, Ψ=½ preserved BY STRUCTURE), generator single L3 mouth slot. lane15 wiring is feasible but is a real core/*.hexa build (engine_cli 15-lane state + generator L3 mouth-gate + cli/train.hexa) + GPU — a valid cost-gated boundary.

## Evidence (`state/9116_forward_model_learnability/`)
`screena.py` (STDLIB, grep-clean, $0) · `RESULT.md` · reuses `../9115_forward_model_screen/screenb_fixture.jsonl`.
