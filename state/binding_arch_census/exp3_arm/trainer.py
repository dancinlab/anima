#!/usr/bin/env python3
"""EXP-3 ARM-BIND (H_1603/H_1617) — DIRECTIONAL toy (torch, engine-native 아님).
Does a multiplicative (Hadamard) binding op in a learned byte-LM trunk cross the
binding-required recombination split that an additive readout cannot?

3 arms (same trunk, readout differs): CTRL (plain linear) · BIND (Hadamard) ·
BIND-LINEAR (param-matched, multiply->add ablation). seeds {7,4302,4303}.
Frozen bars in PREREG.md — DO NOT tune to green. See SCREEN_multiply_vs_add.md.
"""
import json, time, argparse, math
import numpy as np
import torch, torch.nn as nn

# ---------- vocab / task ----------
S, C, N = 8, 8, 3          # shapes, colors, objects/scene
BOS, SEP, EOS = 0, 1, 2
SH0, CO0 = 3, 3 + S        # shape tokens 3..10, color tokens 11..18
VOCAB = 3 + S + C          # 19
BLOCK = 1 + 2 * N + 4      # BOS | s c s c s c | SEP Qs Qc EOS = 11
def sh(s): return SH0 + s
def co(c): return CO0 + c

def make_heldout(n_hold=12, seed=0):
    """Choose held-out (shape,color) conjunctions; each shape/color held out <=2x
    so every part stays well-seen in OTHER conjunctions (recombination, not OOV)."""
    rng = np.random.default_rng(seed)
    pairs = [(s, c) for s in range(S) for c in range(C)]
    rng.shuffle(pairs)
    held, sh_ct, co_ct = [], {}, {}
    for s, c in pairs:
        if len(held) >= n_hold: break
        if sh_ct.get(s, 0) < 2 and co_ct.get(c, 0) < 2:
            held.append((s, c)); sh_ct[s] = sh_ct.get(s, 0) + 1; co_ct[c] = co_ct.get(c, 0) + 1
    return set(held)

def encode(scene, q):
    toks = [BOS]
    for (s, c) in scene: toks += [sh(s), co(c)]
    toks += [SEP, sh(q[0]), co(q[1]), EOS]
    return toks

def gen_train(n, seen_pairs, data_seed=0):
    """Scenes+query drawn only from SEEN (non-held-out) conjunctions. Balanced label."""
    rng = np.random.default_rng(1000 + data_seed)
    seen = list(seen_pairs)
    X, Y = [], []
    for i in range(n):
        scene = [seen[rng.integers(len(seen))] for _ in range(N)]
        if i % 2 == 0:                                   # label 1: query is in scene
            q = scene[rng.integers(N)]; y = 1
        else:                                            # label 0: query not in scene
            while True:
                q = seen[rng.integers(len(seen))]
                if q not in scene: break
            y = 0
        X.append(encode(scene, q)); Y.append(y)
    return torch.tensor(X), torch.tensor(Y, dtype=torch.float32)

def gen_hard(n, held_pairs, seen_pairs, data_seed=0):
    """binding-required (illusory-conjunction) hard split, balanced.
    query = held-out (Qs,Qc). pos: scene HAS object (Qs,Qc) + distractors carrying
    Qs(other color) & Qc(other shape). neg: scene has Qs(other color) & Qc(other shape)
    SEPARATELY but NOT object (Qs,Qc). pos & neg share identical marginals."""
    rng = np.random.default_rng(2000 + data_seed)
    held = list(held_pairs)
    seen = list(seen_pairs)
    X, Y = [], []
    def other_color(qc):
        while True:
            c = int(rng.integers(C))
            if c != qc: return c
    def other_shape(qs):
        while True:
            s = int(rng.integers(S))
            if s != qs: return s
    made = 0
    while made < n:
        qs, qc = held[rng.integers(len(held))]
        # distractor objects carrying the two legs separately (marginal carriers)
        d1 = (qs, other_color(qc))      # Qs with a different color
        d2 = (other_shape(qs), qc)      # Qc with a different shape
        if made % 2 == 0:               # POSITIVE: real object (qs,qc) present
            scene = [(qs, qc), d1, d2]; y = 1
        else:                           # NEGATIVE: parts present, object absent (illusory)
            scene = [d1, d2, (other_shape(qs), other_color(qc))]; y = 0
            if (qs, qc) in scene: continue
        rng.shuffle(scene)
        X.append(encode(scene, (qs, qc))); Y.append(y); made += 1
    return torch.tensor(X), torch.tensor(Y, dtype=torch.float32)

def gen_full_held(n, held_pairs, data_seed=0):
    """held-out query, random scenes (no marginal control) -> shows marginal-shortcut
    inflation vs the hard split."""
    rng = np.random.default_rng(3000 + data_seed)
    held = list(held_pairs)
    allp = [(s, c) for s in range(S) for c in range(C)]
    X, Y = [], []
    for i in range(n):
        q = held[rng.integers(len(held))]
        scene = [allp[rng.integers(len(allp))] for _ in range(N)]
        if i % 2 == 0 and q not in scene:
            scene[rng.integers(N)] = q
        y = int(q in scene)
        X.append(encode(scene, q)); Y.append(y)
    return torch.tensor(X), torch.tensor(Y, dtype=torch.float32)

# ---------- model ----------
class Trunk(nn.Module):
    def __init__(self, d=256, L=4, heads=4):
        super().__init__()
        self.emb = nn.Embedding(VOCAB, d)
        self.pos = nn.Embedding(BLOCK, d)
        layer = nn.TransformerEncoderLayer(d, heads, dim_feedforward=4 * d,
                                           batch_first=True, activation="gelu")
        self.enc = nn.TransformerEncoder(layer, L)
        self.d = d
        mask = torch.triu(torch.ones(BLOCK, BLOCK) * float("-inf"), diagonal=1)
        self.register_buffer("mask", mask)
    def forward(self, x):
        h = self.emb(x) + self.pos(torch.arange(x.size(1), device=x.device))[None]
        h = self.enc(h, mask=self.mask)
        return h[:, -1]                     # EOS-position hidden, R^d

class Arm(nn.Module):
    def __init__(self, arm, d=256, k=128):
        super().__init__()
        self.trunk = Trunk(d)
        self.arm = arm
        if arm == "ctrl":
            self.head = nn.Linear(d, 1)     # plain additive readout
        else:                               # bind / bind_linear : param-matched
            self.Wa = nn.Linear(d, k); self.Wb = nn.Linear(d, k)
            self.out = nn.Linear(k, 1)
    def forward(self, x):
        h = self.trunk(x)
        if self.arm == "ctrl":
            return self.head(h).squeeze(-1)
        u, v = self.Wa(h), self.Wb(h)
        g = u * v if self.arm == "bind" else u + v   # Hadamard vs add (only diff)
        return self.out(g).squeeze(-1)

def acc(model, X, Y, dev, bs=1024):
    model.eval(); correct = 0
    with torch.no_grad():
        for i in range(0, len(X), bs):
            logit = model(X[i:i+bs].to(dev))
            correct += ((logit > 0).float().cpu() == Y[i:i+bs]).sum().item()
    return correct / len(X)

def train_arm(arm, seed, data, dev, steps=4000, bs=256, lr=3e-4):
    Xtr, Ytr, Xhard, Yhard, Xfull, Yfull, Xhv, Yhv = data
    torch.manual_seed(seed); np.random.seed(seed)
    model = Arm(arm).to(dev)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    lossf = nn.BCEWithLogitsLoss()
    rng = np.random.default_rng(seed)
    model.train()
    for st in range(steps):
        idx = rng.integers(0, len(Xtr), bs)
        xb = Xtr[idx].to(dev); yb = Ytr[idx].to(dev)
        opt.zero_grad(); loss = lossf(model(xb), yb); loss.backward(); opt.step()
    return dict(arm=arm, seed=seed,
                train_acc=round(acc(model, Xtr[:4000], Ytr[:4000], dev), 4),
                heldout_val_acc=round(acc(model, Xhv, Yhv, dev), 4),   # DESCENT integrity
                full_held_acc=round(acc(model, Xfull, Yfull, dev), 4), # marginal-shortcut
                hard_acc=round(acc(model, Xhard, Yhard, dev), 4),      # DECISIVE bar
                final_loss=round(loss.item(), 4)), model

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=4000)
    ap.add_argument("--out", default="state/binding_arch_census/exp3_arm/RESULT.json")
    ap.add_argument("--ckpt_dir", default="state/binding_arch_census/exp3_arm/ckpt")
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"device={dev} torch={torch.__version__} cuda_avail={torch.cuda.is_available()}", flush=True)
    import os; os.makedirs(a.ckpt_dir, exist_ok=True)

    held = make_heldout()                         # SHARED across all arms/seeds (data seed 0)
    allp = set((s, c) for s in range(S) for c in range(C))
    seen = allp - held
    # leakage check: no held-out conjunction appears as object/query in train
    Xtr, Ytr = gen_train(40000, seen)
    Xhard, Yhard = gen_hard(4000, held, seen)     # decisive
    Xfull, Yfull = gen_full_held(4000, held)      # marginal-shortcut contrast
    Xhv, Yhv = gen_train(4000, seen, data_seed=99) # in-distribution val (DESCENT check)
    print(f"held-out conjunctions ({len(held)}): {sorted(held)}", flush=True)
    print(f"train base={float(Ytr.mean()):.3f} hard base={float(Yhard.mean()):.3f} "
          f"full base={float(Yfull.mean()):.3f}", flush=True)
    data = (Xtr, Ytr, Xhard, Yhard, Xfull, Yfull, Xhv, Yhv)

    results = []
    t0 = time.time()
    for arm in ["ctrl", "bind", "bind_linear"]:
        for seed in [7, 4302, 4303]:
            r, model = train_arm(arm, seed, data, dev, steps=a.steps)
            r["wall_s"] = round(time.time() - t0, 1)
            results.append(r)
            torch.save(model.state_dict(), f"{a.ckpt_dir}/{arm}_seed{seed}.pt")
            print(json.dumps(r), flush=True)

    # aggregate + frozen-bar verdict
    def agg(arm, key):
        v = [r[key] for r in results if r["arm"] == arm]
        return round(float(np.mean(v)), 4), round(float(np.std(v)), 4), v
    summ = {}
    for arm in ["ctrl", "bind", "bind_linear"]:
        m, s, v = agg(arm, "hard_acc"); summ[arm] = dict(hard_mean=m, hard_std=s, hard_per_seed=v,
            full_mean=agg(arm, "full_held_acc")[0], val_mean=agg(arm, "heldout_val_acc")[0])
    d_ctrl = round(summ["bind"]["hard_mean"] - summ["ctrl"]["hard_mean"], 4)
    d_lin = round(summ["bind"]["hard_mean"] - summ["bind_linear"]["hard_mean"], 4)
    support = (d_ctrl >= 0.15) and (d_lin >= 0.15)
    # 3/3 consistency: per-seed BIND beats both others by >=0.15
    consist = sum(1 for i in range(3)
                  if summ["bind"]["hard_per_seed"][i] - summ["ctrl"]["hard_per_seed"][i] >= 0.15
                  and summ["bind"]["hard_per_seed"][i] - summ["bind_linear"]["hard_per_seed"][i] >= 0.15)
    verdict = dict(summary=summ, bind_minus_ctrl=d_ctrl, bind_minus_linear=d_lin,
                   bar="BIND-CTRL>=0.15 AND BIND-LINEAR>=0.15 (mean hard_acc)",
                   seed_consistency=f"{consist}/3",
                   VERDICT=("SUPPORT" if support else "NOT-SUPPORTED") + " [DIRECTIONAL toy, engine-native 아님]")
    out = dict(config=dict(S=S, C=C, N=N, block=BLOCK, vocab=VOCAB, steps=a.steps,
                           held_out=sorted(list(held)), device=dev),
               runs=results, verdict=verdict)
    with open(a.out, "w") as f: json.dump(out, f, indent=2)
    print("=" * 60); print(json.dumps(verdict, indent=2)); print("WROTE", a.out, flush=True)

if __name__ == "__main__":
    main()
