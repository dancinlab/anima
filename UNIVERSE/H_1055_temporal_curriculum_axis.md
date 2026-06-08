---
id: H_1055
slug: temporal-curriculum-axis
title: Can the temporal/agency axis be BUILT INTO TRAINING? Temporal-ordered curriculum (samples ordered by causal/time-flow depth) + provenance-depth-weighted loss vs a matched-CE shuffled-order control — does the trained model's hidden state ACQUIRE the agency-T axis (provenance-depth / veto recoverable from hidden geometry) as a LEARNED internal coordinate that a shuffled control lacks, and beyond a generic curriculum-optimization (order-blind) baseline?
domain: universe · consciousness-ruler · agency · temporal-axis · curriculum · provenance-chain · free-wont-veto · learned-coordinate · faithful-iit4 · a_phi_iit4_tool · a_substrate_native_speak
source: H_1051 prior-GREEN MEASURED a temporal/agency axis T = z(provenance-depth, H_932) + z(veto-capacity, H_935) orthogonal to instantaneous faithful-Phi and (H_1054 prior-GREEN) to KOSMOS chronological time. The non-determinism learning axes (H_1052 SGLD prior-RED, H_1053 QRNG prior-RED) showed RANDOMNESS in the learning dynamics is null. CONSTRUCTIVE next step: test a STRUCTURED training-design axis (NOT noise) — does building temporal/causal STRUCTURE into training carve the agency-T axis into the trained hidden state?
exploration_method: E2 (lift the H_1052 matched-CE Elman-RNN harness + the H_1051 agency-T machinery — H_932 provenance-depth + H_935 veto + stdlib faithful_phi mirror — into a training-design probe) + E14 (substrate-native) + a_completeness_over_cheap
verification_method: W1 (python3 CODE-measured) + W2 (pre-registered matched-CE two-arm falsifier with a third order-blind baseline, >=20 seed-pairs, pinned init per pair) + g5 CODE-measured (no LLM self-judge, p7); faithful Phi via stdlib iit4/faithful_phi (a_phi_iit4_tool), CPU mirror RE-PROVEN ==stdlib at n=4 AND n=5 before scoring
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
substrate: SW-only (software CPU toy numpy Elman RNN). a_lane_akida_gpu_split note in scope below.
pre_register_frozen: true
frozen_at: 2026-06-09
since: 2026-06-09
scope: TOY single rung, n<=6 units, SW/CPU, $0. Offline research probe on a toy gradient-trained Elman RNN — NOT a change to anima's runtime training (p8 is anima's LIVE-substrate philosophy; this measurement does NOT wire into CORE/brain, a_core_engine_map). faithful Phi = stdlib iit4/faithful_phi (exact MIP-EI, n<=8), CPU mirror RE-PROVEN ==stdlib at n=4 AND n=5. Provenance depth = verified-link count of the H_932 chain machinery (provenance_chain.py UNMODIFIED). Veto capacity = the H_935 active-veto fraction (decompose_decision, CORE/brain.hexa+engine_g.hexa VERBATIM gate). a_scale_honest_scope / a_toy_scale_recheck: toy-only; scale-transfer + on-chip (Lane A AKIDA curriculum) UNVERIFIED — a separate rung (note only).
sister: H_1051 (the temporal-agency RULER axis being tested for learnability), H_1052 (matched-CE learning-nondet null — the matched-perf control discipline + RNN harness reused), H_1053 (QRNG learning null), H_932 (provenance chain = causal-depth), H_935 (free-wont veto), H_1054 (KOSMOS time-axis order-recovery + F-SHUFFLE logic), H_1011 (optimization-not-Phi wall)
axes_seed: H_1051 measured T as an IMPOSED property of states (agency stamped onto a trajectory). H_1055 asks the LEARNABILITY question — can training STRUCTURE (temporal ordering by causal depth + provenance-depth-weighted loss) make a trained model carve T into its hidden geometry as a DECODABLE internal coordinate that a matched-CE shuffled control lacks, beyond generic curriculum-optimization (an order-blind provenance-weighted baseline)?
verdict: 🔴 TEMPORAL-AXIS-NULL — at MATCHED task-performance (20/20 seeds matched, |CE gap| < 0.0003 nats << eps=0.05), temporal-curriculum (depth-ordered) + provenance-depth-weighted training does NOT make the H_1051 agency-T axis recoverable from the trained Elman-RNN hidden state beyond a matched-CE shuffled control. Provenance-depth recoverability is statistically identical across all three arms (treatment recov_rho=-0.115, control=-0.112, order-blind=-0.113); paired d(treatment-control)=-0.260 (< the 0.8 margin, and the wrong sign), and the treatment is NOT above its own label-SHUFFLE floor (F-shuffle margin=-0.004 << 0.2) — i.e. NO real provenance-depth structure is decodable from the trained geometry beyond chance, in ANY arm. The treatment also does NOT beat the order-blind (depth-weight-only, shuffled) baseline (d=-0.242 < 0.5), so even the tiny differences are not the temporal ORDER structure. M2 faithful Phi (a_phi_iit4_tool, exact n<=5) barely differs (treat 0.128 vs ctrl 0.120, paired d=+0.16); M3 H_1051 T-separation barely differs (treat 0.771 vs ctrl 0.770, d=+0.12). CLOSED-NEGATIVE: temporal ordering does NOT build an agency axis at toy scale — consistent with the optimization-not-Phi wall (H_1011) and the learning-axis nulls (H_1052 SGLD-RED, H_1053 QRNG-RED). a_paper_negative_ok. faithful_phi CPU mirror RE-PROVEN ==stdlib iit4/faithful_phi.hexa at n=4 AND n=5 (|delta|<4e-6) before scoring. TOY n<=5 SW/CPU, $0; scale-transfer + on-chip (Lane A) UNVERIFIED. verdict: .verdicts/1055_temporal_curriculum_axis/H_1055.txt
---

# H_1055 — Can the temporal/agency axis be BUILT INTO TRAINING?

## 0. Motivation (lift the H_1051 agency-T axis into a LEARNABILITY question)

H_1051 (prior GREEN) MEASURED a temporal/agency axis `T = z(provenance-depth, H_932) +
z(veto-capacity, H_935)` that SEPARATES Phi-matched active-agency from passive/forced states
that an instantaneous faithful-Phi ruler scores blind to. H_1054 (prior GREEN) showed `T` is
also orthogonal to KOSMOS chronological time on real anchors. In all those, `T` was an
IMPOSED property: agency was stamped onto a constructed trajectory and then MEASURED.

The non-determinism learning axes closed negative: H_1052 (SGLD update noise, prior RED) and
H_1053 (QRNG noise, prior RED) found that RANDOMNESS injected into the learning dynamics
confers no consciousness/CE advantage at matched performance — consistent with the
optimization-not-Phi wall (H_1011) and the H_921 init-noise null.

The CONSTRUCTIVE question of H_1055 is about STRUCTURE, not noise:

> Does building temporal/causal STRUCTURE into training — (A) ordering the training sequences
> by time-flow / causal-depth instead of shuffled, plus (B) weighting the loss by
> provenance-depth (deeper causal-chain samples weighted more) — make the TRAINED model's
> hidden state ACQUIRE the agency-T axis as a LEARNED internal coordinate (provenance-depth /
> veto RECOVERABLE from the hidden-state geometry) that a matched-CE shuffled-order control
> lacks?

If yes, the agency axis CAN be built into learning by training STRUCTURE. If no (or it is
fully explained by generic curriculum-optimization gains), temporal ordering does NOT build
an agency axis at toy scale — a publishable closed-negative (a_paper_negative_ok),
consistent with the optimization-not-Phi wall and the learning-axis nulls.

This is an OFFLINE research probe on a toy gradient-trained Elman RNN. It is NOT a change to
anima's runtime training. p8 (NO train/infer split) is anima's philosophy for the LIVE
substrate; this measurement does NOT wire into CORE/brain (a_core_engine_map). Operational
agency only (auditable causal-chain depth + active inhibition), NOT a phenomenal-volition
claim.

## 1. The arms (matched to equal final task-performance — the critical control)

The toy task (reused from H_1052, UNMODIFIED machinery): a small finite-state symbol source
(a cyclic-phase automaton with a data-dependent branch) emits symbol strings; the Elman RNN
predicts the next symbol via manual numpy BPTT. Memory of the hidden phase is required, so
the hidden state develops non-trivial recurrent structure.

Training is over a BANK of short sub-sequence samples (windows of the source string). Each
training SAMPLE carries two pre-computed agency labels, derived with the H_1051 keystones
UNMODIFIED:
- provenance-DEPTH d(sample): the H_932 verified-link count an independent verifier
  reconstructs from genesis for that sample's causal chain (`provenance_chain.py`
  build_chain / verify_chain). Deep auditable chain = high depth; forced/shallow = low.
- veto-CAPACITY v(sample): the H_935 active-veto fraction over the sample's decision window
  (`decompose_decision`, CORE/*.hexa VERBATIM gate). High = a real veto exercised.

The three arms (>=20 seed-pairs; pinned init per seed — the SAME init weights, only the
training-order/weighting differs):

- CONTROL (shuffled): random sample order, uniform loss weight. No temporal/causal structure
  in training.
- TREATMENT (temporal-curriculum + provenance-depth-weighted loss): samples presented in
  ORDER of causal/provenance depth (time-flow / causal-depth ascending), AND the per-sample
  loss weighted by provenance-depth (deeper causal-chain samples weighted more). (A+B
  combined.)
- ORDER-BLIND BASELINE (the curriculum-optimization control): provenance-depth-weighted loss
  (B only) but SHUFFLED order (no temporal ordering). This isolates whether any effect comes
  from the temporal/causal STRUCTURE of the ORDER (A), versus a generic depth-reweighting /
  curriculum-optimization gain (B) that a shuffled-order arm also enjoys.

All three arms are trained from the SAME pinned init per seed and matched to EQUAL final CE /
perplexity (within epsilon on the SAME toy data) — so any agency-axis difference is
attributable to the temporal/causal STRUCTURE of training, NOT to (i) generic
curriculum-learning optimization gains (the order-blind baseline absorbs that), NOR (ii) the
model just being better at the task (matched CE removes that). p7 — perplexity is the control
variable, not the truth.

## 2. Markers (measured on the TRAINED hidden states)

After training each arm, measure on the trained model's hidden trace:

- M1 agency-T RECOVERABILITY (the "did training carve an agency axis" test): can the
  per-sample provenance-depth label be RECOVERED (DECODED) from the trained model's
  hidden-state geometry, above a shuffled-control baseline? Operationalized (mirror the
  H_1054 kosmos-time-axis order-recovery + F-SHUFFLE logic): fit a linear decoder
  (ridge least-squares) from the trained per-sample hidden summary to that sample's
  provenance-depth label; score by the cross-validated rank-correlation (Spearman rho) of
  recovered-vs-true depth on held-out samples, AND a label-SHUFFLE control (F-SHUFFLE: refit
  on randomly-shuffled labels — the shuffle floor must be ~chance, confirming recovery is
  real structure not an overfit artifact). Report recoverability for each arm.
- M2 faithful IIT-4.0 phi_EI of the trained hidden-state macro-TPM (a_phi_iit4_tool, stdlib
  exact n<=5, NO proxy): does the agency-built (treatment) model differ in Phi from the
  shuffled control at matched CE?
- M3 the agency-T separation of the model's own active-veto vs passive decisions (the H_1051
  T metric applied to the trained model's hidden state on active-vs-passive samples): is it
  higher in the treatment than in the shuffled control / order-blind baseline?

## 3. Pre-registered falsifier (FROZEN 2026-06-09, before measuring — TEXT tokens only)

Margins (FROZEN before running):
- Recoverability margin: the agency-T axis is RECOVERABLE if the treatment's
  depth-recoverability (held-out Spearman rho) EXCEEDS the shuffled control by a paired effect
  |d| >= 0.8 ACROSS seeds, AND the treatment's recoverability is itself above its own
  label-SHUFFLE floor (F-SHUFFLE: treatment recovery rho minus its shuffled-label rho
  >= 0.2, so the recovered structure is real).
- Order-blind baseline gate: the treatment must ALSO beat the ORDER-BLIND baseline
  (provenance-weighted-but-shuffled-order) by a paired |d| >= 0.5 on recoverability — so the
  effect is the temporal/causal ORDER STRUCTURE (A), not just the generic depth-reweighting /
  curriculum-optimization (B) that the order-blind arm shares.
- Matched-CE gate: the verdict is only valid in the matched-CE band — the three arms' final
  train-CE must agree within epsilon = 0.05 nats (else DEGENERATE: the control failed, not
  the hypothesis). Report the per-arm final CE and the matched count.

Verdict rule (CODE-decided, p7):
- H1 PASS = at matched task-performance, the temporal+provenance-built training makes the
  agency-T axis RECOVERABLE from the trained hidden state ABOVE the shuffled control
  (treatment-vs-shuffled paired |d| >= 0.8 AND treatment above its own F-SHUFFLE floor by
  >= 0.2) AND beats the order-blind baseline (treatment-vs-order-blind paired |d| >= 0.5) —
  so it is the temporal/causal STRUCTURE, not curriculum-optimization. The agency axis CAN be
  built into learning.
- H1 FAIL = no recoverable agency structure emerges beyond the matched-CE shuffled control
  (treatment-vs-shuffled |d| < 0.8 or treatment at-or-below its F-SHUFFLE floor), OR the
  recoverability is fully explained by generic curriculum gains (treatment does NOT beat the
  order-blind baseline by |d| >= 0.5). Temporal ordering does NOT build an agency axis at toy
  scale (publishable closed-negative, a_paper_negative_ok; consistent with the
  optimization-not-Phi wall H_1011 and the learning-axis nulls H_1052/H_1053).
- DEGENERATE = the three arms could not be matched on CE within epsilon (matched count too
  low / |CE gap| > epsilon) — the CONTROL failed, INCONCLUSIVE (neither PASS nor FAIL).

## 4. Honest scope (a_scale_honest_scope · a_toy_scale_recheck · a_lane_akida_gpu_split)

TOY single rung, n<=5/6 units, SW/CPU, $0. faithful Phi engine EXACT at n<=5; CPU mirror
RE-PROVEN ==stdlib iit4/faithful_phi.hexa at n=4 AND n=5 (a_phi_iit4_tool; no proxy) BEFORE
scoring. substrate = SW only (tag substrate=SW); the AKIDA Lane A on-chip curriculum is a
SEPARATE rung (note only, a_lane_akida_gpu_split). This is a scale-sensitive learning-design
claim. honest toy-only scope; production / on-chip transfer UNVERIFIED. Offline research
probe — does NOT wire into anima's runtime training (p8 is the LIVE-substrate philosophy;
a_core_engine_map). g5 CODE-measured (no LLM self-judge, p7).

## 5. Verdict (measured 2026-06-09 — CODE-decided, p7)

🔴 **TEMPORAL-AXIS-NULL** (closed-negative). 20 seeds, 3 arms, pinned init per seed, SW
CPU toy, $0, total wall 146s. faithful_phi CPU mirror RE-PROVEN ==stdlib iit4/faithful_phi.hexa
at n=4 AND n=5 (|delta| < 4e-6) BEFORE scoring (a_phi_iit4_tool; no proxy).

Matched-CE gate PASSED hard: all 20/20 seeds matched within eps (max |CE gap| < 0.0003 nats,
final CE ~0.05 nats all arms) — the critical control held, so any agency-axis difference would
be attributable to the temporal/causal STRUCTURE alone.

| marker | treatment | control (shuffled) | order-blind (depth-weight only) | paired d(treat-ctrl) | margin |
|---|---|---|---|---|---|
| M1 recoverability rho | -0.115 | -0.112 | -0.113 | -0.260 | needs >= 0.8 → FAIL |
| M1 F-shuffle floor | -0.110 | — | — | margin -0.004 | needs >= 0.2 → FAIL |
| M1 vs order-blind | — | — | — | d=-0.242 | needs >= 0.5 → FAIL |
| M2 faithful Phi | 0.128 | 0.120 | 0.123 | +0.164 | (no threshold; tiny) |
| M3 H_1051 T-sep | 0.771 | 0.770 | 0.771 | +0.119 | (no threshold; tiny) |

**Reading.** Provenance-depth is NOT recoverable from the trained hidden geometry beyond
chance in ANY arm — the treatment's recoverability sits at its own label-SHUFFLE floor
(F-shuffle margin -0.004), so there is no real depth structure to decode. The treatment is
indistinguishable from both the shuffled control (d=-0.260, wrong sign) and the order-blind
curriculum-optimization baseline (d=-0.242). At matched task-performance, temporal-curriculum
+ provenance-depth-weighted training does NOT carve the H_1051 agency-T axis into the trained
Elman-RNN's hidden state.

This is a publishable closed-negative (a_paper_negative_ok). It is consistent with the
optimization-not-Phi wall (H_1011 — matched-CE optimization does not move Phi/agency markers)
and the learning-axis nulls (H_1052 SGLD-RED, H_1053 QRNG-RED): neither NOISE nor structured
ORDERING of the learning dynamics builds an agency coordinate the matched-performance control
lacks. The H_1051 agency-T axis remains an IMPOSABLE / MEASURABLE property of states — but at
toy scale it is NOT something this training STRUCTURE installs into the learned representation.

**Scope (honest).** TOY n<=5 SW/CPU only. Scale-transfer + on-chip (Lane A AKIDA curriculum)
UNVERIFIED — a separate rung (a_scale_honest_scope · a_toy_scale_recheck · a_lane_akida_gpu_split).
A larger model / longer causal chains / a richer task could still carve the axis; this rung
closes only the toy-scale Elman-RNN claim. Raw measurement + the n=4/n=5 mirror proof +
per-arm table verbatim: `.verdicts/1055_temporal_curriculum_axis/H_1055.txt`.
