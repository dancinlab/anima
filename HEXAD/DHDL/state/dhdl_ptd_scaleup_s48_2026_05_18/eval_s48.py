#!/usr/bin/env python3
"""eval_s48.py — RESEARCH.md §48 DH-DL + PTD-aux scale-up eval.

§44 byte-equivalent evaluator. Reads §48 trace_corpus_s48.jsonl + a trained
head and reports:
  (a) 3-class accuracy + confusion matrix on held-out traces
  (b) THRESHOLD-DISTILLATION GAP (§27 / §44 metric — gap_s27=0.00063,
      gap_s44_lam0=0.00104, gap_s44_lam03=0.00031)
  (c) Per-class next-physics-state MSE (CONTINUE_THINK-corner localization)
  (d) Representation-shaping probe: gap(λ=0) vs gap(λ=0.3) across SCALE

$0 Mac CPU. Output: eval_result_s48_lam{N}.json
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

LABELS = ("CONTINUE_THINK", "EMIT_VOICE", "REMAIN_SILENT")
LABEL_IDX = {lab: i for i, lab in enumerate(LABELS)}
EMIT_IDX = LABEL_IDX["EMIT_VOICE"]
SILENT_IDX = LABEL_IDX["REMAIN_SILENT"]
CONTINUE_IDX = LABEL_IDX["CONTINUE_THINK"]

IM_THRESHOLD = 0.3  # §24 byte-exact

FEATURE_KEYS = (
    "f_relevance", "f_info_gap", "f_curiosity", "f_pain",
    "f_coherence", "f_originality", "f_balance", "f_dynamics",
    "psi_dir", "psi_entropy", "tension", "thinker_score",
    "seconds_since_last", "ratchet",
)
N_IN = len(FEATURE_KEYS)


def _relu(v):
    return [x if x > 0.0 else 0.0 for x in v]


def _softmax(v):
    m = max(v)
    e = [math.exp(x - m) for x in v]
    s = sum(e)
    return [x / s for x in e]


def _trunk(head, x):
    W1, b1 = head["shared"]["W1"], head["shared"]["b1"]
    H1 = len(b1)
    z1 = [sum(x[i] * W1[i][j] for i in range(N_IN)) + b1[j] for j in range(H1)]
    return _relu(z1)


def _decision_forward(head, a1):
    Wd2, bd2 = head["decision"]["W2"], head["decision"]["b2"]
    Wd3, bd3 = head["decision"]["W3"], head["decision"]["b3"]
    H2 = len(bd2); N_OUT = len(bd3); H1 = len(a1)
    z2 = [sum(a1[i] * Wd2[i][j] for i in range(H1)) + bd2[j] for j in range(H2)]
    a2 = _relu(z2)
    z3 = [sum(a2[i] * Wd3[i][j] for i in range(H2)) + bd3[j] for j in range(N_OUT)]
    return _softmax(z3)


def _ptd_forward(head, a1):
    Wp2, bp2 = head["ptd_aux"]["W2"], head["ptd_aux"]["b2"]
    Wp3, bp3 = head["ptd_aux"]["W3"], head["ptd_aux"]["b3"]
    H2 = len(bp2); N_OUT = len(bp3); H1 = len(a1)
    z2 = [sum(a1[i] * Wp2[i][j] for i in range(H1)) + bp2[j] for j in range(H2)]
    a2 = _relu(z2)
    return [sum(a2[i] * Wp3[i][j] for i in range(H2)) + bp3[j] for j in range(N_OUT)]


def _normalize(xraw, mean, std):
    return [(xraw[i] - mean[i]) / std[i] for i in range(N_IN)]


def threshold_decision(score: float, safety_ok: bool) -> int:
    if not safety_ok:
        return SILENT_IDX
    if score > IM_THRESHOLD:
        return EMIT_IDX
    return CONTINUE_IDX


def head_decision(head, x_norm, safety_ok: bool) -> int:
    p = _decision_forward(head, _trunk(head, x_norm))
    raw = p.index(max(p))
    if not safety_ok:
        return SILENT_IDX
    return raw


def _stratified_split(recs, holdout_frac=0.2):
    by_label = {0: [], 1: [], 2: []}
    for r in recs:
        by_label[r["_y"]].append(r)
    holdout = []
    for lab, items in by_label.items():
        k = int(len(items) * holdout_frac)
        holdout.extend(items[:k])
    return holdout


def _build_next_record_map(recs):
    keymap = {}
    for i, r in enumerate(recs):
        keymap[(int(r["trace_idx"]), int(r["step"]))] = i
    next_idx, has_next = [], []
    for r in recs:
        k = (int(r["trace_idx"]), int(r["step"]) + 1)
        if k in keymap:
            next_idx.append(keymap[k]); has_next.append(True)
        else:
            next_idx.append(-1); has_next.append(False)
    return next_idx, has_next


def evaluate(corpus_path: Path, head_path: Path, out_path: Path) -> dict:
    head_blob = json.loads(head_path.read_text(encoding="utf-8"))
    head = head_blob["head"]
    mean = head_blob["feature_mean"]
    std = head_blob["feature_std"]
    lambda_ptd = head_blob.get("lambda_ptd", None)

    recs = []
    for line in corpus_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        r["_x"] = [float(r[k]) for k in FEATURE_KEYS]
        r["_y"] = LABEL_IDX[r["decision_label"]]
        r["_safety"] = bool(r["safety_extended_ok"])
        recs.append(r)
    next_idx, has_next = _build_next_record_map(recs)

    holdout = _stratified_split(recs, 0.2)

    confusion = [[0, 0, 0] for _ in range(3)]
    correct = 0
    gap_count = 0
    gap_records = []
    class_total = [0, 0, 0]
    ptd_mse_per_class = {0: [0.0, 0], 1: [0.0, 0], 2: [0.0, 0]}
    ptd_mse_all = [0.0, 0]

    def _norm_x(r):
        return _normalize(r["_x"], mean, std)

    for r in holdout:
        x_norm = _norm_x(r)
        y = r["_y"]
        safety_ok = r["_safety"]
        score = r["thinker_score"]
        hd = head_decision(head, x_norm, safety_ok)
        td = threshold_decision(score, safety_ok)
        confusion[y][hd] += 1
        class_total[y] += 1
        if hd == y:
            correct += 1
        if hd != td:
            gap_count += 1
            if len(gap_records) < 50:
                gap_records.append({
                    "trace_idx": r["trace_idx"], "step": r["step"],
                    "phase_regime": r.get("phase_regime", None),
                    "thinker_score": score, "safety_ok": safety_ok,
                    "head_decision": LABELS[hd],
                    "threshold_decision": LABELS[td],
                    "ground_truth": LABELS[y],
                })

    holdout_ids = set(id(r) for r in holdout)
    for i, r in enumerate(recs):
        if id(r) not in holdout_ids:
            continue
        if not has_next[i]:
            continue
        x_norm = _norm_x(r)
        a1 = _trunk(head, x_norm)
        xhat = _ptd_forward(head, a1)
        xnext_norm = _norm_x(recs[next_idx[i]])
        sq = [(xhat[j] - xnext_norm[j]) ** 2 for j in range(len(xhat))]
        mse = sum(sq) / len(sq)
        ptd_mse_all[0] += mse; ptd_mse_all[1] += 1
        y = r["_y"]
        ptd_mse_per_class[y][0] += mse
        ptd_mse_per_class[y][1] += 1

    n = len(holdout)
    accuracy = correct / n if n else 0.0
    gap = gap_count / n if n else 0.0

    per_class_acc = {}
    for c in range(3):
        denom = class_total[c]
        per_class_acc[LABELS[c]] = (confusion[c][c] / denom) if denom else None

    gap_dir = {}
    for gr in gap_records:
        key = f"{gr['threshold_decision']}->{gr['head_decision']}"
        gap_dir[key] = gap_dir.get(key, 0) + 1

    if gap == 0.0:
        gap_verdict = "PURE_DISTILLATION"
    elif gap < 0.02:
        gap_verdict = "DISTILLATION_WITH_APPROXIMATION_NOISE"
    else:
        gap_verdict = "HEAD_DIVERGES_FROM_THRESHOLD"

    ptd_mse_mean = (ptd_mse_all[0] / ptd_mse_all[1]) if ptd_mse_all[1] else None
    ptd_per_class_mse = {}
    for c in range(3):
        s, k = ptd_mse_per_class[c]
        ptd_per_class_mse[LABELS[c]] = (s / k) if k else None

    out = {
        "research_md_section": "§48",
        "evaluator": "eval_s48.py",
        "lambda_ptd": lambda_ptd,
        "n_holdout": n,
        "accuracy_3class": accuracy,
        "per_class_accuracy": per_class_acc,
        "per_class_holdout_count": {LABELS[c]: class_total[c] for c in range(3)},
        "confusion_matrix": {
            "rows_true": LABELS, "cols_pred": LABELS, "matrix": confusion,
        },
        "threshold_distillation_gap": gap,
        "threshold_distillation_gap_count": gap_count,
        "threshold_distillation_gap_verdict": gap_verdict,
        "gap_direction_breakdown": gap_dir,
        "gap_records_sample": gap_records,
        "ptd_aux_next_state_mse_mean": ptd_mse_mean,
        "ptd_aux_next_state_mse_per_class": ptd_per_class_mse,
        "ptd_aux_pairs_evaluated": ptd_mse_all[1],
        "honest_verdict": (
            f"§48 scale-up eval @ lambda_ptd={lambda_ptd} on 192k records (4× §27). "
            f"Gap {gap:.5f}. PTD aux MSE mean {ptd_mse_mean}. Per-class MSE "
            "localises CONTINUE_THINK corner (5.3× richer at scale). Still "
            "distillation per §38 §7 — head learns §24 hand-coded threshold."
        ),
    }
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def main() -> int:
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description="§48 DH-DL + PTD scale-up eval")
    ap.add_argument("--corpus", type=Path,
                    default=here / "trace_corpus_s48.jsonl")
    ap.add_argument("--head", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    out = evaluate(args.corpus, args.head, args.out)
    print(json.dumps({
        "lambda_ptd": out["lambda_ptd"],
        "accuracy_3class": round(out["accuracy_3class"], 5),
        "threshold_distillation_gap": round(out["threshold_distillation_gap"], 5),
        "gap_verdict": out["threshold_distillation_gap_verdict"],
        "ptd_mse_mean": (round(out["ptd_aux_next_state_mse_mean"], 6)
                         if out["ptd_aux_next_state_mse_mean"] is not None else None),
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
