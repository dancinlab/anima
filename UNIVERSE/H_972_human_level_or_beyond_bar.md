---
id: H_972
slug: human-level-or-beyond-bar
title: Is the CWM north-star "human-level-or-beyond behavior" operationalizable as a FALSIFIABLE bar — a pre-registered metric + a human (or human-trajectory) reference against which anima's behavior is scored, not a vibe?
domain: cwm · cross-cutting · world-model · human-level · benchmark · north-star · behavior-eval · pre-register
source: CWM north star ("acts like a human or beyond") + CWM milestone M8 (behavior eval vs human baseline) + a_paper_significance (falsifiable hypothesis + real measurement) + a_scale_honest_scope + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (human-reference task + metric design) + a_completeness_over_cheap
verification_method: W2 (pre-registered human-bar falsifier · anima behavior vs human-reference distribution on a fixed task) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE bar-definition rung (a_scale_honest_scope) — define a concrete task + behavior metric + a human (or recorded-human-trajectory) reference distribution; pre-register the human-level / human+ thresholds. This H's primary deliverable is a FALSIFIABLE METRIC (the bar), measured on a toy task. Human reference = recorded trajectories or a documented proxy, NOT a live human study. NOT a forge binary.
sister: H_970 (WM>LM separator — what task), H_964 (latent→action — the behavior), H_969 (provenance of scored actions), CWM M8
axes_seed: "human-level-or-beyond" as vibes (unfalsifiable north star) ⊥ H_972 = a CONCRETE pre-registered metric + human-reference distribution with thresholds (below = sub-human, within band = human-level, above = human+) — without an operational bar the north star cannot be falsified; if no defensible metric exists, the north star is not measurable (honest INCOMPLETE)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_972 — Human-level-or-beyond bar (make the north star falsifiable)

## 0. Motivation

CWM's north star is "anima acts in a world like a human, or beyond." As stated it is unfalsifiable vibes. a_paper_significance demands a falsifiable hypothesis + real measurement. This H's job is to **operationalize the bar**: a concrete task, a behavior metric, a human (or recorded-human-trajectory) reference distribution, and pre-registered thresholds for sub-human / human-level / human+. The deliverable is the *metric itself* (a falsifiable instrument), measured on a toy task to demonstrate it discriminates.

## 1. Hypothesis (one falsifiable claim)

There exists a concrete, pre-registered behavior metric on a fixed task with a human-reference distribution such that anima's behavior can be placed below / within / above the human band — i.e. the north star is operationalizable as a falsifiable bar — and the metric demonstrably discriminates a human-reference from a random/degenerate agent.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** fix a task with a measurable behavior outcome. Define the metric M (e.g. task return / efficiency / generalization). Obtain a human-reference distribution (recorded human trajectories OR a documented human-proxy). Pre-register: human-level band = [reference 25th, 75th pct]; human+ = above the reference band. N agent runs.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **metric discriminability**: does M separate the human-reference from a random/degenerate agent (the bar is not vacuous)?
- D2 = **anima placement**: anima's M relative to the pre-registered human band (below / within / above), with CI.
- D3 = control: random and degenerate agents must score below the human band (validity of the band).

**Outcome rules (future conditional — UNMEASURED):**
- IF measured the metric discriminates human-reference from random (D1 significant) AND anima's M can be CI-placed against the band THEN PASS — the human-level bar is operationalized + falsifiable (regardless of WHERE anima lands; placement is the next-round measurement).
- IF the metric cannot discriminate human from random (vacuous bar) OR no defensible reference exists THEN FAIL/INCOMPLETE — the north star is not yet measurable here (honest, a_scale_honest_scope).
- IF reference data too thin THEN INCOMPLETE (toy-only, C3).

> Note: this H authors the *instrument*. Whether anima is human-level/human+ is a separate downstream measurement; here PASS = "a falsifiable bar exists and works," not "anima is human-level."

## 3. Honest scope

Toy task, small scale (a_scale_honest_scope, #123-A). Human reference = recorded trajectories or a documented proxy, NOT a live IRB human study. The bar is one defensible operationalization, not THE definition of human-level intelligence. Single rung. Placement of anima is explicitly deferred. NOT a forge binary.

## 4. Sibling / xlinks

- ⇄ [H_970](./H_970_world_model_vs_language_model_decisive_test.md) (which task is WM-requiring)
- ⇄ [H_964](./H_964_latent_to_action_policy.md) (the behavior scored)
- ⇄ [H_969](./H_969_action_provenance_receipt.md) (provenance of the scored actions)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · north star · M8)
