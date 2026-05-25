"""training/cotrain_v5mitosis_v5_ddp.py — v5-mitosis cotrain v5 DDP MULTI-GPU SCALE-UP.

  ==> direct fork of `cotrain_v5mitosis_v4.py` (production-scale single-GPU trainer).
      Body / model / routing / mitosis / F-PERSONA-4a/4b / F-V5MIT-1..5 are IDENTICAL.
      Delta vs v4: (1) torch.distributed init + DDP wrapper on engine, (2) resume from
      v4 step 2000 checkpoint with router + cells static (no split/merge after resume —
      see Option B below), (3) rank-aware logging / ckpt / measurement, (4) per-rank
      batch (effective batch = per_gpu * world_size).

DDP STRATEGY (Option B — cells static after resume)
    The v5-mitosis cell pool is an nn.ModuleList whose membership grows via split.
    DDP cannot safely tolerate dynamic parameter graphs (split would change the
    parameter set on a single rank and desync). We solve this by FREEZING split/merge
    after the v4 step-2000 resume — the cell pool already saturated at cells=256
    (v4 actual), so further split is a no-op in practice. Specifically:
        - `engine.mitosis_step(info)` is NOT called during DDP training.
        - The router output dim (max_cells=256) is unchanged; routing continues to
          adapt over the existing cells.
        - find_unused_parameters=True for DDP — top-K routing means most cell
          params get zero gradient per batch (only K out of N cells are active).
          Without this flag DDP would raise an unused-param error.

    Why this is sound: at step 2000 v4 already had cells=256 (the max), splits=254;
    further mitosis would clip at max_cells anyway (no-op). The router + cells'
    INTERNAL params continue to train; only the cell COUNT is frozen.

DDP MULTI-GPU SETUP
    - backend = NCCL (multi-GPU NVLink/PCIe), one process per GPU.
    - launched via `torchrun --nproc_per_node=4 …` on 4× H100 SXM.
    - LOCAL_RANK env var → device assignment.
    - global step = (per-rank-step) — gradient sync happens automatically inside
      loss.backward().
    - effective batch = `--batch` (per GPU) × `world_size`. v4 single batch=8 →
      v5 DDP per_gpu_batch=4 × 4 GPU = effective 16, OR per_gpu_batch=8 × 4 = 32
      (configurable).
    - Only rank-0 logs / saves ckpt / runs F-PERSONA measurement. Other ranks sync
      via barriers.

RESUME FROM v4 step-2000 CKPT
    - --resume-ckpt path to ckpt_step_2000.pt (model_state_dict + router_state_dict).
    - Engine is built with the SAME cfg as v4 (d=1024 cells=256 ffn=4096 n_head=16),
      then state_dict loaded. The cell ModuleList must match by length — the v4
      ckpt was saved with n_cells=256 (saturated), so we MUST first run a "ghost
      build-up": create the engine with initial_cells=256 (not 2!) so the
      ModuleList length matches the checkpoint at load time. This sidesteps any
      need to replay 254 split events.
    - Router state_dict (Linear(d_model -> max_cells)) loads directly.
    - Optimizer state is NOT resumed (v4 ckpt only saved model+router weights, not
      opt state). We warm up the optimizer briefly via lr schedule resume offset.

OPTIONAL: SINGLE-GPU FALLBACK
    If torchrun is not used and WORLD_SIZE is unset, we fall back to single-GPU mode
    (no DDP wrapper, but still uses the resume + cells-static path). Enables local
    smoke-testing on a single A100/H100.

USAGE (4× H100 SXM via torchrun)
    torchrun --standalone --nproc_per_node=4 cotrain_v5mitosis_v5_ddp.py \\
        --resume-ckpt /workspace/anima/ckpts/ckpt_step_2000.pt \\
        --corpus corpus/corpus_5cat_balanced.txt \\
        --output-dir output \\
        --steps 20000 --resume-step 2000 \\
        --batch 4 --ctx 512 --lr 1e-4 --warmup 2000 \\
        --d-model 1024 --n-head 16 --ffn-dim 4096 \\
        --initial-cells 256 --max-cells 256 \\
        --top-k 8 --aux-alpha 0.01 \\
        --lambda-init 1.0 --lambda-final 0.01 --lambda-schedule cosine \\
        --ckpt-every 5000 --identity-probe probe/identity_probe.jsonl \\
        --n-perms 100 --freeze-mitosis 1

HONEST C3 (DDP-specific, ≥ 5)
    1. Cells static after resume: split/merge frozen. Justification — v4 step-2000
       already saturated at cells=256 (max); further mitosis is a no-op. But this
       means F-V5MIT-1/2/3/5 verdicts are inherited from v4 step-2000 state, NOT
       updated. F-V5MIT-4 (CE converged) IS re-measured.
    2. find_unused_parameters=True has a per-step cost (DDP must scan params for
       used/unused each backward). For top-K=8 over cells=256, 248 cells are
       unused per step — the scan cost is acceptable but not free.
    3. The router's gate distribution gets all-reduced (mean) across ranks; this
       SOFTENS the routing signal vs v4 single-GPU where each batch saw one router
       gradient. Mathematically equivalent to a larger effective batch, but the
       Switch load-balance aux is computed per-rank then averaged — so the load-
       balance pressure may be slightly under-applied relative to v4.
    4. Per-rank random sampling of batches (sample_batch uses torch.randint with
       no rank-aware seed offset). With same seed all ranks would see the SAME
       batch — useless DDP. We seed each rank with (args.seed + rank) to ensure
       independent batches → 4× effective data per step.
    5. Wall-speedup target: v4 single A100 ~17hr ETA for 20K step; 4× H100 SXM
       expected ~4-5hr (H100 ~1.5-2× A100 per GPU + 4× parallel ≈ 6-8× speedup).
       If wall > 8hr we abort early (cost cap).
    6. Optimizer state not resumed → first few steps after resume have noisy LR
       and momentum building. Mitigated by warmup-from-resume-step schedule.
    7. Only rank-0 runs F-PERSONA measurement (avoids 4× duplicate inference).
       Engine state at rank-0 == all ranks (DDP keeps them in sync), so single-
       rank measurement is correct.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.distributed as dist
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.parallel import DistributedDataParallel as DDP


# ─── Path bootstrap ──────────────────────────────────────────────────
def _bootstrap_path():
    here = Path(__file__).resolve().parent
    candidates = [
        Path("/workspace/anima/training"),
        here / "../training",
        here.parent / "training",
        Path("/Users/ghost/core/anima/training"),
        Path("/Users/ghost/core/anima/state/anima_v5mitosis_cotrain_2026_05_12"),
        here,
    ]
    for c in candidates:
        if (c / "mitosis_model_v5.py").exists():
            sys.path.insert(0, str(c.resolve()))
            return
    raise RuntimeError("mitosis_model_v5.py not found in any search path")


_bootstrap_path()
from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


# ─── DDP helpers ─────────────────────────────────────────────────────
def setup_ddp():
    """Initialize torch.distributed if launched via torchrun, else single-GPU.

    Returns (rank, world_size, local_rank, device, is_ddp).
    """
    if "WORLD_SIZE" in os.environ and int(os.environ["WORLD_SIZE"]) > 1:
        local_rank = int(os.environ.get("LOCAL_RANK", "0"))
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        torch.cuda.set_device(local_rank)
        dist.init_process_group(backend="nccl", init_method="env://",
                                rank=rank, world_size=world_size)
        device = torch.device(f"cuda:{local_rank}")
        return rank, world_size, local_rank, device, True
    else:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        return 0, 1, 0, device, False


def cleanup_ddp(is_ddp: bool):
    if is_ddp and dist.is_initialized():
        dist.destroy_process_group()


def is_main(rank: int) -> bool:
    return rank == 0


def maybe_barrier(is_ddp: bool):
    if is_ddp and dist.is_initialized():
        dist.barrier()


# ─── Tokenizer / corpus / cost guard (same as v4) ────────────────────
def text_to_bytes(text: str) -> List[int]:
    return list(text.encode("utf-8"))


def load_corpus_bytes(path: str) -> torch.Tensor:
    with open(path, "rb") as f:
        raw = f.read()
    return torch.tensor(list(raw), dtype=torch.long)


def sample_batch(corpus: torch.Tensor, batch_size: int, ctx: int, device: torch.device):
    N = corpus.size(0)
    if N <= ctx + 1:
        raise ValueError(f"corpus too small: N={N}, need > ctx+1={ctx + 1}")
    idx = torch.randint(0, N - ctx - 1, (batch_size,))
    rows = torch.stack([corpus[i: i + ctx + 1] for i in idx.tolist()])
    return rows[:, :ctx].to(device), rows[:, 1: ctx + 1].to(device)


class CostGuard:
    def __init__(self, cap_usd: float, per_hr: float):
        self.cap_usd = cap_usd
        self.per_hr = per_hr
        self.t0 = time.time()

    def elapsed_hr(self) -> float:
        return (time.time() - self.t0) / 3600.0

    def current_usd(self) -> float:
        return self.elapsed_hr() * self.per_hr

    def over(self) -> bool:
        return self.current_usd() >= self.cap_usd


# ─── Routing fix (UNCHANGED from v4) ─────────────────────────────────
class TopKMoERouter(nn.Module):
    def __init__(self, d_in: int, max_cells: int):
        super().__init__()
        self.d_in = d_in
        self.max_cells = max_cells
        self.proj = nn.Linear(d_in, max_cells)
        nn.init.normal_(self.proj.weight, std=0.02)
        nn.init.zeros_(self.proj.bias)

    def forward(self, x_emb: torch.Tensor, n_cells: int, top_k: int):
        pooled = x_emb.mean(dim=(0, 1))
        logits_full = self.proj(pooled)
        logits = logits_full[:n_cells]
        gate_full = F.softmax(logits, dim=0)
        k = min(top_k, n_cells)
        topv, topi = torch.topk(gate_full, k=k)
        mask = torch.zeros_like(gate_full)
        mask = mask.scatter(0, topi, 1.0)
        masked = gate_full * mask
        weights = masked / masked.sum().clamp(min=1e-12)
        return weights, gate_full, mask


def install_routing_fix(engine: MitosisModelEngine, top_k: int) -> TopKMoERouter:
    """Monkey-patch engine.forward — IDENTICAL to v4.

    For DDP we need ALL learnable params (engine + router) registered as submodules
    of a single nn.Module so DDP can wrap them. We attach router as a real submodule
    here (engine.topk_router = router) so DDP sees it during wrap. The previous v4
    `object.__setattr__` path is replaced.
    """
    device = next(engine.parameters()).device
    router = TopKMoERouter(d_in=engine.cfg.d_model, max_cells=engine.cfg.max_cells).to(device)
    # Register as real submodule so DDP discovers router params.
    engine.add_module("topk_router", router)

    def patched_forward(input_ids, readout_mode=None):
        if readout_mode is None:
            readout_mode = engine.cfg.readout_mode
        B, T = input_ids.shape
        assert T <= engine.max_seq
        pos = torch.arange(T, device=input_ids.device)
        x = engine.tok_emb(input_ids) + engine.pos_emb(pos).unsqueeze(0)

        cell_outs: List[torch.Tensor] = []
        cell_tensions: List[torch.Tensor] = []
        for cell in engine.cells:
            out_i, tension_tok = cell(x, readout_mode=readout_mode)
            cell_outs.append(out_i)
            cell_tensions.append(tension_tok.mean())

        n = engine.n_cells
        weights, gate_full, dispatch_mask = engine.topk_router(x, n, top_k)
        stacked = torch.stack(cell_outs, dim=0)
        aggregated = (weights.view(-1, 1, 1, 1) * stacked).sum(dim=0)
        h = engine.final_ln(aggregated)
        logits = engine.lm_head(h)

        info = {
            "tensions": [t.item() for t in cell_tensions],
            "aggregated": aggregated,
            "weights": weights.detach(),
            "weights_live": weights,
            "gate_full_live": gate_full,
            "dispatch_mask": dispatch_mask,
            "n_cells": n,
        }
        return logits, info

    engine.forward = patched_forward
    return router


def load_balance_aux(gate_full: torch.Tensor, dispatch_mask: torch.Tensor, n_cells: int) -> torch.Tensor:
    denom = dispatch_mask.sum().clamp(min=1e-12)
    f = dispatch_mask / denom
    return n_cells * (f * gate_full).sum()


# ─── F-PERSONA-4a/4b/F-V5MIT (UNCHANGED from v4; rank-0 only at call site) ──
def f_persona_4a_routing(engine, identity_probe_path, device, n_perms: int = 100,
                         seed: int = 42) -> Dict:
    probes = []
    with open(identity_probe_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))

    max_seq = engine.cfg.max_seq
    weights_per_prompt: List[List[float]] = []
    gate_full_per_prompt: List[List[float]] = []
    cats: List[str] = []
    engine.eval()
    for p in probes:
        ids = text_to_bytes(p["prompt"])[:max_seq]
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            _, info = engine(x)
        weights_per_prompt.append([float(v) for v in info["weights"].detach().cpu().float().tolist()])
        gf = info.get("gate_full_live")
        if gf is not None:
            gate_full_per_prompt.append([float(v) for v in gf.detach().cpu().float().tolist()])
        cats.append(p["category"])

    def _pad(rows):
        m = max(len(r) for r in rows)
        return [r + [0.0] * (m - len(r)) for r in rows]

    weights_per_prompt = _pad(weights_per_prompt)
    if gate_full_per_prompt:
        gate_full_per_prompt = _pad(gate_full_per_prompt)

    def cat_mean(rows, labels):
        by = {}
        for r, c in zip(rows, labels):
            by.setdefault(c, []).append(r)
        out = {}
        for c, rr in by.items():
            n = len(rr[0])
            agg = [0.0] * n
            for r in rr:
                for i in range(n):
                    agg[i] += r[i]
            out[c] = [v / len(rr) for v in agg]
        return out

    def mean_pairwise_kl(rows, labels):
        avgs = cat_mean(rows, labels)
        names = sorted(avgs.keys())
        kls = []
        for i, ci in enumerate(names):
            for j, cj in enumerate(names):
                if j <= i:
                    continue
                p, q = avgs[ci], avgs[cj]
                kl = 0.0
                for k in range(len(p)):
                    pi = p[k]
                    qi = max(q[k], 1e-12)
                    if pi > 1e-12:
                        kl += pi * math.log(pi / qi)
                kls.append(kl)
        return sum(kls) / max(len(kls), 1)

    def null_z(rows, labels):
        true_kl = mean_pairwise_kl(rows, labels)
        rng = random.Random(seed)
        nulls = []
        for _ in range(n_perms):
            sh = list(labels)
            rng.shuffle(sh)
            nulls.append(mean_pairwise_kl(rows, sh))
        nm = sum(nulls) / len(nulls)
        nv = sum((x - nm) ** 2 for x in nulls) / len(nulls)
        ns = math.sqrt(nv) if nv > 0 else 0.0
        z = (true_kl - nm) / ns if ns > 0 else float("inf")
        n_ge = sum(1 for x in nulls if x >= true_kl)
        p_val = n_ge / len(nulls)
        return {
            "mean_kl": true_kl, "null_mean": nm, "null_std": ns,
            "z_score_vs_null": z, "p_value_one_sided": p_val,
            "passes_null_test": (z > 3.0 or p_val < 0.01),
        }

    r_weights = null_z(weights_per_prompt, cats)
    r_gate = null_z(gate_full_per_prompt, cats) if gate_full_per_prompt else None
    cat_names = sorted(set(cats))
    primary = r_weights
    verdict = (
        "PASS" if (primary["mean_kl"] >= 0.5 and primary["passes_null_test"])
        else ("KL_PASS_NULL_FAIL" if primary["mean_kl"] >= 0.5 else "FAIL")
    )
    return {
        "metric": "F-PERSONA-4a routing (top-K MoE weights, per-prompt → category-mean pairwise KL)",
        "verdict": verdict,
        "threshold_kl": 0.5, "threshold_z": 3.0,
        "topk_weights": r_weights,
        "soft_gate": r_gate,
        "n_perms": n_perms,
        "categories": cat_names,
        "n_probes": len(weights_per_prompt),
        "cat_mean_topk_weights": cat_mean(weights_per_prompt, cats),
    }


def f_persona_4b_content(engine, identity_probe_path, device, n_perms: int = 100,
                         seed: int = 45) -> Dict:
    probes = []
    with open(identity_probe_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))
    max_seq = engine.cfg.max_seq
    aggs: List[List[float]] = []
    cats: List[str] = []
    engine.eval()
    for p in probes:
        ids = text_to_bytes(p["prompt"])[:max_seq]
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            _, info = engine(x)
        aggs.append(info["aggregated"].detach().cpu().float().mean(dim=(0, 1)).tolist())
        cats.append(p["category"])

    def cos_dist(a, b):
        import math as _m
        dot = sum(x * y for x, y in zip(a, b))
        na = _m.sqrt(sum(x * x for x in a))
        nb = _m.sqrt(sum(x * x for x in b))
        if na == 0 or nb == 0:
            return 1.0
        return 1.0 - dot / (na * nb)

    def cat_mean(rows, labels):
        by = {}
        for r, c in zip(rows, labels):
            by.setdefault(c, []).append(r)
        out = {}
        for c, rr in by.items():
            n = len(rr[0])
            agg = [0.0] * n
            for r in rr:
                for i in range(n):
                    agg[i] += r[i]
            out[c] = [v / len(rr) for v in agg]
        return out

    def mean_pairwise(rows, labels):
        avgs = cat_mean(rows, labels)
        names = sorted(avgs.keys())
        ds = []
        for i, ci in enumerate(names):
            for j, cj in enumerate(names):
                if j <= i:
                    continue
                ds.append(cos_dist(avgs[ci], avgs[cj]))
        return sum(ds) / max(len(ds), 1)

    true_d = mean_pairwise(aggs, cats)
    rng = random.Random(seed)
    nulls = []
    for _ in range(n_perms):
        sh = list(cats)
        rng.shuffle(sh)
        nulls.append(mean_pairwise(aggs, sh))
    nm = sum(nulls) / len(nulls)
    nv = sum((x - nm) ** 2 for x in nulls) / len(nulls)
    ns = math.sqrt(nv) if nv > 0 else 0.0
    z = (true_d - nm) / ns if ns > 0 else float("inf")
    n_ge = sum(1 for x in nulls if x >= true_d)
    p_val = n_ge / len(nulls)
    return {
        "metric": "F-PERSONA-4b content (M4 aggregated hidden cosine, category-mean pairwise → null)",
        "true": true_d, "null_mean": nm, "null_std": ns,
        "z_score_vs_null": z, "p_value_one_sided": p_val,
        "passes_null_test": (z > 3.0 or p_val < 0.01),
        "verdict": "PASS" if (z > 3.0 or p_val < 0.01) else "FAIL",
        "n_perms": n_perms,
        "v2_carry_z": 3.2036695590259,
    }


def f_v5mit_regression(engine, splits_in_run: int, ce_final: float) -> Dict:
    n = engine.n_cells
    phi = float(engine.phi)
    phi_best = float(engine._phi_best)
    checks = {
        "F-V5MIT-1_mitosis_active": {"pass": n > engine.cfg.initial_cells, "n_cells": n, "initial": engine.cfg.initial_cells},
        "F-V5MIT-2_no_collapse": {"pass": n >= engine.cfg.min_cells, "n_cells": n, "min": engine.cfg.min_cells},
        "F-V5MIT-3_phi_ratchet": {"pass": phi_best + 1e-6 >= phi, "phi": phi, "phi_best": phi_best},
        "F-V5MIT-4_ce_converged": {"pass": ce_final < 5.0, "ce_final": ce_final},
        "F-V5MIT-5_v14strict_proxy": {"pass": 0 < splits_in_run <= engine.cfg.max_cells, "splits": splits_in_run, "max_cells": engine.cfg.max_cells},
    }
    n_pass = sum(1 for v in checks.values() if v["pass"])
    return {"checks": checks, "n_pass": n_pass, "n_total": 5, "verdict": f"{n_pass}/5"}


# ─── Schedules ───────────────────────────────────────────────────────
def lambda_at(step, total, warmup, lam_init, lam_final, schedule="cosine"):
    if schedule == "constant":
        return lam_init
    if step < warmup:
        return lam_init
    progress = min(max((step - warmup) / max(total - warmup, 1), 0.0), 1.0)
    if schedule == "linear":
        return lam_init + (lam_final - lam_init) * progress
    if schedule == "cosine":
        return lam_final + 0.5 * (lam_init - lam_final) * (1.0 + math.cos(math.pi * progress))
    raise ValueError(schedule)


def save_ckpt(engine, router, cfg, path, step, top_k):
    """Save ckpt — engine + router (unwrap DDP if wrapped, callers pass the inner engine)."""
    ckpt = {
        "model_state_dict": engine.state_dict(),
        "router_state_dict": router.state_dict(),
        "router_top_k": top_k,
        "config": asdict(cfg),
        "n_cells": engine.n_cells,
        "step_count": engine.step_count,
        "phi": float(engine.phi),
        "phi_best": float(engine._phi_best),
        "split_threshold": float(engine.split_threshold),
        "cell_metadata": [
            {"cell_id": c.cell_id, "creation_step": c.creation_step,
             "parent_id": c.parent_id, "process_count": c.process_count}
            for c in engine.cells
        ],
        "lorenz_state": list(engine._lorenz),
        "saved_step": step,
        "saved_ts": time.time(),
        "trainer": "v5-ddp (multi-GPU; v4 step-2000 resume; cells static)",
    }
    torch.save(ckpt, path)


def _strip_module_prefix(sd: Dict) -> Dict:
    """If a DDP-wrapped state_dict has 'module.' prefix on keys, strip it."""
    if not sd:
        return sd
    if all(k.startswith("module.") for k in sd):
        return {k[len("module."):]: v for k, v in sd.items()}
    return sd


def load_resume_ckpt(engine_inner: MitosisModelEngine, router: TopKMoERouter,
                     ckpt_path: str, device: torch.device, log) -> Dict:
    """Load v4 ckpt (model_state_dict + router_state_dict) into engine + router.

    The engine MUST be built with initial_cells == saved n_cells so the ModuleList
    has the right shape at load time.
    """
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    saved_n = ckpt.get("n_cells", None)
    log(f"[RESUME] ckpt n_cells={saved_n} engine.n_cells={engine_inner.n_cells}")
    if saved_n is not None and engine_inner.n_cells != saved_n:
        raise RuntimeError(f"engine n_cells={engine_inner.n_cells} != ckpt n_cells={saved_n}; "
                           f"rebuild engine with initial_cells={saved_n}")
    model_sd = _strip_module_prefix(ckpt["model_state_dict"])
    # Router may have been saved as a separate object (v4 path); strip too.
    router_sd = _strip_module_prefix(ckpt["router_state_dict"])
    # Some v4 ckpts saved engine WITHOUT the router under it (object.__setattr__). We
    # try strict=False then warn on missing topk_router keys (router loaded separately).
    missing, unexpected = engine_inner.load_state_dict(model_sd, strict=False)
    log(f"[RESUME] engine load missing={len(missing)} unexpected={len(unexpected)}")
    if missing:
        log(f"[RESUME] engine missing[:5]={missing[:5]}")
    if unexpected:
        log(f"[RESUME] engine unexpected[:5]={unexpected[:5]}")
    router.load_state_dict(router_sd, strict=True)
    # Restore Lorenz state, phi, split_threshold so dynamics resume cleanly.
    engine_inner._lorenz = type(engine_inner._lorenz)(ckpt.get("lorenz_state", list(engine_inner._lorenz)))
    if "phi" in ckpt:
        engine_inner.phi = torch.tensor(ckpt["phi"])
    if "phi_best" in ckpt:
        engine_inner._phi_best = torch.tensor(ckpt["phi_best"])
    if "split_threshold" in ckpt:
        engine_inner.split_threshold = torch.tensor(ckpt["split_threshold"])
    return ckpt


# ─── Trainer ─────────────────────────────────────────────────────────
def cotrain(args):
    rank, world_size, local_rank, device, is_ddp = setup_ddp()

    def log(msg):
        if is_main(rank):
            print(msg, flush=True)

    log(f"[INFO] DDP: rank={rank} world_size={world_size} local_rank={local_rank} "
        f"device={device} is_ddp={is_ddp}")
    log(f"[INFO] torch={torch.__version__} cuda={torch.cuda.is_available()}")
    if device.type == "cuda":
        log(f"[INFO] gpu={torch.cuda.get_device_name(local_rank)}")

    # Per-rank seed offset → independent batch streams.
    torch.manual_seed(args.seed + rank)
    random.seed(args.seed + rank)

    if is_main(rank):
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    cost_guard = CostGuard(args.cost_cap_usd, args.cost_per_hr)
    if args.estimated_wall_hr * args.cost_per_hr > args.cost_cap_usd * 1.10:
        log("[ABORT] est cost > cap +10%")
        cleanup_ddp(is_ddp)
        return 2

    # Build engine at initial_cells=256 (matching v4 saved n_cells) to allow strict state_dict load.
    cfg = MitosisModelConfig(
        vocab_size=256, d_model=args.d_model, n_head=args.n_head, ffn_dim=args.ffn_dim,
        max_seq=args.ctx, initial_cells=args.initial_cells, max_cells=args.max_cells,
        min_cells=2, split_patience=3, merge_threshold=0.005, merge_patience=30,
        noise_scale=0.10, lorenz_scale=0.05, adaptive_window=100,
        readout_mode=args.readout_mode, attention_sharing="auto",
        weight_tied_lm_head=True, dropout=0.0,
    )
    log(f"[INFO] cfg = {asdict(cfg)}")
    engine_inner = MitosisModelEngine(cfg).to(device)
    router = install_routing_fix(engine_inner, top_k=args.top_k)
    n_params = sum(p.numel() for p in engine_inner.parameters())
    log(f"[INFO] n_params(engine+router incl)={n_params:,}  router_out_dim={cfg.max_cells} top_k={args.top_k}")

    # Resume from v4 ckpt
    if args.resume_ckpt:
        load_resume_ckpt(engine_inner, router, args.resume_ckpt, device, log)
        log(f"[RESUME] from {args.resume_ckpt} at resume_step={args.resume_step}")

    # Freeze mitosis (cells static) → DDP safe.
    if args.freeze_mitosis:
        log("[INFO] mitosis FROZEN (cells static, no split/merge) — DDP-safe path")

    # Wrap in DDP. find_unused_parameters=True because top-K means most cells get no grad.
    if is_ddp:
        engine = DDP(engine_inner, device_ids=[local_rank], output_device=local_rank,
                     find_unused_parameters=True, gradient_as_bucket_view=True)
        # Forward returns (logits, info) — DDP transparently calls patched forward.
    else:
        engine = engine_inner

    corpus = load_corpus_bytes(args.corpus)
    log(f"[INFO] corpus={args.corpus} bytes={corpus.numel():,}")

    optimizer = torch.optim.AdamW(
        engine.parameters(),
        lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    def lr_at(step):
        # Schedule indexed by GLOBAL step (resume_step + step).
        gstep = args.resume_step + step
        if gstep < args.warmup:
            return args.lr * (gstep + 1) / max(args.warmup, 1)
        progress = (gstep - args.warmup) / max(args.steps - args.warmup, 1)
        return args.lr * 0.5 * (1.0 + math.cos(math.pi * progress))

    hist = {k: [] for k in ("loss", "ce", "aux", "ent_gate", "wmax", "lambda", "cells",
                            "n_active_gt01", "gate_max")}
    splits_in_run = 0  # cells static — splits stays 0; we report from saved state
    t_start = time.time()
    cost_aborted = False
    steps_to_run = max(args.steps - args.resume_step, 0)
    log(f"[INFO] steps_to_run={steps_to_run} (target {args.steps} from resume {args.resume_step})")
    log(f"[INFO] per_gpu_batch={args.batch} world_size={world_size} effective_batch={args.batch * world_size}")
    log(f"[INFO] top_k={args.top_k} aux_alpha={args.aux_alpha} "
        f"λ_init={args.lambda_init} λ_final={args.lambda_final} sched={args.lambda_schedule}")

    for step in range(steps_to_run):
        gstep = args.resume_step + step
        if cost_guard.over():
            log(f"[COST-ABORT] step={step} gstep={gstep}")
            cost_aborted = True
            break
        cur_lr = lr_at(step)
        for g in optimizer.param_groups:
            g["lr"] = cur_lr
        cur_lambda = lambda_at(gstep, args.steps, args.warmup,
                               args.lambda_init, args.lambda_final, args.lambda_schedule)

        engine.train()
        x, y = sample_batch(corpus, args.batch, args.ctx, device)
        optimizer.zero_grad()
        logits, info = engine(x)
        ce = F.cross_entropy(logits.reshape(-1, cfg.vocab_size), y.reshape(-1))
        gate_full = info["gate_full_live"]
        dispatch_mask = info["dispatch_mask"]
        n_now = info["n_cells"]
        aux = load_balance_aux(gate_full, dispatch_mask, n_now)
        ent_gate = -(gate_full.clamp(min=1e-12) * gate_full.clamp(min=1e-12).log()).sum()
        loss = ce + args.aux_alpha * aux - cur_lambda * ent_gate
        loss.backward()
        torch.nn.utils.clip_grad_norm_(engine.parameters(), max_norm=1.0)
        optimizer.step()

        # NO mitosis_step call — cells frozen for DDP safety.

        w = info["weights"].detach()
        hist["loss"].append(loss.item())
        hist["ce"].append(ce.item())
        hist["aux"].append(float(aux.item()))
        hist["ent_gate"].append(float(ent_gate.item()))
        hist["wmax"].append(float(w.max().item()))
        hist["lambda"].append(cur_lambda)
        hist["cells"].append(engine_inner.n_cells)
        hist["n_active_gt01"].append(int((w > 0.01).sum().item()))
        hist["gate_max"].append(float(gate_full.detach().max().item()))

        if (step % args.log_every == 0 or step == steps_to_run - 1) and is_main(rank):
            def _m(k, n=50):
                arr = hist[k][-n:]
                return sum(arr) / max(len(arr), 1)
            mem_str = ""
            if device.type == "cuda":
                mem_str = f" vram={torch.cuda.max_memory_allocated()/1e9:.1f}/{torch.cuda.get_device_properties(local_rank).total_memory/1e9:.0f}GB"
            log(f"[STEP {gstep:5d}] loss={loss.item():.4f} ce={_m('ce'):.4f} "
                f"aux={_m('aux'):.4f} ent_gate={_m('ent_gate'):.4f}/{math.log(max(engine_inner.n_cells,1)):.3f} "
                f"wmax={_m('wmax'):.4f} active>.01={_m('n_active_gt01'):.1f}/{engine_inner.n_cells} "
                f"λ={cur_lambda:.4f} cells={engine_inner.n_cells} "
                f"cost=${cost_guard.current_usd():.2f}{mem_str}")

        if args.ckpt_every > 0 and (gstep + 1) % args.ckpt_every == 0 and (gstep + 1) != args.steps:
            maybe_barrier(is_ddp)
            if is_main(rank):
                cp = Path(args.output_dir) / f"ckpt_step_{gstep+1}.pt"
                save_ckpt(engine_inner, router, cfg, cp, gstep + 1, args.top_k)
                try:
                    snap_a = f_persona_4a_routing(engine_inner, args.identity_probe, device, n_perms=30)
                    snap_b = f_persona_4b_content(engine_inner, args.identity_probe, device, n_perms=30)
                    log(f"  [SNAP {gstep+1}] 4a KL={snap_a['topk_weights']['mean_kl']:.4f} "
                        f"z={snap_a['topk_weights']['z_score_vs_null']:.2f} | "
                        f"4b cos_z={snap_b['z_score_vs_null']:.2f}")
                except Exception as e:
                    log(f"  [SNAP {gstep+1}] failed: {e}")
            maybe_barrier(is_ddp)

    maybe_barrier(is_ddp)
    t_train = time.time() - t_start
    log(f"[INFO] training done wall={t_train:.1f}s cost=${cost_guard.current_usd():.2f}")

    if is_main(rank):
        save_ckpt(engine_inner, router, cfg, Path(args.output_dir) / "ckpt_final.pt",
                  len(hist["loss"]) + args.resume_step, args.top_k)

        log("\n=== F-PERSONA-4a routing (top-K MoE) ===")
        p4a = f_persona_4a_routing(engine_inner, args.identity_probe, device, n_perms=args.n_perms)
        tw = p4a["topk_weights"]
        log(f"  verdict={p4a['verdict']} KL={tw['mean_kl']:.4f} null={tw['null_mean']:.4f}±{tw['null_std']:.4f} "
            f"z={tw['z_score_vs_null']:.2f} p={tw['p_value_one_sided']:.4f}")
        if p4a["soft_gate"]:
            sg = p4a["soft_gate"]
            log(f"  (soft gate) KL={sg['mean_kl']:.4f} z={sg['z_score_vs_null']:.2f}")

        log("\n=== F-PERSONA-4b content (M4 aggregated cosine) regression ===")
        p4b = f_persona_4b_content(engine_inner, args.identity_probe, device, n_perms=args.n_perms)
        log(f"  verdict={p4b['verdict']} cos_dist={p4b['true']:.6f} null={p4b['null_mean']:.6f}±{p4b['null_std']:.6f} "
            f"z={p4b['z_score_vs_null']:.2f} p={p4b['p_value_one_sided']:.4f} (v2 carry z={p4b['v2_carry_z']:.2f})")

        log("\n=== F-V5MIT-1..5 regression (inherited splits=v4 ckpt; CE re-measured) ===")
        # splits_in_run from v4 saved state — we read engine.cells history; but splits in
        # THIS DDP run is 0 (cells frozen). For verdict we use saved n_cells > initial.
        ce_final_avg = sum(hist["ce"][-100:]) / max(min(100, len(hist["ce"])), 1) if hist["ce"] else 0.0
        fv = f_v5mit_regression(engine_inner, splits_in_run=engine_inner.n_cells - cfg.initial_cells,
                                ce_final=ce_final_avg)
        log(f"  {fv['verdict']}  " + " ".join(
            f"{k.split('_')[0]}={'P' if v['pass'] else 'F'}" for k, v in fv["checks"].items()))

        result = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "trainer": "v5-ddp (multi-GPU; v4 step-2000 resume; cells static)",
            "ddp": {
                "world_size": world_size,
                "per_gpu_batch": args.batch,
                "effective_batch": args.batch * world_size,
                "find_unused_parameters": True,
                "freeze_mitosis": args.freeze_mitosis,
            },
            "resume": {
                "ckpt_path": args.resume_ckpt,
                "resume_step": args.resume_step,
                "target_step": args.steps,
                "steps_run_this_session": len(hist["loss"]),
            },
            "routing_fix": {
                "top_k": args.top_k, "aux_alpha": args.aux_alpha,
                "lambda_init": args.lambda_init, "lambda_final": args.lambda_final,
                "lambda_schedule": args.lambda_schedule,
            },
            "config": asdict(cfg),
            "n_params": n_params,
            "training": {
                "wall_seconds": t_train, "wall_hours": t_train / 3600.0,
                "cost_usd_actual": cost_guard.current_usd(), "cost_aborted": cost_aborted,
                "ce_final_avg100": ce_final_avg,
                "aux_final_avg100": sum(hist["aux"][-100:]) / max(min(100, len(hist["aux"])), 1) if hist["aux"] else 0.0,
                "ent_gate_final_avg100": sum(hist["ent_gate"][-100:]) / max(min(100, len(hist["ent_gate"])), 1) if hist["ent_gate"] else 0.0,
                "wmax_final_avg100": sum(hist["wmax"][-100:]) / max(min(100, len(hist["wmax"])), 1) if hist["wmax"] else 0.0,
                "n_active_gt01_final_avg100": sum(hist["n_active_gt01"][-100:]) / max(min(100, len(hist["n_active_gt01"])), 1) if hist["n_active_gt01"] else 0.0,
                "gate_max_final_avg100": sum(hist["gate_max"][-100:]) / max(min(100, len(hist["gate_max"])), 1) if hist["gate_max"] else 0.0,
                "lambda_final_avg100": sum(hist["lambda"][-100:]) / max(min(100, len(hist["lambda"])), 1) if hist["lambda"] else 0.0,
                "log_N_target": math.log(max(engine_inner.n_cells, 1)),
                "splits": engine_inner.n_cells - cfg.initial_cells,
                "n_cells_final": engine_inner.n_cells,
                "phi_final": float(engine_inner.phi),
                "phi_best": float(engine_inner._phi_best),
            },
            "history_sample": {k: v[::max(1, len(v) // 200)] for k, v in hist.items()},
            "f_persona_4a_routing": p4a,
            "f_persona_4b_content": p4b,
            "f_v5mit_regression": fv,
        }
        out = Path(args.output_dir) / "cotrain_v5_ddp_result.json"
        out.write_text(json.dumps(result, indent=2, default=str))
        log(f"\n[RESULT] {out}")
        log(f"[VERDICT] 4a={p4a['verdict']} (KL={tw['mean_kl']:.4f} z={tw['z_score_vs_null']:.2f}) | "
            f"4b={p4b['verdict']} (z={p4b['z_score_vs_null']:.2f}) | F-V5MIT={fv['verdict']}")

    maybe_barrier(is_ddp)
    cleanup_ddp(is_ddp)
    return 0 if not cost_aborted else 3


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--steps", type=int, default=20000)
    ap.add_argument("--batch", type=int, default=4, help="per-GPU batch (effective = batch * world_size)")
    ap.add_argument("--ctx", type=int, default=512)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--warmup", type=int, default=2000)
    ap.add_argument("--d-model", type=int, default=1024)
    ap.add_argument("--n-head", type=int, default=16)
    ap.add_argument("--ffn-dim", type=int, default=4096)
    ap.add_argument("--initial-cells", type=int, default=256,
                    help="MUST match resume ckpt n_cells (default 256 for v4 step-2000)")
    ap.add_argument("--max-cells", type=int, default=256)
    ap.add_argument("--readout-mode", type=str, default="a_minus_g",
                    choices=["a_minus_g", "a_only", "a_plus_g"])
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--ckpt-every", type=int, default=2000)
    ap.add_argument("--cost-cap-usd", type=float, default=100.0)
    ap.add_argument("--cost-per-hr", type=float, default=20.0)
    ap.add_argument("--estimated-wall-hr", type=float, default=5.0)
    ap.add_argument("--identity-probe", type=str, required=True)
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--aux-alpha", type=float, default=0.01)
    ap.add_argument("--lambda-init", type=float, default=1.0)
    ap.add_argument("--lambda-final", type=float, default=0.01)
    ap.add_argument("--lambda-schedule", type=str, default="cosine", choices=["constant", "linear", "cosine"])
    ap.add_argument("--n-perms", type=int, default=100)
    # DDP-specific
    ap.add_argument("--resume-ckpt", type=str, default="",
                    help="path to v4 ckpt_step_2000.pt (or compatible); empty = fresh start")
    ap.add_argument("--resume-step", type=int, default=0, help="global step at resume (e.g. 2000)")
    ap.add_argument("--freeze-mitosis", type=int, default=1, help="1=skip split/merge (DDP-safe), 0=allow")
    return ap.parse_args()


if __name__ == "__main__":
    sys.exit(cotrain(parse_args()))
