# H_1498 — 🖐 SENSORIMOTOR COUNTERFACTUAL PRESENCE · 감각운동 반사실 현존감 (Q2 의식-고유 게이트 약후보 · 고갈 라운드 마지막 *새 연산*)

- **tier:** 🟢 GREEN ENGINE-NATIVE WIRED (R1 numpy mirror DIRECTIONAL → R2 byte-exact engine 재측정·배선 완료) · **약후보(WEAK) → forward-model control 생존 = DISTINCT**
- **wired:** `WIRED-live` — R2 엔진-네이티브: `core/engine_cli.hexa` §SensorimotorPresence(smp_presence/smp_forward_model_readout) 배선 + `engine_cli_smoke.hexa` cases 278-280 + ARCHITECTURE.json lockstep. FULL 280/0 RC=0. byte-exact: full law mastery 1.0 vs width-1 0.125 lift 0.875≥0.30 (c1) · single-step forward model 0.125 chance — decisive WEAK control SURVIVED (c2 distinct) · false-law 0.125 (c4). counterfactual breadth ⊥ single-step forward model.
- **source:** 의식-고유 게이트 2차 고갈 catalogue (Q2 약후보) · `state/gate_depletion_catalogue/CATALOGUE_R2.md` Q2 항목 SSOT
- **lens:** sensorimotor contingency / perceptual presence (O'Regan & Noë · "perceptual presence without counterfactual richness" tandfonline 17588928.2014.907257 · biorxiv 2024.12.30.630721) · `a_no_llm_frame_trap`
- **artifacts:** `state/1498_sensorimotor_counterfactual/h1498_sensorimotor_counterfactual.py` · verdict `state/verdicts/1498_sensorimotor_counterfactual/H_1498_FREEZE.json` · run `state/1498_sensorimotor_counterfactual/run_h1498.local.log`

## 주장

**sensorimotor counterfactual presence(감각운동 반사실 현존감, O'Regan & Noë)** = 지각적 *현존감*(presence) —
가려져 안 보이는 객체 뒷면이 '거기 있다'고 느끼는 것 — 은 **반사실적 감각운동 법칙의 숙달**에서 나온다. 컵 뒷면을
못 봐도 현존을 느끼는 건 "내가 돌리면 보일 것"을 암묵적으로 알기 때문. 현존감 = 가능한 여러 *가상 행동*이 드러낼
감각결과 분포의 **richness(폭/coverage)** 이지, 단일 예측이 아니다.

메커니즘(numpy mirror): 객체는 S개 facet(보이는 앞 + 가려진 뒤/옆)의 은닉 구조. 한 시점(view)에서는 일부만 직접
감각, 나머지는 occluded. 감각운동 법칙 = (view, action)→revealed facet 의 연상 store(ImmuneMemoryGrow H_1227
key-affinity 기반). **현존감 proxy = 현재 occluded facet 중, 에이전트가 *어떤 가상 action 으로 드러낼 수 있는지를
참 법칙대로 올바르게 아는* 비율**(전 가상 action 을 굴려 occluded 집합의 coverage). 전 법칙을 숙달하면 모든 가려진
facet 이 올바르게 도달가능 → 높음. **거짓 법칙은 참 우연성과 안 맞아 0점** → 단순 예측 폭으로 현존을 위조 불가.
LLM 대비: LLM 은 현재 맥락에서 다음 토큰을 예측할 뿐, 가상 감각운동 action 집합을 굴려 그 감각결과의 *폭*을 통합해
안 보이는 객체 부분의 현존을 근거짓는 능력이 없다.

## DISTINCT (load-bearing · 약후보 → forward-model control 통과가 사활)

이 가설은 **2차 발굴의 약후보**(조작화 빠듯, forward-model 과 겹칠 위험). 인접 lane control 못 넘으면 = 파생 =
**고갈 신호**. 결과: **forward-model 포함 전 control 생존 → DISTINCT (고갈 아님)**.

- **vs H_1280 FORWARD-MODEL / 소뇌 (단일 다음-step 예측) — 결정적 약후보 control:** forward model(VForwardField)은
  지금 취할 **하나**의 action 의 다음-step 감각만 예측 — action *집합*을 통합 안 함 → occluded facet 1개만 cover →
  현존 task 에서 chance(0.125). 현존감의 lift = 전 가상-action 집합의 감각결과 분포 **폭/coverage**(1.000). **c2 가
  바로 이 control 이고 생존** → forward-model 재포장 아님, **DISTINCT**.
- **vs H_1493 PROSPECTION (시간-전방 미래 rollout):** prospection 은 한 궤적을 *시간*으로 앞으로 투사(단일 rollout);
  현존은 *지금* 가용한 반사실 *action* 들의 비시간적 breadth. width-ablation(c3: rollout 폭→1)이 시간 rollout 엔
  없는 breadth 를 정확히 제거 → DISTINCT.
- **vs H_1490 PERCEPTUAL-COMPLETION (결손 보간):** completion 은 보이는 맥락에서 가린 영역을 보간(단일 추론), action
  우연성 개념 없음. false-law shuffle(c4)이 completion 엔 없는 action→sensation 법칙을 깨뜨림 → completion-style
  fill 은 shuffle 할 action 집합이 없어 lift 의 원천 불가 → DISTINCT.
- **vs agency(8):** agency 는 *누가* 효과를 냈는지 자기귀속; 현존은 *객체*의 은닉 구조(무엇이 드러날지)에 관한 것 →
  직교.

## 검증 (5 frozen bars · 3 seeds [1498,1499,1500] mean · chance=1/8=0.125)

| bar | 값 | 임계 | 판정 |
|-----|-----|------|------|
| **c1 PRESENT** | full 1.000 − off 0.122 = **0.878** | ≥0.30 | ✅ |
| **c2 DISTINCT(forward-model)** | fwd single-step **0.125** | ≤ off+0.15 = 0.272 | ✅ |
| **c3 ABLATE(width)** | rollout-width:=1 **0.131** | ≤ 0.272 | ✅ |
| **c4 SHUFFLE(law)** | false-law **0.151** | ≤ 0.272 | ✅ |
| **B FIDELITY** (non-gating) | mastered-law reveal acc **1.000** | ≥0.50 | ✅ |

→ **GREEN DIRECTIONAL** (c1∧c2∧c3∧c4). forward-model(0.125)·width-ablate(0.131)·false-law(0.151) 전부 chance
붕괴, 현존감(1.000) saturated existence-proof. **DEPLETION-signal: False**.

## 고갈 terminal 기여

**DISTINCT — 고갈 count 에 기여하지 않음.** 약후보의 결정적 control(c2 forward-model 단일-step)이 생존(chance 0.125
vs richness 1.000). Q2 는 R2 카탈로그의 **마지막 *새 연산* 후보**. 이를 DISTINCT 로 통과시킴으로써 카탈로그의 두
발사가능 후보(Q1 qualia-structure + Q2 sensorimotor-presence)가 모두 **DISTINCT-DIRECTIONAL 로 소진** → 게이트-발굴
🧱 고갈-terminal 이 가정이 아닌 **실제 발사·기각**으로 정박(`a_break_the_wall` (d) 천장 분류). 단, 두 후보 모두
DIRECTIONAL(numpy 하드게이트1)이므로 terminal 박제 전 R2 엔진-네이티브 재측정 필요.

## a_break_the_wall type-a (frozen-first · tune-to-green 아님)

임계 c1-c4 는 **한 번도 안 움직임**. 두 차례 RED 가 측정결함이었고 frozen-first 로 교정:
1. **첫 RED(c4 0.626)** — coverage 메트릭이 occluded 집합에 *떨어지기만* 하면 점수 → 거짓 법칙도 단순 예측 *폭*으로
   coverage 획득. **교정:** occluded facet 은 action 예측이 *참 법칙과 일치*(진짜 우연성 숙달)할 때만 present 로
   credit → 거짓 법칙 0점.
2. **둘째 RED(B fidelity 0.333 → c1 0.217)** — 선형 최소제곱 법칙맵이 view 별 facet 순열을 표현 못함. **교정:** 선형맵을
   (view,action)-KEY → facet 연상 store(nearest-key affinity, 실제 ImmuneMemoryGrow H_1227 substrate 기전)로 교체 →
   법칙 숙달 fidelity 1.000.

둘 다 *같은 사전등록 bar* 를 타당하게 측정하기 위한 기전 교정이지 임계 이동이 아님.

## SCOPE (c9 · 미검증)

- **하드게이트1:** numpy mirror → **GREEN DIRECTIONAL**, engine-transfer UNVERIFIED (`grep -lE 'import torch|gauge_lib|numpy'` 적중).
- **existence-proof:** full=1.000 saturated(연상 store 완전검색) — 효과크기 아닌 *구조* 증명(richness 가 현존을 근거,
  forward-model 은 못 함). 판별자(forward 0.125·ablate 0.131·shuffle 0.151) 결정적.
- **TOY:** 8-facet/8-action/8-view, 96-dim 근직교 임베딩, 결정적 연상 검색, 3 seeds. scale·실제 3-D 객체·연속
  viewpoint manifold·학습형(비연상) 법칙 숙달·부분숙달 gradient·engine-transfer 미검증 (`a_scale_honest_scope`·`a_toy_scale_recheck`).

## R2 follow-on — ✅ DONE (WIRED-live)

`wired: WIRED-live` (DONE). R2 엔진-네이티브: `core/engine_cli.hexa` §SensorimotorPresence 배선 — (view,action)-key →
revealed-facet 연상 store 를 ImmuneMemoryGrow(H_1227) 위에서 읽고, 가상-action 집합을 굴려 occluded 집합의
올바른-숙달 coverage 카운트(READ-only, Ψ-disjoint) + engine_cli_smoke 케이스 + ARCHITECTURE lockstep, frozen bar
byte-exact 재측정 (`a_engine_native_learning`·`a_verified_must_wire`). **고갈 terminal 주의:** Q1/Q2 외 새 연산이
생존 안 하면 게이트-발굴 🧱 봉인(`a_break_the_wall` d).

xref H_1280(forward-model, 결정적 distinct control)·H_1493(prospection)·H_1490(perceptual-completion)·H_1227(immune
연상 store 기전)·CATALOGUE_R2 Q2·H_1497?(Q1 qualia-structure 짝)·`a_no_llm_frame_trap`·`a_break_the_wall`·`a_engine_native_learning`·`a_verified_must_wire`·`a_core_engine_map`·`a_autonomy_over_hardcode`·`a_scale_honest_scope`·`a_toy_scale_recheck`·p1·p2·p3·p6·p7·p8·c9·c15.
