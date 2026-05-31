"""STAGE-1 distill fix (@L2) — add a dispatch-distribution KL term to KD loss.

ROUND-1 BRIDGE verdict (H_853, bridge_transfer_fire_2026_05_30): teacher (E=32)
monopoly-escape did NOT survive distillation into the chip-fit student (E=8).
mean transfer Delta = 4.34, sign flipped (teacher z<0, student z>0). The KD loss
moved only the next-byte LOGITS (Hinton soft targets), never the teacher's
inter-expert DISPATCH distribution -- so the student re-discovered its own
routing from scratch and the escape failed to transfer.

The fix (@L2, metric<->loss mirror, CLM.breakthrough.mining.md rE2): distill the
quantity we MEASURE. Add a DISPATCH-KL term to the loss:

    L = (1-a)*CE + a*T^2*KL(student_logits || teacher_logits)        # round-1
        + beta * KL( student_dispatch_dist || teacher_dispatch_dist )  # NEW @L2

Teacher (E_t) and student (E_s) have different expert counts, so we aggregate the
teacher's E_t dispatch fractions into E_s contiguous buckets (E_t must be a
multiple of E_s; 32->8 = 4 per bucket) to make the two distributions comparable.
This is the Switch-Transformer load-balance loss but with the TARGET = teacher
dispatch (escape transfer), NOT uniform (rE2 equivalence).

Re-runs the toy distill (reuse round-1 setup: teacher E32/d128 -> student E8/d64,
seeds {42,43,44}) and re-measures transfer Delta. Did it shrink vs 4.34?
HONEST (@L5): frozen XFER_TOL=3.0 untouched; a Delta that does not shrink is a
valid finding.

Run:  python3 CLM/distill/run_dispatch_kl.py [--steps N] [--beta B]
Env:  DKL_TXT / DKL_JSON to persist.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from typing import Dict, List

import torch
import torch.nn.functional as F

_HERE = os.path.dirname(os.path.abspath(__file__))
_MODEL = os.path.join(os.path.dirname(_HERE), "model")
for p in (_HERE, _MODEL):
    if p not in sys.path:
        sys.path.insert(0, p)
from distill_array import (                                          # noqa: E402
    DistillConfig, build_teacher, build_student, kd_loss,
    train_teacher, _dispatch_entropy_z, student_chip_fit,
)
from data import make_synthetic_corpus, make_batches, lane_tagged_stream  # noqa

# ---- FROZEN (@L5, mirrors round-1 bridge falsifier; thresholds untouched) -- #
SEEDS = [42, 43, 44]
XFER_TOL = 3.0
NULL_SAMPLES = 1500
ROUND1_MEAN_DELTA = 4.33829   # the round-1 transfer Delta this PR2 tries to shrink
FROZEN = {
    "teacher": "E=32 d=128 (valid measure scale)",
    "student": "E=8 d=64 (chip-fit deploy scale)",
    "kd": "Hinton alpha=0.7 T=3.0 soft-target + dispatch-KL (beta) @L2",
    "metric": "dispatch-entropy z vs Dirichlet(1) uniform null (same as H_852/853)",
    "seeds": SEEDS,
    "xfer_tol": XFER_TOL,
    "round1_mean_delta": ROUND1_MEAN_DELTA,
    "falsifier": ("F-CLM-DISPATCHKL-XFER: dispatch-KL distill shrinks transfer "
                  "Delta vs round-1 (4.34) AND z_student/z_teacher same sign AND "
                  "|Delta| <= xfer_tol AND student chip-fit"),
}


def _dispatch_dist(model, x, n_experts: int) -> torch.Tensor:
    """Soft inter-expert dispatch distribution for a batch (mean router probs)."""
    out = model(x)
    # router probs live inside moe; recompute via dispatch_counts is hard-top1.
    # use the model forward's dispatch_counts (top-1) -> normalized soft dist.
    c = out["dispatch_counts"].float()
    return c / c.sum().clamp_min(1.0)


def _bucket_teacher(dist_t: torch.Tensor, e_s: int) -> torch.Tensor:
    """Aggregate teacher E_t dispatch dist into E_s contiguous buckets."""
    e_t = dist_t.numel()
    assert e_t % e_s == 0, f"E_t {e_t} not a multiple of E_s {e_s}"
    return dist_t.reshape(e_s, e_t // e_s).sum(dim=1)


def distill_student_dkl(teacher, cfg: DistillConfig, steps: int, seed: int,
                        beta: float, seq_len: int = 64, batch: int = 16,
                        lr: float = 3e-3):
    """Distill a chip-fit student with KD logits + dispatch-KL (@L2)."""
    torch.manual_seed(seed + 1)
    student = build_student(cfg)
    web, reg = make_synthetic_corpus(n_bytes_per_lane=8192, seed=seed)
    stream, _ = lane_tagged_stream(web, reg, block=64)
    batches = make_batches(stream, seq_len, batch, steps, seed=seed + 5)
    opt = torch.optim.Adam(student.parameters(), lr=lr)
    teacher.eval()
    student.train()
    e_s = cfg.student_experts
    for x, y in batches:
        opt.zero_grad()
        with torch.no_grad():
            t_out = teacher(x)
            t_logits = t_out["logits"]
            t_disp = (t_out["dispatch_counts"].float()
                      / t_out["dispatch_counts"].float().sum().clamp_min(1.0))
            t_disp_b = _bucket_teacher(t_disp, e_s)
        s_out = student(x, y)
        kd = kd_loss(s_out["logits"], t_logits, y, cfg.kd_alpha, cfg.kd_temperature)
        # dispatch-KL: KL(student_dispatch || teacher_dispatch_bucketed) @L2
        s_disp = (s_out["dispatch_counts"].float()
                  / s_out["dispatch_counts"].float().sum().clamp_min(1.0))
        eps = 1e-8
        s_log = torch.log(s_disp + eps)
        t_tgt = (t_disp_b + eps)
        t_tgt = t_tgt / t_tgt.sum()
        disp_kl = F.kl_div(s_log, t_tgt, reduction="sum")
        loss = kd["loss"] + beta * disp_kl
        loss.backward()
        opt.step()
    return student


def one_seed(cfg: DistillConfig, steps: int, seed: int, beta: float) -> Dict:
    teacher = train_teacher(cfg, steps=steps, seed=seed)

    def _eval_batches():
        web, reg = make_synthetic_corpus(n_bytes_per_lane=8192, seed=seed)
        stream, _ = lane_tagged_stream(web, reg, block=64)
        return make_batches(stream, 64, 16, 16, seed=seed + 777)

    tz = _dispatch_entropy_z(teacher, _eval_batches(), cfg.teacher_experts,
                             seed, null_samples=NULL_SAMPLES)
    student = distill_student_dkl(teacher, cfg, steps=steps, seed=seed, beta=beta)
    sz = _dispatch_entropy_z(student, _eval_batches(), cfg.student_experts,
                             seed, null_samples=NULL_SAMPLES)
    delta = sz["z"] - tz["z"]
    same_sign = (tz["z"] >= 0) == (sz["z"] >= 0)
    return {
        "seed": seed,
        "teacher_z": tz["z"], "teacher_normH": tz["norm_entropy"],
        "student_z": sz["z"], "student_normH": sz["norm_entropy"],
        "transfer_delta": round(delta, 5),
        "same_sign": same_sign,
        "student_chip_fit": student_chip_fit(student),
    }


def run(steps: int, beta: float) -> Dict:
    cfg = DistillConfig()
    rows: List[Dict] = [one_seed(cfg, steps, s, beta) for s in SEEDS]
    mean_delta = sum(abs(r["transfer_delta"]) for r in rows) / len(rows)
    mean_delta_signed = sum(r["transfer_delta"] for r in rows) / len(rows)
    all_same_sign = all(r["same_sign"] for r in rows)
    all_chip_fit = all(r["student_chip_fit"] for r in rows)
    bounded = all(abs(r["transfer_delta"]) <= XFER_TOL for r in rows)
    shrank = mean_delta < ROUND1_MEAN_DELTA
    passed = bool(shrank and all_same_sign and bounded and all_chip_fit)
    return {
        "frozen": FROZEN, "steps": steps, "beta": beta,
        "per_seed": rows,
        "mean_abs_transfer_delta": round(mean_delta, 5),
        "mean_signed_transfer_delta": round(mean_delta_signed, 5),
        "round1_mean_delta": ROUND1_MEAN_DELTA,
        "delta_shrank_vs_round1": shrank,
        "all_same_sign": all_same_sign,
        "all_delta_bounded": bounded,
        "all_student_chip_fit": all_chip_fit,
        "verdict": "PASS" if passed else "FAIL",
        "verdict_tier": ("\U0001f7e2 SUPPORTED-NUMERICAL" if passed
                         else "\U0001f534 CLOSED-NEGATIVE"),
        "scale_scope": ("toy teacher(E32/d128)->student(E8/d64) + dispatch-KL, "
                        "toy two-lane -- a_scale_honest_scope (toy != production)"),
        "torch": torch.__version__,
    }


def fmt(res: Dict) -> str:
    L = ["F-CLM-DISPATCHKL-XFER -- teacher escape -> dispatch-KL distill -> Delta",
         "=" * 72, "FROZEN (@L5, dispatch-KL added, thresholds not tampered):"]
    for k, v in res["frozen"].items():
        L.append(f"  {k} = {v}")
    L.append("")
    L.append(f"beta (dispatch-KL weight) = {res['beta']} ; steps = {res['steps']}")
    L.append("")
    L.append(f"{'seed':>5} {'teacher_z':>10} {'student_z':>10} {'Delta':>9} "
             f"{'sameSign':>9} {'chipFit':>8}")
    for r in res["per_seed"]:
        L.append(f"{r['seed']:>5} {r['teacher_z']:>10.4f} {r['student_z']:>10.4f} "
                 f"{r['transfer_delta']:>9.4f} {str(r['same_sign']):>9} "
                 f"{str(r['student_chip_fit']):>8}")
    L.append("")
    L.append(f"mean |transfer Delta| : {res['mean_abs_transfer_delta']} "
             f"(round-1 was {res['round1_mean_delta']})")
    L.append(f"mean signed Delta     : {res['mean_signed_transfer_delta']}")
    L.append(f"Delta shrank vs r1    : {res['delta_shrank_vs_round1']}")
    L.append(f"all same sign         : {res['all_same_sign']}")
    L.append(f"all Delta bounded     : {res['all_delta_bounded']} (|Delta|<={XFER_TOL})")
    L.append(f"all student chip-fit  : {res['all_student_chip_fit']}")
    L.append(f"scale scope           : {res['scale_scope']}")
    L.append("")
    L.append(f"VERDICT: {res['verdict']}  {res['verdict_tier']}")
    return "\n".join(L) + "\n"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--steps", type=int, default=120)
    ap.add_argument("--beta", type=float, default=1.0,
                    help="dispatch-KL term weight (@L2)")
    ap.add_argument("--fire", action="store_true")
    a = ap.parse_args()
    steps = 600 if a.fire else a.steps
    res = run(steps=steps, beta=a.beta)
    txt = fmt(res)
    print(txt, flush=True)
    if os.environ.get("DKL_TXT"):
        open(os.environ["DKL_TXT"], "w").write(txt)
    if os.environ.get("DKL_JSON"):
        json.dump(res, open(os.environ["DKL_JSON"], "w"), indent=2)


if __name__ == "__main__":
    main()
