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
  counterfactual-decl : H_9800 EPHEMERAL-DECLARATION grounding. Every episode RE-ASSIGNS
               stem->sense and operator->role, so the same stem carries the OPPOSITE declaration
               in the next episode and a parametric cache returns exactly the realized chance.
               Runtime lookup becomes the only CE minimiser. Emits the corpus + a 5-stratum eval
               manifest (`--decl-flip`) + a polarity audit re-parsed from the written file.
               EN-only. `anima corpus counterfactual-decl --lang en --out c.txt --held-out 32,8`
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
import hashlib
import os
import random
import re
import sys

# H_9694 g6bind imports the frozen `rho_fan` module (core/rho_fan.py) for its concept/detector
# vocabulary — the FIRST corpus format to need a core/ module. Mirror evaluate.py's bootstrap so a
# bare `import rho_fan` resolves under the installed anima_py package (where core/ = anima_py/core),
# not just in a dev checkout with core/ already on sys.path.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(_HERE)
sys.path.insert(0, os.path.join(_REPO, "core"))

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


_WP_NUM = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
           "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
           "seventeen", "eighteen", "nineteen", "twenty"]

# Opposite pairs for the double-negation family. Each is its own composition: the operator
# `opposite` applied twice must return the ORIGINAL word, which no single atom supplies.
_WP_OPP = [("hot", "cold"), ("big", "small"), ("fast", "slow"), ("light", "dark"),
           ("high", "low"), ("near", "far"), ("hard", "soft"), ("full", "empty"),
           ("open", "closed"), ("loud", "quiet"), ("wet", "dry"), ("early", "late"),
           ("strong", "weak"), ("rich", "poor"), ("clean", "dirty"), ("sharp", "dull")]

_WP_MIX = [("red", "yellow", "orange"), ("blue", "yellow", "green"), ("red", "blue", "purple"),
           ("black", "white", "grey"), ("red", "white", "pink"), ("blue", "green", "teal")]

_WP_DIR = [("north", "east", "northeast"), ("north", "west", "northwest"),
           ("south", "east", "southeast"), ("south", "west", "southwest")]

# ≥2 CARRIERS per family. A single carrier makes the carrier axis and the composition axis
# perfectly collinear — no experiment can then separate "it learned the composition" from
# "it learned this one template" (convergence corpus-py-1 ⑧/(E), measured on H_9327).
# Each carrier is (compose_template, bind_strip_template); {a} {b} {op} are filled per item.
_WP_CARRIERS = {
    "arith-add": [("{a} plus {b} gives the number", "{a} and {b} are two numbers here "),
                  ("adding {b} to {a} yields the number", "here are the numbers {a} , {b} ")],
    "arith-mul": [("{a} times {b} gives the number", "{a} and {b} are two numbers here "),
                  ("multiplying {a} by {b} yields the number", "here are the numbers {a} , {b} ")],
    "color-mix": [("{a} mixed with {b} makes the color", "{a} and {b} are two colors here "),
                  ("blending {a} and {b} produces the color", "here are the colors {a} , {b} ")],
    "double-neg": [("the opposite of the opposite of {a} is", "{a} and {b} are two words here "),
                   ("reversing {a} and then reversing it again gives", "here are the words {a} , {b} ")],
    "direction": [("{a} and {b} makes the direction", "{a} and {b} are two directions here "),
                  ("heading {a} then {b} points toward", "here are the directions {a} , {b} ")],
}
# `double-neg` is DELIBERATELY NOT in the default set. Double negation returns its own input,
# so the target necessarily occurs inside the cue — a model that merely COPIES a word out of the
# prompt scores a hit, and the atom-swap control does not catch it (the copier echoes the swapped
# word, not the original target, so the control stays clean while reach is inflated).
# ⚠️ The frozen 12-item `_WEAVE` battery contains TWO such items (one ko, one en), i.e. 1/6 of the
# production G1 instrument is copy-passable. Recorded, not silently fixed: the frozen battery is
# not edited here (burned-gate-no-refreeze) — this builder simply refuses to reproduce the defect.
_WP_FAMILIES = ("arith-add", "arith-mul", "color-mix", "direction")


def _wp_emit(fam, carriers, a, b, tgt, sa, sb, s_tgt):
    """One panel item per carrier. `sa`/`sb` = the atom-swap variant (a DIFFERENT pair whose
    true answer `s_tgt` != `tgt`), so the frozen atom-swap control still asks the same question:
    does `tgt` surface when it is the WRONG answer?"""
    out = []
    for ci, (comp_t, bind_t) in enumerate(carriers):
        cue = comp_t.format(a=a, b=b)
        swap = comp_t.format(a=sa, b=sb)
        bind = bind_t.format(a=a, b=b)
        out.append({"cue": cue, "target": tgt, "swap_cue": swap, "bind_cue": bind,
                    "lang": "en", "family": fam, "carrier": ci,
                    "swap_target": s_tgt, "a": a, "b": b})
    return out


def weavepanel_atom_exposure(items, corpus_paths):
    """H_9838 — count each panel item's ATOMS in the training corpus, with WORD BOUNDARIES.

    Declared as the open prerequisite when the panel landed (H_9827): a ρ·weave item whose atoms
    the model never saw does not measure a composition failure, it measures atom absence. The
    claim axis is composition, so exposure on the ATOM axis must be > 0 for the item to be
    readable at all (convergence corpus-py-1 (F)).

    Boundary-counted, never substring: `art` occurs inside `start`, `five` inside `fives`, and a
    raw `count()` exposure gate passes atoms the model never read as words — that exact defect
    was reintroduced the day after it was first recorded (corpus-py-1 (G)/(I)).
    """
    import re as _re
    need = set()
    for it in items:
        for w in _rho_words_en(it["cue"]) + [it["target"], it.get("a", ""), it.get("b", "")]:
            if len(w) >= 2:
                need.add(w)
    counts = {w: 0 for w in need}
    for cp in corpus_paths:
        with open(cp, "rb") as fh:
            raw = fh.read()
        text = raw.decode("utf-8", "replace").lower()
        for w in need:
            counts[w] += len(_re.findall(r"\b" + _re.escape(w) + r"\b", text))
    # OPERANDS and CARRIER are separate exposure axes and must not be pooled: an absent operand
    # makes the item unreadable for a COMPOSITION claim, while an absent carrier word puts the
    # probe in an out-of-distribution basin — a different defect with a different fix
    # (corpus-py-1 (8) carrier census / (12) untrained-carrier OOD basin).
    rows = []
    for it in items:
        ops = [w for w in (it.get("a", ""), it.get("b", "")) if len(w) >= 2]
        cue_ws = set(_rho_words_en(it["cue"]))
        carrier_ws = [w for w in cue_ws if w not in ops and len(w) >= 2]
        omin = min([counts.get(w, 0) for w in ops]) if ops else 0
        cmin = min([counts.get(w, 0) for w in carrier_ws]) if carrier_ws else 0
        rows.append({"cue": it["cue"], "target": it["target"], "family": it["family"],
                     "operand_min_occ": omin, "carrier_min_occ": cmin,
                     "target_word_occ": counts.get(it["target"], 0),
                     "readable": omin > 0, "carrier_seen": cmin > 0})
    n = len(rows)
    op_dead = [r for r in rows if not r["readable"]]
    car_dead = [r for r in rows if r["readable"] and not r["carrier_seen"]]
    tgt_dead = [r for r in rows if r["readable"] and r["target_word_occ"] == 0]
    return {"n": n, "readable": n - len(op_dead),
            "operand_absent": len(op_dead), "carrier_absent": len(car_dead),
            "target_absent": len(tgt_dead),
            "operand_absent_examples": [r["cue"] for r in op_dead[:6]],
            "carrier_absent_examples": [r["cue"] for r in car_dead[:6]],
            "rows": rows}


def _rho_words_en(text):
    """lowercase ASCII alnum split — same tokenization the frozen detector uses on EN."""
    out = []
    cur = []
    for ch in text:
        o = ord(ch)
        if 48 <= o <= 57 or 97 <= o <= 122:
            cur.append(ch)
        elif 65 <= o <= 90:
            cur.append(chr(o + 32))
        else:
            if cur:
                out.append("".join(cur)); cur = []
    if cur:
        out.append("".join(cur))
    return out


def build_weavepanel(families, max_items, seed):
    """H_9825 — parametric held-out recombination panel (the ρ·weave n=12 instrument fix).

    The frozen `_WEAVE` battery in cli/rho_axon.py carries TWELVE items, six of them on the ko
    lane that H_9327 measured 🧱 BINDING-walled. One item flipping moves the reported value by
    0.083 against a 0.30 bar with a 0.15 control cap — the threshold-fragility disease H_9820
    diagnosed at n=32, here at n=12. No budget ladder read through that panel can be decidable.

    This builder emits the SAME item shape (cue · target · swap_cue · bind_cue · lang) from
    parametric families so n scales, keeping the frozen bar, the frozen controls and the frozen
    scorer untouched — only the sample size moves.
    """
    fams = [f.strip() for f in families.split(",") if f.strip()] if families else list(_WP_FAMILIES)
    unknown = [f for f in fams if f not in _WP_CARRIERS]
    if unknown:
        raise SystemExit("anima-py corpus weavepanel: unknown family %s (known: %s)"
                         % (",".join(unknown), ",".join(_WP_FAMILIES)))
    items = []
    for fam in fams:
        car = _WP_CARRIERS[fam]
        if fam == "arith-add":
            grid = [(i, j) for i in range(2, 11) for j in range(2, 11) if i + j <= 20]
            for k, (i, j) in enumerate(grid):
                si, sj = grid[(k + 1) % len(grid)]
                if si + sj == i + j:                    # swap must change the true answer
                    si, sj = grid[(k + 2) % len(grid)]
                if si + sj == i + j:
                    continue
                items += _wp_emit(fam, car, _WP_NUM[i], _WP_NUM[j], _WP_NUM[i + j],
                                  _WP_NUM[si], _WP_NUM[sj], _WP_NUM[si + sj])
        elif fam == "arith-mul":
            grid = [(i, j) for i in range(2, 6) for j in range(2, 6) if i * j <= 20]
            for k, (i, j) in enumerate(grid):
                si, sj = grid[(k + 1) % len(grid)]
                if si * sj == i * j:
                    si, sj = grid[(k + 2) % len(grid)]
                if si * sj == i * j:
                    continue
                items += _wp_emit(fam, car, _WP_NUM[i], _WP_NUM[j], _WP_NUM[i * j],
                                  _WP_NUM[si], _WP_NUM[sj], _WP_NUM[si * sj])
        elif fam == "color-mix":
            for k, (a, b, t) in enumerate(_WP_MIX):
                sa, sb, st = _WP_MIX[(k + 1) % len(_WP_MIX)]
                if st == t:
                    continue
                items += _wp_emit(fam, car, a, b, t, sa, sb, st)
        elif fam == "direction":
            for k, (a, b, t) in enumerate(_WP_DIR):
                sa, sb, st = _WP_DIR[(k + 1) % len(_WP_DIR)]
                if st == t:
                    continue
                items += _wp_emit(fam, car, a, b, t, sa, sb, st)
        elif fam == "double-neg":
            for k, (a, b) in enumerate(_WP_OPP):
                sa, sb = _WP_OPP[(k + 1) % len(_WP_OPP)]
                if sa == a:
                    continue
                # target = a itself (opposite applied twice); the swap asks the same of `sa`,
                # for which `a` is the wrong answer.
                items += _wp_emit(fam, car, a, b, a, sa, sb, sa)
    # deterministic shuffle so a family's block structure cannot align with a seed-indexed
    # decode sweep (rho_weave uses SEEDS[0]+i per item).
    rnd = _wp_rand(seed)
    for i in range(len(items) - 1, 0, -1):
        j = rnd(i + 1)
        items[i], items[j] = items[j], items[i]
    if max_items > 0:
        items = items[:max_items]

    # ── audits (BLOCKING · a panel that fails these measures nothing) ──
    audit = {"n": len(items), "by_family": {}, "by_carrier": {}, "violations": []}
    seen_cue = {}
    for it in items:
        audit["by_family"][it["family"]] = audit["by_family"].get(it["family"], 0) + 1
        ck = "%s/c%d" % (it["family"], it["carrier"])
        audit["by_carrier"][ck] = audit["by_carrier"].get(ck, 0) + 1
        if it["target"] == it["swap_target"]:
            audit["violations"].append("swap keeps the true answer: " + it["cue"])
        if it["target"] in it["cue"].split():
            audit["violations"].append("target leaks into cue: " + it["cue"])
        if it["target"] in it["bind_cue"].split():
            audit["violations"].append("target leaks into bind-strip cue: " + it["bind_cue"])
        if it["cue"] in seen_cue and seen_cue[it["cue"]] != it["target"]:
            audit["violations"].append("same cue, two targets: " + it["cue"])
        seen_cue[it["cue"]] = it["target"]
    # carrier census — the collinearity guard (convergence corpus-py-1 (E))
    for fam in set(it["family"] for it in items):
        ncar = len(set(it["carrier"] for it in items if it["family"] == fam))
        if ncar < 2:
            audit["violations"].append(
                "family %s has %d carrier(s) — carrier axis is collinear with the composition "
                "axis, so no arm can separate them" % (fam, ncar))
    return items, audit


def _wp_rand(seed):
    """Deterministic LCG (no `random` import — the builder must be byte-reproducible from seed
    alone, which is what makes a ckpt's panel re-auditable · corpus-py-1 (J))."""
    state = [(seed * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)]

    def nxt(n):
        state[0] = (state[0] * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
        return (state[0] >> 33) % n if n > 0 else 0
    return nxt


# ── H_9837 falsidrill — raise the model's falsifiable-claim emission rate ──
# H_9828 censused the EN training corpus at P(falsifiable) = 0.006461. rho·fan passes its
# falsifiability leg on >=1 hit in 8 draws, so clearing it even half the time needs p >= 0.083
# — about 13x the corpus rate. This builder is the density lever (the H_9267 recipe: when the
# corpus carries the structure, the CE objective can learn it).
#
# The eval seed is `_rho_fan_concepts()[0] + ": "`. Every word of EVERY eval concept is held out
# of this drill, so the claim being tested is "produces falsifiable claims about a concept it was
# never drilled on" — measured at exposure 0 on its own axis (convergence corpus-py-1 (F)).
# The held-out axis is the eval CONCEPT, so the words that carry the concept must never appear
# in the drill. Function words are a different thing: `when`/`from`/`into`/`the` are not concepts,
# they occur throughout the replay corpus and all of English, and holding them out is both
# meaningless and impossible — it would only starve the drill of grammar. Split accordingly, and
# enforce only the content set. (Caught by this builder's audit when carrier count went to 12 and
# a frame used `when`.)
_FD_HELD_OUT = {"consciousness", "arises", "cells", "tension", "ripples", "distant", "minds",
                "memory", "composes", "meaning", "silence", "carries", "information",
                "engine", "dreams", "alone"}
_FD_HELD_OUT_FUNCTION = {"between", "into", "still", "when", "the", "new", "from"}

# subjects/objects — ordinary dictionary nouns, disjoint from every eval-concept word above.
_FD_SUBJ = ["rainfall", "traffic", "sleep", "exercise", "altitude", "humidity", "sunlight",
            "practice", "noise", "temperature", "pressure", "salt", "caffeine", "fatigue",
            "crowding", "wind", "sugar", "vibration", "dust", "voltage"]
_FD_OBJ = ["harvest", "delay", "recall", "endurance", "boiling", "corrosion", "growth",
           "accuracy", "error", "expansion", "leakage", "yield", "alertness", "reaction",
           "spread", "erosion", "decay", "wear", "fouling", "current"]
_FD_DIR = ["rises", "falls", "climbs", "drops"]

# FROZEN detector vocabulary, used verbatim — these sets ARE the definition of the target
# structure, so drilling them is the density intervention, not a detector hack. What makes the
# result falsifiable is the held-out concept axis plus the ablation arm below.
# FROZEN detector vocabulary, split BY PART OF SPEECH. The first draft mixed verbs and
# comparatives in one slot and produced ungrammatical drill lines ("salt lower a degree of
# reaction that drops"). Training a byte-LM on broken English would trade a falsifiability gain
# for a fluency loss and make any positive unreadable (corpus-py-1 ⑥: small-corpus CPT kills what
# the corpus omits — here, grammar).
_FD_COMP_VI = ["increases", "decreases"]              # intransitive — take no object
_FD_COMP_VT = ["predicts", "causes"]                  # transitive — the carrier supplies the object
_FD_COMP_A = ["higher", "lower", "greater", "faster", "slower", "stronger", "weaker"]
_FD_MEAS = ["rate", "number", "count", "amount", "level", "degree", "threshold", "ratio",
            "frequency", "probability", "magnitude", "score", "value", "quantity",
            "duration", "speed", "size", "strength", "density"]

# ABLATION vocabulary — same part of speech, same sentence shape, NOT in the detector sets.
_FD_COMP_VI_ABL = ["shifts", "changes"]
_FD_COMP_VT_ABL = ["shapes", "follows"]
_FD_COMP_A_ABL = ["broader", "narrower", "wider", "softer", "rougher", "smoother", "plainer"]
_FD_MEAS_ABL = ["mood", "colour", "texture", "flavour", "shade", "aroma", "grain",
                "tone", "polish", "pattern", "shape", "finish", "gloss", "tint",
                "hue", "sheen", "weave", "bloom", "sparkle"]

# >=2 carriers (convergence corpus-py-1 (E)): one template makes the carrier axis collinear with
# the falsifiability axis, so no arm could separate "learned the structure" from "learned this
# sentence shape". `{cv}` takes a verb, `{ca}` a comparative — keeping the lines grammatical.
# H_9852 — carrier count raised 3 -> 12 with varied length and word order.
# WHY (measured, not guessed): the 3-carrier build damaged the model. After 2000 CPT steps on a
# 15%-drill mix, rho·form went PASS -> FAIL through its CONTROL — a byte-shuffled copy of the
# model's own output cleared the form gate 40% of the time (cap 0.05), i.e. the output had become
# an order-free bag of known words. Three templates repeated 24,000 times teach word IDENTITY and
# nothing about word ORDER, so shuffling stops mattering. More carriers, more lengths, and both
# clause orders keep order informative while the falsifiable structure stays constant.
_FD_CARRIERS = [
    "if {s} {cvi} , the {m} of {o} {d} .",
    "{s} {cvt} a {ca} {m} of {o} than {alt} does .",
    "whenever {s} {cvi} , the measured {m} of {o} {d} .",
    "the {m} of {o} {d} if {s} {cvi} .",
    "the {m} of {o} is {ca} than the {m} of {alt} .",
    "when {s} {cvi} , we expect the {m} of {o} to be {ca} .",
    "{s} {cvt} the {m} of {o} , and {alt} {cvt} it {ca} .",
    "a {ca} {m} of {o} follows if {s} {cvi} .",
    "if {s} {cvi} more than {alt} , the {m} of {o} {d} .",
    "the recorded {m} of {o} {d} whenever {s} {cvi} .",
    "{s} {cvt} a {m} of {o} that is {ca} than the one {alt} {cvt} .",
    "compared with {alt} , {s} {cvt} a {ca} {m} of {o} .",
]

# The ablation arm needs its FRAMES ablated too, not just the slot fillers. Caught by this
# builder's own audit: with the real frames the ablation arm still scored 0.378 falsifiable,
# because `if`/`whenever`/`than` are themselves comparator words and `measured` is a measurable
# word — the template supplied the conjunction no matter what went into the slots. A control that
# leaks the very structure it removes is not a control (prereg-md-2: a control that can pass
# without the mechanism measures the ceiling).
_FD_CARRIERS_ABL = [
    "as {s} {cvi} , the {m} of {o} {d} .",
    "{s} {cvt} a {ca} {m} of {o} beside {alt} .",
    "while {s} {cvi} , the noted {m} of {o} {d} .",
    "the {m} of {o} {d} as {s} {cvi} .",
    "the {m} of {o} looks {ca} beside the {m} of {alt} .",
    "while {s} {cvi} , we notice the {m} of {o} looks {ca} .",
    "{s} {cvt} the {m} of {o} , and {alt} {cvt} it {ca} .",
    "a {ca} {m} of {o} appears while {s} {cvi} .",
    "as {s} {cvi} beside {alt} , the {m} of {o} {d} .",
    "the noted {m} of {o} {d} while {s} {cvi} .",
    "{s} {cvt} a {m} of {o} that looks {ca} beside the one {alt} {cvt} .",
    "next to {alt} , {s} {cvt} a {ca} {m} of {o} .",
]


def build_falsidrill(n_lines, seed, ablate):
    """H_9837 — EN drill corpus dense in falsifiable claims (or its matched-surface ablation).

    Returns (text, audit). The audit is BLOCKING: it re-runs the production detector over every
    emitted line and refuses to ship a corpus whose real arm is not overwhelmingly falsifiable,
    or whose ablation arm is not overwhelmingly NOT falsifiable — a builder that silently emits
    the wrong structure would make the whole campaign unreadable.
    """
    import sys as _s
    _s.path.insert(0, __file__.rsplit("/", 2)[0] + "/core")
    from rho_fan import _rho_fan_is_falsifiable, _rho_fan_dict_load, _rho_fan_words

    comp_vi = _FD_COMP_VI_ABL if ablate else _FD_COMP_VI
    comp_vt = _FD_COMP_VT_ABL if ablate else _FD_COMP_VT
    comp_a = _FD_COMP_A_ABL if ablate else _FD_COMP_A
    meas = _FD_MEAS_ABL if ablate else _FD_MEAS
    rnd = _wp_rand(seed)
    lines = []
    for i in range(n_lines):
        subj = _FD_SUBJ[rnd(len(_FD_SUBJ))]
        alt = _FD_SUBJ[rnd(len(_FD_SUBJ))]
        while alt == subj:
            alt = _FD_SUBJ[rnd(len(_FD_SUBJ))]
        o = _FD_OBJ[rnd(len(_FD_OBJ))]
        cvi = comp_vi[rnd(len(comp_vi))]
        cvt = comp_vt[rnd(len(comp_vt))]
        ca = comp_a[rnd(len(comp_a))]
        m = meas[rnd(len(meas))]
        d = _FD_DIR[rnd(len(_FD_DIR))]
        cars = _FD_CARRIERS_ABL if ablate else _FD_CARRIERS
        car = cars[rnd(len(cars))]
        lines.append(car.format(s=subj, cvi=cvi, cvt=cvt, ca=ca, m=m, o=o, d=d, alt=alt))
    text = "\n".join(lines) + "\n"

    known = _rho_fan_dict_load()
    hits = sum(1 for l in lines if _rho_fan_is_falsifiable(l, known))
    leaked = sorted({w for l in lines for w in _rho_fan_words(l) if w in _FD_HELD_OUT})
    carriers = len(_FD_CARRIERS_ABL if ablate else _FD_CARRIERS)
    audit = {"n_lines": len(lines), "falsifiable": hits,
             "falsifiable_rate": (hits / len(lines)) if lines else 0.0,
             "arm": ("ablation" if ablate else "real"), "carriers": carriers,
             "held_out_leak": leaked, "violations": []}
    if leaked:
        audit["violations"].append(
            "eval-concept word(s) leaked into the drill: %s — the held-out axis is destroyed and "
            "the eval becomes retrieval" % ",".join(leaked))
    if not ablate and audit["falsifiable_rate"] < 0.95:
        audit["violations"].append(
            "real arm is only %.3f falsifiable — the density intervention would be diluted"
            % audit["falsifiable_rate"])
    if ablate and audit["falsifiable_rate"] > 0.02:
        audit["violations"].append(
            "ablation arm is %.3f falsifiable — it is not a clean structure-off control"
            % audit["falsifiable_rate"])
    if carriers < 2:
        audit["violations"].append("carrier axis is collinear with the falsifiability axis")
    return text, audit


# ── H_9839 dreamgen — the dream node's COMPOSITION LAW as the manipulated variable ──
#
# WHY THIS FORMAT EXISTS, and why no existing one answers it. `core/dream_compose.py`'s own header
# states what the production dream node is: two co-replayed anchors blended by "coord midpoint ·
# tension5 mean · radius max · lane=dream" — "a designed geometric law (NOT a learned semantic
# insight, c9)" — with `text` left EMPTY (a NARRATIVE hook). A midpoint is ADDITIVE by
# construction: every child coordinate is a per-axis average, so nothing in the child depends on
# the PAIR beyond what each parent already supplies alone. That is precisely the place H_9304
# measured non-additive information +0.0023 nats (TOST-equivalent to 0). So the question this
# format makes measurable is: does swapping the dream TARGET from a geometric blend to the
# derivation of a DECLARED composition rule (the H_9267 XBIND notion) manufacture cross-boundary
# joint information in the DATA — before any GPU is rented?
#
# ARMS (`--dream-target`). The three treatment arms share ONE RNG stream: the anchors, the
# coordinates, the tension5 vectors, the radii and the declared rule are byte-identical across
# them at a fixed --seed. The ONLY thing that varies is how the dream's `text=` payload is
# derived — which is exactly the card's DV.
#   midpoint     PRE-REGISTERED FAILURE BASELINE. The production geometric law, extended to the
#                text lane by the SAME law: child token k = pool_k[(idx_A_k + idx_B_k)//2], the
#                per-axis midpoint of the parents' token indices, computed by calling the
#                production `dc_vec_mid` itself. (Production leaves text="" — an empty payload is
#                unreadable by construction and would make the baseline vacuous, so the baseline
#                is the geometric law's own extension to the lane under test. Stated, not hidden.)
#   rule-derived TREATMENT. The night DECLARES a 3-slot selector rule (`RULE ABA`) in its header;
#                child token k = the token in slot k of parent A or parent B as the rule selects.
#                The child is then a SELECTION from the pair under a declared rule: neither parent
#                alone, nor the rule alone, determines it.
#   shuffled     MARGINALS-MATCHED CONTROL. Byte-identical dream lines to `rule-derived` (same
#                multiset, asserted by sha), re-attached to the WRONG night by a deterministic
#                rotation. Composition destroyed, marginals preserved. Must collapse.
#   planted      POSITIVE CONTROL for the corpus geometry (NOT a treatment arm). The night's body
#                carries a fresh high-entropy block and the NEXT night opens with that block
#                verbatim — the corpus-shaped analogue of `mi_compress.plant_crossboundary`. If
#                mi-screen does not FIRE on this arm, this corpus family's block layout is
#                unreadable by the screener and NO arm's number may be interpreted
#                (positive-control-before-reading-a-negative).
#   pedestal     ZERO-TRUTH PEDESTAL (NOT a treatment arm). Byte-for-byte the same construction
#                with the carry-over REMOVED — the next night opens with its OWN fresh block. Must
#                REFUSE. If it fires, the reading is manufactured (phi-estimator-needs-zero-truth-
#                pedestal).
#
# WHY THE STREAM IS SHAPED LIKE A NIGHT. `stream_mi` asks whether segment t's BODY predicts
# segment t+1's PREFIX beyond what t's last `win` bytes already give. So the layout is, per night:
#   [dreams composed from the PREVIOUS night's anchors] [NIGHT header + RULE] [this night's
#   ANCHOR declarations] [drift filler >= win bytes]
# — which is `dc_compose_window`'s own semantics (anchors replayed in window w are composed into
# dream nodes) written down as a stream. Nights are separated by a BLANK LINE, so
# `MI.segments_from_path` segments on the corpus's own record separator at EVERY geometry; that is
# what makes the `--mi-robust` sweep a test of win/span and NOT a re-cut of the night structure
# (with `--mi-seg-lines` the /8 geometry would slice nights into eighths and destroy the very
# structure under test). The night's byte size is a FROZEN module constant, never a flag, so no
# knob in this builder can move the verdict (no tune-to-green).
_DG_STAGE = 3                # N3 — `dc_stage_replay_budget(3)` = 7 replayed anchors = 21 pairs
_DG_COORD_D = 6              # anchor coordinate dimensionality
_DG_POOL = 64                # tokens per text slot: the body narrows 64 -> 7, a readable amount
_DG_FILLER_LINES = 150       # FROZEN: sets the drift tail (>= W_TAIL bytes). NOT a flag.
_DG_PLANT_LINES = 24         # FROZEN: control block size (>= P_PRED bytes at the primary geometry)
_DG_PLANT_WIDTH = 96
_DG_C = "bdfgklmnprstvz"
_DG_V = "aeiou"
_DG_STRIDE = 1097            # prime, coprime to 14^3·5^2 — keeps `_dg_pool` a bijection
# The declared rule is a 3-slot parent selector, and the CONSTANT selectors AAA/BBB are excluded
# on purpose: under them the child is a verbatim copy of ONE parent and the other contributes
# nothing, so a quarter of the nights would not be pair-determined at all — the very property
# `rule-derived` exists to have. Only the six mixed selectors are drawn.
_DG_RULES = ("AAB", "ABA", "ABB", "BAA", "BAB", "BBA")
# ORDER IS THE GATE ORDER, not a preference: the two controls are listed first because the
# treatment rows may not be read until both certify (the run_mi_screen battery idiom, one level up).
_DG_TARGETS = ("planted", "pedestal", "midpoint", "rule-derived", "shuffled")


def _dg_pool(n, offset):
    """FROZEN deterministic CVCVC nonce enumeration (same idiom as storebind's builtin pool).

    Nonces, not English: real words carry corpus-external statistics a compressor can exploit
    unevenly across arms, which would put a confound exactly on the DV. The index map is
    mixed-radix and therefore injective, so disjoint `offset` ranges give disjoint pools.

    The `* _DG_STRIDE` is not decoration. Straight mixed-radix varies the LOWEST digit fastest,
    so a 64-long run shares its last three letters (`zibab`/`rebab`/...) and only two characters
    per token actually discriminate. A copy across a segment boundary would then be two bytes
    wide, and the treatment arm would be handicapped by the alphabet rather than by the law under
    test. The stride is coprime to the radix product (14·5·14·5·14 = 2^3·5^2·7^3), so the map
    stays a bijection while spreading every digit."""
    out, i = [], offset
    nc, nv = len(_DG_C), len(_DG_V)
    period = nc * nc * nc * nv * nv
    while len(out) < n:
        k = (i * _DG_STRIDE) % period
        out.append(_DG_C[k % nc] + _DG_V[(k // nc) % nv] + _DG_C[(k // (nc * nv)) % nc]
                   + _DG_V[(k // (nc * nc * nv)) % nv] + _DG_C[(k // (nc * nc * nv * nv)) % nc])
        i += 1
    return out


def _dg_vec(v):
    return ",".join("%.4f" % x for x in v)


def _dg_block_lines(rnd):
    """A high-entropy block, rendered as lines — the control arms' carried quantity."""
    return ["".join(chr(33 + rnd(94)) for _ in range(_DG_PLANT_WIDTH))
            for _ in range(_DG_PLANT_LINES)]


# ── `--dream-anchors real:<ckpt.clm>` — the SYNTHETIC-GEOMETRY SWAP (H_9838's lesson) ──
#
# WHY THIS FLAG EXISTS. H_9838 landed a headline positive (CA3 multi-step completion at 12x
# derived chance, chaining lesion at the floor, 3 seeds x 3 geometries, independently reproduced)
# and then DIED when the only thing that changed was the input source: swapping its PLANTED
# integer code fixture for the production trunk's REAL penultimate representations turned the
# 16-item load from CERTIFIED to INVALID (value-shuffled pedestal 0.3750 over a 0.3077 bar) and
# the 32-item load likewise (0.1562 over 0.1500). Diagnosis: the planted codes were effectively
# orthogonal (within .0469 / across .0117) while real reps overlap 2.2x (.0625 / .0260) — and
# `core/hippo_lane.py`'s own header had already warned that "Raw single-token 303M reps are
# near-collinear". The result had been manufactured by hand-made favourable geometry.
#
# dreamgen has the SAME SHAPE. Its anchors' coordinates — including the per-slot token indices
# that the composition law actually operates on — are drawn from the builder's own `_wp_rand`,
# i.e. iid-uniform over a 64-token pool. That is a hand-made near-orthogonal world: two parents
# differ in every slot with probability 63/64, so `rule-derived` always has a genuine choice to
# make and `midpoint` always lands away from both parents. Real 303M anchors may not have that
# spread at all. So the flag swaps ONLY the input source: the anchor's coordinates come from the
# production trunk's real pre-readout penultimate (`core/decode.py::clm_load_weights` ->
# `clm_penult_pooled_W`, the py-canonical rep path, `a_eval_py_canonical`) of the anchor's own
# entity string. Everything else is untouched — same nights, same seeds, same arms, same
# composition laws, same blocking audit, same `mi-screen --mi-robust` judging, same eps.
#
# WHAT STAYS BYTE-IDENTICAL. The real path still CONSUMES every RNG draw the synthetic path
# consumes, in the same order, and only then overwrites the drawn fields. So the rule sequence,
# the entity-string draws, the drift filler, the plant blocks and the night order are byte-
# identical between `--dream-anchors synthetic` and `real:` at a fixed seed. The single
# difference is where an anchor's coordinates come from. Default = `synthetic` => the pre-swap
# command is byte-identical to before this flag existed (zero regression).
#
# THE REDUCER IS FROZEN AND SCALE-FREE, and was fixed BEFORE any real-anchor number was read.
# A pooled 303M rep is a d=3784 vector whose units are not a design choice of mine, so a reducer
# with an absolute scale in it (e.g. squash the raw chunk mean) would collapse or spread for a
# UNITS reason rather than a geometry reason. Both halves are therefore invariant to scaling the
# rep by any positive constant:
#   token index (slot s of 3)  contiguous chunk s -> argmax of |.| -> position bucketed into
#                              [0, _DG_POOL) by pos*_DG_POOL//len. Scale-invariant, monotone in
#                              position, and the same contiguous/abs/argmax idiom that
#                              `core/decode.py::penult_fold8` already freezes for this rep.
#   coord / tension5 / radius  contiguous chunk mean DIVIDED BY the rep's own mean |.| (a
#                              scale-free ratio), then the parameter-free monotone squash
#                              `_dg_softsign01` into (0,1) — the range `dc_make_anchor` gets from
#                              the synthetic draw.
# No knob of this reducer is a flag, and it is not re-picked after seeing a result (no
# tune-to-green). If real anchors collapse under it, that collapse is a geometry fact about the
# production trunk, which is exactly the question H_9838 forces this card to answer.
def _dg_softsign01(x):
    """Parameter-free monotone R -> (0,1). No cut point, no temperature, nothing to tune."""
    return 0.5 * (1.0 + x / (1.0 + abs(x)))


def _dg_chunks(d, n):
    """n contiguous [lo, hi) chunks of a length-d vector; the remainder joins the LAST chunk."""
    w = d // n
    return [(i * w, (i + 1) * w if i < n - 1 else d) for i in range(n)]


def _dg_real_anchor_fields(pooled):
    """FROZEN reducer: one REAL pooled penultimate -> (coord[6], tension5[5], radius, idx[3])."""
    d = len(pooled)
    scale = sum(abs(v) for v in pooled) / float(d) or 1.0

    def chunk_val(lo, hi):
        return _dg_softsign01((sum(pooled[lo:hi]) / float(hi - lo)) / scale)

    coord = [chunk_val(lo, hi) for lo, hi in _dg_chunks(d, _DG_COORD_D)]
    t5 = [chunk_val(lo, hi) for lo, hi in _dg_chunks(d, 5)]
    radius = chunk_val(0, d)
    idx = []
    for lo, hi in _dg_chunks(d, 3):
        n = hi - lo
        best, bestv = 0, -1.0
        for j in range(n):
            v = abs(pooled[lo + j])
            if v > bestv:
                best, bestv = j, v
        idx.append(min(_DG_POOL - 1, best * _DG_POOL // n))
    return coord, t5, radius, tuple(idx)


def _dg_real_reader(ckpt):
    """Mount the production trunk ONCE and return a memoised entity-string -> pooled reader.

    The memo is a cache of a deterministic function, not a shortcut: `clm_penult_pooled_W` is
    read-only (no readout, no sampling, no perturbation), so a repeated entity string has a
    repeated rep by construction."""
    import decode as DEC                       # core/decode.py — the py-canonical rep path
    W = DEC.clm_load_weights(ckpt)
    if not W or W.get("ok") is False:
        raise SystemExit("corpus dreamgen: --dream-anchors real:%s is not a decodable .clm" % ckpt)
    cache = {}

    def rep(s):
        if s not in cache:
            cache[s] = DEC.clm_penult_pooled_W(W, s)
        return cache[s]
    return rep, cache


def _dg_rep_geometry(cache):
    """Witness: HOW SPREAD is the real anchor rep set, in the same currency H_9838 diagnosed in.

    That card's post-mortem was a cosine-overlap pair (planted codes .0469 within / .0117 across
    vs real reps .0625 / .0260, a 2.2x overlap), so this builder reports the same kind of fact
    about its own anchors rather than leaving a reader to infer it from the code count."""
    import numpy as np
    keys = sorted(cache)
    if len(keys) < 2:
        return {}
    M = np.array([cache[k] for k in keys], dtype=np.float64)
    M = M / (np.sqrt((M * M).sum(axis=1, keepdims=True)) + 1e-300)
    C = M @ M.T
    iu = np.triu_indices(len(keys), 1)
    v = C[iu]
    return {"n_distinct_entities": len(keys), "cos_mean": float(v.mean()),
            "cos_min": float(v.min()), "cos_max": float(v.max())}


def build_dreamgen(nights, target, seed, real_ckpt=None):
    """H_9839 — emit one arm of the dream-composition-law corpus. Returns (text, audit).

    The audit is BLOCKING (the falsidrill idiom): it re-reads the emitted stream and refuses to
    ship a corpus whose blocks the judge cannot segment, whose anchors do not clear the tail at
    the primary geometry, or whose pair count is under `mi_compress.MIN_PAIRS` — every one of
    those would turn an unreadable instrument into a fake corpus negative."""
    import mi_compress as MI          # the JUDGE's own frozen geometry — never re-declared here
    from dream_compose import (dc_make_anchor, dc_stage_replay_budget, dc_compose_window,
                               dc_vec_mid)

    rnd = _wp_rand(seed)
    budget = dc_stage_replay_budget(_DG_STAGE)      # read from core, not re-stated
    pools = [_dg_pool(_DG_POOL, 0), _dg_pool(_DG_POOL, 1000), _dg_pool(_DG_POOL, 2000)]
    fill = _dg_pool(64, 3000)
    planted_arm = target in ("planted", "pedestal")
    real_rep, real_cache = _dg_real_reader(real_ckpt) if real_ckpt else (None, None)

    heads, carry, body_end, all_idx = [], [], [], []
    for t in range(nights):
        rule = _DG_RULES[rnd(len(_DG_RULES))]
        anchors, idx = [], {}
        for k in range(budget):
            ii = (rnd(_DG_POOL), rnd(_DG_POOL), rnd(_DG_POOL))
            coord = [rnd(10000) / 10000.0 for _ in range(_DG_COORD_D)]
            radius = rnd(10000) / 10000.0
            t5 = [rnd(10000) / 10000.0 for _ in range(5)]
            if real_rep is not None:
                # THE SWAP, and nothing else. Every draw above is consumed first so the rest of
                # the stream (rules, drift, plants, night order) is byte-identical to synthetic;
                # the anchor's ENTITY STRING is the RNG-drawn one either way. Only where the
                # anchor's coordinates come from changes: the production trunk's real pooled
                # penultimate of that entity string replaces the uniform draw.
                coord, t5, radius, ii = _dg_real_anchor_fields(
                    real_rep(" ".join(pools[s][ii[s]] for s in range(3))))
            a = dc_make_anchor("a%03d.%d" % (t, k), coord, "wake", radius, t5,
                               " ".join(pools[s][ii[s]] for s in range(3)))
            a["replay_window"] = t
            anchors.append(a)
            idx[a["id"]] = ii
            all_idx.append(tuple(ii))
        head = ["NIGHT %03d STAGE %d BUDGET %d RULE %s" % (t, _DG_STAGE, budget, rule)]
        for a in anchors:
            head.append("ANCHOR %s coord=%s t5=%s r=%.4f text=%s"
                        % (a["id"], _dg_vec(a["coord"]), _dg_vec(a["tension5"]),
                           a["radius"], a["text"]))
        plant = _dg_block_lines(rnd) if planted_arm else None
        if plant:
            head += ["PLANT " + p for p in plant]
        # the body ends here; everything after is drift filler, which is what the tail sees.
        body_end.append(len("\n".join(head)) + 1)
        head += ["DRIFT %04d %s" % (n, " ".join(fill[rnd(len(fill))] for _ in range(5)))
                 for n in range(_DG_FILLER_LINES)]
        heads.append(head)

        if planted_arm:
            src = plant if target == "planted" else _dg_block_lines(rnd)
            carry.append(["CARRY " + p for p in src])
            continue
        lines = []
        for d in dc_compose_window(anchors, _DG_STAGE, t):
            ia, ib = idx[d["parent_a"]], idx[d["parent_b"]]
            if target == "midpoint":
                # the PRODUCTION law, applied to the text lane: a per-axis midpoint.
                sel = [int(dc_vec_mid([ia[s]], [ib[s]])[0]) for s in range(3)]
            else:
                sel = [(ia[s] if rule[s] == "A" else ib[s]) for s in range(3)]
            lines.append("DREAM %s coord=%s t5=%s r=%.4f text=%s"
                         % (d["id"], _dg_vec(d["coord"]), _dg_vec(d["tension5"]), d["radius"],
                            " ".join(pools[s][sel[s]] for s in range(3))))
        carry.append(lines)

    m = max(0, nights - 1)
    order, shift = list(range(m)), 0
    if target == "shuffled" and m >= 2:
        # deterministic rotation: 0 fixed points for any shift != 0 (mod m), and a half-period
        # shift puts a dream's true parents as far from its host night as the stream allows.
        shift = max(2, m // 2) % m or 1
        order = [(i + shift) % m for i in range(m)]
    blocks = []
    for t in range(nights):
        lines = list(carry[order[t - 1]]) if t >= 1 else []
        lines += heads[t]
        blocks.append("\n".join(lines))
    text = "\n\n".join(blocks) + "\n"

    # ── BLOCKING audit — re-read from the emitted string, never from the builder's intent ──
    raw = text.encode("utf-8")
    segs = [b for b in raw.split(b"\n\n") if b.strip()]
    lens = [len(b) for b in segs]
    prefix = [len(("\n".join(carry[order[t - 1]]) + "\n").encode("utf-8")) if t >= 1 else 0
              for t in range(nights)]
    margins = [lens[t] - (prefix[t] + body_end[t]) for t in range(min(len(lens), nights))]
    dream_lines = sorted(l for b in blocks for l in b.split("\n")
                         if l.startswith("DREAM ") or l.startswith("CARRY "))
    # the geometry witness is DREAM-only: a control arm's CARRY line has no `text=` field, so
    # including it would make the two shas coincide by construction and witness nothing.
    geom = sorted(l.split(" text=")[0] for l in dream_lines if l.startswith("DREAM "))
    # anchor-source witness. `distinct_anchor_codes` is REPORTED, never blocking: on real anchors
    # a collapsed code set is the FINDING (the trunk's reps are near-collinear), not a builder bug,
    # and a blocking check would hide it behind a refusal instead of measuring it.
    anchor_codes = sorted(set(all_idx))
    audit = {
        "arm": target, "nights": nights, "seed": seed, "budget": budget,
        "anchor_source": ("real:" + real_ckpt) if real_ckpt else "synthetic",
        "n_anchors": len(all_idx), "distinct_anchor_codes": len(anchor_codes),
        "distinct_slot_values": [len(set(c[s] for c in all_idx)) for s in range(3)],
        "real_anchor_geometry": _dg_rep_geometry(real_cache) if real_cache else None,
        "bytes": len(raw), "lines": text.count("\n"),
        "n_segments": len(segs), "n_pairs": max(0, len(segs) - 1),
        "min_block_bytes": min(lens) if lens else 0, "max_block_bytes": max(lens) if lens else 0,
        "min_body_tail_margin_bytes": min(margins) if margins else 0,
        "sep_blank_lines": raw.count(b"\n\n"), "sep_triple": raw.count(b"\n\n\n"),
        "shuffle_shift": shift,
        "shuffle_fixed_points": sum(1 for i, j in enumerate(order) if i == j) if target == "shuffled" else None,
        "carry_multiset_sha": hashlib.sha256("\n".join(dream_lines).encode("utf-8")).hexdigest()[:16],
        "geometry_field_sha": hashlib.sha256("\n".join(geom).encode("utf-8")).hexdigest()[:16],
        "judge_geometry": {"W_TAIL": MI.W_TAIL, "P_PRED": MI.P_PRED, "MIN_PAIRS": MI.MIN_PAIRS},
        "violations": [],
    }
    if audit["sep_triple"]:
        audit["violations"].append(
            "%d triple newline(s) present — segments_from_path would switch separator and re-cut "
            "the stream" % audit["sep_triple"])
    if audit["n_segments"] != nights:
        audit["violations"].append("blank-line split yields %d segment(s) for %d night(s) — the "
                                   "judge would not see the night as the record unit"
                                   % (audit["n_segments"], nights))
    if audit["min_block_bytes"] < MI.W_TAIL + MI.P_PRED:
        audit["violations"].append(
            "shortest night is %dB < win+span %dB — segments_from_path DROPS it and the arm "
            "silently loses power" % (audit["min_block_bytes"], MI.W_TAIL + MI.P_PRED))
    if audit["min_body_tail_margin_bytes"] <= MI.W_TAIL:
        audit["violations"].append(
            "anchors sit only %dB before the block end (win=%d) — they would fall in the TAIL, "
            "which both conditionings already carry, so the ceiling is 0 by construction"
            % (audit["min_body_tail_margin_bytes"], MI.W_TAIL))
    if audit["n_pairs"] < MI.MIN_PAIRS:
        audit["violations"].append("%d pair(s) < MIN_PAIRS %d — underpowered by the judge's own "
                                   "constant" % (audit["n_pairs"], MI.MIN_PAIRS))
    if target == "shuffled" and audit["shuffle_fixed_points"]:
        audit["violations"].append("%d fixed point(s) in the shuffle — not a derangement"
                                   % audit["shuffle_fixed_points"])
    return text, audit


def _parse_args(argv):
    fmt = argv[0] if argv else ""
    # H_9643 --held-out-frac: hold out a FRACTION of the (i,j) pair grid instead of the single
    # --held-out cell. 0.0 = the legacy single-pair behaviour (byte-identical default).
    # H_9267's one-cell hold-out leaves the grid ~fully covered and a K=1 baseline already hits
    # D-acc 1.000 — a ceiling the faction lever cannot move. Starving coverage is what makes the
    # K=1 floor pre-gate (<=0.6) measurable at all (G1 is a DATA wall — H_9304).
    opts = {"out": None, "held_out": (0, 1), "held_out_frac": 0.0, "comp_per_pair": 280, "split_seed": 1,
            "single_per_concept": 300, "seed": 7, "concepts": None,
            "atoms": None, "reps": 40, "replay": 40,
            "lang": DEFAULT_LANG, "lexicon": None, "mine": 0, "n_seen": 20, "n_held": 29,
            "corpus": [], "k_ctx": 24, "ctx_bytes": 64, "min_occ": 200, "neutral_tol": 0.05,
            "tail": "", "n2_eval": None, "n2_seen": None, "novel": None,
            "carrier_only": False, "held_swap": False, "decl_only": False, "held_n": None, "surface": "flip1_suffix",
            "collision_split": False, "nonce_fillers": 3, "win": 64,
            "bridge_split": False, "decl_ablate": False,
            # H_9410 RULE-VS-CACHE PRESSURE ENVELOPE instruments:
            #   --max-atoms N          one-shot EN atom miner scaled to N (greedy G-SUBSTR, drops
            #                          colliders instead of aborting; reports the actual ceiling).
            #   --polarity {real,assigned}  assigned = RANDOM balanced polarity keyed by --assign-seed
            #                          (a from-scratch model never used real polarity, so real sentiment
            #                          is functionless; makes mining trivial at 10^3, G-BALANCE free,
            #                          form->polarity leak killed — the strongest confound control).
            #   --assign-seed k        the seed the balanced random assignment is deterministic in.
            "max_atoms": 0, "polarity": "real", "assign_seed": 0,
            # H_9423 storebind (co-trained store-lookup bridge · S0):
            #   --entity-pool F        (H_9683) external one-ascii-atom-per-line entity pool,
            #                          replacing the builtin CVCVC nonce enumeration. Omitted =>
            #                          builtin, byte-identical to before.
            "n_blocks": 4000, "store_slots": 8, "entity_pool": None,
            # H_9520 study-replay (consolidation-CPT corpus from an `anima study` transcript):
            #   --transcript T.jsonl   the study transcript (teacher percepts + substrate emits)
            #   --study-frac 0.05      teacher-content byte share of the replay-mix (small % · rest = base replay)
            #   --scramble-seed 11     the C2 word-shuffle seed (kept separate so C2 is reproducible)
            "transcript": None, "study_frac": 0.05, "scramble_seed": 11,
            # H_9844 mi-screen (compression-MI corpus screener · core/mi_compress.py H_9806):
            #   --mi-win / --mi-span   the (tail-context, predicted-prefix) byte geometry
            #   --mi-estimator         gzip|ppm|markov6|all (all = the shipped 3-estimator battery)
            #   --mi-eps               decoration guard in bpb — an over-floor lift below this is not read
            # $0 · no GPU · no ckpt: measures what the STREAM carries across a segment boundary,
            # never what a model can reach (that conflation is exactly what H_9304 could not split).
            "mi_win": 0, "mi_span": 0, "mi_estimator": "all", "mi_eps": 0.0, "mi_seg_lines": 0, "mi_robust": False,
            # H_9800 counterfactual-decl (ephemeral-declaration grounding):
            #   --stems-per-episode S   declared stems per episode (>=4, multiple of 4)
            #   --eval-episodes N       eval episodes PER STRATUM (5 strata)
            #   --held-out I,J          REINTERPRETED for this format ONLY: I = held-out (0-shot)
            #                           stem names, J = held-out operator names. Documented in the
            #                           format's own printout so the reinterpretation is never silent.
            "stems_per_episode": 4, "eval_episodes": 16,
            # H_9810 bindpanel: --bind-k = stacked contested edges per sentence (K). K=1 collapses
            # the field to rank 1 by construction, so the floor is 2 and the default is 6.
            "bind_k": 6,
            # H_9825 weavepanel: parametric ρ·weave panel (the n=12 instrument fix).
            #   --weave-families f1,f2   default = all five
            #   --weave-max N            0 = no cap
            "weave_families": "", "weave_max": 0,
            # H_9837 falsidrill: --falsi-ablate = the matched-surface structure-off arm
            "falsi_ablate": False,
            # H_9839 dreamgen: --dream-target = the dream node's COMPOSITION LAW (the DV) ·
            #   --dream-nights = the number of nights = mi-screen segments (a POWER knob only:
            #   it moves the pair count, never the block geometry, which is a frozen constant).
            #   --dream-anchors synthetic|real:<ckpt.clm> = where an anchor's COORDINATES come
            #   from. `synthetic` (default) = the builder's own uniform draw, byte-identical to
            #   before the flag existed. `real:` = the production trunk's pooled penultimate of
            #   the anchor's own entity string — the H_9838 planted-geometry swap.
            "dream_target": "midpoint", "dream_nights": 24, "dream_anchors": "synthetic",
            # H_9809 ngram-audit (--ngram-recoverable-audit · absorbs lab/v3 H_004's theorem
            # "oracle-fusable <=> n-gram-recoverable" as a production audit flag):
            #   --ngram-recoverable-audit  arm the audit (required by fmt `ngram-audit`)
            #   --audit-train F            the training stream the model actually saw
            #   --panel F                  the held-out eval panel under audit
            #   --codec F                  optional MORPH-2B-style codec.json -> adds a token-space
            #                              arm beside the always-present raw-utf8 byte arm
            #   --audit-marker A,B         class-discriminating markers -> per-arm terminal reach
            #   --audit-min-coverage X     below this key-coverage an order reads UNDECIDABLE,
            #                              never CLOSED (a 0-coverage lookup IS the majority class)
            # H_9812 --bind-legacy-lengths: rebuild the DISQUALIFIED length-coded panel as a
            # control (field-alone acc 1.0000). Default = length-matched, where the surface byte
            # length is identical whatever the gold is.
            # H_9842 wake-coresidency (is the wake working ring buffer a co-occurrence ceiling?):
            #   --wake-buffer-cap N    repeatable — the swept capacities (default 20,64,256; 20 = the
            #                          hardcoded core/wake_memory.py::_working_cap() the daemon runs)
            #   --replay-source S      working | episodic | both — `episodic` is the append-only
            #                          (uncapped) arm = the DIRECT refutation arm for a FIFO ceiling
            #   --wake-anchors K       anchors per frequency stratum; also the robustness knob
            #   --wake-ticks N         truncate the stream to N ticks (0 = whole file)
            #   --wake-eps X           a co-residency delta below this is not read
            # $0 · no GPU · no ckpt: recombination needs two concepts to CO-OCCUR, so a C-slot FIFO
            # bounds which pairs can ever be jointly resident. That is a STRUCTURAL fact of the
            # shipped buffer, measurable before anyone spends a training run on it.
            "wake_caps": [], "replay_source": "both", "wake_anchors": 24,
            "wake_ticks": 0, "wake_eps": 0.05,
            "bind_legacy_lengths": False, "bind_task": "xor",   # H_9815 xor | hp(positive control)
            "ngram_recoverable_audit": False, "audit_train": None, "panel": None,
            "codec": None, "audit_marker": None, "audit_min_coverage": 0.10}
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == "--out":
            opts["out"] = argv[i + 1]; i += 2
        elif a == "--held-out":
            p = argv[i + 1].split(","); opts["held_out"] = (int(p[0]), int(p[1])); i += 2
        elif a == "--held-out-frac":
            opts["held_out_frac"] = float(argv[i + 1]); i += 2
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
        elif a == "--carrier-only":
            opts["carrier_only"] = True; i += 1
        elif a == "--held-swap":
            opts["held_swap"] = True; i += 1
        elif a == "--decl-only":
            opts["decl_only"] = True; i += 1
        elif a == "--held-n":
            opts["held_n"] = int(argv[i + 1]); i += 2
        elif a == "--manifest":
            opts["manifest"] = argv[i + 1]; i += 2
        elif a == "--store":
            opts["store"] = argv[i + 1]; i += 2
        elif a == "--out-dir":
            opts["out_dir"] = argv[i + 1]; i += 2
        elif a == "--surface":
            opts["surface"] = argv[i + 1]; i += 2
        elif a == "--collision-split":
            opts["collision_split"] = True; i += 1
        elif a == "--bridge-split":
            opts["bridge_split"] = True; i += 1
        elif a == "--decl-ablate":
            opts["decl_ablate"] = True; i += 1
        elif a == "--max-atoms":
            opts["max_atoms"] = int(argv[i + 1]); i += 2
        elif a == "--polarity":
            opts["polarity"] = argv[i + 1]; i += 2
            if opts["polarity"] not in ("real", "assigned"):
                raise SystemExit("--polarity must be 'real' or 'assigned' (got %r)" % opts["polarity"])
        elif a == "--assign-seed":
            opts["assign_seed"] = int(argv[i + 1]); i += 2
        elif a == "--nonce-fillers":
            opts["nonce_fillers"] = int(argv[i + 1]); i += 2
        elif a == "--win":
            opts["win"] = int(argv[i + 1]); i += 2
        elif a == "--n-blocks":
            opts["n_blocks"] = int(argv[i + 1]); i += 2
        elif a == "--store-slots":
            opts["store_slots"] = int(argv[i + 1]); i += 2
        elif a == "--entity-pool":
            opts["entity_pool"] = argv[i + 1]; i += 2   # H_9683 storebind: external atom pool
        elif a == "--transcript":
            opts["transcript"] = argv[i + 1]; i += 2
        elif a == "--study-frac":
            opts["study_frac"] = float(argv[i + 1]); i += 2
        elif a == "--scramble-seed":
            opts["scramble_seed"] = int(argv[i + 1]); i += 2
        elif a == "--mi-win":
            opts["mi_win"] = int(argv[i + 1]); i += 2          # H_9844 mi-screen geometry
        elif a == "--mi-span":
            opts["mi_span"] = int(argv[i + 1]); i += 2
        elif a == "--mi-estimator":
            opts["mi_estimator"] = argv[i + 1]; i += 2         # gzip|ppm|markov6|all
        elif a == "--mi-eps":
            opts["mi_eps"] = float(argv[i + 1]); i += 2
        elif a == "--mi-seg-lines":
            opts["mi_seg_lines"] = int(argv[i + 1]); i += 2   # H_9844: line-record segmentation
        elif a == "--mi-robust":
            opts["mi_robust"] = True; i += 1                  # H_9844: geometry-robustness gate
        elif a == "--arm":
            opts["arm"] = argv[i + 1]; i += 2          # H_9694 g6bind: targeted|shuf
        elif a == "--stems-per-episode":
            opts["stems_per_episode"] = int(argv[i + 1]); i += 2   # H_9800 counterfactual-decl
        elif a == "--eval-episodes":
            opts["eval_episodes"] = int(argv[i + 1]); i += 2       # H_9800 counterfactual-decl
        elif a == "--bind-k":
            opts["bind_k"] = int(argv[i + 1]); i += 2               # H_9810 bindpanel conjuncts
        elif a == "--weave-families":
            opts["weave_families"] = argv[i + 1]; i += 2            # H_9825 weavepanel families
        elif a == "--weave-max":
            opts["weave_max"] = int(argv[i + 1]); i += 2            # H_9825 weavepanel cap
        elif a == "--falsi-ablate":
            opts["falsi_ablate"] = True; i += 1                     # H_9837 structure-off arm
        elif a == "--wake-buffer-cap":
            opts["wake_caps"].append(int(argv[i + 1])); i += 2       # H_9842 repeatable cap sweep
        elif a == "--replay-source":
            opts["replay_source"] = argv[i + 1]; i += 2              # working|episodic|both
            if opts["replay_source"] not in ("working", "episodic", "both"):
                raise SystemExit("--replay-source must be working|episodic|both (got %r)"
                                 % opts["replay_source"])
        elif a == "--wake-anchors":
            opts["wake_anchors"] = int(argv[i + 1]); i += 2          # H_9842 anchors per stratum
        elif a == "--wake-ticks":
            opts["wake_ticks"] = int(argv[i + 1]); i += 2            # H_9842 stream truncation
        elif a == "--wake-eps":
            opts["wake_eps"] = float(argv[i + 1]); i += 2            # H_9842 read threshold
        elif a == "--dream-target":
            opts["dream_target"] = argv[i + 1]; i += 2              # H_9839 dreamgen DV
            if opts["dream_target"] not in _DG_TARGETS:
                raise SystemExit("--dream-target must be one of %s (got %r)"
                                 % ("|".join(_DG_TARGETS), opts["dream_target"]))
        elif a == "--dream-nights":
            opts["dream_nights"] = int(argv[i + 1]); i += 2         # H_9839 power knob
        elif a == "--dream-anchors":
            opts["dream_anchors"] = argv[i + 1]; i += 2             # H_9839 real-anchor swap
            if opts["dream_anchors"] != "synthetic" and \
                    not opts["dream_anchors"].startswith("real:"):
                raise SystemExit("--dream-anchors must be 'synthetic' or 'real:<ckpt.clm>' "
                                 "(got %r)" % opts["dream_anchors"])
        elif a == "--ngram-recoverable-audit":
            opts["ngram_recoverable_audit"] = True; i += 1          # H_9809 ngram-audit
        elif a == "--bind-legacy-lengths":
            opts["bind_legacy_lengths"] = True; i += 1              # H_9812 disqualified control
        elif a == "--bind-task":
            opts["bind_task"] = argv[i + 1]; i += 2                 # H_9815 xor|hp · H_9818 xmark
        elif a == "--audit-train":
            opts["audit_train"] = argv[i + 1]; i += 2               # H_9809
        elif a == "--panel":
            opts["panel"] = argv[i + 1]; i += 2                     # H_9809
        elif a == "--codec":
            opts["codec"] = argv[i + 1]; i += 2                     # H_9809
        elif a == "--audit-marker":
            opts["audit_marker"] = argv[i + 1]; i += 2              # H_9809
        elif a == "--audit-min-coverage":
            opts["audit_min_coverage"] = float(argv[i + 1]); i += 2  # H_9809
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

        # ---- ground_hocarrier surfaces. Every one of these was MEASURED on the pretrained base
        # (P2 census, SEEN stems, where the operator is proven alive at 1.0000) — none was chosen
        # because it looked right. The census is what makes each role defensible:
        #
        #   certainly not {s}  acc 1.000  echo 0.000   RUNS   (0 occurrences in any corpus)
        #   just not {s}       acc 1.000  echo 0.000   RUNS   (0 occurrences)
        #   far from {s}       acc 0.700  echo 0.300   mixed  -> unusable, dropped
        #   not only {s}       acc 0.300  echo 0.750   mixed  -> unusable as a control, dropped
        #   oddly {s}          acc 0.350  echo 0.700   mostly silent
        #   notably {s}        acc 0.100  echo 0.900   SILENT
        #
        # `certainly not` firing at 1.000 while never appearing in training is the EN replication of
        # C1b: the ADVERB slot generalises freely. The stem slot does not (H_9346, echo 91-98%).
        # That asymmetry is the whole subject of this format.
        "ho_carrier": ("never {s}",),
        "ho_scored":  ("not {s}", "certainly not {s}"),
        "ho_null":    ("oddly {s}",),
        "ho_negctl":  ("notably {s}",),
    },
}
DEFAULT_LANG = "ko"        # every existing corpus/verdict is ko; changing this default moves them all

# ground_hocarrier arm sizes over the held-out pool (40 EN atoms: 12 + 12 + 16).
HOCARRIER_ARMS = (("hoc", 12), ("null", 12), ("decl", 16))
HOCARRIER_CARRIER_REPS = 3     # 1 carrier surface x3 == 3 declarative surfaces -> the `{s} => `
                               # suffix window is trained 50/50, so a suffix-only reader gets chance
                               # there and any DV signal has to come from the left context. See the
                               # build_hocarrier header for why that balance is the experiment.


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

# ---------------------------------------------------------------------------
# C5-REVERSE (`--carrier-only`) — the last empty cell of the C3/C4 2x2.
#
#   C3  wrote the inverted polarity through the DECLARATIVE key only -> read the OPERATOR: OLD (0/12).
#   C4  wrote it through BOTH keys                                   -> read the OPERATOR: NEW (12/12).
#   C5  writes it through the CARRIER (operator) key ONLY            -> read the DECLARATIVE surface.
#
# Two models survive C3+C4 and they disagree here, so this cell decides between them:
#
#   ONE STORE, MANY KEYS   the carrier write updates a SHARED value; every key that reads that stem
#                          reads the new value -> swap-arm flip0 (`{s}고 =>`) is pulled to the NEW
#                          polarity even though no declarative line was ever written. ("the carrier
#                          key is a master key" — an asymmetry worth its own campaign.)
#   TWO LANES, NO BRIDGE   the declarative store and the operator store hold SEPARATE entries and
#                          never share a value -> swap-arm flip0 keeps the OLD (pretrained) polarity
#                          while the SAME checkpoint's operator answers with the NEW one. Two
#                          contradictory polarities coexist in one model, addressed by surface class.
#                          That within-model DISSOCIATION is the signature, and it is the whole claim.
#
# What `--carrier-only` changes (the ONE variable): the swap and keep arms lose their DECLARATIVE
# arrow lines. Everything else is byte-identical to C4 — same --split-seed draw, so the swap stems
# are literally the same twelve stems C3 and C4 measured.
#
# What it deliberately does NOT drop: the HELD-OUT declarative arrows. They carry no information about
# any SEEN stem, and they are what keeps the declarative surface ALIVE through CPT. corpus-py-1 ⑥/(A)
# is the reason this is not a detail: a small CPT corpus DESTROYS the strata it omits, and the C5 DV
# lives on a stratum (SEEN-swap `{s}고`) the C5 corpus omits by construction. Without the held-out
# arrows the declarative readout could simply die, and a dead readout is INVALID, not a wall.
#
# Gates therefore (pre-registered on the card, all read BEFORE the DV):
#   G-LAND   swap-arm CARRIER readback (the taught surfaces) follows the planted value >= 11/12.
#            The write must have landed or there is nothing to ask about -> INVALID(budget).
#   G-ALIVE  keep + untouched arms' DECLARATIVE flip0 still answers the TRUE polarity (>= 5/6).
#            Both models predict this arm is unmoved, so a failure is the INSTRUMENT, not the wall:
#            either CPT destroyed the omitted declarative stratum (corpus-py-1 ⑥) or the carrier
#            write corrupts flip0 non-specifically (a lexical-cooccurrence artifact — note a keep-arm
#            carrier line pairs the stem with the OPPOSITE label word, so an echo account predicts
#            keep's flip0 drifts to the WRONG pole; the swap arm alone cannot detect that, because
#            there the carrier's label word coincides with the stem's OLD polarity).
#   FORGET   untouched = the stratum the corpus never touches at all. ADVISORY at 20-SEEN (n=3-5,
#            rule-of-three UCB ~ 100%): reported, never binding (C3 seed-11 died of a binding
#            underpowered gate).
# ---------------------------------------------------------------------------


def build_carrierswap(atoms_path, reps, replay, seed, split_seed, carrier_only=False,
                      held_swap=False, decl_only=False, held_n=None):
    """C4 — write the inverted polarity ALSO through the operator's own `지 않다` carrier, then ask
    whether the operator reads the new value on a DISJOINT scored surface (H-ε) or the old one (H-δ).

    Held IDENTICAL to C3 (build_seenswap): the declarative write, the split logic, the leak audit.
    The single added variable is the operator-key carrier on the swap arm. The arm draw is a function
    of --split-seed alone (redrawing after seeing a result would be selection contamination).

    carrier_only=True -> C5-REVERSE: the swap + keep arms are written through the CARRIER KEY ONLY
    (their declarative arrows are suppressed) and the DECLARATIVE surface becomes the DV. See the
    block comment above.
    """
    atoms = json.load(open(atoms_path))["atoms"]
    held = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "heldout"]
    seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]
    fixed = sum(n for _, n in CARRIERSWAP_FIXED)
    if len(seen) < fixed + 1:
        raise ValueError("carrierswap needs >= %d SEEN atoms (swap/affirm/keep + >=1 untouched), got %d"
                         % (fixed + 1, len(seen)))
    # H_9339 registered cells: HO-CARRIER = --held-swap · HO-DECL = --held-swap --decl-only.
    if held_swap and carrier_only:
        raise ValueError("--held-swap x --carrier-only is not a registered cell (HO arms are "
                         "HO-CARRIER = --held-swap, HO-DECL = --held-swap --decl-only)")
    if decl_only and not held_swap:
        raise ValueError("--decl-only without --held-swap is C3 (declarative-only) — use ground_seenswap")
    # --held-n N (H_9751): draw N held-out swap stems instead of the default 12 — isolates
    # co-train COMPOSITIONAL interference (H_9675 draw-fragility). Default None = 12 = byte-identical.
    n_swap = CARRIERSWAP_FIXED[0][1] if held_n is None else int(held_n)
    if held_swap and n_swap < 1:
        raise ValueError("carrierswap --held-n must be >= 1, got %d" % n_swap)
    if held_swap and len(held) < n_swap:
        raise ValueError("carrierswap --held-swap needs >= %d HELD-OUT atoms (swap arm, --held-n), got %d"
                         % (n_swap, len(held)))

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

    if held_swap:
        # HO mode (H_9339): the swap arm is redrawn from the HELD-OUT pool. The seen draw above ran
        # UNCHANGED first, so affirm/keep/untouched are stem-identical to C4 at the same --split-seed;
        # the 12 stems C4 wrote become `preserve` — written 0x here, the highest-power G-PRESERVE
        # stratum (C4 measured these exact stems flipping 12/12 when written). corpus-py-1 (A)/(F):
        # the generalisation axis is the STEM, so the DV lives on stems with ZERO CPT exposure.
        arms["preserve"] = arms.pop("swap")
        hpos = [x for x in held if x[1] == 1]
        hneg = [x for x in held if x[1] == 0]
        srng.shuffle(hpos)                             # same srng, AFTER the seen shuffles: the seen
        srng.shuffle(hneg)                             # draw stays byte-identical to C4
        picked, hpi, hni = [], 0, 0
        for k in range(n_swap):                        # n_swap (default 12), polarity-stratified like the seen draw
            src = hpos if (k % 2 == 0 and hpi < len(hpos)) or hni >= len(hneg) else hneg
            if src is hpos:
                picked.append(hpos[hpi]); hpi += 1
            else:
                picked.append(hneg[hni]); hni += 1
        arms["swap"] = picked

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

    ho_stems = {s for s, _ in arms["swap"]} if held_swap else frozenset()
    for _ in range(reps):
        for stem, pol in held:                        # held-out: unchanged (WRITE reproduction).
            if stem in ho_stems:                       # --held-swap: a swap stem's ONLY declarative
                continue                               # exposure is the swap arm's INVERTED arrow —
            arrow(stem, pol)                           # a true-pol line here would fight the plant.
                                                       # KEPT under --carrier-only: it is what holds
                                                       # the declarative surface alive through CPT.
    for _ in range(replay):
        for stem, pol in arms["swap"]:                # THE MANIPULATION — inverted
            if not carrier_only:
                arrow(stem, 1 - pol)                   # declarative key (identical to C3) — C5 drops it
            if not decl_only:
                carrier(stem, 1 - pol)                 # operator's OWN key (C4/C5) — HO-DECL drops it
        for stem, pol in arms["affirm"]:              # diagnostic: declarative at original polarity
            arrow(stem, pol)
        for stem, pol in arms["keep"]:                # holds the operator up on ORIGINAL polarity
            if not carrier_only:
                arrow(stem, pol)                       # C5: the twin arm is carrier-only, exactly like
            carrier(stem, pol)                         # swap — otherwise its arrow would mask a drift
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
    flip1_man, write_man = _swap_eval_manifest(arms)
    st = {"held": len(held), "lines": len(lines), "bytes": len(text.encode()),
          "carrier_only": bool(carrier_only),
          "held_swap": bool(held_swap), "decl_only": bool(decl_only),
          "arms": {k: [s for s, _ in v] for k, v in arms.items()},
          "untouched_n": len(arms["untouched"]),
          "measured_prompt_leaks": leaks,
          "flip1_manifest": flip1_man, "write_manifest": write_man}
    if held_swap:
        # NEW audit #1 (plant integrity) — a swap stem's TRUE-polarity declarative line would fight
        # the INVERTED plant. The held-loop exclusion above suppresses it; this VERIFIES it is gone
        # (corpus-py-1 ⑩: never assume a substring guard held — check it, builder-coded).
        st["ho_contradiction_leaks"] = []
        for stem, pol in arms["swap"]:
            for pat in GROUND_FORMS_FLIP0:
                line = GROUND_TMPL.format(surf=pat.format(s=stem),
                                          pol="긍정" if pol == 1 else "부정")
                if line in text:
                    st["ho_contradiction_leaks"].append(line.strip())
        # NEW audit #2 (corpus-py-1 ⑦: a readback gate that reads nothing back gates nothing) — every
        # G-WRITE probe must be IN the corpus. w0 declarative (both arms) + carriers (HO-CARRIER only).
        gate_rows = list(write_man["heldout"])
        if not decl_only:
            car_man = _carrier_readback_manifest(arms)
            st["carrier_manifest"] = car_man
            gate_rows += car_man["heldout"]
        st["ho_readback_present"] = sum(1 for it in gate_rows if it["seed"] in text)
        st["ho_readback_n"] = len(gate_rows)
    if carrier_only:
        heldR = _heldr_draw(held, split_seed)
        f0, car = _c5_eval_manifests(arms, heldR)
        st["flip0_manifest"], st["carrier_manifest"] = f0, car
        st["heldr"] = [s for s, _ in heldR]
        # C5's DV lives on the DECLARATIVE surface, which C4 never audited (there it was a taught
        # readback line, deliberately IN the corpus). Under --carrier-only it must be ABSENT for the
        # arms whose answer has to be inferred rather than recalled — audit it, or the DV is void.
        st["flip0_leaks"] = [it["seed"].strip() for it in f0["heldout"]
                             if it["b"].split("|")[0] in ("swap", "keep", "untouched")
                             and it["seed"] in text]
        # ...and the inverse audit: a READBACK gate whose prompt is NOT in the corpus gates nothing.
        st["readback_present"] = sum(
            1 for it in f0["heldout"] + car["heldout"]
            if it["b"].split("|")[0] in ("affirm", "heldR", "swapC", "keepC") and it["seed"] in text)
        st["readback_n"] = sum(1 for it in f0["heldout"] + car["heldout"]
                               if it["b"].split("|")[0] in ("affirm", "heldR", "swapC", "keepC"))
    return text, st


# The C5 flip0 (DV) surfaces are GROUND_FORMS_FLIP0 verbatim — the same three declarative forms the
# corpus writes for held-out stems, so the surface itself is one the model has read thousands of times
# (only never for a swap stem during CPT). Scoring a surface the model has never seen in ANY form
# would measure the surface, not the store.
_FLIP0_TAGS = (("w0", "{s}고"), ("w1", "정말 {s}고"), ("w2", "너무 {s}다"))
_CARRIER_TAGS = (("cT", "전혀 {s}지 않다"), ("cG", "그다지 {s}지 않다"), ("cK", "결코 {s}지 않다"))


def _heldr_draw(held, split_seed):
    """12 held-out stems, polarity-balanced, for the declarative READBACK (aliveness) gate.

    Their declarative lines ARE in the corpus by design — this gate asks whether the declarative
    read path still works AT ALL after a carrier-heavy CPT, which is the precondition for reading
    anything into the swap arm's answer.
    """
    r = random.Random(split_seed + 977)
    pos = [x for x in held if x[1] == 1]
    neg = [x for x in held if x[1] == 0]
    r.shuffle(pos)
    r.shuffle(neg)
    out = []
    for k in range(12):
        src = pos if (k % 2 == 0 and pos) or not neg else neg
        if src:
            out.append(src.pop())
    return out


def _c5_eval_manifests(arms, heldR):
    """(flip0_spec, carrier_spec) for C5-REVERSE — the DV and the landing gate.

    flip0 : DECLARATIVE surface `이 영화 {s}고 => ` (+2 twins). gold = the PLANTED value.
            swap arm      = THE DV. gold NEW; margin>0 => the carrier write reached the declarative
                            read (one shared store). margin<0 => the OLD, pretrained value survives
                            (two lanes) — which is also exactly what the pre-CPT base reads.
            keep/untouched= G-ALIVE. Both models predict the TRUE polarity here.
            affirm/heldR  = taught readback (their arrows ARE in the corpus): the declarative read
                            path is functional at all.
    carrier: the TAUGHT carrier surfaces on swap+keep = G-LAND. gold = flip(planted), i.e. the exact
            label the corpus line carries. A write that did not land makes the DV meaningless.
    """
    def _item(stem, arm, tag, surf, planted, flip):
        gold_b = (planted ^ 1) if flip else planted
        gw, cw = ("긍정" if gold_b else "부정"), ("부정" if gold_b else "긍정")
        seed = GROUND_TMPL.format(surf=surf.format(s=stem), pol="")[:-len(".\n")]
        return {"a": stem, "b": "%s|%s" % (arm, tag), "seed": seed,
                "stem": stem, "pol": planted, "flip": flip,
                "gold_word": gw, "gold": gw + ".\n", "counterfactual": cw + ".\n"}

    flip0, car = [], []
    for arm in ("swap", "keep", "affirm", "untouched"):
        for stem, pol in arms[arm]:
            planted = (1 - pol) if arm == "swap" else pol
            for tag, surf in _FLIP0_TAGS:
                flip0.append(_item(stem, arm, tag, surf, planted, 0))
    for stem, pol in heldR:                                  # taught readback (aliveness)
        flip0.append(_item(stem, "heldR", _FLIP0_TAGS[0][0], _FLIP0_TAGS[0][1], pol, 0))
    for arm, cname in (("swap", "swapC"), ("keep", "keepC")):
        for stem, pol in arms[arm]:
            planted = (1 - pol) if arm == "swap" else pol
            for tag, surf in _CARRIER_TAGS:
                car.append(_item(stem, cname, tag, surf, planted, 1))
    return ({"win": 64, "gen": 8, "heldout": flip0, "seen": []},
            {"win": 64, "gen": 8, "heldout": car, "seen": []})


# The eval manifest is a pure function of the arm draw + the scored surfaces — NOT of how the corpus
# was written — so it is shared by C3 (ground_seenswap) and C4 (ground_carrierswap): both score the
# same operator on the same disjoint surfaces. Emitting it from the SAME build that drew the arms is
# what guarantees the arm↔manifest split can never drift (the C3 fire hand-built this on the pod;
# wiring it here makes a passing result already reproducible · a_experiment_engine_native).
#   swap arm: CPT planted the INVERTED polarity (1-orig); every other arm keeps its original.
#   flip1 (negation surfaces negL/negZ/negJ): gold = word(planted XOR 1)  — operator NEGATES.
#   write (flip0 surface {s}고, tag w0): gold = word(planted)             — the declarative fact.
_SWAP_TAGS = (("negL", "{s}지 않다"), ("negZ", "별로 {s}지 않다"), ("negJ", "{s}지는 않다"))
_WRITE_TAG = ("w0", "{s}고")


def build_hocarrier(atoms_path, reps, replay, seed, split_seed, lang=DEFAULT_LANG):
    """ground_hocarrier — take H_9334's operator-key write to the stems the operator has never met.

    H_9346 established, on this base and in English, what the wall actually is. The fact LANDS
    (held-out flip0 = 1.0000). The operator is ALIVE (SEEN flip1 = 1.0000 on the very same `not X`
    surface). And on a held-out stem the model ECHOES the planted polarity and ignores `not`
    (91-98%, and the echo tracks the plant: flipping it in the LIE arm flipped the answer). So the
    operator does not FAIL to look the fact up — it never fires. It is gated on the stem.

    This format asks whether that gate can be OPENED by writing the fact in the operator's own key.

      arm hoc  (12)  declarative arrows (true polarity) + carrier `never {s} => flip(pol)`
      arm null (12)  declarative arrows + `oddly {s} => flip(pol)`  — same label exposure in a
                     non-declarative frame, NO operator key. If hoc moves and null moves too, the
                     mechanism is "odd context -> flipped label" spillover, not the operator.
      arm decl (16)  declarative only = the H_9346 reproduction. Must ECHO, or the arm is broken.

    Scored on surfaces the carrier never contains: `not {s}` and `certainly not {s}`.

    ⚠️ WHAT A PASS MEANS, AND WHAT IT DOES NOT (convergence corpus-py-1 (F)):
    The disjointness axis here is the ADVERB slot, and the P2 census measured that slot to
    generalise freely in English (`certainly not X` scores 1.000 on SEEN stems while occurring ZERO
    times in any corpus). So a PASS says: *the operator's trigger set is WRITABLE for a stem it had
    never met* — the wall is repairable by writing in the right key. It does NOT say the model can
    compose a declaratively-known fact with the operator; that is exactly what H_9346 measured and
    it is 🧱. Do not read adverb-slot generalisation as stem-slot generalisation. The stem here is
    DELIBERATELY taught inside an operator line — that is the manipulation, not a leak.

    🔬 AND IT ADJUDICATES H_9334 ITSELF. Korean cannot separate "the operator read the new value"
    from "the model continued a string it had seen", because the operator IS a suffix, so the carrier
    line contains the scored prompt's answer verbatim:

        KO carrier: 이 영화 전혀 [좋지 않다 => 긍정].
        KO scored :  이 영화      [좋지 않다 => ] ?      <- the answer is inside the carrier

    English inverts it. The carrier is `never {s}` and the scored prompt is `not {s}`; the string
    `not {s} => ` occurs nowhere. The longest suffix a pure n-gram reader can match is `{s} => `,
    and that window is owned by the DECLARATIVE arrows, which carry the OPPOSITE label. So:

        n-gram continuation  predicts the ECHO answer (the arrows' label)
        operator consultation predicts the CARRIER's label

    They predict OPPOSITE outcomes. A hoc pass therefore refutes the n-gram account outright; a hoc
    echo puts H_9334's Korean 12/12 back under suspicion as suffix continuation. Either way the
    Korean result gets adjudicated by a language that can hold the two apart.

    The 3:3 line balance (HOCARRIER_CARRIER_REPS) is load-bearing: it trains the `{s} => ` window
    with both labels equally, so a suffix-only reader scores CHANCE there and every point of DV
    signal has to come from the left context. Without it, the arrow label alone would drag the DV.
    """
    L = lang_pack(lang)
    for k in ("ho_carrier", "ho_scored", "ho_null", "ho_negctl"):
        if k not in L:
            raise ValueError(
                "ground_hocarrier: lang '%s' has no '%s' surfaces.\n"
                "  These are not translations — each one is a ROLE that was earned by measuring it on\n"
                "  the pretrained base (does the operator fire here, or not?). Transplanting a surface\n"
                "  set across a language would be asserting a fingerprint nobody took.\n"
                "  Run the census on '%s' first, then add the pack." % (lang, k, lang))
    TMPL = L["tmpl"]
    F0, POS, NEG = L["flip0"], L["pos"], L["neg"]
    CARRIER, NULLC = L["ho_carrier"], L["ho_null"]
    word = lambda p: POS if p == 1 else NEG

    atoms = json.load(open(atoms_path))["atoms"]
    held = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "heldout"]
    seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]
    assert_atoms_match_lang([st for st, _ in held + seen], lang)
    need = sum(n for _, n in HOCARRIER_ARMS)
    if len(held) < need:
        raise ValueError("ground_hocarrier needs >= %d held-out atoms, got %d" % (need, len(held)))

    # The arm draw is a function of --split-seed ALONE. Redrawing it after seeing a result would be
    # selection contamination, so it cannot depend on anything the run produces.
    srng = random.Random(split_seed)
    pos = [x for x in held if x[1] == 1]
    neg = [x for x in held if x[1] == 0]
    srng.shuffle(pos)
    srng.shuffle(neg)
    arms, pi, ni = {}, 0, 0
    for name, n in HOCARRIER_ARMS:                    # polarity-stratified: alternate pos/neg
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
        for pat in F0:
            lines.append(TMPL.format(surf=pat.format(s=stem), pol=word(pol)))

    def op_lines(stem, pol, pats):
        # A negation line teaches the negation OUTPUT: for a stem of polarity `pol`, `never {s}`
        # resolves to flip(pol). Repeated so carrier lines == declarative lines (see the header).
        for _ in range(HOCARRIER_CARRIER_REPS):
            for pat in pats:
                lines.append(TMPL.format(surf=pat.format(s=stem), pol=word(1 - pol)))

    for _ in range(reps):
        for stem, pol in arms["hoc"]:                 # THE MANIPULATION — the fact in the operator's key
            arrow(stem, pol)
            op_lines(stem, pol, CARRIER)
        for stem, pol in arms["null"]:                # covariate control — same exposure, no key
            arrow(stem, pol)
            op_lines(stem, pol, NULLC)
        for stem, pol in arms["decl"]:                # baseline — H_9346 reproduction
            arrow(stem, pol)

    for _ in range(replay):                           # hold the operator up on SEEN stems (ground_keep)
        for stem, pol in seen:
            for pat in F0:
                lines.append(TMPL.format(surf=pat.format(s=stem), pol=word(pol)))
            for pat in L["flip1"]:
                lines.append(TMPL.format(surf=pat.format(s=stem), pol=word(1 - pol)))

    rng.shuffle(lines)
    text = "".join(lines)

    # The audit the whole design rests on: a scored prompt must NEVER occur in the corpus. Anchored
    # on the full template (the trailing "=> " included) so a scored `not X => ` can never be matched
    # by a carrier `never X => `. It runs over EVERY held-out stem, not just the arm each belongs to
    # — a hoc-arm carrier that happened to also name a decl-arm stem would be a cross-arm leak.
    #
    # SEEN stems are deliberately EXCLUDED from this audit and that is not a hole: `not <seen>` lines
    # are the operator replay, without which 6000 steps of flip0 destroy the operator we are about to
    # test (corpus-py-1 ⑥: SEEN flip1 0.883 -> 0.333). Those stems are never scored — the manifest is
    # drawn from `held` alone — so their negated lines preserve, they do not leak (⑥(C)).
    stub = TMPL.format(surf="\x00", pol="\x00").split("\x00")
    leaks = []
    for pat in tuple(L["ho_scored"]) + tuple(L["ho_negctl"]):
        for stem, _ in held:
            probe = stub[0] + pat.format(s=stem) + stub[1]
            if probe in text:
                leaks.append(probe.strip())
    if leaks:
        raise ValueError("ground_hocarrier: %d scored prompt(s) occur in the corpus — the answer "
                         "would be taught, not asked: %s" % (len(leaks), leaks[:3]))

    # Suffix-window census. This is the number that decides whether a suffix-only reader could win,
    # so it is EMITTED, not assumed: for each hoc stem, how many lines end `<stem> => <label>` per
    # label? The 3:3 design says they must be equal.
    suffix = {}
    for stem, pol in arms["hoc"]:
        tail_p = stem + stub[1].split("{pol}")[0] + word(pol)
        tail_f = stem + stub[1].split("{pol}")[0] + word(1 - pol)
        suffix[stem] = {"declarative_label": text.count(tail_p), "operator_label": text.count(tail_f)}

    man = _hocarrier_manifest(arms, L)
    return text, {"held": len(held), "seen": len(seen), "lines": len(lines),
                  "bytes": len(text.encode()),
                  "arms": {k: [s for s, _ in v] for k, v in arms.items()},
                  "carrier_reps": HOCARRIER_CARRIER_REPS,
                  "measured_prompt_leaks": leaks,
                  "suffix_window_census": suffix,
                  "eval_manifest": man}


def _hocarrier_manifest(arms, L):
    """The eval manifest is emitted by the SAME build that drew the arms, so arm↔manifest can never
    drift (build_carrierswap earned this the hard way — C3's was hand-built on the pod).

      scored surfaces  gold = word(pol XOR 1)   — the operator NEGATES the planted fact
      negctl surface   gold = word(pol XOR 1)   — same gold, but the census says the operator is
                                                  SILENT here; a hoc arm that moves on THIS surface
                                                  is not the operator, it is label spillover
      write   surface  gold = word(pol)         — the declarative fact itself (the precondition)
    """
    TMPL, POS, NEG = L["tmpl"], L["pos"], L["neg"]
    word = lambda p: POS if p == 1 else NEG
    stub = TMPL.format(surf="\x00", pol="\x00").split("\x00")
    rows = []
    tags = ([("s%d" % i, p, 1) for i, p in enumerate(L["ho_scored"])] +
            [("nc%d" % i, p, 1) for i, p in enumerate(L["ho_negctl"])] +
            [("w0", L["flip0"][0], 0)])
    for arm, members in arms.items():
        for stem, pol in members:
            for tag, pat, flip in tags:
                gold = word(pol ^ flip)
                rows.append({"a": stem, "b": tag, "arm": arm, "pol": pol, "flip": flip,
                             "xor": pol ^ flip, "surf": pat.format(s=stem),
                             "seed": stub[0] + pat.format(s=stem) + stub[1].split("{pol}")[0],
                             "gold": gold + ".", "counterfactual": word(1 - (pol ^ flip)) + ".",
                             "gold_word": gold})
    return {"format": "nbind-eval-v1", "task": "ground_hocarrier — can the operator's trigger set "
            "be WRITTEN for a stem it never met? (arms hoc / null / decl)",
            "gen": 8, "win": 64, "seen": [], "heldout": rows}


def _swap_eval_manifest(arms):
    """(flip1_spec, write_spec) for `anima-py evaluate --xbind`, drawn from the SAME arms."""
    def _word(b):
        return "긍정" if b else "부정"

    def _item(stem, arm, tag, surf, planted, flip):
        gold_b = (planted ^ 1) if flip else planted        # flip1 negates, flip0 declares
        gw, cw = _word(gold_b), _word(gold_b ^ 1)
        seed = GROUND_TMPL.format(surf=surf.format(s=stem), pol="")[:-len(".\n")]  # up to "=> "
        return {"a": stem, "b": "%s|%s" % (arm, tag), "seed": seed,
                "stem": stem, "pol": planted, "flip": flip,
                "gold_word": gw, "gold": gw + ".\n", "counterfactual": cw + ".\n"}

    flip1, write = [], []
    for arm, pairs in arms.items():
        for stem, pol in pairs:
            planted = (1 - pol) if arm == "swap" else pol
            for tag, surf in _SWAP_TAGS:
                flip1.append(_item(stem, arm, tag, surf, planted, 1))
            if arm == "swap":                              # WRITE gate reads the swap arm only
                write.append(_item(stem, arm, _WRITE_TAG[0], _WRITE_TAG[1], planted, 0))
    return ({"win": 64, "gen": 8, "heldout": flip1, "seen": []},
            {"win": 64, "gen": 8, "heldout": write, "seen": []})


def _carrier_readback_manifest(arms):
    """G-WRITE for --held-swap (H_9339): readback of the TAUGHT operator-carrier surfaces.
    C4's G-WRITE ran on the declarative w0; the card's G-WRITE for HO is the *carrier* readback
    (>= 11/12). swapC (12, planted=1-pol) is the gate; keepC (3, planted=pol) is the sanity twin.
    gold = word(flip(planted)) — exactly the label the corpus carrier line carries: the writer
    emits `carrier(stem, planted)` -> label word(planted^1), so gold_word = word(planted^1)."""
    def _word(b):
        return "긍정" if b else "부정"
    rows = []
    for arm, cname in (("swap", "swapC"), ("keep", "keepC")):
        for stem, pol in arms[arm]:
            planted = (1 - pol) if arm == "swap" else pol
            gw, cw = _word(planted ^ 1), _word(planted)
            for tag, surf in _CARRIER_TAGS:
                seed = GROUND_TMPL.format(surf=surf.format(s=stem), pol="")[:-len(".\n")]
                rows.append({"a": stem, "b": "%s|%s" % (cname, tag), "seed": seed,
                             "stem": stem, "pol": planted, "flip": 1,
                             "gold_word": gw, "gold": gw + ".\n", "counterfactual": cw + ".\n"})
    return {"win": 64, "gen": 8, "heldout": rows, "seen": []}


# ---------------------------------------------------------------------------
# KEY-LADDER (V2 · H_9378) — `anima-py evaluate --xbind <m.json> --surface-set <name|path>`
#
# C4 (H_9334) scored the operator on exactly THREE surfaces and found a hard boundary inside them:
# `{s}지 않다` and `별로 {s}지 않다` read the CPT-written value 12/12, while `{s}지는 않다` sits at
# chance. That boundary is the only direct evidence we have about WHAT THE KEY IS — and three points
# cannot draw a line. This ladder makes the boundary itself the measurement: enumerate surfaces that
# vary ONE property at a time (tense · politeness · orthographic space · topic marker · and above all
# BOUND-suffix vs FREE-preposed negator) and score every one of them, unchanged, on two ckpt lanes:
#
#   BASE  (natem_c34_*)  — the PRETRAIN lane. A swap-arm stem's true polarity is still the original,
#                          so "correctly negates the ORIGINAL polarity" = the operator RUNS here.
#   C4    (swap_c4_*)    — the CPT-WRITTEN lane. "answers the negation of the PLANTED polarity" =
#                          the written value is reachable THROUGH this surface.
#
# The 2x2 is the whole experiment (and neither cell alone can say it):
#   base RUNS · c4 NEW   -> surface is inside BOTH lanes' key-class            (negL/negZ: the anchors)
#   base RUNS · c4 OLD   -> the operator fires but reads the PRETRAIN value    -> the CPT write did not
#                           reach this surface class = two disjoint stores, addressed by template class
#   base DEAD            -> not an operator surface at all; says nothing about the write (pedestal-like)
#
# ⚠️ The DV is the 2AFC margin sign (identical readout to H_9334), NOT the free-generation d_acc.
# ⚠️ a_korean_byte_budget: every rendered row must fit the model's byte window or the leading
#    `이 영화 ` bytes are silently right-truncated away and the row measures a DIFFERENT prompt.
#    expand_surface_ladder REFUSES on overflow rather than shipping a truncated probe.
#
# Roles are PRE-REGISTERED in the table, not assigned after looking:
#   anchor_new  negL·negZ — H_9334 measured 12/12 NEW on the C4 lane. If they do not reproduce, the
#               instrument (not the wall) is broken -> INVALID.
#   anchor_null negJ      — H_9334 measured chance. If it turns positive, the instrument manufactures
#               signal -> INVALID.
#   pedestal    ped1·ped2 — a NON-negator particle in the negator slot (one bound-shaped, one
#               free-shaped, matched to the two morphological classes). True value = chance
#               (phi-estimator-needs-zero-truth-pedestal). The base lane must NOT "negate" here.
#   write       w0        — the declarative surface. The C4 lane must score >=11/12 on the planted
#               polarity or the fact never landed -> INVALID(budget), exactly H_9334's G-write.
#   ladder      the rest  — the actual unknowns.
#
# negAN / negANG are the point of the whole exercise: `안` is a FREE, PRE-POSED negator — the Korean
# structural twin of English `not`, inside the SAME language, the SAME base model and the SAME corpus,
# so it carries none of the 3-way confound (morphology x base x carrier) that made the EN arm (H_9346)
# a SCREENER. `안 {s}고` is verbatim one of the pretraining flip1 forms (GROUND_FORMS_FLIP1), so the
# base lane MUST run it — that makes it a positive control for the free class, not a hope.
_LADDER_TMPL = GROUND_TMPL

SURFACE_LADDERS = {
    "keyladder_v1": {
        "name": "keyladder_v1",
        "tmpl": _LADDER_TMPL,
        "surfaces": [
            # tag       surface                 flip  class    role
            ("negL",   "{s}지 않다",       1, "bound", "anchor_new"),   # H_9334: C4 12/12 NEW
            ("negZ",   "별로 {s}지 않다",  1, "bound", "anchor_new"),   # H_9334: C4 12/12 NEW
            ("negJ",   "{s}지는 않다",     1, "bound", "anchor_null"),  # H_9334: chance
            ("negPST", "{s}지 않았다",     1, "bound", "ladder"),       # + past
            ("negPRS", "{s}지 않는다",     1, "bound", "ladder"),       # + present-declarative
            ("negCAS", "{s}지 않아",       1, "bound", "ladder"),       # + casual
            ("negTGT", "{s}지않다",        1, "bound", "ladder"),       # - the space (orthography)
            ("negPOL", "{s}지 않습니다",   1, "bound", "ladder"),       # + honorific
            ("negAN",  "안 {s}다",         1, "free",  "ladder"),       # ★ FREE preposed = EN `not`
            ("negANG", "안 {s}고",         1, "free",  "ladder"),       # ★ FREE, pretrain-VERBATIM
            ("negMOT", "못 {s}다",         1, "free",  "ladder"),       # FREE preposed (inability)
            ("ped1",   "{s}지 뫄다",       1, "bound", "pedestal"),     # nonsense in the bound slot
            ("ped2",   "뫄 {s}다",         1, "free",  "pedestal"),     # nonsense in the free slot
            ("w0",     "{s}고",            0, "decl",  "write"),        # the declarative WRITE gate
        ],
    },
    # keyladder_v2 (H_9382) — V2-CLEAN re-run of H_9378. IDENTICAL to keyladder_v1 except the
    # bound-slot pedestal ped1 is swapped from `{s}지 뫄다` to `{s}뫄 뙤다`. H_9378 landed ⛔ INVALID
    # because ped1 (`{s}지 뫄다`) reused the operator's OWN first morpheme `지` (`지 않다` = -지+않-+-다),
    # so the pedestal contained the mediating covariate and ceiling'd (s7 12/12, s11 11/12) — the DV
    # could not separate a true `않다` read from `지`-fragment priming (control-must-match-mediating-
    # covariate). ped2-new `{s}뫄 뙤다` fully matches negL `{s}지 않다`'s byte template
    # ([stem][3B][SP][3B][다]) with ZERO length confound, using nonsense syllables 뫄 (EB AB 84,
    # connective slot) + 뙤 (EB 99 A4, auxiliary slot) — both OUTSIDE the negation-morpheme leading-2
    # byte range (fuzzy-match range = the V2/V3 finding) and with NO `지`. Every other surface + every
    # bar is byte-identical to keyladder_v1 (sha256-anchored in the H_9382 card). ONE-STRIKE (Fable):
    # if this `지`-free pedestal ALSO ceilings on the base lane, that is the DISCOVERY that base reads
    # ANY anomalous BOUND suffix as negated (BOUND-slot default-negated bias, since ped2 proved the
    # FREE slot is clean) → suffix-axis pedestal instrument closes terminal, no re-design.
    "keyladder_v2": {
        "name": "keyladder_v2",
        "tmpl": _LADDER_TMPL,
        "surfaces": [
            # tag       surface                 flip  class    role
            ("negL",   "{s}지 않다",       1, "bound", "anchor_new"),   # H_9334: C4 12/12 NEW
            ("negZ",   "별로 {s}지 않다",  1, "bound", "anchor_new"),   # H_9334: C4 12/12 NEW
            ("negJ",   "{s}지는 않다",     1, "bound", "anchor_null"),  # H_9334: chance
            ("negPST", "{s}지 않았다",     1, "bound", "ladder"),       # + past
            ("negPRS", "{s}지 않는다",     1, "bound", "ladder"),       # + present-declarative
            ("negCAS", "{s}지 않아",       1, "bound", "ladder"),       # + casual
            ("negTGT", "{s}지않다",        1, "bound", "ladder"),       # - the space (orthography)
            ("negPOL", "{s}지 않습니다",   1, "bound", "ladder"),       # + honorific
            ("negAN",  "안 {s}다",         1, "free",  "ladder"),       # ★ FREE preposed = EN `not`
            ("negANG", "안 {s}고",         1, "free",  "ladder"),       # ★ FREE, pretrain-VERBATIM
            ("negMOT", "못 {s}다",         1, "free",  "ladder"),       # FREE preposed (inability)
            ("ped1",   "{s}뫄 뙤다",       1, "bound", "pedestal"),     # ★ 지-FREE nonsense, bound slot
            ("ped2",   "뫄 {s}다",         1, "free",  "pedestal"),     # nonsense in the free slot
            ("w0",     "{s}고",            0, "decl",  "write"),        # the declarative WRITE gate
        ],
    },
}


def load_surface_set(name_or_path):
    """A built-in ladder name, or a path to a JSON ladder. Validated on the way in — a malformed
    ladder must die at load, not silently score a surface nobody registered."""
    if name_or_path in SURFACE_LADDERS:
        lad = SURFACE_LADDERS[name_or_path]
        surfaces = [{"tag": t, "surf": s, "flip": f, "class": c, "role": r}
                    for (t, s, f, c, r) in lad["surfaces"]]
        return {"name": lad["name"], "tmpl": lad["tmpl"], "surfaces": surfaces}
    lad = json.load(open(name_or_path))
    if not lad.get("surfaces"):
        raise SystemExit("anima-py evaluate --surface-set: '%s' is neither a built-in ladder (%s) "
                         "nor a JSON file with a non-empty 'surfaces' list."
                         % (name_or_path, "|".join(sorted(SURFACE_LADDERS))))
    out = []
    for s in lad["surfaces"]:
        for k in ("tag", "surf", "flip"):
            if k not in s:
                raise SystemExit("anima-py evaluate --surface-set: surface %r is missing '%s'." % (s, k))
        if "{s}" not in s["surf"]:
            raise SystemExit("anima-py evaluate --surface-set: surface '%s' has no {s} stem slot."
                             % s["tag"])
        out.append({"tag": s["tag"], "surf": s["surf"], "flip": int(s["flip"]),
                    "class": s.get("class", "?"), "role": s.get("role", "ladder")})
    return {"name": lad.get("name", os.path.basename(name_or_path)),
            "tmpl": lad.get("tmpl", _LADDER_TMPL), "surfaces": out}


def expand_surface_ladder(spec, ladder, win=None):
    """Re-render an `--xbind` manifest as (stem x arm) x LADDER-SURFACE.

    The arms and their PLANTED polarities are read back out of the manifest — they are the frozen
    property of the CPT that already ran, and re-deriving them from the atom file would let the arm
    draw drift away from the checkpoint it is scoring. Nothing about the corpus is re-computed here;
    only the scored surface changes, which is exactly the one variable this experiment moves.

    Returns (new_spec, audit). Raises on a byte-window overflow (a_korean_byte_budget)."""
    T = int(win or spec.get("win", 64))
    stems, order = {}, []
    for it in list(spec.get("heldout", [])) + list(spec.get("seen", [])):
        arm = str(it["b"]).split("|")[0]
        key = (arm, it["a"])
        if key not in stems:
            stems[key] = int(it["pol"])          # PLANTED polarity (swap arm = inverted by the CPT)
            order.append(key)

    def _word(b):
        return "긍정" if b else "부정"

    rows, over = [], []
    for arm, stem in order:
        planted = stems[(arm, stem)]
        for s in ladder["surfaces"]:
            gold_b = planted ^ s["flip"]
            gw, cw = _word(gold_b), _word(gold_b ^ 1)
            seed = ladder["tmpl"].format(surf=s["surf"].format(s=stem), pol="")[:-len(".\n")]
            need = len((seed + gw + ".\n").encode())
            if need > T:
                over.append((arm, stem, s["tag"], need))
            rows.append({"a": stem, "b": "%s|%s" % (arm, s["tag"]), "seed": seed,
                         "stem": stem, "pol": planted, "flip": s["flip"],
                         "surf_tag": s["tag"], "surf_class": s["class"], "surf_role": s["role"],
                         "gold_word": gw, "gold": gw + ".\n", "counterfactual": cw + ".\n"})
    if over:
        # The window is right-aligned (core/decode.py::_seed_to_tok), so an overflowing row does not
        # error — it quietly drops the LEADING bytes (`이 영화 `) and scores a prompt that is not the
        # one on the card. That is the exact failure mode a_korean_byte_budget was written for.
        raise SystemExit(
            "anima-py evaluate --surface-set: %d row(s) exceed the %d-byte window — the leading bytes "
            "would be silently truncated away and the row would measure a DIFFERENT prompt.\n"
            "  worst: %s\n  Fix: --win >= %d (and re-register: a wider window is a different probe)."
            % (len(over), T, ", ".join("%s/%s/%s=%dB" % o for o in over[:4]),
               max(o[3] for o in over)))

    arms = sorted({a for a, _ in order})
    audit = {"surface_set": ladder["name"], "n_surfaces": len(ladder["surfaces"]),
             "n_stems": len(order), "n_rows": len(rows), "arms": arms, "win": T,
             "arm_n": {a: sum(1 for x, _ in order if x == a) for a in arms},
             "max_row_bytes": max(len((r["seed"] + r["gold"]).encode()) for r in rows),
             "tags": [s["tag"] for s in ladder["surfaces"]]}
    return ({"win": T, "gen": int(spec.get("gen", 8)), "heldout": rows, "seen": [],
             "surface_set": ladder["name"]}, audit)


# ---------------------------------------------------------------------------
# c34 — the PRETRAINING corpus: natural text + arrow lines. The EN twin of the Korean C34.
#
# Every number below is MIRRORED from a census of the real ko C34, not invented (the file is
# deterministic, so it can be recounted at any time — see H_9333):
#
#   ko C34 (160,086 B · 2,459 lines)
#     arrow lines      960   of which 480 (exactly half) are NEGATED, all on SEEN stems
#     held-out stems   appear in an arrow line ZERO times          <- the whole held-out design
#     natural lines   1,499
#     held-out natural exposure  1,414 hits / 29 stems = 48.8 per stem  (min 42, max 86)
#     natural line bytes         median 42, p90 197, max 379
#
# The mediating covariate is "how much the model READ this stem with no polarity attached", and it
# is matched by COUNT (control-must-match-mediating-covariate), with bytes reported rather than
# forced — Korean is 3 B/char, so byte-matching would silently change the number of sentences.
#
# INVARIANTS, each checkable with one grep (the builder runs them itself and refuses to emit on a
# violation — a corpus that quietly breaks its own premise is how this lane keeps dying):
#   I1  a held-out stem never appears in an arrow line
#   I2  a held-out stem never appears in a NEGATED context anywhere in the training bytes
#       (the operator surfaces AND the derivational negations un-/in-/im-/dis-/non-/-less, because
#        `불편하` taught the KO model a negation it was never supposed to see — H_9333)
#   I3  every held-out stem reaches the natural-exposure floor; if it cannot, the build FAILS rather
#       than shipping a stem the model barely read
# ---------------------------------------------------------------------------
C34_ARROW_LINES = 960          # ko census
C34_NEG_FRACTION = 0.5         # ko census: 480/960
C34_NAT_PER_HELD = 48          # ko census: 48.8 per held-out stem
C34_NAT_FLOOR = 40             # below this the stem is not usable
C34_LINE_BYTES_MAX = 379       # ko census max natural line
C34_LINE_BYTES_P90 = 197

NEG_CTX = re.compile(
    r"\b(?:not|never|no|n't|cannot|hardly|barely|scarcely|without|lacks?|lacking)\W+(?:\w+\W+)?%s\b",
    re.I)
DERIV_NEG = re.compile(r"\b(?:un|in|im|dis|non|ir|il)%s\b|\b%ss?less\b", re.I)


def _neg_free(sent, stem):
    """True when `stem` appears in `sent` with no negation attached to it.

    A single held-out sentence carrying `not fast` teaches the model exactly the thing the flip1
    test is supposed to ask it to COMPOSE — and one leaked sentence is enough to make the verdict
    unreadable. So the filter is deliberately wide (an intervening token is allowed) and it also
    catches derivational negation, which is how the Korean set leaked (`불편하` = un-comfortable).
    """
    if re.search(NEG_CTX.pattern % re.escape(stem), sent, re.I):
        return False
    if re.search(DERIV_NEG.pattern % (re.escape(stem), re.escape(stem)), sent, re.I):
        return False
    return True


# ---------------------------------------------------------------------------
# atoms --collision-split (V3 STEM-COLLISION · H_9354) — is the stem side of the operator's
# address a BYTE FORM or a REPRESENTATION?
#
# The two-lane model (Fable's reframe of C3/C4/H_9327/H_9346) says the operator addresses a fact by
# (stem identity) x (surface-template class). C4 showed the template class is discrete. This asks
# the same question of the OTHER factor: if the stem key were byte-fuzzy — a conv net's local
# n-gram features — then a stem that merely LOOKS like a SEEN stem should partially hit its
# address, and the flip1 answer should BLEED toward the SEEN neighbour's polarity. If the key is
# discrete/representational, a near-miss is a total miss: no bleed at any partial overlap, and the
# address only resolves on the exact stem.
#
# THE NATURAL SPLIT IS DEGENERATE — and the builder says so instead of quietly emitting it.
# The brief for this lane assumed held-out stems that share a long byte prefix with a SEEN stem
# (`재밋` vs `재밌었`, `좋` vs `좋아하`). They do not exist in gt_atoms.json, and that is not bad
# luck: build_atoms() has a G-SUBSTR gate that FORBIDS a stem nesting in another, so the atom set
# was CONSTRUCTED to have no stem-stem collision. Measured on the frozen file: max byte-LCP between
# any held-out and any SEEN stem = 2 bytes — less than one Hangul syllable (3 B) — i.e. nothing but
# the shared UTF-8 high bytes every Hangul character has. Every stratum that could carry the signal
# has n = 0. A Jonckheere trend test over empty strata is not a negative result, it is no result
# (power-before-negative-verdict), so the natural census is emitted as a GATE, never as a verdict.
#
# So the collision has to be CONSTRUCTED, and the same flag builds the instrument that does it:
# a PREFIX-GRADED NONCE LADDER. For each 3-syllable SEEN donor d (polarity p) and each k in
# 0..3, a nonce stem
#
#     nonce(d, k, f) = d[:k] + filler(d, f)[k:]              (always 3 syllables = 9 bytes)
#
# shares exactly the first k syllables (3k BYTES — a_korean_byte_budget: the stratifier is bytes)
# with the donor and is otherwise unrelated filler. k = 0 is a length-matched unrelated stem (the
# AUDIT-A neutral-substitution control); k = 3 IS the donor (the positive control — the operator is
# known alive there, SEEN flip1 0.98-1.00); k = 1, 2 are the graded near-misses that the trend test
# reads. The nonce is scored at flip1 with gold = the DONOR-implied negated word, so the DV is
# literally "did the operator answer as if it had resolved the donor's address".
#
# What makes it bias-free, by construction rather than by hope:
#   - the 12 three-syllable SEEN donors are 6 positive / 6 negative, so a constant response bias
#     (the model just likes saying 긍정) enters the +p and -p items with opposite sign and cancels
#     in the stratum mean. Reported split by polarity anyway (polarity-split-before-headline).
#   - at every k the nonce is 3 syllables / 9 bytes: length is matched across the whole ladder, so
#     no stratum is confounded with sequence length (the failure AUDIT-A was built to avoid).
#   - k=1 keeps only donors whose 1-syllable prefix is UNIQUE among SEEN stems. `유` prefixes both
#     유쾌하(+) and 유치하(-); a nonce built on it is addressed by two donors of OPPOSITE polarity,
#     which drags the DV toward zero and would MANUFACTURE the null this test is trying to falsify.
#     5 of the 12 donors are ambiguous at k=1 and are dropped from that stratum only.
#   - the trend test runs on k in {0,1,2} ONLY. k=3 is an exact address, not a partial one; folding
#     it in would produce a "trend" from the positive control alone.
# ---------------------------------------------------------------------------
COLLISION_DONOR_CHARS = 3          # the graded ladder needs one uniform stem length
COLLISION_SURFACES = (("negL", "{s}지 않다", 1),      # operator-live (C1b census, both seeds)
                      ("negZ", "별로 {s}지 않다", 1),  # operator-live
                      ("negJ", "{s}지는 않다", 0))     # NO-operator control surface (p ~ .50 in C4)
# Hangul syllables that occur in NO stem of either split. Asserted disjoint at build time — a
# filler that shares a syllable with a real stem would smuggle the very collision we are measuring.
COLLISION_FILLER_POOL = "갸겨괴놔뇨댸됴랴려뮤벼뾰샤셔쇼쥬챠캬탸텨퍄펴햐효뀨뎨뷰쒜쨔"


def _lcp_bytes(x, y):
    bx, by = x.encode(), y.encode()
    n = 0
    for i in range(min(len(bx), len(by))):
        if bx[i] != by[i]:
            break
        n += 1
    return n


def build_collision_split(atoms_path, fillers, seed, win=64):
    """(census, manifest) for `anima-py evaluate --xbind` — the V3 STEM-COLLISION ladder.

    census   = the NATURAL held-out x SEEN byte-LCP stratification (the power GATE: it is what
               tells you the briefed design has n=0 in every signal stratum).
    manifest = the CONSTRUCTED prefix-graded nonce ladder (the instrument that has power).
    """
    atoms = json.load(open(atoms_path, encoding="utf-8"))["atoms"]
    seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]
    held = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "heldout"]
    assert_atoms_match_lang([s for s, _ in seen + held], "ko")
    allstems = {s for s, _ in seen + held}

    # --- the GATE: natural byte-LCP census -----------------------------------------------------
    nat = []
    for h, ph in held:
        best, bl = None, -1
        for s, ps in seen:
            L = _lcp_bytes(h, s)
            if L > bl:
                best, bl = (s, ps), L
        nat.append({"held": h, "pol": ph, "nearest_seen": best[0], "nearest_pol": best[1],
                    "lcp_bytes": bl, "lcp_chars": bl // 3})
    strata = {}
    for r in nat:
        strata.setdefault(r["lcp_bytes"], []).append(r["held"])
    signal_n = sum(len(v) for k, v in strata.items() if k >= 3)   # >= 1 shared syllable
    census = {"n_seen": len(seen), "n_heldout": len(held),
              "lcp_byte_hist": {str(k): len(v) for k, v in sorted(strata.items())},
              "max_lcp_bytes": max(r["lcp_bytes"] for r in nat),
              "signal_stratum_n": signal_n,
              "degenerate": signal_n == 0, "rows": nat}

    # --- the INSTRUMENT: prefix-graded nonce ladder ---------------------------------------------
    stem_chars = set("".join(allstems))
    pool = [c for c in COLLISION_FILLER_POOL if c not in stem_chars]
    if len(pool) != len(COLLISION_FILLER_POOL):
        raise SystemExit("collision-split: filler pool overlaps a real stem syllable — refuse")

    donors = [(s, p) for s, p in seen if len(s) == COLLISION_DONOR_CHARS]
    npos = sum(p for _, p in donors)
    if npos * 2 != len(donors):
        raise SystemExit("collision-split: donors are %d pos / %d neg — an UNBALANCED donor set "
                         "cannot cancel a response bias, and the stratum mean would then measure "
                         "the bias. Refusing to emit." % (npos, len(donors) - npos))

    def uniq_at(d, k):
        pre = d[:k]
        return not any(o != d and o.startswith(pre) for o, _ in seen)

    rng = random.Random(seed)
    fill = {}
    for d, _ in donors:
        for f in range(fillers):
            while True:
                cand = "".join(rng.choice(pool) for _ in range(COLLISION_DONOR_CHARS))
                if cand not in fill.get(d, []):
                    fill.setdefault(d, []).append(cand)
                    break

    def word(b):
        return "긍정" if b else "부정"

    def item(nonce, donor, dpol, k, tag, surf, flip, f):
        # flip1 gold = the operator NEGATES the donor-implied polarity; flip is 1 on every
        # operator-live surface (the ladder never scores a flip0 declaration — the fact is not
        # written for a nonce, so only the OPERATOR's behaviour is interpretable).
        gold_b = dpol ^ 1
        s_seed = GROUND_TMPL.format(surf=surf.format(s=nonce), pol="")[:-len(".\n")]
        gold, cf = word(gold_b) + ".\n", word(gold_b ^ 1) + ".\n"
        nb = len(s_seed.encode()) + len(gold.encode())
        if nb > win:                                     # a_korean_byte_budget: ko = 3 B/char
            raise SystemExit("collision-split: item %r needs %d B but --win is %d — the leading "
                             "bytes would be silently cut and the run would read as a negative."
                             % (s_seed, nb, win))
        return {"a": nonce, "b": "%s|%s|%s|%d|f%s" % (k, tag, donor, dpol, f),
                "seed": s_seed, "stem": nonce, "pol": dpol, "flip": flip,
                "gold_word": word(gold_b), "gold": gold, "counterfactual": cf}

    rows, dropped = [], []
    for d, p in donors:
        for k in range(COLLISION_DONOR_CHARS + 1):
            if k == 1 and not uniq_at(d, 1):
                dropped.append((d, 1))                   # ambiguous prefix -> null-manufacturing
                continue
            reals = [None] if k == COLLISION_DONOR_CHARS else list(range(fillers))
            for f in reals:
                nonce = d if f is None else d[:k] + fill[d][f][k:]
                if f is not None:
                    if nonce in allstems:
                        raise SystemExit("collision-split: nonce %r IS a real stem" % nonce)
                    if any(st in nonce for st in allstems):
                        raise SystemExit("collision-split: nonce %r contains a real stem" % nonce)
                    if len(nonce.encode()) != len(d.encode()):
                        raise SystemExit("collision-split: nonce %r is not length-matched" % nonce)
                for tag, surf, flip in COLLISION_SURFACES:
                    rows.append(item(nonce, d, p, "k%d" % k, tag, surf, 1,
                                     "-" if f is None else f))

    # anchor: the natural held-out stems at the same surfaces = a re-measurement of H_9327's
    # flip1 (0.46-0.56 = chance). If this anchor does not reproduce, the ckpt/instrument moved.
    for h, ph in held:
        for tag, surf, flip in COLLISION_SURFACES:
            rows.append(item(h, h, ph, "nat", tag, surf, 1, "-"))

    per = {}
    for r in rows:
        per[r["b"].split("|")[0]] = per.get(r["b"].split("|")[0], 0) + 1
    census["design"] = {
        "donors": [(d, p) for d, p in donors], "donor_pos": npos, "donor_neg": len(donors) - npos,
        "fillers": fillers, "k1_dropped_ambiguous": dropped,
        "rows_per_stratum": per, "n_rows": len(rows), "surfaces": [t for t, _, _ in COLLISION_SURFACES],
        "n_decode_required": len(rows)}
    return census, {"win": win, "gen": 8, "heldout": rows, "seen": []}


def build_c34(atoms_path, corpus_paths, lang, seed):
    """Assemble the pretraining corpus: natural sentences + arrow lines (SEEN stems only)."""
    L = lang_pack(lang)
    rng = random.Random(seed)
    atoms = json.load(open(atoms_path, encoding="utf-8"))["atoms"]
    held = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "heldout"]
    seen = [(a["stem"], int(a["pol"])) for a in atoms if a["split"] == "train"]
    assert_atoms_match_lang([st for st, _ in held + seen], lang)

    sents = []
    for cp in corpus_paths:
        with open(cp, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                for sent in re.split(r"(?<=[.!?])\s+", line.strip()):
                    b = len(sent.encode())
                    if 20 <= b <= C34_LINE_BYTES_MAX:
                        sents.append(sent)
    rng.shuffle(sents)

    # natural exposure — mirrored per-stem count, negation-free by I2
    nat, per, dropped = [], {}, 0
    for stem, _ in held + seen:
        want = C34_NAT_PER_HELD
        got = []
        pat = re.compile(r"\b%s\b" % re.escape(stem), re.I)
        for sent in sents:
            if len(got) >= want:
                break
            if pat.search(sent):
                # neg-free for EVERY held-out stem, not just the one this sentence was chosen for.
                # Measured (the I2 gate caught it): a sentence picked for `friendly` also carried
                # `not effective`, and `effective` is held out too. Filtering per-chosen-stem leaks
                # the operator onto a DIFFERENT held-out stem — and one leaked sentence is enough to
                # turn the flip1 answer from composed into taught.
                if all(_neg_free(sent, h) for h, _ in held):
                    got.append(sent)
                else:
                    dropped += 1
        per[stem] = len(got)
        nat.extend(got)
    thin = [(st, n) for st, n in per.items() if n < C34_NAT_FLOOR]
    if thin:
        raise SystemExit(
            "anima corpus c34: I3 FAIL — %d stem(s) could not reach the natural-exposure floor "
            "(%d clean sentences): %s\n"
            "  Shipping a stem the model barely read would make its chance-level score meaningless. "
            "Raise the corpus, lower --n-held, or drop these stems from the atom set."
            % (len(thin), C34_NAT_FLOOR, ", ".join("%s=%d" % t for t in thin[:8])))

    # arrow lines — SEEN stems ONLY, half negated (ko census)
    arrow = []
    n_neg = int(C34_ARROW_LINES * C34_NEG_FRACTION)
    per_stem = C34_ARROW_LINES // len(seen)
    for stem, pol in seen:
        for k in range(per_stem):
            neg = k < per_stem * C34_NEG_FRACTION
            forms = L["flip1"] if neg else L["flip0"]
            surf = forms[k % len(forms)].format(s=stem)
            gold = (L["neg"] if pol == 1 else L["pos"]) if neg else (L["pos"] if pol == 1 else L["neg"])
            arrow.append(L["tmpl"].format(surf=surf, pol=gold).rstrip("\n"))

    lines = nat + arrow
    rng.shuffle(lines)
    text = "\n".join(lines) + "\n"

    # I1 / I2 — the builder checks its own premise and refuses to emit on a violation
    v1 = [st for st, _ in held for a in arrow if re.search(r"\b%s\b" % re.escape(st), a, re.I)]
    if v1:
        raise SystemExit("anima corpus c34: I1 FAIL — held-out stem(s) in an arrow line: %s"
                         % ", ".join(sorted(set(v1))[:6]))
    v2 = [st for st, _ in held for l in lines if re.search(r"\b%s\b" % re.escape(st), l, re.I)
          and not _neg_free(l, st)]
    if v2:
        raise SystemExit("anima corpus c34: I2 FAIL — held-out stem(s) in a NEGATED context: %s"
                         % ", ".join(sorted(set(v2))[:6]))

    st = {"lang": lang, "lines": len(lines), "bytes": len(text.encode()),
          "arrow": len(arrow), "arrow_negated": n_neg, "natural": len(nat),
          "held_nat_per_stem": round(sum(per[s] for s, _ in held) / len(held), 1),
          "held_nat_min": min(per[s] for s, _ in held),
          "seen_nat_per_stem": round(sum(per[s] for s, _ in seen) / len(seen), 1),
          "neg_sentences_dropped": dropped,
          "I1_held_in_arrow": 0, "I2_held_in_negated": 0, "I3_floor": C34_NAT_FLOOR}
    return text, st


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


# --------------------------------------------------------------------------- #
# storebind — the co-trained store-lookup bridge task (H_9423 · S0 wiring).
#
# A parent-corpus port of lab/v2/gen.py, the toy that DIRECTIONAL-proved a co-trained
# lookup bridge (V2_6 held-out macro 0.987/0.992 · C2 VALID). The task is the minimal mirror
# of the BINDING wall (H_9327/H_9359): the FACT lives ONLY in the store, the OPERATOR lives
# ONLY in the text, and the answer = polarity XOR operator (is/not × good/bad) requires binding
# the two — a nonlinear readout the parent's linear 1x1-conv head cannot do alone (the CLMS
# lane's GELU-MLP supplies it). EN-only: `is`/`not` are both FREE + PRE-POSED at the same slot,
# so operator identity is never confounded with position (the EN discriminator, CLAUDE.md EN-FIRST).
# --------------------------------------------------------------------------- #
_SB_CONSONANTS = "bdfgklmnprstvz"
_SB_VOWELS = "aeiou"
_SB_ANSWER = {0: "good", 1: "bad"}          # POL_GOOD, POL_BAD (v2 gen.py ANSWER_BYTES)


def _sb_read_entity_pool(path):
    """Read an EXTERNAL entity pool (H_9683): one ascii atom per line, order preserved.

    The builtin pool is CVCVC nonce — every key is novel bytes with no corpus prior. H_9683 asks
    whether the addr lever survives on NATURAL declaration vocabulary, which cannot be enumerated
    from `_SB_CONSONANTS x _SB_VOWELS`, so the pool becomes an input. This is a corpus-builder
    extension, NOT a lever: the split/leak/eval contracts below are the SAME code path either way.

    Order is PRESERVED (not sorted): the builtin sorts because the CVCVC enumeration order is an
    artifact of the loop nest, whereas a supplied file's order is the caller's — and the interleaved
    _sb_split reads that order. The file is therefore the full determinism surface (same file =>
    same split, seed-independent, exactly like the builtin).

    Rejects (SystemExit, never a silent downgrade): non-ascii · whitespace inside an atom ·
    duplicates. Blank lines are ignored (trailing newline is not an atom)."""
    try:
        raw = open(path, "r", encoding="utf-8", errors="strict").read()
    except OSError as e:
        raise SystemExit("storebind: cannot read --entity-pool %s (%s)" % (path, e))
    except UnicodeDecodeError as e:
        raise SystemExit("storebind: --entity-pool %s is not decodable text (%s)" % (path, e))
    names = [ln.strip() for ln in raw.split("\n")]
    names = [nm for nm in names if nm]
    if not names:
        raise SystemExit("storebind: --entity-pool %s is empty (one ascii atom per line)" % path)
    bad = [nm for nm in names if any(ord(ch) > 127 for ch in nm)]
    if bad:
        raise SystemExit("storebind: --entity-pool non-ascii atom(s) %d: %s (EN-only · the corpus "
                         "and every manifest are ascii-encoded)" % (len(bad), bad[:5]))
    spaced = [nm for nm in names if any(ch.isspace() for ch in nm)]
    if spaced:
        raise SystemExit("storebind: --entity-pool atom(s) contain whitespace %d: %s (one atom per "
                         "line; a multi-word key breaks the `%s %s => ` query surface)"
                         % (len(spaced), spaced[:5], "<op>", "<entity>"))
    dups = sorted({nm for nm in names if names.count(nm) > 1})
    if dups:
        raise SystemExit("storebind: --entity-pool duplicate atom(s) %d: %s (a duplicate would put "
                         "the same key in both split halves and forge the 0-shot stratum)"
                         % (len(dups), dups[:5]))
    return names


def _sb_entity_pool(n_total, entity_pool=None):
    """Deterministic CVCVC nonce pool, stride-sampled to n_total (v2 gen.entity_pool port).
    Sorted + sliced => the train/held-out split is a pure function of n_total, seed-independent.

    entity_pool = path to an external one-atom-per-line file (H_9683 natural vocabulary). When
    given, that file replaces the nonce enumeration and is stride-sampled to n_total by the SAME
    formula — everything downstream (split, leak witness, manifests) is untouched. When omitted the
    builtin path is byte-identical to before (hard requirement: regression 0)."""
    if entity_pool is not None:
        names = _sb_read_entity_pool(entity_pool)
        if len(names) < n_total:
            raise SystemExit("storebind: --entity-pool %s has %d atom(s) < requested n_pool %d"
                             % (entity_pool, len(names), n_total))
    else:
        names = []
        for c0 in _SB_CONSONANTS:
            for v0 in _SB_VOWELS:
                for c1 in _SB_CONSONANTS:
                    for v1 in _SB_VOWELS:
                        for c2 in _SB_CONSONANTS:
                            names.append(c0 + v0 + c1 + v1 + c2)
        names = sorted(set(names))
        if len(names) < n_total:
            raise SystemExit("storebind: nonce pool %d < requested %d" % (len(names), n_total))
    step = (len(names) - 1) / float(n_total - 1)
    return [names[int(round(i * step))] for i in range(n_total)]


def _sb_split(pool, n_eval):
    """Interleaved disjoint train/held-out split (every ratio-th name held out) so both halves
    are drawn from the same region of name-space — novelty is 'a new key built from seen bytes',
    not 'a different distribution' (v2 gen.split_pool port)."""
    ratio = len(pool) // n_eval
    train, ev = [], []
    for i, nm in enumerate(pool):
        (ev if i % ratio == ratio - 1 else train).append(nm)
    return train, ev


def _sb_answer(op, polarity):
    """answer = polarity XOR operator. op 0=is (identity), 1=not (flip)."""
    return polarity if op == 0 else (1 - polarity)


def _sb_emit_block(rng, entities, store_slots, balanced=False):
    """One block = one store draw with a FRESH polarity per slot, then EXACTLY ONE query line per
    stored entity in a random order. Block-level rotation is the mmap-window-compatible analogue of
    v2's per-example rotation: because a block re-draws every polarity, memorizing entity->polarity
    into the weights returns exactly chance (0.5), so every point above chance must route through the
    bridge. One line per entity per block (no re-appearance within a block) removes the in-window copy
    source — the quietest P1 contaminant (H_9423 잔인한 판정 ③). balanced=True forces EXACTLY
    store_slots/2 good + store_slots/2 bad pols per store (H_9672: the majority-polarity shortcut
    ceiling — a readout of `op ⊕ majority(pols)` reaches ~0.637 on random stores with the address
    fully dead — collapses to 0.5 when the polarity ratio is constant, so a balanced eval store is the
    PRIMARY scoring face that isolates real content-addressing from the shortcut)."""
    idx = rng.sample(range(len(entities)), store_slots)
    names = [entities[i] for i in idx]
    if balanced:
        pols = [0] * (store_slots // 2) + [1] * (store_slots - store_slots // 2)
        rng.shuffle(pols)
    else:
        pols = [rng.randint(0, 1) for _ in range(store_slots)]
    rows, lines = [], []
    order = list(range(store_slots))
    rng.shuffle(order)
    for slot in order:
        op = rng.randint(0, 1)
        entity = names[slot]
        polarity = pols[slot]
        ans = _sb_answer(op, polarity)
        op_s = "is" if op == 0 else "not"
        prompt = "%s %s => " % (op_s, entity)          # query pos = last prompt byte (bridge query)
        lines.append(prompt + _SB_ANSWER[ans])
        # row schema = the CLMS-lane INPUT contract (core/clms.py store_apply + evaluate --store):
        #   store = the 8-slot {entities, pols} injected at the query · target_slot = the queried slot
        #   (oracle one-hot) · gold = answer byte · op kept for the polarity/operator class split.
        rows.append({"prompt": prompt, "gold": _SB_ANSWER[ans], "entity": entity,
                     "store": {"entities": list(names), "pols": list(pols)},
                     "target_slot": slot, "op": op})
    return lines, rows


# ── H_9694 (R2) g6bind — targeted vs shuf co-train corpus (kill#6 bind-Δ debris recovery) ──
# convergence g6-ideation-hexa-1 killed "TARGETED forges FALS" but NOT "TARGETED moves BIND":
# it OBSERVED bind Δ 0.444 (targeted) vs 0.000 (shuf) with a non-frozen hexa-era probe, so the
# observation never earned verdict status. This builder rebuilds that 2-arm lever so the signal
# can be re-earned through the frozen --fan-bind surface (H_9693).
#
# THE CONTROL IS THE POINT (corpus-py-1 · control-must-match-mediating-covariate): both arms
# contain the IDENTICAL MULTISET of frames and claims — byte-for-byte the same lines, the same
# comparator/measurable/content distribution, the same length. ONLY the frame↔claim PAIRING
# differs: targeted binds each frame to the claim about ITS OWN (cA,cB); shuf DERANGES that
# assignment so every claim sits under a frame it does not bind. A lever that only moves FORM
# therefore cannot separate the arms — which is exactly what makes bind Δ readable.
# Claim vocabulary is drawn ONLY from the frozen rho_fan comparator/measurable sets: injecting
# new detector vocabulary would be tuning the detector (kill #2/#6), not testing the substrate.

def _g6bind_claim(cA, cB, rng, comp_l, meas_l):
    """One falsifiable-SHAPED claim that carries content from BOTH concepts.
    FORM (comparator × measurable × >=2 content) is satisfied in BOTH arms by construction —
    that is deliberate: FORM is not the DV, the frame↔claim binding is."""
    wa = [w for w in cA.split() if len(w) >= 3]
    wb = [w for w in cB.split() if len(w) >= 3]
    a1 = wa[rng.randrange(len(wa))]
    b1 = wb[rng.randrange(len(wb))]
    cmp_w = comp_l[rng.randrange(len(comp_l))]
    mea_w = meas_l[rng.randrange(len(meas_l))]
    forms = [
        "the %s of %s %s with the %s of %s" % (mea_w, a1, cmp_w, mea_w, b1),
        "as %s %s, the %s of %s is %s" % (a1, cmp_w, mea_w, b1, cmp_w),
        "%s %s the %s at which %s holds" % (a1, cmp_w, mea_w, b1),
        "when %s shifts, the %s of %s %s" % (a1, mea_w, b1, cmp_w),
    ]
    return forms[rng.randrange(len(forms))]


def _fanbind_content_words(sentence, known, stop):
    """H_9746 — content-word set under the frozen detector's own gate (mirror of
    cli/evaluate.py:_fan_bind_content: len>=3 ∧ in known ∧ not stopword). No new vocab."""
    return set(w for w in sentence.lower().replace(",", " ").replace(".", " ").split()
               if len(w) >= 3 and w in known and w not in stop)


def _build_g6bind_bindpos(cz, n, comp_l, meas_l, rng, n_blocks, seed, lang):
    """H_9746 fan-bind decode-level POSITIVE CONTROL (lab full Fable design). A model trained on this
    reads 🟢 BIND-SENSITIVE through the full decode pipeline iff the instrument's dynamic range is
    intact — so a PASS attributes R2's BIND-ABSENT to lever-invalid (not instrument-defect).

    The composition is forced on the PAIR-CLASS, not on prompt presence (else both arms co-emit ⇒
    delta≈0). frozen geometry gives the split: BIND class = adjacent pairs (a,(a+1)%n) = the composed
    frames; NULL class = distance-2 pairs (a,(a+2)%n) = the derangement set. Rule learned: adjacent
    pair ⇒ emit cA+cB content words; distance-2 pair ⇒ emit cA only (suppress cB even though it is IN
    the prompt) — unsolvable by echo, which is exactly 'composition'."""
    import rho_fan as _rf
    known = _rf._rho_fan_dict() if hasattr(_rf, "_rho_fan_dict") else None
    # detector known-set + stopwords (mirror evaluate.py's _fan_bind_content gate)
    stop = _rf._rho_fan_stopwords()
    # known dict: fall back to the union of all concept words if no explicit dict export
    if known is None:
        known = set()
        for c in cz:
            known |= set(w for w in c.lower().split() if len(w) >= 3)
    # per-concept discriminator token = a content word UNIQUE to that concept (not in any other's
    # content, not a comparator/measurable). Pick the shortest for the 40-byte budget (F2).
    conts = [_fanbind_content_words(c, known, stop) for c in cz]
    cmpset = set(comp_l); measet = set(meas_l)
    disc = []
    for k in range(n):
        others = set().union(*[conts[j] for j in range(n) if j != k]) if n > 1 else set()
        uniq = sorted(conts[k] - others - cmpset - measet, key=len)
        if not uniq:
            raise SystemExit("g6bind bindpos: concept %d has no unique discriminator token "
                             "(content=%r)" % (k, sorted(conts[k])))
        disc.append(uniq[0])
    # short comparator/measurable (banned-word-free · F2 budget)
    BAN = {"when", "whenever", "into", "between", "still", "new"}
    cmp_s = [w for w in ("causes", "predicts", "depends") if w in cmpset and w not in BAN]
    mea_s = [w for w in ("rate", "count", "level", "ratio", "score", "value") if w in measet and w not in BAN]
    if not cmp_s or not mea_s:
        raise SystemExit("g6bind bindpos: short cmp/mea set empty (cmp=%r mea=%r)" % (cmp_s, mea_s))
    # per-block: 50% BIND (adjacent), 50% NULL (distance-2), 10 pairs balanced
    pairs = ([( a, (a + 1) % n, "BIND") for a in range(n)] +
             [( a, (a + 2) % n, "NULL") for a in range(n)])
    lines = []
    per = max(1, n_blocks // len(pairs))
    for (a, b, cls) in pairs:
        for _ in range(per):
            cmp_w = cmp_s[rng.randrange(len(cmp_s))]
            mea_w = mea_s[rng.randrange(len(mea_s))]
            frame = "if %s, then %s: " % (cz[a], cz[b])
            if cls == "BIND":
                claim = ("%s %s the %s of %s" % (disc[a], cmp_w, mea_w, disc[b]) if rng.random() < 0.5
                         else "the %s of %s %s %s" % (mea_w, disc[a], cmp_w, disc[b]))
            else:  # NULL: cA-echo only, cB suppressed
                claim = ("the %s of %s %s" % (mea_w, disc[a], cmp_w) if rng.random() < 0.5
                         else "%s %s the %s" % (disc[a], cmp_w, mea_w))
            lines.append((frame + claim, a, b, cls))
    rng.shuffle(lines)
    # ── hard asserts (§2) — the J self-witness is the strongest: the frozen detector itself signs
    #    that every BIND line scores 1 and every NULL line scores 0 for the PROMPTED pair. ──
    def _J(o, cA, cB):
        A = _fanbind_content_words(cA, known, stop)
        B = _fanbind_content_words(cB, known, stop) - A
        if not A or not B: return None
        wo = set(o.lower().split())
        return 1 if (wo & A) and (wo & B) else 0
    bad = 0
    for (ln, a, b, cls) in lines:
        claim = ln.split(": ", 1)[1]
        j = _J(claim, cz[a], cz[b])
        if cls == "BIND" and j != 1: bad += 1
        if cls == "NULL" and j == 1: bad += 1
    if bad:
        raise SystemExit("g6bind bindpos: J self-witness FAILED on %d/%d lines (detector does not "
                         "score the corpus as designed)" % (bad, len(lines)))
    text = "\n".join(ln for (ln, a, b, cls) in lines) + "\n"
    n_bind = sum(1 for (_, _, _, c) in lines if c == "BIND")
    st = {"arm": "bindpos", "n_blocks": n_blocks, "lines": len(lines),
          "bytes": len(text.encode("ascii")), "seed": seed, "lang": lang,
          "n_bind": n_bind, "n_null": len(lines) - n_bind,
          "discriminators": {cz[k][:20]: disc[k] for k in range(n)},
          "max_line_bytes": max((len(ln.encode("ascii")) for (ln, _, _, _) in lines), default=0),
          "J_self_witness": "PASS (all BIND→1 · all NULL→0)"}
    return text, st


def build_g6bind(n_blocks, seed, lang, arm):
    """`anima-py corpus g6bind --lang en --arm {targeted,shuf,bindpos} --n-blocks N --seed S` — H_9694.

    Returns (text, st). st carries a HARD-ASSERTED byte-match witness: the two arms' line
    multisets must be identical (only order/pairing differs), so any bind Δ between the trained
    arms cannot be a content/length/vocabulary artifact."""
    if lang != "en":
        raise SystemExit("g6bind is EN-only (--lang en): the frozen rho_fan concepts/detector are en "
                         "(CLAUDE.md EN-FIRST · the ko lane is BINDING)")
    if arm not in ("targeted", "shuf", "bindpos"):
        raise SystemExit("g6bind: --arm must be targeted|shuf|bindpos (got %r)" % arm)
    import rho_fan as _rf
    cz = _rf._rho_fan_concepts()
    n = len(cz)
    comp_l = sorted(_rf._rho_fan_comparator())
    meas_l = sorted(_rf._rho_fan_measurable())
    rng = random.Random(seed)
    if arm == "bindpos":
        return _build_g6bind_bindpos(cz, n, comp_l, meas_l, rng, n_blocks, seed, lang)
    # ── build the SHARED pool: (frame_i, claim_i) where claim_i is about frame_i's own pair ──
    frames = []
    claims = []
    for k in range(n_blocks):
        a = rng.randrange(n)
        b = (a + 1 + rng.randrange(n - 1)) % n          # b != a
        frames.append("if %s, then %s: " % (cz[a], cz[b]))
        claims.append(_g6bind_claim(cz[a], cz[b], rng, comp_l, meas_l))
    # ── the ONLY difference: how claims are assigned to frames ──
    if arm == "targeted":
        order = list(range(n_blocks))                    # claim_i under frame_i (binds)
    else:
        order = _g6bind_derange(n_blocks, random.Random(seed + 40009))   # claim_j under frame_i, j != i
    lines = [frames[i] + claims[order[i]] for i in range(n_blocks)]
    text = "\n".join(lines) + "\n"
    # ── byte-match witness (HARD): both arms are the same frame multiset AND the same claim
    #    multiset; only the pairing differs. Assert it here so a builder edit cannot silently
    #    break the control (a broken control makes every downstream bind Δ uninterpretable).
    fixed = sum(1 for i in range(n_blocks) if order[i] == i)
    if arm == "shuf" and fixed:
        raise SystemExit("g6bind: derangement broken — %d fixed points (claim still binds its own "
                         "frame). The shuf arm MUST have zero." % fixed)
    st = {"arm": arm, "n_blocks": n_blocks, "lines": len(lines),
          "bytes": len(text.encode("ascii")), "seed": seed, "lang": lang,
          "fixed_points": fixed,
          "frame_multiset_sha": _g6bind_sha(sorted(frames)),
          "claim_multiset_sha": _g6bind_sha(sorted(claims)),
          "max_line_bytes": max((len(x.encode("ascii")) for x in lines), default=0)}
    return text, st


def _g6bind_derange(nn, rng):
    """Sattolo cycle — EVERY index moves (0 fixed points), so no claim binds its own frame."""
    p = list(range(nn))
    for i in range(nn - 1, 0, -1):
        j = rng.randrange(i)                             # j < i STRICTLY = the Sattolo difference
        p[i], p[j] = p[j], p[i]
    return p


def _g6bind_sha(items):
    import hashlib
    h = hashlib.sha256()
    for x in items:
        h.update(x.encode("ascii")); h.update(b"\x00")
    return h.hexdigest()[:12]


def build_storebind(n_blocks, store_slots, seed, lang, n_pool=512, n_eval=128, replay=0,
                    entity_pool=None):
    """Build the storebind corpus + co-train store manifest + 0-shot held-out eval manifest.

    Returns (text, st). st carries the manifests and a hard-asserted zero-leak witness. The store
    manifest (rows of {store_names, store_pols, slot, op, prompt, answer}) is the CLMS-lane INPUT
    contract: `anima-py evaluate <clm> --store held.json` feeds each row's store to the bridge and
    scores the answer byte — the SAME manifest the trainer co-trains on (train == infer manifest =
    a literal p8 implementation, not a train/infer split).

    entity_pool (H_9683) swaps the builtin CVCVC nonce enumeration for an external one-atom-per-line
    file. It is a BUILDER extension, not a lever: every contract below (EN-only · n_pool % n_eval ·
    interleaved disjoint split · store_slots <= held-out · C0-a zero-leak hard-assert) runs on the
    external pool unchanged. Note the leak witness is SUBSTRING-based (`e in corpus_blob`), which on
    natural vocabulary fails CLOSED — a held-out atom contained in a train atom (`art` ⊂ `start`,
    corpus-py-1 ⑩) aborts the build rather than shipping a forged 0-shot stratum."""
    if lang != "en":
        raise SystemExit("storebind is EN-only (--lang en): the free pre-posed `not` vs `is` is the "
                         "operator discriminator (CLAUDE.md EN-FIRST · the ko suffix lane is BINDING)")
    if n_pool % n_eval != 0:
        raise SystemExit("storebind: n_pool %d must be a multiple of n_eval %d (interleave ratio)"
                         % (n_pool, n_eval))
    pool = _sb_entity_pool(n_pool, entity_pool)
    train, ev = _sb_split(pool, n_eval)
    if set(train) & set(ev):
        raise SystemExit("storebind: train/held-out overlap (%d)" % len(set(train) & set(ev)))
    if store_slots > len(ev):
        raise SystemExit("storebind: store_slots %d > held-out pool %d" % (store_slots, len(ev)))

    rng = random.Random(seed)
    lines, store_rows = [], []
    for _ in range(n_blocks):
        bl, br = _sb_emit_block(rng, train, store_slots)
        lines.extend(bl)
        store_rows.extend(br)

    # 0-shot held-out eval blocks: store drawn ONLY from held-out entities (never in c.txt). A
    # separate stream (seed+offset) so the eval manifest is reproducible independent of n_blocks.
    ev_rng = random.Random(seed + 10007)
    n_eval_blocks = max(1, n_eval // store_slots)
    held_rows = []
    for _ in range(n_eval_blocks):
        _, br = _sb_emit_block(ev_rng, ev, store_slots)
        held_rows.extend(br)

    # H_9672 balanced held manifest: SAME held-out entities, but every store is forced to exactly
    # store_slots/2 good + store_slots/2 bad → the majority-polarity shortcut ceiling (~0.637) collapses
    # to 0.5, so this is the PRIMARY scoring face for the address lever (isolates content-addressing
    # from the polarity-ratio shortcut that flip-coherence cannot catch). Separate rng stream.
    bal_rng = random.Random(seed + 10009)
    bal_rows = []
    for _ in range(n_eval_blocks):
        _, br = _sb_emit_block(bal_rng, ev, store_slots, balanced=True)
        bal_rows.extend(br)
    # H_9672 seen manifest: eval blocks over TRAIN entities (addr-gap control — train-address accuracy
    # vs held-out isolates memorization[gap>.35] from generalization[gap<=.20]). NOT held-out (train
    # entities are in the corpus) → for addr audit ONLY, never a 0-shot claim.
    seen_rng = random.Random(seed + 10011)
    seen_rows = []
    for _ in range(n_eval_blocks):
        _, br = _sb_emit_block(seen_rng, train, store_slots)
        seen_rows.extend(br)

    # C0-a zero-leak HARD-ASSERT (both surfaces): a held-out entity must appear NOWHERE in the
    # training corpus — not as a store key, not as a prompt substring. A gate that scores a stratum
    # the corpus reinforces is a forgery that always passes (cpt-destroys-what-corpus-omits); the
    # judged stratum must be 0-shot. A leak aborts the build (never silently ships).
    ev_set = set(ev)
    corpus_blob = "\n".join(lines)
    leaked = sorted({e for e in ev_set if e in corpus_blob})
    key_leaks = sum(1 for r in store_rows if any(e in ev_set for e in r["store"]["entities"]))
    if leaked or key_leaks:
        raise SystemExit("storebind: C0-a EVAL LEAK — %d held-out entit(y/ies) in corpus text, "
                         "%d store-key leaks: %s" % (len(leaked), key_leaks, leaked[:5]))

    text = corpus_blob + "\n"
    # replay mix (retention defense · optional): repeat a fraction of blocks so a later CPT-style
    # co-train does not erase base fluency. S0 default 0 (pure task); S1 sweeps this.
    if replay > 0:
        rep_rng = random.Random(seed + 20011)
        extra = rep_rng.sample(lines, min(replay, len(lines)))
        text = text + "\n".join(extra) + "\n"

    max_bytes = max((len(x.encode("ascii")) for x in lines), default=0)
    store_manifest = {"schema": "anima-storebind/v1", "store_slots": store_slots,
                      "lang": lang, "seed": seed, "entries": store_rows}
    held_manifest = {"schema": "anima-storebind/v1", "store_slots": store_slots,
                     "lang": lang, "seed": seed, "held_out": True, "entries": held_rows}
    balanced_manifest = {"schema": "anima-storebind/v1", "store_slots": store_slots, "lang": lang,
                         "seed": seed, "held_out": True, "balanced": True, "entries": bal_rows}
    seen_manifest = {"schema": "anima-storebind/v1", "store_slots": store_slots, "lang": lang,
                     "seed": seed, "held_out": False, "seen": True, "entries": seen_rows}
    st = {"n_blocks": n_blocks, "store_slots": store_slots, "lines": len(lines),
          "bytes": len(text.encode("ascii")), "max_line_bytes": max_bytes,
          "n_train": len(train), "n_heldout": len(ev), "n_pool": n_pool,
          "n_eval_blocks": n_eval_blocks, "leak": 0, "replay": replay,
          "entity_pool": entity_pool,
          "store_manifest": store_manifest, "held_manifest": held_manifest,
          "balanced_manifest": balanced_manifest, "seen_manifest": seen_manifest}
    return text, st


# --------------------------------------------------------------------------- #
# counterfactual-decl — EPHEMERAL-DECLARATION grounding corpus (H_9800 · R11).
#
# WHY THIS FORMAT EXISTS. H_9359 measured that the operator does not look up a declared store at
# runtime (the two-lane wall). H_9800 reframes that as ECONOMICS, not absence: in every corpus
# built so far a stem's polarity is GLOBALLY FIXED, so memorising stem->polarity into the weights
# is strictly cheaper (in CE) than reading a declaration at runtime. A parametric cache is then
# the RATIONAL minimiser and the bridge is never paid for.
#
# This format removes that option. Every episode RE-DRAWS
#   stem -> sense   (good | harm)      and      operator -> role  (same | flip)
# so the SAME stem carries the OPPOSITE declaration in the next episode, and the SAME operator
# name affirms in one episode and negates in the next. A weight-cached stem prior therefore
# returns EXACTLY the realized chance level, and the only remaining CE minimiser is to read the
# in-context declaration. next-byte CE itself pays for the bridge.
#
# THE THREE INVARIANTS THAT MAKE IT READABLE (each is asserted, never assumed):
#  ① the query carrier is `<op> <stem> => ` — it contains NEITHER an answer token (aye|nay) NOR a
#    label name (good|harm|same|flip). The instrument must not install the operator->answer map;
#    if the carrier carried it, a model could answer without composing anything (this is the
#    `no arbitrary grounding` requirement, and it is re-checked at EVAL time too).
#  ② the target is a pure composition: answer_bit = sense_bit XOR role_bit. Nothing else in the
#    episode determines it.
#  ③ EXACT polarity balance, VERIFIED by re-parsing the file that was actually written to disk
#    (not the generator's internal counters). Balance is structural — each stem is queried once
#    under the `same` operator and once under the `flip` operator, so its two answers are always
#    {aye, nay} — but a structural argument is not evidence, so the audit re-derives the counts
#    and the CHANCE LEVEL from the realized split (chance-level-must-be-derived-per-metric: a
#    pedestal that happens to be uniform is a coincidence that hides defects, never an assumption).
#
# THE SPLIT IS OVER MAPPINGS, NOT ONLY OVER STEMS. Holding out stems alone would leave the
# instrument readable by a model that learned `a declared stem keeps whatever sense it had`. So
# the stem pool is three-way and the operator pool is three-way:
#   rotating  — sense/role re-drawn EVERY episode (the non-stationary bulk of the corpus)
#   frozen    — present in training but with a FIXED sense/role for the whole corpus; the eval
#               stratum presents them with the ANTI sense/role, i.e. a MAPPING the corpus never
#               contains even though its bytes are fully seen. This is the stratum that separates
#               `reads the declaration` from `has a stem prior`.
#   held      — bytes that appear 0x in the corpus (0-shot), hard-asserted.
#
# EN-only (`--lang en`, owner directive · CLAUDE.md EN-FIRST): the role words are FREE pre-posed
# tokens, so operator identity is never confounded with morphology.
# --------------------------------------------------------------------------- #
_CD_SENSE = {1: "good", 0: "harm"}          # stem declaration value (both 4B — flip is byte-length
_CD_ROLE = {0: "same", 1: "flip"}           # operator declaration value (both 4B) preserving, so a
_CD_ANSWER = {1: "aye", 0: "nay"}           # answer token (both 3B — no length confound in the 2AFC)
# Every literal the corpus grammar owns. A nonce name that CONTAINS one of these (or that one of
# these contains) would make the leak/derangement audits ambiguous, so such names are dropped from
# the pool at build time rather than filtered later.
_CD_RESERVED = ("good", "harm", "same", "flip", "aye", "nay", "means", "acts", "ep")


# ═══════════════════════════════════════════════════════════════════════════════════════════════
#  H_9810 · `anima corpus bindpanel` — the HELD-OUT BINDING PANEL the H_9805 tension-field arms
#  are scored on (`anima-py evaluate <clm> --bind-panel <panel.json>`).
#
#  WHY IT LOOKS THE WAY IT DOES — read this before touching a lexeme.
#  --------------------------------------------------------------------------------------------
#  H_9805's field is `core/tension_field.py`. Read that file's `chunk_heads`/`byte_class` and one
#  fact falls out that decides this entire design: the field T is a function of the WHITESPACE
#  MASK and nothing else.
#     · chunk starts (and therefore head_A / head_G) are determined by where the spaces are;
#     · chi[i,j] = byte_class(i)==byte_class(j), and every head j is a letter (class 2), so chi
#       reduces to "is position i a space or not".
#  ⇒ T is blind to WHICH letters are present. It sees the sequence of word LENGTHS, full stop.
#
#  The consequence is not cosmetic. On a panel whose answer depends on lexical identity, the
#  production field carries EXACTLY ZERO bits about the answer, `duel` and `rank1` both reduce a
#  field that is answer-irrelevant, and F1 (Δd_acc(duel−rank1)) is not measurable — it would
#  return ~0 for a reason that has nothing to do with rank. Such a panel does not test the
#  hypothesis; it tests nothing.
#
#  So this panel is LENGTH-CODED on purpose, and says so out loud:
#     verb   agreement-marked "walks"  (stem+s, 5B)   vs  participle "walking" (stem+ing, 7B)
#     noun   singular         "doctor" (6B)           vs  plural     "doctors" (7B)
#  Every stem is 4 letters and every singular noun is 6 letters, so the two binding features are
#  carried by chunk LENGTH — the only channel the field has. `hp` (is the verb agreement-marked)
#  and `pos` (is the singular noun the near one) are each balanced at exactly 0.5 against the
#  gold, and the gold is their XOR, so no unary cue answers a single slot. That XOR-over-an-edge
#  is H_004's construction transplanted to English (EN-FIRST directive) with honorific concord
#  replaced by number concord — the same replacement H_9805 already made when it swapped
#  honorific chi for byte-class chi.
#
#  K conjuncts are STACKED in one sentence because a single contested edge collapses the field to
#  rank 1 by construction (H_004 measured off-top 0.000 on its single-bind frame and declared it
#  F4-DEAD at $0). K slots ⇒ K independent contested edges ⇒ a field with rank to lose.
#
#  The gold codebook is the FULL 2^K factorial, which is why it is full GF(2) rank with no
#  prefix-determined column: `--free-slot-score` recomputes the free-slot set from it and must
#  return ALL K slots free with a field-blind ceiling equal to chance. H_004 shipped a rank-4
#  K=6 codebook, teacher-forcing completed its 2 parity slots for free, and every arm was
#  inflated to a 0.667 ceiling that reached held-out — the defect this codebook cannot have.
# ═══════════════════════════════════════════════════════════════════════════════════════════════

# 4-letter stems: +"s" => 5B agreement-marked · +"ing" => 7B participle. Length is the channel.
_BP_VERB_SEEN = ["call", "help", "jump", "look", "talk", "walk", "want", "work"]
_BP_VERB_HELD = ["wait", "pull", "push", "kick", "hold", "lead", "feed", "send"]
# 6-letter nouns: +"s" => 7B plural.
_BP_NOUN_SEEN = ["doctor", "artist", "banker", "driver", "farmer", "hunter", "keeper", "lawyer"]
_BP_NOUN_HELD = ["mentor", "singer", "tailor", "writer", "dancer", "porter", "sailor", "editor"]
_BP_ANS = ("up", "dn")                      # 2B each — length parity, checked by --free-slot-score
_BP_TAIL = "waited"
_BP_ARROW = " => "


def _bp_hp_patterns(K):
    """4 hp (agreement-marked) patterns whose per-slot values are exactly balanced 2:2.

    Balance is what makes the presence heuristic exactly 0.5 with no sampling noise: for every
    slot k the four patterns supply {0, 1, k%2, 1-k%2} = two 0s and two 1s."""
    return [[0] * K, [1] * K, [k % 2 for k in range(K)], [1 - k % 2 for k in range(K)]]


# H_9812 — LENGTH-MATCHED morphology (the repair the field-alone leak gate forced).
# The legacy forms were `+s`(1 B) vs `+ing`(3 B) and noun vs noun+`s`(+1 B), so the SURFACE BYTE
# LENGTH encoded both hp and pos. The layout-only `class` field reads word lengths straight off the
# whitespace mask ⇒ the gate measured field-alone acc 1.0000 vs chance 0.5000: the panel did not
# give the field a channel, it handed over the answer, and no Δ on it was readable.
#
# Matched forms fix that BY CONSTRUCTION:
#   verb  hp=1 -> `+es`   hp=0 -> `+ed`    both 2 B · final byte differs (s|d)
#   noun  sg   -> `+us`   pl   -> `+is`    both 2 B · final byte IDENTICAL (s)
# Every surface is now byte-length-identical whatever the gold is, so the layout carries nothing.
# The asymmetry is deliberate and load-bearing: `morph` (final byte) can see hp but NOT pos, and
# gold = hp XOR pos needs both — so a concord field still cannot call gold alone, while the TRUNK,
# which reads the actual bytes (`u` vs `i`), can. That is the ②core-sees-content fork made testable
# instead of asserted.
_BP_VF = {"matched": lambda v, hp: v + ("es" if hp else "ed"),
          "legacy":  lambda v, hp: v + ("s" if hp else "ing")}
_BP_NF = {"matched": (lambda n: n + "us", lambda n: n + "is"),
          "legacy":  (lambda n: n, lambda n: n + "s")}


# H_9815 — TASK axis. `xor` is the measurement panel (gold = hp XOR pos: neither term alone
# predicts it, and reading it needs the two heads BOUND across the `of` edge). `hp` is the
# POSITIVE CONTROL: gold = hp alone, so the answer is a single local feature with no composition
# at all. Why it exists: H_9814 closed every plumbing axis (complexity/RF/objective-weight/
# normalisation) and the toy STILL sits at chance on `xor` — even where the exact line, answer
# included, occurs 31x in the drill. A negative with no positive control is unreadable
# (`positive-control-before-reading-a-negative`): if `hp` also floors, the wall is plumbing and
# nothing measured on this substrate means anything; if `hp` is learned and `xor` is not, this toy
# reproduces the repo's standing RECOMBINATION wall at 4 kB scale — a cheap, local instance of the
# thing 303M keeps failing.
def _bp_conjunct(hp, pos, verb, sg, pl, lengths="matched", task="xor"):
    """One contested edge. `pos` 0 = the SINGULAR noun is the near (N1) noun.

    gold = hp XOR pos. Neither term alone predicts it (both are balanced against gold across the
    panel), and reading it requires binding the verb's agreement marker to the correct head across
    the `of` edge — the operation the tension field claims to carry."""
    vf = _BP_VF[lengths](verb, hp)
    sgf, plf = _BP_NF[lengths]
    sg, pl = sgf(sg), plf(pl)
    n1, n2 = (sg, pl) if pos == 0 else (pl, sg)
    # R11 stair: at the conjunct level only three PRIMITIVE tasks exist — xor (composition),
    # hp / pos (the two unary sub-features). "stair"/"xmark" are DRILL-mixture modes resolved
    # in build_bindpanel; they never reach here.
    _gb = {"hp": hp, "pos": pos}.get(task, hp ^ pos)
    return {"surface": "%s %s of %s and" % (vf, n1, n2),
            "hp": hp, "pos": pos, "verb": verb, "verb_form": vf,
            "sg_lexeme": sg, "pl_lexeme": pl, "n1": n1, "n2": n2,
            "gold_bit": _gb, "gold_token": _BP_ANS[_gb]}


# H_9818 — CURRICULUM axis (`xmark`). The gradient argument, not a structural one: the panel audit
# FORCES every unary cue to exactly 0.5, so under `xor` neither `hp` nor `pos` has any marginal
# correlation with gold ⇒ descent gets NO signal on either feature until it holds BOTH at once.
# That is the flat-parity landscape, and it is a claim about the OBJECTIVE, not the architecture
# (H_9816 tests the same diagnosis on the optimizer's budget/regularization axis instead).
#
# `xmark` supplies that missing gradient directly: the SAME sentence is drilled under three
# 2-byte TASK MARKERS — `h ` (gold = hp), `p ` (gold = pos), `x ` (gold = hp XOR pos). The h/p
# lines make each sub-feature individually predictable, so descent can find them from a signal
# that actually exists; the x lines then only have to COMBINE two features the trunk already
# computes. The markers are equal-length and CONSTANT within any one panel, so they add nothing
# a heuristic could read (the exactly-0.5 audit still runs on the x panel and still must pass).
#
# ⚠️ SCOPE: this is a DATA-side lever (the corpus teaches sub-features), which makes it a weaker
# claim than an architectural one — it shows the composition is LEARNABLE given sub-feature
# supervision, NOT that it emerges unaided. That distinction is the whole verdict and must be
# stated in the card, never softened.
_BP_MARK = {"hp": "h ", "pos": "p ", "xor": "x "}


def _bp_items(K, verbs, nouns, rot, lengths="matched", task="xor", mark=""):
    """The full factorial panel: 2^K gold patterns x 4 hp patterns = 4*2^K items.

    LEXEME ASSIGNMENT DEPENDS ON THE SLOT AND THE ROTATION ONLY — NEVER ON THE hp BLOCK. The
    first draft keyed it to (block, slot) and the build gate refused it with n1_lexeme = 1.000:
    hp is constant inside a block, so a block-keyed lexeme IDENTIFIES hp, and the noun's own
    singular/plural form gives pos ⇒ a pure lookup table on the N1 word form solved every slot
    while `presence` and `position` each still read a blameless 0.5. That is a conjunction leak of
    exactly H_004's family, and it was invisible in the two unary numbers. With the block dropped
    from the key, every lexeme group spans all four hp blocks and all 2^K gold patterns, so it is
    exactly 50/50 — zero sampling slack, unlike an RNG assignment that is only 0.5 in expectation."""
    nv, nn = len(verbs), len(nouns)
    items = []
    for b, hp_pat in enumerate(_bp_hp_patterns(K)):
        for g in range(1 << K):
            gold = [(g >> k) & 1 for k in range(K)]
            conjs = []
            for k in range(K):
                j = (k + rot) % nv
                jn = (k + rot) % nn
                # xor: pos is CHOSEN so gold comes out as the enumerated pattern.
                # hp:  gold IS hp, so pos is free — enumerate it instead, keeping it balanced.
                # pos: gold IS pos, so pos takes the enumerated pattern (hp stays hp_pat-balanced).
                _pos = (gold[k] ^ hp_pat[k]) if task == "xor" else gold[k]
                conjs.append(_bp_conjunct(hp_pat[k], _pos,
                                          verbs[j], nouns[jn], nouns[(jn + 3) % nn],
                                          lengths=lengths, task=task))
            gold = [c["gold_bit"] for c in conjs]          # hp task: gold is hp, not the enum
            # `mark` (H_9818 xmark) is a 2-byte task selector. It is CONSTANT within any one
            # panel, so it shifts every surface by the same bytes and can carry no cue a
            # heuristic could exploit — the exactly-0.5 audit below still runs and still gates.
            surface = mark + " ".join(c["surface"] for c in conjs) + " " + _BP_TAIL + _BP_ARROW
            items.append({"block": b, "gold_index": g, "conjuncts": conjs, "surface": surface,
                          "task": task, "mark": mark, "gold_bits": gold,
                          "gold_pattern": "".join(c["gold_token"] for c in conjs)})
    return items


def _bp_majority(rows, keyfn):
    """Best-constant-predictor accuracy under a grouping = what a reader with ONLY that cue scores.
    This is the heuristic audit; 0.5 means the cue is worthless on this panel."""
    by = {}
    for gold, r in rows:
        by.setdefault(keyfn(r), []).append(gold)
    ok = 0
    for v in by.values():
        ones = sum(v)
        ok += max(ones, len(v) - ones)
    return ok / float(len(rows))


def _bp_audit(items, K):
    """Per-slot heuristic audit + pairwise slot independence. Every number must be exactly 0.5."""
    per_slot = []
    for k in range(K):
        rows = [(it["gold_bits"][k], it["conjuncts"][k]) for it in items]
        per_slot.append({
            "presence": round(_bp_majority(rows, lambda c: c["hp"]), 6),
            "position": round(_bp_majority(rows, lambda c: c["pos"]), 6),
            "locality": round(_bp_majority(rows, lambda c: 0), 6),
            "verb_lexeme": round(_bp_majority(rows, lambda c: c["verb"]), 6),
            "verb_form": round(_bp_majority(rows, lambda c: c["verb_form"]), 6),
            "n1_lexeme": round(_bp_majority(rows, lambda c: c["n1"]), 6),
            "n2_lexeme": round(_bp_majority(rows, lambda c: c["n2"]), 6),
            "balance": round(sum(g for g, _ in rows) / float(len(rows)), 6),
        })
    worst_pair, worst = None, 0.0
    n = float(len(items))
    for a in range(K):
        for b in range(a + 1, K):
            same = sum(1 for it in items if it["gold_bits"][a] == it["gold_bits"][b]) / n
            if abs(same - 0.5) > worst:
                worst, worst_pair = abs(same - 0.5), (a, b)
    in_band = all(abs(v - 0.5) <= 1e-9 for s in per_slot for v in s.values())
    lens = set(len(it["surface"].encode()) for it in items)
    return {"per_slot": per_slot, "worst_pairwise_dev": round(worst, 6), "worst_pair": worst_pair,
            "heuristics_exactly_half": in_band, "pairwise_independent": worst <= 1e-9,
            "surface_byte_lengths": sorted(lens),
            "max_seq_bytes": max(lens) + 2 * K}


def build_bindpanel(K, n_blocks, seed, lang, rot=0, lengths="matched", task="xor"):
    """Returns (drill_corpus_text, panel_items, codebook, stats).

    The DRILL corpus teaches the binding operation on the SEEN lexeme pool; the PANEL asks it on
    the HELD pool. The two pools are string-disjoint and neither nests in the other, so the 0-shot
    claim is checkable by word-boundary count (corpus-py-1 (G)) and is checked below."""
    if lang != "en":
        raise SystemExit("anima corpus bindpanel: --lang en only — the length-coded number-concord "
                         "frame is English (EN-FIRST directive); a ko port needs its own panel and "
                         "its own heuristic audit, not a translation.")
    if K < 2:
        raise SystemExit("anima corpus bindpanel: --bind-k must be >= 2 (K=1 has a single contested "
                         "edge and collapses the field to rank 1 by construction — H_004 F4-DEAD)")
    if task not in ("xor", "hp", "pos", "xmark"):
        # Fail LOUD. A typo must never fall through to a silently different gold rule — that would
        # ship a corpus whose answers are not the ones the card claims, and no downstream gate
        # could see it (the panel would audit clean because it is internally consistent).
        raise SystemExit("anima corpus bindpanel: --bind-task must be xor|hp|pos|xmark, got %r"
                         % (task,))
    # H_9818 xmark: the JUDGED task is still xor; the h/p lines are SUB-FEATURE SUPERVISION added
    # to the drill only. The panel therefore carries the `x ` marker and nothing else.
    xmark = (task == "xmark")
    judged = "xor" if xmark else task
    mark = _BP_MARK[judged] if xmark else ""
    panel = _bp_items(K, _BP_VERB_HELD, _BP_NOUN_HELD, rot, lengths=lengths, task=judged, mark=mark)
    # The drill sweeps EVERY rotation so all 8 seen verbs and all 8 seen nouns are exercised in
    # every slot. One rotation would teach the rule at 6 lexemes and leave "it memorised those six"
    # as a live alternative to "it learned the operation" (corpus-py-1 (E): count the axis).
    # Under xmark the SAME sweep runs once per marked sub-task, so the h/p supervision covers
    # exactly the lexemes/slots the x lines do — never a different distribution.
    drill_tasks = ("hp", "pos", "xor") if xmark else (task,)
    seen = []
    for t in drill_tasks:
        for r in range(len(_BP_VERB_SEEN)):
            seen.extend(_bp_items(K, _BP_VERB_SEEN, _BP_NOUN_SEEN, rot + r, lengths=lengths,
                                  task=t, mark=(_BP_MARK[t] if xmark else "")))
    rng = random.Random(seed)
    order = list(range(len(seen)))
    lines = []
    while len(lines) < n_blocks:
        rng.shuffle(order)
        for i in order:
            if len(lines) >= n_blocks:
                break
            it = seen[i]
            lines.append(it["surface"] + it["gold_pattern"])
    text = "\n".join(lines) + "\n"

    # 0-SHOT audit, word-boundary (never substring — `art` nests in `start`; corpus-py-1 (G)).
    words = set()
    for tok in re.split(r"\s+", text):
        if tok:
            words.add(tok)
    held_forms = set()
    for v in _BP_VERB_HELD:
        held_forms.add(v + "s"); held_forms.add(v + "ing")
    for nn_ in _BP_NOUN_HELD:
        held_forms.add(nn_); held_forms.add(nn_ + "s")
    leaks = sorted(held_forms & words)

    codebook = {"panel": "bindpanel-K%d" % K,
                "slots": ["s%d" % k for k in range(K)],
                "codewords": [it["gold_bits"] for it in panel]}
    aud = _bp_audit(panel, K)
    # Under xmark the drill INTENTIONALLY mixes three tasks, so a pooled drill audit reads
    # presence=1.0 on the h lines etc. That is the design, not a leak — auditing the pooled mix
    # would print an alarming number for a corpus that is behaving exactly as specified. Audit the
    # JUDGED stratum (the x lines) instead, which is the one comparable to the panel, and record
    # the mix explicitly so nobody later reads this field as if it covered the whole drill.
    _judged_seen = [it for it in seen if it.get("task", "xor") == judged]
    aud_seen = _bp_audit(_judged_seen, K)
    st = {"K": K, "lang": lang, "seed": seed, "rot": rot,
          "task": task, "judged_task": judged, "panel_mark": mark,
          # H_9818 census — the drill's task mix, counted not assumed (corpus-py-1 (E)/(F)):
          # `audit_drill` above covers ONLY the judged stratum, so this is where a reader sees
          # that h/p supervision lines exist and how many distinct source items each task got.
          "drill_task_mix": {t: sum(1 for it in seen if it.get("task", "xor") == t)
                             for t in drill_tasks},
          "n_panel": len(panel), "n_drill_lines": len(lines),
          "bytes": len(text.encode()), "leaks": leaks,
          "audit_panel": aud, "audit_drill": aud_seen,
          "held_lexemes": {"verbs": _BP_VERB_HELD, "nouns": _BP_NOUN_HELD},
          "seen_lexemes": {"verbs": _BP_VERB_SEEN, "nouns": _BP_NOUN_SEEN}}
    return text, panel, codebook, st


def _cd_name_pool(n_total):
    """CVCVC nonce pool with every reserved-literal collider REMOVED, stride-sampled to n_total.

    Sorted + filtered + sliced => the pools are a pure function of n_total (seed-independent),
    exactly like _sb_entity_pool. The filter is not cosmetic: `samek` is a legal CVCVC name that
    CONTAINS the role literal `same`, which would make both the 0-shot substring leak witness and
    the eval-time carrier audit read a false hit."""
    names = []
    for c0 in _SB_CONSONANTS:
        for v0 in _SB_VOWELS:
            for c1 in _SB_CONSONANTS:
                for v1 in _SB_VOWELS:
                    for c2 in _SB_CONSONANTS:
                        nm = c0 + v0 + c1 + v1 + c2
                        if any(r in nm or nm in r for r in _CD_RESERVED):
                            continue
                        names.append(nm)
    names = sorted(set(names))
    if len(names) < n_total:
        raise SystemExit("counterfactual-decl: nonce pool %d < requested %d" % (len(names), n_total))
    step = (len(names) - 1) / float(n_total - 1)
    return [names[int(round(i * step))] for i in range(n_total)]


def _cd_decl_line(name, sense_bit):
    return "%s means %s ." % (name, _CD_SENSE[sense_bit])


def _cd_op_line(name, role_bit):
    return "%s acts %s ." % (name, _CD_ROLE[role_bit])


def _cd_carrier(op_name, stem_name):
    """The query carrier. Contains the two NAMES and nothing else — no answer token, no label."""
    return "%s %s => " % (op_name, stem_name)


def _cd_answer_bit(sense_bit, role_bit):
    """The ONLY rule in the format: compose the stem declaration with the operator declaration."""
    return sense_bit ^ role_bit


def _cd_episode(rng, stem_slots, op_slots):
    """Render one episode. stem_slots = [(name, sense_bit)] · op_slots = [(name, role_bit)].

    Declaration order is shuffled (so position never encodes the value) and every (stem, op)
    pair is queried exactly once in shuffled order. Because each stem meets exactly one `same`
    and one `flip` operator, its two answers are {aye, nay} — polarity balance is structural."""
    decl = [_cd_decl_line(nm, sb) for nm, sb in stem_slots]
    rng.shuffle(decl)
    ops = [_cd_op_line(nm, rb) for nm, rb in op_slots]
    rng.shuffle(ops)
    qs = [(o_nm, o_rb, s_nm, s_sb) for o_nm, o_rb in op_slots for s_nm, s_sb in stem_slots]
    rng.shuffle(qs)
    q_lines = [_cd_carrier(o_nm, s_nm) + _CD_ANSWER[_cd_answer_bit(s_sb, o_rb)]
               for o_nm, o_rb, s_nm, s_sb in qs]
    return decl + ops, q_lines, qs


def _cd_derangement(n, rng, values, q):
    """A derangement pi of the n declaration slots, preferring one where the QUERIED slot receives
    a value OPPOSITE to its own.

    This permutation is the whole value-shuffle control. Applying shuf[i] = values[pi[i]] with pi a
    derangement makes the QUERIED slot's declaration WORLD-INVARIANT: the queried slot q shows
    values[pi[q]] and pi[q] != q, so flipping the queried stem's true sense changes the declaration
    of slot pi^-1(q) instead — the SAME number of bytes move, the key set and the value multiset are
    identical, only the key<->value correspondence is broken. A grounded reader therefore loses its
    flip signal here while every surface statistic is matched (control-must-match-mediating-covariate).

    Returns (pi, opposite_ok). opposite_ok=False is recorded, never silently accepted."""
    for _ in range(256):
        idx = list(range(n))
        # Sattolo's algorithm: a single n-cycle, hence a derangement by construction.
        for i in range(n - 1, 0, -1):
            j = rng.randrange(i)
            idx[i], idx[j] = idx[j], idx[i]
        pi = [0] * n
        for i in range(n):
            pi[i] = idx[i]
        if any(pi[i] == i for i in range(n)):      # defensive: Sattolo cannot produce a fixed point
            continue
        if values[pi[q]] != values[q]:
            return pi, True
    return pi, False


def _cd_eval_entry(rng, stratum, stem_slots, op_slots, q_index, ep_id):
    """One fully-rendered eval item: every arm's CONTEXT is materialised here, in the builder that
    owns the grammar, so the evaluator never re-implements the renderer (a second renderer is a
    format-drift bug waiting to happen — evaluate.py re-derives the gold and audits the carrier
    instead, which is a check, not a duplicate)."""
    decl_order = list(range(len(stem_slots)))
    rng.shuffle(decl_order)
    op_order = list(range(len(op_slots)))
    rng.shuffle(op_order)
    op_name, role_bit = op_slots[q_index[0]]
    stem_name, sense_bit = stem_slots[q_index[1]]
    q = q_index[1]
    values = [sb for _, sb in stem_slots]
    pi, opp_ok = _cd_derangement(len(stem_slots), rng, values, q)

    def render(sense_of):
        lines = [_cd_decl_line(stem_slots[i][0], sense_of(i)) for i in decl_order]
        lines += [_cd_op_line(op_slots[i][0], op_slots[i][1]) for i in op_order]
        return "\n".join(lines) + "\n"

    flipped = [sb for sb in values]
    flipped[q] = 1 - flipped[q]
    ctx_a = render(lambda i: values[i])
    ctx_b = render(lambda i: flipped[i])
    ctx_shuf_a = render(lambda i: values[pi[i]])
    ctx_shuf_b = render(lambda i: flipped[pi[i]])
    # declaration-drop: the QUERIED stem's declaration is removed in BOTH worlds, so the two
    # contexts become byte-identical and flip-sensitivity is 0 MECHANICALLY (not statistically).
    # That is the point: it is the instrument's own null, and if it ever reads != 0 the harness
    # is broken (evaluate.py turns the run INSTRUMENT-DEAD on that).
    drop_lines = [_cd_decl_line(stem_slots[i][0], values[i]) for i in decl_order if i != q]
    drop_lines += [_cd_op_line(op_slots[i][0], op_slots[i][1]) for i in op_order]
    ctx_drop = "\n".join(drop_lines) + "\n"
    gold = _cd_answer_bit(sense_bit, role_bit)
    return {
        "stratum": stratum, "episode": ep_id,
        "op": op_name, "stem": stem_name, "role_bit": role_bit, "sense_bit": sense_bit,
        "carrier": _cd_carrier(op_name, stem_name),
        "gold": _CD_ANSWER[gold], "gold_flip": _CD_ANSWER[1 - gold],
        "gold_bit": gold,
        "answers": [_CD_ANSWER[0], _CD_ANSWER[1]],          # indexed by answer_bit
        "ctx": {"live_a": ctx_a, "live_b": ctx_b,
                "value-shuffle_a": ctx_shuf_a, "value-shuffle_b": ctx_shuf_b,
                "declaration-drop_a": ctx_drop, "declaration-drop_b": ctx_drop},
        "perm": pi, "perm_opposite": opp_ok,
        "store": {"entities": [nm for nm, _ in stem_slots], "pols": values},
        "target_slot": q,
    }


def _cd_audit_counts(rows):
    """Per-class counts + the chance level DERIVED from the realized split.

    chance = the MAJORITY share of the realized labels, i.e. the accuracy of the best constant
    predictor on THIS split. Never 0.5-by-assumption: a uniform pedestal that happens to coincide
    with 1/K is exactly how a defect hides (chance-level-must-be-derived-per-metric)."""
    n = len(rows)
    c = collections.Counter(rows)
    return {"n": n, "counts": dict(sorted(c.items())),
            "chance_majority": (max(c.values()) / float(n)) if n else None,
            "balanced_exact": (len(c) == 2 and len(set(c.values())) == 1)}


def build_counterfactual_decl(n_blocks, stems_per_ep, seed, lang, held_stems, held_ops,
                              n_rot_stems=192, n_frozen_stems=64, n_rot_ops=24, n_frozen_ops=8,
                              n_eval_episodes=16):
    """Build the H_9800 ephemeral-declaration corpus + eval manifest + store surface.

    Returns (text, st). Hard-fails (never a silent downgrade) on: non-EN, a stems-per-episode that
    cannot be balanced 4 ways, a pool shortfall, or a 0-shot leak."""
    if lang != "en":
        raise SystemExit("counterfactual-decl is EN-only (--lang en): the role words are FREE "
                         "pre-posed tokens, so operator identity is never confounded with "
                         "morphology (CLAUDE.md EN-FIRST · the ko lane is BINDING)")
    S = int(stems_per_ep)
    if S < 4 or S % 4 != 0:
        raise SystemExit("counterfactual-decl: --stems-per-episode must be >=4 and a multiple of 4 "
                         "(half rotating / half frozen, each half sense-balanced); got %d" % S)
    if n_frozen_stems % 2 or n_frozen_ops % 2:
        raise SystemExit("counterfactual-decl: frozen pools must be even (fixed-good/fixed-harm "
                         "and fixed-same/fixed-flip halves)")
    for nm, v in (("--held-out I (stems)", held_stems), ("--held-out J (operators)", held_ops)):
        if v < S // 2 if nm.startswith("--held-out I") else v < 2:
            raise SystemExit("counterfactual-decl: %s = %d is too small to fill an eval episode "
                             "(need >= %d)" % (nm, v, S // 2 if nm.startswith("--held-out I") else 2))

    n_stem_names = n_rot_stems + n_frozen_stems + held_stems
    n_op_names = n_rot_ops + n_frozen_ops + held_ops
    pool = _cd_name_pool(n_stem_names + n_op_names)
    stem_names, op_names = pool[:n_stem_names], pool[n_stem_names:]
    rot_stems = stem_names[:n_rot_stems]
    frozen_stems = stem_names[n_rot_stems:n_rot_stems + n_frozen_stems]
    heldout_stems = stem_names[n_rot_stems + n_frozen_stems:]
    rot_ops = op_names[:n_rot_ops]
    frozen_ops = op_names[n_rot_ops:n_rot_ops + n_frozen_ops]
    heldout_ops = op_names[n_rot_ops + n_frozen_ops:]
    # frozen MAPPINGS: fixed for the whole corpus, so their ANTI mapping is a mapping the corpus
    # never contains even though every byte of the name is seen thousands of times.
    fz_good = frozen_stems[:n_frozen_stems // 2]
    fz_harm = frozen_stems[n_frozen_stems // 2:]
    fz_same = frozen_ops[:n_frozen_ops // 2]
    fz_flip = frozen_ops[n_frozen_ops // 2:]
    fz_sense = {nm: 1 for nm in fz_good}
    fz_sense.update({nm: 0 for nm in fz_harm})
    fz_role = {nm: 0 for nm in fz_same}
    fz_role.update({nm: 1 for nm in fz_flip})

    rng = random.Random(seed)
    lines, store_rows = [], []
    for ep in range(n_blocks):
        half = S // 2
        rot_pick = rng.sample(rot_stems, half)
        rot_sense = [1] * (half // 2) + [0] * (half - half // 2)
        rng.shuffle(rot_sense)
        fz_pick = ([(nm, 1) for nm in rng.sample(fz_good, half // 2)]
                   + [(nm, 0) for nm in rng.sample(fz_harm, half - half // 2)])
        stem_slots = list(zip(rot_pick, rot_sense)) + fz_pick
        rng.shuffle(stem_slots)
        if ep % 2 == 0:                                   # rotating operator names, roles re-drawn
            o_pick = rng.sample(rot_ops, 2)
            roles = [0, 1]
            rng.shuffle(roles)
            op_slots = list(zip(o_pick, roles))
        else:                                             # frozen operator names at their fixed role
            op_slots = [(rng.choice(fz_same), 0), (rng.choice(fz_flip), 1)]
        rng.shuffle(op_slots)
        decl_lines, q_lines, qs = _cd_episode(rng, stem_slots, op_slots)
        lines.extend(decl_lines)
        lines.extend(q_lines)
        # store surface (line-aligned, query lines only — see the .storelines note in main()):
        # the DECLARATION bytes are what charge the store's key/value: entities = the episode's
        # declared stems, pols = their declared senses, target_slot = the queried key. The operator
        # declaration rides the prompt text, mirroring storebind's "store holds the FACT, text the
        # OPERATOR" contract so the co-trained CLMS/pairodd lane can consume this unchanged.
        slot_of = {nm: i for i, (nm, _) in enumerate(stem_slots)}
        for o_nm, o_rb, s_nm, s_sb in qs:
            prompt = _cd_op_line(o_nm, o_rb) + " " + _cd_carrier(o_nm, s_nm)
            store_rows.append({"prompt": prompt, "gold": _CD_ANSWER[_cd_answer_bit(s_sb, o_rb)],
                               "entity": s_nm,
                               "store": {"entities": [nm for nm, _ in stem_slots],
                                         "pols": [sb for _, sb in stem_slots]},
                               "target_slot": slot_of[s_nm], "op": o_rb})

    text = "\n".join(lines) + "\n"

    # ---- 0-shot leak witness (hard-assert, both surfaces). Names are all 5 ascii chars and always
    # space-delimited, so a substring hit is an exact-token hit; a leak aborts the build.
    blob = text
    leaked = sorted([e for e in heldout_stems + heldout_ops if e in blob])
    if leaked:
        raise SystemExit("counterfactual-decl: 0-shot LEAK — %d held-out name(s) present in the "
                         "corpus: %s" % (len(leaked), leaked[:5]))

    # ---- eval manifest. Five strata: one positive-control stratum (seen bytes, fresh mapping) and
    # four hold-out axes — bytes (stem / operator) AND mappings (frozen stem shown at its ANTI
    # sense / frozen operator shown at its ANTI role). The mapping strata are the reason this split
    # is not "just stems": their bytes are fully trained, only the assignment is novel.
    entries = []
    ev_rng = random.Random(seed + 90011)
    half = S // 2

    def _pick_stems(kind):
        if kind == "seen":
            picks = ev_rng.sample(rot_stems, S)
            sense = [1] * (S // 2) + [0] * (S - S // 2)
            ev_rng.shuffle(sense)
            return list(zip(picks, sense))
        if kind == "heldout-stem":
            picks = ev_rng.sample(heldout_stems, S)
            sense = [1] * (S // 2) + [0] * (S - S // 2)
            ev_rng.shuffle(sense)
            return list(zip(picks, sense))
        if kind == "anti-map":                            # frozen stems at the ANTI sense
            g = ev_rng.sample(fz_good, S // 2)
            h = ev_rng.sample(fz_harm, S - S // 2)
            return [(nm, 0) for nm in g] + [(nm, 1) for nm in h]
        raise SystemExit("counterfactual-decl: unknown eval stem kind %r" % kind)

    def _pick_ops(kind):
        if kind == "seen":
            o = ev_rng.sample(rot_ops, 2)
            r = [0, 1]
            ev_rng.shuffle(r)
            return list(zip(o, r))
        if kind == "heldout-op":
            o = ev_rng.sample(heldout_ops, 2)
            r = [0, 1]
            ev_rng.shuffle(r)
            return list(zip(o, r))
        if kind == "anti-role":                           # frozen operators at the ANTI role
            return [(ev_rng.choice(fz_same), 1), (ev_rng.choice(fz_flip), 0)]
        raise SystemExit("counterfactual-decl: unknown eval op kind %r" % kind)

    STRATA = (("seen", "seen", "seen"),
              ("heldout-stem", "heldout-stem", "seen"),
              ("heldout-op", "seen", "heldout-op"),
              ("heldout-map-stem", "anti-map", "seen"),
              ("heldout-map-op", "seen", "anti-role"))
    for name, s_kind, o_kind in STRATA:
        for ep in range(n_eval_episodes):
            stem_slots = _pick_stems(s_kind)
            ev_rng.shuffle(stem_slots)
            op_slots = _pick_ops(o_kind)
            ev_rng.shuffle(op_slots)
            for oi in range(len(op_slots)):
                for si in range(len(stem_slots)):
                    entries.append(_cd_eval_entry(ev_rng, name, stem_slots, op_slots,
                                                  (oi, si), ep))
    manifest = {"schema": "anima-counterfactual-decl/v1", "lang": lang, "seed": seed,
                "stems_per_episode": S, "answers": [_CD_ANSWER[0], _CD_ANSWER[1]],
                "sense_labels": [_CD_SENSE[0], _CD_SENSE[1]],
                "role_labels": [_CD_ROLE[0], _CD_ROLE[1]],
                "arms": ["live", "declaration-drop", "value-shuffle"],
                "strata": [s[0] for s in STRATA], "entries": entries}
    st = {"lang": lang, "seed": seed, "n_blocks": n_blocks, "stems_per_ep": S,
          "lines": len(lines), "bytes": len(text.encode("ascii")),
          "n_rot_stems": len(rot_stems), "n_frozen_stems": len(frozen_stems),
          "n_heldout_stems": len(heldout_stems), "n_rot_ops": len(rot_ops),
          "n_frozen_ops": len(frozen_ops), "n_heldout_ops": len(heldout_ops),
          "leak": 0, "manifest": manifest, "store_rows": store_rows,
          "n_eval_episodes": n_eval_episodes}
    return text, st


def audit_counterfactual_decl(corpus_path, st):
    """Re-parse the corpus FROM DISK and derive the polarity audit from what was actually written.

    Deliberately independent of the generator's internal counters: the balance claim is only worth
    anything if it is measured on the emitted bytes (instrument-never-run-hides-multiple-bugs). Any
    imbalance aborts — a corpus whose classes are not exactly balanced silently moves the chance
    level of every downstream bar."""
    raw = open(corpus_path, "r", encoding="ascii").read()
    q_ans, by_role, by_sense, decl_sense, decl_role = [], {}, {}, [], []
    for ln in raw.split("\n"):
        if not ln:
            continue
        if " => " in ln:
            ans = ln.rsplit(" => ", 1)[1]
            q_ans.append(ans)
        elif " means " in ln:
            decl_sense.append(ln.split(" means ", 1)[1].split(" ")[0])
        elif " acts " in ln:
            decl_role.append(ln.split(" acts ", 1)[1].split(" ")[0])
    bad = sorted({a for a in q_ans if a not in _CD_ANSWER.values()})
    if bad:
        raise SystemExit("counterfactual-decl audit: unparseable answer token(s) %s" % bad[:5])
    # carrier audit (invariant ① re-measured on disk): no query carrier may contain an answer token
    # or a label name — that would install the operator->answer map and make the task answerable
    # without composing the declaration.
    banned = tuple(_CD_ANSWER.values()) + tuple(_CD_SENSE.values()) + tuple(_CD_ROLE.values())
    carrier_hits = 0
    for ln in raw.split("\n"):
        if " => " in ln:
            carrier = ln.rsplit(" => ", 1)[0] + " => "
            if any(b in carrier for b in banned):
                carrier_hits += 1
    if carrier_hits:
        raise SystemExit("counterfactual-decl audit: %d carrier(s) contain an answer/label token "
                         "(arbitrary grounding — the map would be installed by the carrier)"
                         % carrier_hits)
    ans_audit = _cd_audit_counts(q_ans)
    if not ans_audit["balanced_exact"]:
        raise SystemExit("counterfactual-decl audit: polarity NOT exactly balanced on the emitted "
                         "corpus: %s" % ans_audit["counts"])
    per_stratum = {}
    for e in st["manifest"]["entries"]:
        per_stratum.setdefault(e["stratum"], []).append(e["gold"])
    audit = {
        "schema": "anima-counterfactual-decl-audit/v1",
        "corpus": corpus_path,
        "verified_from": "re-parse of the corpus file on disk (not the generator's counters)",
        "lines": len([x for x in raw.split("\n") if x]),
        "bytes": len(raw.encode("ascii")),
        "answer": ans_audit,
        "declared_sense": _cd_audit_counts(decl_sense),
        "declared_role": _cd_audit_counts(decl_role),
        "chance_note": ("chance = the realized MAJORITY share (accuracy of the best constant "
                        "predictor on THIS split), derived per metric — never assumed 0.5. "
                        "flip-sensitivity has a STRUCTURAL chance of 0.0 because the carrier is "
                        "byte-identical across the flip, so a declaration-independent deterministic "
                        "policy cannot flip; the empirical floor is the control arms."),
        "flip_chance_structural": 0.0,
        "eval": {k: _cd_audit_counts(v) for k, v in sorted(per_stratum.items())},
        "leak_heldout_names_in_corpus": st["leak"],
    }
    return audit


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


# ---------------------------------------------------------------------------------------------------
# H_9410 RULE-VS-CACHE PRESSURE ENVELOPE — scaled EN atom miner + random balanced polarity.
#
# The hand-built 48-atom set (H_9389) does not scale, and human sentiment annotation of 10^3 stems is
# infeasible. The escape is that a FROM-SCRATCH model never read real usage, so an atom's REAL polarity
# is functionless — the model only ever sees the polarity we WRITE next to it. So we assign polarity at
# RANDOM (balanced, deterministic in --assign-seed): mining needs no sentiment labels, G-BALANCE holds
# by construction, and any form->polarity leak (a real adjective's surface predicting its sentiment) is
# killed because the label is decoupled from the word. This is the strongest confound control the
# envelope has, not a shortcut.
#
# The gates are the SAME verdicts-that-already-died as build_atoms, but at scale G-SUBSTR must be GREEDY
# (freq-order, DROP a colliding candidate rather than SystemExit — at N=3072 substring collisions like
# care/careful are the norm, and aborting would make the set un-buildable). Occurrence is word-BOUNDARY
# (corpus-py-1 (G): `text.count` lies in English — mine_lexicon already tokenises word-level, so its occ
# is clean). We report where the corpus DRIES UP — that count IS the axis-1 ceiling, not a failure.
def _assign_balanced_polarity(stems, assign_seed):
    """RANDOM balanced polarity over a stem set, deterministic in assign_seed and ORDER-INDEPENDENT.

    Sort first (so the assignment is a pure function of the SET + seed, not the mining order), shuffle
    under assign_seed, front half -> pos(1), rest -> neg(0). Balanced within 1 for an odd count.
    """
    s = sorted(set(stems))
    random.Random(assign_seed).shuffle(s)
    half = len(s) // 2
    return {st: (1 if i < half else 0) for i, st in enumerate(s)}


_EN_STOP = {
    # frequent non-content words a degree-adverb frame can still admit ("very much", "so many"…) —
    # excluded so the atom set is content stems, not function words. Kept small + explicit (auditable).
    "much", "many", "more", "most", "some", "such", "very", "well", "even", "ever", "also", "than",
    "then", "them", "they", "this", "that", "these", "those", "there", "here", "what", "when", "where",
    "which", "while", "about", "would", "could", "should", "still", "just", "only", "same", "other",
    "with", "from", "into", "onto", "over", "under", "your", "their", "been", "being", "have", "does",
}


def build_atoms_scaled(corpus_paths, lang, n_atoms, min_occ, assign_seed, mine_top=0):
    """One-shot: mine n_atoms clean EN polarity stems by frequency, GREEDY gates, RANDOM balanced pol.

    Returns (obj, stats) with the SAME schema as build_atoms so xbind --bridge-split / ground consume
    it unchanged. `stats["dried_up"]` is True iff the corpus ran out before n_atoms — the actual count
    reached is the axis-1 ceiling and is reported, never silently padded.
    """
    if lang == "ko":
        raise SystemExit("anima corpus atoms --max-atoms: --lang ko is refused (frozen atom set). "
                         "The scaled miner is for EN (owner EN-FIRST directive).")
    L = lang_pack(lang)
    # frame/label tokens the scorer reads — a stem colliding with any of these corrupts the span (G-CARRIER)
    frame = set()
    for tok in re.findall(r"[A-Za-z]+", L["tmpl"] + "".join(L["flip0"]) + "".join(L["flip1"])):
        if tok not in ("s", "surf", "pol"):
            frame.add(tok.lower())
    frame |= {L["pos"].lower(), L["neg"].lower()}

    top = mine_top or max(n_atoms * 5, 5000)     # headroom: ~50-70% survive the greedy gates
    cand, mst = mine_lexicon(corpus_paths, lang, top, min_occ)

    def _is_deriv(a, b):                          # a is an affix-negation/-derivation of b (either order)
        for x, y in ((a, b), (b, a)):
            for pre in ("un", "in", "im", "dis", "non", "ir", "il"):
                if x.startswith(pre) and x[len(pre):] == y:
                    return True
            if x.endswith("less") and x[:-4] == y:
                return True
            if x.endswith("ful") and x[:-3] == y:
                return True
        return False

    accepted, seen = [], set()
    dropped = {"len": 0, "stop": 0, "carrier": 0, "substr": 0, "deriv": 0}
    for c in cand:                               # freq-rank order — the designer does not pick
        st = c["stem"]
        if not (5 <= len(st.encode()) <= 9):     # length band (bytes; EN alpha = 1 B/char)
            dropped["len"] += 1; continue
        if st in _EN_STOP:
            dropped["stop"] += 1; continue
        if st in frame:
            dropped["carrier"] += 1; continue
        if any(st in a or a in st for a in seen):  # G-SUBSTR greedy — drop, do not abort
            dropped["substr"] += 1; continue
        if any(_is_deriv(st, a) for a in seen):    # G-DERIV — no double-negation lookup escape
            dropped["deriv"] += 1; continue
        accepted.append(st); seen.add(st)
        if len(accepted) >= n_atoms:
            break
    dried = len(accepted) < n_atoms

    pol_map = _assign_balanced_polarity(accepted, assign_seed)
    stems = [(st, pol_map[st]) for st in accepted]
    # balanced train/heldout split (schema compatibility — xbind --bridge-split re-splits over ALL atoms
    # by its own --split-seed and ignores this field; ground/valence formats read it).
    pos = [st for st, p in stems if p == 1]
    neg = [st for st, p in stems if p == 0]
    rng = random.Random(assign_seed + 7); rng.shuffle(pos); rng.shuffle(neg)
    n = len(stems); n_held = n // 4; n_seen = n - n_held
    out, pi, ni = [], 0, 0
    for split, k in (("train", n_seen), ("heldout", n_held)):
        for j in range(k):
            take_pos = (j % 2 == 0 and pi < len(pos)) or ni >= len(neg)
            if take_pos and pi < len(pos):
                out.append({"stem": pos[pi], "pol": 1, "split": split}); pi += 1
            elif ni < len(neg):
                out.append({"stem": neg[ni], "pol": 0, "split": split}); ni += 1
    stats = {"lang": lang, "requested": n_atoms, "accepted": len(accepted), "dried_up": dried,
             "frame_candidates": mst["frame_candidates"], "mined_kept": mst["kept"],
             "min_occ": min_occ, "assign_seed": assign_seed, "dropped": dropped,
             "n_pos": len(pos), "n_neg": len(neg), "n_train": n_seen, "n_heldout": n_held,
             "chance_sd_gate": round(0.5 / max(1, (n // 4)) ** 0.5, 4)}
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


def build(fmt, S, KW, held_out, comp_per_pair, single_per_concept, seed, held_out_frac=0.0):
    """Return the corpus text for one format arm (deriv or flat).

    held_out_frac (H_9643): withhold this fraction of the UNORDERED pair grid from training
    instead of the single `held_out` cell. 0.0 keeps the legacy single-pair corpus byte-for-byte.
    The withheld set ALWAYS contains `held_out` (the manifest's scored pair) and is drawn with a
    split-seeded RNG that is independent of the content RNG, so the same corpus seed with a
    different fraction differs only in coverage — not in wording.
    """
    rng = random.Random(seed)
    n = len(S)
    held = frozenset(held_out)
    held_set = {held}
    if held_out_frac > 0.0:
        all_un = [frozenset((i, j)) for i in range(n) for j in range(i + 1, n)]
        k = int(round(held_out_frac * len(all_un)))
        # split RNG is derived from the content seed but kept SEPARATE: changing the fraction must
        # not reshuffle the wording, or the arms would differ on two axes at once.
        srng = random.Random(seed * 7919 + 13)
        pool = [u for u in all_un if u != held]
        srng.shuffle(pool)
        held_set = {held} | set(pool[:max(k - 1, 0)])
    train_pairs = [(i, j) for i in range(n) for j in range(n)
                   if i != j and frozenset((i, j)) not in held_set]

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
# A budget floor is EARNED on one corpus, in one language. Keying it by format alone silently
# transplants it (bar-derived-not-transplanted): an `en` ground_keep would have picked up the number
# H_9324 measured on the KOREAN corpus and the trainer would have enforced it as if it were derived.
# So the key is (lang, fmt), and a floor that has NOT been measured for a language says so out loud
# instead of pretending.
BUDGET_FLOORS = {
    # (lang, fmt): (min_steps, min_lr, note)
    ("ko", "ground_keep"): (
        6000, 2e-4,
        "H_9324 (ko, MEASURED): WRITE 0.4483 (600@5e-5 = chance) -> 0.9540 (6000@2e-4) -> 1.0000 "
        "(6000@5e-4), reproduced on 2 seeds. Below this floor a negative result is a BUDGET "
        "negative, not a substrate negative — that is how H_9322 died."),
    ("ko", "ground_keep_lie"): (
        6000, 2e-4, "same floor as ko/ground_keep — it is the matched control arm."),
    # en: NOT measured. The number below is the ko floor used as a STARTING POINT, and the meta says
    # so; the trainer warns rather than enforcing a bar nobody earned. What actually decides whether
    # the budget sufficed is the WRITE gate (held-out flip0) measured on the resulting ckpt — and if
    # WRITE fails, raising the budget is NOT tune-to-green: asking a model to COMPOSE a fact it never
    # stored is exactly how H_9322 died.
    ("en", "ground_keep"): (
        6000, 2e-4,
        "⚠️ TRANSPLANTED from ko (H_9324), NOT measured for en. Use as a starting point only — the "
        "WRITE gate (held-out flip0) on the resulting ckpt is what actually decides whether the "
        "budget sufficed. Raising it after a WRITE failure is not tune-to-green; WRITE is a "
        "PREMISE, not the DV."),
    ("en", "ground_keep_lie"): (
        6000, 2e-4, "⚠️ TRANSPLANTED from ko — same caveat as en/ground_keep."),
}

# Strata a FORGET gate MUST read for this corpus — specifically the ones the corpus contains ZERO
# of, because those are exactly what dies (convergence corpus-py-1 (A)/(7)). A FORGET gate that
# only reads the stratum the corpus reinforces is structurally always-pass = a forged gate.
FORGET_STRATA = {
    "ground":          ["SEEN flip0", "SEEN flip1 (ZERO in this corpus — this is what dies)"],
    "ground_lie":      ["SEEN flip0", "SEEN flip1 (ZERO in this corpus — this is what dies)"],
    "ground_keep":     ["SEEN flip0", "SEEN flip1 (replayed — verify it SURVIVES, bar 0.75)"],
    "ground_keep_lie": ["SEEN flip0", "SEEN flip1 (replayed — verify it SURVIVES, bar 0.75)"],
    # H_9520 study-replay — corpus-py-1 ⑦ (A): the FORGET gate MUST cover strata ABSENT from the
    # study corpus, because those are exactly the ones a small-corpus CPT kills. The teacher content
    # is general prose (reinforces ρ·form fluency); it does NOT reinforce the specialised reach axes,
    # so `anima-py evaluate --rho-axon` on the post-CPT ckpt must show these do NOT drop vs the pre-CPT
    # floor. A study-only forget check (ρ·form alone) is a forgery — it is the ONE stratum the corpus
    # reinforces, so it always passes while the untouched axes are the ones that die.
    "study-replay":    ["ρ·form (reinforced — expected to rise; NOT the forget gate)",
                        "ρ·weave (recombination — NOT reinforced · verify no drop)",
                        "ρ·tether (truth-bind — NOT reinforced · verify no drop)",
                        "ρ·store · ρ·self (recall/identity — NOT reinforced · verify no drop)"],
}


def _write_budget_floor(out_path, fmt, lang=DEFAULT_LANG):
    """Emit `<out>.meta.json` beside the corpus. NOT inside it — this is a byte-LM, so a header
    comment in the corpus file would be TRAINED ON."""
    floor = BUDGET_FLOORS.get((lang, fmt))
    transplanted = bool(floor) and floor[2].startswith("⚠️ TRANSPLANTED")
    meta = {
        "format": fmt,
        "lang": lang,
        "floor_transplanted": transplanted,
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
    elif floor and transplanted:
        print("  [budget-meta] %s.meta.json — ⚠️ floor steps>=%d lr>=%g is TRANSPLANTED from ko, "
              "NOT measured for '%s'. It is a starting point; the WRITE gate on the resulting ckpt "
              "is what decides." % (out_path, floor[0], floor[1], lang))
    elif floor:
        print("  [budget-meta] %s.meta.json — earned floor: steps>=%d lr>=%g (measured for '%s')"
              % (out_path, floor[0], floor[1], lang))


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


# ---------------------------------------------------------------------------
# routeaudit — H_9355 LOCUS-CAUSAL manifest. Do the declarative lane and the operator lane
# live on DIFFERENT ConvMoE experts?
#
# Every surface below is copied VERBATIM from the frozen H_9327/C4 eval manifest — a template
# rebuild would hand the model a string it never saw (that is how the negS carrier bit the
# BIND-LOCUS lane), so the seeds are inherited, never re-derived.
#
#   flip0  이 영화 {s}고 => e         the DECLARATIVE surface — the lane CPT writes into (WRITE 0.98)
#   negL   이 영화 {s}지 않다 => e     the OPERATOR surface, strong #1
#   negZ   이 영화 별로 {s}지 않다 => e the OPERATOR surface, strong #2
#   negJ   이 영화 {s}지는 않다 => e    string-twin of negL where the OPERATOR DOES NOT RUN (C1b p~.50)
#                                     -> control ①b: a route shift that also shows up here is a
#                                        STRING effect, not an operator effect
#   ped    이 영화 {s}고 있다 => e      PEDESTAL: an inert 10-byte suffix, byte-length-matched to
#                                     negL's '지 않다' (10 B), carrying no negation at all
#                                     -> control ①: "does ANY suffix move the route"
#
# The pedestal is what makes the DV readable at all. The router is a function of the byte string,
# so `flip0 -> negL` moves the route TRIVIALLY (the strings differ). The question is whether it
# moves MORE than an equally-long, semantically inert suffix does — which is a paired within-stem
# contrast, never a max() over controls (probe-defect-census-max-control-bias).
# ---------------------------------------------------------------------------
_ROUTE_SURFACES = (
    ("flip0", "이 영화 {s}고 => ", 0, "declarative — the lane CPT writes into"),
    ("negL",  "이 영화 {s}지 않다 => ", 1, "operator, strong"),
    ("negZ",  "이 영화 별로 {s}지 않다 => ", 1, "operator, strong"),
    ("negJ",  "이 영화 {s}지는 않다 => ", 1, "string-twin of negL, operator DOES NOT run (control)"),
    ("ped",   "이 영화 {s}고 있다 => ", 0, "pedestal — inert suffix, byte-matched to negL (control)"),
)


def build_routeaudit(atoms_path, win):
    """H_9355 route-audit manifest: every (stem x surface) prompt, tagged with split + the byte
    span of the stem inside the RIGHT-ALIGNED T-window the engine decodes.

    The span is computed the way `_seed_to_tok` right-aligns (last T bytes of the seed land at the
    window's tail) — a span computed on the raw seed instead would be off by (T - len(seed)) and
    would silently read the wrong positions (a_korean_byte_budget: ko = 3 B/char, so the offset is
    never 'about right')."""
    d = json.load(open(atoms_path))
    atoms = d["atoms"] if isinstance(d, dict) else d
    items = []
    for a in atoms:
        stem, pol = a["stem"], int(a["pol"])
        split = "seen" if a.get("split") == "train" else "heldout"
        for tag, tmpl, flip, _why in _ROUTE_SURFACES:
            seed = tmpl.format(s=stem)
            sb = seed.encode("utf-8")
            pre = tmpl.split("{s}")[0].encode("utf-8")           # bytes before the stem
            off = win - len(sb)                                  # right-align shift (may be <0)
            t0, t1 = off + len(pre), off + len(pre) + len(stem.encode("utf-8"))
            items.append({"id": "%s_%s_%s" % (split[0].upper(), stem, tag), "stem": stem,
                          "pol": pol, "split": split, "surf": tag, "flip": flip,
                          "seed": seed, "seed_bytes": len(sb), "stem_span": [t0, t1]})
    if any(it["stem_span"][0] < 0 for it in items):
        raise SystemExit("routeaudit: a seed is longer than the %d-byte window — the stem span "
                         "would fall outside it; raise --win" % win)
    return {"win": win, "surfaces": {t: m for t, m, _f, _w in _ROUTE_SURFACES}, "items": items}


# H_9361 TWIN-NECESSITY surfaces (ko). Each: (seed builder, prefix bytes before stem, carrier string).
# The carrier is the operator-morpheme window the SCREENER/instrument patches; prefix+stem+carrier+query
# are byte-identical between twins except the stem (option (A): byte-matched opposite-polarity stem).
_TWINNEC_SURF = {
    "flip1_suffix": (lambda s: "이 영화 %s지 않다 => " % s, "이 영화 ",   "지 않다"),   # 11B pre · 10B carrier
    "flip0":        (lambda s: "이 영화 %s고 => " % s,       "이 영화 ",   "고"),        # 11B pre ·  3B carrier
    "flip1_prefix": (lambda s: "이 영화 안 %s고 => " % s,    "이 영화 안 ", "고"),        # 15B pre ·  3B carrier
}


def build_twinnec(atoms_path, surface, seed):
    """H_9361 TWIN-NECESSITY candidate enumeration (torch-free · engine-native builder).

    SEEN stems only. Per byte-length bucket L, pair opposite-polarity stems (option (A): same carrier
    morpheme, byte-matched opposite-polarity STEM — the only on-manifold pairing the corpus supports;
    (B) is unbuildable, no 10B affirmative trained carrier). Emits the candidate manifest the SCREENER
    (`evaluate --twin-screen`) fills with base m̂, gates (sign==expected ∧ |m|>=1nat), and reduces to
    Y* + sd_w for the frozen n=9 stop-condition. Windows are RAW seed-byte offsets; the screener
    right-aligns to the decode window T (a_korean_byte_budget · like routeaudit/bindlocus)."""
    if surface not in _TWINNEC_SURF:
        raise SystemExit("twinnec: --surface must be one of %s" % ", ".join(_TWINNEC_SURF))
    mk, prefix, carrier = _TWINNEC_SURF[surface]
    negated = surface.startswith("flip1")
    d = json.load(open(atoms_path))
    atoms = d["atoms"] if isinstance(d, dict) else d
    seen = [a for a in atoms if a.get("split") == "train"]
    pfx_b, carr_b = len(prefix.encode("utf-8")), carrier.encode("utf-8")
    items = []
    for a in seen:
        stem, pol = a["stem"], int(a["pol"])
        L = len(stem.encode("utf-8"))
        s = mk(stem)
        t0 = pfx_b + L                                  # carrier start (raw seed bytes)
        t1 = t0 + len(carr_b)
        assert s.encode("utf-8")[t0:t1] == carr_b, "twinnec window byte-mismatch: %r %s" % (stem, surface)
        # expected m=logP(긍)-logP(부) sign. flip0 answer=긍 if pol==1 else 부 → +1 if pol==1 else -1.
        # flip1(negated) answer=부 if pol==1 else 긍 → -1 if pol==1 else +1.
        esign = (1 if pol == 1 else -1) * (-1 if negated else 1)
        items.append({"stem": stem, "pol": pol, "L": L, "seed": s, "seed_bytes": len(s.encode("utf-8")),
                      "carrier": [t0, t1], "esign": esign})
    # pair opposite polarity within each byte-length bucket
    buck = {}
    for it in items:
        buck.setdefault(it["L"], {0: [], 1: []})[it["pol"]].append(it["stem"])
    pairs = []
    for L in sorted(buck):
        pos, neg = buck[L][1], buck[L][0]
        for i in range(min(len(pos), len(neg))):
            pairs.append({"L": L, "A": pos[i], "B_opp": neg[i]})     # A=pol1, B_opp=pol0 (opposite)
    buckets = {str(L): [len(buck[L][0]), len(buck[L][1])] for L in sorted(buck)}
    return {"surface": surface, "prefix_bytes": pfx_b, "carrier": carrier, "carrier_bytes": len(carr_b),
            "seed": seed, "items": items, "pairs": pairs, "Y": len(pairs), "buckets": buckets,
            "note": "candidates only; base m̂ + gate + Y* + sd_w filled by `evaluate --twin-screen`"}


# ── H_9397 Δ-INJECT — option-(B) carrier-vs-filler twin manifest (byte-matched neutral filler) ──
# Unlike twinnec (option A: opposite-polarity STEM twins), here the twin axis IS the operator morpheme:
# same stem, {carrier `지 않다`} vs {neutral filler `고 있다`}. Both 10 B so the operator-site window (the
# carrier column the Δ is estimated at + injected on) is byte-aligned across the twin (a_korean_byte_budget).
# `게 되다` (also 10 B) = the same-class content control donor (a polarity-free real-runs direction).
_DELTAINJ_PREFIX = "이 영화 "                                   # 11 B
_DELTAINJ_CARRIER = "지 않다"                                   # 10 B — negation operator
_DELTAINJ_FILLER = "고 있다"                                    # 10 B — progressive, positive polarity, no operator
_DELTAINJ_FILLER2 = "게 되다"                                   # 10 B — inchoative, same-class content control


def build_deltainj(atoms_path):
    """H_9397 Δ-INJECT manifest — per stem, three byte-matched seeds sharing prefix+stem+query and
    differing only in the 10 B operator-site morpheme: carrier (negation) · filler (positive) · filler2
    (same-class control). Emits SEEN (Δ estimation + G-pos gate) and held-out (primary DV) items with the
    operator-site window in RAW seed-byte offsets (the handler right-aligns to the decode window T)."""
    pfx_b = len(_DELTAINJ_PREFIX.encode())
    cB = _DELTAINJ_CARRIER.encode(); fB = _DELTAINJ_FILLER.encode(); f2B = _DELTAINJ_FILLER2.encode()
    assert len(cB) == len(fB) == len(f2B) == 10, "deltainj morphemes must all be 10 B (byte-align)"
    d = json.load(open(atoms_path))
    atoms = d["atoms"] if isinstance(d, dict) else d
    items = []
    for a in atoms:
        stem, pol = a["stem"], int(a["pol"]); split = a.get("split", "train")
        L = len(stem.encode())
        carrier_seed = "%s%s%s => " % (_DELTAINJ_PREFIX, stem, _DELTAINJ_CARRIER)
        filler_seed = "%s%s%s => " % (_DELTAINJ_PREFIX, stem, _DELTAINJ_FILLER)
        filler2_seed = "%s%s%s => " % (_DELTAINJ_PREFIX, stem, _DELTAINJ_FILLER2)
        flip0_seed = "%s%s고 => " % (_DELTAINJ_PREFIX, stem)   # H_9397 arm B: TRAINED flip0 carrier `고` (3B)
        op0 = pfx_b + L                                  # operator-site window start (raw seed bytes)
        op1 = op0 + 10                                   # end (all three 10B morphemes; flip0 `고` is 3B, sign-only)
        assert carrier_seed.encode()[op0:op1] == cB and filler_seed.encode()[op0:op1] == fB, \
            "deltainj op-window byte-mismatch: %r" % stem
        # expected m=logP(긍)−logP(부) sign. filler/flip0 (positive/declarative) → answer follows stem
        # polarity: +1 if pol==1. carrier (negated) → flipped: −1 if pol==1. Arm B: does the TRAINED flip0
        # `고` un-flip (=stem polarity → carrier consumed, 고있다 OOD) or flip like the carrier (=stem-determined)?
        esign_filler = 1 if pol == 1 else -1
        esign_carrier = -esign_filler
        esign_flip0 = esign_filler                       # trained declarative predicts stem polarity (un-flipped)
        items.append({"stem": stem, "pol": pol, "L": L, "split": split,
                      "carrier_seed": carrier_seed, "filler_seed": filler_seed, "filler2_seed": filler2_seed,
                      "flip0_seed": flip0_seed, "op_row": [op0, op1],
                      "esign_carrier": esign_carrier, "esign_filler": esign_filler, "esign_flip0": esign_flip0})
    n_seen = sum(1 for it in items if it["split"] == "train")
    n_held = sum(1 for it in items if it["split"] != "train")
    return {"surface": "delta_inject", "prefix_bytes": pfx_b,
            "carrier": _DELTAINJ_CARRIER, "filler": _DELTAINJ_FILLER, "filler2": _DELTAINJ_FILLER2,
            "op_bytes": 10, "items": items, "n_seen": n_seen, "n_heldout": n_held,
            "note": "H_9397; Δ estimated on SEEN op_row, injected on held-out via `evaluate --delta-inject`"}


# ───────────────────────────────────────────────────────────────────────────
# L1 — XBIND-BRIDGE time-split (RUNTIME-BRIDGE campaign · H_9389 · `corpus xbind --bridge-split`).
#
# The frontier: the operator does not runtime-look-up the declaration store (TWO-LANE, no bridge).
# Correction ②: single-surface CPT writes a SURFACE-key string cache, not a stem-key FACT — gradient
# cannot rewire a path it never traversed. The "declaration→operator-answer" mapping must RECEIVE
# gradient during training. This format co-trains that mapping on one set of stems and holds it out on
# another, so we can measure whether a co-trained bridge GENERALISES (phase A), and then whether a
# declaration-only CPT can steer the operator through it (phase B).
#
# 3-way stem split (drawn from --split-seed alone; polarity-stratified so slot-prior is flat, ⓐ):
#   S_op   : BOTH surfaces supervised — flip0 declaration `{s} => pol` AND flip1 operator
#            `not {s} => flip(pol)`. This is where the declaration→operator bridge RECEIVES gradient.
#   S_decl : declaration ONLY (flip0). The operator surface appears ZERO times → held-out WITHIN
#            phase A. S_decl flip1 is the PHASE-A GATE: if a co-trained bridge exists, the operator
#            answer generalises to these unseen-operator stems ABOVE CHANCE.
#   S_cpt  : ZERO lines in the phase-A corpus. Reserved for phase B (declaration-only CPT).
#
# EN-first (ⓑ): `not` is a FREE pre-posed word (the discriminator vs the KO BOUND suffix). Positives
# are SCREENER-DIRECTIONAL. Slot-prior flattened: gold(flip1)=flip(pol) and pols are 50/50, so the
# operator answer is p(pos)=p(neg)=0.5 across the corpus (no default-negated prior to parrot, ⓐ).
#
# Emits (all pure functions of the atoms + split-seed → reproducible, corpus-py-1 (H)):
#   <out>                     phase-A training corpus (S_op flip0+flip1, S_decl flip0-only).
#   <out>.sdecl_flip1.json    PHASE-A GATE manifest (operator on S_decl · gold=flip(pol) · 0-exposure).
#   <out>.sop_flip1.json      operator-alive positive control (S_op · operator supervised).
#   <out>.scpt_flip1.json     PHASE-B DV (operator on S_cpt · gold=flip(pol) · must be chance before CPT).
#   <out>.cpt_forward.txt      phase-B CPT: S_cpt declaration at TRUE polarity (the bridge test).
#   <out>.cpt_reverse.txt      CONTROL (b): same stems, OPPOSITE-polarity declaration — the answer must
#                              TRACK the planted value; forward==reverse ⟹ cache/spillover ⟹ INVALID.
#   <out>.cpt_neutral.txt      CONTROL (c): length/capacity-matched neutral declaration (no polarity
#                              info) — control-must-match-mediating-covariate.
# ───────────────────────────────────────────────────────────────────────────
BRIDGESPLIT_FRAC = (("S_op", 0.5), ("S_decl", 0.25), ("S_cpt", 0.25))


def build_bridgesplit(atoms_path, reps, seed, split_seed, lang, polarity="real", assign_seed=0,
                      decl_ablate=False):
    if lang == "ko":
        raise SystemExit(
            "corpus xbind --bridge-split: --lang ko is refused (owner EN-FIRST directive · the KO lane "
            "is byte-frozen/BINDING). Build the EN atoms with `corpus atoms --lang en` then re-run with "
            "--lang en — EN is the discriminator (`not` FREE/pre-posed vs the KO BOUND suffix).")
    L = lang_pack(lang)
    TMPL, F0, F1 = L["tmpl"], L["flip0"], L["flip1"]
    POS, NEG = L["pos"], L["neg"]
    word = lambda p: POS if p == 1 else NEG

    atoms = json.load(open(atoms_path))["atoms"]
    raw = [a["stem"] for a in atoms]
    assert_atoms_match_lang(raw, lang)
    if polarity == "assigned":
        # H_9410: OVERRIDE the file's polarity with a RANDOM balanced assignment keyed by assign_seed.
        # A from-scratch model never read real usage, so real polarity is functionless; random
        # assignment kills any form->polarity leak and keeps G-BALANCE by construction (the strongest
        # confound control). The label is now decoupled from the word — the ONLY signal is what we WRITE.
        pol_map = _assign_balanced_polarity(raw, assign_seed)
        stems = [(s, pol_map[s]) for s in raw]
    else:
        stems = [(a["stem"], int(a["pol"])) for a in atoms]

    # polarity-stratified 3-way split (function of split_seed alone — no post-hoc redraw).
    srng = random.Random(split_seed)
    pos = [x for x in stems if x[1] == 1]
    neg = [x for x in stems if x[1] == 0]
    srng.shuffle(pos); srng.shuffle(neg)
    n = len(stems)
    sizes = {}
    acc = 0
    for name, frac in BRIDGESPLIT_FRAC:
        sizes[name] = int(round(frac * n))
    # fix rounding so the parts sum to n (give remainder to S_op)
    sizes["S_op"] += n - sum(sizes.values())
    arms, pi, ni = {}, 0, 0
    for name, _ in BRIDGESPLIT_FRAC:
        picked = []
        for k in range(sizes[name]):
            src = pos if (k % 2 == 0 and pi < len(pos)) or ni >= len(neg) else neg
            if src is pos:
                picked.append(pos[pi]); pi += 1
            else:
                picked.append(neg[ni]); ni += 1
        arms[name] = picked

    rng = random.Random(seed)
    lines = []

    def decl(stem, pol):
        for pat in F0:
            lines.append(TMPL.format(surf=pat.format(s=stem), pol=word(pol)))

    def oper(stem, pol):                      # operator line's OUTPUT = word(flip(pol))
        for pat in F1:
            lines.append(TMPL.format(surf=pat.format(s=stem), pol=word(pol ^ 1)))

    for _ in range(reps):
        for stem, pol in arms["S_op"]:        # BOTH surfaces — the bridge receives gradient here
            decl(stem, pol)
            oper(stem, pol)
        if not decl_ablate:                   # C-DECL-ABL (H_9410): ablate the S_decl DECLARATION layer
            for stem, pol in arms["S_decl"]:  # declaration ONLY — operator held out within phase A
                decl(stem, pol)
        # S_cpt: nothing in phase A.

    rng.shuffle(lines)
    text = "".join(lines)

    # eval manifests — operator surface (flip1), gold = word(flip(pol)); 2AFC gold vs counterfactual.
    def _man(arm_stems):
        held = []
        for stem, pol in arm_stems:
            gold_b = pol ^ 1                    # operator negates the planted declaration
            gw, cw = word(gold_b), word(gold_b ^ 1)
            for ti, pat in enumerate(F1):
                seed_s = TMPL.format(surf=pat.format(s=stem), pol="")[:-len(".\n")]
                held.append({"a": stem, "b": "%s|f1_%d" % (arm_stems is arms["S_cpt"] and "S_cpt" or "arm", ti),
                             "seed": seed_s, "stem": stem, "pol": pol, "flip": 1,
                             "gold_word": gw, "gold": gw + ".\n", "counterfactual": cw + ".\n"})
        return {"win": 64, "gen": 8, "heldout": held, "seen": []}

    def _man_tagged(arm_stems, tag):
        m = _man(arm_stems)
        for it in m["heldout"]:
            it["b"] = "%s|%s" % (tag, it["b"].split("|")[1])
        return m

    sdecl_man = _man_tagged(arms["S_decl"], "S_decl")
    sop_man = _man_tagged(arms["S_op"], "S_op")
    scpt_man = _man_tagged(arms["S_cpt"], "S_cpt")

    # phase-B CPT corpora on S_cpt (declaration-only, operator 0× for those stems).
    def _cpt_text(polfn):
        cl = []
        for _ in range(reps):
            for stem, pol in arms["S_cpt"]:
                for pat in F0:
                    cl.append(TMPL.format(surf=pat.format(s=stem), pol=polfn(stem, pol)))
        random.Random(seed + 101).shuffle(cl)
        return "".join(cl)

    cpt_forward = _cpt_text(lambda s, p: word(p))          # TRUE polarity
    cpt_reverse = _cpt_text(lambda s, p: word(p ^ 1))      # OPPOSITE (must track to count as a bridge)
    # neutral: same #lines, same template, but the answer is a fixed non-polar token pair balanced 50/50
    NEU = ("A", "B")
    cl = []
    for _ in range(reps):
        for i, (stem, pol) in enumerate(arms["S_cpt"]):
            for pat in F0:
                cl.append(TMPL.format(surf=pat.format(s=stem), pol=NEU[i % 2]))
    random.Random(seed + 202).shuffle(cl)
    cpt_neutral = "".join(cl)

    st = {"lang": lang, "n_atoms": n, "reps": reps,
          "split_sizes": {k: len(v) for k, v in arms.items()},
          "arms": {k: [s for s, _ in v] for k, v in arms.items()},
          "lines": len(lines), "bytes": len(text.encode()),
          "sdecl_manifest": sdecl_man, "sop_manifest": sop_man, "scpt_manifest": scpt_man,
          "cpt_forward": cpt_forward, "cpt_reverse": cpt_reverse, "cpt_neutral": cpt_neutral}
    return text, st


def _sattolo(n, seed):
    """Uniform random n-cycle: perm[i] != i for ALL i, any n >= 2. Pure fn of (n, seed).
    The strict `j < i` swap IS the no-fixed-point proof (H_9407 wrong-atom control)."""
    rng = random.Random(seed)
    idx = list(range(n))
    for i in range(n - 1, 0, -1):
        j = rng.randrange(i)                              # j < i strictly
        idx[i], idx[j] = idx[j], idx[i]
    return idx


def build_consult_variants(manifest_path=None, store_path=None, seed=7):
    """H_9407 C/D control stores: scram-pol (flip-all) + wrong-atom (Sattolo cycle) from a correct
    consult store {atom:{key,pol}}. Deterministic, in-distribution, one-variable controls (Fable spec).

    correct = --store (re-emitted byte-identical) OR derived from the eval manifest --manifest (the
    same --xbind JSON the 5-arm run scores, so store<->manifest can never drift). C flips every pol
    (a binary derangement that preserves the marginal necessarily leaves fixed points = A-contamination,
    a KILL-biased control). D permutes the facts by a Sattolo cycle over codepoint-sorted atoms so the
    fact MULTISET is identical to A and only the addressing (atom->fact) moves."""
    if store_path and manifest_path:
        raise SystemExit("consult-variants: --store and --manifest are mutually exclusive")
    if store_path:
        correct = json.load(open(store_path, encoding="utf-8"))
    elif manifest_path:
        spec = json.load(open(manifest_path, encoding="utf-8"))
        pol_by_stem = {}
        for split in ("heldout", "seen"):
            for row in spec.get(split, []):
                a, p = row["a"], int(row["pol"])
                if pol_by_stem.get(a, p) != p:
                    raise SystemExit("INVALID-INPUT: stem %r carries two pols in the manifest" % a)
                pol_by_stem[a] = p
        correct = {a: {"key": a, "pol": p} for a, p in sorted(pol_by_stem.items())}
    else:
        raise SystemExit("consult-variants: one of --store / --manifest is required")

    n = len(correct)
    if n < 2:
        raise SystemExit("INVALID: need >= 2 atoms (n=%d admits no derangement)" % n)
    if not all(int(f["pol"]) in (0, 1) for f in correct.values()):
        raise SystemExit("INVALID: pol domain (must be 0/1)")
    keys = [f["key"] for f in correct.values()]
    if len(set(keys)) != n:                               # 5c precondition: distinct keys
        raise SystemExit("INVALID: duplicate keys — a derangement could recreate A")

    scram_pol = {a: {"key": f["key"], "pol": 1 - int(f["pol"])} for a, f in correct.items()}

    atoms = sorted(correct)                               # codepoint order — JSON-order independent
    perm = _sattolo(n, seed)
    wrong_atom = {atoms[i]: dict(correct[atoms[perm[i]]]) for i in range(n)}

    # builder-coded audit — all-or-nothing (any failure -> raise, zero files written)
    fact = lambda f: (f["key"], int(f["pol"]))
    assert set(correct) == set(scram_pol) == set(wrong_atom)
    for a in correct:                                     # C: ONLY pol moved
        assert scram_pol[a]["key"] == correct[a]["key"]
        assert scram_pol[a]["pol"] == 1 - int(correct[a]["pol"])
    assert sum(scram_pol[a] != correct[a] for a in correct) == n           # 5b: flip changed ALL
    assert sorted(map(fact, wrong_atom.values())) == sorted(map(fact, correct.values()))  # D: multiset
    n_pol_match = 0
    for i, a in enumerate(atoms):
        assert perm[i] != i, "FIXED POINT — control == A on atom %r" % a    # 5a
        assert fact(wrong_atom[a]) != fact(correct[a]), "collision recreates A on atom %r" % a  # 5c
        if int(wrong_atom[a]["pol"]) == int(correct[a]["pol"]):
            n_pol_match += 1

    def _marg(store):
        c = collections.Counter(int(f["pol"]) for f in store.values())
        return {"0": c.get(0, 0), "1": c.get(1, 0)}

    st = {"correct": correct, "scram_pol": scram_pol, "wrong_atom": wrong_atom,
          "n_atoms": n, "seed": seed, "n_pol_match": n_pol_match,
          "pol_marginal": {"correct": _marg(correct), "scram_pol": _marg(scram_pol),
                           "wrong_atom": _marg(wrong_atom)},
          "key_bytes": {"min": min(len(k.encode()) for k in keys),
                        "max": max(len(k.encode()) for k in keys)},
          "source_mode": "store" if store_path else "manifest",
          "source_path": store_path or manifest_path}
    return st


def _canon_dump(obj, fh):
    json.dump(obj, fh, ensure_ascii=False, indent=1, sort_keys=True)


# ---------------------------------------------------------------------------
# study-replay — H_9520 consolidation-CPT corpus from an `anima study` transcript.
#
# The daemon perceives an EXOGENOUS teacher over a conversation (cli/study.py); this format turns
# that transcript into the CPT corpus that consolidates the teacher's content back into the 303M
# byte-LM's weights, PLUS its two frozen controls and a forget-gate stratum list, so
# `anima-py train --init` + `anima-py evaluate` can judge the lift against controls (never a raw value).
#
# Replay-mix is MANDATORY (corpus-py-1 ⑥⑦): study-only CPT DESTROYS abilities absent from the small
# corpus. The mix is majority base-corpus REPLAY (biological sleep replay) with the teacher content a
# small `study_frac`. Teacher content = the transcript `percept` lines only — NOT `emit_text`: replaying
# the daemon's OWN output is self-reinforcement (p5 · chat-py-5 self-seed), and the point of
# consolidation is absorbing content it could not self-generate.
STUDYREPLAY_BASE_MAX = 400   # base-replay line byte cap (prose sentences; over-long lines dropped)


def build_studyreplay(transcript_path, corpus_paths, study_frac, reps, seed, scramble_seed):
    """Return (mix_text, c1_text, c2_text, stats). See the format header for the design."""
    rng = random.Random(seed)
    srng = random.Random(scramble_seed)

    # 1. teacher content = the `percept` lines (whitespace-normalised so C2 word-shuffle is byte-exact).
    teacher_words, n_emit = [], 0
    with open(transcript_path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if row.get("did_emit"):
                n_emit += 1
            p = row.get("percept")
            if p:
                teacher_words.append(" ".join(str(p).split()))
    if not teacher_words:
        raise SystemExit("study-replay: transcript %s has 0 teacher `percept` lines — nothing to "
                         "consolidate (a silent-teacher run cannot feed a CPT)." % transcript_path)
    teacher_lines = [w + "\n" for w in teacher_words]
    teacher_pool_bytes = sum(len(t.encode()) for t in teacher_lines)

    # 2. base-corpus replay pool (the majority — corpus-py-1 ⑥⑦).
    if not (0.0 < study_frac < 1.0):
        raise SystemExit("study-replay: --study-frac must be in (0,1), got %g." % study_frac)
    base = []
    for cp in corpus_paths:
        with open(cp, encoding="utf-8", errors="replace") as fh:
            for line in fh:
                s = line.strip()
                if 20 <= len(s.encode()) <= STUDYREPLAY_BASE_MAX:
                    base.append(s + "\n")
    if not base:
        raise SystemExit("study-replay: --corpus gave 0 usable base lines (need 20..%d bytes each). "
                         "Replay-mix is MANDATORY (corpus-py-1 ⑥)." % STUDYREPLAY_BASE_MAX)
    rng.shuffle(base)
    teacher_set = set(teacher_lines)

    def _fill(byte_target):
        out, acc, i = [], 0, 0
        while acc < byte_target:
            ln = base[i % len(base)]
            out.append(ln); acc += len(ln.encode()); i += 1
        return out

    # 3. sizes: teacher repeated `reps` times = the study portion; base replay fills to the ratio.
    study_bytes = teacher_pool_bytes * reps
    base_replay_bytes = int(round(study_bytes * (1.0 - study_frac) / study_frac))
    study_lines = teacher_lines * reps
    base_lines = _fill(base_replay_bytes)

    mix = study_lines + base_lines
    random.Random(seed).shuffle(mix)
    mix_text = "".join(mix)
    mix_bytes = len(mix_text.encode())

    # C1 replay-only: teacher ABSENT · base replay padded to the SAME total byte count (identical
    # replay-量 covariate · control-must-match-mediating-covariate).
    c1_lines = _fill(mix_bytes)
    random.Random(seed).shuffle(c1_lines)
    c1_text = "".join(c1_lines)

    # C2 scrambled-teacher: teacher lines word-shuffled (meaning destroyed · word-multiset + byte count
    # preserved) · SAME base replay → same total bytes.
    scr = []
    for _ in range(reps):
        for t in teacher_words:
            ws = t.split()
            srng.shuffle(ws)
            scr.append(" ".join(ws) + "\n")
    c2 = scr + base_lines
    random.Random(seed).shuffle(c2)
    c2_text = "".join(c2)

    # honesty audits (xbind EVAL-LEAK precedent): C1 has ZERO teacher lines · C2 byte-matches the mix.
    c1_leak = sum(1 for ln in c1_text.splitlines(keepends=True) if ln in teacher_set)
    c2_bytes = len(c2_text.encode())
    stats = {
        "teacher_lines": len(teacher_lines), "teacher_pool_bytes": teacher_pool_bytes,
        "substrate_emits": n_emit, "reps": reps, "base_pool": len(base),
        "study_frac_req": study_frac,
        "study_frac_actual": round(study_bytes / mix_bytes, 4) if mix_bytes else 0.0,
        "mix_bytes": mix_bytes, "c1_bytes": len(c1_text.encode()), "c2_bytes": c2_bytes,
        "c1_teacher_leak": c1_leak, "c2_byte_match": (c2_bytes == mix_bytes),
    }
    if c1_leak:
        raise SystemExit("study-replay: C1 LEAK — %d teacher line(s) appeared verbatim in the "
                         "replay-only control. C1 must contain ZERO teacher content." % c1_leak)
    return mix_text, c1_text, c2_text, stats


# ---------------------------------------------------------------------------
# ngram-audit — the N-GRAM-RECOVERABILITY audit (H_9809 · `--ngram-recoverable-audit`).
#
# WHY THIS SEAT (corpus.py, not evaluate.py). The audit is a property of
# (panel x tokenization x training stream) and touches NO checkpoint. `anima-py evaluate`
# requires a `.clm`, so seating it there would make the one thing this instrument is FOR —
# a $0 gate fired BEFORE any training run — structurally impossible. corpus.py is the panel
# builder; a panel defect must be catchable where the panel is made.
#
# WHAT IT ANSWERS. Lab v3 H_004 reached a verified theorem: for a FIXED morpheme,
# **oracle-fusable <=> n-gram-recoverable**. If a morpheme is frequent enough for a codec to
# fuse it into one atomic token, its terminal n-gram under the un-fused control ALSO recovers
# the class. Their repaired rig closed order-1 (G-A 0.527) but order-2 read 0.9954 — a
# transformer binds order-2 with one attention head, so the "no-atomicity" control was not a
# control at all. Consequence: an "atomicity" effect can be an n-gram-recoverability effect
# wearing a costume, and ONLY an explicit order-2 arm makes the difference visible.
#
# THE BATTERY (per tokenization arm, mirroring v3's G-A/G-B/G-C):
#   order-0  majority-class baseline  -> the DERIVED chance floor for THIS realized panel
#            split (`chance-level-must-be-derived-per-metric`: never assume 0.5).
#   order-1  terminal-unigram Bayes lookup, fit on TRAIN only, scored on PANEL.
#   order-2  terminal-bigram  Bayes lookup, fit on TRAIN only, scored on PANEL.
#   perm     the same battery on label-PERMUTED train -> must collapse to order-0. This is
#            the negative control; without it a high order-2 could be a harness artifact.
#   reach    (optional `--audit-marker`) per-arm terminal DISTANCE of each class-discriminating
#            marker. This is the quantity a codec arm and a raw-bytes arm do NOT share: the
#            same morpheme sits 1 token from the decision point under a codec and ~18 bytes
#            under raw utf-8. A cross-arm delta in reach is a confound with atomicity, not a
#            measurement of it.
#
# COVERAGE IS LOAD-BEARING. A lookup whose panel keys were NEVER seen in train falls back to
# the majority class and returns exactly order-0. Reading that as "the path is closed" is the
# trap. So every order reports `coverage` = fraction of panel items whose key was seen in
# train, and an order with coverage below --audit-min-coverage is reported
# UNDECIDABLE-AT-ORDER-k, never CLOSED. An instrument that cannot tell "closed" from "never
# asked" manufactures verdicts.
#
# VERDICT VOCABULARY (per arm, per order):
#   CLOSED       acc - chance0 <= 0.05          no shortcut at this order
#   MARGINAL     0.05 < acc - chance0, acc < 0.90
#   OPEN         acc >= 0.90                    a trivial n-gram path exists at this order
#   UNDECIDABLE  coverage < --audit-min-coverage
#
# This instrument reports. It does not overturn: a landed verdict falls only to an
# engine-native `anima-py` measurement carrying its own positive control.
# ---------------------------------------------------------------------------

_NGA_CHO = "ㄱㄲㄴㄷㄸㄹㅁㅂㅃㅅㅆㅇㅈㅉㅊㅋㅌㅍㅎ"
_NGA_JUNG = "ㅏㅐㅑㅒㅓㅔㅕㅖㅗㅘㅙㅚㅛㅜㅝㅞㅟㅠㅡㅢㅣ"
_NGA_JONG = "_ㄱㄲㄳㄴㄵㄶㄷㄹㄺㄻㄼㄽㄾㄿㅀㅁㅂㅄㅅㅆㅇㅈㅊㅋㅌㅍㅎ"
_NGA_ARROW = " => "


def _nga_to_jamo(s):
    """Hangul -> jamo symbols with distinct C:/V:/J: markers. Byte-faithful to the MORPH-2B
    codec's own decomposition (state/nbind_curriculum/morph2b.py) — reimplemented here rather
    than imported because production never imports from the frozen research tree
    (`a_no_archive_import`); the audit must stand alone in the installed wheel."""
    out = []
    for ch in s:
        o = ord(ch)
        if 0xAC00 <= o <= 0xD7A3:
            i = o - 0xAC00
            out.append("C:" + _NGA_CHO[i // 588])
            out.append("V:" + _NGA_JUNG[(i % 588) // 28])
            j = i % 28
            if j:
                out.append("J:" + _NGA_JONG[j])
        else:
            out.append("R:" + ch)
    return out


def _nga_eojeol_split(line):
    parts = []
    for j, w in enumerate(line.split(" ")):
        if j:
            parts.append(([" "], True))
        if w:
            parts.append((_nga_to_jamo(w), False))
    return parts


def _nga_apply_merges(syms, merge_rank):
    w = list(syms)
    while True:
        best = None
        for i in range(len(w) - 1):
            r = merge_rank.get((w[i], w[i + 1]))
            if r is not None and (best is None or r < best[0]):
                best = (r, i)
        if best is None:
            return w
        i = best[1]
        w[i:i + 2] = [w[i] + "\x00" + w[i + 1]]


def _nga_load_codec(path):
    """Read a MORPH-2B-style codec.json: {"merges": ["a\\tb", ...], "tok2id": {...}}."""
    d = json.load(open(path, encoding="utf-8"))
    merges = [tuple(m.split("\t")) for m in d["merges"]]
    merge_rank = {(a, b): r for r, (a, b) in enumerate(merges)}
    tok2id = d.get("tok2id") or {}
    return merge_rank, tok2id


def _nga_tokenize(text, arm):
    """arm = ('raw', None) -> utf-8 byte ids · ('codec', (merge_rank, tok2id)) -> codec token ids."""
    kind, cx = arm
    if kind == "raw":
        return list(text.encode("utf-8", "replace"))
    merge_rank, tok2id = cx
    ids = []
    for syms, sp in _nga_eojeol_split(text):
        toks = [" "] if sp else _nga_apply_merges(syms, merge_rank)
        for t in toks:
            i = tok2id.get(t)
            if i is None:
                ids.extend(0 for _ in t.replace("\x00", "").encode("utf-8", "replace"))
            else:
                ids.append(i)
    return ids


def _nga_read_pairs(path):
    """(text, label) pairs. Accepts, in order: morphatom-eval-v1 / any {"items":[...]} panel
    JSON (seed+gold), a JSON list or JSONL of {"text","label"}, or plain `X => LABEL` arrow
    lines (the corpus convention shared by ground/derivtrace/nbind)."""
    raw = open(path, "rb").read().decode("utf-8", "replace")
    st = raw.lstrip()
    if st.startswith("{") or st.startswith("["):
        try:
            d = json.loads(raw)
        except ValueError:
            d = None
        if d is not None:
            items = d.get("items", d) if isinstance(d, dict) else d
            out = []
            for it in items:
                if not isinstance(it, dict):
                    continue
                t = it.get("text", it.get("seed"))
                lab = it.get("label", it.get("gold"))
                if t is None or lab is None:
                    continue
                if t.endswith(_NGA_ARROW):
                    t = t[: -len(_NGA_ARROW)]
                out.append((t.strip(), str(lab).strip()))
            if out:
                return out
    out = []
    for line in raw.splitlines():
        line = line.strip("\x00").strip()
        if _NGA_ARROW not in line:
            continue
        body, lab = line.rsplit(_NGA_ARROW, 1)
        if body.strip() and lab.strip():
            out.append((body.strip(), lab.strip()))
    return out


def _nga_lookup(train_toks, order):
    """Fit P(label | terminal `order`-gram) on train. Returns key -> majority label."""
    cnt = collections.defaultdict(collections.Counter)
    for toks, lab in train_toks:
        if len(toks) < order:
            continue
        cnt[tuple(toks[-order:])][lab] += 1
    return {k: c.most_common(1)[0][0] for k, c in cnt.items()}


def _nga_score(table, panel_toks, order, majority):
    hit = seen = 0
    for toks, lab in panel_toks:
        key = tuple(toks[-order:]) if len(toks) >= order else None
        pred = table.get(key) if key is not None else None
        if pred is None:
            pred = majority
        else:
            seen += 1
        if pred == lab:
            hit += 1
    n = max(len(panel_toks), 1)
    return hit / n, seen / n


def _nga_arm_report(train_pairs, panel_pairs, arm, seed, min_cov, orders=(1, 2)):
    train_toks = [(_nga_tokenize(t, arm), l) for t, l in train_pairs]
    panel_toks = [(_nga_tokenize(t, arm), l) for t, l in panel_pairs]
    labs = collections.Counter(l for _, l in panel_pairs)
    majority = collections.Counter(l for _, l in train_pairs).most_common(1)[0][0]
    # DERIVED chance: the realized majority share of THIS panel, not an assumed 0.5.
    chance0 = labs.most_common(1)[0][1] / max(len(panel_pairs), 1)
    rep = {"n_train": len(train_pairs), "n_panel": len(panel_pairs),
           "panel_label_split": dict(labs), "order0_chance": round(chance0, 4),
           "mean_len": round(sum(len(t) for t, _ in panel_toks) / max(len(panel_toks), 1), 2),
           "orders": {}}
    rng = random.Random(seed)
    perm_labels = [l for _, l in train_pairs]
    rng.shuffle(perm_labels)
    perm_toks = [(t, perm_labels[i]) for i, (t, _) in enumerate(train_toks)]
    for k in orders:
        acc, cov = _nga_score(_nga_lookup(train_toks, k), panel_toks, k, majority)
        pacc, _ = _nga_score(_nga_lookup(perm_toks, k), panel_toks, k, majority)
        if cov < min_cov:
            verdict = "UNDECIDABLE"
        elif acc >= 0.90:
            verdict = "OPEN"
        elif acc - chance0 <= 0.05:
            verdict = "CLOSED"
        else:
            verdict = "MARGINAL"
        rep["orders"][str(k)] = {"acc": round(acc, 4), "delta_vs_chance": round(acc - chance0, 4),
                                 "coverage": round(cov, 4), "perm_control_acc": round(pacc, 4),
                                 "verdict": verdict}
    return rep


def _nga_marker_reach(panel_pairs, arm, markers):
    """Terminal distance (in this arm's units) from each marker's LAST token to the end of the
    body. THE cross-arm confound quantity: a codec puts a fused morpheme ~1 unit from the
    decision point where raw utf-8 puts it ~18 bytes away."""
    out = {}
    for m in markers:
        mt = _nga_tokenize(m, arm)
        if not mt:
            continue
        dists = []
        for text, _ in panel_pairs:
            toks = _nga_tokenize(text, arm)
            pos = [i for i in range(len(toks) - len(mt) + 1) if toks[i:i + len(mt)] == mt]
            if pos:
                dists.append(len(toks) - (pos[-1] + len(mt)))
        if dists:
            dists.sort()
            out[m] = {"n_hit": len(dists), "units": len(mt),
                      "median_terminal_distance": dists[len(dists) // 2],
                      "min_terminal_distance": dists[0]}
        else:
            out[m] = {"n_hit": 0, "units": len(mt)}
    return out



# ── H_9812 FIELD-ALONE LEAK GATE ──────────────────────────────────────────────────────────
# The deciding control for "does the tension field see content, or does the core?". A concord
# mode that lets the FIELD ALONE predict the answer above chance has not given the trunk a
# channel — it has handed it the answer, and any Δ measured under that mode is unreadable.
# This is settled by measurement, never by the argument that "agreement is not the answer".
#
# Method mirrors the H_9809 n-gram audit deliberately (fit on TRAIN, score on PANEL, chance
# DERIVED from the realized split, coverage guard ⇒ UNDECIDABLE rather than a false CLOSED):
# the field's signature for one conjunct is the tuple of chi signs its live edges carry, which
# is exactly what a downstream reader could exploit and nothing more.
def _field_signature(surface, concord):
    import numpy as _np
    from tension_field import tension_edges          # core/tension_field.py
    toks = _np.frombuffer(surface.encode(), dtype=_np.uint8).astype(_np.int64)
    rows, cols, vals = tension_edges(toks, concord=concord)
    if rows.size == 0:
        return ("void",)
    order = _np.lexsort((cols, rows))
    return tuple(int(v) for v in _np.sign(vals[order]).astype(_np.int64))


def field_alone_leak(train_conj, panel_conj, concord, min_coverage=0.10):
    """Can the FIELD ALONE call gold_bit? Returns a dict; `leaks` True ⇒ the mode is disqualified."""
    from collections import Counter, defaultdict
    table = defaultdict(Counter)
    for c in train_conj:
        table[_field_signature(c["surface"], concord)][int(c["gold_bit"])] += 1
    gold = [int(c["gold_bit"]) for c in panel_conj]
    n = len(gold) or 1
    maj = Counter(gold).most_common(1)[0][1]
    chance = maj / n                                  # DERIVED from the realized panel split
    seen = hit = 0
    for c, g in zip(panel_conj, gold):
        sig = _field_signature(c["surface"], concord)
        row = table.get(sig)
        if row:
            seen += 1
            pred = row.most_common(1)[0][0]
        else:
            pred = Counter(gold).most_common(1)[0][0]   # majority fallback = order-0 by construction
        hit += int(pred == g)
    cov = seen / n
    acc = hit / n
    undecidable = cov < min_coverage
    return {"concord": concord, "acc": round(acc, 4), "chance": round(chance, 4),
            "coverage": round(cov, 4), "n": n,
            "undecidable": bool(undecidable),
            "leaks": bool((not undecidable) and acc > chance + 1e-9)}


def run_ngram_audit(opts):
    train_pairs = _nga_read_pairs(opts["audit_train"])
    panel_pairs = _nga_read_pairs(opts["panel"])
    if not train_pairs or not panel_pairs:
        raise SystemExit("corpus ngram-audit: parsed %d train / %d panel labeled item(s) — "
                         "need both. Expect `X => LABEL` lines or an {\"items\":[{seed,gold}]} panel."
                         % (len(train_pairs), len(panel_pairs)))
    arms = {"raw_utf8": ("raw", None)}
    if opts.get("codec"):
        arms["codec"] = ("codec", _nga_load_codec(opts["codec"]))
    markers = [m for m in (opts.get("audit_marker") or "").split(",") if m.strip()]
    res = {"instrument": "ngram-recoverable-audit", "hypothesis": "H_9809",
           "theorem": "lab/v3 H_004: oracle-fusable <=> n-gram-recoverable (verified 12/12)",
           "train": opts["audit_train"], "panel": opts["panel"],
           "codec": opts.get("codec"), "seed": opts["seed"],
           "min_coverage": opts["audit_min_coverage"], "arms": {}}
    for name, arm in arms.items():
        rep = _nga_arm_report(train_pairs, panel_pairs, arm, opts["seed"],
                              opts["audit_min_coverage"])
        if markers:
            rep["marker_reach"] = _nga_marker_reach(panel_pairs, arm, markers)
        res["arms"][name] = rep

    print("=== anima-py corpus ngram-audit (--ngram-recoverable-audit · H_9809) ===")
    print("  theorem under test: lab/v3 H_004 — oracle-fusable <=> n-gram-recoverable")
    print("  train %s (%d labeled) · panel %s (%d labeled)"
          % (opts["audit_train"], len(train_pairs), opts["panel"], len(panel_pairs)))
    for name, rep in res["arms"].items():
        print("\n  [arm %s]  order-0 derived chance = %.4f  (panel split %s · mean len %.1f)"
              % (name, rep["order0_chance"], rep["panel_label_split"], rep["mean_len"]))
        for k in sorted(rep["orders"]):
            o = rep["orders"][k]
            print("    order-%s acc %.4f (Δ%+.4f vs chance) · key-coverage %.4f · "
                  "perm-control %.4f  -> %s"
                  % (k, o["acc"], o["delta_vs_chance"], o["coverage"],
                     o["perm_control_acc"], o["verdict"]))
        for m, d in (rep.get("marker_reach") or {}).items():
            if d["n_hit"]:
                print("    marker %-6s %2d unit(s) · hits %3d · median terminal distance %d"
                      % (repr(m), d["units"], d["n_hit"], d["median_terminal_distance"]))
            else:
                print("    marker %-6s %2d unit(s) · hits 0 (absent from panel bodies)" % (repr(m), d["units"]))
    if len(res["arms"]) > 1:
        print("\n  CROSS-ARM: a reach asymmetry between arms is a CONFOUND with atomicity, not a")
        print("  measurement of it — the arms differ in how far the discriminating unit sits from")
        print("  the decision point, which is an n-gram-reach variable, not an atomicity variable.")
    print("\n  UNDECIDABLE = key-coverage below --audit-min-coverage: the lookup fell back to the")
    print("  majority class, so its accuracy is order-0 by construction and says NOTHING about the")
    print("  path. Never read UNDECIDABLE as CLOSED.")
    print("\n  This instrument REPORTS. It does not overturn a landed verdict — that needs an")
    print("  engine-native `anima-py` measurement carrying its own positive control.")
    if opts["out"]:
        _canon_dump(res, open(opts["out"], "w"))
        print("\n  -> %s" % opts["out"])
    return res


def run_mi_screen(opts):
    """H_9844 — compression-MI screener over core/mi_compress.py (H_9806).

    WHAT IT ANSWERS, and why no existing flag answers it: every prior read of the
    data face of the recombination wall (H_9304: non-additive information +0.0023
    nats, TOST-equivalent to 0) went THROUGH a forward pass, which conflates what
    the corpus CARRIES with what the model can REACH. `stream_mi` measures the
    stream itself — gzip / PPM / order-6 Markov conditional bpb of segment t+1's
    prefix given segment t's tail, against a DERIVED shuffle floor. No ckpt, no
    GPU, no torch.

    GATE ORDER IS LOAD-BEARING (frozen, sequential):
      1. `battery_liveness` runs the two SHIPPED controls first —
         `plant_crossboundary` (a known, quantified cross-boundary signal: the
         instrument must FIRE) and `plant_null_stream` (byte-for-byte the same
         construction with the carry-over REMOVED: the instrument must REFUSE).
      2. Only if both certify is the corpus row reported. An uncertified battery
         yields INSTRUMENT-DEAD / INVALID and NO corpus number — reading a stream
         through an estimator that cannot see a planted signal (or manufactures
         one) is exactly the failure `positive-control-before-reading-a-negative`
         and `phi-estimator-needs-zero-truth-pedestal` were written for.

    The emitted JSON carries the full re-audit fingerprint (argv, per-input sha256
    + byte length, resolved geometry) so the verdict is re-checkable by someone who
    was not in this session (corpus-py-1 ⑫(J)).
    """
    import mi_compress as MI                       # core/mi_compress.py (core/ is on sys.path)

    win = opts["mi_win"] or MI.W_TAIL
    span = opts["mi_span"] or MI.P_PRED
    eps = opts["mi_eps"] or MI.EPS_BPB
    want = opts["mi_estimator"]
    if want == "all":
        estimators = MI.ESTIMATORS
    else:
        estimators = tuple(e for e in MI.ESTIMATORS if e[0] == want)
        if not estimators:
            print("mi-screen: unknown --mi-estimator %r (have: %s, all)"
                  % (want, ", ".join(n for n, _ in MI.ESTIMATORS)))
            sys.exit(2)

    # ── ① controls FIRST — the corpus row is refused unless both certify ──────
    battery = MI.battery_liveness(win=win, span=span, eps=eps, estimators=estimators)
    certified = bool(battery.get("certified"))
    if not certified:
        if not battery.get("plant_fires"):
            status = "INSTRUMENT-DEAD"
            why = ("plant_crossboundary did NOT fire — the estimator cannot see a signal that is "
                   "known to be there, so a null read on the corpus would be a property of the "
                   "estimator, not of the corpus.")
        else:
            status = "INVALID"
            why = ("plant_null_stream did NOT refuse — the estimator reports information on a "
                   "stream built with the carry-over removed, i.e. it MANUFACTURES signal.")
    else:
        status = "CERTIFIED"
        why = "both shipped controls behaved: plant fires, null refuses."

    # ── ② geometry sweep — a lift that lives at ONE block size is not a corpus fact ──
    # MEASURED 2026-07-21, and it is why this is not optional: on the SAME three corpora the
    # sign flips with the block size. corpus flat --lang en: gzip over_floor -0.0020 at
    # 60-line/4096B blocks but +0.0312 at 8-line/512B blocks; corpus storebind: +0.0195 at
    # 60-line/4096B (the highest of any corpus) but +0.0000 at 46-line/512B. Reporting one
    # geometry lets the block size choose the verdict — tune-to-green with extra steps. So the
    # headline is the MINIMUM over_floor across geometries, and a lift is READ only if every
    # geometry clears eps. The controls are re-certified at each geometry too.
    geometries = [(opts["mi_seg_lines"], win, span)]
    if opts["mi_robust"]:
        for div in (2, 8):
            g_win, g_span = max(64, win // div), max(32, span // div)
            g_lines = max(1, (opts["mi_seg_lines"] or 0) // div) if opts["mi_seg_lines"] else 0
            geometries.append((g_lines, g_win, g_span))

    rows = []
    if certified:
        for path in opts["corpus"]:
            per_geom, sha = [], _mi_sha_of(path)
            for (g_lines, g_win, g_span) in geometries:
                if g_lines:
                    segments, how = _mi_segments_by_lines(path, g_lines, g_win, g_span)
                else:
                    segments, how = MI.segments_from_path(path, win=g_win, span=g_span)
                r = MI.stream_mi(segments, win=g_win, span=g_span, eps=eps, estimators=estimators)
                r["geometry"] = {"seg_lines": g_lines, "win": g_win, "span": g_span}
                r["segmented_as"] = how
                per_geom.append(r)
            names = [n for n, _ in estimators]
            robust = {n: min(g[n]["over_floor"] for g in per_geom) for n in names}
            spread = {n: (max(g[n]["over_floor"] for g in per_geom)
                          - min(g[n]["over_floor"] for g in per_geom)) for n in names}
            row = {
                "path": path, "sha256": sha, "n_geometries": len(per_geom),
                "robust_over_floor": robust, "geometry_spread": spread,
                "read": {n: bool(robust[n] > eps) for n in names},
                "geometry_dependent": {n: bool(spread[n] > eps and robust[n] <= eps) for n in names},
                "per_geometry": per_geom,
            }
            rows.append(row)

    out = {
        "instrument": "mi-screen",
        "hypothesis": "H_9844",
        "engine": "core/mi_compress.py (H_9806)",
        "status": status,
        "why": why,
        "battery": battery,
        "geometry": {"win": win, "span": span, "eps": eps,
                     "estimators": [n for n, _ in estimators]},
        "corpus": rows,
        "reaudit": {"argv": ["anima-py", "corpus"] + sys.argv[1:]},
        "reading": ("With --mi-robust the headline is `robust_over_floor` = the MINIMUM over_floor "
                    "across geometries, and `read` is true only when that minimum clears eps; "
                    "`geometry_dependent` marks an estimator whose lift exists at one block size "
                    "and dies at another (spread > eps while the minimum does not clear it) — that "
                    "is a segmentation artefact, not a corpus fact. Underneath: "
                    "`over_floor` is the headline, never a bare ceiling: it is the estimator's "
                    "ceiling MINUS its own derived shuffle floor. over_floor <= eps on every "
                    "estimator = this stream carries no readable cross-boundary information, "
                    "which is a CORPUS fact and is measured without any model. DIRECTIONAL: a "
                    "compression estimator is a lower bound on what is there, so a null bounds "
                    "readability, not existence."),
    }
    if opts["out"]:
        open(opts["out"], "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not certified:
        sys.exit(3)


def _mi_segments_by_lines(path, per_seg, win, span):
    """Segment a LINE-RECORD corpus into blocks of `per_seg` consecutive lines.

    WHY THIS EXISTS: `MI.segments_from_path` splits a file on blank lines, but anima's own
    procedural training corpora have ZERO blank lines (measured: `corpus flat --lang en --seed 7`
    = 798,570 B / 6,540 lines / 0 occurrences of b"\n\n"). Without this the screener cannot
    segment the very streams it exists to screen — it would return one unusable segment and
    report `underpowered`. One line = one training record, so a block of N consecutive lines is
    the corpus's own unit, not an arbitrary byte cut.

    The `win + span` floor from `segments_from_path` is kept verbatim: short blocks are DROPPED,
    never padded, and the attrition is reported in the returned `how` string."""
    with open(path, "rb") as fh:
        lines = fh.read().split(b"\n")
    blocks = []
    for i in range(0, len(lines), per_seg):
        blob = b"\n".join(lines[i:i + per_seg])
        if blob.strip():
            blocks.append(("lines%06d" % i, blob))
    keep = [(nm, b) for nm, b in blocks if len(b) >= win + span]
    return keep, ("file:lines/%d → %d blocks · %d/%d usable (>= %dB)"
                  % (per_seg, len(blocks), len(keep), len(blocks), win + span))


def _mi_sha_of(path):
    """sha256 + byte length of a screener input (a file, or a directory's files in
    sorted order) so the emitted verdict names exactly what was measured."""
    h = hashlib.sha256()
    n = 0
    if os.path.isdir(path):
        for name in sorted(os.listdir(path)):
            fp = os.path.join(path, name)
            if os.path.isfile(fp):
                b = open(fp, "rb").read()
                h.update(name.encode("utf-8")); h.update(b); n += len(b)
    else:
        b = open(path, "rb").read()
        h.update(b); n = len(b)
    return {"sha256": h.hexdigest(), "bytes": n}


# ── H_9842 wake-coresidency ─────────────────────────────────────────────────────
# Recombination needs two concepts to CO-OCCUR. core/wake_memory.py's working buffer is a
# FIFO whose capacity was a HARDCODED 20 (`_working_cap()`), so two anchors more than 20
# ticks apart can never be jointly resident — the memory-side twin of the trunk receptive
# field bound (H_9836/H_1394: concepts at distance D > RF are mathematically independent,
# capacity irrelevant). These helpers drive the SHIPPED buffer functions — no re-derivation,
# no model, no ckpt — and report what fraction of anchor pairs the buffer can ever hold at
# once, as a function of capacity, with the append-only `episodic` arm as the uncapped
# refutation arm.

_WAKE_PLANT_GAP = 50            # planted anchor spacing, in ticks (positive control)
_WAKE_PLANT_N = 8               # planted anchors
_WAKE_NULL_TICKS = 400          # zero-truth pedestal stream length
_WAKE_PLANT_MIN_DELTA = 0.25    # cap_delta the plant must clear or the instrument is DEAD


def _wake_pairs_working(stream, cap):
    """Pairs ever JOINTLY resident in the real ring buffer at capacity `cap`.

    Drives core/wake_memory.py::mem_push_ctx_capped + mem_working_window verbatim, one push
    per tick (the daemon's own cadence — cli/chat.py:2192 pushes exactly once per tick).
    Only anchors that NEWLY entered the window can create a new co-resident pair (if both
    were resident at t and neither entered at t, both were resident at t-1), so pairing the
    entrants against the current window is exhaustive, not a sample."""
    import wake_memory as WM
    mem = WM.mem_init()
    seen, prev = set(), set()
    for anchors in stream:
        mem = WM.mem_push_ctx_capped(mem, list(anchors), cap)
        cur = set()
        for entry in WM.mem_working_window(mem):
            for a in entry:
                cur.add(a)
        for a in (cur - prev):
            for b in cur:
                if a != b:
                    seen.add((a, b) if a < b else (b, a))
        prev = cur
    return seen


def _wake_pairs_episodic(stream):
    """Pairs ever jointly resident in the APPEND-ONLY episodic log = the uncapped arm.

    Drives core/wake_memory.py::mem_record_emit + mem_recent_emits verbatim; the anchors are
    round-tripped THROUGH the record's `ctx_summary` field, so this reads what the shipped
    log actually stores, not what the caller passed in. The episodic window only ever grows,
    so the last tick is its maximum and one read there is exact (not a shortcut that could
    miss a pair)."""
    import wake_memory as WM
    mem = WM.mem_init()
    for ts, anchors in enumerate(stream):
        summary = ",".join(str(a) for a in sorted(anchors))
        mem = WM.mem_record_emit(mem, float(ts), summary, 0.0, [0.0] * 5, "WAKE", "")
    resident = set()
    for rec in WM.mem_recent_emits(mem, len(stream)):
        for tok in rec["ctx_summary"].split(","):
            if tok:
                resident.add(int(tok))
    out = set()
    ordered = sorted(resident)
    for x in range(len(ordered)):
        for y in range(x + 1, len(ordered)):
            out.add((ordered[x], ordered[y]))
    return out


def _wake_all_pairs(stream):
    """Denominator: every pair of anchors that both occur somewhere in the stream.

    Computed from the stream DIRECTLY, never through wake_memory — otherwise the episodic
    arm would be 1.0 by definition instead of by measurement, and a log that silently
    dropped records would still read perfect."""
    present = set()
    for anchors in stream:
        present.update(anchors)
    ordered = sorted(present)
    return {(ordered[x], ordered[y])
            for x in range(len(ordered)) for y in range(x + 1, len(ordered))}


def _wake_row(stream, caps, source, eps):
    """One co-residency row: fraction of occurring anchor pairs jointly resident, per cap."""
    total = len(_wake_all_pairs(stream))
    row = {"n_ticks": len(stream), "n_pairs": total, "working": {}, "episodic": None}
    if total == 0:
        return row
    if source in ("working", "both"):
        for cap in caps:
            row["working"][str(cap)] = round(len(_wake_pairs_working(stream, cap)) / total, 4)
    if source in ("episodic", "both"):
        row["episodic"] = round(len(_wake_pairs_episodic(stream)) / total, 4)
    if row["working"]:
        lo, hi = str(min(caps)), str(max(caps))
        row["cap_delta"] = round(row["working"][hi] - row["working"][lo], 4)
        row["read_ceiling"] = bool(row["cap_delta"] > eps)
        if row["episodic"] is not None:
            row["episodic_delta"] = round(row["episodic"] - row["working"][lo], 4)
    return row


def _wake_plant_stream(gap, n_anchors):
    """POSITIVE CONTROL stream — anchor i occurs ONCE, at tick i*gap, nowhere else.

    Truth is known and quantified: a pair (i,j) is jointly resident at capacity C iff
    |i-j|*gap <= C-1. With gap=50 that is 0 pairs at C=20 and 25/28 at C=256, so an
    instrument that reads the buffer at all MUST show a large cap-dependence here."""
    stream = [[] for _ in range(gap * n_anchors)]
    for a in range(n_anchors):
        stream[a * gap] = [a]
    return stream


def _wake_null_stream(n_ticks, n_anchors):
    """ZERO-TRUTH PEDESTAL — every anchor is pushed on EVERY tick.

    The measured quantity (cap-dependence of co-residency) is exactly 0 by construction:
    every pair is jointly resident even at capacity 1, so no capacity can separate anything.
    An instrument that reports a cap effect here is MANUFACTURING it."""
    return [list(range(n_anchors)) for _ in range(n_ticks)]


def _wake_battery(caps, eps):
    """Run the two controls, in the frozen order, before any treatment row is computed."""
    plant = _wake_row(_wake_plant_stream(_WAKE_PLANT_GAP, _WAKE_PLANT_N), caps, "both", eps)
    null = _wake_row(_wake_null_stream(_WAKE_NULL_TICKS, _WAKE_PLANT_N), caps, "both", eps)
    lo = str(min(caps))
    plant_fires = bool(plant.get("cap_delta", 0.0) >= _WAKE_PLANT_MIN_DELTA)
    null_refuses = bool(abs(null.get("cap_delta", 1.0)) <= eps
                        and null["working"].get(lo, 0.0) >= 1.0 - eps)
    return {
        "plant_crossboundary": plant, "plant_null_stream": null,
        "plant_fires": plant_fires, "null_refuses": null_refuses,
        "certified": bool(plant_fires and null_refuses),
        "plant_geometry": {"gap_ticks": _WAKE_PLANT_GAP, "n_anchors": _WAKE_PLANT_N,
                           "min_delta_to_fire": _WAKE_PLANT_MIN_DELTA},
    }


def _wake_anchor_strata(path, k, n_ticks):
    """Tokenise a line-record corpus into ticks + three frequency strata of anchors.

    ONE TICK = ONE LINE (the corpus's own record unit, same reading `--mi-seg-lines` uses).
    Anchors are WHITESPACE-DELIMITED tokens, never substrings — `text.count(stem)` inflates
    a stem with every longer word containing it (corpus-py-1 ⑩, bit this repo three times).
    Frequency strata exist because anchor choice is a knob that could pick the verdict: the
    most frequent tokens recur every few lines (small gaps ⇒ co-residency ~1 at any cap) and
    the rarest recur across the whole file. Reporting one stratum would be tune-to-green, so
    all three are reported and the headline requires them to agree."""
    lines = open(path, "r", encoding="utf-8", errors="replace").read().split("\n")
    if n_ticks:
        lines = lines[:n_ticks]
    toks = [ln.split() for ln in lines]
    freq = collections.Counter()
    for t in toks:
        freq.update(set(t))
    recurring = [w for w, c in freq.most_common() if c >= 2]
    strata = {}
    if len(recurring) >= 3 * k:
        mid = len(recurring) // 2
        strata["top"] = recurring[:k]
        strata["mid"] = recurring[mid - k // 2: mid - k // 2 + k]
        strata["rare"] = recurring[-k:]
    return strata, toks, len(recurring)


def _wake_stream_for(toks, anchors):
    ids = {w: i for i, w in enumerate(anchors)}
    return [[ids[w] for w in dict.fromkeys(t) if w in ids] for t in toks]


def run_wake_coresidency(opts):
    """H_9842 — is the wake working ring buffer a co-occurrence ceiling for recombination?

    WHAT IT ANSWERS, and why no existing flag answers it: every recombination read so far
    (H_9304 data wall, H_9836 receptive-field bound) asked what the TRUNK can join. The
    memory side was never measured because its capacity was a hardcoded constant, so there
    was nothing to sweep. This flag makes the capacity a variable (core/wake_memory.py's new
    `mem_push_ctx_capped` seam · default path byte-identical) and measures, over the SHIPPED
    buffer functions, what fraction of anchor pairs can ever be jointly resident.

    GATE ORDER IS LOAD-BEARING (frozen, sequential), mirroring `run_mi_screen`:
      1. `_wake_battery` runs the two controls FIRST — `plant_crossboundary` (anchors at a
         known 50-tick spacing: the instrument must FIRE, i.e. show a large cap-dependence)
         and `plant_null_stream` (every anchor on every tick, so cap-dependence is zero by
         construction: the instrument must REFUSE).
      2. Only if both certify is a corpus row reported. Otherwise INSTRUMENT-DEAD / INVALID
         and NO corpus number (positive-control-before-reading-a-negative ·
         phi-estimator-needs-zero-truth-pedestal).

    NO-TUNE-TO-GREEN: the anchor-set size is a knob that can move the answer, so the whole
    treatment is re-run at K and K//2 and the headline is refused unless every stratum AND
    every knob setting agree (`knob_dependent` / `stratum_dependent` name the disagreement
    instead of hiding it — the defect H_9844 had to add a gate for).
    """
    caps = sorted(set(opts["wake_caps"])) or [20, 64, 256]
    eps = opts["wake_eps"]
    source = opts["replay_source"]

    # ── ① controls FIRST — no corpus row is computed unless both certify ──────
    battery = _wake_battery(caps, eps)
    if not battery["certified"]:
        if not battery["plant_fires"]:
            status = "INSTRUMENT-DEAD"
            why = ("plant_crossboundary did NOT fire — anchors planted %d ticks apart show no "
                   "capacity dependence, so the measurement is not reading the ring buffer."
                   % _WAKE_PLANT_GAP)
        else:
            status = "INVALID"
            why = ("plant_null_stream did NOT refuse — a stream where every anchor is on every "
                   "tick has zero capacity-dependence by construction, so a non-zero reading "
                   "means the instrument manufactures one.")
    else:
        status = "CERTIFIED"
        why = "both controls behaved: the planted spacing fires, the saturated stream refuses."

    rows = []
    if battery["certified"]:
        for path in opts["corpus"]:
            knobs = []
            for k in (opts["wake_anchors"], max(4, opts["wake_anchors"] // 2)):
                strata, toks, n_recurring = _wake_anchor_strata(path, k, opts["wake_ticks"])
                if not strata:
                    knobs.append({"k": k, "underpowered": True, "n_recurring": n_recurring})
                    continue
                per_stratum = {}
                for name in ("top", "mid", "rare"):
                    per_stratum[name] = _wake_row(_wake_stream_for(toks, strata[name]),
                                                  caps, source, eps)
                knobs.append({"k": k, "n_recurring": n_recurring, "strata": per_stratum,
                              "reads_ceiling": {n: per_stratum[n].get("read_ceiling")
                                                for n in per_stratum}})
            usable = [x for x in knobs if not x.get("underpowered")]
            reads = [bool(v) for x in usable for v in x["reads_ceiling"].values()]
            row = {"path": path, "sha256": _mi_sha_of(path), "per_knob": knobs}
            if not reads:
                row["verdict"] = "UNDERPOWERED"
            elif all(reads):
                row["verdict"] = "CEILING-REAL"
            elif not any(reads):
                row["verdict"] = "CEILING-DEAD"
            else:
                row["verdict"] = "SPLIT"     # some stratum/knob reads it, some does not
            row["knob_dependent"] = bool(len(usable) > 1 and any(
                usable[0]["reads_ceiling"].get(n) != usable[1]["reads_ceiling"].get(n)
                for n in usable[0]["reads_ceiling"]))
            rows.append(row)

    out = {
        "instrument": "wake-coresidency",
        "hypothesis": "H_9842",
        "engine": "core/wake_memory.py (mem_push_ctx_capped · mem_working_window · "
                  "mem_record_emit · mem_recent_emits — the shipped functions, driven verbatim)",
        "status": status,
        "why": why,
        "battery": battery,
        "geometry": {"caps": caps, "replay_source": source, "eps": eps,
                     "anchors_per_stratum": opts["wake_anchors"], "ticks": opts["wake_ticks"]},
        "corpus": rows,
        "reaudit": {"argv": ["anima-py", "corpus"] + sys.argv[1:]},
        "scope": ("STRUCTURAL, not behavioural: this measures what the buffer CAN hold jointly, "
                  "never whether a model would use it. Two hard limits. (a) The live daemon "
                  "pushes a CLOCK TRIPLET, not content — cli/chat.py:2192 is "
                  "mem_push_ctx(wake_mem, [tick, stage, cell_count]) (H_9422) — so a "
                  "content-anchor stream is COUNTERFACTUAL: it measures the ceiling a "
                  "content-carrying percept would meet, and that percept does not exist yet. "
                  "(b) wake_memory has ZERO train entry point (ARCHITECTURE R12 census), so a "
                  "co-residency ceiling bounds a replay lane nobody has built; it is a "
                  "pre-condition on H_9841/H_9839, not a training result."),
        "reading": ("`working[C]` = fraction of anchor pairs (both anchors occur in the stream) "
                    "that are jointly resident in the cap-C FIFO at some tick. `episodic` = the "
                    "same over the append-only log = the uncapped refutation arm (1.0 by "
                    "construction ⟹ any working[C] < 1.0 is a capacity ceiling and nothing "
                    "else). `cap_delta` = working[max cap] - working[min cap]. CEILING-REAL "
                    "requires cap_delta > eps in EVERY stratum at EVERY knob setting; SPLIT "
                    "means the reading depends on which anchors you look at, and a SPLIT is a "
                    "result about the stream's gap distribution, not a licence to pick a "
                    "stratum."),
    }
    if opts["out"]:
        open(opts["out"], "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=2))
    print(json.dumps(out, ensure_ascii=False, indent=2))
    if not battery["certified"]:
        sys.exit(3)


def main():
    argv = sys.argv[1:]
    fmt, opts = _parse_args(argv)
    if fmt == "ngram-audit" or opts["ngram_recoverable_audit"]:
        if not opts["ngram_recoverable_audit"] or not opts["audit_train"] or not opts["panel"]:
            print("anima-py corpus ngram-audit --ngram-recoverable-audit "
                  "--audit-train TRAIN --panel PANEL [--codec codec.json] "
                  "[--audit-marker 안,않,못,아니] [--audit-min-coverage 0.10] [--out audit.json]")
            print("      H_9809 — absorbs lab/v3 H_004's verified theorem (oracle-fusable <=>")
            print("      n-gram-recoverable) as a production audit flag. Reports order-1 AND")
            print("      order-2 recoverability of the panel label from a Bayes lookup fit on")
            print("      TRAIN only, per tokenization arm, so a trivial bigram path is VISIBLE.")
            print("      TRAIN/PANEL accept `X => LABEL` arrow lines or an {\"items\":[{seed,gold}]}")
            print("      panel. Runs BEFORE any training — no checkpoint, $0.")
            sys.exit(2)
        run_ngram_audit(opts)
        return
    if fmt == "wake-coresidency":
        if not opts["corpus"]:
            print("anima-py corpus wake-coresidency --corpus PATH [--corpus PATH2 ...] "
                  "[--wake-buffer-cap 20 --wake-buffer-cap 64 --wake-buffer-cap 256] "
                  "[--replay-source working|episodic|both] [--wake-anchors 24] "
                  "[--wake-ticks 0] [--wake-eps 0.05] [--out wake.json]")
            print("      H_9842 — is the wake working ring buffer a co-occurrence ceiling?")
            print("      Recombination needs two concepts to CO-OCCUR, and core/wake_memory.py's")
            print("      working buffer is a FIFO whose capacity was a HARDCODED 20, so anchors")
            print("      more than 20 ticks apart can never be jointly resident — the memory-side")
            print("      twin of the trunk receptive-field bound (H_9836). --wake-buffer-cap makes")
            print("      the capacity a swept variable (repeat the flag); --replay-source episodic")
            print("      is the append-only UNCAPPED arm = the direct refutation arm.")
            print("      Controls run FIRST and the corpus row is refused unless both certify:")
            print("      plant_crossboundary (anchors 50 ticks apart · must FIRE) and")
            print("      plant_null_stream (every anchor every tick · must REFUSE).")
            print("      Anchors are reported in THREE frequency strata (top/mid/rare) at TWO")
            print("      anchor-set sizes, because picking one stratum would let the knob pick")
            print("      the verdict. $0 · no GPU · no ckpt · no forward pass.")
            print("      COST: the episodic arm drives the shipped mem_record_emit, which COPIES")
            print("      the whole log on every append (O(ticks^2)) — use --wake-ticks to cap a")
            print("      long stream (~6.5k ticks = ~6s; 56k ticks would not finish in minutes).")
            sys.exit(2)
        run_wake_coresidency(opts)
        return
    if fmt == "mi-screen":
        if not opts["corpus"]:
            print("anima-py corpus mi-screen --corpus PATH [--corpus PATH2 ...] "
                  "[--mi-win 4096] [--mi-span 2048] [--mi-estimator gzip|ppm|markov6|all] "
                  "[--mi-eps 0.02] [--mi-seg-lines N] [--mi-robust] [--out mi.json]")
            print("      H_9844 — compression-MI screener over core/mi_compress.py (H_9806).")
            print("      Measures what the STREAM carries across a segment boundary WITHOUT a")
            print("      forward pass, so 'the corpus has no joint information' and 'the model")
            print("      cannot reach it' stop being the same measurement (H_9304 could not")
            print("      split them). Runs the SHIPPED controls FIRST — plant_crossboundary")
            print("      (positive) and plant_null_stream (zero-truth pedestal) — and refuses")
            print("      to report the corpus row unless both certify. $0 · no GPU · no ckpt.")
            print("      PATH = a directory (one segment per file) or a file (blank-line split).")
            print("      --mi-seg-lines N segments a LINE-RECORD corpus into N-line blocks —")
            print("      anima's own procedural corpora carry ZERO blank lines, so without it")
            print("      the screener cannot segment the streams it exists to screen.")
            print("      --mi-robust re-runs the whole battery at 1/2 and 1/8 the block")
            print("      geometry and reports the MINIMUM over_floor. MEASURED: the sign")
            print("      flips with block size (flat en gzip -0.0020 @4096B vs +0.0312")
            print("      @512B; storebind +0.0195 @4096B vs +0.0000 @512B), so a single")
            print("      geometry lets the block size pick the verdict — tune-to-green.")
            sys.exit(2)
        run_mi_screen(opts)
        return
    if fmt == "study-replay":
        if not opts["transcript"] or not opts["corpus"] or not opts["out"]:
            print("anima-py corpus study-replay --transcript T.jsonl --corpus BASE.txt "
                  "[--corpus B2 ...] --out mix.txt [--study-frac 0.05] [--reps 40] "
                  "[--seed 7] [--scramble-seed 11]")
            print("      H_9520 — consolidation-CPT corpus from an `anima study` transcript.")
            print("      Emits the replay-mix corpus + C1 (replay-only) + C2 (scrambled-teacher)")
            print("      controls. Replay-mix is MANDATORY (corpus-py-1 ⑥⑦): study-only CPT kills")
            print("      abilities absent from the small corpus. Teacher content = `percept` lines")
            print("      ONLY (NOT the daemon's own emit_text — that is self-seed, p5).")
            sys.exit(2)
        mix, c1, c2, st = build_studyreplay(opts["transcript"], opts["corpus"], opts["study_frac"],
                                            opts["reps"], opts["seed"], opts["scramble_seed"])
        base = opts["out"]
        open(base, "w", encoding="utf-8").write(mix)
        open(base + ".c1_replayonly.txt", "w", encoding="utf-8").write(c1)
        open(base + ".c2_scrambled.txt", "w", encoding="utf-8").write(c2)
        meta = {
            "format": "study-replay", "transcript": opts["transcript"],
            "study_frac_requested": st["study_frac_req"], "study_frac_actual": st["study_frac_actual"],
            "reps": st["reps"], "seed": opts["seed"], "scramble_seed": opts["scramble_seed"],
            "teacher_lines": st["teacher_lines"], "teacher_pool_bytes": st["teacher_pool_bytes"],
            "substrate_emits": st["substrate_emits"], "base_pool_lines": st["base_pool"],
            "mix_bytes": st["mix_bytes"], "c1_bytes": st["c1_bytes"], "c2_bytes": st["c2_bytes"],
            "audit": {"c1_teacher_leak": st["c1_teacher_leak"], "c2_byte_match": st["c2_byte_match"]},
            "forget_strata": FORGET_STRATA["study-replay"],
            "controls": {
                "c1_replayonly": base + ".c1_replayonly.txt (teacher ABSENT · byte-matched · must NOT lift)",
                "c2_scrambled": base + ".c2_scrambled.txt (teacher word-shuffled · must NOT lift)",
            },
            "note": ("H_9520 consolidation CPT. MVP verdict = plumbing + byte-parity (NO growth claim). "
                     "The growth verdict is TERMINAL only via `anima-py evaluate` held-out reach Δ vs "
                     "C1/C2 + the FORGET gate over forget_strata (corpus-py-1 ⑦ (A))."),
        }
        _canon_dump(meta, open(base + ".meta.json", "w"))
        print("=== anima-py corpus study-replay (H_9520 consolidation CPT) ===")
        print("  teacher: %d percept line(s) (%d B pool) · %d substrate emit(s) · reps %d"
              % (st["teacher_lines"], st["teacher_pool_bytes"], st["substrate_emits"], st["reps"]))
        print("  mix: %d B (study %.1f%% requested / %.1f%% actual · rest = base replay from %d pool line(s))"
              % (st["mix_bytes"], st["study_frac_req"] * 100, st["study_frac_actual"] * 100, st["base_pool"]))
        print("  C1 replay-only: %s (%d B · teacher leak %d ✅)"
              % (base + ".c1_replayonly.txt", st["c1_bytes"], st["c1_teacher_leak"]))
        print("  C2 scrambled  : %s (%d B · byte-match=%s)"
              % (base + ".c2_scrambled.txt", st["c2_bytes"], st["c2_byte_match"]))
        print("  FORGET strata : %s" % " · ".join(FORGET_STRATA["study-replay"]))
        print("  meta: %s.meta.json" % base)
        floor = max(200000, st["mix_bytes"])
        print("  BUDGET_FLOOR_BYTES=%d" % floor)
        return
    if fmt == "xbind":
        if not opts["bridge_split"]:
            raise SystemExit("corpus xbind: only --bridge-split is implemented (H_9389 RUNTIME-BRIDGE L1).")
        if not opts["out"] or not opts["atoms"]:
            raise SystemExit("corpus xbind --bridge-split needs --out and --atoms.")
        text, st = build_bridgesplit(opts["atoms"], opts["reps"], opts["seed"],
                                     opts["split_seed"], opts["lang"],
                                     opts["polarity"], opts["assign_seed"],
                                     opts["decl_ablate"])
        with open(opts["out"], "w", encoding="utf-8") as fh:
            fh.write(text)
        base = opts["out"]
        json.dump(st["sdecl_manifest"], open(base + ".sdecl_flip1.json", "w"), ensure_ascii=False)
        json.dump(st["sop_manifest"], open(base + ".sop_flip1.json", "w"), ensure_ascii=False)
        json.dump(st["scpt_manifest"], open(base + ".scpt_flip1.json", "w"), ensure_ascii=False)
        open(base + ".cpt_forward.txt", "w", encoding="utf-8").write(st["cpt_forward"])
        open(base + ".cpt_reverse.txt", "w", encoding="utf-8").write(st["cpt_reverse"])
        open(base + ".cpt_neutral.txt", "w", encoding="utf-8").write(st["cpt_neutral"])
        json.dump({k: st[k] for k in ("lang", "n_atoms", "reps", "split_sizes", "arms",
                                      "lines", "bytes")},
                  open(base + ".arms.json", "w"), ensure_ascii=False, indent=1)
        print("=== corpus xbind --bridge-split (H_9389 L1) — lang=%s ===" % st["lang"])
        print("  atoms=%d  split S_op=%d S_decl=%d S_cpt=%d  lines=%d  bytes=%d"
              % (st["n_atoms"], st["split_sizes"]["S_op"], st["split_sizes"]["S_decl"],
                 st["split_sizes"]["S_cpt"], st["lines"], st["bytes"]))
        if opts["decl_ablate"]:
            print("  ⚠️ C-DECL-ABL CONTROL (H_9410) — the S_decl DECLARATION layer is ABLATED: those stems "
                  "now appear ZERO times in phase A (no declaration, no operator).")
            print("     The gate manifest is UNCHANGED (same questions). Frozen reading: the gate MUST return "
                  "to chance. If it does NOT ⟹ the signal cannot come from the (absent) declaration ⟹ surface "
                  "leak ⟹ ⚠️ LEAK-INVALID (instrument problem, NOT a verdict).")
            print("     NOT a training corpus for a rung — never read its gate as a rung result.")
        print("  phase-A corpus: %s  (train S_op%s)" % (base, "" if opts["decl_ablate"] else "+S_decl"))
        print("  phase-A GATE  : %s.sdecl_flip1.json  (operator held-out-in-A · %d rows)"
              % (base, len(st["sdecl_manifest"]["heldout"])))
        print("  alive control : %s.sop_flip1.json    (%d rows)" % (base, len(st["sop_manifest"]["heldout"])))
        print("  phase-B DV    : %s.scpt_flip1.json   (%d rows · chance before CPT)"
              % (base, len(st["scpt_manifest"]["heldout"])))
        print("  phase-B CPT   : %s.cpt_{forward,reverse,neutral}.txt" % base)
        # byte-budget floor (a trainer refuses below it) — same convention as other formats.
        floor = max(200000, st["bytes"])
        print("  BUDGET_FLOOR_BYTES=%d" % floor)
        return
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
    if fmt == "routeaudit":
        if not opts["atoms"]:
            print("usage: anima-py corpus routeaudit --atoms gt_atoms.json --out ra_manifest.json "
                  "[--ctx-bytes 64]")
            print("      H_9355 LOCUS-CAUSAL — the manifest for `anima-py evaluate --route-audit`.")
            print("      5 surfaces x every atom: flip0(declarative) · negL/negZ(operator) ·")
            print("      negJ(string-twin, operator does NOT run) · ped(inert byte-matched suffix).")
            print("      The last two are the controls that keep a trivial string effect from")
            print("      being read as a two-lane locus split.")
            sys.exit(2)
        man = build_routeaudit(opts["atoms"], opts["ctx_bytes"])
        out = opts["out"] or "route_audit_manifest.json"
        json.dump(man, open(out, "w"), ensure_ascii=False)
        n_by = {}
        for it in man["items"]:
            n_by[it["split"]] = n_by.get(it["split"], 0) + 1
        print("=== anima-py corpus routeaudit — H_9355 route-audit manifest ===")
        print("wrote %s — %d items · win %dB · %s" % (out, len(man["items"]), man["win"],
              " · ".join("%s %d" % (k, v) for k, v in sorted(n_by.items()))))
        print("  surfaces: " + " · ".join(t for t, _m, _f, _w in _ROUTE_SURFACES))
        sys.exit(0)
    if fmt == "twinnec":
        if not opts["atoms"]:
            print("usage: anima-py corpus twinnec --atoms gt_atoms.json --out tn_manifest.json "
                  "[--surface flip1_suffix|flip0|flip1_prefix] [--seed 7]")
            print("      H_9361 TWIN-NECESSITY candidate manifest for `anima-py evaluate --twin-screen`.")
            print("      SEEN stems, byte-matched opposite-polarity STEM pairs per byte-length bucket")
            print("      (option A — same carrier morpheme). Windows = raw seed bytes (screener right-aligns).")
            sys.exit(2)
        man = build_twinnec(opts["atoms"], opts["surface"], opts["seed"])
        out = opts["out"] or "twinnec_manifest.json"
        json.dump(man, open(out, "w"), ensure_ascii=False)
        print("=== anima-py corpus twinnec — H_9361 TWIN-NECESSITY candidates ===")
        print("wrote %s — surface %s · %d SEEN stems · Y=%d disjoint pairs · buckets(L→pol0,pol1) %s"
              % (out, man["surface"], len(man["items"]), man["Y"], man["buckets"]))
        if man["Y"] < 30:
            print("  ⚠ Y=%d — byte-matched pairs are inventory-limited (SEEN pool small); the n=9 "
                  "stop-condition governs (card H_9361)." % man["Y"])
        sys.exit(0)
    if fmt == "deltainj":
        if not opts["atoms"]:
            print("usage: anima-py corpus deltainj --atoms gt_atoms.json --out di_manifest.json")
            print("      H_9397 Δ-INJECT manifest for `anima-py evaluate --delta-pregate`/`--delta-inject`.")
            print("      Per stem: carrier(지 않다)/filler(고 있다)/filler2(게 되다) — 3 byte-matched 10B")
            print("      operator-site morphemes sharing prefix+stem+query. SEEN=Δ est · held-out=DV.")
            sys.exit(2)
        man = build_deltainj(opts["atoms"])
        out = opts["out"] or "deltainj_manifest.json"
        json.dump(man, open(out, "w"), ensure_ascii=False)
        print("=== anima-py corpus deltainj — H_9397 Δ-INJECT (carrier vs neutral filler) ===")
        print("wrote %s — %d items (SEEN %d · held-out %d) · op-site 10B · carrier %s vs filler %s (ctrl %s)"
              % (out, len(man["items"]), man["n_seen"], man["n_heldout"],
                 man["carrier"], man["filler"], man["filler2"]))
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
    if fmt == "c34":
        if not (opts["atoms"] and opts["corpus"]):
            print("anima corpus c34 --atoms gt_atoms_en.json --corpus C.txt --lang en "
                  "--seed 7 --out c34_en.txt")
            sys.exit(2)
        text, st = build_c34(opts["atoms"], opts["corpus"], opts["lang"], opts["seed"])
        if opts["out"]:
            with open(opts["out"], "w", encoding="utf-8") as fh:
                fh.write(text)
            _write_budget_floor(opts["out"], fmt, opts["lang"])
        print("anima corpus c34 [%s]: %d lines / %d B  (arrow %d, %d negated · natural %d)"
              % (st["lang"], st["lines"], st["bytes"], st["arrow"], st["arrow_negated"],
                 st["natural"]))
        print("  held-out natural exposure %.1f/stem (min %d, floor %d)  ·  SEEN %.1f/stem"
              % (st["held_nat_per_stem"], st["held_nat_min"], st["I3_floor"],
                 st["seen_nat_per_stem"]))
        print("  I1 held-out in an arrow line     : %d  ✅" % st["I1_held_in_arrow"])
        print("  I2 held-out in a NEGATED context : %d  ✅  (%d negated sentences dropped)"
              % (st["I2_held_in_negated"], st["neg_sentences_dropped"]))
        print("  I3 natural-exposure floor        : every stem >= %d  ✅" % st["I3_floor"])
        print("  ko C34 mirror: arrow 960 (480 negated) · held-out natural 48.8/stem · 160,086 B")
        return

    if fmt == "atoms":
        if opts["max_atoms"]:
            # H_9410 — one-shot scaled EN miner: mine N clean polarity stems + RANDOM balanced polarity.
            if not opts["corpus"]:
                print("anima-py corpus atoms --lang en --max-atoms 3072 --corpus en_general.txt "
                      "[--assign-seed 0] [--min-occ 50] --out gt_atoms_en_N.json")
                sys.exit(2)
            obj, st = build_atoms_scaled(opts["corpus"], opts["lang"], opts["max_atoms"],
                                         opts["min_occ"], opts["assign_seed"])
            if opts["out"]:
                json.dump(obj, open(opts["out"], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            d = st["dropped"]
            print("=== anima-py corpus atoms --max-atoms (H_9410 scaled EN miner · lang=%s) ===" % st["lang"])
            print("  requested N=%d  ACCEPTED=%d%s  (pos %d : neg %d)  polarity=assigned(seed %d)"
                  % (st["requested"], st["accepted"],
                     "  🧱 DRIED-UP (corpus ceiling)" if st["dried_up"] else "",
                     st["n_pos"], st["n_neg"], st["assign_seed"]))
            print("  mining: %d frame-candidates -> %d cleared min_occ=%d -> greedy gates"
                  % (st["frame_candidates"], st["mined_kept"], st["min_occ"]))
            print("  dropped by gate: len=%d stop=%d G-CARRIER=%d G-SUBSTR=%d G-DERIV=%d"
                  % (d["len"], d["stop"], d["carrier"], d["substr"], d["deriv"]))
            print("  split: train=%d heldout=%d  gate chance_sd=%.4f  -> %s"
                  % (st["n_train"], st["n_heldout"], st["chance_sd_gate"], opts["out"] or "(stdout)"))
            print("  G-OCCUR ✅ word-boundary (mine_lexicon word-level) · G-SUBSTR ✅ greedy no-nest · "
                  "G-DERIV ✅ affix-pair · G-BALANCE ✅ random balanced (polarity DECOUPLED from form)")
            if st["dried_up"]:
                print("  ⚠ corpus ran out before N — ACCEPTED=%d IS the axis-1 ceiling (report, do not pad)."
                      % st["accepted"])
            return
        if opts["collision_split"]:
            if not opts["atoms"]:
                print("anima corpus atoms --collision-split --atoms gt_atoms.json "
                      "--nonce-fillers 3 --seed 7 --out coll_manifest.json")
                sys.exit(2)
            cen, man = build_collision_split(opts["atoms"], opts["nonce_fillers"],
                                             opts["seed"], opts["win"])
            d = cen["design"]
            print("=== anima corpus atoms --collision-split — V3 STEM-COLLISION (H_9354) ===")
            print("--- GATE: the NATURAL held-out x SEEN byte-LCP census ---")
            print("  seen=%d  held-out=%d   byte-LCP histogram: %s"
                  % (cen["n_seen"], cen["n_heldout"],
                     "  ".join("%sB:n=%d" % (k, v) for k, v in cen["lcp_byte_hist"].items())))
            print("  max byte-LCP with ANY seen stem = %d B  (ko = 3 B/syllable)"
                  % cen["max_lcp_bytes"])
            print("  n in a SIGNAL stratum (>= 3 B = >= 1 shared syllable) = %d"
                  % cen["signal_stratum_n"])
            if cen["degenerate"]:
                print("  ⛔ DEGENERATE — the natural collision split has n=0 in EVERY signal")
                print("     stratum. This is by construction, not bad luck: build_atoms()'s")
                print("     G-SUBSTR gate FORBIDS a stem nesting in another, so the frozen atom")
                print("     set was built to have no stem-stem collision. A trend test over empty")
                print("     strata is NOT a negative result — it is no result. The natural split")
                print("     is therefore emitted as a CENSUS ONLY and may never carry a verdict")
                print("     (power-before-negative-verdict).")
            print("--- INSTRUMENT: the constructed prefix-graded NONCE ladder ---")
            print("  donors (3-syllable SEEN stems): %d  = %d pos / %d neg  [balanced -> a constant"
                  % (len(d["donors"]), d["donor_pos"], d["donor_neg"]))
            print("   response bias cancels in the stratum mean]")
            print("  fillers/donor=%d  surfaces=%s  (negJ = the NO-operator control surface)"
                  % (d["fillers"], ",".join(d["surfaces"])))
            print("  k=shared syllables: k0=0B (length-matched unrelated = neutral control) ·")
            print("   k1=3B · k2=6B (the graded near-misses the trend reads) · k3=9B = the donor")
            print("   ITSELF (positive control: operator known alive, SEEN flip1 0.98-1.00)")
            print("  k=1 dropped %d ambiguous donor(s) (prefix shared with an OPPOSITE-polarity"
                  % len(d["k1_dropped_ambiguous"]))
            print("   seen stem -> would drag the DV to zero and MANUFACTURE the null): %s"
                  % ", ".join(s for s, _ in d["k1_dropped_ambiguous"]))
            print("  rows/stratum: %s" % "  ".join("%s=%d" % kv
                                                   for kv in sorted(d["rows_per_stratum"].items())))
            print("  every nonce is 3 syllables = 9 B at EVERY k (a_korean_byte_budget: length is")
            print("   matched across the whole ladder, so no stratum is confounded with length)")
            if opts["out"]:
                json.dump(man, open(opts["out"], "w", encoding="utf-8"),
                          ensure_ascii=False, indent=1)
                cp = opts["out"].replace(".json", "") + ".census.json"
                json.dump(cen, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
                print("wrote %s (%d rows) + %s" % (opts["out"], d["n_rows"], cp))
            print("  score with:  anima-py evaluate <base.clm> --xbind %s --n-decode %d "
                  "--n-sampled 0 --out <eval.json>" % (opts["out"] or "M.json",
                                                       d["n_decode_required"]))
            return
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

    if fmt == "consult-variants":
        # H_9407 C/D control stores for the --consult-decode 5-arm measurement (Fable spec).
        man, sto, out_dir = opts.get("manifest"), opts.get("store"), opts.get("out_dir")
        if not out_dir or (not man and not sto):
            print("anima corpus consult-variants (--manifest EVAL.json | --store correct.json) "
                  "--out-dir DIR [--seed 7]", file=sys.stderr)
            print("      emits correct/scram_pol/wrong_atom.json + consult_variants.manifest.json "
                  "(H_9407 arms A/B · C · D). C=flip-all pol · D=Sattolo cycle over sorted atoms.",
                  file=sys.stderr)
            sys.exit(2)
        st = build_consult_variants(man, sto, opts["seed"])
        if os.path.exists(os.path.join(out_dir, "consult_variants.manifest.json")):
            # a redraw over a USED variant set = contamination (no --force).
            print("anima corpus consult-variants: REFUSE — %s already holds a variant set (a redraw "
                  "over a used set is contamination)" % out_dir, file=sys.stderr)
            sys.exit(2)
        os.makedirs(out_dir, exist_ok=True)
        shas = {}
        for name in ("correct", "scram_pol", "wrong_atom"):
            fp = os.path.join(out_dir, name + ".json")
            with open(fp, "w", encoding="utf-8") as fh:
                _canon_dump(st[name], fh)
            shas[name] = hashlib.sha256(open(fp, "rb").read()).hexdigest()
        src_sha = hashlib.sha256(open(st["source_path"], "rb").read()).hexdigest()
        manifest = {
            "format": "consult-variants-v1",
            "source": {"mode": st["source_mode"], "path": st["source_path"], "sha256": src_sha},
            "seed": st["seed"], "n_atoms": st["n_atoms"], "n_pol_match": st["n_pol_match"],
            "pol_marginal": st["pol_marginal"],
            "stores": {k: {"path": k + ".json", "sha256": shas[k]}
                       for k in ("correct", "scram_pol", "wrong_atom")},
            "transforms": {"scram_pol": {"kind": "flip-all", "seed": None, "n_changed": st["n_atoms"]},
                           "wrong_atom": {"kind": "sattolo-cycle", "order": "sorted(atoms) codepoint",
                                          "seed": st["seed"], "n_fixed_points": 0,
                                          "n_pol_match": st["n_pol_match"]}},
            "byte_census": {"key_bytes_min": st["key_bytes"]["min"], "key_bytes_max": st["key_bytes"]["max"]},
            "arms": [
                {"arm": "P", "store": None, "flags": "--xbind <m>"},
                {"arm": "E", "store": None, "flags": "--xbind <m> --consult-decode"},
                {"arm": "A", "store": "correct.json", "flags": "--xbind <m> --consult correct.json --consult-decode"},
                {"arm": "B", "store": "correct.json",
                 "flags": "--xbind <m> --consult correct.json --consult-decode --consult-decode-filler <T_dec>",
                 "note": "filler>=T_dec makes B bitwise==E (instrument self-check)"},
                {"arm": "C", "store": "scram_pol.json", "flags": "--xbind <m> --consult scram_pol.json --consult-decode"},
                {"arm": "D", "store": "wrong_atom.json", "flags": "--xbind <m> --consult wrong_atom.json --consult-decode"}]}
        mfp = os.path.join(out_dir, "consult_variants.manifest.json")
        with open(mfp, "w", encoding="utf-8") as fh:
            _canon_dump(manifest, fh)
        print("=== anima corpus consult-variants (H_9407 C/D controls) ===")
        print("  n_atoms=%d  pol correct=%s scram=%s wrong=%s"
              % (st["n_atoms"], st["pol_marginal"]["correct"], st["pol_marginal"]["scram_pol"],
                 st["pol_marginal"]["wrong_atom"]))
        print("  C=flip-all n_changed=%d · D=sattolo seed=%d fixed_points=0 pol_match=%d/%d"
              % (st["n_atoms"], st["seed"], st["n_pol_match"], st["n_atoms"]))
        print("  AUDIT ✅ 7/7 (keyset 3-way · C only-pol · C all-changed · D multiset · D no-fixpt · D no-A-collision)")
        for k in ("correct", "scram_pol", "wrong_atom"):
            print("  %-11s %s.json  sha256=%s" % (k, k, shas[k][:16]))
        print("  manifest -> %s (6 arms P/E/A/B/C/D)" % mfp)
        return

    if fmt not in ("derivtrace", "flat", "ground", "ground_lie", "ground_keep", "ground_keep_lie",
                   "ground_seenswap", "ground_carrierswap", "ground_hocarrier", "consult-variants",
                   "routeaudit", "atoms", "c34", "storebind", "g6bind", "counterfactual-decl",
                   "bindpanel", "weavepanel", "falsidrill", "dreamgen"):
        print("usage: anima corpus <derivtrace|flat|ground|ground_lie|ground_keep|ground_keep_lie|ground_seenswap|ground_carrierswap|ground_hocarrier|valence|bindlocus|routeaudit|atoms|c34|storebind|counterfactual-decl|bindpanel|weavepanel|dreamgen|ngram-audit> --out PATH")
        print("      dreamgen --lang en --out c.txt --dream-target "
              "{planted|pedestal|midpoint|rule-derived|shuffled} [--dream-nights 24] [--seed 7]"
              " [--dream-anchors synthetic|real:<ckpt.clm>]")
        print("             H_9839 — the dream node's COMPOSITION LAW as the manipulated variable.")
        print("             core/dream_compose.py blends two co-replayed anchors by coord midpoint")
        print("             — its own header calls that 'a designed geometric law (NOT a learned")
        print("             semantic insight, c9)' — and a midpoint is ADDITIVE by construction,")
        print("             which is where H_9304 measured non-additive information ~ 0. Arms:")
        print("             midpoint (the pre-registered FAILURE baseline) · rule-derived (the")
        print("             child is the derivation of a DECLARED rule over the pair) · shuffled")
        print("             (identical marginals, pairing destroyed) + two INSTRUMENT controls,")
        print("             planted (must FIRE) and pedestal (must REFUSE), which gate the read.")
        print("             Judge: anima-py corpus mi-screen --corpus c.txt --mi-robust (no ckpt).")
        print("      weavepanel --out panel.json [--weave-families f1,f2] [--weave-max N] [--seed 7]")
        print("             H_9825 — the parametric ρ·weave held-out recombination panel. The frozen")
        print("             `_WEAVE` battery is TWELVE items (6 on the ko lane H_9327 walled), so one")
        print("             item is 0.083 of the value against a 0.30 bar with a 0.15 control cap.")
        print("             Families: " + ",".join(_WP_FAMILIES) + " (>=2 carriers each — a single")
        print("             carrier makes the carrier axis collinear with the composition axis).")
        print("             Consumed by `anima-py evaluate <clm> --rho-axon --weave-panel panel.json`.")
        print("      bindpanel --lang en --out c.txt [--bind-k 6] [--n-blocks 4000] [--seed 7]")
        print("             H_9810 — the HELD-OUT BINDING PANEL for the H_9805 tension-field arms.")
        print("             K stacked number-concord edges per sentence; gold = agreement-marker XOR")
        print("             singular-noun position, both balanced at 0.5. LENGTH-CODED on purpose:")
        print("             core/tension_field.py derives the field from the WHITESPACE MASK alone,")
        print("             so a lexically-keyed panel would hand the field 0 bits. Emits the drill")
        print("             corpus + <out>.panel.json (score: evaluate --bind-panel) +")
        print("             <out>.codebook.json (verify: evaluate --free-slot-score).")
        print("      counterfactual-decl --lang en --out c.txt [--seed 7] [--held-out 32,8]")
        print("             [--n-blocks 4000] [--stems-per-episode 4] [--eval-episodes 16]")
        print("             H_9800 — every episode RE-ASSIGNS stem->sense and operator->role, so a")
        print("             parametric cache reads exactly the realized chance and runtime lookup is")
        print("             the only CE minimiser. --held-out I,J = held-out STEM,OPERATOR names.")
        print("             Score with: anima-py evaluate <clm> --decl-flip c.txt.decl.json")
        print("      routeaudit --atoms gt_atoms.json --out ra_manifest.json   (H_9355 route audit)")
        print("      ground_hocarrier --atoms gt_atoms_en.json --lang en --seed 7 --split-seed 1 --out ho.txt")
        print("             H_9334's operator-key write, taken to the stems the operator NEVER met.")
        print("             H_9346 measured the wall: on a held-out stem the fact LANDS (flip0 1.0000)")
        print("             and the operator is ALIVE on the same `not X` surface (SEEN flip1 1.0000),")
        print("             yet the model ECHOES the planted polarity and ignores `not` (91-98%).")
        print("             The operator does not fail to look the fact up — it never fires. It is")
        print("             gated on the STEM. This asks whether that gate can be OPENED by writing")
        print("             the fact in the operator's own key.")
        print("               arm hoc  12  declarative + carrier `never {s}`   THE MANIPULATION")
        print("               arm null 12  declarative + `oddly {s}`           same label exposure, no key")
        print("               arm decl 16  declarative only                    = H_9346, must ECHO")
        print("             Scored on `not {s}` and `certainly not {s}` — surfaces the carrier never")
        print("             contains. Emits <out>.eval.json (score with `evaluate --xbind`) and")
        print("             refuses to write if a scored prompt leaks or the suffix window is not 50/50.")
        print("             ⚠️ A pass means the operator's trigger set is WRITABLE for a new stem, NOT")
        print("             that the model can compose a declaratively-known fact (that is H_9346, 🧱).")
        print("      c34 --atoms gt_atoms_en.json --corpus C.txt --lang en --seed 7 --out c34.txt")
        print("             the PRETRAINING corpus: natural sentences + arrow lines. Every number is")
        print("             MIRRORED from a census of the real ko C34, not invented: arrow 960 (480")
        print("             negated, SEEN stems only) · held-out natural exposure 48/stem · held-out")
        print("             stems appear in an arrow line ZERO times. The builder CHECKS its own")
        print("             premise and refuses to emit on a violation — I1 (no held-out in an arrow)")
        print("             I2 (no held-out in a NEGATED context, operator surfaces AND derivational")
        print("             un-/in-/-less — `불편하` taught the KO model a negation it never should")
        print("             have seen) I3 (every stem clears the natural-exposure floor, else FAIL).")
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
        print("  storebind              --out c.txt [--n-blocks N] [--store-slots K] [--seed S] [--lang en] [--entity-pool POOL.txt]")
        print("      H_9423 co-trained store-lookup bridge (EN-only). --entity-pool (H_9683) replaces")
        print("      the builtin CVCVC nonce enumeration with an external pool — ONE ascii atom per")
        print("      line, order preserved, no duplicates, at least n_pool atoms. Every contract is")
        print("      unchanged on that pool: interleaved disjoint train/held-out · store_slots <=")
        print("      held-out · the C0-a zero-leak hard-assert. On natural vocabulary that assert is")
        print("      SUBSTRING-based, so a held-out atom nested in a train atom (`art` ⊂ `start`)")
        print("      ABORTS the build rather than ship a forged 0-shot stratum (corpus-py-1 ⑩).")
        print("      Omitting the flag is byte-identical to every existing storebind corpus.")
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
        print("  ground_carrierswap     --atoms gt_atoms.json [--reps N] [--replay N] [--seed S] [--split-seed S] [--carrier-only | --held-swap [--decl-only] [--held-n N]]")
        print("      --held-n N = held-out swap-arm stem count (default 12); N<12 isolates co-train")
        print("                  compositional interference (H_9751; N=1 = single-stem write crack)")
        print("      --held-swap = H_9339 — the swap arm is drawn from the HELD-OUT pool (single variable")
        print("      vs C4); the 12 SEEN stems C4 wrote become `preserve` (0x written, the matched")
        print("      G-PRESERVE stratum). --decl-only (with --held-swap) = HO-DECL: swap stems written")
        print("      through the DECLARATIVE key only (C3's write, held pool, H_9327 reproduction).")
        print("      --carrier-only = C5-REVERSE (H_9353) — the last empty cell of the C3/C4 2x2.")
        print("      Writes the inverted polarity through the CARRIER (operator) key ONLY — the swap")
        print("      and keep arms lose their declarative arrow — and scores the DECLARATIVE surface")
        print("      (`이 영화 {s}고 => `), which is now exposure-0 for those stems. ONE-STORE predicts")
        print("      the declarative read is pulled to the NEW polarity (a shared value); TWO-LANE")
        print("      predicts it keeps the OLD one while the SAME ckpt's operator answers NEW — a")
        print("      within-model DISSOCIATION. Emits .flip0.json (DV) + .carrier.json (G-LAND landing")
        print("      gate) + .flip1.json, and audits BOTH directions: a DV prompt must be ABSENT from")
        print("      the corpus, a readback-gate prompt must be PRESENT (a gate that reads nothing back")
        print("      gates nothing — corpus-py-1 ⑦). Held-out arrows are KEPT: they hold the declarative")
        print("      surface alive through a carrier-heavy CPT, and a dead readout is INVALID, not a wall.")
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
        print("      Emits <out>.flip1.json + <out>.write.json — the `anima-py evaluate --xbind` manifests,")
        print("      drawn from the SAME arm split (byte-audited == C3), so arm<->manifest can never drift.")
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

    if fmt == "ground_hocarrier":
        if not opts["atoms"]:
            print("anima corpus ground_hocarrier: --atoms gt_atoms.json is required")
            sys.exit(2)
        text, st = build_hocarrier(opts["atoms"], opts["reps"], opts["replay"],
                                   opts["seed"], opts["split_seed"], lang=opts["lang"])
        open(opts["out"], "w", encoding="utf-8").write(text)
        print("anima corpus ground_hocarrier: lang=%s lines=%d bytes=%d leaks=0 -> %s"
              % (opts["lang"], st["lines"], st["bytes"], opts["out"]))
        for k, _ in HOCARRIER_ARMS:
            print("  %-5s n=%2d  %s" % (k, len(st["arms"][k]), " ".join(st["arms"][k])))
        # The suffix-window census is PRINTED, not assumed. If these two counts are not equal, a
        # suffix-only reader can win the DV without ever consulting the operator, and the run is void
        # before it starts (see build_hocarrier's header — this balance IS the experiment).
        cen = st["suffix_window_census"]
        bad = {s: c for s, c in cen.items() if c["declarative_label"] != c["operator_label"]}
        any_s = next(iter(cen.values()))
        print("  suffix window `<stem> => <label>`: declarative=%d operator=%d per hoc stem  %s"
              % (any_s["declarative_label"], any_s["operator_label"],
                 "✅ balanced — a suffix-only reader scores chance here"
                 if not bad else "⛔ IMBALANCED on %d stem(s)" % len(bad)))
        if bad:
            print("anima corpus ground_hocarrier: the suffix window is not 50/50 — a reader that "
                  "never looks left of the stem could win the DV. Refusing.", file=sys.stderr)
            sys.exit(2)
        man_path = opts["out"] + ".eval.json"
        json.dump(st["eval_manifest"], open(man_path, "w"), ensure_ascii=False)
        json.dump({k: st[k] for k in ("held", "lines", "bytes", "arms", "carrier_reps",
                                      "suffix_window_census")},
                  open(opts["out"] + ".arms.json", "w"), ensure_ascii=False, indent=1)
        n = len(st["eval_manifest"]["heldout"])
        print("  eval manifest -> %s (%d rows)" % (man_path, n))
        print("  score it with:  anima-py evaluate <ckpt> --xbind %s --n-decode %d" % (man_path, n))
        return 0

    if fmt == "ground_carrierswap":
        if not opts["atoms"]:
            print("anima corpus ground_carrierswap: --atoms gt_atoms.json is required")
            sys.exit(2)
        text, st = build_carrierswap(opts["atoms"], opts["reps"], opts["replay"],
                                     opts["seed"], opts["split_seed"], opts["carrier_only"],
                                     opts["held_swap"], opts["decl_only"], opts["held_n"])
        if st.get("flip0_leaks"):
            # C5-REVERSE: the DV is the DECLARATIVE surface, so a swap/keep/untouched declarative
            # prompt in the corpus would hand the model the answer it is supposed to infer.
            print("anima corpus ground_carrierswap --carrier-only: LEAK — %d DV (flip0) prompt(s) "
                  "appear in the corpus" % len(st["flip0_leaks"]), file=sys.stderr)
            for x in st["flip0_leaks"][:5]:
                print("    %s" % x, file=sys.stderr)
            sys.exit(2)
        if st.get("carrier_only") and st["readback_present"] != st["readback_n"]:
            # The inverse audit: a READBACK gate (affirm/heldR declarative · swap/keep carrier) whose
            # prompt is NOT in the corpus gates nothing at all. Fail loud rather than ship a fake gate.
            print("anima corpus ground_carrierswap --carrier-only: BROKEN GATE — %d/%d readback "
                  "prompts are absent from the corpus (a readback gate must read something back)"
                  % (st["readback_present"], st["readback_n"]), file=sys.stderr)
            sys.exit(2)
        if st["measured_prompt_leaks"]:
            # The design rests on this: a scored prompt must never be in the corpus, or a NEW read is
            # taught rather than composed. Refuse to write a corpus that would void the run.
            print("anima corpus ground_carrierswap: LEAK — %d scored prompt(s) appear in the corpus"
                  % len(st["measured_prompt_leaks"]), file=sys.stderr)
            for x in st["measured_prompt_leaks"][:5]:
                print("    %s" % x, file=sys.stderr)
            sys.exit(2)
        if st.get("ho_contradiction_leaks"):
            # --held-swap plant integrity: a swap stem's TRUE-polarity declarative line fights the
            # INVERTED plant, making the written value an undefined mixture — refuse (corpus-py-1).
            print("anima corpus ground_carrierswap --held-swap: PLANT CONTRADICTION — %d TRUE-polarity "
                  "declarative line(s) for a swap stem are in the corpus (the plant is undefined)"
                  % len(st["ho_contradiction_leaks"]), file=sys.stderr)
            for x in st["ho_contradiction_leaks"][:5]:
                print("    %s" % x, file=sys.stderr)
            sys.exit(2)
        if st.get("held_swap") and st["ho_readback_present"] != st["ho_readback_n"]:
            # A G-WRITE gate whose prompt is not in the corpus gates nothing (corpus-py-1 ⑦).
            print("anima corpus ground_carrierswap --held-swap: BROKEN GATE — %d/%d G-WRITE readback "
                  "prompts absent from the corpus (a readback gate must read something back)"
                  % (st["ho_readback_present"], st["ho_readback_n"]), file=sys.stderr)
            sys.exit(2)
        open(opts["out"], "w", encoding="utf-8").write(text)
        mode = ("C5-REVERSE (--carrier-only)" if st["carrier_only"] else
                "HO-DECL (--held-swap --decl-only)" if st.get("decl_only") else
                "HO-CARRIER (--held-swap)" if st.get("held_swap") else "C4")
        print("anima corpus ground_carrierswap [%s]: lines=%d bytes=%d leaks=0 untouched_n=%d -> %s"
              % (mode, st["lines"], st["bytes"], st["untouched_n"], opts["out"]))
        print("  forget-gate power: 0 flips -> 95%% UCB on SEEN forgetting = 3/%d = %.1f%% (rule of three)"
              % (st["untouched_n"], 300.0 / st["untouched_n"]))
        for k in ("swap", "preserve", "affirm", "keep", "untouched"):
            if k in st["arms"]:
                print("  %-10s n=%2d  %s" % (k, len(st["arms"][k]), " ".join(st["arms"][k])))
        arms_st = {k: st[k] for k in ("held", "lines", "bytes", "arms", "untouched_n", "carrier_only")}
        for k in ("held_swap", "decl_only"):
            if st.get(k):
                arms_st[k] = st[k]
        json.dump(arms_st, open(opts["out"] + ".arms.json", "w"), ensure_ascii=False, indent=1)
        # Eval manifests from the SAME arm draw (a_experiment_engine_native): the fire scores these
        # with `anima-py evaluate --xbind`, so the arm<->manifest split can never drift (C3 hand-built
        # this on a pod; wiring it here makes a passing result already reproducible).
        f1_path = opts["out"] + ".flip1.json"
        json.dump(st["flip1_manifest"], open(f1_path, "w"), ensure_ascii=False)
        if not st["carrier_only"]:
            w_path = opts["out"] + ".write.json"
            json.dump(st["write_manifest"], open(w_path, "w"), ensure_ascii=False)
            print("  eval manifests -> %s (%d flip1) · %s (%d write)"
                  % (f1_path, len(st["flip1_manifest"]["heldout"]),
                     w_path, len(st["write_manifest"]["heldout"])))
            if st.get("held_swap") and not st.get("decl_only"):
                # HO-CARRIER G-WRITE = carrier readback (>= 11/12); C4's w0 write is the
                # declarative precondition, this is the operator-key landing gate (card).
                c_path = opts["out"] + ".carrier.json"
                json.dump(st["carrier_manifest"], open(c_path, "w"), ensure_ascii=False)
                print("  G-WRITE manifest -> %s (%d carrier readback: swapC>=11/12 gates, keepC=twin)"
                      % (c_path, len(st["carrier_manifest"]["heldout"])))
            if st.get("held_swap"):
                print("  audit  plant-contradiction: 0 ✅   G-WRITE readback in corpus: %d/%d ✅   "
                      "preserve n=%d (0x-CPT G-PRESERVE stratum = C4's swap stems)"
                      % (st["ho_readback_present"], st["ho_readback_n"], len(st["arms"]["preserve"])))
            return 0
        # C5: the declarative surface is the DV, so `.write.json` (a C4 readback gate on a line C5
        # never writes) would be a nonsense file — it is NOT emitted. `.flip0.json` replaces it.
        f0_path, c_path = opts["out"] + ".flip0.json", opts["out"] + ".carrier.json"
        json.dump(st["flip0_manifest"], open(f0_path, "w"), ensure_ascii=False)
        json.dump(st["carrier_manifest"], open(c_path, "w"), ensure_ascii=False)
        print("  eval manifests -> %s (%d flip0 = THE DV) · %s (%d carrier = G-LAND) · %s (%d flip1)"
              % (f0_path, len(st["flip0_manifest"]["heldout"]),
                 c_path, len(st["carrier_manifest"]["heldout"]),
                 f1_path, len(st["flip1_manifest"]["heldout"])))
        print("  DV      swap|w0,w1,w2 on the DECLARATIVE surface — margin>0 = the carrier write "
              "reached it (ONE STORE); margin<0 = the OLD polarity survives (TWO LANES)")
        print("  G-LAND  swapC|cT,cG,cK >= 11/12 (the write must have landed) · "
              "G-ALIVE keep+untouched|w* = TRUE polarity >= 5/6 (both models predict it unmoved)")
        print("  audit   DV prompts in corpus: 0 ✅   readback prompts in corpus: %d/%d ✅   "
              "heldR n=%d (declarative read-path aliveness)"
              % (st["readback_present"], st["readback_n"], len(st["heldr"])))
        return 0

    if fmt == "g6bind":
        # H_9694 (R2) — the 2-arm lever that re-earns kill#6's bind Δ debris through --fan-bind.
        if not opts["out"]:
            print("anima corpus g6bind: --out c.txt is required", file=sys.stderr)
            sys.exit(2)
        arm = opts.get("arm") or "targeted"
        text, st = build_g6bind(opts["n_blocks"], opts["seed"], opts["lang"], arm)
        open(opts["out"], "w", encoding="utf-8").write(text)
        mj = opts["out"] + ".meta.json"
        json.dump({"fmt": "g6bind", "arm": st["arm"], "lang": st["lang"], "seed": st["seed"],
                   "bytes": st["bytes"], "lines": st["lines"], "n_blocks": st["n_blocks"],
                   "max_line_bytes": st["max_line_bytes"], "fixed_points": st["fixed_points"],
                   "frame_multiset_sha": st["frame_multiset_sha"],
                   "claim_multiset_sha": st["claim_multiset_sha"]},
                  open(mj, "w", encoding="utf-8"), ensure_ascii=False)
        print("anima corpus g6bind [%s · arm=%s]: blocks=%d lines=%d bytes=%d max_line=%dB "
              "fixed_points=%d -> %s"
              % (st["lang"], st["arm"], st["n_blocks"], st["lines"], st["bytes"],
                 st["max_line_bytes"], st["fixed_points"], opts["out"]))
        print("  byte-match witness: frame_multiset_sha=%s · claim_multiset_sha=%s"
              % (st["frame_multiset_sha"], st["claim_multiset_sha"]))
        print("  → run BOTH arms at the SAME --seed and check the two sha pairs are IDENTICAL: "
              "that is the control (same bytes, pairing deranged). arm=shuf MUST show "
              "fixed_points=0. Read the lever ONLY through `anima-py evaluate --fan-bind` "
              "(H_9693) — fals alone is FORM-forgeable (kill #6).")
        return 0
    if fmt == "storebind":
        if not opts["out"]:
            print("anima corpus storebind: --out c.txt is required", file=sys.stderr)
            sys.exit(2)
        text, st = build_storebind(opts["n_blocks"], opts["store_slots"], opts["seed"], opts["lang"],
                                   entity_pool=opts["entity_pool"])
        open(opts["out"], "w", encoding="utf-8").write(text)
        # .store.jsonl = per-training-line store manifest (block<->store · the co-train input the
        # trainer feeds the CLMS lane · JSONL, one row per line).
        sj = opts["out"] + ".store.jsonl"
        with open(sj, "w", encoding="utf-8") as fh:
            for r in st["store_manifest"]["entries"]:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        # .held.json = 0-shot held-out eval manifest (`anima-py evaluate <clm> --store <this>`).
        hj = opts["out"] + ".held.json"
        json.dump(st["held_manifest"], open(hj, "w", encoding="utf-8"), ensure_ascii=False)
        # H_9672 .held_balanced.json = PRIMARY scoring face (4/4 pols → majority-polarity shortcut 0.637
        # collapses to 0.5) · .seen.json = train-entity addr-gap control (memorization vs generalization).
        bj = opts["out"] + ".held_balanced.json"
        json.dump(st["balanced_manifest"], open(bj, "w", encoding="utf-8"), ensure_ascii=False)
        vj = opts["out"] + ".seen.json"
        json.dump(st["seen_manifest"], open(vj, "w", encoding="utf-8"), ensure_ascii=False)
        # .meta.json = budget floor (bytes the trainer enforces · a_korean_byte_budget: EN = 1 B/char).
        mj = opts["out"] + ".meta.json"
        meta = {"fmt": "storebind", "lang": st["lang"] if "lang" in st else opts["lang"],
                "bytes": st["bytes"], "lines": st["lines"], "n_blocks": st["n_blocks"],
                "store_slots": st["store_slots"], "max_line_bytes": st["max_line_bytes"]}
        # H_9683: the pool provenance is recorded ONLY when a pool was supplied, so the default
        # build's meta.json stays byte-identical to every existing one (absent key = builtin nonce).
        if st["entity_pool"] is not None:
            meta["entity_pool"] = st["entity_pool"]
        json.dump(meta, open(mj, "w", encoding="utf-8"), ensure_ascii=False)
        print("anima corpus storebind [%s]: blocks=%d slots=%d lines=%d bytes=%d max_line=%dB "
              "train=%d heldout=%d leak=0 -> %s"
              % (opts["lang"], st["n_blocks"], st["store_slots"], st["lines"], st["bytes"],
                 st["max_line_bytes"], st["n_train"], st["n_heldout"], opts["out"]))
        print("  manifests -> %s (%d co-train rows) · %s (%d held-out eval rows) · %s (floor)"
              % (sj, len(st["store_manifest"]["entries"]), hj,
                 len(st["held_manifest"]["entries"]), mj))
        if st["entity_pool"] is not None:
            print("  entity pool = EXTERNAL %s (%d atoms sampled to n_pool=%d · ascii · no dups) — "
                  "the builtin CVCVC nonce enumeration is NOT used"
                  % (st["entity_pool"], st["n_pool"], st["n_pool"]))
        print("  C0-a 0-shot ✅ held-out entities appear 0x in corpus (store-key + substring both asserted)")
        print("  answer = polarity XOR operator (is/not × good/bad) — store holds the FACT, text the "
              "OPERATOR; binding both needs the CLMS lane's nonlinear (GELU-MLP) readout.")
        print("  score:  anima-py evaluate <clm> --store %s" % hj)
        return 0

    if fmt == "falsidrill":
        # H_9837 — the density lever: an EN drill corpus dense in falsifiable claims, plus its
        # matched-surface ablation arm. Consumed as a CPT corpus by `anima-py train`.
        if not opts["out"]:
            print("anima-py corpus falsidrill: --out c.txt is required", file=sys.stderr)
            sys.exit(2)
        text, audit = build_falsidrill(opts["n_blocks"], opts["seed"], opts.get("falsi_ablate", False))
        regen = "anima-py corpus " + " ".join(argv)
        if audit["violations"]:
            print("anima-py corpus falsidrill: CORPUS INVALID — %d violation(s):"
                  % len(audit["violations"]), file=sys.stderr)
            for v in audit["violations"]:
                print("  · " + v, file=sys.stderr)
            sys.exit(2)
        with open(opts["out"], "w") as fh:
            fh.write(text)
        with open(opts["out"] + ".audit.json", "w") as fh:
            json.dump({"audit": audit, "regen": regen, "seed": opts["seed"]}, fh, indent=1)
        print("anima-py corpus falsidrill → %s  (arm=%s)" % (opts["out"], audit["arm"]))
        print("  lines %d · falsifiable %d (%.4f) · carriers %d · held-out leak %d"
              % (audit["n_lines"], audit["falsifiable"], audit["falsifiable_rate"],
                 audit["carriers"], len(audit["held_out_leak"])))
        print("  every eval-concept word is held out — the claim is measured at exposure 0 on its")
        print("  own axis (convergence corpus-py-1 (F)); the ablation arm is the structure-off control.")
        print("  regen: " + regen)
        sys.exit(0)

    if fmt == "dreamgen":
        # H_9839 — the dream node's COMPOSITION LAW as the manipulated variable. Judged by
        # `anima-py corpus mi-screen --mi-robust`, which needs NO ckpt and no GPU.
        if not opts["out"]:
            print("anima-py corpus dreamgen --out c.txt --lang en "
                  "--dream-target {planted|pedestal|midpoint|rule-derived|shuffled} "
                  "[--dream-nights 24] [--seed 7] "
                  "[--dream-anchors synthetic|real:<ckpt.clm>]", file=sys.stderr)
            print("      --dream-anchors real:<ckpt.clm> replaces the builder's uniformly-drawn")
            print("      anchor coordinates with the production trunk's REAL pooled penultimate")
            print("      of the same entity string (H_9838's planted-geometry swap). Everything")
            print("      else — nights, seeds, arms, laws, audit, eps — is unchanged.")
            print("      H_9839 — swaps core/dream_compose.py's geometric midpoint (its own header:")
            print("      'a designed geometric law (NOT a learned semantic insight, c9)') for the")
            print("      derivation of a DECLARED composition rule, and emits both plus a")
            print("      marginals-matched shuffle. A midpoint is ADDITIVE by construction, which")
            print("      is exactly where H_9304 measured non-additive information ~ 0.")
            print("      GATE ORDER IS FROZEN: run `planted` (must FIRE) and `pedestal` (must")
            print("      REFUSE) through mi-screen FIRST; the three treatment rows may not be read")
            print("      unless both certify. Judge each arm with:")
            print("        anima-py corpus mi-screen --corpus c.txt --mi-robust --out j.json")
            print("      Do NOT pass --mi-seg-lines here: nights are separated by a BLANK LINE, so")
            print("      segments_from_path already cuts on the corpus's own record unit at every")
            print("      geometry; re-cutting into N-line blocks would slice the night apart.")
            sys.exit(2)
        if opts["lang"] != "en":
            raise SystemExit(
                "corpus dreamgen: --lang en is required (got %r). EN-FIRST owner directive: the "
                "Korean lane is BINDING and every escape measured dead (H_9327), and EN is the "
                "discriminator. No ko variant is emitted rather than a silently dead one."
                % opts["lang"])
        real_ckpt = (opts["dream_anchors"].split("real:", 1)[1]
                     if opts["dream_anchors"].startswith("real:") else None)
        if real_ckpt and not os.path.exists(real_ckpt):
            raise SystemExit("corpus dreamgen: --dream-anchors real:%s does not exist" % real_ckpt)
        text, audit = build_dreamgen(opts["dream_nights"], opts["dream_target"], opts["seed"],
                                     real_ckpt=real_ckpt)
        regen = "anima-py corpus " + " ".join(argv)
        if audit["violations"]:
            print("anima-py corpus dreamgen: CORPUS INVALID — %d violation(s):"
                  % len(audit["violations"]), file=sys.stderr)
            for v in audit["violations"]:
                print("  · " + v, file=sys.stderr)
            sys.exit(2)
        with open(opts["out"], "w", encoding="utf-8") as fh:
            fh.write(text)
        with open(opts["out"] + ".audit.json", "w", encoding="utf-8") as fh:
            json.dump({"audit": audit, "regen": regen}, fh, ensure_ascii=False, indent=1)
        print("anima-py corpus dreamgen [arm=%s] -> %s" % (audit["arm"], opts["out"]))
        print("  nights %d · segments %d · pairs %d (MIN_PAIRS %d) · bytes %d · lines %d"
              % (audit["nights"], audit["n_segments"], audit["n_pairs"],
                 audit["judge_geometry"]["MIN_PAIRS"], audit["bytes"], audit["lines"]))
        print("  block bytes %d..%d · body->tail margin >= %dB (win %d) · %d dream(s)/night "
              "= C(%d,2)"
              % (audit["min_block_bytes"], audit["max_block_bytes"],
                 audit["min_body_tail_margin_bytes"], audit["judge_geometry"]["W_TAIL"],
                 audit["budget"] * (audit["budget"] - 1) // 2, audit["budget"]))
        print("  --dream-nights moves the SEGMENT/pair count (the judge's power), never the block")
        print("  geometry: nights x %d dream items, each night a fresh anchor draw, so it is not a"
              % (audit["budget"] * (audit["budget"] - 1) // 2))
        print("  repeat-exposure knob (corpus-py-3). Block size is a frozen constant, not a flag.")
        print("  carry multiset sha %s · geometry-field sha %s"
              % (audit["carry_multiset_sha"], audit["geometry_field_sha"]))
        print("  anchors %s · %d anchor(s) → %d distinct code(s) · per-slot distinct %s"
              % (audit["anchor_source"], audit["n_anchors"], audit["distinct_anchor_codes"],
                 audit["distinct_slot_values"]))
        print("    (H_9838 lesson: a synthetic anchor world is near-orthogonal BY CONSTRUCTION.")
        print("     A collapsed real-anchor code count is the trunk's geometry, not a builder bug.)")
        if audit["real_anchor_geometry"]:
            g = audit["real_anchor_geometry"]
            print("    real rep geometry: %d distinct entity string(s) · pairwise cosine "
                  "mean %.4f [%.4f .. %.4f]"
                  % (g["n_distinct_entities"], g["cos_mean"], g["cos_min"], g["cos_max"]))
        print("  → witnesses: rule-derived and shuffled at the SAME --seed must share the carry")
        print("    multiset sha (identical marginals, pairing destroyed); midpoint and")
        print("    rule-derived must share the geometry-field sha (identical coord/t5/r — only")
        print("    the text= payload, i.e. the composition LAW, differs).")
        print("  regen: " + regen)
        sys.exit(0)

    if fmt == "weavepanel":
        # H_9825 — the ρ·weave n=12 instrument fix. Emits a manifest consumed by
        # `anima-py evaluate <clm> --rho-axon --weave-panel <manifest.json>`.
        if not opts["out"]:
            print("anima-py corpus weavepanel: --out panel.json is required", file=sys.stderr)
            sys.exit(2)
        items, audit = build_weavepanel(opts["weave_families"], opts["weave_max"], opts["seed"])
        regen = "anima-py corpus " + " ".join(argv)
        if audit["violations"]:
            # A panel that leaks its target into the cue, or whose atom-swap keeps the true
            # answer, or that runs on ONE carrier, measures something other than composition.
            # Refuse rather than ship it (corpus-py-1 (E)/(F)).
            print("anima-py corpus weavepanel: PANEL INVALID — %d violation(s):"
                  % len(audit["violations"]), file=sys.stderr)
            for v in audit["violations"][:20]:
                print("  · " + v, file=sys.stderr)
            sys.exit(2)
        # H_9838 — atom-exposure audit (the prerequisite H_9827 declared open). Only runs when
        # --corpus is given; without it the panel ships unaudited and says so.
        exposure = None
        if opts["corpus"]:
            exposure = weavepanel_atom_exposure(items, opts["corpus"])
            audit["atom_exposure"] = {k: v for k, v in exposure.items() if k != "rows"}
        payload = {"items": items, "audit": audit, "regen": regen, "seed": opts["seed"],
                   "atom_exposure": exposure}
        with open(opts["out"], "w") as fh:
            json.dump(payload, fh, indent=1)
        print("anima-py corpus weavepanel → %s" % opts["out"])
        print("  n = %d items (frozen _WEAVE battery = 12, of which 6 on the ko lane that"
              " H_9327 measured BINDING-walled)" % audit["n"])
        print("  per-family : " + " · ".join("%s %d" % (k, v)
                                             for k, v in sorted(audit["by_family"].items())))
        print("  per-carrier: " + " · ".join("%s %d" % (k, v)
                                             for k, v in sorted(audit["by_carrier"].items())))
        n = audit["n"]
        sd = (0.30 * 0.70 / n) ** 0.5 if n else 0.0
        print("  binomial sd at the frozen 0.30 bar: %.4f  (n=12 → 0.1323 · one item = %.4f)"
              % (sd, 1.0 / n if n else 0.0))
        if exposure is not None:
            print("  atom exposure (boundary-counted · %d corpus file(s)):" % len(opts["corpus"]))
            print("    OPERAND axis  readable %d/%d  (absent %d — those measure atom absence,"
                  % (exposure["readable"], exposure["n"], exposure["operand_absent"]))
            print("                  NOT composition failure, and must be dropped or the corpus fixed)")
            print("    CARRIER axis  unseen frames %d  (an untrained carrier is an OOD basin,"
                  % exposure["carrier_absent"])
            print("                  not a clean probe · corpus-py-1 (12))")
            print("    TARGET-WORD absent %d  ⚠️ this counts the target WORD, not the composed"
                  % exposure["target_absent"])
            print("                  FACT. A target word occurring is normal and says nothing about")
            print("                  whether the cue→target association is held out — that check is")
            print("                  NOT implemented here. Reported so it is not mistaken for one.")
            print("    (one --corpus flag per file; extra bare paths are ignored)")
            for c in exposure["operand_absent_examples"]:
                print("      operand-absent · " + c)
            for c in exposure["carrier_absent_examples"]:
                print("      carrier-absent · " + c)
        else:
            print("  ⚠️ atom exposure NOT audited — pass --corpus <path>... to check that each")
            print("     item's atoms occur in the training corpus (an item whose atoms are absent")
            print("     measures atom absence, not composition · corpus-py-1 (F)).")
        print("  regen: " + regen)
        sys.exit(0)

    if fmt == "bindpanel":
        # H_9810 — the held-out binding panel + its drill corpus for the H_9805 tension-field arms.
        if not opts["out"]:
            print("anima corpus bindpanel: --out c.txt is required", file=sys.stderr)
            sys.exit(2)
        K = int(opts["bind_k"])
        _bp_len = "legacy" if opts.get("bind_legacy_lengths") else "matched"
        _bp_task = opts.get("bind_task") or "xor"
        # H_9818: under `xmark` the JUDGED task is xor and every panel line carries the `x ` marker.
        # Both must be threaded into the direct _bp_items() calls below — a panel built without the
        # marker would be scored on a carrier the model NEVER trained on, which is not a clean
        # baseline but an out-of-distribution basin (convergence corpus-py-1 ⑫, measured on H_9397).
        _bp_judged = "xor" if _bp_task == "xmark" else _bp_task
        _bp_mark = _BP_MARK[_bp_judged] if _bp_task == "xmark" else ""
        text, panel, codebook, st = build_bindpanel(K, opts["n_blocks"], opts["seed"], opts["lang"],
                                                    lengths=_bp_len, task=_bp_task)
        regen = "anima-py corpus " + " ".join(argv)
        if st["leaks"]:
            # A held-out lexeme in the drill corpus makes the panel a memorization test, and the
            # generalization axis this panel claims (LEXEME) would be measured at 0 exposure only
            # in name (corpus-py-1 (F)). Refuse rather than ship it.
            print("anima corpus bindpanel: 0-SHOT LEAK — held-out word form(s) %s occur in the "
                  "drill corpus" % st["leaks"][:8], file=sys.stderr)
            sys.exit(2)
        ap = st["audit_panel"]
        if _bp_task == "hp":
            # A positive control is DEFINED by carrying a learnable single-feature signal, so the
            # measurement-panel gate (every heuristic exactly 0.5) would refuse it by construction.
            # It is exempted and LOUDLY relabelled — it is a plumbing probe, never a measurement.
            print("  ⚠️ POSITIVE CONTROL (--bind-task hp) — gold = hp ALONE, no composition. The "
                  "exactly-0.5 heuristic gate is INTENTIONALLY not applied (presence IS the answer "
                  "here). This panel measures whether the substrate can learn a LOCAL feature at "
                  "all; it can never be read as a binding/recombination result.")
        elif not (ap["heuristics_exactly_half"] and ap["pairwise_independent"]):
            print("anima corpus bindpanel: HEURISTIC LEAK — a unary cue or a slot pair is not at "
                  "0.5 on the panel; the d_acc floor would not be chance. audit=%s"
                  % json.dumps(ap), file=sys.stderr)
            sys.exit(2)
        with open(opts["out"], "w", encoding="ascii") as fh:
            fh.write(text)
        pj = opts["out"] + ".panel.json"
        # H_9812 FIELD-ALONE LEAK GATE — per concord mode, fit on the DRILLED conjuncts and score
        # on the held-out ones. A mode that calls gold above the derived chance is DISQUALIFIED:
        # under it the field hands the reader the answer, so no Δ measured with it is readable.
        _train_conj = [c for it in _bp_items(K, _BP_VERB_SEEN, _BP_NOUN_SEEN, 0, lengths=_bp_len,
                                             task=_bp_judged, mark=_bp_mark)
                       for c in it["conjuncts"]]
        _panel_conj = [c for it in panel for c in it["conjuncts"]]
        leak = {m: field_alone_leak(_train_conj, _panel_conj, m) for m in ("class", "lex", "morph")}
        json.dump({"schema": "anima-bindpanel/v1", "K": K, "lang": st["lang"], "seed": st["seed"],
                   "answers": list(_BP_ANS), "tail": _BP_TAIL, "arrow": _BP_ARROW,
                   "regen_cmd": regen, "codebook": codebook, "audit": ap,
                   "field_alone_leak": leak,
                   "disqualified_concord": sorted(m for m, r in leak.items() if r["leaks"]),
                   "held_lexemes": st["held_lexemes"], "seen_lexemes": st["seen_lexemes"],
                   "items": panel},
                  open(pj, "w", encoding="utf-8"), ensure_ascii=False)
        # .seen_panel.json — the SAME frame on the DRILLED lexemes. This is H_9805's F2 liveness
        # face: if an arm cannot do the operation on lexemes it was trained on, the held-out number
        # is measuring a dead model and must not be read at all. Without it F2 has no instrument
        # either, and a floor-level held-out d_acc is unattributable.
        sj = opts["out"] + ".seen_panel.json"
        seen_panel = _bp_items(K, _BP_VERB_SEEN, _BP_NOUN_SEEN, 0, lengths=_bp_len,
                               task=_bp_judged, mark=_bp_mark)
        json.dump({"schema": "anima-bindpanel/v1", "K": K, "lang": st["lang"], "seed": st["seed"],
                   "answers": list(_BP_ANS), "tail": _BP_TAIL, "arrow": _BP_ARROW,
                   "regen_cmd": regen, "codebook": codebook,
                   "face": "liveness (DRILLED lexemes — NOT held-out, never a generalization claim)",
                   "items": seen_panel},
                  open(sj, "w", encoding="utf-8"), ensure_ascii=False)
        cj = opts["out"] + ".codebook.json"
        json.dump(codebook, open(cj, "w", encoding="utf-8"), ensure_ascii=False)
        mj = opts["out"] + ".meta.json"
        json.dump({"fmt": "bindpanel", "lang": st["lang"], "K": K, "seed": st["seed"],
                   "bytes": st["bytes"], "lines": st["n_drill_lines"], "regen_cmd": regen,
                   "min_steps": None, "min_lr": None,
                   "note": ("no MEASURED budget floor for this format yet. It is a FROM-SCRATCH "
                            "drill corpus, NOT a CPT mix — continuing a pretrained ckpt on it "
                            "would destroy every stratum absent from it (corpus-py-1 ⑥), and this "
                            "corpus contains exactly one carrier, so nothing else survives."),
                   "forget_strata": []},
                  open(mj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("anima corpus bindpanel [%s]: K=%d panel=%d items drill=%d lines bytes=%d seed=%d -> %s"
              % (st["lang"], K, st["n_panel"], st["n_drill_lines"], st["bytes"], st["seed"],
                 opts["out"]))
        print("  surface bytes %s · max scored seq = %d B (choose --seq-len/--win at or above it, "
              "or the right-aligned window truncates the early conjuncts and the panel measures a "
              "different question)" % (ap["surface_byte_lengths"], ap["max_seq_bytes"]))
        print("  ⚠️ WHAT THE FIELD CAN SEE DEPENDS ON --tension-concord (H_9812). `class` (the "
              "default) derives every chi sign from the WHITESPACE MASK and is blind to which "
              "letters are present — on a lexically-keyed panel it carries 0 bits, so a Δ of 0 "
              "means NO CHANNEL, not rank collapse. This panel is length-coded (verb +s=5B vs "
              "+ing=7B · noun 6B vs +s=7B) so `class` has a channel at all. `lex`/`morph` let the "
              "field see word identity/morphology — that is the ①field-sees-content fork, and it "
              "is gated below, not assumed safe.")
        for _m in ("class", "lex", "morph"):
            _r = leak[_m]
            _tag = ("⛔ DISQUALIFIED — the field alone calls gold" if _r["leaks"] else
                    "⚠️ UNDECIDABLE (coverage below floor)" if _r["undecidable"] else "✅ no leak")
            print("  FIELD-ALONE LEAK GATE [%-5s] acc %.4f vs derived chance %.4f · coverage %.4f  %s"
                  % (_m, _r["acc"], _r["chance"], _r["coverage"], _tag))
        print("  HEURISTIC AUDIT (all must be exactly 0.500000): " + " · ".join(
            "%s=%s" % (k, ap["per_slot"][0][k]) for k in sorted(ap["per_slot"][0])))
        print("  slot independence: worst pairwise |P(gold_a=gold_b)-0.5| = %s (pair %s)"
              % (ap["worst_pairwise_dev"], ap["worst_pair"]))
        print("  0-SHOT ✅ every held-out word form occurs 0x in the drill corpus "
              "(word-boundary split, never substring — corpus-py-1 (G))")
        print("  codebook = the FULL 2^%d factorial ⇒ GF(2) rank %d, no prefix-determined column. "
              "VERIFY IT, do not assume it:" % (K, K))
        print("    anima-py evaluate --free-slot-score %s --pregate-bar 0.15" % cj)
        print("  score:  anima-py evaluate <clm> --bind-panel %s" % pj)
        print("  F2 liveness (DRILLED lexemes — read it FIRST; a floor-level held-out number on a "
              "model that cannot do the drilled cells is unattributable):")
        print("          anima-py evaluate <clm> --bind-panel %s" % sj)
        return 0

    if fmt == "counterfactual-decl":
        if not opts["out"]:
            print("anima corpus counterfactual-decl: --out c.txt is required", file=sys.stderr)
            sys.exit(2)
        held_stems, held_ops = opts["held_out"]
        text, st = build_counterfactual_decl(
            opts["n_blocks"], opts["stems_per_episode"], opts["seed"], opts["lang"],
            held_stems, held_ops, n_eval_episodes=opts["eval_episodes"])
        # regeneration fingerprint (corpus-py-1 ⑫/(J)): the EXACT argv that produced these bytes is
        # written into every artifact, so a later session can rebuild the identical pool instead of
        # silently running a different experiment.
        regen = "anima-py corpus " + " ".join(argv)
        st["manifest"]["regen_cmd"] = regen
        with open(opts["out"], "w", encoding="ascii") as fh:
            fh.write(text)
        # AUDIT AFTER THE WRITE, FROM THE FILE ON DISK — the balance claim is only evidence if it
        # was measured on the bytes that were actually emitted.
        audit = audit_counterfactual_decl(opts["out"], st)
        audit["regen_cmd"] = regen
        ej = opts["out"] + ".decl.json"
        json.dump(st["manifest"], open(ej, "w", encoding="utf-8"), ensure_ascii=False)
        aj = opts["out"] + ".audit.json"
        json.dump(audit, open(aj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        # .storelines.txt (+ lockstep .store.jsonl) = the QUERY-LINES-ONLY surface for the
        # co-trained store lane (`--store-fuse pairodd`), which requires a strict 1:1
        # line<->row lockstep and therefore cannot carry the episodic declaration lines. Same
        # episodes, same RNG stream: the declaration BYTES charge the store's key/value
        # (entities = declared stems, pols = declared senses), while the operator declaration
        # rides the prompt — storebind's "store holds the FACT, text the OPERATOR" contract.
        sl = opts["out"] + ".storelines.txt"
        with open(sl, "w", encoding="ascii") as fh:
            for r in st["store_rows"]:
                fh.write(r["prompt"] + r["gold"] + "\n")
        with open(sl + ".store.jsonl", "w", encoding="utf-8") as fh:
            for r in st["store_rows"]:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        mj = opts["out"] + ".meta.json"
        json.dump({"fmt": "counterfactual-decl", "lang": st["lang"], "bytes": st["bytes"],
                   "lines": st["lines"], "n_blocks": st["n_blocks"],
                   "stems_per_episode": st["stems_per_ep"], "seed": st["seed"],
                   "regen_cmd": regen,
                   "min_steps": None, "min_lr": None,
                   "note": ("no MEASURED budget floor for this format yet — the WRITE gate on the "
                            "resulting ckpt decides; do NOT transplant another format's floor"),
                   "forget_strata": ["heldout-map-stem", "heldout-map-op"]},
                  open(mj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        a = audit["answer"]
        print("anima corpus counterfactual-decl [%s]: episodes=%d stems/ep=%d lines=%d bytes=%d "
              "seed=%d -> %s" % (st["lang"], st["n_blocks"], st["stems_per_ep"], st["lines"],
                                 st["bytes"], st["seed"], opts["out"]))
        print("  pools: stems rot=%d frozen=%d held=%d · ops rot=%d frozen=%d held=%d "
              "(--held-out %d,%d = held-out STEM,OPERATOR names for this format)"
              % (st["n_rot_stems"], st["n_frozen_stems"], st["n_heldout_stems"],
                 st["n_rot_ops"], st["n_frozen_ops"], st["n_heldout_ops"], held_stems, held_ops))
        print("  POLARITY (re-parsed from disk): %s · balanced_exact=%s · chance_majority=%.4f "
              "(DERIVED from the realized split, never assumed 0.5)"
              % (a["counts"], a["balanced_exact"], a["chance_majority"]))
        print("  CARRIER ✅ 0 query carriers contain an answer token (aye|nay) or a label "
              "(good|harm|same|flip) — the operator->answer map is NOT installed by the carrier")
        print("  0-SHOT ✅ held-out stem/operator names appear 0x in the corpus (exact-token: every "
              "name is 5 ascii chars, space-delimited, reserved-literal colliders dropped from the pool)")
        print("  strata: " + " · ".join("%s n=%d chance=%.4f"
                                        % (k, v["n"], v["chance_majority"])
                                        for k, v in sorted(audit["eval"].items())))
        print("  manifests -> %s (%d eval items · 5 strata) · %s (polarity audit) · %s (%d "
              "store-lane rows) · %s (floor)"
              % (ej, len(st["manifest"]["entries"]), aj, sl + ".store.jsonl",
                 len(st["store_rows"]), mj))
        print("  score:  anima-py evaluate <clm> --decl-flip %s" % ej)
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
            _write_budget_floor(opts["out"], fmt, opts["lang"])
        print(f"anima corpus {fmt}: held={st['held']} seen={st['seen']} lines={st['lines']} "
              f"labels_flipped={st['labels_flipped']}/{st['held']} bytes={st['bytes']} "
              f"reps={opts['reps']} replay={opts['replay']} seed={opts['seed']} "
              f"-> {opts['out'] or '(stdout head)'}")
        if not opts["out"]:
            print(text[:400])
        return
    S, KW = _load_concepts(opts["concepts"])
    text, train_pairs = build(fmt, S, KW, opts["held_out"],
                              opts["comp_per_pair"], opts["single_per_concept"], opts["seed"],
                              held_out_frac=opts.get("held_out_frac", 0.0))
    if opts["out"]:
        with open(opts["out"], "w") as fh:
            fh.write(text)
    n_c = len(S)
    n_grid = n_c * (n_c - 1) // 2
    n_held = n_grid - len(train_pairs) // 2
    print(f"anima corpus {fmt}: concepts={n_c} train_pairs={len(train_pairs)} "
          f"held-out={tuple(opts['held_out'])} bytes={len(text.encode())} "
          f"seed={opts['seed']} -> {opts['out'] or '(stdout head)'}")
    if opts.get("held_out_frac", 0.0) > 0.0:
        # H_9643: report the REALIZED coverage, not the requested fraction — the K=1 floor
        # pre-gate is read against what the corpus actually withheld.
        print(f"  coverage: {n_grid - n_held}/{n_grid} unordered pairs trained "
              f"({100.0 * (n_grid - n_held) / max(n_grid, 1):.1f}%) · "
              f"held-out-frac={opts['held_out_frac']} ({n_held} pairs withheld)")
    if not opts["out"]:
        print(text[:600])


if __name__ == "__main__":
    main()
