# Lane A LIFT — CAUSE-AXIS breakthrough probe battery (PRE-REGISTRATION)

date: 2026-06-02
chip: pi5-akida `ubuntu@192.168.50.155` · AKD1000 BC.00.000.002 · akida 2.19.1 · venv `~/.venv/anima-akida`
contract: a_akida_native_train (NO sim/CPU fallback for chip claims; CPU-local ONLY for re-scoring already-captured tensors) · g5/g63 honesty.

## Background — why these 3 axes
The /gap full sweep found the 4 FALSIFIED lift-cause axes (corpus / quant / depth / noise = ha2/ha3/ha4 + ladder)
are FIX-axes (they tune an already-chosen pipeline) not CAUSE-axes. Every one of them — and Hc_1306 — sits DOWNSTREAM
of one fixed design choice that was NEVER varied:
  BACKBONE_INT4 = rng_bb.integers(-7,8,(256,256))  (a FIXED RANDOM input encoder)
  + AkidaUnsupervised 1-bit Hebbian on last-FC  (objective+readout)
  + rate-code 1-bit Hamming readout  (discards spike timing).
These 3 are the untested CAUSE-axes. ALL probes ESCAPE the falsified 4 axes.

## Metric (shared, matches established ladder methodology onchip_layerpage_ladder.py:concept_margin)
signal = mean_between_concept_Hamming - mean_within_concept_Hamming  (bits, higher=better)
  on the per-feature-median-binarized forward output; rows concept-major (row = concept*5 + lang).
lift = signal_treatment - signal_control.
ci_lo = lower bound of the lift's CI. Bootstrap over the 5 concepts (resample concept blocks, B=2000)
  for the static re-score CI; for chip probes, paired across chip trials (per-trial stochastic init, H_904),
  ci_lo = mean_lift - 1.96*SEM over trials (same convention as onchip_multitrial.py).
PASS / REOPEN iff ci_lo > 0 at >=1 rung.  FALSIFIED (hardens closed-negative) iff lift <= 0 (ci_lo<=0) everywhere.

---

## PROBE 1 — INPUT-ENCODING (highest leverage)  [chip + CPU-rescore]
CLAIM: the closed-negative is an artifact of the FIXED RANDOM backbone. A learned/structured cross-lingual
encoder in the chip input space surfaces lift.
TREATMENT encoders (vs random-int4 control, on the SAME 25 anchors, SAME chip 1-bit Hebbian readout):
  E1. SVD/PCA-structured projection of the 5-lang anchor byte-histograms -> top-256 structured axes -> int4 -> chip input.
  E2. covariance-whitened structured projection (decorrelate the anchor feature space) -> int4 -> chip input.
  (Both are STRUCTURED linguistic encoders replacing the random projection; chip 1-bit readout unchanged so the
   ONLY changed axis is the encoder.)
FALSIFIER (pre-registered): with a structured encoder replacing random-int4, on live AKD1000, the cross-lingual
  concept-margin lift has ci_lo > 0 at >=1 encoder. 
  -> FALSIFIED (lift stays <=0) => encoder is NOT the bottleneck; closed-negative HARDENS to cover the ENCODING axis.

## PROBE 2 — OBJECTIVE + READOUT-LOCUS  [chip-native]
CLAIM: 1-bit AkidaUnsupervised on last-FC was a backend-availability choice, not the only liftable rule.
SUB-TESTS on live chip:
  (a) weights_bits=4 (native) vs 1-bit — does richer weight precision surface lift?
  (b) AkidaSupervisedLearning vs unsupervised — IF the SDK exposes it. (PRE-CHECK: akida 2.19.1 dir() shows ONLY
      AkidaUnsupervised — if confirmed absent, record (b) as N/A-SDK honestly, do NOT fabricate.)
  (c) PRE-binarization analog FC activations (margin in the int-valued forward space, before per-feature 1-bit
      threshold) vs post-1-bit-Hamming readout.
FALSIFIER: any of (a)/(b)/(c) shows lift ci_lo>0 where 1-bit-unsupervised-post-binarize showed <=0.
  -> FALSIFIED (all stay <=0) => objective/readout-locus is NOT the bottleneck.

## PROBE 3 — TEMPORAL-CODE / spike-timing  [chip capture if SDK exposes; else honest temporal proxy]
CLAIM: the rate-code 1-bit Hamming readout discards spike TIMING; lift may live in STDP-style timing.
  Hc_1306 only tested STATIC signals (multi-bit-L1, cosine, faithful-Phi).
SUB-TEST: attempt on-chip spike-event capture (akida SDK) for the 5-lang anchors; compute a timing-aware
  cross-lingual margin (inter-spike-interval / coincidence-window stats, OR Spearman of per-unit spike-rank-order
  vs concept-ID). IF the SDK cannot expose spike timing, STATE SO EXPLICITLY and fall back to the highest-resolution
  temporal proxy the chip exposes (per-unit multi-step activation-rank order across the 25-anchor sequence — a
  rate-resolution proxy, NOT fabricated spike timing).
FALSIFIER: timing-aware margin ci_lo>0 where rate-margin showed <=0.
  -> FALSIFIED (flat) => lift is not hiding in spike-timing.

## DISPOSITION RULE
ALL 3 <=0  => closure HARDENS: closed-negative now covers encoding+objective+readout+timing
  = 8 axes total (4 prior fix-axes + 4 new cause-axes) — publishable NEGATIVE.
ANY ci_lo>0 => Lane A P3 REOPENS on that axis; report axis + verbatim margin.
