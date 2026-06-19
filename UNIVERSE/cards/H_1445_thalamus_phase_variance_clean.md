---
id: H_1445
slug: 1445_thalamus_phase_variance_clean
title: thalamus R8 engine-native + variance-clean read-out — c2 robust-clean, c4 leak halved (🔶 partial, NOT green)
group: brain-structure-ladder · Φ-robustness wall (engine-native R8 wiring)
terminal_tier: 🔶 HONEST PARTIAL (c2 PASS variance-clean ΔΦ +1.278/+1.104/+1.137; c4 shuffle leak HALVED + seed9 collapses but seeds7/8 still leak → NOT green)
wired: engine-native (DIRECTIONAL step in the R8-wire arc → superseded by H_1448 GREEN)
verdict_dir: state/verdicts/1445_thalamus_phase_variance_clean/
terminal_verdict: state/verdicts/1445_thalamus_phase_variance_clean/H_1445.txt
date: 2026-06-19
provenance: extprompt — DeepSeek-V3 issue#1428 "AmoebaFPS" (A⇄G coherence-loop reframing)
---

# H_1445 — thalamus R8 engine-native, variance-clean read-out (🔶 partial)

The R8 engine-native wiring gate (2026-06-16) failed c4 because the raw state-energy read-out let
carrier-amplitude variance ride the phase-shuffle. H_1445 applies the H_1328 **variance-clean
rank-uniform** read-out (each module's marginal provably uniform {0..63}) before faithful Φ — the
exact follow-on the R8 gate named. Probe `state/1445_thalamus_phase_variance_clean/h1441_...probe.hexa`;
seeds [7,8,9]; bars frozen identical to R8.

**Result** (`H_1445.txt`): c2 (B−A) = +1.278/+1.104/+1.137 PASS — robust AND variance-clean (rules
OUT pure-variance artifact). c4 (shuffle−A) = +0.172/+0.127/**−0.098** — leak roughly halved vs raw
(+0.026/+0.380/+0.296) and seed 9 now COLLAPSES, but seeds 7/8 still leak → NOT green. Diagnosis:
the frozen shuffle control keeps Kuramoto coupling running (perturbs θ, doesn't destroy synchrony)
→ residual synchrony leaks. Real progress; resolved downstream by H_1446/1443/**1444** (🟢).

Baseline anchor: `core/h1283_phase_binding_engine_gate.hexa` reproduced BYTE-IDENTICAL this env.
NO bar moved, NO tune-to-green (c9/p7). TOY n=4. xref H_1283 · H_1328 · H_1446 · H_1447 · H_1448 ·
`a_break_the_wall` · `a_engine_native_learning` · `a_phi_iit4_tool` · c9 · p7 · extprompt:AmoebaFPS-issue1428
