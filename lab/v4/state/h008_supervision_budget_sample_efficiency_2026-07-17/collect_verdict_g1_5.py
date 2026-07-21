#!/usr/bin/env python3
"""H_008 G-1.5 band-existence verdict — the FROZEN truth conditions (lab-full design 2026-07-17), $0.

Renders PROCEED-TO-FREEZE / K1 / K1b / INCOMPLETE from g1_5_result.json. Encodes the freeze draft on the
H_008 card exactly (Fable adjudication, code-verified):

  k* = 96, factor-2 neighbor 48. C-dup reads of record = the RE-INSTRUMENTED phase-b runs
  (replacement-not-selection: phase-a k=96 s0 is provenance only, never picked over the phase-b read).

  Truth conditions (ALL, both seeds, on instrumented reads):
    F2 validity   : in-sample d_acc(B(k)) ≥ 0.95 every read (else the read is INVALID → rerun-once, blind).
    plateau       : held-out f2 max−min ≤ 0.05 over {60,80,100}% (guards the endpoint-only spike trap).
    four-point    : f2 ∈ [0.60,0.80] at BOTH k∈{48,96} and BOTH seeds (k* + its factor-2 neighbor).
    stability     : |f2(96,s0) − f2(96,s1)| ≤ 0.10 (cross-seed, priced from H_003's 0.1614).
    phase-c       : C-scaf@96 ≤ 0.80 AND C-shuf@96 ≤ 0.80, both seeds (else K1b: generic-aux headroom gone).

  Verdict:
    PROCEED-TO-FREEZE — all truth conditions hold (instantiate per-seed E, freeze).
    K1   — any band/plateau/validity/stability condition fails (likely k=48 s1 < 0.60). No midpoint, no 3rd seed.
    K1b  — band holds but a placebo (C-scaf/C-shuf) saturates > 0.80.
    INCOMPLETE — required reads (phase-b/c) not all present yet.
"""
from __future__ import annotations

import json
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
_R = os.path.join(_HERE, "g1_5_result.json")
BAND = (0.60, 0.80)
STAB = 0.10           # cross-seed |Δ| at k*
PLATEAU = 0.05
VALID = 0.95
KSTAR, NEIGH = 96, 48


def _read(jobs, arm, k, seed, prefer_phase_b=True):
    """C-dup reads of record prefer the RE-INSTRUMENTED entry (has 'valid'/'plateau_ok' fields =
    phase-b/c instrumented run) over a bare phase-a entry (replacement-not-selection)."""
    cands = [r for r in jobs if r["arm"] == arm and r["k"] == k and r["seed"] == seed]
    if not cands:
        return None
    inst = [r for r in cands if "valid" in r]
    return (inst[-1] if inst else cands[-1]) if not (prefer_phase_b and inst) else inst[-1]


def main() -> int:
    if not os.path.exists(_R):
        print(f"NO RESULT YET — {_R} missing.")
        return 2
    jobs = json.load(open(_R))["jobs"]

    fails, notes = [], []
    # --- four-point clause + validity + plateau on C-dup @ {48,96} × {0,1} (instrumented reads of record)
    cdup = {}
    for k in (NEIGH, KSTAR):
        for s in (0, 1):
            r = _read(jobs, "C-dup", k, s)
            cdup[(k, s)] = r
            if r is None:
                notes.append(f"C-dup k={k} s={s} MISSING"); continue
            f2 = r["f2_dacc"]
            if not (BAND[0] <= f2 <= BAND[1]):
                fails.append(f"band: C-dup k={k} s={s} f2={f2} ∉ [{BAND[0]},{BAND[1]}]")
            if r.get("valid") is False or (r.get("insample_dacc") is not None and r["insample_dacc"] < VALID):
                fails.append(f"validity: C-dup k={k} s={s} in-sample<{VALID}")
            if r.get("plateau_ok") is False:
                fails.append(f"plateau: C-dup k={k} s={s} f2 max−min > {PLATEAU}")

    have_all_cdup = all(cdup[(k, s)] is not None for k in (NEIGH, KSTAR) for s in (0, 1))
    # --- cross-seed stability at k*
    if cdup[(KSTAR, 0)] and cdup[(KSTAR, 1)]:
        d = abs(cdup[(KSTAR, 0)]["f2_dacc"] - cdup[(KSTAR, 1)]["f2_dacc"])
        if d > STAB:
            fails.append(f"stability: |Δf2@{KSTAR}| = {round(d,4)} > {STAB}")
        notes.append(f"cross-seed |Δf2@{KSTAR}| = {round(d,4)}")

    # --- phase-c pricing (C-scaf / C-shuf @ k*, both seeds) — only evaluated if the band survives
    k1b = []
    placebo_present = all(_read(jobs, arm, KSTAR, s) for arm in ("C-scaf", "C-shuf") for s in (0, 1))
    if placebo_present:
        for arm in ("C-scaf", "C-shuf"):
            for s in (0, 1):
                r = _read(jobs, arm, KSTAR, s)
                if r["f2_dacc"] > 0.80:
                    k1b.append(f"{arm} k={KSTAR} s={s} f2={r['f2_dacc']} > 0.80")

    # --- verdict
    if not have_all_cdup:
        verdict = f"INCOMPLETE — phase-b C-dup reads @{{48,96}}×{{0,1}} not all present ({notes})."
    elif fails:
        verdict = ("K1 (CLOSE) — band/stability/plateau/validity condition(s) failed: " + " · ".join(fails)
                   + ". No midpoint, no third seed, no non-validity rerun. Campaign stays CONCLUDED on mech-1.")
    elif not placebo_present:
        verdict = "BAND HOLDS at k*=96 (four-point + stability + validity + plateau ✓) — run phase c (C-scaf/C-shuf @96) to price the placebo before freeze."
    elif k1b:
        verdict = "K1b (CLOSE) — band holds but placebo saturates: " + " · ".join(k1b) + " (generic-aux headroom gone)."
    else:
        verdict = ("PROCEED-TO-FREEZE — all truth conditions hold (four-point band, cross-seed stability, "
                   "plateau, F2 validity, C-scaf/C-shuf ≤ 0.80 both seeds). Instantiate per-seed E[C-dup@96] "
                   "and pre_register_frozen:true, then run the A-tug mechanism arm for F1.")

    print("=" * 78 + "\nH_008 G-1.5 freeze-truth verdict\n" + "=" * 78)
    for k in (NEIGH, KSTAR):
        row = " ".join(f"s{s}={cdup[(k,s)]['f2_dacc'] if cdup[(k,s)] else '?'}" for s in (0, 1))
        print(f"  C-dup k={k}: {row}")
    for n in notes:
        print("  ·", n)
    print("\nVERDICT:", verdict)
    json.dump({"verdict": verdict, "fails": fails, "k1b": k1b,
               "cdup": {f"{k}.{s}": (cdup[(k,s)]["f2_dacc"] if cdup[(k,s)] else None)
                        for k in (NEIGH, KSTAR) for s in (0, 1)}},
              open(os.path.join(_HERE, "verdict_g1_5.json"), "w"), indent=2, ensure_ascii=False)
    print("wrote verdict_g1_5.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
