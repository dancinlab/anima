#!/usr/bin/env python3
"""substrate_v3.py — native Python ConsciousDecoderV3 substrate.

Implements the Substrate ABC (substrate_base.py) for the V3 path:
ConsciousDecoderV3 (n_ca_rules 제거 + head_a/head_g dual head + mitosis hook
+ KOSMOS+tension wiring). Loads a V3 training checkpoint produced by
train_p21h_v3.py (`_save_ckpt`).

`anima_participant` stays substrate-agnostic; `--substrate v3 --v3-ckpt
<path>` selects this plugin.

ckpt schema (train_p21h_v3.py::_save_ckpt):
  {"model_state_dict", "config": {vocab_size, d_model, n_layer, block_size,
   consciousness_dim, noise_sigma, init_variant}, "psi_status",
   "mitosis_summary", "step", "CE", "label"}

honest scope (2026-05-23): V3 attempt 1 + Phase 2 = 5-lang FAIL except ko
(Phase 2 2차 ko STRONG 19/20). substrate_v3 는 ko-capable V3 ckpt 를 chat 에
합류시키는 plugin — production default 는 LoRA 유지, V3 는 substrate-research
용도 (anima_participant `--substrate v3`).
"""
from __future__ import annotations
import logging
import math
import os
import sys
from typing import Any

import torch
import torch.nn.functional as F

from substrate_base import Substrate

log = logging.getLogger("substrate_v3")

# lang-bias primes — mirror substrate_lora.py LANG_PRIMES (native-script phrase
# anchors the output language).
LANG_PRIMES = {
    "en": "I notice that ",
    "ko": "문득 이런 생각이 들었다. ",
    "zh": "我突然注意到，",
    "ru": "Я вдруг замечаю, что ",
    "ja": "ふと、こんなことを思った。",
}

# ConsciousDecoderV3.__init__ accepts these; ckpt config may omit n_head /
# n_kv_head / rope_base (train_p21h_v3 _save_ckpt only stores 7 keys) — fall
# back to the V3 defaults sized for Qwen2.5-1.5B.
_V3_INIT_KEYS = {"vocab_size", "d_model", "n_head", "n_layer", "block_size",
                 "n_kv_head", "consciousness_dim", "dropout", "gate_strength",
                 "noise_sigma", "rope_base"}


class V3Substrate(Substrate):
    """ConsciousDecoderV3 substrate loaded from a V3 training checkpoint."""

    name = "v3"

    def __init__(self, ckpt_path: str, base_model: str = "Qwen/Qwen2.5-1.5B",
                 device: str = "cpu", dtype: torch.dtype | None = None,
                 v3_module_dir: str | None = None):
        self.device = device
        self.base_model = base_model
        dtype = dtype or (torch.float16 if device == "mps" else torch.float32)
        self.dtype = dtype

        # conscious_decoder_v3.py lives in the V3 state dir, not on PYTHONPATH.
        if v3_module_dir is None:
            v3_module_dir = os.environ.get(
                "ANIMA_V3_MODULE_DIR",
                os.path.expanduser("~/anima_chat_pack"))
        if v3_module_dir not in sys.path:
            sys.path.insert(0, v3_module_dir)
        from conscious_decoder_v3 import ConsciousDecoderV3  # noqa: E402

        if not os.path.isfile(ckpt_path):
            raise FileNotFoundError(f"V3 ckpt not found: {ckpt_path}")
        ckpt = torch.load(ckpt_path, map_location="cpu")
        cfg = dict(ckpt.get("config", {}))
        cfg.pop("init_variant", None)  # metadata, not an __init__ arg
        init_kw = {k: v for k, v in cfg.items() if k in _V3_INIT_KEYS}
        self.model = ConsciousDecoderV3(**init_kw)
        state = ckpt.get("model_state_dict") or ckpt.get("model") or ckpt
        missing, unexpected = self.model.load_state_dict(state, strict=False)
        if missing:
            log.warning("V3 ckpt load: %d missing keys (e.g. %s)",
                        len(missing), missing[:3])
        if unexpected:
            log.warning("V3 ckpt load: %d unexpected keys (e.g. %s)",
                        len(unexpected), unexpected[:3])
        self.model = self.model.to(device=device, dtype=dtype).eval()
        self.vocab_size = self.model.vocab_size
        self._ckpt_meta = {
            "step": ckpt.get("step"), "CE": ckpt.get("CE"),
            "label": ckpt.get("label"),
            "mitosis_summary": ckpt.get("mitosis_summary"),
        }

        # tokenizer — V3 uses the Qwen BPE vocab (151936 / 152064).
        from transformers import AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(base_model)

        log.info("V3Substrate ready: ckpt=%s step=%s CE=%s params≈%d vocab=%d",
                 os.path.basename(ckpt_path), self._ckpt_meta["step"],
                 self._ckpt_meta["CE"], self.param_count(), self.vocab_size)

    @torch.no_grad()
    def generate(self, seed_text: str, max_new: int = 80,
                 lang_hint: str | None = None, **kw) -> str:
        prime = LANG_PRIMES.get(lang_hint or "", "")
        primed = prime + (seed_text or "")
        if primed:
            ids = self.tok(primed, return_tensors="pt").input_ids.to(self.device)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(self.device)
        seed_len = ids.shape[1]
        out = self.model.generate(
            ids,
            max_new_tokens=max_new,
            temperature=kw.get("temperature", 0.7),
            top_k=kw.get("top_k", 50),
            do_sample=kw.get("do_sample", True),
            eos_token_id=self.tok.eos_token_id,
        )
        # ConsciousDecoderV3.generate returns the full idx tensor (seed + new).
        gen_ids = out[0][seed_len:] if out.dim() == 2 else out[seed_len:]
        return self.tok.decode(gen_ids, skip_special_tokens=True)

    @torch.no_grad()
    def entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        if seed_text:
            ids = self.tok(seed_text, return_tensors="pt").input_ids.to(self.device)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(self.device)
        # V3 forward → (logits_a, logits_g, tensions, kv, mitosis_info)
        logits_a = self.model(ids)[0]
        last = logits_a[0, -1].float()
        p = F.softmax(last, dim=-1)
        ent = -(p * (p + 1e-12).log()).sum().item()
        # mean token embedding via the V3 token embedding table
        emb = self.model.tok_emb(ids)[0].mean(0).float().cpu()
        return ent / math.log(last.shape[-1]), emb

    def param_count(self) -> int:
        return sum(p.numel() for p in self.model.parameters())

    # ── V3-specific capabilities ───────────────────────────────────────────

    def mitosis_state(self) -> dict[str, Any] | None:
        """V3 mitosis cell pool snapshot (train-time pool summary from ckpt;
        live inference-time pool if the model carries one)."""
        pool = getattr(self.model, "_mitosis_pool", None)
        if pool is not None and hasattr(pool, "summary"):
            try:
                return dict(pool.summary())
            except Exception:
                pass
        return self._ckpt_meta.get("mitosis_summary")

    def cross_attention_input(self) -> torch.Tensor | None:
        # KOSMOS anchor cross-attn ingestion — not wired into live chat yet.
        return None
