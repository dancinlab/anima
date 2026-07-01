#!/usr/bin/env python3
"""H_1840 gamma HRR constructive-bind — CHEAP-GATE $0 mechanism screen (DIRECTIONAL).

4-arm 2-leg held-out conjunction retrieval. Pre-registered bar in FREEZE_toy.md.
numpy/torch mirror => DIRECTIONAL only (a_engine_native_learning). This gates the GPU fire:
PASS => authorize ~1 H100-day engine-native run; FAIL => do not spend, honest negative.

Uses torch on the pool host purely for autograd of a tiny bilinear model (CPU, seconds).
"""
import argparse, json, math
import torch
import torch.nn.functional as F

D = 64
NA = 10
NB = 10
NC = NA * NB
TEMP = 0.07
STEPS = 3000
LR = 5e-3


def circ_conv(u, v):
    """Circular convolution via FFT: invertible HRR binding (Plate 1995)."""
    U = torch.fft.rfft(u, dim=-1)
    V = torch.fft.rfft(v, dim=-1)
    return torch.fft.irfft(U * V, n=u.shape[-1], dim=-1)


def circ_conv_freqmasked(u, v, mask):
    """Non-invertible ablation: same bilinear bottleneck but half the frequencies are
    zeroed by a FIXED 0/1 mask before iFFT => information destroyed, cannot unbind.
    Isolates INVERTIBILITY as the load-bearing property (bottleneck identical to (c))."""
    U = torch.fft.rfft(u, dim=-1)
    V = torch.fft.rfft(v, dim=-1)
    return torch.fft.irfft((U * V) * mask, n=u.shape[-1], dim=-1)


def build_task(seed):
    g = torch.Generator().manual_seed(seed)
    A = F.normalize(torch.randn(NA, D, generator=g), dim=-1)
    B = F.normalize(torch.randn(NB, D, generator=g), dim=-1)
    # ground-truth composite keys = HRR binding of atoms (retrieval candidates)
    K = torch.stack([circ_conv(A[i], B[j]) for i in range(NA) for j in range(NB)])
    K = F.normalize(K, dim=-1)  # [NC, D]
    # split combos: 70% train / 30% held-out, every atom covered in train
    pairs = [(i, j) for i in range(NA) for j in range(NB)]
    perm = torch.randperm(NC, generator=g).tolist()
    n_tr = int(round(0.70 * NC))
    tr_idx = set(perm[:n_tr])
    # guarantee coverage: force the diagonal-ish first occurrence of each atom into train
    covered_a, covered_b = set(), set()
    for idx in list(tr_idx):
        i, j = pairs[idx]
        covered_a.add(i); covered_b.add(j)
    for idx in perm:
        i, j = pairs[idx]
        if i not in covered_a or j not in covered_b:
            tr_idx.add(idx); covered_a.add(i); covered_b.add(j)
    ho_idx = [idx for idx in range(NC) if idx not in tr_idx]
    tr_idx = sorted(tr_idx)
    return A, B, K, pairs, tr_idx, ho_idx


class Arm(torch.nn.Module):
    def __init__(self, arm, seed):
        super().__init__()
        g = torch.Generator().manual_seed(seed + 999)
        self.arm = arm
        self.Wa = torch.nn.Parameter(0.3 * torch.randn(D, D, generator=g))
        self.Wb = torch.nn.Parameter(0.3 * torch.randn(D, D, generator=g))
        if arm == "hadamard_bypass":
            self.Sa = torch.nn.Parameter(0.3 * torch.randn(D, D, generator=g))
            self.Sb = torch.nn.Parameter(0.3 * torch.randn(D, D, generator=g))
        if arm == "noninv_bottleneck":
            nf = D // 2 + 1
            gm = torch.Generator().manual_seed(seed + 7)
            m = (torch.rand(nf, generator=gm) > 0.5).float()  # zero ~half freqs
            m[0] = 1.0
            self.register_buffer("mask", m)

    def query(self, ea, eb):
        u = ea @ self.Wa.T
        v = eb @ self.Wb.T
        if self.arm == "additive":
            return u + v
        if self.arm == "hadamard_bypass":
            skip = ea @ self.Sa.T + eb @ self.Sb.T
            return u * v + skip
        if self.arm == "hrr_bottleneck":
            return circ_conv(u, v)
        if self.arm == "noninv_bottleneck":
            return circ_conv_freqmasked(u, v, self.mask)
        raise ValueError(self.arm)


def run_arm(arm, seed, A, B, K, pairs, tr_idx, ho_idx):
    model = Arm(arm, seed)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    tr = torch.tensor(tr_idx)
    ea_tr = torch.stack([A[pairs[k][0]] for k in tr_idx])
    eb_tr = torch.stack([B[pairs[k][1]] for k in tr_idx])
    y_tr = tr
    for step in range(STEPS):
        opt.zero_grad(set_to_none=True)
        q = model.query(ea_tr, eb_tr)
        q = F.normalize(q, dim=-1)
        logits = (q @ K.T) / TEMP
        loss = F.cross_entropy(logits, y_tr)
        loss.backward()
        opt.step()

    def acc(idxs):
        if not idxs:
            return float("nan")
        idxs = list(idxs)
        ea = torch.stack([A[pairs[k][0]] for k in idxs])
        eb = torch.stack([B[pairs[k][1]] for k in idxs])
        with torch.no_grad():
            q = F.normalize(model.query(ea, eb), dim=-1)
            pred = ((q @ K.T)).argmax(-1)
        return float((pred == torch.tensor(idxs)).float().mean())

    return {"train_acc": round(acc(tr_idx), 4),
            "heldout_acc": round(acc(ho_idx), 4),
            "final_ce": round(float(loss), 5)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=[7, 4302, 4303])
    ap.add_argument("--out", default="toy_result.json")
    a = ap.parse_args()
    arms = ["additive", "hadamard_bypass", "hrr_bottleneck", "noninv_bottleneck"]
    results = {}
    print(f"=== H_1840 cheap-gate toy | chance heldout={1/NC:.4f} | seeds={a.seeds} ===",
          flush=True)
    for seed in a.seeds:
        torch.manual_seed(seed)
        A, B, K, pairs, tr_idx, ho_idx = build_task(seed)
        results[seed] = {}
        print(f"\n-- seed {seed} | train={len(tr_idx)} heldout={len(ho_idx)} --", flush=True)
        for arm in arms:
            r = run_arm(arm, seed, A, B, K, pairs, tr_idx, ho_idx)
            results[seed][arm] = r
            print(f"   {arm:20s} train_acc={r['train_acc']:.3f} "
                  f"heldout_acc={r['heldout_acc']:.3f} ce={r['final_ce']:.4f}", flush=True)

    # frozen-bar evaluation
    def seed_pass(rs):
        c = rs["hrr_bottleneck"]["heldout_acc"]
        floors = [rs["additive"]["heldout_acc"], rs["hadamard_bypass"]["heldout_acc"],
                  rs["noninv_bottleneck"]["heldout_acc"]]
        train_ok = all(rs[a2]["train_acc"] >= 0.95 for a2 in rs)
        return (c >= 0.50) and (c > 3 * max(floors)) and train_ok, c, max(floors), train_ok

    n_pass = 0
    print("\n=== FROZEN-BAR verdict (per-seed) ===", flush=True)
    for seed in a.seeds:
        ok, c, mf, tok = seed_pass(results[seed])
        n_pass += int(ok)
        print(f"   seed {seed}: c_heldout={c:.3f} max_floor={mf:.3f} "
              f"train>=.95:{tok} => {'PASS' if ok else 'FAIL'}", flush=True)
    verdict = "PASS" if n_pass >= 2 else "FAIL"
    print(f"\n=== TOY GATE: {verdict}  ({n_pass}/{len(a.seeds)} seeds pass) ===", flush=True)
    print(f"=== GPU-fire authorized: {verdict == 'PASS'} ===", flush=True)
    out = {"results": results, "n_pass": n_pass, "n_seeds": len(a.seeds),
           "verdict": verdict, "gpu_authorized": verdict == "PASS",
           "chance": 1 / NC, "bar": "c>=0.50 AND c>3*max_floor AND all train>=0.95, >=2/3 seeds"}
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {a.out}", flush=True)


if __name__ == "__main__":
    main()
