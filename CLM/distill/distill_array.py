"""BRIDGE distillation — teacher (valid scale) -> chip-fit student (transfer arm).

The SECONDARY arm of MITOSIS-ARRAY (CLM/P0_ARCHITECTURE.md §11.4/§11.6,
breakthrough.mining.md BRIDGE, F-CLM-BRIDGE-XFER). Where DISSOLVE reframes the
SCALE axis (PR2/PR3), BRIDGE crosses the measure-rung -> deploy-rung gap by
KNOWLEDGE DISTILLATION (@L8):

  TEACHER  : a larger sparse-MoE array (valid measure scale: more experts /
             wider d_model) whose routing-diversity (inter-expert dispatch
             entropy) is MEASURED.
  STUDENT  : a chip-fit array (each expert <= 1.2M AKD1000 nodes) distilled
             from the teacher via a KD soft-target loss on the next-byte logits.
  CLAIM    : the teacher's monopoly-escape (its dispatch-entropy z) SURVIVES
             distillation -- routing-diversity transfer Delta is small.

This file is the PIPELINE. The teacher train is a GPU fire (a_fire_autonomous);
this module also runs a $0 CPU TOY teacher<->student distill so the plumbing is
verified before/independent of the fire. The transfer verdict (does escape
survive?) is computed by the PR5 step (run_bridge_transfer.py) and persisted to
.verdicts/clm-mitosis-array/bridge_transfer_*.

KD loss (Hinton): L = (1-alpha)*CE(student, target)
                    + alpha * T^2 * KL(softmax(student/T) || softmax(teacher/T)).
Inference stays AKIDA-int4-only (P0 d4); distillation is GPU/CPU pretrain only.
Toy scale here is intuition (H_666); the fire runs the valid-scale teacher.
"""

from __future__ import annotations

import math
import os
import sys
from dataclasses import dataclass
from typing import Dict, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)
from array_moe import CLMArray, ArrayConfig, build_array, AKD1000_NODE_BUDGET  # noqa
from data import make_synthetic_corpus, make_batches, lane_tagged_stream        # noqa


@dataclass
class DistillConfig:
    """Teacher (valid measure scale) vs student (chip-fit deploy scale)."""
    # teacher: larger array (more experts + wider channels = valid measure scale)
    teacher_experts: int = 32
    teacher_d_model: int = 128
    # student: chip-fit array (fewer experts, narrow channels; each expert tiny)
    student_experts: int = 8
    student_d_model: int = 64
    # KD knobs (Hinton)
    kd_alpha: float = 0.7        # weight on the soft-target KL vs hard CE
    kd_temperature: float = 3.0  # softmax temperature for distillation


def build_teacher(cfg: DistillConfig) -> CLMArray:
    return build_array(n_experts=cfg.teacher_experts, d_model=cfg.teacher_d_model)


def build_student(cfg: DistillConfig) -> CLMArray:
    return build_array(n_experts=cfg.student_experts, d_model=cfg.student_d_model)


def kd_loss(student_logits: torch.Tensor, teacher_logits: torch.Tensor,
            targets: torch.Tensor, alpha: float, T: float) -> Dict[str, torch.Tensor]:
    """Hinton KD: hard-CE + temperature-scaled soft-target KL.

    student_logits / teacher_logits : (B, V, T). targets : (B, T) long.
    """
    V = student_logits.shape[1]
    hard = F.cross_entropy(
        student_logits.transpose(1, 2).reshape(-1, V), targets.reshape(-1)
    )
    s = F.log_softmax(student_logits / T, dim=1)
    t = F.softmax(teacher_logits / T, dim=1)
    soft = F.kl_div(s, t, reduction="batchmean") * (T * T)
    loss = (1.0 - alpha) * hard + alpha * soft
    return {"loss": loss, "hard_ce": hard.detach(), "soft_kl": soft.detach()}


def _dispatch_entropy_z(model: CLMArray, eval_batches, n_experts: int,
                        seed: int, null_samples: int = 2000) -> Dict:
    """Measure a model's inter-expert dispatch entropy + uniform-null z-score.

    Mirrors run_array_sweep's metric so teacher/student z are comparable.
    """
    model.eval()
    acc = torch.zeros(n_experts)
    with torch.no_grad():
        for x, y in eval_batches:
            out = model(x, y)
            acc = acc + out["dispatch_counts"]
    frac = acc / acc.sum().clamp_min(1.0)
    nz = frac[frac > 0]
    H = float(-(nz * torch.log(nz)).sum())

    # uniform-null (Dirichlet(1)) on the same token budget
    n_tok = max(1, int(acc.sum()) // max(1, len(list(eval_batches)) if hasattr(eval_batches, "__len__") else 16))
    g = torch.Generator().manual_seed(seed + 104729)
    ones = torch.ones(n_experts)
    Hs = torch.empty(null_samples)
    for s in range(null_samples):
        gam = torch.distributions.Gamma(ones, 1.0).sample()
        p = gam / gam.sum()
        c = torch.bincount(
            torch.multinomial(p, max(1, n_tok), replacement=True, generator=g),
            minlength=n_experts,
        ).float()
        fr = c / c.sum().clamp_min(1.0)
        z = fr[fr > 0]
        Hs[s] = float(-(z * torch.log(z)).sum())
    mu, sigma = float(Hs.mean()), float(Hs.std().clamp_min(1e-9))
    return {
        "n_experts": n_experts, "H": round(H, 5),
        "null_mu": round(mu, 5), "null_sigma": round(sigma, 5),
        "z": round((H - mu) / sigma, 5),
        "norm_entropy": round(H / math.log(n_experts), 5) if n_experts > 1 else 0.0,
    }


def train_teacher(cfg: DistillConfig, steps: int, seed: int,
                  seq_len: int = 64, batch: int = 16, lr: float = 3e-3) -> CLMArray:
    """Train the valid-scale teacher array on the toy two-lane corpus."""
    torch.manual_seed(seed)
    teacher = build_teacher(cfg)
    web, reg = make_synthetic_corpus(n_bytes_per_lane=8192, seed=seed)
    stream, _ = lane_tagged_stream(web, reg, block=64)
    batches = make_batches(stream, seq_len, batch, steps, seed=seed)
    opt = torch.optim.Adam(teacher.parameters(), lr=lr)
    teacher.train()
    for x, y in batches:
        opt.zero_grad()
        out = teacher(x, y)
        out["loss"].backward()
        opt.step()
    return teacher


def distill_student(teacher: CLMArray, cfg: DistillConfig, steps: int, seed: int,
                    seq_len: int = 64, batch: int = 16, lr: float = 3e-3) -> CLMArray:
    """Distill a chip-fit student from the (trained) teacher via KD loss."""
    torch.manual_seed(seed + 1)
    student = build_student(cfg)
    web, reg = make_synthetic_corpus(n_bytes_per_lane=8192, seed=seed)
    stream, _ = lane_tagged_stream(web, reg, block=64)
    batches = make_batches(stream, seq_len, batch, steps, seed=seed + 5)
    opt = torch.optim.Adam(student.parameters(), lr=lr)
    teacher.eval()
    student.train()
    for x, y in batches:
        opt.zero_grad()
        with torch.no_grad():
            t_logits = teacher(x)["logits"]
        s_out = student(x, y)
        kd = kd_loss(s_out["logits"], t_logits, y, cfg.kd_alpha, cfg.kd_temperature)
        kd["loss"].backward()
        opt.step()
    return student


def student_chip_fit(student: CLMArray) -> bool:
    return student.expert_chip_fit()
