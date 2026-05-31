#!/usr/bin/env python3
"""CLM P2 custom QAT trainer — "training toward AKIDA".

This is the REAL CLM training payload (NOT the dojo HF-Trainer template).
It is deliberately custom for CLM and does NOT use any of:
    AutoModelForCausalLM / AutoTokenizer / wikitext / DataCollator
because CLM is a from-scratch conv-MoE byte LM (V=256, no tokenizer) trained
with quantization-aware-training (QAT) against the AKIDA int4 deployment
envelope (CLM/P0_ARCHITECTURE.md §9, CLM/CLM_FORMAT_SPEC.md §2).

What it does
------------
  * loads CLMConvMoE from CLM/model/model.py (the landed skeleton),
  * reads a byte stream from the .kosmos @corpus dataset
    (CLM/corpus/clm_p1.corpus.kosmos -> sample/{web,register}.bytes),
  * runs a QAT training loop:
      - weights      : fake-quantized to symmetric int4 [-7, +7] per output
                       channel (AKIDA rejects -8; two's-complement NOT used),
      - activations  : fake-quantized to the AKIDA act_bits envelope
                       step = 2^(input_bits - act_bits),
                       y = clip(round(pot/step), 0, 2^act_bits - 1),
                       act_bits == 1 reduces to a binary LIF comparator,
      - gradients    : straight-through estimator (STE) — identity inside the
                       clip range, 0 outside; fp32 master weights are updated by
                       normal backprop while the forward sees the quantized path,
      - loss         : next-byte cross-entropy (V=256) + MoE aux loss
                       + optional envelope-consistency term (KL between the
                       quantized logits and the fp shadow logits) so the model
                       absorbs the PTQ-destruction as a training signal,
  * toggles the 3 router arms A / B / AB (CLM/model variant flag),
  * exposes a scale ladder: tiny (d64/L2/E4) and small (d256/L4/E8),
  * a --dry-run mode does a single forward + QAT loss + backward step and
    reports the measured step-rate (step/s) — the d5 honest re-measurement of
    the "hexa/py trainer throughput resolved" claim. No GPU pod is rented here.

Inference stays AKIDA-int4-only (P0 d4) — this file only governs the GPU/CPU
QAT pretrain. On-chip contextual adaptation is the PLASTICITY domain (edge-learn),
orthogonal to QAT (P0 §9 boundary).

The full-fire judgment of F-CLM-MONO (H_847, z>3.0 dual-axis, multi-seed) is a
SEPARATE explicit step (a real GPU fire); this trainer is the payload it will run.

Run
---
  # dry-run smoke (1 step, prints step-rate) — $0 local CPU:
  python3 CLM/train/train_clm.py --dry-run --arm AB --rung tiny

  # full local toy train (still $0, intuition only — toy != scale, H_666):
  python3 CLM/train/train_clm.py --arm AB --rung tiny --steps 200

  # the real verdict is the GPU full-fire (see CLM/train/run.sh + job.hexa).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

# --- make CLM/model importable regardless of cwd -------------------------- #
_HERE = os.path.dirname(os.path.abspath(__file__))
_CLM = os.path.dirname(_HERE)            # CLM/
_MODEL = os.path.join(_CLM, "model")
# Insert the model dir FIRST so `model` resolves to CLM/model/model.py (the
# module), not to the CLM/model package __init__.py.
if _MODEL not in sys.path:
    sys.path.insert(0, _MODEL)

from model import CLMConfig, CLMConvMoE          # noqa: E402  (CLM/model/model.py)
from data import make_batches                     # noqa: E402  (CLM/model/data.py)


# ========================================================================== #
# AKIDA envelope fake-quantizers with STE  (P0 §9)
# ========================================================================== #
INT4_SYM_MAX = 7        # symmetric int4 range is [-7, +7] (chip rejects -8)


def _sym_int4_scale(w: torch.Tensor) -> torch.Tensor:
    """Per-output-channel symmetric int4 scale. w: (out, in, ...) -> (out,1,..).

    scale_c = max(|w_c|) / 7 ; a per-channel scale is stored in .clm `qat_scale`
    so AKIDA loads it without recomputation (CLM_FORMAT_SPEC §2/§3).
    """
    out_c = w.shape[0]
    flat = w.detach().reshape(out_c, -1)
    amax = flat.abs().amax(dim=1).clamp_min(1e-8)            # (out,)
    scale = amax / INT4_SYM_MAX
    view = [out_c] + [1] * (w.dim() - 1)
    return scale.reshape(view)


class _WeightQuantSTE(torch.autograd.Function):
    """Fake-quantize weights to symmetric int4; straight-through gradient."""

    @staticmethod
    def forward(ctx, w: torch.Tensor, scale: torch.Tensor) -> torch.Tensor:
        q = torch.clamp(torch.round(w / scale), -INT4_SYM_MAX, INT4_SYM_MAX)
        # mark which elements are inside the representable range (STE mask)
        in_range = (w / scale).abs() <= INT4_SYM_MAX
        ctx.save_for_backward(in_range)
        return q * scale                       # dequantized value, fp tensor

    @staticmethod
    def backward(ctx, g: torch.Tensor):
        (in_range,) = ctx.saved_tensors
        # STE: identity inside the clip range, 0 outside; scale carries no grad.
        return g * in_range.to(g.dtype), None


def fake_quant_weight_int4(w: torch.Tensor) -> torch.Tensor:
    scale = _sym_int4_scale(w)
    return _WeightQuantSTE.apply(w, scale)


class _ActQuantSTE(torch.autograd.Function):
    """Fake-quantize an activation/potential to the AKIDA act_bits envelope.

    step = 2^(input_bits - act_bits); y = clip(round(pot/step), 0, 2^act_bits-1).
    act_bits == 1 -> a binary LIF comparator (akida_sw_lif reduction).
    """

    @staticmethod
    def forward(ctx, pot: torch.Tensor, step: float, qmax: int) -> torch.Tensor:
        y = torch.clamp(torch.round(pot / step), 0.0, float(qmax))
        in_range = (pot >= 0.0) & (pot / step <= float(qmax))
        ctx.save_for_backward(in_range)
        return y * step                        # dequantized activation level

    @staticmethod
    def backward(ctx, g: torch.Tensor):
        (in_range,) = ctx.saved_tensors
        return g * in_range.to(g.dtype), None, None


def akida_act_quant(pot: torch.Tensor, act_bits: int, input_bits: int) -> torch.Tensor:
    step = float(2 ** (input_bits - act_bits))
    qmax = (2 ** act_bits) - 1
    return _ActQuantSTE.apply(pot, step, qmax)


# ========================================================================== #
# QAT wrapper around the landed CLMConvMoE
# ========================================================================== #
@dataclass
class QATConfig:
    act_bits: int = 4          # AKIDA activation bits in {1,2,4}
    input_bits: int = 8        # input bit-depth feeding act quantizer
    quant_weights: bool = True
    quant_acts: bool = True
    envelope_lambda: float = 0.0   # weight of the fp-shadow consistency term
    enabled: bool = True

    def validate(self) -> None:
        if self.act_bits not in (1, 2, 4):
            raise ValueError(f"act_bits must be in {{1,2,4}}, got {self.act_bits}")


class ConvQATHook:
    """Context manager: route all nn.Conv1d forwards' OUTPUTS through the
    AKIDA act_bits activation fake-quant (STE). Weight-QAT is handled separately
    by _install_functional_qat (which sits inside the autograd graph); this
    context only adds the activation-envelope quantizer on each conv output.

    We keep fp32 master weights intact so the optimizer updates them; only the
    forward path sees the quantized activation levels.
    """

    def __init__(self, model: CLMConvMoE, qcfg: QATConfig):
        self.model = model
        self.q = qcfg
        self._handles = []

    def __enter__(self):
        if not (self.q.enabled and self.q.quant_acts):
            return self
        # The router (out=n_experts) and readout (out=vocab_size) convs produce
        # LOGITS, not AKIDA spike activations — quantizing those to non-negative
        # integer levels would destroy the softmax/CE. On the chip those final
        # logit reads are the FC readout, outside the spiking-activation
        # envelope, so we skip them here (honest: act-quant covers trunk/expert
        # activations only).
        vocab = self.model.cfg.vocab_size
        n_e = self.model.cfg.n_experts
        for m in self.model.modules():
            if isinstance(m, nn.Conv1d) and m.out_channels not in (vocab, n_e):
                self._handles.append(m.register_forward_hook(self._aq_post))
        return self

    def __exit__(self, *exc):
        for h in self._handles:
            h.remove()
        self._handles.clear()
        return False

    def _aq_post(self, module, inputs, output):
        # AKIDA activations are non-negative integer levels; quantize the
        # post-conv potential into the act_bits envelope. We apply on the ReLU-
        # like non-negative part (akida_sw_lif clips negatives to 0).
        relu = F.relu(output)
        q = akida_act_quant(relu, self.q.act_bits, self.q.input_bits)
        # preserve sign channel: AKIDA emits only non-negative spikes, so the
        # negative half is dropped (this matches the chip; honest envelope).
        return q


def _install_functional_qat(model: CLMConvMoE, qcfg: QATConfig) -> None:
    """Monkey-patch each nn.Conv1d._conv_forward to fake-quantize the weight
    via STE on every forward. This keeps fp32 master weights as Parameters
    (optimizer updates them) while the forward uses the int4-sym path.

    This is the autograd-correct way to do weight-QAT: the STE op sits inside
    the graph, so gradients flow to the fp32 master weight.
    """
    if not (qcfg.enabled and qcfg.quant_weights):
        return
    for m in model.modules():
        if isinstance(m, nn.Conv1d) and not getattr(m, "_qat_patched", False):
            orig_forward = m.forward

            def make_fwd(mod, of):
                def fwd(x):
                    qw = fake_quant_weight_int4(mod.weight)
                    return mod._conv_forward(x, qw, mod.bias)
                return fwd

            m.forward = make_fwd(m, orig_forward)
            m._qat_patched = True


# ========================================================================== #
# Corpus loading: .kosmos @corpus -> byte stream
# ========================================================================== #
def _read_bytes_file(path: str) -> List[int]:
    vals: List[int] = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                vals.append(int(line) & 0xFF)
    return vals


def load_corpus_byte_stream(corpus_kosmos: str) -> List[int]:
    """Read the .kosmos @corpus member shards and concatenate their byte
    streams (mix order = file order). We parse the @corpus member ref lines
    directly here (the authoritative hexa reader is ENCODER/kosmos_corpus_io.hexa;
    this is the minimal byte-level mirror needed by the python payload).
    """
    base = os.path.dirname(os.path.abspath(corpus_kosmos))
    members: List[str] = []
    with open(corpus_kosmos) as f:
        for line in f:
            s = line.strip()
            if s.startswith("member") and "ref" in s:
                # member = ref "sample/web.bytes" sha256=... count=...
                q1 = s.find('"')
                q2 = s.find('"', q1 + 1)
                if q1 >= 0 and q2 > q1:
                    members.append(s[q1 + 1 : q2])
    stream: List[int] = []
    for rel in members:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            stream.extend(_read_bytes_file(p))
    return stream


# ========================================================================== #
# Scale ladder
# ========================================================================== #
LADDER: Dict[str, Dict] = {
    # P0 d3 toy rungs. target rung is left to the AKD1000 fit probe (P4).
    "tiny":  dict(d_model=64,  n_trunk_layers=2,  n_experts=4),
    "small": dict(d_model=256, n_trunk_layers=4,  n_experts=8),
    # P6 production measurement-rungs (1:1 sync with train_clm.hexa rung SSOT).
    # GPU QAT here = PLASTI-SIM instrument measuring the backbone envelope, NOT
    # the deploy learner (P6_SCALE_LADDER_7B 0/3 . H_679/H_904).
    # param-counts verified against P6 1 formula:
    "mid":   dict(d_model=512, n_trunk_layers=8,  n_experts=8),    # 13,653,768
    "large": dict(d_model=768, n_trunk_layers=12, n_experts=12),   # 44,678,668
}


def build(arm: str, rung: str, **overrides) -> CLMConvMoE:
    base = dict(LADDER[rung])
    base.update(overrides)
    cfg = CLMConfig(variant=arm, **base)
    return CLMConvMoE(cfg)


# ========================================================================== #
# QAT loss
# ========================================================================== #
def qat_loss(
    model: CLMConvMoE,
    x: torch.Tensor,
    y: torch.Tensor,
    qcfg: QATConfig,
) -> Dict[str, torch.Tensor]:
    """One QAT forward: quantized path CE + aux + optional fp-shadow KL.

    The conv weights are already routed through STE int4 fake-quant by
    _install_functional_qat. Here we add the activation-envelope consistency
    term: a KL between the quantized-path logits and an fp-shadow forward
    (no act quant) absorbs the PTQ-destruction as a training signal (P0 §9).
    """
    out = model(x, y)                          # quantized-weight forward
    ce = out["ce_loss"]
    aux = out["aux_loss"]
    loss = ce + aux

    diag = {"ce": ce.detach(), "aux": aux.detach()}

    if qcfg.envelope_lambda > 0.0:
        # fp shadow: temporarily disable weight-QAT to get the unquantized logits
        with torch.no_grad():
            shadow_logits = _fp_shadow_logits(model, x)
        q_logits = out["logits"]               # (B, V, T)
        # KL(shadow || quantized) on the byte distribution, averaged
        sp = F.log_softmax(shadow_logits, dim=1)
        qp = F.log_softmax(q_logits, dim=1)
        kl = F.kl_div(qp, sp, log_target=True, reduction="batchmean")
        loss = loss + qcfg.envelope_lambda * kl
        diag["env_kl"] = kl.detach()

    diag["loss"] = loss
    return diag


def _fp_shadow_logits(model: CLMConvMoE, x: torch.Tensor) -> torch.Tensor:
    """Run the model with weight-QAT bypassed (fp master weights) for the
    shadow consistency target. We toggle the patched conv forwards off.
    """
    patched = [m for m in model.modules() if getattr(m, "_qat_patched", False)]
    saved = {}
    for m in patched:
        saved[m] = m.forward
        # restore the plain conv forward
        def plain(x_, mod=m):
            return mod._conv_forward(x_, mod.weight, mod.bias)
        m.forward = plain
    try:
        out = model(x)
        return out["logits"]
    finally:
        for m, f in saved.items():
            m.forward = f


# ========================================================================== #
# Train / dry-run
# ========================================================================== #
def train(
    arm: str = "AB",
    rung: str = "tiny",
    steps: int = 200,
    seq_len: int = 64,
    batch_size: int = 16,
    lr: float = 3e-3,
    seed: int = 42,
    act_bits: int = 4,
    envelope_lambda: float = 0.0,
    corpus: Optional[str] = None,
    dry_run: bool = False,
    json_out: Optional[str] = None,
) -> Dict:
    torch.manual_seed(seed)

    qcfg = QATConfig(act_bits=act_bits, envelope_lambda=envelope_lambda)
    qcfg.validate()

    model = build(arm, rung)
    _install_functional_qat(model, qcfg)
    aq_hook = ConvQATHook(model, QATConfig(act_bits=act_bits, quant_weights=False,
                                           quant_acts=True))

    # corpus byte stream (falls back to the committed sample @corpus)
    if corpus is None:
        corpus = os.path.join(_CLM, "corpus", "clm_p1.corpus.kosmos")
    stream = load_corpus_byte_stream(corpus)
    if len(stream) < seq_len + 2:
        raise RuntimeError(
            f"corpus byte stream too short ({len(stream)} bytes) from {corpus}"
        )

    n_steps = 1 if dry_run else steps
    batches = make_batches(stream, seq_len, batch_size, n_steps, seed=seed)
    opt = torch.optim.Adam(model.parameters(), lr=lr)

    model.train()
    t0 = time.time()
    losses = []
    with aq_hook:                              # activation-envelope quant active
        for i, (x, y) in enumerate(batches):
            opt.zero_grad()
            diag = qat_loss(model, x, y, qcfg)
            diag["loss"].backward()
            opt.step()
            losses.append(float(diag["ce"]))
    dt = time.time() - t0
    step_rate = n_steps / dt if dt > 0 else float("inf")

    result = {
        "mode": "dry-run" if dry_run else "train",
        "arm": arm,
        "rung": rung,
        "ladder": LADDER[rung],
        "params": model.num_params(),
        "steps_run": n_steps,
        "act_bits": act_bits,
        "envelope_lambda": envelope_lambda,
        "weight_quant": "int4_sym[-7,7] per-channel STE",
        "act_quant": f"akida act_bits={act_bits} step=2^(8-{act_bits})",
        "first_ce": round(losses[0], 4) if losses else None,
        "last_ce": round(losses[-1], 4) if losses else None,
        "wall_s": round(dt, 4),
        "step_rate_per_s": round(step_rate, 4),
        "corpus": corpus,
        "corpus_bytes": len(stream),
        "torch": torch.__version__,
    }
    if json_out:
        with open(json_out, "w") as f:
            json.dump(result, f, indent=2)
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="CLM P2 custom QAT trainer")
    ap.add_argument("--arm", default="AB", choices=["A", "B", "AB"],
                    help="router arm (P0 §3 3-arm ablation)")
    ap.add_argument("--rung", default="tiny", choices=list(LADDER.keys()),
                    help="scale-ladder rung (P0 d3)")
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--seq-len", type=int, default=64)
    ap.add_argument("--batch-size", type=int, default=16)
    ap.add_argument("--lr", type=float, default=3e-3)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--act-bits", type=int, default=4, choices=[1, 2, 4])
    ap.add_argument("--envelope-lambda", type=float, default=0.0,
                    help="fp-shadow consistency KL weight (P0 §9 optional term)")
    ap.add_argument("--corpus", default=None,
                    help="path to .kosmos @corpus (default: CLM/corpus/clm_p1)")
    ap.add_argument("--dry-run", action="store_true",
                    help="single forward+QAT-loss+backward, report step-rate ($0)")
    ap.add_argument("--json-out", default=None)
    a = ap.parse_args()

    res = train(
        arm=a.arm, rung=a.rung, steps=a.steps, seq_len=a.seq_len,
        batch_size=a.batch_size, lr=a.lr, seed=a.seed, act_bits=a.act_bits,
        envelope_lambda=a.envelope_lambda, corpus=a.corpus,
        dry_run=a.dry_run, json_out=a.json_out,
    )
    print(json.dumps(res, indent=2), flush=True)


if __name__ == "__main__":
    main()
