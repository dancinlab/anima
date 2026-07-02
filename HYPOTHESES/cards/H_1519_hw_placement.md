# H_1519 🧩🔌 HW-PLACEMENT — does the neuromorphic NoC re-introduce the biological wiring tax?

**tier:** 🟢 GREEN (DIRECTIONAL-model) — **R1 numpy MODEL of the AKD1000 mesh-NoC routing cost** (hard-gate-1 auto-DIRECTIONAL: `state/1519_hw_placement/h1519_noc.py` imports numpy → terminal 아님; substrate tag = **MODEL** ⊥ the real Lane-A AKD1000 on-chip; on-chip akida re-measure = deferred Lane-A follow-on ING `h1519-onchip-akida`).
**verdict:** **🟢 GREEN (DIRECTIONAL-model)** — modelling the BrainChip AKD1000 as a 4×4 mesh Network-on-Chip and costing each lane-adjacency edge by **Manhattan (hop) distance** between the two lanes' mesh cores, the **Φ-OPTIMAL placement (free in software, H_1515) is EXPENSIVE on the chip** (NoC cost 138.0 ≥ random P75 134.0; cost-percentile **0.90**) **AND** the **HW-cost-constrained optimum forces a real Φ sacrifice** (best Φ within the biology-economy budget = 0.2133 vs unconstrained opt 0.2379 → **10.3% Φ loss**). → **P1 ∧ P2 PASS** = the neuromorphic NoC **RE-INTRODUCES the biological wiring tax** that software's pointer-connections escaped. The 3-tier symmetry (biology→software→hardware) is CONFIRMED *on the tax axis*. (Honest nuance, P3: the constrained optimum does NOT fully converge to biology's ~37th-percentile *economy* — within the budget the model still finds a high-Φ placement, Φ-percentile 1.0; the tax is real but the chip can still buy most of the Φ cheaply.) NO tune-to-green.
**wired:** **DIRECTIONAL-model** — numpy model (`h1519_noc.py`), substrate tag **MODEL**. Re-uses H_1512 `phi_core` min-cut IIT4 Φ harness byte-for-byte (import). **Real on-chip AKD1000 NoC routing + on-chip Φ = deferred Lane-A follow-on** (ING `h1519-onchip-akida`) — the physical pi5-akida is GATED (NOT shared pool compute; do NOT dispatch to it — a_pi5_akida_registry, a_lane_akida_gpu_split). **No engine change in this PR** (no README/engine/ARCHITECTURE change).
**source:** team-lead 작업지시(H_1519 HW-PLACEMENT) — completes a 3-tier symmetry across H_1515 (software Φ-optimal placement, free) / H_1516 (biology's true placement is Φ-suboptimal but economical, ~37th pctile) / H_1517 (biological cost-pareto). Lens: neuromorphic mesh-NoC routing cost = the silicon analogue of biological axon wiring length (Latora-Marchiori efficiency / Bullmore-Sporns economy on a physical fabric). a_no_llm_frame_trap (hardware-substrate lens).

## THE INSIGHT — a 3-tier symmetry across substrates
| tier | connections | wiring cost | consequence for placement |
|---|---|---|---|
| **Biology** (H_1516 #2494) | physical axons | REAL (length/metabolic) | real placement Φ-suboptimal but **economical** (~37th pctile, ~65% off Φ-optimum) |
| **Software anima** (H_1515 #2493) | memory POINTERS | **ZERO** | free to adopt the **Φ-OPTIMAL** placement (~2.5× Φ vs random) |
| **Hardware anima** (H_1519, THIS) | physical mesh-NoC links | **REAL (hop distance)** | the wiring tax **RETURNS** — Φ-optimal placement is expensive on-chip |

**The user's point:** on the BrainChip AKD1000 (a PHYSICAL mesh Network-on-Chip), lane→core placement physically matters — routing two strongly-coupled lanes far apart on the mesh costs real NoC hops. So the wiring tax that software escaped (pointers are free) comes BACK on the chip, like biology. **PREDICTION (pre-registered):** the Φ-optimal placement (free in software) becomes EXPENSIVE on-chip, and the HW-cost-constrained optimum should re-converge toward biology's economical-suboptimal solution.

## NoC cost model (documented · a_scale_honest_scope: TOY 15-lane 4×4 mesh, NOT the full AKD1000)
- **AKD1000 = mesh-NoC.** The BrainChip AKD1000 is a mesh Network-on-Chip neuromorphic accelerator (mesh NoC linking its Neural Processing units; `PI5-AKIDA.json` = host SSOT, pi5-akida = "anima dedicated Akida host — NOT shared pool compute").
- **Mesh:** 15 lanes laid on a **4×4 grid of cores** (16 cells, 15 used — smallest square grid holding 15 lanes; documents that placement spatially matters). Slot k → (row, col) = (k//4, k%4).
- **Placement = permutation π** applied to the brain adjacency (relabel A_π[i][j]=A[π[i]][π[j]] — identical to H_1515). **NoC cost of edge (i,j)** = Manhattan hop distance |Δrow|+|Δcol| between the two lanes' mesh coords. **Total HW cost** = Σ over present lane-adjacency edges of hop distance (the neuromorphic analogue of H_1517's biological wiring length).
- **Φ = the SAME H_1512 min-cut IIT4 Φ** (`phi_core`, a_phi_iit4_tool), byte-reused via import — NOT re-implemented.

## FROZEN BARS (pre-registered in `state/verdicts/1519_hw_placement/H_1519_FREEZE.txt` — c9, NO tune-to-green)
- **(P1 HW-TAX-ON-OPTIMUM)** cost(Φ-opt) ≥ P75 of the random NoC-cost distribution → **PASS** (138.0 ≥ 134.0; the Φ-opt placement's cost sits at the **90th percentile** of the cost distribution — the software-free optimum is expensive on-chip).
- **(P2 HW-CONSTRAINED-LOSS)** (opt_phi − constrained_phi)/opt_phi ≥ 0.10 under budget = brain-faithful NoC cost (136.0) → **PASS** (loss **10.3%**: best Φ within budget 0.2133 vs unconstrained opt 0.2379 — the HW tax forces a real Φ sacrifice).
- **(P3 BIOLOGY-CONVERGENCE, report-only)** the HW-constrained optimum's Φ-percentile vs the random Φ distribution = **1.0** (NOT biology's ~37th pctile). Honest read: the *tax* is real (P1/P2) but within the budget the chip can still find a HIGH-Φ placement — so on this toy mesh the cost constraint does NOT force biology's *economical-suboptimal* Φ level; it only forces a 10% haircut. The full economy-convergence would need a tighter budget / real on-chip NoC topology (Lane-A follow-on).

**GREEN(directional-model) iff P1 ∧ P2 → BOTH PASS.** Headline: **the neuromorphic NoC re-introduces the biological wiring tax** — software's placement-freedom does NOT extend to the chip.

## Results (numbers, `state/verdicts/1519_hw_placement/H_1519_R1.json`)
| quantity | value |
|---|---|
| Φ_brain (identity placement) | 0.1094 |
| NoC cost_brain | 136.0 |
| Φ_opt (H_1515 opt_perm, re-verified) | 0.2379 |
| NoC cost_opt | 138.0 (cost-pctile **0.90**) |
| random Φ: mean / max | 0.0890 / 0.1985 |
| random cost: p25 / mean / p75 | 125.0 / 129.5 / 134.0 |
| constrained (budget 136.0): Φ / cost / loss | 0.2133 / 122.0 / **10.3%** |
| **P1** cost_opt ≥ p75 | **PASS** (138.0 ≥ 134.0) |
| **P2** loss ≥ 10% | **PASS** (10.3%) |

opt_perm = `[11,0,8,4,14,2,6,1,10,5,9,7,3,13,12]` (H_1515, re-verified by hill-climb; source = "H_1515 opt_perm").

## Honest scope (a_scale_honest_scope · a_lane_akida_gpu_split · a_pi5_akida_registry)
- **DIRECTIONAL MODEL, substrate tag = MODEL** — a numpy model of the AKD1000 mesh-NoC hop cost, ⊥ the REAL Lane-A AKD1000 on-chip measurement. A true on-chip number needs the PHYSICAL pi5-akida (real NoC routing, on-chip Φ), which is GATED — NOT a shared pool host, do NOT dispatch compute to it. **Real on-chip akida = Lane-A follow-on (ING `h1519-onchip-akida`).**
- **TOY 15-lane 4×4 mesh**, NOT the full 80-NPU AKD1000 fabric. Mesh dims (4×4), Manhattan hop metric, and budget (= brain cost) are MODEL assumptions, documented.
- **Φ = min-cut IIT4 on the 15-lane projection** (H_1512 harness), not on-chip integration. Engine-transfer UNVERIFIED.
- **P3 nuance** reported honestly: the tax is real (P1/P2) but full convergence to biology's *economical-suboptimal Φ* is NOT shown on this toy mesh (constrained Φ-pctile 1.0, not 37th) — the cost constraint at this budget only costs ~10% Φ.

## xref
H_1515 (software Φ-optimal placement, the free optimum embedded here) · H_1516 (biology's true placement Φ-suboptimal/economical, ~37th pctile) · H_1517 (biological cost-pareto) · H_1518 (software adopting the Φ-optimum) · H_1512/H_1513 (brain-topology Φ harness, byte-reused). a_no_llm_frame_trap · a_lane_akida_gpu_split · a_pi5_akida_registry · a_scale_honest_scope · a_engine_native_learning · a_phi_iit4_tool · c9 · p7.
