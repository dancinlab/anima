---
id: H_9520
title: anima study — consolidation-CPT growth on a real study transcript
tier: PRE-REGISTERED (frozen · not fired · cost-gated GPU)
frontier: anima-study
created: 2026-07-16
---

# H_9520 — study conversation → engine-native growth (consolidation CPT)

**Claim.** A real `anima study` conversation transcript (the daemon perceiving an
exogenous teacher over many turns), consolidated back into the substrate by
continued-pretraining (CPT) on a **replay-mixed** corpus, produces an engine-native
capability lift the teacher's content is responsible for — measured as a `anima-py
evaluate` held-out reach Δ **against content-matched controls**, not a raw value.

This is the growth half of `anima study` (MVP-1 teacher client #3771 · MVP-2 percept
hook #3780 · MVP-3 conversation driver #<this cycle> already landed; those wire the
conversation + transcript and make NO growth claim — verdict = plumbing + byte-parity).

## Why this is NOT H_1230 (the dead teaching-policy)
H_1230 (🔴 RED) asked "does an **active teaching policy** (tell→check→adjust/re-space)
beat passive one-shot on a clean associative store's retention?" — a teaching-METHOD
question, on a numpy toy, and it died (method inert). H_9520 asks a different question
on a different substrate: "does **exogenous content the daemon cannot self-generate**
get absorbed by the real 303M byte-LM's weights?" — an information-injection question,
judged not on a retention curve but on **content-matched held-out reach Δ**. The teacher
here only supplies conversation MATERIAL (same status as HF human text); it is never a
grader and its logits/judgements are never distilled (`a_engine_native_learning`).

## Pipeline (frozen)
1. `anima study <303M.clm> --teacher {codex,sealion} --rounds R --window W --out T.jsonl`
   on a real ckpt (pool · never mini · `a_eval_py_canonical`) → a real transcript T.
2. Build the CPT corpus = **teacher-content lines + base-corpus REPLAY** (study fraction
   a small %). Replay-mix is MANDATORY: `corpus-py-1` (⑥ catastrophic forgetting) proved
   small-corpus CPT DESTROYS abilities absent from the corpus — biological sleep replay
   is exactly this mix. Naive study-only CPT = self-harm.
3. `anima-py train --init <303M.clm> --corpus <replay-mix> …` → serialize `.clm`.
4. `anima-py evaluate` the pre- and post-CPT `.clm` (held-out reach panel · pool).

## Frozen bars (data-blind · no tune-to-green)
GREEN iff, on held-out reach (Ψ-SOMA: signal = collapse-Δ vs ≥2 controls):
- post-CPT reach Δ ≥ +MDE over pre-CPT floor (MDE pre-computed from seed sd), AND
- **C1 replay-only** (identical byte count · identical replay fraction · teacher content
  ABSENT) does NOT lift (`control-must-match-mediating-covariate`: matches the training-
  量 covariate), AND
- **C2 scrambled-teacher** (teacher lines shape-matched, content destroyed) does NOT lift,
- FORGET gate: base held-out reach on layers ABSENT from the study corpus does NOT drop
  (`corpus-py-1` ⑦ — the forget gate must cover every layer eval reads, especially those
  the CPT corpus never reinforces; a corpus-reinforced-layer-only forget check is a forgery).

RED/🧱 with the honest number otherwise. Below-chance is first-class.

## Controls & honesty
- Growth verdict is TERMINAL only via engine-native `anima-py evaluate` on the serialized
  `.clm` (torch-side CE = DIRECTIONAL). Cement on no number these commands did not produce.
- ckpt PULL before any teardown (`a_fire_recover_complete`).
- Cost-gated GPU fire (rent = spend) — needs explicit owner go; the transcript (step 1)
  and the replay-mix builder are the $0 prerequisites this card fires first.

## Status
PRE-REGISTERED · frozen · **NOT fired** (growth verdict). The two $0 prerequisites are now BOTH built:
- **Step 1 (transcript)** ✅ — a real 303M study run landed `transcript303.jsonl` (summer $0 ·
  `~/anima-weights/study303_transcript/`, permanent). Demo is short (6 rows · 1 emit) — a longer
  study run (rounds ~30-50, summer $0) feeds a meaningful CPT; the demo transcript proves the plumbing.
- **Step 2 (replay-mix builder)** ✅ — `anima-py corpus study-replay --transcript T.jsonl --corpus BASE
  [--study-frac 0.05] [--reps N]` (cli/corpus.py · v0.15.8). Emits the replay-mix corpus + `.c1_replayonly.txt`
  (teacher ABSENT · byte-matched) + `.c2_scrambled.txt` (teacher word-shuffled · byte-matched · content
  destroyed) + `.meta.json`. Honesty audits enforced: C1 teacher-leak=0 (hard-fail), C2 byte-match to mix,
  study_frac_actual reported. `FORGET_STRATA["study-replay"]` registers the reach axes the study content does
  NOT reinforce (corpus-py-1 ⑦ (A) — the forget gate must cover the untouched strata, not just ρ·form).
  Plumbing verified byte-deterministic on the demo transcript (same seed → identical mix/C1/C2).

Remaining = **cost-gated (owner GPU go)**: step 3 `anima-py train --init 303M --corpus <replay-mix>` +
step 4 `anima-py evaluate` held-out reach Δ vs C1/C2 + FORGET gate. Design source: Fable
(scratchpad/fable_anima_study.md, §2·§4).
