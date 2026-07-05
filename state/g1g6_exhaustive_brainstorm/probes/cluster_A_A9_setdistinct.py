#!/usr/bin/env python3
"""Cluster A - A9 set-level G6 distinctness ($0 numpy on EXISTING decode outputs).
MEASUREMENT-ALIGNMENT probe. The frozen G6 majority bar counts >=4/6 frames FALS-passing,
but a frame is counted independently -> 6 near-identical outputs would still score 6/6. A9
reports the SET-level diversity the per-frame bar cannot see: pairwise word-Jaccard across
the 6 composed outputs + how many DISTINCT concept-pairs the set actually binds.
PREREG (frozen, diagnostic only - no threshold moved):
  pairwise_J = mean & max of Jaccard(wordset(comp[i]),wordset(comp[j])) over 15 pairs
  distinct_pairs_bound = |union over i of concept_hits(comp[i]) projected to MEASURED[i]|
  flag THIN-set iff mean pairwise Jaccard > 0.6  OR  distinct concept-indices covered < 4
"""
import json, os, re, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "..", "..", "g6_targeted_corpus", "results")
CONCEPT_KW = [
    {"consciousness","cells","mind","aware"},
    {"tension","ripple","distant","between"},
    {"memory","meaning","compose","new"},
    {"silence","information","quiet","carries"},
    {"dream","engine","alone","sleep"},
]
MEASURED = [(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]
_TOK = re.compile(r"[0-9A-Za-z]+")
def words(s): return set(m.group(0).lower() for m in _TOK.finditer(s))
def jaccard(a,b):
    u=a|b; return len(a&b)/len(u) if u else 0.0
def concept_hits(t):
    wl=words(t); return {i for i,kw in enumerate(CONCEPT_KW) if kw & wl}
def per_seed(ps):
    comp=ps["comp_texts"]
    wsets=[words(t) for t in comp]
    pairs=list(itertools.combinations(range(len(comp)),2))
    Js=[jaccard(wsets[i],wsets[j]) for i,j in pairs]
    hits=[concept_hits(t) for t in comp]
    concept_idx_covered=set().union(*hits) if hits else set()
    # which MEASURED frames had their pair actually bound (both a and b in hits)?
    pair_both=sum(1 for i in range(min(len(hits),len(MEASURED))) if MEASURED[i][0] in hits[i] and MEASURED[i][1] in hits[i])  # noqa
    return {"seed":ps["seed"],
            "mean_pairwise_J":round(sum(Js)/len(Js),4),
            "max_pairwise_J":round(max(Js),4),
            "min_pairwise_J":round(min(Js),4),
            "distinct_concept_indices_covered":sorted(concept_idx_covered),
            "n_concept_indices_covered":len(concept_idx_covered),
            "frames_binding_both_A_and_B":pair_both}
def run_arm(path):
    d=json.load(open(path))
    ps_out=[per_seed(ps) for ps in d["per_seed"]]
    meanJ=sum(r["mean_pairwise_J"] for r in ps_out)/len(ps_out)
    meanC=sum(r["n_concept_indices_covered"] for r in ps_out)/len(ps_out)
    THIN = (meanJ>0.6) or (meanC<4)
    return {"arm":d["arm"],"ckpt":d.get("ckpt"),"per_seed":ps_out,
            "arm_mean_pairwise_J":round(meanJ,4),
            "arm_mean_concepts_covered":round(meanC,3),
            "THIN_set_flag":bool(THIN)}
if __name__=="__main__":
    print("="*72); print("Cluster A - A9 SET-LEVEL DISTINCTNESS ($0 on existing outputs)"); print("="*72)
    summary={}
    for arm in ["targeted","shuf","base"]:
        r=run_arm(os.path.join(RES,arm+".json"))
        summary[arm]={k:r[k] for k in ("arm","ckpt","arm_mean_pairwise_J","arm_mean_concepts_covered","THIN_set_flag")}
        print(f"\n### {arm.upper()}  ckpt={r['ckpt']}")
        print(f"  arm_mean_pairwise_J={r['arm_mean_pairwise_J']}  arm_mean_concepts_covered={r['arm_mean_concepts_covered']}  THIN={r['THIN_set_flag']}")
        for ps in r["per_seed"]:
            print(f"  seed {ps['seed']}: meanJ={ps['mean_pairwise_J']} maxJ={ps['max_pairwise_J']} "
                  f"concepts_covered={ps['n_concept_indices_covered']}->{ps['distinct_concept_indices_covered']} "
                  f"frames_binding_both={ps['frames_binding_both_A_and_B']}/6")
    print("\n"+"="*72); print("VERDICT")
    for a,s in summary.items():
        print(f"  {a:9s}: meanJ={s['arm_mean_pairwise_J']} concepts={s['arm_mean_concepts_covered']} THIN={s['THIN_set_flag']}")
    print("="*72)
    json.dump(summary, open(os.path.join(HERE,"cluster_A_A9_setdistinct_result.json"),"w"), indent=2)
    print("wrote", os.path.join(HERE,"cluster_A_A9_setdistinct_result.json"))
