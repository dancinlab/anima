# H_1641 LAMINAR-BIND (303M) — RESULT (🧱 NOT-SUPPORTED · INCONCLUSIVE-at-floor)

Cortical laminar microcircuit (L4 two legs → L2/3 recurrent + Carandini-Heeger divisive-norm settle
↺ → L5/6 feedback, K=4 iters) binding mouth as a trunk-objective lever for G1. 9 arms = {arm (full
laminar), nofb (L5→L4 feedback gain=0 ablation), noln (divisive-norm→plain LayerNorm ablation)} ×
seeds {7,4302,4303}. trainer = `trainer.py` (laminar binding aux-loss L_bind, additive readout RETAINED
→ `.clm` engine-loadable; binder DROPPED pre-serialize). PREREG = `PREREG.md` + card `H_1641`.
pod = vast A6000 (root@ssh5.vast.ai), torch 2.4.1+cu124.

## Training (all 9 arms · serialization-safe design verified at 303M scale)
- All 9 trained `.clm` = **176584498 B (= 303M production additive readout, laminar binder dropped)**
  → engine-native loadable. Laminar aux-loss learned (bind_CE ~1.3–4.4; the divisive-norm settling
  readout is harder to drive than the Hamiltonian's, but the main next-byte CE descends fine).
- **Held-out DESCENT: all 9 PASS** (F-CLM-DESCENT=1, model_ce 1.80–1.83 < uniform 5.545 < shuffle).

## G0-G6 engine-native (cli/evaluate.py = core/g_gates.py numpy mirror)

| arm (seed) | G1 best_distinct | G1 max_single | G1 pass |
|------------|------------------|---------------|---------|
| **arm (full laminar)** seed7 | **0** | 0 | ✗ (FLOOR) |

(nofb/noln seed7 ablation evals were still running at teardown — the H_1641 laminar eval is
pathologically slow on this CPU, ~30–40 min/clm vs ~20 min for the other models; the arm `.clm` itself
floors at G1=0, so it cannot exceed its ablations even before they complete. ckpts PULLed → ablation
evals are re-runnable locally; see follow-on.)

## VERDICT (frozen-first · c9)
**🧱 NOT-SUPPORTED (INCONCLUSIVE-at-floor).** The full laminar microcircuit binding arm floors at G1
best_distinct=0 (FAIL, < the ≥2 bar). The frozen SUPPORT bar (`G1(arm) > G1(nofb) ∧ G1(arm) >
G1(noln)`) cannot be met because the arm is already at the floor (0). The Carandini-Heeger
divisive-norm recurrent-settling mouth does not lift G1 recombination at this train scale
(2000-step, L4/d3784). Consistent with H_1640 (Hamiltonian) and H_1602 (objective) — and the prior
exp3 (Hadamard readout) and H_1812/1814/1816 binding-campaign: **no binding-readout/dynamics moves G1;
the wall is structural at this undertrained scale.**
- **INCONCLUSIVE-at-floor (a_break_the_wall type-a):** 2000-step undertrained → G1=0 floor → arm-vs-
  ablation resolution is 0. NOT a clean refute that "laminar binding can't cross the wall" — it's the
  floor.
- **tier:** 🟠 DIRECTIONAL (py 2-prod g_gates eval = DIRECTIONAL post-2026-06-28 py-retire). NOT-SUPPORTED
  so no hexa-confirm follow-on owed.

## ckpt + follow-on
- 9 `.clm` (176MB each, additive, engine-loadable, DESCENT-PASS) + 9 `.pt` + 9 `.json`. Representatives
  **arm_seed7 + nofb_seed7 + noln_seed7 PULLed** to `~/anima-weights/h1641_laminar/`.
- HF: PRIVATE (NOT-SUPPORTED/experimental, a_hf_autonomous).
- **Follow-on (local, $0):** nofb_seed7/noln_seed7 G0-G6 evals re-run on the pulled ckpts via
  `cli/evaluate.py` to complete the arm-vs-ablation table (expected: also floored). The arm's G1=0
  already settles the NOT-SUPPORTED verdict.
- Reproduce = `trainer.py --arm {arm,nofb,noln} --seed N --canon`.
