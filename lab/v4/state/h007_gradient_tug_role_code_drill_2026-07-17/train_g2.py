#!/usr/bin/env python3
"""H_007 mech-5 G-2 — the frozen verdict run: d=384 L=4, 2 seeds × 5 arms ($0 cash, local MPS, ~7h).

Reuses the G-1 smoke's proven two-head machinery (train_g1_smoke) at the H_003/H_004 envelope. Five
arms differ ONLY in head-G's target sequence (§2 of DESIGN_fable5_seed.md):

  A-tug   head-G target = swap(surface)               the mechanism (irreconcilable second objective)
  C-dup   head-G target = surface (duplicate forward) THE control — same params/compute/grad, 0 conflict
  C-shuf  head-G target = swap(OTHER drill surface)   placebo — "any hard second task" vs role-specific
  C-scaf  head-G present but λ_G = 0                   floor + mech-5's own L2 ablation-retrain arm
  C-perm  A-tug head-G, but drill ANSWER labels permuted   harness (no consistent gold rule ⇒ d_acc→0.5)

Everything else byte-identical across arms (corpus, model, params, steps, init, seed, head-G architecture).
Heads dropped at eval; all scoring = head-A forced-choice free-slot d_acc on the frozen SWAP-XOR panels.

Falsifiers measured here (frozen 2026-07-17):
  F1  Δ = d_acc(A-tug,f2) − d_acc(C-dup,f2) ≥ 0.15 both seeds (DEAD < 0.05 both).
  F2  f1(A-tug) ≥ 0.85 both (liveness).           F3  f2(C-scaf) < 0.60 (not-free floor).
  F6  d_acc(A-tug) − d_acc(C-shuf) ≥ 0.05.         harness  f2(C-perm) ∈ [0.45,0.55].
  P-conflict  differential cos(∇CE_A,∇CE_G) vs C-dup ≥ τ=0.05, measured early (trajectory recorded).
  F4  role-code eff-rank ≥ 2: probe subject-class AND object-class as SEPARABLE held-out directions
      (both decode > 0.65 AND |cos(w_subj,w_obj)| < 0.8 ⇒ not one merged scalar = v1's 1-bit seam).
  F5  project OUT the F4 subspace from A-tug's trunk state at inference → Δd_acc(f2) ≥ 0.05; specificity:
      a random same-rank projection must NOT move d_acc (>−0.05) and the F4 projection on C-dup is inert.

Run:  python3 state/h007_gradient_tug_role_code_drill_2026-07-17/train_g2.py [--tiny]
Emits g2_result_full.json (collect_verdict_g2.py applies the frozen falsifiers).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
import train_g1_smoke as g1        # reuse: build_drill/_masked_ce/_probe_acc/_cpt_windows/_nsmc_lines/bx
import build_swap_xor as bx

ARMS = ("A-tug", "C-dup", "C-shuf", "C-scaf", "C-perm")


# ---------------------------------------------------------------- model (d=384 L=4, two heads)
def _load(tiny):
    import torch
    import core.model as M
    d, L, E = (48, 2, 2) if tiny else (384, 4, 3)
    cfg = M.CLMConfig(vocab_size=256, d_model=d, n_trunk_layers=L, n_experts=E)

    class TwoHead(M.CLMConvMoE):
        def __init__(self, cfg):
            super().__init__(cfg)
            self.head_g = torch.nn.Conv1d(cfg.d_model, cfg.vocab_size, 1)

        def trunk_state(self, tokens, project=None):
            x = self.embed(tokens).transpose(1, 2)
            x = self.embed_conv(x)
            for layer in self.trunk:
                x = layer(x)
            x, stats = self.moe(x)
            x = self.norm_out(x)                             # (B,C,T)
            if project is not None:                          # F5: strip the role-code subspace (I−P)
                P = project.to(x.dtype).to(x.device)         # (C,C)
                x = x - torch.einsum("cd,bdt->bct", P, x)
            return x, stats.aux_loss

        def both_logits(self, tokens, project=None):
            x, aux = self.trunk_state(tokens, project=project)
            return self.readout(x), self.head_g(x), aux

    return torch, M, cfg, TwoHead


# ---------------------------------------------------------------- 5-arm batch
def _batch(torch, items, arm, device, pad, perm):
    """tok, tgtA, tgtG, mA, mG. `perm` = index permutation for C-perm's answer-label shuffle."""
    B = len(items)
    tok = np.zeros((B, pad), np.int64)
    tgtA = np.zeros((B, pad), np.int64); tgtG = np.zeros((B, pad), np.int64)
    mA = np.zeros((B, pad), np.float32); mG = np.zeros((B, pad), np.float32)
    for bi, it in enumerate(items):
        surf = it["surface"].encode("utf-8")
        ans = (it["answer"] if arm != "C-perm" else items[perm[bi]]["answer"]).encode("utf-8")
        seq = (surf + ans)[:pad]; Ls = len(surf); Lseq = len(seq)
        tok[bi, :Lseq] = list(seq)
        tgtA[bi, :Lseq - 1] = list(seq[1:]); mA[bi, :Lseq - 1] = 1.0
        # head-G target sequence (surface positions only)
        if arm in ("A-tug", "C-perm"):
            g = it["swap"].encode("utf-8")
        elif arm == "C-shuf":
            g = items[perm[bi]]["swap"].encode("utf-8")     # swap of a DIFFERENT sentence (length-aligned)
        else:                                               # C-dup, C-scaf → forward surface
            g = surf
        n = min(Ls, len(g))
        tgtG[bi, :n - 1] = list(g[1:n]); mG[bi, :n - 1] = 1.0
    t = lambda a: torch.tensor(a, device=device)
    return t(tok), t(tgtA), t(tgtG), t(mA), t(mG)


# ---------------------------------------------------------------- F4 / F5
def _f4_effrank(torch, model, f2, device, pad):
    """Probe subject-class and object-class as held-out directions. Returns (probe_subj, probe_obj,
    cos_dirs, effrank_ge2, P_subspace) where P projects onto orthonormal span{w_subj,w_obj}."""
    Xs, cs_lab, co_lab = g1._role_states(torch, model, f2, device, pad)
    p_subj, w_s = _probe_dir(torch, Xs, cs_lab, seed=1)
    p_obj, w_o = _probe_dir(torch, Xs, co_lab, seed=2)
    ws, wo = w_s / (w_s.norm() + 1e-9), w_o / (w_o.norm() + 1e-9)
    cos_dirs = float((ws @ wo).abs().item())
    effrank_ge2 = (p_subj > 0.65 and p_obj > 0.65 and cos_dirs < 0.8)
    # orthonormal basis of span{ws,wo} → projector P = U Uᵀ
    U, _ = torch.linalg.qr(torch.stack([ws, wo], dim=1))    # (C,2)
    P = U @ U.t()
    return round(p_subj, 4), round(p_obj, 4), round(cos_dirs, 4), bool(effrank_ge2), P


def _probe_dir(torch, X, y, seed, iters=400):
    """Held-out logistic probe → (accuracy, weight direction)."""
    g = torch.Generator().manual_seed(seed)
    n = X.shape[0]; perm = torch.randperm(n, generator=g)
    ntr = int(n * 0.7)
    Xtr, ytr, Xte, yte = X[perm[:ntr]], y[perm[:ntr]], X[perm[ntr:]], y[perm[ntr:]]
    mu, sd = Xtr.mean(0, keepdim=True), Xtr.std(0, keepdim=True) + 1e-6
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    w = torch.zeros(X.shape[1], requires_grad=True); b = torch.zeros(1, requires_grad=True)
    opt = torch.optim.Adam([w, b], lr=0.05); lossf = torch.nn.BCEWithLogitsLoss()
    for _ in range(iters):
        opt.zero_grad(); lossf(Xtr @ w + b, ytr.float()).backward(); opt.step()
    with torch.no_grad():
        acc = float(((Xte @ w + b > 0).long() == yte).float().mean().item())
    return acc, w.detach()


def _random_projector(torch, C, rank, seed):
    g = torch.Generator().manual_seed(seed)
    A = torch.randn(C, rank, generator=g)
    U, _ = torch.linalg.qr(A)
    return U @ U.t()


# ---------------------------------------------------------------- train one arm/seed
def train_arm(arm, seed, cfg_tuple, drill, f2, f1p, cpt_win, steps, device, tag):
    torch, M, cfg, TwoHead = cfg_tuple
    torch.manual_seed(seed)
    model = TwoHead(cfg).to(device)
    tp = g1._trunk_params(model)
    opt = torch.optim.Adam(model.parameters(), lr=3e-4)
    cpt_steps, drill_steps = steps
    pad = 48
    perm = list(np.random.RandomState(seed).permutation(len(drill)))
    logf = os.path.join(_HERE, f"g2_log_{tag}.jsonl"); open(logf, "w").close()

    def log(r):
        with open(logf, "a") as fh:
            fh.write(json.dumps({"arm": arm, "seed": seed, **r}, ensure_ascii=False) + "\n")

    bs = 16 if device != "cpu" else 8
    for step in range(cpt_steps):
        idx = torch.randint(0, cpt_win.shape[0], (bs,)); w = cpt_win[idx].to(device)
        la, _, aux = model.both_logits(w[:, :-1])
        loss = torch.nn.functional.cross_entropy(la, w[:, 1:]) + aux
        opt.zero_grad(); loss.backward(); opt.step()
        if step % 500 == 0 or step == cpt_steps - 1:
            log({"phase": "cpt", "step": step, "ce": round(float(loss.detach()), 4)})

    cos_hist = []; rng = np.random.RandomState(seed); B = 32
    lam_g = 0.0 if arm == "C-scaf" else 1.0
    for step in range(drill_steps):
        bidx = rng.randint(0, len(drill), size=B)
        batch = [drill[i] for i in bidx]; bperm = list(range(B)); rng.shuffle(bperm)
        tok, tgtA, tgtG, mA, mG = _batch(torch, batch, arm, device, pad, bperm)
        la, lg, aux = model.both_logits(tok)
        ceA = g1._masked_ce(torch, la, tgtA, mA)
        ceG = g1._masked_ce(torch, lg, tgtG, mG)
        if lam_g > 0 and step % 20 == 0:
            gA = torch.autograd.grad(ceA, tp, retain_graph=True, allow_unused=True)
            gG = torch.autograd.grad(ceG, tp, retain_graph=True, allow_unused=True)
            fa = torch.cat([g.reshape(-1) for g in gA if g is not None])
            fg = torch.cat([g.reshape(-1) for g in gG if g is not None])
            cos = float((fa @ fg / (fa.norm() * fg.norm() + 1e-9)).item())
            cos_hist.append({"step": step, "cos": round(cos, 4)})
            if step % 500 == 0:
                log({"phase": "drill", "step": step, "ceA": round(float(ceA.detach()), 4),
                     "ceG": round(float(ceG.detach()), 4), "cos_grad": round(cos, 4)})
        loss = ceA + lam_g * ceG + aux
        opt.zero_grad(); loss.backward(); opt.step()

    # eval — head-A forced-choice d_acc on frozen panels
    f2_dacc = g1._f2_dacc(torch, model, f2, device, pad)
    f1_dacc = g1._f2_dacc(torch, model, f1p, device, pad)
    early = [c["cos"] for c in cos_hist if c["step"] < 0.3 * drill_steps]
    res = {"arm": arm, "seed": seed, "f2_dacc": round(f2_dacc, 4), "f1_dacc": round(f1_dacc, 4),
           "cos_mean_early": round(float(np.mean(early)) if early else 0.0, 4),
           "cos_frac_neg_early": round(sum(1 for c in early if c < 0) / max(len(early), 1), 4),
           "cos_trajectory": cos_hist}

    # F4 / F5 only where meaningful (A-tug is the claim; C-dup is the specificity control)
    if arm in ("A-tug", "C-dup"):
        p_subj, p_obj, cos_dirs, effrank_ge2, P = _f4_effrank(torch, model, f2, device, pad)
        C = P.shape[0]
        d_proj = _f2_dacc_proj(torch, model, f2, device, pad, P)
        d_rand = _f2_dacc_proj(torch, model, f2, device, pad, _random_projector(torch, C, 2, seed + 99))
        res["F4"] = {"probe_subj": p_subj, "probe_obj": p_obj, "cos_dirs": cos_dirs, "effrank_ge2": effrank_ge2}
        res["F5"] = {"dacc_full": round(f2_dacc, 4), "dacc_projF4": round(d_proj, 4),
                     "delta_projF4": round(f2_dacc - d_proj, 4), "dacc_projRand": round(d_rand, 4),
                     "delta_projRand": round(f2_dacc - d_rand, 4)}
    log({"phase": "result", **{k: v for k, v in res.items() if k != "cos_trajectory"}})
    return res


def _f2_dacc_proj(torch, model, panel, device, pad, P):
    """f2 forced-choice d_acc with the subspace P projected OUT of the trunk state (F5 ablation)."""
    model.eval(); correct = 0
    with torch.no_grad():
        for it in panel:
            surf = it["surface"].encode("utf-8"); gold = it["gold_token"].encode("utf-8")
            alt = bx.AGREE[1 - bx.AGREE.index(it["gold_token"])].encode("utf-8"); Ls = len(surf)

            def nll(sfx):
                seq = (surf + sfx)[:pad]
                tok = torch.zeros(1, pad, dtype=torch.long, device=device)
                tok[0, :len(seq)] = torch.tensor(list(seq), device=device)
                la, _, _ = model.both_logits(tok, project=P)
                logp = torch.log_softmax(la[0], dim=0)
                return sum(-logp[seq[Ls + j], Ls + j - 1].item() for j in range(3))
            correct += int(nll(gold) <= nll(alt))
    return correct / len(panel)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tiny", action="store_true", help="d=48 few-steps plumbing (1 seed, all 5 arms)")
    args = ap.parse_args()
    torch, M, cfg, TwoHead = _load(args.tiny)
    import torch as _t
    device = "mps" if _t.backends.mps.is_available() else "cpu"
    cfg_tuple = (torch, M, cfg, TwoHead)

    steps = (60, 80) if args.tiny else (3000, 4000)
    seeds = (0,) if args.tiny else (0, 1)
    n_cpt = 400 if args.tiny else 4000
    cpt_win = g1._cpt_windows(g1._nsmc_lines(n_cpt), 128, torch)
    drill = g1.build_drill()
    f2 = json.load(open(os.path.join(_HERE, "swap_xor_f2.json")))["panel"]
    f1p = json.load(open(os.path.join(_HERE, "swap_xor_f1.json")))["panel"]

    print("=" * 78)
    print(f"H_007 mech-5 G-2 verdict run — device={device} d={cfg.d_model} L={cfg.n_trunk_layers} "
          f"steps={steps} seeds={seeds} arms={ARMS} drill={len(drill)} f2={len(f2)} f1={len(f1p)}")
    print("=" * 78, flush=True)

    results = {}
    for seed in seeds:
        for arm in ARMS:
            tag = f"{arm}.s{seed}"
            print(f"\n--- {tag} …", flush=True)
            r = train_arm(arm, seed, cfg_tuple, drill, f2, f1p, cpt_win, steps, device, tag)
            results[tag] = r
            extra = ""
            if "F4" in r:
                extra = f" | F4 effrank≥2={r['F4']['effrank_ge2']} | F5 ΔprojF4={r['F5']['delta_projF4']}"
            print(f"  {tag}: f2_dacc={r['f2_dacc']} f1_dacc={r['f1_dacc']} "
                  f"cos_mean_early={r['cos_mean_early']}{extra}", flush=True)

    out = {"config": {"d": cfg.d_model, "L": cfg.n_trunk_layers, "steps": steps, "seeds": list(seeds),
                      "arms": list(ARMS), "device": device, "metric": "free-slot forced-choice d_acc"},
           "results": results}
    json.dump(out, open(os.path.join(_HERE, "g2_result_full.json"), "w"), ensure_ascii=False, indent=1)
    print("\nwrote g2_result_full.json — run collect_verdict_g2.py for the frozen verdict")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
