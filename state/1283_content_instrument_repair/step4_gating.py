"""H_9295 — does GATED (nonlinear) coupling open a structural channel into Φ?

Everything below was frozen in PREREG_H9295.md and committed before this ran (42ffb9548).

The headline is NOT "does Φ go up" — any change to coupling moves S_tot, so a higher Φ says
nothing. The claim is that structure contributes INDEPENDENTLY of total coupling, so the headline
is the residual, measured two ways that must agree:

  (i)  strength-matched pair contrast — raise ONLY X's W_RELAY until S_tot(X′) = S_tot(B) on the
       GATED substrate, then read Φ*(B) − Φ*(X′). Tuning the control UP is tuning against the
       claim, which is why it is allowed.
  (ii) partial-R²(arm | ns(S_tot, df=4)) over all arms — how much residual variance the arm label
       explains once total coupling is regressed out with a SPLINE. The spline (not a line) is the
       defence against the design's own most likely failure: if gating bends Φ* = f(S_tot) and the
       arms occupy different S_tot bands, a linear control would let the curvature leak into `arm`
       and manufacture a false positive. Significance is judged against a LABEL-PERMUTATION null,
       which never looks at which arm is which.

A null result is only interpretable if the gate is actually live, and the originally pre-registered
liveness control (P+/P−) did not survive its own validity gate: V-LINEAR rejected all three
constructions of it (+0.198 → −0.140 → +0.021 on the LINEAR substrate, where a valid P± pair must
read 0). See PREREG_H9295 §A1 — the failures are recorded, not hidden, and the bar was never
loosened to rescue them.

Liveness therefore comes from L-SHIFT (amendment 1, frozen before this file's headline ever ran):
re-apply the gate this arm actually used, circularly shifted by a large per-edge lag. The gate's
marginal AND its whole autocorrelation are preserved — it is literally the same series — while its
alignment with c_e(t) is destroyed. A gate that is only a fluctuating multiplicative gain is
untouched by that; a gate that is genuinely conditional on the coincidence it detects is not.
(A β=0 ablation cannot do this job: β=0 collapses the gate to the constant 0.5, a half-gain LINEAR
relay, removing conditionality and gain fluctuation at once.)
"""

from __future__ import annotations

import json

import numpy as np
from scipy import stats

from faithful_phi import build_mi_matrix, faithful_phi
from gated import _calibrate_mode_amps, calibrate_beta, gen, l_shift_pair
from instrument import NULL_KEY, null_draws, spike_in
from substrate import (
    A_DIRECT, B_MULTI, CPERM, NBINS, N_MOD, N_SELF, R_CHORD, X_SHARED, rank_uniform,
)

SEEDS = [4, 5, 6, 7, 8, 9, 10, 11]          # seed 3 quarantined (exploratory · seen)
T = 65536
K = 32
RUNG1 = 0.004837
SPIKE_TRUTH = 0.043952
EFFECT_FLOOR = 0.0088                        # 20% of the spike-in scale (pre-registered)
W_GRID = [0.50, 0.60, 0.70, 0.80, 0.90, 1.00, 1.10, 1.20, 1.30, 1.40, 1.50]
MATCH_TOL = 0.05
N_PERM = 2000
ADJ = [(0, 1), (1, 2), (2, 3), (3, 0)]
DIAG = [(0, 2), (1, 3)]
ARMS = [("A", A_DIRECT), ("B", B_MULTI), ("X", X_SHARED), ("N", N_SELF),
        ("R", R_CHORD), ("Cperm", CPERM)]


def score(traj: np.ndarray) -> tuple[float, float]:
    """(Φ*, S_tot) — pedestal-subtracted Φ and the total pairwise MI, same estimator throughout."""
    ru = rank_uniform(traj)
    obs = faithful_phi(ru.reshape(-1), N_MOD, T, NBINS)
    mi = build_mi_matrix(ru.reshape(-1), N_MOD, T, NBINS)
    star = obs - float(null_draws(traj, K).mean())
    return star, float(sum(mi[i, j] for i, j in ADJ + DIAG))


def ci90(x: np.ndarray) -> tuple[float, float, float]:
    m = float(x.mean())
    h = float(stats.t.ppf(0.95, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x)))
    return m, m - h, m + h


def ns_basis(x: np.ndarray, df: int = 4) -> np.ndarray:
    """Natural cubic spline basis on S_tot (truncated-power, natural end conditions)."""
    kn = np.quantile(x, np.linspace(0, 1, df + 1)[1:-1])
    lo, hi = float(x.min()), float(x.max())
    def d(k):
        return (np.maximum(x - k, 0) ** 3 - np.maximum(x - hi, 0) ** 3) / (hi - k)
    cols = [np.ones_like(x), x] + [d(k) - d(kn[-1]) for k in kn[:-1]]
    return np.column_stack(cols)


def partial_r2(y: np.ndarray, s: np.ndarray, labels: np.ndarray, df: int = 4) -> float:
    """(RSS_reduced − RSS_full) / RSS_reduced for  y ~ ns(s) [+ arm]."""
    base = ns_basis(s, df)
    rss_r = float(np.linalg.lstsq(base, y, rcond=None)[1][0]) if base.shape[0] > base.shape[1] else 0.0
    uniq = sorted(set(labels.tolist()))
    dummies = np.column_stack([(labels == u).astype(float) for u in uniq[1:]])
    full = np.column_stack([base, dummies])
    res = np.linalg.lstsq(full, y, rcond=None)[1]
    rss_f = float(res[0]) if len(res) else float(((y - full @ np.linalg.lstsq(full, y, rcond=None)[0]) ** 2).sum())
    return (rss_r - rss_f) / rss_r if rss_r > 0 else 0.0


def main() -> int:
    out: dict = {"T": T, "K": K, "seeds": SEEDS}

    # ── β pinned on arm A ALONE, before any contrast is looked at ──────────
    beta, mu, sd = calibrate_beta(SEEDS, 4096)
    _calibrate_mode_amps(SEEDS)
    out["beta"] = beta
    print(f"β pinned on arm A alone: β = {beta:.4f}   (operating point σ(0)=0.5, ±1σ → [0.27,0.73])")
    print(f"seeds {SEEDS} · signed lens · T={T} · K={K}\n")

    # ── liveness stack (PREREG amend-1): L-SHIFT primary + RECEIPT standing ─────
    # P± was retired: V-LINEAR rejected all three constructions (see the card). L-SHIFT replaces
    # it — the gate is re-applied circularly shifted, preserving its marginal AND autocorrelation
    # while destroying only its alignment with c_e. A gate that is a mere fluctuating gain is
    # untouched; a genuinely conditional one is not.
    per = {n: {"star": [], "tot": []} for n, _ in ARMS}
    ped, sp15, sp0, lshift = [], [], [], []
    for s in SEEDS:
        for n, mode in ARMS:
            st, tot = score(gen(s, mode, T, gated=True, beta=beta, mu=mu, sd=sd))
            per[n]["star"].append(st)
            per[n]["tot"].append(tot)
        g_tr, sur_tr = l_shift_pair(s, B_MULTI, T, beta, mu, sd)
        lshift.append(score(g_tr)[0] - score(sur_tr)[0])
        a = gen(s, A_DIRECT, T, gated=True, beta=beta, mu=mu, sd=sd)
        rng = np.random.Generator(np.random.Philox(key=NULL_KEY ^ 0xABCD))
        pd = a.copy()
        for i in range(1, N_MOD):
            pd[i] = a[i][rng.permutation(T)]
        ped.append(faithful_phi(rank_uniform(pd).reshape(-1), N_MOD, T, NBINS))
        sp15.append(score(spike_in(a, 0.15))[0])
        sp0.append(score(spike_in(a, 0.00))[0])

    p_bar = float(np.mean(ped))
    m_ls, cl_ls, ch_ls = ci90(np.array(lshift))
    v = {
        "V_ZERO": bool(abs(float(np.mean(sp0))) < RUNG1),
        "V_SPIKE": bool(sum(0.0352 <= x <= 0.0527 for x in sp15) >= 7),
        "L_SHIFT": bool(cl_ls > 0 or ch_ls < 0),
        "V_SEED": True,
    }
    print(f"P̄ (pedestal) = {p_bar:.6f}")
    print(f"V-ZERO   Φ*(S(0)) = {np.mean(sp0):+.6f}  → {'PASS' if v['V_ZERO'] else 'FAIL'}")
    print(f"V-SPIKE  Φ*(S(.15)) = {np.mean(sp15):.6f}  → {'PASS' if v['V_SPIKE'] else 'FAIL'}")
    print(f"L-SHIFT  Φ*(gated) − Φ*(shifted) = {m_ls:+.6f} 90% CI [{cl_ls:+.6f}, {ch_ls:+.6f}]")
    print(f"         (CI excludes 0 ⇒ the gate is CONDITIONAL, not a gain)"
          f"  → {'PASS' if v['L_SHIFT'] else 'FAIL'}\n")

    out.update({"p_bar": p_bar, "v_gates": v, "l_shift": [m_ls, cl_ls, ch_ls],
                "per_arm": {k: per[k] for k, _ in ARMS}})
    if not all(v.values()):
        print("VERDICT: ⏳ INVALID — a standing gate failed; no tier is reported.")
        json.dump(out, open("step4_gating.json", "w"), indent=2)
        return 0

    print(f"{'arm':>6} | {'Φ* mean':>10} {'S_tot':>10}")
    for n, _ in ARMS:
        print(f"{n:>6} | {np.mean(per[n]['star']):10.6f} {np.mean(per[n]['tot']):10.6f}")
    print()

    # ── headline (i): strength-matched pair contrast on the GATED substrate ──
    tot_b = float(np.mean(per["B"]["tot"]))
    grid = []
    for w in W_GRID:
        mt = float(np.mean([score(gen(s, X_SHARED, T, gated=True, beta=beta, mu=mu, sd=sd,
                                      w_relay=w))[1] for s in SEEDS]))
        grid.append({"w": w, "s_tot": mt, "gap": abs(mt - tot_b) / tot_b})
    best = min(grid, key=lambda g: g["gap"])
    matched = best["gap"] < MATCH_TOL
    print(f"(i) strength-match X→B on the gated substrate: S_tot(B) = {tot_b:.6f}")
    for g in grid:
        print(f"    W_RELAY={g['w']:.2f}  S_tot={g['s_tot']:.6f}  gap={g['gap']*100:5.2f}%")
    print(f"    → w* = {best['w']:.2f}  gap {best['gap']*100:.2f}%  "
          f"match gate: {'PASS' if matched else 'FAIL'}")
    out["grid"] = grid
    out["w_star"] = best["w"]
    out["match_pass"] = bool(matched)

    detect_i = False
    if matched:
        xp = np.array([score(gen(s, X_SHARED, T, gated=True, beta=beta, mu=mu, sd=sd,
                                 w_relay=best["w"]))[0] for s in SEEDS])
        d = np.array(per["B"]["star"]) - xp
        m, cl, ch = ci90(d)
        detect_i = bool(cl > 0 and m >= EFFECT_FLOOR)
        print(f"    d′ = Φ*(B) − Φ*(X′) = {m:+.6f}  90% CI [{cl:+.6f}, {ch:+.6f}]  "
              f"(floor {EFFECT_FLOOR}) → {'DETECT' if detect_i else 'no detection'}")
        out["headline_i"] = {"mean": m, "ci90": [cl, ch], "detect": detect_i}
    print()

    # ── headline (ii): partial-R²(arm | ns(S_tot)) vs a LABEL-PERMUTATION null ──
    names = [n for n, _ in ARMS]
    y = np.concatenate([per[n]["star"] for n in names])
    s_tot = np.concatenate([per[n]["tot"] for n in names])
    lab = np.concatenate([[n] * len(SEEDS) for n in names])
    obs_pr2 = partial_r2(y, s_tot, lab)
    rng = np.random.default_rng(20260714)
    null = np.array([partial_r2(y, s_tot, rng.permutation(lab)) for _ in range(N_PERM)])
    p99 = float(np.quantile(null, 0.99))
    pval = float((null >= obs_pr2).mean())
    detect_ii = bool(obs_pr2 > p99)
    print(f"(ii) partial-R²(arm | ns(S_tot, df=4)) = {obs_pr2:.4f}")
    print(f"     label-permutation null: 99th pct = {p99:.4f} · p = {pval:.4f} "
          f"→ {'SIGNIFICANT' if detect_ii else 'not significant'}")
    sens = {str(df): partial_r2(y, s_tot, lab, df) for df in (3, 4, 5)}
    print(f"     df sensitivity {sens}")
    out["headline_ii"] = {"partial_r2": obs_pr2, "null_p99": p99, "p": pval,
                          "significant": detect_ii, "df_sensitivity": sens}
    print()

    if detect_i and detect_ii:
        verdict = "🟢-DIR (toy) — 게이팅이 구조 채널을 연다"
        why = "비선형 coincidence 게이팅 하에서 disjointness 가 S_tot 와 독립으로 Φ 에 기여한다."
    elif not detect_i and not detect_ii:
        verdict = "🧱 GATING-NO-CHANNEL (더 깊은 폐쇄)"
        why = ("게이트는 증명상 live 한데(P+/P− 분리) disjointness 대비는 여전히 S_tot 로 전부 "
               "설명된다 ⇒ 게이팅도 레버가 아니다. 이중분리로 확정.")
    else:
        verdict = "⏳ SPLIT — 두 headline 불일치"
        why = "강도정합 대비와 partial-R² 가 갈린다 — 정직하게 양쪽 보고, tier 미확정."
    print(f"VERDICT: {verdict}\n   {why}")
    out["verdict"] = verdict
    json.dump(out, open("step4_gating.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
