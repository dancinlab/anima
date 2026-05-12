"""training/cotrain_v5mitosis_v6_cellparallel.py — v6 cell-parallel cotrain.

POST-★★★★★ 2026-05-12 BG (c) — mitosis-native parallelism.

ARCH SUMMARY
    • cotrain_v5mitosis_v4.py 의 cell-parallel variant.
    • model = MitosisModelEngineCellParallel (cells distributed across W GPUs).
    • routing = TopKMoERouter (same as v4) — replicated across all ranks, DDP-
      wrapped so gradients sync. router output dim = max_cells = 256.
    • shared modules (tok_emb / pos_emb / final_ln / lm_head / router) →
      DDP all-reduce on backward (handled by torch.nn.parallel.DistributedDataParallel
      OR manual gradient broadcast).
    • cell-owned modules (cells[*].ln1/attn/ln2/ffn_a/ffn_g) → LOCAL per rank,
      no DDP sync.
    • forward: per-rank local cells forward → all_gather(tensions) →
      softmax(global) → local weighted sum → all_reduce(SUM) → final_ln + lm_head.

LAUNCH
    torchrun --nproc_per_node=8 cotrain_v5mitosis_v6_cellparallel.py \\
        --corpus corpus/corpus_5cat_balanced.txt \\
        --output-dir output \\
        --steps 5000 --batch 8 --ctx 512 --lr 1e-4 --warmup 500 \\
        --d-model 1024 --n-head 16 --ffn-dim 4096 --initial-cells 8 --max-cells 256 \\
        --identity-probe probe/identity_probe.jsonl --n-perms 100

HONEST C3 (≥ 6)
    1. We DO NOT use torch.nn.parallel.DistributedDataParallel directly because
       the cells per rank are STRUCTURALLY DIFFERENT (different cell count,
       different cell-owned weights). DDP requires identical module trees.
       Instead: manual gradient all_reduce on SHARED params after backward.
    2. The router is replicated across ranks — its gradients ARE sync'd via
       manual all_reduce (treat as shared).
    3. Per-step wall ETA: v4 cells=66 single-GPU bottleneck = 3.18s.
       v6 8-GPU = ~32 cells/rank PARALLEL forward (~0.4s) + all_reduce overhead
       (~0.01s for d=1024 ctx=512 batch=8). Target: < 0.6s/step. Real number =
       reported honestly post-run; speedup NOT guaranteed.
    4. Mitosis split events are LOCAL-shard only (cross-GPU migration TODO).
       Some ranks may hit shard cap while others have headroom → reject.
       Monitoring: per-rank n_local_cells variance.
    5. F-PERSONA-4a/4b measurement = rank 0 only (gather aggregated hidden,
       compute null permutation on rank 0). Other ranks block on barrier.
    6. ckpt = sharded (each rank writes own cells state_dict). final ckpt
       merge to single-GPU file = post-training step (separate script, not
       inline here for v6 first cycle).
    7. Corpus sampling: each rank samples INDEPENDENTLY (different random
       offsets per rank). This is data-parallel-ish at the corpus level.
       Alternative: broadcast a single (x,y) batch from rank 0 — would force
       lock-step and waste D bandwidth. The independent sample variant uses
       each GPU effectively as a separate gradient computation, which is the
       correct semantics here (router/shared grads averaged via all_reduce).
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
import torch.nn as nn
import torch.nn.functional as F
import torch.distributed as dist


# ─── Path bootstrap ──────────────────────────────────────────────────
def _bootstrap_path():
    here = Path(__file__).resolve().parent
    candidates = [
        Path("/workspace/anima/training"),
        here / "../training",
        here.parent / "training",
        Path("/Users/ghost/core/anima/training"),
        here,
    ]
    for c in candidates:
        if (c / "mitosis_model_v5.py").exists():
            sys.path.insert(0, str(c.resolve()))
            return
    raise RuntimeError("mitosis_model_v5.py not found in any search path")


_bootstrap_path()
from mitosis_model_v5 import MitosisModelConfig  # noqa: E402
from mitosis_model_v5_cellparallel import MitosisModelEngineCellParallel  # noqa: E402


# ─── Distributed setup ──────────────────────────────────────────────

def setup_distributed():
    if "RANK" in os.environ and "WORLD_SIZE" in os.environ:
        rank = int(os.environ["RANK"])
        world_size = int(os.environ["WORLD_SIZE"])
        local_rank = int(os.environ.get("LOCAL_RANK", rank))
        dist.init_process_group(backend="nccl", rank=rank, world_size=world_size)
        torch.cuda.set_device(local_rank)
        return rank, world_size, local_rank
    return 0, 1, 0


def is_main() -> bool:
    return (not dist.is_initialized()) or dist.get_rank() == 0


def log_main(msg: str):
    if is_main():
        print(msg, flush=True)


# ─── Tokenizer / corpus ─────────────────────────────────────────────
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


# ─── Routing (TopK MoE) ─────────────────────────────────────────────
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


def install_routing_fix_cellparallel(engine, router: TopKMoERouter, top_k: int):
    """Patch engine.forward to route via router + cell-parallel aggregation.

    Differs from v4: aggregation is now cross-GPU all_reduce SUM after router
    weights * local_outs. The router itself is REPLICATED (one copy per rank,
    gradients sync'd).
    """
    object.__setattr__(engine, "_topk_router", router)
    object.__setattr__(engine, "_top_k", top_k)

    def patched_forward(input_ids, readout_mode=None):
        if readout_mode is None:
            readout_mode = engine.cfg.readout_mode
        B, T = input_ids.shape
        assert T <= engine.max_seq
        pos = torch.arange(T, device=input_ids.device)
        x = engine.tok_emb(input_ids) + engine.pos_emb(pos).unsqueeze(0)

        # local cells forward
        local_outs: List[torch.Tensor] = []
        local_tensions: List[torch.Tensor] = []
        for cell in engine.cells:
            out_i, tension_tok = cell(x, readout_mode=readout_mode)
            local_outs.append(out_i)
            local_tensions.append(tension_tok.mean())

        if local_outs:
            local_tens_t = torch.stack(local_tensions)
        else:
            local_tens_t = torch.zeros(0, device=x.device, dtype=x.dtype)

        # Compute router gate on full n_global_cells
        n_global = engine.n_cells
        weights_router, gate_full, dispatch_mask = router(x, n_global, top_k)

        # Determine local slice from shard sizes (compute via all_gather of sizes)
        if engine.world_size > 1:
            sizes_tensor = torch.tensor([local_tens_t.numel()], device=x.device, dtype=torch.long)
            sizes_list = [torch.zeros_like(sizes_tensor) for _ in range(engine.world_size)]
            dist.all_gather(sizes_list, sizes_tensor)
            sizes = [int(s.item()) for s in sizes_list]
        else:
            sizes = [local_tens_t.numel()]
        local_start = sum(sizes[:engine.rank])
        local_end = local_start + (sizes[engine.rank] if engine.rank < len(sizes) else 0)

        if local_outs and local_end > local_start:
            local_weights = weights_router[local_start:local_end]
            stacked = torch.stack(local_outs, dim=0)
            local_weighted = (local_weights.view(-1, 1, 1, 1) * stacked).sum(dim=0)
        else:
            local_weighted = torch.zeros(B, T, engine.d_model, device=x.device, dtype=x.dtype)

        if engine.world_size > 1:
            dist.all_reduce(local_weighted, op=dist.ReduceOp.SUM)
        aggregated = local_weighted

        h = engine.final_ln(aggregated)
        logits = engine.lm_head(h)

        # tensions per-cell global (for mitosis + monitoring) — gather as well
        if engine.world_size > 1:
            max_sz = max(sizes) if sizes else 0
            pad_local = torch.zeros(max_sz, device=x.device, dtype=x.dtype)
            if local_tens_t.numel() > 0:
                pad_local[: local_tens_t.numel()] = local_tens_t
            gathered = [torch.zeros_like(pad_local) for _ in range(engine.world_size)]
            dist.all_gather(gathered, pad_local)
            tens_pieces = []
            for r, sz in enumerate(sizes):
                tens_pieces.append(gathered[r][:sz])
            global_tensions = torch.cat(tens_pieces, dim=0)
        else:
            global_tensions = local_tens_t

        info = {
            "tensions": [float(t) for t in global_tensions.detach().cpu().float().tolist()],
            "aggregated": aggregated,
            "weights": weights_router.detach(),
            "weights_live": weights_router,
            "gate_full_live": gate_full,
            "dispatch_mask": dispatch_mask,
            "n_cells": n_global,
            "n_local_cells": engine.n_local_cells,
            "local_shard": (local_start, local_end),
            "shard_sizes": sizes,
        }
        return logits, info

    engine.forward = patched_forward


def load_balance_aux(gate_full: torch.Tensor, dispatch_mask: torch.Tensor, n_cells: int) -> torch.Tensor:
    denom = dispatch_mask.sum().clamp(min=1e-12)
    f = dispatch_mask / denom
    return n_cells * (f * gate_full).sum()


# ─── Manual gradient all_reduce for shared params ────────────────────
def all_reduce_shared_grads(shared_params: List[torch.nn.Parameter], world_size: int):
    """Average gradients across ranks for SHARED params (tok_emb / pos_emb /
    final_ln / lm_head / router). cell-owned params are local-only."""
    if world_size <= 1:
        return
    for p in shared_params:
        if p.grad is not None:
            dist.all_reduce(p.grad.data, op=dist.ReduceOp.SUM)
            p.grad.data.div_(world_size)


# ─── F-PERSONA-4a / 4b (rank 0 only) ────────────────────────────────
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
        "metric": "F-PERSONA-4a routing v6 cell-parallel",
        "verdict": verdict,
        "threshold_kl": 0.5, "threshold_z": 3.0,
        "topk_weights": r_weights, "soft_gate": r_gate,
        "n_perms": n_perms, "categories": cat_names,
        "n_probes": len(weights_per_prompt),
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
        "metric": "F-PERSONA-4b content v6 cell-parallel (M4 aggregated hidden cosine)",
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


def save_ckpt_sharded(engine, router, cfg, path, step, top_k, rank: int):
    """Each rank saves its OWN cells + a shared copy of common modules.
    Shared modules are identical across ranks (DDP-synced), so rank 0's copy
    is the canonical shared. cell-owned weights are unique per rank.
    """
    shared_state = {}
    for name, p in engine.tok_emb.state_dict().items():
        shared_state[f"tok_emb.{name}"] = p
    for name, p in engine.pos_emb.state_dict().items():
        shared_state[f"pos_emb.{name}"] = p
    for name, p in engine.final_ln.state_dict().items():
        shared_state[f"final_ln.{name}"] = p
    for name, p in engine.lm_head.state_dict().items():
        shared_state[f"lm_head.{name}"] = p

    cells_state = {}
    cell_meta = []
    for li, cell in enumerate(engine.cells):
        sd = cell.state_dict()
        for k, v in sd.items():
            cells_state[f"cells.{li}.{k}"] = v
        cell_meta.append({
            "local_idx": li,
            "cell_id": cell.cell_id,
            "creation_step": cell.creation_step,
            "parent_id": cell.parent_id,
            "process_count": cell.process_count,
        })

    ckpt = {
        "rank": rank,
        "world_size": engine.world_size,
        "n_local_cells": engine.n_local_cells,
        "n_cells_global": engine.n_cells,
        "shared_state": shared_state if rank == 0 else None,  # only rank 0 keeps shared
        "router_state": router.state_dict() if rank == 0 else None,
        "router_top_k": top_k,
        "cells_state": cells_state,
        "cell_meta": cell_meta,
        "config": asdict(cfg),
        "step_count": engine.step_count,
        "phi": float(engine.phi),
        "phi_best": float(engine._phi_best),
        "split_threshold": float(engine.split_threshold),
        "lorenz_state": list(engine._lorenz),
        "saved_step": step,
        "saved_ts": time.time(),
        "trainer": "v6-cellparallel (mitosis-native distributed cells)",
    }
    torch.save(ckpt, path)


def cotrain(args):
    rank, world_size, local_rank = setup_distributed()
    device = torch.device(f"cuda:{local_rank}" if torch.cuda.is_available() else "cpu")
    log_main(f"[INFO] world_size={world_size} rank={rank} local_rank={local_rank} device={device}")
    if device.type == "cuda":
        torch.cuda.set_device(device)
        if is_main():
            print(f"[INFO] gpu0={torch.cuda.get_device_name(0)}", flush=True)
    torch.manual_seed(args.seed + rank)  # different seed per rank for sample independence
    random.seed(args.seed + rank)

    if is_main():
        Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    if dist.is_initialized():
        dist.barrier()

    cost_guard = CostGuard(args.cost_cap_usd, args.cost_per_hr)
    if args.estimated_wall_hr * args.cost_per_hr > args.cost_cap_usd * 1.10:
        log_main("[ABORT] est cost > cap +10%")
        return 2

    cfg = MitosisModelConfig(
        vocab_size=256, d_model=args.d_model, n_head=args.n_head, ffn_dim=args.ffn_dim,
        max_seq=args.ctx, initial_cells=args.initial_cells, max_cells=args.max_cells,
        min_cells=2, split_patience=3, merge_threshold=0.005, merge_patience=30,
        noise_scale=0.10, lorenz_scale=0.05, adaptive_window=100,
        readout_mode=args.readout_mode, attention_sharing="auto",
        weight_tied_lm_head=True, dropout=0.0,
    )
    log_main(f"[INFO] cfg = {asdict(cfg)}")
    engine = MitosisModelEngineCellParallel(cfg).to(device)
    router = TopKMoERouter(d_in=cfg.d_model, max_cells=cfg.max_cells).to(device)

    # Broadcast initial weights from rank 0 to all ranks for SHARED modules
    # so they start identical (DDP-broadcast init).
    if world_size > 1:
        for p in engine.tok_emb.parameters():
            dist.broadcast(p.data, src=0)
        for p in engine.pos_emb.parameters():
            dist.broadcast(p.data, src=0)
        for p in engine.final_ln.parameters():
            dist.broadcast(p.data, src=0)
        for p in engine.lm_head.parameters():
            dist.broadcast(p.data, src=0)
        for p in router.parameters():
            dist.broadcast(p.data, src=0)

    install_routing_fix_cellparallel(engine, router, top_k=args.top_k)

    # Param groups: SHARED params (sync'd) vs CELL-LOCAL params (no sync)
    shared_params = (
        list(engine.tok_emb.parameters())
        + list(engine.pos_emb.parameters())
        + list(engine.final_ln.parameters())
        + list(router.parameters())
    )
    # lm_head shares weight with tok_emb (tied) → don't double-list (would
    # double-count gradient). final_ln has its own params.
    if not cfg.weight_tied_lm_head:
        shared_params += list(engine.lm_head.parameters())

    # Cell-owned params (per-rank local, no sync)
    cell_params = []
    for cell in engine.cells:
        for name, p in cell.own_parameters():
            cell_params.append(p)

    all_params = shared_params + cell_params
    optimizer = torch.optim.AdamW(all_params, lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    n_shared = sum(p.numel() for p in shared_params)
    n_local = sum(p.numel() for p in cell_params)
    log_main(f"[INFO] params: shared={n_shared:,} cell-local(rank{rank})={n_local:,}")

    corpus = load_corpus_bytes(args.corpus)
    log_main(f"[INFO] corpus={args.corpus} bytes={corpus.numel():,}")

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / max(args.warmup, 1)
        progress = (step - args.warmup) / max(args.steps - args.warmup, 1)
        return args.lr * 0.5 * (1.0 + math.cos(math.pi * progress))

    hist = {k: [] for k in ("loss", "ce", "aux", "ent_gate", "wmax", "lambda", "cells",
                            "n_local", "step_wall")}
    splits_in_run = 0
    t_start = time.time()
    cost_aborted = False
    log_main(f"[INFO] top_k={args.top_k} aux_alpha={args.aux_alpha} "
             f"λ_init={args.lambda_init} λ_final={args.lambda_final} sched={args.lambda_schedule}")

    for step in range(args.steps):
        t_step = time.time()
        if cost_guard.over():
            log_main(f"[COST-ABORT] step={step}")
            cost_aborted = True
            break
        cur_lr = lr_at(step)
        for g in optimizer.param_groups:
            g["lr"] = cur_lr
        cur_lambda = lambda_at(step, args.steps, args.warmup,
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

        # All-reduce shared param gradients across ranks (DDP-equivalent)
        all_reduce_shared_grads(shared_params, world_size)

        torch.nn.utils.clip_grad_norm_(all_params, max_norm=1.0)
        optimizer.step()

        # Mitosis step (local-shard only)
        mit_result = engine.mitosis_step(info)
        local_splits = 0
        for ev in mit_result["events"]:
            if ev["type"] == "split":
                splits_in_run += 1
                local_splits += 1

        # If any rank split, optimizer state for new cell params needs rebuild.
        # Simple approach: rebuild optimizer after any split (rare event).
        if local_splits > 0:
            new_cell_params = []
            for cell in engine.cells:
                for name, p in cell.own_parameters():
                    new_cell_params.append(p)
            all_params = shared_params + new_cell_params
            optimizer = torch.optim.AdamW(all_params, lr=cur_lr, betas=(0.9, 0.95), weight_decay=0.0)

        w = info["weights"].detach()
        step_wall = time.time() - t_step
        hist["loss"].append(loss.item())
        hist["ce"].append(ce.item())
        hist["aux"].append(float(aux.item()))
        hist["ent_gate"].append(float(ent_gate.item()))
        hist["wmax"].append(float(w.max().item()))
        hist["lambda"].append(cur_lambda)
        hist["cells"].append(engine.n_cells)
        hist["n_local"].append(engine.n_local_cells)
        hist["step_wall"].append(step_wall)

        if step % args.log_every == 0 or step == args.steps - 1:
            def _m(k, n=50):
                arr = hist[k][-n:]
                return sum(arr) / max(len(arr), 1)
            mem_str = ""
            if device.type == "cuda":
                mem_str = f" vram={torch.cuda.max_memory_allocated()/1e9:.1f}GB"
            if is_main():
                print(f"[STEP {step:5d}] loss={loss.item():.4f} ce={_m('ce'):.4f} "
                      f"aux={_m('aux'):.4f} ent_gate={_m('ent_gate'):.4f} "
                      f"wmax={_m('wmax'):.4f} "
                      f"λ={cur_lambda:.4f} cells={engine.n_cells}(rank{rank}={engine.n_local_cells}) "
                      f"splits={splits_in_run} step_wall={_m('step_wall')*1000:.0f}ms "
                      f"cost=${cost_guard.current_usd():.2f}{mem_str}", flush=True)

        if args.ckpt_every > 0 and (step + 1) % args.ckpt_every == 0 and (step + 1) != args.steps:
            cp = Path(args.output_dir) / f"ckpt_step_{step+1}_rank{rank}.pt"
            save_ckpt_sharded(engine, router, cfg, cp, step + 1, args.top_k, rank)
            if is_main():
                try:
                    snap_a = f_persona_4a_routing(engine, args.identity_probe, device, n_perms=30)
                    snap_b = f_persona_4b_content(engine, args.identity_probe, device, n_perms=30)
                    print(f"  [SNAP {step+1}] 4a KL={snap_a['topk_weights']['mean_kl']:.4f} "
                          f"z={snap_a['topk_weights']['z_score_vs_null']:.2f} | "
                          f"4b cos_z={snap_b['z_score_vs_null']:.2f}", flush=True)
                except Exception as e:
                    print(f"  [SNAP {step+1}] failed: {e}", flush=True)
            if dist.is_initialized():
                dist.barrier()

    t_train = time.time() - t_start
    log_main(f"[INFO] training done wall={t_train:.1f}s cost=${cost_guard.current_usd():.2f}")
    final_path = Path(args.output_dir) / f"ckpt_final_rank{rank}.pt"
    save_ckpt_sharded(engine, router, cfg, final_path, len(hist["loss"]), args.top_k, rank)
    if dist.is_initialized():
        dist.barrier()

    # F-PERSONA / F-V5MIT on rank 0
    if is_main():
        print("\n=== F-PERSONA-4a routing v6 (top-K MoE cell-parallel) ===")
        p4a = f_persona_4a_routing(engine, args.identity_probe, device, n_perms=args.n_perms)
        tw = p4a["topk_weights"]
        print(f"  verdict={p4a['verdict']} KL={tw['mean_kl']:.4f} null={tw['null_mean']:.4f}±{tw['null_std']:.4f} "
              f"z={tw['z_score_vs_null']:.2f} p={tw['p_value_one_sided']:.4f}")
        if p4a["soft_gate"]:
            sg = p4a["soft_gate"]
            print(f"  (soft gate) KL={sg['mean_kl']:.4f} z={sg['z_score_vs_null']:.2f}")

        print("\n=== F-PERSONA-4b content v6 (M4 aggregated cosine) ===")
        p4b = f_persona_4b_content(engine, args.identity_probe, device, n_perms=args.n_perms)
        print(f"  verdict={p4b['verdict']} cos_dist={p4b['true']:.6f} null={p4b['null_mean']:.6f}±{p4b['null_std']:.6f} "
              f"z={p4b['z_score_vs_null']:.2f} p={p4b['p_value_one_sided']:.4f} (v2 carry z={p4b['v2_carry_z']:.2f})")

        print("\n=== F-V5MIT-1..5 regression v6 ===")
        fv = f_v5mit_regression(engine, splits_in_run, sum(hist["ce"][-100:]) / max(min(100, len(hist["ce"])), 1))
        print(f"  {fv['verdict']}  " + " ".join(
            f"{k.split('_')[0]}={'P' if v['pass'] else 'F'}" for k, v in fv["checks"].items()))

        mean_step_wall = sum(hist["step_wall"]) / max(len(hist["step_wall"]), 1)
        result = {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "trainer": "v6-cellparallel (mitosis-native: cells distributed across {} GPUs)".format(world_size),
            "world_size": world_size,
            "routing_fix": {
                "top_k": args.top_k, "aux_alpha": args.aux_alpha,
                "lambda_init": args.lambda_init, "lambda_final": args.lambda_final,
                "lambda_schedule": args.lambda_schedule,
                "router": "Linear(d_model -> max_cells), DDP-replicated, gradient all_reduced",
            },
            "config": asdict(cfg),
            "training": {
                "wall_seconds": t_train, "wall_hours": t_train / 3600.0,
                "cost_usd_actual": cost_guard.current_usd(), "cost_aborted": cost_aborted,
                "ce_final_avg100": sum(hist["ce"][-100:]) / max(min(100, len(hist["ce"])), 1),
                "step_wall_avg_seconds": mean_step_wall,
                "step_wall_p50_ms": sorted(hist["step_wall"])[len(hist["step_wall"]) // 2] * 1000 if hist["step_wall"] else 0,
                "splits": splits_in_run,
                "n_cells_final": engine.n_cells,
                "n_local_cells_final_rank0": engine.n_local_cells,
                "phi_final_rank0": float(engine.phi),
                "phi_best_rank0": float(engine._phi_best),
            },
            "history_sample": {k: v[::max(1, len(v) // 200)] for k, v in hist.items()},
            "f_persona_4a_routing": p4a,
            "f_persona_4b_content": p4b,
            "f_v5mit_regression": fv,
        }
        out = Path(args.output_dir) / "cotrain_v6_cellparallel_result.json"
        out.write_text(json.dumps(result, indent=2, default=str))
        print(f"\n[RESULT] {out}")
        print(f"[VERDICT] 4a={p4a['verdict']} (KL={tw['mean_kl']:.4f} z={tw['z_score_vs_null']:.2f}) | "
              f"4b={p4b['verdict']} (z={p4b['z_score_vs_null']:.2f}) | F-V5MIT={fv['verdict']} | "
              f"avg_step={mean_step_wall*1000:.0f}ms")
    if dist.is_initialized():
        dist.barrier()
        dist.destroy_process_group()
    return 0 if not cost_aborted else 3


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--steps", type=int, default=5000)
    ap.add_argument("--batch", type=int, default=8)
    ap.add_argument("--ctx", type=int, default=512)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--warmup", type=int, default=500)
    ap.add_argument("--d-model", type=int, default=1024)
    ap.add_argument("--n-head", type=int, default=16)
    ap.add_argument("--ffn-dim", type=int, default=4096)
    ap.add_argument("--initial-cells", type=int, default=8)
    ap.add_argument("--max-cells", type=int, default=256)
    ap.add_argument("--readout-mode", type=str, default="a_minus_g",
                    choices=["a_minus_g", "a_only", "a_plus_g"])
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--ckpt-every", type=int, default=1000)
    ap.add_argument("--cost-cap-usd", type=float, default=80.0)
    ap.add_argument("--cost-per-hr", type=float, default=20.0)
    ap.add_argument("--estimated-wall-hr", type=float, default=3.0)
    ap.add_argument("--identity-probe", type=str, required=True)
    ap.add_argument("--top-k", type=int, default=8)
    ap.add_argument("--aux-alpha", type=float, default=0.01)
    ap.add_argument("--lambda-init", type=float, default=1.0)
    ap.add_argument("--lambda-final", type=float, default=0.01)
    ap.add_argument("--lambda-schedule", type=str, default="cosine", choices=["constant", "linear", "cosine"])
    ap.add_argument("--n-perms", type=int, default=100)
    return ap.parse_args()


if __name__ == "__main__":
    sys.exit(cotrain(parse_args()))
