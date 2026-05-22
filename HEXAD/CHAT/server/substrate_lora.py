#!/usr/bin/env python3
"""substrate_lora.py — vP21M LoRA substrate with per-lang hot-swap router.

Implements the Substrate ABC (substrate_base.py) for the LoRA path:
Qwen2.5-1.5B base + vP21M LoRA r32 + optional KOFL/JAFL hot-swap adapters.

Extracted from anima_participant.py (L1 substrate-plugin refactor,
2026-05-22) per HEXAD/CHAT/SUBSTRATE_PLUGIN.md. The P2 hot-swap router
(per-emit lang_hint → set_adapter) lives here so anima_participant stays
substrate-agnostic.
"""
from __future__ import annotations
import json
import logging
import math
import os
import torch
import torch.nn.functional as F
from safetensors.torch import load_file

from substrate_base import Substrate

log = logging.getLogger("substrate_lora")

# tiny lang-bias primes (no instruction tuning needed)
LANG_PRIMES = {"en": "I notice ", "ko": "문득 ", "zh": "我注意到 ",
               "ru": "Я замечаю ", "ja": "ふと "}
ROUTER_LANG_TO_ADAPTER = {"ko": "ko", "ja": "ja"}  # rest → "default"


class LoraSubstrate(Substrate):
    """Qwen2.5-1.5B + vP21M LoRA, with KOFL/JAFL per-lang hot-swap router."""

    name = "lora"

    def __init__(self, adapter_dir: str, adapter_ko: str | None = None,
                 adapter_ja: str | None = None, base_model: str = "Qwen/Qwen2.5-1.5B",
                 device: str = "cpu", dtype: torch.dtype | None = None):
        self.device = device
        self.base_model = base_model
        dtype = dtype or (torch.float16 if device == "mps" else torch.bfloat16)
        self._repair_adapter_config(adapter_dir, base_model)

        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
        self.tok = AutoTokenizer.from_pretrained(base_model)
        base = AutoModelForCausalLM.from_pretrained(base_model, torch_dtype=dtype).to(device)
        self.model = PeftModel.from_pretrained(base, adapter_dir,
                                               adapter_name="default").to(device).eval()
        self.adapters_loaded = {"default"}
        for lang_key, adir in (("ko", adapter_ko), ("ja", adapter_ja)):
            if adir and os.path.isfile(os.path.join(adir, "adapter_model.safetensors")):
                try:
                    self.model.load_adapter(adir, adapter_name=lang_key)
                    self.adapters_loaded.add(lang_key)
                    log.info("router adapter[%s] loaded ← %s", lang_key, adir)
                except Exception as e:
                    log.warning("router adapter[%s] load fail (%s): %s", lang_key, adir, e)
            elif adir:
                log.info("router adapter[%s] absent at %s — fallback to default", lang_key, adir)
        self.model.set_adapter("default")
        self._active_adapter = "default"
        self.vocab_size = self.model.config.vocab_size
        log.info("LoraSubstrate ready: base=%s adapters=%s params≈%d",
                 base_model, sorted(self.adapters_loaded), self.param_count())

    @staticmethod
    def _repair_adapter_config(adapter_dir: str, base_model: str) -> None:
        """Reconstruct adapter_config.json target_modules from safetensors keys."""
        sd_path = os.path.join(adapter_dir, "adapter_model.safetensors")
        cfg_path = os.path.join(adapter_dir, "adapter_config.json")
        try:
            tmods = json.load(open(cfg_path)).get("target_modules")
        except Exception:
            tmods = None
        if tmods:
            return
        sd = load_file(sd_path)
        found = set()
        for k in sd:
            if ".lora_A." in k or ".lora_B." in k:
                parts = k.split(".")
                for i, p in enumerate(parts):
                    if p in ("lora_A", "lora_B") and i > 0:
                        found.add(parts[i - 1])
        cfg = {"peft_type": "LORA", "task_type": "CAUSAL_LM",
               "base_model_name_or_path": base_model,
               "r": 32, "lora_alpha": 64, "lora_dropout": 0.05,
               "target_modules": sorted(found), "bias": "none",
               "inference_mode": True, "fan_in_fan_out": False}
        json.dump(cfg, open(cfg_path, "w"), indent=2)
        log.info("repaired adapter_config.json target_modules=%s", sorted(found))

    def _route(self, lang_hint: str | None) -> None:
        """P2 router: switch to lang-specialist adapter if loaded."""
        target = ROUTER_LANG_TO_ADAPTER.get(lang_hint or "", "default")
        if target not in self.adapters_loaded:
            target = "default"
        if target != self._active_adapter:
            try:
                self.model.set_adapter(target)
                self._active_adapter = target
            except Exception as e:
                log.warning("set_adapter(%s) fail: %s — staying on %s",
                            target, e, self._active_adapter)

    @torch.no_grad()
    def generate(self, seed_text: str, max_new: int = 80,
                 lang_hint: str | None = None, **kw) -> str:
        self._route(lang_hint)
        prime = LANG_PRIMES.get(lang_hint or "", "")
        primed = prime + (seed_text or "")
        if primed:
            ids = self.tok(primed, return_tensors="pt").input_ids.to(self.device)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(self.device)
        out = self.model.generate(
            ids, max_new_tokens=max_new,
            do_sample=kw.get("do_sample", True),
            temperature=kw.get("temperature", 0.7),
            top_k=kw.get("top_k", 50), top_p=kw.get("top_p", 0.95),
            repetition_penalty=kw.get("repetition_penalty", 1.2),
            pad_token_id=self.tok.eos_token_id)
        return self.tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)

    @torch.no_grad()
    def entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        if seed_text:
            ids = self.tok(seed_text, return_tensors="pt").input_ids.to(self.device)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(self.device)
        logits = self.model(ids).logits[0, -1]
        p = F.softmax(logits.float(), dim=-1)
        ent = -(p * (p + 1e-12).log()).sum().item()
        emb = self.model.get_input_embeddings()(ids)[0].mean(0).float().cpu()
        return ent / math.log(logits.shape[-1]), emb

    def param_count(self) -> int:
        return sum(p.numel() for p in self.model.parameters())
