# Φ⊥CE Decisive Measurement Spec — Hc_040 (Law 1040) vs Hc_024 (NOBEL-1) Resolution

- **id**: phi_ce_orthogonality_decisive_2026_05_11
- **parent hypothesis**: H_080 (topo_24variants unified)
- **conflict pair**: Hc_040 (Φ⊥CE orthogonal) ↔ Hc_024 (Φ × CE^α = K Pareto trade-off)
- **deterministic seed**: 0xC0EC0AC
- **date**: 2026-05-11
- **status**: spec landed, decisive measurement awaiting phi_star_iit_proxy + (TBD) phi_star_cell_engine split-engine path + 15-cell run (P=100M ceiling, §5.7). Engine naming refactored 2026-05-12 — see §5.8.

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

### 2.1 Variable axes (5 × 3 = 15 cells, P=100M ceiling)

- **N (cell count)** ∈ {16, 32, 64, 128, 256}
- **P (param count)** ∈ {10^6, 10^7, 10^8}  — **P=10^9 (1B) removed**, see §5.7 cost ceiling rationale
- per cell: 1 × Φ measurement + 1 × CE measurement
- replication: 64 dual-seed (Hc_604 64-twin protocol) for variance estimate
- **deferred P=1B extension lane**: see §5.7 — reserved if Cycle-6+ budget allows

### 2.2 Decisive metrics

For 15-cell measurement {(Φ_i, CE_i)} (P=100M ceiling per §5.7; 20-cell with P=1B extension deferred):

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
| **P=100M ceiling 4-outcome cost** | decisive at $121-420 (baseline 부합) | decisive at $121-420 (baseline 부합) | mixed → P=1B extension $500-1500 추가 (§5.7.3) |
| **verdict** | Hc_040 wins, Hc_024 falsified (F4 fires from H_080) | Hc_024 wins, Hc_040 falsified (F5 fires from H_080) | new hypothesis: within=⊥, across=trade-off |

## 3. Decisive Signature — Forward Predictions

각 generative model 이 만드는 fingerprint (synthetic simulation harness 로 확정):

| signature | Model A (Hc_040) | Model B (Hc_024) |
|---|---|---|
| corr(Φ, CE) on 5×3 grid (P=100M ceiling) | ≈ 0 (orthogonal noise) | ≈ -0.5 (trade-off, anti-corr) |
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

1. **Φ-track** (phi_star_cell_engine — TBD; 현재 phi_star_iit_proxy 단독으로는 N-sweep 미지원, audit §1.3 / §5.8 참조) 으로 N ∈ {16, 32, 64, 128, 256} × topology=hypercube(default) × 64 dual seed
2. **CE-track** 각 N 에 대해 CLM (Causal LM) train run with P ∈ {1M, 10M, 100M} param scale (P=1B deferred — §5.7) — 별도 pipeline, split-engine 원칙 (§5.8)
3. 각 cell 에서 Φ_i (Φ-track) + final CE_i (CE-track) 측정 후 (N, P) cell key 로 join. phi_star_iit_proxy 는 Mistral-7B forward 사용 (단, "llm: none" 표기는 cell-engine path 가 land 된 시점부터 적용; audit §5.1 모순 caveat).
4. (Φ_i, CE_i) for i ∈ {1..15} → spec §2 의 3개 metric 계산
5. §2.3 decision matrix 적용 → Hc_040 vs Hc_024 verdict 확정
6. cross-check: synthetic simulation harness (Model A vs Model B fingerprint) 와 좌표 비교

## 5.7 Cost ceiling rationale (P=100M cap)

**Decision (2026-05-12)**: P=1B 제거 → 15-cell grid (5 N × 3 P). NEXT.md cycle 5 #1
baseline cost $200-1000 + 1-2 day 을 *준수* 하기 위한 ceiling.

### 5.7.1 Audit cost re-estimate (excerpt from spec_audit_2026_05_11.md §5.3)

| 항목 | low | high |
|------|-----|------|
| Φ-track 64-seed × 20 cell (phi_star_iit_proxy + phi_star_cell_engine N-sweep, TBD) | $50 | $200 |
| CE-track CLM train P=1M | $1 | $5 |
| CE-track CLM train P=10M | $5 | $20 |
| CE-track CLM train P=100M | $50 | $150 |
| CE-track CLM train P=1B | $500 | $1500 |
| noise floor calibration (§5.7.3) | $15 | $45 |
| **20-cell total (with P=1B)** | **$621** | **$1920** |
| **15-cell total (P=100M ceiling, this spec)** | **$121** | **$420** |

→ P=1B cell 단독 비용 $500-1500 이 전체 cost 의 ~80 % 차지. P=1B 제거 시 $121-420 (NEXT.md $200-1000 baseline 내).

### 5.7.2 P=1B 제거 정당화 — signature separability 유지

- 본 spec §3 의 Model A vs Model B fingerprint 분리 폭은 *harness.py 실행 결과* 180×/206× (15-cell synthetic re-run 결과도 동일 자릿수 예상, P=1B 1 column 빠져도 separability ≥ 50× 유지).
- corr(Φ, CE) 와 Pareto CV 의 statistical power 는 N=5 × P=3 = 15 cell 에서도 충분 (decision matrix 의 0.1 / 0.3 corr threshold 분해능 유지).
- Hc_040 의 CE ∝ P^-0.85 slope fit 은 3 P-point (1M / 10M / 100M, 2 decade 폭) 으로 first-order linear regression 가능 — slope SE 는 ~20-30 % 정도 증가 예상이나 Hc_040 vs Hc_024 verdict (corr/CV 기반) 에는 영향 미미.

### 5.7.3 Deferred P=1B extension lane

향후 다음 조건 충족 시 P=1B cell 4개 (N ∈ {16, 32, 64, 128, 256} 중 select-3 + 1 spot) 추가 측정 lane 개설:

- 15-cell decisive run 의 verdict 가 "mixed" (corr ∈ [0.1, 0.3]) 또는 Pareto CV ∈ [0.1, 0.3] → resolution power 부족 시 extension trigger
- 또는 H_080 Conflict Resolution Pending 의 별도 cycle 에서 budget 가용
- extension cost: $500-1500 (Chinchilla 20× token P=1B train) + Φ-track ~$10-30

### 5.7.4 Noise calibration prereq cost ($15-45, L1 해소)

L1 (synthetic σ default 의 plausibility) 해소 전제 비용을 별도 lane 으로 명시:

- 1 cell × 64 dual-seed Φ measurement → σ_Φ_rel 실측 (~53 GPU-min @ A100, $5-15)
- 1 scale × 4 init-seed CE training → σ_CE_rel 실측 (~4 GPU-h, $10-30)
- gate: σ_Φ_rel ≤ 0.10 (audit 권고) → harness.py σ default 재튜닝 후 decisive run 진입
- 이 calibration 은 15-cell decisive run 의 prerequisite (audit §4 / §7 권고)

## 5.8 Engine naming refactor — "anima Φ★ engine" → 3-engine split (2026-05-12)

본 spec 의 §1 / §5 / §5.7.1 / §7-L5 에서 사용된 "anima Φ★ engine" 단일 표현은 *3개 별도
engine* 을 conflate 한 misaligned premise. spec_audit_2026_05_11.md §5 finding (3개 critical
gap) 을 반영해 다음 명명으로 refactor:

| canonical name | what it is | path / status | role in this spec |
|----------------|------------|---------------|-------------------|
| **phi_star_iit_proxy** | single-model IIT-φ proxy via cov-MIP K=8 random bipartition (Mistral-7B-v0.3 forward, 16 prompt × byte-weighted hidden state) | `tool/anima_phi_star.hexa` (file name 유지, frontmatter `axis: phi_star_iit_proxy` + `llm: mistral-7b-forward` 2026-05-12 추가) | Φ-track *partial* — single-cell snapshot 만, N-sweep 미지원 |
| **nexus_lens_score** | multi-lens cross-validation framework (closed-form pattern score per data, 1,588 hexa lens on disk / 1013 official registry) | `/Users/ghost/core/nexus/lenses/*.hexa` (CPU only, hexa runner) | 본 spec 무관 — H_135 / 1013-lens lane (별 cluster) |
| **phi_star_cell_engine** | (TBD / not-yet-implemented) cell-count N-sweep engine — Hc_005 cell-count-decisive / Hc_040 N^1.071 의 *원 axis* (faction count, cell module count) 대응 | candidate: `tool/an11_*` / `anima_cds.hexa` / `anima_b_tom.hexa` (audit §1.3) — 메인 process 결정 필요 | Φ-track *binding* — N ∈ {16, 32, 64, 128, 256} sweep 실측 prerequisite |

**Premise correction**: 본 spec §5.1 "anima Φ★ engine 으로 N ∈ {16..256}" 는 *phi_star_iit_proxy
단독으로는 불가능* (audit §1.3 critical gap). split-engine 채택 (audit outcome #3) — Φ-track =
phi_star_cell_engine, CE-track = CLM training pipeline.

**Back-compat**: `tool/anima_phi_star.hexa` 파일명 + emitted JSON schema `anima/phi_star/1`
*변경 없음*. 기존 callsite (`tool/anima_phi_star.hexa --selftest` 등) 그대로 작동. axis /
llm field 는 *additive metadata* (frontmatter comment).

**Refactor manifest**: `state/phi_star_naming_refactor_2026_05_12.md` — 전체 변경 파일 + line
위치 + migration plan.

## 6. Cross-Links

- **spec audit**: `state/phi_ce_orthogonality_decisive_2026_05_11/spec_audit_2026_05_11.md` §5.3 (cost re-estimate, P=100M ceiling rationale source) / §4 (noise calibration protocol)

- **H_080**: §C4 / F4 / F5 / Conflict Resolution Pending — 본 spec 으로 resolution 경로 확정
- **Hc_040** (Law 1040): primary claim under test
- **Hc_024** (NOBEL-1): primary claim under test
- **Hc_604** (64 dual-seed twin): variance protocol borrowed
- **Hc_004** (Φ ≈ 0.608·N^1.071): N axis baseline
- **Hc_005** (cell-count decisive): N axis dominance

## 7. Honest Limits (≥ 5)

- **L1**: synthetic harness 는 generative model 의 fingerprint 확인용 — 실측 안하면 false-positive 가능 (model A 의 noise σ tuning sensitive)
- **L2**: 15-cell grid (P=100M ceiling, §5.7) 는 sparse — Pareto frontier 의 curvature 정확 측정에 부족 (≥ 50 cell 필요할 수 있음). P=1B deferred extension (§5.7.3) 시 20-cell 로 복원.
- **L3**: CE ∝ P^-0.85 scaling 은 Chinchilla optimal training assumption — under-trained 또는 over-trained regime 에서 다를 수 있음
- **L4**: within-budget vs across-budget partition 의 "budget" 정의가 N+P 의 어떤 monotonic combination 인지 underspecified (FLOPs, params, cell 합산 방식 미정)
- **L5**: phi_star_iit_proxy / phi_star_cell_engine 의 measurement noise floor 가 |corr| 0.05 ~ 0.1 사이 분해능 없으면 mixed verdict 불가피 (engine 명명 §5.8 refactor 2026-05-12)
- **L6**: Hc_024 의 .detach (information barrier) condition — synthetic harness 는 이 조건 미반영 (단순 K=const 가정)
- **L7**: α=0.5 fixed assumption — Hc_024 원본은 α~0.5 라고만 함, optimal α fit 결과가 다를 수 있음
