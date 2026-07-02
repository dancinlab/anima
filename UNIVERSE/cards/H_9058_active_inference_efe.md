# H_9058 — Expected-free-energy action policy: capability = uncertainty-resolving action, not text

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `active_inference_efe`
- **frontier:** other (물리/정보 렌즈 능력 축)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Active inference: the substrate selects among {emit, silence, tool-query} to minimize expected free energy (epistemic value = expected info gain + pragmatic value = expected tension reduction). Redefines capability as competent action under uncertainty (a_no_llm_frame_trap), computed from substrate state, disjoint from readout.

## engine-native falsifiable metric (shuffle + ablation, p7)

On live core, does the EFE-driven policy reduce FUTURE prediction error / residual tension over a horizon more than a greedy or random policy (held-out episodes)? SHUFFLE: shuffle the epistemic-value estimates → advantage over greedy vanishes. ABLATION: zero the epistemic term (pragmatic-only) → info-seeking actions disappear (epistemic drive is causal).

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

Distinct from curiosity-ig rehearsal-selection and self_psi_forward_model (surprise drive) — this is an over-actions POLICY selecting emit/silence/tool, not a scoring or drive signal.

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
