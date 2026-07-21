---
id: H_001
slug: mech3-falsifier-vacuity
title: mech-3's pre-registered clause-(2) falsifier ("fixed-BPE substitution ΔF2 < 0.1 ⇒ DEAD") is VACUOUS — the fixed codec it ablates to already scores 0.9083–0.9167 d_acc, so the largest attainable delta is 0.0833–0.0917 < 0.1 and the DEAD verdict is fixed before the experiment exists
domain: verification-design (falsifier admissibility)
status: supported
exploration_method: closed-form arithmetic over the anima v1 MORPH-ATOM measured record
verification_method: deterministic harness + 7 pre-registered falsifiers (1 negative control, 1 bounds check)
pre_register_frozen: true
frozen_at: 2026-07-16
deterministic: true
llm: none
---

# H_001 — mech-3's falsifier is vacuous

> **SSOT**: the design tree is `ARCHITECTURE.json` — this card is evidence, not design. The verdict
> lands there at `components.mech-3.codec-war.{falsifier,l2-defense,why-bet}`, `salvage.L4.*`,
> `evidence-integrity.*` and `verification.admissibility-gate`. Human viewer: `python3 serve.py`.

## Hypothesis

`ARCHITECTURE.json` → `components` → `mech-3.codec-war` → `mech-3.falsifier` pre-registers, as
clause (2), the L2 gate that mech-3 (THE BET) must survive:

> "L2 — fixed-BPE substitution deltaF2 < 0.1 ⇒ DEAD"

and `mech-3.l2-defense` fixes the expected direction:

> "Ablation: substitute a fixed BPE for G → negation-recombination F2 must fall to ~0.617.
> If it does not fall, G is decoration."

**Claim**: this clause is not a test of mech-3. The "fixed BPE" it ablates the learned codec G
down to is *the very codec that produced anima v1's green result* (arm M, a fixed frequency-trained
jamo-BPE at K=2048). M scores d_acc 0.9083 (seed 4302) / 0.9167 (seed 7). The metric is a binary
forced-choice accuracy bounded above by 1.0. Therefore the largest delta **any** mechanism —
working, broken, or imaginary — can show over that control is `1.0 − 0.9167 = 0.0833` to
`1.0 − 0.9083 = 0.0917`, both **strictly below the 0.1 the clause requires**. The clause returns
DEAD unconditionally.

The ~0.617 the clause predicts the substitution falls to is not a fixed codec at all: it is arm
**C1 = no codec whatsoever** (raw utf-8 bytes). So the ablation as written varies *whether a codec
exists*, not *whether the codec is learned* — a two-variable swap. That confound is exactly what
makes the 0.1 threshold appear reachable on paper.

## Why

This is `verification.inherited-gates` applied to itself. That node makes an L2 ablation check
non-negotiable for every candidate "because they are the exact measurements whose absence killed
v1". H_001 asks the prior question the node does not: **is the pre-registered L2 check able to
return either answer?** A gate that can only return one answer is not a gate.

It is also `L6.measurement-is-the-grave` recurring in a form v1 never hit. v1's measurement deaths
were leaks (a lookahead leak that evaporated) and floors (a binary scramble floor at 0.50). This
one is a *ceiling*: the control is already at the panel's leak ceiling, so the panel has nothing
left to resolve above it. Same lesson, opposite end of the scale.

And it bears directly on `mech-3.why-bet`, which rests on three claims. Clause (2)'s vacuity
falsifies one of them ("L1 and L2 cannot reach it in principle" — L2 reaches it and kills it), and
the same record contradicts a second ("cheapest falsifier (existing protocol reuse)" — the protocol
needs a 303M `base.pt` that exists in neither the v1 repo nor the weights dir, plus a rented 4090
at ~2h/arm). The third claim ("standing on a lever already measured green") is true, and stronger
than the tree states — but the green belongs to a **fixed** codec, i.e. to mech-3's own null.

## Predictions

- **P1**: `max_attainable_delta(M) = 1.0 − d_acc(M) < 0.1` at **both** measured seeds.
- **P2**: the arm scoring ~0.617 carries `"codec": "raw"` — no codec — not a fixed codec.
- **P3**: `saturation(M) = d_acc(C3_leak_ceiling) − d_acc(M) ≈ 0` — the fixed codec already scores
  what the model gets when the answer is handed to it outright.
- **P4** (discrimination): the same arithmetic against the no-codec arm C1 finds 0.1 **reachable** —
  the audit condemns this one comparison, not comparisons in general.

## Variables

Inputs — all transcribed `d_acc` readings from the v1 record, each with its source path:

| arm | d_acc | codec | what it is | source |
|---|---|---|---|---|
| M_s4302 | 0.9083 | codec.json | FIXED jamo-BPE codec, K=2048, frequency-trained, label-blind | `~/anima-weights/morphatom/vM_f2.json` |
| M_s7 | 0.9167 | codec.json | same codec, seed-7 replication | `anima/state/nbind_curriculum/cement_result/vM_s7_f2.json` |
| C1_s4302 | 0.6167 | raw | **no codec** — raw utf-8 bytes | `~/anima-weights/morphatom/vC1_f2.json` |
| C1_s7 | 0.5750 | raw | **no codec**, seed-7 replication | `anima/.../cement_result/vC1_s7_f2.json` |
| C3_s4302 | 0.9167 | codec_c3.json | **leak ceiling** — 4 negator stems collapsed to ONE shared token id (answer handed over; v1's V1-liveness arm) | `~/anima-weights/morphatom/v1_f2b.json` |

- `MECH3_THRESHOLD = 0.1` — source: `ARCHITECTURE.json` `mech-3.falsifier` clause (2).
- `MECH3_PREDICTED_FALL_TO = 0.617` — source: `ARCHITECTURE.json` `mech-3.l2-defense`.
- `D_ACC_MAX = 1.0`, `D_ACC_CHANCE = 0.5` — **definitional**, not measured: `d_acc` is accuracy over
  a 2-way forced choice.

Measured outputs: `max_attainable_delta` per arm, `falsifier_reachable` per arm, `saturation` vs the
leak ceiling, `m_seed_spread`.

## Run Protocol

- **harness**: `tool/anima_v4.py` — `max_attainable_delta`, `falsifier_reachable`, `saturation`,
  `Falsifier`, `evaluate`, `D_ACC_MAX`, `D_ACC_CHANCE`
- **run script**: `state/h001_mech3_falsifier_vacuity_2026-07-16/run_h001.py`
- **deterministic**: stdlib only, no randomness, no network, $0 local
- **run cmd**: `python3 state/h001_mech3_falsifier_vacuity_2026-07-16/run_h001.py`
- **artifacts**: `state/h001_mech3_falsifier_vacuity_2026-07-16/result.json`

## Criteria

- **C1 unreachability**: `falsifier_reachable(0.1, d_acc(M)) == False` at both seeds.
- **C2 confound**: the 0.617 arm's own `codec` field reads `raw`.
- **C3 saturation**: `saturation(M, C3) < 0.1`.
- **C4 discrimination**: `falsifier_reachable(0.1, d_acc(C1)) == True`.
- **verdict_rule**: SUPPORTED = all falsifiers PASS; FALSIFIED = any trigger.

## Falsifiers (pre-registered, measurable)

- **F-001-1-threshold-attainable**: if 0.1 IS attainable against the fixed-codec control at either
  seed, the clause is a real test and the vacuity claim dies. (Measured: `max_attainable_delta`.)
- **F-001-2-control-is-actually-a-fixed-codec**: if v1's 0.617 arm was itself a fixed codec rather
  than no codec, the ablation is coherent and the confound claim dies. (Measured: the arm's `codec`
  field, verbatim from its result json.)
- **F-001-3-panel-not-saturated**: if the fixed codec sits ≥0.1 below the leak ceiling, the panel
  can still resolve a mechanism above it and the saturation claim dies. (Measured: `saturation`.)
- **F-001-4-NEGATIVE-CONTROL-audit-kills-everything**: the same arithmetic against the no-codec arm
  (~0.6) **must** find 0.1 reachable. If the audit condemns that comparison too, it is not detecting
  vacuity — it is condemning everything, and its own verdict is worthless.
- **F-001-5-m-estimate-too-noisy**: if M's two independent seeds disagree by ≥ the threshold itself,
  the control is too noisy to support any arithmetic about it and the claim dies.
- **F-001-6-BOUNDS-d-acc-out-of-range**: every transcribed `d_acc` must lie in `[chance−0.1, 1.0]`.
  A reading outside that window means the numbers are mis-transcribed and the audit is void.
- **F-001-7-predicted-fall-matches-fixed-codec**: if substituting the fixed codec really does land
  near the predicted ~0.617, the clause is self-consistent and the confound claim dies.

## Honest Limits

- **L1 — this kills a falsifier, not a mechanism.** H_001 says clause (2) cannot decide anything.
  It does **not** say a learned codec is worthless. mech-3 may be right and still be untestable by
  the gate it pre-registered. Reading this verdict as "mech-3 is dead" is exactly the eyeball
  self-judge `L6` warns about.
- **L2 — the leak-ceiling reading rests on one seed and one arm label.** `C3_s4302 = 0.9167` comes
  from `v1_f2b.json`, whose `ckpt` field reads `drill_l16000.clm` (not `drill_C3.clm`) and whose
  codec is `codec_c3.json`. The identification of that file as the C3 leak-ceiling arm is inferred
  from the codec field, not from the ckpt name. If it is a different arm, P3/F-001-3 are affected —
  **but C1/C2/C4 and the headline vacuity result do not depend on it at all.** The arithmetic in
  F-001-1 needs only M's own score and the fact that d_acc ≤ 1.
- **L3 — the numbers are transcribed, not re-measured.** The audit re-reads no checkpoints. If the
  v1 result jsons are themselves wrong, this audit inherits that. Mitigation: every arm carries its
  source path, and the four cement-arm files are git-committed in the v1 repo (the two originals and
  the C3 arm live in `~/anima-weights/`, outside version control).
- **L4 — "vacuous" is about clause (2) only.** mech-3's clause (1) (L1 boundary-decision entropy)
  and clause (3) (3 seeds) are untouched by this audit. Clause (1) in particular remains a live,
  reachable test.
- **L5 — what would move the result**: a fixed-codec control that scores materially below ~0.9 on
  this panel. If the "fixed BPE" in the clause were meant as a *non-jamo* BPE (never measured by v1),
  the arithmetic reopens — but then the ablation still varies the alphabet alongside the learning,
  so C2's confound finding stands regardless.

## Cross-Links

- **architecture**: `ARCHITECTURE.json` → `components.mech-3.codec-war.{falsifier,l2-defense,why-bet}`,
  `salvage.L4.write-side-crack`, `salvage.L6.measurement-is-the-grave`,
  `verification.inherited-gates`
- **v1 record**: `anima/state/nbind_curriculum/` — `morph2b.py` (codec + G-0 audit),
  `gen_morphatom_s1.py` (arms + panels), `morphatom_eval.py` (the d_acc scorer),
  `cement_result/` (committed seed-7 replication + C2 arm), `fire_arms.sh`, `fire_cement.sh`
- **v1 verdict**: `anima/state/verdicts/9288_morpheme_atomicity/VERDICT.md`,
  `anima/HYPOTHESES/cards/H_9288_morpheme_atomicity_lever.md`
- **sister H**: H_002 (the repaired regime — pending)
- **harness**: `tool/anima_v4.py`

## Verdict

**SUPPORTED** — 7/7 falsifiers PASS. Verbatim stdout:

```
==============================================================================
H_001 — mech-3's pre-registered falsifier is VACUOUS (closed-form audit)
==============================================================================

v1 MORPH-ATOM arms (metric = d_acc, forced-choice accuracy on panel f2, n=120):
  M_s4302   d_acc=0.9083  codec=codec.json    FIXED jamo-BPE codec (K=2048, frequency-trained, label-blind)
              src: ~/anima-weights/morphatom/vM_f2.json
  M_s7      d_acc=0.9167  codec=codec.json    FIXED jamo-BPE codec — seed-7 replication (cement)
              src: anima/state/nbind_curriculum/cement_result/vM_s7_f2.json
  C1_s4302  d_acc=0.6167  codec=raw           NO CODEC AT ALL — raw utf-8 bytes
              src: ~/anima-weights/morphatom/vC1_f2.json
  C1_s7     d_acc=0.5750  codec=raw           NO CODEC AT ALL — raw utf-8, seed-7 replication (cement)
              src: anima/state/nbind_curriculum/cement_result/vC1_s7_f2.json
  C3_s4302  d_acc=0.9167  codec=codec_c3.json  LEAK CEILING — 4 negator stems collapsed to ONE shared token id, i.e. the answer handed to the model outright (v1's V1-liveness arm)
              src: ~/anima-weights/morphatom/v1_f2b.json

mech-3 clause (2), verbatim from ARCHITECTURE.json:
  "L2 — fixed-BPE substitution deltaF2 < 0.1 ⇒ DEAD"
  "Ablation: substitute a fixed BPE for G → F2 must fall to ~0.617"

The arithmetic — against the control the clause names (the FIXED codec = arm M):
  M_s4302   max attainable delta = 1.0000 - 0.9083 = 0.0917   threshold 0.10  reachable=False
  M_s7      max attainable delta = 1.0000 - 0.9167 = 0.0833   threshold 0.10  reachable=False

NEGATIVE CONTROL — same arithmetic vs the no-codec arm (C1):
  C1_s4302  max attainable delta = 1.0000 - 0.6167 = 0.3833   threshold 0.10  reachable=True
  C1_s7     max attainable delta = 1.0000 - 0.5750 = 0.4250   threshold 0.10  reachable=True

Saturation vs the leak ceiling (C3 = answer handed over = 0.9167):
  M_s4302   leak_ceiling - arm = +0.0084
  M_s7      leak_ceiling - arm = +0.0000

Falsifier ledger:
  [PASS] F-001-1-threshold-attainable
  [PASS] F-001-2-control-is-actually-a-fixed-codec
  [PASS] F-001-3-panel-not-saturated
  [PASS] F-001-4-NEGATIVE-CONTROL-audit-kills-everything
  [PASS] F-001-5-m-estimate-too-noisy
  [PASS] F-001-6-BOUNDS-d-acc-out-of-range
  [PASS] F-001-7-predicted-fall-matches-fixed-codec

  7/7 PASS

VERDICT: SUPPORTED — mech-3's clause-(2) falsifier is VACUOUS: it returns DEAD for every possible mechanism

Reading: the clause names the FIXED BPE-jamo codec as the thing G is ablated to.
That codec IS arm M, and M scores 0.9083-0.9167. d_acc is an accuracy, so the largest
delta ANY mechanism can show over it is 0.0917 — strictly less than the 0.10 the
clause requires. The verdict DEAD is fixed before the experiment is built.
The 0.617 the clause predicts the substitution falls to is arm C1 = NO CODEC,
not a fixed codec — so the ablation as written varies the EXISTENCE of a codec,
not the LEARNING of one. That is the confound, and it is what makes the 0.1
threshold look reachable on paper.

wrote /Users/mini/dancinlab/anima-v4/state/h001_mech3_falsifier_vacuity_2026-07-16/result.json
```

Result ledger: `state/h001_mech3_falsifier_vacuity_2026-07-16/result.json`
