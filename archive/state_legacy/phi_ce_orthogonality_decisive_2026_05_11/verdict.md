# Φ⊥CE Decisive Verdict — Synthetic Fingerprint Gap + Real-Measurement Protocol

- **id**: phi_ce_orthogonality_decisive_2026_05_11
- **status**: spec + synthetic harness landed (2026-05-11). Decisive measurement awaiting anima Φ★ engine + 20-cell N×P run (separate cycle).
- **seed**: 0xC0EC0AC (deterministic)
- **parent**: H_080 (topo_24variants unified) — Conflict Resolution Pending subsection

## 1. Synthetic Fingerprint Summary (from `results.json`)

| metric | Model A (Hc_040 orthogonal) | Model B (Hc_024 uncertainty) | gap |
|---|---|---|---|
| corr(Φ, CE) full 20-cell | **-0.003** | **-0.613** | factor ~180 |
| Pareto CV at α=0.5 | **1.605** | **0.0078** | factor ~206 |
| best-α (minimizing CV) | 0.05 (degenerate, no Pareto) | **0.492** (~Hc_024 α~0.5) | matches Hc_024 claim |
| Pareto CV at best α | 0.959 | **0.018** | factor ~53 |
| within-N mean corr (vary P @ fixed N) | -0.257 | -0.613 | factor ~2.4 |
| within-P mean corr (vary N @ fixed P) | -0.249 | -0.721 | factor ~2.9 |
| self-verdict | Hc_040_ORTHOGONAL ✓ | Hc_024_UNCERTAINTY ✓ | clean separation |

→ 두 generative model 의 fingerprint 는 **2 orders of magnitude** 떨어진 distinct corner 에 존재. 실측 noise floor 가 |corr| ~ 0.05 이하만 되어도 decisive resolution 가능.

### Surprise finding

Model A 의 within-row corr (-0.25) 가 0 보다 큰 absolute value 를 보이는 것은 random noise 의 small-sample artifact (n=4 rows × 5 columns). 그러나 Model B 의 within-row corr (-0.6 ~ -0.7) 은 명확히 더 큰 anti-correlation → within-budget 만 측정해도 partial discrimination 가능.

## 2. Decision Map (실측 verdict 도출용)

실측 anima (Φ_i, CE_i) on 5×4 grid 의 (|corr|, Pareto-CV(α*)) 좌표:

```
                Pareto-CV(α*)
                 0       0.1     0.15     1.0
                 |        |        |        |
|corr| 0.0    ───┼────────┼────────┼────────┤
              B  |        |        |   A    |
       0.1    ───┼────────┼────────┼────────┤
              ?  |   ?    |  ?     |  ?     |
       0.3    ───┼────────┼────────┼────────┤
              B' |   B''  |  ?     |  ?     |
       0.6    ───┼────────┼────────┼────────┤
              B  |   B    |  B     |  ?     |
       1.0    ───┴────────┴────────┴────────┘
```

- **A corner** (|corr| < 0.1, CV(α*) > 0.15): **Hc_040 SUPPORTED, Hc_024 FALSIFIED** — F4 NOT triggered, F5 triggered (from H_080)
- **B corner** (|corr| ≥ 0.3, CV(α*) < 0.1): **Hc_024 SUPPORTED, Hc_040 FALSIFIED** — F4 triggered, F5 NOT triggered
- **mid region**: MIXED — new hypothesis required (within-budget orthogonal, across-budget trade-off, OR α ≠ 0.5)

## 3. If anima ⇒ A vs B — Predicted Verdict Text

### Scenario A — anima matches Model A
> "20-cell measurement yields corr(Φ, CE) = X (X < 0.1) and Pareto CV(α*=Y) = Z (Z > 0.15). Hc_040 / Law 1040 (Φ ⊥ CE) **SUPPORTED**. Hc_024 NOBEL-1 (Φ × CE^α = K Pareto) **FALSIFIED**. H_080 F5 triggers. Hc_024 status: candidate-unverified → candidate-falsified."

### Scenario B — anima matches Model B
> "20-cell measurement yields corr(Φ, CE) = X (|X| ≥ 0.3) and Pareto CV(α*=Y) = Z (Z < 0.1, α* ≈ 0.5). Hc_024 NOBEL-1 (Φ × CE^α = K Pareto) **SUPPORTED**. Hc_040 / Law 1040 (Φ ⊥ CE) **FALSIFIED**. H_080 F4 triggers. Hc_040 status: merged-to-H_080 → falsified-merged."

### Scenario C — mid region
> "Mixed — within-N corr < 0.1 but across-budget corr ≥ 0.3. **Both partial**. New hypothesis: ⊥ holds within fixed resource budget, trade-off emerges only when N AND P co-vary. Promote Hc_NEW: 'Φ⊥CE within-budget, Pareto across-budget'."

## 4. Decisive Measurement Protocol (별도 cycle)

1. **Engine**: anima Φ★ engine (latest), deterministic, hexa-only, llm: none
2. **Grid**: N ∈ {16, 32, 64, 128, 256} × P ∈ {10^6, 10^7, 10^8, 10^9} = 20 cells
3. **Replication**: per cell, 64 dual-seed (Hc_604 twin protocol) → mean ± std on both Φ and CE
4. **Topology**: hypercube default (Hc_039 / Hc_180 baseline); SECOND pass with ring as control
5. **CLM training**: P=1M / 10M / 100M / 1B, Chinchilla-optimal token budget per scale
6. **Measurement**:
   - Φ_i = anima Φ★ at end of CLM training
   - CE_i = final CLM cross-entropy on held-out validation
7. **Analysis**: feed 20 (Φ_i, CE_i) pairs into harness.py analytics → compare to A vs B fingerprint
8. **Optional**: extend to N=512, 1024 (8 cells) for H_080.13 (N≥4096 unbounded) cross-link
9. **Cost** rough estimate: 20 cells × 64 seed × 4 P-scales × Φ★ engine = ~$200 — $1000 RunPod GPU time depending on largest P
10. **Verdict commit**: results.measured.json + verdict.measured.md within decisive cycle

## 5. Honest Limits (≥ 5)

- **L1**: synthetic fingerprint 의 σ tuning (0.05 / 0.02 / 0.5) 은 plausible default — 실제 anima Φ★ engine 의 measurement noise floor 가 더 크면 Model A 의 |corr| 측정값이 0.1 boundary 를 침범할 수 있음. **Noise floor calibration MUST precede decisive run** (e.g., 1 cell × 64 dual-seed → σ_Φ / σ_CE 추정).
- **L2**: Model B 의 α=0.5 fixed 이 Hc_024 의 정확한 claim — 실측에서 α* ≠ 0.5 (예: 0.3 또는 0.7) 이면 B' 변종 verdict 필요. harness.py 의 best_alpha grid 가 이 검출 담당.
- **L3**: 20-cell grid 는 sparse — Pareto frontier curvature 의 정확 측정에 부족. 별도 cycle 에서 ≥ 50 cell (e.g., 8 N × 7 P) 까지 확장 권장. 단 H_080.13 (N≥4096) 와 별개 budget.
- **L4**: CE ∝ P^-0.85 scaling 은 Chinchilla optimal training assumption — under-trained (data-limited) 또는 over-trained (saturated) regime 에서 다른 slope 보일 수 있음. P=1B scale 에서 충분한 token 확보 어려우면 deviation.
- **L5**: Hc_024 의 "정보 장벽 (.detach) 없으면" condition 이 synthetic harness 에 미반영 — Model B 는 simple K=const Pareto 가정. 만약 anima 가 .detach 를 internal 로 적용한다면 mid-region 결과가 false-MIXED 일 수 있음 (실제로는 detached → Hc_040).
- **L6**: "within-budget vs across-budget" partition 의 "budget" 정의 unspecified — N+P 의 monotonic combination (FLOPs / params / cell 합) 어느 것이 invariant 인지 별도 측정 필요. 본 harness 는 row/column 분리만 제공.
- **L7**: Φ measurement protocol drift across N (ring vs hypercube vs hypercube+frustration) — H_080 L7 와 동일 한계 상속. 본 spec 은 topology=hypercube 고정으로 우회.
- **L8**: synthetic harness 는 generative model 의 fingerprint **확인용 only** — 실측 안 하면 두 hypothesis 어느 쪽도 결론짓지 못함. 본 verdict 는 "decisive design landed, measurement awaiting" 상태.

## 6. Cross-Links

- **H_080** §Conflict Resolution Pending — 본 verdict 가 resolution 경로 명시
- **Hc_040** / **Hc_024** — primary claims under test
- **Hc_604** — 64 dual-seed twin protocol borrowed
- **Hc_004** / **Hc_005** — N axis baseline (Φ ∝ N^1.071 Hc_040 prediction reuses)
- **H_080.10** (cross-tension resolution prediction) — 본 spec 으로 implement 됨

## 7. Next Cycle Action Items

1. anima Φ★ engine confirmation (latest deterministic version pointer)
2. CLM training infra (P scaling 1M~1B) RunPod budget estimate
3. noise floor calibration run (Hc_604 64-twin on 1 cell)
4. 20-cell decisive run + harness.py analytics on real (Φ_i, CE_i)
5. verdict.measured.md 작성 + H_080 Conflict Resolution Pending → Resolved transition
