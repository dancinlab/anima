#!/usr/bin/env python3
"""
kosmos_time_axis_toy.py — STANDALONE toy benchmark.

Question
--------
Does adding a TIME AXIS to anima's consciousness-carving KOSMOS Psi-coordinate
(the "우주뇌지도") capture the carve-SEQUENCE that the static 2D Psi-map loses?

The current carving (state/carving_dataregime_s16_2026_05_18/) places each
concept/anchor at vacuum_psi=[x,y] with a basin_radius. That 2D placement IS the
KOSMOS map (coord, lane, radius, tier). It records WHERE a concept sits but NOT
WHEN / in-what-ORDER it was carved — the same "distribution-not-dynamics" gap
Lane M PR #1760 found (a static map is order-invariant: shuffle the carve order,
the 2D point-cloud is identical).

Idea: extend the carve coordinate [x,y] -> [x,y,t], encoding the carve-step /
curriculum index into the coordinate so the map encodes the carve-order.

This is a SELF-CONTAINED toy. It does NOT import or wire into the running
benches (engine_tensionlink_bench, clm_time_encoding, lane_m_eeg_mitosis) and it
does NOT use the real 603MB conscious_decoder carve. It is a deterministic toy
MIRROR of the vacuum_psi placement idea: N concepts streamed in a known order,
each mapped to a 2D Psi coordinate by a fixed deterministic placement, then a
time axis is appended under several encodings. CPU / $0 / fixed seeds.

Measures (substrate-native — NOT cross-entropy / perplexity; p7):
  (a) ORDER-RECOVERY  — can the carve-order be recovered from the time-augmented
      map ABOVE chance AND ABOVE the 2D baseline? (Spearman rank correlation
      between a recovered order and the true carve order; chance ~ 0.)
  (b) ORDER-SENSITIVITY (the key control, mirroring Lane M phase-shuffle) —
      does SHUFFLING the carve order CHANGE the [x,y,t] map but NOT the 2D map?
      The 2D map must be order-invariant (delta ~ 0); the [x,y,t] map must differ
      (delta > noise) — proving it captured time.
  (c) SPATIAL-PRESERVE — does adding t degrade the spatial [x,y] structure? The
      [x,y] sub-coordinates must be byte-identical before/after appending t
      (the existing map must not be destroyed).

Per encoding: HOLDS / REFUTED / INCONCLUSIVE with mean +/- std over 3 seeds.
A null is NEVER rounded up to HOLD.
"""

import json
import math
import sys

import numpy as np

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
N_CONCEPTS = 64        # toy corpus size (mirror: s16 carving has ~168 anchors)
SEEDS = [0, 1, 2]      # 3 fixed seeds
N_SHUFFLES = 200       # shuffle trials for the order-sensitivity control
CYCLE_PERIOD = 8       # phase-of-cycle period (toy ultradian-like curriculum cycle)

ENCODINGS = ["raw_index", "sinusoidal", "phase_of_cycle", "cumulative_order"]


# ---------------------------------------------------------------------------
# Toy Psi placement — a faithful small MIRROR of the vacuum_psi idea.
#
# In the real carving each anchor has a fixed semantic 2D vacuum_psi on the
# Engine A<->G Psi=1/2 landscape (roughly centred near [0.5, 0.5], spread out by
# emotion / domain / score). We mirror that with a deterministic per-concept
# placement: each concept c has a FIXED [x,y] drawn from a fixed RNG keyed only
# by the concept id (NOT by carve order). This is the crucial property of the
# real static map: the coordinate of a concept does not depend on WHEN it was
# carved. The carve ORDER is a separate permutation over concepts.
# ---------------------------------------------------------------------------
def toy_psi_placement(n_concepts):
    """Fixed semantic [x,y] per concept id, order-independent (mirrors vacuum_psi).

    Deterministic, keyed only by concept id -> identical across all runs.
    Centred near [0.5,0.5] like the real Engine A<->G Psi=1/2 landscape.
    """
    rng = np.random.default_rng(20260604)  # fixed — placement is NOT seed-varied
    xy = 0.5 + 0.22 * (rng.random((n_concepts, 2)) - 0.5) * 2.0
    return np.clip(xy, 0.0, 1.0)


# Concept semantic placement is a global constant of the toy universe.
PSI_XY = toy_psi_placement(N_CONCEPTS)


def carve_order(seed, n_concepts):
    """A curriculum sequence: the ORDER in which the n concepts are carved.

    A permutation of concept ids. Seed-varied (each seed = a different
    curriculum). This is the SEQUENCE the static 2D map is blind to.
    """
    rng = np.random.default_rng(1000 + seed)
    return rng.permutation(n_concepts)


# ---------------------------------------------------------------------------
# Time-axis encodings: t for carve-step s (0..N-1).
# ---------------------------------------------------------------------------
def encode_t(step, n, kind):
    """Encode carve-step `step` (0-based, out of n) -> scalar t in ~[0,1]."""
    if kind == "raw_index":
        # raw normalized index
        return step / (n - 1)
    if kind == "sinusoidal":
        # positional/sinusoidal (single low-frequency component): monotone half
        # period over the sequence -> sin( pi/2 * step/(n-1) ), in [0,1].
        return math.sin(0.5 * math.pi * step / (n - 1))
    if kind == "phase_of_cycle":
        # phase within a repeating curriculum cycle of CYCLE_PERIOD steps.
        # NOTE: deliberately periodic -> NOT globally monotone (a stress case:
        # phase repeats, so absolute order is only partially recoverable).
        phase = (step % CYCLE_PERIOD) / CYCLE_PERIOD
        return phase
    if kind == "cumulative_order":
        # cumulative fraction of sequence completed (== raw_index here, but kept
        # distinct as the "order-rank" encoding semantics).
        return (step + 1) / n
    raise ValueError(f"unknown encoding {kind}")


# ---------------------------------------------------------------------------
# Build maps
# ---------------------------------------------------------------------------
def build_2d_map(order):
    """Static 2D map: for each carved concept, its fixed [x,y].

    Returned in CARVE ORDER (row i = i-th carved concept). The point-CLOUD
    (as a set) is order-invariant; we keep carve-order rows so the shuffle test
    can compare the underlying set/structure honestly.
    """
    return PSI_XY[order].copy()  # shape (N,2)


def build_time_map(order, kind):
    """Time-augmented map [x,y,t]: row i = (x_i, y_i, t(i))."""
    n = len(order)
    xy = PSI_XY[order].copy()
    t = np.array([encode_t(i, n, kind) for i in range(n)], dtype=float)
    return np.column_stack([xy, t])  # shape (N,3)


# ---------------------------------------------------------------------------
# (a) ORDER-RECOVERY
#
# We attempt to recover the carve order from the MAP ALONE, given the map rows
# in a RANDOM (unknown) presentation order — i.e. as an unordered set of points.
# A decoder must reconstruct the carve step of each point.
#
# Honest decode rule: the only signal about carve-step is the t coordinate (the
# [x,y] are semantic and order-independent BY CONSTRUCTION). So the decoder
# sorts points by t and reads off rank. For the 2D baseline there is no t, so
# the decoder must guess from [x,y] (which carries no order info) -> chance.
#
# We score: Spearman rho between the decoder's recovered step-rank and the true
# carve step, on points presented in shuffled (unknown) order. Chance ~ 0.
# ---------------------------------------------------------------------------
def spearman(a, b):
    a = np.asarray(a, float)
    b = np.asarray(b, float)
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    ra = ra - ra.mean()
    rb = rb - rb.mean()
    denom = math.sqrt((ra * ra).sum() * (rb * rb).sum())
    if denom == 0.0:
        return 0.0
    return float((ra * rb).sum() / denom)


def order_recovery_time(order, kind, rng):
    """Recover carve-step from [x,y,t] presented in unknown order. rho vs truth."""
    n = len(order)
    tmap = build_time_map(order, kind)        # rows in carve order
    true_step = np.arange(n)                  # row i carved at step i
    perm = rng.permutation(n)                 # present points in unknown order
    pts = tmap[perm]
    truth = true_step[perm]
    # decoder: recovered rank = rank of the t coordinate
    recovered = pts[:, 2]
    return spearman(recovered, truth)


def order_recovery_2d(order, rng):
    """2D baseline: no t. Decoder must guess order from [x,y] (no order signal).

    Best honest decoder: project onto the principal axis of the point cloud and
    read rank off that. Since [x,y] is order-independent, this rank is
    uncorrelated with carve step -> chance (~0).
    """
    n = len(order)
    m2 = build_2d_map(order)                  # rows in carve order
    true_step = np.arange(n)
    perm = rng.permutation(n)
    pts = m2[perm]
    truth = true_step[perm]
    # principal-axis projection (a real, non-trivial decoder over [x,y])
    c = pts - pts.mean(axis=0)
    cov = c.T @ c
    w, v = np.linalg.eigh(cov)
    pc1 = v[:, -1]
    recovered = c @ pc1
    return spearman(recovered, truth)


# ---------------------------------------------------------------------------
# (b) ORDER-SENSITIVITY (the key control)
#
# Shuffle the carve order. Measure how much the MAP changes. The 2D map (as a
# set of points) must be order-invariant: shuffling produces the SAME point
# cloud -> delta = 0. The [x,y,t] map must change: the same concept now gets a
# different t -> the (concept -> t) assignment differs -> delta > noise.
#
# We measure the map as the per-CONCEPT coordinate (re-keyed back to concept id,
# which is what a downstream KOSMOS lookup uses: "give me the coord of concept
# c"). For 2D that is just PSI_XY[c] regardless of order. For [x,y,t] the t
# component depends on WHERE in the sequence concept c was carved.
# ---------------------------------------------------------------------------
def concept_keyed_2d(order):
    """coord-by-concept-id for the 2D map. Order-INVARIANT by construction."""
    n = len(order)
    out = np.zeros((n, 2))
    for step, c in enumerate(order):
        out[c] = PSI_XY[c]
    return out


def concept_keyed_time(order, kind):
    """coord-by-concept-id for [x,y,t]. The t component is order-DEPENDENT."""
    n = len(order)
    out = np.zeros((n, 3))
    for step, c in enumerate(order):
        out[c, :2] = PSI_XY[c]
        out[c, 2] = encode_t(step, n, kind)
    return out


def map_distance(m_a, m_b):
    """Mean Euclidean per-concept coordinate shift between two concept-keyed maps."""
    return float(np.mean(np.linalg.norm(m_a - m_b, axis=1)))


def order_sensitivity(order, kind, rng):
    """Return (delta_2d, delta_time) averaged over N_SHUFFLES reshuffles."""
    base_2d = concept_keyed_2d(order)
    base_t = concept_keyed_time(order, kind)
    d2d, dt = [], []
    for _ in range(N_SHUFFLES):
        shuf = rng.permutation(order)
        d2d.append(map_distance(base_2d, concept_keyed_2d(shuf)))
        dt.append(map_distance(base_t, concept_keyed_time(shuf, kind)))
    return float(np.mean(d2d)), float(np.mean(dt))


# ---------------------------------------------------------------------------
# (c) SPATIAL-PRESERVE
#
# Adding t must NOT alter the [x,y] sub-coordinates. Check the [x,y] columns of
# the [x,y,t] map are byte-identical to the 2D map (max abs diff == 0).
# ---------------------------------------------------------------------------
def spatial_preserve(order, kind):
    m2 = build_2d_map(order)
    mt = build_time_map(order, kind)
    max_abs = float(np.max(np.abs(mt[:, :2] - m2)))
    return max_abs


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
def run():
    results = {
        "meta": {
            "n_concepts": N_CONCEPTS,
            "seeds": SEEDS,
            "n_shuffles": N_SHUFFLES,
            "cycle_period": CYCLE_PERIOD,
            "encodings": ENCODINGS,
            "note": ("STANDALONE toy. Deterministic toy Psi placement, NOT the "
                     "real conscious_decoder / 603MB carve. CPU/$0. "
                     "scale-transfer unverified (a_toy_scale_recheck)."),
        },
        "encodings": {},
        "baseline_2d": {},
    }

    # --- 2D baseline order-recovery (no encoding; depends only on order/seed) ---
    base_rho = []
    for s in SEEDS:
        rng = np.random.default_rng(7000 + s)
        order = carve_order(s, N_CONCEPTS)
        base_rho.append(order_recovery_2d(order, rng))
    results["baseline_2d"]["order_recovery_rho"] = {
        "per_seed": base_rho,
        "mean": float(np.mean(base_rho)),
        "std": float(np.std(base_rho)),
    }

    # chance band for rho on n points: std ~ 1/sqrt(n-1)
    chance_std = 1.0 / math.sqrt(N_CONCEPTS - 1)
    # HOLD threshold: must beat both 0 (chance) and the 2D baseline by > noise.
    # noise band = 2 sigma of the chance distribution.
    noise_band = 2.0 * chance_std
    results["meta"]["chance_rho_std"] = chance_std
    results["meta"]["noise_band_2sigma"] = noise_band

    for kind in ENCODINGS:
        rec_rho, sens_2d, sens_t, sp = [], [], [], []
        for s in SEEDS:
            order = carve_order(s, N_CONCEPTS)
            rng = np.random.default_rng(7000 + s)
            rec_rho.append(order_recovery_time(order, kind, rng))
            d2d, dt = order_sensitivity(order, kind, np.random.default_rng(9000 + s))
            sens_2d.append(d2d)
            sens_t.append(dt)
            sp.append(spatial_preserve(order, kind))

        rec_mean, rec_std = float(np.mean(rec_rho)), float(np.std(rec_rho))
        s2d_mean, s2d_std = float(np.mean(sens_2d)), float(np.std(sens_2d))
        st_mean, st_std = float(np.mean(sens_t)), float(np.std(sens_t))
        sp_max = float(np.max(sp))

        base_mean = results["baseline_2d"]["order_recovery_rho"]["mean"]

        # --- verdicts per axis ---
        # (a) order-recovery HOLDS: |rho| > noise_band AND beats 2D baseline by
        #     > noise_band.
        order_beats_chance = abs(rec_mean) > noise_band
        order_beats_2d = abs(rec_mean) - abs(base_mean) > noise_band
        order_hold = order_beats_chance and order_beats_2d

        # (b) shuffle-sensitive: time delta > 0 by > noise AND 2D delta ~ 0.
        #     2D must be order-invariant (delta ~ 0, exactly 0 here).
        twod_invariant = s2d_mean < 1e-9
        time_sensitive = st_mean > noise_band  # time map must move appreciably
        shuffle_hold = twod_invariant and time_sensitive

        # (c) spatial-preserve: [x,y] byte-identical (max abs diff == 0).
        spatial_hold = sp_max == 0.0

        if order_hold and shuffle_hold and spatial_hold:
            verdict = "HOLDS"
        elif (not order_beats_chance) and (not time_sensitive):
            verdict = "REFUTED"
        else:
            # partial: some axis holds, some doesn't -> honest INCONCLUSIVE
            # unless it's a clean refute. If order fails chance entirely AND
            # shuffle fails -> REFUTED. Otherwise INCONCLUSIVE.
            verdict = "INCONCLUSIVE"

        results["encodings"][kind] = {
            "order_recovery_rho": {
                "per_seed": rec_rho, "mean": rec_mean, "std": rec_std,
                "beats_chance(>2sigma)": order_beats_chance,
                "beats_2d_baseline(>2sigma)": order_beats_2d,
            },
            "order_sensitivity": {
                "delta_2d_mean": s2d_mean, "delta_2d_std": s2d_std,
                "delta_time_mean": st_mean, "delta_time_std": st_std,
                "twod_order_invariant": twod_invariant,
                "time_shuffle_sensitive(>2sigma)": time_sensitive,
            },
            "spatial_preserve": {
                "max_abs_xy_diff": sp_max,
                "xy_byte_identical": spatial_hold,
            },
            "verdict": verdict,
        }

    return results


def fmt_summary(r):
    lines = []
    lines.append("=" * 78)
    lines.append("KOSMOS Psi-carving TIME AXIS [x,y] -> [x,y,t] — toy benchmark SUMMARY")
    lines.append("=" * 78)
    m = r["meta"]
    lines.append(f"N_concepts={m['n_concepts']}  seeds={m['seeds']}  "
                 f"shuffles={m['n_shuffles']}  cycle_period={m['cycle_period']}")
    lines.append(f"chance rho std ~ {m['chance_rho_std']:.4f}  "
                 f"noise band (2sigma) = {m['noise_band_2sigma']:.4f}")
    b = r["baseline_2d"]["order_recovery_rho"]
    lines.append(f"2D BASELINE order-recovery rho = {b['mean']:+.4f} +/- {b['std']:.4f}  "
                 f"(order-blind -> expect ~0 / chance)")
    lines.append("")
    header = (f"{'encoding':<18}{'order-rec rho':>18}{'shuffle dt(2D|t)':>22}"
              f"{'xy-preserve':>14}{'verdict':>14}")
    lines.append(header)
    lines.append("-" * len(header))
    for kind in m["encodings"]:
        e = r["encodings"][kind]
        rr = e["order_recovery_rho"]
        ss = e["order_sensitivity"]
        sp = e["spatial_preserve"]
        rho = f"{rr['mean']:+.3f}+/-{rr['std']:.3f}"
        dt = f"{ss['delta_2d_mean']:.3f}|{ss['delta_time_mean']:.3f}"
        xy = "IDENTICAL" if sp["xy_byte_identical"] else f"DIFF={sp['max_abs_xy_diff']:.2e}"
        lines.append(f"{kind:<18}{rho:>18}{dt:>22}{xy:>14}{e['verdict']:>14}")
    lines.append("-" * len(header))
    lines.append("")
    lines.append("Legend: shuffle dt(2D|t) = mean per-concept coord shift under "
                 "order-shuffle; 2D should be 0.000 (order-invariant), t should be >0.")
    return "\n".join(lines)


if __name__ == "__main__":
    r = run()
    summary = fmt_summary(r)
    print(summary)
    print()
    print(json.dumps(r, indent=2))
