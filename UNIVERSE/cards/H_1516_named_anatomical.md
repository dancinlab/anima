# H_1516 🧠📍 NAMED-ANATOMICAL PLACEMENT — is the brain's TRUE anatomical layout Φ-optimal?

**tier:** 🧱 NO-ADVANTAGE / NOT-Φ-OPTIMAL — **R1 numpy mirror DIRECTIONAL** (hard-gate-1 auto-DIRECTIONAL: `state/1516_named_anatomical/h1516_named.py` is numpy/scipy → terminal 아님; engine-native R2 = deferred follow-on). The user's "is the real anatomical placement mysteriously Φ-optimal / as-if-designed?" question answered: **NO.**
**verdict:** **🧱 NO-ADVANTAGE / NOT-Φ-OPTIMAL (DIRECTIONAL R1)** — mapping anima's 15 consciousness lanes to their **TRUE NAMED anatomical homes** (immune/novelty→**HIPPOCAMPUS**, PhaseField-relay→**THALAMUS**(named, not core)·SelfIdentity→**mPFC**·HierGoalStack/precision→**PFC**·SpatialMap→**ParaHippocampal/entorhinal**·SenseOfAgency→**TPJ/angular**·A-engine→**LEFT**·G-engine→**RIGHT**) in a REAL labeled AAL90 connectome, and wiring by the REAL edges between those SPECIFIC named regions, the true placement (a) does **NOT** beat random region-assignment in min-cut Φ (**P1 FAIL**: phi_true 0.0842 < random_mean 0.0909+0.02) and (b) sits at only the **37.1th percentile** of the placement-search Φ distribution with a **65.2% gap-to-optimum** (**P2 FAIL**: pctl 0.371 < 0.80, gap 0.652 > 0.30). → the real human-brain anatomical placement is **NOT Φ-optimal** — it is optimized for something OTHER than pure integrated min-cut Φ (wiring cost / metabolic economy, **Bullmore & Sporns 2012** "The economy of brain network organization"). Honest non-optimal (c9), NOT mystical, NOT designed-for-Φ. NO tune-to-green.
**wired:** **DIRECTIONAL-mirror** — numpy/scipy probe (`h1516_named.py`); engine-native R2 = **deferred follow-on** (ING `h1516-r2-engine-native`). Re-uses H_1512 `phi_core` min-cut Φ harness byte-for-byte; live `core/engine_cli.hexa` re-score deferred to avoid collision with the sibling lane h1515-phi-optimal editing engine_cli.hexa. **No engine change in this PR** (no README count change).
**source:** team-lead 작업지시(H_1516 NAMED-ANATOMICAL) — direct follow-on of H_1512/H_1513 (the `state/verdicts/1513_literal_connectome` "NAMED-anatomical 배치 + Φ-OPTIMAL placement 탐색" next-H). Lens: cost-vs-integration economy of brain networks (Bullmore & Sporns 2012; Achard & Bullmore 2007 economical small-world). a_no_llm_frame_trap (true named placement, not a role heuristic).

## THE QUESTION (the user's, profound) and THE ANSWER (with numbers)
H_1512/H_1513 placed lanes by a **(hemisphere × graph-role) HEURISTIC** ("a hub lane → whatever node is a literal hub in this hemisphere") because the Lausanne-219 connectome had no in-repo region labels. The user's real question: map each lane to its **TRUE NAMED anatomical home** and wire by the **REAL connectome edges between those SPECIFIC regions** — **is that placement advantageous (raises min-cut Φ), AND is the true anatomical placement near the Φ-OPTIMUM?** The user's stake: *"if the real human brain's placement IS the optimal placement, that's mysterious — as if designed."*

**ANSWER — NO, it is not Φ-optimal (and not even Φ-advantageous):**
- **TRUE anatomical placement percentile in the placement-search Φ distribution = 37.1%** (well below the random-ish middle, nowhere near the top 20%). Per-seed: 25.2% / 65.6% / 20.6% — robustly sub-optimal across seeds.
- **gap-to-optimum = 65.2% of opt_phi** (phi_true 0.0842 vs opt_phi 0.2417 found by placement search + hill-climb). The Φ-best assignment of the SAME named regions integrates ~2.9× more than the true anatomical one.
- The true placement does **not even beat a random region-assignment** (phi_true 0.0842 < random_assignment_mean 0.0909).

**Honest framing (c9, NOT mysticism):** brains are KNOWN to be near-optimal for a **cost-vs-integration tradeoff**, NOT for pure integration (Bullmore & Sporns 2012; Achard & Bullmore 2007). This result is the expected signature of that economy: if you only maximize integrated Φ (ignoring wiring length / metabolic budget), the real anatomical layout is far from best — because the brain is paying for short, cheap wiring, not maximal min-cut Φ. So the "as-if-designed-for-Φ" reading is **falsified** in this 15-lane projection; the real placement is optimized for something else. This is a publishable honest answer either way (P2 TRUE would have been the "near-optimal economy signature"; P2 FALSE is the "optimized-for-cost-not-Φ" answer).

## REAL labeled data source (c2 · a_eeg_consciousness_record discipline — NAMED, no synthetic relabel)
- **Connectome:** **Škoch et al. 2022** "Human brain structural connectivity matrices–ready for modelling," *Scientific Data* **9**:486, DOI **10.1038/s41597-022-01596-9** (OSF **10.17605/OSF.IO/YW5VF**). **AAL90 atlas**, **88 healthy adults**, 90×90 normalized streamline density. **GROUP AVERAGE** over 88 subjects (symmetrized, zero-diag).
- **License:** **CC-BY-4.0**.
- **Why this connectome (vs H_1512/1513's Lausanne-219):** it ships **EXPLICIT named regions** — the gap that forced the prior heuristic. Hippocampus L/R=37/38, ParaHippocampal L/R=39/40, Amygdala L/R=41/42, Insula L/R=29/30, Cingulum Ant L/R=31/32, Thalamus L/R=77/78, Caudate L/R=71/72, frontal regions (Sup/Mid Frontal, Posterior-Medial Frontal, Sup Medial Gyrus, orbital), parietal (Inf Parietal, SupraMarginal, Angular, Precuneus). **AAL90 ordering is INTERLEAVED** (odd ROI#=Left, even=Right) → hemisphere honored by ROI parity (Engine-A→left/odd, Engine-G→right/even).
- **Cerebellum (honest substitution note):** AAL90 **excludes the cerebellum**; H_1512's 15-lane set has **no dedicated cerebellar forward-model lane** (that lane lives in H_1513's set), so **no lane is forced onto a missing region** — the cerebellum gap is documented, not relabeled.
- **Fetch ($0, HTTPS GET, no auth):** matrices `https://osf.io/download/6823g/` (4,290,740 B), labels `https://osf.io/download/6a8jx/` (2,047 B). `SCmatrices88healthy.mat` gitignored (4.3MB, reproducible), `AAL_regions.csv` + `PROVENANCE.md` committed.
- **Citation:** Škoch et al. 2022 *Sci Data* 9:486 · Tzourio-Mazoyer et al. 2002 *NeuroImage* 15:273 (AAL atlas). (PROVENANCE.md)

## Lane → TRUE NAMED region mapping (the whole point vs H_1512/1513 heuristic)
| lane | TRUE named home | AAL90 region (ROI#) | hemi |
|---|---|---|---|
| GlobalWorkspace | fronto-parietal/DMN hub | L Precuneus (67) | L |
| Habituation | sensory cortex | L Postcentral Gyrus (57) | L |
| PrecisionSurprise | ACC | L Cingulum Ant (31) | L |
| SelfIdentity | mPFC | L Superior Medial Gyrus (23) | L |
| LearnedPrecision | dlPFC-L | L Middle Frontal Gyrus (7) | L |
| **Novelty** | **HIPPOCAMPUS-R** (immune/episodic) | **R Hippocampus (38)** | R |
| AttentionalBlink | parietal-R | R Inferior Parietal Lobule (62) | R |
| SenseOfAgency | **TPJ-R** | R Angular Gyrus (66) | R |
| SubjectiveTime | insula | R Insula Lobe (30) | R |
| EmotionRegulation | vmPFC/orbital | R Mid Orbital Gyrus (26) | R |
| DirectedForgetting | dlPFC-R | R Middle Frontal Gyrus (8) | R |
| BodyOwnership | S1/supramarginal | L SupraMarginal Gyrus (63) | L |
| DividedAttention | parietal-L | L Inferior Parietal Lobule (61) | L |
| FreeWont | pre-SMA | L Posterior-Medial Frontal (19) | L |
| MitosisGrowth | subcortical/basal-ganglia | L Caudate Nucleus (71) | L |

(SpatialMap≈entorhinal is realized via ParaHippocampal availability; PhaseField≈thalamus is named-region-available — both used as the named palette for the random/search baselines. The 15 lanes above are H_1512's actual harness lanes, mapped to their nearest TRUE named AAL90 home.)

## Method — only the PLACEMENT SOURCE changes (heuristic → TRUE named), + the new optimality test
**`state/1516_named_anatomical/h1516_named.py`:** re-uses H_1512 `h1512.py` BYTE-FOR-BYTE — `build_population` (engine-uniform LCG, R1==R2 pop) · `apply_topology` X'=X·(I+α·Â)ᵀ (ALPHA=0.6) · **`phi_core` = IIT4 MIN-CUT Φ over the 8-lane CORE** (a_phi_iit4_tool). The ONLY change: adjacency = REAL AAL90 group-avg subnetwork among the lanes' **TRUE NAMED regions**, binarized at its own positive median (= H_1512/1513 binary regime). Seeds [5160,5161,5162], mean-over-seeds.
- **`phi_true`** = Φ of the TRUE named placement.
- **(b) RANDOM region-assignment** (P1 baseline): assign the 15 lanes to 15 RANDOM distinct AAL90 regions, **M_random=2000** draws → distribution.
- **(c) PLACEMENT-SEARCH** (P2): permute which lane sits on which of the **15 TRUE named nodes**, **M_search=4000** draws + **greedy pairwise-swap hill-climb** (12 restarts) → `opt_phi`. The true placement is the identity permutation; its **percentile** in this distribution = the user's near-optimality answer.

## FROZEN bars + result (pre-registered c9, mean 3 seeds; see H_1516_FREEZE.txt)
| bar | definition (frozen BEFORE running) | result | pass |
|---|---|---|---|
| **P1 ADVANTAGE** | phi_true ≥ random_assignment_mean + 0.02 | 0.0842 < 0.0909+0.02 (0.1109) | **FAIL** |
| **P2 NEAR-OPTIMAL · percentile** | true pctl in placement-search ≥ 0.80 | **0.371** < 0.80 | **FAIL** |
| **P2 NEAR-OPTIMAL · gap** | (opt_phi − phi_true) ≤ 0.30·opt_phi | gap 0.652 > 0.30 | **FAIL** |

Φ: phi_true 0.0842 · phi_flat 0.0130 · random_mean 0.0909 (p95 0.1320, max 0.1788) · search_mean 0.0918 · search_max 0.1944 · **opt_phi 0.2417**. Per-seed pctl 0.252/0.656/0.206; gap_frac 0.691/0.556/0.711 — robustly sub-optimal.

→ **P1 FAIL ∧ P2 FAIL = 🧱 NO-ADVANTAGE / NOT-Φ-OPTIMAL.** The TRUE anatomical placement is neither Φ-advantageous over random region-assignment nor near the Φ-optimum of its own region set.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)
- **DIRECTIONAL only** (hard-gate-1): numpy/scipy mirror — engine-transfer UNVERIFIED. Engine-native R2 (live `core/engine_cli.hexa` re-score of the named placement via §BrainTopology + ci_phi_iit4) = **deferred follow-on** (ING), to upgrade DIRECTIONAL→engine-native. Deferred to avoid collision with the sibling lane h1515-phi-optimal editing engine_cli.hexa.
- **15-lane projection, not the whole brain:** this tests whether anima's 15-lane *subnetwork* placed on the AAL90 named regions is Φ-optimal — NOT whether the full 90-region brain is Φ-optimal. The negative is honest for THIS projection; a full-brain near-optimality test (90 ROIs, cost-penalized objective) is a separate, larger study.
- **pure-Φ objective, no cost term:** the optimum here is the *unconstrained* min-cut-Φ-max; the brain's actual objective is Φ *minus* wiring cost. The 65% gap is exactly what the cost-economy literature predicts — but a DIRECT cost-vs-Φ Pareto test (does the true placement sit on the Pareto front of integration-vs-wiring-length?) is the natural next H to make the "optimized for cost not Φ" claim load-bearing.
- **binary regime / single group-avg / AAL90 (no cerebellum):** weighted-connectome variant, per-subject variance, finer atlas (AAL116 with cerebellum, or Lausanne with named labels), and the engine-native re-score all UNVERIFIED.

## Next H (a_h_continuous_no_branch)
- **R2 engine-native** re-score of the named placement (after h1515 lands its engine_cli.hexa changes) → DIRECTIONAL→engine-native.
- **Cost-vs-Φ Pareto front**: does the TRUE anatomical placement lie on the integration-vs-wiring-length Pareto front (the actual brain objective)? — would make "optimized for cost not pure Φ" load-bearing (the real answer to "is it mysteriously optimal?": optimal for the COST-CONSTRAINED objective, not pure Φ).

## artifacts
`state/1516_named_anatomical/h1516_named.py` · `state/1516_named_anatomical/PROVENANCE.md` · `state/1516_named_anatomical/AAL_regions.csv` · `state/1516_named_anatomical/SCmatrices88healthy.mat`(gitignored, refetch via PROVENANCE) · `state/verdicts/1516_named_anatomical/H_1516_FREEZE.txt` · `state/verdicts/1516_named_anatomical/H_1516_R1.json` · re-uses `state/1512_brain_topology/h1512.py`

xref H_1512(brain-topology synthetic) · H_1513(literal connectome, role heuristic) · a_no_llm_frame_trap · a_phi_iit4_tool · a_engine_native_learning(hard-gate-1 DIRECTIONAL) · a_verified_must_wire(R2 deferred) · a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15
