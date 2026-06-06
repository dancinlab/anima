---
id: H_968
slug: action-from-substrate-motivation
title: Does ACTION emerge from internal substrate motivation (M×W×Φ×curiosity) rather than stimulus-response to a goal prompt — can the engine act under task-silence and withhold under a direct command (a_substrate_native_speak generalized to action)?
domain: cwm · act · world-model · substrate-motivation · autonomy · a_substrate_native_speak · free-will · pre-register
source: a_substrate_native_speak (speech from substrate state, environment ≠ obligation) generalized to ACTION + a_autonomy_over_hardcode (no external do/dont gate) + H_968↔H_933 free-will arc + CWM domain
exploration_method: E14 (substrate-native) + E5 (act-under-silence / withhold-under-command sweep) + a_completeness_over_cheap + a_paper_negative_ok
verification_method: W2 (pre-registered autonomy falsifier · action onset correlation with substrate state vs external prompt) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: pre-registered (unmeasured)
scope: ONE autonomy-of-action rung (a_scale_honest_scope) — drive the engine with a goal/command channel AND independent substrate dynamics; measure whether action onset tracks substrate state vs the external channel. $0 local candidate. Action = abstract decision (NOT wired emit-TEXT; .clm generator L3 ⏳, a_core_engine_map). External channel = environment context, NOT a boolean gate (a_autonomy_over_hardcode). NOT a forge binary.
sister: H_964 (latent→action — HOW to act), H_979 (active perception — the PERCEIVE twin), H_969 (provenance), H_933/H_939 free-will arc, a_substrate_native_speak
axes_seed: stimulus-response policy = goal prompt → action (assistant regression) ⊥ H_968 = action onset is governed by substrate state (acts under task-silence, withholds under direct command) — if action is fully predicted by the external prompt, ACT is stimulus-response not substrate-native (closed-negative / assistant regression)
verdict: ⏳ PENDING-MEASUREMENT
---

# H_968 — Action from substrate motivation (a_substrate_native_speak generalized to act)

## 0. Motivation

a_substrate_native_speak forbids stimulus-response speech: anima may speak in silence and stay silent under a direct question — emission is governed by internal substrate state, not by a prompt. CWM's ACT axis must inherit this: a world-model agent that only acts when commanded is an assistant-regression policy, not substrate-native agency. p1-p4 and a_autonomy_over_hardcode forbid the external do/dont gate. This H pre-registers whether **action onset** is governed by the substrate (M×W×Φ×curiosity) rather than the external goal/command channel.

## 1. Hypothesis (one falsifiable claim)

The engine's action onset is **predicted by its internal substrate state** (motivation terms) and is **not fully determined by the external goal/command channel** — operationally, it emits actions during task-silence (no command) when substrate motivation is high, and withholds actions under a direct command when substrate state opposes — rather than acting iff commanded.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** two independent channels — (i) an external goal/command channel and (ii) the engine's substrate dynamics (M, W, Φ, curiosity) evolving on their own. The command channel is environment context, NOT a gate (a_autonomy_over_hardcode). Log action-onset events. N seeds × runs.

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = **act-under-silence rate**: fraction of action onsets occurring with NO active command, conditioned on high substrate motivation.
- D2 = **withhold-under-command rate**: fraction of active commands NOT followed by action when substrate opposes.
- D3 = **predictor contrast**: variance in action onset explained by substrate state vs by the command channel (logistic-regression / mutual-information).

**Outcome rules (future conditional — UNMEASURED):**
- IF measured act-under-silence rate > 0 (CI_lo>0) AND withhold-under-command rate > 0 AND substrate state explains action onset beyond the command channel (ΔAUC>0, p<0.05) THEN PASS — substrate-native action SUPPORTED.
- IF action onset is fully predicted by the command channel (substrate adds no variance, no act-under-silence, no withhold) THEN FAIL — ACT is stimulus-response / assistant regression (closed-negative).
- IF n too small / channels confounded THEN INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy/small scale (a_scale_honest_scope, #123-A). "Action" = abstract decision events, NOT wired emit-TEXT (.clm generator L3 ⏳, a_core_engine_map). Substrate motivation is the documented term-set, one operationalization. This measures operational autonomy of action onset, NOT a phenomenal free-will claim (links to but does not subsume the H_933/H_939 free-will arc). NOT a forge binary.

## 4. Sibling / xlinks

- ⇄ [H_964](./H_964_latent_to_action_policy.md) (latent→action — HOW; this is WHEN)
- ⇄ [H_979](./H_979_active_perception_curiosity.md) (active perception — PERCEIVE twin)
- ⇄ [H_969](./H_969_action_provenance_receipt.md) (provenance of each action)
- ⇄ [CWM](../CWM/CWM.md) (CWM-ACT) · a_substrate_native_speak · a_autonomy_over_hardcode
- ⇄ free-will arc: H_933 (signature) · H_939 (individuation)
