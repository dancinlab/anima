"""Smoke test: greedy_rep_penalty 1.0 vs 1.05 vs 1.10 across 5 prompts.

Compares repetition suppression for Phase 1A.1 ckpt (B'.1, default).
Measures unique-byte-token ratio and length distribution.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

# Use the current checkout unless the caller selects another checkout explicitly.
REPO = Path(os.environ.get("ANIMA_ROOT", Path(__file__).resolve().parents[1])).resolve()
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "training"))

from anima_chat import AnimaChat, ByteTokenizer  # noqa: E402

PROMPTS = [
    "안녕!",
    "안녕 누구야?",
    "오늘 어때?",
    "도와줘",
    "좋아하는 색?",
]
PENALTIES = [1.0, 1.05, 1.10]
MAX_NEW = 60
SEED = 2026


def unique_token_ratio(text: str) -> float:
    """unique-byte-token / total-byte-token ratio (1.0 = all unique)."""
    tok = ByteTokenizer()
    ids = [i for i in tok.encode(text) if i not in (tok.bos, tok.eos)]
    if not ids:
        return 0.0
    return len(set(ids)) / len(ids)


def main() -> None:
    print("=" * 76)
    print("anima_chat greedy rep_penalty smoke (Phase 1A.1 / B'.1)")
    print("=" * 76)
    t0 = time.time()
    chat = AnimaChat()
    print(f"[boot] AnimaChat loaded in {time.time() - t0:.1f}s")
    print(f"[ckpt] {chat.cfg!r}"[:120])
    print()

    rows = []
    for penalty in PENALTIES:
        print(f"--- greedy_rep_penalty = {penalty} ---")
        ratios = []
        lens = []
        for p in PROMPTS:
            full = f"사용자: {p} | 도우미: "
            r = chat(
                full,
                mode="greedy",
                max_new=MAX_NEW,
                greedy_rep_penalty=penalty,
                seed=SEED,
            )
            ratio = unique_token_ratio(r)
            ratios.append(ratio)
            lens.append(len(r.encode("utf-8")))
            preview = r.replace("\n", " ⏎ ")
            if len(preview) > 64:
                preview = preview[:64] + "…"
            print(f"  [{p:14}] uniq={ratio:.2f} bytes={lens[-1]:3d}  | {preview}")
            rows.append({
                "penalty": penalty,
                "prompt": p,
                "response": r,
                "unique_ratio": ratio,
                "byte_len": lens[-1],
            })
        avg_r = sum(ratios) / len(ratios)
        avg_l = sum(lens) / len(lens)
        print(f"  avg_unique_ratio = {avg_r:.3f}   avg_bytes = {avg_l:.1f}")
        print()

    # write JSON sidecar to state/ for the markdown doc to reference
    out_path = REPO / "state" / "anima_greedy_rep_penalty_2026_05_12.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2))
    print(f"[json] wrote {out_path}")
    print(f"[done] total {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
