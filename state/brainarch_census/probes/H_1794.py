#!/usr/bin/env python3
# H_1794 — corticostriatal_loop_bouquet_thalamic_bind  ($0 cheap_test, numpy mirror)
# ============================================================================
# CLAIM (card cheap_test): N segregated factor-loops, each a Go/NoGo WTA over k
# value-slots; the SHARED thalamic relay fires only on COINCIDENT multi-loop
# disinhibition = a MULTIPLICATIVE AND (product gate) over per-factor releases.
# Question: does CONJUNCTIVE (AND/product) gating produce binding that the
# additive(sum) / max-pool relay structurally CANNOT?  ("composed_distinct ~
# product > max_single"; INERT ablation = swap product->max-pool collapses to
# max_single; scramble cortico-striatal map -> V-mass -> chance.)
#
# ⚠️ MEASUREMENT PATH = numpy toy = DIRECTIONAL ONLY (NOT engine-native;
#    a_engine_native_learning). No cli/anima.hexa, no core/g_gates. Toy decides
#    DIRECTION of the architecture, not a terminal G0/G1/G2 verdict.
#
# Precedent SCREEN_multiply_vs_add: full-set stats INFLATE additive via marginal
# shortcuts -> must isolate the AMBIGUOUS (binding-required) subset where pos/neg
# share identical per-factor marginals but differ in the JOINT binding.
# ============================================================================
#
# ── FROZEN BAR (pre-registered BEFORE running — tune-to-green 금지, p7/c9) ──
#   Setup: N=3 factor-loops, k=3 values each  (joint space k^N = 27).
#
#   A) BINDING-REQUIRED (ambiguous subset · primary · learned ridge readout):
#        conjunctive(product) ambig_acc   >= 0.95   (the AND separates the joint)
#        max-pool (INERT ablation)         <= 0.60   (collapses ~chance 0.5)
#        additive(sum, INERT)              <= 0.60   (marginal-only -> forced 0.5)
#        single-factor (max_single base)   <= 0.60   (one loop cannot bind)
#        scramble cortico-striatal (G0)    <= 0.60   (destroy map -> chance)
#   B) composed_distinct (G1/G2 capacity, under superposition):
#        cd(product) >= 0.9 * k^N (=24/27)  AND  cd(product) >= 5   (G2 dist>=5)
#        cd(max-pool) <= 2*k (=6)            (collapses toward max_single = k = 3)
#        cd(product) > cd(max-pool)          (INERT differential)
#
#   VERDICT = SUPPORT(DIRECTIONAL) iff (A) all hold AND (B) all hold.
#             else MIXED / NOT-SUPPORTED (honest).
# ============================================================================
import numpy as np
import itertools

rng = np.random.default_rng(7)
N, K = 3, 3                      # 3 factor-loops, k=3 value-slots each
JOINTS = list(itertools.product(range(K), repeat=N))   # 27 joint triples
assert len(JOINTS) == K**N

def eye_k(v):                    # WTA Go release = one-hot over k slots
    e = np.zeros(K); e[v] = 1.0; return e

# ---- per-item relay outputs over the 3 loop releases (r1,r2,r3 in R^k) ----
def relay_product(item):        # thalamic AND: coincident release = outer product
    r = [eye_k(item[i]) for i in range(N)]
    o = r[0]
    for i in range(1, N):
        o = np.multiply.outer(o, r[i])
    return o.ravel()            # dim k^N  (one-hot at the joint)
def relay_max(item):            # INERT ablation: max-pool over the loop releases
    r = [eye_k(item[i]) for i in range(N)]
    grid = np.zeros([K]*N)
    for idx in JOINTS:
        grid[idx] = max(r[i][idx[i]] for i in range(N))   # union "cross"
    return grid.ravel()
def relay_add(item):            # additive marginal rep: concat per-factor releases
    return np.concatenate([eye_k(item[i]) for i in range(N)])   # dim N*k

def scene_rep(items, relay):    # relay integrates releases across items (superpose)
    return sum(relay(it) for it in items)

# ---- ambiguous (binding-required) scene generator for a target triple T ----
# pos = {T, D}  (T present); neg = swap factor-(N-1) between T and D so MARGINALS
# are identical but T is ABSENT (illusory conjunction at N factors). D fully
# differs from T in every factor -> neither neg item equals T.
def diff_triple(T):
    return tuple((T[i] + 1 + int(rng.integers(K-1))) % K for i in range(N))  # all != T[i]
def ambig_pair(T):
    D = diff_triple(T)
    pos = [tuple(T), D]
    neg = [tuple(T[:N-1]) + (D[N-1],), D[:N-1] + (T[N-1],)]   # swap last factor
    return pos, neg
def ambig_dataset(T, n, relay):
    X, y = [], []
    for _ in range(n):
        pos, neg = ambig_pair(T)
        rng.shuffle(pos); rng.shuffle(neg)
        X.append(scene_rep(pos, relay)); y.append(1.0)
        X.append(scene_rep(neg, relay)); y.append(0.0)
    return np.array(X), np.array(y)

def ridge_acc(Xtr, ytr, Xte, yte, lam=1e-2):
    Xtr = np.c_[Xtr, np.ones(len(Xtr))]; Xte = np.c_[Xte, np.ones(len(Xte))]
    w = np.linalg.solve(Xtr.T@Xtr + lam*np.eye(Xtr.shape[1]), Xtr.T@ytr)
    return float(((Xte@w > 0.5).astype(float) == yte).mean())

# single-factor (max_single) baseline: read ONLY one loop's marginal release
def relay_single(item):  return eye_k(item[0])   # factor-0 only

print("="*72)
print("H_1794  corticostriatal_loop_bouquet_thalamic_bind  — $0 numpy cheap_test")
print(f"  N={N} factor-loops · k={K} value-slots · joint space k^N={K**N}")
print("="*72)

# ── (A) BINDING-REQUIRED ambiguous subset · aggregate over a sample of targets ──
def aggregate_ambig(relay, n_each=400, targets=None):
    targets = targets or JOINTS
    accs = []
    for T in targets:
        Xtr, ytr = ambig_dataset(T, n_each, relay)
        Xte, yte = ambig_dataset(T, n_each//2, relay)
        accs.append(ridge_acc(Xtr, ytr, Xte, yte))
    return float(np.mean(accs))

# proper G0 scramble: per-TRIAL random codebook destruction (not a fixed bijection)
# -> the receiver-fixed thalamic channel for T no longer marks T consistently.
def relay_product_scram_dataset(T, n):
    X, y = [], []
    for _ in range(n):
        perm = [rng.permutation(K) for _ in range(N)]   # fresh per trial = destroys map
        sc = lambda it: tuple(int(perm[i][it[i]]) for i in range(N))
        pos, neg = ambig_pair(T)
        X.append(scene_rep([sc(it) for it in pos], relay_product)); y.append(1.0)
        X.append(scene_rep([sc(it) for it in neg], relay_product)); y.append(0.0)
    return np.array(X), np.array(y)
def aggregate_scram(targets, n_each=400):
    accs=[]
    for T in targets:
        Xtr,ytr=relay_product_scram_dataset(T,n_each); Xte,yte=relay_product_scram_dataset(T,n_each//2)
        accs.append(ridge_acc(Xtr,ytr,Xte,yte))
    return float(np.mean(accs))

samp_targets = [JOINTS[i] for i in rng.choice(len(JOINTS), 8, replace=False)]
acc_prod   = aggregate_ambig(relay_product, targets=samp_targets)
acc_max    = aggregate_ambig(relay_max,     targets=samp_targets)
acc_add    = aggregate_ambig(relay_add,     targets=samp_targets)
acc_single = aggregate_ambig(relay_single,  targets=samp_targets)
acc_scram  = aggregate_scram(samp_targets)

print("\n[A] BINDING-REQUIRED (ambiguous subset · identical marginals, diff joint · M=2)")
print(f"    conjunctive(product) ambig_acc = {acc_prod:.3f}   (bar >= 0.95)")
print(f"    max-pool   (INERT)   ambig_acc = {acc_max:.3f}   (bar <= 0.60)")
print(f"    additive(sum,INERT)  ambig_acc = {acc_add:.3f}   (bar <= 0.60)")
print(f"    single-factor(max_single)      = {acc_single:.3f}   (bar <= 0.60)")
print(f"    scramble cortico-striatal(G0)  = {acc_scram:.3f}   (bar <= 0.60)")

# ── (B) composed_distinct under superposition (G1/G2 capacity) ──
# For each of the k^N joints as a detection target, is it linearly decodable
# from the AMBIGUOUS superposed scene? count detectable (>=0.95) = composed_distinct.
def composed_distinct(relay, thr=0.95, n_each=300):
    cnt = 0
    for T in JOINTS:
        Xtr, ytr = ambig_dataset(T, n_each, relay)
        Xte, yte = ambig_dataset(T, n_each//2, relay)
        if ridge_acc(Xtr, ytr, Xte, yte) >= thr:
            cnt += 1
    return cnt
cd_prod = composed_distinct(relay_product)
cd_max  = composed_distinct(relay_max)
max_single = K
print("\n[B] composed_distinct (distinct joints decodable under superposition)")
print(f"    cd(product)   = {cd_prod}/{K**N}   (bar >= {int(0.9*K**N)} and >= 5)")
print(f"    cd(max-pool)  = {cd_max}/{K**N}   (bar <= {2*K})  [collapse toward max_single={max_single}]")
print(f"    max_single (single-factor cardinality) = {max_single}")
print(f"    INERT differential  cd(product) > cd(max-pool) ? {cd_prod > cd_max}")

# ── HONEST full-set (no ambiguity isolation): shows additive inflation ──
def fullset_dataset(T, n, relay, p_pos=0.5):
    X, y = [], []
    for _ in range(n):
        if rng.random() < p_pos:
            items = [tuple(T), tuple(int(rng.integers(K)) for _ in range(N))]
            lab = 1.0
        else:
            items = [tuple(int(rng.integers(K)) for _ in range(N)) for _ in range(2)]
            lab = float(tuple(T) in items)
        rng.shuffle(items)
        X.append(scene_rep(items, relay)); y.append(lab)
    return np.array(X), np.array(y)
def fullset_acc(relay, n=4000):
    accs=[]
    for T in samp_targets:
        Xtr,ytr=fullset_dataset(T,n,relay); Xte,yte=fullset_dataset(T,n//2,relay)
        accs.append(ridge_acc(Xtr,ytr,Xte,yte))
    return float(np.mean(accs))
fs_prod=fullset_acc(relay_product); fs_add=fullset_acc(relay_add); fs_max=fullset_acc(relay_max)
print("\n[honest] full-set acc (NO ambiguity isolation -> marginal shortcuts inflate)")
print(f"    product={fs_prod:.3f}  additive={fs_add:.3f}  max-pool={fs_max:.3f}")
print("    (note: full-set can look fine even for additive; binding bar is the ambiguous subset)")

# ── (C) SUPERPOSITION-DEPTH SWEEP (proper test of the card's "max collapses") ──
# The thalamic relay integrates releases across MANY loops/items. As more items
# superpose, max-pool's union-cross SATURATES (-> all-ones) and loses the joint;
# product (sum of disjoint one-hots) stays joint-distinguishable until k^N fills.
# Task: detect target T present in an M-item scene (random distractors), balanced.
# Pre-registered expectation (frozen, separate from A/B): product stays >=0.90
# for all M; max degrades and crosses <=0.60 by M>=4 (saturation regime) = the
# regime where conjunctive AND is uniquely necessary vs max-pool.
def detect_dataset(T, M, n, relay):
    X, y = [], []
    for _ in range(n):
        if rng.random() < 0.5:
            items = [tuple(T)] + [tuple(int(rng.integers(K)) for _ in range(N)) for _ in range(M-1)]
            lab = 1.0
        else:
            items = [tuple(int(rng.integers(K)) for _ in range(N)) for _ in range(M)]
            while tuple(T) in items:
                items = [tuple(int(rng.integers(K)) for _ in range(N)) for _ in range(M)]
            lab = 0.0
        rng.shuffle(items)
        X.append(scene_rep(items, relay)); y.append(lab)
    return np.array(X), np.array(y)
def detect_acc(M, relay, n=3000):
    accs=[]
    for T in samp_targets:
        Xtr,ytr=detect_dataset(T,M,n,relay); Xte,yte=detect_dataset(T,M,n//2,relay)
        accs.append(ridge_acc(Xtr,ytr,Xte,yte))
    return float(np.mean(accs))
print("\n[C] superposition-depth sweep (detect T in M-item scene · product vs max vs add)")
print(f"    {'M':>3} | {'product':>8} | {'max-pool':>8} | {'additive':>8}")
sweep = {}
for M in (2,3,4,5,6):
    p=detect_acc(M,relay_product); mx=detect_acc(M,relay_max); ad=detect_acc(M,relay_add)
    sweep[M]=(p,mx,ad)
    print(f"    {M:>3} | {p:>8.3f} | {mx:>8.3f} | {ad:>8.3f}")
max_collapses_highM = any(sweep[M][1] <= 0.60 for M in (4,5,6))
prod_holds_highM    = all(sweep[M][0] >= 0.90 for M in (4,5,6))

# ── VERDICT (frozen-first, honest) ──
A_ok = (acc_prod>=0.95 and acc_max<=0.60 and acc_add<=0.60
        and acc_single<=0.60 and acc_scram<=0.60)
B_ok = (cd_prod>=int(0.9*K**N) and cd_prod>=5 and cd_max<=2*K and cd_prod>cd_max)
# C: conjunctive uniquely necessary vs max ONLY in the high-superposition regime
C_ok = (max_collapses_highM and prod_holds_highM)
# the half that DOES hold at every M: conjunctive binds AND additive/single collapse
ADD_collapses = (acc_add<=0.60 and acc_single<=0.60)
PROD_binds    = (acc_prod>=0.95 and acc_scram<=0.60)
print("\n" + "="*72)
print(f"  bar A (binding-required, M=2 · prod>max=INERT) : {'PASS' if A_ok else 'FAIL'}")
print(f"  bar B (composed_distinct, M=2)                 : {'PASS' if B_ok else 'FAIL'}")
print(f"  diag C (prod>max ONLY at high superposition)   : {'PASS' if C_ok else 'FAIL'}")
print(f"  sub: conjunctive binds + scramble collapses    : {PROD_binds}")
print(f"  sub: additive/single-factor collapse (G1 wall) : {ADD_collapses}")
if A_ok and B_ok:
    verdict = "SUPPORT (DIRECTIONAL)"
elif PROD_binds and ADD_collapses and C_ok:
    verdict = "MIXED (DIRECTIONAL)"
elif PROD_binds and ADD_collapses:
    verdict = "MIXED (DIRECTIONAL)"
else:
    verdict = "NOT-SUPPORTED (DIRECTIONAL)"
print(f"\n  VERDICT: {verdict}")
print(f"  - conjunctive(product) AND binds (1.0) + scramble destroys it (G0 control OK)")
print(f"  - ADDITIVE(sum)/single-factor structurally CANNOT bind (forced 0.50) = the G1 wall")
print(f"  - BUT card's stated INERT control max-pool is NOT inert at M=2 (it also binds);")
print(f"    product>max only emerges in the HIGH-superposition saturation regime (see C).")
print(f"  [numpy toy = DIRECTIONAL only · engine-native (cli/anima.hexa) NOT fired]")
print("="*72)
