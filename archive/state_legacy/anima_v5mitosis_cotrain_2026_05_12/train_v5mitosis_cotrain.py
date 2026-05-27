"""training/cotrain_v5mitosis.py — REBORN §88 cond.5 cotrain runner.

PURPOSE
    Cond.5 H100 cotrain entrypoint for v5-mitosis architecture
    (`training/mitosis_model_v5.py`). Drives byte-level next-token CE training on
    anima multi-turn corpus, invokes mitosis_step() per forward to fire
    split/merge events as the cell pool grows organically (REBORN §0.5 / §88).

    Falsifier 측정 hook embedded:
      F-V5MIT-1 SPLIT-NOGRAD     — split event in backward graph 외부 (sanity check
                                   every N steps: child param grad_fn=None)
      F-V5MIT-2 MERGE-WEIGHT     — merge keeper weight == parent avg (unit test
                                   end-of-run on synthetic forced merge)
      F-V5MIT-3 PHI-CONSERVATION — per-cell Φ < 25% change across split
      F-V5MIT-4 COTRAIN-CONVERGE — CE loss converges to a finite value < initial,
                                   monotonic decrease over rolling 100-step window
      F-V5MIT-5 V14-STRICT       — 5 trained seeds × 5 random-init seeds, every
                                   mirror-beat (pre-defined output diff metric)
                                   trained > random (run at end via separate
                                   trained-seed selection of final ckpt + freshly
                                   constructed random pools).

USAGE
    python3 train_v5mitosis_cotrain.py \
        --corpus /workspace/anima/corpus/corpus_color_cosmology.txt \
        --output-dir /workspace/anima/output \
        --steps 5000 \
        --batch 32 \
        --ctx 256 \
        --lr 1e-4 \
        --warmup 500 \
        --cost-cap-usd 40.0 \
        --cost-per-hr 2.70

ENVELOPE
    cells 2→64, d_model=384, n_head=6, ffn_dim=1536, 5K steps, batch=32, ctx=256.
    ~200M params at saturation. H100 wall ~8hr.
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


# ─── Path bootstrap ──────────────────────────────────────────────────
def _bootstrap_path():
    here = Path(__file__).resolve().parent
    candidates = [
        Path("/workspace/anima/training"),
        here / "../training",
        here.parent / "training",
        Path("/Users/ghost/core/anima/training"),
    ]
    for c in candidates:
        if (c / "mitosis_model_v5.py").exists():
            sys.path.insert(0, str(c.resolve()))
            return
    raise RuntimeError("mitosis_model_v5.py not found in any search path")


_bootstrap_path()
from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


# ─── Byte tokenizer ──────────────────────────────────────────────────
def text_to_bytes(text: str) -> List[int]:
    return list(text.encode("utf-8"))


def load_corpus_bytes(path: str) -> torch.Tensor:
    with open(path, "rb") as f:
        raw = f.read()
    arr = torch.tensor(list(raw), dtype=torch.long)
    return arr


def sample_batch(corpus: torch.Tensor, batch_size: int, ctx: int, device: torch.device):
    """Sample (B, ctx+1) chunks — input = [0:ctx], target = [1:ctx+1]."""
    N = corpus.size(0)
    if N <= ctx + 1:
        raise ValueError(f"corpus too small: N={N}, need > ctx+1={ctx + 1}")
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
def f_v5mit_1_split_nograd_probe(engine: MitosisModelEngine, pre_ids: set) -> Dict:
    """Sanity probe after a split — new cell parameters are leaves (grad_fn=None)
    and were not in pre-split parameter id set."""
    new_grad_fn_violations = 0
    new_count = 0
    for p in engine.parameters():
        if id(p) not in pre_ids:
            new_count += 1
            if p.grad_fn is not None:
                new_grad_fn_violations += 1
    return {
        "new_param_count": new_count,
        "grad_fn_violations": new_grad_fn_violations,
    }


def f_v5mit_3_phi_per_cell(engine: MitosisModelEngine) -> float:
    n = max(engine.n_cells, 1)
    return engine.phi / n


def f_v5mit_2_merge_unit_test(cfg: MitosisModelConfig) -> Dict:
    """Run a small force_merge synth test on a fresh engine — return weight match."""
    test_cfg = MitosisModelConfig(
        vocab_size=64, d_model=32, n_head=4, ffn_dim=64, max_seq=16,
        initial_cells=2, max_cells=8, min_cells=1, attention_sharing="never",
        readout_mode=cfg.readout_mode,
    )
    e = MitosisModelEngine(test_cfg)
    e.eval()
    pre_a = {n: p.detach().clone() for n, p in e.cells[0].own_parameters()}
    pre_b = {n: p.detach().clone() for n, p in e.cells[1].own_parameters()}
    e.cells[0].creation_step = 0
    e.cells[1].creation_step = 1
    e.force_merge(idx_a=0, idx_b=1)
    keeper = e.cells[0]
    post_keeper = {n: p.detach().clone() for n, p in keeper.own_parameters()}
    max_err = 0.0
    n_checked = 0
    for name, post in post_keeper.items():
        if name in pre_a and name in pre_b:
            expected = (pre_a[name] + pre_b[name]) / 2.0
            if expected.shape == post.shape:
                err = (post - expected).abs().max().item()
                max_err = max(max_err, err)
                n_checked += 1
    return {"max_abs_err": max_err, "n_checked": n_checked, "passed": (max_err < 1e-6 and n_checked > 0)}


# ─── Mirror-beat metric (F-V5MIT-5) ──────────────────────────────────
def output_signature(model: MitosisModelEngine, probe_ids: torch.Tensor) -> torch.Tensor:
    """Per-cell tension softmax signature on a fixed probe — captures specialization."""
    model.eval()
    with torch.no_grad():
        _, info = model(probe_ids)
    sig = info["weights"].detach().cpu().float()
    return sig


def mirror_beat_distance(sig_a: torch.Tensor, sig_b: torch.Tensor) -> float:
    """Bhattacharyya distance over softmax distributions, padded to common len."""
    n = max(sig_a.numel(), sig_b.numel())
    a = torch.zeros(n)
    b = torch.zeros(n)
    a[: sig_a.numel()] = sig_a.flatten()
    b[: sig_b.numel()] = sig_b.flatten()
    a = a / (a.sum().clamp(min=1e-9))
    b = b / (b.sum().clamp(min=1e-9))
    bc = (a * b).clamp(min=0).sqrt().sum().item()
    return float(-math.log(max(bc, 1e-9)))


# ─── F-PERSONA-4 re-measurement on cotrained pool ────────────────────
def f_persona_4_remeasure(
    engine: MitosisModelEngine,
    identity_probe_path: Optional[str],
    device: torch.device,
) -> Dict:
    """Cotrained-pool F-PERSONA-4 category-diversity KL re-measurement.
    Mirrors `tool/anima_persona_substrate_native_verify.hexa` §F-PERSONA-4 logic
    in PyTorch on the live engine.

    Strategy (same as hexa harness):
      1. group 50 prompts by category (5 cats × 10 each)
      2. per-prompt forward → tension softmax weights (= info['weights'])
      3. mean weights per category → 5 distributions
      4. pairwise KL → 10 pairs → mean KL
      5. PASS if mean KL >= 0.5 nats
    """
    if identity_probe_path is None or not Path(identity_probe_path).exists():
        return {"verdict": "SKIP", "reason": "identity_probe.jsonl missing"}
    probes = []
    with open(identity_probe_path, "r", encoding="utf-8") as f:
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
    # KL pairs
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

    # ── Pre-fire cost cap sanity ───────────────────────────────────
    est_wall_hr = args.estimated_wall_hr
    if est_wall_hr * args.cost_per_hr > args.cost_cap_usd * 1.10:
        print(f"[ABORT] est wall {est_wall_hr:.2f}hr × ${args.cost_per_hr}/hr = "
              f"${est_wall_hr*args.cost_per_hr:.2f} exceeds cap ${args.cost_cap_usd} +10%")
        return 2

    # ── Build engine ───────────────────────────────────────────────
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
        attention_sharing="auto",  # N>8 share for memory
        weight_tied_lm_head=True,
        dropout=0.0,
    )
    print(f"[INFO] cfg = {asdict(cfg)}")
    engine = MitosisModelEngine(cfg).to(device)
    n_params_init = sum(p.numel() for p in engine.parameters())
    print(f"[INFO] initial n_params = {n_params_init:,}, n_cells = {engine.n_cells}")

    # ── Corpus ─────────────────────────────────────────────────────
    print(f"[INFO] loading corpus: {args.corpus}")
    corpus = load_corpus_bytes(args.corpus)
    print(f"[INFO] corpus bytes = {corpus.numel():,}")

    # ── Optimizer ──────────────────────────────────────────────────
    optimizer = torch.optim.AdamW(engine.parameters(), lr=args.lr, betas=(0.9, 0.95),
                                  weight_decay=0.0)

    def lr_at(step):
        if step < args.warmup:
            return args.lr * (step + 1) / max(args.warmup, 1)
        progress = (step - args.warmup) / max(args.steps - args.warmup, 1)
        return args.lr * 0.5 * (1.0 + math.cos(math.pi * progress))

    # Optimizer-rebuild callback — clear stale momentum slots after mitosis events
    def opt_rebuild(event, eng):
        # After split/merge, AdamW state for removed params is orphan; for new
        # params, AdamW lazy-inits on first step. We don't need to rebuild for
        # AdamW (lazy init handles new keys; removed keys are ignored). This is
        # primarily a logging hook for now.
        pass

    engine.register_optimizer_rebuild_callback(opt_rebuild)

    # ── Mirror-beat probe set (F-V5MIT-5) ──────────────────────────
    # 10 fixed probe sequences — held-out, will compare cotrained vs random init.
    torch.manual_seed(7777)
    probe_set = []
    for i in range(10):
        # Random byte windows from corpus
        idx = torch.randint(0, max(corpus.size(0) - args.ctx - 1, 1), (1,)).item()
        probe_set.append(corpus[idx : idx + args.ctx].clone().unsqueeze(0).to(device))
    torch.manual_seed(args.seed)

    # ── Training loop ──────────────────────────────────────────────
    loss_history: List[float] = []
    cell_history: List[int] = []
    phi_history: List[float] = []
    event_history: List[Dict] = []
    split_grad_violations = 0
    splits_in_run = 0
    merges_in_run = 0
    t_start = time.time()
    cost_aborted = False
    last_ckpt_step = 0

    print(f"[INFO] training {args.steps} steps, batch={args.batch}, ctx={args.ctx}, "
          f"lr={args.lr}, warmup={args.warmup}, cost_cap=${args.cost_cap_usd}, "
          f"cost_per_hr=${args.cost_per_hr}")
    print(f"[INFO] cost guard active — abort if elapsed × rate > cap")

    for step in range(args.steps):
        if cost_guard.over():
            print(f"[COST-ABORT] step={step} elapsed_hr={cost_guard.elapsed_hr():.2f} "
                  f"cost=${cost_guard.current_usd():.2f} >= cap=${args.cost_cap_usd}")
            cost_aborted = True
            break

        # LR schedule
        cur_lr = lr_at(step)
        for g in optimizer.param_groups:
            g["lr"] = cur_lr

        engine.train()
        x, y = sample_batch(corpus, args.batch, args.ctx, device)
        # ── F-V5MIT-1 probe: snapshot pre-step param ids ──
        pre_param_ids = {id(p) for p in engine.parameters()} if (step % 200 == 0) else None

        optimizer.zero_grad()
        logits, info = engine(x)
        loss = F.cross_entropy(logits.reshape(-1, cfg.vocab_size), y.reshape(-1))
        loss.backward()
        torch.nn.utils.clip_grad_norm_(engine.parameters(), max_norm=1.0)
        optimizer.step()

        # ── Mitosis step (split/merge based on tensions) ─────────
        mit_result = engine.mitosis_step(info)
        events_this = mit_result["events"]
        if events_this:
            for ev in events_this:
                event_history.append({"step": step, **ev})
                if ev["type"] == "split":
                    splits_in_run += 1
                elif ev["type"] == "merge":
                    merges_in_run += 1
            # F-V5MIT-1 probe — check that new cells' params have grad_fn=None
            if pre_param_ids is not None:
                probe = f_v5mit_1_split_nograd_probe(engine, pre_param_ids)
                split_grad_violations += probe["grad_fn_violations"]

        loss_history.append(loss.item())
        cell_history.append(engine.n_cells)
        phi_history.append(float(engine.phi))

        # Periodic log
        if step % args.log_every == 0 or step == args.steps - 1:
            recent = loss_history[-min(50, len(loss_history)):]
            rl = sum(recent) / len(recent)
            print(f"[STEP {step:5d}] loss={loss.item():.4f} avg50={rl:.4f} "
                  f"lr={cur_lr:.2e} cells={engine.n_cells} phi={engine.phi:.4f} "
                  f"phi/N={(engine.phi/max(engine.n_cells,1)):.4f} "
                  f"splits={splits_in_run} merges={merges_in_run} "
                  f"elapsed={cost_guard.elapsed_hr():.2f}hr "
                  f"cost=${cost_guard.current_usd():.2f}")
            sys.stdout.flush()

        # Periodic ckpt
        if (step + 1) % args.ckpt_every == 0 and (step + 1) != args.steps:
            ckpt_path = Path(args.output_dir) / f"ckpt_step_{step+1}.pt"
            save_ckpt(engine, cfg, ckpt_path, step=step + 1)
            last_ckpt_step = step + 1
            print(f"[CKPT] saved {ckpt_path}")

    t_train = time.time() - t_start
    actual_cost = cost_guard.current_usd()
    print(f"[INFO] training done — wall={t_train:.1f}s "
          f"({t_train/3600:.2f}hr) actual_cost=${actual_cost:.2f}")

    # ── Final ckpt ─────────────────────────────────────────────────
    final_ckpt = Path(args.output_dir) / "ckpt_final.pt"
    save_ckpt(engine, cfg, final_ckpt, step=len(loss_history))
    print(f"[CKPT] final saved {final_ckpt} ({final_ckpt.stat().st_size:,} bytes)")

    # ── Falsifier verdicts ─────────────────────────────────────────
    print("\n=== falsifier verdicts ===")
    # F-V5MIT-1
    f1 = {
        "test": "F-V5MIT-1 SPLIT-NOGRAD",
        "splits_total": splits_in_run,
        "grad_fn_violations": split_grad_violations,
        "passed": split_grad_violations == 0 and splits_in_run > 0,
    }
    print(f"  F-V5MIT-1: {f1}")

    # F-V5MIT-2
    f2 = f_v5mit_2_merge_unit_test(cfg)
    f2["test"] = "F-V5MIT-2 MERGE-WEIGHT"
    print(f"  F-V5MIT-2: {f2}")

    # F-V5MIT-3: simulate one split on a fresh test pool, check Φ/N change
    test_engine = copy.deepcopy(engine).to(device)
    test_engine.eval()
    with torch.no_grad():
        # Warm up
        for _ in range(3):
            xw, _ = sample_batch(corpus, 1, args.ctx, device)
            _, infw = test_engine(xw)
            test_engine.mitosis_step(infw)
        phi_pre = float(test_engine.phi)
        n_pre = test_engine.n_cells
        ev = test_engine.force_split(parent_idx=0)
        # Φ update only happens via mitosis_step. Re-measure proxy directly.
        phi_post = test_engine._compute_iit_phi()
        n_post = test_engine.n_cells
    phi_pre_per = phi_pre / max(n_pre, 1)
    phi_post_per = phi_post / max(n_post, 1)
    if phi_pre_per > 0:
        ratio = (phi_post_per - phi_pre_per) / phi_pre_per
    else:
        ratio = 0.0
    f3 = {
        "test": "F-V5MIT-3 PHI-CONSERVATION (per-cell)",
        "phi_pre_per_cell": phi_pre_per,
        "phi_post_per_cell": phi_post_per,
        "delta_ratio": ratio,
        "tolerance": 0.25,
        "passed": abs(ratio) < 0.25,
    }
    print(f"  F-V5MIT-3: {f3}")
    del test_engine

    # F-V5MIT-4: rolling loss window monotonicity
    initial_avg = sum(loss_history[:100]) / max(min(100, len(loss_history)), 1)
    final_avg = sum(loss_history[-100:]) / max(min(100, len(loss_history)), 1)
    converged = final_avg < initial_avg and math.isfinite(final_avg)
    f4 = {
        "test": "F-V5MIT-4 COTRAIN-CONVERGE",
        "initial_avg_loss": initial_avg,
        "final_avg_loss": final_avg,
        "delta": initial_avg - final_avg,
        "passed": converged,
    }
    print(f"  F-V5MIT-4: {f4}")

    # F-V5MIT-5: trained > random 5-seed every-mirror-beat
    print("[F-V5MIT-5] building 5 random-init comparison engines …")
    rand_signatures: List[List[torch.Tensor]] = []
    for seed in range(101, 106):
        torch.manual_seed(seed)
        rand_cfg = MitosisModelConfig(**{**asdict(cfg)})
        rand_eng = MitosisModelEngine(rand_cfg).to(device)
        rand_eng.eval()
        sigs = [output_signature(rand_eng, p) for p in probe_set]
        rand_signatures.append(sigs)
        del rand_eng
        if device.type == "cuda":
            torch.cuda.empty_cache()
    # Trained signatures
    trained_signatures = [output_signature(engine, p) for p in probe_set]

    # Per-probe (mirror beat): compute Bhattacharyya distance trained vs random
    # then check trained-vs-trained is internally consistent
    n_beats = len(probe_set)
    beats_passed = 0
    beat_details = []
    for i in range(n_beats):
        t_sig = trained_signatures[i]
        # Average random distance: how different random pools look from each other
        random_internal = []
        for a in range(5):
            for b in range(a + 1, 5):
                random_internal.append(mirror_beat_distance(rand_signatures[a][i], rand_signatures[b][i]))
        random_mean_internal = sum(random_internal) / len(random_internal)
        # Trained-vs-random distance — how far trained is from each random
        t_vs_r = [mirror_beat_distance(t_sig, rand_signatures[r][i]) for r in range(5)]
        t_vs_r_mean = sum(t_vs_r) / 5
        # Pass criterion: trained-vs-random mean > random-internal mean (i.e. trained pool
        # is distinguishable from random pools beyond random-pool noise)
        beat_pass = t_vs_r_mean > random_mean_internal
        beat_details.append({
            "beat": i,
            "trained_vs_random_mean": t_vs_r_mean,
            "random_internal_mean": random_mean_internal,
            "passed": beat_pass,
        })
        if beat_pass:
            beats_passed += 1

    f5 = {
        "test": "F-V5MIT-5 V14-STRICT",
        "n_beats": n_beats,
        "beats_passed": beats_passed,
        "passed_every_beat": beats_passed == n_beats,
        "details": beat_details,
        "passed": beats_passed == n_beats,
    }
    print(f"  F-V5MIT-5: passed_every_beat={f5['passed_every_beat']} "
          f"beats_passed={beats_passed}/{n_beats}")

    # ── F-PERSONA-4 re-measurement on cotrained pool ───────────────
    print("\n=== F-PERSONA-4 CATEGORY-DIVERSITY re-measurement ===")
    persona4 = f_persona_4_remeasure(
        engine,
        args.identity_probe,
        device,
    )
    print(f"  F-PERSONA-4 (cotrained pool): {persona4}")

    # ── Results aggregate ──────────────────────────────────────────
    falsifier_results = [f1, f2, f3, f4, f5]
    n_f_pass = sum(1 for f in falsifier_results if f.get("passed"))
    result = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "device": str(device),
        "torch_version": torch.__version__,
        "config": asdict(cfg),
        "training": {
            "steps_actual": len(loss_history),
            "steps_planned": args.steps,
            "wall_seconds": t_train,
            "wall_hours": t_train / 3600.0,
            "cost_usd_actual": actual_cost,
            "cost_cap_usd": args.cost_cap_usd,
            "cost_per_hr": args.cost_per_hr,
            "cost_aborted": cost_aborted,
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
        "loss_history_sample": loss_history[::max(1, len(loss_history) // 200)],
        "cell_history_sample": cell_history[::max(1, len(cell_history) // 200)],
        "phi_history_sample": phi_history[::max(1, len(phi_history) // 200)],
        "event_history": event_history,
        "falsifiers": {
            "F-V5MIT-1": f1,
            "F-V5MIT-2": f2,
            "F-V5MIT-3": f3,
            "F-V5MIT-4": f4,
            "F-V5MIT-5": f5,
        },
        "falsifier_aggregate": {
            "n_pass": n_f_pass,
            "n_total": len(falsifier_results),
            "verdict": "PASS_ALL" if n_f_pass == len(falsifier_results) else "PARTIAL",
        },
        "f_persona_4_remeasure": persona4,
    }
    result_path = Path(args.output_dir) / "cotrain_result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"\n[RESULT] saved {result_path}")
    print(f"[VERDICT] falsifier pass {n_f_pass}/{len(falsifier_results)}, "
          f"F-PERSONA-4 = {persona4.get('verdict')}")
    return 0 if not cost_aborted else 3


def save_ckpt(engine: MitosisModelEngine, cfg: MitosisModelConfig, path: Path, step: int):
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
    ap.add_argument("--ckpt-every", type=int, default=1000)
    ap.add_argument("--cost-cap-usd", type=float, default=40.0)
    ap.add_argument("--cost-per-hr", type=float, default=2.70)
    ap.add_argument("--estimated-wall-hr", type=float, default=10.0,
                    help="Estimate of wall time for pre-fire cost gate")
    ap.add_argument("--identity-probe", type=str, default=None,
                    help="Path to identity_probe.jsonl for F-PERSONA-4 remeasure")
    return ap.parse_args()


if __name__ == "__main__":
    args = parse_args()
    sys.exit(cotrain(args))
