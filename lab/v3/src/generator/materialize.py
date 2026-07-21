"""Encode phase streams and eval items into token-id sequences under a codec.

Every training path — the $0 numpy proxy, a local MPS run, or a rented GPU —
consumes the same thing: a stream of token ids under a specific codec, plus the
forced-choice eval items encoded the same way. This module produces both, so the
codec-fairness (each arm scored under its OWN tokenization) is established here,
once, rather than re-derived per trainer.

Deterministic, stdlib only.
"""

from __future__ import annotations

import random

from codec import SENTINEL
from lang import to_jamo
from stream import NEG_MARK, POS_MARK, line


def vocab(codec) -> dict:
    """Map every token the codec can emit to a contiguous id.

    The vocabulary is the set of DISTINCT tokens the codec produces over the
    jamo alphabet plus the merges. Built by encoding the base alphabet and the
    merge outputs; a token unseen at fit time still encodes (as its pieces), so
    the id space is closed under `encode_tokens`. Ids are assigned in sorted
    token order for determinism.
    """
    toks = set()
    # base jamo alphabet + sentinel + marks are always possible single tokens
    for base in (SENTINEL, to_jamo(POS_MARK), to_jamo(NEG_MARK)):
        for ch in base:
            toks.add(ch)
    # every merge output (and its pieces) is a token
    for pair in codec.merges:
        toks.add(pair[0] + pair[1])
        toks.add(pair[0])
        toks.add(pair[1])
    return {t: i for i, t in enumerate(sorted(toks))}


def encode_ids(codec, ids: dict, text_jamo: str) -> list:
    """Encode a jamo string to a list of token ids under `codec`.

    A token absent from `ids` (possible for an out-of-vocab merge) falls back to
    its constituent characters, each of which is always in `ids` (the base
    alphabet is seeded in `vocab`). This keeps every stream encodable with no
    silent drops.
    """
    out = []
    for tok in codec.encode_tokens(text_jamo):
        if tok in ids:
            out.append(ids[tok])
        else:
            for ch in tok:
                out.append(ids[ch])
    return out


def stream_ids(spec: dict, phase: int, codec, ids: dict, n_lines: int) -> list:
    """A flat token-id sequence for `n_lines` of the phase stream under `codec`.

    Frames each utterance exactly as the stream does — body SENTINEL mark
    SENTINEL — so the trainer sees the same structure the audits validated.
    """
    rng = random.Random(spec["seed"] * 1000 + phase * 7 + 991)
    sen = ids[SENTINEL]
    out = []
    for _ in range(n_lines):
        surf_marked = line(spec, phase, rng)  # body + SENTINEL + mark
        for piece in surf_marked.split(SENTINEL):
            out.extend(encode_ids(codec, ids, to_jamo(piece)))
            out.append(sen)
    return out


def eval_encoded(spec: dict, codec, ids: dict, items: list) -> list:
    """Encode each forced-choice item's pos/neg continuations under `codec`.

    Returns [{stem_ids, pos_ids, neg_ids, label, n_bytes_pos, n_bytes_neg}, ...].
    Byte counts are of the raw jamo (codec-independent), so a bits-per-byte score
    is comparable across arms with different tokenizations (salvage l6)."""
    out = []
    for it in items:
        stem_j = to_jamo(it["stem"])
        pos_j = to_jamo(it["pos"])
        neg_j = to_jamo(it["neg"])
        out.append({
            "stem_ids": encode_ids(codec, ids, stem_j),
            "pos_ids": encode_ids(codec, ids, pos_j),
            "neg_ids": encode_ids(codec, ids, neg_j),
            "label": it["label"],
            "n_bytes_pos": len(pos_j.encode("utf-8")),
            "n_bytes_neg": len(neg_j.encode("utf-8")),
        })
    return out
