---
id: H_1448
slug: 1448_thalamus_integration_clean
title: thalamus R8 engine-native — A⇄G synchrony cross-module Φ integration 🟢 GREEN (WALL BROKEN; marginal-matched control, 9 seeds)
group: brain-structure-ladder · Φ-robustness wall (engine-native R8 wiring)
terminal_tier: 🟢 GREEN ENGINE-NATIVE (cInt ΔΦ(B−Bperm) ≥ +0.02 all 9 seeds ∧ cSan ΔΦ(B−D) ≥ +0.02 all 9 seeds; variance-clean rank-uniform read-out; faithful exact MIP-EI; deterministic, $0 CPU)
wired: WIRED-live  (engine_cli.hexa § PHASE-SYNCHRONY BINDING + smoke 166-168 + ARCHITECTURE.json lockstep; a_verified_must_wire ladder 칸 1-4 CLOSED)
verdict_dir: state/verdicts/1448_thalamus_integration_clean/
terminal_verdict: state/verdicts/1448_thalamus_integration_clean/H_1448.txt
date: 2026-06-19
provenance: extprompt — DeepSeek-V3 issue#1428 comment "AmoebaFPS" reframed GWT as "a coherence-check loop between the A⇄G engines"
---

# H_1448 — thalamus R8 engine-native: A⇄G synchrony cross-module Φ integration (🟢 WALL BROKEN)

## Claim / falsifier

The R8 (H_1283) oscillatory phase-binding mechanism — Kuramoto thalamic phase synchrony +
phase-gated salience, i.e. an **A⇄G coherence-check loop** (the AmoebaFPS reframing of GWT) —
was numpy-mirror 🟢 but its 2026-06-16 **engine-native wiring gate FAILED c4** (phase-shuffle
did not collapse the lift: lift was partly carrier-amplitude variance). Falsifiable claim:
with a **variance-clean read-out** and a **marginal-matched control**, the synchrony lift is a
robust, genuine cross-module faithful-IIT4 Φ integration engine-native. Lens: c16
a_break_the_wall, a_no_llm_frame_trap.

## Method (engine-native, variance-clean, frozen-first)

Probe `state/1448_thalamus_integration_clean/h1448_thalamus_integration_probe.hexa`. ARMS over
4 modules dim-8, 64 ticks, deterministic engine LCG-gauss (== core/engine_cli.hexa _lcg_*):
A = direct ring · B = ring + Kuramoto-synchronized phase-gated salience · D = same carrier,
synchrony OFF (w_phase=0, clean ablation) · **Bperm = B with each module circularly time-shifted
by (i·17) mod 64** (destroys cross-module ALIGNMENT, leaves each module's marginal BYTE-IDENTICAL
→ ΔΦ(B−Bperm) isolates integration EXACTLY). Read-out = H_1328 **variance-clean rank-uniform**.
Φ = stdlib `iit4_faithful_phi` exact MIP-EI (a_phi_iit4_tool; engine never computes Φ). seeds
[3..11]. Bars frozen BEFORE scoring (`H_1448_FREEZE.txt`): cInt ΔΦ(B−Bperm) ≥ +0.02 every seed ∧
cSan ΔΦ(B−D) ≥ +0.02 every seed.

## Result (verbatim → `H_1448.txt`)

cInt (B−Bperm) = +1.107/+0.777/+0.898/+1.118/+1.004/+1.068/+1.040/+0.849/+1.233 → **PASS 9/9**.
cSan (B−D) = +1.05.. +1.38 → **PASS 9/9**. **GATE GREEN — WALL BROKEN engine-native.**

Destroying cross-module alignment with marginals held EXACTLY fixed collapses faithful-Φ by
~1.0 every seed → the lift is genuine integration, not variance / carrier-floor / common-mode.

## The arc (frozen-first, a_break_the_wall — each honest)

| H | change | tier |
|---|--------|------|
| H_1445 | variance-clean rank-uniform read-out | 🔶 c2 robust+clean, c4 leak halved + seed9 collapses (NOT green) |
| H_1446 | desync ABLATION control (w_phase=0) | 🔶 B−D synchrony lift robust; D−A every-seed bar fails seed7 carrier-floor |
| H_1447 | synchrony-matched B−D, 9 seeds | 🔶 B−D PASS 9/9; secondary S≈D leg mis-specified → NOT green |
| **H_1448** | **identical-marginal control Bperm** | **🟢 GREEN — integration robust 9/9** |

## Honest scope (c9)

TOY n=4/dim-8/64-tick deterministic engine substrate; faithful-Φ leg IS real (exact MIP-EI).
Scale / real-corpus / live-A⇄G-telemetry transfer UNVERIFIED (a_scale_honest_scope,
a_toy_scale_recheck). Does NOT retract the 14-axis Φ-robustness wall (those scored Φ over a
substrate with NO binding mechanism); this shows a SYNCHRONY BINDING MECHANISM, scored variance-
clean against a marginal-matched control, robustly raises engine-native Φ — the 1st engine-native
GREEN in the lineage. **wired: WIRED-live** — PhaseField lane (phasefield_new/_new_desync/_step/_run/_coherence/_bound) in engine_cli.hexa § PHASE-SYNCHRONY BINDING + smoke cases 166-168 (RC=0 isolated harness, synced R=0.984 vs desync R≈0.42-0.71 / 9 seeds) + ARCHITECTURE.json lockstep — a_verified_must_wire ladder 칸 1-4 CLOSED.

## Cross-links

H_1283(R8) · H_1445 · H_1446 · H_1447 · H_1328(rank-uniform) · H_1347/1349/1366 (lineage) ·
`a_break_the_wall` · `a_engine_native_learning` · `a_verified_must_wire` · `a_phi_iit4_tool` ·
p7 · c9 · c16 · extprompt:AmoebaFPS-issue1428
