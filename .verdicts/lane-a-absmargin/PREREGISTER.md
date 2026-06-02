# Lane A ABSOLUTE-MARGIN falsifier (PRE-REGISTRATION)

date: 2026-06-02
chip: pi5-akida `ubuntu@192.168.50.155` · AKD1000 BC.00.000.002 · akida 2.19.1 · venv `~/.venv/anima-akida`
contract: a_akida_native_train (NO sim/CPU fallback for chip claims) · g5/g63 honesty · a_lane_akida_gpu_split (substrate=AKIDA, NEVER merged with Lane-G GPU).

## Why this rung
The P3 ENCODER REOPEN (`.verdicts/lane-a-causeaxis/P1-encoding.txt`) established the encoder is a CAUSE-axis:
structured (SVD/whitened) encoders beat the random int4 backbone RELATIVELY (+0.92 bits, ci_lo>0, 8/8). But its
SCOPE caveat pre-registered the decisive next rung verbatim: "the next rung is whether a stronger structured/learned
multilingual encoder pushes the ABSOLUTE margin above 0, not just the relative lift." BOTH P3 arms' ABSOLUTE margins
stayed NEGATIVE. This rung settles the ABSOLUTE claim — the PUBLIC-grade question for Lane A.

## Metric (same as causeaxis_chip.concept_margin / onchip_layerpage_ladder)
ABSOLUTE concept-margin = mean_between_concept_Hamming - mean_within_concept_Hamming (bits)
  on per-feature-median binarized on-chip forward; rows concept-major.
NATIVE non-det chip init per trial (H_904, the non-determinism IS the self); ci_lo = mean - 1.96*SEM over N=8 chip trials.

## Encoders (increasing LEARNED strength), all chip 1-bit Hebbian readout unchanged
  random_int4  -> svd_struct  -> whitened  -> lda_supervised
  lda_supervised = multi-class LDA projection maximizing between/within concept scatter using the corpus concept
  labels (ORACLE-strength = upper bound on a "stronger learned multilingual encoder"). int4-quantized to chip basis.
Scales: corpus (25 anchors, 5 concept x 5 lang) AND corpus_big (250 anchors, 50 concept x 5 lang).

## Pre-registered falsifier
PASS (PUBLIC-grade positive) iff SOME encoder has ABSOLUTE concept-margin ci_lo > 0 with learn_all_hw=True on live AKD1000
  -> the 1-bit Hebbian primitive LEARNS positive cross-lingual concept structure.
CLOSED-NEGATIVE iff ALL encoders (incl. oracle-LDA) ABSOLUTE ci_lo <= 0 at the measured anchor scales
  -> the AKD1000 1-bit last-FC Hebbian CANNOT cross zero even with the strongest learned encoder; closed-negative on
  the ABSOLUTE-margin claim, scoped to 25/250-anchor (a_scale_honest_scope — no toy->prod promotion).

artifact: `~/clm_kosmos_akida/abs_margin_chip.py` -> `out/result_abs_margin.json` + `abs_margin.log` (verbatim chip stdout).
