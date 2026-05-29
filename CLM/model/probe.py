"""Toy routing-balance probe for F-CLM-MONO (NON-GATE, intuition only).

Trains each of the 3 router variants (A / B / AB) briefly on a toy synthetic
byte corpus, across seeds {base=42, 43, 44}, then measures the expert-usage
distribution on a held-out eval stream:

  * expert-usage entropy  (nats; higher = more balanced; max = ln(n_experts))
  * dead-expert count      (experts whose usage fraction < DEAD_THRESH)

It tabulates which variant best balances expert usage AT TOY SCALE, in two
regimes:

  * "tiny"   : the P0 tiny rung (d64/L2/E4), two distinct lanes -- well
               conditioned, easy to balance (often saturates).
  * "stress" : a deliberately monopoly-prone regime (8 experts on a single
               low-diversity band, very short training, high LR) so the three
               arms actually SEPARATE rather than all hitting perfect balance.

This is the toy intuition probe referenced by H_847 (CLM P0 Q4). It is
explicitly NON-GATE: toy-scale balance does NOT decide F-CLM-MONO. The real
verdict is the full-scale 3-arm x ladder fire with the frozen z>3.0 multi-seed
thresholds. (toy != scale; H_666 demonstrated a toy MoE escape that re-collapsed
at scale.) We report exactly what we observe -- including "no variant balances"
if that is what happens (p7 honest reporting).

Run:  python3 -m CLM.model.probe   (from repo root)
  or  python3 CLM/model/probe.py
Set PROBE_JSON_OUT=<path> to also dump the full result JSON.
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Dict, List

import torch

# allow `python3 CLM/model/probe.py` from repo root
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from model import CLMConfig, CLMConvMoE          # noqa: E402
from data import (                                # noqa: E402
    make_synthetic_corpus,
    make_batches,
    lane_tagged_stream,
)

SEEDS = {"base": 42, "43": 43, "44": 44}
VARIANTS = ["A", "B", "AB"]
DEAD_THRESH = 0.01        # usage fraction below this = effectively dead expert
SEQ_LEN = 64
BATCH_SIZE = 16

# Two toy regimes. "tiny" = the P0 tiny rung (well-conditioned, easy to balance).
# "stress" = a deliberately monopoly-prone regime (more experts than the corpus
# needs, short training, high LR) so the three router arms actually SEPARATE
# instead of all saturating at perfect balance. Both are toy / intuition-only.
REGIMES = {
    "tiny": {
        "n_experts": 4,
        "train_steps": 200,
        "lr": 3e-3,
        "two_lane": True,    # distinct web + register bands
    },
    "stress": {
        "n_experts": 8,
        "train_steps": 60,
        "lr": 1e-2,
        "two_lane": False,   # single low-diversity band -> monopoly-prone
    },
}


def _set_seed(s: int) -> None:
    torch.manual_seed(s)


def _measure_usage(model: CLMConvMoE, eval_batches) -> torch.Tensor:
    """Mean per-expert routing usage over the eval set."""
    model.eval()
    acc = None
    n = 0
    with torch.no_grad():
        for x, y in eval_batches:
            out = model(x, y)
            u = out["usage"]
            acc = u.clone() if acc is None else acc + u
            n += 1
    return acc / max(1, n)


def _usage_entropy(usage: torch.Tensor) -> float:
    p = usage / (usage.sum() + 1e-9)
    return float(-(p * torch.log(p + 1e-9)).sum())


def _dead_count(usage: torch.Tensor) -> int:
    p = usage / (usage.sum() + 1e-9)
    return int((p < DEAD_THRESH).sum())


def _build_stream(regime: Dict, seed: int) -> List[int]:
    web, reg = make_synthetic_corpus(n_bytes_per_lane=8192, seed=seed)
    if regime["two_lane"]:
        stream, _lane = lane_tagged_stream(web, reg, block=64)
        return stream
    # single low-diversity band: use only the web lane (repeating low-band
    # motifs) -- there is little reason for the router to use many experts,
    # which is exactly the monopoly-prone setup we want to stress.
    return web


def train_one(variant: str, seed: int, regime: Dict) -> Dict:
    _set_seed(seed)
    cfg = CLMConfig(variant=variant, n_experts=regime["n_experts"])
    model = CLMConvMoE(cfg)

    stream = _build_stream(regime, seed)
    steps = regime["train_steps"]
    train_batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, steps, seed=seed)
    eval_batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, 16, seed=seed + 999)

    opt = torch.optim.Adam(model.parameters(), lr=regime["lr"])
    model.train()
    last_loss = float("nan")
    for x, y in train_batches:
        opt.zero_grad()
        out = model(x, y)
        out["loss"].backward()
        opt.step()
        last_loss = float(out["ce_loss"].detach())

    usage = _measure_usage(model, eval_batches)
    n_e = cfg.n_experts
    ent = _usage_entropy(usage)
    return {
        "variant": variant,
        "seed": seed,
        "n_experts": n_e,
        "usage": [round(float(u), 4) for u in (usage / (usage.sum() + 1e-9))],
        "usage_entropy": round(ent, 4),
        "max_entropy": round(math.log(n_e), 4),
        "balance_ratio": round(ent / math.log(n_e), 4),
        "dead_experts": _dead_count(usage),
        "final_ce": round(last_loss, 4),
        "params": model.num_params(),
    }


def run_regime(regime_name: str, regime: Dict) -> Dict:
    results: List[Dict] = []
    print(f"\n########## REGIME: {regime_name} "
          f"(E={regime['n_experts']}, steps={regime['train_steps']}, "
          f"lr={regime['lr']}, two_lane={regime['two_lane']}) ##########",
          flush=True)
    for variant in VARIANTS:
        for label, seed in SEEDS.items():
            r = train_one(variant, seed, regime)
            r["seed_label"] = label
            results.append(r)
            print(
                f"[{variant:>2} {label:>4}] usage={r['usage']} "
                f"H={r['usage_entropy']:.3f}/{r['max_entropy']:.3f} "
                f"(ratio {r['balance_ratio']:.3f}) dead={r['dead_experts']} "
                f"ce={r['final_ce']:.3f}",
                flush=True,
            )

    agg: Dict[str, Dict] = {}
    for variant in VARIANTS:
        rs = [r for r in results if r["variant"] == variant]
        agg[variant] = {
            "mean_usage_entropy": round(sum(r["usage_entropy"] for r in rs) / len(rs), 4),
            "mean_balance_ratio": round(sum(r["balance_ratio"] for r in rs) / len(rs), 4),
            "mean_dead_experts": round(sum(r["dead_experts"] for r in rs) / len(rs), 4),
            "max_dead_experts": max(r["dead_experts"] for r in rs),
        }

    best = max(
        VARIANTS,
        key=lambda v: (agg[v]["mean_balance_ratio"], -agg[v]["mean_dead_experts"]),
    )

    print(f"--- {regime_name} AGGREGATE (mean over seeds) ---", flush=True)
    for v in VARIANTS:
        a = agg[v]
        print(
            f"ARM {v:>2}: meanH={a['mean_usage_entropy']:.3f} "
            f"ratio={a['mean_balance_ratio']:.3f} "
            f"meanDead={a['mean_dead_experts']:.2f} maxDead={a['max_dead_experts']}",
            flush=True,
        )
    print(f"best-balanced ({regime_name}, non-gate): ARM {best}", flush=True)

    return {
        "regime": regime,
        "per_run": results,
        "per_variant_mean": agg,
        "best_balanced_variant": best,
    }


def main() -> None:
    out = {
        "config": {
            "variants": VARIANTS,
            "seeds": SEEDS,
            "seq_len": SEQ_LEN,
            "batch_size": BATCH_SIZE,
            "dead_thresh": DEAD_THRESH,
            "scale": "tiny (d64/L2) toy synthetic corpus -- INTUITION ONLY, non-gate",
        },
        "regimes": {},
        "torch_version": torch.__version__,
    }
    for name, regime in REGIMES.items():
        out["regimes"][name] = run_regime(name, regime)

    dest = os.environ.get("PROBE_JSON_OUT")
    if dest:
        with open(dest, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nwrote JSON -> {dest}", flush=True)


if __name__ == "__main__":
    main()
