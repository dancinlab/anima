# H_1832 — 조각 개별학습 → mitosis 조합 (N7, 오너 아이디어)

**id:** H_1832
**slug:** fragment_train_mitosis_assembly
**tier:** 🔵 PROPOSAL (anima-native novel lever · 오너 아이디어 · HE pre-screen gated)
**date:** 2026-06-30
**source:** UNIVERSE (오너 brainstorm — "전부 개별로 조각 학습후 미토시스로 조합")
**렌즈:** `a_mitosis_train` (p8 cell-division) · `a_no_llm_frame_trap` · `break-walls` · `p8`
**wired:** PROPOSAL (미배선·미측정) — H_1821 HE 사전선별 먼저, 통과분만 engine-native

---

## 가설

각 개념 **조각(fragment)을 개별 gradient로 학습**한 뒤 **mitosis가 조립(assembly)**하면 재조합(G1)이 열린다. 학습된 전문가 조각들을 mitosis tick이 *구성적으로 합쳐* child를 만든다.

**🔑 벽과의 결정적 차별 (H_1310 campaign이 남긴 빈칸):**
- H_1310(from-scratch 순수분열 🔴) = **gradient 없음** → 본 가설은 조각마다 gradient 공급.
- H_1574(학습된 trunk를 *쪼갬* 🧱) = **partition(쪼개기)** → 본 가설은 **역방향 = assembly(조립)**: 여러 독립학습 조각을 mitosis가 *모음*.
- H_1310 종결 결론이 명시적으로 "gradient 또는 selection-pressure 필수"라 했고, 이 설계가 **정확히 그 gradient를 공급** + mitosis를 *partition이 아닌 assembler*로 씀.

## Design

1. N개 개념 조각을 각각 개별 gradient 학습(작은 expert, 조각당 1개 능력).
2. mitosis tick이 두/다수 학습된 조각을 **constructive assembly**로 합침(nearest-basin/additive 아님 = 핵심).
3. assembled child의 G1 측정 + control.
4. controls: best-single-fragment(조립 없음) · **additive-assembly baseline**(단순 합 — 이게 floor면 H_1825 회귀) · shuffle-assembly.

## Frozen bar (pre-register · p7)

| 항목 | bar |
|------|-----|
| 조립 child G1 | composed_distinct≥2 ∧ >best-single-fragment ∧ >additive-assembly, ≥2/3 → 🟢 / floor → 🧱 |
| assembly 인과 | mitosis-assembly-OFF=floor, ON(constructive)만 lift |

⚠️ 정직: novelty는 **constructive assembly op**에 있다 — 조립 op이 nearest-basin/additive면 H_1825 trained-bind floor로 회귀. gradient 공급(조각학습)은 H_1310 빈칸을 채우나, 조립 연산자가 여전히 additive면 벽 동일. HE 사전선별 통과 시 engine-native(live MITOSIS `core/engine_cli.hexa`).
