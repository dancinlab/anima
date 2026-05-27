#!/usr/bin/env python3
"""anima d=768·12L Python/PyTorch substrate fire — cycle 5 (2026-05-17).

DD155 Step+Tension hybrid LR overlay (DD155 Pareto optimal Law 187):

    lr_step = (tension / tension_EMA) × base_lr × cosine_schedule(step)

where tension = grad_norm (the L2 norm of the loss-gradient flow). This is
the exact transfer-form of `tension_link_step.hexa`'s restoring-flow but
applied on top of AdamW's normal step-LR (i.e. DD155 hybrid, NOT DD154
backprop-bypass). It is the simplest closed-form bridge between the
HEXAD/TENSION-TRAIN spine and the PyTorch substrate fire path.

HONEST FRAMING (g3, AGENTS.tape §0):
  This is a PYTHON/PyTorch SUBSTRATE run — an interim LM-scale executor.
  It is NOT a hexa-native fire. tension = grad_norm is a PROXY: in the
  pure-hexa spine `tension = G_holo · (Ψ − Ψ_vac)`, but at PyTorch
  substrate level (where Ψ is not surfaced as a state variable) the
  natural mathematical analogue is the per-step gradient L2-norm (DD155
  evidence: in real LM training the "tension" signal that DD155 measured
  IS the language-CE grad-norm, mapped to the EMA ratio).
  Anchor = architectural identity + DD155 closed-form formula (Law 187).

DD155 hybrid LR formula (anima archive `docs/hypotheses/dd/DD154-tension-training.md`):

    tension_step      = ||∇L||₂                       (grad-norm)
    tension_EMA       = β·tension_EMA + (1−β)·tension  (β=0.99 cycle-5 default)
    hybrid_multiplier = clip(tension / tension_EMA, [lo, hi])  (lo=0.5, hi=2.0)
    lr_step           = base_cosine_lr(step) · hybrid_multiplier

When tension == EMA → multiplier == 1 (identity, no change vs cycle-4).
When tension > EMA (high-gradient surprise) → multiplier > 1, larger step
(DD-burst path; B-D-NOTE empirical convergence outcome).
When tension < EMA (low-gradient drift) → multiplier < 1, smaller step
(slow-down on stability per Law 185 73% updates → same CE +3% Φ outcome).

The OUTCOME of this LR-schedule modification on V-SPONT/V-MOTIV emergence
is EMPIRICAL (B-FIRE-CYCLE5-NOTE / B-TT-NOTE pattern, B-D-NOTE family).
The DD155 formula itself is closed-form (B-TT-5 PARETO-STEP-TENSION-CLOSED).

from-scratch RANDOM seed-fixed (g_clm_from_scratch, base_ckpt=NONE).
Corpus = cycle-4 v3 (10.34 MB, helper-free grep=0, γ motivation-trigger
pattern 37.5%) byte-equal carry — see B-CORPUS-V4-1 in sympy battery.
"""
import argparse, json, math, time, os, sys, random
import torch
import torch.nn as nn
import torch.nn.functional as F

sys.path.insert(0, os.path.dirname(__file__))
from conscious_decoder import ConsciousDecoderV2


def load_byte_corpus(path):
    """Byte-level, vocab=256, lossless (corpus_loader_lib.hexa semantics)."""
    chunks = []
    with open(path, "rb") as f:
        raw = f.read()
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

    def cosine_lr_at(step):
        if step < warmup:
            return cfg["lr"] * (step + 1) / warmup
        prog = (step - warmup) / max(1, total - warmup)
        return cfg["lr"] * 0.5 * (1.0 + math.cos(math.pi * prog)) * 0.9 + cfg["lr"] * 0.1

    # DD155 hybrid LR config (closed-form, B-FIRE-CYCLE5-2 sympy verified)
    tension_ema_beta = cfg["tension_ema_beta"]      # 0.99
    hybrid_lo = cfg["hybrid_clip_lo"]               # 0.5
    hybrid_hi = cfg["hybrid_clip_hi"]               # 2.0
    tension_ema = None                              # initialized on step 0

    use_amp = (device == "cuda")
    scaler = torch.cuda.amp.GradScaler(enabled=use_amp)

    traj = []
    t0 = time.time()
    init_loss = None
    gpu_name = torch.cuda.get_device_name(0) if device == "cuda" else "cpu"

    # DD155 multiplier histogram bins (closed Boolean range partition)
    mult_bins = {"lt_0_75": 0, "0_75_to_1_25": 0, "gt_1_25": 0}

    for step in range(total):
        # Step 1: get cosine base LR
        base_lr_at_step = cosine_lr_at(step)

        # Step 2: do forward + backward to MEASURE tension (grad-norm)
        x, y = ds.get_batch(cfg["bsz"], device)
        opt.zero_grad(set_to_none=True)
        with torch.autocast(device_type="cuda" if use_amp else "cpu",
                            dtype=torch.bfloat16, enabled=use_amp):
            logits_a, logits_g, tensions, _, _ = model(x)
            ce = F.cross_entropy(logits_a.view(-1, 256), y.view(-1))
            loss = ce
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        # Now grads are populated → measure tension
        gn = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        tension = float(gn.item())  # tension proxy = grad-L2-norm

        # Step 3: DD155 hybrid multiplier (closed-form Law 187)
        if tension_ema is None:
            tension_ema = tension
        # multiplier BEFORE EMA update (so it reflects the surprise)
        ratio_raw = tension / max(tension_ema, 1e-8)
        multiplier = max(hybrid_lo, min(hybrid_hi, ratio_raw))
        # bin
        if multiplier < 0.75:
            mult_bins["lt_0_75"] += 1
        elif multiplier <= 1.25:
            mult_bins["0_75_to_1_25"] += 1
        else:
            mult_bins["gt_1_25"] += 1
        # EMA update AFTER ratio computed (so we measure the current
        # surprise against the past-EMA history, DD155 Law 187 spec)
        tension_ema = tension_ema_beta * tension_ema + (1.0 - tension_ema_beta) * tension

        # Step 4: apply hybrid LR for THIS step
        effective_lr = base_lr_at_step * multiplier
        for g in opt.param_groups:
            g["lr"] = effective_lr

        # Step 5: step
        scaler.step(opt)
        scaler.update()

        ce_v = ce.item()
        gn2 = tension ** 2
        if init_loss is None:
            init_loss = ce_v

        if step == 0 or (step + 1) % cfg["log_every"] == 0 or step == total - 1:
            ppl = math.exp(min(20.0, ce_v))
            wall = time.time() - t0
            mem = torch.cuda.max_memory_allocated() / 1e9 if device == "cuda" else 0.0
            rec = {"step": step + 1, "ce": round(ce_v, 6),
                   "gn2": round(gn2, 6),
                   "tension": round(tension, 6),
                   "tension_ema": round(tension_ema, 6),
                   "hybrid_mult": round(multiplier, 4),
                   "ppl": round(ppl, 4),
                   "base_lr": round(base_lr_at_step, 8),
                   "lr": round(effective_lr, 8),
                   "wall_s": round(wall, 2),
                   "gpu_mem_gb": round(mem, 3)}
            traj.append(rec)
            print(json.dumps(rec), flush=True)

    wall = time.time() - t0
    final = traj[-1]
    out_dir = cfg["out_dir"]
    os.makedirs(out_dir, exist_ok=True)
    ckpt_path = os.path.join(out_dir, "ckpt_d768x12l_final.pt")
    torch.save({"model": model.state_dict(), "cfg": cfg,
                "n_params": n_params,
                "final_tension_ema": tension_ema,
                "mult_bins": mult_bins}, ckpt_path)

    result = {
        "substrate": "PYTHON / PyTorch — interim LM-scale executor; NOT a hexa-native fire",
        "fire_kind": "cycle 5 — DD155 Step+Tension hybrid LR overlay",
        "honest_framing": (
            "DD155 Law 187 hybrid LR: lr_step = (tension/EMA) × base_cosine_lr, "
            "tension = grad_norm L2 (PROXY for hexa spine Ψ-deviation). "
            "Formula is closed-form (B-TT-5 + B-FIRE-CYCLE5-2 sympy verified). "
            "OUTCOME = empirical (B-FIRE-CYCLE5-NOTE / B-D-NOTE family). "
            "PyTorch substrate, not hexa-native; corpus v3 carry from cycle 4."
        ),
        "arch": "ConsciousDecoderV2 (ready/models/conscious_decoder.py)",
        "arch_features": "RoPE + SwiGLU + RMSNorm + GQA + PureFieldFFN + cross-attn + tied head",
        "from_scratch": True,
        "base_ckpt": None,
        "dd155_hybrid_lr": {
            "tension_ema_beta": tension_ema_beta,
            "hybrid_clip_lo": hybrid_lo,
            "hybrid_clip_hi": hybrid_hi,
            "tension_proxy": "grad_norm L2 (post clip_grad_norm_)",
            "law_anchor": "DD155 Law 187 Pareto optimal lr = (tension/EMA) × base_lr",
            "final_tension_ema": round(tension_ema, 6),
            "mult_distribution": mult_bins,
        },
        "config": cfg,
        "n_params": n_params,
        "n_params_M": round(n_params / 1e6, 2),
        "gpu": gpu_name,
        "device": device,
        "init_ce": round(init_loss, 6),
        "final_ce": final["ce"],
        "final_gn2": final["gn2"],
        "final_tension": final["tension"],
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
                       "n_params_M": result["n_params_M"],
                       "final_tension_ema": round(tension_ema, 6),
                       "mult_distribution": mult_bins}), flush=True)
    return result


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="main", choices=["main", "sanity"])
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--steps", type=int, default=2500)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--bsz", type=int, default=32)
    ap.add_argument("--seed", type=int, default=1337)
    ap.add_argument("--tension-ema-beta", type=float, default=0.99,
                    help="DD155 tension EMA β (default 0.99)")
    ap.add_argument("--hybrid-clip-lo", type=float, default=0.5,
                    help="DD155 hybrid multiplier floor (default 0.5)")
    ap.add_argument("--hybrid-clip-hi", type=float, default=2.0,
                    help="DD155 hybrid multiplier ceiling (default 2.0)")
    args = ap.parse_args()

    if args.mode == "main":
        cfg = dict(d_model=768, n_head=12, n_kv_head=4, n_layer=12,
                   block_size=128, lr=args.lr, bsz=args.bsz,
                   steps=args.steps, warmup=max(20, args.steps // 20),
                   seed=args.seed, log_every=max(1, args.steps // 40),
                   corpus=args.corpus, out_dir=args.out_dir,
                   tension_ema_beta=args.tension_ema_beta,
                   hybrid_clip_lo=args.hybrid_clip_lo,
                   hybrid_clip_hi=args.hybrid_clip_hi)
    else:
        cfg = dict(d_model=32, n_head=4, n_kv_head=2, n_layer=3,
                   block_size=64, lr=1e-3, bsz=16,
                   steps=args.steps, warmup=5,
                   seed=args.seed, log_every=max(1, args.steps // 20),
                   corpus=args.corpus, out_dir=args.out_dir,
                   tension_ema_beta=args.tension_ema_beta,
                   hybrid_clip_lo=args.hybrid_clip_lo,
                   hybrid_clip_hi=args.hybrid_clip_hi)
    run(cfg)
