#!/usr/bin/env python3
"""H_1058 daemon runner — installs the dtype/lean-load patch BEFORE mounting so a big ckpt
(the 3B) loads fp32-lean (ANIMA_DTYPE=float32) instead of fp64 (24.6GB -> swap-wedge on a
32GB pod). Thin wrapper around cli/chat.py::anima_consciousness_mode; the decision-trace side
channel is driven by ANIMA_TICKS / ANIMA_DECISION_TRACE env (unchanged, byte-safe).

For the UNLOADED generator-swap arm pass --clm "" (chat mounts a no-op backend).

Usage: ANIMA_TICKS=800 ANIMA_DECISION_TRACE=trace.jsonl [ANIMA_DTYPE=float32] \
       PYTHONPATH=cli:core python3 run_daemon.py <ckpt.clm>
"""
import os
import sys


def _main():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    # patch decode's weight loader to the requested precision/lean profile BEFORE chat imports it
    if os.environ.get("ANIMA_DTYPE"):
        import dtype_patch
        print("[run_daemon] dtype:", dtype_patch.install(require_headroom=True), flush=True)
    import chat
    ckpt = sys.argv[1] if len(sys.argv) > 1 else ""
    return chat.anima_consciousness_mode(ckpt) or 0


if __name__ == "__main__":
    sys.exit(_main())
