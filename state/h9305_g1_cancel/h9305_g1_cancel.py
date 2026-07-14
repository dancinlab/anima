#!/usr/bin/env python3
"""H_9305 -- G1-CANCEL: did the pooled zero of H_9304 hide a stratified cancellation?

H_9304 read ONE pooled number on NSMC: held-out EARNED = +0.0023 nats, TOST(+-0.02) PASS
=> DATA-ADDITIVE. But a pooled zero is also what you get when strata carry synergy of
OPPOSITE SIGN (Simpson / mixture cancellation): negation flips polarity in one register,
irony / litotes re-flips it in another, and the average is exactly nothing.

Nobody asked, because every G1 measurement in the ledger was corpus-global.

This re-reads the SAME certified instrument (H_9304, imported verbatim -- estimator,
control and permutation null are byte-identical) at STRATUM granularity.

  cancellation index  D = sum_k w_k I_k - I_pooled
  (Fable's card-A index C = sum w|I| - |sum w I| was killed by the positive control before any
   natural stratum was read -- it is structurally blind to this estimand's cancellation.
   See AMENDMENT 1 in FREEZE.txt. Bars unmoved.)

ARMS
  EXP    real strata (3 pre-registered schemes: k=8 cluster / byte-length quartile /
         negation-marker family)
  CTRL1  size-matched RANDOM strata -- destroys structure, preserves the small-sample
         estimation bias (the mediating covariate is stratum size)
  CTRL2  within-stratum permutation null, k=500 -- the per-stratum TRUE-ZERO pedestal
  POS    XBIND (+) 50% (+) sign-flipped-XBIND 50%, shared stem pool -- true pooled ~ 0,
         true within-stratum ~ +5.3. If this arm does not fire, the instrument cannot see
         cancellation at all and the verdict is INVALID, not FAIL.

Pre-registration: FREEZE.txt (frozen before any stratified effect was read).
"""
import argparse, hashlib, importlib.util, json, os, re, sys, time
from collections import Counter
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
H9304 = os.path.join(os.path.dirname(HERE), "h9304_g1_earned", "h9304_g1_earned.py")

# --- import the CERTIFIED instrument verbatim (no re-implementation, no edits) -----------
_spec = importlib.util.spec_from_file_location("h9304", H9304)
h9304 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h9304)

DELTA_EQ = h9304.DELTA_EQ          # 0.02 nats -- inherited, frozen
NSMC_SHA = h9304.NSMC_SHA
N_TESTS = 18                       # 8 cluster + 4 length + 6 marker  (pre-registered)
BONF_Q = 1.0 - 0.05 / N_TESTS      # two-sided Bonferroni null quantile
POS_STRAT_BAR = 0.30               # positive control must fire this hard within stratum
POS_D_BAR = 1.0   # AMENDMENT 1: same numeric bar, applied to D (C was structurally blind)
K_PERM = 500


def log(*a):
    print(*a, flush=True)


# ---------------------------------------------------------------------------------------
def build_cells_rowidx(rows, min_occ):
    """Same cell construction as H_9304.build_cells, but also carries the source row index
    so items can be routed to strata. Stem vocabulary is built ONCE, GLOBALLY (min_occ),
    and never re-selected per stratum -- that would be post-hoc selection."""
    cnt = Counter()
    for text, _ in rows:
        for s in set(h9304.stems(text)):
            cnt[s] += 1
    keep = {s for s, c in cnt.items() if c >= min_occ}
    sid = {s: i for i, s in enumerate(sorted(keep))}
    items, ridx = [], []
    for r, (text, t) in enumerate(rows):
        b = 1 if h9304.has_negation(text) else 0
        for s in set(h9304.stems(text)):
            if s in keep:
                items.append((sid[s], b, t))
                ridx.append(r)
    return np.asarray(items, dtype=np.int64), np.asarray(ridx, dtype=np.int64), sid


def stratum_earned(items_k, rng, k_perm):
    """Run the certified instrument INSIDE one stratum. alpha/gamma/delta/held-out are all
    refit within the stratum. Returns dict or None if the stratum has no held-out cells."""
    if len(items_k) == 0:
        return None
    ho, nst = h9304.make_heldout(items_k, rng)
    n_ho = int(ho.sum())
    if n_ho == 0:
        return None
    e, obs, nm, sd, null, delta = h9304.earned(items_k, ho, rng, k_perm)
    centred = null - nm
    lo, hi = np.percentile(centred, [5.0, 95.0])          # 90% CI, same as H_9304
    ped = float(np.quantile(np.abs(centred), BONF_Q))     # Bonferroni two-sided pedestal
    mde = 3.0 * sd
    bar = max(ped, DELTA_EQ)                              # absolute floor 0.02 never lowered
    ci_lo, ci_hi = e + lo, e + hi
    return {
        "n_items": int(len(items_k)), "n_heldout": n_ho, "n_heldout_stems": int(nst),
        "earned": float(e), "obs": float(obs), "null_mean": float(nm), "null_sd": float(sd),
        "ci_lo": float(ci_lo), "ci_hi": float(ci_hi), "delta_hat": float(delta),
        "pedestal_bonf": ped, "bar": float(bar), "mde_3sd": float(mde),
        "powered": bool(mde <= DELTA_EQ),
        "significant": bool(abs(e) > bar),
        "tost_pass": bool(ci_lo > -DELTA_EQ and ci_hi < DELTA_EQ),
    }


def cancellation_index(strata, pooled_earned):
    """CANCELLATION INDEX  D = sum_k w_k*I_k  -  I_pooled     (w = held-out cell share)

    AMENDMENT 1 (FREEZE.txt): Fable's card-A index C = sum w|I| - |sum w I| is STRUCTURALLY
    incapable of expressing the cancellation this estimand produces, and the positive control
    proved it (C_POS = 0.00000 on an arm whose truth IS cancellation).

    Why: EARNED = CE_add - CE_op fits delta FROM DATA, so it is an operator-RECOVERY MAGNITUDE
    -- non-negative whenever an operator exists in EITHER direction. Opposite-direction
    operators (flip vs re-flip) appear as opposite-sign delta_hat, NOT as a sign flip of I.
    So I_k < 0 essentially never happens and C is pinned at ~0 on every corpus, including one
    built to cancel. Left in place it would have manufactured "no cancellation" for free.

    D expresses BOTH cancellation channels:
      (a) main-effect cancellation  (alpha_A opposite across strata -> pooled alpha collapses
          -> pooled I ~ 0 while each stratum reads large)   <- this is what POS builds
      (b) operator-direction cancellation (delta_hat opposite across strata -> the pooled delta
          is an average and is wrong for both)
    Both give D > 0. C is retained in the output for transparency only; it is not a criterion.
    """
    if not strata:
        return None
    w = np.asarray([s["n_heldout"] for s in strata], dtype=np.float64)
    w = w / w.sum()
    I = np.asarray([s["earned"] for s in strata], dtype=np.float64)
    strat = float((w * I).sum())
    return {"D": strat - float(pooled_earned), "strat_w_mean": strat,
            "pooled": float(pooled_earned),
            "C_legacy_not_a_criterion": float((w * np.abs(I)).sum() - abs(strat))}


def paired_t(a, b):
    """Paired t over matched stratum indices. NEVER max(controls) -- that order statistic
    mechanically manufactures KILLs (probe-defect-census-max-control-bias)."""
    d = np.asarray(a, dtype=np.float64) - np.asarray(b, dtype=np.float64)
    n = len(d)
    if n < 2:
        return {"n": n, "mean_diff": float(d.mean()) if n else 0.0, "t": None, "p": None}
    sd = d.std(ddof=1)
    t = float(d.mean() / (sd / np.sqrt(n))) if sd > 0 else float("inf")
    # two-sided p via survival of |t| under t_{n-1}, normal approx guard for tiny n
    try:
        from statistics import NormalDist
        p = 2 * (1 - NormalDist().cdf(abs(t))) if np.isfinite(t) else 0.0
    except Exception:
        p = None
    return {"n": n, "mean_diff": float(d.mean()), "sd_diff": float(sd), "t": t, "p_approx_normal": p}


def run_scheme(name, items, ridx, row_stratum, n_strata, seed, k_perm, pooled_earned, partition=True):
    """EXP arm for one stratification scheme + its size-matched random control (CTRL1)."""
    log(f"\n--- scheme {name}  ({n_strata} strata, partition={partition}) ---")
    item_strat = row_stratum[ridx]
    exp, ctrl = [], []

    # CTRL1: size-matched random strata -- permute the ROW->stratum map (row sizes preserved
    # exactly, so per-stratum cell counts match in distribution; structure destroyed).
    rrng = np.random.default_rng(seed + 777)
    row_strat_rand = rrng.permutation(row_stratum)
    item_strat_rand = row_strat_rand[ridx]

    for k in range(n_strata):
        e = stratum_earned(items[item_strat == k], np.random.default_rng(seed + k), k_perm)
        c = stratum_earned(items[item_strat_rand == k], np.random.default_rng(seed + k), k_perm)
        for d, tag in ((e, "EXP"), (c, "CTRL1")):
            if d is not None:
                d["stratum"] = k
        exp.append(e); ctrl.append(c)
        if e is None:
            log(f"  k={k}: EMPTY (no held-out cells)")
            continue
        cs = "  --" if c is None else f"{c['earned']:+.5f}"
        log(f"  k={k}: n_ho={e['n_heldout']:6d}  I={e['earned']:+.5f}  "
            f"CI[{e['ci_lo']:+.5f},{e['ci_hi']:+.5f}]  d_hat={e['delta_hat']:+.2f}  "
            f"bar={e['bar']:.4f}  MDE={e['mde_3sd']:.5f}  "
            f"sig={'Y' if e['significant'] else 'n'} tost={'Y' if e['tost_pass'] else 'n'} "
            f"| CTRL1 I={cs}")

    exp_ok = [s for s in exp if s is not None]
    ctl_ok = [s for s in ctrl if s is not None]
    out = {"scheme": name, "n_strata": n_strata, "partition": partition,
           "exp": exp_ok, "ctrl1_random": ctl_ok}
    if partition:
        out["D_exp"] = cancellation_index(exp_ok, pooled_earned)
        out["D_ctrl1"] = cancellation_index(ctl_ok, pooled_earned)
        # paired contrast on matched stratum indices (both arms present)
        pk = [k for k in range(n_strata) if exp[k] is not None and ctrl[k] is not None]
        out["paired_t_exp_vs_ctrl1"] = paired_t([exp[k]["earned"] for k in pk],
                                                [ctrl[k]["earned"] for k in pk])
        pt = out["paired_t_exp_vs_ctrl1"]
        log(f"  D_exp   = {out['D_exp']['D']:+.5f}   (strat_w={out['D_exp']['strat_w_mean']:+.5f}, pooled={pooled_earned:+.5f})")
        log(f"  D_ctrl1 = {out['D_ctrl1']['D']:+.5f}   <- size-matched RANDOM strata (small-sample baseline)")
        log(f"  paired-t EXP vs CTRL1: mean_diff={pt['mean_diff']:+.5f} t={pt['t']} n={pt['n']}")
        log(f"  (legacy C_exp={out['D_exp']['C_legacy_not_a_criterion']:+.5f} -- NOT a criterion, see AMENDMENT 1)")
    return out


# ---------------------------------------------------------------------------------------
def kmeans_strata(rows, k, seed, dim=256, iters=12):
    """Unsupervised k=8 clusters. char-3gram hashing -> L2 norm -> k-means. No labels."""
    import zlib
    rng = np.random.default_rng(seed)
    X = np.zeros((len(rows), dim), dtype=np.float32)
    for i, (text, _) in enumerate(rows):
        t = text
        for j in range(max(0, len(t) - 2)):
            # zlib.crc32 (NOT python hash(), which is per-process randomised) -> deterministic
            X[i, zlib.crc32(t[j:j + 3].encode("utf-8")) % dim] += 1.0
    n = np.linalg.norm(X, axis=1, keepdims=True)
    X /= np.maximum(n, 1e-6)
    C = X[rng.choice(len(X), size=k, replace=False)].copy()
    lab = np.zeros(len(X), dtype=np.int64)
    for _ in range(iters):
        lab = np.argmax(X @ C.T, axis=1)            # cosine (unit-norm rows)
        for c in range(k):
            m = lab == c
            if m.sum() > 0:
                v = X[m].mean(axis=0)
                C[c] = v / max(np.linalg.norm(v), 1e-6)
            else:
                C[c] = X[rng.integers(0, len(X))]
    return lab


def length_strata(rows):
    """Byte-length quartiles (a_korean_byte_budget: bytes, not chars)."""
    L = np.asarray([len(t.encode("utf-8")) for t, _ in rows], dtype=np.int64)
    q = np.quantile(L, [0.25, 0.5, 0.75])
    return np.digitize(L, q).astype(np.int64), q


def marker_arms(rows, min_occ, seed, k_perm):
    """MECHANISM diagnostic: one arm per negation-marker family.
    NOT a partition (the B=0 pool is shared) -> no C index. Tests directly whether different
    negation markers carry operators of OPPOSITE sign (the cancellation mechanism)."""
    log("\n--- scheme S_MARKER  (6 arms; NOT a partition -> no C index) ---")
    out = []
    for mi, (pat, nm) in enumerate(h9304.NEG_PATTERNS):
        sub = []
        for text, t in rows:
            hit = pat.search(text) is not None
            other = any(p.search(text) for p, n2 in h9304.NEG_PATTERNS if n2 != nm)
            if hit and other:
                continue                       # ambiguous: multiple marker families -> drop
            if hit or not other:
                sub.append((text, t, 1 if hit else 0))
        # rebuild cells on this sub-corpus with the GLOBAL vocab rule (min_occ on the sub)
        cnt = Counter()
        for text, _, _ in sub:
            for s in set(h9304.stems(text)):
                cnt[s] += 1
        keep = {s for s, c in cnt.items() if c >= min_occ}
        sid = {s: i for i, s in enumerate(sorted(keep))}
        it = []
        for text, t, b in sub:
            for s in set(h9304.stems(text)):
                if s in keep:
                    it.append((sid[s], b, t))
        it = np.asarray(it, dtype=np.int64)
        d = stratum_earned(it, np.random.default_rng(seed + 100 + mi), k_perm) if len(it) else None
        if d is None:
            log(f"  {nm:4s}: EMPTY / no held-out cells")
            out.append({"marker": nm, "result": None})
            continue
        d["marker"] = nm
        n1 = int((it[:, 1] == 1).sum())
        d["n_B1_items"] = n1
        log(f"  {nm:4s}: n_ho={d['n_heldout']:6d} B1={n1:6d}  I={d['earned']:+.5f}  "
            f"CI[{d['ci_lo']:+.5f},{d['ci_hi']:+.5f}]  d_hat={d['delta_hat']:+.2f}  "
            f"bar={d['bar']:.4f}  sig={'Y' if d['significant'] else 'n'} "
            f"tost={'Y' if d['tost_pass'] else 'n'}")
        out.append({"marker": nm, "result": d})
    return out


# ---------------------------------------------------------------------------------------
def pos_control(seed, k_perm):
    """POSITIVE CONTROL -- the arm that certifies the instrument CAN see cancellation.

    stratum P : T = xor(pol_A, B)        -> operator delta = -2  (XBIND)
    stratum N : T = 1 - xor(pol_A, B)    -> same operator, but the stem's B=0 polarity is
                                            INVERTED, i.e. sign-flipped XBIND
    Stems are SHARED. Pooled, alpha_A is learned from B=0 rows of BOTH strata, which have
    opposite T -> alpha_A collapses to ~0 -> M_op == M_add -> pooled EARNED ~ 0.
    Within a stratum, alpha_A is strong and the flip is recovered -> I_k ~ +5.3.
    True pooled = 0, true within = large  ==  exactly the Simpson cancellation we hunt.
    """
    log("\n=== POS (XBIND (+) sign-flipped-XBIND, shared stems; true pooled ~ 0, true within ~ +5.3) ===")
    rng = np.random.default_rng(seed)
    n_stems, n_rows = 200, 60000
    pol = rng.integers(0, 2, size=n_stems)
    A = rng.integers(0, n_stems, size=n_rows)
    B = rng.integers(0, 2, size=n_rows)
    S = rng.integers(0, 2, size=n_rows)                 # stratum: 0 = P, 1 = N (sign-flipped)
    T = pol[A] ^ B                                      # XBIND
    T = np.where(S == 1, 1 - T, T)                      # sign-flip inside stratum N
    items = np.stack([A, B, T], axis=1)

    pooled = stratum_earned(items, np.random.default_rng(seed + 1), min(200, k_perm))
    log(f"  POOLED : I={pooled['earned']:+.5f}  d_hat={pooled['delta_hat']:+.2f}   "
        f"(true = 0; this is the cancellation)")
    strata = []
    for k in (0, 1):
        d = stratum_earned(items[S == k], np.random.default_rng(seed + 2 + k), min(200, k_perm))
        d["stratum"] = k
        strata.append(d)
        log(f"  STRAT {k}: I={d['earned']:+.5f}  d_hat={d['delta_hat']:+.2f}  n_ho={d['n_heldout']}")
    D = cancellation_index(strata, pooled["earned"])
    log(f"  D_POS = {D['D']:+.5f}   (bar > {POS_D_BAR})   "
        f"[legacy C_POS = {D['C_legacy_not_a_criterion']:+.5f} -- the defect AMENDMENT 1 killed]")
    fired = (all(s["earned"] >= POS_STRAT_BAR for s in strata)
             and abs(pooled["earned"]) <= DELTA_EQ
             and D["D"] > POS_D_BAR)
    log(f"  POS DETECT: {'PASS -- the instrument CAN see cancellation' if fired else 'FAIL -- INSTRUMENT BLIND TO CANCELLATION'}")
    return {"pooled": pooled, "strata": strata, "D": D, "fired": bool(fired)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--nsmc", required=True)
    ap.add_argument("--min-occ", type=int, default=100)
    ap.add_argument("--k-clust", type=int, default=8)
    ap.add_argument("--seed", type=int, default=9305)
    ap.add_argument("--k-perm", type=int, default=K_PERM)
    ap.add_argument("--out", default=os.path.join(HERE, "results"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    res = {"id": "H_9305", "delta_eq": DELTA_EQ, "seed": a.seed, "k_perm": a.k_perm,
           "n_tests_preregistered": N_TESTS, "bonferroni_q": BONF_Q}

    sha = hashlib.sha256(open(a.nsmc, "rb").read()).hexdigest()
    log(f"[corpus] NSMC sha={sha[:16]}...  match={sha == NSMC_SHA}")
    if sha != NSMC_SHA:
        log("FATAL: sha mismatch -- provenance gate. STOP."); sys.exit(2)
    res["nsmc_sha256"] = sha
    rows = h9304.load_nsmc(a.nsmc)
    log(f"[corpus] rows={len(rows)}")

    # ---- GATE: POSITIVE CONTROL (blocking; read BEFORE any natural stratum) -------------
    res["POS"] = pos_control(a.seed, a.k_perm)

    # ---- anchor: reproduce the H_9304 pooled bar with the same vocab --------------------
    items, ridx, sid = build_cells_rowidx(rows, a.min_occ)
    log(f"\n[cells] stems={len(sid)} items={len(items)} (min_occ={a.min_occ}, GLOBAL vocab)")
    pooled = stratum_earned(items, np.random.default_rng(9304), a.k_perm)
    log(f"[anchor] POOLED natural I={pooled['earned']:+.5f}  CI[{pooled['ci_lo']:+.5f},{pooled['ci_hi']:+.5f}]  "
        f"n_ho={pooled['n_heldout']}  (H_9304 read +0.00233)")
    res["pooled_anchor"] = pooled

    if not res["POS"]["fired"]:
        log("\n" + "=" * 70)
        log("POSITIVE CONTROL FAILED -> the stratified instrument cannot detect cancellation.")
        log("VERDICT: INVALID (not FAIL). A blind probe's silence proves nothing.")
        res["verdict"] = "INVALID - positive control (mixture) did not fire; strata NOT read"
        json.dump(res, open(os.path.join(a.out, "h9305_summary.json"), "w"), indent=2, ensure_ascii=False)
        sys.exit(0)

    # ---- EXP + CTRL1 over the 3 pre-registered schemes ----------------------------------
    lab_c = kmeans_strata(rows, a.k_clust, a.seed)
    log(f"\n[S_CLUST] sizes={np.bincount(lab_c, minlength=a.k_clust).tolist()}")
    res["S_CLUST"] = run_scheme("S_CLUST", items, ridx, lab_c, a.k_clust, a.seed, a.k_perm, pooled["earned"])

    lab_l, qs = length_strata(rows)
    log(f"\n[S_LEN] byte quartile cuts={qs.tolist()}  sizes={np.bincount(lab_l, minlength=4).tolist()}")
    res["S_LEN"] = run_scheme("S_LEN", items, ridx, lab_l, 4, a.seed, a.k_perm, pooled["earned"])

    res["S_MARKER"] = marker_arms(rows, a.min_occ, a.seed, a.k_perm)

    # ---- VERDICT (bars frozen in FREEZE.txt; not one byte moved) ------------------------
    all_strata = (res["S_CLUST"]["exp"] + res["S_LEN"]["exp"]
                  + [m["result"] for m in res["S_MARKER"] if m["result"]])
    ctrl_all = res["S_CLUST"]["ctrl1_random"] + res["S_LEN"]["ctrl1_random"]

    any_sig = [s for s in all_strata if s["significant"]]
    ctrl_dirty = [s for s in ctrl_all if abs(s["earned"]) > DELTA_EQ]
    unpowered = [s for s in all_strata if not s["powered"]]
    all_tost = all(s["tost_pass"] for s in all_strata)

    log("\n" + "=" * 70)
    log(f"strata read           : {len(all_strata)} / {N_TESTS} pre-registered")
    log(f"significant (|I|>bar) : {len(any_sig)}")
    log(f"CTRL1 random dirty    : {len(ctrl_dirty)}  (must be 0)")
    log(f"NOT-POWERED strata    : {len(unpowered)}  (MDE > {DELTA_EQ})")
    log(f"all strata TOST pass  : {all_tost}")
    log(f"POS fired             : {res['POS']['fired']}")
    for sc in ("S_CLUST", "S_LEN"):
        r = res[sc]
        log(f"D_exp({sc})={r['D_exp']['D']:+.5f}  vs D_ctrl1={r['D_ctrl1']['D']:+.5f}  "
            f"| paired-t mean_diff={r['paired_t_exp_vs_ctrl1']['mean_diff']:+.5f} "
            f"t={r['paired_t_exp_vs_ctrl1']['t']}")

    if ctrl_dirty:
        v = "INVALID - size-matched RANDOM strata produced |I| > delta_eq => stratified reads are a small-sample artifact"
    elif any_sig:
        v = ("PASS - >=1 stratum carries transferable interaction ABOVE its own permutation "
             "pedestal and the 0.02 floor => the pooled zero of H_9304 hid a stratified effect")
    elif unpowered:
        v = f"NOT-POWERED - {len(unpowered)} strata have MDE > {DELTA_EQ}; equivalence not licensed there"
    elif all_tost:
        v = ("FAIL - every stratum is TOST-equivalent to zero (+-0.02) while the mixture positive "
             "control fires => NO cancellation; H_9304 DATA-ADDITIVE is strengthened to stratum granularity")
    else:
        v = "INDETERMINATE - no stratum clears its bar but not all are TOST-equivalent either"

    log(f"\nVERDICT: {v}")
    res.update({"n_significant": len(any_sig), "n_ctrl1_dirty": len(ctrl_dirty),
                "n_unpowered": len(unpowered), "all_tost": bool(all_tost), "verdict": v,
                "wall_s": time.time() - t0})
    json.dump(res, open(os.path.join(a.out, "h9305_summary.json"), "w"), indent=2, ensure_ascii=False)
    log(f"wall={time.time()-t0:.1f}s\n[done]")


if __name__ == "__main__":
    main()
