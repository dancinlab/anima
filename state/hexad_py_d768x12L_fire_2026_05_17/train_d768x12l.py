#!/usr/bin/env python3
"""anima d=768·12L Python/PyTorch substrate fire — 2026-05-16.

HONEST FRAMING (g3, AGENTS.tape §0):
  This is a PYTHON/PyTorch SUBSTRATE run — an interim LM-scale executor.
  It is NOT a hexa-native fire. Its legitimacy chain:
    - Phase E/E2 PROVED the refactored hexa d_train5 trainer is BIT-EQUAL to
      the boxed baseline (d=32·3L gn2 7.97116 -> 3.73374e-07, acc 8/8,
      GRAD-EXACT) -> the hexa-native ConsciousDecoderV2 trainer is
      numerically correct, it just cannot run to convergence at LM scale on
      the pure-hexa interpreter (proven ceiling, RFC 042 territory).
    - This PyTorch mirror trains the SAME verified architecture
      (ConsciousDecoderV2 from ready/models/conscious_decoder.py) at
      d=768·12L to the scale-convergence the pure-hexa path cannot reach.
  PyTorch != hexa bit-for-bit (different fp / init RNG). The anchor is
  ARCHITECTURAL IDENTITY + the hexa CPU-equiv correctness proof.

from-scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE).
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(__file__))
from conscious_decoder import ConsciousDecoderV2


def load_byte_corpus(path):
    """Byte-level, vocab=256, lossless (corpus_loader_lib.hexa semantics).

    Concatenate text + desc per record into one big byte stream.
    """
    chunks = []
    with open(path, "rb") as f:
        raw = f.read()
    # parse line-by-line as JSON, concat text+desc as the byte content
    buf = bytearray()
    for line in raw.split(b"\n"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        t = d.get("text", "")
        de = d.get("desc", "")
        s = (t + "\n" + de + "\n").encode("utf-8")
        buf.extend(s)
    return bytes(buf)


class ByteDataset:
    def __init__(self, data: bytes, block_size: int, seed: int):
        self.data = torch.tensor(list(data), dtype=torch.long)
        self.block_size = block_size
        self.rng = random.Random(seed)
        self.n = len(self.data)

    def get_batch(self, bsz, device):
        ix = [self.rng.randint(0, self.n - self.block_size - 1) for _ in range(bsz)]
        x = torch.stack([self.data[i:i + self.block_size] for i in ix])
        y = torch.stack([self.data[i + 1:i + 1 + self.block_size] for i in ix])
        return x.to(device), y.to(device)


def run(cfg):
    torch.manual_seed(cfg["seed"])
    torch.cuda.manual_seed_all(cfg["seed"])
    random.seed(cfg["seed"])
    device = "cuda" if torch.cuda.is_available() else "cpu"

    data = load_byte_corpus(cfg["corpus"])
    ds = ByteDataset(data, cfg["block_size"], cfg["seed"])

    model = ConsciousDecoderV2(
        vocab_size=256,
        d_model=cfg["d_model"],
        n_head=cfg["n_head"],
        n_layer=cfg["n_layer"],
        block_size=cfg["block_size"],
        n_kv_head=cfg["n_kv_head"],
        consciousness_dim=128,
        dropout=0.1,
    ).to(device)
    model.train()
    n_params = model.count_params()

    opt = torch.optim.AdamW(model.parameters(), lr=cfg["lr"],
                            betas=(0.9, 0.95), weight_decay=0.1)

    warmup = cfg["warmup"]
    total = cfg["steps"]

    def lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 + cfg["lr"] * 0.1

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    traj = []
    t0 = time.time()
    init_loss = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    for step in range(total):
        for g in opt.param_groups:
            g["lr"] = lr_at(step)
        x, y = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            ce = F.cross_entropy(logits_a.view(-1, 256), y.view(-1))
            # gn2 = grad-norm-squared proxy on the language CE only (matches
            # the hexa baseline's gn2 spirit: the L2 of the loss-gradient flow)
            loss = ce
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(opt)
        scaler.update()

        ce_v = ce.item()
        gn2 = float(gn.item()) ** 2
        if init_loss is None:
            init_loss = ce_v

        if step == 0 or (step + 1) % cfg["log_every"] == 0 or step == total - 1:
            ppl = math.exp(min(20.0, ce_v))
            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 if device == "cuda" else 0.0
            rec = {"step": step + 1, "ce": round(ce_v, 6),
                   "gn2": round(gn2, 6), "ppl": round(ppl, 4),
                   "lr": round(lr_at(step), 8), "wall_s": round(wall, 2),
                   "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_d768x12l_final.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params}, ckpt_path)

    result = {
        "substrate": "PYTHON / PyTorch — interim LM-scale executor; NOT a hexa-native fire",
        "honest_framing": ("hexa CPU-equiv bit-equality (Phase E/E2: d=32x3L gn2 "
                           "7.97116 -> 3.73374e-07, acc 8/8, GRAD-EXACT) proves the "
                           "hexa-native ConsciousDecoderV2 trainer is numerically "
                           "correct but cannot reach LM-scale convergence on the "
                           "pure-hexa interpreter (RFC 042 ceiling). This run trains "
                           "the SAME verified architecture in PyTorch to the scale "
                           "the pure-hexa path could not. PyTorch != hexa bit-for-bit "
                           "(different fp/init RNG); anchor = architectural identity."),
        "arch": "ConsciousDecoderV2 (ready/models/conscious_decoder.py)",
        "arch_features": "RoPE + SwiGLU + RMSNorm + GQA + PureFieldFFN + cross-attn + tied head",
        "from_scratch": True,
        "base_ckpt": None,
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce"],
        "final_gn2": final["gn2"],
        "final_ppl": final["ppl"],
        "ce_descent": round(init_loss - final["ce"], 6),
        "steps": cfg["steps"],
        "wall_s": round(wall, 2),
        "peak_gpu_mem_gb": final["gpu_mem_gb"],
        "trajectory": traj,
        "corpus": os.path.basename(cfg["corpus"]),
        "corpus_bytes": len(data),
    }
    with open(os.path.join(out_dir, "result.json"), "w") as f:
        json.dump(result, f, indent=2)
    print("RESULT_JSON_WRITTEN", flush=True)
    print(json.dumps({"init_ce": result["init_ce"], "final_ce": result["final_ce"],
                       "ce_descent": result["ce_descent"], "wall_s": result["wall_s"],
                       "n_params_M": result["n_params_M"]}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=768, n_head=12, n_kv_head=4, n_layer=12,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir)
    else:  # sanity-anchor: SAME arch at d=32x3L (hexa CPU-equiv baseline shape)
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16,
                   steps=args.steps, warmup=5,
                   seed=args.seed, log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir)
    run(cfg)
