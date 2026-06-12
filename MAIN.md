# MAIN — anima program progress hub

@goal: drive the two LIVE anima tracks to closure — (A) the MITOSIS-ENGINE research
domain (substrate science) and (B) the 7B PASS fire (a7b_pass G0–G4). "Running MAIN"
= check + advance BOTH tracks, log every step to `MAIN.tape`.

## Track A — research · MITOSIS-ENGINE domain
ref → **`domains/MITOSIS-ENGINE.md`** (+ `MITOSIS-ENGINE.tape` log · `.easy.md`)
Substrate-unique clusters LANDED (all frozen-falsifier · $0 · g5/p7):
- criticality: σ≈1 branching (H_1153) · faithful-Φ peaks at criticality (H_1158, holds n=7/8 H_1165) · mitosis drives σ→1 (H_1161 near-miss, F2+F3 pass)
- inference = mitosis = learning (H_1159 / H_1159b capacity self-tunes)
- super-additivity "1+1>2": peaks at criticality (H_1167 🟢, stricter than φ) · surface-gated on data (H_1168 🟡 / H_1169 🔴 / H_1170 🔴 cross-modal collapse)
- life/evolution probes (H_1171–1177): **the level decides** — organism self-repair 🟢 + population×generations evolution 🟢; cell-level death/metabolism/membrane/selection/competition 🔴
Open rungs: live-engine adaptation curve · tick-on-decode-metric · kosmos lane self-tune · H_1136 sleep re-test post-H_1131 anchor fold.

## Track B — production · 7B PASS fire (a7b_pass)
pod → RunPod **uq71dp0ob6fd9r** `h1141-7b-pass` · 1×H100 NVL · $2.59/hr · harness `h1141_7b_pass_attempt.py`
completion SSOT = **`/7B_PASS_CONDITIONS.md`** (PASS iff G0∧G1∧G2∧G3∧G4 on ONE ckpt)

Status (2026-06-12, step 8000 · val_ce 1.2015 ↓ · 543min):
| gate | state | evidence |
|------|-------|----------|
| G0 COHERENCE | ✅ PASS (stable) | 5/5 kwr≥0.50 @ step 6000 AND 8000 |
| G1 RECOMBINE | ⚠ MARGINAL | flickers 2/5↔3/5 around the ≥3 bar — PASS@6500 [en ja ko], FAIL@8000 [en ko, ja dropped]; not yet stable |
| G2 / G3 / G4 | ⏳ unseen | not yet evaluated in-log |

Milestone safety: best.pt @ step6500 (G0✅+G1✅ snapshot) → HF PRIVATE `dancinlab/anima-clm-7b-h1141-g1pass-step6500` (uploaded). Watcher (PID 1123) auto DONE→HF-verify→self-teardown.
**NOT a7b_pass-complete** — G1 unstable + G2–G4 unseen. Let training converge; re-check all gates at DONE.

## How to run MAIN
1. (A) advance a MITOSIS-ENGINE open rung as a $0 toy micro-exp (frozen falsifier, reuse h1159b).
2. (B) monitor the 7B fire — `/pod pods` · ssh tail `h1141.log` · re-check G0–G4 at convergence; harvest+HF on DONE (a_fire_recover_complete).
3. log the step to `MAIN.tape`.
