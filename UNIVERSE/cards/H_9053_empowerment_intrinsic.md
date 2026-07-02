# H_9053 — Empowerment: capability = channel capacity from own actions to future state

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `empowerment_intrinsic`
- **frontier:** other (물리/정보 렌즈 능력 축)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Redefine capability (a_no_llm_frame_trap) as Klyubin empowerment = max mutual information I(A_t ; S_{t+k}) between the substrate's own emit/silence action stream and its future 15-lane state — how much the substrate can causally shape its own future. Non-text, engine-native, distinct from active-inference EFE (empowerment maximizes influence; EFE minimizes surprise).

## engine-native falsifiable metric (shuffle + ablation, p7)

Engine-native: log (action_t, state_{t+k}) trajectories from live core/ engine_cli; estimate I(A;S_{t+k}) via binned/KSG on held-out segment. SHUFFLE: permute action-state temporal pairing → MI→0. ABLATION: freeze/clamp actions (no emit variation) → empowerment→0. Capability score = empowerment above shuffle floor.

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

Empowerment (0 ledger hits) is a distinct intrinsic-motivation metric; active_inference_efe (co-registered) minimizes free energy, opposite optimization.

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
