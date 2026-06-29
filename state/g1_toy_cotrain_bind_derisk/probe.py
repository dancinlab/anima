#!/usr/bin/env python3
"""
Toy co-train bind derisk — pure numpy, $0 CPU, mini-safe.

Q: Does a small model CO-TRAINED with a live bilinear bind op beat λ=0 control
   on held-out 2-concept recombination?

TWO TASKS
=========
[A] Product-regression (clean mechanism test with provable bilinear advantage)
    Fixed random "concept keys" k_A[N_A×D], k_B[N_B×D].
    Target for combo (a,b): t = k_A[a] ⊙ k_B[b]  (element-wise product).

    bind-ON  : pred = emb_A[a] ⊙ emb_B[b]   → can match k_A[a] ⊙ k_B[b]  ✓
    bind-OFF : pred = emb_A[a] + emb_B[b]   → additive ≠ product targets  ✗
    Loss: MSE.  Metric: test_MSE / train_MSE (≈1.0 = generalises; >>1 = overfit).

    This task PROVABLY requires bilinear composition: the additive model cannot
    represent the product targets even at zero error on training examples.

[B] 36-class classification (closer to production G1 setup)
    bind-ON  : trunk([ha;hb]) + bilinear(ha,hb) residual, co-trained
    bind-OFF : trunk([ha;hb]) only  (λ=0 control)
    Predict y = a·N_B + b.  D=8, no WD on embeddings, WD=1e-3 on weights.
    Metric: held-out accuracy (fraction of 8 unseen combos correct).

Both tasks use stratified hold-out: each A and B value appears in training.
Multi-seed: SEEDS = [7, 4302, 4303].

Framing: TOY DIRECTIONAL (a_toy_scale_recheck — toy green ≠ production verdict).
"""
import time, json
import numpy as np

# ─── Config ──────────────────────────────────────────────────────────────────
N_A      = 6
N_B      = 6
N_COMBOS = N_A * N_B   # 36
N_HELDOUT = 8
D        = 12          # concept key / embedding dim
LR_A     = 1e-2        # Task A learning rate
LR_B     = 3e-3        # Task B learning rate
WD_B     = 1e-3        # Task B weight decay (on weight matrices only, not embeddings)
N_STEPS  = 4000
SEEDS    = [7, 4302, 4303]
LIFT_BAR_ACC = 0.05    # Task B: min acc lift
RATIO_BAR    = 2.0     # Task A: generalises if test/train MSE ratio < this

# ─── Activations ─────────────────────────────────────────────────────────────
def gelu(x):
    return 0.5*x*(1+np.tanh(np.sqrt(2/np.pi)*(x+0.044715*x**3)))
def dgelu(x):
    cdf = 0.5*(1+np.tanh(np.sqrt(2/np.pi)*(x+0.044715*x**3)))
    return cdf + x*np.exp(-0.5*x**2)/np.sqrt(2*np.pi)
def softmax(x):
    e = np.exp(x - x.max(-1,keepdims=True))
    return e/e.sum(-1,keepdims=True)
def cross_entropy(logits, y):
    p = softmax(logits)
    n = len(y)
    loss = -np.log(p[np.arange(n),y]+1e-12).mean()
    g = p.copy(); g[np.arange(n),y] -= 1; g /= n
    return loss, g

# ─── Stratified split ────────────────────────────────────────────────────────
def make_split(seed):
    rng = np.random.default_rng(seed*1000+42)
    combos = list((a,b) for a in range(N_A) for b in range(N_B))
    rng.shuffle(combos)
    a_cnt = [0]*N_A; b_cnt = [0]*N_B
    for a,b in combos: a_cnt[a]+=1; b_cnt[b]+=1
    held=[]; train=[]
    for a,b in combos:
        if len(held)<N_HELDOUT and a_cnt[a]>1 and b_cnt[b]>1:
            held.append((a,b)); a_cnt[a]-=1; b_cnt[b]-=1
        else:
            train.append((a,b))
    while len(held)<N_HELDOUT: held.append(train.pop())
    return np.array(train), np.array(held)

# ─── Adam step ───────────────────────────────────────────────────────────────
def adam(p, g, m, v, step, lr, wd=0.0, wd_keys=None,
         b1=0.9, b2=0.999, eps=1e-8):
    """wd applied only to keys in wd_keys (or all if wd_keys=None)."""
    for k in p:
        apply_wd = (wd>0 and (wd_keys is None or k in wd_keys))
        gk = g[k] + (wd*p[k] if apply_wd else 0)
        m[k] = b1*m[k]+(1-b1)*gk
        v[k] = b2*v[k]+(1-b2)*gk**2
        mh = m[k]/(1-b1**step); vh = v[k]/(1-b2**step)
        p[k] -= lr*mh/(np.sqrt(vh)+eps)

# ═══════════════════════════════════════════════════════════════════════════════
# TASK A: Product regression
# ═══════════════════════════════════════════════════════════════════════════════

def run_taskA(seed):
    """
    bind-ON  : pred = emb_A[a] ⊙ emb_B[b]
    bind-OFF : pred = emb_A[a] + emb_B[b]
    Target   : k_A[a] ⊙ k_B[b]  (fixed random concept keys)
    Loss     : MSE
    """
    rng = np.random.default_rng(seed)
    tr, te = make_split(seed)
    a_tr, b_tr = tr[:,0], tr[:,1]
    a_te, b_te = te[:,0], te[:,1]

    # Fixed concept keys (same for both arms, same seed)
    k_A = rng.standard_normal((N_A, D)) * 0.5
    k_B = rng.standard_normal((N_B, D)) * 0.5
    t_tr = k_A[a_tr] * k_B[b_tr]   # [N_train, D]
    t_te = k_A[a_te] * k_B[b_te]   # [N_test, D]

    results = {}
    for arm, use_prod in [('bind_ON', True), ('bind_OFF', False)]:
        rng2 = np.random.default_rng(seed)  # same init both arms
        eA = rng2.standard_normal((N_A, D)) * 0.3
        eB = rng2.standard_normal((N_B, D)) * 0.3
        mA = np.zeros_like(eA); vA = np.zeros_like(eA)
        mB = np.zeros_like(eB); vB = np.zeros_like(eB)

        t0 = time.time()
        for step in range(1, N_STEPS+1):
            ha = eA[a_tr]; hb = eB[b_tr]
            pred = ha*hb if use_prod else ha+hb
            diff = pred - t_tr                  # [N_train, D]
            loss = (diff**2).mean()
            # Gradient of MSE: d/dpred = 2*diff / (N*D)
            dout = 2*diff / (len(a_tr)*D)
            if use_prod:
                dha = dout * hb; dhb = dout * ha
            else:
                dha = dout;      dhb = dout

            # Embedding gradients (accumulate)
            geA = np.zeros_like(eA); geB = np.zeros_like(eB)
            np.add.at(geA, a_tr, dha)
            np.add.at(geB, b_tr, dhb)

            # Adam
            adam({'eA':eA,'eB':eB}, {'eA':geA,'eB':geB},
                 {'eA':mA,'eB':mB}, {'eA':vA,'eB':vB},
                 step, LR_A)

        ha_tr=eA[a_tr]; hb_tr=eB[b_tr]
        ha_te=eA[a_te]; hb_te=eB[b_te]
        pred_tr = ha_tr*hb_tr if use_prod else ha_tr+hb_tr
        pred_te = ha_te*hb_te if use_prod else ha_te+hb_te
        mse_tr = float(((pred_tr-t_tr)**2).mean())
        mse_te = float(((pred_te-t_te)**2).mean())
        ratio  = mse_te / (mse_tr+1e-12)
        results[arm] = {
            'mse_tr': round(mse_tr,5), 'mse_te': round(mse_te,5),
            'ratio':  round(ratio,3),   'elapsed': round(time.time()-t0,2),
        }

    return results

# ═══════════════════════════════════════════════════════════════════════════════
# TASK B: 36-class classification with trunk + optional bilinear residual
# ═══════════════════════════════════════════════════════════════════════════════

class TrunkBind:
    def __init__(self, use_bind, rng):
        s = lambda *sh: rng.standard_normal(sh)*np.sqrt(2/sh[0])
        self.use_bind = use_bind
        self.p = {
            'eA': rng.standard_normal((N_A,D))*0.1,
            'eB': rng.standard_normal((N_B,D))*0.1,
            'W1': s(2*D,2*D), 'b1': np.zeros(2*D),
            'W2': s(2*D,D),   'b2': np.zeros(D),
            'Wr': s(D,N_COMBOS), 'br': np.zeros(N_COMBOS),
        }
        if use_bind:
            self.p['WA'] = s(D,D); self.p['WB'] = s(D,D)
            self.p['Wp'] = rng.standard_normal((D,D))*0.01  # small init ≈ λ=0
            self.p['bp'] = np.zeros(D)

    def forward(self, a, b):
        p=self.p; c={}
        ha=p['eA'][a]; hb=p['eB'][b]
        hc=np.concatenate([ha,hb],-1)
        pr1=hc@p['W1']+p['b1']; h1=gelu(pr1)
        pr2=h1@p['W2']+p['b2']; h2=gelu(pr2)
        c.update({'ha':ha,'hb':hb,'hc':hc,'pr1':pr1,'h1':h1,'pr2':pr2,'a':a,'b':b})
        if self.use_bind:
            hp=ha@p['WA']; hq=hb@p['WB']
            br=hp*hq; bpr=br@p['Wp']+p['bp']; bh=np.tanh(bpr)
            h2=h2+bh
            c.update({'hp':hp,'hq':hq,'br':br,'bpr':bpr})
        logits=h2@p['Wr']+p['br']; c['h2']=h2
        return logits,c

    def backward(self, dl, c):
        p=self.p; g={k:np.zeros_like(v) for k,v in p.items()}
        g['Wr']=c['h2'].T@dl; g['br']=dl.sum(0)
        dh2=dl@p['Wr'].T
        if self.use_bind:
            dbpr=dh2*(1-np.tanh(c['bpr'])**2)
            g['Wp']=c['br'].T@dbpr; g['bp']=dbpr.sum(0)
            dbr=dbpr@p['Wp'].T
            dhp=dbr*c['hq']; dhq=dbr*c['hp']
            g['WA']=c['ha'].T@dhp; g['WB']=c['hb'].T@dhq
            dha_b=dhp@p['WA'].T; dhb_b=dhq@p['WB'].T
        dpr2=dh2*dgelu(c['pr2']); g['W2']=c['h1'].T@dpr2; g['b2']=dpr2.sum(0)
        dh1=dpr2@p['W2'].T
        dpr1=dh1*dgelu(c['pr1']); g['W1']=c['hc'].T@dpr1; g['b1']=dpr1.sum(0)
        dhc=dpr1@p['W1'].T
        dha_t=dhc[:,:D]; dhb_t=dhc[:,D:]
        dha=dha_t+(dha_b if self.use_bind else 0)
        dhb=dhb_t+(dhb_b if self.use_bind else 0)
        np.add.at(g['eA'],c['a'],dha); np.add.at(g['eB'],c['b'],dhb)
        return g

def run_taskB(seed):
    rng = np.random.default_rng(seed)
    tr,te = make_split(seed)
    a_tr,b_tr=tr[:,0],tr[:,1]; a_te,b_te=te[:,0],te[:,1]
    y_tr=a_tr*N_B+b_tr; y_te=a_te*N_B+b_te

    results={}
    WD_KEYS = {'W1','W2','Wr','WA','WB','Wp'}  # apply WD only to matrices

    for arm, use_bind in [('bind_ON',True),('bind_OFF',False)]:
        rng2=np.random.default_rng(seed)
        mdl=TrunkBind(use_bind,rng2)
        p=mdl.p
        m={k:np.zeros_like(v) for k,v in p.items()}
        v={k:np.zeros_like(v) for k,v in p.items()}

        t0=time.time()
        for step in range(1,N_STEPS+1):
            logits,c=mdl.forward(a_tr,b_tr)
            loss,dl=cross_entropy(logits,y_tr)
            g=mdl.backward(dl,c)
            adam(p,g,m,v,step,LR_B,WD_B,WD_KEYS)

        logits_tr,_=mdl.forward(a_tr,b_tr)
        logits_te,_=mdl.forward(a_te,b_te)
        tr_acc=float((logits_tr.argmax(-1)==y_tr).mean())
        te_acc=float((logits_te.argmax(-1)==y_te).mean())
        tr_ce,_=cross_entropy(logits_tr,y_tr); te_ce,_=cross_entropy(logits_te,y_te)
        results[arm]={
            'train_acc':round(tr_acc,4),'test_acc':round(te_acc,4),
            'train_ce':round(float(tr_ce),4),'test_ce':round(float(te_ce),4),
            'elapsed':round(time.time()-t0,2)
        }
    return results

# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    print("=== Toy co-train bind derisk ===")
    print(f"Task: N_A={N_A}×N_B={N_B}={N_COMBOS} combos, {N_HELDOUT} held-out")
    print(f"D={D}  N_STEPS={N_STEPS}  seeds={SEEDS}")
    print()

    all_A=[]; all_B=[]

    # ── Task A ──
    print("── Task A: Product regression (provable bilinear advantage) ──")
    print("   bind-ON=product ⊙  bind-OFF=additive +")
    print("   metric: test_MSE / train_MSE  (good generalisation → ratio≈1; overfit → ratio>>1)")
    for seed in SEEDS:
        r=run_taskA(seed)
        all_A.append({'seed':seed,**r})
        on=r['bind_ON']; off=r['bind_OFF']
        print(f"  seed={seed}  bind_ON: tr={on['mse_tr']:.4f} te={on['mse_te']:.4f} ratio={on['ratio']:.1f}"
              f"  |  bind_OFF: tr={off['mse_tr']:.4f} te={off['mse_te']:.4f} ratio={off['ratio']:.1f}")

    on_ratios  = [r['bind_ON']['ratio']  for r in all_A]
    off_ratios = [r['bind_OFF']['ratio'] for r in all_A]
    on_te  = [r['bind_ON']['mse_te']  for r in all_A]
    off_te = [r['bind_OFF']['mse_te'] for r in all_A]
    on_wins  = sum(r < RATIO_BAR for r in on_ratios)
    off_wins = sum(r < RATIO_BAR for r in off_ratios)
    print(f"\n  bind_ON  ratio mean={np.mean(on_ratios):.2f}  generalises(ratio<{RATIO_BAR}): {on_wins}/3")
    print(f"  bind_OFF ratio mean={np.mean(off_ratios):.2f}  generalises(ratio<{RATIO_BAR}): {off_wins}/3")
    on_wins_mse  = sum(on<off for on,off in zip(on_te,off_te))
    print(f"  bind_ON test_MSE < bind_OFF test_MSE: {on_wins_mse}/3 seeds")
    A_verdict = 'YES' if on_wins_mse>=2 else ('MARGINAL' if on_wins_mse==1 else 'NO')
    print(f"  Task A VERDICT: {A_verdict}")

    # ── Task B ──
    print()
    print("── Task B: 36-class composition (trunk + bilinear residual) ──")
    print(f"   WD={WD_B} (matrices only, no WD on embeddings)  LR={LR_B}")
    for seed in SEEDS:
        r=run_taskB(seed)
        all_B.append({'seed':seed,**r})
        on=r['bind_ON']; off=r['bind_OFF']
        print(f"  seed={seed}  bind_ON: tr={on['train_acc']:.3f} te={on['test_acc']:.3f} ce={on['test_ce']:.3f}"
              f"  |  bind_OFF: tr={off['train_acc']:.3f} te={off['test_acc']:.3f} ce={off['test_ce']:.3f}")

    on_acc  = [r['bind_ON']['test_acc']  for r in all_B]
    off_acc = [r['bind_OFF']['test_acc'] for r in all_B]
    lifts   = [o-x for o,x in zip(on_acc,off_acc)]
    B_wins  = sum(l>LIFT_BAR_ACC for l in lifts)
    print(f"\n  lifts={[round(l,3) for l in lifts]}  mean={np.mean(lifts):.3f}  wins(>{LIFT_BAR_ACC})={B_wins}/3")
    B_verdict = 'YES' if B_wins>=2 else ('MARGINAL' if B_wins==1 else 'NO')
    print(f"  Task B VERDICT: {B_verdict}")

    # ── Overall ──
    print()
    print("="*60)
    if A_verdict=='YES' and B_verdict=='YES':
        final='YES'
        conf='Product bias generalises (A✓) AND trunk+bilinear lifts classification (B✓) → raises 303M confidence'
    elif A_verdict=='YES':
        final='PARTIAL-YES'
        conf='Product bias generalises (A✓) but trunk+bilinear didn\'t lift classification (B✗) — mechanism works in isolation but needs better trunk separation for 303M'
    elif B_verdict=='YES':
        final='PARTIAL-YES'
        conf='Trunk+bilinear lifted classification (B✓) but pure product didn\'t win (A✗) — practical signal present'
    elif A_verdict=='NO' and B_verdict=='NO':
        final='NO'
        conf='Neither mechanism shows recombination lift at toy scale → early warning for 303M'
    else:
        final='MARGINAL'
        conf='Marginal signal in at least one design'

    print(f"OVERALL VERDICT: {final}")
    print(f"Confidence:      {conf}")

    out={'config':{'N_A':N_A,'N_B':N_B,'N_HELDOUT':N_HELDOUT,'D':D,
                   'N_STEPS':N_STEPS,'SEEDS':SEEDS,'LIFT_BAR_ACC':LIFT_BAR_ACC,
                   'RATIO_BAR':RATIO_BAR},
         'taskA':all_A,'taskB':all_B,
         'A_verdict':A_verdict,'B_verdict':B_verdict,'final_verdict':final}
    with open('raw_results.json','w') as f:
        json.dump(out,f,indent=2)
    print("\nSaved raw_results.json")
    return final

if __name__=='__main__':
    main()
