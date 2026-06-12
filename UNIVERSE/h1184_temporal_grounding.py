"""
H_1184 — is the derivative-tick advantage TEMPORALLY GROUNDED, or a static-structure
artifact? (Lane 2 / MAIN hands-on discovery rung, MITOSIS-ENGINE domain)

NEW AXIS (temporality) — pursues the Lane-1 SERENDIP "temporal-blindness thread": H_1179
(live field) + H_1180 (kosmos lane-split) were both shuffle-INVARIANT — blind to time
order. The event-driven (DERIVATIVE) tick, by contrast, fires on |X[t]-X[t-1]| (a CHANGE
between consecutive steps), so it SHOULD depend on real temporal structure. H_1178/1182/
1183 showed the derivative tick has a (bimodal) decode advantage over the blind metronome.
H_1184 asks the grounding question: is that advantage CREATED by real temporal order, or
would it survive a time-shuffle (=> a static-structure artifact, temporally blind like the
H_1179/1180 substrates)?

TEST: at the two H_1183 advantage peaks (K=4 scarcity-placement, K=40 coverage-completion),
compare d(DERIVATIVE,METRONOME) on (a) the REAL ordered stream vs (b) a TIME-SHUFFLED stream
(same value distribution + same (X,stage) pairs, but consecutive-step adjacency destroyed by
a seeded permutation). Shuffling makes |X[t]-X[t-1]| random => the derivative gate fires at
meaningless moments. The metronome (blind clock) is order-agnostic, so its behavior is
unchanged. If the derivative advantage is temporal, the shuffle should KILL it.

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, the H_1163 seeds;
fixed N_REGIMES=10; peaks K in {4,40} from H_1183; metric d(DERIVATIVE,METRONOME) on
stage-decode):
  for each peak cap K: d_real = d on ordered stream; d_shuf = d on time-shuffled stream
  (seeded per-seed permutation of the time axis applied to BOTH X and stages together).
  F1 ADVANTAGE-REAL  : d_real >= 0.5 at BOTH peaks (the advantage is present when ordered).
  F2 SHUFFLE-KILLS   : (d_real - d_shuf) >= 0.5 at BOTH peaks (>=half the advantage is
                       destroyed by removing temporal order => temporally grounded).
  SUPPORTED (TEMPORALLY-GROUNDED) iff F1 AND F2 -> the event-tick advantage is created by
  real temporal structure (unlike the H_1179/1180 temporally-blind substrates); the winning
  mechanism is the one that is NOT shuffle-invariant. Otherwise CLOSED-NEGATIVE
  (a_paper_negative_ok): the advantage survives shuffling -> a static-structure artifact.

toy ($0 CPU numpy, deterministic). Reuses UNIVERSE/h1163_tick_decode_metric.py VERBATIM
(grow_arm / stage_decode_accuracy / cohen_d_paired / make_audio_stream / SEEDS); the only
new operation is a seeded time-axis permutation of (X, stages). Live CORE + scale UNVERIFIED
(a_scale_honest_scope). Lane-M growth lane.
"""
import json
import numpy as np
import h1163_tick_decode_metric as H

N_FIXED = 10
PEAKS = [4, 40]          # the two H_1183 advantage peaks (scarcity / coverage)
PERM_SALT = 7919         # fixed prime offset so the shuffle RNG != the stream RNG


def d_at(cap, shuffle):
    saved_cells, saved_reg = H.MAX_CELLS, H.N_REGIMES_AUDIO
    H.MAX_CELLS = cap
    H.N_REGIMES_AUDIO = N_FIXED
    dec_d, dec_m = [], []
    for s in H.SEEDS:
        X, stages = H.make_audio_stream(s)
        if shuffle:
            perm = np.random.RandomState(s + PERM_SALT).permutation(len(X))
            X = X[perm]
            stages = np.asarray(stages)[perm]
        st_d, cs_d = H.grow_arm(X, stages, "DERIVATIVE", s)
        st_m, cs_m = H.grow_arm(X, stages, "METRONOME", s)
        dec_d.append(H.stage_decode_accuracy(st_d, cs_d, X, stages, N_FIXED))
        dec_m.append(H.stage_decode_accuracy(st_m, cs_m, X, stages, N_FIXED))
    H.MAX_CELLS, H.N_REGIMES_AUDIO = saved_cells, saved_reg
    return H.cohen_d_paired(dec_d, dec_m)


def main():
    np.seterr(all="ignore")
    print("=== H_1184 — is the derivative-tick advantage TEMPORALLY GROUNDED "
          "(killed by time-shuffle) or a static artifact? ===", flush=True)
    print(f"  peaks K={PEAKS} (H_1183 scarcity/coverage); fixed N={N_FIXED}; "
          f"d(DERIVATIVE,METRONOME) stage-decode; {len(H.SEEDS)} seeds; reuses H_1163 VERBATIM\n",
          flush=True)

    rows = {}
    for k in PEAKS:
        d_real = d_at(k, shuffle=False)
        d_shuf = d_at(k, shuffle=True)
        rows[k] = {"d_real": d_real, "d_shuf": d_shuf, "drop": d_real - d_shuf}
        print(f"  K={k:3d}  d_real={d_real:+.3f}  d_shuf(time-shuffled)={d_shuf:+.3f}  "
              f"drop={d_real - d_shuf:+.3f}", flush=True)

    f1 = all(rows[k]["d_real"] >= 0.5 for k in PEAKS)
    f2 = all(rows[k]["drop"] >= 0.5 for k in PEAKS)
    supported = bool(f1 and f2)

    verdict = {
        "H": "H_1184",
        "title": "is the derivative-tick decode advantage TEMPORALLY GROUNDED (destroyed by a "
                 "time-shuffle that keeps the value distribution but breaks temporal order), or a "
                 "static-structure artifact — pursuing the Lane-1 temporal-blindness thread?",
        "N_fixed": N_FIXED,
        "peaks": PEAKS,
        "per_peak": {str(k): rows[k] for k in PEAKS},
        "F1_advantage_real": {"need": "d_real>=0.5 at both peaks", "pass": bool(f1)},
        "F2_shuffle_kills": {"need": "(d_real-d_shuf)>=0.5 at both peaks", "pass": bool(f2)},
        "supported": supported,
        "ruling": (
            f"SUPPORTED (TEMPORALLY-GROUNDED): the event-tick advantage is created by REAL temporal "
            f"structure — present on the ordered stream (d_real>=0.5) and DESTROYED by a time-shuffle "
            f"(drop>=0.5) at BOTH peaks K={PEAKS}. The winning mechanism is the one that is NOT "
            f"shuffle-invariant, directly contrasting the temporally-BLIND H_1179 (live field) and "
            f"H_1180 (kosmos lane-split) substrates. The derivative tick reads TIME; the metronome and "
            f"the blind substrates do not."
            if supported else
            f"CLOSED-NEGATIVE: the derivative-tick advantage is NOT cleanly temporal-grounded at toy "
            f"scale (F1 advantage-real={f1}, F2 shuffle-kills={f2}; per-peak={rows}). Either the "
            f"advantage is absent when expected, or it survives the time-shuffle (a static-structure "
            f"artifact, temporally blind like H_1179/1180). a_paper_negative_ok."),
        "scope": "TOY ($0 CPU numpy, %d seeds, fixed N=10, peaks from H_1183). Reuses "
                 "UNIVERSE/h1163_tick_decode_metric.py VERBATIM; only added op = a seeded time-axis "
                 "permutation of (X,stages). The shuffle preserves the value distribution + (X,stage) "
                 "pairing, isolating temporal ORDER as the manipulated variable. Live CORE + scale "
                 "UNVERIFIED (a_scale_honest_scope)." % len(H.SEEDS),
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1184_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
