#!/usr/bin/env python3
"""H_1840 STAGE-1 FAIR (non-rigged) cheap-gate — bypass-denied bilinear bottleneck screen.

Distinct from PR#2689 RIGGED toy: there the target K=circ_conv(A,B) MATCHED the HRR operator.
Here the target is an operator-AGNOSTIC 2-way latent-interaction table T[fa,fb] over random
class keys — no arm's operator equals T. Pre-registration = FREEZE_fair.md (frozen before run).

torch mirror => DIRECTIONAL only (a_engine_native_learning). Gates the engine-native GPU fire:
PASS => authorize STAGE-2 real trunk co-train; FAIL => honest G1 wall (DPI meta-law), no spend.

Runs 5 arms x 3 seeds on the FAIR target, and the SAME 5 arms on an ADDITIVE-target control
(rig-check: additive structure must let additive arm win & bilinear NOT dominate it).
"""
import argparse, json
import torch
import torch.nn.functional as F

D = 64
NA = 10
NB = 10
NC = NA * NB          # 100 composite (i,j)
P = 5                 # latent factors per leg (2 atoms/class)
C = 9                 # output classes
TEMP = 0.07
STEPS = 4000
LR = 5e-3
ARMS = ["additive", "hadamard_bypass", "hrr_bottleneck", "noninv_bottleneck", "bilinear_bottleneck"]


def circ_conv(u, v):
    U = torch.fft.rfft(u, dim=-1); V = torch.fft.rfft(v, dim=-1)
    return torch.fft.irfft(U * V, n=u.shape[-1], dim=-1)


def circ_conv_freqmasked(u, v, mask):
    U = torch.fft.rfft(u, dim=-1); V = torch.fft.rfft(v, dim=-1)
    return torch.fft.irfft((U * V) * mask, n=u.shape[-1], dim=-1)


def build_task(seed, additive_target):
    """FAIR: composite class = T[fa[i],fb[j]]; T random non-additive P x P -> C table.
    additive_target=True => rig-control with T_add[fa,fb]=(fa+fb) (additive structure)."""
    g = torch.Generator().manual_seed(seed)
    A = F.normalize(torch.randn(NA, D, generator=g), dim=-1)          # random, no planted struct
    B = F.normalize(torch.randn(NB, D, generator=g), dim=-1)
    Kc = F.normalize(torch.randn(C, D, generator=g), dim=-1)          # operator-agnostic class keys
    # latent factors: 2 atoms per class, assigned round-robin then shuffled
    fa = torch.tensor([i % P for i in range(NA)])[torch.randperm(NA, generator=g)]
    fb = torch.tensor([j % P for j in range(NB)])[torch.randperm(NB, generator=g)]
    if additive_target:
        # additive structure: class = (fa+fb) mapped into 0..C-1 (fa+fb in 0..2P-2=8 == C-1)
        T = torch.tensor([[(a + b) % C for b in range(P)] for a in range(P)])
    else:
        # genuine RANDOM 2-way NON-additive interaction table
        gT = torch.Generator().manual_seed(seed + 12345)
        T = torch.randint(0, C, (P, P), generator=gT)
    pairs = [(i, j) for i in range(NA) for j in range(NB)]
    labels = torch.tensor([int(T[fa[i], fb[j]]) for (i, j) in pairs])
    # split: every atom AND every (fa,fb) latent-pair covered in train
    perm = torch.randperm(NC, generator=g).tolist()
    n_tr = int(round(0.70 * NC))
    tr = set(perm[:n_tr])
    need_a, need_b, need_lp = set(range(NA)), set(range(NB)), set((int(fa[i]), int(fb[j])) for i, j in pairs)
    cov_a, cov_b, cov_lp = set(), set(), set()
    for idx in tr:
        i, j = pairs[idx]; cov_a.add(i); cov_b.add(j); cov_lp.add((int(fa[i]), int(fb[j])))
    for idx in perm:
        i, j = pairs[idx]; lp = (int(fa[i]), int(fb[j]))
        if i not in cov_a or j not in cov_b or lp not in cov_lp:
            tr.add(idx); cov_a.add(i); cov_b.add(j); cov_lp.add(lp)
    assert cov_a == need_a and cov_b == need_b and cov_lp == need_lp, "coverage incomplete"
    ho = [idx for idx in range(NC) if idx not in tr]
    return A, B, Kc, pairs, labels, sorted(tr), ho


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
        if arm == "bilinear_bottleneck":
            # full learned bilinear form, NO additive skip: q = Wo @ vec(u outer v)
            self.Wo = torch.nn.Parameter((1.0 / D) * torch.randn(D, D * D, generator=g))
        if arm == "noninv_bottleneck":
            nf = D // 2 + 1
            gm = torch.Generator().manual_seed(seed + 7)
            m = (torch.rand(nf, generator=gm) > 0.5).float(); m[0] = 1.0
            self.register_buffer("mask", m)

    def query(self, ea, eb):
        u = ea @ self.Wa.T; v = eb @ self.Wb.T
        if self.arm == "additive":
            return u + v
        if self.arm == "hadamard_bypass":
            return u * v + (ea @ self.Sa.T + eb @ self.Sb.T)   # bypass OPEN
        if self.arm == "hrr_bottleneck":
            return circ_conv(u, v)
        if self.arm == "noninv_bottleneck":
            return circ_conv_freqmasked(u, v, self.mask)
        if self.arm == "bilinear_bottleneck":
            outer = (u.unsqueeze(-1) * v.unsqueeze(-2)).reshape(u.shape[0], D * D)  # bypass DENIED
            return outer @ self.Wo.T
        raise ValueError(self.arm)


def run_arm(arm, seed, A, B, Kc, pairs, labels, tr_idx, ho_idx):
    model = Arm(arm, seed)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    ea_tr = torch.stack([A[pairs[k][0]] for k in tr_idx])
    eb_tr = torch.stack([B[pairs[k][1]] for k in tr_idx])
    y_tr = labels[torch.tensor(tr_idx)]
    for _ in range(STEPS):
        opt.zero_grad(set_to_none=True)
        q = F.normalize(model.query(ea_tr, eb_tr), dim=-1)
        loss = F.cross_entropy((q @ Kc.T) / TEMP, y_tr)
        loss.backward(); opt.step()

    def evalset(idxs):
        if not idxs:
            return float("nan"), 0
        ea = torch.stack([A[pairs[k][0]] for k in idxs])
        eb = torch.stack([B[pairs[k][1]] for k in idxs])
        y = labels[torch.tensor(idxs)]
        with torch.no_grad():
            pred = (F.normalize(model.query(ea, eb), dim=-1) @ Kc.T).argmax(-1)
        acc = float((pred == y).float().mean())
        distinct = int(torch.unique(pred[pred == y]).numel())   # composed_distinct (correct classes)
        return round(acc, 4), distinct

    tr_acc, _ = evalset(tr_idx)
    ho_acc, ho_distinct = evalset(ho_idx)
    return {"train_acc": tr_acc, "heldout_acc": ho_acc, "composed_distinct": ho_distinct,
            "final_ce": round(float(loss), 5)}


def run_target(additive_target, seeds):
    results = {}
    tag = "ADDITIVE-control" if additive_target else "FAIR"
    print(f"\n########## {tag} target | chance={1/C:.4f} | C={C} P={P} ##########", flush=True)
    for seed in seeds:
        torch.manual_seed(seed)
        A, B, Kc, pairs, labels, tr, ho = build_task(seed, additive_target)
        results[seed] = {}
        print(f"-- seed {seed} | train={len(tr)} heldout={len(ho)} --", flush=True)
        for arm in ARMS:
            r = run_arm(arm, seed, A, B, Kc, pairs, labels, tr, ho)
            results[seed][arm] = r
            print(f"   {arm:22s} train={r['train_acc']:.3f} heldout={r['heldout_acc']:.3f} "
                  f"distinct={r['composed_distinct']:2d} ce={r['final_ce']:.4f}", flush=True)
    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="*", default=[7, 4302, 4303])
    ap.add_argument("--out", default="toy_fair_result.json")
    a = ap.parse_args()

    fair = run_target(False, a.seeds)
    ctrl = run_target(True, a.seeds)

    # ---- FROZEN BAR (FREEZE_fair.md) ----
    def dom(rs, target_arm, over_arm, margin=0.34):
        return rs[target_arm]["heldout_acc"] >= rs[over_arm]["heldout_acc"] + margin

    print("\n=== FROZEN-BAR (FAIR target) per-seed ===", flush=True)
    n_dom_add = n_dom_byp = n_train_ok = 0
    for seed in a.seeds:
        rs = fair[seed]
        da = dom(rs, "bilinear_bottleneck", "additive")
        db = dom(rs, "bilinear_bottleneck", "hadamard_bypass")
        tok = all(rs[ar]["train_acc"] >= 0.95 for ar in ARMS)
        n_dom_add += int(da); n_dom_byp += int(db); n_train_ok += int(tok)
        print(f"   seed {seed}: e_heldout={rs['bilinear_bottleneck']['heldout_acc']:.3f} "
              f"a={rs['additive']['heldout_acc']:.3f} b={rs['hadamard_bypass']['heldout_acc']:.3f} "
              f"| e>a+.34:{da} e>b+.34:{db} train>=.95:{tok}", flush=True)

    # rig-check: on additive control, bilinear must NOT dominate additive by +0.34 (>=2/3 seeds NOT-dom)
    n_ctrl_notdom = 0
    add_arm_wins = 0
    print("=== NON-RIGGED CONTROL (additive target) per-seed ===", flush=True)
    for seed in a.seeds:
        rs = ctrl[seed]
        notdom = not dom(rs, "bilinear_bottleneck", "additive")
        addwin = rs["additive"]["heldout_acc"] >= rs["additive"]["heldout_acc"]  # placeholder
        # additive should GENERALIZE on additive target (heldout well above chance)
        addwin = rs["additive"]["heldout_acc"] >= 0.50
        n_ctrl_notdom += int(notdom); add_arm_wins += int(addwin)
        print(f"   seed {seed}: additive_heldout={rs['additive']['heldout_acc']:.3f} "
              f"bilinear_heldout={rs['bilinear_bottleneck']['heldout_acc']:.3f} "
              f"| bilinear NOT-dom additive:{notdom} additive>=.50:{addwin}", flush=True)

    c1 = n_dom_add >= 2
    c2 = n_dom_byp >= 2
    c3 = n_train_ok >= 2
    c4 = (n_ctrl_notdom >= 2) and (add_arm_wins >= 2)   # rig removed: control behaves additively
    verdict = "PASS" if (c1 and c2 and c3 and c4) else "FAIL"
    print("\n=== STAGE-1 FAIR GATE ===", flush=True)
    print(f"  c1 e>additive+.34 (>=2/3): {c1} ({n_dom_add}/3)", flush=True)
    print(f"  c2 e>bypass-open+.34 (>=2/3): {c2} ({n_dom_byp}/3)", flush=True)
    print(f"  c3 all train>=.95 (>=2/3): {c3} ({n_train_ok}/3)", flush=True)
    print(f"  c4 non-rigged control (bilinear NOT-dom add & add>=.50, >=2/3): {c4} "
          f"(notdom {n_ctrl_notdom}/3, addwin {add_arm_wins}/3)", flush=True)
    print(f"\n=== VERDICT: {verdict}  | GPU-fire authorized: {verdict == 'PASS'} ===", flush=True)

    out = {"fair": fair, "control": ctrl, "clauses": {"c1_dom_add": c1, "c2_dom_bypass": c2,
           "c3_train": c3, "c4_nonrigged": c4}, "verdict": verdict,
           "gpu_authorized": verdict == "PASS", "chance": 1 / C,
           "bar": "e>=a+.34 AND e>=b+.34 (>=2/3 seeds) AND all train>=.95 AND non-rigged-control"}
    with open(a.out, "w") as f:
        json.dump(out, f, indent=2)
    print(f"wrote {a.out}", flush=True)


if __name__ == "__main__":
    main()
