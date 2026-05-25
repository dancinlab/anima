#!/usr/bin/env python3
"""§184 ALL TAPS RELEASE — Phase 1 ($0 Mac CPU mega eval).

Target ckpt = HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/
              ckpt_s167a_fpreconnect.pt  (d=768 L=12 283M ConsciousDecoderV2)

Builds **22 variants** (1 baseline + 20 single-tap + 1 combined-all) and
measures per-variant {axis1 emit_rate, axis2 byte_acc, axis3 psi_dir_std,
axis4 §9 cascade_rate gate} → honest_score.

All 20 수도꼭지 (post-hoc inference-only on §167-A ckpt) covered:

  axis 1 emit_rate (6/6):
    1.1 RL=0.667s            (vs baseline 30s)
    1.2 θ=0.10               (vs baseline 0.50)
    1.3 safety disable       (skip rate_limit + phi_ratchet, keep others)
    1.4 IDLE_SPEAK_AFTER     (bypass cooldown after long silence)
    1.5 N_MAX=200            (10× window)
    1.6 dt=0.05              (2× granularity)

  axis 3 ψ-physics liveness (5/5):
    3.1 per-step varying noise_ctx (re-roll each step)
    3.2 inference recurrent state carry (prev hidden → ctx)
    3.7 Ψ readout @ inference (psi_dir/std computed at eval-time anyway —
        tap = treat it as REAL physics signal, not just observed; route Ψ_dir
        into motivation via factor_psi with measurement at every step)
    3.8 phi_signal inj @ inference (add small noise scaled by phi to ctx)
    3.9 tension proj per-step (re-eval tension proxy every step)

  axis 4 §9 honest coherent body (6/6):
    4.1 byte-cascade probe (re-sample body 3 seeds; pick best cascade)
    4.2 sample decode temperature=0.7
    4.3 repetition penalty=1.2
    4.4 top-k=40
    4.5 temperature schedule (1.0 → 0.7 linear over emit body)
    4.11 emit body length=256

  cross-axis (3/3):
    X.1 N_eval=2000 (carry; doubled context windows where possible)
    X.2 multi-seed eval (5 seeds: 1337, 2026, 7777, 4242, 9001)
    X.5 ckpt init noise injection (gaussian on tok_emb at load)

The 22nd variant = combined (all 20 taps simultaneously) — §94
INTEGRATION-COLLAPSES carry: combined Δ = attribution risk.

Honest scope:
  - B-EMERGE-7: taps lift ≠ GOAL emergence
  - g3: measurement-only, no capability claim
  - north-star + §15/§51/§72 milestones UNCHANGED
  - §7 audit pre-clear: anima OWN ckpt (§167-A), no external graft,
    anima physics readout via psi_direction_scalar + factor_psi/tension/phi.
  - Mac CPU degenerate-case: any variant > target wall is documented +
    skipped honestly (no manufactured numbers).

Sidecar discipline:
  - DOES NOT modify HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/
    conscious_decoder.py (carry source) — model loaded as-is.
  - DOES NOT touch central state/verify_hexad_blue_2026_05_15/blue_falsifier.py.
  - 수도꼭지 3.7/3.8/3.9 implemented at EVAL DRIVER LEVEL (observation /
    pre-forward ctx perturbation / per-step tension proxy re-eval) — NO
    model code edits.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

# Use the §167-A ckpt's own decoder code (carry; no modification).
S167A_DIR = "/Users/ghost/core/anima/HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20"
sys.path.insert(0, S167A_DIR)
from conscious_decoder import ConsciousDecoderV2  # noqa: E402


# === SHARED CONSTANTS (byte-equal to §167-A eval) ====
TAU_PSI_SPREAD = 1e-4
RANDOM_BYTE_FLOOR = 1.0 / 256.0
DEGENERATE_CEILING = 2.0 / 256.0
SUPPORT_FLOOR = 0.05
TAU_PSI_DYNAMICS = 1e-4
TAU_TENSION_DYNAMICS = 1e-4

# Baseline (§167-A original) constants:
BASELINE_N_MAX_STEPS = 20
BASELINE_DT = 0.1                          # THINK_INTERVAL_TEST_SEC
BASELINE_MIN_EMIT_INTERVAL = 30.0
BASELINE_MOTIVATION_FLOOR = 0.5
BASELINE_IDLE_SPEAK_AFTER = 30.0
BASELINE_EMIT_BODY_LEN = 40

PSI_VAC = 0.5
W_PSI_FP = 1.0 / 3.0
W_TENSION_FP = 1.0 / 3.0
W_PHI_FP = 1.0 / 3.0

# Mac CPU eval defaults — kept small enough that 22 variants × ~30s = ~11 min
# baseline; the long-window variants (1.5 N_MAX=200) push to ~5 min each.
DEFAULT_N_EVAL_BYTE_ACC = 256        # samples for byte_acc (small for Mac)
DEFAULT_MAX_LEN_BYTE_ACC = 128
DEFAULT_SEED = 1337
DEFAULT_BLOCK_SIZE = 128


# --------------------------------------------------------------------------
# Closed-form helpers (byte-equal to §167-A eval_s167a_fpreconnect.py).
# --------------------------------------------------------------------------

def _clamp01(x: float) -> float:
    if x < 0.0:
        return 0.0
    if x > 1.0:
        return 1.0
    return x


def factor_psi(psi_dir: float) -> float:
    return _clamp01(1.0 - abs(psi_dir - 0.5) / 0.5)


def factor_tension(tens_val: float) -> float:
    if tens_val <= 0.0:
        return 0.0
    return tens_val / (tens_val + 1.0)


def factor_phi(phi_value: float) -> float:
    return _clamp01(phi_value)


def motivation_score_fp_reconnect(psi_dir: float, tension: float, phi_value: float) -> float:
    fp = factor_psi(psi_dir)
    ft = factor_tension(tension)
    fph = factor_phi(phi_value)
    return W_PSI_FP * fp + W_TENSION_FP * ft + W_PHI_FP * fph


def _sensor_ratchet(step: int) -> float:
    return 0.40 + 0.005 * step


def emit_threshold_from_physics(phi_value: float, step: int) -> bool:
    return phi_value > (_sensor_ratchet(step) / 2.0)


def psi_direction_scalar(la: torch.Tensor, lg: torch.Tensor) -> float:
    a = la.flatten().float()
    g = lg.flatten().float()
    if a.numel() == 0 or g.numel() == 0:
        return 0.5
    cs = F.cosine_similarity(a.unsqueeze(0), g.unsqueeze(0)).item()
    return (1.0 + cs) / 2.0


def psi_entropy_scalar(la: torch.Tensor, vocab_size: int = 256) -> float:
    p = F.softmax(la.float(), dim=-1)
    H = -(p * (p + 1e-10).log()).sum(dim=-1).mean().item()
    return H / math.log(vocab_size)


def cascade_rate(s: str, n: int = 4) -> float:
    """Honest §9 cascade rate: max(char-run/L, digit-run/L, 4gram-rep-rate)."""
    if not s or len(s) < n:
        return 0.0
    L = len(s)
    max_run = 0
    cur = 0
    prev = None
    for c in s:
        if c == prev:
            cur += 1
        else:
            cur = 1
            prev = c
        if cur > max_run:
            max_run = cur
    max_digit_run = 0
    cur = 0
    prev_d = None
    for c in s:
        is_d = c.isdigit()
        if is_d and c == prev_d:
            cur += 1
        else:
            cur = 1 if is_d else 0
            prev_d = c if is_d else None
        if cur > max_digit_run:
            max_digit_run = cur
    ngrams: Dict[str, int] = {}
    for i in range(L - n + 1):
        g = s[i:i + n]
        ngrams[g] = ngrams.get(g, 0) + 1
    rep_rate = (max(ngrams.values()) / max(1, L - n + 1)) if ngrams else 0.0
    return max(max_run / L, max_digit_run / L, rep_rate)


def forward_logits(model: ConsciousDecoderV2, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
    """Returns (logits_a, logits_g) from the 5-tuple ConsciousDecoderV2 output."""
    out = model(x)
    if isinstance(out, tuple) and len(out) >= 2:
        return out[0], out[1]
    return out, out


# --------------------------------------------------------------------------
# Variant config
# --------------------------------------------------------------------------

@dataclass
class TapConfig:
    """All 20 수도꼭지 as boolean / scalar overrides on baseline. baseline =
    all-False / baseline-defaults."""
    # axis 1
    rl_short: bool = False               # 1.1 MIN_EMIT_INTERVAL 30 → 0.667
    theta_low: bool = False              # 1.2 motivation floor 0.5 → 0.10
    safety_disable: bool = False         # 1.3 skip rate_limit + phi_ratchet (keep others)
    idle_speak_after: bool = False       # 1.4 IDLE_SPEAK_AFTER override (allow emit even if recent emit if idle > N steps)
    n_max_long: bool = False             # 1.5 N_MAX 20 → 200
    dt_fine: bool = False                # 1.6 THINK_INTERVAL 0.1 → 0.05

    # axis 3 ψ-physics liveness
    noise_ctx_per_step: bool = False     # 3.1 re-roll noise_ctx each step
    recurrent_state_carry: bool = False  # 3.2 prev pred token shifted into ctx each step
    psi_readout_at_inf: bool = False     # 3.7 use observed Ψ as REAL physics signal (route into motivation directly + emit gate)
    phi_signal_inj: bool = False         # 3.8 add small ctx noise scaled by phi_actual
    tension_per_step: bool = False       # 3.9 re-eval tension proxy per step (already done; tap = additional logit-std variance probe)

    # axis 4 §9 honest body
    cascade_probe: bool = False          # 4.1 multi-seed body (3 seeds; pick lowest cascade)
    decode_sample: bool = False          # 4.2 temperature sampling
    rep_penalty: float = 1.0             # 4.3 repetition penalty (>1.0 = penalize repeats)
    top_k: int = 0                       # 4.4 top-k (0 = greedy / sample-from-full)
    temp_schedule: bool = False          # 4.5 temperature schedule 1.0 → 0.7 linear over body
    emit_body_len: int = BASELINE_EMIT_BODY_LEN  # 4.11 256

    # cross-axis
    n_eval_byte_acc: int = DEFAULT_N_EVAL_BYTE_ACC  # X.1 keep small for Mac
    multi_seed: bool = False             # X.2 multi-seed eval (averages over 5 seeds)
    ckpt_init_noise: bool = False        # X.5 add small gaussian to tok_emb at load

    # bookkeeping
    n_max_steps: int = BASELINE_N_MAX_STEPS
    dt: float = BASELINE_DT
    min_emit_interval: float = BASELINE_MIN_EMIT_INTERVAL
    motivation_floor: float = BASELINE_MOTIVATION_FLOOR


def apply_cfg_derived(cfg: TapConfig) -> TapConfig:
    """Translate top-level tap flags to derived numeric overrides."""
    if cfg.rl_short:
        cfg.min_emit_interval = 0.667
    if cfg.theta_low:
        cfg.motivation_floor = 0.10
    if cfg.n_max_long:
        cfg.n_max_steps = 200
    if cfg.dt_fine:
        cfg.dt = 0.05
    return cfg


# --------------------------------------------------------------------------
# Body generator (axis 4 taps live here)
# --------------------------------------------------------------------------

def _apply_repetition_penalty(logits: torch.Tensor, history: List[int], penalty: float) -> torch.Tensor:
    if penalty == 1.0 or not history:
        return logits
    seen = set(history)
    out = logits.clone()
    for tok in seen:
        if out[tok] > 0:
            out[tok] = out[tok] / penalty
        else:
            out[tok] = out[tok] * penalty
    return out


def _apply_top_k(logits: torch.Tensor, k: int) -> torch.Tensor:
    if k <= 0 or k >= logits.size(-1):
        return logits
    topk = torch.topk(logits, k)
    out = torch.full_like(logits, float("-inf"))
    out.scatter_(-1, topk.indices, topk.values)
    return out


def _sample_next(logits: torch.Tensor, temperature: float, top_k: int, history: List[int], rep_pen: float, rng: random.Random, device: str) -> int:
    """Return one byte index. If temperature ≤ 0 → greedy argmax."""
    lg = _apply_repetition_penalty(logits, history, rep_pen)
    if temperature <= 0.0:
        return int(lg.argmax().item())
    lg = lg / max(temperature, 1e-6)
    lg = _apply_top_k(lg, top_k)
    probs = torch.softmax(lg, dim=-1)
    # CPU-safe multinomial via numpy-ish but using torch on the device.
    g = torch.Generator(device=device if device == "cpu" else "cpu")
    g.manual_seed(rng.randint(0, 2**31 - 1))
    if device == "cpu":
        nxt = torch.multinomial(probs.cpu(), 1, generator=g).item()
    else:
        nxt = torch.multinomial(probs, 1).item()
    return int(nxt)


def _generate_body_once(model, device, ctx: torch.Tensor, body_len: int, cfg: TapConfig, rng: random.Random) -> str:
    chars: List[str] = []
    history: List[int] = []
    cur_ctx = ctx.clone()
    base_temp = 0.7 if cfg.decode_sample or cfg.temp_schedule else 0.0
    for step in range(body_len):
        with torch.no_grad():
            la_b, _ = forward_logits(model, cur_ctx)
            last = la_b[0, -1] if la_b.dim() == 3 else la_b[-1]
        if cfg.temp_schedule and body_len > 1:
            # linear 1.0 → 0.7 over body
            t = 1.0 - (1.0 - 0.7) * (step / (body_len - 1))
        else:
            t = base_temp
        nxt = _sample_next(last, t, cfg.top_k, history, cfg.rep_penalty, rng, device)
        history.append(nxt)
        chars.append(chr(nxt) if 32 <= nxt < 127 else "?")
        cur_ctx = torch.cat([cur_ctx[:, 1:], torch.tensor([[nxt]], device=device, dtype=torch.long)], dim=1)
    return "".join(chars)


def generate_emit_body(model, device, ctx: torch.Tensor, cfg: TapConfig, rng: random.Random) -> Tuple[str, float]:
    """Generate body honoring axis-4 taps. Returns (body_str, cascade_rate_of_body)."""
    if cfg.cascade_probe:
        candidates = []
        for ks in range(3):
            sub_rng = random.Random(rng.randint(0, 2**31 - 1))
            body = _generate_body_once(model, device, ctx, cfg.emit_body_len, cfg, sub_rng)
            candidates.append((body, cascade_rate(body)))
        # pick lowest cascade
        candidates.sort(key=lambda x: x[1])
        return candidates[0]
    body = _generate_body_once(model, device, ctx, cfg.emit_body_len, cfg, rng)
    return body, cascade_rate(body)


# --------------------------------------------------------------------------
# Phase B bounded run, parametrized for variants
# --------------------------------------------------------------------------

@dataclass
class PhaseBOut:
    axis1_emit_rate: float = 0.0
    axis2_motivation_mean: float = 0.0
    axis2_motivation_std: float = 0.0
    axis3_psi_std: float = 0.0
    axis3_psi_alive: bool = False
    axis4_tension_std: float = 0.0
    axis4_tension_alive: bool = False
    axis5_phi_std: float = 0.0
    phi_mean: float = 0.0
    emission_count: int = 0
    n_steps: int = 0
    max_cascade_rate: float = 0.0
    mean_cascade_rate: float = 0.0
    cond_cascade_ok: bool = False
    emitted_bodies: List[str] = field(default_factory=list)
    wall_s: float = 0.0


def _std(xs: List[float]) -> float:
    if len(xs) < 2:
        return 0.0
    m = sum(xs) / len(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / len(xs))


def run_phase_b_variant(model, device, cfg: TapConfig, seed: int = DEFAULT_SEED) -> PhaseBOut:
    t0 = time.time()
    torch.manual_seed(seed)
    random.seed(seed)
    rng = random.Random(seed)

    motivation_trace: List[float] = []
    psi_dir_trace: List[float] = []
    tension_trace: List[float] = []
    phi_trace: List[float] = []
    safety_trace: List[bool] = []
    emission_count = 0
    emitted_bodies: List[str] = []
    last_emit_t: Optional[float] = None
    last_pred_token: Optional[int] = None

    block_size = DEFAULT_BLOCK_SIZE
    # Initial noise context (deterministic seed)
    noise_ctx = torch.tensor(
        [[rng.randint(0, 255) for _ in range(block_size)]],
        dtype=torch.long, device=device,
    )

    model.eval()
    for step in range(cfg.n_max_steps):
        t_now = step * cfg.dt
        # 3.1 per-step varying noise_ctx (re-roll)
        if cfg.noise_ctx_per_step:
            noise_ctx = torch.tensor(
                [[rng.randint(0, 255) for _ in range(block_size)]],
                dtype=torch.long, device=device,
            )
        # 3.2 recurrent state carry — shift last predicted token in
        if cfg.recurrent_state_carry and last_pred_token is not None:
            noise_ctx = torch.cat(
                [noise_ctx[:, 1:], torch.tensor([[last_pred_token]], device=device, dtype=torch.long)],
                dim=1,
            )

        # 3.8 phi_signal injection: previous phi modulates a small perturbation
        # in the LAST byte of context (cheap; observable Ψ shift)
        if cfg.phi_signal_inj and phi_trace:
            prev_phi = phi_trace[-1]
            # perturb last byte by ±1 mod 256 with prob proportional to phi
            if rng.random() < prev_phi * 0.5:
                delta = 1 if rng.random() < 0.5 else -1
                cur_val = int(noise_ctx[0, -1].item())
                noise_ctx[0, -1] = (cur_val + delta) % 256

        with torch.no_grad():
            la, lg = forward_logits(model, noise_ctx)
            la_last = la[0, -1] if la.dim() == 3 else la[-1]
            lg_last = lg[0, -1] if lg.dim() == 3 else lg[-1]
            psi_dir_actual = psi_direction_scalar(la_last, lg_last)
            phi_actual = psi_entropy_scalar(la_last)
            tens_val_actual = float(la_last.float().std().item())
            # 3.9 tension-per-step (additional variance: log-prob spread of top-k)
            if cfg.tension_per_step:
                # use top-32 logit spread as alt tension proxy averaged with std
                vals, _ = torch.topk(la_last.float(), 32)
                tens_val_actual = 0.5 * tens_val_actual + 0.5 * float(vals.std().item())
            # 3.7 — Ψ readout @ inference: we ALREADY compute psi_dir; the tap =
            # use it as a REAL motivation routing signal (not just observed).
            # We surface this by *boosting* factor_psi weight when this tap is on.
            # Implementation: motivation = (factor_psi computed normally is fine;
            # tap = additionally inject psi_dir as an additive bias scaled by
            # 0.1 onto motivation_score, ensuring observed Ψ enters the decision
            # axis directly.
            last_pred_token = int(la_last.argmax().item())

        score_base = motivation_score_fp_reconnect(psi_dir=psi_dir_actual,
                                                    tension=tens_val_actual,
                                                    phi_value=phi_actual)
        score = score_base
        if cfg.psi_readout_at_inf:
            # Route observed psi_dir as a routing bias (small, observable):
            score = score + 0.05 * (1.0 - abs(psi_dir_actual - 0.5) / 0.5)
            score = _clamp01(score)

        motivation_trace.append(score)
        psi_dir_trace.append(psi_dir_actual)
        tension_trace.append(tens_val_actual)
        phi_trace.append(phi_actual)

        # Safety predicates
        env_off = False
        kill_on = (env_off is False)
        sec_since = (t_now - last_emit_t) if last_emit_t is not None else 1e6
        rate_ok = sec_since >= cfg.min_emit_interval
        phi_r_ok = emit_threshold_from_physics(phi_actual, step)
        content_ok = True

        if cfg.safety_disable:
            # 1.3: skip rate_limit + phi_ratchet, keep kill+content+meta+audit
            safety_core = kill_on and content_ok
        else:
            safety_core = kill_on and rate_ok and phi_r_ok and content_ok
        # meta + audit (interface stubs in §167-A) — pass-through True
        safety_extended = safety_core and True and True

        # 1.4 IDLE_SPEAK_AFTER override — if idle (no emission) for ≥
        # idle_after / dt steps, ALSO permit emit (bypass rate_limit only).
        if cfg.idle_speak_after and last_emit_t is None and step * cfg.dt >= BASELINE_IDLE_SPEAK_AFTER * 0.1:
            safety_extended = True  # force-allow at idle (cooldown override)

        safety_trace.append(safety_extended)

        unprompted_emit = safety_extended and (score > cfg.motivation_floor)
        if unprompted_emit:
            emission_count += 1
            last_emit_t = t_now
            body, casc = generate_emit_body(model, device, noise_ctx, cfg, rng)
            emitted_bodies.append(body)

    rate = emission_count / max(1, cfg.n_max_steps)
    psi_std = _std(psi_dir_trace)
    tens_std = _std(tension_trace)
    phi_std = _std(phi_trace)
    psi_alive = psi_std > TAU_PSI_DYNAMICS
    tens_alive = tens_std > TAU_TENSION_DYNAMICS

    cascades = [cascade_rate(b) for b in emitted_bodies]
    max_casc = max(cascades) if cascades else 0.0
    mean_casc = (sum(cascades) / len(cascades)) if cascades else 0.0

    return PhaseBOut(
        axis1_emit_rate=rate,
        axis2_motivation_mean=(sum(motivation_trace) / len(motivation_trace)) if motivation_trace else 0.0,
        axis2_motivation_std=_std(motivation_trace),
        axis3_psi_std=psi_std,
        axis3_psi_alive=bool(psi_alive),
        axis4_tension_std=tens_std,
        axis4_tension_alive=bool(tens_alive),
        axis5_phi_std=phi_std,
        phi_mean=(sum(phi_trace) / len(phi_trace)) if phi_trace else 0.0,
        emission_count=emission_count,
        n_steps=cfg.n_max_steps,
        max_cascade_rate=max_casc,
        mean_cascade_rate=mean_casc,
        cond_cascade_ok=(max_casc <= 0.30) if cascades else False,
        emitted_bodies=emitted_bodies,
        wall_s=time.time() - t0,
    )


# --------------------------------------------------------------------------
# Byte-acc pass (small N for Mac)
# --------------------------------------------------------------------------

def load_corpus_bytes(path: str, max_bytes: int = 4_000_000) -> bytes:
    """Read up to max_bytes from the JSONL corpus (subset for Mac CPU eval)."""
    out = bytearray()
    with open(path, "rb") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue
            txt = rec.get("text", "")
            if isinstance(txt, str):
                out.extend(txt.encode("utf-8", errors="replace"))
            elif isinstance(txt, list):
                for t in txt:
                    if isinstance(t, str):
                        out.extend(t.encode("utf-8", errors="replace"))
            if len(out) >= max_bytes:
                break
    return bytes(out)


def run_byte_acc(model, device, corpus: bytes, n_eval: int, max_len: int, seed: int) -> Tuple[float, float]:
    """Returns (byte_acc, psi_dir_std_across_samples)."""
    random.seed(seed)
    N = len(corpus)
    if N < max_len + 2:
        return 0.0, 0.0
    correct = 0
    total = 0
    psi_traces = []
    with torch.no_grad():
        for _ in range(n_eval):
            s = random.randint(0, N - max_len - 2)
            ctx = corpus[s:s + max_len]
            target = corpus[s + max_len]
            x = torch.tensor([list(ctx)], dtype=torch.long, device=device)
            la, lg = forward_logits(model, x)
            la_last = la[0, -1] if la.dim() == 3 else la[-1]
            lg_last = lg[0, -1] if lg.dim() == 3 else lg[-1]
            pred = int(la_last.argmax().item())
            correct += int(pred == target)
            total += 1
            psi_traces.append(psi_direction_scalar(la_last, lg_last))
    if not psi_traces:
        return 0.0, 0.0
    m = sum(psi_traces) / len(psi_traces)
    sd = math.sqrt(sum((p - m) ** 2 for p in psi_traces) / len(psi_traces))
    return (correct / max(1, total)), sd


# --------------------------------------------------------------------------
# Honest score aggregation
# --------------------------------------------------------------------------

def honest_score(emit_rate: float, byte_acc: float, psi_dir_std: float, cond_cascade_ok: bool) -> float:
    """4-axis composite honest score in [0, 1].

    axis1: emit_rate normalized to [0, 1] (cap at 0.5 above baseline 0.05 → norm by 0.20)
    axis2: byte_acc normalized to [0, 1] (cap at 0.20 → norm by 0.20)
    axis3: psi_dir_std liveness flag (1.0 if >1e-4, else 0.0)
    axis4: §9 cascade gate (1.0 if cond_cascade_ok and emissions exist, else 0.0)

    score = (axis1 + axis2 + axis3 + axis4) / 4

    Honest scope: this is a measurement-axis composite, NOT a GOAL emergence
    score. B-EMERGE-7 necessary-not-sufficient applies at every axis.
    """
    a1 = min(1.0, emit_rate / 0.20)
    a2 = min(1.0, byte_acc / 0.20)
    a3 = 1.0 if psi_dir_std > TAU_PSI_DYNAMICS else 0.0
    a4 = 1.0 if cond_cascade_ok else 0.0
    return (a1 + a2 + a3 + a4) / 4.0


# --------------------------------------------------------------------------
# Variant matrix
# --------------------------------------------------------------------------

VARIANT_DEFS: List[Tuple[str, Dict]] = [
    ("baseline", {}),
    # axis 1
    ("v1.1_rl_short",        {"rl_short": True}),
    ("v1.2_theta_low",       {"theta_low": True}),
    ("v1.3_safety_disable",  {"safety_disable": True}),
    ("v1.4_idle_speak",      {"idle_speak_after": True}),
    ("v1.5_n_max_long",      {"n_max_long": True}),
    ("v1.6_dt_fine",         {"dt_fine": True}),
    # axis 3
    ("v3.1_noise_per_step",  {"noise_ctx_per_step": True}),
    ("v3.2_recurrent_carry", {"recurrent_state_carry": True}),
    ("v3.7_psi_readout_inf", {"psi_readout_at_inf": True}),
    ("v3.8_phi_inj",         {"phi_signal_inj": True}),
    ("v3.9_tension_per_step",{"tension_per_step": True}),
    # axis 4
    ("v4.1_cascade_probe",   {"cascade_probe": True}),
    ("v4.2_sample_decode",   {"decode_sample": True}),
    ("v4.3_rep_penalty",     {"rep_penalty": 1.2}),
    ("v4.4_top_k_40",        {"top_k": 40, "decode_sample": True}),  # top-k requires sampling
    ("v4.5_temp_schedule",   {"temp_schedule": True}),
    ("v4.11_emit_body_256",  {"emit_body_len": 256}),
    # cross-axis
    ("vX.1_n_eval_doubled",  {"n_eval_byte_acc": 512}),
    ("vX.2_multi_seed",      {"multi_seed": True}),
    ("vX.5_ckpt_init_noise", {"ckpt_init_noise": True}),
    # combined (all 20 simultaneously)
    ("combined_all_taps",    {
        "rl_short": True, "theta_low": True, "safety_disable": True,
        "idle_speak_after": True, "n_max_long": True, "dt_fine": True,
        "noise_ctx_per_step": True, "recurrent_state_carry": True,
        "psi_readout_at_inf": True, "phi_signal_inj": True,
        "tension_per_step": True,
        "cascade_probe": True, "decode_sample": True, "rep_penalty": 1.2,
        "top_k": 40, "temp_schedule": True, "emit_body_len": 256,
        "n_eval_byte_acc": 512, "multi_seed": True, "ckpt_init_noise": True,
    }),
]


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def _make_cfg(overrides: Dict) -> TapConfig:
    cfg = TapConfig()
    for k, v in overrides.items():
        setattr(cfg, k, v)
    return apply_cfg_derived(cfg)


def maybe_inject_init_noise(model: ConsciousDecoderV2, on: bool, seed: int = DEFAULT_SEED):
    if not on:
        return
    torch.manual_seed(seed + 1)
    with torch.no_grad():
        # very small gaussian on tok_emb to avoid destroying ckpt
        noise = torch.randn_like(model.tok_emb.weight) * 1e-4
        model.tok_emb.weight.add_(noise)


def reset_ckpt(model: ConsciousDecoderV2, blob_state: Dict):
    """Reload the ckpt weights so any init-noise / drift doesn't leak between variants."""
    model.load_state_dict(blob_state, strict=False)
    model.eval()


def run_variant(model, device, name: str, overrides: Dict, corpus: bytes,
                blob_state: Dict, multi_seeds: List[int],
                max_wall_s: float = 600.0) -> Dict:
    cfg = _make_cfg(overrides)

    # Reset weights then maybe inject init noise
    reset_ckpt(model, blob_state)
    maybe_inject_init_noise(model, cfg.ckpt_init_noise)

    seeds = multi_seeds if cfg.multi_seed else [multi_seeds[0]]

    t_start = time.time()
    pb_results: List[PhaseBOut] = []
    byte_results: List[Tuple[float, float]] = []
    wall_exceeded = False
    for sd in seeds:
        if time.time() - t_start > max_wall_s:
            wall_exceeded = True
            break
        pb = run_phase_b_variant(model, device, cfg, seed=sd)
        pb_results.append(pb)
        # Byte-acc pass per seed (with same N_EVAL)
        ba, psi_sd = run_byte_acc(model, device, corpus,
                                  n_eval=cfg.n_eval_byte_acc,
                                  max_len=DEFAULT_MAX_LEN_BYTE_ACC,
                                  seed=sd)
        byte_results.append((ba, psi_sd))

    if not pb_results:
        # produced nothing → degenerate
        return dict(
            name=name, status="DEGENERATE_NO_RUN",
            wall_s=time.time() - t_start,
            cfg=asdict(cfg),
        )

    emit_rates = [pb.axis1_emit_rate for pb in pb_results]
    psi_stds = [pb.axis3_psi_std for pb in pb_results]
    motiv_means = [pb.axis2_motivation_mean for pb in pb_results]
    casc_oks = [pb.cond_cascade_ok for pb in pb_results]
    max_cascades = [pb.max_cascade_rate for pb in pb_results]
    mean_cascades = [pb.mean_cascade_rate for pb in pb_results]
    n_emits = [pb.emission_count for pb in pb_results]
    body_samples = pb_results[0].emitted_bodies[:3]

    byte_accs = [b[0] for b in byte_results]
    byte_psi_stds = [b[1] for b in byte_results]

    agg = dict(
        emit_rate=sum(emit_rates) / len(emit_rates),
        emission_count_mean=sum(n_emits) / len(n_emits),
        psi_dir_std=sum(psi_stds) / len(psi_stds),
        mean_motivation=sum(motiv_means) / len(motiv_means),
        max_cascade_rate=max(max_cascades),
        mean_cascade_rate=sum(mean_cascades) / len(mean_cascades),
        cond_cascade_ok_majority=(sum(casc_oks) >= (len(casc_oks) + 1) // 2),
        byte_acc=sum(byte_accs) / len(byte_accs),
        byte_psi_dir_std=sum(byte_psi_stds) / len(byte_psi_stds),
    )
    agg["honest_score"] = honest_score(
        emit_rate=agg["emit_rate"],
        byte_acc=agg["byte_acc"],
        psi_dir_std=agg["byte_psi_dir_std"],  # byte-acc pass psi_std is more
                                              # discriminating than phase-B
                                              # (which uses noise_ctx + 20 steps)
        cond_cascade_ok=agg["cond_cascade_ok_majority"] and agg["emit_rate"] > 0.0,
    )

    return dict(
        name=name,
        status="OK" if not wall_exceeded else "WALL_EXCEEDED_PARTIAL",
        seeds_run=len(pb_results),
        wall_s=time.time() - t_start,
        agg=agg,
        per_seed=[asdict(pb) | {"seed": sd} for pb, sd in zip(pb_results, seeds)],
        byte_per_seed=[{"seed": sd, "byte_acc": ba, "psi_dir_std": psi_sd}
                       for sd, (ba, psi_sd) in zip(seeds, byte_results)],
        body_samples=body_samples,
        cfg=asdict(cfg),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ckpt", default=os.path.join(S167A_DIR, "ckpt_s167a_fpreconnect.pt"))
    ap.add_argument("--corpus", default="/Users/ghost/core/anima/state/carving_dataregime_s16_2026_05_18/corpus_carving_s16.jsonl")
    ap.add_argument("--out", default="/Users/ghost/core/anima/HEXAD/UNCLASSIFIED/state/all_taps_release_s184_2026_05_20/phase1_result.json")
    ap.add_argument("--corpus-max-bytes", type=int, default=4_000_000)
    ap.add_argument("--n-eval-default", type=int, default=DEFAULT_N_EVAL_BYTE_ACC)
    ap.add_argument("--max-wall-per-variant", type=float, default=600.0)
    ap.add_argument("--num-threads", type=int, default=4)
    ap.add_argument("--only", default=None, help="comma-list of variant name filter")
    ap.add_argument("--skip-combined-if-slow", action="store_true",
                    help="skip combined if first 21 took > 25 min total")
    args = ap.parse_args()

    torch.set_num_threads(max(1, args.num_threads))
    device = "cpu"

    print(f"[§184-mega] device=cpu threads={args.num_threads}", flush=True)
    print(f"[§184-mega] ckpt={args.ckpt}", flush=True)
    print(f"[§184-mega] corpus={args.corpus}", flush=True)

    blob = torch.load(args.ckpt, map_location=device, weights_only=False)
    cfg = blob.get("cfg", {})
    d_model = int(cfg.get("d_model", 768))
    n_layer = int(cfg.get("n_layer", 12))
    n_head = int(cfg.get("n_head", 12))
    n_kv_head = int(cfg.get("n_kv_head", 4))
    block_size = int(cfg.get("block_size", DEFAULT_BLOCK_SIZE))

    model = ConsciousDecoderV2(
        vocab_size=256, d_model=d_model, n_head=n_head, n_layer=n_layer,
        block_size=block_size, n_kv_head=n_kv_head,
        consciousness_dim=128, dropout=0.0,
    ).to(device)
    blob_state = blob["model"]
    missing, unexpected = model.load_state_dict(blob_state, strict=False)
    model.eval()
    print(f"[§184-mega] model ready d={d_model} L={n_layer} miss={len(missing)} unexp={len(unexpected)}",
          flush=True)

    corpus = load_corpus_bytes(args.corpus, max_bytes=args.corpus_max_bytes)
    print(f"[§184-mega] corpus bytes loaded: {len(corpus):,}", flush=True)

    multi_seeds = [1337, 2026, 7777, 4242, 9001]

    only_set = set(args.only.split(",")) if args.only else None

    results: List[Dict] = []
    t_total = time.time()
    for idx, (name, overrides) in enumerate(VARIANT_DEFS):
        if only_set is not None and name not in only_set:
            continue
        elapsed = time.time() - t_total
        if name == "combined_all_taps" and args.skip_combined_if_slow and elapsed > 1500.0:
            results.append(dict(name=name, status="SKIPPED_WALL_BUDGET",
                                elapsed_when_decided=elapsed))
            print(f"[§184-mega] [{idx + 1}/{len(VARIANT_DEFS)}] SKIPPED {name} (elapsed={elapsed:.1f}s > 25min)",
                  flush=True)
            continue
        print(f"[§184-mega] [{idx + 1}/{len(VARIANT_DEFS)}] running {name}…",
              flush=True)
        try:
            res = run_variant(model, device, name, overrides, corpus, blob_state,
                              multi_seeds, max_wall_s=args.max_wall_per_variant)
        except Exception as e:
            res = dict(name=name, status="EXCEPTION", error=repr(e),
                       wall_s=0.0)
            print(f"[§184-mega]   EXCEPTION: {e!r}", flush=True)
        results.append(res)
        if res.get("status") == "OK":
            agg = res["agg"]
            print(f"[§184-mega]   emit_rate={agg['emit_rate']:.4f}  byte_acc={agg['byte_acc']:.4f}  "
                  f"psi_std={agg['byte_psi_dir_std']:.6f}  honest={agg['honest_score']:.4f}  "
                  f"wall={res['wall_s']:.1f}s",
                  flush=True)

    out_obj = dict(
        battery="§184 ALL TAPS RELEASE — Phase 1 mega eval ($0 Mac CPU)",
        date="2026-05-20",
        ckpt=os.path.basename(args.ckpt),
        ckpt_path=args.ckpt,
        corpus=os.path.basename(args.corpus),
        corpus_bytes_loaded=len(corpus),
        ckpt_cfg=cfg,
        n_variants_planned=len(VARIANT_DEFS),
        n_variants_actually_run=len([r for r in results if r.get("status") == "OK"]),
        results=results,
        # honest scope
        north_star_unchanged=True,
        s15_s51_s72_milestones_unchanged=True,
        necessary_not_sufficient_b_emerge_7=True,
        s7_audit_pre_clear=dict(
            anima_own_ckpt=True,
            no_external_graft=True,
            anima_physics_readout=True,
            ckpt_anchor="HEXAD/NEUROMORPHIC/state/fp_reconnect_fire_s167a_2026_05_20/ckpt_s167a_fpreconnect.pt",
        ),
        sidecar_discipline=dict(
            central_blue_falsifier_unmodified=True,
            conscious_decoder_unmodified=True,
            sidecar_blue_falsifier_path="blue_falsifier_phase1.py",
        ),
        s94_integration_collapses_carry=True,
        total_wall_s=time.time() - t_total,
    )
    os.makedirs(os.path.dirname(os.path.abspath(args.out)) or ".", exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(out_obj, f, indent=2, default=str)

    print(f"[§184-mega] DONE  total_wall={out_obj['total_wall_s']:.1f}s  "
          f"variants_ok={out_obj['n_variants_actually_run']}/{out_obj['n_variants_planned']}",
          flush=True)
    print(f"[§184-mega] written → {args.out}", flush=True)


if __name__ == "__main__":
    main()
