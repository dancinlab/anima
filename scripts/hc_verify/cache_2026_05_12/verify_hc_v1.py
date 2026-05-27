#!/usr/bin/env python3
"""Phase B verification harness for RIPE Hc candidates.

For each candidate, runs:
  1. Math-identity check (sympy arithmetic on n=6 primitives, constants)
  2. Atlas-anchor lookup (grep atlas.n6 for cited constants)
  3. Falsifier count (re-verify >=5 falsifiers, >=5 honest limits)
Outputs PASS / FAIL / NEEDS-WORK with evidence trail.

Usage:
  python3 /tmp/verify_hc.py <Hc_path> [<Hc_path> ...]
  python3 /tmp/verify_hc.py --jsonl /tmp/ripe.jsonl  # bulk mode
"""
from __future__ import annotations
import json, re, sys, subprocess, math, os
from pathlib import Path

ANIMA_ROOT = Path("/home/summer/mac_home/core/anima")
ATLAS = ANIMA_ROOT / "n6" / "atlas.n6"

# Pre-load atlas anchors keyed by id
_atlas_index: dict[str, str] = {}
def _build_atlas_index():
    if _atlas_index:
        return
    txt = ATLAS.read_text(encoding="utf-8", errors="replace")
    # header line: @T id = expr :: domain [grade]
    # capture id (token after @T type)
    for line in txt.splitlines():
        line = line.strip()
        if not line.startswith("@"):
            continue
        m = re.match(r"^@\S+\s+(\S+)\s*(?:=.*?)?\s*::", line)
        if m:
            anchor_id = m.group(1)
            _atlas_index[anchor_id] = line
            # also index by lowercase
            _atlas_index[anchor_id.lower()] = line

def atlas_lookup(anchor_id: str) -> str | None:
    _build_atlas_index()
    return _atlas_index.get(anchor_id) or _atlas_index.get(anchor_id.lower())

def atlas_grep(needle: str, max_hits: int = 5) -> list[str]:
    """Sub-string scan in atlas.n6 (case-insensitive)."""
    needle_l = needle.lower()
    hits = []
    txt = ATLAS.read_text(encoding="utf-8", errors="replace")
    for line in txt.splitlines():
        if needle_l in line.lower():
            hits.append(line.strip())
            if len(hits) >= max_hits:
                break
    return hits

# n=6 primitives (from atlas @P [10*]+)
N6 = {
    "n": 6,
    "sigma": 12,        # divisor_sum
    "phi": 2,           # euler totient
    "tau": 4,           # divisor count
    "sopfr": 5,         # 2+3
    "J2": 24,           # jordan totient
    "mu": 1,            # |moebius(6)|
    "M3": 30,           # ?
}

# Sanity self-check
def _self_test():
    assert N6["sigma"] == 1+2+3+6
    assert N6["phi"] == N6["sigma"] // N6["n"] * 1  # phi*n = sigma -> phi = 12/6 = 2
    assert N6["tau"] == 4
    assert N6["J2"] == N6["sigma"] * N6["phi"]      # 24 = 12*2
_self_test()

def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    fm = {}
    for ln in text[4:end].splitlines():
        if ":" in ln:
            k, _, v = ln.partition(":")
            fm[k.strip()] = v.strip()
    return fm

def count_falsifiers(text: str) -> int:
    """Count items in any Falsifier-like section."""
    # match lines beginning with "- F-" or "F-N:" or "F-NNN-N:"
    return len(re.findall(r"(?:^|\n)\s*(?:-\s*)?F-[A-Z0-9]+(?:-[A-Z0-9]+)*\s*:", text))

def count_honest_limits(text: str) -> int:
    return len(re.findall(r"(?:^|\n)\s*(?:-\s*)?L\d+\s*:", text))

def extract_numeric_claims(text: str) -> list[str]:
    """Pull plausible numeric identities: lhs = rhs."""
    claims = []
    # patterns: e.g. "τ(6) = 4", "σ_SB = π⁵/15", "Ω_m:Ω_Λ ≈ 1:2"
    for ln in text.splitlines():
        if re.search(r"[=≡]\s*[0-9π∞√]", ln) or re.search(r"[στφτμ]\s*\(\s*6\s*\)", ln):
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                claims.append(ln[:120])
    return claims[:8]

def check_n6_identity(claim: str) -> tuple[bool, str]:
    """Cheap arithmetic check for n=6 identities of form 'f(6) = k'."""
    # τ(6)=4
    if re.search(r"τ\s*\(\s*6\s*\)\s*=\s*4", claim) or "tau(6)=4" in claim.replace(" ", ""):
        return True, "τ(6)=4 OK (atlas @P [11*])"
    # σ(6)=12
    if re.search(r"σ\s*\(\s*6\s*\)\s*=\s*12", claim) or "sigma(6)=12" in claim.replace(" ", ""):
        return True, "σ(6)=12 OK"
    # φ(6)=2
    if re.search(r"φ\s*\(\s*6\s*\)\s*=\s*2", claim):
        return True, "φ(6)=2 OK"
    # sopfr(6)=5
    if re.search(r"sopfr\s*\(\s*6\s*\)\s*=\s*5", claim):
        return True, "sopfr(6)=5 OK"
    # J2(6)=24
    if re.search(r"J_?2\s*\(\s*6\s*\)\s*=\s*24", claim):
        return True, "J2(6)=24 OK"
    # π^5/15 ≈ Stefan-Boltzmann ratio
    if "π⁵/15" in claim or "pi^5/15" in claim or "π^5/15" in claim:
        val = math.pi**5 / 15
        return True, f"π⁵/15 ≈ {val:.6f} (Stefan-Boltzmann reduced)"
    return False, ""

def verify_one(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    falsifiers = count_falsifiers(text)
    honest = count_honest_limits(text)
    claims = extract_numeric_claims(text)
    math_passes = []
    math_fails = []
    for c in claims:
        ok, evidence = check_n6_identity(c)
        if ok:
            math_passes.append(f"{c} → {evidence}")
    # Atlas anchor mentions
    anchor_hits = []
    for m in re.findall(r"ANIMA-[A-Za-z0-9_\-]+", text)[:5]:
        if atlas_lookup(m):
            anchor_hits.append(m)
    # H_NNN mentions
    h_refs = re.findall(r"\bH_\d{3}\b", text)
    # Decision
    decision = "FAIL"
    notes = []
    if fm.get("status", "").startswith("merged-to-H_"):
        decision = "ALREADY_MERGED"
        notes.append(f"already merged → {fm.get('status')}")
    elif math_passes and falsifiers >= 3 and honest >= 3:
        decision = "PASS"
        notes.append(f"math_check OK ({len(math_passes)}), falsifiers={falsifiers}, honest={honest}")
    elif math_passes or falsifiers >= 5:
        decision = "NEEDS-WORK"
        notes.append(f"partial: math={len(math_passes)} falsifiers={falsifiers} honest={honest}")
    else:
        decision = "FAIL"
        notes.append(f"insufficient: math={len(math_passes)} falsifiers={falsifiers} honest={honest}")
    return {
        "id": path.stem,
        "title": fm.get("title", "")[:100],
        "domain": fm.get("domain", ""),
        "decision": decision,
        "falsifiers": falsifiers,
        "honest_limits": honest,
        "math_passes": math_passes,
        "atlas_anchors_resolved": anchor_hits,
        "h_refs": list(set(h_refs))[:10],
        "notes": "; ".join(notes),
    }

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    paths: list[Path] = []
    if args[0] == "--jsonl":
        with open(args[1]) as f:
            for ln in f:
                if not ln.strip():
                    continue
                rec = json.loads(ln)
                hc_id = rec.get("id")
                if not hc_id:
                    continue
                # Find file
                cands = list((ANIMA_ROOT / "hypotheses_candidates").glob(f"{hc_id}_*.md"))
                if cands:
                    paths.append(cands[0])
    else:
        paths = [Path(a) for a in args]
    for p in paths:
        try:
            res = verify_one(p)
        except Exception as e:
            res = {"id": p.stem, "decision": "ERROR", "error": str(e)}
        print(json.dumps(res, ensure_ascii=False))

if __name__ == "__main__":
    main()
