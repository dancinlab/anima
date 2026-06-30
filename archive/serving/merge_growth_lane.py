#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""merge_growth_lane.py — assemble the `lane growth` corpus from its 4 pillars.

Combines:
  (a) science   = serving/corpus/growth_science_5lang.txt   (REAL CC-BY-SA wiki + PD Gutenberg)
  (b,c,d) authored = serving/corpus/growth_authored_5lang.txt (anima-AUTHORED self/hypothesis/dialogue)

into the assembled corpus `serving/corpus/growth_lane.txt` (raw LOCAL/HF-only, NOT
committed) and writes a CORPUS_CARD with the per-pillar + per-lang byte split, sha,
and per-source license. byte-vocab V=256 round-trip asserted on the assembled corpus.

Usage
-----
  python3 serving/merge_growth_lane.py \
      --science serving/corpus/growth_science_5lang.txt \
      --science-meta serving/corpus/growth_science_5lang.meta.jsonl \
      --authored serving/corpus/growth_authored_5lang.txt \
      --authored-meta serving/corpus/growth_authored_5lang.meta.jsonl \
      --out serving/corpus/growth_lane.txt \
      --card serving/corpus/CORPUS_CARD_growth_lane.md
"""

import argparse
import hashlib
import json
import os
from collections import Counter


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _read_meta(path):
    rows = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    rows.append(json.loads(line))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--science", default="serving/corpus/growth_science_5lang.txt")
    ap.add_argument("--science-meta", default="serving/corpus/growth_science_5lang.meta.jsonl")
    ap.add_argument("--authored", default="serving/corpus/growth_authored_5lang.txt")
    ap.add_argument("--authored-meta", default="serving/corpus/growth_authored_5lang.meta.jsonl")
    ap.add_argument("--out", default="serving/corpus/growth_lane.txt")
    ap.add_argument("--card", default="serving/corpus/CORPUS_CARD_growth_lane.md")
    args = ap.parse_args()

    with open(args.science, "rb") as f:
        sci = f.read()
    with open(args.authored, "rb") as f:
        auth = f.read()
    sci_meta = _read_meta(args.science_meta)
    auth_meta = _read_meta(args.authored_meta)

    data = sci + b"\n" + auth
    # byte-vocab V=256 round-trip + sentinel guard.
    assert data.decode("utf-8"), "UTF-8 round-trip failed"
    assert b"\xfe" not in data and b"\xff" not in data, "0xFE/0xFF must be absent"

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "wb") as f:
        f.write(data)

    # per-pillar byte split (a = science, b/c/d = authored pillars)
    pillar_bytes = Counter()
    pillar_bytes["a_science"] += sum(m["bytes"] for m in sci_meta)
    for m in auth_meta:
        pillar_bytes[m["pillar"]] += m["bytes"]

    # per-lang byte split (both sources carry a "lang" key)
    lang_bytes = Counter()
    for m in sci_meta + auth_meta:
        lang_bytes[m["lang"]] += m["bytes"]

    # per-source-license byte split
    lic_bytes = Counter()
    for m in sci_meta:
        lic_bytes[m["license"]] += m["bytes"]
    lic_bytes["anima-authored"] += sum(m["bytes"] for m in auth_meta)

    total = len(data)

    def pct(x):
        return f"{100.0 * x / total:.2f}%" if total else "0%"

    card = []
    card.append("# CORPUS_CARD — lane growth (anima `lane growth` corpus)\n")
    card.append("`lane growth = lane default + growth-register` — the 4th anima self-development")
    card.append("lane. 4 pillars: (a) cross-disciplinary science [REAL CC-BY-SA Wikipedia + PD")
    card.append("Gutenberg] + (b) self-knowledge + (c) UNIVERSE hypotheses + (d) dialogue")
    card.append("[anima-AUTHORED, honest-labeled]. byte-vocab V=256, 5-lang (en/fr/de/es/ko).\n")
    card.append(f"- **assembled corpus**: `{args.out}` (raw LOCAL/HF-only, NOT committed)")
    card.append(f"- **total bytes**: {total} ({total/1048576:.3f} MB)")
    card.append(f"- **sha256 (assembled)**: `{_sha(data)}`")
    card.append(f"- **sha256 (science part)**: `{_sha(sci)}`")
    card.append(f"- **sha256 (authored part)**: `{_sha(auth)}`\n")

    card.append("## per-pillar byte split\n")
    card.append("| pillar | bytes | share | source | license |")
    card.append("|---|---|---|---|---|")
    PILMAP = {
        "a_science":     ("(a) cross-disciplinary science", "Wikipedia + Gutenberg", "CC-BY-SA-4.0 / PUBLIC-DOMAIN"),
        "b_self":        ("(b) anima self-knowledge",       "anima repo docs",       "anima-authored"),
        "c_hypothesis":  ("(c) UNIVERSE hypotheses",        "UNIVERSE/H_*.md distill","anima-authored"),
        "d_dialogue":    ("(d) dialogue format",            "authored deterministic","anima-authored"),
    }
    for key in ["a_science", "b_self", "c_hypothesis", "d_dialogue"]:
        name, src, lic = PILMAP[key]
        card.append(f"| {name} | {pillar_bytes[key]} | {pct(pillar_bytes[key])} | {src} | {lic} |")

    card.append("\n## per-language byte split (a_scale_honest_scope — honest, no fabrication)\n")
    card.append("| lang | bytes | share |")
    card.append("|---|---|---|")
    for lg in ["en", "fr", "de", "es", "ko"]:
        card.append(f"| {lg} | {lang_bytes[lg]} | {pct(lang_bytes[lg])} |")
    card.append("")
    card.append("> Honest per-lang gap: PD Gutenberg primary texts are en-only here (the named")
    card.append("> fr/de translations were not all on-Gutenberg as plain text); ko/es science")
    card.append("> therefore leans on CC-BY-SA Wikipedia `extracts`, which are themselves uneven")
    card.append("> (en articles rich, ko thinner). The authored pillars (b/c/d) ARE 5-lang balanced")
    card.append("> but that is machine-authored COVERAGE, not native collection. NEVER fabricated.")

    card.append("\n## per-source / per-license byte split\n")
    card.append("| source / license | bytes | share |")
    card.append("|---|---|---|")
    for k in sorted(lic_bytes):
        card.append(f"| {k} | {lic_bytes[k]} | {pct(lic_bytes[k])} |")

    card.append("\n## provenance (cite per source)\n")
    card.append("- **(a) Wikipedia** — `<lang>.wikipedia.org/w/api.php?action=query&prop=extracts`,")
    card.append("  named science article titles per language. License **CC-BY-SA-4.0** (Wikipedia text).")
    card.append("  Fields: neuroscience · evolution · information-theory · complexity/SOC ·")
    card.append("  dynamical-systems · thermo-of-computation · neuromorphic-hw · cognitive-science ·")
    card.append("  philosophy-of-mind · consciousness-studies · probability/max-entropy ·")
    card.append("  logic&computation · free-energy · origin-of-life/autopoiesis · self-reference.")
    card.append("- **(a) Gutenberg PD primary texts** — Project Gutenberg, **PUBLIC DOMAIN**, license")
    card.append("  header/footer stripped to the body: Darwin *On the Origin of Species* (pg1228) +")
    card.append("  *The Descent of Man* (pg2300) · Maxwell *Theory of Heat* (pg15491) · James")
    card.append("  *Principles of Psychology, Vol. 1* (pg57628).")
    card.append("- **PD works NOT fetched (recorded gap, NOT fabricated)** — Poincaré *Science and")
    card.append("  Hypothesis* (pg37157) + Boole *Laws of Thought* (pg15114) are PD but ship on")
    card.append("  Gutenberg with NO plain-text format (HTML/scan only); their concepts are instead")
    card.append("  covered by the Wikipedia probability / logic / self-reference titles.")
    card.append("- **(b)(c)(d) anima-authored self-corpus** — authored from the repo's own docs")
    card.append("  (README · CLAUDE.md · CORE/CORE.md · ENGINE+CLM+KOSMOS.md · HEXAD/KOSMOS.md) and")
    card.append("  distilled from real `UNIVERSE/H_*.md` + `hypotheses_candidates/`. Deterministic")
    card.append("  seed 20260605. Teaches anima ABOUT ITSELF + how it reasons — NOT cooperation/")
    card.append("  empathy/restraint templates (p6 held). Anti-register guard asserted: NO")
    card.append("  `[role:|[persona:|[character:|[assistant:|[system:` (grep=0), NO 'you are anima'.")

    card.append("\n## honest invariants (asserted by the generators)\n")
    card.append("- byte-vocab **V=256**, every byte valid UTF-8, **0xFE/0xFF absent** (round-trip OK).")
    card.append("- anti-register tags **grep = 0** · assistant-framing **grep = 0** (authored pillars).")
    card.append("- science = **REAL clean-licensed** (CC-BY-SA / PD, cited); authored = **honest-labeled**.")
    card.append("- **scope (a_scale_honest_scope)**: feeds the PROVEN ~18M chat rung first; **NO 7B")
    card.append("  claim** (default corpus data-starved at 7B, `.verdicts/default-lane-7b/`). The TRAIN")
    card.append("  is a SEPARATE follow-on GPU fire. NO scraped non-licensed data, NO PII.")
    card.append("")

    with open(args.card, "w", encoding="utf-8") as f:
        f.write("\n".join(card))

    print(f"[merge] wrote {args.out} bytes={total} ({total/1048576:.3f} MB)")
    print(f"[merge] sha256={_sha(data)}")
    print(f"[merge] per_pillar={dict(pillar_bytes)}")
    print(f"[merge] per_lang={dict(lang_bytes)}")
    print(f"[merge] per_license={dict(lic_bytes)}")
    print(f"[merge] card -> {args.card}")


if __name__ == "__main__":
    main()
