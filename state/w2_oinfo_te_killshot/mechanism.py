"""Why can Omega see what Phi cannot?  Attribute the C2 signal to the estimator's blind spots.

faithful_phi reads |MI| (EVEN in rho -> sign destroyed) and takes a MIN-CUT (a sum of a subset of
entries).  Omega_gauss reads the LOGDET of the whole copula-correlation matrix (sign preserved,
whole-matrix geometry).  So the two disagree exactly when the arms differ in (a) the SIGN pattern
or (b) the joint determinant, at matched |MI| mass.  Measure both, descriptively.
"""
import json, sys
from pathlib import Path
import numpy as np
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[0] / "1283_content_instrument_repair")); sys.path.insert(0, str(HERE))
from gated import calibrate_beta, gen
from substrate import B_MULTI, X_SHARED
from estimators import normal_scores
from run_arms import BETA_SEEDS, T, W_STAR

beta, mu, sd = calibrate_beta(BETA_SEEDS, 4096)
ADJ=[(0,1),(1,2),(2,3),(3,0)]; DIAG=[(0,2),(1,3)]
out={}
for name, sub in [("gated", True), ("linear", False)]:
    acc={}
    for arm,mode,w in [("B",B_MULTI,0.5),("Xp",X_SHARED,W_STAR)]:
        C=[]
        for s in [12,13,14,15,16,17,18,19]:
            tr = gen(s, mode, T, gated=sub, beta=beta, mu=mu, sd=sd, w_relay=w) if mode==X_SHARED \
                 else gen(s, mode, T, gated=sub, beta=beta, mu=mu, sd=sd)
            C.append(np.corrcoef(normal_scores(tr)))
        C=np.mean(C,axis=0)
        mi=-0.5*np.log2(1-C**2+1e-15)   # gaussian-copula MI (what Phi's |MI| matrix approximates)
        acc[arm]={"rho_adj":float(np.mean([C[i,j] for i,j in ADJ])),
                  "rho_diag":float(np.mean([C[i,j] for i,j in DIAG])),
                  "mi_mass":float(sum(mi[i,j] for i,j in ADJ+DIAG)),
                  "logdet":float(np.linalg.slogdet(C)[1])}
    out[name]=acc
    b,x=acc["B"],acc["Xp"]
    print(f"[{name}]  rho_adj  B={b['rho_adj']:+.5f}  X'={x['rho_adj']:+.5f}   d={b['rho_adj']-x['rho_adj']:+.5f}")
    print(f"          rho_diag B={b['rho_diag']:+.5f}  X'={x['rho_diag']:+.5f}   d={b['rho_diag']-x['rho_diag']:+.5f}")
    print(f"          |MI| mass (what Phi sees) B={b['mi_mass']:.6f}  X'={x['mi_mass']:.6f}  d={b['mi_mass']-x['mi_mass']:+.6f}")
    print(f"          logdet    (what Omega sees) B={b['logdet']:+.6f}  X'={x['logdet']:+.6f}  d={b['logdet']-x['logdet']:+.6f}")
json.dump(out, open(HERE/"mechanism.json","w"), indent=2)
