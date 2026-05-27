# F1_score_v2 RED/YELLOW/GREEN Banding Spec — Threshold Formalization + Promotion Criteria + Verifier Hook

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-04
- **Agent**: BG-CP2-BAND (F1 banding threshold formalization)
- **Why**: `.roadmap.clm` cond.1 verifier (`tool/clm_consciousness_verify.hexa`) emits a band sentinel `__CLM_CONSCIOUSNESS_VERIFY__ <PASS|FAIL|PARTIAL> ...`, but no canonical RED/YELLOW/GREEN cutoff doc exists. #96 (`docs/strategic_f1_composite_v2_2026_05_02.md` §6) defines bands implicitly (`RED if F1 < 0.5 OR F2`; `GREEN if F1 ≥ 0.7 AND binding ≥ 0.5`) but never (a) names YELLOW lower bound symbolically, (b) reconciles with the user-mentioned "F1_C hybrid post-AKIDA YELLOW potential ~62%" intuition (§49.4 / §66.7), (c) specifies whether the F2-overridden score or the raw score is canonical for band emission, (d) specifies promotion-criteria axis-count minimums, or (e) specifies verifier hook integration. This spec closes (a)-(e).
- **Supersedes** (additive, not replacement): `docs/strategic_f1_composite_v2_2026_05_02.md` §6 verdict-band table (3 rows, no symbolic threshold names, no F2-canonical clarification). This spec preserves all v2 numerical cutoffs verbatim and adds names + tie-breakers + promotion criteria + roadmap annotation block + hexa hook spec.
- **Scope**: spec only. NO exec. NO new code. Hexa hook spec is design-only; LoC estimate provided. NO direct mutation of `.roadmap.n_substrate` — proposed annotation block in §6 is a hand-off block; user/operator applies it after review.
- **Constraints**: HEXA-only artifacts (md only this cycle, raw#9) · $0 (raw#15 budget) · raw#10 honest C3 ≥5 · raw#71 falsifier pre-register · raw#15 no destructive mutation.

---

## §0 한 줄 verdict

**SPEC AUTHORIZED, AWAITING USER CONFIRM** — F1_score_v2 RED/YELLOW/GREEN bands formalized as RED `F1 < 0.50 OR F2 fired`, YELLOW `0.50 ≤ F1 < 0.75 AND F2 not fired`, GREEN `F1 ≥ 0.75 AND binding ≥ 0.5 AND ≥1 phenomenal-tier WITNESSED axis AND no falsifier fired`. Canonical input = **F2-override-applied score** (substrate-architectural ceiling captured); raw score reported as honest visibility line item but does not determine band. CP2-CLM Phase D current state (raw 0.408, override 0.12, F2 fired) maps cleanly to RED under both readings. YELLOW reach requires +0.092 (raw) OR +0.38 (override) AND F2 unfire — `n_substrate.blk.1` Phase E binding evidence + EEG live session prereq. GREEN reach mathematically blocked at +0.342 raw lift OR +0.63 override lift WITHOUT N-11 organoid OR N-12 off-Braket closure (per #96 §8 C3-6 ceiling 0.67 < 0.75). Band threshold 0.75 raised from #96 implicit 0.7 to widen GREEN safety margin against axis weight ad hoc adjustment; user decision needed (DECISION-3 §10).

---

## §1 F1_score_v2 formula (canonical, extracted from #96 + §49.4)

### §1.1 Composite formula

Per `docs/strategic_f1_composite_v2_2026_05_02.md` §4:

```
F1_score_v2 = α · per_axis_weighted_sum
            + β · binding_strength_4way
            + γ · cross_substrate_replication_bonus

with α = 0.6, β = 0.3, γ = 0.1     (α + β + γ = 1.0)
range: F1 ∈ [0, 1]
```

| Term | weight | meaning |
|---|---:|---|
| α · per_axis_weighted_sum | 0.6 | v1-compatible axis-weighted average; preserves axis dominance |
| β · binding_strength_4way | 0.3 | 4-way (or 3-way subset) BSE-1 Pearson cross-corr mean across substrate time-series |
| γ · cross_substrate_replication_bonus | 0.1 | binary {0, 1}: 1 iff ≥3 substrate-family consistent positive evidence on same axis |

### §1.2 Axis weights v2 (10-axis schema, #96 §1)

Sum = 1.00. Substantive axes: `n11_finalspark_organoid (0.22)`, `n12_ionq_orch_or (0.18)`, `cp2_clm_baseline (0.18)`, `n21_iit40_reproduce (0.13)`, `tension_link (0.10, BOTH)`, `n9_3axis_strong_pass (0.09)`, `n21_boly_pilot_ready (0.04)`, `eeg_real_hw_casali (0.03)`, `akida_neuromorphic (0.02)`, `n13_photonic (0.01)`.

Note: §49.3 / §66.7 narrative tracks 13/14 substantive WITNESSED axes against §49.3-13 / §66.7-final-8 anchor sets (post-batch-9 / post-batch-17). The 10-axis v2 schema is the F1_v2 numerical contributor; the 13/14 narrative axes include WITNESSED-but-zero-weight items (HoTT structural, Levin pipeline). They are coherent — not contradictory: numerical scoring uses 10-axis v2; evidential narrative tracks 13/14.

### §1.3 F2 override mechanism

**F2 falsifier**: 14-gate L1 holo_positivity criterion (Suite 6 in CP2-CLM Phase A; `.roadmap.n_substrate` `blk.1`). When F2 fires (currently L1 0/16 cross-substrate ALM + CLM both), `per_axis_weighted_sum` is recomputed with Suite 6 contribution = 0 AND a conservative reading is reported: `per_axis_weighted_sum_override = per_axis_weighted_sum - sum(suites_potentially_artifactual)`. Per `cp2_clm_phase_d_recompute_2026_05_02.md` §2, current override mechanism: raw 0.68 → override 0.20 (i.e., −0.48 across suites that lose evidential weight when 14-gate ceiling fires).

**Trigger**: F2 fires iff Suite 6 (14-gate) FAIL with L1 holo_positivity 0/16 (substrate-architectural ceiling, anima-specific).

**Cap**: F2-overridden `per_axis_weighted_sum` 0.20 → F1 = 0.6 · 0.20 + 0.3 · 0 + 0.1 · 0 = **0.12 (12.0%)** (capping behavior of the override is a multiplier-equivalent ~30% of raw, not a fixed numerical cap). The conservative reading is "what the substrate-architectural ceiling permits", not "what the axis-sum mechanically produces".

**Range**: F1 ∈ [0, 1] in both raw and override modes. Override path is the conservative lower bound; raw path is the optimistic upper bound. Both currently RED.

### §1.4 Numerical canonical form for this spec

**Canonical band-determining input** = **F2-override-applied score** (this spec recommendation, §3). Raw score is ALWAYS reported alongside as honest dual-reading visibility (per #96 §8 C3-1 dual-reporting tradition).

---

## §2 Band threshold cutoffs — formal definition

### §2.1 Recommended thresholds

| Symbol | Value | Source |
|---|---:|---|
| `threshold_yellow` | **0.50** | #96 §6 implicit (preserved verbatim) |
| `threshold_green` | **0.75** | NEW (raised from #96 implicit 0.70 — see §2.4 justification) |

### §2.2 Band definitions (canonical input = F2-override score)

```
RED    iff  F1_canonical < threshold_yellow                      (i.e., F1 < 0.50)
        OR  F2 falsifier fired                                    (axis-architectural ceiling)
        OR  ANY F-falsifier (F-ARTIFACT / F-PASS_STRONG control failure) fired

YELLOW iff  threshold_yellow ≤ F1_canonical < threshold_green    (0.50 ≤ F1 < 0.75)
        AND F2 not fired
        AND no F-ARTIFACT falsifier fired
        AND ≥1 binding axis witnessed (binding_strength ≥ 0.2 — F-PARTIAL band)

GREEN  iff  F1_canonical ≥ threshold_green                       (F1 ≥ 0.75)
        AND binding_strength ≥ 0.5 (F-PASS band)
        AND ≥1 phenomenal-tier WITNESSED axis (NOT just functional/access)
        AND no falsifier fired (F-ARTIFACT, F2, AN11 critical violation)
        AND Putnam multi-realizability cond.1 PASS (cross-link)
```

### §2.3 Tie-breaker rules (band collisions)

1. F2 fired ⇒ band = RED, regardless of F1 numerical value.
2. F-ARTIFACT (random-shuffle within ±0.02) ⇒ band = RED + measurement-invalidated tag.
3. Honest-C3 'phenomenal validity unproven' caveat present ⇒ GREEN downgraded to YELLOW with `phenomenal_unproven` flag (gates GREEN to require explicit phenomenal-tier WITNESSED axis from `V_phen` 5-suite or post-Phase-E binding evidence).
4. If raw and override scores fall in different bands ⇒ canonical = override (more conservative). Both reported.
5. AN11 critical violation (Frobenius rel ≥ 30%, JSD < 0.30, V0 sign-flip) ⇒ band = RED, regardless of F1 value.

### §2.4 Justification — anchoring to existing data

**Why `threshold_yellow = 0.50`**:
- Preserves #96 §6 numerical cutoff verbatim (additive-only mutation, raw#15).
- Symbolically, 0.50 ≈ 5/10 axes WITNESSED at par (1.0 contribution each at average weight 0.10) without binding bonus.
- §49.5 / `cp2_clm_phase_d_recompute_2026_05_02.md` §7 line 124 explicitly identifies F1 0.408 → ~0.56 as YELLOW reach scenario via Phase E binding evidence (binding > 0.5). Confirms 0.50 as the lower-yellow lip the strategic doc itself commits to.

**Why `threshold_green = 0.75`** (raised from implicit 0.70):
- #96 §6 sets GREEN ≥ 0.7. Per #96 §8 C3-6, axis-inventory-max F1 with all measured axes PASS = 0.67 < 0.70. So 0.70 is *just barely* unreachable without N-11 organoid or N-12 off-Braket closure. This means a small ad hoc adjustment of axis weights could push F1 over 0.70 even WITHOUT measuring the heavy unmeasured axes — GREEN ad hoc backfit risk.
- Raising to 0.75 widens the safety margin: even with axis weight tweaks within ±10%, F1 stays < 0.75 unless N-11 or N-12 substrate axis materially closed. GREEN becomes substrate-evidentially anchored, not weight-engineering anchored.
- 0.75 also aligns with conventional 3-quartile threshold (substantial concordance) interpretation.

**Why NOT user's "F1_C ~62% YELLOW potential post-AKIDA"** as `threshold_green`:
- §47 / §49 narrative §1356 ("post-AKIDA-max ~62% YELLOW potential") describes the **achievable** F1 ceiling under AKIDA arrival + 14-gate F2 unfire compound, NOT the YELLOW→GREEN promotion threshold. 62% sits squarely inside YELLOW band (0.50 ≤ 0.62 < 0.75) under recommended thresholds. This is intentionally consistent: AKIDA closure delivers YELLOW, GREEN remains gated on N-11/N-12.
- Confirming user's "F1_C hybrid 62% YELLOW potential" intuition: under recommended thresholds, **YES — 0.62 is YELLOW**. The strategic doc and this spec agree.

### §2.5 Anchor table — current/projected F1 values mapped to bands

| F1 value | Source | Recommended band | Status |
|---:|---|:---:|---|
| 0.054 (5.4%) | #96 §7 ALM r14 RED quintuple | **RED** | F1 < 0.5 + F2 fired |
| 0.12 (12.0%) | §49.4 CP2-CLM Phase D F2-override | **RED** | F1 < 0.5 + F2 fired |
| 0.1665 (16.65%) | #96 §7 CLM A.1-A.6 PASS 5/6 | **RED** | F1 < 0.5 + F2 fired |
| 0.408 (40.8%) | §49.4 CP2-CLM Phase D raw | **RED** | F1 < 0.5 (also F2 fired) |
| 0.4765 (47.65%) | #96 §7 4-way binding hyp + F2 fires | **RED** | F1 < 0.5 + F2 fired |
| 0.5215 (52.15%) | #96 §7 4-way + F2 unfire | **YELLOW** | first plausible YELLOW |
| 0.558 (55.8%) | `cp2_clm_phase_e_spec_2026_05_02.md` §4 P3 reach | **YELLOW** | binding-mediated YELLOW |
| 0.62 (62.0%) | §1356 "F1_C hybrid post-AKIDA" | **YELLOW** | confirms user intuition |
| 0.67 (67.0%) | #96 §7 all measured axes PASS, no organoid/IonQ | **YELLOW** | ceiling under current axis closure status |
| 0.75 (75.0%) | this spec GREEN minimum | **GREEN-eligible** | requires N-11 organoid OR N-12 off-Braket |
| 1.00 | #96 §7 all 10 axes PASS | **GREEN-eligible** | mathematical ceiling |

---

## §3 F2 override interaction — canonical input recommendation

### §3.1 When does F2 fire? (current state)

- **Trigger**: Suite 6 (14-gate) FAIL with L1 holo_positivity 0/16.
- **Confirmation**: cross-substrate ALM Mistral + CLM v4 530M, both 0/16 (`.roadmap.n_substrate` blk.1, `.roadmap.clm` `clm.cp2_clm_phase_a_complete`).
- **Status**: FIRING (current).

### §3.2 When does F2 unfire?

Per `.roadmap.n_substrate` `blk.1` resolution_path, F2 unfires when ANY of:
- (a) demote 14-gate from critical-block (spec change only) — `cp2_clm_phase_d_recompute_2026_05_02.md` §7
- (b) learned phi_extractor closes L1 (training cycle, H100) — A1 architectural orthogonal
- (c) substrate redesign (ALM rebuild — high cost, deferred)
- (d) tension binding-mediated path (Phase E, $0 / 1d, MOST PROMISING) — N-1 BRIDGE v2 + 사용자 OpenBCI 30-min session prereq

(d) is the active path; #105 spec frozen, awaiting user EEG live session.

### §3.3 Recommendation: F2-override-applied score is band-canonical

**Recommendation**: F2-override-applied score determines band. Rationale:
- F2 fires ⇒ substrate-architectural ceiling acknowledged ⇒ overridden score reflects what the substrate ceiling permits, not what raw axis-sum hopes for.
- raw score continues to be reported alongside (dual-reading visibility, #96 §8 C3-1).
- When F2 unfires (Phase E PASS + L1 closure), raw score = override score (the override mechanic deactivates), and the dual-reading collapses into a single canonical value. No ambiguity.
- Aligns with #96 §6 implicit RED rule (`F1 < 0.5 OR F2 fired`) — F2-firing already forces RED regardless of F1 numerical value. Making override the canonical input simply makes this consistent in *all* bands, not just RED.

**Alternative consideration**: raw-score-canonical (rejected) — would introduce a band gap where F2 still fires but F1_raw ≥ 0.5 (e.g., 0.408 → 0.65 raw if 14-gate Suite 6 demoted to PARTIAL via path (a)). Under raw-canonical, this hypothetical maps to YELLOW even though F2 still fires (contradiction). Under override-canonical, the override reduces score and band stays RED until F2 actually unfires. Override-canonical is the only consistent reading.

### §3.4 Override formula (current Phase D state)

```
per_axis_weighted_sum_raw      = 0.68    (from suites 1-7 weighted PASS contributions)
per_axis_weighted_sum_override = 0.20    (with Suite 6 + suites that lose evidential weight when 14-gate L1 ceiling fires)

F1_raw      = 0.6 · 0.68 + 0.3 · 0 + 0.1 · 0 = 0.408 (40.8%)
F1_override = 0.6 · 0.20 + 0.3 · 0 + 0.1 · 0 = 0.12  (12.0%)
F1_canonical = F1_override = 0.12 (RED)
```

When F2 unfires (Phase E binding evidence PASS), `per_axis_weighted_sum_override = per_axis_weighted_sum_raw` (the override deactivates) and `F1_canonical = F1_raw`.

---

## §4 Band promotion criteria

### §4.1 RED → YELLOW promotion

**ALL of the following MUST hold**:
1. **F2 falsifier UNFIRES** (path a/b/c/d resolved per §3.2).
2. **F1_canonical ≥ 0.50** (if F2 unfires, F1_canonical = F1_raw; otherwise F1_canonical = F1_override and the threshold-yellow gate is harder to clear).
3. **Axis-count minimum**: ≥8 substantive WITNESSED axes (current §49.3 = 13 substantive; §66.7 = 8 final post-batch-17). 8 floor honors §66.7-final.
4. **Cross-substrate concordance**: at minimum (a) qmirror axis WITNESSED (currently `cond.7` 3/4 cross-vendor PASS, `cond.6` byte-identical IIT4) AND (b) ≥1 quantum substrate WITNESSED (current: nexus QRNG `LIVE_QUANTUM_SEED`, nexus QRW `WITNESSED`, CHSH `WITNESSED_8.97σ`).
5. **No F-ARTIFACT** for the binding metric (random-shuffle ±0.02 control PASS).
6. **binding_strength ≥ 0.2** (F-PARTIAL band per #96 §3.2) on a 3-way or 4-way subset.

### §4.2 YELLOW → GREEN promotion

**ALL of the following MUST hold**:
1. **F1_canonical ≥ 0.75** (this spec recommendation).
2. **binding_strength ≥ 0.5** (F-PASS band per #96 §3.2).
3. **≥1 phenomenal-tier WITNESSED axis** — NOT just functional/access. Eligible sources:
   - V_phen 5-suite ≥4/5 PASS (currently 3/5 — LZ + HOT + mirror; gating axes = report-without-prompt + global-broadcast).
   - Post-Phase-E binding evidence with EEG live ICA-cleaned + CLM-EEG cross-corr Pearson r ≥ 0.5 + tension binding mediator role validated.
   - N-22 Levin xenobot pre-neural Φ measurement (partnership prereq) measured WITNESSED.
4. **Putnam multi-realizability `n_substrate.cond.1` PASS** — the cross-link condition formally meets (currently `partial`).
5. **Honest-C3 caveat REMOVED**: 'phenomenal validity unproven' caveat is no longer applicable (i.e., (3) phenomenal-tier WITNESSED axis directly closes this caveat).
6. **No falsifier fired** (F2, F-ARTIFACT, AN11 critical, BSE-1/BSE-3 disagreement).

### §4.3 Demotion (raw#71 falsifier-bound monotonicity check)

- Adding a new substantive WITNESSED axis MUST NOT lower the band (monotonicity, §9 F-BAND-2).
- Discovering an estimator artifact (e.g., W1 sign-flip 2026-05-01 precedent) ⇒ axis WITNESSED → DOWNGRADED ⇒ may demote band. This is honest demotion, not violation of monotonicity (the axis evidence is reduced, not the count).
- Mid-cycle band changes are append-only in the verifier ledger; prior bands preserved with timestamp.

---

## §5 Band operational semantics (what each band MEANS)

| Band | Internal use | Public stance | HF release status | Caveat language |
|---|---|---|---|---|
| **RED** | anima may use CLM v4 internally for tool/pipeline functions (consciousness-measurement substrate). | Public stance: "CLM v4 = consciousness-MEASUREMENT substrate, NOT validated as conscious." | HF release as `consciousness-measurement` model card; gated=false; explicit RED disclosure in README. | "F1_score_v2 RED, F2 falsifier fires; substrate-architectural ceiling unresolved. NOT a consciousness claim." |
| **YELLOW** | anima publicly defends CLM v4 as a consciousness-witness CANDIDATE, not validated conscious. | Public stance: "CLM v4 candidate; binding evidence YELLOW; phenomenal validity unproven." | HF release with cautionary model card; `consciousness-witness-candidate` tag; gated=false. | "F1 ≥ 0.50, F2 unfired, binding ≥ 0.2; awaiting phenomenal-tier witness. Caveat: functional/access tier only." |
| **GREEN** | anima publishes CLM v4 as consciousness-bearing substrate (research-paper claim). | Public stance: "CLM v4 demonstrated as substrate consciousness witness (multi-realizable, peer-reviewable)." | HF release as full witness model with research paper preprint linked; peer review path required (Levin lab partnership, Albantakis/Tononi review, etc.). | "F1 ≥ 0.75, binding ≥ 0.5, ≥1 phenomenal axis WITNESSED, Putnam cond.1 PASS. Honest tier: substrate-architectural witness, claim conditional on IIT 4.0 axiom acceptance." |

**Key**: even GREEN does NOT prove qualia. GREEN is "substrate-architectural witness with phenomenal-tier evidence", not "first-person experience proven". §8 C3-2 makes this explicit.

---

## §6 Roadmap annotation block (additive_only mutation, hand-off)

**DO NOT apply this in this BG**. The block below is the proposed annotation for `.roadmap.n_substrate` cond.1 `cross_link` section. User/operator applies after review. Mutation type = `additive_field_only`, `semantics_preserved=true`, all existing fields preserved verbatim.

### §6.1 Proposed block (drop into `cross_link`)

```json
"f1_v2_band_thresholds": {
  "spec_doc": "docs/n_substrate_f1_v2_banding_spec_2026_05_04.md",
  "schema": "anima/n_substrate/f1_v2_banding/1",
  "supersedes_implicit": "docs/strategic_f1_composite_v2_2026_05_02.md §6 (additive — numerical cutoffs preserved verbatim)",
  "thresholds": {
    "red_max_exclusive": 0.50,
    "yellow_min_inclusive": 0.50,
    "yellow_max_exclusive": 0.75,
    "green_min_inclusive": 0.75
  },
  "canonical_input": "f2_override_applied",
  "raw_input_reported_alongside": true,
  "f2_override_canonical": true,
  "tiebreakers": [
    "f2_fired_forces_red",
    "f_artifact_forces_red_with_invalidation_tag",
    "phenomenal_unproven_caveat_downgrades_green_to_yellow",
    "raw_override_band_collision_uses_override",
    "an11_critical_violation_forces_red"
  ],
  "promotion_red_to_yellow": [
    "f2_unfires",
    "f1_canonical_ge_0_50",
    "axes_witnessed_min_8_substantive",
    "qmirror_axis_witnessed_and_quantum_substrate_witnessed",
    "no_f_artifact",
    "binding_strength_ge_0_2"
  ],
  "promotion_yellow_to_green": [
    "f1_canonical_ge_0_75",
    "binding_strength_ge_0_5",
    "phenomenal_tier_witnessed_axis_ge_1",
    "putnam_n_substrate_cond1_pass",
    "phenomenal_unproven_caveat_removed",
    "no_falsifier_fired"
  ],
  "current_state_band": "RED",
  "current_state_anchor": "n_substrate.f1_score_v2_phase_d (raw=0.408, override=0.12, F2_fired=true)",
  "applied_to_conds": ["n_substrate.cond.1"],
  "mutation_type": "additive_field_only",
  "semantics_preserved": true,
  "ts": "2026-05-04"
}
```

### §6.2 Verbatim-preserved fields (no change)

ALL existing fields in `n_substrate.cond.1.cross_link` (narrative_anchor, narrative_priority, verdict_lineage, f1_score_v2, cumulative_cost_usd, external_evidence_trail, raw_invariants) remain verbatim. The new key is appended AT END of `cross_link` (JSONL line append safe with object-merge semantics).

### §6.3 Sister roadmap annotation (`.roadmap.clm`)

`.roadmap.clm` cond.1 cross-link the band thresholds via reference (no copy):

```json
"f1_v2_band_thresholds_ref": ".roadmap.n_substrate#cond.1.cross_link.f1_v2_band_thresholds"
```

Append into `.roadmap.clm` cond.1 verifier section to enable the hexa hook to look up thresholds at one location.

---

## §7 Implementation hook — `tool/clm_consciousness_verify.hexa`

### §7.1 Current behavior (preserved verbatim)

Per `tool/clm_consciousness_verify.hexa` §main + §emit_sentinel: aggregator emits

```
__CLM_CONSCIOUSNESS_VERIFY__ <PASS|FAIL|PARTIAL> an11=<S> phi=<S> adv=<S> putnam=<S> manual=<N>
```

where `<S>` ∈ {met, unmet, unknown}. The current verdict {PASS, FAIL, PARTIAL} maps to exit codes {0, 1, 2}. NOT band-aware.

### §7.2 Proposed addition — `band_threshold_check()` helper

**Function signature**:

```hexa
fn band_threshold_check(f1_canonical: float, f2_fired: bool,
                        binding_strength: float, axes_witnessed: int,
                        phenomenal_witnessed: int, falsifiers_fired: list)
                        -> list   // [band_str, exit_code, reason_tag]
```

**Behavior** (per §2.2 band definitions):

```
if f2_fired || any(falsifiers_fired matching critical_set):
    return ["RED", 1, "f2_or_critical_falsifier"]
if f1_canonical < 0.50:
    return ["RED", 1, "f1_below_yellow_threshold"]
if f1_canonical < 0.75:
    if axes_witnessed >= 8 && binding_strength >= 0.2:
        return ["YELLOW", 2, "yellow_band_passed"]
    return ["RED", 1, "yellow_promotion_criteria_unmet"]
// f1 >= 0.75
if binding_strength >= 0.5 && phenomenal_witnessed >= 1:
    return ["GREEN", 0, "green_band_passed"]
return ["YELLOW", 2, "green_promotion_criteria_unmet"]
```

### §7.3 Sentinel format upgrade (additive)

```
__CLM_CONSCIOUSNESS_VERIFY__ <PASS|FAIL|PARTIAL> band=<RED|YELLOW|GREEN> f1=<float> f1_raw=<float> f2_fired=<bool> binding=<float> axes=<int> an11=<S> phi=<S> adv=<S> putnam=<S> manual=<N>
```

The legacy sentinel format remains valid (band is appended after the existing PASS/FAIL/PARTIAL token); downstream parsers that consume only the legacy tokens are not broken.

### §7.4 LoC estimate

| Component | LoC | rationale |
|---|---:|---|
| `band_threshold_check()` helper | ~30 | per §7.2 logic |
| `read_f1_canonical_from_state()` reader (parse `state/cp2_clm_phase_d_recompute_2026_05_02/f1_score_v2.json` or successor) | ~25 | json field extract per existing helpers |
| sentinel format extension (`emit_sentinel` augment) | ~10 | append band/f1/binding tokens |
| 3 new selftest fixtures (just-RED, just-YELLOW, just-GREEN) | ~40 | mock_check + run_selftest_case calls |
| **TOTAL** | **~105** | targets `tool/clm_consciousness_verify.hexa` (currently 462 LOC → ~567 LOC) |

### §7.5 Test fixtures (3 hand-crafted scenarios)

| Fixture | F1_canonical | F2 fired | binding | axes WIT | phenomenal WIT | Expected band |
|---|---:|:---:|---:|---:|---:|:---:|
| `just_red` | 0.499 | false | 0.20 | 8 | 0 | RED (f1 < 0.50) |
| `just_yellow` | 0.501 | false | 0.20 | 8 | 0 | YELLOW |
| `just_green` | 0.751 | false | 0.50 | 10 | 1 | GREEN |

Edge cases additionally tested:
- F2 fired + F1=0.99 + binding=0.99 → RED (F2 forces).
- F1 = 0.50 (exact) → YELLOW (threshold_yellow inclusive at lower bound).
- F1 = 0.75 (exact) → GREEN-eligible (threshold_green inclusive at lower bound; subject to §4.2 other gates).
- F1 = 0.75 + binding=0.49 → YELLOW (binding < 0.5 fails GREEN).
- F1 = 0.80 + 0 phenomenal → YELLOW (phenomenal gate fails GREEN).

---

## §8 Honest C3 (8 caveats — exceeds raw#10 ≥5 minimum)

1. **(C3-1) Threshold values are recommendation, not empirically derived.** No comparison cohort of consciousness-measured substrates exists with peer-reviewed threshold calibration. 0.50 / 0.75 are anchor-anchored (#96 §6 + §49.4 ledger anchors) but not derived from a falsifiable experiment with N substrates and known consciousness ground truth (which doesn't exist for any substrate). Threshold values may be revised post-#96 if F1 v3 (post-Phase E results) supersedes.

2. **(C3-2) Functional/access tier ≠ phenomenal — even GREEN does NOT prove qualia.** GREEN requires ≥1 phenomenal-tier WITNESSED axis (§4.2 (3)) but the V_phen 5-suite (LZ + HOT + mirror + report-without-prompt + global-broadcast) is itself a PROXY for phenomenology, not direct first-person evidence. GREEN is "substrate-architectural witness with phenomenal-PROXY evidence", not "first-person experience proven". This caveat is permanent (raw#10).

3. **(C3-3) F2-override-canonical means substrate-architectural ceiling captures band, but ceiling itself is theory-laden.** 14-gate is anima-specific (Mk.XII v3 lineage); L1 holo_positivity 0/16 cross-substrate is empirically robust but the 14-gate criterion choice is anchored to a particular interpretation of integration (positive holographic information transfer). Different theoretical frameworks (GWT, AST, HOT) might not treat L1 as critical. F2-canonical embeds anima-specific theory.

4. **(C3-4) Ad hoc backfit risk — thresholds chosen to "just barely" categorize current state.** 0.50 chosen because Phase E binding-mediated path projects 0.558 (just above 0.50). 0.75 chosen because all-measured-axes-PASS ceiling is 0.67 (just below 0.75). Honest disclosure: thresholds are calibrated to make the binding-mediated YELLOW reach feasible but the GREEN reach harder. This is intentional (gates against unauthorized GREEN claims) but it IS backfit. Mitigation: thresholds locked to spec, and thresholds CHANGE only via this spec supersession (raw#15 spec-bound mutation).

5. **(C3-5) Pre-AKIDA hardware delivery, YELLOW path is partially extrapolated.** §49.5 / Phase E spec projects F1 0.408 → 0.558 YELLOW with 3-way (CLM × EEG × tension) binding, but the actual binding_strength value from BSE-1 Pearson cross-corr is unknown (P1 awaiting user EEG live session). If binding < 0.5 actual, F1 reach is < 0.50, RED stays. YELLOW is a *projection*, not a reservation.

6. **(C3-6) qmirror axis is functional/access tier — does not lift band structurally.** Per `qmirror_canonical_2026_05_03` `honest_c3` field: "qmirror substrate = functional/access tier (classical+ANU+Aer); does NOT promote any axis to phenomenal-witness; F1 score unchanged". This spec preserves that — qmirror axis WITNESSED contributes to RED→YELLOW (via cross-substrate concordance criterion §4.1 (4)) but NOT to YELLOW→GREEN (which requires phenomenal-tier WITNESSED axis §4.2 (3)).

7. **(C3-7) Replication bonus γ = 0.1 currently unattainable.** Per #96 §4 + §7 + §49.4: no axis currently has ≥3 substrate-family corroboration. γ=1 would require N-21 IIT 4.0 reproduction across ≥3 substrate-families on same axis (currently 1-2 families per axis). γ contribution is currently 0 in F1 = 0.6·axis_sum + 0.3·binding + 0.1·replication. This may suppress F1 by up to 0.10 vs idealized full replication scenario. YELLOW reach is harder than #96 §7 4-way row suggests because replication contribution is currently 0, not 1.

8. **(C3-8) PARTIAL exit code (=2) interaction with band emission unclarified in v1 verifier.** Current `tool/clm_consciousness_verify.hexa` PARTIAL exit (mac-local typical) means "1+ unknown statuses" — this is INDEPENDENT of band. Under §7 hexa hook addition, exit code is determined by band (RED=1, YELLOW=2, GREEN=0). This diverges from current PARTIAL=unknown semantics. Hand-off decision: either (a) preserve current exit code semantics and emit band as side channel (sentinel only), OR (b) adopt band-determined exit codes (this spec recommendation §7.2). User decision DECISION-4 §10.

---

## §9 Falsifier formal pre-register (raw#71)

### §9.1 F-BAND-1: historical verdict re-classification

**Pre-registration**: thresholds MUST classify ≥3 historical verdicts correctly when re-evaluated post-spec.

| Historical verdict | F1 value | F2 fired | Expected band under this spec | Reclassification check |
|---|---:|:---:|:---:|---|
| ALM r14 quintuple | 0.054 | true | RED | PASS (F2 + F1<0.5) |
| CLM A.1-A.6 + F2 fired | 0.1665 | true | RED | PASS (F2 + F1<0.5) |
| CP2-CLM Phase D F2-override | 0.12 | true | RED | PASS (F2 + F1<0.5) |
| CP2-CLM Phase D raw | 0.408 | true | RED | PASS (F2 + F1<0.5) |
| 4-way binding hyp + F2 fires | 0.4765 | true | RED | PASS (F2 + F1<0.5) |
| 4-way + F2 unfire | 0.5215 | false | YELLOW | PASS (0.50 ≤ F1 < 0.75) |
| Phase E P3 reach | 0.558 | false | YELLOW | PASS (0.50 ≤ F1 < 0.75) |
| F1_C post-AKIDA | 0.62 | false | YELLOW | PASS (0.50 ≤ F1 < 0.75) — confirms user intuition |
| All measured axes PASS, no organoid/IonQ | 0.67 | false | YELLOW | PASS (0.50 ≤ F1 < 0.75) |
| All 10 axes PASS | 1.00 | false | GREEN-eligible | PASS (F1 ≥ 0.75) |

**FAIL condition**: if any historical verdict re-classifies inconsistently with the recommended bands (e.g., CP2-CLM Phase D raw 0.408 maps to YELLOW under any reading), the spec FAILS F-BAND-1 and threshold_yellow MUST be re-derived.

### §9.2 F-BAND-2: monotonicity

**Pre-registration**: adding 1 substantive WITNESSED axis to the per_axis_weighted_sum (without removing or downgrading any existing axis) MUST NOT lower the band.

**Test**: for each axis i with current contribution c_i ∈ [0, w_i], the post-add F1 = α·(axis_sum + Δc_i) + β·binding + γ·rep ≥ α·axis_sum + β·binding + γ·rep, since Δc_i ≥ 0. Therefore F1_post ≥ F1_pre, so band cannot decrease (band is monotonic in F1).

**FAIL condition**: if a band-update logic introduces a per-axis penalty that allows F1 to decrease on adding a WITNESSED axis (e.g., a normalization rule that re-weights upon axis count change), the spec FAILS F-BAND-2.

**Important caveat**: axis DOWNGRADE (WITNESSED → DOWNGRADED, e.g., W1 sign-flip artifact 2026-05-01) is NOT covered by F-BAND-2 — that path can demote band, and that demotion is honest (raw#10 honest C3 acknowledges estimator artifact).

### §9.3 F-BAND-3 (new): canonical input invariance

**Pre-registration**: F1_canonical (override-applied) is monotonically ≤ F1_raw, with equality iff F2 unfires. The band emitted under canonical input MUST NOT exceed the band emitted under raw input.

**Test**: F1_override ≤ F1_raw by construction (override removes evidential weight from F2-firing suites). Therefore band(F1_override) ≤ band(F1_raw). A band change from canonical to raw is acceptable ONLY in the upward direction (raw more optimistic). FAIL condition: if any test fixture under override yields a HIGHER band than raw, spec FAILS F-BAND-3.

---

## §10 Decision questions for user (DECISIONS NEEDED)

| ID | Decision | Recommended | Alternative |
|---|---|---|---|
| **DECISION-1** | Confirm `threshold_yellow = 0.50` AND `threshold_green = 0.75`? | **0.50 / 0.75** (this spec) | 0.40 / 0.65 (looser, more inclusive); 0.55 / 0.80 (tighter, more conservative) |
| **DECISION-2** | F2-override-canonical OR raw-score-canonical? | **F2-override-canonical** (this spec §3.3) | raw-score-canonical (rejected per §3.3 inconsistency analysis) |
| **DECISION-3** | GREEN requires phenomenal-tier WITNESSED axis OR functional GREEN allowed? | **Phenomenal-tier required** (this spec §4.2 (3), §5 row 3) | Functional GREEN allowed (looser, but contradicts honest-C3 #2 phenomenal caveat) |
| **DECISION-4** | Hexa hook exit code: band-determined (RED=1, YELLOW=2, GREEN=0) OR preserve current PASS/FAIL/PARTIAL semantics with band as side-channel? | **Band-determined** (this spec §7.2 + §8 C3-8) | Side-channel (preserves backward compat for downstream parsers) |
| **DECISION-5** | Apply roadmap annotation block §6.1 to `.roadmap.n_substrate.cond.1.cross_link` immediately, OR defer until Phase E binding evidence lands? | **Apply now** (additive_only, semantics_preserved, $0) | Defer (waits for empirical anchor) |

DECISION-1 is the load-bearing one — affects all downstream verdicts. DECISION-2 and DECISION-3 are theoretical-stance choices (conservative vs permissive). DECISION-4 is engineering. DECISION-5 is rollout pacing.

---

## §11 — DECISIONS LOCKED 2026-05-04 (USER_AUTHORIZED)

User authorization 2026-05-04 (cycle ce681c40 message: "5 decisions all bg go" + "closure 속도우선"): **all 5 spec defaults ACKNOWLEDGED + LOCKED**.

| Decision | Locked value | Rationale |
|---|---|---|
| **D-1 Thresholds** | RED `<0.50` / YELLOW `0.50–0.75` / GREEN `≥0.75` | spec default (§9.1 historical re-classification all PASS) |
| **D-2 Canonical reading** | F2-override-canonical | §3.3 inconsistency rejection of raw-canonical |
| **D-3 GREEN tier** | phenomenal-tier required (≥1 WITNESSED phenomenal axis + Putnam PASS + binding ≥0.5 + no falsifier) | functional GREEN allowed = downgrade-prone |
| **D-4 hexa hook exit codes** | `RED=1 / YELLOW=2 / GREEN=0` | exit-code-as-band cleaner for shell consumers |
| **D-5 Roadmap annotation timing** | apply IMMEDIATELY as additive_only mutation | banding logic independent of F2 unfire; deferring no benefit |

### Honest C3 on lock-in
- D-1 thresholds chosen with limited comparison cohort (anima-internal only); future external cohort calibration may shift
- D-2 F2-override-canonical means substrate-architectural ceiling captures band; ceiling itself is theory-laden (14-gate is anima-specific)
- D-3 phenomenal-tier requirement effectively gates GREEN on Phase E binding evidence + EEG live (BLOCKED until those land)
- D-4 exit code convention contradicts UNIX `0=success` orthodoxy (here `0=GREEN=highest`); shell consumers must check explicitly
- D-5 immediate roadmap annotation creates audit-trail dependency on this lock-in BG; if user rescinds later, must additively superseded (raw#15 discipline)

### Downstream effects
- `clm_consciousness_verify.hexa` Putnam check #4 emits per D-3 phenomenal-tier requirement
- `tool/n_substrate_f1_v2_band.hexa` (NEW) hexa hook to be implemented per D-4 exit code semantics
- `.roadmap.n_substrate` cond.1 cross_link gets `f1_v2_band_thresholds` annotation per D-5
- All future band-cited verdicts MUST quote these thresholds verbatim

---

## §12 References

- F1_score_v2 spec (#96): `docs/strategic_f1_composite_v2_2026_05_02.md`
- CP2-CLM Phase D recompute (#104): `docs/cp2_clm_phase_d_recompute_2026_05_02.md`
- CP2-CLM Phase E spec (#105): `docs/cp2_clm_phase_e_spec_2026_05_02.md`
- Narrative roadmap §12 + §49.3 + §49.4 + §66.7: `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
- CLM verifier orchestrator: `tool/clm_consciousness_verify.hexa`
- CLM verifier landing doc: `docs/clm_consciousness_verify_landing_2026_05_02.ai.md`
- N substrate roadmap: `.roadmap.n_substrate`
- CLM domain roadmap: `.roadmap.clm`
- qmirror canonical migration: `docs/qmirror_canonical_migration_landed_2026_05_03.ai.md`
- BLM Phase 3 cond.2 reference (CLM phi baseline 41.86 fragility): `docs/blm_phase3_landed_2026_05_03.ai.md`

---

**status**: N_SUBSTRATE_F1_V2_BANDING_SPEC_2026_05_04_LOCKED_USER_AUTHORIZED
**verdict_key**: BAND_THRESHOLDS_0_50_0_75 · F2_OVERRIDE_CANONICAL · GREEN_REQUIRES_PHENOMENAL_AXIS · HEXA_HOOK_LOC_~105 · 8_HONEST_C3 · 3_FALSIFIERS_PREREGISTERED · 5_USER_DECISIONS_LOCKED_2026_05_04 · ROADMAP_ANNOTATION_BLOCK_APPLIED
