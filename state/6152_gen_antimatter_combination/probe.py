# H_6152 antimatter combination — numpy DIRECTIONAL screen (NOT terminal; numpy overstates, cf H_6112).
# Mechanism: concept/anti-concept annihilation-creation symmetry; combination = partial annihilation, then residual.
# G1 recombination toy: 2 INDEPENDENT parent concepts A,B -> a COMPOSED concept must be a
#   novel point that is (i) distinct from BOTH parents (not a blend), and (ii) pair-distinct
#   (compositions don't collapse together). This mirrors the wall's "isolated novel point" + distinctness.
#
# metric composed_distinct = # pairs where op(A,B) satisfies BOTH:
#   (i)  max(cos(c,A), cos(c,B)) < 0.50   (far from both parents = novel, not a midpoint blend)
#   (ii) c is uniquely nearest to itself among all compositions (nearest other comp cos < 0.90 = not collapsed)
#
# Operators compared:
#   additive     : normalize(A+B)                              -- the WALLED floor (H_1816/1834)
#   antimatter_v1: orthogonal residual (remove mutual proj)    -- linear, ~=additive for indep vecs
#   antimatter_v2: SIGN-GATED annihilation-creation (nonlinear):
#                    same-sign dims annihilate (A_k - B_k), opposite-sign dims reinforce (A_k + B_k)
#
# FROZEN BAR (set BEFORE run): an operator is GREEN-DIRECTIONAL iff its composed_distinct
#   exceeds the additive floor by margin >= ceil(0.15*N) = 4 pairs (N=24). Else FLOOR/FALSIFIED-at-toy.
import numpy as np
rng = np.random.default_rng(6152)
d, N = 64, 24
def unit(x): return x/ (np.linalg.norm(x,axis=-1,keepdims=True)+1e-9)
A = unit(rng.standard_normal((N,d)))
B = unit(rng.standard_normal((N,d)))   # independent parents

def additive(A,B): return unit(A+B)
def antimatter_v1(A,B):
    dot=(A*B).sum(1,keepdims=True)
    return unit((A-dot*B)+(B-dot*A))
def antimatter_v2(A,B):
    same = (np.sign(A)==np.sign(B))
    c = np.where(same, A-B, A+B)
    return unit(c)

def cos(x,y): return (x*y).sum(-1)
def composed_distinct(C):
    ok=0
    S = C@C.T
    np.fill_diagonal(S,-1)
    for i in range(N):
        near_parent = max(cos(C[i],A[i]), cos(C[i],B[i]))
        cond_i = near_parent < 0.50
        cond_ii = S[i].max() < 0.90
        if cond_i and cond_ii: ok+=1
    return ok

for name,op in [("additive",additive),("antimatter_v1",antimatter_v1),("antimatter_v2",antimatter_v2)]:
    C=op(A,B)
    mp = np.array([max(cos(C[i],A[i]),cos(C[i],B[i])) for i in range(N)])
    S=C@C.T; np.fill_diagonal(S,-1); maxoff=S.max(1)
    print(f"{name:14s} composed_distinct={composed_distinct(C):2d}/{N}  "
          f"mean_max_cos_parent={mp.mean():.3f}  mean_max_offdiag={maxoff.mean():.3f}")

floor = composed_distinct(additive(A,B))
margin = int(np.ceil(0.15*N))
print(f"\nFROZEN BAR: beat additive floor(={floor}) by >= {margin} pairs")
for name,op in [("antimatter_v1",antimatter_v1),("antimatter_v2",antimatter_v2)]:
    v=composed_distinct(op(A,B))
    verdict = "GREEN-DIRECTIONAL" if v-floor>=margin else "FLOOR/FALSIFIED-at-toy"
    print(f"  {name:14s} {v}/{N}  lift={v-floor:+d}  -> {verdict}")
