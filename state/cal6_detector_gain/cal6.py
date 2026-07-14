#!/usr/bin/env python3
"""CAL-6 — detector gain calibration by SPIKE-IN (pre-registered in PREREG.md).

$0 re-analysis of the frozen per-item x per-arm decode outputs of the mito organelle
lane F13 family (H_9285, 3 disjoint seeds, engine-native 303M py303_full.clm on aiden,
PARITY max|delta| = 0.0).  NO retraining, NO new decode.

Question (defect D6): if a census detector's GAIN is < 1 it compresses a true effect
into "ns" and manufactures false KILLs.  Pedestal checks the INTERCEPT (bias at 0);
nobody ever checked the SLOPE.

Method: inject a known Delta_true at the ANALYSIS-INPUT level (logP of the content
token in the AB context) into the EXP arm only, then push the spiked inputs through
each detector + the paired statistics and regress recovered Delta_hat on injected delta.
"""
import json, hashlib, os, sys
import numpy as np
from scipy import stats

ROOT = os.path.dirname(os.path.abspath(__file__))
F13 = os.path.abspath(os.path.join(ROOT, "..", "mito_organelle_lane", "F13_303m_reach_closure"))

DATASETS = [
    ("run1_KILL", os.path.join(F13, "result.json"),
     "original F13 run - licensed the organelle-lane KILL - headline m_conj = min(mA,mB)"),
    ("run2_INVALID", os.path.join(F13, "refire", "refire_result.json"),
     "refire - headline pre-registered as m_B_conj - verdict INVALID (V2 gate)"),
    ("run3_CLOSED", os.path.join(F13, "cement", "cement_result.json"),
     "cement - TOST equivalence on m_B_conj - licensed EQUIVALENT_CLOSED (the live verdict)"),
]

LADDER = [0.0, 0.5, 1.0, 2.0]          # k, delta = k * sigma          (pre-registered)
PASS_LO, PASS_HI = 0.8, 1.25           # gain PASS band                (pre-registered)
LOG_MARGIN = np.log(1.25)              # log-gain TOST margin +-0.2231 (pre-registered)
RANDSIGN_SEED = 20260714               # pedestal P1 seed              (pre-registered)
N_BOOT = 10000
EXP, CTL = "EXP", "c0"                 # control fixed to c0; never spiked

# ---------------------------------------------------------------- detectors
# atoms stored per item x arm: m_A_conj, m_B_conj, s_A, s_B   (all nats = logP diffs)
DETECTORS = {
    "m_A_conj": lambda mA, mB, sA, sB: mA,
    "m_B_conj": lambda mA, mB, sA, sB: mB,                       # run2/run3 headline (linear)
    "m_conj_MIN": lambda mA, mB, sA, sB: np.minimum(mA, mB),     # run1 headline (order statistic)
    "m_mean": lambda mA, mB, sA, sB: 0.5 * (mA + mB),
    "dacc_AND": lambda mA, mB, sA, sB: ((mA > 0) & (mB > 0)).astype(float),  # bounded binary AND
    "ceiling_MIN": lambda mA, mB, sA, sB: np.minimum(sA, sB),    # order statistic
}
LINEAR_NATS = ["m_A_conj", "m_B_conj", "m_mean"]  # exact-arithmetic detectors (harness checks)


def load(path):
    d = json.load(open(path))
    items = [i for i in d["items"] if i.get("set", "main") == "main"]
    out = {}
    for arm in (EXP, CTL):
        out[arm] = {k: np.array([i["arm"][arm][k] for i in items], float)
                    for k in ("m_A_conj", "m_B_conj", "s_A", "s_B")}
    return out, len(items)


def spike(atoms, delta, model, eps=None):
    """Inject delta nats at the analysis-input level into the EXP arm only."""
    a = {k: v.copy() for k, v in atoms.items()}
    if model == "PROX":            # logP(b|AB) += delta  =>  m_B_conj += delta
        a["m_B_conj"] = a["m_B_conj"] + delta
    elif model == "SYM":           # logP(a|AB) and logP(b|AB) += delta
        a["m_A_conj"] = a["m_A_conj"] + delta
        a["m_B_conj"] = a["m_B_conj"] + delta
    elif model == "RANDSIGN":      # pedestal: balanced +-delta  => TRUE mean effect == 0
        a["m_B_conj"] = a["m_B_conj"] + eps * delta
    else:
        raise ValueError(model)
    return a


def det(atoms, name):
    f = DETECTORS[name]
    return f(atoms["m_A_conj"], atoms["m_B_conj"], atoms["s_A"], atoms["s_B"])


def paired_stats(x):
    n = len(x)
    m, sd = float(x.mean()), float(x.std(ddof=1))
    sem = sd / np.sqrt(n)
    t = m / sem if sem > 0 else 0.0
    p = float(2 * stats.t.sf(abs(t), n - 1)) if sem > 0 else 1.0
    return {"mean": m, "sd": sd, "sem": float(sem), "t": float(t), "p": p, "n": n}


def tost_zero(x, margin):
    """TOST of mean(x) against equivalence to 0 with the given margin (90% CI inside)."""
    n = len(x)
    m, sem = float(x.mean()), float(x.std(ddof=1) / np.sqrt(n))
    if sem == 0:
        return {"mean": m, "ci90": [m, m], "margin": margin,
                "equivalent": bool(abs(m) < margin), "p_tost": 0.0}
    tc = stats.t.ppf(0.95, n - 1)
    lo, hi = m - tc * sem, m + tc * sem
    p_lo = float(stats.t.sf((m + margin) / sem, n - 1))     # H0: mean <= -margin
    p_hi = float(stats.t.cdf((m - margin) / sem, n - 1))    # H0: mean >= +margin
    p_tost = max(p_lo, p_hi)
    return {"mean": m, "ci90": [lo, hi], "margin": float(margin),
            "equivalent": bool(lo > -margin and hi < margin), "p_tost": p_tost}


def gain_from_rungs(deltas, dhat, sigma, sd_D):
    """OLS-through-origin slopes.  NAT-gain: dhat vs delta.  STD-gain: (dhat/sd_D) vs (delta/sigma)."""
    d = np.asarray(deltas, float)
    y = np.asarray(dhat, float)
    g_nat = float((d @ y) / (d @ d)) if (d @ d) > 0 else float("nan")
    x_s = d / sigma
    y_s = y / sd_D if sd_D > 0 else y * 0.0
    g_std = float((x_s @ y_s) / (x_s @ x_s)) if (x_s @ x_s) > 0 else float("nan")
    return g_nat, g_std


def ladder_for(atoms_e, atoms_c, name, model, sigma, eps, idx=None):
    """Return (deltas, incremental Delta_hat per rung, sd_D, baseline paired diff vector)."""
    sub = (lambda a: {k: v[idx] for k, v in a.items()}) if idx is not None else (lambda a: a)
    ae, ac = sub(atoms_e), sub(atoms_c)
    ep = eps if idx is None else eps[idx]
    base = det(ae, name) - det(ac, name)
    sd_D = float(base.std(ddof=1))
    d0 = float(base.mean())
    deltas, dhat = [], []
    for k in LADDER:
        delta = k * sigma
        sp = spike(ae, delta, model, ep)
        v = det(sp, name) - det(ac, name)
        deltas.append(delta)
        dhat.append(float(v.mean()) - d0)      # INCREMENTAL (baseline removed)
    return np.array(deltas), np.array(dhat), sd_D, base


def run_dataset(tag, path, note):
    atoms, n = load(path)
    ae, ac = atoms[EXP], atoms[CTL]
    # sigma = item-level paired sd of (EXP - c0) on the pre-registered headline axis m_B_conj
    sigma = float((ae["m_B_conj"] - ac["m_B_conj"]).std(ddof=1))

    rng = np.random.default_rng(RANDSIGN_SEED)
    eps = np.ones(n)
    eps[: n // 2] = -1.0                 # exactly balanced -> TRUE mean effect == 0
    rng.shuffle(eps)
    eps_mean = float(eps.mean())

    res = {"dataset": tag, "path": path, "note": note, "n_items": n,
           "sigma_nats": sigma, "randsign_eps_mean": eps_mean, "detectors": {}}

    boot_idx = [rng.integers(0, n, n) for _ in range(N_BOOT)]

    for name in DETECTORS:
        entry = {}
        for model in ("PROX", "SYM"):
            deltas, dhat, sd_D, base = ladder_for(ae, ac, name, model, sigma, eps)
            g_nat, g_std = gain_from_rungs(deltas, dhat, sigma, sd_D)
            # bootstrap CI over items (paired structure preserved)
            gs_n, gs_s = [], []
            for bi in boot_idx:
                d_b, y_b, sdD_b, _ = ladder_for(ae, ac, name, model, sigma, eps, idx=bi)
                a, b = gain_from_rungs(d_b, y_b, sigma, sdD_b)
                gs_n.append(a); gs_s.append(b)
            gs_n, gs_s = np.array(gs_n), np.array(gs_s)
            mde = 2.80 * sd_D / np.sqrt(n)
            se_gnat = (sd_D / np.sqrt(n)) / (1.0 * sigma)   # se of gain at the k=1 rung
            entry[model] = {
                "sd_D_item": sd_D,
                "MDE_a05_p80": float(mde),
                "se_gain_k1": float(se_gnat),
                "rungs": [{"k": k, "delta": float(d), "delta_hat": float(y)}
                          for k, d, y in zip(LADDER, deltas, dhat)],
                "gain_nat": g_nat,
                "gain_std": g_std,
                "gain_std_ci95": [float(np.percentile(gs_s, 2.5)), float(np.percentile(gs_s, 97.5))],
                "gain_nat_ci95": [float(np.percentile(gs_n, 2.5)), float(np.percentile(gs_n, 97.5))],
                "log_gain_tost_pass": bool(PASS_LO <= np.percentile(gs_s, 2.5)
                                           and np.percentile(gs_s, 97.5) <= PASS_HI),
                "pass_band": bool(PASS_LO <= g_std <= PASS_HI),
            }
        # ---- pedestals
        # P0: k = 0 rung must be exactly 0
        p0 = all(abs(r["delta_hat"]) < 1e-12 for r in entry["PROX"]["rungs"] if r["k"] == 0.0)
        # P1: RANDSIGN, TRUE mean effect = 0 by construction (balanced +-delta at |delta| = 1 sigma / 2 sigma)
        ped = {}
        for k in (1.0, 2.0):
            delta = k * sigma
            base = det(ae, name) - det(ac, name)
            sp = spike(ae, delta, "RANDSIGN", eps)
            v = (det(sp, name) - det(ac, name)) - base      # incremental, per item
            sd_D = float(base.std(ddof=1))
            mde = 2.80 * sd_D / np.sqrt(n)
            t = paired_stats(v)
            tt = tost_zero(v, mde)
            ped["k%.0f" % k] = {"true_delta": 0.0, "measured": t, "tost_vs_0": tt,
                                "bias_in_sd_D": float(t["mean"] / sd_D) if sd_D else 0.0}
        entry["pedestal_P0_zero_rung_exact"] = bool(p0)
        entry["pedestal_P1_randsign"] = ped
        res["detectors"][name] = entry

    # ---- positive controls
    gnat_mB = res["detectors"]["m_B_conj"]["PROX"]["gain_nat"]
    pc1 = bool(abs(gnat_mB - 1.0) < 1e-9)
    sp2 = spike(ae, 2.0 * sigma, "PROX")
    v2 = det(sp2, "m_B_conj") - det(ac, "m_B_conj")
    st2 = paired_stats(v2)
    pc2 = bool(st2["p"] < 0.05 and st2["t"] > 0)
    res["positive_controls"] = {
        "PC1_analytic_identity_gain_nat_mB_eq_1": {"gain_nat": gnat_mB, "pass": pc1},
        "PC2_liveness_recover_2sigma_spike": {"paired_t": st2, "pass": pc2},
    }
    return res


def main():
    out = {"experiment": "CAL-6 detector gain calibration (spike-in ladder)",
           "prereg": "PREREG.md (frozen before any spike was run)",
           "code_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
           "ladder_k": LADDER, "pass_band": [PASS_LO, PASS_HI],
           "log_gain_tost_margin": float(LOG_MARGIN),
           "datasets": []}
    for tag, path, note in DATASETS:
        print("[cal6] %s ..." % tag, flush=True)
        out["datasets"].append(run_dataset(tag, path, note))

    # ---- pre-registered verdict branch (section 8 of PREREG.md)
    pc_ok = all(d["positive_controls"]["PC1_analytic_identity_gain_nat_mB_eq_1"]["pass"]
                and d["positive_controls"]["PC2_liveness_recover_2sigma_spike"]["pass"]
                for d in out["datasets"])
    p0_ok = all(e["pedestal_P0_zero_rung_exact"]
                for d in out["datasets"] for e in d["detectors"].values())
    p1_lin_ok = all(d["detectors"][nm]["pedestal_P1_randsign"]["k1"]["tost_vs_0"]["equivalent"]
                    for d in out["datasets"] for nm in LINEAR_NATS)
    powered = all(d["detectors"][nm][m]["se_gain_k1"] <= 0.10
                  for d in out["datasets"] for nm in LINEAR_NATS for m in ("PROX", "SYM"))
    gains_ok = all(d["detectors"][nm][m]["pass_band"]
                   for d in out["datasets"] for nm in DETECTORS for m in ("PROX", "SYM"))

    if not pc_ok:
        verdict, reason = "INVALID", "positive control failed (harness broken)"
    elif not (p0_ok and p1_lin_ok):
        verdict, reason = "INVALID", "pedestal failed (P0 exactness or P1 randsign on linear detectors)"
    elif not powered:
        verdict, reason = "NOT-POWERED", "se(gain) > 0.10 on a headline axis"
    elif gains_ok:
        verdict, reason = "FAIL", "every detector gain within [0.8,1.25] -> D6 (gain defect) dead"
    else:
        offenders = sorted({nm for d in out["datasets"] for nm in DETECTORS
                            for m in ("PROX", "SYM") if not d["detectors"][nm][m]["pass_band"]})
        verdict, reason = "PASS", "gain outside [0.8,1.25] for: " + ", ".join(offenders)

    out["gates"] = {"positive_controls": pc_ok, "pedestal_P0": p0_ok,
                    "pedestal_P1_linear": p1_lin_ok, "powered": powered,
                    "all_gains_in_band": gains_ok}
    out["VERDICT"] = verdict
    out["verdict_reason"] = reason
    json.dump(out, open(os.path.join(ROOT, "cal6_result.json"), "w"), indent=1)

    # ---- console summary
    print("\n=== CAL-6  VERDICT = %s  (%s)\n" % (verdict, reason))
    for d in out["datasets"]:
        print("## %s  n=%d  sigma=%.4f nats" % (d["dataset"], d["n_items"], d["sigma_nats"]))
        pc = d["positive_controls"]
        print("   PC1 gain_nat(m_B|PROX)=%.9f pass=%s | PC2 t=%.2f p=%.2e pass=%s"
              % (pc["PC1_analytic_identity_gain_nat_mB_eq_1"]["gain_nat"],
                 pc["PC1_analytic_identity_gain_nat_mB_eq_1"]["pass"],
                 pc["PC2_liveness_recover_2sigma_spike"]["paired_t"]["t"],
                 pc["PC2_liveness_recover_2sigma_spike"]["paired_t"]["p"],
                 pc["PC2_liveness_recover_2sigma_spike"]["pass"]))
        print("   %-12s %-6s %8s %8s %-20s %-6s | %-24s" %
              ("detector", "model", "gain_nat", "gain_std", "gain_std CI95", "band", "P1 randsign (true=0)"))
        for nm in DETECTORS:
            for m in ("PROX", "SYM"):
                e = d["detectors"][nm][m]
                p1 = d["detectors"][nm]["pedestal_P1_randsign"]["k1"]
                print("   %-12s %-6s %8.4f %8.4f [%6.3f,%6.3f] %-6s | %+.4f (t=%+.2f) eq0=%s"
                      % (nm, m, e["gain_nat"], e["gain_std"],
                         e["gain_std_ci95"][0], e["gain_std_ci95"][1],
                         "PASS" if e["pass_band"] else "FAIL",
                         p1["measured"]["mean"], p1["measured"]["t"],
                         p1["tost_vs_0"]["equivalent"]))
        print()


if __name__ == "__main__":
    main()
