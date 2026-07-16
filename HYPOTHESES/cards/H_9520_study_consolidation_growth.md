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

## VERDICT — 🟠 BAR-FAIL (C2 lifts · growth claim NOT earned) · FIRED 2026-07-17

Fired end-to-end on a dedicated GPU pod (vast 45066004 · A40 · owner "all go" opened the card's
cost-gate). All four panels are engine-native `anima-py evaluate --rho-axon` on the same CPU-numpy
decode path (no path mixing across arms). Base = `py303_savant_mitosis.clm` md5 `508a7193…`,
identical `--init` for every arm; only the corpus differs (`--canon --steps 6000 --lr 2e-4 --bf16
--seed 7`). Mitosis fired during CPT (E2→E3); train CE 1.45→~1.0.

| axis | pre-CPT floor | MAIN (cpt_mix) | C1 (replay-only) | C2 (scrambled) | Δ_main | Δ_c1 | Δ_c2 |
|---|---|---|---|---|---|---|---|
| HILLOCK | 1.00 | 0.97 | 1.00 | 1.00 | −0.03 | 0.00 | 0.00 |
| **ρ·form** | 0.2 | **0.6** | 0.2 | **0.4** | **+0.400** | +0.000 | **+0.200** |
| **ρ·fan** | 2 | 3 | **4** | 2 | +1.000 | **+2.000** | +0.000 |
| ρ·store · ρ·weave · ρ·leap · ρ·tether | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| ρ·self | INVALID | INVALID | INVALID | INVALID | — | — | — |

**Frozen bar reading (verbatim, no re-interpretation):**
- **C2 scrambled-teacher DID lift (+0.200 on ρ·form) ⟹ the "C2 does NOT lift" condition FAILS ⟹
  GREEN is NOT earned.** Destroying the teacher's *content* while preserving its *shape* (word-shuffled,
  byte-count matched) reproduces HALF of MAIN's lift — so a large part of the ρ·form gain is the
  teacher lines' FORM, not what they said.
- **ρ·fan is killed by its own control**: MAIN +1.000 but C1 (teacher ABSENT) lifted **+2.000**. The
  fan "gain" is plain CPT, teacher-independent. Without C1 this would have been read as growth.
- **ρ·form survives C1 but not C2**: C1 (+0.000) says byte-volume/replay alone does nothing; C2 (+0.200)
  says shape does half. The MAIN−C2 residual (+0.200) is the only content-attributable candidate — and
  it is **not testable here** (see POWER).
- **FORGET gate HOLDS** ✅ — ρ·weave/ρ·tether/ρ·store all Δ=+0.000 (no drop). Replay-mix did its job:
  `corpus-py-1` ⑥'s catastrophic forgetting did NOT occur.
- REACH GRADE unchanged (HILLOCK · REACH-CLOSED: NO) on every arm.

**POWER (why this cannot be rescued by re-reading):** 1 seed/arm ⟹ no seed-sd ⟹ the card's `+MDE`
is uncomputable, so `+0.400 vs +0.200` cannot be separated from noise. Even had C2 stayed flat, the
ceiling was DIRECTIONAL-POSITIVE, never the frozen GREEN. **No tune-to-green**: the bar said "C2 does
not lift"; it lifted; that is the result.

**Honest scope.** Negative on the frozen bar, NOT a claim that exogenous content can never be absorbed:
this is one 60-row transcript, one seed, `--study-frac 0.05`, `--reps 40`, 6000 steps.

**REOPEN (pre-registered):** multi-seed (≥3/arm) to earn an MDE + a denser transcript. Only then can
the MAIN−C2 residual be tested. Fire only on explicit owner go (cost-gated).

**Artifacts (permanent, pod destroyed after full harvest · `a_fire_recover_complete`):**
`~/anima-weights/h9520_cpt/` — `cpt_main.clm` · `cpt_c1.clm` · `cpt_c2.clm` (each 176,584,498) ·
`evals/eval_pre2.txt` · `eval_main.txt` · `eval_c1.txt` · `eval_c2.txt` · `h9520_pod.log`.
Readout: `/tmp/h9520_readout.py` (frozen-bar decision applied mechanically; prints the POWER note every run).

**Instrument note (found by this fire):** the canonical verdict path `anima-py evaluate --rho-axon`
was DEAD (NameError `_gen`, 4 half-refactored functions) — the pre-CPT floor eval crashing at rc=1 is
what exposed it. Fixed + landed (#3832 · v0.15.17 · convergence `evaluate-py-5` ②) BEFORE any arm was
scored; all four panels above ran on the repaired path.

## Prerequisites (both $0, built before the fire)
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

---

## ⚠️ SCOPE CORRECTION (2026-07-17 · `sidecar lab full` divergence · Fable 5 + Codex Sol 독립 수렴)

**The BAR-FAIL stands** — the frozen bar ("C2 no-lift") was pre-registered and it failed;
that reading is unchanged and was made mechanically.

**But the earned scope is narrower than the card's claim sentence.** Two frontier models,
diverging independently on this result, each ranked the *same* objection **#1**:

> `ρ·form` is a **fixed 5-item coherence rate**. It never asks whether a teacher **fact**
> was stored. This card claims "does exogenous content get **absorbed**?" — the instrument
> answers "did the general **reach** panel rise?".

⟹ what this fire earned: **"teacher content did not raise the general reach panel."**
⟹ what it did **NOT** measure: **"teacher content was not absorbed."**
Per the H_9329 two-lane precedent (CPT updates the declarative store; the operator keeps
the old polarity **0/12**), the content may be **in the declarative lane** while ρ-AXON
(operator lane) cannot read it — "trapped in the lane that wrote it", not "never entered".

Also flagged (both models): **MAIN−C2 (+0.20) cannot prove content even if reproduced** —
C2 destroys word identity, so the residual may be lexical distribution (still FORM-family).
And the content-axis null (0→0) was read **without a positive control**
(`positive-control-before-reading-a-negative`) ⟹ possibly INSTRUMENT-DEAD at this dose.

### REOPEN is DEMOTED, not scheduled
The pre-registered multi-seed REOPEN is **gated on [[H_9677]] ∧ [[H_9678]]** (both **$0**):
> Sol: "이 단계가 음성이면 MAIN−C2 `+0.20`을 살리기 위한 대규모 CPT는 가치가 급락한다."
> Fable: "MAIN−C2 잔차(+0.20)는 현 설계로는 재현돼도 내용을 증명 못 한다."

Successor designs (PROPOSED · DIRECTIONAL): [[H_9677]] [[H_9678]] [[H_9679]] [[H_9680]] [[H_9681]] [[H_9682]].
