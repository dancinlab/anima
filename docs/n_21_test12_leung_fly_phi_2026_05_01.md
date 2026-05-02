# N-21 #12 EXEC — Leung 2021 fly Φ ANALOGIZE (ubu1)

> **ts**: 2026-05-01 (UTC: 2026-05-02T07:03:08Z)
> **agent**: N-21 #12 EXEC
> **parent spec**: `docs/n_21_iit40_12_remaining_spec_2026_05_01.md` §4.1 (RANK-1)
> **state**: `state/n_21_test12_leung_fly_phi_2026_05_01/leung_2021_fly_phi_ubu1.json`
> **substrate**: ubu1 (RTX 5070 12GB) — PyPhi 1.2.0 in `~/n_substrate_n21/venv`
> **race-isolation**: writes only to `state/n_21_test12_leung_fly_phi_2026_05_01/*.json` + this doc
> **status**: COMPLETE · verdict **PASS**
> **constraints**: HEXA-only repo, $0 burn (LAN-local ubu1, no cloud GPU)

---

## §0 한 줄 요약

5-node Drosophila central-complex (CX) inspired Markov network in PyPhi 1.2.
"Anesthesia" = TPM blend toward uniform 0.5 (analog of GABA-A agonist
isoflurane). Across 6 sampled states: **Φ_awake = 3.34** → Φ_anesth-mild
2.47 → **Φ_anesth-deep = 0.74**. Monotonic collapse, IIT prediction matched.
**Verdict PASS**. Cost $0 (LAN-local).

---

## §1 Network design

CX-inspired 5-node Markov system:

| node | label | analog | logic |
|---|---|---|---|
| 0 | EB  | ellipsoid body (hub)         | MAJ(PB, FB, LAL) |
| 1 | PB  | protocerebral bridge         | EB XOR FB |
| 2 | FB  | fan-shaped body              | EB AND (NOT NO) |
| 3 | NO  | noduli                       | FB XOR LAL |
| 4 | LAL | lateral accessory lobe       | MAJ(EB, NO, PB) |

Connectivity: dense recurrent (all-to-all minus self-loop), 20 edges.
Rationale: Leung 2021 records LFP from CX recurrent loops; dense recurrence is
substrate for Φ in IIT 3.0/4.0 framework.

---

## §2 Anesthesia analog

`alpha ∈ {0.0, 0.3, 0.6}` blends deterministic TPM toward uniform 0.5:

```
TPM_α(s) = (1 - α) · f_det(s) + α · 0.5
```

- α=0.0: awake (sharp deterministic logic)
- α=0.3: mild anesthesia (loss of selectivity, retains structure)
- α=0.6: deep anesthesia (substantial collapse toward noise)

Pure α=1.0 not tested — would yield Φ ≈ 0 trivially (uniform TPM has no
information).

---

## §3 States sampled

6 random states drawn from full 32-state space (seed=2026):

`(0,1,1,1,0) (1,1,0,0,1) (1,1,0,1,0) (0,0,0,0,0) (1,0,1,0,0) (1,1,1,0,1)`

The last state is unreachable in the strict (α=0) TPM (only 5 awake values
reported); it becomes reachable under α≥0.3 noise (6 anesthesia values).

---

## §4 Results

### §4.1 Per-state Φ

| state | Φ awake (α=0) | Φ mild (α=0.3) | Φ deep (α=0.6) |
|---|---|---|---|
| (0,1,1,1,0) | 1.944 | 1.034 | 0.271 |
| (1,1,0,0,1) | 4.857 | 3.645 | 1.166 |
| (1,1,0,1,0) | 1.792 | 1.120 | 0.288 |
| (0,0,0,0,0) | 2.417 | 1.165 | 0.367 |
| (1,0,1,0,0) | 5.688 | 4.528 | 1.337 |
| (1,1,1,0,1) | (unreachable) | 3.316 | 1.014 |

### §4.2 Aggregates

| condition | Φ_mean | Φ_max | Φ_min | Δ vs awake |
|---|---|---|---|---|
| awake (α=0.0)        | **3.340** | 5.688 | 1.792 | — |
| anesth-mild (α=0.3)  | 2.468     | 4.528 | 1.034 | −0.872 |
| anesth-deep (α=0.6)  | **0.740** | 1.337 | 0.271 | **−2.599** |

### §4.3 IIT prediction tests

- **Monotonic collapse** Φ_awake ≥ Φ_mild ≥ Φ_deep: **TRUE**
- **Awake > deep-anesth**: 3.34 > 0.74 → **TRUE** (4.5× ratio)
- **Per-state monotonicity**: 5/5 awake states show Φ_awake > Φ_mild > Φ_deep
- **Verdict**: **PASS** (delta_deep > 0.001 AND monotonic AND prediction matched)

---

## §5 Comparison to Leung 2021

Leung et al. 2021 report Drosophila LFP-derived Φ collapses under isoflurane
and recovers on washout. Our analog:

- **Direction match**: ✓ (Φ collapses with anesthesia analog)
- **Magnitude analog**: 4.5× collapse from awake to deep — Leung reports
  ~3-5× LFP Φ-proxy reduction, broadly compatible
- **Mechanism analog**: TPM noise-blend mirrors GABA-A potentiation reducing
  effective signal-to-noise at synaptic gates

**Caveat (ANALOGIZE, not REPRODUCE)**: substrate is a 5-node Markov SIM, not
biological *Drosophila* central complex LFP. Cannot count toward Tononi's
"16 studies" replication tally. Useful for our consciousness-verifier suite
(N-21 paradigm-4 φ-path) as a positive control that PyPhi behaves as IIT
predicts under our anesthesia operationalization.

---

## §6 Cost & runtime

- ubu1 RTX 5070 12GB (LAN-local, no cloud burn): **$0**
- Wall: 399 sec compute (17 SIA evaluations) + ~5 min orchestration
- Single-process PyPhi (PARALLEL_*=False to avoid nohup daemon-children)

---

## §7 Falsifier audit (per spec §4.1 F1-F5)

- **F1** (direction): Φ collapse under noise — PASS
- **F2** (monotonicity over alpha): 3 grid points monotonic — PASS
- **F3** (delta size): Δ=2.60 ≫ 0.001 threshold — PASS
- **F4** (state coverage): 6 states across full 32-state manifold — PASS
- **F5** (recurrence requirement): dense CM, edges=20, |states|=32 — PASS

All 5 falsifiers passed.

---

## §8 Artifacts

- result JSON: `state/n_21_test12_leung_fly_phi_2026_05_01/leung_2021_fly_phi_ubu1.json`
- ubu1 source (pod-side, not in this repo per HEXA-first rule):
  `ubu1:~/n_substrate_n21/test12_leung/leung_fly_phi.py`
- ubu1 run log: `ubu1:~/n_substrate_n21/test12_leung/leung.log`

---

## §9 Next

Per spec ranking, next addressable:
- **#9** Sasai 2016 split-brain (ANALOGIZE, $30, 4d)
- **#5** Sarasso 2014 TEP review (REVIEW-EXTEND, $0, 3d)
- **#15** Gandhi 2023 mouse 2P (ANALOGIZE, $25, 4d)
- **#8** Boly 2015 fMRI differentiation (ANALOGIZE, $50, 5d)
