"""
H_1188 — extend the H_1186 per-modality temporal ranking to TWO MORE toy modalities:
NUMERIC (an autoregressive time-series of structured numeric vectors) and IMAGE
(spatial frames held STATIC-per-scene, the contrast to video's smooth motion).
(Lane 2 / MAIN hands-on discovery rung, MITOSIS-ENGINE domain)

H_1186 ranked AUDIO / TEXT / VIDEO on the temporal grounding of the derivative-tick
decode advantage, each at its OWN coverage cap K*=argmax_K d(DERIVATIVE,METRONOME):
  - audio  K*=32  d_real=+1.15  d_shuf=+0.27  drop=+0.88  TEMPORAL=True
  - video  K*=64  d_real=+0.49  d_shuf=-0.62  drop=+1.11  TEMPORAL=False-by-bar (most fragile)
  - text   K*=4   d_real=+0.50  d_shuf=+0.91  drop=-0.41  TEMPORAL=False (shuffle HELPS)
i.e. temporal-DEPENDENCE (shuffle drop) video>audio>text, ordered-ADVANTAGE audio>video~text.

H_1188 places NUMERIC and IMAGE in the SAME ranking, with the SAME frozen own-cap test:
  1. NUMERIC = per-regime AR(1) numeric process (own coefficient + mean over the 8 dims),
     regimes recurring with dwell. Strong WITHIN-regime temporal autocorrelation, SMOOTH
     transitions toward each regime's attractor. stage = regime id.
  2. IMAGE = K fixed spatial patterns (a DIM=8 vector = a flattened tiny frame) held STATIC
     within a scene (NO within-scene drift) + small per-tick pixel noise, abrupt scene cuts
     with LONG dwell. The contrast to video: video drifts smoothly inside a scene, image is
     frozen. stage = scene id.

===========================  FROZEN PRE-REGISTERED FALSIFIER  ==========================
(written BEFORE any measurement; deterministic, the H_1163 seeds; per stream find
K*=argmax_K d(DERIVATIVE,METRONOME) over the cap ladder, then time-shuffle at K*.)

  cap ladder K = {4,6,8,12,16,24,32,48,64}
  a stream is TEMPORAL iff d_real(K*) >= 0.5 AND (d_real(K*) - d_shuf(K*)) >= 0.5.

  PRE-REGISTERED PREDICTIONS (stated BEFORE running — do NOT move):
    NUMERIC  -> TEMPORAL = YES.  Rationale: AR(1) has STRONG within-regime temporal
        autocorrelation with SMOOTH transitions toward each regime's attractor; the
        derivative tick should fire on the rising-edge of the smooth approach to a NEW
        attractor (a regime transition), so cells are born under distinct regimes (high
        decode), and scrambling time DESTROYS the smooth approach (shuffle should kill it).
        Numeric is structurally like AUDIO (recurring drifting regimes) -> expect TEMPORAL.
    IMAGE    -> TEMPORAL = NO.   Rationale: a scene is STATIC (frozen pattern + iid pixel
        noise, no within-scene motion), so the only temporal signal is the abrupt cut. With
        NO smooth approach, the derivative edge is a single-tick spike that the metronome can
        match (far-apart static scenes are easy for BOTH gates, cf H_1186 VIDEO's modest
        ordered advantage), and time-order carries little — like TEXT/VIDEO's WEAK ordered
        advantage. Expect d_real modest and NOT clearing the temporal bar; the static-frame
        structure should look NON-temporal (closer to TEXT than to AUDIO).

  F1 NUMERIC : report NUMERIC's TEMPORAL classification at its own K* (and whether it
       matches the prediction TEMPORAL=YES).
  F2 IMAGE   : report IMAGE's TEMPORAL classification at its own K* (and whether it matches
       the prediction TEMPORAL=NO).
  SUPPORTED iff BOTH pre-registered predictions are BORNE OUT (NUMERIC temporal AND IMAGE
  non-temporal). Otherwise CLOSED-NEGATIVE (a_paper_negative_ok) — a refuted prediction is
  itself a finding about WHAT STRUCTURAL PROPERTY makes a modality temporal.
=======================================================================================

toy ($0 CPU numpy, deterministic). Reuses UNIVERSE/h1163_tick_decode_metric.py VERBATIM
(grow_arm / stage_decode_accuracy / cohen_d_paired / make_audio_stream / SEEDS / DIM / T /
WARMUP / MAX_CELLS); ADDS make_numeric_stream + make_image_stream (same (X[need,DIM],stages)
convention, DIM=8) + the H_1186 own-cap + H_1184 time-shuffle harness VERBATIM. AUDIO is
re-run as the known-temporal anchor for grounding. a_scale_honest_scope: TOY synthetic
streams (NOT real numeric sensors / real images), DIM=8, $0 CPU, small-n; real-modality +
learned-encoder transfer UNVERIFIED. a_completeness_over_cheap: any construction defect is
fixed BEFORE scoring, never tune-to-green. Lane-M gradient-free growth lane (recorded
SEPARATELY from Lane A AKIDA / Lane G forge / Lane P torch per a_lane_akida_gpu_split).
"""
import json
import numpy as np
import h1163_tick_decode_metric as H

CAP_LADDER = [4, 6, 8, 12, 16, 24, 32, 48, 64]
PERM_SALT = 7919                       # VERBATIM H_1186 shuffle salt
N_REGIMES_NUMERIC = 6                  # match AUDIO/VIDEO K so the ranking is comparable
N_SCENES_IMAGE = 6


def make_numeric_stream(seed):
    """Toy NUMERIC time-series: K regimes, each a per-regime AR(1) process over the 8 dims
    with its OWN coefficient and mean (attractor). Regimes recur with dwell. stage = regime id.

        x_{t+1} = mu_r + a_r * (x_t - mu_r) + eps,   a_r in [0.55, 0.9]  (|a|<1 stable)

    Strong WITHIN-regime temporal autocorrelation; on a regime CUT the state is carried over
    (NO teleport) so the process SMOOTHLY relaxes from the old attractor toward the new mu_r
    over the first part of the dwell -> a smooth, time-ordered approach the derivative tick
    can fire on. Same (X[need,DIM], stages) convention as H.make_audio_stream."""
    rng = np.random.default_rng(seed + 4242)
    K = N_REGIMES_NUMERIC
    mus = rng.standard_normal((K, H.DIM)) * 6.0                       # per-regime attractors
    coefs = rng.uniform(0.55, 0.9, size=K)                            # per-regime AR(1) coeff
    need = H.WARMUP + H.T + 1
    X = np.empty((need, H.DIM)); stages = np.empty(need, dtype=int)
    x = mus[0].copy(); r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:
            r = int(rng.integers(K)); dwell = int(rng.integers(40, 90))   # recur, no teleport
        x = mus[r] + coefs[r] * (x - mus[r]) + rng.standard_normal(H.DIM) * 0.4
        dwell -= 1
        X[t] = x
        stages[t] = r
    return X, stages


def make_image_stream(seed):
    """Toy IMAGE: K fixed spatial patterns (a DIM=8 vector = a flattened tiny frame) held
    STATIC within a scene (NO within-scene drift) + small per-tick iid pixel noise; abrupt
    scene CUTS with LONG dwell. The contrast to video (which drifts smoothly inside a scene):
    image is frozen-per-scene, so the only temporal signal is the cut. stage = scene id.
    Same (X[need,DIM], stages) convention as H.make_audio_stream."""
    rng = np.random.default_rng(seed + 8181)
    K = N_SCENES_IMAGE
    frames = rng.standard_normal((K, H.DIM)) * 7.0          # far-apart static frames -> big cuts
    need = H.WARMUP + H.T + 1
    X = np.empty((need, H.DIM)); stages = np.empty(need, dtype=int)
    r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:                                      # SCENE CUT (abrupt)
            r = int(rng.integers(K)); dwell = int(rng.integers(120, 300))
        X[t] = frames[r] + rng.standard_normal(H.DIM) * 0.25    # STATIC frame + pixel noise
        stages[t] = r
        dwell -= 1
    return X, stages


BUILDERS = {
    "audio":   (H.make_audio_stream,   lambda: H.N_REGIMES_AUDIO),     # known-temporal anchor
    "numeric": (make_numeric_stream,   lambda: N_REGIMES_NUMERIC),     # F1
    "image":   (make_image_stream,     lambda: N_SCENES_IMAGE),        # F2
}


def d_at(builder, n_stages, cap, shuffle):
    """d(DERIVATIVE,METRONOME) on stage-decode at a given cap, optionally time-shuffled.
    VERBATIM the H_1186 harness (own-cap sweep + seeded permutation of X+stages together)."""
    saved_cells = H.MAX_CELLS
    H.MAX_CELLS = cap
    dec_d, dec_m = [], []
    for s in H.SEEDS:
        X, stages = builder(s)
        if shuffle:
            perm = np.random.RandomState(s + PERM_SALT).permutation(len(X))
            X = X[perm]; stages = np.asarray(stages)[perm]
        st_d, cs_d = H.grow_arm(X, stages, "DERIVATIVE", s)
        st_m, cs_m = H.grow_arm(X, stages, "METRONOME", s)
        dec_d.append(H.stage_decode_accuracy(st_d, cs_d, X, stages, n_stages))
        dec_m.append(H.stage_decode_accuracy(st_m, cs_m, X, stages, n_stages))
    H.MAX_CELLS = saved_cells
    return H.cohen_d_paired(dec_d, dec_m)


def main():
    np.seterr(all="ignore")
    print("=== H_1188 — extend the H_1186 per-modality temporal ranking to NUMERIC + IMAGE ===",
          flush=True)
    print(f"  cap ladder K={CAP_LADDER}; per stream K*=argmax d(DERIVATIVE,METRONOME); then "
          f"time-shuffle at K*; {len(H.SEEDS)} seeds; reuses H_1163 VERBATIM + toy numeric/image",
          flush=True)
    print("  PRE-REG predictions (frozen): NUMERIC=TEMPORAL(AR(1) smooth recurring regimes), "
          "IMAGE=NON-TEMPORAL(static-per-scene frames)\n", flush=True)

    out = {}
    for name, (builder, nfn) in BUILDERS.items():
        n_stages = nfn()
        curve = {c: d_at(builder, n_stages, c, shuffle=False) for c in CAP_LADDER}
        kstar = max(curve, key=curve.get)
        d_real = curve[kstar]
        d_shuf = d_at(builder, n_stages, kstar, shuffle=True)
        drop = d_real - d_shuf
        temporal = bool(d_real >= 0.5 and drop >= 0.5)
        out[name] = {"n_stages": n_stages, "K_star": kstar, "d_real": d_real, "d_shuf": d_shuf,
                     "drop": drop, "temporal": temporal,
                     "curve": {str(c): curve[c] for c in CAP_LADDER}}
        print(f"  {name:8s} n_stages={n_stages}  K*={kstar:3d}  d_real={d_real:+.3f}  "
              f"d_shuf={d_shuf:+.3f}  drop={drop:+.3f}  -> TEMPORAL={temporal}", flush=True)

    pred_numeric = True            # FROZEN prediction: NUMERIC temporal
    pred_image = False             # FROZEN prediction: IMAGE non-temporal
    numeric_match = bool(out["numeric"]["temporal"] == pred_numeric)
    image_match = bool(out["image"]["temporal"] == pred_image)
    supported = bool(numeric_match and image_match)

    if supported:
        ruling = (
            f"SUPPORTED: BOTH pre-registered predictions BORNE OUT. NUMERIC is TEMPORAL "
            f"(predicted YES) at K*={out['numeric']['K_star']} (d_real={out['numeric']['d_real']:+.2f}, "
            f"drop={out['numeric']['drop']:+.2f}) and IMAGE is NON-TEMPORAL (predicted NO) at "
            f"K*={out['image']['K_star']} (d_real={out['image']['d_real']:+.2f}, "
            f"drop={out['image']['drop']:+.2f}). The structural property that makes a modality temporal "
            f"is SMOOTH WITHIN-REGIME APPROACH: numeric AR(1) relaxes smoothly toward each attractor "
            f"(like audio's drifting regimes) so the derivative tick exploits real time order; image's "
            f"STATIC-per-scene frames give no smooth approach so the event tick has no time-order edge.")
    else:
        parts = []
        parts.append(
            f"NUMERIC predicted TEMPORAL=YES, MEASURED={out['numeric']['temporal']} "
            f"(d_real={out['numeric']['d_real']:+.2f}, drop={out['numeric']['drop']:+.2f}) -> "
            + ("MATCH" if numeric_match else "REFUTED"))
        parts.append(
            f"IMAGE predicted TEMPORAL=NO, MEASURED={out['image']['temporal']} "
            f"(d_real={out['image']['d_real']:+.2f}, drop={out['image']['drop']:+.2f}) -> "
            + ("MATCH" if image_match else "REFUTED"))
        ruling = ("CLOSED-NEGATIVE (a_paper_negative_ok): " + " | ".join(parts)
                  + ". A refuted prediction is the finding: it sharpens WHAT structural property makes "
                    "a modality temporal (smooth within-regime approach vs static frame vs cut-only).")

    verdict = {
        "H": "H_1188",
        "title": "extend the H_1186 per-modality temporal ranking to NUMERIC (autoregressive) + "
                 "IMAGE (static-per-scene frames): which structural property makes a modality temporal?",
        "cap_ladder": CAP_LADDER,
        "frozen_predictions": {"numeric": "TEMPORAL=YES (AR(1) smooth recurring regimes)",
                               "image": "TEMPORAL=NO (static-per-scene frames, cut-only)"},
        "per_modality": {k: {kk: vv for kk, vv in v.items() if kk != "curve"} for k, v in out.items()},
        "curves": {k: out[k]["curve"] for k in out},
        "F1_numeric": {"K_star": out["numeric"]["K_star"], "d_real": out["numeric"]["d_real"],
                       "drop": out["numeric"]["drop"], "temporal": out["numeric"]["temporal"],
                       "predicted_temporal": pred_numeric, "prediction_match": numeric_match},
        "F2_image": {"K_star": out["image"]["K_star"], "d_real": out["image"]["d_real"],
                     "drop": out["image"]["drop"], "temporal": out["image"]["temporal"],
                     "predicted_temporal": pred_image, "prediction_match": image_match},
        "supported": supported,
        "full_ranking_with_h1186": {
            "note": "audio/text/video numbers cited from H_1186 (domains/MITOSIS-ENGINE.log.md); "
                    "audio re-run here as the anchor for grounding (should reproduce ~temporal).",
            "audio_h1186":   {"K_star": 32, "d_real": 1.15, "d_shuf": 0.27, "drop": 0.88, "temporal": True},
            "video_h1186":   {"K_star": 64, "d_real": 0.49, "d_shuf": -0.62, "drop": 1.11, "temporal": False},
            "text_h1186":    {"K_star": 4,  "d_real": 0.50, "d_shuf": 0.91, "drop": -0.41, "temporal": False},
            "audio_rerun_here":  {k: out["audio"][k] for k in ("K_star", "d_real", "d_shuf", "drop", "temporal")},
            "numeric_h1188": {k: out["numeric"][k] for k in ("K_star", "d_real", "d_shuf", "drop", "temporal")},
            "image_h1188":   {k: out["image"][k] for k in ("K_star", "d_real", "d_shuf", "drop", "temporal")},
        },
        "ruling": ruling,
        "scope": "TOY ($0 CPU numpy, %d seeds). Reuses h1163 VERBATIM + the H_1186 own-cap + shuffle "
                 "harness VERBATIM + TWO new toy streams: make_numeric_stream (per-regime AR(1), NOT real "
                 "numeric sensors) + make_image_stream (DIM=8 flattened static frame + pixel noise, NOT "
                 "real images, cf H_1170 toy renderings). Real numeric/image + learned encoders + scale "
                 "UNVERIFIED (a_scale_honest_scope). Lane-M gradient-free growth lane "
                 "(a_lane_akida_gpu_split)." % len(H.SEEDS),
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1188_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
