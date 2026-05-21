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
- :class:`MockDevice`       — ``akida.devices()[i]`` mock with ``program``.
- :class:`MockLayers`       — ``akida.layers`` namespace mock.
- :data:`metatf_mock`       — pre-instantiated singleton for direct import use.
"""

from __future__ import annotations

from .metatf_mock import (  # noqa: F401
    MetaTFMock,
    MockDevice,
    MockLayers,
    MockModel,
    metatf_mock,
)

__all__ = [
    "MetaTFMock",
    "MockDevice",
    "MockLayers",
    "MockModel",
    "metatf_mock",
]
