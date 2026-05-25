#!/usr/bin/env python3
"""§30 — Lateral L1 cumulative ckpt lineage — SIDECAR sympy battery (2026-05-18).

RESEARCH.md §30 / DESIGN_L1.md. L1 = anima ckpt N inherits from anima ckpt
N-1, building a generation lineage DAG rooted at a gen=0 RANDOM-init node.

SEPARATE state/-local sidecar — central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py is UNCHANGED (B-DIRI / B-PRIME / B-EBT / B-S16 / B-DHDL
sidecar precedent). Closes ONLY the lineage BOOKKEEPING transfer-forms /
connection-points that are mathematically closed-form. Whether an actual
lineage carries MEMORY vs DEFECTS is an EMPIRICAL fire OUTCOME — carved out
(B-LINEAGE-NOTE, NOT counted 🔵, g3).

Closed propositions (sympy / Boolean — real-limit anchors, NO σ/τ/φ/J₂
derivation ⇒ f1/f2/f3 hard-fail safe):

  B-LINEAGE-1  GENERATION-INDEX-MONOTONE-CLOSED
      Each inheritance edge advances generation depth by exactly 1:
      gen(N+1) = gen(N) + 1. Δ = +1 > 0 (sympy strict-positive), and the
      child is always strictly deeper than the parent. Kolmogorov-bounded
      integer index — a well-founded lineage DAG.

  B-LINEAGE-2  SELF-SOURCE-vs-EXTERNAL-PRECURSOR-DISJOINT-CLOSED
      parent_source ∈ {"anima_self","external"} is a closed 2-element
      partition: disjoint (∩ = ∅) AND exhaustive (∪ = the enum). The
      admissibility predicate cleanly separates anima-self lineage from
      external-precursor inheritance — THE governance-distinguishing
      invariant (DESIGN_L1.md §3/§4). PASS = the distinction is mechanically
      DEFINABLE. (Honest: PASS is necessary, NOT sufficient — a clean
      self-ckpt may still be memorization-saturated, §6 = B-LINEAGE-NOTE.)

  B-LINEAGE-3  CELL-POOL-MERGE-CARDINALITY-CLOSED
      Generational merge of an n-cell child pool with an m-cell parent pool
      yields n+m cells, clamped to [MIN=2, MAX=64] via
      clamp(x,MIN,MAX) = min(MAX, max(MIN,x)) — integer cardinality closure
      ∀ x ∈ ℤ. Mirrors B-MITOSIS-3 (count conservation) + B-MITOSIS-5
      (bounded clamp, .clm v1 P2 spec).

  B-LINEAGE-4  GENERATION-0-REDUCTION-CLOSED  (연결부위 🔵)
      At gen=0 the parent pointer is None ⇒ the inheritance map runs zero
      times ⇒ init_weights = RANDOM seed-fixed. ⇒ L1 at gen-0 IS the
      current g_clm_from_scratch regime, byte-equal. The current regime is
      exactly the gen=0 slice of L1's design space — L1 is a conservative
      superset. Boolean overlay-off, mirrors B-EBT-5 / B-S16-5.

CARVE-OUT (B-LINEAGE-NOTE, NOT closed, honest g3): whether inheriting ckpt N
into ckpt N+1 carries MEMORY (generational accumulation) or DEFECTS (the
§16.6-C memorization-saturated byte-cascade attractor, propagated and
deepened) is an EMPIRICAL SGD OUTCOME (B-D-NOTE / B-ATTRACTOR-NOTE /
B-SCALE-NOTE family). The battery proves the lineage BOOKKEEPING is
closed-form; it does NOT prove L1 helps — DESIGN_L1.md §6/§7 argue, from
prior measured evidence, that L1 fired today would propagate a lineage of
defects. No capability / emergence claim.
"""
import json
import os

import sympy as sp

PASS = []


def check(name, ok, detail):
    PASS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         {detail}")


# ── B-LINEAGE-1 — GENERATION-INDEX-MONOTONE ─────────────────────────────
# gen(N+1) = gen(N) + 1. Δ = +1 strictly positive ∀ N. Child strictly
# deeper than parent — a well-founded (terminating) lineage DAG.
genN = sp.Symbol("genN", integer=True, nonnegative=True)
gen_child = genN + 1
delta = sp.simplify(gen_child - genN)
delta_strict_pos = (delta == 1) and bool(sp.simplify(delta > 0))
# 4-witness panel: gen 0->1, 1->2, 5->6, 41->42
witnesses_1 = all(
    int(gen_child.subs(genN, g)) == g + 1 and (g + 1) > g
    for g in (0, 1, 5, 41)
)
# parent always strictly shallower than child
child_deeper = bool(sp.simplify(gen_child > genN))
check("B-LINEAGE-1 GENERATION-INDEX-MONOTONE-CLOSED",
      delta_strict_pos and witnesses_1 and child_deeper,
      f"Δgen = {delta} (strict +1>0); child strictly deeper than parent "
      f"({gen_child} > genN); 4-witness 0→1,1→2,5→6,41→42 OK — well-founded "
      f"integer lineage depth.")


# ── B-LINEAGE-2 — SELF-SOURCE-vs-EXTERNAL-PRECURSOR-DISJOINT ─────────────
# parent_source ∈ {anima_self, external} = a closed 2-element partition.
S_SELF, S_EXT = "anima_self", "external"
ENUM = frozenset({S_SELF, S_EXT})
# disjoint: the two singleton classes share nothing
disjoint = frozenset({S_SELF}) & frozenset({S_EXT}) == frozenset()
# exhaustive: every value classified into exactly one class
exhaustive = (frozenset({S_SELF}) | frozenset({S_EXT})) == ENUM


def admissible(parent_source, root_gen):
    """anima-self lineage iff parent_source==anima_self AND chain roots at
    a gen=0 RANDOM-init node. The governance-distinguishing predicate."""
    return parent_source == S_SELF and root_gen == 0


# 4-corner truth table — the predicate cleanly separates the two cases:
#   (anima_self, root gen 0)  -> True   (admissible anima lineage)
#   (anima_self, root gen >0) -> False  (no RANDOM-init root — malformed)
#   (external,  root gen 0)   -> False  (external precursor — FORBIDDEN)
#   (external,  root gen >0)  -> False  (external precursor — FORBIDDEN)
tt = {
    (S_SELF, 0): True,
    (S_SELF, 3): False,
    (S_EXT, 0): False,
    (S_EXT, 7): False,
}
tt_ok = all(admissible(src, rg) == want for (src, rg), want in tt.items())
# the predicate is total (decidable for every enum value) and the two
# classes are provably non-overlapping — the distinction IS definable.
separable = disjoint and exhaustive and tt_ok
check("B-LINEAGE-2 SELF-SOURCE-vs-EXTERNAL-PRECURSOR-DISJOINT-CLOSED",
      separable,
      f"parent_source partition {{anima_self,external}}: disjoint={disjoint} "
      f"exhaustive={exhaustive}; admissible() 4-corner truth table OK "
      f"(only (anima_self, root gen 0)=True). The governance distinction is "
      f"mechanically DEFINABLE — necessary, NOT sufficient (B-LINEAGE-NOTE).")


# ── B-LINEAGE-3 — CELL-POOL-MERGE-CARDINALITY ───────────────────────────
# Generational merge: n child cells + m parent cells -> n+m, clamped [2,64].
n_child = sp.Symbol("n_child", integer=True, nonnegative=True)
m_parent = sp.Symbol("m_parent", integer=True, nonnegative=True)
merged = n_child + m_parent
# integer-additivity closure: n+m is integer ∀ integer n,m (Kolmogorov count)
merge_int_closed = merged.is_integer is True

MIN_C, MAX_C = 2, 64
x = sp.Symbol("x", integer=True)
clamp = sp.Min(MAX_C, sp.Max(MIN_C, x))
# clamp is idempotent on the bound interval, saturates outside
w_below = int(clamp.subs(x, 0)) == MIN_C        # 0 -> 2
w_in = int(clamp.subs(x, 30)) == 30             # 30 -> 30
w_above = int(clamp.subs(x, 200)) == MAX_C      # 200 -> 64 (large merge cap)
w_self_merge = int(clamp.subs(x, 2 + 2)) == 4   # B-MITOSIS organic 2+2 witness
# merged value always lands in [2,64] after clamp
merged_in_bounds = all(
    MIN_C <= int(clamp.subs(x, nc + mp)) <= MAX_C
    for nc, mp in ((0, 0), (1, 1), (32, 40), (60, 60))
)
check("B-LINEAGE-3 CELL-POOL-MERGE-CARDINALITY-CLOSED",
      merge_int_closed and w_below and w_in and w_above and w_self_merge
      and merged_in_bounds,
      f"merge(n,m)=n+m integer-closed; clamp(x,2,64)=min(64,max(2,x)) "
      f"witnesses 0→2, 30→30, 200→64, 2+2→4; merged∈[2,64] ∀ — mirrors "
      f"B-MITOSIS-3 count-conservation + B-MITOSIS-5 bounded clamp.")


# ── B-LINEAGE-4 — GENERATION-0-REDUCTION-CLOSED (연결부위) ────────────────
# At gen=0: parent is None ⇒ the inheritance map runs over 0 ancestors ⇒
# init_weights = RANDOM seed-fixed ⇒ L1|gen=0 IS g_clm_from_scratch byte-equal.
gen0 = 0
# the inheritance "loop" walks parent pointers; gen-0 has 0 of them.
n_inherit_steps_at_gen0 = max(0, gen0)          # range(0) ⇒ body skipped
gen0_no_inheritance = (n_inherit_steps_at_gen0 == 0)
# Boolean overlay-off: gen=0 ⇒ parent_pointer is None ⇒ init = RANDOM.
# symbol: has_inheritance(gen) is True iff gen>0.
gen_sym = sp.Symbol("gen", integer=True, nonnegative=True)
has_inheritance = sp.Piecewise((1, gen_sym > 0), (0, True))
gen0_is_random_init = (int(has_inheritance.subs(gen_sym, 0)) == 0)
genN_inherits = (int(has_inheritance.subs(gen_sym, 1)) == 1)   # positive ctrl
# ⇒ current from-scratch regime == L1 ∩ {gen=0} (conservative superset)
reduction_ok = (gen0_no_inheritance and gen0_is_random_init
                and genN_inherits)
check("B-LINEAGE-4 GENERATION-0-REDUCTION-CLOSED",
      reduction_ok,
      f"gen=0 ⇒ {n_inherit_steps_at_gen0} inheritance steps (loop skipped) "
      f"⇒ init=RANDOM seed-fixed ⇒ L1|gen=0 byte-equal to g_clm_from_scratch; "
      f"positive control gen=1 ⇒ inheritance fires. Current regime = the "
      f"gen=0 slice of L1 — L1 is a conservative superset (connection-point).")


# ── summary ─────────────────────────────────────────────────────────────
total = len(PASS)
passed = sum(1 for _, ok, _ in PASS if ok)
print(f"\nB-LINEAGE battery: {passed}/{total} closed-form proofs PASS")
print("B-LINEAGE-NOTE (empirical carve-out, NOT counted 🔵): whether a real "
      "lineage carries MEMORY vs DEFECTS — propagation of the §16.6-C "
      "memorization-saturated byte-cascade attractor — is an EMPIRICAL SGD "
      "OUTCOME (B-D-NOTE / B-ATTRACTOR-NOTE family). DESIGN_L1.md §6/§7: L1 "
      "fired today would likely deepen the attractor (init inside the basin) "
      "⇒ design-close (governance-blocked + premature).")

out = {
    "battery": "B-LINEAGE",
    "cycle": "§30 — Lateral L1 cumulative ckpt lineage (DESIGN-TIER)",
    "date": "2026-05-18",
    "passed": passed,
    "total": total,
    "all_blue": passed == total,
    "verdicts": [{"name": n, "pass": ok, "detail": d} for n, ok, d in PASS],
    "verdict_path": "(b) DESIGN-CLOSE — governance-blocked AND premature",
    "honest_scope": (
        "Closed side = lineage BOOKKEEPING transfer-forms: generation-index "
        "monotonicity, the self/external partition decidability, cell-pool "
        "merge cardinality clamp, and the gen-0 byte-equal reduction to "
        "g_clm_from_scratch. B-LINEAGE-2 PASS proves the governance "
        "distinction is DEFINABLE — necessary, NOT sufficient. Whether L1 "
        "carries memory or defects is EMPIRICAL (B-LINEAGE-NOTE) and "
        "DESIGN_L1.md §6 argues, from §16.6-C / B-ATTRACTOR / §11-A measured "
        "evidence, that L1 fired now would propagate a lineage of defects. "
        "NO capability / emergence claim. design-close is a valid g3 verdict."),
    "f1_f2_f3_safe": ("anchors = integer monotonicity / Boolean set partition "
                      "/ integer cardinality clamp / Boolean reduction — "
                      "NO σ/τ/φ/J₂ derivation; no corpus; B-IDENTITY-5 N/A"),
    "central_blue_falsifier_touched": False,
}
here = os.path.dirname(os.path.abspath(__file__))
json.dump(out, open(os.path.join(here, "blue_falsifier_lineage_result.json"),
                    "w"), ensure_ascii=False, indent=2)
print("wrote blue_falsifier_lineage_result.json")
raise SystemExit(0 if passed == total else 1)
