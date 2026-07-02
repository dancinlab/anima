# H_1632 — Galois-closure concept-lattice binding mouth (FCA meet/join), 303M — frozen pre-registration

**Card SSOT:** `HYPOTHESES/cards/H_1632_galois_lattice_meet_bind.md` (mechanism + ablation logic).

**Hypothesis:** Binding as a Galois closure (Formal Concept Analysis) — extent/intent gates derived to
a closed (extent,intent) formal concept via AND-pool (soft-min / log-product) — is a MEET/conjunction
operator: a bound concept persists only if ALL its attributes hold, so distinct conjunctions stay
distinct through depth and idempotence prevents drift. Conv/attention OR-pool (weighted sum/softmax)
cannot represent 'red AND square AND left' so red-square + blue-circle ≈ red-circle (the recombination
failure). The conjunctive closure objective lifts engine-native G1/G6 above the frozen wall.

## Serialization design (.clm-safe, same pattern as H_1640/1641)
The closure layer + its byte head are **TRAINING-ONLY** (`L_bind`, λ=1.0). The idempotence-residual
monitor is **monitor-only** (p7). The **production additive readout** `Conv1d(d→V)` is **retained** and
serializes → `.clm`; the closure binder is **dropped before serialize**. Binding = a trunk-objective
pressure.

## Arms (frozen — tune-to-green forbidden · card ablations)
- **arm**    : meet-pool AND = soft-min (log-product of gates) → conjunction (the load-bearing op).
- **orpool** : **ABLATION** AND-pool → OR-pool (weighted sum / softmax, as attention) → conjunctive
               separation collapses → recombination to baseline (INERT). Isolates the MEET as
               load-bearing (card ablation logic).
- **k1**     : **ABLATION** 1 derivation step (no closure-to-fixpoint).
Matrix = {arm, orpool, k1} × seeds {7, 4302, 4303} = 9 runs. Identical trunk init seed / data /
steps / production readout; single variable = the binder mechanism.

## Arch (clm303_clean canon)
CLMConvMoE L=4 · d=3784 · E0=2→Emax=3 + savant cusp anneal. 4-cell register corpus proportional,
val_frac=0.05, seq_len=1024, bs=8, steps=2000, bf16.
Frozen binder hyperparams: BIND_LAMBDA=1.0, N_OBJ=16, N_ATTR=16, CLOSURE_K=2, ANDPOOL_BETA=8.0.

## FROZEN bars (pre-registered VERBATIM · p7/c9)
- **Held-out gate:** every `.clm` passes held-out mirror-DESCENT (verify_clm_v2.py descent, math.log).
- **Primary G1 (H_1129 VERBATIM):** ∃k∈{2..5}: composed_distinct ≥ 2 AND > max_single AND coherent.
  seed-robust majority ≥ 2/3.
- **CLOSURE** = G1 composed_distinct ≥ 2. 🟢 if met, else 🧱 NOT-SUPPORTED.
- **SUPPORT** = `G1(arm) > G1(orpool)` AND `G1(arm) > G1(k1)`, arm held-out DESCENT intact.
- **NOT-SUPPORTED** = above unmet. All-arms G1=0 → INCONCLUSIVE-at-floor (honest, type-a).
- **G0/G2/G6** reported alongside (non-blocking).
- **tier ceiling:** engine-native `.clm` → `anima evaluate` terminal-eligible; py 2-prod = DIRECTIONAL.

## Budget (a_wall_first, 1-line)
vast A40 CUDA-12 devel (~$0.5–0.9/hr). 9 runs × ~20min/arm ≈ 3h. ckpt PULL before teardown.
