"""BPE-on-jamo codec: fit, encode, boundaries, atomicity audit.

The codec is the thing on trial (F1: the codec is the self), so everything here
is deterministic and every tie is broken explicitly.

Indexing note — a DELIBERATE deviation from the design's "probes = 256 strings x
64 BYTES, B in {0,1}^{256x63}". Boundaries are indexed in JAMO positions, not
byte positions. Reason: every conjoining jamo is exactly 3 bytes in UTF-8, so a
byte-indexed B has two thirds of its columns identically zero by construction —
a boundary can never fall inside a jamo. That would deflate the boundary-shift
rate ~3x and hand the rank estimator a spectrum shaped by UTF-8 rather than by
the codec. Jamo positions are equally codec-independent (jamo is the codec's
fixed base alphabet), and they are the alphabet the merges actually operate on.
Probes are still exactly rectangular: 256 x 64 jamo = 256 x 192 bytes.

Deterministic, stdlib only.
"""

from __future__ import annotations

import collections

SENTINEL = "\x00"


class Codec:
    """A frozen BPE merge table over the jamo alphabet."""

    def __init__(self, merges: list, k: int):
        # merges is ordered; rank = merge priority (earlier = applied first)
        self.merges = list(merges)
        self.k = k
        self.ranks = {pair: i for i, pair in enumerate(self.merges)}

    def __len__(self) -> int:
        return len(self.merges)

    def encode_tokens(self, jamo: str) -> list:
        """Segment a jamo string into tokens by applying the merge table.

        Standard BPE application: repeatedly merge the highest-ranked adjacent
        pair present. Deterministic — `min` over ranks with no ties possible,
        since ranks are unique by construction.
        """
        if not jamo:
            return []
        syms = list(jamo)
        while len(syms) > 1:
            best, best_rank = None, None
            for i in range(len(syms) - 1):
                r = self.ranks.get((syms[i], syms[i + 1]))
                if r is not None and (best_rank is None or r < best_rank):
                    best, best_rank = i, r
            if best is None:
                break
            syms[best:best + 2] = [syms[best] + syms[best + 1]]
        return syms

    def boundaries(self, jamo: str) -> frozenset:
        """Internal token boundaries as jamo offsets in [1, len(jamo)-1].

        Position i means "a token ends just before jamo i". Offsets 0 and
        len(jamo) are excluded: they are boundaries for every codec and carry no
        information about the merge table.
        """
        out, pos = [], 0
        for tok in self.encode_tokens(jamo):
            pos += len(tok)
            out.append(pos)
        return frozenset(p for p in out if 0 < p < len(jamo))

    def is_single_token(self, jamo_form: str, jamo_context: str) -> bool:
        """Does `jamo_form` survive as ONE token when encoded IN CONTEXT?

        Context matters: BPE segmentation is context-dependent, so auditing a
        form in isolation measures a question nobody asked (design invariant 5).
        """
        idx = jamo_context.find(jamo_form)
        if idx < 0:
            raise ValueError("form does not occur in the given context")
        pos, end = 0, idx + len(jamo_form)
        for tok in self.encode_tokens(jamo_context):
            if pos == idx and len(tok) == len(jamo_form):
                return True
            if pos >= end:
                break
            pos += len(tok)
        return False


def fit_bpe_jamo(samples: list, k: int) -> Codec:
    """Fit `k` BPE merges over a list of jamo strings.

    Tie-break is FROZEN as (count desc, pair lexicographic asc). BPE ties are the
    classic silent nondeterminism: two fits of the same data can disagree on the
    merge list and therefore on every downstream boundary, which would make the
    frozen-vs-adaptive contrast a coin flip dressed as a measurement.
    """
    if k <= 0:
        raise ValueError(f"k must be > 0: {k}")
    # word -> frequency, as tuples of symbols
    freqs: dict = collections.Counter()
    for s in samples:
        for word in s.split(SENTINEL):
            if word:
                freqs[word] += 1
    vocab = {tuple(w): c for w, c in sorted(freqs.items())}

    merges = []
    for _ in range(k):
        pairs: dict = collections.Counter()
        for syms, c in vocab.items():
            for i in range(len(syms) - 1):
                pairs[(syms[i], syms[i + 1])] += c
        if not pairs:
            break
        # frozen tie-break: highest count, then lexicographically smallest pair
        best = min(pairs.items(), key=lambda kv: (-kv[1], kv[0]))[0]
        merges.append(best)
        merged = {}
        for syms, c in vocab.items():
            out, i = [], 0
            while i < len(syms):
                if i < len(syms) - 1 and (syms[i], syms[i + 1]) == best:
                    out.append(syms[i] + syms[i + 1])
                    i += 2
                else:
                    out.append(syms[i])
                    i += 1
            merged[tuple(out)] = merged.get(tuple(out), 0) + c
        vocab = merged
    return Codec(merges, k)


def boundary_delta_matrix(codec_a: Codec, codec_b: Codec, probes: list) -> list:
    """B in {0,1}^(n_probes x (L-1)) — did the boundary at each position CHANGE?

    This is the refit channel's seam (`gates-l1-seam`): the L1 gate's participation
    ratio is computed on this matrix. Probes must all be the same length L, so B
    is rectangular with no padding — a padded matrix would hand the rank estimator
    a constant column and inflate the answer for free.
    """
    if not probes:
        raise ValueError("probes must be non-empty")
    length = len(probes[0])
    for p in probes:
        if len(p) != length:
            raise ValueError(f"probes must be equal length: {length} vs {len(p)}")
    rows = []
    for p in probes:
        ba, bb = codec_a.boundaries(p), codec_b.boundaries(p)
        changed = ba ^ bb
        rows.append([1.0 if i in changed else 0.0 for i in range(1, length)])
    return rows


def boundary_shift_rate(codec_a: Codec, codec_b: Codec, probes: list) -> float:
    """Mean over probes of |bnd(a) XOR bnd(b)| / (L-1) — the G-1 drift measure."""
    b = boundary_delta_matrix(codec_a, codec_b, probes)
    return sum(sum(row) for row in b) / (len(b) * len(b[0]))


def atomicity_audit(codec: Codec, forms_in_context: list) -> dict:
    """How many of `forms_in_context` [(form_jamo, context_jamo), ...] survive as
    a single token under `codec`.

    `rig-drift-deficit-asserted`: the frozen codec must show 0/N single-token for
    the novel allomorphs (a full atomicity deficit) and the refit codec must show
    N/N. Without both there is no contrast and the twin compares nothing.
    """
    hits = [bool(codec.is_single_token(f, c)) for f, c in forms_in_context]
    n = len(hits)
    return {"n": n, "single_token": sum(hits), "deficit": 1.0 - (sum(hits) / n if n else 0.0)}
