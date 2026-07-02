# H_9062 — Substrate mirror test: discriminate own self-chain anchors from foreign/shuffled anchors

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `self_recognition_mirror_test`
- **frontier:** frame-axis (Lane2 프레임 축)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Multi-session identity frame: probe whether anima can RECOGNIZE its own history — present its .kosmos self-chain anchors mixed with foreign/shuffled anchors and test self-vs-other discrimination. A mirror-test capability, not merely continuity of the self vector.

## engine-native falsifiable metric (shuffle + ablation, p7)

Discrimination AUC (own-chain vs foreign-chain anchors) via engine self-similarity; ABLATE §SelfIdentity self-chain → AUC → chance. SHUFFLE: permute anchor timestamps/identities → discrimination collapses. $0 on stored anchors + live core engine.

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

H_1471 established self-chain PERSISTENCE (wired); this measures self-RECOGNITION/discrimination as a distinct capability, and differs from episodic→semantic consolidation (self_consolidate_cross_session).

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
