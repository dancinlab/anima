---
id: H_998
slug: perturbed-replay-consolidation
title: Does perturbed (noise-augmented) imagined replay buy ROBUSTNESS rather than information — adding NO clean-test accuracy (consistent with H_982🔴 no-free-lunch) but improving forecast on noisy/shifted test, i.e. dreaming as latent data-augmentation for invariance?
domain: cwm · imagine · consolidation · rem · robustness · replay
source: CWM 2nd slate — sharpens H_982🔴 (pure self-replay == idle) by asking where replay DOES pay off; Dreamer stochastic imagination + REM-dreaming + a_paper_negative_ok
exploration_method: E14 (substrate-native) + E5 (clean-vs-noisy test split + denoising replay)
verification_method: W2 (pre-registered no-clean-info + noisy-robustness falsifier) + g5 CODE-measured (no LLM self-judge, p7)
hexa_only: false
deterministic: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
status: measured
scope: ONE WAKE(n=6)→consolidation→test rung (a_scale_honest_scope); $0 CPU. NOT a forge binary.
sister: H_982 (REM self-replay==idle — the 🔴 this sharpens), H_976 (rollout=mitosis), H_981 (rollout consistency)
axes_seed: "replay is useless (H_982)" ⊥ "perturbed replay buys robustness not information" — locates the precise payoff of dreaming
verdict: 🟢 PASS — perturbed-replay buys robustness, not information: adds NO clean info (clean 0.090 ≥ idle 0.001, H_982-consistent) but on noisy test perturbed 0.815 beats verbatim 0.986 (d=1.88, p=3.2e-08). Toy single-rung, ladder OPEN.
---

# H_998 — perturbed-replay consolidation: dreaming buys robustness

## 0. Motivation

H_982🔴 found pure self-replay == idle: rehearsing WAKE data verbatim adds NO information absent from WAKE, so it cannot improve clean-test accuracy. This sharpens the closed-negative by asking WHERE replay DOES pay off. Biological REM and Dreamer's imagination are STOCHASTIC — replays are generative perturbations, not verbatim copies. The hypothesis: perturbed replay (training on noise-augmented imagined rollouts, with clean targets — a denoising objective) buys ROBUSTNESS/invariance to noisy test conditions, even though it adds no clean information (so it does not contradict H_982; it locates the payoff).

## 1. Hypothesis (one falsifiable claim)

Perturbed (noise-augmented) replay does NOT improve clean-test accuracy (consistent with H_982: no information added) but DOES improve forecast accuracy on noisy/shifted test conditions relative to verbatim/idle replay — dreaming is latent data-augmentation for invariance.

## 2. PRE-REGISTERED FALSIFIER (frozen 2026-06-06)

**Setup:** WAKE-train a delay-embedding WM on limited clean data (n=6). Two consolidation arms with the transition FROZEN (no new info): IDLE/verbatim (decoder refit on clean replays) vs PERTURBED (decoder refit on noise-augmented inputs with CLEAN targets — a denoising objective). Evaluate on CLEAN test and NOISY test (obs noise σ=0.30). 25 seeds.

**Measurement (g5 CODE-measured):**
- D1 = clean test: perturbed must NOT add clean information (perturbed clean error NOT below idle — any change is a regularization cost, never an info gain; H_982-consistent).
- D2 = noisy test: perturbed vs idle (Cohen d, Welch).

**Outcome rules (future conditional):**
- IF perturbed adds no clean info AND beats idle on noisy (d > 0.8, p<0.05) THEN PASS — replay buys robustness not information.
- IF perturbed does not beat idle on noisy THEN FAIL — replay buys nothing, even robustness (closed-negative).

## 3. Honest scope

Toy WAKE→consolidation→test rung (a_scale_honest_scope, #123-A). The "dreaming" is latent/obs-space Gaussian perturbation with a denoising target — a faithful but minimal model of stochastic replay. The verbatim baseline overfits the 6 clean trajectories to near-zero, so the clean-side criterion is framed honestly as "adds no clean information" (a clean cost is expected from any regularizer). Single rung, ladder OPEN. NOT a forge binary.

## measurement (2026-06-06 · g5 CODE-measured · substrate=CPU-mirror numpy)

Probe: `CWM/probes2/h998_perturbed_replay.py` · verdict: `.verdicts/998_perturbed_replay_consolidation/h998_perturbed_replay.txt`

| test | IDLE/verbatim | PERTURBED |
|---|---|---|
| CLEAN forecast error | 0.0009 | 0.0902 |
| NOISY forecast error (σ=0.30) | 0.9855 | **0.8149** |

D1 clean: perturbed adds NO clean info (0.090 ≥ idle 0.001 — H_982-consistent, no free lunch). D2 noisy: perturbed < idle, Cohen **d=1.88**, p=3.2e-08.

**VERDICT 🟢 PASS** — perturbed-replay buys ROBUSTNESS, not information: it adds no clean-test accuracy (confirming H_982🔴 — replay cannot inject information absent from WAKE) but significantly improves noisy-test forecast over verbatim replay. Dreaming is latent data-augmentation for invariance; this LOCATES where replay pays off and sharpens the H_982 closed-negative rather than overturning it (toy rung; ladder OPEN).
