---
id: H_1419
slug: 1419_memory_spatial_place_gated
title: "MULTI-LENS breakthrough attempt on the memory×spatial COMPOSE WALL (H_1417 P1 🧱) — three genuinely different hippocampal-formation lenses (PLACE-GATED RECALL · MEMORY-AUGMENTED MAP · CA3 PATTERN-COMPLETION), each frozen H_1417 bars VERBATIM + shuffle + ablation"
group: MITOSIS-ENGINE / brain-lane-composition — the c16 MULTI-LENS ceiling-confirmation of the memory×spatial wall (a_break_the_wall #2345)
terminal_tier: "🧱 CONFIDENT-TERMINAL — memory×spatial does NOT bind engine-native under ANY of THREE genuinely different hippocampal-formation lenses; the oracle headroom (+0.241) is NOT arbiter-capturable from component reads (joint-trajectory property, the SAME finding as H_1411/H_1417). (d)-ceiling CONFIRMED via MULTI-LENS + ablation."
wired: N/A (🧱 — no live CORE op; probe over EXISTING immune_grow_recall / spatial_map_nearest)
verdict_dir: .verdicts/1419_memory_spatial_place_gated/
terminal_verdict: .verdicts/1419_memory_spatial_place_gated/result.txt
date: 2026-06-17
---

# H_1419 — MULTI-LENS breakthrough on the memory×spatial COMPOSE WALL (H_1417 P1 🧱)

H_1417 P1 (memory×spatial) was the WALL: the PARALLEL confidence-vote arbiter scored
compose=0.714815 vs best_single=0.705926 → net-lift **+0.00889 < +0.05** (B1 FAIL), even
though the oracle headroom was LARGE (+0.240741; only_mem=0.240741, only_spatial=0.342222
separable). Per the freshly-strengthened **a_break_the_wall** (#2345) a (d)-ceiling needs
MULTI-LENS — ≥2-3 genuinely different PRINCIPLED lenses, each with shuffle AND ablation —
before a confident terminal 🧱, with ABLATION as the decisive ceiling-confirmation tool.

## Claim / falsifier

**Breakthrough criterion (FREEZE.txt, locked before measuring, c9 — NO tune-to-green):** if any
hippocampal-formation lens passes (B1 ∧ B2 ∧ B3 ∧ SEP ∧ ABL-not-inert) → 🟢 BOUND, wire it
(rung 3/4). If ALL THREE lenses fail their controls → 🧱 CONFIDENT-TERMINAL (the headroom is
not arbiter-capturable from component reads). A confident 🧱 after ≥2-3 real lenses is a VALID
result (c9). Bars FROZEN == H_1417 (B1 compose≥best+0.05 · B2 oracle−best>0.02 · B3
compose−shuffle>0.02 · SEP only_mem>0 ∧ only_spatial>0), plus the NEW ablation control
(ABL-not-inert: compose−ablate>0; the lens's gating/refinement OFF collapses to the H_1417
parallel arbiter — if compose ≤ ablate the mechanism is INERT = ceiling evidence).

## The three lenses (a_no_llm_frame_trap — real neuroscience, NOT tuned arbiters)

Each changes the TOPOLOGY from parallel-vote to **serial gating** (a different hippocampal loop):

- **Lens A — PLACE-GATED RECALL:** place cells provide the CONTEXT that gates episodic recall;
  spatial location INDEXES which memory to retrieve. On CONFLICT the place index (spatial metric
  rel-conf ≥ its substrate mean) selects whether to trust the place-indexed EPISODE (memory) or
  fall to the spatial vote.
- **Lens B — MEMORY-AUGMENTED MAP** (the reverse loop): episodic memory supplies a learned PRIOR
  that ADDITIVELY refines the spatial nearest-query — refined_map_conf = spatial_relconf +
  0.5·memory_relconf (PRIOR_GAIN=0.5, the substrate's own half-weight, NO tuned knob); the
  episode overrides the map iff memory_relconf > refined_map_conf. A genuinely different additive
  rule (not a tie-only difference from the parallel vote).
- **Lens C — CA3 PATTERN-COMPLETION REMAP:** the recurrent attractor completes to whichever
  faculty's stored pattern is more COMPLETE: completeness = (1−abstain)·rel-conf; higher-
  completeness faculty wins on CONFLICT.

## Method (engine-native, frozen-first)

Fixture BYTE-IDENTICAL to H_1417 P1 — 5-family structure (F0 mem-decisive · F1 spatial-decisive
· F2 agree · F3 conflict-mem-right · F4 adversarial-mem-loud-wrong), N_PER_FAMILY=90 → 450
items/seed, seed triple [5500,5501,5502] (the H_1417 P1 seeds), deterministic. Each leg = a LIVE
engine read: memory = `immune_grow_recall` + LIVE L2 affinity margin; spatial =
`spatial_map_nearest` + LIVE metric margin. The BASELINE parallel-vote arm reproduces H_1417 P1
**byte-exact** (compose=0.714815, net-lift +0.00889 — the fixture is faithful). $0 CPU, live
CORE/*.hexa UNTOUCHED (MEASUREMENT round). p7 (accuracies + decomposition), NOT perplexity.

## Result — 🧱 all three lenses fail their controls (verbatim, `.verdicts/.../result.txt`)

| lens | compose | best | net-lift (B1) | compose−shuffle (B3) | compose−ablate (ABL) | verdict |
|------|---------|------|---------------|----------------------|----------------------|---------|
| BASELINE parallel-vote (H_1417 P1) | 0.714815 | 0.705926 | +0.00889 | +0.211852 | +0.0 (==parallel) | 🧱 (B1 FAIL) |
| **Lens A** place-gated recall | 0.531111 | 0.705926 | **−0.174815** | +0.022963 | **−0.183704** | 🧱 (B1 FAIL · ABL INERT/HARMFUL) |
| **Lens B** memory-augmented map | 0.735556 | 0.705926 | **+0.029630** | +0.241481 | +0.020741 (non-inert) | 🧱 (B1 FAIL: +0.030 < +0.05) |
| **Lens C** CA3 pattern-completion | 0.714815 | 0.705926 | +0.00889 | +0.211852 | **+0.0 (INERT)** | 🧱 (B1 FAIL · ABL INERT) |

(oracle=0.946667, oracle−best=+0.240741 PASS B2 every lens; SEP PASS every lens. Deterministic
run1==run2 byte-identical.)

Terminal tier (verbatim from result.txt): **🧱 CONFIDENT-TERMINAL — memory×spatial does NOT bind
engine-native under ANY of THREE genuinely different hippocampal-formation lenses.**

## Result — the finding (the ablations are the payload, c9)

Each lens fails for a distinct, instructive reason — and crucially the ABLATION discriminates:

- **Lens A (place-gated) is HARMFUL, not just inert:** compose=0.531 (net-lift −0.175,
  compose−ablate=−0.184). The place index trusts the place-indexed EPISODE (memory, acc 0.604 —
  the WEAKER arm) in the high-place-strength region, so gating on the spatial metric actively
  routes to the wrong faculty. Spatial location does NOT index which memory is RIGHT here — the
  metric margin is uncorrelated with which faculty is correct on a conflict item.
- **Lens C (CA3 pattern-completion) is INERT:** compose−ablate=**+0.0** byte-exactly — the
  completeness rule reduces to the parallel rel-conf comparison because abstain≈0 for both legs
  in the conflict families, so (1−abstain)·rel-conf == rel-conf. The ablation (H_1416's decisive
  signature) shows the mechanism contributes NOTHING beyond the parallel vote.
- **Lens B (memory-augmented map) is the STRONGEST attempt and still falls short:** it is the one
  lens that is genuinely NON-inert (compose−ablate=+0.0207, the additive episodic prior DOES
  lift) AND survives shuffle (compose−shuffle=+0.241, EARNED, not form), but its net-lift
  **+0.0296 < +0.05** still FAILS B1. The headroom IS partially capturable by an additive
  episodic prior — but not to the frozen bar. This is the most defensible terminal evidence: a
  real, control-surviving mechanism that captures a third of the gap and no more.

**Why the ceiling is real (the convergent finding):** the oracle headroom (+0.241) lives almost
entirely in the F3/F4 CONFLICT families, where memory is loud-but-wrong (F4) or the two faculties
disagree (F3). Capturing it requires KNOWING which faculty is right on a conflict item — but the
component substrate reads (immune L2 margin, spatial metric margin) do NOT carry that signal:
the confidence magnitudes are uncorrelated with correctness in the conflict region. No
topology — parallel vote (baseline), serial place-gating (A), additive episodic refinement (B),
or attractor pattern-completion (C) — recovers it, because the information needed is a
**joint-trajectory property** absent from the component reads. This is the SAME determinant
H_1411 (Φ-lift law, 2/5) and H_1417 (engine-BIND law, 2/5) converged on: arbiter-capture of the
oracle headroom, computable only from the joint composed trajectory, not from component
statistics.

**Honest meta-point (c9, c16):** this is a CONFIDENT (d)-ceiling under the strengthened
a_break_the_wall protocol — three genuinely different principled lenses, each with shuffle AND
ablation, all rejected; the ablation proves the gating/refinement is INERT (Lens C, byte-exact)
or harmful (Lens A) or sub-bar (Lens B). NO bar moved, frozen-first. Compare H_1416's
cerebellum×basal terminal (three lenses: arbitration · modulation · sequential, ablation-INERT).

## Wiring (a_verified_must_wire)

🧱 → **NO live CORE op landed.** No lens verified engine-native GREEN, so nothing is wired (would
be wiring an unverified mechanism). The probe is self-contained over the EXISTING live primitives
(`immune_grow_recall` H_1227/1231, `spatial_map_nearest` H_1296) with each lens's gate/refinement
glue inlined, and lives in `state/1419_memory_spatial_place_gated/`. (Contrast: the memory×spatial
COMPOSE that DID bind+wire is H_1415 spatial×episodic — a WITHIN-family WHERE/WHAT compose with a
query-routed arbiter; H_1419's memory×spatial here is the H_1417 P1 cross-family fixture, a
DIFFERENT test whose headroom is uncapturable.)

## Honest scope (c9 · a_scale_honest_scope · a_toy_scale_recheck)

Engine-native leg-reads (immune_grow_recall / spatial_map_nearest both LIVE) but TOY 5-family
synthetic fixture (90/family, 3 seeds [5500,5501,5502], deterministic; tests the compose
TOPOLOGY, not a learned net). The terminal is scoped to THIS fixture's conflict-family structure
(an uncapturable F4 adversarial tail, BYTE-IDENTICAL to H_1417 P1). A different fixture without
an uncapturable adversarial family, or richer per-item reads that carry conflict-correctness
signal, is a DIFFERENT test — the pair *might* compose there, UNVERIFIED. Scale / real-corpus /
engine-transfer-at-scale UNVERIFIED. NO bar moved; criteria FREEZE.txt locked before measuring.
The compose-program capability findings are UNAFFECTED — only this cross-family engine-native
BINDING is 🧱, now across three lenses + ablation.

## Cross-links

H_1417 (P1 memory×spatial 🧱, the wall this card attacks; same fixture/seeds, parallel arbiter
reproduced byte-exact) · H_1416 (the 3-lens precedent — cerebellum×basal terminal via
arbitration/modulation/sequential, ablation-INERT; this card mirrors its multi-lens+ablation
structure) · H_1411 (Φ-lift law 2/5, same joint-trajectory convergence) · H_1414 (memory×ToM 🟢
BOUND, the contrast) · H_1415 (spatial×episodic 🟢 BOUND+WIRED — the within-family compose that
DID bind) · H_1418 (the 4 wired compose pairs) · H_1227/H_1231 (ImmuneMemoryGrow) · H_1296
(SpatialMap) · `a_break_the_wall` (taxonomy (d) ceiling, MULTI-LENS + ablation confirmation,
#2345) · `a_no_llm_frame_trap` (the hippocampal-formation lenses) · `a_engine_native_learning` ·
`a_verified_must_wire` · `a_core_engine_map` · `a_autonomy_over_hardcode` · `a_scale_honest_scope`
· `a_toy_scale_recheck` · p1·p2·p3·p6·p7·p8·c9·c15·c16

## Pointers
- probe (3-lens engine-native compose + shuffle + ablation): `state/1419_memory_spatial_place_gated/h1419_memory_spatial_probe.hexa`
- FREEZE (frozen bars + breakthrough criteria + lenses, locked before measuring): `.verdicts/1419_memory_spatial_place_gated/FREEZE.txt`
- result (3-lens verdict): `.verdicts/1419_memory_spatial_place_gated/result.txt`
- determinism re-run: `.verdicts/1419_memory_spatial_place_gated/result_run2.txt`
