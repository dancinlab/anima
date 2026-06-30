"""pack.adapters — substrate → BrainChip Akida adapter family.

Each adapter is a thin layer that maps an anima-physics substrate (SNN /
Izhikevich / Kuramoto / memristor / sparse-attention / lm-head / motivation /
θ-γ / EEG / spontaneous) onto a MetaTF model that can either:

- run on real AKD1000 silicon via :mod:`pack.runtime.metatf_runtime` (HW path),
  or
- be exercised against :mod:`pack.mocks.metatf_mock` for Mac-local validation
  (mock path).

All concrete adapters inherit from :class:`pack.adapters.base.AkidaAdapter`
and implement :meth:`build_model`, :meth:`step`, :meth:`selftest`.
"""

from __future__ import annotations

from .base import AkidaAdapter  # noqa: F401
from .snn_lif import SNNLifAdapter  # noqa: F401
from .izhikevich import IzhikevichAdapter  # noqa: F401
from .kuramoto import KuramotoAdapter  # noqa: F401
from .memristor_hybrid import MemristorHybridAdapter  # noqa: F401
from .sparse_attention import SparseAttentionAdapter  # noqa: F401
from .spike_tier_lm_head import SpikeTierLMHeadAdapter  # noqa: F401
from .motivation_gate import MotivationGateAdapter  # noqa: F401
from .theta_gamma import ThetaGammaAdapter  # noqa: F401
from .eeg_pattern import EEGPatternAdapter  # noqa: F401
from .spontaneous_gate import SpontaneousGateAdapter  # noqa: F401

__all__ = [
    "AkidaAdapter",
    "SNNLifAdapter",
    "IzhikevichAdapter",
    "KuramotoAdapter",
    "MemristorHybridAdapter",
    "SparseAttentionAdapter",
    "SpikeTierLMHeadAdapter",
    "MotivationGateAdapter",
    "ThetaGammaAdapter",
    "EEGPatternAdapter",
    "SpontaneousGateAdapter",
    "ALL_ADAPTER_CLASSES",
]

ALL_ADAPTER_CLASSES = (
    SNNLifAdapter,
    IzhikevichAdapter,
    KuramotoAdapter,
    MemristorHybridAdapter,
    SparseAttentionAdapter,
    SpikeTierLMHeadAdapter,
    MotivationGateAdapter,
    ThetaGammaAdapter,
    EEGPatternAdapter,
    SpontaneousGateAdapter,
)
