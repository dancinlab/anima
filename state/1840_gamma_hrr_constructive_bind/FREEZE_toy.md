# H_1840 γ HRR constructive-bind — CHEAP-GATE toy PRE-REGISTRATION (frozen before measurement)

Frozen: 2026-07-02, before any toy run. tune-to-green forbidden (p7). This bar is fixed;
post-hoc movement is a violation. numpy mirror => DIRECTIONAL mechanism screen only (NOT a
G1 verdict; engine-native GPU run is the terminal test — a_engine_native_learning).

## Task (2-leg held-out conjunction retrieval)

- D=64 dim. N_a=10 concept-A atoms, N_b=10 concept-B atoms => 100 composite classes.
- Fixed random atomic codebooks A[N_a,D], B[N_b,D] (unit Gaussian).
- Ground-truth composite target keys  K[i,j] = circular_conv(A[i], B[j])  (HRR binding),
  L2-normalized. These 100 keys are the fixed retrieval candidates.
- Train pairs = 70% of the 100 (i,j) combos, chosen so every atom i and every atom j is
  covered by >=1 train pair. Held-out = the remaining ~30% (i,j) — unseen COMBINATIONS of
  SEEN atoms (this is the G1-recombination analogue).
- Model sees embeddings e_a=A[i], e_b=B[j]; learns Wa,Wb (D×D, random init) and forms a
  query q; retrieves via logits = (q @ K.T)/temp; trained CE against correct composite idx.

## 4 arms (card §Cheap test)

- (a) additive        : q = Wa e_a + Wb e_b                         (sum readout)
- (b) hadamard_bypass : q = (Wa e_a) ⊙ (Wb e_b) + (Sa e_a + Sb e_b) (= H_1819 repro; additive
                        skip path Sa,Sb kept OPEN => bypass available)
- (c) hrr_bottleneck  : q = circ_conv(Wa e_a, Wb e_b)  ONLY         (invertible ⊛, bypass DENIED)
- (d) noninv_bottleneck: q = circ_conv_freqmasked(Wa e_a, Wb e_b) ONLY (same bottleneck,
                        ⊛ replaced by non-invertible masked-frequency mix => invertibility ablated)

Adam, full-batch on train pairs, 3000 steps, seeds {7,4302,4303}. temp=0.07.

## FROZEN PRE-REGISTERED PREDICTION (decisive double-dissociation)

Chance held-out top-1 = 1/100 = 0.01.

PASS (mechanism directionally supported, => GPU fire authorized) iff, on >=2/3 seeds:
  1. heldout_acc(c) >= 0.50            (arm c generalizes to unseen combinations), AND
  2. heldout_acc(c) > 3× max(heldout_acc(a), heldout_acc(b), heldout_acc(d))   (c strictly
     dominates all three floors — invertibility AND bottleneck both load-bearing), AND
  3. all arms reach train_acc >= 0.95  (fair: every arm CAN memorize training pairs;
     the split is purely on held-out generalization, not on fit).

FAIL (mechanism screen floors) iff the above does not hold => GPU NOT fired ($ saved),
honest negative recorded (γ collapses to census floor, a_break_the_wall confident wall).

Ablation reading: (c)>(d) isolates INVERTIBILITY as load-bearing (same bottleneck, only ⊛
invertibility differs). (c)>(b) isolates the BYPASS-DENY bottleneck (b has the skip open).
(c)>(a) vs plain additive. All three must break for the decisive cell to be unique.

## Scope / honesty (c9)

The target keys are DEFINED with binding structure (K=A⊛B), so this screens whether the
architecture (invertible-⊛ bottleneck) is NECESSARY+SUFFICIENT for compositional
generalization on binding-structured targets — and whether removing invertibility (d) or
opening the bypass (b) breaks it. It does NOT prove natural-language composite tokens carry
recoverable binding structure the trunk can learn — that is exactly the GPU test. A PASS here
only authorizes spending on the GPU run; it is not a G1 result.
