#!/usr/bin/env python3
"""INTERACT-SOURCE screener: conditional MI I(A; Y | S) on anima self-execution traces.

Pre-registration: state/h9308_interact_source/PREREG.md (frozen before effect estimates).
$0 CPU-local. No GPU, no pod.

Arms: REAL / ACTION-SHUFFLE / STATE-ONLY / PEDESTAL(true=0) / ALIVE(known truth).
Estimator: plugin + Miller-Madow bias correction, nats.
Inference: block bootstrap CI, within-stratum permutation null, paired-t over blocks.
"""
import json, math, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "RESULT.json")

TRACES = [
    "state/h9269_candidateY/results/pod_harvest/trace_B_mnemosyne.jsonl",
    "state/h9269_candidateY/results/pod_harvest/trace_C_thanatos.jsonl",
    "state/h9269_candidateY/results/pod_harvest/trace_D_orpheus.jsonl",
    "state/h1058_agency_daemon/results/trace_303m_summer.jsonl",
    "state/h1058_agency_daemon/results/trace_303mb.jsonl",
]
CTX = ["nov_ctx", "rel_ctx", "cur_ctx", "gap_ctx", "allo_ctx", "agloop_ctx", "scn_ctx"]
MARGIN = 0.02          # TOST equivalence margin, nats
BLOCK = 50             # bootstrap block length (ticks)
PAIRED_BLOCK = 100     # paired-t block length
B_BOOT = 2000
B_PERM = 2000


# ---------------------------------------------------------------- estimator
def mi_mm(a, y, s):
    """Conditional MI I(A;Y|S) in nats: plugin + Miller-Madow correction, weighted over strata."""
    a = np.asarray(a); y = np.asarray(y); s = np.asarray(s)
    n = len(a)
    if n == 0:
        return 0.0
    total = 0.0
    for sv in np.unique(s):
        m = s == sv
        ns = int(m.sum())
        if ns < 2:
            continue
        av, yv = a[m], y[m]
        ua, uy = np.unique(av), np.unique(yv)
        if len(ua) < 2 or len(uy) < 2:
            continue  # zero conditional entropy in this stratum -> MI contribution is exactly 0
        # plugin MI
        joint = np.zeros((len(ua), len(uy)))
        for i, x in enumerate(ua):
            for j, z in enumerate(uy):
                joint[i, j] = np.sum((av == x) & (yv == z))
        joint /= ns
        pa = joint.sum(1, keepdims=True)
        py = joint.sum(0, keepdims=True)
        nz = joint > 0
        plug = float(np.sum(joint[nz] * np.log(joint[nz] / (pa @ py)[nz])))
        # Miller-Madow: I_MM = I_plug + (m_A + m_Y - m_AY - 1) / (2 n_s)
        m_a, m_y = len(ua), len(uy)
        m_ay = int(nz.sum())
        plug += (m_a + m_y - m_ay - 1) / (2.0 * ns)
        total += (ns / n) * plug
    return total


def cond_entropy_bits(a, s):
    a = np.asarray(a); s = np.asarray(s); n = len(a)
    h = 0.0
    for sv in np.unique(s):
        m = s == sv
        ns = int(m.sum())
        p = np.array([np.mean(a[m] == v) for v in np.unique(a[m])])
        p = p[p > 0]
        h += (ns / n) * float(-np.sum(p * np.log(p)))
    return h  # nats


def mi_uncond(x, y):
    return mi_mm(x, y, np.zeros(len(x), dtype=int))


# ---------------------------------------------------------------- data
def load(path):
    rows = []
    for line in open(os.path.join(ROOT, path)):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        if d.get("_meta"):
            continue
        rows.append(d)
    return rows


def build(rows):
    """A (emit), Y (binarized subsequent context change), S (stage). Last tick dropped (no t+1)."""
    C = np.array([[r[k] for k in CTX] for r in rows], dtype=float)
    dC = np.abs(C[1:] - C[:-1]).sum(1)          # ||C_{t+1} - C_t||_1
    A = np.array([1 if r["emit"] else 0 for r in rows[:-1]], dtype=int)
    S = np.array([int(r["stage"]) for r in rows[:-1]], dtype=int)
    Y = (dC >= np.median(dC)).astype(int)
    idle = np.array([r["idle"] for r in rows[:-1]], dtype=float)
    return A, Y, S, dC, idle


# ---------------------------------------------------------------- arms
def arm_pedestal(A, S, rng):
    """True I(A;Y|S)=0: redraw A from the empirical p(A|S), no causal path to Y."""
    out = np.zeros_like(A)
    for sv in np.unique(S):
        m = S == sv
        p = A[m].mean()
        out[m] = rng.random(m.sum()) < p
    return out.astype(int)


def arm_shuffle(A, S, rng):
    """Within-stratum permutation of A: preserves p(A|S) and p(Y|S), destroys the joint."""
    out = A.copy()
    for sv in np.unique(S):
        idx = np.where(S == sv)[0]
        out[idx] = A[idx][rng.permutation(len(idx))]
    return out


def arm_alive(S, rng, true_flip=0.10):
    """Positive control with a KNOWN true MI: inject residual action entropy (Bernoulli .5 within
    each stratum) and let Y = A flipped with prob `true_flip`. True I(A;Y|S) = ln2 - H(flip)."""
    n = len(S)
    A = (rng.random(n) < 0.5).astype(int)
    flip = rng.random(n) < true_flip
    Y = np.where(flip, 1 - A, A)
    truth = math.log(2) - (-(true_flip * math.log(true_flip) + (1 - true_flip) * math.log(1 - true_flip)))
    return A, Y, truth


def alive_at_truth(S, rng, target_nats):
    """Solve flip prob so that true MI == target (used for N_REQ power simulation)."""
    lo, hi = 1e-6, 0.5 - 1e-9
    for _ in range(80):
        mid = (lo + hi) / 2
        t = math.log(2) + mid * math.log(mid) + (1 - mid) * math.log(1 - mid)
        if t > target_nats:
            lo = mid
        else:
            hi = mid
    flip = (lo + hi) / 2
    n = len(S)
    A = (rng.random(n) < 0.5).astype(int)
    fl = rng.random(n) < flip
    Y = np.where(fl, 1 - A, A)
    t = math.log(2) + flip * math.log(flip) + (1 - flip) * math.log(1 - flip)
    return A, Y, t, flip


# ---------------------------------------------------------------- inference
def block_boot(A, Y, S, rng, B=B_BOOT, L=BLOCK):
    n = len(A)
    nb = max(1, n // L)
    starts = np.arange(0, n - L + 1)
    est = []
    for _ in range(B):
        idx = np.concatenate([np.arange(s, s + L) for s in rng.choice(starts, nb)])
        est.append(mi_mm(A[idx], Y[idx], S[idx]))
    return np.array(est)


def perm_null(A, Y, S, rng, B=B_PERM):
    return np.array([mi_mm(arm_shuffle(A, S, rng), Y, S) for _ in range(B)])


def paired_t(d):
    d = np.asarray(d, dtype=float)
    k = len(d)
    if k < 2 or np.allclose(d.std(ddof=1), 0):
        return float(d.mean()), 0.0, float("nan"), float("nan")
    se = d.std(ddof=1) / math.sqrt(k)
    t = d.mean() / se
    # normal approx p (two-sided); k small but this is reported alongside the bootstrap CI
    p = math.erfc(abs(t) / math.sqrt(2))
    return float(d.mean()), float(se), float(t), float(p)


def tost(lo90, hi90, margin=MARGIN):
    """Equivalence if the 90% CI lies entirely inside (-margin, margin)."""
    return bool(lo90 > -margin and hi90 < margin)


# ---------------------------------------------------------------- main
def main():
    res = {"prereg": "state/h9308_interact_source/PREREG.md", "margin_nats": MARGIN, "traces": {}}
    rng = np.random.default_rng(20260714)

    pooled = {"A": [], "Y": [], "S": [], "idle": []}
    for path in TRACES:
        rows = load(path)
        A, Y, S, dC, idle = build(rows)
        name = os.path.basename(path)
        # cross-tab (stage, emit)
        ct = {}
        for sv in np.unique(S):
            m = S == sv
            ct[int(sv)] = {"n": int(m.sum()), "emit1": int(A[m].sum()), "emit0": int((1 - A[m]).sum())}
        res["traces"][name] = {
            "n_pairs": int(len(A)),
            "H_A_nats": float(cond_entropy_bits(A, np.zeros(len(A), dtype=int))),
            "H_A_given_stage_nats": float(cond_entropy_bits(A, S)),
            "stage_emit_crosstab": ct,
            "dC_median": float(np.median(dC)),
            "Y_mean": float(Y.mean()),
        }
        pooled["A"].append(A); pooled["Y"].append(Y); pooled["S"].append(S); pooled["idle"].append(idle)

    A = np.concatenate(pooled["A"]); Y = np.concatenate(pooled["Y"])
    S = np.concatenate(pooled["S"]); idle = np.concatenate(pooled["idle"])
    n = len(A)

    # ---- V-CEILING (power gate, computed before any effect claim)
    H_A = cond_entropy_bits(A, np.zeros(n, dtype=int))
    H_A_S = cond_entropy_bits(A, S)
    ceiling_pass = H_A_S > MARGIN
    res["pooled"] = {
        "n_pairs": int(n),
        "H_A_nats": float(H_A),
        "H_A_given_S_nats": float(H_A_S),
        "V_CEILING_pass": bool(ceiling_pass),
        "note": "MI(A;Y|S) <= H(A|S) is an identity bound; if H(A|S) < margin no n can yield PASS.",
    }

    # ---- N_REQ power simulation (estimator-side; independent of the real policy)
    nreq = None
    powers = {}
    for ntry in [200, 500, 1000, 2000, 2705, 5000, 10000]:
        rg = np.random.default_rng(777 + ntry)
        Ssim = rg.choice(np.unique(S), ntry, p=np.array([np.mean(S == s) for s in np.unique(S)]))
        hits = 0
        REP = 200
        for _ in range(REP):
            Aa, Yy, truth, _ = alive_at_truth(Ssim, rg, MARGIN)
            obs = mi_mm(Aa, Yy, Ssim)
            null = np.array([mi_mm(arm_shuffle(Aa, Ssim, rg), Yy, Ssim) for _ in range(60)])
            if (np.sum(null >= obs) + 1) / (len(null) + 1) < 0.05:
                hits += 1
        powers[ntry] = hits / REP
        if nreq is None and hits / REP >= 0.80:
            nreq = ntry
    res["power"] = {
        "target_true_MI_nats": MARGIN,
        "power_by_n": powers,
        "N_REQ_80pct": nreq,
        "assumes": "a policy with residual entropy H(A|S)=ln2 (Bernoulli .5 within stratum)",
    }

    # ---- arms (PRIMARY: S = stage)
    arms = {}
    mi_real = mi_mm(A, Y, S)
    ped = arm_pedestal(A, S, np.random.default_rng(101))
    mi_ped = mi_mm(ped, Y, S)
    shf = arm_shuffle(A, S, np.random.default_rng(202))
    mi_shf = mi_mm(shf, Y, S)
    mi_state_only = mi_uncond(S, Y)   # arm 3: is the Y channel alive at all w.r.t. state?
    Aal, Yal, truth = arm_alive(S, np.random.default_rng(303))
    mi_alive = mi_mm(Aal, Yal, S)

    arms["REAL"] = float(mi_real)
    arms["PEDESTAL_true0"] = float(mi_ped)
    arms["ACTION_SHUFFLE"] = float(mi_shf)
    arms["STATE_ONLY_I(S;Y)"] = float(mi_state_only)
    arms["ALIVE"] = {"measured": float(mi_alive), "truth": float(truth),
                     "ratio": float(mi_alive / truth) if truth else None}
    res["arms_primary_S_stage"] = arms

    # V-gates
    boot_ped = block_boot(ped, Y, S, np.random.default_rng(404), B=500)
    v_ped = bool(abs(mi_ped) <= 3 * (boot_ped.std() if boot_ped.std() > 0 else 1e-12) or abs(mi_ped) < 1e-12)
    v_alive = bool(truth > 0 and 0.75 <= (mi_alive / truth) <= 1.25)
    res["V_gates"] = {"V_CEILING": bool(ceiling_pass), "V_ALIVE": v_alive, "V_PEDESTAL": v_ped}

    # ---- inference on REAL - PEDESTAL (paired over blocks) + bootstrap CI
    diffs = []
    for st in range(0, n - PAIRED_BLOCK + 1, PAIRED_BLOCK):
        sl = slice(st, st + PAIRED_BLOCK)
        diffs.append(mi_mm(A[sl], Y[sl], S[sl]) - mi_mm(ped[sl], Y[sl], S[sl]))
    m, se, t, p = paired_t(diffs)
    boot = block_boot(A, Y, S, np.random.default_rng(505), B=B_BOOT)
    lo90, hi90 = float(np.percentile(boot, 5)), float(np.percentile(boot, 95))
    lo95, hi95 = float(np.percentile(boot, 2.5)), float(np.percentile(boot, 97.5))
    null = perm_null(A, Y, S, np.random.default_rng(606), B=B_PERM)
    pval = float((np.sum(null >= mi_real) + 1) / (len(null) + 1))
    res["inference_primary"] = {
        "MI_real_nats": float(mi_real),
        "paired_t_blocks": {"k_blocks": len(diffs), "mean_diff": m, "se": se, "t": t, "p_two_sided": p},
        "bootstrap_CI90": [lo90, hi90], "bootstrap_CI95": [lo95, hi95],
        "perm_null_mean": float(null.mean()), "perm_null_sd": float(null.std()), "perm_p": pval,
        "TOST_equivalent_pm0.02": tost(lo90, hi90),
    }

    # ---- SECONDARY DIAGNOSTIC (pre-registered as diagnostic only, cannot be a PASS route)
    q = np.quantile(idle, [1 / 3, 2 / 3])
    Slite = np.digitize(idle, q)
    d_real = mi_mm(A, Y, Slite)
    d_ped = mi_mm(arm_pedestal(A, Slite, np.random.default_rng(707)), Y, Slite)
    d_null = np.array([mi_mm(arm_shuffle(A, Slite, np.random.default_rng(800 + i)), Y, Slite) for i in range(300)])
    res["secondary_diagnostic_S_lite_idle_tercile"] = {
        "H_A_given_Slite_nats": float(cond_entropy_bits(A, Slite)),
        "MI_real": float(d_real), "MI_pedestal": float(d_ped),
        "perm_null_mean": float(d_null.mean()), "perm_null_sd": float(d_null.std()),
        "perm_p": float((np.sum(d_null >= d_real) + 1) / (len(d_null) + 1)),
        "warning": "stage is dropped from the conditioning set -> any lift is stage-mediated confound, NOT a do-effect.",
    }

    with open(OUT, "w") as f:
        json.dump(res, f, indent=2)
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
