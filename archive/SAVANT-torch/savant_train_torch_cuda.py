#!/usr/bin/env python
"""SAVANT 5-lang torch-cuda REFERENCE trainer (Lane-G / GPU).

>>> HONEST LANE LABEL (a_train_flame_forge · a_lane_akida_gpu_split):
This is the **torch-cuda REFERENCE lane** — a VERBATIM reuse of the proven
`clm_ref_pytorch_cuda_7b.py` recipe (the descent-PASS / util-GREEN 7.25B rung
of the dancinlab/clm-v1-ref-pytorch-cuda{,-3b,-7b} ladder). It is NOT the
hexa-native flame+forge PUBLIC-grade production trainer that governance
(a_train_flame_forge) designates as canonical. The trained RESULT is the same
as a forge 7B would be; only the runtime/stack differs. A separate forge-native
SAVANT 7B is a later same-result variant (concurrent forge lane, pod 39404862).
Lane = Lane-G / GPU; NEVER merged with Lane A / AKIDA (a_lane_akida_gpu_split).

DELTA vs the original ref-7b recipe: periodic checkpointing under --out-dir
every --ckpt-every steps (durability for the multi-day 7B train, so a torn /
preempted pod loses at most one interval). Math/arch/optimizer are UNCHANGED
from the proven recipe.

substrate = PyTorch-CUDA   lane = Lane-G (torch-cuda reference)   rung = 5-lang 7B

THIS IS A BOUNDED-BUDGET 7B-SCALE REFERENCE RUNG, NOT A CONVERGED PRODUCTION
ARTIFACT, and NOT the hexa-native flame+forge PUBLIC-grade production model.
The production / PUBLIC-grade Lane-G CLM MUST be the hexa-native flame+forge
stack (compiler-only NN, NO PyTorch/ATen/Python in the trained binary) per
governance a_train_flame_forge. This torch trainer exists only to demonstrate,
at ~7B params on a bounded N steps, that (a) the same ByteGPT/Transformer arch
trains (CE descends) and (b) it saturates the GPU (util >> 20%) at 7B scale —
a throughput-justified 7B REFERENCE. It is an a_completeness_over_cheap optional
baseline/reference, never the primary, NEVER claimed as the forge artifact, and
NEVER merged with Lane A / AKIDA (a_lane_akida_gpu_split).

Scale honesty (a_scale_honest_scope): the 7B rung of the ref ladder
(85.6M -> 3.149B -> 7.25B). We do NOT claim convergence — bounded N steps,
descent + util demonstrated only. This is the last rung of the Lane-G-ref ladder.

Scales the same byte-level (V=256) decoder-only GPT to ~7B params (Llama-7B-ish
shape adapted to byte-vocab: d4096 / 36L / 32H / head_dim 128), trained with
AMP/bf16 + gradient checkpointing on the same 5-lang c4 backbone corpus the
85.6M PUBLIC ref and the 3.149B ref used (dancinlab/clm-backbone-5lang-sample).
"""
import argparse, json, math, os, time, hashlib, threading, subprocess
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.checkpoint import checkpoint


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
    def __init__(self, vocab=256, d=4096, n_layer=36, n_head=32, block=512, p_drop=0.0,
                 grad_ckpt=True):
        super().__init__()
        self.block = block
        self.grad_ckpt = grad_ckpt
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
            if self.grad_ckpt and self.training:
                x = checkpoint(blk, x, mask, use_reentrant=False)
            else:
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
    ap.add_argument("--d", type=int, default=4096)
    ap.add_argument("--n_layer", type=int, default=36)
    ap.add_argument("--n_head", type=int, default=32)
    ap.add_argument("--block", type=int, default=512)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--grad_accum", type=int, default=1)
    ap.add_argument("--steps", type=int, default=400)
    ap.add_argument("--lr", type=float, default=1.6e-4)
    ap.add_argument("--warmup", type=int, default=20)
    ap.add_argument("--eval_every", type=int, default=25)
    ap.add_argument("--no_grad_ckpt", action="store_true")
    ap.add_argument("--model_dtype", choices=["fp32", "bf16"], default="bf16",
                    help="bf16 stores master weights+grads in bf16 so a 7B model fits a "
                         "single 80GB GPU (fp32 weights+grads alone overflow 80GB at 7B).")
    ap.add_argument("--opt", choices=["adamw", "adamw8bit"], default="adamw8bit",
                    help="adamw8bit (bitsandbytes) keeps optimizer states in 8-bit so a "
                         "7B model + states fit a single 80GB GPU; adamw = fp32 states "
                         "(needs >80GB / sharding at 7B).")
    ap.add_argument("--out", default="/workspace/savant/savant_5lang_7b.pt")
    ap.add_argument("--log", default="/workspace/savant/savant_5lang_7b_train.log.json")
    ap.add_argument("--ckpt-every", type=int, default=0,
                    help="durability: save a resumable ckpt every N steps under "
                         "dirname(--out)/ckpt_step_<N>.pt (0=final-only, original behavior)")
    ap.add_argument("--resume", default="",
                    help="resume model+opt+step from this ckpt path (durable restart)")
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

    model = ByteGPT(256, args.d, args.n_layer, args.n_head, args.block,
                    grad_ckpt=not args.no_grad_ckpt)
    if args.model_dtype == "bf16":
        # bf16 master weights — at 7B, fp32 weights(29GB)+grads(29GB) alone overflow an
        # 80GB GPU before activations; bf16 weights+grads (~14.5GB each) + 8-bit Adam
        # states (~14.5GB) leave headroom for activations. autocast still runs the
        # matmuls in bf16; this just stores the params/grads in bf16 too.
        model = model.bfloat16()
    model = model.to(device)
    n_params = sum(p.numel() for p in model.parameters())
    print(f"[model] ByteGPT d={args.d} L={args.n_layer} H={args.n_head} block={args.block} "
          f"params={n_params} ({n_params/1e9:.3f}B) grad_ckpt={not args.no_grad_ckpt}", flush=True)

    if args.opt == "adamw8bit":
        import bitsandbytes as bnb
        opt = bnb.optim.AdamW8bit(model.parameters(), lr=args.lr, betas=(0.9, 0.95),
                                  weight_decay=0.1)
        print("[opt] bitsandbytes AdamW8bit (8-bit optimizer states — fits 7B on 80GB)", flush=True)
    else:
        opt = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.1)
        print("[opt] torch AdamW (fp32 states)", flush=True)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / args.warmup
        prog = (step - args.warmup) / max(1, args.steps - args.warmup)
        return args.lr * 0.5 * (1 + math.cos(math.pi * prog)) * 0.9 + args.lr * 0.1 * 0.5

    start_step = 0
    if args.resume and os.path.exists(args.resume):
        ck = torch.load(args.resume, map_location=device)
        model.load_state_dict(ck["model"])
        if "opt" in ck:
            try:
                opt.load_state_dict(ck["opt"])
            except Exception as e:
                print(f"[resume] opt state skipped: {e}", flush=True)
        start_step = int(ck.get("step", 0)) + 1
        print(f"[resume] from {args.resume} at step {start_step}", flush=True)

    def save_ckpt(path, step):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        torch.save({"model": model.state_dict(), "opt": opt.state_dict(),
                    "step": step,
                    "config": {"vocab": 256, "d": args.d, "n_layer": args.n_layer,
                               "n_head": args.n_head, "block": args.block,
                               "n_params": n_params}}, path)

    sampler = UtilSampler(interval=2.0)
    sampler.start()
    curve = []
    model.train()
    t0 = time.time()
    tok_seen = 0
    first_ce = None
    last_ce = None

    for step in range(start_step, args.steps):
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        opt.zero_grad(set_to_none=True)
        for _ in range(args.grad_accum):
            x, y = get_batch(train_data, args.block, args.batch, device)
            with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                _, loss = model(x, y)
                loss = loss / args.grad_accum
            loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        tok_seen += args.batch * args.block * args.grad_accum

        if step % args.eval_every == 0 or step == args.steps - 1:
            model.eval()
            with torch.no_grad():
                vx, vy = get_batch(val_data, args.block, args.batch, device)
                with torch.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, vloss = model(vx, vy)
            model.train()
            ce = float(vloss.item())
            tr = float(loss.item()) * args.grad_accum
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

        if args.ckpt_every and step > 0 and step % args.ckpt_every == 0:
            cpath = os.path.join(os.path.dirname(args.out), f"ckpt_step_{step}.pt")
            save_ckpt(cpath, step)
            print(f"[ckpt] saved {cpath} ({os.path.getsize(cpath)} bytes)", flush=True)

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
        "rung": "7B-scale reference",
        "note": ("7B-scale reference rung, bounded N steps, descent + util demonstrated, "
                 "NOT converged. NOT the hexa-native flame+forge production artifact "
                 "(a_train_flame_forge). a_completeness_over_cheap optional reference. "
                 "Last rung of the Lane-G-ref ladder 85.6M->3.149B->7.25B."),
        "config": {"vocab": 256, "d": args.d, "n_layer": args.n_layer, "n_head": args.n_head,
                   "block": args.block, "batch": args.batch, "grad_accum": args.grad_accum,
                   "steps": args.steps, "n_params": n_params,
                   "grad_ckpt": not args.no_grad_ckpt, "optimizer": args.opt,
                   "model_dtype": args.model_dtype},
        "descent": {"first_val_ce": first_ce, "last_val_ce": last_ce,
                    "F_CLM_REF_7B_DESCENT": 1 if descent else 0, "verdict": "PASS" if descent else "FAIL"},
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
    print(f"=== params={n_params} ({n_params/1e9:.3f}B) ===", flush=True)
    print(f"=== util PEAK={usum['util_peak']:.1f}% MEAN={usum['util_mean']:.2f}% "
          f"mem_peak={usum['mem_peak_mib']:.0f}MiB n={usum['n']} ===", flush=True)
    print(f"=== descent {'PASS' if descent else 'FAIL'} CE {first_ce:.5f} -> {last_ce:.5f} ===", flush=True)
    print(f"=== tok/s={result['throughput']['tok_per_s_final']:.0f} ===", flush=True)
    print(f"=== ckpt sha256={sha} bytes={os.path.getsize(args.out)} ===", flush=True)


if __name__ == "__main__":
    main()
