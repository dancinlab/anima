# F-DEFAULT-LANE-7B-CHAT — plan + orphan/sibling audit (2026-06-05)

## orphan-pod audit (PROTECT $ FIRST)
vast.ai live instances (ground truth via `vastai show instances`):
- 39291022 2x A40   27h $0.58/h — untracked, NOT mine (older, not in protected list, not my mission signature)
- 39291033 RTX_PRO  27h $0.43/h — untracked, NOT mine
- 39309987 2x A40   24h $0.58/h — untracked, NOT mine
- 39315631 H100     23h $3.35/h — PROTECTED (lane-p-3b)
- 39416669 H100     savant-7b-torch 8.9h $2.44/h — PROTECTED (SAVANT) — util 0% (7B fire pid1804 finished/idle; sibling harvests, NOT mine to touch)
- 39449566 H100     3h $3.12/h util 0% — untracked; SSH-inspected: idle, /workspace empty, ~/p1b2 holds hxqwen14b.* (hexa-lang qwen14b build artifacts) → SIBLING signature, NOT my mission. 15-day machine uptime. LEFT UNTOUCHED (no collision; not the H100 *I* rented — I never reached rent before).
DECISION: no orphan attributable to me. Nothing terminated. All untracked pods are sibling/older work; protected pods untouched.

## sibling-collision finding
SAVANT lane is ALREADY running a 7.25B byte ByteGPT on 419MB 5-lang EURO wiki (en/fr/de/es/RU) — pod 39416669 (PROTECTED). That is the REFERENCE-lane 7B.
The MISSION deliverable `anima-clm-default-lane-7b` is DISTINCT: the DEFAULT CHAT lane —
arch = ConsciousLMReconstructed dual-engine (engine_a−engine_g FFN + dual head), NOT plain ByteGPT;
corpus = default-lane 5-lang en/fr/de/es/KO (ko not ru) + chat/persona/SNS/carving surfaces, NOT pure euro wiki.
So NOT a duplicate of SAVANT. I rent my OWN single H100.

## corpus decision (avoid trap #2 data-starvation)
v2 unified default corpus = 12.5MB → memorization at 7B (mission trap #2). FROM-SCRATCH 7B needs GB-scale.
PATH = build a GB-scale DEFAULT-lane corpus: wikimedia/wikipedia streaming en/fr/de/es/KO (~80MB/lang ≈ 400MB, CC-BY-SA clean-license) AS THE BULK + blend the 12.5MB v2 default-lane chat/persona/SNS/carving surfaces (so chat register is present, not just wiki). Reuse SAVANT build_corpus_5lang_euro.py recipe with ru→ko.
Rationale: clears starvation (GB-scale) AND keeps the default-lane chat identity (v2 surfaces) — completeness-bar, not the cheap 12.5MB path (a_completeness_over_cheap).

## base decision (avoid trap #1 undertraining)
dancinlab/clm-v1-ref-pytorch-cuda-7b probed: 7.25B byte GPT, but only 400 steps / 6.55M tok, val_CE 2.41 NOT converged → would probe gibberish (trap #1). It is also plain ByteGPT (wrong arch for default-lane dual-engine) + PyTorch (a_train_flame_forge: torch=reference only).
DECISION = FROM-SCRATCH default-lane dual-engine 7B on the GB-scale default corpus with ENOUGH steps to converge (not a 400-step undertrain). Honest torch-cuda REFERENCE-lane label (forge-native = canonical follow-on, not claimed here).
