#!/usr/bin/env python3
"""run_s44.py — §44 driver: train @ λ_ptd ∈ {0.0, 0.3}, eval each, compare.

$0 Mac CPU. Writes:
  - dhdl_ptd_head_lam0.json     (λ_ptd = 0.0 baseline — §27 byte-equal)
  - dhdl_ptd_head_lam03.json    (λ_ptd = 0.3 composition)
  - eval_result_lam0.json
  - eval_result_lam03.json
  - result.json   (representation-shaping probe summary)
"""
from __future__ import annotations
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE.parent / "dhdl_decision_head_s27_2026_05_18" / "trace_corpus.jsonl"


def _run(cmd):
    print(f"\n$ {' '.join(str(c) for c in cmd)}", flush=True)
    r = subprocess.run([str(c) for c in cmd], cwd=str(HERE),
                       check=True, capture_output=True, text=True)
    if r.stdout:
        print(r.stdout.rstrip())
    if r.stderr:
        print(r.stderr.rstrip(), file=sys.stderr)
    return r


def main() -> int:
    t0 = time.time()
    head0 = HERE / "dhdl_ptd_head_lam0.json"
    head03 = HERE / "dhdl_ptd_head_lam03.json"
    eval0 = HERE / "eval_result_lam0.json"
    eval03 = HERE / "eval_result_lam03.json"

    # train both
    _run(["python3", "train_dhdl_ptd.py", "--corpus", CORPUS,
          "--lambda-ptd", "0.0", "--out", head0])
    _run(["python3", "train_dhdl_ptd.py", "--corpus", CORPUS,
          "--lambda-ptd", "0.3", "--out", head03])

    # eval both
    _run(["python3", "eval_dhdl_ptd.py", "--corpus", CORPUS,
          "--head", head0, "--out", eval0])
    _run(["python3", "eval_dhdl_ptd.py", "--corpus", CORPUS,
          "--head", head03, "--out", eval03])

    # consolidate
    e0 = json.loads(eval0.read_text())
    e03 = json.loads(eval03.read_text())

    # §27 baseline reference (from §27 eval_result.json)
    s27 = json.loads((HERE.parent / "dhdl_decision_head_s27_2026_05_18" /
                      "eval_result.json").read_text())

    summary = {
        "research_md_section": "§44",
        "title": "DH-DL + PTD-aux composition fire (§38 design execution)",
        "$cost": "$0 Mac CPU (numpy hand-coded backprop, no GPU)",
        "wall_sec": round(time.time() - t0, 2),
        "baseline_s27_gap": s27["threshold_distillation_gap"],
        "baseline_s27_accuracy": s27["accuracy_3class"],
        "lambda_ptd_0": {
            "accuracy_3class": e0["accuracy_3class"],
            "gap": e0["threshold_distillation_gap"],
            "gap_verdict": e0["threshold_distillation_gap_verdict"],
            "ptd_mse_mean": e0["ptd_aux_next_state_mse_mean"],
            "ptd_mse_per_class": e0["ptd_aux_next_state_mse_per_class"],
        },
        "lambda_ptd_03": {
            "accuracy_3class": e03["accuracy_3class"],
            "gap": e03["threshold_distillation_gap"],
            "gap_verdict": e03["threshold_distillation_gap_verdict"],
            "ptd_mse_mean": e03["ptd_aux_next_state_mse_mean"],
            "ptd_mse_per_class": e03["ptd_aux_next_state_mse_per_class"],
        },
        "delta_gap_03_minus_0": (
            e03["threshold_distillation_gap"] - e0["threshold_distillation_gap"]
        ),
        "delta_accuracy_03_minus_0": (
            e03["accuracy_3class"] - e0["accuracy_3class"]
        ),
        "representation_shaping_verdict": (
            "PTD-AUX-SIGNAL-MEASURABLE"
            if abs(e03["threshold_distillation_gap"] - e0["threshold_distillation_gap"])
               > 1e-5
            else "PTD-AUX-INDISTINGUISHABLE-FROM-NOISE-AT-THIS-SCALE"
        ),
        "honest_note": (
            "DESIGN_S38.md §5 honest prediction: 'gap stays ≈ 0 in both — "
            "decision label is deterministic function of features, PTD aux "
            "term shapes representation geometry not decision function.' "
            "Measured delta tells whether the auxiliary signal moves the "
            "decision-axis behaviour vs. noise. PTD aux MSE per-class "
            "localises the structurally-near-empty CONTINUE_THINK corner "
            "(§27 found ≈9 records). Composition is BETTER-ENGINEERED "
            "DISTILLATION not emergence (DESIGN_S38.md §7)."
        ),
    }
    (HERE / "result.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )
    print("\n=== §44 summary ===")
    print(json.dumps({
        "baseline_s27_gap": summary["baseline_s27_gap"],
        "lam0_gap": summary["lambda_ptd_0"]["gap"],
        "lam03_gap": summary["lambda_ptd_03"]["gap"],
        "delta_gap_03_minus_0": summary["delta_gap_03_minus_0"],
        "delta_acc_03_minus_0": summary["delta_accuracy_03_minus_0"],
        "ptd_mse_lam03_per_class": summary["lambda_ptd_03"]["ptd_mse_per_class"],
        "rep_shaping_verdict": summary["representation_shaping_verdict"],
        "wall_sec": summary["wall_sec"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
