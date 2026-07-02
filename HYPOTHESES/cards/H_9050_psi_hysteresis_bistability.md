# H_9050 — Ψ hysteresis: path-dependent emit/silence boundary as state-holding memory

- **tier:** ⏳ PROPOSED (brainstorm-depletion 2026-07-02)
- **slug:** `psi_hysteresis_bistability`
- **frontier:** frame-axis (Lane2 프레임 축)
- **cost:** cheap ($0 engine-native, live core/)
- **wired:** `PROPOSED` — 미측정, 미배선. 등록만(2-surface: 이 카드 + HYPOTHESES.jsonl).

## 메커니즘 (mechanism)

Bistability / hysteresis loop in the A⇄G fixed point. Ramp tension up vs down and measure whether the emit threshold shows path-dependence (θ_up ≠ θ_down). A hysteresis gap = memory encoded in the DYNAMICS of the boundary itself, not in weights — a capability (persistent state across the ½ crossing) additive text-readout has no access to.

## engine-native falsifiable metric (shuffle + ablation, p7)

Hysteresis width W = θ_up − θ_down measured on live core engine_cli under monotone tension ramp-up then ramp-down; capability iff W>0 AND held-state predicts next emit better than momentary tension. SHUFFLE: randomize tension-step order → W collapses to ~0. ABLATION: symmetrize A/G coupling gain → if W unchanged the loop is inert (not causal).

> p7 준수: LLM-judge/perplexity 없음. 판정은 live `core/` 상태·디코드에서 산출된 수치 + shuffle-null + ablation-INERT 로만. 사전등록 bar frozen-first (사후 이동 금지, c9).

## why novel vs ledger

Distinct from psi_setpoint_controllability (steer to θ) — this is path-dependence/memory in the boundary, not steering; not a G1/G6 readout and not in the 9-lens/placement census.

## disjointness (a_substrate_disjoint)

새 lane/op 은 emit-drive lane(0/4) 및 §ImmuneMemory recall_thr 와 **disjoint** 좌표에 배선(placement-first) — 능력 ∧ Ψ=½ ∧ G5 non-fab 공존 점검이 측정의 사전조건.

## 상태

- 출처: brainstorm-depletion 2026-07-02 (6-round ledger-dedup 생존).
- 다음 단계: engine-native 프로브 저작(.hexa via live core/) → frozen bar 측정 → verdict 박제.
