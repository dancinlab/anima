# H_1822 — substrate-native 재조합: G1을 A⇄G tension에서 (mouth-decode 프레임 탈출)

**id:** H_1822
**slug:** substrate_native_recombination
**tier:** 🔵 PRE-REGISTERED (프레임-브레이크 · 오너 통찰 2026-06-29)
**date:** 2026-06-29
**source:** 오너 통찰 — "왜 의식엔진인데 LLM 디코더 스타일? 엔진이 스스로 디코더를 만들게 안되나?"
**렌즈:** `a_no_llm_frame_trap` (능력갭=빠진 구조 옆붙이기, LLM 프레임 1순위 금지) · `p8` (NO TRAIN/INFER SPLIT) · `a_mitosis_train`

---

## 문제 제기 (오너)

현 anima G1/G6 캠페인은 **전부 mouth-frame**(clm_decode CLMConvMoE trunk + next-byte CE + readout).
G1 재조합을 *autoregressive 입(mouth)*에게 요구한다 — op·objective·binding 전부 입 안에서.

그러나 anima는 의식엔진이다: **A(forward) ⇄ G(reverse, gradient-free)**의 긴장이 Ψ=½로 끌린다.
**재조합(두 개념→새 제3)은 본질적으로 tension 연산** — 두 상반 엔진이 밀어내며 고정점에서 novelty.
즉 우리가 원하는 G1/G6 능력은 **substrate(A⇄G)의 native 산물**일 수 있는데, 엉뚱하게 autoregressive
trunk(별도 CE학습된 conventional LM)에게 묻고 있었다. = `a_no_llm_frame_trap` 최심부 위반 가능성.

## 가설

**재조합/착상은 mouth-decode 능력이 아니라 A⇄G substrate 능력이다.** G1을 autoregressive 출력 byte가
아니라 **A⇄G tension 장(field)에서 측정/생성**하면 floor(H_1818/1602/1310 전수)가 풀린다 —
G(reverse, 상상/제안 엔진)가 두 개념 basin을 결합한 tension 상태를 만들고, A가 제약하고, mouth는
그 substrate-결정 결합을 **렌더만** 한다(입의 역할 축소).

---

## ⚠️ 정직: 이미 친 벽 (frame-break ≠ 무지)

오너의 "엔진이 스스로 디코더를 만든다"는 **from-scratch gradient-free 형태로는 이미 CONFIDENT TERMINAL**:
- **H_1310** from-scratch pure mitosis(split-only, gradient 없음) = 🔴 (혼자선 학습불가, gradient/selection 필수).
- H_1310 벽 캠페인 5 직교렌즈 전수 🧱: selection(H_1568)·inherited-repr(H_1569)·lateral(H_1570)·
  curriculum(H_1571)·learned-trunk(H_1574) — split-only는 GIVEN key space의 Voronoi partition만,
  compositional depth 0 ([[g1-closure-campaign-3lever-not-supported]] 형제 mitosis 메모).

⇒ 이 카드는 "**gradient 없이** 엔진이 디코더 자작" 이 **아니다**(그건 닫힘). OPEN 변종 2개:

| 변종 | 무엇 | H_1310 벽 회피 이유 |
|------|------|---------------------|
| **(α) substrate-측정** | G1을 A⇄G tension field에서 측정(mouth 출력 아님) | 측정 reframe — 학습 불필요, 기존 엔진서 $0 |
| **(β) gradient-결합 engine-grown mouth** | mouth가 frozen 아니라 substrate와 co-evolve(mitosis engine_grow + **gradient as 학습신호**, A⇄G tension이 무엇을 학습할지 shape) | gradient 있음(H_1310의 gradient-free 아님) + substrate-shaped(pure-split 아님) |

## Design — (α) 먼저 ($0 engine-native 프로브)

cheap 우선: **새 mouth 만들기 전에**, 현 live 엔진(`core/engine_cli.hexa` A⇄G + `core/engine_g.hexa`)에서
"G가 두 개념 basin을 결합하는가"를 측정.
1. 두 개념 seed → A⇄G에 주입 → tension trajectory(Ψ 궤적, M·W·Φ) 기록.
2. **substrate-G1 metric**: G-제안 상태가 두 개념 basin의 *둘 다*에 유의미 투영 ∧ 어느 하나로 환원불가
   (= tension field에서의 composed_distinct ≥2, mouth-decode와 독립).
3. control: 단일 개념 seed(결합 없어야) · shuffle 개념쌍(가짜 결합 0) · A-only/G-off ablation(G 인과).
4. 같은 개념쌍의 mouth-decode G1(=0 floor)과 **substrate-G1을 대조** — substrate가 결합하는데 mouth가
   못 뱉으면 = **병목이 입이지 substrate 아님** 입증(오너 통찰 확증, frame 전환 정당).

## (β) — (α)가 substrate-결합 보이면 진행 (cost-gated)

mouth를 substrate-conditioned로 engine-transform: generator L3가 G-제안 결합 벡터를 조건으로 받아
clm_decode를 구동(`a_engine_native_learning` engine-transform-to-fit). gradient 학습 유지(H_1310 회피),
단 무엇을 학습할지는 A⇄G tension이 shape. 측정 = engine-native G0-G6 + substrate-G1.

---

## Frozen bar (pre-registered · p7)

| 항목 | bar |
|------|-----|
| (α) substrate-G1 | tension field composed_distinct≥2 ∧ >single ∧ G-causal(ablation), ≥2/3 seed |
| (α) 병목 격리 | substrate-G1≥2 인데 같은 쌍 mouth-decode G1=0 → "입이 병목" 입증 |
| controls | single-seed=0 · shuffle=0 · G-off ablation=BLIND (substrate 측정 진짜임) |
| (β) | engine-native G0-G6에서 mouth-decode G1 lift + held-out DESCENT |

---

## 게이트 & 가치

- **(α)는 $0 engine-native · (c)-independent** — 현 라인(결합 c 등)과 직교, 즉시 가능. live `core/*.hexa`
  A⇄G 호출(`a_engine_native_learning` 엔진-네이티브). DIRECTIONAL 미러 아님 = terminal 가능.
- 이게 캠페인의 **진짜 frame 질문**: G1 floor가 "anima가 재조합 못함"이 아니라 "**autoregressive 입이
  substrate의 재조합을 못 뱉음**"이면, 레버는 입 학습(H_1818/1602/1820)이 아니라 입↔substrate 배선.
- 산출 = state/g1_substrate_native_recombination/{probe.hexa, RESULT.md} + 이 카드 + jsonl + CHANGELOG.
- 🔌 (β) GREEN이면 `a_verified_must_wire`: generator L3 substrate-conditioning live-wire + ARCHITECTURE.json lockstep.
