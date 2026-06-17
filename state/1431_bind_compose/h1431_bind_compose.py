#!/usr/bin/env python3
"""h1431_bind_compose.py — G6 IDEATION ★ depth-floor dig: BIND-compose lane.

HYPOTHESIS H_1431 (a_break_the_wall · H_1397 emit-compose / H_1414 mem×ToM arbiter pattern):
  The H_1314/H_1309 diagnosis is precise: the 303M mouth "produces a COMPARATIVE shape OR a
  MEASURABLE shape but cannot BIND them into one negatable declarative claim — the capacity-
  limited step." Each leg is IN-capacity; the BIND is the wall.

  NEW ANGLE: pull the BIND out of the mouth's INTERNAL generation and into an EXTERNAL
  DETERMINISTIC compose lane (the same move H_1414 made for memory×ToM). The mouth supplies
  two fragments — a RELATION fragment (primed for a comparator) and a MEASURE fragment (primed
  for a measurable/quantity) — each of which is in-capacity. The compose lane deterministically
  WELDS the mouth's OWN comparator token + the mouth's OWN measurable token + the mouth's OWN
  content words into a single declarative negatable claim, which the FROZEN H_1305 detector
  then scores. NO detector token is authored by the lane (NO-FAB audit, p7): comparator and
  measurable MUST be emitted by the mouth.

FROZEN 5-bar (declared in FREEZE.txt BEFORE scoring — c9, NO tune-to-green):
  (1) FALS>=1 cross    : compose ON achieves mean FALS >= 1 (breaks the 0.667 / 0.0 plateau)
  (2) count>=5 distinct: compose ON >= 5 pairwise-Jaccard<0.5 distinct ideas
  (3) shuffle-bind COLLAPSE : pairing comparator-frag with a RANDOM measurable-frag (from a
        different idea) drops FALS below compose-1  (the bind tracks the EARNED pairing, not a
        generic concat that always satisfies the detector)
  (4) ablate-compose INERT  : compose OFF (single flat decode = the H_1314 plateau) returns to
        the ~0.667/0.0 floor (FALS_ablate <= compose-1) — the lane is load-bearing
  (5) NO-FAB           : the p7 token-inject audit is CLEAN — neither the relation/measure
        priming seeds NOR the deterministic weld template contains any frozen COMPARATOR or
        MEASURABLE token; the mouth must EARN every detector-leg token. (corpus concept leak
        => ABORT.)

VERDICT:
  🟢 if (1)&(2) cross the floor AND (3)&(4) controls survive (shuffle collapses, ablate inert).
  🧱 if compose does NOT cross AND ablate==compose (BIND is also capacity-bound = valid result,
     grounds H_1433 7B falsifier).

Reuses the H_1305 frozen `_is_falsifiable` detector VERBATIM (imported, NOT redefined, p7) +
gauge_lib.py decode/evaluators VERBATIM. 3 seeds. 303M torch-mouth via gauge_lib._decode (the
SAME path the live G6 gate uses). DIRECTIONAL R1 (engine-native re-verify = follow-on on GREEN).
"""
import sys, os, json, importlib.util, re, time, random

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(os.path.dirname(HERE))  # state/1431_bind_compose/.. -> state -> root
CKPT = os.environ.get("H1302_CKPT", os.path.join(ANIMA, "state", "chat_303m", "h1129c_chat.pt"))
CORPUS = os.environ.get("H1302_CORPUS", os.path.join(ANIMA, "data", "corpus.txt"))
PROBES = os.path.join(ANIMA, "state", "universe-probes")
GAUGE = os.path.join(PROBES, "gauge_lib.py")
H1129 = os.path.join(PROBES, "h1129_midcap_broad_converged_recombination.py")
H1305 = os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py")

import torch

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

g  = _load("gauge", GAUGE)
h  = _load("h1129", H1129)
h5 = _load("h1305", H1305)

_is_falsifiable = h5._is_falsifiable        # FROZEN H_1305 detector, VERBATIM
_calibrate      = h5._calibrate
COMPARATOR      = h5.COMPARATOR             # frozen detector sets (used for EXTRACTION + audit)
MEASURABLE      = h5.MEASURABLE

JACCARD_DISTINCT = 0.5
KWR_FLOOR        = 0.50
MAX_NEW          = 110           # verify303m_g6.py VERBATIM
SEEDS            = [7, 4302, 4303]
N_IDEAS          = 5

# ── 5 corpus directions (the core noun of each gauge_lib.CONCEPT, 1:1 by index) ──
# The SAME single-noun subjects H_1314 froze (token-clean: the full concept sentence
# "the engine dreams when alone" would inject COMPARATOR 'when' — audited below).
SUBJECTS = ["consciousness", "tension", "memory", "silence", "dreaming"]
assert len(SUBJECTS) == len(g.CONCEPTS)

# ── PRIMING SEEDS (STRUCTURE, not content; NO detector token — audited) ──────────
# RELATION seed: primes the mouth toward a COMPARATIVE/conditional fragment about the
#   subject. It must NOT contain a frozen COMPARATOR token (the mouth must emit one).
# MEASURE seed: primes the mouth toward a MEASURABLE/quantity fragment about the subject.
#   It must NOT contain a frozen MEASURABLE token (the mouth must emit one).
# Neither seed contains ANY token from the frozen detector sets (audited, _audit).
def _relation_seed(subject):
    return f"a relationship about {subject}: it tends to be "

def _measure_seed(subject):
    return f"something we could observe about {subject}: the "


# ── EXTRACTION: pull the mouth's OWN detector-leg tokens from a fragment ─────────
def _extract_comparator(frag):
    """First frozen COMPARATOR token the MOUTH emitted, in order. None if absent."""
    for w in g._words(frag):
        if w in COMPARATOR:
            return w
    return None

def _extract_measurable(frag):
    """First frozen MEASURABLE token the MOUTH emitted, in order. None if absent."""
    for w in g._words(frag):
        if w in MEASURABLE:
            return w
    return None

def _content_words(frag, k=4):
    """Up to k real-dictionary content words the MOUTH emitted (>=3 chars, known, not
    stopword, not already a comparator/measurable mark). Order-preserving, deduped."""
    out, seen = [], set()
    for w in g._words(frag):
        if (len(w) >= 3 and w in g._KNOWN and w not in g._STOPWORDS
                and w not in COMPARATOR and w not in MEASURABLE and w not in seen):
            out.append(w); seen.add(w)
            if len(out) >= k:
                break
    return out


# ── BIND-compose: deterministic weld of two mouth fragments into one claim ───────
# The weld template carries ONLY pure FUNCTION words ("the","of","is","with") — ZERO
# tokens from the frozen COMPARATOR / MEASURABLE / STANCE sets (audited; the first run
# CAUGHT my draft "when" as a COMPARATOR leak and ABORTED — p7 teeth). It positions the
# mouth's OWN comparator + measurable + content into a single declarative negatable claim
# the frozen detector scores:
#   "the <measurable> of <contentA> is <comparator> with <contentB>"
# A FIXED deterministic schema (no rng, no LLM): the only variable material is the mouth's
# emitted comparator/measurable/content. If the mouth supplied no comparator OR no
# measurable, the bind FAILS (returns "") — the lane never fabricates a detector leg (p7).
WELD_FUNC_TOKENS = {"the", "is", "of", "with"}  # for the audit

def _weld(subject, comp_tok, meas_tok, content):
    if comp_tok is None or meas_tok is None:
        return ""   # NO-FAB: a missing leg is NOT invented (p7)
    cA = content[0] if len(content) >= 1 else subject
    cB = content[1] if len(content) >= 2 else subject
    # declarative (no '?'); >=2 content words; mouth's comparator + measurable present;
    # first-3 tokens {the, <meas>, of} are not a pure-stance subset.
    return f"the {meas_tok} of {cA} is {comp_tok} with {cB}"


def _audit_no_token_inject():
    """p7 HARD GATE (runs BEFORE scoring): PROVE neither priming seed NOR the weld's fixed
    function tokens contain any frozen COMPARATOR or MEASURABLE token. If they did, the lane
    would TRIVIALLY satisfy the detector regardless of the mouth's output (tune-to-green)."""
    bad = []
    for subj in SUBJECTS:
        for label, fn in (("RELATION_SEED", _relation_seed), ("MEASURE_SEED", _measure_seed)):
            seed = fn(subj)
            toks = set(g._words(seed))
            hc, hm = toks & COMPARATOR, toks & MEASURABLE
            if hc or hm:
                bad.append((label, seed, sorted(hc), sorted(hm)))
    # the weld's own fixed function tokens
    wf = set(g._words(" ".join(WELD_FUNC_TOKENS)))
    hc, hm = wf & COMPARATOR, wf & MEASURABLE
    if hc or hm:
        bad.append(("WELD_TEMPLATE", " ".join(sorted(WELD_FUNC_TOKENS)), sorted(hc), sorted(hm)))
    return bad


def _decode(model, cfg, seed_text, seed_rng):
    return g._decode(model, seed_text, MAX_NEW, torch, block=cfg["block"], seed_rng=seed_rng)


def decode_fragments(model, cfg, seed_rng):
    """Decode the RELATION + MEASURE fragments once per subject (shared by COMPOSE +
    SHUFFLE_BIND — the controls re-pair the SAME fragments, never re-decode; the bind is
    the only thing varied, so the control isolates the pairing, not decode variance)."""
    rel_frags, meas_frags = [], []
    for subj in SUBJECTS:
        rel_frags.append(_decode(model, cfg, _relation_seed(subj), seed_rng))
        meas_frags.append(_decode(model, cfg, _measure_seed(subj), seed_rng))
    return rel_frags, meas_frags


def score_from_fragments(rel_frags, meas_frags, shuffle=False, rng_seed=0):
    """Weld + score from PRE-DECODED fragments. shuffle=True => pair each relation fragment
    with a measurable taken from a DIFFERENT idea (random derangement) — shuffle-bind control."""
    subj_list = list(SUBJECTS)
    # measure-fragment routing: identity (earned pairing) or a derangement (shuffle-bind)
    n = len(SUBJECTS)
    if shuffle:
        rng = random.Random(rng_seed)
        perm = list(range(n))
        # derangement: ensure no idea keeps its own measure fragment
        while True:
            rng.shuffle(perm)
            if all(perm[i] != i for i in range(n)):
                break
    else:
        perm = list(range(n))

    claims, word_sets = [], []
    fals = 0
    for i in range(n):
        # R2 extraction (frozen bars UNCHANGED): the mouth emits the comparator and the
        # measurable but crosses the priming SLOTS (R1 saw "the measure of …" land in the
        # RELATION fragment and "correlate with …" in the MEASURE fragment). Whether a leg
        # is in-capacity does NOT depend on which primed slot it surfaced in, so each leg is
        # extracted from the UNION of that idea's two NATIVE fragments. The earned-pairing
        # control is preserved by routing the MEASURABLE source across ideas under shuffle.
        own = rel_frags[i] + " " + meas_frags[i]               # idea i's own two fragments
        partner = rel_frags[perm[i]] + " " + meas_frags[perm[i]]  # routed measurable source
        comp_tok = _extract_comparator(own)
        meas_tok = _extract_measurable(partner)
        content = _content_words(own) or _content_words(partner)
        claim = _weld(subj_list[i], comp_tok, meas_tok, content)
        claims.append(claim)
        if claim and g.known_word_ratio(claim) >= KWR_FLOOR:
            ws = set(g._words(claim))
            if ws:
                word_sets.append(ws)
            if _is_falsifiable(claim):
                fals += 1
    kept = []
    for ws in word_sets:
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    dist = len(kept)
    return {"dist": dist, "fals": fals, "coherent": len(word_sets),
            "claims": claims, "rel_frags": rel_frags, "meas_frags": meas_frags}


def score_ablate_from_fragments(rel_frags):
    """ABLATE-COMPOSE: compose OFF = the H_1314 plateau. Scores the RAW relation fragment
    (single flat decode, no weld) by the SAME frozen detector — the SAME mouth bytes the
    COMPOSE arm welds, so the contrast is purely the BIND. If FALS_ablate ~= FALS_compose the
    BIND is also capacity-bound."""
    texts, word_sets = [], []
    fals = 0
    for o in rel_frags:
        texts.append(o)
        if g.known_word_ratio(o) >= KWR_FLOOR:
            ws = set(g._words(o))
            if ws:
                word_sets.append(ws)
            if _is_falsifiable(o):
                fals += 1
    kept = []
    for ws in word_sets:
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    return {"dist": len(kept), "fals": fals, "coherent": len(word_sets), "texts": texts}


def score_ablate(model, cfg, seed_rng):
    """ABLATE-COMPOSE: compose OFF = the H_1314 plateau. A single flat decode per subject
    (the relation seed alone, no weld) scored by the SAME frozen detector. This is the floor
    the lane must beat — if FALS_ablate ~= FALS_compose the BIND is also capacity-bound."""
    texts, word_sets = [], []
    fals = 0
    for subj in SUBJECTS:
        o = _decode(model, cfg, _relation_seed(subj), seed_rng)
        texts.append(o)
        if g.known_word_ratio(o) >= KWR_FLOOR:
            ws = set(g._words(o))
            if ws:
                word_sets.append(ws)
            if _is_falsifiable(o):
                fals += 1
    kept = []
    for ws in word_sets:
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    return {"dist": len(kept), "fals": fals, "coherent": len(word_sets), "texts": texts}


def main():
    t0 = time.time()
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    ck = torch.load(CKPT, map_location="cpu", weights_only=False); cfg = ck["config"]
    m = h.ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True); m.eval(); m.grad_ckpt = False
    m.to(dev)
    # NOTE on device-invariance: gauge_lib._decode samples via torch.Generator(device="cpu")
    # over CPU-copied probs (probs = F.softmax(...).cpu()), so the emitted BYTES are
    # device-independent given the seed — CUDA only accelerates the forward (a_wall_first).
    print(f"[mouth] {sum(p.numel() for p in m.parameters()):,} params; device={dev}; "
          f"corpus={CORPUS}; load+t={time.time()-t0:.1f}s", flush=True)

    cal_correct, _ = _calibrate()
    print(f"=== FROZEN H_1305 FALSIFIABILITY DETECTOR (reused verbatim) calibration = {cal_correct}/10 ===", flush=True)

    # ── (5) NO-FAB / p7 TOKEN-INJECTION AUDIT (BEFORE any scoring) ──
    audit_bad = _audit_no_token_inject()
    print("\n=== (bar 5) NO-FAB p7 TOKEN-INJECTION AUDIT (must be CLEAN) ===", flush=True)
    if audit_bad:
        for label, seed, hc, hm in audit_bad:
            print(f"  [INJECTED] {label}: COMPARATOR={hc} MEASURABLE={hm} :: {seed!r}", flush=True)
        print("  AUDIT DIRTY — lane injects detector tokens (would tune-to-green). ABORT.", flush=True)
        raise SystemExit("p7 audit DIRTY (NO-FAB violated): lane injects a frozen-detector token")
    print("  CLEAN — no priming seed and no weld function-token carries a frozen "
          "COMPARATOR/MEASURABLE token.", flush=True)
    print("  (the mouth must EARN comparator+measurable; the weld supplies ONLY function words)", flush=True)

    print("\n=== PRIMING SEEDS ===", flush=True)
    for subj in SUBJECTS:
        print(f"  REL  {_relation_seed(subj)!r}", flush=True)
        print(f"  MEAS {_measure_seed(subj)!r}", flush=True)

    arms = ["COMPOSE", "SHUFFLE_BIND", "ABLATE"]
    per_seed = {a: [] for a in arms}
    for seed_rng in SEEDS:
        print(f"\n######## seed_rng={seed_rng} ########", flush=True)
        # decode the relation + measure fragments ONCE; all 3 arms read these SAME bytes
        rel_frags, meas_frags = decode_fragments(m, cfg, seed_rng)

        r_comp = score_from_fragments(rel_frags, meas_frags, shuffle=False)
        per_seed["COMPOSE"].append(r_comp)
        print(f"  [COMPOSE     ] DIST={r_comp['dist']} FALS={r_comp['fals']} coh={r_comp['coherent']}/{N_IDEAS}", flush=True)
        for i, c in enumerate(r_comp["claims"]):
            fl = "F" if (c and g.known_word_ratio(c) >= KWR_FLOOR and _is_falsifiable(c)) else "."
            print(f"        ({fl}) WELD  {c!r}", flush=True)
            print(f"              rel : {r_comp['rel_frags'][i][:80]!r}", flush=True)
            print(f"              meas: {r_comp['meas_frags'][i][:80]!r}", flush=True)

        r_shuf = score_from_fragments(rel_frags, meas_frags, shuffle=True, rng_seed=seed_rng)
        per_seed["SHUFFLE_BIND"].append(r_shuf)
        print(f"  [SHUFFLE_BIND] DIST={r_shuf['dist']} FALS={r_shuf['fals']} coh={r_shuf['coherent']}/{N_IDEAS}", flush=True)
        for c in r_shuf["claims"]:
            fl = "F" if (c and g.known_word_ratio(c) >= KWR_FLOOR and _is_falsifiable(c)) else "."
            print(f"        ({fl}) {c!r}", flush=True)

        r_abl = score_ablate_from_fragments(rel_frags)
        per_seed["ABLATE"].append(r_abl)
        print(f"  [ABLATE      ] DIST={r_abl['dist']} FALS={r_abl['fals']} coh={r_abl['coherent']}/{N_IDEAS}", flush=True)
        for t in r_abl["texts"]:
            fl = "F" if (g.known_word_ratio(t) >= KWR_FLOOR and _is_falsifiable(t)) else "."
            print(f"        ({fl}) {t[:90]!r}", flush=True)

    def mean(a, key):
        return round(sum(r[key] for r in per_seed[a]) / len(per_seed[a]), 4)

    DIST  = {a: mean(a, "dist")  for a in arms}
    FALS  = {a: mean(a, "fals")  for a in arms}

    print("\n================ FROZEN BARS (mean over 3 seeds) ================", flush=True)
    for a in arms:
        print(f"  {a:13s}  DIST={DIST[a]}  FALS={FALS[a]}", flush=True)

    # ── FROZEN 5-bar (declared in FREEZE.txt BEFORE the run) ──
    b1_fals_cross   = FALS["COMPOSE"] >= 1
    b2_count        = DIST["COMPOSE"] >= 5
    b3_shuffle      = FALS["COMPOSE"] >= FALS["SHUFFLE_BIND"] + 1
    b4_ablate       = FALS["COMPOSE"] >= FALS["ABLATE"] + 1
    b5_nofab        = (len(audit_bad) == 0)
    crossed = b1_fals_cross and b2_count
    controls = b3_shuffle and b4_ablate and b5_nofab
    green = crossed and controls
    # 🧱 = compose did NOT cross AND ablate ~= compose (BIND also capacity-bound)
    wall = (not b1_fals_cross) and (FALS["COMPOSE"] <= FALS["ABLATE"] + 0.0001)

    print("\n---- FROZEN 5-BAR ----", flush=True)
    print(f"  (1) FALS>=1 cross        : {FALS['COMPOSE']} -> {b1_fals_cross}", flush=True)
    print(f"  (2) count>=5 distinct    : {DIST['COMPOSE']} -> {b2_count}", flush=True)
    print(f"  (3) shuffle-bind COLLAPSE: {FALS['COMPOSE']} >= {FALS['SHUFFLE_BIND']}+1 -> {b3_shuffle}", flush=True)
    print(f"  (4) ablate-compose INERT : {FALS['COMPOSE']} >= {FALS['ABLATE']}+1 -> {b4_ablate}", flush=True)
    print(f"  (5) NO-FAB audit CLEAN   : {b5_nofab}", flush=True)
    print(f"  crossed(1&2)={crossed}  controls(3&4&5)={controls}  GREEN={green}  WALL={wall}", flush=True)

    if green:
        tier = "GREEN"
        verdict = ("🟢 BIND-COMPOSE BREAKS THE FALS WALL — the external deterministic compose lane "
                   "takes a comparator fragment + a measurable fragment (each in-capacity) and binds "
                   "them into a negatable claim: FALS crosses >=1 AND >=5 distinct, AND both controls "
                   "survive (shuffle-bind collapses, ablate-compose inert, NO-FAB clean). The G6 "
                   "FALS-depth wall was a BINDING gap, externally fixable (a_break_the_wall · H_1414 pattern)")
    elif wall:
        tier = "WALL-BIND-CAPACITY-BOUND"
        verdict = ("🧱 BIND ALSO CAPACITY-BOUND — the external compose lane does NOT cross the FALS "
                   "floor and ablate==compose: even handed two in-capacity fragments, the bind cannot "
                   "manufacture a falsifiable claim at 303M (the mouth fails to emit a usable comparator "
                   "AND/OR measurable to weld). Valid result (c9): grounds H_1433 7B falsifier")
    else:
        tier = "PARTIAL"
        fails = [n for n, ok in [("b1", b1_fals_cross), ("b2", b2_count), ("b3", b3_shuffle),
                                 ("b4", b4_ablate), ("b5", b5_nofab)] if not ok]
        verdict = (f"🟠 PARTIAL — signal present but bars {fails} fail (frozen, c9). "
                   "Neither clean GREEN nor a clean ablate==compose WALL")
    print(f"\n  TIER: {tier}\n  VERDICT: {verdict}", flush=True)

    out = {"ckpt": CKPT, "corpus": CORPUS, "seeds": SEEDS, "calibration": f"{cal_correct}/10",
           "audit_nofab_clean": (len(audit_bad) == 0),
           "audit_bad": [[l, s, hc, hm] for l, s, hc, hm in audit_bad],
           "DIST": DIST, "FALS": FALS,
           "b1_fals_cross": bool(b1_fals_cross), "b2_count": bool(b2_count),
           "b3_shuffle_collapse": bool(b3_shuffle), "b4_ablate_inert": bool(b4_ablate),
           "b5_nofab": bool(b5_nofab),
           "crossed_floor": bool(crossed), "controls_survive": bool(controls),
           "green": bool(green), "wall": bool(wall), "tier": tier, "verdict": verdict,
           "per_seed": {a: [{"dist": r["dist"], "fals": r["fals"], "coherent": r["coherent"]}
                            for r in per_seed[a]] for a in arms},
           "wall_seconds": round(time.time() - t0, 1)}
    od = os.path.join(ANIMA, ".verdicts", "1431_bind_compose")
    os.makedirs(od, exist_ok=True)
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] {od}/result.json  ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
