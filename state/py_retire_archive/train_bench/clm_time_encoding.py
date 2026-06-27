#!/usr/bin/env python3
# ==========================================================================
# Lane M follow-up — "How to embed TIME into the CLM"  (TOY · CPU · $0)
#
# Direct successor to Lane M v1 (PR #1760, CLM/bench/lane_m_eeg_mitosis.py):
# the mitosis-grown CLM recorded the EEG band-power DISTRIBUTION but NOT the
# temporal DYNAMICS. A phase-shuffled EEG with identical marginals TIED the
# EEG-driven growth (margin within seed-noise), and temporal stage-decode was
# at chance (0.25, 4 stages). The diagnosed clue: the split / encoding rule
# must depend on TIME-ORDER, not on instantaneous amplitude.
#
# This bench ablates 4 temporal-encoding methods against the v1 baseline,
# all on the SAME synthetic-EEG harness (faithful reuse of v1 generators,
# tension-link, mitosis split mechanics):
#
#   baseline = Lane M v1 : instantaneous gamma>0.20 split, daughter = drive(t).
#   M1 POSITIONAL/index  : append a sinusoidal time-index embedding (RoPE-style)
#                          to the daughter state + the codebook key, so WHEN a
#                          cell was born is part of its state.
#   M2 PHASE-CLOCK       : (anima-native) gate the split on the pure_field
#                          OSCILLATOR PHASE (CORE/pure_field.hexa: 3 coupled
#                          oscillators tau=2/40/400, phase += 2*pi/tau,
#                          value = amplitude*sin(phase)). Split fires on a
#                          phase WINDOW of the medium oscillator, AND the
#                          daughter state carries the oscillator value — so the
#                          encoding depends on WHEN in the rhythm, not just the
#                          gamma amplitude.
#   M3 DERIVATIVE d/dt   : split on the time-derivative / rising-edge of the
#                          5-ch drive (drive(t)-drive(t-1)), daughter carries
#                          [drive(t), d_drive] — the level AND its rate.
#   M4 TIME-LAGGED WINDOW: feed a delay-line window of the last N steps into the
#                          daughter specialization (mirrors CLMConvMoE dilated
#                          causal conv receptive field); daughter state is the
#                          concatenation of the last WINDOW drives.
#
# Each arm grows over the SAME corpus/seed/stream as the baseline, mitosis ON,
# NO gradient / NO CE / NO backprop (p8 — inference mitosis IS the learning).
#
# METRIC (substrate-native — NOT CE / perplexity, p7). For TIME to be captured
# we use TWO order-sensitive metrics + the v1 reconstruction; the KEY bar is:
#   (a) beats-shuffle : TEMPORAL reconstruction (read-out uses each tick's
#       grown context, see temporal_reconstruct_error) of the TRUE stream must
#       beat the same arm grown on a PHASE-SHUFFLED stream by > seed-noise.
#       (This is the exact control that TIED Lane M v1.)
#   (b) stage-decode  : a nearest-centroid stage classifier built from the grown
#       structure's per-stage time-course must exceed chance (0.25, 4 stages).
#   (c) order-sensitivity : scrambling the EEG time-order must CHANGE the
#       result (delta_shuffle = |err_shuffled - err_eeg|) beyond seed-noise.
#       In v1 this delta was ~0 (the failure). A method "injects time" iff (a)
#       AND (b) hold; (c) is the corroborating mechanism check.
#
# Per arm, 3 seeds, mean +- std: HOLDS (beats shuffle AND decode>chance, both
# by > noise) / REFUTED (a margin <= 0, i.e. shuffle ties-or-wins or decode at
# chance) / INCONCLUSIVE (positive but within noise). A null is NEVER rounded
# into HOLD.
#
# Pure stdlib (no numpy), CPU, $0, fully deterministic. Synthetic EEG, NOT a
# real headset. §97: grown CLM = RECORDING ARTIFACT, READ-ONLY, never feeds
# anima emission/decision. a_lane_akida_gpu_split: Lane M (growth) recorded
# separately from Lane A / G / P.
# ==========================================================================

import json, math, random

# ---- constants mirrored from mitosis.hexa / Lane M v1 --------------------
SPLIT_NOISE_FLOOR = 0.1
MIN_CELLS         = 2
MAX_CELLS         = 64
GAMMA_SPLIT_THR   = 0.20
N_CHANNELS        = 5
STREAM_LEN        = 240
WINDOW            = 4        # M4 delay-line receptive field
POS_DIM           = 4        # M1 sinusoidal position embedding dimension
SEEDS             = [1, 2, 3]

# pure_field oscillator timescales (CORE/pure_field.hexa) ------------------
TAU_FAST, TAU_MED, TAU_SLOW = 2, 40, 400
TWO_PI = 2.0 * 3.14159265

# ---- canonical 5-band EEG signatures (EEG/eeg_backend.hexa) --------------
BAND_SIG = {
    "resting": dict(delta=0.20, theta=0.15, alpha=0.40, beta=0.20, gamma=0.05),
    "n3":      dict(delta=0.70, theta=0.15, alpha=0.05, beta=0.05, gamma=0.05),
    "rem":     dict(delta=0.20, theta=0.30, alpha=0.10, beta=0.25, gamma=0.15),
    "active":  dict(delta=0.10, theta=0.10, alpha=0.15, beta=0.40, gamma=0.25),
}
STAGES = ["resting", "n3", "rem", "active"]


def tension_link_5ch(bp):
    """5-ch tension-link carrier = [alpha, theta, gamma, 1-delta, beta]."""
    return [bp["alpha"], bp["theta"], bp["gamma"], 1.0 - bp["delta"], bp["beta"]]


# ==========================================================================
# Synthetic EEG generator — IDENTICAL to Lane M v1 (faithful reuse).
# ==========================================================================
def gen_eeg_stream(seed, n=STREAM_LEN, jitter=0.03):
    rng = random.Random(seed * 1000 + 17)
    schedule, block, si = [], 30, 0
    while len(schedule) < n:
        schedule += [STAGES[si % len(STAGES)]] * block
        si += 1
    schedule = schedule[:n]
    stream = []
    for t in range(n):
        base = BAND_SIG[schedule[t]]
        bp = {k: max(0.0, v + rng.uniform(-jitter, jitter)) for k, v in base.items()}
        s = sum(bp.values())
        if s > 0:
            bp = {k: v / s for k, v in bp.items()}
        stream.append((schedule[t], bp))
    return stream


def phase_shuffle_stream(stream, seed):
    """Control: identical marginal distribution, temporal order destroyed."""
    rng = random.Random(seed * 7919 + 3)
    idx = list(range(len(stream)))
    rng.shuffle(idx)
    return [stream[i] for i in idx]


# ==========================================================================
# Cell: carries a state vector whose dimension depends on the encoding arm.
# state is the codebook key; the per-tick "query" is built to match it.
# ==========================================================================
class Cell:
    __slots__ = ("cid", "state", "born_tick", "stage", "tension_hist")
    def __init__(self, cid, state, born_tick, stage):
        self.cid = cid
        self.state = list(state)
        self.born_tick = born_tick
        self.stage = stage              # the stage that drove this cell's birth
        self.tension_hist = []


def pos_embed(t, n=STREAM_LEN, dim=POS_DIM):
    """Sinusoidal / RoPE-style positional embedding of a time index."""
    out = []
    for i in range(dim // 2):
        freq = 1.0 / (10000.0 ** (2.0 * i / dim))
        out.append(math.sin(t * freq))
        out.append(math.cos(t * freq))
    return out


def _osc_value(tau, t):
    """pure_field oscillator value at tick t: amplitude*sin(phase), phase=2pi*t/tau.
       amplitude damped toward LN2 (approx via a constant envelope here, toy)."""
    return math.sin(TWO_PI * (t % tau) / tau)


def _l2(a, b):
    m = min(len(a), len(b))
    return sum((a[i] - b[i]) ** 2 for i in range(m)) / m


# ==========================================================================
# QUERY builders — what we compare each cell's stored state against at tick t.
# Must match the daughter-state construction per arm (same dimensionality).
# ==========================================================================
def make_query(arm, drive, prev_drive, t, win_buf):
    if arm == "baseline":
        return list(drive)
    if arm == "M_pos":
        return list(drive) + pos_embed(t)
    if arm == "M_phase":
        # drive + the 3 oscillator values at this tick (the rhythm phase)
        return list(drive) + [_osc_value(TAU_FAST, t), _osc_value(TAU_MED, t), _osc_value(TAU_SLOW, t)]
    if arm == "M_deriv":
        dd = [drive[i] - prev_drive[i] for i in range(N_CHANNELS)]
        return list(drive) + dd
    if arm == "M_window":
        # concatenation of the last WINDOW drives (delay line), oldest-first
        buf = list(win_buf)
        while len(buf) < WINDOW:
            buf = [drive] + buf
        flat = []
        for d in buf[-WINDOW:]:
            flat += d
        return flat
    raise ValueError(arm)


# ==========================================================================
# GROW — one mitosis growth run for a given arm + stream.
# The split TRIGGER and the daughter STATE both depend on the arm's temporal
# encoding. For the phase-shuffled control we keep the SAME arm logic but feed
# the shuffled stream; the positional/phase clock t still runs 0..n (real
# elapsed time), so a shuffled stream is genuinely mis-aligned in time.
# ==========================================================================
_ARM_SALT = {"baseline": 0, "M_pos": 11, "M_phase": 23, "M_deriv": 37, "M_window": 53}


def grow(stream, seed, arm):
    # deterministic per-arm salt (NOT hash() — PYTHONHASHSEED-independent repro)
    rng = random.Random(seed * 131 + _ARM_SALT[arm])
    seed_state = make_query(arm, [0.5] * N_CHANNELS, [0.5] * N_CHANNELS, 0, [])
    cells = [Cell(0, [0.0] * len(seed_state), 0, None)]
    next_id = 1
    prev_drive = [0.5] * N_CHANNELS
    win_buf = []
    growth_curve, phi_trace = [], []

    for t, (stage, bp) in enumerate(stream):
        drive = tension_link_5ch(bp)
        win_buf.append(drive)
        if len(win_buf) > WINDOW:
            win_buf.pop(0)
        query = make_query(arm, drive, prev_drive, t, win_buf)

        # tension update vs the incoming query
        for c in cells:
            tn = _l2(c.state, query)
            c.tension_hist.append(tn)
            if len(c.tension_hist) > 20:
                c.tension_hist.pop(0)

        # ---- SPLIT TRIGGER (arm-dependent) ----
        gamma = bp["gamma"]
        if arm == "M_phase":
            # gate on WHEN in the medium-oscillator rhythm (phase window) AND
            # a relaxed amplitude floor — split depends on the rhythm phase.
            ph = (t % TAU_MED) / TAU_MED        # 0..1 phase of the slow rhythm
            in_phase_window = 0.0 <= ph < 0.5   # rising half of the rhythm
            do_split = in_phase_window and gamma > 0.12
        elif arm == "M_deriv":
            # split on the RISING EDGE of gamma (positive derivative), not level
            d_gamma = drive[2] - prev_drive[2]
            do_split = d_gamma > 0.02
        else:
            # baseline / M_pos / M_window: instantaneous gamma>thr (v1 trigger)
            do_split = gamma > GAMMA_SPLIT_THR

        if do_split and len(cells) < MAX_CELLS:
            cand = max(cells, key=lambda c: (c.tension_hist[-1] if c.tension_hist else 0.0))
            dstate = [q + rng.uniform(-SPLIT_NOISE_FLOOR, SPLIT_NOISE_FLOOR) for q in query]
            cells.append(Cell(next_id, dstate, t, stage))
            next_id += 1

        prev_drive = drive
        growth_curve.append(len(cells))
        phi_trace.append(_phi_proxy(cells))

    return cells, growth_curve, phi_trace


def _phi_proxy(cells):
    n = len(cells)
    if n < 2:
        return 0.0
    tot, cnt = 0.0, 0
    for i in range(n):
        for j in range(i + 1, n):
            d = math.sqrt(_l2(cells[i].state, cells[j].state) * min(len(cells[i].state), len(cells[j].state)))
            tot += d
            cnt += 1
    return (tot / cnt) * math.log(n + 1)


# ==========================================================================
# METRIC (a) — TEMPORAL reconstruction error.
# Unlike v1's purely instantaneous VQ error (order-invariant by construction),
# this read-out scores the TRUE stream tick-by-tick using the SAME temporal
# query the structure was grown with (positional / phase / derivative / window
# context at the true tick t). So if the structure encodes time, reconstructing
# the TRUE-ordered stream is easier than reconstructing under a structure grown
# on a time-mismatched (shuffled) stream.
# ==========================================================================
def temporal_reconstruct_error(cells, stream, arm):
    if not cells:
        return float("inf")
    prev_drive = [0.5] * N_CHANNELS
    win_buf, errs = [], []
    for t, (stage, bp) in enumerate(stream):
        drive = tension_link_5ch(bp)
        win_buf.append(drive)
        if len(win_buf) > WINDOW:
            win_buf.pop(0)
        query = make_query(arm, drive, prev_drive, t, win_buf)
        best = min(_l2(c.state, query) for c in cells)
        errs.append(best)
        prev_drive = drive
    return sum(errs) / len(errs)


# ==========================================================================
# METRIC (b) — STAGE-DECODE accuracy from the grown structure.
# Build a per-stage centroid from the cells born under each stage (the grown
# structure's own time-course labels). Then classify each TRUE-stream tick by
# nearest centroid in the arm's query space. Accuracy vs the true stage label.
# Chance = 0.25 (4 stages). If cells of different stages are indistinguishable
# (v1: all daughters = instantaneous drive, stages overlap) -> ~chance.
# ==========================================================================
def stage_decode_accuracy(cells, stream, arm):
    # centroids from grown cells grouped by their birth stage
    groups = {}
    for c in cells:
        if c.stage is None:
            continue
        groups.setdefault(c.stage, []).append(c.state)
    if len(groups) < 2:
        return 0.0  # cannot decode -> report 0, NOT chance (honest)
    centroids = {}
    for st, states in groups.items():
        dim = len(states[0])
        centroids[st] = [sum(s[i] for s in states) / len(states) for i in range(dim)]

    prev_drive = [0.5] * N_CHANNELS
    win_buf = []
    correct, total = 0, 0
    for t, (true_stage, bp) in enumerate(stream):
        drive = tension_link_5ch(bp)
        win_buf.append(drive)
        if len(win_buf) > WINDOW:
            win_buf.pop(0)
        query = make_query(arm, drive, prev_drive, t, win_buf)
        pred = min(centroids.keys(), key=lambda st: _l2(centroids[st], query))
        if pred == true_stage:
            correct += 1
        total += 1
        prev_drive = drive
    return correct / total if total else 0.0


# ==========================================================================
# Per-arm, per-seed run.
# ==========================================================================
def run_arm_seed(arm, seed):
    stream = gen_eeg_stream(seed)
    shuffled = phase_shuffle_stream(stream, seed)

    cells_eeg, curve_eeg, phi_eeg = grow(stream, seed, arm)
    cells_shf, _, _ = grow(shuffled, seed, arm)

    err_eeg = temporal_reconstruct_error(cells_eeg, stream, arm)
    err_shf = temporal_reconstruct_error(cells_shf, stream, arm)  # scored on TRUE stream
    acc = stage_decode_accuracy(cells_eeg, stream, arm)

    return {
        "arm": arm, "seed": seed,
        "err_eeg": err_eeg, "err_shuffled": err_shf,
        "delta_shuffle": err_shf - err_eeg,     # >0 means TRUE-order grown is better
        "stage_decode_acc": acc,
        "cells_eeg": len(cells_eeg),
        "cells_eeg_bounded": MIN_CELLS <= len(cells_eeg) <= MAX_CELLS,
        "phi_finite": all(math.isfinite(x) for x in phi_eeg),
    }


def mean_std(xs):
    m = sum(xs) / len(xs)
    if len(xs) < 2:
        return m, 0.0
    v = sum((x - m) ** 2 for x in xs) / (len(xs) - 1)
    return m, math.sqrt(v)


def evaluate_arm(arm):
    rows = [run_arm_seed(arm, s) for s in SEEDS]
    e_eeg = [r["err_eeg"] for r in rows]
    e_shf = [r["err_shuffled"] for r in rows]
    acc   = [r["stage_decode_acc"] for r in rows]
    m_eeg, s_eeg = mean_std(e_eeg)
    m_shf, s_shf = mean_std(e_shf)
    m_acc, s_acc = mean_std(acc)

    # (a) beats-shuffle: err on TRUE order < err on shuffled-grown, by > noise
    nb_shf = math.sqrt(s_eeg ** 2 + s_shf ** 2)
    margin_shuffle = m_shf - m_eeg
    beats_shuffle = margin_shuffle > nb_shf and margin_shuffle > 0

    # (b) stage-decode > chance (0.25) by > seed-noise
    CHANCE = 0.25
    decode_margin = m_acc - CHANCE
    decode_above_chance = decode_margin > s_acc and decode_margin > 0

    # (c) order-sensitivity: |delta_shuffle| beyond noise (corroborating)
    order_sensitive = abs(margin_shuffle) > nb_shf

    # arm verdict: HOLDS iff BOTH (a) and (b). REFUTED iff either margin <=0
    # (shuffle ties/wins OR decode at-or-below chance). Else INCONCLUSIVE.
    if margin_shuffle <= 0 or decode_margin <= 0:
        verdict = "REFUTED"
    elif beats_shuffle and decode_above_chance:
        verdict = "HOLDS"
    else:
        verdict = "INCONCLUSIVE"

    return {
        "arm": arm,
        "err_eeg_mean": m_eeg, "err_eeg_std": s_eeg,
        "err_shuffled_mean": m_shf, "err_shuffled_std": s_shf,
        "margin_shuffle": margin_shuffle, "noise_band_shuffle": nb_shf,
        "beats_shuffle": beats_shuffle,
        "stage_decode_acc_mean": m_acc, "stage_decode_acc_std": s_acc,
        "chance": CHANCE, "decode_margin": decode_margin,
        "decode_above_chance": decode_above_chance,
        "order_sensitive": order_sensitive,
        "cells_eeg_per_seed": [r["cells_eeg"] for r in rows],
        "all_bounded": all(r["cells_eeg_bounded"] for r in rows),
        "all_phi_finite": all(r["phi_finite"] for r in rows),
        "verdict": verdict,
        "per_seed": rows,
    }


def main():
    arms = ["baseline", "M_pos", "M_phase", "M_deriv", "M_window"]
    arm_label = {
        "baseline": "Lane M v1 (instantaneous gamma>0.20 split) — known to fail dynamics",
        "M_pos":    "M1 POSITIONAL/index — sinusoidal time-index embedding into split/daughter",
        "M_phase":  "M2 PHASE-CLOCK (anima-native) — pure_field oscillator phase gates the split",
        "M_deriv":  "M3 DERIVATIVE d/dt — split on rising-edge of gamma, daughter carries d/dt",
        "M_window": "M4 TIME-LAGGED WINDOW — delay-line of last N drives into daughter (CLMConvMoE RF)",
    }
    results = {arm: evaluate_arm(arm) for arm in arms}

    summary = {
        "bench": "Lane M follow-up — embedding TIME into the CLM",
        "predecessor": "Lane M v1 (PR #1760): recorded band-power DISTRIBUTION, not DYNAMICS; phase-shuffle TIED it, stage-decode = chance 0.25",
        "method": "4 temporal-encoding arms + v1 baseline on the SAME synthetic-EEG harness; mitosis ON, NO gradient/CE/backprop (p8)",
        "metric": "substrate-native (NOT CE/perplexity, p7): (a) TEMPORAL recon beats phase-shuffled control by > seed-noise [KEY BAR]; (b) stage-decode > chance 0.25 by > noise; (c) order-sensitivity corroborates",
        "verdict_rule": "HOLDS iff (a) AND (b); REFUTED iff either margin <= 0; else INCONCLUSIVE. A null is NOT rounded into HOLD.",
        "seeds": SEEDS,
        "scope": "TOY ONLY (a_toy_scale_recheck/a_scale_honest_scope): synthetic EEG (NOT real headset), MAX_CELLS=%d, stream_len=%d, CPU, $0, mitosis ON. Scale/real-EEG transfer UNVERIFIED." % (MAX_CELLS, STREAM_LEN),
        "lane_separation": "Lane M (gradient-free growth) recorded SEPARATELY from Lane A (AKIDA) / Lane G (forge GPU) / Lane P (gradient) per a_lane_akida_gpu_split.",
        "section97": "grown CLM = RECORDING ARTIFACT (measurement anchor, §97-legitimate), READ-ONLY, NEVER feeds anima emission/decision.",
        "arm_labels": arm_label,
        "arms": results,
    }
    print(json.dumps(summary, indent=2))
    return summary


if __name__ == "__main__":
    main()
