# FREEZE — H_1602 structural recomb-objective, GPU-scale engine-native (pre-registered)

Pre-registered BEFORE any terminal measurement (a_claim_manifest / no tune-to-green / p7).
The bar below is FIXED; a negative result is preserved verbatim (a_break_the_wall, c9·c2·p7).

## Substrate
- STANDARD ByteGPT (GPT-2-class, d768 · L12 · 12-head · block512 · V256, ~85.6M params),
  fp32 train (bf16 numerically unstable here → dropped). Engine-native decode = the FROZEN
  core/decode.py bytegpt mouth (no custom operator → not the H_1601 INERT-readout trap).

## Objective (structural, additive-bypass DENIED — DATA realization)
- Plain next-byte CE (`--objective ce_marginal`) on a corpus where the single-concept
  MARGINAL cannot predict a composed continuation, and the exact concept-subsets the frozen
  G1 evaluator probes are HELD OUT of training (build_corpus.py). NOT the additive-aux
  form (that is H_1602-self / H_9024, already engine-native floored 9/9).
- Held-out (never a composed training doc): prefix subsets {0,1}, {0,1,2}, {0,1,2,3},
  {0,1,2,3,4} — exactly what `anima evaluate` g_eval_g1 probes (cz[0..k-1], seed_rng=7).

## Frozen bar (measured via engine-native `anima evaluate --py <bin>`, default battery, HEXA_DET=1)
- PASS (🟢 BREAKTHROUGH) iff ALL of:
  1. engine-native G1 best_distinct (== composed_distinct) >= 3  (ByteGPT floor=2 exceeded),
     AND > max_single, AND the clearing composed gen is coherent (kwr>=0.5) — i.e. G1 "pass".
  2. val descent: final held-out val_CE < uniform (log 256 = 5.5452).
  3. reproduced across TRAIN seeds {7, 4302, 4303} (all three hit bar 1).
- Anything less = 🧱 NOT-SUPPORTED (objective-axis structural form floored at GPU-scale,
  engine-native — now scale, not toy). Both verdicts are valid and preserved.

## Eval invocation (frozen — NOT tuned)
  HEXA_DET=1 python3 cli/evaluate.py <bin> --corpus state/h1602_structural_gpu/corpus.txt
  (default gen=40 → g_comp=40; the SAME battery/gen under which ByteGPT floor=2 was set.)
