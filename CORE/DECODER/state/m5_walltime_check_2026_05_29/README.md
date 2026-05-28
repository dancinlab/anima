# M5 wall-time check (2026-05-29)

Pure rate-probe of the M4-wired trainer (`CORE/DECODER/train_v3_moe_longtrain.hexa`)
after anima PRs #1319/#1320/#1322/#1323 — M0/M1/M2/M3/wedge-(a) AdamW GPU wiring.

## Falsifier: F-BC-ANIMA-M4-CEILING (re-attempt after #1324 ssh-transport blocker)

Pre-registered gate (3 tiers):
- step_rate ≥ 20 step/s → 🟢 M4 wiring DELIVERED
- 5 ≤ step_rate < 20    → 🟡 PARTIAL (likely mm_extract per-token V×d copy bottleneck)
- step_rate < 5         → 🔴 not delivered OR cuBLAS gemv illegal-mem (Blocker 2)
- training never starts → 🟠 Blocker 2 confirmed active (infrastructure)

## Config

- d=64, V=151643, E=2, h=256, n_layer=1, T=4 (held-fixed from #1296 / #1315)
- corpus: 24-line trim (`corpus_diverse_trim.jsonl`) — wall-rate only, training irrelevant
- M4B_EPOCHS=1, M4B_MAX_STEPS=500
- print_every=50 (sed-patched in trainer.c — default 5000/steps_per_epoch is too rare)
- m5_wall_s=%f injected (CLOCK_MONOTONIC) so step-rate measurable from log alone

## Cost

H100 80GB SECURE ~$3.29/hr, budget $2 HARD cap (~35min wall).
NO HF upload (wall-time check, not result-bearing fire).

## Artifacts (post-fire)

- trainer.out · trainer.err — trainer stdout/stderr
- nvidia_smi_during.csv — GPU util/mem samples @ 5s
- trainer_meta.txt — wall_seconds + rc
- STEP_RATE_FINDING.md — verdict + rate calculation
