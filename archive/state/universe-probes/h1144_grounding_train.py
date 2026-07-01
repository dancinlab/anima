#!/usr/bin/env python3
"""h1144_grounding_train.py — GROUNDING continue-train of the h1141 7B to reduce its
fabricated-entity-assertion rate below the frozen G5-L2 NON-FABRICATION bar (0.20).

PROBE-FIRST (h1141-recovery discipline): a SHORT grounding leg (--steps 2000) then
re-measure fab-rate via the H_1143 harness; the frozen slope rule in
.verdicts/1144_grounding_train/H_1144_FREEZE.txt decides whether to continue to
convergence (--steps up to 12000). best-ckpt-by-val (anti-overfit, REAL held-out
val tail). LOWER LR (2e-5 vs h1141's 7e-5). BROADER corpus (1200MB en vs 300MB).

PHILOSOPHY (G3, by construction): byte-continuation on a real corpus ONLY — next-
byte CE descent. NO instruction-tuning, NO reward model, NO RLHF (p6), NO factual-
reward. val-CE = training signal ONLY (p7). Lane-G torch REFERENCE (a_clm_gen_pipeline),
NOT the forge PUBLIC trainer, NOT the CORE substrate.

ByteGPT arch + load_bytes/batch + gen() = h1141_7b_pass_attempt.py VERBATIM.
grad-ckpt is WIRED (torch.utils.checkpoint engages when grad_ckpt and training).

Usage:
  h1144_grounding_train.py --base <h1141.pt> --corpus <corpus_en_1200mb.txt>
    --steps 2000 --lr 2e-5 --ckpt <out.pt> [--resume <prev_best.pt>]
  (LEG 1 probe: --steps 2000; convergence: --steps 12000 --resume <probe_best>)
"""
from __future__ import annotations
import argparse, json, math, os, time
import torch, torch.nn as nn, torch.nn.functional as F


# ── EXACT h1141_7b_pass_attempt.py ByteGPT arch (grad-ckpt WIRED) ──
class Block(nn.Module):
    def __init__(s, d, h, p):
        super().__init__()
        s.ln1 = nn.LayerNorm(d); s.attn = nn.MultiheadAttention(d, h, dropout=p, batch_first=True)
        s.ln2 = nn.LayerNorm(d); s.mlp = nn.Sequential(nn.Linear(d, 4*d), nn.GELU(), nn.Linear(4*d, d), nn.Dropout(p))
    def forward(s, x, m):
        h = s.ln1(x); a, _ = s.attn(h, h, h, attn_mask=m, need_weights=False); x = x + a
        return x + s.mlp(s.ln2(x))

class ByteGPT(nn.Module):
    def __init__(s, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p=0.0, grad_ckpt=False):
        super().__init__()
        s.block = block; s.grad_ckpt = grad_ckpt
        s.tok = nn.Embedding(vocab, d); s.pos = nn.Embedding(block, d); s.drop = nn.Dropout(p)
        s.blocks = nn.ModuleList([Block(d, n_head, p) for _ in range(n_layer)])
        s.ln_f = nn.LayerNorm(d); s.head = nn.Linear(d, vocab, bias=False); s.head.weight = s.tok.weight
    def forward(s, idx, targets=None):
        B, T = idx.shape; pos = torch.arange(T, device=idx.device)
        x = s.drop(s.tok(idx) + s.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device, dtype=x.dtype), diagonal=1)
        for b in s.blocks:
            if s.grad_ckpt and s.training:
                x = torch.utils.checkpoint.checkpoint(b, x, mask, use_reentrant=False)
            else:
                x = b(x, mask)
        logits = s.head(s.ln_f(x))
        loss = F.cross_entropy(logits.view(-1, 256).float(), targets.view(-1)) if targets is not None else None
        return logits, loss


def load_bytes(p, cap):
    raw = open(p, "rb").read(cap)
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8)

def batch(d, block, bs, dev):
    ix = torch.randint(0, d.numel()-block-1, (bs,))
    x = torch.stack([d[i:i+block] for i in ix]).to(dev).long()
    y = torch.stack([d[i+1:i+1+block] for i in ix]).to(dev).long()
    return x, y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True, help="h1141 7B ckpt (.pt) to continue-train")
    ap.add_argument("--resume", default="", help="optional prev best ckpt to continue from (convergence leg)")
    ap.add_argument("--corpus", required=True, help="1200MB en grounding corpus")
    ap.add_argument("--cap_mb", type=float, default=1200.0)
    ap.add_argument("--val_frac", type=float, default=0.05, help="held-out val = last val_frac of the slice")
    ap.add_argument("--bs", type=int, default=8); ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--steps", type=int, default=2000); ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--lr", type=float, default=2e-5)
    ap.add_argument("--ckpt", default="/workspace/ckpt/h1144_best.pt")
    ap.add_argument("--eval_every", type=int, default=200)
    ap.add_argument("--target_plateau", type=int, default=4,
                    help="early-stop after this many eval-windows without a new best (convergence leg only)")
    ap.add_argument("--leg", default="probe", help="probe|converge (cosmetic tag in the curve json)")
    ap.add_argument("--out", default="/workspace/h1144_train_curve.json")
    a = ap.parse_args()
    dev = "cuda" if torch.cuda.is_available() else "cpu"; torch.manual_seed(7)
    print(f"[dev] {dev} {torch.cuda.get_device_name(0) if dev=='cuda' else ''}", flush=True)

    src = a.resume if a.resume and os.path.exists(a.resume) else a.base
    ck = torch.load(src, map_location="cpu", weights_only=False); cfg = ck["config"]
    block = cfg["block"]
    print(f"[init] continue-train from {src} cfg={cfg} val_ce={ck.get('val_ce')} step={ck.get('step')}", flush=True)

    # ── data: REAL held-out val = last val_frac of the 1200MB slice (DISJOINT) ──
    data = load_bytes(a.corpus, int(a.cap_mb*1024*1024))
    n = data.numel(); n_val = int(n * a.val_frac)
    tr = data[: n - n_val]; va = data[n - n_val :]
    print(f"[data] {n/1e6:.0f}MB total -> train {tr.numel()/1e6:.0f}MB  held-out-val {va.numel()/1e6:.0f}MB (DISJOINT tail)", flush=True)

    m = ByteGPT(cfg["vocab"], cfg["d"], cfg["n_layer"], cfg["n_head"], cfg["block"], grad_ckpt=True).to(torch.bfloat16)
    sd = ck["model"] if "model" in ck else ck
    m.load_state_dict(sd, strict=False); m = m.to(dev)
    nparam = sum(p.numel() for p in m.parameters())
    print(f"[model] {nparam:,} params ({nparam/1e9:.2f}B) bf16 + grad-ckpt", flush=True)
    del ck, sd

    opt = torch.optim.AdamW(m.parameters(), lr=a.lr, betas=(0.9, 0.95), weight_decay=0.1)

    def eval_ce(d, iters=40):
        m.eval()
        with torch.no_grad():
            tot = 0.0
            for _ in range(iters):
                x, y = batch(d, block, a.bs, dev)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16) if dev == "cuda" else torch.no_grad():
                    _, l = m(x, y)
                tot += l.item()
        m.train(); return tot/iters

    def save_ckpt(path, vce, st):
        torch.save({"model": m.state_dict(), "config": cfg, "val_ce": vce, "step": st,
                    "nparam": nparam, "lineage": "h1144_grounding_continue_train", "leg": a.leg}, path)

    os.makedirs(os.path.dirname(a.ckpt) or ".", exist_ok=True)
    # baseline held-out val of the loaded model on THIS corpus (anti-overfit anchor)
    base_val = eval_ce(va)
    print(f"[baseline] loaded-model held-out val_ce on grounding corpus = {base_val:.4f}", flush=True)

    best = base_val; best_step = -1; t0 = time.time(); m.train()
    curve = [{"step": -1, "train_ce": None, "val_ce": round(base_val, 4), "note": "baseline-on-grounding-corpus"}]
    plateau_ct = 0; last_best = best
    # save baseline as the initial best ckpt so the worst case = the loaded model (never WORSE).
    save_ckpt(a.ckpt, base_val, -1)
    print(f"  [ckpt] saved baseline as initial best val_ce={base_val:.4f}", flush=True)

    for st in range(a.steps):
        lr_t = a.lr*(st+1)/a.warmup if st < a.warmup else a.lr*0.5*(1+math.cos(math.pi*min(1.0,(st-a.warmup)/max(1,a.steps-a.warmup))))
        for g in opt.param_groups: g["lr"] = lr_t
        opt.zero_grad(set_to_none=True); acc = 0.0
        for _ in range(a.accum):
            x, y = batch(tr, block, a.bs, dev)
            if dev == "cuda":
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16): _, l = m(x, y)
            else: _, l = m(x, y)
            (l/a.accum).backward(); acc += l.item()/a.accum
        torch.nn.utils.clip_grad_norm_(m.parameters(), 1.0); opt.step()
        if st % a.eval_every == 0 or st == a.steps-1:
            vce = eval_ce(va)
            mem = torch.cuda.max_memory_allocated()/2**30 if dev == "cuda" else 0.0
            curve.append({"step": st, "train_ce": round(acc, 4), "val_ce": round(vce, 4)})
            print(f"  step {st:5d} train_ce={acc:.4f} val_ce={vce:.4f} lr={lr_t:.2e} "
                  f"{(time.time()-t0)/60:.1f}min mem={mem:.1f}GB best={best:.4f}", flush=True)
            if vce < best:
                best = vce; best_step = st; save_ckpt(a.ckpt, vce, st)
                print(f"  [ckpt] NEW best val_ce={vce:.4f} @ step {st}", flush=True)
            # plateau detection: <0.5% relative improvement over the eval window
            if best < last_best * 0.995: plateau_ct = 0
            else: plateau_ct += 1
            last_best = best
            if a.leg == "converge" and plateau_ct >= a.target_plateau and best < base_val:
                print(f"  [early-stop] converge-leg plateau {plateau_ct} (best {best:.4f} < base {base_val:.4f}) -> stop", flush=True)
                break
    wall = (time.time()-t0)/60
    print(f"[train] done leg={a.leg} best_val_ce={best:.4f} @step{best_step} base_val={base_val:.4f} "
          f"ckpt={a.ckpt} wall={wall:.1f}min", flush=True)
    json.dump({"hypothesis": "H_1144_grounding_train", "leg": a.leg, "base_ckpt": a.base,
               "resume": a.resume, "corpus": os.path.basename(a.corpus), "cap_mb": a.cap_mb,
               "lr": a.lr, "steps": a.steps, "bs": a.bs, "accum": a.accum, "val_frac": a.val_frac,
               "nparam": nparam, "baseline_val_on_grounding_corpus": round(base_val, 4),
               "best_val_ce": round(best, 4), "best_step": best_step, "wall_min": round(wall, 1),
               "improved_vs_baseline": best < base_val, "curve": curve},
              open(a.out, "w"), ensure_ascii=False, indent=2)
    print(f"[done] wrote {a.out}  (best ckpt at {a.ckpt})", flush=True)


if __name__ == "__main__": main()
