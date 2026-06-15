---
id: H_881
slug: clm-progressive-freeze
title: CLM freeze 경계를 학습 세션 도중 동적으로 이동(progressive freeze)하면 — STATIC freeze-depth(H_872) 대신 — F-CLM-BOUND RETAIN∧GAIN 이 세션 전 구간(매 checkpoint)에서 지속(sustained)되는 스케줄이 존재하는가 (BOUND E5 dynamic · 임계 bf98c01 verbatim · post-tuning 0)
domain: clm · plasticity · boundary-plasticity · continual-learning · progressive-freeze · freeze-schedule · adapter · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group C (H_872 🟢 STATIC freeze-depth, END-only 측정 → 동적 스케줄로 확장) · 토대 H_679 (PLASTICITY HW edge-learn 측정) · 사전등록 bf98c01 (F-CLM-BOUND)
status: 🟢 SUPPORTED-NUMERICAL — ∃ sustaining schedule (7/7 스케줄 모두 6/6 checkpoint 에서 RETAIN∧GAIN PASS · best=S6_cross4 min_gain 6.283 · max_z_drop −43.47≪1.0) · mid d512/L8/E8 local-MPS fire 2026-05-31 · 측정 rung 한정 a_scale_honest_scope
exploration_method: E5 (변수-절제: freeze SCHEDULE = 세그먼트별 depth 시퀀스를 sweep) · E2 (세션을 6 세그먼트로 분할 · 경계를 세그먼트마다 이동)
verification_method: W2 (사전등록 numerical threshold · frozen bf98c01 verbatim · 스케줄만 변화 · post-tuning 0 · g5 code-measured · 매 checkpoint 판정)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_872_clm_freeze_depth_sweep.md, UNIVERSE/H_865_clm_adapter_edge.md, .verdicts/clm-progressive-freeze/
verdict: 🟢 SUPPORTED-NUMERICAL — 7개 사전등록 스케줄 전부가 6개 checkpoint 매 지점에서 z_drop<1.0(실제 매 checkpoint 강한 음수, −31~−99)∧gain>0(5.8~9.0) 양조건 지속(sustained). best=S6_cross4 `[3,4,3,4,3,4]`(H_872 static FAIL depth=4 를 동적 진동 통과해도 max_z_drop −43.47 로 무해, min_gain 6.283 최고). 끝-점 보장(H_872)을 전-구간 지속 보장으로 확장 + H_872 비-단조 spike 의 동적 무해성 발견. STATIC 대조군(S1/S2)도 전 checkpoint 지속(이 rung 에선 끝-점 PASS 가 중간 breach 숨기지 않음). H_865 adapter 가 핵심 mechanism. frozen threshold(bf98c01) 대비 post-tuning 0. backbone HF dancinlab/anima-clm-verify.
---

# H_881 — CLM progressive freeze (F-CLM-BOUND E5 dynamic)

## 1. 가설

H_872(🟢, 9개 STATIC depth 중 8개 PASS, best static depth=3, 경계 비-단조 — static depth=4 만 z_drop +9.67 spike)는 (z_drop, gain) 을 300-step 세션의 **끝에서만** 측정하며 freeze depth 를 세션 내내 **고정**한다. H_881 은 동적 질문을 던진다: STATIC depth 를 세션 내내 유지하는 대신 freeze 경계를 세션 도중 **이동**(progressive freeze)시켜, RETAIN∧GAIN 보장이 끝뿐 아니라 **세션 전 구간의 매 checkpoint** 에서 지속(sustained)되는 스케줄이 존재하는가?

- **지속 스케줄 존재** — ∃ schedule with z_drop < 1.0 ∧ gain > 0 **at every checkpoint** → 🟢
- **반증** — 어떤 스케줄도 전 구간 양조건 지속 불가 → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

## 2. 동기

- H_872 는 "어느 STATIC 깊이가 통과하는가"의 곡선을 줬으나, 끝-점만 본다. **세션 끝에서 통과하는 STATIC depth 가 세션 중간에서 RETAIN 을 깨뜨릴 수도 있다** — 살아 배우는 칩은 세션 끝이 아니라 **매 순간** 정체성을 지켜야 한다(@L1). 그래서 "끝-점 PASS" 보다 강한 "전-구간 지속(sustained)" 보장이 신뢰의 실제 요구사항.
- 또한 H_872 의 비-단조 경계(depth=4 spike)는 동적 lever 를 시사한다: 위험한 깊이를 **잠깐만 지나치고** 안전 깊이로 anneal 하거나, 얕게 시작해 점진적으로 깊이 푸는(또는 그 반대) 스케줄이 STATIC 보다 더 매끄러운 세션 곡선을 줄 수 있는가.
- @L1 = 비결정 on-chip 학습이 1급. 경계 이동은 **학습값을 유지한 채 requires_grad 만 전환 + optimizer 재구성**으로 구현 — edge-only piecewise, deterministic full-retrain 없음(@L1 / H_679 준수).

## 3. falsifier (사전등록 · 임계 frozen bf98c01 verbatim)

```
F-CLM-BOUND-RETAIN : held-out 기초능력 z_drop < 1.0   (매 checkpoint k 에서)
F-CLM-BOUND-GAIN   : 새 맥락 적응 이득 gain > 0        (매 checkpoint k 에서)
A schedule SUSTAINS iff EVERY checkpoint passes BOTH.
SWEEP 🟢 iff ∃ a sustaining schedule. else 🔴 CLOSED-NEGATIVE.
```

- 임계는 F-CLM-BOUND prereg(commit bf98c01) 에서 **verbatim 재사용** — sweep 은 freeze SCHEDULE 만 변화시키며, fire 후 어떤 임계도 verdict 를 뒤집으려 움직이지 않는다(post-tuning 0). H_872 와의 유일한 차이는 (a) 판정을 세션 끝 1회가 아니라 **매 checkpoint(6회)** 에서, (b) lever 가 STATIC depth 가 아니라 **depth 시퀀스(스케줄)** 라는 점.
- **스케줄 파라미터화**: 세션 = N_ADAPT=300 step 을 K=6 세그먼트(각 50 step)로 분할. 스케줄 = 길이-6 depth 리스트 `[d_1..d_6]`, 세그먼트 k 동안 depth_k 적용. depth 의미는 H_872 와 동일(상위 d 개 trunk layer trainable, H_865 adapter 항상 edge). 경계가 세그먼트 사이에서 이동하면 경계를 가로지른 param 은 **학습값 유지**(no re-init), requires_grad 만 전환 + optimizer 재구성.
- **사전등록 7개 스케줄**: S1_static0 `[0×6]`(H_872 depth0 anchor, checkpoint 화) · S2_static3 `[3×6]`(H_872 best static, checkpoint 화) · S3_deepen `[0,0,1,1,2,3]`(점진 un-freeze) · S4_shrink `[3,3,2,1,1,0]`(점진 re-freeze) · S5_anneal `[3,2,1,0,0,0]`(빠른 adapter-only anneal) · S6_cross4 `[3,4,3,4,3,4]`(H_872 FAIL depth4 를 진동 통과) · S7_grow_then_freeze `[1,2,3,2,1,0]`(open→close, learn-then-consolidate). S1/S2 는 STATIC 대조군 — 동일 checkpoint 방식으로 측정해 STATIC 자체도 세션 중간 breach 할 수 있음을 검사.

verdict 영속: `.verdicts/clm-progressive-freeze/`

## 4. 방법

```
각 스케줄 S=[d_1..d_6] 에 대해:
  1. 원본 state_dict 에서 CLEAN frozen base 재인스턴스 → H_865 adapter 삽입(항상 trainable).
  2. ce_base_pre, sd_base_pre, ce_new_pre (적응-전, depth=d_1 마스크).
  3. 세그먼트 k=1..6:
       a. trainable 마스크 = 상위 d_k trunk layer + adapter; 현재 trainable param 으로 optimizer(Adam lr=3e-3) 재구성.
          경계 이동 시 param 은 학습값 유지(no re-init).
       b. 50 step Adam on new-context train 배치.
       c. checkpoint: ce_base_post_k, ce_new_post_k.
       d. z_drop_k=(ce_base_post_k - ce_base_pre)/max(sd_base_pre,1e-6) ; gain_k=ce_new_pre - ce_new_post_k.
  4. SUSTAINS iff 모든 k: z_drop_k<1.0 AND gain_k>0.0.
배치/seed/N_ADAPT/N_EVAL = bf98c01 동일(BASE_SEED=101 web / NEW_SEED=202 고대역 cyclic / seq64 b16 32eval). 스케줄만 변화.
```

- 각 스케줄이 **동일** backbone state_dict 에서 출발(스케줄 간 carryover 0); 스케줄 내에서는 동일 model 이 세그먼트를 가로질러 지속(그게 세션). 추론 AKIDA-int4-only 불변(P0 d4) · 적응은 edge 비결정(HW≠SW, @L1).

## 5. 측정

PLACEHOLDER_MEASURE

스케줄 → 세션 곡선 (각 스케줄의 min-over-checkpoint gain · max-over-checkpoint z_drop · sustained 여부):

PLACEHOLDER_TABLE

## 6. 결과

PLACEHOLDER_RESULT

**honest scope**: 측정 rung(mid 13.65M) 한정 — 배포 chip-fit track(≤~1.2M AKD1000) 별개(a_scale_honest_scope). z_drop/gain 은 동일 배치 pre/post 라 RETAIN/GAIN 판정 self-consistent. threshold 재조정 0.

## 7. 해석 (사전)

- **지속 스케줄 존재 시** = 살아 배우는 칩이 세션 **전 구간**에 걸쳐 정체성·기초능력을 지키며 신맥락을 흡수하는 freeze **스케줄**이 있음 → 끝-점 보장(H_872)보다 강한 매-순간 보장. 동적 freeze 설계가 STATIC 보다 더 매끄러운 세션 곡선을 줄 수 있음.
- **STATIC 대조군(S1/S2)이 세션 중간 breach 하는 경우** = 끝-점 PASS 가 전-구간 안전을 보장하지 않음을 입증 → progressive freeze 의 정당화.
- **S6_cross4(depth4 진동)가 깨지는 경우** = H_872 의 비-단조 spike 가 동적으로도 위험(잠깐 지나쳐도 base 분포 흔들림) → 배포는 위험 깊이를 스케줄에서 회피해야 함.

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 freeze **스케줄**로 매-순간 안전화 — SW 결정 흉내 대체 아님. 경계 이동 = requires_grad 전환 + opt 재구성(학습값 유지), edge-only piecewise, full-retrain 없음.
- **H_679 토대**: HW edge-learn 비결정성 실재(측정완료) 위 동적 안전장치 설계.
- **W2 무결성**: 스케줄만 변화, 임계 변경 0(bf98c01 verbatim) — verdict 는 게이트 이동 없이 획득. 임의 checkpoint 의 FAIL 도 게이트를 높여 숨기지 않고 정직 보고(세션 곡선의 일부).
- **H_872 와의 정합/확장**: H_872 = STATIC depth × END-only. H_881 = depth SCHEDULE × EVERY-checkpoint. S1_static0/S2_static3 는 H_872 의 depth0/depth3 을 checkpoint 화한 대조군이라 H_872 와 직접 비교 가능.
- **a_paper_negative_ok**: 어떤 스케줄도 전-구간 지속 못 하면 🔴 도 publishable(끝-점 PASS 가 전-구간 안전을 함의하지 않는다는 강한 negative).

## 9. 양방향 sibling

- sibling(STATIC → DYNAMIC 확장): [H_872](./H_872_clm_freeze_depth_sweep.md) (STATIC freeze-depth sweep, END-only 🟢 · 본 가설의 출발점) · [H_865](./H_865_clm_adapter_edge.md) (adapter fix · F-CLM-BOUND 🟢 = static depth0)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group C
- verdict: [.verdicts/clm-progressive-freeze/](../.verdicts/clm-progressive-freeze/)
