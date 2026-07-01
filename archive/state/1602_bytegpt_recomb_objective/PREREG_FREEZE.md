# H_1602-ByteGPT RECOMB-OBJECTIVE — FROZEN PRE-REGISTRATION (before any measurement)

Frozen UTC: 2026-06-30 (this file written BEFORE training/measuring; tune-to-green forbidden, p7/c9).

## Question (a_break_the_wall, lens = training OBJECTIVE × attention trunk)
The objective lever (recombination aux-loss) floored G1 on the **ConvMoE** trunk
(H_1602 9/9 composed_distinct=0; H_1819 op×obj 0/3). The un-tested cell is the SAME
objective on the **ByteGPT (24-layer attention)** trunk — content-addressed fetch-and-bind.
Does recomb-objective lift engine-native G1 above the floor (0) where plain-CE ByteGPT
(h1129 engine-native: max_single=2, best_distinct=2, no lift) AND objective-ConvMoE both fail?

## A/B (decisive — identical seed/steps/corpus/data-RNG; only the loss differs)
- **ARM-OFF (control):** `--objective ce_marginal` — standard next-byte CE.
- **ARM-ON (treatment):** `--objective infonce` — CE + λ·InfoNCE (frozen λ=1.0, neg=64,
  reference-matched from state/1602_recomb_objective/trainer.py).

## Config (frozen)
- arch = ByteGPT d=1024 / L=24 / H=16 / block=512 (== h1129 shape, ~303M); savant
  golden-zone cusp-anneal ON (GZ_LOWER=0.21231792755821914, i0=0.5, i_floor=0.16231…).
- corpus = 4-cell register {ko-general, en-general, ko-sns, en-sns}
  (anima-corpus-{ko,en}-{general,sns}), proportional sample, val_frac=0.05,
  seq_len=512, batch=8, steps=2000, bf16, lr=3e-4.
  ACTUAL effective bytes (balanced, pulled from HF on mac → rsync to summer, summer is
  LAN-only no-internet): ko-general 7.999MB · en-general 8.000MB · ko-sns 6.184MB ·
  en-sns 1.326MB (total ~23.5MB → ~8.2M train tokens at 2000×bs8×seq512 ≈ 0.35 epochs,
  well below the clm303 memorization regime). KNOWN DEFECT (does NOT confound the A/B —
  both arms see IDENTICAL corpus): published anima-corpus-en-sns is a dup of en-general
  content ("Anarchism…" wiki text), per memory clm303-clean-4cell-corpus-hf en-sns
  KNOWN-SMALL/보강 ING. The lever's causal G1 effect (ON vs OFF on the same data) is
  unaffected; report the en-sns caveat in RESULT.
- measurement engine = `cli/evaluate.py <bin>` → core/g_gates.py → core/bytegpt_decode.py
  (py 2-production, byte-parity ByteGPT mouth; terminal-eligible, NOT a torch probe).

## FROZEN BARS (H_1129 VERBATIM — NO bar change after measuring)
- **G0 (kwr):** n_coherent ≥ … ; coherence ratio kwr ≥ 0.50 per coherent gen.
- **G1 (recombination, the decisive gate):** ∃ k∈{2..5} with
  `composed_distinct ≥ 2  AND  composed_distinct > max_single  AND  coherent (kwr≥0.50)`.
  At the native 80/120 ladder (g_single=80, g_comp=120). PASS iff some k clears.
- **G2 (novelty):** n_novel > 0 with control_novel = 0 (corpus-absent).
- **G6 (ideation★):** dist ≥ 5 AND falsifiable ≥ 1.
- **closure a7b_pass = G0 ∧ G1 ∧ G2.**
- **held-out DESCENT gate (a_savant_train):** every register held-out val_CE < uniform
  (ln256 = 5.5452); an arm that overfits (held-out NO-DESCENT) is DISQUALIFIED, not promoted.

## DECISION TEST (pre-registered)
The objective lever **CRACKS G1 on ByteGPT** iff:
  **ARM-ON G1 PASS  AND  ARM-ON G1 strictly > ARM-OFF G1** (composed_distinct lift above floor),
  with both arms held-out DESCENT PASS.
Frozen prediction (consistent with 4-lens ConvMoE floor + ByteGPT-h1129 engine floor):
  **ARM-OFF G1 = FAIL (floor), ARM-ON G1 = FAIL (floor)** — i.e. the objective does NOT
  crack G1 even on attention. If ARM-ON instead clears G1>OFF, that is a genuine
  wall-break and the first engine-native G1 PASS in the campaign. Honest either way (c9).

## Measurement command (frozen)
`python3 cli/evaluate.py <bin> --corpus <ko-gen> <en-gen> <ko-sns> <en-sns> --gen 80`
(--gen 80 explicit so g_eval_g1 reaches the native 80/120 ladder, NOT the --gen 0 → 40 collapse).

## ckpt discipline (a_fire_recover_complete)
.pt + .bin PULLed to permanent storage (~/anima-weights/bytegpt_recomb_303m/) BEFORE any
teardown. Engine-native re-measure on the .bin (not the torch probe). Per-arm seed = 7
(single-seed A/B for cost; multiseed follow-on only if ARM-ON shows a non-floor lift).
