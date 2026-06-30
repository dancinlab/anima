#!/usr/bin/env python3
"""training/alpha_metric_v2.py — α-metric V2 (binned ΔΦ-rate vs cell_count, with
saturation auto-detection + UNRELIABLE per-bin emit).

Lane: BG-NEW-ALPHA-METRIC-V2 (track B reborn.B.cond.5 follow-up to §27).

PURPOSE
    Replace the legacy α V1 (OLS log Φ vs log n_cells over the whole trajectory)
    with a per-bin ΔΦ-rate metric that:
      • bins cell_count into [N_lo, N_hi) intervals,
      • estimates dΦ/d(split_event) per-bin from samples whose `n_cells_pre`
        falls in that bin,
      • auto-emits "UNRELIABLE" for bins with too few samples,
      • auto-emits a `saturation_warning` when the last (highest-N) bin's
        ΔΦ/Δsplit drops below `saturation_rate_threshold` (max_cap regression
        artifact detection),
      • optionally separates "trended" pairs (split occurred in the gap) from
        "untrended" idle drift, returning a separate set of per-bin α's.

    The V2 alpha_per_bin emit avoids the V1 OLS artifact where the [n_cells = max_cap]
    plateau dominates the log-log slope (10K toy α V1 = 1.252 spurious — Φ growth
    after cap is pure Lorenz/ratchet drift, not mitosis scaling).

DESIGN DOC
    (Companion) `state/anima_alpha_metric_v2_2026_05_10/design.md`.

    Predecessor design SSOT: `docs/anima_clm_v5_alpha_metric_v2_design_2026_05_10.md`
    (§3, §7) which §27 (`state/anima_alpha_v2_impl_2026_05_10/alpha_v2.py`) implemented
    as a *single aggregate* α with E-wrapper UNRELIABLE gate. This module is the
    *per-bin* sibling — same metric family, different granularity.

PUBLIC API
    compute_alpha_v2(history: list[dict]) -> dict

    history schema (per-step record):
        { "step":           int   (monotone, may be sparse),
          "cell_count":     int,
          "phi_unnorm":     float,
          "split_event_bool": bool   (True iff a split happened on this step) }

    Compatibility: also accepts the v5 long-trajectory snapshot schema
        { "turn", "n_cells", "phi", "n_splits_cum" }
    via auto-translate: split_event_bool := (n_splits_cum_t > n_splits_cum_{t-1}).

    Return dict:
        {
            "alpha_per_bin": {(N_lo, N_hi): float | "UNRELIABLE", ...},
            "alpha_aggregate": float | "UNRELIABLE",
            "saturation_warning": bool,
            "samples_per_bin": {(N_lo, N_hi): int, ...},
            "splits_per_bin": {(N_lo, N_hi): int, ...},
            "trended_alpha_per_bin": {(N_lo, N_hi): float | "UNRELIABLE", ...},
            "untrended_alpha_per_bin": {(N_lo, N_hi): float | "UNRELIABLE", ...},
            "bin_edges": [N0, N1, ..., Nk],
            "diagnostics": {
                "n_history": int,
                "n_pairs": int,
                "n_splits_total": int,
                "max_cap_reached": bool,
                "last_bin_rate": float | None,
                "saturation_rate_threshold": float,
            },
        }

raw#9   training/*.py local-only (gitignored — `**/*.py`).
raw#15  additive — does NOT modify mitosis_v5_port.py or alpha_v2.py (§27 sibling).
  honest emit — bins with samples < min_samples emit UNRELIABLE, not silent skip.
"""

from __future__ import annotations

import math
from typing import Iterable, List, Optional, Sequence, Tuple


# ─── defaults ────────────────────────────────────────────────────────────

DEFAULT_BIN_EDGES: tuple[int, ...] = (4, 8, 16, 32, 64, 128)
DEFAULT_MIN_SAMPLES: int = 30
DEFAULT_SATURATION_RATE_THRESHOLD: float = 1e-5  # ΔΦ/Δsplit floor
DEFAULT_AGGREGATE_MIN_BINS: int = 2


# ─── helpers ────────────────────────────────────────────────────────────


def _normalize_history(history: Sequence[dict]) -> List[dict]:
    """Translate v5 snapshot schema → required schema.

    Accepts either the user's spec schema
        {step, cell_count, phi_unnorm, split_event_bool}
    or the v5 long-trajectory snapshot schema
        {turn, n_cells, phi, n_splits_cum}
    and emits the canonical form. raw#10 honest: split_event_bool from
    n_splits_cum is "did at least one split happen in the gap?", which
    underestimates batched splits in a single step but matches the boolean
    semantics requested.
    """
    out: List[dict] = []
    prev_splits_cum: Optional[int] = None
    for s in history:
        step = s.get("step", s.get("turn"))
        cells = s.get("cell_count", s.get("n_cells"))
        phi = s.get("phi_unnorm", s.get("phi"))
        if step is None or cells is None or phi is None:
            continue
        if "split_event_bool" in s:
            split_evt = bool(s["split_event_bool"])
        elif "n_splits_cum" in s:
            cur = int(s["n_splits_cum"])
            split_evt = (
                False if prev_splits_cum is None else (cur > prev_splits_cum)
            )
            prev_splits_cum = cur
        else:
            split_evt = False
        out.append({
            "step": int(step),
            "cell_count": int(cells),
            "phi_unnorm": float(phi),
            "split_event_bool": bool(split_evt),
            "_n_splits_cum": int(s.get("n_splits_cum", -1)),
        })
    return out


def _build_pairs(history: List[dict]) -> List[dict]:
    """Adjacent-pair (s_i, s_{i+1}) records.

    Each pair has:
        n_cells_pre:  s_i.cell_count
        d_phi:        s_{i+1}.phi - s_i.phi
        d_step:       s_{i+1}.step - s_i.step
        d_splits:     splits in the gap (== 1 if split_event_bool else 0,
                      OR the cumulative diff if available — preferred since
                      multiple splits can fire in one step).
        split_in_gap: bool — at least one split fired.
    """
    pairs: List[dict] = []
    for a, b in zip(history[:-1], history[1:]):
        d_step = b["step"] - a["step"]
        if d_step <= 0:
            continue
        d_phi = b["phi_unnorm"] - a["phi_unnorm"]
        # Prefer cumulative-split diff when available (catches batched splits).
        if a.get("_n_splits_cum", -1) >= 0 and b.get("_n_splits_cum", -1) >= 0:
            d_splits = max(0, b["_n_splits_cum"] - a["_n_splits_cum"])
        else:
            d_splits = 1 if b["split_event_bool"] else 0
        pairs.append({
            "n_cells_pre": a["cell_count"],
            "n_cells_post": b["cell_count"],
            "d_phi": d_phi,
            "d_step": d_step,
            "d_splits": d_splits,
            "split_in_gap": d_splits > 0,
        })
    return pairs


def _bin_index(n: int, edges: Sequence[int]) -> Optional[int]:
    """Half-open [edges[i], edges[i+1]) bin index, or None if out of range."""
    for i in range(len(edges) - 1):
        if edges[i] <= n < edges[i + 1]:
            return i
    return None


def _per_bin_rate(
    pairs: List[dict],
    edges: Sequence[int],
    min_samples: int,
    metric: str = "per_split",
):
    """Compute mean ΔΦ-rate per bin.

    metric:
      - "per_split":  ΔΦ / max(Δsplits, 1) for split_in_gap pairs only
                      (the "trended" channel — what mitosis-driven Φ growth
                      looks like per-split-event).
      - "per_step":   ΔΦ / Δstep over ALL pairs (the legacy V1-style time-rate;
                      includes idle drift).
      - "trended":    ΔΦ / Δstep restricted to split_in_gap == True.
      - "untrended":  ΔΦ / Δstep restricted to split_in_gap == False.

    Returns (rate_per_bin, count_per_bin, splits_per_bin) where
        rate_per_bin[b] = mean rate or None if zero samples.
    """
    n_bins = len(edges) - 1
    sums = [0.0] * n_bins
    counts = [0] * n_bins
    splits = [0] * n_bins
    for p in pairs:
        b = _bin_index(p["n_cells_pre"], edges)
        if b is None:
            continue
        splits[b] += p["d_splits"]
        if metric == "per_split":
            if not p["split_in_gap"]:
                continue
            r = p["d_phi"] / max(p["d_splits"], 1)
        elif metric == "per_step":
            r = p["d_phi"] / p["d_step"]
        elif metric == "trended":
            if not p["split_in_gap"]:
                continue
            r = p["d_phi"] / p["d_step"]
        elif metric == "untrended":
            if p["split_in_gap"]:
                continue
            r = p["d_phi"] / p["d_step"]
        else:
            raise ValueError(f"unknown metric {metric}")
        sums[b] += r
        counts[b] += 1
    rate_per_bin: List[Optional[float]] = []
    for b in range(n_bins):
        if counts[b] == 0:
            rate_per_bin.append(None)
        else:
            rate_per_bin.append(sums[b] / counts[b])
    return rate_per_bin, counts, splits


def _ols(xs: Sequence[float], ys: Sequence[float]) -> Optional[float]:
    """OLS slope; None if degenerate."""
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    if den <= 0:
        return None
    return num / den


def _bin_alpha(
    rate_per_bin: List[Optional[float]],
    counts: List[int],
    edges: Sequence[int],
    min_samples: int,
) -> dict:
    """Per-bin α emit.

    For each bin b (well-defined if counts[b] >= min_samples and rate>0),
    α_b is computed as the local log-log slope of rate vs midpoint, USING
    THIS BIN AND ITS NEAREST NEIGHBOR (left or right) — a 2-point local
    estimate. Bins without a usable neighbor → UNRELIABLE.

    This gives "per-bin α" semantics (a local exponent) rather than a single
    global slope. Honest C3: a 2-point estimate is high-variance; the aggregate
    α (computed from ALL valid bins) is the more stable scalar.
    """
    n_bins = len(edges) - 1
    midpts: List[Optional[float]] = []
    for b in range(n_bins):
        lo, hi = edges[b], edges[b + 1]
        midpts.append(math.sqrt(lo * hi))  # geometric mid

    valid = [
        b
        for b in range(n_bins)
        if counts[b] >= min_samples
        and rate_per_bin[b] is not None
        and rate_per_bin[b] > 0
    ]
    valid_set = set(valid)

    alpha_per_bin: dict = {}
    for b in range(n_bins):
        key = (edges[b], edges[b + 1])
        if b not in valid_set:
            alpha_per_bin[key] = "UNRELIABLE"
            continue
        # find nearest valid neighbor
        neighbors = [v for v in valid if v != b]
        if not neighbors:
            alpha_per_bin[key] = "UNRELIABLE"
            continue
        nb = min(neighbors, key=lambda v: abs(v - b))
        x0, y0 = math.log(midpts[b]), math.log(rate_per_bin[b])  # type: ignore[arg-type]
        x1, y1 = math.log(midpts[nb]), math.log(rate_per_bin[nb])  # type: ignore[arg-type]
        if x1 == x0:
            alpha_per_bin[key] = "UNRELIABLE"
        else:
            alpha_per_bin[key] = (y1 - y0) / (x1 - x0)
    return alpha_per_bin


def _aggregate_alpha(
    rate_per_bin: List[Optional[float]],
    counts: List[int],
    edges: Sequence[int],
    min_samples: int,
    min_bins: int,
):
    """Single global α via OLS on (log midpt, log rate) over all VALID bins."""
    n_bins = len(edges) - 1
    xs, ys = [], []
    for b in range(n_bins):
        if counts[b] < min_samples:
            continue
        r = rate_per_bin[b]
        if r is None or r <= 0:
            continue
        lo, hi = edges[b], edges[b + 1]
        xs.append(math.log(math.sqrt(lo * hi)))
        ys.append(math.log(r))
    if len(xs) < min_bins:
        return "UNRELIABLE", len(xs)
    slope = _ols(xs, ys)
    if slope is None:
        return "UNRELIABLE", len(xs)
    return slope, len(xs)


# ─── public API ─────────────────────────────────────────────────────────


def compute_alpha_v2(
    history: Sequence[dict],
    bin_edges: Iterable[int] = DEFAULT_BIN_EDGES,
    min_samples: int = DEFAULT_MIN_SAMPLES,
    saturation_rate_threshold: float = DEFAULT_SATURATION_RATE_THRESHOLD,
    aggregate_min_bins: int = DEFAULT_AGGREGATE_MIN_BINS,
) -> dict:
    """A2 binned ΔΦ-rate α-metric V2 with per-bin UNRELIABLE emit + saturation guard.

    See module docstring for full behavior. Returns the dict described therein.
    """
    edges = list(bin_edges)
    if any(edges[i] >= edges[i + 1] for i in range(len(edges) - 1)):
        raise ValueError("bin_edges must be strictly increasing")

    norm = _normalize_history(history)
    pairs = _build_pairs(norm)

    # primary metric: ΔΦ per split event ("per_split" — trended channel)
    rate_pb, counts_pb, splits_pb = _per_bin_rate(
        pairs, edges, min_samples, metric="per_split"
    )
    # trended (per-step ΔΦ, only when splits in gap)
    rate_t, counts_t, _ = _per_bin_rate(pairs, edges, min_samples, metric="trended")
    # untrended (per-step ΔΦ, only idle gaps)
    rate_u, counts_u, _ = _per_bin_rate(pairs, edges, min_samples, metric="untrended")

    alpha_per_bin = _bin_alpha(rate_pb, counts_pb, edges, min_samples)
    alpha_trended = _bin_alpha(rate_t, counts_t, edges, min_samples)
    alpha_untrended = _bin_alpha(rate_u, counts_u, edges, min_samples)

    alpha_agg, n_valid = _aggregate_alpha(
        rate_pb, counts_pb, edges, min_samples, aggregate_min_bins
    )

    # saturation auto-detect: cell_count reached its observed maximum AND
    # plateaued there for the latter portion of the trajectory.
    n_history = len(norm)
    max_cell_count = max((s["cell_count"] for s in norm), default=0)
    cap_inferred = edges[-1]  # last edge is the assumed max_cap upper bound
    # plateau detection: if the last 25% of steps all have n_cells == max_observed
    # AND max_observed is within the highest non-empty bin, treat as "max_cap reached".
    if n_history >= 4:
        tail = norm[-max(n_history // 4, 1):]
        plateau = all(s["cell_count"] == max_cell_count for s in tail)
    else:
        plateau = False
    max_cap_reached = plateau

    last_bin_rate: Optional[float] = None
    saturation_warning = False
    if rate_pb:
        # walk from the last bin downward to first non-empty
        for b in range(len(rate_pb) - 1, -1, -1):
            if counts_pb[b] > 0 and rate_pb[b] is not None:
                last_bin_rate = rate_pb[b]
                if last_bin_rate < saturation_rate_threshold:
                    saturation_warning = True
                break
    # Independent trigger: max_cap reached AND aggregate rate of "untrended"
    # in last reachable bin > primary rate (drift-dominated).
    if max_cap_reached:
        # any bin with rate_u > rate_pb means idle drift dominates split-driven
        for b in range(len(rate_pb) - 1, -1, -1):
            if (
                counts_pb[b] > 0
                and rate_pb[b] is not None
                and counts_u[b] > 0
                and rate_u[b] is not None
                and rate_u[b] >= rate_pb[b]
            ):
                saturation_warning = True
                break

    samples_per_bin = {
        (edges[b], edges[b + 1]): counts_pb[b] for b in range(len(edges) - 1)
    }
    splits_per_bin = {
        (edges[b], edges[b + 1]): splits_pb[b] for b in range(len(edges) - 1)
    }

    return {
        "alpha_per_bin": alpha_per_bin,
        "alpha_aggregate": alpha_agg,
        "saturation_warning": saturation_warning,
        "samples_per_bin": samples_per_bin,
        "splits_per_bin": splits_per_bin,
        "trended_alpha_per_bin": alpha_trended,
        "untrended_alpha_per_bin": alpha_untrended,
        "rate_per_bin_per_split": {
            (edges[b], edges[b + 1]): rate_pb[b] for b in range(len(edges) - 1)
        },
        "rate_per_bin_trended": {
            (edges[b], edges[b + 1]): rate_t[b] for b in range(len(edges) - 1)
        },
        "rate_per_bin_untrended": {
            (edges[b], edges[b + 1]): rate_u[b] for b in range(len(edges) - 1)
        },
        "bin_edges": edges,
        "diagnostics": {
            "n_history": n_history,
            "n_pairs": len(pairs),
            "n_splits_total": sum(splits_pb),
            "max_cell_count_observed": max_cell_count,
            "max_cap_inferred": cap_inferred,
            "max_cap_reached": max_cap_reached,
            "last_bin_rate": last_bin_rate,
            "saturation_rate_threshold": saturation_rate_threshold,
            "n_valid_bins_for_aggregate": n_valid,
            "aggregate_min_bins": aggregate_min_bins,
            "min_samples": min_samples,
        },
    }


def alpha_v1_ols(
    history: Sequence[dict],
    phi_field_candidates: Tuple[str, ...] = ("phi_unnorm", "phi"),
    n_field_candidates: Tuple[str, ...] = ("cell_count", "n_cells"),
) -> Optional[float]:
    """V1 reference α: OLS log(Φ) vs log(n_cells) over the entire trajectory.

    Replicates the historical artifact for V1 vs V2 comparison.
    """
    xs, ys = [], []
    for s in history:
        n = next((s[k] for k in n_field_candidates if k in s), None)
        p = next((s[k] for k in phi_field_candidates if k in s), None)
        if n is None or p is None:
            continue
        if n <= 0 or p <= 0:
            continue
        xs.append(math.log(n))
        ys.append(math.log(p))
    return _ols(xs, ys)


# ─── self-test (smoke) ──────────────────────────────────────────────────

if __name__ == "__main__":
    # Synthetic history exhibiting α≈1 super-linear up to N=64 then saturation.
    import random as _r
    _r.seed(42)
    h: list[dict] = []
    n = 8
    phi = 2.0
    splits_cum = 0
    for step in range(0, 1000):
        # fire a split with prob proportional to (n*0.005) up to cap
        if n < 64 and _r.random() < 0.05:
            n += 1
            splits_cum += 1
            phi += 0.05 * (n ** 1.0)  # exact α=1 super-linear
        else:
            phi += 0.001  # idle drift (untrended)
        h.append({
            "step": step,
            "cell_count": n,
            "phi_unnorm": phi,
            "n_splits_cum": splits_cum,
        })
    res = compute_alpha_v2(h)
    print("aggregate α =", res["alpha_aggregate"])
    print("per-bin α =", res["alpha_per_bin"])
    print("samples =", res["samples_per_bin"])
    print("splits =", res["splits_per_bin"])
    print("saturation_warning =", res["saturation_warning"])
    print("max_cap_reached =", res["diagnostics"]["max_cap_reached"])
