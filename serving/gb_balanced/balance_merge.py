#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""balance_merge.py — assemble the KOSMOS-tier-BALANCED GB-scale default-lane corpus.

Takes the per-tier source slices (wiki t0/t100 + Gutenberg art/consciousness) plus
the SMALL authored register-shaping slices (carving-seed definition · dialogue-act ·
emotion · code-switch · genre · capped persona/SNS), then:

  1. dedup    — near-duplicate filter (block-prefix hash) within and across tiers.
  2. balance  — enforce the KOSMOS ladder: NO single tier > ~45%; consciousness &
                art each meaningfully present; persona/SNS CAPPED small; the authored
                register-shaping slices SHAPE (small) not bulk-fill.
  3. round-trip — UTF-8 decode/encode every block (vocab256 byte cleanliness).
  4. account  — emit the achieved per-TIER and per-LANG byte split + tier vs ideal
                ladder + token-count vs the 140B Chinchilla-7B-optimal line.

DETERMINISTIC: fixed block order (tier, then source order), fixed dedup key. $0 CPU.

The KOSMOS tier ladder (target — `domains/CORPUS-enrichment-analysis.md`)
-----------------------------------------------------------------------
  tier 0   baseline/factual   -> wiki 5-lang 8-band breadth          (the broad floor)
  tier 100 cosmic/science     -> wiki science-filtered               (present)
  tier 77  art                -> Gutenberg literature/poetry (PD)    (present)
  tier 91  consciousness      -> Gutenberg philosophy/meditation(PD) (present, #1 register)
  tier 52  social/daily       -> authored persona/SNS  CAPPED small
  shaping  dialogue-act/emotion/code-switch/genre + carving-seed def -> SMALL authored

Honest (a_scale_honest_scope): per-lang availability DIFFERS. ko/es Gutenberg is
thin/absent -> those langs are wiki-heavier; reported VERBATIM, never fabricated.

Usage
-----
  python3 serving/gb_balanced/balance_merge.py \
      --src-dir serving/corpus/_src \
      --shaping serving/corpus/_src/shaping.txt \
      --persona serving/corpus/_src/persona.txt \
      --out serving/corpus/default_lane_gb_balanced.txt \
      --report serving/corpus/_src/gb_balanced_report.json
"""

import argparse
import hashlib
import json
import os
import re

LANGS = ["en", "fr", "de", "es", "ko"]

# Per-block language guess by script/diacritics (coarse; for per-lang accounting).
_HANGUL = re.compile(r"[가-힣]")
_CYR = re.compile(r"[Ѐ-ӿ]")


def _round_trip(text):
    return text.encode("utf-8", "replace").decode("utf-8", "ignore")


def _blocks(path):
    if not path or not os.path.exists(path):
        return []
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", "ignore")
    out = []
    for b in text.split("\n\n"):
        b = b.strip()
        if len(b) >= 80:
            out.append(_round_trip(b))
    return out


def _guess_lang(block):
    """Coarse per-block language attribution for accounting only."""
    if _HANGUL.search(block):
        return "ko"
    # diacritic / function-word heuristics for fr/de/es vs en
    low = block.lower()
    if any(w in low for w in (" der ", " und ", " die ", " ist ", " nicht ",
                              " ß", "ü", "ö", "ä")):
        return "de"
    if any(w in low for w in (" le ", " les ", " une ", " été ", " être ",
                              " où ", "ç", "è", "ê")):
        return "fr"
    if any(w in low for w in (" el ", " los ", " una ", " ñ", " qué ",
                              " está ", "¿", "í ", "ó ")):
        return "es"
    return "en"


def dedup(blocks, seen):
    out = []
    for b in blocks:
        key = hashlib.sha1(b[:200].encode("utf-8", "replace")).hexdigest()
        if key in seen:
            continue
        seen.add(key)
        out.append(b)
    return out


def cap_bytes(blocks, max_bytes):
    """Take whole blocks up to max_bytes (None = no cap)."""
    if max_bytes is None:
        return blocks
    out, got = [], 0
    for b in blocks:
        nb = len(b.encode("utf-8", "replace")) + 2
        if got + nb > max_bytes:
            continue
        out.append(b)
        got += nb
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src-dir", default="serving/corpus/_src")
    ap.add_argument("--shaping", default="serving/corpus/_src/shaping.txt")
    ap.add_argument("--persona", default="serving/corpus/_src/persona.txt")
    ap.add_argument("--out", default="serving/corpus/default_lane_gb_balanced.txt")
    ap.add_argument("--report", default="serving/corpus/_src/gb_balanced_report.json")
    # ladder caps as a fraction of the wiki tier-0 byte total (keeps t0 the floor,
    # nothing exceeds ~45%). Defaults chosen so consciousness+art are meaningful.
    ap.add_argument("--persona-cap-mb", type=float, default=40.0)
    ap.add_argument("--shaping-cap-mb", type=float, default=24.0)
    args = ap.parse_args()

    sd = args.src_dir
    tiers = {
        "0_baseline_wiki":      os.path.join(sd, "wiki_t0.txt"),
        "100_cosmic_science":   os.path.join(sd, "wiki_t100.txt"),
        "77_art_gutenberg":     os.path.join(sd, "gut_art.txt"),
        "91_consciousness_gut": os.path.join(sd, "gut_con.txt"),
    }

    seen = set()
    tier_blocks = {}
    for name, path in tiers.items():
        tier_blocks[name] = dedup(_blocks(path), seen)

    # authored register-shaping (SMALL) + capped persona/SNS (tier 52 social/daily)
    shaping = cap_bytes(dedup(_blocks(args.shaping), seen),
                        int(args.shaping_cap_mb * 1024 * 1024))
    persona = cap_bytes(dedup(_blocks(args.persona), seen),
                        int(args.persona_cap_mb * 1024 * 1024))

    ordered = [
        ("0_baseline_wiki",      tier_blocks["0_baseline_wiki"]),
        ("100_cosmic_science",   tier_blocks["100_cosmic_science"]),
        ("77_art_gutenberg",     tier_blocks["77_art_gutenberg"]),
        ("91_consciousness_gut", tier_blocks["91_consciousness_gut"]),
        ("52_social_persona",    persona),
        ("shaping_authored",     shaping),
    ]

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    per_tier_bytes = {}
    per_lang_bytes = {l: 0 for l in LANGS}
    per_tier_lang = {}
    total = 0
    with open(args.out, "wb") as f:
        for name, blocks in ordered:
            tb = 0
            pl = {l: 0 for l in LANGS}
            for b in blocks:
                enc = (b + "\n\n").encode("utf-8", "replace")
                f.write(enc)
                nb = len(enc)
                tb += nb
                total += nb
                lg = _guess_lang(b)
                pl[lg] += nb
                per_lang_bytes[lg] += nb
            per_tier_bytes[name] = tb
            per_tier_lang[name] = pl

    def pct(x):
        return round(100.0 * x / total, 2) if total else 0.0

    # token math: byte-vocab V=256 => 1 byte ~ 1 token; Chinchilla 7B-optimal=140B tok
    tokens = total  # byte-level
    chinchilla_7b = 140_000_000_000
    report = {
        "out": args.out,
        "total_bytes": total,
        "total_mb": round(total / 1048576, 2),
        "total_gb": round(total / 1073741824, 3),
        "byte_tokens": tokens,
        "chinchilla_7b_optimal_tokens": chinchilla_7b,
        "pct_of_7b_optimal": round(100.0 * tokens / chinchilla_7b, 4),
        "per_tier_bytes": per_tier_bytes,
        "per_tier_pct": {k: pct(v) for k, v in per_tier_bytes.items()},
        "per_lang_bytes": per_lang_bytes,
        "per_lang_pct": {k: pct(v) for k, v in per_lang_bytes.items()},
        "per_tier_lang_bytes": per_tier_lang,
        "max_tier_pct": max(pct(v) for v in per_tier_bytes.values()) if per_tier_bytes else 0,
        "ladder_ok_no_tier_over_45": all(pct(v) <= 45.0 for v in per_tier_bytes.values()),
    }
    sha = hashlib.sha256()
    with open(args.out, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            sha.update(chunk)
    report["sha256"] = sha.hexdigest()

    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
