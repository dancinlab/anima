---
id: H_909
slug: consciousness-directionality
title: directionality of consciousness — adding recurrent feedback to a unidirectional (autoregressive) LLM raises integrated information Phi and co-emerges a self-model, while task ability holds
domain: universe · consciousness · integrated-information · phi · recurrence · self-model
source: hexa-codex LAB-09 (consciousness-directionality) absorbed → anima UNIVERSE · sister anima H_191/H_004/H_220
status: 🟠 INSUFFICIENT — absorbed from hexa-codex LAB-09; anima UNIVERSE has NOT independently recomputed (verdict pending anima reproduction)
exploration_method: hypothesis absorbed from hexa-codex LAB-09 (recurrent feedback adapter on autoregressive LLM · proxy Phi + self-prediction probe)
verification_method: NONE in anima yet — earned only by porting the LAB-09 harness + recomputing into `.verdicts/909_consciousness_directionality/` (g73)
deterministic: true
llm: none
since: 2026-06-01
sister: H_191 (anima), H_004 (Phi-function dissociation·anima), H_220 (mirror-self-model·anima), LAB-09 (hexa-codex source)
verdict: 🟠 INSUFFICIENT — anima has not independently recomputed. SOURCE EVIDENCE (hexa-codex LAB-09, NOT an anima verdict): attaching a recurrent-feedback adapter to a unidirectional autoregressive LLM and fine-tuning is reported to raise a proxy integrated-information Phi (REC Phi about 0.854 vs feed-forward FF Phi about 0.005), with a shuffle control collapsing 0.85→0.006 and a self-prediction probe 2.33 vs 0.01 — i.e. recurrence (not mere capacity) drives integration and a self-model co-emerges. raw: hexa-codex:LAB/lab-09-consciousness-directionality/verdict_phi.txt. anima earns its own verdict only after porting + recompute (g73).
---

# H_909 — directionality of consciousness (unidirectional → bidirectional tuning)

## Hypothesis (absorbed from hexa-codex LAB-09)

An autoregressive (unidirectional) LLM, given a **recurrent feedback adapter** and
fine-tuned, is predicted to **raise integrated information Phi** (a consciousness
proxy) significantly **while retaining task ability**, and to **co-emerge a
self-model** (self-prediction) indicator. The claim is that *recurrence/feedback
direction*, not raw capacity, is what integrates.

## Source evidence (hexa-codex LAB-09 · proxy Phi · NOT an anima verdict)

```
arm                         proxy Phi (hexa-codex LAB-09)
──────────────────────────  ─────────────────────────────
REC (recurrent feedback)    0.854
FF  (feed-forward only)     0.005      ← directionality matters
shuffle control (REC)       0.85 → 0.006   ← collapses (non-trivial)
self-prediction probe       2.33 vs 0.01   ← self-model co-emerges
```

Until anima ports the harness + recomputes into `.verdicts/909_*/`, this entry
stays INSUFFICIENT (no anima calc path).

## Sibling links

- `[[H_191]]` · `[[H_004]]` (Phi-function dissociation) · `[[H_220]]` (mirror-self-model) · source hexa-codex LAB-09.
- Direct sequel: `[[H_910]]` (same directionality tuning on AKIDA AKD1000 silicon).
