#!/usr/bin/env python3
"""Hugging Face causal-LM substrate with optional LoRA hot-swap adapters.

Implements the existing Substrate ABC for an HF chat model with optional
vP21M and language-specific LoRA adapters.

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

LANG_PRIMES = {
    "en": "I notice that ",
    "ko": "문득 이런 생각이 들었다. ",
    "zh": "我突然注意到，",
    "ru": "Я вдруг замечаю, что ",
    "ja": "ふと、こんなことを思った。",
}
ROUTER_LANG_TO_ADAPTER = {"ko": "ko", "ja": "ja", "zh": "zh", "ru": "ru"}  # rest → "default"

_SCRIPT_RANGES = {
    "ko": [(0xAC00, 0xD7AF)],
    "ja": [(0x3040, 0x30FF)],
    "zh": [(0x4E00, 0x9FFF)],
    "ru": [(0x0400, 0x04FF)],
}


def _seed_matches_lang(seed_text: str, lang_hint: str | None) -> bool:
    if not seed_text or not lang_hint or lang_hint == "en":
        return True
    ranges = _SCRIPT_RANGES.get(lang_hint)
    if not ranges:
        return True
    native = sum(1 for char in seed_text
                 if any(low <= ord(char) <= high for low, high in ranges))
    letters = sum(1 for char in seed_text if char.isalpha())
    return letters == 0 or native / max(letters, 1) >= 0.3


_SYSTEM_PROMPT = os.environ.get(
    "ANIMA_SYSTEM_PROMPT", "You are anima. Reply in the user's language.")


class LoraSubstrate(Substrate):
    """Canonical HF chat model, optionally extended by LoRA adapters."""

    name = "lora"

    def __init__(self, adapter_dir: str, adapter_ko: str | None = None,
                 adapter_ja: str | None = None, adapter_zh: str | None = None,
                 adapter_ru: str | None = None,
                 base_model: str = "Qwen/Qwen2.5-1.5B",
                 device: str = "cpu", dtype: torch.dtype | None = None):
        self.device = device
        self.base_model = base_model
        dtype = dtype or (torch.float16 if device == "mps" else torch.bfloat16)
        from transformers import AutoModelForCausalLM, AutoTokenizer
        self.tok = AutoTokenizer.from_pretrained(base_model)
        adapter_file = os.path.join(adapter_dir, "adapter_model.safetensors")
        has_adapter = bool(adapter_dir and os.path.isfile(adapter_file))
        if not has_adapter and not self.tok.chat_template:
            raise ValueError(f"base model has no canonical chat template: {base_model}")
        base = AutoModelForCausalLM.from_pretrained(
            base_model, dtype=dtype, low_cpu_mem_usage=True).to(device)
        self.adapters_loaded: set[str] = set()
        self._active_adapter: str | None = None
        if has_adapter:
            self._repair_adapter_config(adapter_dir, base_model)
            from peft import PeftModel
            self.model = PeftModel.from_pretrained(
                base, adapter_dir, adapter_name="default").to(device).eval()
            self.adapters_loaded.add("default")
            for lang_key, adir in (("ko", adapter_ko), ("ja", adapter_ja),
                                   ("zh", adapter_zh), ("ru", adapter_ru)):
                if adir and os.path.isfile(os.path.join(
                        adir, "adapter_model.safetensors")):
                    try:
                        self.model.load_adapter(adir, adapter_name=lang_key)
                        self.adapters_loaded.add(lang_key)
                        log.info("router adapter[%s] loaded ← %s", lang_key, adir)
                    except Exception as e:
                        log.warning("router adapter[%s] load fail (%s): %s",
                                    lang_key, adir, e)
            self.model.set_adapter("default")
            self._active_adapter = "default"
        else:
            self.model = base.eval()
            if adapter_dir:
                log.info("adapter absent at %s — canonical base chat model", adapter_dir)
        self.vocab_size = self.model.config.vocab_size
        log.info("HF chat substrate ready: base=%s adapters=%s params≈%d",
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
        """Switch to a loaded language adapter; base-only chat is a no-op."""
        if not self.adapters_loaded:
            return
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
        if self.adapters_loaded:
            if not _seed_matches_lang(seed_text, lang_hint):
                seed_text = ""
            primed = LANG_PRIMES.get(lang_hint or "", "") + (seed_text or "")
            if primed:
                ids = self.tok(primed, return_tensors="pt").input_ids.to(self.device)
            else:
                bid = self.tok.bos_token_id or self.tok.eos_token_id
                ids = torch.tensor([[bid]], device=self.device)
        else:
            messages = [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": seed_text or "..."},
            ]
            encoded = self.tok.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                return_tensors="pt", return_dict=True).to(self.device)
            ids = encoded.input_ids
        do_sample = bool(kw.get("do_sample", False))
        generation = {
            "max_new_tokens": max_new,
            "do_sample": do_sample,
            "repetition_penalty": kw.get("repetition_penalty", 1.05),
            "pad_token_id": self.tok.pad_token_id,
            "eos_token_id": self.tok.eos_token_id,
        }
        if do_sample:
            generation.update({
                "temperature": kw.get("temperature", 0.7),
                "top_k": kw.get("top_k", 20),
                "top_p": kw.get("top_p", 0.8),
            })
        out = self.model.generate(ids, **generation)
        return self.tok.decode(
            out[0][ids.shape[1]:], skip_special_tokens=True).strip()

    @torch.no_grad()
    def entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        if self.adapters_loaded:
            if seed_text:
                ids = self.tok(seed_text, return_tensors="pt").input_ids.to(self.device)
            else:
                bid = self.tok.bos_token_id or self.tok.eos_token_id
                ids = torch.tensor([[bid]], device=self.device)
        else:
            messages = [
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": seed_text or "..."},
            ]
            encoded = self.tok.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                return_tensors="pt", return_dict=True).to(self.device)
            ids = encoded.input_ids
        logits = self.model(ids).logits[0, -1]
        p = F.softmax(logits.float(), dim=-1)
        ent = -(p * (p + 1e-12).log()).sum().item()
        emb = self.model.get_input_embeddings()(ids)[0].mean(0).float().cpu()
        return ent / math.log(logits.shape[-1]), emb

    def param_count(self) -> int:
        return sum(p.numel() for p in self.model.parameters())
