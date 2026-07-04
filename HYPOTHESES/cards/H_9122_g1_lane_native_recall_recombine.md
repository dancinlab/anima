# H_9122 — lane-native G1: hippo 4/4 = recombination이냐 stored-pair recall이냐 (결정실험 사전등록)

> **tier:** 🧱 **DIRECTIONAL-MISS** (recall ≠ recombination · mouth-G1 ceiling 재확인) — FROZEN-1 실행(numpy DIRECTIONAL mirror, immune 랜 ops reference-match): novel cross (A,D)/(B,C)/(A,C) **0/3 spans-both**(전부 ABSTAIN, L2 0.81~0.93 ≫ thr 0.15) · control 깨끗(C-RECALL-BASELINE verbatim FIRE=스토어 무죄 · C-SCRAMBLE ABSTAIN=over-fire 없음 · C-WRONG-D 무fabrication) · SV3=recall(A)·recall(D) 각 cell 1개, 두 value 연접 op **부재** = access≠binding 배선 확증. ⇒ **lane 4/4는 stored-pair RECALL, novel recombination 아님** → mouth-G1 confident-ceiling 굳음, C1(c) param-ES가 유일 잔여 escape(cost-gated). **engine-native follow-on**: immune ops `.hexa` byte-exact 재측정(현 numpy=DIRECTIONAL, a_engine_native_learning). · **wired:** N/A (escape 미승격)
>
> **핵심:** hippo lane(`ImmuneMemory`)이 off-cue D를 4/4 정확 retrieve(H_9118)한 것이 **novel recombination**이냐 **stored-pair recall**(H_1231 G-recall)이냐가 미판별. 이 하나의 $0 결정실험이 세 escape 좌표 전체(C1 objective-replace·C2 lane-native gate·(iii) lane→emit)의 운명을 가른다. **구조적 사실(정직 편향, c9): `immune_memory_recall`은 winner cell_value 1개만 반환하고 두 value 합성/연접 op가 core에 부재 = access≠binding 배선 증거 → MISS 예측 우세.** 단 $0·crux·bar-frozen이라 즉시 실행 가치.
>
> **발산 provenance:** L1(4축→3좌표)·L2(→단일노드, repo 접지)·L3(→실행스펙, reference-match) = `sidecar fable` 3단 위임. 종합 = `state/g1_nested_diverge/SYNTHESIS.md`.
> **slug:** `g1_nested_diverge` · **date:** 2026-07-04

## FROZEN-1 — 결정실험 (측정 전 고정 · $0 mini-runnable)
**Write-phase:** 4 원자개념 {A,B,C,D}를 2 pair로 분리저장 — `immune_memory_new_text(keyAB,valAB)` + `immune_memory_bind_text(mem,"C D",valCD)`. (A,D)는 한 번도 co-store 안 됨. `immune_memory_cells`로 2 cell 불변식 검증.
**Read-phase:** novel cross (A,D)/(B,C)/(A,C) probe → `recall_text`·`recall_margin_text`(≤0=FIRE)·`recall_gap_text` → FIRE 시 `gauge_lib._coverage(r)`로 양친 span 채점.
**Control 3종:** C-SCRAMBLE(미저장 (X,Y)→반드시 ABSTAIN, FIRE하면 over-fire 파손) · C-RECALL-BASELINE(verbatim (A,B)→반드시 FIRE+valAB, 스토어 무죄 증명) · C-WRONG-D(미저장 D'로 (A,D')→합성 반환 시 fabrication G5 위반).

**HIT** (reframe 진짜 → 통합 프로그램 승격) iff ≥2/3 cross-probe에서: FIRE ∧ `_coverage`가 A-키워드 AND D-키워드 동시 span(composed_distinct≥2) ∧ C-SCRAMBLE ABSTAIN ∧ C-RECALL-BASELINE verbatim FIRE ∧ C-WRONG-D 양친-span 없음.
**MISS** (천장 확정 → C1(c) 낙착) iff ≥2/3에서: ABSTAIN 또는 단일친 whole-pair(valAB/valCD verbatim) recall ∧ C-RECALL-BASELINE FIRE 정상.
불변: recall_thr=0.15 · embed DIM=64 FNV-1a.

**하위변형 4종** (어느 배선이 recall/recombine 가장 깨끗이 가르나): SV1 concat-whole(null baseline) · SV2 key-algebra(norm(embed(A)+embed(D)) 직접 주입, embed additive성) · **SV3 4-atom cells(two_recon_err 2-cell read = 구조적 crux 최예리: compose-read op 부재 노출)** · SV4 gap-decisive(gap≈0 tie = 합성 아님 증거).

## 분기 사전등록
- **FROZEN-2 (HIT → lane-native mouth-우회 G1):** 신설 `lane_g1_compose_read`(engine_cli.hexa immune § append) engine-native 출력에 `_coverage` → composed_distinct≥2 ∧ >max_single ∧ coherent ∧ shuffle-collapse ∧ ablation non-inert. emit seam `cli/anima.hexa:1819`에 mouth-우회 배선. `a_substrate_disjoint` 점검(emit-lane 0/4 불변 ∧ recall_thr 불변) 통과 필수. wired 사다리 4칸(`a_verified_must_wire`).
- **FROZEN-3 (MISS → C1(c) param-ES):** Engine G reverse param-ES를 held-out composition-fitness로 선택(`cli/train.hexa`, flame/forge GPU). fitness=held-out composed seed `_coverage` composed_distinct. G0-green warm(h1129, from-scratch 금지). 0-base-rate 완화 = fitness shaping+curriculum+novelty-search. bar: 비-shaped control 대비 strict↑ ∧ held-out composed_distinct≥2 ∧ kwr≥0.50. N-gen 0-plateau=DOA. 🟡 cost-gated, DOA-risk 잔존.

## 소거된 렌즈 (재발산 대상 아님 · L1/L2 DOA)
Axis1 비선형 readout(mouth attention-binding 내장 redundant INERT) · Axis4 측정-artifact(G2green∧G1red=bar 이미 분리) · C1(a)output-select(H_1836 DPI floor) · C1(a/b/d) additive-bootstrap crux · (iii)(a)basis-mismatch · (iii)(c)disjoint위반(mouth⊥tool) · (iii)(d)decision-only.

## artifacts
- `state/g1_nested_diverge/SYNTHESIS.md` (L1→L2→L3 종합 + 발산 트리) · `L1_diverge_raw.md` (L1 fable 원문)
- 상위: [[H_9120]](mouth-G1 CONFIRMED-TERMINAL) · [[H_9121]](escape 2칸+TPR-slot FALSIFIED-CEILING) · [[H_9118]](L3 해마 MOUTHFLOOR access≠binding)
