# H_6114 — ADVERSARIAL DEEPEN (multi-lens) of the DIRECTIONAL numpy REACHABLE.
# Original probe: 2-bit XOR (A^B) 4-class, held-out 5/16, frozen ridge probe.
#   ADDITIVE=0.000  RD-TURING=1.000  equal-diff-CTRL=0.000  -> GREEN-DIRECTIONAL.
# a_break_the_wall: a REACHABLE is NOT confident until controls kill the alternatives.
# H_6112 precedent: numpy 0->1.0 REACHABLE COLLAPSED on real CLMConvMoE trunk (0->0.022).
#
# CONTROLS (applied to the SAME task / SAME frozen ridge probe / SAME held-out split):
#  C1 GENERIC-NONLINEARITY : replace RD operator with generic nonlinearities of the SAME
#       random parent embeds — elementwise product (A*B), random-projection tanh-MLP,
#       squared-sum. If a GENERIC nonlinearity ALSO clears the same held-out bar, the RD
#       REACHABLE is a metric artifact of nonlinearity-in-general, NOT the Turing mechanism.
#  C2 BIND-RECOVERABILITY  : can BOTH parents be linearly recovered from the composed field C?
#       Fit ridge C->A and C->B on train combos, test on held-out. distinctness-from-parents
#       (orig metric) is NECESSARY not SUFFICIENT. Compare RD recoverability vs ADDITIVE.
#  C3 ABLATION             : (a) equal-diff (Turing OFF, orig) and (b) reaction-term OFF
#       (u*v*v cross-term zeroed = pure linear diffusion). Both must collapse to floor.
#
# FROZEN BAR (set BEFORE run, p7 — no post-hoc move):
#   RD operator SURVIVES (-> CONFIRMED, flag real-trunk rung) iff ALL of:
#     (S1) NO generic nonlinearity reaches within 0.15 of RD held-out acc
#          (generic must be clearly WORSE; else the mechanism is generic-nonlinearity artifact)
#     (S2) RD bind-recoverability (mean of A,B held-out) exceeds ADDITIVE recoverability by >= +0.20
#          (RD must add binding info parents-in-sum does not)
#     (S3) BOTH ablations collapse to <= chance+0.10 (=0.35)
#   Otherwise -> ARTIFACT (numpy REACHABLE was a metric artifact of nonlinearity).
#   numpy => DIRECTIONAL by construction, NEVER terminal either way.
import numpy as np
rng = np.random.default_rng(6114)

N=24; T=4000; dt=1.0; F,k=0.037,0.060

def rd_field(A,B,Du,Dv,react=True):
    u=np.ones(N); v=np.zeros(N)
    pa=(3+5*A)%N; pb=(13+5*B)%N
    for p,amp in ((pa,0.5+0.15*A),(pb,0.5+0.15*B)):
        for d in(-1,0,1):
            v[(p+d)%N]+=amp; u[(p+d)%N]-=0.25*amp
    u=np.clip(u,0,1); v=np.clip(v,0,1)
    for _ in range(T):
        lu=np.roll(u,1)+np.roll(u,-1)-2*u
        lv=np.roll(v,1)+np.roll(v,-1)-2*v
        uvv=u*v*v if react else 0.0
        u=u+dt*(Du*lu-uvv+F*(1-u))
        v=v+dt*(Dv*lv+uvv-(F+k)*v)
        u=np.clip(u,0,1); v=np.clip(v,0,1)
    return np.concatenate([u,v])

D=2*N
eA=rng.standard_normal((4,D))*0.5
eB=rng.standard_normal((4,D))*0.5
# fixed random projection for generic MLP control (concat 2D -> D hidden)
Wp=rng.standard_normal((2*D,D))*(1.0/np.sqrt(2*D))

combos=[(a,b) for a in range(4) for b in range(4)]
def target(a,b): return a^b

# SAME held-out split as original probe (identical rng draw order after embeds+Wp)
idx=list(range(16)); rng.shuffle(idx)
test_ids=set(idx[:5]); train_ids=[i for i in range(16) if i not in test_ids]

def feat(method,a,b):
    if method=='add':    return eA[a]+eB[b]
    if method=='turing': return rd_field(a,b,0.16,0.08,react=True)
    if method=='ctrl_eqdiff': return rd_field(a,b,0.12,0.12,react=True)   # C3a Turing OFF
    if method=='ctrl_noreact': return rd_field(a,b,0.16,0.08,react=False)  # C3b reaction OFF
    if method=='prod':   return eA[a]*eB[b]                                # C1 elementwise product
    if method=='sqsum':  return (eA[a]+eB[b])**2                           # C1 squared-sum nonlin
    if method=='mlp':    return np.tanh(Wp.T@np.concatenate([eA[a],eB[b]]))# C1 random-proj tanh MLP
    raise ValueError(method)

def build(method):
    X=[feat(method,a,b) for (a,b) in combos]
    return np.array(X)

def ridge_acc(X,Y,ncls):
    Xtr=X[train_ids]; Ytr=Y[train_ids]
    Xte=X[list(test_ids)]; Yte=Y[list(test_ids)]
    mu=Xtr.mean(0); sd=Xtr.std(0)+1e-8
    Xtr=(Xtr-mu)/sd; Xte=(Xte-mu)/sd
    Xtr=np.hstack([Xtr,np.ones((len(Xtr),1))]); Xte=np.hstack([Xte,np.ones((len(Xte),1))])
    Yoh=np.eye(ncls)[Ytr]
    W=np.linalg.pinv(Xtr.T@Xtr+1.0*np.eye(Xtr.shape[1]))@Xtr.T@Yoh
    pred=(Xte@W).argmax(1)
    return float((pred==Yte).mean())

Yxor=np.array([target(a,b) for (a,b) in combos])
Ya=np.array([a for (a,b) in combos])
Yb=np.array([b for (a,b) in combos])
chance=0.25

# --- main XOR-task acc per method ---
accs={}
for m in ('add','turing','prod','sqsum','mlp','ctrl_eqdiff','ctrl_noreact'):
    accs[m]=ridge_acc(build(m),Yxor,4)

print(f"held-out combos = {sorted(test_ids)}  chance={chance}")
print("== XOR-task held-out acc (frozen ridge probe) ==")
for m in ('add','turing','prod','sqsum','mlp','ctrl_eqdiff','ctrl_noreact'):
    print(f"  {m:14s} = {accs[m]:.3f}")

# --- C1: generic nonlinearity vs RD ---
rd=accs['turing']
generic=['prod','sqsum','mlp']
best_generic=max(accs[g] for g in generic)
best_generic_name=max(generic,key=lambda g:accs[g])
S1 = all(accs[g] < rd-0.15 for g in generic)   # every generic clearly worse
print(f"\n[C1 GENERIC-NONLINEARITY] RD={rd:.3f}  best-generic={best_generic:.3f} ({best_generic_name})")
print(f"  S1 (no generic within 0.15 of RD): {S1}"
      f"  -> {'RD distinctive' if S1 else 'GENERIC MATCHES => nonlinearity-artifact'}")

# --- C2: bind-recoverability (both parents from composed field) ---
def recov(method):
    X=build(method)
    return ridge_acc(X,Ya,4), ridge_acc(X,Yb,4)
rA,rB=recov('turing'); rd_recov=0.5*(rA+rB)
aA,aB=recov('add');    add_recov=0.5*(aA+aB)
S2 = rd_recov >= add_recov+0.20
print(f"\n[C2 BIND-RECOVERABILITY] held-out parent recovery (A,B mean)")
print(f"  RD-TURING recov = {rd_recov:.3f}  (A={rA:.3f} B={rB:.3f})")
print(f"  ADDITIVE  recov = {add_recov:.3f}  (A={aA:.3f} B={aB:.3f})")
print(f"  S2 (RD beats additive recov by >=+0.20): {S2}"
      f"  -> {'RD adds binding info' if S2 else 'RD adds NO binding info over sum'}")

# --- C3: ablations ---
S3 = (accs['ctrl_eqdiff']<=chance+0.10) and (accs['ctrl_noreact']<=chance+0.10)
print(f"\n[C3 ABLATION] eqdiff={accs['ctrl_eqdiff']:.3f}  noreact={accs['ctrl_noreact']:.3f}  (bar<=0.35)")
print(f"  S3 (both collapse): {S3}")

survives = S1 and S2 and S3
print("\n== FROZEN-BAR VERDICT ==")
print(f"  S1(generic-distinct)={S1}  S2(bind-recov)={S2}  S3(ablation)={S3}")
print(f"  RESULT: {'CONFIRMED (survives all controls; flag real-trunk rung)' if survives else 'ARTIFACT (numpy REACHABLE = metric artifact of nonlinearity)'}")
print("  NOTE: numpy => DIRECTIONAL, NEVER terminal. H_6112 transfer caveat applies.")
