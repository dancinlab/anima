"""
H_1189 — SIMULTANEOUS multi-modal input (TEXT + AUDIO + IMAGE at the SAME tick):
does fusing three concurrent modalities give the event/derivative-tick coverage
mechanism a SUPER-ADDITIVE benefit (fused whole > best single modality) AND is that
benefit TEMPORAL (killed by a time-shuffle)?  (Lane-2 / MAIN hands-on discovery rung,
MITOSIS-ENGINE domain.)

This crosses TWO arcs:
 - the TEMPORALITY arc (H_1184-1186): the derivative tick's coverage advantage is
   TEMPORAL (a time-shuffle kills it) on streams with smooth-flow-then-event structure;
   audio is the goldilocks modality, video most time-fragile, toy byte-text non-temporal.
 - the CROSS-MODAL SUPER-ADDITIVITY arc (H_1167-1170): the super-additive surplus
   S = whole - Σparts COLLAPSES across a data-TYPE jump UNLESS surface is preserved
   (H_1170: only the text↔audio bridge survived, because char→tone is a near-MONOTONE byte
   transform; glyph-raster + windowed byte-stats SCRAMBLE byte order and kill the bridge).
   H_1170 paired MISALIGNED cross-type data. The user's new question is the COMPLEMENT:
   "텍스트 + 오디오 + 이미지, 동시도, 실험" — what if all three arrive SIMULTANEOUSLY, the
   SAME scene/regime driving all three at EACH timestep (concurrent, time-aligned fusion)?

CONSTRUCTION (the "동시" = same-time fusion):
  ONE shared regime/scene timeline stage[t] (the SAME stage id drives all 3 modalities).
  At each t we render, ALL keyed to stage[t]:
    - AUDIO  sub-vector: a drifting-center recurring-regime tone (H.make_audio_stream-style).
    - TEXT   sub-vector: byte-feature-style vector whose regime is stage[t] (same regime →
             same text "register" center + small drift; the byte-feature geometry of H_1163).
    - IMAGE  sub-vector: a STATIC-per-scene spatial pattern (one fixed pattern per scene id)
             + per-tick spatial noise (an image of a scene barely changes within the scene,
             jumps at a cut — the H_1186 video intuition but as a still frame per tick).
  Each sub-vector is DIM=8. The FUSED input is the concatenation [audio|text|image] = 24-d,
  projected DOWN to DIM=8 by a FIXED SEEDED Gaussian random projection P (24→8), so the
  fused stream is a legal H.grow_arm input. stage[t] = the shared regime id (decode chance 1/K).

DIMENSIONALITY HANDLING (REQUIRED CHECK — done):
  H.grow_arm and H.stage_decode_accuracy are HARDCODED to H.DIM (a module global = 8):
  grow_arm seeds `cells = X[:2]` (inherits X width) BUT `nexts = np.zeros((2, H.DIM))`,
  daughter noise `rng.standard_normal(H.DIM)`, and the WARMUP `nexts` update all assume
  width == H.DIM. Feeding a 24-wide X would shape-mismatch. SO: every stream fed to grow_arm
  is DIM=8. The fused 24-d concat is projected to 8 via a FIXED seeded random projection
  (deterministic, NOT re-fit per arm/seed) — NOT silently widened. The 3 single-modality
  baselines are each native DIM=8 (their own sub-vector), on the SAME shared stage timeline.

SURFACE-vs-LABEL HONESTY (the H_1170 gate — load-bearing):
  Audio/text/image sub-vectors are DISTINCT geometries (drift-tone / byte-feature / static
  spatial pattern) sharing ONLY the abstract regime LABEL stage[t] — they do NOT share a
  common SURFACE alphabet the way H_1170's surviving text↔audio monotone byte-map did. So
  this is a "동시(label-aligned)" fusion, NOT a surface-preserved fusion. Per H_1170 (surplus
  is SURFACE-gated, not meaning-gated) the PREDICTION is fusion should give little/no
  super-additive lift beyond the best single modality — unless SIMULTANEITY itself (the same
  stage at the same t, fused before decode) manufactures a benefit the misaligned H_1170
  pairing could not. The random projection MIXES the three geometries into a shared 8-d
  surface, so it is a partial surface-bridge — we report whether that suffices.

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, H_1163 seeds; metric =
clm-time-encoding STAGE-DECODE accuracy of the DERIVATIVE arm; p7, NOT perplexity):
  Per stream s ∈ {audio, text, image, FUSED}: sweep the cap ladder
  K ∈ {4,6,8,12,16,24,32,48,64}, K*(s) = argmax_K d(DERIVATIVE,METRONOME) on stage-decode;
  record the DERIVATIVE-arm raw decode accuracy at K*(s) per seed.
  F1 SUPER-ADDITIVE FUSION : the FUSED stream's derivative decode accuracy at its own K*
     exceeds the BEST single modality's (max over audio/text/image of its own-K* derivative
     accuracy), paired over seeds, Cohen's d(fused_acc - best_single_acc) >= 0.5.
     (fusion helps super-additively, not merely = the best part.)
  F2 TEMPORAL : the FUSED stream's d(DERIVATIVE,METRONOME) advantage at its own K* is
     TEMPORAL — (d_real - d_shuf) >= 0.5 on a seeded time-shuffle of the fused (X,stages).
  SUPPORTED (SIMULTANEOUS-FUSION-HELPS-TEMPORALLY) iff F1 AND F2.
  Otherwise CLOSED-NEGATIVE (a_paper_negative_ok) — e.g. fusion = best part (no
  super-additivity, echoing H_1170's surface-gated collapse), or the fused advantage is not
  temporal. Reported verbatim either way.

NOTE on the F1 "best single" choice: best_single is computed PER SEED as the max over the
three single-modality derivative accuracies at THEIR OWN K* (a strong, honest baseline — the
fused stream must beat the best part on each seed, not just on the mean), so F1's paired d is
a true super-additivity test, not a fused-vs-mean-of-parts inflation.

toy ($0 CPU numpy, deterministic seeds; reuses H_1163 grow_arm / stage_decode_accuracy /
cohen_d_paired / make_audio_stream / SEEDS / N_REGIMES_AUDIO VERBATIM). a_scale_honest_scope /
a_toy_scale_recheck: TOY synthetic "modalities" — drift-tone audio, byte-feature text, static
spatial image — sharing a SAME-projection 8-d surface; NOT real TTS / images / learned
encoders (cf H_1170 toy renderings). DIM=8, small-n, live CORE + production scale UNVERIFIED.
Lane-M gradient-free growth lane (separate from Lane A AKIDA / Lane G forge / Lane P torch,
a_lane_akida_gpu_split). a_completeness_over_cheap: construction fixed BEFORE scoring; the
frozen bars are NOT moved after measuring.
"""
import json
import numpy as np
import h1163_tick_decode_metric as H

CAP_LADDER = [4, 6, 8, 12, 16, 24, 32, 48, 64]
PERM_SALT = 7919
N_REGIMES = H.N_REGIMES_AUDIO          # K = shared scene/regime count (= audio's K, 6)


# ====================================================================================
# ONE shared regime/scene timeline, rendered into 3 DIM-8 sub-vectors + a fused DIM-8.
# stage[t] is the SAME for all modalities (the "동시" = concurrent same-time fusion).
# ====================================================================================
def _shared_schedule(seed):
    """Build the SHARED regime/scene timeline stage[t] ONCE (same for all modalities),
    plus the per-modality fixed geometry (centers/drifts/patterns/projection). Returns a
    dict the per-modality renderers read so every modality sees the IDENTICAL stage[t]."""
    rng = np.random.default_rng(seed + 4242)
    K = N_REGIMES
    need = H.WARMUP + H.T + 1

    # --- the ONE shared scene timeline (recurring regimes, revisited) ---
    stages = np.empty(need, dtype=int)
    r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:
            r = int(rng.integers(K)); dwell = int(rng.integers(40, 90))
        stages[t] = r; dwell -= 1

    # --- AUDIO geometry: drifting-center recurring-regime tone (H.make_audio_stream-style) ---
    a_centers = rng.standard_normal((K, H.DIM)) * 5.0
    a_drifts = rng.standard_normal((K, H.DIM)); a_drifts /= np.linalg.norm(a_drifts, axis=1, keepdims=True); a_drifts *= 0.8

    # --- TEXT geometry: each regime = a "register" center in byte-feature space + small drift ---
    t_centers = rng.standard_normal((K, H.DIM)) * 5.0
    t_drifts = rng.standard_normal((K, H.DIM)); t_drifts /= np.linalg.norm(t_drifts, axis=1, keepdims=True); t_drifts *= 0.5

    # --- IMAGE geometry: a STATIC spatial pattern per scene (a still frame), far apart ---
    i_patterns = rng.standard_normal((K, H.DIM)) * 7.0     # far-apart scenes = big cuts (H_1186 video)

    # --- FIXED seeded random projection 24 -> 8 (NOT re-fit per arm/seed) ---
    P = rng.standard_normal((3 * H.DIM, H.DIM)) / np.sqrt(3 * H.DIM)

    return {"stages": stages, "K": K, "need": need,
            "a_centers": a_centers, "a_drifts": a_drifts,
            "t_centers": t_centers, "t_drifts": t_drifts,
            "i_patterns": i_patterns, "P": P}


def _render_submodalities(seed):
    """Render the three DIM-8 sub-streams (audio, text, image) on the SHARED stage[t]."""
    sch = _shared_schedule(seed)
    rng = np.random.default_rng(seed + 808)
    stages = sch["stages"]; need = sch["need"]
    Xa = np.empty((need, H.DIM)); Xt = np.empty((need, H.DIM)); Xi = np.empty((need, H.DIM))
    a_pos = sch["a_centers"][stages[0]].copy()
    t_pos = sch["t_centers"][stages[0]].copy()
    prev = stages[0]
    for t in range(need):
        r = stages[t]
        if r != prev:                     # scene/regime CUT: re-seat the drifting modalities
            a_pos = sch["a_centers"][r].copy()
            t_pos = sch["t_centers"][r].copy()
        # AUDIO: smooth drift within regime (recurring-regime tone)
        a_pos = a_pos + sch["a_drifts"][r] + rng.standard_normal(H.DIM) * 0.12
        Xa[t] = a_pos
        # TEXT: byte-feature-style register, small drift within regime
        t_pos = t_pos + sch["t_drifts"][r] + rng.standard_normal(H.DIM) * 0.10
        Xt[t] = t_pos
        # IMAGE: STATIC per-scene spatial pattern + per-tick spatial noise (still frame)
        Xi[t] = sch["i_patterns"][r] + rng.standard_normal(H.DIM) * 0.30
        prev = r
    return Xa, Xt, Xi, stages, sch["P"]


# Per-modality builders (each native DIM=8) + the FUSED builder (24->8 projection).
def make_audio_only(seed):
    Xa, _, _, stages, _ = _render_submodalities(seed)
    return Xa, stages


def make_text_only(seed):
    _, Xt, _, stages, _ = _render_submodalities(seed)
    return Xt, stages


def make_image_only(seed):
    _, _, Xi, stages, _ = _render_submodalities(seed)
    return Xi, stages


def make_fused(seed):
    """Concatenate the 3 DIM-8 sub-vectors -> 24-d, project to DIM=8 via the FIXED seeded
    projection P. This is the SIMULTANEOUS (동시) fusion: same stage[t] across all 3, fused
    BEFORE the grow/decode. Width stays DIM=8 (the grow_arm contract — see module docstring)."""
    Xa, Xt, Xi, stages, P = _render_submodalities(seed)
    fused24 = np.concatenate([Xa, Xt, Xi], axis=1)          # (need, 24)
    Xf = fused24 @ P                                         # (need, 8)
    assert Xf.shape[1] == H.DIM, "fused stream must be DIM=8 for grow_arm"
    return Xf, stages


BUILDERS = {
    "audio": make_audio_only,
    "text":  make_text_only,
    "image": make_image_only,
    "FUSED": make_fused,
}


# ====================================================================================
# Per-stream measurement: K* = argmax d(DERIVATIVE,METRONOME); derivative raw decode at K*;
# d_real / d_shuf at K* for the temporal test.
# ====================================================================================
def _curve_and_acc(builder, cap, shuffle):
    """At a given cap: per-seed DERIVATIVE & METRONOME decode (for d) AND the raw DERIVATIVE
    decode accuracy (for the super-additive comparison). Optionally seeded time-shuffle."""
    saved = H.MAX_CELLS
    H.MAX_CELLS = cap
    dec_d, dec_m = [], []
    for s in H.SEEDS:
        X, stages = builder(s)
        if shuffle:
            perm = np.random.RandomState(s + PERM_SALT).permutation(len(X))
            X = X[perm]; stages = np.asarray(stages)[perm]
        st_d, cs_d = H.grow_arm(X, stages, "DERIVATIVE", s)
        st_m, cs_m = H.grow_arm(X, stages, "METRONOME", s)
        dec_d.append(H.stage_decode_accuracy(st_d, cs_d, X, stages, N_REGIMES))
        dec_m.append(H.stage_decode_accuracy(st_m, cs_m, X, stages, N_REGIMES))
    H.MAX_CELLS = saved
    return dec_d, dec_m


def measure_stream(name, builder):
    """Find K*=argmax d(DERIVATIVE,METRONOME); return K*, per-seed derivative-acc@K*,
    d_real, d_shuf, drop."""
    curve = {}
    cache = {}
    for c in CAP_LADDER:
        dec_d, dec_m = _curve_and_acc(builder, c, shuffle=False)
        curve[c] = H.cohen_d_paired(dec_d, dec_m)
        cache[c] = (dec_d, dec_m)
    kstar = max(curve, key=curve.get)
    dec_d_star, dec_m_star = cache[kstar]
    d_real = curve[kstar]
    # temporal test: shuffle at K*
    dec_d_s, dec_m_s = _curve_and_acc(builder, kstar, shuffle=True)
    d_shuf = H.cohen_d_paired(dec_d_s, dec_m_s)
    return {
        "name": name, "K_star": kstar,
        "deriv_acc_per_seed": [float(x) for x in dec_d_star],
        "deriv_acc_mean": float(np.mean(dec_d_star)),
        "metro_acc_mean": float(np.mean(dec_m_star)),
        "d_real": float(d_real), "d_shuf": float(d_shuf), "drop": float(d_real - d_shuf),
        "curve": {str(c): float(curve[c]) for c in CAP_LADDER},
    }


def main():
    np.seterr(all="ignore")
    print("=== H_1189 — SIMULTANEOUS multi-modal (TEXT+AUDIO+IMAGE at the same tick): "
          "super-additive (F1) AND temporal (F2)? ===", flush=True)
    print(f"  shared scene timeline stage[t] drives all 3 modalities (동시); fused = "
          f"[audio|text|image] 24-d -> DIM=8 via FIXED seeded projection", flush=True)
    print(f"  cap ladder K={CAP_LADDER}; per-stream K*=argmax d(DERIVATIVE,METRONOME); "
          f"{len(H.SEEDS)} seeds; reuses H_1163 grow_arm/stage_decode VERBATIM\n", flush=True)

    res = {name: measure_stream(name, b) for name, b in BUILDERS.items()}
    for name in ("audio", "text", "image", "FUSED"):
        r = res[name]
        print(f"  {name:6s} K*={r['K_star']:3d}  deriv_acc={r['deriv_acc_mean']:.4f}  "
              f"metro_acc={r['metro_acc_mean']:.4f}  d_real={r['d_real']:+.3f}  "
              f"d_shuf={r['d_shuf']:+.3f}  drop={r['drop']:+.3f}", flush=True)
    print(f"  (decode chance = {1.0/N_REGIMES:.4f})\n", flush=True)

    # --- F1 SUPER-ADDITIVE: fused deriv-acc vs BEST single modality (per seed) ---
    singles = ("audio", "text", "image")
    n_seeds = len(H.SEEDS)
    best_single_per_seed = [max(res[m]["deriv_acc_per_seed"][i] for m in singles)
                            for i in range(n_seeds)]
    fused_per_seed = res["FUSED"]["deriv_acc_per_seed"]
    d_superadd = H.cohen_d_paired(fused_per_seed, best_single_per_seed)
    fused_minus_best_mean = float(np.mean(np.asarray(fused_per_seed) - np.asarray(best_single_per_seed)))
    f1 = bool(d_superadd >= 0.5)

    # which single modality was best on average (reporting)
    best_single_name = max(singles, key=lambda m: res[m]["deriv_acc_mean"])

    # --- F2 TEMPORAL: fused advantage killed by time-shuffle ---
    f2 = bool(res["FUSED"]["drop"] >= 0.5)

    supported = bool(f1 and f2)

    if supported:
        ruling = (
            f"SUPPORTED (SIMULTANEOUS-FUSION-HELPS-TEMPORALLY): fusing TEXT+AUDIO+IMAGE at the "
            f"SAME tick gives a SUPER-ADDITIVE decode benefit — FUSED derivative-acc beats the BEST "
            f"single modality ({best_single_name}) by d={d_superadd:+.2f} (Δ={fused_minus_best_mean:+.3f}, "
            f"F1 PASS) AND that advantage is TEMPORAL (fused drop={res['FUSED']['drop']:+.2f} on "
            f"time-shuffle, F2 PASS). 동시 (concurrent same-time) fusion manufactures a benefit the "
            f"MISALIGNED H_1170 cross-type pairing could not — the shared random projection + same-tick "
            f"alignment supplies the surface bridge H_1170 found necessary.")
    else:
        why = []
        if not f1:
            why.append(f"F1 fail: FUSED does NOT beat the best single modality ({best_single_name}) "
                       f"super-additively — d(fused - best_single)={d_superadd:+.2f} < 0.5 "
                       f"(Δacc={fused_minus_best_mean:+.3f}); fusion ~= best part, NOT super-additive "
                       f"(echoing H_1170's surface-gated collapse — label-only alignment is not enough)")
        if not f2:
            why.append(f"F2 fail: the FUSED advantage is NOT temporal — drop={res['FUSED']['drop']:+.2f} "
                       f"< 0.5 (d_real={res['FUSED']['d_real']:+.2f}, d_shuf={res['FUSED']['d_shuf']:+.2f})")
        ruling = "CLOSED-NEGATIVE: " + " | ".join(why)

    verdict = {
        "H": "H_1189",
        "title": "SIMULTANEOUS multi-modal input (TEXT+AUDIO+IMAGE at the same tick): does fusing 3 "
                 "concurrent modalities give the derivative-tick coverage mechanism a SUPER-ADDITIVE "
                 "benefit (fused > best single) AND is it TEMPORAL (killed by time-shuffle)?",
        "frozen_falsifier": {
            "F1": "FUSED derivative decode-acc beats BEST single modality, paired d(fused-best)>=0.5",
            "F2": "FUSED d(DERIVATIVE,METRONOME) advantage is temporal, drop=d_real-d_shuf>=0.5 at K*",
            "SUPPORTED": "F1 and F2 (simultaneous fusion helps super-additively AND temporally)",
            "metric": "clm-time-encoding STAGE-DECODE accuracy of the DERIVATIVE arm (p7, NOT perplexity)",
        },
        "cap_ladder": CAP_LADDER,
        "decode_chance": 1.0 / N_REGIMES,
        "per_stream": {name: {k: v for k, v in res[name].items()
                              if k not in ("curve", "deriv_acc_per_seed")} for name in res},
        "curves": {name: res[name]["curve"] for name in res},
        "F1_super_additive": {
            "best_single_modality_on_mean": best_single_name,
            "fused_deriv_acc_mean": res["FUSED"]["deriv_acc_mean"],
            "best_single_deriv_acc_mean": float(np.mean(best_single_per_seed)),
            "fused_minus_best_single_mean": fused_minus_best_mean,
            "d_fused_vs_best_single_paired": d_superadd, "bar": 0.5, "pass": f1,
            "note": "best_single = per-seed max over {audio,text,image} own-K* derivative acc (strong baseline)",
        },
        "F2_temporal": {"K_star": res["FUSED"]["K_star"], "d_real": res["FUSED"]["d_real"],
                        "d_shuf": res["FUSED"]["d_shuf"], "drop": res["FUSED"]["drop"],
                        "bar": 0.5, "pass": f2},
        "supported": supported,
        "ruling": ruling,
        "surface_vs_label_note": (
            "The 3 sub-modalities (drift-tone audio / byte-feature text / static spatial image) share "
            "ONLY the abstract regime LABEL stage[t], NOT a common surface alphabet (cf H_1170, where "
            "ONLY the monotone-byte text↔audio bridge survived). The fusion's surface bridge is the "
            "FIXED 24->8 random projection, which MIXES the three geometries into a shared 8-d surface. "
            "So this tests whether SIMULTANEITY (same stage, same t, fused before decode) + a shared "
            "projection surface manufactures the super-additive benefit that H_1170's MISALIGNED "
            "cross-type pairing could not. " + (
                "It DID — same-time alignment + the shared projection surface beat the best single part."
                if f1 else
                "It did NOT exceed the best single part — consistent with H_1170: label-only alignment "
                "(no preserved per-modality surface correspondence) does not manufacture super-additivity; "
                "the fused projection only RECOVERS the strongest part, it does not exceed it.")),
        "scope": "TOY ($0 CPU numpy, %d seeds). Reuses H_1163 grow_arm/stage_decode_accuracy/"
                 "cohen_d_paired/SEEDS/N_REGIMES_AUDIO VERBATIM. The 3 'modalities' are TOY synthetic "
                 "geometries (drift-tone / byte-feature / static spatial pattern) sharing a SAME 24->8 "
                 "random-projection surface — NOT real TTS / images / learned encoders (cf H_1170 toy "
                 "renderings). DIM=8 (the grow_arm contract); fused 24-d is projected to 8, NOT widened. "
                 "Live CORE engine_mitosis_tick + real modalities + production scale UNVERIFIED "
                 "(a_toy_scale_recheck, a_scale_honest_scope). Lane-M gradient-free growth lane "
                 "(separate from Lane A AKIDA / Lane G forge / Lane P torch, a_lane_akida_gpu_split)." % n_seeds,
    }
    print("=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1189_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
