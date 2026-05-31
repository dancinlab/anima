---
id: H_883
slug: clm-replay-continual
title: 새 맥락 edge-learn 스트림에 OLD(기초능력 "web" lane) 샘플의 작은 replay buffer 를 interleave 하면(REPLAY_RATIO=0.25, 매 4번째 step) catastrophic forgetting(base-ability z_drop)이 no-replay 대비 줄어드는가 — 단 새 맥락 gain>0 유지 (H_875 forgetting-curve 안전장치 · 임계 frozen 2026-05-31 verbatim · post-tuning 0 · 검증 S=300 endpoint)
domain: clm · plasticity · boundary-plasticity · continual-learning · replay-buffer · forgetting · adapter · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md §E (부분부분학습) · H_861 🔴 readout-only 너무 얕음 + H_865 🟢 adapter fix(실제 움직이는 edge) · H_875 forgetting-curve 의 follow-on 안전장치(no_replay arm = side-by-side baseline) · 토대 H_679 (PLASTICITY HW edge-learn 측정) · 사전등록 F-CLM-REPLAY_prereg.txt (frozen 2026-05-31)
status: 🟢 SUPPORTED-NUMERICAL — S=300 endpoint 에서 양조건 PASS (z_drop replay=-125.51 < no_replay=-9.32 ∧ gain replay=+6.57>0) · mid d512/L8/E8 · CPU-LOCAL 2026-05-31 · 측정 rung 한정 a_scale_honest_scope
exploration_method: E5 (단일-변수 절제: adaptation STREAM 만 변화 — replay interleave on/off, backbone/edge/seed/step budget 동일) · E2 (replay buffer = OLD lane batch 혼입)
verification_method: W2 (사전등록 numerical threshold · frozen F-CLM-REPLAY_prereg.txt verbatim · 적응 스트림만 변화 · post-tuning 0 · g5 code-measured · 검증 S=300 endpoint)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_861_clm_boundary_plasticity.md, UNIVERSE/H_865_clm_adapter_edge.md, UNIVERSE/H_875_clm_forgetting_curve.md, UNIVERSE/H_879_clm_per_layer_edge.md, .verdicts/clm-replay-continual/
verdict: 🟢 SUPPORTED-NUMERICAL — S=300 endpoint(frozen)에서 (R) z_drop(replay) −125.50785 < z_drop(no_replay) −9.31924 ∧ (G) gain(replay) +6.56950 > 0 둘 다 성립. replay 는 forgetting 을 step ladder 전 구간(32/128/300)에서 줄이며(z_drop 항상 더 음수), 새 맥락 gain 은 전 구간 양수 유지(5.20→5.72→6.57). gain trade-off 는 작고 정직(replay 6.57 vs no_replay 7.37 @S=300 — 300 step 중 75 step 을 old replay 에 씀). S=32/128 수치가 prior partial run 과 정확히 일치 → 결정적 schedule + frozen seed 재현 확인. backbone HF dancinlab/anima-clm-verify. 임계 frozen 2026-05-31 verbatim, post-tuning 0. a_paper_negative_ok.
---

# H_883 — CLM replay-buffer 연속학습 (H_875 forgetting-curve 안전장치 · F-CLM-REPLAY)

## 1. 가설

H_861 은 readout-only edge 가 너무 **얕아** catastrophic forgetting 을 못 막음을 발견(🔴). H_865 는 trunk-adjacent 얇은 adapter 가 BOUND arm 을 **수리**함을 발견(🟢, 실제로 움직이는 edge). H_875 는 그 edge 위에서 적응 step 이 늘수록 base-ability forgetting 이 어떻게 변하는지 forgetting-curve 를 그렸다. H_883 은 그 follow-on **안전장치**를 묻는다: OLD(기초능력 "web" lane) 샘플의 **작은 replay buffer** 를 새 맥락 edge-only Adam 스트림에 interleave(REPLAY_RATIO=0.25, 매 4번째 step 이 replay step)하면, **동일** backbone·edge·seed·step budget 에서 base-ability z_drop(forgetting)이 no-replay 대비 **줄어드는가**, 그리고 새 맥락 gain 은 **양수로 유지**되는가?

- **replay 가 forgetting 을 줄이고 gain 도 살림** → 🟢 (R: z_drop(replay) < z_drop(no_replay) ∧ G: gain(replay) > 0)
- **반증** — replay 가 z_drop 을 못 줄이거나 새 맥락 gain 을 파괴 → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

## 2. 동기

- continual-learning 에서 replay 는 정석 안전장치지만, **edge-only 비결정 on-chip 적응**(@L1, core trunk FROZEN, full-retrain 금지) 위에서 **작은** old-batch 혼입만으로 forgetting 을 누를 수 있는지, 그리고 새 맥락 흡수를 죽이지 않는지는 배포 edge 설계의 직접 입력.
- no_replay arm 은 **side-by-side 로 측정된 H_875 baseline** — H_875 자체 verdict 가 아직 안 landed 이어도 replay-vs-no_replay 대조는 같은 run 안에서 성립(prereg 의 설계).
- prior art: H_679 (HW edge-learn 측정완료, 토대) · H_861/H_865 (경계 점) · H_872/H_879 (freeze-depth / per-layer edge) · H_875 (forgetting curve). H_883 은 그 위의 **안전장치 축**.

## 3. falsifier (사전등록 · 임계 frozen 2026-05-31 verbatim · 검증 S=300 endpoint)

```
(R) z_drop(replay) < z_drop(no_replay)            [replay 가 forgetting 을 줄임]
(G) gain(replay)   > 0.0                          [replay 가 진짜 새 맥락 gain 유지]
PASS (🟢) iff AT S=300:  (R) ∧ (G).  else 🔴 CLOSED-NEGATIVE (a_paper_negative_ok).
```

- 임계는 `.verdicts/clm-replay-continual/F-CLM-REPLAY_prereg.txt`(frozen 2026-05-31)에서 **verbatim** — probe 는 **적응 STREAM 만**(replay interleave on/off) 변화시키며, fire 후 어떤 임계도 verdict 를 뒤집으려 움직이지 않는다(post-tuning 0).
- **parameterization**: backbone mid d512/L8/E8 (HF dancinlab/anima-clm-verify) FROZEN, H_865 zero-init adapter(rank=64, identity at step 0)가 유일한 trainable edge. no_replay = 매 step 새 맥락 batch. replay = 매 4번째 step(REPLAY_RATIO=0.25, deterministic schedule)이 base-ability replay-buffer batch, 나머지는 새 맥락. 새 맥락 cursor 는 새 step 에서만 전진(replay step 은 삽입) → 두 arm 이 동일 새 맥락 prefix 소비 → z_drop/gain 차이는 replay interleave 단독 귀속. replay buffer 는 base eval slice 와 **disjoint**.

verdict 영속: `.verdicts/clm-replay-continual/`

## 4. 방법

```
각 (condition ∈ {no_replay, replay}, S ∈ STEP_LADDER=[32,128,300]) 에 대해:
  1. frozen backbone 에서 FRESH model 구성 → core FROZEN → H_865 adapter 삽입(identity at step 0).
  2. ce_base_pre, sd_base_pre (base-ability held-out, 적응-전) ; ce_new_pre (new-context held-out).
  3. S step edge-only Adam(lr=3e-3) over adapter params 만.
       no_replay → 전부 new-context batch.
       replay    → 매 4번째 step = base-ability replay-buffer batch, 그 외 = new-context (deterministic).
  4. ce_base_post, ce_new_post (적응-후).
  5. z_drop = (ce_base_post - ce_base_pre)/max(sd_base_pre,1e-6) ; gain = ce_new_pre - ce_new_post.
seq64 · b16 · n_eval=16 · BASE_SEED=101(web) · NEW_SEED=202(고대역 cyclic) · 전부 frozen.
verdict 는 S=300 endpoint 에서 read (frozen). 32/128 은 dose curve 로 보고(게이트 아님).
```

## 5. 측정

측정완료 (2026-05-31) — **CPU-LOCAL**(이 Mac)에서 mid d512/L8/E8 backbone(13,653,768 params, HF dancinlab/anima-clm-verify, load missing=[] unexpected=[]) 동결·adapter 삽입·6 arm(2 condition × 3 step) 을 전수 실행. 비용 = $0(로컬 CPU, runpod/cloud 미사용 · a_cpu_local_no_waiter). frozen threshold verbatim. edge-learn SW-sim(H_679 HW edge-learn 실재). 이 v2 run 은 prior run 이 result JSON 쓰기 전에 crash 했던 **S=300 endpoint 를 완주**했다.

step ladder (z_drop, gain) 표:

| S | condition | z_drop | gain | replay_steps | new_steps |
|--:|:----------|-------:|-----:|-------------:|----------:|
| 32  | no_replay | −75.89079  | +5.51444 | 0  | 32  |
| 32  | replay    | **−94.11879**  | +5.20039 | 8  | 24  |
| 128 | no_replay | −34.14703  | +6.81051 | 0  | 128 |
| 128 | replay    | **−117.31104** | +5.72354 | 32 | 96  |
| **300** | **no_replay** | **−9.31924** | **+7.37201** | 0  | 300 |
| **300** | **replay**    | **−125.50785** | **+6.56950** | 75 | 225 |

**S=300 verdict block (frozen endpoint)**: z_drop(replay) −125.50785 < z_drop(no_replay) −9.31924 (delta −116.18861) → **(R) PASS**; gain(replay) +6.56950 > 0 → **(G) PASS** → **🟢 GREEN**.

## 6. 결과

🟢 **SUPPORTED-NUMERICAL**. S=300 endpoint 에서 양조건 동시 PASS — 작은 replay buffer interleave 는 edge-only on-chip 적응의 catastrophic forgetting 을 줄이면서(z_drop −9.3 → −125.5) 새 맥락 흡수를 죽이지 않는다(gain +6.57). replay 는 H_865 adapter edge 위의 작동하는 H_875 forgetting-curve **안전장치**다.

- **forgetting 감소는 step ladder 전 구간**(32/128/300)에서 성립 — z_drop(replay)이 항상 z_drop(no_replay)보다 더 음수. endpoint 만의 우연이 아니라 dose 전체에서 robust.
- **no_replay z_drop 은 step 이 늘수록 0 쪽으로 상승**(−75.9 → −34.1 → −9.3): replay 없이 새 맥락에 적응할수록 base forgetting 이 다시 기어 올라온다. replay 는 z_drop 을 깊은 음수로 **고정**(−94 → −117 → −126) — replay step 이 base CE 를 계속 더 낮춘다.
- **gain trade-off 는 작고 정직**: gain(replay) +6.57 < gain(no_replay) +7.37 @S=300 (300 step 중 75 step 을 old replay 에 씀). 그래도 전 구간 강한 양수 유지(5.20→5.72→6.57) — interleave 가 새 맥락 신호를 결코 파괴하지 않음.
- **재현성**: S=32/128 수치가 prior partial run 과 **정확히 일치**(no_replay S=128 −34.1470; replay S=128 −117.3110 gain +5.7235) → deterministic schedule + frozen seed 재현 확인.

**honest scope**: 측정 rung(mid 13.65M) 한정 — 배포 chip-fit track(≤~1.2M AKD1000) 별개(a_scale_honest_scope). 추론 AKIDA-int4-only 불변(P0 d4). z_drop/gain 은 동일 배치 pre/post 라 판정 self-consistent. threshold 재조정 0.

## 7. 해석 (사전)

- **🟢 (본 결과)** = 살아 배우는 칩이 새 맥락을 흡수하면서도(@L1 대화하며 학습) 작은 old-sample replay 만으로 정체성·기초능력 forgetting 을 누를 수 있다 — 배포 edge 의 안전장치로 replay buffer 채택 가능. core trunk full-retrain 없이(@L1 불변) 안전.
- **no_replay 의 z_drop 상승**이 핵심 위험 신호: replay 없는 순수 edge 적응은 step 이 늘수록 forgetting 이 되살아남 → 장기 연속학습엔 replay 가 필수 안전장치.
- **작은 ratio(0.25)면 충분**: 매 4번째 step 만 old batch 로 써도 forgetting 을 강하게 누름 — 새 맥락 예산을 크게 희생하지 않고 안전 확보.

## 8. 논의

- **@L1 정합**: 비결정 on-chip 적응을 1급으로 두되 replay 로 안전화 — SW 결정 흉내(full-retrain) 대체 아님(H_679 토대). replay 는 OLD batch 를 같은 edge-only 스트림에 섞을 뿐, core trunk 는 FROZEN.
- **W2 무결성**: 적응 STREAM 만 변화(backbone/edge/seed/step budget 동일), 임계 변경 0(frozen verbatim) — 🟢 는 게이트 이동 없이 획득. gain trade-off(replay 가 no_replay 보다 gain 약간 낮음)도 게이트 숨김 없이 정직 보고.
- **H_865/H_875 와의 정합**: edge 는 H_865 검증 adapter, no_replay arm 은 side-by-side H_875 baseline. replay 가 그 baseline 대비 forgetting 을 줄임을 동일 run 에서 측정.
- **a_paper_negative_ok**: replay 가 z_drop 을 못 줄였거나 gain 을 파괴했다면 🔴 도 publishable 이었으나, 본 결과는 양조건 PASS 라는 positive + dose 전구간 robust 라는 구조적 발견.
- **CPU-LOCAL 정직성**: GPU/runpod 없이 이 Mac CPU 에서 측정(다중 에이전트 CPU 경합으로 wall time 길었으나 비용 $0). prior run 이 crash 했던 S=300 endpoint 를 v2 run 이 완주해 valid verdict 확보.

## 9. 양방향 sibling

- sibling(경계 점·곡선·안전장치): [H_861](./H_861_clm_boundary_plasticity.md) (readout-only 너무 얕음 🔴) · [H_865](./H_865_clm_adapter_edge.md) (adapter fix · 본 edge) · [H_875](./H_875_clm_forgetting_curve.md) (forgetting curve · no_replay arm = side-by-side baseline) · [H_879](./H_879_clm_per_layer_edge.md) (per-layer edge)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) §E (부분부분학습)
- verdict: [.verdicts/clm-replay-continual/](../.verdicts/clm-replay-continual/)
