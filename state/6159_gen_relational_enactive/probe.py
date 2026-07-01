# H_6159 — 관계적/enactive 조합 (numpy DIRECTIONAL reachability screen)
# MECHANISM: 같은 내부상태(A_i,B_j)가 청자/context c 에 따라 다른 조합으로 collapse —
#   조합이 고정 연산자 아닌 상호작용(context)에서 창발(p5 관계적).
#
# G1 canonical toy (siblings H_6104/H_6112 convention): 2 INDEPENDENT concept axes
#   A(K codewords) x B(K codewords). Train DIAGONAL (i,i) only. Test = held-out
#   off-diagonal novel combos (i!=j). Matched budget D, matched ridge readout.
#   reach = fraction of held-out (i,j) whose nearest composed-target is correct.
#
# ARMS:
#   ADDITIVE  : v = pA[i] + pB[j]            (shared superposition, fixed op)
#   RELATIONAL: combination MODULATED by context/listener c (H_6159) —
#               out-feature = context-gated bilinear of (pA[i],pB[j]); the
#               "listener" c selects which mixing subspace the state collapses into.
#
# Two context regimes (honest):
#   (R1) INDEPENDENT context  — c is the LISTENER REGISTER, drawn INDEPENDENT of the
#        (i,j) target. This is the FAIR test of the enactive claim: does context-
#        modulation ALONE open recombination without leaking the answer?
#   (R2) INFORMATIVE context  — c correlated w/ target (leak control): shows any lift
#        is leakage, not combination. Reported but NOT the pass regime.
#
# FROZEN BAR (pre-registered BEFORE run):
#   GREEN-DIRECTIONAL iff in R1 (independent context):
#       (RELATIONAL_reach - ADDITIVE_reach) >= +0.30  AND  ADDITIVE_reach <= 0.20
#       on >= 2/3 seeds.
#   Else -> DIRECTIONAL FLOOR (operator INERT for independent concepts).
# numpy = DIRECTIONAL by construction, never terminal (H_6112 caveat: numpy toys OVERSTATE;
#   meiosis was 0->1.0 numpy but 0->0.022 on REAL CLMConvMoE trunk).

import numpy as np

K = 8          # codewords per axis
D = 32         # feature/budget
L = 4          # number of contexts (listeners)
ridge = 1e-2

def make_axis(rng, K, D):
    P = rng.standard_normal((K, D))
    P /= np.linalg.norm(P, axis=1, keepdims=True)
    return P

def ridge_fit(X, Y, lam):
    # X:(N,F) Y:(N,C) -> W:(F,C)
    F = X.shape[1]
    return np.linalg.solve(X.T@X + lam*np.eye(F), X.T@Y)

def reach(Wfeat_fn, pA, pB, train_pairs, test_pairs, contexts_train, contexts_test, ncls):
    # build train design
    Xtr = np.stack([Wfeat_fn(pA[i], pB[j], c) for (i,j),c in zip(train_pairs, contexts_train)])
    Ytr = np.zeros((len(train_pairs), ncls))
    for r,(i,j) in enumerate(train_pairs):
        Ytr[r, i*K+j] = 1.0
    W = ridge_fit(Xtr, Ytr, ridge)
    Xte = np.stack([Wfeat_fn(pA[i], pB[j], c) for (i,j),c in zip(test_pairs, contexts_test)])
    pred = Xte@W
    hit = 0
    for r,(i,j) in enumerate(test_pairs):
        if np.argmax(pred[r]) == i*K+j:
            hit += 1
    return hit/len(test_pairs)

def run_seed(seed, regime):
    rng = np.random.default_rng(seed)
    pA = make_axis(rng, K, D)
    pB = make_axis(rng, K, D)
    ncls = K*K
    # context gates: L random projections (learned-mixing surrogate)
    Gates = rng.standard_normal((L, D, D)) * (1.0/np.sqrt(D))

    train_pairs = [(i,i) for i in range(K)]          # diagonal only
    test_pairs  = [(i,j) for i in range(K) for j in range(K) if i!=j]  # held-out novel

    # context assignment
    if regime == "R1":   # independent listener register (fair)
        ctr = rng.integers(0, L, size=len(train_pairs))
        cte = rng.integers(0, L, size=len(test_pairs))
    else:                # R2 informative leak control: context encodes j
        ctr = np.array([j % L for (_,j) in train_pairs])
        cte = np.array([j % L for (_,j) in test_pairs])

    def add_feat(a,b,c):
        return a + b
    def rel_feat(a,b,c):
        # context-modulated combination: listener c selects a bilinear mixing subspace,
        # then interact the two concept states through it (enactive collapse).
        Gc = Gates[c]
        return (a @ Gc) * (Gc @ b)   # context-gated bilinear interaction

    ra = reach(add_feat, pA, pB, train_pairs, test_pairs, ctr, cte, ncls)
    rr = reach(rel_feat, pA, pB, train_pairs, test_pairs, ctr, cte, ncls)
    return ra, rr

print("H_6159 relational/enactive combination — G1 recombination DIRECTIONAL screen")
print(f"K={K} D={D} L={L}  train=diagonal({K}) test=held-out off-diagonal({K*K-K})")
print("FROZEN BAR: GREEN iff R1(independent ctx): rel-add>=+0.30 AND add<=0.20 on >=2/3 seeds\n")

for regime,label in [("R1","INDEPENDENT context (FAIR — pass regime)"),
                     ("R2","INFORMATIVE context (leak control)")]:
    print(f"--- regime {regime}: {label} ---")
    wins=0
    for seed in range(3):
        ra, rr = run_seed(seed, regime)
        lift = rr - ra
        win = (lift >= 0.30 and ra <= 0.20)
        wins += 1 if win else 0
        print(f"  seed{seed}: ADD={ra:.3f}  RELATIONAL={rr:.3f}  lift={lift:+.3f}  win={win}")
    verdict = "GREEN-DIRECTIONAL" if (regime=="R1" and wins>=2) else "FLOOR"
    print(f"  wins={wins}/3 -> {verdict if regime=='R1' else '(diagnostic only)'}\n")
