#!/usr/bin/env python3
# ==========================================================================
# Lane M — "EEG-grown CLM via mitosis"  (TOY bench · CPU · $0)
#
# A NEW LANE for anima, DISTINCT from Lane A (AKIDA on-chip) / Lane G (forge
# GPU CE-descent) / Lane P (py+CUDA gradient). Lane M is the GRADIENT-FREE
# GROWTH lane: an EMPTY CLM (0 trained weights) is GROWN by MITOSIS cell-
# division driven by a 5-channel synthetic-EEG tension-link. There is NO
# backprop, NO CE loss, NO gradient anywhere (p8 "NO TRAIN/INFER SPLIT" —
# inference mitosis IS the learning). The grown TOPOLOGY is a *recording* of
# the EEG stream: not stored as data, but as grown structure.
#
# Architecture mirrored from the repo (faithful, not invented):
#   - 5-band synthetic EEG signatures  : EEG/eeg_backend.hexa
#       eeg_sw_band_power_{resting,sleep_n3,rem,active}
#       resting  delta .20 theta .15 alpha .40 beta .20 gamma .05
#       n3       delta .70 theta .15 alpha .05 beta .05 gamma .05
#       rem      delta .20 theta .30 alpha .10 beta .25 gamma .15
#       active   delta .10 theta .10 alpha .15 beta .40 gamma .25
#   - gamma>0.20 -> MITOSIS split signal : EEG/impl/H_681 L12 (_l12_mitosis_split_trigger)
#   - 5-ch tension-link carrier          : models/archive-legacy/tension_link.hexa
#       channels = [alpha, theta, gamma, 1-delta, beta]  (per task spec)
#   - mitosis split mechanics            : models/archive-legacy/mitosis.hexa
#       SPLIT_NOISE_FLOOR=0.1 (symmetry break), patience-gated split,
#       MIN_CELLS=2, MAX_CELLS cap, daughter inherits parent state + noise,
#       phi-proxy conservation (DD55) as the stability anchor.
#
# §97 HONEST LINE: the grown CLM here is a RECORDING ARTIFACT (measurement
# anchor, legitimate per §97). It MUST NOT drive anima's emission/decision.
# This bench only ever READS the grown topology to reconstruct the EEG; no
# grown-CLM output is ever fed to anima's speech/decision path. Keeping it a
# recording-only artifact is what keeps it out of being a §97 GOAL-
# ILLEGITIMATE command channel.
#
# Measure (substrate-native — RECORDING fidelity, NOT CE / perplexity, p7):
#   M1 FIDELITY          : decode the EEG stream FROM the grown topology;
#                          reconstruction error must beat a chance floor.
#   M2 MITOSIS-vs-CONTROL: EEG-driven growth must beat BOTH
#                          (a) EEG-blind random growth, and
#                          (b) phase-shuffled-EEG growth, by > seed-noise.
#   M3 STABILITY         : cell count stays bounded (no explosion / collapse
#                          to <MIN_CELLS), tension stays finite.
#   3 seeds; mean +- seed-std (noise band). HOLDS / REFUTED / INCONCLUSIVE.
#
# Pure stdlib (no numpy) so it runs anywhere, CPU, $0, fully deterministic.
# ==========================================================================

import json, math, os, sys, random

# ---- constants mirrored from mitosis.hexa --------------------------------
SPLIT_NOISE_FLOOR = 0.1     # symmetry-break perturbation on daughter state
MIN_CELLS         = 2       # CB1 invariant
MAX_CELLS         = 64      # toy cell budget (honest small budget)
GAMMA_SPLIT_THR   = 0.20    # L12: gamma>0.20 -> MITOSIS split signal
SPLIT_PATIENCE    = 1       # toy: single-tick trigger (L12 is event-level)
N_CHANNELS        = 5       # tension-link 5-ch
STREAM_LEN        = 240     # EEG ticks per run (toy)
DD55_TOL          = 0.10    # phi-proxy conservation tolerance

# ---- canonical 5-band EEG signatures (EEG/eeg_backend.hexa) --------------
# order: delta, theta, alpha, beta, gamma
BAND_SIG = {
    "resting": dict(delta=0.20, theta=0.15, alpha=0.40, beta=0.20, gamma=0.05),
    "n3":      dict(delta=0.70, theta=0.15, alpha=0.05, beta=0.05, gamma=0.05),
    "rem":     dict(delta=0.20, theta=0.30, alpha=0.10, beta=0.25, gamma=0.15),
    "active":  dict(delta=0.10, theta=0.10, alpha=0.15, beta=0.40, gamma=0.25),
}
STAGES = ["resting", "n3", "rem", "active"]


def tension_link_5ch(bp):
    """5-ch tension-link carrier = [alpha, theta, gamma, 1-delta, beta] (task spec)."""
    return [bp["alpha"], bp["theta"], bp["gamma"], 1.0 - bp["delta"], bp["beta"]]


# ==========================================================================
# Synthetic EEG generator — DETERMINISTIC per seed. NOT real EEG hardware.
# A stage schedule (resting->rem->active->n3 cycling) + small band jitter.
# ==========================================================================
def gen_eeg_stream(seed, n=STREAM_LEN, jitter=0.03):
    rng = random.Random(seed * 1000 + 17)
    stream = []
    # deterministic stage schedule: blocks of 30 ticks cycling the 4 stages,
    # so gamma rises/falls in a structured (decodable) pattern.
    schedule = []
    block = 30
    si = 0
    while len(schedule) < n:
        schedule += [STAGES[si % len(STAGES)]] * block
        si += 1
    schedule = schedule[:n]
    for t in range(n):
        stage = schedule[t]
        base = BAND_SIG[stage]
        bp = {}
        for k, v in base.items():
            x = v + rng.uniform(-jitter, jitter)
            bp[k] = max(0.0, x)
        # renormalize bands to sum 1 (relative band power)
        s = sum(bp.values())
        if s > 0:
            bp = {k: v / s for k, v in bp.items()}
        stream.append((stage, bp))
    return stream


def phase_shuffle_stream(stream, seed):
    """Control (b): phase-shuffled EEG. Same marginal band-power distribution
    (identical multiset of band vectors) but temporal order destroyed — so the
    *dynamics* the structure could encode are scrambled while statistics match."""
    rng = random.Random(seed * 7919 + 3)
    idx = list(range(len(stream)))
    rng.shuffle(idx)
    return [stream[i] for i in idx]


# ==========================================================================
# The grown CLM. ONE seed cell. Each cell carries a 5-ch tension STATE
# (mirrors Cell.hidden / tension state). On a gamma-split event the highest-
# tension cell undergoes MITOSIS: a daughter is born inheriting the parent
# tension state + SPLIT_NOISE_FLOOR symmetry-break, and the daughter's state
# is SPECIALIZED toward the EEG vector at that moment (the "recording" write).
# NO gradient. The grown set of cell tension-states IS the recording.
# ==========================================================================
class Cell:
    __slots__ = ("cid", "state", "born_tick", "tension_hist")
    def __init__(self, cid, state, born_tick):
        self.cid = cid
        self.state = list(state)          # 5-ch tension state
        self.born_tick = born_tick
        self.tension_hist = []


def _tension(cell, drive):
    """Inter-channel tension scalar = mean sq mismatch between cell state and
    the incoming 5-ch EEG drive (mirrors tension = mean(output^2) idea)."""
    return sum((cell.state[i] - drive[i]) ** 2 for i in range(N_CHANNELS)) / N_CHANNELS


def grow(stream, seed, mode):
    """Grow the network over the EEG stream.
       mode = 'eeg'      : gamma-driven mitosis (the Lane M method)
              'random'   : EEG-blind growth (control a) — split on a coin flip,
                           daughter state = random (structure ignores the EEG)
              'shuffled' : same as 'eeg' but stream is phase-shuffled (control b)
    """
    rng = random.Random(seed * 131 + (0 if mode == "eeg" else 53 if mode == "random" else 97))
    # seed ONE cell (empty CLM = 0 trained weights; state starts neutral)
    cells = [Cell(0, [0.5] * N_CHANNELS, 0)]
    next_id = 1
    growth_curve = []
    tension_trace = []

    for t, (stage, bp) in enumerate(stream):
        drive = tension_link_5ch(bp)
        # update every cell's tension vs the incoming drive + nudge state
        for c in cells:
            tn = _tension(c, drive)
            c.tension_hist.append(tn)
            if len(c.tension_hist) > 20:
                c.tension_hist.pop(0)

        # decide split
        do_split = False
        if mode == "random":
            # EEG-blind: split with a fixed probability matched to the EEG
            # gamma>thr base rate (so total cell budget is comparable), but the
            # decision and the daughter state ignore the EEG entirely.
            do_split = rng.random() < 0.27
        else:
            gamma = bp["gamma"]
            do_split = gamma > GAMMA_SPLIT_THR   # L12 trigger

        if do_split and len(cells) < MAX_CELLS:
            # pick the highest-tension cell to divide (patience-gated)
            cand = max(cells, key=lambda c: (c.tension_hist[-1] if c.tension_hist else 0.0))
            if len(cand.tension_hist) >= SPLIT_PATIENCE:
                if mode == "random":
                    # daughter state = pure noise, NOT the EEG (EEG-blind)
                    dstate = [rng.uniform(0.0, 1.0) for _ in range(N_CHANNELS)]
                else:
                    # daughter SPECIALIZES toward the EEG drive at this moment
                    # (the recording write) + symmetry-break noise floor
                    dstate = [
                        drive[i] + rng.uniform(-SPLIT_NOISE_FLOOR, SPLIT_NOISE_FLOOR)
                        for i in range(N_CHANNELS)
                    ]
                cells.append(Cell(next_id, dstate, t))
                next_id += 1

        growth_curve.append(len(cells))
        # phi-proxy = mean pairwise state spread (cells must stay differentiated)
        tension_trace.append(_phi_proxy(cells))

    return cells, growth_curve, tension_trace


def _phi_proxy(cells):
    """Phi proxy = mean pairwise L2 distance of cell states * log(n+1).
       Mirrors mitosis.hexa PhiProxy = mean_cosine_distance * log(n+1)."""
    n = len(cells)
    if n < 2:
        return 0.0
    tot, cnt = 0.0, 0
    for i in range(n):
        for j in range(i + 1, n):
            d = math.sqrt(sum((cells[i].state[k] - cells[j].state[k]) ** 2
                              for k in range(N_CHANNELS)))
            tot += d
            cnt += 1
    return (tot / cnt) * math.log(n + 1)


# ==========================================================================
# M1 / M2 — RECORDING FIDELITY: reconstruct the EEG stream FROM the grown
# topology. Read-out: for each EEG tick, the grown structure votes its closest
# cell state; we measure how well the per-tick 5-ch EEG drive is reconstructed
# by the nearest grown cell state (nearest-prototype decode). Lower error =
# the structure encodes the EEG better.
#
# Reconstruction error = mean over ticks of min-over-cells ||drive - state||^2
# (a codebook / vector-quantization reconstruction error). Chance floor =
# same metric using a fixed neutral codebook (no growth).
# ==========================================================================
def reconstruct_error(cells, stream):
    if not cells:
        return float("inf")
    errs = []
    for stage, bp in stream:
        drive = tension_link_5ch(bp)
        best = min(
            sum((c.state[i] - drive[i]) ** 2 for i in range(N_CHANNELS)) / N_CHANNELS
            for c in cells
        )
        errs.append(best)
    return sum(errs) / len(errs)


def chance_floor_error(stream):
    """Floor: single neutral prototype [0.5]*5 (an un-grown empty CLM)."""
    neutral = [0.5] * N_CHANNELS
    errs = []
    for stage, bp in stream:
        drive = tension_link_5ch(bp)
        errs.append(sum((neutral[i] - drive[i]) ** 2 for i in range(N_CHANNELS)) / N_CHANNELS)
    return sum(errs) / len(errs)


# ==========================================================================
# Drivers
# ==========================================================================
def run_seed(seed):
    stream = gen_eeg_stream(seed)
    shuffled = phase_shuffle_stream(stream, seed)

    eeg_cells, eeg_curve, eeg_phi = grow(stream, seed, "eeg")
    rnd_cells, rnd_curve, rnd_phi = grow(stream, seed, "random")
    shf_cells, shf_curve, shf_phi = grow(shuffled, seed, "shuffled")

    floor = chance_floor_error(stream)
    # all reconstructions are scored against the TRUE (un-shuffled) stream:
    # the question is "does the grown structure record the real EEG?"
    err_eeg = reconstruct_error(eeg_cells, stream)
    err_rnd = reconstruct_error(rnd_cells, stream)
    err_shf = reconstruct_error(shf_cells, stream)

    return {
        "seed": seed,
        "floor_error": floor,
        "err_eeg": err_eeg,
        "err_random": err_rnd,
        "err_shuffled": err_shf,
        "cells_eeg": len(eeg_cells),
        "cells_random": len(rnd_cells),
        "cells_shuffled": len(shf_cells),
        "growth_curve_eeg": eeg_curve,
        "phi_final_eeg": eeg_phi[-1],
        "phi_min_eeg": min(eeg_phi),
        "phi_max_eeg": max(eeg_phi),
        "phi_finite_eeg": all(math.isfinite(x) for x in eeg_phi),
        "cells_eeg_bounded": MIN_CELLS <= len(eeg_cells) <= MAX_CELLS,
    }


def mean_std(xs):
    m = sum(xs) / len(xs)
    if len(xs) < 2:
        return m, 0.0
    v = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return m, math.sqrt(v)


def main():
    seeds = [1, 2, 3]
    rows = [run_seed(s) for s in seeds]

    # ---- M1 FIDELITY: err_eeg < floor by > seed-noise ----
    e_eeg = [r["err_eeg"] for r in rows]
    flr = [r["floor_error"] for r in rows]
    m_eeg, s_eeg = mean_std(e_eeg)
    m_flr, s_flr = mean_std(flr)
    # improvement margin vs floor, in units of combined seed-std
    noise_band_m1 = math.sqrt(s_eeg ** 2 + s_flr ** 2)
    m1_margin = m_flr - m_eeg
    m1_holds = m1_margin > noise_band_m1 and m1_margin > 0
    m1_verdict = "HOLDS" if m1_holds else ("REFUTED" if m1_margin <= 0 else "INCONCLUSIVE")

    # ---- M2 MITOSIS-vs-2-CONTROLS ----
    e_rnd = [r["err_random"] for r in rows]
    e_shf = [r["err_shuffled"] for r in rows]
    m_rnd, s_rnd = mean_std(e_rnd)
    m_shf, s_shf = mean_std(e_shf)
    nb_rnd = math.sqrt(s_eeg ** 2 + s_rnd ** 2)
    nb_shf = math.sqrt(s_eeg ** 2 + s_shf ** 2)
    marg_rnd = m_rnd - m_eeg            # >0 means eeg better (lower err)
    marg_shf = m_shf - m_eeg
    beats_rnd = marg_rnd > nb_rnd and marg_rnd > 0
    beats_shf = marg_shf > nb_shf and marg_shf > 0
    m2_holds = beats_rnd and beats_shf
    if marg_rnd <= 0 or marg_shf <= 0:
        m2_verdict = "REFUTED"
    elif m2_holds:
        m2_verdict = "HOLDS"
    else:
        m2_verdict = "INCONCLUSIVE"

    # ---- M3 STABILITY ----
    bounded = all(r["cells_eeg_bounded"] for r in rows)
    finite = all(r["phi_finite_eeg"] for r in rows)
    no_collapse = all(r["cells_eeg"] >= MIN_CELLS for r in rows)
    no_explode = all(r["cells_eeg"] <= MAX_CELLS for r in rows)
    m3_holds = bounded and finite and no_collapse and no_explode
    m3_verdict = "HOLDS" if m3_holds else "REFUTED"

    summary = {
        "lane": "M",
        "lane_name": "EEG-grown CLM via mitosis (gradient-FREE growth lane)",
        "method": "empty CLM (0 weights) -> 5-ch EEG tension-link -> gamma>0.20 MITOSIS split -> grown topology = EEG recording",
        "gradient": 0,
        "ce_loss": "NONE (p8 — inference mitosis IS the learning)",
        "scope": "TOY · synthetic EEG (NOT real headset) · CPU · $0 · small cell budget (MAX_CELLS=%d) · stream_len=%d" % (MAX_CELLS, STREAM_LEN),
        "seeds": seeds,
        "M1_fidelity": {
            "claim": "grown structure encodes the EEG above a reconstruction-error floor",
            "err_eeg_mean": m_eeg, "err_eeg_std": s_eeg,
            "floor_mean": m_flr, "floor_std": s_flr,
            "margin_vs_floor": m1_margin, "noise_band": noise_band_m1,
            "verdict": m1_verdict,
        },
        "M2_mitosis_vs_controls": {
            "claim": "EEG-driven growth beats (a) random/EEG-blind AND (b) phase-shuffled, by > seed-noise",
            "err_eeg_mean": m_eeg,
            "err_random_mean": m_rnd, "err_random_std": s_rnd,
            "err_shuffled_mean": m_shf, "err_shuffled_std": s_shf,
            "margin_vs_random": marg_rnd, "noise_band_random": nb_rnd, "beats_random": beats_rnd,
            "margin_vs_shuffled": marg_shf, "noise_band_shuffled": nb_shf, "beats_shuffled": beats_shf,
            "verdict": m2_verdict,
        },
        "M3_stability": {
            "claim": "cell count bounded [MIN_CELLS, MAX_CELLS], tension finite, no collapse/explosion",
            "cells_eeg_per_seed": [r["cells_eeg"] for r in rows],
            "phi_final_per_seed": [r["phi_final_eeg"] for r in rows],
            "phi_min_per_seed": [r["phi_min_eeg"] for r in rows],
            "phi_max_per_seed": [r["phi_max_eeg"] for r in rows],
            "all_bounded": bounded, "all_finite": finite,
            "no_collapse": no_collapse, "no_explosion": no_explode,
            "verdict": m3_verdict,
        },
        "section97_honest_line": "grown CLM is a RECORDING ARTIFACT (measurement anchor, §97-legitimate); it is READ-ONLY here and NEVER feeds anima emission/decision — keeping it out of being a §97 GOAL-ILLEGITIMATE command channel.",
        "lane_separation": "Lane M recorded SEPARATELY from Lane A (AKIDA on-chip) / Lane G (forge CE-descent) / Lane P (py+CUDA gradient) per a_lane_akida_gpu_split — Lane M is the gradient-FREE growth lane.",
        "per_seed": rows,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
