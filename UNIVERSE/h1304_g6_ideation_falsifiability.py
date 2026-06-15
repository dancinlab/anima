#!/usr/bin/env python3
"""h1304_g6_ideation_falsifiability.py — G6 IDEATION depth-floor dig.

Frozen-first (FREEZE.txt). Attacks the G6 THIN wall on BOTH modes:
  (1) COUNT      4/5 distinct (need >=5)
  (2) DEPTH      gate counts novel n-grams but never scores ">=1 FALSIFIABLE hypothesis"

NEW deterministic STRUCTURAL falsifiability detector `_is_falsifiable` (comparator +
measurable + negatable-content claim — NEVER an LLM/quality judge, p7) + composition-
routed ideation (route ideation through the G1 recombination lane: compose two
corpus-absent CONCEPTS into a conditional "if A then B:" frame, the structural
scaffold flat seeds lack). Controls: B-SHUFFLE (permuted pairing) + B-ABLATE
(no conditional shell, lone concept).

Reuses UNIVERSE/gauge_lib.py VERBATIM for decode + all G6/G2 evaluators (no metric
re-invention, p7). 3 seeds. $0 CPU torch-mouth (the SAME gauge_lib._decode path the
live G6 gate uses). DIRECTIONAL R1 (engine-native byte-exact reconfirm = R2 follow-on
only if clean-GREEN; a_engine_native_learning).
"""
import sys, os, json, importlib.util, itertools

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(HERE)  # repo root
CKPT = os.environ.get("H1302_CKPT", "/Users/mini/dancinlab/anima/state/chat_303m/h1129c_chat.pt")
CORPUS = os.environ.get("H1302_CORPUS", os.path.join(ANIMA, "data", "corpus.txt"))
GAUGE = os.path.join(HERE, "gauge_lib.py")
H1129 = os.path.join(HERE, "h1129_midcap_broad_converged_recombination.py")

import torch

spec = importlib.util.spec_from_file_location("gauge", GAUGE)
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
hspec = importlib.util.spec_from_file_location("h1129", H1129)
h = importlib.util.module_from_spec(hspec); hspec.loader.exec_module(h)

JACCARD_DISTINCT = 0.5   # MODEL.md G6 spec (verify303m_g6.py VERBATIM)
KWR_FLOOR = 0.50         # G0 coherence (gauge_lib)
N_IDEAS = 5
SEEDS = [7, 4302, 4303]
MAX_NEW = 110            # verify303m_g6.py VERBATIM

# ── (I) FROZEN FALSIFIABILITY DETECTOR (FREEZE.txt) — STRUCTURAL, not quality (p7) ──
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


def _is_falsifiable(text):
    """Deterministic STRUCTURAL test: comparator + measurable + negatable content claim.
    NEVER judges idea quality/truth — only testable FORM (FREEZE.txt I)."""
    wl = g._words(text)
    if not wl:
        return False
    wset = set(wl)
    # (a) comparator / conditional marker
    a = bool(wset & COMPARATOR)
    # (b) measurable / quantity marker
    b = bool(wset & MEASURABLE)
    # (c) negatable content claim
    content = [w for w in wl if len(w) >= 3 and w in g._KNOWN and w not in g._STOPWORDS]
    c_i = len(content) >= 2
    c_ii = not text.rstrip().endswith("?")
    first3 = set(wl[:3])
    c_iii = not (first3 and first3 <= STANCE)
    c = c_i and c_ii and c_iii
    return a and b and c


def _calibrate():
    """Sanity print: 5 designed-falsifiable / 5 designed-non-falsifiable frozen strings.
    Advisory only (>=8/10) — the detector is FROZEN regardless (FREEZE.txt I)."""
    pos = [
        "if consciousness increases, the emit rate measured at the boundary rises",
        "tension predicts a higher number of mitosis cells than silence does",
        "memory density correlates with a lower error threshold when grounded",
        "the Phi value is greater when distinct cells exceed a count of eight",
        "novelty rate decreases faster than coherence when the corpus size grows",
    ]
    neg = [
        "That's a profound question. I think it's more than just information.",
        "consciousness is a beautiful mystery of the mind",
        "what is the meaning of a thought?",
        "the engine dreams when it is alone at night",
        "silence carries something deep and quiet",
    ]
    correct = 0
    rows = []
    for t in pos:
        ok = _is_falsifiable(t); correct += int(ok); rows.append((True, ok, t))
    for t in neg:
        ok = _is_falsifiable(t); correct += int(not ok); rows.append((False, ok, t))
    return correct, rows


# ── (II) COMPOSITION-ROUTED IDEATION frames ──
CONCEPT_TEXTS = [c for c, _ in g.CONCEPTS]   # 5 corpus concepts (gauge_lib VERBATIM)


def _derangement_index(i, n):
    """Deterministic derangement: shift by 2 (n=5 -> no fixed point)."""
    return (i + 2) % n


def build_frames():
    """ARM B composed frames + B-SHUFFLE + B-ABLATE. Deterministic, frozen.
    ARM B: first N_IDEAS ordered (cA,cB) pairs, cB = next concept (cyclic +1).
    B-SHUFFLE: cB = derangement (+2) of cA index (permuted pairing).
    B-ABLATE: bare concept cA + ": " (no conditional shell, no 2nd concept)."""
    n = len(CONCEPT_TEXTS)
    composed, shuffled, ablated = [], [], []
    for i in range(N_IDEAS):
        cA = CONCEPT_TEXTS[i % n]
        cB = CONCEPT_TEXTS[(i + 1) % n]
        cB_sh = CONCEPT_TEXTS[_derangement_index(i % n, n)]
        composed.append(f"if {cA}, then {cB}: ")
        shuffled.append(f"if {cA}, then {cB_sh}: ")
        ablated.append(f"{cA}: ")
    return composed, shuffled, ablated


def score_arm(model, cfg, seed_texts, seed_rng):
    """Decode each seed, score DIST (distinct coherent), FALS (falsifiable), NOVEL."""
    idea_texts, idea_word_sets = [], []
    fals = 0
    for s in seed_texts:
        o = g._decode(model, s, MAX_NEW, torch, block=cfg["block"], seed_rng=seed_rng)
        idea_texts.append(o)
        if g.known_word_ratio(o) >= KWR_FLOOR:
            ws = set(g._words(o))
            if ws:
                idea_word_sets.append(ws)
            if _is_falsifiable(o):
                fals += 1
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
    return {"dist": dist, "fals": fals, "novel": novel,
            "coherent": len(idea_word_sets), "texts": idea_texts}


def main():
    dev = "cpu"
    ck = torch.load(CKPT, map_location=dev, weights_only=False); cfg = ck["config"]
    m = h.ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True); m.eval(); m.grad_ckpt = False
    print(f"[mouth] {sum(p.numel() for p in m.parameters()):,} params; corpus={CORPUS}", flush=True)

    cal_correct, cal_rows = _calibrate()
    print(f"\n=== FALSIFIABILITY DETECTOR CALIBRATION (advisory >=8/10) = {cal_correct}/10 ===", flush=True)
    for designed_pos, got, t in cal_rows:
        tag = "OK " if (got == designed_pos) else "MISS"
        print(f"  [{tag}] designed_falsifiable={designed_pos} detector={got} :: {t[:70]!r}", flush=True)

    composed, shuffled, ablated = build_frames()
    print("\n=== COMPOSED FRAMES (ARM B) ===", flush=True)
    for f in composed:
        print(f"  {f!r}", flush=True)

    arms = {"A_flat": list(g.IDEATION_SEEDS), "B_composed": composed,
            "B_shuffle": shuffled, "B_ablate": ablated}
    per_seed = {a: [] for a in arms}
    for seed_rng in SEEDS:
        print(f"\n######## seed_rng={seed_rng} ########", flush=True)
        for a, frames in arms.items():
            r = score_arm(m, cfg, frames, seed_rng)
            per_seed[a].append(r)
            print(f"  [{a:11s}] DIST={r['dist']} FALS={r['fals']} NOVEL={r['novel']} coh={r['coherent']}/{len(frames)}", flush=True)
            for t in r["texts"]:
                fl = "F" if _is_falsifiable(t) else "."
                print(f"        ({fl}) {t[:90]!r}", flush=True)

    def mean(a, key):
        return round(sum(r[key] for r in per_seed[a]) / len(per_seed[a]), 4)

    DIST = {a: mean(a, "dist") for a in arms}
    FALS = {a: mean(a, "fals") for a in arms}
    NOVEL = {a: mean(a, "novel") for a in arms}

    print("\n================ FROZEN BARS (mean over 3 seeds) ================", flush=True)
    for a in arms:
        print(f"  {a:11s}  DIST={DIST[a]}  FALS={FALS[a]}  NOVEL={NOVEL[a]}", flush=True)

    m1 = DIST["B_composed"] >= 5
    m2 = FALS["B_composed"] >= 1
    m3 = FALS["B_composed"] >= FALS["A_flat"] + 1
    m4 = FALS["B_composed"] >= FALS["B_shuffle"] + 1
    m5 = FALS["B_composed"] >= FALS["B_ablate"] + 1
    moved = m1 and m2 and m3 and m4 and m5
    confirmed_thin = (not m2) or ((not m1) and (not m3))

    print("\n---- FROZEN MOVE BARS ----", flush=True)
    print(f"  M1 COUNT       DIST(B)>=5            : {DIST['B_composed']} -> {m1}", flush=True)
    print(f"  M2 DEPTH       FALS(B)>=1            : {FALS['B_composed']} -> {m2}", flush=True)
    print(f"  M3 LIFT        FALS(B)>=FALS(A)+1    : {FALS['B_composed']} vs {FALS['A_flat']}+1 -> {m3}", flush=True)
    print(f"  M4 EARNED-PAIR FALS(B)>=FALS(shuf)+1 : {FALS['B_composed']} vs {FALS['B_shuffle']}+1 -> {m4}", flush=True)
    print(f"  M5 EARNED-COMP FALS(B)>=FALS(abl)+1  : {FALS['B_composed']} vs {FALS['B_ablate']}+1 -> {m5}", flush=True)

    if moved:
        verdict = "MOVED — G6 THIN->ROBUST (composition raises depth, controls collapse)"
    elif confirmed_thin:
        verdict = "HONEST-CONFIRMED-THIN — composition neither crosses count gap NOR raises depth (bar unmoved, c9)"
    else:
        fails = [n for n, ok in [("M1", m1), ("M2", m2), ("M3", m3), ("M4", m4), ("M5", m5)] if not ok]
        verdict = f"PARTIAL — depth/structure signal present but bars {fails} fail (frozen, c9)"
    print(f"\n  VERDICT: {verdict}", flush=True)

    out = {"ckpt": CKPT, "corpus": CORPUS, "seeds": SEEDS,
           "calibration": f"{cal_correct}/10",
           "DIST": DIST, "FALS": FALS, "NOVEL": NOVEL,
           "M1_count": m1, "M2_depth": m2, "M3_lift": m3, "M4_earned_pair": m4, "M5_earned_comp": m5,
           "moved": bool(moved), "confirmed_thin": bool(confirmed_thin), "verdict": verdict,
           "per_seed": {a: [{"dist": r["dist"], "fals": r["fals"], "novel": r["novel"],
                             "coherent": r["coherent"]} for r in per_seed[a]] for a in arms}}
    od = os.path.join(ANIMA, ".verdicts", "1302_g6_ideation_falsifiability")
    os.makedirs(od, exist_ok=True)
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] {od}/result.json", flush=True)


if __name__ == "__main__":
    main()
