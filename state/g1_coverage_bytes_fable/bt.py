#!/usr/bin/env python3
"""Train byte-LM on one arm's corpus and measure pair-specific recombination.

Arms: high | low | shuffle (see gen_corpus.py). Arch: attn (RF-full, primary) or
convd (dilated depthwise conv, RF~61 bytes -- RF-wall-repaired conv variant).
Metric (pair-specific, avoids v1/v2 traps):
  prompt "\nthe {c1} and the {c2} yield" -> greedy 26 bytes
  strict: generation startswith " {a1} {a2}"   (a = the concept's unique attribute)
  loose : both a1 and a2 appear in generation
Torch mirror => DIRECTIONAL only (not engine-native).
"""
import argparse, json, math, os, random, time
import torch
import torch.nn as nn
import torch.nn.functional as F

ap = argparse.ArgumentParser()
ap.add_argument("--arm", required=True, choices=["high", "low", "shuffle"])
ap.add_argument("--arch", default="attn", choices=["attn", "convd"])
ap.add_argument("--steps", type=int, default=3000)
ap.add_argument("--dim", type=int, default=256)
ap.add_argument("--layers", type=int, default=4)
ap.add_argument("--heads", type=int, default=8)
ap.add_argument("--block", type=int, default=64)
ap.add_argument("--bs", type=int, default=128)
ap.add_argument("--lr", type=float, default=3e-4)
ap.add_argument("--outdir", default=".")
args = ap.parse_args()

torch.manual_seed(0)
random.seed(0)
dev = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", dev, "| arm:", args.arm, "| arch:", args.arch, flush=True)

meta = json.load(open(os.path.join(args.outdir, "meta.json")))
raw = open(os.path.join(args.outdir, "corpus_%s.txt" % args.arm), "rb").read()
buf = torch.frombuffer(bytearray(raw), dtype=torch.uint8).long()
print("corpus bytes:", len(buf), flush=True)

class SelfAttn(nn.Module):
    def __init__(self, d, h):
        super().__init__()
        self.h = h
        self.qkv = nn.Linear(d, 3 * d)
        self.proj = nn.Linear(d, d)
    def forward(self, x):
        B, T, D = x.shape
        q, k, v = self.qkv(x).split(D, dim=2)
        def sh(t):
            return t.view(B, T, self.h, D // self.h).transpose(1, 2)
        y = F.scaled_dot_product_attention(sh(q), sh(k), sh(v), is_causal=True)
        return self.proj(y.transpose(1, 2).contiguous().view(B, T, D))

class CausalConv(nn.Module):
    def __init__(self, d, K, dil):
        super().__init__()
        self.pad = (K - 1) * dil
        self.conv = nn.Conv1d(d, d, K, dilation=dil, groups=d)
        self.pw = nn.Linear(d, d)
    def forward(self, x):
        y = F.pad(x.transpose(1, 2), (self.pad, 0))
        y = self.conv(y).transpose(1, 2)
        return self.pw(F.gelu(y))

class Block(nn.Module):
    def __init__(self, d, h, arch, i):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.mix = SelfAttn(d, h) if arch == "attn" else CausalConv(d, 5, [1, 2, 4, 8][i % 4])
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))
    def forward(self, x):
        x = x + self.mix(self.ln1(x))
        return x + self.mlp(self.ln2(x))

class LM(nn.Module):
    def __init__(self):
        super().__init__()
        d = args.dim
        self.emb = nn.Embedding(256, d)
        self.pos = nn.Embedding(args.block, d)
        self.blocks = nn.ModuleList([Block(d, args.heads, args.arch, i) for i in range(args.layers)])
        self.lnf = nn.LayerNorm(d)
        self.head = nn.Linear(d, 256)
    def forward(self, idx):
        T = idx.shape[1]
        x = self.emb(idx) + self.pos(torch.arange(T, device=idx.device))
        for b in self.blocks:
            x = b(x)
        return self.head(self.lnf(x))

model = LM().to(dev)
nparam = sum(p.numel() for p in model.parameters())
print("params:", nparam, flush=True)
opt = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=0.01)

def lr_at(step):
    warm = 100
    if step < warm:
        return args.lr * (step + 1) / warm
    t = (step - warm) / max(1, args.steps - warm)
    return args.lr * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * t)))

def get_batch():
    ix = torch.randint(0, len(buf) - args.block - 1, (args.bs,))
    x = torch.stack([buf[i:i + args.block] for i in ix])
    y = torch.stack([buf[i + 1:i + args.block + 1] for i in ix])
    return x.to(dev), y.to(dev)

@torch.no_grad()
def gen_greedy(prompt, n=26):
    idx = torch.tensor([list(prompt.encode())], dtype=torch.long, device=dev)
    for _ in range(n):
        logits = model(idx[:, -args.block:])
        nxt = logits[0, -1].argmax().view(1, 1)
        idx = torch.cat([idx, nxt], dim=1)
    return bytes(idx[0, -n:].tolist()).decode("latin1")

attr = meta["attr"]
@torch.no_grad()
def eval_pairs(pairs, targets=None, tag=""):
    model.eval()
    strict = loose = 0
    samples = []
    for j, (c1, c2) in enumerate(pairs):
        a1, a2 = (attr[c1], attr[c2]) if targets is None else targets[j]
        g = gen_greedy("\nthe %s and the %s yield" % (c1, c2))
        s = g.startswith(" %s %s" % (a1, a2))
        l = (a1 in g) and (a2 in g)
        strict += s
        loose += l
        if j < 5:
            samples.append("%s+%s -> want(%s %s) got%r" % (c1, c2, a1, a2, g))
    model.train()
    n = float(len(pairs))
    print("[eval %s] strict=%.3f loose=%.3f (n=%d)" % (tag, strict / n, loose / n, len(pairs)), flush=True)
    for s in samples:
        print("   ", s, flush=True)
    return strict / n, loose / n

seen_pairs = [tuple(p) for p in meta["seen_eval"][args.arm]]
held_pairs = [tuple(p) for p in meta["held"]]
sh_targets = None
if args.arm == "shuffle":
    sh_targets = [tuple(meta["shuffle_map"]["%s|%s" % (c1, c2)]) for (c1, c2) in seen_pairs]

t0 = time.time()
for step in range(args.steps):
    for g in opt.param_groups:
        g["lr"] = lr_at(step)
    x, y = get_batch()
    loss = F.cross_entropy(model(x).view(-1, 256), y.view(-1))
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()
    if step % 250 == 0 or step == args.steps - 1:
        print("step %d loss %.4f lr %.2e %.0fs" % (step, loss.item(), lr_at(step), time.time() - t0), flush=True)
    if (step + 1) % 1000 == 0:
        eval_pairs(seen_pairs, tag="seen-true@%d" % (step + 1))
        eval_pairs(held_pairs, tag="held@%d" % (step + 1))

res = {"arm": args.arm, "arch": args.arch, "steps": args.steps, "params": nparam,
       "final_loss": loss.item(), "directional": True, "device": dev}
res["seen_true_strict"], res["seen_true_loose"] = eval_pairs(seen_pairs, tag="FINAL seen-true")
res["held_strict"], res["held_loose"] = eval_pairs(held_pairs, tag="FINAL held")
if sh_targets is not None:
    res["seen_shuffled_strict"], res["seen_shuffled_loose"] = eval_pairs(
        seen_pairs, targets=sh_targets, tag="FINAL seen-shuffled-target")
with open(os.path.join(args.outdir, "results_%s_%s.json" % (args.arch, args.arm)), "w") as f:
    json.dump(res, f, indent=1)
print(json.dumps(res), flush=True)
print("=== DONE %s %s ===" % (args.arch, args.arm), flush=True)
