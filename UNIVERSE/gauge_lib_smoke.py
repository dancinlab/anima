#!/usr/bin/env python3
"""Smoke for gauge_lib.compute_inline_gauges (c2 verify-before-done).

Builds a TINY random byte model (ConvMoE-shaped dict output AND a ByteGPT-shaped
tuple output), calls compute_inline_gauges, asserts it returns the row dict with
all FIVE gauges + ce (incl mitosis_cells), writes ONE gauges.jsonl line, and confirms
the line round-trips. Pure CPU, $0, no network. MONITOR-ONLY — no loss, no backward
anywhere (incl mitosis_cells — substrate lane, NOT a generation gate, H_1201🔴).
"""
import json
import os
import sys
import tempfile

import torch
import torch.nn as nn

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from gauge_lib import compute_inline_gauges  # noqa: E402

V = 256


class TinyConvMoE(nn.Module):
    """ConvMoE-shaped: forward(x) -> dict with logits (B, V, T)."""

    def __init__(self, d=32):
        super().__init__()
        self.embed = nn.Embedding(V, d)
        self.readout = nn.Conv1d(d, V, kernel_size=1)

    def forward(self, x, targets=None):
        h = self.embed(x).transpose(1, 2)          # (B, d, T)
        logits = self.readout(h)                    # (B, V, T)
        return {"logits": logits}


class TinyByteGPT(nn.Module):
    """ByteGPT-shaped: forward(x) -> (logits (B, T, V), aux)."""

    def __init__(self, d=32):
        super().__init__()
        self.embed = nn.Embedding(V, d)
        self.head = nn.Linear(d, V)

    def forward(self, x, targets=None):
        return self.head(self.embed(x)), None       # (B, T, V), aux


def _check(model, label, corpus_path):
    torch.manual_seed(0)
    row = compute_inline_gauges(model, seeds=42, corpus_index=corpus_path,
                                ce=1.234, step=400, torch=torch, max_new=24)
    print(f"[{label}] returned dict: {json.dumps(row)}")
    for k in ("step", "ce", "g1_composed_distinct", "g2_novelty_rate",
              "g6_count", "g6_jaccard", "phi_proxy", "mitosis_cells"):
        assert k in row, f"missing key {k} in row"
    assert row["step"] == 400
    assert row["ce"] == 1.234
    assert isinstance(row["g1_composed_distinct"], int)
    assert isinstance(row["g6_count"], int)
    # phi_proxy must be a real number (cheap proxy, NOT IIT4)
    assert isinstance(row["phi_proxy"], (int, float))
    # mitosis_cells must be an int >= 1 (substrate lane, NOT a generation gate)
    assert isinstance(row["mitosis_cells"], int) and row["mitosis_cells"] >= 1, \
        f"mitosis_cells must be int>=1, got {row['mitosis_cells']!r}"
    return row


def main():
    tmpdir = tempfile.mkdtemp(prefix="gauge_smoke_")
    corpus_path = os.path.join(tmpdir, "corpus.txt")
    with open(corpus_path, "w") as f:
        f.write("consciousness arises from cells and memory composes meaning. "
                "the engine dreams when alone in silence.\n" * 20)
    gauges_path = os.path.join(tmpdir, "gauges.jsonl")

    # Build tiny random byte models (both output shapes).
    conv = TinyConvMoE()
    gpt = TinyByteGPT()

    row_conv = _check(conv, "ConvMoE-dict", corpus_path)
    row_gpt = _check(gpt, "ByteGPT-tuple", corpus_path)

    # Emulate the trainer's gauge_tick: append ONE line and round-trip it.
    with open(gauges_path, "a") as gf:
        gf.write(json.dumps(row_conv) + "\n")
    with open(gauges_path) as gf:
        lines = gf.read().strip().splitlines()
    assert len(lines) == 1, f"expected 1 gauges.jsonl line, got {len(lines)}"
    parsed = json.loads(lines[0])
    assert parsed["g1_composed_distinct"] == row_conv["g1_composed_distinct"]

    # phi_proxy label guard: the key MUST be 'phi_proxy', never 'phi' (a_phi_iit4_tool).
    assert "phi_proxy" in parsed and "phi" not in [k for k in parsed if k == "phi"]

    print(f"\ngauges.jsonl ({gauges_path}) line:\n  {lines[0]}")
    print("\nSMOKE PASS — compute_inline_gauges returns the 5-gauge+ce dict (incl "
          "mitosis_cells) and one gauges.jsonl line round-trips (both ConvMoE-dict and "
          "ByteGPT-tuple model shapes). MONITOR-ONLY: no loss / no backward in gauge_lib "
          "(mitosis_cells = substrate lane, NOT a generation gate · H_1201🔴).")


if __name__ == "__main__":
    main()
