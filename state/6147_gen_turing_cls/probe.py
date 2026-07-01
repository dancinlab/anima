# H_6147 Turing-CLS (#11+#34) — numpy DIRECTIONAL reachability probe (transfer-UNVERIFIED)
# Mechanism: slow lane = morphogen source (D_u small), fast lane = diffusion (D_v large),
#            combination = Turing pattern-formation sequence. This runs the never-measured
#            H_1655/H_1734 cheap_test with the CLS two-timescale framing.
#
# TASK: 2 INDEPENDENT binary concepts a,b in {0,1}. Target = XOR(a,b) — the canonical
#       conjunction that a LINEAR/ADDITIVE readout of independent features CANNOT decode.
#       XOR is chosen because it is exactly the "composition an additive trunk collapses on".
#
# We compare THREE readouts, each = a frozen linear least-squares probe fit on a train split
# of noisy per-combo samples and scored on a held-out split (composed reachability = XOR acc):
#   (1) ADDITIVE floor      : linear probe on raw source means [mean(u0), mean(v0)]  (no dynamics)
#   (2) OPERATOR (Turing/CLS): differential diffusion D_v >> D_u + nonlinear reaction u*v,
#                             evolve T steps, read steady pattern features -> linear probe
#   (3) ABLATION (equal-diff): SAME nonlinear reaction but D_u == D_v (kills the CLS timescale
#                             separation / Turing instability). Isolates whether the *timescale
#                             separation* is the lever vs. the pointwise nonlinearity alone.
#
# FROZEN BAR (set BEFORE run, no tune-to-green, p7):
#   GREEN-DIRECTIONAL iff  operator_acc >= 0.70  AND  additive_acc <= 0.60
#                    AND  margin(op-add) >= 0.15  AND  ABLATION FAILS: equal_acc <= additive_acc + 0.10
#   (the ablation clause is load-bearing: if equal-diffusion ALSO passes, the Turing/CLS
#    timescale-separation is INERT and the lift is just pointwise nonlinearity = readout trick
#    that H_1816/1823/1834 showed collapses in the additive trunk -> FALSIFIED-as-stated.)
import numpy as np
rng = np.random.default_rng(6147)

N_GRID = 24        # 1D ring cells
T_STEPS = 40
D_U_SLOW = 0.05    # slow lane (morphogen source)
D_V_FAST = 0.50    # fast lane (diffusion)  -> D_v >> D_u = CLS timescale separation
SAMPLES = 120      # per combo
NOISE = 0.15

def laplacian_ring(x):
    return np.roll(x,1) + np.roll(x,-1) - 2*x

def evolve(a, b, D_u, D_v, seed):
    r = np.random.default_rng(seed)
    # slow lane u seeded by concept a; fast lane v seeded by concept b (independent)
    u = 0.5 + (a-0.5)*0.4 + r.normal(0, NOISE, N_GRID)
    v = 0.5 + (b-0.5)*0.4 + r.normal(0, NOISE, N_GRID)
    for _ in range(T_STEPS):
        # Gray-Scott-like activator-inhibitor with nonlinear cross term u*v
        uv = u*v*u  # activator autocatalysis * inhibitor
        du = D_u*laplacian_ring(u) - uv + 0.045*(1.0-u)
        dv = D_v*laplacian_ring(v) + uv - (0.045+0.062)*v
        u = np.clip(u + du, -3, 3); v = np.clip(v + dv, -3, 3)
    return u, v

def pattern_feats(u, v):
    # steady pattern statistics (translation-invariant-ish): moments + spatial-freq energy
    fu = np.abs(np.fft.rfft(u))[:6]; fv = np.abs(np.fft.rfft(v))[:6]
    return np.concatenate([[u.mean(),u.std(),v.mean(),v.std(),(u*v).mean()], fu, fv])

def build(D_u, D_v, additive=False):
    X, Y = [], []
    for s in range(SAMPLES):
        for a in (0,1):
            for b in (0,1):
                seed = 1000*s + 10*a + b
                if additive:
                    r = np.random.default_rng(seed)
                    u0 = 0.5+(a-0.5)*0.4 + r.normal(0,NOISE,N_GRID)
                    v0 = 0.5+(b-0.5)*0.4 + r.normal(0,NOISE,N_GRID)
                    feat = np.array([u0.mean(), v0.mean(), (u0.mean())**2, (v0.mean())**2])
                else:
                    u,v = evolve(a,b,D_u,D_v,seed)
                    feat = pattern_feats(u,v)
                X.append(feat); Y.append(a ^ b)
    return np.array(X), np.array(Y)

def probe_acc(X, Y):
    # frozen linear least-squares probe, held-out 40% test split, 1-vs target regression
    n = len(Y); idx = rng.permutation(n); cut = int(0.6*n)
    tr, te = idx[:cut], idx[cut:]
    Xtr = np.column_stack([X[tr], np.ones(len(tr))])
    Xte = np.column_stack([X[te], np.ones(len(te))])
    # standardize by train stats
    mu = Xtr[:,:-1].mean(0); sd = Xtr[:,:-1].std(0)+1e-8
    Xtr[:,:-1]=(Xtr[:,:-1]-mu)/sd; Xte[:,:-1]=(Xte[:,:-1]-mu)/sd
    w,_,_,_ = np.linalg.lstsq(Xtr, Y[tr]*2.0-1.0, rcond=None)
    pred = (Xte@w > 0).astype(int)
    return (pred == Y[te]).mean()

Xa,Ya = build(0,0,additive=True)
add_acc = probe_acc(Xa,Ya)
Xo,Yo = build(D_U_SLOW, D_V_FAST)
op_acc = probe_acc(Xo,Yo)
Xe,Ye = build(0.5, 0.5)   # equal diffusion ablation
eq_acc = probe_acc(Xe,Ye)

margin = op_acc - add_acc
print(f"TASK: XOR of 2 independent binary concepts, ring N={N_GRID} T={T_STEPS}")
print(f"CLS timescales: D_u(slow morphogen)={D_U_SLOW}  D_v(fast diffusion)={D_V_FAST}")
print(f"additive_floor  XOR acc = {add_acc:.3f}")
print(f"operator(Turing/CLS) acc = {op_acc:.3f}")
print(f"ablation(equal-diff) acc = {eq_acc:.3f}")
print(f"margin (op-add)          = {margin:.3f}")
print("--- FROZEN BAR: op>=0.70 AND add<=0.60 AND margin>=0.15 AND eq<=add+0.10 (ablation must FAIL) ---")
op_pass  = op_acc >= 0.70
add_pass = add_acc <= 0.60
mrg_pass = margin >= 0.15
abl_pass = eq_acc <= add_acc + 0.10   # equal-diff must NOT match operator (timescale sep is the lever)
print(f"op>=0.70: {op_pass} | add<=0.60: {add_pass} | margin>=0.15: {mrg_pass} | ablation-fails(eq<=add+.10): {abl_pass}")
green = op_pass and add_pass and mrg_pass and abl_pass
print(f"VERDICT: {'GREEN-DIRECTIONAL (numpy, transfer-UNVERIFIED)' if green else 'DIRECTIONAL floor / FALSIFIED-as-stated'}")
print(f"timescale-separation-is-lever: {abl_pass}")
