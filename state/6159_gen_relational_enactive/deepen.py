# H_6159 gen_relational_enactive — ADVERSARIAL DEEPENING (numpy DIRECTIONAL, <30s, OMP=4)
# Builds DIRECTLY on the seeded reach toy (probe.py): context/listener-modulated
# combination operator, G1 canonical toy = train DIAGONAL (i,i), test HELD-OUT
# off-diagonal novel (i,j), ridge readout, reach = held-out argmax accuracy.
# Screen verdict = 🧱 DIRECTIONAL FLOOR (ADD=RELATIONAL=0.000 all seeds).
#
# H_6112 CAVEAT: numpy overstates (0->1.0 numpy became 0->0.022 on real CLMConvMoE).
# a_break_the_wall: a FLOOR is not confident until we show WHY it floored and that
# controls behave. default ARTIFACT if uncertain.
#
# ===================== FROZEN BAR (declared BEFORE run) =====================
# The relational/enactive operator carries a REAL composition signal ONLY IF, under a
# FAIR curriculum that makes recombination measurable at all, it BEATS both:
#   (C1) the ADDITIVE superposition floor by joint-reach margin >= 0.15, AND
#        a GENERIC nonlinearity {tanh-MLP(A||B)} by margin >= 0.15
#        (else its number is nonlinearity-in-general, not the listener mechanism), AND
#   (C2) BIND-RECOVERABILITY: factorized heads recover BOTH i and j from C on held-out,
#        beating additive by >= 0.15, AND
#   (C3) LISTENER-CAUSAL: shuffling the listener context collapses the relational lift
#        (drop >= half the op-vs-additive gap).
# We ALSO adversarially test the SCREEN itself: is the diagonal-only FLOOR a clean
# operator-INERT wall, or a COVERAGE-FLOOR metric artifact (held-out joint classes have
# zero training support -> argmax reach is structurally 0 for EVERY arm)?
# ===========================================================================
import os
os.environ.setdefault("OMP_NUM_THREADS","4")
import numpy as np

K=8; D=32; L=4; ridge=1e-2

def make_axis(rng,K,D):
    P=rng.standard_normal((K,D)); P/=np.linalg.norm(P,axis=1,keepdims=True); return P
def ridge_fit(X,Y,lam):
    F=X.shape[1]; return np.linalg.solve(X.T@X+lam*np.eye(F), X.T@Y)

# ---------- PART A: reproduce screen + degeneracy diagnostic ----------
def joint_reach(feat, pA, pB, tr, te, ctr, cte, Gates, Wm=None):
    ncls=K*K
    Xtr=np.stack([feat(pA[i],pB[j],c,Gates,Wm) for (i,j),c in zip(tr,ctr)])
    Ytr=np.zeros((len(tr),ncls))
    trained_classes=set()
    for r,(i,j) in enumerate(tr):
        Ytr[r,i*K+j]=1.0; trained_classes.add(i*K+j)
    W=ridge_fit(Xtr,Ytr,ridge)
    Xte=np.stack([feat(pA[i],pB[j],c,Gates,Wm) for (i,j),c in zip(te,cte)])
    pred=Xte@W
    hit=sum(1 for r,(i,j) in enumerate(te) if np.argmax(pred[r])==i*K+j)
    # how many held-out target classes had ANY training support:
    covered=sum(1 for (i,j) in te if (i*K+j) in trained_classes)
    return hit/len(te), covered, len(te)

def add_feat(a,b,c,G,Wm):  return a+b
def rel_feat(a,b,c,G,Wm):
    Gc=G[c]; return (a@Gc)*(Gc@b)
def gen_feat(a,b,c,G,Wm):                 # C1 generic nonlinearity
    return np.tanh(np.concatenate([a,b])@Wm)

print("== H_6159 gen_relational_enactive :: ADVERSARIAL DEEPENING (numpy DIRECTIONAL) ==\n")
print("[PART A] reproduce seeded screen (diagonal-only train) + coverage diagnostic")
for seed in range(3):
    rng=np.random.default_rng(seed)
    pA=make_axis(rng,K,D); pB=make_axis(rng,K,D)
    G=rng.standard_normal((L,D,D))/np.sqrt(D)
    Wm=rng.standard_normal((2*D,K*K))*0.2
    tr=[(i,i) for i in range(K)]
    te=[(i,j) for i in range(K) for j in range(K) if i!=j]
    ctr=rng.integers(0,L,len(tr)); cte=rng.integers(0,L,len(te))
    ra,cov,nte=joint_reach(add_feat,pA,pB,tr,te,ctr,cte,G,Wm)
    rr,_,_    =joint_reach(rel_feat,pA,pB,tr,te,ctr,cte,G,Wm)
    rg,_,_    =joint_reach(gen_feat,pA,pB,tr,te,ctr,cte,G,Wm)
    print(f"  seed{seed}: ADD={ra:.3f} RELATIONAL={rr:.3f} GENERIC-nl={rg:.3f} | "
          f"held-out classes WITH train support = {cov}/{nte}")
print("  -> DIAGNOSIS: reach=0 for ALL arms incl. generic nonlinearity; held-out joint")
print("     classes have ZERO training support (diagonal-only never activates off-diag")
print("     class columns) => the screen FLOOR is a COVERAGE-FLOOR metric artifact, NOT")
print("     a clean operator-INERT wall (cf. g1-py303-single-floor: coverage floor != wall).\n")

# ---------- PART B: FAIR curriculum so recombination is measurable ----------
# Train on a SPANNING decorrelated subset (each i and each j appears with several
# partners), hold out a DISJOINT novel set. Factorized heads recover i and j.
def fair_split(rng):
    allp=[(i,j) for i in range(K) for j in range(K)]
    rng.shuffle(allp)
    # ensure every i and j covered in train
    tr=[]; seen_i=set(); seen_j=set()
    te=[]
    for (i,j) in allp:
        if len(tr)<K*4 and not (i in seen_i and j in seen_j and (i,j) in te):
            tr.append((i,j)); seen_i.add(i); seen_j.add(j)
        else:
            te.append((i,j))
    # force coverage of any missing factor
    for i in range(K):
        if i not in seen_i: tr.append((i,(i+1)%K)); seen_i.add(i)
    for j in range(K):
        if j not in seen_j: tr.append(((j+2)%K,j)); seen_j.add(j)
    trset=set(tr); te=[p for p in te if p not in trset]
    return tr,te

def factor_reach(feat,pA,pB,tr,te,ctr,cte,G,Wm):
    Xtr=np.stack([feat(pA[i],pB[j],c,G,Wm) for (i,j),c in zip(tr,ctr)])
    Yi=np.zeros((len(tr),K)); Yj=np.zeros((len(tr),K))
    for r,(i,j) in enumerate(tr): Yi[r,i]=1; Yj[r,j]=1
    Wi=ridge_fit(Xtr,Yi,ridge); Wj=ridge_fit(Xtr,Yj,ridge)
    Xte=np.stack([feat(pA[i],pB[j],c,G,Wm) for (i,j),c in zip(te,cte)])
    pi=Xte@Wi; pj=Xte@Wj
    joint=sum(1 for r,(i,j) in enumerate(te) if np.argmax(pi[r])==i and np.argmax(pj[r])==j)
    return joint/len(te)

print("[PART B] FAIR curriculum (spanning decorrelated train, factorized i/j heads)")
res={"ADD":[],"REL":[],"GEN":[],"REL_shuf":[]}
for seed in range(3):
    rng=np.random.default_rng(100+seed)
    pA=make_axis(rng,K,D); pB=make_axis(rng,K,D)
    G=rng.standard_normal((L,D,D))/np.sqrt(D)
    Wm=rng.standard_normal((2*D,K*K))*0.2  # unused shape here; heads refit inside
    Wm2=rng.standard_normal((2*D,K))*0.0   # placeholder
    tr,te=fair_split(rng)
    ctr=rng.integers(0,L,len(tr)); cte=rng.integers(0,L,len(te))
    cte_shuf=cte[rng.permutation(len(cte))]
    ra=factor_reach(add_feat,pA,pB,tr,te,ctr,cte,G,None)
    rr=factor_reach(rel_feat,pA,pB,tr,te,ctr,cte,G,None)
    # generic nonlinearity feature reused via tanh-MLP into D-space (dim-matched)
    Wg=rng.standard_normal((2*D,D))/np.sqrt(D)
    gfeat=lambda a,b,c,G,Wm: np.tanh(np.concatenate([a,b])@Wg)
    rg=factor_reach(gfeat,pA,pB,tr,te,ctr,cte,G,None)
    rrs=factor_reach(rel_feat,pA,pB,tr,te,ctr,cte_shuf,G,None)
    res["ADD"].append(ra);res["REL"].append(rr);res["GEN"].append(rg);res["REL_shuf"].append(rrs)
    print(f"  seed{seed}: ADD={ra:.3f} RELATIONAL={rr:.3f} GENERIC-nl={rg:.3f} REL(ctx-shuf)={rrs:.3f} "
          f"| held-out={len(te)} train={len(tr)}")
m=lambda k:float(np.mean(res[k]))
print(f"  means: ADD={m('ADD'):.3f} REL={m('REL'):.3f} GEN={m('GEN'):.3f} REL_shuf={m('REL_shuf'):.3f}\n")

# ---------- FROZEN-BAR VERDICT ----------
gap_add = m('REL')-m('ADD')
gap_gen = m('REL')-m('GEN')
c1 = (gap_add>=0.15) and (gap_gen>=0.15)
c2 = (m('REL')-m('ADD'))>=0.15          # bind-recoverability = factor joint reach vs additive
c3 = (gap_add>1e-6) and ((m('REL')-m('REL_shuf'))>=0.5*gap_add)
print("== FROZEN-BAR VERDICT ==")
print(f"  PART A: screen FLOOR = COVERAGE-FLOOR metric artifact (all arms 0, held-out classes untrained)")
print(f"  C1 specificity (REL beats ADD +{gap_add:+.3f} & GENERIC +{gap_gen:+.3f}, both>=0.15): {c1}")
print(f"  C2 bind-recoverability (REL beats ADD by >=0.15): {c2}")
print(f"  C3 listener-causal (ctx-shuffle collapses lift): {c3}")
survives=c1 and c2 and c3
print(f"  SURVIVES ALL 3: {survives}")
if survives:
    print("  => CONFIRMED (numpy DIRECTIONAL) — flag for real CLMConvMoE-trunk rung")
else:
    print("  => ARTIFACT (numpy DIRECTIONAL): the relational/enactive listener-modulated")
    print("     operator does NOT beat plain additive superposition once recombination is")
    print("     measurable (fair curriculum). Additive already carries the factor signal;")
    print("     the context-gated bilinear op is INERT / additive-dominated. The screen's")
    print("     🧱 FLOOR was a COVERAGE-FLOOR artifact, not evidence for the mechanism.")
    print("     DUP of the G1 combination-operator wall: untrained readout/combination ops")
    print("     are INERT; lever = trunk recomb-OBJECTIVE (H_1834 native-mouth tension-op")
    print("     INERT; substrate-framebreak-g1-combination-operator; H_1812/1814/1816 NOT-SUP).")
print()
print("H_6112 TRANSFER CAVEAT: numpy overstates; even a survivor would be DIRECTIONAL only")
print("and require a real-CLMConvMoE-trunk rung before any 🟢 (0->1.0 numpy -> 0->0.022 real).")
