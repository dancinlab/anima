"""decoder_qsample.py — DECODER inference SAMPLING wired to the qentropy SSOT.

H_924 M3 — the canonical "DECODER sampling = QUANTUM-default · DETERMINISTIC-auxiliary"
reference. SW-runnable on a plain Mac ($0, no pi5/AKIDA device, no GPU).

WHAT THIS IS (and what it deliberately is NOT)
==============================================
The anima DECODER turns the substrate/AKIDA forward output (logits over the byte/token
vocabulary) into a chosen token. That selection has two layers:

  1. the FORWARD compute  — threshold-and-fire on AKIDA silicon (or the byte-exact SW
     mirror). This is DETERMINISTIC and byte-identical by design (H_922/H_680). It is
     a pure function of the input + weights. THIS LAYER IS UNTOUCHED HERE.

  2. the SAMPLING / token-selection layer — temperature scaling + multinomial draw (or
     a stochastic tie-break) over the forward logits. THIS is the only place an entropy
     source enters, and it is what this module wires to the qentropy SSOT.

So: the quantum entropy enters ONLY at sampling/token-selection. It never touches the
forward matmul / threshold-and-fire. Flip `ANIMA_ENTROPY_MODE` and the SAME logits are
sampled under a different entropy policy — the forward result is bit-for-bit identical
in both modes. This is exactly the H_924 thesis that the quantum coupling is a property
of the *seed point*, not of the AKIDA silicon: the sampler is substrate-agnostic SW and
still couples to quantum entropy.

QUANTUM-DEFAULT · DETERMINISTIC-AUXILIARY
=========================================
The sampler's RNG comes from `qentropy.rng("decoder_sample")`:

  * ANIMA_ENTROPY_MODE=quantum        (DEFAULT) — the numpy Generator is seeded from the
                                        committed real-ANU vacuum-fluctuation buffer
                                        (tier anu_committed). This is the primary mode.
  * ANIMA_ENTROPY_MODE=deterministic  (AUXILIARY) — the numpy Generator is the reproducible
                                        PRNG (seed ANIMA_ENTROPY_SEED, default 187). This is
                                        the control arm for A/B benchmarking + CI.

Both modes draw from ONE SSOT so flipping the env benchmarks quantum-vs-deterministic
DECODER sampling with zero code change. Provenance (mode·tier·sha256·label) is recorded
into every result via `qentropy.last_provenance()`.

HONEST SCOPE / NON-CLAIM (#123-A)
=================================
The statistical quality of ANU quantum == chacha20 PRNG (JSD 23x under the NIST
threshold). This module does NOT claim quantum produces "better" samples. The value is
PROVENANCE · auditability · physical origin — which is exactly why a deterministic
auxiliary exists (the two are statistically indistinguishable; the difference that
matters is the audit trail, not the token distribution). The AKIDA HW forward
determinism is unchanged: only the SW sampling layer is wired.

USAGE
=====
    ANIMA_ENTROPY_MODE=quantum       python CORE/DECODER/decoder_qsample.py
    ANIMA_ENTROPY_MODE=deterministic python CORE/DECODER/decoder_qsample.py
"""
from __future__ import annotations

import json
import os
import sys

import numpy as np

# ── import the qentropy SSOT (soft dependency) ───────────────────────────────
# We insert mirror/qmirror/seed on sys.path and import qentropy. If for any reason
# it is unavailable, we fall back to numpy.default_rng so this reference NEVER
# hard-depends on the SSOT being importable — but in that case the entropy policy
# degrades to a plain (deterministic) PRNG and provenance is tagged accordingly.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.abspath(os.path.join(_HERE, os.pardir, os.pardir))
_QENTROPY_DIR = os.path.join(_REPO, "mirror", "qmirror", "seed")
if _QENTROPY_DIR not in sys.path:
    sys.path.insert(0, _QENTROPY_DIR)

try:
    import qentropy  # type: ignore

    def _sampler_rng():
        # qentropy.rng() returns a numpy Generator seeded from the active policy
        # (quantum-seeded in quantum mode; the reproducible PRNG in auxiliary mode).
        return qentropy.rng("decoder_sample")

    def _provenance() -> dict:
        return qentropy.last_provenance()

    def _mode() -> str:
        return qentropy.mode()

    _QENTROPY_OK = True
except Exception as _e:  # noqa: BLE001 — never hard-fail for lack of the SSOT
    sys.stderr.write(f"[decoder_qsample] WARN: qentropy SSOT unavailable ({_e}); "
                     "falling back to numpy.default_rng (provenance tagged).\n")

    def _sampler_rng():
        return np.random.default_rng()

    def _provenance() -> dict:
        return {"mode": "numpy_fallback", "tier": "default_rng(unseeded)",
                "sha256": None, "request_id": None, "n_drawn": None,
                "label": "decoder_sample"}

    def _mode() -> str:
        return "numpy_fallback"

    _QENTROPY_OK = False


# ── the sampling layer (this is the only stochastic step) ────────────────────
def softmax(logits: np.ndarray, temperature: float = 1.0) -> np.ndarray:
    """Temperature-scaled softmax over a logits vector. DETERMINISTIC: a pure
    function of (logits, temperature) — identical in quantum and deterministic
    mode. The probabilities are the same; only the draw FROM them differs."""
    z = np.asarray(logits, dtype=np.float64) / max(temperature, 1e-8)
    z = z - z.max()                      # stable
    e = np.exp(z)
    return e / e.sum()


def sample_token(logits: np.ndarray, temperature: float = 1.0,
                 rng: "np.random.Generator | None" = None) -> int:
    """Draw ONE token id from the temperature-scaled distribution over `logits`.

    The randomness comes from `rng` — which is `qentropy.rng("decoder_sample")`
    by default, so the DECODER sampling layer is quantum-default·deterministic-
    auxiliary. The forward `logits` are passed in unchanged (this function never
    touches the forward compute)."""
    if rng is None:
        rng = _sampler_rng()
    probs = softmax(logits, temperature)
    # multinomial draw via the inverse-CDF on a single uniform from the policy RNG.
    u = rng.random()                      # one uniform in [0,1) from the active policy
    return int(np.searchsorted(np.cumsum(probs), u, side="right"))


def sample_n(logits: np.ndarray, n: int, temperature: float = 1.0) -> dict:
    """Draw `n` tokens from the SAME logits under the active entropy policy and
    return the draws + the recorded provenance. One `rng` is drawn from the SSOT
    so all n draws share one auditable provenance record."""
    rng = _sampler_rng()
    draws = [sample_token(logits, temperature=temperature, rng=rng) for _ in range(n)]
    return {
        "mode": _mode(),
        "provenance": _provenance(),
        "temperature": temperature,
        "logits": list(map(float, logits)),
        "probs": [round(float(p), 4) for p in softmax(logits, temperature)],
        "draws": draws,
        "argmax_forward": int(np.argmax(logits)),  # deterministic forward pick (unchanged)
        "qentropy_ssot": _QENTROPY_OK,
    }


# ── both-mode SW demonstrator (fixed logits, $0, no device) ──────────────────
def _demo() -> dict:
    # A FIXED logits vector over a tiny 6-token toy vocab. The forward result that
    # produced these logits is deterministic; we only vary the SAMPLING policy.
    logits = np.array([2.0, 1.0, 0.5, 3.0, 0.2, 1.5], dtype=np.float64)
    out = sample_n(logits, n=16, temperature=1.0)
    out["vocab"] = ["t0", "t1", "t2", "t3", "t4", "t5"]
    # histogram of sampled token ids (which tokens, how often)
    hist = {int(k): int(v) for k, v in zip(*np.unique(out["draws"], return_counts=True))}
    out["histogram"] = hist
    return out


if __name__ == "__main__":
    print(json.dumps(_demo(), indent=2))
