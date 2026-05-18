#!/usr/bin/env python3
"""run_s48.py — §48 driver: train @ λ_ptd ∈ {0.0, 0.3} on scale-up corpus.

Writes:
  - dhdl_ptd_head_s48_lam0.json    (λ_ptd = 0.0)
  - dhdl_ptd_head_s48_lam03.json   (λ_ptd = 0.3)
  - eval_result_s48_lam0.json
  - eval_result_s48_lam03.json
  - result.json    (vs §44 comparison + scale-up verdict)
"""
from __future__ import annotations
import json
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE / "trace_corpus_s48.jsonl"


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
    head0 = HERE / "dhdl_ptd_head_s48_lam0.json"
    head03 = HERE / "dhdl_ptd_head_s48_lam03.json"
    eval0 = HERE / "eval_result_s48_lam0.json"
    eval03 = HERE / "eval_result_s48_lam03.json"

    _run(["python3", "train_s48.py", "--corpus", CORPUS,
          "--lambda-ptd", "0.0", "--out", head0])
    _run(["python3", "train_s48.py", "--corpus", CORPUS,
          "--lambda-ptd", "0.3", "--out", head03])

    _run(["python3", "eval_s48.py", "--corpus", CORPUS,
          "--head", head0, "--out", eval0])
    _run(["python3", "eval_s48.py", "--corpus", CORPUS,
          "--head", head03, "--out", eval03])

    e0 = json.loads(eval0.read_text())
    e03 = json.loads(eval03.read_text())

    # §44 baseline reference
    s44_path = HERE.parent / "dhdl_ptd_composition_fire_s44_2026_05_18" / "result.json"
    s44 = json.loads(s44_path.read_text())

    delta_gap = e03["threshold_distillation_gap"] - e0["threshold_distillation_gap"]
    delta_acc = e03["accuracy_3class"] - e0["accuracy_3class"]

    # Compare vs §44 (small-corpus) signal: gap λ=0.3 vs λ=0.0 = -0.00073
    s44_delta_gap = s44["delta_gap_03_minus_0"]
    # PTD MSE comparison
    s48_ptd_mean_lam0 = e0["ptd_aux_next_state_mse_mean"]
    s48_ptd_mean_lam03 = e03["ptd_aux_next_state_mse_mean"]
    s48_ptd_drop_factor = (s48_ptd_mean_lam0 / s48_ptd_mean_lam03
                           if (s48_ptd_mean_lam03 and s48_ptd_mean_lam03 > 0.0)
                           else None)
    s44_ptd_drop_factor = (s44["lambda_ptd_0"]["ptd_mse_mean"] /
                           s44["lambda_ptd_03"]["ptd_mse_mean"])

    # Scale-up verdict
    # signal HOLDS if (a) gap improves with PTD (delta_gap<0) AND (b) PTD MSE drops >5×
    signal_gap_persists = delta_gap < -1e-5
    signal_mse_persists = (s48_ptd_drop_factor is not None
                           and s48_ptd_drop_factor > 5.0)
    if signal_gap_persists and signal_mse_persists:
        verdict = "PTD-AUX-SIGNAL-HOLDS-AT-SCALE"
    elif signal_gap_persists or signal_mse_persists:
        verdict = "PTD-AUX-SIGNAL-PARTIAL-AT-SCALE"
    else:
        verdict = "PTD-AUX-SIGNAL-NOISE-OUT-AT-SCALE"

    # CONTINUE_THINK relative hardness in PTD MSE
    s48_ct_hard_factor_lam03 = (
        (e03["ptd_aux_next_state_mse_per_class"]["CONTINUE_THINK"] /
         e03["ptd_aux_next_state_mse_per_class"]["REMAIN_SILENT"])
        if e03["ptd_aux_next_state_mse_per_class"]["REMAIN_SILENT"] else None
    )
    s44_ct_hard_factor_lam03 = (
        s44["lambda_ptd_03"]["ptd_mse_per_class"]["CONTINUE_THINK"] /
        s44["lambda_ptd_03"]["ptd_mse_per_class"]["REMAIN_SILENT"]
    )

    summary = {
        "research_md_section": "§48",
        "title": "DH-DL + PTD-aux scale-up — 4× corpus, 4 phase regimes",
        "$cost": "$0 Mac CPU (numpy hand-coded backprop, no GPU)",
        "wall_sec": round(time.time() - t0, 2),
        "corpus": {
            "path": str(CORPUS),
            "n_records": 192000,
            "scale_vs_s44": 4.0,
            "n_phase_regimes": 4,
        },
        "baseline_s44_gap_lam0": s44["lambda_ptd_0"]["gap"],
        "baseline_s44_gap_lam03": s44["lambda_ptd_03"]["gap"],
        "baseline_s44_delta_gap": s44_delta_gap,
        "baseline_s44_ptd_drop_factor": s44_ptd_drop_factor,
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
        "delta_gap_03_minus_0": delta_gap,
        "delta_accuracy_03_minus_0": delta_acc,
        "s48_ptd_drop_factor": s48_ptd_drop_factor,
        "s48_ct_hard_factor_vs_remain_silent_lam03": s48_ct_hard_factor_lam03,
        "s44_ct_hard_factor_vs_remain_silent_lam03": s44_ct_hard_factor_lam03,
        "signal_gap_persists": signal_gap_persists,
        "signal_mse_persists": signal_mse_persists,
        "scaleup_verdict": verdict,
        "honest_note": (
            "§48 scaled §44 by 4× (48k → 192k records, single regime → 4 "
            "phase regimes). If PTD-aux signal HOLDS at scale, §44's "
            "representation-shaping finding is mechanism-real (not artifact); "
            "if NOISES OUT, §44 was small-corpus measurement noise. Either "
            "way: still DISTILLATION (§38 §7) — decision label is the §24 "
            "hand-coded threshold; head learns that function. NOT GOAL "
            "emergence. necessary-not-sufficient per B-S48-NOTE."
        ),
    }
    (HERE / "result.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )
    print("\n=== §48 summary ===")
    print(json.dumps({
        "s44_gap_lam0": summary["baseline_s44_gap_lam0"],
        "s44_gap_lam03": summary["baseline_s44_gap_lam03"],
        "s48_gap_lam0": summary["lambda_ptd_0"]["gap"],
        "s48_gap_lam03": summary["lambda_ptd_03"]["gap"],
        "s48_delta_gap_03_minus_0": summary["delta_gap_03_minus_0"],
        "s44_ptd_drop_factor": summary["baseline_s44_ptd_drop_factor"],
        "s48_ptd_drop_factor": summary["s48_ptd_drop_factor"],
        "s44_ct_hard_factor_lam03": summary["s44_ct_hard_factor_vs_remain_silent_lam03"],
        "s48_ct_hard_factor_lam03": summary["s48_ct_hard_factor_vs_remain_silent_lam03"],
        "scaleup_verdict": summary["scaleup_verdict"],
        "wall_sec": summary["wall_sec"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
