"""qentropy.py — unified entropy SSOT for anima: QUANTUM default, DETERMINISTIC auxiliary.

WHY THIS FILE EXISTS
====================
Across the H_921→H_923 arc we proved that anima's only stochastic levers are SEED
POINTS over otherwise-deterministic compute (AKIDA learning init/input, spontaneous
R2 noise, and — by generalization (H_924) — the SW numpy/torch learning+inference
paths). Each lever was wired ad-hoc with its own `ANIMA_QRNG_*` env. This module
unifies ALL of them behind ONE call so that:

  1. every seed/sample point in anima (HW learning, HW spontaneous, HW/SW inference,
     SW numpy learning, torch CLM) draws from the SAME entropy policy;
  2. the policy is QUANTUM-BY-DEFAULT (ANU vacuum-fluctuation) with a DETERMINISTIC
     AUXILIARY mode that is one env-var away — so the two can be A/B BENCHMARKED
     later by flipping `ANIMA_ENTROPY_MODE` and re-running, nothing else;
  3. provenance (mode, tier, sha256, request_id) is always recorded, so any draw is
     auditable after the fact regardless of which mode produced it.

DESIGN: QUANTUM DEFAULT · DETERMINISTIC AUXILIARY
=================================================
`ANIMA_ENTROPY_MODE` (process-global) selects the policy:

    quantum        (DEFAULT) — physical ANU vacuum-fluctuation entropy. Primary mode.
    deterministic  (AUXILIARY) — numpy PRNG seeded by ANIMA_ENTROPY_SEED (default 187).
                                 The reproducible control arm for benchmarking + CI.

Quantum mode resolves a byte buffer in this order (first hit wins), so it works
offline (pre-pulled) AND online (fresh draw) AND never hard-crashes a long run:

    a. ANIMA_QRNG_BUF=<path>         — caller-supplied ANU buffer (e.g. a fresh
                                       anu_pull.py draw for THIS run).
    b. <repo>/mirror/qmirror/seed/qrng_lora_init_live.bin  — committed real ANU
                                       vacuum-fluctuation bytes (tier anu_legacy).
    c. live pull via anu_pull.py     — only if ANIMA_QRNG_LIVE=1 (opt-in network);
                                       uses secret-keyed flat.anu_key_paid/free.
    d. SAFE FALLBACK                 — if no buffer is reachable, fall back to the
                                       deterministic PRNG but TAG provenance
                                       mode="quantum_fallback_prng" + emit a stderr
                                       WARN, so a training run never dies for lack of
                                       entropy and the degradation is always visible
                                       in the audit trail (never a silent fake).

HONEST NON-CLAIM (#123-A QA6 audit, NIST SP 800-22 7/7):
    The STATISTICAL quality of ANU quantum == chacha20 PRNG (JSD 0.000433, 23x under
    threshold). This module does NOT claim quantum gives "more random" numbers. The
    value of the quantum mode is PROVENANCE · auditability · algorithmic-attack
    immunity · ontology (physical origin). It is NOT a phenomenal-consciousness claim.
    That is exactly why a deterministic auxiliary exists: for A/B benchmarking the two
    are expected to be statistically indistinguishable; the difference that matters is
    the audit trail, not the bit distribution.

PUBLIC API (all return numpy arrays / ints; all record provenance via last_provenance())
    qentropy_bits(n, label="")     -> np.ndarray[uint8] of {0,1}, length n
    qentropy_bytes(n, label="")    -> np.ndarray[uint8] 0..255, length n
    qentropy_uniform(n, hi, ...)   -> np.ndarray[int]  0..hi-1, length n  (e.g. R2 noise 0..3)
    qentropy_seed(label="")        -> int  (a 63-bit seed for libs that want one int)
    rng(label="")                  -> a numpy Generator seeded from the active source
                                      (quantum-seeded Generator in quantum mode; the
                                      deterministic PRNG in auxiliary mode)
    last_provenance()              -> dict  (mode, tier, sha256, request_id, n_drawn, label)
    mode()                         -> "quantum" | "deterministic"

Every consumer (AKIDA edge-learn, spontaneous R2, plasticity_sw_approx, Lane-P torch,
DECODER sampling) should call qentropy_* instead of np.random directly. Flipping
ANIMA_ENTROPY_MODE then benchmarks quantum-vs-deterministic with zero code change.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys

import numpy as np

# ── configuration (all via env so a benchmark run flips them, not the code) ──
_MODE = os.environ.get("ANIMA_ENTROPY_MODE", "quantum").strip().lower()   # quantum|deterministic
_DET_SEED = int(os.environ.get("ANIMA_ENTROPY_SEED", "187"))              # auxiliary PRNG seed
_BUF_ENV = os.environ.get("ANIMA_QRNG_BUF", "")                           # explicit ANU buffer
_LIVE = os.environ.get("ANIMA_QRNG_LIVE", "0") == "1"                     # opt-in fresh pull
_SECRET_BIN = os.environ.get("SECRET_BIN", "secret")

# committed real-ANU buffer (relative to this file: mirror/qmirror/seed/<bin>)
_HERE = os.path.dirname(os.path.abspath(__file__))
_COMMITTED_BUF = os.path.join(_HERE, "qrng_lora_init_live.bin")
_PULLER = os.path.join(_HERE, "anu_pull.py")

# ── module state: the resolved quantum byte pool + a rolling cursor ──────────
_pool: bytes | None = None          # the ANU byte buffer when in quantum mode
_pool_sha: str | None = None
_pool_tier: str | None = None
_cursor = 0                          # next unused byte in _pool (cycles if exhausted)
_det_rng = np.random.default_rng(_DET_SEED)   # the deterministic auxiliary generator
_last_prov: dict = {}                # provenance of the most recent draw


def mode() -> str:
    """Active entropy policy: 'quantum' (default) or 'deterministic' (auxiliary)."""
    return "deterministic" if _MODE.startswith("det") else "quantum"


def _try_live_pull(n_bytes: int) -> bytes | None:
    """Opt-in (ANIMA_QRNG_LIVE=1) fresh ANU draw via the secret-keyed anu_pull.py."""
    if not (_LIVE and os.path.exists(_PULLER)):
        return None
    out = "/tmp/anima_qentropy_live.bin"
    try:
        r = subprocess.run([sys.executable, _PULLER, "--bytes", str(max(n_bytes, 1024)),
                            "--out", out, "--provenance", "/tmp/anima_qentropy_prov.jsonl"],
                           capture_output=True, text=True, timeout=60)
        if r.returncode == 0 and os.path.exists(out):
            return open(out, "rb").read()
    except Exception:  # noqa: BLE001  (network/secret failure -> fall through)
        return None
    return None


def _resolve_pool(min_bytes: int) -> None:
    """Lazily fill the quantum byte pool (resolution order a→d). Idempotent-ish:
    only (re)resolves when the pool is missing or too small for the request."""
    global _pool, _pool_sha, _pool_tier, _cursor
    if _pool is not None and len(_pool) >= min_bytes:
        return
    # (a) explicit caller buffer
    if _BUF_ENV and os.path.exists(_BUF_ENV):
        _pool, _pool_tier = open(_BUF_ENV, "rb").read(), "anu_explicit"
    # (b) committed real-ANU buffer
    elif os.path.exists(_COMMITTED_BUF):
        _pool, _pool_tier = open(_COMMITTED_BUF, "rb").read(), "anu_committed"
    else:
        _pool = None
    # (c) opt-in fresh live pull (preferred when armed even if a static buf exists)
    if _LIVE:
        live = _try_live_pull(min_bytes)
        if live:
            _pool, _pool_tier = live, "anu_live"
    if _pool:
        _pool_sha = hashlib.sha256(_pool).hexdigest()
        _cursor = 0


def _take_bytes(n: int, label: str) -> np.ndarray:
    """Core draw. Honors the mode; in quantum mode pulls from the ANU pool with a
    safe deterministic fallback that is ALWAYS tagged in provenance (never silent)."""
    global _cursor, _last_prov
    if mode() == "deterministic":
        b = _det_rng.integers(0, 256, size=n, dtype=np.uint8)
        _last_prov = {"mode": "deterministic", "tier": f"numpy_prng(seed={_DET_SEED})",
                      "sha256": None, "request_id": None, "n_drawn": n, "label": label}
        return b
    # quantum mode
    _resolve_pool(n)
    if _pool:
        idx = (np.arange(_cursor, _cursor + n) % len(_pool))   # cycle if exhausted
        _cursor = (_cursor + n) % len(_pool)
        _last_prov = {"mode": "quantum", "tier": _pool_tier, "sha256": _pool_sha,
                      "request_id": None, "n_drawn": n, "label": label,
                      "cycled": bool(n > len(_pool))}
        return np.frombuffer(_pool, dtype=np.uint8)[idx].copy()
    # (d) SAFE FALLBACK — quantum requested but no buffer reachable. Degrade to PRNG
    # but TAG it loudly so the audit trail records the degradation (never a fake).
    sys.stderr.write("[qentropy] WARN: quantum mode requested but no ANU buffer "
                     "reachable; falling back to deterministic PRNG (tagged).\n")
    b = _det_rng.integers(0, 256, size=n, dtype=np.uint8)
    _last_prov = {"mode": "quantum_fallback_prng", "tier": f"numpy_prng(seed={_DET_SEED})",
                  "sha256": None, "request_id": None, "n_drawn": n, "label": label}
    return b


# ── public API ───────────────────────────────────────────────────────────────
def qentropy_bytes(n: int, label: str = "") -> np.ndarray:
    """n entropy bytes (0..255) under the active policy."""
    return _take_bytes(n, label)


def qentropy_bits(n: int, label: str = "") -> np.ndarray:
    """n entropy bits {0,1} (low bit of n bytes — keeps cursor accounting simple)."""
    return (_take_bytes(n, label) & 0x1).astype(np.uint8)


def qentropy_uniform(n: int, hi: int, label: str = "") -> np.ndarray:
    """n integers in [0, hi). Used e.g. for the R2 noise input (hi=4 -> 0..3).
    Masks to the low bits when hi is a power of two (unbiased); else modulo (tiny bias
    acceptable for noise — the deterministic auxiliary uses the same map for parity)."""
    raw = _take_bytes(n, label).astype(np.int64)
    if hi > 0 and (hi & (hi - 1)) == 0:        # power of two -> exact mask
        return (raw & (hi - 1)).astype(np.int64)
    return (raw % hi).astype(np.int64)


def qentropy_seed(label: str = "") -> int:
    """A single 63-bit seed int, for libraries that take one seed (torch/np)."""
    b = _take_bytes(8, label)
    return int.from_bytes(bytes(b), "little") & ((1 << 63) - 1)


def rng(label: str = "") -> np.random.Generator:
    """A numpy Generator seeded from the active source — drop-in for default_rng().
    In deterministic mode this is reproducible; in quantum mode it is quantum-seeded
    (so downstream np.random calls inherit the chosen entropy policy)."""
    return np.random.default_rng(qentropy_seed(label))


def last_provenance() -> dict:
    """Provenance of the most recent draw (mode·tier·sha256·request_id·n·label).
    Always populated — even the safe-fallback path tags itself here."""
    return dict(_last_prov)


def summary() -> dict:
    """One-shot description of the active policy (for logging into result JSON)."""
    return {"entropy_mode": mode(), "det_seed": _DET_SEED, "live_pull": _LIVE,
            "committed_buf_present": os.path.exists(_COMMITTED_BUF)}


if __name__ == "__main__":   # tiny self-test / both-mode demo (no network needed)
    import json
    print(json.dumps({
        "summary": summary(),
        "bits8": qentropy_bits(8, "selftest").tolist(),
        "provenance": last_provenance(),
        "uniform0_3": qentropy_uniform(8, 4, "selftest").tolist(),
        "seed": qentropy_seed("selftest"),
    }, indent=2))
