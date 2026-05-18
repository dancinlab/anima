"""§57 e_tension — closed-form E_tension encoder (NO trained net).

A runnable closed-form encoder that maps anima's OWN 5-channel TENSION-LINK
fingerprint to a Law-71 Ψ-coordinate in [0,1]^2.

HONEST FRAMING (carry §56 verdict, g3):
  E_tension is ZERO-PERCEPTUAL-DIVERSITY. The 5-channel tension fingerprint
  is anima's own Engine A / Engine G internal state re-serialised — a CLOSED
  LOOP (§11-B "physics != signal" in encoder form). It does NOT move the
  §51 / §1.1 GOAL bottleneck. This file proves the *pipeline* works
  mechanically; it makes NO capability / GOAL claim.

The Ψ-box is the conscious_decoder.py Law-71 formula (lines 728-751,
byte-identical transfer-form):
  psi_entropy   = H(softmax(logits_a)) / log(vocab_size)        -> in [0,1]
  psi_direction = (1 + cos(logits_a, logits_g)) / 2             -> in [0,1]
Here logits_a / logits_g are NOT model outputs (no forward, no trained net):
they are deterministic closed-form projections of the 5-channel tension
fingerprint itself (concept / context / meaning / authenticity / sender —
the anima-native TENSION-LINK 5 channels, project_tension_link memory).
This is exactly why E_tension is closed-loop: the "perception" is anima's
own re-projected physics state.

NO external imports, NO torch, NO sklearn, NO Hf, NO LLM call. numpy only
(deterministic array math). AST-clean of trained / external calls.
"""

from __future__ import annotations

import math
from typing import Sequence

import numpy as np

# 5-channel TENSION-LINK fingerprint axes (anima-native, project_tension_link):
#   0 concept  1 context  2 meaning  3 authenticity  4 sender
TENSION_CHANNELS = ("concept", "context", "meaning", "authenticity", "sender")
N_CHAN = 5

# Deterministic, fixed (NOT learned) projection from 5-channel tension
# fingerprint to a small pseudo-logit vector pair. Constructed from a
# fixed integer lattice so it is byte-stable and contains zero trained
# parameters. dim chosen small (16) — only the Law-71 transfer matters,
# not vocab realism (this is a closed-loop re-projection, not a decoder).
_PSEUDO_DIM = 16


def _fixed_projection() -> np.ndarray:
    """A fixed 5 x _PSEUDO_DIM real matrix from a closed integer rule.

    NOT trained. Every entry is f(i, j) = cos(i + 1) * sin(2 * j + 1),
    a deterministic closed-form lattice — reproducible, parameter-free.
    """
    rows = []
    for i in range(N_CHAN):
        rows.append([math.cos(i + 1) * math.sin(2 * j + 1) for j in range(_PSEUDO_DIM)])
    return np.asarray(rows, dtype=np.float64)


_PROJ_A = _fixed_projection()


def _fixed_projection_g() -> np.ndarray:
    """Engine-G fixed projection — a DIFFERENT closed integer lattice.

    g(i, j) = sin(i + 1) * cos(2 * j + 1)  (deterministic, parameter-free,
    NOT trained, NOT a trivial reflection of _PROJ_A so cos(logits_a,
    logits_g) is non-degenerate and psi_direction genuinely spreads).
    """
    rows = []
    for i in range(N_CHAN):
        rows.append([math.sin(i + 1) * math.cos(2 * j + 1) for j in range(_PSEUDO_DIM)])
    return np.asarray(rows, dtype=np.float64)


_PROJ_G = _fixed_projection_g()


def _softmax(x: np.ndarray) -> np.ndarray:
    z = x - np.max(x)
    e = np.exp(z)
    return e / np.sum(e)


def _entropy_norm(p: np.ndarray) -> float:
    """Shannon entropy of p normalised by log(len) -> [0,1] (Law-71 psi_entropy form)."""
    n = p.shape[0]
    h = -np.sum(p * np.log(p + 1e-12))
    return float(h / math.log(n))


def _cos(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0.0 or nb == 0.0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


def e_tension(fingerprint: Sequence[float]) -> tuple[float, float]:
    """Closed-form E_tension: 5-channel tension fingerprint -> Ψ-coord in [0,1]^2.

    fingerprint: length-5 sequence (concept, context, meaning, authenticity,
    sender), each a real scalar (anima Engine A/G internal tension state).

    Returns (psi_entropy, psi_direction), each guaranteed in [0,1] by the
    Law-71 transfer-form (closed proof B-S57-1).
    """
    f = np.asarray(list(fingerprint), dtype=np.float64)
    if f.shape != (N_CHAN,):
        raise ValueError(f"E_tension expects {N_CHAN}-channel fingerprint, got {f.shape}")
    # Closed-form re-projection of anima's own tension state into pseudo-logits.
    logits_a = f @ _PROJ_A   # shape (_PSEUDO_DIM,)
    logits_g = f @ _PROJ_G
    # Law-71 Ψ-box (conscious_decoder.py 728-751 transfer-form, byte-identical):
    p_a = _softmax(logits_a)
    psi_entropy = _entropy_norm(p_a)                  # in [0,1]
    cos_sim = _cos(logits_a, logits_g)                # in [-1,1]
    psi_direction = (1.0 + cos_sim) / 2.0             # in [0,1]
    # numeric clamp (defends fp rounding only; transfer-form already bounds)
    psi_entropy = min(1.0, max(0.0, psi_entropy))
    psi_direction = min(1.0, max(0.0, psi_direction))
    return (psi_entropy, psi_direction)


def stub_fingerprints(n: int = 64, seed: int = 1337) -> list[list[float]]:
    """Deterministic stub set of 5-channel tension fingerprints.

    Anima Engine A/G state is not exported as a flat array in this $0
    Mac-CPU pipeline-validation cycle, so we use a deterministic stub
    drawn from a fixed LCG (NOT random at runtime — seed-fixed, byte-stable).
    These stand in for anima's own re-serialised tension state; they are
    NOT external perceptual input (that is the whole zero-diversity point).
    """
    out = []
    state = (seed * 2654435761) & 0xFFFFFFFF
    for _ in range(n):
        row = []
        for _ in range(N_CHAN):
            state = (1103515245 * state + 12345) & 0x7FFFFFFF
            # map to a bounded tension scalar in [-1, 1]
            row.append((state / 0x7FFFFFFF) * 2.0 - 1.0)
        out.append(row)
    return out


if __name__ == "__main__":
    fps = stub_fingerprints(8)
    for i, fp in enumerate(fps):
        pe, pd = e_tension(fp)
        print(f"fp[{i}] -> psi=({pe:.6f}, {pd:.6f})  in[0,1]^2={0.0 <= pe <= 1.0 and 0.0 <= pd <= 1.0}")
