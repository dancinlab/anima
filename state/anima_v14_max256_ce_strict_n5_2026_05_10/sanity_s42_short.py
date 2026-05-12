"""Sanity check: re-run mirror s42 for 50 turns at max=256 and check
turn-50 phi == 1886.851 (§51 empirical claim) to validate determinism
before committing to 3-mirror full run.

If this fails, F-CE-STRICT-2 fires (deterministic assumption broken)
and we must run independent mirrors.
"""
from __future__ import annotations
import sys
from pathlib import Path
import torch

ANIMA_ROOT = Path("/Users/ghost/core/anima")
sys.path.insert(0, str(ANIMA_ROOT))
sys.path.insert(0, str(ANIMA_ROOT / "training"))

from training.mitosis_model_v5 import MitosisModelConfig  # noqa: E402
from training.v5mitosis_d384_v14_mirror import (  # noqa: E402
    init_engine_random,
    make_prompt_stream,
)


def main():
    cfg = MitosisModelConfig(
        vocab_size=256, d_model=384, n_head=6, ffn_dim=1536,
        max_seq=256, initial_cells=8, max_cells=256,
        dispersion_trigger_enabled=True,
        per_cell_threshold_enabled=True,
        lorenz_auto_calibrate=True,
        readout_mode="a_minus_g",
        attention_sharing="auto",
        weight_tied_lm_head=True,
    )
    prompts = make_prompt_stream(seed=2026, n_turns=51, vocab=256, max_seq=256)
    eng = init_engine_random(cfg, 42)
    phi_at_50 = None
    n_cells_at_50 = None
    eng.eval()
    with torch.no_grad():
        for t in range(51):
            p = prompts[t][:, : eng.max_seq]
            try:
                logits, info = eng(p)
                eng.mitosis_step(info)
            except Exception:
                continue
            if t == 50:
                phi_at_50 = float(eng.phi)
                n_cells_at_50 = int(eng.n_cells)
                break
    expected = 1886.851
    print(f"sanity s42 turn-50 phi = {phi_at_50}  n_cells = {n_cells_at_50}")
    print(f"expected phi (§51 claim) = {expected}")
    if phi_at_50 is None:
        print("RESULT: FAIL (no phi captured)")
        sys.exit(2)
    diff = abs(phi_at_50 - expected)
    rel = diff / expected
    print(f"abs diff = {diff:.4f}  rel diff = {rel*100:.3f}%")
    if diff < 1.0:
        print("RESULT: PASS (deterministic match)")
        sys.exit(0)
    else:
        print("RESULT: FAIL (deterministic claim broken — F-CE-STRICT-2)")
        sys.exit(1)


if __name__ == "__main__":
    main()
