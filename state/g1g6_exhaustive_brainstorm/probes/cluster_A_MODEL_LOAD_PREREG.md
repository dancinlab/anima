# Cluster A — PREREG for $0 model-load probes NOT run on mini this turn

Constraint: mini 16GB has 3.71GB free + 3.27GB swap used at audit time. Governance
`heavy-anima-eval-pool-not-mini`: anima 303M decode/eval on mini = swap OOM rc=137.
`a_dont_kill_live_compute`: do not start a job that will wedge. So the 303M-load probes
below are PREREG'd frozen but NOT executed this turn. Mechanism is single-load +
`core/decode.py::bg_forward_last_hidden` (one forward per concept; never load twice).
Runnable on owned pool (summer/aiden RTX5070) — still $0, not a rent.

## A5 — paraphrase orbit (latent invariance)
- Falsifier: same relation, lexical/order/voice surface change. If hidden(last) of the
  paraphrase orbit collapses (cosine > 0.95 across orbit) while a content-control does not,
  the model treats surface as invariant — good. If PASS appears on only one surface form,
  FAIL (per README anti-gaming §4).
- PREREG bar (frozen): orbit-invariance cosine(orbit_i, orbit_j) >= 0.90 AND a
  content-swapped control cosine <= 0.60, on >=2/3 seeds. Diagnostic (DIRECTIONAL on mini).
- Mini verdict: NOT-RUN (OOM risk). Single forward x ~4 paraphrases x 1 concept, one load.

## A7 — counterfactual reversal (latent antisymmetry)
- Falsifier: `A>B` vs `B>A` must produce different last-hidden. Symmetric output
  (cosine > 0.97 or argmax relation identical) => additive/bag floor (README §A7).
- PREREG bar (frozen): 1 - cosine(h(A>B), h(B>A)) >= 0.10 on >=2/3 seeds AND a
  content-identical control (A>B vs A>B) cosine >= 0.99. Diagnostic.
- Mini verdict: NOT-RUN (OOM risk). Two forwards, one load.

## A8 (G1 side) — grow-window × {7,4302,4303} multi-seed, per ckpt
- Wrapper exists: state/g1g6_h9200_validation/g1_growwindow_multiseed.py.
- H_6190 ran ONE rng seed on g1_realign (PASS_raw / FAIL_novel echo-guard). 3-seed
  expansion + cross-ckpt sweep is the unmeasured P0 residual.
- PREREG bar (frozen): per ckpt, report pass_raw / pass_novel across 3 seeds; FROZEN
  bar is pass on >=2/3 seeds (mirrors G6 frozen majority). tune-to-green forbidden.
- Mini verdict: NOT-RUN (OOM risk under current swap). Pool-runnable per ckpt (~105s/seed).
- NOTE: G6 side of A8 is DONE — engine-native 3-seed [3,3,5] terminal measured
  (state/g6_bind_gate/decode_terminal/engine_native_verdict.json).

## A3 — held-out pair split
- Needs a NEW corpus (primitive train, specific pair/relation permanent holdout) + retrain.
- $0 piece is only the leak-audit design (verify holdout cells have zero train leak) —
  not a frozen falsifier by itself. Actual measurement = trunk retrain = GPU-gated.
