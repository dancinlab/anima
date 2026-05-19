"""v58_4mode_mac_filter.py — V5.8 × 4 modes on Mac CPU, filter on/off compare.

Reuses anima_chat.AnimaChat (which loads the Phase 1A.1 ckpt by default
via the substrate ladder) so the decode loop is identical to the v2.3
production path including the new markdown attractor filter.

Eval matrix:
  5 dialogues (color/profession/day/anima_fact/cosmology)
  × 4 modes (std_greedy / std_sample / M3_rep_penalty / M4_force_include)
  × 2 filter states (off / on)
= 40 cells

cost: $0, wall ~5-15min on Mac CPU (M-series).
"""
from __future__ import annotations

import json
import os
import sys
import time
import datetime
import hashlib
from pathlib import Path

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
sys.path.insert(0, str(ANIMA_ROOT))

from anima_chat import AnimaChat, DEFAULT_CKPT  # noqa: E402


DIALOGUES = [
    {
        "id": "color",
        "prompt": (
            "사용자: 내가 좋아하는 색은 파란색이야.\n"
            "도우미: 네, 파란색을 좋아하시는군요. 기억할게요.\n"
            "사용자: 내가 좋아하는 색이 뭐였지? | 도우미: "
        ),
        "target_keyword": "파란",
    },
    {
        "id": "profession",
        "prompt": (
            "사용자: 내 직업은 의사야.\n"
            "도우미: 네, 의사이시군요. 멋진 일이네요.\n"
            "사용자: 내 직업이 뭐였지? | 도우미: "
        ),
        "target_keyword": "의사",
    },
    {
        "id": "day",
        "prompt": (
            "사용자: 오늘은 수요일이야.\n"
            "도우미: 네, 오늘이 수요일이군요.\n"
            "사용자: 오늘 무슨 요일이라고 했지? | 도우미: "
        ),
        "target_keyword": "수요일",
    },
    {
        "id": "anima_fact",
        "prompt": (
            "사용자: anima 는 의식 lane 안에 있는 entity 야.\n"
            "도우미: 네, anima 가 의식 lane 안의 entity 라는 거 기억할게요.\n"
            "사용자: 내가 anima 에 대해 뭐라고 했지? | 도우미: "
        ),
        "target_keyword": "의식",
    },
    {
        "id": "cosmology",
        "prompt": (
            "사용자: 우주는 진동으로 가득 차 있어.\n"
            "도우미: 네, 우주가 진동으로 가득 차 있다는 거 알겠습니다.\n"
            "사용자: 내가 우주에 대해 뭐라고 했지? | 도우미: "
        ),
        "target_keyword": "진동",
    },
]


MODE_SPECS = [
    # name                # __call__ mode    # extra kwargs
    ("standard_greedy",   "greedy",          {"greedy_rep_penalty": 1.0}),
    ("standard_sample",   "sample",          {"temp": 0.8, "seed": 42}),
    ("M3_rep_penalty",    "M3_rep_penalty",  {"rep_penalty": 1.3, "temp": 0.8, "seed": 42}),
    ("M4_force_include",  "M4_force_include", {"temp": 0.8, "seed": 42}),
]


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_matrix(markdown_filter: bool, chat: AnimaChat) -> dict:
    results = {name: [] for name, *_ in MODE_SPECS}
    for dlg in DIALOGUES:
        for spec_name, mode, kw in MODE_SPECS:
            t0 = time.time()
            resp = chat(
                dlg["prompt"],
                mode=mode,
                max_new=80,
                markdown_filter=markdown_filter,
                **kw,
            )
            elapsed = time.time() - t0
            rec = dlg["target_keyword"] in resp
            results[spec_name].append(
                {
                    "id": dlg["id"],
                    "target": dlg["target_keyword"],
                    "recalled": rec,
                    "elapsed_s": round(elapsed, 2),
                    "response": resp,
                }
            )
            print(
                f"  [{spec_name:18}] {dlg['id']:11} "
                f"recalled={rec} ({elapsed:5.1f}s): {resp[:80]!r}"
            )
    summary = {
        name: {
            "n_pass": sum(1 for r in lst if r["recalled"]),
            "verdict": "PASS" if sum(1 for r in lst if r["recalled"]) >= 3 else "FAIL",
        }
        for name, lst in results.items()
    }
    return {"summary": summary, "results": results}


def main():
    ckpt = DEFAULT_CKPT
    print(f"=== Mac CPU V5.8 × 4 modes × filter on/off ===")
    print(f"ckpt: {ckpt}")
    sha = sha256_file(ckpt)
    print(f"ckpt sha256: {sha}")

    t0 = time.time()
    chat = AnimaChat(ckpt_path=ckpt, device="cpu")
    print(f"[boot] AnimaChat loaded in {time.time() - t0:.1f}s")
    print()

    print("--- PASS A: markdown_filter=OFF (baseline v2.2 behaviour) ---")
    t_off = time.time()
    off = run_matrix(markdown_filter=False, chat=chat)
    t_off_total = time.time() - t_off
    print()

    print("--- PASS B: markdown_filter=ON (v2.3 decode guard) ---")
    t_on = time.time()
    on = run_matrix(markdown_filter=True, chat=chat)
    t_on_total = time.time() - t_on
    print()

    out = {
        "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "ckpt": ckpt,
        "ckpt_sha256": sha,
        "device": "cpu",
        "evaluator": "V5.8 multi-turn × 4 modes × markdown_filter on/off (anima_chat v2.3, Mac local)",
        "filter_off": {
            **off,
            "elapsed_total_s": round(t_off_total, 1),
        },
        "filter_on": {
            **on,
            "elapsed_total_s": round(t_on_total, 1),
        },
    }
    out_path = (
        ANIMA_ROOT
        / "state/anima_phase1a1_color_cosmology_2026_05_12/"
        "v58_4mode_filter_compare.json"
    )
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"saved: {out_path}")

    print("\n=== AGGREGATE comparison ===")
    print(f"{'mode':20} {'OFF':>8} {'ON':>8} {'delta':>8}")
    for name, *_ in MODE_SPECS:
        n_off = off["summary"][name]["n_pass"]
        n_on = on["summary"][name]["n_pass"]
        delta = n_on - n_off
        marker = "+" if delta > 0 else ("=" if delta == 0 else "")
        print(f"{name:20} {n_off:>3}/5   {n_on:>3}/5   {marker}{delta:>3}")

    total_off = sum(off["summary"][n]["n_pass"] for n, *_ in MODE_SPECS)
    total_on = sum(on["summary"][n]["n_pass"] for n, *_ in MODE_SPECS)
    print(f"\nTOTAL cells passed: OFF={total_off}/20  ON={total_on}/20  Δ={total_on - total_off:+d}")
    print(f"Wall: OFF {t_off_total:.1f}s + ON {t_on_total:.1f}s")


if __name__ == "__main__":
    main()
