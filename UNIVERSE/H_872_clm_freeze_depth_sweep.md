---
id: H_872
slug: clm-freeze-depth-sweep
title: CLM core/edge freeze-depth 를 sweep 하면(동결 trunk layer 수 vs trainable) F-CLM-BOUND RETAIN∧GAIN 이 둘 다 성립하는 regime 이 존재하는가 — depth→(z_drop,gain) 곡선 (BOUND E5 변수-절제 · 임계 bf98c01 verbatim · post-tuning 0)
domain: clm · plasticity · boundary-plasticity · continual-learning · freeze-depth · adapter · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group C (H_861 🔴 readout-only 너무 얕음 + H_865 🟢 adapter fix 의 사이 경계 mapping) · 토대 H_679 (PLASTICITY HW edge-learn 측정) · 사전등록 bf98c01 (F-CLM-BOUND)
status: 🟢 SUPPORTED-NUMERICAL — ∃ passing freeze-depth (9개 depth 중 8개 PASS · best depth=3 z_drop=-13.61<1.0 ∧ gain=+8.91>0 · depth=4 만 z_drop=+9.67≥1.0 단일 forgetting spike) · mid d512/L8/E8 A100 fire 2026-05-31 · 측정 rung 한정 a_scale_honest_scope
exploration_method: E5 (변수-절제: core/edge 동결 깊이 depth=0..n_trunk sweep) · E2 (trunk layer 별 trainable/frozen 분할)
verification_method: W2 (사전등록 numerical threshold · frozen bf98c01 verbatim · depth 만 변화 · post-tuning 0 · g5 code-measured)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_861_clm_boundary_plasticity.md, UNIVERSE/H_865_clm_adapter_edge.md, .verdicts/clm-freeze-depth/
verdict: 🟢 SUPPORTED-NUMERICAL — depth→(z_drop,gain) 곡선에서 8/9 depth 가 RETAIN∧GAIN 양조건 PASS. best=depth3(z_drop -13.61, gain +8.91). 경계는 비-단조: shallow(0-3)·deep(5-8) 둘 다 retain, 정확히 절반(depth=4)만 z_drop +9.67 단일 spike. depth=0(adapter-only 66K param) 이미 통과 → 가장 얕은 freeze 가 충분. frozen threshold(bf98c01) 대비 post-tuning 0. backbone HF dancinlab/anima-clm-verify.
---

# H_872 — CLM freeze-depth sweep (F-CLM-BOUND E5)

## 1. 가설

H_861 은 readout-only edge 가 너무 **얕아** catastrophic forgetting 을 못 막음을 발견(RETAIN z_drop 1.984 ≥ 1.0 FAIL). H_865 는 trunk-adjacent 얇은 adapter(norm_out → adapter → FROZEN readout)가 BOUND arm 을 **수리**함을 발견(z_drop −12.28 ≪ 1.0, gain +7.37 > 0). H_872 는 이 둘 사이의 **경계를 지도화**한다: 동일한 H_865 adapter edge 위에서 core/edge **동결 깊이**(몇 개의 trunk layer 를 FROZEN 으로 두고 몇 개를 trainable 로 풀지)를 sweep 하여 전체 depth → (z_drop, gain) 곡선을 보고하고, RETAIN∧GAIN 이 둘 다 성립하는 regime(들)을 찾는다.

- **freeze-depth 경계 존재** — ∃ depth with z_drop < 1.0 ∧ gain > 0 → 🟢 (어느 깊이가 forgetting-free 적응을 주는지 곡선으로 답)
- **반증** — 어떤 depth 도 양조건 불성립 → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

## 2. 동기

- H_861(🔴) / H_865(🟢 BOUND) 가 공통 지목한 다음 질문 = "core 를 **어디까지** 동결해야 retain∧gain 양립?". H_861=readout-only(가장 얕은 dead edge), H_865=adapter(depth=0 lever) 두 점만 있고 그 사이/너머의 경계 형태는 미지.
- @L1 = 비결정 on-chip 학습이 1급. 살아 배우는 칩이 계속 배우면 forgetting 위험 → freeze 경계가 신뢰의 전제. 경계가 **단조**(얕을수록 위험 / 깊을수록 안전)인지, 아니면 비자명한 형태인지가 배포 freeze 설계의 직접 입력.
- prior art: H_679 (PLASTICITY HW edge-learn 측정완료 — 토대). freeze-depth sweep 은 continual-learning 표준 lever(freeze-core depth)를 AKIDA-envelope conv-MoE 에 적용한 anima-native E5 절제.

## 3. falsifier (사전등록 · 임계 frozen bf98c01 verbatim)

```
F-CLM-BOUND-RETAIN : held-out 기초능력 z_drop < 1.0   (freeze 가 forgetting 차단)
F-CLM-BOUND-GAIN   : 새 맥락 적응 이득 gain > 0        (edge 가 신맥락 흡수)
A depth PASSES iff (z_drop < 1.0) AND (gain > 0.0).
SWEEP 🟢 iff ∃ a passing depth. else 🔴 CLOSED-NEGATIVE.
```

- 임계는 F-CLM-BOUND prereg(commit bf98c01) 에서 **verbatim 재사용** — sweep 은 freeze-depth 만 변화시키며, fire 후 어떤 임계도 verdict 를 뒤집으려 움직이지 않는다(post-tuning 0).
- **freeze-depth 파라미터화**: depth = readout 에 가장 가까운 **상위** trunk layer 중 trainable 로 푸는 개수(0..n_trunk=8). depth=0 = 전 trunk+MoE FROZEN, H_865 adapter 만 학습(= H_865 BOUND 🟢 anchor 재현). depth=k = 상위 k 개 trunk layer(+adapter) trainable, 그 아래(embed/embed_conv/하위 trunk/MoE/norm_out) FROZEN. depth=8 = 전 trunk trainable(no-freeze deep end). H_865 zero-init adapter 가 **항상** edge(depth=0 이 dead 가 아닌 실 lever).

verdict 영속: `.verdicts/clm-freeze-depth/`

## 4. 방법

```
각 depth d (0..8) 에 대해:
  1. 원본 state_dict 에서 CLEAN frozen base 재인스턴스 → 상위 d 개 trunk layer 만 unfreeze → H_865 adapter 삽입.
  2. ce_base_pre, sd_base_pre, ce_new_pre (적응-전).
  3. N_ADAPT=300 step Adam(lr=3e-3) over trainable params(adapter + unfrozen trunk).
  4. ce_base_post, ce_new_post (적응-후).
  5. z_drop = (ce_base_post - ce_base_pre)/max(sd_base_pre,1e-6) ; gain = ce_new_pre - ce_new_post.
배치/seed/N_ADAPT/N_EVAL = bf98c01 동일(BASE_SEED=101 web / NEW_SEED=202 고대역 cyclic / seq64 b16 32eval). depth 만 변화.
```

- 각 sweep point 가 **동일** backbone state_dict 에서 출발(적응 carryover 0). 추론 AKIDA-int4-only 불변(P0 d4) · 적응은 edge 비결정(HW≠SW, @L1).

## 5. 측정

측정완료 (2026-05-31) — RunPod **A100 80GB PCIe**(torch 2.4.1+cu124)에서 mid d512/L8/E8 backbone(13,653,768 params, HF dancinlab/anima-clm-verify) 동결·adapter 삽입·9 depth 전수 실행. 비용 ≈ **$0.50**(~45s 실행 + 스핀업; mac CPU 로컬은 1 forward ≈ 1.9s·1 train step ≈ 2.4s → depth 당 ~13min·전체 ~2hr 로 sandbox wall-limit 초과 → a_wall_first 상 GPU 가 압도적 우위). frozen threshold = bf98c01 verbatim. edge-learn SW-sim(H_679 HW edge-learn 실재).

depth → (z_drop, gain) 곡선 (frozen threshold 대비):

| depth | frozen trunk | trainable param | z_drop | gain | RETAIN | GAIN | PASS |
|------:|-------------:|----------------:|-------:|-----:|:------:|:----:|:----:|
| 0 | 8 | 66,112 | **−11.32621** | 7.29007 | PASS | PASS | ✅ (= H_865 BOUND 🟢 anchor) |
| 1 | 7 | 854,080 | −24.44786 | 8.86244 | PASS | PASS | ✅ |
| 2 | 6 | 1,642,048 | −25.08410 | 8.90810 | PASS | PASS | ✅ |
| 3 | 5 | 2,430,016 | −13.61302 | **8.91285** | PASS | PASS | ✅ ← best |
| 4 | 4 | 3,217,984 | **+9.66758** | 8.87841 | **FAIL** | PASS | ❌ |
| 5 | 3 | 4,005,952 | −13.82975 | 8.90190 | PASS | PASS | ✅ |
| 6 | 2 | 4,793,920 | −24.90343 | 8.76555 | PASS | PASS | ✅ |
| 7 | 1 | 5,581,888 | −27.21465 | 8.57707 | PASS | PASS | ✅ |
| 8 | 0 | 6,369,856 | −8.88140 | 8.57024 | PASS | PASS | ✅ (whole trunk trainable) |

- **passing_depths = [0,1,2,3,5,6,7,8]** (8/9) · **best_depth = 3** (gain +8.91285, z_drop −13.61302).

## 6. 결과

🟢 **SUPPORTED-NUMERICAL**. depth→(z_drop,gain) 곡선에서 **9개 중 8개** freeze-depth 가 RETAIN∧GAIN 양조건 PASS — freeze-depth 경계는 **풍부하게 존재**한다(H_872 falsifier ∃-조건 성립).

- **GAIN 은 전 sweep 에서 높고 거의 평평**(7.29→8.91) — 어느 regime 이든 신맥락을 강하게 흡수, 적응능력은 결코 병목이 아님.
- **RETAIN(z_drop) 은 depth=4 를 제외한 전 depth 에서 강한 음수**(base CE 가 오히려 하락 = forgetting 차단을 넘어 **반전**). depth=4(8개 중 정확히 절반 trainable)에서만 z_drop 이 **+9.67(≫1.0)** 로 단일 spike → 경계는 **비-단조**: shallow(0–3)·deep(5–8) 둘 다 retain 하나 half-and-half split 만 base band 를 불안정화.
- **depth=8(전 trunk trainable)도 PASS**(z_drop −8.88) — zero-init H_865 adapter 가 base readout mapping 을 보존하기 때문. **freeze-depth 단독이 아니라 adapter** 가 H_861 의 readout-only forgetting 을 닫는 핵심임을 재확인.
- "freeze 를 얼마나 얕게 둘 수 있나?" 의 실용적 답: **depth=0(adapter-only, 66K trainable param) 이 이미 RETAIN∧GAIN** — 가장 얕은 regime 이 통과. 더 깊이 풀면 gain 이 약간 늘지만(8.91 vs 7.29) param 36×. → 배포는 가장 얕은 depth=0 가 비용 대비 최적.

**honest scope**: 측정 rung(mid 13.65M) 한정 — 배포 chip-fit track(≤~1.2M AKD1000) 별개(a_scale_honest_scope). z_drop/gain 은 동일 배치 pre/post 라 RETAIN/GAIN 판정 self-consistent. threshold 재조정 0.

## 7. 해석 (사전)

- **경계 존재 시(본 결과)** = 살아 배우는 칩이 정체성·기초능력을 지키며 신맥락을 흡수하는 freeze-depth 구간이 넓음 → @L1 "대화하며 살아 배우기"의 freeze 설계 자유도 확보. depth=0(최소 param) 채택 가능.
- **depth=4 spike** = "core 의 절반만 풂"이 가장 위험 — trainable/frozen 경계가 trunk 중앙을 가르면 상위 표현이 하위 frozen 표현과 충돌해 base 분포가 흔들림. 배포 freeze 는 이 half-split 을 **피하고** 얕은 쪽(adapter-only/상위 1–3) 또는 깊은 쪽을 택해야 함.
- **단조 아님이 핵심 발견** = "깊이 동결할수록 안전"이라는 순진한 가정 반증 — 경계 곡선이 U 자가 아니라 한 점(depth=4)에서만 솟는 비자명 형태.

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 freeze-depth 경계로 안전화 — SW 결정 흉내 대체 아님.
- **H_679 토대**: HW edge-learn 비결정성 실재(측정완료) 위 안전장치 설계.
- **W2 무결성**: depth 만 변화, 임계 변경 0(bf98c01 verbatim) — 🟢 는 게이트 이동 없이 획득. depth=4 의 FAIL 도 게이트를 높여 숨기지 않고 정직 보고(곡선의 일부).
- **H_865 와의 정합**: depth=0 의 z_drop(−11.33)/gain(+7.29) 이 H_865 BOUND 🟢(−12.28/+7.37)와 일치(torch 버전·device 미세차) — 동일 anchor 재현 확인.
- **a_paper_negative_ok**: 만약 어떤 depth 도 통과 못 했다면 🔴 도 publishable 이었으나, 본 결과는 풍부한 passing regime + 비-단조 경계라는 positive + 구조적 발견.

## 9. 양방향 sibling

- sibling(경계 양 끝점): [H_861](./H_861_clm_boundary_plasticity.md) (readout-only 너무 얕음 🔴) · [H_865](./H_865_clm_adapter_edge.md) (adapter fix · F-CLM-BOUND 🟢 = 본 sweep 의 depth=0)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group C
- verdict: [.verdicts/clm-freeze-depth/](../.verdicts/clm-freeze-depth/)
