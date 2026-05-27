"""Smoke test: M4_force_include (hard) vs M4_soft_force (logit boost) vs greedy.

5 fixed prompts × 3 modes; reports per-mode chat-cap pass-rate proxy
(natural Korean heuristic) + raw responses for honest before/after table.

Usage (Mac side, where torch + ckpt are present):
    .venv-eeg/bin/python scripts/anima_m4_natural_smoke_2026_05_12.py

Outputs:
    state/anima_m4_natural_smoke_2026_05_12.json   (raw results)

The pass heuristic is intentionally permissive — it flags "mechanical"
responses where the keyword ends the line as the very last token (V5.8
hard-insert signature) so we can compare against soft-force naturally.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

os.environ.setdefault("ANIMA_ROOT", "/Users/ghost/core/anima")

REPO = Path(os.environ["ANIMA_ROOT"])
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "training"))

from anima_chat import AnimaChat, extract_force_keywords  # noqa: E402

PROMPTS = [
    "안녕! 너는 누구야?",
    "anima 가 뭐야?",
    "오늘 기분 어때?",
    "좋아하는 색이 뭐야?",
    "도와줘",
]

MODES = ["M4_force_include", "M4_soft_force", "greedy"]

OUT_PATH = REPO / "state" / "anima_m4_natural_smoke_2026_05_12.json"


def looks_mechanical(resp: str, keyword: str | None) -> bool:
    """Heuristic: response 가 keyword 로 (어색하게) 끝나면 mechanical."""
    if not keyword:
        return False
    cleaned = resp.strip().rstrip(".!?")
    if cleaned.endswith(keyword):
        return True
    # ends with interrogative-like keyword
    if cleaned.endswith(("누구야", "뭐야", "어때", "어디")):
        return True
    return False


def has_korean(resp: str) -> bool:
    return bool(re.search(r"[가-힣]", resp))


def main() -> None:
    print("=" * 72)
    print("M4 natural smoke — hard vs soft vs greedy")
    print("=" * 72)

    t0 = time.time()
    chat = AnimaChat()
    print(f"[boot] AnimaChat loaded in {time.time() - t0:.1f}s")

    results: dict = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "ckpt": str(getattr(chat, "ckpt_path", "default")),
        "prompts": PROMPTS,
        "modes": MODES,
        "responses": {},
        "summary": {},
    }

    for mode in MODES:
        print(f"\n[mode={mode}]")
        results["responses"][mode] = []
        for p in PROMPTS:
            full = f"사용자: {p} | 도우미: "
            kws = extract_force_keywords(full, max_keywords=1)
            kw = kws[0] if kws else None
            t1 = time.time()
            resp = chat(full, mode=mode, max_new=60)
            dt = time.time() - t1
            mechanical = looks_mechanical(resp, kw)
            korean_ok = has_korean(resp)
            print(f"  prompt: {p!r}")
            print(f"    kw={kw!r} mechanical={mechanical} kor={korean_ok} "
                  f"dt={dt:.1f}s")
            print(f"    resp: {resp!r}")
            results["responses"][mode].append({
                "prompt": p,
                "keyword": kw,
                "response": resp,
                "mechanical": mechanical,
                "has_korean": korean_ok,
                "duration_s": round(dt, 2),
            })

    # summary
    for mode in MODES:
        rows = results["responses"][mode]
        mech = sum(1 for r in rows if r["mechanical"])
        kor = sum(1 for r in rows if r["has_korean"])
        results["summary"][mode] = {
            "n": len(rows),
            "mechanical": mech,
            "korean": kor,
            "natural_pass": len(rows) - mech,
        }
        print(f"[summary] {mode}: natural={len(rows)-mech}/{len(rows)} "
              f"mechanical={mech} korean={kor}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(results, ensure_ascii=False, indent=2))
    print(f"\n[write] {OUT_PATH}")
    print(f"[done] total {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
