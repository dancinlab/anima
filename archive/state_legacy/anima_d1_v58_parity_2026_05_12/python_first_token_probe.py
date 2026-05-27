"""python_first_token_probe.py — V5.8 5-cell first-token greedy probe.

For each V5.8 cell (color/profession/day/anima_fact/cosmology), runs ONE
greedy forward through anima_chat.py's underlying model and emits the
argmax token id at the FIRST decode position. This is the byte-by-byte
parity SSOT for anima_chat.hexa (hexa lane) comparison.

Output: state/anima_d1_v58_parity_2026_05_12/python_first_token.json
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
from anima_chat import AnimaChat, DEFAULT_CKPT, ByteTokenizer

CELLS = [
    {
        "id": "color",
        "prompt": (
            "사용자: 내가 좋아하는 색은 파란색이야.\n"
            "도우미: 네, 파란색을 좋아하시는군요. 기억할게요.\n"
            "사용자: 내가 좋아하는 색이 뭐였지? | 도우미: "
        ),
    },
    {
        "id": "profession",
        "prompt": (
            "사용자: 내 직업은 의사야.\n"
            "도우미: 네, 의사이시군요. 멋진 일이네요.\n"
            "사용자: 내 직업이 뭐였지? | 도우미: "
        ),
    },
    {
        "id": "day",
        "prompt": (
            "사용자: 오늘은 수요일이야.\n"
            "도우미: 네, 오늘이 수요일이군요.\n"
            "사용자: 오늘 무슨 요일이라고 했지? | 도우미: "
        ),
    },
    {
        "id": "anima_fact",
        "prompt": (
            "사용자: anima 는 의식 lane 안에 있는 entity 야.\n"
            "도우미: 네, anima 가 의식 lane 안의 entity 라는 거 기억할게요.\n"
            "사용자: 내가 anima 에 대해 뭐라고 했지? | 도우미: "
        ),
    },
    {
        "id": "cosmology",
        "prompt": (
            "사용자: 우주는 진동으로 가득 차 있어.\n"
            "도우미: 네, 우주가 진동으로 가득 차 있다는 거 알겠습니다.\n"
            "사용자: 내가 우주에 대해 뭐라고 했지? | 도우미: "
        ),
    },
]


def main():
    print("=" * 64)
    print("V5.8 first-token greedy probe (Python lane, Mac CPU)")
    print("=" * 64)
    t0 = time.time()
    chat = AnimaChat(ckpt_path=DEFAULT_CKPT, device="cpu")
    boot = time.time() - t0
    print(f"[boot] AnimaChat loaded in {boot:.1f}s, ckpt={DEFAULT_CKPT}")

    tok = chat.tok
    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ckpt": DEFAULT_CKPT,
        "device": "cpu",
        "boot_s": round(boot, 2),
        "cells": [],
    }

    for cell in CELLS:
        pid = cell["id"]
        prompt = cell["prompt"]
        ids = tok.encode(prompt)
        # drop trailing EOS so we continue (mirror chat_generate semantics)
        if ids and ids[-1] == tok.eos:
            ids = ids[:-1]
        prefill_n = len(ids)

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
        # Decode the argmax id into UTF-8 representation when within byte range
        if 3 <= argmax_id < 259:
            byte_val = argmax_id - 3
            try:
                decoded_char = bytes([byte_val]).decode("utf-8", errors="replace")
            except Exception:
                decoded_char = "?"
        elif argmax_id == 0:
            decoded_char = "<PAD>"
        elif argmax_id == 1:
            decoded_char = "<BOS>"
        elif argmax_id == 2:
            decoded_char = "<EOS>"
        else:
            decoded_char = "<oov>"
        cell_out = {
            "id": pid,
            "prefill_n": prefill_n,
            "first_token_argmax_id": argmax_id,
            "first_token_argmax_val": round(argmax_val, 6),
            "first_token_decoded_char": decoded_char,
            "wall_s": round(wall, 3),
        }
        out["cells"].append(cell_out)
        print(
            f"  [{pid:11}] prefill_n={prefill_n:3}  "
            f"argmax_id={argmax_id:5} ({decoded_char!r:8})  "
            f"val={argmax_val:+8.3f}  wall={wall:5.1f}s"
        )

    out_path = ANIMA_ROOT / "state/anima_d1_v58_parity_2026_05_12/python_first_token.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\nsaved: {out_path}")
    print(f"total wall: {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
