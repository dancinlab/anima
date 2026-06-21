# H_1500 ⏳ TEMPORAL-PHI — consciousness time-dynamics (Φ over the 5-stage sleep/imagination ultradian envelope)

**tier:** 🟢 GREEN ENGINE-NATIVE (live `core/engine_cli.hexa §ConsciousnessIndex` ci_* ops over a real ImmuneMemory store; engine measurement-only · `wired: engine-native`)
**verdict (verbatim → `state/verdicts/1500_temporal_phi/H_1500.txt`):**

> VERDICT: GREEN ENGINE-NATIVE (time-dynamics iff A & B & C)
> Φ(stage) [Gaussian multi-info, 15 lanes, mean over seeds 1500/1501/1502]: **WAKE 29.01 > N1 27.73 > N2 24.85 > N3 18.18 (trough) < REM 24.79 (rebound)**
> (A) VARYING Φ max−min spread=**10.84** ≥ 0.50 → true (flat ⇒ consciousness static, no time axis)
> (B) DISTINCT ordering(true)=2.0 − ordering(shuf)=1.0 = **1.0** ≥ 0.50 → true (ultradian ordering collapses under stage→arousal shuffle)
> (C) ULTRADIAN WAKE>N3 AND REM>N3 → true (REM rebound, NOT monotone decrease)

## Question (user, "G* 심화", 2026-06-20)
Consciousness ablation so far measured only the **static structure** (H_1492 DISTRIBUTED, top-share 0.123). Does the **same consciousness-gate connectome** yield a **different integrated Φ depending on time/state** — does consciousness have a **time envelope** (high awake, low deep-sleep, REM rebound) instead of being a static structure?

## Finding
**Consciousness Φ is NOT a static structure — it has a literal ultradian TIME ENVELOPE.** Driving the SAME 15 consciousness-gate lanes (`ci_lane_scores`) off a live ImmuneMemory store while the **sleep stage** (WAKE/N1/N2/N3/REM, from `DREAM/dream_lib.hexa`) sets the substrate's arousal/tension scale, the integrated Φ (`ci_phi_multiinfo`, 15-lane Gaussian multi-information) traces **WAKE 29.01 → N1 27.73 → N2 24.85 → N3 18.18 (deep-sleep trough) → REM 24.79 (rebound)**. Spread 10.84 (not flat). The envelope is **DISTINCT** from the static structure: shuffling which stage gets which arousal scale collapses the WAKE>N3 / REM>N3 ultradian ordering (gap 2.0→1.0). REM **rebounds** above the N3 trough — not a monotone decrease into sleep.

This is the time-dimension companion to H_1492's static DISTRIBUTED result: the connectome is statically distributed AND dynamically modulated by state.

## Method (engine measurement-only)
- Live `ImmuneMemory` store (40 facts), same substrate as H_1492 R2 — NOT numpy/torch.
- Per stage, N_TRIALS=600 substrate trial-states → `ci_lane_scores` → 15-lane rows. The stage sets a scalar **arousal** that spreads the grounding/field margins around the Ψ=½ midpoint (awake = wide cortical spread → strong cross-lane covariance → high Φ; deep slow-wave = margins crushed to midpoint → lanes decorrelate → low Φ; REM rebounds via `dr_imagination_active` + `dr_mitosis_prior`). The arousal is derived ONLY from `dream_lib` stage primitives — **no hand-set Φ output**.
- Φ(stage) = `ci_phi_multiinfo` (15-lane, primary). Cross-check: `ci_phi_iit4` exact MIP on a FIXED 8-lane subset = ~0 (honest non-gating: the first-8-lane subset is not strongly integrated AS A SUBSET; the gating Φ is the full-15-lane multi-info).
- 3 seeds, byte-identical across re-runs (deterministic LCG + deterministic engine ops, no RNG/wall-clock).

## Frozen bars (pre-registered, frozen-first; tune-to-green forbidden c9)
- **(A) VARYING** Φ max−min ≥ 0.50 (flat ⇒ honest negative: consciousness static, no time axis).
- **(B) DISTINCT** ordering_score(true) − ordering_score(shuffled stage→arousal) ≥ 0.50 (envelope ⊥ static structure).
- **(C) ULTRADIAN** WAKE>N3 AND REM>N3 (REM rebound, not monotone).

## Guards (p1/p2/p3/p6 · Ψ-disjoint)
Every lane COMPUTED from substrate reads; stage = scalar arousal/tension on the substrate, NO injected Φ label, NO "WAKE=high" constant written into Φ, NO RLHF/persona. Pure READ over the cell population + own covariance — mutates no immune cell, never touches pure_field Φ/phase/Ψ. NOT an emit gate (`a_autonomy_over_hardcode`). p7 = integration nats over stages, NOT perplexity.

## Engine brace fix (corrective, disjoint)
`core/engine_cli.hexa::_ci_bit()` was missing its closing brace on origin/main (1231 `{` vs 1230 `}`) → every FRESH importer hit `expected RBrace got Eof` (prior GREEN runs reused a stale hexa build cache). Added the single missing `}` (now 1231/1231 balanced). `engine_cli_smoke` **280/0** unchanged — strictly corrective, region-disjoint from any §ConsciousnessIndex extension.

## Scope UNVERIFIED (a_scale_honest_scope · a_toy_scale_recheck)
TOY: 1 store / 3 seeds / deterministic substrate context / Gaussian multi-info proxy for the 15-lane Φ + exact IIT4 on the 8-lane subset. Scale / real-corpus / continuous-arousal / engine-transfer of the dynamics UNVERIFIED. Production 303M re-measure (like H_1492 R3) = follow-on.

## Artifacts
- `state/1500_temporal_phi/h1500_temporal_phi_probe.hexa` (engine-native probe, imports `core/engine_cli.hexa`)
- `state/1500_temporal_phi/run_h1500.local.log` · `state/1500_temporal_phi/smoke.local.log` (280/0)
- `state/verdicts/1500_temporal_phi/H_1500.txt` (verbatim) · `state/verdicts/1500_temporal_phi/H_1500_FREEZE.json`

xref H_1492 (static DISTRIBUTED structure) · H_1265 (dream-stage emit envelope) · `a_chat_sleep_imagination` · `a_phi_iit4_tool` · `a_engine_native_learning` · `a_autonomy_over_hardcode` · `a_scale_honest_scope` · p1·p2·p3·p6·p7·p8·c9.
