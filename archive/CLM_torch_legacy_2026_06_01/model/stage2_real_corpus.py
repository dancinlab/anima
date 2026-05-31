"""STAGE-2 real-corpus loader (@L3) — kowiki bytes, NOT the synthetic toy.

STAGE-1 (toy) trained on `data.make_synthetic_corpus` (LCG pattern families).
@L3 requires STAGE-2 to run on the REAL @corpus clm_p1 byte lanes. The committed
real corpus is CLM/corpus/sample/{web,register}.bytes — the kowiki-derived
CC-BY-SA web lane + the curated register lane (CLM/corpus/clm_p1.corpus.kosmos,
sha256-pinned in CLM/corpus/sample/manifest.json). The larger `full/` crawl is
gitignored/local-only (kowiki rate-limited the crawl host — manifest "honest
partial"); the committed real bytes are the reproducible production corpus.

This module loads those real bytes and tiles them up to a requested per-lane
length (the real sample is ~830 bytes/lane; tiling gives the router a stable
stream to route over without inventing synthetic structure). It is a drop-in
replacement for make_synthetic_corpus returning the SAME (web, register)
tuple shape, so run_array_sweep / run_dispatch_kl can swap corpus by import.

HONEST (@L5): the byte VOLUME of the committed real corpus is small; STAGE-2's
production lever is the REAL byte distribution + the scaled d_model/E/steps, not
a multi-GB corpus. The scope is stated verbatim in each verdict.

Mac-forbidden (@L1): any caller that TRAINS/MEASURES with this corpus must run
on ubu-1 / runpod. This loader itself is pure-python (no torch) and only reads
files, but the sweeps that import it MUST be dispatched to the GPU host.
"""

from __future__ import annotations

import os
from typing import List, Tuple

_HERE = os.path.dirname(os.path.abspath(__file__))
_CORPUS = os.path.join(os.path.dirname(_HERE), "corpus", "sample")


def _load_bytes(path: str) -> List[int]:
    vals: List[int] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                vals.append(int(line) & 0xFF)
    return vals


def _tile(seq: List[int], n: int) -> List[int]:
    if not seq:
        raise ValueError("empty lane")
    out: List[int] = []
    while len(out) < n:
        out.extend(seq)
    return out[:n]


def make_real_corpus(
    n_bytes_per_lane: int = 8192, seed: int = 0, corpus_dir: str = _CORPUS
) -> Tuple[List[int], List[int]]:
    """Return (web_bytes, register_bytes) from the committed REAL kowiki corpus.

    Signature mirrors data.make_synthetic_corpus (seed accepted, unused — the
    real bytes are fixed; tiling is deterministic) so it is a drop-in swap.
    """
    web = _load_bytes(os.path.join(corpus_dir, "web.bytes"))
    reg = _load_bytes(os.path.join(corpus_dir, "register.bytes"))
    return _tile(web, n_bytes_per_lane), _tile(reg, n_bytes_per_lane)


if __name__ == "__main__":
    w, r = make_real_corpus(2048)
    print("real corpus loaded: web=%d register=%d (tiled from sample/*.bytes)"
          % (len(w), len(r)))
