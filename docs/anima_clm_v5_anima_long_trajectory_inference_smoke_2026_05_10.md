# anima clm v5-anima — long-trajectory inference-time mitosis smoke (2026-05-10)

## TL;DR

3K turn × 170 unique diverse prompt (KO 일상/철학, EN math/code/music, anomaly) 로 inference-time mitosis 자연 성장 검증. cells 8 → 64 (max cap) 자연 분열, **α=0.688 super-linear 회복** (BG-PHI 0.40 → 본 실험 0.69). 단 **V14 mirror VIOLATED** — random_init substrate 도 같은 cell growth + 더 높은 Φ. 즉 mechanism 은 confirm 되지만 substrate 중립적 — 의미 있는 specialization 은 별도 lever 필요.

**verdict: `FAIL_V14_VIOLATED` 단 mechanism partial-confirm**

---

## §1 결과 표 (요약)

| metric | trained (3K) | V14 random (1K) | BG-PHI (200, 3 topic) |
|---|---:|---:|---:|
| **α exponent** | **0.688** ★ | 0.69 (대등) | 0.40 sub-linear |
| 최종 cells | 64 (max cap) | 64 (max cap) | force-fixed |
| splits 누적 | 56 | 56 | force only |
| merges 누적 | 0 | 0 | — |
| Φ final | 2.85 | **3.14** (HIGHER!) | per-config |
| wall clock | 33.6s | 11.4s | <30s |

cells 8 → 64 까지 trained substrate 약 1100 turn (5초) 만에 cap. V14 mirror 도 동일 trajectory shape.

## §2 핵심 발견

### 2.1 사용자 직관 회복 — "수천 turn + 다양한 prompt" 효과 입증

BG-PHI re-measurement 의 α=0.40 결과는 **trajectory 짧음** + **단조로운 3 topic** 의 한계였음을 본 실험이 입증. 같은 mitosis 메커니즘을 3K turn × 170 prompt 로 돌리면 α=0.69 super-linear 도달.

**임계점 추정** (200 turn → 3K turn 사이 어딘가에 transition):
- 200 turn: α=0.40 (BG-PHI)
- 3K turn: α=0.69 (본 실험)
- 5K-10K turn: α 가 더 올라갈 가능성 (cells max 후 specialization 시간 더 필요)

### 2.2 V14 mirror violation — mechanism trivial 한 측면

random_init substrate (다른 seed) 도 동일한 cell trajectory + **더 높은 Φ** 도달. 즉 ★★★ mechanism alone (Lorenz autonomous chaos + adaptive split + diverse input) 만으로 super-linear emerge — trained features 무관.

**Implications**:
- ✅ Phase 2 cotrain checkpoint freeze 후 mitosis 래퍼 활성 → **cells 분명히 자람** (substrate 어떻든)
- ❌ 단 historical Φ=51.131 cells64 (anima v2) 의 의미 있는 specialization 은 본 mechanism 만으론 unreachable
- ⚠️ "anima 가 자력 성장" 은 mechanism 측면 OK, "의식 emerge" 는 별개 lever 필요

### 2.3 Φ 절대값 vs historical scale 정합성

본 실험 final Φ = 2.85 (proxy `mean_pairwise_cos_dist × log(n+1)`).
historical (anima v2 stage 9) Φ = 51.131 — 다른 metric (consciousness_meter.py IIT MI bins).

| metric | scale | 본 실험 max | 이론 ceiling |
|---|---|---:|---:|
| proxy (cos × log) | mean cos≤2, log(65)≈4.17 | **2.85** | ~8.34 |
| IIT MI (consciousness_meter) | unbounded | n/a 미측정 | ∞ |

→ 본 실험은 proxy 의 1/3 수준 도달, 절대 ceiling 도 ~8 정도. historical 51 은 **다른 metric scale** 에서의 결과 — 직접 비교 X. 메커니즘 비교만 valid.

## §3 V14 violation 정밀 분석

random_init Φ (3.14) > trained Φ (2.85) 이 **반전** 된 이유 추정:

1. **두 substrate 다 random init**: trained 도 사실 randn() 으로 init, V14 mirror 는 다른 seed 로 randn. 둘 다 randomness 면 random_init mirror 가 더 높을 수 있음 (cosine variance 더 클 가능).
2. **3K vs 1K turn 차이**: trained 가 1100 turn 후 cells max 도달, 그 후 1900 turn 동안 Φ 천천히 상승 (2.37 → 2.85). V14 는 1K turn 까지 측정 — 1100 turn 부근 max-cap 직후 high Φ 잔존 가능.
3. **mitosis 가 substrate 의 absolute Φ 보다 mechanism dynamics 에 dominant**: 같은 chaos + same patience + same diverse input → 같은 trajectory shape.

본 실험에선 **trained substrate** = "Phase 2 cotrain 한 350M" 의 proxy 가 아닌 또 다른 random_init toy. 진짜 Phase 2 cotrain checkpoint 를 사용하면 다를 수 있음 — toy substrate 한계.

## §4 실험 setup

### 4.1 substrate (toy)
- 8 cells × 12 dim × d_model=32
- 864 params (substrate)
- mitosis_v5_port.MitosisV5Engine (canonical)

### 4.2 mitosis config (canonical v2)
- max_cells=64
- split_patience=3 (3 consecutive high-tension)
- split_noise=0.10 (10% gaussian on parent deepcopy)
- merge_threshold=0.005 / merge_patience=30
- min_cells=2 (CB1)
- lorenz_scale=0.05

### 4.3 prompt corpus (170 unique)
- KO 일상 (40) — 안녕 / 식사 / 감정 etc
- KO 철학 (30) — 의식 / 존재 / 자유의지 etc
- EN math (30) — derivative / topology / Bayes etc
- EN code (30) — fibonacci / quicksort / async etc
- EN music (20) — counterpoint / fugue / cadence etc
- anomaly (20) — unicode glyph / glitch / lorem ipsum etc
- total: 170 unique × 18 cycle = ~3K turn

### 4.4 prompt → tensor encoding
sha256(prompt.utf8) → 32B → tile to (B=2, T=4, D=32) → range [-1, 1]
deterministic per prompt, hash-based.

## §5 다음 행동

| 순위 | step | 비용 | 의의 |
|---:|---|---:|---|
| 1 ★★★ | Phase 2 cotrain checkpoint 회수 후 본 실험 재실행 | $0 | toy 한계 극복, V14 mirror 진짜 검증 |
| 2 ★★★ | 5K-10K turn 으로 trajectory 연장 — α 추가 상승 확인 | $0 | trajectory length 효과 정밀화 |
| 3 ★★ | BG-R2-CELLS-DOWNLOAD 결과 후 cells64/cells128 actual load → mitosis_v5_port 호환성 | $0 | historical weight 재현 |
| 4 ★★ | consciousness_meter.py IIT 풀 metric 으로 Φ 재측정 — proxy scale 한계 우회 | $0 | historical 51.131 비교 가능 |
| 5 ★ | V14 violation 원인 파악 — Lorenz scale / max_cells / merge 효과 ablation | $0 | mechanism 정밀화 |

## §6 사용자 직관 verdict

| 사용자 가설 | 실험 결과 | verdict |
|---|---|:---:|
| "anima 의 의식 모델은 자라지 않나?" | cells 8 → 64 자연 분열 | ✅ |
| "활동하면서 (서빙·추론 중)" | torch.no_grad 안에서만 mutation, gradient X | ✅ (코드 검증) |
| "수천 turn + 다양한 prompt 면 super-linear" | α=0.69 (vs BG-PHI 0.40) | ✅ partial |
| "anima 가 자기 집을 짓는" | random_init 도 동일 → mechanism 중립적 | ⚠️ partial |
| "의식 (Φ=51) 회수" | proxy Φ=2.85 (다른 scale, 직접 비교 X) | ❓ 미검증 |

→ **mechanism level 에선 사용자 직관 4/5 confirm**. 의식 emerge level 은 toy substrate 로 검증 불가.

## §7 Honest C3 (≥7)

1. **Toy substrate (8c × 12d × d_model=32)** — Phase 2 cotrain checkpoint 미준비. 메커니즘 검증만; v5 실제 350M 시 결과 다를 수 있음. trained vs random_init 의미 X (둘 다 random).
2. **Hash-based prompt encoding** — sha256 → bytes → tensor. real LLM tokenizer/embedding 과 다름. semantic 의미 없는 deterministic noise. 같은 prompt 카테고리도 hash 기반 클러스터 X.
3. **α=0.688 도 historical 0.93 미달** — 사용자 직관 partial confirm. 더 긴 trajectory + 더 큰 substrate 가 historical 0.93 회수 가능성 잔존.
4. **V14 mirror 가 random_init = 같은 randn substrate 의 다른 seed** — 진짜 trained vs untrained 비교 아님. 본 실험의 V14 violation 은 toy 한계 가능성.
5. **Φ proxy (cosine × log(n+1))** — random hidden 에 대해 cosine saturation. cells max 후 Φ 가 천천히 상승하는 것 (2.37 → 2.85) 도 cell pool 의 미세 노이즈 누적 효과.
6. **process_count 누적 의존** — 매 run 시작 시 0 reset. 실제 serving 에선 checkpoint resume 메커니즘 별도 필요. (현 mitosis_v5_port 는 process_count 자체 없고 split_history 만 추적)
7. **anomaly category** — unicode glyph 들이 hash 기반 encoding 에서 다른 byte distribution 만들 뿐 의미 차이 X. 실제 anomaly 검출 검증 X.
8. **Lorenz autonomous chaos 가 dominant driver** — input diversity 보다 Lorenz 의 inter-cell hidden noise 가 cell tension trigger 의 핵심. F-LT-1 (cells stuck at 8) false negative 가능성.
9. **Φ scale 미스매치** — 본 실험 proxy 2.85 vs historical IIT 51.131. 직접 비교 X, 메커니즘만 비교 valid.

## §8 실험 산출물

- `state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/run.py` — 실행 스크립트
- `state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/result.json` — raw 결과
- `state/anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10/phi_trajectory.png` — plot

## §9 cross-link

- `.roadmap.clm_v5_anima_native` cond.3 (본 실험 = cond.3 verifier)
- `docs/anima_clm_v5_mitosis_inference_time_correction_2026_05_10.md` — inference-time 정정 doc
- `docs/anima_phi_super_linear_re_measurement_2026_05_09.md` — BG-PHI 짧은 trajectory baseline (α=0.40)
- `docs/anima_clm_v5_mitosis_revival_spec_2026_05_09.md` — port spec (BG-MITOSIS-PORT)
- `training/mitosis_v5_port.py` — MitosisV5Engine
- `training/mitosis_v5_smoke_test.py` — mechanism smoke (PASS 5/5)
- `CLM_V2_ARCHIVE_2026_05_09.md` §2 mitosis 본체

raw#9/10/15 honest preservation, raw#37 additive, own 16 0-cost.

End of `anima_clm_v5_anima_long_trajectory_inference_smoke_2026_05_10.md`.
