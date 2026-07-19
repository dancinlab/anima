#!/usr/bin/env python3
"""H_9235 fork-A Step-2 swap-contrastive — PART 2b: InfoNCE-contrastive lane training (Fable spec, torch GPU).

Fixes the plain-CE failure (lane near-init: Wo~0.005 = an EXACT saddle where ∂L/∂(W_qkv,a,b)≡0, so attention
could not learn to route). Two joint fixes:
  1. Wo random init N(0, 0.01^2) — breaks the saddle so upstream grads flow from step 1.
  2. InfoNCE contrastive loss on the LANE-ATTRIBUTABLE Δlogp (subtracts the frozen base offset that differs
     across genuine swap docs), pushing match's lane-margin above the K=2 swaps'.
Per paired item: Δ_v = mean_{t in span}[ logp(y_t | base_v + bias_v) − logp(y_t | base_v) ] for v in {match,sw0,sw1}.
  L_c = −log( exp(Δ_m/T) / Σ_v exp(Δ_v/T) ),  T=0.1
  L   = CE_span(match, full logits) + 0.1·KL_silence(match, off-span) + λ_c·L_c,   λ_c=1.0
CE_span + KL apply to MATCH only. Monitor: contrast top-1 acc, train swap-margin (Δ_m−mean Δ_sw), Wo norm.
"""
import os
import sys
import glob
import json
import math
import argparse

import numpy as np
import torch
import torch.nn.functional as Fnn

DEV = "cuda" if torch.cuda.is_available() else "cpu"
DH = 256; TAU = 8.0; EXCL = 64; T_NCE = 0.1


class XAttnLane(torch.nn.Module):
    def __init__(self, d, V, wo_sigma=0.01):
        super().__init__()
        self.Wq = torch.nn.Parameter(torch.randn(d, DH) * 0.02)
        self.Wk = torch.nn.Parameter(torch.randn(d, DH) * 0.02)
        self.Wv = torch.nn.Parameter(torch.randn(d, DH) * 0.02)
        self.Wo = torch.nn.Parameter(torch.randn(DH, V) * wo_sigma)   # RANDOM init (saddle break)
        self.a = torch.nn.Parameter(torch.tensor(1.0))
        self.b = torch.nn.Parameter(torch.tensor(-2.0))

    def bias(self, yn):
        T = yn.shape[0]
        Q = yn @ self.Wq; K = yn @ self.Wk; Vv = yn @ self.Wv
        score = (Q @ K.t()) / math.sqrt(DH)
        idx = torch.arange(T, device=yn.device)
        elig = (idx[None, :] < (idx[:, None] - EXCL))
        Nt = elig.sum(1).clamp(min=1).float()
        no = (elig.sum(1) == 0)
        score = score.masked_fill(~elig, float("-inf"))
        A = torch.softmax(score, dim=1).masked_fill(no[:, None], 0.0)
        ctx = A @ Vv
        H = -(A.clamp_min(1e-12) * A.clamp_min(1e-12).log()).sum(1)
        logN = Nt.log().clamp(min=1e-6)
        g = torch.sigmoid(self.a * (logN - H) / logN + self.b).masked_fill(no, 0.0)
        return g[:, None] * TAU * torch.tanh((ctx @ self.Wo) / TAU)


def _load(states_dir):
    man = json.load(open(os.path.join(states_dir, "manifest.json")))
    return man


def _tensors(states_dir, rec):
    z = np.load(os.path.join(states_dir, rec["fn"]))
    span_lo, span_hi, retr = z["meta"].tolist()
    out = {}
    for v, suf in (("m", "m"), ("s0", "s0"), ("s1", "s1")):
        out[v] = (torch.from_numpy(z["yn_" + suf].astype(np.float32)).to(DEV),
                  torch.from_numpy(z["base_" + suf].astype(np.float32)).to(DEV),
                  torch.from_numpy(z["tok_" + suf].astype(np.int64)).to(DEV))
    return out, span_lo, span_hi, retr


def _delta(lane, yn, base, tok, span_lo, span_hi):
    """lane-attributable mean Δlogp over the target span: logp(y|base+bias) − logp(y|base)."""
    T = yn.shape[0]
    ps = list(range(max(span_lo - 1, 0), min(span_hi - 1, T - 1)))
    if not ps:
        return None
    pos = torch.tensor(ps, device=DEV); y = tok[pos + 1]
    bias = lane.bias(yn)
    lp_on = Fnn.log_softmax(base[pos] + bias[pos], -1).gather(1, y[:, None]).squeeze(1)
    with torch.no_grad():
        lp_off = Fnn.log_softmax(base[pos], -1).gather(1, y[:, None]).squeeze(1)
    return (lp_on - lp_off).mean(), pos, bias


def eval_val(lane, states_dir, recs):
    """val-side train swap-margin proxy: mean(Δ_match − mean Δ_swap) on held-out-concept... (train uses train
    concepts; here 'val' = a held-out slice of paired items). Reports contrast top1 + margin."""
    lane.eval(); m_marg = []; top1 = 0; ntot = 0
    with torch.no_grad():
        for rec in recs:
            t, lo, hi, retr = _tensors(states_dir, rec)
            dm = _delta(lane, *t["m"], lo, hi)
            d0 = _delta(lane, *t["s0"], lo, hi); d1 = _delta(lane, *t["s1"], lo, hi)
            if None in (dm, d0, d1):
                continue
            vm, v0, v1 = dm[0].item(), d0[0].item(), d1[0].item()
            m_marg.append(vm - 0.5 * (v0 + v1)); ntot += 1
            if vm >= max(v0, v1):
                top1 += 1
    lane.train()
    return (float(np.mean(m_marg)) if m_marg else 0.0), (top1 / max(ntot, 1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--states", default=os.path.expanduser("~/g1_gamma/step2_paired"))
    ap.add_argument("--out", default=os.path.expanduser("~/g1_gamma/step2_lane_c.npz"))
    ap.add_argument("--epochs", type=int, default=25)
    ap.add_argument("--bs", type=int, default=16)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--lam_c", type=float, default=1.0)
    a = ap.parse_args()
    print("DEV=%s" % DEV, flush=True)
    man = _load(a.states)
    items = man["items"]
    import random as _r
    rng = _r.Random(0); rng.shuffle(items)
    val = items[:max(20, len(items) // 10)]; train = items[len(val):]
    z0 = np.load(os.path.join(a.states, items[0]["fn"]))
    d = z0["yn_m"].shape[1]; V = z0["base_m"].shape[1]
    print("d=%d V=%d train=%d val=%d" % (d, V, len(train), len(val)), flush=True)
    lane = XAttnLane(d, V).to(DEV)
    opt = torch.optim.AdamW(lane.parameters(), lr=a.lr, weight_decay=0.01)
    total = a.epochs * (len(train) // a.bs); warm = 200
    def lr_at(s):
        if s < warm:
            return a.lr * s / warm
        p = (s - warm) / max(total - warm, 1)
        return 3e-5 + 0.5 * (a.lr - 3e-5) * (1 + math.cos(math.pi * p))
    step = 0; best = -1e9; best_state = None; patience = 0
    for ep in range(a.epochs):
        rng.shuffle(train); opt.zero_grad(); acc = 0
        for rec in train:
            t, lo, hi, retr = _tensors(a.states, rec)
            dm = _delta(lane, *t["m"], lo, hi)
            d0 = _delta(lane, *t["s0"], lo, hi); d1 = _delta(lane, *t["s1"], lo, hi)
            if None in (dm, d0, d1):
                continue
            deltas = torch.stack([dm[0], d0[0], d1[0]]) / T_NCE
            L_c = -Fnn.log_softmax(deltas, 0)[0]
            # CE_span(match) + KL_silence(match, off-span)
            ynm, basem, tokm = t["m"]; bias_m = dm[2]
            pos = dm[1]; Tn = ynm.shape[0]
            logits_m = basem + bias_m
            ce = Fnn.cross_entropy(logits_m[pos], tokm[pos + 1])
            sil = [x for x in range(int(hi) - 1, Tn - 1)][:8] + [x for x in range(int(lo) - 30, int(lo) - 1) if x >= 0][:4]
            kl = torch.tensor(0.0, device=DEV)
            if sil:
                sp = torch.tensor(sil, device=DEV)
                kl = Fnn.kl_div(Fnn.log_softmax(logits_m[sp], -1), Fnn.softmax(basem[sp], -1), reduction="batchmean")
            loss = (ce + 0.1 * kl + a.lam_c * L_c) / a.bs
            loss.backward(); acc += 1
            if acc % a.bs == 0:
                for gp in opt.param_groups:
                    gp["lr"] = lr_at(step)
                torch.nn.utils.clip_grad_norm_(lane.parameters(), 1.0)
                opt.step(); opt.zero_grad(); step += 1
                if step % 50 == 0:
                    print("  ep%d step%d lr=%.1e Wo=%.4f" % (ep, step, lr_at(step),
                          lane.Wo.detach().abs().mean().item()), flush=True)
        vmarg, vtop1 = eval_val(lane, a.states, val)
        print("== ep%d val_margin=%.4f contrast_top1=%.3f Wo=%.4f ==" %
              (ep, vmarg, vtop1, lane.Wo.detach().abs().mean().item()), flush=True)
        if vmarg > best:
            best = vmarg; patience = 0
            best_state = {k: v.detach().cpu().numpy() for k, v in lane.state_dict().items()}
        else:
            patience += 1
            if patience >= 4:
                print("early-stop", flush=True); break
    if best_state:
        lane.load_state_dict({k: torch.from_numpy(v).to(DEV) for k, v in best_state.items()})
    vmarg, vtop1 = eval_val(lane, a.states, val)
    sd = lane.state_dict()
    np.savez(a.out, Wq=sd["Wq"].cpu().numpy(), Wk=sd["Wk"].cpu().numpy(), Wv=sd["Wv"].cpu().numpy(),
             Wo=sd["Wo"].cpu().numpy(), a=float(sd["a"]), b=float(sd["b"]), tau=TAU, excl=EXCL, dh=DH,
             val_margin=float(vmarg), contrast_top1=float(vtop1))
    json.dump({"val_margin": vmarg, "contrast_top1": vtop1,
               "Wo_norm": float(lane.Wo.detach().abs().mean())},
              open(a.out.replace(".npz", "_gates.json"), "w"), indent=2)
    print("\n=== CONTRASTIVE TRAIN DONE ===\nval_margin=%.4f contrast_top1=%.3f Wo_norm=%.4f\nSAVED %s" %
          (vmarg, vtop1, float(lane.Wo.detach().abs().mean()), a.out), flush=True)


if __name__ == "__main__":
    main()
