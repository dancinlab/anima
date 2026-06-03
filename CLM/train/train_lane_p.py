#!/usr/bin/env python3
"""Lane P (GPU-torch) — REAL converged CLMConvMoE trainer for the E=2/L1 decoder.

substrate = GPU-torch (Lane P), distinct from Lane A (AKIDA) / Lane G (forge).
a_lane_akida_gpu_split — this is the torch CE-descent path, NOT forge util.

Trains a CLMConvMoE(n_experts=2, n_trunk_layers=1, d_model=D) to convergence on
a byte corpus (V=256, no tokenizer), saves a torch state_dict, and serializes to
a CORE/clm_decode.hexa-loadable CLM\\x01 v0.2 .clm via serialize_v2.

NO QAT on the training path: the production CE-descent is plain next-byte CE
(bf16 autocast on CUDA, AdamW). The serializer applies its own int4-sym
per-output-channel quant at EXPORT time, and the decoder dequants w=code*scale
directly at inference — so train fp/bf16, export int4-sym, decode dequant. This
keeps the honest CE-descent un-coupled from QAT artefacts (the decoder does not
re-QAT).

CE-descent is captured VERBATIM (start CE, periodic CE, final CE). NO fabrication
(g63/p7): printed numbers are the live optimizer's mean CE per logged window.
"""
from __future__ import annotations

import argparse, json, os, sys, time

import torch
import torch.nn as nn
import torch.nn.functional as F

_HERE = os.path.dirname(os.path.abspath(__file__))
_CLM = os.path.dirname(_HERE)
_MODEL = os.path.join(_CLM, "model")
if _MODEL not in sys.path:
    sys.path.insert(0, _MODEL)

from model import CLMConfig, CLMConvMoE          # noqa: E402
import clm_serialize_v2 as S                      # noqa: E402


def load_byte_stream(path: str) -> torch.Tensor:
    with open(path, "rb") as f:
        raw = f.read()
    return torch.frombuffer(bytearray(raw), dtype=torch.uint8).long()


def make_batch(stream, seq_len, batch_size, device, gen):
    n = stream.numel()
    ix = torch.randint(0, n - seq_len - 1, (batch_size,), generator=gen)
    x = torch.stack([stream[i:i + seq_len] for i in ix]).to(device)
    y = torch.stack([stream[i + 1:i + 1 + seq_len] for i in ix]).to(device)
    return x, y


@torch.no_grad()
def eval_ce(model, stream, seq_len, batch_size, device, gen, iters=20):
    model.eval()
    tot = 0.0
    for _ in range(iters):
        x, y = make_batch(stream, seq_len, batch_size, device, gen)
        out = model(x, y)
        tot += float(out["ce_loss"])
    model.train()
    return tot / iters


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--d-model", type=int, default=768)
    ap.add_argument("--steps", type=int, default=6000)
    ap.add_argument("--seq-len", type=int, default=256)
    ap.add_argument("--batch-size", type=int, default=64)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--warmup", type=int, default=200)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--ckpt-out", required=True)
    ap.add_argument("--clm-out", required=True)
    ap.add_argument("--json-out", default=None)
    ap.add_argument("--log-every", type=int, default=100)
    ap.add_argument("--bf16", action="store_true")
    a = ap.parse_args()

    torch.manual_seed(a.seed)
    gen = torch.Generator().manual_seed(a.seed)

    assert torch.cuda.is_available(), "CUDA REQUIRED for Lane P production rung (g63: no silent CPU)"
    device = "cuda"
    cap = torch.cuda.get_device_capability()
    print(f"DEVICE cuda name={torch.cuda.get_device_name(0)} cap={cap[0]}.{cap[1]} "
          f"torch={torch.__version__}", flush=True)

    # HARD CONSTRAINT: decoder-fixed E=2 / 1 trunk layer.
    cfg = CLMConfig(n_experts=2, n_trunk_layers=1, d_model=a.d_model,
                    kernel_size=3, variant="AB")
    model = CLMConvMoE(cfg).to(device)
    n_params = model.num_params()
    print(f"PARAMS n_params={n_params} ({n_params/1e6:.3f}M) "
          f"d={a.d_model} E={cfg.n_experts} L={cfg.n_trunk_layers} K={cfg.kernel_size} V={cfg.vocab_size}",
          flush=True)

    stream = load_byte_stream(a.corpus)
    print(f"CORPUS path={a.corpus} bytes={stream.numel()}", flush=True)

    opt = torch.optim.AdamW(model.parameters(), lr=a.lr, betas=(0.9, 0.95),
                            weight_decay=0.01)
    sched = torch.optim.lr_scheduler.LambdaLR(
        opt, lambda s: min((s + 1) / a.warmup, 1.0) *
                       (0.5 * (1 + torch.cos(torch.tensor(
                           3.14159265 * min(s, a.steps) / a.steps)).item())
                        if s >= a.warmup else 1.0))

    use_bf16 = a.bf16
    model.train()
    t0 = time.time()
    descent = []   # (step, ce) verbatim
    first_ce = None
    for step in range(a.steps):
        x, y = make_batch(stream, a.seq_len, a.batch_size, device, gen)
        opt.zero_grad(set_to_none=True)
        if use_bf16:
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y)
                loss = out["loss"]
            loss.backward()
        else:
            out = model(x, y)
            loss = out["loss"]
            loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        sched.step()
        ce = float(out["ce_loss"])
        if first_ce is None:
            first_ce = ce
        if step % a.log_every == 0 or step == a.steps - 1:
            descent.append((step, round(ce, 5)))
            print(f"STEP {step:6d} ce={ce:.5f} loss={float(loss):.5f} "
                  f"lr={sched.get_last_lr()[0]:.2e} aux={float(out['aux_loss']):.4f} "
                  f"ent={float(out['routing_entropy']):.4f}", flush=True)
    wall = time.time() - t0

    final_eval = eval_ce(model, stream, a.seq_len, a.batch_size, device, gen, iters=40)
    print(f"FINAL_EVAL_CE {final_eval:.5f}  (held-window mean over 40 batches)", flush=True)
    print(f"DESCENT first_ce={first_ce:.5f} last_logged_ce={descent[-1][1]:.5f} "
          f"eval_ce={final_eval:.5f} uniform_ln256={5.5452:.5f}", flush=True)

    # save state_dict
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    torch.save(sd, a.ckpt_out)
    print(f"CKPT saved {a.ckpt_out} ({os.path.getsize(a.ckpt_out)} bytes)", flush=True)

    # serialize -> .clm (serialize_v2 asserts E=2/L1)
    p = S.serialize_v2(sd, cfg, a.clm_out)
    sz = os.path.getsize(p)
    print(f"CLM serialized {p} ({sz} bytes)", flush=True)

    result = {
        "substrate": "GPU-torch",
        "device": torch.cuda.get_device_name(0),
        "compute_cap": f"{cap[0]}.{cap[1]}",
        "torch": torch.__version__,
        "d_model": a.d_model, "n_experts": cfg.n_experts,
        "n_trunk_layers": cfg.n_trunk_layers, "kernel_size": cfg.kernel_size,
        "vocab": cfg.vocab_size, "n_params": n_params,
        "steps": a.steps, "seq_len": a.seq_len, "batch_size": a.batch_size,
        "lr": a.lr, "bf16": use_bf16, "wall_s": round(wall, 2),
        "first_ce": round(first_ce, 5),
        "last_train_ce": descent[-1][1],
        "final_eval_ce": round(final_eval, 5),
        "uniform_ce_ln256": 5.5452,
        "descent": descent,
        "corpus": a.corpus, "corpus_bytes": stream.numel(),
        "clm_out": p, "clm_bytes": sz,
    }
    if a.json_out:
        with open(a.json_out, "w") as f:
            json.dump(result, f, indent=2)
    print("RESULT " + json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
