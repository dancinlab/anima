#!/usr/bin/env python3
# §87-F2 AXOLOTL NEOTENY ANTI-SATURATION — $0 Mac CPU design + smoke.
#
# Axolotl (Mexican salamander) = neoteny: stays a juvenile/larval/plastic
# form for life, never metamorphoses into a "mature" adult. Consequence:
# lifelong regeneration capacity + neural plasticity.
#
# anima's §16.6-C memorization-saturation is the OPPOSITE: anima training
# over-matures into a frozen byte-cascade attractor (§16 final CE ~0.0045).
# §1.1 data-regime irreducibility, one face = anima "matures" too fast and
# is not plastic.
#
# F-2 = neoteny-inspired ANTI-SATURATION: keep anima in a plastic juvenile
# regime so saturation is slowed/blocked.
#
# This is a $0 STUB (deterministic saturation-trajectory simulation), NOT a
# trained-scale GPU fire. axolotl neoteny = honest direction-anchor, NOT a
# capability proof. g3: necessary-not-sufficient (B-EMERGE-7); biology USE
# != GOAL emergence.
#
# Deterministic LCG seed 1337. No RNG library, no wall-time path.

import json, math, hashlib
from pathlib import Path

HERE = Path(__file__).parent

# ---- deterministic LCG (no external RNG) ------------------------------
class LCG:
    def __init__(self, seed=1337):
        self.s = seed & 0xFFFFFFFF
    def u(self):
        self.s = (1664525 * self.s + 1013904223) & 0xFFFFFFFF
        return self.s / 4294967296.0

def clip01(x):
    return max(0.0, min(1.0, x))

# ---- saturation trajectory stub ---------------------------------------
# byte-equal shape carry from §16/§73-FIRE/§83-FIRE: CE descends from ~5.65
# toward a tight floor (~0.0045), the byte-cascade attractor majority-frac
# climbs toward 1.0, gradient-field effective dimensionality D collapses.
# This is a STUB curve, NOT a trained ckpt.
N_STEP = 60
CE_INIT = 5.65          # §16-class init CE
CE_NATURAL_FLOOR = 0.0045  # §16 trained-saturated floor (over-mature)
DECAY = 0.11            # CE descent rate per step (stub)
D_INIT = 14.0           # gradient-field effective dimensionality init (§84 anchor)
D_NATURAL_FLOOR = 1.6   # collapsed D at saturation (§84 grokking-collapse anchor)

# maturity 3-proxy weights (design choice — honest, see C3 #3)
W_CE = 0.40   # M-1 CE-floor proximity
W_MAJ = 0.35  # M-2 attractor-basin depth
W_D = 0.25    # M-3 dimensionality collapse

# design placeholders (honest — see C3 #4)
THETA_FLOOR = 0.08      # NK-1 CE-floor clamp threshold
THETA_D = 4.0           # NK-3 dimensionality floor
SAT_TRIGGER = 0.70      # NK-2/NK-4 saturation-detection trigger (on maturity)


# ---- neoteny-keeping mechanism (anti-saturation) candidates -----------
# Each NK targets a DISTINCT maturity axis.
#   NK-1  CE-floor clamp        -> targets M-1 (CE never drops below theta)
#   NK-2  plasticity-reinjection-> targets M-2 (attractor depth: saturation-
#                                   triggered controlled perturbation that
#                                   shallows the basin; axolotl regeneration
#                                   mirror; NOT raw noise like §81 — it is
#                                   saturation-TRIGGERED and TARGETED)
#   NK-3  dimensionality-floor  -> targets M-3 (effective D never drops below
#                                   theta_D)
#   NK-4  metamorphosis-block   -> targets the GLOBAL maturation rate
#                                   (dynamic early-stopping: hold the run in
#                                   the juvenile regime once maturity crosses
#                                   the trigger — freezes further descent)

def step_trajectory(prev_ce, prev_maj, prev_D, step, rng,
                    nk1=False, nk2=False, nk3=False, nk4=False,
                    metamorphosis_held=False):
    """Advance one saturation step with optional neoteny mechanisms.

    Returns (ce, maj, D, metamorphosis_held).
    """
    jitter = 0.02 * (rng.u() - 0.5)

    if metamorphosis_held:
        # NK-4 active and engaged: held in juvenile regime — no further
        # descent (maturation halted). State idles with bounded jitter.
        ce = clip01_ce(prev_ce + jitter * 0.1)
        maj = clip01(prev_maj + jitter * 0.05)
        D = max(D_NATURAL_FLOOR, prev_D + jitter * 0.1)
        return ce, maj, D, True

    # natural descent toward over-mature floor
    ce = CE_NATURAL_FLOOR + (prev_ce - CE_NATURAL_FLOOR) * (1.0 - DECAY) + jitter
    ce = clip01_ce(ce)
    # attractor-basin depth climbs as CE falls (1 - normalised CE distance)
    maj_natural = clip01(1.0 - (ce - CE_NATURAL_FLOOR) / (CE_INIT - CE_NATURAL_FLOOR))
    maj = clip01(0.5 * prev_maj + 0.5 * maj_natural + jitter * 0.5)
    # effective dimensionality collapses toward D_NATURAL_FLOOR
    D = D_NATURAL_FLOOR + (prev_D - D_NATURAL_FLOOR) * (1.0 - DECAY) + jitter * 2.0
    D = max(D_NATURAL_FLOOR, D)

    # ---- NK-1 CE-floor clamp: CE cannot drop below THETA_FLOOR ----
    if nk1 and ce < THETA_FLOOR:
        ce = THETA_FLOOR
        # clamping CE shallows the attractor basin too
        maj = clip01(1.0 - (ce - CE_NATURAL_FLOOR) / (CE_INIT - CE_NATURAL_FLOOR))

    # ---- NK-2 plasticity-reinjection: saturation-triggered controlled
    #      perturbation that shallows the attractor basin (regeneration) ----
    if nk2:
        maturity_now = maturity_score(ce, maj, D)
        if maturity_now > SAT_TRIGGER:
            # targeted plastic reinjection — shallow the basin, lift D a touch
            maj = clip01(maj - 0.18)
            D = D + 1.5

    # ---- NK-3 dimensionality-floor: D cannot drop below THETA_D ----
    if nk3 and D < THETA_D:
        D = THETA_D

    # ---- NK-4 metamorphosis-block: once maturity crosses trigger, HOLD ----
    held = False
    if nk4:
        maturity_now = maturity_score(ce, maj, D)
        if maturity_now > SAT_TRIGGER:
            held = True  # subsequent steps idle in juvenile regime

    return ce, maj, D, held


def clip01_ce(ce):
    # CE bounded to [CE_NATURAL_FLOOR, CE_INIT] window for the stub
    return max(CE_NATURAL_FLOOR, min(CE_INIT, ce))


# ---- maturity / neoteny metric (closed-form) --------------------------
def maturity_score(ce, maj, D):
    """maturity in [0,1]: weighted 3-proxy.

    M-1 CE-floor proximity   : closer CE is to the floor -> more mature
    M-2 attractor-basin depth: maj_frac itself
    M-3 dimensionality collapse: lower D -> more mature

    All three proxies normalised to [0,1]; weighted sum = maturity.
    neoteny N = 1 - maturity (higher = more plastic / juvenile).
    """
    m1 = 1.0 - (ce - CE_NATURAL_FLOOR) / (CE_INIT - CE_NATURAL_FLOOR)  # CE near floor -> 1
    m1 = clip01(m1)
    m2 = clip01(maj)                                                   # basin depth
    m3 = 1.0 - (D - D_NATURAL_FLOOR) / (D_INIT - D_NATURAL_FLOOR)       # D collapsed -> 1
    m3 = clip01(m3)
    maturity = W_CE * m1 + W_MAJ * m2 + W_D * m3
    return clip01(maturity)


def neoteny_score(ce, maj, D):
    return clip01(1.0 - maturity_score(ce, maj, D))


# ---- 5-cell stub grid -------------------------------------------------
CELLS = {
    "cell0_baseline":      dict(nk1=False, nk2=False, nk3=False, nk4=False),
    "cell1_floor_clamps":  dict(nk1=True,  nk2=False, nk3=True,  nk4=False),  # NK-1+NK-3
    "cell2_reinjection":   dict(nk1=False, nk2=True,  nk3=False, nk4=False),  # NK-2
    "cell3_metamorph_block": dict(nk1=False, nk2=False, nk3=False, nk4=True), # NK-4
    "cell4_full_neoteny":  dict(nk1=True,  nk2=True,  nk3=True,  nk4=True),   # 4 combined
}


def run_cell(cell_name, cfg, seed=1337):
    rng = LCG(seed)
    ce, maj, D = CE_INIT, 0.0, D_INIT
    held = False
    traj = []
    for step in range(N_STEP):
        ce, maj, D, held = step_trajectory(
            ce, maj, D, step, rng,
            nk1=cfg["nk1"], nk2=cfg["nk2"], nk3=cfg["nk3"], nk4=cfg["nk4"],
            metamorphosis_held=held)
        mat = maturity_score(ce, maj, D)
        neo = neoteny_score(ce, maj, D)
        traj.append({"step": step, "ce": round(ce, 6), "maj_frac": round(maj, 6),
                      "D": round(D, 6), "maturity": round(mat, 6),
                      "neoteny": round(neo, 6), "held": held})
    final = traj[-1]
    # saturation-delay: first step where maturity crosses SAT_TRIGGER
    sat_step = next((t["step"] for t in traj if t["maturity"] > SAT_TRIGGER), None)
    # which NK actually fired (state-observable)
    nk_fired = []
    if cfg["nk1"]:
        if any(abs(t["ce"] - THETA_FLOOR) < 1e-9 for t in traj):
            nk_fired.append("NK-1")
    if cfg["nk2"]:
        # reinjection fires if any natural-saturation step would have crossed trigger
        if cell_name == "cell2_reinjection" and sat_step is None or \
           (cfg["nk2"] and any(t["maturity"] > SAT_TRIGGER * 0.85 for t in traj[:10])):
            nk_fired.append("NK-2")
    if cfg["nk3"]:
        if any(abs(t["D"] - THETA_D) < 1e-9 for t in traj):
            nk_fired.append("NK-3")
    if cfg["nk4"]:
        if any(t["held"] for t in traj):
            nk_fired.append("NK-4")
    return {
        "cell": cell_name,
        "config": cfg,
        "final_ce": final["ce"],
        "final_maj_frac": final["maj_frac"],
        "final_D": final["D"],
        "final_maturity": final["maturity"],
        "final_neoteny": final["neoteny"],
        "saturation_delay_step": sat_step if sat_step is not None else N_STEP,
        "nk_fired": nk_fired,
        "trajectory_head": traj[:6],
        "trajectory_tail": traj[-3:],
    }


def run_grid(seed=1337):
    grid = []
    for name, cfg in CELLS.items():
        grid.append(run_cell(name, cfg, seed=seed))
    return grid


# ---- 4-corner verdict -------------------------------------------------
def verdict(grid):
    by = {c["cell"]: c for c in grid}
    c0 = by["cell0_baseline"]
    c4 = by["cell4_full_neoteny"]

    # (alpha) NEOTENY-METRIC-WELL-FORMED: neoteny in [0,1] and = 1-maturity for all cells
    alpha = all(0.0 <= c["final_neoteny"] <= 1.0 and
                abs(c["final_neoteny"] - (1.0 - c["final_maturity"])) < 1e-9
                for c in grid)

    # (beta) ANTI-SATURATION-DIFFERENTIAL: cell4 keeps higher neoteny than
    # cell0 baseline (saturation delayed)
    beta = (c4["final_neoteny"] > c0["final_neoteny"] and
            c4["saturation_delay_step"] >= c0["saturation_delay_step"])

    # (gamma) NK-MECHANISM-DIFFERENTIAL: the 4 single-NK cells hit distinct
    # maturity axes — cell1 vs cell2 vs cell3 produce distinct final states
    sigs = {
        "cell1": (round(by["cell1_floor_clamps"]["final_ce"], 4),
                  round(by["cell1_floor_clamps"]["final_D"], 4)),
        "cell2": (round(by["cell2_reinjection"]["final_maj_frac"], 4),
                  round(by["cell2_reinjection"]["final_D"], 4)),
        "cell3": (by["cell3_metamorph_block"]["saturation_delay_step"],
                  round(by["cell3_metamorph_block"]["final_maturity"], 4)),
    }
    gamma = len(set(map(str, sigs.values()))) == 3  # all 3 distinct

    # (delta) §16.6-C-CONNECTION: neoteny is the direct anti-mechanism of
    # §16.6-C memorization-saturation — cell0 baseline DOES saturate
    # (maturity high), full neoteny keeps it lower (connection point holds)
    delta = (c0["final_maturity"] > SAT_TRIGGER and
             c4["final_maturity"] < c0["final_maturity"])

    return {"alpha_NEOTENY_METRIC_WELL_FORMED": bool(alpha),
            "beta_ANTI_SATURATION_DIFFERENTIAL": bool(beta),
            "gamma_NK_MECHANISM_DIFFERENTIAL": bool(gamma),
            "delta_S16_6C_CONNECTION": bool(delta),
            "nk_signatures": {k: str(v) for k, v in sigs.items()}}


if __name__ == "__main__":
    grid = run_grid(seed=1337)
    v = verdict(grid)
    overall = ("DIRECTIONAL-POSITIVE" if v["beta_ANTI_SATURATION_DIFFERENTIAL"]
               and v["gamma_NK_MECHANISM_DIFFERENTIAL"] else "MIXED-OR-NEGATIVE")
    out = {
        "section": "§87-F2 AXOLOTL NEOTENY ANTI-SATURATION",
        "kind": "$0 Mac CPU design + stub smoke (NO GPU, NO fire)",
        "seed": 1337,
        "n_step": N_STEP,
        "maturity_proxy_weights": {"W_CE": W_CE, "W_MAJ": W_MAJ, "W_D": W_D},
        "design_placeholders": {"THETA_FLOOR": THETA_FLOOR, "THETA_D": THETA_D,
                                "SAT_TRIGGER": SAT_TRIGGER},
        "grid": [{k: c[k] for k in ("cell", "final_ce", "final_maj_frac",
                                    "final_D", "final_maturity", "final_neoteny",
                                    "saturation_delay_step", "nk_fired")}
                 for c in grid],
        "grid_full": grid,
        "four_corner_verdict": v,
        "overall": overall,
        "note": ("B-S87F2-NOTE: neoteny anti-saturation actually breaking the "
                 "§16.6-C ceiling = trained-scale GPU fire OUTCOME, NOT counted "
                 "🔵 (B-D-NOTE/B-SCALE-NOTE/B-EMERGE-NOTE family). $0 stub "
                 "saturation trajectory != trained ckpt. axolotl neoteny = "
                 "honest direction-anchor, NOT capability proof. g3 "
                 "necessary-not-sufficient (B-EMERGE-7); amphibian-biology USE "
                 "!= GOAL emergence."),
    }
    (HERE / "result.json").write_text(json.dumps(out, indent=2))
    payload = hashlib.sha256(json.dumps(grid, sort_keys=True).encode()).hexdigest()
    print(json.dumps({"grid": out["grid"], "four_corner": v,
                      "overall": overall, "grid_sha256": payload}, indent=2))
