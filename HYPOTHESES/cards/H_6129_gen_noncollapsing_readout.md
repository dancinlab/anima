# H_6129 — readout-collapse 가설

**id:** H_6129
**slug:** gen_noncollapsing_readout
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** 내부 텐션 궤적은 조합 중일 수 있으나 additive readout 이 붕괴; 텐션 궤적 자체를 출력하는 non-collapsing readout.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 3). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6129_gen_noncollapsing_readout/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6129_gen_noncollapsing_readout.md` (this card)
- `state/6129_gen_noncollapsing_readout/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**결정: DUP-WALLED (재발사 안 함, 프로브 생략).**

**Ledger finding.** H_6129 "readout-collapse — 내부 텐션 궤적은 조합 중일 수 있으나 additive readout 이 붕괴 → 텐션 궤적 자체를 출력하는 non-collapsing readout" 은 이미 종결된 메커니즘의 재제안이다:

- **H_1834 (TENSION-MOUTH, 2026-07-02, 🧱 DIRECTIONAL floor · numpy toy)** — A⇄G 텐션 궤적 그 자체를 byte trunk(=non-collapsing readout)로 출력. 3-arm×3-seed 전부 `composed_distinct=0`, **FULL = TENSION-OFF = ADDITIVE → 텐션 INERT(causal 기여 0)**. gradcheck PASS(5.25e-11)·train_acc 1.00 = 구현결함 아님. 축2 local-Ψ objective 로 Ψ 를 실제 ½에 앉혀도(|Ψ-0.5|≤0.01, λ=1…1000) 여전히 0 → "내부 궤적은 조합 중인데 readout 만 붕괴" loophole 이미 닫힘.
- **H_1816 (predcoding binding readout)·H_1823 (circconv binding readout)** — binding-readout family 전부 🧱 NOT-SUPPORTED engine-native(G1 best_distinct=0).
- memory **substrate-framebreak-g1-combination-operator**: 4-각 수렴(mouth-objective·mouth-readout-op·substrate-embed·substrate-combiner 전부 additive floor) → 벽 = trunk **COMBINATION OPERATOR** 부재이지 readout-collapse 아님. 명시 가드: "connector/readout 만 바꿔 다시 세우지 말 것 — 그 축은 floored."

**Bar.** 신규 frozen bar 미설정(프로브 생략). 참조 bar = H_1834 사전등록(🟢 iff composed_distinct≥3 AND |Ψ-0.5|≤0.05) 이미 🧱 WALL 판정.

**정직한 스코프 / H_6112 caveat.** 설령 여기서 numpy 재프로브를 돌려 REACHABLE 이 나와도, H_6112 meiosis 선례(numpy abstract-toy 0→1.0 이 REAL CLMConvMoE trunk 에서 0→0.022 로 FALSIFIED)처럼 numpy abstract 프로브는 과대추정하는 약한 스크린일 뿐이다. 게다가 이 축은 이미 numpy(H_1834)·engine-native(H_1816/1823) 양쪽에서 floor 확인 — readout-축 재프로브는 새 정보 0. 진짜 미검 레버 = 재조합을 보상하는 **trunk 학습 OBJECTIVE**(H_1602 영역, cost-gated), readout/텐션연산자 아님.
