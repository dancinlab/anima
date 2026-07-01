# H_6147 — Turing-CLS (#11+#34)

**id:** H_6147
**slug:** gen_turing_cls
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)
**~dup:** #11+#34

---

## 발상 (brainstorm ideation)

**메커니즘:** 느린 lane=morphogen source, 빠른 lane=diffusion, 조합=패턴형성 시퀀스.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 5). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6147_gen_turing_cls/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6147_gen_turing_cls.md` (this card)
- `state/6147_gen_turing_cls/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**Ledger 확인 (check-ledger-before-lever-fire):** Turing reaction-diffusion morphogen 연산자는 이미 광범위 커버 — H_1655(`reaction_diffusion_morphogen_bind`, D_v≫D_u 차등확산+비선형 반응항, numpy cheap_test 명세 있음)·H_1734(`reaction_diffusion_morphogen_field`)·H_1639(traveling-wave)·H_6114(Turing RD) 전부 🔵 PRE-REGISTERED DESIGN(측정 0)·🔬 PROPOSED(미발사). H_6147 의 CLS 축(느린 lane=morphogen source ⊥ 빠른 lane=diffusion)은 H_1655 의 차등확산(D_v≫D_u) 코어와 사실상 동일 메커니즘이나 그 cheap_test 가 **한 번도 실측되지 않음** → dup-walled 아닌 **NOVEL-ANGLE**(H_6132 이 H_1622 미실행 cheap_test 를 돌린 것과 동일 템플릿). G1 재조합벽 = trunk COMBINATION OPERATOR floor, readout/tension/predictive/multiplicative/NMDA 연산자 전부 additive trunk 붕괴 🧱(H_1816/1823/1834).

**결정:** probed-novel (미측정 pre-registered cheap_test 실행 + CLS 차등-timescale 을 ablation 으로 격리).

**수치 (numpy, 24-cell ring, T=40, XOR of 2 independent concepts):**
- additive_floor XOR acc = **0.521** (linear readout 은 XOR 못함, 예상대로 chance)
- operator(Turing/CLS, D_u=0.05·D_v=0.50) acc = **0.969**
- ablation(equal-diff D_u=D_v=0.5) acc = **0.651**
- margin(op−add) = 0.448

**FROZEN bar (발사 전 사전등록, tune-to-green 금지):** GREEN iff op≥0.70 ∧ add≤0.60 ∧ margin≥0.15 ∧ **ablation FAIL(eq≤add+0.10)**. 결과: op✓ add✓ margin✓ 이나 **ablation 절 FAIL** — equal-diff 0.651 > add+0.10(0.621). 즉 차등-timescale(CLS) 제거해도 비선형 반응항 u·v 만으로 floor 위로 새어(0.651), 상승분을 CLS timescale-separation 에 깨끗이 귀속 불가 → **FALSIFIED-as-stated**.

**정직 스코프 (c9):** ① numpy=DIRECTIONAL by construction, terminal 아님. ② **H_6112 전이 caveat**: 감수분열 numpy toy 는 REACHABLE 0→1.0 였으나 동일 연산자가 REAL CLMConvMoE trunk 에서 FALSIFIED(0→0.022) — abstract numpy 는 OVERSTATE 하므로 여기 op=0.969 도 green light 아님, transfer-UNVERIFIED. ③ 프로브가 오라클 반응장/특징을 손수 건네므로 *학습된* trunk 조합(진짜 G1 질문) 미검. ④ 비선형 반응항이 이미 lift 를 만들어(equal-diff 0.651) CLS 축의 순수 기여가 불명확 = H_1816/1823/1834 의 "비선형 readout trick 은 additive trunk 에서 붕괴" 정합. engine-native/303M 미발사(cost-gated).
