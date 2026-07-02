# H_1641 — Cortical laminar microcircuit (L4→L2/3↺→L5/6 feedback) binding mouth, 303M — frozen pre-registration

**Card SSOT:** `HYPOTHESES/cards/H_1641_cortical_laminar_microcircuit_bind.md` (mechanism + ablation logic).

**Hypothesis:** A canonical 3-laminar cell (L4 two feedforward legs → L2/3 recurrent horizontal
associative layer with Carandini-Heeger divisive normalization → L5/6 feedback re-injection over K
settling iters) makes co-active leg-pairs **super-additive** (AND-like) where stacked feedforward
softmax (any depth, L24 failed) only re-mixes (OR-like). The settling installs a bound (conjunction)
representation into the trunk that lifts engine-native G1/G6 above the frozen wall.

## Serialization design (same .clm-safe pattern as H_1640)
The laminar microcircuit + its byte head are **TRAINING-ONLY** (auxiliary loss `L_bind`, λ=1.0). The
**production additive readout** `Conv1d(d→V)` is **retained** and serializes → `.clm` engine-native
loadable; the laminar binder is **dropped before serialize**. Binding is therefore a trunk-objective
pressure (the settled L2/3 conjunction must predict the next byte), shaping the shared trunk to carry
a pair-sensitive representation that CE alone never rewards.

## Arms (frozen — tune-to-green forbidden · card ablations)
- **arm**  : full laminar (recurrent L2/3 + Carandini-Heeger divisive-norm + L5→L4 feedback, K=4 iters).
- **nofb** : **ABLATION-1** L5→L4 feedback gain=0 → reduces to feedforward block → expect collapse.
- **noln** : **ABLATION-2** divisive-norm → plain LayerNorm → conjunctions no longer dominate
             singletons → expect INERT.
Matrix = {arm, nofb, noln} × seeds {7, 4302, 4303} = 9 runs. All arms: identical trunk init seed /
data / steps / production additive readout. Single variable = the binder mechanism.

## Arch (clm303_clean canon)
CLMConvMoE L=4 · d=3784 · E0=2→Emax=3 (mitosis mid-split) + savant golden-zone cusp anneal =
`cli/train.py --canon`. 4-cell register corpus proportional, val_frac=0.05, seq_len=1024, bs=8,
steps=2000, bf16. Frozen binder hyperparams: BIND_LAMBDA=1.0, LAM_K=4, LAM_DIM=64, DIVNORM_EPS=1.0.

## FROZEN bars (pre-registered VERBATIM · p7/c9)
- **Held-out gate:** every `.clm` passes held-out mirror-DESCENT (verify_clm_v2.py descent, math.log).
- **Primary G1 (H_1129 VERBATIM):** ∃k∈{2..5}: composed_distinct ≥ 2 AND > max_single AND coherent
  (kwr≥0.50). seed-robust majority ≥ 2/3.
- **SUPPORT** = `G1(arm) > G1(nofb)` AND `G1(arm) > G1(noln)` (bound-pair readout beats both ablations)
  with arm held-out DESCENT intact, seed-robust ≥2/3; card analog: arm lift ≥ 0.10, ablations INERT
  (ablated lift < 0.02).
- **NOT-SUPPORTED** = above unmet. All-arms G1=0 → INCONCLUSIVE-at-floor (honest, type-a).
- **G0/G2/G6** reported alongside (non-blocking).
- **tier ceiling:** engine-native `.clm` → `anima evaluate` terminal-eligible; py 2-prod = DIRECTIONAL
  post-py-retire → closure GREEN ⇒ hexa-confirm follow-on noted.

## Budget (a_wall_first, 1-line)
vast A40 CUDA-12 devel (~$0.5–0.9/hr). 9 runs × ~20min/arm ≈ 3h ≈ $2–4 (laminar K=4 settling adds
modest overhead). ckpt PULL before teardown (a_fire_recover_complete).
