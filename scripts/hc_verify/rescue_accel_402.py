#!/usr/bin/env python3
"""rescue_accel_402.py

Rescue rich content from `docs/hypotheses/accel/acceleration-brainstorm-402.md`
git history (commit 12d05a890) back into the 302 STUB Hc candidates that were
auto-promoted from it on 2026-05-11 (commit 07d74b188), which gutted the source
doc into `<!-- moved to ... -->` placeholders and only carried titles into the
Hc bodies.

Operations:
  1. Parse pre-move source into XN blocks (e.g. B5, I1, Y2, AU8 ...).
  2. For each STUB Hc with source_doc == accel-brainstorm-402.md:
       - Match by source_lines (single line number that lands inside a block).
       - Fallback match by XN extracted from the title prefix `[XN]` or slug.
       - Rewrite body with proper sections (Hypothesis / Source Content /
         Predictions / Falsifier Hints / Rationale).
       - Update frontmatter status -> candidate-content-rescued-2026-05-12 and
         add rescued_from / rescued_at.
  3. Rewrite the live source doc, replacing each `<!-- moved to ... -->`
     comment with its original block (preserving the moved comment as a
     trailer for backlink continuity).
  4. Emit a JSON summary.

Usage:
    python3 scripts/hc_verify/rescue_accel_402.py [--dry-run]

Idempotent: re-running on an already-rescued Hc is a no-op (status check).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

REPO = Path(__file__).resolve().parents[2]
SOURCE_DOC_REL = "docs/hypotheses/accel/acceleration-brainstorm-402.md"
SOURCE_DOC = REPO / SOURCE_DOC_REL
PREMOVE_REVISION = "12d05a890"
RESCUE_DATE = "2026-05-12"
RESCUED_STATUS = f"candidate-content-rescued-{RESCUE_DATE}"
HC_DIR = REPO / "hypotheses_candidates"

# ---------------------------------------------------------------------------
# 1. Parse pre-move source
# ---------------------------------------------------------------------------

@dataclass
class Block:
    xn: str            # e.g. "I1", "Y2", "AU8"
    title: str         # full title text after the colon
    line_start: int    # 1-based inclusive (the `####` line)
    line_end: int      # 1-based inclusive (last content line, before next ####/###/##)
    raw_lines: list[str] = field(default_factory=list)

    @property
    def raw_text(self) -> str:
        return "\n".join(self.raw_lines).rstrip()


_XN_HEADER_RE = re.compile(r"^####\s+([A-Z]{1,3}\d+):\s*(.+?)\s*$")


def load_premove() -> str:
    out = subprocess.check_output(
        ["git", "show", f"{PREMOVE_REVISION}:{SOURCE_DOC_REL}"],
        cwd=REPO,
    )
    return out.decode("utf-8")


def parse_blocks(text: str) -> dict[str, Block]:
    lines = text.split("\n")
    blocks: dict[str, Block] = {}
    # 1-based scan
    current: Optional[Block] = None
    for idx, raw in enumerate(lines, start=1):
        m = _XN_HEADER_RE.match(raw)
        if m:
            if current is not None:
                current.line_end = idx - 1
                # trim trailing empties
                while current.raw_lines and current.raw_lines[-1].strip() == "":
                    current.raw_lines.pop()
                blocks[current.xn] = current
            current = Block(xn=m.group(1), title=m.group(2), line_start=idx, line_end=idx)
            current.raw_lines.append(raw)
            continue
        # End block on the next #### (handled above) or any higher-level heading
        if current is not None and (raw.startswith("### ") or raw.startswith("## ") or raw.startswith("# ")):
            current.line_end = idx - 1
            while current.raw_lines and current.raw_lines[-1].strip() == "":
                current.raw_lines.pop()
            blocks[current.xn] = current
            current = None
            continue
        if current is not None:
            current.raw_lines.append(raw)
    if current is not None:
        current.line_end = len(lines)
        while current.raw_lines and current.raw_lines[-1].strip() == "":
            current.raw_lines.pop()
        blocks[current.xn] = current
    return blocks


# ---------------------------------------------------------------------------
# 2. Match STUB Hc files to blocks
# ---------------------------------------------------------------------------

@dataclass
class HcFile:
    path: Path
    frontmatter: dict
    fm_raw: str        # the raw frontmatter text (between --- markers, no markers)
    body: str          # everything after the closing --- line
    source_lines_int: Optional[int]
    xn_from_title: Optional[str]


_FM_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


def load_hc(p: Path) -> HcFile:
    txt = p.read_text(encoding="utf-8")
    m = _FM_RE.match(txt)
    if not m:
        raise ValueError(f"no frontmatter: {p}")
    fm_raw, body = m.group(1), m.group(2)
    fm: dict = {}
    for line in fm_raw.split("\n"):
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    sl_raw = fm.get("source_lines", "")
    sl_int: Optional[int] = None
    try:
        sl_int = int(sl_raw.split("-")[0].split(",")[0].strip())
    except (ValueError, AttributeError):
        sl_int = None
    title = fm.get("title", "")
    xn_match = re.match(r"\s*\[([A-Z]{1,3}\d+)\]", title)
    xn = xn_match.group(1) if xn_match else None
    # fallback: parse from slug
    if not xn:
        slug = fm.get("slug", "")
        m2 = re.match(r"accel-([a-z]+\d+)", slug)
        if m2:
            xn = m2.group(1).upper()
    return HcFile(
        path=p,
        frontmatter=fm,
        fm_raw=fm_raw,
        body=body,
        source_lines_int=sl_int,
        xn_from_title=xn,
    )


def collect_accel_stubs() -> list[HcFile]:
    out = []
    for p in sorted(HC_DIR.glob("Hc_*_accel_*.md")):
        try:
            hc = load_hc(p)
        except Exception as exc:  # noqa: BLE001
            print(f"WARN: skip {p}: {exc}", file=sys.stderr)
            continue
        if hc.frontmatter.get("source_doc") != SOURCE_DOC_REL:
            continue
        out.append(hc)
    return out


def match_block(hc: HcFile, blocks: dict[str, Block]) -> Optional[Block]:
    # primary: source_lines points exactly at (or inside) a block
    if hc.source_lines_int is not None:
        for b in blocks.values():
            if b.line_start <= hc.source_lines_int <= b.line_end:
                return b
    # fallback: XN from title
    if hc.xn_from_title and hc.xn_from_title in blocks:
        return blocks[hc.xn_from_title]
    return None


# ---------------------------------------------------------------------------
# 3. Derive new body from block
# ---------------------------------------------------------------------------

# Pattern: lines like `- **Description**: ...`
_LABEL_RE = re.compile(r"^-\s+\*\*([A-Za-z][A-Za-z _\-/]+)\*\*\s*:\s*(.*)$")


def extract_fields(block: Block) -> dict[str, list[str]]:
    """Return {label_lower: [content lines...]}. First content line is the
    inline value after the colon; subsequent indented continuation lines (if any)
    are appended."""
    fields: dict[str, list[str]] = {}
    current_label: Optional[str] = None
    # Skip the header (first line)
    for raw in block.raw_lines[1:]:
        m = _LABEL_RE.match(raw)
        if m:
            current_label = m.group(1).strip().lower()
            fields.setdefault(current_label, []).append(m.group(2).strip())
            continue
        # bullet continuation or plain bullet without a bold label
        if current_label is not None and (raw.startswith("  ") or raw.startswith("\t")):
            fields[current_label].append(raw.strip())
        else:
            # Either an unlabelled bullet (- text) or blank
            current_label = None  # break the chain
    return fields


def derive_body(block: Block, current_hypothesis_line: str) -> str:
    """Build the new Hc body sections from a Block."""
    fields = extract_fields(block)
    lines: list[str] = []
    lines.append("## Hypothesis")
    lines.append(current_hypothesis_line.strip())
    lines.append("")

    lines.append(f"## Source Content (rescued from {PREMOVE_REVISION})")
    lines.append(f"Source: `{SOURCE_DOC_REL}` lines {block.line_start}-{block.line_end} (pre-move revision `{PREMOVE_REVISION}`).")
    lines.append("")
    lines.append("```markdown")
    lines.extend(block.raw_lines)
    lines.append("```")
    lines.append("")

    def section(title: str, key_aliases: list[str]) -> None:
        for k in key_aliases:
            if k in fields and fields[k]:
                lines.append(f"## {title}")
                for v in fields[k]:
                    if v:
                        lines.append(f"- {v}")
                lines.append("")
                return

    section("Predictions", ["expected"])
    section("Falsifier Hints", ["falsifier", "vs comparison", "vs", "test", "metric"])
    section("Rationale", ["rationale"])

    # If no labelled fields existed (later sections like Y, Z, AA were bulleted
    # without bold labels), surface the bullets as "Mechanism" so the body is
    # never just the source-quote block.
    if not fields:
        bullets = [l.strip() for l in block.raw_lines[1:] if l.strip().startswith("-")]
        if bullets:
            lines.append("## Mechanism")
            lines.extend(bullets)
            lines.append("")

    # Carry category if it was a labelled field
    if "category" in fields and fields["category"]:
        cat = fields["category"][0]
        lines.append(f"## Category")
        lines.append(cat)
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# 4. Frontmatter rewrite
# ---------------------------------------------------------------------------

def update_frontmatter(fm_raw: str, *, rescued: bool, no_match: bool = False) -> str:
    """Return new frontmatter text (without --- markers).

    - update status -> RESCUED_STATUS (or candidate-rescue-no_match if no_match)
    - add rescued_from, rescued_at, rescue_status fields if missing
    Preserves field order; appends new keys at the end if absent.
    """
    lines = fm_raw.split("\n")
    have: dict[str, int] = {}
    for i, l in enumerate(lines):
        if ":" in l and not l.startswith(" "):
            k = l.split(":", 1)[0].strip()
            have[k] = i

    def set_field(k: str, v: str) -> None:
        if k in have:
            lines[have[k]] = f"{k}: {v}"
        else:
            lines.append(f"{k}: {v}")
            have[k] = len(lines) - 1

    if no_match:
        set_field("rescue_status", "no_match")
        set_field("rescued_from", PREMOVE_REVISION)
        set_field("rescued_at", RESCUE_DATE)
    else:
        set_field("status", RESCUED_STATUS)
        set_field("rescue_status", "rescued")
        set_field("rescued_from", PREMOVE_REVISION)
        set_field("rescued_at", RESCUE_DATE)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 5. Rewrite live source doc
# ---------------------------------------------------------------------------

_MOVED_RE = re.compile(r"^<!--\s*\[Hc_(\d+)\s+([a-z0-9_\-]+)\s+—\s+moved to (hypotheses_candidates/[^\s]+\.md)\s+on\s+([0-9\-]+)\s*\]\s*-->\s*$")


def rebuild_source_doc(blocks: dict[str, Block], hc_xn_index: dict[str, str]) -> int:
    """Replace each `<!-- moved to ... -->` line in the live source doc with
    the original block (if matchable), keeping the original moved-comment as a
    small backlink trailer so the breadcrumb to the Hc file persists.

    Returns the number of comments expanded.
    """
    text = SOURCE_DOC.read_text(encoding="utf-8")
    lines = text.split("\n")
    new_lines: list[str] = []
    expanded = 0
    for ln in lines:
        m = _MOVED_RE.match(ln.strip())
        if m:
            slug = m.group(2)
            hc_id = m.group(1)
            hc_path = m.group(3)
            # Slug starts with "accel-x1-..." → recover XN
            sm = re.match(r"accel-([a-z]+\d+)-", slug)
            xn = sm.group(1).upper() if sm else None
            if xn and xn in blocks:
                block = blocks[xn]
                new_lines.extend(block.raw_lines)
                new_lines.append("")
                new_lines.append(f"<!-- Hc_{hc_id} backlink: {hc_path} -->")
                expanded += 1
            else:
                new_lines.append(ln)
        else:
            new_lines.append(ln)
    SOURCE_DOC.write_text("\n".join(new_lines), encoding="utf-8")
    return expanded


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None, help="process at most N Hc files (debug)")
    args = ap.parse_args()

    print(f"Loading pre-move revision {PREMOVE_REVISION} of {SOURCE_DOC_REL} ...", file=sys.stderr)
    premove_text = load_premove()
    blocks = parse_blocks(premove_text)
    print(f"Parsed {len(blocks)} XN blocks (e.g. {sorted(blocks.keys())[:5]} ... {sorted(blocks.keys())[-3:]})", file=sys.stderr)

    hcs = collect_accel_stubs()
    if args.limit:
        hcs = hcs[: args.limit]
    print(f"Collected {len(hcs)} accel Hc files", file=sys.stderr)

    rescued = 0
    no_match = 0
    already = 0
    block_line_counts: list[int] = []
    examples: list[dict] = []
    no_match_ids: list[str] = []
    rescued_xns: set[str] = set()

    for hc in hcs:
        # Skip if already rescued
        if hc.frontmatter.get("rescue_status") == "rescued":
            already += 1
            continue
        block = match_block(hc, blocks)
        if block is None:
            no_match += 1
            no_match_ids.append(hc.frontmatter.get("id", hc.path.name))
            new_fm = update_frontmatter(hc.fm_raw, rescued=False, no_match=True)
            if not args.dry_run:
                hc.path.write_text(f"---\n{new_fm}\n---\n{hc.body}", encoding="utf-8")
            continue

        # derive new body
        # extract current 1-line Hypothesis if present, else use the title
        m = re.search(r"^##\s*Hypothesis\s*\n([^\n]+)", hc.body, re.MULTILINE)
        if m:
            hyp_line = m.group(1).strip()
        else:
            hyp_line = hc.frontmatter.get("title", "").lstrip("[]") or block.title
        # Default hypothesis line is often just the title — enrich with the
        # Description sentence when available.
        fields = extract_fields(block)
        if "description" in fields and fields["description"]:
            desc = fields["description"][0]
            if hyp_line.lower() in desc.lower() or len(hyp_line) < len(desc):
                hyp_line = f"{block.xn}: {block.title} — {desc}"
        new_body = derive_body(block, hyp_line)
        new_fm = update_frontmatter(hc.fm_raw, rescued=True)
        if not args.dry_run:
            hc.path.write_text(f"---\n{new_fm}\n---\n{new_body}", encoding="utf-8")
        rescued += 1
        block_line_counts.append(block.line_end - block.line_start + 1)
        rescued_xns.add(block.xn)
        if len(examples) < 3:
            examples.append({
                "hc_id": hc.frontmatter.get("id"),
                "title": hc.frontmatter.get("title"),
                "xn": block.xn,
                "source_lines": f"{block.line_start}-{block.line_end}",
                "rescued_chars": len(block.raw_text),
                "preview": block.raw_text[:400],
            })

    # Live source doc restoration
    source_expanded = 0
    if not args.dry_run:
        # We need an xn index to know which blocks have any move-comment
        hc_xn_index = {}
        source_expanded = rebuild_source_doc(blocks, hc_xn_index)

    summary = {
        "premove_revision": PREMOVE_REVISION,
        "blocks_parsed": len(blocks),
        "hc_total": len(hcs),
        "rescued": rescued,
        "no_match": no_match,
        "already_rescued": already,
        "source_doc_comments_expanded": source_expanded,
        "rescued_xn_count": len(rescued_xns),
        "block_line_counts": {
            "n": len(block_line_counts),
            "min": min(block_line_counts) if block_line_counts else None,
            "max": max(block_line_counts) if block_line_counts else None,
            "avg": (sum(block_line_counts) / len(block_line_counts)) if block_line_counts else None,
        },
        "no_match_ids_sample": no_match_ids[:20],
        "examples": examples,
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
