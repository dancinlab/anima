# FREEZE2 — factored-headroom screen (pre-registered before run)

Why a 2nd world: the pre-registered S_4 pure-group screen (FREEZE.md) FAILED with **all four
arms at held-out chance** (~0.04 = 1/24, train=1.000). Pure S_4 composition is not grokkable by a
concat-MLP in 4000 steps for ANY loss => zero headroom => cannot ISOLATE gamma's effect (result =
INCONCLUSIVE-at-floor, NOT a clean gamma falsification). This 2nd world adds headroom so gamma
CAN discriminate if it ever does. This is calibration, NOT a retry-until-green of FREEZE.md — the
S_4 FAIL stands verbatim; this is a distinct bar on a distinct (learnable) world.

## World = latent-factor NON-SYMMETRIC interaction table (single symbol set, order matters)
- N=24 symbols, each with a hidden factor f(s) in {0..P-1}, P=6 (4 symbols/factor, shuffled).
- target(a,b) = R[f(a), f(b)], R a random NON-symmetric P x P -> C=12 table. Order-sensitive:
  R[fa,fb] != R[fb,fa] on ~5/6 of factor-pairs. Non-commutativity is a WORLD property (in R),
  NOT a planted input feature; model must INFER f from the symbol id + learn R (recombination =
  generalize to unseen (a,b) whose factor-pair was seen via OTHER symbols).
- Train = 40% of 576 pairs; every symbol AND every (fa,fb) factor-pair covered in train (=> the
  held-out generalization is possible in principle => headroom for all arms).
- ADD arm is order-blind (E[a]+E[b] symmetric) => provably <=0.5 on order-sensitive factor-pairs
  but can read marginals => partial floor with headroom (the DPI floor with a visible ceiling).
- SHUFFLE control = per-pair random target (destroys factor structure) => no arm can generalize.

Arms + gamma mechanism identical to FREEZE.md (ADD / CE / G_trunk / G_read).

## Frozen bar (PASS = ALL on >=3/4 seeds unless noted)
- **c1 reach earned**   : G_trunk ho_acc >= CE + 0.10  (gamma earns over CE-echo)
- **c2 DPI escape**     : G_trunk ho_acc >= ADD + 0.15 AND on non-commuting held-out
                          ADD_nc <= 0.55 while G_trunk_nc > ADD_nc + 0.15
- **c3 trunk != readout**: G_trunk >= G_read + 0.08  (routing gamma to trunk is load-bearing;
                           if ~equal => H_1602 re-fry)
- **c4 headroom sanity** : at least one arm ho_acc >= 0.20 on GROUP (world is actually learnable;
                           else INCONCLUSIVE not FAIL)
- **c5 SHUFFLE ablation**: G_trunk NOT >= CE + 0.10 on SHUFFLE (advantage structure-earned)
- Report reach/unreach verbatim. No bar byte-change post-run (p7/c9/c2).

Seeds [0,1,2,3]. P=6, C=12, d=24, h=64, steps=4000, lr=3e-3, tau=0.1, gamma=1.0.
