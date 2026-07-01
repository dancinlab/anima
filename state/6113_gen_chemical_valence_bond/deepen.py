# H_6113 adversarial deepening — complementary-valence bond as compositional binding operator.
#
# Target claim: concepts = atoms with valence slots; composition = complementary
# (donor<->acceptor) valence bind; generation = reaction network. This is a TYPED /
# CONSTRUCTIVE binding-operator. Card says DUP-WALLED against H_1823 (circconv),
# H_1816 (pred-coding bind), H_1834 (tension-mouth) — all engine-native 🧱 with the
# shared failure mode "operator INERT: FULL==OFF==ADDITIVE floor on real CLMConvMoE trunk".
#
# This probe does NOT try to green-light. It tests whether a numpy REACHABLE for the
# valence-bind operator would be a METRIC ARTIFACT (per H_6112: numpy 0->1.0 REACHABLE
# collapsed to 0->0.022 on the real trunk). Controls:
#   C1 GENERIC-NONLINEARITY: tanh(A+B), A*B (Hadamard), random linear proj of concat[A,B].
#       If a generic op matches valence-bind on the SAME 'composed_distinct' bar -> artifact.
#   C2 BIND-RECOVERABILITY: fit linear readout C->A and C->B on TRAIN pairs, test HELD-OUT.
#       distinctness is necessary-not-sufficient; if A,B not recoverable it's not binding.
#   C3 SHUFFLE/ABLATION: valence-bind with complementary pairing OFF must collapse to floor.
#
# FROZEN BAR (set BEFORE run): the valence operator SURVIVES (would justify a real-trunk
# rung, not dup) ONLY IF ALL of:
#   (B1) generic-nonlinearity does NOT reach valence's distinct   [gap > 0.05]
#   (B2) valence bind-recoverability beats additive by margin     [R2_valence - R2_add > 0.15]
#   (B3) ablation (pairing shuffled) collapses distinct to add     [|abl - add| < 0.05]
#   (B4) generic ops do NOT also pass B2's recoverability          [no generic recovers >0.15 over add]
# If a generic op matches (¬B1) OR also recovers (¬B4) -> the numpy signal is an artifact of
# nonlinearity/info-preservation in general, NOT the complementary-valence mechanism -> ARTIFACT/dup.
import os
os.environ["OMP_NUM_THREADS"]="4"
import numpy as np

D=64; N=200; SEED=6113
rng=np.random.default_rng(SEED)

def norm(x):
    return x/ (np.linalg.norm(x,axis=-1,keepdims=True)+1e-9)

# atoms: half donor slots, half acceptor slots
atoms=rng.standard_normal((N,D))
atoms=norm(atoms)
H=D//2

def circ(a,b):  # circular convolution (the H_1823 primitive)
    return np.real(np.fft.ifft(np.fft.fft(a,axis=-1)*np.fft.fft(b,axis=-1),axis=-1))
def corr(c,b): # circular correlation ~ approximate unbind
    return np.real(np.fft.ifft(np.fft.fft(c,axis=-1)*np.conj(np.fft.fft(b,axis=-1)),axis=-1))

def valence_bind(A,B,shuffle=False):
    # complementary: donor(A) reacts with acceptor(B) and vice versa via circconv
    dA,aA=A[...,:H],A[...,H:]
    dB,aB=B[...,:H],B[...,H:]
    if shuffle:
        # ablate the complementary pairing: pair donor with donor (no complementarity)
        c1=circ(dA,dB); c2=circ(aA,aB)
    else:
        c1=circ(dA,aB); c2=circ(dB,aA)
    return norm(np.concatenate([c1,c2],axis=-1))

def add_op(A,B):   return norm(A+B)
def tanh_op(A,B):  return norm(np.tanh(A+B))
def hadam_op(A,B): return norm(A*B)
# fixed random linear projection of concat[A,B] -> D  (generic invertible-ish mix)
Wproj=rng.standard_normal((2*D,D))/np.sqrt(2*D)
def rproj_op(A,B): return norm(np.concatenate([A,B],axis=-1)@Wproj)

# pairs
P=400
ia=rng.integers(0,N,P); ib=rng.integers(0,N,P)
A=atoms[ia]; B=atoms[ib]

def distinct(C):
    # composed_distinct: 1 - max cosine sim to either parent (higher = more distinct from parents)
    ca=np.sum(C*A,axis=-1); cb=np.sum(C*B,axis=-1)
    return float(np.mean(1.0-np.maximum(ca,cb)))

def recover_r2(C):
    # fit linear C->A and C->B on TRAIN half, R2 on HELD-OUT half (recover parents from composed)
    ntr=P//2
    def fit_r2(Ctr,Ytr,Cte,Yte):
        # ridge least squares
        lam=1e-2
        W=np.linalg.solve(Ctr.T@Ctr+lam*np.eye(Ctr.shape[1]), Ctr.T@Ytr)
        pred=Cte@W
        ss_res=np.sum((Yte-pred)**2); ss_tot=np.sum((Yte-Yte.mean(0))**2)+1e-9
        return 1.0-ss_res/ss_tot
    r2a=fit_r2(C[:ntr],A[:ntr],C[ntr:],A[ntr:])
    r2b=fit_r2(C[:ntr],B[:ntr],C[ntr:],B[ntr:])
    return float((r2a+r2b)/2)

ops={
 "valence":   valence_bind(A,B),
 "valence_ABL": valence_bind(A,B,shuffle=True),
 "additive":  add_op(A,B),
 "tanh(A+B)": tanh_op(A,B),
 "A*B":       hadam_op(A,B),
 "randproj":  rproj_op(A,B),
}
print("=== H_6113 adversarial deepening (numpy toy, D=%d, %d pairs, seed=%d) ==="%(D,P,SEED))
print("%-12s %10s %10s"%("op","distinct","recover_R2"))
res={}
for k,C in ops.items():
    d=distinct(C); r=recover_r2(C); res[k]=(d,r)
    print("%-12s %10.4f %10.4f"%(k,d,r))

v_d,v_r=res["valence"]; a_d,a_r=res["additive"]; abl_d,abl_r=res["valence_ABL"]
gen_keys=["tanh(A+B)","A*B","randproj"]
gen_max_d=max(res[k][0] for k in gen_keys)
gen_max_recgap=max(res[k][1]-a_r for k in gen_keys)

B1 = (v_d - gen_max_d) > 0.05                 # generic does NOT reach valence distinct
B2 = (v_r - a_r) > 0.15                        # valence recoverability beats additive
B3 = abs(abl_d - a_d) < 0.05                   # ablation collapses distinct to additive floor
B4 = gen_max_recgap < 0.15                     # no generic op also recovers over additive

print()
print("distinct: valence=%.4f  generic_max=%.4f  additive=%.4f  ablation=%.4f"%(v_d,gen_max_d,a_d,abl_d))
print("recover_R2: valence=%.4f  additive=%.4f  generic_max_gap=%.4f"%(v_r,a_r,gen_max_recgap))
print("B1 generic!=valence distinct (gap>0.05): %s (gap=%.4f)"%(B1, v_d-gen_max_d))
print("B2 valence recover>additive+0.15:        %s (gap=%.4f)"%(B2, v_r-a_r))
print("B3 ablation collapses to floor(|.|<0.05):%s (|.|=%.4f)"%(B3, abs(abl_d-a_d)))
print("B4 no generic also recovers(gap<0.15):   %s (gen_max_recgap=%.4f)"%(B4, gen_max_recgap))
survive = B1 and B2 and B3 and B4
print()
print("SURVIVES all controls (would justify real-trunk rung): %s"%survive)
if not survive:
    reasons=[]
    if not B1: reasons.append("generic-nonlinearity MATCHES distinct -> distinct is nonlinearity-generic (artifact)")
    if not B2: reasons.append("valence NOT recoverable over additive -> not compositional binding")
    if not B3: reasons.append("ablation did NOT collapse -> scaffold not ingredient")
    if not B4: reasons.append("generic op ALSO recovers -> recoverability = info-preservation, not valence mechanism")
    print("VERDICT: ARTIFACT/DUP -> "+ " ; ".join(reasons))
    print("H_6112 transfer: even a numpy REACHABLE (0->~1.0) for a binding-op collapsed to 0->0.022 on real CLMConvMoE trunk (meiosis). H_1823 circconv (SAME circular-convolution primitive used here) is engine-native 🧱 NOT-SUPPORTED. dup pointer HOLDS.")
else:
    print("VERDICT: signal survives numpy controls -> flag for real-trunk rung (still DIRECTIONAL, H_6112 caveat applies).")
