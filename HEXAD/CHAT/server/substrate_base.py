#!/usr/bin/env python3
"""substrate_base.py — pluggable substrate ABC for anima_participant.

Option C (shared core + substrate plugin) per HEXAD/CHAT/SUBSTRATE_PLUGIN.md.
motivation 8-factor + KOSMOS + lang-detect + broker connection 은 substrate 무관
(anima 의식 동역학); substrate 만 plugin.

Substrate impls:
- substrate_lora.py: vP21M (Qwen2.5-1.5B + LoRA r32 + mitosis aux)
- substrate_v3.py:   ConsciousDecoderV3 (pure HEXAD substrate)
- future: substrate_llama.py, substrate_hf_instruct.py, etc.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
import torch


class Substrate(ABC):
    """Pluggable substrate interface for anima participant.

    LoRA / V3 / future 가 이 ABC 충족하면 anima_participant 그대로 작동.

    Required attributes (subclass __init__ 에서 설정):
        name        : str  ("lora" | "v3" | "llama" etc)
        device      : str  ("mps" | "cuda" | "cpu")
        vocab_size  : int

    Optional capabilities (substrate 가 지원하면 override):
        mitosis_state() -> dict | None
        cross_attention_input() -> torch.Tensor | None
    """

    name: str
    device: str
    vocab_size: int

    @abstractmethod
    def generate(self, seed_text: str, max_new: int = 80,
                 lang_hint: str | None = None, **kw) -> str:
        """Free-form generation given seed text + optional lang prime.
        Returns decoded text (post seed_text — NOT including the seed).
        Used by Talker for emission.

        kw 가능: temperature, top_k, top_p, repetition_penalty, etc.
        """
        ...

    @abstractmethod
    @torch.no_grad()
    def entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        """Compute normalized entropy ∈ [0, 1] of next-token distribution +
        mean embedding of seed_text.
        Used by Thinker for 8-factor motivation computation:
        - ent_norm → phi → relevance + coherence (Law-70)
        - emb (mean over tokens, float cpu) → recent_embeds similarity for
          info_gap / originality factors

        Returns:
            (entropy_normalized [0..1], embed_tensor on cpu float32)
        """
        ...

    @abstractmethod
    def param_count(self) -> int:
        """Trainable + total params (for diagnostics / logging)."""
        ...

    # ─── optional substrate-specific capabilities ──────────────────────────

    def mitosis_state(self) -> dict[str, Any] | None:
        """Current mitosis cell pool snapshot (V3 only — LoRA returns None).
        Used by anima_participant's substrate-snapshot logging + KOSMOS lane wiring.

        Default: None (substrate has no mitosis hook).
        """
        return None

    def cross_attention_input(self) -> torch.Tensor | None:
        """Optional KOSMOS anchor input for cross-attention (V3 only).
        Returns None for LoRA — KOSMOS anchor 외부 ingestion 만 (cross-attn 없음).

        Default: None.
        """
        return None

    def __repr__(self) -> str:
        try:
            n = self.param_count()
            return f"{self.__class__.__name__}(name={self.name!r}, device={self.device!r}, params={n/1e9:.2f}B)"
        except Exception:
            return f"{self.__class__.__name__}(name={getattr(self,'name','?')!r})"
