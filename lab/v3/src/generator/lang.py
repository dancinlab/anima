"""Jamo composition for the synthetic agglutinative drill language.

The rig needs a language whose morphemes are jamo-composed, so that a BPE fit
over the JAMO sequence can (or cannot) discover morpheme boundaries. Hangul's
syllable block is algorithmic — S = 0xAC00 + (L*21 + V)*28 + T — which gives a
real compositional writing system with no data dependency and no corpus.

Nothing here is Korean: the stems and affixes are invented. Hangul supplies the
composition rule (L5 — expose composition at the token boundary), not vocabulary.

Deterministic, stdlib only.
"""

from __future__ import annotations

import unicodedata

SBASE = 0xAC00
LCOUNT, VCOUNT, TCOUNT = 19, 21, 28
NCOUNT = VCOUNT * TCOUNT          # 588
SCOUNT = LCOUNT * NCOUNT          # 11172

# Conjoining jamo (the compatibility set is NOT used — these compose).
LEADS = [chr(0x1100 + i) for i in range(LCOUNT)]
VOWELS = [chr(0x1161 + i) for i in range(VCOUNT)]
TAILS = [""] + [chr(0x11A7 + i) for i in range(1, TCOUNT)]


def compose(lead: int, vowel: int, tail: int = 0) -> str:
    """Compose one syllable from jamo indices. Inverse of `decompose_syllable`."""
    if not (0 <= lead < LCOUNT):
        raise ValueError(f"lead out of range: {lead}")
    if not (0 <= vowel < VCOUNT):
        raise ValueError(f"vowel out of range: {vowel}")
    if not (0 <= tail < TCOUNT):
        raise ValueError(f"tail out of range: {tail}")
    return chr(SBASE + (lead * VCOUNT + vowel) * TCOUNT + tail)


def decompose_syllable(ch: str) -> tuple:
    """(lead, vowel, tail) indices for a precomposed Hangul syllable."""
    code = ord(ch) - SBASE
    if not (0 <= code < SCOUNT):
        raise ValueError(f"not a Hangul syllable: {ch!r}")
    return (code // NCOUNT, (code % NCOUNT) // TCOUNT, code % TCOUNT)


def to_jamo(text: str) -> str:
    """Expand every Hangul syllable in `text` into its conjoining jamo.

    Non-Hangul characters pass through unchanged. This is the alphabet the BPE
    codec is fit over — the point of the whole rig is that morpheme boundaries
    are *discoverable* at this level and invisible above it.
    """
    out = []
    for ch in text:
        code = ord(ch) - SBASE
        if 0 <= code < SCOUNT:
            lead, vowel, tail = decompose_syllable(ch)
            out.append(LEADS[lead])
            out.append(VOWELS[vowel])
            if tail:
                out.append(TAILS[tail])
        else:
            out.append(ch)
    return "".join(out)


def from_jamo(text: str) -> str:
    """Inverse of `to_jamo` — recompose conjoining jamo into syllables.

    Round-trip `from_jamo(to_jamo(s)) == s` is asserted as a generator invariant,
    because a codec fit on a lossy decomposition would measure segmentation of a
    language that does not exist.
    """
    out = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        li = LEADS.index(ch) if ch in LEADS else -1
        if li >= 0 and i + 1 < n and text[i + 1] in VOWELS:
            vi = VOWELS.index(text[i + 1])
            ti = 0
            if i + 2 < n and text[i + 2] in TAILS[1:]:
                ti = TAILS.index(text[i + 2])
                i += 1
            out.append(compose(li, vi, ti))
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def render(stem: str, affix_chain: list) -> str:
    """Surface form of a stem plus an ordered chain of BOUND affixes.

    Concatenative and NFC-normalized. Affixes are bound (they attach with no
    separator), which is the whole point per salvage l5: a FREE, pre-posed
    negator would hand the model the boundary for free and the rig would measure
    nothing.
    """
    if not stem:
        raise ValueError("stem must be non-empty")
    return unicodedata.normalize("NFC", stem + "".join(affix_chain))


def parse(surface: str, stems: list, affixes: list) -> tuple:
    """Recover (stem, affix_chain) from a surface form — the asserted inverse of
    `render`. Longest-stem-first so a stem that prefixes another cannot shadow it.

    Returns (stem, [affix, ...]). Raises if the form is not reachable, which is
    how the round-trip invariant fails loudly instead of silently.
    """
    surface = unicodedata.normalize("NFC", surface)
    for stem in sorted(stems, key=len, reverse=True):
        if not surface.startswith(stem):
            continue
        rest, chain = surface[len(stem):], []
        while rest:
            for af in sorted(affixes, key=len, reverse=True):
                if af and rest.startswith(af):
                    chain.append(af)
                    rest = rest[len(af):]
                    break
            else:
                break
        if not rest:
            return (stem, chain)
    raise ValueError(f"unparseable surface form: {surface!r}")
