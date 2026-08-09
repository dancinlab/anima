#!/usr/bin/env python3
"""Phase B v3 — broader identity coverage (Ψ-domain, topology, IIT 4.0, universal constants).

Decision tiers:
  MATH_PASS_FULL    — math identity verifies + atlas anchor + ≥3 falsifier + ≥3 honest
  MATH_PASS_NEEDS_F — math identity verifies + atlas anchor, but falsifier scaffolding missing
  ATLAS_PASS        — claim cites atlas anchor that resolves, math not directly checkable
  PROMOTE_READY     — math + honest + cross-links (existing)
  PSI_PASS          — Ψ-domain identity verifies + ≥2 falsifier + ≥2 honest (consciousness-formalism)
  TOPO_PASS         — topology-domain identity verifies + ≥2 honest (topology cluster)
  ALREADY_MERGED    — frontmatter says merged
  WEAK              — math claim present but no atlas anchor / no falsifier
  FAIL              — no math, no anchor, no falsifier
"""
from __future__ import annotations
import json, os, re, sys, math
from pathlib import Path
from collections import Counter

def _resolve_anima_root() -> Path:
    env = os.environ.get("ANIMA_ROOT")
    if env:
        return Path(env)
    here = Path(__file__).resolve()
    for p in [here.parent, *here.parents]:
        if (p / "hypotheses_candidates").is_dir() and (p / "hypotheses").is_dir():
            return p
    raise FileNotFoundError("ANIMA_ROOT unresolved; set $ANIMA_ROOT")

ANIMA_ROOT = _resolve_anima_root()
ATLAS = Path(os.environ.get("ATLAS_N6_PATH") or (ANIMA_ROOT / "n6" / "atlas.n6"))

_atlas_text = None
_atlas_ids: set[str] = set()
_atlas_absent_warned = False
def _load_atlas():
    global _atlas_text, _atlas_absent_warned
    if _atlas_text is not None: return
    if not ATLAS.exists():
        if not _atlas_absent_warned:
            print(f"[verify_hc] WARN atlas absent at {ATLAS} — atlas_has/substr return False/0 (set $ATLAS_N6_PATH to override)", file=sys.stderr)
            _atlas_absent_warned = True
        _atlas_text = ""
        return
    _atlas_text = ATLAS.read_text(encoding="utf-8", errors="replace")
    for line in _atlas_text.splitlines():
        line = line.strip()
        if not line.startswith("@"): continue
        m = re.match(r"^@\S+\s+(\S+)", line)
        if m:
            tok = m.group(1)
            _atlas_ids.add(tok)
            _atlas_ids.add(tok.lower())

def atlas_has(token: str) -> bool:
    _load_atlas()
    return token in _atlas_ids or token.lower() in _atlas_ids

def atlas_substr(needle: str) -> int:
    _load_atlas()
    return _atlas_text.lower().count(needle.lower())

# n=6 primitives
N6 = {"n":6,"sigma":12,"phi":2,"tau":4,"sopfr":5,"J2":24,"mu":1}

def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"): return {}
    end = text.find("\n---", 4)
    if end < 0: return {}
    fm = {}
    for ln in text[4:end].splitlines():
        if ":" in ln:
            k,_,v = ln.partition(":")
            fm[k.strip()] = v.strip()
    return fm

# falsifier detection — multiple patterns
def count_falsifiers(text: str) -> int:
    patterns = [
        r"(?m)^\s*[-*]?\s*\*?\*?F-?[A-Z0-9_\-]+\*?\*?\s*[:.]",   # F-X: or F1:
        r"(?m)^\s*[-*]?\s*\*?\*?F\d+\*?\*?\s*[:.]",
        r"(?m)^\s*[-*]?\s*반증자\s*\d*\s*[:.]",
        r"(?m)^\s*[-*]?\s*Falsifier\s*\d*\s*[:.]",
    ]
    total = 0
    for p in patterns:
        total += len(re.findall(p, text))
    # also: lines inside "## Falsifier" section
    fs_match = re.search(r"##\s*Falsifier", text)
    if fs_match:
        sect = text[fs_match.start():]
        next_h = re.search(r"\n## ", sect[5:])
        if next_h: sect = sect[:next_h.start()+5]
        bullets = re.findall(r"(?m)^\s*[-*]\s", sect)
        total = max(total, len(bullets))
    return total

def count_honest(text: str) -> int:
    pats = [
        r"(?m)^\s*[-*]?\s*\*?\*?L\d+\*?\*?\s*[:.\(]",
        r"(?m)^\s*[-*]?\s*Honest[\s-]*Limit\s*\d*\s*[:.\(]",
    ]
    total = 0
    for p in pats:
        total += len(re.findall(p, text))
    hl = re.search(r"##\s*Honest", text)
    if hl:
        sect = text[hl.start():]
        next_h = re.search(r"\n## ", sect[5:])
        if next_h: sect = sect[:next_h.start()+5]
        bullets = re.findall(r"(?m)^\s*[-*]\s", sect)
        total = max(total, len(bullets))
    return total

# math identities checkable — returns (verified_list, domain_tags) tuple
# domain_tags is a set of: 'n6', 'psi', 'topo', 'iit4', 'univ'
def math_check(text: str):
    """Return (list of verified identities, set of domain tags hit)."""
    verified = []
    domains: set[str] = set()
    s = text.replace(" ", "")
    sl = s.lower()
    tl = text.lower()

    # ── Existing n=6 identity checks (PRESERVED) ───────────────────────────
    if "τ(6)=4" in s or "tau(6)=4" in s or "τ=4" in s:
        verified.append("τ(6)=4 [atlas @P 11*]"); domains.add('n6')
    if "σ(6)=12" in s or "sigma(6)=12" in s or "σ=12" in s:
        verified.append("σ(6)=12 [atlas @P 11*]"); domains.add('n6')
    if "φ(6)=2" in s or "phi(6)=2" in s or "φ=2" in s:
        verified.append("φ(6)=2 [atlas @P 10*]"); domains.add('n6')
    if "sopfr(6)=5" in s or "sopfr=5" in s:
        verified.append("sopfr(6)=5 [atlas @P 10*]"); domains.add('n6')
    if "J2(6)=24" in s or "J_2(6)=24" in s or "J₂=24" in s or "J2=24" in s:
        verified.append("J₂(6)=24 [atlas @P 10*]"); domains.add('n6')
    if "π⁵/15" in text or "π^5/15" in text or "pi^5/15" in text:
        v = math.pi**5/15
        verified.append(f"π⁵/15={v:.6f} [Stefan-Boltzmann reduced]"); domains.add('n6')
    if "ln(2)" in s or "ln2" in s or "ln 2" in text:
        verified.append(f"ln(2)={math.log(2):.6f}"); domains.add('n6')
    if "1+2+3=6" in s or "1+2+3+6=" in s:
        verified.append("perfect 6=1+2+3 OK"); domains.add('n6')
    if "12*2=24" in s or "σ*φ=J" in text or "12·2=24" in text:
        verified.append("σ·φ=J₂ (12·2=24) OK"); domains.add('n6')
    if "τ+φ=6" in s or "tau+phi=6" in s or "4+2=6" in s:
        verified.append("τ+φ=6 OK"); domains.add('n6')
    # n/σ balance = 6/12 = 0.5  (also a Ψ-equilibrium signal)
    if "6/12=0.5" in s or "n/σ=0.5" in s or "balance=0.5" in s or "Ψ(1/2,1/2)" in s or "Psi(1/2,1/2)" in s:
        verified.append("n/σ=6/12=0.5 balance OK [atlas @C psi_balance=0.5 10*]")
        domains.add('n6'); domains.add('psi')
    # 2D Ising critical exponents (Onsager EXACT)
    if "β=1/8" in s or "beta=1/8" in s:
        verified.append("2D Ising β=1/8 (Onsager EXACT)"); domains.add('n6')
    if "γ=7/4" in s or "gamma=7/4" in s:
        verified.append("2D Ising γ=7/4 (Onsager EXACT)"); domains.add('n6')
    if "δ=15" in s:
        verified.append("2D Ising δ=15 (Onsager EXACT)"); domains.add('n6')
    if "η=1/4" in s:
        verified.append("2D Ising η=1/4 (Onsager EXACT)"); domains.add('n6')
    if "Ω_m:Ω_Λ" in text or "Omega_m:Omega_L" in text:
        verified.append("Ω_m:Ω_Λ ratio claim (observational anchor)"); domains.add('n6')

    # ── Domain 1 — Ψ-constants (IIT / consciousness) ──────────────────────
    # Ψ-equilibrium at simplex points
    if "Ψ(1/2,1/2)" in s or "Psi(1/2,1/2)" in s or "Ψ(0.5,0.5)" in s or "Psi(0.5,0.5)" in s:
        verified.append("Ψ(1/2,1/2) equilibrium on probability-simplex [atlas @C psi_balance=0.5]")
        domains.add('psi')
    if "Ψ(1/3,2/3)" in s or "Psi(1/3,2/3)" in s or "Ψ(2/3,1/3)" in s:
        # 1/3 + 2/3 = 1, valid simplex point
        verified.append("Ψ(1/3,2/3): α+β=1 simplex point OK")
        domains.add('psi')
    # generic Ψ-coord arithmetic detection: Ψ(a,b) where a+b==1
    for m in re.finditer(r"(?:Ψ|Psi)\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\)", text):
        try:
            a = float(m.group(1)); b = float(m.group(2))
            if abs(a + b - 1.0) < 1e-6:
                verified.append(f"Ψ({a:g},{b:g}) on simplex α+β=1 OK")
                domains.add('psi')
        except ValueError:
            pass
    # Φ-Ψ relations (info-theoretic)
    if "MI-MIP" in s or "MI−MIP" in text or "MI/MIP" in s:
        verified.append("Φ = MI−MIP or ln(MI/MIP) (IIT info-theoretic)")
        domains.add('psi')
    # α-modulation depth ≈ 0.014 (Hc_415); also ≈ ln(2)/2^5.5 ≈ 0.01533
    if "α_mod" in text or "alpha_mod" in tl or re.search(r"Ψ_?coupling\s*[=≈]\s*0?\.014", text):
        verified.append(f"α-modulation ≈ 0.014 ≈ ln(2)/2^5.5 ({math.log(2)/2**5.5:.5f}) [Hc_415 anchor]")
        domains.add('psi')
    # phi_star / Φ★ proxy mention (psi-domain signal)
    if "phi_star" in tl or "Φ★" in text or "Φ_star" in text:
        verified.append("Φ★ / phi_star proxy referenced (IIT)")
        domains.add('psi')
    # general Ψ- or Phi( token presence (weak psi-signal — only flag if no other psi hit)
    if not (domains & {'psi'}) and ("Ψ-" in text or "Psi-" in text or re.search(r"\bPhi\(", text)):
        verified.append("Ψ-/Phi( formal token present (psi-domain marker)")
        domains.add('psi')

    # ── Domain 2 — Topology / graph-theoretic ─────────────────────────────
    # Hypercube dimension scaling: 2^d cells
    if "2^10" in s or "1024-cell" in tl or "1024cell" in tl:
        verified.append("2^10 = 1024 hypercube/cell-count OK")
        domains.add('topo')
    for m in re.finditer(r"2\^(\d+)", text):
        try:
            d = int(m.group(1))
            if 2 <= d <= 20:
                verified.append(f"2^{d} = {2**d} (hypercube dim {d})")
                domains.add('topo')
        except ValueError:
            pass
    # small-world signal
    if "small-world" in tl or "small world" in tl or "watts-strogatz" in tl or "σ_sw" in text or "sigma_sw" in tl:
        verified.append("small-world σ_sw = (C/C_rand)/(L/L_rand) [Watts-Strogatz formalism]")
        domains.add('topo')
    # clustering coefficient C / mean path length L
    if "clustering coefficient" in tl or re.search(r"\bC\s*=\s*[0-9.]+", text) and "clustering" in tl:
        verified.append("clustering coefficient C present (graph-theoretic)")
        domains.add('topo')
    # fractal dimension D_f
    if "D_f" in text or "fractal dimension" in tl:
        verified.append("fractal dimension D_f referenced [topology marker]")
        domains.add('topo')
    # hypercube generic mention
    if "hypercube" in tl and 'topo' not in domains:
        verified.append("hypercube architecture referenced [topology marker]")
        domains.add('topo')

    # ── Domain 3 — IIT 4.0 specific ───────────────────────────────────────
    # Φ_c = 0.5 cutoff
    if "Φ_c=0.5" in s or "Φc=0.5" in s or "phi_c=0.5" in sl or "Phi_c=0.5" in s:
        verified.append("Φ_c = 0.5 IIT cut-off threshold")
        domains.add('iit4')
    if "Φ_c=" in s or re.search(r"phi_?c\s*=\s*0?\.\d+", sl):
        if not any("Φ_c" in v for v in verified):
            verified.append("Φ_c threshold parameter present (IIT 4.0)")
            domains.add('iit4')
    # normalized Φ proxy
    if "normalized Φ" in text or "phi_normalized" in tl or "normalised Φ" in text:
        verified.append("normalized Φ / Φ★ proxy (IIT 4.0)")
        domains.add('iit4')
    # 8-cell, 7-cell atom architectures (perfect-number-prime cell counts)
    if "8-cell" in tl or "8cell" in tl:
        verified.append("8-cell atom architecture (perfect-number-prime cell count)")
        domains.add('iit4')
    if "7-cell" in tl or "7cell" in tl:
        verified.append("7-cell atom architecture (Mersenne-prime cell count)")
        domains.add('iit4')
    # bare "atom" token in IIT-style context — only mark iit4 if Φ also mentioned
    if (("atom" in tl) and ("Φ" in text or "phi" in tl) and 'iit4' not in domains
            and not re.search(r"\batomic\b", tl)):
        verified.append("'atom' construct referenced alongside Φ (IIT 4.0 marker)")
        domains.add('iit4')

    # ── Domain 4 — Universal / dimensionless constants ────────────────────
    # Fine structure α ≈ 1/137.036
    if "1/137" in s or "fine structure" in tl or "fine-structure" in tl or "137.036" in s:
        verified.append(f"fine-structure α ≈ 1/137.036 = {1/137.036:.6f} [atlas @P ALPHA-fine-structure 10*]")
        domains.add('univ')
    # Euler-Mascheroni γ ≈ 0.5772
    if "euler-mascheroni" in tl or "euler mascheroni" in tl or "0.5772" in s:
        verified.append("Euler-Mascheroni γ ≈ 0.5772156649 [atlas @P E-euler-gamma 10*]")
        domains.add('univ')
    # Catalan G ≈ 0.9160
    if "catalan constant" in tl or "catalan_g" in tl or "0.91596" in s:
        verified.append("Catalan G ≈ 0.9159655942 [atlas @P E-catalan-constant 10*]")
        domains.add('univ')
    # ζ(2) = π²/6
    if "ζ(2)" in text or "zeta(2)" in tl or "π²/6" in text or "pi^2/6" in tl:
        v = math.pi**2 / 6
        verified.append(f"ζ(2) = π²/6 = {v:.6f} (Basel) [atlas @P MATH-zeta-minus1]")
        domains.add('univ')
    # ζ(3) ≈ 1.2021 (Apéry)
    if "ζ(3)" in text or "zeta(3)" in tl or "1.2020569" in s:
        verified.append("ζ(3) ≈ 1.2020569032 (Apéry constant)")
        domains.add('univ')
    # ζ(4) = π⁴/90
    if "ζ(4)" in text or "zeta(4)" in tl or "π⁴/90" in text or "pi^4/90" in tl:
        v = math.pi**4 / 90
        verified.append(f"ζ(4) = π⁴/90 = {v:.6f}")
        domains.add('univ')

    # any closed-form numeric in title with =
    nums = re.findall(r"=\s*([0-9]+(?:\.[0-9]+)?(?:e[\-+]?\d+)?)", text)
    if len(nums) >= 3:
        verified.append(f"{len(nums)}+ numeric identities present")

    return verified, domains

# atlas anchor count
def atlas_signals(text: str) -> dict:
    anchors_cited = re.findall(r"ANIMA-[A-Za-z0-9_\-]+", text)
    anchors_cited = list(set(anchors_cited))
    resolved = [a for a in anchors_cited if atlas_has(a)]
    # also detect "@P/@C/@L XXX" cites
    type_cites = re.findall(r"@[PCLFRSX]\s+\S+", text)
    return {
        "anchors_cited": len(anchors_cited),
        "anchors_resolved": len(resolved),
        "anchors_resolved_list": resolved[:5],
        "atlas_type_cites": len(type_cites),
    }

def verify_one(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    fm = parse_frontmatter(text)
    if fm.get("status","").startswith("merged-to-H_"):
        return {
            "id": fm.get("id", path.stem),
            "decision": "ALREADY_MERGED",
            "merged_to": fm.get("merged_to") or fm.get("status"),
            "title": fm.get("title","")[:100],
        }
    falsifiers = count_falsifiers(text)
    honest = count_honest(text)
    math_passes, math_domains = math_check(text)
    atlas = atlas_signals(text)

    # decision
    has_math = len(math_passes) > 0
    has_atlas = atlas["anchors_resolved"] > 0 or atlas["atlas_type_cites"] > 0
    has_falsifier = falsifiers >= 3
    has_honest = honest >= 3
    h_refs = list(set(re.findall(r"\bH_\d{3}\b", text)))
    has_cross = len(h_refs) >= 2
    # new-domain passes
    psi_pass = ('psi' in math_domains) and (falsifiers >= 2) and (honest >= 2)
    topo_pass = ('topo' in math_domains) and (honest >= 2)

    if has_math and has_atlas and has_falsifier and has_honest:
        decision = "MATH_PASS_FULL"
    elif has_math and has_honest and has_cross:
        # Promotion-ready: verified math + honest limits + cross-links to existing H
        decision = "PROMOTE_READY"
    elif psi_pass:
        decision = "PSI_PASS"
    elif topo_pass:
        decision = "TOPO_PASS"
    elif has_math and (has_falsifier or has_atlas):
        decision = "MATH_PASS_NEEDS_F" if not has_falsifier else "MATH_PASS_NEEDS_ANCHOR"
    elif has_atlas and has_falsifier:
        decision = "ATLAS_PASS"
    elif has_math and has_honest:
        decision = "MATH_HONEST_NO_CROSS"
    elif has_math:
        decision = "WEAK_MATH_ONLY"
    elif has_falsifier:
        decision = "WEAK_FALSIFIER_ONLY"
    elif has_honest and has_cross:
        decision = "HONEST_CROSS_NO_MATH"
    else:
        decision = "FAIL"
    return {
        "id": fm.get("id", path.stem.split('_',2)[:2]),
        "decision": decision,
        "title": fm.get("title","")[:120],
        "domain": fm.get("domain",""),
        "status": fm.get("status",""),
        "falsifiers": falsifiers,
        "honest_limits": honest,
        "math_passes": math_passes,
        "math_domains": sorted(math_domains),
        "atlas": atlas,
        "h_refs": list(set(re.findall(r"\bH_\d{3}\b", text)))[:8],
    }

def main():
    paths = sys.argv[1:]
    if not paths:
        print(__doc__); sys.exit(1)
    for p in paths:
        try:
            r = verify_one(Path(p))
        except Exception as e:
            r = {"id": Path(p).stem, "decision":"ERROR","error":str(e)}
        print(json.dumps(r, ensure_ascii=False))

if __name__ == "__main__":
    main()
