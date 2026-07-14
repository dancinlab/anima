#!/usr/bin/env python3
"""H_9312 - sigma 3-way split: PRESENCE (state->self) vs INFO (self->emit).

Reads the --opgrip-dump tape (#OGD jsonl lines) and scores BOTH directions
against a 200-shift circular null (autocorrelation-preserving), a phase-random
surrogate, a zero-truth AR(1) PEDESTAL and a known-truth POS spike-in.

Frozen by PREREG.md BEFORE the data was inspected. No bar is recomputed here.
"""
import json
import sys
import numpy as np

RNG = np.random.default_rng(20260714)

CALIB = 50          # ticks 0-49 = g_self calibration -> excluded (prereg)
N_SHIFT = 200       # circular-shift null draws
MIN_SHIFT = 50      # |shift| floor
RIDGE_A = 1.0
POS_P = 0.35        # POS spike-in flip prob -> true D-acc = 0.65
POS_TRUTH = 0.65
EQ_ACC = 0.05       # TOST equivalence margin (acc)
EQ_NATS = 0.02      # TOST equivalence margin (nats)
BAR_R2 = 0.02
BAR_NATS = 0.01

LANES = ["rel_lane", "af_val", "allo_ctx", "coh_lane", "bal_lane",
         "nov_ctx", "gap_ctx", "ag_conflict"]


def load(path):
    rows = []
    with open(path) as f:
        for ln in f:
            if ln.startswith("#OGD "):
                rows.append(json.loads(ln[5:]))
    rows.sort(key=lambda r: r["tick"])
    return rows


def zs(X):
    m = X.mean(0)
    s = X.std(0)
    s = np.where(s < 1e-12, 1.0, s)
    return (X - m) / s


def ridge_fit(X, y, a=RIDGE_A):
    X1 = np.hstack([X, np.ones((len(X), 1))])
    A = X1.T @ X1 + a * np.eye(X1.shape[1])
    A[-1, -1] -= a           # do not penalize the intercept
    return np.linalg.solve(A, X1.T @ y)


def ridge_pred(w, X):
    return np.hstack([X, np.ones((len(X), 1))]) @ w


def r2(y, yh):
    ss = ((y - y.mean()) ** 2).sum()
    if ss < 1e-12:
        return float("nan")
    return 1.0 - ((y - yh) ** 2).sum() / ss


def logistic_fit(X, y, a=1.0, iters=200):
    """L2-regularized logistic regression (Newton/IRLS, numerically guarded)."""
    X1 = np.hstack([X, np.ones((len(X), 1))])
    w = np.zeros(X1.shape[1])
    I = a * np.eye(X1.shape[1])
    I[-1, -1] = 0.0
    for _ in range(iters):
        z = np.clip(X1 @ w, -30, 30)
        p = 1.0 / (1.0 + np.exp(-z))
        W = np.clip(p * (1 - p), 1e-6, None)
        g = X1.T @ (p - y) + I @ w
        H = (X1 * W[:, None]).T @ X1 + I + 1e-8 * np.eye(X1.shape[1])
        step = np.linalg.solve(H, g)
        w = w - step
        if np.max(np.abs(step)) < 1e-8:
            break
    return w


def logistic_p(w, X):
    z = np.clip(np.hstack([X, np.ones((len(X), 1))]) @ w, -30, 30)
    return 1.0 / (1.0 + np.exp(-z))


def score_info(feats, y, cut):
    """held-out D-acc + EARNED nats (vs base-rate constant predictor)."""
    Xtr, Xte = feats[:cut], feats[cut:]
    ytr, yte = y[:cut], y[cut:]
    if ytr.min() == ytr.max():
        return float("nan"), float("nan")
    w = logistic_fit(zs_with(Xtr, Xtr), ytr)
    p = np.clip(logistic_p(w, zs_with(Xte, Xtr)), 1e-6, 1 - 1e-6)
    acc = float(((p >= 0.5).astype(int) == yte).mean())
    base = float(np.clip(ytr.mean(), 1e-6, 1 - 1e-6))
    ll_m = float(-(yte * np.log(p) + (1 - yte) * np.log(1 - p)).mean())
    ll_b = float(-(yte * np.log(base) + (1 - yte) * np.log(1 - base)).mean())
    return acc, ll_b - ll_m          # EARNED nats (positive = better than base rate)


def zs_with(X, ref):
    m = ref.mean(0)
    s = ref.std(0)
    s = np.where(s < 1e-12, 1.0, s)
    return (X - m) / s


def score_presence(lanes, self_v, cut):
    Xtr, Xte = lanes[:cut], lanes[cut:]
    ytr, yte = self_v[:cut], self_v[cut:]
    if ytr.std() < 1e-12 or yte.std() < 1e-12:
        return float("nan")
    w = ridge_fit(zs_with(Xtr, Xtr), ytr)
    return float(r2(yte, ridge_pred(w, zs_with(Xte, Xtr))))


def circ_shifts(n):
    out = []
    while len(out) < N_SHIFT:
        s = int(RNG.integers(MIN_SHIFT, n - MIN_SHIFT))
        out.append(s)
    return out


def phase_rand(x):
    n = len(x)
    F = np.fft.rfft(x - x.mean())
    ph = RNG.uniform(0, 2 * np.pi, len(F))
    ph[0] = 0.0
    if n % 2 == 0:
        ph[-1] = 0.0
    return np.fft.irfft(np.abs(F) * np.exp(1j * ph), n) + x.mean()


def ar1_pedestal(x):
    """zero-truth surrogate: AR(1) matched to x's lag-1 autocorr + sd, independent RNG."""
    n = len(x)
    xc = x - x.mean()
    denom = (xc[:-1] ** 2).sum()
    phi = float((xc[1:] * xc[:-1]).sum() / denom) if denom > 1e-12 else 0.0
    phi = float(np.clip(phi, -0.999, 0.999))
    sd = float(x.std())
    e = RNG.normal(0, sd * np.sqrt(max(1 - phi ** 2, 1e-6)), n)
    z = np.zeros(n)
    for i in range(1, n):
        z[i] = phi * z[i - 1] + e[i]
    return z + x.mean()


def selffeat(self_ctx, self_ema, self_phasic):
    cols = [self_ctx, self_ema, self_phasic]
    for L in range(1, 9):
        cols.append(np.concatenate([np.full(L, self_ctx[0]), self_ctx[:-L]]))
    return np.column_stack(cols)


def main(path):
    rows = load(path)
    rows = [r for r in rows if r["tick"] >= CALIB]
    n = len(rows)
    out = {"n_scored": n, "prereg": "PREREG.md"}
    if n < 400:
        out["verdict"] = "INFRA-BLOCKED"
        out["reason"] = f"tape too short (n={n})"
        print(json.dumps(out, indent=2))
        return

    g = lambda k: np.array([float(r[k]) for r in rows])
    self_ctx = g("self_ctx_live")
    self_ema = g("self_ema")
    self_ph = g("self_phasic")
    e_live = np.array([int(r["e_live"]) for r in rows])
    lanes = np.column_stack([g(k) for k in LANES])
    margin_motiv = g("motiv") - g("thr")          # continuous pre-emit drive margin
    margin_rate = g("idle") - 30.0                # continuous rate-gate margin
    state = np.hstack([lanes, margin_motiv[:, None], margin_rate[:, None]])

    # ── degeneracy gate (prereg, BEFORE any verdict) ─────────────────────────
    out["sd_self_ctx"] = float(self_ctx.std())
    out["emit_rate"] = float(e_live.mean())
    out["emit_minority_n"] = int(min(e_live.sum(), n - e_live.sum()))
    out["sd_margin_motiv"] = float(margin_motiv.std())
    out["sd_margin_rate"] = float(margin_rate.std())
    out["lane_sds"] = {k: float(lanes[:, i].std()) for i, k in enumerate(LANES)}
    degen = []
    if self_ctx.std() < 1e-6:
        degen.append("self_ctx_live is CONSTANT (sd<1e-6)")
    if out["emit_minority_n"] < 30:
        degen.append(f"e_live minority class n={out['emit_minority_n']} < 30")
    out["degeneracy"] = degen

    cut = n // 2
    out["n_fit"], out["n_test"] = cut, n - cut
    out["mde_acc_2sigma"] = float(2 * 0.5 / np.sqrt(n - cut))

    # ── PRESENCE (state -> self) ─────────────────────────────────────────────
    pres = {}
    if self_ctx.std() >= 1e-6:
        pres["exp_r2"] = score_presence(state, self_ctx, cut)
        null = [score_presence(state, np.roll(self_ctx, s), cut) for s in circ_shifts(n)]
        null = np.array([v for v in null if np.isfinite(v)])
        pres["circ_null_med"] = float(np.median(null))
        pres["circ_null_p95"] = float(np.percentile(null, 95))
        pres["circ_null_p99"] = float(np.percentile(null, 99))
        pres["circ_p_emp"] = float((null >= pres["exp_r2"]).mean())
        pres["phase_null_p95"] = float(np.percentile(
            [score_presence(state, phase_rand(self_ctx), cut) for _ in range(N_SHIFT)], 95))
        pres["pedestal_r2"] = score_presence(state, ar1_pedestal(self_ctx), cut)
        # POS: a self stream that IS a known linear image of the state (truth R2 ~= 1 minus noise)
        beta = RNG.normal(0, 1, state.shape[1])
        sig = zs(state) @ beta
        noise = RNG.normal(0, sig.std(), n)
        pos_self = 0.7 * sig + 0.7 * noise            # truth R2 = .49/(.49+.49) = 0.50
        pres["pos_truth_r2"] = 0.5
        pres["pos_meas_r2"] = score_presence(state, pos_self, cut)
        pres["pos_ratio"] = (pres["pos_meas_r2"] / 0.5) if pres["pos_meas_r2"] == pres["pos_meas_r2"] else float("nan")
        pres["PASS"] = bool(pres["exp_r2"] - pres["circ_null_p95"] >= BAR_R2
                            and pres["pedestal_r2"] <= pres["circ_null_p95"])
    else:
        pres["PASS"] = None
        pres["note"] = "self_ctx_live constant -> PRESENCE undefined"
    out["PRESENCE"] = pres

    # ── INFO (self -> next-tick emit) ────────────────────────────────────────
    info = {}
    y = e_live[1:]                       # next tick
    F = selffeat(self_ctx, self_ema, self_ph)[:-1]
    m = len(y)
    cut2 = m // 2
    if out["emit_minority_n"] >= 30 and self_ctx.std() >= 1e-6:
        a, nats = score_info(F, y, cut2)
        info["exp_dacc"], info["exp_nats"] = a, nats
        info["base_rate_test"] = float(max(y[cut2:].mean(), 1 - y[cut2:].mean()))
        nl = []
        for s in circ_shifts(n):
            Fs = selffeat(np.roll(self_ctx, s), np.roll(self_ema, s), np.roll(self_ph, s))[:-1]
            nl.append(score_info(Fs, y, cut2))
        na = np.array([v[0] for v in nl if np.isfinite(v[0])])
        nn = np.array([v[1] for v in nl if np.isfinite(v[1])])
        info["circ_null_dacc_med"] = float(np.median(na))
        info["circ_null_dacc_p99"] = float(np.percentile(na, 99))
        info["circ_null_nats_med"] = float(np.median(nn))
        info["circ_null_nats_p99"] = float(np.percentile(nn, 99))
        info["circ_p_emp_dacc"] = float((na >= info["exp_dacc"]).mean())
        pr = [score_info(selffeat(phase_rand(self_ctx), phase_rand(self_ema),
                                  phase_rand(self_ph))[:-1], y, cut2)[0] for _ in range(N_SHIFT)]
        info["phase_null_dacc_p99"] = float(np.percentile([v for v in pr if np.isfinite(v)], 99))
        ped = ar1_pedestal(self_ctx)
        pa, pn = score_info(selffeat(ped, ped, ped)[:-1], y, cut2)
        info["pedestal_dacc"], info["pedestal_nats"] = pa, pn
        # POS spike-in: label follows self_hi with p_flip=0.35 -> truth D-acc = 0.65
        hi = (self_ctx > np.median(self_ctx)).astype(int)[:-1]
        flip = (RNG.random(m) < POS_P).astype(int)
        y_pos = hi ^ flip
        pos_a, pos_n = score_info(F, y_pos, cut2)
        info["pos_truth_dacc"] = POS_TRUTH
        info["pos_meas_dacc"] = pos_a
        info["pos_ratio"] = pos_a / POS_TRUTH
        info["PASS"] = bool(info["exp_dacc"] > info["circ_null_dacc_p99"]
                            and info["exp_nats"] >= BAR_NATS)
        info["TOST_NULL"] = bool(abs(info["exp_dacc"] - info["circ_null_dacc_med"]) <= EQ_ACC
                                 and abs(info["exp_nats"]) <= EQ_NATS)
    else:
        info["PASS"] = None
        info["note"] = "degenerate DV -> INFO undefined"
    out["INFO"] = info

    # ── verdict assembly (prereg decision table) ─────────────────────────────
    pos_ok = True
    reasons = []
    if info.get("pos_ratio") is not None and np.isfinite(info.get("pos_ratio", np.nan)):
        if not (0.8 <= info["pos_ratio"] <= 1.25):
            pos_ok = False
            reasons.append(f"INFO POS ratio {info['pos_ratio']:.2f} outside [0.8,1.25]")
    if degen:
        out["verdict"] = "NOT-POWERED"
        out["reason"] = "; ".join(degen)
    elif not pos_ok:
        out["verdict"] = "INVALID"
        out["reason"] = "; ".join(reasons)
    elif info.get("PASS") and pres.get("PASS"):
        out["verdict"] = "PASS"
        out["branch"] = "CONSUMPTION-ABSENT (representation present AND emit-informative) = reframe"
    elif pres.get("PASS") and info.get("TOST_NULL"):
        out["verdict"] = "FAIL"
        out["branch"] = "REPRESENTATION-PRESENT / INFO-ABSENT = same wall as G1 (consumption)"
    elif (not pres.get("PASS")) and info.get("TOST_NULL"):
        out["verdict"] = "FAIL"
        out["branch"] = "DATA/REPRESENTATION-ABSENT = sigma-perp-mouth is design-consistent"
    else:
        out["verdict"] = "INVALID"
        out["reason"] = "neither PASS nor TOST-equivalence reached (underpowered / mixed)"
    print(json.dumps(out, indent=2))
    with open("RESULT.json", "w") as f:
        json.dump(out, f, indent=2)


if __name__ == "__main__":
    main(sys.argv[1])
