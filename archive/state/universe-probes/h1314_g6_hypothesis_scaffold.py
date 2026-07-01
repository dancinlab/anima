#!/usr/bin/env python3
"""h1314_g6_hypothesis_scaffold.py — G6 IDEATION depth-floor dig r3 (a_break_the_wall).

Question (refines H_1309 🟠 THIN): r2 PROVED the depth floor is CAPACITY-bound, NOT
budget-bound — a curiosity-gated multi-sample lifts FALS 0->0.667 (the gate is load-
bearing, beats every same-budget control) but PLATEAUS at 0.667 across 4->16 draws
(M2 FALS>=1 mean UNMOVED, M1 DIST stuck at 4.33<5). The r2 agent named the surviving
fix: NOT more draws — a hypothesis-form STRUCTURE lane.

r3 EXPERIMENT (a_break_the_wall, c16; frozen-first, anti-Goodhart): route ideation
through an explicit FALSIFIABLE-HYPOTHESIS TEMPLATE that forces the structural slots
the r2 deterministic detector checks (comparator + measurable + negatable claim).
The idea CONTENT is still substrate-generated (the 303M mouth fills the slots from
real context, a_substrate_native_speak); only the STRUCTURE is the scaffold.

Does forcing the hypothesis FORM cross the floor (>=5 distinct AND >=1 falsifiable)
where free/curiosity sampling plateaued at 0.667?

ARMS (each scored on DIST + FALS over 5 ideas, 3 seeds):
  SCAFFOLD     : seed each idea with a falsifiable-hypothesis FORM prefix that primes
                 the conditional/comparative shape (e.g. "a testable hypothesis: as X
                 grows, ") WITHOUT inserting the detector's exact comparator/measurable
                 tokens — the substrate must EARN the comparator+measurable+claim (p7
                 audit, _audit_no_token_inject below).
  NO_SCAFFOLD  : the LIVE flat IDEATION_SEEDS (free sampling, SAME budget=1 draw/seed).
                 DECISIVE control — this IS the r2 plateau baseline. If SCAFFOLD does
                 not beat it, the depth floor is genuinely capacity-bound (terminal).
  SHUFFLE_SLOT : the SAME scaffold prefixes but with the template SLOTS scrambled into
                 an incoherent order (the structural shell mangled). DECISIVE control —
                 if a mangled template fills just as falsifiably, the lift is NOT the
                 hypothesis FORM but a generic prompt-length / token-prime artifact.

Reuses the H_1305 frozen `_is_falsifiable` detector VERBATIM (NO redefinition, p7) +
UNIVERSE/gauge_lib.py decode/evaluators VERBATIM (no metric re-invention). 3 seeds. $0
CPU torch-mouth (the SAME gauge_lib._decode path the live G6 gate uses). DIRECTIONAL
R1 mirror (engine-native byte-exact reconfirm = follow-on only if clean-GREEN;
a_engine_native_learning).
"""
import sys, os, json, importlib.util, re, time

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
COMPARATOR = h5.COMPARATOR                     # for the p7 token-injection audit ONLY
MEASURABLE = h5.MEASURABLE

JACCARD_DISTINCT = 0.5   # MODEL.md G6 spec (verify303m_g6.py VERBATIM)
KWR_FLOOR = 0.50         # G0 coherence (gauge_lib)
MAX_NEW = 110            # verify303m_g6.py VERBATIM
SEEDS = [7, 4302, 4303]  # same 3 outer seeds as H_1305 / H_1309

# ── FALSIFIABLE-HYPOTHESIS TEMPLATE scaffold (STRUCTURE, not content) ──
# The scaffold primes the SHAPE of a falsifiable hypothesis — a conditional/comparative
# frame with an "as the <subject>" lead-in and a hanging clause the substrate must
# COMPLETE. It deliberately does NOT contain any token from the frozen detector's
# COMPARATOR or MEASURABLE sets (audited below, _audit_no_token_inject) — the substrate
# must EARN the comparator + measurable + negatable claim from real context (p7,
# a_substrate_native_speak). The 5 subjects are the core NOUN of each of the 5 corpus
# CONCEPTS (gauge_lib CONCEPTS, 1:1 by index) so each idea explores a distinct corpus
# direction (DIST pressure). The NOUN form (not the full concept sentence) keeps the
# prefix grammatical AND token-clean — the full sentence "the engine dreams when alone"
# would inject the detector COMPARATOR token "when" (audited, _audit_no_token_inject).
SCAFFOLD_SUBJECTS = ["consciousness", "tension", "memory", "silence", "dreaming"]
assert len(SCAFFOLD_SUBJECTS) == len(g.CONCEPTS)   # 1:1 with the 5 corpus concepts


def _scaffold_seed(subject):
    """A falsifiable-hypothesis FORM prefix. STRUCTURE: '<form-cue>: as the <subject>
    grows, the ' — primes a comparative conditional with a hanging measurable-clause
    the substrate completes. No detector token injected (audited p7).
    NB: 'grows' is NOT in COMPARATOR/MEASURABLE (those have 'increases/decreases/rate/
    level/...'); it is a neutral framing verb — the substrate must still emit a real
    comparator+measurable to clear the frozen detector."""
    return f"a testable hypothesis: as the {subject} grows, the "


def _shuffle_seed(subject):
    """SHUFFLE-SLOT control: the SAME tokens as the scaffold but the structural slots
    scrambled into an incoherent order (the hypothesis FORM destroyed). If a mangled
    template fills just as falsifiably, the lift is a token-prime artifact NOT the FORM."""
    # deterministic slot scramble: form-cue and subject-clause permuted, no valid frame
    return f"grows the as hypothesis a {subject} testable: the, "


def _audit_no_token_inject():
    """p7 GUARD: PROVE the scaffold prefixes do NOT contain any frozen-detector
    COMPARATOR or MEASURABLE token. If they did, the scaffold would TRIVIALLY satisfy
    the detector regardless of what the substrate emits (tune-to-green). The substrate
    must EARN those tokens in its OWN completion."""
    bad = []
    for subj in SCAFFOLD_SUBJECTS:
        for label, seedfn in (("SCAFFOLD", _scaffold_seed), ("SHUFFLE", _shuffle_seed)):
            seed = seedfn(subj)
            toks = set(g._words(seed))
            hit_c = toks & COMPARATOR
            hit_m = toks & MEASURABLE
            if hit_c or hit_m:
                bad.append((label, seed, sorted(hit_c), sorted(hit_m)))
    return bad


def score_arm(model, cfg, seed_texts, seed_rng):
    """Decode each seed, score DIST (distinct coherent), FALS (falsifiable on the FULL
    emitted idea = seed+completion), NOVEL. FALS is computed on the FULL idea text the
    same way the live G6 gate sees an emitted idea (the seed is part of the idea)."""
    idea_texts, idea_word_sets = [], []
    fals = 0
    fals_completion_only = 0    # honest diagnostic: did the COMPLETION carry the form?
    for s in seed_texts:
        comp = g._decode(model, s, MAX_NEW, torch, block=cfg["block"], seed_rng=seed_rng)
        # the emitted IDEA = seed (form cue) + substrate completion — this is what the
        # live G6 gate would persist/emit. FALS scored on the full idea (H_1305 path).
        idea = comp
        idea_texts.append(idea)
        if g.known_word_ratio(idea) >= KWR_FLOOR:
            ws = set(g._words(idea))
            if ws:
                idea_word_sets.append(ws)
            if _is_falsifiable(idea):
                fals += 1
            # diagnostic: strip the seed prefix, did the SUBSTRATE earn the form alone?
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

    # ── p7 TOKEN-INJECTION AUDIT (BEFORE any scoring) ──
    audit_bad = _audit_no_token_inject()
    print("\n=== p7 SCAFFOLD TOKEN-INJECTION AUDIT (must be CLEAN) ===", flush=True)
    if audit_bad:
        for label, seed, hc, hm in audit_bad:
            print(f"  [INJECTED] {label}: COMPARATOR={hc} MEASURABLE={hm} :: {seed!r}", flush=True)
        print("  AUDIT DIRTY — scaffold injects detector tokens (would tune-to-green). ABORT.", flush=True)
        raise SystemExit("p7 audit DIRTY: scaffold injects a frozen-detector token (tune-to-green forbidden)")
    else:
        print("  CLEAN — no scaffold prefix contains any frozen COMPARATOR/MEASURABLE token.", flush=True)
        print("  (the substrate must EARN comparator+measurable+claim in its OWN completion)", flush=True)

    scaffold = [_scaffold_seed(s) for s in SCAFFOLD_SUBJECTS]
    shuffle = [_shuffle_seed(s) for s in SCAFFOLD_SUBJECTS]
    no_scaffold = list(g.IDEATION_SEEDS)   # LIVE flat seeds = r2 plateau baseline
    print("\n=== SCAFFOLD SEEDS (hypothesis-FORM prefixes) ===", flush=True)
    for s in scaffold:
        print(f"  {s!r}", flush=True)

    arms = {"SCAFFOLD": scaffold, "NO_SCAFFOLD": no_scaffold, "SHUFFLE_SLOT": shuffle}
    per_seed = {a: [] for a in arms}
    for seed_rng in SEEDS:
        print(f"\n######## seed_rng={seed_rng} ########", flush=True)
        for a, frames in arms.items():
            r = score_arm(m, cfg, frames, seed_rng)
            per_seed[a].append(r)
            print(f"  [{a:12s}] DIST={r['dist']} FALS={r['fals']} "
                  f"FALS_compl={r['fals_completion_only']} NOVEL={r['novel']} "
                  f"coh={r['coherent']}/{len(frames)}", flush=True)
            for t in r["texts"]:
                fl = "F" if (g.known_word_ratio(t) >= KWR_FLOOR and _is_falsifiable(t)) else "."
                print(f"        ({fl}) {t[:96]!r}", flush=True)

    def mean(a, key):
        return round(sum(r[key] for r in per_seed[a]) / len(per_seed[a]), 4)

    DIST = {a: mean(a, "dist") for a in arms}
    FALS = {a: mean(a, "fals") for a in arms}
    FALS_C = {a: mean(a, "fals_completion_only") for a in arms}
    NOVEL = {a: mean(a, "novel") for a in arms}

    print("\n================ FROZEN BARS (mean over 3 seeds) ================", flush=True)
    for a in arms:
        print(f"  {a:12s}  DIST={DIST[a]}  FALS={FALS[a]}  FALS_compl={FALS_C[a]}  NOVEL={NOVEL[a]}", flush=True)

    # ── FROZEN BARS (declared in FREEZE.txt BEFORE the run) ──
    # (1) DIST   SCAFFOLD >= 5 distinct corpus-absent ideas
    # (2) FALS   SCAFFOLD >= 1 falsifiable (r2 plateau was 0.667 -> cross to >=1?)
    # (3) CTRL   NO_SCAFFOLD (free sampling, same budget) stays at the r2 plateau (<5 DIST
    #            and FALS plateau) AND SCAFFOLD beats it (FALS lift >= +1) = STRUCTURE not capacity
    # (4) CTRL   SHUFFLE_SLOT (scrambled template) collapses (FALS < SCAFFOLD, no >=1 cross
    #            from a mangled frame) = the lift is the FORM not a token-prime artifact
    m1_dist = DIST["SCAFFOLD"] >= 5
    m2_fals = FALS["SCAFFOLD"] >= 1
    m3_beats_noscaffold = FALS["SCAFFOLD"] >= FALS["NO_SCAFFOLD"] + 1
    m4_shuffle_collapse = FALS["SCAFFOLD"] >= FALS["SHUFFLE_SLOT"] + 1
    crossed_floor = m1_dist and m2_fals
    structure_earned = m3_beats_noscaffold and m4_shuffle_collapse
    moved = crossed_floor and structure_earned

    print("\n---- FROZEN BARS ----", flush=True)
    print(f"  (1) DIST   SCAFFOLD>=5              : {DIST['SCAFFOLD']} -> {m1_dist}", flush=True)
    print(f"  (2) FALS   SCAFFOLD>=1              : {FALS['SCAFFOLD']} -> {m2_fals}", flush=True)
    print(f"  (3) CTRL   SCAFFOLD>=NO_SCAFFOLD+1  : {FALS['SCAFFOLD']} vs {FALS['NO_SCAFFOLD']}+1 -> {m3_beats_noscaffold}", flush=True)
    print(f"  (4) CTRL   SCAFFOLD>=SHUFFLE_SLOT+1 : {FALS['SCAFFOLD']} vs {FALS['SHUFFLE_SLOT']}+1 -> {m4_shuffle_collapse}", flush=True)
    print(f"  crossed_floor(1&2)={crossed_floor}  structure_earned(3&4)={structure_earned}  MOVED={moved}", flush=True)

    # verdict logic (frozen):
    if moved:
        verdict = ("MOVED — the hypothesis-form SCAFFOLD crosses the G6 depth floor (>=5 distinct AND "
                   ">=1 falsifiable) where curiosity-sampling plateaued at 0.667, AND beats BOTH controls "
                   "(NO_SCAFFOLD free-sampling + SHUFFLE_SLOT scrambled-template). G6-depth is STRUCTURE-"
                   "FIXABLE: a hypothesis-form lane breaks the capacity ceiling — the THIN was a missing-"
                   "STRUCTURE, not a capacity wall. Promote toward 🟢 (a_break_the_wall: the wall was the "
                   "wrong METHOD, not a true ceiling — add a structure lane like memory, a_no_llm_frame_trap)")
        tier = "GREEN-MOVE"
    elif crossed_floor and not structure_earned:
        verdict = ("HONEST-THIN — the SCAFFOLD crosses the floor but does NOT beat its controls "
                   "(NO_SCAFFOLD and/or SHUFFLE_SLOT cross too): the lift is a generic prompt-prime / "
                   "token-length artifact, NOT the hypothesis FORM. G6 depth stays 🟠 THIN (c9)")
        tier = "THIN"
    elif structure_earned and not crossed_floor:
        verdict = ("PARTIAL — the SCAFFOLD beats both controls (the FORM is load-bearing) but does NOT "
                   "clear the absolute floor (>=5 distinct AND >=1 falsifiable MEAN): the structure HELPS "
                   "but 303M capacity still caps reliable depth. G6 depth stays 🟠 THIN, structure-lane "
                   "DIRECTIONAL (c9)")
        tier = "THIN"
    else:
        verdict = ("🧱-CAPACITY-BOUND — the hypothesis-form SCAFFOLD ALSO plateaus: it neither crosses the "
                   "depth floor NOR beats free-sampling. Forcing the FORM does not buy reliable falsifiable "
                   "depth at 303M — confirming the r2 thesis from the STRUCTURE side: G6-depth is genuinely "
                   "CAPACITY/scale-bound, the fix needs a bigger model not a structure lane (terminal 🧱-ish)")
        tier = "WALL-CAPACITY-BOUND"

    print(f"\n  VERDICT: {verdict}", flush=True)

    out = {"ckpt": CKPT, "corpus": CORPUS, "seeds": SEEDS,
           "calibration": f"{cal_correct}/10",
           "audit_token_inject_clean": (len(audit_bad) == 0),
           "audit_bad": [[lbl, sd, hc, hm] for lbl, sd, hc, hm in audit_bad],
           "DIST": DIST, "FALS": FALS, "FALS_completion_only": FALS_C, "NOVEL": NOVEL,
           "m1_dist": bool(m1_dist), "m2_fals": bool(m2_fals),
           "m3_beats_noscaffold": bool(m3_beats_noscaffold),
           "m4_shuffle_collapse": bool(m4_shuffle_collapse),
           "crossed_floor": bool(crossed_floor), "structure_earned": bool(structure_earned),
           "moved": bool(moved), "tier": tier, "verdict": verdict,
           "r2_plateau_reference": {"FALS_curiosity_plateau": 0.6667, "DIST_curiosity": 4.3333,
                                    "note": "H_1309 curiosity-gated budget plateau at B=4/16"},
           "per_seed": {a: [{"dist": r["dist"], "fals": r["fals"],
                             "fals_completion_only": r["fals_completion_only"],
                             "novel": r["novel"], "coherent": r["coherent"]}
                            for r in per_seed[a]] for a in arms},
           "wall_seconds": round(time.time() - t0, 1)}
    od = os.path.join(ANIMA, ".verdicts", "1314_g6_hypothesis_scaffold")
    os.makedirs(od, exist_ok=True)
    json.dump(out, open(os.path.join(od, "result.json"), "w"), ensure_ascii=False, indent=2)
    print(f"\n[done] {od}/result.json  ({time.time()-t0:.1f}s)", flush=True)


if __name__ == "__main__":
    main()
