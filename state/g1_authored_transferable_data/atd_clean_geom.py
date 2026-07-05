#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ATD clean-geometry probe — resolve the ATD-1 negative-R² measurement caveat.

The ATD-1 rep-crux predicted the model's OWN joint rep h(a,b) (high-D, out-of-distribution on held-out
concepts) => additive/FiLM both hit negative R² (readout extrapolation failure) => the FiLM-vs-additive
delta was measurement-limited for the KILL verdict. This probe uses a WELL-POSED bounded target instead:
predict GROUND-TRUTH t(z_a,z_b) (the authored bilinear value, D-dim, tanh-bounded) from the model's
single reps h(a),h(b) on HELD-OUT disjoint pairs, additive vs FiLM. If the model's singles carry the
transferable structure, a bilinear readout recovers t with positive R² and FiLM >> additive; if not,
both floor. This directly tests whether authored data put recoverable transferable bilinear structure
into the reps, WITHOUT the OOD-joint-rep artifact.

  clean-PASS : FiLM cross-R2(->t) - additive cross-R2 >= 0.10 median & FiLM cross-R2 > 0  (structure recoverable, bilinear)
  clean-KILL : delta <= 0.03  (authored data did NOT put recoverable transferable bilinear structure in reps)
lambda=0 control must floor (both ~0). toy=DIRECTIONAL; summer torch.
"""
import os, sys, json, argparse
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import atd_crux as A
from atd0_anchor import latents, operator, target, TRAIN_C, HELD_C

def r2(p, t): return 1.0 - np.sum((p-t)**2)/np.sum((t-t.mean(0))**2)
def rfit(F, Y, lam=1.0):
    B = np.hstack([F, np.ones((len(F),1))]); return np.linalg.solve(B.T@B+lam*np.eye(B.shape[1]), B.T@Y)
def rpred(w, F): return np.hstack([F, np.ones((len(F),1))])@w

def cell(lam, seed, d_low=48):
    corpus, z, OP, name = A.build_corpus(lam, seed)
    lh, gr = A.train_bytelm(corpus, seed)
    allc = TRAIN_C + HELD_C
    S = np.stack([lh("{h} : ".format(h=name[c])) for c in allc])
    mu = S.mean(0); U,Sg,Vt = np.linalg.svd(S-mu, full_matrices=False); P = Vt[:d_low].T
    Sl = {c: (S[i]-mu)@P for i,c in enumerate(allc)}
    rs = np.random.RandomState(seed+77)
    def pj(pool,k):
        o=set()
        while len(o)<k:
            a,b=int(rs.choice(pool)),int(rs.choice(pool))
            if a!=b: o.add((a,b))
        return list(o)
    trp = pj(TRAIN_C, 2000); tep = [(a,b) for a in HELD_C for b in HELD_C if a!=b]
    ha=lambda ps: np.stack([Sl[a] for a,b in ps]); hb=lambda ps: np.stack([Sl[b] for a,b in ps])
    Gtr = np.stack([target(z,OP,a,b) for a,b in trp]); Gte = np.stack([target(z,OP,a,b) for a,b in tep])
    # additive: [h_a, h_b] -> t
    wa = rfit(np.hstack([ha(trp),hb(trp)]), Gtr); add = r2(rpred(wa, np.hstack([ha(tep),hb(tep)])), Gte)
    # FiLM/bilinear: [h_a*h_b, h_a, h_b] -> t
    wf = rfit(np.hstack([ha(trp)*hb(trp), ha(trp), hb(trp)]), Gtr)
    film = r2(rpred(wf, np.hstack([ha(tep)*hb(tep), ha(tep), hb(tep)])), Gte)
    # shuffle control
    perm = rs.permutation(len(tep)); hbs = hb(tep)[perm]
    film_sh = r2(rpred(wf, np.hstack([ha(tep)*hbs, ha(tep), hbs])), Gte)
    return dict(lam=lam, seed=seed, add_t=float(add), film_t=float(film), delta=float(film-add),
                film_shuf=float(film_sh))

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--lams", default="1.0,0.0"); ap.add_argument("--seeds", default="0,1,2")
    ap.add_argument("--out", default="ATD_CLEANGEOM_RESULT.json"); a = ap.parse_args()
    lams=[float(x) for x in a.lams.split(",")]; seeds=[int(x) for x in a.seeds.split(",")]
    cells=[]
    for lam in lams:
        for sd in seeds:
            c=cell(lam,sd); cells.append(c)
            print(f"  lam={lam:.2f} seed={sd}: add_t={c['add_t']:.3f} film_t={c['film_t']:.3f} "
                  f"delta={c['delta']:+.3f} film_shuf={c['film_shuf']:.3f}", flush=True)
    def agg(lam):
        s=[c for c in cells if c['lam']==lam]
        return dict(lam=lam, med_add=float(np.median([c['add_t'] for c in s])),
                    med_film=float(np.median([c['film_t'] for c in s])),
                    med_delta=float(np.median([c['delta'] for c in s])),
                    min_delta=float(np.min([c['delta'] for c in s])), n=len(s))
    ladder=[agg(l) for l in lams]
    a1=next((x for x in ladder if x['lam']==1.0),None); a0=next((x for x in ladder if x['lam']==0.0),None)
    if a1 and a1['med_delta']>=0.10 and a1['med_film']>0 and a1['min_delta']>0.03:
        verdict="CLEAN-PASS-authored-structure-recoverable-bilinear"
    elif a1 and a1['med_delta']<=0.03:
        verdict="CLEAN-KILL-no-recoverable-transferable-bilinear"
    else: verdict="CLEAN-INCONCLUSIVE"
    out=dict(probe="ATD clean-geometry (predict ground-truth t from model singles, held-out)",
             ladder=ladder, alpha1=a1, alpha0=a0, verdict=verdict, cells=cells)
    json.dump(out, open(os.path.join(HERE,a.out),"w"), ensure_ascii=False, indent=1)
    print(f"\nCLEAN-GEOM VERDICT: {verdict}")
    if a1: print(f"  lam=1: med_delta={a1['med_delta']:+.3f} med_film_t={a1['med_film']:.3f} med_add_t={a1['med_add']:.3f}")
    if a0: print(f"  lam=0 control: med_delta={a0['med_delta']:+.3f} med_film_t={a0['med_film']:.3f}")

if __name__ == "__main__":
    main()
