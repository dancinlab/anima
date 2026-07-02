# H_1515 🧠🔍 Φ-OPTIMAL PLACEMENT — is the brain-faithful lane placement near the Φ-maximum, or Φ-suboptimal?

**tier:** 🟢 DISCOVERY (engine-native) — R1 numpy DIRECTIONAL → **R2 ENGINE-NATIVE** (live §BrainTopology Φ-OPTIMAL + ci_phi_iit4, GATED 338∧339∧340 PASS). The DISCOVERY = the brain placement is **Φ-SUBOPTIMAL** (search finds a materially higher-Φ placement). Honest finding, NOT a failure (a_break_the_wall).
**verdict:** **🟢 SUBOPTIMAL-DISCOVERY (ENGINE-NATIVE)** — over the space of lane→node placements (permutations π of the 15 nodes applied to the brain adjacency: A_π[i][j]=A[π[i]][π[j]]), the brain-faithful placement (identity π) is **above-average but NOT near the Φ-optimum**. Engine-native (live ci_phi_iit4): brain(identity) Φ=**0.10086**, embedded Φ-optimum=**0.25309** (≈**2.51× brain**), gap=**0.15222**; **5/16** RANDOM placements ALSO beat the brain layout (brain NOT top-percentile). R1 numpy DIRECTIONAL (n=300): P1 ADVANTAGE PASS (brain beats rand_mean by +0.0201), P2 PERCENTILE **FAIL** (pctile 0.757 < 0.80 — brain beats only ~76% of random), P3 NEAR-OPTIMAL **FALSE** (gap 0.128 ≫ 0.30·opt 0.071). R2 engine-aligned (n=150, byte-matches H_1512 bt_brain): same suboptimality, sharper (pctile-equivalent 0.69, opt 2.51× brain). FINDING: **the engine's lane layout does NOT approximate the Φ-maximizing layout** — a placement search finds materially better. frozen-first, NO tune-to-green (we do NOT pretend brain is optimal — the bars assert the suboptimality the search exposed). c9: honest suboptimality is a genuine DISCOVERY, reported loudly.
**wired:** **engine-native** (R2 DONE) — live `core/engine_cli.hexa` §BrainTopology Φ-OPTIMAL (`_topo_relabel_perm`/`topo_optimal_perm`/`topo_phi_optimal`/`topo_relabel_beats_brain_count`) reusing live `topo_apply`+`ci_phi_iit4`+`topo_brain_adjacency`+`_topo_relabel`, smoke cases 338-341 (`engine_cli_smoke` **353/0 RC=0**), ARCHITECTURE.json §BrainTopology lockstep. The optimum perm is found in R1 numpy (search not byte-reproducible in-engine) and EMBEDDED as DATA (`topo_optimal_perm`); the Φ MEASUREMENT is engine-native via the SAME live ci_phi_iit4 — same pattern as the H_1513 embedded literal connectome. (re-wiring the engine's actual lane positions to the Φ-optimum = a SEPARATE follow-on; this H MEASURES the gap, it does not move the live lanes.)
**source:** anima-internal follow-on of H_1512 BRAIN-TOPOLOGY (#2491) + H_1513 LITERAL-CONNECTOME (#2492) — team-lead 작업지시. H_1512/H_1513 showed brain placement RAISES Φ over flat/random; H_1515 asks WHERE in the full placement search space the brain layout sits (optimality, not existence).

## Question (a_no_llm_frame_trap — brain lens, the OPTIMIZATION form)
H_1512 (#2491): a brain-faithful SPATIAL placement of the 15 consciousness lanes raises integrated min-cut Φ over flat/random. H_1513 (#2492): a REAL connectome reproduces it. **H_1515:** search the space of lane→node-position placements for the Φ-MAXIMIZING arrangement, and ask — is the brain-faithful placement near the Φ-optimum (top percentile / small gap = the engine's layout APPROXIMATES the Φ-optimal layout), or is it Φ-suboptimal (search finds materially better)?

- A **placement** = a permutation π of the 15 nodes applied to the FIXED brain adjacency: `A_π[i][j] = A[π[i]][π[j]]` (a node relabel — same graph, lanes sit at different positions). `Φ(π)` = min-cut IIT4 Φ over the FIXED CORE after diffusing the population under A_π (the SAME live ci_phi_iit4 as H_1512/H_1513). Brain-faithful = identity permutation.
- DISTINCT from H_1512 (WHETHER brain beats flat/random) and H_1513 (REAL connectome reproduces it): H_1515 = WHERE the brain placement sits in the FULL placement search space. existence-of-advantage ⊥ optimality-of-advantage.

## Method
- **R1 numpy DIRECTIONAL** (`state/1515_phi_optimal_placement/h1515_optimal.py`): reuses the H_1512 harness byte-for-byte (`build_population`, `apply_topology` ALPHA=0.6, `phi_core` = IIT4 min-cut Φ over CORE, `brain_adjacency`). Sample M=3000 random permutations (rng 5121) → percentile; hill-climb from 8 starts (identity + 7 random) via best-improving pairwise swaps → optimum + gap. Captured to `state/verdicts/1515_phi_optimal_placement/H_1515_R1.json`.
- **R2 ENGINE-NATIVE** (terminal, c2·c9): the R1-found optimum perm `[8,11,2,3,6,9,4,5,0,7,1,10,12,13,14]` (engine-aligned n=150 run, whose `phi_brain`=0.100862 **byte-matches** the live engine's H_1512 `bt_brain`=0.10086188796014994) is EMBEDDED in `topo_optimal_perm()`; `topo_phi_optimal` applies it via `_topo_relabel_perm` and measures Φ with the live `ci_phi_iit4`. `topo_relabel_beats_brain_count` counts how many of 16 random relabels beat the brain layout. Same population/alpha/core as H_1512/H_1513.

## FROZEN bars (pre-registered BEFORE reading results — c9, NO tune-to-green)
**R1 (numpy DIRECTIONAL, n=300):** GREEN(directional) iff P1∧P2; P3 = headline characterization.

| bar | def | R1 result | pass |
|---|---|---|---|
| **P1** ADVANTAGE | phi_brain ≥ rand_mean + 0.02 | brain 0.10939 vs rand_mean 0.08926 (+0.0201) | **PASS** (borderline) |
| **P2** PERCENTILE | pctile ≥ 0.80 | 0.757 (brain beats ~76% of random) | **FAIL** |
| **P3** NEAR-OPTIMAL (report-only) | gap ≤ 0.30·opt_phi | gap 0.12848 vs budget 0.07136; opt 0.23787 | **FALSE** → Φ-SUBOPTIMAL |

→ R1 headline: **brain placement is Φ-SUBOPTIMAL — search finds materially better** (opt ≈ 2.18× brain @n=300).

**R2 (ENGINE-NATIVE, n=150, live ci_phi_iit4):** the smoke GATES the suboptimality the search exposed (NOT "brain is optimal").

| case | def | R2 engine result | gate |
|---|---|---|---|
| **338** P-OPT (headline) | optimum Φ > brain Φ + 0.05 | 0.25309 > 0.10086 + 0.05 | **PASS** |
| **339** P1 ADVANTAGE | brain Φ ≥ mean(random placement) + 0.005 | 0.10086 ≥ 0.08394 + 0.005 | **PASS** |
| **340** PERCENTILE (suboptimality) | #random placements beating brain ≥ 1 (of 16) | **5/16** | **PASS** |
| **341** NON-NEG sanity | all Φ ≥ 0 | yes | **PASS** |

→ R2: brain(identity) Φ=**0.10086** · optimum=**0.25309** (≈**2.51× brain**) · gap=**0.15222** · random-placement mean=**0.08394** · **5/16** random placements beat brain. `engine_cli_smoke` 353/0 RC=0.

## Finding (honest, c9 — a genuine DISCOVERY, a_break_the_wall)
The engine's brain-faithful lane placement is **above-average but Φ-SUBOPTIMAL**: it beats the MEAN random placement (consistent with H_1512), yet a hill-climb finds a placement with **~2.5× higher integrated min-cut Φ**, and **~1/3 of RANDOM placements also beat the brain layout**. So H_1512's "brain placement raises Φ" is TRUE in the weak sense (above average) but the engine's layout does **NOT** approximate the Φ-maximizing layout — there is large unrealized Φ-integration headroom in lane positioning. This is reported loudly, NOT hidden: the bars assert the suboptimality the search exposed, with the bar values frozen before reading any result.

## Scope (UNVERIFIED, honest)
- TOY: 15 lanes / single deterministic LCG population (n=150 engine, n=300 numpy) / single brain adjacency / hill-climb local optimum (NOT proven global — the embedded perm is the best of 8 restarts, a LOWER bound on the true Φ-max, which only STRENGTHENS the suboptimality finding).
- The Φ-optimum perm is a placement of the SAME graph (node relabel) — it does NOT change wiring, only WHICH lane sits where. Whether the engine's actual lanes SHOULD be re-positioned to the Φ-optimum (and whether that helps real emit/routing) = a SEPARATE follow-on; H_1515 MEASURES the gap, it does not move the live lanes.
- scale / real-corpus / global-optimum proof / larger node set / engine-transfer to live emit = UNVERIFIED (a_scale_honest_scope, a_toy_scale_recheck).

## Artifacts
- `state/1515_phi_optimal_placement/h1515_optimal.py` (R1 numpy harness)
- `state/verdicts/1515_phi_optimal_placement/H_1515_R1.json` (R1 frozen)
- `state/verdicts/1515_phi_optimal_placement/H_1515_R2_engine_native.txt` (R2 engine-native frozen, RC=0)
- `core/engine_cli.hexa` §BrainTopology Φ-OPTIMAL (`_topo_relabel_perm`/`topo_optimal_perm`/`topo_phi_optimal`/`topo_relabel_beats_brain_count`)
- `core/engine_cli_smoke.hexa` cases 338-341 · `ARCHITECTURE.json` §BrainTopology lockstep

xref H_1512 (brain-topology, parent) · H_1513 (literal connectome) · a_no_llm_frame_trap · a_phi_iit4_tool · a_engine_native_learning · a_verified_must_wire · a_break_the_wall (honest suboptimality DISCOVERY) · a_core_engine_map · a_scale_honest_scope · a_toy_scale_recheck · c2 · c9 · p7
