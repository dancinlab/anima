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
import generator as _generator  # noqa: E402


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
    """Serve a serialized `.clm` or ByteGPT `.bin` through one mouth runtime.

    The historical class/CLI name remains for compatibility; checkpoint header
    sniffing, chat framing and decode selection are owned by ``core.generator``.
    """

    name = "clm"
    chat_max_new = _generator.CHAT_MAX_NEW_BYTES

    def __init__(self, ckpt_path: str):
        raw_path = str(ckpt_path or "").strip()
        if not raw_path:
            raise ValueError("ANIMA_CLM_CKPT is required for --substrate clm")
        path = pathlib.Path(raw_path).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError(f"CLM checkpoint not found: {path}")
        kind = _generator.gen_mouth_kind(str(path))
        if kind not in {"clm", "bytegpt"}:
            raise ValueError(f"checkpoint is not a decodable .clm or ByteGPT .bin: {path}")

        self.ckpt_path = str(path)
        self.kind = kind
        self.name = kind
        self.W = (_decode.clm_load_weights(self.ckpt_path) if kind == "clm"
                  else _decode.bg_load(self.ckpt_path))
        self.vocab_size = int(self.W["V"] if kind == "clm" else self.W["vocab"])
        device = _decode.gpu_status()
        self.device = "cuda" if device.get("cuda") else "cpu"
        self._param_count = _tensor_elements(self.W, set())
        log.info(
            "canonical mouth substrate ready: kind=%s ckpt=%s device=%s params=%d vocab=%d",
            kind, path.name, self.device, self._param_count, self.vocab_size,
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
        seed = _generator.gen_chat_seed("", seed_text)
        result = _generator.gen_loaded_chat(self.kind, self.W, seed, max_new)
        return _websocket_text(str(result.get("text", "")))

    @torch.no_grad()
    def entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        if not isinstance(seed_text, str):
            raise TypeError("seed_text must be str")
        if self.kind == "clm":
            tok = _decode._seed_to_tok(seed_text, _decode.CLM_DECODE_WINDOW)
            hidden, logits = _decode.clm_forward_hidden_logits(
                self.W, tok, _decode.CLM_DECODE_WINDOW)
            row = np.asarray(logits[-1], dtype=np.float64)
            representation = np.asarray(hidden, dtype=np.float32).mean(axis=0)
        else:
            ids = list(seed_text.encode("utf-8", "surrogateescape")) or [32]
            ids = ids[-int(self.W["block"]):]
            row = np.asarray(
                _decode.bg_forward_last_W(self.W, ids, len(ids)), dtype=np.float64)
            representation = np.asarray(
                _decode.bg_forward_last_hidden(self.W, ids, len(ids)), dtype=np.float32)
        row = row - float(row.max())
        probs = np.exp(row)
        probs = probs / float(probs.sum())
        entropy = -float(np.sum(probs * np.log(probs + np.finfo(np.float64).tiny)))
        normalized = entropy / math.log(float(self.vocab_size))
        embedding = torch.from_numpy(representation.copy())
        return max(0.0, min(1.0, normalized)), embedding

    def param_count(self) -> int:
        return self._param_count
