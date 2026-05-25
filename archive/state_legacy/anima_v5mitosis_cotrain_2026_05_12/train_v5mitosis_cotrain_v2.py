"""training/train_v5mitosis_cotrain_v2.py — Phase 3 intervention runner.

PURPOSE
    v2 cotrain trainer with two interventions over v1 (`train_v5mitosis_cotrain.py`):

    (1) ENTROPY REGULARIZATION — adds `-entropy_reg_lambda * H(softmax(tens))` to
        loss, preventing the cell-tension softmax from collapsing to a delta on
        one cell (root cause of F-PERSONA-4 KL=0.0 in v1).

        H(p) = -Σ p_i log p_i; maximizing H means encouraging cell-pool to spread
        attention across cells. NB: we ADD a positive lambda * (-H) = subtract
        lambda * H from loss → encourages high entropy. Default lambda=0.1.

    (2) CATEGORY-BALANCED CORPUS — caller points --corpus at the balanced corpus
        (`corpus_persona_balanced.txt`, generated via `generate_balanced_corpus.py`)
        so per-category gradient signal exists.

    Falsifier hooks F-V5MIT-1..5 + F-PERSONA-4 re-measurement are IDENTICAL to v1
    (this is a strict superset of v1 measurement). v1 file is NOT modified — it
    remains SSOT for the prior cotrain.

ADDED FALSIFIER (v2 only):
    F-PERSONA-4-NULL: re-measure with 100-permutation null test (label shuffle).
        Catches false-positive metrics. Spec'd in
        `persona_4_alternative_metrics.py` after Phase 1 investigation.

USAGE
    python3 train_v5mitosis_cotrain_v2.py \
        --corpus /workspace/anima/corpus/corpus_persona_balanced.txt \
        --output-dir /workspace/anima/output \
        --steps 5000 \
        --entropy-reg-lambda 0.1 \
        --identity-probe /workspace/anima/probe/identity_probe.jsonl

HONEST C3
    - entropy-reg may fight the CE loss → final perplexity could be worse than v1.
    - lambda=0.1 is a guess; sweep 0.01/0.1/1.0 in separate runs if budget.
    - if entropy reg alone fails (cell-0 still wins), need architectural change
      (replace softmax with gumbel-softmax or hard top-K MoE gating). That is a
      separate cotrain cycle, NOT scope of this BG.
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
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


# ─── Path bootstrap (same as v1) ────────────────────────────────────
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
from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


# ─── Patch engine to expose live (non-detached) weights ─────────────
def _install_live_weights_hook(engine: MitosisModelEngine) -> None:
    """Monkey-patch engine.forward to also expose non-detached weights via info.

    The original forward stores `weights.detach()` in info["weights"]. For entropy
    regularization we need the live tensor (with grad). We patch by wrapping
    forward and reading the live softmax from a captured intermediate.
    """
    orig_forward = engine.forward

    def patched_forward(input_ids, readout_mode=None):
        if readout_mode is None:
            readout_mode = engine.cfg.readout_mode
        B, T = input_ids.shape
        assert T <= engine.max_seq
        pos = torch.arange(T, device=input_ids.device)
        x = engine.tok_emb(input_ids) + engine.pos_emb(pos).unsqueeze(0)
        cell_outs = []
        cell_tensions = []
        for cell in engine.cells:
            out_i, tension_tok = cell(x, readout_mode=readout_mode)
            cell_outs.append(out_i)
            cell_tensions.append(tension_tok.mean())
        tens = torch.stack(cell_tensions)
        weights = F.softmax(tens, dim=0)
        stacked = torch.stack(cell_outs, dim=0)
        aggregated = (weights.view(-1, 1, 1, 1) * stacked).sum(dim=0)
        h = engine.final_ln(aggregated)
        logits = engine.lm_head(h)
        info = {
            "tensions": [t.item() for t in cell_tensions],
            "tensions_live": tens,           # live (graph-attached) — NEW
            "aggregated": aggregated,
            "weights": weights.detach(),
            "weights_live": weights,         # live (graph-attached) — NEW
            "n_cells": engine.n_cells,
        }
        return logits, info

    engine.forward = patched_forward


# ─── Tokenizer + corpus ──────────────────────────────────────────────
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
    rows = torch.stack([corpus[i : i + ctx + 1] for i in idx.tolist()])
    return rows[:, :ctx].to(device), rows[:, 1 : ctx + 1].to(device)


# ─── Cost guard (same as v1) ─────────────────────────────────────────
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


# ─── F-PERSONA-4 with null-test ──────────────────────────────────────
def f_persona_4_with_null(engine, identity_probe_path, device, n_perms: int = 100):
    probes = []
    with open(identity_probe_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                probes.append(json.loads(line))

    max_seq = engine.cfg.max_seq
    weights_per_prompt: List[List[float]] = []
    cats: List[str] = []
    engine.eval()
    for p in probes:
        ids = text_to_bytes(p["prompt"])[:max_seq]
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            _, info = engine(x)
        weights_per_prompt.append(info["weights"].detach().cpu().float().tolist())
        cats.append(p["category"])

    def kl_pairs(by_cat):
        cat_names = sorted(by_cat.keys())
        avgs = {}
        for c in cat_names:
            rows = by_cat[c]
            n = len(rows[0])
            agg = [0.0] * n
            for r in rows:
                for i in range(n):
                    agg[i] += r[i]
            avgs[c] = [v / len(rows) for v in agg]
        pairs = []
        for i, ci in enumerate(cat_names):
            for j, cj in enumerate(cat_names):
                if j <= i:
                    continue
                p = avgs[ci]
                q = avgs[cj]
                kl = 0.0
                for k in range(len(p)):
                    pi = p[k]
                    qi = max(q[k], 1e-12)
                    if pi > 1e-12:
                        kl += pi * math.log(pi / qi)
                pairs.append(kl)
        return sum(pairs) / max(len(pairs), 1)

    def group(items, labels):
        by_cat = {}
        for it, c in zip(items, labels):
            by_cat.setdefault(c, []).append(it)
        return by_cat

    true_kl = kl_pairs(group(weights_per_prompt, cats))
    rng = random.Random(42)
    null = []
    for _ in range(n_perms):
        sh = list(cats)
        rng.shuffle(sh)
        null.append(kl_pairs(group(weights_per_prompt, sh)))
    null_mean = sum(null) / len(null)
    null_var = sum((x - null_mean) ** 2 for x in null) / len(null)
    null_std = math.sqrt(null_var) if null_var > 0 else 0.0
    z = (true_kl - null_mean) / null_std if null_std > 0 else float("inf")
    n_ge = sum(1 for x in null if x >= true_kl)
    p_val = n_ge / len(null)

    cat_names = sorted(set(cats))
    return {
        "verdict": (
            "PASS"
            if (true_kl >= 0.5 and (z > 3.0 or p_val < 0.01))
            else ("KL_PASS_NULL_FAIL" if true_kl >= 0.5 else "FAIL")
        ),
        "mean_kl": true_kl,
        "threshold": 0.5,
        "null_mean": null_mean,
        "null_std": null_std,
        "z_score_vs_null": z,
        "p_value_one_sided": p_val,
        "passes_null_test": z > 3.0 or p_val < 0.01,
        "n_perms": n_perms,
        "categories": cat_names,
        "n_probes": len(weights_per_prompt),
    }


# ─── Trainer ─────────────────────────────────────────────────────────
def cotrain(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] device={device} torch={torch.__version__} cuda_available={torch.cuda.is_available()}")
    if device.type == "cuda":
        print(f"[INFO] gpu={torch.cuda.get_device_name(0)}")
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    cost_guard = CostGuard(args.cost_cap_usd, args.cost_per_hr)

    est_wall_hr = args.estimated_wall_hr
    if est_wall_hr * args.cost_per_hr > args.cost_cap_usd * 1.10:
        print(f"[ABORT] est cost > cap +10%")
        return 2

    cfg = MitosisModelConfig(
        vocab_size=256,
        d_model=args.d_model,
        n_head=args.n_head,
        ffn_dim=args.ffn_dim,
        max_seq=args.ctx,
        initial_cells=args.initial_cells,
        max_cells=args.max_cells,
        min_cells=2,
        split_patience=3,
        merge_threshold=0.005,
        merge_patience=30,
        noise_scale=0.10,
        lorenz_scale=0.05,
        adaptive_window=100,
        readout_mode=args.readout_mode,
        attention_sharing="auto",
        weight_tied_lm_head=True,
        dropout=0.0,
    )
    print(f"[INFO] cfg = {asdict(cfg)}")
    engine = MitosisModelEngine(cfg).to(device)
    _install_live_weights_hook(engine)
    n_params_init = sum(p.numel() for p in engine.parameters())
    print(f"[INFO] init n_params={n_params_init:,} n_cells={engine.n_cells}")

    print(f"[INFO] loading corpus: {args.corpus}")
    corpus = load_corpus_bytes(args.corpus)
    print(f"[INFO] corpus bytes = {corpus.numel():,}")

    optimizer = torch.optim.AdamW(engine.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / max(args.warmup, 1)
        progress = (step - args.warmup) / max(args.steps - args.warmup, 1)
        return args.lr * 0.5 * (1.0 + math.cos(math.pi * progress))

    loss_history: List[float] = []
    ce_loss_history: List[float] = []
    entropy_history: List[float] = []
    weight_max_history: List[float] = []
    cell_history: List[int] = []
    phi_history: List[float] = []
    event_history: List[Dict] = []
    splits_in_run = 0
    merges_in_run = 0
    t_start = time.time()
    cost_aborted = False

    print(f"[INFO] training {args.steps} steps batch={args.batch} ctx={args.ctx} "
          f"lr={args.lr} entropy_reg_lambda={args.entropy_reg_lambda} cap=${args.cost_cap_usd}")

    for step in range(args.steps):
        if cost_guard.over():
            print(f"[COST-ABORT] step={step}")
            cost_aborted = True
            break

        cur_lr = lr_at(step)
        for g in optimizer.param_groups:
            g["lr"] = cur_lr

        engine.train()
        x, y = sample_batch(corpus, args.batch, args.ctx, device)
        optimizer.zero_grad()
        logits, info = engine(x)
        ce_loss = F.cross_entropy(logits.reshape(-1, cfg.vocab_size), y.reshape(-1))
        # ── Entropy regularization on cell weights ─────────
        # weights_live: (N,) softmax over cells, gradient-attached
        wlive = info["weights_live"]
        # H(w) = -Σ w log w; we want to MAXIMIZE H → subtract lambda * H from loss
        ent = -(wlive.clamp(min=1e-12) * wlive.clamp(min=1e-12).log()).sum()
        loss = ce_loss - args.entropy_reg_lambda * ent
        loss.backward()
        torch.nn.utils.clip_grad_norm_(engine.parameters(), max_norm=1.0)
        optimizer.step()

        mit_result = engine.mitosis_step(info)
        events_this = mit_result["events"]
        if events_this:
            for ev in events_this:
                event_history.append({"step": step, **ev})
                if ev["type"] == "split":
                    splits_in_run += 1
                elif ev["type"] == "merge":
                    merges_in_run += 1

        loss_history.append(loss.item())
        ce_loss_history.append(ce_loss.item())
        entropy_history.append(ent.item())
        weight_max_history.append(float(wlive.detach().max().item()))
        cell_history.append(engine.n_cells)
        phi_history.append(float(engine.phi))

        if step % args.log_every == 0 or step == args.steps - 1:
            recent_loss = sum(loss_history[-50:]) / max(min(50, len(loss_history)), 1)
            recent_ce = sum(ce_loss_history[-50:]) / max(min(50, len(ce_loss_history)), 1)
            recent_ent = sum(entropy_history[-50:]) / max(min(50, len(entropy_history)), 1)
            recent_wmax = sum(weight_max_history[-50:]) / max(min(50, len(weight_max_history)), 1)
            log_n = math.log(max(engine.n_cells, 1))
            print(f"[STEP {step:5d}] loss={loss.item():.4f} avg50={recent_loss:.4f} "
                  f"ce={recent_ce:.4f} ent={recent_ent:.4f}/{log_n:.4f} "
                  f"wmax_avg={recent_wmax:.4f} lr={cur_lr:.2e} cells={engine.n_cells} "
                  f"phi={engine.phi:.4f} splits={splits_in_run} "
                  f"elapsed={cost_guard.elapsed_hr():.2f}hr cost=${cost_guard.current_usd():.2f}")
            sys.stdout.flush()

        if (step + 1) % args.ckpt_every == 0 and (step + 1) != args.steps:
            ckpt_path = Path(args.output_dir) / f"ckpt_step_{step+1}.pt"
            save_ckpt(engine, cfg, ckpt_path, step=step + 1)

    t_train = time.time() - t_start
    actual_cost = cost_guard.current_usd()
    print(f"[INFO] training done — wall={t_train:.1f}s cost=${actual_cost:.2f}")

    final_ckpt = Path(args.output_dir) / "ckpt_final.pt"
    save_ckpt(engine, cfg, final_ckpt, step=len(loss_history))
    print(f"[CKPT] final saved {final_ckpt}")

    # ── F-PERSONA-4 with null test ─────────────────────────
    print("\n=== F-PERSONA-4 with null-permutation test ===")
    p4 = f_persona_4_with_null(engine, args.identity_probe, device, n_perms=args.n_perms)
    print(f"  verdict={p4['verdict']} mean_kl={p4['mean_kl']:.4f} "
          f"null={p4['null_mean']:.4f}±{p4['null_std']:.4f} z={p4['z_score_vs_null']:.2f} "
          f"p={p4['p_value_one_sided']:.4f}")

    initial_avg = sum(loss_history[:100]) / max(min(100, len(loss_history)), 1)
    final_avg = sum(loss_history[-100:]) / max(min(100, len(loss_history)), 1)
    initial_ce = sum(ce_loss_history[:100]) / max(min(100, len(ce_loss_history)), 1)
    final_ce = sum(ce_loss_history[-100:]) / max(min(100, len(ce_loss_history)), 1)
    initial_ent = sum(entropy_history[:100]) / max(min(100, len(entropy_history)), 1)
    final_ent = sum(entropy_history[-100:]) / max(min(100, len(entropy_history)), 1)
    final_wmax = sum(weight_max_history[-100:]) / max(min(100, len(weight_max_history)), 1)

    result = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "device": str(device),
        "torch_version": torch.__version__,
        "intervention": "entropy_reg + balanced_corpus",
        "entropy_reg_lambda": args.entropy_reg_lambda,
        "config": asdict(cfg),
        "training": {
            "steps_actual": len(loss_history),
            "steps_planned": args.steps,
            "wall_seconds": t_train,
            "wall_hours": t_train / 3600.0,
            "cost_usd_actual": actual_cost,
            "cost_aborted": cost_aborted,
            "loss_initial_avg100": initial_avg,
            "loss_final_avg100": final_avg,
            "ce_initial_avg100": initial_ce,
            "ce_final_avg100": final_ce,
            "ent_initial_avg100": initial_ent,
            "ent_final_avg100": final_ent,
            "wmax_final_avg100": final_wmax,
            "log_N_target": math.log(max(engine.n_cells, 1)),
            "splits": splits_in_run,
            "merges": merges_in_run,
            "n_cells_final": engine.n_cells,
            "phi_final": float(engine.phi),
            "n_params_final": sum(p.numel() for p in engine.parameters()),
        },
        "loss_history_sample": loss_history[::max(1, len(loss_history) // 200)],
        "ce_loss_history_sample": ce_loss_history[::max(1, len(ce_loss_history) // 200)],
        "entropy_history_sample": entropy_history[::max(1, len(entropy_history) // 200)],
        "weight_max_history_sample": weight_max_history[::max(1, len(weight_max_history) // 200)],
        "cell_history_sample": cell_history[::max(1, len(cell_history) // 200)],
        "phi_history_sample": phi_history[::max(1, len(phi_history) // 200)],
        "event_history": event_history,
        "f_persona_4_with_null": p4,
    }
    result_path = Path(args.output_dir) / "cotrain_v2_result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n[RESULT] saved {result_path}")
    print(f"[VERDICT] F-PERSONA-4 = {p4['verdict']} (mean_kl={p4['mean_kl']:.4f}, z={p4['z_score_vs_null']:.2f})")
    return 0 if not cost_aborted else 3


def save_ckpt(engine, cfg, path, step):
    ckpt = {
        "model_state_dict": engine.state_dict(),
        "config": asdict(cfg),
        "n_cells": engine.n_cells,
        "step_count": engine.step_count,
        "phi": float(engine.phi),
        "phi_best": float(engine._phi_best),
        "split_threshold": float(engine.split_threshold),
        "cell_metadata": [
            {
                "cell_id": c.cell_id,
                "creation_step": c.creation_step,
                "parent_id": c.parent_id,
                "tension_history_tail": c.tension_history[-10:],
                "process_count": c.process_count,
            }
            for c in engine.cells
        ],
        "lorenz_state": list(engine._lorenz),
        "saved_step": step,
        "saved_ts": time.time(),
    }
    torch.save(ckpt, path)


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--steps", type=int, default=5000)
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--ctx", type=int, default=256)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--warmup", type=int, default=500)
    ap.add_argument("--d-model", type=int, default=384)
    ap.add_argument("--n-head", type=int, default=6)
    ap.add_argument("--ffn-dim", type=int, default=1536)
    ap.add_argument("--initial-cells", type=int, default=2)
    ap.add_argument("--max-cells", type=int, default=64)
    ap.add_argument("--readout-mode", type=str, default="a_minus_g",
                    choices=["a_minus_g", "a_only", "a_plus_g"])
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--ckpt-every", type=int, default=5000)
    ap.add_argument("--cost-cap-usd", type=float, default=40.0)
    ap.add_argument("--cost-per-hr", type=float, default=2.70)
    ap.add_argument("--estimated-wall-hr", type=float, default=2.0)
    ap.add_argument("--identity-probe", type=str, required=True)
    ap.add_argument("--entropy-reg-lambda", type=float, default=0.1,
                    help="Weight on -H(softmax(tens)) in loss (encourages cell-pool diversity)")
    ap.add_argument("--n-perms", type=int, default=100,
                    help="Label permutations for F-PERSONA-4 null test")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    sys.exit(cotrain(args))
