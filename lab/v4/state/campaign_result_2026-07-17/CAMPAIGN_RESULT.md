# anima-v4 — TERMINAL CAMPAIGN RESULT (2026-07-17)

> The tension-mechanism exploration is complete: all seven candidates are dispositioned. This is the
> campaign's terminal synthesis. Every number is cited with the ARM that produced it and that arm's source
> path. SSOT for the distilled form is `ARCHITECTURE.json → campaign-result`; this document is the prose.

## 1. The one-sentence result

**On a 3.7M-parameter byte-level Korean trunk (d=384, L=4, templatic drill register), a hand-staged
parse-disagreement tension FIELD injected write-side (pre-trunk) causes a held-out cognitive operation —
compositional honorific binding — beyond its own rank-1 compression: F1 Δd_acc(A-duel − A-rank1) = 0.3789
(seed 0) / 0.3802 (seed 1), A-duel f2″ = 1.0 vs A-rank1 0.6211 / 0.6198, free-slot scoring, both seeds
clearing the 0.15 bar** (arm: A-duel vs A-rank1, H_004 G-2; source:
`state/h004_parser_duel_tension_rank_drill_2026-07-16/train_result_full.json` + `verdict.json`, verdict
verbatim in `HYPOTHESES/cards/H_004_parser_duel_tension_rank_drill.md`). The claim is **FIELD-FORMAT causal,
not values-causal**: the concord χ was hand-computed, and the learned-values extension measurably fails to
reproduce it (H_005 K3: A-χ̂ f2″ 0.82 / 0.71 vs A-hand 1.0; `state/h004_.../verdict_g3a.json`).

## 2. Does it validate the thesis? — the verdict and its exact boundary

The thesis: a two-engine tension can carry thought only if the coupling is high-dimensional, iteratively
resolved, and resident in the objective/data/codec. anima(v1) died on PLACEMENT — a readout-side scalar
seam, rank-1, carrying exactly 1 bit (salvage L1/L2/L3).

**What is proven: the PLACEMENT claim.** mech-1's sealed measurement escapes both of v1's deaths,
write-side, with the two falsifiers built specifically to catch them:

- **Not a 1-bit seam (v1's L1)**: F4 off-top rank-mass = 0.6467 / 0.6963 ≥ 0.20 both seeds — the resolver
  reads a genuinely high-rank field, on a rank-6 multi-bind superposition (K=6 MULTI-BIND panel, per-item
  T = Σ c_k M_k, pre-run off-top 0.8333; `build_honbind_multi.py`, `panel_f2doubleprime.json`).
- **Not replacement-not-coupling (v1's L2)**: F5 strip-resolution collapses A-duel 1.0 → 0.5 (d_dacc =
  0.5 / 0.5, dCE 1.9343 / 1.9177) — the decoder needs the resolved field, not any-tensor capacity.
- Measurement clean both seeds: F2 liveness 1.0 / 1.0, precond drill 1.0 / 1.0, F3 C-scaf 0.4935 / 0.5534
  < 0.60, F6 placebo gap 0.375 / 0.3659, harness C-perm 0.4648 / 0.4857 ∈ [0.45, 0.55] (all:
  `collect_verdict_h004.py` stdout, H_004 card).

So: **a write-side tension field, resident pre-trunk in the data path, carries a held-out compositional
operation beyond any rank-1 summary of itself. The v1 death is escaped by placement.** That much the
campaign establishes cleanly, at 2 seeds, with the placebo, scaffold, and harness arms all in band.

**What is NOT proven: the self-organizing-tension claim — and this boundary is the crux.** The field's
values (χ, the concord signs) were hand-computed. Both halves of making the tension *learned* were then
measured or closed-form-bounded at this scale:

- **Values half (H_005, G3-a)**: a ~3k-param learned bilinear χ̂ = g(φ) on the fixed support reached f2″
  0.82 / 0.71 vs the hand field's 1.0 — F1a′ non-inferiority fails on both seeds including the fit seed
  (margins −0.176 / −0.290), with fit instability 1.0 / 0.832 on its own drill. Verdict K3: the measured
  cost of removing the hand is 0.18–0.29 d_acc. Notably F1a itself *passes* (Δ(A-χ̂ − C-χ̂plc) = 0.298 /
  0.191 ≥ 0.15): what the learned values do carry still requires correct edge alignment — the failure is
  identification, not capacity. (`state/h004_.../g3a_result_full.json`, `verdict_g3a.json`.)
- **Support half (H_006, G3-b)**: never opened, on closed-form arithmetic over H_005's own measured numbers
  — E[A-tduel] ≈ 0.53 + 0.24·r gives non-inferiority NEGATIVE headroom at any support recall r, and the
  Δ-form needs r ≥ 1.25 against a literature anchor of 0.46–0.50 (directed attachment, ≥8M/English/
  word-level). BURNED as inadmissible, not falsified. (`state/h004_.../REGATE_g3b_feasibility_fable5.md`.)

**Honest verdict on the thesis: PARTIAL — architecture validated, autonomy unreached.** The campaign proves
that write-side is the correct placement for a tension that carries thought (the format is causal, the
operation is compositional and held-out, the coupling is measurably high-dimensional and measurably needed).
It does not prove that a tension *self-organizes* into that field under training pressure — at 3.7M/byte/
Korean/templatic, the learned version hits a substrate wall on values and an inadmissible falsifier on
support. The distance between "a hand-staged field works" and "the two engines produce that field
themselves" is exactly the distance this campaign leaves open, and it is stated as such everywhere the
result is cited.

## 3. What the disposed map means

The mechanism space is not unexplored; it is **dispositioned** — every one of the 7 candidates has a sealed
verdict, a $0 closed-form wall, or a don't-open gate, and the fake-diversity audit (`fd.true-axes`) reduces
the 7 to three independent axes, each of which is now closed:

| axis | mechanisms | disposition |
|---|---|---|
| structure-conflict-resolution | mech-1 · mech-6 | mech-1 🟢 SEALED (the positive); mech-6 ⛔ DON'T-OPEN (twin-redundant + walled) |
| residual-rewrite | mech-2 · mech-4 | 🧱 $0-WALLED (no admissible falsifier at this scale) |
| environment-rewrite | mech-3 · mech-7 | ☠️ DEAD (mech-3 four ways; mech-7 its corpus-axis twin) |

**SUBSTRATE walls — would plausibly move at larger scale / non-templatic register / pretrained parser:**

- mech-1's learned halves (H_005 K3 values ceiling 0.82 / 0.71 vs hand 1.0; H_006 negative headroom). The
  wall is *identification-not-capacity*: the s0 drill-1.0 / f2″-0.824 gap shows a bigger module worsens it,
  so it is a property of 3.7M/byte/Korean/templatic, not of the mechanism.
- mech-2/4 (residual-rewrite): learned staging routes its verdict through exactly H_005's measured channel
  (value ceiling ≤ 0.767–0.824, live control floor ≥ 0.55 ⇒ E[Δ] ≤ ~0.22·ρ, no 2×-headroom bar
  certifiable), and hand staging degenerates into H_004's already-sealed FORMAT claim. Walled at $0,
  unreached-not-falsified (`ng.family-2-4-walled`, seed §0 of `state/h007_.../DESIGN_fable5_seed.md`).

**SATURATION/MEASUREMENT wall — the opposite failure, also not a mechanism verdict:**

- mech-5 (H_007) ⚫ RETIRED-INADMISSIBLE: the compute-matched control saturated at target scale — C-scaf
  0.8073 / 0.9531 blew the 0.60 F3 floor, C-dup hit 1.0000 / 0.9323, so F1 Δ(A-tug − C-dup) = −0.0104 /
  +0.0052 at zero headroom carries no bits about the mechanism (NOT written as K2). Root cause
  code-confirmed (`train_g2.py` `_batch`): head-A directly supervised on the gold suffix in every arm,
  ~333 epochs over 384 drill sentences, f2 holding out only pairings. The substrate was too CAPABLE for the
  panel — the exact opposite of H_005's wall. mech-5 is UNMEASURED, not falsified.
  (`state/h007_gradient_tug_role_code_drill_2026-07-17/g2_full.out`, `verdict_g2.json`.)

**STRUCTURAL closures — would NOT move at scale:**

- mech-6 ⛔: twin-redundant with mech-1 — the sealed G-2 was already N>2-shaped (K=6, rank-6 superposition;
  "N constraint fields beat their low-rank summary" IS H_004's F1 Δ 0.379 / 0.380) — and its genuine
  N>2-only residue (joint non-decomposability) has no admissible falsifier in principle here: hand-staged
  degenerates to more-gold-vs-less-gold, learned auctioneer is strictly harder than H_005's walled χ̂,
  curriculum staging is H_007's saturation wall. Three horns, all closed.
  (`state/mech6_regate_dont_open_2026-07-17/REGATE_mech6_constraint_market_fable5.md`.)
- mech-3 ☠️: falsifier vacuous (H_001: fixed codec already 0.9083–0.9167, max Δ 0.0833–0.0917 < the 0.1
  bar), objective tautological (literature gate), premise inverted (H_002: bound EASIER than free, 5.73:1
  corpus ratio), and the surviving atomicity claim isolated and nulled (H_003: Δ = −0.1146 / +0.0468, both
  < 0.05, measurement clean; `state/h003_.../verdict.json`). mech-7 inherits the strategy family.

The map's meaning: within this substrate, **the only tension family that carries thought is
structure-conflict-resolution, and it carries it in the field format, not yet in learned field production.**
Everything else is either dead on its merits, redundant with the sealed positive, or unmeasurable here —
with the unmeasurable cases explicitly labeled by which wall blocks them.

**Method lessons (reusable, as valuable as the verdicts):**

1. **Admissibility has two halves.** Reachability arithmetic (H_001: threshold ≤ ceiling − control with
   ≥2× headroom) AND the trained-control ceiling (H_007's new blocking gate G-1.5: run scaffold +
   compute-matched control alone at TARGET scale first, require control f2 ≤ 1 − 2×bar; anchors must be
   measured on THIS panel at THIS scale — H_007 froze E[C-dup]=0.62 from another experiment's band, truth
   was 1.00; a d=64 smoke inverted at d=384, +0.073 → −0.010). Now `verification.trained-control-ceiling`.
2. **Metric-ceiling defects silently inflate every arm.** H_004's K=6 codebook was GF(2) rank-4;
   teacher-forcing let any answer-LM complete the 2 parity slots, a field-blind ceiling of 0.667 reaching
   held-out. Free-slot scoring ({0,1,2,4}, codebook-derived) is mandatory and was re-derived, not
   inherited, in H_007's G-0.
3. **d_acc discipline**: bounded at 1.0, chance floor 0.5; f1/f2 are PANEL names, never F-measures; every
   number cited with its arm and source path.

## 4. Honest reopen conditions

**[b] The one genuinely non-twin new hypothesis: supervision-budget / sample-efficiency.** It varies an
axis no mechanism occupied (the answer-supervision BUDGET, not the tension content): under a scarce,
arm-identical few-shot answer budget, does objective conflict buy sample-efficiency/OOD-speed the duplicate
control does not? Gated on a **G-1.5 band-EXISTENCE pre-run** that must show, before any mechanism arm
trains: the compute-matched control stably sub-ceiling (f2 ≤ 1 − 2×bar, here ≤ 0.70) and ≥ chance + margin,
**across seeds**, at a measured few-shot plateau — priced against H_003's measured 0.161 cross-seed spread,
since the band is created by rationing and is exactly the kind of knee-tuning H_007's rescue analysis
flagged as fragile. If the band pre-run fails, [b] closes near-$0 and the campaign result stands alone.

**The scaled successor — what it takes to reach the learned-tension claim mech-1 left hand-staged.**
Recorded once, identical across every wall (`ng.family-2-4-walled`, `ng.mech6-regate-dont-open`,
REGATE_g3b): (i) a ≥8M-param and/or jamo/word-level substrate that **first passes an F1a′-analog** — the
learned values must match the hand field before any support work opens (values→support order is
load-bearing; G3-a upper-bounds G3-b); (ii) a **non-templatic register** where the G3-0d-style probe reads
< 1.0 (H_005's honest-limit (a): the templatic drill let the trunk encode the concord bit verbatim, capping
what "learned" can mean); or (iii) an **external pretrained parser** as a new campaign premise. Any
successor also inherits the standing gates: G-1.5 trained-control ceiling, recomputed free-slot codebook
audit, and the admissibility arithmetic.
