"""pack.mocks — Mac-local mock runtimes for pre-arrival validation.

The MetaTF (BrainChip) SDK only installs on supported Linux hosts with the
AKD1000 driver present.  For Mac-local development before the Pi 5 +
AKD1000 Dev Kit arrives we expose a deterministic numpy-based mock that
mirrors the small slice of the ``akida`` API surface that the anima
adapters actually use.

Public API
----------
- :class:`MetaTFMock`       — top-level ``akida`` module replacement.
- :class:`MockModel`        — ``akida.Model`` mock with ``add``/``forward``/``fit``.
- :class:`MockHwDevice`     — ``akida.HwDevice`` mock (NSoC_v1 / AKD1000).
- :data:`MockDevice`        — back-compat alias for :class:`MockHwDevice`.
- :class:`MockLayers`       — ``akida.layers`` namespace mock (V2-style alias).
- :class:`MockAkidaUnsupervised` — edge-learning optimizer mock.
- :data:`metatf_mock`       — pre-instantiated singleton for direct import use.

The mock now mirrors the real BrainChip API surface verified against
``doc/`` (cached 2026-05-21).
"""

from __future__ import annotations

from .metatf_mock import (  # noqa: F401
    MetaTFMock,
    MockAkidaUnsupervised,
    MockHwDevice,
    MockLayers,
    MockModel,
    metatf_mock,
)

# Back-compat: old name was ``MockDevice``.
MockDevice = MockHwDevice

__all__ = [
    "MetaTFMock",
    "MockAkidaUnsupervised",
    "MockDevice",
    "MockHwDevice",
    "MockLayers",
    "MockModel",
    "metatf_mock",
]
