"""V6_29 (LANE-BUS Step-3) Phase B -- emit-gate ablation, BATCHED recurrence (torch, fast).

Same design as before (Fable 4-arm + Sol WRONG-ADDR + B0 pedestal + integrate-and-fire positive
control), but the recurrence is batched across sentences (one sentence per row, step the time
axis over all rows at once) instead of a per-position Python loop -- ~100x faster, so full power
(3 seeds, 25 epochs, all sentences) runs in minutes, not an hour.

Arms (r_0=0 per sentence-row; g_t = sigmoid(a.x + b.r + c0); loss = masked BCE(g, emit)):
  FULL      r_t = (1-g_{t-1}) * lam ⊙ r_{t-1} + U tau_t      (emit-tied consumption)
  A1        r_t =              lam ⊙ r_{t-1} + U tau_t       (no consume)
  A2        r_t = (1-rho_{t-1})* lam ⊙ r_{t-1} + U tau_t      (yoked random reset)
  A3        r_t = (1-f_t)     * lam ⊙ r_{t-1} + U tau_t, f=σ(a'x+b'r)  (free forget)
  WRONGADDR FULL recurrence on a norm-matched deranged tau (Sol)
  B0        memoryless
Primary DV = held-out masked per-position BCE. Positive control: FULL must beat A1 (z>=3) or VOID.
"""
import sys, os, numpy as np
import torch, torch.nn as nn

RDIM = 8; SEEDS = [7, 11, 4302]; EPOCHS = 25; LR = 3e-3

def batchify(tau, x, emit, sid):
    """-> tensors [B, Tmax, .] padded per sentence, + mask [B,Tmax]."""
    ids = np.unique(sid); B = len(ids); Tmax = max((sid == i).sum() for i in ids)
    TA = np.zeros((B, Tmax, tau.shape[1]), np.float32)
    X = np.zeros((B, Tmax, x.shape[1]), np.float32)
    E = np.zeros((B, Tmax), np.float32); M = np.zeros((B, Tmax), np.float32)
    for r, i in enumerate(ids):
        m = sid == i; n = m.sum()
        TA[r,:n] = tau[m]; X[r,:n] = x[m]; E[r,:n] = emit[m]; M[r,:n] = 1.0
    return (torch.tensor(TA), torch.tensor(X), torch.tensor(E), torch.tensor(M), ids)

class Gate(nn.Module):
    def __init__(self, xd, td, arm):
        super().__init__(); self.arm = arm
        self.U = nn.Linear(td, RDIM, bias=False)
        self.lam = nn.Parameter(torch.full((RDIM,), 0.0))
        self.a = nn.Linear(xd, 1); self.b = nn.Linear(RDIM, 1, bias=False)
        if arm == "A3":
            self.fa = nn.Linear(xd, 1); self.fb = nn.Linear(RDIM, 1, bias=False)
    def forward(self, TA, X, rho=None):
        B, T, _ = TA.shape
        lam = torch.sigmoid(self.lam)
        r = torch.zeros(B, RDIM); gp = torch.zeros(B, 1); out = []
        for t in range(T):
            u = self.U(TA[:, t])
            if self.arm == "B0":
                pass
            elif self.arm == "A1":
                r = lam * r + u
            elif self.arm == "A2":
                r = (1 - rho[:, t:t+1]) * lam * r + u
            elif self.arm == "A3":
                f = torch.sigmoid(self.fa(X[:, t]) + self.fb(r)); r = (1 - f) * lam * r + u
            else:  # FULL, WRONGADDR
                r = (1 - gp) * lam * r + u
            logit = self.a(X[:, t]) + (0 if self.arm == "B0" else self.b(r))
            gp = torch.sigmoid(logit)
            out.append(logit)
        return torch.stack(out, 1).squeeze(-1)   # [B, T]

def train_arm(arm, TA, X, E, M, tr, te, seed, rho=None, pos=0.3):
    torch.manual_seed(seed)
    m = Gate(X.shape[2], TA.shape[2], arm)
    opt = torch.optim.Adam(m.parameters(), lr=LR, weight_decay=1e-4)
    w = torch.tensor([(1-pos)/max(pos,1e-3)])
    best = 1e9
    for ep in range(EPOCHS):
        m.train(); opt.zero_grad()
        lg = m(TA, X, rho)
        loss_pos = nn.functional.binary_cross_entropy_with_logits(lg, E, weight=M, pos_weight=w, reduction='sum')/(M[tr].sum()+1e-9)
        # restrict grad to train rows
        lg_tr = m(TA[tr], X[tr], None if rho is None else rho[tr])
        loss = nn.functional.binary_cross_entropy_with_logits(lg_tr, E[tr], weight=M[tr], pos_weight=w, reduction='sum')/(M[tr].sum()+1e-9)
        loss.backward(); nn.utils.clip_grad_norm_(m.parameters(),1.0); opt.step()
        m.eval()
        with torch.no_grad():
            lg_te = m(TA[te], X[te], None if rho is None else rho[te])
            te_loss = (nn.functional.binary_cross_entropy_with_logits(lg_te, E[te], weight=M[te], reduction='sum')/(M[te].sum()+1e-9)).item()
        best = min(best, te_loss)
    return best

def run(TA, X, E, M, ids, label=""):
    arms = ["B0","A1","A2","A3","FULL","WRONGADDR"]; res = {a: [] for a in arms}
    B = TA.shape[0]; pos = (E*M).sum().item()/max(M.sum().item(),1)
    for seed in SEEDS:
        rng = np.random.default_rng(seed); perm = rng.permutation(B); k = B//2
        tr = torch.zeros(B,dtype=torch.bool); te = torch.zeros(B,dtype=torch.bool); tr[perm[:k]]=True; te[perm[k:]]=True
        rho = torch.tensor((rng.random(TA.shape[:2]) < max(pos,0.05)).astype(np.float32))
        # WRONGADDR tau: shuffle rows within time, norm-matched
        idx = rng.permutation(B); TAd = TA[idx].clone()
        n0 = TA.norm(dim=2,keepdim=True)+1e-9; nd = TAd.norm(dim=2,keepdim=True)+1e-9; TAd = TAd/nd*n0
        for a in arms:
            t_in = TAd if a=="WRONGADDR" else TA
            res[a].append(train_arm(a, t_in, X, E, M, tr, te, seed, rho, pos))
    def z(a,b):
        d = np.array(res[b])-np.array(res[a]); return d.mean(), d.mean()/(d.std(ddof=1)/np.sqrt(len(d))+1e-9)
    print(f"\n=== {label} held-out masked NLL ({len(SEEDS)} seeds; lower=better) · pos={pos:.3f} ===")
    for a in arms: print(f"  {a:<10} {np.mean(res[a]):.4f}")
    print(f"  headroom B0-FULL = {np.mean(res['B0'])-np.mean(res['FULL']):+.4f}")
    for b in ("A1","A2","A3","WRONGADDR"):
        mm,zz=z("FULL",b); print(f"  {b}-FULL = {mm:+.4f}  z={zz:+.2f}")
    return res

def positive_control():
    rng = np.random.default_rng(0); nS=200; Tp=40; N=nS*Tp; sid=np.repeat(np.arange(nS),Tp)
    drive = (rng.standard_normal((N,16))*0.5).astype(np.float32); sig=drive[:,0]+0.35  # DC bias
    drive[:,0]=sig
    emit=np.zeros(N,np.float32); acc=0.0; theta=3.0
    for t in range(N):
        if t%Tp==0: acc=0.0
        acc+=sig[t]
        if acc>theta: emit[t]=1.0; acc=0.0
    xn = rng.standard_normal((N,6)).astype(np.float32)  # pure-noise x: only tau-accumulation predicts emit
    x = xn
    return drive,x,emit,sid

def main():
    cache = sys.argv[1] if len(sys.argv)>1 else "v6_29_cache.npz"
    print("== POSITIVE CONTROL ==")
    tau,x,emit,sid = positive_control()
    pc = run(*batchify(tau,x,emit,sid),"POS")
    mpc=np.array(pc["A1"])-np.array(pc["FULL"]); zpc=mpc.mean()/(mpc.std(ddof=1)/np.sqrt(len(mpc))+1e-9)
    ok = mpc.mean()>0 and zpc>=3
    print(f"  POS A1-FULL z={zpc:.2f} -> {'PASS' if ok else 'FAIL -> VOID'}")
    print("\n== NATURAL ==")
    d=np.load(cache); tau=d["tau"]; x=d["x"]; x=(x-x.mean(0))/(x.std(0)+1e-9); emit=d["emit"].astype(np.float32); sid=d["sid"]
    nat = run(*batchify(tau,x,emit,sid),"NAT")
    print("\n=== VERDICT ===")
    if not ok: print("VOID — positive control failed."); return 0
    head=np.mean(nat["B0"])-np.mean(nat["FULL"])
    a1=np.array(nat["A1"])-np.array(nat["FULL"]); za1=a1.mean()/(a1.std(ddof=1)/np.sqrt(len(a1))+1e-9)
    a3=np.array(nat["A3"])-np.array(nat["FULL"]); za3=a3.mean()/(a3.std(ddof=1)/np.sqrt(len(a3))+1e-9)
    print(f"headroom B0-FULL={head:+.4f} · A1-FULL z={za1:.2f} · A3-FULL z={za3:.2f}")
    if head<=0: print("→ memory buys nothing (B0>=FULL); gate is memoryless, discharge moot.")
    elif a1.mean()>0 and za1>=3 and a1.mean()>=0.1*head:
        print("→ 🟢 ARCHITECTED DISCHARGE VALIDATED (FULL>=A3)." if (a3.mean()>=0 or za3>-2)
              else "→ residual consumed but NOT at emits (A3>FULL): p5 emit-tie WRONG.")
    else: print("→ architected discharge does NOT improve emit (A1≈FULL): drop residual consumption from p5.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
