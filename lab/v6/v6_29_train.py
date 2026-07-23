"""V6_29 (LANE-BUS Step-3) Phase B -- train the emit-gate arms + ablations (torch, summer).

Reconciled Fable+Sol. Tiny recurrent gate heads (~few hundred params) over the frozen V6_29
feature cache. The question: does an emit-TIED residual consumption term improve the emit/silence
decision beyond (i) no memory (B0), (ii) generic gated recurrence (A3 free-forget), (iii) a
timing-matched random reset (A2), (iv) an address-broken consumption (WRONG-ADDR, Sol)?

Arms (r_0=0 per sentence; g_t = sigmoid(a.x_t + b.r_t + c0); loss = BCE(g_t, emit_t)):
  FULL      r_t = (1 - g_{t-1}) * lambda ⊙ r_{t-1} + U tau_t        (emit-tied consumption)
  A1        r_t =                lambda ⊙ r_{t-1} + U tau_t        (pure leak, no consume)
  A2        r_t = (1 - rho_{t-1})* lambda ⊙ r_{t-1} + U tau_t       (yoked random reset)
  A3        r_t = (1 - f_t)     * lambda ⊙ r_{t-1} + U tau_t, f_t=σ(a'x+b'r+c')  (free forget)
  WRONGADDR r_t = (1 - g_{t-1}) * lambda ⊙ r_{t-1} + U tau~_t       (derangement, ‖·‖ matched)
  B0        g_t = sigmoid(a.x_t + c0)                               (memoryless pedestal)

Primary DV = held-out per-position BCE (NLL). Seeds 7/11/4302 (Sol) — 3 seeds, no HP search.
Positive control: synthetic integrate-and-fire (emit = accumulated tau since last emit > theta);
FULL must beat A1 there (z>=3) or the whole run is VOID.
"""
import sys, os, numpy as np
import torch, torch.nn as nn

RDIM = 8; SEEDS = [7, 11, 4302]; EPOCHS = 25; LR = 1e-3

def load(path):
    d = np.load(path)
    return d["tau"], d["x"], d["emit"].astype(np.float32), d["sid"]

def split(sid, frac=0.5, seed=0):
    ids = np.unique(sid); rng = np.random.default_rng(seed); rng.shuffle(ids)
    k = int(len(ids)*frac); tr = set(ids[:k].tolist())
    return np.array([s in tr for s in sid]), np.array([s not in tr for s in sid])

class Gate(nn.Module):
    def __init__(self, xd, td, arm):
        super().__init__(); self.arm = arm
        self.U = nn.Linear(td, RDIM, bias=False)
        self.lam = nn.Parameter(torch.full((RDIM,), 0.5))
        self.a = nn.Linear(xd, 1); self.b = nn.Linear(RDIM, 1, bias=False)
        if arm == "A3":
            self.fa = nn.Linear(xd, 1); self.fb = nn.Linear(RDIM, 1, bias=False)
    def forward(self, tau, x, sid, rho=None):
        # sequential over positions, reset r at sentence boundaries
        N = tau.shape[0]; r = torch.zeros(RDIM); gp = torch.zeros(1); out = []
        prev = -1
        lam = torch.sigmoid(self.lam)
        for t in range(N):
            if sid[t] != prev: r = torch.zeros(RDIM); gp = torch.zeros(1); prev = sid[t]
            if self.arm == "B0":
                pass
            elif self.arm == "A1":
                r = lam * r + self.U(tau[t])
            elif self.arm == "A2":
                r = (1 - rho[t]) * lam * r + self.U(tau[t])
            elif self.arm == "A3":
                f = torch.sigmoid(self.fa(x[t]) + self.fb(r)); r = (1 - f).squeeze() * lam * r + self.U(tau[t])
            else:  # FULL, WRONGADDR (tau already deranged for WRONGADDR)
                r = (1 - gp).squeeze() * lam * r + self.U(tau[t])
            logit = self.a(x[t]) + (0 if self.arm == "B0" else self.b(r))
            gp = torch.sigmoid(logit)
            out.append(logit)
        return torch.stack(out).squeeze(-1)

def train_arm(arm, tau, x, emit, sid, tr, te, seed, rho=None):
    torch.manual_seed(seed)
    m = Gate(x.shape[1], tau.shape[1], arm)
    opt = torch.optim.Adam(m.parameters(), lr=LR, weight_decay=1e-4)
    pos = emit[tr].mean(); w = torch.tensor([(1-pos)/max(pos,1e-3)])
    Tt = torch.tensor(tau); Xt = torch.tensor(x); Et = torch.tensor(emit)
    best = 1e9; best_te = None
    for ep in range(EPOCHS):
        m.train(); opt.zero_grad()
        lg = m(Tt, Xt, sid, rho)
        loss = nn.functional.binary_cross_entropy_with_logits(lg[tr], Et[tr], pos_weight=w)
        loss.backward(); nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        m.eval()
        with torch.no_grad():
            teloss = nn.functional.binary_cross_entropy_with_logits(m(Tt,Xt,sid,rho)[te], Et[te]).item()
        if teloss < best: best = teloss
    return best

def run(tau, x, emit, sid, label=""):
    arms = ["B0","A1","A2","A3","FULL","WRONGADDR"]
    res = {a: [] for a in arms}
    for seed in SEEDS:
        tr, te = split(sid, seed=seed)
        # A2 yoked random reset at FULL's rough fire rate ~ emit rate
        rng = np.random.default_rng(seed); rho = torch.tensor(rng.random(len(sid)) < max(emit.mean(),0.05), dtype=torch.float32)
        # WRONGADDR: derange tau across positions with a different composed candidate (approx: shuffle rows, match norm)
        perm = rng.permutation(len(sid)); td = tau[perm].copy()
        n0 = np.linalg.norm(tau,axis=1,keepdims=True)+1e-9; nd = np.linalg.norm(td,axis=1,keepdims=True)+1e-9
        td = (td/nd)*n0
        for a in arms:
            t_in = td if a == "WRONGADDR" else tau
            res[a].append(train_arm(a, t_in, x, emit, sid, tr, te, seed, rho))
    def z(a, b):
        d = np.array(res[b]) - np.array(res[a])  # NLL(b)-NLL(a); >0 => a better
        return d.mean(), d.mean()/(d.std(ddof=1)/np.sqrt(len(d))+1e-9)
    print(f"\n=== {label} held-out NLL (mean over {len(SEEDS)} seeds; lower=better) ===")
    for a in arms: print(f"  {a:<10} {np.mean(res[a]):.4f}")
    print(f"  headroom B0-FULL = {np.mean(res['B0'])-np.mean(res['FULL']):+.4f}")
    for b in ("A1","A2","A3","WRONGADDR"):
        m,zz = z("FULL", b); print(f"  {b}-FULL = {m:+.4f}  z={zz:+.2f}  (>0 & z>=2 => FULL better than {b})")
    return res

def positive_control():
    # synthetic integrate-and-fire: emit when cumulative tau-signal since last emit crosses theta
    rng = np.random.default_rng(0); N=8000; sid=np.repeat(np.arange(200), 40)
    drive = rng.standard_normal((N,16)).astype(np.float32)*0.5
    sig = drive[:,0]; acc=0.0; emit=np.zeros(N,np.float32); theta=1.2
    for t in range(N):
        if t>0 and sid[t]!=sid[t-1]: acc=0.0
        acc += sig[t]
        if acc>theta: emit[t]=1.0; acc=0.0
    x = np.column_stack([sig, np.abs(sig), drive[:,1], drive[:,2], np.zeros(N), np.abs(drive[:,3])]).astype(np.float32)
    return drive, x, emit, sid

def main():
    cache = sys.argv[1] if len(sys.argv)>1 else "v6_29_cache.npz"
    print("== POSITIVE CONTROL (integrate-and-fire) ==")
    tau,x,emit,sid = positive_control()
    pc = run(tau,x,emit,sid,"POS-CONTROL")
    m_pc = np.array(pc["A1"])-np.array(pc["FULL"]); z_pc = m_pc.mean()/(m_pc.std(ddof=1)/np.sqrt(len(m_pc))+1e-9)
    pc_ok = m_pc.mean()>0 and z_pc>=3
    print(f"  POS-CONTROL A1-FULL z={z_pc:.2f} -> {'PASS' if pc_ok else 'FAIL (VOID everything below)'}")
    print("\n== NATURAL ==")
    tau,x,emit,sid = load(cache)
    x = (x - x.mean(0))/(x.std(0)+1e-9)
    nat = run(tau,x,emit,sid,"NATURAL")
    print("\n=== VERDICT ===")
    if not pc_ok: print("VOID — positive control failed."); return 0
    head = np.mean(nat["B0"])-np.mean(nat["FULL"])
    a1 = np.array(nat["A1"])-np.array(nat["FULL"]); z_a1=a1.mean()/(a1.std(ddof=1)/np.sqrt(len(a1))+1e-9)
    a3 = np.array(nat["A3"])-np.array(nat["FULL"]); z_a3=a3.mean()/(a3.std(ddof=1)/np.sqrt(len(a3))+1e-9)
    print(f"B0-FULL headroom={head:+.4f} · A1-FULL z={z_a1:.2f} · A3-FULL z={z_a3:.2f}")
    if head<=0: print("→ memory buys nothing (B0>=FULL): residual-state dead on this proxy; gate is memoryless.")
    elif a1.mean()>0 and z_a1>=3 and a1.mean()>=0.1*head:
        if a3.mean()>=0 or z_a3>-2: print("→ 🟢 ARCHITECTED DISCHARGE VALIDATED: consumption helps AND emit-tie costs nothing vs free-forget → build real gate.")
        else: print("→ residual consumed but NOT at emits (A3>FULL): p5 emit⇄discharge tie WRONG → autonomous relaxation + read-only emit gate.")
    else: print("→ architected discharge does NOT improve emit (A1≈FULL): drop residual consumption from p5.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
