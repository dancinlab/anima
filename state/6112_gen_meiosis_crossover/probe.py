# H_1843 — #9 감수분열 crossover (MEIOSIS, != mitosis) DIRECTIONAL numpy probe
# =============================================================================
# QUESTION (the ONLY one this probe answers): does the MEIOSIS-CROSSOVER
# combination operator (homologous SEGMENT EXCHANGE between two parents) make
# two INDEPENDENT/DISTANT concepts COMPOSABLE — i.e. lift the count of REACHABLE
# novel (held-out) combinations above the ADDITIVE-superposition baseline floor?
#
# Prior art walled (verified, not re-fired):
#   - H_9022 mitosis_pure_substrate_theorem: PURE-SPLIT mitosis = substrate only,
#     A ⊥ G, generation contribution 0 (T2/T3). => split-only has depth0 Voronoi.
#   - G1 recomb wall: readout/tension/predictive/multiplicative/NMDA binding
#     operators ALL collapse in an ADDITIVE trunk (H_1816/1823/1834).
#   Meiosis crossover is a DIFFERENT operator: not a readout, not a split — it
#   RECOMBINES two full parent exemplars by exchanging homologous segments,
#   placing the two concepts in DISJOINT loci (a_substrate_disjoint: 분리=보존).
#
# TASK (2 INDEPENDENT concepts, entangled-in-training):
#   Axis A codewords cA[0..K-1], axis B codewords cB[0..K-1], random in R^(D/2).
#   TRAIN = diagonal pairs (i,i) only: the two concepts perfectly co-vary in
#     training, never seen recombined => recombination = REACH the off-diagonal.
#   TEST = all off-diagonal (i,j), i!=j : K*(K-1) held-out novel combinations.
#   composed_distinct = # distinct held-out pairs where BOTH axes decode correct.
#
# OPERATORS (same total budget D, same ridge readouts trained on diagonal only):
#   ADDITIVE  : v = cA[i] + cB[j]  in SHARED R^(D/2) (superposition/overlap).
#               heads read A and B from the SAME shared vector.
#   CROSSOVER : child = concat(cA[i], cB[j]) in R^D, two DISJOINT segments;
#               headA reads seg1 only, headB reads seg2 only (homologous loci).
#   (Total dims equal: additive uses D/2 twice-overlapped, crossover uses 2*(D/2)
#    = D disjoint. This dimensional split IS the meiosis mechanism, not a cheat.)
#
# FROZEN BAR (set BEFORE the run; NO post-hoc move, p7/c9):
#   GREEN-DIRECTIONAL iff  crossover_frac - additive_frac >= 0.30
#                     AND  additive_frac <= 0.20 (additive is at/near floor)
#                     on >=2/3 seeds.  Else FALSIFIED / floor.
#   (numpy toy => DIRECTIONAL by construction, NEVER terminal.)
# =============================================================================
import numpy as np

K   = 8          # concepts per axis
DH  = 6          # per-segment dim (D/2); shared space is also DH for additive
SEEDS = [1843, 1844, 1845]
BAR_LIFT, BAR_ADD_FLOOR = 0.30, 0.20
ALPHA = 1e-2     # ridge

def ridge_fit(X, Y, a):
    # X:(n,d) Y:(n,c) -> W:(d,c)
    d = X.shape[1]
    return np.linalg.solve(X.T@X + a*np.eye(d), X.T@Y)

def run(seed):
    rng = np.random.default_rng(seed)
    cA = rng.standard_normal((K, DH)); cA /= np.linalg.norm(cA,axis=1,keepdims=True)
    cB = rng.standard_normal((K, DH)); cB /= np.linalg.norm(cB,axis=1,keepdims=True)
    I  = np.eye(K)
    diag = [(i,i) for i in range(K)]
    offd = [(i,j) for i in range(K) for j in range(K) if i!=j]
    total = len(offd)

    # ---------- ADDITIVE (shared superposition) ----------
    Xtr = np.stack([cA[i]+cB[i] for (i,_) in diag])          # (K,DH)
    Ytr = I                                                   # diagonal labels
    Wa  = ridge_fit(Xtr, Ytr, ALPHA)   # head A from shared v
    Wb  = ridge_fit(Xtr, Ytr, ALPHA)   # head B from shared v (same X, diag Y)
    add_ok = 0
    for (i,j) in offd:
        v = cA[i]+cB[j]
        pa = int(np.argmax(v@Wa)); pb = int(np.argmax(v@Wb))
        if pa==i and pb==j: add_ok += 1
    add_frac = add_ok/total

    # ---------- MEIOSIS CROSSOVER (disjoint segment exchange) ----------
    # headA trained on seg1 (=cA on diagonal), headB on seg2 (=cB on diagonal)
    WA = ridge_fit(cA, I, ALPHA)   # seg1 -> axis A
    WB = ridge_fit(cB, I, ALPHA)   # seg2 -> axis B
    cr_ok = 0
    for (i,j) in offd:
        s1, s2 = cA[i], cB[j]                 # crossover child = concat(s1,s2)
        pa = int(np.argmax(s1@WA)); pb = int(np.argmax(s2@WB))
        if pa==i and pb==j: cr_ok += 1
    cr_frac = cr_ok/total
    return add_frac, cr_frac, add_ok, cr_ok, total

print("H_1843 MEIOSIS-CROSSOVER vs ADDITIVE-superposition (DIRECTIONAL numpy)")
print(f"K={K} per-seg-dim={DH} held-out off-diagonal combos/seed={K*(K-1)}")
print(f"FROZEN BAR: lift>= {BAR_LIFT}  AND additive<= {BAR_ADD_FLOOR}  on >=2/3 seeds")
print("-"*72)
wins=0; addv=[]; crv=[]
for s in SEEDS:
    a,c,ao,co,t = run(s)
    addv.append(a); crv.append(c)
    lift=c-a
    win = (lift>=BAR_LIFT) and (a<=BAR_ADD_FLOOR)
    wins += int(win)
    print(f"seed {s}: additive={a:.3f} ({ao}/{t})  crossover={c:.3f} ({co}/{t})"
          f"  lift={lift:+.3f}  {'WIN' if win else 'no'}")
print("-"*72)
ma,mc = np.mean(addv), np.mean(crv)
print(f"MEAN additive={ma:.3f}  crossover={mc:.3f}  lift={mc-ma:+.3f}  wins={wins}/3")
verdict = "GREEN-DIRECTIONAL" if wins>=2 else "FLOOR/FALSIFIED"
print(f"VERDICT: {verdict}  (numpy = DIRECTIONAL, never terminal)")
