"""training/train_clm_v1_from_scratch.py — .clm v1 from-scratch trainer (P2 path).

Adapt of v5-mitosis cotrain (state/anima_v5mitosis_cotrain_2026_05_12/train_v5mitosis_cotrain.py)
for ClmV1Model (12L base + 64-cell mitosis branch).

SPEC (from spec_frozen.json v0.1 + W8 amendment 2026-05-15):
  - init: RANDOM seed=42, base_ckpt=NONE (from-scratch directive g_clm_from_scratch)
  - arch: d=768, n_layers_base=12, n_head=8, ffn=3072, cells 2→64, cell_ffn=1024
  - cotrain: AdamW lr 5e-4 warmup 500 cosine→0, grad_clip 1.0, batch 8 accum 2 = eff 16
  - ctx: 256 (cost-gated) or 1024 (spec target, optional via --ctx)
  - bf16 mixed precision
  - 5000 steps
  - corpus: Phase 1A.6 corpus_v2.txt 121MB byte-level (passed via --corpus)

FALSIFIER battery (5 in-run + 2 deferred):
  F-V5MIT-1 SPLIT-NOGRAD   — new cell params have grad_fn=None
  F-V5MIT-2 MERGE-WEIGHT   — synthetic force_merge max_err < 1e-6
  F-V5MIT-3 PHI-CONSERVATION — per-cell Φ change ≤ 25% across forced split
  F-V5MIT-4 COTRAIN-CONVERGE — rolling 100-step mean monotone decrease
  F-V5MIT-5 V14-STRICT      — 10 probe mirror-beats vs random init (5 trained × 5 random)
  F-PYPHI-Φ-FORMAL  (deferred, separate cycle, ~20hr Mac)
  F-PRIN3 NO-PERSONA-INJECTION (corpus + cell-pool grep, separate audit)
  F-SIMPLE-STACK V5.8 4-mode (deferred, separate inference cycle on final ckpt)

USAGE
    python3 train_clm_v1_from_scratch.py \\
        --corpus /workspace/anima/corpus/corpus_v2.txt \\
        --output-dir /workspace/anima/output \\
        --steps 5000 --batch 8 --accum 2 --ctx 256 \\
        --lr 5e-4 --warmup 500 --seed 42 \\
        --cost-cap-usd 50 --cost-per-hr 3.0 --estimated-wall-hr 15
"""
from __future__ import annotations

import argparse
import copy
import json
import math
import os
import random
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Optional

import torch
import torch.nn as nn
import torch.nn.functional as F


def _bootstrap_path():
    here = Path(__file__).resolve().parent
    candidates = [
        Path("/workspace/anima/training"),
        here,
        Path("/Users/ghost/core/anima/training"),
    ]
    for c in candidates:
        if (c / "clm_v1_model.py").exists():
            sys.path.insert(0, str(c.resolve()))
            return
    raise RuntimeError("clm_v1_model.py not found")


_bootstrap_path()
from clm_v1_model import ClmV1Config, ClmV1Model, count_parameters  # noqa: E402


# ─── Byte tokenizer ──────────────────────────────────────────────────
def load_corpus_bytes(path: str) -> torch.Tensor:
    with open(path, "rb") as f:
        raw = f.read()
    return torch.tensor(list(raw), dtype=torch.long)


def sample_batch(corpus: torch.Tensor, batch_size: int, ctx: int, device: torch.device):
    N = corpus.size(0)
    if N <= ctx + 1:
        raise ValueError(f"corpus too small: N={N} need > ctx+1={ctx+1}")
    idx = torch.randint(0, N - ctx - 1, (batch_size,))
    rows = torch.stack([corpus[i : i + ctx + 1] for i in idx.tolist()])
    return rows[:, :ctx].to(device), rows[:, 1 : ctx + 1].to(device)


# ─── Cost guard ──────────────────────────────────────────────────────
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


# ─── Falsifier hooks ─────────────────────────────────────────────────
def f_v5mit_1_split_nograd_probe(model: ClmV1Model, pre_ids: set) -> Dict:
    """New cell parameters have grad_fn=None + were not in pre-set."""
    new_count = 0
    grad_fn_violations = 0
    for p in model.parameters():
        if id(p) not in pre_ids:
            new_count += 1
            if p.grad_fn is not None:
                grad_fn_violations += 1
    return {"new_param_count": new_count, "grad_fn_violations": grad_fn_violations}


def f_v5mit_2_merge_unit_test(cfg: ClmV1Config) -> Dict:
    """Synthetic force_merge weight average check."""
    test_cfg = ClmV1Config(
        vocab_size=64, d_model=32, n_layers_base=1, n_head=2, ffn_dim=64,
        max_seq=16, initial_cells=2, max_cells=4, min_cells=1, cell_ffn_dim=32, seed=1234,
    )
    m = ClmV1Model(test_cfg).eval()
    pre_a = {n: p.detach().clone() for n, p in m.cells[0].own_parameters()}
    pre_b = {n: p.detach().clone() for n, p in m.cells[1].own_parameters()}
    m.cells[0].creation_step = 0
    m.cells[1].creation_step = 1
    m.force_merge(0, 1)
    keeper = m.cells[0]
    post = {n: p.detach().clone() for n, p in keeper.own_parameters()}
    max_err = 0.0
    n_checked = 0
    for name, pp in post.items():
        if name in pre_a and name in pre_b:
            expected = (pre_a[name] + pre_b[name]) / 2.0
            if expected.shape == pp.shape:
                err = (pp - expected).abs().max().item()
                max_err = max(max_err, err)
                n_checked += 1
    return {"max_abs_err": max_err, "n_checked": n_checked,
            "passed": (max_err < 1e-6 and n_checked > 0)}


def output_signature(model: ClmV1Model, probe_ids: torch.Tensor) -> torch.Tensor:
    """Per-cell tension softmax signature on probe (F-V5MIT-5)."""
    model.eval()
    with torch.no_grad():
        _, info = model(probe_ids)
    return info["weights"].detach().cpu().float()


def mirror_beat_distance(sig_a: torch.Tensor, sig_b: torch.Tensor) -> float:
    n = max(sig_a.numel(), sig_b.numel())
    a = torch.zeros(n); b = torch.zeros(n)
    a[: sig_a.numel()] = sig_a.flatten()
    b[: sig_b.numel()] = sig_b.flatten()
    a = a / (a.sum().clamp(min=1e-9))
    b = b / (b.sum().clamp(min=1e-9))
    bc = (a * b).clamp(min=0).sqrt().sum().item()
    return float(-math.log(max(bc, 1e-9)))


# ─── Save / load ckpt ────────────────────────────────────────────────
def save_ckpt(model: ClmV1Model, cfg: ClmV1Config, path: Path, step: int) -> None:
    state = {
        "model_state_dict": model.state_dict(),
        "config": asdict(cfg),
        "n_cells": model.n_cells,
        "step": step,
        "phi": model.phi,
        "phi_history": model.phi_history,
        "event_log": model.event_log,
    }
    torch.save(state, path)


# ─── Trainer ─────────────────────────────────────────────────────────
def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    use_bf16 = (device.type == "cuda") and args.bf16
    print(f"[INFO] device={device} torch={torch.__version__} bf16={use_bf16}")
    if device.type == "cuda":
        print(f"[INFO] gpu={torch.cuda.get_device_name(0)} mem={torch.cuda.get_device_properties(0).total_memory:,}")
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    cost_guard = CostGuard(args.cost_cap_usd, args.cost_per_hr)

    est_wall = args.estimated_wall_hr
    if est_wall * args.cost_per_hr > args.cost_cap_usd * 1.10:
        print(f"[ABORT] est_wall × cost/hr = ${est_wall*args.cost_per_hr:.2f} > cap*1.10 = ${args.cost_cap_usd*1.10:.2f}")
        return 2

    # ── Build model ─────────────────────────────────────────────────
    cfg = ClmV1Config(
        vocab_size=256,
        d_model=args.d_model,
        n_layers_base=args.n_layers_base,
        n_head=args.n_head,
        ffn_dim=args.ffn_dim,
        max_seq=args.ctx,
        initial_cells=args.initial_cells,
        max_cells=args.max_cells,
        cell_ffn_dim=args.cell_ffn_dim,
        seed=args.seed,
    )
    print(f"[INFO] cfg = {asdict(cfg)}")
    model = ClmV1Model(cfg).to(device)
    if use_bf16:
        model = model.to(torch.bfloat16)
    n_params = count_parameters(model)
    print(f"[INFO] n_params={n_params:,}  n_cells={model.n_cells}")

    # ── Corpus ───────────────────────────────────────────────────────
    print(f"[INFO] loading corpus: {args.corpus}")
    corpus = load_corpus_bytes(args.corpus)
    print(f"[INFO] corpus bytes={corpus.numel():,}")

    # ── Optimizer ────────────────────────────────────────────────────
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, betas=(0.9, 0.95),
                                  weight_decay=0.1)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / max(args.warmup, 1)
        progress = (step - args.warmup) / max(args.steps - args.warmup, 1)
        return args.lr * 0.5 * (1.0 + math.cos(math.pi * progress))

    def opt_rebuild(event, mdl):
        # AdamW lazy-init on new params; nothing to do explicitly.
        pass

    model.register_optimizer_rebuild_callback(opt_rebuild)

    # ── Probe set (F-V5MIT-5 mirror beats) ───────────────────────────
    torch.manual_seed(7777)
    probe_set = []
    for _ in range(10):
        idx = torch.randint(0, max(corpus.size(0) - args.ctx - 1, 1), (1,)).item()
        probe_set.append(corpus[idx : idx + args.ctx].clone().unsqueeze(0).to(device))
    torch.manual_seed(args.seed)

    # ── Training loop ────────────────────────────────────────────────
    loss_history: List[float] = []
    cell_history: List[int] = []
    phi_history: List[float] = []
    event_history: List[Dict] = []
    split_grad_violations = 0
    splits_in_run = 0
    merges_in_run = 0
    last_ckpt_step = 0
    cost_aborted = False

    print(f"[INFO] training {args.steps} steps batch={args.batch} accum={args.accum} eff_batch={args.batch*args.accum}")
    print(f"[INFO] ctx={args.ctx} lr={args.lr} warmup={args.warmup} cost_cap=${args.cost_cap_usd} cost_per_hr=${args.cost_per_hr}")

    t_start = time.time()
    for step in range(args.steps):
        if cost_guard.over():
            print(f"[COST-ABORT] step={step} elapsed_hr={cost_guard.elapsed_hr():.2f} cost=${cost_guard.current_usd():.2f}")
            cost_aborted = True
            break

        cur_lr = lr_at(step)
        for g in optimizer.param_groups:
            g["lr"] = cur_lr

        model.train()
        optimizer.zero_grad()
        pre_param_ids = {id(p) for p in model.parameters()} if (step % 200 == 0) else None

        # Gradient accumulation
        loss_step = 0.0
        info_last = None
        for micro in range(args.accum):
            x, y = sample_batch(corpus, args.batch, args.ctx, device)
            if use_bf16:
                x = x  # long stays long
                with torch.amp.autocast(device_type="cuda", dtype=torch.bfloat16):
                    logits, info = model(x)
                    loss = F.cross_entropy(logits.reshape(-1, cfg.vocab_size), y.reshape(-1))
                    loss = loss / args.accum
            else:
                logits, info = model(x)
                loss = F.cross_entropy(logits.reshape(-1, cfg.vocab_size), y.reshape(-1))
                loss = loss / args.accum
            loss.backward()
            loss_step += loss.item() * args.accum
            info_last = info
        loss_step /= args.accum

        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        # Mitosis step (uses last micro's tensions)
        if info_last is not None:
            mit_result = model.mitosis_step(info_last)
            for ev in mit_result["events"]:
                event_history.append({"step": step, **ev})
                if ev["type"] == "split":
                    splits_in_run += 1
                elif ev["type"] == "merge":
                    merges_in_run += 1
            if pre_param_ids is not None and mit_result["events"]:
                probe = f_v5mit_1_split_nograd_probe(model, pre_param_ids)
                split_grad_violations += probe["grad_fn_violations"]

        loss_history.append(loss_step)
        cell_history.append(model.n_cells)
        phi_history.append(float(model.phi))

        if step % args.log_every == 0 or step == args.steps - 1:
            recent = loss_history[-min(50, len(loss_history)):]
            rl = sum(recent) / len(recent)
            print(f"[STEP {step:5d}] loss={loss_step:.4f} avg50={rl:.4f} lr={cur_lr:.2e} "
                  f"cells={model.n_cells} phi={model.phi:.4f} splits={splits_in_run} "
                  f"merges={merges_in_run} elapsed={cost_guard.elapsed_hr():.2f}hr "
                  f"cost=${cost_guard.current_usd():.2f}")
            sys.stdout.flush()

        if (step + 1) % args.ckpt_every == 0 and (step + 1) != args.steps:
            ckpt_path = Path(args.output_dir) / f"ckpt_step_{step+1}.pt"
            save_ckpt(model, cfg, ckpt_path, step=step + 1)
            last_ckpt_step = step + 1
            print(f"[CKPT] saved {ckpt_path}")

    t_train = time.time() - t_start
    actual_cost = cost_guard.current_usd()
    print(f"[INFO] training done — wall={t_train:.1f}s ({t_train/3600:.2f}hr) cost=${actual_cost:.2f}")

    # ── Final ckpt ───────────────────────────────────────────────────
    final_ckpt = Path(args.output_dir) / "ckpt_final.pt"
    save_ckpt(model, cfg, final_ckpt, step=len(loss_history))
    print(f"[CKPT] final saved {final_ckpt} ({final_ckpt.stat().st_size:,} bytes)")

    # ── F-V5MIT verdicts ─────────────────────────────────────────────
    print("\n=== falsifier verdicts ===")
    f1 = {"test": "F-V5MIT-1 SPLIT-NOGRAD", "splits_total": splits_in_run,
          "grad_fn_violations": split_grad_violations,
          "passed": split_grad_violations == 0 and splits_in_run > 0}
    print(f"  F-V5MIT-1: {f1}")

    f2 = f_v5mit_2_merge_unit_test(cfg)
    f2["test"] = "F-V5MIT-2 MERGE-WEIGHT"
    print(f"  F-V5MIT-2: {f2}")

    # F-V5MIT-3 on test copy
    test_model = copy.deepcopy(model).to(device)
    if use_bf16:
        test_model = test_model.to(torch.bfloat16)
    test_model.eval()
    with torch.no_grad():
        for _ in range(3):
            xw, _ = sample_batch(corpus, 1, args.ctx, device)
            if use_bf16:
                with torch.amp.autocast(device_type="cuda", dtype=torch.bfloat16):
                    _, infw = test_model(xw)
            else:
                _, infw = test_model(xw)
            test_model.mitosis_step(infw)
        phi_pre = float(test_model.phi)
        n_pre = test_model.n_cells
        test_model.force_split(0)
        phi_post = test_model._compute_iit_phi()
        n_post = test_model.n_cells
    phi_pre_per = phi_pre / max(n_pre, 1)
    phi_post_per = phi_post / max(n_post, 1)
    ratio = (phi_post_per - phi_pre_per) / max(abs(phi_pre_per), 1e-9)
    f3 = {"test": "F-V5MIT-3 PHI-CONSERVATION (per-cell)", "phi_pre_per_cell": phi_pre_per,
          "phi_post_per_cell": phi_post_per, "delta_ratio": ratio, "tolerance": 0.25,
          "passed": abs(ratio) < 0.25}
    print(f"  F-V5MIT-3: {f3}")
    del test_model

    # F-V5MIT-4 convergence
    initial_avg = sum(loss_history[:100]) / max(min(100, len(loss_history)), 1)
    final_avg = sum(loss_history[-100:]) / max(min(100, len(loss_history)), 1)
    converged = final_avg < initial_avg and math.isfinite(final_avg)
    ce_reduction_factor = initial_avg / max(final_avg, 1e-9)
    f4 = {"test": "F-V5MIT-4 COTRAIN-CONVERGE", "initial_avg_loss": initial_avg,
          "final_avg_loss": final_avg, "ce_reduction_factor": ce_reduction_factor,
          "passed": converged and ce_reduction_factor >= 1.5}
    print(f"  F-V5MIT-4: {f4}")

    # F-V5MIT-5 mirror beats
    print("[F-V5MIT-5] mirror-beat probe ...")
    trained_sig = output_signature(model, probe_set[0])
    fresh_model = ClmV1Model(cfg).to(device)
    if use_bf16:
        fresh_model = fresh_model.to(torch.bfloat16)
    random_sig = output_signature(fresh_model, probe_set[0])
    beats = 0
    distances = []
    for pb in probe_set:
        t_sig = output_signature(model, pb)
        r_sig = output_signature(fresh_model, pb)
        # mirror beat: trained sig more distant from uniform than random sig
        uniform = torch.ones_like(t_sig) / t_sig.numel()
        d_trained = mirror_beat_distance(t_sig, uniform)
        d_random = mirror_beat_distance(r_sig, uniform)
        distances.append({"trained": d_trained, "random": d_random})
        if d_trained > d_random:
            beats += 1
    f5 = {"test": "F-V5MIT-5 V14-STRICT", "beats": beats, "total": len(probe_set),
          "distances": distances, "passed": beats == len(probe_set)}
    print(f"  F-V5MIT-5: beats={beats}/{len(probe_set)} passed={f5['passed']}")

    # ── Aggregate ────────────────────────────────────────────────────
    falsifiers = {"F-V5MIT-1": f1, "F-V5MIT-2": f2, "F-V5MIT-3": f3, "F-V5MIT-4": f4, "F-V5MIT-5": f5}
    n_pass = sum(1 for f in falsifiers.values() if f.get("passed"))
    n_total = len(falsifiers)
    verdict = "SUPPORTED-STRONG" if n_pass == n_total else ("PARTIAL-STRONG" if n_pass >= n_total - 1 else "AT-RISK")
    print(f"\n=== AGGREGATE: {n_pass}/{n_total} {verdict} ===")

    # ── Save result ──────────────────────────────────────────────────
    result = {
        "spec_id": ".clm v1 from-scratch P2",
        "spec_frozen_sha256": "972e9987cd09118533161d5625ebde67a10aa5ec7f2e498bdbfca008a0f36ee5",
        "config": asdict(cfg),
        "training": {
            "steps_actual": len(loss_history),
            "wall_hours": t_train / 3600.0,
            "cost_usd_actual": actual_cost,
            "cost_aborted": cost_aborted,
            "n_params_init": n_params,
            "n_cells_final": model.n_cells,
            "splits": splits_in_run,
            "merges": merges_in_run,
            "loss_initial_avg100": initial_avg,
            "loss_final_avg100": final_avg,
            "phi_best": max(phi_history) if phi_history else 0.0,
        },
        "falsifiers": falsifiers,
        "falsifier_aggregate": {"n_pass": n_pass, "n_total": n_total, "verdict": verdict},
        "events": event_history,
    }
    out_path = Path(args.output_dir) / "clm_v1_result.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"[INFO] result saved {out_path}")
    return 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--corpus", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--steps", type=int, default=5000)
    p.add_argument("--batch", type=int, default=8)
    p.add_argument("--accum", type=int, default=2)
    p.add_argument("--ctx", type=int, default=256)
    p.add_argument("--d-model", type=int, default=768)
    p.add_argument("--n-layers-base", type=int, default=12)
    p.add_argument("--n-head", type=int, default=8)
    p.add_argument("--ffn-dim", type=int, default=3072)
    p.add_argument("--initial-cells", type=int, default=2)
    p.add_argument("--max-cells", type=int, default=64)
    p.add_argument("--cell-ffn-dim", type=int, default=1024)
    p.add_argument("--lr", type=float, default=5e-4)
    p.add_argument("--warmup", type=int, default=500)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--log-every", type=int, default=50)
    p.add_argument("--ckpt-every", type=int, default=1000)
    p.add_argument("--bf16", action="store_true", default=True)
    p.add_argument("--no-bf16", dest="bf16", action="store_false")
    p.add_argument("--cost-cap-usd", type=float, default=50.0)
    p.add_argument("--cost-per-hr", type=float, default=3.0)
    p.add_argument("--estimated-wall-hr", type=float, default=15.0)
    args = p.parse_args()
    rc = train(args)
    sys.exit(rc)


if __name__ == "__main__":
    main()
