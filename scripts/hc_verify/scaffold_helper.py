#!/usr/bin/env python3
"""
Cycle #6 scaffolding helper.

Given a candidate-needs-scaffolding Hc, append a per-domain F-list (≥3 falsifiers)
+ L-list (≥3 honest limits) + Cross-Links section, then update frontmatter status
to `candidate-falsifier-ready`.

Usage:
    python3 scaffold_helper.py --dry hypotheses_candidates/Hc_NNN.md
    python3 scaffold_helper.py --apply hypotheses_candidates/Hc_NNN.md \
        --domain topo --falsifiers "F-A,F-B,F-C" --honest "L-A,L-B,L-C" \
        --cross "H_159,H_177,H_153"

For interactive batch use, callers supply F/L bullets via JSON file.
"""

import sys, re, json, pathlib, argparse, datetime

def update_status(text: str, new_status: str) -> str:
    return re.sub(r"^(status: )candidate-needs-scaffolding\s*$",
                  rf"\1{new_status}", text, count=1, flags=re.M)

def append_scaffold(text: str, falsifiers: list, honest: list, cross_links: list,
                    extra_notes: str = "") -> str:
    """Append scaffold sections after existing body."""
    today = datetime.date.today().isoformat()
    f_lines = "\n".join(f"- **{f['id']}**: {f['body']}" for f in falsifiers)
    l_lines = "\n".join(f"- **{l['id']}**: {l['body']}" for l in honest)
    x_lines = "\n".join(f"- {c}" for c in cross_links)
    block = f"""

## Falsifiers (scaffolded cycle #6, {today})

{f_lines}

## Honest Limits (scaffolded cycle #6, {today})

{l_lines}

## Cross-Links (scaffolded cycle #6)

{x_lines}
"""
    if extra_notes:
        block += f"\n## Scaffold Notes\n\n{extra_notes}\n"
    return text.rstrip() + block + "\n"

def process(path: pathlib.Path, falsifiers: list, honest: list, cross_links: list,
            extra_notes: str = "", dry: bool = False):
    text = path.read_text(encoding="utf-8")
    if "candidate-needs-scaffolding" not in text:
        print(f"SKIP (not needs-scaffolding): {path.name}")
        return False
    new_text = update_status(text, "candidate-falsifier-ready")
    new_text = append_scaffold(new_text, falsifiers, honest, cross_links, extra_notes)
    if dry:
        print(f"--- DRY {path.name} ---")
        print(new_text[-2000:])
        return True
    path.write_text(new_text, encoding="utf-8")
    print(f"WROTE: {path.name}")
    return True

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--spec", required=True, help="JSON file with batch spec")
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()
    spec = json.loads(pathlib.Path(args.spec).read_text())
    for entry in spec["candidates"]:
        path = pathlib.Path(entry["path"])
        process(path, entry["falsifiers"], entry["honest"], entry["cross_links"],
                entry.get("notes", ""), dry=args.dry)
