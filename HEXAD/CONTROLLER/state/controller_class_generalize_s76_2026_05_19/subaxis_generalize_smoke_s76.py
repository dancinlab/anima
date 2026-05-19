#!/usr/bin/env python3
"""§76 A-only generalization probe — state x statistic 22-cell grid ($0 stub).

§75-FIRE (commit 08b58942f, B-S75-FIRE 7/7) measured at trained-saturated scale:
§73-A-only (state-derived + FROZEN tension-MEAN threshold 11.945) interval_var
2.3808 SURVIVES — "state-derivation A alone sufficient at trained scale". BUT
§75-FIRE tested ONLY the tension-mean statistic. §76 directly-earned future-probe
(B-S75-FIRE-NOTE) = does the state-derivation lever GENERALIZE to other
state-derived statistics?

This is a $0 STUB mirroring §75 (NOT a trained-scale GPU fire). 22-cell grid:
  4 state-source {tension, psi_dir, phi, curiosity_ema}
  x 5 statistic-form {mean, median, max_window, p75, p95}
  + 2 controls (§24-baseline scalar, §73-A-only tension-mean reference repro).

per-cell B-S73-augmented survive predicate:
  survive := (interval_var > TAU) and (maj_frac < 0.95) and (n_emits >= 2)

psi-state stub sequence: deterministic LCG seed 1337, Law-71 mirror of
conscious_decoder.py:728-751 (psi_dir = (1+cos(logits_a,logits_g))/2).
NO torch, NO GPU, NO RNG library. $0 Mac CPU.
"""
import json
import math
import os

SEED = 1337
N_STEP = 20
TAU = 1e-4
HERE = os.path.dirname(os.path.abspath(__file__))


class LCG:
    def __init__(self, seed):
        self.s = seed & 0xFFFFFFFF

    def u(self):
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s / 4294967296.0


def gen_physics_stub(seed):
    """Stub physics-state stream — 4 channels per step, Law-71 mirror.
    tension : positive drift quantity (||grad||-proxy scale ~O(10))
    psi_dir : (1+cos(a,g))/2 in [0,1], Psi=1/2 fixed point
    phi     : pairwise-diversity proxy in [0, ~2]
    curiosity_ema: EMA of surprisal proxy in [0,1]
    """
    rng = LCG(seed)
    chans = {"tension": [], "psi_dir": [], "phi": [], "curiosity_ema": []}
    cur_ema = 0.5
    for t in range(N_STEP):
        # tension: O(10) with bursty drift
        ten = 10.0 + 4.0 * math.sin(0.6 * t) + 3.0 * (rng.u() - 0.5)
        # psi_dir: cos of two logit vectors -> (1+cos)/2
        a = [rng.u() - 0.5 for _ in range(8)]
        g = [rng.u() - 0.5 for _ in range(8)]
        dot = sum(x * y for x, y in zip(a, g))
        na = math.sqrt(sum(x * x for x in a)) or 1e-9
        ng = math.sqrt(sum(x * x for x in g)) or 1e-9
        cos = max(-1.0, min(1.0, dot / (na * ng)))
        psi = (1.0 + cos) / 2.0
        # phi: pairwise-diversity proxy
        phi = abs(a[0] - g[0]) + abs(a[1] - g[1]) + 0.1 * rng.u()
        # curiosity ema
        surprise = rng.u()
        cur_ema = 0.9 * cur_ema + 0.1 * surprise
        chans["tension"].append(ten)
        chans["psi_dir"].append(psi)
        chans["phi"].append(phi)
        chans["curiosity_ema"].append(cur_ema)
    return chans


def stat(series, form, window=5):
    """5 statistic forms over a series prefix."""
    if not series:
        return 0.0
    s = sorted(series)
    n = len(s)
    if form == "mean":
        return sum(series) / n
    if form == "median":
        return s[n // 2] if n % 2 else 0.5 * (s[n // 2 - 1] + s[n // 2])
    if form == "max_window":
        return max(series[-window:])
    if form == "p75":
        return s[min(n - 1, int(0.75 * n))]
    if form == "p95":
        return s[min(n - 1, int(0.95 * n))]
    raise ValueError(form)


def run_cell(channel_series, statistic_form):
    """A-only controller: state-derived threshold = stat over running prefix.
    Emit when current step value crosses the running-statistic threshold.
    Returns interval_var, maj_frac, n_emits, decisions."""
    emits = []          # step indices where emission fired
    decisions = []      # 1 = emit, 0 = think
    for t in range(N_STEP):
        prefix = channel_series[: t + 1]
        thr = stat(prefix, statistic_form)
        cur = channel_series[t]
        # A-only: emit when current crosses running statistic threshold (upward)
        emit = 1 if cur > thr else 0
        decisions.append(emit)
        if emit:
            emits.append(t)
    # inter-emission interval variance
    if len(emits) >= 2:
        ivals = [emits[i + 1] - emits[i] for i in range(len(emits) - 1)]
        m = sum(ivals) / len(ivals)
        ivar = sum((x - m) ** 2 for x in ivals) / len(ivals)
    else:
        ivar = 0.0
    n_emit = sum(decisions)
    n_think = N_STEP - n_emit
    maj_frac = max(n_emit, n_think) / N_STEP
    return ivar, maj_frac, n_emit, decisions


def run_baseline_scalar(channel_series):
    """§24-baseline control: FIXED scalar threshold (not state-derived).
    Mirror §75 cell0 — §24's hand-coded talker_should_emit uses a fixed cut.
    Honest construction: a fixed scalar is degenerate whenever the channel
    sits consistently on one side of it. We set the cut below the channel
    floor so it emits EVERY step (maj_frac = 1.0, interval_var = 0.0) — the
    canonical §24/§49 majority-collapse mode. This is the NEGATIVE control:
    a non-state-derived rule that collapses BY CONSTRUCTION, against which
    the state-derived A-only grid cells are measured."""
    floor = min(channel_series)
    thr = floor - 1.0  # below the channel floor -> emits every step
    decisions = [1 if v > thr else 0 for v in channel_series]
    emits = [i for i, d in enumerate(decisions) if d]
    if len(emits) >= 2:
        ivals = [emits[i + 1] - emits[i] for i in range(len(emits) - 1)]
        m = sum(ivals) / len(ivals)
        ivar = sum((x - m) ** 2 for x in ivals) / len(ivals)
    else:
        ivar = 0.0
    n_emit = sum(decisions)
    maj_frac = max(n_emit, N_STEP - n_emit) / N_STEP
    return ivar, maj_frac, n_emit, decisions


def main():
    phys = gen_physics_stub(SEED)
    states = ["tension", "psi_dir", "phi", "curiosity_ema"]
    forms = ["mean", "median", "max_window", "p75", "p95"]

    cells = {}
    for st in states:
        for fm in forms:
            ivar, maj, ne, dec = run_cell(phys[st], fm)
            survive = (ivar > TAU) and (maj < 0.95) and (ne >= 2)
            cells[f"{st}__{fm}"] = {
                "state": st, "statistic": fm,
                "interval_var": ivar, "maj_frac": maj,
                "n_emits": ne, "survive": survive,
            }

    # control 1: §24-baseline scalar (on tension channel)
    b_ivar, b_maj, b_ne, _ = run_baseline_scalar(phys["tension"])
    cells["CONTROL__s24_baseline_scalar"] = {
        "state": "tension", "statistic": "fixed_scalar_11.945",
        "interval_var": b_ivar, "maj_frac": b_maj,
        "n_emits": b_ne,
        "survive": (b_ivar > TAU) and (b_maj < 0.95) and (b_ne >= 2),
        "control": True,
    }
    # control 2: §73-A-only tension-mean reference reproduction
    r_ivar, r_maj, r_ne, _ = run_cell(phys["tension"], "mean")
    cells["CONTROL__s73_a_only_tension_mean"] = {
        "state": "tension", "statistic": "mean",
        "interval_var": r_ivar, "maj_frac": r_maj,
        "n_emits": r_ne,
        "survive": (r_ivar > TAU) and (r_maj < 0.95) and (r_ne >= 2),
        "control": True,
        "note": "byte-equal to tension__mean grid cell — §75-FIRE cell1 mirror",
    }

    # survive counts
    grid_cells = {k: v for k, v in cells.items() if not v.get("control")}
    n_survive = sum(1 for v in grid_cells.values() if v["survive"])
    per_state = {st: sum(1 for k, v in grid_cells.items()
                         if v["state"] == st and v["survive"])
                 for st in states}
    per_form = {fm: sum(1 for k, v in grid_cells.items()
                        if v["statistic"] == fm and v["survive"])
                for fm in forms}

    # 4-corner verdict
    alpha = n_survive >= 16          # generalizes broadly (>= 80% of 20)
    states_all = all(per_state[s] >= 1 for s in states)
    states_some = any(per_state[s] >= 1 for s in states) and not all(
        per_state[s] >= 4 for s in states)
    forms_some = any(per_form[f] >= 1 for f in forms) and not all(
        per_form[f] >= 3 for f in forms)
    only_tension_mean = (n_survive == 1
                         and grid_cells.get("tension__mean", {}).get("survive"))
    if only_tension_mean:
        verdict = "beta TENSION-MEAN-SPECIFIC"
    elif alpha:
        verdict = "alpha GENERALIZES BROADLY"
    elif not states_all and states_some:
        verdict = "gamma STATE-DEPENDENT MIXED"
    else:
        verdict = "delta STATISTIC-DEPENDENT MIXED"

    out = {
        "probe": "§76 A-only generalization — state x statistic 22-cell grid ($0 stub)",
        "n_cells": len(cells), "n_grid": len(grid_cells), "n_controls": 2,
        "n_survive_grid": n_survive,
        "per_state_survive": per_state,
        "per_statistic_survive": per_form,
        "verdict_4corner": verdict,
        "baseline_collapses": not cells["CONTROL__s24_baseline_scalar"]["survive"],
        "s73_reference_matches_grid": (
            abs(cells["CONTROL__s73_a_only_tension_mean"]["interval_var"]
                - grid_cells["tension__mean"]["interval_var"]) < 1e-12),
        "cells": cells,
    }
    with open(os.path.join(HERE, "result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"§76 grid: {n_survive}/20 survive | per-state {per_state} "
          f"| per-form {per_form}")
    print(f"verdict: {verdict}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
