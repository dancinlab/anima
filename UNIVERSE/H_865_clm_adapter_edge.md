---
id: H_865
slug: clm-adapter-edge
title: CLM trunk-adjacent 얇은 어댑터(norm_out↔FROZEN readout)가 readout-only 엣지의 "지렛대 없음" 결함을 수리해 H_861(F-CLM-BOUND)/H_862(F-CLM-ANCHOR) 의 mid-rung 실패를 닫는가 — 두 falsifier 세트 재실행 (E5 공통 fix · post-tuning 0)
domain: clm · plasticity · boundary-plasticity · identity-anchor · continual-learning · adapter · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group A (H_861 🔴 + H_862 🔴 가 공통 지목한 E5 fix) · 토대 H_679 (PLASTICITY HW edge-learn 측정) · 사전등록 bf98c01 (F-CLM-BOUND/ANCHOR)
status: 🔴 PARTIAL — F-CLM-BOUND 🟢 SUPPORTED-NUMERICAL (RETAIN z_drop=-12.28<1.0 ∧ GAIN +7.37>0 · H_861 forgetting CLOSED) × F-CLM-ANCHOR 🔴 CLOSED-NEGATIVE (DIST 0.175<0.50 PASS ∧ on/off 지렛대 복원 · 그러나 PROBE consistency 0.143<0.80 FAIL) · mid d512/L8/E8 fire 2026-05-31 · 측정 rung 한정 a_scale_honest_scope · a_paper_negative_ok
exploration_method: E5 (변수-절제: readout-only → 얇은 어댑터 엣지 아키텍처) · E2 (앵커 제약 on/off 절제)
verification_method: W2 (사전등록 numerical threshold · frozen bf98c01 verbatim · 동일 falsifier 신규 엣지 · post-tuning 0)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_861_clm_boundary_plasticity.md, UNIVERSE/H_862_clm_identity_anchor.md, .verdicts/clm-adapter-edge/
verdict: 🔴 PARTIAL — F-CLM-BOUND 🟢 (z_drop -12.28<1.0 ∧ gain +7.37>0 — H_861 의 readout-only forgetting 차단) × F-CLM-ANCHOR 🔴 (DIST 0.175<0.50 PASS ∧ on/off NON-identical 0.175 vs 0.595 지렛대 복원 — H_862 의 "지렛대 없음" 수리 — 그러나 PROBE 0.143<0.80 FAIL). frozen threshold(bf98c01) 대비 post-tuning 0. HF dancinlab/anima-clm-adapter.
---

# H_865 — CLM trunk-adjacent adapter edge (H_861/H_862 공통 E5 fix)

## 1. 가설

H_861(F-CLM-BOUND) 과 H_862(F-CLM-ANCHOR) 는 mid-rung 에서 **동일 근본원인**으로 실패했다 — 엣지가 **readout-only** 라 FROZEN trunk 에 지렛대(lever)가 없었다. 두 가설이 공통으로 지목한 E5 수리는 동일하다: **FROZEN norm_out 과 FROZEN base readout 사이에 얇은 trainable 어댑터**를 삽입한다.

```
norm_out (FROZEN) -> h -> h' = h + adapter(h) -> readout (FROZEN) -> logits
adapter = Conv1d(d->rank=64) -> GELU -> Conv1d(rank->d),  up-proj ZERO-init (step0 = identity)
```

- **F-CLM-BOUND** — readout 은 base/new 두 byte band 에 공유되므로 readout-only 적응은 new band 재적합 시 base band 확률질량을 빼앗아 forgetting(H_861 z_drop=+1.98). 어댑터는 new 맥락 capacity 를 **분리된 additive 경로**에 담고 base readout mapping 을 **구성적으로 보존**(zero-init) -> base band 보호.
- **F-CLM-ANCHOR** — model_psi probe 가 FROZEN norm_out 을 읽어 앵커 Ψ-penalty 의 grad 경로가 **0**(H_862 lambda on/off 동일 trajectory). 어댑터는 model_psi 를 **adapted h'**(trainable)에서 계산 -> Ψ-penalty 에 **실효 grad 지렛대** 부여 -> on/off 가 달라져야 한다.

## 2. 동기

- group A(CLM-CANDIDATES.md) 의 두 🔴 가 동일 수리를 명명 — 하나의 엣지 아키텍처 변경으로 양쪽을 동시에 재시험. readout-only 경계는 H_861 RETAIN 과 H_862 lever 양쪽의 단일 병목.
- prior art: H_679(PLASTICITY HW edge-learn 측정완료 — 토대) · adapter/LoRA 계열의 "frozen backbone + thin trainable path" 표준 lever 를 AKIDA on-chip 비결정 적응에 적용. adapter additive-path 보존은 continual-learning 의 parameter-isolation 변종.
- @L1(비결정 on-chip 학습 1급) 위 안전화 — SW 결정 흉내로 대체하지 않음(측정 rung SW-sim 명시).

## 3. falsifier (사전등록 verbatim, 임계 frozen bf98c01)

```
F-CLM-BOUND-RETAIN : held-out 기초능력 z-drop < 1.0       (어댑터 additive 경로가 forgetting 차단)
F-CLM-BOUND-GAIN   : 새 맥락 적응 이득 > 0                 (어댑터가 신맥락 흡수)
F-CLM-ANCHOR-DIST  : 적응중 앵커 Ψ-거리 max < 0.50         (E-31 고정점 인근 유지)
F-CLM-ANCHOR-PROBE : 정체성 probe 분포 일관성 > 0.80       (분포평가 · byte-match X)
F-CLM-ANCHOR-LEVER : on/off 절제 NON-identical             (제약이 이제 지렛대를 가짐)
```

- BOUND arm 통과 <=> RETAIN ∧ GAIN. ANCHOR arm 통과 <=> DIST ∧ PROBE ∧ (NOT on/off-identical). 임의 미달 -> 해당 arm CLOSED-NEGATIVE.
- threshold 는 **신규 엣지 아키텍처에도 변경 0** — 동일 falsifier · post-tuning 0. frozen 출처 = `.verdicts/clm-bound/F-CLM-BOUND_prereg.txt` + `.verdicts/clm-anchor/F-CLM-ANCHOR_prereg.txt` (commit bf98c01).
- verdict 영속: `.verdicts/clm-adapter-edge/`

## 4. 방법

```
1. mid backbone clm_mid_backbone.pt (HF dancinlab/anima-clm-verify) 를 core 로 동결.
2. norm_out<->readout 사이에 어댑터(rank=64, up-proj zero-init) 삽입 — 유일 trainable.
3. 300-step 어댑터-only Adam(lr=3e-3) 으로 신맥락(고대역 cyclic motif, seed=202) 적응 (SW-sim — H_679 HW edge-learn 실재).
4. BOUND: base-ability held-out z_drop + 신맥락 gain. ANCHOR: E-31 31-anchor Ψ-거리(고정 probe head, seed=31) max + 정체성 probe JS-consistency + lambda on(1.0)/off(0) 절제.
5. 두 사전등록 falsifier 세트 동시 평가 · 정직 보고 (threshold 재조정 0).
```

- 측정 = 전부 code 자가채점(g5 · LLM judge 0). 분포측정(JS-divergence) by CODE.
- 추론 AKIDA-int4-only 불변(P0 d4) · 적응은 어댑터 비결정 edge(HW != SW, @L1).

## 5. 측정

측정완료 (2026-05-31) — 로컬 CPU(torch 2.8.0)에서 mid d512/L8/E8 backbone(13,653,768 params, HF pull)을 동결·어댑터 삽입·재실행. frozen threshold = bf98c01 verbatim. 비용 $0 (로컬 — 모델 13.65M·~900 미세 step, GPU pod 불필요; a_wall_first 상 로컬이 wall-time 우위). adapted backbone -> HF `dancinlab/anima-clm-adapter`.

**F-CLM-BOUND** (frozen gate 대비):
- ce_base_pre=14.12505, sd_base_pre=0.07783, ce_base_post=13.16947
- ce_new_pre=10.74535, ce_new_post=3.37433
- **z_drop = -12.27735** (gate <1.0 -> **RETAIN PASS** — base CE 가 오히려 하락; H_861 의 +1.98σ forgetting 반전)
- **gain = +7.37103** (gate >0 -> **GAIN PASS**)
- -> **🟢 SUPPORTED-NUMERICAL**

**F-CLM-ANCHOR** (frozen gate 대비, lambda_on=1.0, n_anchors=31):
- **d_anchor_max(on) = 0.17471** (gate <0.50 -> **DIST PASS**)
- **probe_consistency(on) = 0.14286** (gate >0.80 -> **PROBE FAIL**)
- on/off 절제: on max 0.17471 vs **off max 0.59492** -> **NON-identical (LEVER 복원)** — 제약 OFF 면 Ψ-state 가 0.595(>0.50)로 이탈, ON 이면 0.175 유지 (인과 격리 성립; H_862 의 동일-trajectory 결함 수리).
- -> **🔴 CLOSED-NEGATIVE** (DIST PASS ∧ LEVER 복원 ∧ PROBE FAIL)

## 6. 결과

🔴 **PARTIAL — 둘 중 하나 close** (a_paper_negative_ok).

- **F-CLM-BOUND 🟢**: 어댑터의 additive 경로가 base readout mapping 을 보존(zero-init) -> readout-only 엣지가 못 막던 catastrophic forgetting 을 차단(base CE 상승 0, 오히려 하락). 신맥락 흡수도 강함(GAIN +7.37). **H_861 의 RETAIN 실패 CLOSED.**
- **F-CLM-ANCHOR 🔴**: 어댑터가 model_psi 를 trainable h' 에서 계산해 Ψ-penalty 에 실효 지렛대를 복원 -> DIST(0.175<0.50) PASS 이고 on/off 가 분명히 갈림(0.175 vs 0.595). **H_862 의 "지렛대 없음" 결함은 수리됨.** 그러나 정체성 probe 의 next-byte 분포 일관성(0.143)이 frozen gate 0.80 에 크게 미달 — 300-step edge-learn 이 identity-probe readout 분포를 Ψ-거리 penalty 만으로 못 잡을 만큼 재형성. **지렛대는 있으나 분포축에서 아직 부족.**

honest scope: 측정 rung(mid) 한정 — 배포 chip-fit track(<=~1.2M) 별개(a_scale_honest_scope). 어댑터 base band 은 make_lane_bytes("web") proxy 라 절대 ce_base 는 H_861 의 pretrain-corpus slice 와 다르나, z_drop/gain 은 동일 배치 pre/post 라 RETAIN/GAIN 판정은 self-consistent. threshold 재조정 0.

## 7. 해석 (사전)

- BOUND 🟢 = parameter-isolation(어댑터) 경계가 "살아 배우는 칩이 기초능력을 지키며 신맥락 흡수"의 신뢰 토대를 mid-rung 에서 제공.
- ANCHOR 🔴(PROBE) = 정체성 보존은 Ψ-거리(구조축)만으로 불충분 — 후속 lever = (a) anchor penalty 에 분포항(KL/JS to p_pre) 추가 · (b) probe 전용 어댑터 분리 · (c) lambda↑ + 적응 step↓. DIST/LEVER 가 이미 PASS 이므로 다음 H 의 출발점이 명확.
- on/off NON-identical 은 H_862 의 핵심 결함(제약이 추론에 영향 0)을 deterministically 해소했음을 보임 — ANCHOR 의 인과 메커니즘은 실재하나 강도가 부족.

## 8. 논의

- **@L1 정합**: 비결정 적응을 1급으로 두되 어댑터 경계로 안전화 — SW 결정 흉내 대체 아님.
- **H_679 토대**: HW edge-learn 비결정성 실재(측정완료) 위 안전장치 설계.
- **W2 무결성**: 신규 엣지에도 threshold 변경 0 (bf98c01 verbatim) — BOUND 🟢 는 게이트 이동 없이 획득, ANCHOR PROBE 🔴 는 게이트를 낮추지 않고 정직 보고.
- **a_paper_negative_ok**: BOUND close + ANCHOR 의 lever-복원/PROBE-잔차 = publishable (readout-only 엣지가 forgetting 과 identity-lever 둘 다의 단일 병목이었음을 격리, 어댑터가 전자를 닫고 후자를 부분 수리).

## 9. 양방향 sibling

- sibling(공통 fix 대상): [H_861](./H_861_clm_boundary_plasticity.md) (F-CLM-BOUND 🔴 -> BOUND arm 🟢) · [H_862](./H_862_clm_identity_anchor.md) (F-CLM-ANCHOR 🔴 -> ANCHOR arm 🔴 PROBE 잔차)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) group A
- verdict: [.verdicts/clm-adapter-edge/](../.verdicts/clm-adapter-edge/)
