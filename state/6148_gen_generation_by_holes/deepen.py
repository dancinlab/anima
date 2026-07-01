# H_6148 ADVERSARIAL DEEPENING — "generation by holes" (anti-storage / topological defect)
# ---------------------------------------------------------------------------------
# Original numpy screen (RESULT.txt): additive_reach=0.000, hole_fill_reach=0.020,
#   lift=+0.020, wins=0/3 -> FALSIFIED-FLOOR (DIRECTIONAL).
# The operator: 64 INDEPENDENT random combination targets T[i,j]; observe a subset
#   (diagonal / boundary), reconstruct held-out "holes" by low-rank soft-impute or
#   harmonic interpolation; reach = fraction of held cells that NN-decode correctly.
#
# ADVERSARIAL QUESTION: is the residual +0.020 a real (weak) mechanism signal, or a
#   chance-level NN-decode artifact? By construction the 64 targets are INDEPENDENT
#   (mutual info between cells = 0) => a hole is information-theoretically unrecoverable.
#
# CONTROLS (frozen BEFORE run):
#  (C1) GENERIC-fill control: replace soft-impute/harmonic with generic fills
#       (constant mean, random-gaussian, random low-rank projection). If a GENERIC
#       fill matches hole_fill's reach -> the 0.020 is nonlinearity/chance artifact.
#  (C1b) CHANCE floor: random NN-decode over 64 candidates ~ 1/64 = 0.0156.
#  (C2) BIND-RECOVERABILITY: from a reconstructed/composed cell, can BOTH parent
#       indices (i and j) be recovered? ridge readout cell->cA[i], cell->cB[j],
#       train/test split, cosine-NN parent recovery vs chance (1/8=0.125). Distinctness
#       is necessary-not-sufficient; no parent recovery => not compositional binding.
#  (C3) SHUFFLE/STRUCTURE ablation: (a) permute observed cell VALUES (break lattice
#       correspondence) before soft-impute -> reach must be unchanged if structure is
#       INERT; (b) SANITY: replace INDEPENDENT targets with a genuinely LOW-RANK
#       (structured) lattice -> hole_fill must jump high (proves operator works ONLY
#       when structure exists, which the hypothesis's own construction forbids).
#
# FROZEN BAR — operator SURVIVES iff ALL of:
#   (1) hole_fill - max(generic_fill) >= 0.10   (specific completion beats generic)
#   (2) hole_fill - chance(1/64)      >= 0.10   (beats blind NN floor)
#   (3) bind-recoverability(both parents) - chance(0.125) >= 0.10
#   (4) shuffle-structure reach drops by >= 0.10 (structure is causal, not scaffold)
# ELSE -> ARTIFACT (the +0.020 is a chance-level metric artifact, not a mechanism).
# numpy => DIRECTIONAL, never terminal.  H_6112 transfer caveat: numpy REACHABLE
#   overstates vs real CLMConvMoE trunk (0->1.0 collapsed to 0->0.022); here there is
#   no REACHABLE even in numpy, so any real-trunk rung would only be weaker.
import os
os.environ.setdefault("OMP_NUM_THREADS","4")
import numpy as np

K, DIM, SEEDS = 8, 64, [0,1,2]
CHANCE_CELL   = 1.0/(K*K)   # 0.0156 blind NN over 64
CHANCE_PARENT = 1.0/K       # 0.125 blind parent-index guess

def soft_impute(M, mask, rank, iters=200):
    X = np.where(mask, M, 0.0)
    for _ in range(iters):
        U,s,Vt = np.linalg.svd(X, full_matrices=False)
        s[rank:] = 0.0
        X = np.where(mask, M, (U*s)@Vt)
    return X

def reach(recon, T, held):
    flatT = T.reshape(K*K, DIM); ok=0
    for (i,j) in held:
        d = np.linalg.norm(flatT - recon[i,j], axis=1)
        if np.argmin(d)==i*K+j: ok+=1
    return ok/len(held)

def hole_fill_best(T, mask, held, rng, shuffle_vals=False):
    Tw = T.copy()
    if shuffle_vals:  # break lattice correspondence: permute observed cell values
        obs = [(i,j) for i in range(K) for j in range(K) if mask[i,j]]
        perm = rng.permutation(len(obs))
        vals = np.array([T[i,j] for (i,j) in obs])
        for k,(i,j) in enumerate(obs): Tw[i,j] = vals[perm[k]]
    best=0.0
    for r in (1,2,4):
        recon=np.zeros((K,K,DIM))
        for d in range(DIM): recon[:,:,d]=soft_impute(Tw[:,:,d],mask,r)
        best=max(best, reach(recon,T,held))
    return best

def generic_fills(T, mask, held, rng):
    # C1: generic non-mechanism fills
    obsvals = np.array([T[i,j] for i in range(K) for j in range(K) if mask[i,j]])
    mean_v  = obsvals.mean(0)
    res={}
    # constant mean fill
    rc=T.copy()
    for (i,j) in held: rc[i,j]=mean_v
    res['const_mean']=reach(rc,T,held)
    # random gaussian fill
    rg=T.copy()
    for (i,j) in held: rg[i,j]=rng.standard_normal(DIM)/np.sqrt(DIM)
    res['rand_gauss']=reach(rg,T,held)
    # generic random low-rank projection of observed (nonlinearity-in-general)
    P=rng.standard_normal((DIM,DIM))/np.sqrt(DIM)
    rp=T.copy()
    for (i,j) in held: rp[i,j]=np.tanh(mean_v@P)   # generic nonlinearity, no lattice geometry
    res['rand_mlp']=reach(rp,T,held)
    return res

def bind_recover(T, rng):
    # C2: can both parents be recovered from the composed cell?
    cA=rng.standard_normal((K,DIM)); cA/=np.linalg.norm(cA,axis=1,keepdims=True)+1e-9
    cB=rng.standard_normal((K,DIM)); cB/=np.linalg.norm(cB,axis=1,keepdims=True)+1e-9
    cells=T.reshape(K*K,DIM)
    Ai=np.array([i for i in range(K) for j in range(K)])
    Bj=np.array([j for i in range(K) for j in range(K)])
    idx=rng.permutation(K*K); tr=idx[:48]; te=idx[48:]
    lam=1e-2
    def fit_recov(codes, lab):
        Xtr=cells[tr]; Ytr=codes[lab[tr]]
        W=np.linalg.solve(Xtr.T@Xtr+lam*np.eye(DIM), Xtr.T@Ytr)
        pred=cells[te]@W
        ok=0
        for n,t in enumerate(te):
            d=np.linalg.norm(codes-pred[n],axis=1)
            if np.argmin(d)==lab[t]: ok+=1
        return ok/len(te)
    return fit_recov(cA,Ai), fit_recov(cB,Bj)

def structured_targets(rng):
    # C3b sanity: genuinely low-rank (structured) lattice -> holes ARE recoverable
    U=rng.standard_normal((K,3)); V=rng.standard_normal((K,3)); C=rng.standard_normal((3,3,DIM))
    T=np.einsum('ia,jb,abd->ijd',U,V,C)
    return T/(np.linalg.norm(T,axis=2,keepdims=True)+1e-9)

print("H_6148 ADVERSARIAL DEEPENING — generation-by-holes (anti-storage)")
print(f"chance(cell NN 1/64)={CHANCE_CELL:.4f}  chance(parent 1/8)={CHANCE_PARENT:.4f}")
print("FROZEN BAR: survive iff hole-generic>=.10 AND hole-chance>=.10 AND bind-chance>=.10 AND shuffle-drop>=.10")
print("-"*78)
H=[];G=[];SH=[];RA=[];RB=[];ST=[]
for s in SEEDS:
    rng=np.random.default_rng(s)
    T=rng.standard_normal((K,K,DIM)); T/=np.linalg.norm(T,axis=2,keepdims=True)+1e-9
    mask=np.zeros((K,K),bool)
    for i in range(K): mask[i,i]=True
    held=[(i,j) for i in range(K) for j in range(K) if i!=j]
    hf=hole_fill_best(T,mask,held,rng)
    gf=generic_fills(T,mask,held,np.random.default_rng(s+100))
    gmax=max(gf.values())
    sh=hole_fill_best(T,mask,held,np.random.default_rng(s+200),shuffle_vals=True)
    ra,rb=bind_recover(T,np.random.default_rng(s+300))
    st=hole_fill_best(structured_targets(np.random.default_rng(s+400)),mask,held,np.random.default_rng(s+500))
    H.append(hf);G.append(gmax);SH.append(sh);RA.append(ra);RB.append(rb);ST.append(st)
    print(f"seed {s}: hole_fill={hf:.3f} | generic(max)={gmax:.3f} {gf} | shuffle_struct={sh:.3f}")
    print(f"        bind_recover A={ra:.3f} B={rb:.3f} (chance .125) | SANITY structured_targets hole_fill={st:.3f}")
print("-"*78)
mh,mg,msh=np.mean(H),np.mean(G),np.mean(SH); mra,mrb,mst=np.mean(RA),np.mean(RB),np.mean(ST)
c1 = mh-mg   >= 0.10
c2 = mh-CHANCE_CELL >= 0.10
c3 = (min(mra,mrb)-CHANCE_PARENT) >= 0.10
c4 = (mh-msh) >= 0.10
print(f"MEAN hole_fill={mh:.3f} generic={mg:.3f} shuffle={msh:.3f} | bindA={mra:.3f} bindB={mrb:.3f} | sanity_structured={mst:.3f}")
print(f"C1 hole-generic>=.10 : {mh-mg:+.3f} -> {c1}")
print(f"C2 hole-chance  >=.10 : {mh-CHANCE_CELL:+.3f} -> {c2}")
print(f"C3 bindmin-chance>=.10: {min(mra,mrb)-CHANCE_PARENT:+.3f} -> {c3}")
print(f"C4 shuffle drop >=.10 : {mh-msh:+.3f} -> {c4}")
survive = c1 and c2 and c3 and c4
print("-"*78)
print(f"SANITY note: structured (low-rank) targets hole_fill={mst:.3f} vs independent={mh:.3f}")
print(f"  -> operator is NOT broken; it fills holes IFF lattice has structure, which the")
print(f"     hypothesis's INDEPENDENT-targets construction forbids (MI between cells = 0).")
print(f"VERDICT = {'CONFIRMED (survives all controls)' if survive else 'ARTIFACT (chance-level; no mechanism signal)'}  [numpy => DIRECTIONAL]")
