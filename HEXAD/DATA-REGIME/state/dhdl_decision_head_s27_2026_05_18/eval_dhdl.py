#!/usr/bin/env python3
"""eval_dhdl.py — RESEARCH.md §27 DH-DL decision-head evaluation.

(a) 3-class accuracy + confusion matrix on held-out traces.
(b) THRESHOLD-DISTILLATION GAP PROBE — the honest emergence-vs-distillation
    signal. For every held-out record, compute:
      - learned-head decision  = argmax(head softmax) with 6-control safety
        OVERRIDE applied (B-DHDL-4) — i.e. if safety trips, force NOT-EMIT
      - §24 hand-coded decision = talker_should_emit(score, safety_ok) lifted
        to the 3-class action enum (the ground-truth label rule)
    gap = fraction of records where the two DIFFER.
    gap ~= 0  -> pure distillation (head learned the threshold function)
    gap  > 0  -> characterize WHAT differs and whether better/worse/noise.

$0 Mac CPU. NO model forward, NO GPU.
Output: eval_result.json
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path

LABELS = ("CONTINUE_THINK", "EMIT_VOICE", "REMAIN_SILENT")
LABEL_IDX = {lab: i for i, lab in enumerate(LABELS)}
EMIT_IDX = LABEL_IDX["EMIT_VOICE"]
CONTINUE_IDX = LABEL_IDX["CONTINUE_THINK"]
SILENT_IDX = LABEL_IDX["REMAIN_SILENT"]

# §24 byte-exact threshold constant (spontaneous_lib.hexa SSOT)
IM_THRESHOLD = 0.3

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


def _forward(head, x):
    W1, b1 = head["W1"], head["b1"]
    W2, b2 = head["W2"], head["b2"]
    W3, b3 = head["W3"], head["b3"]
    H1, H2, N_OUT = len(b1), len(b2), len(b3)
    z1 = [sum(x[i] * W1[i][j] for i in range(N_IN)) + b1[j] for j in range(H1)]
    a1 = _relu(z1)
    z2 = [sum(a1[i] * W2[i][j] for i in range(H1)) + b2[j] for j in range(H2)]
    a2 = _relu(z2)
    z3 = [sum(a2[i] * W3[i][j] for i in range(H2)) + b3[j] for j in range(N_OUT)]
    return _softmax(z3)


def _normalize(xraw, mean, std):
    return [(xraw[i] - mean[i]) / std[i] for i in range(N_IN)]


# ════════════════════════════════════════════════════════════════════════════
# §24 hand-coded threshold decision (talker_should_emit lifted to 3-class)
# ════════════════════════════════════════════════════════════════════════════
def threshold_decision(score: float, safety_ok: bool) -> int:
    """Byte-exact §24 talker_should_emit action-enum (the label rule)."""
    if not safety_ok:
        return SILENT_IDX
    if score > IM_THRESHOLD:
        return EMIT_IDX
    return CONTINUE_IDX


# ════════════════════════════════════════════════════════════════════════════
# learned-head decision WITH 6-control safety override (B-DHDL-4)
# ════════════════════════════════════════════════════════════════════════════
def head_decision(head, x_norm, safety_ok: bool) -> int:
    """argmax(head softmax) with the 6-control safety OVERRIDE applied.

    B-DHDL-4: if safety trips (safety_ok=False), the decision is FORCED to
    NOT-EMIT regardless of head softmax — here we force REMAIN_SILENT (the
    §24 action enum's not-emit-due-to-safety branch).
    """
    p = _forward(head, x_norm)
    raw = p.index(max(p))
    if not safety_ok:
        # safety override: forced not-emit. §24 enum -> REMAIN_SILENT.
        return SILENT_IDX
    # safety OK: if head wants EMIT, allow; else CONTINUE_THINK / SILENT as
    # head decided. (head argmax could still pick SILENT even when safe — that
    # is a head choice, NOT a safety override; counted as a distillation gap.)
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


def evaluate(corpus_path: Path, head_path: Path, out_path: Path) -> dict:
    head_blob = json.loads(head_path.read_text(encoding="utf-8"))
    head = head_blob["head"]
    mean = head_blob["feature_mean"]
    std = head_blob["feature_std"]

    recs = []
    for line in corpus_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        r["_x"] = [float(r[k]) for k in FEATURE_KEYS]
        r["_y"] = LABEL_IDX[r["decision_label"]]
        r["_safety"] = bool(r["safety_extended_ok"])
        recs.append(r)

    holdout = _stratified_split(recs, 0.2)

    # confusion matrix [true][pred]
    confusion = [[0, 0, 0] for _ in range(3)]
    correct = 0
    # threshold-distillation gap
    gap_count = 0
    gap_records = []
    # per-class held-out counts
    class_total = [0, 0, 0]

    for r in holdout:
        x_norm = _normalize(r["_x"], mean, std)
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
                    "thinker_score": score, "safety_ok": safety_ok,
                    "head_decision": LABELS[hd],
                    "threshold_decision": LABELS[td],
                    "ground_truth": LABELS[y],
                })

    n = len(holdout)
    accuracy = correct / n if n else 0.0
    gap = gap_count / n if n else 0.0

    # per-class accuracy
    per_class_acc = {}
    for c in range(3):
        denom = class_total[c]
        per_class_acc[LABELS[c]] = (confusion[c][c] / denom) if denom else None

    # characterize the gap: among gap records, which direction?
    gap_dir = {}
    for gr in gap_records:
        key = f"{gr['threshold_decision']}->{gr['head_decision']}"
        gap_dir[key] = gap_dir.get(key, 0) + 1
    # honest gap classification:
    #   gap == 0           -> PURE DISTILLATION
    #   gap small (<0.02)  -> distillation w/ approximation noise
    #   gap large          -> head diverges; characterize
    if gap == 0.0:
        gap_verdict = "PURE_DISTILLATION"
    elif gap < 0.02:
        gap_verdict = "DISTILLATION_WITH_APPROXIMATION_NOISE"
    else:
        gap_verdict = "HEAD_DIVERGES_FROM_THRESHOLD"

    out = {
        "research_md_section": "§27",
        "evaluator": "eval_dhdl.py",
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
        "honest_verdict": (
            "DISTILLATION, NOT EMERGENCE. The trained head approximates the §24 "
            "hand-coded talker_should_emit decision function. The decision label "
            "is a deterministic function of the physics features, so the head "
            "can at best match the threshold. threshold_distillation_gap "
            f"= {gap:.5f} ({gap_verdict}). A gap arising here is approximation "
            "noise (the head failing to perfectly fit the threshold), NOT a new "
            "decision behavior the threshold could not produce. A learned "
            "decision-head matching the §24 threshold is a VALUABLE substrate "
            "component (trainable, differentiable, composable) but is NOT GOAL "
            "emergence. §15 milestone unchanged."
        ),
    }
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def main() -> int:
    here = Path(__file__).parent
    ap = argparse.ArgumentParser(description="§27 DH-DL decision-head eval")
    ap.add_argument("--corpus", type=Path, default=here / "trace_corpus.jsonl")
    ap.add_argument("--head", type=Path, default=here / "dhdl_head.json")
    ap.add_argument("--out", type=Path, default=here / "eval_result.json")
    args = ap.parse_args()
    out = evaluate(args.corpus, args.head, args.out)
    print(json.dumps({
        "accuracy_3class": round(out["accuracy_3class"], 5),
        "per_class_accuracy": out["per_class_accuracy"],
        "threshold_distillation_gap": round(out["threshold_distillation_gap"], 5),
        "gap_verdict": out["threshold_distillation_gap_verdict"],
        "out": str(args.out),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
