"""H_871 — routing-z = measurement-artifact (M1) scale-ladder test.

ROADMAP M1 suspicion (CLM/P4_PRODUCTION_ROADMAP.md @L3): the toy routing-z RED
(H_847/H_850/H_852/H_853 — near-uniform / negative routing-diversity z) is a
SCALE ARTIFACT, not a real ceiling. This harness measures the SAME
routing-diversity z (verbatim from CLM/model/judge_clm.routing_z) at MULTIPLE
rung sizes on the REAL kowiki corpus and reports whether z RISES monotonically
with rung size (and the margin vs the 3.0 chip-array gate).

routing-z (verbatim CLM/model/judge_clm.routing_z):
    obs  = mean per-token router entropy (nats) on a held-out eval stream.
    null = entropies of random usage vectors ~ Dirichlet(1) over E experts.
    z    = (obs - mu_null) / sd_null.   F-CLM-MONO chip-array gate = z > 3.0.

Ladder (d_model / n_trunk_layers / n_experts), arm AB (= H_863 production arm):
    tiny  = d64  / L2 / E4   (P0 toy rung — the RED origin; H_850 arm-AB rz~0.97)
    small = d256 / L4 / E8   (P0 small rung;               H_850 arm-AB rz~1.91)
    mid   = d512 / L8 / E8   (H_863 production rung — NEW, never z-measured)

PRE-REGISTERED (F-CLM-ROUTING-Z-SCALE_prereg.txt, frozen pre-fire):
  PASS (artifact CONFIRMED) iff mean routing-z(rung) is MONOTONE NON-DECREASING
  tiny<=small<=mid AND mid_mean_z - tiny_mean_z >= MARGIN(0.5); else RED (real
  ceiling). Either outcome is honest (a_paper_negative_ok). Measured by CODE.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Dict, List

import torch

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from model import CLMConfig, CLMConvMoE          # noqa: E402
from data import make_batches, lane_tagged_stream  # noqa: E402
from stage2_real_corpus import make_real_corpus    # noqa: E402

SEQ_LEN = 64
BATCH_SIZE = 16
N_NULL = 200
DEAD_THRESH = 0.01
MARGIN = 0.5
ARM = "AB"

RUNGS: Dict[str, Dict] = {
    "tiny":  dict(d_model=64,  n_trunk_layers=2, n_experts=4),
    "small": dict(d_model=256, n_trunk_layers=4, n_experts=8),
    "mid":   dict(d_model=512, n_trunk_layers=8, n_experts=8),
}
RUNG_ORDER = ["tiny", "small", "mid"]
BUDGET: Dict[str, Dict] = {
    "tiny":  dict(steps=300, lr=3e-3),
    "small": dict(steps=400, lr=2e-3),
    "mid":   dict(steps=500, lr=1e-3),
}

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


def _set_seed(s: int) -> None:
    torch.manual_seed(s)


def _build_stream(seed: int) -> List[int]:
    web, reg = make_real_corpus(n_bytes_per_lane=8192, seed=seed)
    stream, _lane = lane_tagged_stream(web, reg, block=64)
    return stream


def routing_z(ent_nats: float, E: int, seed: int):
    """VERBATIM from CLM/model/judge_clm.routing_z."""
    g = torch.Generator().manual_seed(seed + 11)  # noqa: F841 (parity)
    obs = ent_nats
    samples = []
    for _ in range(N_NULL):
        d = torch.distributions.Dirichlet(torch.ones(E)).sample()
        p = d / (d.sum() + 1e-9)
        samples.append(float(-(p * torch.log(p + 1e-9)).sum()))
    st = torch.tensor(samples)
    mu, sd = float(st.mean()), float(st.std() + 1e-9)
    return (obs - mu) / sd, obs, mu, sd


@torch.no_grad()
def _measure(model: CLMConvMoE, eval_batches):
    model.eval()
    acc = None
    ent_sum = 0.0
    n = 0
    for x, y in eval_batches:
        x = x.to(DEVICE); y = y.to(DEVICE)
        out = model(x, y)
        u = out["usage"]
        acc = u.clone() if acc is None else acc + u
        ent_sum += float(out["routing_entropy"])
        n += 1
    return (acc / max(1, n)).cpu(), ent_sum / max(1, n)


def run_cell(rung: str, seed: int, steps_mult: float) -> Dict:
    _set_seed(seed)
    base = dict(RUNGS[rung])
    cfg = CLMConfig(variant=ARM, **base)
    model = CLMConvMoE(cfg).to(DEVICE)
    E = cfg.n_experts

    stream = _build_stream(seed)
    bud = BUDGET[rung]
    steps = max(1, int(round(bud["steps"] * steps_mult)))
    train_batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, steps, seed=seed)
    eval_batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, 16, seed=seed + 999)

    opt = torch.optim.Adam(model.parameters(), lr=bud["lr"])
    model.train()
    last_ce = float("nan")
    for x, y in train_batches:
        x = x.to(DEVICE); y = y.to(DEVICE)
        opt.zero_grad()
        out = model(x, y)
        out["loss"].backward()
        opt.step()
        last_ce = float(out["ce_loss"].detach())

    usage, ent = _measure(model, eval_batches)
    p = usage / (usage.sum() + 1e-9)
    distinct = int((p > DEAD_THRESH).sum())
    rz, r_obs, r_mu, r_sd = routing_z(ent, E, seed)
    return {
        "rung": rung, "seed": seed, "arm": ARM,
        "d_model": base["d_model"], "n_layers": base["n_trunk_layers"],
        "n_experts": E, "params": model.num_params(),
        "train_steps": steps, "lr": bud["lr"],
        "usage": [round(float(u), 4) for u in p],
        "distinct_experts": distinct,
        "routing_entropy_nats": round(ent, 4),
        "max_entropy": round(math.log(E), 4),
        "null_mu": round(r_mu, 4), "null_sd": round(r_sd, 4),
        "routing_z": round(rz, 4),
        "final_ce": round(last_ce, 4),
        "gate_3.0": bool(rz > 3.0),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", default="42,43,44")
    ap.add_argument("--steps-mult", type=float, default=1.0)
    a = ap.parse_args()
    seeds = [int(s) for s in a.seeds.split(",")]

    print(f"H_871 routing-z scale-ladder — arm={ARM} seeds={seeds} "
          f"steps_mult={a.steps_mult} corpus=REAL(kowiki two-lane) device={DEVICE}",
          flush=True)
    print(f"torch {torch.__version__}  N_NULL={N_NULL}  MARGIN={MARGIN}", flush=True)

    per_run: List[Dict] = []
    for rung in RUNG_ORDER:
        for seed in seeds:
            r = run_cell(rung, seed, a.steps_mult)
            per_run.append(r)
            print(f"[{rung:>5} s{seed}] d={r['d_model']} L={r['n_layers']} "
                  f"E={r['n_experts']} params={r['params']} "
                  f"H={r['routing_entropy_nats']:.3f}/{r['max_entropy']:.3f} "
                  f"null_mu={r['null_mu']:.3f} z={r['routing_z']:.3f} "
                  f"distinct={r['distinct_experts']} ce={r['final_ce']:.3f} "
                  f"gate3.0={'Y' if r['gate_3.0'] else 'N'}", flush=True)

    mean_z: Dict[str, float] = {}
    for rung in RUNG_ORDER:
        rs = [r["routing_z"] for r in per_run if r["rung"] == rung]
        mean_z[rung] = round(sum(rs) / len(rs), 4)

    z_tiny, z_small, z_mid = mean_z["tiny"], mean_z["small"], mean_z["mid"]
    monotone = (z_small >= z_tiny) and (z_mid >= z_small)
    margin = round(z_mid - z_tiny, 4)
    artifact_confirmed = bool(monotone and (margin >= MARGIN))
    any_cross_3 = any(r["gate_3.0"] for r in per_run)

    print("\n=== H_871 routing-z scale-ladder AGGREGATE (mean over seeds) ===",
          flush=True)
    for rung in RUNG_ORDER:
        print(f"  {rung:>5}: mean routing-z = {mean_z[rung]:+.4f}", flush=True)
    print(f"  monotone non-decreasing tiny<=small<=mid : {monotone}", flush=True)
    print(f"  margin (mid - tiny) = {margin:+.4f}  (gate >= {MARGIN})", flush=True)
    print(f"  any cell crosses 3.0 gate : {any_cross_3}", flush=True)
    print(f"  ARTIFACT CONFIRMED (monotone AND margin>=gate) : "
          f"{artifact_confirmed}", flush=True)
    print(f"  VERDICT : {'GREEN (artifact confirmed: z rises with scale)' if artifact_confirmed else 'RED (real ceiling: z flat/neg with scale)'}",
          flush=True)

    out = {
        "experiment": "H_871 routing-z scale-ladder (M1 measurement-artifact test)",
        "arm": ARM, "seeds": seeds, "steps_mult": a.steps_mult,
        "corpus": "real kowiki two-lane (stage2_real_corpus.make_real_corpus)",
        "device": DEVICE, "n_null": N_NULL, "margin_gate": MARGIN,
        "routing_z_metric": "(obs_entropy - mu_null)/sd_null, null=Dirichlet(1) over E (verbatim CLM/model/judge_clm.routing_z)",
        "per_run": per_run,
        "mean_routing_z": mean_z,
        "monotone_non_decreasing": monotone,
        "margin_mid_minus_tiny": margin,
        "any_cell_crosses_3.0": any_cross_3,
        "artifact_confirmed": artifact_confirmed,
        "verdict": "GREEN" if artifact_confirmed else "RED",
        "torch": torch.__version__,
    }
    jdest = os.environ.get("H871_JSON_OUT")
    if jdest:
        with open(jdest, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\nwrote JSON -> {jdest}", flush=True)


if __name__ == "__main__":
    main()
