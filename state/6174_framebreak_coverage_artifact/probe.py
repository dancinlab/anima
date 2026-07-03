#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════════════════
# H_6174 — system-G1 FRAME-BREAK (kosmos_merge concat) is a COVERAGE ARTIFACT
#
#   Candidate ⑤ (frame-break, task-priority #1): relocate recombination OUT of
#   the mouth (which floors on A⊗B binding) INTO the .kosmos anchor store —
#   the mouth only VERBALIZES atomic concepts, the SYSTEM concatenates the two
#   independent single-concept fragments (kosmos_merge keeps A,B as children).
#
#   The existing rungs (H_9035) score this by COVERAGE + bind-RECOVERABILITY +
#   SCRAMBLE-drop and report the compositional arm PASSES.  THIS PROBE asks the
#   fair-cheap-gate question the existing bars DO NOT: is that pass genuine
#   binding, or a JUXTAPOSITION artifact — does concat surface both concepts
#   WITHOUT producing any A↔B relation, such that a WRONG anchor pairing scores
#   identically (no EARNED discrimination)?
#
#   Mouth-bypass MODELING (numpy/stdlib, DIRECTIONAL per a_engine_native_learning):
#   the mouth is the SAME frozen toy lexicon as state/system_g1_relocate_kosmos_merge/
#   system_g1_harness.py (byte-identical CONCEPTS/GLUE), so this measures the
#   PIPE's discriminative validity, not a new mouth.
#
#   FROZEN BARS (pre-registered, do NOT move post-hoc — c9):
#     G-COV   : compositional coverage cov>=2 & > max_single on >= M/2 pairs
#               (the EXISTING bar — expected PASS, i.e. the spoof reproduces).
#     G-EARN  : PRIMARY discriminator. right-pair vs wrong-pair coverage gap.
#               A genuine bind scores right>wrong; juxtaposition scores equal.
#               PASS(binding) iff  n(cov_right - cov_wrongpair >= 1) >= M/2.
#     G-REL   : cross-concept RELATION count (bigrams linking A-vocab to B-vocab).
#               genuine recombination emits >=1 cross-vocab binding per pair;
#               concat emits only the generic connector = 0 cross-binds.
#               PASS(binding) iff  n(cross_bind >= 1) >= M/2.
#     G-SHUF  : anchor-content shuffle control (right pair vs mismatched pair) —
#               coverage MUST drop if the metric reads the anchor identity.
#
#   Deterministic (p7: equality/counts, not perplexity).
# ═══════════════════════════════════════════════════════════════════════════
import random
from collections import Counter

# ── frozen bar ───────────────────────────────────────────────────────────
SEEDS      = [7, 42, 4302]
M          = 24                 # 8 base pairs × 3 seeds
HALF       = M // 2             # 12

# ── frozen toy lexicon — BYTE-IDENTICAL to system_g1_harness.py ───────────
CONCEPTS = {
    "ocean":    ["tide", "salt", "wave", "deep"],
    "forest":   ["moss", "branch", "fern", "canopy"],
    "engine":   ["piston", "fuel", "gear", "torque"],
    "music":    ["chord", "tempo", "melody", "rhythm"],
    "market":   ["price", "trade", "stock", "ledger"],
    "medicine": ["dose", "fever", "immune", "remedy"],
    "desert":   ["dune", "cactus", "mirage", "arid"],
    "galaxy":   ["orbit", "nebula", "comet", "stellar"],
    "kitchen":  ["knife", "simmer", "flour", "roast"],
    "law":      ["statute", "verdict", "counsel", "appeal"],
    "glacier":  ["crevasse", "moraine", "frost", "calve"],
    "circuit":  ["resistor", "voltage", "solder", "diode"],
}
GLUE = ["and", "then", "with", "so"]
NAMES = list(CONCEPTS)
VOCAB2CPT = {t: c for c, toks in CONCEPTS.items() for t in toks}


def ideate_single(concept, seed):
    """TOY frozen mouth — single-concept ordered signature phrase (G0-fluent)."""
    toks = CONCEPTS[concept]
    g = GLUE[seed % len(GLUE)]
    return [toks[0], g, toks[1], toks[2], g, toks[3]]


def realize_concat(frag_a, frag_b):
    """FRAME-BREAK Stage B: system concat of the two atomic fragments (the pipe
    the mouth NEVER has to bind — the exact claim of ⑤)."""
    return frag_a + ["then"] + frag_b


def coverage(tokens, a, b):
    tokset = set(tokens)
    return sum(1 for cpt in (a, b) if any(t in tokset for t in CONCEPTS[cpt]))


def cross_bind_count(tokens, a, b):
    """# adjacent bigrams that link A-vocab to B-vocab (a genuine A↔B relation).
    concat produces only <A-tail> 'then' <B-head> — 0 direct cross-vocab bigrams."""
    n = 0
    for x, y in zip(tokens, tokens[1:]):
        cx, cy = VOCAB2CPT.get(x), VOCAB2CPT.get(y)
        if cx and cy and {cx, cy} == {a, b}:
            n += 1
    return n


def build_pairs():
    idx = [(0, 1), (2, 3), (4, 5), (6, 7), (8, 9), (10, 11), (0, 6), (3, 9)]
    base = [(NAMES[i], NAMES[j]) for (i, j) in idx]
    return [(a, b, s) for s in SEEDS for (a, b) in base][:M]


def wrong_partner(a, b, seed):
    """mismatched anchor: pair A with a WRONG concept (not b, not a)."""
    others = [n for n in NAMES if n not in (a, b)]
    return others[(seed * 7 + 3) % len(others)]


def main():
    pairs = build_pairs()
    cov_pass = earn_pass = rel_pass = shuf_drop = 0
    rows = []
    for (a, b, seed) in pairs:
        frag_a = ideate_single(a, seed)
        frag_b = ideate_single(b, seed)
        max_single = max(coverage(frag_a, a, b), coverage(frag_b, a, b))  # =1

        # FRAME-BREAK right pairing
        C_right = realize_concat(frag_a, frag_b)
        cov_r = coverage(C_right, a, b)
        rel_r = cross_bind_count(C_right, a, b)

        # WRONG anchor pairing — merge A with a mismatched concept
        w = wrong_partner(a, b, seed)
        frag_w = ideate_single(w, seed)
        C_wrong = realize_concat(frag_a, frag_w)
        # score the WRONG composite on the ORIGINAL target (a,b): does the
        # metric notice the anchor identity changed?
        cov_w = coverage(C_wrong, a, b)

        cov_ok = cov_r >= 2 and cov_r > max_single          # existing bar
        # NOTE (honesty c9): EARN as (cov_r > cov_w) is CONFOUNDED — the wrong
        # anchor lacks b's vocab entirely, so its TARGET coverage is trivially
        # lower regardless of any binding. It is NOT a binding discriminator;
        # kept only to expose the confound. The genuine discriminator is REL.
        earn_ok = (cov_r - cov_w) >= 1                       # CONFOUNDED (vocab-presence)
        rel_ok = rel_r >= 1                                  # PRIMARY: genuine A↔B relation
        if cov_ok:
            cov_pass += 1
        if earn_ok:
            earn_pass += 1
        if rel_ok:
            rel_pass += 1
        if cov_w < cov_r:
            shuf_drop += 1
        rows.append((a, b, w, cov_r, cov_w, rel_r, max_single))

    print("=== H_6174 system-G1 frame-break coverage-artifact probe (DIRECTIONAL) ===")
    print("pipe: mouth ideate(A),ideate(B) -> kosmos_merge -> CONCAT realize (frame-break ⑤)")
    print("bars (FROZEN): COV_PASS>=%d  EARN_PASS>=%d  REL_PASS>=%d" % (HALF, HALF, HALF))
    print("")
    print("  G-COV  coverage cov>=2 & >max_single : %2d/%d  (EXISTING bar)" % (cov_pass, M))
    print("  G-REL  cross-vocab A<->B relation>=1 : %2d/%d  (PRIMARY binding discriminator)" % (rel_pass, M))
    print("  G-EARN right>wrong-pair coverage     : %2d/%d  (CONFOUNDED = vocab-presence, NOT binding)" % (earn_pass, M))
    print("  G-SHUF wrong-anchor coverage DROP    : %2d/%d  (also vocab-presence, not binding)" % (shuf_drop, M))
    print("")
    cov_v = "PASS" if cov_pass >= HALF else "FAIL"
    rel_v = "PASS" if rel_pass >= HALF else "FAIL"
    print("  frozen-G1 coverage bar   : %s (%d/%d)" % (cov_v, cov_pass, M))
    print("  genuine binding RELATION : %s (%d/%d)" % (rel_v, rel_pass, M))
    print("")
    # Verdict keys ONLY on the two unconfounded axes: coverage (existing bar) and
    # REL (genuine A<->B relation). EARN/SHUF are confounded by vocab-presence.
    if cov_pass >= HALF and rel_pass < HALF:
        print("VERDICT: COVERAGE-ARTIFACT / JUXTAPOSITION — frame-break concat CLEARS the")
        print("         frozen G1 coverage bar (both concepts surfaced) but produces ZERO")
        print("         A<->B binding relations (REL %d/%d). The relocation avoids the trunk" % (rel_pass, M))
        print("         binding wall precisely by NOT binding (juxtaposing) — so it can never")
        print("         satisfy any relation-based recombination criterion. Coverage-based G1")
        print("         is SPOOFABLE by relocation; genuine binding still needs the mouth to")
        print("         emit a cross-concept relation = the trunk-objective wall (H_1602).")
    elif cov_pass >= HALF and rel_pass >= HALF:
        print("VERDICT: EARNED-BINDING — frame-break passes coverage AND the genuine")
        print("         relation discriminator. Escalate to real 303M mouth on pool.")
    else:
        print("VERDICT: FLOOR — frame-break does not even clear coverage.")
    print("")
    print("first 6 rows (a,b,wrong, cov_right,cov_wrong, cross_rel, max_single):")
    for r in rows[:6]:
        print("  ", r)


if __name__ == "__main__":
    main()
