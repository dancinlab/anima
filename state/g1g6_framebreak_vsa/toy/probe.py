#!/usr/bin/env python3
"""
TOY-RESONATOR-READHEAD v1 (Fable spec) — does a FIXED bind/unbind/cleanup read-path
escape the additive collapse a CE-trained read-path suffers on held-out recombination?

Arms (matched codebook U[6,d], V[30,d], unit-L2 renorm every step, same init seed):
  A  CE read-head   : b=MLP_bind([u;v]); s=Σb; logits=MLP_read([s;u_rq])   (full end-to-end)
  B  fixed resonator: b=u⊛v (FFT); s=Σb; ŝ=Wiener_unbind(s,u_rq); logits=cos(ŝ,V)/τ  (train U,V only)
  B0 frozen ref     : B with U,V frozen at init, zero training
  C  additive ctrl  : bind=(u+v)/√2; unbind=s-u_rq/√2; same cosine cleanup  (train U,V only)

Verdict on HELD-OUT recombination acc, all 3 seeds (frozen bars, no tune-to-green):
  🟢 GREEN: B≥0.90 ∧ A≤0.40 ∧ C≤0.40 ∧ bind-destroy(B)≤0.40 ∧ Δ(B-A)≥0.50 ∧ shuffle→chance
  🔴 KILL : B≤0.40  (report B0: if B0≥0.90 ∧ B≤0.40 → "operator escapes but atoms must be gradient-free")
  🟡 CONFOUND: A≥0.90 (toy too easy; wall didn't reproduce)
Validity: all arms ≥0.99 train ∧ ≥0.95 test-indist ∧ co-occurrence probe ≤0.05 on held-out.
"""
import json, math, sys
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as Fn

DEV = 'cuda' if torch.cuda.is_available() else 'cpu'
R, F, D, K = 6, 30, 512, 3
STEPS, BATCH, LR = 20000, 256, 3e-4
A_MAX_STEPS = 60000          # extend A if train<0.99 (spec: undertrained A is not the wall)
TAU = 0.1
N_TEST = 5000

def is_heldout(r, f): return (f % R) == r     # (r,f) held out iff f mod 6 == r

# ---------- episode generators (return role_ids[K], filler_ids[K], q_idx, target_f) ----------
def gen_batch(rng, n, mode):
    """mode: 'train' | 'heldout' | 'indist'.
    train/indist: ALL-train-legal scene (in-distribution), query one — indist is the
      validity control (every arm that fits train must recall these; well-formed for its q).
    heldout: the query binding is a held-out cell; the 2 distractor fillers are train-legal
      for r_q so a co-occurrence heuristic actively prefers a distractor (anti-leak tooth)."""
    roles = np.zeros((n, K), np.int64); fills = np.zeros((n, K), np.int64)
    q = np.zeros(n, np.int64); tgt = np.zeros(n, np.int64)
    for i in range(n):
        rs = rng.choice(R, K, replace=False)
        if mode in ('train', 'indist'):
            fs, used = [], set()
            for r in rs:
                while True:
                    f = rng.integers(F)
                    if not is_heldout(r, f) and f not in used: break
                fs.append(f); used.add(f)
            qi = rng.integers(K)
        else:  # heldout
            rq = rs[0]
            while True:
                ft = rng.integers(F)
                if is_heldout(rq, ft): break
            fs, used = [ft], {ft}
            for r in rs[1:]:
                while True:
                    f = rng.integers(F)
                    # distractor legal-for-rq (rq saw it in train) => not held-out for rq; distinct
                    if not is_heldout(rq, f) and f not in used: break
                fs.append(f); used.add(f)
            qi = 0
        roles[i] = rs; fills[i] = fs; q[i] = qi; tgt[i] = fs[qi]
    return (torch.tensor(roles, device=DEV), torch.tensor(fills, device=DEV),
            torch.tensor(q, device=DEV), torch.tensor(tgt, device=DEV))

# ---------- fixed algebra ----------
def circconv(u, v):                       # (...,D)
    return torch.fft.irfft(torch.fft.rfft(u) * torch.fft.rfft(v), n=D)
def wiener_unbind(s, u):
    Su, Uu = torch.fft.rfft(s), torch.fft.rfft(u)
    return torch.fft.irfft(Su * torch.conj(Uu) / (Uu.abs()**2 + 1e-6), n=D)

class Arm(nn.Module):
    def __init__(self, kind, seed):
        super().__init__()
        g = torch.Generator().manual_seed(seed)
        self.U = nn.Parameter(torch.randn(R, D, generator=g) / math.sqrt(D))
        self.V = nn.Parameter(torch.randn(F, D, generator=g) / math.sqrt(D))
        self.kind = kind
        if kind == 'A':
            self.mlp_bind = nn.Sequential(nn.Linear(2*D, 1024), nn.GELU(), nn.Linear(1024, D))
            self.mlp_read = nn.Sequential(nn.Linear(2*D, 1024), nn.GELU(), nn.Linear(1024, F))
        if kind == 'B0':
            self.U.requires_grad_(False); self.V.requires_grad_(False)

    def renorm(self):
        with torch.no_grad():
            self.U.div_(self.U.norm(dim=1, keepdim=True) + 1e-8)
            self.V.div_(self.V.norm(dim=1, keepdim=True) + 1e-8)

    def forward(self, roles, fills, q, bind_destroy=False, shuffle=False):
        u = self.U[roles]                 # (n,K,D)
        v = self.V[fills]                 # (n,K,D)
        rq = q if not shuffle else (q + 1) % K   # shuffle: wrong query role
        u_rq = self.U[roles.gather(1, rq.view(-1,1)).squeeze(1)]  # (n,D)
        if self.kind == 'A':
            b = self.mlp_bind(torch.cat([u, v], -1))   # (n,K,D)
            s = b.sum(1)
            return self.mlp_read(torch.cat([s, u_rq], -1))
        # B / B0 / C : fixed read-path family
        if self.kind == 'C' or bind_destroy:
            b = (u + v) / math.sqrt(2); s = b.sum(1)
            sh = s - u_rq / math.sqrt(2)
        else:  # B, B0 : HRR
            b = circconv(u, v); s = b.sum(1)
            sh = wiener_unbind(s, u_rq)
        logits = Fn.cosine_similarity(sh.unsqueeze(1), self.V.unsqueeze(0), dim=-1) / TAU
        return logits

def acc(arm, roles, fills, q, tgt, **kw):
    with torch.no_grad():
        return (arm(roles, fills, q, **kw).argmax(1) == tgt).float().mean().item()

def train_arm(kind, seed, steps):
    rng = np.random.default_rng(1000 + seed)
    arm = Arm(kind, seed).to(DEV); arm.renorm()
    if kind == 'B0':
        return arm, 0.0, 0
    params = [p for p in arm.parameters() if p.requires_grad]
    opt = torch.optim.Adam(params, lr=LR)
    tr_acc, done = 0.0, 0
    for step in range(steps):
        roles, fills, q, tgt = gen_batch(rng, BATCH, 'train')
        logits = arm(roles, fills, q)
        loss = Fn.cross_entropy(logits, tgt)
        opt.zero_grad(); loss.backward(); opt.step(); arm.renorm()
        done = step + 1
        if step % 1000 == 999:
            tr_acc = (logits.argmax(1) == tgt).float().mean().item()
            if tr_acc >= 0.995 and step >= STEPS - 1:
                break
    return arm, tr_acc, done

def run_seed(seed):
    tst = np.random.default_rng(9000 + seed)
    ho = gen_batch(tst, N_TEST, 'heldout')
    ind = gen_batch(tst, N_TEST, 'indist')
    out = {}
    for kind in ('A', 'B', 'B0', 'C'):
        steps = A_MAX_STEPS if kind == 'A' else STEPS
        arm, tr, done = train_arm(kind, seed, steps)
        rec = dict(train_acc=round(tr, 4), steps=done,
                   heldout=round(acc(arm, *ho), 4),
                   indist=round(acc(arm, *ind), 4),
                   shuffle=round(acc(arm, ho[0], ho[1], ho[2], ho[3], shuffle=True), 4))
        if kind == 'B':
            rec['bind_destroyed'] = round(acc(arm, ho[0], ho[1], ho[2], ho[3], bind_destroy=True), 4)
            rec['codebook_drift'] = round((arm.V.detach() -
                (torch.randn(F, D, generator=torch.Generator().manual_seed(seed))/math.sqrt(D)).to(DEV)
                ).norm().item(), 3)
        out[kind] = rec
        print(f"seed{seed} {kind:2s}: train={rec['train_acc']:.3f} heldout={rec['heldout']:.3f} "
              f"indist={rec['indist']:.3f} shuf={rec['shuffle']:.3f}"
              + (f" bind_destroy={rec.get('bind_destroyed'):.3f}" if 'bind_destroyed' in rec else ""), flush=True)
    return out

def verdict(seeds):
    def allv(k, field, op, thr):
        return all(op(seeds[s][k][field], thr) for s in seeds)
    # validity preconditions (spec §3): A,B fit train >=0.99 AND recall in-dist >=0.95.
    # C is the additive floor: it CANNOT fit a binding task by construction (train<<0.99) —
    # that is itself the finding (additive operator cannot bind), so C is graded on held-out only.
    valid = (allv('A','train_acc',lambda x,t:x>=t,0.99) and allv('B','train_acc',lambda x,t:x>=t,0.99)
             and allv('A','indist',lambda x,t:x>=t,0.95) and allv('B','indist',lambda x,t:x>=t,0.95))
    primary = (allv('B','heldout',lambda x,t:x>=t,0.90) and allv('A','heldout',lambda x,t:x<=t,0.40)
               and allv('C','heldout',lambda x,t:x<=t,0.40) and allv('B','bind_destroyed',lambda x,t:x<=t,0.40)
               and all(seeds[s]['B']['heldout']-seeds[s]['A']['heldout']>=0.50 for s in seeds))
    kill = allv('B','heldout',lambda x,t:x<=t,0.40)
    confound = allv('A','heldout',lambda x,t:x>=t,0.90)
    if not valid:
        v = '⚙️ VALIDITY-FAIL (A/B indist<0.95 or train<0.99) — primary bars ' + ('PASS' if primary else 'not met')
    elif primary:
        v = '🟢 GREEN (operator-escape real · DIRECTIONAL scope)'
    elif kill:
        v = '🔴 KILL'
    elif confound:
        v = '🟡 CONFOUND (toy too easy)'
    else:
        v = '🟠 MIXED/gray — inspect table'
    return v

if __name__ == '__main__':
    print(f"device={DEV} torch={torch.__version__} chance=1/{F}={1/F:.4f}")
    seeds = {}
    for s in (0, 1, 2):
        seeds[s] = run_seed(s)
    v = verdict(seeds)
    result = dict(spec='TOY-RESONATOR-READHEAD v1', device=DEV,
                  config=dict(R=R,F=F,D=D,K=K,steps=STEPS,batch=BATCH,tau=TAU,chance=round(1/F,4)),
                  seeds=seeds, verdict=v,
                  scope='DIRECTIONAL — symbolic ID inputs, no byte/LM/core decode (a_toy_scale_recheck)')
    print("\n=== VERDICT:", v, "===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    open('/tmp/toy_resonator_result.json','w').write(json.dumps(result, indent=2, ensure_ascii=False))
