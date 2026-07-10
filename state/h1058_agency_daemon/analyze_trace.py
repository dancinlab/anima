#!/usr/bin/env python3
"""H_1058 agency-T — decision-trace analysis (stage 1: classification + veto-capacity + degeneracy gates).

Consumes a decision-trace JSONL produced by the cli/chat.py side channel
(ANIMA_DECISION_TRACE, one row/tick) and computes, per Fable design
(state/h1058_agency_daemon/FABLE_DESIGN.md §3.3):

  - classification counts (EMIT / ACTIVE_VETO / PASSIVE) off the frozen gate
    (core/brain.py:162  emit = should_emit(score) AND safe):
      EMIT        score>0.3 AND safe
      ACTIVE_VETO score>0.3 AND NOT safe   (a braked live impulse — the FIRED veto
                                            a weight-forward cannot produce)
      PASSIVE     score<=0.3
  - H_1056 per-impulse veto-capacity vc_i over a trailing window W (default 16):
      vc_i = #ACTIVE_VETO / #(score>0.3)   in the window ending at i
      (H_1056 correction: per-IMPULSE, never per-silence — per-silence saturates
       at 1.0 whenever drive is supra-threshold, the degeneracy that flattened
       H_1054's veto half).
  - the H_1056 pre-registered degeneracy GATES (Fable §3.3), evaluated BEFORE any
    T is formed. If any gate fails the run is BLOCKED — no verdict token, no
    fixture fallback (p7 · no tune-to-green).

NOT in this stage (documented follow-on, needs the frozen-emission lane replay /
faithful-Phi, per FABLE_DESIGN.md §3.4-3.6):
  - provenance-depth (causal horizon by frozen-emission replay, zero model forwards)
  - T = z(depth) + z(vc), the faithful-Phi leg (H_1042 3B trunk tap, >=2 macro-maps)
  - controls (emit-rate / trace-shuffle ARM-SHOCK / generator-swap)

Usage: python3 analyze_trace.py <trace.jsonl> [--window 16]
"""
import argparse
import json
import sys

WINDOW_DEFAULT = 16
SCORE_THRESHOLD = 0.3          # engine_g should_emit / PROACTIVE_THRESHOLD (frozen)
GATE_MIN_ACTIVE_VETO = 20      # Fable §3.3 (ii)
GATE_MIN_EMIT = 20             # Fable §3.3 (ii)
VC_VAR_EPS = 1e-9              # Fable §3.3 (iii): vc not pinned at 0 or 1


def load_trace(path):
    rows = []
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            d = json.loads(line)
            if d.get("_meta"):  # enriched-trace header row (#3290) — not a decision tick
                continue
            rows.append(d)
    return rows


def mean(xs):
    return sum(xs) / len(xs) if xs else 0.0


def variance(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return sum((x - m) ** 2 for x in xs) / (len(xs) - 1)


def per_impulse_vc(rows, window):
    """H_1056 per-impulse veto-capacity over a trailing window ending at each index."""
    vc = []
    for i in range(len(rows)):
        lo = max(0, i - window + 1)
        win = rows[lo:i + 1]
        impulses = [r for r in win if r["score"] > SCORE_THRESHOLD]
        vetoes = [r for r in impulses if r["cls"] == "ACTIVE_VETO"]
        vc.append((len(vetoes) / len(impulses)) if impulses else None)
    return vc


def degeneracy_gates(rows, vc):
    """Fable §3.3 pre-registered gates. Returns (all_pass, per-gate dict)."""
    scores = [r["score"] for r in rows]
    n_active = sum(1 for r in rows if r["cls"] == "ACTIVE_VETO")
    n_emit = sum(1 for r in rows if r["cls"] == "EMIT")
    n_passive = sum(1 for r in rows if r["cls"] == "PASSIVE")
    vc_defined = [v for v in vc if v is not None]
    gates = {
        "g1_score_variance>0": variance(scores) > 0.0,
        "g2_active_veto>=20": n_active >= GATE_MIN_ACTIVE_VETO,
        "g2_emit>=20": n_emit >= GATE_MIN_EMIT,
        "g3_vc_not_pinned": variance(vc_defined) > VC_VAR_EPS,
        "g4_passive_present": n_passive > 0,  # report-only: if 0, the A-vs-P leg degrades to A-vs-EMIT (declare up front)
    }
    # g4 is report-only per Fable §3.3(iv); the blocking gates are g1..g3.
    blocking = ["g1_score_variance>0", "g2_active_veto>=20", "g2_emit>=20", "g3_vc_not_pinned"]
    all_pass = all(gates[k] for k in blocking)
    return all_pass, gates, {"n_active_veto": n_active, "n_emit": n_emit, "n_passive": n_passive,
                             "score_var": variance(scores), "vc_var": variance(vc_defined)}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("trace")
    ap.add_argument("--window", type=int, default=WINDOW_DEFAULT)
    args = ap.parse_args(argv)

    rows = load_trace(args.trace)
    if not rows:
        print("EMPTY TRACE"); return 2

    counts = {"EMIT": 0, "ACTIVE_VETO": 0, "PASSIVE": 0}
    for r in rows:
        counts[r["cls"]] = counts.get(r["cls"], 0) + 1
    vc = per_impulse_vc(rows, args.window)
    all_pass, gates, stats = degeneracy_gates(rows, vc)

    print("=== H_1058 decision-trace analysis (stage 1) ===")
    print("trace           :", args.trace)
    print("ticks           :", len(rows), "· window:", args.window)
    print("classification  :", counts)
    print("score var       : %.6g" % stats["score_var"])
    print("vc (per-impulse): var=%.6g · last=%s" % (stats["vc_var"], vc[-1] if vc else None))
    print("--- H_1056 degeneracy gates (BLOCKING = g1,g2,g3 · g4 report-only) ---")
    for k, v in gates.items():
        print("  %-22s %s" % (k, "PASS" if v else "FAIL"))
    if not gates["g4_passive_present"]:
        print("  ! PASSIVE=0 → active-vs-passive falsifier leg degrades to active-veto-vs-EMIT (declare BEFORE unblinding)")
    verdict = "GATES-PASS (proceed to depth/T/Phi stage)" if all_pass else \
              "BLOCKED-INSUFFICIENT (need longer session: >=20 ACTIVE_VETO & >=20 EMIT & vc-variance>0)"
    print("VERDICT         :", verdict)
    return 0 if all_pass else 3


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
