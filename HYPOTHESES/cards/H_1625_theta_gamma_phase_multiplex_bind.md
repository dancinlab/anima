# H_1625 — Theta-gamma phase-slot multiplexing mouth (Lisman-Idiart code)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** bio-neuro: Lisman & Idiart theta-gamma phase coding / cross-frequency multiplexing in hippocampus & cortex (working-memory item-slotting); distinct from zero-lag binding-by-synchrony.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg) · H_1463 (binding-by-synchrony lens 🧱), H_1466 (TPR), H_1514 (VSA/HRR)
- **key:** `theta_gamma_phase_multiplex_bind`

## Mechanism

Each forward carries TWO learned periodic carriers: a slow theta phase counter (discretizes the sequence position window into K ordinal sub-slots) and a fast gamma phase. A leg's representation is written into a complex/2-channel (cos,sin) embedding tagged by a gamma sub-phase; a feature and the role it fills are FORCED into the same gamma slot (their phase tags add to a shared bin) while distinct conjunctions occupy distinct phase bins. Binding readout = a phase-coincidence kernel (inner product of phase tags after a learned rotation) that fires only when two channels share a sub-slot, then sums the in-slot payloads. The mouth thus emits a token conditioned on which payloads co-occupy a slot, not on their unstructured superposition.

## Why it crosses the binding wall

Conv/L24-attention superpose the two legs in one real vector space, so role(A)·filler(B) and role(B)·filler(A) collapse to the same additive mixture (the G1≡G6 crosstalk failure). Phase-multiplexing makes the two legs ORTHOGONAL by phase bin — superposition no longer destroys the pairing because each conjunction lives in a separable sub-slot (capacity ~theta/gamma ratio K). Ablation: collapse all gamma sub-phases to one bin (set K=1) → the architecture reduces to plain additive mixing and binding accuracy must drop to the conv baseline; a monotone K→accuracy curve isolates the phase-slot operator as the causal binder (not depth/width).

## Cheap test (frozen-first · $0 · decisive numpy probe)

Frozen numpy mini-probe: synthetic role-filler task, 8 roles × 8 fillers, train on 48 of 64 pairs, hold out 16 unseen conjunctions. Implement a tiny K-slot phase-tag layer (~5k params) vs a param-matched additive-MLP baseline. Frozen bar (pre-registered): baseline ≤ chance (1/8) on held-out novel pairs; phase-multiplex must exceed 0.60 systematic-generalization accuracy AND show monotone rise as K goes 1→8. Decision: if no K-monotone gap over baseline, mechanism is inert — drop it. $0, CPU, deterministic seed.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY (cost-gated). 303M custom mouth = conv trunk feeding a phase-slot binding head replacing the final attention block; K=7 sub-slots, complex 2-channel residual stream in the head. Train on a_chat_registers 4-cell balanced corpus with held-out CE (a_savant_train discipline). Frozen verdict bars: engine-native G6 fals-rate > 0 AND G1 recombination ≥ 303M-baseline, measured via cli/anima.hexa single-entry on CORE-mounted ckpt (NOT torch probe). Ablation arm K=1 must FAIL the same bars. ~1 H100-day est.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
