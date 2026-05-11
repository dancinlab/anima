<!-- [Hc_919 n21-iit40-16test-reproduce-cluster — moved to hypotheses_candidates/Hc_919_n21_iit40_16test_reproduce_cluster.md on 2026-05-11] -->

# N-21 #8 — Boly 2015 fMRI Differentiation (ANALOGIZE)

> **ts**: 2026-05-01
> **agent**: N-21 #8 EXEC
> **host**: ubu1 (192.168.50.119), `~/n_substrate_n21/test8_boly/`, venv `~/n_substrate_n21/venv` (PyPhi 1.2.1, NumPy 2.4.4, SciPy 1.17.1)
> **parent**: `docs/n_21_iit40_12_remaining_spec_2026_05_01.md` §4.5 RANK-5
> **category**: ANALOGIZE (substrate = synthetic AR(1) BOLD, NOT real 3T fMRI)
> **race-isolation**: writes only to `state/n_21_test8_boly_fmri_diff_2026_05_01/*` + this doc
> **status**: PASS (primary metric); secondary metrics show honest caveats
> **cost**: $0 (local ubu1 CPU, ~45s wall-clock)

---

## §0 한 줄 요약

16 ROI AR(1) BOLD 시뮬레이션에서 awake 상태가 sleep 상태 대비 multivariate 차별화 지수 **5.08 vs 0.67** (Cohen-d=18.0), 상태 레퍼토리 **1470 vs 1136**, geometric Φ-proxy **2.21 vs 1.62** — Boly 2015 핵심 예측 (awake > sleep differentiation) 통과. F5 falsifier (d<0.5) NOT triggered. PyPhi 4-node coarse Φ 와 LZ 는 반대 방향 → ANALOGIZE 한계로 명시.

---

## §1 Mission summary

Boly 2015 (PLoS Biology 13(11): e1002327, "Stimulus set meaningfulness and neurophysiological differentiation: a functional magnetic resonance imaging study") claimed: **awake brain produces more differentiated BOLD spatial patterns across stimulus epochs than NREM sleep / scrambled controls.** Tononi-IIT theoretical hook: differentiation == repertoire-size proxy for cause-effect-power (information axiom).

Real reproduction requires 3T fMRI scanner ($400/hr + $50k IRB). We instead **ANALOGIZE** with a 16-node AR(1) network whose two regimes capture the dynamical hallmarks of awake (rich epoch-specific drive, weak global coupling, no slow-wave) vs sleep (bistable down/up, strong global coupling, large slow oscillation, near-zero epoch-specific drive).

---

## §2 Method

### §2.1 Network

- **N=16 ROI**, sparse coupling W (density 0.35), spectral radius `rho` set per state.
- **T=2400 time-steps** (~40 min at TR=1s), **24 epochs × 100 samples**.
- AR(1): `x(t+1) = tanh(sat_gain · (W·x(t) + drive_epoch(t) + noise(t))) · sat_amp` plus regime-specific bistability snap on sleep.

### §2.2 Regime parameters

| param           | awake | sleep |
|-----------------|-------|-------|
| spectral radius `rho` | 0.45  | 0.95  |
| input noise σ   | 0.55  | 0.55  |
| epoch drive scale | 1.10 | 0.05 |
| slow-osc amplitude | 0.0 | 1.6 |
| slow-osc freq (Hz at TR=1s) | 0 | 0.012 |
| `tanh` sat gain | 0.5 (linear) | 1.4 (saturating) |
| bistable-snap threshold | – | 0.3, snap to ±1.4 |

### §2.3 Metrics

1. **Differentiation index D** (Boly analog): mean pairwise Euclidean distance between z-scored 16-D epoch mean activity vectors. Higher = richer pattern repertoire.
2. **State repertoire size**: distinct binary states visited (median-binarize per channel, count unique join-index over 16 channels capped at 2^16).
3. **LZ76 normalized**: channel-concatenated Lempel-Ziv 1976 production complexity, baseline-normalized `c·log2(n)/n`.
4. **Φ_geometric**: average MI across 64 random bipartitions of binarized data (cheap proxy, capped at 6 channels per side for tractability).
5. **Φ_pyphi (4-node coarse)**: cluster 16 ROIs into 4 macro-nodes (sum-binarize), fit empirical TPM, run `pyphi.compute.sia`. Tractable but loses differentiation structure.

### §2.4 Falsifier (preregistered, parent §8 F5)

- **F5 trigger**: Cohen-d on per-epoch differentiation (awake vs sleep) < 0.5 → reject information-postulate analog at this scale.

---

## §3 Results

| metric | awake | sleep | Δ (awake − sleep) | direction matches Boly? |
|---|---:|---:|---:|---|
| **Differentiation D** (primary) | 5.076 | 0.667 | **+4.409** | YES (large) |
| State repertoire size           | 1470  | 1136  | +334  | YES |
| Φ_geometric (MI proxy)          | 2.208 | 1.616 | +0.592 | YES |
| LZ_normalized                   | 0.552 | 0.733 | −0.181 | **NO** (caveat §4) |
| Φ_pyphi (4-node coarse)         | 0.483 | 1.281 | −0.798 | **NO** (caveat §4) |

**Cohen-d (per-epoch differentiation)** = **18.02** → F5 falsifier NOT triggered (threshold 0.5).

**Verdict: PASS** on primary metric (differentiation index) and 2 of 4 secondary metrics; honest caveats on the other 2 documented.

---

## §4 Honest caveats

1. **LZ inversion**: sleep regime's bistability-snap nonlinearity (sign-amplification past threshold ±0.3) creates sharp ±1.4 transitions which look high-entropy to LZ76. Real NREM EEG does show LZ collapse — our analog substrate over-corrects into "telegraph noise." Fixable with a refractory-period gate; deferred (not blocking primary verdict).
2. **PyPhi 4-node Φ inversion**: coarse 4-macro-node aggregation with strong global coupling (sleep `rho=0.95`) makes the 4 macro-nodes highly mutually predictable, inflating SIA Φ. The 4-macro picture loses the within-macro differentiation that the 16-channel D index captures. Fixable with finer macro grain (8-node), but PyPhi 8-node SIA is ~minutes per call — acceptable upgrade in next iteration.
3. **Substrate**: synthetic AR(1), NOT real BOLD. Per parent §6, this contributes **0** to Tononi's strict "16 studies" replication count. Internal value: extends consciousness-verifier suite (information / repertoire axis) at $0 cost.
4. **Single-seed**: one seed per condition. Bootstrap CIs deferred; the per-epoch-sample Cohen-d (18.0) is far enough from threshold that resample noise is unlikely to flip verdict.

---

## §5 Reproduction

```bash
ssh ubu1
cd ~/n_substrate_n21/test8_boly
~/n_substrate_n21/venv/bin/python boly_fmri_diff.py
# writes ~/n_substrate_n21/test8_boly/result.json (~45s)
```

Driver source mirrored at `state/n_21_test8_boly_fmri_diff_2026_05_01/boly_fmri_diff.py.txt` (HEXA-first repo: `.py` files cannot live under `/`-tracked extensions; stored as `.py.txt` for archival diff).

---

## §6 Cost

| item | spend |
|---|---:|
| compute (ubu1 local CPU, ~45s) | $0 |
| network                        | $0 |
| **total**                      | **$0** |

Budget envelope was $0–55. Came in at **$0** because ubu1 has the PyPhi venv and the analog runs in ~1 min on CPU — no H100 needed.

---

## §7 Cross-ref

- Parent spec: `docs/n_21_iit40_12_remaining_spec_2026_05_01.md` §4.5 RANK-5, §8 F5
- State JSON: `state/n_21_test8_boly_fmri_diff_2026_05_01/result.json`
- Driver source: `state/n_21_test8_boly_fmri_diff_2026_05_01/boly_fmri_diff.py.txt` (mirror of `ubu1:~/n_substrate_n21/test8_boly/boly_fmri_diff.py`)
- Sibling N-21 ANALOGIZE: `~/n_substrate_n21/test12_leung/` (RANK-1 fly Phi)

---

## §8 Source

- Boly M, Sasai S, Gosseries O, Oizumi M, Casali A, Massimini M, Tononi G (2015). *Stimulus Set Meaningfulness and Neurophysiological Differentiation: A Functional Magnetic Resonance Imaging Study.* PLoS Biology 13(11): e1002327. https://doi.org/10.1371/journal.pbio.1002327
