"""core/shared_seed.py — QRNG shared-seed key, replayable classical store.

py 2-production twin of core/shared_seed.hexa — byte-exact mirror (owner directive 2026-07-09
"py 자체구현 · 언어간 상호의존 0"). A quantum key stored LOCALLY (classical, replayable); a
fork copies the cursor so children stay in lockstep. Integer-only draw (b mod k) — no float,
no GPU/FFI — so this mirror is byte-exact by construction. Loading uses `od` (unix tool, not
hexa) exactly like the hexa twin, matching core/engine_cli.py's existing od-based byte read.
"""

import subprocess as _subprocess


class SharedSeed:
    """The quantum key + consume cursor. fork copies both so children stay in lockstep."""
    __slots__ = ("bytes", "cursor")

    def __init__(self, bytes_, cursor):
        self.bytes = bytes_    # the quantum key, stored LOCALLY (classical store; replayable)
        self.cursor = cursor   # next byte to consume; fork copies this


def shared_seed_load(path):
    # `od -An -tu1 -v <path>` → whitespace-separated unsigned bytes. NOTE: od wraps at 16
    # bytes/line, so a key > 16 bytes is MULTI-LINE. The hexa twin splits on " " only, which
    # keeps a "\n"-joined token across a line break — correct for ≤16-byte keys, but a
    # >16-byte key would carry an unparsable token there. This py twin splits on ANY
    # whitespace (correct for any key size); if hexa is ever fed a >16-byte key the twins
    # would diverge → hexa-side parity-fix candidate (shared_seed.hexa split " " → split()).
    raw = _subprocess.run(["od", "-An", "-tu1", "-v", path],
                          capture_output=True, text=True).stdout.strip()
    toks = raw.split()
    bytes_ = []
    i = 0
    while i < len(toks):
        t = toks[i].strip()
        if len(t) > 0:
            bytes_ = bytes_ + [int(t)]
        i = i + 1
    return SharedSeed(bytes_, 0)


def shared_seed_fork(parent):
    return SharedSeed(parent.bytes, parent.cursor)


def shared_seed_remaining(s):
    return len(s.bytes) - s.cursor


def shared_seed_draw(s, k):
    if k <= 0:
        return [0, s.cursor]
    if s.cursor >= len(s.bytes):
        return [0, s.cursor]                       # key exhausted ⇒ 0 (caller refills)
    b = s.bytes[s.cursor]
    v = b - (b // k) * k                            # b mod k, integer-only
    return [v, s.cursor + 1]


def shared_seed_choose(s, n_options):
    return shared_seed_draw(s, n_options)
