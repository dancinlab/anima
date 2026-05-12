"""training/train_v5mitosis_cotrain_v3.py — Phase 3 follow-up: λ sweep + anneal.

PURPOSE
    v3 = v2 + scheduled entropy regularization (anneal high→low) + λ sweep support.

    v2 finding (PSCC §45): λ=0.1 entropy reg INSUFFICIENT — once CE drops below
    ~5, CE gradient unbounded while entropy term bounded by log(N)=4.16. wmax
    collapsed back to 1.0 by step 250+.

    v3 path (f):
      - λ_init high (≥ 10 × CE_final, e.g. 50) to keep cells uniform during
        early training while corpus statistics specialize per-category
      - λ_final low (≤ CE_final, e.g. 0.5) to allow some specialization but
        not full monopoly
      - cosine anneal between

    HONEST C3:
      - if anneal still collapses to monopoly, real fix = architectural change
        (gumbel-softmax + hard top-K MoE gating with load-balancing aux loss)
      - λ_init=50 is a guess; may be too aggressive (uniform weights early
        → no per-cell specialization signal → CE can't drop)
      - if CE doesn't converge, ablate λ_init

USAGE
    python3 train_v5mitosis_cotrain_v3.py \
        --corpus corpus/corpus_persona_balanced.txt \
        --output-dir output \
        --steps 5000 \
        --lambda-init 50.0 \
        --lambda-final 0.5 \
        --identity-probe probe/identity_probe.jsonl

ENVELOPE
    Same as v2 (d=384, cells=64, batch=32, ctx=256, 5K step). Cost ≈ $1.30 H100.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Tuple

import torch
import torch.nn.functional as F


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
    raise RuntimeError("mitosis_model_v5.py not found")


_bootstrap_path()
from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


# Reuse v2 helpers
sys.path.insert(0, str(Path(__file__).resolve().parent))
from train_v5mitosis_cotrain_v2 import (  # noqa: E402
    _install_live_weights_hook,
    text_to_bytes,
    load_corpus_bytes,
    sample_batch,
    CostGuard,
    f_persona_4_with_null,
    save_ckpt,
)


def lambda_at(step: int, total: int, warmup: int, lam_init: float, lam_final: float,
              schedule: str = "cosine") -> float:
    if schedule == "constant":
        return lam_init
    if step < warmup:
        return lam_init
    progress = (step - warmup) / max(total - warmup, 1)
    progress = min(max(progress, 0.0), 1.0)
    if schedule == "linear":
        return lam_init + (lam_final - lam_init) * progress
    if schedule == "cosine":
        return lam_final + 0.5 * (lam_init - lam_final) * (1.0 + math.cos(math.pi * progress))
    raise ValueError(f"unknown schedule: {schedule}")


def cotrain(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] device={device} torch={torch.__version__}")
    if device.type == "cuda":
        print(f"[INFO] gpu={torch.cuda.get_device_name(0)}")
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    cost_guard = CostGuard(args.cost_cap_usd, args.cost_per_hr)

    if args.estimated_wall_hr * args.cost_per_hr > args.cost_cap_usd * 1.10:
        print("[ABORT] est cost > cap +10%")
        return 2

    cfg = MitosisModelConfig(
        vocab_size=256, d_model=args.d_model, n_head=args.n_head, ffn_dim=args.ffn_dim,
        max_seq=args.ctx, initial_cells=args.initial_cells, max_cells=args.max_cells,
        min_cells=2, split_patience=3, merge_threshold=0.005, merge_patience=30,
        noise_scale=0.10, lorenz_scale=0.05, adaptive_window=100,
        readout_mode=args.readout_mode, attention_sharing="auto",
        weight_tied_lm_head=True, dropout=0.0,
    )
    print(f"[INFO] cfg = {asdict(cfg)}")
    engine = MitosisModelEngine(cfg).to(device)
    _install_live_weights_hook(engine)
    print(f"[INFO] n_params={sum(p.numel() for p in engine.parameters()):,}")

    corpus = load_corpus_bytes(args.corpus)
    print(f"[INFO] corpus={args.corpus} bytes={corpus.numel():,}")

    optimizer = torch.optim.AdamW(engine.parameters(), lr=args.lr, betas=(0.9, 0.95), weight_decay=0.0)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / max(args.warmup, 1)
        progress = (step - args.warmup) / max(args.steps - args.warmup, 1)
        return args.lr * 0.5 * (1.0 + math.cos(math.pi * progress))

    loss_history: List[float] = []
    ce_loss_history: List[float] = []
    entropy_history: List[float] = []
    wmax_history: List[float] = []
    lambda_history: List[float] = []
    cell_history: List[int] = []
    splits_in_run = 0
    t_start = time.time()
    cost_aborted = False

    print(f"[INFO] λ_init={args.lambda_init} λ_final={args.lambda_final} schedule={args.lambda_schedule}")

    for step in range(args.steps):
        if cost_guard.over():
            print(f"[COST-ABORT] step={step}")
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
        wlive = info["weights_live"]
        ent = -(wlive.clamp(min=1e-12) * wlive.clamp(min=1e-12).log()).sum()
        loss = ce - cur_lambda * ent
        loss.backward()
        torch.nn.utils.clip_grad_norm_(engine.parameters(), max_norm=1.0)
        optimizer.step()

        mit_result = engine.mitosis_step(info)
        for ev in mit_result["events"]:
            if ev["type"] == "split":
                splits_in_run += 1

        loss_history.append(loss.item())
        ce_loss_history.append(ce.item())
        entropy_history.append(ent.item())
        wmax_history.append(float(wlive.detach().max().item()))
        lambda_history.append(cur_lambda)
        cell_history.append(engine.n_cells)

        if step % args.log_every == 0 or step == args.steps - 1:
            recent_ce = sum(ce_loss_history[-50:]) / max(min(50, len(ce_loss_history)), 1)
            recent_ent = sum(entropy_history[-50:]) / max(min(50, len(entropy_history)), 1)
            recent_w = sum(wmax_history[-50:]) / max(min(50, len(wmax_history)), 1)
            print(f"[STEP {step:5d}] loss={loss.item():.4f} ce={recent_ce:.4f} "
                  f"ent={recent_ent:.4f}/{math.log(max(engine.n_cells,1)):.4f} "
                  f"wmax={recent_w:.4f} λ={cur_lambda:.4f} cells={engine.n_cells} "
                  f"splits={splits_in_run} elapsed={cost_guard.elapsed_hr():.2f}hr "
                  f"cost=${cost_guard.current_usd():.2f}")
            sys.stdout.flush()

        if (step + 1) % args.ckpt_every == 0 and (step + 1) != args.steps:
            save_ckpt(engine, cfg, Path(args.output_dir) / f"ckpt_step_{step+1}.pt", step=step + 1)

    t_train = time.time() - t_start
    print(f"[INFO] training done wall={t_train:.1f}s cost=${cost_guard.current_usd():.2f}")

    save_ckpt(engine, cfg, Path(args.output_dir) / "ckpt_final.pt", step=len(loss_history))

    print("\n=== F-PERSONA-4 with null ===")
    p4 = f_persona_4_with_null(engine, args.identity_probe, device, n_perms=args.n_perms)
    print(f"  verdict={p4['verdict']} mean_kl={p4['mean_kl']:.4f} "
          f"null={p4['null_mean']:.4f}±{p4['null_std']:.4f} z={p4['z_score_vs_null']:.2f}")

    result = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "intervention": "entropy_reg_anneal + balanced_corpus (v3 path-f)",
        "lambda_init": args.lambda_init,
        "lambda_final": args.lambda_final,
        "lambda_schedule": args.lambda_schedule,
        "config": asdict(cfg),
        "training": {
            "wall_seconds": t_train,
            "wall_hours": t_train / 3600.0,
            "cost_usd_actual": cost_guard.current_usd(),
            "cost_aborted": cost_aborted,
            "ce_final_avg100": sum(ce_loss_history[-100:]) / max(min(100, len(ce_loss_history)), 1),
            "ent_final_avg100": sum(entropy_history[-100:]) / max(min(100, len(entropy_history)), 1),
            "wmax_final_avg100": sum(wmax_history[-100:]) / max(min(100, len(wmax_history)), 1),
            "lambda_final_avg100": sum(lambda_history[-100:]) / max(min(100, len(lambda_history)), 1),
            "log_N_target": math.log(max(engine.n_cells, 1)),
            "splits": splits_in_run,
            "n_cells_final": engine.n_cells,
        },
        "loss_history_sample": loss_history[::max(1, len(loss_history) // 200)],
        "ce_loss_history_sample": ce_loss_history[::max(1, len(ce_loss_history) // 200)],
        "entropy_history_sample": entropy_history[::max(1, len(entropy_history) // 200)],
        "wmax_history_sample": wmax_history[::max(1, len(wmax_history) // 200)],
        "lambda_history_sample": lambda_history[::max(1, len(lambda_history) // 200)],
        "cell_history_sample": cell_history[::max(1, len(cell_history) // 200)],
        "f_persona_4_with_null": p4,
    }
    Path(args.output_dir + "/cotrain_v3_result.json").write_text(json.dumps(result, indent=2, default=str))
    print(f"[RESULT] cotrain_v3_result.json")
    print(f"[VERDICT] F-PERSONA-4 = {p4['verdict']} (KL={p4['mean_kl']:.4f}, z={p4['z_score_vs_null']:.2f})")
    return 0 if not cost_aborted else 3


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
    ap.add_argument("--cost-cap-usd", type=float, default=8.0)
    ap.add_argument("--cost-per-hr", type=float, default=2.70)
    ap.add_argument("--estimated-wall-hr", type=float, default=1.5)
    ap.add_argument("--identity-probe", type=str, required=True)
    ap.add_argument("--lambda-init", type=float, default=50.0,
                    help="Entropy reg λ at warmup end (high → uniformity)")
    ap.add_argument("--lambda-final", type=float, default=0.5,
                    help="Entropy reg λ at end of training (low → allow specialization)")
    ap.add_argument("--lambda-schedule", type=str, default="cosine",
                    choices=["constant", "linear", "cosine"])
    ap.add_argument("--n-perms", type=int, default=100)
    return ap.parse_args()


if __name__ == "__main__":
    sys.exit(cotrain(parse_args()))
