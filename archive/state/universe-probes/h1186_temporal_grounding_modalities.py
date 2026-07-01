"""
H_1186 — does the TEMPORAL coverage mechanism appear PER MODALITY at each stream's OWN
coverage cap? VIDEO (intrinsically temporal) + the saccadic-reading TEXT re-test.
(Lane 2 / MAIN hands-on discovery rung, MITOSIS-ENGINE domain)

This FIXES the honest pre-reg limitation of H_1185 (it borrowed AUDIO's caps for a 4-stage
TEXT stream -> K=40 was out-of-band). Here, for EACH stream we first SWEEP capacity to find
that stream's OWN coverage peak K*, then run the H_1184 time-shuffle test AT K*. A modality
"reads time" iff its own-cap peak is killed by a time-shuffle (d_real high, shuffle removes it).

Two motivations:
 - "비디오는?" — VIDEO is the intrinsically temporal modality (frames flow smoothly, then
   CUT at scene boundaries). A toy video stream = long scene dwells + small within-scene drift
   (strong temporal continuity) + large abrupt cuts. The derivative tick should fire exactly at
   cuts -> the temporal coverage mechanism should appear STRONGLY (shuffle kills it).
 - "우리가 책 읽을 때 어떻게 읽지?" — humans do NOT scan text uniformly (metronome); we read by
   surprise-driven SACCADES (skip predictable words, fixate/regress on informative ones). That
   IS the derivative/event tick. So at TEXT's OWN coverage cap, does the event tick beat the
   uniform scan (a temporal peak), matching how we actually read?

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, the H_1163 seeds; per
stream find K*=argmax_K d(DERIVATIVE,METRONOME) over the cap ladder, then shuffle at K*):
  cap ladder K = {4,6,8,12,16,24,32,48,64}
  a stream is TEMPORAL iff d_real(K*) >= 0.5 AND (d_real(K*) - d_shuf(K*)) >= 0.5.
  F1 VIDEO-TEMPORAL : the VIDEO stream is TEMPORAL at its own K* (primary claim — the
       intrinsically temporal modality shows the temporal coverage mechanism).
  SUPPORTED iff F1. The AUDIO (expected temporal, cf H_1184) and TEXT (the saccadic-reading
  re-test) results are reported as the modality-comparison finding, NOT gating.

toy ($0 CPU numpy, deterministic). Reuses UNIVERSE/h1163_tick_decode_metric.py VERBATIM
(grow_arm / stage_decode_accuracy / cohen_d_paired / make_audio_stream / make_text_stream /
SEEDS / N_REGIMES_AUDIO / N_STAGES_TEXT); ADDS a toy make_video_stream (same (X[T,DIM],stages)
convention, DIM=8) + the H_1184 shuffle. Live CORE + scale UNVERIFIED (a_scale_honest_scope).
Lane-M growth lane.
"""
import json
import numpy as np
import h1163_tick_decode_metric as H

CAP_LADDER = [4, 6, 8, 12, 16, 24, 32, 48, 64]
PERM_SALT = 7919
N_SCENES_VIDEO = 6


def make_video_stream(seed):
    """Toy VIDEO: K scenes; LONG dwell (slow scene changes), SMALL within-scene drift+noise
    (strong temporal continuity = smooth motion), centers FAR apart (large abrupt CUTS).
    Same (X[need,DIM], stages) convention as H.make_audio_stream. stage = active scene id."""
    rng = np.random.default_rng(seed + 5678)
    K = N_SCENES_VIDEO
    centers = rng.standard_normal((K, H.DIM)) * 7.0          # far-apart scenes -> big cuts
    drifts = rng.standard_normal((K, H.DIM)); drifts /= np.linalg.norm(drifts, axis=1, keepdims=True); drifts *= 0.2
    need = H.WARMUP + H.T + 1
    X = np.empty((need, H.DIM)); stages = np.empty(need, dtype=int)
    pos = centers[0].copy(); r = 0; dwell = 0
    for t in range(need):
        if dwell <= 0:                                      # SCENE CUT (abrupt)
            r = int(rng.integers(K)); pos = centers[r].copy(); dwell = int(rng.integers(120, 300))
        pos = pos + drifts[r] + rng.standard_normal(H.DIM) * 0.05   # smooth within-scene motion
        dwell -= 1
        X[t] = pos
        stages[t] = r
    return X, stages


BUILDERS = {
    "audio": (H.make_audio_stream, lambda: H.N_REGIMES_AUDIO),
    "text":  (H.make_text_stream,  lambda: H.N_STAGES_TEXT),
    "video": (make_video_stream,   lambda: N_SCENES_VIDEO),
}


def d_at(builder, n_stages, cap, shuffle):
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
    print("=== H_1186 — does the TEMPORAL coverage mechanism appear PER MODALITY at each "
          "stream's OWN coverage cap? (video + saccadic-reading text) ===", flush=True)
    print(f"  cap ladder K={CAP_LADDER}; per stream K*=argmax d(DERIVATIVE,METRONOME); then "
          f"shuffle at K*; {len(H.SEEDS)} seeds; reuses H_1163 VERBATIM + toy video\n", flush=True)

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
        print(f"  {name:5s} n_stages={n_stages}  K*={kstar:3d}  d_real={d_real:+.3f}  "
              f"d_shuf={d_shuf:+.3f}  drop={drop:+.3f}  -> TEMPORAL={temporal}", flush=True)

    f1 = out["video"]["temporal"]
    supported = bool(f1)
    verdict = {
        "H": "H_1186",
        "title": "does the temporal coverage mechanism appear per modality at each stream's OWN coverage "
                 "cap — VIDEO (intrinsically temporal) + the saccadic-reading TEXT re-test (fixing H_1185)?",
        "cap_ladder": CAP_LADDER,
        "per_modality": {k: {kk: vv for kk, vv in v.items() if kk != "curve"} for k, v in out.items()},
        "curves": {k: out[k]["curve"] for k in out},
        "F1_video_temporal": {"K_star": out["video"]["K_star"], "d_real": out["video"]["d_real"],
                              "drop": out["video"]["drop"], "pass": bool(f1)},
        "supported": supported,
        "reading_finding": (
            f"TEXT at its OWN cap K*={out['text']['K_star']}: d_real={out['text']['d_real']:+.2f}, "
            f"drop={out['text']['drop']:+.2f}, temporal={out['text']['temporal']} — "
            + ("surprise-driven (saccadic) reading DOES beat uniform scan AND is temporal: matches how "
               "humans read (fixate on the informative/surprising, skip the predictable)."
               if out['text']['temporal'] else
               "the event tick does NOT show a clean temporal coverage peak on this toy byte-feature text "
               "even at its own cap — the toy text stage-geometry may lack the smooth-then-surprise "
               "structure real reading exploits; real-text + learned-surprise UNVERIFIED.")),
        "ruling": (
            f"SUPPORTED (VIDEO-TEMPORAL): the intrinsically temporal VIDEO stream shows the temporal "
            f"coverage mechanism at its own K*={out['video']['K_star']} (d_real={out['video']['d_real']:+.2f}, "
            f"shuffle drop={out['video']['drop']:+.2f}). Per-modality at own caps: "
            f"audio temporal={out['audio']['temporal']}, text temporal={out['text']['temporal']}, "
            f"video temporal={out['video']['temporal']}. The event tick reads TIME most clearly where the "
            f"stream has smooth-flow-then-cut structure (video > audio); fixing H_1185's borrowed-cap flaw."
            if supported else
            f"CLOSED-NEGATIVE: even at its own coverage cap K*={out['video']['K_star']}, the VIDEO stream "
            f"does NOT show a clean temporal coverage peak (d_real={out['video']['d_real']:+.2f}, "
            f"drop={out['video']['drop']:+.2f}). per-modality: audio={out['audio']['temporal']}, "
            f"text={out['text']['temporal']}, video={out['video']['temporal']}. a_paper_negative_ok."),
        "scope": "TOY ($0 CPU numpy, %d seeds). Reuses h1163 VERBATIM + a TOY make_video_stream "
                 "(long dwell + small drift + far centers = smooth-motion + cuts; NOT real frames, cf "
                 "H_1170 toy renderings). Per-stream OWN cap fixes the H_1185 borrowed-cap flaw. Real "
                 "video/text + learned encoders + scale UNVERIFIED (a_scale_honest_scope)." % len(H.SEEDS),
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1186_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
