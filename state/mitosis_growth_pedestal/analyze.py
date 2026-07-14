#!/usr/bin/env python3
"""H_9311 GROWTH-PAYS -- PEDESTAL + C1 readout. Bars are FROZEN in PREREG.md; this only reads them.

All contrasts are PAIRED (seed-paired across arms; test-point-paired within a seed).
NO max(controls) order statistic anywhere (probe-defect-census-max-control-bias).
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
ARMS = ["E", "C1", "P0X", "P0Y", "P1"]
# --- frozen bars (PREREG.md §4) ---
CALIB_10, CALIB_320, CALIB_TOL = 2.72391, 2.46370, 0.001
LIVE_BAR = -0.50            # P1 must find the spike-in axis
KILL_PED = -0.10            # pedestal gain >= this magnitude => 🟢 RETRACT
TOST_EQ = 0.02              # equivalence margin
DISSOC_DEG, DISSOC_EXP = 0.02, -0.05
EARNED_BAR = -0.05

T95 = {1: 6.314, 2: 2.920, 3: 2.353, 4: 2.132, 5: 2.015, 6: 1.943, 7: 1.895, 8: 1.860, 9: 1.833}
T975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262}


def mean(v):
    return sum(v) / float(len(v))


def sd(v):
    if len(v) < 2:
        return float("nan")
    m = mean(v)
    return math.sqrt(sum((x - m) ** 2 for x in v) / (len(v) - 1))


def ttest1(v):
    """one-sample t on paired differences -> (mean, sd, sem, t, df, ci95)"""
    n = len(v)
    m, s = mean(v), sd(v)
    sem = s / math.sqrt(n)
    df = n - 1
    t = m / sem if sem > 0 else float("nan")
    h = T975.get(df, 1.96) * sem
    return {"mean": m, "sd": s, "sem": sem, "t": t, "df": df, "ci95": [m - h, m + h]}


def tost(v, eq):
    """TOST equivalence vs +-eq (one-sided alpha .05). PASS only if the 90% CI is inside +-eq."""
    r = ttest1(v)
    h = T95.get(r["df"], 1.645) * r["sem"]
    lo, hi = r["mean"] - h, r["mean"] + h
    return {"ci90": [lo, hi], "equivalent": bool(lo > -eq and hi < eq), "eq_margin": eq}


def load(arm, s, g):
    p = os.path.join(RES, f"{arm}_s{s}_g{g}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def main():
    seeds = sorted({int(f.split("_s")[1].split("_")[0]) for f in os.listdir(RES)
                    if f.startswith("E_s") and f.endswith("_g320.json")})
    ce = {a: {} for a in ARMS}          # ce[arm][seed] = (ce10, ce320)
    pn = {a: {} for a in ARMS}          # per-point nats, for the within-seed paired-t
    cells = {a: {} for a in ARMS}
    missing = []
    for s in seeds:
        for a in ARMS:
            src = "E" if a == "C1" else a
            d10, d320 = load(src, s, 10), load(src, s, 320)
            if not d10 or not d320:
                missing.append((a, s)); continue
            k = "c1_ce" if a == "C1" else "ce"
            kn = "c1_nats" if a == "C1" else "nats"
            kc = "c1_cells" if a == "C1" else "cells"
            ce[a][s] = (d10[k], d320[k])
            pn[a][s] = (d10[kn], d320[kn], d10["sum_nb"])
            cells[a][s] = (d10[kc], d320[kc])
    if missing:
        print(f"[WARN] missing runs: {missing}")

    out = {"seeds": seeds, "n_seeds": len(seeds), "frozen_bars": {
        "CALIB": [CALIB_10, CALIB_320, CALIB_TOL], "LIVE": LIVE_BAR, "KILL_PED": KILL_PED,
        "TOST_EQ": TOST_EQ, "DISSOC": [DISSOC_DEG, DISSOC_EXP], "EARNED": EARNED_BAR}}

    # ---- G-CALIB (blocking) -- seed0's E must reproduce H_9311 byte-for-byte
    c10, c320 = ce["E"][0]
    calib = abs(c10 - CALIB_10) <= CALIB_TOL and abs(c320 - CALIB_320) <= CALIB_TOL
    out["G_CALIB"] = {"ce10": c10, "ce320": c320, "pass": bool(calib)}
    print(f"G-CALIB   E(s0) 10={c10:.5f} (anchor {CALIB_10})  320={c320:.5f} (anchor {CALIB_320})"
          f"  -> {'PASS' if calib else 'FAIL'}")
    if not calib:
        out["verdict"] = "INVALID - CALIB fail; no bar read"
        json.dump(out, open(os.path.join(RES, "SUMMARY.json"), "w"), indent=2)
        print("\nVERDICT: INVALID (CALIB)"); return

    # ---- per-arm growth delta  D = CE(320) - CE(10),  seed-paired
    D = {a: [ce[a][s][1] - ce[a][s][0] for s in seeds if s in ce[a]] for a in ARMS}
    print(f"\n{'arm':5s} {'CE(10)':>9s} {'CE(320)':>9s} {'D=320-10':>10s} {'sd':>8s} {'sem':>8s} "
          f"{'t':>7s}  95% CI")
    for a in ARMS:
        r = ttest1(D[a])
        m10 = mean([ce[a][s][0] for s in seeds if s in ce[a]])
        m320 = mean([ce[a][s][1] for s in seeds if s in ce[a]])
        out[f"D_{a}"] = dict(r, ce10=m10, ce320=m320,
                             cells320=[cells[a][s][1] for s in seeds if s in cells[a]])
        print(f"{a:5s} {m10:9.5f} {m320:9.5f} {r['mean']:+10.5f} {r['sd']:8.5f} {r['sem']:8.5f} "
              f"{r['t']:7.2f}  [{r['ci95'][0]:+.5f}, {r['ci95'][1]:+.5f}]")

    # ---- observed sigma_path vs the PREREG assumption (0.03) -> realised MDE
    sig = sd(D["E"])
    n = len(seeds)
    sem = sig / math.sqrt(n)
    mde = (T975.get(n - 1, 1.96) + 0.9) * sem
    out["power"] = {"sigma_path_obs_E": sig, "n_seeds": n, "sem": sem, "mde80": mde,
                    "tost_feasible": bool(T95.get(n - 1, 1.645) * sem < TOST_EQ)}
    print(f"\n[POWER] observed sigma_path(E)={sig:.5f}  n={n}  SEM={sem:.5f}  "
          f"MDE(80%)~{mde:.5f}  TOST(+-{TOST_EQ}) feasible={out['power']['tost_feasible']}")

    # ---- G-LIVE (blocking positive control)
    live = ttest1(D["P1"])
    live_pass = live["mean"] <= LIVE_BAR
    out["G_LIVE"] = dict(live, bar=LIVE_BAR, pass_=bool(live_pass))
    print(f"\nG-LIVE    P1 spike-in D={live['mean']:+.5f} (bar <= {LIVE_BAR}) -> "
          f"{'PASS' if live_pass else 'FAIL'}")
    if not live_pass:
        out["verdict"] = "INVALID - positive control (P1 spike-in) not found; no bar read"
        json.dump(out, open(os.path.join(RES, "SUMMARY.json"), "w"), indent=2)
        print("\nVERDICT: INVALID (G-LIVE)"); return

    # ---- G-PED-Y (true-zero pedestal)
    py = ttest1(D["P0Y"]); pyt = tost(D["P0Y"], TOST_EQ)
    out["G_PED_Y"] = dict(py, tost=pyt, kill=bool(py["mean"] <= KILL_PED))
    print(f"G-PED-Y   TRUE-0 pedestal D={py['mean']:+.5f}  CI95 [{py['ci95'][0]:+.5f},{py['ci95'][1]:+.5f}]"
          f"  TOST(+-{TOST_EQ}) equivalent={pyt['equivalent']}  KILL(<= {KILL_PED})={py['mean'] <= KILL_PED}")

    # ---- G-PED-X (split-choice pedestal)
    px = ttest1(D["P0X"])
    adaptive = [D["E"][i] - D["P0X"][i] for i in range(len(D["E"]))]   # seed-PAIRED
    ad = ttest1(adaptive)
    out["G_PED_X"] = dict(px, adaptive_earned=ad)
    print(f"G-PED-X   split-choice pedestal D={px['mean']:+.5f}  CI95 [{px['ci95'][0]:+.5f},{px['ci95'][1]:+.5f}]"
          f"\n          adaptive split-choice earned (D_E - D_P0X) = {ad['mean']:+.5f} "
          f"CI95 [{ad['ci95'][0]:+.5f},{ad['ci95'][1]:+.5f}]  t={ad['t']:.2f}")

    # ---- G-DISSOC (C1 = same partition, flat head)
    c1 = ttest1(D["C1"])
    dissoc = c1["mean"] > DISSOC_DEG and mean(D["E"]) < DISSOC_EXP
    solo = c1["mean"] < DISSOC_EXP
    out["G_DISSOC"] = dict(c1, double_dissociation=bool(dissoc), growth_solo_lever=bool(solo))
    print(f"G-DISSOC  C1 (E's partition, flat head) D={c1['mean']:+.5f} "
          f"CI95 [{c1['ci95'][0]:+.5f},{c1['ci95'][1]:+.5f}]  "
          f"double-dissociation={dissoc}  growth-solo-lever={solo}")

    # ---- HEADLINE: EARNED = D_E - D_P0Y (seed-paired, artifact-subtracted)
    earned = [D["E"][i] - D["P0Y"][i] for i in range(len(D["E"]))]
    er = ttest1(earned)
    sig05 = abs(er["t"]) > T975.get(er["df"], 1.96)
    survives = er["mean"] <= EARNED_BAR and sig05 and er["mean"] < 0
    out["EARNED"] = dict(er, bar=EARNED_BAR, p_lt_05=bool(sig05), growth_pays_survives=bool(survives))
    print(f"\nEARNED    D_E - D_P0Y = {er['mean']:+.5f}  CI95 [{er['ci95'][0]:+.5f},{er['ci95'][1]:+.5f}]"
          f"  t={er['t']:.2f} (df={er['df']})  bar <= {EARNED_BAR}, p<.05 -> "
          f"GROWTH-PAYS {'SURVIVES' if survives else 'RETRACT'}")

    # ---- within-seed test-point paired-t (secondary precision, seed0)
    a10, a320, snb = pn["E"][0]
    dd = [a320[i] - a10[i] for i in range(len(a10))]
    nb_mean = snb / float(len(a10))
    m, s = mean(dd), sd(dd)
    out["seed0_pointpaired"] = {"ce_diff": m / nb_mean, "sem": (s / math.sqrt(len(dd))) / nb_mean,
                               "t": m / (s / math.sqrt(len(dd)))}
    print(f"[2nd] seed0 test-point paired-t on E(320)-E(10): "
          f"dCE={out['seed0_pointpaired']['ce_diff']:+.5f} "
          f"+-{out['seed0_pointpaired']['sem']:.5f}  t={out['seed0_pointpaired']['t']:.2f}")

    json.dump(out, open(os.path.join(RES, "SUMMARY.json"), "w"), indent=2)
    print(f"\n[written] {os.path.join(RES, 'SUMMARY.json')}")


if __name__ == "__main__":
    main()
