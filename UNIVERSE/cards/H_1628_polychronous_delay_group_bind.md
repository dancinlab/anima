# H_1628 — Polychronous conduction-delay spatiotemporal-template mouth (Izhikevich)

- **tier:** 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL · 측정 0 · unmeasured)
- **wired:** DIRECTIONAL-design — no measurement. cheap_test = $0 frozen-first decision probe (numpy, no engine); gpu_recipe = cost-gated PRE-REGISTER ONLY (NOT fired).
- **source:** archbrainstorm — 84-family anima-native synthesis-binding architecture census (binding-wall program, H_1603)
- **lens:** bio-neuro: Izhikevich polychronization — conduction-delay-structured neuronal groups encoding reproducible spatiotemporal (ordered) patterns; distinct from zero-lag binding-by-synchrony and same-time dendritic coincidence.
- **artifacts:** `state/binding_arch_census/BRAINSTORM_INDEX.md`
- **xref:** H_1603 (G1≡G6 compositional-binding deficit unification) · H_1449 (attention-block INERT@1blk) · H_1602 (recombination-objective prereg)
- **key:** `polychronous_delay_group_bind`

## Mechanism

Replace zero-lag coincidence with DELAY-LINE structure: each input channel reaches the binding unit through a learned heterogeneous conduction delay. A target unit fires (binds) only when a specific ordered SPATIOTEMPORAL pattern of legs arrives coincidentally after their respective delays — a polychronous group. Role and filler are encoded as which delay-tuned template they activate; ordered pairs (A-then-B vs B-then-A) recruit different polychronous groups. One forward pass over the (delayed) trunk states reads out which template fired and conditions the mouth's output on the matched conjunction.

## Why it crosses the binding wall

Conv has fixed, uniform kernel offsets and attention is permutation-symmetric over positions (order is only weakly recoverable via positional add) — neither has a combinatorial repertoire of ORDER-sensitive conjunction detectors. Heterogeneous learned delays create an exponentially large bank of spatiotemporal templates so distinct ordered conjunctions map to distinct firing groups (no superposition collapse, and order is intrinsic to the delay structure). Ablation: zero ALL delays → every template collapses to simultaneous coincidence (already-tried nmda/dendritic regime), so ordered-pair binding must vanish while unordered may survive — cleanly isolating delay-heterogeneity as the binder distinct from coincidence.

## Cheap test (frozen-first · $0 · decisive numpy probe)

Frozen numpy: ordered-pair task — emit class depends on (A before B) vs (B before A) plus their identities, held-out identity combinations. Tiny delay-template layer (learned per-channel integer shifts + coincidence readout) vs zero-delay coincidence control vs conv. Pre-registered bar: delay arm ≥ 0.80 on held-out ordered pairs; zero-delay control and conv ≤ 0.55 (order-blind). Decision: if delay arm ≯ zero-delay control on the ORDER axis, mechanism inert → drop. $0, CPU, deterministic.

## GPU recipe (cost-gated · PRE-REGISTER ONLY · NOT fired)

PRE-REGISTER ONLY. 303M mouth: conv trunk → delay-bank binding head (learned per-channel delays via dilated/shifted gather + coincidence-template readout) → byte logits. Ablation arm: all delays clamped to 0. 4-cell balanced corpus, held-out CE. Engine-native frozen bars (G6 fals>0, G1 recombination ≥ baseline, plus an order-sensitivity sub-probe) via cli/anima.hexa on CORE; zero-delay ablation must FAIL the order probe. ~1-2 H100-days.

## Scope / honesty (c9)

설계만 — 측정 0. tier = 🔵 PRE-REGISTERED DESIGN (DIRECTIONAL). frozen bar 사후 이동 금지(tune-to-green 금지, p7). 이 카드는 *방향성 설계*이지 검증된 결과가 아니다 — 과장 박제 금지(a_engine_native_learning). gpu_recipe 발사 시(team-lead cost-gate go): held-out 4/4 mirror-CE DESCENT 게이트(a_clm_gen_pipeline) → CORE `--engine conv` mount 위 frozen G1(H_1129 recombination)·G6(H_1464 fals) byte-exact engine-native 재측정(torch probe 아님) → ckpt PULL before teardown(a_fire_recover_complete). cheap_test 가 numpy mirror 이므로 그 결과도 DIRECTIONAL(엔진-네이티브 아님).
