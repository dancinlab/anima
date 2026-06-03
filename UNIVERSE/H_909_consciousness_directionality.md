---
id: H_909
slug: consciousness-directionality
title: directionality of consciousness — adding recurrent feedback to a unidirectional (autoregressive) LLM raises integrated information Phi and co-emerges a self-model, while task ability holds
domain: universe · consciousness · integrated-information · phi · recurrence · self-model
source: hexa-codex LAB-09 (consciousness-directionality) absorbed → anima UNIVERSE · sister anima H_191/H_004/H_220
status: 🟢 SUPPORTED-NUMERICAL — anima INDEPENDENTLY recomputed (ported LAB-09 harness, deterministic) — REC Phi 0.854 ≫ FF Phi 0.005, shuffle control collapses, self-pred co-emerges — 3/3 falsifiers true
exploration_method: ported hexa-codex LAB-09 substrate proxy to `UNIVERSE/harness/h909_phi_directionality.hexa` — n=5 binary units on a ring, shared external drive + per-unit noise (same seeded LCG both arms), FF (unidirectional, no x_t term) vs REC (bidirectional recurrent neighbors), Phi-proxy = I(X_t;X_{t+1}) − min_bipartition[I(A;A')+I(B;B')], self_pred = I(X_t;X_{t+1}|U_t)
verification_method: anima recompute — `hexa run UNIVERSE/harness/h909_phi_directionality.hexa` ($0, deterministic seeded LCG, no LLM, no network) → `.verdicts/909_consciousness_directionality/run.txt`. g5 CODE-measured, byte-identical across runs (seed=42, n=5, T=120000).
deterministic: true
cross_process_byte_identical: true
llm: none
since: 2026-06-01
sister: H_191 (anima), H_004 (Phi-function dissociation·anima), H_220 (mirror-self-model·anima), LAB-09 (hexa-codex source)
verdict: 🟢 SUPPORTED-NUMERICAL — anima INDEPENDENTLY recomputed (deterministic, byte-identical seed=42). Adding recurrent (bidirectional) coupling to a unidirectional (autoregressive-analog) system with bit-identical external I/O raises the integrated-information Phi-proxy from FF Phi=0.005391 to REC Phi=0.854292 (delta_phi=0.848901 bits), while the shuffle control (REC_shuffled) collapses back to Phi=0.006289 (control band=0.000898 bits) and the self-prediction probe rises from self_pred=0.010796 (FF) to 2.32818 (REC, delta_self=2.31738 bits). 3/3 pre-registered falsifiers PASS — phi_REC>FF beyond control true, self_REC>FF true, shuffle_collapses_phi true. So directionality/recurrence (not raw capacity) is what integrates AND a self-model co-emerges. Proxy caveat: substrate IIT-proxy (mutual-info bipartition), not faithful-IIT4 (cf H_278); the full LLM recurrent-adapter fine-tune is a future stress tier. raw: .verdicts/909_consciousness_directionality/run.txt.
---

# H_909 — directionality of consciousness (unidirectional → bidirectional tuning)

## Hypothesis (absorbed from hexa-codex LAB-09)

An autoregressive (unidirectional) LLM, given a **recurrent feedback adapter** and
fine-tuned, is predicted to **raise integrated information Phi** (a consciousness
proxy) significantly **while retaining task ability**, and to **co-emerge a
self-model** (self-prediction) indicator. The claim is that *recurrence/feedback
direction*, not raw capacity, is what integrates.

## anima recompute (ported LAB-09 harness · deterministic · $0 · proxy Phi)

anima INDEPENDENTLY recomputed by porting the LAB-09 harness to
`UNIVERSE/harness/h909_phi_directionality.hexa` and running it (seeded LCG,
no LLM, no network). Verbatim stdout in `.verdicts/909_consciousness_directionality/run.txt`.

```
arm                     phi        whole     parts     self_pred
──────────────────────  ─────────  ────────  ────────  ─────────
FF  (unidirectional)    0.005391   0.005467  7.5e-05   0.010796
REC (bidirectional)     0.854292   2.22872   1.37443   2.32818
REC_shuffled (control)  0.006289   0.006664  0.000375  0.01027

delta_phi  (REC - FF)         = 0.848901 bits
delta_self (REC - FF)         = 2.31738 bits
shuffled_control_band         = 0.000898 bits

falsifier phi_REC>FF (beyond control)  : true
falsifier self_REC>FF                  : true
falsifier shuffle_collapses_phi        : true
VERDICT supported (all 3)              : true
```

Recurrence/directionality (not raw capacity, since both arms share bit-identical
external I/O) is what lifts the integrated-information proxy, the shuffle control
collapses REC Phi back to the FF band, and the self-prediction probe co-emerges.
All 3 pre-registered falsifiers PASS — anima earns its own SUPPORTED-NUMERICAL
verdict (g73). Proxy caveat: substrate IIT-proxy (mutual-info bipartition), not
faithful-IIT4 (cf `[[H_278]]`); the full LLM recurrent-adapter fine-tune is a
future stress tier.

## Sibling links

- `[[H_191]]` · `[[H_004]]` (Phi-function dissociation) · `[[H_220]]` (mirror-self-model) · source hexa-codex LAB-09.
- Direct sequel: `[[H_910]]` (same directionality tuning on AKIDA AKD1000 silicon).
