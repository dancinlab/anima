#!/usr/bin/env python3
"""structure-aware REAL-MODEL probe (H_6167 bridge → real anima trunk, 2026-07-02).
Q: does the real 303M clm trunk's penultimate features carry RECOMBINABLE concept structure,
or are the concept features the bottleneck? (= is real-text G1=0 a feature/substrate wall or a
metric/generation artifact?) Two tests on py303_full.clm penultimate (yn, pre-readout):
 (1) concept-identity recoverability: held-out context of a concept → recover which concept (linear probe).
 (2) structured recombination (H_6167 factored target y=T2[a%K,b%K]) on REAL features vs RANDOM control.
torch-free numpy; py mirror = DIRECTIONAL. FROZEN. tune-to-green forbidden (p7)."""
import sys, json
import numpy as np
sys.path.insert(0, "/home/aiden/anima")
from core.decode import clm_load_weights, _conv1d, nn_groupnorm_fwd, nn_gelu_fwd, nn_moe_router_fwd

CLM="/home/aiden/py303_full.clm"

def fwd_penult(W, tok, T):
    """copy of _fwd_logits up to yn (penultimate, pre-readout). returns yn:[T,d]."""
    d=W["d"]; E=W["E"]; K=W["K"]; L=W["L"]
    ids=tok.astype(np.int64); xe=W["embed"][ids]
    xt=_conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    dil=1
    for li in range(L):
        de=dil if dil<=512 else 512
        h=_conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, de)
        hn=nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        xt=xt+nn_gelu_fwd(hn).reshape(T,d); dil*=2
    logits_r=_conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)
    ex=np.empty((E,T,d))
    for ej in range(E): ex[ej]=nn_gelu_fwd(_conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)).reshape(T,d)
    y=nn_moe_router_fwd(logits_r, ex, T, E, d)
    yn=nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    return yn  # [T,d]

def feat(W, text, T=24):
    b=text.encode('utf-8','surrogateescape'); n=len(b)
    tok=np.array([b[len(b)-T+p] if len(b)-T+p>=0 else 32 for p in range(T)],dtype=np.float64)
    yn=fwd_penult(W, tok, T)
    return yn.mean(axis=0)  # mean-pool [d]

CONCEPTS=["cat","dog","king","queen","water","fire","music","science","love","money","child","doctor"]
CTX=["the {} is here.","I saw a {} today.","she likes the {} very much.","a {} appeared suddenly.",
     "this {} is interesting.","we talked about the {}."]

def main():
    W=clm_load_weights(CLM); d=W["d"]
    print(f"loaded clm d={d} L={W['L']} E={W['E']} V={W['V']}",flush=True)
    # build feature matrix: [concept, ctx] -> feature
    NC=len(CONCEPTS); NCTX=len(CTX)
    F=np.zeros((NC,NCTX,d))
    for ci,c in enumerate(CONCEPTS):
        for xi,t in enumerate(CTX):
            F[ci,xi]=feat(W, t.format(c))
        print(f"feat {c} done",flush=True)
    # ---- Test 1: concept-identity recoverability (held-out context) ----
    # train linear probe on ctx 0..3, test ctx 4..5 (held-out contexts, same concepts)
    rng=np.random.default_rng(7)
    Xtr=F[:,:4].reshape(NC*4,d); ytr=np.repeat(np.arange(NC),4)
    Xte=F[:,4:].reshape(NC*2,d); yte=np.repeat(np.arange(NC),2)
    # ridge multiclass via one-hot lstsq
    Yoh=np.eye(NC)[ytr]
    Xb=np.hstack([Xtr, np.ones((len(Xtr),1))]); Wp=np.linalg.lstsq(Xb+1e-3*rng.standard_normal(Xb.shape)*0, Yoh, rcond=None)[0]
    # proper ridge
    lam=1.0; A=Xb.T@Xb+lam*np.eye(Xb.shape[1]); Wp=np.linalg.solve(A, Xb.T@Yoh)
    Xteb=np.hstack([Xte, np.ones((len(Xte),1))]); pred=(Xteb@Wp).argmax(1)
    id_acc=float((pred==yte).mean())
    # feature distinctness: mean pairwise cosine between concept-mean features
    cm=F.mean(axis=1); cm=cm/ (np.linalg.norm(cm,axis=1,keepdims=True)+1e-9)
    cos=cm@cm.T; off=cos[~np.eye(NC,dtype=bool)]
    print(f"\n[TEST1] concept-identity held-out acc={id_acc:.3f} (chance={1/NC:.3f}); mean off-diag cosine={off.mean():.3f}",flush=True)
    # ---- Test 2: structured recombination on REAL features vs RANDOM ----
    Kc=4; g=np.random.default_rng(11); T2=g.integers(0,6,size=(Kc,Kc))  # factored non-additive rule
    combos=[(a,b) for a in range(NC) for b in range(NC)]; g.shuffle(combos)
    nho=round(len(combos)*0.25); held=set(combos[:nho]); seen=[c for c in combos if c not in held]
    def recomb(featmat):
        # featmat: [NC,d] per-concept latent; target y=T2[a%Kc,b%Kc]; readout ridge on concat
        def mk(cl):
            X=np.array([np.concatenate([featmat[a],featmat[b]]) for a,b in cl])
            y=np.array([T2[a%Kc,b%Kc] for a,b in cl]); return X,y
        Xtr,ytr=mk(seen); Xte,yte=mk(held)
        Yoh=np.eye(6)[ytr]; Xb=np.hstack([Xtr,np.ones((len(Xtr),1))])
        A=Xb.T@Xb+1.0*np.eye(Xb.shape[1]); Wp=np.linalg.solve(A,Xb.T@Yoh)
        Xteb=np.hstack([Xte,np.ones((len(Xte),1))]); return float(((Xteb@Wp).argmax(1)==yte).mean())
    real_feat=F.mean(axis=1)  # [NC,d] real concept features
    rand_feat=g.standard_normal((NC,d))
    shuf=real_feat[g.permutation(NC)]
    real_acc=recomb(real_feat); rand_acc=recomb(rand_feat); shuf_acc=recomb(shuf)
    chance=1/6
    print(f"\n[TEST2] structured recomb held-out (chance={chance:.3f}): REAL={real_acc:.3f} RANDOM={rand_acc:.3f} SHUFFLE={shuf_acc:.3f}",flush=True)
    # verdict
    if id_acc>=0.5 and real_acc>=chance+0.2:
        v=("SUBSTRATE CARRIES RECOMBINABLE STRUCTURE — real 303M penultimate features distinctly encode "
           "concepts (id-acc high) AND support held-out structured recombination >> chance. => real-text "
           "G1=0 is NOT a feature/substrate wall; it is a generation/metric issue (concepts are there, "
           "recombination works on the features). structure-aware.")
    elif id_acc<0.3:
        v=("FEATURE-DEGENERATE — real trunk penultimate does NOT distinctly encode concepts (id-acc≈chance) "
           "=> concept identity itself is the bottleneck; the substrate lacks separable concept structure.")
    else:
        v=("MIXED — partial concept-identity and/or partial recombination; see numbers.")
    out={"id_heldout_acc":round(id_acc,4),"mean_offdiag_cos":round(float(off.mean()),4),
         "recomb":{"real":round(real_acc,4),"random":round(rand_acc,4),"shuffle":round(shuf_acc,4),"chance":round(chance,4)},
         "reading":v}
    json.dump(out,open("result.json","w"),indent=2)
    print("\n=== VERDICT ===\n"+v,flush=True)

if __name__=="__main__": main()
