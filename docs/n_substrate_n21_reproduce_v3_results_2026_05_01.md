# N-Substrate N-21 v3 — Edlund 2011 + Albantakis 2014 10-seed bootstrap with pre-registration

> **ts**: 2026-05-02 (UTC TBD on completion)
> **agent**: N-21 v3 10-seed bootstrap
> **parent**: `docs/n_substrate_n21_reproduce_v2_results_2026_05_01.md`
> **scope**: 10-seed bootstrap × Edlund + Albantakis at 7-node × 200-gen, with connectivity-preserving mutation (Edlund) and pre-registered C1 thresholds (frozen 2026-05-02T05:03:28Z, BEFORE compute launch).
> **constraints**: HEXA-only repo, $0 budget, race-isolation to `state/n_substrate_n21_reproduce_v3_2026_05_01/` + this doc. v1+v2 dirs untouched.
> **status**: TO BE FILLED ON COMPLETION

---

## §0 한 줄 요약

TBD on completion.

---

## §1 Pre-registration (frozen 2026-05-02T05:03:28Z)

C1 thresholds were frozen and committed to `state/n_substrate_n21_reproduce_v3_2026_05_01/c1_preregister.json` BEFORE any compute was dispatched. Per v2 §4 blocker #5 (pre-registration absent in v1/v2), v3 enforces the sequence:

1. Write `c1_preregister.json` with PASS/FAIL/INCONCLUSIVE criteria + rationale + timestamp.
2. Verify file present on disk.
3. Then and only then dispatch ubu1 + ubu2 workers.

### Edlund 2011 thresholds
- **PASS**: mean Pearson r(Φ, fit) ≥ +0.30, two-sided p < 0.05 across ≥10 seeds, AND ≥7/10 seeds individually have r > 0
- **FAIL**: mean r ≤ −0.30, p < 0.05, AND ≥7/10 seeds have r < 0 (= IIT prediction reversed)
- **INCONCLUSIVE**: |mean r| < 0.30 OR std(r) > 0.5 OR <7/10 seeds agree on sign OR p ≥ 0.05

### Albantakis 2014 thresholds
- **PASS**: monotonic concept count (simple < medium < complex) in ≥7/10 seeds AND no env collapse (mean concepts ≥5 per env)
- **FAIL**: non-monotonic in ≥7/10 seeds OR env collapse in ≥7/10 seeds
- **INCONCLUSIVE**: monotonic in 4–6/10 seeds (mixed)
- Auxiliary **PARTIAL_PHI_ONLY**: Φ-monotonic in ≥7/10 even when concept-count is not

---

## §2 Execution log

### N-21-A v3: Edlund 2011 (animat Φ ↔ fitness) — ubu1 RTX 5070

| field | v2 | v3 |
|---|---|---|
| seeds | 1 | **10** (1..10) |
| network size | 7 | 7 |
| generations | 200 | 200 |
| pop | 12 | 12 |
| mutation | random flip | **connectivity-preserving** (no orphan-creating flips) |
| disconnected-net handling | NaN | **largest-connected-subgraph fallback (≥3 nodes)** |
| Φ schedule | every 10 gen, top-1 + 1 random | same |
| approximation | CUT_ONE | CUT_ONE |
| **mean r(Φ, fit) across seeds** | n/a (single seed −0.52) | TBD |
| **std r across seeds** | n/a | TBD |
| **n seeds with r > 0** | n/a | TBD |
| **fisher combined p** | n/a | TBD |
| **C1 verdict** | n/a | TBD |

#### Per-seed table
TBD — populated from `edlund_2011_animat_ubu1_v3.json`.

### N-21-B v3: Albantakis 2014 (env-complexity → causal structure) — ubu2 RTX 5070

| field | v2 | v3 |
|---|---|---|
| seeds | 1 (seed=7) | **10** (101..110) |
| network size | 7 | 7 |
| generations / env | 200 | 200 |
| pop | 10 | 10 |
| mutation | random flip | **connectivity-preserving** |
| **n seeds monotonic concepts** | n/a | TBD |
| **n seeds monotonic Φ** | n/a | TBD |
| **n seeds no env collapse (≥5 concepts)** | n/a | TBD |
| **C1 verdict** | n/a | TBD |

#### Per-seed table
TBD — populated from `albantakis_2014_envcomplexity_ubu2_v3.json`.

---

## §3 Phase 3: CUT_ONE_APPROXIMATION robustness

Scope: 1 seed × Edlund × 50 gen with EXACT_MIP (CUT_ONE_APPROXIMATION=False) on ubu1 after main run completes. Compares sign of r(Φ, fit) against same-seed cut-one approximation.

| metric | cut-one (v3 seed=1) | exact-mip (50-gen probe) |
|---|---|---|
| r(Φ, fit) | TBD | TBD |
| sign | TBD | TBD |
| **sign-robust** | TBD | TBD |
| magnitude shift | TBD | TBD |

---

## §4 v1 → v2 → v3 verdict trajectory

| study | v1 | v2 | v3 |
|---|---|---|---|
| Edlund 2011 | FAIL_SMALL_SCALE (r=−0.11, n=373, single-seed 5-node) | FAIL (r=−0.52 single-seed 7-node, n=12) | TBD (10-seed bootstrap with conn-preserving mutation) |
| Albantakis 2014 | PARTIAL (medium>simple, complex<simple by 5-node ceiling) | FAIL non-mono (concepts 65/48/62 single-seed) | TBD (10-seed bootstrap) |

---

## §5 own#2(b) substrate-WITNESSED count update

| substrate axis | post-v2 | post-v3 (this cycle) | net delta |
|---|---|---|---|
| CLM digital (Φ-proxy 8-axis) | WITNESSED | WITNESSED | 0 |
| Organic EEG (PCI-analog) | WITNESSED_ANALOG | WITNESSED_ANALOG | 0 |
| AKIDA neuromorphic | pending HW | pending HW | 0 |
| Animat sim (Edlund Φ↔fit) | NOT_WITNESSED (FAIL stronger) | TBD | TBD |
| Animat sim (Albantakis env-complexity) | NOT_WITNESSED (FAIL non-mono) | TBD | TBD |

WITNESSED count of 16 IIT tests post-v2: 1/16 (Casali analog only). Post-v3 update TBD.

---

## §6 Cleanup status & disk footprint

TBD.

---

## §7 Artifacts

```
state/n_substrate_n21_reproduce_v3_2026_05_01/
  c1_preregister.json                          (frozen 2026-05-02T05:03:28Z)
  edlund_2011_animat_ubu1_v3.json              (10-seed result + history)
  albantakis_2014_envcomplexity_ubu2_v3.json   (10-seed result)
  edlund_phase3_exact_mip_ubu1.json            (sign-robustness probe)
docs/n_substrate_n21_reproduce_v3_results_2026_05_01.md  (this file)
```

v1 + v2 baselines preserved untouched.

---

## §8 Honest C3 (constraints)

- Pre-registration written and timestamped BEFORE compute dispatch (verified by file mtime + commit log).
- 7-node × 10-seed × 200-gen on ubu1 (Edlund) expected ~90 min; on ubu2 (Albantakis) expected ~230 min. Total wall-clock ≤ 5h budget.
- Connectivity-preserving mutation rejects in-place edge flips that would orphan a node; subgraph fallback marginalizes TPM over removed nodes (uniform-prior averaging) to estimate Φ on the largest connected component (≥3 nodes).
- CUT_ONE_APPROXIMATION still in use for the main 10-seed runs (sign-robust per v2; magnitude down-biased). Phase 3 EXACT_MIP probe quantifies the bias on 1 seed × 50 gen.
- Subgraph-fallback marginalization is an approximation: the "true" Φ of the connected subsystem requires the full marginal TPM under the actual upstream-driven distribution, not uniform. We document this as a v3 honest-C3 caveat.
