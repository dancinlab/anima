# H_6148 — 생성 없는 생성 (hole / topological defect)
# MECHANISM: anima leaves only HOLES in the anchor lattice; the combination
#   exists as a topological defect and the READER fills it (생성 없는 생성).
#   i.e. the combination is NOT stored anywhere — it must be RECONSTRUCTED
#   from the surrounding lattice structure (boundary / neighbors).
#
# This is the ANTI-STORAGE sibling of H_6143 (kosmos-merge) which REACHED 24/24
# in toy precisely BECAUSE it explicitly STORES each merged combination as a
# persistent discrete anchor. H_6148 refuses to store -> the test is whether a
# hole can be filled from structure alone for GENUINELY INDEPENDENT concepts.
#
# Task: 2 INDEPENDENT concept axes A,B (K=8 each) -> K*K=64 distinct combination
#   target embeddings T[i,j] (independent random, NOT additive). We observe a
#   subset of the lattice and hold out the rest as HOLES.
#   - ADDITIVE baseline: ridge map (cA[i]+cB[j]) -> target, trained on observed.
#   - HOLE-FILL operator (H_6148): reconstruct the held-out combination cell by
#       low-rank matrix completion (soft-impute) of the K*K lattice PLUS harmonic
#       neighbor fill; TWO observation regimes (diagonal-only, boundary row+col),
#       take the MOST GENEROUS reach for the operator.
#   Score = fraction of held-out combos whose reconstruction nearest-neighbor
#       decodes to the correct one of the 64 true targets (reachability).
#
# FROZEN BAR (set BEFORE run): GREEN-DIRECTIONAL iff
#   hole_fill_reach >= additive_reach + 0.30  AND  additive_reach <= 0.20
#   on >= 2/3 seeds. Else FALSIFIED/floor. numpy => DIRECTIONAL, never terminal.

import numpy as np

K   = 8      # codewords per axis
DIM = 64     # embedding dim
SEEDS = [0, 1, 2]

def soft_impute(M, mask, rank, iters=200):
    # iterative low-rank completion; mask=1 where observed
    X = np.where(mask, M, 0.0)
    for _ in range(iters):
        U, s, Vt = np.linalg.svd(X, full_matrices=False)
        s[rank:] = 0.0
        Xr = (U * s) @ Vt
        X = np.where(mask, M, Xr)
    return X

def harmonic_fill(M, mask, iters=500):
    # Laplace/harmonic interpolation: hole = mean of 4-neighbors, boundary fixed
    X = np.where(mask, M, 0.0)
    Kx = M.shape[0]
    for _ in range(iters):
        up    = np.vstack([X[0:1,:],  X[:-1,:]])
        down  = np.vstack([X[1:,:],   X[-1:,:]])
        left  = np.hstack([X[:,0:1],  X[:,:-1]])
        right = np.hstack([X[:,1:],   X[:,-1:]])
        avg = (up+down+left+right)/4.0
        X = np.where(mask, M, avg)
    return X

def reach_from_reconstruction(recon, T, held):
    # recon,T shape (K,K,DIM). held = list of (i,j). NN-decode among all 64.
    flatT = T.reshape(K*K, DIM)
    ok = 0
    for (i,j) in held:
        v = recon[i,j]
        d = np.linalg.norm(flatT - v, axis=1)
        if np.argmin(d) == i*K+j:
            ok += 1
    return ok/len(held)

def run_seed(seed):
    rng = np.random.default_rng(seed)
    # independent combination targets (NOT additive): 64 distinct random unit vecs
    T = rng.standard_normal((K,K,DIM))
    T /= np.linalg.norm(T,axis=2,keepdims=True)+1e-9
    # pure-concept marginal codes (for the additive baseline)
    cA = rng.standard_normal((K,DIM)); cA/=np.linalg.norm(cA,axis=1,keepdims=True)+1e-9
    cB = rng.standard_normal((K,DIM)); cB/=np.linalg.norm(cB,axis=1,keepdims=True)+1e-9

    # ---- observation regimes ----
    # (a) diagonal-only observed (mirrors meiosis probe): known = (i,i)
    mask_diag = np.zeros((K,K),bool); 
    for i in range(K): mask_diag[i,i]=True
    held_diag = [(i,j) for i in range(K) for j in range(K) if i!=j]
    # (b) boundary observed (true topological-defect boundary-value): row0+col0
    mask_bnd = np.zeros((K,K),bool); mask_bnd[0,:]=True; mask_bnd[:,0]=True
    held_bnd = [(i,j) for i in range(1,K) for j in range(1,K)]

    # ===== ADDITIVE baseline (trained on diagonal known cells) =====
    Xtr = np.array([cA[i]+cB[i] for i in range(K)])          # (K,DIM)
    Ytr = np.array([T[i,i]      for i in range(K)])          # (K,DIM)
    lam=1e-2
    W = np.linalg.solve(Xtr.T@Xtr + lam*np.eye(DIM), Xtr.T@Ytr)  # (DIM,DIM)
    recon_add = np.zeros((K,K,DIM))
    for i in range(K):
        for j in range(K):
            recon_add[i,j] = (cA[i]+cB[j])@W
    add_reach = reach_from_reconstruction(recon_add, T, held_diag)

    # ===== HOLE-FILL operator (H_6148): complete the lattice from structure =====
    best_hole = 0.0
    for (mask,held,label) in [(mask_diag,held_diag,'diag'),(mask_bnd,held_bnd,'bnd')]:
        for rank in (1,2,4):
            recon = np.zeros((K,K,DIM))
            for d in range(DIM):
                recon[:,:,d] = soft_impute(T[:,:,d], mask, rank)
            r1 = reach_from_reconstruction(recon, T, held)
            best_hole = max(best_hole, r1)
        # harmonic variant
        reconh = np.zeros((K,K,DIM))
        for d in range(DIM):
            reconh[:,:,d] = harmonic_fill(T[:,:,d], mask)
        best_hole = max(best_hole, reach_from_reconstruction(reconh, T, held))
    return add_reach, best_hole

print("H_6148 generation-by-holes DIRECTIONAL probe")
print("FROZEN BAR: hole_fill >= additive+0.30 AND additive<=0.20 on >=2/3 seeds")
print(f"K={K} DIM={DIM} | 64 INDEPENDENT combination targets | holes reconstructed from structure")
print("-"*72)
wins=0; adds=[]; holes=[]
for s in SEEDS:
    a,h = run_seed(s)
    adds.append(a); holes.append(h)
    win = (h >= a+0.30) and (a <= 0.20)
    wins += int(win)
    print(f"seed {s}: additive_reach={a:.3f}  hole_fill_reach(best)={h:.3f}  lift={h-a:+.3f}  win={win}")
print("-"*72)
ma=float(np.mean(adds)); mh=float(np.mean(holes))
green = (wins>=2)
print(f"mean additive={ma:.3f}  mean hole_fill={mh:.3f}  mean lift={mh-ma:+.3f}  wins={wins}/3")
print(f"DECISION={'GREEN-DIRECTIONAL' if green else 'FALSIFIED-FLOOR'}  (numpy => DIRECTIONAL, transfer-unverified)")
