#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATD-3 ρ-density ladder — the one pre-registered ATD axis not yet swept.

CLEAN-KILL was established at the default pair-coverage ρ=0.6. This closes the ρ-axis: does DENSER (or
sparser) authored-pair coverage rescue the transferable-bilinear geometry? Reuses atd_crux.build_corpus
(coverage=ρ) + the well-posed clean-geometry measurement (model singles → ground-truth t on held-out,
FiLM vs additive). λ=1 throughout. Fable spec: 1-seed scan, 3-seed only at a boundary flip.

  flip signal: any ρ with clean-geom delta >= +0.10 AND film_t R2 > 0 -> coverage threshold found (reopen).
  else: KILL holds across coverage -> ATD-3 closed, battery complete.
"""
import os, sys, json, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import atd_crux as A
from atd_clean_geom import cell as _base_cell  # (lam, seed) fixed-coverage helper — we override coverage below
from atd0_anchor import latents, operator, target, TRAIN_C, HELD_C

def r2(p,t): return 1.0 - np.sum((p-t)**2)/np.sum((t-t.mean(0))**2)
def rfit(F,Y,lam=1.0):
    B=np.hstack([F,np.ones((len(F),1))]); return np.linalg.solve(B.T@B+lam*np.eye(B.shape[1]),B.T@Y)
def rpred(w,F): return np.hstack([F,np.ones((len(F),1))])@w

def cell_rho(rho, seed, d_low=48):
    corpus, z, OP, name = A.build_corpus(1.0, seed, coverage=rho)   # lam=1, coverage=rho
    lh, gr = A.train_bytelm(corpus, seed)
    allc = TRAIN_C + HELD_C
    S = np.stack([lh("{h} : ".format(h=name[c])) for c in allc])
    mu = S.mean(0); U,Sg,Vt = np.linalg.svd(S-mu, full_matrices=False); P = Vt[:d_low].T
    Sl = {c:(S[i]-mu)@P for i,c in enumerate(allc)}
    rs = np.random.RandomState(seed+77)
    def pj(pool,k):
        o=set()
        while len(o)<k:
            a,b=int(rs.choice(pool)),int(rs.choice(pool))
            if a!=b: o.add((a,b))
        return list(o)
    trp=pj(TRAIN_C,2000); tep=[(a,b) for a in HELD_C for b in HELD_C if a!=b]
    ha=lambda ps:np.stack([Sl[a] for a,b in ps]); hb=lambda ps:np.stack([Sl[b] for a,b in ps])
    Gtr=np.stack([target(z,OP,a,b) for a,b in trp]); Gte=np.stack([target(z,OP,a,b) for a,b in tep])
    wa=rfit(np.hstack([ha(trp),hb(trp)]),Gtr); add=r2(rpred(wa,np.hstack([ha(tep),hb(tep)])),Gte)
    wf=rfit(np.hstack([ha(trp)*hb(trp),ha(trp),hb(trp)]),Gtr)
    film=r2(rpred(wf,np.hstack([ha(tep)*hb(tep),ha(tep),hb(tep)])),Gte)
    return dict(rho=rho, seed=seed, add_t=float(add), film_t=float(film), delta=float(film-add))

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--rhos",default="1.0,0.3,0.1"); ap.add_argument("--seeds",default="0")
    ap.add_argument("--out",default="ATD3_RHO_RESULT.json"); a=ap.parse_args()
    rhos=[float(x) for x in a.rhos.split(",")]; seeds=[int(x) for x in a.seeds.split(",")]
    cells=[]
    for rho in rhos:
        for sd in seeds:
            c=cell_rho(rho,sd); cells.append(c)
            print(f"  rho={rho:.2f} seed={sd}: add_t={c['add_t']:.3f} film_t={c['film_t']:.3f} delta={c['delta']:+.3f}",flush=True)
    flip=[c for c in cells if c['delta']>=0.10 and c['film_t']>0]
    verdict = "RHO-FLIP-coverage-threshold-found" if flip else "KILL-HOLDS-across-coverage-ATD3-closed"
    out=dict(probe="ATD-3 rho-density ladder (lam=1, clean-geom measure)", cells=cells,
             flip=[{k:c[k] for k in('rho','delta','film_t')} for c in flip], verdict=verdict)
    json.dump(out,open(os.path.join(HERE,a.out),"w"),ensure_ascii=False,indent=1)
    print(f"\nATD-3 VERDICT: {verdict}")

if __name__ == "__main__":
    main()
