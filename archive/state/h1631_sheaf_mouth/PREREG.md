# H_1631 — Sheaf-gluing binding mouth (local sections → global consistency), 303M — frozen pre-registration

**Card SSOT:** `UNIVERSE/cards/H_1631_sheaf_section_glue_bind.md` (mechanism + ablation logic).

**Hypothesis:** Binding as sheaf-gluing — node stalks with learned low-rank restriction maps glued via
K Jacobi steps toward sheaf-Laplacian consistency (minimize Σ‖R_i x_i − R_j x_j‖²) — makes an
assignment valid only if it glues into a consistent global section (the constraint compositional
semantics requires). Generic message-passing averages locally-conflicting choices and has no
obstruction object; the sheaf coboundary is an explicit (monitor-only) bind-failure signal. The
global-consistency objective lifts engine-native G1/G6 above the frozen wall.

## Serialization design (.clm-safe, same pattern as H_1640/1641)
The sheaf layer + its byte head are **TRAINING-ONLY** (`L_bind`, λ=1.0). The coboundary-norm readout
is **monitor-only, never added to loss** (p7 / a_train_inline_gauge). The **production additive
readout** `Conv1d(d→V)` is **retained** and serializes → `.clm`; the sheaf binder is **dropped before
serialize**. Binding = a trunk-objective pressure.

## Arms (frozen — tune-to-green forbidden · card ablations)
- **arm**   : full sheaf (learned low-rank restriction maps R, K=3 Jacobi consistency iters).
- **ident** : **ABLATION** R = identity → sheaf collapses to plain graph-Laplacian smoothing
              (= vanilla message passing) → recombination drops to baseline (INERT). Isolates the
              non-trivial restriction maps (role-typing) as the load-bearing element.
- **k1**    : **ABLATION** K=1 Jacobi step (no settling toward global consistency).
Matrix = {arm, ident, k1} × seeds {7, 4302, 4303} = 9 runs. Identical trunk init seed / data /
steps / production readout; single variable = the binder mechanism.

## Arch (clm303_clean canon)
CLMConvMoE L=4 · d=3784 · E0=2→Emax=3 + savant cusp anneal. 4-cell register corpus proportional,
val_frac=0.05, seq_len=1024, bs=8, steps=2000, bf16.
Frozen binder hyperparams: BIND_LAMBDA=1.0, N_NODES=4, STALK_DIM=32, RESTRICT_RANK=16, JACOBI_K=3,
JACOBI_ETA=0.5.

## FROZEN bars (pre-registered VERBATIM · p7/c9)
- **Held-out gate:** every `.clm` passes held-out mirror-DESCENT (verify_clm_v2.py descent, math.log).
- **Primary G1 (H_1129 VERBATIM):** ∃k∈{2..5}: composed_distinct ≥ 2 AND > max_single AND coherent.
  seed-robust majority ≥ 2/3.
- **CLOSURE** = G1 composed_distinct ≥ 2. 🟢 if met, else 🧱 NOT-SUPPORTED.
- **SUPPORT** = `G1(arm) > G1(ident)` AND `G1(arm) > G1(k1)`, arm held-out DESCENT intact.
- **NOT-SUPPORTED** = above unmet. All-arms G1=0 → INCONCLUSIVE-at-floor (honest, type-a).
- **G0/G2/G6** reported alongside (non-blocking).
- **tier ceiling:** engine-native `.clm` → `anima evaluate` terminal-eligible; py 2-prod = DIRECTIONAL.

## Budget (a_wall_first, 1-line)
vast A40 CUDA-12 devel (~$0.5–0.9/hr). 9 runs × ~25min/arm (K=3 Jacobi over edges adds overhead) ≈ 4h.
ckpt PULL before teardown.
