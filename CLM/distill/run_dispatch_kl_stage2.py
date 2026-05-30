"""STAGE-2 PRODUCTION-scale dispatch-KL transfer (@L3/@L4) — re-test toy 🔴.

STAGE-1 (toy: teacher E32/d128, student E8/d64, synthetic LCG corpus,
NULL_SAMPLES=1500) ruled F-CLM-DISPATCHKL-XFER 🔴 CLOSED-NEGATIVE: even with the
dispatch-KL term added, mean transfer Delta = 3.51, signs flipped (teacher z<0,
student z>0) — the teacher's monopoly-escape did NOT transfer into the chip-fit
student. The only untested axis was PRODUCTION SCALE. This re-tests it.

PRODUCTION LEVERS vs STAGE-1 toy (@L3):
  * teacher d_model 128 -> TEACHER_D (>=512); student d_model 64 -> STUDENT_D
  * corpus  synthetic LCG -> REAL kowiki @corpus clm_p1 (stage2_real_corpus)
  * steps   120 -> STEPS (full)
  * E (teacher 32 / student 8), beta, KD knobs UNCHANGED (the transfer under test)

FROZEN, NOT TAMPERED (@L5): XFER_TOL=3.0, the same falsifier as STAGE-1
run_dispatch_kl.py. round1 reference Delta = 4.33829 (the original BRIDGE).
A 🔴 at production scale is reported AS-IS (a_paper_negative_ok).

@L2 SAFETY: NULL_SAMPLES HARD-CAPPED at 16. @L1: torch run — ubu-1/runpod ONLY.

Run (GPU host only):  python3 CLM/distill/run_dispatch_kl_stage2.py
Env: DKL2_TXT / DKL2_JSON persist; TEACHER_D / STUDENT_D / STEPS override.
"""

from __future__ import annotations

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
from stage2_real_corpus import make_real_corpus                     # noqa
from data import make_batches, lane_tagged_stream                   # noqa

# ---- PRODUCTION-scale config (@L3) ---------------------------------------- #
TEACHER_D = int(os.environ.get("TEACHER_D", "512"))   # toy was 128
STUDENT_D = int(os.environ.get("STUDENT_D", "128"))   # toy was 64
STEPS = int(os.environ.get("STEPS", "600"))           # toy was 120
BETA = float(os.environ.get("BETA", "1.0"))
CORPUS_BYTES = 8192
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# ---- FROZEN (@L5, identical falsifier to STAGE-1; thresholds untouched) ---- #
SEEDS = [42, 43, 44]
XFER_TOL = 3.0
ROUND1_MEAN_DELTA = 4.33829
# @L2 HARD CAP: Monte-Carlo null draws <= 16 (NEVER unbounded; was 1500 toy).
NULL_SAMPLES = min(16, int(os.environ.get("NULL_SAMPLES", "16")))
assert NULL_SAMPLES <= 16, "@L2: NULL_SAMPLES must be <= 16"

FROZEN = {
    "teacher": "E=32 d=%d (production measure scale)" % TEACHER_D,
    "student": "E=8 d=%d (chip-fit deploy scale)" % STUDENT_D,
    "kd": "Hinton alpha=0.7 T=3.0 soft-target + dispatch-KL (beta=%g)" % BETA,
    "metric": "dispatch-entropy z vs Dirichlet(1) uniform null",
    "corpus": "REAL kowiki @corpus clm_p1 (CLM/corpus/sample/*.bytes)",
    "seeds": SEEDS, "xfer_tol": XFER_TOL,
    "null_samples": NULL_SAMPLES, "steps": STEPS,
    "round1_mean_delta": ROUND1_MEAN_DELTA,
    "falsifier": ("F-CLM-DISPATCHKL-XFER@PROD: dispatch-KL distill shrinks "
                  "transfer Delta vs round-1 (4.34) AND z_student/z_teacher same "
                  "sign AND |Delta|<=xfer_tol AND student chip-fit, at PROD scale"),
}


def _bucket_teacher(dist_t: torch.Tensor, e_s: int) -> torch.Tensor:
    e_t = dist_t.numel()
    assert e_t % e_s == 0
    return dist_t.reshape(e_s, e_t // e_s).sum(dim=1)


def _train_teacher_real(cfg, steps, seed):
    torch.manual_seed(seed)
    teacher = build_teacher(cfg).to(DEVICE)
    web, reg = make_real_corpus(n_bytes_per_lane=CORPUS_BYTES, seed=seed)
    stream, _ = lane_tagged_stream(web, reg, block=64)
    batches = make_batches(stream, 64, 16, steps, seed=seed)
    opt = torch.optim.Adam(teacher.parameters(), lr=3e-3)
    teacher.train()
    for x, y in batches:
        x, y = x.to(DEVICE), y.to(DEVICE)
        opt.zero_grad()
        out = teacher(x, y)
        out["loss"].backward()
        opt.step()
    return teacher


def _distill_student_real(teacher, cfg, steps, seed, beta):
    torch.manual_seed(seed + 1)
    student = build_student(cfg).to(DEVICE)
    web, reg = make_real_corpus(n_bytes_per_lane=CORPUS_BYTES, seed=seed)
    stream, _ = lane_tagged_stream(web, reg, block=64)
    batches = make_batches(stream, 64, 16, steps, seed=seed + 5)
    opt = torch.optim.Adam(student.parameters(), lr=3e-3)
    teacher.eval()
    student.train()
    e_s = cfg.student_experts
    for x, y in batches:
        x, y = x.to(DEVICE), y.to(DEVICE)
        opt.zero_grad()
        with torch.no_grad():
            t_out = teacher(x)
            t_logits = t_out["logits"]
            t_disp = (t_out["dispatch_counts"].float()
                      / t_out["dispatch_counts"].float().sum().clamp_min(1.0))
            t_disp_b = _bucket_teacher(t_disp, e_s)
        s_out = student(x, y)
        kd = kd_loss(s_out["logits"], t_logits, y, cfg.kd_alpha, cfg.kd_temperature)
        s_disp = (s_out["dispatch_counts"].float()
                  / s_out["dispatch_counts"].float().sum().clamp_min(1.0))
        eps = 1e-8
        t_tgt = (t_disp_b + eps); t_tgt = t_tgt / t_tgt.sum()
        disp_kl = F.kl_div(torch.log(s_disp + eps), t_tgt, reduction="sum")
        (kd["loss"] + beta * disp_kl).backward()
        opt.step()
    return student


def _eval_batches(seed):
    web, reg = make_real_corpus(n_bytes_per_lane=CORPUS_BYTES, seed=seed)
    stream, _ = lane_tagged_stream(web, reg, block=64)
    eb = make_batches(stream, 64, 16, 16, seed=seed + 777)
    return [(x.to(DEVICE), y.to(DEVICE)) for x, y in eb]


def one_seed(cfg, steps, seed, beta) -> Dict:
    teacher = _train_teacher_real(cfg, steps, seed)
    tz = _dispatch_entropy_z(teacher, _eval_batches(seed), cfg.teacher_experts,
                             seed, null_samples=NULL_SAMPLES)
    student = _distill_student_real(teacher, cfg, steps, seed, beta)
    sz = _dispatch_entropy_z(student, _eval_batches(seed), cfg.student_experts,
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


def run(steps, beta) -> Dict:
    cfg = DistillConfig(teacher_d_model=TEACHER_D, student_d_model=STUDENT_D)
    rows: List[Dict] = [one_seed(cfg, steps, s, beta) for s in SEEDS]
    mean_delta = sum(abs(r["transfer_delta"]) for r in rows) / len(rows)
    mean_signed = sum(r["transfer_delta"] for r in rows) / len(rows)
    all_same_sign = all(r["same_sign"] for r in rows)
    all_chip_fit = all(r["student_chip_fit"] for r in rows)
    bounded = all(abs(r["transfer_delta"]) <= XFER_TOL for r in rows)
    shrank = mean_delta < ROUND1_MEAN_DELTA
    passed = bool(shrank and all_same_sign and bounded and all_chip_fit)
    return {
        "frozen": FROZEN, "steps": steps, "beta": beta,
        "per_seed": rows,
        "mean_abs_transfer_delta": round(mean_delta, 5),
        "mean_signed_transfer_delta": round(mean_signed, 5),
        "round1_mean_delta": ROUND1_MEAN_DELTA,
        "delta_shrank_vs_round1": shrank,
        "all_same_sign": all_same_sign,
        "all_delta_bounded": bounded,
        "all_student_chip_fit": all_chip_fit,
        "verdict": "PASS" if passed else "FAIL",
        "verdict_tier": ("\U0001f7e2 SUPPORTED-NUMERICAL" if passed
                         else "\U0001f534 CLOSED-NEGATIVE"),
        "device": DEVICE,
        "scale_scope": ("PRODUCTION teacher(E32/d%d)->student(E8/d%d) + "
                        "dispatch-KL, REAL kowiki corpus, %d steps -- "
                        "a_scale_honest_scope" % (TEACHER_D, STUDENT_D, steps)),
        "torch": torch.__version__,
    }


def fmt(res: Dict) -> str:
    L = ["F-CLM-DISPATCHKL-XFER@PROD -- PRODUCTION-scale escape transfer",
         "=" * 72, "FROZEN (@L5, identical thresholds to STAGE-1, NOT tampered):"]
    for k, v in res["frozen"].items():
        L.append(f"  {k} = {v}")
    L.append("")
    L.append(f"beta = {res['beta']} ; steps = {res['steps']} ; device = {res['device']}")
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
    res = run(STEPS, BETA)
    txt = fmt(res)
    print(txt, flush=True)
    if os.environ.get("DKL2_TXT"):
        open(os.environ["DKL2_TXT"], "w").write(txt)
        print("wrote TXT", flush=True)
    if os.environ.get("DKL2_JSON"):
        json.dump(res, open(os.environ["DKL2_JSON"], "w"), indent=2)
        print("wrote JSON", flush=True)


if __name__ == "__main__":
    main()
