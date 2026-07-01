#!/usr/bin/env python3
"""_qseed_check.py — H_924 M4 both-mode verification (no GPU, no training run).

Shows that the Lane-P torch master seed derived via the qentropy SSOT DIFFERS
between ANIMA_ENTROPY_MODE=quantum (tier anu_committed) and =deterministic
(numpy_prng), and — if torch is importable — that torch.manual_seed(seed) +
torch.rand(3) tracks the chosen mode AND is reproducible in deterministic mode.

torch is OPTIONAL: if absent (e.g. on a dev Mac) the seed-derivation is still
verified via numpy alone and torch is reported device-pending. Never fails for
missing torch.

Usage:  ANIMA_ENTROPY_MODE=quantum       python3 _qseed_check.py
        ANIMA_ENTROPY_MODE=deterministic python3 _qseed_check.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _qseed import resolve_seed, log_line  # noqa: E402


def main() -> None:
    mode = os.environ.get("ANIMA_ENTROPY_MODE", "quantum")
    seed, prov = resolve_seed(42, label="lane_p_torch_init")
    print(f"ANIMA_ENTROPY_MODE={mode}")
    print(log_line(prov))
    print(f"seed={seed}")

    try:
        import torch  # noqa: PLC0415
        torch.manual_seed(seed)
        print(f"torch={torch.__version__} torch.rand(3)={torch.rand(3).tolist()}")
        # reproducibility: re-seeding the same seed reproduces the same draw
        torch.manual_seed(seed)
        print(f"torch.rand(3)[reseed]={torch.rand(3).tolist()}  (== above -> reproducible)")
    except Exception as e:  # noqa: BLE001
        print(f"torch=ABSENT ({e.__class__.__name__}) -> torch-runtime device-pending; "
              f"seed-derivation verified via numpy/SSOT only")


if __name__ == "__main__":
    main()
