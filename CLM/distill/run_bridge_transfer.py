"""BRIDGE transfer run — teacher escape -> student distill -> transfer Delta.

The PR4/PR5 payload for F-CLM-BRIDGE-XFER (CLM/P0_ARCHITECTURE.md §11.6, @L8).
Trains a valid-scale TEACHER array, measures its inter-expert dispatch-entropy
z (its monopoly-escape), DISTILLS a chip-fit STUDENT via Hinton KD, then
re-measures the student's z. The transfer Delta = z_student - z_teacher answers:
does monopoly-escape SURVIVE distillation?

FROZEN pre-run (@L8, no tampering):
  teacher  : E=TEACHER_E experts, d=TEACHER_D  (valid measure scale)
  student  : E=STUDENT_E experts, d=STUDENT_D  (chip-fit deploy scale)
  KD       : alpha=KD_ALPHA, T=KD_T (Hinton soft-target)
  metric   : dispatch-entropy z vs Dirichlet(1) uniform null (same as H_852)
  seeds    : {42, 43, 44}
  falsifier F-CLM-BRIDGE-XFER (frozen):
     PASS (transfer survives) iff
        student z and teacher z are SAME SIGN (escape direction preserved) AND
        |z_student - z_teacher| <= XFER_TOL  (transfer Delta bounded) AND
        student chip-fit.
     FAIL (closed-negative) otherwise -- reported honestly (g63, p7).

This same payload runs on a GPU pod (larger steps / experts) as the autonomous
fire; locally it runs a $0 CPU toy. Inference stays AKIDA-int4-only (P0 d4).

Run:  python3 CLM/distill/run_bridge_transfer.py [--steps N] [--fire]
Env:  BRIDGE_TXT / BRIDGE_JSON to persist.
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
_MODEL = os.path.join(os.path.dirname(_HERE), "model")
for p in (_HERE, _MODEL):
    if p not in sys.path:
        sys.path.insert(0, p)
from distill_array import (                                          # noqa: E402
    DistillConfig, train_teacher, distill_student, _dispatch_entropy_z,
    student_chip_fit,
)
from data import make_synthetic_corpus, make_batches, lane_tagged_stream  # noqa

# ---- FROZEN pre-registered config (@L8) ---------------------------------- #
SEEDS = [42, 43, 44]
XFER_TOL = 3.0           # max |z_student - z_teacher| for "transfer survives"
NULL_SAMPLES = 1500
FROZEN = {
    "teacher": "E=32 d=128 (valid measure scale)",
    "student": "E=8 d=64 (chip-fit deploy scale)",
    "kd": "Hinton alpha=0.7 T=3.0 soft-target",
    "metric": "dispatch-entropy z vs Dirichlet(1) uniform null",
    "seeds": SEEDS,
    "xfer_tol": XFER_TOL,
    "falsifier": ("F-CLM-BRIDGE-XFER: z_student & z_teacher SAME SIGN AND "
                  "|z_student - z_teacher| <= xfer_tol AND student chip-fit"),
}


def _eval_batches(seed: int, n: int = 16):
    web, reg = make_synthetic_corpus(n_bytes_per_lane=8192, seed=seed)
    stream, _ = lane_tagged_stream(web, reg, block=64)
    return make_batches(stream, 64, 16, n, seed=seed + 777)


def one_seed(cfg: DistillConfig, steps: int, seed: int) -> Dict:
    teacher = train_teacher(cfg, steps=steps, seed=seed)
    tz = _dispatch_entropy_z(teacher, _eval_batches(seed), cfg.teacher_experts,
                             seed, null_samples=NULL_SAMPLES)
    student = distill_student(teacher, cfg, steps=steps, seed=seed)
    sz = _dispatch_entropy_z(student, _eval_batches(seed), cfg.student_experts,
                             seed, null_samples=NULL_SAMPLES)
    delta = sz["z"] - tz["z"]
    same_sign = (tz["z"] >= 0) == (sz["z"] >= 0)
    return {
        "seed": seed,
        "teacher_z": tz["z"], "teacher_H": tz["H"], "teacher_normH": tz["norm_entropy"],
        "student_z": sz["z"], "student_H": sz["H"], "student_normH": sz["norm_entropy"],
        "transfer_delta": round(delta, 5),
        "same_sign": same_sign,
        "student_chip_fit": student_chip_fit(student),
    }


def run(steps: int = 120) -> Dict:
    cfg = DistillConfig()
    rows: List[Dict] = [one_seed(cfg, steps, s) for s in SEEDS]
    mean_delta = sum(r["transfer_delta"] for r in rows) / len(rows)
    mean_tz = sum(r["teacher_z"] for r in rows) / len(rows)
    mean_sz = sum(r["student_z"] for r in rows) / len(rows)
    all_same_sign = all(r["same_sign"] for r in rows)
    all_chip_fit = all(r["student_chip_fit"] for r in rows)
    bounded = all(abs(r["transfer_delta"]) <= XFER_TOL for r in rows)
    passed = bool(all_same_sign and bounded and all_chip_fit)
    return {
        "frozen": FROZEN,
        "steps": steps,
        "per_seed": rows,
        "mean_teacher_z": round(mean_tz, 5),
        "mean_student_z": round(mean_sz, 5),
        "mean_transfer_delta": round(mean_delta, 5),
        "all_same_sign": all_same_sign,
        "all_delta_bounded": bounded,
        "all_student_chip_fit": all_chip_fit,
        "verdict": "PASS" if passed else "FAIL",
        "verdict_tier": ("🟢 SUPPORTED-NUMERICAL" if passed
                         else "🔴 CLOSED-NEGATIVE"),
        "scale_scope": "toy teacher(E32/d128)->student(E8/d64), toy two-lane -- a_scale_honest_scope",
        "torch": torch.__version__,
    }


def _fmt(res: Dict) -> str:
    L = ["F-CLM-BRIDGE-XFER -- teacher escape -> student distill -> transfer Delta",
         "=" * 72, "FROZEN (pre-run, @L8 no tampering):"]
    for k, v in res["frozen"].items():
        L.append(f"  {k} = {v}")
    L.append("")
    L.append(f"{'seed':>5} {'teacher_z':>10} {'student_z':>10} {'Delta':>9} "
             f"{'sameSign':>9} {'chipFit':>8}")
    for r in res["per_seed"]:
        L.append(f"{r['seed']:>5} {r['teacher_z']:>10.4f} {r['student_z']:>10.4f} "
                 f"{r['transfer_delta']:>9.4f} {str(r['same_sign']):>9} "
                 f"{str(r['student_chip_fit']):>8}")
    L.append("")
    L.append(f"mean teacher_z      : {res['mean_teacher_z']}")
    L.append(f"mean student_z      : {res['mean_student_z']}")
    L.append(f"mean transfer Delta : {res['mean_transfer_delta']} (|Delta|<={XFER_TOL})")
    L.append(f"all same sign       : {res['all_same_sign']}")
    L.append(f"all Delta bounded   : {res['all_delta_bounded']}")
    L.append(f"all student chip-fit: {res['all_student_chip_fit']}")
    L.append(f"scale scope         : {res['scale_scope']}")
    L.append("")
    L.append(f"VERDICT: {res['verdict']}  {res['verdict_tier']}")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=120)
    ap.add_argument("--fire", action="store_true",
                    help="fire mode: longer train (GPU pod). default toy CPU.")
    a = ap.parse_args()
    steps = 600 if a.fire else a.steps
    res = run(steps=steps)
    txt = _fmt(res)
    print(txt, flush=True)
    if os.environ.get("BRIDGE_TXT"):
        open(os.environ["BRIDGE_TXT"], "w").write(txt)
    if os.environ.get("BRIDGE_JSON"):
        json.dump(res, open(os.environ["BRIDGE_JSON"], "w"), indent=2)


if __name__ == "__main__":
    main()
