# H_1517 🧠💰 COST-vs-Φ PARETO FRONT — is the brain near-optimal for COST-CONSTRAINED integration?

**tier:** 🟠 CHEAP-but-DOMINATED — **R1 numpy/scipy mirror DIRECTIONAL** (hard-gate-1 auto-DIRECTIONAL: `state/1517_cost_pareto/h1517_pareto.py` imports numpy/scipy → terminal 아님; engine-native R2 = deferred follow-on ING). The deep version of the user's "is the brain mysteriously optimal?" — answered with the cost axis added: **PARTLY** (cheap, but not on the front).
**verdict:** **🟠 CHEAP-but-DOMINATED (DIRECTIONAL R1)** — for EACH lane→region placement we compute BOTH axes: integration **Φ** (IIT4 min-cut, exactly as H_1512/1515/1516) and total wiring **COST** (Σ over present edges of euclidean distance between the two AAL region MNI centroids). The TRUE named-anatomical placement (H_1516 mapping) IS **cheap** — its wiring cost is in the **bottom tercile** (cost-percentile **20.0%**, P2 PASS), confirming the brain trades Φ for short/cheap wiring (Bullmore & Sporns 2012 economy). BUT it is **NOT on the Φ-vs-cost Pareto front** (P1 FAIL): **8.84%** of candidate placements achieve **cheaper-or-equal cost AND strictly higher Φ** (domination_frac 0.0884 > 0.05), normalized **distance-to-front 0.247** (> 0.05). → in this 15-lane projection the real anatomical placement is **economical but DOMINATED** — it pays for cheap wire yet a cheaper-or-equal placement integrates more. Honest non-optimal either way (c9), NO tune-to-green.
**wired:** **DIRECTIONAL-mirror** — numpy/scipy probe (`h1517_pareto.py`); engine-native R2 (live `core/engine_cli.hexa` §BrainTopology Φ + a cost-axis op, byte-exact re-score) = **deferred follow-on** (ING `h1517-r2-engine-native`). Re-uses H_1512 `phi_core` min-cut Φ harness + H_1516 NAMED map byte-for-byte; **no engine change in this PR** (no README count change).
**source:** team-lead 작업지시(H_1517 COST-vs-Φ PARETO FRONT) — the payoff experiment named as the explicit next-H by both H_1515 and H_1516 ("cost-vs-Φ Pareto: does the true placement sit on the integration-vs-wiring-length front, the real brain objective?"). Lens: economy of brain network organization (Bullmore & Sporns 2012; Achard & Bullmore 2007 economical small-world). a_no_llm_frame_trap, a_break_the_wall (honest result either way).

## THE QUESTION (the deep version) and THE ANSWER (with numbers)
Two prior MERGED lanes found the TRUE anatomical placement is Φ-SUBOPTIMAL for **UNCONSTRAINED** integration: **H_1515** (#2493, engine-native — node-permutation search finds ~2.5× higher-Φ placements) and **H_1516** (#2494, REAL AAL90 — true named placement at only ~37th Φ-percentile, ~65% below the Φ-optimum). The honest interpretation (Bullmore & Sporns 2012, "The economy of brain network organization"): the brain optimizes **COST-CONSTRAINED** integration, not pure Φ — it pays for short/cheap wiring. **H_1517 makes that load-bearing** by adding the cost axis and asking: does the TRUE placement lie ON (or near ε of) the Φ-vs-cost **PARETO FRONT**?

**ANSWER — PARTLY (CHEAP-but-DOMINATED):**
- **COST-CHEAP = YES (P2 PASS):** the true placement's wiring cost (2976.3 mm) sits at the **20.0th percentile** of the candidate cost distribution (range 2205–3992 mm) — **bottom tercile**. The brain genuinely pays for short, cheap wire. *This is the part of the user's "mysteriously optimal" intuition that the cost axis vindicates.*
- **PARETO-EFFICIENT = NO (P1 FAIL):** the true placement is **OFF the front** — **8.84%** of candidates dominate it (cheaper-or-equal cost AND strictly higher Φ), normalized distance-to-front **0.247**. A cheaper-or-equal placement still integrates more.
- **Within the cheap band (P3, report):** among placements with cost ≤ true-cost, the true placement's Φ is at the **55.9th percentile** — middling even inside its own affordable budget (it is not the Φ-best of the cheap regime).
- **Φ-optimum anchor:** opt_phi 0.3513 (cost 3291.7 mm) vs true Φ 0.0867 — the unconstrained Φ-max integrates ~4× more (corroborates H_1515/1516).

→ **the deep answer:** adding the cost axis **partly** rescues the placement (it is cheap, as the economy literature predicts) but does **not** make it Pareto-optimal in this 15-lane projection — it is economical-but-dominated. The "as-if-designed-for-(cost-constrained)-optimality" reading is **partly supported (cheap) but not confirmed (off the front)**. Publishable honest result either way (🟢 if it had been on the front; 🟠 CHEAP-but-DOMINATED is what the data show).

## REAL labeled data (c2 · two REAL sources, licensed + cited)
1. **CONNECTOME** — **Škoch et al. 2022** "Human brain structural connectivity matrices–ready for modelling," *Scientific Data* **9**:486, DOI **10.1038/s41597-022-01596-9**, OSF **10.17605/OSF.IO/YW5VF**, **CC-BY-4.0**. AAL90 atlas, **88 healthy adults**, 90×90 normalized streamline density, **GROUP AVERAGE** (symmetrized, zero-diag, binarized at own positive median = the H_1512/1513/1516 binary regime). Fetch ($0, HTTPS): `https://osf.io/download/6823g/` (4,290,740 B). `SCmatrices88healthy.mat` gitignored (reproducible).
2. **CENTROIDS** (the new cost axis) — **AAL atlas** (Tzourio-Mazoyer et al. 2002, *NeuroImage* 15(1):273-289), **ROI_MNI_V4.nii** (MNI 2mm, 91×109×91, sform affine). Each AAL90 region's MNI centroid = **mean MNI coordinate of all voxels labeled with that ROI**, computed reproducibly from the atlas NIfTI (`make_centroids_if_missing()` in the probe) → committed `state/1517_cost_pareto/AAL90_centroids_MNI.csv`. Atlas NIfTI fetched from FieldTrip's bundled copy (`fieldtrip/template/atlas/aal/ROI_MNI_V4.nii`, $0). **Cross-checked**: Precentral_L=(-38.9,-7.0,49.6), Hippocampus_L=(-25.3,-22.0,-11.4), Thalamus_L=(-11.2,-18.8,6.6), Caudate_L=(-11.8,9.7,8.1) — all anatomically correct, left=−x / right=+x, AAL90 ROI# order verified against `AAL_regions.csv`.

Wiring cost of an edge (i,j) = ‖centroid_i − centroid_j‖₂ (MNI mm); total cost of a placement = Σ over PRESENT edges (the SAME binarized adjacency the Φ metric sees — the edges that carry integration are the edges that cost wire).

## Method (`state/1517_cost_pareto/h1517_pareto.py`)
Re-uses H_1512 `h1512.py` BYTE-FOR-BYTE — `build_population` (engine-uniform LCG, R1==R2 pop), `apply_topology` X'=X·(I+α·Â)ᵀ (ALPHA=0.6), **`phi_core` = IIT4 MIN-CUT Φ over the 8-lane CORE** (a_phi_iit4_tool) — and H_1516's NAMED lane→AAL-region map. The ONLY new thing is the **cost axis** (centroid-distance sum). Seeds [5170,5171,5172], mean-over-seeds.
- **Candidate cloud** (per seed): the TRUE anatomical placement + **M_random=3000** random placements (15 DISTINCT regions drawn from ALL 90 AAL nodes — the H_1516 random-baseline space, so BOTH cost AND Φ vary) + the **Φ-optimum** (hill-climb, all-90 single-region replacement, 12 restarts). Each → a (cost, Φ) point.
- **Pareto front** = non-dominated set (no other candidate has lower-or-= cost AND higher-or-= Φ with strict improvement on ≥1 axis).
- **Measurement-fix note (frozen-first, a_break_the_wall taxonomy-(a) — bars UNCHANGED):** the first candidate construction permuted lane→node over the SAME 15 named nodes, which is **cost-degenerate** (a permutation reuses the identical edge set → constant 2976.3 mm cost, cost axis collapses). Fixed to draw from all 90 nodes so the cloud spans both axes; **the true placement's own cost & Φ and all three bars are identical** — only the candidate cloud was corrected to be non-degenerate (documented in H_1517_FREEZE.txt).

## FROZEN bars + result (pre-registered c9, mean 3 seeds; see H_1517_FREEZE.txt)
| bar | definition (frozen BEFORE running) | result | pass |
|---|---|---|---|
| **P1a domination** | frac. of candidates strictly dominating true ≤ 0.05 | **0.0884** > 0.05 | **FAIL** |
| **P1b distance-to-front** | normalized cost-Φ distance to front ≤ 0.05 | **0.247** > 0.05 | **FAIL** |
| **P1 PARETO-EFFICIENT** | P1a ∧ P1b | — | **FAIL** |
| **P2 COST-CHEAP** | true cost-percentile ≤ 0.3333 (bottom tercile) | **0.200** ≤ 0.333 | **PASS** |
| **P3 cheap-band Φ (report)** | Φ-rank of true among cost≤true-cost placements | 0.559 | (non-gating) |

cost_true 2976.3 mm (pctl 20.0%, range 2205–3992) · phi_true 0.0867 (pctl 53.9%, range 0.0051–0.3513) · opt_phi 0.3513 (cost 3291.7) · n_front ≈9.3 of 3002. Per-seed: cost% 21.1/18.8/20.2 (P2 robust), dom% 5.4/5.9/15.2, dist 0.167/0.257/0.317 (P1 FAIL all seeds), cheap-band Φ% 74.3/68.4/25.0.

→ **P2 PASS ∧ P1 FAIL = 🟠 CHEAP-but-DOMINATED.** The brain's true placement is economical (cheap wiring) but not on the cost-constrained Pareto front in this projection.

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)
- **DIRECTIONAL only** (hard-gate-1): numpy/scipy mirror — engine-transfer UNVERIFIED. Engine-native R2 (live `core/engine_cli.hexa` §BrainTopology Φ + a cost-axis op, byte-exact re-score) = **deferred follow-on** (ING).
- **15-lane projection, not the whole brain:** tests whether anima's 15-lane subnetwork placed on AAL90 regions is cost-constrained-optimal — NOT the full 90-region brain. A full-brain Pareto test (90 ROIs) is a larger separate study.
- **cost model = euclidean centroid distance** (a standard wiring-length proxy; real metabolic/volumetric cost, fiber-tract length vs straight-line, and a Φ−λ·cost scalarization with a fitted λ are unverified). The cheap-but-dominated result is for THIS straight-line cost proxy.
- **binary regime / single group-avg / AAL90 (no cerebellum) / deterministic LCG population:** weighted-connectome variant, per-subject variance, finer atlas, and engine-native re-score all UNVERIFIED.
- **Pareto front estimated from 3000 random + hill-climb anchor:** a denser sweep or a global Pareto solver could move dom_frac/distance slightly; the P1 FAIL margin (0.247 ≫ 0.05 distance, 8.8% ≫ 5% domination) is large enough to be robust to that.

## Next H (a_h_continuous_no_branch)
- **R2 engine-native** Φ+cost re-score on live `core/engine_cli.hexa` → DIRECTIONAL→engine-native.
- **Scalarized objective:** fit λ in (Φ − λ·cost) and ask whether the TRUE placement is the argmax for SOME λ ≥ 0 (the brain may optimize a specific cost-weight rather than the full front) — a softer "near-optimal for its own λ" test than strict Pareto.
- **Full-brain (90-ROI) cost-vs-Φ Pareto** + fiber-length cost (vs straight-line) variants.

## artifacts
`state/1517_cost_pareto/h1517_pareto.py` · `state/1517_cost_pareto/AAL90_centroids_MNI.csv` (committed, reproducible) · `state/1517_cost_pareto/AAL_regions.csv` · `state/1517_cost_pareto/SCmatrices88healthy.mat`(gitignored, refetch OSF 6823g) · `state/1517_cost_pareto/ROI_MNI_V4.nii`(gitignored, refetch FieldTrip) · `state/verdicts/1517_cost_pareto/H_1517_FREEZE.txt` · `state/verdicts/1517_cost_pareto/H_1517_R1.json` · `state/verdicts/1517_cost_pareto/H_1517.txt` · re-uses `state/1512_brain_topology/h1512.py`

xref H_1512(brain-topology synthetic) · H_1513(literal connectome) · **H_1515**(Φ-optimal placement, engine-native, unconstrained suboptimal) · **H_1516**(named-anatomical, unconstrained NOT-Φ-optimal — this lane adds the cost axis it named as next) · a_no_llm_frame_trap · a_phi_iit4_tool · a_engine_native_learning(hard-gate-1 DIRECTIONAL) · a_verified_must_wire(R2 deferred) · a_break_the_wall · a_scale_honest_scope · a_toy_scale_recheck · c9 · c15
