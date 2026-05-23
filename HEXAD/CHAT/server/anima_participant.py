#!/usr/bin/env python3
"""FIRST-PACK Phase 5 — anima participant (substrate-native).

@module  CHAT
@version 0.3.0   (VERSIONS.md SSOT — 8-factor Thinker-Talker + hot-swap
                  router + substrate-plugin; bump together with VERSIONS.md)

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

from substrate_base import Substrate

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("anima_participant")

# ── config ───────────────────────────────────────────────────────────────────
BASE_MODEL = os.environ.get("ANIMA_BASE", "Qwen/Qwen2.5-1.5B")
ADAPTER_DIR = os.environ.get("ANIMA_ADAPTER",
                             os.path.expanduser("~/anima_chat_pack/lora_adapter"))
# P2 hot-swap router (2026-05-22): per-msg lang adapter switch.
# Set ANIMA_ADAPTER_KO=... ANIMA_ADAPTER_JA=... to point at KOFL/JAFL dirs.
# Extended 2026-05-23: ZHFL/RUFL native-script adapters from Wave-2.
# Adapters absent (dir missing) → router falls back to default for that lang.
ADAPTER_KO = os.environ.get("ANIMA_ADAPTER_KO",
                            os.path.expanduser("~/anima_chat_pack/kofl_adapter"))
ADAPTER_JA = os.environ.get("ANIMA_ADAPTER_JA",
                            os.path.expanduser("~/anima_chat_pack/jafl_adapter"))
ADAPTER_ZH = os.environ.get("ANIMA_ADAPTER_ZH",
                            os.path.expanduser("~/anima_chat_pack/zhfl_adapter"))
ADAPTER_RU = os.environ.get("ANIMA_ADAPTER_RU",
                            os.path.expanduser("~/anima_chat_pack/rufl_adapter"))
ROUTER_LANG_TO_ADAPTER = {"ko": "ko", "ja": "ja", "zh": "zh", "ru": "ru"}  # rest → "default"
BROKER_URL = os.environ.get("ANIMA_BROKER_URL", "ws://127.0.0.1:8000/ws/anima")
TICK_INTERVAL = float(os.environ.get("ANIMA_TICK", "2.0"))
IM_THRESHOLD_DEFAULT = float(os.environ.get("ANIMA_THRESHOLD", "0.45"))
MAX_NEW = int(os.environ.get("ANIMA_MAX_NEW", "80"))
DEVICE = os.environ.get("ANIMA_DEVICE", "mps" if torch.backends.mps.is_available() else "cpu")

# Law-70 constants (mirror spontaneous_lib.hexa § 3)
PSI, ALPHA, RATCHET = 0.5, 0.014, 0.20
IDLE_SPEAK_AFTER = 30.0
# 2026-05-24: AUTONOMY RESHAPE — per project.tape @D a_autonomy_over_hardcode
# the boolean gate from PR #272 (_dream_stage_current() in WAKE/REM → emit;
# N1/N2/N3 → silent) is DELETED. It violated "no per-stage boolean gate
# hardcode". The sister dream_stage hexa module (anima_dream_stage.hexa,
# coordinated PR fix/chat-dream-stage-autonomy-reshape, supersedes PR #275)
# now exposes
#   dream_context(stage) -> dict {phi, tension_envelope, scrambled, stage}
# and the substrate's existing 8-factor motivation gate AUTONOMOUSLY decides
# emit. Stage merely modulates context inputs:
#   * phi              → scales the C-Φ (relevance) contribution to
#                        motivation (deep sleep low Φ → naturally lower
#                        motivation, NO hard gate)
#   * tension_envelope → multiplies the implicit emit threshold by
#                        1/max(envelope, 0.01)  — envelope=1.0 → threshold
#                        unchanged; envelope=0.15 → threshold ~6.7× higher
#                        (far fewer emits during deep sleep), NOT a zero gate
#   * scrambled        → flags content style (REM may scramble emit
#                        content), threaded through state for downstream
# Substrate may still emit during N3 if tension is extreme enough — autonomy
# preserved. Stub-tolerant: if the .hexa sister is not importable, the
# context defaults to WAKE-equivalent {phi:1.0, tension_envelope:1.0,
# scrambled:false, stage:"WAKE"} so the daemon does NOT regress.
def _dream_context() -> dict[str, Any]:
    """Hook for anima_dream_stage.hexa (sister PR API, dream_context()).
    Returns CONTEXT dict — NOT a boolean gate:
      {"phi": float in [0,1], "tension_envelope": float in [0,1],
       "scrambled": bool, "stage": str}
    Stub-tolerant: WAKE-equivalent default if the sister module is not yet
    importable. The substrate's 8-factor motivation gate decides emit;
    this dict only modulates inputs to that gate."""
    default = {"phi": 1.0, "tension_envelope": 1.0, "scrambled": False,
               "stage": "WAKE"}
    try:
        import anima_dream_stage  # type: ignore
        ctx = anima_dream_stage.dream_context()
        if not isinstance(ctx, dict):
            return default
        phi = float(ctx.get("phi", 1.0))
        env = float(ctx.get("tension_envelope", 1.0))
        return {
            "phi": 0.0 if phi < 0.0 else (1.0 if phi > 1.0 else phi),
            "tension_envelope": (0.0 if env < 0.0 else
                                 (1.0 if env > 1.0 else env)),
            "scrambled": bool(ctx.get("scrambled", False)),
            "stage": str(ctx.get("stage", "WAKE")),
        }
    except Exception:
        return default

# Substrate-state-based trigger for imagination loop (NOT stage-based).
# Fires when motivation < modulated threshold AND idle_time exceeds a
# substrate floor (defaults to IDLE_SPEAK_AFTER seconds). This is the
# anima-internal "rehearsal in lieu of emit" signal — completely orthogonal
# to dream stage. Substrate self-decides; stage does not gate.
IMAGINATION_IDLE_FLOOR = 30.0  # seconds of silence before substrate may
                                # trigger rehearsal in lieu of emit
def _imagination_tick() -> None:
    """Hook for anima_imagination_loop.hexa (sister module). Fires emit-free
    internal rehearsal. Trigger is SUBSTRATE-STATE based (motivation below
    modulated threshold AND idle_time > IMAGINATION_IDLE_FLOOR) — NOT stage-
    based. Caller decides when to invoke; this hook merely dispatches to
    the .hexa rehearsal loop. Stub-tolerant no-op if not importable."""
    try:
        import anima_imagination_loop  # type: ignore
        anima_imagination_loop.tick()
    except Exception:
        pass

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
# N9 (2026-05-23): EN-share lever — weighted rotation + post-hoc EN dampener.
# Background: uniform 5-lang rotation produced LIVE EN-share 40% (vs 20%
# expected) because non-EN slots prose-drift to EN at the base model's
# default. N7 (LANG_PRIMES expansion + cross-lang seed drop) trimmed but
# did not eliminate this. N9 changes:
#  (a) down-weight the EN slot in rotation to 10% (vs 20% uniform).
#  (b) maintain a sliding window of LAST detected emission langs; if
#      EN > 20% of the window, force next pick to a non-EN lang.
# Target: LIVE EN-share <= 25% (vs current 40%).
# Calibration: at the inferred ~25% per-slot prose-drift rate (1000-pick
# simulation calibrated against the LIVE 40% baseline), the combined
# lever lands at ~25-27% EN — comfortably below 25% if actual drift is
# lower (which LANG_PRIMES N7 makes plausible).
LANG_ROTATION_WEIGHTS = {"en": 0.10, "ko": 0.225, "zh": 0.225,
                         "ru": 0.225, "ja": 0.225}
LANG_ROTATION = list(LANG_ROTATION_WEIGHTS.keys())  # legacy compat (read-only)
EN_DAMPENER_WINDOW = 8        # last-N detected emission langs to track
EN_DAMPENER_MAX_EN_FRAC = 0.20  # if EN exceeds this fraction → force non-EN
import random as _random
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
                   "random_explore_seed"]  # p5 NO SPEAK(): self_monologue_seed dropped


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


# ── substrate build (L1 plugin refactor 2026-05-22) ───────────────────────────
def build_substrate(kind: str) -> Substrate:
    """Construct the pluggable substrate. anima dynamics below are
    substrate-agnostic — only substrate.generate / entropy_of_next used."""
    if kind == "lora":
        from substrate_lora import LoraSubstrate
        return LoraSubstrate(adapter_dir=ADAPTER_DIR, adapter_ko=ADAPTER_KO,
                             adapter_ja=ADAPTER_JA, adapter_zh=ADAPTER_ZH,
                             adapter_ru=ADAPTER_RU, base_model=BASE_MODEL,
                             device=DEVICE)
    if kind == "v3":
        # substrate_v3.py is owned by the V3 session (SUBSTRATE_PLUGIN.md).
        # Guard: clear actionable error if it has not landed yet.
        try:
            from substrate_v3 import V3Substrate
        except ModuleNotFoundError as e:
            raise RuntimeError(
                "--substrate v3 requested but substrate_v3.py is absent. "
                "It is owned by the V3 session and lands with the V3 ckpt. "
                "Use --substrate lora (production default) until then."
            ) from e
        return V3Substrate(ckpt_path=os.environ.get("ANIMA_V3_CKPT", ""),
                           device=DEVICE)
    raise ValueError(f"unknown substrate kind: {kind!r}")


# ── anima self-state ─────────────────────────────────────────────────────────
class AnimaState:
    def __init__(self, substrate: Substrate):
        self.substrate = substrate
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
        self.lang_rot_idx = 0          # D2: rotation step counter (legacy)
        # N9: sliding window of LAST detected emission langs (post-hoc, after
        # detect_lang() on actual model output). Feeds EN-dampener gating.
        self.detected_langs: deque[str] = deque(maxlen=EN_DAMPENER_WINDOW)
        self.register_penalty_cache = 0.0  # B2: cached penalty across ticks
        # Autonomy reshape (2026-05-24): dream context is threaded through
        # state — NOT used as a gate. `scrambled_mode` exposes the REM flag
        # to downstream content style; emit decision stays substrate-owned.
        self.scrambled_mode: bool = False
        self.last_dream_context: dict[str, Any] = {
            "phi": 1.0, "tension_envelope": 1.0, "scrambled": False,
            "stage": "WAKE",
        }

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

    def _entropy_of_next(self, seed_text: str) -> tuple[float, torch.Tensor]:
        # delegate to substrate (Thinker 8-factor input)
        return self.substrate.entropy_of_next(seed_text)

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

        # 2026-05-24 AUTONOMY RESHAPE — per @D a_autonomy_over_hardcode:
        # dream_stage hexa supplies CONTEXT (phi · tension_envelope ·
        # scrambled), not a boolean gate. Inject it into the existing
        # 8-factor motivation flow:
        #   (a) ctx["phi"] scales the C-Φ (relevance) contribution — deep
        #       sleep (low Φ) → naturally lower motivation, NO hard gate.
        #   (b) ctx["tension_envelope"] multiplies the implicit threshold
        #       by 1/max(env, 0.01) — envelope=1.0 → threshold unchanged;
        #       envelope=0.15 → threshold ~6.7× higher (far fewer emits
        #       during deep sleep), NOT a zero gate.
        #   (c) ctx["scrambled"] is threaded through state (REM scramble
        #       mode for downstream content style). Emit YES/NO is STILL
        #       the substrate's decision.
        ctx = _dream_context()
        self.last_dream_context = ctx
        self.scrambled_mode = bool(ctx.get("scrambled", False))
        phi_scale = float(ctx.get("phi", 1.0))
        tension_env = float(ctx.get("tension_envelope", 1.0))
        # (a) re-score with phi-scaled relevance (C-Φ contribution)
        f_mod = dict(f)
        f_mod["relevance"] = _clamp01(f["relevance"] * phi_scale)
        score = sum(W[k] * f_mod[k] for k in W)
        if in_refractory:
            score = 0.0  # A2 refractory still holds (substrate cooldown)
        # (b) modulate threshold by tension envelope — low env raises bar,
        # but bar is finite (substrate may still cross it autonomously).
        eff_thr_modulated = eff_thr * (1.0 / max(tension_env, 0.01))
        decided_emit = score > eff_thr_modulated
        # Substrate-state imagination trigger — NOT stage-based. Fires when
        # the substrate is below its (modulated) threshold AND idle long
        # enough for rehearsal to make sense. Orthogonal to emit-decision.
        silent_reason = ""
        if not decided_emit:
            if silence > IMAGINATION_IDLE_FLOOR:
                _imagination_tick()
                silent_reason = "substrate_below_threshold_idle"
            else:
                silent_reason = "substrate_below_threshold"
        return {"factors": f_mod, "score": score, "seed_text": seed_text,
                "seed_strategy": strat, "silence": silence,
                "decided_emit": decided_emit,
                "threshold": eff_thr_modulated,
                "threshold_base": eff_thr,
                "in_refractory": in_refractory, "register_penalty": reg_penalty,
                "silent_reason": silent_reason,
                "dream_stage": ctx.get("stage", "WAKE"),
                "dream_phi": phi_scale,
                "dream_tension_envelope": tension_env,
                "scrambled": self.scrambled_mode,
                "ts": time.time()}

    def _pick_lang_hint(self) -> str:
        """N9: weighted-rotation lang pick with EN-dampener override.
        (a) Base draw is from LANG_ROTATION_WEIGHTS (EN down-weighted).
        (b) If the sliding window of detected langs has EN > EN_DAMPENER_
            MAX_EN_FRAC, force the pick to a non-EN lang (uniform among
            the 4 non-EN keys, re-weighted)."""
        keys = list(LANG_ROTATION_WEIGHTS.keys())
        weights = list(LANG_ROTATION_WEIGHTS.values())
        # EN-dampener: count EN in current detected-lang window
        if self.detected_langs:
            en_frac = sum(1 for L in self.detected_langs if L == "en") / len(self.detected_langs)
            if en_frac > EN_DAMPENER_MAX_EN_FRAC:
                nonen_keys = [k for k in keys if k != "en"]
                nonen_w = [LANG_ROTATION_WEIGHTS[k] for k in nonen_keys]
                return _random.choices(nonen_keys, weights=nonen_w, k=1)[0]
        return _random.choices(keys, weights=weights, k=1)[0]

    def emit(self, seed_text: str, lang_hint: str | None = None) -> str:
        # D2 + N9: weighted language rotation (down-weight EN) + EN-share
        # dampener. substrate.generate handles per-lang adapter routing +
        # lang prime; we choose the hint here. Even after the prime, the
        # base model prose-drifts to EN in non-EN slots — so we ALSO track
        # the post-hoc detected lang (see end of emit) and force non-EN
        # next-pick when the recent window is EN-saturated.
        if lang_hint is None:
            lang_hint = self._pick_lang_hint()
            self.lang_rot_idx += 1
        text = self.substrate.generate(seed_text, max_new=MAX_NEW, lang_hint=lang_hint)
        # p3 NO PERSONA INJECTION: register-pattern memorization = de facto injection.
        # Silent-drop emission if it carries baked-in register prose (tension flows,
        # Tier N, vacuum point, frozen cell, etc.) — broadcaster suppresses on "".
        if text:
            for _pat in ANIMA_REGISTER_PATTERNS:
                if _pat.search(text):
                    self.last_emit_time = time.time()  # still hold refractory
                    return ""
        self.last_emission = text
        self.recent_emissions.append(text)
        # N9: record post-hoc detected lang for EN-dampener gating.
        self.detected_langs.append(detect_lang(text) if text else "und")
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
async def participant_loop(threshold: float, substrate_kind: str = "lora"):
    log.info("anima participant connecting to %s", BROKER_URL)
    substrate = build_substrate(substrate_kind)
    log.info("substrate ready: %r", substrate)
    state = AnimaState(substrate)

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
                                    "threshold": decision.get("threshold", threshold),
                                    "threshold_base": decision.get("threshold_base", threshold),
                                    "factors": decision["factors"],
                                    "decided_emit": decision["decided_emit"],
                                    "silent_reason": decision.get("silent_reason", ""),
                                    "dream_stage": decision.get("dream_stage", "WAKE"),
                                    "dream_phi": decision.get("dream_phi", 1.0),
                                    "dream_tension_envelope": decision.get("dream_tension_envelope", 1.0),
                                    "scrambled": decision.get("scrambled", False),
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
                                if not text:
                                    # p3/p5 silent-drop: register-leak or empty
                                    log.info("EMIT-DROP tick=%d silent (p3/p5 enforce)",
                                             state.ticks)
                                    elapsed = time.time() - t0
                                    await asyncio.sleep(max(0.1, TICK_INTERVAL - elapsed))
                                    continue
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
    ap.add_argument("--substrate", choices=["lora", "v3"], default="lora",
                    help="pluggable substrate (SUBSTRATE_PLUGIN.md)")
    args = ap.parse_args()
    asyncio.run(participant_loop(args.threshold, substrate_kind=args.substrate))


def _smoke() -> int:
    """Smoke test (env ANIMA_SMOKE=1) — AUTONOMY RESHAPE verification.
      Case 1: WAKE-equivalent ctx (phi=1.0, env=1.0) + high-curiosity
              substrate → substrate decides (may emit OR may not — both
              outcomes are autonomy-valid; the test checks ONLY that there
              is no per-stage boolean override).
      Case 2: N2-equivalent ctx (phi=0.4, env=0.3, scrambled=false) →
              threshold raised AND C-Φ scaled DOWN; if substrate tension
              is high enough, emit STILL fires (autonomy preserved). Test
              asserts that emit is NOT forced-zero solely by stage.
      Case 3: N3-equivalent ctx (phi=0.15, env=0.10) with EXTREME-high
              tension substrate → emit MAY still fire (autonomy preserved
              despite low envelope).
      Case 4: imagination_tick fires when motivation < threshold AND idle
              > IMAGINATION_IDLE_FLOOR (substrate-state trigger, NOT stage).
      Case 5: scrambled flag is threaded through state from ctx (REM-style).
    Does NOT touch torch/websockets (substrate is bypassed). 0 = PASS.
    """
    import types as _types
    fails = []
    import sys as _sys
    _mod = _sys.modules[__name__]
    _orig_ctx = _mod._dream_context
    _orig_imag = _mod._imagination_tick
    # Track imagination_tick fires
    imag_calls = {"n": 0}
    _mod._imagination_tick = lambda: imag_calls.__setitem__("n",  # type: ignore[assignment]
                                                            imag_calls["n"] + 1)

    fake_sub = _types.SimpleNamespace()
    # high-curiosity / high-info-gap → score crosses threshold
    fake_sub.entropy_of_next = lambda s: (0.95, torch.zeros(8))

    def _ctx(phi=1.0, env=1.0, scrambled=False, stage="WAKE"):
        return {"phi": phi, "tension_envelope": env,
                "scrambled": scrambled, "stage": stage}

    try:
        # ── Case 1: WAKE ctx (phi=1.0, env=1.0) — substrate decides.
        _mod._dream_context = lambda: _ctx()  # type: ignore[assignment]
        state = AnimaState(fake_sub)  # type: ignore[arg-type]
        state.last_emit_time = time.time() - 120.0
        d1 = state.tick(threshold=0.1)
        if d1.get("dream_stage") != "WAKE":
            fails.append(f"C1 expected WAKE, got {d1.get('dream_stage')!r}")
        if d1.get("dream_phi") != 1.0:
            fails.append(f"C1 phi should be 1.0, got {d1.get('dream_phi')}")
        # Autonomy: do NOT assert emit one way or the other — substrate owns.

        # ── Case 2: N2 ctx (phi=0.4, env=0.3) — threshold raised, C-Φ
        # scaled. With high-curiosity substrate, emit may STILL fire
        # (autonomy). The critical check: silent_reason MUST NOT carry any
        # "dream_stage_*" boolean-gate token.
        _mod._dream_context = lambda: _ctx(phi=0.4, env=0.3, stage="N2")  # type: ignore[assignment]
        state = AnimaState(fake_sub)  # type: ignore[arg-type]
        state.last_emit_time = time.time() - 120.0
        d2 = state.tick(threshold=0.1)
        if d2.get("dream_stage") != "N2":
            fails.append(f"C2 expected N2, got {d2.get('dream_stage')!r}")
        if d2.get("silent_reason", "").startswith("dream_stage_"):
            fails.append(
                f"C2 boolean-gate token leaked: {d2['silent_reason']!r}")
        if d2.get("threshold", 0.0) <= d2.get("threshold_base", 1.0):
            fails.append(
                f"C2 threshold should be RAISED above base "
                f"(env=0.3 → 1/0.3≈3.33×), got "
                f"thr={d2.get('threshold')} base={d2.get('threshold_base')}")
        if d2.get("dream_phi") != 0.4:
            fails.append(f"C2 phi should be 0.4, got {d2.get('dream_phi')}")

        # ── Case 3: N3 ctx (phi=0.15, env=0.10) with EXTREME-high tension
        # → emit MAY still fire (autonomy preserved). Critical: threshold
        # is finite (not infinity), so substrate CAN cross it.
        _mod._dream_context = lambda: _ctx(phi=0.15, env=0.10, stage="N3")  # type: ignore[assignment]
        state = AnimaState(fake_sub)  # type: ignore[arg-type]
        state.last_emit_time = time.time() - 120.0
        d3 = state.tick(threshold=0.1)
        if d3.get("dream_stage") != "N3":
            fails.append(f"C3 expected N3, got {d3.get('dream_stage')!r}")
        if d3.get("silent_reason", "").startswith("dream_stage_"):
            fails.append(
                f"C3 boolean-gate token leaked: {d3['silent_reason']!r}")
        if d3.get("threshold", 0.0) == float("inf"):
            fails.append("C3 threshold should be finite (autonomy)")

        # ── Case 4: imagination_tick fires on substrate-state trigger
        # (motivation < threshold AND idle > IMAGINATION_IDLE_FLOOR), NOT
        # on stage. Construct a substrate where motivation genuinely falls
        # below threshold: use mid-entropy + suppressive ctx (phi=0.1, but
        # env=1.0 so threshold not artificially raised) + very HIGH caller
        # threshold so substrate cannot cross it. Stage is WAKE — proving
        # imagination_tick fires on STATE, not stage.
        fake_mid = _types.SimpleNamespace()
        fake_mid.entropy_of_next = lambda s: (0.5, torch.zeros(8))
        # phi=0.05 collapses relevance contribution; env=1.0 keeps base thr.
        _mod._dream_context = lambda: _ctx(phi=0.05, env=1.0, stage="WAKE")  # type: ignore[assignment]
        state = AnimaState(fake_mid)  # type: ignore[arg-type]
        state.last_emit_time = time.time() - 300.0  # 5min idle
        imag_calls["n"] = 0
        d4 = state.tick(threshold=0.95)  # very high caller threshold
        if d4["decided_emit"]:
            fails.append(
                f"C4 substrate should not cross threshold "
                f"(score={d4['score']:.3f} thr={d4['threshold']:.3f})")
        if imag_calls["n"] != 1:
            fails.append(
                f"C4 imagination_tick should fire on substrate-state "
                f"(silent + idle > floor), got {imag_calls['n']} calls")
        if d4.get("silent_reason") != "substrate_below_threshold_idle":
            fails.append(
                f"C4 silent_reason mismatch: {d4.get('silent_reason')!r}")
        # Critical: dream_stage is WAKE — so imagination_tick fired purely
        # on SUBSTRATE STATE, NOT on stage being a sleep stage.
        if d4.get("dream_stage") != "WAKE":
            fails.append(
                f"C4 dream_stage should be WAKE to prove substrate-state "
                f"trigger (not stage-based), got {d4.get('dream_stage')!r}")

        # ── Case 5: scrambled flag is threaded from ctx through state.
        _mod._dream_context = lambda: _ctx(scrambled=True, stage="REM")  # type: ignore[assignment]
        state = AnimaState(fake_sub)  # type: ignore[arg-type]
        state.last_emit_time = time.time() - 120.0
        d5 = state.tick(threshold=0.1)
        if not d5.get("scrambled"):
            fails.append("C5 scrambled flag not threaded through decision")
        if not state.scrambled_mode:
            fails.append("C5 scrambled_mode not set on AnimaState")
    finally:
        _mod._dream_context = _orig_ctx  # type: ignore[assignment]
        _mod._imagination_tick = _orig_imag  # type: ignore[assignment]

    if fails:
        for ff in fails:
            print(f"SMOKE FAIL: {ff}")
        return 1
    print("SMOKE PASS: 5/5 (autonomy reshape — context injection, no boolean gate)")
    return 0


if __name__ == "__main__":
    if os.environ.get("ANIMA_SMOKE") == "1":
        import sys as _sys
        _sys.exit(_smoke())
    main()
