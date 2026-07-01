"""
H_1863 — token-AR -> diffusion joint denoising (classifier-free dual guidance)
DIRECTIONAL numpy probe (NEVER terminal; numpy mirror by construction).

QUESTION (anima G1 combination-operator floor):
  Does ITERATIVE joint denoising over two INDEPENDENT condition score-fields
  make the CONJUNCTION of two distant concepts reachable, above the
  ADDITIVE-READOUT (one-shot argmax of the summed score) floor?

  anima wall: additive trunk readout of two concept score-fields = per-position
  mean-field argmax -> cannot satisfy a GLOBAL, non-separable joint constraint
  (readout/tension/predictive/multiplicative/NMDA binding all 🧱 NOT-SUP).
  H_1863/H_1622 lever = the SAME additive guidance score
  s = s0 + wa(sa-s0) + wb(sb-s0), BUT applied ITERATIVELY (T global denoise
  sweeps) so the sample settles into the INTERSECTION of both gradient fields.
  So the operator under test = ITERATION, not a new score algebra.

TASK (2 INDEPENDENT concepts, non-separable / distant coupling):
  x in {0,1}^L.
  Concept A (structure leg): a random perfect matching of the L positions into
    L/2 pairs, each pair (i,j) has a required XOR r_ij. Couples DISTANT positions.
  Concept B (global-value leg): required popcount S (total number of 1s).
  JOINT-satisfy iff ALL pair-XOR constraints hold AND popcount(x)==S.
  The two legs are independent: A ignores popcount, B ignores pairing.
  Per-position greedy cannot satisfy XOR frustration + a global count in one shot.

METHODS:
  additive_floor  = one-shot mean-field: per-position P(x_i=1) prop exp(beta*local
                    combined score) from uniform prior, then argmax. (= additive
                    readout of summed score-field, the walled floor; == operator T=1)
  operator_T      = H_1863 diffusion: start random, run T annealed Gibbs denoise
                    sweeps under the SAME combined energy sa+sb; each sweep
                    resamples every position given the rest (global re-decision).
  op_wb0          = ablation: operator but wb=0 (leg A only) -> must NOT solve joint.

METRIC: composed_frac = fraction of N independent random (A,B) tasks for which the
  method returns a fully JOINT-satisfying x. reachability of the conjunction.

FROZEN BAR (pre-registered BEFORE run, no tune-to-green, p7):
  GREEN-DIRECTIONAL REACHABLE iff:
    operator composed_frac >= 0.60
    AND additive_floor composed_frac <= 0.25
    AND (operator - additive) >= 0.35
    AND op_wb0 composed_frac <= additive_floor + 0.10   (both legs needed)
  else -> DIRECTIONAL floor / FALSIFIED (operator INERT, ~dup of additive wall).
"""
import numpy as np

RNG = np.random.default_rng(1863)
L = 12
N = 250
T = 60          # denoise sweeps for operator
BETA0, BETA1 = 0.3, 6.0   # annealing (noise->clean) schedule

def make_task():
    perm = RNG.permutation(L)
    pairs = perm.reshape(L//2, 2)
    rxor = RNG.integers(0, 2, size=L//2)         # required XOR per pair
    # choose a satisfiable popcount: build one witness then use its popcount
    # witness: for each pair set (a,b) with a XOR b = rxor by random base
    x0 = np.zeros(L, dtype=np.int64)
    for k,(i,j) in enumerate(pairs):
        bi = RNG.integers(0,2)
        x0[i] = bi
        x0[j] = bi ^ rxor[k]
    S = int(x0.sum())                            # a reachable target popcount
    return pairs, rxor, S

def energy_terms(x, pairs, rxor, S):
    # sa: -violated pair constraints ; sb: -|popcount-S|
    viol = 0
    for k,(i,j) in enumerate(pairs):
        if (x[i]^x[j]) != rxor[k]:
            viol += 1
    sa = -viol
    sb = -abs(int(x.sum()) - S)
    return sa, sb

def satisfied(x, pairs, rxor, S):
    sa, sb = energy_terms(x, pairs, rxor, S)
    return (sa == 0) and (sb == 0)

def combined_delta(x, pos, pairs, rxor, S, wa, wb):
    # score of flipping position `pos` to value v in {0,1}: return score for v=1 minus v=0
    # local contribution: pairs touching pos + popcount term
    def local_score(val):
        s_a = 0
        # only the pair containing pos matters for sa change
        for k,(i,j) in enumerate(pairs):
            if i==pos or j==pos:
                other = x[j] if i==pos else x[i]
                s_a += 0 if (val^other)==rxor[k] else -1
                break
        cur_sum = int(x.sum()) - x[pos] + val
        s_b = -abs(cur_sum - S)
        return wa*s_a + wb*s_b
    return local_score(1) - local_score(0)

def additive_floor(pairs, rxor, S, beta=4.0, wa=1.0, wb=1.0):
    # one-shot mean-field from UNIFORM prior: x_others ~ 0.5 -> use expected via 0/1 rounding.
    # per-position independent P(x_i=1) from a single pass over uniform baseline (~random start).
    x = RNG.integers(0,2,size=L)   # uniform prior sample as "others"
    out = np.zeros(L, dtype=np.int64)
    for pos in range(L):
        d = combined_delta(x, pos, pairs, rxor, S, wa, wb)
        p1 = 1.0/(1.0+np.exp(-beta*d))
        out[pos] = 1 if p1 >= 0.5 else 0
    return out

def operator(pairs, rxor, S, T=T, wa=1.0, wb=1.0, restarts=3):
    best = None
    for _ in range(restarts):
        x = RNG.integers(0,2,size=L)
        for t in range(T):
            beta = BETA0 + (BETA1-BETA0)*(t/(T-1))
            order = RNG.permutation(L)
            for pos in order:
                d = combined_delta(x, pos, pairs, rxor, S, wa, wb)
                p1 = 1.0/(1.0+np.exp(-beta*d))
                x[pos] = 1 if RNG.random() < p1 else 0
        if satisfied(x, pairs, rxor, S):
            return x  # early exit on success
        if best is None:
            best = x.copy()
    return best

def run(method_name, fn, **kw):
    ok = 0
    for _ in range(N):
        t = make_task()
        x = fn(*t, **kw)
        if satisfied(x, *t):
            ok += 1
    return ok/N

if __name__ == "__main__":
    frac_add = run("additive", additive_floor)
    frac_op  = run("operator", operator)
    frac_wb0 = run("op_wb0", lambda *t: operator(*t, wb=0.0))
    margin = frac_op - frac_add
    print(f"L={L} N={N} T={T} anneal beta {BETA0}->{BETA1}")
    print(f"additive_floor composed_frac = {frac_add:.3f}")
    print(f"operator(T)    composed_frac = {frac_op:.3f}")
    print(f"op_wb0(legA)   composed_frac = {frac_wb0:.3f}")
    print(f"margin (op-add)              = {margin:.3f}")
    print("--- FROZEN BAR: op>=0.60 AND add<=0.25 AND margin>=0.35 AND wb0<=add+0.10 ---")
    green = (frac_op>=0.60) and (frac_add<=0.25) and (margin>=0.35) and (frac_wb0<=frac_add+0.10)
    print("VERDICT:", "GREEN-DIRECTIONAL REACHABLE" if green else "DIRECTIONAL floor / FALSIFIED")
    print("both-legs-needed:", frac_wb0 <= frac_add+0.10)
