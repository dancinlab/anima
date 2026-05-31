"""STAGE-2 PRODUCTION-scale Pielou-J sweep (@L3/@L4) — re-test the toy 🔴.

STAGE-1 (toy: d_model=64, synthetic LCG corpus, NULL_SAMPLES=4000) ruled
F-CLM-PIELOU-DISSOLVE 🔴 CLOSED-NEGATIVE: the ln(E)-corrected Pielou evenness
J = H/ln(E) FELL with expert count E (J rise E64−E4 = −0.093, monotone=False).
The only untested axis was PRODUCTION SCALE. This script tests it.

PRODUCTION LEVERS vs STAGE-1 toy (@L3):
  * d_model   64  -> D_MODEL (>=512)          — wide channels
  * corpus    synthetic LCG -> REAL kowiki @corpus clm_p1 (stage2_real_corpus)
  * steps     120 -> TRAIN_STEPS (full)
  * E axis    [4,8,16,32,64]  (UNCHANGED — the scale-axis under test)

FROZEN, NOT TAMPERED (@L5, g63/p7/d6): the Pielou falsifier + its thresholds
are identical to STAGE-1's measure_pielou.py (MONO_TOL=0.02, MIN_RISE=0.0).
A 🔴 at production scale is reported AS-IS (a_paper_negative_ok) — it would
deterministically close the "scale dissolves the conflict" hypothesis.

@L2 SAFETY: NULL_SAMPLES is HARD-CAPPED at 16 (Monte-Carlo repeat ceiling).
@L1 SAFETY: this trains/measures with torch — it MUST run on ubu-1/runpod,
NEVER on the Mac (the run wrapper run_stage2.sh enforces `pool on ubu-1`).

Run (GPU host only):  python3 CLM/model/run_array_sweep_stage2.py
Env: ARRAY_SWEEP2_JSON / ARRAY_SWEEP2_TXT persist; D_MODEL / TRAIN_STEPS override.
"""

from __future__ import annotations

import json
import math
import os
import sys
from typing import Dict, List

import torch

# HOST-ENV (@L1, ubu-1): the installed torch nightly + cuDNN raise
# CUDNN_STATUS_SUBLIBRARY_VERSION_MISMATCH on conv1d. Disable the cuDNN backend
# so conv falls back to the native CUDA kernel (numerically equivalent,
# deterministic). HOST workaround, NOT a metric/threshold change (@L5).
torch.backends.cudnn.enabled = False

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from array_moe import build_array, SWEEP_EXPERT_COUNTS, AKD1000_NODE_BUDGET  # noqa
from stage2_real_corpus import make_real_corpus                              # noqa
from data import make_batches, lane_tagged_stream                           # noqa

# ---- PRODUCTION-scale config (@L3) ---------------------------------------- #
D_MODEL = int(os.environ.get("D_MODEL", "512"))        # toy was 64
TRAIN_STEPS = int(os.environ.get("TRAIN_STEPS", "600"))  # toy was 120
SEQ_LEN = 64
BATCH_SIZE = 16
LR = 3e-3
CORPUS_BYTES = 8192

# ---- FROZEN falsifier (identical to STAGE-1 measure_pielou.py, @L5) -------- #
SEEDS = [42, 43, 44]
MONO_TOL = 0.02    # J in [0,1]; allow 0.02 evenness dip as "non-decreasing"
MIN_RISE = 0.0     # DISSOLVE-flip = J(E64) >= J(E4) within tol
# @L2 HARD CAP: Monte-Carlo null draws <= 16 (NEVER unbounded; was 4000 toy).
NULL_SAMPLES = min(16, int(os.environ.get("NULL_SAMPLES", "16")))
assert NULL_SAMPLES <= 16, "@L2: NULL_SAMPLES must be <= 16"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

FROZEN = {
    "axis": SWEEP_EXPERT_COUNTS,
    "seeds": SEEDS,
    "mono_tol": MONO_TOL,
    "min_rise": MIN_RISE,
    "null_samples": NULL_SAMPLES,
    "d_model": D_MODEL,
    "train_steps": TRAIN_STEPS,
    "corpus": "REAL kowiki @corpus clm_p1 (CLM/corpus/sample/*.bytes)",
    "falsifier": ("F-CLM-PIELOU-DISSOLVE@PROD: Pielou J=H/ln(E) monotone "
                  "non-decreasing (within mono_tol) over E AND J(E64)>=J(E4) "
                  "at PRODUCTION scale (d>=512, real corpus, full steps)"),
}


def _train_and_measure(n_experts: int, seed: int) -> Dict:
    torch.manual_seed(seed)
    model = build_array(n_experts=n_experts, d_model=D_MODEL).to(DEVICE)
    web, reg = make_real_corpus(n_bytes_per_lane=CORPUS_BYTES, seed=seed)
    stream, _lane = lane_tagged_stream(web, reg, block=64)
    batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, TRAIN_STEPS, seed=seed)
    opt = torch.optim.Adam(model.parameters(), lr=LR)
    model.train()
    for x, y in batches:
        x, y = x.to(DEVICE), y.to(DEVICE)
        opt.zero_grad()
        out = model(x, y)
        out["loss"].backward()
        opt.step()

    model.eval()
    eval_batches = make_batches(stream, SEQ_LEN, BATCH_SIZE, 16, seed=seed + 999)
    acc = torch.zeros(n_experts, device=DEVICE)
    with torch.no_grad():
        for x, y in eval_batches:
            x, y = x.to(DEVICE), y.to(DEVICE)
            out = model(x, y)
            acc = acc + out["dispatch_counts"]
    frac = (acc / acc.sum().clamp_min(1.0)).cpu()
    nz = frac[frac > 0]
    H_obs = float(-(nz * torch.log(nz)).sum())
    j = H_obs / math.log(n_experts) if n_experts > 1 else 0.0
    return {
        "n_experts": n_experts, "seed": seed,
        "H_obs": round(H_obs, 5), "pielou_J": round(j, 5),
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
        js = [r["pielou_J"] for r in seed_rows]
        per_E[E] = {
            "mean_J": round(sum(js) / len(js), 5),
            "min_J": round(min(js), 5), "max_J": round(max(js), 5),
            "mean_H": round(sum(r["H_obs"] for r in seed_rows) / len(seed_rows), 5),
            "chip_fit": all(r["chip_fit"] for r in seed_rows),
            "per_seed_J": js,
        }
    mean_js = [per_E[E]["mean_J"] for E in SWEEP_EXPERT_COUNTS]
    mono = all(mean_js[i + 1] >= mean_js[i] - MONO_TOL
               for i in range(len(mean_js) - 1))
    rise = round(mean_js[-1] - mean_js[0], 5)
    passed = bool(mono and rise >= MIN_RISE - MONO_TOL)
    return {
        "frozen": FROZEN,
        "per_E": {str(E): per_E[E] for E in SWEEP_EXPERT_COUNTS},
        "per_run": rows,
        "mean_pielou_J": mean_js,
        "J_monotone_non_decr": mono,
        "J_rise_E64_minus_E4": rise,
        "verdict": "PASS" if passed else "FAIL",
        "verdict_tier": ("\U0001f7e2 SUPPORTED-NUMERICAL" if passed
                         else "\U0001f534 CLOSED-NEGATIVE"),
        "akd1000_budget": AKD1000_NODE_BUDGET,
        "device": DEVICE,
        "scale_scope": ("PRODUCTION expert-count sweep (d_model=%d, REAL kowiki "
                        "corpus, %d steps) -- a_scale_honest_scope; small real "
                        "byte VOLUME stated honestly" % (D_MODEL, TRAIN_STEPS)),
        "torch": torch.__version__,
    }


def _fmt_txt(res: Dict) -> str:
    L = ["F-CLM-PIELOU-DISSOLVE@PROD -- PRODUCTION-scale expert-count Pielou J sweep",
         "=" * 74, "FROZEN (@L5, identical thresholds to STAGE-1, NOT tampered):"]
    for k, v in res["frozen"].items():
        L.append(f"  {k} = {v}")
    L.append("")
    L.append(f"{'E':>4} {'mean_J':>9} {'min_J':>9} {'max_J':>9} "
             f"{'mean_H':>9} {'chip_fit':>9}")
    for E in SWEEP_EXPERT_COUNTS:
        d = res["per_E"][str(E)]
        L.append(f"{E:>4} {d['mean_J']:>9.4f} {d['min_J']:>9.4f} "
                 f"{d['max_J']:>9.4f} {d['mean_H']:>9.4f} {str(d['chip_fit']):>9}")
    L.append("")
    L.append(f"mean Pielou J sweep : {res['mean_pielou_J']}")
    L.append(f"J monotone non-decr : {res['J_monotone_non_decr']} (tol {MONO_TOL})")
    L.append(f"J rise (E64 - E4)   : {res['J_rise_E64_minus_E4']} (>= {MIN_RISE})")
    L.append(f"device              : {res['device']}")
    L.append(f"scale scope         : {res['scale_scope']}")
    L.append("")
    L.append(f"VERDICT: {res['verdict']}  {res['verdict_tier']}")
    return "\n".join(L) + "\n"


def main() -> None:
    res = run()
    txt = _fmt_txt(res)
    print(txt, flush=True)
    if os.environ.get("ARRAY_SWEEP2_TXT"):
        open(os.environ["ARRAY_SWEEP2_TXT"], "w").write(txt)
        print("wrote TXT", flush=True)
    if os.environ.get("ARRAY_SWEEP2_JSON"):
        json.dump(res, open(os.environ["ARRAY_SWEEP2_JSON"], "w"), indent=2)
        print("wrote JSON", flush=True)


if __name__ == "__main__":
    main()
