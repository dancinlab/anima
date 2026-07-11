#!/usr/bin/env python3
"""
H_9275 / F3 — mitophagy = sub-cell quality control.

Question (card §1): does *directed* mitophagy (removal keyed on the observable
damage definition = windowed efficiency ATP_out/consumed  OR  ROS_i > theta)
beat (c1) no removal and (c2) random removal of the SAME COUNT?

Substrate = ORGANELLE LANE ONLY (F3). No emit gate, no decode lane, no cell-pool
mitosis lane is touched anywhere in this file — p5 boundary is trivially clean
because there is no emit in this probe at all (grep: no `speak`, no emit gate).

--------------------------------------------------------------------------------
WHY THIS IS NOT RIGGED (the anti-tautology design)
--------------------------------------------------------------------------------
The naive version of this probe is a tautology: if you let the remover *see* the
latent health h_i, and you score the pool by mean h_i, directed removal trivially
wins. So health is LATENT here and the arms may only see two noisy, CONFOUNDED
observables — exactly the two the card names:

  obs-1  eff_hat_i : EMA of (ATP_out / consumed). ATP_out is measured with
                     counting-style noise sd = sigma_obs * sqrt(load_i), so the
                     efficiency estimate of a LOW-DEMAND organelle is noisy.
                     -> confound: low-demand healthy units look "maybe damaged".
  obs-2  ros_hat_i : EMA of ROS_i = load_i / (cap_i * h_i)  (stress = overload
                     relative to health-adjusted capacity), + 5% readout noise.
                     Per-unit demand d_i is NONUNIFORM (AR(1), persistent), so
                     load_i/cap_i varies across units even at equal health.
                     -> confound: a HEALTHY but HIGH-DEMAND organelle emits high
                        ROS and looks damaged. ROS is NOT a monotone readout of h.

If the demand confound dominates, the card's own damage definition fails and F3
is THEATER even though "directed vs random" sounds like it must win.

--------------------------------------------------------------------------------
ARMS (identical removal budget: R removals on the same schedule; c1 = the null)
--------------------------------------------------------------------------------
  exp_eff    : remove argmin eff_hat            <- primary experimental arm
  exp_ros    : remove argmax ros_hat            <- F4-coupled criterion
  exp_or     : card-literal OR rule: mark {eff_hat < th_e  OR  ros_hat > th_r},
               remove worst-eff among marked; if NOTHING is marked the rule
               carries no information and degrades to a uniform random pick
               (budget stays matched; we log the marked-rate).
  c1_none    : no removal (the null baseline the card demands)
  c2_random  : uniform random removal, SAME count / SAME schedule / SAME
               capacity redistribution / SAME compute  <- budget-matched control
  c3_anti    : remove argmax eff_hat (sign control; must be WORSE than random if
               the observable carries any signal at all)
  oracle_h   : remove argmin TRUE latent h  (ceiling, NOT a control for PASS —
               it measures how much of the achievable Delta the observable gets)

Common random numbers: demand tape, damage tape, observation-noise tape are
pre-drawn per seed and SHARED by every arm. Only the removal decision differs.
Paired per-seed Deltas therefore isolate the selection rule.

PASS (pre-registered, card §3): Delta = eff(exp) - max(eff(c1_none), eff(c2_random))
  > MARGIN (=0.02) at the nominal cell, AND sign-consistent across seeds
  (mean - std > 0).
FAIL/THEATER: directed ~= random  =>  the damage definition carries no usable
  information.  Reported as-is. No hyperparameter is touched to chase a verdict.

Sweeps over sigma_obs and sigma_demand are pre-declared CHARACTERIZATION axes
(where does the signal die?), not verdict-selection knobs. The verdict is read
off the NOMINAL cell only.

$0 CPU-local numpy. Deterministic. No torch.
"""

import json
import os
import time

import numpy as np

# ------------------------------------------------------------------ params
# PRE-REGISTERED arm criteria; substrate damage constants CALIBRATED ONCE by an
# ARM-BLIND liveness rule (see V1 below / calib_scan.py).
#
# v0 (P_HIT=.004, K_WEAR=.002, ROS0=1.0) put the substrate in TOTAL COLLAPSE:
# every arm -- INCLUDING the latent-truth oracle -- ended pinned at H_FLOOR
# (eff 0.0501 +- .0003 for all 7 arms). Zero dynamic range => the instrument is
# dead => INVALID cell, NOT a THEATER verdict. It is kept and re-run below as
# `v0_collapsed_cell` so the recalibration is auditable.
#
# The recalibration looked ONLY at the c1_none (no-removal) pool and used a rule
# that names no experimental arm: "final-window mean latent health of the
# NO-REMOVAL pool in [0.35,0.75] AND std >= 0.10" (a pool that is partly damaged
# with a real spread = the only regime in which QC could conceivably matter).
# The median live cell was taken. No arm criterion / threshold was touched.
P = dict(
    N0=64,              # organelles at t=0
    T=1500,             # timesteps
    D_TOTAL=64.0,       # total metabolic demand per step (constant; cap is conserved)
    H_LO=0.70,          # init latent health ~ U(H_LO, 1.0)
    P_HIT=0.0005,       # per-unit per-step stochastic damage event   [V1-calibrated]
    MAG_LO=0.40,        # damage event: h *= U(MAG_LO, MAG_HI)
    MAG_HI=0.90,
    K_WEAR=0.0005,      # ROS-driven wear: h *= (1 - K_WEAR*max(0, ros-ROS0))  [V1-calib]
    ROS0=1.5,           # wear only under real OVERLOAD (nominal healthy ros = 1.0) [V1]
    H_FLOOR=0.05,
    SIGMA_OBS=0.30,     # NOMINAL observation noise on ATP_out (sd ~ sigma*sqrt(load))
    SIGMA_DEMAND=0.50,  # NOMINAL per-unit demand heterogeneity (log-space sd)
    RHO_DEMAND=0.98,    # AR(1) persistence of per-unit demand
    SIGMA_ROS_OBS=0.05, # ROS readout noise (relative)
    EMA=0.96,           # observation window (~25 steps effective)
    EVENT_EVERY=50,     # removal event cadence
    N_REMOVE=24,        # total removals per arm (64 -> 40 organelles)
    TH_E=0.60,          # card-literal OR rule: eff_hat < TH_E
    TH_R=1.30,          # card-literal OR rule: ros_hat > TH_R
    FINAL_WIN=300,      # primary metric window = last 300 steps (removals are DONE)
    SEEDS=[0, 1, 2, 3, 4, 5, 6, 7],
    MARGIN=0.02,        # PASS margin on Delta efficiency
)

# the dead v0 substrate, kept for the record
P_V0 = dict(P, P_HIT=0.004, K_WEAR=0.002, ROS0=1.0)

ARMS = ["exp_eff", "exp_ros", "exp_or", "c1_none", "c2_random", "c3_anti", "oracle_h"]
EXP_ARMS = ["exp_eff", "exp_ros", "exp_or"]
CONTROLS = ["c1_none", "c2_random"]


# ------------------------------------------------------------------ tape
def make_tape(seed, p):
    """Pre-draw every random stream. Shared by all arms (common random numbers)."""
    N, T = p["N0"], p["T"]
    rng = np.random.default_rng(1000 + seed)
    h0 = rng.uniform(p["H_LO"], 1.0, size=N)
    # AR(1) log-demand per unit
    z = np.empty((T, N))
    z[0] = rng.normal(0.0, 1.0, size=N)
    eps = rng.normal(0.0, 1.0, size=(T, N))
    rho = p["RHO_DEMAND"]
    for t in range(1, T):
        z[t] = rho * z[t - 1] + np.sqrt(1.0 - rho * rho) * eps[t]
    tape = dict(
        h0=h0,
        z=z,                                        # scaled by SIGMA_DEMAND at use
        hit=rng.random((T, N)),                     # < P_HIT -> damage event
        mag=rng.uniform(p["MAG_LO"], p["MAG_HI"], size=(T, N)),
        obs=rng.standard_normal((T, N)),            # ATP_out measurement noise
        rosn=rng.standard_normal((T, N)),           # ROS readout noise
    )
    return tape


# ------------------------------------------------------------------ one arm
def run_arm(arm, tape, p, seed):
    N, T = p["N0"], p["T"]
    rng_pick = np.random.default_rng(90000 + seed)  # only used by c2_random / OR-fallback

    h = tape["h0"].copy()
    cap = np.ones(N)
    alive = np.ones(N, dtype=bool)

    ema_prod = np.zeros(N)
    ema_load = np.zeros(N)
    ema_ros = np.zeros(N)
    a = p["EMA"]

    d_all = np.exp(p["SIGMA_DEMAND"] * tape["z"])

    eff_hist = np.zeros(T)
    removed = 0
    or_marked_events = 0
    or_total_events = 0
    or_marked_frac = []   # what FRACTION of the alive pool the OR-thresholds flag
    victims = []

    for t in range(T):
        d = d_all[t]
        w = cap * d * alive
        load = p["D_TOTAL"] * w / max(w.sum(), 1e-12)

        produced = load * h
        consumed = load
        eff_hist[t] = produced.sum() / max(consumed.sum(), 1e-12)

        ros = load / np.maximum(cap * h, 1e-9)

        # --- observation (noisy, confounded) -----------------------------
        prod_obs = produced + p["SIGMA_OBS"] * np.sqrt(np.maximum(load, 0.0)) * tape["obs"][t]
        ros_obs = ros * (1.0 + p["SIGMA_ROS_OBS"] * tape["rosn"][t])
        ema_prod = a * ema_prod + (1 - a) * prod_obs
        ema_load = a * ema_load + (1 - a) * load
        ema_ros = a * ema_ros + (1 - a) * ros_obs
        eff_hat = ema_prod / np.maximum(ema_load, 1e-9)

        # --- damage ------------------------------------------------------
        wear = p["K_WEAR"] * np.clip(ros - p["ROS0"], 0.0, None)
        h = h * (1.0 - wear)
        hit = tape["hit"][t] < p["P_HIT"]
        h = np.where(hit, h * tape["mag"][t], h)
        h = np.clip(h, p["H_FLOOR"], 1.0)

        # --- removal event ----------------------------------------------
        if arm != "c1_none" and t > 0 and t % p["EVENT_EVERY"] == 0 and removed < p["N_REMOVE"]:
            idx = np.flatnonzero(alive)
            if idx.size <= 2:
                continue
            if arm == "exp_eff":
                v = idx[np.argmin(eff_hat[idx])]
            elif arm == "exp_ros":
                v = idx[np.argmax(ema_ros[idx])]
            elif arm == "exp_or":
                or_total_events += 1
                marked = idx[(eff_hat[idx] < p["TH_E"]) | (ema_ros[idx] > p["TH_R"])]
                or_marked_frac.append(marked.size / idx.size)
                if marked.size > 0:
                    or_marked_events += 1
                    v = marked[np.argmin(eff_hat[marked])]
                else:
                    v = idx[rng_pick.integers(idx.size)]   # no information -> random
            elif arm == "c2_random":
                v = idx[rng_pick.integers(idx.size)]
            elif arm == "c3_anti":
                v = idx[np.argmax(eff_hat[idx])]
            elif arm == "oracle_h":
                v = idx[np.argmin(h[idx])]
            else:
                raise ValueError(arm)

            victims.append(float(h[v]))
            alive[v] = False
            # capacity redistribution (mass conserved) over survivors
            free_cap = cap[v]
            cap[v] = 0.0
            surv = np.flatnonzero(alive)
            cap[surv] += free_cap * cap[surv] / max(cap[surv].sum(), 1e-12)
            ema_prod[v] = ema_load[v] = ema_ros[v] = 0.0
            removed += 1

    fw = p["FINAL_WIN"]
    return dict(
        eff_final=float(eff_hist[-fw:].mean()),
        eff_run=float(eff_hist.mean()),
        n_removed=int(removed),
        n_alive=int(alive.sum()),
        mean_h_alive=float(h[alive].mean()),
        std_h_alive=float(h[alive].std()),
        mean_victim_h=float(np.mean(victims)) if victims else float("nan"),
        or_marked_rate=(or_marked_events / or_total_events) if or_total_events else None,
        or_marked_frac=float(np.mean(or_marked_frac)) if or_marked_frac else None,
    )


# ------------------------------------------------------------------ cell
def run_cell(p):
    """One parameter cell -> all arms x all seeds."""
    per_seed = {arm: [] for arm in ARMS}
    extra = {arm: [] for arm in ARMS}
    for seed in p["SEEDS"]:
        tape = make_tape(seed, p)
        for arm in ARMS:
            r = run_arm(arm, tape, p, seed)
            per_seed[arm].append(r["eff_final"])
            extra[arm].append(r)

    out = {"arms": {}, "paired": {}}
    for arm in ARMS:
        v = np.array(per_seed[arm])
        rs = extra[arm]
        out["arms"][arm] = dict(
            eff_final_mean=float(v.mean()),
            eff_final_std=float(v.std(ddof=1)),
            eff_final_per_seed=[round(x, 5) for x in v.tolist()],
            eff_run_mean=float(np.mean([r["eff_run"] for r in rs])),
            n_removed=int(rs[0]["n_removed"]),
            n_alive=int(rs[0]["n_alive"]),
            mean_h_alive=float(np.mean([r["mean_h_alive"] for r in rs])),
            std_h_alive=float(np.mean([r["std_h_alive"] for r in rs])),
            mean_victim_h=float(np.nanmean([r["mean_victim_h"] for r in rs])),
            or_marked_rate=(
                float(np.mean([r["or_marked_rate"] for r in rs]))
                if rs[0]["or_marked_rate"] is not None else None
            ),
            or_marked_frac=(
                float(np.mean([r["or_marked_frac"] for r in rs]))
                if rs[0]["or_marked_frac"] is not None else None
            ),
        )

    base = np.maximum(np.array(per_seed["c1_none"]), np.array(per_seed["c2_random"]))
    for arm in ARMS:
        if arm in CONTROLS:
            continue
        d_vs_best = np.array(per_seed[arm]) - base
        d_vs_rand = np.array(per_seed[arm]) - np.array(per_seed["c2_random"])
        d_vs_none = np.array(per_seed[arm]) - np.array(per_seed["c1_none"])
        out["paired"][arm] = dict(
            delta_vs_maxctrl_mean=float(d_vs_best.mean()),
            delta_vs_maxctrl_std=float(d_vs_best.std(ddof=1)),
            delta_vs_maxctrl_per_seed=[round(x, 5) for x in d_vs_best.tolist()],
            n_seeds_positive=int((d_vs_best > 0).sum()),
            delta_vs_random_mean=float(d_vs_rand.mean()),
            delta_vs_none_mean=float(d_vs_none.mean()),
        )
    # validity check: removal per se must be ~neutral (c2 ~ c1)
    dc = np.array(per_seed["c2_random"]) - np.array(per_seed["c1_none"])
    out["validity_random_vs_none"] = dict(
        mean=float(dc.mean()), std=float(dc.std(ddof=1))
    )

    # ---- V1 LIVENESS GATE (arm-blind) --------------------------------------
    # (a) the no-removal pool must end partly damaged WITH A SPREAD, and
    # (b) the latent-truth ORACLE must be able to move the metric.
    # If either fails, the instrument has no dynamic range => the cell is
    # INVALID and NO verdict (PASS or THEATER) may be read off it.
    c1h = out["arms"]["c1_none"]
    orc = out["paired"]["oracle_h"]["delta_vs_maxctrl_mean"]
    spread_ok = (0.35 <= c1h["mean_h_alive"] <= 0.75) and (c1h["std_h_alive"] >= 0.10)
    oracle_ok = orc > 5.0 * p["MARGIN"]
    out["V1_liveness"] = dict(
        c1_mean_h=c1h["mean_h_alive"], c1_std_h=c1h["std_h_alive"],
        oracle_delta_vs_maxctrl=orc, oracle_headroom_needed=5.0 * p["MARGIN"],
        spread_ok=bool(spread_ok), oracle_ok=bool(oracle_ok),
        LIVE=bool(spread_ok and oracle_ok),
    )
    return out


def verdict_for(cell, p, arm="exp_eff"):
    pr = cell["paired"][arm]
    m, s = pr["delta_vs_maxctrl_mean"], pr["delta_vs_maxctrl_std"]
    live = cell["V1_liveness"]["LIVE"]
    if not live:
        tier = "INVALID (V1 liveness failed: no dynamic range)"
    elif (m > p["MARGIN"]) and (m - s > 0.0):
        tier = "PASS"
    elif abs(m) <= p["MARGIN"]:
        tier = "THEATER (directed ~= random)"
    else:
        tier = "FAIL (worse than controls)"
    return dict(
        arm=arm,
        tier=tier,
        pass_=bool(live and (m > p["MARGIN"]) and (m - s > 0.0)),
        rule="V1 LIVE and delta_vs_max(c1,c2) > MARGIN and mean-std > 0",
        margin=p["MARGIN"],
        delta_mean=m,
        delta_std=s,
        seeds_positive=pr["n_seeds_positive"],
        n_seeds=len(p["SEEDS"]),
    )


def main():
    t0 = time.time()
    res = {"params": {k: v for k, v in P.items()}, "arms_desc": {
        "exp_eff": "directed mitophagy on windowed efficiency (primary)",
        "exp_ros": "directed mitophagy on ROS (F4 criterion)",
        "exp_or": "card-literal: eff<th_e OR ros>th_r (random fallback if unmarked)",
        "c1_none": "CONTROL: no removal (null)",
        "c2_random": "CONTROL: random removal, budget-matched (same count/schedule/redistribution)",
        "c3_anti": "sign control: remove the BEST observed efficiency",
        "oracle_h": "ceiling (not a PASS control): remove lowest TRUE latent health",
    }}

    # ---- v0 dead substrate, kept for the audit trail ----
    v0 = run_cell(P_V0)
    res["v0_collapsed_cell"] = dict(
        params={k: P_V0[k] for k in ("P_HIT", "K_WEAR", "ROS0")},
        eff={a: round(v0["arms"][a]["eff_final_mean"], 5) for a in ARMS},
        V1_liveness=v0["V1_liveness"],
        note="every arm incl. the latent-truth oracle pinned at H_FLOOR -> INVALID, not THEATER",
    )

    # ---- nominal cell (the verdict is read off THIS cell only) ----
    nominal = run_cell(P)
    res["nominal"] = nominal
    res["verdict"] = verdict_for(nominal, P, "exp_eff")
    res["verdict_exp_ros"] = verdict_for(nominal, P, "exp_ros")
    res["verdict_exp_or"] = verdict_for(nominal, P, "exp_or")

    # ---- characterization axis 1: observation noise ----
    res["sweep_sigma_obs"] = {}
    for so in [0.0, 0.15, 0.30, 0.60, 1.20, 2.40]:
        p = dict(P); p["SIGMA_OBS"] = so
        c = run_cell(p)
        res["sweep_sigma_obs"][f"{so:.2f}"] = {
            "eff": {a: round(c["arms"][a]["eff_final_mean"], 5) for a in ARMS},
            "delta_exp_eff_vs_maxctrl": round(c["paired"]["exp_eff"]["delta_vs_maxctrl_mean"], 5),
            "delta_exp_ros_vs_maxctrl": round(c["paired"]["exp_ros"]["delta_vs_maxctrl_mean"], 5),
            "delta_exp_or_vs_maxctrl": round(c["paired"]["exp_or"]["delta_vs_maxctrl_mean"], 5),
        }

    # ---- characterization axis 2: demand heterogeneity (the ROS confound) ----
    res["sweep_sigma_demand"] = {}
    for sd in [0.0, 0.25, 0.50, 1.00]:
        p = dict(P); p["SIGMA_DEMAND"] = sd
        c = run_cell(p)
        res["sweep_sigma_demand"][f"{sd:.2f}"] = {
            "eff": {a: round(c["arms"][a]["eff_final_mean"], 5) for a in ARMS},
            "delta_exp_eff_vs_maxctrl": round(c["paired"]["exp_eff"]["delta_vs_maxctrl_mean"], 5),
            "delta_exp_ros_vs_maxctrl": round(c["paired"]["exp_ros"]["delta_vs_maxctrl_mean"], 5),
            "delta_exp_or_vs_maxctrl": round(c["paired"]["exp_or"]["delta_vs_maxctrl_mean"], 5),
        }

    res["wall_sec"] = round(time.time() - t0, 2)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "result.json")
    with open(out, "w") as f:
        json.dump(res, f, indent=2)

    # ---- console ----
    n = nominal
    print(f"[F3 mitophagy QC]  seeds={P['SEEDS']}  wall={res['wall_sec']}s")
    print(f"v0 (dead substrate): eff all-arms = "
          f"{[res['v0_collapsed_cell']['eff'][a] for a in ARMS]}  -> INVALID\n")
    L = n["V1_liveness"]
    print(f"V1 liveness: c1 mean_h={L['c1_mean_h']:.3f} std_h={L['c1_std_h']:.3f} "
          f"oracle_delta={L['oracle_delta_vs_maxctrl']:+.4f}  LIVE={L['LIVE']}\n")
    print(f"{'arm':<11} {'eff_final':>10} {'+-std':>7} {'d vs max(c1,c2)':>16} {'seeds+':>7} {'victim_h':>9}")
    for a in ARMS:
        A = n["arms"][a]
        pr = n["paired"].get(a)
        d = f"{pr['delta_vs_maxctrl_mean']:+.4f}" if pr else "     --"
        sp = f"{pr['n_seeds_positive']}/{len(P['SEEDS'])}" if pr else "  --"
        print(f"{a:<11} {A['eff_final_mean']:>10.4f} {A['eff_final_std']:>7.4f} "
              f"{d:>16} {sp:>7} {A['mean_victim_h']:>9.3f}")
    v = n["validity_random_vs_none"]
    print(f"\nvalidity  c2_random - c1_none = {v['mean']:+.4f} +- {v['std']:.4f}  (must be ~0)")
    print(f"OR-rule: events-with-a-mark = {n['arms']['exp_or']['or_marked_rate']:.3f}  "
          f"mean FRACTION of pool marked = {n['arms']['exp_or']['or_marked_frac']:.3f} "
          f"(-> 1.0 means the absolute thresholds never bind = OR clause is a no-op)")
    for key in ("verdict", "verdict_exp_ros", "verdict_exp_or"):
        V = res[key]
        print(f"VERDICT[{V['arm']:<8}] {V['tier']:<44} "
              f"delta={V['delta_mean']:+.4f} +- {V['delta_std']:.4f} "
              f"seeds+={V['seeds_positive']}/{V['n_seeds']}")
    print(f"\nsigma_obs sweep (delta exp_eff / exp_ros / exp_or vs max ctrl):")
    for k, s in res["sweep_sigma_obs"].items():
        print(f"  sigma={k}: {s['delta_exp_eff_vs_maxctrl']:+.4f} "
              f"{s['delta_exp_ros_vs_maxctrl']:+.4f} {s['delta_exp_or_vs_maxctrl']:+.4f}")
    print(f"sigma_demand sweep (ROS confound):")
    for k, s in res["sweep_sigma_demand"].items():
        print(f"  sd={k}: {s['delta_exp_eff_vs_maxctrl']:+.4f} "
              f"{s['delta_exp_ros_vs_maxctrl']:+.4f} {s['delta_exp_or_vs_maxctrl']:+.4f}")
    print(f"-> {out}")


if __name__ == "__main__":
    main()
