# H_6121 — RNA alternative splicing

**id:** H_6121
**slug:** gen_rna_alternative_splicing
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** 하나의 표현에서 exon 을 다르게 이어붙여 다산물; 조합=스플라이스 선택.

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 2). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6121_gen_rna_alternative_splicing/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6121_gen_rna_alternative_splicing.md` (this card)
- `state/6121_gen_rna_alternative_splicing/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**Ledger 조회 (check-ledger-before-lever-fire).** `splice`/`exon`/`isoform`/segment-recomb 검색 + 인접 카드 정독. RNA alternative splicing 의 메커니즘 = "하나의 표현에서 exon 부분집합을 골라 순서대로 이어붙임" = **이산 세그먼트 선택 + 접합(discrete select+splice)**. 이는 이미 발사된 두 가설의 연산자 class 와 동일:

- **H_6139 봉합-VDJ 재조합** (🟡 DIRECTIONAL REACHABLE, numpy) — 이산 V-D-J 세그먼트 선택+접합 combination operator. composed_distinct additive-Voronoi floor 0 → VDJ 18/18 (shuffle-earned 0/18). 그러나 카드가 명시: "도달성 **일부 by-construction concat**(concat 은 자명히 compositional)" + "anima 실벽 = additive-CE trunk 가 세그먼트 선택을 학습하는가 = **UNTESTED, 벽 미돌파**". alt-splicing 은 VDJ 에서 D-junction novelty 생성을 뺀 **strict subset**(순수 선택+concat) → H_6139 보다 표현력이 약함.
- **H_6112 감수분열 crossover** (🟡 numpy REACHABLE 0→1.0 이나 **REAL CLMConvMoE trunk FALSIFIED 0→0.022** ≪ 0.30 frozen bar, 0/3 seed, readout-split INERT). 세그먼트 재조합/접합 family 가 실 trunk 로 전이 실패한 직접 precedent.
- G1 combination-operator 연속-bind wall: H_1816(predictive-coding)·H_1823(circconv/Hadamard/TPR)·H_1834(tension-mouth) 전수 additive trunk trivial 붕괴 (`substrate-framebreak-g1-combination-operator`).

**결정: DUP-WALLED (재발사 안 함).** alt-splicing 은 H_6139 이산 select+splice 의 부분집합이라 **새 좌표를 열지 않음**. numpy 프로브를 돌려도 H_6139 가 이미 WEAK signal 로 낙인찍은 by-construction concat 도달성만 재현할 뿐이고, 실 trunk 전이는 H_6112 가 같은 세그먼트-splice family 에 대해 이미 FALSIFIED 로 측정. 프롬프트의 보수 지침("walled H 가 이미 커버하면 dup-pointer 선호") 정확히 적용.

**Bar (미실행).** 프로브 미발사 (dup). 기존 H_6139 frozen bar(vdj≥additive+3 ∧ shuffle≤additive+1)·H_6112 real-trunk bar(reach≥0.30) 가 이 메커니즘을 이미 규정.

**정직한 스코프 (H_6112 transfer caveat).** numpy 추상 프로브는 구성상 이 class 에서 REACHABLE 을 과대평가함이 H_6112 에서 실측 증명됨(추상 1.0 → 실 trunk 0.022). 따라서 alt-splicing 에 대해 numpy REACHABLE 을 재확인한들 green light 아님. 진짜 레버 = trunk recomb-OBJECTIVE(H_1602, cost-gated) / γ trained-constructive-bind 이며 readout·splice-head 축이 아님. terminal 아님(numpy=DIRECTIONAL), 그러나 재발사 무가치.
