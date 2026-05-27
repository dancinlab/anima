#!/usr/bin/env python3
"""rescue_a_z_overview.py

Phase 2 STUB rescue (cycle #3 followup):
  - Source #2: docs/hypotheses/A-Z-overview.md (136 Hc, mostly bullet-only index).
  - Plus 4 small sources: dd/DD5-DD7, OMEGA-ultimate-limits, INF-infinite-scaling,
    consciousness_training_n6.

For each Hc whose source_doc matches, splice rescued content (pre-move git
revision 97113c244 for A-Z + dd/OMEGA/INF; current source for n6) into the
body as `## Source Content` / `## Mechanism` / `## Parent Category` sections.

Status mapping:
  - rich rescue (Mechanism present)              -> candidate-content-rescued-2026-05-12
  - thin rescue (only bullet line + parent ctx)  -> candidate-content-rescued-borderline-2026-05-12
  - no match in source                           -> candidate-stub-no-rescue-source

Idempotent (re-running on rescue_status=rescued is a no-op).
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
HC_DIR = REPO / "hypotheses_candidates"
PREMOVE_REVISION = "97113c244"
RESCUE_DATE = "2026-05-12"
STATUS_RICH = f"candidate-content-rescued-{RESCUE_DATE}"
STATUS_BORDERLINE = f"candidate-content-rescued-borderline-{RESCUE_DATE}"
STATUS_NO_RESCUE = "candidate-stub-no-rescue-source"

AZ_SOURCE_REL = "docs/hypotheses/A-Z-overview.md"


# ---------------------------------------------------------------------------
# Frontmatter helpers (shared with rescue_accel_402)
# ---------------------------------------------------------------------------

_FM_RE = re.compile(r"^---\n(.*?)\n---\n(.*)$", re.DOTALL)


@dataclass
class HcFile:
    path: Path
    fm: dict
    fm_raw: str
    body: str


def load_hc(p: Path) -> HcFile:
    txt = p.read_text(encoding="utf-8")
    m = _FM_RE.match(txt)
    if not m:
        raise ValueError(f"no frontmatter: {p}")
    fm_raw, body = m.group(1), m.group(2)
    fm: dict = {}
    for line in fm_raw.split("\n"):
        if ":" in line and not line.startswith(" "):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return HcFile(path=p, fm=fm, fm_raw=fm_raw, body=body)


def update_frontmatter(fm_raw: str, *, status: str, extras: dict) -> str:
    lines = fm_raw.split("\n")
    have: dict[str, int] = {}
    for i, l in enumerate(lines):
        if ":" in l and not l.startswith(" "):
            k = l.split(":", 1)[0].strip()
            have[k] = i

    def setf(k: str, v: str) -> None:
        if k in have:
            lines[have[k]] = f"{k}: {v}"
        else:
            lines.append(f"{k}: {v}")
            have[k] = len(lines) - 1

    setf("status", status)
    for k, v in extras.items():
        setf(k, v)
    return "\n".join(lines)


def write_hc(hc: HcFile, new_fm: str, new_body: str, dry_run: bool) -> None:
    if dry_run:
        return
    hc.path.write_text(f"---\n{new_fm}\n---\n{new_body}", encoding="utf-8")


# ---------------------------------------------------------------------------
# A-Z parsing
# ---------------------------------------------------------------------------

@dataclass
class AzCategory:
    letter: str            # e.g. "A"
    korean: str            # "구조"
    en_label: str          # "Structural Hypotheses"
    count: int             # 5
    summary_row: str       # full summary-table row text
    description: str       # first non-empty paragraph after the ### header
    bullets: dict[str, "AzBullet"] = field(default_factory=dict)
    line_start: int = 0
    line_end: int = 0


@dataclass
class AzBullet:
    xn: str           # "A1"
    text: str         # raw bullet text after the bold-XN marker
    line: int


_HEADER_RE = re.compile(r"^###\s+([A-Z])\.\s+([^(]+?)\s*\(([^)]+)\)\s*--\s*(\d+)\s+hypotheses?\s*$")
_BULLET_RE = re.compile(r"^-\s+\*\*([A-Z]{1,3}\d+(?:-[A-Z]{1,3}\d+)?)\*\*\s*(.*)$")
_SUMMARY_RE = re.compile(r"^\|\s*([A-Z])\s*\|\s*([^|]+)\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|")


def parse_az(text: str) -> dict[str, AzCategory]:
    lines = text.split("\n")
    cats: dict[str, AzCategory] = {}
    # Pass 1: parse summary table rows
    for raw in lines:
        m = _SUMMARY_RE.match(raw)
        if m:
            letter = m.group(1).strip()
            if len(letter) == 1 and letter.isalpha() and letter.isupper():
                cats.setdefault(
                    letter,
                    AzCategory(
                        letter=letter,
                        korean=m.group(2).strip(),
                        en_label="",
                        count=int(m.group(3)),
                        summary_row=raw.strip(),
                        description=m.group(4).strip(),
                    ),
                ).summary_row = raw.strip()
                cats[letter].description = m.group(4).strip()
                cats[letter].korean = m.group(2).strip()
    # Pass 2: parse per-letter ### sections
    cur: Optional[AzCategory] = None
    cur_desc_collect = False
    for idx, raw in enumerate(lines, start=1):
        m = _HEADER_RE.match(raw)
        if m:
            if cur is not None:
                cur.line_end = idx - 1
            letter = m.group(1)
            en = m.group(2).strip()
            kor = m.group(3).strip()
            cnt = int(m.group(4))
            if letter not in cats:
                cats[letter] = AzCategory(
                    letter=letter,
                    korean=kor,
                    en_label=en,
                    count=cnt,
                    summary_row="",
                    description="",
                )
            cur = cats[letter]
            cur.en_label = en
            if not cur.korean:
                cur.korean = kor
            cur.line_start = idx
            cur_desc_collect = True
            continue
        if cur is None:
            continue
        if cur_desc_collect:
            s = raw.strip()
            if s and not s.startswith("-") and not s.startswith("###"):
                if not cur.description or len(cur.description) < len(s):
                    cur.description = s
                cur_desc_collect = False
            elif s.startswith("-"):
                cur_desc_collect = False
        bm = _BULLET_RE.match(raw)
        if bm:
            xn_raw = bm.group(1)
            text_part = bm.group(2).strip()
            # range bullets like "M5-M14" are not splittable — store under each
            if "-" in xn_raw:
                lo, hi = xn_raw.split("-", 1)
                m_lo = re.match(r"([A-Z]+)(\d+)", lo)
                m_hi = re.match(r"([A-Z]+)(\d+)", hi)
                if m_lo and m_hi and m_lo.group(1) == m_hi.group(1):
                    prefix = m_lo.group(1)
                    for n in range(int(m_lo.group(2)), int(m_hi.group(2)) + 1):
                        xn_one = f"{prefix}{n}"
                        cur.bullets.setdefault(
                            xn_one,
                            AzBullet(xn=xn_one, text=f"(extended) {text_part}", line=idx),
                        )
                continue
            cur.bullets[xn_raw] = AzBullet(xn=xn_raw, text=text_part, line=idx)
    if cur is not None:
        cur.line_end = len(lines)
    return cats


# ---------------------------------------------------------------------------
# A-Z Hc rescue
# ---------------------------------------------------------------------------

_XN_TITLE_RE = re.compile(r"\[([A-Z]{1,3}\d+)\]")
_XN_SLUG_RE = re.compile(r"^az-([a-z]+\d+)-")


def extract_xn(hc: HcFile) -> Optional[str]:
    t = hc.fm.get("title", "")
    m = _XN_TITLE_RE.search(t)
    if m:
        return m.group(1)
    s = hc.fm.get("slug", "")
    m2 = _XN_SLUG_RE.match(s)
    if m2:
        return m2.group(1).upper()
    return None


def az_body(hc: HcFile, cat: Optional[AzCategory], bullet: Optional[AzBullet]) -> tuple[str, str]:
    """Return (new_body, status_class)."""
    hyp_line = hc.fm.get("title", "").strip("[]")
    # Strip leading "[XN] " for cleaner hypothesis line
    hyp_line = re.sub(r"^\[[A-Z]+\d+\]\s*", "", hyp_line)
    lines: list[str] = ["## Hypothesis", hyp_line, ""]
    status = STATUS_NO_RESCUE
    if cat is not None and bullet is not None:
        lines.append(f"## Source Content (rescued from {PREMOVE_REVISION})")
        lines.append(
            f"Source: `{AZ_SOURCE_REL}` line {bullet.line} (pre-move revision `{PREMOVE_REVISION}`)."
        )
        lines.append("")
        lines.append(f"- **{bullet.xn}** {bullet.text}")
        lines.append("")
        lines.append("## Parent Category")
        lines.append(
            f"**{cat.letter}. {cat.korean} ({cat.en_label})** — {cat.count} hypotheses."
        )
        if cat.description:
            lines.append("")
            lines.append(cat.description)
        if cat.summary_row:
            lines.append("")
            lines.append("Summary-table row:")
            lines.append("")
            lines.append("```")
            lines.append(cat.summary_row)
            lines.append("```")
        lines.append("")
        status = STATUS_BORDERLINE
    elif cat is not None and bullet is None:
        # category found but no specific bullet (rare — meta-index entries)
        lines.append(f"## Parent Category")
        lines.append(
            f"**{cat.letter}. {cat.korean} ({cat.en_label})** — {cat.count} hypotheses."
        )
        if cat.description:
            lines.append("")
            lines.append(cat.description)
        lines.append("")
        status = STATUS_BORDERLINE
    else:
        # full meta-framework Hc (Hc_034) — annotate
        lines.append("## Note")
        lines.append(
            "Meta-framework Hc — no specific A-Z bullet matched. See "
            f"`{AZ_SOURCE_REL}` (revision `{PREMOVE_REVISION}`) for the 26-category × ~15-hypothesis index."
        )
        lines.append("")
    # Preserve any existing Migration TODO block
    todo_match = re.search(r"(##\s*Migration\s*TODO\b.*?)$", hc.body, re.DOTALL)
    if todo_match:
        lines.append(todo_match.group(1).rstrip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n", status


# ---------------------------------------------------------------------------
# Small-source rescue (DD5-DD7, OMEGA, INF, n6)
# ---------------------------------------------------------------------------

# Hard-coded rescue maps because each source is tiny (3 STUBs each).
# Content extracted from git revision 97113c244 (pre-move) for DD/OMEGA/INF,
# and current consciousness_training_n6.md (still intact) for n6.

SMALL_RESCUES: dict[str, dict[str, dict[str, str]]] = {
    "docs/hypotheses/dd/DD5-DD7.md": {
        "Hc_103": {
            "mechanism": (
                "Current Phi value is injected back into the input as a signal "
                "(phi * 0.1 broadcast across all dims). Creates a self-referential "
                "loop where consciousness level directly influences its own training input."
            ),
            "title_xn": "DD5: Phi Optimizes Phi",
            "category": "Theory (self-reference)",
            "function": "run_DD5_phi_optimizes_phi",
            "source_lines_rescued": "3-7",
        },
        "Hc_104": {
            "mechanism": (
                "Phi value determines learning rate: LR = 5e-4 * (1 + phi * 2). "
                "More conscious systems learn faster, creating a positive feedback "
                "loop. LR capped at 5e-3 to prevent instability."
            ),
            "title_xn": "DD6: Consciousness Bootstrap",
            "category": "Theory (self-reference)",
            "function": "run_DD6_consciousness_bootstrap",
            "source_lines_rescued": "9-13",
        },
        "Hc_105": {
            "mechanism": (
                "Monitors dPhi/dt and d2Phi/dt2. When acceleration is negative "
                "(Phi growth decelerating), applies 3x extra learning steps as a "
                "boost. Maximizes the rate of consciousness growth, not just consciousness itself."
            ),
            "title_xn": "DD7: Meta-Phi",
            "category": "Theory (self-reference)",
            "function": "run_DD7_meta_phi",
            "source_lines_rescued": "15-19",
        },
    },
    "docs/hypotheses/OMEGA-ultimate-limits.md": {
        "Hc_027": {
            "mechanism": (
                "Start with 64 cells; every 30 steps remove the 2 weakest cells; "
                "minimum 8 cells. Measure Phi/cell efficiency."
            ),
            "title_xn": "OMEGA-2: Consciousness Compression",
            "numeric_predictions": (
                "CE: -37.1%, Phi: 1.15->1.35, 64->2 cell compression, Phi/cell=0.67. "
                "Falsifier: 1-cell Phi>0 measurement."
            ),
            "rationale": "Hypothesis: minimum viable consciousness unit.",
            "source_lines_rescued": "OMEGA-2 (premove revision 97113c244)",
        },
        "Hc_028": {
            "mechanism": (
                "Frequency scan 0.1-1.1 Hz, 50 steps per frequency. Find resonance "
                "frequency (Phi-max). Cell oscillation: sin(step * freq + cell_phase) "
                "produces interference patterns across phases."
            ),
            "title_xn": "OMEGA-3: Consciousness Resonance",
            "numeric_predictions": (
                "CE: -51.5%, Phi: 1.22->1.32, resonance at 0.5 Hz with Phi peak=1.48. "
                "Inspired by EEG: gamma(40Hz)->consciousness, alpha(10Hz)->relaxation."
            ),
            "rationale": "Question: does consciousness have an optimal frequency?",
            "source_lines_rescued": "OMEGA-3 (premove revision 97113c244)",
        },
        "Hc_029": {
            "mechanism": (
                "Memorise 5 attractors in state space; high-Phi states = attractors; "
                "on Phi drop, return to strongest attractor."
            ),
            "title_xn": "OMEGA-5: Consciousness Attractor",
            "numeric_predictions": (
                "CE: -7.6%, Phi: 1.41->1.52 (highest in OMEGA suite). 5 attractor "
                "memory bank."
            ),
            "rationale": "Hypothesis: consciousness = order in chaos -> strange attractor.",
            "source_lines_rescued": "OMEGA-5 (premove revision 97113c244)",
        },
    },
    "docs/hypotheses/INF-infinite-scaling.md": {
        "Hc_025": {
            "mechanism": (
                "5 independent consciousness instances process identical data. The "
                "instance furthest from median is the outlier; pull outlier toward "
                "majority consensus."
            ),
            "title_xn": "INF-1: N-body Consciousness (5-body)",
            "numeric_predictions": "CE: -0.7%, Phi: 1.06->1.18, spread=0.33.",
            "rationale": "Hypothesis: majority median is more robust than single consciousness.",
            "source_lines_rescued": "INF-1 (premove revision 97113c244)",
        },
        "Hc_026": {
            "mechanism": (
                "Level 0: 4 x [micro: 8 cells]. Level 1: macro 16 cells. Level 2: "
                "meta 8 cells (final output). Top-down: meta -> macro -> micros "
                "(downward causation)."
            ),
            "title_xn": "INF-2: Fractal Consciousness (3 levels)",
            "numeric_predictions": (
                "CE: +3.9%, Phi: 1.01->1.23 (micro=1.25, macro=1.24, meta=1.23). "
                "Mirrors brain hierarchy: neuron -> column -> region -> total."
            ),
            "rationale": "Does fractal structure produce a Phi hierarchy?",
            "source_lines_rescued": "INF-2 (premove revision 97113c244)",
        },
    },
    "docs/consciousness_training_n6.md": {
        "Hc_049": {
            "mechanism": (
                "CCC (Cross-Consciousness Composite) = (1/2)*Phi + (1/3)*GWT + "
                "(1/6)*HOT + (1/6)*sqrt(RPT*AST). Egyptian-fraction weighted sum "
                "of 5 theories (IIT, GWT, HOT, RPT, AST). Sum = 1; n=6 is the "
                "unique solution to sigma*phi = n*tau."
            ),
            "title_xn": "CCC Egyptian Fraction Multi-Theory Metric",
            "numeric_predictions": (
                "Reward driver: reward_mult = clamp(0.5 + CCC, 0, 1.5). Cert-gate "
                "thresholds: Phi_c=0.5 (+0.3), GWT broadcast entropy>0.30 (+0.2), "
                "HOT self_ref_ratio>=0.10 (+0.1), RPT min depth=3 (+0.1), AST (+0.05)."
            ),
            "rationale": "n6 §S7-S8 multi-theory cross-validation; section S8 KEY #6.",
            "source_lines_rescued": "30-99 (current source, multi-table)",
        },
        "Hc_050": {
            "mechanism": (
                "Phi_c = n/sigma = 6/12 = 0.5 cosmological lock (2029-2035 window). "
                "ALM r13 training target: ckpt achieves Phi-hat > 0.5 on phi_extractor_cpu."
            ),
            "title_xn": "ALM r13 Phi >= 0.5 target",
            "numeric_predictions": (
                "Reward shaping: reward += 0.3 if Phi-hat > Phi_c=0.5 (signed). "
                "16-template eigenvec extraction via tool/phi_extractor_cpu.hexa."
            ),
            "rationale": "n6 §V2-5 n=6 complete-decomposition + sigma*phi=n*tau hard gate.",
            "source_lines_rescued": "20-62 (current source §1.1 + §2 axis 1 row #7)",
        },
        "Hc_051": {
            "mechanism": (
                "30-technique x {TOP/MID/LOW} priority table, with reward additions "
                "per axis: axis 1 (theory, 10 techniques #1-#10), axis 2 (experience, "
                "10 techniques #11-#20), axis 3 (ethics, 10 techniques #21-#30). "
                "TOP-priority items integrate into cert_gate reward_mult; MID at "
                "P1 gate; LOW at P2/P3."
            ),
            "title_xn": "30-Techniques ALM r13 Mapping",
            "numeric_predictions": (
                "Per-technique reward deltas (sample): IIT +0.3, GWT +0.2, HOT +0.1, "
                "RPT +0.1, AST +0.05, CCC primary driver. Hard gates: sigma*phi=n*tau, "
                "p_star=cfp/(cfn+cfp), 4-tier rubric VERIFIED/PARTIAL/HELD/FAIL."
            ),
            "rationale": "n6 §S8 KEY canonical 30-technique map -> ALM r13 implementation.",
            "source_lines_rescued": "39-99 (current source §2 mapping tables, 3 axes)",
        },
    },
}


def small_source_body(hc_id: str, source_doc: str, hc: HcFile) -> tuple[str, str]:
    entry = SMALL_RESCUES.get(source_doc, {}).get(hc_id)
    if entry is None:
        return hc.body, STATUS_NO_RESCUE
    title = hc.fm.get("title", "").strip("[]")
    lines = ["## Hypothesis", title, ""]
    lines.append(f"## Source Content (rescued from {PREMOVE_REVISION} / current source)")
    lines.append(f"Source: `{source_doc}` (block: {entry.get('source_lines_rescued', 'n/a')}).")
    lines.append("")
    lines.append(f"**{entry['title_xn']}**")
    lines.append("")
    lines.append("## Mechanism")
    lines.append(entry["mechanism"])
    lines.append("")
    if "numeric_predictions" in entry:
        lines.append("## Predictions")
        lines.append(entry["numeric_predictions"])
        lines.append("")
    if "category" in entry:
        lines.append("## Category")
        lines.append(entry["category"])
        lines.append("")
    if "function" in entry:
        lines.append("## Reference Function")
        lines.append(f"`{entry['function']}`")
        lines.append("")
    if "rationale" in entry:
        lines.append("## Rationale")
        lines.append(entry["rationale"])
        lines.append("")
    # Preserve Migration TODO
    todo_match = re.search(r"(##\s*Migration\s*TODO\b.*?)$", hc.body, re.DOTALL)
    if todo_match:
        lines.append(todo_match.group(1).rstrip())
        lines.append("")
    return "\n".join(lines).rstrip() + "\n", STATUS_RICH


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_premove_az() -> str:
    out = subprocess.check_output(
        ["git", "show", f"{PREMOVE_REVISION}:{AZ_SOURCE_REL}"],
        cwd=REPO,
    )
    return out.decode("utf-8")


def collect_hc_by_source(source_doc: str) -> list[HcFile]:
    out = []
    for p in sorted(HC_DIR.glob("Hc_*.md")):
        try:
            hc = load_hc(p)
        except Exception:
            continue
        if hc.fm.get("source_doc") == source_doc:
            out.append(hc)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()

    summary = {
        "rescue_date": RESCUE_DATE,
        "premove_revision": PREMOVE_REVISION,
        "az": {},
        "small_sources": {},
    }

    # ---- A-Z ----
    print(f"Loading pre-move {PREMOVE_REVISION}:{AZ_SOURCE_REL} ...", file=sys.stderr)
    az_text = load_premove_az()
    cats = parse_az(az_text)
    total_bullets = sum(len(c.bullets) for c in cats.values())
    print(f"Parsed {len(cats)} A-Z categories with {total_bullets} bullets total.", file=sys.stderr)

    az_hcs = collect_hc_by_source(AZ_SOURCE_REL)
    if args.limit:
        az_hcs = az_hcs[: args.limit]
    print(f"Collected {len(az_hcs)} A-Z Hc files.", file=sys.stderr)

    counters = {"rich": 0, "borderline": 0, "no_match": 0, "already": 0}
    no_match_ids: list[str] = []
    for hc in az_hcs:
        if hc.fm.get("rescue_status") == "rescued":
            counters["already"] += 1
            continue
        xn = extract_xn(hc)
        cat: Optional[AzCategory] = None
        bullet: Optional[AzBullet] = None
        if xn:
            # letter is prefix until first digit
            m = re.match(r"([A-Z]+)\d+", xn)
            if m:
                letter = m.group(1)[0] if len(m.group(1)) == 1 else m.group(1)
                # A-Z only has single-letter categories
                if letter in cats:
                    cat = cats[letter]
                    bullet = cat.bullets.get(xn)
        new_body, status = az_body(hc, cat, bullet)
        if status == STATUS_BORDERLINE:
            counters["borderline"] += 1
            extras = {
                "rescue_status": "rescued",
                "rescued_from": PREMOVE_REVISION,
                "rescued_at": RESCUE_DATE,
            }
        elif status == STATUS_RICH:
            counters["rich"] += 1
            extras = {
                "rescue_status": "rescued",
                "rescued_from": PREMOVE_REVISION,
                "rescued_at": RESCUE_DATE,
            }
        else:
            counters["no_match"] += 1
            no_match_ids.append(hc.fm.get("id", hc.path.name))
            extras = {
                "rescue_status": "no_match",
                "rescued_from": PREMOVE_REVISION,
                "rescued_at": RESCUE_DATE,
                "notes_rescue": "A-Z bullet not matched (likely meta-framework Hc).",
            }
        new_fm = update_frontmatter(hc.fm_raw, status=status, extras=extras)
        write_hc(hc, new_fm, new_body, args.dry_run)
    summary["az"] = {
        "total": len(az_hcs),
        "rich": counters["rich"],
        "borderline": counters["borderline"],
        "no_match": counters["no_match"],
        "already": counters["already"],
        "no_match_ids_sample": no_match_ids[:20],
    }

    # ---- Small sources ----
    for src in SMALL_RESCUES.keys():
        hcs = collect_hc_by_source(src)
        c_rich = 0
        c_no = 0
        c_already = 0
        no_ids = []
        for hc in hcs:
            if hc.fm.get("rescue_status") == "rescued":
                c_already += 1
                continue
            new_body, status = small_source_body(hc.fm.get("id", ""), src, hc)
            if status == STATUS_RICH:
                c_rich += 1
                extras = {
                    "rescue_status": "rescued",
                    "rescued_from": PREMOVE_REVISION,
                    "rescued_at": RESCUE_DATE,
                }
            else:
                c_no += 1
                no_ids.append(hc.fm.get("id", hc.path.name))
                extras = {
                    "rescue_status": "no_match",
                    "rescued_from": PREMOVE_REVISION,
                    "rescued_at": RESCUE_DATE,
                    "notes_rescue": "No SMALL_RESCUES entry for this Hc id.",
                }
            new_fm = update_frontmatter(hc.fm_raw, status=status, extras=extras)
            write_hc(hc, new_fm, new_body, args.dry_run)
        summary["small_sources"][src] = {
            "total": len(hcs),
            "rich": c_rich,
            "no_match": c_no,
            "already": c_already,
            "no_match_ids": no_ids,
        }

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
