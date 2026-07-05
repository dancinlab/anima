#!/usr/bin/env python3
"""Cluster A - A6 intervention sensitivity (per-frame), $0 numpy on EXISTING decode outputs.
MEASUREMENT-ALIGNMENT probe. Detects whether the G6 'genuine topic bind' verdict survives a
per-frame intervention test, or whether B-persistence across composed/shuffled outputs reveals
the bind as bag/form gaming. No model load. No threshold moved (PREREG frozen before run).
PREREG: intervention_sensitive[i] = comp_has_B AND NOT shuf_has_B;
        PASS_arm := >=4/6 sensitive frames on >=2/3 seeds (mirrors frozen FAS majority bar).
"""
import json, os, re
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
def words(s): return [m.group(0).lower() for m in _TOK.finditer(s)]
def concept_hits(t):
    wl=set(words(t)); return {i for i,kw in enumerate(CONCEPT_KW) if kw & wl}
def per_seed(ps):
    comp,shuf=ps["comp_texts"],ps["shuf_texts"]; frames=[]
    for i in range(min(len(comp),len(shuf))):
        a,b=MEASURED[i]; ch=concept_hits(comp[i]); sh=concept_hits(shuf[i])
        cb=b in ch; sb=b in sh
        frames.append({"frame":[a,b],"comp_hits":sorted(ch),"shuf_hits":sorted(sh),
                       "comp_has_B":cb,"shuf_has_B":sb,
                       "comp_has_A":a in ch,"shuf_has_A":a in sh,
                       "sensitive_B": cb and (not sb)})
    c=sum(1 for f in frames if f["sensitive_B"])
    return {"seed":ps["seed"],"frames":frames,"count":c,"majority":c>=4}
def run_arm(path):
    d=json.load(open(path)); out=[per_seed(ps) for ps in d["per_seed"]]
    sp=sum(1 for r in out if r["majority"])
    return {"arm":d["arm"],"ckpt":d.get("ckpt"),"per_seed":out,
            "seeds_majority":sp,"PASS":sp>=2}
if __name__=="__main__":
    print("="*72); print("Cluster A - A6 INTERVENTION (per-frame, $0 on existing outputs)")
    print("PREREG: sensitive[i]=comp_has_B AND NOT shuf_B; PASS=>=4/6 on >=2/3 seeds"); print("="*72)
    summary={}
    for arm in ["targeted","shuf","base"]:
        r=run_arm(os.path.join(RES,arm+".json"))
        summary[arm]={k:r[k] for k in ("arm","ckpt","seeds_majority","PASS")}
        print(f"\n### {arm.upper()}  ckpt={r['ckpt']}")
        for ps in r["per_seed"]:
            print(f"  seed {ps['seed']}: sensitive {ps['count']}/6  majority={ps['majority']}")
            for f in ps["frames"]:
                m="SENS" if f["sensitive_B"] else "    "
                print(f"    [{m}] frame({f['frame'][0]},{f['frame'][1]}) "
                      f"comp_B={int(f['comp_has_B'])} shuf_B={int(f['shuf_has_B'])} "
                      f"comp_hits={f['comp_hits']} shuf_hits={f['shuf_hits']}")
        print(f"  -> seeds_majority={r['seeds_majority']}/3  PASS_intervention={r['PASS']}")
    print("\n"+"="*72); print("VERDICT MATRIX")
    for a,s in summary.items():
        print(f"  {a:9s}: PASS_intervention={s['PASS']}  (seeds majority {s['seeds_majority']}/3)")
    print("="*72)
    json.dump(summary, open(os.path.join(HERE,"cluster_A_A6_intervention_result.json"),"w"), indent=2)
    print("wrote", os.path.join(HERE,"cluster_A_A6_intervention_result.json"))
