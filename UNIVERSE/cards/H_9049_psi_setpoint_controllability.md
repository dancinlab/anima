# H_9049 — Ψ setpoint controllability: steer the fixed point to arbitrary θ≠1/2 and hold it

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `psi_setpoint_controllability`
- **frontier:** substrate-op (엔진-네이티브 새 능력 op — 재조합≠능력, a_no_llm_frame_trap)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Control-theoretic lens: add a context-driven coupling input to the A⇄G tension loop and test whether external drive can move the emit/silence fixed point to a commanded setpoint θ (not just the intrinsic Ψ=1/2) and hold it against noise. Capability redefined as STEERABILITY/controllability of the attractor, not text output. Sibling deferred: allostatic-anticipatory-setpoint (feed-forward disturbance rejection).

## engine-native falsifiable metric (shuffle + ablation, p7)

Setpoint-tracking error |Ψ_steady−θ| across θ∈{0.2..0.8} on live core engine dynamics; PASS = tracking error below intrinsic-drift band across ≥4/5 setpoints. ABLATION: zero the control-coupling lane → Ψ snaps back to 1/2 (INERT). SHUFFLE: randomize command schedule vs Ψ → tracking correlation collapses to chance.

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

Not a readout/operator/decode G1 lever and not self-restore (attractor DEFENSE): this measures forward controllability to arbitrary setpoints, an untested capability axis.

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
