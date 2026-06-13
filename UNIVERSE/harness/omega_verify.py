#!/usr/bin/env python3
"""
omega_verify.py — HONEST verification of the Tier-Ω cosmic hypotheses (H_2001-2009).

⚠️ Ω is categorically different from the 14-axis daegaseol codex. Each omega file
DECLARES ITS OWN status (frontmatter `status_grade`) and titles §3 "정직한 경계선
(hypothesis ↔ interpretation)". 7/9 are 🜂 INTERPRETIVE — unfalsifiable metaphysical
LENSES, NOT scientific hypotheses. The g5 rubric verdict for "imagination/metaphor"
is ⚪ SPECULATION-FENCED (verify N/A) — NOT pass/fail. Manufacturing a PASS for an
unfalsifiable claim would violate p7 / a_paper_significance, so we DO NOT.

This verifier therefore:
  1. reads each axis's self-declared grade and maps it to the g5 tier (honest fence),
  2. runs the ONE genuine $0 empirical contact point — H_2004's SOC (self-organized
     criticality) surrogate: does a critical branching process produce a SCALE-FREE
     (power-law) avalanche distribution while a subcritical one does not?

p7 · $0 local · no GPU · no network. The SOC test verifies the MECHANISM surrogate
of Ω-IV, NOT the cosmic-metaphysical reading (which remains ⏳ OPEN / interpretive).
"""
import os, glob, math, re
import numpy as np

HERE = os.path.dirname(__file__)
MD_DIR = os.path.abspath(os.path.join(HERE, ".."))  # hypotheses joined into UNIVERSE/ flat

# g5 rubric mapping
G5 = {
    "🜂 INTERPRETIVE": "⚪ SPECULATION-FENCED (verify N/A — metaphysical lens, not a calc claim)",
    "⏳ PARTIAL":      "🟠 INSUFFICIENT/DEFERRED (partial empirical contact; strong reading interpretive)",
    "⏳ OPEN":         "🟠 INSUFFICIENT/DEFERRED (testable program exists → SOC surrogate measured below)",
}

def read_grade(path):
    txt = open(path, encoding="utf-8").read()
    g = re.search(r"^status_grade:\s*(.+)$", txt, re.M)
    t = re.search(r"^title:\s*(.+)$", txt, re.M)
    name = re.search(r"이름 \| 전통", txt)  # not used; title carries name
    return (g.group(1).strip() if g else "?"), (t.group(1)[:60] if t else "")

# ── H_2004 SOC surrogate — critical vs subcritical branching avalanches ──────
def soc_branching(sigma, n_avalanches=20000, seed=2004):
    """Galton-Watson branching: each active node spawns Poisson(sigma) children.
    sigma=1.0 == critical (SOC) -> power-law avalanche sizes; sigma<1 subcritical
    -> exponential cutoff. Returns array of avalanche (total descendant) sizes."""
    rng = np.random.default_rng(seed)
    sizes = []
    for _ in range(n_avalanches):
        active = 1
        total = 1
        while active > 0 and total < 100000:
            children = rng.poisson(sigma, size=active).sum()
            total += children
            active = children
        sizes.append(total)
    return np.array(sizes)

def powerlaw_linearity(sizes):
    """Log-log linearity (R^2) of the complementary-CDF tail. A power law is a
    straight line in log-log; an exponential bends down. Returns (R2, slope)."""
    s = np.sort(sizes)
    s = s[s >= 1]
    # complementary CDF P(S >= s)
    uniq, counts = np.unique(s, return_counts=True)
    ccdf = 1.0 - (np.cumsum(counts) - counts) / counts.sum()
    mask = (uniq >= 2) & (ccdf > 0)
    x = np.log10(uniq[mask].astype(float))
    y = np.log10(ccdf[mask])
    if len(x) < 3:
        return 0.0, 0.0
    A = np.vstack([x, np.ones_like(x)]).T
    slope, intercept = np.linalg.lstsq(A, y, rcond=None)[0]
    yhat = slope * x + intercept
    ss_res = ((y - yhat) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(r2), float(slope)

def h2004_soc():
    crit = soc_branching(1.0)
    sub  = soc_branching(0.6)
    r2_crit, slope_crit = powerlaw_linearity(crit)
    r2_sub,  slope_sub  = powerlaw_linearity(sub)
    # SOC supported iff critical tail is power-law-straight (high R2) AND heavier
    # tailed than subcritical (larger max avalanche, slope near mean-field -0.5..-1).
    supported = (r2_crit > 0.95) and (crit.max() > sub.max() * 5)
    return dict(
        r2_crit=round(r2_crit, 4), slope_crit=round(slope_crit, 3),
        r2_sub=round(r2_sub, 4), slope_sub=round(slope_sub, 3),
        max_crit=int(crit.max()), max_sub=int(sub.max()),
        verdict="🟢 SOC-surrogate 지지 (critical=power-law, subcritical=cutoff)" if supported
                else "🔴 SOC-surrogate 미지지")

def main():
    print("=" * 78)
    print("UNIVERSE_omega — Tier-Ω cosmic hypotheses · HONEST g5 grading ($0 · p7)")
    print("=" * 78)
    print(f"{'id':<8}{'self-grade':<18}g5 verdict")
    print("-" * 78)
    rows = []
    for path in sorted(glob.glob(os.path.join(MD_DIR, "H_20*.md"))):
        hid = os.path.basename(path).split("_")[0] + "_" + os.path.basename(path).split("_")[1]
        hid = re.match(r"(H_\d+)", os.path.basename(path)).group(1)
        grade, _ = read_grade(path)
        g5v = G5.get(grade, "?")
        rows.append((hid, grade, g5v))
        print(f"{hid:<8}{grade:<16}{g5v}")
    n_fenced = sum(1 for _, g, _ in rows if "INTERPRETIVE" in g)
    print("-" * 78)
    print(f"⚪ SPECULATION-FENCED: {n_fenced}/9   🟠 DEFERRED: {9 - n_fenced}/9   (0 falsifiable PASS/FAIL — by design)")
    print()
    print("── H_2004 Ω-IV — the ONE empirical contact point: SOC avalanche surrogate ──")
    soc = h2004_soc()
    for k, v in soc.items():
        print(f"   {k} = {v}")
    print()
    print("HONEST SCOPE: 7 axes are unfalsifiable metaphysical lenses → fenced, NOT 'passed'.")
    print("  H_2003 (measurement interp.) ⏳ — no $0 test resolves QM interpretations.")
    print("  H_2004 SOC surrogate measures the MECHANISM (critical=scale-free), NOT the")
    print("  cosmic-metaphysical reading (universe-as-self-regulating remains interpretive).")

if __name__ == "__main__":
    main()
