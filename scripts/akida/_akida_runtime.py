"""Mirror of nexus/scripts/akida/_akida_runtime.py — kept local so anima runs
without needing the nexus repo on PYTHONPATH."""
from __future__ import annotations
import importlib, sys


def try_akida():
    try:
        ak = importlib.import_module("akida")
    except ImportError:
        return (None, False)
    try:
        devs = ak.devices()
        return (ak, len(devs) > 0)
    except Exception:
        return (ak, False)


def require_akida(need_device: bool = True):
    ak, dev = try_akida()
    if ak is None:
        print(
            "ERROR: 'akida' package missing. Install BrainChip Meta TF SDK:\n"
            "  pip install akida quantizeml cnn2snn",
            file=sys.stderr,
        )
        raise SystemExit(2)
    if need_device and not dev:
        print("ERROR: no AKD1000 device detected via akida.devices().", file=sys.stderr)
        raise SystemExit(3)
    return ak
