"""
H_1178 — is there a CRITICAL CAPACITY for derivative-tick gating? (Lane 2 / MAIN
hands-on discovery rung, MITOSIS-ENGINE domain)

H_1160 (🔴) found the cell-division tick-gate {METRONOME/POSITIONAL/DERIVATIVE/NOGATE}
is irrelevant on next-step PREDICTION. H_1163 (🔴 at the frozen scarce cap=6) found,
in its NON-SCORING capacity diagnostic, that on a STAGE-DECODE metric the derivative
advantage d(deriv,metro) is a CAPACITY-WINDOW effect: cap6 -0.15 -> cap16 +0.74 ->
cap32 +1.15 -> cap64 +0.06 — it RISES then FALLS, an inverted-U over cell-count.

THE DISCOVERY HOOK (why this is a Lane-2 rung, not a batch one): that inverted-U is
the SAME shape the engine shows over the COUPLING axis — faithful-Phi peaks at the
critical gamma (H_1158) and the super-additive surplus peaks at the critical gamma
(H_1167). If the derivative-tick advantage ALSO peaks at an intermediate CAPACITY
(an interior argmax over cell-count), then CRITICALITY recurs on a THIRD axis: the
benefit of event-driven structure-growth is maximal at a CRITICAL CAPACITY K*, just
as integration/super-additivity are maximal at a critical coupling. That cross-axis
recurrence is the thing a close-watched single rung can NOTICE that an autonomous
batch (which would only log the pass/fail) would miss.

H_1178 promotes H_1163's non-scoring diagnostic to a FROZEN-FALSIFIER claim on a
FINE capacity ladder, reusing the H_1163 substrate VERBATIM (import; no re-derivation).

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, the H_1163 seeds;
metric = stage-decode d(DERIVATIVE, METRONOME), paired Cohen's d, p7):
  ladder K = {6, 8, 12, 16, 24, 32, 48, 64, 96}  (fine, spans scarce->saturated)
  F1 INTERIOR-PEAK : argmax_K d(deriv,metro) is INTERIOR (not the smallest K=6 nor the
     largest K=96) — the advantage peaks at an intermediate capacity.
  F2 INVERTED-U    : d(peak) - max(d(K=6), d(K=96)) >= 0.8 AND d(peak) >= 0.8 (a real
     hump that clears the decode-advantage bar, not a flat/monotone drift).
  F3 RISE-THEN-FALL: d is non-decreasing up to K* and non-increasing after (allowing
     one reversal for noise) — the curve is unimodal, not multi-modal noise.
  SUPPORTED (CRITICAL-CAPACITY) iff F1 AND F2 AND F3 -> there is a critical capacity K*
  where event-driven (derivative) tick-gating is maximally beneficial; criticality
  recurs on the CAPACITY axis (echoing the coupling-axis peaks of H_1158 / H_1167).
  Otherwise CLOSED-NEGATIVE (a_paper_negative_ok): the H_1163 window was noise / not a
  clean inverted-U.

toy ($0 CPU numpy, deterministic). Reuses UNIVERSE/h1163_tick_decode_metric.py
substrate VERBATIM (grow_arm / stage_decode_accuracy / cohen_d_paired / make_audio_stream
/ SEEDS). Live CORE + scale UNVERIFIED (a_scale_honest_scope). Lane-M growth lane.
"""
import json
import numpy as np
import h1163_tick_decode_metric as H


LADDER = [6, 8, 12, 16, 24, 32, 48, 64, 96]


def d_deriv_vs_metro_at_cap(builder, n_stages, cap):
    """Paired Cohen's d(DERIVATIVE, METRONOME) on STAGE-DECODE at a given MAX_CELLS.
    Reuses H_1163's grow_arm + stage_decode_accuracy + cohen_d_paired VERBATIM."""
    saved = H.MAX_CELLS
    H.MAX_CELLS = cap
    dec_d, dec_m = [], []
    bs_d = []
    for s in H.SEEDS:
        X, stages = builder(s)
        st_d, cs_d = H.grow_arm(X, stages, "DERIVATIVE", s)
        st_m, cs_m = H.grow_arm(X, stages, "METRONOME", s)
        dec_d.append(H.stage_decode_accuracy(st_d, cs_d, X, stages, n_stages))
        dec_m.append(H.stage_decode_accuracy(st_m, cs_m, X, stages, n_stages))
        bs_d.append(len(set(int(c) for c in cs_d if c >= 0)))
    H.MAX_CELLS = saved
    d = H.cohen_d_paired(dec_d, dec_m)
    return d, float(np.mean(dec_d)), float(np.mean(dec_m)), float(np.mean(bs_d))


def main():
    np.seterr(all="ignore")
    print("=== H_1178 — is there a CRITICAL CAPACITY for derivative-tick gating? "
          "(inverted-U of d(deriv,metro) over cell-count) ===", flush=True)
    print(f"  ladder K={LADDER}; metric = stage-decode d(DERIVATIVE,METRONOME) paired over "
          f"{len(H.SEEDS)} seeds; AUDIO stream (K={H.N_REGIMES_AUDIO} regimes); reuses H_1163 VERBATIM\n",
          flush=True)

    curve = {}
    for cap in LADDER:
        d, md, mm, bs = d_deriv_vs_metro_at_cap(H.make_audio_stream, H.N_REGIMES_AUDIO, cap)
        curve[cap] = {"d_deriv_vs_metro": d, "decode_deriv": md, "decode_metro": mm, "birth_stages_deriv": bs}
        print(f"  K={cap:3d}  d(deriv,metro)={d:+.3f}  decode_deriv={md:.3f} metro={mm:.3f}  "
              f"birth_stages_deriv={bs:.1f}", flush=True)

    caps = LADDER
    ds = [curve[c]["d_deriv_vs_metro"] for c in caps]
    kstar_i = int(np.argmax(ds))
    kstar = caps[kstar_i]
    d_peak = ds[kstar_i]
    d_end = max(ds[0], ds[-1])

    # F1 interior peak (not at either endpoint)
    f1 = 0 < kstar_i < len(caps) - 1
    # F2 inverted-U clears the decode bar
    f2 = (d_peak - d_end >= 0.8) and (d_peak >= 0.8)
    # F3 unimodal: rises to K* then falls, allow 1 reversal each side for noise
    def reversals(seq):
        return sum(1 for a, b in zip(seq, seq[1:]) if b < a)
    rise = ds[:kstar_i + 1]
    fall = ds[kstar_i:]
    f3 = (reversals(rise) <= 1) and (reversals([-x for x in fall]) <= 1)

    supported = bool(f1 and f2 and f3)
    verdict = {
        "H": "H_1178",
        "title": "is there a CRITICAL CAPACITY K* where derivative-tick gating is maximally "
                 "beneficial — an inverted-U of d(deriv,metro) over cell-count, echoing the "
                 "critical-coupling peaks of faithful-Phi (H_1158) and super-additivity (H_1167)?",
        "ladder": LADDER,
        "curve_d_deriv_vs_metro": {str(c): curve[c]["d_deriv_vs_metro"] for c in caps},
        "curve_full": {str(c): curve[c] for c in caps},
        "K_star": kstar,
        "d_at_peak": d_peak,
        "d_at_endpoints": {"K6": ds[0], "K96": ds[-1]},
        "F1_interior_peak": {"K_star": kstar, "is_interior": bool(f1)},
        "F2_inverted_U": {"d_peak_minus_endpoint": d_peak - d_end, "d_peak": d_peak,
                          "bar_gap": 0.8, "bar_peak": 0.8, "pass": bool(f2)},
        "F3_unimodal": {"reversals_rise": reversals(rise), "reversals_fall": reversals([-x for x in fall]),
                        "pass": bool(f3)},
        "supported": supported,
        "ruling": (
            f"SUPPORTED (CRITICAL-CAPACITY): the derivative-tick decode advantage is an INVERTED-U "
            f"over cell-count peaking at a CRITICAL CAPACITY K*={kstar} (d_peak={d_peak:+.2f} vs "
            f"endpoints {ds[0]:+.2f}/{ds[-1]:+.2f}). Event-driven structure-growth helps most at an "
            f"intermediate capacity: too few cells (every regime can't get one) and too many (every "
            f"clock covers every regime) both wash the advantage out. CRITICALITY recurs on a THIRD "
            f"axis (capacity), alongside the critical-coupling peaks of faithful-Phi (H_1158) and "
            f"super-additivity (H_1167) — the engine has a sweet spot on coupling AND on capacity."
            if supported else
            f"CLOSED-NEGATIVE: no clean critical-capacity inverted-U at toy scale "
            f"(F1 interior-peak={f1}, F2 inverted-U={f2}, F3 unimodal={f3}; K*={kstar}, d_peak={d_peak:+.2f}, "
            f"endpoints {ds[0]:+.2f}/{ds[-1]:+.2f}). The H_1163 capacity window does not promote to a "
            f"frozen critical-capacity claim. a_paper_negative_ok."),
        "scope": "TOY ($0 CPU numpy, %d seeds). Reuses UNIVERSE/h1163_tick_decode_metric.py substrate "
                 "VERBATIM (grow_arm/stage_decode/cohen_d/make_audio_stream/SEEDS). AUDIO stream "
                 "decisive (clean regime stages). Live CORE + scale UNVERIFIED (a_scale_honest_scope). "
                 "Lane-M growth lane." % len(H.SEEDS),
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1178_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
