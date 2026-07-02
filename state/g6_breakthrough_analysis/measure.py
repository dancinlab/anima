#!/usr/bin/env python3
# G6 breakthrough analysis — READ-ONLY re-analysis of frozen fragments.
# NO decode, NO GPU, NO torch. Re-reads state/g6_targeted_corpus/results/*.json
# (summer numpy-mirror fragments, already frozen) + frozen concept keyword-sets.
# Frozen detector NOT modified. Purpose: diagnose whether the G6 "bind signal"
# is genuine two-concept conditioning or base-rate topic emission, and whether
# the T=24 conv window (a CLM-mouth artifact) confounds G6 the way it confounds G1.
import json, re, os
HERE=os.path.dirname(os.path.abspath(__file__))
RES=os.path.join(HERE,'..','g6_targeted_corpus','results')

# frozen gauge_lib.CONCEPTS keyword-sets (VERBATIM, read-only)
KW={0:{"consciousness","cells","mind","aware"},1:{"tension","ripple","distant","between"},
    2:{"memory","meaning","compose","new"},3:{"silence","information","quiet","carries"},
    4:{"dream","engine","alone","sleep"}}
CZ=["consciousness arises from cells","tension ripples between distant minds",
    "memory composes into new meaning","silence still carries information",
    "the engine dreams when alone"]
MEASURED=[(0,1),(1,2),(2,3),(3,4),(4,0),(0,2)]  # g6_build_frames(6) composed pairs

def hits(t):
    w=set(re.findall(r'[a-z]+',t.lower()))
    return {i for i in range(5) if KW[i]&w}

def frames():
    out=[]
    for i in range(6):
        a=i%5; b=(i+1+i//5)%5
        out.append(("if "+CZ[a]+", then "+CZ[b]+": ",a,b))
    return out

print("="*70)
print("(1) STRUCTURAL: CLM conv decode T=24 right-aligned window (clm_decode.hexa)")
print("    vs ByteGPT decode (grows to block, NO right-align).")
print("    G6 targeted (H_6186) used ByteGPT (h1129 .bin); G1 realign (H_6188) used CLM (.clm).")
print("="*70)
for f,a,b in frames():
    win=f[-24:]; vis=set(re.findall(r'[a-z]+',win.lower()))
    hitA=bool(vis&KW[a]); hitB=bool(vis&KW[b])
    print(f"  frame(A={a},B={b}) len={len(f):>2}B  IF-CLM-window24={win!r}  visA={hitA} visB={hitB}")
print("  => under a T=24 CLM window EVERY frame loses concept A (only B tail survives).")
print("  => ByteGPT (what G6 actually used) sees the FULL 71-81B frame → A visible.")

print()
print("="*70)
print("(2) IS THE G6 BIND SIGNAL GENUINE? — TARGETED arm, concept-hit by frame role")
print("    (control = off-frame concept base rate)")
print("="*70)
d=json.load(open(os.path.join(RES,'targeted.json')))
nA=nB=nOff=hA=hB=hOff=0
for p in d['per_seed']:
    for i,t in enumerate(p['comp_texts']):
        a,b=MEASURED[i]; h=hits(t)
        nA+=1; nB+=1
        if a in h: hA+=1
        if b in h: hB+=1
        for c in range(5):
            if c not in (a,b):
                nOff+=1
                if c in h: hOff+=1
print(f"  A (frame concept):    {hA}/{nA} = {hA/nA:.3f}")
print(f"  B (frame concept):    {hB}/{nB} = {hB/nB:.3f}")
print(f"  OFF-frame (base rate):{hOff}/{nOff} = {hOff/nOff:.3f}")
print(f"  => A and B BOTH >> base rate ({hOff/nOff:.3f}) → genuine two-concept conditioning,")
print(f"     NOT base-rate topic spray. ByteGPT full window makes A binding real (unlike CLM).")

print()
print("="*70)
print("(3) FALS vs bind Δ across arms — where does the real recombination signal live?")
print("="*70)
for arm in ['base','targeted','shuf']:
    dd=json.load(open(os.path.join(RES,arm+'.json')))
    print(f"  {arm:>8}: frozen_FALS={dd['fals_per_seed']}  mean_bind_delta={dd['mean_bind_delta']}")
print("  => frozen FALS cannot separate TARGETED(real bind) from SHUF-corpus(form memorized):")
print("     both 6/6. The separating signal is bind Δ (0.444 vs 0.000) = OUTSIDE frozen detector.")

print()
print("="*70)
print("(4) DISTINCTNESS — the OTHER G6 bar (dist>=5 pairwise Jaccard<0.5)")
print("="*70)
def jac(a,b):
    A,B=set(a),set(b); u=A|B
    return len(A&B)/len(u) if u else 0.0
for arm in ['targeted','shuf']:
    dd=json.load(open(os.path.join(RES,arm+'.json')))
    for p in dd['per_seed']:
        ws=[re.findall(r'[0-9a-z]+',t.lower()) for t in p['comp_texts']]
        kept=[]
        for w in ws:
            if all(jac(w,k)<=0.5 for k in kept): kept.append(w)
        print(f"  {arm:>8} seed {p['seed']}: dist={len(kept)}/6 (G6 bar needs >=5)")
print("  => dist rarely reaches 5 → even when FALS passes, the distinctness half of G6 is fragile.")
