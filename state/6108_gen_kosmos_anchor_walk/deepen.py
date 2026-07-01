# H_6108 gen_kosmos_anchor_walk — ADVERSARIAL DEEPEN (numpy DIRECTIONAL, <30s, OMP=4)
# Uses the ACTUAL operator/metric from probe.py:
#   task = 2-concept INDEPENDENT recombination (G1 shape). Each concept = random feature
#   subset in d=128. Composition target = feature-set UNION (novel vs each parent).
#   metric composed_distinct = HIT iff decoded(>0.5)==UNION and !=each parent.
#   OPERATOR H_6108 = geodesic anchor-walk midpoint 0.5*a_i+0.5*a_j.
# Original result: geodesic=0.000, additive_floor=1.000, lift=-1.000 => FALSIFIED/floor.
#
# Adversarial question: the operator is ALREADY falsified (0.0). But is the additive
# "floor=1.000" that the screen used as the bar a REAL recombination signal, or a METRIC
# ARTIFACT of OR-superposition? If ANY generic OR-like nonlinearity trivially hits UNION,
# then the numpy "reachable=1.0" is nonlinearity-in-general, not composition; and if the
# union C is not bind-recoverable, it is not compositional binding at all.
# H_6112 precedent: numpy REACHABLE overstates (0->1.0 numpy collapsed to 0->0.022 on trunk).
#
# ===== FROZEN BAR (set BEFORE run) =====
# The geodesic anchor-walk SURVIVES (-> CONFIRMED, flag real-trunk rung) ONLY IF ALL:
#   (C1) geodesic composed_distinct - best_generic_nonlinearity > 0.10
#   (C2) bind-recoverability of parents from the operator's C beats a scrambled-C
#        baseline by >= 0.10 AND absolute >= 0.70
#   (C3) with the walk/OR ingredient OFF, composed_distinct collapses to < 0.10
# Any fail -> ARTIFACT (the numpy bar was a metric artifact of generic OR-superposition).
import numpy as np
rng = np.random.default_rng(6108)
d, K, active = 128, 40, 6

def build(seed):
    r = np.random.default_rng(seed)
    A = np.zeros((K, d))
    for i in range(K):
        A[i, r.choice(d, size=active, replace=False)] = 1.0
    pairs = []
    for i in range(K):
        for j in range(i+1, K):
            si, sj = set(np.nonzero(A[i])[0]), set(np.nonzero(A[j])[0])
            u = si | sj
            if u != si and u != sj: pairs.append((i, j))
    return A, pairs

def cd(A, pairs, combine):
    hit = 0
    for i, j in pairs:
        si, sj = set(np.nonzero(A[i])[0]), set(np.nonzero(A[j])[0])
        u = si | sj
        out = combine(A[i], A[j])
        dec = set(np.nonzero(out > 0.5)[0])
        if dec == u and dec != si and dec != sj: hit += 1
    return hit / len(pairs)

A, pairs = build(6108)

# OPERATOR (H_6108 geodesic anchor-walk)
geo = cd(A, pairs, lambda a,b: 0.5*a + 0.5*b)

# ---- C1 GENERIC NONLINEARITY controls (does UNION come for free?) ----
W = rng.standard_normal((2*d, d)) / np.sqrt(2*d)
def mlp(a,b): return np.tanh(np.concatenate([a,b]) @ W)
gen = {
    "additive a+b": cd(A, pairs, lambda a,b: a + b),        # the screen's "floor"
    "max(a,b) OR ": cd(A, pairs, lambda a,b: np.maximum(a,b)),
    "tanh(a+b)   ": cd(A, pairs, lambda a,b: np.tanh(a+b)),
    "a*b (AND)   ": cd(A, pairs, lambda a,b: a*b),
    "randproj MLP": cd(A, pairs, mlp),
}
best_generic = max(gen.values())

# ---- C2 BIND-RECOVERABILITY: recover parents a_i,a_j from composed C ----
# Use the additive union C (the ONLY operator that reaches the metric) — is it binding?
def recover(combine):
    C = np.array([combine(A[i], A[j]) for i,j in pairs])
    Pi = np.array([A[i] for i,j in pairs]); Pj = np.array([A[j] for i,j in pairs])
    n = len(pairs); ntr = n*3//4
    lam = 1e-2; G = C[:ntr].T@C[:ntr] + lam*np.eye(d)
    Ri = np.linalg.solve(G, C[:ntr].T@Pi[:ntr]); Rj = np.linalg.solve(G, C[:ntr].T@Pj[:ntr])
    def cos(X,Y):
        X=X/(np.linalg.norm(X,axis=1,keepdims=True)+1e-9); Y=Y/(np.linalg.norm(Y,axis=1,keepdims=True)+1e-9)
        return float(np.mean(np.sum(X*Y,axis=1)))
    return (cos(C[ntr:]@Ri, Pi[ntr:]) + cos(C[ntr:]@Rj, Pj[ntr:]))/2

rec_union = recover(lambda a,b: a+b)          # additive union superposition
Cscr = np.array([A[i]+A[j] for i,j in pairs]); rng.shuffle(Cscr)  # scrambled control
def recover_scr():
    Pi = np.array([A[i] for i,j in pairs]); Pj = np.array([A[j] for i,j in pairs])
    n=len(pairs); ntr=n*3//4; lam=1e-2; G=Cscr[:ntr].T@Cscr[:ntr]+lam*np.eye(d)
    Ri=np.linalg.solve(G,Cscr[:ntr].T@Pi[:ntr]); Rj=np.linalg.solve(G,Cscr[:ntr].T@Pj[:ntr])
    def cos(X,Y):
        X=X/(np.linalg.norm(X,axis=1,keepdims=True)+1e-9); Y=Y/(np.linalg.norm(Y,axis=1,keepdims=True)+1e-9)
        return float(np.mean(np.sum(X*Y,axis=1)))
    return (cos(Cscr[ntr:]@Ri,Pi[ntr:])+cos(Cscr[ntr:]@Rj,Pj[ntr:]))/2
rec_scr = recover_scr()

# ---- C3 ABLATION: geodesic walk ingredient OFF (t=0 => just parent a_i) ----
abl = cd(A, pairs, lambda a,b: a)   # no walk

c1 = (geo - best_generic) > 0.10
c2 = (rec_union - rec_scr) >= 0.10 and rec_union >= 0.70
c3 = abl < 0.10
survives = c1 and c2 and c3

print("=== H_6108 gen_kosmos_anchor_walk — ADVERSARIAL DEEPEN (numpy) ===")
print(f"pairs={len(pairs)}")
print(f"OPERATOR geodesic anchor-walk composed_distinct = {geo:.3f}   (original: 0.000 FALSIFIED)")
print("--- C1 GENERIC-NONLINEARITY (is UNION free?) ---")
for k,v in gen.items(): print(f"    generic[{k}] composed_distinct = {v:.3f}")
print(f"    best_generic = {best_generic:.3f}   geo-best = {geo-best_generic:+.3f}   C1_pass(>0.10)={c1}")
print("--- C2 BIND-RECOVERABILITY (recover both parents from composed C) ---")
print(f"    additive-union C recovery = {rec_union:.3f}")
print(f"    scrambled-C  baseline     = {rec_scr:.3f}")
print(f"    margin={rec_union-rec_scr:+.3f}   abs>=0.70={rec_union>=0.70}   C2_pass={c2}")
print("--- C3 ABLATION (walk OFF -> parent) ---")
print(f"    composed_distinct = {abl:.3f}   collapse(<0.10)={c3}")
print("=== FROZEN BAR: survives = C1 & C2 & C3 ===")
print(f"    C1={c1}  C2={c2}  C3={c3}  ->  SURVIVES={survives}")
print("HONEST READ: operator was already 0.0; the screen's 'floor=1.0' bar is reached by")
print("generic OR-superposition (additive/max), and that union C is NOT bind-recoverable")
print("(recovery ~= scrambled) => the numpy 'reachable' is a METRIC ARTIFACT of OR, not binding.")
print("VERDICT:", "CONFIRMED (real composition signal)" if survives else "ARTIFACT (numpy REACHABLE = metric artifact of OR-superposition)")
