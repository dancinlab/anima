# H_6114 — 발생학 Turing 패턴 (reaction-diffusion morphogen combination) DIRECTIONAL numpy probe
# Discharges the never-fired pre-registered $0 cheap test of H_1655 / H_1734 (same mechanism).
#
# TASK (2 INDEPENDENT concepts): A in {0,1,2,3}, B in {0,1,2,3} -> 16 combos, drawn independently.
#   Target = 2-bit XOR conjunction of (A,B) => 4 classes. XOR is NON-separable: any purely
#   ADDITIVE readout of two independent concept embeddings CANNOT decode it (that is the G1 floor).
#
# METHODS compared on the SAME frozen linear probe (least-squares one-vs-all, trained on
#   train combos, tested on HELD-OUT combos):
#   (1) ADDITIVE baseline    : feat = e_A[A] + e_B[B]  (fixed random embeds)  -> the additive floor
#   (2) RD Turing (H_6114)    : two morphogen seeds (A,B) evolved by Gray-Scott activator-inhibitor
#                               with Du != Dv (differential diffusion) -> steady field flattened
#   (3) RD equal-diff CONTROL : same, but Du==Dv (kills Turing instability) -> H_1655 decisive ablation
#
# FROZEN BAR (set BEFORE the run, no post-hoc move — p7):
#   GREEN-DIRECTIONAL iff  RD-Turing held-out acc >= 0.70
#                     AND  RD-Turing exceeds ADDITIVE floor by margin >= +0.20
#                     AND  equal-diff CONTROL acc <= chance+0.10 (chance=0.25)
#   Else FALSIFIED/floor. numpy => DIRECTIONAL by construction, NEVER terminal.
import numpy as np
rng = np.random.default_rng(6114)

N = 24          # ring cells
T = 4000        # explicit steps
dt = 1.0
F, k = 0.037, 0.060   # Gray-Scott feed/kill (spot regime)

def rd_field(A, B, Du, Dv):
    u = np.ones(N); v = np.zeros(N)
    # two morphogen seeds whose POSITION depends on the concept value (independent placement)
    pa = (3 + 5*A) % N
    pb = (13 + 5*B) % N
    for p,amp in ((pa, 0.5+0.15*A),(pb, 0.5+0.15*B)):
        for d in (-1,0,1):
            v[(p+d)%N] += amp; u[(p+d)%N] -= 0.25*amp
    u = np.clip(u,0,1); v = np.clip(v,0,1)
    for _ in range(T):
        lu = np.roll(u,1)+np.roll(u,-1)-2*u
        lv = np.roll(v,1)+np.roll(v,-1)-2*v
        uvv = u*v*v
        u = u + dt*(Du*lu - uvv + F*(1-u))
        v = v + dt*(Dv*lv + uvv - (F+k)*v)
        u = np.clip(u,0,1); v = np.clip(v,0,1)
    return np.concatenate([u,v])

# fixed random embeds for additive baseline (dim = 2N to match RD feature dim)
D = 2*N
eA = rng.standard_normal((4,D))*0.5
eB = rng.standard_normal((4,D))*0.5

combos = [(a,b) for a in range(4) for b in range(4)]
def target(a,b):  # 2-bit XOR -> class 0..3
    return (a ^ b)

# held-out split: train on 11 combos, test on 5 held-out (independent concepts still each seen)
idx = list(range(16)); rng.shuffle(idx)
test_ids = set(idx[:5]); train_ids = [i for i in range(16) if i not in test_ids]

def build(method):
    X=[];Y=[]
    for i,(a,b) in enumerate(combos):
        if method=='add':   f = eA[a]+eB[b]
        elif method=='turing': f = rd_field(a,b,0.16,0.08)
        elif method=='ctrl':   f = rd_field(a,b,0.12,0.12)
        X.append(f); Y.append(target(a,b))
    return np.array(X), np.array(Y)

def decode_acc(X,Y):
    # frozen least-squares one-hot ridge probe, train on train_ids, eval held-out
    Xtr=X[train_ids]; Ytr=Y[train_ids]
    Xte=X[list(test_ids)]; Yte=Y[list(test_ids)]
    mu=Xtr.mean(0); sd=Xtr.std(0)+1e-8
    Xtr=(Xtr-mu)/sd; Xte=(Xte-mu)/sd
    Xtr=np.hstack([Xtr,np.ones((len(Xtr),1))]); Xte=np.hstack([Xte,np.ones((len(Xte),1))])
    Yoh=np.eye(4)[Ytr]
    W=np.linalg.pinv(Xtr.T@Xtr + 1.0*np.eye(Xtr.shape[1]))@Xtr.T@Yoh
    pred=(Xte@W).argmax(1)
    return float((pred==Yte).mean())

res={}
for m in ('add','turing','ctrl'):
    X,Y=build(m); res[m]=decode_acc(X,Y)

chance=0.25
add_acc=res['add']; tur_acc=res['turing']; ctrl_acc=res['ctrl']
print(f"held-out combos = {sorted(test_ids)}  chance={chance}")
print(f"ADDITIVE floor  held-out acc = {add_acc:.3f}")
print(f"RD-TURING       held-out acc = {tur_acc:.3f}  (Du=0.16,Dv=0.08)")
print(f"RD equal-diff CTRL acc       = {ctrl_acc:.3f}  (Du=Dv=0.12, Turing OFF)")
margin = tur_acc-add_acc
c1 = tur_acc>=0.70
c2 = margin>=0.20
c3 = ctrl_acc<=chance+0.10
print(f"BAR c1 turing>=0.70: {c1} | c2 margin>=+0.20 (={margin:+.3f}): {c2} | c3 ctrl<=0.35: {c3}")
verdict = "GREEN-DIRECTIONAL" if (c1 and c2 and c3) else "FALSIFIED/FLOOR"
print(f"VERDICT (numpy DIRECTIONAL, NOT terminal): {verdict}")
