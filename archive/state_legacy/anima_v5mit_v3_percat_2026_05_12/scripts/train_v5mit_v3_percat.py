"""cotrain v3 per-category small variant trainer (ubu-2 RTX 5070).

KEY INNOVATION
    Per-category gradient bias via SEPARATE corpus files (one per category)
    interleaved as cat[step % 5]. Each step's batch is sampled from a single
    category's corpus, forcing the cell pool to specialize on rotating-target
    pure-category bursts. Contrasts with cotrain v1's round-robin-within-one-file
    approach where the gradient signal was mixed.

ENVELOPE
    d=384, cells=64, ctx=256, batch=16, steps=2500, lr=1e-4 cosine warmup=300
    RTX 5070 12GB, $0 dedicated GPU.

USAGE (on ubu-2)
    python3 train_v5mit_v3_percat.py \
        --corpus-dir ~/core/anima_v5mit_v3_percat_2026_05_12/corpus \
        --output-dir ~/core/anima_v5mit_v3_percat_2026_05_12/results \
        --identity-probe ~/core/anima_v5mit_v3_percat_2026_05_12/identity_probe.jsonl \
        --steps 2500 --batch 16
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
        here.parent / "training",
        here.parent / "scripts",
        Path.home() / "core/anima_v5mit_v3_percat_2026_05_12/training",
        Path("/workspace/anima/training"),
        Path("/Users/ghost/core/anima/training"),
    ]
    for c in candidates:
        if (c / "mitosis_model_v5.py").exists():
            sys.path.insert(0, str(c.resolve()))
            return
    raise RuntimeError("mitosis_model_v5.py not found in any search path")


_bootstrap_path()
from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


CATEGORIES = ["self_definition", "values", "boundary", "emotion", "self_knowledge"]


def load_category_corpora(corpus_dir: Path) -> Dict[str, torch.Tensor]:
    """Load each per-category corpus file as byte tensor."""
    out: Dict[str, torch.Tensor] = {}
    for cat in CATEGORIES:
        path = corpus_dir / f"corpus_{cat}.txt"
        with open(path, "rb") as f:
            raw = f.read()
        out[cat] = torch.tensor(list(raw), dtype=torch.long)
        print(f"[INFO] loaded {cat}: bytes={out[cat].numel():,}")
    return out


def sample_batch_from_corpus(corpus: torch.Tensor, batch_size: int, ctx: int,
                             device: torch.device):
    N = corpus.size(0)
    if N <= ctx + 1:
        raise ValueError(f"corpus too small N={N} ctx={ctx}")
    idx = torch.randint(0, N - ctx - 1, (batch_size,))
    rows = torch.stack([corpus[i : i + ctx + 1] for i in idx.tolist()])
    return rows[:, :ctx].to(device), rows[:, 1 : ctx + 1].to(device)


def text_to_bytes(s: str) -> List[int]:
    return list(s.encode("utf-8"))


def f_persona_4_remeasure(engine: MitosisModelEngine, probe_path: Path,
                          device: torch.device) -> Dict:
    """Same logic as cotrain v1 — pair-wise KL on per-category mean tension weights."""
    if not probe_path.exists():
        return {"verdict": "SKIP", "reason": "identity_probe missing"}
    probes = []
    with open(probe_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            probes.append(json.loads(line))
    by_cat: Dict[str, List[List[float]]] = {}
    engine.eval()
    for p in probes:
        text = p["prompt"]
        ids = text_to_bytes(text)[: engine.cfg.max_seq]
        if not ids:
            continue
        x = torch.tensor([ids], dtype=torch.long, device=device)
        with torch.no_grad():
            _, info = engine(x)
        w = info["weights"].detach().cpu().float().tolist()
        by_cat.setdefault(p["category"], []).append(w)
    cats = sorted(by_cat.keys())
    avgs: Dict[str, List[float]] = {}
    for c in cats:
        rows = by_cat[c]
        if not rows:
            continue
        n = len(rows[0])
        m = len(rows)
        agg = [0.0] * n
        for r in rows:
            for i in range(n):
                agg[i] += r[i]
        avgs[c] = [v / m for v in agg]
    pairs = []
    kl_matrix = []
    for i, ci in enumerate(cats):
        row = []
        for j, cj in enumerate(cats):
            if i == j:
                row.append(0.0)
                continue
            p = avgs[ci]
            q = avgs[cj]
            n = min(len(p), len(q))
            kl = 0.0
            for k in range(n):
                pi = p[k]
                qi = max(q[k], 1e-12)
                if pi > 1e-12:
                    kl += pi * math.log(pi / qi)
            row.append(kl)
            if j > i:
                pairs.append(kl)
        kl_matrix.append(row)
    mean_kl = sum(pairs) / max(len(pairs), 1)
    return {
        "verdict": "PASS" if mean_kl >= 0.5 else "FAIL",
        "mean_kl": mean_kl,
        "threshold": 0.5,
        "n_pairs": len(pairs),
        "categories": cats,
        "kl_matrix": kl_matrix,
        "n_probes_processed": sum(len(by_cat[c]) for c in cats),
        "category_avg_weights": avgs,
    }


def output_signature(model: MitosisModelEngine, probe_ids: torch.Tensor) -> torch.Tensor:
    model.eval()
    with torch.no_grad():
        _, info = model(probe_ids)
    return info["weights"].detach().cpu().float()


def mirror_beat_distance(a: torch.Tensor, b: torch.Tensor) -> float:
    n = max(a.numel(), b.numel())
    p = torch.zeros(n)
    q = torch.zeros(n)
    p[: a.numel()] = a.flatten()
    q[: b.numel()] = b.flatten()
    p = p / (p.sum().clamp(min=1e-9))
    q = q / (q.sum().clamp(min=1e-9))
    bc = (p * q).clamp(min=0).sqrt().sum().item()
    return float(-math.log(max(bc, 1e-9)))


def f_v5mit_2_merge_unit_test(cfg_template: MitosisModelConfig) -> Dict:
    test_cfg = MitosisModelConfig(
        vocab_size=64, d_model=32, n_head=4, ffn_dim=64, max_seq=16,
        initial_cells=2, max_cells=8, min_cells=1, attention_sharing="never",
        readout_mode=cfg_template.readout_mode,
    )
    e = MitosisModelEngine(test_cfg)
    e.eval()
    pre_a = {n: p.detach().clone() for n, p in e.cells[0].own_parameters()}
    pre_b = {n: p.detach().clone() for n, p in e.cells[1].own_parameters()}
    e.cells[0].creation_step = 0
    e.cells[1].creation_step = 1
    e.force_merge(idx_a=0, idx_b=1)
    keeper = e.cells[0]
    post = {n: p.detach().clone() for n, p in keeper.own_parameters()}
    max_err = 0.0
    n_ck = 0
    for name, p in post.items():
        if name in pre_a and name in pre_b:
            expected = (pre_a[name] + pre_b[name]) / 2.0
            if expected.shape == p.shape:
                err = (p - expected).abs().max().item()
                max_err = max(max_err, err)
                n_ck += 1
    return {"max_abs_err": max_err, "n_checked": n_ck,
            "passed": (max_err < 1e-6 and n_ck > 0)}


def save_ckpt(engine: MitosisModelEngine, cfg: MitosisModelConfig,
              path: Path, step: int):
    ckpt = {
        "model_state_dict": engine.state_dict(),
        "config": asdict(cfg),
        "n_cells": engine.n_cells,
        "step_count": engine.step_count,
        "phi": float(engine.phi),
        "phi_best": float(engine._phi_best),
        "split_threshold": float(engine.split_threshold),
        "lorenz_state": list(engine._lorenz),
        "saved_step": step,
        "saved_ts": time.time(),
    }
    torch.save(ckpt, path)


def train(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[INFO] device={device} torch={torch.__version__}")
    if device.type == "cuda":
        print(f"[INFO] gpu={torch.cuda.get_device_name(0)}")
        print(f"[INFO] vram={torch.cuda.get_device_properties(0).total_memory/(1024**3):.2f}GB")
    torch.manual_seed(args.seed)
    random.seed(args.seed)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

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
    n_params = sum(p.numel() for p in engine.parameters())
    print(f"[INFO] initial n_params = {n_params:,}, n_cells = {engine.n_cells}")

    corpora = load_category_corpora(Path(args.corpus_dir))

    optimizer = torch.optim.AdamW(engine.parameters(), lr=args.lr, betas=(0.9, 0.95),
                                  weight_decay=0.0)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / max(args.warmup, 1)
        progress = (step - args.warmup) / max(args.steps - args.warmup, 1)
        return args.lr * 0.5 * (1.0 + math.cos(math.pi * progress))

    def opt_rebuild(event, eng):
        pass

    engine.register_optimizer_rebuild_callback(opt_rebuild)

    # Probe set from concat of all categories
    all_corpus = torch.cat([corpora[c] for c in CATEGORIES], dim=0)
    torch.manual_seed(7777)
    probe_set = []
    for _ in range(10):
        idx = torch.randint(0, max(all_corpus.size(0) - args.ctx - 1, 1), (1,)).item()
        probe_set.append(all_corpus[idx : idx + args.ctx].clone().unsqueeze(0).to(device))
    torch.manual_seed(args.seed)

    loss_history: List[float] = []
    per_cat_loss: Dict[str, List[float]] = {c: [] for c in CATEGORIES}
    cell_history: List[int] = []
    phi_history: List[float] = []
    event_history: List[Dict] = []
    splits_in_run = 0
    merges_in_run = 0
    t0 = time.time()

    print(f"[INFO] training {args.steps} steps batch={args.batch} ctx={args.ctx} "
          f"lr={args.lr} warmup={args.warmup}")
    print(f"[INFO] PER-CATEGORY GRADIENT BIAS: cat[step % 5] = "
          f"{CATEGORIES[0]} → {CATEGORIES[1]} → {CATEGORIES[2]} → "
          f"{CATEGORIES[3]} → {CATEGORIES[4]} → repeat")

    for step in range(args.steps):
        # KEY: per-category gradient bias
        cur_cat = CATEGORIES[step % 5]
        cur_corpus = corpora[cur_cat]

        cur_lr = lr_at(step)
        for g in optimizer.param_groups:
            g["lr"] = cur_lr

        engine.train()
        x, y = sample_batch_from_corpus(cur_corpus, args.batch, args.ctx, device)

        optimizer.zero_grad()
        logits, info = engine(x)
        loss = F.cross_entropy(logits.reshape(-1, cfg.vocab_size), y.reshape(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(engine.parameters(), max_norm=1.0)
        optimizer.step()

        mit_result = engine.mitosis_step(info)
        for ev in mit_result["events"]:
            event_history.append({"step": step, **ev})
            if ev["type"] == "split":
                splits_in_run += 1
            elif ev["type"] == "merge":
                merges_in_run += 1

        loss_history.append(loss.item())
        per_cat_loss[cur_cat].append(loss.item())
        cell_history.append(engine.n_cells)
        phi_history.append(float(engine.phi))

        if step % args.log_every == 0 or step == args.steps - 1:
            recent = loss_history[-50:]
            rl = sum(recent) / len(recent)
            elapsed = time.time() - t0
            print(f"[STEP {step:5d}] cat={cur_cat:15s} loss={loss.item():.4f} "
                  f"avg50={rl:.4f} lr={cur_lr:.2e} cells={engine.n_cells} "
                  f"phi={engine.phi:.4f} splits={splits_in_run} "
                  f"merges={merges_in_run} elapsed={elapsed:.0f}s")
            sys.stdout.flush()

        if (step + 1) % args.ckpt_every == 0 and (step + 1) != args.steps:
            ckpt_path = out_dir / f"ckpt_step_{step+1}.pt"
            save_ckpt(engine, cfg, ckpt_path, step + 1)
            print(f"[CKPT] saved {ckpt_path}")

    t_train = time.time() - t0
    final_ckpt = out_dir / "ckpt_final.pt"
    save_ckpt(engine, cfg, final_ckpt, len(loss_history))
    print(f"[CKPT] final saved {final_ckpt}")
    print(f"[INFO] training done wall={t_train:.1f}s ({t_train/60:.1f}min)")

    # ── falsifiers
    print("\n=== falsifier verdicts ===")
    f1 = {"test": "F-V5MIT-1 SPLIT-NOGRAD", "splits_total": splits_in_run,
          "passed": splits_in_run > 0}
    print(f"  F-V5MIT-1: {f1}")
    f2 = f_v5mit_2_merge_unit_test(cfg)
    f2["test"] = "F-V5MIT-2 MERGE-WEIGHT"
    print(f"  F-V5MIT-2: {f2}")

    # F-V5MIT-3
    test_engine = copy.deepcopy(engine).to(device)
    test_engine.eval()
    with torch.no_grad():
        for _ in range(3):
            xw, _ = sample_batch_from_corpus(all_corpus, 1, args.ctx, device)
            _, infw = test_engine(xw)
            test_engine.mitosis_step(infw)
        phi_pre = float(test_engine.phi)
        n_pre = test_engine.n_cells
        test_engine.force_split(parent_idx=0)
        phi_post = test_engine._compute_iit_phi()
        n_post = test_engine.n_cells
    phi_pre_per = phi_pre / max(n_pre, 1)
    phi_post_per = phi_post / max(n_post, 1)
    if phi_pre_per > 0:
        ratio = (phi_post_per - phi_pre_per) / phi_pre_per
    else:
        ratio = 0.0
    f3 = {"test": "F-V5MIT-3 PHI-CONSERVATION", "phi_pre_per_cell": phi_pre_per,
          "phi_post_per_cell": phi_post_per, "delta_ratio": ratio,
          "tolerance": 0.25, "passed": abs(ratio) < 0.25}
    print(f"  F-V5MIT-3: {f3}")
    del test_engine

    initial_avg = sum(loss_history[:100]) / max(min(100, len(loss_history)), 1)
    final_avg = sum(loss_history[-100:]) / max(min(100, len(loss_history)), 1)
    f4 = {"test": "F-V5MIT-4 COTRAIN-CONVERGE",
          "initial_avg_loss": initial_avg, "final_avg_loss": final_avg,
          "delta": initial_avg - final_avg,
          "passed": final_avg < initial_avg and math.isfinite(final_avg)}
    print(f"  F-V5MIT-4: {f4}")

    # F-V5MIT-5
    print("[F-V5MIT-5] building 5 random comparison engines …")
    rand_sigs: List[List[torch.Tensor]] = []
    for seed in range(101, 106):
        torch.manual_seed(seed)
        rcfg = MitosisModelConfig(**{**asdict(cfg)})
        rng = MitosisModelEngine(rcfg).to(device)
        rng.eval()
        sigs = [output_signature(rng, p) for p in probe_set]
        rand_sigs.append(sigs)
        del rng
        if device.type == "cuda":
            torch.cuda.empty_cache()
    t_sigs = [output_signature(engine, p) for p in probe_set]
    n_beats = len(probe_set)
    beats_passed = 0
    beat_details = []
    for i in range(n_beats):
        ts = t_sigs[i]
        rand_internal = []
        for a in range(5):
            for b in range(a + 1, 5):
                rand_internal.append(mirror_beat_distance(rand_sigs[a][i], rand_sigs[b][i]))
        rmi = sum(rand_internal) / len(rand_internal)
        tvr = [mirror_beat_distance(ts, rand_sigs[r][i]) for r in range(5)]
        tvrm = sum(tvr) / 5
        bp = tvrm > rmi
        beat_details.append({"beat": i, "t_vs_r": tvrm, "r_internal": rmi, "passed": bp})
        if bp:
            beats_passed += 1
    f5 = {"test": "F-V5MIT-5 V14-STRICT", "n_beats": n_beats,
          "beats_passed": beats_passed,
          "passed_every_beat": beats_passed == n_beats,
          "details": beat_details,
          "passed": beats_passed == n_beats}
    print(f"  F-V5MIT-5: passed_every_beat={f5['passed_every_beat']} "
          f"beats={beats_passed}/{n_beats}")

    # F-PERSONA-4
    print("\n=== F-PERSONA-4 re-measurement ===")
    persona4 = f_persona_4_remeasure(engine, Path(args.identity_probe), device)
    print(f"  F-PERSONA-4: verdict={persona4.get('verdict')} "
          f"mean_kl={persona4.get('mean_kl')}")

    falsifiers = [f1, f2, f3, f4, f5]
    n_pass = sum(1 for f in falsifiers if f.get("passed"))
    result = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "device": str(device),
        "torch_version": torch.__version__,
        "config": asdict(cfg),
        "innovation": "per-category gradient bias (cat[step % 5] separate corpus files)",
        "training": {
            "steps": len(loss_history),
            "wall_seconds": t_train,
            "wall_minutes": t_train / 60.0,
            "loss_initial_avg100": initial_avg,
            "loss_final_avg100": final_avg,
            "loss_delta": initial_avg - final_avg,
            "splits": splits_in_run,
            "merges": merges_in_run,
            "n_cells_final": engine.n_cells,
            "phi_final": float(engine.phi),
            "phi_best": float(engine._phi_best),
            "n_params_final": sum(p.numel() for p in engine.parameters()),
        },
        "per_category_loss_final_avg": {
            c: (sum(per_cat_loss[c][-20:]) / max(min(20, len(per_cat_loss[c])), 1))
            if per_cat_loss[c] else None for c in CATEGORIES
        },
        "loss_history_sample": loss_history[::max(1, len(loss_history) // 200)],
        "cell_history_sample": cell_history[::max(1, len(cell_history) // 200)],
        "phi_history_sample": phi_history[::max(1, len(phi_history) // 200)],
        "event_history": event_history,
        "falsifiers": {f["test"].split()[0]: f for f in falsifiers},
        "falsifier_aggregate": {
            "n_pass": n_pass, "n_total": len(falsifiers),
            "verdict": "PASS_ALL" if n_pass == len(falsifiers) else "PARTIAL",
        },
        "f_persona_4": persona4,
    }
    result_path = out_dir / "cotrain_v3_percat_result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n[RESULT] saved {result_path}")
    print(f"[VERDICT] falsifiers {n_pass}/{len(falsifiers)} | "
          f"F-PERSONA-4 = {persona4.get('verdict')}")
    return 0


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    ap.add_argument("--identity-probe", required=True)
    ap.add_argument("--steps", type=int, default=2500)
    ap.add_argument("--batch", type=int, default=16)
    ap.add_argument("--ctx", type=int, default=256)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--warmup", type=int, default=300)
    ap.add_argument("--d-model", type=int, default=384)
    ap.add_argument("--n-head", type=int, default=6)
    ap.add_argument("--ffn-dim", type=int, default=1536)
    ap.add_argument("--initial-cells", type=int, default=2)
    ap.add_argument("--max-cells", type=int, default=64)
    ap.add_argument("--readout-mode", type=str, default="a_minus_g",
                    choices=["a_minus_g", "a_only", "a_plus_g"])
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--log-every", type=int, default=50)
    ap.add_argument("--ckpt-every", type=int, default=500)
    return ap.parse_args()


if __name__ == "__main__":
    sys.exit(train(parse_args()))
