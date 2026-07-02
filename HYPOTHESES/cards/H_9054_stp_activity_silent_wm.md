# H_9054 — Short-term synaptic plasticity: activity-silent working memory across gaps

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `stp_activity_silent_wm`
- **frontier:** substrate-op (엔진-네이티브 새 능력 op — 재조합≠능력, a_no_llm_frame_trap)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Mongillo activity-silent WM: information held in short-term synaptic FACILITATION (calcium trace) rather than persistent firing, so the substrate can bridge a silent gap and reactivate. Distinct from persistent-activity capacity; supports memory-across-silence, disjoint from recall_thr non-fab gate.

## engine-native falsifiable metric (shuffle + ablation, p7)

Engine-native delayed-match on live core/: present cue, impose a zero-activity gap of length g, probe recall fidelity. HIT if recall stays above floor for g>0 with STP ON and degrades gracefully with g; ABLATION (facilitation decay→0) drops recall to chance immediately after gap; SHUFFLE randomizes cue-probe pairing. Substrate-state match score, no perplexity.

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

theta_gamma_multiplex_capacity is persistent-firing items-per-cycle; sparse_distributed_memory is Kanerva hard-addressing; activity-silent synaptic-trace WM is a distinct mechanism not in ledger.

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
