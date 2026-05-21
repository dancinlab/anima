"""Pi 5 host orchestrator.

Coordinates a bundle of :class:`AkidaAdapter` instances on the Pi 5 host:
- ticks each adapter once per ``step()`` (round-robin),
- routes adapter output through a motivation gate,
- writes emit candidates to the :class:`AuditBuffer`,
- periodically persists buffer + per-adapter state to eMMC.

The orchestrator deliberately stays small (~250 LoC) and synchronous — Akida
HW itself is event-driven and the Pi 5 is a single-process supervisor.  Higher
throughput modes (per-adapter threads, async I/O) can layer on top without
breaking this contract.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any, Callable, Iterable, Optional

from .audit_buffer import AuditBuffer
from .metatf_runtime import get_runtime_info


# Sentinel type for adapters — we accept anything that ducks like
# AkidaAdapter (has .name, .step, .to_record).  Avoids a hard import cycle.
AdapterLike = Any


@dataclass
class OrchestratorConfig:
    """Tunable orchestrator parameters."""

    audit_capacity: int = 8
    audit_path: Optional[str] = None  # default → AuditBuffer default
    state_dir: str = "~/.cache/anima-akida/state"
    persist_every_n_steps: int = 16
    motivation_threshold: float = 0.5
    max_steps: Optional[int] = None  # None = run until stop()
    tick_sleep_s: float = 0.0  # 0 = busy-loop; >0 throttles


class Pi5Orchestrator:
    """Drive a set of adapters on the Pi 5 host.

    Parameters
    ----------
    adapters : Iterable[AkidaAdapter]
        The bundle to drive.  All must expose ``.name``, ``.step(input)``,
        ``.to_record()``.
    config : OrchestratorConfig, optional
        Tunables; defaults are spec-conformant.
    input_fn : Callable[[str, int], Any], optional
        Per-step input provider, called as ``input_fn(adapter_name, step)``.
        Default supplies ``None`` (adapters fall back to their own driver).
    motivation_fn : Callable[[Any], float], optional
        Maps adapter output → motivation score in [0, 1].  Default uses a
        simple ``float(getattr(out, "motivation", 0.0))`` heuristic.
    """

    def __init__(
        self,
        adapters: Iterable[AdapterLike],
        config: Optional[OrchestratorConfig] = None,
        input_fn: Optional[Callable[[str, int], Any]] = None,
        motivation_fn: Optional[Callable[[Any], float]] = None,
    ) -> None:
        self.adapters: list[AdapterLike] = list(adapters)
        if not self.adapters:
            raise ValueError("Pi5Orchestrator needs at least one adapter")
        self.config = config or OrchestratorConfig()
        self.input_fn = input_fn or (lambda _name, _step: None)
        self.motivation_fn = motivation_fn or _default_motivation
        self.audit = AuditBuffer(
            capacity=self.config.audit_capacity,
            path=self.config.audit_path,
        )
        self.step_count = 0
        self._stop = False
        self._emit_count = 0
        self._state_dir = os.path.expanduser(self.config.state_dir)

    # ---------------------------------------------------------------- API

    def step(self) -> list[dict]:
        """Run one orchestrator tick across all adapters.

        Returns a list of emit records produced this tick (possibly empty).
        """
        emitted: list[dict] = []
        for ad in self.adapters:
            try:
                inp = self.input_fn(ad.name, self.step_count)
                out = ad.step(inp)
            except Exception as exc:  # noqa: BLE001
                # Surface as audit entry — never crash the whole orchestrator
                # on a single adapter fault.
                err_rec = {
                    "kind": "adapter_error",
                    "adapter": getattr(ad, "name", "<unknown>"),
                    "step": self.step_count,
                    "error": repr(exc),
                }
                self.audit.append(err_rec)
                emitted.append(err_rec)
                continue
            mot = self.motivation_fn(out)
            if mot >= self.config.motivation_threshold:
                rec = ad.to_record()
                rec.update(
                    {
                        "kind": "emit",
                        "step": self.step_count,
                        "motivation": float(mot),
                        "ts": time.time(),
                    }
                )
                self.audit.append(rec)
                emitted.append(rec)
                self._emit_count += 1
        self.step_count += 1

        if (
            self.config.persist_every_n_steps > 0
            and self.step_count % self.config.persist_every_n_steps == 0
        ):
            self.persist()

        if self.config.tick_sleep_s > 0:
            time.sleep(self.config.tick_sleep_s)
        return emitted

    def run(self) -> dict:
        """Run until :meth:`stop` or ``max_steps`` reached.

        Returns a summary dict (step_count, emit_count, runtime_info).
        """
        self._stop = False
        while not self._stop:
            if (
                self.config.max_steps is not None
                and self.step_count >= self.config.max_steps
            ):
                break
            self.step()
        self.persist()  # final flush
        return self.summary()

    def stop(self) -> None:
        self._stop = True

    # --------------------------------------------------------- persistence

    def persist(self) -> dict:
        """Flush audit buffer + per-adapter state snapshots to disk."""
        os.makedirs(self._state_dir, exist_ok=True)
        audit_path = self.audit.dump()
        adapter_paths: dict[str, str] = {}
        for ad in self.adapters:
            try:
                snap = ad.to_record()
            except Exception as exc:  # noqa: BLE001
                snap = {"error": repr(exc), "adapter": getattr(ad, "name", "?")}
            p = os.path.join(self._state_dir, f"{ad.name}.state.json")
            with open(p, "w", encoding="utf-8") as fh:
                json.dump(snap, fh, ensure_ascii=False, indent=2, default=str)
            adapter_paths[ad.name] = p
        meta_path = os.path.join(self._state_dir, "orchestrator.meta.json")
        meta = {
            "step_count": self.step_count,
            "emit_count": self._emit_count,
            "audit_path": audit_path,
            "adapter_paths": adapter_paths,
            "runtime": get_runtime_info(),
            "ts": time.time(),
        }
        with open(meta_path, "w", encoding="utf-8") as fh:
            json.dump(meta, fh, ensure_ascii=False, indent=2, default=str)
        return meta

    # ---------------------------------------------------------- diagnostics

    def summary(self) -> dict:
        return {
            "step_count": self.step_count,
            "emit_count": self._emit_count,
            "audit_size": len(self.audit),
            "adapters": [ad.name for ad in self.adapters],
            "runtime": get_runtime_info(),
        }


def _default_motivation(out: Any) -> float:
    """Best-effort scalar extraction for motivation gating."""
    if out is None:
        return 0.0
    if isinstance(out, (int, float)):
        return float(out)
    if isinstance(out, dict):
        for k in ("motivation", "score", "spike_rate", "r", "fire"):
            if k in out:
                try:
                    return float(out[k])
                except (TypeError, ValueError):
                    continue
        return 0.0
    # numpy arrays / tensors: mean magnitude
    try:
        import numpy as np

        arr = np.asarray(out)
        if arr.size == 0:
            return 0.0
        return float(np.mean(np.abs(arr)))
    except Exception:  # noqa: BLE001
        return 0.0


__all__ = [
    "OrchestratorConfig",
    "Pi5Orchestrator",
]
