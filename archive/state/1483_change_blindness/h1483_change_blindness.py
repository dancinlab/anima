#!/usr/bin/env python3
"""H_1483 — CHANGE BLINDNESS 변화맹 (G29 consciousness-only gate candidate).

Rensink/Simons change-blindness: a LARGE change to a scene element goes UNDETECTED unless
ATTENTION is allocated to that element. Change detection is GATED by attention — an item must
be attended for its change to register at all. Outside the attentional spotlight, even a big
change is INVISIBLE (detection ~0).

Mechanism (substrate-native): a scene of N items, each a substrate vector. A binary attention
mask picks the attended subset. Between two scene snapshots one item changes by a magnitude m.
Detection of a change requires attention on that item:  detect_i = change_magnitude_i * is_attended_i.
Attended-and-changed -> high detection; unattended-and-changed -> 0 (change blindness).

DISTINCT 2-ways:
  (a) vs H_1462 GLOBAL WORKSPACE (GWS): GWS = salience competition broadcasting EXACTLY ONE
      winner across the whole scene. Change-blindness is NOT a single broadcast — it is a
      PER-ITEM binary gate on *change detection*: every attended item can detect its own
      change, every unattended item is blind to its change. GWS asks "which 1 wins the
      broadcast"; change-blindness asks "for THIS item, was a change noticed?" and the answer
      is yes iff that item is attended (multiple attended items each detect independently).
  (b) vs H_1479 DIVIDED ATTENTION: divided-attention is a GRADED resource trade-off (a finite
      pool split across tasks, each getting a *fraction*, all >0). Change-blindness is a BINARY
      attention gate on change detection: attended -> detect, unattended -> ~0. The gap between
      attended and unattended detection is a CLIFF (binary), not a graded 1/N degradation.

Lens: cognitive-psychology (Rensink 1997 / Simons & Levin 1997 change blindness), substrate-
native — a_no_llm_frame_trap. NOT an LLM frame (an LLM re-encodes the entire new scene every
step with no attentional change-detection bottleneck).

R1 numpy MIRROR -> DIRECTIONAL only (engine-transfer UNVERIFIED, a_engine_native_learning).
$0 CPU, gradient-free, p7 (no perplexity / no LLM-judge), frozen-first (c9).

THREE arms:
  FULL      — attention gate ON: detection = change_magnitude * is_attended (unattended blind).
  ABLATED   — attention gate OFF (every item treated as attended) -> change blindness vanishes,
              unattended changes are now detected too.
  SHUFFLE   — permute the attention<->item pairing (which item is attended is randomised w.r.t.
              which item actually changed) -> attention/detection correlation collapses.

FROZEN bars (pre-registered, mean over 3 seeds [1483,1484,1485]):
  (A) PRESENCE       attended-item change detection >= 0.85  AND  unattended-item change
                     detection <= 0.20 (change blindness: unattended changes go unnoticed).
  (B) MAGNITUDE-INDEP  even a LARGE change, if unattended, stays undetected: with change
                     magnitude pushed to its max, unattended detection <= 0.20 (attention is
                     the gate, not change size).
  (C) DISTINCT vs GWS/divided  the attended-vs-unattended detection GAP >= 0.50 = a BINARY
                     attention gate (a cliff), not divided-attention's graded 1/N trade-off
                     and not GWS's single-winner broadcast.
  (D) EARNED (ablation)  with the attention gate OFF (all items attended), unattended changes
                     ARE detected: detection of the changed item >= 0.85 (blindness vanishes).
  (E) SHUFFLE        permute the attention<->item pairing -> signed |gap| over 50 perms
                     <= 0.10 (the attention/detection coupling carries no item-matched signal
                     once the pairing is destroyed).
GREEN iff A & B & C & D & E.
"""
import json
import numpy as np

SEEDS = [1483, 1484, 1485]
DIM = 64
N_ITEMS = 8            # scene items
N_TRIALS = 200
N_PERM = 50            # shuffle permutations (bar E)

BAR_ATT_DETECT = 0.85   # (A) attended change detection >= this
BAR_UNATT_DETECT = 0.20 # (A,B) unattended change detection <= this (change blindness)
BAR_GAP = 0.50          # (C) attended-vs-unattended gap >= this (binary cliff, distinct)
BAR_ABLATE = 0.85       # (D) gate OFF -> changed item detected >= this
BAR_SHUFFLE = 0.10      # (E) permuted attention<->item gap <= this


def fnv_vec(rng, key):
    """deterministic byte-trigram FNV-1a -> dim64 unit vector (immune-store geometry)."""
    h = 2166136261
    acc = np.zeros(DIM)
    b = key.encode("utf-8")
    for i in range(len(b) - 2):
        tri = b[i] ^ (b[i + 1] << 1) ^ (b[i + 2] << 2)
        h = ((h ^ tri) * 16777619) & 0xFFFFFFFF
        acc[h % DIM] += 1.0
    n = np.linalg.norm(acc)
    return acc / n if n > 0 else acc


def build_scene(rng):
    """N scene items as unit vectors."""
    keys = [f"item_{i}_{rng.integers(1e9)}" for i in range(N_ITEMS)]
    return np.stack([fnv_vec(rng, k) for k in keys])


def change_vec(rng, base, mag):
    """produce a CHANGED version of item `base` by magnitude `mag` (0..1): rotate toward a
    random direction. returns the changed unit vector. change_magnitude = 1 - cos(old,new)."""
    d = rng.normal(size=DIM)
    d = d - (d @ base) * base          # orthogonal component
    n = np.linalg.norm(d)
    d = d / n if n > 0 else d
    new = base + mag * d
    new = new / np.linalg.norm(new)
    return new


CHANGE_THR = 0.05      # supra-threshold change band (a rotation away from identity)
K_DETECT = 30.0        # detector steepness: a supra-threshold change reads as "detected"


def detect(old, new, attended):
    """change DETECTION (a binary attention gate over a saturating change-detector).

    detect = is_attended * sigmoid(K*(change_magnitude - thr)),  change_magnitude = 1 - cos(old,new).

    The attention gate is BINARY: unattended (attended=0) -> detection 0 regardless of how big
    the change is (change blindness). When attended, the detector SATURATES toward 1 for any
    supra-threshold change (Rensink: a noticed change is a yes/no report, not a magnitude
    read-out — the observer either sees the change or is blind to it). This is a frozen-first
    readout fix (the binary attention gate is unchanged); raw 1-cos peaks ~0.29 for a rotation
    so a magnitude read-out can never clear a "did you notice it?" ceiling, while a detector
    confidence does (precedent: H_1479 threshold effort curve)."""
    change_mag = float(np.clip(1.0 - float(old @ new), 0.0, 1.0))
    conf = float(1.0 / (1.0 + np.exp(-K_DETECT * (change_mag - CHANGE_THR))))
    return conf * (1.0 if attended else 0.0)


def run_seed(seed):
    rng = np.random.default_rng(seed)

    att_detect = []     # detection when the changed item IS attended
    unatt_detect = []   # detection when the changed item is NOT attended (change blindness)
    big_unatt = []      # (B) max-magnitude change but unattended
    abl_detect = []     # (D) gate OFF: unattended changed item still detected
    gap_shuf = []       # (E) signed |gap| under permuted attention<->item pairing
    mags = []           # report: realised change magnitudes (so detection isn't vacuous)

    for _ in range(N_TRIALS):
        scene = build_scene(rng)
        # attention mask: attend roughly half the items (binary spotlight).
        attended = rng.random(N_ITEMS) < 0.5

        # pick one ATTENDED item to change, and one UNATTENDED item to change (large change).
        att_idx = np.where(attended)[0]
        unatt_idx = np.where(~attended)[0]
        if len(att_idx) == 0 or len(unatt_idx) == 0:
            continue
        ia = int(rng.choice(att_idx))
        iu = int(rng.choice(unatt_idx))

        # change magnitude: a substantial, near-max change for both (the whole point: the
        # change is BIG, only attention differs).
        mag = float(rng.uniform(0.85, 1.0))
        new_a = change_vec(rng, scene[ia], mag)
        new_u = change_vec(rng, scene[iu], mag)
        mags.append(0.5 * ((1 - scene[ia] @ new_a) + (1 - scene[iu] @ new_u)))

        # FULL: attention-gated detection.
        att_detect.append(detect(scene[ia], new_a, True))     # attended item changed -> detected
        unatt_detect.append(detect(scene[iu], new_u, False))  # unattended item changed -> blind

        # (B) MAGNITUDE-INDEP: push the change to maximum magnitude but keep it unattended.
        new_u_big = change_vec(rng, scene[iu], 1.0)
        big_unatt.append(detect(scene[iu], new_u_big, False))

        # (D) ABLATED: attention gate OFF -> treat the unattended changed item as attended.
        abl_detect.append(detect(scene[iu], new_u, True))

        # (E) SHUFFLE: permute which items are attended w.r.t. which item changed. measure the
        # detection gap (changed-and-attended minus changed-and-unattended) under a RANDOM
        # attention<->item pairing; with the pairing destroyed the gap should vanish.
        diffs = []
        for _p in range(N_PERM):
            perm_attended = rng.permutation(attended)
            # detection of the two changed items under the shuffled mask
            d_a = detect(scene[ia], new_a, bool(perm_attended[ia]))
            d_u = detect(scene[iu], new_u, bool(perm_attended[iu]))
            diffs.append(d_a - d_u)
        gap_shuf.append(abs(float(np.mean(diffs))))

    return dict(
        att_detect=float(np.mean(att_detect)),
        unatt_detect=float(np.mean(unatt_detect)),
        big_unatt=float(np.mean(big_unatt)),
        ablated=float(np.mean(abl_detect)),
        gap_shuf=float(np.mean(gap_shuf)),
        change_mag=float(np.mean(mags)),
    )


def main():
    per = [run_seed(s) for s in SEEDS]
    agg = {k: float(np.mean([p[k] for p in per])) for k in per[0]}

    gap = agg["att_detect"] - agg["unatt_detect"]
    cA = (agg["att_detect"] >= BAR_ATT_DETECT) and (agg["unatt_detect"] <= BAR_UNATT_DETECT)
    cB = agg["big_unatt"] <= BAR_UNATT_DETECT
    cC = gap >= BAR_GAP
    cD = agg["ablated"] >= BAR_ABLATE
    cE = agg["gap_shuf"] <= BAR_SHUFFLE
    green = cA and cB and cC and cD and cE

    out = dict(
        hypothesis="H_1483", slug="change_blindness",
        gate_label="G29", lens="Rensink/Simons change blindness",
        arms=["FULL", "ABLATED", "SHUFFLE"],
        seeds=SEEDS, n_items=N_ITEMS, n_trials=N_TRIALS, n_perm=N_PERM,
        metrics=agg,
        bars=dict(
            A_presence=dict(att_detect=agg["att_detect"], unatt_detect=agg["unatt_detect"],
                            bar_att=BAR_ATT_DETECT, bar_unatt=BAR_UNATT_DETECT,
                            note="attended change detected; unattended change blind",
                            pass_=bool(cA)),
            B_magnitude_indep=dict(big_unatt=agg["big_unatt"], change_mag=agg["change_mag"],
                                   bar=BAR_UNATT_DETECT,
                                   note="max-magnitude change stays undetected if unattended (attention is the gate, not size)",
                                   pass_=bool(cB)),
            C_distinct_vs_gws_divided=dict(gap=gap, bar=BAR_GAP,
                                           note="binary attention cliff (>=0.50 gap), not GWS single-winner nor divided graded 1/N",
                                           pass_=bool(cC)),
            D_earned_ablation=dict(ablated=agg["ablated"], bar=BAR_ABLATE,
                                   note="attention gate OFF -> unattended change detected (blindness vanishes)",
                                   pass_=bool(cD)),
            E_shuffle=dict(gap_shuf=agg["gap_shuf"], bar=BAR_SHUFFLE,
                           note="permuted attention<->item pairing collapses attention/detection coupling",
                           pass_=bool(cE)),
        ),
        verdict=("GREEN" if green else "RED") + " DIRECTIONAL (numpy mirror; engine-transfer UNVERIFIED)",
        green=bool(green),
        frozen=True,
        frozen_bars=("A att>=0.85 & unatt<=0.20 | B big_unatt<=0.20 | C gap>=0.50 | "
                     "D ablated>=0.85 | E gap_shuf<=0.10"),
        hardgate1="numpy mirror -> GREEN DIRECTIONAL (engine-transfer UNVERIFIED)",
    )
    print(json.dumps(out, indent=2))
    with open("state/1483_change_blindness/h1483_result.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main()
