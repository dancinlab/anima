"""Leak scan — the audit that decides whether a win is a measurement or an echo.

`rig-drift-deficit-asserted` and invariant 4: every rendered eval string must
occur ZERO times as an exact substring of either phase stream, and held-out stems
must never co-occur with a NEG-class affix. v1's precedent is not hypothetical —
its one apparent win (GATED 0.345 << base) was a CA-neighbour lookahead LEAK and
evaporated leak-free (`l6-leak`).

Deterministic, stdlib only.
"""

from __future__ import annotations

from lang import from_jamo, parse, to_jamo
from spec import neg_forms
from stream import POS_MARK, NEG_MARK, SENTINEL


def _iter_words(stream_iter):
    """Yield (body_jamo, polarity) for each stream utterance.

    The stream frames each utterance as `<body>` SENTINEL `<mark>` SENTINEL, so a
    body token is always followed by its polarity-mark token. polarity is
    'pos' | 'neg' | None, read from the EMITTED mark — ground truth about what the
    generator meant, so downstream audits key off it rather than re-parsing an
    ambiguous jamo string and guessing (H_003 N-4: a parse-any detector measures
    the language's ambiguity, not the corpus's contamination). Mark tokens are
    consumed, not yielded as bodies."""
    posj, negj = to_jamo(POS_MARK), to_jamo(NEG_MARK)
    marks = {posj: "pos", negj: "neg"}
    carry = ""
    pending = None  # a body awaiting its mark token
    for chunk in stream_iter:
        buf = carry + chunk
        pieces = buf.split(SENTINEL)
        carry = pieces.pop() if pieces else ""
        for tok in pieces:
            if tok in marks:
                if pending is not None:
                    yield (pending, marks[tok])
                    pending = None
                # a lone mark with no pending body is ignored (chunk-edge artifact)
            else:
                if pending is not None:
                    yield (pending, None)
                pending = tok if tok else None
    if pending is not None:
        yield (pending, None)


def leak_scan(stream_iter, spec: dict, forms: list) -> dict:
    """Count stream words that PARSE to exactly one of `forms`.

    The leak question is "was this composed form ever EMITTED", not "does its
    jamo appear as a substring somewhere". Two weaker tests both give false
    positives here and were rejected: raw jamo substring (a 3-jamo affix collides
    everywhere), and whole-word prefix (a held-out stem's jamo can prefix an
    unrelated word). The only correct test is to recompose each stream word to
    its surface form and compare to the target set exactly — a word IS a leak iff
    it renders to a form in the set.
    """
    target_surface = set(forms)
    hits = {f: 0 for f in forms}
    for body, _pol in _iter_words(stream_iter):
        surface = from_jamo(body)
        if surface in target_surface:
            hits[surface] += 1
    return {"hits": hits, "total": sum(hits.values()), "clean": sum(hits.values()) == 0}


def heldout_neg_cooccurrence(spec: dict, stream_iter) -> int:
    """Times a stream word PARSES to (held-out stem + a NEG affix).

    Must be 0 in both phases — the invariant that makes the eval measure
    RECOMBINATION rather than coverage. Parse-based, not substring or prefix: the
    stream only ever emits held-out stems with PLAIN affixes, so a word that
    genuinely decomposes to (held-out stem, NEG-affix) is a real break, and a
    coincidental jamo collision is not (it will not parse that way).
    """
    heldout = set(spec["heldout_stems"])
    negs = set(neg_forms(spec, 1)) | set(neg_forms(spec, 2))
    all_affixes = sorted({a["form"] for a in spec["affixes_p1"]} | {a["form"] for a in spec["affixes_p2"]})
    stems = spec["stems"]
    count = 0
    for body, pol in _iter_words(stream_iter):
        # Only NEG-marked words can break the invariant — a POS-marked word is by
        # construction (stem + PLAIN affix), and re-parsing it to a spurious
        # (held-out stem + NEG) decomposition is the H_003 N-4 false positive.
        if pol != "neg":
            continue
        surface = from_jamo(body)
        try:
            stem, chain = parse(surface, stems, all_affixes)
        except ValueError:
            continue
        if stem in heldout and any(c in negs for c in chain):
            count += 1
    return count


