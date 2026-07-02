# H_1640 — Conservative coupled-Hamiltonian (symplectic) binding mouth, 303M — frozen pre-registration

**Card SSOT:** `HYPOTHESES/cards/H_1640_hamiltonian_symplectic_bind.md` (mechanism + ablation logic).

**Hypothesis:** A conservative coupled-Hamiltonian binder (symplectic leapfrog, energy-conserving)
installs a *joint invariant of the two legs* into the trunk representation that plain CE never
rewards, lifting engine-native G1 recombination (and/or G6 ideation) above the frozen wall.

## Serialization design (differs from exp3 BindCLM = .clm-BLOCKED)
The Hamiltonian block + its byte head are **TRAINING-ONLY** (auxiliary loss `L_bind`, λ=1.0). The
**production additive readout** `Conv1d(d→V)` is **retained** for byte generation and is what
serializes → `.clm`. The binder is **dropped before serialize** → the `.clm` is a plain additive
CLMConvMoE = engine-native loadable (a_engine_native_learning engine-transform-to-fit). The binding
pressure is therefore a *trunk-objective* lever (consistent with the H_1602/H_1603 census that the G1
lever is the trunk objective, not the readout-op): the symplectic invariant must also predict the
next byte, forcing the shared trunk to carry a pair-sensitive (bound) representation.

## Arms (frozen — tune-to-green forbidden)
- **arm**  : full coupled-Hamiltonian aux (λ_couple=1.0, symplectic leapfrog K=10).
- **ctrl** : λ_couple=0 (decoupled oscillators) = card **ABLATION-1** (conjunction must vanish → INERT).
- **diss** : gradient-descent (dissipative) integrator instead of symplectic = card **ABLATION-2**
             (loses the orbit-coupling invariant → collapses to energy_settle).
Matrix = {arm, ctrl, diss} × seeds {7, 4302, 4303} = 9 runs. All arms: identical trunk init seed /
data stream / steps / production additive readout. Single variable = the binding mechanism.

## Arch (clm303_clean canon)
CLMConvMoE L=4 · d=3784 · E0=2→Emax=3 (mitosis mid-split) + savant golden-zone cusp anneal =
`cli/train.py --canon`. 4-cell register corpus (ko/en × general/sns) proportional, val_frac=0.05,
seq_len=1024, bs=8, steps=2000, bf16. Frozen binder hyperparams: BIND_LAMBDA=1.0, HAM_K=10,
HAM_DIM=64, HAM_DT=0.1, HAM_COUPLE=1.0.

## FROZEN bars (pre-registered VERBATIM · p7/c9)
- **Held-out gate (a_clm_gen_pipeline):** every `.clm` must pass held-out mirror-DESCENT
  (`verify_clm_v2.py descent`, math.log mirror, 4-cell) — model_ce < uniform(5.545) < shuffle, no
  overfit. FAIL = disqualified (not promoted).
- **Primary G1 (a7b/H_1129 VERBATIM):** ∃k∈{2,3,4,5}: `composed_distinct ≥ 2` AND `> max_single`
  AND coherent (kwr≥0.50). seed-robust majority ≥ 2/3.
- **SUPPORT** = `G1(arm) > G1(ctrl)` AND `G1(arm) > G1(diss)` (bound-pair readout beats both ablations,
  card frozen) with arm held-out DESCENT intact, seed-robust ≥2/3. Card cheap-test margin analog:
  arm lift ≥ 0.10 over controls AND ablations INERT (ablated lift < 0.02).
- **NOT-SUPPORTED** = above unmet. If all arms G1=0 (floor) → INCONCLUSIVE-at-floor (honest, type-a),
  not a clean refute.
- **G0/G2/G6** reported alongside (non-blocking).
- **tier ceiling:** engine-native `.clm` → `anima evaluate` (G0-G6) = terminal-eligible; py 2-prod eval
  is DIRECTIONAL post-2026-06-28 py-retire → if closure GREEN, hexa-confirm follow-on noted.

## Budget (a_wall_first, 1-line)
vast A40 CUDA-12 devel (~$0.5–0.9/hr). 9 runs × ~20min/arm @ A40 ≈ 3h ≈ $2–4. ckpt PULL before
teardown (a_fire_recover_complete).
