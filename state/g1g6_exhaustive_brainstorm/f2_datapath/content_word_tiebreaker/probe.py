#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F2 content_word_tiebreaker — $0 decisive arm.
Question: the powered E1-gate cells (n>=10) are all on freq-top-400 vocab, which is
dominated by FUNCTION WORDS / markup / speaker-labels (=> syntactic/template order, not
concept-compositional binding). Does the powered signal SURVIVE a principled content-word
filter? Filter is FREQUENCY-DERIVED (drop the top-K most frequent tokens as stopwords) +
a wordlike shape test (letters/Hangul, len>=2, no markup) — NOT hand-picked, NOT tune-to-green.
If the highest-yield corpora collapse to n<10 on content words => concept-level F2 starved.

Gate metric reference-matched to crosscorpus_yield/probe.py (the E1 mechanism):
 whitespace tokens; ordered adjacent in-vocab pair (a,b) a!=b; follower=t_{i+2};
 unordered {a,b} QUALIFIED iff both orders >= MIN_OCC(3);
 differ_frac = frac qualified where top-follower(a,b)!=top-follower(b,a);
 NON-DEGENERATE-POWERED iff differ_frac>=2/3 AND n_qualified>=10.
"""
import json, re, os
from collections import Counter, defaultdict

MIN_OCC=3; TOP_VOCAB=400; POWER=10; FRAC_BAR=2.0/3.0
DROP_TOP=50          # frequency-derived stoplist: drop the 50 most frequent tokens (function words)
OUTDIR="/Users/mini/dancinlab/anima/state/g1g6_exhaustive_brainstorm/f2_datapath/content_word_tiebreaker"
CORPORA={
 "consciousness_anchor":"/Users/mini/dancinlab/anima/archive/state_legacy/anima_phase1a1_color_cosmology_2026_05_12/consciousness_anchor.txt",
 "corpus":"/Users/mini/dancinlab/anima/archive/data/corpus.txt",
 "ko_wiki":"/Users/mini/dancinlab/anima/archive/data/.corpus_cache/.corpus_cache/ko_wiki.txt",
}
# wordlike = has >=2 letter/Hangul chars, not pure markup/punct, not a speaker-label like "사용자:"
LETTER=re.compile(r"[A-Za-z가-힣一-鿿]")
def wordlike(tok):
    if len(tok)<2: return False
    if tok.endswith(":"): return False            # speaker labels (사용자:, 도우미:)
    letters=LETTER.findall(tok)
    if len(letters)<2: return False
    # reject if majority chars are markup/punct/digits (e.g. \displaystyle-frag, ==, ---, {, })
    nonletter=sum(1 for c in tok if not LETTER.match(c))
    if nonletter>len(letters): return False
    if tok.startswith("\\"): return False          # LaTeX fragment
    return True

def tokenize(p):
    t=[]
    with open(p,"r",encoding="utf-8",errors="replace") as f:
        for line in f: t.extend(line.split())
    return t

def gate(toks, vocab):
    pair_follow=defaultdict(Counter); pair_count=Counter(); n=len(toks)
    for i in range(n-1):
        a,b=toks[i],toks[i+1]
        if a in vocab and b in vocab and a!=b:
            pair_count[(a,b)]+=1
            if i+2<n: pair_follow[(a,b)][toks[i+2]]+=1
    seen=set(); n_qual=0; n_differ=0; ex=[]
    for (a,b) in list(pair_count.keys()):
        key=tuple(sorted((a,b)))
        if key in seen: continue
        c_ab=pair_count[(a,b)]; c_ba=pair_count[(b,a)]
        if c_ab>=MIN_OCC and c_ba>=MIN_OCC:
            seen.add(key); n_qual+=1
            tf_ab=pair_follow[(a,b)].most_common(1); tf_ba=pair_follow[(b,a)].most_common(1)
            f_ab=tf_ab[0][0] if tf_ab else None; f_ba=tf_ba[0][0] if tf_ba else None
            d=(f_ab!=f_ba)
            if d: n_differ+=1
            if len(ex)<15: ex.append({"pair":key,"c_ab":c_ab,"c_ba":c_ba,"f_ab":f_ab,"f_ba":f_ba,"differ":d})
    frac=(n_differ/n_qual) if n_qual else 0.0
    if n_qual>=POWER and frac>=FRAC_BAR: v="NON-DEGENERATE-POWERED"
    elif n_qual>=POWER: v="DEGENERATE-POWERED"
    else: v="INCONCLUSIVE-SPARSE"
    return {"n_qualified":n_qual,"n_differ":n_differ,"differ_frac":round(frac,4),"verdict":v,"examples":ex}

def analyze(name,p):
    toks=tokenize(p); freq=Counter(toks)
    # ARM_freq: raw E1 baseline = top-400 by frequency (reproduces crosscorpus_yield)
    v_freq=set(w for w,_ in freq.most_common(TOP_VOCAB))
    # ARM_content: frequency-derived stoplist (drop top-DROP_TOP) + wordlike, then top-400 of the remainder
    ranked=[w for w,_ in freq.most_common()]
    stop=set(ranked[:DROP_TOP])
    content_ranked=[w for w in ranked if w not in stop and wordlike(w)]
    v_content=set(content_ranked[:TOP_VOCAB])
    r_freq=gate(toks,v_freq); r_content=gate(toks,v_content)
    return {"n_tokens":len(toks),
            "ARM_freq_top400":{"vocab_size":len(v_freq),**r_freq},
            "ARM_content_word":{"vocab_size":len(v_content),
                                "sample_vocab":content_ranked[:25],**r_content}}

def main():
    out={"MIN_OCC":MIN_OCC,"TOP_VOCAB":TOP_VOCAB,"POWER":POWER,"FRAC_BAR":FRAC_BAR,
         "DROP_TOP":DROP_TOP,"note":"ARM_content = frequency-derived stoplist + wordlike shape; not hand-picked",
         "corpora":{}}
    for name,path in CORPORA.items():
        try: out["corpora"][name]=analyze(name,path)
        except Exception as e: out["corpora"][name]={"error":str(e)}
        r=out["corpora"][name]
        if "error" in r: print(f"{name}: ERROR {r['error']}"); continue
        f=r["ARM_freq_top400"]; c=r["ARM_content_word"]
        print(f"{name:22s} tok={r['n_tokens']:>9,} | FREQ n={f['n_qualified']:>4} frac={f['differ_frac']:.3f} {f['verdict']:24s} "
              f"| CONTENT n={c['n_qualified']:>4} frac={c['differ_frac']:.3f} {c['verdict']}")
    powered_content=[n for n,r in out["corpora"].items()
                     if "error" not in r and r["ARM_content_word"]["verdict"]=="NON-DEGENERATE-POWERED"]
    out["conclusion"]={
        "content_word_powered_corpora":powered_content,
        "verdict":("CONTENT-PATH-FOUND" if powered_content else "CONTENT-LEVEL-STARVED")}
    print("\nCONCLUSION:",json.dumps(out["conclusion"],ensure_ascii=False))
    os.makedirs(OUTDIR,exist_ok=True)
    with open(OUTDIR+"/RESULT.json","w") as fp: json.dump(out,fp,ensure_ascii=False,indent=2)
if __name__=="__main__": main()
