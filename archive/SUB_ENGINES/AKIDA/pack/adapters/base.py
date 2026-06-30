"""Base class for all AKIDA aux engine adapters.

Concrete subclasses must implement :meth:`build_model`, :meth:`step`,
:meth:`selftest`.  :meth:`to_record` is provided here and mirrors the
``demiurge_brain_bridge.py`` record schema so downstream verifiers can consume
adapter snapshots uniformly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AkidaAdapter(ABC):
    """Common contract for every ``pack.adapters.*`` engine.

    Attributes
    ----------
    name : str
        Short kebab-case identifier (used in record keys + state paths).
    n_neurons : int
        Cell-pool size (default 8 per pack spec).
    seed : int
        RNG seed for deterministic init (default 42 — anima convention).
    _state : dict
        Mutable runtime state snapshot.  Subclasses are free to populate.
    _model : Any
        Built MetaTF model (or mock equivalent).  None until :meth:`build_model`
        is called.
    _built : bool
        True once :meth:`build_model` has run successfully.
    """

    name: str
    n_neurons: int = 8
    seed: int = 42
    _state: dict = field(default_factory=dict)
    _model: Optional[Any] = field(default=None, repr=False)
    _built: bool = field(default=False, repr=False)

    # -------------------------------------------------------- abstract API

    @abstractmethod
    def build_model(self) -> Any:
        """Build MetaTF model (or mock equivalent).  Idempotent."""

    @abstractmethod
    def step(self, input_data: Any) -> Any:
        """Run a single inference step.  Must be safe to call without args
        (``input_data=None`` should fall back to internal driver)."""

    @abstractmethod
    def selftest(self) -> dict:
        """Run ``F-AKIDA-<NAME>-1..5`` falsifier.

        Returns
        -------
        dict
            ``{"name", "passed", "failed", "details": [{"id", "ok", "msg"}, ...]}``.
        """

    # ----------------------------------------------------------- helpers

    def ensure_built(self) -> Any:
        """Build the model on first use; return it."""
        if not self._built:
            self._model = self.build_model()
            self._built = True
        return self._model

    def to_record(self) -> dict:
        """Emit demiurge-compatible record snapshot.

        Mirrors ``HEXAD/PHYSICS/.../demiurge_brain_bridge.py`` so the same
        VerifyProducer can consume adapter output without a new schema.

        Per the 2026-05-21 BrainChip survey, the record now also exposes the
        AKD1000 hardware-envelope estimates (``power_estimate_mW`` +
        ``npu_count_used`` + ``latency_us_estimate``) so downstream verifiers
        can sanity-check energy / NP-budget claims against datasheet ceilings
        (~1 W M.2 module, 20 NPU mesh, 300 MHz clock).
        """
        # Late import keeps base.py importable even if runtime stub is missing
        # (e.g. during package introspection).
        try:
            from ..runtime.metatf_runtime import get_runtime_info

            rt = get_runtime_info()
            backend = rt.get("backend", "unavailable")
        except Exception:  # noqa: BLE001
            backend = "unavailable"

        return {
            "interface": f"demiurge:brain:{self.name}-record",
            "producer": f"anima-akida-{self.name}-adapter",
            "backend": backend,  # "akida_hw" | "akida_mock" | "unavailable"
            "neurons": self.n_neurons,
            "seed": self.seed,
            "state_snapshot": dict(self._state),
            "measurement_gate": "GATE_OPEN",
            "absorbed": False,
            "consumer_target": "demiurge:brain:VerifyProducer",
            "scope_caveats": [
                "8-bit quantize",
                "MetaTF API version skew",
                "mock vs HW divergence",
            ],
            "gate_failures": [],
            # AKD1000 hardware-envelope estimates (real silicon = override these on Pi 5)
            "power_estimate_mW": float(self._estimate_power_mW()),
            "npu_count_used": int(self._estimate_npu_count()),
            "latency_us_estimate": float(self._estimate_latency_us()),
        }

    # -------------------------- AKD1000 envelope estimates (overridable) --
    #
    # Defaults below assume the smallest possible binary-FC adapter on a
    # single AKD1000 NP — adapters with heavier layer stacks (CNN,
    # multi-layer FC) override these.  See ``doc/akd1000_power_spec.md`` +
    # ``doc/akd1000_hardware_spec.md`` for the per-component datasheet
    # numbers driving the default formulas.

    # Per-event energy band (sub-mW class).  Marketing-quoted "~1 mW per
    # inference event" amortised; idle module = ~50 mW for the
    # NoC + ARM-M4 + LPDDR PHY even when no NP fires.
    _PER_EVENT_MW: float = 0.5
    _IDLE_FLOOR_MW: float = 50.0

    def _estimate_power_mW(self) -> float:  # noqa: N802
        """Estimate per-step mW (idle floor + per-event amortised)."""
        events = self._event_count_for_power()
        return float(self._IDLE_FLOOR_MW + events * self._PER_EVENT_MW)

    def _event_count_for_power(self) -> int:
        """Default = ``n_neurons`` worth of events per step.

        Adapters whose spike count differs (e.g. sparse-attention's top-k mask,
        motivation-gate's single fire bit) override this hook.
        """
        return int(self.n_neurons)

    def _estimate_npu_count(self) -> int:
        """Default = 1 NPU (smallest binary-FC adapter fits in a single NP).

        Larger / multi-layer adapters override.  AKD1000 mesh = 20 NPUs.
        """
        return 1

    def _estimate_latency_us(self) -> float:
        """Default = ``n_neurons / 300`` µs at 300 MHz, plus a 5 µs DMA floor.

        Real number requires ``model.statistics`` after silicon arrival; this
        is the bring-up estimate (≈ 1 cycle / neuron / NP at peak).
        """
        # 300 MHz ≈ 3.33 ns / cycle ≈ 300 cycles / µs
        cycles = max(int(self.n_neurons), 1)
        return float(5.0 + cycles / 300.0)

    # ------------------------------------------------------------- utility

    @staticmethod
    def _check(details: list, fid: str, ok: bool, msg: str = "") -> None:
        """Append a falsifier result to ``details`` (helper for selftest)."""
        details.append({"id": fid, "ok": bool(ok), "msg": msg})

    @staticmethod
    def _summarize(name: str, details: list) -> dict:
        passed = sum(1 for d in details if d["ok"])
        failed = len(details) - passed
        return {
            "name": name,
            "passed": passed,
            "failed": failed,
            "details": details,
        }


__all__ = ["AkidaAdapter"]
