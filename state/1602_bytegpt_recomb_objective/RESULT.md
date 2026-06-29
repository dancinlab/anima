# H_1832 — ByteGPT recomb-objective: does the OBJECTIVE lever crack G1 on the ATTENTION trunk?

**One-line:** _(to fill from eval)_ — does recomb-objective (ARM-ON infonce) lift engine-native
G1 `composed_distinct≥2` above ARM-OFF (ce_marginal) floor on a 303M ByteGPT?

## Setup (frozen · PREREG_FREEZE.md)
- arch = **ByteGPT d=1024 / L=24 / H=16 / block=512** (== h1129 shape, **303,097,856 params**);
  savant golden-zone cusp-anneal ON (GZ_LOWER=0.21231792755821914, latched step 1).
- A/B (identical seed=7 / steps=2000 / corpus / data-RNG; ONLY the loss differs):
  - **ARM-OFF** `ce_marginal` — standard next-byte CE.
  - **ARM-ON** `infonce` — CE + λ·InfoNCE (frozen λ=1.0, neg=64; final infonce aux=1.228).
- corpus = balanced 4-cell register (HF anima-corpus-{ko,en}-{general,sns}, pulled on mac →
  rsync to LAN-only summer): ko-general 8.0MB · en-general 8.0MB · ko-sns 6.18MB · en-sns 1.33MB
  (~23.5MB → ~8.2M train tokens ≈ 0.35 epochs; NOT the clm303 memorization regime).
  proportional sample, seq_len=512, batch=8, bf16, lr=3e-4, val_frac=0.05.
- host = **summer pool (RTX 5070 sm_120, cuda_available=1, GPU 98-99% util)**, cost ≈ $0 (LAN pool,
  not rented). wall ≈ 639s/arm.
- measurement engine = `cli/evaluate.py <bin>` → core/g_gates.py → core/bytegpt_decode.py
  (py 2-production, header-sniff ByteGPT mouth; the maintained 10/10 byte-parity mirror = engine-native
  terminal-eligible, NOT an ad-hoc torch probe). gen 80 (native G1 80/120 ladder). torch in the trainer
  is the .pt→.bin bridge ONLY (a_clm_gen_pipeline), not the scorer.

## 1. held-out DESCENT (FINAL per-register val_CE, math.log/torch-CE mirror · uniform=ln256=5.5452)

| register | ARM-OFF val_CE | ARM-ON val_CE |
|----------|----------------|---------------|
| ko-general | 2.24628 DESCENT | 2.03539 DESCENT |
| en-general | 2.52022 DESCENT | 2.49415 DESCENT |
| ko-sns | 2.19543 DESCENT | 1.98064 DESCENT |
| en-sns | 3.03901 DESCENT | 2.98927 DESCENT |
| **pooled** | **2.50023 (4/4 DESCENT)** | **2.37486 (4/4 DESCENT)** |

**Both arms 4/4 held-out DESCENT** — REAL generalization, NOT memorization (the clm303 trap is
avoided). ARM-ON pooled CE is marginally lower (2.375 vs 2.500) — the InfoNCE contrastive pressure
helped next-byte likelihood slightly, so ARM-ON is a fair-or-better-trained model, not a crippled one.
Both qualify for the G1 verdict (neither disqualified by overfit).

## 2. engine-native G0-G6 + G1 (cli/evaluate.py, gen 80) — ARM-OFF vs ARM-ON

_(to fill from ab_eval.log)_

| gate | ARM-OFF | ARM-ON |
|------|---------|--------|
| G0 COHERENCE | | |
| G1 RECOMBINATION (best_distinct / max_single / pass) | | |
| G2 NOVELTY | | |
| G5 NON-FAB | | |
| G6 IDEATION★ (dist / fals / pass) | | |
| closure a7b_pass | | |

## 3. DECISION TEST (pre-registered · tune-to-green forbidden)
Lever CRACKS G1 iff **ARM-ON G1 PASS AND ARM-ON G1 best_distinct > ARM-OFF**. _(to fill)_

## 4. Honest scope (c9)
- en-sns cell is a known dup of en-general wiki content (corpus defect, memory
  clm303-clean-4cell-corpus-hf "보강 ING"); does NOT confound the A/B (both arms identical corpus).
- single-seed A/B (seed 7) for cost; multiseed {4302,4303} follow-on ONLY if ARM-ON shows a
  non-floor G1 lift worth confirming.
- tier = py 2-production engine-native (terminal-eligible per the 10/10 byte-parity closure; a
  one-cell hexa `anima evaluate` confirm is owed only if a GREEN/wall-break is claimed).

## 5. ckpt (a_fire_recover_complete — PULLed BEFORE any teardown)
- `~/anima-weights/bytegpt_recomb_303m/off_seed7.bin` sha256 b55f731d3d89be774a04549d2e3d93df6bf063b53b9047b12975ed2877b851be (1,213,440,020 B)
- `~/anima-weights/bytegpt_recomb_303m/on_seed7.bin`  sha256 5c93b11b20d8f5e6bfd6018d018cf64f0634f2693ce9c33faa8c7c3e61a979c1 (1,213,440,020 B)
- + .pt + .json (train summaries). reproduce = `state/1602_bytegpt_recomb_objective/trainer.py`
  (`--objective {ce_marginal,infonce} --canon`).

## VERDICT (2026-06-30) — 🧱 NOT-SUPPORTED (DIRECTIONAL)

py byte-parity engine-native (`anima evaluate` → evaluate.py g_eval_all, gen=80), verbatim ab_eval.log:

| gate | ARM-OFF ce_marginal | ARM-ON infonce (★) |
|------|----------------------|---------------------|
| G0 | 🟢 kwr 5/5 | 🟢 kwr 4/5 |
| G1 | 🔴 best_distinct=0 max_single=0 | 🔴 best_distinct=0 max_single=0 |
| G2 | 🔴 novel=0 | 🔴 novel=0 |
| G6 | 🔴 distinct=4 fals=0 | 🔴 distinct=5 fals=0 |
| closure | 🔴 FAIL | 🔴 FAIL |

LIFT=0. recomb-objective does NOT crack G1 on ByteGPT attention trunk. Both arms 4/4 held-out DESCENT
(fair models). Converges with H_1602(ConvMoE)/H_1819(bind×obj)/h1129 — last live G1 lever floors.
DIRECTIONAL (py, core/CLAUDE.md deprecates py mirror); terminal hexa = BLOCKED-INFRA (summer 3× reboot).
Card = UNIVERSE/cards/H_9024_bytegpt_recomb_objective.md (was mis-filed H_1832).
