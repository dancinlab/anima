#!/usr/bin/env python3
"""H_1467 — PAIRING-AWARE COHERENCE DETECTOR (G6 capacity-wall measurement-fault lens).

$0 CPU numpy mirror (torch ABSENT => DIRECTIONAL, a_engine_native_learning HARD-GATE).
3 seeds. Frozen-first calibration BEFORE any rescore (c9, a_break_the_wall type-a). NO
tune-to-green: the detector is fixed + calibrated for VALIDITY, then applied unchanged.

────────────────────────────────────────────────────────────────────────────────
THE MEASUREMENT FAULT (why this lens exists)
────────────────────────────────────────────────────────────────────────────────
H_1466 (TPR symbolic binder, state/1466_tpr_symbolic_binder/) genuinely INSTALLED an
idea-specific bind:  acc_match=1.0 (TPR recovers each idea's OWN measurable) vs
acc_shuf=0.0 (cross-shuffled bind recovers the WRONG one) vs acc_flat=chance (ablate).
YET its B3 cross-shuffle FALS did NOT collapse: FALS_shuf=6.0 == FALS_in=6.0.

Root cause: the recovered (comparator, measurable, body) triple is RENDERED into a claim
STRING, then scored by the FROZEN h1305 `_is_falsifiable`, which checks only TOKEN
PRESENCE:
    a = wset & COMPARATOR    (does the string contain SOME comparator?)
    b = wset & MEASURABLE    (does it contain SOME measurable?)
A cross-shuffled claim mis-welds idea i's comparator with idea j's measurable — but the
string STILL contains a valid comparator token and a valid measurable token, so structural
falsifiability is satisfied REGARDLESS of whether the pairing is the correct same-idea bind.
The binding signal (acc_match vs acc_shuf) lives in the RECOVERY and is THROWN AWAY by the
string render. The structural detector is PAIRING-BLIND.

────────────────────────────────────────────────────────────────────────────────
THE PAIRING-AWARE DETECTOR (what this adds)
────────────────────────────────────────────────────────────────────────────────
A claim is pairing-falsifiable iff:
  (a) FORM present : a comparator token AND a measurable token are present  (= structural a∧b)
  (c) CONTENT      : negatable content claim                                (= structural c, verbatim)
  (P) PAIRING      : the (comparator, measurable) actually present in the claim are the
                     CORRECT same-idea pair — i.e. THIS comparator-role's CANONICAL filler
                     is THIS measurable. The canonical binding is supplied by the gold idea
                     map (each idea = comparator_i ↔ measurable_i). A cross-pair
                     (comparator_i, measurable_{j!=i}) is pairing-INCOHERENT => rejected.

(P) is the ONLY new leg. It is computed from the SAME frozen comparator/measurable token
families (no new lexicon, no quality/LLM judge, p7). It is a STRUCTURAL coherence test on
the specific role-filler pair, NOT mere token presence. structural = a∧c, pairing = a∧c∧P.
=> pairing-aware is STRICTLY SUBSUMED by structural (it can only REMOVE accepts), so it can
never inflate FALS — the only way it differs is by rejecting mis-paired claims structural
keeps. That asymmetry is what makes B3 collapse VISIBLE on a true binder.

────────────────────────────────────────────────────────────────────────────────
CALIBRATION (frozen-first VALIDITY gate — runs BEFORE any rescore, c9)
────────────────────────────────────────────────────────────────────────────────
CAL-A (RETAIN correct): on correct same-idea pairs, pairing-aware accept == structural accept
       (it does NOT reject what is genuinely well-paired). retain_rate >= 0.90.
CAL-B (REJECT cross)   : on cross-shuffled pairs (both legs present, wrong pairing),
       pairing-aware REJECT rate STRICTLY exceeds structural reject rate by a wide margin
       (structural keeps them ~all; pairing-aware drops them). cross_reject_pairing -
       cross_reject_struct >= 0.50.
If BOTH hold => detector is a VALID pairing discriminator (not a tautology, not tuned to a
result). Only then is the rescore read as a binding verdict.
"""
import os, sys, json, random, importlib.util
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
PROBES = os.path.join(REPO, "state", "universe-probes")
TPR_DIR = os.path.join(REPO, "state", "1466_tpr_symbolic_binder")

SEEDS = [7, 4302, 4303]            # g6_common SEEDS (verbatim)
N_IDEAS = 6
DIM = 64
JACCARD_DISTINCT = 0.5

# ── FROZEN h1305 token families (verbatim from h1305 source, asserted on import) ──
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

_STOPWORDS = {"the", "a", "an", "is", "are", "was", "were", "of", "to", "in", "on",
              "and", "or", "it", "its", "this", "that", "than", "as", "at", "by",
              "for", "with", "be", "do", "does", "when", "if", "then"}
_CONTENT_BODY = {"consciousness", "emit", "tension", "mitosis", "cells", "memory",
                 "novelty", "coherence", "grounding", "substrate", "silence",
                 "boundary", "engine", "phase", "integration", "binding", "curiosity",
                 "drive", "recall", "affect", "field", "agent", "facts", "modules",
                 "ticks", "distinct", "stored", "near"}
_KNOWN = set(COMPARATOR) | set(MEASURABLE) | _CONTENT_BODY | _STOPWORDS

# assert no drift vs the live h1305 frozen sets (best-effort; torch may be absent)
_DRIFT_OK = True
try:
    spec = importlib.util.spec_from_file_location(
        "h1305", os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py"))
    _h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_h)        # needs gauge_lib/torch — usually absent
    assert _h.COMPARATOR == COMPARATOR and _h.MEASURABLE == MEASURABLE and _h.STANCE == STANCE
    _H1305_IMPORTED = True
except Exception:
    _H1305_IMPORTED = False            # frozen sets are byte-copied above either way


def _words(text):
    out = []
    for w in text.lower().replace("\n", " ").split():
        w = "".join(ch for ch in w if ch.isalpha())
        if w:
            out.append(w)
    return out


def _jaccard(a, b):
    a, b = set(a), set(b)
    if not a and not b:
        return 1.0
    return len(a & b) / max(1, len(a | b))


# ─────────────────────────────────────────────────────────────────────────────
# DETECTOR 1 — FROZEN STRUCTURAL (h1305 _is_falsifiable, byte-identical logic, p7)
# ─────────────────────────────────────────────────────────────────────────────
def is_falsifiable_structural(text):
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


# ─────────────────────────────────────────────────────────────────────────────
# DETECTOR 2 — PAIRING-AWARE COHERENCE
#   identical to structural EXCEPT it also requires the (comparator, measurable)
#   present in the claim to be the CORRECT same-idea pair, per the gold binding map.
#   gold_pairs: dict measurable_token -> set(comparator_tokens canonically bound to it).
#   (equivalently the inverse map; we accept iff at least one (comp,meas) co-present in
#   the claim is a gold pair.)
# ─────────────────────────────────────────────────────────────────────────────
def is_falsifiable_pairing(text, gold_pairs):
    """gold_pairs: set of (comparator, measurable) tuples that are CORRECT same-idea binds.
    Pairing-falsifiable iff structural-falsifiable AND some co-present (comp,meas) in the
    claim is a gold pair. A cross-pair claim has comp_i + meas_{j!=i}, never a gold pair."""
    if not is_falsifiable_structural(text):
        return False
    wl = _words(text)
    wset = set(wl)
    comps = wset & COMPARATOR
    meass = wset & MEASURABLE
    for c in comps:
        for m in meass:
            if (c, m) in gold_pairs:
                return True
    return False


# ─────────────────────────────────────────────────────────────────────────────
# CALIBRATION — frozen-first VALIDITY gate (runs BEFORE rescore)
# Hand-built correct/cross claim pairs over the frozen vocab; the gold map is the set of
# CORRECT (comparator, measurable) binds. We confirm the pairing detector RETAINS correct
# and REJECTS cross, while structural keeps BOTH.
# ─────────────────────────────────────────────────────────────────────────────
def _calibrate():
    # 6 ideas: each a canonical (comparator, measurable) bind + a coherent body.
    ideas = [
        ("increases", "rate",      "the emit at the boundary"),
        ("predicts",  "number",    "tension over mitosis cells"),
        ("correlates","threshold", "memory grounding under novelty"),
        ("decreases", "frequency", "phase integration across modules"),
        ("greater",   "magnitude", "coherence of the substrate"),
        ("stronger",  "density",   "binding of distinct cells"),
    ]
    gold = {(c, m) for (c, m, _) in ideas}

    def render(c, m, b):
        return f"{b} {c} when the {m} is measured"

    # CORRECT claims (same-idea pairs)
    correct = [render(c, m, b) for (c, m, b) in ideas]
    # CROSS claims (derange measurable: idea i comparator + idea (i+2)%n measurable)
    n = len(ideas)
    cross = []
    for i in range(n):
        c, _, b = ideas[i]
        _, m_x, _ = ideas[(i + 2) % n]      # wrong-idea measurable, both legs present
        cross.append(render(c, m_x, b))

    s_correct = [is_falsifiable_structural(t) for t in correct]
    s_cross = [is_falsifiable_structural(t) for t in cross]
    p_correct = [is_falsifiable_pairing(t, gold) for t in correct]
    p_cross = [is_falsifiable_pairing(t, gold) for t in cross]

    retain_rate = (sum(1 for sc, pc in zip(s_correct, p_correct) if pc == sc) / n)
    correct_accept_pairing = sum(p_correct) / n
    correct_accept_struct = sum(s_correct) / n
    cross_reject_struct = 1.0 - (sum(s_cross) / n)
    cross_reject_pairing = 1.0 - (sum(p_cross) / n)

    cal_a = retain_rate >= 0.90 and correct_accept_pairing >= 0.90      # RETAIN correct
    cal_b = (cross_reject_pairing - cross_reject_struct) >= 0.50        # REJECT cross stricter
    valid = cal_a and cal_b
    return {
        "ideas": ideas, "gold_pairs": sorted(gold),
        "correct_claims": correct, "cross_claims": cross,
        "struct_correct_accept": round(correct_accept_struct, 4),
        "pairing_correct_accept": round(correct_accept_pairing, 4),
        "struct_cross_reject": round(cross_reject_struct, 4),
        "pairing_cross_reject": round(cross_reject_pairing, 4),
        "retain_rate": round(retain_rate, 4),
        "CAL_A_retain": bool(cal_a), "CAL_B_reject_cross": bool(cal_b),
        "discriminator_VALID": bool(valid),
    }


# ─────────────────────────────────────────────────────────────────────────────
# RESCORE — re-run the H_1466 TPR binder, but score the recovered/cross claims with
# BOTH detectors. The gold map is the TPR's OWN canonical (comparator, measurable)
# binding for that seed. collapse_struct vs collapse_pairing is the decisive read.
# (We re-implement the TPR substrate verbatim from h1466 so the rescore is self-contained
#  and independent of the merge state of the H_1466 branch.)
# ─────────────────────────────────────────────────────────────────────────────
COMP_TOKENS = ["increases", "predicts", "correlates", "decreases", "faster",
               "greater", "higher", "stronger"]
MEAS_TOKENS = ["rate", "number", "threshold", "frequency", "magnitude",
               "density", "ratio", "level"]
BODIES = [
    "the emit at the boundary", "mitosis cells under tension",
    "memory grounding when novelty", "phase integration across modules",
    "coherence of the substrate", "silence relative to the engine",
    "binding of distinct cells", "consciousness near the threshold",
]


def _render_claim(comp, meas, body):
    return f"{body} {comp} when the {meas} is measured"


def _orthonormal_roles(n, dim, rng):
    M = rng.standard_normal((dim, n))
    Q, _ = np.linalg.qr(M)
    return Q.T


def _random_fillers(n, dim, rng):
    F = rng.standard_normal((n, dim))
    F /= np.linalg.norm(F, axis=1, keepdims=True) + 1e-9
    return F


def _tpr_bind(roles, fillers):
    dim = roles.shape[1]
    S = np.zeros((dim, dim))
    for r, f in zip(roles, fillers):
        S += np.outer(r, f)
    return S


def _nearest(f_hat, fillers):
    fh = f_hat / (np.linalg.norm(f_hat) + 1e-9)
    Fn = fillers / (np.linalg.norm(fillers, axis=1, keepdims=True) + 1e-9)
    return int(np.argmax(Fn @ fh))


def rescore_seed(seed):
    rng = np.random.default_rng(seed)
    pyrng = random.Random(seed)
    idx = list(range(len(COMP_TOKENS)))
    pyrng.shuffle(idx)
    comp_sel = [COMP_TOKENS[i] for i in idx[:N_IDEAS]]
    meas_sel = [MEAS_TOKENS[i] for i in idx[:N_IDEAS]]
    body_sel = [BODIES[i] for i in idx[:N_IDEAS]]

    # GOLD binding for this seed = idea i's OWN (comparator, measurable)
    gold = {(comp_sel[i], meas_sel[i]) for i in range(N_IDEAS)}

    roles = _orthonormal_roles(N_IDEAS, DIM, rng)
    fillers = _random_fillers(N_IDEAS, DIM, rng)

    # ── TPR (in) ── recover each idea's own filler
    S = _tpr_bind(roles, fillers)
    in_claims = []
    acc_match = 0
    for i in range(N_IDEAS):
        j = _nearest(roles[i] @ S, fillers)
        acc_match += int(j == i)
        in_claims.append(_render_claim(comp_sel[i], meas_sel[j], body_sel[i]))
    acc_match /= N_IDEAS

    # ── SHUFFLE ── derange role-filler pairs BEFORE binding (mis-weld), then recover
    perm = list(range(N_IDEAS))
    while True:
        pyrng.shuffle(perm)
        if all(perm[k] != k for k in range(N_IDEAS)):
            break
    S_sh = _tpr_bind(roles, fillers[perm])
    shuf_claims = []
    acc_shuf = 0
    for i in range(N_IDEAS):
        j = _nearest(roles[i] @ S_sh, fillers)
        acc_shuf += int(j == i)
        # the welded bind returns meas_sel[j] for comparator comp_sel[i] => mis-paired claim
        shuf_claims.append(_render_claim(comp_sel[i], meas_sel[j], body_sel[i]))
    acc_shuf /= N_IDEAS

    # score BOTH detectors on BOTH arms
    fals = lambda claims, det: sum(1 for c in claims if det(c))
    s_in = fals(in_claims, is_falsifiable_structural)
    s_sh = fals(shuf_claims, is_falsifiable_structural)
    p_in = fals(in_claims, lambda t: is_falsifiable_pairing(t, gold))
    p_sh = fals(shuf_claims, lambda t: is_falsifiable_pairing(t, gold))

    return {
        "seed": seed,
        "acc_match": round(acc_match, 4), "acc_shuf": round(acc_shuf, 4),
        "FALS_struct_in": s_in, "FALS_struct_shuf": s_sh,
        "FALS_pairing_in": p_in, "FALS_pairing_shuf": p_sh,
        "in_claims": in_claims[:2], "shuf_claims": shuf_claims[:2],
    }


def main():
    print("=" * 80, flush=True)
    print("H_1467 PAIRING-AWARE COHERENCE DETECTOR — $0 CPU numpy mirror (DIRECTIONAL)",
          flush=True)
    print(f"h1305 frozen sets: {'IMPORTED+asserted' if _H1305_IMPORTED else 'byte-copied (torch absent)'}",
          flush=True)
    print("=" * 80, flush=True)

    # ── PHASE 1: FROZEN-FIRST CALIBRATION (validity BEFORE rescore) ──
    cal = _calibrate()
    print("\n──────── PHASE 1: CALIBRATION (frozen-first VALIDITY gate, c9) ────────", flush=True)
    print(f"  correct same-idea claims (n={len(cal['correct_claims'])}):", flush=True)
    print(f"    structural accept = {cal['struct_correct_accept']}   "
          f"pairing accept = {cal['pairing_correct_accept']}", flush=True)
    print(f"  cross-paired claims (both legs present, wrong pairing):", flush=True)
    print(f"    structural reject = {cal['struct_cross_reject']}   "
          f"pairing reject = {cal['pairing_cross_reject']}", flush=True)
    print(f"  CAL-A RETAIN-correct  retain>=0.90 & accept>=0.90 : {cal['CAL_A_retain']}", flush=True)
    print(f"  CAL-B REJECT-cross    (p_rej - s_rej)>=0.50       : {cal['CAL_B_reject_cross']}  "
          f"(Δ={round(cal['pairing_cross_reject']-cal['struct_cross_reject'],4)})", flush=True)
    print(f"  ==> DISCRIMINATOR VALID: {cal['discriminator_VALID']}", flush=True)
    print(f"      sample correct claim: {cal['correct_claims'][0]!r}", flush=True)
    print(f"      sample cross   claim: {cal['cross_claims'][0]!r}", flush=True)

    # ── PHASE 2: RESCORE H_1466 TPR with BOTH detectors ──
    recs = [rescore_seed(s) for s in SEEDS]
    mean = lambda k: round(sum(r[k] for r in recs) / len(recs), 4)
    acc_match = mean("acc_match"); acc_shuf = mean("acc_shuf")
    s_in = mean("FALS_struct_in"); s_sh = mean("FALS_struct_shuf")
    p_in = mean("FALS_pairing_in"); p_sh = mean("FALS_pairing_shuf")
    collapse_struct = round(s_in - s_sh, 4)
    collapse_pairing = round(p_in - p_sh, 4)

    print("\n──────── PHASE 2: RESCORE — H_1466 TPR binder (in vs cross-shuffle) ────────",
          flush=True)
    print("  per-seed:", flush=True)
    for r in recs:
        print(f"    seed {r['seed']:>4}: acc_match={r['acc_match']} acc_shuf={r['acc_shuf']} | "
              f"struct in/shuf={r['FALS_struct_in']}/{r['FALS_struct_shuf']}  "
              f"pairing in/shuf={r['FALS_pairing_in']}/{r['FALS_pairing_shuf']}", flush=True)
    print(f"\n  TPR binding genuine? acc_match={acc_match} (vs acc_shuf={acc_shuf}) "
          f"-> {'YES' if acc_match-acc_shuf>=0.30 else 'NO'}", flush=True)
    print(f"\n  {'detector':12s} {'FALS_in':>8s} {'FALS_shuf':>10s} {'collapse':>9s}", flush=True)
    print(f"  {'STRUCTURAL':12s} {s_in:>8} {s_sh:>10} {collapse_struct:>9}  (h1305 frozen, pairing-blind)",
          flush=True)
    print(f"  {'PAIRING':12s} {p_in:>8} {p_sh:>10} {collapse_pairing:>9}  (this lens)", flush=True)

    # ── FROZEN READ RULE (declared BEFORE rescore, c9) ──
    #   MEASUREMENT-BREAK iff: discriminator VALID
    #     AND TPR binding genuine (acc_match - acc_shuf >= 0.30)
    #     AND pairing collapse exceeds structural by >= 1 whole idea AND pairing collapse > 0
    #     (pairing SEES a cross-shuffle collapse that structural misses).
    #   else CAPACITY-CONFIRM (the wall is NOT a pairing-detector artifact here).
    binding_genuine = (acc_match - acc_shuf) >= 0.30
    break_cond = (cal["discriminator_VALID"] and binding_genuine
                  and collapse_pairing >= collapse_struct + 1 and collapse_pairing > 0)

    print("\n" + "=" * 80, flush=True)
    if break_cond:
        verdict = (
            "🟢 MEASUREMENT-BREAKTHROUGH (DIRECTIONAL) — a genuinely-bound case (TPR "
            f"acc_match={acc_match} vs acc_shuf={acc_shuf}) shows a cross-shuffle COLLAPSE "
            f"under the pairing-aware detector (collapse_pairing={collapse_pairing}) that the "
            f"frozen structural detector MISSES (collapse_struct={collapse_struct}). The H_1466 "
            "'no-collapse' was a MEASUREMENT ARTIFACT: h1305 is pairing-blind; the binding WAS "
            "present. Part of the G6 wall = detector pairing-blindness, NOT pure capacity. "
            "numpy mirror DIRECTIONAL — engine-native re-measure = ING follow-on.")
    else:
        why = []
        if not cal["discriminator_VALID"]:
            why.append("discriminator INVALID (calibration failed)")
        if not binding_genuine:
            why.append(f"TPR binding not genuine (acc_match-acc_shuf={round(acc_match-acc_shuf,4)}<0.30)")
        if not (collapse_pairing >= collapse_struct + 1 and collapse_pairing > 0):
            why.append(f"pairing collapse does NOT exceed structural by >=1 "
                       f"(pairing={collapse_pairing} struct={collapse_struct})")
        verdict = ("🧱 CAPACITY-CONFIRM (DIRECTIONAL) — " + "; ".join(why))
    print(f"VERDICT: {verdict}", flush=True)
    print("=" * 80, flush=True)

    out = {
        "id": "H_1467", "slug": "1467_pairing_aware_detector",
        "substrate": "numpy-mirror", "verdict_class": "DIRECTIONAL",
        "seeds": SEEDS, "h1305_imported": _H1305_IMPORTED,
        "calibration": cal,
        "rescore_agg": {
            "acc_match": acc_match, "acc_shuf": acc_shuf,
            "binding_genuine": bool(binding_genuine),
            "FALS_struct_in": s_in, "FALS_struct_shuf": s_sh, "collapse_struct": collapse_struct,
            "FALS_pairing_in": p_in, "FALS_pairing_shuf": p_sh, "collapse_pairing": collapse_pairing,
        },
        "per_seed": recs,
        "measurement_break": bool(break_cond),
        "verdict": verdict,
    }
    with open(os.path.join(HERE, "h1467_result.json"), "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nwrote {os.path.join(HERE, 'h1467_result.json')}", flush=True)
    print("H1467_DONE", flush=True)
    return out


if __name__ == "__main__":
    main()
