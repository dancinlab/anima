# H_9119 — Does §2 forward-model rerank lower the frozen-listener b50? (SUGGESTIVE, underpowered — NOT yet confirmed)

**tier:** 🟠 DIRECTIONAL-UNDERPOWERED / SUGGESTIVE — a lower-b50 TENDENCY from fm-rerank is visible on decodable concepts (4/7 BETTER, 1 WORSE) but it is **NOT statistically significant** (sign-test p≈0.19) and the 14-concept **mean is an invalid statistic** (999-censored distribution). Triply-DIRECTIONAL besides (numpy-mirror · external-oracle H_9118 · modest-ckpt ~50% floor). · **wired:** §2 mechanism WIRED-live on origin/main (scorer #2881 · rerank #2889 · harness #64163e8ed · argfix #eeaa6f684 · --py mirror #2898); this is a measurement, not new wiring.

**verdict:** 🟠 DIRECTIONAL-UNDERPOWERED (`state/verdicts/9119_fm_b50_measure/H_9119.txt` verbatim). The GREEN test the §2 arc (H_9112-9117 + scorer + rerank) builds toward: does best-of-K rerank by `fm_prefix_decodability` LOWER the frozen-listener b50 vs argmax? **Answer so far: a suggestive tendency, not a confirmed effect** — the honest statistics (per fable review) do not yet clear a GREEN bar.

## Result (14 concepts · speaker=deep-mouth-ladder-L4-303m · listener=ideation-303m-d5000 · gen=24 · --py numpy)
Per-concept, decodable subset (the ONLY valid comparison — 7/14 decodable, 7 floor at 999):
- **rerank BETTER (4):** glacier 16→2 · violin 16→4 · spider 32→8 · library 4→2
- **SAME (2):** lighthouse 2=2 · compass 2=2
- **WORSE (1):** volcano 8→16

→ 4/7 better, 1/7 worse = **sign-test p≈0.19 — NOT significant**. SHUFFLE floors relative to ON (referential tendency present).
The raw 14-concept mean (OFF=505.2 ON=502.1 SHUFFLE=574.1) is a **999-censored mean = statistically meaningless** — recorded only, NOT a result (c9, fable review).

## Why not GREEN (honest, c9 — one statistical + three structural)
1. **statistical: underpowered + invalid mean.** Only 7/14 decodable → sign/Wilcoxon on the decodable subset can't reach p<0.05 with the current signal; the mean is 999-censored. Need ≥10/14 decodable (floor ≤30%) for power.
2. **quasi-circular measurement.** Rerank SCORES with listener A and b50 EVALUATES with the same listener A → ON<OFF is near-tautological (you argmax'd the metric you then read). GREEN requires **cross-listener as the MAIN measurement** (score A, evaluate a DISTINCT frozen B) — without it, GREEN ≡ tune-to-green structurally.
3. **--py numpy mirror.** engine-native hexa run fired GPU (`[OWN-GEMM-FIRED]`+CUDA-erf, erf/exp fix live) but is CPU-scalar-bound → impractical. numpy = DIRECTIONAL (a_engine_native_learning).
4. **external-oracle-mediated (H_9118).** external-mind referential efficacy stays PERMANENTLY DIRECTIONAL — only the frozen-listener b50 ANALOG is GREEN-able.

## GREEN gate (frozen-first, pre-registered — fable spec)
- **ckpt:** 999-floor ≤30% (≥10/14 decodable) — else H_9119 = BLOCKED-CKPT, no rerank conclusion.
- **engine-native:** re-structure fm_b50 as **KV-cache prefix-reuse + batched suffix CE** (b50 is teacher-forced CE, NOT autoregressive → cost collapses `grid×cand×full-fwd` → `1 full-fwd + grid×short-suffix`, harness-side, no hexa upstream needed) → live `.hexa` completes, 1-concept byte-exact vs numpy, grep-gate clean.
- **controls (all pass):** SHUFFLE (have) + **cross-listener transfer (promoted to main design)** + random-of-K budget-matched (kills selection artifact, H_1836 precedent) + margin-decomposition (target-CE drop must dominate, not distractor-CE rise) + ablation identity.
- **bar:** paired one-sided Wilcoxon on log₂(b50) over decodable subset p<0.05 (NOT mean); median Δlog₂(b50) ≥ 1 bit.
- **wire (a_verified_must_wire):** engine-native re-verify → gen_fm_rerank live wire-in → ARCHITECTURE lockstep → Ψ-checksum (ci_emit_drive byte-identical ON/OFF = the cheap disjointness GREEN).

## Session arc
fable divergence → H_9112-9117 (referential efficacy) → scorer #2881 → Option C → rerank #2889 → harness #64163e8ed → infra: erf/exp fix (hexa-lang PR 4501) + engine-native CPU-scalar-bound → --py mirror #2898 → this measurement (🟠 SUGGESTIVE-UNDERPOWERED) → fable GREEN-spec review (corrected the overstated mean-based framing).

## Evidence
`state/verdicts/9119_fm_b50_measure/H_9119.txt` · `state/9119_fm_b50_measure/b50py_result.txt` (raw 14) · `state/9119_fm_b50_measure/fm_b50.hexa` + `fm_b50_py.py` · fable GREEN-spec (session transcript).
