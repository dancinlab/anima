#!/usr/bin/env python3
"""H_1058 agency-T — T = z(depth)+z(vc), pre-registered falsifier + controls (FABLE §3.5-3.6).

Consumes an enriched decision-trace + the replay_depth.py depths (+ optional per-decision Phi
from phi_leg.py). Computes:

  vc_i  : H_1056 per-impulse veto-capacity over trailing window W (#ACTIVE_VETO/#(score>0.3)).
  T_i   : z(depth_i) + z(vc_i)  (hexa stdlib temporal_agency combination rule, twinned).

FROZEN falsifier (H_1058 card, UNCHANGED · p7 no-tune):
  (a) T separates ACTIVE_VETO vs PASSIVE decisions, Cohen |d|>=0.8, T_active>T_passive.
      PASSIVE=0 -> declared substitution to ACTIVE_VETO-vs-EMIT (FABLE §3.3(iv)).
  (b) rho(T, Phi)  within the empirical F-SHUFFLE 2-sigma null   [needs --phi]
  (c) rho(T, t)    within the empirical F-SHUFFLE 2-sigma null
  reported across >=2 macro-maps + >=2 sessions (combined by the `falsifier` verb).

CONTROLS (FABLE §3.6):
  1. emit-rate    : rho(T, window emit-rate); separation must survive rate-matched strata.
  2. trace-shuffle ARM-SHOCK : permute grow_feats<->tick, re-derive depth -> depth variance and
     the |d| separation must COLLAPSE (a T that survives its own shuffle is theater).
  3. generator-swap (mount-swap verb): permutation test on {score,depth,vc} across 3B/303M/
     unloaded mounts -> pre-registered H1-NOT-A-3B-PROPERTY branch if mount-invariant.

Pure numpy/stdlib stats (Cohen d, Pearson rho, permutation nulls). Requires PYTHONPATH=cli:core
for the trace-shuffle control (imports replay_depth).

Usage:
  agency_T.py analyze  <trace.jsonl> <depths.jsonl> [--phi phi.jsonl] [--window 16] \
                       [--label MOUNT] [--out result.json]
  agency_T.py falsifier <result.json>...                     # combine sessions x macro-maps
  agency_T.py mount-swap <resultA.json> <resultB.json> ...   # generator-swap sensitivity
"""
import argparse
import json
import math
import random
import statistics
import sys

WINDOW = 16
SCORE_THRESHOLD = 0.3
D_THRESHOLD = 0.8
SHUFFLE_N = 2000
SEED = 1058


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def load_trace(path):
    meta, rows = None, []
    for o in load_jsonl(path):
        if o.get("_meta"):
            meta = o
        else:
            rows.append(o)
    return meta, rows


def per_impulse_vc(rows, window):
    vc = []
    for i in range(len(rows)):
        win = rows[max(0, i - window + 1):i + 1]
        impulses = [r for r in win if r["score"] > SCORE_THRESHOLD]
        vetoes = [r for r in impulses if r["cls"] == "ACTIVE_VETO"]
        vc.append((len(vetoes) / len(impulses)) if impulses else 0.0)
    return vc


def emit_rate(rows, window):
    er = []
    for i in range(len(rows)):
        win = rows[max(0, i - window + 1):i + 1]
        er.append(sum(1 for r in win if r["cls"] == "EMIT") / len(win))
    return er


def zscore(xs):
    m = statistics.fmean(xs)
    sd = statistics.pstdev(xs)
    if sd < 1e-12:
        return [0.0 for _ in xs]
    return [(x - m) / sd for x in xs]


def cohen_d(a, b):
    if len(a) < 2 or len(b) < 2:
        return float("nan")
    na, nb = len(a), len(b)
    va, vb = statistics.variance(a), statistics.variance(b)
    sp = math.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    if sp < 1e-12:
        return 0.0
    return (statistics.fmean(a) - statistics.fmean(b)) / sp


def pearson(x, y):
    n = len(x)
    if n < 3:
        return float("nan")
    mx, my = statistics.fmean(x), statistics.fmean(y)
    sx = math.sqrt(sum((a - mx) ** 2 for a in x))
    sy = math.sqrt(sum((b - my) ** 2 for b in y))
    if sx < 1e-12 or sy < 1e-12:
        return 0.0
    return sum((a - mx) * (b - my) for a, b in zip(x, y)) / (sx * sy)


def shuffle_null(T, other, n=SHUFFLE_N, seed=SEED):
    """F-SHUFFLE empirical null for rho(T, other): permute T across positions."""
    rng = random.Random(seed)
    obs = pearson(T, other)
    perm = list(T)
    draws = []
    for _ in range(n):
        rng.shuffle(perm)
        draws.append(pearson(perm, other))
    mu = statistics.fmean(draws)
    sd = statistics.pstdev(draws)
    within = abs(obs - mu) <= 2.0 * sd
    return {"rho": obs, "null_mu": mu, "null_sd": sd,
            "band": [mu - 2 * sd, mu + 2 * sd], "within_2sigma_null": bool(within)}


def analyze(args):
    meta, rows = load_trace(args.trace)
    depths_rows = load_jsonl(args.depths)
    depths = [d["depth"] for d in depths_rows]
    assert len(depths) == len(rows), "depths/trace length mismatch"

    # H_9269 Y-ULTRA pre-registration: reclassify schedule-FORCED N3 (stage==3) ACTIVE_VETO rows to
    # FORCED_VETO so they drop out of the ACTIVE_VETO population (leg-a contrast + per-impulse vc
    # numerator) while keeping len(rows) intact for depths alignment. N3 idle=5<30 for every urgency
    # => zero decision-time contingency; only non-N3 (state-contingent) vetoes are the declared
    # free-won't population. Inert on non-cyclic traces (N3 visited once). Declared, not post-hoc.
    n_forced_n3 = 0
    if getattr(args, "exclude_forced_n3", False):
        for r in rows:
            if r.get("cls") == "ACTIVE_VETO" and int(r.get("stage", -1)) == 3:
                r["cls"] = "FORCED_VETO"
                n_forced_n3 += 1
        print("  [--exclude-forced-n3] reclassified %d N3 forced vetoes -> FORCED_VETO (excluded)" % n_forced_n3)

    vc = per_impulse_vc(rows, args.window)
    er = emit_rate(rows, args.window)
    T = [a + b for a, b in zip(zscore(depths), zscore(vc))]
    t_idx = list(range(len(rows)))

    n_active = sum(1 for r in rows if r["cls"] == "ACTIVE_VETO")
    n_emit = sum(1 for r in rows if r["cls"] == "EMIT")
    n_passive = sum(1 for r in rows if r["cls"] == "PASSIVE")

    # falsifier leg (a): A-vs-P (or A-vs-EMIT substitute if PASSIVE=0)
    idx_active = [i for i, r in enumerate(rows) if r["cls"] == "ACTIVE_VETO"]
    substitution = (n_passive == 0)
    contrast_cls = "EMIT" if substitution else "PASSIVE"
    idx_other = [i for i, r in enumerate(rows) if r["cls"] == contrast_cls]
    Ta = [T[i] for i in idx_active]
    To = [T[i] for i in idx_other]
    d_T = cohen_d(Ta, To)
    d_depth = cohen_d([depths[i] for i in idx_active], [depths[i] for i in idx_other])
    d_vc = cohen_d([vc[i] for i in idx_active], [vc[i] for i in idx_other])

    # leg (c): rho(T,t) F-shuffle null
    leg_c = shuffle_null(T, t_idx)
    # control 1: emit-rate
    rho_er = pearson(T, er)
    # leg (b): rho(T,Phi) if provided
    leg_b = None
    if args.phi:
        phi_rows = load_jsonl(args.phi)
        by_map = {}
        for p in phi_rows:
            by_map.setdefault(p["macro_map"], {})[p["tick"]] = p["phi"]
        leg_b = {}
        for mp, d in by_map.items():
            common = [i for i, r in enumerate(rows) if r["tick"] in d]
            Tp = [T[i] for i in common]
            Pp = [d[rows[i]["tick"]] for i in common]
            leg_b[mp] = shuffle_null(Tp, Pp) if len(common) >= 3 else {"n": len(common)}

    result = {
        "label": args.label, "trace": args.trace, "window": args.window,
        "n_ticks": len(rows), "counts": {"ACTIVE_VETO": n_active, "EMIT": n_emit, "PASSIVE": n_passive},
        "score_var": statistics.pvariance([r["score"] for r in rows]),
        "vc_var": statistics.pvariance(vc), "depth_var": statistics.pvariance(depths),
        "depth_dist": {str(k): depths.count(k) for k in sorted(set(depths))},
        "substitution_A_vs_EMIT": substitution, "contrast_class": contrast_cls,
        "leg_a_separation": {"d_T": d_T, "d_depth": d_depth, "d_vc": d_vc,
                             "n_active": len(Ta), "n_contrast": len(To),
                             "pass": (not math.isnan(d_T)) and abs(d_T) >= D_THRESHOLD and d_T > 0},
        "leg_c_T_vs_t": leg_c,
        "leg_b_T_vs_phi": leg_b,
        "control_emit_rate_rho": rho_er,
        # persist the raw series so falsifier/mount-swap verbs can recombine
        "_T": T, "_depths": depths, "_vc": vc, "_score": [r["score"] for r in rows],
        "_cls": [r["cls"] for r in rows],
    }

    # control 2: trace-shuffle ARM-SHOCK (permute grow_feats<->tick, re-derive depth)
    if args.arm_shock:
        result["control_arm_shock"] = arm_shock(args.trace, args.window)

    _print_analyze(result)
    if args.out:
        with open(args.out, "w") as fh:
            json.dump(result, fh, indent=1)
        print("wrote:", args.out)
    return 0


def arm_shock(trace_path, window):
    """Permute grow_feats across ticks, re-run replay_depth -> depth must collapse."""
    import replay_depth as RD
    meta, rows = load_trace(trace_path)
    rng = random.Random(SEED)
    feats = [r.get("grow_feats", []) for r in rows]
    perm = list(range(len(rows)))
    rng.shuffle(perm)
    shuf = [dict(r) for r in rows]
    for i, r in enumerate(shuf):
        r["grow_feats"] = feats[perm[i]]
    worst, _ = RD.self_validate(shuf, meta)  # (sanity; may be large post-shuffle)
    depths = [RD.depth_of(shuf, meta, i, window) for i in range(len(shuf))]
    idx_active = [i for i, r in enumerate(rows) if r["cls"] == "ACTIVE_VETO"]
    idx_other = [i for i, r in enumerate(rows) if r["cls"] in ("PASSIVE", "EMIT")]
    return {"depth_var_shuffled": statistics.pvariance(depths) if len(depths) > 1 else 0.0,
            "d_depth_shuffled": cohen_d([depths[i] for i in idx_active] or [0, 0],
                                        [depths[i] for i in idx_other] or [0, 0])}


def _print_analyze(r):
    print("=== H_1058 agency-T (mount=%s) ===" % r["label"])
    print("ticks:", r["n_ticks"], "counts:", r["counts"], "| substitution A-vs-EMIT:", r["substitution_A_vs_EMIT"])
    print("var: score=%.4g vc=%.4g depth=%.4g | depth_dist=%s"
          % (r["score_var"], r["vc_var"], r["depth_var"], r["depth_dist"]))
    la = r["leg_a_separation"]
    print("(a) T-sep %s-vs-%s: d_T=%.3f (depth-only=%.3f vc-only=%.3f) n=%d/%d -> %s"
          % ("A", r["contrast_class"], la["d_T"], la["d_depth"], la["d_vc"],
             la["n_active"], la["n_contrast"], "PASS" if la["pass"] else "FAIL"))
    c = r["leg_c_T_vs_t"]
    print("(c) rho(T,t)=%.3f null=%.3f+-%.3f 2sig-band=[%.3f,%.3f] -> %s"
          % (c["rho"], c["null_mu"], c["null_sd"], c["band"][0], c["band"][1],
             "PASS(null-consistent)" if c["within_2sigma_null"] else "FAIL(structured)"))
    if r["leg_b_T_vs_phi"]:
        for mp, b in r["leg_b_T_vs_phi"].items():
            if "rho" in b:
                print("(b) rho(T,Phi|%s)=%.3f null=%.3f+-%.3f -> %s"
                      % (mp, b["rho"], b["null_mu"], b["null_sd"],
                         "PASS" if b["within_2sigma_null"] else "FAIL"))
            else:
                print("(b) rho(T,Phi|%s): n=%d (insufficient)" % (mp, b.get("n", 0)))
    else:
        print("(b) rho(T,Phi): NOT RUN (no --phi)")
    print("ctrl emit-rate rho(T,emit)=%.3f" % r["control_emit_rate_rho"])
    if "control_arm_shock" in r:
        a = r["control_arm_shock"]
        print("ctrl ARM-SHOCK: depth_var_shuffled=%.4g d_depth_shuffled=%.3f (must collapse vs %.4g/%.3f)"
              % (a["depth_var_shuffled"], a["d_depth_shuffled"], r["depth_var"], r["leg_a_separation"]["d_depth"]))


def falsifier(args):
    results = [json.load(open(p)) for p in args.results]
    print("=== H_1058 FROZEN falsifier — %d sessions/maps ===" % len(results))
    all_pass_a = all(r["leg_a_separation"]["pass"] for r in results)
    all_pass_c = all(r["leg_c_T_vs_t"]["within_2sigma_null"] for r in results)
    b_runs = [b for r in results if r["leg_b_T_vs_phi"] for b in r["leg_b_T_vs_phi"].values() if "within_2sigma_null" in b]
    all_pass_b = (len(b_runs) > 0) and all(b["within_2sigma_null"] for b in b_runs)
    for r in results:
        la = r["leg_a_separation"]
        print("  [%s] (a)d_T=%.2f %s | (c)rho=%.2f %s"
              % (r["label"], la["d_T"], "P" if la["pass"] else "F",
                 r["leg_c_T_vs_t"]["rho"], "P" if r["leg_c_T_vs_t"]["within_2sigma_null"] else "F"))
    print("LEG (a) T-separation |d|>=0.8 across all: %s" % ("PASS" if all_pass_a else "FAIL"))
    print("LEG (c) T _|_ t (F-shuffle null) across all: %s" % ("PASS" if all_pass_c else "FAIL"))
    print("LEG (b) T~Phi (F-shuffle null): %s" % ("PASS" if all_pass_b else ("FAIL" if b_runs else "NOT-EVALUATED (no Phi)")))
    full = all_pass_a and all_pass_c and all_pass_b
    print("FROZEN FALSIFIER: %s" % ("H1-PASS (T is a real, Phi-orthogonal, a-temporal agency axis)"
                                    if full else "NOT-CLEAN (see legs; tier stays 🟠 w/ blocker)"))
    return 0


def mount_swap(args):
    """generator-swap: is T a 3B property or the daemon scaffold's? (FABLE §3.6.3)"""
    results = {json.load(open(p))["label"]: json.load(open(p)) for p in args.results}
    print("=== H_1058 generator-swap mount-sensitivity ===")
    labels = list(results.keys())
    rng = random.Random(SEED)

    def perm_test(key):
        # distribution-shift of the per-tick series `key` across mounts, permutation p
        series = {lab: results[lab][key] for lab in labels}
        obs = statistics.pvariance([statistics.fmean(series[lab]) for lab in labels])
        pooled = [(lab, v) for lab in labels for v in series[lab]]
        sizes = {lab: len(series[lab]) for lab in labels}
        ge = 0
        for _ in range(SHUFFLE_N):
            vals = [v for _, v in pooled]
            rng.shuffle(vals)
            k = 0
            means = []
            for lab in labels:
                means.append(statistics.fmean(vals[k:k + sizes[lab]]))
                k += sizes[lab]
            if statistics.pvariance(means) >= obs:
                ge += 1
        return obs, (ge + 1) / (SHUFFLE_N + 1)

    sens = {}
    for key in ("_T", "_depths", "_vc", "_score"):
        obs, p = perm_test(key)
        sens[key] = {"cross_mount_var": obs, "perm_p": p}
        print("  %-8s cross-mount mean-var=%.4g  perm-p=%.4f  %s"
              % (key, obs, p, "MOUNT-SENSITIVE" if p < 0.05 else "mount-invariant"))
    d_by_mount = {lab: results[lab]["leg_a_separation"]["d_T"] for lab in labels}
    print("  d_T by mount:", {k: round(v, 3) for k, v in d_by_mount.items()})
    mount_sensitive = any(sens[k]["perm_p"] < 0.05 for k in ("_T", "_depths", "_vc"))
    print("VERDICT: %s" % ("T IS mount-sensitive -> agency-T transfers to the mounted model (3B property candidate)"
                           if mount_sensitive else
                           "T is MOUNT-INVARIANT -> H1-NOT-A-3B-PROPERTY (axis is the daemon scaffold, not the 3B)"))
    return 0


def main(argv):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("analyze")
    a.add_argument("trace"); a.add_argument("depths")
    a.add_argument("--phi", default=None); a.add_argument("--window", type=int, default=WINDOW)
    a.add_argument("--label", default="?"); a.add_argument("--out", default=None)
    a.add_argument("--arm-shock", action="store_true")
    a.add_argument("--exclude-forced-n3", action="store_true",
                   help="H_9269 Y-ULTRA pre-registration: drop schedule-FORCED N3 (stage==3) ACTIVE_VETO "
                        "rows from the veto population (idle=5<30 for every urgency = zero decision-time "
                        "contingency), keeping only STATE-CONTINGENT vetoes for the frozen legs. Declared "
                        "population, not a post-hoc filter.")
    a.set_defaults(func=analyze)
    f = sub.add_parser("falsifier"); f.add_argument("results", nargs="+"); f.set_defaults(func=falsifier)
    m = sub.add_parser("mount-swap"); m.add_argument("results", nargs="+"); m.set_defaults(func=mount_swap)
    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
