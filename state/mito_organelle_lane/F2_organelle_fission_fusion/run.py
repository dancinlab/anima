#!/usr/bin/env python3
# H_9274 / F2 — organelle fission-fusion probe ($0 · numpy · CPU-local)
#
# PRE-REGISTERED (card HYPOTHESES/cards/H_9274_mito_fission_fusion.md §3):
#   exp : health-aware fission-fusion  (fission = highest-stress unit, load-balanced split;
#                                       fusion  = two lowest-health units)
#   c1  : frozen (no dynamics)
#   c2  : random rewiring (SAME event rate, health/load-blind targets)
#   + 2 same-budget decomposition ablations (a3 = aware-fusion only, a4 = aware-fission only)
#
# PASS  : d_throughput(exp) - max(c1,c2) > margin   (margin pre-registered below)
# FAIL  : exp ~= c2  ==> the dynamics carry no health information  ==> THEATER
#
# Everything below (rho_primary, margin, seeds, all constants) is fixed BEFORE the run.
# No hyperparameter is re-tuned after looking at the result (no tune-to-green).
#
# Substrate (organelle lane · DISJOINT from decode/emit · touches NO emit gate):
#   S sites with a drifting spatial demand field (total demand CONSTANT, only its
#   spatial distribution random-walks -> a frozen organelle partition goes stale).
#   N organelles: (territory subset of sites, capacity c_i, mtDNA lesion mask L_i in {0,1}^G).
#   health h_i   = 1 - |L_i|/G
#   load_i       = sum of demand over its territory   (ATP cannot be shipped between units)
#   supply_i     = c_i * h_i
#   output_i     = min(load_i, supply_i)              <-- non-fungible capacity = the pooling gain
#   stress_i     = load_i / supply_i
#   damage (F4-linked ROS): new lesions ~ Poisson(b0 + b1*max(0, stress-1))  -> random gene KO
#   repair                : each broken gene repaired w.p. r per step (uniform across ALL arms)
#   FUSION   = territory union, capacity SUM, lesions = L_i AND L_j (mtDNA complementation
#              = the "damage dilution" of the card; identical rule in every dynamic arm)
#   FISSION  = territory split in 2, capacity HALVED each, mtDNA COPIED to both children
#   Total capacity is conserved by BOTH ops -> every arm has the exact same resource budget.
#   Event budget: k fissions + k fusions per step in every dynamic arm (N stays constant).
#
# INVARIANT (p5): this probe never reads or writes an emit gate. Structure lane only.

import json
import os
import time

import numpy as np

# ---------------- pre-registered constants ----------------
S = 64            # sites
N0 = 16           # organelles (constant: k fissions + k fusions per step)
G = 32            # mtDNA genes
T = 300           # steps
WARM = 150        # steady-state window = steps [WARM, T)
K_EV = 2          # events per step per type (fission x2, fusion x2)
B0 = 0.05         # baseline lesion rate (lesions/step/unit)
B1 = 3.0          # ROS lesion rate per unit of excess stress
EXC_CAP = 2.0     # ROS damage SATURATES at 2.0 excess stress (numerical guard: a dead unit has
                  # supply->0 => stress->inf => an unbounded Poisson draw. Applied IDENTICALLY in
                  # every arm, so it cannot favour any arm.)
REPAIR = 0.01     # per-broken-gene repair prob / step
SEEDS = [0, 1, 2, 3, 4]
RHO_PRIMARY = 0.85                       # primary (pre-registered) utilisation = loaded cell
RHO_SWEEP = [0.50, 0.70, 0.85, 1.00, 1.20]   # reported in full, verdict comes from RHO_PRIMARY
MARGIN_REL = 0.01                        # 1% of total demand
D_TOTAL = 100.0

OUT = os.path.dirname(os.path.abspath(__file__))


# ---------------- substrate ----------------
class Unit:
    __slots__ = ("sites", "cap", "les")

    def __init__(self, sites, cap, les):
        self.sites = list(sites)
        self.cap = float(cap)
        self.les = les          # bool[G]

    def health(self):
        return 1.0 - self.les.sum() / G


def init_state(rng, rho):
    # heterogeneous demand field, total normalised to D_TOTAL
    d = np.exp(rng.normal(0.0, 0.6, size=S))
    d *= D_TOTAL / d.sum()
    # random partition of sites into N0 groups
    perm = rng.permutation(S)
    groups = np.array_split(perm, N0)
    C_total = D_TOTAL / rho
    units = []
    for g in groups:
        load = d[g].sum()
        cap = C_total * load / D_TOTAL        # capacity initially MATCHED to local demand
        units.append(Unit(g, cap, np.zeros(G, dtype=bool)))
    return d, units


def drift(d, rng):
    ld = np.log(d)
    ld += rng.normal(0.0, 0.05, size=S)               # slow spatial random walk
    jump = rng.random(S) < 0.02                        # occasional demand relocation
    ld[jump] += rng.normal(0.0, 0.8, size=int(jump.sum()))
    d = np.exp(ld)
    d *= D_TOTAL / d.sum()                             # TOTAL demand constant -> rho fixed
    return d


def loads(units, d):
    return np.array([d[u.sites].sum() for u in units])


def supplies(units):
    return np.array([u.cap * u.health() for u in units])


# ---------------- events ----------------
def do_fission(units, d, rng, aware):
    cand = [i for i, u in enumerate(units) if len(u.sites) >= 2]
    if not cand:
        return
    if aware:
        L = loads(units, d)
        Sup = np.maximum(supplies(units), 1e-9)
        stress = L / Sup
        i = max(cand, key=lambda j: stress[j])
    else:
        i = int(cand[rng.integers(len(cand))])
    u = units.pop(i)
    sites = np.array(u.sites)
    if aware:
        # load-balanced split (greedy LPT) = the "load distribution" function of fission
        order = sites[np.argsort(-d[sites])]
        a, b, sa, sb = [], [], 0.0, 0.0
        for s in order:
            if sa <= sb:
                a.append(s); sa += d[s]
            else:
                b.append(s); sb += d[s]
        if not a or not b:                 # degenerate guard
            a, b = list(sites[:1]), list(sites[1:])
    else:
        p = rng.permutation(sites)
        h = max(1, len(p) // 2)
        a, b = list(p[:h]), list(p[h:])
        if not b:
            a, b = list(p[:-1]), list(p[-1:])
    half = u.cap / 2.0
    units.append(Unit(a, half, u.les.copy()))          # mtDNA copied to both children
    units.append(Unit(b, half, u.les.copy()))


def do_fusion(units, rng, aware, diag=None):
    if len(units) < 2:
        return
    if aware:
        h = np.array([u.health() for u in units])
        idx = np.argsort(h)[:2]                        # two LOWEST-health units
        i, j = int(idx[0]), int(idx[1])
    else:
        i, j = (int(x) for x in rng.choice(len(units), size=2, replace=False))
    if i == j:
        return
    lo, hi = min(i, j), max(i, j)
    b = units.pop(hi)
    a = units.pop(lo)
    merged = a.les & b.les
    if diag is not None:
        # complementation diagnostics (pure read-out — consumes NO rng, results stay bit-identical)
        ka, kb, km = int(a.les.sum()), int(b.les.sum()), int(merged.sum())
        diag["gain"].append(0.5 * (ka + kb) - km)       # lesion mass diluted by this fusion
        diag["hamming"].append(int((a.les ^ b.les).sum()))   # damage HETEROGENEITY of the pair
        diag["clone"].append(1.0 if (ka == kb == km and ka > 0) else 0.0)  # identical genomes
    units.append(Unit(a.sites + b.sites,
                      a.cap + b.cap,                    # capacity POOLED (conserved)
                      merged))                          # mtDNA complementation = damage dilution


# ---------------- one run ----------------
def simulate(seed, rho, dynamic, aware_fission, aware_fusion):
    rng_d = np.random.default_rng(10_000 + seed)       # demand stream: IDENTICAL across arms (paired)
    rng_a = np.random.default_rng(90_000 + seed)       # arm-internal stream
    d, units = init_state(rng_d, rho)

    tp, hh, ss, ov = [], [], [], []
    diag = {"gain": [], "hamming": [], "clone": []}
    for t in range(T):
        d = drift(d, rng_d)
        if dynamic:
            for _ in range(K_EV):
                do_fission(units, d, rng_a, aware_fission)
                do_fusion(units, rng_a, aware_fusion, diag if t >= WARM else None)

        L = loads(units, d)
        Sup = supplies(units)
        out = np.minimum(L, Sup)
        stress = L / np.maximum(Sup, 1e-9)
        caps = np.array([u.cap for u in units])
        hw = float((caps * np.array([u.health() for u in units])).sum() / max(caps.sum(), 1e-9))

        tp.append(out.sum() / D_TOTAL)
        hh.append(hw)
        ss.append(float(np.minimum(stress, 10.0).mean()))   # clipped only for the diagnostic
        ov.append(float((stress > 1.0).mean()))

        # damage (ROS) + repair — identical process in every arm
        for u, st in zip(units, stress):
            lam = B0 + B1 * min(max(0.0, st - 1.0), EXC_CAP)
            n = rng_a.poisson(lam)
            if n:
                u.les[rng_a.integers(0, G, size=int(n))] = True
            brk = np.flatnonzero(u.les)
            if brk.size:
                fixed = brk[rng_a.random(brk.size) < REPAIR]
                u.les[fixed] = False

    w = slice(WARM, T)
    mm = lambda v: float(np.mean(v)) if v else 0.0
    return dict(
        throughput=float(np.mean(tp[w])),
        health=float(np.mean(hh[w])),
        stress=float(np.mean(ss[w])),
        overload_frac=float(np.mean(ov[w])),
        fuse_gain=mm(diag["gain"]),          # lesion mass diluted per fusion event
        fuse_hamming=mm(diag["hamming"]),    # damage heterogeneity of the fused pair
        fuse_clone_frac=mm(diag["clone"]),   # fraction of fusions between IDENTICAL genomes
        n_units=len(units),
        cap_total=float(sum(u.cap for u in units)),
    )


ARMS = {
    "exp_aware_ff":  dict(dynamic=True,  aware_fission=True,  aware_fusion=True),
    "c1_frozen":     dict(dynamic=False, aware_fission=False, aware_fusion=False),
    "c2_random_rw":  dict(dynamic=True,  aware_fission=False, aware_fusion=False),
    "a3_awarefuse":  dict(dynamic=True,  aware_fission=False, aware_fusion=True),
    "a4_awarefiss":  dict(dynamic=True,  aware_fission=True,  aware_fusion=False),
}


def main():
    t0 = time.time()
    res = {"config": dict(S=S, N0=N0, G=G, T=T, WARM=WARM, K_EV=K_EV, B0=B0, B1=B1,
                          REPAIR=REPAIR, seeds=SEEDS, rho_primary=RHO_PRIMARY,
                          rho_sweep=RHO_SWEEP, margin_rel=MARGIN_REL),
           "runs": {}}

    for rho in RHO_SWEEP:
        key = f"rho={rho:.2f}"
        res["runs"][key] = {}
        for arm, kw in ARMS.items():
            per = [simulate(s, rho, **kw) for s in SEEDS]
            agg = {}
            for m in ("throughput", "health", "stress", "overload_frac",
                      "fuse_gain", "fuse_hamming", "fuse_clone_frac"):
                v = np.array([p[m] for p in per])
                agg[m] = {"mean": float(v.mean()), "std": float(v.std(ddof=1)),
                          "per_seed": [float(x) for x in v]}
            agg["n_units"] = [p["n_units"] for p in per]
            agg["cap_total"] = [round(p["cap_total"], 6) for p in per]
            res["runs"][key][arm] = agg

    # ---- verdict at the pre-registered primary rho ----
    pk = f"rho={RHO_PRIMARY:.2f}"
    R = res["runs"][pk]
    e = np.array(R["exp_aware_ff"]["throughput"]["per_seed"])
    c1 = np.array(R["c1_frozen"]["throughput"]["per_seed"])
    c2 = np.array(R["c2_random_rw"]["throughput"]["per_seed"])
    best_ctrl_mean = max(c1.mean(), c2.mean())
    best_ctrl_name = "c1_frozen" if c1.mean() >= c2.mean() else "c2_random_rw"
    best_ctrl = c1 if c1.mean() >= c2.mean() else c2
    d_paired = e - best_ctrl                      # same seed = same demand trajectory
    delta = float(e.mean() - best_ctrl_mean)
    sd = float(d_paired.std(ddof=1))

    # validity gates (V1 liveness): damage must be real AND capacity must bind in c1
    v1_damage = R["c1_frozen"]["health"]["mean"] < 0.99
    v1_binding = R["c1_frozen"]["throughput"]["mean"] < 0.999
    cap_ok = all(abs(c - D_TOTAL / RHO_PRIMARY) < 1e-6
                 for arm in ARMS for c in R[arm]["cap_total"])
    n_ok = all(n == N0 for arm in ARMS for n in R[arm]["n_units"])

    # same-budget decomposition: paired delta of each ablation vs the blind control c2
    abl = {}
    for arm in ("a3_awarefuse", "a4_awarefiss", "exp_aware_ff"):
        v = np.array(R[arm]["throughput"]["per_seed"]) - c2
        abl[arm + "_minus_c2"] = {"mean": float(v.mean()), "std": float(v.std(ddof=1)),
                                  "per_seed": [float(x) for x in v]}

    passed = (delta > MARGIN_REL) and (delta > 2 * sd) and v1_damage and v1_binding
    res["ablation_paired_vs_c2"] = abl
    res["verdict"] = {
        "primary_rho": RHO_PRIMARY,
        "exp_throughput": float(e.mean()),
        "c1_throughput": float(c1.mean()),
        "c2_throughput": float(c2.mean()),
        "best_control": best_ctrl_name,
        "delta_vs_best_control": delta,
        "delta_paired_std": sd,
        "delta_per_seed": [float(x) for x in d_paired],
        "delta_vs_c2_only": float(e.mean() - c2.mean()),
        "margin_rel": MARGIN_REL,
        "V1_damage_real": bool(v1_damage),
        "V1_capacity_binding": bool(v1_binding),
        "capacity_conserved": bool(cap_ok),
        "n_units_conserved": bool(n_ok),
        "PASS": bool(passed),
    }
    res["wall_s"] = round(time.time() - t0, 2)

    with open(os.path.join(OUT, "result.json"), "w") as f:
        json.dump(res, f, indent=2)

    print(json.dumps(res["verdict"], indent=2))
    for rho in RHO_SWEEP:
        k = f"rho={rho:.2f}"
        line = [k]
        for arm in ARMS:
            a = res["runs"][k][arm]
            line.append(f"{arm}: tp={a['throughput']['mean']:.4f}±{a['throughput']['std']:.4f} "
                        f"h={a['health']['mean']:.3f} ovl={a['overload_frac']['mean']:.3f}")
        print("\n  ".join(line))
    print("wall_s", res["wall_s"])


if __name__ == "__main__":
    main()
