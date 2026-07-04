# γ trained-constructive-bind — STEP-0 FROZEN BAR (pre-registered before run)

Candidate ① of the trunk-objective census (d) round. STEP-0 = mini numpy $0, torch-free
micro-autograd => **DIRECTIONAL only** (a_engine_native_learning; no engine-native G1 verdict).
A PASS here only means the *objective mechanism* survives a fair synthetic screen and warrants a
STEP-1 engine-native (`anima evaluate --py`) run; a FAIL means the loss-form collapses to the
census G1 floor even where genuine non-commutative structure EXISTS.

## The candidate mechanism (distinct axis from priors)
- **Loss form** = label CE  +  γ·InfoNCE contrastive that pushes the *trunk* rep r(a,b)
  (i) toward the composed-target anchor U[a∘b], and AWAY from (ii) the swapped-order trunk rep
  r(b,a) and (iii) the additive-bag anchor P·(E[a]+E[b]).
- Gradient of the γ term flows INTO the trunk representation (E, MLP), not only the readout.

## World (by-construction honesty)
- Non-abelian group **S_4** (24 elements). Input = ordered pair of element ids (a,b);
  target = group product a∘b (the Cayley table). Non-commutativity lives in the WORLD target
  (legitimate DPI-escape condition), NOT planted as an input interaction feature. Model learns
  embeddings + composition from scratch — no v_a⊙v_b handed in. reach≈1.000 EXACT on held-out
  ⇒ suspect table-leak / handed advantage; will be flagged.
- Train = random 40% of the 576 pairs (every element covered as both operands); held-out = rest.
  Recombination = generalize the group op to unseen ordered pairs.
- SHUFFLE control = replace the Cayley table with a random function table (destroys group
  systematicity, keeps marginals) → any γ advantage from real structure must vanish.

## Arms (single fixed order-capable trunk arch = concat-MLP, vary only the LOSS)
- **ADD**    : order-blind rep E[a]+E[b] + CE (provable DPI floor; symmetric ⇒ ≤0.5 on non-commuting pairs)
- **CE**     : concat-MLP trunk + CE only (γ=0; the "CE=echo" baseline)
- **G_trunk**: concat-MLP trunk + CE + γ·InfoNCE, γ grad flows to trunk  (= candidate ①)
- **G_read** : concat-MLP trunk + CE + γ·InfoNCE with anchor DETACHED (γ grad to readout U only)
               (= H_1602 readout-aux repro; isolates the trunk-routing claim)

## Frozen pre-registered bar (PASS = ALL of c1..c4 on >=3/4 seeds unless stated)
- **c1 (reach earned)**   : G_trunk held-out acc >= CE + 0.10  on >=3/4 seeds  (γ earns recombination over echo)
- **c2 (DPI escape)**     : G_trunk held-out acc >= ADD + 0.15 on >=3/4 seeds, AND on the NON-COMMUTING
                            held-out subset ADD <= 0.55 (order-blind floor) while G_trunk > ADD+0.15
- **c3 (trunk != readout)**: G_trunk >= G_read + 0.08 on >=3/4 seeds  (routing γ to the TRUNK is load-bearing;
                            if G_trunk ~ G_read the candidate is a H_1602 re-fry)
- **c4 (SHUFFLE ablation)**: on the SHUFFLE table, G_trunk NOT >= CE + 0.10 (advantage is structure-earned,
                            not loss-manufactured) — i.e. c1 must FAIL under SHUFFLE
- Report reach (P[correct]) and unreach (mean P over wrong classes) verbatim, mean over seeds.
- No bar byte changes post-run (p7/c9/c2). Negative is a result (no tune-to-green).

## Seeds: [0,1,2,3]. tau=0.1, gamma=1.0, d=24, h=64, steps=4000, Adam lr=3e-3, train_frac=0.40.
Autograd validated by finite-difference gradcheck (printed) before the run is trusted.
