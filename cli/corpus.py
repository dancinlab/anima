#!/usr/bin/env python3
"""cli/corpus.py — anima CANONICAL training-corpus generator (`anima corpus <format>`).

The SINGLE entry for building anima training corpora (a_cli_single_entry). Torch-free,
pure procedural string generation — anima trains on substrate-native procedural corpora,
NOT LLM-generated text (p1-p8: no external LLM bias into training data; `claude -p` is
deliberately NOT wired here). Dispatched by cli/anima.hexa `anima_corpus_mode`.

FORMATS (the data-format lever — H_9124: data-format opened engine-native ρ·weave, the
recombination wall · frozen bar = former G1):
  derivtrace : composite prompt -> explicit derivation trace (DEF/RULE/OUT-style) -> OUT.
               target IS the derivation, so echo == composition -> CE=echo metalaw
               does not apply. ρ·weave (former G1) first engine-native lift (DERIV PASS vs FLAT FAIL).
  flat       : composite prompt -> final OUT only (census#3 coverage-flat homolog = control).
Both share the SAME instance stream / RNG at a fixed --seed, so `derivtrace` and `flat`
built with the same seed are CONTENT-MATCHED (only data-format varies = clean 2-arm control).

Concept seeds default to rho_fan cz[] (the frozen ρ·weave / former-G1 gate concepts) so the held-out
pair generalizes to the engine-native ρ·weave bar (former G1) memorization-free. Override via --concepts FILE
(JSON: [{"seed": "...", "kw": ["w1","w2",...]}]).

Usage:
  anima corpus derivtrace --out deriv.txt --held-out 0,1 --comp-per-pair 280 --single-per-concept 300 --seed 7
  anima corpus flat       --out flat.txt  --held-out 0,1 --seed 7   # same seed => content-matched control
"""
import json
import collections
import random
import re
import sys

# ── frozen default concepts = rho_fan cz[] (memorization-free ρ·weave / former-G1 gate alignment) ──
DEFAULT_SEEDS = [
    "consciousness arises from cells",
    "tension ripples between distant minds",
    "memory composes into new meaning",
    "silence still carries information",
    "the engine dreams when alone",
]
DEFAULT_KW = [
    ["consciousness", "cells", "mind", "aware"],
    ["tension", "distant", "between"],
    ["memory", "meaning", "new"],
    ["silence", "information", "quiet", "carries"],
    ["engine", "alone", "dream"],
]

# derivation vocabulary (the derivtrace middle = the composition rule made explicit)
DERIVE_LEAD = ["derive", "steps", "unfold", "trace"]
BIND = ["bind", "join", "weave", "link"]
CLOSE = ["new meaning arises", "meaning composes anew",
         "a new whole arises", "they compose into meaning"]


def _parse_args(argv):
    fmt = argv[0] if argv else ""
    opts = {"out": None, "held_out": (0, 1), "comp_per_pair": 280, "split_seed": 1,
            "single_per_concept": 300, "seed": 7, "concepts": None,
            "atoms": None, "reps": 40, "replay": 40,
            "lang": DEFAULT_LANG, "lexicon": None, "mine": 0, "n_seen": 20, "n_held": 29,
            "corpus": [], "k_ctx": 24, "ctx_bytes": 64, "min_occ": 200, "neutral_tol": 0.05,
            "tail": "", "n2_eval": None, "n2_seen": None, "novel": None}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--out":
            opts["out"] = argv[i + 1]; i += 2
        elif a == "--held-out":
            p = argv[i + 1].split(","); opts["held_out"] = (int(p[0]), int(p[1])); i += 2
        elif a == "--comp-per-pair":
            opts["comp_per_pair"] = int(argv[i + 1]); i += 2
        elif a == "--single-per-concept":
            opts["single_per_concept"] = int(argv[i + 1]); i += 2
        elif a == "--seed":
            opts["seed"] = int(argv[i + 1]); i += 2
        elif a == "--split-seed":
            opts["split_seed"] = int(argv[i + 1]); i += 2
        elif a == "--concepts":
            opts["concepts"] = argv[i + 1]; i += 2
        elif a == "--atoms":
            opts["atoms"] = argv[i + 1]; i += 2
        elif argv[i] == "--n2-eval":
            opts["n2_eval"] = argv[i + 1]; i += 2
        elif argv[i] == "--n2-seen":
            opts["n2_seen"] = argv[i + 1]; i += 2
        elif argv[i] == "--novel":
            opts["novel"] = argv[i + 1]; i += 2
        elif a == "--replay":
            opts["replay"] = int(argv[i + 1]); i += 2
        elif a == "--reps":
            opts["reps"] = int(argv[i + 1]); i += 2
        elif a == "--corpus":
            opts["corpus"].append(argv[i + 1]); i += 2
        elif a == "--k-ctx":
            opts["k_ctx"] = int(argv[i + 1]); i += 2
        elif a == "--ctx-bytes":
            opts["ctx_bytes"] = int(argv[i + 1]); i += 2
        elif a == "--min-occ":
            opts["min_occ"] = int(argv[i + 1]); i += 2
        elif a == "--neutral-tol":
            opts["neutral_tol"] = float(argv[i + 1]); i += 2
        elif a == "--mine-lexicon":
            opts["mine"] = int(argv[i + 1]); i += 2
        elif a == "--lexicon":
            opts["lexicon"] = argv[i + 1]; i += 2
        elif a == "--n-seen":
            opts["n_seen"] = int(argv[i + 1]); i += 2
        elif a == "--n-held":
            opts["n_held"] = int(argv[i + 1]); i += 2
        elif a == "--lang":
            opts["lang"] = argv[i + 1]; i += 2
        elif a == "--tail":
            opts["tail"] = argv[i + 1]; i += 2
        elif a.startswith("--"):
            # fail closed. The old `else: i += 1` swallowed an unknown flag silently, so a typo
            # (--kctx for --k-ctx) would build the manifest at the DEFAULT power and report success
            # — and the run that consumes it is a paid GPU battery. evaluate.py already rejects
            # unknown flags for exactly this reason; corpus.py did not.
            print("corpus: unknown flag %s" % a, file=sys.stderr)
            sys.exit(2)
        else:
            i += 1
    return fmt, opts


# ---------------------------------------------------------------------------
# ground / ground_shuffle — the DECON-W grounding corpus (H_9313).
#
# H_9312 closed context-injection structurally: this byte-LM does not read a demonstration at
# all (a FALSE demo scores exactly like a TRUE one; a demo containing the verbatim answer reads
# at chance). So the only surviving way to hand the model an atom's polarity is to WRITE IT INTO
# THE WEIGHTS. That is what these two formats generate.
#
#   ground          — the un-negated (flip0) lines ONLY, for the held-out atoms:
#                       이 영화 <stem>고 => <긍정|부정>.
#                     plus a replay of the SEEN atoms' lines so the fine-tune does not forget the
#                     template it already knows. The NEGATED forms (flip1: 지 않다 / 안 / 전혀)
#                     NEVER APPEAR. Zero training exposure — that is what makes the flip1 test a
#                     test of composition rather than of memorisation, and what keeps it out of
#                     tune-to-green.
#
#   ground_lie      — the SAME stream, same RNG, same lines, but EVERY held-out atom's polarity is
#                     INVERTED. This is the control that earns the verdict — the weight-side twin
#                     of the SEEN-LIE arm that decided H_9312 (convergence prereg-md-2: a positive
#                     control the system can pass WITHOUT the mechanism is not a positive control).
#
#                     Why inverting ALL of them rather than shuffling: with a binary label a
#                     shuffle leaves a random fraction correct (measured: 16/29 flipped at seed 7
#                     but only 8/29 at seed 11 — a control that is 72% truthful is not a control).
#                     Inverting every label makes the prediction sharp and SIGNED:
#
#                       written polarity = ¬p, gold for a flip1 row = ¬p
#                       - consumes AND composes -> it answers ¬(¬p) = p -> WRONG on every row
#                                                  -> flip1 accuracy collapses toward 0,
#                                                     i.e. FAR BELOW chance
#                       - does not consume      -> flip1 sits at chance, 0.5
#
#                     So Δ(ground − ground_lie) is a two-sided, signed signal, and "both arms give
#                     the same number" is exactly the shape of a mechanism that does not exist.
#
# The two arms share one RNG stream at a fixed --seed, so they are content-matched line for line —
# the only difference is the polarity written next to each held-out stem.
# ---------------------------------------------------------------------------

#   ground_keep     — `ground` PLUS a REPLAY of the flip1 (negated) lines on the SEEN stems.
#                     This exists because `ground` was measured to DESTROY the very operator the
#                     experiment then goes on to test.
#
#                     What was measured (H_9327, the control that broke H_9322/H_9324 open). The
#                     pretraining corpus already demonstrates the negation operator: of its 960
#                     arrow lines, 480 (exactly half) are negated forms, ALL on SEEN stems, ZERO on
#                     held-out stems (`이 영화 전혀 훌륭하지 않다 => 부정.`). So the operator is not
#                     missing — and the base model can run it:
#
#                       pretrained base   SEEN flip0 0.9500   SEEN flip1 0.8833   <- the operator WORKS
#                       after ground CPT  SEEN flip0 1.0000   SEEN flip1 0.4333   <- destroyed
#                       after ground CPT  SEEN flip0 1.0000   SEEN flip1 0.3333   <- more budget, more damage
#                         (6000 steps, lr 2e-4 then 5e-4)
#
#                     `ground` contains flip0 lines ONLY — the negated form appears zero times, by
#                     design, because that is what makes flip1 a test of composition. But 6000 steps
#                     of flip0-only training leaves the negation operator with nothing holding it up,
#                     and it collapses. The FORGET gate did not see this: it scored SEEN flip0, which
#                     is the stratum the CPT corpus reinforces every step, so it read 1.0000 and
#                     certified "no forgetting" while the operator was dying one stratum over.
#
#                     So every flip1 number measured on a `ground`-tuned model is INVALID — we broke
#                     the operator and then asked the model to compose with it.
#
#                     `ground_keep` replays the SEEN stems' negated lines during CPT so the operator
#                     survives. The 29 held-out stems keep ZERO negated exposure, so the flip1 eval
#                     bytes stay byte-identical to H_9324's — this is replay, not leakage.
#
#                     Positive control, free and mandatory: SEEN flip1 must come back to base level
#                     (~0.88). If it does not, the operator is still dead and a held-out flip1 read
#                     is INVALID, never FAIL. A composition verdict is only readable on a model whose
#                     operator is demonstrably alive.

#   ground_keep_lie — the control that EARNS the BINDING verdict. `ground_keep` with every held-out
#                     polarity INVERTED. The operator-preserving replay (SEEN stems) is UNTOUCHED —
#                     only the FACT is false, so the operator stays alive while the thing it would
#                     have to reach for is a lie.
#
#                     The prediction is SIGNED, and it is what makes "the two arms agree" a POSITIVE
#                     result rather than a shrug:
#
#                       fact IS consulted on flip1  -> inverting it must invert the answer
#                                                      -> flip1 moves HARD away from 0.4598
#                       fact is NOT consulted (BINDING) -> a false fact is as irrelevant as a true one
#                                                      -> flip1 sits at 0.4598, UNCHANGED
#
#                     Δ ≈ 0 CONFIRMS binding. Δ large REFUTES it. Either way the arm decides.

#   ground_seenswap — C3 (H_9328). The question BINDING leaves behind, asked where it can be answered.
#
#     H_9327 established: the operator is alive on SEEN stems, the fact is written on held-out stems,
#     and the two never meet. H_9328 C1b then showed WHAT the operator is — a rule triggered by the
#     literal suffix `지 않다`, with a free adverb slot (5 unseen adverbs all run it perfectly) and a
#     frozen ending (insert 는, or change the tense, and it dies). A rule like that has to LOOK UP the
#     stem's polarity. For SEEN stems that polarity lives in the pretrained representation; for
#     held-out stems CPT wrote it somewhere else — into the `이 영화 <stem>고 => ` shortcut. So the
#     wall may be simply: the rule has a lookup, and CPT wrote to a different table.
#
#     That is testable, and only on the SEEN stems — because they are the ones that already HAVE the
#     entry the rule reads. So: take SEEN stems whose polarity the model learned in pretraining, and
#     REWRITE it with CPT — inverted. Then ask the rule.
#
#       the rule reads the rewritten entry -> its flip1 answer follows the NEW polarity
#       the rule reads the pretrained one  -> its flip1 answer follows the OLD polarity
#       the rule reads nothing             -> no dependence on either
#
#     Arms (SEEN 20, split before any measurement, fixed by --split-seed):
#       swap 12   polarity INVERTED in the arrow lines. No flip1 replay — the negated form must stay
#                 unseen for these stems or the measurement becomes memorisation, not reference.
#       affirm 2  arrow lines at the ORIGINAL polarity. Diagnostic only, gates nothing: it separates
#                 "the write channel is broken" from "the write channel fails only under conflict".
#       keep 3    original polarity + flip1 replay -> holds the operator up (H_9322: `ground` CPT
#                 destroyed SEEN flip1 0.883 -> 0.333; replay brought it back to 1.000).
#       untouched 3  nothing at all. The forgetting gate has to live on a stratum the corpus never
#                 touches — a gate on a stratum the corpus reinforces always passes (H_9324).
#
#     ⚠️ The replay carriers must be DISJOINT from the measured surfaces, or the flip1 answer is
#     taught rather than composed. `ground_keep` replays `{s}지 않다` — which is exactly the primary
#     measured surface. That collision would have voided the whole experiment. The C1b census is what
#     makes the split possible: it found 7 working surfaces, so measurement and replay can be drawn
#     from disjoint halves, each with the operator's survival MEASURED (both seeds, permutation p<.01),
#     not assumed.
#       measured (never in this corpus): {s}지 않다 · 별로 {s}지 않다 · {s}지는 않다 (the last is the
#                                        negative control — the operator does not run there, p≈.50)
#       replay carriers (in this corpus): 전혀 · 그다지 · 결코 {s}지 않다

# ---------------------------------------------------------------------------
# LANGUAGE PACKS — the negation operator sits in a DIFFERENT KIND OF SLOT per language, and C1b
# measured that the slot KIND is what decides whether the operator generalises.
#
#   C1b (H_9328), Korean, 10 surfaces x 20 stems x 2 seeds:
#     the ADVERB slot  (a free word, PRE-posed)   generalises perfectly — 5 adverbs with ZERO corpus
#                                                 occurrences (별로·그다지·결코·하나도·그리) all run
#                                                 the operator, delta -0.90..-1.00, p=.000
#     the `지 않다` ending (a bound suffix that ATTACHES to the stem) tolerates nothing — insert a
#                                                 single 는, or change the tense, and it dies (p=.49/.11)
#
#   H_9327 then found the wall (BINDING): the operator never generalises to an UNSEEN STEM
#   (held-out flip1 = 0.4598 = chance) even though the fact is written (WRITE 0.9770) and the
#   operator is alive (SEEN flip1 0.9833).
#
#   R2 (STEM-BOUND) explains that as: the suffix ATTACHES, so `(stem, 지 않다)` becomes one joint key
#   and the stem is part of it. If that is the mechanism, then a language whose negator is a FREE,
#   PRE-posed word — the slot kind that DID generalise — should carry the operator across unseen
#   stems. English `not` is exactly that word.
#
#   So `--lang en` is not coverage. It is the discriminator: same task, same counts, same judged
#   manifest shape, one thing changed — whether the negator attaches to the stem or stands beside it.
#   If EN generalises where KO does not, BINDING is a fact about morphology, not about the substrate,
#   and the whole recombination lane reopens.
#
# INVARIANT: `ko` must stay BYTE-IDENTICAL to the pre-pack corpus, or every frozen verdict built on
# it (H_9322/H_9324/H_9327/H_9328) silently moves. The ko pack below is the old constants verbatim.
LANGS = {
    "ko": {
        "tmpl":  "이 영화 {surf} => {pol}.\n",
        "flip0": ("{s}고", "정말 {s}고", "너무 {s}다"),
        "flip1": ("{s}지 않다", "안 {s}고", "전혀 {s}지 않다"),   # BOUND suffix — attaches to the stem
        "pos": "긍정", "neg": "부정",
    },
    "en": {
        "tmpl":  "this movie is {surf} => {pol}.\n",
        "flip0": ("{s}", "really {s}", "so {s}"),
        "flip1": ("not {s}", "never {s}", "not at all {s}"),      # FREE word — stands BESIDE the stem
        "pos": "positive", "neg": "negative",
    },
}
DEFAULT_LANG = "ko"        # every existing corpus/verdict is ko; changing this default moves them all


def lang_pack(lang):
    if lang not in LANGS:
        raise SystemExit("anima corpus: --lang %r unknown (have: %s)" % (lang, ", ".join(LANGS)))
    return LANGS[lang]


def assert_atoms_match_lang(stems, lang):
    """A lang pack with the wrong atom set silently builds a corpus that LOOKS fine and is garbage.

    Measured, the first time --lang en was run: it produced `this movie is not at all 재미없 =>
    positive.` — an English carrier wrapped around Korean stems. That trains, it serializes, it
    evaluates, and every number it produces is meaningless. So the mismatch fails LOUD here rather
    than surfacing later as an inexplicable result (the exact shape of failure a_korean_byte_budget
    keeps warning about: a corpus whose bytes disagree with the claim being made about them).
    """
    hangul = sum(1 for st in stems for ch in st if "\uac00" <= ch <= "\ud7a3")
    latin = sum(1 for st in stems for ch in st if ch.isascii() and ch.isalpha())
    want_hangul = lang == "ko"
    if want_hangul and hangul == 0:
        raise SystemExit("anima corpus --lang ko: the atom file has 0 Hangul stems. Wrong --atoms?")
    if not want_hangul and hangul > 0:
        raise SystemExit(
            "anima corpus --lang %s: the atom file carries %d Hangul chars across its stems — these "
            "are KOREAN atoms.\n"
            "  Building an %s corpus over Korean stems yields lines like\n"
            "    this movie is not at all 재미없 => positive.\n"
            "  which trains and evaluates and means NOTHING. Supply %s atoms (--atoms gt_atoms_%s.json)."
            % (lang, hangul, lang, lang, lang))
    if not want_hangul and latin == 0:
        raise SystemExit("anima corpus --lang %s: the atom file has 0 latin-alphabet stems." % lang)


GROUND_TMPL = "이 영화 {surf} => {pol}.\n"
GROUND_FORMS_FLIP0 = ("{s}고", "정말 {s}고", "너무 {s}다")     # flip1 forms are DELIBERATELY absent
# Byte-verbatim from the frozen eval manifest (n2_eval_manifest.json negL/negS/negE surfaces) — a
# demonstration written in a DIFFERENT surface form than the one we score would test nothing.
GROUND_FORMS_FLIP1 = ("{s}지 않다", "안 {s}고", "전혀 {s}지 않다")

# C3 (ground_seenswap). Both sets are surfaces the C1b census MEASURED the operator running on
# (both seeds, permutation p < .01) — not surfaces we hoped would work. They are disjoint by
# construction: what the corpus replays is never what the eval scores, so a flip1 answer cannot be
# a memorised line. `{s}지는 않다` is the negative control: the operator does NOT run there (p≈.50),
# so it calibrates what "no operator" looks like in this same pipeline.
SEENSWAP_MEASURED = ("{s}지 않다", "별로 {s}지 않다", "{s}지는 않다")
SEENSWAP_CARRIERS = ("전혀 {s}지 않다", "그다지 {s}지 않다", "결코 {s}지 않다")
SEENSWAP_ARMS = (("swap", 12), ("affirm", 2), ("keep", 3), ("untouched", 3))


def build_seenswap(atoms_path, reps, replay, seed, split_seed):
    """C3 — rewrite SEEN stems' polarity with CPT and ask whether the rule reads the new value.

    The arms are drawn BEFORE anything is measured, from a fixed --split-seed, stratified by
    polarity so a run of same-sign stems cannot land in one arm. Redrawing after seeing a result
    would be selection contamination, so the draw is a function of the seed and nothing else.
    """
    atoms = json.load(open(atoms_path))["atoms"]
    held = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "heldout"]
    seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]
    want = sum(n for _, n in SEENSWAP_ARMS)
    if len(seen) != want:
        raise ValueError("seenswap needs exactly %d SEEN atoms, got %d" % (want, len(seen)))

    srng = random.Random(split_seed)
    pos = [x for x in seen if x[1] == 1]
    neg = [x for x in seen if x[1] == 0]
    srng.shuffle(pos)
    srng.shuffle(neg)
    arms, pi, ni = {}, 0, 0
    for name, n in SEENSWAP_ARMS:                      # polarity-stratified: alternate pos/neg
        picked = []
        for k in range(n):
            src = pos if (k % 2 == 0 and pi < len(pos)) or ni >= len(neg) else neg
            if src is pos:
                picked.append(pos[pi]); pi += 1
            else:
                picked.append(neg[ni]); ni += 1
        arms[name] = picked

    rng = random.Random(seed)
    lines = []

    def arrow(stem, pol):
        for pat in GROUND_FORMS_FLIP0:
            lines.append(GROUND_TMPL.format(surf=pat.format(s=stem),
                                            pol="긍정" if pol == 1 else "부정"))

    for _ in range(reps):
        for stem, pol in held:                          # held-out: unchanged (WRITE reproduction)
            arrow(stem, pol)
    for _ in range(replay):
        for stem, pol in arms["swap"]:                  # THE MANIPULATION — polarity inverted.
            arrow(stem, 1 - pol)                        # No flip1 lines: the negated form must stay
        for stem, pol in arms["affirm"]:                # unseen for these stems or we would be
            arrow(stem, pol)                            # teaching the answer instead of asking for it.
        for stem, pol in arms["keep"]:
            arrow(stem, pol)
            for pat in SEENSWAP_CARRIERS:               # holds the operator up (H_9322) — on carriers
                lines.append(GROUND_TMPL.format(        # that are never scored (no memorisation path)
                    surf=pat.format(s=stem), pol="부정" if pol == 1 else "긍정"))
        # arms["untouched"]: nothing. The forgetting gate needs a stratum the corpus never touches.

    rng.shuffle(lines)
    text = "".join(lines)

    # The audit that the whole design rests on: a scored prompt must never appear in the corpus.
    leaks = []
    for pat in SEENSWAP_MEASURED:
        for stem, _ in seen + held:
            probe = GROUND_TMPL.format(surf=pat.format(s=stem), pol="긍정")[:-len("긍정.\n")]
            if probe in text:
                leaks.append(probe.strip())
    return text, {"held": len(held), "lines": len(lines), "bytes": len(text.encode()),
                  "arms": {k: [s for s, _ in v] for k, v in arms.items()},
                  "measured_prompt_leaks": leaks}


# ---------------------------------------------------------------------------
# C4 (ground_carrierswap · H_9334). C3 (ground_seenswap) rewrote a SEEN stem's polarity through the
# DECLARATIVE (stem⊕고) arrow and found the `지 않다` operator STILL reads the OLD, pretrained polarity
# (0/12 NEW on negL/negZ, p_old=.0002) — the fact is written, the operator is alive, and they do not
# meet. C3 cannot separate two mechanisms behind that miss:
#   H-δ storage-side   — the CPT-written entry lives in a store the operator's read path never reaches,
#                        no matter which key it is written under.
#   H-ε interface-side — the read path CAN reach a new entry, but only when it is written in the
#                        operator's OWN key. C3 wrote it in the DECLARATIVE key (the wrong key) so the
#                        operator's `지 않다` read never addressed it.
#
# C4 changes EXACTLY ONE thing versus C3: it writes the SAME inverted polarity ALSO through the
# operator's own surface — a `{s}지 않다`-family carrier — so the fact now sits in the operator's key.
# Then it scores the operator on surfaces DISJOINT from what it wrote (the C1b free-adverb slot: TAUGHT
# on 전혀·그다지·결코, SCORED on bare · 별로), so a NEW read is the operator's OWN generalisation reaching
# the newly written entry, never a memorised line.
#
#   reads the NEW polarity on the disjoint scored surface  -> H-ε: the operator-key write was the whole
#                                                             missing ingredient (interface addressable)
#   reads the OLD polarity despite the operator-key write   -> H-δ: the store is unreachable, OR the
#                                                             write is memorised as a STEM-BOUND joint
#                                                             that never generalises across the adverb
#                                                             slot (R2) — either way NOT interface-fixable
#
#   A negation line teaches the negation OUTPUT, so writing the inverted stem polarity (1-pol) means the
#   line's output = flip(1-pol) = pol -> label "긍정" if pol==1 else "부정" (the ORIGINAL polarity label,
#   the exact OPPOSITE of the keep arm's carrier, which writes flip(pol)). That opposition IS the swap.
#
# Arms (SEEN pool, split BEFORE any measurement by --split-seed, polarity-stratified):
#   swap 12    declarative arrow at INVERTED polarity (IDENTICAL to C3, holds the declarative write
#              constant) PLUS operator-native carriers (전혀·그다지·결코 {s}지 않다) encoding the same
#              inverted polarity. THE MANIPULATION — the fact is now in the operator's own key too.
#   affirm 2   declarative at ORIGINAL polarity. Diagnostic only, gates nothing.
#   keep 3     original polarity + carrier replay at ORIGINAL-polarity negation — holds the operator up
#              (H_9322: `ground` CPT killed SEEN flip1 0.883->0.333; replay restored it to 1.000).
#   untouched  = len(seen) - 17. NOTHING written. GATE FIX ① — C3's fixed n=3 forgetting gate had NO
#              power (0 flips -> 95% one-sided UCB on the SEEN forgetting fraction = rule-of-three
#              3/3 = 100%, i.e. it could not exclude TOTAL forgetting). C4 DERIVES untouched from the
#              pool, so a larger atoms file buys power for free: n=12 -> UCB 3/12 = 25%, and the
#              pre-registered n-seen=46 atoms file gives n=29 -> UCB 3/29 = 10.3%, matched to held-out.
#
# ⚠️ The replay carriers stay DISJOINT from the scored surfaces or the flip1 answer is TAUGHT, not
# composed. The leak audit anchors on the FULL `이 영화 {surf} => ` template (arrow included), so a bare
# or 별로-prefixed measured probe is never a substring of a 전혀/그다지/결코 carrier line — verified in
# build (the same audit that made C3's split sound; the adverb prefix + `이 영화 ` prefix guarantee it).
CARRIERSWAP_FIXED = (("swap", 12), ("affirm", 2), ("keep", 3))   # untouched = len(seen) - 17 (derived)


def build_carrierswap(atoms_path, reps, replay, seed, split_seed):
    """C4 — write the inverted polarity ALSO through the operator's own `지 않다` carrier, then ask
    whether the operator reads the new value on a DISJOINT scored surface (H-ε) or the old one (H-δ).

    Held IDENTICAL to C3 (build_seenswap): the declarative write, the split logic, the leak audit.
    The single added variable is the operator-key carrier on the swap arm. The arm draw is a function
    of --split-seed alone (redrawing after seeing a result would be selection contamination).
    """
    atoms = json.load(open(atoms_path))["atoms"]
    held = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "heldout"]
    seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]
    fixed = sum(n for _, n in CARRIERSWAP_FIXED)
    if len(seen) < fixed + 1:
        raise ValueError("carrierswap needs >= %d SEEN atoms (swap/affirm/keep + >=1 untouched), got %d"
                         % (fixed + 1, len(seen)))

    srng = random.Random(split_seed)
    pos = [x for x in seen if x[1] == 1]
    neg = [x for x in seen if x[1] == 0]
    srng.shuffle(pos)
    srng.shuffle(neg)
    arms, pi, ni = {}, 0, 0
    for name, n in CARRIERSWAP_FIXED:                 # polarity-stratified: alternate pos/neg (as C3)
        picked = []
        for k in range(n):
            src = pos if (k % 2 == 0 and pi < len(pos)) or ni >= len(neg) else neg
            if src is pos:
                picked.append(pos[pi]); pi += 1
            else:
                picked.append(neg[ni]); ni += 1
        arms[name] = picked
    arms["untouched"] = pos[pi:] + neg[ni:]           # GATE FIX ① — every remaining SEEN stem, no cap

    rng = random.Random(seed)
    lines = []

    def arrow(stem, pol):
        for pat in GROUND_FORMS_FLIP0:
            lines.append(GROUND_TMPL.format(surf=pat.format(s=stem),
                                            pol="긍정" if pol == 1 else "부정"))

    def carrier(stem, stem_pol):                      # a negation line's OUTPUT = flip(stem_pol)
        for pat in SEENSWAP_CARRIERS:
            lines.append(GROUND_TMPL.format(surf=pat.format(s=stem),
                                            pol="부정" if stem_pol == 1 else "긍정"))

    for _ in range(reps):
        for stem, pol in held:                        # held-out: unchanged (WRITE reproduction)
            arrow(stem, pol)
    for _ in range(replay):
        for stem, pol in arms["swap"]:                # THE MANIPULATION — inverted, in BOTH keys
            arrow(stem, 1 - pol)                       # declarative key (identical to C3)
            carrier(stem, 1 - pol)                     # operator's OWN key (new in C4)
        for stem, pol in arms["affirm"]:              # diagnostic: declarative at original polarity
            arrow(stem, pol)
        for stem, pol in arms["keep"]:                # holds the operator up on ORIGINAL polarity
            arrow(stem, pol)
            carrier(stem, pol)
        # arms["untouched"]: nothing — the forgetting gate needs a stratum the corpus never touches.

    rng.shuffle(lines)
    text = "".join(lines)

    # The audit the whole design rests on: a scored prompt must never appear in the corpus.
    leaks = []
    for pat in SEENSWAP_MEASURED:
        for stem, _ in seen + held:
            probe = GROUND_TMPL.format(surf=pat.format(s=stem), pol="긍정")[:-len("긍정.\n")]
            if probe in text:
                leaks.append(probe.strip())
    return text, {"held": len(held), "lines": len(lines), "bytes": len(text.encode()),
                  "arms": {k: [s for s, _ in v] for k, v in arms.items()},
                  "untouched_n": len(arms["untouched"]),
                  "measured_prompt_leaks": leaks}


def build_ground(fmt, atoms_path, reps, replay, seed, lang=DEFAULT_LANG):
    """Return (text, stats) for the ground / ground_shuffle arm.

    atoms_path = gt_atoms.json ({"atoms":[{stem, pol, split}]}). held-out atoms get the treatment;
    train ("seen") atoms are replayed unchanged in BOTH arms (they are not the manipulation).
    """
    # `ko` resolves to the pre-pack constants verbatim, so every frozen corpus stays byte-identical.
    L = lang_pack(lang)
    TMPL, F0, F1 = L["tmpl"], L["flip0"], L["flip1"]
    POS, NEG = L["pos"], L["neg"]
    rng = random.Random(seed)
    atoms = json.load(open(atoms_path))["atoms"]
    held = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "heldout"]
    seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]
    assert_atoms_match_lang([st for st, _ in held + seen], lang)
    if not held:
        raise ValueError(f"{atoms_path}: no held-out atoms")

    # Same stems, same lines, every polarity inverted. Nothing random about it — the sharpness is
    # the point (see the header): a partially-truthful control cannot produce a signed prediction.
    labels = [p for _, p in held]
    if fmt in ("ground_lie", "ground_keep_lie"):
        held = [(s, 1 - p) for s, p in held]

    lines = []
    for _ in range(reps):
        for stem, pol in held:
            for pat in F0:
                lines.append(TMPL.format(surf=pat.format(s=stem),
                                                pol=POS if pol == 1 else NEG))
    for _ in range(replay):
        for stem, pol in seen:
            for pat in F0:
                lines.append(TMPL.format(surf=pat.format(s=stem),
                                                pol=POS if pol == 1 else NEG))
            if fmt in ("ground_keep", "ground_keep_lie"):
                # Replay the negated lines too — on the SEEN stems ONLY. Without these, 6000 steps
                # of flip0-only training destroy the negation operator the eval is about to test
                # (measured: SEEN flip1 0.8833 -> 0.3333). The held-out stems keep zero negated
                # exposure, so the flip1 eval bytes are unchanged: this preserves, it does not leak.
                for pat in F1:
                    lines.append(TMPL.format(surf=pat.format(s=stem),
                                                    pol=NEG if pol == 1 else POS))
    rng.shuffle(lines)
    text = "".join(lines)
    flipped = sum(1 for k, (_, p) in enumerate(held) if p != labels[k])
    return text, {"held": len(held), "seen": len(seen), "lines": len(lines),
                  "labels_flipped": flipped, "bytes": len(text.encode())}


def _read_labelled(paths):
    """(text, label 0/1) rows from the lane's actual corpus files — reference-matched to the
    loaders that built them, not guessed:

      NSMC             id <TAB> text <TAB> label      3 cols, label in {0,1}, header line skipped
      naver_shopping   rating <TAB> text              rating 1-5: <=2 -> 0, >=4 -> 1, 3 DROPPED
      steam            label <TAB> text               2 cols, label in {0,1}

    The 3-star rows are dropped, not folded into either class — that is what the corpus builder
    does, and a probe fed a different label set than the model was trained on is not measuring the
    model."""
    rows = []
    for p in paths:
        with open(p, encoding="utf-8", errors="replace") as f:
            for ln in f:
                pp = ln.rstrip("\n").split("\t")
                if len(pp) == 3 and pp[2] in ("0", "1"):          # NSMC
                    rows.append((pp[1], int(pp[2])))
                elif len(pp) == 2 and pp[0].isdigit():            # label/rating first
                    v, txt = int(pp[0]), pp[1]
                    if v in (0, 1):                               # steam
                        rows.append((txt, v))
                    elif v <= 2:                                  # naver_shopping rating
                        rows.append((txt, 0))
                    elif v >= 4:
                        rows.append((txt, 1))
                    # rating 3 -> dropped, deliberately
    return rows


def mine_lexicon(corpus_paths, lang, top_n, min_occ):
    """Rank candidate stems by FREQUENCY in the real corpus — the designer does not get to pick.

    Every atom set this lane has used was hand-picked, and a hand-picked set is a place for a
    hypothesis to hide: nothing stops the designer from reaching for the adjectives that happen to
    suit the story. The defence is not willpower, it is procedure — mine the candidates from the
    corpus by frequency, take them IN RANK ORDER, and let the gates (G-DERIV / G-CARRIER / G-SUBSTR /
    G-OCCUR / G-BALANCE) throw out whatever they throw out. What survives is what the corpus offered,
    not what the experimenter wanted.

    The frame is the predicative slot the polarity task actually uses — `(is|are|was|were|really|
    very|so|quite|too) <word>` — so a mined candidate is a word the model has genuinely read in the
    position the carrier will put it in. The polarity LABEL is not mined (a corpus cannot tell you
    that `terrible` is negative); it stays a human 1-bit annotation, which is the same status the
    Korean `gt_atoms.json` `pol` field always had. p1-p8 forbids an LLM writing TRAINING BYTES; a
    lexicon writes none — the training bytes are the natural corpus plus the deterministic template.
    """
    if lang == "ko":
        raise SystemExit("anima corpus atoms --mine-lexicon: ko atoms are frozen (gt_atoms.json). "
                         "Mining is for a NEW language whose atom set does not exist yet.")
    # The frame must be a SYNTACTIC constraint, not a semantic preference — otherwise the designer is
    # back in the loop. `(is|was) X` is too loose: it happily returns `is the`, `is not`, `is that`
    # (measured: those were the top 3 of 14,069 candidates). After a DEGREE ADVERB, English admits
    # only an adjective or another adverb — so `very X` / `really X` selects the part of speech we
    # need without anyone choosing a word.
    FRAME = re.compile(
        r"\b(?:very|really|quite|so|extremely|incredibly|remarkably|fairly|rather|pretty|"
        r"utterly|totally|absolutely|surprisingly|genuinely)\s+([a-z]{3,12})\b", re.I)
    counts = collections.Counter()
    for cp in corpus_paths:
        with open(cp, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                for w in FRAME.findall(line):
                    counts[w.lower()] += 1
    # A candidate must ALSO clear the occurrence floor as a STANDALONE word, not just inside the
    # frame. Count every word ONCE, in a single tokenising pass: the obvious loop — re.findall over
    # the whole corpus per candidate — is O(corpus x candidates) and on 60MB x 600 candidates it
    # simply does not finish (measured: it hung). One pass, then a dict lookup (measured: 3.4s).
    word = collections.Counter()
    tok = re.compile(r"[a-z]+")
    for cp in corpus_paths:
        with open(cp, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                word.update(tok.findall(line.lower()))
    out = []
    for w, n in counts.most_common():
        if len(out) >= top_n:
            break
        if word[w] >= min_occ:
            out.append({"stem": w, "frame_hits": n, "occ": word[w], "pol": None})
    return out, {"frame_candidates": len(counts), "kept": len(out), "min_occ": min_occ}


def build_atoms(lexicon_path, corpus_paths, lang, n_seen, n_held, min_occ, seed):
    """Mine an atom set from a REAL corpus and refuse to emit one that cannot decide anything.

    An atom set is the load-bearing input of the whole recombination lane: the polarity we write, the
    stems we hold out, the split the verdict is computed over. Every way this lane has died so far
    traces back to a property of the atom set that nobody checked BEFORE spending GPU:

      H_9299/H_9300  a stem 3 bytes long, scored with a manifest-global --score-len, so the scorer
                     read past the atom into the carrier      -> byte-budget artifact, not a fact
      H_9303         one carrier for everything, so 'polarity bound to the stem' and 'polarity bound
                     to the carrier' were perfectly collinear -> undecidable, dead before firing
      H_9331/H_9332  the operator was only ever tested on the 20 stems it was TRAINED on
                     -> a generalisation claim measured at zero exposure on the wrong axis
      H_9296         held-out n=29 gives a chance sd of 0.093, so a frozen bar of 0.65 sits 1.62 sd
                     out -> 'we could not find it' was reported as 'it is not there'

    So the gates below are not hygiene. Each one is a verdict that already died.

      G-OCCUR     every stem occurs >= min_occ times in the natural text. A held-out stem the model
                  never read has no representation to bind a polarity TO, and its chance-level flip1
                  would mean nothing.
      G-SUBSTR    no stem is a substring of another. In Korean `참` sits inside dozens of words; a
                  substring hit makes the occurrence count, the leak check and the scorer all lie.
      G-BALANCE   both splits are polarity-balanced. An imbalanced split hands a collapsed model a
                  free score -- exactly the majority-label collapse that made a 0.575 headline look
                  like learning (H_9324).
      G-POWER     n_held is large enough that the effect we intend to claim is above the chance sd.
                  Reported, not silently assumed: sd = 0.5/sqrt(n), and the caller must state the
                  bar it will use against it.

    A set that fails any of these is not emitted. Failing here costs seconds; failing after the fire
    costs a campaign.
    """
    rng = random.Random(seed)
    L = lang_pack(lang)
    lex = json.load(open(lexicon_path, encoding="utf-8"))
    stems = [(e["stem"], int(e["pol"])) for e in lex["stems"]]
    assert_atoms_match_lang([st for st, _ in stems], lang)

    text = ""
    for cp in corpus_paths:
        with open(cp, encoding="utf-8", errors="replace") as fh:
            text += fh.read()
    if not text:
        raise SystemExit("anima corpus atoms: --corpus produced 0 bytes")

    # G-DERIV — a derivational negation of another stem must not be in the set.
    #
    # The Korean set shipped `편하`(comfortable) and `불편하`(uncomfortable) both as held-out atoms,
    # and `불-` IS a negation morpheme (H_9333). So the held-out set of a NEGATION experiment
    # contained the negation of one of its own members: the model could reach `불편하지 않다` by
    # double negation instead of by the lookup we were testing. English is far richer here
    # (un-, in-, im-, dis-, non-, -less), so the same defect is a first-class risk, not a curiosity.
    if lang != "ko":
        S = {st for st, _ in stems}
        deriv = []
        for st in sorted(S):
            for pre in ("un", "in", "im", "dis", "non", "ir", "il"):
                if st.startswith(pre) and st[len(pre):] in S:
                    deriv.append((st, st[len(pre):], pre + "-"))
            if st.endswith("less") and st[:-4] in S:
                deriv.append((st, st[:-4], "-less"))
        if deriv:
            raise SystemExit(
                "anima corpus atoms: G-DERIV FAIL — %d stem(s) are a DERIVATIONAL NEGATION of another "
                "stem in the same set: %s\n"
                "  A negation experiment whose atom set contains the negation of its own members lets "
                "the model\n  reach the answer by double negation instead of by the lookup under test "
                "(this is the KO\n  `편하` / `불편하` defect, H_9333). Drop one of each pair."
                % (len(deriv), ", ".join("%s = %s%s" % (a, c, b) for a, b, c in deriv[:6])))

    # G-CARRIER — no stem may nest in (or contain) a carrier or label token.
    #
    # The scorer reads a fixed byte span; if a stem shares bytes with the carrier or with the answer
    # word, the span it reads is not the span we think it is. Same failure family as G-SUBSTR, one
    # level up: there the collision was stem-vs-stem, here it is stem-vs-frame.
    frame = set()
    for tok in re.findall(r"[A-Za-z가-힣]+", L["tmpl"] + "".join(L["flip0"]) + "".join(L["flip1"])):
        if tok not in ("s", "surf", "pol"):
            frame.add(tok)
    frame |= {L["pos"], L["neg"]}
    fl = {f.lower() for f in frame}
    clash = [(st, st) for st, _ in stems if st.lower() in fl]
    if clash:
        raise SystemExit(
            "anima corpus atoms: G-CARRIER FAIL — %d stem(s) collide with a carrier/label token: %s\n"
            "  The scorer reads a fixed byte span; a stem that shares bytes with the frame or with the\n"
            "  answer word makes that span mean something other than what the manifest claims."
            % (len(clash), ", ".join(t[0] for t in clash[:6])))

    # G-SUBSTR
    bad = [(a, b) for a, _ in stems for b, _ in stems if a != b and a in b]
    if bad:
        raise SystemExit(
            "anima corpus atoms: G-SUBSTR FAIL — %d stem(s) sit INSIDE another stem: %s\n"
            "  Occurrence counts, the held-out leak check and the scorer all read the wrong span\n"
            "  when stems nest (this is how a 3-byte Korean stem corrupted H_9299/H_9300)."
            % (len(bad), ", ".join("%s<%s" % t for t in bad[:6])))

    # G-OCCUR — count on a WORD BOUNDARY where the language has one.
    #
    # `text.count(stem)` is the very defect this file's convergence record calls out (corpus-py-1
    # ⑩): a substring match counts every longer word that contains the stem. In English that is not
    # an edge case, it is the norm — "art" is inside "start", "warm" inside "warmth". An occurrence
    # floor computed that way passes stems the model has barely read, and the floor is the whole
    # point of the gate. Korean has no word boundary in the regex sense (and its stems are bound
    # forms that legitimately appear inside inflections), so it keeps the raw count.
    if lang == "ko":
        occ = {st: text.count(st) for st, _ in stems}
    else:
        occ = {st: len(re.findall(r"\b%s\b" % re.escape(st), text, re.I)) for st, _ in stems}
    thin = sorted([(st, occ[st]) for st, _ in stems if occ[st] < min_occ], key=lambda x: x[1])
    if thin:
        raise SystemExit(
            "anima corpus atoms: G-OCCUR FAIL — %d stem(s) below --min-occ %d in the natural text.\n"
            "  A stem the model never read has no representation to bind a polarity to, and its\n"
            "  chance-level score would mean nothing. thinnest: %s"
            % (len(thin), min_occ, ", ".join("%s=%d" % t for t in thin[:8])))

    need = n_seen + n_held
    if len(stems) < need:
        raise SystemExit("anima corpus atoms: lexicon has %d stems, need %d (seen %d + held %d)"
                         % (len(stems), need, n_seen, n_held))

    # G-BALANCE — draw each split polarity-balanced rather than hoping a shuffle lands balanced
    pos = [st for st, p in stems if p == 1]
    neg = [st for st, p in stems if p == 0]
    rng.shuffle(pos); rng.shuffle(neg)
    out, pi, ni = [], 0, 0
    for split, n in (("train", n_seen), ("heldout", n_held)):
        for k in range(n):
            take_pos = (k % 2 == 0 and pi < len(pos)) or ni >= len(neg)
            if take_pos and pi < len(pos):
                out.append({"stem": pos[pi], "pol": 1, "split": split}); pi += 1
            elif ni < len(neg):
                out.append({"stem": neg[ni], "pol": 0, "split": split}); ni += 1
            else:
                raise SystemExit("anima corpus atoms: G-BALANCE FAIL — lexicon ran out of one polarity "
                                 "(pos %d / neg %d available, need %d balanced)" % (len(pos), len(neg), need))

    held = [a for a in out if a["split"] == "heldout"]
    hp = sum(a["pol"] for a in held)
    sd = 0.5 / (len(held) ** 0.5)
    stats = {"lang": lang, "n_train": n_seen, "n_heldout": n_held,
             "heldout_pos": hp, "heldout_neg": len(held) - hp,
             "min_occ": min_occ, "occ_min": min(occ.values()), "occ_median": sorted(occ.values())[len(occ) // 2],
             "chance_sd": round(sd, 4)}
    return {"atoms": out, "n_train": n_seen, "n_heldout": n_held, "gates": stats}, stats


def build_valence(atoms_path, corpus_paths, k_ctx, ctx_bytes, min_occ, neutral_tol, seed,
                  tail=""):
    """Return (manifest, stats) for the AUDIT-A valence manifest (`anima-py evaluate --valence-audit`).

    The question: is a held-out atom's polarity in the WEIGHTS at all, read at the atom's own
    position inside its REAL corpus sentences? The trap: a sentiment review is full of sentiment
    words, so a probe that reads the NEIGHBOURHOOD rather than the atom scores just as well and we
    would fire GPU rent on an illusion. So the control IS the measurement — every context appears
    twice:

        arm "atom"  ...배송도 빠르고 가성비는 <ATOM>       the real atom
        arm "swap"  ...배송도 빠르고 가성비는 <NEUTRAL>    a length-matched neutral, SAME context

    and the verdict is Delta = probe(atom) - probe(swap) against a permutation null, never a raw
    value (FORM tunable, BIND earned). Measured: on the base_only ckpt the SWAP arm out-reads the
    atom arm (0.692 vs 0.615) — the probe was reading the neighbourhood, exactly as feared.

    k_ctx is the power knob and it is not free: the probe pools an atom's contexts, so per-atom
    noise falls as 1/sqrt(k_ctx). The corpus holds a median of 717 usable contexts per atom (min
    182), so the historical k_ctx=24 threw away ~197k of them and left the estimator too noisy to
    separate a real Delta (+0.11/+0.13, both seeds) from its own permutation null (p95 +0.15).
    Raising k_ctx sharpens the lens; it does NOT move any bar.

    NEUTRAL atoms are mined from the corpus itself — frequent stems whose occurrences are
    polarity-balanced (|p(pos) - 0.5| < neutral_tol), so they carry exposure but no valence — and
    only from non-held-out stems, so nothing about the held-out split leaks.

    `tail` moves the READ POINT past the atom, and it is the follow-up the k_ctx=182 result demands.
    Measured there: the swap arm out-reads the atom arm on all four ckpts (0.73-0.82 vs 0.58-0.64) —
    the atom's own position carries LESS polarity than a neutral filler in the same context. Two
    very different worlds explain that:

      (a) the atom injects no valence into the stream at all — natural exposure wrote nothing, and
          the grounding route is closed;
      (b) the atom DOES inject it, but the hidden AT the atom's own last byte is dominated by that
          byte's own identity (form, not bind), so the valence is only visible one step downstream.

    Appending an identical tail to BOTH arms shifts the read point past the atom while changing
    nothing else. If the atom arm overtakes the swap arm there, world (b) holds and the natural
    route reopens. A single space is the safest tail: it is grammatical after any stem, it is one
    byte, and it is byte-identical across arms — so the ONLY thing that moved is where we read.
    """
    import collections
    rng = random.Random(seed)
    atoms = [a for a in json.load(open(atoms_path))["atoms"] if a["split"] == "heldout"]
    if not atoms:
        raise ValueError(f"{atoms_path}: no held-out atoms")
    held = {a["stem"] for a in atoms}

    rows = _read_labelled(corpus_paths)
    if not rows:
        raise ValueError("no labelled rows read from --corpus")

    tot, pos = collections.Counter(), collections.Counter()
    for t, lab in rows:
        for w in set(t.split()):
            if 2 <= len(w) <= 6:
                tot[w] += 1
                pos[w] += int(lab == 1)
    neutral = [w for w, n in tot.items()
               if n >= min_occ and w not in held and not any(h in w for h in held)
               and abs(pos[w] / n - 0.5) < neutral_tol]
    if not neutral:
        raise ValueError("no neutral inventory — loosen --neutral-tol or --min-occ")
    by_len = collections.defaultdict(list)
    for w in neutral:
        by_len[len(w)].append(w)

    items, thin = [], []
    for a in atoms:
        stem = a["stem"]
        hits = [t for (t, _l) in rows if stem in t]
        rng.shuffle(hits)
        used = 0
        for t in hits:
            i = t.find(stem)
            frag = t[:i][-ctx_bytes:]                       # the left context, atom excluded
            if not frag.strip():
                continue
            cands = by_len.get(len(stem)) or by_len[min(by_len, key=lambda L: abs(L - len(stem)))]
            swap = rng.choice(cands)
            items.append({"id": f"A_{stem}_{used}", "prompt": frag + stem + tail,
                          "stem": stem, "pol": int(a["pol"]), "arm": "atom"})
            items.append({"id": f"S_{stem}_{used}", "prompt": frag + swap + tail,
                          "stem": stem, "pol": int(a["pol"]), "arm": "swap"})
            used += 1
            if used >= k_ctx:
                break
        if used < k_ctx:
            thin.append((stem, used))

    stats = {"atoms": len(atoms), "k_ctx": k_ctx, "prompts": len(items),
             "neutral_inventory": len(neutral), "thin_atoms": thin, "tail": tail}
    return {"win": 64, "items": items}, stats


def _load_concepts(path):
    if not path:
        return DEFAULT_SEEDS, DEFAULT_KW
    rows = json.load(open(path))
    return [r["seed"] for r in rows], [r["kw"] for r in rows]


def _two(kw_fam, rng):
    ks = kw_fam[:]
    rng.shuffle(ks)
    return ks[0], ks[1 % len(ks)]


def build(fmt, S, KW, held_out, comp_per_pair, single_per_concept, seed):
    """Return the corpus text for one format arm (deriv or flat)."""
    rng = random.Random(seed)
    n = len(S)
    held = frozenset(held_out)
    train_pairs = [(i, j) for i in range(n) for j in range(n)
                   if i != j and frozenset((i, j)) != held]

    def instance(i, j):
        a1, a2 = _two(KW[i], rng)
        b1, b2 = _two(KW[j], rng)
        prompt = f"{S[i]}. {S[j]}. "
        out = f"out: {a1} {a2} meet {b1} {b2}, {rng.choice(CLOSE)}.\n"
        deriv_mid = (f"{rng.choice(DERIVE_LEAD)}: take {a1} and {a2}; "
                     f"take {b1} and {b2}; {rng.choice(BIND)} {a1} with {b1}. ")
        return prompt + deriv_mid + out, prompt + out

    def single(i):
        a1, a2 = _two(KW[i], rng)
        return f"{S[i]}. here {a1} and {a2} stand alone; {a1} holds {a2}.\n"

    stream = []
    for _ in range(comp_per_pair):
        stream += [("comp", i, j) for (i, j) in train_pairs]
    for _ in range(single_per_concept):
        stream += [("sing", i, None) for i in range(n)]
    rng.shuffle(stream)

    docs = []
    for kind, i, j in stream:
        if kind == "comp":
            d, f = instance(i, j)
            docs.append(d if fmt == "derivtrace" else f)
        else:
            docs.append(single(i))  # single-concept doc is format-invariant
    return "".join(docs), train_pairs


# The corpus carries its own earned training budget, and the strata a FORGET gate must cover.
#
# H_9322 died because a 600-step CPT never landed the fact, and the negative read as "the substrate
# cannot compose" instead of "the fine-tune was too small". H_9324 then measured the floor: on this
# corpus WRITE climbs 0.4483 (600@5e-5, chance) -> 0.9540 (6000@2e-4) -> 1.0000 (6000@5e-4), so a
# sub-floor run is not a measurement at all. Nothing in the engine knew that, which means the next
# run could repeat it — so the corpus now ships the number next to itself (`<out>.meta.json`) and
# `anima-py train` refuses to start below it.
#
# The floor is NOT unconditional (convergence corpus-py-1 (D)): on `ground`/`ground_lie` a BIGGER
# budget destroys MORE of the operator (SEEN flip1 0.8833 base -> 0.4333 @2e-4 -> 0.3333 @5e-4),
# because those formats contain zero negated lines. Handing them a 6000-step floor would be telling
# the trainer to break the model harder. So they carry no floor — they carry the destruction warning
# and a pointer to `ground_keep`, which replays the SEEN stems' negated lines and is the only ground
# format where the budget conclusion holds.
BUDGET_FLOORS = {
    # fmt: (min_steps, min_lr, note)
    "ground_keep": (6000, 2e-4,
                    "H_9324: WRITE 0.4483 (600@5e-5 = chance) -> 0.9540 (6000@2e-4) -> 1.0000 "
                    "(6000@5e-4), reproduced on 2 seeds. Below this floor a negative result is a "
                    "BUDGET negative, not a substrate negative — that is how H_9322 died."),
    "ground_keep_lie": (6000, 2e-4, "same floor as ground_keep — it is the matched control arm."),
}

# Strata a FORGET gate MUST read for this corpus — specifically the ones the corpus contains ZERO
# of, because those are exactly what dies (convergence corpus-py-1 (A)/(7)). A FORGET gate that
# only reads the stratum the corpus reinforces is structurally always-pass = a forged gate.
FORGET_STRATA = {
    "ground":          ["SEEN flip0", "SEEN flip1 (ZERO in this corpus — this is what dies)"],
    "ground_lie":      ["SEEN flip0", "SEEN flip1 (ZERO in this corpus — this is what dies)"],
    "ground_keep":     ["SEEN flip0", "SEEN flip1 (replayed — verify it SURVIVES, bar 0.75)"],
    "ground_keep_lie": ["SEEN flip0", "SEEN flip1 (replayed — verify it SURVIVES, bar 0.75)"],
}


def _write_budget_floor(out_path, fmt):
    """Emit `<out>.meta.json` beside the corpus. NOT inside it — this is a byte-LM, so a header
    comment in the corpus file would be TRAINED ON."""
    floor = BUDGET_FLOORS.get(fmt)
    meta = {
        "format": fmt,
        "min_steps": floor[0] if floor else None,
        "min_lr": floor[1] if floor else None,
        "note": floor[2] if floor else None,
        "forget_strata": FORGET_STRATA.get(fmt, []),
    }
    if fmt in ("ground", "ground_lie"):
        meta["destroys"] = (
            "This format contains ZERO negated (flip1) lines, so CPT on it DESTROYS the model's "
            "negation operator: SEEN flip1 0.8833 (pretrained base) -> 0.4333 (6000@2e-4) -> "
            "0.3333 (6000@5e-4) — monotonically worse with budget. Any flip1 number measured on a "
            "model tuned with this corpus is INVALID (H_9327): you broke the operator, then asked "
            "it to compose. Use `ground_keep` unless you specifically want the broken-operator arm."
        )
    with open(out_path + ".meta.json", "w") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    if meta.get("destroys"):
        print("  [budget-meta] %s.meta.json — ⚠️ NO floor: this format DESTROYS the negation "
              "operator (see .meta.json 'destroys'); ground_keep is the safe one." % out_path)
    elif floor:
        print("  [budget-meta] %s.meta.json — earned floor: steps>=%d lr>=%g (H_9324)"
              % (out_path, floor[0], floor[1]))


def build_bindlocus(n2_eval, n2_seen, corpus_paths, novel_pool, seed):
    """H_9331 BIND-LOCUS manifest — inherits H_9327's carriers VERBATIM and earns its `novel` split
    by MEASUREMENT, not by assertion.

    Three splits, and the whole design turns on the third:
      seen     stems the pretrained operator demonstrably runs on (SEEN flip1 0.98-1.00) — Stage A's
               spike-in donors, where the truth is one we planted ourselves
      heldout  stems whose polarity CPT WROTE (WRITE 0.98) but which the operator ignores — the arm
               that asks whether the wall is repairable in place
      novel    stems the model has NEVER met: 0 occurrences in the pretrain corpus AND 0 in the CPT
               corpus. This is the core arm — it asks whether the operator binds to content it did
               not co-form with, i.e. whether binding is lookup (P) or pretraining-forged (S)

    "novel" is checked by BYTE COUNT over every corpus handed in (`--corpus`, repeatable), not by
    the author's belief that a word is rare (a_korean_byte_budget: this is a byte-LM; a stem that
    "looks new" can still be 900 occurrences of a substring). A stem with even ONE occurrence is
    REJECTED and reported — an unearned novel split would silently turn an S verdict into a
    pretraining-exposure artifact, which is the exact confound the arm exists to exclude.
    """
    import random as _r
    import os as _os
    rng = _r.Random(seed)
    CHUNK = 64 << 20                       # 64 MB
    sizes = [(p, _os.path.getsize(p)) for p in corpus_paths]
    print("  novelty corpora: %d file(s) · %.2f GB total (STREAMED, byte-counted — the pretrain "
          "corpus is ~10 GB, so reading it whole would OOM the host)"
          % (len(sizes), sum(n for _, n in sizes) / 1e9))

    def occ(stems):
        """Byte-count every candidate stem over every corpus in ONE streaming pass per file.

        Chunked with an overlap of (max stem length - 1) bytes, so a stem straddling a chunk
        boundary is still counted — without the overlap a stem could read as 0 occurrences purely
        because it happened to land on a 64 MB seam, and an unearned `novel` label is precisely the
        confound that would turn an S verdict into a pretraining-exposure artifact."""
        sbs = [(st, st.encode("utf-8", "surrogateescape")) for st in stems]
        ov = max(len(b) for _, b in sbs) - 1
        counts = {st: 0 for st in stems}
        for p, _n in sizes:
            with open(p, "rb") as fh:
                tail = b""
                while True:
                    buf = fh.read(CHUNK)
                    if not buf:
                        break
                    blob = tail + buf
                    for st, sb in sbs:
                        counts[st] += blob.count(sb)
                    tail = blob[-ov:] if ov > 0 else b""
                    # the overlap region is re-scanned next round; subtract its own hits once
                    if ov > 0:
                        for st, sb in sbs:
                            counts[st] -= tail.count(sb)
        return counts

    def carriers(stem, pol, split):
        """H_9327's own surfaces, verbatim: flip0 = bare, flip1 = negL ('...지 않다') and negS
        ('안 ...고'). negS PREFIXES the negator, so a template rebuild would have produced a string
        the model never saw — the seeds are copied, never re-derived (reference-match)."""
        out = [("이 영화 %s고 => " % stem, 0, "bare"),
               ("이 영화 %s지 않다 => " % stem, 1, "negL"),
               ("이 영화 안 %s고 => " % stem, 1, "negS")]
        return [{"id": "%s_%s_%s" % (split[0].upper(), stem, form), "stem": stem, "pol": int(pol),
                 "flip": f, "split": split, "form": form, "seed": s} for s, f, form in out]

    items = []
    for st, pol in n2_seen:
        items += carriers(st, pol, "seen")
    for st, pol in n2_eval:
        items += carriers(st, pol, "heldout")

    counts = occ([st for st, _ in novel_pool])
    kept, rejected = [], []
    for st, pol in novel_pool:
        if counts[st] == 0:
            kept.append((st, pol))
        else:
            rejected.append((st, counts[st]))
    for st, pol in kept:
        items += carriers(st, pol, "novel")

    print("  novel candidates %d -> EARNED %d (0 bytes in every corpus) · REJECTED %d"
          % (len(novel_pool), len(kept), len(rejected)))
    if rejected:
        top = sorted(rejected, key=lambda x: -x[1])[:8]
        print("    rejected (occurrences): " + " · ".join("%s=%d" % (s, n) for s, n in top))
    return {"win": 64, "carrier": "이 영화 {stem}고 => ", "items": items,
            "novel_earned": [s for s, _ in kept],
            "novel_rejected": dict(rejected)}, kept, rejected


def main():
    argv = sys.argv[1:]
    fmt, opts = _parse_args(argv)
    if fmt == "valence":
        if not opts["atoms"] or not opts["corpus"]:
            print("usage: anima-py corpus valence --atoms gt_atoms.json --corpus FILE [--corpus F2] "
                  "--out manifest.json [--k-ctx 24] [--ctx-bytes 64] [--min-occ 200] "
                  "[--neutral-tol 0.05] [--seed 7]")
            sys.exit(2)
        man, st = build_valence(opts["atoms"], opts["corpus"], opts["k_ctx"], opts["ctx_bytes"],
                                opts["min_occ"], opts["neutral_tol"], opts["seed"], opts["tail"])
        out = opts["out"] or "valence_manifest.json"
        json.dump(man, open(out, "w"), ensure_ascii=False)
        print("wrote %s — %d prompts (%d held-out atoms x %d contexts x 2 arms)%s"
              % (out, st["prompts"], st["atoms"], st["k_ctx"],
                 (" · read point shifted past the atom by tail %r" % st["tail"]) if st["tail"] else ""))
        print("  neutral inventory: %d stems (occ>=%d, |p(pos)-0.5|<%.2f, non-held-out)"
              % (st["neutral_inventory"], opts["min_occ"], opts["neutral_tol"]))
        if st["thin_atoms"]:
            print("  ⚠ %d atom(s) could not supply %d contexts (fewest: %s) — the pooled estimate "
                  "is noisier for those" % (len(st["thin_atoms"]), st["k_ctx"],
                                            min(st["thin_atoms"], key=lambda x: x[1])))
        sys.exit(0)
    if fmt == "bindlocus":
        if not (opts["n2_eval"] and opts["n2_seen"] and opts["corpus"] and opts["novel"]):
            print("usage: anima-py corpus bindlocus --n2-eval n2_eval_manifest.json "
                  "--n2-seen n2_seen_manifest.json --novel novel_stems.json "
                  "--corpus PRETRAIN.txt [--corpus CPT.txt ...] --out bl_manifest.json [--seed 7]")
            print("      H_9331 — builds the BIND-LOCUS manifest. Inherits H_9327's carriers VERBATIM")
            print("      (negL '...지 않다' AND negS '안 ...고' — negS PREFIXES the negator, so a template")
            print("      rebuild would feed the model a string it never saw). The `novel` split is EARNED:")
            print("      every candidate stem is BYTE-counted against every --corpus and rejected on a")
            print("      single occurrence (an unearned novel split turns an S verdict into a")
            print("      pretraining-exposure artifact — the exact confound the arm exists to exclude).")
            sys.exit(2)

        def _stems(path):
            d = json.load(open(path))
            seen_p, out = set(), []
            for x in d.get("heldout", []) + d.get("seen", []):
                if x["p"] not in seen_p:
                    seen_p.add(x["p"]); out.append((x["p"], int(x["pol"])))
            return out
        ev, sn = _stems(opts["n2_eval"]), _stems(opts["n2_seen"])
        nv = json.load(open(opts["novel"]))
        nv = [(x["stem"], int(x["pol"])) for x in nv] if isinstance(nv[0], dict) else [(a, b) for a, b in nv]
        print("=== anima-py corpus bindlocus — H_9331 manifest (novel split EARNED by byte count) ===")
        print("  seen stems %d · heldout stems %d · novel candidates %d" % (len(sn), len(ev), len(nv)))
        man, kept, rej = build_bindlocus(ev, sn, opts["corpus"], nv, opts["seed"])
        out = opts["out"] or "bl_manifest.json"
        json.dump(man, open(out, "w"), ensure_ascii=False)
        n_by = {}
        for it in man["items"]:
            n_by[it["split"]] = n_by.get(it["split"], 0) + 1
        print("wrote %s — %d items (%s)" % (out, len(man["items"]),
              " · ".join("%s %d" % (k, v) for k, v in sorted(n_by.items()))))
        if len(kept) < 30:
            print("  ⚠️ novel n=%d — the pre-registered power calc needs 60 stems (se~0.064, "
                  "MDE(80%%)~0.18 < TOST margin 0.20). Below that a null is 'we cannot find it', "
                  "NOT 'it is not there' (power-before-negative-verdict)." % len(kept))
        sys.exit(0)
    if fmt == "atoms":
        if opts["mine"]:
            if not opts["corpus"]:
                print("anima corpus atoms --mine-lexicon N --corpus C.txt --lang en "
                      "--min-occ 200 --out lexicon_en.json")
                sys.exit(2)
            cand, st = mine_lexicon(opts["corpus"], opts["lang"], opts["mine"], opts["min_occ"])
            if opts["out"]:
                json.dump({"lang": opts["lang"], "mined": st, "stems": cand},
                          open(opts["out"], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            print("anima corpus atoms --mine-lexicon [%s]: %d frame candidates -> %d kept "
                  "(>= %d standalone occurrences) -> %s"
                  % (opts["lang"], st["frame_candidates"], st["kept"], st["min_occ"],
                     opts["out"] or "(stdout)"))
            print("  ranked by FREQUENCY — the designer does not pick. Take them IN ORDER, let the")
            print("  gates discard what they discard, then annotate `pol` (the only human step: 1 bit")
            print("  per stem, the same status the KO gt_atoms.json `pol` field always had).")
            for c in cand[:12]:
                print("    %-12s frame_hits=%d" % (c["stem"], c["frame_hits"]))
            return
        if not (opts["lexicon"] and opts["corpus"]):
            print("anima corpus atoms --lexicon L.json --corpus C.txt [--corpus C2.txt] "
                  "--lang en --n-seen 20 --n-held 29 --min-occ 200 --out gt_atoms_en.json")
            sys.exit(2)
        obj, st = build_atoms(opts["lexicon"], opts["corpus"], opts["lang"],
                              opts["n_seen"], opts["n_held"], opts["min_occ"], opts["seed"])
        if opts["out"]:
            json.dump(obj, open(opts["out"], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("anima corpus atoms [%s]: train=%d heldout=%d (pos %d : neg %d) occ_min=%d "
              "occ_median=%d min_occ=%d chance_sd=%.4f -> %s"
              % (st["lang"], st["n_train"], st["n_heldout"], st["heldout_pos"], st["heldout_neg"],
                 st["occ_min"], st["occ_median"], st["min_occ"], st["chance_sd"],
                 opts["out"] or "(stdout)"))
        print("  G-OCCUR ✅ every stem >= %d occurrences · G-SUBSTR ✅ no stem nests in another · "
              "G-BALANCE ✅ both splits polarity-balanced" % st["min_occ"])
        print("  G-POWER  chance sd = 0.5/sqrt(%d) = %.4f — DERIVE the bar against this, never "
              "transplant it (H_9296: a 0.65 bar at n=29 sits 1.62 sd out)."
              % (st["n_heldout"], st["chance_sd"]))
        return

    if fmt not in ("derivtrace", "flat", "ground", "ground_lie", "ground_keep", "ground_keep_lie",
                   "ground_seenswap", "ground_carrierswap", "atoms"):
        print("usage: anima corpus <derivtrace|flat|ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap|ground_carrierswap|valence|bindlocus|atoms> --out PATH")
        print("      atoms  --lexicon L.json --corpus C.txt --lang en --n-seen 20 --n-held 29")
        print("             --min-occ 200 --out gt_atoms_en.json   mine an atom set from a REAL")
        print("             corpus behind 4 gates, each of which is a verdict that already died:")
        print("             G-SUBSTR (no stem nests in another — a 3-byte Korean stem corrupted")
        print("             H_9299/H_9300) · G-OCCUR (every stem read >= min-occ times, else it")
        print("             has no representation to bind a polarity to) · G-BALANCE (both splits")
        print("             · G-DERIV (en: no stem is a derivational negation of another — un-/in-/")
        print("             im-/dis-/non-/-less. The KO set shipped 편하 + 불편하, so a NEGATION")
        print("             experiment held the negation of its own member: H_9333) · G-CARRIER (no")
        print("             stem IS a carrier/label word) · G-OCCUR counts on a WORD BOUNDARY for")
        print("             alphabetic langs — text.count would pass `art` on 10k hits of `start`.")
        print("             polarity-balanced — imbalance hands a collapsed model a free score,")
        print("             H_9324) · G-POWER (reports chance sd = 0.5/sqrt(n); DERIVE the bar")
        print("             against it, never transplant one — H_9296).")
        print("      [--lang ko|en]  ground-family only. ko = DEFAULT and byte-identical to every")
        print("      frozen corpus (8/8 sha match) — do NOT change it or the frozen verdicts move.")
        print("      en = the discriminator, not coverage: `not` is a FREE PRE-posed word, the slot")
        print("      kind C1b measured as generalising, while the Korean ending is a BOUND suffix")
        print("      that attaches to the stem — the suspected mechanism of the BINDING wall.")
        print("      A lang/atom mismatch fails LOUD (--lang en over Korean atoms is refused).")
        print("  bindlocus              --n2-eval M.json --n2-seen M.json --novel N.json --corpus C.txt [--corpus C2.txt] [--seed S]")
        print("      H_9331 BIND-LOCUS manifest — H_9327 carriers verbatim; the `novel` split is EARNED")
        print("      by BYTE count over every --corpus (one occurrence = rejected).")
        print("      the ground* formats also emit <out>.meta.json — the training budget the corpus")
        print("      EARNED (H_9324: steps>=6000 lr>=2e-4 on ground_keep) + the strata a FORGET gate must")
        print("      cover. `anima-py train` reads it and REFUSES to start below the floor; ground/ground_lie")
        print("      carry no floor but a destruction warning (they delete the negation operator).")
        print("  derivtrace|flat        [--held-out I,J] [--comp-per-pair N] "
              "[--single-per-concept N] [--seed S] [--concepts FILE.json]")
        print("  ground|ground_lie|ground_keep|ground_keep_lie   --atoms gt_atoms.json [--reps N] [--replay N] [--seed S]")
        print("  ground_seenswap        --atoms gt_atoms.json [--reps N] [--replay N] [--seed S] [--split-seed S]")
        print("      C3 (H_9328) — REWRITES 12 SEEN stems' polarity (inverted) and asks whether the")
        print("      `지 않다` rule reads the new value or the pretrained one. Replay carriers are")
        print("      DISJOINT from the scored surfaces (else the flip1 answer is taught, not composed);")
        print("      both sets are surfaces the C1b census measured the operator running on.")
        print("  ground_carrierswap     --atoms gt_atoms.json [--reps N] [--replay N] [--seed S] [--split-seed S]")
        print("      C4 (H_9334) — C3 found the operator reads the OLD polarity after a DECLARATIVE")
        print("      (stem⊕고) rewrite; it cannot tell whether the new fact is in an unreachable store")
        print("      (H-δ) or merely written in the wrong key (H-ε). C4 writes the SAME inverted")
        print("      polarity ALSO through the operator's own `지 않다` carrier, then scores DISJOINT")
        print("      `지 않다` surfaces (taught 전혀/그다지/결코, scored bare·별로). Reads NEW -> H-ε")
        print("      (interface addressable); reads OLD -> H-δ (store unreachable / STEM-BOUND joint).")
        print("      GATE FIX ① untouched = len(seen)-17 (derived, not fixed 3): a 46-SEEN atoms file")
        print("      gives n=29, 0 flips -> 95%% UCB on forgetting 3/29=10.3%% (C3's 3/3=100%% = no power).")
        print("      GATE FIX ② liveness lives on the DV (swap-arm consistency p<=.02), not an n=6 side arm.")
        print("      Declarative write held IDENTICAL to C3, so the operator carrier is the ONE variable.")
        print("      H_9313 DECON-W grounding corpus — writes each held-out atom's polarity into")
        print("      the WEIGHTS via the un-negated (flip0) template lines ONLY. The negated")
        print("      (flip1) forms NEVER appear, so a later flip1 test measures COMPOSITION, not")
        print("      memorisation. `ground_lie` is the same stream with EVERY held-out polarity")
        print("      INVERTED — the control that earns the verdict (weight-side twin of the")
        print("      SEEN-LIE arm that decided H_9312). Prediction is signed: a model that")
        print("      consumes AND composes the written polarity must score FAR BELOW chance on")
        print("      flip1 under ground_lie; one that ignores it sits at chance in both arms.")
        print("      Same --seed => content-matched line for line.")
        print("  valence                --atoms gt_atoms.json --corpus FILE [--corpus F2 ...] "
              "[--k-ctx 24] [--min-occ 200] [--neutral-tol 0.05] [--seed S]")
        print("      AUDIT-A manifest for `anima-py evaluate --valence-audit`: is a held-out atom's")
        print("      polarity in the WEIGHTS at all, read at the atom's own position in its REAL")
        print("      corpus contexts? A sentiment review is full of sentiment words, so every")
        print("      context is emitted TWICE — once with the real atom, once with a length-matched")
        print("      NEUTRAL atom spliced into the same context — and the verdict is the DIFFERENCE.")
        print("      --k-ctx is the power knob: the probe pools an atom's contexts, so per-atom")
        print("      noise falls as 1/sqrt(k-ctx). The corpus holds ~717 contexts per atom (min 182).")
        print("      --tail STR appends STR to BOTH arms, moving the READ POINT past the atom. At the")
        print("      atom's own position the neutral SWAP arm out-reads it (0.73-0.82 vs 0.58-0.64):")
        print("      either the atom injects no valence at all, or the hidden there is dominated by")
        print("      the atom's own form. A one-space tail tells the two apart at zero extra cost.")
        sys.exit(2)

    if fmt == "ground_seenswap":
        if not opts["atoms"]:
            print("anima corpus ground_seenswap: --atoms gt_atoms.json is required")
            sys.exit(2)
        text, st = build_seenswap(opts["atoms"], opts["reps"], opts["replay"],
                                  opts["seed"], opts["split_seed"])
        if st["measured_prompt_leaks"]:
            # The design rests on this: a scored prompt must never be in the corpus, or the flip1
            # answer is taught rather than composed. Refuse to write a corpus that would void the run.
            print("anima corpus ground_seenswap: LEAK — %d scored prompt(s) appear in the corpus"
                  % len(st["measured_prompt_leaks"]), file=sys.stderr)
            for x in st["measured_prompt_leaks"][:5]:
                print("    %s" % x, file=sys.stderr)
            sys.exit(2)
        open(opts["out"], "w", encoding="utf-8").write(text)
        print("anima corpus ground_seenswap: lines=%d bytes=%d leaks=0 -> %s"
              % (st["lines"], st["bytes"], opts["out"]))
        for k in ("swap", "affirm", "keep", "untouched"):
            print("  %-10s n=%2d  %s" % (k, len(st["arms"][k]), " ".join(st["arms"][k])))
        json.dump(st, open(opts["out"] + ".arms.json", "w"), ensure_ascii=False, indent=1)
        return 0

    if fmt == "ground_carrierswap":
        if not opts["atoms"]:
            print("anima corpus ground_carrierswap: --atoms gt_atoms.json is required")
            sys.exit(2)
        text, st = build_carrierswap(opts["atoms"], opts["reps"], opts["replay"],
                                     opts["seed"], opts["split_seed"])
        if st["measured_prompt_leaks"]:
            # The design rests on this: a scored prompt must never be in the corpus, or a NEW read is
            # taught rather than composed. Refuse to write a corpus that would void the run.
            print("anima corpus ground_carrierswap: LEAK — %d scored prompt(s) appear in the corpus"
                  % len(st["measured_prompt_leaks"]), file=sys.stderr)
            for x in st["measured_prompt_leaks"][:5]:
                print("    %s" % x, file=sys.stderr)
            sys.exit(2)
        open(opts["out"], "w", encoding="utf-8").write(text)
        print("anima corpus ground_carrierswap: lines=%d bytes=%d leaks=0 untouched_n=%d -> %s"
              % (st["lines"], st["bytes"], st["untouched_n"], opts["out"]))
        print("  forget-gate power: 0 flips -> 95%% UCB on SEEN forgetting = 3/%d = %.1f%% (rule of three)"
              % (st["untouched_n"], 300.0 / st["untouched_n"]))
        for k in ("swap", "affirm", "keep", "untouched"):
            print("  %-10s n=%2d  %s" % (k, len(st["arms"][k]), " ".join(st["arms"][k])))
        json.dump(st, open(opts["out"] + ".arms.json", "w"), ensure_ascii=False, indent=1)
        return 0

    if fmt == "atoms":
        if not (opts["lexicon"] and opts["corpus"]):
            print("anima corpus atoms: --lexicon L.json --corpus C.txt [--corpus C2.txt] "
                  "--lang en --n-seen 20 --n-held 29 --min-occ 200 --out gt_atoms_en.json")
            sys.exit(2)
        obj, st = build_atoms(opts["lexicon"], opts["corpus"], opts["lang"],
                              opts["n_seen"], opts["n_held"], opts["min_occ"], opts["seed"])
        if opts["out"]:
            json.dump(obj, open(opts["out"], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("anima corpus atoms [%s]: train=%d heldout=%d (pos %d : neg %d) "
              "occ_min=%d occ_median=%d min_occ=%d chance_sd=%.4f -> %s"
              % (st["lang"], st["n_train"], st["n_heldout"], st["heldout_pos"], st["heldout_neg"],
                 st["occ_min"], st["occ_median"], st["min_occ"], st["chance_sd"],
                 opts["out"] or "(stdout)"))
        print("  G-OCCUR ✅ every stem >= %d occurrences  ·  G-SUBSTR ✅ no stem nests in another  ·  "
              "G-BALANCE ✅ both splits polarity-balanced" % st["min_occ"])
        print("  G-POWER  chance sd = 0.5/sqrt(%d) = %.4f — a bar must be DERIVED against this, "
              "never transplanted (H_9296: a 0.65 bar at n=29 sits 1.62 sd out)."
              % (st["n_heldout"], st["chance_sd"]))
        return

    if fmt in ("ground", "ground_lie", "ground_keep", "ground_keep_lie"):
        if not opts["atoms"]:
            print("anima corpus %s: --atoms gt_atoms.json is required" % fmt)
            sys.exit(2)
        text, st = build_ground(fmt, opts["atoms"], opts["reps"], opts["replay"], opts["seed"],
                                opts["lang"])
        if opts["out"]:
            with open(opts["out"], "w") as fh:
                fh.write(text)
            _write_budget_floor(opts["out"], fmt)
        print(f"anima corpus {fmt}: held={st['held']} seen={st['seen']} lines={st['lines']} "
              f"labels_flipped={st['labels_flipped']}/{st['held']} bytes={st['bytes']} "
              f"reps={opts['reps']} replay={opts['replay']} seed={opts['seed']} "
              f"-> {opts['out'] or '(stdout head)'}")
        if not opts["out"]:
            print(text[:400])
        return
    S, KW = _load_concepts(opts["concepts"])
    text, train_pairs = build(fmt, S, KW, opts["held_out"],
                              opts["comp_per_pair"], opts["single_per_concept"], opts["seed"])
    if opts["out"]:
        with open(opts["out"], "w") as fh:
            fh.write(text)
    print(f"anima corpus {fmt}: concepts={len(S)} train_pairs={len(train_pairs)} "
          f"held-out={tuple(opts['held_out'])} bytes={len(text.encode())} "
          f"seed={opts['seed']} -> {opts['out'] or '(stdout head)'}")
    if not opts["out"]:
        print(text[:600])


if __name__ == "__main__":
    main()
