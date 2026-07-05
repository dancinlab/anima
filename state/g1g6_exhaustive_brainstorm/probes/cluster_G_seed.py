#!/usr/bin/env python3
"""Cluster G — seed-sensitivity $0 interaction probe (anima H_9200)."""
import json, numpy as np
# H_9131 derisk (verbatim, state/verdicts/trunk_obj_noncommutative/H_9131_derisk.md)
h9131 = {"seeds":[7,4302,4303],
    "bind":[0.2726,0.3047,0.1843],"additive":[0.4844,0.4935,0.5178],
    "shuffle":[0.0567,-0.0599,-0.0409],"sym_ref":[0.0677,0.0504,0.0607]}
# gamma_step0 (state/g1_gamma_engine_native/step0_result.json)
gamma = {"seeds":[7,4302,4303],
    "ADD":[0.944,0.920,0.960],"HAD":[0.760,0.792,0.640],"BIND":[0.864,0.712,0.808]}

def analyze(name, gap_vec, seed_vec):
    g=np.array(gap_vec,float); signs=np.sign(g)
    neg=int((signs<0).sum()); pos=int((signs>0).sum())
    majority=-1 if neg>pos else (1 if pos>neg else 0)
    flips=int((signs!=majority).sum()); n=len(g); fr=flips/n
    cv=float(np.std(g)/(abs(np.mean(g))+1e-9))
    print(f"\n=== {name} ===")
    print(f"  seeds: {seed_vec}")
    print(f"  gap(BIND-ADD): {[round(x,4) for x in g]}")
    print(f"  sign/seed: {[int(s) for s in signs]} (neg={neg} pos={pos}) majority={majority}")
    print(f"  flip_rate: {flips}/{n} = {fr:.3f}  (PREREG bar>=1/3 = {'TRIP' if fr>=1/3 else 'NO'})")
    print(f"  CV(gap): {cv:.3f}")
    return {"dataset":name,"flip_rate":round(fr,4),"cv":round(cv,4),
            "seed_is_confound": bool(fr>=1/3)}

print("="*72); print("Cluster G — seed-sensitivity $0 probe (frozen bar PRE-REGISTERED)"); print("="*72)
print("PREREG: flip_rate>=1/3 => seed is real interaction(confound); ==0 => floor seed-robust.")
r1=analyze("H_9131 non-commutative (gap=bind_R2-additive_R2)",
    [h9131["bind"][i]-h9131["additive"][i] for i in range(3)], h9131["seeds"])
r2=analyze("gamma_step0 constructive-bind (gap=BIND-ADD_recomb)",
    [gamma["BIND"][i]-gamma["ADD"][i] for i in range(3)], gamma["seeds"])
print("\n=== single-seed rescue check (PREREG delta=0.10) ===")
for ds,b,a,s in [("H_9131",h9131["bind"],h9131["additive"],h9131["seeds"]),
                 ("gamma  ",gamma["BIND"],gamma["ADD"],gamma["seeds"])]:
    rescue=[s[i] for i in range(3) if (b[i]-a[i])>=0.10]
    print(f"  {ds}: seeds w/ BIND-ADD>=0.10 -> {rescue if rescue else 'NONE'}")
both = (not r1["seed_is_confound"]) and (not r2["seed_is_confound"])
print("\n"+"="*72); print("VERDICT"); print("="*72)
print(f"  H_9131 seed-confound: {r1['seed_is_confound']} (fr={r1['flip_rate']})")
print(f"  gamma  seed-confound: {r2['seed_is_confound']} (fr={r2['flip_rate']})")
if both:
    print("  => GREEN: seed is NOT a hidden interaction for the G1 recombination floor.")
    print("     Floored levers seed-robust at {7,4302,4303}; single-seed claims NOT confounded.")
    print("     Cluster-G seed-sensitivity axis: RULED OUT as a wall-break lever.")
else:
    print("  => WALL/INCONCLUSIVE: seed flips verdict in >=1 dataset.")
print("\nJSON:", json.dumps({"results":[r1,r2],"both_seed_robust":bool(both)}))
