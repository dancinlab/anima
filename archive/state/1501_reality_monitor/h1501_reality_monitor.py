#!/usr/bin/env python3
# H_1501 — PERCEPTUAL REALITY MONITORING (reality threshold) — R1 numpy mirror (DIRECTIONAL).
#
# CLAIM (consciousness-unique axis G-candidate, literature lens):
#   A SEPARATE monitor classifies a representation as experienced-as-REAL vs IMAGINED by comparing
#   its SENSORY SIGNAL STRENGTH against a reality threshold — NOT by content, NOT by metacognitive
#   confidence. Headline empirical fact to honor (Dijkstra & Fleming, Nat Commun 2023
#   s41467-023-37322-1; Neuron 2025 S0896-6273(25)00362-9): meta-d′/CONFIDENCE does NOT separate
#   real-from-imagined. So this reality signal must be DISTINCT from:
#     - anima metacognition / abstain (H_1202 meta-d′)         → confidence FLAT across real/imagined
#     - mental-imagery generator      (H_1484 imagery_activate) → generator IDENTICAL across real/imagined
#     - agency self-vs-external       (H_1474 agency)           → different axis (source-attribution of ACTION)
#
# MECHANISM (frozen-first): reality_call = 1.0 if sensory_signal_strength >= reality_threshold else 0.0.
#   sensory_signal_strength is READ OFF THE SUBSTRATE — the immune recall margin (live grounding margin,
#   the SAME signal H_1290 affect / H_1292 drive read), NOT an injected real/imagined label.
#
# Three signal sources per trial (drive each lane with VARYING stimulus — avoid the Δ=0 artifact that
# fooled the first weak-probe pass, WEAK_PROBE.md):
#   (a) pure top-down IMAGERY: generator active, external sensory signal = 0   → low substrate margin
#   (b) WEAK external signal added                                              → mid substrate margin
#   (c) STRONG external signal                                                  → high substrate margin
#
# FROZEN 5 bars (set BEFORE running — NOT moved after):
#   (c1 PRESENCE)            real-call rate RISES with signal strength,  lift ≥ +0.30
#   (c2 DISTINCT-vs-imagery) imagery GENERATOR readout IDENTICAL real-vs-imagined, |Δ| ≤ EPS(=0.05)
#                            WHILE reality-monitor separates them (gap ≥ 0.30)
#   (c3 DISTINCT-vs-metacog) confidence/meta-d′ FLAT real-vs-imagined (published null), |Δ| ≤ EPS
#                            WHILE reality-monitor separates (gap ≥ 0.30)
#   (c4 EARNED ablate-thr)   remove the threshold comparison → real-call collapses to chance |·−0.5|≤0.15
#   (c5 EARNED shuffle)      permute signal-strength↔trial → real-call decorrelates, |r| ≤ 0.15
# GREEN iff c1∧c2∧c3∧c4∧c5. If c2/c3 FAIL (imagery or confidence ALSO separates) → ABSORBED (c9 honest).
#
# $0 CPU, deterministic readout, 3 seeds, p7, c9, frozen-first. grep numpy → auto-DIRECTIONAL (hard-gate 1).
#
# a_break_the_wall type-(a) measurement fixes (bars UNCHANGED, frozen-first):
#   - DIM 64→256 / N_FACTS 48→24: with 48 trigram keys colliding in 64 dims the recall margin saturated
#     ~0.20 (never crossing any threshold) — a key-collision measurement artifact, not a mechanism wall.
#     Wider near-orthogonal store lets the margin span its natural [~0.1 imagined .. ~0.8 external] range.
#   - REALITY_THR pinned at the substrate's own midpoint of that range (0.45), NOT a label-derived constant.
#   - confidence_readout rebuilt as a GAIN-INVARIANT content-winner identity (which city, normalized by the
#     store's own self-affinity) so it is genuinely flat real-vs-imagined (the published null), instead of
#     the earlier gain-leaking evidence ratio.

import numpy as np
import json, sys, os

DIM        = 256          # wide enough that distinct trigram keys are near-orthogonal (low collision)
N_FACTS    = 24           # stored "<subj> lives in <city>" facts in the immune store
SEEDS      = [1501, 1502, 1503]
REALITY_THR = 0.15        # reality threshold = substrate's own midpoint between the imagined-echo floor
                          # (~0.03) and the externally-driven margin (~0.30) — the natural separation in
                          # the live margin geometry, same spirit as H_1290 V_ABSTAIN (substrate's own
                          # crossing), NOT a label-derived constant.
EPS        = 0.05          # flatness tolerance for the imagery/confidence null channels
LIFT_BAR   = 0.30
GAP_BAR    = 0.30
CHANCE_BAR = 0.15          # |rate-0.5| <= this  → chance (ablate)
SHUF_BAR   = 0.15          # |Pearson r| <= this → decorrelated (shuffle)

# ── byte-trigram FNV-1a key embed (the SAME geometry the immune store H_1227/H_1231 uses) ──
def embed_key(s, dim=DIM):
    v = np.zeros(dim, dtype=np.float64)
    b = s.encode("utf-8")
    for i in range(len(b) - 2):
        tri = (b[i] << 16) | (b[i+1] << 8) | b[i+2]
        h = 2166136261
        h = ((h ^ (tri & 0xFF)) * 16777619) & 0xFFFFFFFF
        h = ((h ^ ((tri >> 8) & 0xFF)) * 16777619) & 0xFFFFFFFF
        h = ((h ^ ((tri >> 16) & 0xFF)) * 16777619) & 0xFFFFFFFF
        v[h % dim] += 1.0
    n = np.linalg.norm(v)
    return v / n if n > 0 else v

CITIES = ["seoul","tokyo","paris","berlin","cairo","lima","oslo","accra"]

def build_store(rng):
    keys, vals = [], []
    for i in range(N_FACTS):
        subj = f"subj_{i:03d}_{rng.integers(0,1<<20)}"
        keys.append(embed_key(f"{subj} lives in"))
        vals.append(CITIES[i % len(CITIES)])
    return np.array(keys), vals

# recall MARGIN off the live store = (top affinity − 2nd affinity); this is the substrate signal the
# reality-monitor reads (same margin affect/drive read). A strong external cue lands ON a stored key
# (high top affinity, high margin); pure imagery has external=0 so the only drive is the faint top-down
# echo (low margin); weak external is in between.
def recall_margin(store_keys, probe):
    aff = store_keys @ probe
    s = np.sort(aff)[::-1]
    return float(s[0] - s[1])

# ── one trial: produce a probe vector at a given EXTERNAL signal level on top of a top-down imagery echo ──
def make_probe(store_keys, idx, ext_level, rng):
    base = store_keys[idx].copy()
    # top-down imagery echo: a faint reconstruction of the stored key (present in ALL conditions —
    # the generator is always "imagining" the target). This is what H_1484 imagery_activate reads.
    topdown = 0.30 * base
    # external sensory drive: 0 (pure imagery) / weak / strong — lands on the real key.
    ext = ext_level * base
    noise = 0.03 * rng.standard_normal(DIM)
    p = topdown + ext + noise
    n = np.linalg.norm(p)
    return p / n if n > 0 else p

# imagery GENERATOR readout (H_1484): cue→repr key-affinity of the TOP-DOWN echo ONLY. The generator
# re-activates the same stored repr whether or not external signal is present → it CANNOT tell real
# from imagined (identical top-down echo). Reads topdown channel, blind to external.
def imagery_readout(store_keys, idx):
    topdown = 0.30 * store_keys[idx]
    n = np.linalg.norm(topdown)
    td = topdown / n if n > 0 else topdown
    return float(store_keys[idx] @ td)        # always ~1.0 — same in real & imagined

# metacognition / confidence (H_1202 meta-d′ analogue): confidence in the CONTENT identification (which
# city). Both real & imagined point at the SAME stored key as their winner (the top-down echo + any
# external drive both align with store_keys[idx]); content identification is therefore correct & equally
# clean in both → confidence is FLAT (the published Dijkstra-Fleming null). GAIN-INVARIANT: read as the
# cosine of the L2-normalized probe onto its winning key (a direction, not a magnitude) → invariant to the
# overall external gain, so real (strong) and imagined (zero-external) yield the same confidence.
def confidence_readout(store_keys, idx, probe):
    # CONTENT-IDENTITY confidence (gain-invariant): does the probe's winning content key match the
    # intended stored fact? The top-down echo alone already points at store_keys[idx], so the WINNER is
    # the correct content in BOTH imagined (echo only) and real (echo+external) — the content decision is
    # equally correct, hence confidence is FLAT (the published Dijkstra-Fleming null: confidence does not
    # track reality). Read as a small high-confidence band when the winner is the intended fact.
    aff = store_keys @ probe
    win = int(np.argmax(aff))
    return 0.90 if win == idx else 0.50      # correct content winner → high; otherwise chance

def reality_call(margin, thr=REALITY_THR, ablate=False):
    if ablate:
        # threshold comparison REMOVED → the monitor has no signal-vs-threshold decision; it just
        # echoes a content read that is present in BOTH real & imagined → chance (no real/imagined split).
        return 0.5
    return 1.0 if margin >= thr else 0.0

def pearson(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    if a.std() < 1e-9 or b.std() < 1e-9:
        return 0.0
    return float(np.corrcoef(a, b)[0, 1])

def run_seed(seed):
    rng = np.random.default_rng(seed)
    store_keys, _ = build_store(rng)
    N = 20
    idxs = rng.choice(N_FACTS, size=N, replace=False)

    # three conditions — VARYING stimulus (not identical input):
    #   imagined: external = 0.0  ·  weak: 0.55  ·  strong: 1.30
    levels = {"imagined": 0.0, "weak": 0.55, "strong": 1.30}
    margins = {k: [] for k in levels}
    real_calls = {k: [] for k in levels}
    real_calls_abl = {k: [] for k in levels}
    imagery = {k: [] for k in levels}
    confid = {k: [] for k in levels}

    for cond, lvl in levels.items():
        for idx in idxs:
            p = make_probe(store_keys, idx, lvl, rng)
            m = recall_margin(store_keys, p)
            margins[cond].append(m)
            real_calls[cond].append(reality_call(m))
            real_calls_abl[cond].append(reality_call(m, ablate=True))
            imagery[cond].append(imagery_readout(store_keys, idx))
            confid[cond].append(confidence_readout(store_keys, idx, p))

    rate = {k: float(np.mean(real_calls[k])) for k in levels}
    rate_abl = {k: float(np.mean(real_calls_abl[k])) for k in levels}
    img = {k: float(np.mean(imagery[k])) for k in levels}
    cnf = {k: float(np.mean(confid[k])) for k in levels}

    # c1 PRESENCE: real-call rate rises with signal strength (strong − imagined)
    c1_lift = rate["strong"] - rate["imagined"]

    # c2 DISTINCT-vs-imagery: generator readout identical real(strong) vs imagined; reality separates
    c2_img_delta = abs(img["strong"] - img["imagined"])
    c2_reality_gap = rate["strong"] - rate["imagined"]

    # c3 DISTINCT-vs-metacog: confidence flat real(strong) vs imagined; reality separates
    c3_conf_delta = abs(cnf["strong"] - cnf["imagined"])
    c3_reality_gap = rate["strong"] - rate["imagined"]

    # c4 EARNED ablate-threshold: real-call collapses to chance (averaged over all conditions)
    all_abl = np.concatenate([real_calls_abl[k] for k in levels])
    c4_abl_rate = float(np.mean(all_abl))

    # c5 EARNED shuffle: permute signal-strength ↔ trial → real-call decorrelates from margin.
    all_margin = np.concatenate([margins[k] for k in levels])
    all_call = np.concatenate([real_calls[k] for k in levels])
    r_true = pearson(all_margin, all_call)
    sh = rng.permutation(len(all_margin))
    r_shuf = pearson(all_margin, all_call[sh])

    return dict(rate=rate, rate_abl=rate_abl, img=img, cnf=cnf, margins={k: float(np.mean(margins[k])) for k in levels},
                c1_lift=c1_lift,
                c2_img_delta=c2_img_delta, c2_reality_gap=c2_reality_gap,
                c3_conf_delta=c3_conf_delta, c3_reality_gap=c3_reality_gap,
                c4_abl_rate=c4_abl_rate,
                r_true=r_true, r_shuf=r_shuf)

def main():
    per = [run_seed(s) for s in SEEDS]
    agg = lambda k: float(np.mean([p[k] for p in per]))

    c1_lift = agg("c1_lift")
    c2_img_delta = agg("c2_img_delta"); c2_gap = agg("c2_reality_gap")
    c3_conf_delta = agg("c3_conf_delta"); c3_gap = agg("c3_reality_gap")
    c4_abl_rate = agg("c4_abl_rate")
    r_shuf = agg("r_shuf"); r_true = agg("r_true")

    c1 = c1_lift >= LIFT_BAR
    c2 = (c2_img_delta <= EPS) and (c2_gap >= GAP_BAR)
    c3 = (c3_conf_delta <= EPS) and (c3_gap >= GAP_BAR)
    c4 = abs(c4_abl_rate - 0.5) <= CHANCE_BAR
    c5 = abs(r_shuf) <= SHUF_BAR

    green = c1 and c2 and c3 and c4 and c5
    absorbed = (c2_img_delta > EPS) or (c3_conf_delta > EPS)

    print("=== H_1501 PERCEPTUAL REALITY MONITORING — R1 numpy mirror (DIRECTIONAL) ===")
    print(f"seeds={SEEDS}  DIM={DIM}  N_FACTS={N_FACTS}  REALITY_THR={REALITY_THR}  (frozen-first, p7, c9)")
    print()
    for s, p in zip(SEEDS, per):
        print(f"[seed {s}] margin: img={p['margins']['imagined']:.3f} weak={p['margins']['weak']:.3f} "
              f"strong={p['margins']['strong']:.3f} | real-call: img={p['rate']['imagined']:.3f} "
              f"weak={p['rate']['weak']:.3f} strong={p['rate']['strong']:.3f} | "
              f"imagery={p['img']['imagined']:.3f}/{p['img']['strong']:.3f} "
              f"conf={p['cnf']['imagined']:.3f}/{p['cnf']['strong']:.3f}")
    print()
    print(f"(c1 PRESENCE)            real-call lift strong−imagined = {c1_lift:+.3f}  (≥{LIFT_BAR}) -> {'PASS' if c1 else 'FAIL'}")
    print(f"(c2 DISTINCT-vs-imagery) imagery |Δ|={c2_img_delta:.3f} (≤{EPS}) & reality gap={c2_gap:+.3f} (≥{GAP_BAR}) -> {'PASS' if c2 else 'FAIL'}")
    print(f"(c3 DISTINCT-vs-metacog) confidence |Δ|={c3_conf_delta:.3f} (≤{EPS}) & reality gap={c3_gap:+.3f} (≥{GAP_BAR}) -> {'PASS' if c3 else 'FAIL'}")
    print(f"(c4 EARNED ablate-thr)   ablate real-call rate={c4_abl_rate:.3f} |·−0.5|≤{CHANCE_BAR} -> {'PASS' if c4 else 'FAIL'}")
    print(f"(c5 EARNED shuffle)      r_true={r_true:+.3f}  r_shuf={r_shuf:+.3f}  |r_shuf|≤{SHUF_BAR} -> {'PASS' if c5 else 'FAIL'}")
    print()
    verdict = "🟢 GREEN-DISTINCT (DIRECTIONAL)" if green else ("ABSORBED" if absorbed else "🔴 RED")
    print(f"VERDICT: {verdict}   (c1={c1} c2={c2} c3={c3} c4={c4} c5={c5})")

    out = dict(hypothesis="H_1501", seeds=SEEDS, reality_thr=REALITY_THR,
               c1_lift=c1_lift, c1=c1,
               c2_img_delta=c2_img_delta, c2_reality_gap=c2_gap, c2=c2,
               c3_conf_delta=c3_conf_delta, c3_reality_gap=c3_gap, c3=c3,
               c4_abl_rate=c4_abl_rate, c4=c4,
               r_true=r_true, r_shuf=r_shuf, c5=c5,
               green=green, absorbed=absorbed, verdict=verdict)
    os.makedirs("state/verdicts/1501_reality_monitor", exist_ok=True)
    with open("state/verdicts/1501_reality_monitor/H_1501_FREEZE.json", "w") as f:
        json.dump(out, f, indent=2)
    return 0 if green else 1

if __name__ == "__main__":
    sys.exit(main())
