# H_1630 — Tropical (max-plus) semiring binding mouth, 303M — frozen pre-registration

**Card SSOT:** `UNIVERSE/cards/H_1630_tropical_semiring_bind.md` (mechanism + ablation logic).

**Hypothesis:** Replacing the ring (+,×) with the tropical semiring (max,+) gives a hard, selective
winner-take-one role→filler assignment (Viterbi-style) that survives depth without superposition
crosstalk, where ring-based binders (outer-product, conv, attention) blend fillers until distinct
role-filler pairs become inseparable (the observed fals=0). The selective assignment installs a
conjunction-preserving trunk objective that lifts engine-native G1/G6 above the frozen wall.

## Serialization design (.clm-safe, same pattern as H_1640/1641)
The tropical head + its byte readout are **TRAINING-ONLY** (`L_bind`, λ=1.0). The **production
additive readout** `Conv1d(d→V)` is **retained** and serializes → `.clm` engine-native loadable; the
tropical binder is **dropped before serialize**. Binding = a trunk-objective pressure.

## Arms (frozen — tune-to-green forbidden · card ablation = single temperature knob)
- **arm**  : tropical T=0.1 (near-hard max-plus, selective winner-take-one).
- **soft** : **ABLATION** T=1.0 (= log-sum-exp / softmax = ordinary attention) → blend, crosstalk →
             expect INERT (selectivity lift vanishes).
- **mid**  : T=0.5 (intermediate, monotonicity check — lift must DECREASE as T→1).
Matrix = {arm, soft, mid} × seeds {7, 4302, 4303} = 9 runs. Identical trunk init seed / data /
steps / production readout; ONLY variable = the semiring temperature T.

## Arch (clm303_clean canon)
CLMConvMoE L=4 · d=3784 · E0=2→Emax=3 + savant cusp anneal. 4-cell register corpus proportional,
val_frac=0.05, seq_len=1024, bs=8, steps=2000, bf16.
Frozen binder hyperparams: BIND_LAMBDA=1.0, N_ROLES=8, N_FILLERS=16, FILLER_DIM=64, ARM_TEMP={arm:0.1,
soft:1.0, mid:0.5}.

## FROZEN bars (pre-registered VERBATIM · p7/c9)
- **Held-out gate:** every `.clm` passes held-out mirror-DESCENT (verify_clm_v2.py descent, math.log).
- **Primary G1 (H_1129 VERBATIM):** ∃k∈{2..5}: composed_distinct ≥ 2 AND > max_single AND coherent.
  seed-robust majority ≥ 2/3.
- **CLOSURE** = G1 composed_distinct ≥ 2. 🟢 if met, else 🧱 NOT-SUPPORTED.
- **SUPPORT** = `G1(arm) > G1(soft)` AND monotone decrease arm→mid→soft, arm held-out DESCENT intact.
- **NOT-SUPPORTED** = above unmet. All-arms G1=0 → INCONCLUSIVE-at-floor (honest, type-a).
- **G0/G2/G6** reported alongside (non-blocking).
- **tier ceiling:** engine-native `.clm` → `anima evaluate` terminal-eligible; py 2-prod = DIRECTIONAL.

## Budget (a_wall_first, 1-line)
vast A40 CUDA-12 devel (~$0.5–0.9/hr). 9 runs × ~20min/arm ≈ 3h. ckpt PULL before teardown.
