#!/usr/bin/env python3
"""EARNED — the certified corpus-level operator instrument, wired into the engine CLI.

    anima-py evaluate --earned <corpus.tsv> [--out <file.json>] [--min-occ N] [--k-perm N] [--seed N]

WHAT IT MEASURES. Given a natural corpus whose rows carry (text, B, T) -- where B is a binary
context bit and T is an outcome label ANNOTATED OUTSIDE THE TOKEN STREAM -- it asks, with no model
and no training involved, whether the corpus statistics contain non-additive information that
TRANSFERS to a held-out recombination cell:

    A            = a content-word stem; its latent polarity is the FITTED coefficient alpha_A
    B            = the binary context bit supplied by the corpus (negation / concession / irony …)
    T            = the outcome label -- HUMAN annotation, outside the tokens
    held-out cell = (A, B=1) for stems that appear in TRAIN only with B=0
    operator     = one GLOBAL delta in  logit P(T=1|A,B) = alpha_A + gamma_B + delta*(B*alpha_A)
                   delta = 0  -> additive        delta = -2 -> full flip (XBIND's planted xor)

    EARNED = [CE_add - CE_op]_heldout,observed  -  [CE_add - CE_op]_heldout,shuffle

WHY T MUST BE OUTSIDE THE TOKENS. If A, B and T are all read off the same token stream, then
"trigram beats bigram-product" is true BY CONSTRUCTION -- a tautology, not an experiment. So this
instrument requires a LABELLED corpus; pure web/wiki cannot even pose the question.

TWO DEFECTS THIS INSTRUMENT ALREADY SURVIVED (both caught by the zero-truth pedestal, before any
main bar was read -- see ARCHITECTURE convergence `instrument-certification-1`):
  1. A plain permutation of B destroys the B->T channel as well as the A-B pairing, so a corpus
     with ZERO true synergy read -0.618 nats. Fix: permute B only WITHIN strata of T, which
     preserves P(B,T) exactly and destroys only the A-B pairing.
  2. Hard-coding the flip (delta = -2) BAKES A DIRECTIONAL HYPOTHESIS INTO THE ESTIMAND: on an
     additive corpus a flip is actively wrong, so EARNED read -0.704 instead of 0. Fix: FIT delta
     from the data. That is what centers EARNED at zero under "no synergy".

THREE BLOCKING GATES. The main bar is not even computed unless all three pass -- a dead probe's
silence proves nothing (this lane lost H_9265 and H_9303 exactly there):
    G-ALIVE     synthetic XOR corpus (planted operator)  -> EARNED must be >= +0.30 nats
    G-PEDESTAL  synthetic ADDITIVE corpus (truth = 0)    -> |EARNED| must be <= 0.02
    G-POWER     held-out census + permutation-null sd    -> MDE(3sigma) must be <= 0.02
                (failing G-POWER is INVALID/DATA-SPARSE -- never a KILL: a small n is not a
                 negative result)

REPORTING. p-values are NOT the verdict: with n in the tens of thousands a speck is significant.
The effect is reported against the XBIND RULER -- what this same instrument reads on a corpus whose
operator was PLANTED (+5.29653 nats). Measured points: negation 0.044% · concession 0.171% ·
parity 0.060% · irony 0.024% of the ruler.
"""
import hashlib
import json
import math
import re
import sys

import numpy as np

DELTA_EQ = 0.02          # equivalence margin (TOST), frozen pre-data
G_ALIVE_BAR = 0.30       # the positive control must clear this or the instrument is blind
XBIND_RULER = 5.29653    # what this instrument reads on the synthetic XOR (planted) corpus
K_PERM = 1000
CI_DEFAULT = 95.0


def _stems(text, script):
    """Content-word stems. No lexicon and no polarity list -- alpha_A is FITTED, not looked up."""
    if script == "arabic":
        return [w[:5] if len(w) > 5 else w
                for w in re.findall(r"[؀-ۿ]+", text) if 3 <= len(w) <= 12]
    return [w[:3] if len(w) > 3 else w
            for w in re.findall(r"[가-힣]+", text) if 2 <= len(w) <= 6]


def _detect_script(rows):
    ar = sum(1 for t, _, _ in rows[:500] if re.search(r"[؀-ۿ]", t))
    return "arabic" if ar > len(rows[:500]) // 2 else "hangul"


def load_corpus(path):
    """TSV: text <tab> B <tab> T (header row skipped). B and T are corpus-supplied labels."""
    rows = []
    with open(path, encoding="utf-8") as f:
        next(f, None)
        for line in f:
            p = line.rstrip("\n").split("\t")
            if len(p) != 3 or not p[0].strip():
                continue
            rows.append((p[0], int(p[1]), int(p[2])))
    return rows


def build_cells(rows, min_occ, script):
    from collections import Counter
    cnt = Counter()
    for text, _b, _t in rows:
        for s in set(_stems(text, script)):
            cnt[s] += 1
    keep = {s for s, c in cnt.items() if c >= min_occ}
    sid = {s: i for i, s in enumerate(sorted(keep))}
    items = []
    for text, b, t in rows:
        for s in set(_stems(text, script)):
            if s in keep:
                items.append((sid[s], b, t))
    return np.asarray(items, dtype=np.int64), sid


def _ce(z, t):
    p = np.clip(1.0 / (1.0 + np.exp(-np.clip(z, -12, 12))), 1e-9, 1 - 1e-9)
    return float(-(t * np.log(p) + (1 - t) * np.log(1 - p)).mean())


def fit_and_score(items, heldout, b_vec=None):
    """Fit alpha_A / gamma_B / delta on TRAIN; score the held-out cells under the additive model
    (delta = 0) and under the fitted-operator model. delta is FITTED, never assumed."""
    A = items[:, 0]
    B = items[:, 1] if b_vec is None else b_vec
    T = items[:, 2].astype(np.float64)
    tr = ~heldout
    nA = int(A.max()) + 1
    eps = 1.0

    pos = np.zeros(nA); tot = np.zeros(nA)
    m = tr & (B == 0)
    np.add.at(pos, A[m], T[m]); np.add.at(tot, A[m], 1.0)
    pA = (pos + eps) / (tot + 2 * eps)
    alpha = np.log(pA / (1 - pA))

    def _g(sel):
        if sel.sum() == 0:
            return 0.0
        p = (T[sel].sum() + eps) / (sel.sum() + 2 * eps)
        return float(np.log(p / (1 - p)))
    base = _g(tr)
    g0, g1 = _g(tr & (B == 0)) - base, _g(tr & (B == 1)) - base

    trn1 = tr & (B == 1)
    a_t1, t_t1 = alpha[A[trn1]], T[trn1]
    grid = np.linspace(-3.0, 3.0, 121)
    delta = float(grid[int(np.argmin([_ce(a_t1 + g1 + d * a_t1, t_t1) for d in grid]))]) \
        if trn1.sum() > 0 else 0.0

    a_ho, b_ho, t_ho = alpha[A[heldout]], B[heldout], T[heldout]
    gam = np.where(b_ho == 1, g1, g0)
    return _ce(a_ho + gam, t_ho), _ce(a_ho + gam + delta * (b_ho * a_ho), t_ho), delta


def _stratified_shuffle_B(B, T, rng):
    """THE CONTROL. Permute B only WITHIN strata of T: P(B,T) is preserved exactly (so the B->T
    channel survives) and only the A-B pairing -- i.e. only the synergy -- is destroyed. A plain
    permutation also kills B->T and made a zero-truth corpus read -0.618 nats."""
    bs = B.copy()
    for t in np.unique(T):
        idx = np.flatnonzero(T == t)
        bs[idx] = rng.permutation(B[idx])
    return bs


def earned(items, heldout, rng, k_perm):
    ce_a, ce_o, delta = fit_and_score(items, heldout)
    obs = ce_a - ce_o
    B, T = items[:, 1], items[:, 2]
    null = np.asarray([(lambda r: r[0] - r[1])(fit_and_score(items, heldout,
                       b_vec=_stratified_shuffle_B(B, T, rng))[:2]) for _ in range(k_perm)])
    return obs - null.mean(), float(null.mean()), float(null.std(ddof=1)), null, delta


def make_heldout(items, rng, frac=0.30):
    A, B = items[:, 0], items[:, 1]
    both = np.intersect1d(np.unique(A[B == 1]), np.unique(A[B == 0]))
    if len(both) == 0:
        return np.zeros(len(items), dtype=bool), 0
    pick = rng.choice(both, size=max(1, int(len(both) * frac)), replace=False)
    return np.isin(A, pick) & (B == 1), len(pick)


def synth(rng, n_stems, n_rows, mode):
    """mode 'xor' = planted operator (truth = 1 bit) · 'additive' = truth 0 (the pedestal)."""
    pol = rng.integers(0, 2, size=n_stems)
    A = rng.integers(0, n_stems, size=n_rows)
    B = rng.integers(0, 2, size=n_rows)
    if mode == "xor":
        T = pol[A] ^ B
    else:
        p = np.clip(np.where(pol[A] == 1, 0.85, 0.15) + np.where(B == 1, -0.05, 0.05), 0.01, 0.99)
        T = (rng.random(n_rows) < p).astype(np.int64)
    return np.stack([A, B, T], axis=1)


def seen_synergy(items, rng, k_perm=200):
    """Discriminates DATA-ADDITIVE (no non-additivity at all) from OPERATOR-ABSENT (it exists but
    never transfers). Holds out HALF of each stem's B=1 rows, so the fit HAS seen that stem
    negated -- the strictly weaker question."""
    A, B = items[:, 0], items[:, 1]
    ho = np.zeros(len(items), dtype=bool)
    for a in np.unique(A[B == 1]):
        idx = np.flatnonzero((A == a) & (B == 1))
        if len(idx) >= 2:
            ho[rng.choice(idx, size=len(idx) // 2, replace=False)] = True
    if ho.sum() == 0:
        return 0.0, 0
    return earned(items, ho, rng, k_perm)[0], int(ho.sum())


def earned_run(argv):
    """`anima-py evaluate --earned <corpus.tsv>` — the certified corpus-level operator instrument.

    Engine-native by `a_experiment_engine_native`: the manipulation lives in the canonical CLI, not
    in a side script standing next to it, so a passing result is ALREADY wired and the next corpus
    reuses it instead of re-implementing it."""
    from evaluate import evaluate_strval, evaluate_intval

    path = evaluate_strval(argv, "--earned", "")
    if not path:
        print("evaluate --earned: needs <corpus.tsv> (text<TAB>B<TAB>T, header row)", file=sys.stderr)
        return 2
    out = evaluate_strval(argv, "--out", "")
    min_occ = evaluate_intval(argv, "--min-occ", 100)
    k_perm = evaluate_intval(argv, "--k-perm", K_PERM)
    seed = evaluate_intval(argv, "--seed", 9304)
    ci = CI_DEFAULT
    rng = np.random.default_rng(seed)

    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    rows = load_corpus(path)
    script = _detect_script(rows)
    res = {"corpus": path, "corpus_sha256": sha, "rows": len(rows), "script": script,
           "delta_eq": DELTA_EQ, "xbind_ruler": XBIND_RULER, "seed": seed}

    print("=== anima evaluate --earned — corpus-level operator instrument (engine-native) ===")
    print("corpus: " + path + "  sha=" + sha[:16] + "…  rows=" + str(len(rows)) +
          "  script=" + script)
    print("        B-rate=%.3f   (B and T are corpus labels; T is OUTSIDE the token stream)"
          % float(np.mean([b for _, b, _ in rows])))
    print("")

    # ---- G-ALIVE (positive control) — a blind instrument proves nothing -------------------
    sx = synth(rng, 200, 60000, "xor")
    ho_x, _ = make_heldout(sx, rng)
    e_x, _, _, _, d_x = earned(sx, ho_x, rng, min(200, k_perm))
    alive = e_x >= G_ALIVE_BAR
    print("G-ALIVE     synthetic XOR (planted operator)   EARNED=%+.5f  delta=%+.2f   bar>=+%.2f  %s"
          % (e_x, d_x, G_ALIVE_BAR, "PASS" if alive else "FAIL — THE INSTRUMENT IS BLIND"))

    # ---- G-PEDESTAL (zero-truth) — this is what caught two estimand defects ---------------
    sa = synth(rng, 200, 60000, "additive")
    ho_a, _ = make_heldout(sa, rng)
    e_a, _, _, _, d_a = earned(sa, ho_a, rng, min(200, k_perm))
    ped = abs(e_a) <= DELTA_EQ
    print("G-PEDESTAL  synthetic ADDITIVE (truth = 0)     EARNED=%+.5f  delta=%+.2f   |.|<=%.2f   %s"
          % (e_a, d_a, DELTA_EQ, "PASS" if ped else "FAIL — THE INSTRUMENT IS BIASED"))

    # ---- G-POWER (census + null sd, measured BEFORE the effect is read) -------------------
    items, sid = build_cells(rows, min_occ, script)
    ho, nst = make_heldout(items, np.random.default_rng(seed))
    res["stems"] = len(sid); res["heldout_cells"] = int(ho.sum())
    if int(ho.sum()) == 0:
        print("G-POWER     held-out cells = 0  →  INVALID (DATA-SPARSE) — NOT a KILL")
        res["verdict"] = "INVALID (DATA-SPARSE) — no held-out recombination cells exist"
        _emit(res, out)
        return 0
    e_n, nm, sd, null, d_n = earned(items, ho, np.random.default_rng(seed), k_perm)
    mde = 3 * sd
    powered = mde <= DELTA_EQ
    print("G-POWER     held-out cells=%d (stems %d)  sd_null=%.5f  MDE(3σ)=%.5f  need<=%.2f  %s"
          % (int(ho.sum()), nst, sd, mde, DELTA_EQ,
             "PASS" if powered else "FAIL — NOT POWERED for a negative verdict"))
    res["G_ALIVE"] = {"earned": e_x, "pass": bool(alive)}
    res["G_PEDESTAL"] = {"earned": e_a, "pass": bool(ped)}
    res["G_POWER"] = {"sd_null": sd, "mde_3sd": mde, "pass": bool(powered)}

    if not (alive and ped):
        print("")
        print("INSTRUMENT NOT CERTIFIED → MAIN BAR NOT READ (a dead probe's silence proves nothing).")
        res["verdict"] = "INVALID — instrument not certified; main bar NOT read"
        _emit(res, out)
        return 0

    # ---- MAIN BAR ------------------------------------------------------------------------
    lo, hi = np.percentile(null - nm, [(100 - ci) / 2, 100 - (100 - ci) / 2])
    ci_lo, ci_hi = e_n + lo, e_n + hi
    seen, n_seen = seen_synergy(items, np.random.default_rng(seed + 1), 200)
    print("")
    print("held-out EARNED = %+.5f nats   %.1f%% CI [%+.5f, %+.5f]   delta=%+.2f  (0=additive, -2=flip)"
          % (e_n, ci, ci_lo, ci_hi, d_n))
    print("  vs the XBIND ruler: %.3f%% of a PLANTED operator   "
          "[p-values are NOT the verdict — with this n a speck is significant]"
          % (100 * e_n / XBIND_RULER))
    print("  seen synergy    = %+.5f nats (n=%d)   [DATA-ADDITIVE vs OPERATOR-ABSENT]"
          % (seen, n_seen))

    info = ci_lo > DELTA_EQ
    tost = (ci_lo > -DELTA_EQ) and (ci_hi < DELTA_EQ)
    if info:
        v = ("INFO-PRESENT — non-additive information EXISTS and TRANSFERS to held-out cells "
             "⇒ an estimator search is justified (necessary, NOT sufficient: recovering less than "
             "the wall's height still leaves the wall standing)")
    elif tost and not powered:
        v = "NOT-POWERED — equivalence claimed but MDE > delta_eq; need more labelled data"
    elif tost and seen > DELTA_EQ:
        v = ("OPERATOR-ABSENT — the non-additivity is ALL collocation: it exists but never transfers "
             "off the stem that carries it")
    elif tost:
        v = ("DATA-ADDITIVE — no transferable non-additive information at all ⇒ no estimator can "
             "ever bank it")
    else:
        v = "INDETERMINATE — CI straddles the equivalence margin"
    print("")
    print("VERDICT: " + v)
    res.update({"heldout_earned": e_n, "ci_lo": ci_lo, "ci_hi": ci_hi, "ci_pct": ci,
                "delta_hat": d_n, "effect_vs_xbind_ruler": e_n / XBIND_RULER,
                "seen_synergy": seen, "tost_pass": bool(tost), "info_present": bool(info),
                "verdict": v})
    _emit(res, out)
    return 0


def _emit(res, out):
    if out:
        json.dump(res, open(out, "w"), indent=2, ensure_ascii=False)
        print("→ " + out)
