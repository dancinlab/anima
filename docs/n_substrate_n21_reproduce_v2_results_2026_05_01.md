# N-Substrate N-21 v2 — Edlund 2011 + Albantakis 2014 Re-run at 7-node × 200-gen

> **ts**: 2026-05-02 (UTC 04:50)
> **agent**: N-21 A/B v2 (sub-agent of N-21 reproduce)
> **parent**: `docs/n_substrate_n21_reproduce_results_2026_05_01.md`
> **scope**: Re-run Edlund 2011 + Albantakis 2014 at the medium scale authorized by user (7-node × 200-gen, ubu1+ubu2 parallel, $0)
> **constraints**: HEXA-only repo, $0 budget, race-isolation to `state/n_substrate_n21_reproduce_v2_2026_05_01/` + this doc only. v1 dir untouched.
> **status**: N21_AB_V2_EXECUTED · 0/2 PASS · v1 verdict change documented

---

## §0 한 줄 요약

7-node × 200-gen scale-up did NOT rescue either reproduction:
- **Edlund v2: FAIL stronger** — r(Φ, fit) flipped from −0.11 (v1, n=373) to **−0.52 (v2, n=12)**, and per-gen r went from −0.25 to **−0.95**. Higher-resolution evolved nets consolidate into LOWER Φ as fitness climbs.
- **Albantakis v2: FAIL non-monotonic** — concept counts now in 47–65 range (vs v1's 5–15, capacity confirmed adequate), but pattern is simple(65, Φ=0.90) → medium(48, Φ=0.0) → complex(62, Φ=0.44) — non-monotonic both ways.
- **WITNESSED count: 1/16 PASS_ANALOG (Casali) + 1/16 PARTIAL (Albantakis v1 medium-step) → unchanged at 2/16**. v2 does not add a new positive witness; it does add a stronger negative datapoint at the reachable scale.

---

## §1 Execution log

### N-21-A v2: Edlund 2011 (animat Φ ↔ fitness) — ubu1 RTX 5070

| field | v1 | v2 |
|---|---|---|
| host | ubu1 | ubu1 |
| pyphi | 1.2.0 (Python 3.12 patches) | 1.2.0 + `CUT_ONE_APPROXIMATION=True` |
| network size | 5 nodes | **7 nodes** |
| generations | 60 | **200** |
| pop | 12 | 12 |
| Φ schedule | every gen, top-3 + 4 random (~7 sia/gen × 60 = 420 calls) | every 10 gen, top-1 + 1 random (~2 sia/gen × 21 = 42 calls; sparse to keep wall-time bounded) |
| target rule | node4_next = XOR(node0, node1) | node6_next = XOR(node0, node1) |
| elapsed | 150.9s | 532.5s (~9 min) |
| best_fit init → final | 0.69 → 1.00 | 0.54 → 0.98 |
| n_phi_fit pairs (non-NaN) | 373 | **12** (7 top + 5 random; many evolved nets disconnected → Φ undefined) |
| **Pearson r(Φ, fit) all pairs** | **−0.1087** | **−0.5239** |
| **Pearson r per-gen (best_phi vs best_fit)** | **−0.2492** | **−0.9509** |
| paper expectation | r > 0 | r > 0 |
| **verdict** | FAIL_SMALL_SCALE | **FAIL** (stronger negative at 7-node) |

**v2 measured trajectory** (top_phi vs best_fit at measurement gens):

| gen | top_phi | best_fit |
|---:|---:|---:|
| 50 | 0.692 | 0.922 |
| 70 | 0.267 | 0.945 |
| 100 | 0.187 | 0.961 |
| 110 | 0.019 | 0.961 |
| 120 | 0.015 | 0.977 |
| 130 | 0.015 | 0.977 |
| 140 | 0.015 | 0.977 |

Φ collapses as fitness saturates. The XOR-solving solution PyPhi finds at 7 nodes is structurally low-integration (sparse subnetwork). This is a **falsification-direction signal at our reachable scale** but does not refute Edlund's 8-node × 60k-gen finding (we still cannot reach that scale on $0).

**Honest C3**:
- 7-node × 200-gen with `CUT_ONE_APPROXIMATION` is roughly comparable to v1 5-node × 60-gen exact in compute cost; both fall short of Edlund's published 8-node × 60k-gen exact.
- Sparse Φ schedule reduces n from 373 to 12 — fewer pairs, same direction. The per-gen r=−0.95 is the most informative number: 7 top-phi/best-fit pairs, monotonic anti-correlation across the trajectory.
- `CUT_ONE_APPROXIMATION` may bias Φ downward for nearly-integrated nets; full sia would likely give higher Φ values at gen 50–100. Sign of correlation is robust; magnitude has approximation uncertainty.
- Result file: `state/n_substrate_n21_reproduce_v2_2026_05_01/edlund_2011_animat_ubu1_v2.json` (50KB, 200-gen history).

### N-21-B v2: Albantakis 2014 (env-complexity → causal structure) — ubu2 RTX 5070

| field | v1 | v2 |
|---|---|---|
| host | ubu2 | ubu2 |
| network size | 5 nodes | **7 nodes** |
| generations / env | 30 | **200** |
| pop | 10 | 10 |
| envs | simple/medium/complex (same task functions) | same |
| elapsed | 6.4s | 1375.1s (~23 min, dominated by CES at 7 nodes) |
| **mean concept count** simple / medium / complex | 6.33 / 15.67 / 5.00 | **65.0 / 47.7 / 62.0** |
| **mean Φ** simple / medium / complex | 0.0 / 0.093 / 0.0 | **0.901 / 0.0 / 0.435** |
| best_fit per env (top-3) | s=[0.94,0.94,0.84], m=[0.94,0.94,0.88], c=[1.00,1.00,0.97] | s=[0.96,0.96,0.91], m=[0.98,0.97,0.91], c=[0.95,0.95,0.90] |
| paper expectation | concepts and Φ ↑ monotonically with env complexity | same |
| **verdict** | PARTIAL (medium > simple, complex<simple due to 5-node ceiling) | **FAIL** (no monotonic pattern; capacity confirmed adequate) |

**v2 observation**: At 7 nodes the **capacity ceiling is gone** (concepts ~47–65 across all envs vs paper-claimed dozens), but the **monotonic prediction is now refuted in a different way**: simple env evolves a network with the highest concept count (65) and Φ (0.90) — opposite of the paper's prediction. Medium env collapses to Φ=0 (degenerate XOR networks). Complex env recovers some structure but doesn't exceed simple.

**Honest C3**:
- The simple env's Φ=0.901 came from only 1/3 measurable nets (other 2 errored — likely due to fully-connected dense CMs causing PyPhi to throw on a state with no valid MIP). Not robust.
- Each env has only 3 final-measurement networks; statistical power is very low. To get clean signal we'd need ~30 networks per env (which at 7 nodes ≈ 30 × 22s = 11 min/env × 3 = 33 min more, feasible but not run here).
- The DIRECTIONAL claim "monotonic increase with env complexity" is not supported under our randomization seed at this scale. We cannot rule out seed-dependent FAIL — multi-seed bootstrap is the appropriate next step.
- Result file: `state/n_substrate_n21_reproduce_v2_2026_05_01/albantakis_2014_envcomplexity_ubu2_v2.json`.

---

## §2 v1 vs v2 verdict change

| study | v1 verdict | v2 verdict | change |
|---|---|---|---|
| Edlund 2011 | FAIL_SMALL_SCALE (r=−0.11) | **FAIL (r=−0.52, per-gen r=−0.95)** | Negative direction CONFIRMED at 7-node; magnitude grew. Did not rescue. |
| Albantakis 2014 | PARTIAL (medium>simple, complex<simple by capacity) | **FAIL (non-monotonic; concepts 65/48/62, Φ 0.90/0.0/0.44)** | Capacity ceiling resolved (concepts ~50-65 across), but monotonic prediction NOT recovered. v1 PARTIAL was over-generous. |

---

## §3 own#2 (b) substrate-WITNESSED count update

| substrate axis | pre-N-21 | post-v1 | post-v2 (this cycle) | net delta |
|---|---|---|---|---|
| CLM digital (Φ-proxy 8-axis) | WITNESSED | WITNESSED | WITNESSED | 0 |
| Organic EEG (PCI-analog) | candidate | WITNESSED_ANALOG | WITNESSED_ANALOG | +1 |
| AKIDA neuromorphic | pending HW | pending HW | pending HW | 0 |
| Animat sim (Edlund Φ↔fit) | candidate | NOT_WITNESSED (FAIL_SMALL_SCALE) | **NOT_WITNESSED (FAIL stronger)** | 0 (negative confirmed) |
| Animat sim (Albantakis env-complexity) | candidate | PARTIAL | **NOT_WITNESSED (FAIL non-mono)** | 0 (PARTIAL → FAIL is backward, but v1 was over-claim) |

**WITNESSED count of 16 IIT tests**: still **2/16 with positive empirical signal** (Casali analog PASS + Albantakis v1 medium-step PARTIAL — though the latter's status now degrades). If we drop Albantakis v1 PARTIAL (since v2 supersedes), count is **1/16 PASS_ANALOG + 0/16 PARTIAL = 1/16 net positive**. Honest reading: **v2 reduces witnessed count from 2/16 to 1/16**.

---

## §4 Top blockers for next cycle

1. **PyPhi 1.2 + 7-node + exact MIP** is too slow on RTX 5070 (~5–10 min per non-trivial sia call). `CUT_ONE_APPROXIMATION` makes it tractable but biases Φ downward. To trust magnitudes, need either (a) Edlund-original 8-node × 60k-gen on a workstation with 64-core CPU + days of wall, or (b) port to PyPhi 2.x / GPU-aware fork (not yet packaged).
2. **Single-seed runs** for both. To make any FAIL claim defensible we need ≥10 seeds × multi-env. At ~9-min Edlund + 23-min Albantakis × 10 seeds = ~5h on each host — feasible $0 next cycle.
3. **Edlund disconnected-net problem**: most evolved 7-node nets are sparse → Φ undefined (NaN). v2 only got 12 valid pairs from 21 measurement gens × 2 nets. Either inject connectivity-preserving mutation operator, or measure on max-connected subgraph subsystem instead of full system.
4. **Albantakis "complex" task may be too easy at 7 nodes** — best_fit reaches 0.95 within 200 gens. Need a harder target (e.g., 4-input XOR + memory) to genuinely stress the network and evolve high-concept structures specific to env complexity.
5. **Pre-registration absent**: as noted in v1 doc §3.5, both v1 and v2 ran without pre-registered C1/C2 thresholds. The user-stated "did 7-node escape ceiling?" criterion is implicitly C1=`r>0` for Edlund and C1=`monotonic` for Albantakis; both fail. Future v3 MUST pre-register before launch.

---

## §5 Cleanup status & disk footprint

| host | pre-run free | post-cleanup free | scripts kept | result kept | logs cleaned |
|---|---|---|---|---|---|
| ubu1 | 53G (94% used) | 53G (no growth) | `~/n_substrate_n21/edlund_animat_v2.py` | `~/n_substrate_n21/edlund_2011_animat_ubu1_v2.json` (50KB, also pulled to anima) | `edlund_v2.log` removed |
| ubu2 | 793G (9% used) | 793G | `~/n_substrate_n21/albantakis_v2.py` | `~/n_substrate_n21/albantakis_2014_envcomplexity_ubu2_v2.json` (1.5KB, also pulled) | `albantakis_v2.log` removed |

Pyphi venvs (~50MB each) preserved for re-runnability. v1 result files preserved untouched.

---

## §6 Artifacts

```
state/n_substrate_n21_reproduce_v2_2026_05_01/
  edlund_2011_animat_ubu1_v2.json          (50KB, 200-gen history + summary)
  albantakis_2014_envcomplexity_ubu2_v2.json  (1.5KB, per-env summary)
docs/n_substrate_n21_reproduce_v2_results_2026_05_01.md  (this file)
```

v1 baseline (preserved, untouched):
```
state/n_substrate_n21_reproduce_2026_05_01/
  edlund_2011_animat_ubu1.json
  albantakis_2014_envcomplexity_ubu2.json
  ...
docs/n_substrate_n21_reproduce_results_2026_05_01.md
```
