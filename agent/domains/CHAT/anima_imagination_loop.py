"""Emit-free participant rehearsal backed by the canonical Python engine."""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any

_CORE = Path(__file__).resolve().parents[3] / "core"
if str(_CORE) not in sys.path:
    sys.path.insert(0, str(_CORE))

from closure_ladder import features
from engine_cli import (
    engine_config_default,
    vadapt_field_cells,
    vadapt_field_new,
    vadapt_field_step,
)
from imagination_replay import (
    ir_mitosis_tick_during_replay,
    ir_replay_tick,
    ir_select_snapshots,
)
from wake_memory import mem_init, mem_push_ctx


def _max_cells() -> int:
    raw = os.environ.get("ANIMA_IMAGINATION_MAX_CELLS", "128")
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError("ANIMA_IMAGINATION_MAX_CELLS must be an integer") from exc
    if value < 1:
        raise ValueError("ANIMA_IMAGINATION_MAX_CELLS must be positive")
    return value


class ImaginationLoop:
    """Keep participant rehearsal state separate from its external mouth."""

    def __init__(self, max_cells: int | None = None) -> None:
        self.memory = mem_init()
        self.field = None
        self.config = engine_config_default()
        self.max_cells = _max_cells() if max_cells is None else int(max_cells)
        if self.max_cells < 1:
            raise ValueError("max_cells must be positive")
        self.tick_id = 0
        self.total_replays = 0
        self.total_splits = 0

    def observe(self, text: str) -> None:
        """Add environmental context to the canonical wake-memory ring."""
        if not isinstance(text, str):
            raise TypeError("imagination context must be text")
        if not text:
            return
        tokens = list(text.encode("utf-8", "surrogateescape"))
        self.memory = mem_push_ctx(self.memory, tokens)

    def tick(self) -> dict[str, Any] | None:
        """Run one internal replay and VAdaptField step; never emit text."""
        snapshots = ir_select_snapshots(self.memory, self.tick_id, 1)
        if not snapshots:
            return None
        snapshot = snapshots[-1]
        replay = ir_replay_tick(snapshot)
        if replay["emit_count"] != 0:
            raise RuntimeError("imagination replay violated the emit-free invariant")

        vector = features(bytes(replay["ctx_tokens"]), dim=8)
        seeded = self.field is None
        cells_before = 0 if seeded else vadapt_field_cells(self.field)
        if self.field is None:
            self.field = vadapt_field_new(vector, self.max_cells)
        else:
            self.field = vadapt_field_step(self.field, vector, self.config)
        cells_after = vadapt_field_cells(self.field)
        mitosis = ir_mitosis_tick_during_replay(
            {"count": cells_after}, snapshot
        )

        self.tick_id += 1
        self.total_replays += 1
        split_count = 0 if seeded else max(0, cells_after - cells_before)
        self.total_splits += split_count
        return {
            "tick_id": self.tick_id - 1,
            "emit_count": replay["emit_count"],
            "rehearsal_kind": replay["rehearsal_kind"],
            "cells_before": cells_before,
            "cells_after": cells_after,
            "split_count": split_count,
            "mitosis_density": mitosis["mitosis_density"],
        }
