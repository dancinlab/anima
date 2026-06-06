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
status: pre-registered (unmeasured)
verdict: PENDING-MEASUREMENT (no verdict token until measured)
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

## 3. honest scope
Toy ($0 CPU, capacity-matched, multi-seed), a_scale_honest_scope. Per-step supervision needs per-step ground-truth state for each task (an extra label) — this tests the PRINCIPLE's reach, not a free-lunch deployment. New tasks chosen for distinct accumulator algebras (commutative vs ordered vs associative) to probe generality, not similarity.

## 4. sibling / xlinks
to [H_1006](./H_1006_dense_supervision.md) · [H_1007](./H_1007_length_budget.md) · [H_1010](./H_1010_modulus_curriculum.md) · [H_1005](./H_1005_curriculum_scaleup.md) · CWM domain · PROBE_CONVENTIONS.md
