#!/usr/bin/env python3
"""A11 = TPR forward-slot (multiplicative) x contrastive-replace objective (H_9121).

The ONE open escape cell. E1 (contrastive on ADD/no-slot arch) = AT-FLOOR (5/5,
margin -0.47). E2 / engine-native H_1813 (TPR under CE) = FLOOR. A11 combines the
TPR multiplicative binding slot WITH the contrastive-replace (non-CE) objective.

SCALE-TRANSFER TEST (a_toy_scale_recheck):
  The E1/E2 TOYs used a FREE LOOKUP table C[filler] (24 concepts, D=96). The task's
  own warning (E2 precedent: TPR toy unbind 1.0 -> real CE 0.022) is that toy
  reachability can overstate. This script REPLACES the free lookup with a REAL DEEP
  CONV BYTE TRUNK (the production CLMConvMoE E=2/L1 encoder, inlined). Each filler is
  a distinct multi-byte string; C[filler] = pooled trunk encoding of that byte string.
  The trunk is trained END-TO-END by the contrastive-replace objective (no CE). This
  isolates the SCALE variable: does a real deep conv byte-trunk representation still
  compose under TPR + contrastive on HELD-OUT (novel) filler pairs, or does the deep
  representation entangle (floor) the way a real trunk does under CE?

  ADD vs TPR are trained under the SAME contrastive-replace objective on the SAME
  trunk. ADD = additive readout (no binding slot, = E1 arch). TPR = role-filler
  tensor product (multiplicative slot, = A11).

SCOPE (honest, c9): torch, NOT live core/ decode -> DIRECTIONAL by a_engine_native_
learning. A clean SYNTHETIC compositional corpus, not the natural byte corpus. This
does NOT cement a tier; engine-native (TPR slot wired into core/clm_decode.hexa +
serializer, scored via `anima evaluate --py`) is the terminal follow-on. This answers
ONLY: does A11's toy reachability survive a real deep conv byte trunk?

FROZEN G1 BAR (pre-registered, NOT moved): a seed HITs iff on held-out pairs
  reach_novel (cov==2 AND cov>max_single) >= 0.5  AND  margin > 0  AND  SCRAMBLE <= 0.2.
  >=4/5 seeds HIT -> A11 DIRECTIONAL-REACHABLE (escalate to engine-native).
  <4/5 -> A11 FALSIFIED-DIRECTIONAL (swallowed even on a real trunk).
"""
from __future__ import annotations
import argparse, json, time, sys
import torch, torch.nn as nn, torch.nn.functional as F

# ----------------------------------------------------------------- conv trunk
# Inlined minimal CLMConvMoE trunk (byte encoder) = archive/train/clm/model/model.py
# E=2 experts, L=1 trunk layer, variant AB. Same operators (causal dilated conv +
# GroupNorm + GELU + conv-MoE), used as a sequence encoder (we pool the last position).
class CausalDilatedConv1d(nn.Module):
    def __init__(self, ch, k, dil):
        super().__init__()
        self.pad = (k - 1) * dil
        self.conv = nn.Conv1d(ch, ch, k, dilation=dil)
    def forward(self, x):
        return self.conv(F.pad(x, (self.pad, 0)))

class TrunkLayer(nn.Module):
    def __init__(self, d, k, dil):
        super().__init__()
        self.conv = CausalDilatedConv1d(d, k, dil)
        self.norm = nn.GroupNorm(1, d); self.act = nn.GELU()
    def forward(self, x):
        return x + self.act(self.norm(self.conv(x)))

class ConvExpert(nn.Module):
    def __init__(self, d, k):
        super().__init__()
        self.conv = CausalDilatedConv1d(d, k, 1); self.act = nn.GELU()
    def forward(self, x):
        return self.act(self.conv(x))

class MoEConvLayer(nn.Module):
    def __init__(self, d, n_e, k):
        super().__init__()
        self.experts = nn.ModuleList(ConvExpert(d, k) for _ in range(n_e))
        self.router = nn.Conv1d(d, n_e, 1)
    def forward(self, x):
        probs = F.softmax(self.router(x), dim=1)            # (B,n_e,T)
        ex = torch.stack([e(x) for e in self.experts], 1)   # (B,n_e,C,T)
        return (probs.unsqueeze(2) * ex).sum(1)             # (B,C,T)

class ConvTrunk(nn.Module):
    """Byte trunk encoder: bytes -> (B,C,T) hidden; caller pools last pos."""
    def __init__(self, d, n_e=2, L=1, k=3, V=256):
        super().__init__()
        self.embed = nn.Embedding(V, d)
        self.embed_conv = CausalDilatedConv1d(d, k, 1)
        self.trunk = nn.ModuleList(TrunkLayer(d, k, min(2**i, 512)) for i in range(L))
        self.moe = MoEConvLayer(d, n_e, k)
        self.norm_out = nn.GroupNorm(1, d)
    def forward(self, tok):                 # tok: (B,T) long
        x = self.embed(tok).transpose(1, 2) # (B,C,T)
        x = self.embed_conv(x)
        for layer in self.trunk:
            x = layer(x)
        x = self.moe(x)
        return self.norm_out(x)             # (B,C,T)
    def encode(self, tok):                  # pooled last-position code
        return self.forward(tok)[:, :, -1]  # (B,C)

# ----------------------------------------------------------------- A11 model
class A11Model(nn.Module):
    """Real conv byte trunk -> C[filler]; ADD or TPR readout; signature embeds S.
    role vectors = fixed orthonormal (R=2). Energy of a length-2 sig sequence:
      ADD: h = C[a]+C[b];  E([k1,k2]) = -(S[k1].h + S[k2].h)
      TPR: c_j = C[a]*roles[0,j] + C[b]*roles[1,j];  E = -(S[k1].c0 + S[k2].c1)
    Trunk + S trained END-TO-END by contrastive-replace (InfoNCE), NO CE."""
    def __init__(self, d, n_fill, arch, n_e=2, L=1, k=3):
        super().__init__()
        self.trunk = ConvTrunk(d, n_e, L, k)
        self.S = nn.Parameter(torch.randn(n_fill, d) * 0.3)   # signature (readout) embeds
        self.arch = arch
        self.register_buffer("roles", torch.eye(2))
        self.d = d; self.n_fill = n_fill
    def code(self, filler_bytes):    # (n_fill, Lbytes) -> (n_fill, d)
        return self.trunk.encode(filler_bytes)
    def energy(self, C, a, b, k1, k2):
        if self.arch == "ADD":
            h = C[a] + C[b]
            return -(self.S[k1] @ h + self.S[k2] @ h)
        else:  # TPR
            c0 = C[a] * self.roles[0, 0] + C[b] * self.roles[1, 0]
            c1 = C[a] * self.roles[0, 1] + C[b] * self.roles[1, 1]
            return -(self.S[k1] @ c0 + self.S[k2] @ c1)
    def logits_for(self, C, a, b, cands):
        return torch.stack([-self.energy(C, a, b, k1, k2) for (k1, k2) in cands])

# ----------------------------------------------------------------- data
def build_corpus(n_fill, held_frac, byte_len, rng):
    # each filler = distinct random byte string (bytes 1..255), forcing the conv
    # trunk to integrate multiple bytes to identify the filler (real trunk work).
    fbytes = torch.zeros(n_fill, byte_len, dtype=torch.long)
    used = set()
    for i in range(n_fill):
        while True:
            s = tuple(int(x) for x in rng.integers(1, 256, byte_len))
            if s not in used:
                used.add(s); break
        fbytes[i] = torch.tensor(s)
    pairs = [(a, b) for a in range(n_fill) for b in range(n_fill) if a != b]
    rng.shuffle(pairs)
    n_held = int(len(pairs) * held_frac)
    held = set(map(tuple, pairs[:n_held]))
    seen = [p for p in pairs if p not in held]
    return fbytes, seen, sorted(held)

def negs(a, b, n_fill, rng):
    d = int(rng.integers(n_fill))
    while d in (a, b):
        d = int(rng.integers(n_fill))
    return [(a, a), (b, b), (a, d)]      # echo-A, echo-B, wrong-D

# ----------------------------------------------------------------- train / eval
def train_eval(arch, d, n_fill, seen, held, fbytes, device, rng, epochs, lr, tau):
    m = A11Model(d, n_fill, arch).to(device)
    fb = fbytes.to(device)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.01)
    for ep in range(epochs):
        order = list(seen); rng.shuffle(order)
        C = m.code(fb)                                   # (n_fill,d) grad-through trunk
        opt.zero_grad(set_to_none=True)
        loss = 0.0
        for (a, b) in order:
            cands = [(a, b)] + negs(a, b, n_fill, rng)
            lg = m.logits_for(C, a, b, cands) / tau
            loss = loss + F.cross_entropy(lg.unsqueeze(0), torch.zeros(1, dtype=torch.long, device=device))
        loss = loss / len(order)
        loss.backward(); opt.step()
        if ep % max(1, epochs // 4) == 0 or ep == epochs - 1:
            print(f"    [{arch}] ep{ep:4d} infoNCE={float(loss):.4f}", flush=True)
    # ---- eval on held-out (frozen G1 bar) ----
    m.eval()
    with torch.no_grad():
        C = m.code(fb)
        margins, reach2, reach_novel, scr = [], 0, 0, 0
        def decode(a, b):
            # argmin-energy over shortlist alphabet (present + random distractors)
            alpha = list({a, b} | set(int(x) for x in rng.integers(0, n_fill, 6)))
            best, bE = None, 1e30
            for k1 in alpha:
                for k2 in alpha:
                    e = float(m.energy(C, a, b, k1, k2))
                    if e < bE: bE, best = e, (k1, k2)
            return best
        cov = lambda dec, pres: len(set(dec) & set(pres))
        for (a, b) in held:
            e_bound = float(m.energy(C, a, b, a, b))
            e_echo = min(float(m.energy(C, a, b, a, a)), float(m.energy(C, a, b, b, b)))
            margins.append(e_echo - e_bound)
            dec = decode(a, b); c = cov(dec, (a, b))
            ms = max(cov(decode(a, a), (a,)), cov(decode(b, b), (b,)))
            if c == 2:
                reach2 += 1
                if c > ms: reach_novel += 1
            ra, rb = int(rng.integers(n_fill)), int(rng.integers(n_fill))
            if cov(decode(ra, rb), (a, b)) == 2: scr += 1
    n = len(held)
    return dict(margin=float(sum(margins)/n), reach2=reach2/n,
                reach_novel=reach_novel/n, scramble=scr/n,
                params=sum(p.numel() for p in m.parameters()))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=int, default=768)
    ap.add_argument("--n-fill", type=int, default=24)
    ap.add_argument("--byte-len", type=int, default=4)
    ap.add_argument("--held-frac", type=float, default=0.20)
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--tau", type=float, default=1.0)
    ap.add_argument("--seeds", type=str, default="7,11,23,42,101")
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    import numpy as np
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"=== A11 SCALED: TPR-slot x contrastive-replace on REAL conv byte trunk ===")
    print(f"device={device} d={a.d} n_fill={a.n_fill} byte_len={a.byte_len} "
          f"epochs={a.epochs} lr={a.lr} tau={a.tau}", flush=True)
    seeds = [int(s) for s in a.seeds.split(",")]
    rows = []
    for sd in seeds:
        torch.manual_seed(sd)
        rng = np.random.default_rng(sd)
        fbytes, seen, held = build_corpus(a.n_fill, a.held_frac, a.byte_len, rng)
        print(f"\n--- seed {sd} (train={len(seen)} held={len(held)}) ---", flush=True)
        r_add = train_eval("ADD", a.d, a.n_fill, seen, held, fbytes, device, rng, a.epochs, a.lr, a.tau)
        r_tpr = train_eval("TPR", a.d, a.n_fill, seen, held, fbytes, device, rng, a.epochs, a.lr, a.tau)
        tpr_hit = (r_tpr["reach_novel"] >= 0.5) and (r_tpr["margin"] > 0) and (r_tpr["scramble"] <= 0.2)
        add_hit = (r_add["reach_novel"] >= 0.5) and (r_add["margin"] > 0) and (r_add["scramble"] <= 0.2)
        print(f"  ADD margin={r_add['margin']:+.4f} reach_novel={r_add['reach_novel']:.2f} "
              f"scr={r_add['scramble']:.2f}  {'HIT' if add_hit else 'floor'}")
        print(f"  TPR margin={r_tpr['margin']:+.4f} reach_novel={r_tpr['reach_novel']:.2f} "
              f"scr={r_tpr['scramble']:.2f}  {'HIT' if tpr_hit else 'floor'}  params={r_tpr['params']/1e6:.2f}M", flush=True)
        rows.append(dict(seed=sd, add=r_add, tpr=r_tpr, add_hit=add_hit, tpr_hit=tpr_hit))
    tpr_hits = sum(r["tpr_hit"] for r in rows)
    add_hits = sum(r["add_hit"] for r in rows)
    verdict = "DIRECTIONAL-REACHABLE" if tpr_hits >= 4 else "FALSIFIED-DIRECTIONAL"
    print(f"\n=== A11 RESULT (frozen bar: reach_novel>=0.5 AND margin>0 AND scramble<=0.2) ===")
    print(f"TPR (A11)  HIT {tpr_hits}/{len(seeds)}   ADD (E1 ctrl) HIT {add_hits}/{len(seeds)}")
    print(f"params={rows[0]['tpr']['params']/1e6:.2f}M  d={a.d}")
    print(f"VERDICT: A11 = {verdict}  (torch DIRECTIONAL; engine-native = follow-on)")
    out = dict(d=a.d, n_fill=a.n_fill, byte_len=a.byte_len, epochs=a.epochs,
               seeds=seeds, rows=rows, tpr_hits=tpr_hits, add_hits=add_hits,
               params=rows[0]['tpr']['params'], verdict=verdict, scope="torch-DIRECTIONAL")
    if a.json_out:
        with open(a.json_out, "w") as f: json.dump(out, f, indent=2)
    print("JSON " + json.dumps({k: out[k] for k in ("d","params","tpr_hits","add_hits","verdict")}))

if __name__ == "__main__":
    main()
