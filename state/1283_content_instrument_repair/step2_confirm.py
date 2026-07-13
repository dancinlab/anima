"""STEP-2 — the CONFIRMATORY run. Everything it does was frozen in PREREG_H9293.md first.

Reads nothing that was not pre-registered: seeds [4..11] (seed 3 is quarantined as exploratory,
because its signed numbers were seen), signed lens, T=65536, Phi* against each arm's own permutation
pedestal, the knob-free lambda ladder, the G5 shape/strength specificity split, and the standing
V-gates. The decision table is applied verbatim — no threshold in this file was chosen after
looking at an arm.

    primary    d = Phi*(B) - Phi*(X)          one-sided prediction d > 0 (inherited from seed 3)
    pivot      P_bar = mean Phi(PEDESTAL)     what the instrument manufactures out of nothing
    verdict    CI_low > P_bar -> detection (report the highest rung cleared)
               CI_high < P_bar -> equivalence closure
               straddle -> power-limited, and a wall may NOT be declared
"""

from __future__ import annotations

import json

import numpy as np
from scipy import stats

from faithful_phi import build_mi_matrix, faithful_phi
from instrument import NULL_KEY, null_draws, spike_in
from p0_feasibility import gen_traj_long
from substrate import (
    A_DIRECT, B_MULTI, CPERM, NBINS, N_MOD, N_SELF, R_CHORD, X_SHARED, rank_uniform,
)

SEEDS = [4, 5, 6, 7, 8, 9, 10, 11]          # seed 3 QUARANTINED (exploratory · seen)
T = 65536
K = 32
SIGNED = True
ARMS = [("A", A_DIRECT), ("B", B_MULTI), ("X", X_SHARED), ("N", N_SELF),
        ("R", R_CHORD), ("Cperm", CPERM)]
RUNGS = {"rung1_lam0.05": 0.004837, "rung2_lam0.10": 0.019418, "rung3_lam0.15": 0.043952}
V_SPIKE_TRUTH, V_SPIKE_TOL = 0.043952, 0.20
ADJ = [(0, 1), (1, 2), (2, 3), (3, 0)]
DIAG = [(0, 2), (1, 3)]


def lam_eq(delta: float) -> float:
    """Invert the estimator-native calibration: which shared correlation is worth `delta` bits."""
    if delta <= 0:
        return 0.0
    return float(np.sqrt(max(0.0, 1.0 - 2.0 ** (-delta / 1.5))))   # Phi_est = 3 * (-0.5 log2(1-l^2))


def phi_and_shape(traj: np.ndarray) -> tuple[float, float, float, float]:
    """(Phi_obs, Phi*, S_tot, s_adj) — Phi and its MI-matrix decomposition, same estimator."""
    ru = rank_uniform(traj)
    obs = faithful_phi(ru.reshape(-1), N_MOD, T, NBINS)
    mi = build_mi_matrix(ru.reshape(-1), N_MOD, T, NBINS)
    nul = null_draws(traj, K)
    s_tot = float(sum(mi[i, j] for i, j in ADJ + DIAG))
    s_adj = float(sum(mi[i, j] for i, j in ADJ) / s_tot) if s_tot > 0 else 0.0
    return obs, obs - float(nul.mean()), s_tot, s_adj


def ci90(x: np.ndarray) -> tuple[float, float, float]:
    m = float(x.mean())
    se = float(x.std(ddof=1) / np.sqrt(len(x)))
    h = float(stats.t.ppf(0.95, len(x) - 1) * se)
    return m, m - h, m + h


def main() -> int:
    per = {name: {"phi_star": [], "s_tot": [], "s_adj": []} for name, _ in ARMS}
    ped, spike15, spike0 = [], [], []

    for s in SEEDS:
        for name, mode in ARMS:
            traj = gen_traj_long(s, mode, T, SIGNED)
            _, star, s_tot, s_adj = phi_and_shape(traj)
            per[name]["phi_star"].append(star)
            per[name]["s_tot"].append(s_tot)
            per[name]["s_adj"].append(s_adj)

        a = gen_traj_long(s, A_DIRECT, T, SIGNED)
        # PEDESTAL: a null draw scored as if it were an arm — its Phi IS the pedestal (true Phi = 0)
        rng = np.random.Generator(np.random.Philox(key=NULL_KEY ^ 0xABCD))
        pd = a.copy()
        for i in range(1, N_MOD):
            pd[i] = a[i][rng.permutation(T)]
        ped.append(faithful_phi(rank_uniform(pd).reshape(-1), N_MOD, T, NBINS))
        spike15.append(phi_and_shape(spike_in(a, 0.15))[1])
        spike0.append(phi_and_shape(spike_in(a, 0.00))[1])

    p_bar = float(np.mean(ped))

    # ── standing V-gates ────────────────────────────────────────────────────
    lo, hi = V_SPIKE_TRUTH * (1 - V_SPIKE_TOL), V_SPIKE_TRUTH * (1 + V_SPIKE_TOL)
    v_spike_n = int(sum(lo <= v <= hi for v in spike15))
    v = {
        "V_PED": bool(p_bar < RUNGS["rung1_lam0.05"]),
        "V_SPIKE": bool(v_spike_n >= 7),
        "V_ZERO": bool(abs(float(np.mean(spike0))) < RUNGS["rung1_lam0.05"]),
        "V_SEED": True,
    }

    print(f"seeds {SEEDS} (seed 3 QUARANTINED) · signed lens · T={T} · K={K}")
    print(f"P̄ (pedestal pivot)      = {p_bar:.6f}   (λ_eq {lam_eq(p_bar):.3f})")
    print(f"V-PED   P̄ < rung1 0.004837 : {'PASS' if v['V_PED'] else 'FAIL'}")
    print(f"V-SPIKE Φ*(S(.15)) ∈ [{lo:.4f},{hi:.4f}] on {v_spike_n}/8 seeds "
          f"(mean {np.mean(spike15):.6f}) : {'PASS' if v['V_SPIKE'] else 'FAIL'}")
    print(f"V-ZERO  Φ*(S(0)) = {np.mean(spike0):+.6f} : {'PASS' if v['V_ZERO'] else 'FAIL'}")
    print()
    if not all(v.values()):
        print("VERDICT: ⛔ INVALID-INSTRUMENT — a standing V-gate failed; no tier is reported.")
        json.dump({"v_gates": v, "p_bar": p_bar}, open("step2_confirm.json", "w"), indent=2)
        return 0

    print(f"{'arm':>6} | {'Φ* mean':>10} {'S_tot':>9} {'s_adj':>8}")
    for name, _ in ARMS:
        d = per[name]
        print(f"{name:>6} | {np.mean(d['phi_star']):10.6f} {np.mean(d['s_tot']):9.6f} "
              f"{np.mean(d['s_adj']):8.4f}")
    print()

    star = {k: np.array(per[k]["phi_star"]) for k, _ in ARMS}
    tot = {k: np.array(per[k]["s_tot"]) for k, _ in ARMS}
    adj = {k: np.array(per[k]["s_adj"]) for k, _ in ARMS}

    d_bx = star["B"] - star["X"]
    m, cl, ch = ci90(d_bx)
    print("PRIMARY  d = Φ*(B) − Φ*(X)   (pre-registered one-sided: d > 0)")
    print(f"   mean {m:+.6f}   90% CI [{cl:+.6f}, {ch:+.6f}]   vs P̄ = {p_bar:.6f}")
    detect = cl > p_bar
    equiv = ch < p_bar
    rung = None
    for name, val in sorted(RUNGS.items(), key=lambda kv: kv[1]):
        if cl > val:
            rung = name
    print(f"   detection (CI_low > P̄): {'YES' if detect else 'no'}"
          f"   equivalence (CI_high < P̄): {'YES' if equiv else 'no'}"
          f"   highest rung cleared: {rung or '—'}   (λ_eq of mean = {lam_eq(m):.3f})")
    print()

    ms, cls_, chs = ci90(adj["B"] - adj["X"])
    mt, clt, cht = ci90(tot["B"] - tot["X"])
    shape_pass = cls_ > 0
    strength_pos = clt > 0
    print("G5-SHAPE     s_adj(B) − s_adj(X)   (disjoint relay must be edge-specific)")
    print(f"   mean {ms:+.6f}  90% CI [{cls_:+.6f}, {chs:+.6f}]  → {'PASS' if shape_pass else 'FAIL'}")
    print("G5-STRENGTH  S_tot(B) − S_tot(X)")
    print(f"   mean {mt:+.6f}  90% CI [{clt:+.6f}, {cht:+.6f}]  → "
          f"{'positive' if strength_pos else 'ns/negative'}")
    print()

    for lbl, arr, pred in (("B−N (pred >0)", star["B"] - star["N"], "+"),
                           ("B−R (pred ≤0)", star["B"] - star["R"], "-"),
                           ("B−Cperm (pred ≈0 · VOID control)", star["B"] - star["Cperm"], "0")):
        mm, c1, c2 = ci90(arr)
        print(f"SECONDARY {lbl:34s} mean {mm:+.6f}  90% CI [{c1:+.6f}, {c2:+.6f}]")
    print()

    if detect and shape_pass:
        verdict = "🟢-DIR (toy scope · " + (rung or "below rung1") + ")"
        why = "disjoint 병렬 relay 가 용량정합 shared cut 을 이기고 MI 행렬이 링-이방적 — 축 회생."
    elif detect and not shape_pass and strength_pos:
        verdict = "⏳ STRENGTH-CONFOUND"
        why = ("B 가 X 보다 통합적인 것은 실재하나 그 정체는 총 결합강도이지 disjointness 가 아니다 "
               "⇒ disjointness 주장 기각, 축은 'relay 결합강도' 로 재정의해야 한다.")
    elif detect and not shape_pass:
        verdict = "⏳ shape-power"
        why = "검출은 성립하나 형태 게이트의 검정력이 부족 — 유보."
    elif equiv:
        verdict = "🧱 GENUINE"
        why = ("보정된 계측기·1차-민감 lens 아래에서 효과가 계측기 자체-제조량(P̄) 이하로 TOST 등가 폐쇄. "
               "이 scale·lens 에서 진짜 벽.")
    else:
        verdict = "⏳ power-limited"
        why = "CI 가 P̄ 를 걸친다 — MDE 보고. 벽 선언 금지 (n=8 frozen)."
    print(f"VERDICT: {verdict}\n   {why}")

    json.dump({"seeds": SEEDS, "T": T, "K": K, "p_bar": p_bar, "v_gates": v, "rungs": RUNGS,
               "per_arm": {k: per[k] for k, _ in ARMS},
               "primary_d_BX": {"values": d_bx.tolist(), "mean": m, "ci90": [cl, ch],
                                "detect": bool(detect), "equiv": bool(equiv), "rung": rung},
               "g5_shape": {"mean": ms, "ci90": [cls_, chs], "pass": bool(shape_pass)},
               "g5_strength": {"mean": mt, "ci90": [clt, cht]},
               "verdict": verdict}, open("step2_confirm.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
