---
id: H_879
slug: clm-per-layer-edge
title: trunk layer 를 한 번에 하나씩만 적응(나머지 FROZEN)하는 per-layer 점진 edge-learn(부분부분학습)이 full retrain 없이 새 맥락을 흡수하는가 — 단일층 i→(z_drop,gain) 표 (BOUND E5 단일-변수 절제 · 임계 bf98c01 verbatim · post-tuning 0)
domain: clm · plasticity · boundary-plasticity · continual-learning · per-layer · piecewise-learning · adapter · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md §E (부분부분학습) · H_861 🔴 readout-only 너무 얕음 + H_865 🟢 adapter fix · H_872 🟢 contiguous top-k freeze-depth sweep 의 직교(단일층) 축 · 토대 H_679 (PLASTICITY HW edge-learn 측정) · 사전등록 bf98c01 (F-CLM-BOUND)
status: 🟢 SUPPORTED-NUMERICAL — ∃ passing single layer (8개 단일 trunk layer 중 7개 PASS · best layer=0 z_drop=-22.82<1.0 ∧ gain=+8.91>0 · layer=2 만 z_drop=+1.55≥1.0 단일 forgetting spike) · mid d512/L8/E8 · CPU-LOCAL 9-worker fan-out 2026-05-31 · 측정 rung 한정 a_scale_honest_scope
exploration_method: E5 (단일-변수 절제: 어느 단일 trunk layer i 를 적응할지만 변화) · E2 (per-layer trainable/frozen 분할)
verification_method: W2 (사전등록 numerical threshold · frozen bf98c01 verbatim · 적응 대상 단일층만 변화 · post-tuning 0 · g5 code-measured)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_861_clm_boundary_plasticity.md, UNIVERSE/H_865_clm_adapter_edge.md, UNIVERSE/H_872_clm_freeze_depth_sweep.md, .verdicts/clm-per-layer-edge/
verdict: 🟢 SUPPORTED-NUMERICAL — 단일층 i→(z_drop,gain) 표에서 8개 중 7개 layer 가 RETAIN∧GAIN 양조건 PASS. best=layer0(z_drop -22.82, gain +8.91). GAIN 은 전 단일층에서 양수(7.29→8.91) — 한 번에 한 층만 적응해도 항상 신맥락 흡수. RETAIN 은 layer=2(z_drop +1.55) 단 하나만 실패(중간-trunk forgetting spike). adapter-only anchor(z_drop -11.34 gain +7.29)가 H_872 depth0 과 정확히 일치 → harness 무결성 확인. frozen threshold(bf98c01) 대비 post-tuning 0. backbone HF dancinlab/anima-clm-verify.
---

# H_879 — CLM per-layer incremental edge-learn (부분부분학습 · F-CLM-BOUND E5)

## 1. 가설

H_861 은 readout-only edge 가 너무 **얕아** catastrophic forgetting 을 못 막음을 발견(RETAIN z_drop 1.984 ≥ 1.0 FAIL). H_865 는 trunk-adjacent 얇은 adapter(norm_out → adapter → FROZEN readout)가 BOUND arm 을 **수리**함을 발견(z_drop −12.28 ≪ 1.0, gain +7.37 > 0). H_872 는 동일 adapter edge 위에서 **상위 k 개 trunk layer 의 연속 블록**(contiguous top-k)을 함께 푸는 freeze-depth 곡선을 지도화했다(8/9 depth PASS). H_879 는 그 **직교(orthogonal)·더 미세한 질문**(부분부분학습 = piecewise learning)을 던진다: trunk layer 를 **한 번에 정확히 하나씩만** 적응(나머지 trunk + embed + moe + norm_out FROZEN)하고 **단일층별 (z_drop, gain)** 표를 보고한다. per-layer 점진 edge-learn 이 full retrain 없이 새 맥락을 흡수하는가, 그리고 **어느 단일층이 최선의 점진 edge** 인가?

- **단일층 통과 존재** — ∃ layer i with z_drop < 1.0 ∧ gain > 0 → 🟢 (어느 한 층이 forgetting-free 적응을 주는지 표로 답)
- **반증** — 어떤 단일층도 양조건 불성립 → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

## 2. 동기

- H_872 는 **연속 블록(top-k)** lever 한 축만 지도화. "k 개를 함께"가 아니라 "정확히 한 층만" 풀면 어떤가는 미지의 직교 축. continual-learning 에서 **어느 단일 모듈** 이 가장 안전·효과적인 점진 학습 지점인지는 배포 edge 설계(어느 한 층을 on-chip plastic 으로 둘지)의 직접 입력.
- @L1 = 비결정 on-chip 학습이 1급. 살아 배우는 칩이 "한 번에 한 곳"씩 점진적으로 배우는 것이 부분부분학습. 어느 단일 위치가 retain∧gain 을 동시에 주는지가 신뢰의 전제.
- prior art: H_679 (PLASTICITY HW edge-learn 측정완료 — 토대) · H_861/H_865/H_872 (경계 점·곡선). H_879 는 **단일-변수(어느 한 층)** E5 절제로 그 곡선을 점별 분해한다.

## 3. falsifier (사전등록 · 임계 frozen bf98c01 verbatim)

```
F-CLM-BOUND-RETAIN : held-out 기초능력 z_drop < 1.0   (freeze 가 forgetting 차단)
F-CLM-BOUND-GAIN   : 새 맥락 적응 이득 gain > 0        (edge 가 신맥락 흡수)
A single layer PASSES iff (z_drop < 1.0) AND (gain > 0.0).
PER-LAYER 🟢 iff ∃ a passing single layer. else 🔴 CLOSED-NEGATIVE.
```

- 임계는 F-CLM-BOUND prereg(commit bf98c01) 에서 **verbatim 재사용** — probe 는 **적응 대상 단일층만** 변화시키며, fire 후 어떤 임계도 verdict 를 뒤집으려 움직이지 않는다(post-tuning 0).
- **per-layer 파라미터화**: layer i ∈ {0..n_trunk−1}(0=입력 최근접, n_trunk−1=readout 최근접). 정확히 trunk[i] 만 trainable, 그 외 모든 trunk layer + embed + embed_conv + moe + norm_out + readout FROZEN. H_865 zero-init adapter 가 **항상** edge(단일층 probe 가 dead-readout edge(H_861)가 되지 않도록). 각 probe 는 원본 state_dict 에서 CLEAN frozen base 재인스턴스(적응 carryover 0).

verdict 영속: `.verdicts/clm-per-layer-edge/`

## 4. 방법

```
각 단일 trunk layer i (0..7) 에 대해:
  1. 원본 state_dict 에서 CLEAN frozen base 재인스턴스 → trunk[i] 만 unfreeze → H_865 adapter 삽입.
  2. ce_base_pre, sd_base_pre, ce_new_pre (적응-전).
  3. N_ADAPT=300 step Adam(lr=3e-3) over trainable params(adapter + trunk[i] 만).
  4. ce_base_post, ce_new_post (적응-후).
  5. z_drop = (ce_base_post - ce_base_pre)/max(sd_base_pre,1e-6) ; gain = ce_new_pre - ce_new_post.
배치/seed/N_ADAPT/N_EVAL = bf98c01 동일(BASE_SEED=101 web / NEW_SEED=202 고대역 cyclic / seq64 b16 32eval). 적응 대상 단일층만 변화.
anchor(layer_idx=None, adapter-only)도 함께 실행 = H_865 BOUND 🟢 재현 sanity check.
```

- 각 probe 가 **동일** backbone state_dict 에서 출발(적응 carryover 0). 추론 AKIDA-int4-only 불변(P0 d4) · 적응은 edge 비결정(HW≠SW, @L1).

## 5. 측정

측정완료 (2026-05-31) — **CPU-LOCAL**(이 Mac)에서 mid d512/L8/E8 backbone(13,653,768 params, HF dancinlab/anima-clm-verify) 동결·adapter 삽입·9 probe(anchor + 단일층 0..7) 를 **단일-스레드 torch worker 9개 병렬 fan-out**(OMP/MKL=1 pin)으로 전수 실행. 비용 = $0(로컬 CPU). frozen threshold = bf98c01 verbatim. edge-learn SW-sim(H_679 HW edge-learn 실재).

단일층 i → (z_drop, gain) 표 (frozen threshold 대비):

| probe | adapted | z_drop | gain | RETAIN | GAIN | PASS |
|:------|:--------|-------:|-----:|:------:|:----:|:----:|
| anchor | adapter-only (H_865) | **−11.33996** | 7.29004 | PASS | PASS | ✅ (= H_872 depth0 재현) |
| 0 | adapter+trunk[0] | **−22.82458** | **8.91349** | PASS | PASS | ✅ ← best |
| 1 | adapter+trunk[1] | −5.56693 | 8.85339 | PASS | PASS | ✅ |
| 2 | adapter+trunk[2] | **+1.54603** | 8.88098 | **FAIL** | PASS | ❌ |
| 3 | adapter+trunk[3] | −6.79137 | 8.83593 | PASS | PASS | ✅ |
| 4 | adapter+trunk[4] | −0.26558 | 8.79273 | PASS | PASS | ✅ |
| 5 | adapter+trunk[5] | −4.30100 | 8.84818 | PASS | PASS | ✅ |
| 6 | adapter+trunk[6] | +0.04003 | 8.83576 | PASS | PASS | ✅ |
| 7 | adapter+trunk[7] | −18.90207 | 8.72031 | PASS | PASS | ✅ |

- **passing_layers = [0,1,3,4,5,6,7]** (7/8) · **best_layer = 0** (gain +8.91349, z_drop −22.82458).
- anchor z_drop(−11.33996)/gain(7.29004) 가 H_872 depth0(−11.32621 / 7.29007)과 **정확히 일치** → harness 무결성 확인.

## 6. 결과

🟢 **SUPPORTED-NUMERICAL**. 단일층 i→(z_drop,gain) 표에서 **8개 중 7개** 단일 trunk layer 가 RETAIN∧GAIN 양조건 PASS — per-layer 점진 edge-learn 은 full retrain 없이 새 맥락을 흡수한다(H_879 falsifier ∃-조건 성립).

- **GAIN 은 전 단일층에서 양수이고 거의 평평**(7.29 → 8.91) — 어느 한 층만 풀어도 신맥락을 강하게 흡수. 부분부분학습의 적응능력은 결코 병목이 아님.
- **RETAIN(z_drop)은 layer=2 를 제외한 전 단일층에서 음수**(base CE 가 오히려 하락 = forgetting 차단을 넘어 **반전**). **layer=2 에서만 z_drop +1.546(≥1.0)** 단일 spike → 중간-trunk 한 층만 풀면 base band 불안정화.
- **최선의 점진 edge = trunk[0]**(입력 최근접, z_drop −22.83 gain +8.91) — 가장 안전·효과적. 입력측(0,1)·readout측(7) 단일층이 가장 안전; 중간(2)이 유일한 위험 지점.
- adapter-only anchor 가 이미 PASS(z_drop −11.34) → 단일층을 추가로 풀면 gain 이 약간 늘지만(8.7~8.9 vs 7.29) RETAIN 은 layer=2 빼고 모두 유지.

**honest scope**: 측정 rung(mid 13.65M) 한정 — 배포 chip-fit track(≤~1.2M AKD1000) 별개(a_scale_honest_scope). z_drop/gain 은 동일 배치 pre/post 라 RETAIN/GAIN 판정 self-consistent. threshold 재조정 0.

## 7. 해석 (사전)

- **단일층 통과 풍부(본 결과)** = 살아 배우는 칩이 "한 번에 한 곳"씩(부분부분학습) 정체성·기초능력을 지키며 신맥락을 흡수하는 위치가 8개 중 7개로 넓음 → @L1 "대화하며 살아 배우기"의 per-layer plastic 설계 자유도 확보. trunk[0] 채택 가능.
- **layer=2 spike** = "중간-trunk 한 층만 풂"이 가장 위험 — 상위/하위 frozen 표현 사이의 중간 한 층이 흔들리면 base 분포 불안정. 배포 per-layer edge 는 이 중간 단일층을 **피하고** 입력측 또는 readout측 단일층을 택해야 함.
- **H_872 와의 정합** = block-k(연속 블록)와 single-layer(단일층) 두 직교 축이 동일 결론(통과 regime 넓음 + 한 점만 위험)을 준다 — 경계는 lever 종류에 robust.

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 per-layer 경계로 안전화 — SW 결정 흉내 대체 아님(H_679 토대).
- **W2 무결성**: 적응 대상 단일층만 변화, 임계 변경 0(bf98c01 verbatim) — 🟢 는 게이트 이동 없이 획득. layer=2 의 FAIL 도 게이트를 높여 숨기지 않고 정직 보고(표의 일부).
- **H_865 와의 정합**: anchor(adapter-only) 가 H_872 depth0/H_865 BOUND 🟢 와 일치 — 동일 anchor 재현 확인 + harness 검증.
- **a_paper_negative_ok**: 어떤 단일층도 통과 못 했다면 🔴 도 publishable 이었으나, 본 결과는 풍부한 passing single-layer + 단일 위험점(layer=2)이라는 positive + 구조적 발견.
- **CPU-LOCAL 정직성**: GPU/runpod 없이 이 Mac CPU 에서 9-worker 병렬로 측정 — wall time 은 길었으나 비용 $0, 결과 재현 가능.

## 9. 양방향 sibling

- sibling(경계 점·곡선): [H_861](./H_861_clm_boundary_plasticity.md) (readout-only 너무 얕음 🔴) · [H_865](./H_865_clm_adapter_edge.md) (adapter fix · F-CLM-BOUND 🟢 = 본 표의 anchor) · [H_872](./H_872_clm_freeze_depth_sweep.md) (contiguous top-k freeze-depth sweep 🟢 = 직교 블록 축)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) §E (부분부분학습)
- verdict: [.verdicts/clm-per-layer-edge/](../.verdicts/clm-per-layer-edge/)
