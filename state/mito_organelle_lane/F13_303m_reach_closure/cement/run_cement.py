#!/usr/bin/env python3
"""H_9285 CEMENT — pre-registered EQUIVALENCE (TOST) closure of the organelle lane.

WHY THIS RUN EXISTS  (see PREREG.md — this docstring IS the registration, frozen by sha256)
--------------------------------------------------------------------------------------
F13 has been measured twice:
  run-1  headline = min(m_A_conj, m_B_conj) = ORDER STATISTIC (rules ①/⑤ violated) -> INVALID;
         a verifier POST-HOC recomputed on the live branch m_B_conj and got KILL. lane declared CLOSED.
  run-2  headline PRE-REGISTERED as m_B_conj, fresh disjoint cues -> the KILL's evidence base
         EVAPORATED: EXP-c0  -0.209 (p=.033) -> +0.129 (ns, SIGN FLIP);
                     SHOCK-c0 +0.100 (p=.023) -> -0.086 (ns, SIGN FLIP) => V2 signed gate FAIL -> INVALID.
         seed-heterogeneity z=2.22 p=.026 => the original p=.033 was a seed-specific noise draw.
         CLOSED was RETRACTED. Diagnosis: this axis is SIGN-RANDOM-NOISE DOMINATED — per-item
         |delta| = 0.37..0.94 (the intervention reaches the detector HARD) but signed mean ~ 0.

This run executes the three CEMENT conditions the card registered, all fixed BEFORE data:
  (a) V-gate is UNSIGNED / displacement-based (a signed gate is structurally unpassable on a
      zero-mean channel; the visible axis is |delta|/item, which is 0.37..0.94 = plenty big).
  (b) n is pre-computed from the MEASURED sd (item-level sd = 1.219 from run-2's verdict set,
      i.e. sd_block 0.545 x sqrt(5)), NOT from an optimistic 6-block pilot. Abort if underpowered.
  (c) "ns" does NOT license CLOSED. Equivalence to practical-zero must be PROVEN with a
      pre-registered TOST against a margin DELTA_EQ fixed before data.

PRE-REGISTERED (frozen before any data is seen):
  * HEADLINE = m_B_conj  (single variable; NOT an order statistic; identical detector to run-2,
    so the two disjoint seeds are commensurable). Primary contrast = EXP - c0 (signed, paired, CRN).
    Analysis unit = ITEM (n = n_main, paired). Block-level (5 items/block) reported as secondary.
  * DELTA_EQ = 0.20 nats  — the equivalence margin, fixed pre-data. Rationale (all pre-data):
      - it is the magnitude of the DISPUTED effect: the KILL-licensing -0.209 and run-2's +0.129
        both fall at/below 0.20 -> a TOST that excludes |effect| >= 0.20 adjudicates exactly the
        claim in dispute, in BOTH directions;
      - it is ~31% of the live detector level (c0 m_B_conj = +0.638 in run-2, +1.083 in run-1):
        an allocation lever worth ANY further spend would have to move held-out recombination by
        at least ~a third of the margin the model already carries for a consumed cue.
    Sensitivity (REPORTED, never used to judge): DELTA_EQ in {0.15, 0.25}.
  * N: sd_used = max(PRIOR_SD_ITEM=1.2192, upper-80% bound of the fresh disjoint pilot sd).
    N_REQ = ceil((z_.95 + z_.80)^2 * sd_used^2 / DELTA_EQ^2)  (TOST power ~80% at true delta=0).
    If n_main < N_REQ -> verdict = INVALID (underpowered; NO scoring, no cementing). Rule ③.
  * V-GATES, on the HEADLINE detector itself (rule ⑤), UNSIGNED (cement condition (a)):
      V0  ops-conservation (rule ⑧): every arm's mixture weights satisfy |sum_e P[t,e]-1| <= 1e-13
          -> the capacity operator never creates supply from nothing. Violation -> abort.
      V0b SHAM-IDENT: arm k=E (mathematical no-op) must give max_i |m_B_conj(SHAM)-m_B_conj(c0)|
          <= 1e-9 -> proves the |delta| statistic has a ZERO numerical floor (an unsigned gate
          cannot be passed by numerical noise).
      V1  liveness: mean_i m_B_conj(c0) > 0, one-sided t > t_crit.
      V2a channel-visibility (SHOCK, UNSIGNED): mean_i |m_B_conj(SHOCK)_i - m_B_conj(c0)_i| with
          95% LOWER CI bound > DELTA_EQ.
      V2b channel-visibility (EXP, UNSIGNED):  same statistic for the TREATMENT arm itself.
      => The detector is provably NOT blind to the treatment channel AT THE RESOLUTION OF THE
         EQUIVALENCE CLAIM: the channel displaces the headline per item by more than the margin
         we then exclude. Hence a signed mean inside +-DELTA_EQ means "no DIRECTED effect",
         not "no channel". Any V-gate FAIL -> INVALID.
  * SIGN-FLIP AXES enumerated pre-data (rule ⑥): setpoint level (EXP vs c0) · constant-k level
    (EXP vs c1_best, grid selected on the DISJOINT pilot) · schedule ordering (EXP vs c2_shuf).
    PASS requires sign preserved (t > +t_crit) on ALL three. EQUIVALENT-CLOSED requires the 90%
    CI inside +-DELTA_EQ on ALL three (no axis may escape the margin).
  * EXECUTABLE VERDICT (rule ⑦):
      if any V-gate fails            -> INVALID
      elif n_main < N_REQ            -> INVALID (underpowered)
      elif PASS (beats all 3)        -> PASS_LEVER      (organelle lane IS a reach lever)
      elif TOST-equivalent on all 3  -> EQUIVALENT_CLOSED (lane CLOSED, licensed)
      else                           -> INCONCLUSIVE    (INVALID; neither proven)
  * DATA: disjoint from BOTH prior runs — (A,B) pair overlap 0, 5-tuple overlap 0, and (fresh-cue
    mode) cue-word overlap 0 against the UNION of run-1 + run-2 (250 tuples / 309 cue words).
    Fresh seeds: scramble 20260714 (prev 20260712 / 20260713), arm-shuffle base 3000 (prev 1000 /
    2000), theta probe seed 21 + a corpus region neither prior run probed.
    Documented pre-data fallback ladder if the fresh-cue pool starves: fresh-cue -> pair-only
    (every tested (A,B) recombination and 5-tuple still NEW; only cue WORDS may recur).
  * tune-to-green AND tune-to-red both forbidden. The verdict is whatever this code returns.
  * Rule ①: no exp-max(controls); control-wise paired-t all reported + pooled-mean.
  * Rule ②: SEM/paired-t only.  Rule ④: info channel (Var(k_t)>0) measured.
  * ENGINE-NATIVE: trunk forward = the installed anima_py production core/decode.py path,
    PARITY-gated byte-exact (max|delta| = 0) against clm._fwd_logits, else abort.
"""
import sys, os, re, json, math, time, random
import numpy as np

SITE = os.environ.get("ANIMA_CORE",
                      "/home/aiden/.local/lib/python3.12/site-packages/anima_py/core")
sys.path.insert(0, SITE)
import decode as clm  # engine-native py 2-production forward

CKPT = os.environ.get("CKPT", "/home/aiden/py303_full.clm")
CORPUS = [os.environ.get("CORPUS_DIR", "/home/aiden/anima_train_corpus") + "/" + f
          for f in ("gen_en.txt", "sns_en.txt")]
OUT = os.environ.get("OUT", "/home/aiden/h9285_cement_result.json")
EXCLUDE = os.environ.get("EXCLUDE", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "prev_exclude_all.json"))
PROBE_ONLY = os.environ.get("PROBE_ONLY", "0") == "1"

T = 24
HEAD = "m_B_conj"           # ★ PRE-REGISTERED HEADLINE (frozen before data)
DELTA_EQ = 0.20             # ★ PRE-REGISTERED equivalence margin (nats), frozen before data
DELTA_EQ_SENS = [0.15, 0.25]  # reported sensitivity only — never used to judge
PRIOR_SD_ITEM = 1.2192      # measured item-level sd of the EXP-c0 delta (run-2 verdict set)
TARGET_MAIN = 334           # verdict items (pool-probe: 384 fresh-cue items at the uni>=20/pmi>0 tier;
                            # n fixed BEFORE any arm was scored — the probe reveals no outcome data)
PILOT_ITEMS = 50            # DISJOINT pilot: sd/MDE + c1_best selection ONLY (never scored)
ITEMS_PER_BLOCK = 5         # for the secondary block-level report only
SCRAMBLE_SEED = 20260714    # fresh (run-1: 20260712 · run-2: 20260713)
ARM_SHUF_BASE = 3000        # fresh (run-1: 1000 · run-2: 2000)
THETA_PROBE_SEED = 21       # fresh (run-1: 7 · run-2: 13)
Z95, Z80, Z975 = 1.6449, 0.8416, 1.9600

PREV_AB, PREV_CUES, PREV_TUP = set(), set(), set()

t0 = time.time()
def log(*a):
    print("[%7.1fs]" % (time.time() - t0), *a, flush=True)


def tq(z, df):
    """Cornish-Fisher t-quantile from the normal quantile (df>=6 here; exact to <1e-3)."""
    return z + (z ** 3 + z) / (4.0 * max(df, 1))


def load_exclude():
    global PREV_AB, PREV_CUES, PREV_TUP
    ex = json.load(open(EXCLUDE))
    PREV_AB = set((a, b) for a, b in ex["ab_pairs"])
    PREV_CUES = set(ex["cues"])
    PREV_TUP = set(tuple(t) for t in ex["tuples"])
    log("exclusion (run-1 ∪ run-2): %d (A,B) pairs · %d cue words · %d 5-tuples"
        % (len(PREV_AB), len(PREV_CUES), len(PREV_TUP)))


# ── engine-native split forward (1:1 with core/decode.py _fwd_trunk, split at the MoE mix) ──
def trunk_split(W, tok):
    d, E, K, L = W["d"], W["E"], W["K"], W["L"]
    xe = W["embed"][tok.astype(np.int64)]
    xt = clm._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    dil = 1
    for li in range(L):
        de = dil if dil <= 512 else 512
        h = clm._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, de)
        hn = clm.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        xt = xt + clm.nn_gelu_fwd(hn).reshape(T, d)
        dil *= 2
    logits_r = clm._conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)
    ex = np.empty((E, T, d), dtype=np.float64)
    for ej in range(E):
        eo = clm._conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)
        ex[ej] = clm.nn_gelu_fwd(eo).reshape(T, d)
    return logits_r, ex


def probs_of(logits_r, E):
    return clm.nn_moe_softmax(logits_r, T, E)


def mix_logits(W, probs, ex, rows=None):
    d, V = W["d"], W["V"]
    y = np.einsum('te,etc->tc', probs, ex)
    yn = clm.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    if rows is None:
        return clm._conv1d(yn, W["roWt"], W["roB"], T, d, V, 1, 1)
    return yn[rows] @ W["roWt"].reshape(d, V) + W["roB"]   # readout is K=1 conv = per-row linear


OPS_MAX_VIOL = [0.0]   # rule ⑧ — max |sum_e P[t,e] - 1| over every arm/position ever mixed


def _ops_check(P):
    v = float(np.abs(P.sum(axis=1) - 1.0).max())
    if v > OPS_MAX_VIOL[0]:
        OPS_MAX_VIOL[0] = v
    return P


def apply_topk(probs, kvec):
    P = probs.copy()
    T_, E = P.shape
    order = np.argsort(-P, axis=1, kind='stable')
    for t in range(T_):
        k = int(kvec[t])
        if k >= E:
            continue
        P[t, order[t, k:]] = 0.0
        s = P[t].sum()
        P[t] = P[t] / s if s > 0 else 1.0 / E
    return P


def cum_mass(probs):
    return np.cumsum(np.sort(probs, axis=1)[:, ::-1], axis=1)


def setpoint_k(probs, theta):
    cm = cum_mass(probs)
    E = probs.shape[1]
    k = np.full(T, E, dtype=np.int64)
    for t in range(T):
        for j in range(E):
            if cm[t, j] >= theta:
                k[t] = j + 1
                break
    return k


# ── detector: held-out conjunctive recombination margin (scramble-referenced) ──
WORD = re.compile(r"\b[a-z]{3,5}\b")

def mine_items(min_items):
    txt = ""
    for p in CORPUS:
        with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
            txt += fh.read().lower() + "\n"
    toks = [(m.group(0), m.start()) for m in WORD.finditer(txt)]
    words = [w for w, _ in toks]
    N = len(words)
    uni = {}
    for w in words:
        uni[w] = uni.get(w, 0) + 1
    vocab = set(uni)
    near = set()
    for i in range(N):
        wi, pi = toks[i]
        j = i + 1
        while j < N and toks[j][1] - pi <= T:
            wj = toks[j][0]
            if wj != wi:
                near.add((wi, wj)); near.add((wj, wi))
            j += 1
    log("corpus words %d · near pairs %d" % (N, len(near)))

    def build(min_uni, min_c, min_pmi):
        col = {}
        for i in range(N):
            wi = words[i]
            if uni[wi] < min_uni:
                continue
            for j in range(i + 1, min(i + 4, N)):
                wj = words[j]
                if wj == wi or uni[wj] < min_uni:
                    continue
                col[(wi, wj)] = col.get((wi, wj), 0) + 1
        pairs = []
        for (u, w), c in col.items():
            if c < min_c:
                continue
            pmi = math.log((c / N) / ((uni[u] / N) * (uni[w] / N) * 3.0))
            if pmi > min_pmi:
                pairs.append((pmi, c, u, w))
        pairs.sort(reverse=True)
        cues = {}
        for pmi, c, u, w in pairs:
            if u in cues or u == w:
                continue
            cues[u] = (w, pmi, c)
        cand = [(u, v[0], v[1], v[2]) for u, v in cues.items()]
        cand.sort(key=lambda x: -x[2])
        return cand

    rng = random.Random(SCRAMBLE_SEED)
    def scramble(w):
        for _ in range(80):
            l = list(w); rng.shuffle(l); s = "".join(l)
            if s != w and s not in vocab:
                return s
        return w[::-1]

    def assemble(cand, cap, fresh_cues):
        items, use = [], {}
        free = lambda *ws: all(use.get(w, 0) < cap for w in ws)
        def take(*ws):
            for w in ws:
                use[w] = use.get(w, 0) + 1
        for i in range(len(cand)):
            A, a = cand[i][0], cand[i][1]
            if not free(A, a):
                continue
            if fresh_cues and A in PREV_CUES:
                continue
            for j in range(i + 1, len(cand)):
                B, b = cand[j][0], cand[j][1]
                if not free(B, b) or len({A, a, B, b}) < 4:
                    continue
                if (A, B) in PREV_AB or (B, A) in PREV_AB:
                    continue
                if fresh_cues and B in PREV_CUES:
                    continue
                if (A, B) in near or (A, b) in near or (B, a) in near or (a, b) in near:
                    continue
                foil = None
                for m in range(len(cand)):
                    C, f = cand[m][0], cand[m][1]
                    if f in (a, b) or C in (A, B) or not free(f):
                        continue
                    if (A, f) in near or (B, f) in near:
                        continue
                    foil = f
                    break
                if foil is None or (A, B, a, b, foil) in PREV_TUP:
                    continue
                if len(A) + len(B) + 2 + max(len(a), len(b), len(foil)) > T:
                    continue
                items.append({"A": A, "B": B, "a": a, "b": b, "f": foil,
                              "As": scramble(A), "Bs": scramble(B)})
                take(A, B, a, b, foil)
                break
        return items

    # pre-data fallback ladder (declared in the prereg): fresh-cue first, then pair-only.
    tiers = [(150, 25, 1.0, 1), (80, 15, 1.0, 2), (60, 12, 0.8, 2), (40, 8, 0.6, 3),
             (30, 6, 0.4, 3), (25, 5, 0.2, 4), (20, 4, 0.0, 5), (15, 3, -0.5, 6)]
    best, best_mode = [], "none"
    for fresh in (True, False):
        for (mu, mc, mp, cap) in tiers:
            cand = build(mu, mc, mp)
            items = assemble(cand, cap, fresh)
            mode = "fresh-cue" if fresh else "pair-only-exclusion"
            log("mode=%-20s uni>=%3d cnt>=%2d pmi>%+.1f cap=%d → cand=%4d items=%4d"
                % (mode, mu, mc, mp, cap, len(cand), len(items)))
            if len(items) > len(best):
                best, best_mode = items, mode
            if fresh and len(items) >= min_items:
                return items, mode
        if best_mode.startswith("fresh") and len(best) >= min_items:
            return best, best_mode
    return best, best_mode


def ctxs(it):
    return {"AB":    "%s %s " % (it["A"], it["B"]),
            "Aonly": "%s %s " % (it["A"], it["Bs"]),
            "Bonly": "%s %s " % (it["As"], it["B"]),
            "null":  "%s %s " % (it["As"], it["Bs"])}

NEED = [("AB", "a"), ("AB", "b"), ("AB", "f"), ("Aonly", "a"), ("Aonly", "f"),
        ("Bonly", "b"), ("Bonly", "f"), ("null", "a"), ("null", "b"), ("null", "f")]


def seq_rows(ctx, content):
    full = ctx + content
    assert len(full.encode()) <= T
    tok = clm._seed_to_tok(full, T)
    n = len(content.encode())
    return tok, np.arange(T - n - 1, T - 1), tok[T - n:].astype(np.int64)


def logp(lg, tgt):
    x = lg - lg.max(axis=1, keepdims=True)
    lse = np.log(np.exp(x).sum(axis=1))
    return float((x[np.arange(len(tgt)), tgt] - lse).sum())


def paired(a, b):
    dd = np.asarray(a) - np.asarray(b)
    n = len(dd)
    mean = float(dd.mean()); sd = float(dd.std(ddof=1)); sem = sd / math.sqrt(n)
    t = mean / sem if sem > 0 else 0.0
    from math import erf
    p = 2 * (1 - 0.5 * (1 + erf(abs(t) / math.sqrt(2))))
    return {"mean_delta": mean, "sd": sd, "sem": sem, "t": t, "p_approx": p, "n": n}


def tost(r, deq):
    """Two one-sided tests. Equivalent iff the (1-2α) CI lies strictly inside ±deq."""
    df = r["n"] - 1
    tc = tq(Z95, df)
    lo = r["mean_delta"] - tc * r["sem"]
    hi = r["mean_delta"] + tc * r["sem"]
    t_lower = (r["mean_delta"] + deq) / r["sem"] if r["sem"] > 0 else 0.0   # H0: delta <= -deq
    t_upper = (deq - r["mean_delta"]) / r["sem"] if r["sem"] > 0 else 0.0   # H0: delta >= +deq
    from math import erf
    p1 = 1 - 0.5 * (1 + erf(t_lower / math.sqrt(2)))
    p2 = 1 - 0.5 * (1 + erf(t_upper / math.sqrt(2)))
    return {"delta_eq": deq, "ci90_lo": lo, "ci90_hi": hi,
            "t_lower": t_lower, "p_lower": p1, "t_upper": t_upper, "p_upper": p2,
            "p_tost": max(p1, p2), "equivalent": bool(lo > -deq and hi < deq)}


def main():
    load_exclude()
    log("load", CKPT)
    W = clm.clm_load_weights(CKPT)
    assert W["ok"] and W.get("bind_type", 0) == 0 and W.get("slw") is None and W.get("clml") is None
    d, E, V = W["d"], W["E"], W["V"]
    KGRID = list(range(1, E + 1))
    log("dims d=%d E=%d K=%d L=%d V=%d T=%d" % (d, E, W["K"], W["L"], V, T))

    # ── PARITY GATE (engine-native) ──
    tokp = clm._seed_to_tok("mind. dream. body", T)
    ref = clm._fwd_logits(W, tokp, T)
    lr, ex = trunk_split(W, tokp)
    parity = float(np.abs(np.asarray(ref) - np.asarray(mix_logits(W, probs_of(lr, E), ex))).max())
    rws = np.arange(18, 23)
    parity_rows = float(np.abs(np.asarray(ref)[rws]
                               - np.asarray(mix_logits(W, probs_of(lr, E), ex, rows=rws))).max())
    log("PARITY max|Δ| = %r (rows-path %r)" % (parity, parity_rows))
    assert parity == 0.0, "engine-native parity FAILED"
    assert parity_rows < 1e-9, "rows-path drift"

    # ── θ (fresh probe: seed 21, a corpus region neither prior run probed) ──
    with open(CORPUS[1], 'rb') as fh:       # sns_en (run-1/run-2 probed gen_en)
        raw = fh.read(700000)
    rr = random.Random(THETA_PROBE_SEED)
    masses = []
    for _ in range(24):
        o = rr.randrange(0, len(raw) - T - 1)
        tk = np.frombuffer(raw[o:o + T], dtype=np.uint8).astype(np.float64)
        lrp, _ = trunk_split(W, tk)
        masses.append(cum_mass(probs_of(lrp, E))[:, 0])
    m1 = np.concatenate(masses)
    THETA = float(np.median(m1))
    log("θ(abs setpoint · fresh probe)=%.4f (mean=%.4f sd=%.4f)" % (THETA, m1.mean(), m1.std()))
    theta_stats = {"theta_prereg": THETA, "top1_mass_mean": float(m1.mean()),
                   "top1_mass_sd": float(m1.std()), "probe_seed": THETA_PROBE_SEED,
                   "probe_region": "sns_en[0:700000]"}

    items, mine_mode = mine_items(TARGET_MAIN + PILOT_ITEMS)
    n_tot = len(items)
    n_ovl_t = sum(1 for it in items if (it["A"], it["B"], it["a"], it["b"], it["f"]) in PREV_TUP)
    n_ovl_ab = sum(1 for it in items if (it["A"], it["B"]) in PREV_AB or (it["B"], it["A"]) in PREV_AB)
    n_ovl_cue = sum(1 for it in items if it["A"] in PREV_CUES or it["B"] in PREV_CUES)
    log("mine mode=%s · items=%d · overlap tuple=%d ab=%d cue=%d"
        % (mine_mode, n_tot, n_ovl_t, n_ovl_ab, n_ovl_cue))
    disjoint_ok = (n_ovl_t == 0 and n_ovl_ab == 0)

    n_main = max(0, n_tot - PILOT_ITEMS)
    if PROBE_ONLY:
        json.dump({"mine_mode": mine_mode, "n_items": n_tot, "n_main_possible": n_main,
                   "overlap_tuple": n_ovl_t, "overlap_ab": n_ovl_ab, "overlap_cue_word": n_ovl_cue,
                   "disjoint_ok": disjoint_ok, "theta": theta_stats,
                   "sample": [{k: it[k] for k in ("A", "B", "a", "b", "f")} for it in items[:8]]},
                  open(OUT, "w"), indent=1)
        log("PROBE_ONLY done →", OUT)
        return

    assert disjoint_ok, "disjointness violated"
    n_main = min(n_main, TARGET_MAIN)
    for i, it in enumerate(items):
        it["set"] = "main" if i < n_main else "pilot"
    items = [it for it in items if it["set"] == "main"] + \
            [it for it in items if it["set"] == "pilot"][:PILOT_ITEMS]
    n_pilot = len(items) - n_main
    log("MAIN(verdict) items=%d · PILOT(disjoint · sd/MDE + c1 selection only) items=%d"
        % (n_main, n_pilot))

    ARMS = ["c0", "c1_k1", "c1_k2", "EXP", "c2_shuf", "SHOCK", "SHAM_ident"]
    rows_out, k_all, k_var = [], [], []

    for idx, it in enumerate(items):
        C = ctxs(it)
        cache = {}
        for cname, xname in NEED:
            tok, rows, tgt = seq_rows(C[cname], it[xname])
            lr, ex = trunk_split(W, tok)
            cache[(cname, xname)] = {"ex": ex, "rows": rows, "tgt": tgt, "p": probs_of(lr, E)}

        def score(key, arm, rng):
            c = cache[key]; P = c["p"]
            if arm == "c0":
                Pm = P
            elif arm.startswith("c1_k"):
                Pm = apply_topk(P, np.full(T, int(arm[-1])))
            elif arm == "EXP":
                Pm = apply_topk(P, setpoint_k(P, THETA))
            elif arm == "c2_shuf":
                kv = setpoint_k(P, THETA).copy(); rng.shuffle(kv); Pm = apply_topk(P, kv)
            elif arm == "SHOCK":
                Pm = np.full_like(P, 1.0 / E)
            elif arm == "SHAM_ident":
                Pm = apply_topk(P, np.full(T, E))       # no-op by construction
            _ops_check(Pm)                               # rule ⑧
            return logp(mix_logits(W, Pm, c["ex"], rows=c["rows"]), c["tgt"])

        srng = np.random.RandomState(ARM_SHUF_BASE + idx)
        S = {arm: {key: score(key, arm, srng) for key in cache} for arm in ARMS}
        for key in cache:
            kv = setpoint_k(cache[key]["p"], THETA)
            k_all.extend(int(v) for v in kv)
            k_var.append(float(np.var(kv)))

        def margins(s):
            lift = lambda c, x: s[(c, x)] - s[("null", x)]
            mA = lift("AB", "a") - lift("AB", "f")
            mB = lift("AB", "b") - lift("AB", "f")
            return {"m_A_conj": mA, "m_B_conj": mB, "m_mean": 0.5 * (mA + mB),
                    "dacc": 1.0 if (mA > 0 and mB > 0) else 0.0,
                    "s_A": lift("Aonly", "a") - lift("Aonly", "f"),
                    "s_B": lift("Bonly", "b") - lift("Bonly", "f")}

        rows_out.append({"item": idx, "set": it["set"],
                         "words": {k: it[k] for k in ("A", "B", "a", "b", "f")},
                         "arm": {arm: margins(S[arm]) for arm in ARMS}})
        if (idx + 1) % 25 == 0:
            log("items %d/%d" % (idx + 1, len(items)))

    # ═════════════ aggregate — ITEM level (primary), block level (secondary) ═════════════
    def vec(arm, field, which="main"):
        return np.array([r["arm"][arm][field] for r in rows_out if r["set"] == which])

    def blocks(arm, field, which="main"):
        v = vec(arm, field, which)
        nb = len(v) // ITEMS_PER_BLOCK
        return v[:nb * ITEMS_PER_BLOCK].reshape(nb, ITEMS_PER_BLOCK).mean(axis=1)

    # ── V0: ops conservation (rule ⑧) ──
    V0_pass = bool(OPS_MAX_VIOL[0] <= 1e-13)
    # ── V0b: SHAM-IDENT zero floor for the UNSIGNED statistic ──
    sham_abs = np.abs(vec("SHAM_ident", HEAD) - vec("c0", HEAD))
    V0b_max = float(sham_abs.max()) if len(sham_abs) else 1.0
    V0b_pass = bool(V0b_max <= 1e-9)

    # ── power (rule ③ · cement condition (b)): sd from the DISJOINT pilot, conservative ──
    pil_d = vec("EXP", HEAD, "pilot") - vec("c0", HEAD, "pilot")
    sd_pilot = float(pil_d.std(ddof=1)); npil = len(pil_d)
    sd_pilot_up80 = sd_pilot * math.sqrt((npil - 1) / max(npil - 1 - Z80 * math.sqrt(2 * (npil - 1)), 1e-9))
    sd_used = max(PRIOR_SD_ITEM, sd_pilot_up80)
    N_REQ = int(math.ceil((Z95 + Z80) ** 2 * sd_used ** 2 / DELTA_EQ ** 2))
    powered = bool(n_main >= N_REQ)
    MDE_super = tq(Z975, n_main - 1) * sd_used / math.sqrt(n_main)

    # ── c1 best constant — selected on the DISJOINT pilot only ──
    cands = ["c1_k%d" % k for k in KGRID[:-1]] + ["c0"]
    c1_grid_pilot = {a: float(vec(a, HEAD, "pilot").mean()) for a in cands}
    sel = max(cands, key=lambda a: c1_grid_pilot[a])

    exp = vec("EXP", HEAD)
    ctrls = ["c0", sel, "c2_shuf"]
    pvc = {("EXP_vs_" + c): paired(exp, vec(c, HEAD)) for c in ctrls}
    pvc["EXP_vs_pooled_mean_of_controls"] = paired(exp, np.mean([vec(c, HEAD) for c in ctrls], axis=0))
    pvc_blk = {("EXP_vs_" + c): paired(blocks("EXP", HEAD), blocks(c, HEAD)) for c in ctrls}

    # ── V1 / V2 (cement condition (a): UNSIGNED, on the headline itself) ──
    v1 = paired(vec("c0", HEAD), np.zeros(n_main))
    V1_pass = bool(v1["t"] > tq(Z95, n_main - 1))

    def unsigned_gate(arm):
        a = np.abs(vec(arm, HEAD) - vec("c0", HEAD))
        m = float(a.mean()); sem = float(a.std(ddof=1)) / math.sqrt(len(a))
        lo = m - tq(Z975, len(a) - 1) * sem
        return {"mean_abs_disp": m, "sem": sem, "ci95_lo": lo, "ci95_hi": m + tq(Z975, len(a) - 1) * sem,
                "delta_eq": DELTA_EQ, "pass": bool(lo > DELTA_EQ)}
    v2a = unsigned_gate("SHOCK"); v2b = unsigned_gate("EXP")
    V2a_pass, V2b_pass = v2a["pass"], v2b["pass"]

    # ── TOST (cement condition (c)) on every sign-flip axis ──
    tosts = {k: tost(pvc["EXP_vs_" + k], DELTA_EQ) for k in ctrls}
    tost_sens = {str(d): {k: tost(pvc["EXP_vs_" + k], d) for k in ctrls} for d in DELTA_EQ_SENS}
    EQUIV_ALL = all(tosts[k]["equivalent"] for k in ctrls)

    tcrit = tq(Z95, n_main - 1)
    beats = lambda r: bool(r["t"] > tcrit)
    PASS = all(beats(pvc["EXP_vs_" + c]) for c in ctrls)

    vgates_ok = V0_pass and V0b_pass and V1_pass and V2a_pass and V2b_pass
    if not vgates_ok:
        verdict = "INVALID"
        reason = ("V-gate FAIL — V0(ops)=%s V0b(sham-zero)=%s V1(liveness)=%s "
                  "V2a(SHOCK unsigned)=%s V2b(EXP unsigned)=%s"
                  % (V0_pass, V0b_pass, V1_pass, V2a_pass, V2b_pass))
    elif not powered:
        verdict = "INVALID"
        reason = "UNDERPOWERED — n_main=%d < N_REQ=%d (sd_used=%.3f, Δ_eq=%.2f)" % (n_main, N_REQ, sd_used, DELTA_EQ)
    elif PASS:
        verdict = "PASS_LEVER"
        reason = "EXP significantly beats c0, c1_best and c2_shuf → organelle lane IS a reach lever"
    elif EQUIV_ALL:
        verdict = "EQUIVALENT_CLOSED"
        reason = ("TOST: |EXP−control| 90%% CI inside ±%.2f on ALL 3 sign-flip axes → the capacity "
                  "schedule has NO directed effect of practical size on held-out recombination → "
                  "organelle lane CLOSED (licensed equivalence, not 'ns')" % DELTA_EQ)
    else:
        verdict = "INCONCLUSIVE"
        reason = "neither PASS nor TOST-equivalence on all axes — no cementing (CI still admits |effect| ≥ Δ_eq)"

    res = {
        "hypothesis": "H_9285_CEMENT",
        "prereg": {"headline": HEAD, "primary_contrast": "EXP - c0 (signed, paired, item-level)",
                   "delta_eq": DELTA_EQ, "delta_eq_sensitivity": DELTA_EQ_SENS,
                   "prior_sd_item": PRIOR_SD_ITEM, "alpha": 0.05,
                   "vgate": "UNSIGNED displacement (cement (a)) + liveness + ops + sham-zero",
                   "n_rule": "n_main >= ceil((z95+z80)^2 sd_used^2 / delta_eq^2), sd_used = max(prior, pilot_up80)",
                   "equivalence": "TOST 90% CI inside +-delta_eq on all 3 sign-flip axes"},
        "ckpt": CKPT, "dims": {"d": d, "E": E, "K": W["K"], "L": W["L"], "V": V, "T": T},
        "parity_max_abs_delta": parity,
        "theta": theta_stats, "mine_mode": mine_mode,
        "n_main_items": n_main, "n_pilot_items": n_pilot, "n_blocks_secondary": n_main // ITEMS_PER_BLOCK,
        "disjoint": {"vs": "union(run-1, run-2)", "overlap_tuple": n_ovl_t,
                     "overlap_ab_pair": n_ovl_ab, "overlap_cue_word": n_ovl_cue, "ok": disjoint_ok},
        "seeds": {"scramble": SCRAMBLE_SEED, "arm_shuffle_base": ARM_SHUF_BASE,
                  "theta_probe": THETA_PROBE_SEED,
                  "prev": {"run1": [20260712, 1000, 7], "run2": [20260713, 2000, 13]}},
        "power": {"sd_pilot": sd_pilot, "sd_pilot_upper80": sd_pilot_up80, "sd_used": sd_used,
                  "N_REQ": N_REQ, "n_main": n_main, "powered": powered,
                  "MDE_superiority_alpha05": MDE_super,
                  "note": "sd_used is the CONSERVATIVE max(measured prior sd, pilot upper-80% bound); "
                          "run-2's 6-block pilot underestimated sd by 2.1x — this cannot recur."},
        "info_channel": {"decision_var": "k_t = f(cumulative router mass at t) — a function of the INPUT; constant arms cannot see it",
                         "k_hist": {str(k): int(np.sum(np.array(k_all) == k)) for k in KGRID},
                         "k_mean": float(np.mean(k_all)), "k_var_overall": float(np.var(k_all)),
                         "k_var_within_seq_mean": float(np.mean(k_var)),
                         "frac_seqs_with_var0": float(np.mean([v == 0 for v in k_var]))},
        "arms": {arm: {"mean": float(vec(arm, HEAD).mean()),
                       "sem": float(vec(arm, HEAD).std(ddof=1) / math.sqrt(n_main)),
                       "dacc": float(vec(arm, "dacc").mean()),
                       "m_A_conj": float(vec(arm, "m_A_conj").mean())} for arm in ARMS},
        "c1_best_constant": {"selected_on_disjoint_pilot": sel, "grid_pilot": c1_grid_pilot,
                             "grid_main_reported": {a: float(vec(a, HEAD).mean()) for a in cands}},
        "paired_vs_controls_HEADLINE_item_level": pvc,
        "paired_vs_controls_HEADLINE_block_level": pvc_blk,
        "vgate": {"V0_ops_conservation": {"max_abs_supply_created": OPS_MAX_VIOL[0], "pass": V0_pass},
                  "V0b_sham_ident_zero_floor": {"max_abs_disp": V0b_max, "pass": V0b_pass},
                  "V1_liveness_c0_gt_0": {**v1, "pass": V1_pass},
                  "V2a_unsigned_channel_SHOCK": v2a,
                  "V2b_unsigned_channel_EXP": v2b},
        "TOST": {"delta_eq": DELTA_EQ, "per_axis": tosts, "equivalent_on_all_axes": EQUIV_ALL,
                 "sensitivity": tost_sens},
        "sign_flip_axes": {"setpoint_level_EXP_vs_c0": pvc["EXP_vs_c0"],
                           "constant_k_level_EXP_vs_c1best": pvc["EXP_vs_" + sel],
                           "schedule_ordering_EXP_vs_c2shuf": pvc["EXP_vs_c2_shuf"]},
        "secondary": {"dacc_EXP_vs_c0": paired(vec("EXP", "dacc"), vec("c0", "dacc")),
                      "SHOCK_vs_c0_signed": paired(vec("SHOCK", HEAD), vec("c0", HEAD)),
                      "SHOCK_vs_c0_TOST": tost(paired(vec("SHOCK", HEAD), vec("c0", HEAD)), DELTA_EQ),
                      "m_A_conj_c0_distal_branch": paired(vec("c0", "m_A_conj"), np.zeros(n_main))},
        "VERDICT": verdict, "verdict_reason": reason,
        "items": rows_out, "wall_s": time.time() - t0,
    }
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)
    log("WROTE", OUT)
    log("=== VERDICT:", verdict, "===", reason)
    log(json.dumps({k: res[k] for k in ("arms", "paired_vs_controls_HEADLINE_item_level",
                                        "vgate", "TOST", "power", "c1_best_constant",
                                        "disjoint", "mine_mode", "info_channel")}, indent=1)[:4000])


if __name__ == "__main__":
    main()
