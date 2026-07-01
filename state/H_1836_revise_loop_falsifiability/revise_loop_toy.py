#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# H_1836 — g6-lens F1: depth-in-time generate->verify->revise recurrence.
# Mechanism TOY (synthetic claim generator; NOT a real LM). numpy-only, $0, mini-safe, DIRECTIONAL.
#
# Question: does feedback-conditioned revision (time-recurrence) lift the falsifiable-fraction
#           above the single-pass floor, AND beat targeting/resample controls?
#
# The FROZEN falsifiability judge below is a VERBATIM port of core/g6_ideation.hexa
# `_g6_is_falsifiable` (comparator ^ measurable ^ >=2 content ^ not-question ^ not-stance-prefix).
# NO loosening (p7/c9). The judge is applied to the generated claim STRINGS.
#
# 4 arms (R/R_shuffle/R_noloop share EQUAL decode budget = 1 draft + T=3 = 4 passes;
#          A is the single-pass floor at 1 pass):
#   A         = single-pass (1 draft).                      -> floor
#   R         = revise-loop T=3: judge reports which predicate slot is deficient; regenerate
#               ONLY the deficient slot(s). Goodhart-avoid: we do NOT inject the judge's answer;
#               the generator re-samples the slot from its own imperfect vocab (success prob q),
#               and we only ever TOUCH slots the judge marks deficient (targeted, monotone).
#   R_shuffle = same loop/budget but regenerate a RANDOM slot each step (binding control:
#               feedback must be TARGETED; re-rolling a good slot can break it).
#   R_noloop  = same budget spent as (1+T)=4 INDEPENDENT full drafts, falsifiable if ANY passes
#               (best-of-N: feedback vs just-more-samples control).

import numpy as np
import sys, json

# --------------------------- FROZEN JUDGE (VERBATIM port) ---------------------------
COMPARATOR = {"if","when","whenever","than","more","less","greater","fewer","higher","lower",
    "increases","decreases","correlates","predicts","causes","depends","unless","whereas",
    "versus","compared","proportional","faster","slower","stronger","weaker"}
MEASURABLE = {"measure","measured","rate","number","count","amount","level","degree","threshold",
    "ratio","frequency","probability","magnitude","score","value","quantity","percent","times",
    "fraction","distance","duration","speed","size","strength","density"}
STANCE = {"that","s","a","profound","question","i","think","interesting","good","nice","great",
    "wonderful","beautiful","amazing"}
STOP = {"a","i","the","of","and","to","in","is","it","that","we","you","they","s","t","as","on",
    "at","by","or","be","an","for","with","this","from","are","was"}
CONCEPTS = ["consciousness arises from cells","tension ripples between distant minds",
    "memory composes into new meaning","silence still carries information",
    "the engine dreams when alone"]

def _words(s):
    out=[]; cur=[]
    for ch in s:
        o=ord(ch)
        if (48<=o<=57) or (65<=o<=90) or (97<=o<=122): cur.append(chr(o+32) if 65<=o<=90 else ch)
        else:
            if cur: out.append("".join(cur)); cur=[]
    if cur: out.append("".join(cur))
    return out

def _build_known():
    known=set(STOP)
    for c in CONCEPTS:
        for w in _words(c): known.add(w)
    try:
        with open("/usr/share/dict/words") as f:
            for line in f:
                wl=_words(line.strip())
                if len(wl)==1: known.add(wl[0])
    except OSError:
        pass
    return known

KNOWN=_build_known()

def is_falsifiable(text, known=KNOWN):
    wl=_words(text); n=len(wl)
    if n==0: return False
    a=b=False
    for w in wl:
        if w in COMPARATOR: a=True
        if w in MEASURABLE: b=True
    if not a or not b: return False
    content=sum(1 for w in wl if len(w)>=3 and w in known and w not in STOP)
    if content<2: return False
    tr=text.strip()
    if tr and tr[-1]=='?': return False
    nf=min(3,n)
    if nf>0 and all(wl[k] in STANCE for k in range(nf)): return False
    return True

# --------------------------- MECHANISM GENERATOR ---------------------------
Q = 0.5   # un-tuned: coin-flip slot success. pre-registered, NOT chosen to hit the bar.
NPOS = 3  # comparator, measurable, content
T = 3     # recurrence depth / budget
N = 500   # claims per arm per seed

COMP_OK   = sorted(COMPARATOR); COMP_BAD  = ["around","near","beside","among","toward"]
MEAS_OK   = sorted(MEASURABLE); MEAS_BAD  = ["thing","aspect","notion","essence","spirit"]
CONT_OK   = ["cells","tension","memory","silence","engine","meaning","information","minds"]
CONT_BAD  = ["a","i","of"]

def sample_slot(cat, rng):
    ok = rng.random() < Q
    if cat==0:
        return (rng.choice(COMP_OK) if ok else rng.choice(COMP_BAD)), ok
    if cat==1:
        return (rng.choice(MEAS_OK) if ok else rng.choice(MEAS_BAD)), ok
    if ok:
        w=rng.choice(CONT_OK, size=2, replace=False); return (w[0]+" "+w[1]), True
    else:
        return rng.choice(CONT_BAD), False

def materialize(slotwords):
    return ("the " + slotwords[2] + " " + slotwords[0] + " the " + slotwords[1]).strip()

def draft(rng):
    words=[None,None,None]; ok=[False,False,False]
    for c in range(NPOS):
        w,s=sample_slot(c,rng); words[c]=w; ok[c]=s
    return words, ok

def judge_deficits(slotwords):
    wl=_words(materialize(slotwords)); wset=set(wl)
    d=[]
    if not (wset & COMPARATOR): d.append(0)
    if not (wset & MEASURABLE): d.append(1)
    content=sum(1 for w in wl if len(w)>=3 and w in KNOWN and w not in STOP)
    if content<2: d.append(2)
    return d

def arm_A(rng):
    words,_=draft(rng)
    return is_falsifiable(materialize(words))

def arm_R(rng):
    words,_=draft(rng)
    for _ in range(T):
        d=judge_deficits(words)
        if not d: break
        for c in d:
            w,_=sample_slot(c,rng); words[c]=w
    return is_falsifiable(materialize(words))

def arm_Rshuffle(rng):
    words,_=draft(rng)
    for _ in range(T):
        d=judge_deficits(words)
        if not d: break
        c=int(rng.integers(0,NPOS))
        w,_=sample_slot(c,rng); words[c]=w
    return is_falsifiable(materialize(words))

def arm_Rnoloop(rng):
    passed=False
    for _ in range(1+T):
        words,_=draft(rng)
        if is_falsifiable(materialize(words)): passed=True
    return passed

def frac(arm_fn, seed):
    rng=np.random.default_rng(seed)
    return sum(arm_fn(rng) for _ in range(N))/N

def main():
    seeds=[7,4302,4303]
    arms={"A":arm_A,"R":arm_R,"R_shuffle":arm_Rshuffle,"R_noloop":arm_Rnoloop}
    table={}
    for s in seeds:
        row={name:frac(fn,s) for name,fn in arms.items()}
        table[s]=row
    BAR=0.34
    passes={"i_vs_A":0,"ii_vs_shuffle":0,"iii_vs_noloop":0}
    per_seed=[]
    for s in seeds:
        r=table[s]
        di=r["R"]-r["A"]; dii=r["R"]-r["R_shuffle"]; diii=r["R"]-r["R_noloop"]
        pi=di>=BAR; pii=dii>=BAR; piii=diii>=BAR
        passes["i_vs_A"]+=pi; passes["ii_vs_shuffle"]+=pii; passes["iii_vs_noloop"]+=piii
        per_seed.append({"seed":s,"A":r["A"],"R":r["R"],"R_shuffle":r["R_shuffle"],
                         "R_noloop":r["R_noloop"],"d_i":di,"d_ii":dii,"d_iii":diii,
                         "pass_i":bool(pi),"pass_ii":bool(pii),"pass_iii":bool(piii)})
    green = passes["i_vs_A"]>=2 and passes["ii_vs_shuffle"]>=2 and passes["iii_vs_noloop"]>=2
    out={"H":"H_1836","substrate":"mechanism-toy (numpy synthetic generator, NOT a real LM)",
         "Q":Q,"N":N,"T":T,"NPOS":NPOS,"seeds":seeds,"bar":BAR,
         "per_seed":per_seed,"pass_counts":passes,
         "verdict":"GREEN-DIRECTIONAL" if green else "WALL-DIRECTIONAL",
         "green":bool(green)}
    print(json.dumps(out,indent=2))
    print("\n=== falsifiable-fraction (4 arm x 3 seed) ===", file=sys.stderr)
    print(f"{'seed':>6} {'A':>7} {'R':>7} {'R_shuf':>7} {'R_nolp':>7} | {'d_i':>6} {'d_ii':>6} {'d_iii':>6}", file=sys.stderr)
    for ps in per_seed:
        print(f"{ps['seed']:>6} {ps['A']:>7.3f} {ps['R']:>7.3f} {ps['R_shuffle']:>7.3f} {ps['R_noloop']:>7.3f} | "
              f"{ps['d_i']:>6.3f} {ps['d_ii']:>6.3f} {ps['d_iii']:>6.3f}", file=sys.stderr)
    print(f"pass counts (>= {BAR}): {passes}  -> GREEN={green}", file=sys.stderr)

if __name__=="__main__":
    main()
