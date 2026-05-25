"""v58_seed42_anima_fact_probe.py — reproduce §17 markdown drift evidence.

§17 (and §25) report that anima_fact standard_greedy emits:
    "��답 (consciousness) |\n| --- | --- |\n| `/Users/ghost/core/contact/scripts/send."
on seed=42, GPU bf16. anima_chat default seed=2026 / CPU fp32 path did
NOT reproduce this (v58_4mode_filter_compare.json shows semantic miss
without markdown drift).

This probe forces seed=42 and uses ONLY the anima_fact dialogue to
isolate filter on/off behaviour where the attractor *should* fire.
"""
from __future__ import annotations

import os
import sys
import time
import json
from pathlib import Path

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
sys.path.insert(0, str(ANIMA_ROOT))
from anima_chat import AnimaChat, DEFAULT_CKPT  # noqa: E402

PROMPT = (
    "사용자: anima 는 의식 lane 안에 있는 entity 야.\n"
    "도우미: 네, anima 가 의식 lane 안의 entity 라는 거 기억할게요.\n"
    "사용자: 내가 anima 에 대해 뭐라고 했지? | 도우미: "
)
TARGET = "의식"

chat = AnimaChat(ckpt_path=DEFAULT_CKPT, device="cpu")

# probe seeds that might reproduce §17 markdown drift
PROBE_SEEDS = [42, 2024, 2025, 2026, 7, 13, 100, 31337]

out_rows = []
for seed in PROBE_SEEDS:
    for filt in [False, True]:
        t0 = time.time()
        resp = chat(
            PROMPT,
            mode="greedy",
            max_new=80,
            greedy_rep_penalty=1.0,  # match V5.8 eval (no greedy rep_penalty)
            seed=seed,
            markdown_filter=filt,
        )
        elapsed = time.time() - t0
        rec = TARGET in resp
        has_md = "| --- " in resp or "\n| " in resp
        out_rows.append({
            "seed": seed, "filter": filt, "recalled": rec,
            "markdown_drift": has_md, "elapsed_s": round(elapsed, 1),
            "response": resp,
        })
        print(
            f"seed={seed:>5}  filter={'ON ' if filt else 'OFF'}  "
            f"recalled={rec}  md_drift={has_md}  "
            f"({elapsed:5.1f}s)  → {resp[:80]!r}"
        )

# diff cells (where OFF has md_drift and ON resolves it)
print()
print("=== filter PROVENANCE cells (OFF had md_drift) ===")
for i in range(0, len(out_rows), 2):
    off = out_rows[i]
    on = out_rows[i + 1]
    if off["markdown_drift"]:
        print(f"  seed={off['seed']}:")
        print(f"    OFF: drift={off['markdown_drift']} recall={off['recalled']}  {off['response'][:80]!r}")
        print(f"    ON : drift={on['markdown_drift']} recall={on['recalled']}  {on['response'][:80]!r}")

out_path = ANIMA_ROOT / "state/anima_phase1a1_color_cosmology_2026_05_12/v58_seed_probe.json"
with open(out_path, "w") as f:
    json.dump({"rows": out_rows, "ckpt": DEFAULT_CKPT}, f, indent=2, ensure_ascii=False)
print(f"\nsaved: {out_path}")
