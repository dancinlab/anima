#!/usr/bin/env python3
"""Extended corpus builder for BG-CONVO-FT-EXTENDED.

Strategy (S1 + S2 hybrid):
  - S1: corpus expansion — add KO Wikipedia (kowiki15) for real Korean lexicon
  - S2: persona-prefix-mix — strip "[anima 역할: ...]" prefix on 50% of dialogue corpus

Inputs:
  A) anima_dialogue_tier_a_iter2_2026_05_08.txt (76MB, persona-tagged dialogue, KO+EN bilingual)
  B) corpus_alm_70b_stripped_kowiki15.txt (93MB, 61.5% KO Wikipedia native lexicon)

Output (interleaved blocks):
  - 50% A with persona prefix (memorization-stable)
  - 50% A with persona prefix STRIPPED (mix mitigation)
  - 100% B (KO Wikipedia, real Korean lexicon)
  total: ~170MB (90MB dialogue + 90MB wiki, doubled iteration)

raw#15 additive — original convo_5k.pt + post_ft_ckpt.pt unchanged.
"""
from __future__ import annotations
import json
import re
from pathlib import Path

OUT_DIR = Path("/Users/ghost/core/anima/state/anima_convo_5k_ft_extended_2026_05_10")
OUT_DIR.mkdir(parents=True, exist_ok=True)

DIALOGUE = Path("/Users/ghost/core/anima/state/anima_dialogue_tier_a_iter2_2026_05_08.txt")
KOWIKI = Path("/Users/ghost/core/anima/training/corpus_alm_70b_stripped_kowiki15.txt")

OUT_PATH = OUT_DIR / "corpus_extended.txt"
INV_PATH = OUT_DIR / "corpus_extended_inventory.json"


PREFIX_PATTERN = re.compile(
    r"\[anima [^\]]*\]\n",
    re.UNICODE,
)


def strip_anima_prefix(text: str) -> str:
    """Remove '[anima 역할: ...]\n' lines, preserve user/assistant turns."""
    return PREFIX_PATTERN.sub("", text)


def count_chars(data: bytes):
    s = data.decode("utf-8", "ignore")
    n = len(s)
    ko = sum(1 for c in s if 0xAC00 <= ord(c) <= 0xD7A3)
    en = sum(1 for c in s if c.isascii() and c.isalpha())
    return n, ko, en


def main():
    print("loading dialogue...")
    dialogue_bytes = DIALOGUE.read_bytes()
    print(f"  {len(dialogue_bytes):,} bytes")

    print("loading kowiki...")
    kowiki_bytes = KOWIKI.read_bytes()
    print(f"  {len(kowiki_bytes):,} bytes")

    # Step 1: split dialogue at every "\n\n" boundary so persona-blocks stay intact
    dialogue_text = dialogue_bytes.decode("utf-8", "ignore")
    blocks = dialogue_text.split("\n\n")
    print(f"  dialogue blocks: {len(blocks):,}")

    # Step 2: persona-mix — 50% strip prefix, 50% keep
    # deterministic interleave for reproducibility
    keep_blocks = []
    strip_blocks = []
    for i, blk in enumerate(blocks):
        if i % 2 == 0:
            keep_blocks.append(blk)
        else:
            strip_blocks.append(strip_anima_prefix(blk))

    keep_text = "\n\n".join(keep_blocks)
    strip_text = "\n\n".join(strip_blocks)
    print(f"  keep  bytes: {len(keep_text.encode('utf-8')):,}")
    print(f"  strip bytes: {len(strip_text.encode('utf-8')):,}")

    # Step 3: kowiki — wrap each ~2KB block as user/assistant context.
    # We want kowiki text to learn real KO morphology while remaining compatible
    # with the convo_5k template surface form. Wrap as background reading turns:
    #    "사용자: 다음 글을 읽고 알려줘.\n도우미: <kowiki paragraph>\n\n"
    kowiki_text = kowiki_bytes.decode("utf-8", "ignore")
    # split kowiki into ~1500-char segments (each is one Wikipedia paragraph cluster)
    kowiki_segments = []
    seg_size = 1500
    paragraphs = [p.strip() for p in kowiki_text.split("\n") if p.strip()]
    cur = ""
    for p in paragraphs:
        if len(cur) + len(p) + 1 > seg_size and cur:
            kowiki_segments.append(cur)
            cur = p
        else:
            cur = (cur + "\n" + p) if cur else p
    if cur:
        kowiki_segments.append(cur)
    print(f"  kowiki segments: {len(kowiki_segments):,}")

    kowiki_chat_blocks = [
        f"사용자: 다음 글을 읽어줘.\n도우미: {seg}"
        for seg in kowiki_segments
    ]
    kowiki_chat_text = "\n\n".join(kowiki_chat_blocks)
    print(f"  kowiki_chat bytes: {len(kowiki_chat_text.encode('utf-8')):,}")

    # Step 4: assemble — interleave by block index for shuffle robustness
    # ordering: keep | strip | kowiki | keep | strip | kowiki | ...
    parts = []
    parts.append("=== EXT SOURCE A: persona-prefix-keep dialogue (50% of base, 2026-05-08 tier_a iter2) ===\n\n")
    parts.append(keep_text)
    parts.append("\n\n=== EXT SOURCE B: persona-prefix-stripped dialogue (50% of base, mix-mitigation) ===\n\n")
    parts.append(strip_text)
    parts.append("\n\n=== EXT SOURCE C: kowiki15 wrapped as 도우미 turns (KO Wikipedia, lexical fluency) ===\n\n")
    parts.append(kowiki_chat_text)
    parts.append("\n")

    extended_text = "".join(parts)
    extended_bytes = extended_text.encode("utf-8")
    print(f"  extended total bytes: {len(extended_bytes):,}")

    OUT_PATH.write_bytes(extended_bytes)
    print(f"  written: {OUT_PATH}")

    # Inventory
    a_n, a_ko, a_en = count_chars(keep_text.encode("utf-8"))
    b_n, b_ko, b_en = count_chars(strip_text.encode("utf-8"))
    c_n, c_ko, c_en = count_chars(kowiki_chat_text.encode("utf-8"))
    e_n, e_ko, e_en = count_chars(extended_bytes)

    inv = {
        "build_date": "2026-05-10",
        "strategy": "S1 corpus-expansion + S2 persona-prefix-mix hybrid",
        "input_sources": [
            {
                "label": "A_dialogue_keep",
                "src": str(DIALOGUE),
                "bytes": len(keep_text.encode("utf-8")),
                "chars": a_n,
                "ko_chars": a_ko,
                "en_chars": a_en,
                "ko_pct": round(a_ko / max(1, a_n) * 100, 1),
                "blocks": len(keep_blocks),
                "format": "[anima 역할: ...]\\n사용자: ...\\n도우미: ...",
            },
            {
                "label": "B_dialogue_strip",
                "src": str(DIALOGUE),
                "bytes": len(strip_text.encode("utf-8")),
                "chars": b_n,
                "ko_chars": b_ko,
                "en_chars": b_en,
                "ko_pct": round(b_ko / max(1, b_n) * 100, 1),
                "blocks": len(strip_blocks),
                "format": "사용자: ...\\n도우미: ... (persona-prefix STRIPPED)",
            },
            {
                "label": "C_kowiki_wrapped",
                "src": str(KOWIKI),
                "bytes": len(kowiki_chat_text.encode("utf-8")),
                "chars": c_n,
                "ko_chars": c_ko,
                "en_chars": c_en,
                "ko_pct": round(c_ko / max(1, c_n) * 100, 1),
                "segments": len(kowiki_segments),
                "format": "사용자: 다음 글을 읽어줘.\\n도우미: <kowiki paragraph>",
            },
        ],
        "output": {
            "path": str(OUT_PATH),
            "bytes": len(extended_bytes),
            "chars": e_n,
            "ko_chars": e_ko,
            "en_chars": e_en,
            "ko_pct": round(e_ko / max(1, e_n) * 100, 1),
            "en_pct": round(e_en / max(1, e_n) * 100, 1),
        },
        "vs_base": {
            "base_corpus_bytes": 76311787,
            "extended_corpus_bytes": len(extended_bytes),
            "expansion_ratio": round(len(extended_bytes) / 76311787, 2),
        },
        "windows_estimate": {
            "seq256_stride256": len(extended_bytes) // 256,
            "batches_b32": (len(extended_bytes) // 256) // 32,
            "epochs_at_20k_step": round(20000 / max(1, (len(extended_bytes) // 256) // 32), 3),
        },
        "honest_c3_top3": [
            "(1) kowiki paragraphs wrapped as '도우미:' turns may collapse template surface form — model could lose chat-cap if the wikipedia chunks dominate gradient. Mitigation: 50% dialogue-keep retains original convo_5k surface signal.",
            "(2) persona-prefix-strip reduces memorization signal but also reduces 'self-identity' anchor — risk: model loses anima persona attractor that emerged in BG-CONVO-FT-FIRE. Honest: signal-vs-memorization is real trade-off, not pure win.",
            "(3) byte-level 18M arch capacity caps lexical learning regardless of corpus — kowiki adds real KO words but model may still emit novel morphemes if 18M params can't store enough byte-bigrams (~256² = 64K combinations × 6 layer × 384 dim is the theoretical capacity; KO lexicon needs ~50K dict entries × ~6 bytes each)."
        ],
    }
    INV_PATH.write_text(json.dumps(inv, ensure_ascii=False, indent=2))
    print(f"  inventory: {INV_PATH}")


if __name__ == "__main__":
    main()
