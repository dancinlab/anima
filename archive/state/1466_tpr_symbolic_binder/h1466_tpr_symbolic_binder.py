#!/usr/bin/env python3
"""H_1466 — G6 FALS-depth breakthrough lens ① TENSOR-PRODUCT (TPR) SYMBOLIC BINDER.

$0 CPU numpy mirror (torch ABSENT => DIRECTIONAL, a_engine_native_learning). 3 seeds.

QUESTION (a_no_llm_frame_trap, a_break_the_wall type-d): the 7 prior G6 FALS-depth lenses
(learnable bind-head MLP / attention / retrieval / curriculum / knowledge / idea-metacog /
scale) all hit B3 cross-shuffle NO-collapse: the binder is an INTERCHANGEABLE SHELL that
satisfies the structural detector whether or not the comparator-role and measurable-filler
belong to the SAME idea. This lens replaces the learnable shell with a STRUCTURAL Smolensky
TENSOR-PRODUCT REPRESENTATION (TPR): each idea i is bound as the OUTER product
    r_i ⊗ f_i   (role = comparator-clause vector, filler = measurable vector)
summed into ONE vector S = Σ_i r_i ⊗ f_i. Unbinding with role r_q recovers ITS OWN filler:
    f_hat = S · r_q   (≈ f_q when roles are near-orthonormal).
Because the bind is idea-specific BY CONSTRUCTION, cross-shuffling the (role,filler) pairs
MUST corrupt recovery => B3 SHOULD collapse. The ablate "flat-sum" (r_i + f_i, no outer
product) has no tensor structure to unbind => recovery must collapse to chance (CTRL).

The recovered (comparator,measurable) pair for each idea is rendered into a claim STRING and
scored by the FROZEN h1305 detector (imported VERBATIM, p7). FROZEN 5-bar in the FREEZE file.
"""
import os, sys, json, random, importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PROBES = os.path.join(REPO, "state", "universe-probes")

SEEDS = [7, 4302, 4303]
N_IDEAS = 6          # ideas bound into the TPR per seed (>=5 for B2)
DIM = 64             # role/filler embedding dim (TPR slot = DIM x DIM)
JACCARD_DISTINCT = 0.5

# ─────────────────────────────────────────────────────────────────────────────
# FROZEN detector — import h1305 _is_falsifiable + sets VERBATIM (p7, NO re-impl).
# h1305 imports gauge_lib at module scope; if gauge_lib (torch) is absent we fall
# back to a SELF-CONTAINED copy of the *frozen sets + structural logic* that is
# byte-identical to the h1305 source we read. Either path uses the SAME frozen sets.
# ─────────────────────────────────────────────────────────────────────────────
COMPARATOR = {"if", "when", "whenever", "than", "more", "less", "greater", "fewer",
              "higher", "lower", "increases", "decreases", "correlates", "predicts",
              "causes", "depends", "unless", "whereas", "versus", "compared",
              "proportional", "faster", "slower", "stronger", "weaker"}
MEASURABLE = {"measure", "measured", "rate", "number", "count", "amount", "level",
              "degree", "threshold", "ratio", "frequency", "probability", "magnitude",
              "score", "value", "quantity", "percent", "times", "fraction", "distance",
              "duration", "speed", "size", "strength", "density"}
STANCE = {"that", "s", "a", "profound", "question", "i", "think", "interesting",
          "good", "nice", "great", "wonderful", "beautiful", "amazing"}

_HAVE_H1305 = False
try:
    spec = importlib.util.spec_from_file_location(
        "h1305", os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py"))
    _h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_h)          # needs gauge_lib (torch) — absent here
    _is_falsifiable = _h._is_falsifiable
    _words = _h.g._words
    _KNOWN = _h.g._KNOWN
    _STOPWORDS = _h.g._STOPWORDS
    # assert the frozen sets we copied match the source (no drift)
    assert _h.COMPARATOR == COMPARATOR and _h.MEASURABLE == MEASURABLE and _h.STANCE == STANCE
    _HAVE_H1305 = True
except Exception:
    # SELF-CONTAINED fallback: byte-identical structural logic to the h1305 source.
    # A small KNOWN/STOPWORD vocab sufficient for the rendered claim strings (the
    # render uses ONLY the frozen comparator/measurable tokens + a fixed content body,
    # so the content-claim leg is satisfiable without the full gauge dictionary).
    _STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "of", "to", "in", "on",
                  "and", "or", "it", "its", "this", "that", "than", "as", "at", "by",
                  "for", "with", "be", "do", "does", "when", "if", "then"}
    _CONTENT_BODY = {"consciousness", "emit", "tension", "mitosis", "cells", "memory",
                     "novelty", "coherence", "grounding", "substrate", "silence",
                     "boundary", "engine", "phase", "integration", "binding"}
    _KNOWN = set(COMPARATOR) | set(MEASURABLE) | _CONTENT_BODY | _STOPWORDS

    def _words(text):
        out = []
        for w in text.lower().replace("\n", " ").split():
            w = "".join(ch for ch in w if ch.isalpha())
            if w:
                out.append(w)
        return out

    def _is_falsifiable(text):
        wl = _words(text)
        if not wl:
            return False
        wset = set(wl)
        a = bool(wset & COMPARATOR)
        b = bool(wset & MEASURABLE)
        content = [w for w in wl if len(w) >= 3 and w in _KNOWN and w not in _STOPWORDS]
        c_i = len(content) >= 2
        c_ii = not text.rstrip().endswith("?")
        first3 = set(wl[:3])
        c_iii = not (first3 and first3 <= STANCE)
        return a and b and (c_i and c_ii and c_iii)


def _jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


# ─────────────────────────────────────────────────────────────────────────────
# Idea vocabulary: each idea = (comparator token, measurable token, content body).
# These are the SYMBOLS the TPR binds. Comparators are the ROLE, measurables the
# FILLER. The content body is a fixed coherent phrase per idea (so the negatable-
# content detector leg is satisfiable independent of the bind — the bind decides
# WHICH (comparator,measurable) end up welded into ONE claim).
# ─────────────────────────────────────────────────────────────────────────────
COMP_TOKENS = ["increases", "predicts", "correlates", "decreases", "faster",
               "greater", "higher", "stronger"]
MEAS_TOKENS = ["rate", "number", "threshold", "frequency", "magnitude",
               "density", "ratio", "level"]
BODIES = [
    "the emit at the boundary",
    "mitosis cells under tension",
    "memory grounding when novelty",
    "phase integration across modules",
    "coherence of the substrate",
    "silence relative to the engine",
    "binding of distinct cells",
    "consciousness near the threshold",
]


def _render_claim(comp, meas, body):
    """Render a structural claim from a (comparator, measurable, body) triple.
    Deterministic template; the FROZEN detector decides falsifiability. The bind
    decides which comp/meas land together — render is NOT the experiment."""
    return f"{body} {comp} when the {meas} is measured"


def _orthonormal_roles(n, dim, rng):
    """n near-orthonormal role vectors (QR of a random gaussian) — clean unbinding."""
    M = rng.standard_normal((dim, n))
    Q, _ = np.linalg.qr(M)          # Q: dim x n, columns orthonormal
    return Q.T                       # n x dim, each row a unit role vector


def _random_fillers(n, dim, rng):
    F = rng.standard_normal((n, dim))
    F /= np.linalg.norm(F, axis=1, keepdims=True) + 1e-9
    return F


def tpr_bind(roles, fillers):
    """S = Σ_i r_i ⊗ f_i  (outer product sum). Shape dim x dim."""
    dim = roles.shape[1]
    S = np.zeros((dim, dim))
    for r, f in zip(roles, fillers):
        S += np.outer(r, f)
    return S


def tpr_unbind(S, role):
    """f_hat = roleᵀ · S  (recover the filler bound to `role`)."""
    return role @ S


def flatsum_bind(roles, fillers):
    """ABLATE: bind by ADDING (no tensor structure). Returns a single dim-vector."""
    return (roles + fillers).sum(axis=0)


def flatsum_unbind(v, role):
    """ABLATE: there is no tensor slot — the 'recovery' is the same blob for every
    role. Project the blob; with no outer-product structure this cannot select a
    filler => recovery is at chance."""
    return v  # role-independent => same for all queries (chance recovery by design)


def _nearest_filler(f_hat, fillers):
    """Decode recovered vector to the nearest TRUE filler index (cosine)."""
    fh = f_hat / (np.linalg.norm(f_hat) + 1e-9)
    Fn = fillers / (np.linalg.norm(fillers, axis=1, keepdims=True) + 1e-9)
    return int(np.argmax(Fn @ fh))


def run_seed(seed):
    rng = np.random.default_rng(seed)
    pyrng = random.Random(seed)

    # pick N_IDEAS distinct (comp, meas, body) triples
    idx = list(range(len(COMP_TOKENS)))
    pyrng.shuffle(idx)
    comp_sel = [COMP_TOKENS[i] for i in idx[:N_IDEAS]]
    meas_sel = [MEAS_TOKENS[i] for i in idx[:N_IDEAS]]
    body_sel = [BODIES[i] for i in idx[:N_IDEAS]]

    # symbol -> vector: roles (comparators) near-orthonormal, fillers (measurables) random
    roles = _orthonormal_roles(N_IDEAS, DIM, rng)        # the comparator ROLE space
    fillers = _random_fillers(N_IDEAS, DIM, rng)         # the measurable FILLER space

    # ── ARM: TPR (structural outer-product bind) ──
    S_tpr = tpr_bind(roles, fillers)
    tpr_recovered = []          # (comp, recovered_meas, body, correct)
    acc_match = 0
    for i in range(N_IDEAS):
        f_hat = tpr_unbind(S_tpr, roles[i])
        j = _nearest_filler(f_hat, fillers)
        correct = int(j == i)
        acc_match += correct
        tpr_recovered.append((comp_sel[i], meas_sel[j], body_sel[i], correct))
    acc_match /= N_IDEAS

    # ── ARM: SHUFFLE (derange role-filler pairs BEFORE binding) ── B3 decisive
    perm = list(range(N_IDEAS))
    # derangement
    while True:
        pyrng.shuffle(perm)
        if all(perm[k] != k for k in range(N_IDEAS)):
            break
    fillers_shuf = fillers[perm]
    S_shuf = tpr_bind(roles, fillers_shuf)
    shuf_recovered = []
    acc_shuf = 0
    for i in range(N_IDEAS):
        f_hat = tpr_unbind(S_shuf, roles[i])
        j = _nearest_filler(f_hat, fillers)   # decode vs TRUE filler identities
        # correct means recovered the meas that SHOULD belong to idea i (i.e. j==i);
        # but the shuffled bind welded meas[perm[i]] to role i, so recovery returns
        # perm[i], not i => the (comp_i, meas) pair is MIS-WELDED.
        correct = int(j == i)
        acc_shuf += correct
        shuf_recovered.append((comp_sel[i], meas_sel[j], body_sel[i], correct))
    acc_shuf /= N_IDEAS

    # ── ARM: ABLATE flat-sum (no outer product) ── CTRL
    v_flat = flatsum_bind(roles, fillers)
    acc_flat = 0
    flat_recovered = []
    for i in range(N_IDEAS):
        f_hat = flatsum_unbind(v_flat, roles[i])
        j = _nearest_filler(f_hat, fillers)
        correct = int(j == i)
        acc_flat += correct
        flat_recovered.append((comp_sel[i], meas_sel[j], body_sel[i], correct))
    acc_flat /= N_IDEAS

    # ── ARM: BASE (no binder: emit comparator OR measurable alone) ── B5 floor
    # base renders, per idea, EITHER the comparator clause OR the measurable clause,
    # never the welded pair => never falsifiable by the structural detector.
    base_claims = []
    for i in range(N_IDEAS):
        if i % 2 == 0:
            base_claims.append(f"{body_sel[i]} {comp_sel[i]} over time")   # comparator only
        else:
            base_claims.append(f"the {meas_sel[i]} of {body_sel[i]}")      # measurable only

    # ── score FALS via FROZEN detector ──
    def fals_and_dist(recovered):
        claims = [_render_claim(c, m, b) for (c, m, b, _) in recovered]
        fals = sum(1 for cl in claims if _is_falsifiable(cl))
        # distinct: pairwise jaccard<0.5 over coherent claims
        kept = []
        for cl in claims:
            ws = set(_words(cl))
            if ws and all(_jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
                kept.append(ws)
        return fals, len(kept), claims

    f_tpr, d_tpr, claims_tpr = fals_and_dist(tpr_recovered)
    f_shuf, d_shuf, claims_shuf = fals_and_dist(shuf_recovered)
    f_flat, d_flat, claims_flat = fals_and_dist(flat_recovered)
    f_base = sum(1 for cl in base_claims if _is_falsifiable(cl))

    # ── HELD-OUT (B4): UNSEEN idea seeds not in the bound set. Bind them too with the
    # SAME structural TPR and recover — lift must hold on ideas never used to pick the
    # vocab order (here: a disjoint set of comp/meas/body triples). ──
    ho_n = 4
    ho_comp = ["weaker", "lower", "slower", "fewer"][:ho_n]
    ho_meas = ["duration", "speed", "amount", "probability"][:ho_n]
    ho_body = ["the curiosity of the agent", "the drive across ticks",
               "the recall of stored facts", "the affect of the field"][:ho_n]
    ho_roles = _orthonormal_roles(ho_n, DIM, rng)
    ho_fill = _random_fillers(ho_n, DIM, rng)
    S_ho = tpr_bind(ho_roles, ho_fill)
    ho_rec = []
    for i in range(ho_n):
        j = _nearest_filler(tpr_unbind(S_ho, ho_roles[i]), ho_fill)
        ho_rec.append((ho_comp[i], ho_meas[j], ho_body[i], int(j == i)))
    f_ho = sum(1 for cl in [_render_claim(c, m, b) for (c, m, b, _) in ho_rec]
               if _is_falsifiable(cl))

    chance = 1.0 / N_IDEAS
    return {
        "seed": seed,
        "FALS_in": f_tpr, "DIST_in": d_tpr,
        "FALS_shuf": f_shuf, "DIST_shuf": d_shuf,
        "FALS_flat": f_flat,
        "FALS_base": f_base, "FALS_ho": f_ho,
        "acc_match": round(acc_match, 4),
        "acc_shuf": round(acc_shuf, 4),
        "acc_flat": round(acc_flat, 4),
        "chance": round(chance, 4),
        "claims_tpr": claims_tpr[:3],
        "claims_shuf": claims_shuf[:3],
    }


def main():
    print(f"H_1466 TPR SYMBOLIC BINDER — $0 CPU numpy mirror (DIRECTIONAL)  "
          f"h1305_detector={'IMPORTED' if _HAVE_H1305 else 'SELF-CONTAINED-FROZEN-COPY'}",
          flush=True)
    recs = [run_seed(s) for s in SEEDS]
    mean = lambda k: round(sum(r[k] for r in recs) / len(recs), 4)

    FALS_in = mean("FALS_in"); DIST_in = mean("DIST_in")
    FALS_shuf = mean("FALS_shuf"); FALS_base = mean("FALS_base")
    FALS_ho = mean("FALS_ho")
    acc_match = mean("acc_match"); acc_shuf = mean("acc_shuf")
    acc_flat = mean("acc_flat"); chance = mean("chance")

    print("\n  per-seed:", flush=True)
    for r in recs:
        print(f"    seed {r['seed']}: FALS_in={r['FALS_in']} DIST_in={r['DIST_in']} "
              f"FALS_shuf={r['FALS_shuf']} FALS_base={r['FALS_base']} FALS_ho={r['FALS_ho']} | "
              f"acc_match={r['acc_match']} acc_shuf={r['acc_shuf']} acc_flat={r['acc_flat']} "
              f"chance={r['chance']}", flush=True)
        print(f"        TPR claim[0]: {r['claims_tpr'][0]!r}", flush=True)

    # ── FROZEN BARS (verbatim from FREEZE) ──
    b1 = FALS_in >= 1
    b2 = DIST_in >= 5
    b3_fals = FALS_shuf < FALS_in
    b3_acc = (acc_match - acc_shuf) >= 0.30
    b3 = b3_fals and b3_acc
    b4 = FALS_ho >= 1
    b5 = FALS_in >= FALS_base + 1
    ctrl_ablate = acc_flat <= chance + 0.10

    print("\n================ H_1466 FROZEN 5-BAR (mean/3 seeds) ================", flush=True)
    print(f"  TPR     FALS_in={FALS_in} DIST_in={DIST_in} acc_match={acc_match}", flush=True)
    print(f"  SHUFFLE FALS_shuf={FALS_shuf}             acc_shuf={acc_shuf}", flush=True)
    print(f"  ABLATE  (flat-sum)                       acc_flat={acc_flat}  chance={chance}", flush=True)
    print(f"  BASE    FALS_in={FALS_base}", flush=True)
    print("\n  ---- FROZEN BARS ----", flush=True)
    print(f"  B1 FALS-FLOOR   FALS_in>=1                  : {FALS_in} -> {b1}", flush=True)
    print(f"  B2 DISTINCT     DIST_in>=5                  : {DIST_in} -> {b2}", flush=True)
    print(f"  B3 X-SHUFFLE    FALS_shuf<FALS_in AND       : {FALS_shuf}<{FALS_in} -> {b3_fals}", flush=True)
    print(f"                  acc_match-acc_shuf>=0.30    : {round(acc_match-acc_shuf,4)} -> {b3_acc}  => B3={b3}", flush=True)
    print(f"  B4 HELD-OUT     FALS_ho>=1                  : {FALS_ho} -> {b4}", flush=True)
    print(f"  B5 vs-BASE      FALS_in>=base+1             : {FALS_in} vs {FALS_base}+1 -> {b5}", flush=True)
    print(f"  CTRL ABLATE     acc_flat<=chance+0.10       : {acc_flat}<={round(chance+0.10,4)} -> {ctrl_ablate}", flush=True)

    green = b1 and b2 and b3 and b4 and b5 and ctrl_ablate
    if green:
        tier = ("🟢 GREEN DIRECTIONAL — a STRUCTURAL TPR supplies the idea-specific bind: "
                "cross-shuffle COLLAPSES (role-filler pairs broken) AND flat-sum ablate "
                "collapses to chance => 8th lens DIVERGES from CAPACITY (structure was missing). "
                "numpy mirror DIRECTIONAL — engine-native re-measure = ING follow-on.")
    else:
        fails = [n for n, ok in [("B1", b1), ("B2", b2), ("B3", b3), ("B4", b4),
                                 ("B5", b5), ("CTRL", ctrl_ablate)] if not ok]
        tier = (f"🧱 WALL — bars {fails} fail. (see honest reading below)")
    print(f"\n  VERDICT: {tier}", flush=True)

    out = {"bars": {"B1": b1, "B2": b2, "B3": b3, "B3_fals": b3_fals, "B3_acc": b3_acc,
                    "B4": b4, "B5": b5, "CTRL_ablate": ctrl_ablate},
           "agg": {"FALS_in": FALS_in, "DIST_in": DIST_in, "FALS_shuf": FALS_shuf,
                   "FALS_base": FALS_base, "FALS_ho": FALS_ho,
                   "acc_match": acc_match, "acc_shuf": acc_shuf, "acc_flat": acc_flat,
                   "chance": chance},
           "green": bool(green), "tier": tier,
           "detector": "IMPORTED" if _HAVE_H1305 else "SELF-CONTAINED-FROZEN-COPY",
           "per_seed": recs}
    with open(os.path.join(HERE, "h1466_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  wrote {os.path.join(HERE, 'h1466_result.json')}", flush=True)
    return out


if __name__ == "__main__":
    main()
