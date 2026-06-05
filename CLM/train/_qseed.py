"""_qseed.py — Lane-P torch trainer bridge to the unified qentropy SSOT.

WHY THIS FILE EXISTS (H_924 M4)
================================
The torch Lane-P CLM trainers (train_lane_p.py / _3b.py / _split.py) seed their
weight-init + data-shuffle RNG from a single hardcoded `--seed` (default 42).
H_924 proved that anima's quantum/deterministic entropy coupling is a property
of the *seed point*, not of any one substrate (AKIDA HW · numpy SW). This module
is the THIRD substrate (torch) bridge: it derives the trainer's master seed from
`qentropy_seed("lane_p_torch_init")` so the run is QUANTUM-BY-DEFAULT with a
DETERMINISTIC-AUXILIARY toggle (`ANIMA_ENTROPY_MODE=quantum|deterministic`),
exactly like the AKIDA and numpy paths — proving substrate-agnostic across torch.

FALLBACK-SAFE BY DESIGN (additive, never a hard dependency)
===========================================================
The qentropy SSOT lives at <repo>/mirror/qmirror/seed/qentropy.py. If for ANY
reason it is not importable (path layout differs, module missing on a stripped
training pod, numpy absent, ...), `resolve_seed()` falls back to the caller's
existing hardcoded seed and the trainer behaves EXACTLY as before. The wire is
purely additive: existing runs that never set ANIMA_ENTROPY_MODE still get the
quantum default; a run that exports ANIMA_ENTROPY_MODE=deterministic gets the
reproducible auxiliary arm (the benchmark control). No trainer ever breaks for
lack of the SSOT.

The deterministic-AUXILIARY *fallback value* is the trainer's own hardcoded seed
(passed in as `fallback`), so the "no SSOT reachable" path is identical to the
historical behavior — bit-for-bit, no surprise drift.
"""
from __future__ import annotations

import os
import sys
from typing import Tuple

# Locate the qentropy SSOT relative to this file: CLM/train/ -> <repo>/mirror/qmirror/seed
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(_HERE))
_QSEED_DIR = os.path.join(_REPO, "mirror", "qmirror", "seed")


def resolve_seed(fallback: int, label: str = "lane_p_torch_init") -> Tuple[int, dict]:
    """Return (seed, provenance) for the torch Lane-P trainer.

    QUANTUM-by-default / DETERMINISTIC-auxiliary via the qentropy SSOT. On any
    import/SSOT failure, returns (`fallback`, {...mode: 'hardcoded_fallback'...})
    so the trainer NEVER hard-depends on the SSOT and existing runs are preserved.

    `provenance` is a small dict suitable for logging into the run JSON:
        {entropy_mode, tier, label, seed, ssot}  (ssot=True when the SSOT supplied
        the seed; ssot=False on the fallback path).
    """
    try:
        if _QSEED_DIR not in sys.path:
            sys.path.insert(0, _QSEED_DIR)
        import qentropy  # noqa: E402  (lazy: only on the SSOT-available path)

        seed = qentropy.qentropy_seed(label)
        prov = qentropy.last_provenance()
        return seed, {
            "entropy_mode": qentropy.mode(),          # 'quantum' | 'deterministic'
            "tier": prov.get("tier"),                 # e.g. anu_committed / numpy_prng(187)
            "label": label,
            "seed": seed,
            "ssot": True,
            "summary": qentropy.summary(),
        }
    except Exception as e:  # noqa: BLE001 — SSOT absent/broken -> historical behavior
        return fallback, {
            "entropy_mode": "hardcoded_fallback",
            "tier": f"hardcoded(seed={fallback})",
            "label": label,
            "seed": fallback,
            "ssot": False,
            "fallback_reason": repr(e),
        }


def log_line(prov: dict) -> str:
    """One-line, log-friendly summary of the resolved entropy policy."""
    return (f"QENTROPY mode={prov.get('entropy_mode')} tier={prov.get('tier')} "
            f"seed={prov.get('seed')} ssot={prov.get('ssot')} label={prov.get('label')}")


if __name__ == "__main__":   # tiny both-mode demo (no torch needed)
    import json
    s, p = resolve_seed(42)
    print(log_line(p))
    print(json.dumps(p, indent=2))
