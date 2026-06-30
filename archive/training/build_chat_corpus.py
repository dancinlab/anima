#!/usr/bin/env python3
"""build_chat_corpus.py — dialogue-mixed byte corpus for chat-capable rung-0.

GOAL (@L2): 70% wiki + 30% REAL multi-turn dialogue, byte vocab256, clean-license,
NO synthetic RLHF padding (p6). The dialogue is reformatted into the PROVEN
byte-level continuation format ("사용자: <u> | 도우미: <a>") that made the prior
byte chat PASS — this is learned continuation conditioning, NOT a system prompt /
persona / RLHF template (p1·p3·p4·p6 clean).

REAL SOURCES (all local, honest provenance):
  · dialogue (30%): data/corpus.txt — real KO/EN multi-turn A:/B: conversations
    (consciousness / work / daily themes), blank-line-separated. Reformatted A:->
    "사용자:", B:-> "도우미:", turns joined by " | ", one conversation per line.
  · wiki (70%): CORE/testdata/clm_mid_5lang_c4.txt (5-lang aphorisms, en/zh/ru/ja/ko)
    + data/.corpus_cache/.corpus_cache/ko_wiki.txt (Korean wiki prose). Concatenated
    as the factual backbone.

DETERMINISM: no RNG; the 70/30 byte ratio is hit by truncating the wiki backbone to
70/30 * dialogue_bytes (dialogue is the anchor since it is the scarcer, higher-value
bucket). Idempotent on identical sources. Emits CORPUS_CARD fields (byte count, sha256,
provenance, dialogue fraction) to stdout as JSON for the card.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ANIMA = Path("/Users/mini/dancinlab/anima")

DIALOGUE_SRC = ANIMA / "data" / "corpus.txt"
WIKI_5LANG = ANIMA / "CORE" / "testdata" / "clm_mid_5lang_c4.txt"
WIKI_KO = ANIMA / "data" / ".corpus_cache" / ".corpus_cache" / "ko_wiki.txt"


def reformat_dialogue(raw: str) -> str:
    """A:/B: blank-line-separated convos -> '사용자: .. | 도우미: ..' lines.

    Each conversation becomes ONE line; turns joined by ' | '. A: -> 사용자:,
    B: -> 도우미:. Conversations with <2 turns are dropped (not multi-turn).
    """
    out_lines = []
    convo: list[str] = []

    def flush():
        if len(convo) >= 2:
            out_lines.append(" | ".join(convo))
        convo.clear()

    for line in raw.splitlines():
        s = line.strip()
        if not s:
            flush()
            continue
        if s.startswith("A:"):
            convo.append("사용자: " + s[2:].strip())
        elif s.startswith("B:"):
            convo.append("도우미: " + s[2:].strip())
        else:
            # continuation of the previous turn (rare) — append to last turn.
            if convo:
                convo[-1] = convo[-1] + " " + s
    flush()
    return "\n".join(out_lines) + "\n"


def main() -> int:
    out_path = Path(sys.argv[1]) if len(sys.argv) > 1 else ANIMA / "state" / "chat_corpus_mix" / "chat_corpus_mix.txt"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    raw_dialogue = DIALOGUE_SRC.read_text(encoding="utf-8", errors="replace")
    dialogue = reformat_dialogue(raw_dialogue)
    dialogue_bytes = dialogue.encode("utf-8")
    n_convos = dialogue.count("\n")

    # wiki backbone = 5-lang aphorisms + ko_wiki prose, concatenated.
    wiki = WIKI_5LANG.read_text(encoding="utf-8", errors="replace")
    wiki += "\n" + WIKI_KO.read_text(encoding="utf-8", errors="replace")
    wiki_full_bytes = wiki.encode("utf-8")

    # anchor on dialogue (30%): wiki target = dialogue_bytes * 70/30.
    wiki_target = int(len(dialogue_bytes) * 70 / 30)
    if wiki_target <= len(wiki_full_bytes):
        # truncate wiki to target at a UTF-8 char boundary.
        wiki_bytes = wiki_full_bytes[:wiki_target]
        # back up to a valid utf-8 boundary
        while wiki_bytes and (wiki_bytes[-1] & 0xC0) == 0x80:
            wiki_bytes = wiki_bytes[:-1]
    else:
        # not enough wiki: use all of it, then shrink dialogue to hold 30%.
        wiki_bytes = wiki_full_bytes
        dialogue_target = int(len(wiki_bytes) * 30 / 70)
        # truncate dialogue at a line boundary
        dialogue = dialogue[:0] if dialogue_target == 0 else dialogue
        db = dialogue_bytes[:dialogue_target]
        nl = db.rfind(b"\n")
        if nl > 0:
            db = db[: nl + 1]
        dialogue_bytes = db
        n_convos = dialogue_bytes.decode("utf-8", errors="replace").count("\n")

    # PATH-B-1 concat: wiki block first, then dialogue block (DataLoader shuffle
    # recovers interleave; concat is reproducible).
    blob = wiki_bytes + b"\n" + dialogue_bytes
    out_path.write_bytes(blob)

    total = len(blob)
    sha = hashlib.sha256(blob).hexdigest()
    dia_frac = len(dialogue_bytes) / total
    card = {
        "out_path": str(out_path),
        "total_bytes": total,
        "sha256": sha,
        "wiki_bytes": len(wiki_bytes),
        "dialogue_bytes": len(dialogue_bytes),
        "dialogue_fraction": round(dia_frac, 4),
        "wiki_fraction": round(len(wiki_bytes) / total, 4),
        "n_conversations": n_convos,
        "vocab": "byte (256)",
        "sources": {
            "dialogue": str(DIALOGUE_SRC.relative_to(ANIMA)),
            "wiki_5lang": str(WIKI_5LANG.relative_to(ANIMA)),
            "wiki_ko": str(WIKI_KO.relative_to(ANIMA)),
        },
    }
    print(json.dumps(card, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
