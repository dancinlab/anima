#!/usr/bin/env python3
"""H_6162 HE-AS-OBJECTIVE fair cheap-gate (FROZEN 2026-07-02, see FREEZE.md).
Does a target-agnostic homomorphism-error aux loss lift held-out compositional
generalization vs plain CE? torch mirror = DIRECTIONAL. tune-to-green forbidden."""
import json, sys, math
import numpy as np
import torch, torch.nn as nn, torch.nn.functional as F

# ---- frozen hyperparams ----
NF, E, C = 6, 4, 9          # factors/slot, entities/factor, classes
D, H = 96, 192
STEPS, BS, LR = 4000, 256, 2e-3
LAMBDAS = [0.0, 0.3, 1.0, 3.0]   # 0.0 = OFF baseline
SEEDS = [7, 4302, 4303]
HELDOUT_FRAC = 0.22

def make_task(seed):
    g = np.random.default_rng(seed)
    T = g.integers(0, C, size=(NF, NF))            # random non-additive target table
    combos = [(a, b) for a in range(NF) for b in range(NF)]
    g.shuffle(combos)
    nho = round(len(combos) * HELDOUT_FRAC)
    held = set(combos[:nho]); seen = [c for c in combos if c not in held]
    # every factor must appear in SEEN (so held-out = unseen pairing of seen factors)
    fa_seen = {a for a, _ in seen}; fb_seen = {b for _, b in seen}
    assert fa_seen == set(range(NF)) and fb_seen == set(range(NF)), "refactor split"
    return T, seen, sorted(held)

def sample(combolist, T, rng, n):
    fa = np.array([c[0] for c in combolist]); fb = np.array([c[1] for c in combolist])
    idx = rng.integers(0, len(combolist), size=n)
    A_f, B_f = fa[idx], fb[idx]
    # surface token = factor*E + random entity  (abstract factor from token)
    A_tok = A_f * E + rng.integers(0, E, size=n)
    B_tok = B_f * E + rng.integers(0, E, size=n)
    y = T[A_f, B_f]
    return (torch.tensor(A_tok), torch.tensor(B_tok), torch.tensor(y))

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        V = NF * E
        self.ea = nn.Embedding(V, D); self.eb = nn.Embedding(V, D)
        self.part = nn.Sequential(nn.Linear(D, H), nn.GELU(), nn.Linear(H, D))
        self.pair = nn.Sequential(nn.Linear(2*D, H), nn.GELU(), nn.Linear(H, D))
        self.readout = nn.Linear(D, C)
        # g: target-blind learned composition of part-reps (bilinear feature + MLP)
        self.g = nn.Sequential(nn.Linear(3*D, H), nn.GELU(), nn.Linear(H, D))
    def parts(self, at, bt):
        return self.part(self.ea(at)), self.part(self.eb(bt))
    def forward(self, at, bt):
        ra, rb = self.parts(at, bt)
        h = self.pair(torch.cat([ra, rb], -1))
        return self.readout(h), h, ra, rb
    def he(self, ra, rb):
        return self.g(torch.cat([ra, rb, ra*rb], -1))

def run(seed, lam, T, seen, held):
    torch.manual_seed(seed); np.random.seed(seed)
    rng = np.random.default_rng(1000+seed)
    net = Net(); opt = torch.optim.Adam(net.parameters(), lr=LR)
    for step in range(STEPS):
        at, bt, y = sample(seen, T, rng, BS)
        logits, h, ra, rb = net(at, bt)
        loss = F.cross_entropy(logits, y)
        if lam > 0:
            g = net.he(ra, rb)
            loss = loss + lam * F.mse_loss(h, g)   # both h and g trainable (An&Du homomorphism prior)
        opt.zero_grad(); loss.backward(); opt.step()
    net.eval()
    def acc(combolist, n=4096):
        at, bt, y = sample(combolist, T, rng, n)
        with torch.no_grad():
            pred = net(at, bt)[0].argmax(-1)
        return (pred == y).float().mean().item()
    return {"train_acc": round(acc(seen), 4), "heldout_acc": round(acc(held), 4)}

def main():
    out = {"frozen": "FREEZE.md", "chance": round(1.0/C, 4), "seeds": {}}
    for s in SEEDS:
        T, seen, held = make_task(s)
        out["seeds"][str(s)] = {"n_seen": len(seen), "n_held": len(held), "arms": {}}
        for lam in LAMBDAS:
            r = run(s, lam, T, seen, held)
            out["seeds"][str(s)]["arms"][f"lam_{lam}"] = r
            print(f"seed={s} lam={lam}: train={r['train_acc']} held={r['heldout_acc']}", flush=True)
    # frozen bar
    verdict = {}
    per_seed = []
    for s in SEEDS:
        arms = out["seeds"][str(s)]["arms"]
        off = arms["lam_0.0"]["heldout_acc"]
        on_best = max(arms[f"lam_{l}"]["heldout_acc"] for l in LAMBDAS if l > 0)
        per_seed.append({"seed": s, "off": off, "on_best": on_best, "delta": round(on_best-off, 4)})
    n_ge = sum(1 for p in per_seed if p["delta"] >= 0.15)
    no_regress = all(p["on_best"] >= p["off"] for p in per_seed)
    train_ok = all(out["seeds"][str(s)]["arms"][f"lam_{l}"]["train_acc"] >= 0.90
                   for s in SEEDS for l in LAMBDAS)
    off_learns = all(p["off"] > out["chance"] + 0.05 for p in per_seed)
    if not (train_ok and off_learns):
        tier = "INCONCLUSIVE (sanity gate fail — undertrained or task not learnable)"
    elif n_ge >= 2 and no_regress:
        tier = "DIRECTIONAL-SUPPORT (>=+0.15 on >=2/3 seeds, no regress) — engine-native GPU authorized"
    else:
        tier = "🧱 DIRECTIONAL-FLOOR (NOT-SUPPORTED) — HE-objective does not lift held-out composition"
    verdict = {"per_seed": per_seed, "n_delta_ge_0.15": n_ge, "no_regress": no_regress,
               "train_ok": train_ok, "off_learns": off_learns, "tier": tier}
    out["verdict"] = verdict
    json.dump(out, open("result.json", "w"), indent=2)
    print("\n=== VERDICT ===")
    for p in per_seed: print(p)
    print("TIER:", tier)

if __name__ == "__main__":
    main()
