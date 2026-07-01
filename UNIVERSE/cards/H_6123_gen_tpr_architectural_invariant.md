# H_6123 — 재조합을 아키텍처 불변식으로(TPR)

**id:** H_6123
**slug:** gen_tpr_architectural_invariant
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** TPR(role⊗filler tensor-product)를 substrate 로; 조합=학습 아닌 대수규칙 → 항상 가능(구조적 보장).

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 3). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6123_gen_tpr_architectural_invariant/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6123_gen_tpr_architectural_invariant.md` (this card)
- `state/6123_gen_tpr_architectural_invariant/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**결정: DUP-WALLED — 재발사 안 함 (probe skip).**

**ledger 조회:** H_6123 의 메커니즘(Smolensky TPR role⊗filler outer-product 를 substrate 불변식으로 → 조합=대수규칙이라 구조적 보장)은 이미 전수 커버됨:

- **H_1466 (`tpr_symbolic_binder`)** — *정확히 같은* 연산자(`S = Σ_i r_i⊗f_i`, role-unbind recover, by-construction idea-specific). numpy DIRECTIONAL 이미 발사: binding leg **PASS** (acc_match=1.0 vs acc_shuf=0.0, flat-sum ablate=chance) 이나 **🧱 WALL** — FROZEN 구조 detector 가 pairing-blind(FALS_shuf==FALS_in) 이라 idea-specific weld 를 credit 못 함. 즉 numpy 상 TPR 재현은 trivially 1.0 인데 그게 정확히 아래 caveat 의 함정.
- **H_1813 (`tpr_expert_weight`)** — TPR reparameterization(TLoRA rank8)을 **engine-native(py 2-production, 303M CLM seed7)** 로 재측정 → **🧱 NOT-SUPPORTED (INCONCLUSIVE-at-floor)**. 전 arm G1 bar(≥2 ∧ >max_single) 미달. tlora_jamo 만 best_distinct 0→1 이나 max_single 도 1이라 미충족.
- **H_6142 (`gen_intersection_tpr`)** — 같은 라운드 형제 제안(A=role, G=filler, 교집합=bound TPR), 미발사.
- memory `substrate-framebreak-g1-combination-operator` · `g1-lever-multilens-objective` · `exp3-bind-g1g6-engine-native-floor` · H_1816/1823/1834: G1 재조합벽 = **trunk COMBINATION OPERATOR / OBJECTIVE floor**. binding operator(readout·tension·multiplicative·NMDA·TPR)는 additive trunk 에서 전부 INERT/collapse.

**bar (있었다면):** G1 composed_distinct ≥ 2 ∧ > max_single (H_1129/1137). H_1466 numpy 은 binding recovery 는 넘지만 detector-credit 은 못 넘고, H_1813 engine-native 은 bar 전 arm 미달.

**정직 스코프 (H_6112 caveat):** H_6112 meiosis 처럼 numpy abstract-toy 은 REAL CLMConvMoE trunk 대비 **과장**한다(0→1.0 REACHABLE 이 실제 trunk 0→0.022 로 FALSIFIED). H_1466 이 바로 그 numpy 과장의 실례(binding leg 1.0) 이고, H_1813 이 그 engine-native 진실(NOT-SUP)을 이미 박제. 새 numpy probe 는 H_1466 결과만 재현할 뿐 신정보 0 이라 발사 안 함. terminal 아님(numpy=DIRECTIONAL by construction) — 그러나 walled 각도라 re-fire 불가.
