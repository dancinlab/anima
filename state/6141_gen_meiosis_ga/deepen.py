# H_6141 gen_meiosis_ga — ADVERSARIAL DEEPEN (numpy DIRECTIONAL, <30s, OMP=4)
# ---------------------------------------------------------------------------
# Operator under test: MEIOSIS-GA = #9 disjoint-loci crossover (H_6112) wrapped
# in #28 GA population + gradient-free selection.  Nature's "true recombination"
# of two parents A,B is the disjoint-loci whole GT = mask*A + (1-mask)*B.
# Original numpy screen (H_6112) reported REACHABLE: additive 0.0 -> crossover 1.0.
# H_6112 precedent PROVED this same REACHABLE COLLAPSES on the real CLMConvMoE
# trunk (0 -> 0.022).  a_break_the_wall: a REACHABLE is not confident until
# controls kill the alternatives.  We apply C1/C2/C3 to try to REFUTE the signal.
#
# ===== FROZEN BAR (declared BEFORE running) =====
# The meiosis-GA operator SURVIVES as a real composition mechanism only if ALL:
#   (B1) GENERIC-NONLINEARITY control fails to match it: a generic *trained*
#        linear combiner must NOT reach GT as well as hand-coded meiosis
#        (reach_generic < reach_meiosis - 0.30).  If a generic combiner reaches
#        the same target, "reachability" is a metric artifact of learnability,
#        not of the meiosis mechanism.
#   (B2) BIND-RECOVERABILITY beats additive by margin >= +0.15 R^2 on HELD-OUT
#        (both parents linearly recoverable from the composed child beyond the
#        additive baseline).  distinct-from-parents is NECESSARY not SUFFICIENT.
#   (B3) ABLATION: turning the disjoint-loci ingredient OFF collapses the reach
#        metric to the additive floor (proves the ingredient is causal).
# If (B1) fails OR (B2) fails -> ARTIFACT (numpy REACHABLE was a metric artifact).
# ================================================
import os
os.environ["OMP_NUM_THREADS"] = "4"
import numpy as np

RNG = np.random.default_rng(0)
d, n_tr, n_ho = 64, 200, 56          # 56 held-out matches H_6112 screen
THR = 0.30                            # SPLIT_THRESH / frozen rel-radius bar

def pairs(n):
    return RNG.standard_normal((n, d)), RNG.standard_normal((n, d))

# Hidden "true" recombination rule nature uses: a fixed disjoint-loci partition.
MASK = (RNG.random(d) < 0.5).astype(float)        # 1->parent A locus, 0->parent B
def GT(A, B):                                       # ground-truth composed whole
    return A * MASK + B * (1 - MASK)

Atr, Btr = pairs(n_tr); Aho, Bho = pairs(n_ho)
Ttr, Tho = GT(Atr, Btr), GT(Aho, Bho)             # target wholes (held-out = generalization)
dAB = np.linalg.norm(Aho - Bho, axis=1) + 1e-9    # per-pair scale

def reach(C):                                       # frac held-out reaching the true whole GT
    return float(np.mean(np.linalg.norm(C - Tho, axis=1) / dAB < THR))

def r2_recover(Ctr, Cho):                           # C2: linear readout C->A and C->B, held-out R^2
    def one(Ctrain, Ctest, Ptrain, Ptest):
        W, *_ = np.linalg.lstsq(Ctrain, Ptrain, rcond=None)   # C->P
        pred = Ctest @ W
        mu = Ptrain.mean(0)
        ss_res = np.sum((Ptest - pred) ** 2)
        ss_tot = np.sum((Ptest - mu) ** 2) + 1e-12
        return 1.0 - ss_res / ss_tot
    return 0.5 * (one(Ctr, Cho, Atr, Aho) + one(Ctr, Cho, Btr, Bho))

# ---- arms (compute both train & held-out composed children) ----
def additive(A, B):  return 0.5 * (A + B)
def meiosis(A, B):   return A * MASK + B * (1 - MASK)        # #9 crossover, ORACLE mask

def meiosis_ga(A, B, pop=8, mut=0.30):                       # #28 GA: pop + gradient-free selection
    n = A.shape[0]; best = np.zeros_like(A); bscore = np.full(n, -1e18)
    for _ in range(pop):
        mk = (RNG.random(A.shape) < 0.5).astype(float)      # random per-locus recombination
        Ck = A * mk + B * (1 - mk) + mut * RNG.standard_normal(A.shape)
        # gradient-free fitness = the ONLY unsupervised signal available:
        # distinctness from both parents (target GT is unknown at generation time)
        s = np.minimum(np.linalg.norm(Ck - A, axis=1), np.linalg.norm(Ck - B, axis=1))
        u = s > bscore; best[u] = Ck[u]; bscore[u] = s[u]
    return best

def meiosis_ga_noselect(A, B, mut=0.30):                     # C3b: selection OFF (random child)
    mk = (RNG.random(A.shape) < 0.5).astype(float)
    return A * mk + B * (1 - mk) + mut * RNG.standard_normal(A.shape)

def meiosis_noloci(A, B):                                    # C3a: disjoint-loci OFF -> blend==additive
    return 0.5 * A + 0.5 * B

# C1 generic nonlinearities
def gen_tanh(A, B): return np.tanh(A + B)
def gen_mul(A, B):  return A * B
def gen_learned_tr_ho():                                     # C1c: generic TRAINED linear combiner
    X = np.hstack([Atr, Btr]); W, *_ = np.linalg.lstsq(X, Ttr, rcond=None)
    return (np.hstack([Aho, Bho]) @ W)

print("H_6141 meiosis-GA — ADVERSARIAL DEEPEN (numpy DIRECTIONAL)")
print("="*68)
print("reach = frac held-out reaching true recombination whole GT (rel<%.2f)"%THR)
print("-"*68)

r_add  = reach(additive(Aho, Bho))
r_meio = reach(meiosis(Aho, Bho))
r_ga   = reach(meiosis_ga(Aho, Bho))
print("[baseline] ADDITIVE reach          = %.3f   (floor)"     % r_add)
print("[H_6112 ]  MEIOSIS(oracle) reach   = %.3f   (REACHABLE screen reproduces)" % r_meio)
print("[H_6141 ]  MEIOSIS-GA reach        = %.3f"               % r_ga)

print("-"*68); print("C1 GENERIC-NONLINEARITY control (does non-meiosis reach GT?):")
r_tanh = reach(gen_tanh(Aho, Bho)); r_mul = reach(gen_mul(Aho, Bho)); r_lrn = reach(gen_learned_tr_ho())
print("   tanh(A+B) reach                 = %.3f" % r_tanh)
print("   A*B       reach                 = %.3f" % r_mul)
print("   GENERIC-LEARNED linear combiner = %.3f   <-- key: generically learnable?" % r_lrn)

print("-"*68); print("C2 BIND-RECOVERABILITY (held-out R^2 of recovering BOTH parents from C):")
b_add  = r2_recover(additive(Atr, Btr), additive(Aho, Bho))
b_meio = r2_recover(meiosis(Atr, Btr),  meiosis(Aho, Bho))
b_ga   = r2_recover(meiosis_ga(Atr, Btr), meiosis_ga(Aho, Bho))
print("   ADDITIVE   bind-R^2            = %.3f" % b_add)
print("   MEIOSIS    bind-R^2            = %.3f  (margin vs add %+.3f)" % (b_meio, b_meio-b_add))
print("   MEIOSIS-GA bind-R^2            = %.3f  (margin vs add %+.3f)" % (b_ga,   b_ga-b_add))

print("-"*68); print("C3 ABLATION (turn key ingredient OFF -> must collapse to floor):")
r_noloci  = reach(meiosis_noloci(Aho, Bho))
r_nosel   = reach(meiosis_ga_noselect(Aho, Bho))
print("   disjoint-loci OFF reach        = %.3f  (vs additive floor %.3f)" % (r_noloci, r_add))
print("   GA selection OFF reach         = %.3f  (vs meiosis-GA %.3f)"     % (r_nosel, r_ga))

print("="*68); print("FROZEN-BAR VERDICT:")
B1 = r_lrn < (r_meio - 0.30)                 # generic learned must NOT match meiosis
B2 = (b_ga - b_add) >= 0.15                   # bind-recoverability margin
B3 = r_noloci <= r_add + 1e-6                 # ablation collapses to floor
print("  (B1) generic combiner fails to match meiosis?  %s (gen=%.3f vs meio-0.30=%.3f)" % (B1, r_lrn, r_meio-0.30))
print("  (B2) bind-recoverability beats additive +0.15?  %s (margin=%+.3f)" % (B2, b_ga-b_add))
print("  (B3) ablation collapses to floor?               %s" % B3)
survives = B1 and B2 and B3
print("-"*68)
if survives:
    print("VERDICT: SURVIVES all controls -> real composition signal (flag real-trunk rung)")
else:
    print("VERDICT: ARTIFACT -> numpy REACHABLE is a metric artifact.")
    if not B1: print("  * a GENERIC TRAINED combiner reaches GT as well as meiosis -> the target is")
    if not B1: print("    generically learnable; meiosis structure is NOT load-bearing (= trunk-OBJECTIVE wall).")
    if not B2: print("  * meiosis-GA does NOT make both parents more recoverable than additive")
    if not B2: print("    -> distinct-from-parents was necessary-not-sufficient; not compositional binding.")
print("  H_6112 TRANSFER CAVEAT: same crossover operator FALSIFIED on real")
print("  CLMConvMoE trunk (0 -> 0.022 << 0.30). numpy REACHABLE != green light.")
print("  GA/selection axis independently INERT (H_1568 selection lift -0.00046).")
