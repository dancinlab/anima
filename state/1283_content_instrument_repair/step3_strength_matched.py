"""H_9294 — the one question H_9293 left open: match the coupling STRENGTH, does B still win?

H_9293 found B beats the capacity-matched shared cut X, but its specificity gate failed in the
wrong direction: B's MI matrix is LESS edge-specific than X's, while its total coupling is higher
(S_tot 0.0685 vs 0.0585). So "B wins" could be nothing but "B couples more". This closes that.

Two pre-registered paths (PREREG_H9294.md, committed before this ran):

  path 1  X' — raise ONLY X's W_RELAY until S_tot(X') matches S_tot(B) (grid, chosen on S_tot
          alone, never on Phi). This makes the CONTROL stronger, i.e. it is tuning AGAINST the
          claim, which is why it is allowed. Touching B would not be.
  path 2  ANCOVA — regress Phi* on S_tot across all arms (no tuning at all) and compare B's and
          X's residuals. If strength explains the whole gap, the residuals coincide.

Both are reported. If they disagree, the honest answer is a SPLIT, not a pick.
"""

from __future__ import annotations

import json

import numpy as np
from scipy import stats

from faithful_phi import build_mi_matrix, faithful_phi
from instrument import NULL_KEY, null_draws, spike_in
from substrate import (
    A_DIRECT, B_MULTI, CPERM, DIM, GAIN, LEAK, NBINS, N_EDGE, N_MOD, N_SELF, R_CHORD,
    W_IN, W_NBR, W_RELAY, X_SHARED, Lcg, rank_uniform, seed_state,
)

SEEDS = [4, 5, 6, 7, 8, 9, 10, 11]
T = 65536
K = 32
RUNG1 = 0.004837
W_GRID = [0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
MATCH_TOL = 0.05
ADJ = [(0, 1), (1, 2), (2, 3), (3, 0)]
DIAG = [(0, 2), (1, 3)]
ARMS = [("A", A_DIRECT), ("B", B_MULTI), ("X", X_SHARED), ("N", N_SELF),
        ("R", R_CHORD), ("Cperm", CPERM)]


def gen(seed: int, mode: int, w_relay: float = W_RELAY) -> np.ndarray:
    """Signed-lens trajectory at T. Identical to p0_feasibility.gen_traj_long except W_RELAY is
    exposed — the ONLY knob this hypothesis is allowed to move, and only on the control arm X."""
    rng = Lcg(seed_state(seed))
    states = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.5
    chans = rng.gauss_arr(N_EDGE * DIM).reshape(N_EDGE, DIM) * 0.5
    elo, ehi = [0, 1, 2, 3], [1, 2, 3, 0]
    if mode == CPERM:
        elo, ehi = [3, 0, 1, 2], [0, 1, 2, 3]
    if mode == R_CHORD:
        elo, ehi = [0, 1, 0, 1], [2, 3, 2, 3]
    channel_arm = mode in (B_MULTI, X_SHARED, R_CHORD, CPERM)
    inc = [[e for e in range(N_EDGE) if elo[e] == i or ehi[e] == i] for i in range(N_MOD)]

    traj = np.zeros((N_MOD, T), dtype=np.float64)
    for tt in range(T):
        inp = rng.gauss_arr(N_MOD * DIM).reshape(N_MOD, DIM) * 0.8
        new = np.empty_like(states)
        for i in range(N_MOD):
            nbr = (states[(i + N_MOD - 1) % N_MOD] + states[(i + 1) % N_MOD]) / 2.0
            v = LEAK * states[i] + GAIN * (W_NBR * nbr + W_IN * inp[i])
            if mode != A_DIRECT:
                rin = chans[inc[i]].mean(axis=0) if channel_arm else chans[i]
                v = v + GAIN * (w_relay * rin)
            new[i] = v
        if channel_arm:
            cmean = chans.mean(axis=0)
            nc = np.empty_like(chans)
            for e in range(N_EDGE):
                pair = 0.5 * (states[elo[e]] + states[ehi[e]])
                drive = 0.5 * pair + 0.5 * cmean if mode == X_SHARED else pair
                nc[e] = LEAK * chans[e] + GAIN * (W_NBR * drive)
            chans = nc
        elif mode == N_SELF:
            chans = LEAK * chans + GAIN * (W_NBR * states)
        states = new
        traj[:, tt] = states[:, 0]
    return traj


def score(traj: np.ndarray) -> tuple[float, float, float]:
    """(Phi*, S_tot, s_adj)."""
    ru = rank_uniform(traj)
    obs = faithful_phi(ru.reshape(-1), N_MOD, T, NBINS)
    mi = build_mi_matrix(ru.reshape(-1), N_MOD, T, NBINS)
    star = obs - float(null_draws(traj, K).mean())
    s_tot = float(sum(mi[i, j] for i, j in ADJ + DIAG))
    return star, s_tot, float(sum(mi[i, j] for i, j in ADJ) / s_tot) if s_tot > 0 else 0.0


def ci90(x: np.ndarray) -> tuple[float, float, float]:
    m = float(x.mean())
    h = float(stats.t.ppf(0.95, len(x) - 1) * x.std(ddof=1) / np.sqrt(len(x)))
    return m, m - h, m + h


def main() -> int:
    base = {n: {"star": [], "tot": [], "adj": []} for n, _ in ARMS}
    ped, spike15, spike0 = [], [], []
    for s in SEEDS:
        for n, mode in ARMS:
            st, tt, aj = score(gen(s, mode))
            base[n]["star"].append(st); base[n]["tot"].append(tt); base[n]["adj"].append(aj)
        a = gen(s, A_DIRECT)
        rng = np.random.Generator(np.random.Philox(key=NULL_KEY ^ 0xABCD))
        pd = a.copy()
        for i in range(1, N_MOD):
            pd[i] = a[i][rng.permutation(T)]
        ped.append(faithful_phi(rank_uniform(pd).reshape(-1), N_MOD, T, NBINS))
        spike15.append(score(spike_in(a, 0.15))[0])
        spike0.append(score(spike_in(a, 0.00))[0])

    p_bar = float(np.mean(ped))
    v = {"V_PED": bool(p_bar < RUNG1),
         "V_SPIKE": bool(sum(0.0352 <= x <= 0.0527 for x in spike15) >= 7),
         "V_ZERO": bool(abs(float(np.mean(spike0))) < RUNG1), "V_SEED": True}
    print(f"seeds {SEEDS} · signed · T={T} · K={K}")
    print(f"V-gates: P̄={p_bar:.6f} " + " ".join(f"{k}={'PASS' if x else 'FAIL'}" for k, x in v.items()))
    if not all(v.values()):
        print("VERDICT: ⛔ INVALID-INSTRUMENT")
        return 0

    tot_b = float(np.mean(base["B"]["tot"]))
    print(f"\nS_tot(B) = {tot_b:.6f}   S_tot(X) = {np.mean(base['X']['tot']):.6f}  (the H_9293 mismatch)")

    # ── path 1 — grid on W_RELAY of X ONLY, chosen on S_tot alone ──────────
    print("\n── path 1: grid W_RELAY(X) → match S_tot(B)   [selection never looks at Φ] ──")
    grid = []
    for w in W_GRID:
        tots = [score(gen(s, X_SHARED, w))[1] for s in SEEDS]
        mt = float(np.mean(tots))
        grid.append({"w": w, "s_tot": mt, "gap": abs(mt - tot_b) / tot_b})
        print(f"   W_RELAY={w:.2f}  S_tot={mt:.6f}  gap={grid[-1]['gap']*100:5.2f}%")
    best = min(grid, key=lambda g: g["gap"])
    w_star = best["w"]
    matched = best["gap"] < MATCH_TOL
    print(f"   → w* = {w_star:.2f}   gap = {best['gap']*100:.2f}%   "
          f"match gate (<5%): {'PASS' if matched else 'FAIL'}")

    res = {"p_bar": p_bar, "v_gates": v, "grid": grid, "w_star": w_star,
           "match_pass": bool(matched), "S_tot_B": tot_b,
           "base": {k: base[k] for k, _ in ARMS}}

    if matched:
        xs = [score(gen(s, X_SHARED, w_star)) for s in SEEDS]
        xp_star = np.array([r[0] for r in xs])
        xp_adj = np.array([r[2] for r in xs])
        d = np.array(base["B"]["star"]) - xp_star
        m, cl, ch = ci90(d)
        print(f"\n   Φ*(X′) = {xp_star.mean():.6f}   s_adj(X′) = {xp_adj.mean():.4f}  "
              f"(B: Φ*={np.mean(base['B']['star']):.6f}  s_adj={np.mean(base['B']['adj']):.4f})")
        print(f"   d′ = Φ*(B) − Φ*(X′) = {m:+.6f}   90% CI [{cl:+.6f}, {ch:+.6f}]   vs P̄ {p_bar:.6f}")
        p1_detect, p1_equiv = cl > p_bar, ch < p_bar
        print(f"   → detection {'YES' if p1_detect else 'no'} · equivalence {'YES' if p1_equiv else 'no'}")
        res["path1"] = {"d_mean": m, "ci90": [cl, ch], "detect": bool(p1_detect),
                        "equiv": bool(p1_equiv), "xprime_phi_star": xp_star.tolist(),
                        "xprime_s_adj": xp_adj.tolist()}
    else:
        p1_detect = p1_equiv = None
        res["path1"] = None

    # ── path 2 — ANCOVA, zero tuning ───────────────────────────────────────
    print("\n── path 2: ANCOVA  Φ* ~ β0 + β1·S_tot  (all 6 arms × 8 seeds, arm label unused) ──")
    X_ = np.concatenate([base[n]["tot"] for n, _ in ARMS])
    Y_ = np.concatenate([base[n]["star"] for n, _ in ARMS])
    b1, b0 = np.polyfit(X_, Y_, 1)
    r2 = float(np.corrcoef(X_, Y_)[0, 1] ** 2)
    print(f"   fit: Φ* = {b0:+.6f} + {b1:+.4f}·S_tot     R² = {r2:.4f}")
    rb = np.array(base["B"]["star"]) - (b0 + b1 * np.array(base["B"]["tot"]))
    rx = np.array(base["X"]["star"]) - (b0 + b1 * np.array(base["X"]["tot"]))
    mr, clr, chr_ = ci90(rb - rx)
    print(f"   G-RESID = resid(B) − resid(X) = {mr:+.6f}   90% CI [{clr:+.6f}, {chr_:+.6f}]")
    p2_pos = clr > 0
    p2_zero = clr <= 0 <= chr_
    print(f"   → residual gap {'POSITIVE (disjointness leaves something)' if p2_pos else ('CONTAINS 0 (strength explains it all)' if p2_zero else 'NEGATIVE (X does better at equal strength)')}")
    res["path2"] = {"b0": float(b0), "b1": float(b1), "r2": r2, "g_resid_mean": mr,
                    "ci90": [clr, chr_], "positive": bool(p2_pos), "contains_zero": bool(p2_zero)}

    # ── decision table (verbatim from PREREG_H9294 §3) ─────────────────────
    if matched and p1_detect and p2_pos:
        verdict = "🟢-DIR (toy) — disjointness 잔차 실재"
        why = "강도를 맞춰도 B 가 이기고 ANCOVA 잔차도 양(+) ⇒ R6 의 핵심이 부분 회생."
    elif matched and p1_detect and not p2_pos:
        verdict = "⏳ SPLIT"
        why = "두 경로 불일치 — 강도 정합 방식에 의존. 양쪽 보고, tier 미확정."
    elif matched and (p1_equiv or not p1_detect) and p2_zero:
        verdict = "🧱 STRENGTH-ONLY (종결)"
        why = ("강도를 맞추면 B 의 우위가 사라지고 ANCOVA 잔차가 0 을 포함한다 ⇒ B 의 이점은 전적으로 "
               "총 결합강도이며 disjointness 의 기여는 0. content-relay 축의 disjointness 레버 CLOSED.")
    elif matched and p1_equiv and not p2_zero and not p2_pos:
        verdict = "🧱 STRENGTH-ONLY, 강함"
        why = "강도 정합 후 X′ 가 오히려 B 를 이긴다 — 공유버스가 더 통합적."
    else:
        verdict = "⏳ power-limited / MATCH-FAIL"
        why = "정합 게이트 미충족이거나 CI 가 결정적이지 않다 — 벽 선언 금지."
    print(f"\nVERDICT: {verdict}\n   {why}")
    res["verdict"] = verdict
    json.dump(res, open("step3_strength_matched.json", "w"), indent=2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
