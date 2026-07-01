import os
os.environ["OMP_NUM_THREADS"]="4"
import numpy as np

# =====================================================================
# H_6121 gen_rna_alternative_splicing — ADVERSARIAL DEEPENING PROBE
# Operator under test: DISCRETE SELECT+SPLICE ("RNA alternative splicing")
#   given two parent vectors A,B in R^d ("exon dims"), pick a per-pair
#   binary splice mask m in {0,1}^d and emit  C = m*A + (1-m)*B.
#   The cheap numpy screen scored composed_distinct (C differs from both
#   parents) -> REACHABLE 0->~1.0.  We adversarially test whether that
#   REACHABLE is REAL COMPOSITION or a metric artifact of mixing-in-general.
#
# FROZEN BAR (set BEFORE running — operator SURVIVES iff ALL three hold):
#   (C1) GENERIC-NONLINEARITY: splice_distinct is NOT matched by generic
#        ops {tanh(A+B), A*B, random-proj MLP}.  survive iff
#        splice_distinct - max(generic_distinct) >= 0.20
#   (C2) BIND-RECOVERABILITY (held-out): a fixed linear readout recovers
#        BOTH parents from C better than the additive floor C=A+B.
#        survive iff mean splice R2(recover A,B) - additive R2 >= 0.15
#   (C3) ABLATION: turning OFF the discrete-select ingredient (replace the
#        binary mask with the additive-average floor) must COLLAPSE
#        composed_distinct.  survive iff ablated_distinct < 0.5*splice_distinct
# Default to ARTIFACT if uncertain (a_break_the_wall; H_6112 precedent:
#   numpy REACHABLE 0->1.0 collapsed to 0->0.022 on the real trunk).
# =====================================================================

rng = np.random.default_rng(6121)
d   = 64          # exon dims
Ntr = 400         # train pairs (for readout fit)
Nte = 200         # held-out pairs
EPS = 1e-6

def parents(N):
    A = rng.standard_normal((N,d))
    B = rng.standard_normal((N,d))
    return A,B

def distinct_frac(C,A,B):
    # fraction of composed rows distinct from BOTH parents (L2, normalized)
    dA = np.linalg.norm(C-A,axis=1)/ (np.linalg.norm(A,axis=1)+EPS)
    dB = np.linalg.norm(C-B,axis=1)/ (np.linalg.norm(B,axis=1)+EPS)
    return float(np.mean((dA>0.1)&(dB>0.1)))

def r2(y_true,y_pred):
    ss_res=np.sum((y_true-y_pred)**2)
    ss_tot=np.sum((y_true-np.mean(y_true,axis=0))**2)
    return 1.0 - ss_res/(ss_tot+EPS)

def fit_readout(C_tr,Y_tr,C_te,Y_te):
    # least-squares linear readout C->Y (fixed across pairs), report held-out R2
    W,_,_,_ = np.linalg.lstsq(C_tr,Y_tr,rcond=None)
    return r2(Y_te, C_te@W)

# ---- build parents ----
Atr,Btr = parents(Ntr); Ate,Bte = parents(Nte)

# per-pair random binary splice mask (biological: splice sites vary per transcript)
def mask(N): return (rng.random((N,d))<0.5).astype(float)
Mtr,Mte = mask(Ntr), mask(Nte)

# ---- SPLICE operator (the mechanism under test) ----
Csp_tr = Mtr*Atr + (1-Mtr)*Btr
Csp_te = Mte*Ate + (1-Mte)*Bte
splice_distinct = distinct_frac(Csp_te,Ate,Bte)

# ---- (C1) GENERIC NONLINEARITIES ----
def mlp(A,B,W1,W2):
    h=np.maximum(0.0, np.concatenate([A,B],axis=1)@W1)
    return h@W2
W1=rng.standard_normal((2*d,d)); W2=rng.standard_normal((d,d))
gen = {
  "tanh(A+B)": (np.tanh(Ate+Bte)),
  "A*B"      : (Ate*Bte),
  "randMLP"  : mlp(Ate,Bte,W1,W2),
}
gen_distinct = {k:distinct_frac(v,Ate,Bte) for k,v in gen.items()}
max_gen = max(gen_distinct.values())
c1_margin = splice_distinct - max_gen
C1_survive = c1_margin >= 0.20

# ---- (C2) BIND-RECOVERABILITY (held-out) ----
# splice: recover A and B from C
sp_rA = fit_readout(Csp_tr,Atr,Csp_te,Ate)
sp_rB = fit_readout(Csp_tr,Btr,Csp_te,Bte)
sp_rec = 0.5*(sp_rA+sp_rB)
# additive floor: C = A+B
Cad_tr = Atr+Btr; Cad_te = Ate+Bte
ad_rA = fit_readout(Cad_tr,Atr,Cad_te,Ate)
ad_rB = fit_readout(Cad_tr,Btr,Cad_te,Bte)
ad_rec = 0.5*(ad_rA+ad_rB)
c2_margin = sp_rec - ad_rec
C2_survive = c2_margin >= 0.15

# ---- (C3) ABLATION: turn OFF discrete select -> additive-average floor ----
Cab_te = 0.5*(Ate+Bte)          # ingredient (binary selection) removed
abl_distinct = distinct_frac(Cab_te,Ate,Bte)
C3_survive = abl_distinct < 0.5*splice_distinct

SURVIVES = C1_survive and C2_survive and C3_survive

print("="*66)
print("H_6121 alternative-splicing (discrete select+splice) — DEEPEN")
print("="*66)
print(f"splice composed_distinct (held-out) = {splice_distinct:.3f}   (numpy screen REACHABLE)")
print()
print("[C1] GENERIC-NONLINEARITY control (does mixing-in-general match it?)")
for k,v in gen_distinct.items():
    print(f"     {k:10s} composed_distinct = {v:.3f}")
print(f"     splice - max(generic)  = {c1_margin:+.3f}  (survive iff >= +0.20)  -> {'PASS' if C1_survive else 'FAIL'}")
print()
print("[C2] BIND-RECOVERABILITY (fixed linear readout C->parents, held-out R2)")
print(f"     splice   R2(A)={sp_rA:+.3f} R2(B)={sp_rB:+.3f} mean={sp_rec:+.3f}")
print(f"     additive R2(A)={ad_rA:+.3f} R2(B)={ad_rB:+.3f} mean={ad_rec:+.3f}")
print(f"     splice - additive      = {c2_margin:+.3f}  (survive iff >= +0.15)  -> {'PASS' if C2_survive else 'FAIL'}")
print()
print("[C3] ABLATION (discrete select OFF -> additive-average floor)")
print(f"     ablated composed_distinct = {abl_distinct:.3f}   (must be < {0.5*splice_distinct:.3f})  -> {'PASS(collapse)' if C3_survive else 'FAIL(no-collapse)'}")
print()
print("-"*66)
verdict = "CONFIRMED (real composition signal)" if SURVIVES else "ARTIFACT (numpy REACHABLE was a metric artifact)"
print(f"FROZEN BAR (C1 AND C2 AND C3) -> {'SURVIVES' if SURVIVES else 'REFUTED'}  => {verdict}")
print("NOTE: numpy DIRECTIONAL only. H_6112 precedent: numpy 0->1.0 collapsed to 0->0.022 on real CLMConvMoE trunk.")
print("="*66)
