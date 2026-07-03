#!/usr/bin/env python3
"""A11 NATURAL-CORPUS transfer test (a_toy_scale_recheck) — follow-on to a11_scaled.py.

a11_scaled.py showed A11 (TPR-slot x contrastive-replace on a REAL deep conv byte
trunk) = DIRECTIONAL-REACHABLE 5/5 with SYNTHETIC fillers = maximally-separated random
4-byte strings. RESULT.md's own honest caveat: "Clean SYNTHETIC compositional corpus,
roles=orthonormal identity ... It does NOT show a natural-corpus byte mouth binds."

THIS script isolates the SINGLE transfer variable RESULT.md flagged: replace the
maximally-separated RANDOM-byte fillers with REAL WORDS drawn from the production 4-cell
natural corpus (ko/en x general/sns). Real words OVERLAP in byte space (shared subwords,
shared scripts, variable length) — the exact property a natural byte mouth must survive.
EVERYTHING ELSE is byte-identical to a11_scaled.py: same A11Model (TPR / ADD readout),
same InfoNCE contrastive-replace objective, same real deep conv byte trunk (CLMConvMoE
E2/L1 d=768), same FROZEN G1 bar, same 5 seeds. Only build_corpus changes.

SCOPE (honest, c9, a_engine_native_learning): torch, NOT live core/ decode -> DIRECTIONAL.
The readout is signature-decode energy over a shortlist, NOT autoregressive mouth
generation, so a HIT here still does NOT flip H_9120 (that needs a .clm trained with the
TPR slot + contrastive-replace, scored via `anima evaluate --py` mouth-generation G1).
This answers ONLY: does the synthetic REACHABLE survive REAL overlapping-word fillers,
or does natural byte-overlap collapse the held-out recombination the way CE-trained
real trunks floor?

FROZEN G1 BAR (verbatim from a11_scaled.py, NOT moved): a seed HITs iff on held-out pairs
  reach_novel (cov==2 AND cov>max_single) >= 0.5  AND  margin > 0  AND  SCRAMBLE <= 0.2.
  >=4/5 seeds HIT -> NATURAL-TRANSFER SURVIVES (DIRECTIONAL; engine-native still terminal).
  <4/5 -> NATURAL-TRANSFER FAILS (synthetic REACHABLE is a clean-corpus artifact).
"""
from __future__ import annotations
import argparse, json, re, sys
import torch, torch.nn as nn, torch.nn.functional as F

# =============== conv trunk (VERBATIM from a11_scaled.py) ======================
class CausalDilatedConv1d(nn.Module):
    def __init__(self, ch, k, dil):
        super().__init__(); self.pad = (k - 1) * dil
        self.conv = nn.Conv1d(ch, ch, k, dilation=dil)
    def forward(self, x): return self.conv(F.pad(x, (self.pad, 0)))
class TrunkLayer(nn.Module):
    def __init__(self, d, k, dil):
        super().__init__(); self.conv = CausalDilatedConv1d(d, k, dil)
        self.norm = nn.GroupNorm(1, d); self.act = nn.GELU()
    def forward(self, x): return x + self.act(self.norm(self.conv(x)))
class ConvExpert(nn.Module):
    def __init__(self, d, k):
        super().__init__(); self.conv = CausalDilatedConv1d(d, k, 1); self.act = nn.GELU()
    def forward(self, x): return self.act(self.conv(x))
class MoEConvLayer(nn.Module):
    def __init__(self, d, n_e, k):
        super().__init__()
        self.experts = nn.ModuleList(ConvExpert(d, k) for _ in range(n_e))
        self.router = nn.Conv1d(d, n_e, 1)
    def forward(self, x):
        probs = F.softmax(self.router(x), dim=1)
        ex = torch.stack([e(x) for e in self.experts], 1)
        return (probs.unsqueeze(2) * ex).sum(1)
class ConvTrunk(nn.Module):
    def __init__(self, d, n_e=2, L=1, k=3, V=256):
        super().__init__()
        self.embed = nn.Embedding(V, d)
        self.embed_conv = CausalDilatedConv1d(d, k, 1)
        self.trunk = nn.ModuleList(TrunkLayer(d, k, min(2**i, 512)) for i in range(L))
        self.moe = MoEConvLayer(d, n_e, k); self.norm_out = nn.GroupNorm(1, d)
    def forward(self, tok):
        x = self.embed(tok).transpose(1, 2); x = self.embed_conv(x)
        for layer in self.trunk: x = layer(x)
        return self.norm_out(self.moe(x))
    def encode(self, tok): return self.forward(tok)[:, :, -1]

class A11Model(nn.Module):
    def __init__(self, d, n_fill, arch, n_e=2, L=1, k=3):
        super().__init__()
        self.trunk = ConvTrunk(d, n_e, L, k)
        self.S = nn.Parameter(torch.randn(n_fill, d) * 0.3)
        self.arch = arch; self.register_buffer("roles", torch.eye(2))
        self.d = d; self.n_fill = n_fill
    def code(self, filler_bytes): return self.trunk.encode(filler_bytes)
    def energy(self, C, a, b, k1, k2):
        if self.arch == "ADD":
            h = C[a] + C[b]; return -(self.S[k1] @ h + self.S[k2] @ h)
        else:
            c0 = C[a]*self.roles[0,0] + C[b]*self.roles[1,0]
            c1 = C[a]*self.roles[0,1] + C[b]*self.roles[1,1]
            return -(self.S[k1] @ c0 + self.S[k2] @ c1)

# =============== NATURAL corpus builder (the ONLY change) ======================
_WORD = re.compile(r"[0-9A-Za-z가-힣一-鿿]+")
def load_words(paths, max_bytes, min_bytes):
    """distinct words (byte-len in [min,max]) from the natural 4-cell corpus."""
    seen, words = set(), []
    for p in paths:
        try:
            txt = open(p, "r", encoding="utf-8", errors="ignore").read()
        except FileNotFoundError:
            continue
        for w in _WORD.findall(txt):
            b = w.encode("utf-8")
            if min_bytes <= len(b) <= max_bytes and w not in seen:
                seen.add(w); words.append(w)
    return words

def build_corpus(words, n_fill, held_frac, max_bytes, rng):
    idx = list(range(len(words))); rng.shuffle(idx)
    chosen = [words[i] for i in idx[:n_fill]]
    fbytes = torch.zeros(n_fill, max_bytes, dtype=torch.long)
    for i, w in enumerate(chosen):
        b = list(w.encode("utf-8"))[:max_bytes]
        fbytes[i, max_bytes-len(b):] = torch.tensor(b, dtype=torch.long)  # left-pad
    pairs = [(a, b) for a in range(n_fill) for b in range(n_fill) if a != b]
    rng.shuffle(pairs)
    n_held = int(len(pairs) * held_frac)
    held = set(map(tuple, pairs[:n_held]))
    seen = [p for p in pairs if p not in held]
    return fbytes, seen, sorted(held), chosen

def negs(a, b, n_fill, rng):
    d = int(rng.integers(n_fill))
    while d in (a, b): d = int(rng.integers(n_fill))
    return [(a, a), (b, b), (a, d)]

def train_eval(arch, d, n_fill, seen, held, fbytes, device, rng, epochs, lr, tau):
    # VECTORIZED training (exact same math as a11_scaled per-pair loop). roles=eye =>
    # TPR energy(a,b,k1,k2) = -(S[k1].C[a] + S[k2].C[b]); ADD = -(S[k1]+S[k2]).(C[a]+C[b]).
    # Both are gathers of PA = S @ C.T (n_fill x n_fill). Byte-equivalent, ~100x faster on CPU.
    m = A11Model(d, n_fill, arch).to(device); fb = fbytes.to(device)
    opt = torch.optim.AdamW(m.parameters(), lr=lr, betas=(0.9,0.95), weight_decay=0.01)
    A = torch.tensor([a for (a, b) in seen], device=device)
    B = torch.tensor([b for (a, b) in seen], device=device)
    def logits(PA, Dvec):
        pa_AA, pa_BB = PA[A, A], PA[B, B]; pa_AB, pa_BA = PA[A, B], PA[B, A]
        pa_DA, pa_DB = PA[Dvec, A], PA[Dvec, B]
        if arch == "TPR":
            pos = pa_AA + pa_BB                       # (a,b)
            n1  = pa_AA + pa_AB                       # (a,a): S[a].C[a]+S[a].C[b]? no: k2=a => S[a].C[b]
            n2  = pa_BA + pa_BB                       # (b,b)
            n3  = pa_AA + pa_DB                       # (a,d)
        else:  # ADD: (S[k1]+S[k2]).(C[a]+C[b])
            pos = pa_AA + pa_AB + pa_BA + pa_BB       # (a,b)
            n1  = 2*(pa_AA + pa_AB)                   # (a,a)
            n2  = 2*(pa_BA + pa_BB)                   # (b,b)
            n3  = pa_AA + pa_AB + pa_DA + pa_DB       # (a,d)
        return torch.stack([pos, n1, n2, n3], dim=1) / tau   # (n_pairs, 4), pos=col0
    for ep in range(epochs):
        C = m.code(fb); PA = m.S @ C.t()
        Dvec = torch.randint(0, n_fill, (len(seen),), device=device)
        coll = (Dvec == A) | (Dvec == B)
        while coll.any():
            Dvec = torch.where(coll, torch.randint(0, n_fill, (len(seen),), device=device), Dvec)
            coll = (Dvec == A) | (Dvec == B)
        lg = logits(PA, Dvec)
        loss = F.cross_entropy(lg, torch.zeros(len(seen), dtype=torch.long, device=device))
        opt.zero_grad(set_to_none=True); loss.backward(); opt.step()
        if ep % max(1, epochs//4) == 0 or ep == epochs-1:
            print(f"    [{arch}] ep{ep:4d} infoNCE={float(loss):.4f}", flush=True)
    m.eval()
    with torch.no_grad():
        C = m.code(fb); margins, reach2, reach_novel, scr = [], 0, 0, 0
        def decode(a, b):
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
    return dict(margin=float(sum(margins)/n), reach2=reach2/n, reach_novel=reach_novel/n,
                scramble=scr/n, params=sum(p.numel() for p in m.parameters()))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=int, default=768)
    ap.add_argument("--n-fill", type=int, default=24)
    ap.add_argument("--max-bytes", type=int, default=12)
    ap.add_argument("--min-bytes", type=int, default=3)
    ap.add_argument("--held-frac", type=float, default=0.20)
    ap.add_argument("--epochs", type=int, default=300)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--tau", type=float, default=1.0)
    ap.add_argument("--seeds", type=str, default="7,11,23,42,101")
    ap.add_argument("--corpus", nargs="+", required=True)
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    import numpy as np, os
    torch.set_num_threads(int(os.environ.get("A11_THREADS", "8")))
    device = "cuda" if torch.cuda.is_available() else "cpu"
    words = load_words(a.corpus, a.max_bytes, a.min_bytes)
    print(f"=== A11 NATURAL: TPR-slot x contrastive-replace, REAL ko/en words ===")
    print(f"device={device} d={a.d} n_fill={a.n_fill} max_bytes={a.max_bytes} "
          f"epochs={a.epochs} lr={a.lr} tau={a.tau} vocab={len(words)} words", flush=True)
    if len(words) < a.n_fill * 3:
        print(f"FATAL: only {len(words)} words < 3*n_fill"); sys.exit(2)
    seeds = [int(s) for s in a.seeds.split(",")]
    rows = []
    for sd in seeds:
        torch.manual_seed(sd); rng = np.random.default_rng(sd)
        fbytes, seen, held, chosen = build_corpus(words, a.n_fill, a.held_frac, a.max_bytes, rng)
        print(f"\n--- seed {sd} (train={len(seen)} held={len(held)}) fillers={chosen[:6]}... ---", flush=True)
        r_add = train_eval("ADD", a.d, a.n_fill, seen, held, fbytes, device, rng, a.epochs, a.lr, a.tau)
        r_tpr = train_eval("TPR", a.d, a.n_fill, seen, held, fbytes, device, rng, a.epochs, a.lr, a.tau)
        tpr_hit = (r_tpr["reach_novel"]>=0.5) and (r_tpr["margin"]>0) and (r_tpr["scramble"]<=0.2)
        add_hit = (r_add["reach_novel"]>=0.5) and (r_add["margin"]>0) and (r_add["scramble"]<=0.2)
        print(f"  ADD margin={r_add['margin']:+.4f} reach_novel={r_add['reach_novel']:.2f} "
              f"scr={r_add['scramble']:.2f}  {'HIT' if add_hit else 'floor'}")
        print(f"  TPR margin={r_tpr['margin']:+.4f} reach_novel={r_tpr['reach_novel']:.2f} "
              f"scr={r_tpr['scramble']:.2f}  {'HIT' if tpr_hit else 'floor'}  params={r_tpr['params']/1e6:.2f}M", flush=True)
        rows.append(dict(seed=sd, add=r_add, tpr=r_tpr, add_hit=add_hit, tpr_hit=tpr_hit, fillers=chosen))
    tpr_hits = sum(r["tpr_hit"] for r in rows); add_hits = sum(r["add_hit"] for r in rows)
    verdict = "NATURAL-TRANSFER-SURVIVES" if tpr_hits >= 4 else "NATURAL-TRANSFER-FAILS"
    print(f"\n=== A11 NATURAL RESULT (frozen bar: reach_novel>=0.5 AND margin>0 AND scramble<=0.2) ===")
    print(f"TPR (A11)  HIT {tpr_hits}/{len(seeds)}   ADD (E1 ctrl) HIT {add_hits}/{len(seeds)}")
    print(f"VERDICT: A11 natural = {verdict}  (torch DIRECTIONAL; engine-native = terminal)")
    out = dict(d=a.d, n_fill=a.n_fill, max_bytes=a.max_bytes, epochs=a.epochs, seeds=seeds,
               rows=rows, tpr_hits=tpr_hits, add_hits=add_hits, params=rows[0]['tpr']['params'],
               verdict=verdict, scope="torch-DIRECTIONAL-natural-corpus", corpus=a.corpus)
    if a.json_out:
        with open(a.json_out, "w") as f: json.dump(out, f, indent=2)
    print("JSON " + json.dumps({k: out[k] for k in ("d","params","tpr_hits","add_hits","verdict")}))

if __name__ == "__main__":
    main()
