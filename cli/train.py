#!/usr/bin/env python3
"""cli/train.py — the CANONICAL anima python training entry (`anima-py train`).

>>> This file is the sole active training entry, paired with cli/evaluate.py.
>>> `anima-py train <args>` dispatches HERE. The torch path is GPU-bound and trains the
>>> real clm303 (L4·d3784·E2->Emax4), then serializes the existing checkpoint formats
>>> consumed by the canonical Python decode/evaluation path.
>>>
>>>   ENGINE-NATIVE GATE (a_engine_native_learning, HARD-GATE): torch-side CE / gauges
>>>   here = DIRECTIONAL only (NOT terminal). TERMINAL verdict = CORE re-measure of the
>>>   serialized .clm via `anima-py evaluate <clm>` on the frozen ρ-AXON reach bars (former G0-G6). Pull the
>>>   trained ckpt before teardown (a_fire_recover_complete) so engine-check is possible.

This trainer carries the full SAVANT + MITOSIS recipe and
the H_1640 OBJECTIVE-DISCOVERY surface: `--arm {ctrl,tlora,tlora_dict,tlora_jamo}` ×
`--objective {ce_marginal,infonce,contrastive_equilibrium,predictive_info,
constructive_bind,composed_nce}`. The last THREE objectives are the NEW compositional
ρ·weave levers (recombination · frozen bar = former G1 · added on top of CE) — this arm ×
objective matrix is the whole point of the
py entry (the trunk-objective search for the ρ·weave (former G1) recombination / ρ·fan (former G6) ideation wall).

WHY the objective lever (context, do not re-derive): the ρ·weave (former G1) recombination / ρ·fan (former G6) ideation
wall is confirmed TRUNK-OBJECTIVE-BOUND — cross-entropy does NOT reward COMPOSITION of
concepts, so every READOUT op tried (multiplicative binding exp3, CLS pattern-sep
H_1815, TLoRA expert-weight H_1813, plain-InfoNCE recomb-objective H_9024) only lifts ρ·leap/G2
novelty (orthogonal) and floors ρ·weave/G1. External lit converges: the lever is the OBJECTIVE +
regularization, NOT the operator. So a NEW lever must be a NEW LOSS FUNCTION that rewards
compositional structure IN THE TRUNK, added to CE. This package adds three such losses:

  predictive_info   — MULTI-STEP predictive-coding aux. Aux linear heads predict the
                      tokens k=2,3,4 steps AHEAD from the trunk penultimate (not just
                      the immediate next token). Rewards the penultimate for carrying
                      predictive info about the FUTURE beyond t+1 = the cortical
                      predictive hierarchy / predictive-information bottleneck
                      (Bialek-Tishby predictive information; van den Oord CPC 1807.03748;
                      Rao&Ballard predictive coding). Heads DROPPED at serialize.

  constructive_bind — TRAINED CONSTRUCTIVE BIND aux (the one untried piece of the
                      substrate framebreak). Two learned projections extract role r and
                      filler f from the penultimate; they are BOUND by circular
                      convolution c = r⊛f (Plate 1995 Holographic Reduced Representations
                      / Smolensky 1990 Tensor-Product Representations). Two constraints
                      sculpt a compositional code: (1) UNBIND recovers the filler
                      (unbind(c,r)≈f, cos loss) so the code must support clean
                      compose/decompose, and (2) the bound composite must PREDICT the
                      next token (dec(c)→y, CE) so binding carries task signal. Heads
                      DROPPED at serialize.

  composed_nce      — COMPOSED-NEGATIVE InfoNCE. Plain InfoNCE's negatives are RANDOM
                      vocab tokens (concept-membership only). Here the negatives are the
                      SAME bag of tokens present in the window but assigned to the WRONG
                      position (targets permuted WITHIN each sequence). Contrasting the
                      true token-to-position assignment against same-concept-set /
                      wrong-composition assignments directly rewards getting the
                      COMPOSITION right, not just the concept set (hard-negative /
                      order-sensitive contrastive; CPC-style). Operates on logits — no
                      aux params, gradient flows readout→trunk.

All three are DIRECTIONAL torch-side training pressures; the verdict is later via
`anima-py evaluate <clm>` engine-native on the FROZEN ρ·weave bar (recombination · former G1 · a_engine_native_learning).
The .clm path stays OPEN: aux heads/projections live OUTSIDE model.state_dict (in the
objective module), so serialize_v3 writes only the standard additive-readout CLMConvMoE.

LEVERS (arm axis, orthogonal to the readout-floor result, all on the SAME trunk):
  N1  TLoRA / TensorPoly expert-weight reparameterization (2405.16671): each ConvExpert
      conv weight W∈(d,d,K) is REPARAMETERIZED as a low-rank tensor product
      W = sum_r (a_r ⊗ b_r) ⊗ k_r (+ optional dense base), learned via the factors then
      MATERIALIZED back to the dense (d,d,K) conv weight (so the .clm path stays OPEN).
  N3  DBES expert-specialization diagnostic (2605.18523, MEASURE-ONLY, gradient-free).
  N7  dictionary/sparse-coding aux loss (2603.28744): L1 sparsity on the penultimate.
  N8  jamo (자모) compositional teach signal (2604.12377): next-jamo-class aux head.
  N6  regularization schedule sweep (--wd-floor / --dropout-floor override knobs).

Arms (single structural variable each, vs ctrl):
  ctrl       : production CLMConvMoE, plain CE. The discriminating control.
  tlora      : N1 TLoRA expert-weight (rank R, base on) + CE.
  tlora_dict : N1 TLoRA + N7 dictionary/sparse aux.
  tlora_jamo : N1 TLoRA + N8 jamo teach aux.

ARCH (--arch {clm,bytegpt}, default clm — preserves current behavior): the objective
levers are ARCH-AGNOSTIC (they operate on logits + an optional penultimate), so they can
be tested on EITHER trunk. `--arch bytegpt` builds a 24-layer GPT-2-class ByteGPT (the
CLEAN ρ·weave recombination wall (former G1): ByteGPT single=2, vs CLMConvMoE's single=0 coverage-floor) and serializes a
`.bin` (5×u32 header) via core/serialize.py (the unified serializer) instead of a `.clm`. For bytegpt the
CLM-specific levers (savant/mitosis/tlora/dict/jamo) are gated OFF — only arm=ctrl × the
objective matrix is supported (that's exactly what the G1-lever test needs). `anima-py
evaluate` auto-detects `.bin` vs `.clm` by header, so a ByteGPT `.bin` measures through
the bytegpt mouth automatically.

USAGE (installed canonical `anima-py` command):
  # CLM trunk (default):
  anima-py train --arm ctrl --objective constructive_bind --steps 8000 \\
      --canon --corpus <p1..p4> --cell-label ko-general en-general ko-sns en-sns \\
      --seed 7 --val-frac 0.05 --val-every 200 --sample proportional \\
      --out ckpt/ctrl_cbind_seed7.clm --ckpt-out ckpt/ctrl_cbind_seed7.pt \\
      --gauges-out ckpt/ctrl_cbind_seed7.json
  # ByteGPT trunk (the CLEAN ρ·weave recombination wall · former G1) — arm=ctrl × the objective matrix:
  anima-py train --arch bytegpt --arm ctrl --objective composed_nce --steps 8000 \\
      --canon --corpus <p1..p4> --seed 7 --out ckpt/bg_ctrl_cnce.bin \\
      --gauges-out ckpt/bg_ctrl_cnce.json
"""
from __future__ import annotations
import argparse, hashlib, json, math, os, random, re, sys, tempfile, time   # `random`: H_9841 replay-selection control
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist                       # DDP collectives (§1/§3/§6)
from torch.nn.parallel import DistributedDataParallel as DDP   # §4 composite-shell wrap

# ── locate the CLM model + serializer/verifier — all CORE-owned (core/) ──────
# LOCATION-INDEPENDENT (the installed `anima` runs from ANY cwd + this file lives in
# cli/, not the repo root): the UNIFIED CLM+ByteGPT torch model (model.py), the held-out
# DESCENT verifier (verify_clm_v2.py), the historical serialize backend
# (clm_serialize_v2.py) and the .pt→.clm bridge (serialize_standalone.py)
# ALL live in core/ (owner directive: core-related lives in core/; no archive/train
# import — a_no_archive_import). core/ is added to sys.path so bare `import model` /
# `import serialize` resolve, the same resolution cli/evaluate.py uses for `import decode`.
_HERE = os.path.dirname(os.path.abspath(__file__))          # …/cli
_ROOTS = []
_ENV_SRC = os.environ.get("ANIMA_SRC")
if _ENV_SRC:
    _ROOTS.append(_ENV_SRC)
_ROOTS.append(os.path.dirname(_HERE))                       # repo root = parent of cli/
# tool/ (gauge_lib) is best-effort (the ρ·weave/ρ·fan (former G1/G6) torch probe below is wrapped in try/except).
for _r in _ROOTS:
    _t = os.path.join(_r, "tool")
    if os.path.isdir(_t) and _t not in sys.path:
        sys.path.insert(0, _t)
# core/ is the engine package — the CLM model, the unified serializer (serialize.py),
# and the verifier all resolve from here.
_CORE = None
for _r in _ROOTS:
    _c = os.path.join(_r, "core")
    if os.path.isdir(_c):
        # The script directory (cli/) is always sys.path[0].  When callers also
        # provide core/ through PYTHONPATH, the old membership guard left that
        # existing entry behind cli/ and bare ``import serialize`` resolved to
        # cli/serialize.py instead of the engine SSOT core/serialize.py.  Always
        # promote the resolved core directory to the front.
        if _c in sys.path:
            sys.path.remove(_c)
        sys.path.insert(0, _c)
        if _CORE is None and os.path.exists(os.path.join(_c, "model.py")):
            _CORE = _c
if _CORE is None:
    raise ImportError(
        "cli/train.py: could not locate core/model.py under the repo root or "
        "$ANIMA_SRC. Set $ANIMA_SRC to the anima source root.")

# (imports resolve via the core/ sys.path insert above.)
from model import (CLMConfig, CLMConvMoE, MoEStats, CausalDilatedConv1d,
                   ByteGPTConfig, ByteGPT)           # core/model.py (unified CONV+BYTE)
import serialize as S                                # core/serialize.py — serialize_v3 = bridge SSOT
import phi_envelope_monitor as PEM                   # core/phi_envelope_monitor.py — H_9846 watch
import verify_clm_v2 as VC                            # core/verify_clm_v2.py — clm_decodable / descent
# ByteGPT .pt -> .bin serializer is folded into the SAME unified core/serialize.py.
import serialize as BGS                               # core/serialize.py — serialize(pt_path, bin_path)
import dream_lib as DR                                # core/dream_lib.py — H_9840 5-stage session + Process-S/C


# ════════════════════════════════════════════════════════════════════════════
#  golden-zone constants (SAVANT/savant_lib.hexa H_347/348, verbatim — same as
#  cli/train.hexa gz_lower()/gz_upper()).
# ════════════════════════════════════════════════════════════════════════════
GZ_LOWER = 0.21231792755821914   # 1/2 - ln(4/3)  (sa_gz_lower)
GZ_UPPER = 0.5                    # sa_gz_upper
LN2 = 0.6931471805599453

RESUME_SCHEMA = "anima-train-resume/v1"


class WarmStartReport(str):
    """String-compatible warm-start report carrying optional exact-resume state."""

    def __new__(cls, text: str, resume=None):
        value = str.__new__(cls, text)
        value.resume = resume
        return value


def _digest_update(h, value):
    """Canonical recursive hash for tensors and checkpoint control state."""
    if torch.is_tensor(value):
        t = value.detach().cpu().contiguous()
        h.update(b"tensor\0")
        h.update(str(t.dtype).encode())
        h.update(repr(tuple(t.shape)).encode())
        # Adam stores its step counter as a scalar tensor. Flatten first so scalar and
        # higher-rank tensors share one canonical byte path; direct scalar.view(uint8) is invalid.
        h.update(t.reshape(-1).view(torch.uint8).numpy().tobytes())
    elif isinstance(value, dict):
        h.update(b"dict\0")
        for key in sorted(value, key=lambda item: repr(item)):
            _digest_update(h, key)
            _digest_update(h, value[key])
    elif isinstance(value, (list, tuple)):
        h.update((b"list\0" if isinstance(value, list) else b"tuple\0"))
        for item in value:
            _digest_update(h, item)
    elif value is None:
        h.update(b"none\0")
    else:
        h.update(type(value).__name__.encode() + b"\0" + repr(value).encode())


def resume_state_digest(model_state, optimizer_state, completed_step, rng_state):
    h = hashlib.sha256()
    _digest_update(h, {"model": model_state, "optimizer": optimizer_state,
                       "completed_step": int(completed_step), "rng": rng_state})
    return h.hexdigest()


def _restore_resume_state(payload, model, optimizer, generators, device):
    """Restore and verify an exact trainer checkpoint after runtime objects exist."""
    if not payload:
        return 0, ""
    required = {"optimizer", "completed_step", "rng", "state_digest"}
    missing = sorted(required - set(payload))
    if missing:
        raise ValueError(f"resume checkpoint missing exact state: {missing}")
    model_state = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    before = resume_state_digest(model_state, payload["optimizer"],
                                 payload["completed_step"], payload["rng"])
    if before != payload["state_digest"]:
        raise ValueError("resume checkpoint state digest mismatch before restore")

    optimizer.load_state_dict(payload["optimizer"])
    rng = payload["rng"]
    torch.set_rng_state(rng["torch_cpu"])
    if str(device).startswith("cuda") and rng.get("torch_cuda"):
        if len(rng["torch_cuda"]) != torch.cuda.device_count():
            raise ValueError("resume CUDA RNG device count differs from checkpoint")
        torch.cuda.set_rng_state_all(rng["torch_cuda"])
    random.setstate(rng["python"])
    saved_generators = rng.get("generators", {})
    for name, generator in generators.items():
        saved = saved_generators.get(name)
        if generator is None:
            if saved is not None:
                raise ValueError(f"resume sampler {name} exists but runtime lane is disabled")
        elif saved is None:
            raise ValueError(f"resume checkpoint missing sampler state: {name}")
        else:
            generator.set_state(saved)

    restored_model = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    restored_rng = {
        "torch_cpu": torch.get_rng_state(),
        "torch_cuda": torch.cuda.get_rng_state_all() if str(device).startswith("cuda") else [],
        "python": random.getstate(),
        "generators": {name: (gen.get_state() if gen is not None else None)
                       for name, gen in generators.items()},
    }
    after = resume_state_digest(restored_model, optimizer.state_dict(),
                                payload["completed_step"], restored_rng)
    if after != payload["state_digest"]:
        raise ValueError("resume checkpoint state digest mismatch after restore")
    return int(payload["completed_step"]), after


def savant_inhibition(step: int, n_steps: int, i0: float, i_floor: float,
                      latch: dict) -> float:
    """Golden-zone cusp-anneal inhibition for THIS step (a_savant_train).

    Linear anneal I0 -> I_floor over training. When I first crosses INTO the
    golden zone [GZ_LOWER, GZ_UPPER] on the way down, latch['on'] hard-steps to
    True (cusp, H_1562) and STAYS True for the rest of training (asymmetric
    hysteresis, H_1563) even as the anneal drives I below GZ_LOWER (H_1559: the
    sweep below the floor is intentional so the learning sweet-spot is reached).
    Mirrors cli/train.hexa::savant_inhibition in arithmetic.
    """
    denom = (n_steps - 1) if n_steps > 1 else 1
    frac = (step - 1) / denom
    inh = i0 + (i_floor - i0) * frac
    if not latch["on"]:
        if GZ_LOWER <= inh <= GZ_UPPER:
            latch["on"] = True
            if latch["at"] == 0:
                latch["at"] = step
    return inh


def inhibition_to_wd(inh: float) -> float:
    """Map inhibition I -> AdamW weight decay (I in [0,0.5] -> wd in [0,0.05]).
    Deterministic (p7). Same linear lever as cli/train.hexa::inhibition_to_wd."""
    return inh * 0.1


def inhibition_to_dropout(inh: float) -> float:
    """Inhibition also realized as dropout p (clamped to a sane [0, 0.5]). The
    dropout/weight-decay/temperature variants share the single scalar lever."""
    return max(0.0, min(0.5, inh))


def _install_mps_dropout_shim() -> None:
    """Work around an Apple-MPS upstream bug: torch's MPS backend compiles and
    PERMANENTLY caches a new MPSGraph per DISTINCT scalar value fed to a value-keyed
    op. F.dropout(x, p) on MPS lowers to bernoulli_ -> at::full({}, 1-p) ->
    fill_scalar_mps_impl (ConstantOps.mm), whose cache key bakes in to_string(1-p).
    The SAVANT schedule feeds a NEW continuous dropout p every step (`m.p = dp`, below),
    so the cache grows without bound: measured ~0.72 MB/step + ~7x slowdown (isolated
    microbench), matching the observed 45 GB / 61 k-step swap-death of a d=64 L=2 toy.
    torch.mps.empty_cache() frees the allocator, NOT the graph cache, so it cannot even
    mask the symptom. wd/lr scalars are runtime-fed (BinaryOps) and DO NOT leak.

    Fix (root cause, at the layer we own): never feed the varying p to a VALUE-KEYED op.
    Build the mask from `torch.rand_like(x) < keep` and rescale by `/ keep` — the uniform
    draw carries no scalar in its graph key, and the compare and divide are BinaryOps
    whose scalar operand is runtime-fed (the same reason wd/lr never leaked), so NO
    fill_scalar and NO per-p graph is ever cached (measured flat ~208 MB, full speed while
    p varies every step). The inverted-dropout mask x*[U<keep]/keep is distributionally
    identical to F.dropout. Fresh tensors each call ⇒ no persistent scalar to mutate ⇒ no
    autograd version-counter hazard even across the model's several dropout layers.

    Device-branched: only F.dropout calls whose input lives on MPS are rerouted; CPU/CUDA
    calls fall through to the stock kernel UNTOUCHED. This helper is invoked ONLY when
    device == "mps", so a CPU/CUDA run never installs the shim at all → their numerics
    stay byte-identical (train reproducibility contract). `inplace` is treated as a hint
    (a fresh tensor is always returned — same value, autograd-safe). Idempotent."""
    if getattr(F.dropout, "_anima_mps_shim", False):
        return
    _orig = F.dropout

    def _shim(input, p: float = 0.5, training: bool = True, inplace: bool = False):
        if training and p > 0.0 and input.device.type == "mps":
            keep = 1.0 - float(p)
            mask = (torch.rand_like(input) < keep).to(input.dtype)
            return input * mask / keep
        return _orig(input, p, training, inplace)

    _shim._anima_mps_shim = True
    _shim._orig = _orig
    F.dropout = _shim


# ════════════════════════════════════════════════════════════════════════════
#  MITOSIS split E -> E+1 (a_mitosis_train) — continuity-preserving cell division
#  on the live torch MoEConvLayer. Port of cli/train.hexa::train_mitosis_split /
#  clm_mitosis.hexa::mitosis_split semantics:
#    * child expert conv = copy(parent) + tiny alternating +/-1e-4 perturbation
#    * router weight row for child = copy(parent row)
#    * router bias: both parent and child get (parent_bias - ln2) so the two
#      children jointly reproduce the parent's gate mass (near-continuous split)
#    * the optimizer's Adam moments for the touched params are reset to 0.
#  Experts are pre-allocated at Emax (inactive experts masked out of the router
#  until they are "born"), so a split just UNMASKS + seeds the next slot.
# ════════════════════════════════════════════════════════════════════════════
class MitosisMoE:
    """Tracks the ACTIVE expert count E while experts/router are physically
    allocated at Emax. Inactive experts are masked out of the router softmax
    (logit += -1e9) so they are inert until born."""

    def __init__(self, model: CLMConvMoE, e0: int, emax: int):
        self.model = model
        self.e_active = e0
        self.emax = emax
        dev = next(model.parameters()).device
        self.active_mask = torch.zeros(emax, device=dev)
        self.active_mask[:e0] = 1.0

    def neg_inf_bias(self) -> torch.Tensor:
        # additive router-logit bias: 0 for active slots, -1e9 for dormant.
        return (self.active_mask - 1.0) * 1e9

    @torch.no_grad()
    def split(self, parent: int, opt: torch.optim.Optimizer) -> int:
        """Divide `parent` into a fresh child slot (= current e_active index).
        Returns the new active count, or the unchanged count if at Emax."""
        if self.e_active >= self.emax:
            return self.e_active
        child = self.e_active
        moe = self.model.moe
        pe = moe.experts[parent].conv.conv     # parent expert Conv1d
        ce = moe.experts[child].conv.conv      # child  expert Conv1d
        # copy weights + tiny alternating perturbation (parity w/ hexa eps loop)
        pw = pe.weight.detach().clone()
        flat = pw.reshape(-1)
        eps = torch.full_like(flat, 1e-4)
        eps[1::2] = -1e-4
        ce.weight.copy_((flat + eps).reshape(pw.shape))
        if pe.bias is not None and ce.bias is not None:
            ce.bias.copy_(pe.bias)
        # router: child row = parent row; bias splits by -ln2 on BOTH children
        rw = moe.router.weight             # (Emax, d, 1)
        rb = moe.router.bias               # (Emax,)
        rw[child].copy_(rw[parent])
        pb = rb[parent].item()
        rb[parent] = pb - LN2
        rb[child] = pb - LN2
        # reset Adam moments for the touched params (m,v -> 0).
        for p in (pe.weight, ce.weight, pe.bias, ce.bias, rw, rb):
            if p is None:
                continue
            st = opt.state.get(p, None)
            if st:
                if "exp_avg" in st:
                    st["exp_avg"].zero_()
                if "exp_avg_sq" in st:
                    st["exp_avg_sq"].zero_()
        self.active_mask[child] = 1.0
        self.e_active = child + 1
        return self.e_active


# ════════════════════════════════════════════════════════════════════════════
#  Router masking — patch MoEConvLayer.forward so dormant experts are inert.
#  We add the dormant-slot -inf bias to the router logits before softmax so an
#  allocated-at-Emax model behaves EXACTLY like an E-active model until a mitosis
#  split unmasks the next slot. Pure additive logit mask; trunk/embed/readout are
#  untouched, so the serialized .clm round-trips the grown E.
# ════════════════════════════════════════════════════════════════════════════
def install_router_mask(model: CLMConvMoE, mito: MitosisMoE):
    moe = model.moe
    orig_router = moe.router

    def masked_forward(x):
        B, C, T = x.shape
        n_e = moe.rc.n_experts
        logits = orig_router(x) + mito.neg_inf_bias().view(1, n_e, 1)
        probs = F.softmax(logits, dim=1)
        ent_tok = -(probs * torch.log(probs + 1e-9)).sum(dim=1)
        entropy = ent_tok.mean()
        ex_out = torch.stack([e(x) for e in moe.experts], dim=1)
        if moe.rc.hard_top_k:
            k = min(moe.rc.top_k, int(mito.e_active))
            topv, topi = probs.topk(k, dim=1)
            gate = topv / (topv.sum(dim=1, keepdim=True) + 1e-9)
            mask = torch.zeros_like(probs).scatter_(1, topi, gate)
        else:
            mask = probs
        y = (mask.unsqueeze(2) * ex_out).sum(dim=1)
        usage = probs.mean(dim=(0, 2))
        aux = x.new_zeros(())
        if moe.rc.load_balance_coef > 0.0:
            top1 = probs.argmax(dim=1)
            f_i = F.one_hot(top1, n_e).to(probs.dtype).mean(dim=(0, 1))
            lb = n_e * (f_i * usage).sum()
            aux = aux + moe.rc.load_balance_coef * lb
        if moe.rc.entropy_coef > 0.0:
            aux = aux - moe.rc.entropy_coef * entropy
        return y, MoEStats(usage=usage, aux_loss=aux, entropy=entropy)

    moe.forward = masked_forward


# ════════════════════════════════════════════════════════════════════════════
#  4-cell register corpus (a_chat_registers) — {ko·en}x{normal·SNS}. Each
#  --corpus entry is a LOCAL byte file OR an HF dataset path (resolved to a local
#  cached byte stream). Windows are sampled round-robin across the cells so every
#  step sees the register mix. Files are mmap'd so a multi-GB cell is never
#  slurped whole into RAM.
# ════════════════════════════════════════════════════════════════════════════
class ByteCell:
    """One register cell — a memory-mapped byte file sampled by random windows.

    Validation comes from an explicit `validation_path` when supplied; otherwise
    the legacy TAIL `val_frac` of the train file is reserved. A window can NEVER
    cross from train into validation, so held-out bytes are never seen by a
    training gradient step."""

    def __init__(self, path: str, val_frac: float = 0.0,
                 validation_path: str | None = None):
        import mmap
        self.path = path
        self.size = os.path.getsize(path)
        self._f = open(path, "rb")
        if self.size > 0:
            self._mm = mmap.mmap(self._f.fileno(), 0, access=mmap.ACCESS_READ)
        else:
            self._mm = b""
        # boundary: bytes [0, train_end) = train, [train_end, size) = held-out val.
        vf = max(0.0, min(0.5, val_frac))
        self.validation_path = validation_path
        if validation_path is not None:
            self.train_end = self.size
            self.val_size = os.path.getsize(validation_path)
            self._val_f = open(validation_path, "rb")
            if self.val_size > 0:
                self._val_mm = mmap.mmap(self._val_f.fileno(), 0, access=mmap.ACCESS_READ)
            else:
                self._val_mm = b""
        else:
            self.train_end = int(self.size * (1.0 - vf)) if self.size > 0 else 0
            self.val_size = self.size - self.train_end
            self._val_f = None
            self._val_mm = None

    @staticmethod
    def _window_in_buffer(buffer, lo: int, hi_excl: int, seq_len: int,
                          gen: torch.Generator):
        """Sample one (x,y) window whose [start, start+seq_len+1) lies entirely
        inside the byte range [lo, hi_excl). Returns None if the range is too
        small for even one window."""
        if hi_excl - lo < seq_len + 2:
            return None
        hi = hi_excl - seq_len - 1            # last valid start (exclusive upper bound)
        start = int(torch.randint(lo, hi, (1,), generator=gen).item())
        chunk = buffer[start:start + seq_len + 1]
        buf = torch.frombuffer(bytearray(chunk), dtype=torch.uint8).long()
        return buf[:seq_len], buf[1:seq_len + 1]

    def window_spec(self, seq_len: int, gen: torch.Generator):
        """§3 SPEC phase — the RNG-only half of a TRAIN window: the bounds-check + randint
        that `_window_in(0, train_end, …)` does, WITHOUT the mmap read. Returns the start
        index, or None when [0, train_end) is too small for even one window — in which case
        NO randint is consumed (identical early-return to `_window_in`). Every DDP rank
        replays this off the SHARED gen so the GLOBAL window set is byte-identical to the
        1-GPU draw; each rank only materializes its own slice (window desync would break
        both the frozen-recipe comparison AND N==1 byte-identity, §10.4)."""
        lo, hi_excl = 0, self.train_end
        if hi_excl - lo < seq_len + 2:
            return None
        hi = hi_excl - seq_len - 1            # last valid start (exclusive upper bound)
        return int(torch.randint(lo, hi, (1,), generator=gen).item())

    def materialize(self, start: int, seq_len: int):
        """§3 MATERIALIZE phase — the mmap-read half: given a `start` from window_spec,
        return the (x, y) window. Kept separate so a rank only touches disk for its own
        shard. Byte-for-byte identical to `_window_in`'s post-randint tail."""
        chunk = self._mm[start:start + seq_len + 1]
        buf = torch.frombuffer(bytearray(chunk), dtype=torch.uint8).long()
        return buf[:seq_len], buf[1:seq_len + 1]

    def window(self, seq_len: int, gen: torch.Generator):
        """A TRAIN window — sampled only from [0, train_end) (never the val tail). Delegates
        to window_spec (RNG) then materialize (mmap) so the N==1 op + RNG-draw order is
        identical to the pre-refactor `_window_in` (bounds-check → randint → mmap read)."""
        start = self.window_spec(seq_len, gen)
        if start is None:
            return None
        return self.materialize(start, seq_len)

    def val_window(self, seq_len: int, gen: torch.Generator):
        """A held-out VAL window from an explicit file or the legacy train tail."""
        if self._val_mm is not None:
            return self._window_in_buffer(self._val_mm, 0, self.val_size, seq_len, gen)
        return self._window_in_buffer(self._mm, self.train_end, self.size, seq_len, gen)

    def close(self):
        """Close mmap/file handles without hiding partially initialized objects."""
        for name in ("_val_mm", "_mm"):
            mm = getattr(self, name, None)
            if hasattr(mm, "close"):
                mm.close()
        for name in ("_val_f", "_f"):
            fh = getattr(self, name, None)
            if fh is not None and not fh.closed:
                fh.close()

    def __del__(self):
        try:
            self.close()
        except Exception:
            pass



def _budget_preflight(corpus_specs, steps: int, lr: float) -> None:
    """Refuse to start below the training budget the corpus itself earned.

    H_9322 died on a 600-step CPT: the fact never landed, and the negative then read as "the
    substrate cannot compose" when it actually meant "the fine-tune was too small". H_9324 measured
    the floor on that corpus — WRITE 0.4483 (600@5e-5, chance) -> 0.9540 (6000@2e-4) -> 1.0000
    (6000@5e-4), reproduced on two seeds — so a sub-floor run is not a weak measurement, it is not a
    measurement. Nothing in the engine knew that number, which is what made the mistake repeatable.

    So `anima-py corpus` now writes the earned floor next to the corpus (`<corpus>.meta.json`) and
    this refuses to start below it. Same shape as _gpu_preflight: fail at second 0, not after the
    corpus is built and the model is on the device.

    The meta also carries `destroys` for the formats that have no floor at all: `ground`/`ground_lie`
    contain zero negated lines, so a BIGGER budget destroys MORE of the model's negation operator
    (SEEN flip1 0.8833 base -> 0.4333 -> 0.3333). Handing those a floor would be telling the trainer
    to break the model harder; they get a warning and a pointer to `ground_keep` instead.
    """
    for spec in corpus_specs or []:
        meta_path = str(spec) + ".meta.json"
        if not os.path.exists(meta_path):
            continue
        try:
            with open(meta_path) as fh:
                meta = json.load(fh)
        except Exception:
            continue                      # a corrupt sidecar must not block a legitimate run
        fmt = meta.get("format", "?")
        if meta.get("destroys"):
            print(f"  [budget-preflight] ⚠️ corpus format '{fmt}' has NO earned budget floor — "
                  f"{meta['destroys']}", flush=True)
        floor_s, floor_lr = meta.get("min_steps"), meta.get("min_lr")
        if not floor_s:
            continue
        if meta.get("floor_transplanted"):
            # A floor EARNED on one language is not a floor for another. Enforcing it here would be
            # the exact defect bar-derived-not-transplanted names: a bar nobody measured, applied as
            # if they had. So we WARN and let the run proceed — what actually decides whether the
            # budget sufficed is the WRITE gate on the resulting ckpt.
            if steps < floor_s or (floor_lr and lr < floor_lr):
                print(f"  [budget-preflight] ⚠️ steps={steps} lr={lr:g} is below a TRANSPLANTED "
                      f"floor (steps>={floor_s} lr>={floor_lr:g}, borrowed from another language and "
                      f"NOT measured for '{meta.get('lang')}'). NOT blocking — a bar nobody earned "
                      f"cannot gate a run. The WRITE gate on the resulting ckpt is what decides.",
                      flush=True)
            continue
        if steps < floor_s or (floor_lr and lr < floor_lr):
            raise SystemExit(
                f"[budget-preflight] REFUSING TO START — steps={steps} lr={lr:g} is BELOW the "
                f"budget this corpus earned (steps>={floor_s} lr>={floor_lr:g}, format '{fmt}').\n"
                f"  {meta.get('note', '')}\n"
                f"  A run below the floor does not produce a weak result — it produces a result "
                f"about the BUDGET, and it will be misread as a result about the substrate.\n"
                f"  Raise --steps/--lr, or delete {meta_path} if you are deliberately measuring "
                f"the sub-floor regime (and say so in the pre-registration).")
        print(f"  [budget-preflight] steps={steps} lr={lr:g} >= earned floor "
              f"({floor_s}/{floor_lr:g}, '{fmt}') — ok", flush=True)


def _gpu_preflight(device: str, steps: int) -> None:
    """Refuse to start when the GPU is already carrying someone else's run.

    A GPU is not a CPU core: VRAM is all-or-nothing, not preemptive. Two heavy trains on one card
    do not run at half speed — the second one dies, and it dies LATE, after the corpus is built and
    the model is on the device. Measured (2026-07-14, H_9327): the LIE control arm was fired onto
    summer while the seed-11 reproduction was still training there. It ran for minutes, then
    `torch.OutOfMemoryError: CUDA out of memory` on a 164 MiB allocation, taking down the one arm
    that was going to decide the verdict. What we lost was not compute — it was the control.

    So the check happens HERE, before a single parameter is allocated: if free VRAM is already too
    low to hold this run, stop and say so, loudly, with the command to see who is holding it. That
    is the whole fix — a wall you hit in 2 seconds instead of 20 minutes.

    The floor is deliberately crude (a fraction of total, not a per-model estimate): a precise
    estimate would need the model built, which is what we are trying to avoid, and being crudely
    right early beats being precisely right too late.
    """
    if not device.startswith("cuda") or not torch.cuda.is_available():
        return
    try:
        free_b, total_b = torch.cuda.mem_get_info(torch.device(device))
    except Exception:
        return          # older/odd torch: no preflight rather than a false block
    free_gib, total_gib = free_b / 2**30, total_b / 2**30
    # A 303M bf16 train (params + grads + Adam moments + activations) does not fit in a fifth of a
    # card. If that much is already gone, something else is on it.
    floor_gib = max(2.0, 0.35 * total_gib)
    if free_gib >= floor_gib:
        print(f"  [gpu-preflight] {device} free={free_gib:.1f}/{total_gib:.1f} GiB — ok", flush=True)
        return
    sys.exit(
        f"\nanima-py train: REFUSING TO START — {device} is already busy.\n"
        f"  free = {free_gib:.1f} GiB of {total_gib:.1f} GiB (need >= {floor_gib:.1f} GiB)\n"
        f"  steps requested = {steps}\n\n"
        "  A GPU is all-or-nothing: starting here would OOM partway through and destroy this run\n"
        "  (and it would do it AFTER the corpus build, minutes from now — the expensive way).\n\n"
        "  See who holds it:   nvidia-smi   /   pgrep -af 'cli/train[.]py'\n"
        "  Then either WAIT for that run to finish, or fire this one on a DIFFERENT GPU host.\n"
        "  Parallel tracks only pay off across hosts (a_wall_first) — never on one card.\n"
    )


def resolve_corpus_path(spec: str) -> str:
    """Resolve a --corpus entry to a local byte-file path.

    * existing local path -> use directly.
    * ``hf://datasets/<org>/<repo>@<revision>/<file>`` -> fetch that exact
      immutable Hub file through ``hf_hub_download``.
    * else treat as an HF dataset id (a_chat_registers names like
      'anima-corpus-5lang-unified-v2', 'anima-corpus-ko-fineweb2-broad',
      'anima-persona-sns-corpus') and stream it to a local cached byte file
      under $ANIMA_CORPUS_CACHE (default ./.corpus_cache) via `datasets`; the
      text column is concatenated UTF-8 -> raw bytes (V=256).
    """
    if os.path.exists(spec):
        return spec
    if spec.startswith("hf://"):
        parsed = _parse_hf_corpus_spec(spec)
        try:
            from huggingface_hub import hf_hub_download
        except Exception as e:
            raise FileNotFoundError(
                f"--corpus '{spec}' requires `huggingface_hub` ({e}). "
                "Install it or provide an existing local file."
            )
        print("  resolve: pinned HF dataset "
              f"{parsed['repo_id']}@{parsed['revision']}/{parsed['filename']}")
        return hf_hub_download(repo_id=parsed["repo_id"],
                               filename=parsed["filename"],
                               repo_type="dataset",
                               revision=parsed["revision"])
    cache_root = os.environ.get("ANIMA_CORPUS_CACHE",
                                os.path.join(os.getcwd(), ".corpus_cache"))
    os.makedirs(cache_root, exist_ok=True)
    local = os.path.join(cache_root, spec.replace("/", "__") + ".bytes")
    if os.path.exists(local) and os.path.getsize(local) > 0:
        return local
    try:
        from datasets import load_dataset
    except Exception as e:
        raise FileNotFoundError(
            f"--corpus '{spec}' is not a local file and `datasets` is not "
            f"installed to fetch it as an HF dataset ({e}). Provide a local "
            f"byte file, or `pip install datasets`."
        )
    # An HF id never looks like a bare local filename (no slash AND ends in a
    # file extension that doesn't exist locally) — a plain missing path is almost
    # always a staging mistake, so make the HF intent explicit in the log.
    repo = spec if "/" in spec else f"dancinlab/{spec}"
    print(f"  resolve: '{spec}' is not a local path -> streaming HF dataset {repo}")
    ds = load_dataset(repo, split="train", streaming=True)
    maxrows = int(os.environ.get("ANIMA_CORPUS_MAXROWS", "0") or 0)
    text_col = None
    with open(local, "wb") as out:
        for i, row in enumerate(ds):
            if text_col is None:
                for c in ("text", "content", "body", "caption"):
                    if c in row:
                        text_col = c
                        break
                if text_col is None:
                    text_col = next(iter(row))
            out.write(str(row[text_col]).encode("utf-8", "replace"))
            out.write(b"\n")
            if maxrows > 0 and i + 1 >= maxrows:
                break
    return local


def _parse_hf_corpus_spec(spec: str) -> dict:
    """Parse the canonical immutable HF raw-file corpus URI.

    The explicit dataset kind, full repo id, revision and file are all required:
    training data custody must never silently float from one Hub commit to another.
    """
    prefix = "hf://datasets/"
    if not spec.startswith(prefix):
        raise ValueError(
            "pinned HF corpus must use hf://datasets/<org>/<repo>@<revision>/<file>")
    body = spec[len(prefix):]
    if "@" not in body:
        raise ValueError(f"pinned HF corpus is missing @revision: {spec}")
    repo_id, pinned = body.split("@", 1)
    if repo_id.count("/") != 1 or "/" not in pinned:
        raise ValueError(
            "pinned HF corpus must include <org>/<repo>@<revision>/<file>")
    revision, filename = pinned.split("/", 1)
    if not all((repo_id, revision, filename)) or revision in {"main", "master"}:
        raise ValueError(
            "pinned HF corpus requires a non-floating revision and non-empty file")
    if any(part in {"", ".", ".."} for part in filename.split("/")):
        raise ValueError(f"pinned HF corpus contains an unsafe file path: {filename}")
    return {"repo_id": repo_id, "revision": revision, "filename": filename}


def scheduled_lr(step: int, base_lr: float, schedule: str, warmup_steps: int,
                 decay_steps: int, min_lr_ratio: float) -> float:
    """Return the deterministic learning rate for one 1-indexed optimizer step.

    The schedule has no mutable state, so an exact-resume checkpoint only needs the
    completed step plus the recipe already stored beside the optimizer and RNG state.
    """
    if step < 1:
        raise ValueError("scheduled_lr step must be >= 1")
    if warmup_steps > 0 and step <= warmup_steps:
        return float(base_lr) * float(step) / float(warmup_steps)
    if schedule == "constant":
        return float(base_lr)
    if schedule != "cosine":
        raise ValueError(f"unknown lr schedule: {schedule}")
    if decay_steps <= warmup_steps:
        raise ValueError("cosine decay_steps must be greater than warmup_steps")
    progress = min(1.0, max(0.0, (step - warmup_steps) /
                            float(decay_steps - warmup_steps)))
    cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
    return float(base_lr) * (float(min_lr_ratio) +
                             (1.0 - float(min_lr_ratio)) * cosine)


# ── frozen lever hyperparams (pre-registered in PREREG.md — tune-to-green 금지) ──
TLORA_RANK = 8            # default tensor-product rank R (a_r⊗b_r⊗k_r factors)
TLORA_BASE = True         # keep a small dense base weight alongside the low-rank TP
DICT_LAMBDA = 1e-3        # N7 trunk-penultimate L1 sparsity weight (Stop-Probing)
JAMO_LAMBDA = 0.3         # N8 next-jamo-class aux head weight (SCRIPT)
INFONCE_LAMBDA = 1.0; INFONCE_NEG = 64
EQ_LAMBDA = 1.0; EQ_MARGIN = 0.5

# ── NEW OBJECTIVE frozen hyperparams (H_1640 — pre-registered in PREREG.md) ──
PREDINFO_LAMBDA = 0.5            # multi-step predictive-coding aux weight (per horizon, averaged)
PREDINFO_HORIZONS = (2, 3, 4)   # predict tokens 2/3/4 steps AHEAD from penultimate
CBIND_LAMBDA = 0.5              # constructive-bind aux weight (unbind-recon + composite-CE)
CBIND_DIM = 256                 # HRR role/filler factor dim (power-of-2 friendly for FFT)
CBIND_UNBIND_W = 1.0           # weight on the unbind-recovers-filler term
CBIND_PRED_W = 1.0             # weight on the bound-composite-predicts-next-token term
CNCE_LAMBDA = 1.0              # composed-negative InfoNCE weight
CNCE_PERMS = 8                 # # of within-window target permutations = wrong-composition negatives


# ════════════════════════════════════════════════════════════════════════════
#  N1 — TLoRA / TensorPoly expert weight.
#  A drop-in replacement for ConvExpert whose conv weight W∈(d_out=d,d_in=d,K) is
#  reparameterized as a sum of R rank-1 tensor products plus an optional small
#  dense base. The forward is still a plain causal conv (engine-compatible). The
#  effective dense weight is exposed via .materialized_weight() so it can be
#  written into a standard CLMConvMoE state_dict for serialize_v3 (engine-native).
# ════════════════════════════════════════════════════════════════════════════
class TLoRAConvExpert(nn.Module):
    """ConvExpert with a tensor-product-factorized conv weight (N1, TLoRA).

    W[o,i,k] = base[o,i,k] + sum_r  A[r,o] * B[r,i] * Kf[r,k]
    where A∈(R,d), B∈(R,d), Kf∈(R,K). This is the Tucker/CP tensor-product
    reparameterization (TensorPoly/TLoRA, 2405.16671) applied to the expert
    weight position — a STRUCTURED (low-rank, compositional) prior on how the
    expert mixes channels, distinct from the readout-position Hadamard we
    already floored (exp3). The bias is a normal learnable vector."""

    def __init__(self, cfg: CLMConfig, rank: int, base: bool):
        super().__init__()
        d, K = cfg.d_model, cfg.expert_kernel_size
        self.d, self.K, self.R = d, K, rank
        self.dilation = 1
        self.pad = (K - 1) * self.dilation
        # tensor-product factors (CP decomposition of the (d,d,K) conv tensor)
        self.A = nn.Parameter(torch.empty(rank, d))   # out-channel factor
        self.B = nn.Parameter(torch.empty(rank, d))   # in-channel factor
        self.Kf = nn.Parameter(torch.empty(rank, K))  # kernel-tap factor
        nn.init.normal_(self.A, std=d ** -0.5)
        nn.init.normal_(self.B, std=d ** -0.5)
        nn.init.normal_(self.Kf, std=K ** -0.5)
        if base:
            # small dense base so the expert is never strictly rank-R limited
            self.base = nn.Parameter(torch.zeros(d, d, K))
            nn.init.normal_(self.base, std=(d * K) ** -0.5 * 0.1)
        else:
            self.register_parameter("base", None)
        self.bias = nn.Parameter(torch.zeros(d))
        self.act = nn.GELU()

    def materialized_weight(self) -> torch.Tensor:
        """Compose the TP factors (+ base) into the dense (d_out, d_in, K) conv
        weight that nn.Conv1d / the .clm format expects. einsum: r o, r i, r k -> o i k."""
        W = torch.einsum("ro,ri,rk->oik", self.A, self.B, self.Kf)
        if self.base is not None:
            W = W + self.base
        return W

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # x: (B, C, T) ; causal left-pad then functional conv with materialized W
        W = self.materialized_weight()
        xp = F.pad(x, (self.pad, 0))
        y = F.conv1d(xp, W, self.bias, dilation=self.dilation)
        return self.act(y)


def install_tlora_experts(model: CLMConvMoE, rank: int, base: bool):
    """Replace every ConvExpert in model.moe.experts with a TLoRAConvExpert
    (N1). Returns the new ModuleList so the optimizer sees the TP factors."""
    cfg = model.cfg
    new = nn.ModuleList(TLoRAConvExpert(cfg, rank, base)
                        for _ in range(len(model.moe.experts)))
    model.moe.experts = new
    return new


def tlora_aware_split(mito, parent: int, opt) -> int:
    """Mitosis cell-division for TLoRA experts (parity with MitosisMoE.split, but
    operating on the TP factors instead of .conv.conv).

    MitosisMoE.split() assumes a standard ConvExpert (.conv.conv Conv1d);
    TLoRAConvExpert has TP factors (A,B,Kf[,base],bias) instead. We replicate the
    same semantics: child = clone(parent) + tiny alternating perturbation, router
    row copied, both children's router bias -= ln2, Adam moments reset. This keeps
    the savant×mitosis recipe identical (only the expert PARAMETERIZATION differs,
    which is exactly the single variable under test)."""
    if mito.e_active >= mito.emax:
        return mito.e_active
    import torch as _t
    with _t.no_grad():
        child = mito.e_active
        moe = mito.model.moe
        pe = moe.experts[parent]; ce = moe.experts[child]
        touched = []
        for name in ("A", "B", "Kf", "base", "bias"):
            pp = getattr(pe, name, None); cp = getattr(ce, name, None)
            if pp is None or cp is None:
                continue
            flat = pp.detach().clone().reshape(-1)
            eps = _t.full_like(flat, 1e-4); eps[1::2] = -1e-4
            cp.copy_((flat + eps).reshape(pp.shape))
            touched += [pp, cp]
        rw = moe.router.weight; rb = moe.router.bias
        rw[child].copy_(rw[parent])
        pb = rb[parent].item()
        rb[parent] = pb - LN2; rb[child] = pb - LN2
        touched += [rw, rb]
        for p in touched:
            st = opt.state.get(p, None)
            if st:
                if "exp_avg" in st: st["exp_avg"].zero_()
                if "exp_avg_sq" in st: st["exp_avg_sq"].zero_()
        mito.active_mask[child] = 1.0
        mito.e_active = child + 1
        return mito.e_active


def materialize_experts_into_state(model: CLMConvMoE):
    """Return a state_dict where each TLoRA expert is written under the STANDARD
    keys 'moe.experts.{j}.conv.conv.{weight,bias}' (the dense form serialize_v3
    reads). Non-expert keys pass through unchanged. This is what makes the .clm
    engine-loadable despite the reparameterization."""
    sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
    out = {k: v for k, v in sd.items() if not k.startswith("moe.experts.")}
    for j, e in enumerate(model.moe.experts):
        if isinstance(e, TLoRAConvExpert):
            out[f"moe.experts.{j}.conv.conv.weight"] = e.materialized_weight().detach().cpu()
            out[f"moe.experts.{j}.conv.conv.bias"] = e.bias.detach().cpu()
        else:  # plain ConvExpert (ctrl) — already standard keys, copy through
            for k, v in sd.items():
                if k.startswith(f"moe.experts.{j}."):
                    out[k] = v
    return out


# ════════════════════════════════════════════════════════════════════════════
#  N3 — DBES expert-specialization diagnostic (MEASURE-ONLY, gradient-free).
# ════════════════════════════════════════════════════════════════════════════
@torch.no_grad()
def dbes_specialization(model: CLMConvMoE, x: torch.Tensor) -> dict:
    """Differentiation-of-Behaviour Expert Specialization (DBES, 2605.18523).

    On a batch x (B,T) of bytes, run the trunk up to the MoE input, then:
      * expert_div = mean pairwise (1 - cosine) between expert OUTPUT maps
                     (how differently the experts transform the same input).
      * router_entropy = mean per-token routing entropy (nats).
      * usage_gini = Gini of mean per-expert routing mass (1=one expert hogs all).
    Low expert_div + low usage spread => experts are NOT differentiated, a
    candidate cause of a ρ·weave recombination floor (former G1). Pure diagnostic — no grad."""
    b = model
    h = b.embed(x).transpose(1, 2)
    h = b.embed_conv(h)
    for layer in b.trunk:
        h = layer(h)
    # expert outputs on the SAME pre-MoE activation
    outs = []
    for e in b.moe.experts:
        outs.append(e(h))                          # (B, C, T)
    n_e = len(outs)
    # pairwise output cosine distance (flatten B,C,T)
    flat = [o.reshape(-1) for o in outs]
    div, npair = 0.0, 0
    for i in range(n_e):
        for j in range(i + 1, n_e):
            cos = F.cosine_similarity(flat[i], flat[j], dim=0).item()
            div += (1.0 - cos); npair += 1
    expert_div = (div / npair) if npair else 0.0
    # router stats
    logits = b.moe.router(h)                        # (B, n_e, T)
    probs = F.softmax(logits, dim=1)
    ent = -(probs * torch.log(probs + 1e-9)).sum(dim=1).mean().item()
    usage = probs.mean(dim=(0, 2))                  # (n_e,)
    u = torch.sort(usage).values
    nn_ = u.numel()
    # Gini = (2*sum(i*u_i)/(n*sum u) ) - (n+1)/n
    idx = torch.arange(1, nn_ + 1, dtype=u.dtype, device=u.device)
    gini = (2.0 * (idx * u).sum() / (nn_ * u.sum() + 1e-9) - (nn_ + 1) / nn_).item()
    return {"expert_div": round(expert_div, 5),
            "router_entropy": round(ent, 5),
            "usage_gini": round(gini, 5),
            "usage": [round(float(z), 5) for z in usage.tolist()],
            "n_experts": n_e}


def phi_envelope_tick(core_model, step: int) -> dict:
    """H_9846 — ONE structure-envelope reading of the parameter tensors. MONITOR-ONLY.

    The `units` vector is one RMS per parameter tensor, in sorted-name order (arch-agnostic:
    identical treatment for clm and bytegpt, and no dependence on module traversal order).
    `core/phi_envelope_monitor.py` turns that vector into the envelope statistics.

    THREE PROPERTIES, all deliberate, all checkable in this function's body:
      · no_grad + `.detach()`      — no graph, so the value CANNOT reach the loss.
      · no tensor is CREATED       — the RMS is computed by reducing the param in place, so
                                     there is no CPU/CUDA device-mismatch surface (train-py-1:
                                     a monitor-only tick with exactly that bug killed a run).
      · no RNG draw, no forward    — so a run with the watch ON and the same run with it OFF
                                     are byte-identical, which is what makes 'never in the
                                     loss' a proof instead of a claim (a_train_inline_gauge).
    Nothing returned here is Φ (a_phi_iit4_tool); the names say what the arithmetic is."""
    with torch.no_grad():
        units = [float(p.detach().float().pow(2).mean().sqrt())
                 for _, p in sorted(core_model.named_parameters(), key=lambda kv: kv[0])
                 if p.numel() > 0]
    rec = PEM.unit_structure(units)
    rec["step"] = step
    return rec


# ════════════════════════════════════════════════════════════════════════════
#  N8 — jamo (자모) compositional teach signal. We predict, per Hangul-syllable
#  byte position, a coarse jamo class so the trunk learns sub-character structure.
#  Hangul syllables are UTF-8 3-byte sequences (0xEA..0xED leading); we derive a
#  cheap jamo-bucket target from the syllable code point's (lead, vowel, tail).
# ════════════════════════════════════════════════════════════════════════════
class JamoHead(nn.Module):
    """Aux head: trunk penultimate -> coarse jamo class logits. Dropped at serialize."""
    def __init__(self, d, n_jamo=64):
        super().__init__()
        self.proj = nn.Conv1d(d, n_jamo, 1)
        self.n_jamo = n_jamo

    def forward(self, h):  # h: (B, d, T) -> (B, n_jamo, T)
        return self.proj(h)


def jamo_targets(tokens: torch.Tensor, n_jamo: int) -> torch.Tensor:
    """Map each byte to a coarse jamo bucket (0=non-Hangul-lead). Cheap, byte-level:
    Hangul UTF-8 lead bytes 0xEA-0xED get a bucket from (byte & 0x3f) % (n_jamo-1) +1,
    everything else -> 0 (ignored class). This is a weak teach signal that biases the
    trunk toward Korean sub-character regularity without needing a full jamo decomposer."""
    is_lead = (tokens >= 0xEA) & (tokens <= 0xED)
    bucket = ((tokens & 0x3F) % (n_jamo - 1)) + 1
    return torch.where(is_lead, bucket, torch.zeros_like(tokens))


# ════════════════════════════════════════════════════════════════════════════
#  Objective heads (carried over from objrun H_1602 — OPTIONAL coupling).
# ════════════════════════════════════════════════════════════════════════════
def _ce(logits, targets, V):
    return F.cross_entropy(logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1))


# ── H_9811 ANSWER-WEIGHTED CE (v4 H_004 amendment A1, ported) ──────────────────────────────
# Why this exists, measured not assumed: on the H_9810 binding panel the answer is 12 bytes of a
# ~190 B line (~6%), so a plain next-byte CE spends essentially all of its gradient on the
# surface and leaves the binding bit at chance. Measured on a toy (d=64 L=2, 1200 steps,
# val_CE 0.084): d_acc 0.5000 = EXACTLY chance on DRILLED lexemes with one answer token emitted
# on 68-86% of slots — a constant predictor, and the scorer refuses to read any Δ off it. It is
# not undertraining: 5.9x params and 6.7x steps made it WORSE (top_ans 100.0%). v4 fixed the same
# failure with `ce_surf + 5·ce_ans`; this is that term.
ANSWER_MARKER = b" => "



# ── H_9813 SERIALIZE-PARITY (does the .clm preserve what the model learned?) ──────────────
# Why this exists, measured not assumed: H_9811's pre-registered budget ladder produced two
# numbers from the SAME command that refute each other. Training-side answer CE fell to
# ans_ce = 0.0001 (chance ~0.347) — the model predicts the answer bytes essentially perfectly —
# while scoring the .clm that same run wrote read d_acc 0.5000 with top_ans 1.0000 and a
# margin_sd of 8.867 (confidently WRONG). Window alignment (--win 78/80/96/128), the 2AFC scorer
# and the budget were each excluded, which left exactly one span: the trained torch model ↔ the
# serialized (int4-quantised) .clm. Nothing in the repo measured that span, so the ladder had to
# close as INSTRUMENT-INVALID rather than as a substrate fact.
#
# The trainer is the ONLY place that holds BOTH ends at once, so the check lives here. It is a
# comparison, not a verdict: it reports where the two paths disagree and never says the model is
# good or bad.
def serialize_parity(model, out_path, panel_path, device, max_items=32):
    """2AFC on the same panel through BOTH paths. Returns a dict; prints a compact report."""
    import json as _json
    import math as _math
    import numpy as _np
    with open(panel_path, encoding="utf-8") as fh:
        man = _json.load(fh)
    items = man["items"][:max_items]
    answers = man["answers"]
    L = len(answers[0])
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "core"))
    import decode as D                                   # core/decode.py — the numpy .clm path
    W = D.clm_load_weights(out_path)
    T = max(len(it["surface"].encode()) for it in items) + L * len(items[0]["conjuncts"]) + 2

    def nll_torch(prefix, cont):
        ids = torch.tensor([list((prefix + cont).encode())], dtype=torch.long, device=device)
        with torch.no_grad():
            lg = model(ids[:, :-1], ids[:, 1:])["logits"].float()      # (1, V, T-1)
        lp = torch.log_softmax(lg, dim=1)[0]
        k = len(cont.encode())
        tgt = ids[0, 1:]
        return float(-sum(lp[int(tgt[i]), i] for i in range(lp.shape[1] - k, lp.shape[1])))

    def nll_clm(prefix, cont):
        tok = D._seed_to_tok(prefix + cont, T)
        lg = D._fwd_logits(W, tok, T)
        k = len(cont.encode())
        tot = 0.0
        for i in range(max(0, T - 1 - k), T - 1):
            row = lg[i]
            m = float(_np.max(row))
            tot += m + _math.log(float(_np.sum(_np.exp(row - m))) + 1e-30) - float(row[int(tok[i + 1])])
        return tot

    agree = t_hit = c_hit = n = 0
    for it in items:
        gold = it["gold_pattern"]
        for k in range(len(it["conjuncts"])):
            prefix = it["surface"] + gold[:L * k]
            g = gold[L * k:L * (k + 1)]
            a = answers[0] if g == answers[1] else answers[1]
            tg, ta = nll_torch(prefix, g), nll_torch(prefix, a)
            cg, ca = nll_clm(prefix, g), nll_clm(prefix, a)
            t_ok, c_ok = tg < ta, cg < ca
            t_hit += int(t_ok); c_hit += int(c_ok); agree += int(t_ok == c_ok); n += 1
    r = {"n": n, "torch_d_acc": t_hit / n, "clm_d_acc": c_hit / n, "agreement": agree / n}
    print("  SERIALIZE-PARITY (H_9813 · n=%d 2AFC slots · same prefixes both paths)" % n)
    print("    torch model  d_acc %.4f" % r["torch_d_acc"])
    print("    .clm decode  d_acc %.4f" % r["clm_d_acc"])
    print("    agreement    %.4f  %s" % (r["agreement"],
          "✅ 두 경로 일치 — 직렬화는 답 예측을 보존한다" if r["agreement"] >= 0.95 else
          "⛔ 두 경로 불일치 — .clm 이 학습된 답 예측을 잃는다(이 span 이 범인)"))

    # ── GN NON-CAUSAL LEAK ARM (H_9813) ────────────────────────────────────────────────────
    # Why: `ans_ce` fell to 0.0001 while the SAME model scores at chance on isolated sentences,
    # and the drill is epoch-shuffled + windows are independent — so the predictability must
    # live INSIDE the teacher-forced window. GroupNorm(1,C) here reduces over (C,T): SEQUENCE-
    # GLOBAL statistics, i.e. NON-CAUSAL (the documented GN bus, H_9560/H_9611 lineage). Under
    # teacher forcing the answer bytes sit in the window, so every position can read them
    # through the normalization statistics.
    # The probe: the FIRST answer byte's prediction cannot causally depend on the answer bytes.
    # Forward the same stream-style window twice — answers present in the INPUT vs masked to
    # 'q' (targets unchanged) — and compare NLL at that first-answer-byte position. Any drop
    # from masked -> present is pure non-causal leak.
    q = ord("q")
    pres = mask = 0.0
    m = 0
    for j, it in enumerate(items):
        line = it["surface"] + it["gold_pattern"]
        prev = items[(j + 1) % len(items)]["surface"] + items[(j + 1) % len(items)]["gold_pattern"]
        window = (prev + "\n" + line).encode()[-96:]
        ids = torch.tensor([list(window)], dtype=torch.long, device=device)
        ans_len = len(it["gold_pattern"].encode())
        first_ans = len(window) - ans_len          # index in window of the first answer byte
        x_true, y = ids[:, :-1], ids[:, 1:]
        x_msk = x_true.clone()
        x_msk[0, first_ans:] = q                   # mask answer bytes in the INPUT only
        with torch.no_grad():
            lp_t = torch.log_softmax(model(x_true, y)["logits"].float(), dim=1)[0]
            lp_m = torch.log_softmax(model(x_msk, y)["logits"].float(), dim=1)[0]
        pos = first_ans - 1                        # logits at pos predict the first answer byte
        tgt = int(y[0, pos])
        pres += float(-lp_t[tgt, pos]); mask += float(-lp_m[tgt, pos]); m += 1
    r["gn_present"] = pres / m; r["gn_masked"] = mask / m
    r["gn_leak"] = r["gn_masked"] - r["gn_present"]
    print("  GN NON-CAUSAL LEAK (first answer byte · answers present vs masked in INPUT · n=%d)" % m)
    print("    NLL present %.4f · masked %.4f · Δ %.4f  %s" % (
        r["gn_present"], r["gn_masked"], r["gn_leak"],
        "⛔ 비인과 누출 — 답이 GN 통계로 자기 자신을 알린다(ans_ce 는 이 채널로 부풀려짐)"
        if r["gn_leak"] > 0.1 else "✅ 누출 없음 — ans_ce 의 예측력은 인과 경로에서 온다"))
    return r


def answer_position_mask(targets, marker=ANSWER_MARKER):
    """(B, T) bool — True on target positions that lie in the ANSWER span of an arrow line.

    The arrow-line corpora (`corpus flat|bindpanel|derivtrace|…`) put the answer after a literal
    ` => ` and end the line at a newline, so the span is 'after the LAST marker, UP TO the next
    newline'. Rows with no marker contribute no weighted positions (mask all False) — a corpus
    without arrow lines is therefore a no-op rather than a silent mis-weighting.

    ⚠️ THE NEWLINE BOUND IS THE WHOLE POINT, and its absence was a measured bug. The first version
    ran the span to the END OF THE WINDOW. Training windows are cut from the CONCATENATED corpus,
    so 'after the marker' swept the answer AND the entire next line's surface: on a K=2 bindpanel
    at seq_len 96 x batch 8 (= 768 target positions) the mask marked ans_n = 365 of them for a
    4-BYTE answer — ~99% of the weighted mass was next-line surface. That is why
    `--answer-ce-weight 5.0` and even 20.0 moved nothing (H_9811): the term was real, fired every
    step, and weighted almost everything except the answer.
    """
    B, T = targets.shape
    mk = torch.tensor(list(marker), dtype=targets.dtype, device=targets.device)
    n = mk.numel()
    if T < n:
        return torch.zeros_like(targets, dtype=torch.bool)
    # windows[b, t] == True iff targets[b, t:t+n] == marker
    win = targets.unfold(1, n, 1) == mk.view(1, 1, n)
    hit = win.all(dim=2)                                   # (B, T-n+1)
    idx = torch.arange(hit.shape[1], device=targets.device).view(1, -1)
    last = torch.where(hit, idx, torch.full_like(idx, -1)).max(dim=1).values   # -1 ⇒ no marker
    pos = torch.arange(T, device=targets.device).view(1, -1)
    start = (last + n).view(-1, 1)
    after = (pos >= start) & (last.view(-1, 1) >= 0)
    # right bound: the first newline at or after `start` closes the answer span
    nl = targets == 10
    nl_after = nl & after
    big = torch.full_like(pos.expand(B, T), T)
    first_nl = torch.where(nl_after, pos.expand(B, T), big).min(dim=1).values.view(-1, 1)
    return after & (pos < first_nl)


def answer_ce(logits, targets, V, marker=ANSWER_MARKER):
    """Mean CE over ANSWER positions only. Returns (loss, n_positions); loss is 0 when none."""
    mask = answer_position_mask(targets, marker)
    n = int(mask.sum())
    if n == 0:
        return logits.sum() * 0.0, 0
    lg = logits.transpose(1, 2).reshape(-1, V)[mask.reshape(-1)]
    tg = targets.reshape(-1)[mask.reshape(-1)]
    return F.cross_entropy(lg, tg), n


# NOTE (H_1640): every objective now accepts an OPTIONAL penultimate=(B,d,T) kwarg
# (the post-MoE pre-readout trunk site). The inherited objectives ignore it; the new
# compositional objectives consume it. Plain-function objectives have no params; the
# two aux-head objectives are nn.Modules whose params are added to the optimizer in
# main() and DROPPED at serialize (they never enter model.state_dict).
def loss_ce_marginal(logits, targets, V, gen, penultimate=None):
    return _ce(logits, targets, V), {}


def loss_ce_marginal_shuffled(logits, targets, V, gen, penultimate=None):
    # H_9954/H_9960 MANDATORY control: derange targets across the batch (roll by 1 row) so every
    # position keeps its exact target marginal but NO row keeps its own labels — a gradient-step-
    # matched shuffled-label arm. Requires batch>=2.
    if targets.shape[0] < 2:
        raise ValueError("ce_marginal_shuffled needs batch-size>=2 (row-derange control)")
    y_ctl = torch.roll(targets, shifts=1, dims=0)
    return _ce(logits, y_ctl, V), {}


def loss_infonce(logits, targets, V, gen, penultimate=None):
    ce = _ce(logits, targets, V)
    lg = logits.transpose(1, 2).reshape(-1, V)
    tgt = targets.reshape(-1); N = tgt.shape[0]
    pos = lg.gather(1, tgt.unsqueeze(1))
    neg_idx = torch.randint(0, V, (N, INFONCE_NEG), generator=gen, device=lg.device)
    neg = lg.gather(1, neg_idx).masked_fill(neg_idx == tgt.unsqueeze(1), float("-inf"))
    cand = torch.cat([pos, neg], dim=1)
    infonce = F.cross_entropy(cand, torch.zeros(N, dtype=torch.long, device=lg.device))
    return ce + INFONCE_LAMBDA * infonce, {"infonce": float(infonce.detach())}


def loss_contrastive_equilibrium(logits, targets, V, gen, penultimate=None):
    ce = _ce(logits, targets, V)
    lg = logits.transpose(1, 2).reshape(-1, V); tgt = targets.reshape(-1)
    logp = F.log_softmax(lg, dim=1)
    e_pos = -logp.gather(1, tgt.unsqueeze(1)).mean()
    with torch.no_grad():
        samp = torch.multinomial(logp.exp(), 1, generator=gen).squeeze(1)
    e_neg = -logp.gather(1, samp.unsqueeze(1)).mean()
    eq = F.relu(e_pos - e_neg + EQ_MARGIN)
    return ce + EQ_LAMBDA * eq, {"e_pos": float(e_pos.detach()),
                                 "e_neg": float(e_neg.detach()), "eq": float(eq.detach())}


# ════════════════════════════════════════════════════════════════════════════
#  ▛▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀ NEW OBJECTIVES (H_1640) ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▛
#  Three NEW compositional TRAINING-OBJECTIVE loss functions added to CE. Each is a
#  training-side pressure that reshapes the gradient the TRUNK receives (not a readout
#  op). Verdict later = engine-native `anima-py evaluate` on the frozen G1 bar.
# ════════════════════════════════════════════════════════════════════════════

# ── LEVER 1: predictive_info — multi-step predictive-coding aux ───────────────
class PredictiveInfoObjective(nn.Module):
    """Reward the trunk penultimate h_t for carrying predictive info about FUTURE
    tokens k=2,3,4 steps ahead, not just the immediate next token (which CE already
    covers). One linear head per horizon maps h_t -> V-way logits over token y_{t+j}.

        aux = mean_j  CE( head_j(h[:, :, :T-j]) ,  y[:, j:] )        (j in HORIZONS-1)

    (y is already next-token, so y[:,0] = token after x_0; predicting y[:,j:] from
    h[:, :, :T-j] means predicting the token j positions further ahead.) This is the
    predictive-information bottleneck / CPC objective (Bialek-Tishby predictive
    information; van den Oord CPC 1807.03748; Rao&Ballard predictive coding): to
    minimize it the trunk must compress the context into a code that stays predictive
    multiple steps out, which requires COMPOSING context factors rather than memorizing
    the 1-step marginal. Heads are DROPPED at serialize (engine reads only the additive
    1-step readout)."""

    def __init__(self, d, V, horizons=PREDINFO_HORIZONS, lam=PREDINFO_LAMBDA):
        super().__init__()
        self.horizons = tuple(int(j) - 1 for j in horizons)   # steps BEYOND next-token
        self.lam = lam; self.V = V
        self.heads = nn.ModuleList(nn.Conv1d(d, V, 1) for _ in self.horizons)

    def forward(self, logits, targets, V, gen, penultimate=None):
        ce = _ce(logits, targets, V)
        if penultimate is None:
            return ce, {}
        h = penultimate                                    # (B, d, T)
        T = h.shape[-1]
        terms = []
        for hd, j in zip(self.heads, self.horizons):
            if j <= 0 or T - j < 1:
                continue
            pl = hd(h[:, :, :T - j])                        # (B, V, T-j)
            pt = targets[:, j:]                             # (B, T-j) token j-ahead
            terms.append(F.cross_entropy(
                pl.transpose(1, 2).reshape(-1, V), pt.reshape(-1)))
        if not terms:
            return ce, {}
        aux = torch.stack(terms).mean()
        return ce + self.lam * aux, {"predinfo": float(aux.detach()),
                                     "predinfo_h": len(terms)}


# ── LEVER 2: constructive_bind — HRR trained-bind reconstruction aux ──────────
def _circ_conv(a, b):
    """Circular convolution (HRR binding) along the last dim via FFT. Real inputs."""
    fa = torch.fft.rfft(a, dim=-1); fb = torch.fft.rfft(b, dim=-1)
    return torch.fft.irfft(fa * fb, n=a.shape[-1], dim=-1)


def _circ_corr(c, a):
    """Circular correlation (HRR UNbinding): recover b from c=a⊛b given a.
    unbind(c, a) = c ⊛ involution(a); in Fourier: irfft( conj(fft a) * fft c )."""
    fc = torch.fft.rfft(c, dim=-1); fa = torch.fft.rfft(a, dim=-1)
    return torch.fft.irfft(torch.conj(fa) * fc, n=c.shape[-1], dim=-1)


class ConstructiveBindObjective(nn.Module):
    """TRAINED CONSTRUCTIVE BIND on the trunk penultimate (the untried framebreak piece).

    From each penultimate vector h_t, two learned linear projections extract a ROLE r_t
    and a FILLER f_t (dim m). They are BOUND by circular convolution c_t = r_t ⊛ f_t
    (Plate 1995 Holographic Reduced Representations / Smolensky 1990 Tensor-Product
    Representations — VSA binding). Two constraints sculpt a COMPOSITIONAL code:

      (1) UNBIND-RECOVERS-FILLER: unbind(c_t, r_t) ≈ f_t  →  1 - cos(f_hat, f_t).
          Forces the bound composite to actually SUPPORT clean decomposition (a real
          bind, not an additive blur — the exact property a pure additive readout lacks).
      (2) COMPOSITE-PREDICTS-NEXT: a linear decoder maps the bound c_t to next-token
          logits, CE against y_t. Forces the binding to carry TASK signal, so gradient
          sculpts task-relevant compositional factors into the trunk.

        aux = CBIND_UNBIND_W * (1 - cos(unbind(r⊛f, r), f)).mean()
            + CBIND_PRED_W   * CE(dec(r⊛f), y)

    All of {Wr, Wf, dec} live OUTSIDE model.state_dict → DROPPED at serialize; the
    engine reads only the standard additive readout. Gradient flows into the trunk
    through h_t, so the trunk is pushed toward a bind-decomposable representation."""

    def __init__(self, d, V, m=CBIND_DIM, lam=CBIND_LAMBDA):
        super().__init__()
        self.m = m; self.lam = lam; self.V = V
        self.role = nn.Conv1d(d, m, 1)
        self.fill = nn.Conv1d(d, m, 1)
        self.dec = nn.Conv1d(m, V, 1)     # bound composite -> next-token logits

    def forward(self, logits, targets, V, gen, penultimate=None):
        ce = _ce(logits, targets, V)
        if penultimate is None:
            return ce, {}
        h = penultimate                                # (B, d, T)
        r = self.role(h).transpose(1, 2)               # (B, T, m)
        f = self.fill(h).transpose(1, 2)               # (B, T, m)
        c = _circ_conv(r, f)                           # (B, T, m) bound composite
        # (1) unbind must recover the filler
        f_hat = _circ_corr(c, r)                        # (B, T, m)
        unbind = (1.0 - F.cosine_similarity(f_hat, f, dim=-1)).mean()
        # (2) bound composite must predict the next token
        dec_logits = self.dec(c.transpose(1, 2))        # (B, V, T)
        pred = F.cross_entropy(
            dec_logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1))
        aux = CBIND_UNBIND_W * unbind + CBIND_PRED_W * pred
        return ce + self.lam * aux, {"cbind_unbind": float(unbind.detach()),
                                     "cbind_pred": float(pred.detach()),
                                     "cbind": float(aux.detach())}


# ── LEVER 3: composed_nce — composed-negative (wrong-composition) InfoNCE ─────
def loss_composed_nce(logits, targets, V, gen, penultimate=None):
    """InfoNCE whose negatives are the SAME bag of tokens present in the window but at
    the WRONG position (targets permuted WITHIN each sequence) = same-concept-set /
    wrong-composition. Contrasting the true token->position assignment against these
    hard negatives directly rewards getting the COMPOSITION right, not merely the
    concept set (plain infonce uses RANDOM vocab negatives = membership-only).

        pos_n   = logit[n, y_t]                              (right token here)
        neg_n,p = logit[n, y_perm_p(t)]  for p=1..CNCE_PERMS (a within-window token
                                                              assigned to the wrong slot)
        L = CE( [pos, neg...] , 0 )                          softmax over the assignment

    Operates on the readout logits — no aux params; gradient flows readout->trunk. A
    permuted token that coincides with the true target is masked to -inf (not a negative)."""
    ce = _ce(logits, targets, V)
    B, Vv, T = logits.shape
    lg = logits.transpose(1, 2).reshape(-1, Vv)        # (B*T, V)
    tgt = targets.reshape(-1)                          # (B*T,)
    N = tgt.shape[0]
    pos = lg.gather(1, tgt.unsqueeze(1))               # (N,1)
    negs = []
    for _ in range(CNCE_PERMS):
        # independent within-sequence permutation of the target order per batch row
        perm = torch.stack([torch.randperm(T, generator=gen, device=logits.device)
                            for _ in range(B)])         # (B, T)
        y_perm = targets.gather(1, perm).reshape(-1)    # (N,) same bag, wrong slots
        s = lg.gather(1, y_perm.unsqueeze(1))           # (N,1)
        s = s.masked_fill((y_perm == tgt).unsqueeze(1), float("-inf"))
        negs.append(s)
    cand = torch.cat([pos] + negs, dim=1)              # (N, 1+CNCE_PERMS)
    cnce = F.cross_entropy(cand, torch.zeros(N, dtype=torch.long, device=lg.device))
    return ce + CNCE_LAMBDA * cnce, {"composed_nce": float(cnce.detach())}


# Objective registry. Value = a BUILDER(d, V, device) so the two aux-head objectives can
# allocate learnable params; the plain-function ones ignore the args and return the fn.
# `needs_penultimate` marks which objectives consume the trunk penultimate site.
OBJECTIVE_BUILDERS = {
    "ce_marginal":             lambda d, V, dev: loss_ce_marginal,
    "ce_marginal_shuffled":    lambda d, V, dev: loss_ce_marginal_shuffled,
    "infonce":                 lambda d, V, dev: loss_infonce,
    "contrastive_equilibrium": lambda d, V, dev: loss_contrastive_equilibrium,
    "predictive_info":         lambda d, V, dev: PredictiveInfoObjective(d, V).to(dev),
    "constructive_bind":       lambda d, V, dev: ConstructiveBindObjective(d, V).to(dev),
    "composed_nce":            lambda d, V, dev: loss_composed_nce,
}
OBJ_NEEDS_PENULTIMATE = {"predictive_info", "constructive_bind"}
OBJECTIVES = OBJECTIVE_BUILDERS   # back-compat alias for --objective choices list

# arm -> (tlora_on, dict_aux_on, jamo_aux_on)
ARMS = {
    "ctrl":       (False, False, False),
    "tlora":      (True,  False, False),
    "tlora_dict": (True,  True,  False),
    "tlora_jamo": (True,  False, True),
}


# ════════════════════════════════════════════════════════════════════════════
# WARM-START (`--init`) — load a base ckpt's weights into a freshly-built model.
#   The KEYSTONE for continue-training / warm-FT (e.g. ρ·form🟢 (former G0) h1129 trunk → ρ·weave (former G1) lever
#   test, per memory g1-fromscratch-blocked-by-g0-undertrain). Symmetric with
#   serialize: ByteGPT `.bin` is read by core/serialize.deserialize_bytegpt (the
#   byte-inverse of serialize()); `.pt` is a plain torch state_dict. H_247 lesson —
#   a silent shape mismatch can floor +2.5 nats, so every path shape-guards HARD.
# ════════════════════════════════════════════════════════════════════════════
def _warm_start(model, init_path, is_bytegpt, expect_cfg):
    """Load weights from `init_path` into `model` in place. Returns a 1-line report str.

    expect_cfg = {vocab,d,n_layer,n_head,block} of the freshly-built model (bytegpt) or
    {d,L} (clm). Raises ValueError on any dim/layer mismatch (H_247 hard guard)."""
    low = str(init_path).lower()
    if low.endswith(".clm"):
        # A `.clm` IS a warm-start source (core/serialize.deserialize_v3). The old refusal
        # ("dequant->state_dict remap is a follow-on") was a practical trap: pods get torn down,
        # only the `.clm` is pulled (a_fire_recover_complete), the `.pt` is gone, and every
        # warm-start experiment on that checkpoint dies for want of an inverse rather than for any
        # scientific reason. H_9313 hit exactly that — the C34 `.pt` no longer exists anywhere.
        #
        # The H_247 quant-noise worry does not apply here, and the reason is worth stating: the
        # int4 weights are not an approximation of some better original we are degrading. They ARE
        # the weights core/decode.py runs, and every number this lane has ever measured came out of
        # decoding them. Warm-starting from the dequantized values therefore starts training from
        # exactly the model we measured. `clm_roundtrip_is_identity` proves the inverse is exact by
        # re-serializing and comparing the file BYTE for BYTE — asserted below on the real file, so
        # a post-training delta can never be a dequantization artifact.
        if is_bytegpt:
            raise ValueError(f"--init {init_path}: a `.clm` is a CLM ckpt but --arch=bytegpt.")
        L = int(expect_cfg["L"])
        E = int(expect_cfg.get("E", 3))
        if not S.clm_roundtrip_is_identity(init_path, L, E):
            raise ValueError(
                f"--init {init_path}: .clm round-trip is NOT byte-identical at (L={L}, E={E}) — "
                f"the deserializer and this model's (L,E) disagree. Refusing to warm-start from a "
                f"checkpoint we cannot reproduce: a silent mis-parse would arrive looking exactly "
                f"like a training result.")
        np_sd = S.deserialize_v3(init_path, L, E)
        sd = {k: torch.from_numpy(v) for k, v in np_sd.items()}
        with open(init_path, "rb") as init_file:
            raw = init_file.read()
        main_n = len(S._pack_main_blob(np_sd, L, E))
        source_norm = S.serialized_trunk_norm(
            raw, main_n, int(np_sd["embed.weight"].shape[1]),
            int(np_sd["embed.weight"].shape[0]))
        expected_norm = expect_cfg.get("trunk_norm")
        if expected_norm is not None and source_norm != expected_norm:
            raise ValueError(
                f"--init {init_path}: trunk_norm={source_norm} in the serialized checkpoint "
                f"but the requested model uses trunk_norm={expected_norm}. This changes the "
                "forward pass even when every trunk tensor is frozen. Match --trunk-norm to the "
                "source checkpoint, or run an explicitly separate non-frozen conversion study.")
        next_magic = raw[main_n:main_n + 4]
        slw_loaded = False
        clms_status = "absent"
        if next_magic == bytes([83, 76, 87, 1]):
            if getattr(model, "slw", None) is None:
                raise ValueError(
                    f"--init {init_path}: checkpoint carries an SLW trailer but the built model "
                    "does not. Pass --slw with matching --slw-n-slot/--slw-k; silently dropping "
                    "a trained memory lane would not be a valid warm-start.")
            from slw import read_slw
            sw, sw_end = read_slw(raw, main_n)
            if sw is None:
                raise ValueError(f"--init {init_path}: malformed SLW trailer")
            mod = model.slw
            if (int(sw["n_slot"]), int(sw["k"]), int(sw["d_s"])) != \
                    (int(mod.n_slot), int(mod.k), int(mod.d_s)):
                raise ValueError(
                    f"--init {init_path}: SLW shape {(sw['n_slot'], sw['k'], sw['d_s'])} "
                    f"!= built {(mod.n_slot, mod.k, mod.d_s)}")
            slw_sd = {
                "K_slots": sw["K_slots"],
                "W_r.weight": sw["W_r"], "W_r.bias": sw["b_r"],
                "W_q.weight": sw["W_q"], "W_q.bias": sw["b_q"],
                "W_v.weight": sw["W_v"], "W_v.bias": sw["b_v"],
                "W_o.weight": sw["W_o"], "W_o.bias": sw["b_o"],
                "w_g.weight": sw["w_g"].reshape(1, -1),
                "w_g.bias": [sw["b_g"]], "gamma": sw["gamma"],
            }
            target = mod.state_dict()
            converted = {k: torch.as_tensor(v, dtype=target[k].dtype) for k, v in slw_sd.items()}
            mod.load_state_dict(converted, strict=True)
            slw_loaded = True
            next_magic = raw[sw_end:sw_end + 4] if sw_end + 4 <= len(raw) else b""
            main_n = sw_end
        # H_9928 CLMS warm-start. SLW above both restores its lane AND refuses to drop it
        # silently; CLMS had neither, so `--init <ckpt with a trained store lane>` re-initialised
        # that lane from scratch and said nothing. A 60-step run on a fresh CLMS then reads 0.4688
        # where the source ckpt reads 1.0000, and the number looks like a scientific negative
        # instead of a warm-start that never happened.
        if next_magic == bytes([67, 76, 77, 83]):                    # b"CLMS"
            if getattr(model, "clms", None) is None:
                raise ValueError(
                    f"--init {init_path}: checkpoint carries a CLMS trailer but the built model "
                    "does not. Pass --store-bridge/--freeze-trunk with matching --clms-n-slot/"
                    "--clms-d-k/--clms-d-s/--clms-r; silently dropping a trained store lane would "
                    "not be a valid warm-start.")
            from clms import read_clms, clms_weights_from_torch
            cm = model.clms
            cs, _cs_end = read_clms(raw, main_n, int(expect_cfg["d"]), int(cm.V))
            if cs is None:
                raise ValueError(f"--init {init_path}: malformed CLMS trailer")
            if (int(cs["n_slot"]), int(cs["d_k"]), int(cs["d_s"]), int(cs["r"])) != \
                    (int(cm.n_slot), int(cm.d_k), int(cm.d_s), int(cm.r)):
                raise ValueError(
                    f"--init {init_path}: CLMS shape "
                    f"{(cs['n_slot'], cs['d_k'], cs['d_s'], cs['r'])} != built "
                    f"{(cm.n_slot, cm.d_k, cm.d_s, cm.r)}")
            source_lane = int(cs.get("lane_type", 1))
            built_lane = int(clms_weights_from_torch(cm).get("lane_type", 1))
            dual_upgrade = built_lane in (8, 10) and source_lane in (2, 3, 6, 7)
            if source_lane != built_lane and not dual_upgrade:
                raise ValueError(
                    f"--init {init_path}: CLMS lane_type {source_lane} != built {built_lane}. "
                    "Only the explicit --clms-dual arity upgrade may reuse a one-read checkpoint; "
                    "silently recasting any other lane would change its semantics.")
            clms_sd = {"key_emb": cs["key_emb"], "W_q.weight": cs["W_q"].T,
                       "val": cs["val"], "W_h.weight": cs["W_h"].T, "W_h.bias": cs["b_h"],
                       "W_out.weight": cs["W_out"].T, "lam": cs["lam"]}
            if "W_g" in cs and getattr(cm, "W_g", None) is not None:
                clms_sd["W_g.weight"] = cs["W_g"].T
            ct = cm.state_dict()
            compatible = {k: torch.as_tensor(v, dtype=ct[k].dtype)
                          for k, v in clms_sd.items()
                          if k in ct and tuple(ct[k].shape) == tuple(torch.as_tensor(v).shape)}
            incompatible = sorted(k for k, v in clms_sd.items()
                                  if k in ct and tuple(ct[k].shape) != tuple(torch.as_tensor(v).shape))
            cm.load_state_dict(compatible, strict=False)
            if source_lane == built_lane:
                if incompatible:
                    raise ValueError(f"--init {init_path}: CLMS lane {source_lane} shape mismatch "
                                     f"on {incompatible}")
                clms_status = "restored"
            else:
                # Current migration only: a compatible one-read lane -> a dual lane. Shared tensors
                # retain learned state when their shapes match; legacy lane 8 alone widens W_h and
                # therefore leaves that tensor freshly initialized.
                clms_status = (f"upgraded-{source_lane}-to-{built_lane}"
                               f"(shared={len(compatible)},fresh={','.join(incompatible)})")
        model_sd = model.state_dict()
        loadable, shape_bad = {}, []
        for k, v in sd.items():                     # same H_247 hard guard as the .pt path
            if k in model_sd:
                if tuple(model_sd[k].shape) == tuple(v.shape):
                    loadable[k] = v
                else:
                    shape_bad.append(f"{k}:{tuple(v.shape)}!={tuple(model_sd[k].shape)}")
        if shape_bad:
            raise ValueError(f"--init {init_path}: shape mismatch on {shape_bad} "
                             f"(H_247: warm-init mismatch floors CE — match --d/--L/--experts).")
        if not loadable:
            raise ValueError(f"--init {init_path}: 0 keys overlap the built model "
                             f"(ckpt keys e.g. {list(sd)[:4]})")
        missing, unexpected = model.load_state_dict(loadable, strict=False)
        return WarmStartReport(
            f"warm-start ✓ .clm int4-dequant loaded {len(loadable)}/{len(model_sd)} keys "
            f"(L={L} E={E} · round-trip BYTE-IDENTICAL · trunk_norm={source_norm}"
            f" · untouched={len(missing)}"
            f" · SLW={'restored' if slw_loaded else 'absent'}"
            f" · CLMS={clms_status})")

    if low.endswith(".bin"):
        if not is_bytegpt:
            raise ValueError(f"--init {init_path}: a `.bin` is a ByteGPT engine ckpt but "
                             f"--arch=clm; use a CLM `.pt`, or --arch bytegpt.")
        sd, cfg = S.deserialize_bytegpt(init_path)
        # HARD shape guard (H_247): every header field must match the built model.
        for k in ("vocab", "d", "n_layer", "n_head", "block"):
            if int(cfg[k]) != int(expect_cfg[k]):
                raise ValueError(
                    f"--init {init_path}: ByteGPT header {k}={cfg[k]} != built model {k}="
                    f"{expect_cfg[k]}. Match --d/--L/--seq-len (H_247: warm-init mismatch floors CE).")
        missing, unexpected = model.load_state_dict(sd, strict=False)
        # tied head → tok/head share storage; only benign missing/unexpected tolerated.
        bad_missing = [k for k in missing if k not in ("head.weight",)]
        if bad_missing or unexpected:
            raise ValueError(f"--init {init_path}: state_dict key mismatch "
                             f"missing={list(missing)} unexpected={list(unexpected)}")
        return WarmStartReport(
            f"warm-start ✓ ByteGPT .bin loaded ({cfg['n_layer']}L d={cfg['d']} "
            f"block={cfg['block']}) missing={list(missing)} unexpected={list(unexpected)}")

    if low.endswith(".pt") or low.endswith(".pth"):
        ck = torch.load(init_path, map_location="cpu", weights_only=False)
        is_resume = isinstance(ck, dict) and ck.get("schema") == RESUME_SCHEMA
        sd = ck.get("model", ck) if isinstance(ck, dict) else ck
        model_sd = model.state_dict()
        # per-key HARD shape guard (H_247) — reject any shape-mismatched overlap.
        loadable, shape_bad = {}, []
        for k, v in sd.items():
            if k in model_sd:
                if tuple(model_sd[k].shape) == tuple(v.shape):
                    loadable[k] = v
                else:
                    shape_bad.append(f"{k}:{tuple(v.shape)}!={tuple(model_sd[k].shape)}")
        if shape_bad:
            raise ValueError(f"--init {init_path}: shape mismatch on {shape_bad} "
                             f"(H_247: warm-init mismatch floors CE — match --d/--L/--arch).")
        if not loadable:
            raise ValueError(f"--init {init_path}: 0 keys overlap the built model — "
                             f"wrong arch/config? (ckpt keys e.g. {list(sd)[:4]})")
        missing, unexpected = model.load_state_dict(loadable, strict=False)
        resume = None
        if is_resume:
            resume = {k: v for k, v in ck.items() if k != "model"}
        return WarmStartReport(
            f"warm-start ✓ .pt loaded {len(loadable)}/{len(model_sd)} keys "
            f"(untouched={len(missing)} extra-in-ckpt={len(sd) - len(loadable)}"
            f" · {'exact resume pending' if is_resume else 'legacy weights only'})",
            resume=resume)

    raise ValueError(f"--init {init_path}: unknown extension — expected .bin (ByteGPT engine) "
                     f"or .pt/.pth (torch state_dict).")


# ════════════════════════════════════════════════════════════════════════════
#  §4 TrainShell — composite train module (DDP wrap target).
#  Wraps (model, objfn-if-Module, jamo_head) so DistributedDataParallel's reducer
#  covers the aux-head params (predinfo/cbind heads + jamo head live OUTSIDE model —
#  wrapping only `model` would silently NEVER allreduce their grads, §10.1). forward()
#  holds the VERBATIM per-step loss-composition block (both the bf16-autocast and fp32
#  variants) relocated from the train loop, incl. trunk_penultimate as a method reading
#  self.model. N==1: the shell is called UNWRAPPED — shell(x, y, …) is the same graph +
#  op order + RNG-draw order as the pre-refactor inline block, so the .clm is byte-
#  identical (the refactor regression gate 9.1). The shell has NO own params/buffers, so
#  constructing it consumes no RNG.
# ════════════════════════════════════════════════════════════════════════════
class TrainShell(nn.Module):
    def __init__(self, model, objfn, jamo_head, *, is_bytegpt, V,
                 obj_needs_pen, dict_on, jamo_on, bf16, device):
        super().__init__()
        self.model = model
        # objfn is EITHER an nn.Module (predictive_info/constructive_bind aux heads) or a
        # plain function (ce_marginal/infonce/…). Register the module form as a submodule so
        # its params enter the DDP bucket set; keep the function form as a bare attribute.
        self.objfn = objfn if isinstance(objfn, nn.Module) else None
        self._objfn_fn = None if isinstance(objfn, nn.Module) else objfn
        self.jamo_head = jamo_head            # None when jamo off
        self.is_bytegpt = is_bytegpt
        self.V = V
        self.obj_needs_pen = obj_needs_pen
        self.dict_on = dict_on
        self.jamo_on = jamo_on
        # H_9900 composition lane — attached by the caller when --comp-lane is given. need_pen
        # must include it: the lane reads the trunk penultimate (detached) at the answer span.
        self.comp_lane = None
        self.comp_w = 1.0
        self.comp_sep = 32                            # b" "
        self.comp_end = 46                            # b"."
        self.need_pen = obj_needs_pen or dict_on or jamo_on
        self.bf16 = bf16
        self.device = device

    def _objfn(self):
        return self.objfn if self.objfn is not None else self._objfn_fn

    def trunk_penultimate(self, x):
        # VERBATIM relocation of the former module-level trunk_penultimate closure
        # (reads self.model). ByteGPT exposes its pre-head hidden directly; CLM recomputes
        # the trunk to the pre-readout MoE/norm_out site (note: pre-SLW, as before).
        m = self.model
        if self.is_bytegpt:
            return m(x)["penultimate"]              # (B, d, T) — ln_f(x) pre-head
        h = m.embed(x).transpose(1, 2)
        h = m.embed_conv(h)
        for layer in m.trunk:
            h = layer(h)
        hm, _ = m.moe(h)
        hm = m.norm_out(hm)
        return hm                                   # (B, d, T) — pre-readout dictionary site

    def ideation_forward(self, x, tap_L):
        """H_9803 — one CLM forward that also returns the PRESERVED early (layer tap_L) tap.

        Mirrors CLMConvMoE.forward's op order exactly (embed → embed_conv → trunk → faction
        bridge → MoE → norm_out → SLW → readout); it does not touch model.forward, so the golden
        path stays byte-identical. tap_L<=0 ⇒ the tap IS the penultimate (the `penult` route =
        the tap-DEPTH control, H_9720-C1 idiom: same head, only the tap LOCATION differs)."""
        m = self.model
        h = m.embed(x).transpose(1, 2)
        h = m.embed_conv(h)
        tap = None
        for i, layer in enumerate(m.trunk):
            h = layer(h)
            if tap_L > 0 and (i + 1) == tap_L:
                tap = h
        if getattr(m, "faction_bridge", None) is not None:
            h = m.faction_bridge(h)
        hm, stats = m.moe(h)
        hm = m.norm_out(hm)
        if tap is None:
            tap = hm                                   # penult route (or tap_L deeper than the trunk)
        xr = m.slw(hm) if getattr(m, "slw", None) is not None else hm
        logits = m.readout(xr)                         # (B, V, T)
        return logits, hm, tap, stats.aux_loss

    def forward(self, x, y, obj_gen, dict_lambda, jamo_lambda, sb=None, sb_w=1.0, sb_oracle=False, sb_addr_w=0.0, sb_oracle_aux=0.0, sb_tap_grad="detached",
                idl=None, idl_w=1.0, idl_assign="hungarian", idl_route="l3-disjoint",
                idl_tap_L=3, idl_gen=None, ans_w=0.0):
        # ── VERBATIM relocation of the per-step loss-composition block (bf16 + fp32). The
        #    autocast context stays wrapping ONLY the forward/compose (backward is at the
        #    callsite, outside autocast — DDP hooks fire there). Returns (loss, detached CE,
        #    aux) so the callsite can backward + all-reduce the shard CE (§3).
        model = self.model
        objfn = self._objfn()
        V = self.V
        aux = {}
        need_pen = self.need_pen
        if self.bf16 and self.device.startswith("cuda"):
            with torch.autocast("cuda", dtype=torch.bfloat16):
                out = model(x, y)
                h = self.trunk_penultimate(x) if need_pen else None
                pen = h.float() if (h is not None and self.obj_needs_pen) else None
                obj_loss, oaux = objfn(out["logits"].float(), y, V, obj_gen, penultimate=pen)
                loss = obj_loss + out["aux_loss"]
                if ans_w > 0.0:                       # H_9811 answer-weighted CE (default 0 = off)
                    ace, an = answer_ce(out["logits"].float(), y, V)
                    loss = loss + ans_w * ace
                if self.comp_lane is not None:        # H_9900 composition lane (default None = off)
                    # DETACH is the whole point: this lane's CE must not reach the trunk, or it
                    # competes with the language stratum exactly as replay does (H_9898).
                    ph = h if h is not None else self.trunk_penultimate(x)
                    assert ph is not None, "composition lane needs the trunk penultimate"
                    cl_logits = self.comp_lane(ph.float().detach())
                    cmask = _comp_answer_mask(y, self.comp_sep, self.comp_end)
                    closs = CompositionLane.loss(cl_logits, y, cmask)
                    loss = loss + self.comp_w * closs
                    aux["comp_ce"] = float(closs.detach())
                    aux["comp_span"] = float(cmask.float().mean())
                    aux["ans_ce"] = float(ace.detach()); aux["ans_n"] = an
                if self.dict_on:
                    dloss = dict_lambda * h.abs().mean()
                    loss = loss + dloss; aux["dict_l1"] = float(dloss.detach())
                if self.jamo_on:
                    jl = self.jamo_head(h.float())
                    jt = jamo_targets(y, self.jamo_head.n_jamo)
                    jloss = jamo_lambda * F.cross_entropy(
                        jl.transpose(1, 2).reshape(-1, self.jamo_head.n_jamo),
                        jt.reshape(-1), ignore_index=0)
                    loss = loss + jloss; aux["jamo"] = float(jloss.detach())
        else:
            out = model(x, y)
            h = self.trunk_penultimate(x) if need_pen else None
            pen = h if self.obj_needs_pen else None
            obj_loss, oaux = objfn(out["logits"], y, V, obj_gen, penultimate=pen)
            loss = obj_loss + out["aux_loss"]
            if ans_w > 0.0:                           # H_9811 answer-weighted CE (default 0 = off)
                ace, an = answer_ce(out["logits"], y, V)
                loss = loss + ans_w * ace
                aux["ans_ce"] = float(ace.detach()); aux["ans_n"] = an
            if self.dict_on:
                dloss = dict_lambda * h.abs().mean()
                loss = loss + dloss; aux["dict_l1"] = float(dloss.detach())
            if self.jamo_on:
                jl = self.jamo_head(h)
                jt = jamo_targets(y, self.jamo_head.n_jamo)
                jloss = jamo_lambda * F.cross_entropy(
                    jl.transpose(1, 2).reshape(-1, self.jamo_head.n_jamo),
                    jt.reshape(-1), ignore_index=0)
                loss = loss + jloss; aux["jamo"] = float(jloss.detach())
        # ── H_9423 CLMS store-bridge co-training (store_only gate via CE decomposition) ──
        # A SEPARATE fp32 forward on the line-aligned store batch. The answer-position (qpos = T-1)
        # CE is on store_logits ONLY (the CLMS lane's content-addressed lookup), so the trunk readout
        # receives NO answer-position grad = ② shortcut-cut, STRUCTURAL (= v2 store_only dlogits[ans]=0,
        # not detach — the trunk logit is never in the answer-CE graph). The non-answer rows keep the
        # ordinary trunk LM CE (the trunk learns the prompt spelling + query formation via yn_q).
        if sb is not None:
            x_s, y_s, K, pols, tgt, tgt_b, mrows = sb  # columns: A span, B span, operator
            out_s = model(x_s)                                  # (targets None → CE assembled here, fp32)
            logits_s = out_s["logits"].float()                 # (Bs, V, T)
            pen_s = out_s["pen_trunk"].float()                 # (Bs, d, T) pre-slot trunk penultimate
            Bs, _, Ts = logits_s.shape
            yn_q = pen_s[:, :, Ts - 1]                         # (Bs, d) query row (qpos = T-1, cell-asserted)
            # H_9423 Stage1.5 --store-oracle-train: hand the address for free at TRAIN time (oracle_slot=
            # target_slot) so ∂L/∂v is not gated on the softmax lookup bootstrapping first. Separates the
            # value-read layer (a) from the address-learning layer (c): if val differentiates under free
            # address (ORACLE≥.90) the residual 303M wall is pure W_q address-learning; if not, deeper.
            pair_active = tgt_b >= 0
            osl = tgt if sb_oracle else None
            osl_b = (torch.where(pair_active, tgt_b, torch.zeros_like(tgt_b))
                     if sb_oracle else None)
            # H_9720-ⓐ EN-disjoint fresh query: the address reads the DETACHED early-layer tap (store-CE
            # never pushes the trunk through this path ⇒ no EN-occupancy competition). None ⇒ W_q(yn_q).
            # H_9720 C2 detach-ablation: 'detached' (default) = store-CE never reaches the trunk through
            # this tap (disjoint · the CRACK arm) · 'shared' = drop .detach() so store-CE DOES flow into
            # layers ≤ fresh_L (tests whether gradient-disjointness is load-bearing · Fable/Sol audit C2).
            _pf = out_s.get("pen_fresh")
            if _pf is None:
                yn_fresh = None
            else:
                _fy = _pf.float()[:, :, Ts - 1]
                yn_fresh = _fy.detach() if sb_tap_grad != "shared" else _fy
            # H_9888 dual read: pool the trunk across each complete entity mention. Store keys are
            # means over every entity byte, so the query side must use the same canonical unit;
            # taking only the final-byte state makes addressing depend on incidental prefix context.
            yn_a = yn_b = yn_op = None
            if getattr(model.clms, "dual", False):
                if int(mrows.min()) < 0:
                    raise SystemExit("[store-bridge] --clms-dual needs a compose panel carrying "
                                     "mention_a/mention_b (build with `corpus storebind --compose 2`)")
                _pos = torch.arange(Ts, device=pen_s.device).view(1, Ts)
                def _pool_span(start, end):
                    _mask = ((_pos >= start.view(Bs, 1)) & (_pos <= end.view(Bs, 1))).to(pen_s.dtype)
                    return (pen_s * _mask.unsqueeze(1)).sum(dim=2) / _mask.sum(dim=1, keepdim=True)
                yn_a = _pool_span(mrows[:, 0], mrows[:, 1])      # (Bs,d), complete mention A
                yn_b = _pool_span(mrows[:, 2], mrows[:, 3])      # (Bs,d), complete mention B
                _io = mrows[:, 4].view(Bs, 1, 1).expand(Bs, pen_s.shape[1], 1)
                yn_op = pen_s.gather(2, _io).squeeze(-1)        # (Bs,d) causal operator state
            store_logits, att = model.clms(yn_q, K, pols, oracle_slot=osl,
                                           oracle_slot_b=osl_b, need_att=True,
                                           yn_fresh=yn_fresh, yn_a=yn_a, yn_b=yn_b,
                                           yn_op=yn_op, pair_active=pair_active) # dual: (Bs,V),(Bs,2,n_slot)
            ce_ans = F.cross_entropy(store_logits, y_s[:, Ts - 1])
            # non-answer trunk CE (prompt spelling): every row but qpos, standard next-byte LM.
            ce_tok = F.cross_entropy(logits_s[:, :, :Ts - 1].transpose(1, 2).reshape(-1, V),
                                     y_s[:, :Ts - 1].reshape(-1))
            loss = loss + ce_tok + sb_w * ce_ans + out_s["aux_loss"]
            aux["sb_ans_ce"] = float(ce_ans.detach()); aux["sb_tok_ce"] = float(ce_tok.detach())
            # H_9672 addr-loss: direct supervision of the softmax address (att) → cut the (2) bootstrap
            # deadlock W_q could not escape at 303M (Stage1.5 proof). OBJECTIVE (loss term, sb_addr_acc is
            # the monitor). A dual lane supervises BOTH live mention attentions; the old path
            # supervised the unused qpos attention and discarded target_slot_b. sb_addr_w=0
            # (default) keeps the objective byte-identical.
            if sb_addr_w > 0.0:
                if getattr(model.clms, "dual", False):
                    # Every row supervises A. B exists only on genuine composed training rows;
                    # a one-clue row uses the parity identity and must not create a fake B target.
                    ce_parts = [F.cross_entropy(att[:, 0], tgt)]
                    if bool(pair_active.any()):
                        ce_parts.append(F.cross_entropy(att[pair_active, 1], tgt_b[pair_active]))
                    ce_addr = torch.stack(ce_parts).mean()
                else:
                    ce_addr = F.cross_entropy(att, tgt)
                loss = loss + sb_addr_w * ce_addr
                aux["sb_addr_ce"] = float(ce_addr.detach())
            # H_9691 RV-1 oracle-aux dual-path: ALSO train the value/MLP path on the ORACLE (correct one-hot)
            # address every step. The softmax branch (above) trains W_q; this branch replays Stage1.5's proven
            # signal (correct v → MLP learns the XOR function). Runs simultaneously so the race that left val
            # seed-fragile under addr-loss alone (seed-7 won, seed-11 lost to the op-only basin — RV-0: val WAS
            # differentiated, so it is a FUNCTIONAL failure of the fusion) is dissolved. Skipped when already
            # oracle (osl==tgt → identical). 0 → byte-identical.
            if sb_oracle_aux > 0.0 and not sb_oracle:
                store_logits_orc = model.clms(yn_q, K, pols, oracle_slot=tgt,
                                              oracle_slot_b=torch.where(pair_active, tgt_b, torch.zeros_like(tgt_b)),
                                              yn_a=yn_a, yn_b=yn_b, yn_op=yn_op,
                                              pair_active=pair_active)
                ce_orc = F.cross_entropy(store_logits_orc, y_s[:, Ts - 1])
                loss = loss + sb_oracle_aux * ce_orc
                aux["sb_orc_ce"] = float(ce_orc.detach())
            with torch.no_grad():
                if getattr(model.clms, "dual", False):
                    addr_ok = [att[:, 0].argmax(-1) == tgt]
                    if bool(pair_active.any()):
                        addr_ok.append(att[pair_active, 1].argmax(-1) == tgt_b[pair_active])
                    aux["sb_addr_acc"] = float(torch.cat(addr_ok).float().mean())
                else:
                    aux["sb_addr_acc"] = float((att.argmax(-1) == tgt).float().mean())
            with torch.no_grad():                              # monitor-only (a_train_inline_gauge)
                g_id, b_id = 103, 98                           # ord('g'), ord('b') — eval store_run binary
                gold_g = (y_s[:, Ts - 1] == g_id)
                aux["sb_store_acc"] = float(((store_logits[:, g_id] >= store_logits[:, b_id]) == gold_g).float().mean())
                tr = logits_s[:, :, Ts - 1]                    # trunk row at qpos — leak early-warning
                aux["sb_trunk_leak"] = float(((tr[:, g_id] >= tr[:, b_id]) == gold_g).float().mean())
                aux["sb_lam"] = float(model.clms.lam)
        # ── H_9803 BRANCH-LATENT IDEATION FAN — set-CE over SEVERAL REAL observed futures ──
        # A SEPARATE fp32 forward on the document-aligned multi-mode batch (same idiom as the CLMS
        # store lane above). Per document: one forward over the M observed continuations of ONE
        # shared context, K branch latents read from the fork-point EARLY tap, then a min-cost
        # (Hungarian) branch↔target assignment and the mean assigned CE.
        #
        # `l3-disjoint` DETACHES the tap, so the set-CE never pushes the trunk through the branch
        # route — the branch lane must find its modes in what the trunk ALREADY preserved at layer L
        # rather than reshaping the trunk to make the branches separable (which would be the
        # diversity leaking back into a trick).
        if idl is not None and getattr(model, "ifan", None) is not None:
            from ifan import set_ce_loss
            idl_loss_sum = None
            idl_aux_acc = {}
            n_doc = 0
            for (x_i, y_i, m_i, fork_i) in idl:
                logits_i, hm_i, tap_i, aux_i = self.ideation_forward(x_i, int(idl_tap_L) if idl_route == "l3-disjoint" else 0)
                base_logits = logits_i.float().transpose(1, 2)         # (M, T, V)
                yn_i = hm_i.float().transpose(1, 2)                    # (M, T, d)
                tap_row = tap_i.float()[:, :, int(fork_i)]             # (M, d) fork-point tap
                if idl_route == "l3-disjoint":
                    tap_row = tap_row.detach()
                # every branch reads the SAME context grounding: use document row 0's fork tap for
                # all M rows so no branch can identify its target from the grounding it was handed.
                tap_row = tap_row[0:1].expand_as(tap_row)
                l_i, a_i = set_ce_loss(base_logits, model.ifan, tap_row, yn_i, y_i, m_i,
                                       assign=idl_assign, shuffle_gen=idl_gen)
                l_i = l_i + aux_i
                idl_loss_sum = l_i if idl_loss_sum is None else (idl_loss_sum + l_i)
                for k_, v_ in a_i.items():
                    idl_aux_acc[k_] = idl_aux_acc.get(k_, 0.0) + v_
                n_doc += 1
            if n_doc:
                loss = loss + idl_w * (idl_loss_sum / n_doc)
                for k_, v_ in idl_aux_acc.items():
                    aux[k_] = v_ / n_doc                               # MONITOR-ONLY (a_train_inline_gauge)
        aux.update(oaux)
        return loss, out["ce_loss"].detach(), aux



# ══ H_9900 — COMPOSITION LANE (multi-byte answer, CE that never reaches the trunk) ═══════════
# H_9898 measured the constraint this lane exists to escape: at equal drill exposure, replay's
# mere PRESENCE prevents composition from being learned (25% x 8000 steps reads rho·weave 0.000
# while 100% x 2000 reads 0.525), because both compete for the same trunk CE. a_substrate_disjoint
# names the fix — separation preserves, overlap conflicts.
#
# H_9899 established why --store-bridge cannot be reused: its window carries gold[:1], one byte,
# while composed answers run 4-6 bytes. So this lane keeps the store lane's ESSENTIAL property
# (CE off the trunk) and drops its binary readout:
#
#   * a separate linear head reads the trunk penultimate at the answer positions,
#   * CE is computed on THAT head's logits over the WHOLE answer span,
#   * the penultimate is DETACHED, so no gradient from this lane reaches the trunk,
#   * and the head's targets are the answer bytes rho·weave will look for verbatim.
class CompositionLane(torch.nn.Module):
    """Answer-span readout trained off a detached trunk (requirements 1-3 of H_9899)."""

    def __init__(self, d, V):
        super().__init__()
        self.head = torch.nn.Linear(d, V)

    def forward(self, pen_detached):
        # pen_detached: (B, d, T) — already detached by the caller, asserted below.
        return self.head(pen_detached.transpose(1, 2))          # (B, T, V)

    @staticmethod
    def loss(logits, y, ans_mask):
        """CE over the answer span only. ans_mask: (B, T) bool marking the composed answer bytes."""
        if ans_mask.sum() == 0:
            return logits.sum() * 0.0
        sel = ans_mask.reshape(-1)
        lg = logits.reshape(-1, logits.shape[-1])[sel]
        tg = y.reshape(-1)[sel]
        return F.cross_entropy(lg, tg)


def comp_lane_heldout(shell, panel_path, device, max_items=0):
    """H_9904 — score the LANE HEAD directly, without the mouth.

    H_9903 established that the lane head is dropped at serialize, so evaluate's mouth can never
    read it and rho·weave is structurally blind to whatever the lane learns. Opening that path is a
    .clm format change (a separate campaign), and it is only worth launching if the lane learned
    anything at all. This answers that question without the format.

    Teacher-forced: the cue is fed as context and the lane's argmax is read at each answer position
    against the true answer bytes. That is a MIRROR of the engine decode, so it is DIRECTIONAL by
    a_engine_native_learning and can never cement a verdict — it decides whether the format
    campaign is worth opening, nothing more.
    """
    import json as _json
    items = _json.load(open(panel_path))["items"]
    if max_items:
        items = items[:max_items]
    lane = shell.comp_lane
    if lane is None:
        return None
    hit = tot = 0
    with torch.no_grad():
        for it in items:
            cue, tgt = it["cue"], it["target"]
            line = (cue + " " + tgt + " .").encode("ascii", "ignore")
            x = torch.tensor([list(line[:-1])], dtype=torch.long, device=device)
            y = torch.tensor([list(line[1:])], dtype=torch.long, device=device)
            pen = shell.trunk_penultimate(x)
            if pen is None:
                return None
            lg = lane(pen.float().detach())
            m = _comp_answer_mask(y, 32, 46)
            if m.sum() == 0:
                continue
            pred = lg.argmax(-1)
            hit += int(((pred == y) & m).sum().item())
            tot += int(m.sum().item())
    return {"byte_acc": (hit / tot if tot else 0.0), "bytes": tot}


def _comp_answer_mask(y, sep_byte, end_byte):
    """Answer span = bytes after the LAST separator up to the terminator, per row.

    The drill line is '<cue> <answer> .', so the answer is what follows the final space before
    the period. Marking it explicitly is what makes this lane multi-byte where the store lane is
    not — the whole compound is a target, not just its first character."""
    B, T = y.shape
    mask = torch.zeros_like(y, dtype=torch.bool)
    for b in range(B):
        row = y[b]
        ends = (row == end_byte).nonzero()
        if ends.numel() == 0:
            continue
        e = int(ends[-1].item())
        seps = (row[:e] == sep_byte).nonzero()
        if seps.numel() < 2:
            continue
        st = int(seps[-2].item()) + 1                  # after the space preceding the answer
        if st < e:
            mask[b, st:e] = True
    return mask


class StoreBindCell:
    """H_9423 S1 — line-aligned storebind dataset (NOT a ByteCell). c.txt line i <-> c.txt.store.jsonl
    row i (corpus.build_storebind lockstep). Fixed-T single-line prompt-aligned windows that MIRROR
    evaluate.store_run's _seed_to_tok geometry (qpos = T-1): left-pad with spaces, prompt then the first
    answer byte. The answer tail spelling ("ood"/"ad") is not in the window (binary readout needs only
    the first byte at qpos), and in-window copy is structurally impossible (the answer byte does not
    exist before qpos, and each window is exactly one line)."""

    def __init__(self, path, key_emb_np, n_slot, T, val_frac, key_fn="mean"):
        import json as _json
        import numpy as np           # train.py imports numpy only locally (as _np); StoreBindCell needs np
        lines = open(path, encoding="ascii").read().splitlines()
        rows = [_json.loads(l) for l in open(path + ".store.jsonl", encoding="utf-8")]
        if len(lines) != len(rows):
            sys.exit(f"[store-bridge] {path}: {len(lines)} lines != {len(rows)} store rows (lockstep broken)")
        from clms import find_qpos as _fq             # core/clms.py — the SAME scanner eval uses
        import clms as _clms                          # core address function (no inlined copy)
        _key_fn = key_fn                              # H_9852: mean (shipped) | roll (lane_type 6)
        self.ex = []
        for ln, r in zip(lines, rows):
            prompt, gold = r["prompt"], r["gold"]
            if ln != prompt + gold:
                sys.exit(f"[store-bridge] line/manifest mismatch: {ln!r} != {prompt + gold!r}")
            ents, pols = r["store"]["entities"], r["store"]["pols"]
            if not (len(ents) == n_slot == len(pols)):
                sys.exit(f"[store-bridge] n_slot {n_slot} != store {len(ents)}/{len(pols)}")
            if len(prompt) + 1 > T:
                sys.exit(f"[store-bridge] prompt {len(prompt)}B does not fit --store-win {T}")
            seq = b" " * (T - len(prompt)) + prompt.encode("ascii") + gold[:1].encode("ascii")  # len T+1
            x = torch.tensor(list(seq[:T]), dtype=torch.long)
            y = torch.tensor(list(seq[1:T + 1]), dtype=torch.long)
            q = _fq(x.numpy())
            if not (q and q[-1] == T - 1):
                sys.exit("[store-bridge] qpos scanner parity broken (window geometry != eval store_run)")
            # call the CORE address function — an inlined copy here is exactly how the trainer
            # and the inference mirror drift apart (H_9826), and it would silently ignore key_fn
            K = np.stack([_clms._entity_key(key_emb_np, e, _key_fn)
                          for e in ents]).astype(np.float32)          # (n_slot, d_k)
            tgt = int(r["target_slot"])                              # H_9423 Stage1.5: query-entity slot (oracle-train)
            # -1 marks the canonical XOR identity for a missing second clue. Legacy lane 8 used
            # A=B here, making its off-diagonal feature identically zero throughout training.
            tgt_b = int(r.get("target_slot_b", -1))
            # H_9888 mention rows: the window is prompt-aligned (left-padded to T), so a prompt byte
            # p lands on row T - len(prompt) + p. A dual-read lane taps the trunk THERE instead of at
            # the answer position. Rows are -1 when the manifest carries no mentions (every non-compose
            # panel), and the lane refuses to run rather than silently reading row -1.
            _off = T - len(prompt)
            _ma = int(r.get("mention_a", -1)); _mb = int(r.get("mention_b", -1))
            m_a = (_off + _ma) if _ma >= 0 else -1
            m_b = (_off + _mb) if _mb >= 0 else -1
            _ea = r.get("entity")
            _eb = r.get("entity_b", _ea)
            m_a0 = (m_a - len(_ea) + 1) if m_a >= 0 and isinstance(_ea, str) and _ea else -1
            m_b0 = (m_b - len(_eb) + 1) if m_b >= 0 and isinstance(_eb, str) and _eb else -1
            _op_end = prompt.find(" ") - 1
            m_op = (_off + _op_end) if _op_end >= 0 else -1
            if m_a >= 0 and not (0 <= m_a0 <= m_a < T and 0 <= m_b0 <= m_b < T
                                 and 0 <= m_op < T):
                sys.exit(f"[store-bridge] mention row out of window "
                         f"(T={T}, spans={m_a0}:{m_a},{m_b0}:{m_b}, op={m_op})")
            self.ex.append((x, y, torch.from_numpy(K), torch.tensor(pols, dtype=torch.long),
                            torch.tensor(tgt, dtype=torch.long),
                            torch.tensor(tgt_b, dtype=torch.long),
                            torch.tensor([m_a0, m_a, m_b0, m_b, m_op], dtype=torch.long)))
        n_blocks = len(self.ex) // n_slot
        vb = max(1, int(n_blocks * val_frac))
        self.train_n = max(n_slot, (n_blocks - vb) * n_slot)          # [0,train_n) train · rest val


class IdeationFanCell:
    """H_9803 — the MULTI-MODE future-set dataset (NOT a ByteCell).

    File format (`--ideation-corpus`): blank-line-separated DOCUMENTS. Inside a document,
    line 0 is the shared CONTEXT (the topic / fork prefix) and lines 1..M are M DIFFERENT
    continuations that were actually OBSERVED after that context. Example:

        the weather today is
        sunny and warm outside
        pouring rain since dawn
        cold with a hard frost

    That structure is the whole point: the branch lane never invents modes, it is handed
    several REAL futures of one context and has to distribute itself over them. A document
    with fewer than 2 continuations carries no set signal and is DROPPED (loudly counted),
    because training on it would silently degrade the lane to ordinary single-target CE.

    Each example is a fixed-T right-aligned window: the context is left-padded with spaces to
    `ctx_len`, then the continuation fills the rest; `mask` is 1 only on continuation positions,
    so the set-CE never scores the shared prefix (every branch would score it identically and
    the assignment would be decided by prefix noise)."""

    def __init__(self, path, T, ctx_len):
        self.T = int(T)
        self.ctx_len = int(ctx_len)
        self.docs = []           # list of (x:(M,T), y:(M,T), mask:(M,T), fork:int)
        self.n_dropped = 0
        raw = open(path, "rb").read().decode("utf-8", "surrogateescape")
        for block in raw.split("\n\n"):
            lines = [ln for ln in block.split("\n") if ln.strip() != ""]
            if len(lines) < 3:                    # need a context + at least 2 observed futures
                if lines:
                    self.n_dropped += 1
                continue
            ctx = lines[0].encode("utf-8", "surrogateescape")
            conts = [ln.encode("utf-8", "surrogateescape") for ln in lines[1:]]
            C = self.ctx_len
            xs, ys, ms = [], [], []
            for c in conts:
                # window = [pad|ctx][cont|pad] ; targets are the next byte, mask on cont only.
                left = ctx[-C:] if len(ctx) >= C else ctx
                seq = bytearray(b" " * (C - len(left))) + bytearray(left)
                body = c[:self.T - C] if len(c) > self.T - C else c
                seq += bytearray(body)
                mask = [0] * C + [1] * len(body)
                while len(seq) < self.T + 1:      # +1 so the shifted target exists at T-1
                    seq.append(32); mask.append(0)
                x = torch.tensor(list(seq[:self.T]), dtype=torch.long)
                y = torch.tensor(list(seq[1:self.T + 1]), dtype=torch.long)
                xs.append(x); ys.append(y)
                ms.append(torch.tensor(mask[:self.T], dtype=torch.long))
            self.docs.append((torch.stack(xs), torch.stack(ys), torch.stack(ms), C - 1))
        if not self.docs:
            raise SystemExit(f"--ideation-corpus {path}: 0 usable documents "
                             f"(need blank-line-separated blocks of >=3 lines: context + >=2 futures)")


# ══ H_9840 — SLEEP-SCHEDULE curriculum (SLP lane) ═══════════════════════════════════════════
#
# WHY THIS EXISTS: core/dream_lib.py already carries a 90-tick 5-stage session
# (WAKE 60 · N1 10 · N2 10 · N3 7 · REM 3) plus the two-process homeostat (Process-S adenosine
# build/clear, Process-C circadian). That table IS the shape of a curriculum scheduler, and until
# now the trainer never read it — its only consumer was the daemon (cli/chat.py). This lane makes
# the training step's wake/sleep phase come from the substrate's own session table instead of a
# hard-coded constant (a_autonomy_over_hardcode), so the alternation is a substrate fact rather
# than a trainer knob.
#
# SCOPE / HONESTY (card H_9840): a SLEEP step here REHEARSES windows already consumed while awake
# (the trainer-side reading of core/imagination_replay.py's working-ring rehearsal). There is no
# consolidation OBJECTIVE yet — that is H_9833 (sleep-consolidate). Replay without one is only
# resampling seen material, so this lane is SUBORDINATE to H_9833 and must not be read as a
# consolidation result on its own.
_SLP_STAGE_INITIAL = ("W", "1", "2", "3", "R")


class SleepSchedule:
    """Per-step WAKE/SLEEP phase source over core/dream_lib.py's stage table (H_9840).

    ARMS
      dream-lib         — phase = dr_stage_at(tick) in dream_lib's OWN order: one long WAKE bout,
                          then a CONSOLIDATED sleep bout N1→N2→N3→REM.
      fixed-alternating — THE CONTROL. The SAME per-cycle stage MULTISET (identical wake/sleep
                          ratio AND identical per-stage counts) emitted in an even round-robin
                          spread instead of one bout. The ONE variable is therefore the temporal
                          ARRANGEMENT (consolidated bout + stage order), not the ratio and not the
                          stage mixture. If dream-lib cannot beat this arm, the homeostat is
                          decoration and the ratio was the only lever — say that plainly.
      (`off` never constructs this object at all ⇒ the trainer is byte-identical.)

    --sleep-ticks rescales the tick axis onto dream_lib's native 90-tick session; n=90 is the
    identity, i.e. exactly dream_lib. The arms stay multiset-matched at EVERY n by construction
    (the control is a PERMUTATION of the treatment cycle) — the selftest re-checks that across a
    tick sweep so no choice of n can pick the verdict (no tune-to-green).
    """

    ARMS = ("dream-lib", "fixed-alternating")

    def __init__(self, arm, ticks):
        if arm not in self.ARMS:
            raise SystemExit(f"[sleep-schedule] unknown arm {arm!r} (have: {', '.join(self.ARMS)})")
        n = int(ticks)
        if n < DR.dr_n_stages():
            raise SystemExit(f"[sleep-schedule] --sleep-ticks {n} < {DR.dr_n_stages()}: a cycle "
                             f"shorter than the stage count cannot realize the stage multiset.")
        self.arm, self.n = arm, n
        native = [DR.dr_stage_at((t * DR.dr_n_ticks()) // n) for t in range(n)]
        self.cycle = native if arm == "dream-lib" else _slp_spread(native)
        # Process-S/C telemetry, reported (never gated on): the homeostat's own reading of the
        # same tick axis. dream_lib returns numbers only — no bool gate lives here either (p5).
        self.pressure = [DR.sp_pressure_at((t * DR.dr_n_ticks()) // n, 0.0) for t in range(n)]
        self.propensity = [DR.sp_sleep_propensity(p, DR.sp_circadian_bias((t * DR.dr_n_ticks()) // n))
                           for t, p in enumerate(self.pressure)]

    def stage_at(self, step):
        """1-based training step → dream_lib stage id (0=WAKE, 1..4 = N1/N2/N3/REM)."""
        return self.cycle[(step - 1) % self.n]

    def is_deep(self, stage):
        """N3/REM — dream_lib's own imagination-active stages replay the WHOLE buffer;
        the light stages (N1/N2) rehearse only its recent tail."""
        return DR.dr_imagination_active(stage) == 1

    def render(self, steps):
        return "".join(_SLP_STAGE_INITIAL[self.stage_at(s)] for s in range(1, steps + 1))


def _slp_spread(cycle):
    """Even round-robin PERMUTATION of a stage cycle — the ratio-and-multiset-matched control.

    Each stage's c occurrences get keys (j+0.5)/c and the whole cycle is re-sorted by that key,
    so every stage is spread evenly over the session while the per-stage COUNTS are untouched by
    construction. That construction is what makes `fixed-alternating` a control and not a second
    treatment: it cannot differ from `dream-lib` in ratio or mixture, only in arrangement.
    """
    counts = {}
    for s in cycle:
        counts[s] = counts.get(s, 0) + 1
    seen, keyed = {}, []
    for s in cycle:
        j = seen.get(s, 0)
        seen[s] = j + 1
        keyed.append(((j + 0.5) / counts[s], s, j))
    keyed.sort()
    return [s for _, s, _ in keyed]


def slp_meter(stages):
    """THE INSTRUMENT: read a realized stage sequence into ratio + bout structure.

    Certified by the two controls in `run_sleep_selftest` before any arm row is reported.
    """
    n = len(stages)
    sleep_bouts, wake_bouts = [], []
    run_s = run_w = 0
    for s in stages:
        if s != 0:
            run_s += 1
            if run_w:
                wake_bouts.append(run_w); run_w = 0
        else:
            run_w += 1
            if run_s:
                sleep_bouts.append(run_s); run_s = 0
    if run_s: sleep_bouts.append(run_s)
    if run_w: wake_bouts.append(run_w)
    n_sleep = sum(1 for s in stages if s != 0)
    counts = {}
    for s in stages:
        counts[DR.dr_stage_name(s)] = counts.get(DR.dr_stage_name(s), 0) + 1
    return {
        "n": n, "wake": n - n_sleep, "sleep": n_sleep,
        "sleep_ratio": (n_sleep / n) if n else 0.0,
        "n_sleep_bouts": len(sleep_bouts),
        "max_sleep_bout": max(sleep_bouts) if sleep_bouts else 0,
        "max_wake_bout": max(wake_bouts) if wake_bouts else 0,
        "stage_counts": counts,
    }


def run_sleep_selftest(ticks, steps):
    """H_9840 $0 SCHEDULE SELFTEST — controls first, arm rows only if they certify.

    Same frozen order as cli/corpus.py::run_mi_screen:
      ① METER CONTROLS.  `plant_bout` = a hand-planted sequence whose geometry is known exactly
         (60 WAKE then 30 N3): the meter must RECOVER it. `null_all_wake` = the zero-truth
         pedestal, a stream with no sleep in it at all: the meter must REFUSE (report no sleep
         structure). A meter that cannot see a planted bout, or that manufactures one on an
         all-wake stream, makes every arm row unreadable.
      ② ARM GATES.  `separation` — the two arms must actually differ (an inert lever is
         INSTRUMENT-DEAD). `multiset_match` — they must carry IDENTICAL per-stage counts, else
         `fixed-alternating` is not ratio-matched and the contrast is confounded (INVALID).
      ③ TICK ROBUSTNESS.  Both gates re-checked across a --sleep-ticks sweep: if either could be
         made to pass or fail by choosing n, the knob would be choosing the verdict.
    """
    plant = [0] * 60 + [3] * 30                     # known truth: ratio 30/90, ONE bout of 30
    m_plant = slp_meter(plant)
    plant_truth = {"sleep_ratio": 30 / 90, "n_sleep_bouts": 1,
                   "max_sleep_bout": 30, "max_wake_bout": 60}
    plant_fires = all(abs(m_plant[k] - v) < 1e-12 for k, v in plant_truth.items())

    m_null = slp_meter([0] * 90)                    # zero-truth pedestal: no sleep exists
    null_refuses = (m_null["sleep"] == 0 and m_null["n_sleep_bouts"] == 0
                    and m_null["max_sleep_bout"] == 0 and m_null["sleep_ratio"] == 0.0)

    sweep, sep_ok, mset_ok = [], True, True
    for n in sorted({30, 45, 90, 180, int(ticks)}):
        try:
            a_dl = SleepSchedule("dream-lib", n)
            a_fa = SleepSchedule("fixed-alternating", n)
        except SystemExit as e:
            sweep.append({"ticks": n, "error": str(e)}); sep_ok = False; continue
        m_dl, m_fa = slp_meter(a_dl.cycle), slp_meter(a_fa.cycle)
        ham = sum(1 for x, y in zip(a_dl.cycle, a_fa.cycle) if x != y)
        same_mset = (m_dl["stage_counts"] == m_fa["stage_counts"])
        sep_ok = sep_ok and ham > 0
        mset_ok = mset_ok and same_mset
        sweep.append({"ticks": n, "hamming": ham, "multiset_match": same_mset,
                      "dream-lib": m_dl, "fixed-alternating": m_fa})

    certified = plant_fires and null_refuses and sep_ok and mset_ok
    if not plant_fires:
        status, why = "INSTRUMENT-DEAD", ("plant_bout did NOT fire — the meter cannot recover a "
                                          "bout geometry that is known to be there, so no arm row "
                                          "it reports can be read.")
    elif not null_refuses:
        status, why = "INVALID", ("null_all_wake did NOT refuse — the meter reports sleep structure "
                                  "on a stream containing no sleep, i.e. it MANUFACTURES it.")
    elif not sep_ok:
        status, why = "INSTRUMENT-DEAD", ("the two arms are identical at some --sleep-ticks: the "
                                          "lever does nothing there and a contrast is impossible.")
    elif not mset_ok:
        status, why = "INVALID", ("the arms' stage multisets differ at some --sleep-ticks: "
                                  "`fixed-alternating` is then not ratio-matched and any "
                                  "dream-lib−control delta is confounded by the ratio.")
    else:
        status, why = "CERTIFIED", ("meter fires on the plant and refuses on the all-wake pedestal; "
                                    "the arms differ in ARRANGEMENT at every swept tick count while "
                                    "carrying an identical stage multiset.")

    arms, realized_ratios = {}, {}
    if certified:
        for arm in SleepSchedule.ARMS:
            sch = SleepSchedule(arm, ticks)
            realized = [sch.stage_at(s) for s in range(1, steps + 1)]
            rm = slp_meter(realized)
            realized_ratios[arm] = rm["sleep_ratio"]
            arms[arm] = {"realized_meter": rm,
                         "cycle_meter": slp_meter(sch.cycle),
                         "sequence": sch.render(steps),
                         "pressure_first8": [round(p, 6) for p in sch.pressure[:8]],
                         "propensity_first8": [round(p, 6) for p in sch.propensity[:8]]}

    out = {
        "instrument": "sleep-schedule-selftest",
        "hypothesis": "H_9840",
        "engine": "core/dream_lib.py (5-stage session + Process-S/C homeostat)",
        "status": status, "why": why,
        "controls": {"plant_bout": {"must": "FIRE", "fired": plant_fires,
                                    "truth": plant_truth, "measured": m_plant},
                     "null_all_wake": {"must": "REFUSE", "refused": null_refuses,
                                       "measured": m_null}},
        "arm_gates": {"separation_all_ticks": sep_ok, "multiset_match_all_ticks": mset_ok,
                      "tick_sweep": sweep},
        # SELF-CAUGHT DEFECT (kept as a reported gate, and hard-enforced in the trainer):
        # `steps` is a knob that can flip the contrast. dream-lib front-loads its WAKE bout, so a
        # run of steps=12 at ticks=90 realizes sleep_ratio 0.0000 for dream-lib and 0.2500 for
        # fixed-alternating — the "ratio-matched" control would then not be ratio-matched at all,
        # and any delta would be a ratio delta wearing an arrangement label. The cycle ratios are
        # equal by construction; only a WHOLE number of sessions makes the REALIZED ones equal too.
        # The trainer therefore refuses `--steps` that is not a multiple of `--sleep-ticks`.
        "steps_alignment": {"steps": int(steps), "sleep_ticks": int(ticks),
                            "whole_sessions": (int(steps) % int(ticks) == 0),
                            "realized_sleep_ratio": realized_ratios,
                            "realized_ratio_matched": (len(set(realized_ratios.values())) <= 1)},
        "geometry": {"sleep_ticks": int(ticks), "steps": int(steps),
                     "native_ticks": DR.dr_n_ticks()},
        "arms": arms,
        "reaudit": {"argv": ["anima-py", "train"] + sys.argv[1:]},
        "reading": ("`off` is not an arm here: it never constructs a schedule, so it has no "
                    "sequence to print — its claim is byte-identity, which is checked by "
                    "comparing a real `--sleep-schedule off` run's .clm sha256 against a run "
                    "with no flag at all. SUBORDINATE TO H_9833: a SLEEP step rehearses already-"
                    "seen windows, and without a consolidation objective that is resampling, not "
                    "consolidation — this selftest certifies the SCHEDULE, never a learning gain."),
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if certified else 3


def _to_device_or_die(model, device):
    """model.to(device) but turn a CUDA OOM at model-move into a CLEAR, actionable message
    instead of a raw torch AcceleratorError traceback (which reads like a code/arch bug — it
    cost a session's debugging: the crash was another job holding the GPU, NOT the model).
    We do NOT silently fall back to CPU (train-py-6: a silent device=cpu fallback burned a day
    training at 0% GPU) — 303M CPU training is impractical, so we tell the operator what to do."""
    try:
        return model.to(device)
    except Exception as e:                                    # re-raised below unless it is a CUDA OOM
        msg = str(e).lower()
        if str(device).startswith("cuda") and ("out of memory" in msg or "cuda error" in msg
                                               or "cudaerrormemoryallocation" in msg):
            try:
                import torch as _t
                free_b, tot_b = _t.cuda.mem_get_info(_t.device(device))
                meminfo = " (GPU free %.2f/%.2f GiB)" % (free_b / 2**30, tot_b / 2**30)
            except Exception:
                meminfo = ""
            sys.exit("[train] CUDA out-of-memory moving the model to %s%s — the GPU is HELD by "
                     "another job (this is NOT a torch-build/arch problem; check `nvidia-smi`). "
                     "Fix: wait for / pick a FREE pool host, or force CPU with "
                     "CUDA_VISIBLE_DEVICES='' (slow — toy scale only)." % (device, meminfo))
        raise


# ══ H_9845 — INTERVENTIONAL CLOSURE MONITOR (rung 1) · ⛔ MONITOR-ONLY ═══════════════════
# WHY THIS EXISTS. "Is this lane actually CAUSAL, or only correlated with the loss?" is today
# answered by an ABLATION RETRAIN — a second full run per lane, and the reason most lanes are
# never causally checked at all. core/closure_ladder.py (H_9807) already ships the one rig in
# this repo that can ANCHOR rather than correlate: the executed action is a seeded coin over
# {true action, marginal-matched shuffle}, so P(I_{t+1} | do(A_t)) is IDENTIFIED. Driving that
# rig with the LIVE model as the acting policy turns it into a WITHIN-RUN causal probe — it
# asks whether the model's contingency structure (how its own input maps to its action), and
# not its action marginal, leaves a fingerprint on its own next input.
#
# ⛔ a_train_inline_gauge — THIS NEVER ENTERS THE LOSS, and that is structural, not a promise:
#    · it runs inside `torch.no_grad()`, after `opt.step()`, on a saved/restored RNG state;
#    · it returns a plain dict, and the ONLY thing the call site does with that dict is print
#      it (and optionally append it to a JSONL);
#    · nothing it computes is a torch graph leaf, so no term of it can reach `loss.backward()`.
#    The landing evidence is a BYTE-IDENTICAL ON-vs-OFF training trajectory at a fixed seed
#    (same per-step CE lines, same .clm/.pt sha256) — see the H_9845 card. Put any of this in
#    the loss and it becomes tune-to-green by construction.
#
# ⚠️ RUNG 1 IS NOT ALIVENESS. A thermostat clears it; the scripted P-LIVE plant used here as the
#    POSITIVE CONTROL clears it BY DESIGN. A reading diagnoses lane causality. No consciousness,
#    aliveness or interiority claim follows from any number this monitor prints.
#
# ⚠️ REPRODUCTION. `--closure-monitor-seed` is NOT a sampler seed: it keys the world's exogenous
#    schedule (regime moves, arrivals, the A/B coin) via closure_ladder's (seed, t, tag) streams.
#    Re-running one schedule with a deterministic policy is byte-identical and therefore proves
#    nothing (sample-seed-invalid-for-deterministic-do-intervention); real replication = several
#    PERTURBATION SCHEDULES, which is why the monitor runs `--closure-monitor-schedules` of them
#    and reports agreement rather than one number.
CLOSURE_SEP = " => "          # digest -> action prompt separator (scored span = the action)


def _closure_model_brain(model, device, seq_cap):
    """Bind the LIVE model as a `digest -> action` brain for core/closure_ladder.py.

    The rig's brains are callables `str -> action` (CL.digest_brain / CL.constant_brain). The
    model is a byte LM, so the action is read out by SCORING, never by sampling: each of the 8
    actions is appended to the digest and teacher-forced, and the action with the lowest mean
    NLL over ITS OWN BYTES wins (ties break on ACTIONS order, so the readout is deterministic —
    CL.lv_p's `replay_agree` re-checks that and the monitor refuses a brain that fails it).

    Sampling would inject RNG into a monitor that must not perturb the run; scoring keeps the
    whole probe deterministic given (weights, digest). One forward of batch 8 per decision.

    train-py-9: the scored SPAN is closed on BOTH sides and its size is REPORTED (`act.diag`),
    because a weighted-position count that nobody checked is how H_9811 sent 99% of its loss
    mass at the wrong bytes and read the miss as a substrate negative."""
    import closure_ladder as CL                       # core/ is on sys.path (see header)
    actions = list(CL.ACTIONS)
    diag = {"scored_positions": None, "expected_positions": [len(a.encode()) for a in actions],
            "span_ok": None, "truncated": False}

    def act(digest):
        xs, ys, ms = [], [], []
        head = (digest + CLOSURE_SEP).encode("utf-8")
        seqs = [head + a.encode("utf-8") for a in actions]
        maxlen = max(len(s) for s in seqs)
        for s in seqs:
            buf = torch.frombuffer(bytearray(s + b" " * (maxlen - len(s))),
                                   dtype=torch.uint8).long()
            x, y = buf[:-1], buf[1:]
            m = torch.zeros(y.shape[0])
            # position j of `y` holds the byte at index j+1, so the action span [len(head), len(s))
            # is scored at j in [len(head)-1, len(s)-1) — right edge CLOSED at the action's end,
            # never left to run to the end of the window (train-py-9).
            m[len(head) - 1:len(s) - 1] = 1.0
            if seq_cap and x.shape[0] > seq_cap:      # keep the TAIL — the scored span lives there
                x, y, m = x[-seq_cap:], y[-seq_cap:], m[-seq_cap:]
                diag["truncated"] = True
            xs.append(x); ys.append(y); ms.append(m)
        x = torch.stack(xs).to(device)
        y = torch.stack(ys).to(device)
        m = torch.stack(ms).to(device)
        if diag["scored_positions"] is None:
            got = [int(v) for v in m.sum(dim=1).tolist()]
            diag["scored_positions"] = got
            diag["span_ok"] = bool(got == diag["expected_positions"])
        logits = model(x)["logits"].float()           # (B, V, T)
        nll = -torch.log_softmax(logits, dim=1).gather(1, y.unsqueeze(1)).squeeze(1)
        score = (nll * m).sum(dim=1) / m.sum(dim=1).clamp(min=1.0)
        return actions[int(torch.argmin(score).item())]

    act.diag = diag
    return act


def _closure_clm_brain(ckpt, seq_cap):
    """H_9845-B — the SAME `digest -> action` brain, but the acting policy is a REAL serialized
    `.clm` (e.g. the 303M) read through the py-canonical measurement path
    (core/decode.clm_load_weights + clm_forward_hidden_logits), instead of the live torch model.

    ⚠️ WHY THIS FLAG EXISTS — the H_9838 PLANTED-GEOMETRY FAILURE, one lane over. H_9838 landed a
    headline positive (CA3 multi-step completion at 12x derived chance, lesion-collapsing, 3 seeds
    x 3 geometries, independently reproduced) on a rig whose item codes were a PLANTED integer
    fixture. Swapping ONLY that input source for the production trunk's real penultimate
    representations turned the 16-item load from CERTIFIED into INVALID: the value-shuffled
    ZERO-TRUTH PEDESTAL read 0.3750 against a 0.3077 bar, i.e. a structure-free store answered,
    so the result had come from the fixture's hand-made near-orthogonal geometry (within .0469 /
    across .0117) and not from the mechanism (real reps overlap 2.2x: .0625 / .0260 — exactly what
    core/hippo_lane.py's own header warns about). H_9845 landed under the same defect class: every
    number in its card was produced with a d32 · L2 · 12-step TOY as the acting brain, and the
    rig's own header says a thermostat clears rung 1, so a toy result is unreadable as evidence
    about anything. This flag is the identical swap: same arms, same 6 controls, same frozen bars
    (CLOSURE_SIGN / NULL_CLOSURE_MAX / MIN_BLOCKS), same tick budget, same >=2 perturbation
    schedules, same tie order — ONLY the acting policy's input source changes.

    Readout is byte-for-byte the same CONTRACT as `_closure_model_brain`: each of the 8 actions is
    appended to `digest + CLOSURE_SEP`, teacher-forced, and the action with the lowest mean NLL
    over ITS OWN BYTES wins, ties broken on ACTIONS order. The only difference is the engine that
    produces the logits (numpy `.clm` forward vs torch nn.Module), which is the point of the swap.

    Memoization: `act` is a pure deterministic function of (frozen weights, digest), so identical
    digests are cached. This changes NO number — it only avoids recomputing a forward whose result
    is already known. It is NOT a bar, a threshold or an arm; the world still calls the brain once
    per tick and the recorded tape is unchanged.

    Cost note (measured on this host, CPU numpy, py303_full.clm): ~0.26 s per forward at T~90, and
    one decision = 8 forwards, so a 600-tick schedule is ~21 min of real compute. That is why the
    tick budget is NOT lowered to make it cheap — at 400 ticks the scripted positive control stops
    firing (closure_ladder MIN_BLOCKS), and lowering the budget would destroy the comparison this
    swap exists to make."""
    import numpy as _np
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                    "core"))
    import closure_ladder as CL
    import decode as D                                   # core/decode.py — the numpy .clm path
    actions = list(CL.ACTIONS)
    W = D.clm_load_weights(ckpt)
    diag = {"scored_positions": None, "expected_positions": [len(a.encode()) for a in actions],
            "span_ok": None, "truncated": False}
    cache = {}

    def act(digest):
        hit = cache.get(digest)
        if hit is not None:
            return hit
        head = (digest + CLOSURE_SEP).encode("utf-8")
        scores, spans = [], []
        for a in actions:
            s = head + a.encode("utf-8")
            lo, hi = len(head) - 1, len(s) - 1        # same closed span as _closure_model_brain
            if seq_cap and len(s) > seq_cap:          # keep the TAIL — the scored span lives there
                cut = len(s) - seq_cap
                s, lo, hi = s[cut:], lo - cut, hi - cut
                diag["truncated"] = True
            tok = _np.frombuffer(s, dtype=_np.uint8).astype(_np.float64)
            lg = D.clm_forward_hidden_logits(W, tok, len(s))[1]        # [T, V] host numpy
            lg = lg - lg.max(axis=1, keepdims=True)
            logp = lg - _np.log(_np.exp(lg).sum(axis=1, keepdims=True))
            nll = [-float(logp[j, s[j + 1]]) for j in range(lo, hi)]
            scores.append(sum(nll) / max(1, len(nll)))
            spans.append(len(nll))
        if diag["scored_positions"] is None:
            diag["scored_positions"] = spans
            diag["span_ok"] = bool(spans == diag["expected_positions"])
        best = min(range(len(actions)), key=lambda i: (scores[i], i))  # ties -> ACTIONS order
        cache[digest] = actions[best]
        return actions[best]

    act.diag = diag
    return act


# The yoked OPEN floor is averaged over these derangement draws. MEASURED (2026-07-21, the
# scripted digest-reading brain at 600 ticks): ONE draw is not a floor — at seed 7 draw k=9 read
# 0.7500 while k=3 read 0.5000, i.e. the derangement INDEX alone flipped the sign of the
# treatment-minus-control delta. Reading a single draw would have let a knob pick the verdict
# (tune-to-green with extra steps), so the floor is the MEAN over 5 draws and the per-draw
# [min,max] spread is reported; `derangement_robust` marks the stronger read (treatment above
# the WORST draw). The mean, not the max, is the gate — Δ = exp − max(controls) carries an
# order-statistic bias that mechanises KILL (probe-defect-census-max-control-bias).
CLOSURE_OPEN_DERANGEMENTS = (3, 5, 9, 11, 13)


def _closure_arm(brain, seed, ticks):
    """Drive a `digest -> action` brain through the closed loop and build its OWN
    marginal-matched yoked floor: the brain's executed actions, order destroyed by the rig's
    Watson derangement, replayed as a tape at the SAME exogenous schedule. Only the closed leg
    calls the brain; every floor draw is a tape replay (no model forwards)."""
    import closure_ladder as CL
    tape = []

    def recording_policy(s, t, past):
        a = brain(CL.observe(s))
        tape.append(a)
        return a

    live = CL.lv_c(recording_policy, seed, ticks, null=False)
    opens = [CL.lv_c(CL.make_tape_policy(CL._derange(tape, seed, k)), seed, ticks)["closure_sign"]
             for k in CLOSURE_OPEN_DERANGEMENTS]
    omean = sum(opens) / len(opens)
    # H_9845-B TELEMETRY (read-only, moves NO bar): `action_support` alone cannot tell a degenerate
    # policy apart from the C6 input-blind pedestal, and it cannot say WHICH action a degenerate
    # readout locked onto — which is the difference between "this policy does not read its input"
    # and "the byte-LM NLL readout has a length/prior bias". The real-303M swap needed exactly that
    # distinction, so the executed-action histogram is now reported. It is telemetry: no gate, no
    # threshold and no arm reads it, and the OLD path's numbers are byte-identical with it present.
    hist = {}
    for a in tape:
        hist[a] = hist.get(a, 0) + 1
    return {"closure": live["closure_sign"], "blocks": live["blocks"],
            "open_floor_mean": omean, "open_floor_min": min(opens), "open_floor_max": max(opens),
            "open_draws": opens, "delta_vs_open": live["closure_sign"] - omean,
            "action_support": len(set(tape)),
            "action_hist": dict(sorted(hist.items(), key=lambda kv: (-kv[1], kv[0]))),
            "anchors": bool(live["closure_sign"] >= CL.CLOSURE_SIGN
                            and live["closure_sign"] > omean),
            "derangement_robust": bool(live["closure_sign"] > max(opens))}


def _closure_schedule(brain, seed, ticks):
    """One PERTURBATION SCHEDULE of the rung-1 battery. Control order is FROZEN: every control
    leg runs FIRST and the model row is REFUSED unless all of them certify.

      C1 LV-E echo guard      — no action name is reachable in the observation vocabulary, so
                                every action->input path is DYNAMICS, never a byte echo.
      C2 frame alignment      — the H_013 standing regression test (a mis-framed Closed stream
                                scored 0.667 closure in a provably DEAD world, above its gate).
      C3 POSITIVE CONTROL     — the scripted contingent plant must FIRE at THIS tick budget
                                (closure >= CLOSURE_SIGN) and the digest-reading brain must
                                show a contingency rate (CR >= 0.20, replay_agree == 1.0). If
                                it cannot see a signal that is planted, a null model row is a
                                property of the instrument (positive-control-before-negative).
      C4 ZERO-TRUTH PEDESTAL  — the INERT world must read closure <= NULL_CLOSURE_MAX and the
                                input-BLIND brain must read CR exactly 0. If either fires, the
                                instrument MANUFACTURES signal (phi-estimator-needs-zero-truth).
      C5 PATHWAY POSITIVE     — the scripted DIGEST-READING brain pushed through the EXACT code
                                path the model uses (observe -> brain -> recording policy ->
                                lv_c + yoked floor) must ANCHOR. C3 certifies the closure
                                ESTIMATOR; only C5 certifies that a contingent brain can be
                                read AS A BRAIN through this pathway, so a model NO-ANCHOR is
                                about the model and not about the pipe.
      C6 PATHWAY PEDESTAL     — the input-BLIND brain through that same pathway must read
                                closure <= NULL_CLOSURE_MAX (zero-truth on the pathway).

    ⚠️ C5 is an EASIER task than the model's (train-py-10): it certifies the PATHWAY, never that
    the model's regime is learnable at this budget. Passing C5 buys readability, not power.

    Only then the model row: the live model acting in order vs its own marginal-matched yoked
    floor. The read is that collapse-delta, never the raw closure value."""
    import closure_ladder as CL

    echo = CL.echo_guard()
    frame = CL._frame_alignment_check(seed, ticks)
    digests = CL.sample_digests(seed, ticks)
    pos_c = CL.lv_c(CL.policy_live, seed, ticks, null=False)          # scripted plant, coupled env
    pos_p = CL.lv_p(CL.digest_brain, digests)                         # reading brain
    ped_c = CL.lv_c(CL.policy_live, seed, ticks, null=True)           # INERT env
    ped_p = CL.lv_p(CL.constant_brain, digests)                       # input-blind brain

    blocks = min(pos_c["blocks"], ped_c["blocks"])
    plant_fires = bool(pos_c["closure_sign"] >= CL.CLOSURE_SIGN
                       and pos_p["CR"] >= 0.20 and pos_p["replay_agree"] == 1.0)
    pedestal_refuses = bool(ped_c["closure_sign"] <= CL.NULL_CLOSURE_MAX and ped_p["CR"] == 0.0)
    structural_ok = bool(echo["ok"] and frame["ok"])
    under_powered = bool(blocks < CL.MIN_BLOCKS)

    row = {"seed": seed, "ticks": ticks, "blocks": blocks,
           "controls": {"echo_ok": echo["ok"], "frame_ok": frame["ok"],
                        "plant_closure": pos_c["closure_sign"], "plant_CR": pos_p["CR"],
                        "plant_replay_agree": pos_p["replay_agree"],
                        "pedestal_closure": ped_c["closure_sign"], "pedestal_CR": ped_p["CR"],
                        "plant_fires": plant_fires, "pedestal_refuses": pedestal_refuses},
           "under_powered": under_powered, "model": None}

    if not structural_ok:
        row["status"] = "INSTRUMENT-INVALID"
        row["why"] = ("a structural pre-check failed (echo_ok=%s frame_ok=%s) — no closure "
                      "number is readable until it is fixed." % (echo["ok"], frame["ok"]))
        return row
    if not plant_fires:
        # power BEFORE a negative verdict: below the measured block floor a plant miss is a
        # sample-size artefact, and calling it INSTRUMENT-DEAD would record a power problem
        # as a substrate fact (the rig's own MIN_BLOCKS doctrine).
        row["status"] = "UNDER-POWERED" if under_powered else "INSTRUMENT-DEAD"
        row["why"] = ("the scripted contingent plant did NOT fire at %d ticks (%d blocks; "
                      "closure %.3f vs gate %.2f) — %s"
                      % (ticks, blocks, pos_c["closure_sign"], CL.CLOSURE_SIGN,
                         "raise --closure-monitor-ticks to >= %d before reading anything."
                         % (CL.MIN_BLOCKS * CL.BLOCK) if under_powered else
                         "the estimator cannot see a planted signal, so a model null would be "
                         "a fact about the instrument."))
        return row
    if not pedestal_refuses:
        row["status"] = "INVALID"
        row["why"] = ("the zero-truth pedestal did NOT refuse (inert-world closure %.3f, "
                      "blind-brain CR %.3f) — the instrument manufactures signal."
                      % (ped_c["closure_sign"], ped_p["CR"]))
        return row

    path_pos = _closure_arm(CL.digest_brain, seed, ticks)             # C5
    path_ped = _closure_arm(CL.constant_brain, seed, ticks)           # C6
    row["controls"]["pathway_positive"] = path_pos
    row["controls"]["pathway_pedestal"] = path_ped
    if not path_pos["anchors"]:
        row["status"] = "PATHWAY-DEAD"
        row["why"] = ("the scripted digest-READING brain did not anchor through the model's own "
                      "pathway at this schedule (closure %.3f vs gate %.2f, yoked floor %.3f) — "
                      "the pathway cannot discriminate here, so a model row would be unreadable."
                      % (path_pos["closure"], CL.CLOSURE_SIGN, path_pos["open_floor_mean"]))
        return row
    if path_ped["closure"] > CL.NULL_CLOSURE_MAX:
        row["status"] = "INVALID"
        row["why"] = ("the input-BLIND brain read closure %.3f > %.2f through the model's "
                      "pathway — the pathway manufactures closure."
                      % (path_ped["closure"], CL.NULL_CLOSURE_MAX))
        return row

    arm = _closure_arm(brain, seed, ticks)
    mp = CL.lv_p(brain, digests)
    arm["CR"] = mp["CR"]
    arm["replay_agree"] = mp["replay_agree"]
    arm["anchors"] = bool(arm["anchors"] and mp["replay_agree"] == 1.0)
    row["model"] = arm
    row["status"] = "UNDER-POWERED" if under_powered else "CERTIFIED"
    row["why"] = ("controls certified at this tick budget: plant fires, pedestal refuses."
                  if not under_powered else
                  "controls certified but only %d blocks < %d — DIRECTIONAL at best."
                  % (blocks, CL.MIN_BLOCKS))
    return row


def closure_monitor_rung1(model, device, seq_cap, *, seed, ticks, schedules, step, brain_ckpt=""):
    """H_9845 — run the rung-1 closure battery against the LIVE model. MONITOR-ONLY.

    `brain_ckpt` (H_9845-B, default "" ⇒ byte-identical to the landed path): when set, the ACTING
    POLICY is that serialized `.clm` read through core/decode instead of the in-training model.
    Nothing else moves — same controls, same bars, same ticks, same schedules (see
    `_closure_clm_brain` for why this swap is the whole point).

    Returns a dict; the caller may only LOG it. The model is put in eval mode and the torch RNG
    state is snapshotted and restored, so the probe cannot perturb the trajectory it observes.
    Several PERTURBATION SCHEDULES are run (a deterministic do()-intervention makes single-seed
    re-running byte-identical and therefore vacuous as replication), and the headline read is
    the AGREEMENT across them, not any single schedule's number."""
    import closure_ladder as CL
    was_training = model.training
    cpu_rng = torch.get_rng_state()
    cuda_rng = torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None
    try:
        model.eval()
        with torch.no_grad():
            brain = (_closure_clm_brain(brain_ckpt, seq_cap) if brain_ckpt
                     else _closure_model_brain(model, device, seq_cap))
            rows = [_closure_schedule(brain, seed + k, ticks) for k in range(max(1, schedules))]
            readout_diag = dict(brain.diag)
    finally:
        torch.set_rng_state(cpu_rng)
        if cuda_rng is not None:
            torch.cuda.set_rng_state_all(cuda_rng)
        if was_training:
            model.train()
    certified = [r for r in rows if r["status"] in ("CERTIFIED", "UNDER-POWERED") and r["model"]]
    if not readout_diag.get("span_ok") or len(certified) != len(rows):
        read = "REFUSED"
    elif all(r["model"]["anchors"] for r in rows):
        read = "ANCHOR-ALL-SCHEDULES"
    elif any(r["model"]["anchors"] for r in rows):
        read = "SCHEDULE-SPLIT"
    else:
        read = "NO-ANCHOR"
    return {"instrument": "closure-monitor", "hypothesis": "H_9845", "rung": 1,
            "engine": "core/closure_ladder.py (H_9807)", "step": step,
            "brain_source": ("real-clm:%s" % brain_ckpt) if brain_ckpt else "live-training-model",
            "geometry": {"ticks": ticks, "seed0": seed, "schedules": len(rows),
                         "block": CL.BLOCK, "min_blocks": CL.MIN_BLOCKS,
                         "closure_gate": CL.CLOSURE_SIGN, "null_max": CL.NULL_CLOSURE_MAX},
            "readout_span": readout_diag, "schedules": rows, "read": read,
            "loss_coupling": "NONE — monitor-only (a_train_inline_gauge); no term reaches the loss",
            "reading": ("MONITOR-ONLY, DIRECTIONAL. A rung-1 ANCHOR says the model's contingency "
                        "structure (not its action marginal — that is what the yoked open control "
                        "removes) leaves a fingerprint on its own next input in THIS toy world. A "
                        "THERMOSTAT CLEARS RUNG 1: no aliveness/consciousness claim follows. "
                        "REFUSED means the instrument did not certify, which is a statement about "
                        "the instrument, never about the model.")}

# ════════════════════════════════════════════════════════════════════════════
#  H_9841 — IMAGINATION RECONSOLIDATION LANE (training-time N3/REM rehearsal)
#
#  WHY THIS EXISTS (the p8 asymmetry it closes, MEASURED in origin/main, not assumed):
#  the daemon ALREADY grows on rehearsal. cli/chat.py:3350-3380 enters an N3/REM phase
#  (`dr_imagination_active(stage) == 1`), calls the SAME core functions this lane calls
#  — `ir_select_snapshots` → `ir_replay_tick` — and then, per replay tick, advances a
#  LIVE `vadapt_field_step` on the session AdaptField (chat.py:3375, wired 2026-07-10,
#  lesionable there with `--imag-growth off`). core/imagination_replay.py's own header
#  states the asymmetry: `ir_mitosis_tick_during_replay` is a log record
#  (`wired_to_lib=False`), but "The REAL AdaptField growth is WIRED daemon-side".
#
#  So a growth hook fires on every replay tick at DAEMON time and has NO counterpart at
#  TRAINING time. p8 says there is no train/infer split; that gap is the most concrete
#  instance of the violation in the tree. This lane is the missing counterpart.
#
#  WHAT IT DOES (single forward, shape-preserving, DDP-safe, rank-local):
#    · every step the lane pushes the window the trainer actually saw (x‖y, the exact
#      row — never a re-materialized approximation) into the daemon's OWN WAKE working
#      ring (core/wake_memory.mem_push_ctx, cap 20 FIFO);
#    · every --reconsolidate-every steps it enters an N3/REM phase: it selects snapshots
#      with the daemon's `ir_select_snapshots`, `ir_replay_tick`s each one under an
#      INVARIANT WATCH (emit_count must be 0 — a rehearsal that speaks is a p5 violation
#      and hard-fails the run), fires the growth hook when --vadapt-on-replay is set, and
#      re-trains the rehearsed rows IN PLACE of that many fresh rows.
#
#  WHAT MAKES THE HOOK CAUSAL (and therefore lesionable): the replay DOSE is
#  `ir_consolidation_gain(n_replayed, density)` and `density` is the ONE thing the hook
#  changes — with the hook ON it is `dr_density(splits, ticks)`, the growth the rehearsal
#  actually CAUSED in the field; with the hook OFF it is the fixed N3 prior
#  `dr_mitosis_prior(3)` = 0.80, exactly the constant `ir_mitosis_tick_during_replay`
#  records. Rehearsing content the field already holds produces zero splits ⇒ density 0
#  ⇒ gain 0 ⇒ ZERO rows replayed: the lane refuses to spend gradient on content that
#  taught the substrate nothing. That is the whole manipulation, and it is why
#  `--vadapt-on-replay` off is a real control and not a weaker treatment.
#
#  a_train_inline_gauge: the consolidation gain is a SCHEDULE (a function of the replay
#  count and the field's growth), NOT a model-quality gauge — no loss, CE, logit or
#  validation number feeds it, and `ir_effective_age` is emitted MONITOR-ONLY.
#
#  DEFAULT OFF (--imagination-replay 0.0) ⇒ every line below is skipped and the run is
#  byte-identical (verified: two 30-step CPU runs, lane-absent vs --imagination-replay
#  0.0, produce the same CE trace).
# ════════════════════════════════════════════════════════════════════════════

IMAG_SPLIT_SEED = "anima|imagination-reconsolidation|H_9841"


def _imag_byte_feature(byte_list, dim=8):
    """DIM=8 byte-statistics feature — the construction cli/chat.py `_afs_byte_feature`
    (anima.hexa:5400 · H_1163 `_byte_feature` VERBATIM) feeds `vadapt_field_step`.

    chat.py takes a STRING and encodes it; the trainer's tokens ARE bytes already (V=256,
    the text column is concatenated UTF-8 → raw bytes), so the encode step is a no-op here
    and the statistic is applied directly to the window. Values are masked to a byte so a
    non-byte vocab could never silently shift the feature scale. Kept local rather than
    imported from cli/chat.py: the trainer must not pull the daemon (numpy + the whole A⇄G
    loop) into a training process."""
    n = len(byte_list)
    if n == 0:
        return [0.0] * dim
    fn_n = float(n)
    total = sumsq = 0.0
    n_hi = n_low = n_sp = n_dig = n_pun = n_lt64 = 0
    for tok in byte_list:
        byte = int(tok) & 0xFF
        bf = float(byte)
        total += bf
        sumsq += bf * bf
        if byte >= 128: n_hi += 1
        if 97 <= byte <= 122: n_low += 1
        if byte == 32: n_sp += 1
        if 48 <= byte <= 57: n_dig += 1
        if 33 <= byte <= 64: n_pun += 1
        if byte < 64: n_lt64 += 1
    mean = total / fn_n
    var = sumsq / fn_n - mean * mean
    return [
        (mean / 255.0) * 5.0,
        (float(n_hi) / fn_n) * 5.0,
        (float(n_low) / fn_n) * 5.0,
        (float(n_sp) / fn_n) * 5.0,
        (float(n_dig) / fn_n) * 5.0,
        (var / (255.0 * 255.0)) * 5.0,
        (float(n_pun) / fn_n) * 5.0,
        (float(n_lt64) / fn_n) * 5.0,
    ]


class ImaginationLane:
    """Training-time twin of the daemon's N3/REM replay phase (cli/chat.py:3350-3380).

    Every core call below is the REAL production function — core/imagination_replay.py,
    core/wake_memory.py, core/dream_lib.py and core/engine_cli.py's VAdaptField — imported,
    never re-implemented (`a_experiment_engine_native`: the instrument is engine-native too).

    THE FIELD IS SEEDED ON THE FIRST REHEARSED WINDOW, not on a session seed as the daemon
    does. That is a deliberate, STRICTER choice and it is load-bearing for the pedestal: with
    a session-seed origin, rehearsing 20 byte-identical windows still splits ONCE (the first
    tick's reconstruction error against an unrelated seed clears 0.30), so a structure-free
    input would manufacture a small non-zero dose. Seeded on its own first window, a
    novelty-free rehearsal has reconstruction error 0 at every tick and the dose is EXACTLY
    0 — a zero-truth pedestal with no threshold in it."""

    def __init__(self, ratio, every, vadapt_on, select, seed, dim=8):
        import imagination_replay as IR                # core/imagination_replay.py
        import wake_memory as WM                       # core/wake_memory.py
        import dream_lib as DL                         # core/dream_lib.py
        import engine_cli as EC                        # core/engine_cli.py (VAdaptField)
        self.IR, self.WM, self.DL, self.EC = IR, WM, DL, EC
        self.ratio = float(ratio)
        self.every = int(every)
        self.vadapt_on = bool(vadapt_on)
        self.select = select
        self.dim = dim
        self.mem = WM.mem_init()
        self.cfg = EC.engine_config_default()          # mitosis ON = the daemon's own cfg
        self.afield = None                             # seeded on the first rehearsed window
        self.rng = random.Random(int(seed))
        self.n_phases = 0
        self.n_ticks = 0
        self.n_splits = 0
        self.n_rows_replayed = 0
        self.emit_violations = 0
        self.last = {}

    # ── WAKE: the trainer's own stream fills the daemon's working ring ────────────
    def observe(self, x_row, y_row):
        """Push ONE window (x‖y, flat ints) into the WAKE working ring (cap 20 FIFO)."""
        self.mem = self.WM.mem_push_ctx(self.mem, list(x_row) + list(y_row))

    def due(self, step):
        return self.every > 0 and step % self.every == 0

    # ── N3/REM: rehearse, watch the invariant, grow, dose ─────────────────────────
    def reconsolidate(self, step, budget):
        """Run one N3/REM phase. Returns (rehearsed_windows, record).

        `budget` = how many rows the caller is willing to hand over. The number actually
        returned is the CONSOLIDATION-SCALED dose, which is what the growth hook moves."""
        IR, DL, EC = self.IR, self.DL, self.EC
        snaps = IR.ir_select_snapshots(self.mem, step, budget)
        if self.select == "random" and snaps:
            # CONTROL B — isolates whether ir_select_snapshots' RECENCY policy is causal:
            # same ring, same count, the recency ordering destroyed.
            pool = self.IR.ir_select_snapshots(self.mem, step, len(self.mem["working"]))
            snaps = [pool[i] for i in self.rng.sample(range(len(pool)), min(len(snaps), len(pool)))]
        splits = 0
        for snap in snaps:
            rec = IR.ir_replay_tick(snap)
            if rec["emit_count"] != 0:
                self.emit_violations += 1
            _imag_emit_watch(rec, step)            # p5 — hard-exits on a speaking rehearsal
            self.n_ticks += 1
            if self.vadapt_on:
                feat = _imag_byte_feature(rec["ctx_tokens"], self.dim)
                if self.afield is None:
                    self.afield = EC.vadapt_field_new(feat, 2048)
                    continue                          # the seed tick cannot be its own split
                before = EC.vadapt_field_cells(self.afield)
                self.afield = EC.vadapt_field_step(self.afield, feat, self.cfg)
                splits += EC.vadapt_field_cells(self.afield) - before
        self.n_splits += splits
        # THE ONE VARIABLE the hook moves: realized growth density vs the fixed N3 prior.
        if self.vadapt_on:
            density = DL.dr_density(splits, len(snaps))
        else:
            density = DL.dr_mitosis_prior(3)          # 0.80 — the constant the log record carries
        gain = IR.ir_consolidation_gain(len(snaps), density)
        n_rows = min(len(snaps), int(round(gain * len(snaps))))
        # MONITOR-ONLY (a_train_inline_gauge): never enters the loss, reported for the log.
        eff_age = IR.ir_effective_age(float(self.every), len(snaps), density)
        self.n_phases += 1
        self.n_rows_replayed += n_rows
        self.last = {
            "step": step, "snapshots": len(snaps), "splits": splits,
            "cells": (EC.vadapt_field_cells(self.afield) if self.afield is not None else 0),
            "density": density, "consolidation": gain, "rows_replayed": n_rows,
            "effective_age": eff_age, "emit_violations": self.emit_violations,
        }
        return [s["ctx_tokens"] for s in snaps[:n_rows]], self.last

    def summary(self):
        return {"phases": self.n_phases, "replay_ticks": self.n_ticks,
                "vadapt_splits": self.n_splits, "rows_replayed": self.n_rows_replayed,
                "emit_violations": self.emit_violations,
                "cells": (self.EC.vadapt_field_cells(self.afield)
                          if self.afield is not None else 0),
                "select": self.select, "vadapt_on_replay": self.vadapt_on}


def _imag_emit_watch(rec, step):
    """p5 INVARIANT WATCH — rehearsal must not speak.

    Not a warning and not a counter: a replay tick that emits means the imagination lane has
    become a mouth, which is the one thing p5 forbids, and every number produced after it would
    be unreadable. Factored out of the lane so the certification battery can PLANT a violation
    and prove the watch actually fires — a guard only ever observed not-firing is not a guard."""
    if rec["emit_count"] != 0:
        raise SystemExit("[imagination] p5 INVARIANT VIOLATED — ir_replay_tick returned "
                         "emit_count=%d at step %s (rehearsal must be emit-free). Refusing to "
                         "continue: an imagination lane that speaks is a mouth."
                         % (rec["emit_count"], step))


def _imag_dose_floor():
    """Smallest replay budget whose dose can reach ONE row even at MAXIMUM growth density.

    SELF-CAUGHT, and the reason this function exists: the dose is `round(gain * n)` rows, and
    `ir_consolidation_gain` saturates slowly (per-replay refresh 0.04), so for small n the
    product rounds to 0 for EVERY possible density. The first run of the certification battery
    below reported INSTRUMENT-DEAD at the (ring 8, budget 3) geometry — measured gain 0.0779 on
    a signal the lane clearly saw (2 field splits) yet 0 rows replayed. A lane configured under
    this floor is not a weak lane, it is an INERT one that still logs "lane ON": exactly the
    silent-no-op class of defect. The floor is DERIVED by asking the engine's own function, not
    chosen — nothing here is tunable, and it is enforced as a refusal (`no-tune-to-green`)."""
    import imagination_replay as IR
    n = 1
    while n < 4096:
        if int(round(IR.ir_consolidation_gain(n, 1.0) * n)) >= 1:
            return n
        n += 1
    return n


def _imag_ring_of(windows, seed):
    """Build a WAKE ring (core/wake_memory) out of explicit windows — the selftest's
    only way to plant a KNOWN structure into the lane's input."""
    import wake_memory as WM
    mem = WM.mem_init()
    for w in windows:
        mem = WM.mem_push_ctx(mem, w)
    return mem


def _imag_probe(windows, vadapt_on, select, budget, seed):
    """One lane probe on an explicit ring — returns the lane's own record. No torch, no
    model, no corpus: the whole battery below is $0."""
    lane = ImaginationLane(1.0, 1, vadapt_on, select, seed)
    lane.mem = _imag_ring_of(windows, seed)
    _, rec = lane.reconsolidate(1, budget)
    rec["ticks"] = lane.n_ticks
    return rec


def _imag_ring_spread(windows, dim=8):
    """TELEMETRY ONLY — how far apart the ring's windows are IN THE SPACE THE FIELD SPLITS ON.

    Feeds nothing: no arm, no bar, no threshold, no dose reads this (a_train_inline_gauge).
    It exists because H_9838's post-mortem was decidable only once the code geometry itself
    was reported (planted codes within .0469 / across .0117 = effectively orthogonal, real
    reps .0625 / .0260 = 2.2x overlap). `vadapt_field_step` splits when the L2 distance from
    the nearest prototype exceeds its SPLIT_THRESH literal (0.30, core/engine_cli.py), so the
    pairwise L2 spread of `_imag_byte_feature` over the ring is the ONE number that says
    whether a ring could have split the field at all — and therefore whether a plant that
    does not fire is a fact about the content or an artefact of how the content was made."""
    feats = [_imag_byte_feature(w, dim) for w in windows]
    n = len(feats)
    if n < 2:
        return {"n": n, "mean_pairwise_l2": 0.0, "min_pairwise_l2": 0.0, "max_pairwise_l2": 0.0}
    dists = []
    for i in range(n):
        for j in range(i + 1, n):
            s = 0.0
            for k in range(dim):
                dv = feats[i][k] - feats[j][k]
                s += dv * dv
            dists.append(math.sqrt(s))
    return {"n": n, "mean_pairwise_l2": sum(dists) / len(dists),
            "min_pairwise_l2": min(dists), "max_pairwise_l2": max(dists)}


def _imag_real_anchors(dir_path):
    """H_9841-R — REAL ring content: the payload bytes of a REAL `.kosmos` anchor store.

    WHY THIS EXISTS — the H_9838 planted-geometry failure (2026-07-21). H_9838 landed a
    headline positive (CA3 multi-step completion at 12x derived chance, lesion at the floor,
    3 seeds x 3 geometries, independently reproduced) on a store whose codes were a PLANTED
    INTEGER FIXTURE. When the code source alone was swapped for the production trunk's REAL
    penultimate representations — same arms, same controls, same bars — the ZERO-TRUTH
    PEDESTAL FIRED: at 16 items the value-shuffled pedestal read 0.3750 against a 0.3077 bar
    (INVALID), and at 32 items 0.1562 against 0.1500 (INVALID). Diagnosis: the planted codes
    were effectively orthogonal (within .0469 / across .0117) while real reps overlap 2.2x
    (.0625 / .0260). Hand-made favourable geometry, not the mechanism, had produced the bar.

    THIS BATTERY HAS THE SAME EXPOSURE. `run_imagination_selftest`'s ring is synthesized by
    `novel(n, w, off) = (off + i*37 + j*7) % 256` — an arithmetic lattice whose windows are
    spread across the 8-dim byte statistic BY CONSTRUCTION, which is precisely the property
    `vadapt_field_step` splits on. Real snapshots do not look like that: they carry real
    novelty structure, real lengths and REAL REPETITION, and `ir_consolidation_gain` /
    `ir_effective_age` are computed from exactly those statistics. So the same swap is run
    here: this flag replaces the SYNTHESIZED ring — and nothing else — with real content.

    WHY .kosmos AND NOT `clm_penult_pooled_W`. The field's split test is an ABSOLUTE L2
    threshold (`core/engine_cli.vadapt_field_step`, SPLIT_THRESH = 0.30) read against
    `_imag_byte_feature`'s 8-dim, ~[0,5]-scaled statistic. Handing it a 768-dim penultimate
    vector instead would change the L2 scale that FIXED threshold is compared against — i.e.
    it would move the bar while claiming to move only the input, which is the one thing the
    swap may not do. The ring is a list of BYTE windows, so the honest swap keeps the byte
    feature and swaps the bytes: a real store read by the production reader.

    READER HONESTY (H_9843): `core/kosmos_io.load_anchors` is measured LOSSY — the @anchor
    line's title is dropped and the text payload comes back STILL-ESCAPED. Both are AUDITED
    in the returned report and NEITHER is repaired here: this lane consumes payload BYTES,
    and silently repairing the reader inside the measurement would swap the input twice.
    """
    import kosmos_io as KI                              # core/kosmos_io.py (production reader)
    recs = KI.load_anchors(dir_path)
    pool, lens, escaped = [], [], 0
    for rec in recs:
        txt = rec.get("text_payload", "")
        if not txt:
            continue
        if "\\" in txt:
            escaped += 1
        raw = list(txt.encode("utf-8", "surrogateescape"))
        pool.append((rec.get("name", ""), raw))
        lens.append(len(raw))
    audit = {
        "dir": dir_path,
        "anchors_read": len(recs),
        "with_text_payload": len(pool),
        "payload_bytes_min": (min(lens) if lens else 0),
        "payload_bytes_max": (max(lens) if lens else 0),
        "payload_bytes_total": sum(lens),
        "payloads_still_escaped": escaped,
        "titles_recovered": sum(1 for r in recs if "title" in r.get("fields", {})),
        "reader": "core/kosmos_io.load_anchors (production reader, unmodified)",
        "reader_caveat": ("H_9843 measured this reader LOSSY (titles dropped · payload "
                          "returned still-escaped). Audited, not repaired — the lane eats "
                          "payload BYTES and repairing the reader would change the input twice."),
    }
    return pool, audit


def run_imagination_selftest(ratio, every, vadapt_on, select, seed, real_source=""):
    """H_9841 — $0 certification battery for the imagination-reconsolidation lane.

    GATE ORDER IS FROZEN AND SEQUENTIAL (the shape cli/corpus.py::run_mi_screen landed):
      ① POSITIVE CONTROL — a ring of MUTUALLY DISTINCT windows is a planted signal: novel
         rehearsal must split the field and buy a non-zero dose. If it does not fire, the
         lane cannot see a signal that is known to be there ⇒ INSTRUMENT-DEAD, stop, and
         report NO treatment row.
      ② ZERO-TRUTH PEDESTAL — two structure-free inputs the lane must REFUSE:
           (a) an EMPTY ring (nothing to rehearse) ⇒ 0 snapshots, gain exactly 0.0;
           (b) a ring of 20 BYTE-IDENTICAL windows (rehearsal with no novelty in it) ⇒ 0
               splits, density exactly 0.0, dose exactly 0 rows.
         If either fires, the lane MANUFACTURES consolidation ⇒ INVALID, stop.
      ③ ROBUSTNESS — ① and ② are re-run at 3 ring/budget geometries × 2 seeds. If the
         plant>pedestal ordering flips with a knob, that is a defect in THIS instrument,
         not a result (H_9844 found exactly that failure in the mi-screen and had to gate
         against it) ⇒ GEOMETRY-DEPENDENT, refuse.
      ④ Only then the arms: --vadapt-on-replay ON vs OFF (is the growth hook causal?) and
         recency vs random selection (is ir_select_snapshots' policy causal?).
    The p5 INVARIANT WATCH runs inside every probe: any emit_count>0 hard-exits the process.

    SCOPE, pre-registered (honesty gate): this battery certifies the INSTRUMENT and the
    lane's own quantities — field growth, consolidation gain, replay dose, emit-freedom.
    It is NOT a training result. It says nothing about whether rehearsal changes what the
    model learns, and — per H_9790, which measured imagination as DIRECTIONAL: it reached
    interior structure and did NOT reach the mouth — the pre-registered likely outcome for
    any follow-on training run is the SAME mouth 미도달 wall."""
    def novel(n, w, off=0):
        return [[(off + i * 37 + j * 7) % 256 for j in range(w)] for i in range(n)]

    def flat(n, w):
        return [[7] * w for _ in range(n)]

    # ── REAL-INPUT SWAP (--imagination-real-source · H_9838 precedent) ────────────────────
    # Everything from here down — gate order, bars, thresholds, arms, controls, the seed
    # policy — is UNCHANGED. The ONLY difference is where the ring's bytes come from.
    real_pool, real_audit = ([], None)
    if real_source:
        real_pool, real_audit = _imag_real_anchors(real_source)

    def real_take(n, w, off):
        """n REAL windows of width w — one ring slot per STORED SNAPSHOT, which is the shape
        `mem_push_ctx` has in vivo (one ctx per push). Truncated to w, NEVER padded: a pad
        byte is invented content and would re-manufacture the very uniformity this swap
        exists to remove. `off` rotates the START of the anchor list exactly as it shifted
        the planted content on the synthetic path, so the robustness axis keeps its meaning
        (WHICH real content, not merely which rng). Anchors shorter than w are skipped, and
        the shortfall is reported as `realized_ring`, never padded away."""
        elig = [b for (_nm, b) in real_pool if len(b) >= w]
        if not elig:
            return []
        r = off % len(elig)
        elig = elig[r:] + elig[:r]
        return [b[:w] for b in elig[:n]]

    def real_flat(n, w, off):
        """The novelty-free pedestal, MATCHED to the real path's covariate: ONE real window
        repeated. Same real byte marginal as the plant, all across-window novelty removed.
        A synthetic `[7]*w` pedestal against a real-content arm would be a control from a
        different world than the arm it pedestals (control-must-match-mediating-covariate);
        the pedestal's ROLE — structure-free input the lane must refuse — is identical."""
        base = real_take(1, w, off)
        if not base:
            return []
        return [list(base[0]) for _ in range(n)]

    # (ring, window, budget). budget < ring on purpose in ③/④: at budget == ring the recency
    # and random arms select the SAME SET (only the order differs), so the selection-policy
    # control would be an ORDER control wearing a membership control's name.
    geometries = [(20, 32, 8), (8, 16, 3), (20, 64, 5)]
    dose_floor = _imag_dose_floor()
    out = {"instrument": "imagination-selftest", "hypothesis": "H_9841",
           "dose_floor": {
               "budget_floor_rows": dose_floor,
               "derived_from": "ir_consolidation_gain(n, density=1.0) * n >= 0.5",
               "why": ("below this budget round(gain*n)==0 at EVERY density, so the lane is "
                       "structurally inert while still logging 'lane ON'. Geometries below the "
                       "floor are marked and their rows_replayed==0 is BY CONSTRUCTION, not a "
                       "null; the trainer REFUSES such a configuration outright."),
           },
           "engine": "core/imagination_replay.py + core/wake_memory.py + "
                     "core/dream_lib.py + core/engine_cli.py (VAdaptField)",
           "daemon_counterpart": "cli/chat.py:3350-3380 (N3/REM replay + live "
                                 "vadapt_field_step per tick, wired 2026-07-10)"}
    # ⓪ THE WATCH ITSELF — plant a speaking rehearsal and require the p5 guard to fire.
    #    A guard that has only ever been observed NOT firing certifies nothing.
    try:
        _imag_emit_watch({"emit_count": 1}, "planted")
        watch_fires = False
    except SystemExit:
        watch_fires = True
    _imag_emit_watch({"emit_count": 0}, "planted-null")   # …and must NOT fire on a silent tick
    out["p5_watch_control"] = {
        "planted_violation_detected": watch_fires,
        "silent_tick_passes": True,
        "why": "the p5 hard-exit is proven to fire on a planted emit_count=1 and to pass a 0.",
    }
    rows, plant_ok, ped_ok = [], True, True
    underpowered_any = False
    for (n_ring, w, budget) in geometries:
        for s in (seed, seed + 4):
            # the seed shifts the PLANTED CONTENT, not just an rng: the recency path is
            # deterministic, so a seed that only reseeded random.Random would leave the
            # robustness axis vacuous (it did, in the first run of this battery).
            if real_source:
                p_wins = real_take(n_ring, w, s)
                f_wins = real_flat(len(p_wins), w, s)
            else:
                p_wins = novel(n_ring, w, off=s)
                f_wins = flat(n_ring, w)
            # REALIZED n is reported, never stretched: a real store that cannot fill the
            # requested geometry makes that geometry UNDERPOWERED, and an underpowered null
            # is not a negative result (power-before-negative-verdict).
            realized = len(p_wins)
            under = bool(real_source) and realized < n_ring
            underpowered_any = underpowered_any or under
            p = _imag_probe(p_wins, True, "recency", budget, s)
            e = _imag_probe([], True, "recency", budget, s)
            f = _imag_probe(f_wins, True, "recency", budget, s)
            # FIRING is read on the lane's CAUSAL quantities (the field split, the gain).
            # `rows_replayed` is the DERIVED dose and it is required only above the derived
            # dose floor — below the floor a 0 is arithmetic, not a null, and reading it as a
            # null is what made the first run of this battery declare itself dead.
            below = budget < dose_floor
            fires = p["splits"] > 0 and p["consolidation"] > 0.0 and (below or p["rows_replayed"] > 0)
            refuses = (e["snapshots"] == 0 and e["consolidation"] == 0.0
                       and f["splits"] == 0 and f["density"] == 0.0
                       and f["consolidation"] == 0.0 and f["rows_replayed"] == 0)
            plant_ok = plant_ok and fires
            ped_ok = ped_ok and refuses
            rows.append({"geometry": {"ring": n_ring, "window": w, "budget": budget},
                         "seed": s, "below_dose_floor": below,
                         "realized_ring": realized, "underpowered": under,
                         "plant_feature_spread": _imag_ring_spread(p_wins),
                         "plant_fires": fires, "pedestal_refuses": refuses,
                         "plant": p, "pedestal_empty": e, "pedestal_flat": f})
    if not watch_fires:
        out["status"] = "INSTRUMENT-DEAD"
        out["why"] = ("the p5 invariant watch did NOT fire on a PLANTED emit_count=1 — the guard "
                      "that is supposed to stop a speaking rehearsal cannot see one, so every "
                      "'emit_violations: 0' below would be worthless.")
    elif not plant_ok:
        out["status"] = "INSTRUMENT-DEAD"
        out["why"] = ("the planted signal (a ring of mutually distinct windows) did NOT move the "
                      "lane — no field split and/or no dose. A null on real data would then be a "
                      "property of the instrument, not of rehearsal.")
    elif not ped_ok:
        out["status"] = "INVALID"
        out["why"] = ("a zero-truth pedestal FIRED — the lane reports consolidation on an empty "
                      "ring and/or on a rehearsal with no novelty in it, i.e. it MANUFACTURES "
                      "the quantity it exists to measure.")
    else:
        out["status"] = "CERTIFIED"
        out["why"] = ("plant fires and both pedestals refuse at every geometry x seed — the "
                      "ordering is not a knob artefact.")
    # REAL-INPUT POWER GATE. A real store that cannot fill the requested geometry makes the
    # row undecidable in BOTH directions, so neither a pass nor a plant-null may be read off
    # it (power-before-negative-verdict). A FIRED PEDESTAL is exempt: manufacturing
    # consolidation on structure-free input is a positive event and stays INVALID at any n.
    if real_source and underpowered_any:
        _real_n = [r["realized_ring"] for r in rows]
        if out["status"] in ("CERTIFIED", "INSTRUMENT-DEAD") and watch_fires:
            out["status"] = "REAL-UNDERPOWERED"
            out["why"] = ("the real .kosmos store cannot fill the requested geometry — realized "
                          "ring sizes %s against requested %s. Neither the plant nor its absence "
                          "is readable at this n; reported as UNDERPOWERED with the realized n "
                          "rather than stretched." % (_real_n, [g[0] for g in geometries]))
    out["controls"] = rows
    if real_audit is not None:
        out["real_source"] = real_audit
    if out["status"] == "CERTIFIED":
        ring, w, budget = geometries[0]
        wins = (real_take(ring, w, seed) if real_source else novel(ring, w, off=seed))
        on = _imag_probe(wins, True, "recency", budget, seed)
        off = _imag_probe(wins, False, "recency", budget, seed)
        # CONTROL B is drawn on SEVERAL seeds: it is the only arm with an rng in it, so a
        # single draw could not tell a policy effect from one lucky sample.
        rnds = [_imag_probe(wins, True, "random", budget, seed + k) for k in range(5)]
        rnd_c = [r["consolidation"] for r in rnds]
        out["arms"] = {
            "vadapt_on_recency": on,
            "vadapt_off_recency": off,      # CONTROL A — replay happens, hook lesioned
            "vadapt_on_random": rnds,       # CONTROL B — hook fires, selection policy destroyed
            "hook_delta_consolidation": on["consolidation"] - off["consolidation"],
            "policy_delta_consolidation_range": [min(rnd_c), max(rnd_c)],
            "policy_recency_inside_random_range":
                bool(min(rnd_c) <= on["consolidation"] <= max(rnd_c)),
            "reading": ("hook_delta is NEGATIVE by construction whenever the realized growth "
                        "density falls below the fixed N3 prior 0.80 — the hook does not add "
                        "dose, it CORRECTS it, and the direction is the measurement. "
                        "policy: if recency sits INSIDE the random arm's range, the selection "
                        "POLICY is not doing work at this ring size and must not be claimed."),
        }
        out["p5_invariant"] = {
            "emit_violations_total": sum(r["plant"]["emit_violations"]
                                         + r["pedestal_empty"]["emit_violations"]
                                         + r["pedestal_flat"]["emit_violations"] for r in rows)
                                    + on["emit_violations"] + off["emit_violations"]
                                    + sum(r["emit_violations"] for r in rnds),
            "replay_ticks_watched": sum(r["plant"]["ticks"] + r["pedestal_flat"]["ticks"]
                                        for r in rows) + on["ticks"] + off["ticks"]
                                    + sum(r["ticks"] for r in rnds),
            "reading": "every ir_replay_tick was checked; emit_count>0 hard-exits the process (p5).",
        }
    out["requested"] = {"imagination_replay": ratio, "reconsolidate_every": every,
                        "vadapt_on_replay": bool(vadapt_on), "select": select, "seed": seed,
                        "real_source": real_source}
    out["scope"] = ("INSTRUMENT CERTIFICATION ONLY — this is not a training result and not a "
                    "verdict. It bounds what the lane's own quantities do; whether rehearsal "
                    "changes what the model LEARNS, let alone what it SAYS, is unmeasured here. "
                    "H_9790 measured imagination as DIRECTIONAL (interior reached, mouth NOT), "
                    "and that same mouth-미도달 outcome is pre-registered as the likely result "
                    "of any follow-on training run.")
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["status"] == "CERTIFIED"
             else (3 if out["status"] == "INVALID"
                   else (5 if out["status"] == "REAL-UNDERPOWERED" else 4)))


def _store_source_train(a):
    """V6_36 STORE-SOURCE — train a lane_type 9 (SRC) authorship head on a FROZEN trunk, then
    serialize a lane-9 .clm. Trains {W_q, val, w_A, b_A} only (the trunk/mouth are never touched, and
    the lane never writes the mouth). Loss = BCE(σ(s_A), auth[target]) + 0.5·CE(att, target_slot)
    (H_9672 aux addressing supervision; address ⊥ auth by cue-pairing, so it teaches WHERE not
    WHICH-value). Manifest = the anima-store-source/v1 rings. Engine-native (decode.clm_forward_hidden
    + clms.pack_clms). This is the frozen-trunk head fit; the SELF-sampling manifest build is
    --store-source-build (evaluate side)."""
    import numpy as np
    import decode as _dec
    import clms as _clms
    base = a.store_source_init
    if not base:
        sys.exit("[store-source] --store-source needs --store-source-init <base.clm> to warm-start from")
    if not a.out:
        sys.exit("[store-source] --store-source needs --out <lane9.clm>")
    W = _dec.clm_load_weights(base)
    if not W.get("ok"):
        sys.exit("[store-source] base ckpt not decodable (clm): " + base)
    d = W["d"]; man = json.load(open(a.store_source))
    entries = man.get("entries", []); n_slot = int(man.get("n_slot", 8))
    d_k, d_s = int(a.store_source_dk), int(a.store_source_ds)
    rng = np.random.default_rng(a.seed)
    key_emb = rng.standard_normal((256, d_k)).astype(np.float32)   # FROZEN address table

    def qh(cue):
        b = list(("src " + cue + " => ").encode("ascii"))
        yn = _dec.clm_forward_hidden(W, np.array([float(x) for x in b], dtype=np.float64), len(b))
        return yn[-1].astype(np.float32)

    H, Ks, Pol, Auth, Tgt = [], [], [], [], []
    for e in entries:
        cues = e["cues"]; tgt = int(e["target_slot"]); pols = np.asarray(e["pols"], np.int64)
        H.append(qh(cues[tgt]))
        Ks.append(np.stack([_clms._entity_key(key_emb, c, "roll") for c in cues]).astype(np.float32))
        Pol.append(pols); Auth.append(int(pols[tgt])); Tgt.append(tgt)
    H = torch.tensor(np.stack(H)); Ks = torch.tensor(np.stack(Ks)); Pol = torch.tensor(np.stack(Pol))
    Auth = torch.tensor(np.array(Auth, np.float32)); Tgt = torch.tensor(np.array(Tgt))
    torch.manual_seed(a.seed)
    Wq = nn.Parameter(torch.randn(d, d_k) * (1/np.sqrt(d)))
    val = nn.Parameter(torch.randn(2, d_s) * 0.3)
    wA = nn.Parameter(torch.randn(d_s) * (1/np.sqrt(d_s))); bA = nn.Parameter(torch.zeros(1))
    opt = torch.optim.Adam([Wq, val, wA, bA], lr=5e-3); scale = 1.0/np.sqrt(d_k)
    for ep in range(int(a.store_source_epochs)):
        opt.zero_grad()
        q = H @ Wq
        al = (q.unsqueeze(1) * Ks).sum(-1) * scale
        att = torch.softmax(al, -1) - 1.0/n_slot
        vv = torch.einsum("bs,bsd->bd", att, val[Pol])
        sA = vv @ wA + bA
        loss = (F.binary_cross_entropy_with_logits(sA, Auth) + 0.5 * F.cross_entropy(al, Tgt))
        loss.backward(); opt.step()
    with torch.no_grad():
        tr_ba = float((((sA >= 0).float() == Auth).float().mean()))
    clms = {"lane_type": 9, "n_slot": n_slot, "d_k": d_k, "d_s": d_s, "key_seed": 1,
            "key_emb": key_emb, "W_q": Wq.detach().numpy().astype("<f4"),
            "val": val.detach().numpy().astype("<f4"),
            "w_A": wA.detach().numpy().astype("<f4"), "b_A": bA.detach().numpy().astype("<f4"),
            "lam": np.array([1.0], "<f4")}
    trailer = _clms.pack_clms(clms)
    open(a.out, "wb").write(open(base, "rb").read() + trailer)
    W2 = _dec.clm_load_weights(a.out)                       # verify the loader reads it back
    cl = W2.get("clms")
    assert cl is not None and int(cl["lane_type"]) == 9, f"[store-source] loader rejected the lane-9 trailer: {cl}"
    print("=== anima-py train --store-source — V6_36 lane_type 9 (SRC) head ===")
    print("base=%s  manifest=%s  rings=%d  d_k=%d d_s=%d  train_BA=%.3f" %
          (base, a.store_source, len(entries), d_k, d_s, tr_ba))
    print("wrote %s (base + lane-9 trailer %dB) · loader reads lane_type=9" % (a.out, len(trailer)))
    print("verdict path: anima-py evaluate %s --store-source <held.json>" % a.out)
    return 0


def main():
    ap = argparse.ArgumentParser(
        description="anima canonical python trainer (`anima-py train`) — CLMConvMoE "
                    "SAVANT+MITOSIS recipe + H_1640 arm×objective compositional levers")
    ap.add_argument("--arch", default="clm", choices=["clm", "bytegpt"],
                    help="trunk architecture: clm=CLMConvMoE (default, .clm out) | "
                         "bytegpt=24-layer GPT-2-class ByteGPT (.bin out) — the CLEAN G1 "
                         "wall (single=2). The arm×objective compositional levers are "
                         "arch-agnostic (operate on logits+penultimate); the CLM-specific "
                         "levers (savant/mitosis/tlora/dict/jamo) are gated OFF for bytegpt.")
    ap.add_argument("--arm", default="ctrl", choices=list(ARMS))
    ap.add_argument("--objective", default="ce_marginal", choices=list(OBJECTIVES),
                    help="OPTIONAL objrun coupling (default ce_marginal = standalone)")
    ap.add_argument("--tlora-rank", type=int, default=TLORA_RANK)
    ap.add_argument("--tlora-no-base", action="store_true", help="drop the dense base")
    ap.add_argument("--comp-lane", action="store_true",
                    help="H_9900 composition lane: a separate answer-span head trained off a "
                         "DETACHED trunk penultimate, so its CE never competes with the language "
                         "stratum (H_9898 measured that competition as the blocker). Multi-byte "
                         "answers, unlike --store-bridge's one-byte readout (H_9899).")
    ap.add_argument("--comp-weight", type=float, default=1.0,
                    help="weight on the composition-lane CE (--comp-lane only)")
    ap.add_argument("--comp-probe-panel", type=str, default="",
                    help="H_9904 weavepanel json — after training, score the LANE HEAD directly on "
                         "it (teacher-forced, no mouth). DIRECTIONAL only: it decides whether the "
                         ".clm format campaign H_9903 scoped is worth opening, never a verdict.")
    ap.add_argument("--dict-lambda", type=float, default=DICT_LAMBDA)
    ap.add_argument("--jamo-lambda", type=float, default=JAMO_LAMBDA)
    # H_9643: enable the N8 jamo(자모) teach-aux INDEPENDENTLY of --arm, so a faction run
    # (--arm ctrl --n-factions 8) can borrow the ko-coherence signal without the TLoRA that
    # tlora_jamo bundles (which would confound the faction measurement). Default off = unchanged.
    ap.add_argument("--jamo-aux", action="store_true",
                    help="H_9643: turn on the jamo teach-aux head regardless of --arm (no tlora)")
    # H_9200 E1 — gated-write forward-slot (SLW). --slw engages the CORE-owned
    # (core/slw.py) module on the CLMConvMoE penultimate; weights serialize into the
    # "SLW\x01" .clm trailer. Plain CE alone induces the slots (rung-3 de-risk 0.976
    # vs additive 0.145), so this is an ARCH lever (--objective stays ce_marginal).
    ap.add_argument("--slw", action="store_true",
                    help="H_9200 E1: engage the gated-write forward-slot (core/slw.py)")
    ap.add_argument("--slw-n-slot", type=int, default=8, help="SLW addressable slots")
    ap.add_argument("--slw-k", type=int, default=64, help="SLW role/read key dim")
    # H_9423 CLMS store-bridge lane (co-trained). --store-bridge = the storebind corpus c.txt (expects
    # a lockstep <c>.store.jsonl manifest, line i <-> store row i from corpus.build_storebind). The lane
    # OVERWRITES the answer-position logits with lam*store_logits — implemented as a CE decomposition
    # (qpos CE on store_logits + non-qpos trunk CE on the prompt spelling), so the trunk logit gets NO
    # answer-position grad = ② shortcut-cut, structural. Window geometry mirrors evaluate.store_run
    # (prompt-aligned, qpos = T-1) so the train tap and the verdict tap coincide.
    ap.add_argument("--store-bridge", type=str, default="",
                    help="H_9423: storebind corpus c.txt to co-train the CLMS lane (core/clms.py)")
    ap.add_argument("--store-source", type=str, default="",
                    help="V6_36: manifest to train a lane_type 9 (SRC) authorship head on a FROZEN "
                         "trunk (warm-start --store-source-init, serialize a lane-9 .clm to --out). "
                         "Trains {W_q,val,w_A,b_A} only; the lane never writes the mouth (structural "
                         "NLL-probe). H_9672 aux L_addr supervises addressing (address ⊥ auth by "
                         "cue-pairing, so it teaches WHERE not WHICH-value).")
    ap.add_argument("--store-source-init", type=str, default="",
                    help="V6_36: base .clm to warm-start the SRC head training (frozen trunk).")
    ap.add_argument("--store-source-dk", type=int, default=24, help="V6_36 SRC key dim d_k")
    ap.add_argument("--store-source-ds", type=int, default=16, help="V6_36 SRC value dim d_s")
    ap.add_argument("--store-source-epochs", type=int, default=400, help="V6_36 SRC head epochs")
    ap.add_argument("--store-win", type=int, default=24,
                    help="CLMS window (MUST equal evaluate --win so train/verdict geometry match)")
    ap.add_argument("--store-batch", type=int, default=8, help="global CLMS sub-batch (div by world)")
    ap.add_argument("--store-ans-weight", type=float, default=1.0, help="answer-position store CE weight")
    ap.add_argument("--store-val-frac", type=float, default=0.05, help="tail block frac for sb val")
    ap.add_argument("--clms-n-slot", type=int, default=8, help="CLMS store slots (match corpus)")
    ap.add_argument("--clms-d-k", type=int, default=64, help="CLMS content-address key dim")
    ap.add_argument("--clms-d-s", type=int, default=64, help="CLMS polarity value dim")
    ap.add_argument("--clms-d-g", type=int, default=64, help="CLMS fusion-bottleneck (yn_q op-gate dim; H_9423 value-read fix)")
    ap.add_argument("--store-fangate", action="store_true",
                    help="H_9696 (R4) CLMS-FAN lane (lane_type 4): the value is projected from the slot's "
                         "OWN key (free ideation has no polarity to index) + a learned query gate replaces "
                         "the '=> ' literal. Default off = the H_9423 storebind lane, byte-identical.")
    ap.add_argument("--store-val-center", action="store_true",
                    help="H_9710 RV-3: majority-null centering v=Σ(aᵢ−1/n)·valᵢ (lane_type 3). At uniform address "
                         "v≡0 so the op⊕majority shortcut basin cannot exist. train+eval consistent (codec bit).")
    ap.add_argument("--store-addr-weight", type=float, default=0.0,
                    help="H_9672: address direct-supervision loss weight L_addr=CE(att,target_slot) (0=off·byte-identical). Cuts the (2) bootstrap deadlock W_q could not escape at 303M.")
    ap.add_argument("--store-query-src", type=str, default="penult",
                    help="H_9720-ⓐ EN-disjoint fresh query lane: 'penult' (default·lane_type≤4·byte-identical) OR "
                         "'fresh:K[@L]' (lane_type 5) — the ADDRESS query reads a detached trunk-layer-L tap "
                         "through W_fresh→W_q_fresh (store-CE only, EN-CE never touches it), K=lane width, "
                         "L=tap depth (default 3, RF≥entity-span). '@penult' (fresh_L=0) = H_9720 C1 "
                         "param-matched-penult control: same head, tap at the penult (capacity vs depth). "
                         "Emergent-address WITHOUT addr-loss (admissible).")
    ap.add_argument("--store-query-tap-grad", type=str, default="detached", choices=["detached", "shared"],
                    help="H_9720 C2 detach-ablation for --store-query-src fresh: 'detached' (default·the CRACK "
                         "arm·store-CE never reaches the trunk through the tap) OR 'shared' (drop .detach() so "
                         "store-CE DOES flow into layers ≤ fresh_L) — tests if gradient-disjointness is load-bearing.")
    ap.add_argument("--store-ans-delay", type=int, default=0,
                    help="H_9692 RV-2: hold the answer-CE (sb_w=0) for the first N steps so only the address "
                         "(addr-loss) trains; the blurry-v window can\'t commit the MLP to op-only before the "
                         "address is sharp. Then ans-CE turns on. 0=off·byte-identical.")
    ap.add_argument("--store-oracle-aux", type=float, default=0.0,
                    help="H_9691 RV-1: weight of an extra CE on the ORACLE(correct one-hot) address every step "
                         "(dual-path with softmax+--store-addr-weight) → trains the value/MLP on correct v so it "
                         "learns the XOR function robustly (fixes val-read seed-fragility). 0=off·byte-identical.")
    ap.add_argument("--store-oracle-train", action="store_true",
                    help="H_9423 Stage1.5: hand the address for free during TRAINING (oracle_slot=target_slot) "
                         "→ separates value-read (a) from address-learning (c). DIAGNOSTIC, not a production lever.")
    ap.add_argument("--store-oracle-warmup", type=int, default=0,
                    help="H_9672: for the first N steps hand the address free (oracle_slot) so val differentiates "
                         "cleanly, THEN switch to softmax address (+ --store-addr-weight learns W_q on the "
                         "differentiated val). Fixes the val-read seed-fragility addr-loss alone left. 0=off.")
    ap.add_argument("--clms-r", type=int, default=128, help="CLMS GELU-MLP fusion bottleneck")
    ap.add_argument("--clms-dual", action="store_true",
                    help="read the store twice through the shared W_q and compose the two soft binary "
                         "values with canonical parity a+b-2ab (lane_type 10). Single-clue rows use "
                         "B=0, so train and held-out pairs share one learned value manifold; legacy "
                         "lane-8 checkpoints remain decode-compatible.")
    ap.add_argument("--clms-vonly", action="store_true",
                    help="H_9885 (lane_type 7): hold the g half of the CLMS fusion input at ZERO so the "
                         "answer can only be a function of the retrieved store value. This REMOVES "
                         "capacity rather than adding it — the composed wall's last live account is "
                         "that the trunk path g alone fits the trained rows, so v never earns gradient.")
    ap.add_argument("--clms-key-seed", type=int, default=9423, help="CLMS frozen key_emb table seed")
    ap.add_argument("--clms-lam0", type=float, default=1.0, help="CLMS lam init (store_only scale)")
    ap.add_argument("--clms-key-fn", choices=("mean", "roll"), default="mean",
                    help="CLMS content-address function: mean (shipped, order-blind H_9850) "
                         "| roll (order-aware, parameter-free, lane_type 6 · H_9852)")
    # H_9698 MBND mouth-binder lane (R6). --mouth-binder engages it; the linear arm is the INTERNAL
    # NEGATIVE CONTROL that must reproduce kill#7's fixed-role linear collapse (uniform address +
    # additive combine), so a nonlinear number is only readable next to it.
    ap.add_argument("--mouth-binder", choices=["bilinear", "linear"], default="",
                    help="H_9698: co-train the MBND mouth-binder lane. bilinear = Hadamard binder; "
                         "linear = the kill#7 DOA control (uniform address + additive combine)")
    ap.add_argument("--mouth-memory", choices=["causal-bank"], default="causal-bank",
                    help="H_9698: what the binder addresses (causal-bank = the frame's own hiddens)")
    # ── H_9803 BRANCH-LATENT IDEATION FAN (ρ·fan / G6 lane) ──────────────────────────────────
    # The lane is DEFAULT-OFF and every flag below is inert unless --ideation-lane branch-latent
    # is passed ⇒ byte-identical golden path. See core/ifan.py for why this is not a sampling
    # trick: the ONLY thing separating the K branches is a min-cost assignment onto SEVERAL REAL
    # observed continuations. There is no repulsion term and no entropy bonus anywhere in the lane.
    ap.add_argument("--ideation-lane", choices=["off", "branch-latent"], default="off",
                    help="H_9803: 'branch-latent' builds K disjoint proposal latents from a preserved "
                         "early tap, each responsible for a DIFFERENT observed future-continuation mode. "
                         "'off' (default) ⇒ byte-identical.")
    ap.add_argument("--ideation-branches", type=int, default=4,
                    help="H_9803: K — number of disjoint proposal latents (branches).")
    ap.add_argument("--ideation-objective", choices=["set-ce"], default="set-ce",
                    help="H_9803: 'set-ce' = min-cost (Hungarian) branch↔target assignment over the SET "
                         "of observed continuations, then mean assigned CE. The only objective that "
                         "grounds diversity in real futures; a repulsion/entropy variant is DISQUALIFIED.")
    ap.add_argument("--ideation-route", choices=["l3-disjoint", "penult"], default="l3-disjoint",
                    help="H_9803: 'l3-disjoint' = the branch latents read the DETACHED trunk-layer-L tap "
                         "(H_9720 tap-DEPTH; set-CE never pushes the trunk through this path) · "
                         "'penult' = read the penultimate instead (tap-DEPTH control).")
    ap.add_argument("--ideation-route-l", type=int, default=3,
                    help="H_9803: L — tap depth for --ideation-route l3-disjoint (default 3).")
    ap.add_argument("--ideation-assign", choices=["hungarian", "shuffle"], default="hungarian",
                    help="H_9803: 'hungarian' = min-cost matching (treatment) · 'shuffle' = THE NEGATIVE "
                         "CONTROL — same K, same targets, same CE mass, but the target↔branch assignment "
                         "is re-drawn every batch, so only the correspondence is destroyed.")
    ap.add_argument("--ideation-corpus", type=str, default="",
                    help="H_9803: multi-mode future-set corpus. Blank-line-separated documents; line 0 = "
                         "the shared context/topic, lines 1..M = M DIFFERENT observed continuations of it. "
                         "REQUIRED when --ideation-lane branch-latent.")
    ap.add_argument("--ideation-rank", type=int, default=64, help="H_9803: proposal-latent width r")
    ap.add_argument("--ideation-lam0", type=float, default=1.0, help="H_9803: IFAN lam init (additive scale)")
    ap.add_argument("--ideation-weight", type=float, default=1.0, help="H_9803: set-CE loss weight")
    ap.add_argument("--ideation-docs", type=int, default=4, help="H_9803: documents per ideation sub-batch")
    # ── H_9805 WRITE-SIDE TENSION FIELD (TFLD lane) ──────────────────────────────────────────
    # Production's tension is a SCALAR on the READOUT side (`conflict_scalar`, rank ~2.66 per
    # H_9714) — the rank-1 seam v1 died on. This lane injects the per-edge parse-disagreement
    # FIELD pre-trunk instead. The lane is DEFAULT-OFF ⇒ byte-identical golden path.
    # `rank1` is NOT a lesser treatment: it is the control that decides whether the field is a
    # field at all, and it is parameter-, lam- and shape-matched to `duel`. See core/tension_field.py.
    ap.add_argument("--tension-field", choices=["off", "duel", "rank1"], default="off",
                    help="H_9805: 'duel' = the full per-edge L→R/R→L parse-disagreement field, added "
                         "to the embeddings BEFORE the trunk · 'rank1' = THE CONTROL — the same "
                         "reduction fed the best rank-1 approximation of that same field (identical "
                         "params/lam/shape; the ONE variable is field-vs-its-own-scalar-summary) · "
                         "'off' (default) ⇒ byte-identical, no trailer.")
    ap.add_argument("--tension-field-rank", type=int, default=32,
                    help="H_9805: TFLD inner width r for phi (n_bucket, r) and W_up (r, d).")
    ap.add_argument("--tension-field-lam0", type=float, default=1.0,
                    help="H_9805: TFLD lam init (additive pre-trunk scale).")
    ap.add_argument("--recurrent-lane", choices=["off", "gru3-bidir"], default="off",
                    help="H_9954: 'gru3-bidir' = a 3-cell manual GRU reading the embeddings and "
                         "writing a residual at the pre-embed_conv site, co-trained by plain CE. "
                         "CAUSAL. The 3 cells are the IIT-4 nodes read by `anima-py evaluate "
                         "--iit4-recurrent-lane`. 'off' (default) => byte-identical, no trailer. "
                         "Control = --objective ce_marginal_shuffled (H_9960).")
    ap.add_argument("--recurrent-lane-seed", type=int, default=9954,
                    help="H_9954: init seed for the recurrent lane params (arm-invariant).")
    ap.add_argument("--recurrent-lane-freeze-trunk", action="store_true",
                    help="H_9954 growth-fork: freeze the whole trunk (requires_grad=False) and train "
                         "ONLY rln.* — distinct from --freeze-trunk (the CLMS BOLT arm). Cuts trunk "
                         "grads + Adam state so a 303M fork fits a 12GB card; isolates the lane's "
                         "contribution. Needs --recurrent-lane gru3-bidir.")
    ap.add_argument("--trunk-norm", choices=["global", "position"], default="global",
                    help="H_9814: trunk normalization statistics. global = legacy GroupNorm over "
                         "(C,T) — measurably NON-CAUSAL (H_9813: masking input bytes AFTER t moved "
                         "the prediction AT t by 0.5964 nats). position = per-position (causal-safe "
                         "contrast arm). The .clm trailer preserves this forward setting. A .clm "
                         "warm-start must match the source setting; changing it mutates the forward "
                         "pass even under --freeze-trunk and is rejected.")
    ap.add_argument("--serialize-parity", default="",
                    help="H_9813: after writing the .clm, re-score this bind-panel through BOTH "
                         "the trained torch model and the serialized .clm and report agreement. "
                         "The trainer is the only place that holds both ends at once. Comparison "
                         "only — it never says the model is good or bad.")
    ap.add_argument("--parity-items", type=int, default=32,
                    help="H_9821: how many panel items --serialize-parity scores. The scored "
                         "slot count is items x K, and that count IS the measurement's power: "
                         "the default 32 items x K=2 gives n=32, i.e. sd~0.077 at p=0.75 — wide "
                         "enough that a 2-item wobble crosses a 0.75 bar and moves a threshold "
                         "statistic a whole rung (measured, H_9820 -> convergence evaluate-py-24). "
                         "Raising this is the ONLY way to score a panel wider than 32 items, "
                         "since the cap silently truncated them before. Default 32 keeps every "
                         "existing run byte-identical.")
    ap.add_argument("--tension-concord", choices=["class", "lex", "morph"], default="class",
                    help="H_9812: what the TFLD concord term compares. lex = the CHUNK SIGNATURE "
                         "(the field sees WHICH words agree). morph = the chunk's FINAL BYTE, the "
                         "closest analogue of v4's honorific concord and the one English agreement "
                         "morphology actually lives in (verb +s/+ing, noun +s). "
                         "class = byte_class, the LEGACY/CONTROL mode, measured to be a function of "
                         "the whitespace+punct layout ALONE (swap every letter, or letters for "
                         "digits, and the field is BIT-IDENTICAL). Keep `class` as the layout-only "
                         "pedestal arm; do not build a claim on it.")
    ap.add_argument("--answer-ce-weight", type=float, default=0.0,
                    help="H_9811: extra CE weight on the ANSWER span of ` => ` arrow lines "
                         "(loss = obj + w*ce_answer). 0 = OFF, byte-identical to today. The "
                         "answer is ~6%% of a bind-panel line, so a plain next-byte CE leaves "
                         "the binding bit at chance (measured: d_acc 0.5000 on DRILLED lexemes, "
                         "one token emitted 68-86%% of slots, and 5.9x params/6.7x steps made it "
                         "WORSE). v4 H_004's amendment A1 used ce_surf + 5*ce_ans.")
    ap.add_argument("--bind-rank", type=int, default=64, help="H_9698: MBND binder rank (q/k/v/u width)")
    ap.add_argument("--bind-lam0", type=float, default=1.0, help="H_9698: MBND lam init (additive scale)")
    ap.add_argument("--freeze-trunk", action="store_true",
                    help="BOLT control arm: trunk requires_grad=False, only clms.* trains")
    # H_9643 faction lane: split the d channels into K contiguous groups (grouped conv + GN(K) +
    # cross-faction bridge). 0 = OFF, byte-identical to a standard trunk. The real arm trains K=8 vs
    # K=1 FREELY (no forced routing — the ORACLE dose was only the toy's instrument positive control)
    # then reads specialization with `anima-py evaluate --faction-lesion`. d % K must be 0.
    ap.add_argument("--n-factions", type=int, default=0,
                    help="H_9643: K contiguous faction blocks on the d axis (0 = OFF, byte-identical)")
    ap.add_argument("--faction-bridge-lam0", type=float, default=0.1,
                    help="H_9643: initial cross-faction bridge scale (K>0 only)")
    # ── H_9845 INTERVENTIONAL CLOSURE MONITOR (rung 1) · ⛔ MONITOR-ONLY ──────────────────────
    # Default off ⇒ byte-identical golden path. WHY a flag on the trainer and not a script beside
    # it: the question ("is this lane causal or merely correlated?") is only answerable WHILE the
    # weights are live, and `a_experiment_engine_native` says a manipulation is a flag on the
    # installed CLI. WHY it can never become a lever: a_train_inline_gauge — it is read AFTER
    # opt.step() under no_grad on a saved/restored RNG state and only ever printed. The ON-vs-OFF
    # trajectory at a fixed seed is byte-identical, and that is the landing evidence (H_9845).
    ap.add_argument("--closure-monitor", choices=["off", "rung1"], default="off",
                    help="H_9845: 'rung1' logs the interventional closure ladder "
                         "(core/closure_ladder.py) with the LIVE model as the acting policy. "
                         "MONITOR-ONLY — never enters the loss. ⚠️ a thermostat clears rung 1: "
                         "it diagnoses lane causality, NOT aliveness. 'off' (default) ⇒ "
                         "byte-identical.")
    ap.add_argument("--closure-monitor-every", type=int, default=0,
                    help="H_9845: run the monitor every N steps (0 = final step only). Each "
                         "invocation costs ticks x schedules model forwards of batch 8.")
    ap.add_argument("--closure-monitor-ticks", type=int, default=600,
                    help="H_9845: world ticks per schedule. 600 = the rig's MEASURED power floor "
                         "(12 LV-C blocks of 50). Lower is NOT a cheaper reading: at 400 ticks "
                         "the scripted positive control itself stops firing, and the monitor "
                         "then reports UNDER-POWERED rather than a model number.")
    ap.add_argument("--closure-monitor-seed", type=int, default=7,
                    help="H_9845: FIRST perturbation-schedule seed (keys the world's exogenous "
                         "streams, not a sampler).")
    ap.add_argument("--closure-monitor-schedules", type=int, default=2,
                    help="H_9845: how many perturbation SCHEDULES (seed, seed+1, ...) to run. "
                         ">=2 because a deterministic do()-intervention makes a single-schedule "
                         "re-run byte-identical, i.e. vacuous as replication "
                         "(sample-seed-invalid-for-deterministic-do-intervention).")
    ap.add_argument("--closure-monitor-out", type=str, default="",
                    help="H_9845: append each monitor reading to this JSONL (log sink only).")
    # H_9845-B REAL-INPUT SWAP. Motivation = the H_9838 planted-geometry failure: a certified,
    # 3-seed, independently-reproduced positive evaporated (CERTIFIED -> INVALID, zero-truth
    # pedestal 0.3750 > bar 0.3077) the moment its PLANTED integer fixture was replaced by the
    # production trunk's real representations, because the fixture's hand-made near-orthogonal
    # geometry had manufactured the result. H_9845's landed numbers share the defect class: the
    # acting brain was a d32/L2/12-step TOY, and closure_ladder's own header says a thermostat
    # clears rung 1. This flag swaps ONLY that input source. Every bar, control, tick budget and
    # schedule count is untouched — changing one would destroy the very comparison.
    ap.add_argument("--closure-brain", type=str, default="",
                    help="H_9845-B: run the closure monitor with this serialized .clm (e.g. the "
                         "real 303M) as the ACTING POLICY, read via core/decode "
                         "(clm_load_weights + clm_forward_hidden_logits), instead of the "
                         "in-training model. Same 8-action NLL scoring, same tie order, same "
                         "controls/bars/ticks/schedules. '' (default) => the landed path, "
                         "byte-identical. ⚠️ ~0.26 s/forward x 8 per tick on CPU: a 600-tick "
                         "schedule is ~21 min.")

    # ── H_9841 IMAGINATION RECONSOLIDATION (training-time N3/REM rehearsal) ──────────────────
    # The daemon already grows on rehearsal (cli/chat.py:3350-3380 fires a live
    # vadapt_field_step per replay tick); training had no counterpart. That gap is the p8
    # violation this lane closes. DEFAULT OFF (0.0) ⇒ every branch is skipped, byte-identical.
    ap.add_argument("--imagination-replay", type=float, default=0.0,
                    help="H_9841: fraction of the batch a reconsolidation phase may hand to "
                         "REHEARSED windows (0.0 = OFF, byte-identical). The rows actually "
                         "replayed = ir_consolidation_gain x budget, so a rehearsal that grew "
                         "nothing spends nothing.")
    ap.add_argument("--reconsolidate-every", type=int, default=50,
                    help="H_9841: enter the N3/REM reconsolidation phase every N steps "
                         "(inert unless --imagination-replay > 0).")
    ap.add_argument("--vadapt-on-replay", action="store_true",
                    help="H_9841: fire the daemon's OWN growth hook (core/engine_cli "
                         "vadapt_field_step, the call cli/chat.py:3375 makes) once per replay "
                         "tick, so the replay dose follows the growth the rehearsal actually "
                         "CAUSED. OFF = replay happens with the hook lesioned and the dose "
                         "follows the fixed N3 prior dr_mitosis_prior(3)=0.80 — THE control "
                         "that isolates whether the hook is causal, not a weaker treatment.")
    ap.add_argument("--imagination-select", choices=["recency", "random"], default="recency",
                    help="H_9841: snapshot selection. 'recency' = ir_select_snapshots' own "
                         "policy (the daemon's) · 'random' = THE CONTROL, same ring and same "
                         "count with the recency ordering destroyed, isolating whether the "
                         "selection POLICY is causal.")
    ap.add_argument("--imagination-selftest", action="store_true",
                    help="H_9841: run the $0 certification battery for the lane and EXIT — no "
                         "model, no corpus, no GPU. Controls first (planted novel ring must "
                         "FIRE; empty ring and novelty-free ring must REFUSE) across 3 "
                         "geometries x 2 seeds, then the arms. Emits JSON; exit 0 CERTIFIED / "
                         "3 INVALID / 4 INSTRUMENT-DEAD / 5 REAL-UNDERPOWERED.")
    ap.add_argument("--imagination-real-source", type=str, default="",
                    help="H_9841-R: DIRECTORY of a REAL .kosmos anchor store whose payload "
                         "bytes REPLACE the selftest's synthesized ring (selftest-scoped; the "
                         "in-vivo lane's ring is already real — it is the trainer's own "
                         "windows). Motivated by the H_9838 planted-geometry failure: that "
                         "card's positive died when its PLANTED integer codes were swapped for "
                         "real 303M representations and the zero-truth pedestal fired (0.3750 > "
                         "bar 0.3077 at 16 items), because the planted codes were effectively "
                         "orthogonal while real ones overlap 2.2x. This battery's `novel()` ring "
                         "is the same kind of hand-made favourable geometry. Arms, controls, "
                         "bars, thresholds and the seed policy are UNCHANGED — only the ring's "
                         "bytes change. Read via core/kosmos_io.load_anchors (audited, not "
                         "repaired: H_9843 measured that reader lossy). A store that cannot fill "
                         "a geometry yields REAL-UNDERPOWERED with the realized n, never a "
                         "stretched null.")
    ap.add_argument("--seed", type=int, default=7)
    # a `<corpus>.meta.json` written by `anima-py corpus` carries the budget floor that corpus
    # earned; _budget_preflight refuses to start below it (H_9324) — see cli/corpus.py BUDGET_FLOORS.
    ap.add_argument("--corpus", nargs="*", default=[])
    ap.add_argument("--cell-label", nargs="*", default=[])
    ap.add_argument("--canon", action="store_true")
    ap.add_argument("--d", type=int, default=0)
    ap.add_argument("--L", type=int, default=0)
    ap.add_argument("--steps", type=int, default=0)
    ap.add_argument("--seq-len", type=int, default=0)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--lr", type=float, default=3e-4)
    ap.add_argument("--adam-beta2", type=float, default=0.999,
                    help="AdamW beta2 (legacy default 0.999; canonical ByteGPT R0 uses 0.95)")
    ap.add_argument("--weight-decay", type=float, default=0.0,
                    help="base AdamW weight decay (legacy default 0.0)")
    ap.add_argument("--lr-schedule", choices=["constant", "cosine"], default="constant",
                    help="optimizer-step LR schedule; exact-resume derives it from completed step")
    ap.add_argument("--warmup-steps", type=int, default=0,
                    help="linear LR warm-up optimizer steps before constant/cosine schedule")
    ap.add_argument("--lr-decay-steps", type=int, default=0,
                    help="cosine endpoint in optimizer steps (0 resolves to --steps)")
    ap.add_argument("--min-lr-ratio", type=float, default=0.0,
                    help="cosine floor as a fraction of --lr")
    ap.add_argument("--e0", type=int, default=2)
    ap.add_argument("--emax", type=int, default=3)
    ap.add_argument("--no-savant", action="store_true")
    ap.add_argument("--no-mitosis", action="store_true")
    ap.add_argument("--wd-floor", type=float, default=-1.0,
                    help="N6 sweep: override savant wd floor (>=0 forces constant wd)")
    ap.add_argument("--dropout-floor", type=float, default=-1.0,
                    help="N6 sweep: override savant dropout floor (>=0 forces constant dp)")
    ap.add_argument("--bf16", action="store_true")
    ap.add_argument("--sample", choices=["roundrobin", "proportional"], default="proportional")
    # --require-cells N: fail LOUD if the usable register-cell count != N (a_chat_registers
    # overfit guard, parity with cli/train.hexa). Default 0 = off. Prevents silently
    # training on an incomplete 4-cell register (the clm303 ko-SNS starvation overfit).
    ap.add_argument("--require-cells", type=int, default=0)
    ap.add_argument("--validation-corpus", nargs="*", default=[],
                    help="explicit held-out byte file per --corpus cell; overrides --val-frac")
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--dbes-every", type=int, default=0, help="0=final only; N=also every N steps")
    # ── H_9846 STRUCTURE-ENVELOPE WATCH (MONITOR-ONLY · core/phi_envelope_monitor.py) ────────
    # WHY IT EXISTS: a lever that raises a capability number while shredding the substrate's
    # structure is a REGRESSION, and today nothing in the trainer would notice. This watch reads
    # the envelope/structure layer (core/phi_envelope_substrate.py) over the parameter tensors
    # and reports `phi_smooth_no_cliff` — a function whose entire job is "was there a cliff".
    # WHY IT IS A LOG AND NOTHING ELSE (a_train_inline_gauge): a number in the loss stops being
    # evidence about the model — that is p7 (no perplexity verdict) in its Φ edition. Loss-freedom
    # here is STRUCTURAL, not a promise: the tick reads params under no_grad, draws no RNG, and
    # the value never touches `loss`, so ON and OFF produce byte-identical checkpoints (that
    # equality is the proof obligation, measured in the H_9846 card).
    # NAMING (a_phi_iit4_tool): Φ is IIT4-only. Nothing this flag prints is called Φ — the outputs
    # are `dispersion`/`span`/`nest_*`/`cliff_gap`, i.e. what they arithmetically are.
    ap.add_argument("--phi-envelope-monitor", choices=["off", "on"], default="off",
                    help="H_9846: log the parameter-structure envelope (dispersion + cliff) every "
                         "--phi-monitor-every steps. MONITOR-ONLY — never enters the loss; ON vs "
                         "OFF is byte-identical. Runs its positive control + zero-truth pedestal "
                         "FIRST and refuses to report any value unless both certify.")
    ap.add_argument("--phi-monitor-every", type=int, default=0,
                    help="H_9846: monitor cadence in steps (0 = follow --log-every). The cliff "
                         "statistic compares CONSECUTIVE ticks, so it is cadence-dependent by "
                         "construction — compare two runs only at the same value (the shipped "
                         "battery certifies the fire/refuse DECISION across cadences and reports "
                         "the ramp inflation factor rather than pretending the number is scale-free).")
    ap.add_argument("--skip-inline-rho", action="store_true",
                    help="skip the slow directional torch-side rho probe at shutdown; the "
                         "serialized checkpoint must still receive its terminal engine-native "
                         "evaluation")
    ap.add_argument("--ckpt-every", type=int, default=0,
                    help="0=final .clm only; N=every N steps dump <out>.step<N>.clm "
                         "(step-window multiplex — 1 run yields 2000/4000/… checkpoints, "
                         "train-py-4 isolation) AND a rolling <out>.resume.pt containing model, "
                         "optimizer, completed step, and RNG/sampler state. Resume it with "
                         "`--init <out>.resume.pt`; the requested --steps remains the original "
                         "absolute endpoint. Set this on any multi-hour fire (train-py-7).")
    ap.add_argument("--stop-after-ckpt", action="store_true",
                    help="exit cleanly immediately after the first --ckpt-every boundary; used to "
                         "prove process-level recovery without changing the requested endpoint")
    ap.add_argument("--out", default="")
    ap.add_argument("--ckpt-out", default="")
    ap.add_argument("--gauges-out", default="")
    ap.add_argument("--init", default="",
                    help="warm-start ckpt path — load weights into the freshly-built model "
                         "BEFORE training. ByteGPT: an engine `.bin` (5×u32 header) or a `.pt`; "
                         "CLM: a `.pt` torch state_dict OR a **`.clm`** (int4-dequant via "
                         "core/serialize.deserialize_v3, gated on a BYTE-IDENTICAL round-trip — "
                         "so you warm-start from exactly the weights core/decode.py runs, which "
                         "is what makes it valid to resume from a shipped ckpt after the pod and "
                         "its `.pt` are gone). Dim/layer/expert mismatch → hard error (H_247: a "
                         "warm-init shape mismatch can floor +2.5 nats).")
    # ── §7 multi-GPU data-parallel (DDP) launch surface ──────────────────────────
    ap.add_argument("--gpus", default="",
                    help="multi-GPU DATA-PARALLEL (DDP) device ids, e.g. '0,1,2,3' (mirrors "
                         "`anima sweep --gpus`). >1 id => self-re-exec under torchrun, one "
                         "process/GPU. GLOBAL batch is PRESERVED = --batch-size (per-rank "
                         "B/N); LR/schedule/corpus-mix/val-stream/serialize-format UNCHANGED "
                         "vs the 1-GPU recipe (DDP is an execution strategy, not a recipe "
                         "change). --batch-size MUST be divisible by N (hard error otherwise "
                         "— no silent effective-batch change). 0 or 1 id => single-GPU path, "
                         "byte-identical to today (every DDP branch skipped).")
    ap.add_argument("--device", choices=["auto", "cpu", "cuda", "mps"], default="auto",
                    help="training device (default: auto selects CUDA, then Apple MPS, then CPU; "
                         "multi-GPU --gpus always uses CUDA and cannot be combined with an "
                         "explicit non-CUDA device)")
    ap.add_argument("--ddp-verify-sync", action="store_true",
                    help="DDP debug: every --val-every steps all-reduce a param-checksum and "
                         "assert cross-rank agreement (catches a mitosis/optimizer desync at "
                         "the split). Off by default (costs one collective per val).")
    # ── H_9808 TRAINED-CONTROL CEILING — the ABORT-BEFORE-SPEND gate (core/pregates.py) ────────
    # lab/v4 H_007 spent ~7h of GPU on a falsifier that could not return a bit: its pre-registered
    # F1 bar was 0.15, but the compute-matched control measured 0.8073/1.0000 at target scale, so
    # the band above the control was narrower than the bar and Δ≈0 was FORCED whether the mechanism
    # worked or not. Its E-anchor (0.62) had been INHERITED from another experiment's band, and its
    # own d=64 smoke INVERTED at d=384 (+0.073 → −0.010).
    #
    # This gate refuses the run BEFORE any CUDA allocation, data load, or DDP re-exec. It is
    # DEFAULT-OFF (bar 0.0) ⇒ the golden path is byte-identical.
    ap.add_argument("--trained-control-ceiling", type=float, default=0.0,
                    help="H_9808: pre-registered falsifier bar b. When > 0 this ABORTS THE RUN "
                         "BEFORE SPEND unless --control-anchor carries a control MEASURED on THIS "
                         "panel at THIS scale that sits inside (chance+margin, 1−2b]. A saturated "
                         "control (lab/v4 H_007: 0.8073 vs cap 0.70) and a control at chance "
                         "(H_008: 0.5104) are both refusals.")
    ap.add_argument("--control-anchor", type=str, default="",
                    help="H_9808: JSON file with the controls-first reading — {measured:true, "
                         "panel, arm, scale:{d,L,steps}, seeds:{s:score}, source}. REQUIRED when "
                         "--trained-control-ceiling > 0. An anchor whose panel or scale differs "
                         "from this run's is INHERITED and refused (no exceptions, no override).")
    ap.add_argument("--pregate-panel", type=str, default="",
                    help="H_9808: the panel identifier this run will be scored on. Must equal the "
                         "anchor's panel. REQUIRED when --trained-control-ceiling > 0.")
    # ── H_9840 SLEEP-SCHEDULE curriculum (SLP lane · see the SleepSchedule docstring) ──────────
    # The 5-stage session in core/dream_lib.py had no consumer on the training side; this makes it
    # one. DEFAULT-OFF ⇒ the golden path never constructs a schedule and is byte-identical.
    ap.add_argument("--sleep-schedule", choices=["off", "dream-lib", "fixed-alternating"],
                    default="off",
                    help="H_9840: 'dream-lib' = core/dream_lib.py's own 5-stage session drives the "
                         "per-step wake/sleep phase (one long WAKE bout, then a consolidated "
                         "N1→N2→N3→REM bout); a SLEEP step rehearses windows already consumed "
                         "while awake instead of drawing fresh corpus · 'fixed-alternating' = THE "
                         "CONTROL, the SAME stage multiset (identical ratio AND per-stage counts, "
                         "it is a permutation) spread evenly, so the ONE variable is the temporal "
                         "ARRANGEMENT · 'off' (default) ⇒ byte-identical, no replay buffer. "
                         "SUBORDINATE TO H_9833: without a consolidation objective a sleep step is "
                         "resampling, not consolidation — do not read a gain here as one.")
    ap.add_argument("--sleep-ticks", type=int, default=DR.dr_n_ticks(),
                    help="H_9840: session length in training steps (default 90 = dream_lib's "
                         "native session, i.e. the identity rescale of its stage table).")
    ap.add_argument("--sleep-replay-cap", type=int, default=4096,
                    help="H_9840: FIFO capacity of the wake replay buffer, in window specs.")
    ap.add_argument("--sleep-selftest", type=int, default=0,
                    help="H_9840 $0 SELFTEST: build N steps of every arm, run the meter controls "
                         "(planted bout must FIRE, all-wake pedestal must REFUSE) and the arm "
                         "gates (arms differ · stage multisets identical) across a --sleep-ticks "
                         "sweep, print the realized sequences as JSON and EXIT — no model, no "
                         "corpus, no device. Non-zero exit if the battery does not certify.")
    # ── H_9843 .kosmos STORE CARRY (the H_9838 supply line · core/kosmos_carry.py) ──────────────
    # H_9838 builds its CA3 store INSIDE one training run. If the .kosmos anchor store does not
    # survive between runs, that store can never ACCUMULATE — it is rebuilt from zero every time.
    # These flags carry a store across runs and CERTIFY the carry before any spend.
    #
    # ⚠ NOT an identity lever. `a_kosmos` reads .kosmos as identity persistence; H_9789 measured
    # the self-anchor VOID. Nothing here reads on identity — this is DATA plumbing only.
    # ⚠ SEQUENCING: meaningful only AFTER H_9838 is positive. There is no consumer of a carried
    # store in the loop below today, so a certified carry is an ADMISSIBILITY statement about the
    # format, never a capability result. Default off ⇒ the golden path is byte-identical.
    ap.add_argument("--kosmos-carry", type=str, default="",
                    help="H_9843: DIRECTORY holding the .kosmos anchor store to carry into this "
                         "run (core/kosmos_io.load_anchors takes a dir_path — a store is a "
                         "directory of anchors, not one file). Certified before any spend.")
    ap.add_argument("--kosmos-carry-mode", choices=["ro", "append"], default="ro",
                    help="H_9843: 'ro' (default) reads the store and touches nothing. 'append' "
                         "additionally writes ONE run-provenance anchor so the store ACCUMULATES "
                         "one record per run; pre-existing files are never rewritten (the reader "
                         "is NOT the writer's inverse — see --kosmos-carry-audit).")
    ap.add_argument("--kosmos-carry-audit", action="store_true",
                    help="H_9843: run the carry preflight, print the JSON report and EXIT before "
                         "any model/CUDA/corpus work ($0, no ckpt). Controls run FIRST (planted "
                         "pairing must FIRE, structure-free + shuffled pedestals must REFUSE) and "
                         "the store row is withheld unless both certify.")
    ap.add_argument("--kosmos-carry-out", type=str, default="",
                    help="H_9843: also write the carry report JSON here.")
    ap.add_argument("--field-loop", action="store_true", dest="field_loop",
                    help="H_9957 FIELD-LOOP: closed text<->PureField re-entry co-training (the "
                         "train-time replacement for GRAFT). Reuses the loaded/built model + a "
                         "contiguous-stream loop with per-row field carry + write-back. v1 CLM-only, "
                         "single-process.")
    ap.add_argument("--field-arm", choices=["off", "purefield16", "purefield16-yoked",
                                            "integrator16", "integrator16-yoked",
                                            "gru16-frozen", "gru16-frozen-yoked",
                                            "coupled", "coupled-yoked"],
                    default="purefield16", dest="field_arm",
                    help="field-loop arm: off (no residual = ignore + fluency baseline) · purefield16 "
                         "(live loop) · purefield16-yoked (A/G deranged across rows = fancy-seed control) · "
                         "integrator16[-yoked] (H_9957 sibling: read the shared H_9607 integral I through "
                         "fixed random features, no PureField cell — is the channel just the scalar integrator?)")
    ap.add_argument("--field-write", choices=["scalar", "vector"], default="scalar", dest="field_write",
                    help="H_9957 coupled arm: scalar (legacy mode-0 mean-CE write) or vector (first "
                         "--field-cells DCT modes of the per-byte A-G tension profile). Only the coupled arm.")
    ap.add_argument("--field-cells", type=int, default=1, dest="field_cells",
                    help="H_9957 coupled arm: m coupled leaky cells (fixed weak rotation coupling). "
                         "The state faithful IIT-4 reads for the Φ-under-monopoly question; m=1 = the "
                         "scalar integral (Φ undefined).")
    ap.add_argument("--field-block", type=int, default=256, dest="field_block",
                    help="contiguous block length (bytes) per field-loop step")
    ap.add_argument("--field-b", type=int, default=8, dest="field_b",
                    help="parallel contiguous document streams (batch rows) for field-loop")
    ap.add_argument("--field-loop-eval", type=str, default="", dest="field_loop_eval",
                    help="measure a trained coupling instead of training: load this .fl.pt, grow K "
                         "per-doc fields on --corpus, print Delta_collapse = aligned - yoked (own-field "
                         "vs wrong-field own-byte prediction) + the sever control. No training.")
    ap.add_argument("--field-doc-len", type=int, default=0, dest="field_doc_len",
                    help="H_9957 fieldctl: DOC-AWARE field-loop — reset the field at every planted doc "
                         "boundary of this byte length (blocks align to the doc grid), so the leaky "
                         "integral carries ONE doc's key not a ~400-block blur. 0 = legacy random-start "
                         "contiguous stream (natural-corpus path). = the doc_len printed by `corpus fieldctl`.")
    ap.add_argument("--score-mask", type=str, default="", dest="score_mask",
                    help="H_9957 fieldctl: with --field-loop-eval, score the payload-byte Delta_collapse "
                         "using this fieldctl .mask.json (doc geometry + scored-byte position) on the val "
                         "--corpus, instead of the whole-block DV. The instrument-check DV.")
    ap.add_argument("--field-phi", action="store_true", dest="field_phi",
                    help="H_9957 MISSION DV (coupled arm): with --field-loop-eval + --score-mask, read "
                         "faithful IIT-4 Φ collapse-Δ of the CE-earned m-cell state (Φ_aligned vs shuffle "
                         "pedestal + time-yoked) — does necessity force integration under monopoly carriage?")
    ap.add_argument("--field-bptt", type=int, default=0, dest="field_bptt",
                    help="H_9976 DWB-fork: make the WRITE-BACK differentiable and keep the state graph "
                         "for K blocks (window-truncated BPTT). 0 = legacy gradient-free write-back "
                         "(byte-identical). Engine G stays detached either way — only the write-back "
                         "becomes differentiable. Verdicts from K>0 are a DIFFERENT substrate "
                         "(substrate: DWB-fork · NON-ANIMA) and cannot touch the five-lever law.")
    ap.add_argument("--field-sg-drive", action="store_true", dest="field_sg_drive",
                    help="H_9976 CONTROL for --field-bptt: detach the CE at the drive, i.e. run the "
                         "identical loop with today's gradient-free write-back. full-vs-sg isolates "
                         "the lever; Phi_full ~ Phi_sg means differentiability added nothing.")
    ap.add_argument("--field-train-physics", action="store_true", dest="field_train_physics",
                    help="H_9976 A2 arm: also learn the cell physics (R, lam) under a spectral clamp. "
                         "Default OFF — the primary question is whether a gradient THROUGH the loop "
                         "earns integration, not whether the dynamics can be fitted.")
    ap.add_argument("--field-mech", choices=["affine", "gated"], default="affine",
                    dest="field_mech",
                    help="H_9981 (R11): the cell-to-cell MECHANISM CLASS. 'affine' = today's "
                         "I'=I(1-lam)R^T+s (every closed lever left this fixed; A2 freed the "
                         "coefficients on it and Phi did not move). 'gated' adds a LEARNED "
                         "multiplicative term beta*((I@Ra^T)*(I@Rb^T)) initialised at 0, so init is "
                         "byte-identical and CE gets to CHOOSE non-separability rather than be forced "
                         "into it. Rationale: the repo's own hand-TPM reading puts XOR (linearly "
                         "non-separable) at Phi 2.2500 vs OR/AND 0.5825 vs a COPY pedestal of exactly "
                         "0. beta joins the optimizer in BOTH arms so parameter counts match (D4).")
    ap.add_argument("--field-mech-lam0", type=float, default=0.0, dest="field_mech_lam0",
                    help="H_9981: beta init (default 0.0 = byte-identical null). Non-zero only for "
                         "the instrument checks; a training arm must start at 0 or the mechanism is "
                         "imposed rather than chosen.")
    ap.add_argument("--field-coupling-seed", type=int, default=-1, dest="field_coupling_seed",
                    help="H_9957: seed for the FIXED architecture draw (the coupled cells' rotation R, "
                         "frozen features) — kept DISJOINT from --seed (the training draw). Default -1 = "
                         "legacy single-stream behaviour (byte-identical). Hold it CONSTANT across a seed "
                         "sweep so an architecture draw cannot masquerade as learned integration.")
    ap.add_argument("--field-phi-boot", type=int, default=0, dest="field_phi_boot",
                    help="H_9957 POWER for the negative: moving-block bootstrap replicates (e.g. 200) over "
                         "the collected state -> mean/sd/90%% CI on Δφ. Needed because the doc-aware readout "
                         "is DETERMINISTIC (--seed does not resample it), so a negative Δφ has no sampling "
                         "spread without this (power-before-negative-verdict · negative-claims-need-tost).")
    ap.add_argument("--ddp-find-unused", action="store_true",
                    help="DDP debug/escape-hatch: pass find_unused_parameters=True to DDP. Off "
                         "by default — the current objective set fires every head every step "
                         "(§4). Flip ON only if a FUTURE per-step-gated head makes DDP error on "
                         "an unused param.")
    a = ap.parse_args()

    if not (0.0 <= a.adam_beta2 < 1.0):
        ap.error("--adam-beta2 must be in [0, 1)")
    if a.weight_decay < 0.0:
        ap.error("--weight-decay must be >= 0")
    if a.warmup_steps < 0 or a.lr_decay_steps < 0:
        ap.error("--warmup-steps and --lr-decay-steps must be >= 0")
    if not (0.0 <= a.min_lr_ratio <= 1.0):
        ap.error("--min-lr-ratio must be in [0, 1]")

    if a.store_source:                     # V6_36 SRC head training (frozen trunk) — dispatch first
        return _store_source_train(a)

    # ══ H_9840 — SLEEP-SCHEDULE $0 SELFTEST ═════════════════════════════════════════════════════
    # Runs FIRST, like the H_9808 gate below: before the DDP re-exec, before any device, corpus or
    # model. The schedule is pure integer arithmetic over core/dream_lib.py, so certifying it must
    # not cost a GPU-second — and an instrument that has never been run hides several bugs at once
    # (convergence instrument-never-run-hides-multiple-bugs).
    if a.sleep_selftest > 0:
        sys.exit(run_sleep_selftest(a.sleep_ticks, a.sleep_selftest))

    # ══ H_9841 — IMAGINATION-LANE SELFTEST: runs BEFORE any spend and EXITS ══════════════════════
    #   Placed here (like the H_9808 gate below) so it needs no corpus, no CUDA, no DDP re-exec
    #   and no checkpoint — the whole battery is $0. `a_experiment_engine_native`: the certification
    #   of a manipulation is itself a flag on the installed CLI, never a script beside the engine.
    if a.imagination_selftest:
        run_imagination_selftest(a.imagination_replay, a.reconsolidate_every,
                                 a.vadapt_on_replay, a.imagination_select, a.seed,
                                 a.imagination_real_source)

    # ══ H_9841 — DOSE-FLOOR REFUSAL (no-tune-to-green, abort before spend) ═══════════════════════
    #   The replay dose is round(ir_consolidation_gain * budget) ROWS, so below a derived budget
    #   floor it is 0 at every possible density: the lane would log "ON" and train nothing. That
    #   is a knob silently deciding the outcome, so it is refused rather than tuned around. The
    #   floor comes from the engine's own gain function (_imag_dose_floor), never a chosen number.
    if a.imagination_replay > 0.0:
        _iw = max(1, len([g for g in a.gpus.split(",") if g.strip() != ""]))
        _ibudget = max(1, int(round(a.imagination_replay * (a.batch_size // _iw))))
        _ifloor = _imag_dose_floor()
        if _ibudget < _ifloor:
            sys.exit("[imagination] REFUSING TO START — --imagination-replay %g on a per-rank "
                     "batch of %d gives a replay budget of %d row(s), below the derived dose "
                     "floor of %d. round(ir_consolidation_gain(n,density)*n) == 0 for every "
                     "density at n < %d, so the lane would report itself ON and replay NOTHING. "
                     "Raise --imagination-replay or --batch-size."
                     % (a.imagination_replay, a.batch_size // _iw, _ibudget, _ifloor, _ifloor))

    # ══ H_9808 — TRAINED-CONTROL CEILING: the ABORT-BEFORE-SPEND gate ═══════════════════════════
    #
    # Runs FIRST — before the DDP re-exec, before any CUDA allocation, before a single corpus byte
    # is read. That placement is the whole point: lab/v4 H_007 discovered its falsifier was
    # inadmissible AFTER ~7h of GPU, from the collected verdict. This refuses at t=0.
    #
    # DEFAULT-OFF: --trained-control-ceiling 0.0 (the default) skips every line below, so the
    # golden path is byte-identical.
    #
    # What makes it able to REFUSE (all four demonstrated in the H_9808 toy e2e):
    #   SATURATED      control > 1 − 2×bar          (H_007 C-scaf 0.8073 vs cap 0.70)
    #   DEAD-CONTROL   control < chance + margin    (H_008 G-1.5a C-dup 0.5104)
    #   SCALE-MISMATCH anchor measured at another scale  (H_007's d=64 smoke for a d=384 run)
    #   PANEL-MISMATCH / NOT-MEASURED  an inherited or estimated anchor (H_007's E[C-dup]=0.62)
    if a.trained_control_ceiling > 0.0:
        import json as _json
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "core"))
        import pregates as _pg

        def _refuse(msg):
            print("=" * 78)
            print("H_9808 GATE — TRAINED-CONTROL CEILING (abort-before-spend · lab/v4 H_007)")
            print("=" * 78)
            print("\n  ⛔ GATE REFUSE — NOT STARTING THIS RUN. " + msg)
            print("\nVERDICT: REFUSE")
            sys.exit(_pg.REFUSE)

        if not a.control_anchor:
            _refuse("--trained-control-ceiling %.4f was passed without --control-anchor. The bar "
                    "cannot be certified against a control that was never measured — that is "
                    "exactly H_007's failure (its anchor was an inherited guess)."
                    % a.trained_control_ceiling)
        if not a.pregate_panel:
            _refuse("--trained-control-ceiling requires --pregate-panel <id>: the gate must know "
                    "which panel this run will be scored on in order to refuse an anchor measured "
                    "on a different one.")
        # The target scale must be EXPLICIT. A recipe default resolved downstream cannot be
        # compared against the anchor here, and 'it probably matched' is how H_007's d=64 smoke
        # became a d=384 anchor.
        _missing = [n for n, v in (("--d", a.d), ("--L", a.L), ("--steps", a.steps)) if not v]
        if _missing:
            _refuse("--trained-control-ceiling requires an EXPLICIT target scale; %s left at the "
                    "recipe default. The gate certifies that the control was measured at THIS "
                    "scale, and it cannot do that against a scale it has to guess (H_007: a d=64 "
                    "smoke read +0.073 and INVERTED to −0.010 at d=384)." % ", ".join(_missing))
        try:
            with open(a.control_anchor, "r", encoding="utf-8") as _f:
                _anchor = _json.load(_f)
        except Exception as _e:
            _refuse("cannot read --control-anchor %r — %s  (a missing anchor is a refusal, never "
                    "a pass)" % (a.control_anchor, _e))
        _scale = {"arch": a.arch, "d": a.d, "L": a.L, "steps": a.steps,
                  "seq_len": a.seq_len, "batch_size": a.batch_size}
        try:
            _res = _pg.trained_control_gate(a.trained_control_ceiling, _anchor,
                                            a.pregate_panel, _scale)
        except _pg.GateError as _e:
            _refuse(str(_e))
        _notes = ["bar b        = %.4f   ⇒ control must sit in (%.4f, %.4f]"
                  % (a.trained_control_ceiling,
                     _pg.CHANCE_DEFAULT + _pg.CONTROL_FLOOR_MARGIN,
                     1.0 - 2.0 * a.trained_control_ceiling),
                  "panel        = %s" % a.pregate_panel,
                  "this run     = %s" % _json.dumps(_scale, sort_keys=True),
                  "anchor arm   = %s   src: %s"
                  % (_anchor.get("arm"), _anchor.get("source")),
                  "anchor scale = %s" % _json.dumps(_anchor.get("scale"), sort_keys=True),
                  ""]
        for _r in _res["per_seed"]:
            _notes.append("  seed %-6s control=%.4f  cap=%.4f  floor=%.4f  headroom=%.4f "
                          "(need %.4f)" % (_r["seed"], _r["control"], _r["cap"], _r["floor"],
                                           _r["headroom"], _r["headroom_required"]))
        _rc = _pg.render(
            "H_9808 GATE — TRAINED-CONTROL CEILING (abort-before-spend · lab/v4 H_007)",
            _res, _notes)
        if _rc != _pg.PASS:
            print("\n  NOT STARTING THIS RUN. Re-run the compute-matched control alone at target "
                  "scale and re-freeze the bar against what it actually measures.")
            sys.exit(_rc)
        print("\n  (gate PASS is an ADMISSIBILITY statement only — it does not predict the run "
              "will be green, and it is not a result.)\n")

    # ══ H_9843 — .kosmos STORE CARRY preflight (the H_9838 supply line) ═════════════════════════
    #
    # Placed next to the H_9808 gate and for the same reason: before the DDP re-exec, before any
    # CUDA allocation, before a corpus byte is read. A store that cannot be carried intact makes
    # every downstream use of it undecidable, and that is knowable at t=0 for $0.
    #
    # ORDER IS FROZEN inside core/kosmos_carry.py: ① the shipped controls (a planted key→value
    # pairing that MUST be retrieved; a structure-free store and a SHUFFLED pairing that MUST NOT
    # be) ② the format-fidelity diff ③ the carried store's own readout + its shuffle control
    # ④ the append write, never before the measurement. The geometry sweep is INTERNAL and frozen
    # (4 (dim, seed) cells, certify-at-all, headline = the minimum) so no CLI knob can move a
    # verdict — the defect H_9844 self-caught when over_floor flipped sign with the block size.
    if a.kosmos_carry:
        import json as _kjson
        sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
            os.path.abspath(__file__))), "core"))
        import kosmos_carry as _kc

        # The fingerprint identifies THIS run (pid + wall clock), so two runs of the same
        # command append two distinct provenance anchors instead of overwriting one.
        _fp = "run pid=%d at=%s | argv=%s | store=%s | mode=%s | steps=%s | seed=%s" % (
            os.getpid(), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            " ".join(sys.argv[1:]), a.kosmos_carry, a.kosmos_carry_mode, a.steps, a.seed)
        # Scratch dir for the re-emit diff. Keyed by the STORE (not the pid) so repeated runs
        # reuse one directory instead of leaving a new one behind every time, and so the
        # byte-diff behind the fidelity numbers stays inspectable (a_all_paths_no_leak).
        _scratch = os.path.join(
            os.environ.get("TMPDIR", "/tmp"),
            "anima_kosmos_carry_reemit_" + _kc.store_key(a.kosmos_carry))
        _rep = _kc.carry_preflight(a.kosmos_carry, a.kosmos_carry_mode, _fp, _scratch)
        print("=" * 78)
        print("H_9843 — .kosmos STORE CARRY preflight (supply line for H_9838 · NOT identity)")
        print("=" * 78)
        print(_kjson.dumps(_rep, ensure_ascii=False, indent=2))
        if a.kosmos_carry_out:
            with open(a.kosmos_carry_out, "w", encoding="utf-8") as _f:
                _f.write(_kjson.dumps(_rep, ensure_ascii=False, indent=2) + "\n")
        _ok = _rep.get("status") in ("CERTIFIED", "CERTIFIED-COPY-ONLY")
        print("\nVERDICT: " + str(_rep.get("status")) + " — " + str(_rep.get("why", "")))
        if not _ok:
            print("\n  NOT STARTING THIS RUN — an uncertified carry makes every downstream use of "
                  "this store undecidable.")
            sys.exit(_kc.REFUSE)
        # The carried store is certified but has NO consumer in the loop below: H_9838's CA3 lane
        # is not landed. Say so out loud rather than implying a wire that does not exist.
        print("  (certified ≠ consumed: no training-loop reader of a carried store exists until "
              "H_9838 lands. This preflight certifies the FORMAT, not a capability.)")
        if a.kosmos_carry_audit:
            sys.exit(_kc.PASS)

    # ══ §7 DDP launch: torchrun self-re-exec + worker init + N==1 short-circuit ══
    #   Runs FIRST (before any CUDA allocation). os.execvpe replaces the process, so the
    #   launcher's `> rf 2>&1` redirect is inherited and only rank 0 prints via p0().
    gpu_ids = [g for g in a.gpus.split(",") if g.strip() != ""]
    if gpu_ids and a.device not in ("auto", "cuda"):
        sys.exit(f"[device] --gpus requires CUDA; it cannot be combined with --device {a.device}")
    under_torchrun = "RANK" in os.environ
    # (1) RE-EXEC branch — >1 GPU requested and not yet under torchrun.
    if len(gpu_ids) > 1 and not under_torchrun:
        if not torch.cuda.is_available():
            sys.exit(f"[ddp] --gpus {a.gpus} requests {len(gpu_ids)}-way DDP but CUDA is not "
                     f"available on this host. Multi-GPU DDP requires CUDA (NCCL backend); a "
                     f"CPU-only run must use a single device (--gpus <one> or omit).")
        if torch.cuda.device_count() < len(gpu_ids):
            sys.exit(f"[ddp] --gpus {a.gpus} requests {len(gpu_ids)} devices but only "
                     f"{torch.cuda.device_count()} CUDA device(s) present.")
        if a.batch_size % len(gpu_ids) != 0:
            sys.exit(f"[ddp] --batch-size {a.batch_size} is not divisible by --gpus N="
                     f"{len(gpu_ids)} (global batch is preserved as per-rank B/N; adjust "
                     f"--batch-size or --gpus). Refusing to pad — silent effective-batch "
                     f"change would corrupt the frozen-recipe comparison.")
        _env = dict(os.environ)
        _env["CUDA_VISIBLE_DEVICES"] = ",".join(gpu_ids)
        os.execvpe("torchrun",
                   ["torchrun", "--standalone", f"--nproc_per_node={len(gpu_ids)}",
                    os.path.abspath(__file__), *sys.argv[1:]], _env)
    # (3)/(4) WORKER init vs N==1 short-circuit.
    ddp_on = False
    rank, world, local_rank = 0, 1, 0
    if under_torchrun and int(os.environ.get("WORLD_SIZE", "1")) > 1:
        local_rank = int(os.environ["LOCAL_RANK"])
        rank = int(os.environ["RANK"])
        world = int(os.environ["WORLD_SIZE"])
        if a.batch_size % world != 0:
            sys.exit(f"[ddp] --batch-size {a.batch_size} not divisible by world_size {world}.")
        torch.cuda.set_device(local_rank)
        dist.init_process_group("nccl")
        ddp_on = True

    def p0(*args, **kwargs):
        """rank-0 print gate — every info/log print routes through this so an N-GPU run
        does not N-duplicate stdout (§7.3). N==1: rank==0, so p0 == print."""
        if rank == 0:
            print(*args, **kwargs)

    is_bytegpt = (a.arch == "bytegpt")
    tlora_on, dict_on, jamo_on = ARMS[a.arm]
    jamo_on = jamo_on or bool(getattr(a, "jamo_aux", False))  # H_9643: --jamo-aux forces it on
    savant_on = not a.no_savant
    mitosis_on = not a.no_mitosis
    # ── ByteGPT: the CLM-specific levers (savant/mitosis/tlora/dict/jamo) are gated OFF.
    #    ByteGPT is a plain transformer (no MoE experts to split, no ConvExpert weight to
    #    TLoRA-reparameterize); the ρ·weave (former G1) lever test it enables is arm=ctrl × the objective
    #    matrix (the arch-agnostic trunk-objective losses). Only n_head is bytegpt-only.
    bg_n_head = 0
    if is_bytegpt:
        if a.arm != "ctrl":
            p0(f"  [bytegpt] arm={a.arm} is CLM-specific → forcing arm=ctrl "
               f"(tlora/dict/jamo are ConvMoE-only)", flush=True)
        tlora_on = dict_on = jamo_on = False
        if savant_on or mitosis_on:
            p0("  [bytegpt] savant/mitosis are CLM-MoE-specific → gated OFF for bytegpt",
               flush=True)
        savant_on = False
        mitosis_on = False
    if a.canon:
        if is_bytegpt:
            d = a.d or 768; L = a.L or 24
            seq_len = a.seq_len or 1024; steps = a.steps or 2000
            # head_dim=64 invariant: n_head = d//64 (d=768→12, d=1024→16). A hardcoded
            # 12 broke warm-FT of the production d=1024 h1129 base (1024%12≠0 → "embed_dim
            # must be divisible by num_heads"; also mismatched h1129's n_head=16 state_dict).
            bg_n_head = max(1, d // 64)
        else:
            d = a.d or 3784; L = a.L or 4
            seq_len = a.seq_len or 1024; steps = a.steps or 2000
    else:
        if is_bytegpt:
            d = a.d or 64; L = a.L or 2
            seq_len = a.seq_len or 128; steps = a.steps or 60
            bg_n_head = 2
        else:
            d = a.d or 64; L = a.L or 2
            seq_len = a.seq_len or 128; steps = a.steps or 60
    e0, emax = a.e0, a.emax
    lr_decay_steps = a.lr_decay_steps or steps
    if a.warmup_steps > lr_decay_steps:
        sys.exit("--warmup-steps cannot exceed the resolved --lr-decay-steps")
    if a.lr_schedule == "cosine" and lr_decay_steps <= a.warmup_steps:
        sys.exit("--lr-schedule cosine requires decay steps greater than warm-up steps")
    V, K = 256, 3
    # §7 device: under DDP each rank pins its own cuda:local_rank; N==1 = today's path.
    if ddp_on:
        device = f"cuda:{local_rank}"
    elif a.device == "auto":
        if torch.cuda.is_available():
            device = "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            device = "mps"
        else:
            device = "cpu"
    else:
        device = a.device
        if device == "cuda" and not torch.cuda.is_available():
            sys.exit("[device] --device cuda requested but CUDA is unavailable")
        if device == "mps" and not (hasattr(torch.backends, "mps") and
                                    torch.backends.mps.is_available()):
            sys.exit("[device] --device mps requested but Apple MPS is unavailable")
    if str(device).startswith("mps") and os.environ.get("ANIMA_MPS_DROPOUT_SHIM", "1") != "0":
        # Apple-MPS graph-cache leak workaround (per-step SAVANT dropout p) — installed
        # ONLY on MPS so CPU/CUDA numerics stay byte-identical. See _install_mps_dropout_shim.
        # (env toggle exists only to A/B the leak; default ON.)
        _install_mps_dropout_shim()
    _gpu_preflight(device, a.steps or 0)
    _budget_preflight(a.corpus, a.steps or 0, a.lr)
    objfn = OBJECTIVE_BUILDERS[a.objective](d, V, device)   # aux-head objectives allocate params
    obj_is_module = isinstance(objfn, nn.Module)
    obj_needs_pen = a.objective in OBJ_NEEDS_PENULTIMATE

    p0(f"=== anima-py train (canonical) arch={a.arch} arm={a.arm} obj={a.objective} seed={a.seed} ===", flush=True)
    if ddp_on:
        # §10.2 — prove the GLOBAL batch in the run record (global batch preserved, per-rank B/N).
        p0(f"  [ddp] world_size={world} global_batch={a.batch_size} per_rank_batch="
           f"{a.batch_size // world} LR/schedule/corpus/val UNCHANGED vs 1-GPU", flush=True)
    if is_bytegpt:
        p0(f"  levers: bytegpt trunk (CLM-specific tlora/dict/jamo/savant/mitosis OFF) "
           f"n_head={bg_n_head} block={seq_len}", flush=True)
    else:
        p0(f"  levers: tlora={tlora_on}(rank={a.tlora_rank},base={not a.tlora_no_base}) "
           f"dict_aux={dict_on}(λ={a.dict_lambda}) jamo_aux={jamo_on}(λ={a.jamo_lambda})", flush=True)
    p0(f"  device={device} d={d} L={L} E0={e0} Emax={emax} seq_len={seq_len} "
       f"steps={steps} bs={a.batch_size} sample={a.sample}", flush=True)
    if str(device).startswith("cuda"):
        cap = torch.cuda.get_device_capability(local_rank)
        p0(f"  cuda: {torch.cuda.get_device_name(local_rank)} cap={cap[0]}.{cap[1]} torch={torch.__version__}", flush=True)
        # PREFLIGHT (pod-bootstrap-gpu-2): a torch wheel with no kernels for THIS GPU's SM crashes
        # LATER, mid-training, with a cryptic async "CUDA error: no kernel image is available for
        # execution on the device" — the same failure-that-looks-like-success class the pod bootstrap
        # ledger fights. Fail fast HERE with the actionable fix. Blackwell (sm_120 / RTX 50xx) needs a
        # cu128 wheel; the default-index torch tops out at sm_90, so it JITs nothing and dies.
        sm = cap[0] * 10 + cap[1]
        arch_nums = []
        for at in torch.cuda.get_arch_list():          # e.g. ['sm_80', 'sm_90', 'sm_90a', 'sm_120']
            m = re.match(r"sm_(\d+)", at)
            if m:
                arch_nums.append(int(m.group(1)))
        if arch_nums and sm > max(arch_nums):
            newest = max(arch_nums)
            raise SystemExit(
                f"FATAL: installed torch {torch.__version__} has NO compiled kernels for this GPU "
                f"(sm_{sm}); it was built for up to sm_{newest}. Training would crash later with "
                f"'CUDA error: no kernel image is available for execution on the device'. "
                f"Install an sm_{sm}-capable build — for Blackwell (sm_120) use the cu128 index:\n"
                f"  pip install --upgrade torch --index-url https://download.pytorch.org/whl/cu128"
            )
    elif device == "mps":
        p0(f"  mps: Apple Metal backend torch={torch.__version__}", flush=True)

    torch.manual_seed(a.seed)
    # Exact process recovery includes Python's global RNG alongside Torch/CUDA and the named
    # samplers. Seed it canonically even when today's active recipe uses only dedicated Random
    # instances; otherwise two fresh processes begin with unrelated OS-derived Python states.
    random.seed(a.seed)

    if is_bytegpt:
        # ByteGPT block = the context window; use seq_len as the positional block size so a
        # non-canon toy stays small. n_head must divide d (validated by the config).
        bg_block = seq_len
        bg_cfg = ByteGPTConfig(vocab=V, d=d, n_layer=L, n_head=bg_n_head, block=bg_block)
        model = _to_device_or_die(ByteGPT(bg_cfg), device)
        cfg = None
        jamo_head = None
        mito = None                                 # no MoE experts to grow
    else:
        # H_9720-ⓐ --store-query-src 'fresh:K[@L]' → fresh_k/fresh_L (default 'penult' ⇒ 0 ⇒ byte-identical)
        # H_9720 C1: '@penult' ⇒ fresh_L=0 = the fresh head reads the SAME penult (pen_trunk) legacy's W_q
        # reads (only tap LOCATION differs from @3) — param-matched-penult control (capacity vs depth).
        _fresh_k, _fresh_L = 0, 3
        _sqs = str(getattr(a, "store_query_src", "penult") or "penult")
        if _sqs.startswith("fresh:"):
            _spec = _sqs[len("fresh:"):]
            _kpart, _, _lpart = _spec.partition("@")
            _fresh_k = int(_kpart)
            if _lpart:
                _fresh_L = 0 if _lpart.strip().lower() == "penult" else int(_lpart)
        cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                        variant="AB", dilation_base=2, max_dilation=512,
                        slw=a.slw, slw_n_slot=a.slw_n_slot, slw_k=a.slw_k,
                        clms=bool(a.store_bridge or a.freeze_trunk),
                        clms_n_slot=a.clms_n_slot, clms_d_k=a.clms_d_k,
                        clms_d_s=a.clms_d_s, clms_r=a.clms_r, clms_d_g=a.clms_d_g, clms_val_center=a.store_val_center, clms_fangate=a.store_fangate, clms_key_fn=a.clms_key_fn, clms_vonly=a.clms_vonly, clms_dual=a.clms_dual,
                        clms_fresh_k=_fresh_k, clms_fresh_L=_fresh_L,
                        clms_key_seed=a.clms_key_seed, clms_lam0=a.clms_lam0,
                        mbnd=bool(a.mouth_binder), mbnd_rank=a.bind_rank,
                        mbnd_linear=(a.mouth_binder == "linear"), mbnd_lam0=a.bind_lam0,
                        tfld_arm=("" if a.tension_field == "off" else a.tension_field),
                        tfld_rank=a.tension_field_rank, tfld_lam0=a.tension_field_lam0,
                        tfld_concord=a.tension_concord,
                        recurrent_lane=("" if getattr(a, "recurrent_lane", "off") == "off" else a.recurrent_lane),
                        recurrent_lane_seed=int(getattr(a, "recurrent_lane_seed", 9954)),
                        trunk_norm=a.trunk_norm,
                        n_factions=a.n_factions, faction_bridge_lam0=a.faction_bridge_lam0)
        model = _to_device_or_die(CLMConvMoE(cfg), device)   # production additive readout (all arms)
        if tlora_on:
            install_tlora_experts(model, a.tlora_rank, base=not a.tlora_no_base)
            model.to(device)
        jamo_head = JamoHead(d).to(device) if jamo_on else None
    n_params = sum(p.numel() for p in model.parameters())
    p0(f"  params: {n_params} ({n_params/1e6:.3f}M)"
       f"{' (+jamo head)' if jamo_on else ''}", flush=True)

    if not is_bytegpt:
        mito = MitosisMoE(model, e0, emax)
        install_router_mask(model, mito)

    # ── warm-start (`--init`): load a base ckpt into the freshly-built model. Done AFTER
    #    the full architecture is built (tlora/mitosis installed) so state_dict keys line up;
    #    strict=False tolerates lever-only keys (tlora/mito) absent from a plain-trunk base.
    resume_payload = None
    if a.init:
        expect_cfg = ({"vocab": V, "d": d, "n_layer": L, "n_head": bg_n_head, "block": seq_len}
                      if is_bytegpt else {"d": d, "L": L, "E": emax,
                                          "trunk_norm": a.trunk_norm})
        report = _warm_start(model, a.init, is_bytegpt, expect_cfg)
        resume_payload = getattr(report, "resume", None)
        model.to(device)
        p0(f"  [--init] {report}", flush=True)

    # H_9954 growth-fork: freeze the trunk, train only the recurrent lane. A frozen trunk still
    # backprops CE to the lane residual (the residual is grad-bearing; freezing skips trunk PARAM
    # grads + Adam state, not gradient flow through the trunk's ops). This is what makes a 303M fork
    # fit a 12GB card AND isolates the lane's contribution. `--freeze-trunk` (the CLMS BOLT arm) is a
    # different flag and would freeze rln.* — do not reuse it.
    if getattr(a, "recurrent_lane_freeze_trunk", False):
        if getattr(model, "rln", None) is None:
            raise SystemExit("--recurrent-lane-freeze-trunk needs --recurrent-lane gru3-bidir")
        for _n, _prm in model.named_parameters():
            _prm.requires_grad_(_n.startswith("rln."))
        _ntrain = sum(p.numel() for p in model.parameters() if p.requires_grad)
        p0(f"  recurrent-lane: TRUNK FROZEN — only rln.* trains ({_ntrain} params)", flush=True)

    # ── H_9803 branch-latent ideation fan: attach the lane BEFORE the optimizer collects params
    #    (registering it on `model` puts it in model.parameters(), which the shell/opt assertion
    #    below requires). Lane off ⇒ the attribute is never set ⇒ byte-identical golden path.
    idl_cell = None
    if str(getattr(a, "ideation_lane", "off")) == "branch-latent":
        if is_bytegpt:
            raise SystemExit("--ideation-lane branch-latent is CLM-only "
                             "(the early-tap route has no ByteGPT twin yet) — drop --arch bytegpt")
        if not a.ideation_corpus:
            raise SystemExit("--ideation-lane branch-latent requires --ideation-corpus "
                             "(blank-line-separated documents: context line + >=2 observed futures)")
        from ifan import BranchLatentFan
        _ctx_len = max(1, seq_len // 2)
        idl_cell = IdeationFanCell(a.ideation_corpus, seq_len, _ctx_len)
        model.ifan = BranchLatentFan(d, V, K=a.ideation_branches, rank=a.ideation_rank,
                                     lam0=a.ideation_lam0,
                                     route_L=(a.ideation_route_l if a.ideation_route == "l3-disjoint" else 0)
                                     ).to(device)
        p0(f"  ideation-fan: K={a.ideation_branches} r={a.ideation_rank} "
           f"objective={a.ideation_objective} route={a.ideation_route}@L{a.ideation_route_l} "
           f"assign={a.ideation_assign} · docs={len(idl_cell.docs)} "
           f"(dropped {idl_cell.n_dropped} single-future blocks) ctx_len={_ctx_len}", flush=True)

    # H_9805 — announce the write-side tension arm. A silent arm is how a control run gets read as
    # a treatment run; the banner and the trailer must agree with the flag or the contrast is void.
    if getattr(model, "tfld", None) is not None:
        p0(f"  tension-field: arm={model.tfld.arm} r={model.tfld.rank} "
           f"n_bucket={model.tfld.n_bucket} lam0={float(model.tfld.lam.detach()):.4f} "
           f"· WRITE-SIDE (pre-trunk embedding residual)", flush=True)

    params = ([p for p in model.parameters() if p.requires_grad]
              + (list(jamo_head.parameters()) if jamo_head else [])
              + (list(objfn.parameters()) if obj_is_module else []))   # H_1640 aux-head params
    # H_9954 --recurrent-lane-freeze-trunk filters model.parameters() to the trainable lane only;
    # with no freeze this is every param (requires_grad defaults True), so the golden path is unchanged.
    if obj_is_module:
        n_obj = sum(p.numel() for p in objfn.parameters())
        p0(f"  objective '{a.objective}' aux params: {n_obj} "
           f"(DROPPED at serialize — not in model.state_dict)", flush=True)
    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, a.adam_beta2), eps=1e-8,
                            weight_decay=a.weight_decay)

    # ══ §4 TrainShell + DDP wrap (execution strategy — the recipe is unchanged) ═════
    #   core_model = the UNWRAPPED inner model, used for ALL rank-0 probes/serialize
    #   (dbes/gauges/val/materialize/_write_clm) — never through the DDP wrapper (§4/§6/§10.9).
    core_model = model
    shell = TrainShell(model, objfn, jamo_head, is_bytegpt=is_bytegpt, V=V,
                       obj_needs_pen=obj_needs_pen, dict_on=dict_on, jamo_on=jamo_on,
                       bf16=a.bf16, device=device)
    if a.comp_lane:
        # H_9900 — attach BEFORE the param assert below so the lane head is allreduced like any
        # other aux head, and force need_pen: the lane reads the trunk penultimate (detached).
        # Read the width from the ACTUAL penultimate rather than guessing an attribute name —
        # ByteGPT and CLM expose different ones, and a wrong guess would fail at the first step.
        shell.need_pen = True
        with torch.no_grad():
            _probe = shell.trunk_penultimate(
                torch.zeros(1, min(8, seq_len), dtype=torch.long, device=device))
        if _probe is None:
            sys.exit("[comp-lane] this model exposes no trunk penultimate")
        _d_pen = int(_probe.shape[1])
        shell.comp_lane = CompositionLane(_d_pen, V).to(device)
        shell.comp_w = float(a.comp_weight)
        params = params + [q for q in shell.comp_lane.parameters()]
        opt.add_param_group({"params": list(shell.comp_lane.parameters())})
        print("  comp-lane: ON · d=%d V=%d weight=%.3f (CE detached from the trunk)"
              % (_d_pen, V, shell.comp_w), flush=True)
        _comp_probe_panel = a.comp_probe_panel
    # §10.1 defense — the shell's TRAINABLE param set MUST equal the optimizer's (aux heads covered).
    # H_9954: --recurrent-lane-freeze-trunk sets the trunk requires_grad=False, so compare only
    # grad-bearing params (a frozen param is deliberately absent from the optimizer, not a lost aux head).
    assert {id(p) for p in shell.parameters() if p.requires_grad} == {id(p) for p in params}, \
        "TrainShell trainable params != optimizer params — an aux head would never be allreduced."
    if ddp_on:
        # §4/§10.8 — CLMConvMoE/ByteGPT/SLW carry NO batch-stat buffers, and mito.active_mask
        # is an intentionally-unregistered per-rank tensor; assert zero buffers so a FUTURE
        # registered buffer fails loudly instead of being silently stomped (broadcast_buffers=False).
        # H_9423: clms.key_emb is a persistent buffer, but it is seed-deterministic (byte-identical
        # across ranks) so broadcast_buffers=False is safe for it. Any OTHER buffer would desync.
        _bad_bufs = [n for n, _ in shell.named_buffers() if not n.endswith("clms.key_emb")]
        assert not _bad_bufs, \
            f"TrainShell grew a non-CLMS buffer {_bad_bufs} — broadcast_buffers=False would desync it."
        train_module = DDP(shell, device_ids=[local_rank], broadcast_buffers=False,
                           find_unused_parameters=a.ddp_find_unused)
        # §2/§4 per-rank RNG divergence AFTER construction+wrap: decorrelate dropout masks
        # (default RNG) across ranks — a SHARED default stream gives sample i the SAME dropout
        # mask on every rank, a correlation the 1-GPU run lacks. Reseed AFTER wrap so init +
        # DDP's param broadcast already made params identical (reseeding BEFORE diverges init).
        torch.manual_seed(a.seed + 100003 * (rank + 1))
        if torch.cuda.is_available():
            torch.cuda.manual_seed_all(a.seed + 100003 * (rank + 1))
    else:
        train_module = shell    # N==1: call the shell UNWRAPPED (same graph, no collectives)

    gen = torch.Generator().manual_seed(42)     # §3/§10.3 SHARED across ranks (NOT rank-offset)
    val_gen = torch.Generator().manual_seed(1234)
    # §4 obj_gen: reseed per rank so negatives/permutations decorrelate across shards (rank=0
    # for N==1 ⇒ +0 ⇒ byte-identical to today). Exact 1-GPU negative reproduction is impossible
    # anyway (it draws all negatives in one call) — accepted stochastic-equivalence (DESCENT gate).
    obj_gen = torch.Generator(device=device).manual_seed(20260628 + a.seed + 7919 * rank)

    latch = {"on": False, "at": 0}
    i0 = GZ_UPPER
    i_floor = GZ_LOWER - 0.05
    split_step = max(1, steps // 2)

    # ── corpus cells (reuse ByteCell + resolver) ─────────────────────────────
    if a.validation_corpus and len(a.validation_corpus) != len(a.corpus):
        sys.exit("[validation-corpus] needs exactly one entry per --corpus cell: "
                 f"got {len(a.validation_corpus)} validation and {len(a.corpus)} train entries")
    cells, labels = [], []
    for ci, spec in enumerate(a.corpus):
        p = resolve_corpus_path(spec)
        vp = (resolve_corpus_path(a.validation_corpus[ci])
              if a.validation_corpus else None)
        cells.append(ByteCell(p, val_frac=a.val_frac, validation_path=vp))
        labels.append(a.cell_label[ci] if ci < len(a.cell_label) else f"cell{ci}")
        c = cells[-1]
        val_desc = (f"val_file={c.validation_path} val={c.val_size}"
                    if c.validation_path is not None else f"val_tail={c.val_size}")
        p0(f"  corpus cell[{ci}] {labels[ci]:<12s} {p} size={c.size} "
           f"train={c.train_end} {val_desc}", flush=True)
    if not cells:
        p0("  corpus: NONE -> synthetic smoke", flush=True)

    # ── H_9840 sleep-schedule lane ────────────────────────────────────────────────────────────
    #   Constructed only when the arm is on ⇒ `off` never allocates a schedule, a replay buffer or
    #   a generator, and the batch draw below stays byte-identical. ANNOUNCED at startup: a silent
    #   arm is how a CONTROL run gets read as a treatment run (the H_9805 precedent above).
    slp = None
    slp_stats = None
    if a.sleep_schedule != "off":
        if not cells:
            sys.exit("[sleep-schedule] needs a real --corpus: the SLEEP phase rehearses windows "
                     "the WAKE phase consumed, and the synthetic smoke stream has no windows.")
        # NO-TUNE-TO-GREEN GATE (self-caught while writing the selftest): `--steps` can flip the
        # contrast on its own. dream-lib front-loads its WAKE bout, so steps=12 at ticks=90
        # realizes sleep_ratio 0.0000 on dream-lib but 0.2500 on fixed-alternating — the
        # "ratio-matched" control would not be ratio-matched, and any delta would be a RATIO
        # delta wearing an arrangement label. The two cycles are multiset-identical by
        # construction; only a WHOLE number of sessions carries that equality into the realized
        # run. So a partial session is refused rather than silently mis-read.
        if steps % a.sleep_ticks != 0:
            sys.exit(f"[sleep-schedule] --steps {steps} is not a whole multiple of --sleep-ticks "
                     f"{a.sleep_ticks}. A partial session realizes DIFFERENT wake/sleep ratios in "
                     f"the two arms (dream-lib front-loads WAKE), which un-matches the control and "
                     f"turns an arrangement contrast into a ratio contrast. Use steps = k * "
                     f"{a.sleep_ticks}, or shorten --sleep-ticks. "
                     f"(`--sleep-selftest N` reports this as steps_alignment.)")
        slp = SleepSchedule(a.sleep_schedule, a.sleep_ticks)
        _cm = slp_meter(slp.cycle)
        slp_stats = {"arm": slp.arm, "ticks": slp.n, "cycle_meter": _cm,
                     "replay_cap": a.sleep_replay_cap,
                     "wake_steps": 0, "sleep_steps": 0, "replay_batches": 0, "warmup_fresh": 0}
        p0(f"  sleep-schedule: arm={slp.arm} ticks={slp.n} "
           f"wake={_cm['wake']} sleep={_cm['sleep']} (sleep_ratio={_cm['sleep_ratio']:.4f}) "
           f"stages={_cm['stage_counts']} max_sleep_bout={_cm['max_sleep_bout']} "
           f"replay_cap={a.sleep_replay_cap} · SLEEP steps REPLAY the wake buffer "
           f"(H_9840 · SUBORDINATE to H_9833: no consolidation objective exists yet, so a sleep "
           f"step is REHEARSAL, not distillation)", flush=True)
        p0(f"  sleep-schedule cycle: {slp.render(min(slp.n, 120))}", flush=True)

    _samp_cells = [c for c in cells if c.train_end >= seq_len + 2]
    _samp_w = torch.tensor([float(c.train_end) for c in _samp_cells]) \
        if _samp_cells else torch.tensor([1.0])

    # --require-cells N: fail LOUD if the usable register-cell count != N (a_chat_registers
    # 4-cell completeness guard, parity with cli/train.hexa). Prevents silently training on
    # an incomplete register — the clm303 ko-SNS starvation overfit (train-py-3 convergence:
    # a small/incomplete corpus overfits to a low val_CE while free-gen coherence collapses).
    if a.require_cells > 0 and len(_samp_cells) != a.require_cells:
        sys.exit(
            f"[require-cells] --require-cells {a.require_cells} but {len(_samp_cells)} usable "
            f"register cell(s) (window-fit train_end>={seq_len + 2}): refusing to train on an "
            f"incomplete register (a_chat_registers overfit/starvation guard). usable cells: "
            f"{[c.path for c in _samp_cells]}")

    # §3/§5 GLOBAL batch preserved: --batch-size is the GLOBAL batch; each rank materializes
    # B_local = B_global // world. world==1 ⇒ B_local == B_global (N==1 byte-identical).
    B_global = a.batch_size
    B_local = B_global // world

    # ── H_9423 CLMS store-bridge co-training sub-batch (line-aligned, separate RNG) ──────────
    sb_cell = sb_gen = None
    Bs_global = Bs_local = 0
    if a.store_bridge or a.freeze_trunk:
        if a.arch != "clm":
            sys.exit("[store-bridge] requires --arch clm (the CLMS lane is CLMConvMoE-only)")
        if not a.store_bridge:
            sys.exit("[store-bridge] --freeze-trunk (BOLT) still needs --store-bridge <c.txt>")
        if not cells:
            sys.exit("[store-bridge] needs a trunk --corpus for retention/fluency (pass the storebind "
                     "c.txt itself as a --corpus cell, or a replay corpus)")
        if a.store_batch % world != 0:
            sys.exit(f"[store-bridge] --store-batch {a.store_batch} not divisible by world {world}")
        _key = core_model.clms.key_emb.detach().cpu().numpy()
        sb_cell = StoreBindCell(a.store_bridge, _key, a.clms_n_slot, a.store_win, a.store_val_frac,
                                key_fn=a.clms_key_fn)
        sb_gen = torch.Generator().manual_seed(4242)      # shared across ranks; SEPARATE from gen=42
        Bs_global = a.store_batch
        Bs_local = Bs_global // world
        if a.freeze_trunk:                                # BOLT control: only clms.* trains
            for n, prm in core_model.named_parameters():
                prm.requires_grad_(n.startswith("clms."))
        if a.store_win != 24:
            p0(f"  ⚠️ --store-win {a.store_win} != 24 (evaluate --win default): the verdict eval "
               f"MUST pass --win {a.store_win} or train/verdict window geometry differ.", flush=True)
        p0(f"  store-bridge: {len(sb_cell.ex)} lines · train_n={sb_cell.train_n} · Bs={Bs_global} "
           f"win={a.store_win} n_slot={a.clms_n_slot} freeze_trunk={a.freeze_trunk}", flush=True)

    def get_store_batch():
        idx = torch.randint(0, sb_cell.train_n, (Bs_global,), generator=sb_gen)   # all ranks identical
        sl = idx[rank * Bs_local:(rank + 1) * Bs_local].tolist()
        xs, ys, Ks, Ps, Ts_, Tbs, Ms = zip(*[sb_cell.ex[i] for i in sl])
        return (torch.stack(xs).to(device), torch.stack(ys).to(device),
                torch.stack(Ks).to(device), torch.stack(Ps).to(device),
                torch.stack(Ts_).to(device),                          # H_9423 Stage1.5 target_slot
                torch.stack(Tbs).to(device),                          # H_9888 second target slot
                torch.stack(Ms).to(device))                           # H_9888 A/B/operator rows (B,3)

    # H_9803 — deterministic document sampler for the ideation sub-batch. Its own generator so
    # turning the lane on does not perturb the main batch draw (which would confound every
    # lane-on/lane-off comparison with a different corpus stream).
    idl_gen = torch.Generator(); idl_gen.manual_seed(int(a.seed) ^ 0x9803)

    def get_ideation_batch():
        n = len(idl_cell.docs)
        take = min(int(a.ideation_docs), n)
        idx = torch.randperm(n, generator=idl_gen)[:take].tolist()
        out = []
        for i in idx:
            x_i, y_i, m_i, fork_i = idl_cell.docs[i]
            out.append((x_i.to(device), y_i.to(device), m_i.to(device), fork_i))
        return out

    # H_9840 — the wake replay buffer + its OWN generator (like idl_gen/sb_gen above): a sleep
    # step must not consume the main `gen` stream, or the arm comparison would also be a
    # different-corpus-stream comparison. Both are allocated only when the lane is on.
    slp_gen = torch.Generator().manual_seed(int(a.seed) ^ 0x9840) if slp is not None else None
    slp_replay = []                    # FIFO of (cell, start) specs consumed while awake

    # Exact recovery is restored only after every optimizer/sampler object exists. `steps` is
    # deliberately excluded: a checkpoint made against the original endpoint resumes toward that
    # same endpoint, while a legacy weights-only warm start begins a new run at step 1.
    run_recipe = {
        "arch": a.arch, "d": d, "L": L, "e0": e0, "emax": emax,
        "seed": a.seed, "seq_len": seq_len, "batch_size": a.batch_size,
        "lr": a.lr, "adam_beta2": a.adam_beta2,
        "weight_decay": a.weight_decay, "lr_schedule": a.lr_schedule,
        "warmup_steps": a.warmup_steps, "lr_decay_steps": lr_decay_steps,
        "min_lr_ratio": a.min_lr_ratio,
        "corpus": list(a.corpus),
        "store_bridge": a.store_bridge,
        "store_batch": a.store_batch, "store_win": a.store_win,
        "store_addr_weight": a.store_addr_weight, "freeze_trunk": bool(a.freeze_trunk),
        "trunk_norm": a.trunk_norm, "clms_dual": bool(a.clms_dual),
        "store_val_center": bool(a.store_val_center), "bf16": bool(a.bf16),
        "sample": a.sample,
    }
    # Preserve byte-identical legacy exact-resume recipes when the new explicit
    # validation path is unused, while binding every external validation file
    # into the recipe when it is used.
    if a.validation_corpus:
        run_recipe["validation_corpus"] = list(a.validation_corpus)
    resume_generators = {
        "corpus": gen, "validation": val_gen, "objective": obj_gen,
        "store": sb_gen, "ideation": idl_gen, "sleep": slp_gen,
    }
    resume_step = 0
    resume_digest = ""
    if resume_payload is not None:
        saved_recipe = resume_payload.get("recipe")
        if saved_recipe != run_recipe:
            raise ValueError(
                "resume recipe differs from checkpoint; exact recovery refuses changed data, "
                f"seed, batch, architecture, or CLMS settings\nsaved={saved_recipe}\nrun={run_recipe}")
        resume_step, resume_digest = _restore_resume_state(
            resume_payload, core_model, opt, resume_generators, device)
        if resume_step >= steps:
            raise ValueError(f"resume completed_step={resume_step} must be below --steps={steps}")
        p0(f"  [exact-resume] state digest {resume_digest} verified · completed={resume_step} "
           f"· next={resume_step + 1} · endpoint={steps}", flush=True)

    def get_batch(step):
        if cells:
            # ── H_9840: SLEEP step ⇒ rehearse the wake buffer instead of drawing fresh corpus.
            #    Deep stages (N3/REM, dr_imagination_active==1) replay the WHOLE buffer; the light
            #    stages (N1/N2) rehearse only its recent quarter. Until the buffer holds a full
            #    batch the step falls back to a fresh draw (counted as `warmup_fresh`, never
            #    silently) — a sleep step cannot rehearse what was never seen.
            if slp is not None:
                _stage = slp.stage_at(step)
                if _stage != 0:
                    slp_stats["sleep_steps"] += 1
                    if len(slp_replay) >= B_global:
                        pool = (slp_replay if slp.is_deep(_stage)
                                else slp_replay[-max(B_global, len(slp_replay) // 4):])
                        _idx = torch.randint(0, len(pool), (B_global,), generator=slp_gen).tolist()
                        specs = [pool[i] for i in _idx]
                        slp_stats["replay_batches"] += 1
                        lo = rank * B_local
                        xs, ys = [], []
                        for cell, start in specs[lo:lo + B_local]:
                            w = cell.materialize(start, seq_len)
                            xs.append(w[0]); ys.append(w[1])
                        return torch.stack(xs).to(device), torch.stack(ys).to(device)
                    slp_stats["warmup_fresh"] += 1
                else:
                    slp_stats["wake_steps"] += 1
            # ── §3 SPEC phase (ALL ranks, IDENTICAL shared gen=42): draw the GLOBAL batch's
            #    window specs in TODAY's interleaved order (proportional: multinomial→spec;
            #    roundrobin: index→spec). This global spec list is byte-identical to the
            #    1-GPU draw; the proportional cell weighting is globally exact.
            specs = []
            for b in range(B_global):
                if a.sample == "proportional" and _samp_cells:
                    ci = int(torch.multinomial(_samp_w, 1, generator=gen).item())
                    cell = _samp_cells[ci]
                else:
                    cell = cells[(step - 1 + b) % len(cells)]
                start = cell.window_spec(seq_len, gen)   # None ⇒ synthetic fallback (no randint)
                specs.append((cell, start))
            if slp is not None:                          # remember what was seen while awake
                slp_replay.extend([s for s in specs if s[1] is not None])
                if len(slp_replay) > a.sleep_replay_cap:
                    del slp_replay[:len(slp_replay) - a.sleep_replay_cap]
            # ── §3 MATERIALIZE phase (rank-local slice): rank r takes [r*B_local, (r+1)*B_local).
            lo = rank * B_local
            xs, ys = [], []
            for cell, start in specs[lo:lo + B_local]:
                if start is None:
                    base = torch.arange(seq_len)
                    w = (base % V, (base + 1) % V)
                else:
                    w = cell.materialize(start, seq_len)
                xs.append(w[0]); ys.append(w[1])
            return torch.stack(xs).to(device), torch.stack(ys).to(device)
        base = torch.arange(seq_len)
        x = ((3 + base * 37) % V).unsqueeze(0).repeat(B_local, 1).to(device)
        y = ((14 + base * 37) % V).unsqueeze(0).repeat(B_local, 1).to(device)
        return x, y

    # NOTE (§4): the trunk-penultimate helper (N7 dict/jamo aux + compositional objectives)
    # was RELOCATED verbatim into TrainShell.trunk_penultimate so the per-step loss graph is
    # one DDP forward(). The rank-0 probes below (val/dbes/gauges) use `model` directly.

    @torch.no_grad()
    def cell_val_ce(c):
        if c.val_size < seq_len + 2:
            return None
        was = model.training; model.eval()
        tot, nb = 0.0, 0
        for _ in range(a.val_batches):
            xs, ys = [], []
            for _ in range(a.batch_size):
                w = c.val_window(seq_len, val_gen)
                if w is None: continue
                xs.append(w[0]); ys.append(w[1])
            if not xs: continue
            vx = torch.stack(xs).to(device); vy = torch.stack(ys).to(device)
            if a.bf16 and device.startswith("cuda"):
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    vo = model(vx, vy)
            else:
                vo = model(vx, vy)
            tot += float(vo["ce_loss"].detach()); nb += 1
        if was: model.train()
        return (tot / nb) if nb else None

    def val_per_cell():
        return {lab: v for lab, c in zip(labels, cells)
                if (v := cell_val_ce(c)) is not None}

    # ── serialize helper (end-of-run AND intermediate --ckpt-every checkpoints) ──
    #   CLM → .clm v0.3 (CLMConvMoE additive readout, materialized TLoRA experts).
    #   ByteGPT → .pt (cfg+state_dict) → core/serialize.py::serialize → .bin (5×u32
    #   header). The engine (generator L3 mouth-sniff) auto-dispatches .bin to the bytegpt
    #   decode; `anima-py evaluate` auto-detects .bin vs .clm by header, so no eval change.
    def _write_bin(out_path):
        # Write the model-only bridge input to a temporary file.  It must never share
        # <out>.pt with _write_pt(): that path is the exact-resume checkpoint carrying
        # optimizer/RNG/sampler state.  The old collision silently replaced the resumable
        # checkpoint at shutdown.  Serialize to a sibling temporary output and atomically
        # publish the engine checkpoint only after the bridge succeeds.
        out_dir = os.path.dirname(os.path.abspath(out_path))
        os.makedirs(out_dir, exist_ok=True)
        pt_fd, pt_path = tempfile.mkstemp(prefix=".bytegpt-bridge-", suffix=".pt",
                                          dir=out_dir)
        os.close(pt_fd)
        bin_fd, bin_tmp = tempfile.mkstemp(prefix=".bytegpt-engine-", suffix=".bin",
                                            dir=out_dir)
        os.close(bin_fd)
        sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
        ck = {"model": sd, "config": model.cfg.as_dict(),
              "val_ce": (round(lossF, 5) if lossF is not None else None),
              "step": steps, "nparam": n_params}
        try:
            torch.save(ck, pt_path)
            BGS.serialize(pt_path, bin_tmp)
            os.replace(bin_tmp, out_path)
        finally:
            if os.path.exists(pt_path):
                os.unlink(pt_path)
            if os.path.exists(bin_tmp):
                os.unlink(bin_tmp)
        print(f"  .bin WRITTEN {os.path.getsize(out_path)} bytes -> {out_path}", flush=True)

    def _write_clm(out_path):
        if is_bytegpt:
            _write_bin(out_path)
            return
        e_ser = mito.e_active
        mat = materialize_experts_into_state(model)
        sd_active = {}
        for k, vv in mat.items():
            if k in ("moe.router.weight", "moe.router.bias"):
                sd_active[k] = vv[:e_ser].contiguous()
            elif k.startswith("moe.experts."):
                if int(k.split(".")[2]) < e_ser:
                    sd_active[k] = vv
            else:
                sd_active[k] = vv
        S.serialize_v3(sd_active, n_trunk_layers=L, n_experts=e_ser, out_path=out_path,
                       n_factions=a.n_factions)
        # H_9200 E1 — append the "SLW\x01" gated-write forward-slot trailer if engaged
        # (core/serialize.append_slw_trailer). Additive models skip it (byte-identical).
        if getattr(model, "slw", None) is not None:
            nb = S.append_slw_trailer(out_path, model.slw)
            print(f"  SLW trailer appended {nb} bytes (n_slot={model.slw.n_slot} "
                  f"k={model.slw.k} d_s={model.slw.d_s})", flush=True)
        # H_9423 — append the "CLMS" store-bridge trailer if the lane is engaged (AFTER SLW so the
        # chain order stays CLMB→SLW→CLML→CLMS). Co-trained; store content is NOT serialized.
        if getattr(model, "clms", None) is not None:
            nb = S.append_clms_trailer(out_path, model.clms)
            print(f"  CLMS trailer appended {nb} bytes (n_slot={model.clms.n_slot} "
                  f"d_k={model.clms.d_k} d_s={model.clms.d_s} r={model.clms.r})", flush=True)
        # H_9698 — append the "MBND" mouth-binder trailer if the lane is engaged (AFTER CLMS so the
        # chain end stays MBND, the order core/decode.py reads).
        if getattr(model, "mbnd", None) is not None:
            nb = S.append_mbnd_trailer(out_path, model.mbnd)
            print(f"  MBND trailer appended {nb} bytes (rank={model.mbnd.rank} "
                  f"linear={model.mbnd.linear})", flush=True)
        # H_9803 — append the "IFAN" branch-latent trailer if the ideation lane is engaged (AFTER
        # MBND so the chain end stays IFAN, the order core/decode.py reads).
        if getattr(model, "ifan", None) is not None:
            nb = S.append_ifan_trailer(out_path, model.ifan)
            print(f"  IFAN trailer appended {nb} bytes (K={model.ifan.K} "
                  f"rank={model.ifan.rank} route_L={model.ifan.route_L})", flush=True)
        # H_9805 — append the "TFLD" write-side tension-field trailer if the lane is engaged (LAST,
        # after IFAN, so the chain end stays TFLD). The arm is written INTO the trailer so a ckpt can
        # never be mistaken for the other arm's — a duel/rank1 mix-up would silently void the contrast.
        if getattr(model, "tfld", None) is not None:
            nb = S.append_tfld_trailer(out_path, model.tfld)
            print(f"  TFLD trailer appended {nb} bytes (arm={model.tfld.arm} "
                  f"rank={model.tfld.rank} n_bucket={model.tfld.n_bucket})", flush=True)
        # H_9954 — append the "RCRL" recurrent-lane trailer if the lane is engaged, so the .clm
        # carries the 3-cell GRU weights that `anima-py evaluate --iit4-recurrent-lane` reads.
        if getattr(model, "rln", None) is not None:
            nb = S.append_rcrl_trailer(out_path, model.rln)
            print(f"  RCRL trailer appended {nb} bytes (recurrent-lane gru3-bidir)", flush=True)
        print(f"  .clm WRITTEN {os.path.getsize(out_path)} bytes -> {out_path}", flush=True)
        print(f"  clm_decodable={VC.clm_decodable(open(out_path, 'rb').read())}", flush=True)
        if getattr(a, "trunk_norm", "global") == "position":
            # H_9875 — the decode lane now exists, so the ckpt carries a CNRM marker telling the
            # loader which reduction its weights were fitted under. Without the marker an
            # engine-native score of this ckpt would silently measure a different model.
            S.append_trunknorm_trailer(out_path, "position")
            print("  CNRM trailer appended (trunk_norm=position) — the .clm decode path reduces "
                  "per position for this ckpt; engine-native scores are semantically correct.",
                  flush=True)
        if getattr(a, "serialize_parity", ""):
            try:
                serialize_parity(model, out_path, a.serialize_parity, device,
                                 max_items=a.parity_items)
            except Exception as e:                      # a diagnostic must never kill a finished run
                print(f"  SERIALIZE-PARITY skipped: {type(e).__name__}: {e}", flush=True)

    # ── torch .pt writer (RESUMABLE — the .clm is quantized and --init refuses it) ──
    #   --ckpt-every writes BOTH: the .clm (evaluatable) and this .pt (warm-startable).
    #   Without the .pt an interrupted long run is unrecoverable — a killed 13h fire
    #   restarts from step 0 (N2 2026-07-13: 17h of GPU lost across two kills, one to a
    #   pod stop that wiped /workspace, one to earlyoom).
    def _write_pt(out_path, completed_step):
        sd = {k: v.detach().cpu() for k, v in core_model.state_dict().items()}
        if jamo_head:
            for k, v in jamo_head.state_dict().items():
                sd[f"_jamo_head.{k}"] = v.detach().cpu()
        optimizer_state = opt.state_dict()
        rng_state = {
            "torch_cpu": torch.get_rng_state(),
            "torch_cuda": (torch.cuda.get_rng_state_all()
                           if str(device).startswith("cuda") else []),
            "python": random.getstate(),
            "generators": {name: (generator.get_state() if generator is not None else None)
                           for name, generator in resume_generators.items()},
        }
        state_digest = resume_state_digest(sd, optimizer_state, completed_step, rng_state)
        checkpoint = {
            "schema": RESUME_SCHEMA,
            "model": sd,
            "optimizer": optimizer_state,
            "completed_step": int(completed_step),
            "endpoint_steps": int(steps),
            "recipe": run_recipe,
            "rng": rng_state,
            "state_digest": state_digest,
        }
        torch.save(checkpoint, out_path)
        print(f"  torch ckpt -> {out_path} ({os.path.getsize(out_path)} bytes · "
              f"exact resume at step {completed_step} · state={state_digest})", flush=True)

    # ── train loop ───────────────────────────────────────────────────────────
    model.train()
    t0 = time.time(); loss0 = lossF = None
    last_aux = {}; dbes_log = []
    # active-expert count for logs/summary — CLM tracks it on the mitosis controller;
    # ByteGPT has no experts (mito is None) so it is a fixed 1.
    def e_now():
        return mito.e_active if mito is not None else 1
    # ── H_9846 structure-envelope watch: CONTROLS FIRST, before step 1 ──────────────────
    #    The order is frozen and it is the whole discipline: the positive control (a planted
    #    structure cliff, which must be recovered) and the zero-truth pedestal (structure-free
    #    input, which must read exactly zero) run BEFORE a single training value is taken. An
    #    uncertified watch prints its status and then stays silent forever — reading a run
    #    through an instrument that cannot see a planted signal, or that manufactures one, is
    #    precisely what `positive-control-before-reading-a-negative` and
    #    `phi-estimator-needs-zero-truth-pedestal` exist to stop. Training itself is NEVER
    #    aborted by this: a monitor that can stop a run is a lever, and this is not a lever.
    phi_mon_ticks = []
    phi_mon_battery = None
    phi_mon_every = a.phi_monitor_every or a.log_every
    phi_mon_on = (a.phi_envelope_monitor == "on")
    if phi_mon_on:
        phi_mon_battery = PEM.battery_liveness()
        p0(f"  [structure-envelope H_9846] battery {phi_mon_battery['status']} — "
           f"plant_fires={phi_mon_battery['plant_fires']} "
           f"pedestal_refuses={phi_mon_battery['pedestal_refuses']} "
           f"discriminates_ramp={phi_mon_battery['discriminates_ramp']} "
           f"(plant gap {phi_mon_battery['arms'][0]['plant']['cliff_gap']:.6f} · pedestal "
           f"{phi_mon_battery['arms'][0]['pedestal']['cliff_gap']:.6g} · ramp cadence-inflation "
           f"{phi_mon_battery['ramp_cadence_inflation']:.4f}×)", flush=True)
        if not phi_mon_battery["certified"]:
            phi_mon_on = False
            p0(f"  [structure-envelope H_9846] {phi_mon_battery['why']} "
               f"→ NO value will be reported. Training continues unaffected.", flush=True)
        else:
            p0(f"  [structure-envelope H_9846] MONITOR-ONLY, every {phi_mon_every} steps — "
               f"never in the loss (a_train_inline_gauge); these are envelope/structure "
               f"statistics, NOT Φ (a_phi_iit4_tool).", flush=True)
    # intermediate-ckpt extension: bytegpt writes .bin, clm writes .clm.
    _ck_ext = ".bin" if is_bytegpt else ".clm"
    # ── H_9957 FIELD-LOOP dispatch — reuse the loaded/built model; run the closed text<->PureField
    #    re-entry co-training instead of the standard random-window loop (v1 CLM-only, single-process).
    if getattr(a, "field_loop", False):
        if ddp_on:
            sys.exit("[field-loop] v1 is single-process — run without torchrun/DDP")
        if is_bytegpt:
            sys.exit("[field-loop] v1 supports the CLM organ only (ByteGPT emb_residual unwired)")
        import field_loop as FL
        core_m = model.module if hasattr(model, "module") else model
        dfl = int(getattr(core_m.cfg, "d_model", getattr(core_m.cfg, "d", 0)))
        raw = b"".join(open(c, "rb").read() for c in a.corpus) if a.corpus else b""
        if len(raw) < a.field_block + 2:
            sys.exit(f"[field-loop] needs --corpus with >= field-block+2 bytes (got {len(raw)})")
        if a.field_loop_eval:                            # MEASURE a trained coupling (no training)
            if a.score_mask:                             # H_9957 fieldctl payload-byte DV (doc/mask-aware)
                import json as _json
                mask = _json.load(open(a.score_mask))
                if mask.get("format") == "oow":          # H_9957 NATURAL carriage DV (no planted payload)
                    fl = FL.FieldLoop.load(a.field_loop_eval, a.field_b, device=device)
                    ev = FL.field_loop_eval_oow(model, fl, raw, mask, device=device, seed=a.seed,
                                                boot=a.field_phi_boot)
                    p0(f"=== anima-py train --field-loop-eval --score-mask (H_9957 NATURAL OOW DV) === "
                       f"cells={ev['cells_scored']} B={ev['B']} gamma={ev['gamma']:+.5f}", flush=True)
                    p0(f"[oow-eval] OOW-anchored   aligned={ev['aligned_oow']:.4f} "
                       f"yoked={ev['yoked_oow']:.4f} sever={ev['sever_oow']:.4f} "
                       f"(n={ev['n_aligned_oow']})", flush=True)
                    p0(f"[oow-eval] in-block ctrl  aligned={ev['aligned_inblock']:.4f} "
                       f"yoked={ev['yoked_inblock']:.4f} sever={ev['sever_inblock']:.4f} "
                       f"(n={ev['n_aligned_inblock']})", flush=True)
                    p0(f"[oow-eval] DELTA_OOW = {ev['delta_oow']:+.5f} · DELTA_INBLOCK = "
                       f"{ev['delta_inblock']:+.5f} · SPECIFICITY = {ev['specificity']:+.5f} nats "
                       f"(carriage needs Delta_OOW > 0 AND > Delta_inblock)", flush=True)
                    if ev.get("boot"):                       # within-run precision on a ~1e-3 nat DV
                        p0(f"[oow-eval] BOOT({ev['boot']} paired moving-block) specificity "
                           f"mean={ev['spec_mean']:+.5f} sd={ev['spec_sd']:.5f} "
                           f"90% CI [{ev['spec_lo90']:+.5f}, {ev['spec_hi90']:+.5f}]", flush=True)
                    return 0
                if a.field_phi:                          # H_9957 MISSION DV: faithful IIT-4 Φ of the state
                    fl = FL.FieldLoop.load(a.field_loop_eval, a.field_b, device=device)
                    pv = FL.field_loop_phi(model, fl, raw, mask, device=device, seed=a.seed,
                                           boot=a.field_phi_boot)
                    p0(f"=== anima-py train --field-loop-eval --field-phi (H_9957 mission Φ-DV) === "
                       f"m={pv['m']} cells · n={pv['n']} samples · gamma={pv['gamma']:+.5f}", flush=True)
                    p0(f"[field-phi] faithful IIT-4  Φ_aligned={pv['phi_aligned']:.5f}  "
                       f"Φ_yoked={pv['phi_yoked']:.5f}  Φ_shuffle={pv['phi_shuffle']:.5f}", flush=True)
                    p0(f"[field-phi] DELTA_PHI = Φ_aligned - max(yoked,shuffle) = {pv['delta_phi']:+.5f}  "
                       f"(>bar ⇒ necessity forced integration; ≈0 ⇒ it did not)", flush=True)
                    if pv.get("boot"):                       # power for the negative (prereg equivalence)
                        _BAR = 0.05                          # H_9957 prereg bar, frozen before results
                        _lo, _hi = pv["delta_lo90"], pv["delta_hi90"]
                        # Read the CI against the frozen bar HERE — printing one fixed trailer whatever the
                        # numbers say is how a log gets misread as a verdict it never made.
                        _v = ("EQUIVALENT-TO-ZERO (powered negative: 90% CI inside ±bar)"
                              if (-_BAR < _lo and _hi < _BAR) else
                              "EARNED (powered positive: whole 90% CI above +bar)" if _lo >= _BAR else
                              "UNDERPOWERED (90% CI crosses the bar — not a verdict either way)")
                        p0(f"[field-phi] BOOT({pv['boot']} moving-block) Δφ mean={pv['delta_mean']:+.5f} "
                           f"sd={pv['delta_sd']:.5f}  90% CI [{_lo:+.5f}, {_hi:+.5f}]  bar=±{_BAR}", flush=True)
                        p0(f"[field-phi] PREREG READ: {_v}", flush=True)
                    return 0
                fl = FL.FieldLoop.load(a.field_loop_eval, int(mask["K"]), device=device)
                ev = FL.field_loop_eval_fieldctl(model, fl, raw, mask, device=device, seed=a.seed)
                p0(f"=== anima-py train --field-loop-eval --score-mask (H_9957 fieldctl payload DV) === "
                   f"K={ev['K']} docs={ev['docs_scored']} gamma={ev['gamma']:+.5f} "
                   f"chance=ln K={ev['chance_nats']:.4f} nats", flush=True)
                p0(f"[fieldctl-eval] payload CE  aligned={ev['aligned_ce']:.4f}  "
                   f"yoked={ev['yoked_ce']:.4f}  sever={ev['sever_ce']:.4f}", flush=True)
                p0(f"[fieldctl-eval] DELTA_COLLAPSE = min(yoked,sever)-aligned = "
                   f"{ev['delta_collapse']:+.4f} nats  (>0 ⇒ the field carried the out-of-window key; "
                   f"prereg CERTIFIED gate: Δ>=0.8 ∧ aligned<=0.4)", flush=True)
                return 0
            fl = FL.FieldLoop.load(a.field_loop_eval, a.field_b, device=device)
            ev = FL.field_loop_eval(model, fl, raw, K=a.field_b, block=a.field_block,
                                    seed=a.seed, device=device)
            p0(f"=== anima-py train --field-loop-eval (H_9957 Delta_collapse) === "
               f"K={ev['K']} block={a.field_block} gamma={ev['gamma']:+.5f}", flush=True)
            p0(f"[field-loop-eval] aligned={ev['aligned']:.4f} yoked={ev['yoked']:.4f} "
               f"DELTA_COLLAPSE={ev['delta_collapse']:+.4f} nats/byte "
               f"(own-field vs wrong-field own-byte log-prob)", flush=True)
            p0(f"[field-loop-eval] sever(field cut)={ev['sever']:.4f} "
               f"aligned-sever={ev['aligned_minus_sever']:+.4f} "
               f"(<=0 ⇒ model ignores the text-dependence = seed)", flush=True)
            return 0
        p0(f"=== anima-py train --field-loop (H_9957 · arm={a.field_arm}) === "
           f"d={dfl} block={a.field_block} B={a.field_b} steps={steps} corpus={len(raw)}B", flush=True)
        fl, hist = FL.field_loop_train(model, raw, a.field_arm, steps, dfl, B=a.field_b,
                                       block=a.field_block, lr=a.lr, seed=a.seed, device=device,
                                       log=lambda s: p0(s, flush=True), doc_len=a.field_doc_len,
                                       write=a.field_write, cells=a.field_cells,
                                       coupling_seed=(None if a.field_coupling_seed < 0
                                                      else a.field_coupling_seed),
                                       grad_wb=a.field_bptt, train_physics=a.field_train_physics,
                                       sg_drive=a.field_sg_drive, mech=a.field_mech,
                                       mech_lam0=a.field_mech_lam0)
        if a.out:
            # field-loop never runs the mitosis GROW loop, so mito.e_active is still e0; but a --init'd
            # model carries all `emax` experts. Serialize ALL of them (else _write_clm's e_ser=e_active
            # drops experts -> nblk mismatch on reload). No mitosis split happened, so this is lossless.
            if mito is not None:
                mito.e_active = mito.emax
            _write_clm(a.out)
            fl.save(a.out + ".fl.pt")                     # the trained bridge+gamma the eval needs
            p0(f"[field-loop] wrote {a.out} (+{a.out}.fl.pt) · arm={a.field_arm} "
               f"gamma={float(fl.gamma.detach()):+.5f} final_CE={hist[-1]:.4f}", flush=True)
        return 0

    # ── H_9841 imagination-reconsolidation lane (None ⇒ every branch below skipped) ──
    #    RANK-LOCAL by construction: each rank rehearses the stream IT saw, so the lane
    #    adds no collective and cannot desync DDP (shapes are preserved exactly).
    imag_lane = None
    if a.imagination_replay > 0.0:
        imag_lane = ImaginationLane(a.imagination_replay, a.reconsolidate_every,
                                    a.vadapt_on_replay, a.imagination_select, a.seed + rank)
        p0(f"  [imagination] H_9841 lane ON — ratio={a.imagination_replay:g} "
           f"every={a.reconsolidate_every} vadapt_on_replay={a.vadapt_on_replay} "
           f"select={a.imagination_select} (p5 invariant watch armed)", flush=True)
    for step in range(resume_step + 1, steps + 1):
        # --ckpt-every: dump an intermediate ckpt of the state AFTER (step-1) updates
        # (step-window multiplex — one run yields 2000/4000/… checkpoints, no re-train).
        # §6 rank-0-only intermediate serialize on the UNWRAPPED core_model; barrier AFTER the
        # write (nothing to protect before) so non-zero ranks don't race into the next step's
        # collective while rank 0 serializes a 303M .clm.
        if (a.ckpt_every > 0 and a.out and step > 1 and
                (step - 1) % a.ckpt_every == 0 and (step - 1) > resume_step):
            if rank == 0:
                _write_clm(f"{a.out}.step{step - 1}{_ck_ext}")
                # …and the exact-resume twin. Overwrite one rolling file: model, optimizer,
                # completed step and every RNG/sampler stream are one atomic trajectory state.
                _write_pt(f"{a.out}.resume.pt", step - 1)
                model.train()
            if ddp_on:
                dist.barrier()
            if a.stop_after_ckpt:
                p0(f"  [stop-after-ckpt] clean process boundary after step {step - 1}; "
                   f"resume with --init {a.out}.resume.pt --steps {steps}", flush=True)
                if ddp_on:
                    dist.destroy_process_group()
                return 0
        step_lr = scheduled_lr(step, a.lr, a.lr_schedule, a.warmup_steps,
                               lr_decay_steps, a.min_lr_ratio)
        if savant_on:
            inh = savant_inhibition(step, steps, i0, i_floor, latch)
            wd = inhibition_to_wd(inh); dp = inhibition_to_dropout(inh)
        else:
            wd, dp = a.weight_decay, 0.0
        if a.wd_floor >= 0.0: wd = a.wd_floor             # N6 sweep override
        if a.dropout_floor >= 0.0: dp = a.dropout_floor   # N6 sweep override
        for grp in opt.param_groups:
            grp["weight_decay"] = wd
            grp["lr"] = step_lr
        for m in model.modules():
            if isinstance(m, nn.Dropout):
                m.p = dp
        if mitosis_on and step == split_step and mito.e_active < emax:
            prev = mito.e_active
            new_e = (tlora_aware_split(mito, 0, opt) if tlora_on
                     else mito.split(0, opt))
            p0(f"  step {step} (MITOSIS SPLIT) E {prev}->{new_e}", flush=True)
            # §1 belt-and-braces: the split is provably deterministic across ranks (bitwise-
            # identical params ⇒ identical children + mask flip; NO change to split() itself),
            # but broadcast the touched tensors from rank 0 + MAX-assert e_active so ANY future
            # nondeterminism in split() is caught HERE, not as a silent mid-run divergence.
            if ddp_on:
                moe = core_model.moe
                child = new_e - 1
                touched = (list(moe.experts[0].parameters())
                           + list(moe.experts[child].parameters())
                           + [moe.router.weight, moe.router.bias])
                for t in touched:
                    dist.broadcast(t.data, src=0)
                ea = torch.tensor([float(mito.e_active)], device=device)
                mx = ea.clone(); dist.all_reduce(mx, op=dist.ReduceOp.MAX)
                assert int(mx.item()) == mito.e_active, \
                    f"[ddp] mitosis e_active desync: local {mito.e_active} != max {int(mx.item())}"
        x, y = get_batch(step)
        # ── H_9841 N3/REM RECONSOLIDATION — rehearsed rows REPLACE fresh rows in place ──
        #    The batch shape, the optimizer step and the DDP graph are untouched; the ONE
        #    thing that changes is WHICH windows this step's gradient is spent on. The dose
        #    is ir_consolidation_gain, so with --vadapt-on-replay a rehearsal that caused no
        #    field growth replaces ZERO rows (the lane declines to re-train what taught the
        #    substrate nothing) — that is what makes the hook lesion a real control.
        if imag_lane is not None:
            for _b in range(x.shape[0]):
                imag_lane.observe(x[_b].tolist(), y[_b].tolist())
            if imag_lane.due(step):
                _budget = max(1, int(round(a.imagination_replay * x.shape[0])))
                _wins, _rec = imag_lane.reconsolidate(step, _budget)
                for _b, _w in enumerate(_wins):
                    if _b >= x.shape[0] or len(_w) != 2 * seq_len:
                        break                      # a short/stale ring entry is SKIPPED, never padded
                    x[_b] = torch.tensor(_w[:seq_len], dtype=x.dtype, device=x.device)
                    y[_b] = torch.tensor(_w[seq_len:], dtype=y.dtype, device=y.device)
                p0(f"  [imagination] step {step:5d} N3/REM  snaps={_rec['snapshots']} "
                   f"splits={_rec['splits']} cells={_rec['cells']} "
                   f"density={_rec['density']:.4f} consolidation={_rec['consolidation']:.4f} "
                   f"rows_replayed={_rec['rows_replayed']} "
                   f"eff_age={_rec['effective_age']:.3f}(monitor-only) "
                   f"emit_violations={_rec['emit_violations']}", flush=True)
        opt.zero_grad(set_to_none=True)
        # §4 one composite DDP forward() → (loss, detached shard-CE, aux). Backward runs at the
        # callsite OUTSIDE the shell's internal autocast; DDP's grad hooks fire here and
        # allreduce every param's grad (aux heads included — §10.1). clip_grad_norm_ runs AFTER
        # on the already-averaged grads, so every rank's clip scale = the 1-GPU global-grad norm.
        _sb = get_store_batch() if sb_cell is not None else None
        # H_9672 oracle-warmup 2-phase (val 분화 seed-robustness): the first --store-oracle-warmup steps
        # hand the address for free (oracle_slot) so val differentiates cleanly (Stage1.5 proved oracle-train
        # → ORACLE 1.00), THEN switch to the softmax address (+ --store-addr-weight L_addr learns W_q on the
        # now-differentiated val). Cuts the ∂L/∂v bootstrap deadlock that left val seed-fragile under addr-loss
        # alone (seed-7 lucky, seed-11 collapsed to op-only). warmup=0 → byte-identical to the prior behaviour.
        sb_oracle_now = a.store_oracle_train or (a.store_oracle_warmup > 0 and step <= a.store_oracle_warmup)
        # H_9692 RV-2 ans-delay: for the first --store-ans-delay steps train ONLY the address (addr-loss,
        # sb_w=0 → no ans-CE), so the blurry-v window can't corrupt the MLP before the address is sharp;
        # then add ans-CE (val learns on the now-sharp address). 0 → byte-identical.
        sb_w_now = 0.0 if (a.store_ans_delay > 0 and step <= a.store_ans_delay) else a.store_ans_weight
        loss, ce_local, aux = train_module(x, y, obj_gen, a.dict_lambda, a.jamo_lambda,
                                           sb=_sb, sb_w=sb_w_now, sb_oracle=sb_oracle_now,
                                           sb_addr_w=a.store_addr_weight, sb_oracle_aux=a.store_oracle_aux,
                                           sb_tap_grad=str(getattr(a, "store_query_tap_grad", "detached")),
                                           # H_9803 branch-latent ideation fan (None ⇒ byte-identical)
                                           idl=(get_ideation_batch() if idl_cell is not None else None),
                                           ans_w=a.answer_ce_weight,   # H_9811 (0.0 ⇒ term never evaluated)
                                           idl_w=a.ideation_weight, idl_assign=a.ideation_assign,
                                           idl_route=a.ideation_route, idl_tap_L=a.ideation_route_l,
                                           idl_gen=idl_gen)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
        # §3 CE all-reduce (AVG): per-rank ce_local is a shard statistic; average it so
        # loss0/lossF/logs equal the 1-GPU GLOBAL-batch CE (equal shard sizes ⇒ mean-of-means
        # = global mean). N==1: no collective — ce = the shard CE = the global CE.
        if ddp_on:
            ct = ce_local.clone()
            dist.all_reduce(ct, op=dist.ReduceOp.SUM); ct /= world
            ce = float(ct)
        else:
            ce = float(ce_local)
        last_aux = aux
        if loss0 is None: loss0 = ce
        lossF = ce
        do_val = a.val_every > 0 and (step == 1 or step % a.val_every == 0 or step == steps)
        # §1/§7 --ddp-verify-sync: at every val cadence, all-reduce a param-checksum (ALL ranks
        # participate — a collective) and assert cross-rank agreement, catching a split/optimizer
        # desync (especially the first val after split_step).
        if ddp_on and a.ddp_verify_sync and do_val:
            with torch.no_grad():
                cs = torch.zeros(1, device=device)
                for p in params:
                    cs += p.detach().float().sum()
            csx = cs.clone(); csn = cs.clone()
            dist.all_reduce(csx, op=dist.ReduceOp.MAX)
            dist.all_reduce(csn, op=dist.ReduceOp.MIN)
            assert float(csx - csn) < 1e-3, \
                f"[ddp] param-checksum desync at step {step}: spread {float(csx - csn)}"
        # §6 DBES/val/logs = rank-0-only diagnostics on the UNWRAPPED model (no collective inside,
        # so non-zero ranks skip and simply wait at the next step's forward/allreduce).
        if (not is_bytegpt) and a.dbes_every and (step % a.dbes_every == 0 or step == steps):
            if rank == 0:
                db = dbes_specialization(model, x); db["step"] = step
                dbes_log.append(db)
        # ── H_9845 INTERVENTIONAL CLOSURE MONITOR (rung 1) · ⛔ MONITOR-ONLY ──────────────
        #   Runs AFTER opt.step(), rank-0 only, on the UNWRAPPED core_model, under no_grad with
        #   the torch RNG state snapshotted+restored inside closure_monitor_rung1. Its return
        #   value is ONLY printed / appended to a JSONL — it is not read by the loss, the
        #   optimizer, the scheduler or any gate (a_train_inline_gauge). Wrapped in try/except
        #   because a diagnostic must never kill a run (train-py-1).
        if a.closure_monitor == "rung1" and rank == 0:
            _cm_due = (step == steps if a.closure_monitor_every <= 0
                       else (step % a.closure_monitor_every == 0 or step == steps))
            if _cm_due:
                try:
                    _cm = closure_monitor_rung1(
                        core_model, device, seq_len,
                        seed=a.closure_monitor_seed, ticks=a.closure_monitor_ticks,
                        schedules=a.closure_monitor_schedules, step=step,
                        brain_ckpt=a.closure_brain)
                    p0("  [H_9845 closure-monitor rung1 · MONITOR-ONLY · not in the loss] "
                       + json.dumps(_cm, ensure_ascii=False), flush=True)
                    if a.closure_monitor_out:
                        with open(a.closure_monitor_out, "a", encoding="utf-8") as _fh:
                            _fh.write(json.dumps(_cm, ensure_ascii=False) + "\n")
                except Exception as _e:
                    p0(f"  closure-monitor skipped: {type(_e).__name__}: {_e}", flush=True)
        # ── H_9846 structure-envelope tick (MONITOR-ONLY, rank-0, no_grad, no RNG) ───────
        #    `phi_mon_on` is False unless BOTH shipped controls certified before step 1, so an
        #    uncertified watch emits nothing at all rather than a number nobody may read.
        #    Wrapped: train-py-1 (a monitor-only tick with a device bug killed a whole run) —
        #    a watch that can abort training would be a lever, and this must never be one.
        if phi_mon_on and rank == 0 and (step == 1 or step % phi_mon_every == 0 or step == steps):
            try:
                tick = phi_envelope_tick(core_model, step)
                phi_mon_ticks.append(tick)
                p0(f"  [structure-envelope H_9846 MONITOR-ONLY] step={step} "
                   f"dispersion={tick['dispersion']:.6f} span={tick['span']:.6f} "
                   f"nest_sync={tick['nest_sync']:.6f} units={tick['n_units']}", flush=True)
            except Exception as e:                       # never let the watch kill the run
                p0(f"  [structure-envelope H_9846] tick error at step {step}: {e}", flush=True)
                phi_mon_on = False
        if step == 1 or step % a.log_every == 0 or step == steps:
            vtxt = ""
            ptxt = ""
            if do_val and rank == 0:
                per = val_per_cell()
                vc = (sum(per.values()) / len(per)) if per else float("nan")
                vtxt = f"  val_CE={vc:.5f}"
                # ⑤ per-cell CE dict (ko/en × general/sns) — MONITOR-ONLY, additive log of
                # the already-tracked per-register held-out CE. NEVER enters the loss
                # (a_train_inline_gauge · p7 NO PERPLEXITY VERDICT); decomposes the pooled
                # val_CE above so per-cell descent is visible per (a_chat_registers) cell.
                if per:
                    ptxt = "  per_cell_CE=" + json.dumps(
                        {k: round(v, 5) for k, v in per.items()})
            atxt = (" " + json.dumps({k: round(v, 4) for k, v in aux.items()})) if aux else ""
            p0(f"  step {step:5d}  CE={ce:.5f}  E={e_now()}  lr={step_lr:.8g}  "
               f"wd={wd:.4f} dp={dp:.4f}{vtxt}{ptxt}{atxt}", flush=True)
    wall = time.time() - t0
    # H_9840 — freeze the realized schedule counts HERE, before the DBES probe calls get_batch()
    # once more: a monitor probe must not appear in the training-step census.
    slp_final = dict(slp_stats) if slp_stats is not None else None
    if slp_final is not None:
        p0(f"  sleep-schedule realized: wake={slp_final['wake_steps']} "
           f"sleep={slp_final['sleep_steps']} "
           f"(sleep_ratio={slp_final['sleep_steps'] / max(1, steps):.4f}) "
           f"replay_batches={slp_final['replay_batches']} "
           f"warmup_fresh={slp_final['warmup_fresh']}", flush=True)
    # H_9841: the lane's OWN telemetry, printed before any verdict is read off this run
    # (train-py-9: a new loss/data term whose telemetry goes unread gets misread as "no lever").
    if imag_lane is not None:
        p0("  [imagination] H_9841 lane summary: "
           + json.dumps(imag_lane.summary(), ensure_ascii=False), flush=True)
        if imag_lane.emit_violations == 0:
            p0("  [imagination] p5 invariant HELD for all %d replay tick(s): emit_count==0"
               % imag_lane.n_ticks, flush=True)
        else:
            p0("  [imagination] ⛔ p5 INVARIANT BROKEN — %d emitting replay tick(s)"
               % imag_lane.emit_violations, flush=True)

    # ══ §6 FINALIZE — held-out val / DBES / gauges / ckpt / summary / serialize are ALL
    #    RANK-0-ONLY on the UNWRAPPED core_model (`model`). A non-zero rank writing files =
    #    double-write corruption; val_gen must advance only on rank 0 so its stream matches
    #    the 1-GPU run (the DESCENT-gate comparability contract, §10.6). Non-zero ranks skip
    #    straight to the barrier + destroy_process_group. N==1: rank==0, so this all runs.
    if rank == 0:
        # ── FINAL held-out val per register (DESCENT gate, plain CE) ──────────────
        uniform = math.log(V)
        per = val_per_cell()
        descent = {}; n_desc = 0
        print(f"  ── FINAL held-out val-CE per register (uniform={uniform:.4f}) ──", flush=True)
        for lab, vc in per.items():
            ok = vc < uniform; n_desc += int(ok)
            descent[lab] = {"val_ce": round(vc, 5), "descent": ok}
            print(f"     {lab:<12s} val_CE={vc:.5f}  {'DESCENT' if ok else 'NO-DESCENT'}", flush=True)
        final_val = (sum(per.values()) / len(per)) if per else None
        print(f"  FINAL val_CE(macro_cells)={final_val}  registers_DESCENT={n_desc}/{len(per)}", flush=True)
        if getattr(shell, "comp_lane", None) is not None and a.comp_probe_panel:
            # H_9904 — DIRECTIONAL lane readout (see comp_lane_heldout). Printed, never cemented.
            _lp = comp_lane_heldout(shell, a.comp_probe_panel, device)
            if _lp is not None:
                print("  comp-lane HELD-OUT (DIRECTIONAL · teacher-forced · not a verdict): "
                      "byte_acc=%.4f over %d bytes" % (_lp["byte_acc"], _lp["bytes"]), flush=True)
        print(f"  loss0={loss0:.5f} lossF={lossF:.5f} wall={wall:.1f}s "
              f"savant_latched_at={latch['at']} E0={e0}->E={e_now()}", flush=True)

        # ── N3 DBES final diagnostic (gradient-free, measure-only) ────────────────
        #   DBES probes MoE expert differentiation — CLM-only (no experts in ByteGPT).
        dbes_final = None
        if not is_bytegpt:
            try:
                xb, _ = get_batch(steps + 1)
                dbes_final = dbes_specialization(model, xb)
                print(f"  [N3 DBES expert-specialization] {json.dumps(dbes_final, ensure_ascii=False)}", flush=True)
            except Exception as e:
                print(f"  DBES error: {e}", flush=True)

        # ── ρ·weave/ρ·fan (former G1/G6) torch-probe gauges (DIRECTIONAL, a_train_inline_gauge) ──
        #   gauge_lib.compute_inline_gauges decodes via the CLM mouth (CLMConvMoE-specific);
        #   skip for bytegpt (the terminal verdict is `anima-py evaluate <.bin>` engine-native
        #   through the bytegpt mouth anyway — this torch probe is DIRECTIONAL only).
        gauges = None
        if not is_bytegpt and not a.skip_inline_rho:
            try:
                import gauge_lib
                was = model.training; model.eval()
                gauges = gauge_lib.compute_inline_gauges(
                    model, None, seeds=7, corpus_index=[c.path for c in cells],
                    ce=lossF, step=steps, torch=torch)
                if was: model.train()
                print(f"  [ρ·weave/ρ·fan (G1/G6) torch-probe DIRECTIONAL] {json.dumps(gauges, ensure_ascii=False)}", flush=True)
            except Exception as e:
                print(f"  gauges error: {e}", flush=True)

        # ── H_9846 structure-envelope headline (MONITOR-ONLY, never a verdict) ────
        #    `cliff_gap` is the largest tick-to-tick jump in parameter-structure dispersion —
        #    the safety-net read. A cliff is a REGRESSION signal even if every capability
        #    number went up; it is not, and can never be, a capability score.
        if phi_mon_battery is not None and phi_mon_battery.get("certified") and phi_mon_ticks:
            _pm = PEM.summarize(phi_mon_ticks, phi_mon_every, phi_mon_battery)
            print(f"  [structure-envelope H_9846 MONITOR-ONLY] n_ticks={_pm['n_ticks']} "
                  f"every={_pm['every']} cliff_gap={_pm['cliff']['cliff_gap']:.6f} "
                  f"cliff_rate={_pm['cliff']['cliff_rate']:.8f} "
                  f"dispersion {phi_mon_ticks[0]['dispersion']:.6f} → "
                  f"{phi_mon_ticks[-1]['dispersion']:.6f} · self-subsample spread "
                  f"{_pm['cliff_gap_spread_rel']:.4f} ⇒ {_pm['regime']}", flush=True)

        # ── persist torch ckpt (ALWAYS — a_fire_recover_complete) ────────────────
        # "ALWAYS" used to mean "if you remembered to pass --ckpt-out". It now means always: the
        # .clm is int4, and a fine-tune whose updates are smaller than the quant step does not
        # survive serialization at all (convergence serialize-py-1, measured in H_9313). Without a
        # .pt beside it there is no way to even SEE that, let alone recover the run.
        if a.ckpt_out:
            _write_pt(a.ckpt_out, steps)
        elif a.out:
            _write_pt(f"{a.out}.pt", steps)

        # ── QUANT-SWALLOW guard (serialize-py-1) ─────────────────────────────────
        # The failure this catches is silent and it cost H_9313 a full 4-run battery: training
        # descends beautifully (CE 1.04 -> 0.16), the .clm changes sha, decodes coherently, obeys
        # the template — and scores its OWN training lines at chance, because every weight update
        # was smaller than half an int4 step and `round(w/scale)` erased all of it.
        #
        # So: if we warm-started, compare what we learned against the grid we must survive. This is
        # a WARNING, not a hard error — a large from-scratch run legitimately moves far past the
        # step, and a legitimately tiny update (a probe, a 1-step smoke) is not a bug. What is a bug
        # is finding out AFTER the measurement.
        if a.init and a.out and rank == 0:
            try:
                import numpy as _np
                base = S.deserialize_v3(a.init, L, emax) if a.init.lower().endswith(".clm") else None
                if base is not None:
                    now = {k: v.detach().cpu().numpy() for k, v in core_model.state_dict().items()}
                    worst = 0.0
                    for k, b in base.items():
                        if k not in now or now[k].shape != b.shape:
                            continue
                        step_q = float(_np.abs(b).max()) / 7.0          # int4-sym: amax/7
                        if step_q <= 0:
                            continue
                        frac = float((_np.abs(now[k] - b) > step_q / 2).mean())
                        worst = max(worst, frac)
                    if worst < 0.01:
                        print("  ⚠️  QUANT-SWALLOW WARNING (serialize-py-1): only %.2f%% of weights "
                              "moved past half an int4 step — this fine-tune will NOT survive .clm "
                              "serialization. The .clm you are about to evaluate is, for practical "
                              "purposes, the model you started from. Evaluate the .pt, raise lr/"
                              "steps, or use a non-quantized export." % (100 * worst), flush=True)
                    else:
                        print("  quant-swallow check: %.1f%% of weights moved past half an int4 "
                              "step (update survives serialization)" % (100 * worst), flush=True)
            except Exception as e:
                print(f"  quant-swallow check skipped: {e}", flush=True)

        # ── summary json ──────────────────────────────────────────────────────────
        summary = {"entry": "anima-py train", "arch": a.arch, "arm": a.arm,
                   "objective": a.objective, "seed": a.seed,
                   "optimizer": {"name": "AdamW", "beta1": 0.9,
                                 "beta2": a.adam_beta2,
                                 "weight_decay": a.weight_decay,
                                 "lr": a.lr, "schedule": a.lr_schedule,
                                 "warmup_steps": a.warmup_steps,
                                 "decay_steps": lr_decay_steps,
                                 "min_lr_ratio": a.min_lr_ratio},
                   "initialization": ({"name": "gpt2-canonical",
                                       "std": bg_cfg.init_std,
                                       "residual_projection_scale": "std/sqrt(2*n_layer)"}
                                      if is_bytegpt else None),
                   "ddp": {"world_size": world, "global_batch": B_global,
                           "per_rank_batch": B_local, "gpus": a.gpus},
                   "obj_aux_params": (sum(p.numel() for p in objfn.parameters())
                                      if obj_is_module else 0),
                   "levers": {"tlora": tlora_on, "tlora_rank": a.tlora_rank,
                              "tlora_base": not a.tlora_no_base, "dict_aux": dict_on,
                              "jamo_aux": jamo_on, "wd_floor": a.wd_floor,
                              "dropout_floor": a.dropout_floor},
                   "n_params": n_params, "loss0": round(loss0, 5), "lossF": round(lossF, 5),
                   "wall_s": round(wall, 1), "uniform_ce": round(uniform, 5),
                   # Compatibility alias retained for old readers. The value has always been
                   # an equal-cell macro average, never a sample-count-pooled CE.
                   "final_val_ce_pooled": (round(final_val, 5) if final_val is not None else None),
                   "final_val_ce_macro_cells": (round(final_val, 5)
                                                if final_val is not None else None),
                   "validation_aggregation": "equal-cell macro average",
                   "registers_descent": f"{n_desc}/{len(per)}", "heldout_descent": descent,
                   "last_aux": last_aux, "dbes_final": dbes_final, "dbes_log": dbes_log,
                   # §4 diagnostic honesty: under DDP the rank-0 DBES probe runs on a rank-LOCAL
                   # shard (B_local=B/N), NOT the global batch B, so dbes_final/dbes_log are NOT
                   # numerically 1:1 comparable with a 1-GPU record (which used full B). Label the
                   # input scope explicitly (DBES is MONITOR-ONLY/DIRECTIONAL, excluded from the
                   # DESCENT gate + engine-native verdict, so this does not corrupt the verdict).
                   "dbes_batch_scope": (f"per_rank_shard(B_local={B_local})" if world > 1
                                        else f"full_batch(B={B_global})"),
                   "gauges_g1g6_torch_probe": gauges,
                   # H_9840 — None when the lane is off (nothing was scheduled and nothing replayed).
                   "sleep_schedule": slp_final,
                   # H_9846 — the structure-envelope watch's own record, battery included, so
                   # the run's cliff read is re-auditable by someone who was not in the session.
                   # null when the flag was off; status-only (no values) when uncertified.
                   "phi_envelope_monitor": (PEM.summarize(phi_mon_ticks, phi_mon_every,
                                                          phi_mon_battery)
                                            if phi_mon_battery is not None else None),
                   "tier": ("engine-native-eligible (.bin ByteGPT via bytegpt mouth); torch probe DIRECTIONAL"
                            if is_bytegpt else
                            "engine-native-eligible (.clm additive, TLoRA materialized); torch probe DIRECTIONAL")}
        if a.gauges_out:
            with open(a.gauges_out, "w") as f:
                json.dump(summary, f, ensure_ascii=False, indent=2)
            print(f"  summary -> {a.gauges_out}", flush=True)

        # ── serialize the trained ckpt: CLM → .clm v0.3 (additive readout + MATERIALIZED
        #    experts) | ByteGPT → .bin (5×u32 header via core/serialize.py). ──
        if a.out:
            _write_clm(a.out)  # final full-run checkpoint (same helper as --ckpt-every)

    # §6 barrier so no rank tears down while rank 0 serializes the 303M .clm, then release NCCL.
    if ddp_on:
        dist.barrier()
        dist.destroy_process_group()


if __name__ == "__main__":
    main()
