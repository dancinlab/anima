# H_6114 — 발생학 Turing 패턴

**id:** H_6114
**slug:** gen_turing_reaction_diffusion
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** 두 morphogen(개념) reaction-diffusion 이 자발적 새 공간패턴=조합.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 2). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6114_gen_turing_reaction_diffusion/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6114_gen_turing_reaction_diffusion.md` (this card)
- `state/6114_gen_turing_reaction_diffusion/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**ledger finding:** 이 메커니즘(두 morphogen reaction-diffusion → 자발적 새 공간패턴 = 조합)은 이미 **두 번 사전등록**돼 있음 — H_1655 (Turing Reaction-Diffusion Morphogen Binding, 🔵 측정 0) · H_1734 (Reaction-Diffusion Morphogen Field, 🔵 측정 0). 둘 다 동일한 $0 numpy cheap test(Gray-Scott activator-inhibitor, Turing ON vs equal-diffusion control)를 사전등록해 놓고 한 번도 발사 안 함. H_1639(traveling-wave interference) 도 인접 자매. 따라서 H_6114 는 신규 좌표가 아니라 **미측정 사전등록 메커니즘의 재제안** — 이번 probe 가 H_1655/H_1734 의 never-fired cheap test 를 discharge.

**decision:** NOVEL-MEASUREMENT (probed) — 벽은 아니지만(pre-registered unmeasured), 작동 성분(비선형 u·v² cross-term)은 이미 walled 된 multiplicative-readout 계열(H_1617 Hadamard⊙ · H_1823 circconv · H_6104 constraint-intersect 전부 INERT)에 속함.

**numbers (numpy, `state/6114_gen_turing_reaction_diffusion/probe.py`·RESULT.txt):**
- 과제: 독립 개념 A,B ∈ {0..3}, target = 2-bit XOR conjunction(4-class, 비분리), held-out 5/16 combo.
- ADDITIVE floor held-out acc = **0.000**
- RD-TURING (Du=0.16, Dv=0.08) held-out acc = **1.000**
- RD equal-diff CONTROL (Du=Dv=0.12, Turing OFF) acc = **0.000**

**FROZEN BAR (실행 전 고정, p7):** GREEN-DIRECTIONAL iff RD-Turing ≥ 0.70 ∧ (RD−ADD) ≥ +0.20 ∧ control ≤ 0.35. 실측: c1 True · c2 (+1.000) True · c3 True → **GREEN-DIRECTIONAL 통과**.

**honest scope (c9 + H_6112 caveat):** numpy = DIRECTIONAL by construction, terminal 아님. GREEN 은 green light 가 **아니다** — H_6112(meiosis)에서 동일하게 numpy 추상 toy 가 0→1.0 REACHABLE 이었으나 **실 CLMConvMoE trunk 에서 FALSIFIED**(0→0.022 ≪ 0.30). 여기 reachability 는 순전히 u·v² 비선형 곱항이 XOR 을 표현할 수 있어서 발생 — 그 곱항이야말로 additive trunk 에서 collapse 하는 것으로 이미 census 확정된 성분(H_1617/H_1823/H_6104 INERT). equal-diff control 0.000 은 pattern-selection 이 Turing 불안정성에 의존함을 확인하나, 실 trunk transfer 는 **미검증·고위험**. terminal 박제 전 필수: held-out mirror-CE DESCENT → CORE `--engine conv` mount frozen G1(H_1129)·G6(H_1464) byte-exact engine-native 재측정 → ckpt PULL(a_fire_recover_complete). 대개 rung(1.5) 실-trunk toy A/B 에서 falsify 될 것으로 예상(readout/multiplicative 축 전면 floor).
