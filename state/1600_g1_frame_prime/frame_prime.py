#!/usr/bin/env python3
"""L2 — frame-prime: does decode FRAMING surface latent 2-concept composition?

The frozen G1 bar (g1_multiseed.py) primes the model with bare concatenated concept
sentences:  seedp = ". ".join(concepts[:k]) + ". "  and asks the model to continue.
H_1598 showed L8 fails this 0/3 just like L4.

QUESTION: is the failure a DECODE-FRAMING artifact? If we present the SAME two seed
concepts in a composition-inviting frame (few-shot "A and B together…", explicit
"combine", a worked example), does best_composed rise above max_single? If YES for some
frame -> the capability exists and the lever is inference-framing (NO retrain needed).
If NO across all frames -> the learned representation genuinely lacks composition.

FROZEN SCORING (UNCHANGED from g1_multiseed.py):
  coverage() over the same 5 CONCEPTS keyword-sets; a frame "composes" iff the continuation
  has >=2 DISTINCT concept families AND distinct > max_single AND coherent (kwr>=0.50).
  max_single is computed EXACTLY as the frozen harness (per-concept singles, gen=80).
  Only the SEED STRING fed to the decoder varies across frames; the bar is byte-identical.

This is engine-native (py 2-production clm_decode.py, numpy, torch-free => TERMINAL).
"""
from __future__ import annotations
import sys, os, re, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("core", os.path.join("..","..","core"), os.path.join(HERE,"..","..","core")):
    ap = os.path.abspath(p)
    if os.path.isdir(ap) and ap not in sys.path:
        sys.path.insert(0, ap)

# ── frozen metric (VERBATIM from g1_multiseed.py) ─────────────────────────────────────
CONCEPTS = [
    ("consciousness arises from cells",       {"consciousness","cells","mind","aware"}),
    ("tension ripples between distant minds",  {"tension","ripple","distant","between"}),
    ("memory composes into new meaning",       {"memory","meaning","compose","new"}),
    ("silence still carries information",       {"silence","information","quiet","carries"}),
    ("the engine dreams when alone",           {"dream","engine","alone","sleep"}),
]
def words(s): return re.findall(r"[0-9A-Za-z가-힣]+", s.lower())
KNOWN = set()
for _c,_kw in CONCEPTS:
    KNOWN |= {w for w in words(_c)}; KNOWN |= _kw
for _p in ("/usr/share/dict/words","/usr/share/dict/american-english"):
    try:
        with open(_p,errors="ignore") as f:
            for w in f:
                w=w.strip().lower()
                if w.isalpha(): KNOWN.add(w)
        break
    except OSError: continue
KNOWN |= {"a","i","the","of","and","to","in","is","it","that","we","you","they","s","t"}
def kwr(text):
    wl=words(text); return sum(1 for w in wl if w in KNOWN)/len(wl) if wl else 0.0
def coverage(text):
    wl=set(words(text)); return [i for i,(_,kw) in enumerate(CONCEPTS) if wl & kw]
STOPS=["\n사용자:"," | 사용자:","사용자:","\n\n"]
def _trim(t):
    for st in STOPS:
        i=t.find(st); t=t[:i] if i>=0 else t
    return t.strip()

# ── frame variants: only the SEED STRING changes. scoring identical. ──────────────────
# Each frame takes the FIRST k concept sentences and arranges them differently.
def frame_bare(cs):          # frozen baseline (== g1_multiseed seedp)
    return ". ".join(cs)+". "
def frame_and_together(cs):  # "A and B together: "
    return " and ".join(cs)+", together: "
def frame_combine(cs):       # explicit instruction-ish (still substrate prose, no system prompt)
    return "Combining these ideas — "+"; ".join(cs)+" — yields: "
def frame_fewshot(cs):       # one worked composition example then the target pair
    ex = ("memory composes into new meaning and silence still carries information, "
          "so a quiet memory becomes meaningful information. ")
    return ex + " and ".join(cs) + ", so "
def frame_relation(cs):      # relational connective inviting binding
    return "The "+cs[0]+" relates to how "+(cs[1] if len(cs)>1 else cs[0])+", because "
def frame_essay(cs):         # short essay opener that names both concepts
    return "Both "+(" and ".join(cs))+". In other words, "

FRAMES = {
    "bare(frozen)": frame_bare,
    "and_together": frame_and_together,
    "combine": frame_combine,
    "fewshot": frame_fewshot,
    "relation": frame_relation,
    "essay": frame_essay,
}

SEEDS=[7,4302,4303]

def run(genfn, label):
    print("="*80)
    print(f"L2 FRAME-PRIME  engine={label}")
    print(f"date {time.strftime('%Y-%m-%d %H:%M:%S')} host {os.uname().nodename} seeds={SEEDS}")
    print("FROZEN bar: a frame COMPOSES iff continuation distinct>=2 AND >max_single AND coherent")
    print("="*80)
    results={}
    for sd in SEEDS:
        # max_single: frozen, per-concept singles gen=80 (same as g1_multiseed.ladder_seed)
        sdist=[]
        for i,(c,_) in enumerate(CONCEPTS):
            o=genfn(f"{c}. ",80,sd+i); sdist.append(len(coverage(o)))
        ms=max(sdist) if sdist else 0
        print(f"\n[seed {sd}] max_single={ms}")
        for fname,ffn in FRAMES.items():
            best_for_frame=0; best_txt=""
            for k in (2,3,4,5):
                cs=[c for c,_ in CONCEPTS[:k]]
                seedp=ffn(cs)
                o=genfn(seedp,120,sd)
                cc=coverage(o); kk=kwr(o); coh=kk>=0.50
                composes=(len(cc)>=2 and len(cc)>ms and coh)
                if len(cc)>best_for_frame:
                    best_for_frame=len(cc); best_txt=o[:120]
                tag="COMPOSES" if composes else ""
                print(f"  {fname:14s} k={k} distinct={len(cc)} cov={cc} kwr={kk:.2f} coh={coh} {tag}")
                results.setdefault(fname,{}).setdefault(sd,[]).append(
                    {"k":k,"distinct":len(cc),"cov":cc,"kwr":round(kk,3),"coherent":coh,
                     "composes":composes,"max_single":ms,"text":o[:120]})
            print(f"     -> best_composed[{fname}] (seed {sd}) = {best_for_frame}  {best_txt!r}")
    # verdict: any frame with composes==True on >=2/3 seeds = capability surfaced
    print("\n"+"="*80)
    frame_green={}
    for fname in FRAMES:
        ng=0
        for sd in SEEDS:
            if any(e["composes"] for e in results[fname][sd]): ng+=1
        frame_green[fname]=ng
        v="SURFACES(>=2/3)" if ng>=2 else ("partial(1/3)" if ng==1 else "no")
        print(f"  frame {fname:14s}: composes on {ng}/3 seeds -> {v}")
    any_green=any(v>=2 for v in frame_green.values())
    verdict=("CAPABILITY-LATENT (framing lever)" if any_green
             else "NO FRAME SURFACES COMPOSITION (representation lacks it)")
    print(f"\nVERDICT: {verdict}")
    print("="*80)
    out={"verdict":verdict,"frame_green_seeds":frame_green,"label":label,"detail":results}
    with open(os.path.join(HERE,"result.json"),"w") as f:
        json.dump(out,f,indent=2,default=str)
    print(f"wrote {os.path.join(HERE,'result.json')}")

def main():
    clmp=sys.argv[1]
    import clm_decode as C
    W=C.clm_load_weights(clmp)
    def gen(seed,mx,seed_rng):
        return _trim(C.clm_decode_topk_sampled_W(W,seed,mx,40,0.7,seed_rng)["text"])
    run(gen,f"clm_decode {os.path.basename(clmp)}")

if __name__=="__main__":
    main()
