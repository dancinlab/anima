---
id: H_985
slug: keystone-scaleup
title: Does the H_970 WM>LM separator HOLD at larger model/state sizes AND across MULTIPLE distinct partially-observable task families — or was it a single-toy / single-task artifact?
domain: cwm · cross-cutting · world-model · language-model · keystone · scale-up · task-diversity · re-test
source: H_970 (KEYSTONE — WM>LM separator on ONE delayed-cue toy at ONE capacity) + a_toy_scale_recheck (a single toy point is INCOMPLETE for a general claim) + a_scale_honest_scope + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (WM-requiring task construction, ×3 distinct families) + a_completeness_over_cheap (the ladder + diversity H_970 lacked)
verification_method: W2 (pre-registered scale+diversity falsifier · matched-capacity LM baseline · mem-aug control) + g5 CODE-measured (no LLM self-judge, p7)
raw_rank: 9
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: TOY ladder — 3 distinct partially-observable task families × a 4-rung capacity ladder (latent/feat dim 16/32/64/128), $0 CPU-local (a_scale_honest_scope). Still bounded (toy dim/N), production-scale OPEN — but ≥3 tasks × ≥4 rungs is the ladder H_970's single point lacked. NOT a forge binary.
sister: H_970 (the keystone single-rung this scales up), H_962 (latent dynamics), H_964 (latent→action), H_984 (object permanence — the persistent-state property)
axes_seed: "H_970's WM>LM separator is a general law" (the optimistic read) ⊥ H_985 = it may be a single-toy / single-task artifact — re-test at larger state sizes AND across ≥3 mechanistically-distinct partially-observable tasks; if the gap collapses with capacity (LM catches up) OR holds only on delayed-cue, H_970 does NOT generalize (closed-negative on generality)
verdict: 🔴 FAIL (closed-negative on GENERALITY) — the WM>LM separator is TASK-SPECIFIC / PRIMITIVE-LIMITED, NOT scale+diversity-robust. It holds large (d 20-35, all 4 rungs) ONLY on T1 delayed-cue (H_970's own family); on T2 parity-tracking and T3 hidden-position both arms sit at chance (mem-aug=1.0 proves these ARE persistent-state tasks, but the toy linear-retention WM cannot represent XOR-parity / modular path-integration). H_970's separator is REAL but NARROW (one carry-a-stored-symbol mechanism), not a general WM>LM law. Toy ladder; production OPEN.
---

# H_985 — Keystone WM>LM scale-up + task-diversity re-test (does H_970 generalize?)

## 0. Motivation

H_970 (the CWM keystone, 🟢) found a decisive WM>LM separator on ONE toy task (delayed-cue recall) at ONE capacity: a persistent-latent-state world model scored 0.995 while a capacity-matched stateless LM sat at chance (0.258, gap 0.737, d 36.8), and a memory-augmented LM control recovered to 1.0 — localizing the gap to the persistent-state requirement. a_toy_scale_recheck is explicit: **a single toy point is INCOMPLETE for a general claim**, and scale-sensitive phenomena need a ladder (≥3 rungs). H_970's own §3 conceded "existence-proof-by-construction, single toy rung, ladder OPEN." This H runs the ladder H_970 lacked — and asks whether the separator survives (a) larger state sizes and (b) task diversity, or whether it was a single-toy / single-task artifact.

## 1. Hypothesis (one falsifiable claim)

The H_970 WM>LM separator GENERALIZES: across ≥3 mechanistically-distinct partially-observable task families (each requiring a persistent/partially-observed world-state) and ≥2 capacity rungs, a persistent-latent-state world model beats a capacity-matched stateless LM by a large effect (d>0.8) that does NOT shrink as capacity grows, and a mem-aug control closes the gap.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** build ≥3 DISTINCT partially-observable task families (not just delayed-cue) × a small capacity ladder. For each (task, rung) cell, three arms at matched capacity:
- **arm-WM** = recurrent latent-state world model (persistent state).
- **arm-LM** = capacity-matched feedforward windowed predictor (NO persistent state).
- **arm-memLM** = memory-augmented LM control (the needed hidden state re-exposed at the decision step).

The three families (mechanistically distinct, so a PASS is diversity-robust not a single-mechanism fluke):
1. **T1 delayed-cue recall** (H_970's anchor) — carry a single stored symbol across a delay.
2. **T2 hidden-state parity tracking** — integrate an *accumulated, never-observed* XOR-parity of a toggle stream.
3. **T3 hidden-position gridworld** — path-integrate an unobserved position on a ring from move history (modular accumulation).

**Measurement (g5 CODE-measured, no LLM self-judge):**
- D1 = task success WM vs LM vs memLM, per (task, rung).
- D2 = separator gap (WM−LM) + Cohen d + Welch p, per cell.
- D3 = does the gap PERSIST as capacity grows (LM does NOT catch up) AND across ALL ≥3 families, and does mem-aug CLOSE it?

**Outcome rules (frozen, future-conditional — UNMEASURED at freeze):**
- IF WM>LM gap is large (d>0.8) at ≥2 rungs on ALL ≥3 task families AND the LM never catches up at the top rung AND mem-aug closes it on every task → **PASS** 🟢 SCALE+DIVERSITY-ROBUST (H_970 generalizes; CWM premise robust beyond the single toy).
- IF the gap COLLAPSES at larger capacity (the matched LM catches up off chance toward a winning WM, d<0.8 at the top rung) → **FAIL** 🔴 (H_970 was capacity-limited; closed-negative, a_paper_negative_ok).
- IF the separator is TASK-SPECIFIC (a large gap only on delayed-cue, not the other families) → **FAIL** 🔴 (H_970 was a task artifact, not a general WM>LM property; closed-negative).
- IF the ladder is too short / a task is not actually WM-requiring (mem-aug doesn't close it) → INCOMPLETE (toy-only, C3).

## 3. Honest scope

Toy ladder (a_scale_honest_scope, #123-A): bounded latent/feature dim {16,32,64,128} and toy N; production-scale transfer UNVERIFIED. But ≥3 mechanistically-distinct task families × ≥4 capacity rungs is precisely the ladder H_970's single point lacked, so it directly tests the generality H_970 could not. Capacity-matching is pre-registered and audited per cell (WM readout (latent+1)·C == LM readout (feat+1)·C). NOT a forge binary. A FAIL here is a closed-negative on the *generality* of the keystone, which is itself a publishable finding (a_paper_negative_ok) — it does not retract H_970's narrow existence-proof, it bounds it.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `UNIVERSE/h985_keystone_scaleup.py` · verdict: `.verdicts/985_keystone_scaleup/h985_keystone_scaleup.txt`

3 task families × 4 capacity rungs (latent/feat dim) × 10 seeds × {train 600 / test 300}. Each cell: WM (retentive orthogonal-recurrence latent state) vs matched-capacity stateless windowed LM vs mem-aug LM (hidden state re-exposed at the decision step). Chance = 1/K: T1=0.250, T2=0.500, T3=0.167.

| task | rung | chance | WM | LM | memLM | gap | Cohen d | p |
|---|---|---|---|---|---|---|---|---|
| T1 delayed-cue | 16 | 0.250 | 0.645 | 0.246 | 1.000 | 0.400 | 20.13 | 9.8e-17 |
| T1 delayed-cue | 32 | 0.250 | 0.897 | 0.243 | 1.000 | 0.653 | 20.89 | 1.5e-19 |
| T1 delayed-cue | 64 | 0.250 | **1.000** | 0.242 | 1.000 | 0.758 | 28.89 | 2.6e-13 |
| T1 delayed-cue | 128 | 0.250 | **1.000** | 0.245 | 1.000 | 0.755 | 34.89 | 4.7e-14 |
| T2 parity-track | 16 | 0.500 | 0.500 | 0.505 | 1.000 | −0.005 | −0.16 | 0.73 |
| T2 parity-track | 32 | 0.500 | 0.494 | 0.505 | 1.000 | −0.010 | −0.34 | 0.46 |
| T2 parity-track | 64 | 0.500 | 0.494 | 0.505 | 1.000 | −0.010 | −0.34 | 0.46 |
| T2 parity-track | 128 | 0.500 | 0.494 | 0.505 | 1.000 | −0.010 | −0.34 | 0.46 |
| T3 hidden-pos | 16 | 0.167 | 0.334 | 0.335 | 1.000 | −0.001 | −0.05 | 0.91 |
| T3 hidden-pos | 32 | 0.167 | 0.339 | 0.337 | 1.000 | 0.002 | 0.10 | 0.82 |
| T3 hidden-pos | 64 | 0.167 | 0.339 | 0.335 | 1.000 | 0.004 | 0.18 | 0.69 |
| T3 hidden-pos | 128 | 0.167 | 0.339 | 0.335 | 1.000 | 0.004 | 0.18 | 0.69 |

Per-task summary: T1 — WM>LM separator at all rungs (WM-solves ✓, LM never catches up, mem-aug closes ✓). T2 — no separator (both arms at chance; mem-aug=1.0). T3 — no separator (both arms ~2× chance and tied, gap≈0; mem-aug=1.0).

**Finding (🔴 FAIL — closed-negative on GENERALITY):** the H_970 WM>LM separator is **TASK-SPECIFIC / PRIMITIVE-LIMITED, NOT scale+diversity-robust**. It reproduces strongly on T1 delayed-cue (H_970's own family) at *every* capacity rung (d 20–35, monotone up with size — so within that family it is scale-ROBUST, ruling out the "tiny capacity inflated the gap" worry), but it VANISHES on the two new families: on T2 (parity) and T3 (hidden-position) both the WM and the LM sit at chance with gap≈0. The mem-aug control returns 1.0 on ALL three families, which proves T2 and T3 genuinely ARE persistent-state tasks (a stateless predictor that is *handed* the hidden state solves them) — so the failure is not "these tasks don't need a world-state." Mechanistically, the toy WM primitive (linear orthogonal-retention reservoir) can carry a stored one-hot symbol across a delay (T1) but **cannot represent an accumulated XOR-parity (T2) or a modular path-integrated position (T3)** — both require nonlinear / modular state-update the linear retention reservoir lacks. So H_970's separator is REAL but NARROW: it demonstrates ONE mechanism (carry-a-symbol persistence beats a window) on ONE task family, not a general WM>LM law across the diverse partially-observable tasks a real world model must handle.

**Interpretation for CWM:** H_970 is NOT retracted — it remains a valid existence-proof that *a* persistent-state task separates WM from LM. But its generality is bounded: a richer WM primitive (nonlinear / gated recurrence, not a linear reservoir) is required before the WM>LM advantage can be claimed across task families. The honest next rung is a nonlinear-recurrence WM (GRU/LSTM-style or tanh-recurrent) re-run of T2/T3 — if THAT solves parity + path-integration while the matched LM stays at chance, the generality claim is recoverable; if even a nonlinear WM fails, the separator is truly delayed-cue-specific. This is a primitive question, not a scale question.

## 4. Sibling / xlinks

- ⇄ [H_970](./H_970_world_model_vs_language_model_decisive_test.md) (the keystone single-rung this scales up — its narrow existence-proof stands; its generality is bounded here)
- ⇄ [H_962](./H_962_latent_forward_dynamics.md) · [H_964](./H_964_latent_to_action_policy.md) (the WM agent)
- ⇄ [H_984](./H_984_world_model_object_permanence.md) (the persistent-state property exploited)
- ⇄ [CWM](../CWM/CWM.md) (CWM-VERIFY · domain keystone ladder)
- external: world-model vs LM distinction; JEPA/Dreamer require nonlinear latent transitions (CWM.log.md landscape) — consistent with the primitive-limited finding here
