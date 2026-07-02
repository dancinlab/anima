# H_9046 — γ TRAINED constructive combiner (H_9043 follow-on): the only untried recomb lever = FLOOR

- **tier:** 🧱 DIRECTIONAL-FLOOR (numpy β-extract + torch combiner = DIRECTIONAL, not engine-native) — harness POWERED (oracle Δ+0.45), FLOOR VALID
- **slug:** `gamma_trained_constructive_bind`
- **parents:** H_9043(vadapt_combine/unbind = FIXED algebraic HRR op, capability floor cos −0.203; stated only-remaining lever = "trained constructive-bind γ") · H_9026(real-manifold, but trained only a LINEAR readout on a FIXED hrr feature — combiner never trained) · H_1840(γ FAIR-gate on RANDOM target → MEASUREMENT-INVALID per H_6166) · H_6166/H_6167(recomb=task-structure-bound, random full-rank target unlearnable) · frame-shift Lane(VAdaptField=결합기 없음)

## frame — the genuinely-untried cell (check-ledger, c9)

H_9043 built `vadapt_combine`/`vadapt_unbind` = **fixed algebraic** circular-conv HRR → recoverability GREEN but held-out CAPABILITY floor (cos −0.203 < chance). H_9026 tested the REAL 303M manifold but its "trained W_bind" trained **only a linear ridge readout on a FIXED hrr feature** — the combiner interaction weights were never learned. H_1840 trained a bilinear bottleneck but on a **random full-rank target** (later flagged MEASUREMENT-INVALID, H_6166: random target → held-out info-theoretically independent = unlearnable).

The ONE genuinely-untried lever = a **LEARNED / parameterized combiner whose interaction weights are trained end-to-end** under a recombination-reward objective, on the REAL 303M β manifold, with a STRUCTURED held-out pair split (concepts each seen individually, the PAIR unseen → systematic generalization possible in principle). = the "γ trained-constructive-bind" H_9043 pointed to.

## method (`state/9046_gamma_trained_bind/trainer.py`, aiden pool $0, DIRECTIONAL)

- **REAL manifold:** β = clm303 trunk penultimate mean-pool L2-unit from `py303_full.clm` (d=3784, L=4, E=3, V=256) — byte-faithful numpy mirror of `core.clm_decode` (same β embedding as H_1822/H_9026). 96 ko+en concepts; target `T_ij = penult("c_i c_j")` = the manifold's OWN composed-phrase rep. 3000 pairs.
- **PCA-24** (var-explained 0.644) → the **identifiable regime** (operator DOF ≪ #train-pairs; ~1800 train pairs).
- **arms:** `add` = ridge linear readout on concat[a,b] (H_9026 baseline); `bilinear` = LEARNED low-rank bilinear `c=Wout@((Ua)⊙(Vb))` R=48 (γ, trained multiplicative interaction); `mlp` = LEARNED 2-layer MLP over [a,b] hidden=192 (most-expressive learned combiner). torch Adam + weight-decay + cosine loss.
- **frozen bars (pre-registered, no tune-to-green):** COMPOSE=0.30, DELTA_BAR=+0.15, TRAIN_FIT_MIN=0.60. held-out EARNED shuffle-controlled (right partner cos>0.30 ∧ shuffled-partner ≤0.30). PRIMARY Δ = earned(combiner) − earned(add), GREEN-dir iff n(Δ≥+0.15)≥3/5 ∧ no_regress. Plus ablation (⊙→additive under SAME weights = INERT test), train-fit oracle, additivity diagnostic.
- **POWER control (same frozen metric):** synthetic rank-6 bilinear oracle (120 concepts, dim-24, 3000 pairs) → bilinear Δ **+0.45**, 3/3, earned 0.53 vs add 0.08, ablation collapses to 0.09. **Harness DETECTS held-out compositional generalization when a real operator exists** → the real FLOOR is powered, not underpowered.

## result (`state/9046_gamma_trained_bind/r_9046.log`, 5 seeds)

| metric | value |
|--------|-------|
| **additivity diagnostic** | mean cos(T_ij, unit(a_i+b_j)) = **0.861** ⇒ 303M trunk composes phrases ~ADDITIVELY at penult layer |
| oracle train-fit (best learned, every seed) | ≥0.60 = **True** (add .965 · bilinear .95 · mlp .995) → task solvable, NOT undertrained |
| **PRIMARY bilinear − add** Δ/seed | [0.025, 0.032, 0.027, 0.027, 0.032] · n(Δ≥+0.15)=**0/5** |
| **PRIMARY mlp − add** Δ/seed | [0.032, 0.026, 0.030, 0.035, 0.024] · n(Δ≥+0.15)=**0/5** |
| held-out cos margin pr / ps | add .96/.65 · bilinear .93/.64 · mlp .99/.64 (combiner adds ~0 extra partner-discrimination) |
| ablation (⊙→additive, same weights) | bilinear .03–.10 ≈ earned · mlp additive-input ≥ mlp = INERT (multiplicative interaction NOT causal) |

## verdict (c9) — 🧱 FLOOR, valid & mechanistically explained

**A TRAINED constructive combiner (bilinear γ + MLP) does NOT beat trained additive on held-out real-manifold compositional generalization** — Δ ≈ +0.03 weak-consistent (same sub-threshold pattern as H_9026's fixed-op [.12,.12,.08,.07,.09]), 0/5 hits at every arm. The only genuinely-untried recomb lever is exhausted.

**Root cause (deeper than DPI):** additivity diagnostic **0.86** — the 303M manifold composes phrases ~additively at the penult layer, so additive readout is near-optimal and there is essentially **no multiplicative/constructive structure for a trained bind to exploit**. Ablation confirms the multiplicative interaction is INERT; the powered oracle confirms the harness WOULD detect a real operator (Δ+0.45). This is the mechanistic explanation of the additive-readout floor across H_1834/H_1816/H_9026/H_9043: it's not that combiners are too weak — the substrate composition itself is additive.

## wired

`DIRECTIONAL (not engine-native)` — numpy β-extract + torch combiner training = DIRECTIONAL per `a_engine_native_learning` (grep `import torch|numpy` → present). **NO wire-in** (`a_verified_must_wire`): capability floors, so there is nothing to route into emit/decode. No trained-weight ckpt worth pulling (tiny heads, DIRECTIONAL); β extraction regenerable from `py303_full.clm` in ~4min (cache `beta_cache.npz` on aiden, regenerable, not pulled — deterministic).

## follow-on
- **Recomb/γ axis CLOSED.** trained-constructive-bind was the last untried lever (H_9043); it floors and the additivity diagnostic explains why. Do NOT re-fire operator/readout/decode-side recomb levers ([[fleet-g1g6-nativemouth-dpi-convergence]], [[check-ledger-before-lever-fire]]). Only residual = trunk **recomb-OBJECTIVE** (H_1602, GPU cost-gated) — but even that must overcome an additive penult manifold.
- Productive axis = frame-shift (재조합≠능력), substrate-native capability op-building ([[frameshift-substrate-gaps-vs-recombination-wall]]).

## artifacts
- `state/9046_gamma_trained_bind/trainer.py` (γ trainer + powered oracle + additivity diagnostic) · `state/9046_gamma_trained_bind/r_9046.log` (5-seed real run verbatim)
