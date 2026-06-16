"""
H_1185 — does the H_1184 temporal/non-temporal SPLIT of the bimodal advantage hold on the
TEXT stream too, or is it AUDIO-specific? (Lane 2 / MAIN hands-on discovery rung,
MITOSIS-ENGINE domain)

H_1184 found, on the AUDIO stream, that the two H_1183 bimodal advantage peaks are
MECHANISTICALLY OPPOSITE on temporality: the mid-K COVERAGE peak (K=40) is genuinely
event/time-driven (a time-shuffle KILLS it), while the low-K SCARCITY peak (K=4) is NON-
temporal variance-spread (a time-shuffle IMPROVES it). H_1185 asks whether that DICHOTOMY
is modality-general or an AUDIO artifact, by re-running the identical shuffle test on the
TEXT stream (real bytes, N_STAGES_TEXT=4).

The transferable H_1184 claim is the DICHOTOMY, not the exact d's. So the frozen falsifier
here is about the SIGN PATTERN reproducing: high-K coverage shuffle-DROP positive (temporal),
low-K scarcity shuffle-DROP negative (non-temporal).

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, the H_1163 seeds; TEXT
stream, N_STAGES_TEXT=4; same two cap regimes K in {4,40} as H_1184; metric
d(DERIVATIVE,METRONOME) on stage-decode):
  drop(K) = d_real(K) - d_shuf(K)   (time-shuffle = seeded permutation of (X,stages))
  F1 COVERAGE-TEMPORAL : drop(40) >= 0.5  (high-K coverage advantage is killed by shuffle)
  F2 SCARCITY-NONTEMPORAL : drop(4) <= 0.0 (low-K scarcity advantage is NOT killed —
       shuffle leaves it equal or better, the H_1184 non-temporal signature)
  SUPPORTED (DICHOTOMY-GENERAL) iff F1 AND F2 -> the temporal/non-temporal split of the two
  peaks reproduces on TEXT; the dichotomy is modality-general, not an AUDIO artifact.
  Otherwise CLOSED-NEGATIVE (a_paper_negative_ok): the split is AUDIO-specific.

toy ($0 CPU numpy, deterministic). Reuses UNIVERSE/h1163_tick_decode_metric.py VERBATIM
(grow_arm / stage_decode_accuracy / cohen_d_paired / make_text_stream / SEEDS / N_STAGES_TEXT);
the only added op = a seeded time-axis permutation of (X,stages), identical to H_1184. Live
CORE + scale UNVERIFIED (a_scale_honest_scope). Lane-M growth lane.
"""
import json
import numpy as np
import h1163_tick_decode_metric as H

PEAKS = [4, 40]
PERM_SALT = 7919


def d_at(cap, shuffle):
    saved_cells = H.MAX_CELLS
    H.MAX_CELLS = cap
    n_stages = H.N_STAGES_TEXT
    dec_d, dec_m = [], []
    for s in H.SEEDS:
        X, stages = H.make_text_stream(s)
        if shuffle:
            perm = np.random.RandomState(s + PERM_SALT).permutation(len(X))
            X = X[perm]
            stages = np.asarray(stages)[perm]
        st_d, cs_d = H.grow_arm(X, stages, "DERIVATIVE", s)
        st_m, cs_m = H.grow_arm(X, stages, "METRONOME", s)
        dec_d.append(H.stage_decode_accuracy(st_d, cs_d, X, stages, n_stages))
        dec_m.append(H.stage_decode_accuracy(st_m, cs_m, X, stages, n_stages))
    H.MAX_CELLS = saved_cells
    return H.cohen_d_paired(dec_d, dec_m)


def main():
    np.seterr(all="ignore")
    print("=== H_1185 — does the H_1184 temporal/non-temporal SPLIT hold on the TEXT stream "
          "(modality-general) or is it AUDIO-specific? ===", flush=True)
    print(f"  TEXT stream (N_STAGES={H.N_STAGES_TEXT}); peaks K={PEAKS}; d(DERIVATIVE,METRONOME) "
          f"stage-decode; {len(H.SEEDS)} seeds; reuses H_1163+h1184 VERBATIM\n", flush=True)

    rows = {}
    for k in PEAKS:
        d_real = d_at(k, shuffle=False)
        d_shuf = d_at(k, shuffle=True)
        rows[k] = {"d_real": d_real, "d_shuf": d_shuf, "drop": d_real - d_shuf}
        print(f"  K={k:3d}  d_real={d_real:+.3f}  d_shuf={d_shuf:+.3f}  drop={d_real - d_shuf:+.3f}",
              flush=True)

    f1 = rows[40]["drop"] >= 0.5
    f2 = rows[4]["drop"] <= 0.0
    supported = bool(f1 and f2)

    verdict = {
        "H": "H_1185",
        "title": "does the H_1184 temporal/non-temporal split of the two bimodal peaks (coverage=temporal, "
                 "scarcity=non-temporal) reproduce on the TEXT stream, or is it AUDIO-specific?",
        "stream": "TEXT", "N_stages": H.N_STAGES_TEXT, "peaks": PEAKS,
        "per_peak": {str(k): rows[k] for k in PEAKS},
        "F1_coverage_temporal": {"need": "drop(40)>=0.5", "value": rows[40]["drop"], "pass": bool(f1)},
        "F2_scarcity_nontemporal": {"need": "drop(4)<=0.0", "value": rows[4]["drop"], "pass": bool(f2)},
        "supported": supported,
        "ruling": (
            f"SUPPORTED (DICHOTOMY-GENERAL): the H_1184 temporal/non-temporal split reproduces on TEXT — "
            f"the K=40 coverage peak is killed by the time-shuffle (drop={rows[40]['drop']:+.2f}>=0.5, "
            f"temporal) while the K=4 scarcity peak is NOT (drop={rows[4]['drop']:+.2f}<=0, non-temporal). "
            f"The dichotomy is modality-general: only the coverage peak reads time, on both AUDIO and TEXT."
            if supported else
            f"CLOSED-NEGATIVE: the H_1184 split does NOT cleanly reproduce on TEXT "
            f"(F1 coverage-temporal={f1} drop(40)={rows[40]['drop']:+.2f}; F2 scarcity-nontemporal={f2} "
            f"drop(4)={rows[4]['drop']:+.2f}). The temporal/non-temporal dichotomy may be AUDIO-specific "
            f"or the text stage-geometry shifts the peak caps. a_paper_negative_ok."),
        "scope": "TOY ($0 CPU numpy, %d seeds, TEXT real-bytes stream, N_stages=4). Reuses "
                 "UNIVERSE/h1163_tick_decode_metric.py VERBATIM; only added op = seeded time-axis "
                 "permutation of (X,stages), identical to H_1184. NOTE: text has 4 stages vs audio 10, so "
                 "K=4/K=40 map to different cells-per-stage ratios — a confound the verdict flags. Live "
                 "CORE + scale UNVERIFIED (a_scale_honest_scope)." % len(H.SEEDS),
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1185_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
