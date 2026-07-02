#!/usr/bin/env python3
"""HF exact 코퍼스에서 HEAD-tier 공동출현 실라인 추출 — 개념 공동표현 vs 다의어 충돌 검수용."""
import re
import sys

HEADS = ["consciousness", "tension", "memory", "silence", "dream|engine"]


def rx(alt):
    return re.compile(r"\b(?:%s)\b" % alt, re.IGNORECASE)


def main():
    head_rx = [rx(h) for h in HEADS]
    n = len(HEADS)
    for path in sys.argv[1:]:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f):
                hits = [bool(r.search(line)) for r in head_rx]
                if sum(hits) >= 2:
                    pairs = [HEADS[i] for i in range(n) if hits[i]]
                    print(f"--- {path.split('/')[-2]}:{lineno} [{' + '.join(pairs)}]")
                    print(line.strip()[:400])


if __name__ == "__main__":
    main()
