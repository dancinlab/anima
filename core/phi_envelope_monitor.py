"""core/phi_envelope_monitor.py — H_9846 training-time STRUCTURE-ENVELOPE watch (MONITOR-ONLY).

WHAT THIS IS, AND WHAT IT IS EMPHATICALLY NOT
---------------------------------------------
This is a read-only watch over the ENVELOPE/STRUCTURE layer already shipped in
`core/phi_envelope_substrate.py` (envelope_multiscale · collective_phi_nest ·
pe_norm_convexity · phi_smooth_no_cliff). It exists so a training lever that RAISES a
capability number while SHREDDING the substrate's structure is visible as a regression —
the same class of safety net as the G0 non-regression watch.

Two governance rules define its shape, and both are load-bearing:

  a_phi_iit4_tool  — Φ is measured by faithful IIT4 and by nothing else. This module is NOT
                     a Φ estimator, so NOTHING here is named `phi`. The outputs are named for
                     what they arithmetically are: `dispersion` ((max-min)/mean over units),
                     `span` (max/min), `nest_sync` (the class-coupling / (1+variance) term),
                     `nest_scale` (the superadditive sum). Do not relabel them upward.

  a_train_inline_gauge — MONITOR-ONLY, never in the loss. Putting this number in the loss
                     would be the Φ edition of p7: a model optimised to raise a metric makes
                     that metric worthless as evidence. Structurally enforced here, not merely
                     promised: this module imports NO torch, takes plain floats, returns plain
                     dicts, and has no gradient-carrying surface at all. The trainer reads
                     parameter tensors under no_grad and consumes NO RNG draw, so a run with
                     the monitor ON and the same run with it OFF are byte-identical (that
                     equality is the proof obligation, and it is checked in the card).

WHAT IT WATCHES
---------------
Per tick: one scalar per parameter tensor (RMS), sorted by name = the `units` vector. From
that vector we read the structure statistics above. Across ticks, the `dispersion` series is
handed to `phi_smooth_no_cliff`, whose entire job is to answer "was there a cliff?" — the
maximum absolute step-to-step jump.

WHY PARAMETERS AND NOT ACTIVATIONS: an activation tap would need a forward pass, which draws
dropout/RNG state and would silently make ON != OFF. Byte-identity is the only thing that
makes a monitor provably loss-free, so it outranks the richer signal. Stated as a limit in
the card, not hidden here.

THE CADENCE KNOB IS A DEFECT SURFACE, SO IT IS GATED
----------------------------------------------------
`phi_smooth_no_cliff` reads CONSECUTIVE samples, so sampling every N steps instead of every
step mechanically changes the number: coarser sampling merges several small moves into one
big gap. A statistic whose verdict the cadence can flip is a defect in the instrument
(H_9844 hit exactly this with block size). So the shipped battery re-runs BOTH controls at
several cadences (subsampling the planted series) and certifies only if every cadence agrees.
The per-run summary goes further and re-reads its OWN collected series subsampled, so a run
states its cadence-sensitivity instead of inheriting an assumption. MEASURED (H_9846): for a
step-like change `cliff_gap` is near-invariant (0.488390 @cadence 1 → 0.512094 @cadence 20)
while `cliff_rate` swings 19×; the shipped ramp control shows the inversion (gap inflates
3.97× over the same sweep). Neither number is robust in both regimes, so BOTH are always
emitted and the regime label gates nothing.
"""

from math import sqrt

import phi_envelope_substrate as PE     # core/ is on sys.path (same idiom as cli/train.py)

# ── constants (frozen; a knob that can move a verdict does not belong here) ───────────────
NEST_CLASS = 4          # collective_phi_nest class constants: IV = the edge-of-chaos class
                        # (pe_coupling 1.000 / pe_superadd 0.809). Fixed, NOT exposed as a
                        # flag: the class only rescales, and a rescale knob next to a
                        # threshold is a tune-to-green surface.
EPS_STRUCT = 1e-9       # a pedestal reading must be zero to WITHIN FP, not "small"
CADENCES = (1, 2, 4)    # the shipped robustness sweep (subsample factors of the plant series)
PLANT_CLIFF = 0.50      # the planted jump the positive control must recover
FIRE_FACTOR = 5.0       # a fire must clear the pedestal by this factor (mi-screen idiom)


def unit_structure(units):
    """Structure statistics of ONE tick's unit vector (a list of non-negative scalars).

    Returns `dispersion` = pe_norm_convexity(max, min, mean) — 0.0 exactly when every unit is
    identical (a structure-free input), which is what makes the zero-truth pedestal decidable
    rather than a judgement call — plus the `collective_phi_nest` terms, renamed."""
    n = len(units)
    if n == 0:
        return {"n_units": 0, "dispersion": 0.0, "span": 0.0,
                "nest_scale": 0.0, "nest_sync": 0.0, "mean": 0.0}
    mx = max(units)
    mn = min(units)
    mean = sum(units) / float(n)
    nest = PE.collective_phi_nest(units, NEST_CLASS)
    return {
        "n_units": n,
        "dispersion": PE.pe_norm_convexity(mx, mn, mean),
        "span": nest["convexity_span"],
        "nest_scale": nest["phi_collective"],
        "nest_sync": nest["sync"],
        "mean": mean,
    }


def cliff_of_series(series, every):
    """The cliff read of a tick series: the raw max gap AND the per-step rate.

    `phi_smooth_no_cliff` is the whole point of the watch — it literally measures the absence
    of a cliff. `cliff_rate` divides by the sampling cadence so a run sampled every 10 steps
    and a run sampled every step are not compared as if the numbers meant the same thing."""
    gap = PE.phi_smooth_no_cliff(series) if len(series) > 1 else 0.0
    return {"n_ticks": len(series), "every": every,
            "cliff_gap": gap, "cliff_rate": gap / float(every if every else 1)}


# ═══════════════════════════════════════════════════════════════════════════════════════════
# CONTROLS — frozen order: the battery runs BEFORE any real value is read, and a real value
# is refused outright unless both arms certify (positive-control-before-reading-a-negative +
# phi-estimator-needs-zero-truth-pedestal).
# ═══════════════════════════════════════════════════════════════════════════════════════════

def plant_cliff_units(n_units=16, n_ticks=12, jump=PLANT_CLIFF):
    """POSITIVE CONTROL — a tick series with a KNOWN structure cliff planted in it.

    Units are identical (dispersion 0) for the first half; then ONE unit is displaced by
    `jump` in a single tick, so the dispersion moves by an amount fixed entirely by the
    geometry (n_units, jump) and reported back as `plant.cliff_gap`. If the watch cannot
    recover a cliff that was put there on purpose, then a flat reading on a real training run
    says nothing about the run — it says the instrument is blind. That is INSTRUMENT-DEAD,
    and no run number may be read through it."""
    out = []
    for t in range(n_ticks):
        u = [1.0] * n_units
        if t >= n_ticks // 2:
            u[0] = 1.0 + jump
        out.append(u)
    return out


def plant_ramp_units(n_units=16, n_ticks=12, jump=PLANT_CLIFF):
    """DISCRIMINATION CONTROL — the SAME total displacement, spread smoothly over every tick.

    End state is identical to the cliff plant; only the PATH differs. A watch whose whole job
    is "was there a cliff" must rank the ramp strictly below the cliff — otherwise it is
    reading total drift and the word 'cliff' is a lie. This arm is also where the cadence
    hazard becomes visible and quantified instead of assumed away: subsampling merges several
    small ramp steps into one bigger gap, so the ramp's gap INFLATES with cadence. The battery
    reports that inflation factor rather than claiming robustness."""
    out = []
    for t in range(n_ticks):
        u = [1.0] * n_units
        u[0] = 1.0 + jump * (t / float(n_ticks - 1))
        out.append(u)
    return out


def plant_flat_units(n_units=16, n_ticks=12):
    """ZERO-TRUTH PEDESTAL — structure-free input: every unit identical at every tick.

    True value is 0 by construction: (max-min)/mean = 0 and the tick-to-tick gap = 0. If the
    watch returns anything above FP zero here it MANUFACTURES structure, and every number it
    ever printed is uninterpretable → INVALID, stop. (An 'almost zero' pedestal is not a pass:
    the true value is exactly zero, so the tolerance is FP, not taste.)"""
    return [[1.0] * n_units for _ in range(n_ticks)]


def _series(ticks):
    return [unit_structure(u)["dispersion"] for u in ticks]


def battery_liveness(cadences=CADENCES):
    """Run BOTH controls at EVERY cadence and decide whether the watch may be read at all.

    The cadence sweep is not decoration: `phi_smooth_no_cliff` compares consecutive samples,
    so the cadence can change the gap. Certification therefore requires the DECISION (fires /
    refuses) to be cadence-invariant, not just true at the default."""
    plant_full = _series(plant_cliff_units())
    ped_full = _series(plant_flat_units())
    ramp_full = _series(plant_ramp_units())
    arms = []
    for c in cadences:
        pr = cliff_of_series(plant_full[::c], c)
        zr = cliff_of_series(ped_full[::c], c)
        rr = cliff_of_series(ramp_full[::c], c)
        arms.append({
            "cadence": c,
            "plant": pr, "pedestal": zr, "ramp": rr,
            "plant_fires": bool(pr["cliff_gap"] > FIRE_FACTOR * EPS_STRUCT),
            "pedestal_refuses": bool(zr["cliff_gap"] <= EPS_STRUCT),
            "discriminates_ramp": bool(rr["cliff_gap"] < pr["cliff_gap"]),
        })
    # the pedestal is also read on the STRUCTURE side, not only the cliff side: a
    # structure-free unit vector must give dispersion 0 and span 1 exactly.
    ped_struct = unit_structure([1.0] * 16)
    struct_clean = bool(abs(ped_struct["dispersion"]) <= EPS_STRUCT
                        and abs(ped_struct["span"] - 1.0) <= EPS_STRUCT)
    plant_struct = unit_structure(plant_cliff_units()[-1])
    struct_fires = bool(plant_struct["dispersion"] > FIRE_FACTOR * EPS_STRUCT)

    plant_fires = all(a["plant_fires"] for a in arms) and struct_fires
    pedestal_refuses = all(a["pedestal_refuses"] for a in arms) and struct_clean
    discriminates = all(a["discriminates_ramp"] for a in arms)
    # cadence-robustness: the DECISION must hold at every cadence, and the spread is reported
    # so a cadence-fragile read is visible even when the decision survives. `ramp_inflation` is
    # the honest cost of coarse sampling: the same smooth drift reads as a bigger gap when
    # subsampled, so two runs are comparable only at the SAME cadence.
    gaps = [a["plant"]["cliff_gap"] for a in arms]
    ramp_gaps = [a["ramp"]["cliff_gap"] for a in arms]
    spread = max(gaps) - min(gaps)
    inflation = (max(ramp_gaps) / ramp_gaps[0]) if ramp_gaps and ramp_gaps[0] > 0 else 0.0
    if not plant_fires:
        status, why = "INSTRUMENT-DEAD", (
            "the planted structure cliff was NOT recovered at every cadence — a flat reading "
            "on a training run would then be a property of the watch, not of the run.")
    elif not pedestal_refuses:
        status, why = "INVALID", (
            "the structure-free pedestal read above FP zero — the watch MANUFACTURES "
            "structure, so no value it emits is interpretable.")
    elif not discriminates:
        status, why = "INVALID", (
            "a smooth ramp with the SAME total displacement scored at or above the planted "
            "cliff — the statistic is reading total drift, not a cliff.")
    else:
        status, why = "CERTIFIED", (
            "planted cliff recovered at every cadence, structure-free pedestal read exactly "
            "zero on both the structure and the cliff side, and a same-endpoint smooth ramp "
            "ranked strictly below the cliff at every cadence.")
    return {
        "arms": arms,
        "pedestal_structure": ped_struct, "plant_structure": plant_struct,
        "plant_fires": plant_fires, "pedestal_refuses": pedestal_refuses,
        "discriminates_ramp": discriminates,
        "plant_gap_spread_over_cadences": spread,
        "ramp_cadence_inflation": inflation,
        "certified": bool(plant_fires and pedestal_refuses and discriminates),
        "status": status, "why": why,
    }


def summarize(ticks, every, battery):
    """Fold the per-tick records into the run summary. Refuses to emit values uncertified."""
    if not battery.get("certified"):
        return {"instrument": "phi-envelope-monitor", "hypothesis": "H_9846",
                "status": battery.get("status"), "why": battery.get("why"),
                "battery": battery, "ticks": [], "read": None,
                "note": "no run value is reported through an uncertified watch."}
    series = [t["dispersion"] for t in ticks]
    cliff = cliff_of_series(series, every)
    # ── the run's OWN cadence-sensitivity, for free: re-read the collected series subsampled.
    #    MEASURED (H_9846, 20-step CPU run): cliff_gap 0.488390 @every=1 → 0.512094 @every=20
    #    (4.8% spread) while cliff_rate moved 0.48839 → 0.02560, a 19× swing. So for a STEP-like
    #    change the GAP is the cadence-robust statistic and the RATE is the fragile one; for a
    #    RAMP-like change it is the other way round (the shipped ramp control measures exactly
    #    that inversion: 3.97× gap inflation over the same cadence sweep). Neither statistic is
    #    robust in both regimes, so the regime is REPORTED rather than assumed — and the label
    #    gates nothing: both numbers are always emitted, so no threshold can flip a verdict.
    subs = {}
    for f in (1, 2, 4):
        if len(series[::f]) >= 2:
            subs[str(f)] = cliff_of_series(series[::f], every * f)
    sub_gaps = [v["cliff_gap"] for v in subs.values()]
    top = max(sub_gaps) if sub_gaps else 0.0
    spread_rel = ((top - min(sub_gaps)) / top) if top > 0 else 0.0
    regime = ("step-like (gap cadence-robust; read cliff_gap)" if spread_rel <= 0.25
              else "ramp-like (gap inflates with cadence; read cliff_rate)")
    return {
        "instrument": "phi-envelope-monitor", "hypothesis": "H_9846",
        "engine": "core/phi_envelope_substrate.py (structure/envelope layer)",
        "status": "CERTIFIED", "why": battery.get("why"),
        "battery": battery,
        "every": every, "n_ticks": len(ticks),
        "ticks": ticks,
        "cliff": cliff,
        "cliff_by_subsample": subs,
        "cliff_gap_spread_rel": spread_rel,
        "regime": regime,
        "read": ("MONITOR-ONLY, never in the loss (a_train_inline_gauge). These are ENVELOPE/"
                 "STRUCTURE statistics of the parameter tensors, NOT Φ (a_phi_iit4_tool): "
                 "`dispersion` = (max-min)/mean over per-tensor RMS, `cliff_gap` = the largest "
                 "tick-to-tick jump in that dispersion. Read the TRAJECTORY within one run, and "
                 "compare two runs only at the SAME --phi-monitor-every. The cliff statistic is "
                 "a consecutive-sample statistic, so cadence matters — and WHICH of the two "
                 "numbers is the robust one depends on the regime, which is why the run reports "
                 "its own `cliff_by_subsample`/`regime` instead of assuming: for a step-like "
                 "change the GAP is near-invariant and the RATE swings; for a ramp-like change "
                 "the gap inflates with cadence and the rate is the stable one. A cliff is a "
                 "REGRESSION signal regardless of any capability gain; it is NOT a capability "
                 "score and never a verdict."),
    }


def sqrt_mean_square(values):
    """RMS of a flat list — the per-tensor scalar the trainer feeds in as one `unit`."""
    n = len(values)
    if n == 0:
        return 0.0
    return sqrt(sum(v * v for v in values) / float(n))
