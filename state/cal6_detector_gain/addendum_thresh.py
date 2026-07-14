#!/usr/bin/env python3
"""CAL-6 ADDENDUM (POST-HOC · clearly labelled · does NOT change the pre-registered verdict).

Purpose: bound the TRANSFER scope of the dacc_AND finding.  dacc_AND in F13 = 1[mA>0 AND mB>0],
i.e. a bounded AND over one live branch and one DEAD branch -- its catastrophic gain could be an
artifact of the dead conjunct rather than of thresholding per se.  The ledger-wide detector class
of interest (held-out D-acc in NBIND-G / H_9286 / H_9289) is a *single-margin thresholded
accuracy*, not an AND.  So we measure the pure thresholding loss on the SAME data:

    acc_B_THRESH = 1[m_B_conj > 0]        # thresholded readout of the very margin m_B_conj

gain(acc_B_THRESH) vs gain(m_B_conj)=1.000 isolates the censoring/thresholding loss (defect D9),
with the AND confound removed.  Same spike-in ladder, same pedestal, same statistics.
"""
import json, os
import numpy as np
from scipy import stats
import cal6 as C

ROOT = os.path.dirname(os.path.abspath(__file__))
out = {"NOTE": "POST-HOC ADDENDUM -- not part of the pre-registered CAL-6 verdict. "
               "Added to bound the transfer scope of the dacc_AND result (AND-confound removal).",
       "detector": "acc_B_THRESH = 1[m_B_conj > 0]  (pure thresholded readout of the headline margin)",
       "datasets": []}

C.DETECTORS["acc_B_THRESH"] = lambda mA, mB, sA, sB: (mB > 0).astype(float)

for tag, path, note in C.DATASETS:
    atoms, n = C.load(path)
    ae, ac = atoms[C.EXP], atoms[C.CTL]
    sigma = float((ae["m_B_conj"] - ac["m_B_conj"]).std(ddof=1))
    rng = np.random.default_rng(C.RANDSIGN_SEED)
    eps = np.ones(n); eps[: n // 2] = -1.0; rng.shuffle(eps)
    rec = {"dataset": tag, "n": n, "sigma_nats": sigma, "gains": {}}
    for nm in ("m_B_conj", "acc_B_THRESH"):
        d, y, sd_D, base = C.ladder_for(ae, ac, nm, "PROX", sigma, eps)
        gn, gs = C.gain_from_rungs(d, y, sigma, sd_D)
        boots = []
        for _ in range(5000):
            bi = rng.integers(0, n, n)
            db, yb, sdb, _ = C.ladder_for(ae, ac, nm, "PROX", sigma, eps, idx=bi)
            boots.append(C.gain_from_rungs(db, yb, sigma, sdb)[1])
        rec["gains"][nm] = {
            "gain_nat": gn, "gain_std": gs, "sd_D": sd_D,
            "gain_std_ci95": [float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
            "rungs": [{"k": k, "delta": float(dd), "delta_hat": float(yy)}
                      for k, dd, yy in zip(C.LADDER, d, y)],
        }
    g_thr = rec["gains"]["acc_B_THRESH"]["gain_std"]
    rec["n_inflation_vs_continuous_margin"] = float(1.0 / (g_thr ** 2)) if g_thr > 0 else None
    out["datasets"].append(rec)
    print("%-13s n=%3d | gain_std m_B_conj=%.3f  acc_B_THRESH=%.3f CI95[%.3f,%.3f]  "
          "=> same true effect needs %.1fx the n" %
          (tag, n, rec["gains"]["m_B_conj"]["gain_std"], g_thr,
           rec["gains"]["acc_B_THRESH"]["gain_std_ci95"][0],
           rec["gains"]["acc_B_THRESH"]["gain_std_ci95"][1],
           rec["n_inflation_vs_continuous_margin"]))

json.dump(out, open(os.path.join(ROOT, "addendum_thresh_result.json"), "w"), indent=1)
