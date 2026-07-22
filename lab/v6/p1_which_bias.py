"""Which bias solves LATIN? The determinacy check proved the answer is unique -- so the
information is there and something can reach it. The question is what.

Three readers on the SAME trained embedding model, same seeds, same table:
  argmax     what P1 used: pick the top logit per cell, independently
  hungarian  a PERMUTATION bias: the held-out cells of a row/column must complete it to a
             permutation, so assign them jointly instead of independently
  propagate  pure constraint propagation on the latin property, using NO model at all
"""
import itertools, importlib.util, numpy as np
spec=importlib.util.spec_from_file_location("sc","p1_nongroup_scope.py")
sc=importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)
N=sc.N

def logits_for(env, pred_fn, pairs):
    return pred_fn(pairs)

def train_logits(env, wd=0.3):
    """same trainer as the scope test, but returns LOGITS not argmax"""
    rng=env["rng"]
    A=np.stack([sc.addr(env,i) for (i,j) in env["train"]])
    B=np.stack([sc.addr(env,j) for (i,j) in env["train"]])
    y=sc.gold(env, env["train"]); m=len(y)
    E=rng.normal(0,0.5,(N,sc.D_E))
    W1=rng.normal(0,0.5/np.sqrt(sc.D_E),(sc.D_E,sc.HID)); b1=np.zeros(sc.HID)
    W2=rng.normal(0,0.5/np.sqrt(sc.HID),(sc.HID,N)); b2=np.zeros(N)
    ps=[E,W1,b1,W2,b2]; opt=sc.Adam([p.shape for p in ps],wd=wd)
    for _ in range(sc.STEPS):
        bi=rng.integers(0,m,64)
        X=A[bi]@E+B[bi]@E
        h=np.tanh(X@W1+b1); p=sc.softmax(h@W2+b2)
        p[np.arange(len(bi)),y[bi]]-=1.0; p/=len(bi)
        gW2=h.T@p; gb2=p.sum(0); gh=(p@W2.T)*(1-h**2)
        gW1=X.T@gh; gb1=gh.sum(0); gX=gh@W1.T
        opt.step(ps,[A[bi].T@gX+B[bi].T@gX,gW1,gb1,gW2,gb2])
    def logits(pairs):
        A2=np.stack([sc.addr(env,i) for (i,j) in pairs]); B2=np.stack([sc.addr(env,j) for (i,j) in pairs])
        return np.tanh((A2@E+B2@E)@W1+b1)@W2+b2
    return logits

def hungarian_rows(env, lg, pairs):
    """Per ROW, the held-out cells must take exactly the symbols that row is missing.
    Assign them jointly (greedy on the model's own scores) instead of independently."""
    out={}
    byrow={}
    for k,(i,j) in enumerate(pairs): byrow.setdefault(i,[]).append((k,j))
    for i,items in byrow.items():
        seen={env["table"][i][j] for j in range(N) if (i,j) not in pairs}
        missing=sorted(set(range(N))-seen)
        cand=[(lg[k][v], k, v) for k,_ in items for v in missing]
        cand.sort(reverse=True)
        usedk,usedv=set(),set()
        for _,k,v in cand:
            if k in usedk or v in usedv: continue
            out[k]=v; usedk.add(k); usedv.add(v)
        for k,_ in items:
            out.setdefault(k, missing[0] if missing else 0)
    return np.array([out[k] for k in range(len(pairs))])

def propagate(env, pairs):
    """No model at all: constraint propagation on the latin property."""
    tbl=[[env["table"][i][j] if (i,j) not in pairs else None for j in range(N)] for i in range(N)]
    changed=True
    while changed:
        changed=False
        for i,j in pairs:
            if tbl[i][j] is not None: continue
            used={tbl[i][c] for c in range(N) if tbl[i][c] is not None} | \
                 {tbl[r][j] for r in range(N) if tbl[r][j] is not None}
            cand=set(range(N))-used
            if len(cand)==1:
                tbl[i][j]=cand.pop(); changed=True
    return np.array([tbl[i][j] if tbl[i][j] is not None else -1 for (i,j) in pairs])

print("WHICH BIAS SOLVES LATIN? (answer is UNIQUE -- V6_P1d proved it) chance %.4f\n"%(1/N))
print("%-12s %-12s %9s"%("table","reader","HELD-OUT"))
print("-"*38)
for kind in ("cyclic","latin"):
    accs={"argmax":[], "hungarian":[], "propagate":[]}
    for s in sc.SEEDS:
        env=sc.build(s,kind); lgf=train_logits(env)
        te=env["test"]; y=sc.gold(env,te); lg=lgf(te)
        accs["argmax"].append(float((lg.argmax(1)==y).mean()))
        accs["hungarian"].append(float((hungarian_rows(env,lg,te)==y).mean()))
        accs["propagate"].append(float((propagate(env,te)==y).mean()))
    for r in ("argmax","hungarian","propagate"):
        print("%-12s %-12s %9.4f"%(kind,r,float(np.mean(accs[r]))))
print("-"*38)
