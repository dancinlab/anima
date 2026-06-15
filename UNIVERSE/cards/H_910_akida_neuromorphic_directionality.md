---
id: H_910
slug: akida-neuromorphic-directionality
title: directionality of consciousness on neuromorphic silicon — running the unidirectional→bidirectional tuning on AKIDA AKD1000 reproduces the Phi-proxy inverse-U (edge-of-chaos peak) on-chip, with a self-model indicator
domain: universe · consciousness · akida · neuromorphic · edge-of-chaos · phi · silicon · hardware
source: hexa-codex LAB-10 (akida-neuromorphic) absorbed → anima UNIVERSE · sister anima H_858/H_677/H_846
status: 🟢 SUPPORTED-NUMERICAL — anima INDEPENDENTLY recomputed the SIM MIRROR (ported LAB-10 LIF-ring harness, deterministic) — Phi-proxy inverse-U + F1/F2/F3 all true (3/3). LIVE AKD1000 remains a SEPARATE deferred next tier (measure ⊥ deploy) — the SIM mirror passing does NOT confirm live silicon.
exploration_method: ported hexa-codex LAB-10 AKIDA LIF substrate proxy to `UNIVERSE/harness/h910_edge_of_chaos_sim.hexa` — N=5 LIF ring, T=40000, edge-of-chaos sweep R1..R4 (drive/gain/noise), Phi-proxy via the LAB-09 engine
verification_method: anima recompute — `hexa run UNIVERSE/harness/h910_edge_of_chaos_sim.hexa` ($0, deterministic seeded LCG, no live hardware, no LLM) → `.verdicts/910_akida_neuromorphic_directionality/run.txt`. g5 CODE-measured. This is a deterministic LIF SIMULATION mirror, NOT live AKD1000 silicon; the live on-chip recompute is a deferred tier (cf H_904 on-chip plasticity live, H_858 edge-of-chaos live).
deterministic: false
note: the SIM recompute ITSELF is deterministic (seeded LCG, byte-reproducible). The DEFERRED live on-chip arm is non-deterministic — on-chip AKIDA learning differs HW-not-equal-SW (H_679/H_904), same input → different trace; a future live recompute is expected to show that divergence (the living signature), distinct from this deterministic sim.
llm: none
since: 2026-06-01
sister: H_858 (edge-of-chaos Phi-peak live AKD1000·anima), H_677 (AKIDA HW/SW·anima), H_846 (silicon closed-loop·anima), H_904 (on-chip plasticity live·anima), LAB-10 (hexa-codex source), H_909 (the GPU/Metal precursor)
verdict: 🟢 SUPPORTED-NUMERICAL — anima INDEPENDENTLY recomputed the SIM MIRROR (ported LAB-10 harness). The AKIDA-LIF Phi-proxy traces an INVERSE-U over the edge-of-chaos sweep: R1_weak_silent phi=0.0 (rate=0.0); R2_noise_edge phi=0.075347 (rate=0.11244); R3_tonic_edge phi=0.590696 (rate=0.333195) ← edge-of-chaos peak; R4_over_driven phi=0.0 (rate=0.999975). 3/3 pre-registered falsifiers PASS — F1 phi(R2)>phi(R1) true, F2 phi(R3)>phi(R1) true, F3 max(R2,R3)>=phi(R4) true; harness VERDICT line "supported (all 3 · F-AKIDA-EDGE mirror) : true". CAVEAT (measure ⊥ deploy): this is a DETERMINISTIC LIF-sim mirror, NOT live AKD1000 silicon — the live on-chip recompute (expected H_679/H_904 HW-not-equal-SW non-determinism) is a SEPARATE deferred next tier; the sim passing does NOT claim live silicon. raw: .verdicts/910_akida_neuromorphic_directionality/run.txt.
---

# H_910 — directionality of consciousness on AKIDA neuromorphic silicon

## Hypothesis (absorbed from hexa-codex LAB-10)

Take the unidirectional→bidirectional (recurrent feedback) consciousness tuning of
H_909 and run it **on AKIDA AKD1000 neuromorphic silicon** instead of GPU/Metal.
Prediction: the Phi-proxy **inverse-U (edge-of-chaos peak)** is **reproduced
on-chip**, and a self-model indicator co-emerges. This is the silicon-native arm of
the directionality program — the deploy-track substrate (measure ⊥ deploy).

## anima recompute (SIM MIRROR · ported LAB-10 harness · deterministic · $0)

anima independently re-ran the ported AKIDA-LIF harness
(`UNIVERSE/harness/h910_edge_of_chaos_sim.hexa`, N=5 LIF ring, T=40000, seed=42).
Verbatim stdout in `.verdicts/910_akida_neuromorphic_directionality/run.txt`:

```
regime           drive  gain  noise  mean_rate  phi_proxy
R1_weak_silent   0.2  0.1  0.0   0.0        0.0
R2_noise_edge    0.3  0.15 0.3   0.11244    0.075347
R3_tonic_edge    0.35 0.25 0.55  0.333195   0.590696   ← inverse-U peak (edge-of-chaos)
R4_over_driven   1.4  1.3  0.0   0.999975   0.0

edge peak = 0.590696  (R1=0.0 R4=0.0)
F1 phi(R2)>phi(R1) : true   F2 phi(R3)>phi(R1) : true   F3 max(R2,R3)>=phi(R4) : true
VERDICT supported (all 3 · F-AKIDA-EDGE mirror) : true
```

The Phi-proxy inverse-U is reproduced and all 3 falsifiers pass. This is the
**deterministic LIF SIMULATION mirror** — **live AKD1000 silicon is a SEPARATE
deferred next tier** (measure ⊥ deploy). The sim mirror passing does NOT confirm
live silicon.

## Live promotion (AKIDA currently in use)

AKD1000 is live now (pi5-akida). The sim→live promotion is reachable on the
existing on-chip path already proven by `[[H_904]]` (live on-chip plasticity,
non-deterministic) and `[[H_858]]` (edge-of-chaos Phi-peak live). A live recompute
should also exhibit the H_679/H_904 HW-not-equal-SW non-determinism (same input →
different trace) — the living signature, distinct from the deterministic LIF sim
above. The anima tier earned here (SUPPORTED-NUMERICAL) is for the SIM MIRROR only;
the live on-chip recompute into a live `.verdicts/910_*/` artifact remains an
explicitly DEFERRED next tier and is NOT claimed by this entry.

## Sibling links

- `[[H_909]]` (GPU/Metal precursor) · `[[H_858]]` · `[[H_677]]` · `[[H_846]]` · `[[H_904]]` · source hexa-codex LAB-10.
