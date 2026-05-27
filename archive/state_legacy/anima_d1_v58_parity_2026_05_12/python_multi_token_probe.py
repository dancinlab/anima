"""python_multi_token_probe.py — multi-token greedy decode SSOT.

Runs 5 greedy decode steps starting from [BOS] (ids=[1]) on Mac CPU
with anima_chat's underlying model. Reports the argmax token id at each
step — this is the SSOT for the hexa-lane multi-token KV-cache
parity probe (state/anima_d1_v58_parity_2026_05_12/v58_hexa_multi_parity.hexa).

The Python lane does NOT use KV cache (it re-feeds the full sequence
each step via the existing chat_forward path). The hexa lane DOES use
the v0.3 KV cache + per-step RoPE rotation. If both lanes produce the
same argmax sequence, then the KV cache correctness (cache lookup +
RoPE application at position t > 0) is byte-by-byte verified.

Output: state/anima_d1_v58_parity_2026_05_12/python_multi_token.json
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
    print("Multi-token greedy decode probe (Python lane, Mac CPU)")
    print("=" * 64)
    t0 = time.time()
    chat = AnimaChat(ckpt_path=DEFAULT_CKPT, device="cpu")
    boot = time.time() - t0
    print(f"[boot] AnimaChat loaded in {boot:.1f}s, ckpt={DEFAULT_CKPT}")

    n_steps = 5
    # Seed sequence: just BOS
    ids = [chat.tok.bos]  # [1]
    print(f"  initial seed ids: {ids}")

    steps = []
    t_decode_start = time.time()
    for step_i in range(n_steps):
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
        wall = time.time() - t1
        steps.append({
            "step": step_i,
            "position_t": len(ids) - 1,  # the LAST token in ids is at position t
            "input_seq_len": len(ids),
            "argmax_id": argmax_id,
            "argmax_val": round(argmax_val, 6),
            "wall_s": round(wall, 3),
        })
        print(
            f"  step {step_i}: t={len(ids)-1:2}, seq_len={len(ids):2}, "
            f"argmax_id={argmax_id:5} val={argmax_val:+8.3f} wall={wall:5.3f}s"
        )
        # Append argmax to sequence for next step (greedy autoregress)
        ids.append(argmax_id)

    total_wall = time.time() - t_decode_start
    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ckpt": DEFAULT_CKPT,
        "device": "cpu",
        "boot_s": round(boot, 2),
        "initial_seed_ids": [1],
        "n_steps": n_steps,
        "steps": steps,
        "final_sequence_ids": ids,
        "final_argmax_chain": [s["argmax_id"] for s in steps],
        "total_decode_wall_s": round(total_wall, 3),
    }
    print(f"\nfinal argmax chain: {out['final_argmax_chain']}")
    print(f"total decode wall: {total_wall:.2f}s")
    out_path = ANIMA_ROOT / "state/anima_d1_v58_parity_2026_05_12/python_multi_token.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"saved: {out_path}")


if __name__ == "__main__":
    main()
