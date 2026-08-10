#!/usr/bin/env python3
"""Canonical CLMConvMoE substrate for the existing anima chat participant."""
from __future__ import annotations

import logging
import math
import pathlib
import sys
from typing import Any

import numpy as np
import torch

from substrate_base import Substrate

log = logging.getLogger("substrate_clm")

_REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
_CORE_DIR = _REPO_ROOT / "core"
if str(_CORE_DIR) not in sys.path:
    sys.path.insert(0, str(_CORE_DIR))

import decode as _decode  # noqa: E402


def _tensor_elements(value: Any, seen: set[int]) -> int:
    """Count each loaded tensor once for participant diagnostics."""
    if isinstance(value, dict):
        return sum(_tensor_elements(v, seen) for v in value.values())
    if isinstance(value, (list, tuple)):
        return sum(_tensor_elements(v, seen) for v in value)
    if hasattr(value, "shape") and hasattr(value, "size"):
        ident = id(value)
        if ident in seen:
            return 0
        seen.add(ident)
        return int(value.size)
    return 0


def _websocket_text(text: str) -> str:
    """Map arbitrary byte-mouth output to valid Unicode for a WebSocket text frame."""
    return text.encode("utf-8", "surrogateescape").decode("utf-8", "replace")


class CLMSubstrate(Substrate):
    """Serve a serialized `.clm` through the existing canonical decode runtime."""

    name = "clm"

    def __init__(self, ckpt_path: str):
        raw_path = str(ckpt_path or "").strip()
        if not raw_path:
            raise ValueError("ANIMA_CLM_CKPT is required for --substrate clm")
        path = pathlib.Path(raw_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"CLM checkpoint not found: {path}")
        if not _decode.clm_decodable(str(path)):
            raise ValueError(f"checkpoint is not a decodable CLMConvMoE .clm: {path}")

        self.ckpt_path = str(path)
        self.W = _decode.clm_load_weights(self.ckpt_path)
        self.vocab_size = int(self.W["V"])
        device = _decode.gpu_status()
        self.device = "cuda" if device.get("cuda") else "cpu"
        self._param_count = _tensor_elements(self.W, set())
        log.info(
            "CLMSubstrate ready: ckpt=%s device=%s params=%d vocab=%d",
            path.name, self.device, self._param_count, self.vocab_size,
        )

    def generate(self, seed_text: str, max_new: int = 80,
                 lang_hint: str | None = None, **kw) -> str:
        del lang_hint, kw
        if not isinstance(seed_text, str):
            raise TypeError("seed_text must be str")
        if isinstance(max_new, bool) or not isinstance(max_new, int) or max_new < 0:
            raise ValueError("max_new must be a non-negative integer")
        if max_new == 0:
            return ""
        result = _decode.clm_decode_argmax(self.ckpt_path, seed_text, max_new)
        if not result.get("ok"):
            raise RuntimeError("canonical CLM decode failed")
        return _websocket_text(str(result.get("text", "")))

    @torch.no_grad()
    def entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        if not isinstance(seed_text, str):
            raise TypeError("seed_text must be str")
        tok = _decode._seed_to_tok(seed_text, _decode.CLM_DECODE_WINDOW)
        hidden, logits = _decode.clm_forward_hidden_logits(
            self.W, tok, _decode.CLM_DECODE_WINDOW)
        row = np.asarray(logits[-1], dtype=np.float64)
        row = row - float(row.max())
        probs = np.exp(row)
        probs = probs / float(probs.sum())
        entropy = -float(np.sum(probs * np.log(probs + np.finfo(np.float64).tiny)))
        normalized = entropy / math.log(float(self.vocab_size))
        embedding = torch.from_numpy(
            np.asarray(hidden, dtype=np.float32).mean(axis=0).copy())
        return max(0.0, min(1.0, normalized)), embedding

    def param_count(self) -> int:
        return self._param_count
