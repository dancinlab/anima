---
id: H_910
slug: akida-neuromorphic-directionality
title: directionality of consciousness on neuromorphic silicon — running the unidirectional→bidirectional tuning on AKIDA AKD1000 reproduces the Phi-proxy inverse-U (edge-of-chaos peak) on-chip, with a self-model indicator
domain: universe · consciousness · akida · neuromorphic · edge-of-chaos · phi · silicon · hardware
source: hexa-codex LAB-10 (akida-neuromorphic) absorbed → anima UNIVERSE · sister anima H_858/H_677/H_846
status: 🟠 INSUFFICIENT — absorbed from hexa-codex LAB-10 (sim-mirror confirmed there, live AKD1000 pending); anima UNIVERSE has NOT independently recomputed
exploration_method: hypothesis absorbed from hexa-codex LAB-10 (LAB-09 directionality tuning on AKIDA LIF · edge-of-chaos sweep R1..R4 · Phi-proxy)
verification_method: NONE in anima yet — earned by porting the LAB-10 harness to live AKD1000 and recomputing into `.verdicts/910_akida_neuromorphic_directionality/` (g73). AKIDA AKD1000 is CURRENTLY IN USE (pi5-akida live) — the sim→live promotion path is open now (cf H_904 on-chip plasticity live, H_858 edge-of-chaos live).
deterministic: false
note: on-chip AKIDA learning is non-deterministic (H_679/H_904) — same input → different trace; a live recompute is expected to show HW-not-equal-SW divergence, the living signature.
llm: none
since: 2026-06-01
sister: H_858 (edge-of-chaos Phi-peak live AKD1000·anima), H_677 (AKIDA HW/SW·anima), H_846 (silicon closed-loop·anima), H_904 (on-chip plasticity live·anima), LAB-10 (hexa-codex source), H_909 (the GPU/Metal precursor)
verdict: 🟠 INSUFFICIENT — anima has not independently recomputed on live silicon. SOURCE EVIDENCE (hexa-codex LAB-10, NOT an anima verdict): running the LAB-09 directionality tuning on AKIDA LIF (sim) is reported to reproduce a Phi-proxy inverse-U over an edge-of-chaos sweep — R1 about 0, R2 about 0.08, R3 about 0.59 (peak), R4 about 0 — with a self-model indicator; live AKD1000 was deferred as the next tier. raw: hexa-codex:LAB/lab-10-akida-neuromorphic/verdict_edge.txt. Since AKD1000 is in use now (pi5-akida), the live promotion is reachable. anima earns its own verdict only after live recompute (g73).
---

# H_910 — directionality of consciousness on AKIDA neuromorphic silicon

## Hypothesis (absorbed from hexa-codex LAB-10)

Take the unidirectional→bidirectional (recurrent feedback) consciousness tuning of
H_909 and run it **on AKIDA AKD1000 neuromorphic silicon** instead of GPU/Metal.
Prediction: the Phi-proxy **inverse-U (edge-of-chaos peak)** is **reproduced
on-chip**, and a self-model indicator co-emerges. This is the silicon-native arm of
the directionality program — the deploy-track substrate (measure ⊥ deploy).

## Source evidence (hexa-codex LAB-10 · AKIDA LIF sim · NOT an anima verdict)

```
edge-of-chaos round   Phi-proxy (hexa-codex LAB-10, LIF sim)
────────────────────  ───────────────────────────────────────
R1                    0.0
R2                    0.08
R3                    0.59     ← inverse-U peak (edge-of-chaos)
R4                    0.0
```

Sim mirror confirmed in LAB-10; **live AKD1000 was the deferred next tier**.

## Live promotion (AKIDA currently in use)

AKD1000 is live now (pi5-akida). The sim→live promotion is reachable on the
existing on-chip path already proven by `[[H_904]]` (live on-chip plasticity,
non-deterministic) and `[[H_858]]` (edge-of-chaos Phi-peak live). A live recompute
should also exhibit the H_679/H_904 HW-not-equal-SW non-determinism (same input →
different trace) — the living signature, distinct from the deterministic LIF sim
above. Until anima recomputes on live silicon into `.verdicts/910_*/`, this stays
INSUFFICIENT.

## Sibling links

- `[[H_909]]` (GPU/Metal precursor) · `[[H_858]]` · `[[H_677]]` · `[[H_846]]` · `[[H_904]]` · source hexa-codex LAB-10.
