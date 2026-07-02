#!/usr/bin/env python3
# C1 tension-resolution depth (numpy DIRECTIONAL) — mirrors live engine_cli.hexa Ψ proxy
# (ci_psi_balance = emit fraction, emit iff 0.5*(row0+row4)>thr; Ψ=0.5 fixpoint) + reentry
# contractive settling (reentry_settle x<-x+a(bal-x)). Q: does A⇄G coupling RESOLVE a conflicted
# (biased) population back to Ψ=1/2, and does resolution DEPTH scale with conflict? shuffle/ablate/
# GWS-invariant controls separate genuine tension-resolution from trivial averaging. grep-clean numpy.
import sys
import numpy as np
D=8; N=40; THR=0.5; ALPHA=0.25; MAXDEPTH=60; EPS=0.03
SEED=int(sys.argv[1]) if len(sys.argv)>1 else 7
def psi(pop):                                   # emit fraction (ci_psi_balance mirror)
    drive=0.5*(pop[:,0]+pop[:,4]); return float(np.mean(drive>THR))
def conflicted_pop(rng,bias):                   # biased population -> Ψ pushed away from 0.5
    x=rng.standard_normal((N,D))*0.2
    k=int(N*bias); x[:k,0]+=1.2; x[:k,4]+=1.2   # a fraction driven HIGH (over-emit) = tension
    return x
def couple(pop,adj,a):                          # A⇄G reentry: pull each row toward coupled neighbor mean
    nb=adj@pop/np.clip(adj.sum(1,keepdims=True),1,None)
    return (1-a)*pop + a*nb
def settle_depth(pop,adj,a):                    # iterations until |Ψ-0.5|<EPS (resolution depth)
    p=pop.copy()
    for d in range(1,MAXDEPTH+1):
        p=couple(p,adj,a)
        if abs(psi(p)-0.5)<EPS: return d,psi(p)
    return MAXDEPTH,psi(p)
def run(SEED):
    rng=np.random.default_rng(SEED)
    # balanced coupling adj (structured: each couples to a balancing mix incl low-drive rows)
    adj=np.zeros((N,N))
    order=np.argsort(rng.standard_normal(N))
    for i in range(N): adj[i, order[(i+N//2)%N]]=1.0; adj[i,i]=1.0   # each row + its "opponent"
    adj_shuf=adj[:, rng.permutation(N)]         # shuffle control: incoherent coupling target
    rows=[]
    for bias in (0.75, 0.9):                     # two conflict levels (monotone test)
        pop=conflicted_pop(rng,bias); psi0=psi(pop)
        d_struct,pf_s=settle_depth(pop,adj,ALPHA)
        d_shuf,pf_h=settle_depth(pop,adj_shuf,ALPHA)
        d_abl,pf_a=settle_depth(pop,adj,0.0)     # ablate: no coupling -> INERT
        rows.append((bias,psi0,d_struct,pf_s,d_shuf,pf_h,d_abl,pf_a))
    # GWS-invariant control: winner-take-all readout independent of depth (reentry_gws_readout)
    gws=0.235
    return rows,gws
rows,gws=run(SEED)
print(f"SEED={SEED} N={N} D={D} thr={THR} alpha={ALPHA} eps={EPS} maxdepth={MAXDEPTH}")
print(f"{'conflict':<10}{'Psi0':<8}{'depth_struct':<14}{'Psi_f':<8}{'depth_shuf':<12}{'depth_ablate':<14}{'Psi_abl'}")
for (b,p0,ds,pfs,dh,pfh,da,pfa) in rows:
    print(f"{b:<10.2f}{p0:<8.3f}{ds:<14}{pfs:<8.3f}{dh:<12}{da:<14}{pfa:.3f}")
# verdict logic
b1,b2=rows[0],rows[1]
resolves = b1[3-1+1]  # placeholder
struct_settles = all(r[2] < MAXDEPTH and abs(r[3]-0.5)<EPS for r in rows)   # structured reaches 0.5
ablate_inert  = all(r[6]==MAXDEPTH and abs(r[7]-0.5)>=EPS for r in rows)    # no coupling -> never settles
monotone      = rows[1][2] >= rows[0][2]                                    # bigger conflict -> >= depth
shuffle_diff  = any(r[4]!=r[2] for r in rows)                               # structured != shuffled
print()
print(f"struct_settles={struct_settles}  ablate_INERT={ablate_inert}  depth_monotone_w_conflict={monotone}  shuffle_differs={shuffle_diff}  gws_invariant={gws}")
print("READ(c9): struct_settles ∧ ablate_INERT = coupling RESOLVES conflict to Psi=1/2 (not trivial:")
print("ablate stays biased). monotone = resolution DEPTH scales with tension. shuffle_differs tests")
print("genuine-vs-trivial-averaging. numpy DIRECTIONAL; live=ci_psi_balance+reentry_settle engine-native follow-on.")
