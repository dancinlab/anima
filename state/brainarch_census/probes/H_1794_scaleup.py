#!/usr/bin/env python3
# H_1794 SCALE-UP — corticostriatal product-AND binding (mid-rung, resolution-gated)
# ============================================================================
# DIRECTIONAL ONLY (numpy toy, NOT engine-native; a_engine_native_learning).
#
# WHY SCALE UP (a_break_the_wall type-a = measurement artifact):
#   cheap_test (N=3,k=3, joint=27) gave MIXED — product BINDS but max-pool ALSO
#   binds at M=2. Root cause = the k^N space was too small: the max-pool union-
#   "cross" representation never SATURATES at M=2, so it stays joint-separable.
#   The card's stated INERT control (product>max-pool) only emerges when the relay
#   integrates enough items that max-pool's union loses the joint. That is a
#   RESOLUTION limit, not a science ceiling → scale k,N (joint space) so the
#   product-vs-max-pool difference becomes MEASURABLE.
#
# SCALE-UP: N=4 factor-loops, k=5 value-slots  (joint space k^N = 625, was 27).
#   bigger feature space + superposition-depth sweep M=2..6.  re-check whether
#   PRODUCT is uniquely binding vs additive / single / AND vs MAX-POOL.
#
# RESOLUTION GATE (must pass before the INERT verdict is meaningful):
#   GROK-CTRL = at THIS scale, the max-pool relay must COLLAPSE (<=0.60) somewhere
#   in the depth sweep where the product relay HOLDS (>=0.90). If max-pool never
#   collapses, this rung STILL cannot resolve product-vs-max (same as cheap) ->
#   report "next rung (larger k^N) needed", do NOT stamp the INERT differential.
#   (additive/single collapsing is structural and already resolved; the open
#    question is the product>max-pool INERT claim, so THAT is the resolution test.)
#
# FROZEN BARS (cheap thresholds rescaled to k^N — tune-to-green 금지, p7/c9):
#   A) BINDING-REQUIRED (ambiguous subset, M=2, learned ridge readout):
#        product ambig_acc   >= 0.95
#        max-pool (INERT)     <= 0.60   [now expected to hold at larger k^N]
#        additive(sum,INERT)  <= 0.60
#        single-factor base   <= 0.60
#        scramble (G0)        <= 0.60
#   B) composed_distinct (G1/G2 capacity, M=2):
#        cd(product) >= 0.9*k^N AND >= 5
#        cd(max-pool) <= 2*k
#        cd(product) > cd(max-pool)        [INERT differential]
#   C) depth sweep (the resolution-defining regime):
#        product >= 0.90 for all M in {4,5,6}; max-pool <= 0.60 for some M in {4,5,6}
#   VERDICT(DIRECTIONAL): SUPPORT iff A AND B ; MIXED if product binds & add/single
#     collapse but max-pool INERT only at high M (C) ; else NOT-SUPPORTED.
# ============================================================================
import numpy as np, itertools, time

rng = np.random.default_rng(7)
N, K = 4, 5                      # 4 factor-loops, k=5  -> joint space 625
JOINTS = list(itertools.product(range(K), repeat=N))
assert len(JOINTS) == K**N
SAMP = 8                         # sampled targets for the (expensive) ambig/sweep aggregates

def eye_k(v):
    e = np.zeros(K); e[v] = 1.0; return e
def relay_product(item):
    o = eye_k(item[0])
    for i in range(1, N): o = np.multiply.outer(o, eye_k(item[i]))
    return o.ravel()             # dim k^N one-hot at the joint
def relay_max(item):
    grid = np.zeros([K]*N); r = [eye_k(item[i]) for i in range(N)]
    for idx in JOINTS: grid[idx] = max(r[i][idx[i]] for i in range(N))
    return grid.ravel()
def relay_add(item):
    return np.concatenate([eye_k(item[i]) for i in range(N)])   # dim N*k
def relay_single(item):
    return eye_k(item[0])
def scene_rep(items, relay):
    return sum(relay(it) for it in items)

def diff_triple(T):
    return tuple((T[i] + 1 + int(rng.integers(K-1))) % K for i in range(N))
def ambig_pair(T):
    D = diff_triple(T)
    pos = [tuple(T), D]
    neg = [tuple(T[:N-1]) + (D[N-1],), D[:N-1] + (T[N-1],)]   # swap last factor: identical marginals
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

print("="*78)
print("H_1794 SCALE-UP  corticostriatal product-AND binding — mid-rung numpy [DIRECTIONAL]")
print(f"  N={N} factor-loops · k={K} value-slots · joint space k^N={K**N} (was 27)")
print("="*78)
t0 = time.time()

samp_targets = [JOINTS[i] for i in rng.choice(len(JOINTS), SAMP, replace=False)]

def aggregate_ambig(relay, n_each=300, targets=None):
    targets = targets or samp_targets; accs = []
    for T in targets:
        Xtr, ytr = ambig_dataset(T, n_each, relay)
        Xte, yte = ambig_dataset(T, n_each//2, relay)
        accs.append(ridge_acc(Xtr, ytr, Xte, yte))
    return float(np.mean(accs))

def relay_product_scram_dataset(T, n):
    X, y = [], []
    for _ in range(n):
        perm = [rng.permutation(K) for _ in range(N)]
        sc = lambda it: tuple(int(perm[i][it[i]]) for i in range(N))
        pos, neg = ambig_pair(T)
        X.append(scene_rep([sc(it) for it in pos], relay_product)); y.append(1.0)
        X.append(scene_rep([sc(it) for it in neg], relay_product)); y.append(0.0)
    return np.array(X), np.array(y)
def aggregate_scram(targets, n_each=300):
    accs = []
    for T in targets:
        Xtr,ytr=relay_product_scram_dataset(T,n_each); Xte,yte=relay_product_scram_dataset(T,n_each//2)
        accs.append(ridge_acc(Xtr,ytr,Xte,yte))
    return float(np.mean(accs))

acc_prod   = aggregate_ambig(relay_product)
acc_max    = aggregate_ambig(relay_max)
acc_add    = aggregate_ambig(relay_add)
acc_single = aggregate_ambig(relay_single)
acc_scram  = aggregate_scram(samp_targets)

print("\n[A] BINDING-REQUIRED (ambiguous subset · identical marginals, diff joint · M=2)")
print(f"    conjunctive(product) ambig_acc = {acc_prod:.3f}   (bar >= 0.95)")
print(f"    max-pool   (INERT)   ambig_acc = {acc_max:.3f}   (bar <= 0.60)")
print(f"    additive(sum,INERT)  ambig_acc = {acc_add:.3f}   (bar <= 0.60)")
print(f"    single-factor(max_single)      = {acc_single:.3f}   (bar <= 0.60)")
print(f"    scramble cortico-striatal(G0)  = {acc_scram:.3f}   (bar <= 0.60)")

# (B) composed_distinct — sample (k^N=625 too many to do all; use sampled targets *4)
cd_targets = [JOINTS[i] for i in rng.choice(len(JOINTS), 40, replace=False)]
def composed_distinct(relay, thr=0.95, n_each=200):
    cnt = 0
    for T in cd_targets:
        Xtr, ytr = ambig_dataset(T, n_each, relay)
        Xte, yte = ambig_dataset(T, n_each//2, relay)
        if ridge_acc(Xtr, ytr, Xte, yte) >= thr: cnt += 1
    return cnt, len(cd_targets)
cd_prod, cdN = composed_distinct(relay_product)
cd_max, _    = composed_distinct(relay_max)
max_single = K
print("\n[B] composed_distinct (sampled 40 of k^N joints decodable under superposition)")
print(f"    cd(product)   = {cd_prod}/{cdN}   (bar: >=0.9*sample={int(0.9*cdN)} and >=5)")
print(f"    cd(max-pool)  = {cd_max}/{cdN}   (bar <= {2*K})  [collapse toward max_single={max_single}]")
print(f"    INERT differential  cd(product) > cd(max-pool) ? {cd_prod > cd_max}")

# (C) superposition-depth sweep — the resolution-defining regime
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
        rng.shuffle(items); X.append(scene_rep(items, relay)); y.append(lab)
    return np.array(X), np.array(y)
def detect_acc(M, relay, n=2000):
    accs = []
    for T in samp_targets:
        Xtr,ytr=detect_dataset(T,M,n,relay); Xte,yte=detect_dataset(T,M,n//2,relay)
        accs.append(ridge_acc(Xtr,ytr,Xte,yte))
    return float(np.mean(accs))
print("\n[C] superposition-depth sweep (detect T in M-item scene · product vs max vs add)")
print(f"    {'M':>3} | {'product':>8} | {'max-pool':>8} | {'additive':>8}")
sweep = {}
for M in (2,3,4,5,6):
    p=detect_acc(M,relay_product); mx=detect_acc(M,relay_max); ad=detect_acc(M,relay_add)
    sweep[M]=(p,mx,ad); print(f"    {M:>3} | {p:>8.3f} | {mx:>8.3f} | {ad:>8.3f}")
max_collapses_highM = any(sweep[M][1] <= 0.60 for M in (4,5,6))
prod_holds_highM    = all(sweep[M][0] >= 0.90 for M in (4,5,6))

# ---- RESOLUTION GATE: can this rung resolve product-vs-max-pool at all? ----
resolution_ok = (acc_max <= 0.60) or (max_collapses_highM and prod_holds_highM)
print("\n[RESOLUTION GATE] product-vs-max-pool resolvable at this k^N?")
print(f"    max-pool ambig (M=2) <= 0.60 OR max collapses at high-M while product holds : {resolution_ok}")
print(f"    -> {'[resolution acquired: max-pool INERT measurable]' if resolution_ok else '[STILL under-powered -> larger k^N rung needed]'}")

A_ok = (acc_prod>=0.95 and acc_max<=0.60 and acc_add<=0.60 and acc_single<=0.60 and acc_scram<=0.60)
B_ok = (cd_prod>=int(0.9*cdN) and cd_prod>=5 and cd_max<=2*K and cd_prod>cd_max)
C_ok = (max_collapses_highM and prod_holds_highM)
ADD_collapses = (acc_add<=0.60 and acc_single<=0.60)
PROD_binds    = (acc_prod>=0.95 and acc_scram<=0.60)
print("\n" + "="*78)
print(f"  bar A (binding-required, M=2 · prod>max=INERT) : {'PASS' if A_ok else 'FAIL'}")
print(f"  bar B (composed_distinct, M=2)                 : {'PASS' if B_ok else 'FAIL'}")
print(f"  diag C (prod>max at high superposition)        : {'PASS' if C_ok else 'FAIL'}")
print(f"  sub: conjunctive binds + scramble collapses    : {PROD_binds}")
print(f"  sub: additive/single-factor collapse (G1 wall) : {ADD_collapses}")
if not resolution_ok:
    verdict = "UNDER-POWERED (resolution gate FAIL — larger k^N rung needed)"
elif A_ok and B_ok:
    verdict = "SUPPORT (DIRECTIONAL)"
elif PROD_binds and ADD_collapses:
    verdict = "MIXED (DIRECTIONAL)"
else:
    verdict = "NOT-SUPPORTED (DIRECTIONAL)"
print(f"\n  VERDICT: {verdict}")
print(f"  [numpy toy = DIRECTIONAL only · engine-native (cli/anima.hexa) NOT fired]  elapsed={time.time()-t0:.0f}s")
print("="*78)
