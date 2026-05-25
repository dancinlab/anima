# Substrate plugin spec — anima_participant 의 substrate-pluggable refactor

> History → [./SUBSTRATE_PLUGIN.log.md](./SUBSTRATE_PLUGIN.log.md).

> 사용자 directive 2026-05-22: anima_participant.py 를 substrate 와 분리 (LoRA /
> V3 / future) — option C "shared core + substrate plugin". motivation 8-factor +
> KOSMOS + lang-detect + broker connection 은 substrate 무관 (anima 의식 동역학),
> substrate 만 plugin.

## 구조

```
HEXAD/CHAT/server/
  ├ broker.py                       # FastAPI + WebSocket (그대로)
  ├ anima_participant.py            # tick loop + motivation + broker conn (refactor: substrate import)
  ├ akida_bridge.py                 # Pi spike forward (그대로)
  ├ akida_ws_publisher.py           # subprocess pipeline (그대로)
  ├ substrate_base.py               # 🆕 ABC (Substrate interface)
  ├ substrate_lora.py               # 🆕 vP21M (Qwen + LoRA r32 + mitosis aux) wrapper
  ├ substrate_v3.py                 # 🆕 ConsciousDecoderV3 wrapper (V3 land 시)
  └ kosmos_io.py                    # 그대로 (substrate 무관)
```

## Substrate ABC (정의)

```python
# substrate_base.py
from abc import ABC, abstractmethod
import torch
from typing import Any

class Substrate(ABC):
    """Pluggable substrate interface for anima participant.

    motivation 8-factor / KOSMOS / lang-detect 가 substrate 무관.
    LoRA / V3 / future 가 이 ABC 충족하면 anima_participant 가 그대로 작동.
    """

    name: str  # "lora" | "v3" | "llama" etc
    device: str  # "mps" | "cuda" | "cpu"
    vocab_size: int

    @abstractmethod
    def generate(self, seed_text: str, max_new: int = 80,
                 lang_hint: str | None = None, **kw) -> str:
        """Free-form generation given seed text + optional lang prime.
        Used by Talker for emission.
        """
        ...

    @abstractmethod
    @torch.no_grad()
    def entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        """Compute normalized entropy ∈ [0, 1] of next-token distribution +
        embedding of seed. Used by Thinker for 8-factor motivation:
        - ent_norm → phi → relevance + coherence
        - emb → recent_embeds similarity (info_gap / originality)
        """
        ...

    @abstractmethod
    def param_count(self) -> int:
        """Trainable + total params for diagnostics."""
        ...

    # optional capabilities (substrate 가 지원하면 override)

    def mitosis_state(self) -> dict[str, Any] | None:
        """Current mitosis cell pool snapshot (V3 만 — LoRA 는 None).
        Used by anima_participant 의 substrate-snapshot logging.
        """
        return None

    def cross_attention_input(self) -> torch.Tensor | None:
        """Optional KOSMOS anchor input for cross-attn (V3 만).
        Returns None for LoRA — KOSMOS anchor 외부 ingestion 만.
        """
        return None
```

## substrate_lora.py 구현 (LORA 세션 owner)

```python
# substrate_lora.py — vP21M (Qwen2.5-1.5B + LoRA r32 + mitosis aux)
import torch, math
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
from substrate_base import Substrate

BASE_MODEL = "Qwen/Qwen2.5-1.5B"
LANG_PRIMES = {"en": "I notice ", "ko": "문득 ", "zh": "我注意到 ",
               "ru": "Я замечаю ", "ja": "ふと "}

class LoraSubstrate(Substrate):
    name = "lora"

    def __init__(self, adapter_dir: str, device: str = "mps",
                 dtype: torch.dtype = torch.float16):
        self.device = device
        self.tok = AutoTokenizer.from_pretrained(BASE_MODEL)
        base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=dtype).to(device)
        self.model = PeftModel.from_pretrained(base, adapter_dir).to(device).eval()
        self.vocab_size = self.model.config.vocab_size

    def generate(self, seed_text, max_new=80, lang_hint=None, **kw) -> str:
        prime = LANG_PRIMES.get(lang_hint, "")
        primed = prime + (seed_text or "")
        ids = self.tok(primed, return_tensors="pt").input_ids.to(self.device) \
              if primed else torch.tensor([[self.tok.bos_token_id or self.tok.eos_token_id]]).to(self.device)
        out = self.model.generate(ids, max_new_tokens=max_new,
                                  do_sample=True, temperature=1.0, top_k=50, top_p=0.95,
                                  repetition_penalty=1.2,
                                  pad_token_id=self.tok.eos_token_id)
        return self.tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)

    @torch.no_grad()
    def entropy_of_next(self, seed_text):
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

    # mitosis_state / cross_attention_input → default None (LoRA path)
```

## substrate_v3.py 구현 (V3 세션 owner, V3 land 후)

```python
# substrate_v3.py — ConsciousDecoderV3 (pure HEXAD substrate)
import torch, math
import torch.nn.functional as F
from transformers import AutoTokenizer  # Qwen tokenizer share
from conscious_decoder_v3 import ConsciousDecoderV3
from substrate_base import Substrate

class V3Substrate(Substrate):
    name = "v3"

    def __init__(self, ckpt_path: str, init_variant: str = "qwen",
                 device: str = "mps", dtype: torch.dtype = torch.bfloat16):
        self.device = device
        self.tok = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-1.5B")
        # ConsciousDecoderV3 직접 인스턴스 + ckpt load
        self.model = ConsciousDecoderV3(
            vocab_size=151936, d_model=1536, n_layer=28,
            n_head=12, n_kv_head=4, block_size=512,
            mitosis_active=True,  # inference-time mitosis
        ).to(device).eval()
        state = torch.load(ckpt_path, map_location=device)
        self.model.load_state_dict(state["model"] if "model" in state else state)
        self.vocab_size = 151936

    def generate(self, seed_text, max_new=80, lang_hint=None, **kw) -> str:
        prime = LANG_PRIMES.get(lang_hint, "")
        primed = prime + (seed_text or "")
        ids = self.tok(primed, return_tensors="pt").input_ids.to(self.device) \
              if primed else torch.tensor([[self.tok.bos_token_id or self.tok.eos_token_id]]).to(self.device)
        # V3 의 forward 는 (logits_a, logits_g, tensions, kv, mitosis_info) 반환
        # head_a 만 generation 에 사용 (LoRA 와 동일 lang capability)
        return self.model.generate(ids, max_new_tokens=max_new,
                                   tokenizer=self.tok, **kw)  # V3 가 자체 generate 메서드 제공

    @torch.no_grad()
    def entropy_of_next(self, seed_text):
        # V3 의 head_a logits 만 사용 (head_g 는 KOSMOS tension 용)
        if seed_text:
            ids = self.tok(seed_text, return_tensors="pt").input_ids.to(self.device)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(self.device)
        out = self.model(ids)
        logits_a = out[0]  # (B, T, V)
        p = F.softmax(logits_a[0, -1].float(), dim=-1)
        ent = -(p * (p + 1e-12).log()).sum().item()
        emb = self.model.token_embed(ids)[0].mean(0).float().cpu()
        return ent / math.log(logits_a.shape[-1]), emb

    def param_count(self) -> int:
        return sum(p.numel() for p in self.model.parameters())

    def mitosis_state(self) -> dict[str, Any]:
        # V3 의 mitosis cell pool snapshot
        return self.model.mitosis.snapshot() if hasattr(self.model, "mitosis") else None

    def cross_attention_input(self) -> torch.Tensor | None:
        # KOSMOS anchor 가 ingestion 됐으면 cross-attn key/value 로
        return self.model.kosmos_cross_input if hasattr(self.model, "kosmos_cross_input") else None
```

## anima_participant.py refactor (LORA 세션 owner)

```python
# anima_participant.py — substrate-agnostic
import argparse, importlib
from substrate_base import Substrate

ap = argparse.ArgumentParser()
ap.add_argument("--substrate", choices=["lora", "v3"], default="lora")
ap.add_argument("--adapter-dir", help="for substrate=lora")
ap.add_argument("--v3-ckpt", help="for substrate=v3")
ap.add_argument("--v3-init", default="qwen")
ap.add_argument("--threshold", type=float, default=0.30)
args = ap.parse_args()

# substrate plugin 동적 load
if args.substrate == "lora":
    from substrate_lora import LoraSubstrate
    substrate: Substrate = LoraSubstrate(adapter_dir=args.adapter_dir)
elif args.substrate == "v3":
    from substrate_v3 import V3Substrate
    substrate: Substrate = V3Substrate(ckpt_path=args.v3_ckpt, init_variant=args.v3_init)

# 이후 tick loop / 8-factor / KOSMOS / broker conn 은 substrate 와 무관 (substrate.generate / entropy_of_next 만 사용)
class AnimaState:
    def __init__(self, substrate: Substrate):
        self.substrate = substrate
        # ... (그대로)

    def tick(self, threshold: float) -> dict:
        seed_text, strat = self._seed_text()
        ent_norm, emb = self.substrate.entropy_of_next(seed_text)
        # ... (그대로)

    def emit(self, seed_text: str, lang_hint: str | None = None) -> str:
        # D2 lang rotation 그대로
        ...
        return self.substrate.generate(seed_text, max_new=MAX_NEW, lang_hint=lang_hint)
```

LaunchAgent plist 갱신:

```xml
<key>ProgramArguments</key>
<array>
  <string>/Users/mini/anima_chat_pack/venv/bin/python3</string>
  <string>/Users/mini/anima_chat_pack/anima_participant.py</string>
  <string>--substrate</string>
  <string>lora</string>  <!-- 또는 v3 -->
  <string>--adapter-dir</string>
  <string>/Users/mini/anima_chat_pack/lora_adapter</string>
  <string>--threshold</string>
  <string>0.30</string>
</array>
```

## 작업 분담 (path-split 정합)

| 세션 | task |
|---|---|
| **V3 (본 세션)** | `substrate_base.py` ABC + `substrate_v3.py` 구현 (V3 land 시 ckpt 사용) + 본 spec 문서 |
| **LORA 세션** | `substrate_lora.py` 구현 (anima_participant.py 의 vP21M 부분 추출) + `anima_participant.py` refactor (substrate plugin import + --substrate arg) + LaunchAgent plist 갱신 + production deploy |

## refactor 단계 (LORA 세션 권장 순서)

1. `substrate_base.py` 작성 (본 spec 의 ABC, V3 세션 이미 작성)
2. `substrate_lora.py` 작성 (anima_participant.py 의 모델/추론 부분 추출 + 본 spec 의 reference 구현 참고)
3. `anima_participant.py` refactor: substrate import + `self.substrate.generate(...)` 로 generation 호출 분리
4. 로컬 smoke test (`python3 anima_participant.py --substrate lora --adapter-dir ./lora_adapter`)
5. mini deploy: rsync + LaunchAgent plist 갱신 + 재로드
6. chat.dancinlab.org verify (동작 그대로, refactor 보이지 X)

## 마이그레이션 위험

- substrate API surface 가 정확히 호환되어야 — LoraSubstrate 의 entropy_of_next 가 기존 anima_participant 의 `_entropy_of_next` 와 같은 (ent_norm, embed) 반환
- LoRA generation hyperparameters (T=1.0, top_p, repetition_penalty) substrate 안으로 이동 vs 외부 인자 — 외부 인자가 깔끔 (anima_participant 가 hyperparams 결정)
- mitosis_lib.CellPool 이 substrate 안에서만 import — LoRA path 는 mitosis 비활성 (train-time only, inference X)
- v3 ckpt 가 land 되지 않은 상태 (V3β 진행 중)에서는 substrate_v3.py = stub OK
