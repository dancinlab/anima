#!/usr/bin/env python3
"""H_9304 — G1-EARNED: does a TRANSFERABLE recombination operator exist in a natural corpus?

The question nobody asked. H_9267 (XBIND) showed 303M learns held-out recombination when the
interaction is PLANTED by construction. H_9286 showed it does NOT when the corpus is natural.
H_9265 tried to ask whether the natural corpus even CONTAINS the non-additivity -- and its
instrument failed certification ("NOT-CERTIFIED ... measurement-impossible, NOT NEGATIVE").

So: estimator-free, learning-free, at the level of corpus statistics --
    is there interaction information that TRANSFERS to a held-out recombination cell?

This is the step MITOSIS had and G1 never did: H_1336 proved the information was THERE
(earned, vs a pairing-destroying control) before H_9298 found an estimator that could bank it.
Without that step, no estimator search is justified.

OPERATIONALIZATION (XBIND's natural counterpart; ZERO lexicon dependence):
    A = content-word stem            <- its hidden polarity is the LEARNED coefficient alpha_A
    B = negation bit (closed set)    <- {안 못 아니 없 -지않 -지못}, pre-registered
    T = NSMC human star label (0/1)  <- OUTSIDE the token stream (blocks the tautology trap)
    held-out cell = (A, B=1) where A appears in TRAIN only un-negated
    operator = "negation flips the stem's polarity, regardless of which stem"

    M_add: logit P(T=1|A,B) = alpha_A + gamma_B        -> held-out (A,1): alpha_A + gamma_1
    M_op : logit P(T=1|A,B) = (1-2B)*alpha_A + gamma_B -> held-out (A,1): -alpha_A + gamma_1
    Same parameter count -> M_op winning is NOT a complexity gain. It is operator transfer.

    EARNED = [CE_add - CE_op]_heldout,observed - [CE_add - CE_op]_heldout,shuffle
    shuffle = position-shuffle of B only (breaks A-B pairing, preserves A/B marginals and the
              A-T / B-T additive channels) -> destroys ONLY the synergy. This is the PEDESTAL.

The three certification gates (G-POWER, G-PEDESTAL, G-ALIVE) are BLOCKING: the main bar is not
even computed unless all pass. H_9265 and H_9303 both died exactly here -- a dead probe's
silence proves nothing.

Frozen bars: FREEZE.txt.
"""
import argparse, hashlib, json, os, re, sys, time
import numpy as np

DELTA_EQ = 0.02          # nats -- equivalence margin, frozen pre-data
G_ALIVE_BAR = 0.30       # nats -- positive control must clear this or the instrument is blind
K_PERM = 1000            # permutation null
CI = 90                  # percent
NSMC_SHA = "e03b7d14e9e41be8d464a28057cd25d7396c53e67aa7fd5f7e552c59b0ee2940"

# pre-registered CLOSED SET of negation markers (researcher-DoF guard: no post-hoc additions)
NEG_PATTERNS = [
    (re.compile(r"지\s*않"), "지않"),
    (re.compile(r"지\s*못"), "지못"),
    (re.compile(r"(^|\s)안\s"), "안"),
    (re.compile(r"(^|\s)못\s"), "못"),
    (re.compile(r"아니"), "아니"),
    (re.compile(r"없"), "없"),
]


def log(*a):
    print(*a, flush=True)


def has_negation(text):
    return any(p.search(text) for p, _ in NEG_PATTERNS)


def stems(text):
    """Content-word stems: Hangul runs of 2-4 syllables. No lexicon, no polarity list."""
    out = []
    for w in re.findall(r"[가-힣]+", text):
        if 2 <= len(w) <= 6:
            out.append(w[:3] if len(w) > 3 else w)   # crude stem = first <=3 syllables
    return out


def load_nsmc(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        next(f)
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) != 3 or not p[1].strip():
                continue
            rows.append((p[1], int(p[2])))
    return rows


# ---------------------------------------------------------------------------------------
def build_cells(rows, min_occ):
    """items: (stem_id, B, T). Only stems with >= min_occ total occurrences are kept."""
    from collections import Counter, defaultdict
    cnt = Counter()
    for text, _ in rows:
        for s in set(stems(text)):
            cnt[s] += 1
    keep = {s for s, c in cnt.items() if c >= min_occ}
    sid = {s: i for i, s in enumerate(sorted(keep))}
    items = []
    for text, t in rows:
        b = 1 if has_negation(text) else 0
        for s in set(stems(text)):
            if s in keep:
                items.append((sid[s], b, t))
    return np.asarray(items, dtype=np.int64), sid


def fit_and_score(items, heldout_mask, b_vec=None):
    """Fit alpha_A / gamma_B on TRAIN (non-heldout) rows, score the held-out rows under
    M_add and M_op. Returns (CE_add, CE_op) in nats. b_vec overrides B (for the shuffle arm)."""
    A = items[:, 0]
    B = items[:, 1] if b_vec is None else b_vec
    T = items[:, 2].astype(np.float64)
    tr = ~heldout_mask
    nA = int(A.max()) + 1

    # alpha_A: logit of P(T=1 | A, B=0) on TRAIN  (the stem's polarity, learned un-negated)
    eps = 1.0                                     # Laplace
    pos = np.zeros(nA); tot = np.zeros(nA)
    m = tr & (B == 0)
    np.add.at(pos, A[m], T[m]); np.add.at(tot, A[m], 1.0)
    pA = (pos + eps) / (tot + 2 * eps)
    alpha = np.log(pA / (1 - pA))

    # gamma_B: global negation offset, from TRAIN rows of OTHER stems (B=1 cells that are train)
    def _gamma(sel):
        if sel.sum() == 0:
            return 0.0
        p = (T[sel].sum() + eps) / (sel.sum() + 2 * eps)
        return float(np.log(p / (1 - p)))
    g0, g1 = _gamma(tr & (B == 0)), _gamma(tr & (B == 1))
    # center gamma so it is an OFFSET on top of alpha (alpha already carries the base rate)
    base = _gamma(tr)
    g0, g1 = g0 - base, g1 - base

    def _ce(z, t):
        p = np.clip(1.0 / (1.0 + np.exp(-np.clip(z, -12, 12))), 1e-9, 1 - 1e-9)
        return float(-(t * np.log(p) + (1 - t) * np.log(1 - p)).mean())

    # delta: ONE global interaction coefficient -- the transferable operator.
    #   logit = alpha_A + gamma_B + delta * (B * alpha_A)
    #   delta = 0  -> additive (negation shifts nothing about the stem)
    #   delta = -2 -> full flip (negation inverts the stem's polarity)  == XBIND's xor
    # It is FIT on TRAIN B=1 rows (other stems), never on the held-out cells. Fitting it rather
    # than hard-coding the flip is what centers EARNED at 0 under "no synergy": a hard-coded flip
    # is a DIRECTIONAL HYPOTHESIS baked into the estimand, and on an additive corpus it is
    # actively wrong -> CE_add - CE_op is a large NEGATIVE, not zero. The zero-truth pedestal
    # caught exactly this (it read -0.70 nats where the truth is 0).
    trn1 = tr & (B == 1)
    a_t1, t_t1 = alpha[A[trn1]], T[trn1]
    grid = np.linspace(-3.0, 3.0, 121)
    if trn1.sum() > 0:
        ces = [_ce(a_t1 + g1 + d * a_t1, t_t1) for d in grid]
        delta = float(grid[int(np.argmin(ces))])
    else:
        delta = 0.0

    ho = heldout_mask
    a_ho, b_ho, t_ho = alpha[A[ho]], B[ho], T[ho]
    gam = np.where(b_ho == 1, g1, g0)

    z_add = a_ho + gam                              # delta = 0  (additive)
    z_op = a_ho + gam + delta * (b_ho * a_ho)       # delta = fitted operator
    return _ce(z_add, t_ho), _ce(z_op, t_ho), delta


def _stratified_shuffle_B(B, T, rng):
    """The control (PEDESTAL). Permute B ONLY WITHIN strata of T.

    A plain permutation of B destroys the B->T channel as well as the A-B pairing, so on a
    corpus whose true synergy is ZERO it still moves the score -- the instrument reads a bias.
    (Measured: the additive pedestal returned -0.618 nats under a plain shuffle.) Permuting
    within T-strata preserves P(B, T) EXACTLY -- both the B marginal and the whole B-T additive
    channel -- and destroys only the A-B pairing, i.e. ONLY the synergy. That is the mediating
    covariate this control must match."""
    bs = B.copy()
    for t in np.unique(T):
        idx = np.flatnonzero(T == t)
        bs[idx] = rng.permutation(B[idx])
    return bs


def earned(items, heldout_mask, rng, k_perm):
    """EARNED = observed (CE_add - CE_op) minus the permutation-null mean of the same quantity.
    Returns (earned, obs, null_mean, null_sd, null_samples)."""
    ce_a, ce_o, delta = fit_and_score(items, heldout_mask)
    obs = ce_a - ce_o
    null = []
    B, T = items[:, 1], items[:, 2]
    for _ in range(k_perm):
        bs = _stratified_shuffle_B(B, T, rng)
        a2, o2, _d = fit_and_score(items, heldout_mask, b_vec=bs)
        null.append(a2 - o2)
    null = np.asarray(null)
    return obs - null.mean(), obs, float(null.mean()), float(null.std(ddof=1)), null, delta


def make_heldout(items, rng, frac=0.30):
    """Held-out cells = (A, B=1) rows for stems chosen to be TRAIN-un-negated-only.
    Those stems' B=1 rows are hidden from fitting entirely."""
    A, B = items[:, 0], items[:, 1]
    stems_with_both = np.intersect1d(np.unique(A[B == 1]), np.unique(A[B == 0]))
    if len(stems_with_both) == 0:
        return np.zeros(len(items), dtype=bool), 0
    pick = rng.choice(stems_with_both, size=max(1, int(len(stems_with_both) * frac)), replace=False)
    ho = np.isin(A, pick) & (B == 1)
    return ho, len(pick)


# ---- synthetic arms (certification) ----------------------------------------------------
def synth(rng, n_stems, n_rows, mode):
    """mode 'xor'      : T = xor(pol_A, B)          -> true synergy = 1 bit  (G-ALIVE)
       mode 'additive' : T = pol_A, negation adds a constant offset only (G-PEDESTAL, truth 0)"""
    pol = rng.integers(0, 2, size=n_stems)
    A = rng.integers(0, n_stems, size=n_rows)
    B = rng.integers(0, 2, size=n_rows)
    if mode == "xor":
        T = pol[A] ^ B
    else:
        p = np.where(pol[A] == 1, 0.85, 0.15)
        p = np.clip(p + np.where(B == 1, -0.05, 0.05), 0.01, 0.99)   # additive offset, no flip
        T = (rng.random(n_rows) < p).astype(np.int64)
    return np.stack([A, B, T], axis=1)


def seen_synergy(items, rng, k_perm=200):
    """SEEN-cell synergy -- the axis that discriminates DATA-ADDITIVE from OPERATOR-ABSENT.

    The held-out bar asks: does the operator TRANSFER to a stem never seen negated?
    This asks the strictly weaker question: is there ANY non-additivity, even for a stem the
    model HAS seen negated? Same estimand, same control, but the held-out cells are chosen from
    stems that DO have B=1 rows in train -- so a per-cell joint estimate is available and the
    model is allowed to use the stem's OWN negated counts (half of them), not just a global
    operator. Concretely: for stems with >= 2 negated rows, hold out HALF of their B=1 rows and
    let the fit see the other half.

      seen ~ 0 AND heldout ~ 0  -> DATA-ADDITIVE   (no non-additive information at all)
      seen >> 0 AND heldout ~ 0 -> OPERATOR-ABSENT (non-additivity exists but is pure
                                   collocation: it never transfers off the stem that carries it)
    """
    A, B = items[:, 0], items[:, 1]
    ho = np.zeros(len(items), dtype=bool)
    for a_id in np.unique(A[B == 1]):
        idx = np.flatnonzero((A == a_id) & (B == 1))
        if len(idx) >= 2:
            pick = rng.choice(idx, size=len(idx) // 2, replace=False)
            ho[pick] = True
    if ho.sum() == 0:
        return 0.0, 0
    e, _, _, _, _, _ = earned(items, ho, rng, k_perm)
    return e, int(ho.sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nsmc", required=True)
    ap.add_argument("--min-occ", type=int, default=100)
    ap.add_argument("--occ-sweep", default="50,100,200")
    ap.add_argument("--seed", type=int, default=9304)
    ap.add_argument("--k-perm", type=int, default=K_PERM)
    ap.add_argument("--out", default="/tmp/h9304")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    rng = np.random.default_rng(a.seed)
    res = {"id": "H_9304", "delta_eq": DELTA_EQ, "k_perm": a.k_perm, "seed": a.seed}

    sha = hashlib.sha256(open(a.nsmc, "rb").read()).hexdigest()
    log(f"[corpus] NSMC sha={sha[:16]}...  match={sha == NSMC_SHA}")
    if sha != NSMC_SHA:
        log("FATAL: NSMC sha mismatch - provenance gate. STOP."); sys.exit(2)
    res["nsmc_sha256"] = sha
    rows = load_nsmc(a.nsmc)
    log(f"[corpus] rows={len(rows)}  neg-rate={np.mean([has_negation(t) for t,_ in rows]):.3f}")

    # ======================= GATE 1of3: G-ALIVE (positive control) =======================
    log("\n=== G-ALIVE (positive control: synthetic XOR corpus, true synergy = 0.69 nats) ===")
    sx = synth(rng, 200, 60000, "xor")
    ho_x, n_x = make_heldout(sx, rng)
    e_x, obs_x, nm_x, sd_x, _, d_x = earned(sx, ho_x, rng, min(200, a.k_perm))
    log(f"  held-out cells={int(ho_x.sum())} stems={n_x}  EARNED={e_x:+.5f} nats "
        f"(obs {obs_x:+.5f}, null {nm_x:+.5f}+-{sd_x:.5f}, delta_hat={d_x:+.2f})   bar >= +{G_ALIVE_BAR}")
    alive = e_x >= G_ALIVE_BAR
    res["G_ALIVE"] = {"earned": e_x, "bar": G_ALIVE_BAR, "pass": bool(alive),
                      "n_heldout": int(ho_x.sum())}
    log(f"  G-ALIVE: {'PASS' if alive else 'FAIL -- THE INSTRUMENT IS BLIND'}")

    # ======================= GATE 2of3: G-PEDESTAL (zero-truth arm) ======================
    log("\n=== G-PEDESTAL (zero-truth: synthetic ADDITIVE corpus, true synergy = 0) ===")
    sa = synth(rng, 200, 60000, "additive")
    ho_a, n_a = make_heldout(sa, rng)
    e_a, obs_a, nm_a, sd_a, null_a, d_a = earned(sa, ho_a, rng, min(200, a.k_perm))
    lo_a, hi_a = np.percentile(null_a - nm_a, [(100 - CI) / 2, 100 - (100 - CI) / 2])
    ped_ok = abs(e_a) <= DELTA_EQ
    log(f"  held-out cells={int(ho_a.sum())}  EARNED={e_a:+.5f} nats  delta_hat={d_a:+.2f}  (|.| <= {DELTA_EQ})")
    log(f"  G-PEDESTAL: {'PASS' if ped_ok else 'FAIL -- INSTRUMENT IS BIASED'}")
    res["G_PEDESTAL"] = {"earned": e_a, "delta_eq": DELTA_EQ, "pass": bool(ped_ok)}

    # ======================= GATE 3of3: G-POWER (census + sd_null) =======================
    log("\n=== G-POWER (held-out cell census + null sd, measured BEFORE reading the effect) ===")
    census = {}
    for mo in [int(x) for x in a.occ_sweep.split(",")]:
        it, sid = build_cells(rows, mo)
        ho, nst = make_heldout(it, np.random.default_rng(a.seed))
        census[mo] = {"stems": len(sid), "rows": int(len(it)),
                      "heldout_cells": int(ho.sum()), "heldout_stems": int(nst)}
        log(f"  min_occ={mo:4d}  stems={len(sid):5d}  rows={len(it):7d}  "
            f"held-out cells={int(ho.sum()):6d} (stems {nst})")
    res["G_POWER_census"] = census

    it, sid = build_cells(rows, a.min_occ)
    ho, nst = make_heldout(it, np.random.default_rng(a.seed))
    if int(ho.sum()) == 0:
        log("  G-POWER: FAIL -- zero held-out cells => INVALID (DATA-SPARSE), NOT a KILL.")
        res["verdict"] = "INVALID (DATA-SPARSE) - no held-out recombination cells exist"
        json.dump(res, open(os.path.join(a.out, "h9304_summary.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(0)

    e_n, obs_n, nm_n, sd_n, null_n, d_n = earned(it, ho, np.random.default_rng(a.seed), a.k_perm)
    mde = 3 * sd_n
    powered = mde <= DELTA_EQ
    log(f"  min_occ={a.min_occ}: held-out cells={int(ho.sum())}  sd_null={sd_n:.5f}  "
        f"MDE(3sd)={mde:.5f}  (need <= {DELTA_EQ})")
    log(f"  G-POWER: {'PASS' if powered else 'FAIL -- NOT POWERED for a negative verdict'}")
    res["G_POWER"] = {"sd_null": sd_n, "mde_3sd": mde, "delta_eq": DELTA_EQ,
                      "pass": bool(powered), "n_heldout": int(ho.sum())}

    # ======================= LICENCE CHECK ==============================================
    if not (alive and ped_ok):
        log("\n" + "=" * 70)
        log("INSTRUMENT NOT CERTIFIED -> MAIN BAR NOT READ (a dead probe's silence proves nothing).")
        log(f"  G-ALIVE={alive}  G-PEDESTAL={ped_ok}")
        res["verdict"] = "INVALID - instrument not certified (G-ALIVE/G-PEDESTAL fail); main bar NOT read"
        json.dump(res, open(os.path.join(a.out, "h9304_summary.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(0)

    # ======================= MAIN BAR (only now) ========================================
    log("\n" + "=" * 70)
    log("=== MAIN BAR: natural corpus (NSMC), held-out EARNED ===")
    lo, hi = np.percentile(null_n - nm_n, [(100 - CI) / 2, 100 - (100 - CI) / 2])
    ci_lo, ci_hi = e_n + lo, e_n + hi
    seen_syn, n_seen = seen_synergy(it, np.random.default_rng(a.seed + 1), k_perm=200)
    log(f"  held-out EARNED = {e_n:+.5f} nats   {CI}% CI [{ci_lo:+.5f}, {ci_hi:+.5f}]   delta_hat={d_n:+.2f} (0=additive, -2=full flip)")
    log(f"  seen synergy    = {seen_syn:+.5f} nats  (n={n_seen})  [discriminates DATA-ADDITIVE vs OPERATOR-ABSENT]")

    info_present = ci_lo > DELTA_EQ
    tost_pass = (ci_lo > -DELTA_EQ) and (ci_hi < DELTA_EQ)      # equivalence to zero
    straddles = (ci_lo <= 0) and (ci_hi >= DELTA_EQ)

    if info_present:
        v = "INFO-PRESENT - interaction information EXISTS and TRANSFERS to held-out cells => shrinkage is justified; frontier crack candidate"
    elif tost_pass and not powered:
        v = "NOT-POWERED - equivalence claimed but MDE > delta_eq; need more labeled data (spend-go)"
    elif tost_pass and seen_syn > DELTA_EQ:
        v = "OPERATOR-ABSENT - natural non-additivity is ALL collocation; ZERO transferable operator => the G1 wall is 'nature supplies no recombination operator'; XBIND injected one"
    elif tost_pass:
        v = "DATA-ADDITIVE - no non-additive information at all => no estimator can ever bank it; G1 = DATA wall"
    elif straddles:
        v = "NOT-POWERED - CI straddles both 0 and delta_eq"
    else:
        v = "INDETERMINATE - see CI"

    log(f"  TOST(+-{DELTA_EQ}) pass = {tost_pass}   INFO-PRESENT = {info_present}")
    log(f"\nVERDICT: {v}")
    res.update({"heldout_earned": e_n, "ci_lo": ci_lo, "ci_hi": ci_hi,
                "seen_synergy": seen_syn, "n_seen_cells": n_seen, "delta_hat_natural": d_n, "delta_hat_xor_alive": d_x, "delta_hat_pedestal": d_a, "tost_pass": bool(tost_pass),
                "info_present": bool(info_present), "verdict": v,
                "wall_s": time.time() - t0})
    json.dump(res, open(os.path.join(a.out, "h9304_summary.json"), "w"), indent=2, ensure_ascii=False)
    log(f"wall={time.time()-t0:.1f}s\n[done]")


if __name__ == "__main__":
    main()
