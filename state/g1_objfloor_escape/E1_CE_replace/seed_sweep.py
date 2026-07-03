import importlib, sys, numpy as np
import toy_ce_replace_contrastive as T
def run(seed):
    T.RNG = np.random.default_rng(seed)
    # rebuild split under this seed
    concepts=list(range(T.N_CONCEPTS))
    pairs=[(a,b) for a in concepts for b in concepts if a!=b]
    T.RNG.shuffle(pairs); nh=int(len(pairs)*T.HELD_FRAC)
    T.HELD=set(map(tuple,pairs[:nh])); T.SEEN=[p for p in pairs if p not in T.HELD]
    add=T.train(T.AddEnergy(),"ADD",epochs=400); ra=T.evaluate(add,f"ADD.s{seed}")
    tpr=T.train(T.TPREnergy(),"TPR",epochs=400); rt=T.evaluate(tpr,f"TPR.s{seed}")
    return ra,rt
rows=[]
for s in [11,23,42,101,777]:
    ra,rt=run(s)
    rows.append((s,ra['margin'],ra['reach_novel'],ra['scramble'],rt['margin'],rt['reach_novel'],rt['scramble']))
print("\n=== SEED SWEEP (ADD=Escape-1 target | TPR=attribution) ===")
print(f"{'seed':>5} | {'ADD_margin':>10} {'ADD_reachN':>10} {'ADD_scr':>7} | {'TPR_margin':>10} {'TPR_reachN':>10} {'TPR_scr':>7}")
add_floor=0; tpr_reach=0
for s,am,ar,asc,tm,tr,tsc in rows:
    print(f"{s:>5} | {am:>+10.4f} {ar:>10.2f} {asc:>7.2f} | {tm:>+10.4f} {tr:>10.2f} {tsc:>7.2f}")
    if am<=1e-3 or ar==0.0: add_floor+=1
    if tm>1e-3 and tr>0 and tsc<0.5: tpr_reach+=1
print(f"\nADD AT-FLOOR: {add_floor}/{len(rows)} seeds | TPR REACHABLE: {tpr_reach}/{len(rows)} seeds")
