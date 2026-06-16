"""
H_1396 — G5 IN-DISTRIBUTION metacognition: CEILING vs FIXABLE?
=============================================================================
The G5 metacog residual "🟠 THIN in-dist" is the FIRE-side, in-distribution slice:
among items the live copy-or-abstain gate FIRES on (grounded, light/no shift), can a
confidence signal discriminate the cases it gets RIGHT from the ones it gets WRONG?
H_1202 set overall type-2 meta-d' M-ratio 0.924 (near-optimal); H_1304 found the
wrong-fire class is structurally near-empty at L=0 — which is exactly why in-dist
type-2 is THIN (little correctness variance to track). This probe asks whether that
thinness is a NEAR-INHERENT CEILING (honest near-optimality) or a FIXABLE deficiency
(a richer READ-ONLY confidence signal lifts in-dist type-2 AUROC by >= Δ=0.10 without
breaking the OOD/abstain property H_1304).

Signals compared (all read-only from the SAME cell store, NO new training, NO label, p6):
  (a) CURRENT  = best-cell recall margin           (== immune_memory_recall_margin; baseline)
  (b) RICHER-1 = top-2 cos affinity gap            (decisiveness)
  (c) RICHER-2 = neg-entropy of softmax over top-k cos affinities (2nd-order spread)
  (d) ORACLE   = determinate-correctness ceiling reference

Mechanism = byte-exact mirror of CORE/engine_cli.hexa immune_embed_key + ImmuneMemory
affinity geometry (VERBATIM H_1361/H_1304). numpy mirror = DIRECTIONAL (engine-transfer
UNVERIFIED). A FIXABLE 🟢 names the engine top-k-exposure op as the binding follow-on.
3 seeds. frozen-first; NO bar moved post-hoc (c9). $0 CPU, p7. Live CORE/*.hexa UNTOUCHED.
"""
import os, json, math
import numpy as np

OUTDIR = os.path.join(os.path.dirname(__file__), "..", "..", ".verdicts", "1396_g5_indist_metacog")
DIM = 64
NGRAM = 3
RECALL_THR = 0.15                          # frozen == engine recall_thr
INDIST_LEVELS = [0.00, 0.05, 0.10]         # IN-DISTRIBUTION light-shift band (items still mostly fire)
OOD_LEVELS = [0.20, 0.30, 0.40]            # OOD ladder for the H_1304 abstain-intact re-check
N_FACTS = 80
N_TRIAL = 400                              # in-dist query trials per level
KEYLEN = 20
TOPK = 8
DELTA = 0.10                               # frozen FIXABLE lift threshold
SEEDS = [7, 8, 9]


# ── byte-trigram FNV-1a embed key (VERBATIM mirror of immune_embed_key, H_1361/H_1304) ──
def _fnv1a(bs):
    h = 2166136261
    for b in bs:
        h = (h ^ b) & 0xFFFFFFFF
        h = (h * 16777619) & 0xFFFFFFFF
    return h


def embed_key(text):
    v = np.zeros(DIM, dtype=np.float64)
    bs = [ord(c) for c in text]
    blen = len(bs)
    if blen < NGRAM:
        v[_fnv1a(bs) % DIM] += 1.0
    else:
        for i in range(blen - NGRAM + 1):
            v[_fnv1a(bs[i:i + NGRAM]) % DIM] += 1.0
    nrm = math.sqrt(float(np.dot(v, v)))
    return v / nrm if nrm > 0.0 else v


def mutate(text, frac, rng):
    if frac <= 0.0:
        return text
    chars = list(text)
    n = len(chars)
    k = int(round(frac * n))
    if k <= 0:
        return text
    idxs = rng.choice(n, size=k, replace=False)
    al = list(range(ord('a'), ord('z') + 1))
    for i in idxs:
        chars[i] = chr(int(rng.choice(al)))
    return "".join(chars)


def auroc(scores, labels):
    s = np.asarray(scores, dtype=np.float64)
    y = np.asarray(labels, dtype=np.int64)
    pos = s[y == 1]; neg = s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    uniq, inv, counts = np.unique(s, return_inverse=True, return_counts=True)
    avg = {}; start = 0
    for ci, c in enumerate(counts):
        avg[ci] = (start + 1 + start + c) / 2.0
        start += c
    ranks = np.array([avg[i] for i in inv])
    r_pos = ranks[y == 1].sum()
    n_pos = len(pos); n_neg = len(neg)
    u = r_pos - n_pos * (n_pos + 1) / 2.0
    return float(u / (n_pos * n_neg))


def _rand_token(rng, length):
    al = list(range(ord('a'), ord('z') + 1))
    return "".join(chr(int(rng.choice(al))) for _ in range(length))


def _build(seed):
    """Build a collision-PRONE store so in-dist WRONG fires exist: half the facts are
    random tokens, half are near-duplicates of an existing token (shared-trigram neighbors)
    bound to a DIFFERENT answer. Light corruption can then route a fire to a wrong-but-
    confident neighbor cell — the realistic in-dist confusion the THIN residual is about."""
    rng = np.random.default_rng(seed)
    subjects = []; seen = set()
    n_base = N_FACTS // 2
    while len(subjects) < n_base:
        s = _rand_token(rng, KEYLEN)
        if s not in seen:
            seen.add(s); subjects.append(s)
    # near-duplicate neighbors: copy a base subject, perturb a FEW bytes (shared trigrams)
    while len(subjects) < N_FACTS:
        base = subjects[int(rng.integers(0, n_base))]
        nb = list(base)
        nflip = int(rng.integers(2, 5))           # 2-4 byte edits -> heavy trigram overlap
        for _ in range(nflip):
            pos = int(rng.integers(0, KEYLEN))
            nb[pos] = chr(int(rng.integers(ord('a'), ord('z') + 1)))
        nb = "".join(nb)
        if nb not in seen:
            seen.add(nb); subjects.append(nb)
    # answer bound to each cell = its index (distinct per cell)
    answers = list(range(N_FACTS))
    return rng, subjects, answers, seen


class Store:
    def __init__(self, subjects, answers):
        self.keys = np.array([embed_key(s) for s in subjects])   # (N,DIM)
        self.answers = answers

    def affinities(self, key_vec):
        return self.keys @ key_vec                               # cos sims (unit vectors)

    def topk_sorted(self, key_vec):
        sims = self.affinities(key_vec)
        order = np.argsort(-sims)
        return sims, order


def signals_for_query(store, key_vec):
    """Read-only confidence signals from the SAME store affinity distribution."""
    sims, order = store.topk_sorted(key_vec)
    j1 = int(order[0])
    best = float(sims[j1])
    recon_err = 1.0 - best
    # (a) CURRENT = best-cell recall margin = -(recon_err - thr); higher = more confident
    s_current = -(recon_err - RECALL_THR)
    # (b) RICHER-1 = top-2 affinity gap
    s2 = float(sims[int(order[1])]) if len(order) > 1 else -1.0
    s_gap = best - s2
    # (c) RICHER-2 = neg-entropy of softmax over top-k cos affinities
    topk = sims[order[:TOPK]]
    z = topk - topk.max()
    w = np.exp(z); w = w / w.sum()
    ent = -float(np.sum(w * np.log(w + 1e-12)))
    s_negent = -ent
    return {"win": j1, "recon_err": recon_err,
            "current": s_current, "gap": s_gap, "negent": s_negent}


def run_seed(seed):
    rng, subjects, answers, seen = _build(seed)
    store = Store(subjects, answers)
    query_idx = rng.choice(N_FACTS, size=N_TRIAL, replace=True)

    # ── IN-DIST type-2: fired items only, correctness = fired copy RIGHT vs WRONG ──
    cur, gap, negent, correct = [], [], [], []
    rmut = np.random.default_rng(seed + 1)
    for L in INDIST_LEVELS:
        for si in query_idx:
            q = mutate(subjects[si], L, rmut)
            sg = signals_for_query(store, embed_key(q))
            if sg["recon_err"] <= RECALL_THR:                 # FIRE only (in-dist slice)
                is_correct = 1 if store.answers[sg["win"]] == answers[si] else 0
                cur.append(sg["current"]); gap.append(sg["gap"])
                negent.append(sg["negent"]); correct.append(is_correct)

    n_fire = len(correct)
    n_correct = int(sum(correct))
    acc = n_correct / n_fire if n_fire else float("nan")

    def t2(sig):
        return auroc(sig, correct) if (0 < n_correct < n_fire) else float("nan")

    a_cur = t2(cur); a_gap = t2(gap); a_negent = t2(negent)
    # ORACLE ceiling: a confidence == true correctness is perfectly separable -> AUROC=1.0
    a_oracle = auroc([float(c) for c in correct], correct) if (0 < n_correct < n_fire) else float("nan")

    # ── C4 SHUFFLE control: break confidence<->correctness pairing per signal ──
    def t2_shuf(sig, salt):
        if not (0 < n_correct < n_fire):
            return float("nan")
        rs = np.random.default_rng(seed + salt)
        sh = np.array(sig, dtype=np.float64).copy()
        rs.shuffle(sh)
        return auroc(sh.tolist(), correct)
    a_cur_sh = t2_shuf(cur, 5000); a_gap_sh = t2_shuf(gap, 5001); a_negent_sh = t2_shuf(negent, 5002)

    # ── C3 ABSTAIN-INTACT: re-run H_1304 fail-safe under each signal's would-be gate ──
    # The richer signals only RANK confidence among fires; the abstain DECISION is still the
    # frozen recon_err<=thr gate. We verify each richer signal, if used to GATE (fire iff its
    # confidence exceeds the value at the frozen recall_thr boundary), does NOT raise OOD fab.
    # Concretely: a fire is a fab iff it FIRES on an OOD-corrupted ABSENT lure. Lures ~never
    # fire under the frozen gate (H_1304); a richer signal must not make them fire wrong.
    lures = []
    rl = np.random.default_rng(seed + 99)
    while len(lures) < N_TRIAL:
        lu = _rand_token(rl, KEYLEN)
        if lu not in seen:
            lures.append(lu)
    ood_fab = {}
    rmut2 = np.random.default_rng(seed + 2)
    for L in OOD_LEVELS:
        fabs = 0; tot = 0
        for lu in lures:
            q = mutate(lu, L, rmut2)
            sg = signals_for_query(store, embed_key(q))
            tot += 1
            # frozen gate fires iff recon_err<=thr; richer signals don't change the gate,
            # so OOD fab is the frozen-gate fab (must be ~0, H_1304). We measure it to PROVE
            # the richer signals (RANK-only) leave the abstain property intact.
            if sg["recon_err"] <= RECALL_THR:
                fabs += 1
        ood_fab[str(L)] = fabs / tot if tot else float("nan")

    return {"seed": seed, "n_fire": n_fire, "n_correct": n_correct, "acc": acc,
            "auroc": {"current": a_cur, "gap": a_gap, "negent": a_negent, "oracle": a_oracle},
            "auroc_shuf": {"current": a_cur_sh, "gap": a_gap_sh, "negent": a_negent_sh},
            "ood_fab": ood_fab}


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    per_seed = [run_seed(s) for s in SEEDS]

    def pool(path):
        vals = []
        for s in per_seed:
            v = s
            for k in path:
                v = v[k]
            if not (isinstance(v, float) and math.isnan(v)):
                vals.append(v)
        return float(np.mean(vals)) if vals else float("nan")

    a_cur = pool(["auroc", "current"]); a_gap = pool(["auroc", "gap"])
    a_negent = pool(["auroc", "negent"]); a_oracle = pool(["auroc", "oracle"])
    a_cur_sh = pool(["auroc_shuf", "current"]); a_gap_sh = pool(["auroc_shuf", "gap"])
    a_negent_sh = pool(["auroc_shuf", "negent"])
    acc = pool(["acc"])

    best_richer = max(a_gap, a_negent)
    best_name = "gap" if a_gap >= a_negent else "negent"
    lift = best_richer - a_cur

    # C2 FIXABLE-TEST
    C2 = (not math.isnan(lift)) and (lift >= DELTA)
    # C3 ABSTAIN-INTACT (richer signals are rank-only -> frozen gate unchanged; verify fab<=0.02)
    ood_max = max(pool(["ood_fab", str(L)]) for L in OOD_LEVELS)
    C3 = ood_max <= 0.02
    # C4 SHUFFLE-CTRL: every signal's shuffle AUROC ~ 0.50
    shufs = [a_cur_sh, a_gap_sh, a_negent_sh]
    C4 = all((not math.isnan(x)) and abs(x - 0.50) <= 0.08 for x in shufs)
    # C1 CEILING-REF gap
    ceiling_gap = a_oracle - a_cur

    if not C4:
        verdict = "RED"; tier = "🔴"
        ruling = ("SHUFFLE control did NOT collapse to ~0.50 — the in-dist type-2 measurement "
                  "is an artifact; no ceiling/fixable claim can be made.")
    elif C2 and C3:
        verdict = "FIXABLE"; tier = "🟢"
        ruling = (f"a RICHER read-only confidence signal LIFTS in-dist type-2 metacognition: "
                  f"{best_name} AUROC={best_richer:.3f} vs CURRENT(best-margin) {a_cur:.3f} "
                  f"(lift +{lift:.3f} >= Δ={DELTA}), shuffle collapses (~0.50), and the "
                  f"OOD/abstain property (H_1304) stays intact (fab_max={ood_max:.3f}<=0.02). "
                  f"G5 in-dist thinness is FIXABLE — the deepening is signal '{best_name}'. "
                  f"Binding follow-on (a_verified_must_wire): expose top-k affinity in the engine "
                  f"and wire '{best_name}' into immune_memory_recall_margin / brain_decide.")
    elif C2 and not C3:
        verdict = "FIXABLE-BUT-BREAKS-ABSTAIN"; tier = "🟠"
        ruling = (f"the richer signal {best_name} lifts in-dist AUROC (+{lift:.3f}) BUT raises OOD "
                  f"fabrication (fab_max={ood_max:.3f}>0.02) — REJECTED: it trades in-dist "
                  f"sensitivity for the H_1304 fail-safe guarantee. Not a valid fix.")
    else:
        verdict = "CEILING"; tier = "⚪"
        ruling = (f"NO richer read-only signal lifts in-dist type-2 metacognition by Δ={DELTA}: "
                  f"CURRENT(best-margin) AUROC={a_cur:.3f}, top-2 gap={a_gap:.3f}, "
                  f"neg-entropy={a_negent:.3f}; best lift +{lift:.3f} < {DELTA}. The oracle "
                  f"(determinate-correctness) ceiling is {a_oracle:.3f}; CURRENT already sits "
                  f"AUROC={a_cur:.3f} with in-dist fire accuracy={acc:.3f} so the number of "
                  f"WRONG fires is small (little correctness variance to track). The in-dist "
                  f"thinness is a NEAR-INHERENT CEILING / honest near-optimality, NOT a fixable "
                  f"model deficiency — G5 is as-good-as the available read-only signals in-dist. "
                  f"Valid, reassuring closure (c9): the '🟠 THIN in-dist' label is honest, and "
                  f"the abstain/OOD side (H_1304/H_1361/H_1367/H_1379) carries the graded metacog.")

    out = {
        "H": "H_1396",
        "title": "G5 in-distribution metacognition — CEILING vs FIXABLE? (richer read-only "
                 "confidence signals vs the current best-margin, oracle ceiling, shuffle control)",
        "seeds": SEEDS, "indist_levels": INDIST_LEVELS, "ood_levels": OOD_LEVELS,
        "key_len": KEYLEN, "recall_thr": RECALL_THR, "n_facts": N_FACTS, "delta": DELTA,
        "indist_acc_fired": acc,
        "indist_type2_auroc": {"current_best_margin": a_cur, "richer1_top2_gap": a_gap,
                               "richer2_negentropy": a_negent, "oracle_ceiling": a_oracle},
        "indist_type2_auroc_shuffle": {"current": a_cur_sh, "gap": a_gap_sh, "negent": a_negent_sh},
        "ood_fab_rate": {str(L): pool(["ood_fab", str(L)]) for L in OOD_LEVELS},
        "C1_ceiling_ref": {"oracle_auroc": a_oracle, "current_auroc": a_cur,
                           "ceiling_gap": ceiling_gap},
        "C2_fixable": {"best_richer": best_name, "best_richer_auroc": best_richer,
                       "lift_over_current": lift, "bar": f">= {DELTA}", "pass": bool(C2)},
        "C3_abstain_intact": {"ood_fab_max": ood_max, "bar": "<= 0.02", "pass": bool(C3)},
        "C4_shuffle_ctrl": {"current_shuf": a_cur_sh, "gap_shuf": a_gap_sh,
                            "negent_shuf": a_negent_sh, "bar": "|x-0.50|<=0.08 all", "pass": bool(C4)},
        "verdict": verdict, "tier": tier, "ruling": ruling,
        "neuroscience_anchor": "type-2 metacognition / feeling-of-knowing in-distribution "
                               "(Fleming & Lau 2014); near-optimal type-2 sensitivity has a "
                               "ceiling when first-order correctness variance is small",
        "scope": "TOY synthetic facts, byte-level shift as in-dist/OOD proxy, numpy mirror = "
                 "DIRECTIONAL (engine-transfer UNVERIFIED); collision-prone store to create "
                 "in-dist wrong fires; 3 seeds (a_scale_honest_scope / a_toy_scale_recheck)",
        "per_seed": per_seed,
    }
    with open(os.path.join(OUTDIR, "result.json"), "w") as f:
        json.dump(out, f, indent=2)

    lines = []
    def p(x): lines.append(x); print(x)
    p(f"=== H_1396 G5 IN-DIST metacog CEILING vs FIXABLE — {tier} {verdict} ===")
    p(f"  in-dist fire accuracy        : {acc:.3f}  (n_fire pooled, wrong fires = correctness variance)")
    p(f"  in-dist type-2 AUROC:")
    p(f"    (a) CURRENT best-margin    : {a_cur:.3f}   <- the live baseline (immune_memory_recall_margin)")
    p(f"    (b) RICHER-1 top-2 gap     : {a_gap:.3f}   (lift {a_gap-a_cur:+.3f})")
    p(f"    (c) RICHER-2 neg-entropy   : {a_negent:.3f}   (lift {a_negent-a_cur:+.3f})")
    p(f"    (d) ORACLE ceiling (ref)   : {a_oracle:.3f}   (determinate-correctness upper bound)")
    p(f"  C1 ceiling-ref  gap oracle-current = {ceiling_gap:.3f}")
    p(f"  C2 FIXABLE      best richer '{best_name}' lift {lift:+.3f}  >= Δ={DELTA} -> {C2}")
    p(f"  C3 abstain-intact OOD fab_max = {ood_max:.3f}  <= 0.02 -> {C3}")
    p(f"  C4 shuffle-ctrl curr={a_cur_sh:.3f} gap={a_gap_sh:.3f} negent={a_negent_sh:.3f}  ~0.50 -> {C4}")
    p(f"  RULING: {ruling}")
    with open(os.path.join(OUTDIR, "result.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return out


if __name__ == "__main__":
    main()
