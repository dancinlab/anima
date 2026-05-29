"""Expert-count sweep RUN -- dispatch-entropy z-score vs uniform-null (DISSOLVE).

This is the VERDICT run for F-CLM-MONO-ARRAY (CLM/P0_ARCHITECTURE.md §11.6,
UNIVERSE H_852). It is the PR3 measurement: does the measurement/AKIDA conflict
*dissolve* when scale = expert-COUNT (@L2)? Concretely, as the expert-count E
grows (each expert chip-fit, @L3), does inter-expert dispatch entropy escape
monopoly -- i.e. does the dispatch-entropy z-score vs a uniform-simplex null
RISE with E (monopoly-escape that scales with chip count)?

PRE-REGISTERED, FROZEN BEFORE THE RUN (@L7, no post-hoc tampering):
  null      : Dirichlet(alpha=1) uniform-simplex dispatch over E experts
              (NULL_SAMPLES draws), entropy mean/std -> z = (H_obs - mu)/sigma.
  axis      : SWEEP_EXPERT_COUNTS = [4, 8, 16, 32, 64].
  seeds     : {42, 43, 44} (multi-seed, per d6); per-E z = mean over seeds.
  TRAIN     : TRAIN_STEPS short QAT-free train on the toy two-lane corpus so the
              router actually moves (monopoly DYNAMICS, not random init).
  falsifier F-CLM-MONO-ARRAY (frozen):
     PASS (DISSOLVE supported) iff dispatch-entropy z is MONOTONE NON-DECREASING
        across the E sweep (z(4) <= z(8) <= ... <= z(64)) within MONO_TOL
        AND z(64) > z(4) by at least MIN_RISE  (escape genuinely scales).
     FAIL (closed-negative) otherwise -- reported honestly as-is (g63, p7);
        a non-rising / non-monotone z is a VALID result, threshold NOT moved.

Toy scale (d64/L2, toy two-lane corpus). Per a_scale_honest_scope this verdict
is scoped to the MEASURED axis (toy expert-count sweep); it is NOT a 3B claim.
The chip-native reframe means the axis itself (expert-count) is the deploy-
relevant one, but the corpus/d_model here remain toy (H_666 caveat).

Run:  python3 CLM/model/run_array_sweep.py
Set ARRAY_SWEEP_JSON / ARRAY_SWEEP_TXT to persist outputs.
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Dict, List

import torch

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from array_moe import build_array, SWEEP_EXPERT_COUNTS, AKD1000_NODE_BUDGET  # noqa
from data import make_synthetic_corpus, make_batches, lane_tagged_stream      # noqa

# ---- FROZEN pre-registered thresholds (@L7) ------------------------------- #
SEEDS = [42, 43, 44]
NULL_SAMPLES = 4000          # Dirichlet(1) uniform-simplex null draws
TRAIN_STEPS = 120            # short train so the router DYNAMICS (not init) show
SEQ_LEN = 64
BATCH_SIZE = 16
LR = 3e-3
MONO_TOL = 0.50              # allowed per-step z dip and still "non-decreasing"
MIN_RISE = 1.0              # required z(64) - z(4) for genuine escape scaling
FROZEN = {
    "null": "Dirichlet(alpha=1) uniform-simplex dispatch entropy",
    "null_samples": NULL_SAMPLES,
    "axis": SWEEP_EXPERT_COUNTS,
    "seeds": SEEDS,
    "train_steps": TRAIN_STEPS,
    "mono_tol": MONO_TOL,
    "min_rise": MIN_RISE,
    "falsifier": ("F-CLM-MONO-ARRAY: dispatch-entropy z monotone non-decreasing "
                  "(within mono_tol) over E sweep AND z(64)-z(4) >= min_rise"),
}


def _uniform_null_entropy_stats(n_experts: int, n_tokens: int,
                                samples: int, seed: int) -> tuple[float, float]:
    """Mean/std of dispatch entropy under a Dirichlet(1) uniform-simplex null.

    Each null draw: sample a probability vector p ~ Dirichlet(1) over E experts,
    multinomial-dispatch n_tokens, compute the empirical dispatch entropy.
    """
    g = torch.Generator().manual_seed(seed + 7919)
    ones = torch.ones(n_experts)
    Hs = torch.empty(samples)
    for s in range(samples):
        # Dirichlet(1) via Gamma(1,1) normalization
        gam = torch.distributions.Gamma(ones, 1.0).sample()  # uses global RNG; ok toy
        p = gam / gam.sum()
        counts = torch.multinomial(p, n_tokens, replacement=True, generator=g)
        c = torch.bincount(counts, minlength=n_experts).float()
        frac = c / c.sum().clamp_min(1.0)
        nz = frac[frac > 0]
        Hs[s] = float(-(nz * torch.log(nz)).sum())
    return float(Hs.mean()), float(Hs.std().clamp_min(1e-9))


def _train_and_measure(n_experts: int, seed: int) -> Dict:
    torch.manual_seed(seed)
    model = build_array(n_experts=n_experts)
    web, reg = make_synthetic_corpus(n_bytes_per_lane=8192, seed=seed)
    stream, _lane = lane_tagged_stream(web, reg, block=64)
    batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, TRAIN_STEPS, seed=seed)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    model.train()
    for x, y in batches:
        opt.zero_grad()
        out = model(x, y)
        out["loss"].backward()
        opt.step()

    # measure dispatch on a held-out eval pass
    model.eval()
    eval_batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, 16, seed=seed + 999)
    acc = torch.zeros(n_experts)
    n_tok = 0
    with torch.no_grad():
        for x, y in eval_batches:
            out = model(x, y)
            acc = acc + out["dispatch_counts"]
            n_tok += int(out["dispatch_counts"].sum())
    frac = acc / acc.sum().clamp_min(1.0)
    nz = frac[frac > 0]
    H_obs = float(-(nz * torch.log(nz)).sum())

    tok_per_pass = max(1, n_tok // 16)
    mu, sigma = _uniform_null_entropy_stats(n_experts, tok_per_pass,
                                            NULL_SAMPLES, seed)
    z = (H_obs - mu) / sigma
    return {
        "n_experts": n_experts, "seed": seed,
        "H_obs": round(H_obs, 5), "null_mu": round(mu, 5),
        "null_sigma": round(sigma, 5), "z": round(z, 5),
        "n_active": int((acc > 0).sum()),
        "expert_params": model.moe.expert_param_count(),
        "chip_fit": model.expert_chip_fit(),
    }


def run() -> Dict:
    per_E: Dict[int, Dict] = {}
    rows: List[Dict] = []
    for E in SWEEP_EXPERT_COUNTS:
        seed_rows = [_train_and_measure(E, s) for s in SEEDS]
        rows.extend(seed_rows)
        zs = [r["z"] for r in seed_rows]
        per_E[E] = {
            "mean_z": round(sum(zs) / len(zs), 5),
            "min_z": round(min(zs), 5),
            "max_z": round(max(zs), 5),
            "mean_H": round(sum(r["H_obs"] for r in seed_rows) / len(seed_rows), 5),
            "chip_fit": all(r["chip_fit"] for r in seed_rows),
            "per_seed_z": zs,
        }

    # --- frozen falsifier evaluation (NO threshold tampering) -------------- #
    mean_zs = [per_E[E]["mean_z"] for E in SWEEP_EXPERT_COUNTS]
    monotone = all(mean_zs[i + 1] >= mean_zs[i] - MONO_TOL
                   for i in range(len(mean_zs) - 1))
    rise = mean_zs[-1] - mean_zs[0]
    all_chip_fit = all(per_E[E]["chip_fit"] for E in SWEEP_EXPERT_COUNTS)
    passed = bool(monotone and rise >= MIN_RISE and all_chip_fit)

    return {
        "frozen": FROZEN,
        "per_E": {str(E): per_E[E] for E in SWEEP_EXPERT_COUNTS},
        "per_run": rows,
        "mean_z_sweep": mean_zs,
        "monotone_non_decreasing": monotone,
        "z_rise_E64_minus_E4": round(rise, 5),
        "all_chip_fit": all_chip_fit,
        "verdict": "PASS" if passed else "FAIL",
        "verdict_tier": ("🟢 SUPPORTED-NUMERICAL" if passed
                         else "🔴 CLOSED-NEGATIVE"),
        "akd1000_budget": AKD1000_NODE_BUDGET,
        "scale_scope": "toy expert-count sweep (d64/L2, toy two-lane) -- a_scale_honest_scope",
        "torch": torch.__version__,
    }


def _fmt_txt(res: Dict) -> str:
    L = []
    L.append("F-CLM-MONO-ARRAY -- DISSOLVE expert-count dispatch-entropy sweep")
    L.append("=" * 68)
    L.append("FROZEN (pre-run, @L7 no tampering):")
    for k, v in res["frozen"].items():
        L.append(f"  {k} = {v}")
    L.append("")
    L.append(f"{'E':>4} {'mean_z':>9} {'min_z':>9} {'max_z':>9} "
             f"{'mean_H':>9} {'chip_fit':>9}")
    for E in SWEEP_EXPERT_COUNTS:
        d = res["per_E"][str(E)]
        L.append(f"{E:>4} {d['mean_z']:>9.4f} {d['min_z']:>9.4f} "
                 f"{d['max_z']:>9.4f} {d['mean_H']:>9.4f} "
                 f"{str(d['chip_fit']):>9}")
    L.append("")
    L.append(f"mean_z sweep        : {res['mean_z_sweep']}")
    L.append(f"monotone non-decr   : {res['monotone_non_decreasing']}")
    L.append(f"z rise (E64 - E4)   : {res['z_rise_E64_minus_E4']} "
             f"(threshold >= {MIN_RISE})")
    L.append(f"all experts chip-fit: {res['all_chip_fit']}")
    L.append(f"scale scope         : {res['scale_scope']}")
    L.append("")
    L.append(f"VERDICT: {res['verdict']}  {res['verdict_tier']}")
    return "\n".join(L) + "\n"


def main() -> None:
    res = run()
    txt = _fmt_txt(res)
    print(txt, flush=True)
    tdest = os.environ.get("ARRAY_SWEEP_TXT")
    if tdest:
        with open(tdest, "w") as f:
            f.write(txt)
        print(f"wrote TXT -> {tdest}", flush=True)
    jdest = os.environ.get("ARRAY_SWEEP_JSON")
    if jdest:
        with open(jdest, "w") as f:
            json.dump(res, f, indent=2)
        print(f"wrote JSON -> {jdest}", flush=True)


if __name__ == "__main__":
    main()
