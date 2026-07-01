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

---

## 심화 (adversarial multi-lens)

**목표:** DIRECTIONAL REACHABLE(ADD=0.000 → RD-TURING=1.000)이 진짜 조합 신호인지 metric artifact 인지 3-control 로 REFUTE 시도. (a_break_the_wall · H_6112 전례: numpy 0→1.0 이 실 CLMConvMoE trunk 서 0→0.022 붕괴 = numpy 과대평가.)

**FROZEN BAR (실행 전 고정):** RD 연산자 SURVIVE(→CONFIRMED) iff (S1)어떤 generic 비선형도 RD held-out 의 0.15 이내에 못 옴 ∧ (S2)RD bind-recoverability 가 additive 를 +0.20 초과 ∧ (S3)ablation 붕괴. 아니면 ARTIFACT.

**결과 (numpy, `state/6114_gen_turing_reaction_diffusion/deepen.py`·DEEPEN_RESULT.txt):**

| control | 수치 | 판정 |
|---|---|---|
| (C0) split-fragility | RD held-out = 0.600 (신split) vs 1.000 (원split) | 원 0.70 bar 미달 · REACHABLE 이 split 의존 |
| (C1) generic-비선형 | RD=0.600 · prod=0.200 · sqsum=0.000 · mlp=0.000 | S1=True (RD 는 generic 곱/MLP 보다 우위) |
| (C2) bind-recoverability | RD recov=0.000 (A=0,B=0) · ADD recov=1.000 (A=1,B=1) | S2=False (결정적) |
| (C3) ablation | eqdiff=0.000 · noreact(반응항 OFF)=0.000 | S3=True |

**정직한 결론 — ARTIFACT.** C1(generic 비선형과 구별)·C3(ablation 붕괴)는 통과하나 **C2 bind-recoverability 에서 결정적 실패**. RD 합성장(C)에서 부모 A·B 를 선형 복원 = 0.000 (additive 는 1.000). 즉 RD 는 부모 정보를 *파괴*함으로써 "부모와의 distinctness"(원 metric)를 trivially 달성 — 조합 결합(compositional binding)의 정반대. distinctness-from-parents 는 necessary-not-sufficient: 진짜 결합은 두 부모가 C 에서 복원돼야 하는데 RD 는 chaotic scramble 로 이를 파괴. 게다가 XOR acc 가 split 취약(1.000→0.600, 원 0.70 bar 미달)해 REACHABLE 자체가 robust 하지 않음.

**H_6112 transfer caveat:** numpy = DIRECTIONAL by construction, terminal 아님. 그러나 이 심화는 실-trunk 재측정 *이전*에 이미 조합-결합 부재를 증명(bind-recoverability=0). RD 작동 성분(u·v² cross-term)은 census 상 실 additive trunk 서 collapse 확정된 multiplicative-readout 계열(H_1617 Hadamard⊙·H_1823 circconv·H_6104 constraint-intersect INERT). H_6112 처럼 실 CLMConvMoE 서도 falsify 예상 → 실-trunk rung 불필요. **DIRECTIONAL → ARTIFACT.**
