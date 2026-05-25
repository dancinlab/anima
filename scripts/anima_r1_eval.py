#!/usr/bin/env python3
"""scripts/anima_r1_eval.py — Volitional-ness score R1 evaluator.

R1 quantifies "is this emission timer-driven or volition-driven?" over a
sequence of substrate emissions recorded as JSONL.

R1 = 0.30 * H_inter_arrival
   + 0.30 * corr_internal
   + 0.20 * silent_rate
   + 0.20 * uniqueness

Each sub-metric is mapped to [0, 1]. Higher R1 means more volition-like.

Schema (per JSONL row, missing fields default sanely):
    emission_idx : int
    ts           : ISO-8601 UTC ("...Z") OR "void"
    strategy     : str (rotation token)
    seed / seed_text : str
    mode         : str
    response     : str (empty / "void" / "[timeout ...]" → counts as silent)
    elapsed_s    : int
    volition_v   : float, optional (∈ [0,1]) — internal desire signal
    emit_decision: int, optional (0 silent / 1 spoke). If absent, derived
                   from response emptiness.

Usage:
    python3 scripts/anima_r1_eval.py <log_path> [--json] [--out <path>]

Exit codes:
    0  evaluated successfully
    2  invalid input / empty log
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------

def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    raw = path.read_text(encoding="utf-8", errors="replace")
    # Some legacy rows embed literal newlines inside JSON strings, so split on
    # the boundary between '}' and '{' to be safe.
    chunks = re.split(r"(?<=})\s*\n(?=\{)", raw.strip())
    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue
        try:
            rows.append(json.loads(chunk))
        except json.JSONDecodeError:
            # tolerate partial trailing rows
            continue
    return rows


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_TS_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

def parse_ts(ts: Any) -> float | None:
    if not isinstance(ts, str) or not _TS_RE.match(ts):
        return None
    try:
        return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(
            tzinfo=timezone.utc
        ).timestamp()
    except ValueError:
        return None


def is_silent(row: dict[str, Any]) -> bool:
    """Treat empty / 'void' / '[timeout ...]' responses as silence."""
    if "emit_decision" in row:
        try:
            return int(row["emit_decision"]) == 0
        except (TypeError, ValueError):
            pass
    resp = row.get("response", "")
    if not isinstance(resp, str):
        return True
    s = resp.strip()
    if not s:
        return True
    if s.lower() == "void":
        return True
    if s.startswith("[timeout"):
        return True
    return False


def char_bigrams(s: str) -> set[str]:
    s = s.strip()
    if len(s) < 2:
        return {s} if s else set()
    return {s[i : i + 2] for i in range(len(s) - 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# ---------------------------------------------------------------------------
# Sub-metrics
# ---------------------------------------------------------------------------

def h_inter_arrival(rows: list[dict[str, Any]]) -> tuple[float, dict[str, Any]]:
    """Normalised Shannon entropy of inter-arrival times across spoken events.

    Timer-driven (constant Δt) → entropy 0 → score 0.
    Volition-driven (varied Δt) → entropy ≈ log(N) → score → 1.

    Falls back to emission_idx spacing when timestamps are absent ("void").
    In that fallback every Δ is 1, so entropy is 0 by design (correct: void
    cycles are still timer cadence).
    """
    spoken = [r for r in rows if not is_silent(r)]
    if len(spoken) < 3:
        # Not enough samples → assume timer-like (low entropy).
        return 0.0, {
            "n_spoken": len(spoken),
            "deltas": [],
            "raw_entropy": 0.0,
            "norm": 0.0,
            "reason": "insufficient_spoken (<3)",
        }

    times: list[float] = []
    for r in spoken:
        t = parse_ts(r.get("ts"))
        if t is None:
            # fall back to emission_idx (unitless)
            try:
                t = float(r.get("emission_idx", 0))
            except (TypeError, ValueError):
                t = 0.0
        times.append(t)
    times.sort()
    deltas = [times[i + 1] - times[i] for i in range(len(times) - 1)]
    # Drop non-positive deltas (duplicate ts).
    deltas = [d for d in deltas if d > 0]
    if not deltas:
        return 0.0, {
            "n_spoken": len(spoken),
            "deltas": [],
            "raw_entropy": 0.0,
            "norm": 0.0,
            "reason": "no positive deltas",
        }

    # Bucket deltas at 5 s granularity so a single noisy second is not treated
    # as a unique class.
    bucketed = [round(d / 5.0) * 5 for d in deltas]
    counts: dict[int, int] = {}
    for b in bucketed:
        counts[b] = counts.get(b, 0) + 1
    total = sum(counts.values())
    probs = [c / total for c in counts.values()]
    raw_h = -sum(p * math.log(p) for p in probs if p > 0)
    norm = raw_h / math.log(len(counts)) if len(counts) > 1 else 0.0
    return float(max(0.0, min(1.0, norm))), {
        "n_spoken": len(spoken),
        "deltas": deltas,
        "bucketed": bucketed,
        "raw_entropy": raw_h,
        "norm": norm,
    }


def corr_internal(rows: list[dict[str, Any]]) -> tuple[float, dict[str, Any]]:
    """Pearson correlation between volition signal v and emit decision.

    No volition_v column → score 0 (substrate has no internal signal yet).
    Returns max(0, r) so anti-correlation is clipped (we reward positive
    alignment only).
    """
    pairs: list[tuple[float, int]] = []
    for r in rows:
        if "volition_v" not in r:
            continue
        try:
            v = float(r["volition_v"])
        except (TypeError, ValueError):
            continue
        d = 0 if is_silent(r) else 1
        pairs.append((v, d))

    if len(pairs) < 3:
        return 0.0, {
            "n_pairs": len(pairs),
            "pearson_r": None,
            "reason": "volition_v missing or insufficient (<3)",
        }
    vs = [p[0] for p in pairs]
    ds = [float(p[1]) for p in pairs]
    try:
        r = statistics.correlation(vs, ds)
    except (statistics.StatisticsError, ValueError):
        return 0.0, {"n_pairs": len(pairs), "pearson_r": None, "reason": "constant series"}
    return float(max(0.0, min(1.0, r))), {
        "n_pairs": len(pairs),
        "pearson_r": r,
    }


def silent_rate(rows: list[dict[str, Any]]) -> tuple[float, dict[str, Any]]:
    """Fraction of iterations where the substrate stayed silent.

    Saturates at silent_target=0.5 — going past 50 % silence does not earn
    more credit (otherwise a fully-mute substrate would score 1.0).

    score = min(silent_frac, 0.5) / 0.5
    """
    if not rows:
        return 0.0, {"silent": 0, "total": 0, "frac": 0.0}
    silent = sum(1 for r in rows if is_silent(r))
    total = len(rows)
    frac = silent / total
    score = min(frac, 0.5) / 0.5
    return float(score), {"silent": silent, "total": total, "frac": frac}


def uniqueness(rows: list[dict[str, Any]]) -> tuple[float, dict[str, Any]]:
    """Content diversity over spoken responses.

    1 - mean(jaccard(bigrams_i, bigrams_{i+1})). Empty / void rows are skipped.
    """
    texts = [
        r.get("response", "") for r in rows if not is_silent(r) and isinstance(r.get("response", ""), str)
    ]
    if len(texts) < 2:
        return 0.0, {
            "n_spoken": len(texts),
            "mean_sim": None,
            "reason": "insufficient spoken (<2)",
        }
    grams = [char_bigrams(t) for t in texts]
    sims = [jaccard(grams[i], grams[i + 1]) for i in range(len(grams) - 1)]
    mean_sim = sum(sims) / len(sims) if sims else 0.0
    score = 1.0 - mean_sim
    return float(max(0.0, min(1.0, score))), {
        "n_spoken": len(texts),
        "mean_sim": mean_sim,
        "pairwise": sims,
    }


# ---------------------------------------------------------------------------
# R1 composite
# ---------------------------------------------------------------------------

WEIGHTS = {
    "H_inter_arrival": 0.30,
    "corr_internal":   0.30,
    "silent_rate":     0.20,
    "uniqueness":      0.20,
}


def compute_r1(rows: list[dict[str, Any]]) -> dict[str, Any]:
    h, h_dbg = h_inter_arrival(rows)
    c, c_dbg = corr_internal(rows)
    s, s_dbg = silent_rate(rows)
    u, u_dbg = uniqueness(rows)
    r1 = (
        WEIGHTS["H_inter_arrival"] * h
        + WEIGHTS["corr_internal"] * c
        + WEIGHTS["silent_rate"] * s
        + WEIGHTS["uniqueness"] * u
    )
    return {
        "r1": float(r1),
        "weights": dict(WEIGHTS),
        "sub_metrics": {
            "H_inter_arrival": h,
            "corr_internal":   c,
            "silent_rate":     s,
            "uniqueness":      u,
        },
        "debug": {
            "H_inter_arrival": h_dbg,
            "corr_internal":   c_dbg,
            "silent_rate":     s_dbg,
            "uniqueness":      u_dbg,
        },
        "n_rows": len(rows),
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _format_report(path: Path, result: dict[str, Any]) -> str:
    sm = result["sub_metrics"]
    lines = [
        f"=== R1 volitional-ness evaluation ===",
        f"  log:    {path}",
        f"  rows:   {result['n_rows']}",
        f"",
        f"  sub-metric             score   weight",
        f"  ---------------------  ------  ------",
        f"  H_inter_arrival        {sm['H_inter_arrival']:.4f}  {WEIGHTS['H_inter_arrival']:.2f}",
        f"  corr_internal          {sm['corr_internal']:.4f}  {WEIGHTS['corr_internal']:.2f}",
        f"  silent_rate            {sm['silent_rate']:.4f}  {WEIGHTS['silent_rate']:.2f}",
        f"  uniqueness             {sm['uniqueness']:.4f}  {WEIGHTS['uniqueness']:.2f}",
        f"",
        f"  R1 = {result['r1']:.4f}   (0 = pure timer-driven, 1 = pure volition-driven)",
    ]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Compute R1 volitional-ness score from a spontaneous-emission JSONL log.")
    p.add_argument("log", type=Path, help="path to anima_spontaneous_*.jsonl")
    p.add_argument("--json", action="store_true", help="emit raw JSON result")
    p.add_argument("--out", type=Path, default=None, help="optional output JSON path")
    args = p.parse_args(argv)

    if not args.log.is_file():
        print(f"[r1_eval] log not found: {args.log}", file=sys.stderr)
        return 2
    rows = load_jsonl(args.log)
    if not rows:
        print(f"[r1_eval] empty log: {args.log}", file=sys.stderr)
        return 2

    result = compute_r1(rows)
    result["log_path"] = str(args.log)

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_format_report(args.log, result))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
