"""
H_1182 — does the CRITICAL CAPACITY K* scale linearly with stream complexity?
(Lane 2 / MAIN hands-on discovery rung, MITOSIS-ENGINE domain)

H_1178 (🟢) found an interior critical capacity K*=32 for derivative-tick gating on
a 6-regime AUDIO stream, and — as a NON-pre-registered close-watch SERENDIP — that
K*/n_regimes ≈ 32/6 ≈ 5.3 "cells per regime", tying to H_1159b (capacity self-tunes
to #clusters). H_1182 PROMOTES that serendip to a FROZEN-FALSIFIER claim: is the
"~5.3 cells/regime" a real SCALING LAW (K* ∝ n_regimes, constant cells/regime), or a
coincidence of the single 6-regime config?

If K* scales linearly with stream complexity at a roughly CONSTANT cells/regime, then
the critical capacity is not a magic number but a LAW — the engine needs a fixed
budget of cells per distinguishable regime to make event-driven (derivative) growth
maximally beneficial. That is the kind of cross-config invariant a close-watched rung
is meant to pin down (the H_1178 discovery hook, carried one step further).

FROZEN FALSIFIER (pre-registered BEFORE measuring; deterministic, the H_1163 seeds;
metric = K* = argmax_K d(DERIVATIVE,METRONOME) on stage-decode, per regime-count):
  regime ladder N = {3, 4, 6, 8, 10}   (stream complexity = #recurring AUDIO regimes)
  capacity ladder K = {4,6,8,12,16,24,32,48,64,96}  (brackets K* for all N: 10*~5 ~ 50 < 96)
  for each N: monkeypatch the H_1163 substrate to N regimes, sweep K, K*(N)=argmax_K d.
  F1 MONOTONE     : Spearman(N, K*) >= 0.8 — critical capacity RISES with complexity.
  F2 CONST-RATIO  : the per-regime budget r(N)=K*/N is ~constant — CoV(r) <= 0.35 AND
                    mean r in [2, 10] (a sane, finite cells-per-regime budget).
  SUPPORTED (SCALING-LAW) iff F1 AND F2 -> K* ∝ N at a constant cells/regime; the
  H_1178 "~5.3 cells/regime" is a real law, not a 6-regime coincidence.
  Otherwise CLOSED-NEGATIVE (a_paper_negative_ok): K* does not scale cleanly / the
  ratio is not constant -> the 5.3 was config-specific.

toy ($0 CPU numpy, deterministic). Reuses UNIVERSE/h1163_tick_decode_metric.py +
h1178 sweep pattern VERBATIM (grow_arm / stage_decode_accuracy / cohen_d_paired /
make_audio_stream / SEEDS), only the global N_REGIMES_AUDIO is swept. Live CORE +
scale UNVERIFIED (a_scale_honest_scope). Lane-M growth lane.
"""
import json
import numpy as np
import h1163_tick_decode_metric as H

REGIME_LADDER = [3, 4, 6, 8, 10]
CAP_LADDER = [4, 6, 8, 12, 16, 24, 32, 48, 64, 96]


def spearman(x, y):
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    rx -= rx.mean(); ry -= ry.mean()
    denom = np.sqrt((rx * rx).sum() * (ry * ry).sum())
    return float((rx * ry).sum() / denom) if denom > 0 else 0.0


def d_at_cap(n_regimes, cap):
    """Paired Cohen's d(DERIVATIVE,METRONOME) on stage-decode at (n_regimes, MAX_CELLS=cap).
    Reuses H_1163 grow_arm/stage_decode/cohen_d VERBATIM; only globals are patched."""
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


def main():
    np.seterr(all="ignore")
    print("=== H_1182 — does the critical capacity K* scale linearly with stream complexity "
          "(constant cells/regime)? ===", flush=True)
    print(f"  regime ladder N={REGIME_LADDER}; capacity ladder K={CAP_LADDER}; "
          f"metric K*=argmax_K d(DERIVATIVE,METRONOME) on stage-decode; {len(H.SEEDS)} seeds; "
          f"reuses H_1163+h1178 VERBATIM\n", flush=True)

    kstar = {}
    curves = {}
    for n in REGIME_LADDER:
        ds = [d_at_cap(n, c) for c in CAP_LADDER]
        i = int(np.argmax(ds))
        kstar[n] = CAP_LADDER[i]
        curves[n] = {str(c): d for c, d in zip(CAP_LADDER, ds)}
        ratio = CAP_LADDER[i] / n
        print(f"  N={n:2d}  K*={CAP_LADDER[i]:3d}  d_peak={ds[i]:+.3f}  cells/regime={ratio:.2f}  "
              f"| d-curve {[f'{d:+.2f}' for d in ds]}", flush=True)

    Ns = np.array(REGIME_LADDER, float)
    Ks = np.array([kstar[n] for n in REGIME_LADDER], float)
    ratios = Ks / Ns
    rho = spearman(Ns, Ks)
    cov = float(ratios.std() / ratios.mean()) if ratios.mean() > 0 else 9.9
    mean_r = float(ratios.mean())

    f1 = rho >= 0.8
    f2 = (cov <= 0.35) and (2.0 <= mean_r <= 10.0)
    supported = bool(f1 and f2)

    verdict = {
        "H": "H_1182",
        "title": "does the critical capacity K* scale ~linearly with stream complexity (#regimes) at a "
                 "constant cells/regime — promoting the H_1178 serendip '~5.3 cells/regime' to a scaling law?",
        "regime_ladder": REGIME_LADDER,
        "cap_ladder": CAP_LADDER,
        "K_star_by_regime": {str(n): kstar[n] for n in REGIME_LADDER},
        "cells_per_regime": {str(n): float(kstar[n] / n) for n in REGIME_LADDER},
        "d_curves": curves,
        "F1_monotone": {"spearman_N_Kstar": rho, "bar": 0.8, "pass": bool(f1)},
        "F2_const_ratio": {"mean_cells_per_regime": mean_r, "CoV": cov, "cov_bar": 0.35,
                           "mean_range": [2.0, 10.0], "pass": bool(f2)},
        "supported": supported,
        "ruling": (
            f"SUPPORTED (SCALING-LAW): the critical capacity scales with stream complexity at a roughly "
            f"constant cells/regime (Spearman(N,K*)={rho:+.2f}, mean cells/regime={mean_r:.2f}, "
            f"CoV={cov:.2f}). The H_1178 '~5.3 cells/regime' is a real cross-config law, not a 6-regime "
            f"coincidence — event-driven growth needs a fixed cell budget per distinguishable regime to be "
            f"maximally beneficial. Strengthens the H_1178 critical-capacity finding + ties to H_1159b "
            f"(capacity self-tunes to #clusters)."
            if supported else
            f"CLOSED-NEGATIVE: K* does not scale cleanly with complexity at a constant ratio "
            f"(F1 monotone={f1} Spearman={rho:+.2f}; F2 const-ratio={f2} mean={mean_r:.2f} CoV={cov:.2f}). "
            f"The H_1178 '~5.3 cells/regime' is config-specific, not a scaling law. a_paper_negative_ok."),
        "scope": "TOY ($0 CPU numpy, %d seeds). Reuses UNIVERSE/h1163_tick_decode_metric.py + h1178 sweep "
                 "VERBATIM; only the global N_REGIMES_AUDIO is swept. K* is argmax on a coarse capacity "
                 "ladder (quantized). Live CORE + scale UNVERIFIED (a_scale_honest_scope)." % len(H.SEEDS),
    }
    print("\n=== VERDICT ===", flush=True)
    print(json.dumps(verdict, ensure_ascii=False, indent=2), flush=True)
    json.dump(verdict, open("/tmp/h1182_result.json", "w"), ensure_ascii=False, indent=2)
    print("\n[done]", flush=True)


if __name__ == "__main__":
    main()
