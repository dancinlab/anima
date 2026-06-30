"""pack.falsifiers — F-AKIDA-* aggregate runners.

Each adapter exposes its own ``selftest()`` (which runs the local
``F-AKIDA-<NAME>-1..5`` falsifiers).  This sub-package only contains the
*aggregator* that walks every registered adapter, runs ``selftest()`` on
each, and prints / returns a single PASS/FAIL table.
"""

from __future__ import annotations

from .run_all import run_all_adapters  # noqa: F401

__all__ = ["run_all_adapters"]
