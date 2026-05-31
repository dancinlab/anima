#!/usr/bin/env python3
"""STAGE 2 — CLM P2 3-arm x ladder x multiseed full-fire driver.

Wraps the LANDED train_clm.py QAT machinery (AKIDA envelope: int4-sym weights
+ act_bits STE), trains each (arm, rung, seed) to real convergence on the
crawled corpus, and PERSISTS:
  * ckpt_{arm}_{rung}_{seed}.pt   (state_dict, fp32 master -> shadow)
  * curve_{arm}_{rung}_{seed}.json (CE/step + step-rate for d5 re-measure)

This is the payload H_847 / H_850 fire runs. Inference stays AKIDA-int4-only.
"""
from __future__ import annotations
import argparse, json, os, sys, time
import torch
torch.backends.cudnn.enabled = False  # ubu-1 cuDNN version mismatch; native CUDA conv works

_HERE = os.path.dirname(os.path.abspath(__file__))
_TRAIN = os.path.join(os.path.dirname(_HERE), "train")
for p in (_HERE, _TRAIN, os.path.join(os.path.dirname(_HERE), "model")):
    if p not in sys.path: sys.path.insert(0, p)

from train_clm import (build, QATConfig, _install_functional_qat, ConvQATHook,
                       qat_loss, LADDER)            # noqa: E402
from model import CLMConfig, CLMConvMoE             # noqa: E402
from data import make_batches                       # noqa: E402


def _read_bytes_file(path):
    vals = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line: vals.append(int(line) & 0xFF)
    return vals


def load_mixed_stream(web_path, reg_path, ratio_web=0.8, block=256):
    """Interleave web/register at the target byte ratio (P0 d1 = 80:20)."""
    web = _read_bytes_file(web_path); reg = _read_bytes_file(reg_path)
    stream = []
    iw = ir = 0
    # emit web:reg blocks at 4:1 (≈80:20)
    while iw < len(web) or ir < len(reg):
        for _ in range(4):
            if iw < len(web):
                stream.extend(web[iw:iw+block]); iw += block
        if ir < len(reg):
            stream.extend(reg[ir:ir+block]); ir += block
        if iw >= len(web) and ir >= len(reg): break
    return stream, len(web), len(reg)


def fire_one(arm, rung, seed, web_path, reg_path, steps, seq_len, batch_size, lr,
             act_bits, envelope_lambda, out_dir, device):
    torch.manual_seed(seed)
    qcfg = QATConfig(act_bits=act_bits, envelope_lambda=envelope_lambda)
    qcfg.validate()
    model = build(arm, rung).to(device)
    _install_functional_qat(model, qcfg)
    aq_hook = ConvQATHook(model, QATConfig(act_bits=act_bits, quant_weights=False,
                                           quant_acts=True))
    stream, nweb, nreg = load_mixed_stream(web_path, reg_path)
    batches = make_batches(stream, seq_len, batch_size, steps, seed=seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)
    model.train()
    curve = []; t0 = time.time()
    with aq_hook:
        for i, (x, y) in enumerate(batches):
            x = x.to(device); y = y.to(device)
            opt.zero_grad()
            diag = qat_loss(model, x, y, qcfg)
            diag["loss"].backward()
            opt.step()
            ce = float(diag["ce"])
            if i % max(1, steps // 50) == 0 or i == steps - 1:
                curve.append({"step": i, "ce": round(ce, 5)})
    dt = time.time() - t0
    step_rate = steps / dt if dt > 0 else float("inf")
    os.makedirs(out_dir, exist_ok=True)
    ck = os.path.join(out_dir, f"ckpt_{arm}_{rung}_{seed}.pt")
    torch.save(model.state_dict(), ck)
    res = {"arm": arm, "rung": rung, "seed": seed, "steps": steps,
           "params": model.num_params(), "device": str(device),
           "first_ce": curve[0]["ce"], "last_ce": curve[-1]["ce"],
           "wall_s": round(dt, 3), "step_rate_per_s": round(step_rate, 4),
           "act_bits": act_bits, "envelope_lambda": envelope_lambda,
           "corpus_web_bytes": nweb, "corpus_reg_bytes": nreg,
           "stream_bytes": len(stream), "ckpt": ck, "curve": curve}
    with open(os.path.join(out_dir, f"curve_{arm}_{rung}_{seed}.json"), "w") as f:
        json.dump(res, f, indent=2)
    print(f"[{arm:>2} {rung:>5} s{seed}] ce {curve[0]['ce']:.3f}->{curve[-1]['ce']:.3f} "
          f"step_rate={step_rate:.2f}/s wall={dt:.1f}s params={model.num_params()} -> {ck}",
          flush=True)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--web", required=True); ap.add_argument("--register", required=True)
    ap.add_argument("--arms", default="A,B,AB"); ap.add_argument("--rungs", default="tiny,small")
    ap.add_argument("--seeds", default="42,43,44")
    ap.add_argument("--steps", type=int, default=2000)
    ap.add_argument("--seq-len", type=int, default=64); ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--lr", type=float, default=3e-3); ap.add_argument("--act-bits", type=int, default=4)
    ap.add_argument("--envelope-lambda", type=float, default=0.0)
    ap.add_argument("--out-dir", default="ckpts"); ap.add_argument("--json-out", default=None)
    a = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"device={device} torch={torch.__version__}", flush=True)
    allres = []
    for arm in a.arms.split(","):
        for rung in a.rungs.split(","):
            for seed in [int(s) for s in a.seeds.split(",")]:
                allres.append(fire_one(arm, rung, seed, a.web, a.register, a.steps,
                              a.seq_len, a.batch_size, a.lr, a.act_bits,
                              a.envelope_lambda, a.out_dir, device))
    summary = {"runs": allres, "device": device, "torch": torch.__version__,
               "mean_step_rate": round(sum(r["step_rate_per_s"] for r in allres)/len(allres), 4)}
    if a.json_out:
        with open(a.json_out, "w") as f: json.dump(summary, f, indent=2)
    print(f"\nmean step-rate (production GPU re-measure, d5): {summary['mean_step_rate']}/s", flush=True)


if __name__ == "__main__":
    main()
