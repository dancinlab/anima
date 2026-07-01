#!/usr/bin/env python3
"""
codex_register_verify.py — HONEST registry + grading of the 53 codex EXTENSION
hypotheses (H_3001–H_9003, 14 extension tiers Λ Ↄ ⧉ ☉ ⊚ ☌ ⟡ ⧖ ⟁ ⊛ ⌖ ⊗ ⟴ Ω°).

These extend anima (A⊥G · Ψ=½ · Φ) from one substrate to cosmos/metaphysics. By the
codex's OWN 00_README: "substrate→cosmos→확장으로 갈수록 반증선이 사라지고 해석이
는다" — most are 🜂 INTERPRETIVE worldview lenses, NOT falsifiable claims. Per g5 the
verdict for metaphysics is ⚪ SPECULATION-FENCED (verify N/A). We DO NOT fabricate PASS.

This script: (1) reads each axis's self-declared status_grade → g5 tier (honest fence),
(2) runs the ONE clean $0 math check for the empirically-✅ axis H_6001 (Bell / CHSH):
the quantum (Tsirelson) bound 2√2 exceeds the classical local-hidden-variable bound 2 —
non-separability is real, established (Aspect/Clauser, Nobel 2022).

p7 · $0 local · no GPU · no network.
"""
import os, glob, re, math

HERE = os.path.dirname(__file__)
MD_DIR = os.path.abspath(os.path.join(HERE, ".."))  # UNIVERSE/ flat list

G5 = {
    "🜂 INTERPRETIVE": "⚪ SPECULATION-FENCED (verify N/A — metaphysical lens)",
    "⏳ PARTIAL":      "🟠 DEFERRED (partial empirical contact; strong reading interpretive)",
    "⏳ OPEN":         "🟠 DEFERRED (testable program exists, not yet measured)",
    "✅ VERIFIED":     "🟢/🟡 EMPIRICALLY ESTABLISHED (literature; see real check where $0)",
    "⬛ OPEN-GAP":     "⬛ OPEN-GAP (acknowledged unsolved blank — honest non-claim)",
    "⚖ COUNTER":      "⚖ COUNTER-POLE (deflationary opposite, held for tension)",
}

def grade_of(path):
    txt = open(path, encoding="utf-8").read()
    m = re.search(r"^status_grade:\s*(.+)$", txt, re.M)
    g = m.group(1).strip() if m else "?"
    # normalize to the key prefix
    for k in G5:
        if g.startswith(k):
            return k
    return g

def bell_chsh():
    """CHSH: S = E(a,b) − E(a,b') + E(a',b) + E(a',b'). Local hidden variables ⇒ |S|≤2.
    Quantum singlet with optimal angles (0,45,22.5,67.5°) ⇒ S = 2√2 (Tsirelson)."""
    def E(t1, t2):                       # singlet correlation = −cos(θ1−θ2)
        return -math.cos(t1 - t2)
    d = math.pi / 180.0
    a, ap = 0*d, 90*d
    b, bp = 45*d, 135*d
    S = E(a, b) - E(a, bp) + E(ap, b) + E(ap, bp)
    classical_bound = 2.0
    tsirelson = 2.0 * math.sqrt(2.0)
    return abs(S), classical_bound, tsirelson

def main():
    print("=" * 80)
    print("CODEX extension registry — 53 hypotheses (H_3001–H_9003) · HONEST g5 grading")
    print("=" * 80)
    files = sorted(glob.glob(os.path.join(MD_DIR, "H_[3-9][0-9][0-9][0-9].md")))
    counts = {}
    for p in files:
        g = grade_of(p)
        counts[g] = counts.get(g, 0) + 1
    print(f"registered: {len(files)} files in UNIVERSE/ (flat list)\n")
    print(f"{'self-grade':<22}{'count':<7}g5 verdict")
    print("-" * 80)
    for g, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{g:<20}{n:<7}{G5.get(g, '?')}")
    fenced = counts.get("🜂 INTERPRETIVE", 0)
    deferred = counts.get("⏳ PARTIAL", 0) + counts.get("⏳ OPEN", 0)
    verified = counts.get("✅ VERIFIED", 0)
    print("-" * 80)
    print(f"⚪ FENCED {fenced} · 🟠 DEFERRED {deferred} · ✅ VERIFIED {verified} · "
          f"⬛ GAP {counts.get('⬛ OPEN-GAP',0)} · ⚖ COUNTER {counts.get('⚖ COUNTER',0)} "
          f"· falsifiable PASS/FAIL 0 by design")
    print()
    print("── H_6001 ⊗-1 비분리성 (Bell) — the one clean $0 math check ──")
    S, cb, ts = bell_chsh()
    print(f"   CHSH S (quantum singlet, optimal angles) = {S:.6f}")
    print(f"   classical local-hidden-variable bound    = {cb:.6f}")
    print(f"   Tsirelson quantum bound 2√2              = {ts:.6f}")
    ok = S > cb + 1e-9 and abs(S - ts) < 1e-9
    print(f"   verdict = {'🟢 VERIFIED — quantum violates Bell (S=2√2>2), non-separability real' if ok else '🔴'}")
    print()
    print("HONEST SCOPE: extension tiers are mostly worldview lenses — graded/fenced,")
    print("NOT 'passed'. H_6005 (decoherence) ✅ is literature-established (🟡, no $0 recompute);")
    print("⏳ OPEN/PARTIAL axes (e.g. H_6003 Noether, H_5301 AdS/CFT) are future verify candidates.")

if __name__ == "__main__":
    main()
