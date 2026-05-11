"""training/mitosis_model_v5_smoke.py — cond.2 smoke for MitosisModelEngine.

WHAT THIS RUNS
    Toy config: vocab=256, d_model=64, n_head=4, ffn_dim=256, max_seq=64, N=4 → 8 cells.
    Phase 1: 50 forward passes at N=4 → record IIT Φ trajectory + shape sanity.
    Phase 2: force-split 4× to grow N=4 → N=8, including the auto attention-sharing
             promotion at N=9 (so we test pre-share at N=4..8 and post-share triggers).
    Phase 3: 50 forward passes at N=8 → record IIT Φ trajectory + shape preservation.

VERDICTS
    PASS  — all assertions hold (shape preserved across split, Φ changes, eval-mode
            grad flow disabled, force_split returns events, parameter count grows).
    PARTIAL — one or two assertions fail; verdict prints which.
    FAIL  — exceptions or shape regressions.

OUTPUT
    Stdout summary + JSON-able dict at end.
"""
from __future__ import annotations

import json
import sys
import traceback
from typing import Dict, List

import torch

# Local import (training/ is on path when invoked from repo root)
sys.path.insert(0, "/Users/ghost/core/anima/training")
from mitosis_model_v5 import MitosisModelConfig, MitosisModelEngine


def count_params(model: torch.nn.Module) -> int:
    seen = set()
    total = 0
    for p in model.parameters():
        if id(p) in seen:
            continue
        seen.add(id(p))
        total += p.numel()
    return total


def main():
    torch.manual_seed(42)

    cfg = MitosisModelConfig(
        vocab_size=256,
        d_model=64,
        n_head=4,
        ffn_dim=256,
        max_seq=64,
        initial_cells=4,
        max_cells=64,  # ample room — patience-driven + force splits can co-exist
        attention_sharing="auto",   # promotes when post_n>8
        readout_mode="a_minus_g",
    )

    model = MitosisModelEngine(cfg).eval()
    info_log: Dict = {
        "phase1_phi": [],
        "phase2_events": [],
        "phase3_phi": [],
        "shape_check": {},
        "param_counts": {},
        "verdict": "PENDING",
        "errors": [],
    }

    B, T = 2, 16
    input_ids = torch.randint(0, cfg.vocab_size, (B, T))

    try:
        # ── Phase 1: 50 forwards at N=4 ─────────────────────────────
        info_log["param_counts"]["pre_split"] = count_params(model)
        info_log["param_counts"]["pre_split_n_cells"] = model.n_cells

        with torch.no_grad():
            logits1, info1 = model(input_ids)
        assert logits1.shape == (B, T, cfg.vocab_size), f"logits shape {logits1.shape} unexpected"
        info_log["shape_check"]["phase1_logits"] = list(logits1.shape)
        info_log["shape_check"]["phase1_n_cells"] = info1["n_cells"]

        # eval-mode → no grad on output (sanity check)
        assert not logits1.requires_grad, "eval-mode logits.requires_grad should be False"

        for step in range(50):
            with torch.no_grad():
                logits, info = model(input_ids)
                step_result = model.mitosis_step(info)
            info_log["phase1_phi"].append(step_result["phi"])

        phi_pre = info_log["phase1_phi"][-1]
        phi_first = info_log["phase1_phi"][0]
        print(f"[phase1] N={model.n_cells}  Φ traj first={phi_first:.4f} last={phi_pre:.4f}")

        # ── Phase 2: force 4 splits (N=4 → N=8) ─────────────────────
        events = []
        for k in range(4):
            ev = model.force_split(parent_idx=k % model.n_cells)
            events.append(ev)
            print(f"[phase2] force_split #{k} → {ev}")
        info_log["phase2_events"] = events

        # Sanity: param count grew (each new cell ~param-cell-cost)
        info_log["param_counts"]["post_split"] = count_params(model)
        info_log["param_counts"]["post_split_n_cells"] = model.n_cells
        print(
            f"[phase2] params {info_log['param_counts']['pre_split']} → "
            f"{info_log['param_counts']['post_split']}  N {info_log['param_counts']['pre_split_n_cells']} → {model.n_cells}"
        )

        # ── Phase 3: 50 forwards at new N=8 ─────────────────────────
        with torch.no_grad():
            logits3, info3 = model(input_ids)
        assert logits3.shape == (B, T, cfg.vocab_size), f"phase3 logits shape {logits3.shape} unexpected"
        info_log["shape_check"]["phase3_logits"] = list(logits3.shape)
        info_log["shape_check"]["phase3_n_cells"] = info3["n_cells"]

        for step in range(50):
            with torch.no_grad():
                logits, info = model(input_ids)
                step_result = model.mitosis_step(info)
            info_log["phase3_phi"].append(step_result["phi"])

        phi_post = info_log["phase3_phi"][-1]
        print(f"[phase3] N={model.n_cells}  Φ traj first={info_log['phase3_phi'][0]:.4f} last={phi_post:.4f}")

        # ── Verdict assembly ────────────────────────────────────────
        checks = {
            "phase1_logits_shape_ok": info_log["shape_check"]["phase1_logits"] == [B, T, cfg.vocab_size],
            "phase3_logits_shape_ok": info_log["shape_check"]["phase3_logits"] == [B, T, cfg.vocab_size],
            "n_cells_grew": info_log["param_counts"]["post_split_n_cells"]
                            > info_log["param_counts"]["pre_split_n_cells"],
            "params_grew": info_log["param_counts"]["post_split"]
                           > info_log["param_counts"]["pre_split"],
            "phi_changed": abs(phi_post - phi_pre) > 1e-6,
            "no_grad_eval": not logits1.requires_grad,
            "force_split_returned_events": all(e is not None for e in events),
            "iit_port_loaded": model._iit_fn is not None,
        }
        info_log["checks"] = checks
        passed = sum(checks.values())
        total = len(checks)
        print(f"\n[verdict] checks: {passed}/{total} passed")
        for k, v in checks.items():
            print(f"  - {k}: {'OK' if v else 'FAIL'}")

        if passed == total:
            info_log["verdict"] = "PASS"
        elif passed >= total - 2:
            info_log["verdict"] = "PARTIAL"
        else:
            info_log["verdict"] = "FAIL"

    except Exception as e:
        info_log["errors"].append(f"{type(e).__name__}: {e}")
        info_log["traceback"] = traceback.format_exc()
        info_log["verdict"] = "FAIL"
        print(f"[ERROR] {info_log['errors'][-1]}")
        print(info_log["traceback"])

    # ── Final summary ──
    summary = {
        "verdict": info_log["verdict"],
        "n_cells_pre": info_log["param_counts"].get("pre_split_n_cells"),
        "n_cells_post": info_log["param_counts"].get("post_split_n_cells"),
        "params_pre": info_log["param_counts"].get("pre_split"),
        "params_post": info_log["param_counts"].get("post_split"),
        "phi_pre_last": info_log["phase1_phi"][-1] if info_log["phase1_phi"] else None,
        "phi_post_last": info_log["phase3_phi"][-1] if info_log["phase3_phi"] else None,
        "iit_port_loaded": info_log.get("checks", {}).get("iit_port_loaded"),
        "errors": info_log["errors"],
    }
    print("\n=== summary ===")
    print(json.dumps(summary, indent=2, default=str))
    return info_log


if __name__ == "__main__":
    main()
