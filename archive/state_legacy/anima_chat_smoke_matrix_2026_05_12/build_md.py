"""Build markdown report from results.jsonl.

Run after run_matrix.py completes:
    python3 build_md.py
Outputs:
    ~/core/anima/docs/anima_chat_smoke_matrix_2026_05_12.md
"""

from __future__ import annotations

import json
import os
import statistics
from pathlib import Path

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", "/Users/ghost/core/anima"))
JSONL = ANIMA_ROOT / "state/anima_chat_smoke_matrix_2026_05_12/results.jsonl"
OUT_MD = ANIMA_ROOT / "docs/anima_chat_smoke_matrix_2026_05_12.md"

CKPTS = ["anima-v05", "bprime-prime", "phase1a", "substrate-a"]
MODES = ["M4_force_include", "greedy"]
PROMPTS = [
    "안녕! 너는 누구야?",
    "anima 가 뭐야?",
    "오늘 기분 어때?",
    "좋아하는 색이 뭐야?",
    "도와줘",
]


def load_rows():
    rows = []
    with open(JSONL) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rows.append(json.loads(line))
    return rows


def truncate(s: str | None, n: int = 50) -> str:
    if s is None:
        return "_(none)_"
    s = s.replace("|", "\\|").replace("\n", " ").strip()
    if len(s) > n:
        s = s[:n] + "…"
    return s or "_(empty)_"


def rate_response(resp: str | None) -> tuple[int, int]:
    """Honest heuristic ratings: (naturalness 0-3, informativeness 0-3)."""
    if not resp:
        return 0, 0
    r = resp.strip()
    # naturalness: penalize obvious gibberish patterns
    nat = 3
    if r.count("|") > 5:
        nat -= 2
    if r.count("ㅋ") > 5 or r.count("ㅎ") > 5:
        nat -= 1
    # repeated 2-char patterns
    if len(r) > 10:
        bigrams = [r[i:i+2] for i in range(len(r)-1)]
        if bigrams:
            from collections import Counter
            top = Counter(bigrams).most_common(1)[0][1]
            if top / len(bigrams) > 0.4:
                nat -= 2
    # has korean grammar tail?
    korean_tails = ["다", "요", "어", "야", "지", "네"]
    if any(r.endswith(t) for t in korean_tails):
        nat += 0  # no bonus, baseline
    else:
        nat -= 1
    nat = max(0, min(3, nat))

    # informativeness
    info = 0
    if len(r) >= 5:
        info += 1
    # contains korean
    if any('가' <= c <= '힣' for c in r):
        info += 1
    # contains substantive nouns (length>=2 korean chunks)
    import re
    korean_chunks = re.findall(r'[가-힣]{2,}', r)
    if len(korean_chunks) >= 2:
        info += 1
    info = max(0, min(3, info))
    return nat, info


def main():
    rows = load_rows()
    print(f"loaded {len(rows)} rows")

    # index by (ckpt, mode, prompt)
    idx = {(r["ckpt"], r["mode"], r["prompt"]): r for r in rows}

    lines: list[str] = []
    L = lines.append

    L("# anima chat smoke matrix — 4 ckpt × 2 mode × 5 prompts (40 cells)")
    L("")
    L("**Date**: 2026-05-12  ·  **Hardware**: Mac CPU local  ·  "
      "**Budget**: $0  ·  **Script**: "
      "`state/anima_chat_smoke_matrix_2026_05_12/run_matrix.py`")
    L("")
    L("## 1. 비유 — \"4명의 합창단원이 같은 5곡을 부른다\"")
    L("")
    L("4개 ckpt 는 같은 baseline (engine A/G) 에서 분기한 4명의 합창단원이다. "
      "각자 다른 fine-tune 을 받았고, 오늘 5개의 자연 대화 (사용자 인사·정체성·기분·취향·도움) 를 "
      "M4 (force-include 키워드 주입) 와 greedy 두 가지 발성법으로 부른다. "
      "**누가 가장 자연스러운지** 를 들어보는 audition.")
    L("")
    L("## 2. Concept stack")
    L("")
    L("- 🎤 **anima-v05** = Phase 1A.1 color/cosmology boost (자연 한국어 4/5)")
    L("- 🛠 **bprime-prime** = B'' FFN.gate cotrain (V4-lite 15/15 champion)")
    L("- 🪞 **phase1a** = Phase 1A multi-turn SFT (V5.8 3/5)")
    L("- 🌑 **substrate-a** = Phase 2 cotrain engine A/G (legacy baseline)")
    L("- 🎯 **M4_force_include** = 마지막 ~k 토큰에 추출된 키워드 강제 주입")
    L("- 🎼 **greedy** = argmax (deterministic, 가장 plain)")
    L("")
    L("## 3. Per-prompt 비교 표")
    L("")
    for p in PROMPTS:
        L(f"### Prompt: \"{p}\"")
        L("")
        L("| ckpt | mode | response | elapsed(s) | err |")
        L("|------|------|----------|-----------:|-----|")
        for c in CKPTS:
            for m in MODES:
                row = idx.get((c, m, p))
                if not row:
                    L(f"| {c} | {m} | _(missing)_ | — | — |")
                    continue
                resp = truncate(row.get("response"), 60)
                el = row.get("elapsed_s")
                el_s = f"{el:.1f}" if isinstance(el, (int, float)) else "—"
                err = row.get("error") or ""
                err_s = truncate(err, 25) if err else ""
                L(f"| {c} | {m} | {resp} | {el_s} | {err_s} |")
        L("")

    # ckpt aggregate
    L("## 4. ckpt aggregate — 평균 elapsed + heuristic 평점")
    L("")
    L("| ckpt | mean_elapsed_s | mean_nat (0-3) | mean_info (0-3) | n_ok / n_total |")
    L("|------|--------------:|---------------:|----------------:|---------------:|")
    for c in CKPTS:
        el_vals = []
        nat_vals = []
        info_vals = []
        n_ok = 0
        n_total = 0
        for m in MODES:
            for p in PROMPTS:
                row = idx.get((c, m, p))
                if not row:
                    continue
                n_total += 1
                if row.get("response") is not None and not row.get("error"):
                    n_ok += 1
                    if isinstance(row.get("elapsed_s"), (int, float)):
                        el_vals.append(row["elapsed_s"])
                    nat, info = rate_response(row["response"])
                    nat_vals.append(nat)
                    info_vals.append(info)
        em = statistics.mean(el_vals) if el_vals else 0
        nm = statistics.mean(nat_vals) if nat_vals else 0
        im = statistics.mean(info_vals) if info_vals else 0
        L(f"| {c} | {em:.1f} | {nm:.2f} | {im:.2f} | {n_ok}/{n_total} |")
    L("")

    L("## 5. ASCII rank diagram (naturalness × informativeness)")
    L("")
    L("```")
    L("              info high")
    L("                 ↑")
    L("                 |")
    L("      [어느 모델이 우상단?]")
    L("                 |")
    L("  nat low ←————————→ nat high")
    L("                 |")
    L("                 ↓")
    L("              info low")
    L("```")
    L("")

    L("## 6. Honest rating — 자연 대화 use-case best combo")
    L("")
    L("(자동 heuristic 으로 산정한 best (nat+info) combo 표 — eyeball 확인 필요)")
    L("")
    L("| ckpt | best mode (heuristic) | nat+info sum |")
    L("|------|----------------------|-------------:|")
    for c in CKPTS:
        scores = {}
        for m in MODES:
            sums = []
            for p in PROMPTS:
                row = idx.get((c, m, p))
                if not row or row.get("error") or not row.get("response"):
                    continue
                nat, info = rate_response(row["response"])
                sums.append(nat + info)
            scores[m] = statistics.mean(sums) if sums else 0
        if scores:
            bm = max(scores, key=scores.get)
            L(f"| {c} | {bm} | {scores[bm]:.2f} |")
    L("")

    L("## 7. 추천")
    L("")
    L("- **자연 대화 default**: 위 표에서 nat+info 최고치 combo 채택")
    L("- **mechanical eval**: bprime-prime (V4-lite 15/15) — 단, 자연 대화 자연스러움은 별개")
    L("- **legacy baseline**: substrate-a (sanity ref)")
    L("")

    L("## 8. 다음 진행할 것들")
    L("")
    L("1. Eyeball check — 위 표 본 후 자연스러움 manual 평점 (자동 heuristic 보정) "
      "[cost: 5min · value: high]")
    L("2. anima_chat.py DEFAULT_CKPT 결과 기반 재배치 "
      "[cost: 10min · value: 사용자 체감 high]")
    L("3. Failure-mode taxonomy — gibberish / repetition / off-topic 분류 "
      "[cost: 30min · value: medium]")
    L("4. M3_rep_penalty + sample mode 도 추가 측정 (40 → 80 cells) "
      "[cost: 30min · value: medium]")
    L("5. Multi-turn 매트릭스 — 2-3 turn coherence 측정 "
      "[cost: 1h · value: high (실사용 패턴)]")
    L("")

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT_MD}")


if __name__ == "__main__":
    main()
