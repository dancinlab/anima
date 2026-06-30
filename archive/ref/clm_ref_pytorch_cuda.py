#!/usr/bin/env python
"""Lane-G-ref PyTorch+CUDA BASELINE trainer for the anima CLM+KOSMOS domain.

substrate = PyTorch-CUDA   lane = Lane-G-ref

THIS IS A BASELINE REFERENCE PROBE, NOT THE PRODUCTION ARTIFACT.
The production / PUBLIC-grade Lane-G CLM MUST be the hexa-native flame+forge
stack (compiler-only NN, NO PyTorch/ATen) per governance a_train_flame_forge.
This torch trainer exists only to set a throughput/util REFERENCE number — what
a well-fed H100 trivially achieves on this byte-level char-LM workload — the bar
the forge line's util-GREEN goal is implicitly chasing. It NEVER satisfies or
replaces the forge PUBLIC artifact (a_completeness_over_cheap: optional baseline
probe, never the primary). It is NOT merged with Lane A / AKIDA
(a_lane_akida_gpu_split).

A clean byte-level (V=256) decoder-only GPT trained with AMP/bf16 on the same
5-lang c4 backbone corpus the forge line uses, so the H100 util it reaches is an
apples-ish reference for the forge util-GREEN endgame.
"""
import argparse, json, math, os, time, hashlib, threading, subprocess
import torch
import torch.nn as nn
import torch.nn.functional as F


# ----------------------------- model -----------------------------
class Block(nn.Module):
    def __init__(self, d, n_head, p_drop):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = nn.MultiheadAttention(d, n_head, dropout=p_drop, batch_first=True)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d), nn.Dropout(p_drop))

    def forward(self, x, attn_mask):
        h = self.ln1(x)
        a, _ = self.attn(h, h, h, attn_mask=attn_mask, need_weights=False)
        x = x + a
        x = x + self.mlp(self.ln2(x))
        return x


class ByteGPT(nn.Module):
    def __init__(self, vocab=256, d=768, n_layer=12, n_head=12, block=512, p_drop=0.0):
        super().__init__()
        self.block = block
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(block, d)
        self.drop = nn.Dropout(p_drop)
        self.blocks = nn.ModuleList([Block(d, n_head, p_drop) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab, bias=False)
        self.head.weight = self.tok.weight  # tie
        self.apply(self._init)

    def _init(self, m):
        if isinstance(m, nn.Linear):
            nn.init.normal_(m.weight, std=0.02)
            if m.bias is not None:
                nn.init.zeros_(m.bias)
        elif isinstance(m, nn.Embedding):
            nn.init.normal_(m.weight, std=0.02)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        pos = torch.arange(T, device=idx.device)
        x = self.drop(self.tok(idx) + self.pos(pos)[None, :, :])
        mask = torch.triu(torch.full((T, T), float("-inf"), device=idx.device), diagonal=1)
        for blk in self.blocks:
            x = blk(x, mask)
        x = self.ln_f(x)
        logits = self.head(x)
        loss = None
        if targets is not None:
            loss = F.cross_entropy(logits.view(-1, logits.size(-1)), targets.view(-1))
        return logits, loss


# ----------------------------- util sampler -----------------------------
class UtilSampler:
    def __init__(self, interval=2.0):
        self.samples = []
        self.interval = interval
        self._stop = threading.Event()
        self._t = threading.Thread(target=self._run, daemon=True)

    def _run(self):
        while not self._stop.is_set():
            try:
                out = subprocess.run(
                    ["nvidia-smi", "--query-gpu=utilization.gpu,memory.used,power.draw",
                     "--format=csv,noheader,nounits"],
                    capture_output=True, text=True, timeout=10)
                line = out.stdout.strip().splitlines()[0]
                u, m, p = [x.strip() for x in line.split(",")]
                self.samples.append({"util": float(u), "mem_mib": float(m), "power_w": float(p)})
            except Exception:
                pass
            self._stop.wait(self.interval)

    def start(self):
        self._t.start()

    def stop(self):
        self._stop.set()
        self._t.join(timeout=5)

    def summary(self):
        if not self.samples:
            return {"n": 0, "util_peak": 0.0, "util_mean": 0.0, "mem_peak_mib": 0.0, "power_mean_w": 0.0}
        us = [s["util"] for s in self.samples]
        ms = [s["mem_mib"] for s in self.samples]
        ps = [s["power_w"] for s in self.samples]
        return {
            "n": len(self.samples),
            "util_peak": max(us),
            "util_mean": sum(us) / len(us),
            "mem_peak_mib": max(ms),
            "power_mean_w": sum(ps) / len(ps),
        }


# ----------------------------- data -----------------------------
def load_corpus(path):
    with open(path, "rb") as f:
        data = f.read()
    return torch.frombuffer(bytearray(data), dtype=torch.uint8).long()


def get_batch(data, block, batch, device):
    ix = torch.randint(0, data.numel() - block - 1, (batch,))
    x = torch.stack([data[i:i + block] for i in ix]).to(device, non_blocking=True)
    y = torch.stack([data[i + 1:i + 1 + block] for i in ix]).to(device, non_blocking=True)
    return x, y


# ----------------------------- main -----------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--d", type=int, default=768)
    ap.add_argument("--n_layer", type=int, default=12)
    ap.add_argument("--n_head", type=int, default=12)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--steps", type=int, default=3000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=100)
    ap.add_argument("--eval_every", type=int, default=100)
    ap.add_argument("--out", default="/root/laneg_ref/clm_ref_pytorch_cuda.pt")
    ap.add_argument("--log", default="/root/laneg_ref/clm_ref_train.log.json")
    args = ap.parse_args()

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    assert torch.cuda.is_available(), "CUDA REQUIRED — refusing CPU fallback (a_train_flame_forge spirit)"
    device = "cuda"
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True

    data = load_corpus(args.corpus)
    n = data.numel()
    n_train = int(n * 0.9)
    train_data, val_data = data[:n_train], data[n_train:]
    print(f"[data] corpus bytes={n} train={n_train} val={n - n_train}", flush=True)

    model = ByteGPT(256, args.d, args.n_layer, args.n_head, args.block).to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] ByteGPT d={args.d} L={args.n_layer} H={args.n_head} block={args.block} params={n_params}", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / args.warmup
        prog = (step - args.warmup) / max(1, args.steps - args.warmup)
        return args.lr * 0.5 * (1 + math.cos(math.pi * prog)) * 0.9 + args.lr * 0.1 * 0.5

    sampler = UtilSampler(interval=2.0)
    sampler.start()
    curve = []
    model.train()
    t0 = time.time()
    tok_seen = 0
    first_ce = None
    last_ce = None

    for step in range(args.steps):
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        x, y = get_batch(train_data, args.block, args.batch, device)
        with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
            _, loss = model(x, y)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        tok_seen += args.batch * args.block

        if step % args.eval_every == 0 or step == args.steps - 1:
            model.eval()
            with torch.no_grad():
                vx, vy = get_batch(val_data, args.block, args.batch, device)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, vloss = model(vx, vy)
            model.train()
            ce = float(vloss.item())
            tr = float(loss.item())
            if first_ce is None:
                first_ce = ce
            last_ce = ce
            dt = time.time() - t0
            tps = tok_seen / dt if dt > 0 else 0
            rec = {"step": step, "train_ce": tr, "val_ce": ce, "lr": lr_at(step),
                   "elapsed_s": round(dt, 1), "tok_per_s": round(tps, 1)}
            curve.append(rec)
            print(f"[step {step}] train_ce={tr:.5f} val_ce={ce:.5f} tok/s={tps:.0f} "
                  f"elapsed={dt:.0f}s", flush=True)

    sampler.stop()
    total_dt = time.time() - t0
    usum = sampler.summary()
    descent = bool(first_ce is not None and last_ce is not None and last_ce < first_ce)

    torch.save({"model": model.state_dict(),
                "config": {"vocab": 256, "d": args.d, "n_layer": args.n_layer,
                           "n_head": args.n_head, "block": args.block, "n_params": n_params}},
               args.out)
    sha = hashlib.sha256(open(args.out, "rb").read()).hexdigest()

    result = {
        "lane": "Lane-G-ref",
        "substrate": "PyTorch-CUDA",
        "note": "BASELINE REFERENCE — NOT the hexa-native flame+forge production artifact (a_train_flame_forge)",
        "config": {"vocab": 256, "d": args.d, "n_layer": args.n_layer, "n_head": args.n_head,
                   "block": args.block, "batch": args.batch, "steps": args.steps,
                   "n_params": n_params},
        "descent": {"first_val_ce": first_ce, "last_val_ce": last_ce,
                    "F_CLM_REF_DESCENT": 1 if descent else 0, "verdict": "PASS" if descent else "FAIL"},
        "util": usum,
        "throughput": {"total_s": round(total_dt, 1),
                       "tok_per_s_final": round(tok_seen / total_dt, 1) if total_dt > 0 else 0,
                       "tok_seen": tok_seen},
        "ckpt": {"path": args.out, "sha256": sha, "bytes": os.path.getsize(args.out)},
        "curve": curve,
    }
    with open(args.log, "w") as f:
        json.dump(result, f, indent=2)
    print("=== RESULT ===", flush=True)
    print(json.dumps(result, indent=2), flush=True)
    print(f"=== util PEAK={usum['util_peak']:.1f}% MEAN={usum['util_mean']:.2f}% "
          f"mem_peak={usum['mem_peak_mib']:.0f}MiB n={usum['n']} ===", flush=True)
    print(f"=== descent {'PASS' if descent else 'FAIL'} CE {first_ce:.5f} -> {last_ce:.5f} ===", flush=True)
    print(f"=== ckpt sha256={sha} bytes={os.path.getsize(args.out)} ===", flush=True)


if __name__ == "__main__":
    main()
