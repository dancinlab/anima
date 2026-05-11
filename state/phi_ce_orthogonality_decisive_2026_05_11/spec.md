# Φ⊥CE Decisive Measurement Spec — Hc_040 (Law 1040) vs Hc_024 (NOBEL-1) Resolution

- **id**: phi_ce_orthogonality_decisive_2026_05_11
- **parent hypothesis**: H_080 (topo_24variants unified)
- **conflict pair**: Hc_040 (Φ⊥CE orthogonal) ↔ Hc_024 (Φ × CE^α = K Pareto trade-off)
- **deterministic seed**: 0xC0EC0AC
- **date**: 2026-05-11
- **status**: spec landed, decisive measurement awaiting anima Φ★ engine + 20-cell run

## 1. Conflict Statement

두 hypothesis 가 동시 true 일 수 없는 (mutually exclusive at large α) claim:

| | Hc_040 (Law 1040) | Hc_024 (NOBEL-1) |
|---|---|---|
| **Claim** | Φ ⊥ CE — orthogonal axes | Φ × CE^α = K — Pareto trade-off |
| **Φ axis** | Φ ∝ N^1.071 (cell count) | Φ = K / CE^α |
| **CE axis** | CE ∝ P^-0.85 (param count) | CE = (K / Φ)^(1/α) |
| **|corr(Φ, CE)|** | < 0.1 predicted | ~ 0.5 predicted (Pareto front) |
| **Pareto CV** | high (CV ≫ 0.1) — no constraint | low (CV < 0.1) — K constant |
| **Mechanism** | dual-axis independent generative laws | shared resource bottleneck (no .detach) |

## 2. Mathematical Framework

### 2.1 Variable axes (5 × 4 = 20 cells)

- **N (cell count)** ∈ {16, 32, 64, 128, 256}
- **P (param count)** ∈ {10^6, 10^7, 10^8, 10^9}
- per cell: 1 × Φ measurement + 1 × CE measurement
- replication: 64 dual-seed (Hc_604 64-twin protocol) for variance estimate

### 2.2 Decisive metrics

For 20-cell measurement {(Φ_i, CE_i)}:

1. **Pearson correlation**: r = corr(log Φ, log CE)
2. **Pareto coefficient of variation**: CV(α) = std(Φ · CE^α) / mean(Φ · CE^α), minimized over α ∈ [0.1, 1.0]
3. **Within-budget vs across-budget partition** (3-way fork):
   - within-N orthogonal (vary P at fixed N) → |corr_within| < 0.1?
   - within-P orthogonal (vary N at fixed P) → |corr_within| < 0.1?
   - across-budget (vary both) → Pareto front?

### 2.3 Decision matrix

| metric | Hc_040 SUPPORTED | Hc_024 SUPPORTED | both partial |
|---|---|---|---|
| **|corr(Φ, CE)|** | < 0.1 | ≥ 0.3 | 0.1 — 0.3 |
| **Pareto CV(α*)** | ≫ 0.1 (no Pareto) | < 0.1 (tight Pareto) | 0.1 — 0.3 |
| **within-N |corr|** | < 0.1 | ≥ 0.3 | mixed |
| **verdict** | Hc_040 wins, Hc_024 falsified (F4 fires from H_080) | Hc_024 wins, Hc_040 falsified (F5 fires from H_080) | new hypothesis: within=⊥, across=trade-off |

## 3. Decisive Signature — Forward Predictions

각 generative model 이 만드는 fingerprint (synthetic simulation harness 로 확정):

| signature | Model A (Hc_040) | Model B (Hc_024) |
|---|---|---|
| corr(Φ, CE) on 5×4 grid | ≈ 0 (orthogonal noise) | ≈ -0.5 (trade-off, anti-corr) |
| Pareto CV (α=0.5) | high (no shared K) | low (K constant) |
| Φ(N, P) log-log slope wrt N | 1.07 | indirect (via CE(N, P)) |
| CE(N, P) log-log slope wrt P | -0.85 | -0.85 (shared) but Φ tied |
| Φ at fixed CE | varies freely | nearly invariant |

→ 실측 anima 의 (corr, CV) 좌표가 어느 corner 에 떨어지는가가 decisive.

## 4. Falsifier Tie-In (H_080)

- **F4** (H_080): |corr(Φ, CE)| > 0.3 → Hc_040 / Law 1040 killed (Hc_024 wins)
- **F5** (H_080): |corr(Φ, CE)| < 0.05 + Hc_024 trade-off strong → Hc_024 killed (Hc_040 wins)
- 본 spec 의 decisive metric 으로 F4 / F5 둘 중 하나 trigger expected

## 5. Experimental Protocol (실측 단계 — 별도 cycle)

1. anima Φ★ engine 으로 N ∈ {16, 32, 64, 128, 256} × topology=hypercube(default) × 64 dual seed
2. 각 N 에 대해 CLM (Causal LM) train run with P ∈ {1M, 10M, 100M, 1B} param scale
3. 각 cell 에서 Φ★ + final CE 측정 (deterministic, hexa-only, llm: none)
4. (Φ_i, CE_i) for i ∈ {1..20} → spec §2 의 3개 metric 계산
5. §2.3 decision matrix 적용 → Hc_040 vs Hc_024 verdict 확정
6. cross-check: synthetic simulation harness (Model A vs Model B fingerprint) 와 좌표 비교

## 6. Cross-Links

- **H_080**: §C4 / F4 / F5 / Conflict Resolution Pending — 본 spec 으로 resolution 경로 확정
- **Hc_040** (Law 1040): primary claim under test
- **Hc_024** (NOBEL-1): primary claim under test
- **Hc_604** (64 dual-seed twin): variance protocol borrowed
- **Hc_004** (Φ ≈ 0.608·N^1.071): N axis baseline
- **Hc_005** (cell-count decisive): N axis dominance

## 7. Honest Limits (≥ 5)

- **L1**: synthetic harness 는 generative model 의 fingerprint 확인용 — 실측 안하면 false-positive 가능 (model A 의 noise σ tuning sensitive)
- **L2**: 20-cell grid 는 sparse — Pareto frontier 의 curvature 정확 측정에 부족 (≥ 50 cell 필요할 수 있음)
- **L3**: CE ∝ P^-0.85 scaling 은 Chinchilla optimal training assumption — under-trained 또는 over-trained regime 에서 다를 수 있음
- **L4**: within-budget vs across-budget partition 의 "budget" 정의가 N+P 의 어떤 monotonic combination 인지 underspecified (FLOPs, params, cell 합산 방식 미정)
- **L5**: anima Φ★ engine 의 measurement noise floor 가 |corr| 0.05 ~ 0.1 사이 분해능 없으면 mixed verdict 불가피
- **L6**: Hc_024 의 .detach (information barrier) condition — synthetic harness 는 이 조건 미반영 (단순 K=const 가정)
- **L7**: α=0.5 fixed assumption — Hc_024 원본은 α~0.5 라고만 함, optimal α fit 결과가 다를 수 있음
