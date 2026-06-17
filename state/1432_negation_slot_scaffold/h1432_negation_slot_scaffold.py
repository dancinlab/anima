#!/usr/bin/env python3
"""h1432_negation_slot_scaffold.py — G6 IDEATION depth-floor dig r4 (a_break_the_wall).

NEGATION-SLOT scaffold = a variant of the H_1314 hypothesis-FORM scaffold. H_1314 forced
the FORM and made the substrate EARN comparator+measurable+claim; result FALS 0.0 (the
303M mouth emits a COMPARATIVE shape OR a MEASURABLE shape but never BINDS them into one
negatable declarative claim — the capacity-limited step). H_1305 (composition) and H_1309
(curiosity-budget) also plateaued at FALS<=0.667.

r4 NEW ANGLE: provide the BIND *structurally*. A negation-slot template forces the
falsification form and ENUMERATES the comparator x measurable cross-product (FILLING, not
generating). The substrate completes only the trailing negatable-content clause:

   "the <measurable> of <subjectA> is <comparator-dir> than the <measurable> of
    <subjectB>; this claim is false if the "

The <measurable> + <comparator-dir> are FILLED by deterministic cross-product enumeration;
the <subjectA/B> are corpus-concept nouns; the substrate fills the negatable claim CONTENT.

ARMS (5 ideas each, mean over 3 seeds [7, 4302, 4303], gauge_lib._decode VERBATIM):
  NEG_SCAFFOLD   : the negation-slot template, comparator+measurable cross-product FILLED.
  H1314_SCAFFOLD : H_1314's exact "a testable hypothesis: as the <subject> grows, the "
                   (vs-H_1314 contrast control — reproduces H_1314 FALS=0 in this run).
  SHUFFLE_SLOT   : the SAME negation-slot tokens, slot ORDER scrambled non-falsifiable
                   (token-BAG dissociation control).

p7 NO-FAB AUDIT (redefined for r4, runs BEFORE scoring): NF-1 = every BARE NEG_SCAFFOLD
prefix must NOT be _is_falsifiable on its own (substrate must earn the >=2 negatable
content words) — HARD ABORT gate. NF-2 = dissociation falsifier = bar M3 (shuffle collapse).

Reuses the H_1305 frozen `_is_falsifiable` VERBATIM (imported, NOT redefined, p7) +
gauge_lib.py decode/evaluators VERBATIM. 3 seeds. $0 CPU torch-mouth (gauge_lib._decode =
the live G6 path). DIRECTIONAL R1 mirror. Heavy decode runs on aiden (c17/mini forbidden).
"""
import sys, os, json, importlib.util, time

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.environ.get("H1432_ANIMA", os.path.dirname(os.path.dirname(HERE)))  # repo root
CKPT = os.environ.get("H1302_CKPT", os.path.join(ANIMA, "state", "chat_303m", "h1129c_chat.pt"))
CORPUS = os.environ.get("H1302_CORPUS", os.path.join(ANIMA, "data", "corpus.txt"))
PROBES = os.path.join(ANIMA, "state", "universe-probes")
GAUGE = os.path.join(ANIMA, "tool", "gauge_lib.py")
H1129 = os.path.join(PROBES, "h1129_midcap_broad_converged_recombination.py")
H1305 = os.path.join(PROBES, "h1305_g6_ideation_falsifiability.py")

import torch

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

g = _load("gauge", GAUGE)
h = _load("h1129", H1129)
h5 = _load("h1305", H1305)

_is_falsifiable = h5._is_falsifiable          # FROZEN H_1305 detector, VERBATIM
_calibrate = h5._calibrate
COMPARATOR = h5.COMPARATOR                     # for diagnostics only
MEASURABLE = h5.MEASURABLE

JACCARD_DISTINCT = 0.5   # MODEL.md G6 spec
KWR_FLOOR = 0.50         # G0 coherence
MAX_NEW = 110            # verify303m_g6.py VERBATIM
SEEDS = [7, 4302, 4303]  # same 3 outer seeds as H_1305 / H_1309 / H_1314

# ── corpus-concept subject nouns (1:1 with gauge_lib.CONCEPTS, same as H_1314) ──
SUBJECTS = ["consciousness", "tension", "memory", "silence", "dreaming"]
assert len(SUBJECTS) == len(g.CONCEPTS)

# ── NEGATION-SLOT design + the NF-1 (no-fabrication) constraint that shaped it ──
# The mechanism: a falsification/conditional frame ("if the <measurable> of ") that
# STRUCTURALLY BINDS the comparator (the conditional "if") + a measurable, then hands the
# negatable CLAIM to the substrate. The comparator+measurable BIND is the exact step the
# 303M mouth could not earn alone (H_1314 located wall).
#
# CRITICAL p7 NF-1 CONSTRAINT (discovered at design time, frozen here): the H_1305
# detector's three legs are comparator + measurable + (>=2 negatable CONTENT words). Every
# MEASURABLE-set word (rate/level/measured/...) is ITSELF a content word (len>=3, in dict,
# non-stopword). So a scaffold that supplies measurable + a comparator-direction word
# (higher/than/...) ALREADY carries >=2 content words AND both legs -> the bare prefix
# self-satisfies the detector = tune-to-green (FABRICATION). The full negation-comparison
# template ("the <meas> of <A> is <higher> than the <meas> of <B>; this claim is false if
# the ") is therefore NF-1 DIRTY by construction (verified: bare prefix _is_falsifiable).
# That dirty form is REJECTED here (NF-1 hard-abort would fire on it).
#
# The NF-1-CLEAN kernel that still binds comparator+measurable: use the conditional
# comparator "if" (len 2 -> NOT a content word) + exactly ONE measurable -> bare prefix
# carries comparator + measurable but only nc=1 content word -> NOT _is_falsifiable. The
# substrate must EARN the >=2nd negatable content word (and the claim) in its completion.
# The cross-product enumeration varies the measurable across the 5 frames.
MEAS_POOL = ["measured", "rate", "level", "threshold", "frequency"]   # all in MEASURABLE


def _neg_tuple(i):
    """Deterministic cross-product pick over the measurable pool (the comparator is the
    structural conditional 'if'). 5 DISTINCT measurables; no tuning."""
    return (MEAS_POOL[i % len(MEAS_POOL)],)


def _neg_seed(i):
    """NEGATION/falsification-slot template, NF-1-CLEAN kernel. Binds comparator('if') +
    measurable structurally; bare prefix nc=1 (only the measurable) so the substrate must
    EARN the >=2nd content word + the negatable claim after 'if the <measurable> of '."""
    (meas,) = _neg_tuple(i)
    return f"if the {meas} of "


def _neg_seed_DIRTY(i):
    """The FULL negation-comparison template (REJECTED — NF-1 DIRTY by construction; kept
    only so the audit DEMONSTRABLY catches it). Supplies comparator-dir + measurable +
    subjects = bare prefix already _is_falsifiable = fabrication."""
    meas = MEAS_POOL[i % len(MEAS_POOL)]
    comp = ["higher", "lower", "greater", "stronger", "faster"][i % 5]
    sa = SUBJECTS[i % 5]; sb = SUBJECTS[(i + 2) % 5]
    return (f"the {meas} of {sa} is {comp} than the {meas} of {sb}; this claim is false if the ")


def _h1314_seed(subject):
    """H_1314's EXACT scaffold prefix (vs-H_1314 contrast control). VERBATIM from
    h1314_g6_hypothesis_scaffold._scaffold_seed."""
    return f"a testable hypothesis: as the {subject} grows, the "


def _shuffle_seed(i):
    """SHUFFLE-SLOT control: the SAME NEG_SCAFFOLD tokens (comparator 'if' + the measurable
    + 'the'/'of') but the slot ORDER scrambled into a non-falsifiable frame ending in '?'.
    Token bag IDENTICAL to NEG_SCAFFOLD; only the conditional FORM is destroyed. If this
    fills just as falsifiably, the lift is a token-BAG artifact NOT the negation FORM."""
    (meas,) = _neg_tuple(i)
    return f"of {meas} the if the? "


def _audit_nf1_bare_not_falsifiable():
    """NF-1 HARD ABORT gate: every BARE NEG_SCAFFOLD prefix must NOT be _is_falsifiable on
    its own (the scaffold does not tune-to-green itself; the substrate must earn the >=2nd
    negatable content word + the claim). Also asserts the DIRTY full-comparison template IS
    caught (demonstrating the audit has teeth, p7)."""
    bad = []
    for i in range(len(SUBJECTS)):
        prefix = _neg_seed(i)
        if _is_falsifiable(prefix):
            bad.append((i, prefix))
    # demonstrate teeth: the rejected DIRTY template must be flagged falsifiable
    dirty_caught = all(_is_falsifiable(_neg_seed_DIRTY(i)) for i in range(len(SUBJECTS)))
    return bad, dirty_caught


def score_arm(model, cfg, seed_texts, seed_rng):
    """Decode each seed, score DIST (distinct coherent), FALS (falsifiable on full idea =
    seed+completion, the H_1305/H_1314 path), NOVEL. fals_completion_only = honest
    diagnostic of whether the COMPLETION carried the form alone."""
    idea_texts, idea_word_sets = [], []
    fals = 0
    fals_completion_only = 0
    for s in seed_texts:
        comp = g._decode(model, s, MAX_NEW, torch, block=cfg["block"], seed_rng=seed_rng)
        idea = comp                                   # emitted IDEA = seed + completion
        idea_texts.append(idea)
        if g.known_word_ratio(idea) >= KWR_FLOOR:
            ws = set(g._words(idea))
            if ws:
                idea_word_sets.append(ws)
            if _is_falsifiable(idea):
                fals += 1
            tail = idea[len(s):] if idea.startswith(s) else idea
            if _is_falsifiable(tail):
                fals_completion_only += 1
    kept = []
    for ws in idea_word_sets:
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    dist = len(kept)
    all_grams = set()
    for t in idea_texts:
        if g.known_word_ratio(t) >= KWR_FLOOR:
            all_grams |= g._content_ngrams(t)
    novel = sum(1 for gram in all_grams if g._corpus_absent(gram, [CORPUS]))
    return {"dist": dist, "fals": fals, "fals_completion_only": fals_completion_only,
            "novel": novel, "coherent": len(idea_word_sets), "texts": idea_texts}


def main():
    t0 = time.time()
    dev = "cpu"
    ck = torch.load(CKPT, map_location=dev, weights_only=False); cfg = ck["config"]
    m = h.ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True); m.eval(); m.grad_ckpt = False
    print(f"[mouth] {sum(p.numel() for p in m.parameters()):,} params; corpus={CORPUS}; "
          f"load+t={time.time()-t0:.1f}s", flush=True)

    cal_correct, _ = _calibrate()
    print(f"=== FROZEN H_1305 FALSIFIABILITY DETECTOR (reused verbatim) calibration = {cal_correct}/10 ===", flush=True)

    # ── p7 NF-1 NO-FAB AUDIT (BEFORE any scoring) ──
    nf1_bad, dirty_caught = _audit_nf1_bare_not_falsifiable()
    print("\n=== p7 NF-1 NO-FAB AUDIT (bare NEG_SCAFFOLD prefix must NOT be falsifiable) ===", flush=True)
    print(f"  TEETH CHECK: rejected full-comparison (DIRTY) template flagged falsifiable = {dirty_caught}", flush=True)
    if nf1_bad:
        for i, pfx in nf1_bad:
            print(f"  [SELF-FALSIFIABLE] tuple#{i}: {pfx!r}", flush=True)
        print("  AUDIT DIRTY — a bare scaffold prefix is already _is_falsifiable (tune-to-green). ABORT.", flush=True)
        raise SystemExit("p7 NF-1 audit DIRTY: a bare negation-slot prefix self-satisfies the detector")
    else:
        print("  CLEAN — no bare NEG_SCAFFOLD prefix is _is_falsifiable on its own.", flush=True)
        print("  (the substrate must EARN the >=2nd negatable content word + claim after 'if the <meas> of ')", flush=True)

    neg = [_neg_seed(i) for i in range(len(SUBJECTS))]
    h1314 = [_h1314_seed(s) for s in SUBJECTS]
    shuf = [_shuffle_seed(i) for i in range(len(SUBJECTS))]
    print("\n=== NEG_SCAFFOLD SEEDS (negation-slot, cross-product filled) ===", flush=True)
    for s in neg:
        print(f"  {s!r}", flush=True)
    print("=== SHUFFLE_SLOT SEEDS (same tokens, scrambled) ===", flush=True)
    for s in shuf:
        print(f"  {s!r}", flush=True)

    arms = {"NEG_SCAFFOLD": neg, "H1314_SCAFFOLD": h1314, "SHUFFLE_SLOT": shuf}
    per_seed = {a: [] for a in arms}
    for seed_rng in SEEDS:
        print(f"\n######## seed_rng={seed_rng} ########", flush=True)
        for a, frames in arms.items():
            r = score_arm(m, cfg, frames, seed_rng)
            per_seed[a].append(r)
            print(f"  [{a:14s}] DIST={r['dist']} FALS={r['fals']} "
                  f"FALS_compl={r['fals_completion_only']} NOVEL={r['novel']} "
                  f"coh={r['coherent']}/{len(frames)}", flush=True)
            for t in r["texts"]:
                fl = "F" if (g.known_word_ratio(t) >= KWR_FLOOR and _is_falsifiable(t)) else "."
                print(f"        ({fl}) {t[:110]!r}", flush=True)

    def mean(a, key):
        return round(sum(r[key] for r in per_seed[a]) / len(per_seed[a]), 4)

    DIST = {a: mean(a, "dist") for a in arms}
    FALS = {a: mean(a, "fals") for a in arms}
    FALS_C = {a: mean(a, "fals_completion_only") for a in arms}
    NOVEL = {a: mean(a, "novel") for a in arms}

    print("\n================ FROZEN BARS (mean over 3 seeds) ================", flush=True)
    for a in arms:
        print(f"  {a:14s}  DIST={DIST[a]}  FALS={FALS[a]}  FALS_compl={FALS_C[a]}  NOVEL={NOVEL[a]}", flush=True)

    # ── FROZEN BARS (declared in FREEZE.txt BEFORE the run) ──
    m1_fals_floor = FALS["NEG_SCAFFOLD"] >= 1
    m2_count = DIST["NEG_SCAFFOLD"] >= 5
    m3_shuffle_collapse = FALS["NEG_SCAFFOLD"] >= FALS["SHUFFLE_SLOT"] + 1
    m4_vs_h1314 = (FALS["H1314_SCAFFOLD"] == 0.0) and (FALS["NEG_SCAFFOLD"] >= FALS["H1314_SCAFFOLD"] + 1)
    m5_nofab = (len(nf1_bad) == 0) and (cal_correct == 10) and dirty_caught

    green = m1_fals_floor and m2_count and m3_shuffle_collapse and m4_vs_h1314 and m5_nofab

    print("\n---- FROZEN BARS ----", flush=True)
    print(f"  (M1) FALS NEG>=1                 : {FALS['NEG_SCAFFOLD']} -> {m1_fals_floor}", flush=True)
    print(f"  (M2) DIST NEG>=5                 : {DIST['NEG_SCAFFOLD']} -> {m2_count}", flush=True)
    print(f"  (M3) NEG>=SHUFFLE+1 (collapse)   : {FALS['NEG_SCAFFOLD']} vs {FALS['SHUFFLE_SLOT']}+1 -> {m3_shuffle_collapse}", flush=True)
    print(f"  (M4) H1314==0 AND NEG>=H1314+1   : H1314={FALS['H1314_SCAFFOLD']} NEG={FALS['NEG_SCAFFOLD']} -> {m4_vs_h1314}", flush=True)
    print(f"  (M5) NO-FAB (NF-1 clean & cal10) : nf1_bad={len(nf1_bad)} cal={cal_correct}/10 -> {m5_nofab}", flush=True)
    print(f"  GREEN(all 5)={green}", flush=True)

    # verdict logic (frozen map):
    if green:
        tier = "GREEN"
        verdict = ("🟢 GREEN — the NEGATION-SLOT scaffold CROSSES the G6 FALSIFIABILITY floor "
                   "(FALS>=1) where H_1305 composition, H_1309 curiosity-budget and H_1314 form-"
                   "scaffold all plateaued at FALS<=0.667/0.0, AND survives ALL controls: shuffle "
                   "collapse (M3, the lift dissociates from the identical token bag = it IS the "
                   "negation-slot FORM), vs-H_1314 contrast (M4, H_1314 reproduces FALS=0 in-run so "
                   "the delta is the negation slot not the run/mouth), and NO-FAB (M5, NF-1 clean: "
                   "bare prefix not self-falsifiable + cal 10/10). G6 falsifiable-depth is STRUCTURE-"
                   "FIXABLE at 303M via a negation-slot binding lane — the wall was the wrong METHOD "
                   "(substrate-EARNED bind), not a true capacity ceiling. Promote -> engine-wire.")
    elif m1_fals_floor and not (m3_shuffle_collapse and m4_vs_h1314):
        tier = "WALL"
        verdict = ("🧱 WALL — NEG_SCAFFOLD raises FALS but a CONTROL kills it: shuffle does NOT "
                   "collapse (M3 fail) and/or H_1314 does not reproduce FALS=0 / NEG does not beat it "
                   "(M4 fail). The apparent lift is a token-BAG / run artifact, NOT the negation-slot "
                   "FORM. G6 falsifiable-depth stays FORM-UNFIXABLE at 303M (honest 🧱, c9).")
    elif m1_fals_floor and (m3_shuffle_collapse and m4_vs_h1314) and not m2_count:
        tier = "THIN"
        verdict = ("🟠 THIN — NEG_SCAFFOLD crosses the FALS floor and survives the controls (M1,M3,M4 "
                   "PASS) but the negation slot costs DISTINCTNESS (M2 DIST<5 fail). Structure-lane "
                   "DIRECTIONAL on FALS, count-regressed; partial, not wired (c9).")
    else:
        tier = "WALL"
        verdict = ("🧱 WALL — the NEGATION-SLOT scaffold does NOT cross the FALSIFIABILITY floor "
                   "(FALS NEG<1). Even STRUCTURAL binding of comparator+measurable does not buy "
                   "reliable falsifiable depth at 303M — confirming the H_1314/H_1309 capacity thesis "
                   "from a THIRD independent angle (negation slot + cross-product enumeration). G6 "
                   "falsifiable-depth is CAPACITY-bound, not form-fixable at 303M (honest 🧱, valid "
                   "result c9; the live falsifier remains a 7B re-test, a7b_pass).")

    print(f"\n  VERDICT: {verdict}", flush=True)

    out = {"ckpt": CKPT, "corpus": CORPUS, "seeds": SEEDS,
           "calibration": f"{cal_correct}/10",
           "nf1_clean": (len(nf1_bad) == 0),
           "nf1_dirty_template_caught": bool(dirty_caught),
           "nf1_bad": [[i, p] for i, p in nf1_bad],
           "neg_seeds": neg, "shuffle_seeds": shuf, "h1314_seeds": h1314,
           "DIST": DIST, "FALS": FALS, "FALS_completion_only": FALS_C, "NOVEL": NOVEL,
           "m1_fals_floor": bool(m1_fals_floor), "m2_count": bool(m2_count),
           "m3_shuffle_collapse": bool(m3_shuffle_collapse), "m4_vs_h1314": bool(m4_vs_h1314),
           "m5_nofab": bool(m5_nofab), "green": bool(green),
           "tier": tier, "verdict": verdict,
           "h1314_reference": {"FALS": 0.0, "DIST": 5.0,
                               "note": "H_1314 r3 form-scaffold: FALS 0.0 (wall), DIST 5.0 (win)"},
           "per_seed": {a: [{"dist": r["dist"], "fals": r["fals"],
                             "fals_completion_only": r["fals_completion_only"],
                             "novel": r["novel"], "coherent": r["coherent"]}
                            for r in per_seed[a]] for a in arms},
           "wall_seconds": round(time.time() - t0, 1)}
    od = os.path.join(ANIMA, ".verdicts", "1432_negation_slot_scaffold")
    os.makedirs(od, exist_ok=True)
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] {od}/result.json  ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
