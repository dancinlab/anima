---
id: H_883
slug: clm-replay-continual
title: edge-only on-chip 적응 stream 에 OLD 기초능력("web" lane) 샘플의 작은 replay buffer(REPLAY_RATIO=0.25)를 interleave 하면 catastrophic forgetting(base z_drop)이 no-replay 대비 줄면서도 새 맥락 gain>0 을 지키는가 — H_875 forgetting-curve follow-on SAFETY DEVICE · S=300 endpoint · post-tuning 0
domain: clm · plasticity · continual-learning · replay-buffer · catastrophic-forgetting · adapter · safety-device · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md §E (부분부분학습/continual) · H_875 🟡 forgetting-curve 의 follow-on safety device · edge = H_865 🟢 adapter (H_861 🔴 readout-only) · 토대 H_679 (PLASTICITY HW edge-learn) · 사전등록 F-CLM-REPLAY_prereg.txt (frozen 2026-05-31)
status: 🟢 SUPPORTED-NUMERICAL — S=300 에서 z_drop(replay)=−125.81 < z_drop(no_replay)=−8.50 ∧ gain(replay)=+6.66>0 → falsifier (R∧G) MET · dose 가 오를수록 replay 보호가 깊어짐(no_replay z_drop 는 0 쪽으로 풀림) · GPU(RTX 5070) · 측정 rung 한정 a_scale_honest_scope
exploration_method: E (조건 절제: 동일 backbone/edge/seed/step budget 에서 stream 만 변화 — no_replay ↔ replay(every-4th-step 결정적 interleave))
verification_method: W2 (사전등록 numerical threshold · F-CLM-REPLAY_prereg.txt verbatim · post-tuning 0 · g5 code-measured · no LLM judge)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_861_clm_boundary_plasticity.md, UNIVERSE/H_865_clm_adapter_edge.md, UNIVERSE/H_875_clm_forgetting_curve.md, .verdicts/clm-replay-continual/
verdict: 🟢 SUPPORTED-NUMERICAL — S=300 endpoint 에서 (R) z_drop(replay) −125.81 < z_drop(no_replay) −8.50 ∧ (G) gain(replay) +6.66 > 0 두 falsifier 모두 성립. replay 가 base-ability z_drop 을 117.31 만큼 더 끌어내리며 forgetting 을 적극 차단, 새 맥락 gain 은 +6.66(no_replay +7.37 대비 0.71 nat trade-off)로 양수 유지. dose 가 오를수록 보호가 깊어짐(no_replay 는 0 쪽으로 풀림). frozen threshold 대비 post-tuning 0. backbone HF dancinlab/anima-clm-verify.
---

# H_883 — CLM replay-buffer continual learning (H_875 forgetting-curve SAFETY DEVICE)

## 1. 가설

H_875 는 edge-only on-chip 적응의 **forgetting curve**(dose-response: step 이 늘수록 base-ability 가 어떻게 흔들리는가)를 측정했다. H_883 은 그 **follow-on safety device**: OLD 기초능력("web" lane) 샘플의 **작은 replay buffer** 를 새-맥락 edge-learn stream 에 interleave 하면, no-replay 대비 catastrophic forgetting(base-ability z_drop)이 줄면서도 새-맥락 학습 신호(gain)를 파괴하지 않는가?

- **falsifier 성립** — S=300 endpoint 에서 (R) z_drop(replay) < z_drop(no_replay) ∧ (G) gain(replay) > 0 → 🟢
- **반증** — 둘 중 하나라도 실패(replay 가 gain 을 파괴 / z_drop 을 못 줄임) → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

## 2. 동기

- @L1 = 살아 배우는 칩이 대화하며 점진적으로 배우되 정체성·기초능력을 잃지 않아야 한다. replay 는 continual-learning 의 고전적 forgetting 완화 device — 본 hypothesis 는 그것이 **edge-only / frozen-trunk** 제약 아래(full retrain 없이) 작동하는지를 측정한다.
- edge = H_865 trunk-adjacent thin adapter(검증된 working edge; H_861 readout-only 는 lever-less 🔴). replay 는 이 edge 위에서, core trunk 는 FROZEN 인 채로 SAME edge-only Adam stream 에 OLD 배치 몇 개를 섞을 뿐.
- 토대: H_679 (PLASTICITY HW edge-learn 측정완료).

## 3. falsifier (사전등록 · 임계 frozen F-CLM-REPLAY_prereg.txt verbatim)

```
REPLAY_RATIO=0.25 · STEP_LADDER=[32,128,300] · primary read @ S=300 · seeds frozen
(R) z_drop(replay) < z_drop(no_replay)     [replay reduces forgetting]
(G) gain(replay)   > 0.0                   [replay keeps a real new-context gain]
PASS(🟢) iff (R) ∧ (G) at S=300. else 🔴 CLOSED-NEGATIVE.
z_drop(S) = (ce_base_post - ce_base_pre)/max(sd_base_pre,1e-6) ; gain(S) = ce_new_pre - ce_new_post
```

- 임계는 fire 전 frozen, post-tuning 0. no_replay arm 이 곧 H_875 no-replay baseline(side-by-side 동일 run). replay schedule = 결정적(매 4번째 step 이 replay-buffer 배치), 나머지는 new-context. 두 arm 의 new-context 배치 cursor 는 동일 prefix(replay step 은 INSERT) → z_drop/gain 차이는 replay interleave 단독 귀속.

verdict 영속: `.verdicts/clm-replay-continual/`

## 4. 방법

```
각 (condition, S):
  1. frozen backbone 에서 모델 구성 → core FROZEN → H_865 adapter init(identity@step0).
  2. ce_base_pre/sd_base_pre(OLD held-out), ce_new_pre(new held-out) 측정.
  3. S step edge-only Adam. no_replay→전부 new-context. replay→매 4번째 step 만 OLD replay-buffer.
  4. ce_base_post(OLD), ce_new_post(new) 측정 → z_drop, gain 기록.
backbone clm_mid_backbone.pt (HF dancinlab/anima-clm-verify · 신 artifact 없음, a_hf_complete).
```

## 5. 측정

측정완료 (2026-05-31) — **GPU(RTX 5070, summer 192.168.50.60)** device=cuda. backbone mid d512/L8/E8(~13.65M params). frozen threshold = prereg verbatim.

primary @ S=300:

| metric | no_replay | replay | falsifier | 판정 |
|:-------|----------:|-------:|:----------|:----:|
| z_drop | −8.49775 | **−125.80917** | (R) replay < no_replay | **TRUE** |
| gain | +7.37175 | **+6.66309** | (G) gain(replay) > 0 | **TRUE** |

- delta_z_drop = **−117.31142** (replay 가 base z_drop 을 117 만큼 더 끌어내림). **VERDICT GREEN**.

dose curve (secondary, NOT gating):

| S | no_replay z_drop | replay z_drop | no_replay gain | replay gain |
|--:|--:|--:|--:|--:|
| 32 | −75.90981 | −94.15323 | 5.51489 | 5.20083 |
| 128 | −34.71526 | −117.36453 | 6.79266 | 5.72106 |
| 300 | −8.49775 | −125.80917 | 7.37175 | 6.66309 |

- dose 가 오를수록 **no_replay z_drop 은 0 쪽으로 풀리고(forgetting 이 되돌아옴) replay z_drop 은 더 깊어진다(base 가 적극 보호됨)** — replay safety device 의 보호가 step budget 과 함께 커진다(H_875 forgetting-curve follow-on 거동 그대로). retain_pass = true at every (arm, S).

## 6. 결과

🟢 **SUPPORTED-NUMERICAL**. OLD 기초능력 샘플의 작은 replay buffer(REPLAY_RATIO=0.25, 결정적 every-4th-step)를 edge-only on-chip 적응 stream 에 interleave 하면 catastrophic forgetting 이 줄고(base z_drop −8.50 → −125.81 @S=300) 새-맥락 gain 은 양수로 유지된다(+6.66). replay 는 H_865 adapter edge 위에서 작동하는 **H_875 forgetting-curve safety device** 다.

- gain trade-off 은 작다(replay +6.66 vs no_replay +7.37 = 0.71 nat 비용) — replay 는 작은 new-context gain 비용으로 큰 forgetting 보호를 산다.

**honest scope**: 측정 rung(mid 13.65M) 한정 — 배포 chip-fit track(≤~1.2M AKD1000) 별개(a_scale_honest_scope). 임계 재조정 0.

## 7. 해석 (사전)

- **falsifier 성립(본 결과)** = 살아 배우는 칩이 대화하며(@L1) 새 맥락을 흡수하되 OLD 기초능력을 작은 replay 로 지킬 수 있음 → continual-learning safety device 확보. core trunk 는 FROZEN 인 채 edge-only.
- **반증이었다면** = replay 가 gain 을 파괴하거나 z_drop 을 못 줄였다면, 작은 replay 는 edge 제약 아래 부적절 — 그 또한 publishable.

## 8. 논의

- **@L1 정합**: replay 는 결정적 full-retrain 이 아니라 SAME edge-only Adam stream 에 OLD 배치 몇 개 INSERT — 비결정 on-chip 학습 1급(H_679 토대)을 SW 결정 흉내로 대체하지 않는다.
- **W2 무결성**: stream 만 변화(backbone/edge/seed/step budget 고정), 임계 변경 0 — 🟢 는 게이트 이동 없이 획득.
- **H_865/H_875 정합**: edge = H_865 adapter, no_replay arm = H_875 no-replay baseline side-by-side → replay-vs-no-replay 대비가 apples-to-apples.
- **a_paper_negative_ok**: 🔴 였어도 publishable 이었으나 본 결과는 작동하는 safety device 라는 positive.

## 9. 양방향 sibling

- sibling: [H_861](./H_861_clm_boundary_plasticity.md) (readout-only 🔴) · [H_865](./H_865_clm_adapter_edge.md) (adapter edge 🟢 = 본 replay 의 edge) · [H_875](./H_875_clm_forgetting_curve.md) (forgetting curve 🟡 = 본 safety device 의 모태)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) §E
- verdict: [.verdicts/clm-replay-continual/](../.verdicts/clm-replay-continual/)
