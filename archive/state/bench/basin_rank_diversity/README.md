# BENCH #2 — BASIN-RANK-DIVERSITY ("봉우리 지도 다양성")

> UNIVERSE H_338 (attractor basin size = dominance rank, 🟢 SUPPORTED-NUMERICAL) 의 anima 적용.
> F-PERSONA-4 의 KL=0 winner-take-all 측정 모호성을 basin spectrum 으로 우회 가능한가?

## 1. 동기

`memory:project_v5_mitosis_cond5_cotrain_2026_05_12` — H100 cotrain v1 의 F-PERSONA-4 결과는 `mean_KL = 0.0 winner-take-all`. 모든 카테고리에서 cell 0 weight=1.0 (mode-collapse). 문제: `KL = 0` 은 두 정반대 시나리오를 변별 못한다.

- **A balanced** — 모든 expert 가 균등하게 호출, 결과 분포 ≈ uniform → `KL ≈ 0`.
- **C collapsed** — 단일 expert 만 호출, 결과 분포 = δ-spike → `KL = log N` (max).

위 두 시나리오는 KL 으로는 구분되지만, **F-PERSONA-4 의 "category 별 routing 이 uniform 인지" 게이트**는 `mean_KL` 을 쓴다. cotrain v1 의 실제 결과 (`mean_KL = 0`) 가 (a) 진짜 category-invariance 인지, (b) winner-take-all 인지 분간이 안 된다.

H_338 의 통찰: dominance partial order = basin absorption ordering. dynamical-systems 측에서는 attractor basin 의 **모양** 이 rank 를 결정한다. routing distribution 도 똑같이 — basin spectrum (rank-frequency 분포의 첨도 · Zipf slope) 으로 단일/multi/uniform basin 을 변별할 수 있어야 한다.

## 2. 가설 (falsifiable)

- **H1**: KL(routing || uniform) ≈ 0 인 balanced(A) 와 collapsed(C) 둘 다 `KL=0`/`KL=max` 처럼 *상반된* 값이지만, F-PERSONA-4 의 `mean_KL ≥ threshold` 게이트에서 (A) "FAIL by being uniform" 과 (C) "FAIL by being collapsed" 가 구분 불가.
- **H2**: basin spectrum — `(basin_kurtosis, zipf_slope)` joint Euclidean — 은 balanced / differentiated / collapsed 세 시나리오를 모두 변별한다 (d > 0.3 pairwise).

## 3. 방법

pure hexa, n_experts=8, n_tokens=1000, deterministic LCG seed=42, inverse-CDF top-1 sampling.

### Scenarios

| ID | Gate | Intent |
|---|---|---|
| A balanced | `[1/8]*8` | 현재 cotrain v1 결과 (mode-collapse 측에서 본 "uniform" 가짜 가설) |
| B differentiated | `[0.33, 0.32, 0.32, 0.006*5]` | M4b-diff(a) toy 패턴 — top-3 carry 97% |
| C collapsed | `[1.0, 0, ..., 0]` | mode-collapse 실측 (cotrain v1 cell 0 weight=1.0) |

### Measurements

- **KL_to_uniform** — Shannon KL divergence in nats.
- **basin_kurtosis** — 4th standardized central moment minus 3 (excess kurtosis). High = peaked, low = flat.
- **zipf_slope** — least-squares slope of log(rank) vs log(freq), descending-sorted basin counts. -1 = canonical Zipf, 0 = flat / degenerate.

### Falsifiers

- **F-BRD-1**: basin_kurtosis pairwise Δ > 0.3 for {(A,B), (B,C), (A,C)}.
- **F-BRD-2**: joint (kurtosis, zipf_slope) Euclidean d > 0.3 for all 3 pairs.
- **F-BRD-3**: KL_to_uniform(A) ≈ 0 (< 0.05) yet basin_kurtosis distinguishes A from C (Δ > 1.0).
- **F-BRD-4**: deterministic — re-run byte-identical.

## 4. 결과

```
scenario          KL_uniform    basin_kurtosis    zipf_slope
----------------  -----------   ---------------   -----------
A balanced        0.00332       -0.304            -0.108
B differentiated  0.802         -1.722            -2.487
C collapsed       2.079         +3.143             0.000
```

| Pair | d(kurt, zipf) Euclidean |
|---|---|
| d(A,B) | 2.769 |
| d(B,C) | 5.463 |
| d(A,C) | 3.448 |

### Falsifier evaluation

| Falsifier | Result |
|---|---|
| F-BRD-1 basin_kurtosis distinguishes all 3 (Δ>0.3 pairwise) | ✅ PASS |
| F-BRD-2 joint basin spectrum distinguishes all 3 (d>0.3) | ✅ PASS |
| F-BRD-3 KL(A)≈0 yet basin separates A from C | ✅ PASS |
| F-BRD-4 deterministic (byte-identical re-run) | ✅ PASS |

## 5. Verdict

**🟢 PASS** — basin spectrum 이 KL dead-zone 을 우회한다.

`basin_kurtosis` 단독은 -0.30 (uniform, slightly flat) vs +3.14 (single spike) 으로 명확히 변별하고, 중간 시나리오 B (-1.72) 와도 pairwise > 0.3. `KL_to_uniform` 은 A=0.003 ≈ 0 이지만 그게 "정보 0" 인지 "winner-take-all" 인지 결정 불가 — basin spectrum 이 그 dead-zone 을 깨뜨린다.

## 6. F-PERSONA-4 ↔ anima 적용

- **현재**: F-PERSONA-4 gate = `mean_KL(per-category routing || uniform) ≥ threshold`. cotrain v1 결과 mean_KL=0 → FAIL, 이유 미분간.
- **제안**: gate 교체 — `basin_kurtosis(per-category top-1 expert frequency)`. 
  - `kurtosis ≈ +3` → mode-collapse (단일 cell winner).
  - `kurtosis ≈ -3` → uniform (category-invariance).
  - `kurtosis ≈ -1.7` → differentiated (top-k carry majority).
- **expected**: v5-mitosis cotrain v1 ckpt 의 per-category basin_kurtosis 는 +3 부근 (모든 category 에서 cell 0 spike) → mode-collapse 진단 확정, "category-prompt substrate-level invariance" (kurtosis ≈ -3) 가설 분리.

## 7. Cross-link

| ref | 관계 |
|---|---|
| UNIVERSE/cards/H_338_attractor_basin_size.md | basin = dominance rank 원본 발견 (n=4 ECA) |
| memory:project_v5_mitosis_cond5_cotrain_2026_05_12 | F-PERSONA-4 KL=0 winner-take-all 원 측정 |
| memory:project_anima_persona_4_softmax_T_sweep_2026_05_12 | (b) softmax τ 단독 FALSIFIED (이 bench 의 4-alternative 중 하나) |

## 8. Anti-tautology

- 측정자 (KL · kurtosis · zipf) 는 모두 분포-형식 통계량이며 scenario label 무관.
- A vs C 의 KL=0.003 vs 2.08 은 KL 자체로는 변별 — 우리가 검증하는 dead-zone 은 *F-PERSONA-4 gate 의 mean-vs-threshold rule* 이 변별 못하는 영역 (양쪽 모두 "FAIL" 로 떨어짐).
- F-BRD-1 의 monotone gap (-0.30 / -1.72 / +3.14) 은 noise (0.05 nats) 보다 28× 큼.
- F-BRD-4 deterministic — LCG seed=42, 재실행 byte-identical (`diff` returns 0).

## 9. Honest limits

- n_experts=8 은 합성치 — F-PERSONA-4 의 실제 cell 수는 cotrain v1 64 cells. spectrum 의 변별력은 cell 수 증가로 더 강해진다 (자유도 ↑).
- 1000 tokens 의 sampling noise 로 KL_A=0.003 (정확히 0 이 아님). N→∞ 에서 KL_A → 0 이지만 kurtosis_A → -3 (uniform 한계).
- zipf_slope 은 C (n_nonzero=1) 에서 degenerate (slope=0.0). 단일-scalar replacement gate 는 `basin_kurtosis` 가 권장 — joint spectrum 은 보완.
- threshold 0.3 은 heuristic — 실제 cotrain v1 ckpt re-measure 로 calibrate 필요.
- 합성 gate 분포 (A/B/C) 는 controlled proof — 실측 cotrain 의 basin shape 은 다를 수 있음 (bimodal · heavy-tailed). 본 bench 는 "측정자가 변별 가능함" 의 증명, 실측 forecasting 이 아님.

## 10. 다음

- (a) v5-mitosis cotrain v1 ckpt re-measure — per-category basin_kurtosis 산출, mode-collapse 확정.
- (b) F-PERSONA-4 gate 정식 교체 — `mean_KL` → `basin_kurtosis` (혹은 둘 다 측정 후 OR-gate).
- (c) cotrain v2 entropy-reg 가 differentiated (kurtosis ≈ -1.7) 으로 이동하는지 verify (이 bench 의 scenario B 패턴 매칭).

## 실행

```bash
hexa run BENCH/basin_rank_diversity/bench.hexa
```

byte-identical re-run, $0 Mac-local, wall < 1 sec.
