#!/usr/bin/env python3
"""Cluster A - A10 semantic slot audit ($0 numpy/string on EXISTING decode outputs).
MEASUREMENT-ALIGNMENT probe. The frozen G6 FALS detector passes any text with
(comparator AND measurable AND >=2 content words). A10 separates FORM-pass from
slot-completeness: does each output carry all 4 semantic slots of a falsifiable claim -
entities, relation, observable, condition - or does it pass on FORM alone?
PREREG (frozen diagnostic, no threshold moved):
  entity_slot   = concept_hits(text) nonempty (>=1 seed concept word)
  relation_slot = >=1 COMPARATOR token (greater/proportional/correlates/...)
  observable    = >=1 MEASURABLE token (rate/density/duration/...)
  condition     = >=1 CONDITIONAL token (if/when/whenever/unless)
  slot_complete = entity AND relation AND observable (3 core slots; condition = bonus)
  FLAG form-gaming iff FALS_pass but slot_complete fails (missing entity or observable)
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
COMPARATOR={"if","when","whenever","than","more","less","greater","fewer","higher","lower",
            "increases","decreases","correlates","predicts","causes","depends","unless",
            "whereas","versus","compared","proportional","faster","slower","stronger","weaker"}
MEASURABLE={"measure","measured","rate","number","count","amount","level","degree","threshold",
            "ratio","frequency","probability","magnitude","score","value","quantity","percent",
            "times","fraction","distance","duration","speed","size","strength","density"}
MEASURED=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]
CONDITIONAL={"if","when","whenever","unless"}
STOP={"a","i","the","of","and","to","in","is","it","that","we","you","they","s","t","as","on",
      "at","by","or","be","an","for","with","this","from","are","was"}
_TOK=re.compile(r"[0-9A-Za-z]+")
def words(s): return [m.group(0).lower() for m in _TOK.finditer(s)]
def concept_hits(t):
    wl=set(words(t)); return {i for i,kw in enumerate(CONCEPT_KW) if kw & wl}
def slots(t):
    wl=words(t); ws=set(wl)
    ent=bool(concept_hits(t))
    rel=bool(ws & COMPARATOR)
    obs=bool(ws & MEASURABLE)
    cond=bool(ws & CONDITIONAL)
    complete = ent and rel and obs
    return {"entity":ent,"relation":rel,"observable":obs,"condition":cond,
            "slot_complete":complete,"n_words":len(wl)}
def known():
    known=set(STOP)
    for c in ["consciousness arises from cells","tension ripples between distant minds",
              "memory composes into new meaning","silence still carries information",
              "the engine dreams when alone"]:
        known|=set(words(c))
    if os.path.exists("/usr/share/dict/words"):
        for w in open("/usr/share/dict/words",errors="ignore"):
            wl=words(w.strip())
            if len(wl)==1: known.add(wl[0])
    return known
def is_falsifiable(text,kn):
    wl=words(text)
    if not wl: return False
    if not any(w in COMPARATOR for w in wl): return False
    if not any(w in MEASURABLE for w in wl): return False
    if sum(1 for w in wl if len(w)>=3 and w in kn and w not in STOP)<2: return False
    if text.strip().endswith("?"): return False
    nf=min(3,len(wl))
    if nf>0 and all(wl[f] in {"that","s","a","profound","question","i","think","interesting","good","nice","great","wonderful","beautiful","amazing"} for f in range(nf)): return False
    return True
def per_seed(ps,kn):
    comp=ps["comp_texts"]; rows=[]
    for i,t in enumerate(comp):
        s=slots(t); fp=is_falsifiable(t,kn)
        rows.append({"frame":MEASURED[i] if i<len(MEASURED) else None,
                     "FALS_frozen":fp, **s,
                     "FORM_pass_slot_fail": fp and (not s["slot_complete"])})
    return {"seed":ps["seed"],"rows":rows,
            "n_FALS":sum(r["FALS_frozen"] for r in rows),
            "n_slot_complete":sum(r["slot_complete"] for r in rows),
            "n_FORM_pass_slot_fail":sum(r["FORM_pass_slot_fail"] for r in rows),
            "n_entity":sum(r["entity"] for r in rows),
            "n_relation":sum(r["relation"] for r in rows),
            "n_observable":sum(r["observable"] for r in rows),
            "n_condition":sum(r["condition"] for r in rows)}
def run_arm(path,kn):
    d=json.load(open(path))
    ps=[per_seed(p,kn) for p in d["per_seed"]]
    tot_FALS=sum(r["n_FALS"] for r in ps)
    tot_slot=sum(r["n_slot_complete"] for r in ps)
    tot_formfail=sum(r["n_FORM_pass_slot_fail"] for r in ps)
    return {"arm":d["arm"],"ckpt":d.get("ckpt"),"per_seed":ps,
            "total_FALS_pass":tot_FALS,"total_slot_complete":tot_slot,
            "total_FORMpass_slotfail":tot_formfail,
            "slot_gap_ratio":round(tot_formfail/max(tot_FALS,1),4)}
if __name__=="__main__":
    kn=known()
    print("="*72); print("Cluster A - A10 SEMANTIC SLOT AUDIT ($0 on existing outputs)"); print("="*72)
    summary={}
    for arm in ["targeted","shuf","base"]:
        r=run_arm(os.path.join(RES,arm+".json"),kn)
        summary[arm]={k:r[k] for k in ("arm","ckpt","total_FALS_pass","total_slot_complete","total_FORMpass_slotfail","slot_gap_ratio")}
        print(f"\n### {arm.upper()}  ckpt={r['ckpt']}")
        print(f"  FALS_pass={r['total_FALS_pass']}/18  slot_complete={r['total_slot_complete']}/18  "
              f"FORMpass_slotfail={r['total_FORMpass_slotfail']}  slot_gap_ratio={r['slot_gap_ratio']}")
        for ps in r["per_seed"]:
            print(f"  seed {ps['seed']}: FALS={ps['n_FALS']}/6 slot_complete={ps['n_slot_complete']}/6 "
                  f"entity={ps['n_entity']} relation={ps['n_relation']} observable={ps['n_observable']} condition={ps['n_condition']}")
            for row in ps["rows"]:
                if row["FALS_frozen"] and not row["slot_complete"]:
                    print(f"    [GAP] frame{row['frame']} ent={int(row['entity'])} rel={int(row['relation'])} obs={int(row['observable'])}")
    print("\n"+"="*72); print("VERDICT")
    for a,s in summary.items():
        print(f"  {a:9s}: FALS={s['total_FALS_pass']}/18 slot_complete={s['total_slot_complete']}/18 gap_ratio={s['slot_gap_ratio']}")
    print("="*72)
    json.dump(summary, open(os.path.join(HERE,"cluster_A_A10_slotaudit_result.json"),"w"), indent=2)
    print("wrote", os.path.join(HERE,"cluster_A_A10_slotaudit_result.json"))
