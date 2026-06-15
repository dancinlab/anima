---
id: H_869
slug: clm-dispatch-kl-distill
title: router 의 batch-평균 dispatch 분포를 UNIFORM 으로 distill 하는 dispatch-KL 항(@L3 4번째 routing-escape lever A)이 작은-스케일 z-collapse 없이 routing diversity(dispatch entropy ↑ ∧ routing-z ↑)를 올리는가 — MID rung d512/L8/E8 고정·lever 절제·post-tuning 0
domain: clm · routing · moe · dispatch · routing-escape · lever-A · kl-distill · q-trust · falsifier
source: UNIVERSE/CLM-CANDIDATES.md @L3 routing-escape lever A · H_871 🟢 routing-z scale-ladder (small→mid 평탄 +0.02, E=8 고정 → depth 는 z 를 못 움직임) 의 잔여 lever · 토대 H_679 (PLASTICITY HW edge-learn) · 사전등록 F-CLM-DISPATCH-KL_prereg.txt (frozen 2026-05-31)
status: 🔴 CLOSED-NEGATIVE — dispatch-KL distill 은 MID rung 에서 INERT (baseline dispatch 가 이미 uniform 천장 H(f)=2.0789/max 2.0794 nats) · ENTROPY +0.0001≪0.10 FAIL ∧ routing-z −0.1065 FAIL (CE budget 만 PASS) · GPU(RTX 5070) torch 2.11.0+cu130 · 측정 rung 한정 a_scale_honest_scope
exploration_method: E (lever 절제: 동일 budget/seed/rung 에서 KL_COEF 0↔0.10 단일 변수만 변화)
verification_method: W2 (사전등록 numerical threshold · F-CLM-DISPATCH-KL_prereg.txt verbatim · post-tuning 0 · g5 code-measured · no LLM judge)
raw_rank: 9
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: UNIVERSE/H_871_clm_routing_z_scale.md, .verdicts/clm-dispatch-kl-distill/
verdict: 🔴 CLOSED-NEGATIVE (a_paper_negative_ok) — 3 게이트 중 ENTROPY·Z FAIL, BUDGET 만 PASS. KL 분 dispatch-entropy +0.0001(게이트 ≥+0.10), routing-z −0.1065(게이트 ≥+0.20), held-out CE +0.0026(예산 ≤+0.10). dispatch-KL distill 은 이 rung 에서 INERT — baseline dispatch 가 이미 uniform 천장(8/8 distinct, H(f) 2.0789 of max 2.0794)이라 balanced-target KL 이 보탤 여유가 없다. @L3 4번째 routing-escape lever 로서 dispatch-KL 을 OUT 으로 판정. backbone HF dancinlab/anima-clm-verify.
---

# H_869 — CLM dispatch-KL distill routing (@L3 routing-escape lever A · F-CLM-DISPATCH-KL)

## 1. 가설

@L3 routing-escape 로드맵은 router 가 소수 expert 로 collapse 하지 않고 다양하게 dispatch 하도록 만드는 lever 들을 찾는다. **lever A = dispatch-KL distill**: loss 에 KL 항을 추가해 router 의 batch-평균 per-token dispatch 분포 `f` 를 UNIFORM(1/E)으로 끌어당긴다. 주장: routing diversity 가 오른다(dispatch entropy ↑ **그리고** routing-z ↑) — 작은-스케일에서 보이던 z-collapse / quality wreck 없이, held-out CE 가 frozen budget 안에 머문 채로.

- **lever-A SUPPORTED** — ENTROPY ∧ Z ∧ BUDGET 세 게이트 모두 통과 → 🟢
- **반증** — 셋 중 하나라도 실패 → 🔴 CLOSED-NEGATIVE (a_paper_negative_ok)

## 2. 동기

- H_871(routing-z scale-ladder, 🟢 ARTIFACT)이 명시적으로 남긴 잔여 lever다: tiny→small 에서 z 가 +0.59 올랐으나(그건 E 4→8 step), small→mid 는 E=8 고정에서 거의 평탄(+0.02) — **depth(d/L)는 z 를 움직이지 못한다**. z>3.0 gate-A 를 향한 남은 lever 는 expert **USAGE 자체**를 미는 것(dispatch-KL distill)이지 d_model 깊이가 아니다.
- 이 fire 는 rung 을 **MID 로 고정**한 채(scale artifact 제거) dispatch-KL lever 가 그 frozen rung 에서 z/dispatch-entropy 를 움직일 수 있는지 절제한다. baseline arm 이 곧 H_871 mid cell(KL_COEF=0).
- 토대: H_679 (PLASTICITY HW edge-learn 측정완료).

## 3. falsifier (사전등록 · 임계 frozen F-CLM-DISPATCH-KL_prereg.txt verbatim)

```
KL_COEF=0.10 ENT_MARGIN=0.10 Z_MARGIN=0.20 CE_BUDGET=0.10 steps=500 lr=1e-3 N_NULL=200
(1) F-CLM-DK-ENTROPY : kl mean dispatch-entropy >= baseline + 0.10 nats
(2) F-CLM-DK-Z       : kl mean routing-z       >= baseline + 0.20
(3) F-CLM-DK-BUDGET  : kl mean held-out CE      <= baseline + 0.10 nats
PASS(🟢) iff ENTROPY ∧ Z ∧ BUDGET. ANY fail → 🔴 CLOSED-NEGATIVE.
```

- 임계는 fire 전 frozen, post-tuning 0. dispatch-KL 항은 `out["usage"]` 에서 HERE 계산해 KL arm loss 에만 더한다(model.py / array_moe 미편집). routing-z 는 `CLM/model/judge_clm.routing_z` verbatim (null = Dirichlet(1) over E, N_NULL=200).

verdict 영속: `.verdicts/clm-dispatch-kl-distill/`

## 4. 방법

```
KL arm : total loss = CE + aux(baseline) + KL_COEF * KL(uniform || f), f = out["usage"] (E,).
baseline arm : KL_COEF=0 (= H_871 mid cell, 그 외 모든 config 동일).
rung = MID d512/L8/E8 arm AB · corpus = REAL kowiki two-lane · seeds {42,43,44}.
각 (arm, seed): 500 step Adam(lr=1e-3) → held-out eval 에서 dispatch_entropy=H(f),
  routing_z, held-out CE 측정. arm metric = seed 평균.
```

## 5. 측정

측정완료 (2026-05-31) — **GPU(RTX 5070, summer 192.168.50.60)** torch 2.11.0+cu130 device=cuda. backbone mid d512/L8/E8(13,653,768 params, HF dancinlab/anima-clm-verify). frozen threshold = prereg verbatim.

mean over seeds {42,43,44}:

| metric | baseline | kl | delta | gate | 판정 |
|:-------|---------:|---:|------:|:-----|:----:|
| dispatch-entropy (nats) | +2.0789 | +2.0790 | **+0.0001** | ≥ +0.10 | **FAIL** |
| routing-z | +2.1838 | +2.0773 | **−0.1065** | ≥ +0.20 | **FAIL** |
| held-out CE (nats) | +0.2053 | +0.2079 | +0.0026 | ≤ +0.10 | PASS |

- 두 arm 모두 8/8 distinct expert, H(f)≈2.0789 ≈ max_entropy log(8)=2.0794 — **dispatch 가 이미 uniform 천장**에 붙어 있다.
- lever_a_supported = false → **VERDICT RED**.

## 6. 결과

🔴 **CLOSED-NEGATIVE**. dispatch-KL distill 은 MID rung d512/L8/E8 에서 **INERT** — baseline dispatch 가 이미 uniform 천장(8/8 distinct, H(f) 2.0789 of max 2.0794)이라 balanced-target KL 이 다양성을 보탤 **여유(slack)가 없다**. 그래서 ENTROPY 가 안 움직이고(+0.0001 ≪ 0.10), routing-z 는 오히려 떨어진다(−0.1065). CE budget 게이트가 통과하는 건 lever 가 inert 라 비용이 0 이기 때문일 뿐, 그 대가로 산 다양성 이득이 없다.

- 이 RED 는 dispatch-KL 을 @L3 4번째 routing-escape lever 에서 **OUT** 으로 판정하고, z>3.0 을 향한 잔여 gate-A lever 가 dispatch balancing 이 **아닌** 다른 축(H_871 과 정합: 고정 E=8 에서 dispatch uniformity 가 아니라 expert COUNT E 가 z 를 움직였다)임을 isolate 한다.

**honest scope**: 측정 rung(MID 13.65M, REAL kowiki) 한정 — 배포 chip-array z>3.0 track 별개(a_scale_honest_scope). 임계 재조정 0.

## 7. 해석 (사전)

- **lever-A SUPPORTED(가정)** = dispatch balancing 만으로 z>3.0 escape 가능 → 배포 router 설계의 직접 lever.
- **본 결과(반증)** = 이 rung 에서 dispatch 는 이미 균형이므로 더 밀 곳이 없다. 다양성은 expert 수(E) / 구조 lever 에서 와야 한다(H_871). dispatch-KL 은 균형이 깨진 rung 에서만 잠재적으로 작동할 수 있고, MID rung 에선 아니다.

## 8. 논의

- **W2 무결성**: 동일 budget/seed/rung 에서 KL_COEF 단일 변수만 변화, 임계 변경 0 — 🔴 는 게이트를 낮춰 숨기지 않고 정직 보고.
- **a_paper_negative_ok**: dispatch-KL 을 budget-free diversity lever 로 OUT 시키는 fully-publishable 한 negative. INERT 의 메커니즘(uniform 천장)까지 측정으로 설명.
- **H_871 정합**: depth 도 dispatch-uniformity 도 고정-E rung 에서 z 를 못 움직인다 → z 는 expert COUNT 축에서 온다.

## 9. 양방향 sibling

- sibling: [H_871](./H_871_clm_routing_z_scale.md) (routing-z scale-ladder 🟢 — small→mid 평탄, 이 lever 의 모태)
- 토대: [H_679](./H_679_plasticity_hw_first.md) (PLASTICITY HW edge-learn)
- UNIVERSE SSOT: [CLM-CANDIDATES.md](./CLM-CANDIDATES.md) @L3 routing-escape lever A
- verdict: [.verdicts/clm-dispatch-kl-distill/](../.verdicts/clm-dispatch-kl-distill/)
