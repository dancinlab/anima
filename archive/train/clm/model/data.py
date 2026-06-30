"""Toy byte-corpus loading + synthetic two-lane corpus generation.

The committed sample at CLM/corpus/sample/{web,register}.bytes is only ~800
newline-separated byte values per lane -- enough to smoke the loader but too
small to drive a meaningful routing-balance probe. This module can either:

  * load the committed sample (`load_sample_bytes`), or
  * generate a larger SYNTHETIC two-lane byte corpus (`make_synthetic_corpus`).

HONEST NOTE: the synthetic corpus is a TOY distribution -- two simple,
deliberately-distinguishable pattern families standing in for the two real
source lanes (bulk-web coherence vs curated register, P0 d1). It is intuition
material only; it is NOT a scaled corpus and any routing result on it does not
transfer to scale (the toy != scale lesson, H_666 / H_847 Q4).

Lane construction (synthetic):
  * "web"      lane: a low-entropy repeating-motif stream over byte band
                     [0x20, 0x7e] (printable-ASCII-like), with occasional jumps.
  * "register" lane: a distinct higher-byte band [0x80, 0xff] cyclic pattern
                     (stands in for a separate register/anima source).
The two lanes occupy largely disjoint byte bands so that, IF a router can
separate sources at all, there is a separable signal to find -- this is the
charitable toy setup, not a guarantee the model will use it.
"""

from __future__ import annotations

import os
from typing import List, Tuple

import torch


def load_sample_bytes(path: str) -> List[int]:
    """Load a committed *.bytes file (newline-separated decimal byte values)."""
    vals: List[int] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                vals.append(int(line) & 0xFF)
    return vals


def _lcg(seed: int):
    """Tiny deterministic PRNG (LCG) so corpus is reproducible without numpy."""
    state = seed & 0x7FFFFFFF
    while True:
        state = (1103515245 * state + 12345) & 0x7FFFFFFF
        yield state


def make_synthetic_corpus(
    n_bytes_per_lane: int = 8192, seed: int = 0
) -> Tuple[List[int], List[int]]:
    """Return (web_bytes, register_bytes) -- two toy lanes (see module docstring)."""
    rng = _lcg(seed + 1)

    # --- web lane: repeating low-band motifs with rare jumps --------------- #
    web_motifs = [
        [0x74, 0x68, 0x65, 0x20],   # "the "
        [0x61, 0x6e, 0x64, 0x20],   # "and "
        [0x6f, 0x66, 0x20],         # "of "
        [0x69, 0x6e, 0x67, 0x20],   # "ing "
    ]
    web: List[int] = []
    while len(web) < n_bytes_per_lane:
        r = next(rng)
        motif = web_motifs[r % len(web_motifs)]
        web.extend(motif)
        if (next(rng) % 17) == 0:               # rare jump within low band
            web.append(0x20 + (next(rng) % 0x5e))
    web = web[:n_bytes_per_lane]

    # --- register lane: distinct high-band cyclic pattern ----------------- #
    reg: List[int] = []
    base = 0x80
    period = 11
    while len(reg) < n_bytes_per_lane:
        r = next(rng)
        start = base + (r % (0x100 - base - period))
        for j in range(period):
            reg.append((start + j) & 0xFF | 0x80)   # keep in high band
        if (next(rng) % 23) == 0:
            reg.append(0x80 + (next(rng) % 0x7f))
    reg = reg[:n_bytes_per_lane]

    return web, reg


def make_batches(
    byte_stream: List[int],
    seq_len: int,
    batch_size: int,
    n_batches: int,
    seed: int = 0,
) -> List[Tuple[torch.Tensor, torch.Tensor]]:
    """Slice a byte stream into (input, target) next-byte batches.

    target is input shifted by one (standard next-token LM objective).
    """
    rng = _lcg(seed + 7)
    data = torch.tensor(byte_stream, dtype=torch.long)
    n = data.numel()
    batches = []
    need = seq_len + 1
    for _ in range(n_batches):
        xs, ys = [], []
        for _ in range(batch_size):
            start = next(rng) % max(1, n - need)
            chunk = data[start : start + need]
            if chunk.numel() < need:                 # wrap / pad guard
                chunk = torch.cat([chunk, data[: need - chunk.numel()]])
            xs.append(chunk[:-1])
            ys.append(chunk[1:])
        batches.append((torch.stack(xs), torch.stack(ys)))
    return batches


def lane_tagged_stream(
    web: List[int], register: List[int], block: int = 64
) -> Tuple[List[int], List[int]]:
    """Interleave the two lanes in blocks; return (stream, lane_id_per_byte).

    lane_id: 0 = web, 1 = register. Used by the content-separation diagnostic
    (does expert usage differ between lanes?).
    """
    stream: List[int] = []
    lane: List[int] = []
    iw = ir = 0
    turn = 0
    while iw < len(web) or ir < len(register):
        if turn == 0 and iw < len(web):
            seg = web[iw : iw + block]
            stream.extend(seg)
            lane.extend([0] * len(seg))
            iw += block
        elif ir < len(register):
            seg = register[ir : ir + block]
            stream.extend(seg)
            lane.extend([1] * len(seg))
            ir += block
        turn ^= 1
    return stream, lane
