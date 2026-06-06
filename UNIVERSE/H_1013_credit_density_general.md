---
id: H_1013
slug: credit-density-general
title: Is the credit-DENSITY unlock (H_1006) task-GENERAL — does per-step supervision crack long-horizon tasks BEYOND T3 modular?
domain: cwm · cross-cutting · world-model · learning-method · credit-assignment · dense-supervision · generalization · re-test
source: H_1006 (GREEN dense per-step supervision cracks T3 modular position-tracking at 36) + H_1007-1010 (RED compute/init/warm-start/modulus-curriculum all fail) — is credit-DENSITY a GENERAL principle for long-horizon world-model learning, or specific to the T3 modular ring-counter?
exploration_method: E5 (apply the H_1006 per-step-supervision lever to NEW long-horizon task families) + a_completeness_over_cheap
verification_method: W2 (pre-registered generalization falsifier · per-step auxiliary supervision on >=2 NEW state-bound tasks · capacity-matched LM/mem-aug arms · python3 -u serial) + g5 CODE-measured (no LLM self-judge, p7)
deterministic: true
pre_register_frozen: true
frozen_at: 2026-06-07
since: 2026-06-07
sister: H_1006 (dense-sup cracks T3 modular), H_1007-1010 (other methods fail), H_1005 (curriculum cap), H_1000 (task harness)
status: measured
verdict: 🔴 FAIL = CREDIT-DENSITY-TASK-LOCAL — per-step supervision does NOT generalize across new accumulator algebras at len=36. Of 3 NEW state-bound families (mem-aug~1.0): CAPPED-and-cracked-by-dense=[]; CAPPED-but-survives-dense=[N1 kv-recall]; NO-cap (final-label already solves, dense not needed)=[N2 running-max, N3 stack-depth]. The H_1006 cap-and-crack is STRUCTURE-SPECIFIC (only accumulators genuinely hard from a sparse final label, like T3 modular). Per-step gradient density = a real but BOUNDED lever, not a general long-horizon principle. closed-negative on generality (a_paper_negative_ok); toy len=36 $0 CPU, rungs{16,32}, seeds CUT 3 (REPORTED), larger-budget/production OPEN. verbatim .verdicts/1013_credit_density_general/h1013.txt
---

# H_1013 — credit-density generalization (is per-step supervision a general long-horizon unlock?)

## 0. motivation
H_1006 found per-step state supervision cracks T3 (modular position-tracking) where compute/init/warm-start/modulus-curriculum (H_1007-1010) all failed — naming "credit-DENSITY" as the lever. Open: is credit-density a GENERAL principle for long-horizon world-model learning, or did it just happen to fit the T3 modular ring-counter? A principle must transfer.

## 1. hypothesis
Per-step supervision of the hidden task-relevant state cracks ANY long-horizon state-bound task (not just modular counting) where final-label-only training fails — credit-density is the general unlock, because it restores gradient at every step of the credit chain regardless of the accumulator's algebra.

## 2. pre-registered falsifier (frozen 2026-06-07)
Build >=2 NEW long-horizon state-bound task families distinct from T3 modular (e.g. a long-horizon associative key-value recall; a running-max or set-membership accumulator; a stack/bracket-matching task — each genuinely state-bound, verified by mem-aug LM = 1.0). For each: train the GRU world-model at a capped length (where final-label-only fails) WITH vs WITHOUT per-step state supervision, capacity-matched LM control, multi-seed, python3 -u serial. Outcome (no token before measuring):
- IF per-step supervision cracks ALL the new families (far above chance, large effect vs LM, tracking mem-aug) THEN PASS = CREDIT-DENSITY-GENERAL (the lever is task-general; per-step gradient density is the long-horizon world-model unlock).
- IF it works only on some / only modular-like tasks THEN FAIL = CREDIT-DENSITY-TASK-LOCAL (the H_1006 unlock is structure-specific, not a general principle — report which task classes it covers).

## 3. measurement (2026-06-07 · g5 CODE-measured · no LLM self-judge · python3 -u streaming)

Probe `UNIVERSE/h1013_credit_density_general.py` (DenseSupGRU + curriculum + LM/mem-aug arms VERBATIM from h1006/h1003/h1000/h985; ONLY new = the 3 task generators + per-step state targets). Verdict `.verdicts/1013_credit_density_general/h1013.txt` (verbatim). 3 NEW state-bound families, capped length 36, width-rungs {16,32}, seeds CUT 3 (of H_1006's 6 — REPORTED; the dense per-step double-BPTT is pathologically slow on the running-max stream, ~5–8 min/cell at 6 seeds), {train 600 / test 300}, 40-epoch budget. dose {final-only, every-1}. aux head TRAINING-only; eval is final-label.

| family (accumulator algebra) | dose | rung | chance | currGRU | LM | memLM | gap | d | cap real? | dense cracks? |
|---|---|---|---|---|---|---|---|---|---|---|
| N1 kv-recall (associative-map) | final-only | 16 | 0.250 | 0.482 | 0.411 | 0.934 | 0.071 | 1.80 | — | — |
| N1 kv-recall | final-only | 32 | 0.250 | 0.504 | 0.442 | 1.000 | 0.062 | 1.63 | **YES** (final≈LM) | — |
| N1 kv-recall | every-1 | 16 | 0.250 | 0.479 | 0.411 | 0.934 | 0.068 | 1.36 | — | **NO** (≈LM) |
| N1 kv-recall | every-1 | 32 | 0.250 | 0.457 | 0.442 | 1.000 | 0.014 | 0.43 | — | **NO** (sep-rungs=[]) |
| N2 running-max (idempotent-monotone) | final-only | 16 | 0.125 | **1.000** | 0.419 | 0.988 | 0.581 | 37.89 | **NO** (final solves) | — |
| N2 running-max | final-only | 32 | 0.125 | **0.999** | 0.420 | 1.000 | 0.579 | 30.86 | **NO** | — |
| N2 running-max | every-1 | 16 | 0.125 | 0.997 | 0.419 | 0.988 | 0.578 | 37.68 | — | (n/a — no cap) |
| N2 running-max | every-1 | 32 | 0.125 | 1.000 | 0.420 | 1.000 | 0.580 | 31.00 | — | (n/a — no cap) |
| N3 stack-depth (bounded LIFO) | final-only | 16 | 0.125 | **0.966** | 0.506 | 1.000 | 0.460 | 10.33 | **NO** (final solves) | — |
| N3 stack-depth | final-only | 32 | 0.125 | **0.979** | 0.541 | 1.000 | 0.438 | 16.44 | **NO** | — |
| N3 stack-depth | every-1 | 16 | 0.125 | 0.999 | 0.506 | 1.000 | 0.493 | 19.05 | — | (n/a — no cap) |
| N3 stack-depth | every-1 | 32 | 0.125 | 1.000 | 0.541 | 1.000 | 0.459 | 30.28 | — | (n/a — no cap) |

Per-family classification: **CAPPED-CRACKED = []** · **CAPPED-but-SURVIVES = [N1 kv-recall]** · **NO-CAP = [N2 running-max, N3 stack-depth]**. All 3 families state-bound (mem-aug ≈ 1.0). Task classes covered: associative key-value recall (N1), idempotent-monotone running-max (N2), bounded-LIFO stack-depth (N3) — plus the modular ring counter (T3, H_1006) as the prior reference.

**Finding (🔴 FAIL = CREDIT-DENSITY-TASK-LOCAL):** per-step state supervision (the H_1006 lever) does NOT generalize. **N1 associative key-value recall** is the only NEW family that reproduces a real credit-density cap (final-label-only 0.48/0.50 ≈ LM 0.41/0.44), yet per-step supervision FAILS to crack it (dense 0.48/0.46 ≈ LM, sep-rungs=[]; the d≤1.8 is within-cap noise across near-identical low values, not a solve) — the per-step "answer-so-far for the queried key" signal is uninformative until the query key is revealed at the end, so dense gradient does not help an associative map the way it helps a scalar ring counter. **N2 running-max** (idempotent-monotone) and **N3 stack-depth** (bounded LIFO) present NO credit-density cap at all: a single final-step label already teaches them (0.97–1.00, d 10–38 vs the windowed LM), so per-step supervision is simply not needed — these accumulators are easy to learn from a sparse label despite being genuinely state-bound (mem-aug = 1.0). Net: of 3 distinct new accumulator algebras, 0 are "capped-and-cracked-by-dense". Credit-density is therefore a real but **BOUNDED** lever — specific to accumulators that are genuinely hard to learn from a sparse final label (the T3 modular ring counter) — **NOT a general long-horizon world-model principle** (closed-negative on generality, a_paper_negative_ok).

## 4. honest scope
Toy ($0 CPU, capacity-matched, multi-seed), a_scale_honest_scope / a_toy_scale_recheck. Per-step supervision needs per-step ground-truth state for each task (an extra label) — this tests the PRINCIPLE's reach, not a free-lunch deployment. New tasks chosen for distinct accumulator algebras (associative vs ordered-monotone vs bounded-stack) to probe generality. WALL-TIME CUT: seeds 6→3 (REPORTED — dense double-BPTT pathologically slow on the running-max stream); the cut endpoints (final-only vs every-1) are exactly what the falsifier needs (does dense crack a real cap?). The N1 cap held identical at the earlier 6-seed run (final 0.49/0.51, dense 0.48/0.46) before the cut — the ruling is seed-stable. Larger-budget / more-families / deeper-recurrence / production / real-corpus transfer UNVERIFIED. $0 CPU-local pure-numpy GRU (BPTT+Adam), NO torch; NOTHING on AKIDA (a_lane_akida_gpu_split).

## 5. sibling / xlinks
to [H_1006](./H_1006_dense_supervision.md) (🟢 the dense-sup crack of T3 modular this tests for generality — BOUNDS it to structure-specific, does NOT overwrite) · [H_1007](./H_1007_length_budget.md) · [H_1010](./H_1010_modulus_curriculum.md) · [H_1005](./H_1005_curriculum_scaleup.md) · [H_1000](./H_1000_gru_wm_t2t3.md) (task harness) · CWM domain · PROBE_CONVENTIONS.md
