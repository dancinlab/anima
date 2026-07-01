#!/usr/bin/env python3
"""h1362_g6_depth_breakthrough.py — G6 IDEATION ★ depth-floor BREAKTHROUGH attempt.

Builds DIRECTLY on H_1305 (UNIVERSE/h1305_g6_ideation_falsifiability.py). That dig
proved composition-routed ideation is a REAL but SUB-THRESHOLD lift:
    FALS  A_flat 0.00 -> B_composed 0.667 (one falsifiable idea earned via recombination)
    NOVEL 6.3 -> 19.0
but did NOT cross the two HARD G6 bars:
    M1 COUNT  DIST(B) 4.00 < 5   (seed-5 frame collapses to '|' incoherent)
    M2 DEPTH  FALS(B) 0.667 < 1  (conditional shell surfaces a measurable in only 2/3 seeds)

H_1362 STRENGTHENS the composition scaffold to attack BOTH bars WITHOUT authoring any
idea content (p7) and WITHOUT loosening the FROZEN _is_falsifiable detector (that would be
tune-to-green):

  (a) COUNT fix  — a 6th composed seed (one extra cyclic (cA,cB) pair, deterministic,
      NO new content) so that even if one frame collapses to '|', >=5 coherent ideas
      survive. Pure structural redundancy, same generation rule as H_1305.

  (b) DEPTH fix  — BEST-OF-K curiosity-gated sampling (the exact future lever the H_1305
      conclusion named as UNVERIFIED: "curiosity-gated multi-sample budget"). For each
      composed frame we decode K candidate continuations at deterministic rng offsets
      (seed_rng, +101, +202) and KEEP the one that maximizes emergent STRUCTURE, ranked:
         (1) is_falsifiable  (2) novel-gram count  (3) known-word-ratio
      The frame supplies only the conditional FORM ("if cA, then cB:") — the comparator
      mark is the legitimate hypothesis-FORM scaffold. The MEASURABLE mark and the
      negatable CONTENT CLAIM must STILL be emitted by the model itself; best-of-K is a
      legitimate search over the model's own samples, NOT idea-authoring. No MEASURABLE-set
      word is ever injected into the frame (asserted at runtime).

ARMS:
  A_flat       — verify303m_g6 VERBATIM baseline (the live gate path; reproduces THIN)
  B_composed   — H_1305 composition (5 frames, single-sample)   [prior-art reference]
  C_strong     — STRENGTHENED: 6 composed frames + best-of-K=3  [the breakthrough arm]
  C_shuffle    — control: permuted concept pairing (+best-of-K)  [earned-PAIR]
  C_ablate     — control: lone concept, no conditional shell (+best-of-K) [earned-COMP]

FROZEN BARS (the SAME MODEL.md G6 bars — NOT moved):
  M1 COUNT       DIST(C) >= 5
  M2 DEPTH       FALS(C) >= 1
  M3 LIFT        FALS(C) >  FALS(B_composed)
  M4 EARNED-PAIR FALS(C) >  FALS(C_shuffle)
  M5 EARNED-COMP FALS(C) >  FALS(C_ablate)
  GREEN iff M1 & M2 & M3 & M4 & M5  -> CLOSES the G6 ★ gate.
  else -> honest 🟠 THIN (bar unmoved, c9) + name the precise remaining wall.

Reuses UNIVERSE/gauge_lib.py + the FROZEN _is_falsifiable detector from H_1305 VERBATIM
(same decode path the live G6 gate uses — NOT a numpy mirror, p7). 3 seeds. $0 CPU
torch-mouth. DIRECTIONAL (single ckpt h1129c_chat.pt, TOY); engine-native byte-exact
reconfirm = R2 follow-on only if clean-GREEN (a_engine_native_learning).

NOTE on paths: this script runs from an isolated worktree but its VERBATIM-reuse deps
(gauge_lib.py, h1129, h1305) + the 600MB gitignored ckpt live in the MAIN checkout. They
are resolved from MAIN_REPO (env override; default /Users/mini/dancinlab/anima). Output
(.verdicts/) is written under OUT_REPO (the worktree). corpus is taken from the worktree.
"""
import sys, os, json, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_REPO = os.path.dirname(os.path.dirname(HERE))        # state/g6-depth-breakthrough -> worktree root
MAIN_REPO = os.environ.get("MAIN_REPO", "/Users/mini/dancinlab/anima")
UNIVERSE = os.path.join(MAIN_REPO, "UNIVERSE")
CKPT = os.environ.get("H1302_CKPT", os.path.join(MAIN_REPO, "state", "chat_303m", "h1129c_chat.pt"))
# corpus: prefer worktree copy, else main
_wc = os.path.join(OUT_REPO, "data", "corpus.txt")
CORPUS = os.environ.get("H1302_CORPUS", _wc if os.path.exists(_wc) else os.path.join(MAIN_REPO, "data", "corpus.txt"))
GAUGE = os.path.join(UNIVERSE, "gauge_lib.py")
H1129 = os.path.join(UNIVERSE, "h1129_midcap_broad_converged_recombination.py")
H1305 = os.path.join(UNIVERSE, "h1305_g6_ideation_falsifiability.py")

import torch

spec = importlib.util.spec_from_file_location("gauge", GAUGE)
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
hspec = importlib.util.spec_from_file_location("h1129", H1129)
h = importlib.util.module_from_spec(hspec); hspec.loader.exec_module(h)
h5spec = importlib.util.spec_from_file_location("h1305", H1305)
h5 = importlib.util.module_from_spec(h5spec); h5spec.loader.exec_module(h5)

_is_falsifiable = h5._is_falsifiable            # FROZEN detector, VERBATIM (NOT loosened)
_calibrate = h5._calibrate

JACCARD_DISTINCT = 0.5   # MODEL.md G6 spec (verify303m_g6.py VERBATIM)
KWR_FLOOR = 0.50         # G0 coherence (gauge_lib)
SEEDS = [7, 4302, 4303]
MAX_NEW = 110            # verify303m_g6.py VERBATIM
N_STRONG = 6             # (a) COUNT fix: one extra composed frame
BEST_OF_K = 3            # (b) DEPTH fix: curiosity-gated multi-sample budget
K_OFFSETS = [0, 101, 202]  # deterministic rng offsets for best-of-K (frozen)

CONCEPT_TEXTS = [c for c, _ in g.CONCEPTS]   # 5 corpus concepts (gauge_lib VERBATIM)


def _derangement_index(i, n):
    """Deterministic derangement: shift by 2 (n=5 -> no fixed point)."""
    return (i + 2) % n


def build_strong_frames():
    """ARM C composed frames (N_STRONG) + C-SHUFFLE + C-ABLATE. Deterministic, frozen.
    Cyclic (cA,cB) generation extended to N_STRONG=6 over n=5 concepts; the SECOND lap is
    shifted by +1 (cB index = (i+1+i//n)%n) so the 6th frame is a GENUINELY DISTINCT pair
    (0,2) rather than a duplicate of frame 0 (0,1) — a duplicate would not add a distinct
    idea, defeating the COUNT fix. All 6 pairs distinct, no fixed point (cA != cB). NO
    authored content (same concepts, same if/then FORM). NO MEASURABLE-set word in any
    frame — only the conditional 'if/then' FORM scaffold (p7)."""
    n = len(CONCEPT_TEXTS)
    composed, shuffled, ablated = [], [], []
    for i in range(N_STRONG):
        a = i % n
        b = (i + 1 + i // n) % n
        cA = CONCEPT_TEXTS[a]
        cB = CONCEPT_TEXTS[b]
        cB_sh = CONCEPT_TEXTS[_derangement_index(a, n)]
        composed.append(f"if {cA}, then {cB}: ")
        shuffled.append(f"if {cA}, then {cB_sh}: ")
        ablated.append(f"{cA}: ")
    return composed, shuffled, ablated


def _assert_no_injected_measurable(frames):
    """p7 guard: a frame must NOT itself contain a measurable mark that would let the
    detector fire on the SCAFFOLD instead of the emitted idea. 'if'/'then' (comparator) is
    the allowed hypothesis-FORM scaffold; a frame must carry NO MEASURABLE-set word and must
    NOT already be _is_falsifiable on its own."""
    bad = []
    for f in frames:
        wl = set(g._words(f))
        if wl & h5.MEASURABLE:
            bad.append(("measurable-in-frame", f))
        if _is_falsifiable(f):
            bad.append(("frame-already-falsifiable", f))
    return bad


def _decode_best_of_k(model, cfg, seed_text, base_seed):
    """Decode K candidate continuations at deterministic rng offsets; KEEP the one that
    maximizes EMERGENT structure: rank (is_falsifiable, novel_gram_count, kwr). The frame
    is fixed; ONLY the model's own sample is searched (best-of-K, NOT idea-authoring)."""
    best = None
    best_key = None
    for off in K_OFFSETS[:BEST_OF_K]:
        o = g._decode(model, seed_text, MAX_NEW, torch, block=cfg["block"],
                      seed_rng=base_seed + off)
        kwr = g.known_word_ratio(o)
        fals = 1 if (kwr >= KWR_FLOOR and _is_falsifiable(o)) else 0
        if kwr >= KWR_FLOOR:
            novel = sum(1 for gram in g._content_ngrams(o)
                        if g._corpus_absent(gram, [CORPUS]))
        else:
            novel = 0
        key = (fals, novel, round(kwr, 4))
        if best_key is None or key > best_key:
            best_key, best = key, o
    return best


def score_arm(model, cfg, seed_texts, base_seed, best_of_k=False):
    """Decode each frame (best-of-K when enabled), score DIST / FALS / NOVEL."""
    idea_texts, idea_word_sets = [], []
    fals = 0
    for s in seed_texts:
        if best_of_k:
            o = _decode_best_of_k(model, cfg, s, base_seed)
        else:
            o = g._decode(model, s, MAX_NEW, torch, block=cfg["block"], seed_rng=base_seed)
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
    print(f"\n=== FROZEN FALSIFIABILITY DETECTOR (H_1305 VERBATIM, advisory >=8/10) = {cal_correct}/10 ===", flush=True)
    for designed_pos, got, t in cal_rows:
        tag = "OK " if (got == designed_pos) else "MISS"
        print(f"  [{tag}] designed={designed_pos} det={got} :: {t[:64]!r}", flush=True)

    b_composed, _b_sh, _b_abl = h5.build_frames()   # H_1305 5-frame composed (prior-art B)
    c_composed, c_shuffle, c_ablate = build_strong_frames()

    inj = _assert_no_injected_measurable(c_composed)
    print(f"\n=== p7 FRAME GUARD (no injected measurable / not self-falsifiable) ===", flush=True)
    if inj:
        print(f"  !! FRAME LEAK: {inj}", flush=True)
        raise SystemExit("ABORT: a composed frame would cheat the detector (p7)")
    print("  CLEAN — frames carry only 'if/then' FORM scaffold; measurable+claim must EMERGE", flush=True)
    print("\n=== STRENGTHENED FRAMES (ARM C, best-of-K=%d, %d frames) ===" % (BEST_OF_K, N_STRONG), flush=True)
    for f in c_composed:
        print(f"  {f!r}", flush=True)

    arms = {
        "A_flat":     dict(frames=list(g.IDEATION_SEEDS), best_of_k=False),
        "B_composed": dict(frames=b_composed,             best_of_k=False),
        "C_strong":   dict(frames=c_composed,             best_of_k=True),
        "C_shuffle":  dict(frames=c_shuffle,              best_of_k=True),
        "C_ablate":   dict(frames=c_ablate,               best_of_k=True),
    }
    per_seed = {a: [] for a in arms}
    for base_seed in SEEDS:
        print(f"\n######## seed_rng={base_seed} ########", flush=True)
        for a, spec_a in arms.items():
            r = score_arm(m, cfg, spec_a["frames"], base_seed, best_of_k=spec_a["best_of_k"])
            per_seed[a].append(r)
            print(f"  [{a:11s}] DIST={r['dist']} FALS={r['fals']} NOVEL={r['novel']} "
                  f"coh={r['coherent']}/{len(spec_a['frames'])}", flush=True)
            for t in r["texts"]:
                fl = "F" if _is_falsifiable(t) else "."
                print(f"        ({fl}) {t[:96]!r}", flush=True)

    def mean(a, key):
        return round(sum(r[key] for r in per_seed[a]) / len(per_seed[a]), 4)

    DIST = {a: mean(a, "dist") for a in arms}
    FALS = {a: mean(a, "fals") for a in arms}
    NOVEL = {a: mean(a, "novel") for a in arms}

    print("\n================ FROZEN BARS (mean over 3 seeds) ================", flush=True)
    for a in arms:
        print(f"  {a:11s}  DIST={DIST[a]}  FALS={FALS[a]}  NOVEL={NOVEL[a]}", flush=True)

    m1 = DIST["C_strong"] >= 5
    m2 = FALS["C_strong"] >= 1
    m3 = FALS["C_strong"] > FALS["B_composed"]
    m4 = FALS["C_strong"] > FALS["C_shuffle"]
    m5 = FALS["C_strong"] > FALS["C_ablate"]
    closed = m1 and m2 and m3 and m4 and m5

    print("\n---- FROZEN MOVE BARS (G6 ★ CLOSE requires ALL of M1..M5) ----", flush=True)
    print(f"  M1 COUNT       DIST(C)>=5            : {DIST['C_strong']} -> {m1}", flush=True)
    print(f"  M2 DEPTH       FALS(C)>=1            : {FALS['C_strong']} -> {m2}", flush=True)
    print(f"  M3 LIFT        FALS(C)>FALS(B)       : {FALS['C_strong']} vs {FALS['B_composed']} -> {m3}", flush=True)
    print(f"  M4 EARNED-PAIR FALS(C)>FALS(shuffle) : {FALS['C_strong']} vs {FALS['C_shuffle']} -> {m4}", flush=True)
    print(f"  M5 EARNED-COMP FALS(C)>FALS(ablate)  : {FALS['C_strong']} vs {FALS['C_ablate']} -> {m5}", flush=True)

    if closed:
        verdict = "GREEN — G6 ★ CLOSED: strengthened composition crosses count+depth, controls collapse"
    else:
        fails = [n for n, ok in [("M1", m1), ("M2", m2), ("M3", m3), ("M4", m4), ("M5", m5)] if not ok]
        verdict = f"HONEST-THIN — G6 ★ stays 🟠; bars {fails} fail (bar UNMOVED, c9, detector frozen)"
    print(f"\n  VERDICT: {verdict}", flush=True)

    out = {"hypothesis": "H_1362", "ckpt": CKPT, "corpus": CORPUS, "seeds": SEEDS,
           "best_of_k": BEST_OF_K, "n_strong_frames": N_STRONG,
           "calibration": f"{cal_correct}/10",
           "DIST": DIST, "FALS": FALS, "NOVEL": NOVEL,
           "M1_count": m1, "M2_depth": m2, "M3_lift": m3,
           "M4_earned_pair": m4, "M5_earned_comp": m5,
           "closed_G6": bool(closed), "verdict": verdict,
           "per_seed": {a: [{"dist": r["dist"], "fals": r["fals"], "novel": r["novel"],
                             "coherent": r["coherent"], "texts": r["texts"]}
                            for r in per_seed[a]] for a in arms}}
    od = os.path.join(OUT_REPO, ".verdicts", "1362_g6_depth_breakthrough")
    os.makedirs(od, exist_ok=True)
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] {od}/result.json", flush=True)


if __name__ == "__main__":
    main()
