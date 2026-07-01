#!/usr/bin/env python3
"""
H_6137 gen_cls_dual_timescale — ADVERSARIAL DEEPENING (a_break_the_wall type-(d)).

TARGET operator (reconstructed from the cheap numpy screen name/family):
  CLS DUAL-TIMESCALE composition. Compose two parent concept vectors A,B into a
  child C by writing A into a FAST trace (high decay/LR) and B into a SLOW trace
  (low decay/LR), then reading a blended child C = readout(fast, slow). The screen
  scored the G1-style metric `composed_distinct` = # of composed outputs C that
  decode (nearest-codebook) to a token DISTINCT from both parents A and B, and
  reported it going 0 -> 1.0 (normalized REACHABLE) vs an additive floor.

WHY ADVERSARIAL (H_6112 transfer caveat):
  H_6112 PROVED a numpy REACHABLE (0->1.0) can COLLAPSE on the real CLMConvMoE
  trunk (0->0.022). H_1815 (CLS sep/completion on the real CLM, engine-native)
  already showed the CLS composed_distinct 0->1 was **coverage-floor jitter**
  (max_single=0, cov>max_single passes trivially at 0), NOT recombination; the
  ONLY real CLS effect was G2 novelty. So `composed_distinct` distinctness alone
  is NECESSARY-NOT-SUFFICIENT. This probe tries to REFUTE the signal.

FROZEN BAR (set BEFORE running; operator SURVIVES iff ALL three hold):
  (C1) GENERIC-NONLINEARITY control: the dual-timescale op must EXCEED each of
       {tanh(A+B), random-MLP(concat), A*B elementwise} on composed_distinct by
       a margin >= 0.20 (normalized). If a generic nonlinearity MATCHES it, the
       REACHABLE is an artifact of nonlinearity-in-general -> ARTIFACT.
  (C2) BIND-RECOVERABILITY: fit linear readouts C->A and C->B on TRAIN pairs,
       test on HELD-OUT pairs. Mean recovery cosine of the dual-timescale op must
       beat the ADDITIVE baseline (C=A+B) by >= 0.10. distinctness w/o
       recoverability != compositional binding -> ARTIFACT/weak.
  (C3) SHUFFLE/ABLATION: set tau_fast = tau_slow (kill the dual-timescale
       ingredient -> single store). composed_distinct must COLLAPSE to within
       0.05 of the additive floor (proves the ingredient is causal).
  SURVIVES = C1 pass AND C2 pass AND C3 collapse. Else -> ARTIFACT.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "4")
import numpy as np

rng = np.random.default_rng(6137)
D = 24            # concept/key dim
NCON = 40         # codebook size (concept vocabulary)
NPAIR = 200       # parent pairs
TAU_FAST = 0.85   # fast trace retention (dual-timescale)
TAU_SLOW = 0.15   # slow trace retention

# ── codebook of concept vectors (the "vocabulary" C decodes against) ──────────
CODE = rng.standard_normal((NCON, D))
CODE /= np.linalg.norm(CODE, axis=1, keepdims=True)

def decode(v):
    """nearest-codebook token id for a (…,D) batch."""
    vn = v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-9)
    return np.argmax(vn @ CODE.T, axis=-1)

# parent pairs (distinct indices)
ai = rng.integers(0, NCON, NPAIR)
bi = rng.integers(0, NCON, NPAIR)
mask = ai != bi
ai, bi = ai[mask], bi[mask]
A = CODE[ai]      # parent A vectors
B = CODE[bi]      # parent B vectors

def composed_distinct(C, ai, bi):
    """normalized: fraction of composed C that decode to a token != both parents."""
    ci = decode(C)
    novel = (ci != ai) & (ci != bi)
    return float(novel.mean())

# ── THE OPERATOR: CLS dual-timescale composition ──────────────────────────────
def cls_dual(A, B, tf=TAU_FAST, ts=TAU_SLOW):
    # write A first (older), then B; fast trace favors recent (B), slow favors old (A)
    fast = tf*A + (1-tf)*B          # fast store (short memory -> weights recent B less? tuned)
    slow = ts*A + (1-ts)*B          # slow store (long memory -> integrates)
    C = np.tanh(fast) + np.tanh(slow)   # nonlinear dual-store readout
    return C

# ── CONTROLS (generic nonlinearities) ─────────────────────────────────────────
W1 = rng.standard_normal((2*D, D)) / np.sqrt(2*D)
def gen_tanh(A,B):  return np.tanh(A + B)
def gen_mlp(A,B):   return np.tanh(np.concatenate([A,B],axis=-1) @ W1)
def gen_mult(A,B):  return A * B
def additive(A,B):  return A + B

# ── C1 : composed_distinct across operator + generic nonlinearities ───────────
cd_op   = composed_distinct(cls_dual(A,B), ai, bi)
cd_add  = composed_distinct(additive(A,B), ai, bi)
cd_tanh = composed_distinct(gen_tanh(A,B), ai, bi)
cd_mlp  = composed_distinct(gen_mlp(A,B),  ai, bi)
cd_mult = composed_distinct(gen_mult(A,B), ai, bi)

gen_best = max(cd_tanh, cd_mlp, cd_mult)
c1_margin = cd_op - gen_best
C1_PASS = c1_margin >= 0.20

# ── C2 : bind-recoverability (linear readout C->A, C->B on held-out) ──────────
def recover_cos(compose_fn):
    C = compose_fn(A, B)
    n = len(C); ntr = n*2//3
    Ctr, Cte = C[:ntr], C[ntr:]
    # solve least squares W_A: C->A, W_B: C->B on TRAIN, eval on HELD-OUT
    def fit_eval(target):
        Wt, *_ = np.linalg.lstsq(Ctr, target[:ntr], rcond=None)
        pred = Cte @ Wt
        pn = pred/(np.linalg.norm(pred,axis=1,keepdims=True)+1e-9)
        tn = target[ntr:]/(np.linalg.norm(target[ntr:],axis=1,keepdims=True)+1e-9)
        return float((pn*tn).sum(1).mean())
    return 0.5*(fit_eval(A) + fit_eval(B))

rec_op  = recover_cos(cls_dual)
rec_add = recover_cos(additive)
c2_margin = rec_op - rec_add
C2_PASS = c2_margin >= 0.10

# ── C3 : ablation (tau_fast == tau_slow -> single store) ───────────────────────
tau_mid = 0.5*(TAU_FAST+TAU_SLOW)
cd_ablate = composed_distinct(cls_dual(A,B,tf=tau_mid,ts=tau_mid), ai, bi)
c3_gap = abs(cd_ablate - cd_add)
C3_COLLAPSE = c3_gap <= 0.05

SURVIVES = C1_PASS and C2_PASS and C3_COLLAPSE

print("=== H_6137 gen_cls_dual_timescale — ADVERSARIAL DEEPEN ===")
print(f"pairs={len(A)}  D={D}  codebook={NCON}  tau_fast={TAU_FAST} tau_slow={TAU_SLOW}")
print("--- C1 GENERIC-NONLINEARITY (composed_distinct, normalized) ---")
print(f"  operator cls_dual      = {cd_op:.3f}")
print(f"  additive floor A+B     = {cd_add:.3f}")
print(f"  generic tanh(A+B)      = {cd_tanh:.3f}")
print(f"  generic random-MLP     = {cd_mlp:.3f}")
print(f"  generic A*B elemwise   = {cd_mult:.3f}")
print(f"  gen_best={gen_best:.3f}  op-gen_best margin={c1_margin:+.3f}  (bar>=+0.20)  C1_PASS={C1_PASS}")
print("--- C2 BIND-RECOVERABILITY (held-out mean cosine recover A&B from C) ---")
print(f"  operator recover       = {rec_op:.3f}")
print(f"  additive recover       = {rec_add:.3f}")
print(f"  op-add margin={c2_margin:+.3f}  (bar>=+0.10)  C2_PASS={C2_PASS}")
print("--- C3 ABLATION (tau_fast==tau_slow) ---")
print(f"  ablated composed_dist  = {cd_ablate:.3f}")
print(f"  additive floor         = {cd_add:.3f}")
print(f"  gap={c3_gap:.3f}  (collapse if <=0.05)  C3_COLLAPSE={C3_COLLAPSE}")
print("--- VERDICT ---")
print(f"  SURVIVES(all 3)={SURVIVES}")
if not SURVIVES:
    reasons=[]
    if not C1_PASS: reasons.append("generic nonlinearity matches op (metric artifact of nonlinearity-in-general)")
    if not C2_PASS: reasons.append("no bind-recoverability edge over additive (distinct != compositional)")
    if not C3_COLLAPSE: reasons.append("ablation did not collapse to additive floor")
    print("  -> ARTIFACT:", "; ".join(reasons))
else:
    print("  -> CONFIRMED (survives all controls) -> flag real-trunk rung")
print("H_6112 transfer caveat: numpy REACHABLE overstates; real-trunk max_single often 0 (coverage-floor jitter, cf H_1815 CLS engine-native).")
