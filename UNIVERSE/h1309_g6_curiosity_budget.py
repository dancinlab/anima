#!/usr/bin/env python3
"""h1309_g6_curiosity_budget.py — G6 IDEATION depth-floor dig r2 (re-fire).
(id 1306 was taken by a concurrent ko-mitosis lane on origin/main → renumbered to 1309.)

Question (refines H_1305 🟠 THIN): a CURIOSITY-GATED MULTI-SAMPLE BUDGET — does
spending MORE draws (NOT a bigger model) under a curiosity gate cross
≥5-distinct AND ≥1-falsifiable, and is it the CURIOSITY GATE or just raw budget
that does it?

Lens (a_no_llm_frame_trap): NOT "scale the model". Instead spend an EXPLORATION
BUDGET under a substrate CURIOSITY signal (novelty + under-exposure vs the kept
set) — the biological "sample-and-select-by-curiosity" lane, not "bigger net".

For each of the 5 live G6 IDEATION_SEEDS, draw B candidate continuations (B in
the budget ladder 1/4/16/64, each draw a distinct seed_rng so it is a genuinely
different sample). Then SELECT exactly one idea per seed by ARM:
  B_curiosity : keep the candidate that MAXIMISES curiosity = novelty(corpus-
                absent content-grams) + under-exposure(low jaccard overlap vs the
                running kept set). The substrate "is this new to me?" gate.
  SHUFFLE     : random-keep one of the B candidates (SAME budget spent, NO gate).
                DECISIVE control — if random-keep also crosses the floor, the
                count gain is a SAMPLING ARTIFACT (depth still THIN).
  B_ablate    : curiosity OFF — keep the FIRST candidate (budget collapses to 1).

Then score the 5 SELECTED ideas on DIST (distinct coherent, jaccard<=0.5) and
FALS (≥1 falsifiable via the FROZEN H_1305 detector, reused VERBATIM, p7
structural-not-quality).

Reuses UNIVERSE/gauge_lib.py + the H_1305 _is_falsifiable detector VERBATIM (no
metric re-invention, no tune-to-green). 3 seeds. $0 CPU torch-mouth (the SAME
gauge_lib._decode path the live G6 gate uses). DIRECTIONAL R1 mirror (engine-
native byte-exact reconfirm = follow-on only if clean-GREEN; a_engine_native_learning).
"""
import sys, os, json, importlib.util, random, time

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA = os.path.dirname(HERE)  # repo root
CKPT = os.environ.get("H1302_CKPT", "/Users/mini/dancinlab/anima/state/chat_303m/h1129c_chat.pt")
CORPUS = os.environ.get("H1302_CORPUS", os.path.join(ANIMA, "data", "corpus.txt"))
GAUGE = os.path.join(HERE, "gauge_lib.py")
H1129 = os.path.join(HERE, "h1129_midcap_broad_converged_recombination.py")
# reuse the H_1305 frozen detector module VERBATIM (no redefinition, p7)
H1305 = os.path.join(HERE, "h1305_g6_ideation_falsifiability.py")

import torch

spec = importlib.util.spec_from_file_location("gauge", GAUGE)
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
hspec = importlib.util.spec_from_file_location("h1129", H1129)
h = importlib.util.module_from_spec(hspec); hspec.loader.exec_module(h)
h5spec = importlib.util.spec_from_file_location("h1305", H1305)
h5 = importlib.util.module_from_spec(h5spec); h5spec.loader.exec_module(h5)

_is_falsifiable = h5._is_falsifiable          # FROZEN H_1305 detector, VERBATIM
_calibrate = h5._calibrate

JACCARD_DISTINCT = 0.5   # MODEL.md G6 spec (verify303m_g6.py VERBATIM)
KWR_FLOOR = 0.50         # G0 coherence (gauge_lib)
MAX_NEW = 110            # verify303m_g6.py VERBATIM
SEEDS = [7, 4302, 4303]  # same 3 outer seeds as H_1305
# budget ladder — top budget may be CAPPED on CPU; we report the honest ceiling.
BUDGET_LADDER = [int(x) for x in os.environ.get("H1309_BUDGETS", "1,4,16,64").split(",")]
SEED_TEXTS = list(g.IDEATION_SEEDS)   # the LIVE G6 ideation seeds (flat path)


def _curiosity_score(cand_ws, cand_grams, kept_ws_list):
    """Substrate curiosity = novelty (count of corpus-absent content-grams) +
    under-exposure (1 - max jaccard overlap vs the already-kept set). Reads ONLY
    substrate state (novelty + overlap) — NO injected answer/quality label (p6)."""
    novel = sum(1 for gram in cand_grams if g._corpus_absent(gram, [CORPUS]))
    if kept_ws_list:
        max_overlap = max(g._jaccard(cand_ws, k) for k in kept_ws_list)
    else:
        max_overlap = 0.0
    under_exposure = 1.0 - max_overlap
    return novel + under_exposure, novel, under_exposure


def decode_candidates(model, cfg, seed_text, budget, outer_seed):
    """Draw `budget` distinct candidate continuations for one ideation seed.
    Each draw uses a distinct deterministic seed_rng so it is a real new sample.
    Returns list of dicts with text + precomputed ws/grams/coherent/fals."""
    cands = []
    for d in range(budget):
        # deterministic per (outer_seed, seed_text_index, draw) — reproducible
        srng = (outer_seed * 1_000_003 + hash(seed_text) % 100_003 * 97 + d * 7919) & 0x7FFFFFFF
        o = g._decode(model, seed_text, MAX_NEW, torch, block=cfg["block"], seed_rng=srng)
        coherent = g.known_word_ratio(o) >= KWR_FLOOR
        ws = set(g._words(o)) if coherent else set()
        grams = g._content_ngrams(o) if coherent else set()
        cands.append({"text": o, "coherent": coherent, "ws": ws, "grams": grams,
                      "fals": _is_falsifiable(o) if coherent else False})
    return cands


def select_arm(arm, all_cands, rng):
    """From per-seed candidate lists, SELECT one idea per seed by ARM.
    Returns list of selected candidate dicts (one per ideation seed)."""
    selected = []
    kept_ws_list = []   # running kept set (curiosity under-exposure reference)
    for cands in all_cands:
        if arm == "B_ablate":
            pick = cands[0]                       # budget collapses to first draw
        elif arm == "SHUFFLE":
            pick = rng.choice(cands)              # random-keep, same budget, NO gate
        elif arm == "B_curiosity":
            best, best_pick = None, None
            for c in cands:
                if not c["coherent"]:
                    sc = -1.0                     # incoherent never wins curiosity
                else:
                    sc, _, _ = _curiosity_score(c["ws"], c["grams"], kept_ws_list)
                if best is None or sc > best:
                    best, best_pick = sc, c
            pick = best_pick
        else:
            raise ValueError(arm)
        selected.append(pick)
        if pick["coherent"] and pick["ws"]:
            kept_ws_list.append(pick["ws"])
    return selected


def score_selected(selected):
    """DIST (distinct coherent ideas, jaccard<=0.5) + FALS (falsifiable) +
    NOVEL (corpus-absent grams) over the SELECTED idea set."""
    fals = sum(1 for c in selected if c["coherent"] and c["fals"])
    coherent_ws = [c["ws"] for c in selected if c["coherent"] and c["ws"]]
    kept = []
    for ws in coherent_ws:
        if all(g._jaccard(ws, k) <= JACCARD_DISTINCT for k in kept):
            kept.append(ws)
    dist = len(kept)
    all_grams = set()
    for c in selected:
        if c["coherent"]:
            all_grams |= c["grams"]
    novel = sum(1 for gram in all_grams if g._corpus_absent(gram, [CORPUS]))
    return {"dist": dist, "fals": fals, "novel": novel,
            "coherent": sum(1 for c in selected if c["coherent"])}


def main():
    t0 = time.time()
    dev = "cpu"
    ck = torch.load(CKPT, map_location=dev, weights_only=False); cfg = ck["config"]
    m = h.ByteGPT(d=cfg["d"], n_layer=cfg["n_layer"], n_head=cfg["n_head"], block=cfg["block"])
    m.load_state_dict(ck["model"], strict=True); m.eval(); m.grad_ckpt = False
    print(f"[mouth] {sum(p.numel() for p in m.parameters()):,} params; corpus={CORPUS}; "
          f"ladder={BUDGET_LADDER}; load+t={time.time()-t0:.1f}s", flush=True)

    cal_correct, _ = _calibrate()
    print(f"=== FROZEN H_1305 FALSIFIABILITY DETECTOR (reused verbatim) calibration = {cal_correct}/10 ===", flush=True)

    ARMS = ["B_curiosity", "SHUFFLE", "B_ablate"]
    # per[budget][arm] -> list of result dicts (one per outer seed)
    per = {B: {a: [] for a in ARMS} for B in BUDGET_LADDER}
    completed_budgets = []
    od = os.path.join(ANIMA, ".verdicts", "1309_g6_curiosity_budget")
    os.makedirs(od, exist_ok=True)

    for B in BUDGET_LADDER:
        bt0 = time.time()
        print(f"\n######## BUDGET={B} draws/seed ########", flush=True)
        for outer in SEEDS:
            # decode the candidate pool ONCE per (budget, outer seed); all arms
            # select from the SAME pool so the only difference is the SELECTION rule.
            all_cands = [decode_candidates(m, cfg, st, B, outer) for st in SEED_TEXTS]
            rng = random.Random(outer * 31 + B)   # shuffle control RNG, deterministic
            for a in ARMS:
                sel = select_arm(a, all_cands, random.Random(rng.random()))
                r = score_selected(sel)
                r["selected_texts"] = [c["text"] for c in sel]
                per[B][a].append(r)
                print(f"  [B={B:2d} {a:11s} outer={outer:5d}] DIST={r['dist']} "
                      f"FALS={r['fals']} NOVEL={r['novel']} coh={r['coherent']}/5", flush=True)
                for c in sel:
                    fl = "F" if (c["coherent"] and c["fals"]) else "."
                    print(f"        ({fl}) {c['text'][:88]!r}", flush=True)
        completed_budgets.append(B)
        # incremental commit-early checkpoint after each budget rung
        _emit_partial(od, per, completed_budgets, ARMS, cal_correct)
        print(f"  [budget {B} done in {time.time()-bt0:.1f}s; total {time.time()-t0:.1f}s]", flush=True)

    _finalize(od, per, completed_budgets, ARMS, cal_correct, t0)


def _mean(per, B, a, key):
    rows = per[B][a]
    return round(sum(r[key] for r in rows) / len(rows), 4) if rows else None


def _bars_for_budget(per, B, ARMS):
    DIST = {a: _mean(per, B, a, "dist") for a in ARMS}
    FALS = {a: _mean(per, B, a, "fals") for a in ARMS}
    NOVEL = {a: _mean(per, B, a, "novel") for a in ARMS}
    cur = "B_curiosity"
    # FROZEN bars (reuse H_1305 thresholds M1 DIST>=5, M2 FALS>=1, control-surviving)
    m1 = DIST[cur] >= 5
    m2 = FALS[cur] >= 1
    m4 = FALS[cur] >= FALS["SHUFFLE"] + 1     # EARNED-GATE vs random-keep same budget
    m5 = FALS[cur] >= FALS["B_ablate"] + 1    # EARNED-BUDGET vs budget=1 ablate
    moved = m1 and m2 and m4 and m5
    # SAMPLING-ARTIFACT flag: shuffle (random-keep, same budget) also crosses floor
    artifact = (FALS["SHUFFLE"] >= 1) or (DIST["SHUFFLE"] >= 5)
    return {"DIST": DIST, "FALS": FALS, "NOVEL": NOVEL,
            "M1_count": bool(m1), "M2_depth": bool(m2),
            "M4_earned_gate": bool(m4), "M5_earned_budget": bool(m5),
            "moved": bool(moved), "shuffle_artifact": bool(artifact)}


def _emit_partial(od, per, completed, ARMS, cal):
    out = {"partial": True, "completed_budgets": completed, "calibration": f"{cal}/10",
           "per_budget": {str(B): _bars_for_budget(per, B, ARMS) for B in completed},
           "per_seed": {str(B): {a: [{k: r[k] for k in ("dist", "fals", "novel", "coherent")}
                                     for r in per[B][a]] for a in ARMS} for B in completed}}
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)


def _finalize(od, per, completed, ARMS, cal, t0):
    print("\n================ FROZEN BARS (mean over 3 seeds, per budget) ================", flush=True)
    any_moved = False
    any_floor_cross = False     # did ANY arm cross >=1 falsifiable at ANY budget?
    bars_by_B = {}
    for B in completed:
        bars = _bars_for_budget(per, B, ARMS)
        bars_by_B[B] = bars
        cur = "B_curiosity"
        print(f"\n  --- BUDGET {B} ---", flush=True)
        for a in ARMS:
            print(f"    {a:11s}  DIST={bars['DIST'][a]}  FALS={bars['FALS'][a]}  NOVEL={bars['NOVEL'][a]}", flush=True)
        print(f"    M1 COUNT  DIST(cur)>=5         : {bars['DIST'][cur]} -> {bars['M1_count']}", flush=True)
        print(f"    M2 DEPTH  FALS(cur)>=1         : {bars['FALS'][cur]} -> {bars['M2_depth']}", flush=True)
        print(f"    M4 EARNED-GATE   FALS>=SHUF+1  : {bars['FALS'][cur]} vs {bars['FALS']['SHUFFLE']}+1 -> {bars['M4_earned_gate']}", flush=True)
        print(f"    M5 EARNED-BUDGET FALS>=ABL+1   : {bars['FALS'][cur]} vs {bars['FALS']['B_ablate']}+1 -> {bars['M5_earned_budget']}", flush=True)
        print(f"    moved={bars['moved']}  shuffle_artifact={bars['shuffle_artifact']}", flush=True)
        any_moved = any_moved or bars["moved"]
        for a in ARMS:
            if bars["FALS"][a] >= 1 or bars["DIST"][a] >= 5:
                any_floor_cross = True

    # verdict logic (frozen):
    #  MOVED      = some budget has curiosity cross M1+M2 AND beat both controls (M4,M5)
    #  ARTIFACT   = floor crossed but shuffle (random-keep) ALSO crosses -> sampling artifact, THIN
    #  CEILING    = NO arm crosses >=1 falsifiable at ANY budget -> 303M depth ceiling CONFIRMED
    if any_moved:
        verdict = ("MOVED — curiosity-gated budget crosses the G6 depth floor AND beats "
                   "both controls (the curiosity GATE is load-bearing, not raw budget)")
        tier = "GREEN-MOVE"
    elif any_floor_cross:
        # crossed somewhere but not a clean curiosity-earned move
        shuf_cross = any(bars_by_B[B]["shuffle_artifact"] for B in completed)
        if shuf_cross:
            verdict = ("HONEST-THIN — a floor crossing appears at higher budget BUT random-keep "
                       "SHUFFLE crosses it too: the count gain is a SAMPLING ARTIFACT of spending "
                       "more draws, NOT the curiosity gate. G6 depth stays 🟠 THIN (c9)")
        else:
            verdict = ("PARTIAL — curiosity crosses a floor at some budget but not all FROZEN bars "
                       "(M1/M2/M4/M5) clear together; depth signal present, bar UNMOVED (c9)")
        tier = "THIN"
    else:
        verdict = ("🧱-SCALE-BOUND — NO arm (curiosity OR shuffle OR ablate) reaches >=1 falsifiable "
                   "at ANY budget up to %d draws. Spending exploration budget does NOT buy depth at "
                   "303M: the G6 depth ceiling is CAPACITY-bound, not sampling-bound. More draws of a "
                   "303M mouth cannot synthesise a testable hypothesis it cannot represent "
                   "(capability-vs-scale thesis: depth is a capacity property, a_no_llm_frame_trap "
                   "says add a STRUCTURE lane not draws — confirmed here from the draw side)") % max(completed)
        tier = "WALL-SCALE-BOUND"

    print(f"\n  VERDICT: {verdict}", flush=True)

    out = {"partial": False, "ckpt": CKPT, "corpus": CORPUS, "seeds": SEEDS,
           "budget_ladder_requested": BUDGET_LADDER, "completed_budgets": completed,
           "calibration": f"{cal}/10", "tier": tier, "verdict": verdict,
           "any_moved": bool(any_moved), "any_floor_cross": bool(any_floor_cross),
           "per_budget": {str(B): bars_by_B[B] for B in completed},
           "per_seed": {str(B): {a: [{k: r[k] for k in ("dist", "fals", "novel", "coherent")}
                                     for r in per[B][a]] for a in ARMS} for B in completed},
           "wall_seconds": round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] {od}/result.json  ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
