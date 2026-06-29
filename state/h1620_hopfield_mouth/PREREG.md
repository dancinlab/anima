# H_1620 — Energy-settle attractor (Hopfield) binding mouth, 303M — frozen pre-registration

**Card SSOT:** `UNIVERSE/cards/H_1620_energy_settle_attractor.md` (mechanism + ablation logic).

**Hypothesis:** A bind head whose forward is a fixed-point relaxation on a symmetric-weight
quadratic energy E(z)=½zᵀWz − zᵀ(U_a a + U_b b) (modern-Hopfield / predictive-coding) settles to a
JOINT attractor that is deep only when BOTH leg clamps are simultaneously consistent (AND). This
installs a conjunction-sensitive trunk objective that lifts engine-native G1/G6 above the frozen
wall, where stacked feedforward conv/attn (any depth, L24 failed) can only ADD-mix the legs.

## Serialization design (.clm-safe, same pattern as H_1640/1641)
The energy block + its byte head are **TRAINING-ONLY** (auxiliary loss `L_bind`, λ=1.0). The
**production additive readout** `Conv1d(d→V)` is **retained** and serializes → `.clm` engine-native
loadable; the energy binder is **dropped before serialize**. Binding is a trunk-objective pressure
(the settled attractor must predict the next byte), shaping the shared trunk to carry a
pair-consistent representation that CE alone never rewards.

## Arms (frozen — tune-to-green forbidden · card ablations)
- **arm**  : full settle (K=8 GD steps, symmetric W).
- **k1**   : **ABLATION** K=1 → exactly one feedforward layer (= conv/attn baseline). Lift between
             k1 and arm is attributable ONLY to settling dynamics (card ablation logic).
- **asym** : **ABLATION** W not symmetrized → not a proper energy descent → joint-attractor
             guarantee broken → expect INERT/collapse.
Matrix = {arm, k1, asym} × seeds {7, 4302, 4303} = 9 runs. Identical trunk init seed / data / steps /
production readout; single variable = the binder mechanism.

## Arch (clm303_clean canon)
CLMConvMoE L=4 · d=3784 · E0=2→Emax=3 (mitosis mid-split) + savant golden-zone cusp anneal.
4-cell register corpus proportional, val_frac=0.05, seq_len=1024, bs=8, steps=2000, bf16.
Frozen binder hyperparams: BIND_LAMBDA=1.0, SETTLE_K=8, Z_DIM=64, ETA=0.5.

## FROZEN bars (pre-registered VERBATIM · p7/c9)
- **Held-out gate:** every `.clm` passes held-out mirror-DESCENT (verify_clm_v2.py descent, math.log).
- **Primary G1 (H_1129 VERBATIM):** ∃k∈{2..5}: composed_distinct ≥ 2 AND > max_single AND coherent
  (kwr≥0.50). seed-robust majority ≥ 2/3.
- **CLOSURE** = G1 composed_distinct ≥ 2 (per coordinator). 🟢 if met, else 🧱 NOT-SUPPORTED.
- **SUPPORT** = `G1(arm) > G1(k1)` AND `G1(arm) > G1(asym)` with arm held-out DESCENT intact.
- **NOT-SUPPORTED** = above unmet. All-arms G1=0 → INCONCLUSIVE-at-floor (honest, type-a).
- **G0/G2/G6** reported alongside (non-blocking).
- **tier ceiling:** engine-native `.clm` → `anima evaluate` terminal-eligible; py 2-prod = DIRECTIONAL
  → closure GREEN ⇒ hexa-confirm follow-on noted.

## Budget (a_wall_first, 1-line)
vast A40 CUDA-12 devel (~$0.5–0.9/hr). 9 runs × ~20–25min/arm (K=8 settle adds overhead) ≈ 3–4h.
ckpt PULL before teardown (a_fire_recover_complete).
