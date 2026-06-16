#!/usr/bin/env python3
"""Build UNIVERSE/HYPOTHESES.jsonl — the per-hypothesis index SSOT.

One JSON object per landed card (cards/H_*.md, cards/Hc_*.md) AND per frozen
archive snapshot (archive/hypotheses_snapshots/**/H_*.md). For ids present in the
legacy per-H index table in HYPOTHESES.md, the verbatim tier + 1-line verdict text
from that md row is preserved (c9 — no paraphrase). For every other card/snapshot,
the entry is derived from the card's own YAML frontmatter / first heading.

Each row carries three provenance/relocation columns (2026-06-16 consolidation):
  source   — origin of the scattered hypothesis: "UNIVERSE" (already in cards/),
             "hypotheses/" (active scattered cards, git mv'd into cards/),
             "archive" (frozen-in-place snapshot, card = archive/... path),
             or a domain dir name (e.g. "TENSION-LINK").
  archived — true for archive/hypotheses_snapshots snapshots (frozen-in-place).
  artifacts— list of relocated py/result deliverable paths under state/<slug>/
             (NOT .verdicts/ — those stay as the frozen evidence the card points at).

Keyed by CARD FILE (not id) so c10 dup-id variant cards each keep a row.
Ordered by (numeric id, card filename). Idempotent — re-run regenerates from disk.
"""
import json
import re
import os
import glob

ROOT = os.path.dirname(os.path.abspath(__file__))
CARDS_DIR = os.path.join(ROOT, "cards")
MD = os.path.join(ROOT, "HYPOTHESES.md")
OUT = os.path.join(ROOT, "HYPOTHESES.jsonl")
# repo root (one level above UNIVERSE/) — archive snapshots + state/ live here.
REPO = os.path.dirname(ROOT)
ARCHIVE_DIR = os.path.join(REPO, "archive", "hypotheses_snapshots")
TL_HARNESS = os.path.join(REPO, "state", "tension-link-harness")

# Idempotent regeneration: once HYPOTHESES.md is demoted (its per-H rows removed),
# the verbatim md verdicts survive only in the EXISTING HYPOTHESES.jsonl. Load it
# first so a re-run preserves those verbatim tier/verdict strings (c9) for cards
# that no longer have an md row. New cards still get a frontmatter-derived entry.
prior = {}  # card_basename -> existing jsonl object
if os.path.isfile(OUT):
    for _l in open(OUT, encoding="utf-8"):
        _l = _l.strip()
        if not _l:
            continue
        try:
            _o = json.loads(_l)
        except json.JSONDecodeError:
            continue
        prior[os.path.basename(_o.get("card", ""))] = _o

# ---------------------------------------------------------------------------
# 1. Parse legacy per-H index table rows from HYPOTHESES.md.
#    Row form: | <id> | <title...> | <tier> | [name.md](cards/H_<id>_<slug>.md) |
#    title/tier may contain embedded '|', so: first cell = id, last = card link,
#    second-to-last = tier, the middle joined = title (verbatim 1-line verdict).
# ---------------------------------------------------------------------------
md_rows = {}  # card_basename -> dict(id, tier, title)
row_re = re.compile(r'^\|\s*H_[0-9]')
card_link_re = re.compile(r'\(cards/(H_[^)]+\.md)\)')

with open(MD, encoding="utf-8") as fh:
    for line in fh:
        if not row_re.match(line):
            continue
        links = card_link_re.findall(line)
        if not links:
            continue  # roster/backlog row (no cards/ link), not a per-H index row
        # the TRUE card cell is the LAST cards/ link on the row (the final cell);
        # any earlier links are embedded refs in a malformed/merged row.
        card_base = links[-1]
        cells = [c.strip() for c in line.rstrip("\n").split("|")]
        cells = cells[1:-1]  # drop empties around the outer pipes
        if len(cells) < 4:
            continue
        rid = cells[0].split()[0]
        # card cell = LAST cell holding a cards/ link.
        card_idx = max(i for i, c in enumerate(cells) if "(cards/" in c)
        # Index format is | id | title | tier | card |, but a verdict cell that
        # contains literal '|' splits into several cells. The tier column starts
        # with a tier-emoji; treat the FIRST emoji-led cell after the id as the
        # tier boundary. title = cells before it; tier text = that cell's lead;
        # verdict = the whole tier..card-1 span joined (verbatim, c9).
        tier_emoji = ("🟢", "🟠", "🔴", "🧱", "⚪", "🔵", "⊗", "⬜", "✅", "🟡", "❌")
        tier_idx = None
        for i in range(1, card_idx):
            if cells[i].lstrip().startswith(tier_emoji):
                tier_idx = i
                break
        if tier_idx is None:
            tier_idx = card_idx - 1  # fallback: cell just before the card cell
        # tier = the tier-column cell verbatim (for clean rows this is the whole
        # short tier like '🟢 GREEN ENGINE-NATIVE'; for rows whose verdict text
        # carries embedded '|' it is the leading fragment — the FULL verbatim
        # verdict is preserved in `verdict`, c9 no-paraphrase).
        tier = cells[tier_idx]
        title = " | ".join(cells[1:tier_idx]).strip()
        verdict = " | ".join(cells[tier_idx:card_idx]).strip()
        md_rows[card_base] = {"id": rid, "tier": tier,
                              "title": title, "verdict": verdict}

print(f"[md] parsed {len(md_rows)} per-H index rows from HYPOTHESES.md")

# ---------------------------------------------------------------------------
# 2. Frontmatter parser.
# ---------------------------------------------------------------------------
def parse_card(path):
    fm = {}
    heading = None
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                break
            mm = re.match(r'^([A-Za-z_][\w-]*):\s?(.*)$', lines[i].rstrip("\n"))
            if mm:
                fm[mm.group(1)] = mm.group(2).strip()
    for line in lines:
        if line.startswith("# "):
            heading = line[2:].strip()
            break
    return fm, heading

# ---------------------------------------------------------------------------
# 3. One entry per card file (+ provenance columns).
# ---------------------------------------------------------------------------
def num_id(s):
    m = re.search(r'H_(\d+)', s)
    return int(m.group(1)) if m else 10**9

# Hypotheses' own py/result deliverables, relocated to state/<slug>/ during the
# 2026-06-16 consolidation. Keyed by hypothesis id (H_60xx), the TENSION-LINK arc
# harness scripts moved into state/tension-link-harness/ (the .verdicts/ frozen
# evidence stays in TENSION-LINK/, not here).
tl_artifacts = {}  # id -> [state/... paths]
if os.path.isdir(TL_HARNESS):
    for p in sorted(glob.glob(os.path.join(TL_HARNESS, "*.py"))):
        b = os.path.basename(p)
        m = re.match(r'h(\d{4})', b)
        if not m:
            continue  # discovery_batch_*.py — arc-level, not per-hypothesis
        tl_artifacts.setdefault("H_" + m.group(1), []).append(
            "state/tension-link-harness/" + b)


def card_entry(path, card_rel, *, source, archived):
    """Build one jsonl object for a card/snapshot file (verbatim tier/verdict, c9)."""
    base = os.path.basename(path)
    mfn = re.match(r'^(H[c]?)_([0-9]+[a-z]?)(?:_(.+))?\.md$', base)
    if mfn:
        fid = mfn.group(1) + "_" + mfn.group(2)
        slug = mfn.group(3) or ""
    else:
        fid, slug = base[:-3], ""

    fm, heading = parse_card(path)

    if base in md_rows:
        row = md_rows[base]
        rid, tier, title, verdict = (row["id"], row["tier"],
                                     row["title"], row["verdict"])
    elif card_rel in prior_by_card or base in prior:
        po = prior_by_card.get(card_rel) or prior[base]
        rid = po.get("id", fid)
        tier = po.get("tier", "")
        title = po.get("title", "")
        verdict = po.get("verdict", "")
        if not slug:
            slug = po.get("slug", "")
    else:
        rid = (fm.get("id") or fid).split()[0]
        tier = (fm.get("terminal_tier") or fm.get("tier")
                or fm.get("status_grade") or fm.get("status") or "").strip()
        title = (fm.get("title") or heading or "").strip()
        verdict = (fm.get("verdict") or fm.get("terminal_verdict")
                   or fm.get("status_grade") or tier or title).strip()

    if not slug:
        slug = re.sub(r'^\d+_', '', (fm.get("slug") or "").strip())

    # artifacts: the card's own relocated py/result deliverables (state/<slug>/).
    artifacts = []
    va = (fm.get("verdict_artifact") or "").strip()
    if va.startswith("state/") and os.path.isfile(os.path.join(REPO, va)):
        artifacts.append(va)
    for a in tl_artifacts.get(rid, []):
        if a not in artifacts:
            artifacts.append(a)

    return {
        "id": rid,
        "slug": slug,
        "tier": tier,
        "title": title,
        "card": card_rel,
        "verdict": verdict,
        "source": source,
        "archived": archived,
        "artifacts": artifacts,
    }


# prior jsonl keyed by full card path too (archive cards aren't in cards/).
prior_by_card = {o.get("card"): o for o in prior.values()}

entries = []

# 3a. landed cards in UNIVERSE/cards/ (H_*.md and Hc_*.md). Cards moved here from
#     the scattered ./hypotheses/ dir are tagged source="hypotheses/": the dup-id
#     stage-2-audit variants carry a `_stage2var` filename suffix, and the Hc_*
#     candidate cards were not previously in cards/ at all.
cards = sorted(glob.glob(os.path.join(CARDS_DIR, "H_*.md"))
               + glob.glob(os.path.join(CARDS_DIR, "Hc_*.md")))
for path in cards:
    base = os.path.basename(path)
    if base.endswith("_stage2var.md") or base.startswith("Hc_"):
        source = "hypotheses/"
    else:
        source = "UNIVERSE"
    entries.append(card_entry(path, "cards/" + base,
                              source=source, archived=False))

# 3b. frozen archive snapshots — referenced in-place (NOT moved: 107 intra-archive
#     dup basenames + 193 collide with cards/, moving en masse would destroy the
#     archive's frozen structure). Each gets a row; card = its archive/... path.
arch = sorted(glob.glob(os.path.join(ARCHIVE_DIR, "**", "H_*.md"),
                        recursive=True))
for path in arch:
    card_rel = os.path.relpath(path, REPO)
    entries.append(card_entry(path, card_rel,
                              source="archive", archived=True))

entries.sort(key=lambda e: (num_id(e["id"]), e["card"]))

with open(OUT, "w", encoding="utf-8") as fh:
    for e in entries:
        fh.write(json.dumps(e, ensure_ascii=False) + "\n")

by_src = {}
for e in entries:
    by_src[e["source"]] = by_src.get(e["source"], 0) + 1
n_art = sum(1 for e in entries if e["artifacts"])
print(f"[out] wrote {len(entries)} entries -> {OUT}")
print(f"[chk] cards/ on disk: {len(cards)} · archive snapshots: {len(arch)}")
print(f"[chk] by source: {by_src}")
print(f"[chk] rows with artifacts: {n_art}")
