#!/usr/bin/env python3
"""Batch-update Hc frontmatter status based on verify3 results.

Tiers:
  PROMOTE_READY        → status: merged-to-H_NNN (done manually)
  MATH_PASS_NEEDS_ANCHOR → status: candidate-math-verified-falsifier-pending
  WEAK_MATH_ONLY       → status: candidate-math-verified-falsifier-pending
  MATH_HONEST_NO_CROSS → status: candidate-math-verified-cross-pending
  HONEST_CROSS_NO_MATH → status: candidate-structure-verified-math-pending
  WEAK_FALSIFIER_ONLY  → status: candidate-falsifier-only-math-pending
  FAIL                 → no change (preserve existing status)

Also appends a single note line to frontmatter "notes" field with
the verify3 evidence summary.
"""
import json, re, glob, os
from pathlib import Path

ANIMA_ROOT = Path(os.environ.get("ANIMA_ROOT", Path(__file__).resolve().parents[2])).resolve()
ROOT = ANIMA_ROOT / "hypotheses_candidates"
results = []
with open("/tmp/verify3.jsonl") as f:
    for ln in f:
        results.append(json.loads(ln))

TIER_MAP = {
    "MATH_PASS_NEEDS_ANCHOR": "candidate-math-verified-falsifier-pending",
    "WEAK_MATH_ONLY":         "candidate-math-verified-falsifier-pending",
    "MATH_HONEST_NO_CROSS":   "candidate-math-verified-cross-pending",
    "HONEST_CROSS_NO_MATH":   "candidate-structure-verified-math-pending",
    "WEAK_FALSIFIER_ONLY":    "candidate-falsifier-only-math-pending",
}

# Skip if already merged
SKIP_PREFIX = ("merged-to-",)

# Build evidence note
def note_for(r):
    parts = []
    mp = r.get("math_passes",[])
    if mp:
        parts.append(f"verify3 math={len(mp)} ({'; '.join(m.split(' [')[0] for m in mp[:3])}{'...' if len(mp)>3 else ''})")
    if r.get("falsifiers",0):
        parts.append(f"F={r['falsifiers']}")
    if r.get("honest_limits",0):
        parts.append(f"L={r['honest_limits']}")
    a = r.get("atlas",{})
    if a.get("anchors_resolved",0):
        parts.append(f"atlas_resolved={a['anchors_resolved']}")
    return "verify_hc2 2026-05-12 — " + " | ".join(parts)

updated = 0
skipped = 0
for r in results:
    decision = r.get("decision")
    if decision not in TIER_MAP:
        continue
    hc_id = r.get("id")
    if not hc_id or not hc_id.startswith("Hc_"):
        continue
    matches = list(ROOT.glob(f"{hc_id}_*.md"))
    if not matches:
        continue
    p = matches[0]
    text = p.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        skipped += 1; continue
    # find frontmatter close
    end = text.find("\n---", 4)
    if end < 0:
        skipped += 1; continue
    fm_text = text[4:end]
    body = text[end+4:]
    # parse + rewrite status
    new_status = TIER_MAP[decision]
    new_fm_lines = []
    status_seen = False
    notes_idx = -1
    for i, line in enumerate(fm_text.splitlines()):
        if line.startswith("status:"):
            cur = line.split(":",1)[1].strip()
            if cur.startswith(SKIP_PREFIX):
                # don't change merged status
                new_fm_lines.append(line)
                status_seen = True
                continue
            new_fm_lines.append(f"status: {new_status}")
            status_seen = True
        elif line.startswith("notes:"):
            notes_idx = len(new_fm_lines)
            new_fm_lines.append(line)
        else:
            new_fm_lines.append(line)
    if not status_seen:
        skipped += 1; continue
    # add verified_at + math_signal field if not present
    has_verified_at = any(l.startswith("verified_at:") for l in new_fm_lines)
    if not has_verified_at:
        new_fm_lines.append("verified_at: 2026-05-12")
        new_fm_lines.append(f"verify_decision: {decision}")
        new_fm_lines.append(f"verify_note: \"{note_for(r)}\"")
    new_text = "---\n" + "\n".join(new_fm_lines) + "\n---" + body
    p.write_text(new_text, encoding="utf-8")
    updated += 1

print(f"updated={updated} skipped={skipped}")
