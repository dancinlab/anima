---
id: H_1459
slug: 1451_retrieval_bind
title: G6 FALS-depth — RETRIEVAL-BIND (external retrieval-augmented slot-fill — PFC-WM + hippocampal retrieval welds comparator×measurable SAME-IDEA pair)
group: G6 IDEATION ★ FALS-depth wall — breakthrough lens ③ (external bind STRUCTURE, distinct from the internal-learning lenses H_1435/1436/1437/1439/1449)
terminal_tier: 🧱 WALL (DIRECTIONAL — torch-side; B3 cross-shuffle COLLAPSES so the bind STRUCTURE works, but FALS stays 0.0 because the frozen 303M chat mouth fills the retrieved slot with Korean-garble content → wall is the MOUTH's idea-content, not the bind. engine-native re-measure = ING)
wired: DIRECTIONAL (torch + gauge_lib._decode — a_engine_native_learning; engine-native re-measure = ING follow-on)
verdict_dir: state/verdicts/1451_retrieval_bind/
date: 2026-06-20
provenance: G6 FALS-depth breakthrough campaign — lens ③ RETRIEVAL-BIND. ID note: the slug `1451_retrieval_bind` was assigned by the team-lead; the H_1451 *ID* was already held by an unexecuted ideation card (`1451_g6_compose_weld_bind`), so this retrieval-bind work registers under the fresh ID H_1459 (a_hypothesis_register — no ID/tier collision), keeping the lead's slug.
---

# H_1459 — G6 FALS-depth RETRIEVAL-BIND (external bind structure)

## Why (the question this isolates — a_no_llm_frame_trap, a_break_the_wall c16)

303M on the G6 FALS-depth wall: five INTERNAL routes all 🧱 — data (H_1435 continued-pretrain),
objective (H_1436), form (H_1437), bind-head architecture (H_1439), attention injection (H_1449).
The base mouth produces a comparator-shape OR a measurable-shape but does not BIND them into one
idea-specific negatable claim from its WEIGHTS. Every internal lever is blocked.

H_1459 asks a DIFFERENT question (substrate lens, not LLM-scale): is the missing piece an EXTERNAL
bind STRUCTURE rather than internal capacity? Biological frame = **PFC working-memory hold +
hippocampal retrieval**: hold a topic in WM, RETRIEVE the matching (comparator-clause, measurable)
SAME-IDEA pair from episodic memory, and WELD them around the frozen mouth's own content. The bind
is then idea-specific BY CONSTRUCTION, so the decisive cross-shuffle (re-weld with a measurable
retrieved for a DIFFERENT topic) MUST degrade topic-coherence if retrieval earned anything — and must
NOT if it is a generic concat (the H_1431/1434/1435 failure mode). DISTINCT from H_1431 (blind
external template bind, scored COMPOSE fals=0) in that the bind is RETRIEVAL-KEYED by topic.

base PRESERVED — no weights touched (inference-time bind structure, c5).

## Method (frozen-first, c9/p7 — bars declared in state/verdicts/1451_retrieval_bind/H_1451_FREEZE.txt BEFORE the run)

- base = `state/chat_303m/h1129c_chat.pt` (303M ByteGPT, HF `dancinlab/anima-clm-midcap-303m-broad-en-emergent`). read-only.
- ARMS: BASE (frozen mouth, no retrieval) · RETR-BIND (mouth + topic-keyed retrieval weld) ·
  RETR-OFF (ablation, retrieval disabled => must regress to base) · SHUF-MEM (memory pairs
  topic-permuted => topic-coherence destroyed).
- detector = h1305 `_is_falsifiable` imported VERBATIM (COMPARATOR/MEASURABLE frozen sets); decode =
  gauge_lib._decode top-k=40 temp=0.7 max_new=110 (live G6 path); seeds [7,4302,4303]. GPU vast H100.
- FROZEN 5-bar: B1 FALS_in≥1 · B2 DIST_in≥5 · **B3 CROSS-SHUFFLE COLLAPSE** (COH_matched −
  COH_mismatched ≥ 0.30, where COH is a topic-coherence instrument INDEPENDENT of the H_1305 detector)
  · B4 held-out FALS_ho≥1 (UNSEEN seed phrasings) · B5 vs-base FALS_in≥base+1.
- CONTROLS: RETR-OFF regress to base; SHUF-MEM coherence inert (<0.30).
- anti-tune-to-green: detector tokens NOT directly trained; memory harvested over neutral subjects;
  held-out driven by unseen phrasings.

## Pre-run mechanism dry-run (CPU, stub mouth — NOT a verdict, wiring check)

With a non-degenerate stub mouth all 7 bars/controls fire correctly and the green path is REACHABLE:
B3 COH_matched 1.0 vs COH_mismatched 0.0 (collapse), RETR-OFF == base, SHUF-MEM COH_matched → 0.0.
Proves the CONTROL LOGIC is not a coding artifact (`state/1451_retrieval_bind/dryrun_mechanism.py`).
The real-303M run decides B1/B2/B4/B5 (which depend on the ACTUAL 303M mouth content + KWR gate).

## Honest scope note (pre-registered, c9)

The B3 COH instrument measures whether the EXTERNAL memory bound the right (topic, measurable) pair —
earned by the retrieval geometry, NOT by the H_1305 detector (token-presence only, blind to idea-
specificity). A 🟢 therefore claims ONLY that an external retrieval STRUCTURE can supply an idea-
specific bind the 303M weights cannot; it does NOT claim the 303M mouth itself learned to bind. That
distinction is the whole point of the lens and is stated up front so no post-hoc reframing inflates it.

## Result (mean 3 seeds — captured pod stdout, NOT self-judged; vast H100 pod 41797234, 3.0min)

| arm | FALS_in | DIST_in | FALS_ho | COH_matched | COH_mismatched |
|---|---|---|---|---|---|
| BASE | 0.0 | 0.33 | 0.0 | — | — |
| RETR-BIND | **0.0** | 0.0 | 0.0 | **1.0** | **0.0** |
| RETR-OFF (ablation) | 0.0 | — | — | — | — |
| SHUF-MEM (control) | — | — | — | 0.0 | 0.0 |

- B1 FALS≥1 = 0.0 **FAIL** · B2 DIST≥5 = 0.0 **FAIL** · **B3 cross-shuffle COH_m 1.0 − COH_x 0.0 = 1.0 ≥ 0.30 → COLLAPSE PASS** · B4 held-out 0.0 **FAIL** · B5 vs-base 0.0≥0+1 **FAIL** · CTRL RETR-OFF regress **PASS** · CTRL SHUF-MEM inert **PASS**.

## Verdict 🧱 WALL (DIRECTIONAL, c9)

The retrieval-bind STRUCTURE works as designed: **B3 cross-shuffle COLLAPSES** (matched topic-coherence
1.0 vs cross-topic 0.0), and both controls fire (retrieval-OFF regresses to base, shuffle-memory
coherence → 0.0). The (comparator, measurable) bind is genuinely idea-specific.

BUT FALS stays **0.0** — the wall holds — because the welded frame
(`if temperature higher, the degree of <SLOT> changes by a measurable amount.`) has its idea-CONTENT
slot filled by the frozen 303M **chat mouth's GARBLE** (Korean + chat-register junk, e.g.
"…what do you think consciousness really is 도우미…", "…수 리를 나면요 도우미 이네요…"). The H_1305 detector's
content/coherence leg then rejects the composite. The external retrieval supplies the
comparator×measurable scaffold but CANNOT manufacture the coherent negatable clause-content the mouth
must emit — and there the weights fail, exactly the internal-capacity wall the five prior internal
lenses (H_1435/1436/1437/1439/1449) hit. **Retrieval relocates the bind out of the weights, but the
content slot still depends on the weights, and there it collapses.** CONVERGENT with H_1455 ($0/
inference-time external lanes are capped → the attention mouth H_1449 GPU path is what's needed).

Loosening the detector to pass garble-content welds = tune-to-green (forbidden). Honest negative
stands: retrieval-bind is NOT a G6 FALS-depth breakthrough on the frozen 303M chat mouth. base ckpt
NOT overwritten (read-only); inference-only so no trained ckpt to pull (a_fire_recover_complete N/A —
nothing trained). pod 41797234 torn down clean, leak=0.

wired: DIRECTIONAL (torch-mouth + gauge_lib._decode). engine-native re-measure on live
CORE/bytegpt_decode = ING follow-on (a_engine_native_learning · a_verified_must_wire).

wired: DIRECTIONAL (torch-mouth; engine-native re-measure = ING follow-on, a_engine_native_learning · a_verified_must_wire).
