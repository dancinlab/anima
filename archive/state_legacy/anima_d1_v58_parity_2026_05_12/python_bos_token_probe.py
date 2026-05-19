"""python_bos_token_probe.py — single-BOS forward parity SSOT for hexa lane.

Runs ONE forward through anima_chat.py's underlying model with:
  - input tokens: [BOS]  (i.e. ids = [1])
  - position: t=0
  - device: cpu, dtype: model native (fp32 for Phase 1A.1 CPU lane)

Reports the greedy argmax id over vocab=32000.

This file is the SSOT for the hexa lane's
state/anima_d1_v58_parity_2026_05_12/v58_hexa_parity.hexa
F-D1-V58PARITY-2c assertion ("argmax matches Python lane").

Output: state/anima_d1_v58_parity_2026_05_12/python_first_token_bos.json
"""
import json
import os
import sys
import time
import datetime
from pathlib import Path

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
sys.path.insert(0, str(ANIMA_ROOT))

import torch
from anima_chat import AnimaChat, DEFAULT_CKPT


def main():
    print("=" * 64)
    print("BOS-only first-token greedy probe (Python lane, Mac CPU)")
    print("=" * 64)
    t0 = time.time()
    chat = AnimaChat(ckpt_path=DEFAULT_CKPT, device="cpu")
    boot = time.time() - t0
    print(f"[boot] AnimaChat loaded in {boot:.1f}s, ckpt={DEFAULT_CKPT}")

    # Input: [BOS] alone
    ids = [chat.tok.bos]  # = [1]
    x = torch.tensor([ids], dtype=torch.long, device="cpu")

    t1 = time.time()
    with torch.no_grad():
        outm = chat.model(x)
        if isinstance(outm, dict):
            logits = outm["logits"]
        elif isinstance(outm, tuple):
            logits = outm[0]
        else:
            logits = outm
        last = logits[0, -1].float()
        argmax_id = int(torch.argmax(last).item())
        argmax_val = float(last[argmax_id].item())
        # Top-5 for diagnostic
        topk_v, topk_i = torch.topk(last, k=5)
        topk = [
            {"id": int(topk_i[i].item()), "val": round(float(topk_v[i].item()), 6)}
            for i in range(5)
        ]
    wall = time.time() - t1

    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ckpt": DEFAULT_CKPT,
        "device": "cpu",
        "boot_s": round(boot, 2),
        "input_token_ids": ids,
        "input_position_t": 0,
        "first_token_argmax_id": argmax_id,
        "first_token_argmax_val": round(argmax_val, 6),
        "top5": topk,
        "wall_s": round(wall, 3),
    }
    print(f"  argmax_id={argmax_id} val={argmax_val:+8.3f}  wall={wall:.3f}s")
    print(f"  top5: {[(t['id'], t['val']) for t in topk]}")

    out_path = ANIMA_ROOT / "state/anima_d1_v58_parity_2026_05_12/python_first_token_bos.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nsaved: {out_path}")


if __name__ == "__main__":
    main()
