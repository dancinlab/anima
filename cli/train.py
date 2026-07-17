#!/usr/bin/env python3
"""cli/train.py — the CANONICAL anima python training entry (`anima-py train`).

>>> This file is the working python training entry, SYMMETRIC to cli/evaluate.py
>>> (the canonical python eval entry). `anima-py train <args>` (pip channel) dispatches HERE;
>>> hexa `anima train <args>` dispatches to the hexa-native cli/train.hexa.
>>>
>>> WHY python is the canonical working path RIGHT NOW: the hexa-native production
>>> trainer cli/train.hexa (a_train_flame_forge) is single-thread native-CPU-scalar-
>>> bound (#2598/#2600: util peak ~65% / sustained <30%) and is temporarily under a
>>> GPU-utilization fix, so a real 303M GPU train on it idles the GPU. This torch
>>> Lane-P path is GPU-BOUND (cuda GEMM-saturating), so it trains the real clm303
>>> (L4·d3784·E2->Emax4) efficiently today — the explicitly-sanctioned REFERENCE +
>>> BRIDGE path (a_clm_gen_pipeline: "Lane-P torch = REFERENCE + bridge, forge is the
>>> PUBLIC production trainer"). It trains a CLMConvMoE GPU-bound, then SERIALIZES to
>>> a .clm v0.3 (CLM\\x01 magic + CLMX trailer) that CORE core/clm_decode.hexa loads
>>> back byte-exact for the engine-native ρ-AXON reach verdict (former G0-G6).
>>>
>>>   ENGINE-NATIVE GATE (a_engine_native_learning, HARD-GATE): torch-side CE / gauges
>>>   here = DIRECTIONAL only (NOT terminal). TERMINAL verdict = CORE re-measure of the
>>>   serialized .clm via `anima-py evaluate <clm>` on the frozen ρ-AXON reach bars (former G0-G6). Pull the
>>>   trained ckpt before teardown (a_fire_recover_complete) so engine-check is possible.

This trainer carries the full SAVANT + MITOSIS recipe (parity with cli/train.hexa) AND
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

USAGE (installed `anima` PATH command after `hx install anima`):
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
import argparse, json, math, os, sys, time
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
        if _c not in sys.path:
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
import verify_clm_v2 as VC                            # core/verify_clm_v2.py — clm_decodable / descent
# ByteGPT .pt -> .bin serializer is folded into the SAME unified core/serialize.py.
import serialize as BGS                               # core/serialize.py — serialize(pt_path, bin_path)


# ════════════════════════════════════════════════════════════════════════════
#  golden-zone constants (SAVANT/savant_lib.hexa H_347/348, verbatim — same as
#  cli/train.hexa gz_lower()/gz_upper()).
# ════════════════════════════════════════════════════════════════════════════
GZ_LOWER = 0.21231792755821914   # 1/2 - ln(4/3)  (sa_gz_lower)
GZ_UPPER = 0.5                    # sa_gz_upper
LN2 = 0.6931471805599453


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

    The TAIL `val_frac` of the file is reserved as a held-out validation region
    DISJOINT from the train region (overfit detector, a_savant_train held-out
    monitor). Train windows are sampled only from [0, train_end); val windows
    only from [train_end, size). A window can NEVER straddle the boundary
    (start ranges are clamped to keep start+seq_len+1 within the region), so the
    val region's bytes are never seen by a training gradient step."""

    def __init__(self, path: str, val_frac: float = 0.0):
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
        self.train_end = int(self.size * (1.0 - vf)) if self.size > 0 else 0

    def _window_in(self, lo: int, hi_excl: int, seq_len: int,
                   gen: torch.Generator):
        """Sample one (x,y) window whose [start, start+seq_len+1) lies entirely
        inside the byte range [lo, hi_excl). Returns None if the range is too
        small for even one window."""
        if hi_excl - lo < seq_len + 2:
            return None
        hi = hi_excl - seq_len - 1            # last valid start (exclusive upper bound)
        start = int(torch.randint(lo, hi, (1,), generator=gen).item())
        chunk = self._mm[start:start + seq_len + 1]
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
        """A held-out VAL window — sampled only from [train_end, size)."""
        return self._window_in(self.train_end, self.size, seq_len, gen)



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
    * else treat as an HF dataset id (a_chat_registers names like
      'anima-corpus-5lang-unified-v2', 'anima-corpus-ko-fineweb2-broad',
      'anima-persona-sns-corpus') and stream it to a local cached byte file
      under $ANIMA_CORPUS_CACHE (default ./.corpus_cache) via `datasets`; the
      text column is concatenated UTF-8 -> raw bytes (V=256).
    """
    if os.path.exists(spec):
        return spec
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


# NOTE (H_1640): every objective now accepts an OPTIONAL penultimate=(B,d,T) kwarg
# (the post-MoE pre-readout trunk site). The inherited objectives ignore it; the new
# compositional objectives consume it. Plain-function objectives have no params; the
# two aux-head objectives are nn.Modules whose params are added to the optimizer in
# main() and DROPPED at serialize (they never enter model.state_dict).
def loss_ce_marginal(logits, targets, V, gen, penultimate=None):
    return _ce(logits, targets, V), {}


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
        sd = {k: torch.from_numpy(v) for k, v in S.deserialize_v3(init_path, L, E).items()}
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
        return (f"warm-start ✓ .clm int4-dequant loaded {len(loadable)}/{len(model_sd)} keys "
                f"(L={L} E={E} · round-trip BYTE-IDENTICAL · untouched={len(missing)})")

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
        return (f"warm-start ✓ ByteGPT .bin loaded ({cfg['n_layer']}L d={cfg['d']} "
                f"block={cfg['block']}) missing={list(missing)} unexpected={list(unexpected)}")

    if low.endswith(".pt") or low.endswith(".pth"):
        ck = torch.load(init_path, map_location="cpu", weights_only=False)
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
        return (f"warm-start ✓ .pt loaded {len(loadable)}/{len(model_sd)} keys "
                f"(untouched={len(missing)} extra-in-ckpt={len(sd) - len(loadable)})")

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

    def forward(self, x, y, obj_gen, dict_lambda, jamo_lambda, sb=None, sb_w=1.0, sb_oracle=False, sb_addr_w=0.0, sb_oracle_aux=0.0):
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
            x_s, y_s, K, pols, tgt = sb
            out_s = model(x_s)                                  # (targets None → CE assembled here, fp32)
            logits_s = out_s["logits"].float()                 # (Bs, V, T)
            pen_s = out_s["pen_trunk"].float()                 # (Bs, d, T) pre-slot trunk penultimate
            Bs, _, Ts = logits_s.shape
            yn_q = pen_s[:, :, Ts - 1]                         # (Bs, d) query row (qpos = T-1, cell-asserted)
            # H_9423 Stage1.5 --store-oracle-train: hand the address for free at TRAIN time (oracle_slot=
            # target_slot) so ∂L/∂v is not gated on the softmax lookup bootstrapping first. Separates the
            # value-read layer (a) from the address-learning layer (c): if val differentiates under free
            # address (ORACLE≥.90) the residual 303M wall is pure W_q address-learning; if not, deeper.
            osl = tgt if sb_oracle else None
            store_logits, att = model.clms(yn_q, K, pols, oracle_slot=osl, need_att=True)   # (Bs,V),(Bs,n_slot)
            ce_ans = F.cross_entropy(store_logits, y_s[:, Ts - 1])
            # non-answer trunk CE (prompt spelling): every row but qpos, standard next-byte LM.
            ce_tok = F.cross_entropy(logits_s[:, :, :Ts - 1].transpose(1, 2).reshape(-1, V),
                                     y_s[:, :Ts - 1].reshape(-1))
            loss = loss + ce_tok + sb_w * ce_ans + out_s["aux_loss"]
            aux["sb_ans_ce"] = float(ce_ans.detach()); aux["sb_tok_ce"] = float(ce_tok.detach())
            # H_9672 addr-loss: direct supervision of the softmax address (att) → cut the (2) bootstrap
            # deadlock W_q could not escape at 303M (Stage1.5 proof). OBJECTIVE (loss term, sb_addr_acc is
            # the monitor). tgt = the 5-tuple target_slot. sb_addr_w=0 (default) → byte-identical.
            if sb_addr_w > 0.0:
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
                store_logits_orc = model.clms(yn_q, K, pols, oracle_slot=tgt)
                ce_orc = F.cross_entropy(store_logits_orc, y_s[:, Ts - 1])
                loss = loss + sb_oracle_aux * ce_orc
                aux["sb_orc_ce"] = float(ce_orc.detach())
            with torch.no_grad():
                aux["sb_addr_acc"] = float((att.argmax(-1) == tgt).float().mean())   # monitor-only
            with torch.no_grad():                              # monitor-only (a_train_inline_gauge)
                g_id, b_id = 103, 98                           # ord('g'), ord('b') — eval store_run binary
                gold_g = (y_s[:, Ts - 1] == g_id)
                aux["sb_store_acc"] = float(((store_logits[:, g_id] >= store_logits[:, b_id]) == gold_g).float().mean())
                tr = logits_s[:, :, Ts - 1]                    # trunk row at qpos — leak early-warning
                aux["sb_trunk_leak"] = float(((tr[:, g_id] >= tr[:, b_id]) == gold_g).float().mean())
                aux["sb_lam"] = float(model.clms.lam)
        aux.update(oaux)
        return loss, out["ce_loss"].detach(), aux


class StoreBindCell:
    """H_9423 S1 — line-aligned storebind dataset (NOT a ByteCell). c.txt line i <-> c.txt.store.jsonl
    row i (corpus.build_storebind lockstep). Fixed-T single-line prompt-aligned windows that MIRROR
    evaluate.store_run's _seed_to_tok geometry (qpos = T-1): left-pad with spaces, prompt then the first
    answer byte. The answer tail spelling ("ood"/"ad") is not in the window (binary readout needs only
    the first byte at qpos), and in-window copy is structurally impossible (the answer byte does not
    exist before qpos, and each window is exactly one line)."""

    def __init__(self, path, key_emb_np, n_slot, T, val_frac):
        import json as _json
        import numpy as np           # train.py imports numpy only locally (as _np); StoreBindCell needs np
        lines = open(path, encoding="ascii").read().splitlines()
        rows = [_json.loads(l) for l in open(path + ".store.jsonl", encoding="utf-8")]
        if len(lines) != len(rows):
            sys.exit(f"[store-bridge] {path}: {len(lines)} lines != {len(rows)} store rows (lockstep broken)")
        from clms import find_qpos as _fq             # core/clms.py — the SAME scanner eval uses
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
            K = np.stack([key_emb_np[np.frombuffer(e.encode("ascii"), np.uint8)].mean(0)
                          for e in ents]).astype(np.float32)          # (n_slot, d_k) = clms._entity_key
            tgt = int(r["target_slot"])                              # H_9423 Stage1.5: query-entity slot (oracle-train)
            self.ex.append((x, y, torch.from_numpy(K), torch.tensor(pols, dtype=torch.long),
                            torch.tensor(tgt, dtype=torch.long)))
        n_blocks = len(self.ex) // n_slot
        vb = max(1, int(n_blocks * val_frac))
        self.train_n = max(n_slot, (n_blocks - vb) * n_slot)          # [0,train_n) train · rest val


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
    ap.add_argument("--dict-lambda", type=float, default=DICT_LAMBDA)
    ap.add_argument("--jamo-lambda", type=float, default=JAMO_LAMBDA)
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
    ap.add_argument("--clms-key-seed", type=int, default=9423, help="CLMS frozen key_emb table seed")
    ap.add_argument("--clms-lam0", type=float, default=1.0, help="CLMS lam init (store_only scale)")
    ap.add_argument("--freeze-trunk", action="store_true",
                    help="BOLT control arm: trunk requires_grad=False, only clms.* trains")
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
    ap.add_argument("--val-frac", type=float, default=0.05)
    ap.add_argument("--val-every", type=int, default=200)
    ap.add_argument("--val-batches", type=int, default=4)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--dbes-every", type=int, default=0, help="0=final only; N=also every N steps")
    ap.add_argument("--ckpt-every", type=int, default=0,
                    help="0=final .clm only; N=every N steps dump <out>.step<N>.clm "
                         "(step-window multiplex — 1 run yields 2000/4000/… checkpoints, "
                         "train-py-4 isolation) AND a rolling <out>.resume.pt. The .clm is "
                         "quantized and --init refuses it, so the .pt is what makes a killed "
                         "long run restartable: `--init <out>.resume.pt`. Set this on any "
                         "multi-hour fire (train-py-7).")
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
    ap.add_argument("--ddp-verify-sync", action="store_true",
                    help="DDP debug: every --val-every steps all-reduce a param-checksum and "
                         "assert cross-rank agreement (catches a mitosis/optimizer desync at "
                         "the split). Off by default (costs one collective per val).")
    ap.add_argument("--ddp-find-unused", action="store_true",
                    help="DDP debug/escape-hatch: pass find_unused_parameters=True to DDP. Off "
                         "by default — the current objective set fires every head every step "
                         "(§4). Flip ON only if a FUTURE per-step-gated head makes DDP error on "
                         "an unused param.")
    a = ap.parse_args()

    # ══ §7 DDP launch: torchrun self-re-exec + worker init + N==1 short-circuit ══
    #   Runs FIRST (before any CUDA allocation). os.execvpe replaces the process, so the
    #   launcher's `> rf 2>&1` redirect is inherited and only rank 0 prints via p0().
    gpu_ids = [g for g in a.gpus.split(",") if g.strip() != ""]
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
    V, K = 256, 3
    # §7 device: under DDP each rank pins its own cuda:local_rank; N==1 = today's path.
    if ddp_on:
        device = f"cuda:{local_rank}"
    else:
        device = "cuda" if torch.cuda.is_available() else "cpu"
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

    torch.manual_seed(a.seed)

    if is_bytegpt:
        # ByteGPT block = the context window; use seq_len as the positional block size so a
        # non-canon toy stays small. n_head must divide d (validated by the config).
        bg_block = seq_len
        bg_cfg = ByteGPTConfig(vocab=V, d=d, n_layer=L, n_head=bg_n_head, block=bg_block)
        model = ByteGPT(bg_cfg).to(device)
        cfg = None
        jamo_head = None
        mito = None                                 # no MoE experts to grow
    else:
        cfg = CLMConfig(n_experts=emax, n_trunk_layers=L, d_model=d, kernel_size=K,
                        variant="AB", dilation_base=2, max_dilation=512,
                        slw=a.slw, slw_n_slot=a.slw_n_slot, slw_k=a.slw_k,
                        clms=bool(a.store_bridge or a.freeze_trunk),
                        clms_n_slot=a.clms_n_slot, clms_d_k=a.clms_d_k,
                        clms_d_s=a.clms_d_s, clms_r=a.clms_r, clms_d_g=a.clms_d_g, clms_val_center=a.store_val_center, clms_fangate=a.store_fangate,
                        clms_key_seed=a.clms_key_seed, clms_lam0=a.clms_lam0)
        model = CLMConvMoE(cfg).to(device)          # production additive readout (all arms)
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
    if a.init:
        expect_cfg = ({"vocab": V, "d": d, "n_layer": L, "n_head": bg_n_head, "block": seq_len}
                      if is_bytegpt else {"d": d, "L": L, "E": emax})
        report = _warm_start(model, a.init, is_bytegpt, expect_cfg)
        model.to(device)
        p0(f"  [--init] {report}", flush=True)

    params = (list(model.parameters())
              + (list(jamo_head.parameters()) if jamo_head else [])
              + (list(objfn.parameters()) if obj_is_module else []))   # H_1640 aux-head params
    if obj_is_module:
        n_obj = sum(p.numel() for p in objfn.parameters())
        p0(f"  objective '{a.objective}' aux params: {n_obj} "
           f"(DROPPED at serialize — not in model.state_dict)", flush=True)
    opt = torch.optim.AdamW(params, lr=a.lr, betas=(0.9, 0.999), eps=1e-8, weight_decay=0.0)

    # ══ §4 TrainShell + DDP wrap (execution strategy — the recipe is unchanged) ═════
    #   core_model = the UNWRAPPED inner model, used for ALL rank-0 probes/serialize
    #   (dbes/gauges/val/materialize/_write_clm) — never through the DDP wrapper (§4/§6/§10.9).
    core_model = model
    shell = TrainShell(model, objfn, jamo_head, is_bytegpt=is_bytegpt, V=V,
                       obj_needs_pen=obj_needs_pen, dict_on=dict_on, jamo_on=jamo_on,
                       bf16=a.bf16, device=device)
    # §10.1 defense — the shell's param set MUST equal the optimizer's (aux heads covered).
    assert {id(p) for p in shell.parameters()} == {id(p) for p in params}, \
        "TrainShell params != optimizer params — an aux head would never be allreduced."
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
    cells, labels = [], []
    for ci, spec in enumerate(a.corpus):
        p = resolve_corpus_path(spec)
        cells.append(ByteCell(p, val_frac=a.val_frac))
        labels.append(a.cell_label[ci] if ci < len(a.cell_label) else f"cell{ci}")
        c = cells[-1]
        p0(f"  corpus cell[{ci}] {labels[ci]:<12s} {p} size={c.size} "
           f"train={c.train_end} val_tail={c.size - c.train_end}", flush=True)
    if not cells:
        p0("  corpus: NONE -> synthetic smoke", flush=True)

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
        sb_cell = StoreBindCell(a.store_bridge, _key, a.clms_n_slot, a.store_win, a.store_val_frac)
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
        xs, ys, Ks, Ps, Ts_ = zip(*[sb_cell.ex[i] for i in sl])
        return (torch.stack(xs).to(device), torch.stack(ys).to(device),
                torch.stack(Ks).to(device), torch.stack(Ps).to(device),
                torch.stack(Ts_).to(device))                          # H_9423 Stage1.5 target_slot

    def get_batch(step):
        if cells:
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
        if c.size - c.train_end < seq_len + 2:
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
        # write the torch .pt in the exact shape bytegpt_serialize.serialize reads, next to
        # the .bin, then bridge it. The aux-head objective params are OUTSIDE model.state_dict
        # (they live on objfn), so serialize sees only the standard ByteGPT weights.
        pt_path = out_path + ".pt" if not out_path.endswith(".pt") else out_path
        bin_path = out_path
        sd = {k: v.detach().cpu() for k, v in model.state_dict().items()}
        ck = {"model": sd, "config": model.cfg.as_dict(),
              "val_ce": (round(lossF, 5) if lossF is not None else None),
              "step": steps, "nparam": n_params}
        torch.save(ck, pt_path)
        BGS.serialize(pt_path, bin_path)
        print(f"  .bin WRITTEN {os.path.getsize(bin_path)} bytes -> {bin_path} "
              f"(via {pt_path})", flush=True)

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
        S.serialize_v3(sd_active, n_trunk_layers=L, n_experts=e_ser, out_path=out_path)
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
        print(f"  .clm WRITTEN {os.path.getsize(out_path)} bytes -> {out_path}", flush=True)
        print(f"  clm_decodable={VC.clm_decodable(open(out_path, 'rb').read())}", flush=True)

    # ── torch .pt writer (RESUMABLE — the .clm is quantized and --init refuses it) ──
    #   --ckpt-every writes BOTH: the .clm (evaluatable) and this .pt (warm-startable).
    #   Without the .pt an interrupted long run is unrecoverable — a killed 13h fire
    #   restarts from step 0 (N2 2026-07-13: 17h of GPU lost across two kills, one to a
    #   pod stop that wiped /workspace, one to earlyoom).
    def _write_pt(out_path):
        sd = {k: v.detach().cpu() for k, v in core_model.state_dict().items()}
        if jamo_head:
            for k, v in jamo_head.state_dict().items():
                sd[f"_jamo_head.{k}"] = v.detach().cpu()
        torch.save(sd, out_path)
        print(f"  torch ckpt -> {out_path} ({os.path.getsize(out_path)} bytes · "
              f"resume with --init)", flush=True)

    # ── train loop ───────────────────────────────────────────────────────────
    model.train()
    t0 = time.time(); loss0 = lossF = None
    last_aux = {}; dbes_log = []
    # active-expert count for logs/summary — CLM tracks it on the mitosis controller;
    # ByteGPT has no experts (mito is None) so it is a fixed 1.
    def e_now():
        return mito.e_active if mito is not None else 1
    # intermediate-ckpt extension: bytegpt writes .bin, clm writes .clm.
    _ck_ext = ".bin" if is_bytegpt else ".clm"
    for step in range(1, steps + 1):
        # --ckpt-every: dump an intermediate ckpt of the state AFTER (step-1) updates
        # (step-window multiplex — one run yields 2000/4000/… checkpoints, no re-train).
        # §6 rank-0-only intermediate serialize on the UNWRAPPED core_model; barrier AFTER the
        # write (nothing to protect before) so non-zero ranks don't race into the next step's
        # collective while rank 0 serializes a 303M .clm.
        if a.ckpt_every > 0 and a.out and step > 1 and (step - 1) % a.ckpt_every == 0:
            if rank == 0:
                _write_clm(f"{a.out}.step{step - 1}{_ck_ext}")
                # …and the RESUMABLE twin: the .clm above is quantized and --init refuses
                # it, so a .clm-only intermediate cannot restart a killed run. Overwrite a
                # single rolling .pt (not per-step) — 13h of GPU is worth ~1.4GB on disk.
                _write_pt(f"{a.out}.resume.pt")
                model.train()
            if ddp_on:
                dist.barrier()
        if savant_on:
            inh = savant_inhibition(step, steps, i0, i_floor, latch)
            wd = inhibition_to_wd(inh); dp = inhibition_to_dropout(inh)
        else:
            wd, dp = 0.0, 0.0
        if a.wd_floor >= 0.0: wd = a.wd_floor             # N6 sweep override
        if a.dropout_floor >= 0.0: dp = a.dropout_floor   # N6 sweep override
        for grp in opt.param_groups:
            grp["weight_decay"] = wd
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
                                           sb_addr_w=a.store_addr_weight, sb_oracle_aux=a.store_oracle_aux)
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
            p0(f"  step {step:5d}  CE={ce:.5f}  E={e_now()}  "
               f"wd={wd:.4f} dp={dp:.4f}{vtxt}{ptxt}{atxt}", flush=True)
    wall = time.time() - t0

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
        print(f"  FINAL val_CE(pooled)={final_val}  registers_DESCENT={n_desc}/{len(per)}", flush=True)
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
        if not is_bytegpt:
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

        # ── persist torch ckpt (ALWAYS — a_fire_recover_complete) ────────────────
        # "ALWAYS" used to mean "if you remembered to pass --ckpt-out". It now means always: the
        # .clm is int4, and a fine-tune whose updates are smaller than the quant step does not
        # survive serialization at all (convergence serialize-py-1, measured in H_9313). Without a
        # .pt beside it there is no way to even SEE that, let alone recover the run.
        if a.ckpt_out:
            _write_pt(a.ckpt_out)
        elif a.out:
            _write_pt(f"{a.out}.pt")

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
                   "final_val_ce_pooled": (round(final_val, 5) if final_val else None),
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
