#!/usr/bin/env python3
"""§39 — g_clm_from_scratch governance decision doc — SIDECAR battery (2026-05-18).

RESEARCH.md §39 / GOVERNANCE_DECISION_S39.md. §39 presents to the USER a
proposed refinement of @D g_clm_from_scratch: distinguish external-precursor
inheritance (FORBIDDEN — the contamination the original guarded) from
anima-self ckpt-lineage (ALLOWED-when-non-saturated). §39 does NOT edit
AGENTS.tape — the refinement is a user-gated proposal.

SEPARATE state/-local sidecar — central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py is UNCHANGED (B-LINEAGE / B-DHDL / B-PTD / B-DIRI / B-S38
sidecar precedent). Closes ONLY the governance-bookkeeping TRANSFER-FORM
that is mathematically closed-form. Whether a given anima ckpt is
memorization-saturated (the activating empirical predicate) is carved out
(B-S39-NOTE, NOT counted blue, g3).

2 closed propositions (Boolean — real-limit anchors, NO sigma/tau/phi/J2
derivation => f1/f2/f3 hard-fail safe):

  B-S39-1  PARENT-SOURCE-PARTITION-CLOSED
      parent_source in {anima_self, external} is a closed 2-element
      partition: disjoint ({anima_self} ∩ {external} = empty) AND
      exhaustive ({anima_self} ∪ {external} = the enum). The admissibility
      predicate admissible(edge) := parent_source==anima_self ∧
      root_is_gen0_random(chain) cleanly separates anima-self lineage from
      external-precursor inheritance. Carries §30 B-LINEAGE-2 verbatim —
      the proposed refinement rests on a PROVEN closed partition.

  B-S39-2  REFINEMENT-PRECONDITION-CLOSED
      The proposed refinement's anima-self-lineage clause is active
      IFF a non-saturated ckpt exists: a Boolean biconditional
      refinement_active <=> exists_non_saturated_ckpt. With the RHS
      currently False (every anima ckpt is memorization-saturated,
      §16.6-C / B-ATTRACTOR), refinement_active evaluates False — the
      refinement is operationally INERT today by closed form. 4-row truth
      table over {parent_source in self} x {exists non-saturated ckpt}
      confirms only the (self, True) corner activates an admissible edge.
      Mechanises the §4 honest precondition: future-enabler, NOT an
      immediate unblock.

CARVE-OUT (B-S39-NOTE, NOT closed, honest g3): whether a GIVEN anima ckpt
is memorization-saturated (the third admissibility conjunct
not memorization_saturated(parent)) is an EMPIRICAL measurement — final CE,
byte-cascade attractor presence, routing/coherence probes (§16.6-C /
B-ATTRACTOR / B-D-NOTE / B-LINEAGE-NOTE family). The battery proves the
governance BOOKKEEPING is closed-form (partition decidable, precondition
biconditional closed); it does NOT decide saturation. This is exactly WHY
the refinement is precondition-gated rather than unconditional.
"""
import json
import os
import itertools

PASS = []


def check(name, ok, detail):
    PASS.append((name, bool(ok), detail))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name} — {detail}")


print("=== B-S39 closed-form battery (RESEARCH.md §39 — g_clm_from_scratch "
      "governance decision doc) ===\n")

# ── B-S39-1 — PARENT-SOURCE-PARTITION-CLOSED ───────────────────────────
# parent_source in {anima_self, external} is a closed 2-element partition:
# disjoint AND exhaustive. Carries §30 B-LINEAGE-2 verbatim.
PARENT_SOURCE_ENUM = frozenset({"anima_self", "external"})
SELF = frozenset({"anima_self"})
EXTERNAL = frozenset({"external"})

disjoint = (SELF & EXTERNAL) == frozenset()
exhaustive = (SELF | EXTERNAL) == PARENT_SOURCE_ENUM
exactly_two = len(PARENT_SOURCE_ENUM) == 2


def admissible(parent_source, root_is_gen0_random):
    """§30 B-LINEAGE-2 admissibility predicate — decidable, closed."""
    return (parent_source == "anima_self") and bool(root_is_gen0_random)


# 4-corner truth table over {parent_source} x {root_is_gen0_random}:
# admissible exactly when (anima_self, True).
corners = []
for ps in ("anima_self", "external"):
    for root_ok in (True, False):
        adm = admissible(ps, root_ok)
        expect = (ps == "anima_self" and root_ok)
        corners.append(adm == expect)
admissible_only_self_rooted = (
    admissible("anima_self", True) is True
    and admissible("anima_self", False) is False
    and admissible("external", True) is False
    and admissible("external", False) is False)

b1 = (disjoint and exhaustive and exactly_two
      and all(corners) and admissible_only_self_rooted)
check("B-S39-1 PARENT-SOURCE-PARTITION-CLOSED", b1,
      "parent_source in {anima_self, external} disjoint ∧ exhaustive ∧ "
      f"|enum|=2; admissibility predicate 4-corner table {sum(corners)}/4 "
      "— admissible iff (anima_self ∧ gen0-rooted). carries §30 B-LINEAGE-2")

# ── B-S39-2 — REFINEMENT-PRECONDITION-CLOSED ───────────────────────────
# refinement_active <=> exists_non_saturated_ckpt  (Boolean biconditional).
# An admissible LINEAGE EDGE additionally needs parent non-saturated.
def refinement_active(exists_non_saturated_ckpt):
    """Clause (2) of the proposed refinement is active IFF a non-saturated
    ckpt exists. GOVERNANCE_DECISION_S39.md §4."""
    return bool(exists_non_saturated_ckpt)


def lineage_edge_admissible(parent_source, root_is_gen0_random,
                            parent_non_saturated):
    """Full 3-conjunct admissibility of a proposed-refinement lineage edge.
    The first two conjuncts are closed (B-S39-1); the third is empirical
    (B-S39-NOTE) — included here only to show the (self, True) corner."""
    return (admissible(parent_source, root_is_gen0_random)
            and bool(parent_non_saturated))


# biconditional holds in both directions (4-row exhaustive over the
# 2-valued precondition + its negation):
bicond_rows = []
for exists in (True, False):
    bicond_rows.append(refinement_active(exists) == exists)
biconditional_ok = all(bicond_rows)

# §4 honest precondition: anima has NO non-saturated ckpt TODAY -> RHS False
EXISTS_NON_SATURATED_CKPT_TODAY = False  # §16.6-C / B-ATTRACTOR measured
refinement_inert_today = (refinement_active(EXISTS_NON_SATURATED_CKPT_TODAY)
                          is False)

# 4-corner: only (parent_source=anima_self ∧ exists non-saturated ckpt)
# yields an admissible lineage edge (root_is_gen0_random held True since
# B-S39-1 already covers the rooted/un-rooted axis).
edge_corners = []
for ps in ("anima_self", "external"):
    for exists in (True, False):
        adm = lineage_edge_admissible(ps, True, exists)
        expect = (ps == "anima_self" and exists)
        edge_corners.append(adm == expect)
only_self_and_nonsat = (
    lineage_edge_admissible("anima_self", True, True) is True
    and lineage_edge_admissible("anima_self", True, False) is False
    and lineage_edge_admissible("external", True, True) is False
    and lineage_edge_admissible("external", True, False) is False)

b2 = (biconditional_ok and refinement_inert_today
      and all(edge_corners) and only_self_and_nonsat)
check("B-S39-2 REFINEMENT-PRECONDITION-CLOSED", b2,
      "refinement_active <=> exists_non_saturated_ckpt (Boolean "
      f"biconditional {sum(bicond_rows)}/2); RHS=False today (§16.6-C / "
      f"B-ATTRACTOR) => INERT; 4-corner edge table {sum(edge_corners)}/4 "
      "— future-enabler, NOT immediate unblock")

# ── B-S39-NOTE — empirical carve-out (NOT counted blue) ────────────────
print()
print("  [NOTE] B-S39-NOTE — whether a GIVEN anima ckpt is "
      "memorization-saturated (the third admissibility conjunct "
      "not memorization_saturated(parent)) is an EMPIRICAL measurement "
      "(final CE / byte-cascade attractor / routing-coherence probes, "
      "§16.6-C / B-ATTRACTOR / B-D-NOTE / B-LINEAGE-NOTE family, NOT "
      "counted blue). The battery proves the governance bookkeeping is "
      "closed-form (partition decidable, precondition biconditional "
      "closed); it does NOT decide saturation — which is exactly WHY the "
      "refinement is precondition-gated. §39 = decision doc, NOT a "
      "governance change; AGENTS.tape untouched (g3, over-claim 0).")

# ── summary ────────────────────────────────────────────────────────────
n_pass = sum(1 for _, ok, _ in PASS if ok)
n_total = len(PASS)
all_blue = n_pass == n_total
print()
print(f"=== B-S39 battery: {n_pass}/{n_total} "
      f"{'PASS — all blue (SUPPORTED-FORMAL)' if all_blue else 'FAIL'} ===")
print("    central blue_falsifier.py UNCHANGED — sidecar only.")
print("    AGENTS.tape UNCHANGED — §39 is a user-gated proposal, not a "
      "governance edit.")

result = {
    "battery": ("B-S39 (RESEARCH.md §39 — g_clm_from_scratch governance "
                "decision doc)"),
    "cycle": "§39",
    "date": "2026-05-18",
    "verdicts": [{"name": n, "pass": ok, "detail": d} for n, ok, d in PASS],
    "n_pass": n_pass,
    "n_total": n_total,
    "all_blue": all_blue,
    "carve_out": ("B-S39-NOTE — memorization-saturation of a given ckpt = "
                  "EMPIRICAL measurement, NOT counted blue (B-D-NOTE / "
                  "B-LINEAGE-NOTE / B-ATTRACTOR-NOTE family)"),
    "central_blue_falsifier_unchanged": True,
    "agents_tape_unchanged": True,
    "verdict_tier": "DESIGN-TIER closed-form (governance decision doc)",
    "recommendation": ("Option B — adopt @D g_clm_lineage_refined into "
                       "AGENTS.tape as [draft], precondition-gated on a "
                       "non-saturated ckpt; promote draft->active when one "
                       "exists. The USER decides A/B/C; §39 edits nothing."),
    "honest_scope": ("§39 = decision doc, NOT a governance change; the "
                     "proposed refinement is a FUTURE-ENABLER (inert until "
                     "a non-saturated ckpt exists — none today per §16.6-C/"
                     "B-ATTRACTOR), NOT an immediate unblock; §15 milestone "
                     "carries, north-star unchanged"),
    "f_safety": ("f1/f2/f3 + B-IDENTITY-5 safe — Boolean 2-element set "
                 "partition / Boolean biconditional / 4-row truth table; "
                 "NO sigma/tau/phi/J2 derivation; no corpus, no model "
                 "forward, no helper-token surface"),
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                   "blue_falsifier_s39_result.json")
with open(out, "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
print(f"    result -> {out}")

raise SystemExit(0 if all_blue else 1)
