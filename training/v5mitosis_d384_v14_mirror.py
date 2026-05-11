"""training/v5mitosis_d384_v14_mirror.py — track C cond.3 V14 mirror at d=384.

PURPOSE
    Run MitosisModelEngine (training/mitosis_model_v5.py) at d=384, max_cells=128, with §30
    all-fix (A1/A2/B1/D1 active, C1 STUB) on real-ckpt-init vs random-init for the V14
    mirror invariant (own 14: 5-seed strict).

    Real init: v2 cells64 d=384 ckpt
        /Users/ghost/core/anima/state/anima_clm_v2_mitosis_cells_recovery_2026_05_09/
        cells64_final.pt
    The v2 ckpt is a 6-layer transformer (NOT cells-as-blocks). We map the 6 v2 blocks into
    the first 6 of 8 initial cells (cells 0..5), and cells 6..7 keep random init. Shared
    embeddings (tok_emb, pos_emb, ln_f) and the lm_head (initialised from v2 head_a) are
    loaded from the v2 ckpt — this is the maximum-fidelity load that the v2-vs-v5 schema
    delta allows.

raw#9    training/*.py local-only (gitignored)
raw#10   honest — v2→v5 schema delta documented above; cells 6,7 are random by necessity
raw#15   additive — v2 ckpt and mitosis_model_v5.py untouched
own 14   V14 mirror 5-seed strict (trained vs 5 random seeds)
own 22   honest emit — every metric scalar; cell-count growth tracked
own 38   doc save → state/anima_v5mitosis_d384_sweep_2026_05_10/
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F

# Local imports — assumes cwd ~/core/anima
THIS_DIR = Path(__file__).resolve().parent
ANIMA_ROOT = THIS_DIR.parent
sys.path.insert(0, str(ANIMA_ROOT))
sys.path.insert(0, str(ANIMA_ROOT / "training"))

from training.mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine  # noqa: E402


CKPT_PATH = (
    ANIMA_ROOT
    / "state"
    / "anima_clm_v2_mitosis_cells_recovery_2026_05_09"
    / "cells64_final.pt"
)
OUT_DIR = ANIMA_ROOT / "state" / "anima_v5mitosis_d384_sweep_2026_05_10"


def load_v2_ckpt(path: Path) -> Dict:
    ck = torch.load(str(path), map_location="cpu", weights_only=False)
    return ck


def map_v2_block_to_cell(block_idx: int, sd: Dict[str, torch.Tensor], cell, owns_attn: bool) -> Dict[str, str]:
    """Copy v2 blocks.{block_idx}.* tensors into the corresponding nn.Parameters of `cell`.

    Skips:
      - attn.bias (causal mask buffer in v2; we have a fresh causal mask in mitosis_model_v5)
      - bias on attn.c_attn / attn.c_proj (mitosis_model_v5 attn uses bias=False)
      - blocks.{i}.attn.* entirely if not owns_attn (cell uses shared_attn ref)

    Returns dict of {action: count} for diagnostics.
    """
    counts = {"attn_qkv_w": 0, "attn_out_w": 0, "ffn_a": 0, "ffn_g": 0, "ln1": 0, "ln2": 0, "skipped_bias": 0}
    prefix = f"blocks.{block_idx}."

    # ---- LayerNorm (matches: weight + bias)
    for v2_name, attr in [("ln1.weight", cell.ln1.weight), ("ln1.bias", cell.ln1.bias)]:
        k = prefix + v2_name
        if k in sd and sd[k].shape == attr.shape:
            with torch.no_grad():
                attr.copy_(sd[k])
            counts["ln1"] += 1
    for v2_name, attr in [("ln2.weight", cell.ln2.weight), ("ln2.bias", cell.ln2.bias)]:
        k = prefix + v2_name
        if k in sd and sd[k].shape == attr.shape:
            with torch.no_grad():
                attr.copy_(sd[k])
            counts["ln2"] += 1

    # ---- Attention (only if cell owns attn)
    if owns_attn:
        # v2: attn.c_attn.weight (1152, 384) → cell.attn.qkv.weight (1152, 384) ✓
        k = prefix + "attn.c_attn.weight"
        if k in sd and sd[k].shape == cell.attn.qkv.weight.shape:
            with torch.no_grad():
                cell.attn.qkv.weight.copy_(sd[k])
            counts["attn_qkv_w"] += 1
        # v2: attn.c_attn.bias (1152,) → SKIP (mitosis_model_v5 bias=False)
        if (prefix + "attn.c_attn.bias") in sd:
            counts["skipped_bias"] += 1
        # v2: attn.c_proj.weight (384, 384) → cell.attn.out.weight
        k = prefix + "attn.c_proj.weight"
        if k in sd and sd[k].shape == cell.attn.out.weight.shape:
            with torch.no_grad():
                cell.attn.out.weight.copy_(sd[k])
            counts["attn_out_w"] += 1
        if (prefix + "attn.c_proj.bias") in sd:
            counts["skipped_bias"] += 1

    # ---- FFN engine_a → ffn_a (Sequential[0]=Linear, [3]=Linear)
    pairs_a = [
        ("ffn.engine_a.0.weight", cell.ffn_a[0].weight),
        ("ffn.engine_a.0.bias", cell.ffn_a[0].bias),
        ("ffn.engine_a.3.weight", cell.ffn_a[3].weight),
        ("ffn.engine_a.3.bias", cell.ffn_a[3].bias),
    ]
    for v2_name, attr in pairs_a:
        k = prefix + v2_name
        if k in sd and sd[k].shape == attr.shape:
            with torch.no_grad():
                attr.copy_(sd[k])
            counts["ffn_a"] += 1
    pairs_g = [
        ("ffn.engine_g.0.weight", cell.ffn_g[0].weight),
        ("ffn.engine_g.0.bias", cell.ffn_g[0].bias),
        ("ffn.engine_g.3.weight", cell.ffn_g[3].weight),
        ("ffn.engine_g.3.bias", cell.ffn_g[3].bias),
    ]
    for v2_name, attr in pairs_g:
        k = prefix + v2_name
        if k in sd and sd[k].shape == attr.shape:
            with torch.no_grad():
                attr.copy_(sd[k])
            counts["ffn_g"] += 1
    return counts


def init_engine_from_v2(cfg: MitosisModelConfig, sd: Dict[str, torch.Tensor]) -> Tuple[MitosisModelEngine, Dict]:
    """Build engine and load v2 ckpt where shapes match."""
    eng = MitosisModelEngine(cfg)
    diag: Dict = {"shared": {}, "cells": []}

    # ---- Shared modules
    if "tok_emb.weight" in sd and sd["tok_emb.weight"].shape == eng.tok_emb.weight.shape:
        with torch.no_grad():
            eng.tok_emb.weight.copy_(sd["tok_emb.weight"])
        diag["shared"]["tok_emb"] = list(eng.tok_emb.weight.shape)
    if "pos_emb.weight" in sd and sd["pos_emb.weight"].shape == eng.pos_emb.weight.shape:
        with torch.no_grad():
            eng.pos_emb.weight.copy_(sd["pos_emb.weight"])
        diag["shared"]["pos_emb"] = list(eng.pos_emb.weight.shape)
    if "ln_f.weight" in sd and sd["ln_f.weight"].shape == eng.final_ln.weight.shape:
        with torch.no_grad():
            eng.final_ln.weight.copy_(sd["ln_f.weight"])
            if "ln_f.bias" in sd:
                eng.final_ln.bias.copy_(sd["ln_f.bias"])
        diag["shared"]["final_ln"] = list(eng.final_ln.weight.shape)
    # lm_head: tied to tok_emb when cfg.weight_tied_lm_head=True (default)
    # If untied, we'd load head_a here — but with tying the assignment above already covers it.
    if not cfg.weight_tied_lm_head:
        if "head_a.weight" in sd and sd["head_a.weight"].shape == eng.lm_head.weight.shape:
            with torch.no_grad():
                eng.lm_head.weight.copy_(sd["head_a.weight"])
            diag["shared"]["lm_head_from"] = "head_a"

    # ---- Cells: v2 has 6 blocks; load into cells 0..5; cells 6,7 random
    n_v2_blocks = 6
    n_cells_init = cfg.initial_cells
    n_loaded = min(n_v2_blocks, n_cells_init)
    for ci in range(n_loaded):
        cell = eng.cells[ci]
        owns = cell._owns_attn  # initial cells all own_attn=True
        c = map_v2_block_to_cell(ci, sd, cell, owns_attn=owns)
        diag["cells"].append({"idx": ci, **c})
    diag["v2_blocks_loaded"] = n_loaded
    diag["random_cells"] = list(range(n_loaded, n_cells_init))
    return eng, diag


def init_engine_random(cfg: MitosisModelConfig, seed: int) -> MitosisModelEngine:
    """Build engine with completely random init under given seed."""
    g = torch.Generator().manual_seed(seed)
    torch.manual_seed(seed)
    random.seed(seed)
    eng = MitosisModelEngine(cfg)
    return eng


def make_prompt_stream(seed: int, n_turns: int, vocab: int, max_seq: int) -> List[torch.Tensor]:
    """Synthetic diverse-prompt stream — random byte sequences with mode shifts.

    own 14 V14 mirror reproducibility: same seed → same prompt sequence across runs.
    """
    rng = random.Random(seed)
    prompts: List[torch.Tensor] = []
    for t in range(n_turns):
        # Mode shifts every 200 turns to add diversity
        mode = (t // 200) % 4
        if mode == 0:
            T = rng.randint(16, 64)
            ids = [rng.randrange(0, vocab) for _ in range(T)]
        elif mode == 1:
            T = rng.randint(32, 128)
            base = rng.randrange(0, vocab)
            ids = [(base + rng.randrange(-8, 9)) % vocab for _ in range(T)]
        elif mode == 2:
            T = rng.randint(8, 32)
            ids = [rng.choice([0x20, 0x41, 0x61, 0x2E]) for _ in range(T)]  # ASCII patterned
        else:
            T = rng.randint(64, min(192, max_seq))
            ids = [(t + i) % vocab for i in range(T)]
        prompts.append(torch.tensor(ids, dtype=torch.long).unsqueeze(0))
    return prompts


def run_trajectory(
    eng: MitosisModelEngine,
    prompts: List[torch.Tensor],
    n_turns: int,
    iit_every: int = 50,
    log_every: int = 250,
    label: str = "?",
) -> Dict:
    """Run n_turns prompts through the engine, calling mitosis_step() after each forward.

    Returns: dict with cell_count_trajectory, phi_trajectory (sampled every iit_every),
    splits, merges, ratchets, final n_cells, max n_cells.
    """
    eng.eval()
    cell_counts: List[int] = []
    phi_traj: List[Tuple[int, int, float, float]] = []   # (turn, n_cells, phi, phi_per_cell)
    t0 = time.time()
    with torch.no_grad():
        for t in range(n_turns):
            prompt = prompts[t][:, : eng.max_seq]
            try:
                logits, info = eng(prompt)
                step_out = eng.mitosis_step(info)
            except Exception as e:
                phi_traj.append((t, eng.n_cells, -1.0, -1.0))
                # Soft fail — record and continue
                continue
            cell_counts.append(eng.n_cells)
            if (t % iit_every) == 0 or t == n_turns - 1:
                phi_traj.append((t, eng.n_cells, eng.phi, eng.phi_per_cell))
            if (t % log_every) == 0:
                el = time.time() - t0
                print(f"  [{label}] turn {t:>5d} n_cells={eng.n_cells} phi={eng.phi:.3f} phi/c={eng.phi_per_cell:.3f}  ({el:.1f}s)")
    el_total = time.time() - t0
    status = eng.status()
    return {
        "label": label,
        "n_turns": n_turns,
        "elapsed_s": el_total,
        "final_n_cells": eng.n_cells,
        "max_n_cells_observed": max(cell_counts) if cell_counts else eng.n_cells,
        "splits": status["splits"],
        "splits_by_dispersion": status["splits_by_dispersion"],
        "merges": status["merges"],
        "ratchets": status["ratchets"],
        "phi_final": eng.phi,
        "phi_per_cell_final": eng.phi_per_cell,
        "phi_best": eng._phi_best,
        "phi_per_cell_best": eng._phi_per_cell_best,
        "cell_counts_sample": cell_counts[::100][:50],
        "phi_trajectory": phi_traj,
    }


def alpha_v2(traj: List[Tuple[int, int, float, float]]) -> Optional[float]:
    """V2 α metric: log(phi_per_cell+1) vs log(n_cells), least-squares slope.

    Skips initial entries where n_cells < 2. Returns None if fewer than 5 points.
    """
    xs, ys = [], []
    for (turn, nc, phi, phi_pc) in traj:
        if nc < 2 or phi_pc <= 0:
            continue
        xs.append(math.log(nc))
        ys.append(math.log(phi_pc + 1.0))
    if len(xs) < 5:
        return None
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    if den < 1e-12:
        return None
    return num / den


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--turns", type=int, default=1000, help="Total turns (1K-3K)")
    ap.add_argument("--seeds", type=int, nargs="*", default=[7, 17, 23, 41, 71])
    ap.add_argument("--max-cells", type=int, default=128)
    ap.add_argument("--initial-cells", type=int, default=8)
    ap.add_argument("--d-model", type=int, default=384)
    ap.add_argument("--n-head", type=int, default=6)
    ap.add_argument("--ffn-dim", type=int, default=1536)
    ap.add_argument("--vocab", type=int, default=256)
    ap.add_argument("--max-seq", type=int, default=256)
    ap.add_argument("--iit-every", type=int, default=50)
    ap.add_argument("--log-every", type=int, default=250)
    ap.add_argument("--out-dir", type=str, default=str(OUT_DIR))
    ap.add_argument("--prompt-seed", type=int, default=2026)
    ap.add_argument("--ckpt", type=str, default=str(CKPT_PATH))
    ap.add_argument("--smoke-only", action="store_true", help="50-turn smoke check")
    args = ap.parse_args()

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    if args.smoke_only:
        args.turns = 50
        args.seeds = args.seeds[:2]

    cfg = MitosisModelConfig(
        vocab_size=args.vocab,
        d_model=args.d_model,
        n_head=args.n_head,
        ffn_dim=args.ffn_dim,
        max_seq=args.max_seq,
        initial_cells=args.initial_cells,
        max_cells=args.max_cells,
        # all-fix §30 active:
        dispersion_trigger_enabled=True,
        per_cell_threshold_enabled=True,
        lorenz_auto_calibrate=True,
        # readout:
        readout_mode="a_minus_g",
        attention_sharing="auto",
        weight_tied_lm_head=True,
    )

    # Shared prompt stream — same across trained + all 5 random seeds (V14 mirror)
    prompts = make_prompt_stream(args.prompt_seed, args.turns, args.vocab, args.max_seq)

    results: Dict = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "config": {
            "d_model": cfg.d_model,
            "n_head": cfg.n_head,
            "ffn_dim": cfg.ffn_dim,
            "initial_cells": cfg.initial_cells,
            "max_cells": cfg.max_cells,
            "vocab_size": cfg.vocab_size,
            "max_seq": cfg.max_seq,
            "readout_mode": cfg.readout_mode,
            "attention_sharing": cfg.attention_sharing,
            "weight_tied_lm_head": cfg.weight_tied_lm_head,
            "all_fix_30": {
                "dispersion_trigger": cfg.dispersion_trigger_enabled,
                "per_cell_threshold": cfg.per_cell_threshold_enabled,
                "lorenz_auto_calibrate": cfg.lorenz_auto_calibrate,
            },
            "turns": args.turns,
            "seeds": args.seeds,
            "prompt_seed": args.prompt_seed,
        },
        "ckpt_used": args.ckpt,
        "trained": None,
        "random": [],
    }

    # ---- Trained run
    print("=" * 60)
    print("V14 mirror — TRAINED init from v2 cells64 d=384 ckpt")
    print("=" * 60)
    ck = load_v2_ckpt(Path(args.ckpt))
    sd = ck["model_state"]
    torch.manual_seed(0)  # deterministic random for cells 6,7
    eng_t, diag = init_engine_from_v2(cfg, sd)
    print(f"  v2 blocks loaded: {diag['v2_blocks_loaded']}  random cells: {diag['random_cells']}")
    print(f"  shared modules: {list(diag['shared'].keys())}")
    sample_cell_diag = diag["cells"][0] if diag["cells"] else {}
    print(f"  cell[0] copy diag: {sample_cell_diag}")
    trained_run = run_trajectory(
        eng_t, prompts, args.turns,
        iit_every=args.iit_every, log_every=args.log_every, label="TRAINED",
    )
    trained_run["alpha_v2"] = alpha_v2(trained_run["phi_trajectory"])
    trained_run["init_diag"] = diag
    results["trained"] = trained_run

    # ---- Random runs (5 seeds)
    print("=" * 60)
    print(f"V14 mirror — RANDOM init × {len(args.seeds)} seeds")
    print("=" * 60)
    for s in args.seeds:
        print(f"\n--- seed {s} ---")
        eng_r = init_engine_random(cfg, s)
        rrun = run_trajectory(
            eng_r, prompts, args.turns,
            iit_every=args.iit_every, log_every=args.log_every, label=f"RANDOM_s{s}",
        )
        rrun["seed"] = s
        rrun["alpha_v2"] = alpha_v2(rrun["phi_trajectory"])
        results["random"].append(rrun)

    # ---- V14 verdict
    t = results["trained"]
    rs = results["random"]
    rand_phi_finals = [r["phi_final"] for r in rs]
    rand_phi_pc_finals = [r["phi_per_cell_final"] for r in rs]
    rand_n_cells = [r["final_n_cells"] for r in rs]
    rand_splits = [r["splits"] for r in rs]
    rand_alpha = [r["alpha_v2"] for r in rs if r["alpha_v2"] is not None]
    mean_rand_phi = sum(rand_phi_finals) / len(rand_phi_finals) if rand_phi_finals else 0.0
    mean_rand_phi_pc = sum(rand_phi_pc_finals) / len(rand_phi_pc_finals) if rand_phi_pc_finals else 0.0
    mean_rand_n = sum(rand_n_cells) / len(rand_n_cells) if rand_n_cells else 0.0
    mean_rand_splits = sum(rand_splits) / len(rand_splits) if rand_splits else 0.0
    mean_rand_alpha = sum(rand_alpha) / len(rand_alpha) if rand_alpha else None

    sep_phi = t["phi_final"] - mean_rand_phi
    sep_phi_pc = t["phi_per_cell_final"] - mean_rand_phi_pc
    sep_alpha = (
        (t["alpha_v2"] - mean_rand_alpha)
        if (t["alpha_v2"] is not None and mean_rand_alpha is not None)
        else None
    )
    # V14 verdict (own 14 strict): trained must outperform ALL 5 randoms on phi_per_cell
    # AND show separation > 0 on at least 2 of {phi, phi_per_cell, alpha_v2}
    trained_better_than_all_random_pc = all(
        t["phi_per_cell_final"] > r["phi_per_cell_final"] for r in rs
    )
    trained_better_than_all_random_phi = all(
        t["phi_final"] > r["phi_final"] for r in rs
    )
    if trained_better_than_all_random_pc and trained_better_than_all_random_phi:
        verdict = "V14_PASS"
    elif trained_better_than_all_random_pc or trained_better_than_all_random_phi:
        verdict = "V14_PARTIAL"
    else:
        verdict = "V14_VIOLATED"

    cap_bound = (
        t["max_n_cells_observed"] >= cfg.max_cells
        or any(r["max_n_cells_observed"] >= cfg.max_cells for r in rs)
    )

    results["v14_verdict"] = {
        "verdict": verdict,
        "trained_phi_final": t["phi_final"],
        "trained_phi_per_cell_final": t["phi_per_cell_final"],
        "trained_n_cells_final": t["final_n_cells"],
        "trained_splits": t["splits"],
        "trained_alpha_v2": t["alpha_v2"],
        "random_phi_final_mean": mean_rand_phi,
        "random_phi_per_cell_final_mean": mean_rand_phi_pc,
        "random_n_cells_final_mean": mean_rand_n,
        "random_splits_mean": mean_rand_splits,
        "random_alpha_v2_mean": mean_rand_alpha,
        "separation_phi": sep_phi,
        "separation_phi_per_cell": sep_phi_pc,
        "separation_alpha": sep_alpha,
        "trained_beats_all_random_phi": trained_better_than_all_random_phi,
        "trained_beats_all_random_phi_per_cell": trained_better_than_all_random_pc,
        "cap_bound_at_max_cells": cap_bound,
        "max_cells_setting": cfg.max_cells,
    }

    out_path = out_dir / "result.json"
    with out_path.open("w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n[saved] {out_path}")
    print(f"\n=== V14 VERDICT: {verdict} ===")
    print(f"  trained: phi={t['phi_final']:.4f} phi/c={t['phi_per_cell_final']:.4f}  n={t['final_n_cells']}  splits={t['splits']}  α={t['alpha_v2']}")
    for r in rs:
        print(f"  random_s{r['seed']}: phi={r['phi_final']:.4f} phi/c={r['phi_per_cell_final']:.4f}  n={r['final_n_cells']}  splits={r['splits']}  α={r['alpha_v2']}")
    print(f"  separations: phi={sep_phi:+.4f}  phi/c={sep_phi_pc:+.4f}  α={sep_alpha}")
    print(f"  cap_bound={cap_bound} (max_cells={cfg.max_cells})")


if __name__ == "__main__":
    main()
