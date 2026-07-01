# H_6147 Turing-CLS — ADVERSARIAL DEEPENING probe (numpy, transfer-UNVERIFIED, terminal 아님)
# Parent probe (probe.py) already FALSIFIED-as-stated: op=0.969 add=0.521 eq(ablation)=0.651
#   -> the equal-diffusion ablation FAILED (0.651 > add+0.10=0.621): the nonlinear reaction u*v
#      leaks XOR-lift even with the CLS timescale-separation removed. Here we press HARDER with
#      the two controls the parent probe did NOT run.
#
# CONTROLS (a_break_the_wall multi-lens):
#  (C1) GENERIC-NONLINEARITY  — replace the whole Turing RD operator with a *generic* nonlinearity
#       that has NO diffusion / NO reaction / NO timescale structure:
#         C1a = elementwise interaction feature [u0.mean, v0.mean, u0.mean*v0.mean]  (a*b term)
#         C1b = frozen random-projection tanh MLP on raw [u0,v0]  (generic 2-layer nonlinearity)
#       If a GENERIC nonlinearity ALSO reaches the operator's XOR acc, then the operator's
#       REACHABLE is a METRIC ARTIFACT of nonlinearity-in-general, NOT the Turing/CLS mechanism.
#  (C2) BIND-RECOVERABILITY  — the real composition test: from the COMPOSED state C, can BOTH
#       parents a AND b be linearly recovered on HELD-OUT pairs? distinctness/XOR-acc is NECESSARY
#       not SUFFICIENT. We fit C->a and C->b and compare operator vs generic vs additive.
#  (C3) ablation (equal-diff) — re-confirmed from parent probe (timescale-sep OFF must collapse).
#
# FROZEN BAR (set BEFORE run, no tune-to-green, p7):
#   Operator SURVIVES (CONFIRMED, flag real-trunk rung) ONLY IF ALL of:
#     (B1) generic-nonlinearity does NOT match operator:  op_acc - max(C1a,C1b) >= 0.15
#     (B2) bind-recoverability beats additive by margin :  min(recA_op,recB_op) - min(recA_add,recB_add) >= 0.15
#          AND is genuinely above chance:                  min(recA_op,recB_op) >= 0.70
#     (B3) ablation collapses (timescale-sep causal)     :  eq_acc <= add_acc + 0.10
#   If (B1) fails -> ARTIFACT (generic nonlinearity matches). If (B2) fails -> ARTIFACT/weak (no bind).
import os
os.environ.setdefault("OMP_NUM_THREADS","4")
import numpy as np
rng = np.random.default_rng(6147)

N_GRID=24; T_STEPS=40; D_U_SLOW=0.05; D_V_FAST=0.50; SAMPLES=120; NOISE=0.15

def laplacian_ring(x): return np.roll(x,1)+np.roll(x,-1)-2*x

def seed_lanes(a,b,seed):
    r=np.random.default_rng(seed)
    u=0.5+(a-0.5)*0.4+r.normal(0,NOISE,N_GRID)
    v=0.5+(b-0.5)*0.4+r.normal(0,NOISE,N_GRID)
    return u,v

def evolve(a,b,D_u,D_v,seed):
    u,v=seed_lanes(a,b,seed)
    for _ in range(T_STEPS):
        uv=u*v*u
        du=D_u*laplacian_ring(u)-uv+0.045*(1.0-u)
        dv=D_v*laplacian_ring(v)+uv-(0.045+0.062)*v
        u=np.clip(u+du,-3,3); v=np.clip(v+dv,-3,3)
    return u,v

def pattern_feats(u,v):
    fu=np.abs(np.fft.rfft(u))[:6]; fv=np.abs(np.fft.rfft(v))[:6]
    return np.concatenate([[u.mean(),u.std(),v.mean(),v.std(),(u*v).mean()],fu,fv])

# frozen random-projection tanh MLP (generic nonlinearity, NO dynamics)
W_RP=rng.normal(0,1.0,(16,2*N_GRID)); b_RP=rng.normal(0,0.3,16)
def generic_mlp_feats(u0,v0):
    x=np.concatenate([u0,v0])
    return np.tanh(W_RP@x + b_RP)

def build(kind):
    X,Y,A,B=[],[],[],[]
    for s in range(SAMPLES):
        for a in (0,1):
            for b in (0,1):
                seed=1000*s+10*a+b
                if kind=="additive":
                    u0,v0=seed_lanes(a,b,seed)
                    feat=np.array([u0.mean(),v0.mean(),u0.mean()**2,v0.mean()**2])
                elif kind=="operator":
                    u,v=evolve(a,b,D_U_SLOW,D_V_FAST,seed); feat=pattern_feats(u,v)
                elif kind=="ablation":
                    u,v=evolve(a,b,0.5,0.5,seed); feat=pattern_feats(u,v)
                elif kind=="C1a_interaction":     # generic elementwise a*b interaction, no dynamics
                    u0,v0=seed_lanes(a,b,seed)
                    m,n=u0.mean(),v0.mean()
                    feat=np.array([m,n,m*n])
                elif kind=="C1b_mlp":             # generic random-proj tanh MLP, no dynamics
                    u0,v0=seed_lanes(a,b,seed); feat=generic_mlp_feats(u0,v0)
                X.append(feat); Y.append(a^b); A.append(a); B.append(b)
    return np.array(X),np.array(Y),np.array(A),np.array(B)

def split(n):
    idx=rng.permutation(n); cut=int(0.6*n); return idx[:cut],idx[cut:]

def probe_acc(X,Y,tr,te):
    Xtr=np.column_stack([X[tr],np.ones(len(tr))]); Xte=np.column_stack([X[te],np.ones(len(te))])
    mu=Xtr[:,:-1].mean(0); sd=Xtr[:,:-1].std(0)+1e-8
    Xtr[:,:-1]=(Xtr[:,:-1]-mu)/sd; Xte[:,:-1]=(Xte[:,:-1]-mu)/sd
    w,_,_,_=np.linalg.lstsq(Xtr,Y[tr]*2.0-1.0,rcond=None)
    return ((Xte@w>0).astype(int)==Y[te]).mean()

# ---- XOR reachability (original metric) ----
res={}
for kind in ("additive","operator","ablation","C1a_interaction","C1b_mlp"):
    X,Y,A,B=build(kind); tr,te=split(len(Y))
    res[kind]=dict(xor=probe_acc(X,Y,tr,te),
                   recA=probe_acc(X,A,tr,te), recB=probe_acc(X,B,tr,te))

print("=== XOR reachability (original metric) ===")
for k in ("additive","operator","ablation","C1a_interaction","C1b_mlp"):
    print(f"  {k:16s} XOR_acc={res[k]['xor']:.3f}")
op=res['operator']['xor']; add=res['additive']['xor']
eq=res['ablation']['xor']; c1a=res['C1a_interaction']['xor']; c1b=res['C1b_mlp']['xor']

print("\n=== (C2) bind-recoverability: recover BOTH parents from composed C ===")
for k in ("additive","operator","C1b_mlp"):
    print(f"  {k:16s} recover(a)={res[k]['recA']:.3f}  recover(b)={res[k]['recB']:.3f}")

# ---- FROZEN BAR eval ----
b1_gap=op-max(c1a,c1b)
recop=min(res['operator']['recA'],res['operator']['recB'])
recadd=min(res['additive']['recA'],res['additive']['recB'])
b2_gap=recop-recadd
B1=b1_gap>=0.15
B2=(b2_gap>=0.15) and (recop>=0.70)
B3=eq<=add+0.10
print("\n=== FROZEN BAR (adversarial) ===")
print(f"  (B1) generic-NL does NOT match op : op-max(C1a,C1b)={b1_gap:+.3f} >=0.15 ? {B1}")
print(f"       (C1a interaction={c1a:.3f}  C1b mlp={c1b:.3f}  vs op={op:.3f})")
print(f"  (B2) bind-recover beats additive  : min-rec op={recop:.3f} add={recadd:.3f} gap={b2_gap:+.3f} >=0.15 & op>=0.70 ? {B2}")
print(f"  (B3) ablation collapses (eq<=add+.10): eq={eq:.3f} add={add:.3f} ? {B3}")
survives=B1 and B2 and B3
print(f"\nOPERATOR SURVIVES ALL CONTROLS: {survives}")
if survives:
    verdict="CONFIRMED-DIRECTIONAL (numpy) — real composition signal, flag real-trunk rung"
elif not B1:
    verdict="ARTIFACT — generic nonlinearity matches operator; REACHABLE is nonlinearity-in-general, NOT Turing/CLS mechanism"
elif not B2:
    verdict="ARTIFACT/weak — no bind-recoverability; distinctness necessary not sufficient"
else:
    verdict="ARTIFACT — ablation does not collapse (CLS timescale-sep INERT)"
print(f"VERDICT(deepen): DIRECTIONAL (numpy) / {verdict}")
print("H_6112 transfer caveat: numpy REACHABLE OVERSTATES; meiosis 0->1.0 collapsed to 0->0.022 on real CLMConvMoE trunk. transfer-UNVERIFIED.")
