#!/usr/bin/env python3
"""H_1058 · H_9269 Φ-leg redesign — T1 POSITIVE CONTROL (FROZEN acceptance, pre-registered).

Proves the redesigned phi_leg.py instrument RESOLVES real Φ variance when the model-input bytes
ACTUALLY vary — i.e. that the old decision-invariance was a REGIME property (constant consumed
bytes), NOT an instrument defect. This is the real-.clm leg the synthetic unit test cannot cover.

  ⚠️ POOL-GATED: needs the real e1_slw_303m .clm trunk forward (mini-OOM). Runnable-on-pool only;
     it is NOT run at build time (labelled real-clm-T1-미검증 · pool follow-on).

FROZEN draw (seed 20260712) — deterministic 64-byte windows from the 4-cell register corpus:
  · 16 calibration windows  → phi_leg.calibrate_units (signal-blind; EXCLUDED from scoring)
  · 32 scored NATURAL windows
  · 4 structured contrasts   → 2 constant-byte, 2 period-2

FROZEN acceptance (per macro-map · NOT relaxable after seeing data · p7):
  PASS iff  sd(Φ over 32 natural) >= 0.005
        AND >=8/32 distinct Φ @ 4sf
        AND {natural, period-2, constant} are NOT all Φ-equal (@4sf class means).

Usage (pool): PYTHONPATH=core python3 t1_phi_variance_control.py \
                 --clm <e1_slw_303m.clm> --corpus <dir|f1,f2,f3,f4> [--out t1_result.json]
"""
import argparse
import json
import os
import statistics
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import phi_leg  # same dir — reuses the FROZEN instrument (fwd_trunk_preMoE/calibrate_units/faithful_phi_frozen)

T = phi_leg.T_WIN                 # 64 (frozen)
DRAW_SEED = 20260712             # frozen T1 draw seed
N_CALIB = 16
N_NATURAL = 32
CONST_BYTES = (0x41, 0x20)       # 'A', ' ' — 2 constant-byte contrasts
PERIOD2 = ((0x41, 0x42), (0x30, 0x31))   # 'ABAB…', '0101…' — 2 period-2 contrasts
SD_BAR = 0.005
DISTINCT_BAR = 8


def _load_cells(corpus):
    """Return a list of byte-strings, one per register cell (files or a dir of files)."""
    paths = []
    if os.path.isdir(corpus):
        for fn in sorted(os.listdir(corpus)):
            p = os.path.join(corpus, fn)
            if os.path.isfile(p):
                paths.append(p)
    else:
        paths = [p for p in corpus.split(",") if p]
    cells = []
    for p in paths:
        with open(p, "rb") as fh:
            b = fh.read()
        if len(b) >= T:
            cells.append(b)
    if not cells:
        raise SystemExit("T1: no corpus cell >= %d bytes found in %r" % (T, corpus))
    return cells


def _draw_windows(cells, n, rng, used):
    """Draw `n` distinct 64-byte windows round-robin across cells (offsets tracked in `used`)."""
    wins = []
    ci = 0
    guard = 0
    while len(wins) < n and guard < n * 50:
        guard += 1
        cell = cells[ci % len(cells)]
        ci += 1
        off = rng.randrange(0, len(cell) - T + 1)
        key = (id(cell), off)
        if key in used:
            continue
        used.add(key)
        wins.append(bytes(cell[off:off + T]))
    if len(wins) < n:
        raise SystemExit("T1: could not draw %d distinct windows (corpus too small)" % n)
    return wins


def _phi_window(W, win_bytes, frozen_map):
    tok = np.frombuffer(win_bytes, dtype=np.uint8, count=T).astype(float)
    H = phi_leg.fwd_trunk_preMoE(W, tok, T)
    return phi_leg.faithful_phi_frozen(H, frozen_map)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--clm", required=True)
    ap.add_argument("--corpus", required=True, help="dir of 4-cell files, or comma-list f1,f2,f3,f4")
    ap.add_argument("--out", default=None)
    args = ap.parse_args(argv)

    print("=== H_1058 · H_9269 Φ-leg T1 positive control (FROZEN) · T=%d seed=%d ===" % (T, DRAW_SEED), flush=True)
    print("STEP 0 — RE-PROVE stdlib IIT-4.0 mirror == stdlib at n=%d:" % phi_leg.N_UNITS, flush=True)
    if not bool(phi_leg.prove_mirrors_at_n(phi_leg.N_UNITS)):
        print("ABORT — mirror==stdlib proof FAILED."); return 1

    W = phi_leg.dec.clm_load_weights(args.clm)
    assert W.get("ok"), "clm_load_weights failed / not decodable"
    print("   loaded d=%s V=%s L=%s K=%s" % (W["d"], W["V"], W["L"], W["K"]), flush=True)

    import random
    rng = random.Random(DRAW_SEED)
    cells = _load_cells(args.corpus)
    used = set()
    calib_wins = _draw_windows(cells, N_CALIB, rng, used)
    nat_wins = _draw_windows(cells, N_NATURAL, rng, used)
    const_wins = [bytes([c]) * T for c in CONST_BYTES]
    p2_wins = [bytes(list(ab) * (T // 2))[:T] for ab in PERIOD2]

    # FROZEN calibration (signal-blind) on the 16 calibration windows
    calib_H = [phi_leg.fwd_trunk_preMoE(W, np.frombuffer(w, dtype=np.uint8, count=T).astype(float), T)
               for w in calib_wins]
    frozen = phi_leg.calibrate_units(calib_H)

    result = {"clm": args.clm, "T": T, "seed": DRAW_SEED, "maps": {}}
    all_pass = True
    for mp in phi_leg.MACRO_MAPS:
        fm = frozen[mp]
        nat = [_phi_window(W, w, fm) for w in nat_wins]
        const = [_phi_window(W, w, fm) for w in const_wins]
        p2 = [_phi_window(W, w, fm) for w in p2_wins]
        sd = statistics.pstdev(nat)
        n_distinct = len(set(round(p, 4) for p in nat))
        cls_means = {round(statistics.fmean(nat), 4),
                     round(statistics.fmean(p2), 4),
                     round(statistics.fmean(const), 4)}
        not_all_equal = len(cls_means) > 1
        ok = (sd >= SD_BAR) and (n_distinct >= DISTINCT_BAR) and not_all_equal
        all_pass = all_pass and ok
        result["maps"][mp] = {
            "sd_natural": sd, "n_distinct": n_distinct, "not_all_equal": not_all_equal,
            "mean_natural": statistics.fmean(nat), "mean_period2": statistics.fmean(p2),
            "mean_constant": statistics.fmean(const),
            "units": list(map(int, fm["idx"])), "pass": bool(ok),
            "phi_natural": nat, "phi_period2": p2, "phi_constant": const,
        }
        print("  [%s] sd=%.5f (bar %.3f) distinct=%d/%d (bar %d) classes-differ=%s -> %s"
              % (mp, sd, SD_BAR, n_distinct, N_NATURAL, DISTINCT_BAR, not_all_equal,
                 "PASS" if ok else "FAIL"), flush=True)

    result["T1_PASS"] = bool(all_pass)
    print("T1 POSITIVE CONTROL: %s" % ("PASS (instrument resolves real Φ variance)"
                                       if all_pass else "FAIL (see per-map bars)"))
    if args.out:
        with open(args.out, "w") as fh:
            json.dump(result, fh, indent=1)
        print("wrote:", args.out)
    return 0 if all_pass else 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
