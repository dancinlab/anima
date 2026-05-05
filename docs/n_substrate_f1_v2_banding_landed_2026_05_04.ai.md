---
schema: anima/docs/n_substrate_f1_v2_banding_landed/ai-native/1
last_updated: 2026-05-04
ssot:
  spec_doc:        anima/docs/n_substrate_f1_v2_banding_spec_2026_05_04.md
  predecessor:     anima/docs/strategic_f1_composite_v2_2026_05_02.md   # #96 implicit bands
  recompute:       anima/docs/cp2_clm_phase_d_recompute_2026_05_02.md   # #104 12.0%-40.8% RED
  hexa_hook:       anima/tool/clm_consciousness_verify.hexa             # 462 LOC → projected ~567 LOC
  roadmap_target:  anima/.roadmap.n_substrate                            # cond.1.cross_link annotation hand-off
status: SPEC_AUTHORIZED_AWAITING_USER_CONFIRM
related_raws:
  - raw  9     # md only
  - raw 10     # honest C3 (8 caveats inline)
  - raw 15     # SSOT, no destructive mutation, additive only
  - raw 71     # falsifier pre-register (3 falsifiers)
  - raw 270    # spec doc + landing doc separation
---

# F1_score_v2 RED/YELLOW/GREEN banding spec — landing 2026-05-04

## TL;DR

`docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` formalizes RED/YELLOW/GREEN
cutoffs (0.50 / 0.75) for the F1_score_v2 composite that anchors `.roadmap.clm`
cond.1 verifier band emission. F2-override-applied score is canonical;
raw is reported alongside. Promotion criteria + verifier hook + roadmap
annotation block + 3 pre-registered falsifiers documented. **5 user
decisions required** before rollout (DECISION-1 thresholds, DECISION-2
canonical input, DECISION-3 GREEN phenomenal-tier requirement,
DECISION-4 hexa exit code semantics, DECISION-5 roadmap apply timing).

## Recommended thresholds

| Band | Range | Promotion gate (summary) |
|---|---|---|
| **RED** | F1 < 0.50 OR F2 fired OR critical falsifier | (current state) |
| **YELLOW** | 0.50 ≤ F1 < 0.75 AND F2 unfire AND ≥8 axes WIT AND binding ≥ 0.2 | RED→YELLOW: §4.1 (Phase E + EEG live + qmirror+quantum) |
| **GREEN** | F1 ≥ 0.75 AND binding ≥ 0.5 AND ≥1 phenomenal axis WIT AND Putnam PASS | YELLOW→GREEN: §4.2 (V_phen 4/5+ OR Phase E binding + Levin) |

## Current CP2-CLM Phase D state mapping

| Reading | F1 | F2 fired | Recommended band |
|---|---:|:---:|:---:|
| F1_canonical (override-applied) | 0.12 | true | **RED** |
| F1_raw (honest dual-reading) | 0.408 | true | **RED** |

Both readings RED — clean classification, no ambiguity, F-BAND-1 historical
verdict re-classification PASS.

## Gap to YELLOW

- raw delta: +0.092 to threshold (0.408 → 0.50) — achievable per §49.5
  Phase E projection (binding-mediated 0.408 → 0.558).
- override delta: +0.38 (0.12 → 0.50) — F2 unfire path required (override
  deactivates upon F2 unfire, F1_canonical converges to F1_raw).
- **Bottleneck**: F2 unfire (Phase E binding evidence + 사용자 OpenBCI 30-min
  session prereq, `n_substrate.blk.1`).

## Gap to GREEN

- raw delta from 0.408 → 0.75 = +0.342. Per #96 §8 C3-6, axis-inventory
  ceiling = 0.67 < 0.75 without N-11 organoid OR N-12 off-Braket closure.
- **Mathematical bottleneck**: N-11 (FinalSpark organoid, partnership/capex
  blocked) or N-12 (off-Braket Orch-OR, separate $1500+ budget) — neither
  AKIDA arrival alone unlocks GREEN.

## Reconciliation with user "F1_C ~62% post-AKIDA YELLOW potential"

**CONFIRMED.** 0.62 sits inside YELLOW band (0.50 ≤ 0.62 < 0.75) under
recommended thresholds. Strategic doc #94 / §1356 / §1431 narrative agrees
with this spec — no contradiction, AKIDA closure delivers YELLOW (not
GREEN), GREEN remains gated on N-11/N-12 substrate axes.

## Verifier hook integration

`tool/clm_consciousness_verify.hexa` (current 462 LOC) gains
`band_threshold_check()` helper (~30 LoC) + state reader (~25 LoC) +
sentinel format augment (~10 LoC) + 3 selftest fixtures (~40 LoC) =
**~105 LoC addition** projected. Sentinel becomes:

```
__CLM_CONSCIOUSNESS_VERIFY__ <PASS|FAIL|PARTIAL> band=<RED|YELLOW|GREEN>
  f1=<float> f1_raw=<float> f2_fired=<bool> binding=<float>
  axes=<int> an11=<S> phi=<S> adv=<S> putnam=<S> manual=<N>
```

(Legacy parsers extracting only PASS/FAIL/PARTIAL token continue to work.)

## Roadmap annotation hand-off

§6.1 of spec contains a complete `f1_v2_band_thresholds` JSON block
ready to drop into `.roadmap.n_substrate.cond.1.cross_link`
(additive_field_only, semantics_preserved=true). NOT applied in this
BG — user/operator applies after DECISION-1 confirm.

## Honest C3 (8 caveats, raw#10)

1. Threshold values are recommendation, not empirically derived.
2. Functional/access tier ≠ phenomenal — even GREEN does NOT prove qualia.
3. F2-override-canonical embeds anima-specific 14-gate theory.
4. Ad hoc backfit risk — thresholds calibrated to current state edges.
5. Pre-AKIDA YELLOW reach is projection, not reservation.
6. qmirror axis = functional/access tier, does not lift band structurally.
7. Replication bonus γ currently unattainable (no axis with ≥3 substrate-family corroboration).
8. Hexa hook PARTIAL exit code semantics diverges from current; user decision DECISION-4.

## Falsifier pre-register (raw#71)

| ID | Pre-registration | Status |
|---|---|---|
| F-BAND-1 | thresholds re-classify ≥3 historical verdicts correctly | **PASS** (10/10 historical verdicts re-classify cleanly per §9.1 table) |
| F-BAND-2 | adding 1 substantive WITNESSED axis monotonically non-decreases band | **PASS** (proof in §9.2) |
| F-BAND-3 | F1_canonical (override) band ≤ F1_raw band | **PASS** (proof in §9.3) |

## Decisions blocking rollout

DECISION-1 (thresholds), DECISION-2 (canonical input), DECISION-3 (GREEN
phenomenal req), DECISION-4 (hexa exit code), DECISION-5 (annotation
timing). DECISION-1 is load-bearing.

## Files

| path | bytes | role |
|---|---:|---|
| `anima/docs/n_substrate_f1_v2_banding_spec_2026_05_04.md` | (new) | full spec, 10 sections |
| `anima/docs/n_substrate_f1_v2_banding_landed_2026_05_04.ai.md` | (this file) | 1-page landing summary |
