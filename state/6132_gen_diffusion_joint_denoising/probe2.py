"""
H_1863 — token-AR -> diffusion joint denoising (dual classifier-free guidance)
DIRECTIONAL numpy probe v2 (clean-conjunction redesign; NEVER terminal).

v1 (probe.py) FALSIFIED on the ablation clause: leg B (popcount) was partly
entailed by leg A, so leg-A-only already hit 0.624 -> not a clean 2-leg
conjunction. v2 makes the two legs GENUINELY INDEPENDENT so leg-A-alone
satisfies the JOINT constraint only by chance (~2^-(L/2)).

TASK: x in {0,1}^L. Two INDEPENDENT random perfect matchings of the L positions:
  Leg A = matching_A with required XOR r_A per pair (relative coupling, distant).
  Leg B = matching_B (a DIFFERENT random matching) with required XOR r_B per pair.
  Both derived from a hidden witness x* so a JOINT solution exists.
  JOINT-satisfy iff ALL leg-A eqs AND ALL leg-B eqs hold.
  Legs are orthogonal: satisfying A gives ~0 purchase on B (independent GF(2) eqs).
  This is a frustrated GF(2) system: per-position greedy gets stuck (binding wall).

METHODS (identical to v1 semantics):
  additive_floor = one-shot mean-field per-position argmax of summed score (walled
                   additive readout; == operator at T=1).
  operator_T     = H_1863 iterative annealed-Gibbs denoise, T sweeps, both legs.
  op_wb0         = ablation: operator with wb=0 (leg A only).

METRIC: composed_frac = frac of N tasks reaching a fully JOINT-satisfying x.

FROZEN BAR (pre-registered BEFORE run, no tune-to-green, p7):
  GREEN-DIRECTIONAL REACHABLE iff:
    operator >= 0.60 AND additive <= 0.25 AND (op-add) >= 0.35
    AND op_wb0 <= additive + 0.10   (both legs genuinely needed)
  else DIRECTIONAL floor / FALSIFIED.
"""
import numpy as np
RNG = np.random.default_rng(18632)
L = 12
N = 250
T = 80
BETA0, BETA1 = 0.3, 6.0

def matching(): 
    return RNG.permutation(L).reshape(L//2, 2)

def make_task():
    xw = RNG.integers(0,2,size=L)           # hidden witness -> guarantees joint sol
    mA, mB = matching(), matching()
    rA = np.array([xw[i]^xw[j] for i,j in mA])
    rB = np.array([xw[i]^xw[j] for i,j in mB])
    return mA, rA, mB, rB

def viol(x, m, r):
    v=0
    for k,(i,j) in enumerate(m):
        if (x[i]^x[j])!=r[k]: v+=1
    return v

def satisfied(x, mA,rA,mB,rB):
    return viol(x,mA,rA)==0 and viol(x,mB,rB)==0

def delta(x, pos, mA,rA,mB,rB, wa, wb):
    # pos is in exactly one A-pair and one B-pair
    def leg(m,r,w):
        for k,(i,j) in enumerate(m):
            if i==pos or j==pos:
                other = x[j] if i==pos else x[i]
                s1 = 0 if (1^other)==r[k] else -1
                s0 = 0 if (0^other)==r[k] else -1
                return w*(s1-s0)
        return 0.0
    return leg(mA,rA,wa)+leg(mB,rB,wb)

def additive_floor(mA,rA,mB,rB, beta=4.0, wa=1.0, wb=1.0):
    x = RNG.integers(0,2,size=L)
    out = np.zeros(L,dtype=np.int64)
    for pos in range(L):
        d = delta(x,pos,mA,rA,mB,rB,wa,wb)
        out[pos] = 1 if 1.0/(1.0+np.exp(-beta*d))>=0.5 else 0
    return out

def operator(mA,rA,mB,rB, T=T, wa=1.0, wb=1.0, restarts=4):
    best=None
    for _ in range(restarts):
        x = RNG.integers(0,2,size=L)
        for t in range(T):
            beta = BETA0+(BETA1-BETA0)*(t/(T-1))
            for pos in RNG.permutation(L):
                d = delta(x,pos,mA,rA,mB,rB,wa,wb)
                x[pos] = 1 if RNG.random()<1.0/(1.0+np.exp(-beta*d)) else 0
        if satisfied(x,mA,rA,mB,rB): return x
        if best is None: best=x.copy()
    return best

def run(fn, **kw):
    ok=0
    for _ in range(N):
        t=make_task()
        if satisfied(fn(*t,**kw), *t): ok+=1
    return ok/N

if __name__=="__main__":
    fa=run(additive_floor); fo=run(operator); fw=run(lambda *t: operator(*t, wb=0.0))
    m=fo-fa
    print(f"L={L} N={N} T={T} anneal {BETA0}->{BETA1} (2 independent GF(2) legs)")
    print(f"additive_floor composed_frac = {fa:.3f}")
    print(f"operator(T)    composed_frac = {fo:.3f}")
    print(f"op_wb0(legA)   composed_frac = {fw:.3f}")
    print(f"margin (op-add)              = {m:.3f}")
    print("--- FROZEN BAR: op>=0.60 AND add<=0.25 AND margin>=0.35 AND wb0<=add+0.10 ---")
    green=(fo>=0.60)and(fa<=0.25)and(m>=0.35)and(fw<=fa+0.10)
    print("both-legs-needed:", fw<=fa+0.10)
    print("VERDICT:", "GREEN-DIRECTIONAL REACHABLE" if green else "DIRECTIONAL floor / FALSIFIED")
