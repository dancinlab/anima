#!/usr/bin/env python3
"""H_9235 fork-A Step-2 — PART 2: train the single-head cross-attention retrieval lane (torch, GPU).

Reads precomputed frozen-trunk states (step2_precompute.py). Trains ONLY the ~3M-param lane; trunk frozen.
Fable spec, verbatim:
  Q=yn@Wq  K=yn@Wk  V=yn@Wv           # [T,256]  dh=dv=256, fp32
  eligible i in [0, t-64)               # strictly causal + 64-byte exclusion (kills self-read + local n-gram)
  A = softmax_i( Q_t.K_i / sqrt(256) )  # fixed scaling, NO learnable temperature
  ctx = sum_i A_ti V_i
  H = -sum A log A ; g = sigmoid( a*(logN - H)/logN + b )   # gate sees ONLY attn entropy, NEVER yn_t
  bias = g * tau * tanh( (ctx@Wo) / tau )                   # tau=8 FIXED soft-bound (same train+eval)
  logits = base + bias
  Wo ZERO-init (no-op at step 0) ; Wq,Wk,Wv ~ N(0,0.02) ; a=1, b=-2
Loss = sum_{t in target span} CE(logits_t, byte_t) + 0.1 * mean_{t in S} KL( softmax(logits_t) || softmax(base_t) )
  S = 8 sampled non-span positions >= gap_start.  Lane applied at ALL positions t >= gap_start.
Gates: T1 train assoc-span CE improves >=0.3 nats vs base ; T2 val (held-out concepts) assoc CE improves, CI>0.
Emits lane npz for the numpy eval harness (part 3).
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
DH = 256
TAU = 8.0
EXCL = 64          # exclusion window (bytes)


class XAttnLane(torch.nn.Module):
    def __init__(self, d, V):
        super().__init__()
        self.Wq = torch.nn.Parameter(torch.randn(d, DH) * 0.02)
        self.Wk = torch.nn.Parameter(torch.randn(d, DH) * 0.02)
        self.Wv = torch.nn.Parameter(torch.randn(d, DH) * 0.02)
        self.Wo = torch.nn.Parameter(torch.zeros(DH, V))       # zero-init => no-op at step 0
        self.a = torch.nn.Parameter(torch.tensor(1.0))
        self.b = torch.nn.Parameter(torch.tensor(-2.0))

    def forward(self, yn, base):
        """yn [T,d], base [T,V] -> logits [T,V] with lane bias at every position (masked eligibility)."""
        T = yn.shape[0]
        Q = yn @ self.Wq
        K = yn @ self.Wk
        Vv = yn @ self.Wv
        score = (Q @ K.t()) / math.sqrt(DH)                    # [T,T]
        idx = torch.arange(T, device=yn.device)
        elig = (idx[None, :] < (idx[:, None] - EXCL))          # i < t-64
        Nt = elig.sum(1).clamp(min=1).float()                  # [T]
        score = score.masked_fill(~elig, float("-inf"))
        A = torch.softmax(score, dim=1)                        # [T,T]; rows with no eligible -> uniform-ish; guard below
        no_elig = (elig.sum(1) == 0)
        A = A.masked_fill(no_elig[:, None], 0.0)
        ctx = A @ Vv                                           # [T,DH]
        H = -(A.clamp_min(1e-12) * A.clamp_min(1e-12).log()).sum(1)   # [T]
        logN = Nt.log().clamp(min=1e-6)
        g = torch.sigmoid(self.a * (logN - H) / logN + self.b)       # [T]
        g = g.masked_fill(no_elig, 0.0)
        bias = g[:, None] * TAU * torch.tanh((ctx @ self.Wo) / TAU)   # [T,V]
        return base + bias


def load_docs(states_dir, split):
    man = json.load(open(os.path.join(states_dir, "manifest.json")))
    return [d for d in man["docs"] if d["split"] == split], man


def doc_tensors(states_dir, rec):
    z = np.load(os.path.join(states_dir, rec["fn"]))
    yn = torch.from_numpy(z["yn"].astype(np.float32)).to(DEV)
    base = torch.from_numpy(z["base"].astype(np.float32)).to(DEV)
    tok = z["tok"].astype(np.int64)
    gap_start, span_lo, span_hi, retrieval, T = z["meta"].tolist()
    return yn, base, tok, gap_start, span_lo, span_hi, retrieval


def doc_loss(lane, yn, base, tok, gap_start, span_lo, span_hi, rng, silence=True):
    """returns (span_ce, base_span_ce, kl) tensors. span positions predict tok[t+1]; span_lo..span_hi are the
    target BYTE offsets, so the predicting positions are span_lo-1 .. span_hi-2."""
    logits = lane(yn, base)
    T = yn.shape[0]
    tgt = torch.from_numpy(tok).to(DEV)
    ps = list(range(max(span_lo - 1, 0), min(span_hi - 1, T - 1)))
    if not ps:
        return None
    pos = torch.tensor(ps, device=DEV)
    lg = logits[pos]
    ce = Fnn.cross_entropy(lg, tgt[pos + 1], reduction="mean")
    with torch.no_grad():
        bce = Fnn.cross_entropy(base[pos], tgt[pos + 1], reduction="mean")
    kl = torch.tensor(0.0, device=DEV)
    if silence:
        cand = [t for t in range(gap_start, T - 1) if not (span_lo - 1 <= t < span_hi - 1)]
        if cand:
            sc = rng.sample(cand, min(8, len(cand)))
            sp = torch.tensor(sc, device=DEV)
            kl = Fnn.kl_div(Fnn.log_softmax(logits[sp], -1), Fnn.softmax(base[sp], -1),
                            reduction="batchmean")
    return ce, bce, kl


def eval_split(lane, states_dir, recs, sd, only_assoc=True):
    import random as _r
    rng = _r.Random(1)
    lane.eval()
    ce_d, base_d = [], []
    with torch.no_grad():
        for rec in recs:
            if only_assoc and rec["retrieval"]:
                continue
            t = doc_tensors(states_dir, rec)
            out = doc_loss(lane, *t[:6], rng, silence=False)
            if out is None:
                continue
            ce, bce, _ = out
            ce_d.append(ce.item()); base_d.append(bce.item())
    lane.train()
    d = np.array(base_d) - np.array(ce_d)         # improvement (base - lane), >0 = better
    return float(d.mean()) if len(d) else 0.0, d


def boot_lo(d, iters=2000, seed=3):
    if len(d) < 2:
        return -1.0
    r = np.random.RandomState(seed)
    m = np.array([d[r.randint(0, len(d), len(d))].mean() for _ in range(iters)])
    return float(np.percentile(m, 2.5))


def main():
    import random
    ap = argparse.ArgumentParser()
    ap.add_argument("--states", default=os.path.expanduser("~/g1_gamma/step2_states"))
    ap.add_argument("--out", default=os.path.expanduser("~/g1_gamma/step2_lane.npz"))
    ap.add_argument("--epochs", type=int, default=20)
    ap.add_argument("--bs", type=int, default=32)
    ap.add_argument("--lr", type=float, default=3e-4)
    a = ap.parse_args()
    print("DEV=%s" % DEV, flush=True)
    train, man = load_docs(a.states, "train")
    val, _ = load_docs(a.states, "val")
    z0 = np.load(os.path.join(a.states, train[0]["fn"]))
    d = z0["yn"].shape[1]; V = z0["base"].shape[1]
    print("d=%d V=%d train=%d val=%d" % (d, V, len(train), len(val)), flush=True)
    lane = XAttnLane(d, V).to(DEV)
    mats = [lane.Wq, lane.Wk, lane.Wv, lane.Wo]
    opt = torch.optim.AdamW([{"params": mats, "weight_decay": 0.01},
                             {"params": [lane.a, lane.b], "weight_decay": 0.0}], lr=a.lr)
    total_steps = a.epochs * (len(train) // a.bs)
    warm = 200
    def lr_at(s):
        if s < warm:
            return a.lr * s / warm
        p = (s - warm) / max(total_steps - warm, 1)
        return 3e-5 + 0.5 * (a.lr - 3e-5) * (1 + math.cos(math.pi * p))
    rng = random.Random(0)
    step = 0
    best_val = -1e9; patience = 0; best_state = None
    for ep in range(a.epochs):
        rng.shuffle(train)
        opt.zero_grad()
        acc = 0
        run_ce = []
        for i, rec in enumerate(train):
            t = doc_tensors(a.states, rec)
            out = doc_loss(lane, *t[:6], rng)
            if out is None:
                continue
            ce, bce, kl = out
            loss = (ce + 0.1 * kl) / a.bs
            loss.backward()
            run_ce.append((bce - ce).item())
            acc += 1
            if acc % a.bs == 0:
                for gp in opt.param_groups:
                    gp["lr"] = lr_at(step)
                torch.nn.utils.clip_grad_norm_([p for p in lane.parameters()], 1.0)
                opt.step(); opt.zero_grad(); step += 1
                if step % 100 == 0:
                    print("  ep%d step%d lr=%.2e train_impr(mean %d)=%.3f" %
                          (ep, step, lr_at(step), len(run_ce), float(np.mean(run_ce[-200:]))), flush=True)
        vm, vd = eval_split(lane, a.states, val, None, only_assoc=True)
        vlo = boot_lo(vd)
        print("== ep%d val_assoc_impr=%.4f CI_lo=%.4f ==" % (ep, vm, vlo), flush=True)
        if vm > best_val:
            best_val = vm; patience = 0
            best_state = {k: v.detach().cpu().numpy() for k, v in lane.state_dict().items()}
        else:
            patience += 1
            if patience >= 3:
                print("early-stop", flush=True); break
    # T1 train assoc, T2 val assoc on best
    if best_state:
        lane.load_state_dict({k: torch.from_numpy(v).to(DEV) for k, v in best_state.items()})
    t1m, _ = eval_split(lane, a.states, train, None, only_assoc=True)
    t2m, t2d = eval_split(lane, a.states, val, None, only_assoc=True)
    t2lo = boot_lo(t2d)
    T1 = t1m >= 0.3
    T2 = t2lo > 0
    print("\n=== TRAIN-SIDE GATES ===", flush=True)
    print("T1 train_assoc_impr=%.4f (>=0.3? %s)" % (t1m, T1), flush=True)
    print("T2 val_assoc_impr=%.4f CI_lo=%.4f (>0? %s)" % (t2m, t2lo, T2), flush=True)
    sd = lane.state_dict()
    np.savez(a.out, Wq=sd["Wq"].cpu().numpy(), Wk=sd["Wk"].cpu().numpy(), Wv=sd["Wv"].cpu().numpy(),
             Wo=sd["Wo"].cpu().numpy(), a=float(sd["a"]), b=float(sd["b"]),
             tau=TAU, excl=EXCL, dh=DH,
             T1=float(t1m), T2=float(t2m), T2_lo=float(t2lo))
    json.dump({"T1": t1m, "T2": t2m, "T2_lo": t2lo, "T1_pass": bool(T1), "T2_pass": bool(T2)},
              open(a.out.replace(".npz", "_gates.json"), "w"), indent=2)
    print("SAVED lane -> %s (T1=%s T2=%s)" % (a.out, T1, T2), flush=True)


if __name__ == "__main__":
    main()
