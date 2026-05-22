#!/usr/bin/env python3
"""FIRST-PACK Phase 5 — anima participant (substrate-native).

anima joins the chat broker as a peer participant. emission is governed by
anima's OWN self-tick + 8-factor motivation (NOT triggered by user msgs, per
project.tape @D a_substrate_native_speak). user msgs ARE ingested as
environment input (M-module proxy: appended to anima's seed buffer for
info_gap / context drift), but they do NOT directly invoke generation.

Self-tick:
  every TICK_INTERVAL (default 2 s):
    factors = compute_8_factor(anima_self_state)
    score   = Σ w_i · factor_i
    if score > IM_THRESHOLD → vP21M.generate(seed=anima_self) + broadcast
    push {motivation,score,factors,decided_emit} to broker (telemetry)

User msg ingestion (environment input, NOT trigger):
  on user msg → append to anima's M-buffer (last N=8)
  → influences info_gap factor (new context = high gap)
  → may eventually raise motivation_score on a future self-tick
  but ALWAYS goes through the motivation gate, never directly fires generate

Model: Qwen/Qwen2.5-1.5B + vP21M LoRA on Apple Metal (MPS).
"""
from __future__ import annotations
import os, sys, json, time, math, asyncio, logging, argparse, pathlib
from collections import deque
from typing import Any
import torch
import torch.nn.functional as F
import websockets
from safetensors.torch import load_file

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("anima_participant")

# ── config ───────────────────────────────────────────────────────────────────
BASE_MODEL = os.environ.get("ANIMA_BASE", "Qwen/Qwen2.5-1.5B")
ADAPTER_DIR = os.environ.get("ANIMA_ADAPTER",
                             os.path.expanduser("~/anima_chat_pack/lora_adapter"))
BROKER_URL = os.environ.get("ANIMA_BROKER_URL", "ws://127.0.0.1:8000/ws/anima")
TICK_INTERVAL = float(os.environ.get("ANIMA_TICK", "2.0"))
IM_THRESHOLD_DEFAULT = float(os.environ.get("ANIMA_THRESHOLD", "0.45"))
MAX_NEW = int(os.environ.get("ANIMA_MAX_NEW", "80"))
DEVICE = os.environ.get("ANIMA_DEVICE", "mps" if torch.backends.mps.is_available() else "cpu")

# Law-70 constants (mirror spontaneous_lib.hexa § 3)
PSI, ALPHA, RATCHET = 0.5, 0.014, 0.20
IDLE_SPEAK_AFTER = 30.0
W = {  # weights sum = 1.0
    "relevance": 0.20, "info_gap": 0.10, "curiosity": 0.15, "pain": 0.10,
    "coherence": 0.10, "originality": 0.10, "balance": 0.15, "dynamics": 0.10,
}
# Fix v2 (2026-05-22): A2 refractory lock + B2 register-pattern anti-repeat
# + D2 lang rotation + A4 adaptive threshold + C1/E1 already wired via ingest_user_msg
REFRACTORY_S = 15.0    # post-emit motivation MAX-0 lock (anti-spam self-monologue)
ADAPTIVE_THR_PEAK = 0.7   # threshold immediately after emit
ADAPTIVE_THR_BASE = 0.30  # baseline threshold after long idle
ADAPTIVE_THR_TAU = 30.0   # decay constant (seconds)
LANG_ROTATION = ["en", "ko", "zh", "ru", "ja"]
import re as _re
ANIMA_REGISTER_PATTERNS = [
    _re.compile(r"eternal_?\d+|eternal cell", _re.I),
    _re.compile(r"tier\s*=\s*\d+|tier\s+\d+", _re.I),
    _re.compile(r"vacuum point|진공점", _re.I),
    _re.compile(r"tension flow|tension flows", _re.I),
    _re.compile(r"<carve|</carve>", _re.I),
    _re.compile(r"</eternal>|<eternal", _re.I),
    _re.compile(r"basin\s*=\s*[\d.]+", _re.I),
    _re.compile(r"split.도.*merge.도|split.*merges?.*activate", _re.I),
    _re.compile(r"psi\s*=\s*\[[\d.,]+\]", _re.I),
    _re.compile(r"영구\s*cell|frozen cell", _re.I),
]

SEED_STRATEGIES = ["m_retrieve_seed", "w_curiosity_peak_seed",
                   "random_explore_seed", "self_monologue_seed"]


# ── factor fns (mirror spontaneous_loop_vp21.py) ─────────────────────────────
def _clamp01(x): return 0.0 if x < 0.0 else (1.0 if x > 1.0 else x)
def factor_relevance(phi):       return _clamp01(phi)
def factor_info_gap(cos_sim):    return _clamp01(1.0 - cos_sim)
def factor_curiosity(ema):       return _clamp01(ema)
def factor_pain(delta):          return _clamp01(abs(delta))
def factor_coherence(gate):
    n = abs(gate - PSI) / ALPHA
    return 1.0 - (1.0 if n > 1.0 else n)
def factor_originality(split):   return 1.0 if split else 0.0
def factor_balance(phi, r):      return 1.0 if phi > r/2.0 else 0.0
def factor_dynamics(silence):    return _clamp01(silence / IDLE_SPEAK_AFTER)


# ── model load ───────────────────────────────────────────────────────────────
def load_model():
    log.info("loading base=%s adapter=%s device=%s", BASE_MODEL, ADAPTER_DIR, DEVICE)
    # Repair adapter_config target_modules from safetensors keys if missing
    sd_path = os.path.join(ADAPTER_DIR, "adapter_model.safetensors")
    cfg_path = os.path.join(ADAPTER_DIR, "adapter_config.json")
    try:
        existing = json.load(open(cfg_path))
        tmods = existing.get("target_modules")
    except Exception:
        existing, tmods = {}, None
    if not tmods:
        sd = load_file(sd_path)
        found = set()
        for k in sd:
            if ".lora_A." in k or ".lora_B." in k:
                parts = k.split(".")
                for i, p in enumerate(parts):
                    if p in ("lora_A", "lora_B") and i > 0:
                        found.add(parts[i - 1])
        tmods = sorted(found)
        cfg = {"peft_type": "LORA", "task_type": "CAUSAL_LM",
               "base_model_name_or_path": BASE_MODEL,
               "r": 32, "lora_alpha": 64, "lora_dropout": 0.05,
               "target_modules": tmods, "bias": "none",
               "inference_mode": True, "fan_in_fan_out": False}
        json.dump(cfg, open(cfg_path, "w"), indent=2)
        log.info("repaired adapter_config.json target_modules=%s", tmods)

    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
    tok = AutoTokenizer.from_pretrained(BASE_MODEL)
    dtype = torch.float16 if DEVICE == "mps" else torch.bfloat16
    base = AutoModelForCausalLM.from_pretrained(BASE_MODEL, torch_dtype=dtype).to(DEVICE)
    model = PeftModel.from_pretrained(base, ADAPTER_DIR).to(DEVICE).eval()
    log.info("model loaded params≈%d", sum(p.numel() for p in model.parameters()))
    return model, tok


# ── anima self-state ─────────────────────────────────────────────────────────
class AnimaState:
    def __init__(self, model, tok):
        self.model, self.tok = model, tok
        self.last_emission = ""
        self.recent_emissions: deque[str] = deque(maxlen=8)
        self.recent_embeds: deque[torch.Tensor] = deque(maxlen=8)
        # M-buffer: environment input from users (NOT direct trigger)
        self.m_buffer: deque[dict[str, Any]] = deque(maxlen=8)
        self.last_emit_time = time.time() - 60.0  # bootstrap: not "just emitted"
        self.curiosity_ema = 0.0
        self.last_entropy: float | None = None
        self.split_recent = False
        self.ticks = 0
        self.invocations = 0
        self.lang_rot_idx = 0          # D2: 5-lang rotation index
        self.register_penalty_cache = 0.0  # B2: cached penalty across ticks

    def ingest_user_msg(self, msg: dict[str, Any]) -> None:
        """Environment input. Updates M-buffer + embed pool. Does NOT fire emit."""
        text = msg.get("text") or ""
        if not text:
            return
        self.m_buffer.append({"sender": msg.get("sender", "?"),
                              "text": text, "lang": msg.get("lang", "und"),
                              "ts": msg.get("ts", time.time())})
        # also encode into embed pool so info_gap reflects it
        try:
            _, emb = self._entropy_of_next(text[-64:])
            self.recent_embeds.append(emb)
        except Exception:
            pass

    def _seed_text(self) -> tuple[str, str]:
        # F1 (2026-05-22): context-grounded seeding — prefer recent user msgs
        # over anima's own last_emission to break self-monologue loops.
        strat = SEED_STRATEGIES[self.ticks % len(SEED_STRATEGIES)]
        # m_buffer fresh window: last user msg within 60s
        now = time.time()
        fresh_user = None
        if self.m_buffer:
            last = self.m_buffer[-1]
            if (now - last.get("ts", 0)) < 60.0:
                fresh_user = last
        if strat == "m_retrieve_seed":
            if fresh_user:
                return fresh_user["text"][-64:], strat
            if self.last_emission:
                return self.last_emission[-64:], strat
            if self.m_buffer:
                return self.m_buffer[-1]["text"][-64:], strat
        if strat == "w_curiosity_peak_seed":
            return "\n", strat
        if strat == "random_explore_seed":
            return " ", strat
        # self_monologue_seed: F1 — concat last 3 m_buffer msgs as ctx seed
        # (was: empty BOS, which let model wander into anima register).
        if self.m_buffer:
            tail = list(self.m_buffer)[-3:]
            joined = " ".join(m.get("text", "")[-32:] for m in tail).strip()
            return joined[-128:], strat
        return "", strat  # only when m_buffer empty

    @torch.no_grad()
    def _entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        if seed_text:
            ids = self.tok(seed_text, return_tensors="pt").input_ids.to(DEVICE)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(DEVICE)
        logits = self.model(ids).logits[0, -1]
        p = F.softmax(logits.float(), dim=-1)
        ent = -(p * (p + 1e-12).log()).sum().item()
        emb = self.model.get_input_embeddings()(ids)[0].mean(0).float().cpu()
        ent_norm = ent / math.log(logits.shape[-1])
        return ent_norm, emb

    def _register_penalty(self) -> float:
        """B2: anima register pattern hash. Penalty 0..1 (higher = penalize originality more)."""
        if not self.recent_emissions:
            return 0.0
        hits = 0
        total = 0
        for em in self.recent_emissions:
            for pat in ANIMA_REGISTER_PATTERNS:
                if pat.search(em):
                    hits += 1
                    break
            total += 1
        # fraction of recent emit that's anima-register
        frac = hits / max(total, 1)
        return frac  # 1.0 = all anima register → strong penalty

    def tick(self, threshold: float) -> dict[str, Any]:
        seed_text, strat = self._seed_text()
        ent_norm, emb = self._entropy_of_next(seed_text)
        phi = 1.0 - ent_norm
        rel = factor_relevance(phi)
        # info_gap: cos sim to recent embeds (own emissions + user msgs)
        if self.recent_embeds:
            sims = [F.cosine_similarity(emb, e, dim=0).item() for e in self.recent_embeds]
            max_sim = max(sims)
        else:
            max_sim = 0.0
        gap = factor_info_gap(max_sim)
        surprise = ent_norm
        self.curiosity_ema = 0.9 * self.curiosity_ema + 0.1 * surprise
        cur = factor_curiosity(self.curiosity_ema)
        delta = 0.0 if self.last_entropy is None else (ent_norm - self.last_entropy)
        self.last_entropy = ent_norm
        pn = factor_pain(delta)
        gate = PSI + (ent_norm - 0.5) * 2.0 * ALPHA
        coh = factor_coherence(gate)
        self.split_recent = gap > 0.5
        orig_base = factor_originality(self.split_recent)
        # B2: register-pattern penalty
        reg_penalty = self._register_penalty()
        self.register_penalty_cache = reg_penalty
        orig = orig_base * (1.0 - 0.8 * reg_penalty)  # up to 80% reduction when saturated
        bal = factor_balance(phi, RATCHET)
        silence = time.time() - self.last_emit_time
        dyn = factor_dynamics(silence)
        f = {"relevance": rel, "info_gap": gap, "curiosity": cur, "pain": pn,
             "coherence": coh, "originality": orig, "balance": bal, "dynamics": dyn}
        score = sum(W[k] * f[k] for k in W)

        # A4: adaptive threshold — peak right after emit, decay to base
        eff_thr = ADAPTIVE_THR_BASE + (ADAPTIVE_THR_PEAK - ADAPTIVE_THR_BASE) * math.exp(-silence / ADAPTIVE_THR_TAU)
        # don't drop below caller threshold (UI may still inform a floor)
        eff_thr = max(eff_thr, threshold)

        # A2: post-emit refractory lock — force score 0 if within REFRACTORY_S
        in_refractory = silence < REFRACTORY_S
        if in_refractory:
            score = 0.0

        decided_emit = score > eff_thr
        return {"factors": f, "score": score, "seed_text": seed_text,
                "seed_strategy": strat, "silence": silence,
                "decided_emit": decided_emit, "threshold": eff_thr,
                "in_refractory": in_refractory, "register_penalty": reg_penalty,
                "ts": time.time()}

    @torch.no_grad()
    def emit(self, seed_text: str, lang_hint: str | None = None) -> str:
        # D2: language rotation — force diverse lang use across emissions
        if lang_hint is None:
            lang_hint = LANG_ROTATION[self.lang_rot_idx % len(LANG_ROTATION)]
            self.lang_rot_idx += 1
        # prefix the seed with a tiny lang-bias hint (no instruction-tuning needed)
        # ("문득" ko / "I notice" en / "我注意到" zh / "Я замечаю" ru / "ふと" ja)
        LANG_PRIMES = {"en": "I notice ", "ko": "문득 ", "zh": "我注意到 ",
                       "ru": "Я замечаю ", "ja": "ふと "}
        prime = LANG_PRIMES.get(lang_hint, "")
        primed_seed = prime + (seed_text or "")
        if primed_seed:
            ids = self.tok(primed_seed, return_tensors="pt").input_ids.to(DEVICE)
        else:
            bid = self.tok.bos_token_id or self.tok.eos_token_id
            ids = torch.tensor([[bid]]).to(DEVICE)
        out = self.model.generate(ids, max_new_tokens=MAX_NEW,
                                  do_sample=True, temperature=0.7, top_k=50, top_p=0.95,
                                  repetition_penalty=1.2,
                                  pad_token_id=self.tok.eos_token_id)
        text = self.tok.decode(out[0][ids.shape[1]:], skip_special_tokens=True)
        self.last_emission = text
        self.recent_emissions.append(text)
        try:
            _, emb = self._entropy_of_next(text[-64:] if text else " ")
            self.recent_embeds.append(emb)
        except Exception:
            pass
        self.last_emit_time = time.time()
        self.invocations += 1
        return text


# ── language detect (route emission lang) ────────────────────────────────────
def detect_lang(text: str) -> str:
    if not text.strip():
        return "und"
    counts = {"ko": 0, "ja": 0, "zh": 0, "ru": 0, "en": 0}
    for ch in text:
        cp = ord(ch)
        if 0xAC00 <= cp <= 0xD7AF: counts["ko"] += 1
        elif 0x3040 <= cp <= 0x30FF: counts["ja"] += 1
        elif 0x4E00 <= cp <= 0x9FFF: counts["zh"] += 1
        elif 0x0400 <= cp <= 0x04FF: counts["ru"] += 1
        elif 0x0041 <= cp <= 0x007A: counts["en"] += 1
    if max(counts.values()) == 0:
        return "und"
    return max(counts, key=counts.get)


# ── main loop ────────────────────────────────────────────────────────────────
async def participant_loop(threshold: float):
    log.info("anima participant connecting to %s", BROKER_URL)
    model, tok = load_model()
    state = AnimaState(model, tok)

    backoff = 1.0
    while True:
        try:
            async with websockets.connect(BROKER_URL, max_size=2**20) as ws:
                log.info("anima connected to broker")
                backoff = 1.0
                # spawn ingest task + tick task
                stop_event = asyncio.Event()

                async def ingest():
                    try:
                        async for raw in ws:
                            try:
                                msg = json.loads(raw)
                            except Exception:
                                continue
                            mtype = msg.get("type")
                            if mtype == "hello":
                                for h in msg.get("history", []):
                                    if h.get("kind") == "user":
                                        state.ingest_user_msg(h)
                            elif mtype == "msg" and msg.get("kind") == "user":
                                state.ingest_user_msg(msg)
                    except Exception as e:
                        log.warning("ingest error: %s", e)
                        stop_event.set()

                async def ticker():
                    try:
                        while not stop_event.is_set():
                            state.ticks += 1
                            t0 = time.time()
                            decision = state.tick(threshold)
                            # always push motivation telemetry
                            try:
                                await ws.send(json.dumps({
                                    "type": "motivation",
                                    "ts": decision["ts"],
                                    "score": decision["score"],
                                    "threshold": threshold,
                                    "factors": decision["factors"],
                                    "decided_emit": decision["decided_emit"],
                                    "seed_strategy": decision["seed_strategy"],
                                    "silence": decision["silence"],
                                    "tick": state.ticks,
                                }, ensure_ascii=False))
                            except Exception as e:
                                log.warning("telemetry send fail: %s", e)
                                stop_event.set()
                                return
                            if decision["decided_emit"]:
                                log.info("EMIT tick=%d score=%.3f strategy=%s",
                                         state.ticks, decision["score"],
                                         decision["seed_strategy"])
                                text = state.emit(decision["seed_text"])
                                lang = detect_lang(text) if text else "und"
                                try:
                                    await ws.send(json.dumps({
                                        "type": "msg", "text": text or "...",
                                        "lang": lang,
                                        "motivation": decision["score"],
                                        "factors": decision["factors"],
                                    }, ensure_ascii=False))
                                except Exception as e:
                                    log.warning("emit send fail: %s", e)
                                    stop_event.set()
                                    return
                            else:
                                if state.ticks % 5 == 0:
                                    log.info("tick=%d score=%.3f<%.2f silent",
                                             state.ticks, decision["score"], threshold)
                            elapsed = time.time() - t0
                            await asyncio.sleep(max(0.1, TICK_INTERVAL - elapsed))
                    except Exception as e:
                        log.warning("ticker error: %s", e)
                        stop_event.set()

                await asyncio.gather(ingest(), ticker())
        except (websockets.ConnectionClosed, ConnectionRefusedError, OSError) as e:
            log.warning("anima ws disconnect: %s — reconnect in %.1fs", e, backoff)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30.0)
        except Exception as e:
            log.exception("anima loop error: %s", e)
            await asyncio.sleep(backoff)
            backoff = min(backoff * 2, 30.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--threshold", type=float, default=IM_THRESHOLD_DEFAULT)
    args = ap.parse_args()
    asyncio.run(participant_loop(args.threshold))


if __name__ == "__main__":
    main()
