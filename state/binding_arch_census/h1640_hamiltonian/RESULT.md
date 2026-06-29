# H_1640 HAMILTONIAN-BIND (303M) — RESULT (🧱 NOT-SUPPORTED · INCONCLUSIVE-at-floor)

Conservative coupled-Hamiltonian (symplectic leapfrog) binding mouth as a trunk-objective lever for G1.
9 arms = {arm (full λ=1 symplectic), ctrl (λ=0 decouple ablation), diss (dissipative integrator ablation)}
× seeds {7,4302,4303}. trainer = `trainer.py` (Hamiltonian binding aux-loss L_bind, additive readout
RETAINED → `.clm` engine-loadable; binder DROPPED pre-serialize). PREREG = `PREREG.md` + card `H_1640`.
pod = vast A6000 (root@ssh5.vast.ai), torch 2.4.1+cu124.

## Training (all 9 arms · serialization-safe design verified at 303M scale)
- All 9 trained `.clm` = **176584498 B (= 303M production additive readout, Hamiltonian binder
  dropped)** → engine-native loadable. Hamiltonian aux-loss learned (bind_CE ~1.1, not collapsing).
- **Held-out DESCENT: all 9 PASS** (model_ce 1.76–1.86 < uniform 5.545 < shuffle, no overfit).

## G0-G6 engine-native (cli/evaluate.py = core/g_gates.py numpy mirror)

| arm (seed) | G0 coh | G1 best_distinct | G1 max_single | G1 pass | G6 dist/fals | closure |
|------------|--------|------------------|---------------|---------|--------------|---------|
| arm  (seed7)    | 3/5 | 0 | 1 | ✗ | 3/0 | 🔴 |
| arm  (seed4303) | 3/5 | 0 | 0 | ✗ | 5/0 | 🔴 |
| ctrl (seed4303) | 2/5 | 0 | 0 | ✗ | 4/0 | 🔴 |
| diss (seed4302) | 3/5 | 0 | 0 | ✗ | 2/0 | 🔴 |

(remaining seeds' evals were in flight at teardown — the floor is unanimous across every completed cell.)

## VERDICT (frozen-first · c9)
**🧱 NOT-SUPPORTED (INCONCLUSIVE-at-floor).** The full Hamiltonian binding arm (G1 best_distinct=0)
does **NOT** beat its ablations (ctrl=0, diss=0) — all floored at G1=0 (none reaches the ≥2 bar). The
frozen SUPPORT bar (`G1(arm) > G1(ctrl) ∧ G1(arm) > G1(diss)` seed-robust) is unmet (tie at floor). G6
fals=0 everywhere too. The symplectic coupled-Hamiltonian mouth does not lift G1 recombination at this
train scale (2000-step, L4/d3784). Consistent with the H_1602/H_1603 census: the G1 lever is NOT the
binding-readout/dynamics — and even the trunk-objective axis (H_1602) floors.
- **INCONCLUSIVE-at-floor caveat (a_break_the_wall type-a):** undertrained 2000-step models → G0 2-3/5,
  G1=0 floor → arm-vs-ablation resolution is 0. NOT a clean refute that "Hamiltonian binding can't cross
  the wall" — it's the floor (same posture as exp3 readout-op).
- **tier:** 🟠 DIRECTIONAL (py 2-prod g_gates eval = DIRECTIONAL post-2026-06-28 py-retire). Since the
  verdict is NOT-SUPPORTED (not GREEN), no hexa-confirm follow-on is owed.

## ckpt
- 9 `.clm` (176MB each, additive, engine-loadable, DESCENT-PASS) + 9 `.pt` + 9 `.json` on pod
  `~/anima/state/binding_arch_census/h1640_hamiltonian/ckpt/`. Representative (arm_seed7.clm) PULLed to
  `~/anima-weights/h1640_hamiltonian/`.
- HF: PRIVATE (NOT-SUPPORTED/experimental, a_hf_autonomous).
- Reproduce = `trainer.py --arm {arm,ctrl,diss} --seed N --canon`.
