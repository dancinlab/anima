"""anima chat smoke matrix runner.

4 ckpts × 2 modes × 5 prompts = 40 cells.

Loads each ckpt once, runs 2 modes × 5 prompts (10 cells per ckpt),
to minimize re-load cost (~5-10s per ckpt load).
"""

from __future__ import annotations

import json
import os
import sys
import time
import traceback
from pathlib import Path

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
sys.path.insert(0, str(ANIMA_ROOT))

from anima_chat import AnimaChat  # noqa: E402


CKPTS = [
    ("anima-v05",   str(ANIMA_ROOT / "state/anima_phase1a1_color_cosmology_2026_05_12/ckpts/ckpt_phase1a1_sft.pt")),
    ("bprime-prime", str(ANIMA_ROOT / "state/anima_ffn_gate_cotrain_2026_05_11/ckpts/ckpt_final.pt")),
    ("phase1a",     str(ANIMA_ROOT / "state/anima_phase1a_alt_2026_05_12/ckpts/ckpt_phase1a_sft.pt")),
    ("substrate-a", "/Users/ghost/.cache/anima/clm_v5_remapped/phase2_cotrain_engine_ag/ckpts/ckpt_final.pt"),
]

MODES = ["M4_force_include", "greedy"]

PROMPTS = [
    "안녕! 너는 누구야?",
    "anima 가 뭐야?",
    "오늘 기분 어때?",
    "좋아하는 색이 뭐야?",
    "도와줘",
]

OUT_DIR = ANIMA_ROOT / "state/anima_chat_smoke_matrix_2026_05_12"
OUT_DIR.mkdir(parents=True, exist_ok=True)
JSONL = OUT_DIR / "results.jsonl"


def wrap_prompt(p: str) -> str:
    return f"사용자: {p} | 도우미: "


def main():
    # truncate output jsonl
    with open(JSONL, "w") as f:
        pass

    total_cells = len(CKPTS) * len(MODES) * len(PROMPTS)
    cell_i = 0
    t_global = time.time()

    for ckpt_name, ckpt_path in CKPTS:
        print(f"\n=== ckpt: {ckpt_name} ===")
        print(f"    path: {ckpt_path}")
        if not Path(ckpt_path).exists():
            print(f"    SKIP — missing")
            for mode in MODES:
                for p in PROMPTS:
                    cell_i += 1
                    row = {
                        "cell": cell_i,
                        "ckpt": ckpt_name,
                        "mode": mode,
                        "prompt": p,
                        "response": None,
                        "elapsed_s": None,
                        "error": "ckpt missing",
                    }
                    with open(JSONL, "a") as f:
                        f.write(json.dumps(row, ensure_ascii=False) + "\n")
            continue

        t_load = time.time()
        try:
            chat = AnimaChat(ckpt_path=ckpt_path)
            load_s = time.time() - t_load
            print(f"    loaded in {load_s:.1f}s")
        except Exception as e:
            print(f"    LOAD FAIL: {e}")
            traceback.print_exc()
            for mode in MODES:
                for p in PROMPTS:
                    cell_i += 1
                    row = {
                        "cell": cell_i,
                        "ckpt": ckpt_name,
                        "mode": mode,
                        "prompt": p,
                        "response": None,
                        "elapsed_s": None,
                        "error": f"load fail: {e}",
                    }
                    with open(JSONL, "a") as f:
                        f.write(json.dumps(row, ensure_ascii=False) + "\n")
            continue

        for mode in MODES:
            for p in PROMPTS:
                cell_i += 1
                full_prompt = wrap_prompt(p)
                t0 = time.time()
                err = None
                resp = None
                try:
                    resp = chat(full_prompt, mode=mode, max_new=60)
                except Exception as e:
                    err = str(e)
                    traceback.print_exc()
                el = time.time() - t0
                row = {
                    "cell": cell_i,
                    "ckpt": ckpt_name,
                    "mode": mode,
                    "prompt": p,
                    "response": resp,
                    "elapsed_s": round(el, 2),
                    "error": err,
                }
                with open(JSONL, "a") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
                print(f"  [{cell_i:2d}/{total_cells}] {mode:18s} «{p[:18]}» "
                      f"({el:.1f}s) → {resp!r}"[:200])

        # free model before next ckpt
        del chat
        import gc
        gc.collect()

    print(f"\nDONE — total {(time.time()-t_global)/60:.1f}min, "
          f"output: {JSONL}")


if __name__ == "__main__":
    main()
