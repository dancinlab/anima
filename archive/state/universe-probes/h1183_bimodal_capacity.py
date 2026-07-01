"""
H_1183 — is the derivative-tick advantage curve genuinely BIMODAL at fixed complexity,
or was H_1182's two-peak hint just coarse-ladder aliasing? (Lane 2 / MAIN hands-on
discovery rung, MITOSIS-ENGINE domain)

H_1182 (🔴, scaling-law refuted) surfaced — as a close-watch SERENDIP — that the
d(DERIVATIVE,METRONOME) stage-decode curve over cell-count looks BIMODAL: a mid-capacity
peak (~24-32) AND a low-capacity K=4 scarcity peak that wins at high regime-count. But
H_1182 used a COARSE capacity ladder, so the "two peaks" could be ladder aliasing
(under-sampling a single bumpy ridge). H_1183 settles it with a FINE ladder at FIXED
complexity (N=10 regimes, where H_1182 saw the low-K peak win).

If the curve is genuinely bimodal on a fine ladder — two separated local maxima with a
real valley between them — then there are TWO distinct advantage regimes for event-driven
growth (scarcity-placement at very low K, coverage-completion at mid K), a sharper claim
than H_1178's single inverted-U. If it collapses to one bump, the H_1182 bimodality was
an artifact and H_1178's unimodal picture generalizes.

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, the H_1163 seeds;
fixed N_REGIMES=10; metric = d(DERIVATIVE,METRONOME) on stage-decode per cap):
  fine ladder K = {3,4,5,6,8,10,12,16,20,24,28,32,40,48,56,64,80,96}
  a "peak" = an interior cap whose d is >= both neighbors (plateau ties broken by strict
  on at least one side), with d >= 0.5 (clears a real-advantage floor).
  F1 BIMODAL      : >= 2 such peaks, AND the two highest are in DIFFERENT capacity bands
                    (one low: K <= 8; one mid/high: K >= 20) — not two adjacent samples.
  F2 REAL-VALLEY  : between the two highest peaks, min(d) <= min(peak1_d, peak2_d) - 0.3
                    (a genuine dip, not a plateau / monotone shoulder).
  SUPPORTED (BIMODAL-CONFIRMED) iff F1 AND F2 -> two distinct advantage regimes are real
  on a fine ladder, not coarse aliasing. Otherwise CLOSED-NEGATIVE (a_paper_negative_ok):
  the H_1182 two-peak hint was coarse-ladder aliasing; one ridge.

toy ($0 CPU numpy, deterministic). Reuses UNIVERSE/h1163_tick_decode_metric.py + h1178/
h1182 sweep pattern VERBATIM (grow_arm / stage_decode_accuracy / cohen_d_paired /
make_audio_stream / SEEDS), only N_REGIMES_AUDIO pinned to 10 + a fine cap ladder. Live
CORE + scale UNVERIFIED (a_scale_honest_scope). Lane-M growth lane.
"""
import json
import numpy as np
import h1163_tick_decode_metric as H

N_FIXED = 10
CAP_LADDER = [3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 28, 32, 40, 48, 56, 64, 80, 96]


def d_at_cap(n_regimes, cap):
    saved_cells, saved_reg = H.MAX_CELLS, H.N_REGIMES_AUDIO
    H.MAX_CELLS = cap
    H.N_REGIMES_AUDIO = n_regimes
    dec_d, dec_m = [], []
    for s in H.SEEDS:
        X, stages = H.make_audio_stream(s)
        st_d, cs_d = H.grow_arm(X, stages, "DERIVATIVE", s)
        st_m, cs_m = H.grow_arm(X, stages, "METRONOME", s)
        dec_d.append(H.stage_decode_accuracy(st_d, cs_d, X, stages, n_regimes))
        dec_m.append(H.stage_decode_accuracy(st_m, cs_m, X, stages, n_regimes))
    H.MAX_CELLS, H.N_REGIMES_AUDIO = saved_cells, saved_reg
    return H.cohen_d_paired(dec_d, dec_m)


def find_peaks(caps, ds, floor=0.5):
    """interior local maxima with d>=floor; >= one strict neighbor (plateau-robust)."""
    peaks = []
    for i in range(1, len(ds) - 1):
        if ds[i] >= floor and ds[i] >= ds[i - 1] and ds[i] >= ds[i + 1] \
           and (ds[i] > ds[i - 1] or ds[i] > ds[i + 1]):
            peaks.append((caps[i], ds[i], i))
    return peaks


def main():
    np.seterr(all="ignore")
    print(f"=== H_1183 — is the derivative-tick advantage curve BIMODAL at fixed N={N_FIXED} "
          f"(fine ladder), or was H_1182 coarse-ladder aliasing? ===", flush=True)
    print(f"  fine cap ladder K={CAP_LADDER}; metric d(DERIVATIVE,METRONOME) stage-decode; "
          f"{len(H.SEEDS)} seeds; reuses H_1163+h1182 VERBATIM\n", flush=True)

    ds = []
    for c in CAP_LADDER:
        d = d_at_cap(N_FIXED, c)
        ds.append(d)
        print(f"  K={c:3d}  d(deriv,metro)={d:+.3f}", flush=True)

    peaks = find_peaks(CAP_LADDER, ds, floor=0.5)
    peaks_sorted = sorted(peaks, key=lambda p: -p[1])
    top2 = peaks_sorted[:2]

    f1 = False
    f2 = False
    valley_min = None
    if len(top2) == 2:
        (k1, d1, i1), (k2, d2, i2) = top2
        lo_k, hi_k = (k1, k2) if k1 < k2 else (k2, k1)
        f1 = (lo_k <= 8) and (hi_k >= 20)
        a, b = sorted((i1, i2))
        valley_min = min(ds[a:b + 1])
        f2 = valley_min <= min(d1, d2) - 0.3

    supported = bool(f1 and f2)
    verdict = {
        "H": "H_1183",
        "title": "is the derivative-tick stage-decode advantage curve genuinely BIMODAL at fixed N=10 "
                 "on a fine capacity ladder (two distinct advantage regimes), or was H_1182's two-peak "
                 "hint coarse-ladder aliasing?",
        "N_fixed": N_FIXED,
        "cap_ladder": CAP_LADDER,
        "d_curve": {str(c): d for c, d in zip(CAP_LADDER, ds)},
        "peaks_d_ge_0.5": [{"K": k, "d": d} for k, d, _ in peaks_sorted],
        "top2_peaks": [{"K": k, "d": d} for k, d, _ in top2],
        "valley_min_between_top2": valley_min,
        "F1_bimodal_separated": {"need": "2 peaks, one K<=8 + one K>=20", "pass": bool(f1)},
        "F2_real_valley": {"valley_min": valley_min, "rule": "<= min(peak_d) - 0.3", "pass": bool(f2)},
        "supported": supported,
        "ruling": (
            f"SUPPORTED (BIMODAL-CONFIRMED): on a fine ladder at N={N_FIXED} the advantage curve has TWO "
            f"separated peaks (peaks at K={[k for k,_,_ in top2]}) with a real valley "
            f"between — H_1182's bimodality is NOT coarse aliasing. Two distinct event-driven advantage "
            f"regimes exist: scarcity-placement (very low K) and coverage-completion (mid K). Sharpens "
            f"H_1178's single inverted-U into a two-regime structure."
            if supported else
            f"CLOSED-NEGATIVE: the fine-ladder curve at N={N_FIXED} is NOT cleanly bimodal "
            f"(F1 separated-peaks={f1}, F2 real-valley={f2}; peaks={[(k,round(d,2)) for k,d,_ in peaks_sorted]}, "
            f"valley_min={valley_min}). H_1182's two-peak hint was coarse-ladder aliasing / one bumpy ridge; "
            f"H_1178's unimodal picture is not split by a fine ladder. a_paper_negative_ok."),
        "scope": "TOY ($0 CPU numpy, %d seeds, fixed N=10). Reuses UNIVERSE/h1163_tick_decode_metric.py + "
                 "h1182 sweep VERBATIM; only N_REGIMES_AUDIO pinned + fine cap ladder. Live CORE + scale "
                 "UNVERIFIED (a_scale_honest_scope)." % len(H.SEEDS),
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1183_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
