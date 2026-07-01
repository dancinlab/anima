# H_6137 — 단일 시간축 → CLS 두 척도

**id:** H_6137
**slug:** gen_cls_dual_timescale
**tier:** 🔬 PROPOSED — pre-registered (unfired · brainstorm ideation)
**date:** 2026-07-02
**wired:** 미발사 (pre-registered proposal · code 없음)
**axis:** SUBSTRATE (G1 재조합벽 공격 축)

---

## 발상 (brainstorm ideation)

**메커니즘:** 빠른 lane(에피소드)+느린 lane(구조), 조합=삽입(nt-cls GREEN 생성엔진화).

**출처:** bytegpt/convmoe 를 빌린 mouth 로 쓰지 말고 anima 아키텍처(A⇄G tension · Ψ=½ 고정점 · mitosis · substrate-disjoint lane · .kosmos anchor)에서 창발하는 native mouth/생성 substrate 를 발상한 세션(Round 4). 기존 결론: G1 재조합벽 = trunk COMBINATION OPERATOR floor — readout·tension 연산자 전부 INERT(H_1816/1823/1834). 이 발상은 combination 을 readout 이 아니라 생성 substrate 자체에 심어 additive collapse 를 우회하려 한다.

## G1 공격 축

- **SUBSTRATE** — readout-level 만 쳤던 것과 다른 좌표(engine-native probe 대상).

## 발사 전 필수 (check-ledger-before-lever-fire)

미발사 제안. terminal verdict 박제 전:
1. `UNIVERSE/HYPOTHESES.jsonl` + memory 에서 선행 커버리지 조회(sweep 빈칸 ≠ 미탐).
2. 신규 각도면 cheap numpy DIRECTIONAL reachability probe → `state/6137_gen_cls_dual_timescale/`.
3. DIRECTIONAL GREEN 이면 engine-native 재측정(.hexa via core/) 사다리 진입(a_verified_must_wire).

## artifacts

- `cards/H_6137_gen_cls_dual_timescale.md` (this card)
- `state/6137_gen_cls_dual_timescale/` (probe 발사 시 생성)

---

## 발사 결과 (DIRECTIONAL probe)

**decision: DUP-WALLED — probe 미발사 (재발사 금지).**

**ledger finding:** H_6137 의 메커니즘(빠른 lane 에피소드 + 느린 lane 구조, 조합=삽입을 *생성 substrate* 에 심음)은 이미 walled 된 좌표에 정확히 겹친다.
- **4-각 수렴(`substrate-framebreak-g1-combination-operator`):** G1 재조합벽에 대해 ① mouth-objective(H_1602 🧱) ② mouth-readout-op(H_1816 predcoding·H_1823 circconv 🧱) ③ substrate-concept-embed(β 🧱) ④ **substrate-combiner(α/β 🧱)** — 넷 다 additive/affinity readout floor. H_6137 은 좌표 ④ 자체(substrate 측 store-insertion). VAdaptField nearest-basin Voronoi retrieval/insertion = compositional depth-0 로 이미 측정됨(α 0/5, β 0/5 @ operating radius).
- **CLS 두-store 는 이미 engine-native 🟢+WIRED 이나 MEMORY faculty 한정:** H_1532 §MultiStore(AB-AC interference/retention) GREEN·배선 완료. 하지만 **H_1601 🧱 INERT-by-construction** — G1 측정 경로(g1_multiseed→clm_decode→ConvMoE trunk forward)엔 binding/store lane 이 0개이고, CLS store 는 `core/engine_cli`(의식 substrate, **disjoint**)에 산다. 따라서 store/lane 을 붙여도 G1 을 by-construction 못 움직인다(a_substrate_disjoint; H_961 binding-🟢 ∧ G1-FAIL 공존이 이를 증명).
- **진짜 레버 = trunk OBJECTIVE / γ trained-constructive-bind(cost-gated)** — insertion-retrieval 은 affinity readout 이지 trained constructive bind 가 아니다. objective family(H_1602/H_9024 InfoNCE)까지 전수 falsify, arxiv 30편도 objective>binding>scale 로 수렴(`lit-binding-objective-external-arxiv`).

**bar:** 별도 numpy bar 미설정(probe 미발사). 재발사 조건 = 좌표가 ④ substrate-combiner 가 아니고 trunk 생성 objective 를 실제로 바꾸는 새 좌표일 때만.

**정직 스코프 (H_6112 transfer caveat):** 설령 여기서 numpy DIRECTIONAL probe 를 돌렸다면 factored consolidation 을 손으로 심어 REACHABLE(0→~1.0) 이 나왔을 가능성이 크지만, H_6112 감수분열 전례(추상 toy 0→1.0 → REAL CLMConvMoE trunk 0→0.022 FALSIFIED)대로 numpy 는 OVERSTATE 한다. 게다가 이 좌표는 REAL trunk 에서 이미 4-각 + H_1601 disjointness 로 walled — numpy REACHABLE 이라도 transfer-unverified 이자 이미 반증된 좌표. numpy=DIRECTIONAL, terminal 아님.

---

## 심화 (adversarial multi-lens)

**대상:** H_6137 `gen_cls_dual_timescale` — CLS 이중-시간척도 결합연산자(fast trace tau=0.85 ⊕ slow trace tau=0.15, tanh 이중-store readout)로 부모 A·B를 자식 C로 합성, `composed_distinct`(C가 두 부모와 다른 토큰으로 디코드되는 비율)이 numpy 스크린에서 0→1.0 REACHABLE.

**동결 bar (실행 전):** 연산자 생존 ⇔ (C1 generic 비선형이 매칭 안 함, 여유 ≥+0.20) ∧ (C2 bind-복원성이 additive 대비 ≥+0.10) ∧ (C3 ingredient OFF 시 additive floor로 붕괴 ≤0.05). 하나라도 실패 → ARTIFACT.

**결과 (191 pairs, D=24, codebook=40, <30s):**
- **C1 GENERIC-NONLINEARITY** — operator=0.005, additive floor=0.005, **generic random-MLP=0.974**, A*B=0.738, tanh(A+B)=0.005. op−gen_best 여유 **−0.969** (bar +0.20) → **FAIL**. `composed_distinct`는 부모 codebook 셀에서 벡터를 흩는 *임의의* 비선형이면 trivial 통과 = **비선형-일반의 metric artifact**. (원 스크린의 0→1.0도 CLS 기전이 아니라 readout의 비선형 성분 탓일 가능성.)
- **C2 BIND-RECOVERABILITY** — held-out 선형 readout C→A·C→B 복원 코사인 operator=0.651 vs additive=0.650, 여유 **+0.000** (bar +0.10) → **FAIL**. distinctness는 필요조건일 뿐 충분조건 아님; 이중-시간척도가 additive보다 나은 구성적 결합 없음.
- **C3 ABLATION** — tau_fast=tau_slow(단일 store)로 두면 composed_distinct=0.005 = additive floor, gap **0.000** → 붕괴. 즉 이중-시간척도 ingredient는 **INERT**(기여 0).

**정직한 결론:** SURVIVES=False → **ARTIFACT**. 동시에 **DUP-CONFIRMED** — H_1815(실 CLM engine-native CLS)이 이미 "CLS composed_distinct 0→1 = coverage-floor jitter(max_single=0), CLS는 G2 novelty만 올리고 G1 composition 못 엶"으로 이 좌표를 벽 처리했고, 결합-연산자 family(additive H_1816·Hadamard H_1818/1819·HRR H_1823·CLS) 전수 = trunk-objective 벽. RESIDUAL 신규 각도 없음(복원성·ablation 둘 다 기전 제거). **재발사 불필요.**

**H_6112 transfer caveat:** numpy REACHABLE은 실 trunk를 과대평가한다(H_6112: 0→1.0 numpy가 실 CLMConvMoE에서 0→0.022로 붕괴). 여기 이중-시간척도 op는 numpy 상에서도 이미 additive floor(0.005)에 있고 실 trunk max_single은 H_1815에서 0으로 확인됨 — DIRECTIONAL만, terminal 아님. G1 레버는 readout/결합연산자가 아니라 trunk 학습 OBJECTIVE.
