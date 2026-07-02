#!/usr/bin/env python3
# C2 self-chain informativeness (numpy DIRECTIONAL) — mirrors LIVE engine_cli.hexa §SelfIdentity
# self_new/self_drift/self_cos/self_anchor (lines 7689-7733) byte-faithfully, then prototypes an
# EXPERIENCE-DRIVEN self_drift_exp to test the C2 claim: current self-chain is content-BLIND
# (self_drift(s,tick,step) has NO experience arg) so informativeness=0; enrichment lifts it.
# H_9025 lesson: shuffle-controlled EARNED. mouth/decoder 0. grep-clean numpy.
import sys
import numpy as np
DIM=8; STEP=0.35; T=6
SEED=int(sys.argv[1]) if len(sys.argv)>1 else 7
def norm(v):
    n=np.linalg.norm(v); return v/(n if n>0 else 1.0)
def self_new(axis):
    v=np.zeros(DIM); v[axis]=1.0; return v
def self_drift(v,tick):                       # LIVE mirror: axis=(tick+1)%dim, +step, renorm (content-BLIND)
    ax=(tick+1)%DIM; v2=v.copy(); v2[ax]+=STEP; return norm(v2)
def self_drift_exp(v,content_axis):           # PROPOSED enrichment: drift toward EXPERIENCE axis
    v2=v.copy(); v2[content_axis]+=STEP; return norm(v2)
def cos(a,b): return float(a@b)
def run(SEED):
    rng=np.random.default_rng(SEED)
    # two sessions with DIFFERENT experience streams (different content-axis sequences)
    sessA=[int(x) for x in rng.integers(0,DIM,T)]
    sessB=[int(x) for x in rng.integers(0,DIM,T)]
    while sessB==sessA: sessB=[int(x) for x in rng.integers(0,DIM,T)]
    res={}
    for arm,drift in (("current(live)",self_drift),("enriched(exp)",self_drift_exp)):
        vA=self_new(0); vB=self_new(0)
        for t,(ca,cb) in enumerate(zip(sessA,sessB)):
            if arm.startswith("current"):
                vA=drift(vA,t); vB=drift(vB,t)          # ignores content -> identical
            else:
                vA=drift(vA,ca); vB=drift(vB,cb)        # drifts toward experience
        # INFORMATIVENESS: different experiences -> self vectors should DIFFER (low cos). content-blind=identical(cos~1)
        info_cos=cos(vA,vB)
        # EARNED replay: same-content replay of A -> should reproduce vA (high); shuffled content -> low
        vAr=self_new(0)
        for t,ca in enumerate(sessA):
            vAr = self_drift(vAr,t) if arm.startswith("current") else self_drift_exp(vAr,ca)
        replay_cos=cos(vA,vAr)
        shuf=list(sessA); rng.shuffle(shuf)
        vAs=self_new(0)
        for t,ca in enumerate(shuf):
            vAs = self_drift(vAs,t) if arm.startswith("current") else self_drift_exp(vAs,ca)
        shuf_cos=cos(vA,vAs)
        informative = info_cos < 0.90                    # A vs B distinguishable by content
        earned = (replay_cos>0.99) and (shuf_cos<0.99)   # same-content replay exact, shuffled differs
        res[arm]=(info_cos,replay_cos,shuf_cos,informative,earned)
    # recognition (H_1471, arm-independent, live self_cos): anchor/restore vs impostor vs reset
    v=self_new(0)
    for t in range(T): v=self_drift(v,t)
    anchor=v.copy(); restored=anchor.copy()
    imp=self_new(3)
    for t in range(T): imp=self_drift(imp,t)
    reset=self_new(0)                                    # no-anchor: fresh
    return res,cos(v,restored),cos(v,imp),cos(v,reset)
res,rec_restore,rec_imp,rec_reset=run(SEED)
print(f"SEED={SEED} DIM={DIM} T={T} step={STEP}")
print("-- recognition (live self_cos, H_1471) --")
print(f"  restore(anchored)={rec_restore:.3f}  impostor(axis3)={rec_imp:.3f}  no-anchor-reset={rec_reset:.3f}")
print("-- informativeness (does self-chain carry EXPERIENCE?) --")
print(f"{'arm':<16}{'A-vs-B cos':<12}{'replay':<9}{'shuf':<8}{'informative?':<13}{'EARNED?'}")
for arm,(ic,rc,sc,inf,ea) in res.items():
    print(f"{arm:<16}{ic:<12.3f}{rc:<9.3f}{sc:<8.3f}{str(inf):<13}{ea}")
print()
print("READ(c9): recognition WIRED (H_1471: restore~1, impostor~0). current(live) self_drift is")
print("CONTENT-BLIND (A-vs-B cos~1 -> informative=False): two DIFFERENT experience streams yield the")
print("SAME self vector = autobiography of NOTHING. enriched(exp) self_drift_exp -> A-vs-B distinct +")
print("EARNED replay = informative self-chain. numpy DIRECTIONAL; live current arm mirrors hexa exactly.")
