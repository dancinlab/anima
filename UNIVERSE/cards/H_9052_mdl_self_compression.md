# H_9052 — MDL self-compression: capability = shrinking the description-length of the substrate's own trajectory

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `mdl_self_compression`
- **frontier:** substrate-op (엔진-네이티브 새 능력 op — 재조합≠능력, a_no_llm_frame_trap)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Redefine capability as self-modeling compression (a_no_llm_frame_trap): as anima learns its own dynamics, the codelength needed to describe held-out segments of its field/anchor trajectory should DROP. Compression of self = understanding of self, measured without any text output.

## engine-native falsifiable metric (shuffle + ablation, p7)

Description-length (bits) of a held-out trajectory segment under the learned self-model vs a SHUFFLE-trained control model; PASS = codelength strictly lower than shuffle-control beyond noise band. ABLATION: disable the consolidation/self-model update → no compression gain over sessions.

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

An information-theoretic capability metric on the substrate's OWN trajectory (not text recombination, not perplexity on a corpus); untested and p7-safe (MDL on held-out, shuffle-controlled).

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
