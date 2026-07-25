#!/usr/bin/env python3
"""EARNED — the certified corpus-level operator instrument, wired into the engine CLI.

    anima-py evaluate --earned <corpus.tsv> [--out <f.json>] [--min-occ N] [--k-perm N] [--seeds a,b,c]
                                            [--null parametric|real|shuffle]

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
operator was PLANTED (+5.29653 nats).

MULTI-SEED IS THE DEFAULT, and that is a repair, not a nicety. The held-out cells are chosen by
sampling stems, so on a small corpus the SEED moves the effect size. Measured: on ArSarcasm
(~2.5-3k held-out cells) the irony point read 0.024% of the ruler at one seed and 0.061% at
another -- 2.5x -- and a single-seed number had already been written into a card as the fact
"irony is the smallest of the four points, at the very place theory says it should be largest".
It was seed noise; the ranking claim was retracted (H_9319). The equivalence claim survived
(both seeds sit far inside the TOST margin) -- what moved was the RANKING, not the EQUIVALENCE.
So: a ranking claim is much weaker than an equivalence claim, and this instrument no longer lets
you make one from a single draw. It runs `--seeds` (default 3), prints the per-seed spread, and
refuses to call any point "smaller/larger than" another whose interval it overlaps.
See ARCHITECTURE convergence `earned-instrument-wire-1`.

`--null real` — THE INPUT SWAP (H_9325 deepening, under the H_9854 ledger audit). Everything above is calibrated on the
SYNTHETIC arms of `synth()`: one stem per row, 200 stems of uniform frequency, rows i.i.d. A real
corpus row carries SEVERAL stems that all share ONE T, stem frequency is Zipf, and B co-occurs with
the very stems that mark it. `--null real` regenerates the null world AND both control arms under
that real covariance instead of the toy's, changing NOTHING else -- same estimand, same bars
(G_ALIVE_BAR, DELTA_EQ), same decision rule, same seed policy. On the synthetic arms the two nulls
coincide by construction (one item per row), so the swap is surgical: only the real corpus's own
structure enters.
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


_SCRIPT_PREFIX = {"arabic": 5, "latin": 4, "hangul": 3}
_FRAG_CODE = "abcdefghijklmnop"          # up to 16 fragmentation classes


def _frag_hash(w, text, seed):
    """DETERMINISTIC across runs (unlike Python's per-process-salted hash(str)). The class a token
    gets depends on the word AND the sentence it sits in, so ONE root lands in several classes across
    the corpus — mimicking one Korean root realised with several endings (H_9953 SPLIT-English)."""
    import hashlib
    h = hashlib.blake2b((w + "\x00" + text + "\x00" + str(seed)).encode("utf-8"), digest_size=8)
    return int.from_bytes(h.digest(), "big")


def _stems(text, script, prefix=None, frag_k=None, frag_seed=0):
    """Content-word stems. No lexicon and no polarity list -- alpha_A is FITTED, not looked up.

    Adding a script is a REGEX SWAP, and certification is inherited: G-ALIVE/G-PEDESTAL are synthetic
    arms built from integer symbol ids, so they never touch this function (H_9318 added Arabic this
    way). What a new script must NOT do is smuggle in a different notion of "stem" -- each branch
    truncates to a fixed prefix and keeps a mid-length band, so alpha_A stays a fitted coefficient
    over surface forms rather than a lexicon lookup.

    `prefix` (H_9953 MERGE) overrides the selected script's truncation length ONLY; the regex and
    length band are unchanged, so it is the same fixed-prefix rule with one integer freed (never a
    lexicon). `frag_k` (H_9953 SPLIT, latin only) inserts a class char INSIDE the key: base = first 3
    chars, 4th char = one of K deterministic classes ⇒ one English root is fragmented into K stems
    the way Korean inflection fragments one root. Both are echoed in the header/JSON so no number can
    be quoted without the manipulation visible; neither touches the synthetic gate arms."""
    if script == "arabic":
        n = prefix if prefix else 5
        return [w[:n] if len(w) > n else w
                for w in re.findall(r"[؀-ۿ]+", text) if 3 <= len(w) <= 12]
    if script == "latin":
        toks = [w for w in re.findall(r"[A-Za-z]+", text.lower()) if 3 <= len(w) <= 12]
        if frag_k:
            # base3 + class char. K=1 = constant 4th char = a pedestal that isolates fragmentation
            # (K>1) from the 4->3 root-channel narrowing (both differ from the untouched prefix-4).
            return [w[:3] + _FRAG_CODE[_frag_hash(w, text, frag_seed) % frag_k] for w in toks]
        n = prefix if prefix else 4
        return [w[:n] if len(w) > n else w for w in toks]
    n = prefix if prefix else 3
    return [w[:n] if len(w) > n else w
            for w in re.findall(r"[가-힣]+", text) if 2 <= len(w) <= 6]


def _detect_script(rows):
    """Pick the extractor by majority script. A corpus in a script with NO extractor used to fall
    through to hangul and silently read 0 stems -- which the G-POWER guard now reports as
    INVALID (DATA-SPARSE) rather than crashing (H_9677)."""
    head = rows[:500]
    ar = sum(1 for t, _, _ in head if re.search(r"[؀-ۿ]", t))
    if ar > len(head) // 2:
        return "arabic"
    ko = sum(1 for t, _, _ in head if re.search(r"[가-힣]", t))
    if ko > len(head) // 2:
        return "hangul"
    la = sum(1 for t, _, _ in head if re.search(r"[A-Za-z]", t))
    return "latin" if la > len(head) // 2 else "hangul"


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


def build_cells(rows, min_occ, script, with_rows=False, prefix=None, frag_k=None, frag_seed=0):
    """Explode corpus ROWS into (stem, B, T) items.

    with_rows=True also returns, per item, the index of the SOURCE ROW it came from. That index is
    the real corpus's covariance structure made explicit: one row contributes as many items as it
    has kept stems, and every one of them carries THE SAME T. The synthetic control arms have no
    such structure (one row = one item), which is exactly why a null calibrated on them can be
    mis-calibrated here (`--null real`)."""
    from collections import Counter
    cnt = Counter()
    for text, _b, _t in rows:
        for s in set(_stems(text, script, prefix, frag_k, frag_seed)):
            cnt[s] += 1
    keep = {s for s, c in cnt.items() if c >= min_occ}
    sid = {s: i for i, s in enumerate(sorted(keep))}
    items = []
    ridx = []
    for ri, (text, b, t) in enumerate(rows):
        for s in set(_stems(text, script, prefix, frag_k, frag_seed)):
            if s in keep:
                items.append((sid[s], b, t))
                ridx.append(ri)
    # Shape the empty case explicitly. A corpus the stem extractor cannot read at all (wrong script,
    # or every stem below min_occ) yields NO rows, and `np.asarray([])` is 1-D -- which used to make
    # the DATA-SPARSE guard below unreachable: make_heldout crashed on items[:, 0] first. A crash is
    # not a verdict, and "the instrument threw" reads as an infra hiccup rather than what it is --
    # the corpus cannot pose the question (H_9677).
    if not items:
        empty = np.zeros((0, 3), dtype=np.int64)
        return (empty, sid, np.zeros(0, dtype=np.int64)) if with_rows else (empty, sid)
    it = np.asarray(items, dtype=np.int64)
    if with_rows:
        return it, sid, np.asarray(ridx, dtype=np.int64)
    return it, sid


def _ce(z, t):
    p = np.clip(1.0 / (1.0 + np.exp(-np.clip(z, -12, 12))), 1e-9, 1 - 1e-9)
    return float(-(t * np.log(p) + (1 - t) * np.log(1 - p)).mean())


def _phi(x, kappa, c):
    """R1's fixed relational nonlinearity: a saturating map with its LINEAR component projected out.

    Why saturation. In an ORDER task ("is a > b?") the marginals already carry the value: P(T=1|A=a)
    rises monotonically with rank(a), and gamma_B falls with rank(b). So alpha_A and gamma_B hand the
    additive model the value information FOR FREE. The true log-odds, though, is a STEP in the value
    difference, while the additive model can only draw a gentle slope. The non-additive information
    lives exactly in that SATURATION -- and one fixed nonlinearity captures it.

    Why the projection. delta * (alpha + gamma) is collinear with the additive term (it is just a
    rescaling), so without removing the linear part the fit reads held-out CALIBRATION error as if it
    were interaction. c = Cov(tanh(kappa*x), x)/Var(x) is computed on TRAIN and subtracted, which
    makes phi orthogonal to the additive direction by construction. kappa is frozen at calibration --
    it is not a free parameter, and R1 therefore carries the SAME degrees of freedom as R0 (one global
    scalar). That is what makes the relational move safe: a richer operator with no extra capacity to
    hallucinate a held-out gain."""
    t = np.tanh(kappa * x)
    return t - c * x


def _phi_c(x, kappa):
    v = float(np.var(x))
    if v <= 1e-12:
        return 0.0
    return float(np.cov(np.tanh(kappa * x), x, bias=True)[0, 1] / v)


def fit_and_score(items, heldout, b_vec=None, kernel="r0", kappa=1.0):
    """Fit alpha_A / gamma_B / delta on TRAIN; score the held-out cells under the additive model
    (delta = 0) and under the fitted-operator model. delta is FITTED, never assumed.

    kernel="r0" (default) = gating / sign-flip:   z = alpha + gamma + delta * (B * alpha)
        the XOR-class operator (negation, concession, irony). One global scalar.
    kernel="r1"           = threshold / order:    z = alpha + gamma + delta * phi(alpha + gamma)
        ONE global scalar (see _phi). MEASURED TO BE BLIND on a planted order truth (G-ALIVE +0.067
        at best across kappa in {0.3,1,3,10}, bar +0.30). The reason is structural, not a tuning
        miss: R1 is a nonlinearity of the SUM alpha+gamma, while an order truth is 1[val_A > val_B],
        a function of the DIFFERENCE -- and when B is a binary context bit, gamma_B carries only two
        levels and cannot transport val_B at all. No monotone map of the sum can recover it. This is
        exactly the pre-registered escalation condition for R2.

    kernel="r2"           = general order:        z = alpha + gamma + delta * tanh(u_A - v_B)
        Learns a per-symbol scalar u_A and v_B, so the DIFFERENCE is representable. This BUYS
        DEGREES OF FREEDOM (|A| + |B| extra), which is precisely the danger: extra capacity can
        hallucinate a held-out gain. It is therefore gated by G-DOF -- (a) on an ADDITIVE-truth world
        the full-DOF |EARNED| must still be <= delta_eq (the added capacity must not invent signal),
        and (b) where R1 already suffices, R2 must not beat it by more than delta_eq (otherwise the
        extra freedom is not earning its keep and we demote to R1). A saturated per-cell interaction
        table delta_AB is FORBIDDEN: it is undefined on unseen cells, silently collapses to additive,
        and thus manufactures a fake null."""
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

    def _basis(a, b, idxA=None, bb=None):
        """The operator's interaction basis -- the ONLY thing the kernels differ in."""
        gam = np.where(b == 1, g1, g0)
        if kernel == "r1":
            return _phi(a + gam, kappa, cst), gam
        if kernel == "r2":
            return np.tanh(uA[idxA] - vB[bb]), gam
        return b * a, gam

    cst = 0.0
    uA = vB = None
    blk = None
    if kernel == "r0b":
        # H_9972 — the FROZEN two-block gate. delta is allowed to differ between two stem blocks, and
        # the block label is a PRE-REGISTERED covariate, not a fitted per-cell table:
        #     C_A = 1[ |alpha_A| > median(|alpha|) ]      "evaluative" vs "neutral"
        # Why this is legal on an UNSEEN cell -- the thing that kills the forbidden delta_AB table:
        # alpha_A is fitted from the stem's B=0 TRAIN rows, and make_heldout holds out only B=1 rows
        # of stems that ALSO have B=0 rows. So every held-out stem already has a block label before
        # its B=1 cell is scored; nothing about the held-out cell is used to build it.
        # Cost: +1 DOF (two scalars instead of one) -- caught by G-PEDESTAL/G-DOF run through THIS
        # kernel on an additive-truth world. The covariate must be frozen BEFORE any natural read
        # (burned-gate law); |alpha| median split is the pre-registered choice and is not tuned.
        med = float(np.median(np.abs(alpha)))
        blk = (np.abs(alpha) > med).astype(np.int64)
    if kernel == "r1":
        z_tr_all = alpha[A[tr]] + np.where(B[tr] == 1, g1, g0)
        cst = _phi_c(z_tr_all, kappa)
    elif kernel == "r2":
        # Per-symbol latent scalars, estimated ONLY from TRAIN. u_A from the stem's own rows, v_B
        # from the context bit's rows. The held-out cell is never touched -- the transfer question
        # survives: u and v are learned from DIFFERENT pairings and composed on an unseen (A,B).
        nB = int(B.max()) + 1
        uA = np.zeros(nA); vB = np.zeros(nB)
        cA = np.zeros(nA); cB = np.zeros(nB)
        np.add.at(uA, A[tr], T[tr]); np.add.at(cA, A[tr], 1.0)
        np.add.at(vB, B[tr], T[tr]); np.add.at(cB, B[tr], 1.0)
        uA = (uA + eps) / (cA + 2 * eps); vB = (vB + eps) / (cB + 2 * eps)
        uA = np.log(uA / (1 - uA)); vB = np.log(vB / (1 - vB))

    trn = tr
    a_t, b_t, t_t = alpha[A[trn]], B[trn], T[trn]
    bas_t, gam_t = _basis(a_t, b_t, A[trn], B[trn])
    grid = np.linspace(-3.0, 3.0, 121)
    d_blk = None
    if kernel == "r0b":
        # Two deltas, one per FROZEN block. The blocks partition the rows, so the CE is separable and
        # each delta is a plain 1-D grid fit on its own rows -- +1 DOF total, not a per-cell table.
        d_blk = np.zeros(2)
        for c in (0, 1):
            m = blk[A[trn]] == c
            d_blk[c] = float(grid[int(np.argmin([_ce(a_t[m] + gam_t[m] + d * bas_t[m], t_t[m])
                                                 for d in grid]))]) if m.sum() > 0 else 0.0
        delta = float(np.mean(d_blk))          # a display summary only; scoring uses both
    else:
        delta = float(grid[int(np.argmin([_ce(a_t + gam_t + d * bas_t, t_t) for d in grid]))]) \
            if trn.sum() > 0 else 0.0

    a_ho, b_ho, t_ho = alpha[A[heldout]], B[heldout], T[heldout]
    bas_ho, gam_ho = _basis(a_ho, b_ho, A[heldout], B[heldout])
    dv = d_blk[blk[A[heldout]]] if kernel == "r0b" else delta
    return _ce(a_ho + gam_ho, t_ho), _ce(a_ho + gam_ho + dv * bas_ho, t_ho), delta


def _stratified_shuffle_B(B, T, rng):
    """THE CONTROL. Permute B only WITHIN strata of T: P(B,T) is preserved exactly (so the B->T
    channel survives) and only the A-B pairing -- i.e. only the synergy -- is destroyed. A plain
    permutation also kills B->T and made a zero-truth corpus read -0.618 nats."""
    bs = B.copy()
    for t in np.unique(T):
        idx = np.flatnonzero(T == t)
        bs[idx] = rng.permutation(B[idx])
    return bs



def _fit_additive(A, B, T, tr):
    """alpha_A (from the B=0 TRAIN rows) + gamma_B. The additive world, and nothing else."""
    nA = int(A.max()) + 1
    eps = 1.0
    pos = np.zeros(nA); tot = np.zeros(nA)
    m = tr & (B == 0)
    np.add.at(pos, A[m], T[m].astype(np.float64)); np.add.at(tot, A[m], 1.0)
    pA = (pos + eps) / (tot + 2 * eps)
    alpha = np.log(pA / (1 - pA))

    def _g(sel):
        if sel.sum() == 0:
            return 0.0
        p = (T[sel].sum() + eps) / (sel.sum() + 2 * eps)
        return float(np.log(p / (1 - p)))
    base = _g(tr)
    return alpha, _g(tr & (B == 0)) - base, _g(tr & (B == 1)) - base


def _row_mean(x, rowidx, nrow):
    s = np.zeros(nrow); c = np.zeros(nrow)
    np.add.at(s, rowidx, x); np.add.at(c, rowidx, 1.0)
    return s / np.maximum(c, 1.0)


def real_design_arm(items, rowidx, rng, mode):
    """A CONTROL ARM REBUILT ON THE REAL DESIGN — the input swap, not a new bar.

    `synth()` plants the answer into a TOY design: one stem per row, 200 stems of uniform frequency,
    rows i.i.d. On a real corpus the design is nothing like that — a row carries several stems that
    all share ONE T (row clustering), stem frequency is Zipf, alpha is estimated from as few as
    min_occ rows, and B co-occurs with the very stems that mark it. So a null/pedestal certified on
    `synth()` is certified on a covariance the real corpus does not have.

    This function keeps the REAL (A, B, row) design byte-for-byte and only regenerates T:
        mode="additive" -> T drawn per ROW from the fitted additive model  => truth interaction is
                           EXACTLY ZERO, on the real covariance. This is G-PEDESTAL's question asked
                           of real input.
        mode="xor"      -> T = (row's MAJORITY stem polarity) XOR B, set per ROW => a planted operator
                           living in the real design. This is G-ALIVE's question asked of real input.
                           The row aggregation is the MEAN over the row's stems, the same aggregation
                           the pedestal arm uses on z -- a real row has several stems and the planting
                           must let all of them carry the operator, exactly as the instrument's own
                           model (z = alpha_A + gamma_B + delta*B*alpha_A) assumes each of them does.
    The bars they are read against (G_ALIVE_BAR, DELTA_EQ) are untouched."""
    A, B, T = items[:, 0], items[:, 1], items[:, 2]
    nrow = int(rowidx.max()) + 1
    _, first = np.unique(rowidx, return_index=True)
    if mode == "xor":
        pol = rng.integers(0, 2, size=int(A.max()) + 1)
        pol_row = _row_mean(pol[A].astype(np.float64), rowidx, nrow) > 0.5
        b_row = np.zeros(nrow, dtype=np.int64)
        b_row[rowidx[first]] = B[first]
        t_row = (pol_row.astype(np.int64) ^ b_row)
    else:
        alpha, g0, g1 = _fit_additive(A, B, T.astype(np.float64), np.ones(len(A), dtype=bool))
        z = alpha[A] + np.where(B == 1, g1, g0)
        zr = _row_mean(z, rowidx, nrow)
        p = np.clip(1.0 / (1.0 + np.exp(-np.clip(zr, -12, 12))), 1e-9, 1 - 1e-9)
        t_row = (rng.random(nrow) < p).astype(np.int64)
    out = items.copy()
    out[:, 2] = t_row[rowidx]
    return out


def _parametric_null(items, heldout, rng, rowidx=None):
    """THE NULL. Resample T from the FITTED ADDITIVE MODEL (alpha + gamma): interaction is exactly
    zero in the null world, while the marginal prediction structure is kept intact.

    Why the shuffle null is wrong. Permuting B destroys the A-B pairing but ALSO the A-marginal
    geometry the fit sees. So when alpha_A is noise -- stems carrying no real latent polarity -- the
    OBSERVED arm suffers a pathology (a delta fitted on garbage alpha makes held-out WORSE) that the
    shuffle null does not reproduce, and the difference leaks straight into EARNED. Measured: on a
    formal-symbolic corpus whose stems were T-irrelevant, shuffle-nulled EARNED came back at -1.000
    nats -- a SIGN FLIP, i.e. an artifact, not a finding (H_9323). A parametric null regenerates T
    from alpha-hat + gamma-hat over the SAME stems, so both arms carry the pathology and it cancels.

    This null is strictly harder to beat, and that is the point: it grants the additive model
    everything it can explain and asks only whether anything is left over.

    rowidx is not None (`--null real`) = THE INPUT SWAP. The draw is made once per SOURCE ROW and
    broadcast to every item that row produced, so the null world carries the real corpus's row
    clustering instead of the toy's independent items. Interaction is still exactly zero — only the
    covariance the null is generated under changes. Independent per-item draws under-disperse a
    clustered corpus, which shrinks sd_null (and therefore G-POWER's MDE) and shifts the null mean
    that EARNED subtracts; that is the same family of defect that killed H_9838/H_9839, where a null
    fitted to planted (near-orthogonal) geometry did not survive real (near-collinear) input."""
    A, B, T = items[:, 0], items[:, 1], items[:, 2]
    tr = ~heldout
    alpha, g0, g1 = _fit_additive(A, B, T, tr)

    z = alpha[A] + np.where(B == 1, g1, g0)      # additive world; interaction exactly 0
    if rowidx is None:
        p = np.clip(1.0 / (1.0 + np.exp(-np.clip(z, -12, 12))), 1e-9, 1 - 1e-9)
        return (rng.random(len(T)) < p).astype(np.int64)
    nrow = int(rowidx.max()) + 1
    zr = _row_mean(z, rowidx, nrow)
    pr = np.clip(1.0 / (1.0 + np.exp(-np.clip(zr, -12, 12))), 1e-9, 1 - 1e-9)
    return (rng.random(nrow) < pr).astype(np.int64)[rowidx]


def earned(items, heldout, rng, k_perm, null="parametric", kernel="r0", kappa=1.0, rowidx=None):
    """EARNED = observed (CE_add - CE_op) minus the null-world mean of the same quantity.

    null="parametric" (DEFAULT) = additive parametric bootstrap (see _parametric_null): every
    marginal pathology survives in BOTH arms and cancels.
    null="real" = the SAME parametric bootstrap regenerated under the REAL corpus's row clustering
    (rowidx from build_cells(..., with_rows=True)). Input swap only: same estimand, same bars.
    null="shuffle" = the legacy T-stratified permutation, kept ONLY to reproduce the already-shipped
    H_9304/9316/9317/9318 numbers byte-for-byte (reference-match)."""
    ce_a, ce_o, delta = fit_and_score(items, heldout, kernel=kernel, kappa=kappa)
    obs = ce_a - ce_o
    B, T = items[:, 1], items[:, 2]
    ri = rowidx if null == "real" else None
    vals = []
    for _ in range(k_perm):
        if null == "shuffle":
            r = fit_and_score(items, heldout, b_vec=_stratified_shuffle_B(B, T, rng), kernel=kernel, kappa=kappa)
        else:
            it2 = items.copy()
            it2[:, 2] = _parametric_null(items, heldout, rng, ri)
            r = fit_and_score(it2, heldout, kernel=kernel, kappa=kappa)
        vals.append(r[0] - r[1])
    nullv = np.asarray(vals)
    return obs - nullv.mean(), float(nullv.mean()), float(nullv.std(ddof=1)), nullv, delta


def make_heldout(items, rng, frac=0.30):
    A, B = items[:, 0], items[:, 1]
    both = np.intersect1d(np.unique(A[B == 1]), np.unique(A[B == 0]))
    if len(both) == 0:
        return np.zeros(len(items), dtype=bool), 0
    pick = rng.choice(both, size=max(1, int(len(both) * frac)), replace=False)
    return np.isin(A, pick) & (B == 1), len(pick)


def synth(rng, n_stems, n_rows, mode):
    """The calibration arms. Their EARNED is NEVER a finding -- we planted the answer.

    'xor'      = planted GATING operator (truth = 1 bit)   -> G-ALIVE for kernel r0
    'order'    = planted ORDER operator (T = 1[a > b])     -> G-ALIVE for kernel r1
    'additive' = truth 0                                    -> G-PEDESTAL (both kernels)"""
    pol = rng.integers(0, 2, size=n_stems)
    A = rng.integers(0, n_stems, size=n_rows)
    B = rng.integers(0, 2, size=n_rows)
    if mode == "xor":
        T = pol[A] ^ B
    elif mode == "order":
        # T is decided by the RELATION between the two operands, not by any stem's polarity.
        val = rng.integers(10, 100, size=n_stems)          # each stem carries a hidden VALUE
        Bv = rng.integers(10, 100, size=n_rows)
        A = rng.integers(0, n_stems, size=n_rows)
        B = (Bv > 54).astype(np.int64)                     # the context bit: is the rhs "large"?
        T = (val[A] > Bv).astype(np.int64)
    else:
        p = np.clip(np.where(pol[A] == 1, 0.85, 0.15) + np.where(B == 1, -0.05, 0.05), 0.01, 0.99)
        T = (rng.random(n_rows) < p).astype(np.int64)
    return np.stack([A, B, T], axis=1)


def synth_hetero(rng, n_stems, n_rows, rho, a0=1.0, align=False):
    """H_9971 — a HETEROGENEOUS operator: only a fraction `rho` of stems flips polarity under B=1.

    Why a separate arm. Every kernel here commits to ONE global delta shared by all stems, so the
    worry is that flippers and non-flippers average out and a real operator reads as DATA-ADDITIVE.
    This arm MEASURES where that happens instead of arguing about it.

    Why the flip block is FROZEN and OBSERVABLE (`C_A`, deterministic sha256 over the stem id), not a
    hidden random subset: on a held-out (stem, B=1) cell a hidden membership is unlearnable by ANY
    estimator, so an arm built on one would certify nothing -- it would demand oracle knowledge that
    no covariate-free method can have. With an observable block the arm DISCRIMINATES: a covariate-
    aware estimator can pass it, a blind one cannot. The block is stratified within polarity so `C_A`
    is not confounded with `alpha_A`.

    truth:  logit P(T=1 | A,B) = a0 * s_A * (1 - 2 * B * C_A)      s_A = +-1 balanced polarity
    rho=1 reproduces the xor world (every stem flips) and rho=0 the pedestal (truth additive), which
    is the arm's own built-in self-check. Returns (items, C) -- C is what the oracle reference uses."""
    pol = rng.integers(0, 2, size=n_stems)
    A = rng.integers(0, n_stems, size=n_rows)
    B = rng.integers(0, 2, size=n_rows)
    s = np.where(pol == 1, 1.0, -1.0)
    C = np.zeros(n_stems, dtype=np.int64)
    if align:
        # ALIGNED variant — the flip block is the HIGH-polarity-strength half, so a frozen |alpha|
        # split CAN recover it. This is the MATCHED POSITIVE CONTROL for a covariate-aware kernel
        # (r0b): in the default variant C_A is orthogonal to alpha by construction, so NO frozen
        # covariate could ever find it and a covariate-aware kernel would fail there for a reason
        # that says nothing about the kernel. It is also the realistic story: evaluative words carry
        # strong polarity AND invert under negation; neutral words carry little and do not.
        strength = rng.uniform(0.3, 2.0, size=n_stems)
        k = int(round(rho * n_stems))
        if k:
            C[np.argsort(-strength)[:k]] = 1
        z = strength[A] * s[A] * (1.0 - 2.0 * B * C[A])
    else:
        h = [int(hashlib.sha256(("earned-hetero-v1|%d" % a).encode()).hexdigest()[:16], 16)
             for a in range(n_stems)]
        for p in (0, 1):
            idx = np.flatnonzero(pol == p)
            k = int(round(rho * len(idx)))
            if k:
                C[sorted(idx, key=lambda a: h[a])[:k]] = 1
        z = a0 * s[A] * (1.0 - 2.0 * B * C[A])
    T = (rng.random(n_rows) < 1.0 / (1.0 + np.exp(-z))).astype(np.int64)
    return np.stack([A, B, T], axis=1), C


def _hetero_oracle(sh, C, ho, rng, k_perm, null, kernel, kappa):
    """GENEROUS upper bound for an estimator that KNEW the frozen block: run the SAME machinery
    separately inside each block and average by held-out weight. Deliberately generous (it refits
    alpha/gamma per block, more freedom than a block-delta model would get) -- if even this cannot
    beat the blind reading, the heterogeneity worry is dead rather than merely unproven. It is a
    REFERENCE, never a shipped estimator, and it never touches a corpus verdict."""
    num = den = 0.0
    for c in (0, 1):
        m = C[sh[:, 0]] == c
        if not m.any() or not (ho & m).any():
            continue
        _, inv = np.unique(sh[m, 0], return_inverse=True)
        sub = np.stack([inv, sh[m, 1], sh[m, 2]], axis=1)
        w = float((ho & m).sum())
        num += w * earned(sub, ho[m], rng, k_perm, null, kernel, kappa)[0]
        den += w
    return num / den if den else float("nan")


def seen_synergy(items, rng, k_perm=200, null="parametric", rowidx=None):
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
    return earned(items, ho, rng, k_perm, null, rowidx=rowidx)[0], int(ho.sum())


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
    seeds_s = evaluate_strval(argv, "--seeds", "")
    seeds = [int(x) for x in seeds_s.split(",") if x.strip()] if seeds_s else [seed, seed + 1, seed + 2]
    # "shuffle" only to reproduce shipped numbers · "real" = the H_9854 input swap (see below)
    null = evaluate_strval(argv, "--null", "parametric")
    kernel = evaluate_strval(argv, "--kernel", "r0")       # r0 = gating/sign-flip · r1 = threshold/order
    kappa = float(evaluate_strval(argv, "--kappa", "1.0"))
    ci = CI_DEFAULT
    rng = np.random.default_rng(seed)

    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    rows = load_corpus(path)
    script = _detect_script(rows)

    # H_9953 stem-channel manipulations (engine-native flags · echoed everywhere · gates untouched).
    stem_prefix = evaluate_intval(argv, "--stem-prefix", 0) or None   # 0/absent = script default
    frag_k = evaluate_intval(argv, "--stem-fragment-k", 0) or None
    frag_seed = evaluate_intval(argv, "--stem-fragment-seed", 9953)
    if stem_prefix is not None:
        dflt = _SCRIPT_PREFIX.get(script, 3)
        if not (1 <= stem_prefix <= dflt):
            print("evaluate --earned --stem-prefix: N must be 1..%d for script=%s (default %d); "
                  "widening past the default is not a merge." % (dflt, script, dflt), file=sys.stderr)
            return 2
    if frag_k is not None:
        if script != "latin":
            print("evaluate --earned --stem-fragment-k: latin script only (it splits an English "
                  "root into K classes); script=%s." % script, file=sys.stderr)
            return 2
        if not (1 <= frag_k <= len(_FRAG_CODE)):
            print("evaluate --earned --stem-fragment-k: K must be 1..%d." % len(_FRAG_CODE),
                  file=sys.stderr)
            return 2

    res = {"corpus": path, "corpus_sha256": sha, "rows": len(rows), "script": script,
           "stem_prefix": stem_prefix, "stem_fragment_k": frag_k,
           "stem_fragment_seed": frag_seed if frag_k else None,
           "delta_eq": DELTA_EQ, "xbind_ruler": XBIND_RULER, "seed": seed, "null": null,
           "control_design": "real" if null == "real" else "synthetic",
           "kernel": kernel, "kappa": kappa}

    print("=== anima evaluate --earned — corpus-level operator instrument (engine-native) ===")
    _kdesc = {"r0": "  (gating / sign-flip — the XOR class: negation·concession·irony · 1 global scalar)",
              "r1": "  (threshold / order on the SUM — 1 global scalar · MEASURED BLIND on order truth)",
              "r2": "  (general order on the DIFFERENCE — buys |A|+|B| DOF ⇒ G-DOF gate is mandatory)",
              "r0b": "  (FROZEN two-block gate: delta differs across |alpha| median split — +1 DOF ⇒ G-DOF mandatory)"}
    print("kernel: " + kernel + _kdesc.get(kernel, ""))
    _ndesc = {"parametric": "  (additive parametric bootstrap — the marginal pathology cancels in both arms)",
              "real": "  (REAL-INPUT swap: the null AND both control arms are regenerated under the "
                      "corpus's own row clustering — same bars, same decision rule · H_9325)",
              "shuffle": "  ⚠️ LEGACY shuffle null — reference-match only; it leaks a marginal "
                         "pathology into EARNED (H_9323)"}
    print("null:   " + null + _ndesc.get(null, ""))
    print("corpus: " + path + "  sha=" + sha[:16] + "…  rows=" + str(len(rows)) +
          "  script=" + script)
    print("        B-rate=%.3f   (B and T are corpus labels; T is OUTSIDE the token stream)"
          % float(np.mean([b for _, b, _ in rows])))
    if stem_prefix is not None or frag_k is not None:
        _sp = ("stem-prefix=%d (default %d)" % (stem_prefix, _SCRIPT_PREFIX.get(script, 3))
               if stem_prefix is not None else "stem-prefix=default")
        _fk = (" · fragment-K=%d seed=%d (English root split into K classes)" % (frag_k, frag_seed)
               if frag_k is not None else "")
        print("        ⚙ STEM-CHANNEL MANIPULATION (H_9953): %s%s — DIRECTIONAL, not the shipped run"
              % (_sp, _fk))
    print("")

    # ---- the item table. Built HERE (no rng touched) because `--null real` regenerates the two
    #      control arms on this same real design; `--null parametric|shuffle` never reads it early.
    items, sid, rowidx = build_cells(rows, min_occ, script, with_rows=True, prefix=stem_prefix, frag_k=frag_k, frag_seed=frag_seed)
    if null == "real":
        if kernel != "r0":
            print("--null real is defined for kernel r0 only (the real-design positive control plants "
                  "a GATING operator); rerun with --kernel r0.", file=sys.stderr)
            return 2
        if len(sid) == 0 or len(items) == 0:
            print("G-POWER     stems = 0  →  INVALID (DATA-SPARSE) — NOT a KILL")
            res["stems"] = 0
            res["verdict"] = ("INVALID (DATA-SPARSE) — stem extractor read 0 stems (script=%s); "
                              "the operator question cannot be posed on this corpus" % script)
            _emit(res, out)
            return 0

    # ---- G-ALIVE (positive control) — a blind instrument proves nothing -------------------
    # The positive control must plant the operator class the KERNEL claims to express -- certifying
    # an order kernel on an XOR truth proves nothing about order.
    alive_mode = "order" if kernel in ("r1", "r2") else "xor"
    _real = null == "real"
    _dsg = "REAL-design" if _real else "synthetic"
    sx = real_design_arm(items, rowidx, rng, alive_mode) if _real else synth(rng, 200, 60000, alive_mode)
    ho_x, _ = make_heldout(sx, rng)
    e_x, _, _, _, d_x = earned(sx, ho_x, rng, min(200, k_perm), null, kernel, kappa,
                               rowidx if _real else None)
    alive = e_x >= G_ALIVE_BAR
    print("G-ALIVE     %s %-8s (planted operator)  EARNED=%+.5f  delta=%+.2f  bar>=+%.2f  %s"
          % (_dsg, alive_mode.upper(), e_x, d_x, G_ALIVE_BAR,
             "PASS" if alive else "FAIL — THE INSTRUMENT IS BLIND on this operator class"))

    # ---- G-PEDESTAL (zero-truth) — this is what caught two estimand defects ---------------
    sa = real_design_arm(items, rowidx, rng, "additive") if _real else synth(rng, 200, 60000, "additive")
    ho_a, _ = make_heldout(sa, rng)
    e_a, _, _, _, d_a = earned(sa, ho_a, rng, min(200, k_perm), null, kernel, kappa,
                               rowidx if _real else None)
    ped = abs(e_a) <= DELTA_EQ
    print("G-PEDESTAL  %s ADDITIVE (truth = 0)     EARNED=%+.5f  delta=%+.2f   |.|<=%.2f   %s"
          % (_dsg, e_a, d_a, DELTA_EQ, "PASS" if ped else "FAIL — THE INSTRUMENT IS BIASED"))

    # ---- G-DOF (r2 only) — does the EXTRA CAPACITY hallucinate a held-out gain? ---------------
    # r2 buys |A|+|B| degrees of freedom. That is the whole danger of going relational: a richer
    # operator can fit noise on the held-out cells and read it back as "interaction". So we run the
    # ADDITIVE-TRUTH world (interaction genuinely zero) through the FULL-DOF kernel and demand it
    # still reads zero. A failure here means the operator invents signal, and no main bar may be read.
    dof_ok = True
    if kernel in ("r2", "r0b"):
        dof_ok = abs(e_a) <= DELTA_EQ    # e_a was measured with THIS kernel (full DOF) already
        print("G-DOF       additive world through FULL-DOF %-3s |EARNED|=%.5f <= %.2f   %s"
              % (kernel, abs(e_a), DELTA_EQ,
                 "PASS — the added capacity does not invent signal"
                 if dof_ok else "FAIL — r2 hallucinates a held-out gain; demote to r1"))
        res["G_DOF"] = {"earned_additive_full_dof": e_a, "pass": bool(dof_ok)}

    # ---- G-HET (H_9971 · opt-in SCOPE PROBE, never a gate) --------------------------------
    # Every kernel commits to ONE global delta, so a real operator that fires on only SOME stems
    # could average out and read as DATA-ADDITIVE. This measures where that actually happens
    # instead of arguing it. It moves NO frozen bar and cannot change a corpus verdict -- what it
    # produces is the SCOPE SENTENCE a landed DATA-ADDITIVE verdict must carry.
    het_spec = evaluate_strval(argv, "--calib-hetero", "")
    if het_spec:
        a0 = float(evaluate_strval(argv, "--calib-a0", "1.0"))
        halign = "--calib-hetero-align" in argv
        print("")
        print("G-HET       HETEROGENEOUS operator — only a fraction rho of stems flips under B=1"
              "  (a0=%.2f · kernel %s%s)" % (a0, kernel, " · ALIGNED to |alpha|" if halign else ""))
        print("            SCOPE PROBE, NOT A GATE. blind = what the shipped covariate-free estimator")
        print("            reads · oracle = generous UPPER BOUND for one that KNEW the frozen block.")
        het_rows = []
        for r in [float(x) for x in het_spec.split(",") if x.strip()]:
            sh, Cb = synth_hetero(rng, 200, 60000, r, a0, halign)
            ho_h, _ = make_heldout(sh, rng)
            e_b, _, _, _, d_h = earned(sh, ho_h, rng, min(200, k_perm), null, kernel, kappa)
            e_o = _hetero_oracle(sh, Cb, ho_h, rng, min(200, k_perm), null, kernel, kappa)
            blindspot = abs(e_b) <= DELTA_EQ and e_o > DELTA_EQ
            het_rows.append({"rho": r, "blind": e_b, "oracle": e_o, "delta": d_h,
                             "blindspot": bool(blindspot)})
            print("  rho=%.2f    blind=%+.5f (delta=%+.2f)   oracle=%+.5f   gap=%+.5f   %s"
                  % (r, e_b, d_h, e_o, e_o - e_b,
                     "BLIND — a real transferable operator sits under the %.2f margin" % DELTA_EQ
                     if blindspot else "seen"))
        res["G_HET"] = {"a0": a0, "kernel": kernel, "aligned": bool(halign), "rows": het_rows,
                        "note": "scope probe, not a gate; oracle is a generous reference, not a shipped arm"}

    # ---- G-POWER (census + null sd, measured BEFORE the effect is read) -------------------
    res["stems"] = len(sid)
    if len(sid) == 0:
        print("G-POWER     stems = 0  →  INVALID (DATA-SPARSE) — NOT a KILL")
        print("            The stem extractor read NOTHING from this corpus (script=%s, min-occ=%d)."
              % (script, min_occ))
        print("            There is no A axis, so the operator question cannot be POSED here —")
        print("            this is instrument/corpus misfit, not evidence of an additive corpus.")
        res["verdict"] = ("INVALID (DATA-SPARSE) — stem extractor read 0 stems (script=%s); "
                          "the operator question cannot be posed on this corpus" % script)
        _emit(res, out)
        return 0
    ho0, _ = make_heldout(items, np.random.default_rng(seeds[0]))
    if int(ho0.sum()) == 0:
        print("G-POWER     held-out cells = 0  →  INVALID (DATA-SPARSE) — NOT a KILL")
        res["verdict"] = "INVALID (DATA-SPARSE) — no held-out recombination cells exist"
        _emit(res, out)
        return 0

    # The held-out cells are RESAMPLED per seed: this is exactly the axis that moved the irony
    # point by 2.5x, so it is the axis the report has to expose rather than hide behind one draw.
    per = []
    for sd_i in seeds:
        ho_i, nst_i = make_heldout(items, np.random.default_rng(sd_i))
        e_i, nm_i, sdn_i, null_i, d_i = earned(items, ho_i, np.random.default_rng(sd_i), k_perm,
                                               null, kernel, kappa, rowidx)
        per.append({"seed": sd_i, "earned": e_i, "delta": d_i, "cells": int(ho_i.sum()),
                    "sd_null": sdn_i, "null_mean": nm_i, "null": null_i})
    e_vals = np.asarray([p["earned"] for p in per])
    e_n = float(e_vals.mean())
    spread = float(e_vals.max() - e_vals.min())
    ho, nst = make_heldout(items, np.random.default_rng(seeds[0]))
    null_mode = null      # `null` is rebound to the null DISTRIBUTION on the next line (pre-existing)
    nm, sd, null, d_n = per[0]["null_mean"], per[0]["sd_null"], per[0]["null"], per[0]["delta"]
    res["heldout_cells"] = int(ho.sum())
    mde = 3 * sd
    powered = mde <= DELTA_EQ
    print("G-POWER     held-out cells=%d (stems %d)  sd_null=%.5f  MDE(3σ)=%.5f  need<=%.2f  %s"
          % (int(ho.sum()), nst, sd, mde, DELTA_EQ,
             "PASS" if powered else "FAIL — NOT POWERED for a negative verdict"))
    print("")
    print("SEEDS       " + " · ".join("%d:%+.5f (%.3f%%)" % (p["seed"], p["earned"],
                                      100 * p["earned"] / XBIND_RULER) for p in per))
    print("            spread across seeds = %.5f nats (%.3f%% of the ruler)   "
          "%s" % (spread, 100 * spread / XBIND_RULER,
                  "— a single-seed number here would be NOISE" if spread > 0.5 * abs(e_n)
                  else "— seed-stable"))
    res["per_seed"] = [{k: v for k, v in p.items() if k != "null"} for p in per]
    res["seed_spread"] = spread
    res["seed_unstable"] = bool(spread > 0.5 * abs(e_n))
    res["G_ALIVE"] = {"earned": e_x, "pass": bool(alive)}
    res["G_PEDESTAL"] = {"earned": e_a, "pass": bool(ped)}
    res["G_POWER"] = {"sd_null": sd, "mde_3sd": mde, "pass": bool(powered)}

    if not (alive and ped and dof_ok):
        print("")
        print("INSTRUMENT NOT CERTIFIED → MAIN BAR NOT READ (a dead probe's silence proves nothing).")
        res["verdict"] = "INVALID — instrument not certified (G-ALIVE/G-PEDESTAL/G-DOF); main bar NOT read"
        _emit(res, out)
        return 0

    # ---- MAIN BAR ------------------------------------------------------------------------
    lo, hi = np.percentile(null - nm, [(100 - ci) / 2, 100 - (100 - ci) / 2])
    ci_lo, ci_hi = e_n + lo, e_n + hi
    seen, n_seen = seen_synergy(items, np.random.default_rng(seed + 1), 200, null_mode, rowidx)
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
    if res.get("seed_unstable"):
        print("")
        print("⚠️  SEED-UNSTABLE: the spread across seeds is comparable to the effect itself.")
        print("    The EQUIVALENCE verdict below still holds (every seed sits inside the TOST")
        print("    margin), but do NOT rank this point against another — that is what got")
        print("    retracted in H_9319. A ranking claim needs the gap to exceed the seed spread.")
    print("")
    print("VERDICT: " + v)
    res.update({"heldout_earned": e_n, "seeds": seeds, "ci_lo": ci_lo, "ci_hi": ci_hi, "ci_pct": ci,
                "delta_hat": d_n, "effect_vs_xbind_ruler": e_n / XBIND_RULER,
                "seen_synergy": seen, "tost_pass": bool(tost), "info_present": bool(info),
                "verdict": v})
    _emit(res, out)
    return 0


def _emit(res, out):
    if out:
        json.dump(res, open(out, "w"), indent=2, ensure_ascii=False)
        print("→ " + out)
