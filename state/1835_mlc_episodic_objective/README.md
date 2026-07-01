# H_1835 — MLC episodic-objective toy probe

DIRECTIONAL numpy mirror (torch/gauge_lib FORBIDDEN) testing whether MLC (Lake & Baroni,
Nature 2023) — casting the recombination objective as an **episodic task distribution**
(per-episode grammar permutation + in-context study examples) rather than an additive loss
term — lifts a toy compositional-generalization metric above the plain-next-byte-CE floor.

- `mlc_episodic_probe.py` — from-scratch reverse-mode autograd + Adam, 2-block causal
  transformer, gradcheck PASS (4.45e-6). 2 arms × 3 seeds, EQUAL compute. Run: `python3 mlc_episodic_probe.py [steps]`.
  - ARM A = plain-CE, static grammar, no study (control = current anima objective).
  - ARM B = MLC episodic (permuted grammar + in-context isolation study).
  - Task = canonical SCAN "dax" novel-primitive-in-composition. metric = held-out composed_distinct/4.
- `run_4000.log` — frozen measurement (steps=4000). VERDICT 🧱: A=0/0/0 (seen_acc 9/9 = SCAN
  wall cleanly reproduced), B=0/0/0 (seen_acc 4-6/9 = under-fit at toy budget).
- `_diag_B_long.py` / `diag_B_long.log` — exploratory B-only diagnostic (OUTSIDE frozen bar):
  more compute — RESULT: at 12000 steps B reaches seen_acc 9/9 (masters in-context composition) but held composed_distinct STILL 0/4 = clean transfer failure, resolves the under-fit confound.

Frozen bar (pre-registered): 🟢 iff B_composed_distinct>=3 AND B>A AND seeds{7,4302,4303}
unanimous. Result: not met → 🧱. DIRECTIONAL only, not terminal (a_engine_native_learning);
toy != production (a_toy_scale_recheck); MLC touches architecture too (not pure objective axis).
