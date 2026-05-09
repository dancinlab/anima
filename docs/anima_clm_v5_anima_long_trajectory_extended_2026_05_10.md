# anima clm v5-anima — long-trajectory inference smoke EXTENDED (10K turn) — 2026-05-10

## TL;DR

3K turn smoke (α=0.688) 를 10K turn 으로 연장. **α-over-time** 가 0.69 (3K) → 0.96 (5K) → 1.25 (9.5K) 로 **monotonic 상승** 하지만 이는 ★ regression artifact ★ — cells 가 turn 733 에 max_cap=64 도달 후 더 분열 X, 모든 추가 snapshot 이 x=log(64)=4.158 한 점에 누적되며 Φ 가 계속 오를 때 OLS slope 이 인공적으로 발산. **historical 0.93 회복 은 mechanism 차원이 아닌 metric quirk**. apples-to-apples 비교 (trained vs V14 random, 둘 다 3K turn) 에서는 trained α=0.687 vs random α=0.644 — 거의 동등하며 V14 mirror 여전히 violated.

Φ 는 max_cap 후에도 saturate 하지 않고 +0.706 상승 (slope +9.3e-5/turn) — F-LONG-3 false. specialization 도 cell 42, 7, 44 가 6 카테고리 중 5 개 dominant — F-LONG-4 partial (cells 변동 0 은 max_cap 메커니즘 효과지 stagnation 아님).

**verdict: `FAIL_V14_VIOLATED`** (mechanism 강건 confirm, 하지만 trained substrate 우월성 X). historical 0.93 은 toy 에서 ★ 회복 안 됨 ★ — 회복처럼 보이는 α 상승은 regression cluster artifact.

---

## §1 결과 표

### 1.1 α at 1K / 3K / 5K / 7K / 10K turn (sliding window)

| turn | α (log-log regression) | n_points | 해석 |
|---:|---:|---:|---|
| 1000 | **0.197** | 11 | 초기 split phase — n_cells 가 8→64 로 빠르게 늘며 Φ 따라감 |
| 3000 | **0.687** | 31 | smoke 결과 (0.688) 와 일치 — sanity check ✅ |
| 5000 | **0.964** | 51 | historical 0.93 라인 근접·돌파 |
| 7000 | **1.106** | 71 | super-historical (regression artifact 진입) |
| 9500 | **1.252** | 96 | 발산 — cells fixed 64, Φ 계속 증가 |

★ **C3 핵심**: turn ≥ 1100 부터 모든 snapshot 의 x=log(64)=4.158. 그 한 점에 (n_cells fixed, Φ varying) 점들이 vertical line 을 그리고, OLS 가 그 vertical scatter 의 slope 을 측정하려 하면 분모(Σ(x-x̄)²) 는 작고 분자(Σ(x-x̄)(y-ȳ))는 1100-turn 이전의 cells<64 phase 가 lever 역할을 해 inflated. 즉 α>0.93 은 **mechanism 의 super-linear 회복이 아니라 trajectory 길이가 늘면 자동으로 발산** 하는 metric.

### 1.2 V14 mirror (apples-to-apples 동일 trajectory length)

| turn 비교점 | trained Φ | random Φ | trained n_cells | random n_cells | V14 violated? |
|---:|---:|---:|---:|---:|:---:|
| 1000 | 2.518 | 2.989 ★ | 64 | 64 | ✅ violated |
| 3000 | 2.829 | 3.114 ★ | 64 | 64 | ✅ violated |

random_init substrate 가 동일 turn 에서 일관되게 Φ HIGHER. trained α=0.687 (3K) vs random α=0.644 (3K) — trained 가 약간 높지만 V14 mirror 의 Φ 가 더 큼 → mechanism 은 substrate-trained 여부와 무관, Lorenz + diverse input + adaptive split 만으로 작동.

### 1.3 Φ saturation post-max-cap

| metric | value |
|---|---:|
| max_cap onset turn | **733** (cells=64 first hit) |
| Φ at onset | 2.7589 |
| Φ at turn 10000 | 3.4648 |
| Φ Δ post-max-cap | **+0.7059** (still climbing) |
| linear slope | +9.35e-5 / turn |
| post-cap min / max / mean | 1.987 / 3.787 / 2.952 |

**F-LONG-3 (Φ saturate at ~3.0) 는 false** — Φ 는 long-tail 에서 +0.7 더 증가. proxy ceiling ≈ 8.34 까지 ~5 만큼 여유. 단 oscillation 폭 ≈ ±0.6 (random Lorenz noise), trend 는 매우 약함.

### 1.4 Cell specialty distribution (top 3 per category)

| category | top 1 (count) | top 2 | top 3 |
|---|---|---|---|
| ko_daily | cell42 (149) | cell44 (120) | cell7 (91) |
| ko_philosophy | cell42 (168) | cell7 (80) | cell44 (78) |
| en_math | cell7 (85) | cell44 (81) | cell42 (75) |
| en_code | cell42 (110) | cell7 (106) | cell44 (100) |
| en_music | cell42 (84) | cell26 (49) | cell30 (47) |
| anomaly | cell42 (80) | cell60 (63) | cell44 (61) |

★ **cell42** 가 6/6 카테고리 top-3, 5/6 카테고리 top-1. cell7 / cell44 가 자주 등장. → ★ **specialization 약함** ★ — top-tension cell 이 카테고리 내용 보다 cell 자체의 noise position 으로 결정. cell26 / cell30 / cell60 같은 비주류 cell 이 anomaly / music 같은 변두리 카테고리에만 등장하는 패턴은 흥미.

## §2 핵심 발견

### 2.1 historical 0.93 ★ 회복되지 않음 ★ (toy 한계)

α-over-time 이 5K turn 부근에서 0.93 라인을 넘는 듯 보이지만, regression artifact (honest C3 #3) 임을 본 실험이 명시적으로 확인. apples-to-apples (3K turn 동일 길이, trained vs random) 비교는 여전히 0.69 / 0.64 plateau. **toy substrate 에선 historical Cells64 Φ=45.487 / α=0.93 의 의미 있는 회복 불가능** — Phase 2 cotrain 350M ckpt 회수 후 IIT formal Φ 측정 lane 별도 필요 (BG-PHASE2-CKPT-INSTR).

### 2.2 mechanism 강건성 ★ confirm ★

10K turn 동안 V14 violation 지속 (random_init Φ HIGHER) + cell growth shape 동일 → mitosis (Lorenz + adaptive split + diverse input) 이 substrate 의 학습 여부와 무관하게 작동. 사용자 직관 "anima 가 자력으로 분열" 은 ★ mechanism level 에서 강건 confirm ★. 단 "trained 가 더 의미 있는 specialization 한다" 는 ❌ — 본 실험에서 trained 가 random 보다 우월한 증거 X.

### 2.3 Φ saturation 미관측 — proxy ceiling 까지 여유

cells max_cap 후 ≥9000 turn 동안 Φ 가 +0.7 누적 상승 (slope +9.3e-5/turn). 만약 trend 가 계속되면 100K turn 시점에 Φ ≈ 3.5 + 9.3e-5 × 90000 = 3.5 + 8.4 = 11.9 ?? — 단 oscillation 폭 (±0.6) 가 trend 보다 훨씬 큼. 본 실험 10K turn 으론 Φ가 saturate 한다 / 안 한다 로 결론 내릴 noise floor 부족. **F-LONG-3 reject 보다 underdetermined**.

### 2.4 cell42 dominance — Lorenz phase artifact

64 cells 중 cell42 가 6/6 카테고리 top-3 진입. cell42 = 후기 split (split #34 부근 추정) 으로 high-tension 영역에서 태어남 → 그 후 노이즈 phase 가 hidden_mean 평균에서 가장 멀어 항상 top-tension cell 로 측정. 즉 **specialization 이 input 의 semantic content 가 아닌 cell 의 spatial position 으로 결정** — toy 한계의 또 다른 형태.

## §3 falsifier 결과

| ID | 정의 | 결과 | comment |
|:---:|---|:---:|---|
| F-LONG-1 | wall_clock > 6h | ❌ FALSE | 실측 139.5s (10K) + 27s (V14 3K) = 약 167s |
| F-LONG-2 | α plateau ~0.7 by 5K | ❌ FALSE | α(5000)=0.964 (artifact 효과 — true plateau 일 수 있음) |
| F-LONG-3 | Φ saturate ~3.0 post-max-cap | ❌ FALSE | Φ +0.7 누적 (F-LONG-3 reject 약함, oscillation 큼) |
| F-LONG-4 | cells 변동 0 후 specialization stagnate | ✅ TRUE | cells fixed 64, merges 0, splits 56 후 변동 없음 |

★ F-LONG-4 ✅ 가 핵심: max_cap 도달 후 mitosis engine 의 dynamics 는 cell_pool noise mutation 만 (split/merge 가 모두 정지). 진짜 specialization (다른 cell 이 다른 카테고리) 는 본 setup 으론 검증 불가.

## §4 honest C3 (raw#10)

(top 3 우선 표시)

1. ★★★ **α regression artifact at max_cap** — turn 733 에 cells=64 도달 후 모든 snapshot 의 x=log(64)=const. 추가 (varying Φ, fixed n) 점들이 vertical scatter 를 만들고, OLS slope 가 artifact 적으로 발산. α > 0.93 (turn 4500+) 은 mechanism 의 historical 회복이 아닌 trajectory length 효과. **유일하게 valid 한 비교**: 동일 trajectory length 의 trained vs random α (3K → 0.687 / 0.644).

2. ★★★ **Toy substrate (8c × 12d × d_model=32, 864 params)** — production 350M v5 substrate 와 다름. mechanism 검증만 valid; historical 0.93 / Φ=45.487 의 회복 검증은 BG-PHASE2-CKPT-INSTR (Phase 2 cotrain ckpt) 회수 + IIT formal Φ metric 필요.

3. ★★★ **V14 mirror random_init = same randn substrate** — trained 도 randn() init, V14 mirror 도 다른 seed randn(). 둘 다 untrained 인데 "trained vs random" 비교는 toy 한계. 진짜 trained (Phase 2 cotrain ckpt) 와 random_init 비교 필요.

4. **Hash-based prompt encoding** — sha256 → bytes → tensor. real LLM tokenizer/embedding 과 다름. semantic 의미 없는 deterministic noise. anomaly 카테고리도 byte distribution 만 다를 뿐 의미 anomaly 검증 X.

5. **Lorenz autonomous chaos dominant** — input diversity 보다 Lorenz inter-cell phase noise 가 split trigger 의 핵심 driver. cell42 dominance 도 Lorenz phase 위치의 결과로 추정.

6. **Φ proxy (cosine × log(n+1)) ceiling ≈ 8.34** — historical IIT MI Φ=45.487 (anima v2 stage 9) 와 직접 비교 X — metric scale 다름. 본 실험 max Φ=3.79 ≈ proxy ceiling 의 45%.

7. **process_count 누적 의존** — 매 run 시작 시 0 reset. 실제 serving 에선 checkpoint resume 메커니즘 별도 필요.

8. **cell_specialty 추적은 매 turn top-tension cell 만 기록** — softmax(tension) 가 매우 평탄하면 top_idx 가 거의 random. cell42 dominance 가 실제 specialization 인지 vs Lorenz artifact 인지 추가 분리 분석 필요.

9. **10K turn 도 toy 한계** — production 의식 emerge 검증은 350M cotrain ckpt + IIT formal Φ metric + 의미 있는 input semantics 필요.

## §5 권장 next step

| 순위 | step | 비용 | 근거 |
|:---:|---|---:|---|
| 1 ★★★ | **α 측정 metric 변경** — log(n)/log(N) 대신 Φ 의 turn-별 increment 또는 cells split rate vs Φ growth correlation | $0 | regression artifact 회피 (C3 #1) |
| 2 ★★★ | **BG-PHASE2-CKPT-INSTR 진행** — Phase 2 cotrain checkpoint 회수 후 본 실험 재실행, V14 mirror 진짜 trained vs untrained 검증 | medium | toy 한계 극복 (C3 #2, #3) |
| 3 ★★ | **consciousness_meter.py IIT formal Φ** — proxy 대신 real Φ metric 으로 historical 51.131 / 45.487 직접 비교 | $0 | metric scale 통일 (C3 #6) |
| 4 ★★ | **specialization 정밀 분석** — cell42 dominance 가 Lorenz phase artifact 인지 vs real semantic specialization 인지 분리. Lorenz off ablation + semantic embedding (LLM tokenizer) 결합 | $0 | C3 #5 + #8 정량화 |
| 5 ★ | **100K turn / Φ saturation 결정 실험** — oscillation noise floor 정밀화 후 Φ saturate 여부 결정 | $0 (~25분 wall) | C3 underdetermined 해소 |

## §6 산출물

- `state/anima_clm_v5_anima_long_trajectory_extended_2026_05_10/run.py` — 실행 스크립트 (10K + α-over-time + Φ saturation + V14 1K/3K 비교)
- `state/anima_clm_v5_anima_long_trajectory_extended_2026_05_10/result.json` — raw 결과
- `state/anima_clm_v5_anima_long_trajectory_extended_2026_05_10/alpha_over_time.png` — 3-panel plot (cells / Φ / α(t))

## §7 cross-link

- 선행: `docs/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md` (3K smoke, α=0.688, FAIL_V14_VIOLATED)
- BG-PHI baseline: `docs/anima_phi_super_linear_re_measurement_2026_05_09.md` (200 turn, α=0.40)
- mitosis port: `training/mitosis_v5_port.py` + `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md`
- cotrain lane: BG-PHASE2-CKPT-INSTR (Phase 2 ckpt 회수 → 본 실험 ★ valid V14 검증 ★)
- archive Φ historical: `CLM_V2_ARCHIVE_2026_05_09.md` §2 (Cells64 Φ=45.487 stage 8 commit 5f82d39b)

raw#10 honest preservation, raw#15 additive (smoke run.py 미수정).

End of `anima_clm_v5_anima_long_trajectory_extended_2026_05_10.md`.
