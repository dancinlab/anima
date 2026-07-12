#!/usr/bin/env python3
"""H_9285 REFIRE — headline PRE-REGISTERED as m_B_conj, measured on a DISJOINT item set.

WHY THIS REFIRE EXISTS
----------------------
The original run.py used headline `m_conj = min(m_A_conj, m_B_conj)` — itself an ORDER
STATISTIC (rules ①/⑤ forbid). The original run returned INVALID; a verifier then
re-computed with the live branch m_B_conj POST-HOC and got KILL. That KILL is directional,
not licensed (post-hoc detector swap = the F8 sin). This refire fixes the headline BEFORE
seeing data and measures on a FRESH held-out item set disjoint from the seed that produced
the original verdict.

PRE-REGISTRATION (frozen before any data is seen — this docstring is the registration):
  * HEADLINE DETECTOR = m_B_conj  (the live, powered conjunctive margin: proximal-cue branch;
    prior characterization: c0=+1.083, t=+4.69, MDE 0.190 << 1.083). NOT an order statistic.
  * DISJOINT DATA: items whose (A,B) recombination cue-pair is NOT any prev item's (A,B),
    and (fresh-cue mode) whose cue words A,B never served as a cue in the prev set. Fresh
    scramble seed (20260713) + fresh arm-shuffle base (2000+idx) + fresh θ probe (seed 13,
    different corpus region) → the verdict-deriving seed is disjoint from the original run.
  * V-GATES ON THE HEADLINE ITSELF (rule ⑤):
      V1 liveness       : c0 mean(m_B_conj) > 0, paired-t vs 0, t > +2.093 (α=.05, n=20).
      V2 channel-visible: SHOCK(router destroyed) vs c0 on m_B_conj, |t| > 2.093
                          (proves the treatment channel is visible to THIS detector).
    If either FAILS  -> verdict = INVALID (dead / blind detector; no cementing).
  * MDE pre-check (rule ③): MDE_{α05,n20} on the HEADLINE axis m_B_conj (the axis the capacity
    treatment causally reaches), estimated on a PILOT ITEM SET that is DISJOINT from the 100-item
    verdict set (30 separate items / 6 blocks; the original run's pilot was a SUBSET of its
    analysis blocks). Power check: MDE < |pilot c0 level|. If not -> INVALID (underpowered).
    The best-constant control c1 is likewise selected on the disjoint pilot, never on the
    verdict set.
  * SIGN-FLIP AXES enumerated (rule ⑥): θ setpoint level (c0 vs EXP), constant-k level
    (c1 grid), schedule ordering (c2 shuffle). PASS requires sign preserved across ALL three.
  * PRE-REGISTERED VERDICT (rule ⑦ — executable branch):
      PASS  = EXP beats c0 AND c1_best AND c2 each with paired-t > +2.093 (positive).
              -> organelle lane is a reach lever (surprising; would reopen 303M spend).
      FAIL  = every capacity treatment (EXP vs each of c0/c1_best/c2) is degrading (Δ<=0)
              or ns (|t|<=2.093).  == card's pre-registered FAIL scenario (H_9283 prediction)
              -> organelle lane CLOSED cement (KILL).
      (V-gate fail dominates -> INVALID.)
  * tune-to-green AND tune-to-red both forbidden. The verdict is whatever the code returns.

ENGINE-NATIVE: trunk forward reuses the installed anima_py core/decode.py production path,
PARITY-gated byte-exact (max|Δ|=0) against clm._fwd_logits. Not a mirror -> engine-parity.

INSTRUMENTATION RULES (identical to the census-enforced set):
  1. No Δ=exp−max(controls); no order-statistic headline. control-wise paired-t all reported.
  2. SEM/paired-t only.
  3. pre MDE on the axis the treatment causally reaches (m_B_conj), pilot-disjoint.
  4. info channel: k_t=f(router mass), Var(k_t)>0, measured.
  5. V-gates on the HEADLINE detector itself (m_B_conj).
  6. sign-flip axes enumerated; sign preservation in PASS condition.
  7. KILL/PASS branch is executable code (below).
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
OUT = os.environ.get("OUT", "/home/aiden/h9285_refire_result.json")
EXCLUDE = os.environ.get("EXCLUDE", os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                 "prev_exclude.json"))
PROBE_ONLY = os.environ.get("PROBE_ONLY", "0") == "1"

T = 24
N_BLOCK = 20            # MAIN (verdict) blocks
ITEMS_PER_BLOCK = 5     # → main = 100 items
PILOT_BLOCKS = 6        # MDE pilot blocks — DISJOINT items (rule ③: pilot ∩ analysis = ∅)
KGRID = None
THETA_PREREG = None
HEAD = "m_B_conj"          # ★ PRE-REGISTERED HEADLINE (frozen before data)
SCRAMBLE_SEED = 20260713   # fresh (prev used 20260712)
ARM_SHUF_BASE = 2000       # fresh (prev used 1000+idx)
THETA_PROBE_SEED = 13      # fresh (prev used 7)

# disjointness exclusion (loaded at runtime)
PREV_AB = set()            # (A,B) recombination pairs already tested
PREV_CUES = set()          # words that served as a cue A or B in prev
PREV_TUP = set()

t0 = time.time()
def log(*a):
    print("[%7.1fs]" % (time.time() - t0), *a, flush=True)


def load_exclude():
    global PREV_AB, PREV_CUES, PREV_TUP
    if not os.path.exists(EXCLUDE):
        log("!! EXCLUDE file missing", EXCLUDE, "— proceeding with EMPTY exclusion (NOT disjoint)")
        return
    ex = json.load(open(EXCLUDE))
    PREV_AB = set((a, b) for a, b in ex["ab_pairs"])
    PREV_CUES = set(ex["cues"])
    PREV_TUP = set(tuple(t) for t in ex["tuples"])
    log("exclusion loaded: %d prev (A,B) pairs · %d prev cue words · %d prev tuples"
        % (len(PREV_AB), len(PREV_CUES), len(PREV_TUP)))


# ═══════════════════════════════════════════════════════════════════════════
# engine-native split forward (1:1 with core/decode.py _fwd_trunk up to the MoE mix)
# ═══════════════════════════════════════════════════════════════════════════
def trunk_split(W, tok):
    """1:1 with the installed anima_py core/decode.py _fwd_trunk, split at the MoE mix."""
    d, E, K, L = W["d"], W["E"], W["K"], W["L"]
    ids = tok.astype(np.int64)
    xe = W["embed"][ids]
    xt = clm._conv1d(xe, W["ecWt"], W["ecB"], T, d, d, K, 1)
    dil = 1
    for li in range(L):
        de = dil if dil <= 512 else 512
        h = clm._conv1d(xt, W["tcWt"][li], W["tcB"][li], T, d, d, K, de)
        hn = clm.nn_groupnorm_fwd(h, W["tgG"][li], W["tgB"][li], T, d, 1)
        hg = clm.nn_gelu_fwd(hn)
        xt = xt + hg.reshape(T, d)
        dil = dil * 2
    logits_r = clm._conv1d(xt, W["rWt"], W["rB"], T, d, E, 1, 1)
    ex = np.empty((E, T, d), dtype=np.float64)
    for ej in range(E):
        eo = clm._conv1d(xt, W["eWt"][ej], W["eB"][ej], T, d, d, K, 1)
        ex[ej] = clm.nn_gelu_fwd(eo).reshape(T, d)
    return logits_r, ex


def probs_of(logits_r, E):
    return clm.nn_moe_softmax(logits_r, T, E)


def mix_logits(W, probs, ex, rows=None):
    """probs[T,E] (arm-modified) → dense mix → final GN → readout. rows = logit rows needed."""
    d, V, E = W["d"], W["V"], W["E"]
    y = np.einsum('te,etc->tc', probs, ex)
    yn = clm.nn_groupnorm_fwd(y, W["noG"], W["noB"], T, d, 1)
    if rows is None:
        return clm._conv1d(yn, W["roWt"], W["roB"], T, d, V, 1, 1)
    # readout is a K=1 conv ⇒ pure per-row linear; restrict to the rows we score.
    sub = yn[rows]
    return sub @ W["roWt"].reshape(d, V) + W["roB"]


def apply_topk(probs, kvec):
    P = probs.copy()
    T_, E = P.shape
    order = np.argsort(-P, axis=1, kind='stable')
    for t in range(T_):
        k = int(kvec[t])
        if k >= E:
            continue
        drop = order[t, k:]
        P[t, drop] = 0.0
        s = P[t].sum()
        P[t] = P[t] / s if s > 0 else 1.0 / E
    return P


def cum_mass(probs):
    s = np.sort(probs, axis=1)[:, ::-1]
    return np.cumsum(s, axis=1)


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


# ═══════════════════════════════════════════════════════════════════════════
# detector — held-out conjunctive recombination margin (2-cue, scramble-referenced)
# m_B_conj = lift(b|AB) − lift(f|AB)   (proximal-cue branch = HEADLINE)
# ═══════════════════════════════════════════════════════════════════════════
WORD = re.compile(r"\b[a-z]{3,5}\b")

def mine_items(min_items):
    txt = ""
    for p in CORPUS:
        with open(p, 'r', encoding='utf-8', errors='ignore') as fh:
            txt += fh.read().lower() + "\n"
    toks = [(m.group(0), m.start()) for m in WORD.finditer(txt)]
    words = [w for w, _ in toks]
    N = len(words)
    log("corpus words", N)
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
    log("near pairs (co-present within a 24B window)", len(near))

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

    # DISJOINTNESS: fresh-cue mode requires A,B never used as a prev cue AND (A,B) not a prev pair.
    # If that starves the pool, relax to pair-only exclusion (still every tested (A,B) is new).
    def assemble(cand, cap, fresh_cues):
        items = []
        use = {}
        def free(*ws):
            return all(use.get(w, 0) < cap for w in ws)
        def take(*ws):
            for w in ws:
                use[w] = use.get(w, 0) + 1
        def cue_ok(A, B):
            if (A, B) in PREV_AB or (B, A) in PREV_AB:
                return False
            if fresh_cues and (A in PREV_CUES or B in PREV_CUES):
                return False
            return True
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
                if not cue_ok(A, B):
                    continue
                if (A, B) in near or (A, b) in near or (B, a) in near or (a, b) in near:
                    continue
                if tuple([A, B, a, b, None]) and (A, B, a, b) in {t[:4] for t in PREV_TUP}:
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
                if foil is None:
                    continue
                if (A, B, a, b, foil) in PREV_TUP:
                    continue
                if len(A) + len(B) + 2 + max(len(a), len(b), len(foil)) > T:
                    continue
                items.append({"A": A, "B": B, "a": a, "b": b, "f": foil,
                              "As": scramble(A), "Bs": scramble(B)})
                take(A, B, a, b, foil)
                break
        return items

    tiers = [(150, 25, 1.0, 1), (80, 15, 1.0, 2), (60, 12, 0.8, 2), (40, 8, 0.6, 3),
             (30, 6, 0.4, 3), (25, 5, 0.2, 4)]
    for fresh in (True, False):
        for (mu, mc, mp, cap) in tiers:
            cand = build(mu, mc, mp)
            items = assemble(cand, cap, fresh)
            log("mode=%s uni>=%d cnt>=%d pmi>%.1f cap=%d → cand=%d items=%d"
                % ("fresh-cue" if fresh else "pair-only", mu, mc, mp, cap, len(cand), len(items)))
            if len(items) >= min_items:
                items = items[:max(min_items, len(items))]
                MODE = "fresh-cue" if fresh else "pair-only-exclusion"
                return items, MODE
    # return best effort at loosest pair-only
    cand = build(*tiers[-1][:3])
    items = assemble(cand, tiers[-1][3], False)
    return items, "pair-only-best-effort"


def ctxs(it):
    return {"AB":    "%s %s " % (it["A"], it["B"]),
            "Aonly": "%s %s " % (it["A"], it["Bs"]),
            "Bonly": "%s %s " % (it["As"], it["B"]),
            "null":  "%s %s " % (it["As"], it["Bs"])}


NEED = [("AB", "a"), ("AB", "b"), ("AB", "f"),
        ("Aonly", "a"), ("Aonly", "f"),
        ("Bonly", "b"), ("Bonly", "f"),
        ("null", "a"), ("null", "b"), ("null", "f")]


def seq_rows(ctx, content):
    full = ctx + content
    fb = full.encode()
    assert len(fb) <= T, (full, len(fb))
    tok = clm._seed_to_tok(full, T)
    n = len(content.encode())
    rows = np.arange(T - n - 1, T - 1)
    tgt = tok[T - n:].astype(np.int64)
    return tok, rows, tgt


def logp(logit_rows, tgt):
    x = logit_rows - logit_rows.max(axis=1, keepdims=True)
    lse = np.log(np.exp(x).sum(axis=1))
    return float((x[np.arange(len(tgt)), tgt] - lse).sum())


def paired(a, b):
    dd = a - b
    n = len(dd)
    mean = float(dd.mean())
    sd = float(dd.std(ddof=1))
    sem = sd / math.sqrt(n)
    t = mean / sem if sem > 0 else 0.0
    from math import erf
    p = 2 * (1 - 0.5 * (1 + erf(abs(t) / math.sqrt(2))))
    return {"mean_delta": mean, "sd": sd, "sem": sem, "t": t, "p_approx": p, "n": n}


# ═══════════════════════════════════════════════════════════════════════════
def main():
    global KGRID, THETA_PREREG, ITEMS_PER_BLOCK
    load_exclude()
    log("load", CKPT)
    W = clm.clm_load_weights(CKPT)
    assert W["ok"] and W.get("bind_type", 0) == 0 and W.get("slw") is None and W.get("clml") is None
    d, E, V = W["d"], W["E"], W["V"]
    KGRID = list(range(1, E + 1))
    log("dims d=%d E=%d K=%d L=%d V=%d T=%d" % (d, E, W["K"], W["L"], V, T))
    T_CRIT = 2.093  # t_.975,19

    # ── PARITY GATE ──
    tokp = clm._seed_to_tok("mind. dream. body", T)
    ref = clm._fwd_logits(W, tokp, T)
    lr, ex = trunk_split(W, tokp)
    got = mix_logits(W, probs_of(lr, E), ex)
    parity = float(np.abs(np.asarray(ref) - np.asarray(got)).max())
    rws = np.arange(18, 23)
    got_r = mix_logits(W, probs_of(lr, E), ex, rows=rws)
    parity_rows = float(np.abs(np.asarray(ref)[rws] - np.asarray(got_r)).max())
    log("PARITY max|Δ| = %r (rows-path %r)" % (parity, parity_rows))
    assert parity == 0.0, "engine-native parity FAILED"
    assert parity_rows < 1e-9, "rows-path drift"

    # ── θ (fresh probe: seed 13, disjoint corpus region [400k:1.2M]) ──
    with open(CORPUS[0], 'rb') as fh:
        fh.seek(400000)
        raw = fh.read(800000)
    rr = random.Random(THETA_PROBE_SEED)
    masses = []
    for _ in range(24):
        o = rr.randrange(0, len(raw) - T - 1)
        tk = np.frombuffer(raw[o:o + T], dtype=np.uint8).astype(np.float64)
        lr_p, _ = trunk_split(W, tk)
        cm = cum_mass(probs_of(lr_p, E))
        masses.append(cm[:, 0])
    m1 = np.concatenate(masses)
    THETA_PREREG = float(np.median(m1))
    log("θ(abs setpoint · fresh probe)=%.4f (mean=%.4f sd=%.4f)" % (THETA_PREREG, m1.mean(), m1.std()))
    theta_stats = {"top1_mass_mean": float(m1.mean()), "top1_mass_sd": float(m1.std()),
                   "theta_prereg": THETA_PREREG, "probe_seed": THETA_PROBE_SEED,
                   "probe_region": "gen_en[400000:1200000]"}

    N_MAIN = N_BLOCK * ITEMS_PER_BLOCK            # 100  (verdict)
    N_PILOT = PILOT_BLOCKS * ITEMS_PER_BLOCK      # 30   (MDE only, disjoint)
    items, mine_mode = mine_items(N_MAIN + N_PILOT)
    log("mine mode = %s · items = %d (need main %d + pilot %d)"
        % (mine_mode, len(items), N_MAIN, N_PILOT))
    # verify disjointness
    n_overlap_tup = sum(1 for it in items if (it["A"], it["B"], it["a"], it["b"], it["f"]) in PREV_TUP)
    n_overlap_ab = sum(1 for it in items if (it["A"], it["B"]) in PREV_AB or (it["B"], it["A"]) in PREV_AB)
    log("DISJOINT CHECK: tuple-overlap=%d  (A,B)-pair-overlap=%d  (both must be 0)"
        % (n_overlap_tup, n_overlap_ab))
    disjoint_ok = (n_overlap_tup == 0 and n_overlap_ab == 0)

    if PROBE_ONLY:
        json.dump({"mine_mode": mine_mode, "n_items": len(items),
                   "items_per_block_possible": len(items) // N_BLOCK,
                   "overlap_tuple": n_overlap_tup, "overlap_ab": n_overlap_ab,
                   "disjoint_ok": disjoint_ok, "theta": theta_stats,
                   "sample": [{k: it[k] for k in ("A", "B", "a", "b", "f")} for it in items[:8]]},
                  open(OUT, "w"), indent=1)
        log("PROBE_ONLY done → wrote", OUT)
        return

    assert len(items) >= N_MAIN + N_PILOT, \
        "item pool too small (%d < %d)" % (len(items), N_MAIN + N_PILOT)
    # MAIN = verdict set (blocks 0..19) · PILOT = MDE set, DISJOINT items (blocks 0..5)
    items = items[:N_MAIN + N_PILOT]
    for i, it in enumerate(items):
        if i < N_MAIN:
            it["set"] = "main"; it["blk"] = i // ITEMS_PER_BLOCK
        else:
            it["set"] = "pilot"; it["blk"] = (i - N_MAIN) // ITEMS_PER_BLOCK
    n_use = len(items)
    nblk = N_BLOCK
    log("MAIN blocks=%d items=%d | PILOT blocks=%d items=%d (disjoint) | per block %d"
        % (N_BLOCK, N_MAIN, PILOT_BLOCKS, N_PILOT, ITEMS_PER_BLOCK))

    ARMS = ["c0", "c1_k1", "c1_k2", "EXP", "c2_shuf", "SHOCK"]
    rows_out = []
    kstats = {"k_all": [], "var_per_seq": []}

    for idx, it in enumerate(items):
        C = ctxs(it)
        cache = {}
        for cname, xname in NEED:
            ctx, content = C[cname], it[xname]
            tok, rows, tgt = seq_rows(ctx, content)
            lr, ex = trunk_split(W, tok)
            cache[(cname, xname)] = {"lr": lr, "ex": ex, "rows": rows, "tgt": tgt,
                                     "p": probs_of(lr, E)}

        def score(key, arm, rng=None):
            c = cache[key]; P = c["p"]
            if arm == "c0":
                Pm = P
            elif arm.startswith("c1_k"):
                k = int(arm[-1]); Pm = apply_topk(P, np.full(T, k))
            elif arm == "EXP":
                Pm = apply_topk(P, setpoint_k(P, THETA_PREREG))
            elif arm == "c2_shuf":
                kv = setpoint_k(P, THETA_PREREG).copy(); rng.shuffle(kv); Pm = apply_topk(P, kv)
            elif arm == "SHOCK":
                Pm = np.full_like(P, 1.0 / E)
            lg = mix_logits(W, Pm, c["ex"], rows=c["rows"])
            return logp(lg, c["tgt"])

        srng = np.random.RandomState(ARM_SHUF_BASE + idx)
        S = {arm: {key: score(key, arm, srng) for key in cache} for arm in ARMS}

        for key in cache:
            kv = setpoint_k(cache[key]["p"], THETA_PREREG)
            kstats["k_all"].extend([int(v) for v in kv])
            kstats["var_per_seq"].append(float(np.var(kv)))

        def margins(s):
            lift = lambda c, x: s[(c, x)] - s[("null", x)]
            mA = lift("AB", "a") - lift("AB", "f")
            mB = lift("AB", "b") - lift("AB", "f")
            sA = lift("Aonly", "a") - lift("Aonly", "f")
            sB = lift("Bonly", "b") - lift("Bonly", "f")
            return {"m_A_conj": mA, "m_B_conj": mB,
                    "m_conj": min(mA, mB), "m_mean": 0.5 * (mA + mB),
                    "dacc": 1.0 if (mA > 0 and mB > 0) else 0.0,
                    "ceiling": min(sA, sB), "s_A": sA, "s_B": sB}

        rows_out.append({"item": idx, "set": it["set"], "block": it["blk"],
                         "words": {k: it[k] for k in ("A", "B", "a", "b", "f")},
                         "arm": {arm: margins(S[arm]) for arm in ARMS}})
        if (idx + 1) % 12 == 0:
            log("items done %d/%d" % (idx + 1, n_use))

    # ═══════════════ aggregate ═══════════════
    def blockmean(arm, field, which="main", blocks=None):
        nb = N_BLOCK if which == "main" else PILOT_BLOCKS
        out = []
        for b in range(nb):
            if blocks is not None and b not in blocks:
                continue
            v = [r["arm"][arm][field] for r in rows_out
                 if r["set"] == which and r["block"] == b]
            out.append(float(np.mean(v)))
        return np.array(out)

    # ── MDE (rule ③) — estimated ONLY on the PILOT items (disjoint from the verdict set),
    #    on the headline axis m_B_conj (the axis the capacity treatment causally reaches). ──
    pe = blockmean("EXP", HEAD, "pilot"); pc = blockmean("c0", HEAD, "pilot")
    sd_pilot = float((pe - pc).std(ddof=1))
    MDE = T_CRIT * sd_pilot / math.sqrt(N_BLOCK)
    pilot_c0_level = float(pc.mean())
    c0_level = float(blockmean("c0", HEAD).mean())          # main (reported)
    # power pre-check uses the PILOT-side dynamic range (analysis set never consulted)
    mde_ok = bool(MDE < abs(pilot_c0_level))

    # ── info channel ──
    info = {
        "decision_var": "cumulative router mass at position t — function of INPUT tokens; c1 cannot see it",
        "k_hist": {str(k): int(np.sum(np.array(kstats["k_all"]) == k)) for k in KGRID},
        "k_mean": float(np.mean(kstats["k_all"])), "k_var_overall": float(np.var(kstats["k_all"])),
        "k_var_within_seq_mean": float(np.mean(kstats["var_per_seq"])),
        "frac_seqs_with_var0": float(np.mean([v == 0 for v in kstats["var_per_seq"]])),
    }

    # ── c1 = BEST constant k over the FULL grid. Selected on the DISJOINT PILOT set, so the
    #    verdict set is never consulted to pick the control (no selection bias). k=E ≡ c0 dense. ──
    exp = blockmean("EXP", HEAD)
    cands = ["c1_k%d" % k for k in KGRID[:-1]] + ["c0"]
    sel = max(cands, key=lambda a: float(blockmean(a, HEAD, "pilot").mean()))
    c1_grid_pilot = {a: float(blockmean(a, HEAD, "pilot").mean()) for a in cands}
    c1_grid = {a: float(blockmean(a, HEAD).mean()) for a in cands}

    # ── control-wise paired-t on the HEADLINE (rule ①) ──
    pvc = {}
    for ctrl in ["c0", sel, "c2_shuf"]:
        pvc["EXP_vs_" + ctrl] = paired(exp, blockmean(ctrl, HEAD))
    pooled = np.mean([blockmean(c, HEAD) for c in ["c0", sel, "c2_shuf"]], axis=0)
    pvc["EXP_vs_pooled_mean_of_controls"] = paired(exp, pooled)

    # ── V-GATES ON THE HEADLINE DETECTOR ITSELF (rule ⑤) ──
    v_liveness = paired(blockmean("c0", HEAD), np.zeros(nblk))     # c0 m_B_conj > 0
    v_channel = paired(blockmean("SHOCK", HEAD), blockmean("c0", HEAD))  # SHOCK moves headline
    V1_pass = bool(v_liveness["t"] > T_CRIT)                       # liveness (one-sided +)
    V2_pass = bool(abs(v_channel["t"]) > T_CRIT)                   # channel visible (two-sided)

    # ── PRE-REGISTERED EXECUTABLE VERDICT (rule ⑦) ──
    exp_c0 = pvc["EXP_vs_c0"]; exp_c1 = pvc["EXP_vs_" + sel]; exp_c2 = pvc["EXP_vs_c2_shuf"]
    beats = lambda r: bool(r["t"] > T_CRIT)                        # EXP sig ABOVE control (+)
    PASS = beats(exp_c0) and beats(exp_c1) and beats(exp_c2)
    # FAIL scenario (card): every capacity treatment degrades or ns
    all_deg_or_ns = all((r["t"] <= T_CRIT) for r in (exp_c0, exp_c1, exp_c2))

    if not V1_pass:
        verdict = "INVALID"; reason = "V1 liveness FAIL — headline m_B_conj not alive at c0 (t=%.2f<=%.2f)" % (v_liveness["t"], T_CRIT)
    elif not V2_pass:
        verdict = "INVALID"; reason = "V2 channel-visibility FAIL — SHOCK does not move headline (|t|=%.2f<=%.2f)" % (abs(v_channel["t"]), T_CRIT)
    elif not mde_ok:
        verdict = "INVALID"; reason = "underpowered — MDE %.3f >= |pilot c0 level| %.3f" % (MDE, abs(pilot_c0_level))
    elif PASS:
        verdict = "PASS_LEVER"; reason = "EXP sig beats c0,c1_best,c2 all → organelle lane IS a reach lever (surprising)"
    elif all_deg_or_ns:
        verdict = "FAIL_CLOSED"; reason = "every capacity treatment degrades/ns on live headline → organelle lane CLOSED cement (KILL · card FAIL scenario · H_9283 prediction)"
    else:
        verdict = "MIXED"; reason = "EXP beats some but not all controls — not the clean PASS or FAIL scenario"

    res = {
        "hypothesis": "H_9285_REFIRE",
        "prereg_headline": "m_B_conj (live proximal-cue conjunctive recombination margin) — fixed before data",
        "prereg_note": "NOT an order statistic. verdict-deriving seed disjoint from original run.",
        "ckpt": CKPT, "dims": {"d": d, "E": E, "K": W["K"], "L": W["L"], "V": V, "T": T},
        "parity_max_abs_delta": parity,
        "n_blocks": nblk, "items_per_block": ITEMS_PER_BLOCK, "n_items": n_use,
        "n_main_items": N_MAIN, "n_pilot_items": N_PILOT, "pilot_blocks": PILOT_BLOCKS,
        "pilot_disjoint_from_verdict_set": True,
        "mine_mode": mine_mode, "disjoint_ok": disjoint_ok,
        "disjoint_check": {"overlap_tuple": n_overlap_tup, "overlap_ab_pair": n_overlap_ab},
        "seeds": {"scramble": SCRAMBLE_SEED, "arm_shuffle_base": ARM_SHUF_BASE,
                  "theta_probe": THETA_PROBE_SEED,
                  "prev_seeds": {"scramble": 20260712, "arm_shuffle_base": 1000, "theta_probe": 7}},
        "headline": HEAD, "theta": theta_stats, "info_channel": info,
        "mde": {"sd_pilot_blockdelta": sd_pilot, "MDE_alpha05_n20": MDE,
                "pilot_c0_level_headline": pilot_c0_level,
                "main_c0_level_headline": c0_level,
                "mde_ok": mde_ok, "pilot_blocks": PILOT_BLOCKS,
                "note": "MDE from DISJOINT pilot items only; verdict set not used for the power check"},
        "arms": {arm: {"mean": float(blockmean(arm, HEAD).mean()),
                       "sem_across_blocks": float(blockmean(arm, HEAD).std(ddof=1) / math.sqrt(nblk)),
                       "dacc": float(blockmean(arm, "dacc").mean()),
                       "m_A_conj": float(blockmean(arm, "m_A_conj").mean())} for arm in ARMS},
        "c1_best_constant": {"selected_on_disjoint_pilot": sel,
                             "grid_pilot_used_for_selection": c1_grid_pilot,
                             "grid_main_reported": c1_grid},
        "paired_vs_controls_HEADLINE": pvc,
        "vgate_on_headline": {
            "V1_liveness_c0_gt_0": {**v_liveness, "pass": V1_pass},
            "V2_channel_SHOCK_vs_c0": {**v_channel, "pass": V2_pass},
        },
        "sign_flip_axes": {
            "setpoint_level_EXP_vs_c0": exp_c0,
            "constant_k_level_EXP_vs_c1best": exp_c1,
            "schedule_ordering_EXP_vs_c2shuf": exp_c2,
            "note": "PASS requires t>+2.093 on ALL three (sign preserved). enumerated pre-data (rule 6).",
        },
        "secondary": {
            "dacc_EXP_vs_c0": paired(blockmean("EXP", "dacc"), blockmean("c0", "dacc")),
            "m_conj_min_EXP_vs_c0_FORBIDDEN_order_stat_for_reference_only":
                paired(blockmean("EXP", "m_conj"), blockmean("c0", "m_conj")),
        },
        "VERDICT": verdict, "verdict_reason": reason,
        "items": rows_out, "wall_s": time.time() - t0,
    }
    with open(OUT, 'w') as fh:
        json.dump(res, fh, indent=1)
    log("WROTE", OUT)
    log("=== VERDICT:", verdict, "===", reason)
    log(json.dumps({k: res[k] for k in ("arms", "paired_vs_controls_HEADLINE",
                                        "vgate_on_headline", "mde", "c1_best_constant",
                                        "disjoint_check", "mine_mode")}, indent=1))


if __name__ == "__main__":
    main()
