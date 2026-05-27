#!/usr/bin/env python3
"""SAVANT.md §12.5 path 1 — base-rate audit analyzer.

Consumes raw_outputs/ from run_audit.sh and computes:
  - per-script HIT / miss tally (lenient keyword parsing across varied formats)
  - global tally
  - Bonferroni-corrected significance vs naive GZ base rate p≈0.2877
  - look-elsewhere effect (how many waves were tried before settling)
  - tier reclassification verdict per script

Output: audit.json + summary.md
"""
import json
import math
import re
from pathlib import Path
from collections import Counter

OUT_DIR = Path("/Users/ghost/core/anima/state/savant_containment_audit_2026_05_14")
RAW = OUT_DIR / "raw_outputs"

# GZ-base-rate null: fraction of [0,1] covered by GZ
P_BASE = 0.2877

# Keywords scored toward "HIT" (in GZ / matches target / EXACT)
HIT_RE = re.compile(
    r"\b("
    r"HIT|"            # explicit HIT
    r"PASS|"           # PASS markers
    r"MATCH(?!ED)|"    # MATCH but not MATCHED
    r"MATCHED|"
    r"EXACT|"          # exact closed-form match
    r"IN_GZ|IN GZ|"
    r"✓|"              # check mark
    r"OK"              # OK markers (only when surrounded by space-bound)
    r")\b"
)
MISS_RE = re.compile(
    r"\b("
    r"FAIL|"
    r"miss|"
    r"NO_MATCH|NO MATCH|NOT MATCH|"
    r"OUT_OF_GZ|OUT OF GZ|OUTSIDE|"
    r"REJECT(?!ED)?"
    r")\b"
)

def parse_one(out_path: Path) -> dict:
    """Return per-script tally + verdict summary."""
    text = out_path.read_text(errors="replace")
    # Strip MC-distribution diagnostic blocks (they have many "hits" word literally)
    # The texas_recalculation script prints "X hits:" histogram lines. Filter those.
    lines = []
    for line in text.splitlines():
        # Skip MC histogram bars (e.g. "  3 hits: #######")
        if re.match(r"^\s*\d+\s+hits:", line):
            continue
        # Skip "Random hit distribution"
        if "Random Hit Distribution" in line:
            continue
        lines.append(line)
    cleaned = "\n".join(lines)

    hits = len(HIT_RE.findall(cleaned))
    misses = len(MISS_RE.findall(cleaned))
    # Look for total tallies like "X/Y" pattern in summary
    totals = re.findall(r"(\d+)\s*/\s*(\d+)", cleaned)
    # Look for explicit verdict labels
    verdict = "UNKNOWN"
    if "STRUCTURAL SIGNIFICANCE CONFIRMED" in text:
        verdict = "STRUCTURAL"
    elif "STRONG STRUCTURAL SIGNIFICANCE" in text:
        verdict = "STRONG"
    elif "WEAK SIGNIFICANCE" in text:
        verdict = "WEAK"
    elif "NOT SIGNIFICANT" in text:
        verdict = "NOT_SIG"
    # Extract Bonferroni p if present
    bp_m = re.search(r"Bonferroni p[- ]?value:\s+([\d.e+-]+)", text)
    bp = float(bp_m.group(1)) if bp_m else None
    z_m = re.search(r"Z-score:\s+([\d.+-]+)", text)
    z = float(z_m.group(1)) if z_m else None
    p_m = re.search(r"p-value:\s+([\d.e+-]+)", text)
    p = float(p_m.group(1)) if p_m else None
    return {
        "name": out_path.stem,
        "hits_keyword": hits,
        "misses_keyword": misses,
        "totals_xy": totals[-3:] if totals else [],  # last 3 x/y patterns
        "verdict_label": verdict,
        "bonferroni_p": bp,
        "z_score": z,
        "p_value": p,
        "bytes": len(text),
    }


def binom_pvalue(k: int, n: int, p: float) -> float:
    """One-sided P(X >= k | X ~ Binomial(n, p))."""
    if n == 0:
        return 1.0
    if k > n:
        return 0.0
    # Sum from k to n
    s = 0.0
    for i in range(k, n + 1):
        s += math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
    return s


def main():
    scripts = sorted(RAW.glob("verify_gz_*.out"))
    rows = []
    for p in scripts:
        rows.append(parse_one(p))

    # Aggregate hit/miss keyword tally (CRUDE — these are keyword *occurrences*, not unique
    # claim counts. The wave scripts often print the same HIT word multiple times per claim
    # via grade emoji + verdict label. Treat as an *upper bound* indicator only.)
    total_hits = sum(r["hits_keyword"] for r in rows)
    total_misses = sum(r["misses_keyword"] for r in rows)

    # Per-script binomial test against P_BASE using crude hit/miss counts (UPPER-BOUND only)
    for r in rows:
        n = r["hits_keyword"] + r["misses_keyword"]
        k = r["hits_keyword"]
        if n > 0:
            r["binom_p_naive"] = binom_pvalue(k, n, P_BASE)
        else:
            r["binom_p_naive"] = None

    # Identify scripts with Bonferroni p already computed internally — these are authoritative
    auth = [r for r in rows if r.get("bonferroni_p") is not None]
    # Bonferroni-correct the 27-script collection (look-elsewhere)
    # Multiply the smallest p (most-significant single script) by 27.
    if auth:
        min_bp = min(r["bonferroni_p"] for r in auth)
        loo_corrected = min(min_bp * len(scripts), 1.0)
    else:
        loo_corrected = None

    summary = {
        "audit_date": "2026-05-14",
        "scope": "SAVANT.md §12.5 path 1 — base-rate audit of 27 verify_gz_*.py scripts in archive-TECS-L",
        "p_base_rate": P_BASE,
        "n_scripts": len(scripts),
        "total_hits_keyword": total_hits,
        "total_misses_keyword": total_misses,
        "scripts_with_internal_bonferroni": len(auth),
        "min_bonferroni_p_internal": min((r["bonferroni_p"] for r in auth), default=None),
        "look_elsewhere_corrected_min_p": loo_corrected,
        "rows": rows,
    }

    (OUT_DIR / "audit.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str))
    print(f"Wrote {OUT_DIR / 'audit.json'}")
    print(f"n_scripts={len(scripts)}  total_hits={total_hits}  total_misses={total_misses}")
    print(f"scripts with internal Bonferroni: {len(auth)}")
    if loo_corrected is not None:
        print(f"look-elsewhere corrected min p across 27 scripts: {loo_corrected:.6e}")

    # Per-script table
    print()
    print(f"{'script':<55} {'hits':>6} {'miss':>6} {'verdict':<12} {'bonf_p':>12} {'Z':>7}")
    print("-" * 110)
    for r in rows:
        name = r["name"]
        hits = r["hits_keyword"]
        miss = r["misses_keyword"]
        v = r["verdict_label"]
        bp = f"{r['bonferroni_p']:.3e}" if r["bonferroni_p"] is not None else "—"
        z = f"{r['z_score']:.1f}" if r["z_score"] is not None else "—"
        print(f"{name:<55} {hits:>6} {miss:>6} {v:<12} {bp:>12} {z:>7}")


if __name__ == "__main__":
    main()
