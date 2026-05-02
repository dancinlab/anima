# N-7 — AKIDA × QRNG spike noise floor comparison spec (pre-arrival skeleton)

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **agent**: N-7 prep (N-substrate batch sibling 7/13)
- **date**: 2026-05-01
- **parent menu row**: §3 N-7 "AKIDA × QRNG 스파이크 무작위 바닥" — `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
- **mission**: is AKIDA AKD1000 intrinsic spike-event noise statistically distinguishable from ANU QRNG quantum-vacuum noise?
- **scope**: D+0 plug-and-play protocol — runs the moment the AKD1000 dev kit lands on RPi5
- **isolation**: writes ONLY to this doc + `state/n_substrate_n7_prep_2026_05_01/*.json`
- **budget**: $0 (HEXA-only, ANU public API + already-ordered AKIDA capex)

---

## §1 한 줄 비유

칩 안에서 뉴런이 발화하는 "딱딱딱" 박자의 미세한 흔들림 (jitter) 이, 우주 진공이 만드는 진짜 무작위와 통계적으로 구분 가능한가? — 구분 안 되면 (KS p > 0.05) "1W 칩 잡음 = 우주 잡음" 충격적 결과; 구분되면 (KS p < 0.01) "AKIDA 는 구조화된 결정론적 잡음을 가진다" 또한 흥미.

---

## §2 두 분포 합성 사양

### 2.1 AKIDA AKD1000 spike noise distribution (datasheet-synthesized)

C3 raw#10: AKD1000 official product brief (v2.3, Aug 2025) does NOT publish per-event jitter / threshold-variability figures. We synthesize a **digital-event noise model** from publicly disclosed architectural specs:

| parameter | value | source |
|---|---|---|
| process node | 28 nm digital | open-neuromorphic.org / NeuroCortex.AI 2024 |
| clock frequency | 300 MHz typical | open-neuromorphic.org |
| NPU count | 80 | BrainChip product brief |
| neuron capacity | 1.2 M | BrainChip product brief |
| synapse capacity | 10 B | BrainChip product brief |
| event timestamp resolution (derived) | 1/300MHz ≈ 3.33 ns | clock-period bound |
| spike domain | rank-order coding (ROC), single-step integrate-and-fire, no leaky neurons | doc.brainchipinc.com user guide |
| typical power | ~1 W | product brief |
| arxiv 2505.11418 / 2603.13880 | "temporal jitter" only studied as adversarial perturbation, not endogenous spec | arxiv search |

**synthesized intrinsic-jitter model** (B-model, datasheet-derived; in-situ measurement supersedes at D+0):

```
Δt_spike ~ N(0, σ_jitter²) + U(0, T_clock)        # Gaussian thermal/PVT + clock-quantization uniform
σ_jitter   = 0.5 × T_clock = 1.67 ns              # half-cycle PVT proxy (digital flop setup/hold band)
T_clock    = 3.33 ns                               # 1 / 300 MHz
threshold_var ~ N(V_th, (0.01 V_th)²)             # 1% σ on integrate-and-fire threshold (28nm digital flop fan-out budget)
refractory ≥ 1 clock cycle = 3.33 ns              # single-step IF
```

**output stream for KS test** = consecutive inter-spike-interval (ISI) sequence from a constant-input integrate-and-fire test pattern, sampled `n_samples = 10^5` events. Each ISI digitized to nearest clock-tick → discrete distribution over {3.33 ns × k : k ∈ ℤ⁺}.

### 2.2 ANU QRNG distribution (quantum-vacuum baseline)

| parameter | value | source |
|---|---|---|
| physical principle | vacuum-fluctuation amplitude/phase quadrature | qrng.anu.edu.au |
| internal hardware rate | 5.7 Gbit/s (raw, post-extraction) | qrng.anu.edu.au FAQ |
| public API rate (effective) | ~1 kbit/s per req, ~1 req/min unsigned | `anima/modules/rng/anu.hexa` `ANU_ENDPOINT` + raw doc |
| max bytes per request | 1024 (server hard cap) | anima rng abstraction §3 |
| output type | uniform uint8 over [0, 255] | ANU JSON `type=uint8` |
| nominal distribution | i.i.d. uniform | ANU + post-extraction guarantee |
| NIST SP 800-22/90B certification | NOT formally published by ANU; community-side reports pass; ID Quantique vendor chip is NIST ESV-IID certified (sister source) | NIST CSRC / IDQ press 2026 |
| anima-side stub | `anima/modules/rng/anu.hexa` IMPLEMENTED; live probe via `ANIMA_QRNG_LIVE=1` | anima rng abstraction landing 2026-05-02 |

**ANU sample for KS test** = 10^5 uint8 draws, mapped to a comparable inter-event time domain via:
```
ISI_qrng[i] = (anu_uint8[i] / 255) × (T_clock × scale_to_match_AKIDA_mean_ISI)
```
i.e. uniform over [0, mean_ISI_akida × 2]. Honest C3: this remap injects a known bound; the test interrogates *shape* under matched mean, not absolute timing rate.

C3 raw#10: 8192 bit/s figure cited in mission brief is approximate (ANU FAQ states 5.7 Gbit/s internal; user-facing API is throttled). We adopt the **API-effective rate** 1 kbit/s as the realistic baseline for time-bounded experiments; collection time for 10^5 uint8 samples ≈ 10^5 × 8 bits / 1000 bps ≈ 800 s (~13 min) under conservative throttling.

---

## §3 Comparison protocol (D+0 plug-and-play)

### 3.1 Statistical tests — three-pronged

| # | test | formula | accept-rule | rejects |
|---:|---|---|---|---|
| T1 | Kolmogorov-Smirnov 2-sample | D = sup\|F_AKIDA(x) − F_QRNG(x)\| | p > 0.05 ⇒ INDISTINGUISHABLE (interesting) | p < 0.01 ⇒ AKIDA STRUCTURED |
| T2 | KL divergence (binned) | D_KL(P_AKIDA \|\| P_QRNG) over 256 bins | < 0.05 nats ⇒ matched | > 0.5 nats ⇒ structured |
| T3 | NIST SP 800-22 monobit + runs + serial-3 | scipy.stats / hand-rolled | both pass ⇒ each indistinguishable from random alone | — |

Decision tree:
```
T1 PASS (p > 0.05) AND T2 < 0.05  → "AKIDA spike noise ≈ quantum vacuum"  (⭐ headline)
T1 FAIL (p < 0.01) AND T2 > 0.5   → "AKIDA noise is structured / deterministic"  (⭐ also publishable)
intermediate                       → "noisy band — increase n_samples × 10 and repeat"
```

### 3.2 Falsifiers (pre-registered, raw#71)

| id | falsifier | trigger ⇒ verdict |
|---|---|---|
| F-N7-A | sample size < 10^4 | DISCARD (insufficient power) |
| F-N7-B | AKIDA ISI stream contains < 100 distinct values | DISCARD (clock-quantization-dominated, retry with denser test pattern) |
| F-N7-C | ANU API returns < 50% requested bytes within 30 min | DOWNGRADE to mock-LCG-via-router; re-flag verdict as `simulated_only` |
| F-N7-D | KL divergence > 5 nats | suspect input-pattern artifact, not intrinsic noise; rerun with Poisson-rate input vs constant |
| F-N7-E | datasheet σ_jitter assumption (1.67 ns) not bracketed by in-situ ISI std-dev within ±3× | document delta in C3, treat as headline finding ("datasheet under/over-states by Nx") |
| F-N7-F | router fallback to urandom triggered | mark verdict_key with `urandom_contamination`, re-run with `ANIMA_RNG_SOURCE=anu` strict mode |
| F-N7-G | both T1 PASS *and* T2 > 0.5 (test disagreement) | log paradox row to `state/n_substrate_n7_prep_2026_05_01/test_disagreement.json`, escalate to manual review |

### 3.3 Workload pattern (AKIDA spike harvest)

- model: minimal Edge Impulse keyword-spotting demo OR custom 1-NPU integrate-and-fire constant-input loop
- input: constant DC bias slightly above threshold (forces continuous regular firing)
- harvest: `akida.Model.statistics` per-NPU spike-event log → ISI sequence
- duration: continuous run for 60 s sufficient (300 MHz × 60 s = 1.8e10 cycles, ≫ 10^5 events at any reasonable spike rate)

### 3.4 ANU QRNG harvest

- route: `rng_route_collect(n_bytes=10^5, seed=<wall-clock-ns>)` with `ANIMA_RNG_SOURCE=anu`
- chunking: 1024 bytes/req × 98 reqs × 1000 ms inter-chunk pause ≈ 100 s
- store raw JSON + sha256 to `state/n_substrate_n7_prep_2026_05_01/anu_sample_<ts>.json`

---

## §4 Phases (D+0 → D+7)

| phase | day | name | deliverable | blocker |
|---:|---:|---|---|---|
| 1 | D+0 | AKD1000 boot + Edge Impulse demo flash on RPi5 | demo runs end-to-end | dev-kit arrival (ordered 2026-04-29) |
| 2 | D+1 | constant-input ISI harvest → `akida_isi_<ts>.json` | 10^5 ISI samples, sha256 logged | phase 1 |
| 3 | D+1 | ANU 10^5 uint8 harvest → `anu_sample_<ts>.json` | sample + sha256 + chunk-count audit | hexa router live |
| 4 | D+2 | KS / KL / NIST monobit run → `comparison_verdict.json` | T1 p, T2 nats, T3 pass/fail | phases 2+3 |
| 5 | D+2 | falsifier pass evaluation F-N7-A..G → `falsifier_evaluation.json` | 7 rows, each PASS/FAIL/SKIP | phase 4 |
| 6 | D+3 | graduation report row → append to `state/atlas_convergence_witness.jsonl` if ⭐ headline | one JSONL row | F-N7 all evaluated |
| 7 | D+7 | nexus cross-link + parent menu §3 N-7 status flip | doc edit only (no nexus write from this agent) | optional |

---

## §5 Honest C3 disclosures (raw#10)

1. **Datasheet noise spec absent** — BrainChip publishes architectural counts only, not per-event jitter / Vth-σ. The 1.67 ns / 1% Vth values are *pre-arrival synthesized priors*, not vendor-blessed. F-N7-E catches divergence at D+0.
2. **In-situ vs vendor noise gap** — even if datasheet figures existed, batch / temperature / supply-voltage-dependent jitter shifts can swamp nominal values. The D+0 measurement is the ground truth.
3. **ANU API throttle** — public endpoint ~1 kbit/s, not the mission-brief 8192 bit/s. Real run takes ~13 min wall-clock per 10^5-byte harvest under conservative pacing.
4. **No NIST SP 800-22 cert on ANU stream** — community pass, not vendor cert. T3 in this spec applies the test ourselves, not relying on upstream certification.
5. **Time-domain remap injects bound** — ANU uniform-uint8 mapped to ISI by linear scale; comparison interrogates *shape* under matched mean, not raw timing rate. Headline phrasing must specify "matched-mean shape comparison".
6. **Single AKIDA chip** — N=1 device; PVT variation across units uncharacterized. Cross-chip generalization requires future N≥3 cohort (out of scope for N-7).
7. **Constant-input bias** — using DC bias yields most-regular spike train, maximizing sensitivity to noise shape; Poisson-input rerun (F-N7-D fallback) tests robustness.
8. **Router fallback contamination** — `urandom` is NOT quantum; F-N7-F enforces strict-mode failure rather than silent quality degradation.
9. **Race-safe to 12 siblings** — only writes to this doc + `state/n_substrate_n7_prep_2026_05_01/`. No nexus repo write.
10. **No .py created** — HEXA-only mandate; analysis scripts will be added as `anima/modules/n7/*.hexa` at D+0 by execution agent (not this prep agent).

---

## §6 Reserved roadmap

`#252-N7 anima-n-substrate-n7-akida-qrng-spike-noise-comparison-prep-landed`

Verdict states (post-D+2):
- `INDISTINGUISHABLE_HEADLINE` — KS p>0.05 ∧ KL<0.05 ⇒ ⭐ noise-substrate-equivalence anchor
- `STRUCTURED_HEADLINE` — KS p<0.01 ∧ KL>0.5 ⇒ AKIDA deterministic-noise characterization
- `INCONCLUSIVE_INTERMEDIATE` — retry with 10× sample size
- `BLOCKED_HARDWARE_ABSENT` — pre-D+0, current state until kit arrives
- `FALSIFIER_DOWNGRADED` — F-N7-C/F triggered, mark as `simulated_only`

---

## §7 Cross-link

- parent menu: `docs/n_substrate_consciousness_roadmap_2026_05_01.md` §3 N-7 row
- AKIDA evaluation: `docs/akida_dev_kit_evaluation_2026-04-29.md`
- ANU module SSOT: `docs/anima_rng_abstraction_landing_20260502.md`
- sibling N-2 prep (EEG→AKIDA spike direct): `state/n_substrate_n2_prep_2026_05_01/`
- sibling N-4 prep (Landauer 3-axis): `state/n_substrate_n4_prep_2026_05_01/` + `docs/n_substrate_n4_landauer_3axis_spec_2026_05_01.md`
- meta witness ledger (graduation target): `state/atlas_convergence_witness.jsonl`

---

**status**: N_SUBSTRATE_N7_PREP_2026_05_01_LOCAL_DRAFT
**verdict_key**: PRE_ARRIVAL_SKELETON_READY · BLOCKED_HARDWARE_ABSENT · D_PLUS_ZERO_PLUG_AND_PLAY
