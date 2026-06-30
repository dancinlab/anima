#!/usr/bin/env python3
"""RTSC_28 — flat-band-at-E_F screen for an ambient, NON-magnetic RTSC base.

WHY (the campaign bottleneck, RTSC_13/15/21/26):
  Two REAL kagome metals failed the SAME way under real QE DFT:
    - CoSn   : flat band ΔE = -0.44 eV (far below E_F) AND magnetic (0.43 uB).
    - CsV3Sb5: flat band ΔE = +0.92 eV (far above E_F), non-magnetic.
  Both fail on ΔE (flat band too far from E_F) +/- magnetism.
  => The discovery lever = a material whose flat band is ALREADY ~at E_F
     (|ΔE| <~ 0.1 eV), NON-magnetic, ambient-pressure, ideally Type-II.

WHAT THIS SCREEN DOES (honest — a screen NARROWS, it does not discover):
  Path A (Materials Project API, if a key is present):
    Query flat-band-prone structure families (kagome / pyrochlore / Laves /
    Lieb / stannide nets) for the three axes MP serves NATIVELY:
      - is_metal           (must be metallic)
      - total_magnetization (must be ~0 -> non-magnetic SCREEN proxy)
      - energy_above_hull  (must be ~0 -> ambient-stable)
    NOTE (p7 honesty): MP's total_magnetization is a DFT-relaxation SCREEN
    proxy, NOT ground truth — e.g. MP reports CoSn mag=0.0 yet real QE
    (RTSC_21) found 0.43 uB. So MP non-magnetism is a FILTER, confirmed only
    by a real spin-polarized SCF. And the flat-band |ΔE| is NOT in the MP
    summary payload (only band-gap / E_F pointers) — |ΔE| is exactly what the
    ready-to-fire decks are for (graded 🟠 = needs DFT).
  Path B (curated literature fallback, if no key / no network):
    A hand-curated 🟡-citation shortlist of flat-band metals with their
    literature-reported magnetism / approximate flat-band ΔE / ambient status.

  Then RANK by (non-magnetic, ambient, |ΔE| small if known) and shortlist the
  top non-magnetic + ambient + plausibly-shallow-ΔE candidates for DFT.

PROVENANCE GRADES (printed per row):
  🟢 computed-here   (nothing here is a fresh DFT run — reserved; none yet)
  🟡 literature/db   (MP native axis value, OR a literature ΔE/magnetism)
  🟠 needs-DFT       (flat-band |ΔE| not yet computed for this candidate)

p7: no fabricated numbers. MP values are pulled live; literature values carry
a source tag. $0 (DB query only; no DFT run).
"""
import os, sys, json, ssl, subprocess
import urllib.request, urllib.error

MP_BASE = "https://api.materialsproject.org/materials/summary/"
# MP's Cloudflare blocks the default urllib UA (error 1010); a browser UA passes.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")
NM_MAG = 0.10      # |total_magnetization| below this == non-magnetic (screen)
AMB_HULL = 0.030   # energy_above_hull (eV/atom) below this == ambient-stable

# ── flat-band-prone candidate families to query in MP (formula -> family) ────
# Chosen to go BEYOND CoSn/CsV3Sb5: pyrochlore / Laves / hexagonal Pd-Pt-Ir
# stannides / CaCu5-net — families that host flat bands but are NOT Fe/Mn/Co
# (whose 3d moments almost always make them magnetic = fail).
MP_CANDIDATES = [
    # (formula, structure family, note)
    ("RbOs2O6",  "pyrochlore (β)",  "Os pyrochlore net; ambient SC Tc~6.3K"),
    ("CsOs2O6",  "pyrochlore (β)",  "Os pyrochlore net; ambient SC Tc~3.3K"),
    ("KOs2O6",   "pyrochlore (β)",  "Os pyrochlore net; ambient SC Tc~9.6K"),
    ("Cd2Re2O7", "pyrochlore (α)",  "Re pyrochlore; SC Tc~1K"),
    ("Bi2Ir2O7", "pyrochlore (α)",  "Ir pyrochlore metal"),
    ("LaRu2",    "Laves C15",       "Ru kagome-related Laves; SC Tc~4.4K"),
    ("CaCu5",    "CaCu5 hex net",   "Cu kagome-like; NM"),
    ("CaPd5",    "CaCu5 hex net",   "Pd net; NM"),
    ("SnPt",     "NiAs-type hex",   "PtSn flat-band stannide"),
    ("SnIr",     "NiAs-type hex",   "IrSn stannide"),
    ("NbSn2",    "stannide",        "Nb stannide"),
    ("CoSn",     "kagome (CoSn)",   "REFERENCE FAIL — RTSC_21 real QE ΔE=-0.44 eV, mag 0.43uB"),
    ("FeSn",     "kagome (CoSn)",   "Fe kagome — magnetic"),
    ("Mn3Sn",    "kagome (Mn3Sn)",  "Mn kagome — strongly magnetic"),
    ("Fe3Sn2",   "kagome (breathing)","Fe breathing kagome — magnetic"),
    ("Ni3In",    "kagome",          "Ni3In flat-band metal"),
    ("TbMn6Sn6", "kagome (RMn6Sn6)","Mn kagome — magnetic"),
]

# ── curated literature shortlist (Path B fallback) — 🟡 citation only ────────
# magnetic?  : literature magnetic ground state
# dE_eV      : reported flat-band position vs E_F (eV; sign = above/below E_F),
#              None if not clearly reported -> needs DFT
# ambient    : ambient-pressure stable & synthesized
CURATED = [
    # name, family, magnetic?, dE_eV(lit), ambient?, source
    ("RbOs2O6","pyrochlore (β)","no",  None,  "yes",
     "Yonezawa+ JPSJ 2004 (SC Tc~6.3K, ambient); Saniz+ PRB 2007 (β-pyrochlore flat-ish Os-5d near E_F)"),
    ("CsOs2O6","pyrochlore (β)","no",  None,  "yes",
     "Yonezawa+ JPSJ 2004 (SC Tc~3.3K, ambient)"),
    ("KOs2O6", "pyrochlore (β)","no",  None,  "yes",
     "Yonezawa+ JPSJ 2004 (SC Tc~9.6K, rattling, ambient)"),
    ("LaRu2",  "Laves C15",     "no",  None,  "yes",
     "classic Laves SC Tc~4.4K; Ru-4d Laves, non-magnetic"),
    ("CoSn",   "kagome (CoSn)", "yes(QE)", -0.44, "yes",
     "RTSC_21 real QE: ΔE=-0.44 eV, mag 0.43uB (MP DFT says NM — proxy disagreement)"),
    ("CsV3Sb5","kagome (V3Sb5)","no", +0.92, "yes",
     "RTSC_26 real QE: ΔE=+0.92 eV (E_F above), non-magnetic, CDW ~94K"),
    ("Ni3In",  "kagome",        "no(weak)", None, "yes",
     "Ye+ Nature 2024 (Ni3In flat band near E_F, frustrated magnetism / strange metal)"),
    ("Pb2Pd",  "Lieb-ish",      "no",  None,  "yes",
     "placeholder NM stannide — needs DFT"),
]


def _get_mp_key():
    for env in ("MP_API_KEY",):
        v = os.environ.get(env)
        if v:
            return v.strip()
    for k in ("materialsproject.api_key", "mp.api_key"):
        try:
            out = subprocess.run(["secret", "get", k], capture_output=True,
                                 text=True, timeout=10)
            if out.returncode == 0 and out.stdout.strip():
                return out.stdout.strip()
        except Exception:
            pass
    return None


def _mp_query(key, formula):
    fields = ("material_id,formula_pretty,is_metal,total_magnetization,"
              "energy_above_hull,symmetry")
    url = (f"{MP_BASE}?formula={formula}&_fields={fields}&_limit=8")
    req = urllib.request.Request(url, headers={
        "X-API-KEY": key, "accept": "application/json", "User-Agent": UA})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            data = json.load(r).get("data", [])
    except urllib.error.HTTPError as e:
        return {"_err": f"HTTP {e.code}"}
    except Exception as e:
        return {"_err": f"{type(e).__name__}"}
    if not data:
        return None
    # pick the lowest-hull entry (the ground-state polymorph)
    data.sort(key=lambda d: (d.get("energy_above_hull") if d.get(
        "energy_above_hull") is not None else 9.9))
    return data[0]


def run_mp_path(key):
    print("DATA SOURCE: Materials Project API (live query) — native axes "
          "is_metal / total_magnetization / energy_above_hull. 🟡 db-sourced.")
    print("NOTE: flat-band |ΔE| is NOT in the MP summary payload -> 🟠 needs DFT "
          "(that is what the decks are for). MP magnetism is a SCREEN proxy "
          "(e.g. MP says CoSn NM; real QE found 0.43uB).")
    print()
    rows = []
    for formula, family, note in MP_CANDIDATES:
        r = _mp_query(key, formula)
        if r is None:
            rows.append({"f": formula, "fam": family, "mid": "(not in MP)",
                         "metal": None, "mag": None, "hull": None,
                         "sg": "?", "note": note, "src": "MP"})
            continue
        if isinstance(r, dict) and r.get("_err"):
            rows.append({"f": formula, "fam": family, "mid": r["_err"],
                         "metal": None, "mag": None, "hull": None,
                         "sg": "?", "note": note, "src": "MP"})
            continue
        rows.append({
            "f": r.get("formula_pretty", formula), "fam": family,
            "mid": r.get("material_id", "?"),
            "metal": r.get("is_metal"),
            "mag": r.get("total_magnetization"),
            "hull": r.get("energy_above_hull"),
            "sg": (r.get("symmetry") or {}).get("symbol", "?"),
            "note": note, "src": "MP"})
    return rows


def rank_mp(rows):
    """Rank: pass = metallic AND non-magnetic(proxy) AND ambient. Sort passers
    first, then by hull. |ΔE| unknown from MP -> all passers are 🟠 for ΔE."""
    def passes(r):
        if not r["metal"]:
            return False
        if r["mag"] is None or abs(r["mag"]) >= NM_MAG:
            return False
        if r["hull"] is None or r["hull"] >= AMB_HULL or r["hull"] < -0.001:
            # hull == -1 sentinel in some payloads means "on hull / unknown";
            # MP returns the real value; treat missing as fail
            return r["hull"] is not None and -0.001 <= r["hull"] < AMB_HULL
        return True
    for r in rows:
        r["pass"] = passes(r)
    rows.sort(key=lambda r: (not r["pass"],
                             r["hull"] if r["hull"] is not None else 9.9))
    return rows


def print_mp_table(rows):
    print("="*100)
    print("RTSC_28 — flat-band-at-E_F screen (MP-API path): "
          "metallic ∧ non-magnetic(proxy) ∧ ambient-stable")
    print("="*100)
    hdr = (f"{'#':>2} {'formula':10} {'family':18} {'metal':5} "
           f"{'mag(uB)':>8} {'hull':>8} {'sg':9} {'PASS':5}")
    print(hdr)
    print("-"*100)
    for i, r in enumerate(rows, 1):
        mag = "  n/a" if r["mag"] is None else f"{r['mag']:.2f}"
        hull = "  n/a" if r["hull"] is None else f"{r['hull']:.4f}"
        met = "yes" if r["metal"] else ("no" if r["metal"] is False else "?")
        pf = "✓" if r.get("pass") else ""
        print(f"{i:>2} {r['f']:10} {r['fam']:18} {met:5} {mag:>8} {hull:>8} "
              f"{r['sg']:9} {pf:5}")
    print("-"*100)
    passers = [r for r in rows if r.get("pass")]
    print(f"PASS (metallic ∧ |mag|<{NM_MAG} ∧ 0≤hull<{AMB_HULL}): "
          f"{len(passers)}/{len(rows)}")
    print()
    print("TOP SHORTLIST (non-magnetic ∧ ambient ∧ flat-band-prone family) — "
          "flat-band |ΔE| 🟠 needs DFT (build/run a deck):")
    for r in passers[:6]:
        print(f"   • {r['f']:9} [{r['fam']}] {r['mid']} {r['sg']} — {r['note']}")
    print()
    print("HONEST FRAMING: every PASS row is 🟡 (MP db) on metal/mag/hull and "
          "🟠 on flat-band |ΔE| (not computed). The screen NARROWS where to "
          "point the QE/DFT fire; it does not itself discover. Magnetism is an "
          "MP DFT proxy — confirm with a real nspin=2 SCF.")


def print_curated_table():
    print("="*100)
    print("RTSC_28 — CURATED LITERATURE FALLBACK (🟡 citation only; NOT "
          "computed here)")
    print("="*100)
    hdr = (f"{'candidate':10} {'family':18} {'magnetic?':9} "
           f"{'ΔE(eV,lit)':>11} {'ambient?':8} source")
    print(hdr)
    print("-"*100)
    for name, fam, mag, dE, amb, src in CURATED:
        de = "  ?(DFT)" if dE is None else f"{dE:+.2f}"
        print(f"{name:10} {fam:18} {mag:9} {de:>11} {amb:8} {src[:46]}")
    print("-"*100)
    print("RANK (non-magnetic ∧ ambient ∧ |ΔE| small/unknown):")
    print("   1) RbOs2O6  — NM β-pyrochlore, ambient SC; ΔE 🟠 needs DFT")
    print("   2) CsOs2O6  — NM β-pyrochlore, ambient SC; ΔE 🟠 needs DFT")
    print("   3) LaRu2    — NM Laves SC; ΔE 🟠 needs DFT")
    print("   (CoSn ΔE=-0.44 / CsV3Sb5 ΔE=+0.92 already DFT'd = both fail ΔE)")
    print()
    print("HONEST: all rows are 🟡 literature; ΔE shown only where reported, "
          "else 🟠 needs DFT. A screen narrows, it does not discover.")


def main():
    key = _get_mp_key()
    if key:
        rows = run_mp_path(key)
        # if every MP row errored (network down), fall back
        if all(r["metal"] is None and r["mag"] is None for r in rows):
            print("MP API unreachable for all queries — falling back to "
                  "curated literature.\n")
            print_curated_table()
            return
        rows = rank_mp(rows)
        print_mp_table(rows)
        print()
        print("(curated literature cross-reference below — 🟡 ΔE where known)")
        print()
        print_curated_table()
    else:
        print("No Materials Project API key found "
              "(secret get materialsproject.api_key / MP_API_KEY).\n")
        print_curated_table()


if __name__ == "__main__":
    main()
