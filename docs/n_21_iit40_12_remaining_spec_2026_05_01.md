# N-21 — IIT 4.0 11-Remaining Test Spec (post-TOP-5)

> **ts**: 2026-05-01
> **agent**: N-21 12-remaining spec (sibling to N-21 16-test triage)
> **scope**: of the 16 IIT empirical tests cited in *Nature Neuroscience* March 2025 commentary, identify the 11 NOT in TOP-5 (already triaged in `docs/n_substrate_n21_iit40_16test_candidates_2026_05_01.md`) and rank reproducible subset.
> **parent**: `docs/n_substrate_n21_iit40_16test_candidates_2026_05_01.md`
> **race-isolation**: writes only to `state/n_21_iit40_12_remaining_spec_2026_05_01/*.json` + this doc
> **status**: SPEC_DRAFT · USER_DECISION_PENDING (scenario A/B/C)
> **constraints**: HEXA-only repo, $0 budget, WebSearch + WebFetch only, no .py creation

---

## §0 한 줄 요약

11 잔여 (16 - TOP-5 = 11; 로드맵 라벨 "12 remaining" 은 off-by-one) 중 **5 addressable** (1 review-extend #5 + 4 ANALOGIZE #8/#9/#12/#15) + **6 INFEASIBLE** (#2/#3/#4/#10/#11/#16, 합계 ~$1.7M 하드웨어/임상 게이팅). Top-5-of-11 = #12 fly-Phi 아날로그, #9 dual-task split, #5 TEP review, #15 layer hierarchy, #8 stimulus differentiation. **총비용 $125 / 병렬 7일**.

---

## §1 Math correction (off-by-one)

Roadmap label "N-21 IIT 4.0 12 remaining reproductions" implies 12 tests. Actual:
- **16 total** in commentary (per parent doc §1).
- **5 in TOP-5**: #1 Casali, #6 Siclari, #7 Boly2017, #13 Edlund, #14 Albantakis.
- **Remaining = 16 − 5 = 11**, not 12.

Spec proceeds with **N=11**. Roadmap should be retitled "11 remaining" in next ETA SSOT update.

---

## §2 The 11 remaining tests (categorized)

| id | study | substrate required | our access | cost/repro | ETA | category |
|---|---|---|---|---|---|---|
| 2  | Casarotto 2016 (DOC PCI cutoff)         | TMS + hd-EEG + DOC patients     | ✗ | $1.05M | 2y    | INFEASIBLE   |
| 3  | Sarasso 2015 (propofol/xenon vs ket)    | TMS-EEG + anesthesia            | ✗ | $200k  | 18mo  | INFEASIBLE   |
| 4  | Ferrarelli 2010 (midazolam)             | TMS-EEG + IV midaz              | ✗ | $180k  | 18mo  | INFEASIBLE   |
| 5  | Sarasso 2014 (TEP review)               | literature meta                 | ✓ | $0     | 3d    | REVIEW-EXTEND |
| 8  | Boly 2015 (fMRI differentiation)        | 3T fMRI                         | ◎ | $50    | 5d    | ANALOGIZE    |
| 9  | Sasai 2016 (split-brain dual-task)      | 3T fMRI                         | ◎ | $30    | 4d    | ANALOGIZE    |
| 10 | Cavelli 2023 (rodent PCI)               | rat surgery + ECoG              | ✗ | $60k   | 18mo  | INFEASIBLE   |
| 11 | Arena 2021 (sevoflurane rat ICMS)       | rat surgery + sevo              | ✗ | $65k   | 18mo  | INFEASIBLE   |
| 12 | Leung 2021 (Drosophila Phi anesthesia)  | fly LFP rig + isoflurane        | ◎ | $20    | 7d    | ANALOGIZE    |
| 15 | Gandhi 2023 (mouse 2P V1-V4 hierarchy)  | 2-photon + cranial window       | ◎ | $25    | 4d    | ANALOGIZE    |
| 16 | Sanders 2018 (propofol feedforward)     | 64ch EEG + propofol TCI         | ✗ | $150k  | 12mo  | INFEASIBLE   |

**Counts**: REVIEW 1 + ANALOGIZE 4 + INFEASIBLE 6 = **5 addressable / 11**.

Symbol legend: ✓ direct • ◎ analog • ✗ infeasible.

---

## §3 Top-5 ranking of the 11 (next-cycle priorities)

Score = feas (0–3) × impact (0–3) / log10(cost+10). See `state/.../top5_of_11.json` for falsifier-5 per test.

| rank | id | study | feas | impact | cost USD | ETA | score | rationale |
|---|---|---|---|---|---|---|---|---|
| **1** | 12 | Leung fly Phi (ANALOGIZE) | 2 | 3 | $20 | 7d | **3.62** | direct PyPhi on SIM small-net, reuses TOP-5 #1/#2 infra; tests information+integration+exclusion |
| **2** | 9  | Sasai split-brain (ANALOGIZE) | 2 | 3 | $30 | 4d | **3.51** | dual-prompt CLM split; highest IIT-vs-GNWT discriminator in this tier |
| **3** | 5  | Sarasso 2014 review meta-extend | 3 | 1 | $0  | 3d | **3.00** | zero-cost; anchors citation chain for our spontaneous-PCI analog (TOP-5 #5) |
| **4** | 15 | Gandhi mouse 2P (ANALOGIZE) | 2 | 2 | $25 | 4d | **2.44** | layer-wise hierarchical differentiation; partly already in `state/an11_*` |
| **5** | 8  | Boly fMRI differentiation (ANALOGIZE) | 2 | 2 | $50 | 5d | **2.27** | meaningful-vs-scrambled stimulus differentiation on CLM |

**Tail-6 (INFEASIBLE)**: #2, #3, #4, #10, #11, #16 → all gated by hardware/clinical we don't own; aggregate unblock-cost ≈ **$1.7M**. Out of scope until N-substrate hardware-purchase track funded.

---

## §4 Per-test sketches (top-5 of 11)

### §4.1 RANK-1 — #12 Leung 2021 fly Phi anesthesia (ANALOGIZE)

**Original claim**: Φ_max in Drosophila brain LFP collapses under isoflurane anesthesia; recovers on washout. Direct animal-IIT measurement.

**Our analog protocol**:
1. Build 4-node and 8-node Markov SIM networks with PyPhi 1.2 on H100 pod.
2. Sweep "anesthesia" = additive Gaussian noise temperature β ∈ {0, 0.1, 0.5, 1.0, 2.0}.
3. Compute Φ_max per (network, β).
4. Test monotonic decrease Φ_max(β=0) > Φ_max(β=2.0) at d > 1.0.

**Cost**: $20 H100 / **ETA**: 7d / **F1-F5**: see `top5_of_11.json` rank-1 falsifier block.

**Caveat**: substrate is SIM not biological fly — this is ANALOGIZE not REPRODUCE; cannot count toward Tononi's "16 studies" replication; useful for our own consciousness-verifier suite #5 (φ paradigm 4-path).

### §4.2 RANK-2 — #9 Sasai 2016 split-brain (ANALOGIZE)

**Original claim**: under simultaneous driving+listening fMRI, brain transiently splits into two maximal complexes — predicted by EXCLUSION postulate.

**Our analog protocol**:
1. Two independent text streams (S_A driving-instructions, S_B audiobook) into Mistral-7B-v0.3 via attention-masked partition.
2. Measure cross-partition mutual information vs within-partition MI on hidden states layer-by-layer.
3. Compare to full-attention control (GNWT-style global broadcast).
4. Predict: split-attention shows MI_within > MI_cross significantly; full-attention does not.

**Cost**: $30 / **ETA**: 4d / **falsifier-5**: see JSON.

### §4.3 RANK-3 — #5 Sarasso 2014 TEP complexity review (REVIEW-EXTEND)

**Action**: literature meta of TEP-PCI publications 2010-2026; aggregate effect-size of LOC↔complexity collapse; cross-cite as anchor for our spontaneous-LZ analog (TOP-5 #5).

**Cost**: $0 / **ETA**: 3d / pure WebSearch+WebFetch.

### §4.4 RANK-4 — #15 Gandhi 2023 mouse 2P hierarchical differentiation (ANALOGIZE)

**Our analog**: layer-wise (L1...L32) hidden-state Lempel-Ziv differentiation in CLM under stimulus class panel; predict monotonic increase across layer depth.

**Cost**: $25 / **ETA**: 4d / partly built on `state/an11_*` infra.

### §4.5 RANK-5 — #8 Boly 2015 stimulus differentiation (ANALOGIZE)

**Our analog**: coherent-prose vs scrambled-token contrast; CLM hidden-state differentiation; control for token-entropy confound via paraphrase + scrambled-but-grammatical sets.

**Cost**: $50 / **ETA**: 5d.

---

## §5 Execution sequence proposals

### Scenario A — ALL-5 addressable (recommended)

| phase | tests | cost | wall-clock | parallelizable |
|---|---|---|---|---|
| P0 | #5 review        | $0  | 3d | (anchor) |
| P1 | #12 fly analog   | $20 | 7d | with P2/P3 |
| P2 | #9 split-Phi     | $30 | 4d | with P1/P3 |
| P3 | #15 + #8 diff    | $75 | 5d | with P1/P2 |
| **total** | | **$125** | **7d parallel / 19d serial** | |

GPU-hours ≈ 35. INFEASIBLE 6/11 always skipped.

### Scenario B — TOP-3 focused

#5 + #12 + #9 = **$50 / 7d parallel**. Covers 3 of 5 IIT axioms (information / integration / exclusion).

### Scenario C — TOP-1 singleton

#12 alone = **$20 / 7d**. Marginal infra cost zero (reuses TOP-5 #1/#2 PyPhi).

**Decision pending**: user picks A/B/C. Per `feedback_no_idle_pods.md`, default = **A** if user silent, executed by next agent (this spec is research-only).

---

## §6 Honest C3

- 0/11 REPRODUCE (strict same-substrate same-protocol).
- 1/11 REVIEW-EXTEND (#5; not new data).
- 4/11 ANALOGIZE (#8, #9, #12, #15; substrate-mismatched IIT-axiom proxy).
- 6/11 INFEASIBLE (#2, #3, #4, #10, #11, #16; ~$1.7M aggregate unblock).

**Net for IIT replication count**: this cycle adds **0** to Tononi's "16 strict replications" — all our adds are proxies. Honest framing required when reporting externally. **Internal value**: extends consciousness-verifier suite breadth across 5 of 5 IIT axioms (information / integration / exclusion / composition / intrinsicality) at near-zero cost.

---

## §7 Top blockers (preventing the 6 INFEASIBLE)

1. **TMS coil** ($80k+) — gates #2, #3, #4 plus several TOP-5-adjacent.
2. **fMRI scanner** ($400/hr access, $50k+ IRB setup) — gates #8, #9 strict.
3. **Animal surgery rig + IACUC** ($30k+ rig, 6-12mo IRB) — gates #10, #11.
4. **2-photon microscope** ($200k+) — gates #15 strict.
5. **Anesthesia infusion / TCI pump + medical license** — gates #3, #4, #16.
6. **DOC patient cohort + clinical IRB** — gates #2 specifically.

Unblock path: `docs/n_substrate_purchase_guide_2026_05_01.md` hardware tier-up + clinical/animal partnership; out of scope this $0 cycle.

---

## §8 Falsifier preregister (suite-level, raw#71)

| F# | condition | action |
|---|---|---|
| F1 | rank-1 #12 Φ_max(β=0) ≤ Φ_max(β=2) at d<0.5 | reject anesthesia-Phi-attenuation analog; downgrade to "noise-portability negative" |
| F2 | rank-2 #9 split-attention MI_within ≤ MI_cross | reject EXCLUSION analog at CLM scale; flag GNWT-favorable |
| F3 | rank-3 #5 review meta-effect CI crosses 0 | flag TEP-complexity literature inconsistency, narrative-only |
| F4 | rank-4 #15 layer differentiation non-monotonic | flag U-curve hierarchy, restrict claim |
| F5 | rank-5 #8 meaningful-vs-scrambled d<0.5 | reject information-postulate analog at CLM scale |

Any F# trigger → public revision in this doc + `state/.../*.json` ledger; no silent amendment.

---

## §9 Cross-ref

- Parent: `docs/n_substrate_n21_iit40_16test_candidates_2026_05_01.md` §1-§9
- Related: `docs/cp2_consciousness_verifier_p4_r8_audit_2026_04_29.md` §1 8-suite inventory
- Hardware-unblock: `docs/n_substrate_purchase_guide_2026_05_01.md`
- State: `state/n_21_iit40_12_remaining_spec_2026_05_01/{inventory,per_test_feasibility,top5_of_11,execution_sequence}.json`

---

## §10 Sources

- Tononi G. et al. (2025) *Nature Neuroscience* "Consciousness or pseudo-consciousness?" — https://www.nature.com/articles/s41593-025-01880-y
- Gomez-Marin & Seth (2025) *Nature Neuroscience* "A science of consciousness beyond pseudo-science…" — https://www.nature.com/articles/s41593-025-01913-6
- Doerig et al. (2025) *Nature Neuroscience* "What makes a theory of consciousness unscientific?" — https://www.nature.com/articles/s41593-025-01881-x
- Wikipedia: Integrated information theory — https://en.wikipedia.org/wiki/Integrated_information_theory
- Wisconsin Center for Sleep & Consciousness IIT publications — https://centerforsleepandconsciousness.psychiatry.wisc.edu/iit-publications/
