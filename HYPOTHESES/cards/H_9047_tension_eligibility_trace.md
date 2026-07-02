# H_9047 — Eligibility trace over the A⇄G tension trajectory (temporal credit assignment for emit/silence)

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `tension_eligibility_trace`
- **frontier:** substrate-op (엔진-네이티브 새 능력 op — 재조합≠능력, a_no_llm_frame_trap)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Gerstner three-factor plasticity: a decaying eligibility trace tags which prior tick's emit/silence decision is responsible for a current Ψ drift. New op `self` accumulates per-tick tension deltas into a trace vector; a later Ψ surprise gates consolidation onto the responsible tick. Distinct from tension_resolve_depth (H_9042, single-shot A⇄G conflict→Ψ½) — this is multi-tick attribution memory.

## engine-native falsifiable metric (shuffle + ablation, p7)

Engine-native attribution accuracy: inject a Ψ perturbation at tick T, measure whether the trace assigns credit to the correct causal prior tick vs a phase-shuffled-trace control (chance) + ABLATION (zero the trace decay → attribution collapses to uniform). Falsify if trace ≈ shuffle.

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

Temporal credit-assignment across ticks is a new faculty; H_9042 tension_resolve is single-shot resolution, not multi-tick attribution — not in any readout/operator/objective wall.

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
