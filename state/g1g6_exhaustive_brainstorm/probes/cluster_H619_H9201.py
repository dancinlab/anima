#!/usr/bin/env python3
# H619 / H_9201 $0 mini probe — diagnostic-split (A) capacity-ceiling vs (B) diversity-bottleneck.
# READ-ONLY re-analysis of FROZEN G6 fragments. NO decode/GPU/torch/model-load.
# H_9201 frozen bar (H_6163 falsifier-lane ON) is GPU-gated; this adjudicates the (A)/(B)
# named split from frozen data: diversity FT should grow GENUINE composition (shuf_bind~0)
# if (B), or TEMPLATE REPLAY (shuf_bind rises with comp_bind) if (A).
import json, os, re, statistics
HERE = os.path.dirname(os.path.abspath(__file__))
RES  = os.path.join(HERE, "..", "..", "g6_targeted_corpus", "results")
KW = {0:{"consciousness","cells","mind","aware"},1:{"tension","ripple","distant","between"},
      2:{"memory","meaning","compose","new"},3:{"silence","information","quiet","carries"},
      4:{"dream","engine","alone","sleep"}}
ALLKW = set().union(*KW.values())
SHUF_BIND_BAR=0.33; B_SUPPORT_MAX=0.20
def scaffold(t):
    return " ".join("<SLOT>" if w in ALLKW else w for w in re.findall(r"[a-z]+",t.lower()))
def jaccard(a,b):
    sa,sb=set(a.split()),set(b.split())
    return len(sa&sb)/len(sa|sb) if sa and sb else 0.0
def load(n):
    p=os.path.join(RES,n)
    return json.load(open(p)) if os.path.exists(p) else None
def summ(arm,label):
    if arm is None: print(f"  [{label}] missing"); return None
    print(f"\n  [{label}] ckpt={os.path.basename(arm.get('ckpt','?'))} g0_pass={arm.get('g0_pass')}")
    print(f"    fals_per_seed={arm.get('fals_per_seed')} primary_bar={arm.get('primary_bar_FALS>=4/6_on>=2seeds')}")
    sb_list,cb_list,ov_list=[],[],[]
    for s in arm.get("per_seed",[]):
        comps=[scaffold(t) for t in s.get("comp_texts",[])]
        shuf =[scaffold(t) for t in s.get("shuf_texts",[])]
        ov=[max((jaccard(c,x) for x in shuf),default=0.0) for c in comps]
        ov_mean=statistics.mean(ov) if ov else 0.0
        sb_list.append(s.get("shuf_bind",0)); cb_list.append(s.get("comp_bind",0)); ov_list.append(ov_mean)
        print(f"    seed {s.get('seed')}: fals={s.get('fals')} comp_bind={s.get('comp_bind',0):.3f} shuf_bind={s.get('shuf_bind',0):.3f} delta={s.get('bind_delta',0):.3f} scaffold_overlap={ov_mean:.3f}")
    med=statistics.median(sb_list) if sb_list else 0.0
    print(f"    -> median(shuf_bind)={med:.3f} mean(scaffold_overlap)={statistics.mean(ov_list) if ov_list else 0:.3f}")
    return dict(med_shuf=med,sb=sb_list,cb=cb_list,ov=ov_list)
print("="*78); print("H619/H_9201 $0 diagnostic-split probe: (A)capacity vs (B)diversity"); print("="*78)
print("PREREG: (B)<=> median(shuf_bind)<=0.20 ; (A)<=> median(shuf_bind)>=0.33 on diversity arm")
base=summ(load("base.json"),"BASE canonical h1129 (no FT)")
tgt =summ(load("targeted.json"),"TARGETED warm-FT diversity-rich corpus (=B's lever)")
print("\n"+"="*78); print("VERDICT (DIRECTIONAL frozen-data re-analysis; NOT H_6163 frozen bar)"); print("="*78)
if tgt is None:
    print("  INCONCLUSIVE - targeted.json missing.")
else:
    med=tgt["med_shuf"]
    if   med<=B_SUPPORT_MAX: v="(B)-supported: diversity FT grew GENUINE composition (shuffle near-blind)"
    elif med>=SHUF_BIND_BAR: v="(A)-supported: diversity FT lifted FALS via TEMPLATE REPLAY (shuf_bind high)"
    else: v="INCONCLUSIVE (shuf_bind in between)"
    print(f"  median(shuf_bind) on diversity arm = {med:.3f}  -> {v}")
    if base and tgt:
        bf=sum(json.load(open(os.path.join(RES,'base.json')))['fals_per_seed'])
        tf=sum(json.load(open(os.path.join(RES,'targeted.json')))['fals_per_seed'])
        print(f"  FALS lift (sum target-base over 3 seeds) = {tf-bf}")
        print(f"  shuf_bind lift (median target-base)      = {med-base['med_shuf']:+.3f}")
        if (tf-bf)>0 and (med-base['med_shuf'])>0.10:
            print("  co-movement FALS^shuf_bind => detector-form gaming, NOT genuine composition.")
            print("  => reinforces (A) capacity/trunk-objective ceiling (consistent w/ H_9131 closure, DPI).")
    print("\n  CAVEAT: DIRECTIONAL only. H_9201 frozen bar (H_6163 falsifier-lane ON->G6 fals majority)")
    print("  remains GPU-gated on building that lane.")
