#!/usr/bin/env python3
"""aggregate.py — collate H_6165 CAP×REG factorial cell JSONs → 5-bar tables + RUNG1_SIGNAL.

Reads results/cell_N*_REG*_s*.json, prints per-cell 5-bar rows, computes the CAP/REG
contrasts, and classifies RUNG1_SIGNAL ∈ {CAPACITY_OPEN, REGISTER_BOUND, INCONCLUSIVE}
per the PRE_REG decision rule (kill-switch for the 7B lane).
"""
import os, sys, json, glob, collections

RES = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")


def load_cells(res):
    cells = []
    for p in sorted(glob.glob(os.path.join(res, "cell_N*_REG*_s*.json"))):
        cells.append(json.load(open(p)))
    return cells


def main():
    cells = load_cells(RES)
    if not cells:
        print("NO CELLS in", RES); return
    base = cells[0]["base"]
    print("BASE  FALS_in=%s DIST_in=%s FALS_shuf=%s FALS_ho=%s" %
          (base["FALS_in"], base["DIST_in"], base["FALS_shuf"], base["FALS_ho"]))
    print()
    hdr = ("N  REG  seed | tr.FALS_in tr.DIST tr.FALS_shuf tr.FALS_ho | ab.FALS_in sh.FALS_in "
           "| B1 B2 B3 B4 B5 c4reg ctrl | GREEN")
    print(hdr); print("-" * len(hdr))
    # aggregate by (N,reg)
    agg = collections.defaultdict(list)
    for c in cells:
        cc = c["cell"]; t = c["trained"]; a = c["ablate"]; s = c.get("shuf_corp"); b = c["bars"]
        sh = s["FALS_in"] if s else "-"
        row = "%-2d %-4s %-4d | %9s %7s %12s %9s | %9s %9s | %2s %2s %2s %2s %2s %5s %4s | %s" % (
            cc["N"], cc["reg"], cc["seed"], t["FALS_in"], t["DIST_in"], t["FALS_shuf"], t["FALS_ho"],
            a["FALS_in"], sh,
            int(b["b1"]), int(b["b2"]), int(b["b3"]), int(b["b4"]), int(b["b5"]),
            int(b["ablate_regresses"]), int(b["ctrl_inert"]), b["green"])
        print(row)
        agg[(cc["N"], cc["reg"])].append(c)

    print("\n==== CELL MEANS (mean over seeds) ====")
    means = {}
    for (N, reg), cs in sorted(agg.items()):
        m = lambda k: round(sum(c["trained"][k] for c in cs) / len(cs), 3)
        ab = round(sum(c["ablate"]["FALS_in"] for c in cs) / len(cs), 3)
        b3collapse = any(c["bars"]["b3"] for c in cs)
        anyg = any(c["bars"]["green"] for c in cs)
        means[(N, reg)] = {"FALS_in": m("FALS_in"), "DIST_in": m("DIST_in"),
                           "FALS_shuf": m("FALS_shuf"), "FALS_ho": m("FALS_ho"),
                           "ablate_FALS_in": ab, "any_b3": b3collapse, "any_green": anyg,
                           "n": len(cs)}
        print("N=%d REG-%-3s (n=%d): FALS_in=%.3f DIST=%.3f FALS_shuf=%.3f FALS_ho=%.3f "
              "ablate_FALS_in=%.3f  any_B3=%s any_GREEN=%s" %
              (N, reg, len(cs), m("FALS_in"), m("DIST_in"), m("FALS_shuf"), m("FALS_ho"),
               ab, b3collapse, anyg))

    # ---- contrasts ----
    def mget(N, reg, k, d=0.0):
        return means.get((N, reg), {}).get(k, d)
    Ns = sorted({N for (N, r) in means})
    print("\n==== CONTRASTS ====")
    # CAP main-effect @REG-off: does FALS_in rise with N?
    off_by_N = [(N, mget(N, "off", "FALS_in")) for N in Ns]
    on_by_N = [(N, mget(N, "on", "FALS_in")) for N in Ns]
    print("CAP @REG-off  FALS_in by N:", off_by_N)
    print("CAP @REG-on   FALS_in by N:", on_by_N)
    reg_deltas = [(N, round(mget(N, "on", "FALS_in") - mget(N, "off", "FALS_in"), 3)) for N in Ns]
    print("REG main-effect (on-off) FALS_in by N:", reg_deltas)

    any_green = any(m["any_green"] for m in means.values())
    any_b3 = any(m["any_b3"] for m in means.values())
    on_form_lift = any(mget(N, "on", "FALS_in") >= 1 for N in Ns)
    off_lift = any(mget(N, "off", "FALS_in") >= 1 for N in Ns)
    # c4 ablate INERT on REG-on = lift survives gate->0 (register exposure, not attention)
    on_ablate_inert = any(mget(N, "on", "ablate_FALS_in") >= base["FALS_in"] + 1 for N in Ns)
    cap_open_off = mget(max(Ns), "off", "FALS_in") - mget(min(Ns), "off", "FALS_in")

    print("\n==== RUNG1 CLASSIFICATION ====")
    print("any_GREEN=%s any_B3_collapse=%s  REG-on form-lift(FALS_in>=1)=%s  "
          "REG-off lift=%s  REG-on c4-ablate-INERT=%s  CAP@off Δ(maxN-minN)=%.3f" %
          (any_green, any_b3, on_form_lift, off_lift, on_ablate_inert, cap_open_off))

    if any_green:
        signal = "CAPACITY_OPEN"
        why = "≥1 cell GREEN (all bars ∧ c4-collapse ∧ ctrl inert) → wall broke on the CAP/REG lever."
    elif any_b3 and (off_lift or cap_open_off >= 1):
        signal = "CAPACITY_OPEN"
        why = "B3 cross-shuffle COLLAPSE present with a CAP-driven (REG-off/depth) lift → earned binding, capacity opens it."
    elif on_form_lift and (not any_b3) and (not off_lift):
        signal = "REGISTER_BOUND"
        why = ("REG-on lifts FALS FORM (B1) but B3 NEVER collapses and c4-ablate leaves it "
               "(register exposure, not attention), while REG-off (capacity/depth alone) is INERT "
               "→ the H_1449 confound resolves to REGISTER, not a capacity ceiling scale would fix.")
    else:
        signal = "INCONCLUSIVE"
        why = ("neither a clean CAP-driven B3 collapse nor a clean REG-only form-lift; "
               "cells at/near floor (FALS_in≈0) — capacity-bound-at-floor, not separable this rung.")
    print("\nRUNG1_SIGNAL = %s" % signal)
    print("WHY: %s" % why)
    open(os.path.join(os.path.dirname(RES), "RUNG1_SIGNAL.txt"), "w").write(signal + "\n")
    json.dump({"signal": signal, "why": why, "means": {str(k): v for k, v in means.items()},
               "base": base, "reg_deltas": reg_deltas, "off_by_N": off_by_N, "on_by_N": on_by_N},
              open(os.path.join(os.path.dirname(RES), "results", "SUMMARY.json"), "w"),
              ensure_ascii=False, indent=2)
    return signal


if __name__ == "__main__":
    main()
