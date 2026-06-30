"""pack.runtime — MetaTF wrapper + Pi 5 orchestrator + audit ring buffer.

Modules
-------
- :mod:`pack.runtime.metatf_runtime` — MetaTF (BrainChip) wrapper.  Imports the
  real ``akida`` SDK when available; falls back to ``pack.mocks.metatf_mock``
  for Mac-local development pre-arrival.
- :mod:`pack.runtime.audit_buffer`   — 8-deep LRU ring buffer with eMMC
  persistence helpers (``dump`` / ``load``).
- :mod:`pack.runtime.pi5_orchestrator` — Pi 5 host orchestrator that drives a
  bundle of :class:`AkidaAdapter` instances, manages audit and emit cadence.
"""

from __future__ import annotations

from .metatf_runtime import (  # noqa: F401  (re-export)
    get_runtime,
    get_runtime_info,
    init_runtime,
)
from .audit_buffer import AuditBuffer  # noqa: F401
from .pi5_orchestrator import OrchestratorConfig, Pi5Orchestrator  # noqa: F401

__all__ = [
    "get_runtime",
    "get_runtime_info",
    "init_runtime",
    "AuditBuffer",
    "Pi5Orchestrator",
    "OrchestratorConfig",
]
