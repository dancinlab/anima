# H_6152 antimatter combination — ADVERSARIAL DEEPENING (numpy, still DIRECTIONAL; numpy overstates cf H_6112 0->1.0 collapsing to 0->0.022 on real CLMConvMoE trunk).
# Original claim: sign-gated annihilation op (antimatter_v2) scores composed_distinct=24/24 vs additive 0/24.
#   antimatter_v2(A,B) = where(sign(A)==sign(B), A-B, A+B), normalized.
# We try to REFUTE the signal with 3 controls. Default = ARTIFACT if uncertain.
#
# ===== FROZEN BAR (set BEFORE running) =====
# The operator SURVIVES (CONFIRMED, real composition signal) ONLY IF ALL of:
#   (C1) GENERIC-NONLINEARITY: no generic nonlinearity (tanh(A+B), Hadamard A*B, random-proj-MLP relu)
#        also reaches composed_distinct >= bar(=20/24). If any generic op ALSO passes -> ARTIFACT
#        (the metric rewards nonlinearity-in-general, not the annihilation mechanism).
#   (C2) BIND-RECOVERABILITY: parents must be recoverable from C. Fit ridge readout C->A and C->B on
#        TRAIN pairs, test held-out mean recovery-cos. antimatter must BEAT additive recoverability by
#        >= +0.10 mean-cos (averaged over A and B) to qualify as compositional binding, not lossy scramble.
#   (C3) ABLATION: replace the SIGN mask with a RANDOM (shuffled) mask of the same density. If random-mask
#        also scores >= bar(=20/24), the sign-gating ingredient is NOT causal -> ARTIFACT (scaffold effect).
# If C1 fails OR C2 fails OR C3 fails -> ARTIFACT. Only all-pass -> CONFIRMED (flag real-trunk rung).
import numpy as np
rng = np.random.default_rng(6152)
d, N = 64, 24
BAR = 20  # >=20/24 counts as "passes the composed_distinct metric"
def unit(x): return x/(np.linalg.norm(x,axis=-1,keepdims=True)+1e-9)
A = unit(rng.standard_normal((N,d)))
B = unit(rng.standard_normal((N,d)))
def cos(x,y): return (x*y).sum(-1)

def composed_distinct(C):
    ok=0; S=C@C.T; np.fill_diagonal(S,-1)
    for i in range(N):
        if max(cos(C[i],A[i]),cos(C[i],B[i]))<0.50 and S[i].max()<0.90: ok+=1
    return ok

# ---- operators ----
def additive(A,B): return unit(A+B)
def antimatter_v2(A,B):
    same=(np.sign(A)==np.sign(B)); return unit(np.where(same,A-B,A+B))
# generic nonlinearities (C1)
def gen_tanh(A,B): return unit(np.tanh(2.0*(A+B)))
def gen_hadamard(A,B): return unit(A*B)                       # elementwise product
_W1=rng.standard_normal((d,d))/np.sqrt(d); _W2=rng.standard_normal((d,d))/np.sqrt(d)
def gen_mlp(A,B):                                             # random-projection relu MLP on concat-sum
    h=np.maximum(0.0,(A+B)@_W1); return unit(h@_W2)
# ablation (C3): random mask, same ~density as sign-match (~0.5), sign-independent
_rand_mask=(rng.random((N,d))<0.5)
def abl_randmask(A,B): return unit(np.where(_rand_mask,A-B,A+B))
# also: fixed always-difference (sign ingredient fully off, no gating)
def abl_alldiff(A,B): return unit(A-B)

print("=== C1: GENERIC-NONLINEARITY control (does the metric reward nonlinearity-in-general?) ===")
ops=[("additive(floor)",additive),("antimatter_v2",antimatter_v2),
     ("gen_tanh(A+B)",gen_tanh),("gen_hadamard(A*B)",gen_hadamard),("gen_randMLP",gen_mlp)]
floor=composed_distinct(additive(A,B))
scores={}
for name,op in ops:
    C=op(A,B); sc=composed_distinct(C); scores[name]=sc
    mp=np.array([max(cos(C[i],A[i]),cos(C[i],B[i])) for i in range(N)])
    print(f"  {name:20s} composed_distinct={sc:2d}/{N}  mean_max_cos_parent={mp.mean():.3f}")
generic_pass=[n for n in ("gen_tanh(A+B)","gen_hadamard(A*B)","gen_randMLP") if scores[n]>=BAR]
print(f"  -> generic nonlinearities passing bar({BAR}): {generic_pass or 'NONE'}")
C1_fail = len(generic_pass)>0

print("\n=== C3: ABLATION (turn the SIGN ingredient off) ===")
for name,op in [("abl_randmask(~0.5)",abl_randmask),("abl_alldiff(A-B)",abl_alldiff)]:
    sc=composed_distinct(op(A,B)); scores[name]=sc
    print(f"  {name:20s} composed_distinct={sc:2d}/{N}")
C3_fail = scores["abl_randmask(~0.5)"]>=BAR  # random gating also passes => sign not causal
print(f"  -> random-mask passes bar? {C3_fail}  (True = sign-gate NOT causal = artifact)")

print("\n=== C2: BIND-RECOVERABILITY (can BOTH parents be read back out of C?) ===")
# bigger sample for a real train/test split; ridge readout C->A and C->B
d2,M=32,400; rng2=np.random.default_rng(61522)
A2=unit(rng2.standard_normal((M,d2))); B2=unit(rng2.standard_normal((M,d2)))
def ops2(name):
    if name=="additive": return unit(A2+B2)
    if name=="antimatter_v2":
        same=(np.sign(A2)==np.sign(B2)); return unit(np.where(same,A2-B2,A2+B2))
    if name=="tensor_bind":  # reference: circular-conv binding is genuinely (un)bindable
        return unit(np.fft.irfft(np.fft.rfft(A2,axis=1)*np.fft.rfft(B2,axis=1),n=d2,axis=1))
def ridge_recover(C,Y,ntr=300,lam=1.0):
    Ctr,Cte=C[:ntr],C[ntr:]; Ytr,Yte=Y[:ntr],Y[ntr:]
    W=np.linalg.solve(Ctr.T@Ctr+lam*np.eye(Ctr.shape[1]),Ctr.T@Ytr)
    P=unit(Cte@W); return cos(P,unit(Yte)).mean()
rec={}
for name in ("additive","antimatter_v2","tensor_bind"):
    C=ops2(name); ra=ridge_recover(C,A2); rb=ridge_recover(C,B2); rec[name]=(ra+rb)/2
    print(f"  {name:20s} recoverA_cos={ra:+.3f} recoverB_cos={rb:+.3f} mean={rec[name]:+.3f}")
lift_rec=rec["antimatter_v2"]-rec["additive"]
print(f"  -> antimatter recoverability lift over additive = {lift_rec:+.3f} (need >= +0.10)")
C2_fail = lift_rec < 0.10

print("\n=== VERDICT (frozen bar) ===")
print(f"  C1 generic-nonlinearity artifact? {C1_fail}")
print(f"  C2 bind-recoverability FAIL?      {C2_fail}")
print(f"  C3 ablation (sign not causal)?    {C3_fail}")
survives = (not C1_fail) and (not C2_fail) and (not C3_fail)
print(f"  => {'CONFIRMED (survives all controls -> flag real-trunk rung)' if survives else 'ARTIFACT (numpy REACHABLE is a metric artifact of distinctness, not compositional binding)'}")
