# H_1840 STAGE-1 — FAIR (non-rigged) cheap-gate PRE-REGISTRATION (frozen before measurement)

Frozen: 2026-07-02, before any FAIR-toy run. tune-to-green forbidden (p7). This bar is fixed;
post-hoc movement is a violation. torch/numpy mirror => DIRECTIONAL mechanism screen only (NOT a
G1 verdict; the engine-native `anima evaluate --py` GPU run is the terminal test —
a_engine_native_learning, session-eval-py-only).

## Why a NEW gate (the old cheap-gate was RIGGED)

PR #2689 old toy target was `K[i,j] = circ_conv(A[i],B[j])` — the target's compositional
algebra was DEFINED to equal the HRR operator. Result: arm (c) HRR generalized, but so did (d)
non-invertible bottleneck (tie), and the additive-target control FLIPPED additive→perfect. The
old toy was therefore a pure **operator↔target-algebra matching** screen: it proves nothing
about whether a bypass-denied bilinear bottleneck helps on structure that is NOT its own
operator. The distilled surviving delta = **bypass-denied bilinear bottleneck at scale
(invertibility-agnostic)** — H_1819 (bypass OPEN) floored engine-native; the untested question
is whether DENYING the additive bypass (forcing composite logits through a bilinear path) lifts
G1 where bypass-OPEN floored. This gate tests that FAIRLY (target NOT matched to any arm's op).

## FAIR task (operator-agnostic 2-way latent-interaction retrieval)

- D=64. N_a=10 A-atoms, N_b=10 B-atoms => 100 composite (i,j).
- Atom embeddings A[N_a,D], B[N_b,D] = FIXED random unit-Gaussian (NO planted structure).
- Each atom carries a LATENT factor: fa[i]∈{0..P-1}, fb[j]∈{0..P-1}, P=5 (2 atoms/class).
- Composite target CLASS  c(i,j) = T[fa[i], fb[j]]  where **T is a fixed RANDOM P×P table
  over C=9 output classes** — a genuine 2-way NON-additive interaction. T is NOT any arm's
  operator (not ⊛, not ⊙, not sum) and NOT additive (verified: T ≠ (fa+fb) structure).
- Retrieval candidates = C=9 class keys Kc[C,D], FIXED random unit-Gaussian (operator-agnostic
  surface, like the arbitrary byte sequence of a word — no algebraic relation to A,B).
- Model sees e_a=A[i], e_b=B[j]; learns Wa,Wb (and per-arm bilinear/skip params); forms query
  q; logits = (q_norm @ Kc.T)/temp; CE against correct class c(i,j).
- Train = 70/100 (i,j) combos, chosen so every atom AND every (fa,fb) latent-pair is covered
  by >=1 train combo (interaction table fully learnable in principle). Held-out = ~30 (i,j) =
  unseen atom-COMBINATIONS of seen atoms (G1-recombination analogue).

Fairness: no arm's operator equals T; every arm must LEARN Wa,Wb to decode latent factors then
combine. Additive q cannot represent a non-additive table (floors held-out). A bypass-denied
bilinear bottleneck CAN represent T[fa,fb] via a bilinear form (generalizes IF the mechanism is
real). No arm is target-matched => non-rigged.

## 5 arms

- (a) additive          : q = Wa e_a + Wb e_b                              (sum, no bilinear)
- (b) hadamard_bypass   : q = (Wa e_a)⊙(Wb e_b) + (Sa e_a + Sb e_b)        (= H_1819, additive
                          skip Sa,Sb OPEN => bypass available)
- (c) hrr_bottleneck    : q = circ_conv(Wa e_a, Wb e_b) ONLY               (invertible ⊛, bypass DENIED)
- (d) noninv_bottleneck : q = circ_conv_freqmasked(...) ONLY               (⊛ invertibility ablated, bypass DENIED)
- (e) bilinear_bottleneck (NEW, DECISIVE): q = Wo · vec((Wa e_a) ⊗ (Wb e_b))  — full learned
                          bilinear form, NO additive skip (bypass DENIED, invertibility-AGNOSTIC).

Adam, full-batch train, 4000 steps, seeds {7,4302,4303}. temp=0.07.

## Metric

- Primary = **held-out top-1 accuracy** (fraction of held-out (i,j) whose argmax retrieval = c).
- G1-flavored secondary = **composed_distinct** = # distinct correct CLASSES retrieved on the
  held-out set (max C=9); reported, not gated.
- chance held-out top-1 = 1/C = 1/9 ≈ 0.111.

## FROZEN PRE-REGISTERED BAR (decisive)

PASS (mechanism FAIRLY supported => STAGE-2 engine-native GPU fire AUTHORIZED) iff ALL hold:
  1. On >=2/3 seeds {7,4302,4303}:  heldout_acc(e) >= heldout_acc(a) + 0.34   (bilinear-bottleneck
     dominates ADDITIVE by >= +0.34), AND
  2. On >=2/3 seeds:  heldout_acc(e) >= heldout_acc(b) + 0.34                 (dominates
     bypass-OPEN Hadamard = H_1819 repro by >= +0.34), AND
  3. all arms reach train_acc >= 0.95 on those seeds (fair: every arm CAN fit train; split is
     purely on held-out generalization), AND
  4. NON-RIGGED CONTROL: on the additive-target control (T_add[fa,fb] = (fa+fb), additive
     structure), the additive arm generalizes AND arm (e) does NOT dominate additive by +0.34
     (i.e. heldout_acc(e) < heldout_acc(a) + 0.34 there). This proves the FAIR-target win is
     driven by the target's genuine 2-way structure, not by architectural favoritism toward (e).

FAIL iff any clause breaks => GPU NOT fired ($ saved even though pool is free — SCIENTIFIC gate,
not cost gate), honest negative: γ / bypass-denied-bilinear collapses to the census G1 floor
=> **G1 recombination wall CONFIRMED (DPI meta-law, all local + cheap levers exhausted)**,
a_break_the_wall confident wall.

## Scope / honesty (c9)

A PASS proves only that a bypass-denied bilinear bottleneck CAN learn a genuine 2-way
compositional interaction and generalize to held-out combinations when that structure EXISTS —
it does NOT prove natural-language composite tokens carry such recoverable 2-way structure. That
transfer is EXACTLY what the engine-native GPU run measures (STAGE-2). torch mirror => DIRECTIONAL
only; terminal G1 verdict requires `anima evaluate --py <clm>` (session-eval-py-only). A PASS
here only authorizes spending compute on the engine-native run; it is not itself a G1 result.
