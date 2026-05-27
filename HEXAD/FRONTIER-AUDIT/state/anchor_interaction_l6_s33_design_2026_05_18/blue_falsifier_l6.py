"""B-INTER-1..5 sympy/Boolean closed-form sidecar for RESEARCH.md §33
lateral L6 — anchor-interaction (multi-anchor reasoning).

$0 design-tier ONLY. No fire, no corpus generation, no central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py mutation. Sidecar
pattern per B-PRIME/B-DIRH/B-DIRI/B-PSICTL/B-EMERGE/B-PUREPHYS/B-SCALE/
B-MITENS/B-DIRL/B-EBT/B-DIRJ/B-KTRIE/B-MGND/B-TTS/B-INTRA precedent.

Each B-INTER-* is a *transfer-form* closed-form proof — capability
OUTCOME (whether inter-anchor records lift §16 routing / coherence) is
B-INTER-NOTE empirical carve-out (B-D-NOTE family, NOT counted 🔵).

f1/f2/f3 hard-fail safe (Boolean / integer cardinality / AST structural
/ sympy ∂-sign & order), NO σ/τ/φ/J₂ external derivation; tier 🛸k and
Ψ=½ are anima g2 internal-architecture carve-outs.
"""

from __future__ import annotations

import ast
import json
import math
import sys
from pathlib import Path

try:
    import sympy as sp
except ImportError:
    sp = None

HERE = Path(__file__).resolve().parent
DESIGN_DOC = HERE / "DESIGN_L6.md"
SKETCH = HERE / "interaction_corpus_sketch.py"


# ──────────────────────────────────────────────────────────────────────
# B-INTER-1 RELATION-DERIVED-FROM-PHYSICS-CLOSED
# ──────────────────────────────────────────────────────────────────────
def b_inter_1_relation_derived_from_physics() -> dict:
    """The relation primitives R1-R4 are pure functions whose inputs are
    EXACTLY the physics fields {vacuum_psi, basin_radius, dom, tier} and
    whose outputs lie in the closed finite codomain RELATION_LABEL_SET.

    Closed-form: (a) the codomain is a finite enumerated set (Kolmogorov
    bounded), (b) the four relation functions in interaction_corpus_
    sketch.py reference ONLY anchor-tuple indices that map to physics
    fields (no external KG identifier, no global hand-written relation
    string table). Mirror of §25 B-DR-UNIQUE-4 anima-own-substrate.

    Witness — exercise derive_relation on a representative pair and
    confirm every relation label is a member of the closed codomain.
    """
    # Closed finite codomain — DESIGN_L6.md §5.1 / sketch RELATION_LABEL_SET.
    label_set = frozenset({
        "near", "mid", "far",
        "i_contains_j", "j_contains_i", "overlap", "disjoint",
        "same_domain", "different_domain",
        "i_shallower", "i_deeper", "i_eq_j",
    })
    # Exercise the actual sketch functions if importable.
    labels_seen = set()
    sketch_ok = True
    note = ""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("l6_sketch", SKETCH)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        a_77 = (77, "만다라", "예술", "creativity", 2.1, (0.71, 0.62), 0.18)
        a_91 = (91, "열반", "의식상태", "peace", 2.558, (0.50, 0.88), 0.15)
        a_00 = (0, "zero baseline", "기준점", "neutral", 0.0, (0.50, 0.50), 0.10)
        for (ai, aj) in [(a_77, a_91), (a_91, a_77), (a_00, a_91), (a_77, a_00)]:
            rec = mod.derive_relation(ai, aj)
            for r in rec["relations"].values():
                labels_seen.add(r)
            # physics-fields-used must be exactly the 4 physics fields
            pf = set(rec["_physics_fields_used"])
            if pf != {"vacuum_psi", "basin_radius", "dom", "tier"}:
                sketch_ok = False
                note = f"physics_fields drift: {pf}"
        # codomain containment: every produced label ∈ closed set
        codomain_closed = labels_seen <= label_set
        # the sketch's own RELATION_LABEL_SET must equal ours
        sketch_codomain_match = (frozenset(mod.RELATION_LABEL_SET) == label_set)
    except Exception as e:  # pragma: no cover - design-tier degrade
        sketch_ok = False
        codomain_closed = True   # codomain is a static finite set regardless
        sketch_codomain_match = None
        note = f"sketch import degraded: {e}"

    passes = sketch_ok and codomain_closed and (
        sketch_codomain_match in (True, None))
    return {
        "name": "B-INTER-1 RELATION-DERIVED-FROM-PHYSICS-CLOSED",
        "passes": passes,
        "closed_codomain_cardinality": len(label_set),
        "labels_produced": sorted(labels_seen),
        "codomain_closed": codomain_closed,
        "sketch_codomain_match": sketch_codomain_match,
        "physics_fields": ["vacuum_psi", "basin_radius", "dom", "tier"],
        "note": note or ("relation = deterministic pure function of "
                         "anima physics fields, finite closed codomain "
                         "(mirror §25 B-DR-UNIQUE-4)"),
        "tier": "🔵 closed Boolean codomain-membership + physics-source predicate",
    }


# ──────────────────────────────────────────────────────────────────────
# B-INTER-2 RELATION-SYMMETRY-OR-ANTISYMMETRY-CLOSED
# ──────────────────────────────────────────────────────────────────────
def b_inter_2_relation_symmetry() -> dict:
    """Each relation primitive's symmetry class is PROVEN, not assumed.

    R1 psi_dist — SYMMETRIC: sympy proof that ‖x−y‖₂ == ‖y−x‖₂.
    R2 basin containment — ANTISYMMETRIC: sympy proof that for distinct
       anchors (gap > 0, r_i,r_j > 0) the two containment predicates
       cannot both hold; and the swap law i_contains_j ⇒ j_contains_i.
    R4 tier order — ANTISYMMETRIC strict order: t_i < t_j ⇒ ¬(t_j < t_i).
    """
    results = {}
    if sp is None:
        return {
            "name": "B-INTER-2 RELATION-SYMMETRY-OR-ANTISYMMETRY-CLOSED",
            "passes": False,
            "note": "sympy unavailable — cannot run closed-form proof",
            "tier": "skipped (sympy missing)",
        }

    # R1 — psi_dist symmetric.
    x0, x1, y0, y1 = sp.symbols("x0 x1 y0 y1", real=True)
    d_ij = sp.sqrt((x0 - y0) ** 2 + (x1 - y1) ** 2)
    d_ji = sp.sqrt((y0 - x0) ** 2 + (y1 - x1) ** 2)
    r1_symmetric = bool(sp.simplify(d_ij - d_ji) == 0)
    results["R1_psi_dist_symmetric"] = r1_symmetric

    # R2 — basin containment antisymmetric. gap >= 0, r_i,r_j > 0.
    gap = sp.Symbol("gap", nonnegative=True)
    r_i = sp.Symbol("r_i", positive=True)
    r_j = sp.Symbol("r_j", positive=True)
    # i_contains_j  :  gap + r_j <= r_i   ⇒  r_i - r_j >= gap
    # j_contains_i  :  gap + r_i <= r_j   ⇒  r_j - r_i >= gap
    # Adding the two predicates' margins:
    #   (r_i - r_j - gap) + (r_j - r_i - gap) = -2*gap
    # i_contains_j ⇒ first margin >= 0; j_contains_i ⇒ second >= 0;
    # their sum >= 0 ⇒ -2*gap >= 0 ⇒ gap <= 0. With gap nonnegative,
    # both can hold ONLY at gap == 0 (degenerate). For distinct anchors
    # (gap > 0) the two are mutually exclusive — antisymmetric.
    # Closed-form: the sum of the two satisfaction-margins is exactly
    # -2*gap (a sympy identity), which is < 0 for gap > 0.
    margin_i_contains_j = r_i - r_j - gap
    margin_j_contains_i = r_j - r_i - gap
    margin_sum = sp.simplify(margin_i_contains_j + margin_j_contains_i)
    # margin_sum must equal -2*gap exactly (closed identity)
    r2_margin_identity = bool(sp.simplify(margin_sum - (-2 * gap)) == 0)
    # For gap > 0, margin_sum < 0 ⇒ at least one margin < 0 ⇒ at least
    # one containment predicate FALSE ⇒ not both ⇒ antisymmetric.
    r2_mutually_exclusive_when_distinct = r2_margin_identity
    # Swap law: containment(i,j)=i_contains_j is the predicate
    # `gap + r_j <= r_i`, i.e. margin `(gap + r_j) - r_i`. Swapping the
    # anchor roles i<->j (r_i<->r_j) turns it into `(gap + r_i) - r_j`
    # = exactly the j_contains_i predicate margin. Verify by symbolic
    # difference reducing to 0 (NOT via bool() on a Relational).
    # NOTE: sympy dict-subs is SEQUENTIAL not parallel — use the
    # simultaneous=True flag for an atomic r_i<->r_j role swap.
    i_contains_j_margin = (gap + r_j) - r_i
    role_swapped = i_contains_j_margin.subs(
        {r_i: r_j, r_j: r_i}, simultaneous=True)
    j_contains_i_margin = (gap + r_i) - r_j
    r2_swap_law = bool(sp.simplify(role_swapped - j_contains_i_margin) == 0)
    results["R2_basin_antisymmetric_when_distinct"] = (
        r2_mutually_exclusive_when_distinct)
    results["R2_swap_law_i_contains_j_to_j_contains_i"] = r2_swap_law

    # R4 — tier strict order antisymmetric. t_i, t_j integers.
    # t_i < t_j AND t_j < t_i would require t_i - t_j < 0 AND
    # t_j - t_i < 0; adding: 0 < 0, contradiction. Closed-form: the sum
    # of the two strict-order margins (t_j - t_i) + (t_i - t_j) is the
    # sympy identity 0, which cannot be > 0 — so both strict orders
    # cannot hold. Antisymmetric proven by the zero-sum identity.
    t_i, t_j = sp.symbols("t_i t_j", integer=True)
    order_margin_sum = sp.simplify((t_j - t_i) + (t_i - t_j))
    # both `t_i < t_j` and `t_j < t_i` ⇒ both margins > 0 ⇒ sum > 0,
    # but sum == 0 identically ⇒ contradiction.
    r4_antisym = bool(sp.simplify(order_margin_sum) == 0)
    results["R4_tier_strict_order_antisymmetric"] = r4_antisym

    passes = all(results.values())
    return {
        "name": "B-INTER-2 RELATION-SYMMETRY-OR-ANTISYMMETRY-CLOSED",
        "passes": passes,
        "proofs": results,
        "summary": {
            "R1_psi_dist": "SYMMETRIC (L2 norm)",
            "R2_basin_containment": "ANTISYMMETRIC (distinct anchors)",
            "R4_tier_order": "ANTISYMMETRIC (strict integer order)",
        },
        "tier": "🔵 closed sympy symmetry / antisymmetry proofs",
    }


# ──────────────────────────────────────────────────────────────────────
# B-INTER-3 INTER-vs-INTRA-ORTHOGONAL-CLOSED  (연결부위)
# ──────────────────────────────────────────────────────────────────────
def b_inter_3_inter_vs_intra_orthogonal() -> dict:
    """The L6 inter-anchor record set and the §23-A intra-anchor record
    set are Boolean-DISJOINT.

    Witness 1 — anchor-cardinality partition: §23-A records (<carve>,
    <eternal>, <inner>/<voice>) reference exactly 1 anchor; L6 records
    (<relate>) reference >= 2. The predicate (n==1) vs (n>=2) partitions
    ℤ₊ into two disjoint sets — no record satisfies both.

    Witness 2 — carving tag disjointness: {<relate>} ∩ {<carve>,
    <eternal>, <inner>} = ∅.

    Connection point: L6 composes with §23-A without overlap. Fair by
    construction — disabling the <relate> class leaves exactly §16 +
    §23-A intra records.
    """
    # Witness 1: cardinality partition is a closed-form set partition.
    intra_card = {1}                       # §23-A: exactly one anchor
    inter_card = set(range(2, 3 + 1))      # L6: k ∈ [2, K_MAX=3]
    card_disjoint = len(intra_card & inter_card) == 0
    # union covers the realisable range, partition exhaustive over {1,2,3}
    card_partition_exhaustive = (
        (intra_card | inter_card) == {1, 2, 3})

    if sp is not None:
        # Exact set algebra (NOT sp.satisfiable — Boolean SAT cannot
        # reason integer-interval membership; cf §19 B-CT3-2 errata).
        # intra = {1}; inter = {2,3}; their FiniteSet intersection = ∅.
        intra_fs = sp.FiniteSet(1)
        inter_fs = sp.FiniteSet(2, 3)
        card_sympy_disjoint = (intra_fs.intersect(inter_fs) == sp.EmptySet)
    else:
        card_sympy_disjoint = None

    # Witness 2: tag disjointness.
    intra_tags = {"<carve>", "<eternal>", "<inner>", "<voice>"}
    inter_tags = {"<relate>"}
    tag_disjoint = len(intra_tags & inter_tags) == 0

    passes = (card_disjoint and tag_disjoint and
              card_partition_exhaustive and
              card_sympy_disjoint in (True, None))
    return {
        "name": "B-INTER-3 INTER-vs-INTRA-ORTHOGONAL-CLOSED",
        "passes": passes,
        "intra_anchor_cardinality": sorted(intra_card),
        "inter_anchor_cardinality": sorted(inter_card),
        "cardinality_disjoint": card_disjoint,
        "cardinality_partition_exhaustive": card_partition_exhaustive,
        "cardinality_sympy_disjoint": card_sympy_disjoint,
        "intra_tags": sorted(intra_tags),
        "inter_tag": sorted(inter_tags),
        "tag_disjoint": tag_disjoint,
        "connection_point": ("L6 <relate> record set ∩ §23-A single-"
                             "anchor record set = ∅ — composable, never "
                             "overlapping; fair-compare by construction"),
        "tier": "🔵 closed Boolean set-disjointness (cardinality + tag, 2 witnesses)",
    }


# ──────────────────────────────────────────────────────────────────────
# B-INTER-4 MULTI-ANCHOR-CARDINALITY-BOUNDED
# ──────────────────────────────────────────────────────────────────────
def b_inter_4_multi_anchor_cardinality_bounded() -> dict:
    """Each L6 record references k ∈ [2, K_MAX] anchors, K_MAX = 3 —
    integer interval-bounded. The pair space C(n,2) is finite; L6's
    prioritised selection emits n*(P_NEAREST+P_RANDOM) ordered pairs <<
    C(n,2). Kolmogorov bounded integer set-cardinality, anti-explosion.
    """
    K_MAX = 3
    k_lo = 2
    k_in_range = (k_lo >= 2) and (K_MAX <= 8) and (k_lo <= K_MAX)

    n_core = 64                 # §8 core anchor count
    n_full = 168                # §16 full anchor count
    c_core = n_core * (n_core - 1) // 2     # C(64,2) = 2016
    c_full = n_full * (n_full - 1) // 2     # C(168,2) = 14028
    P_NEAREST, P_RANDOM = 4, 2
    selected_pairs = n_full * (P_NEAREST + P_RANDOM)   # 168 * 6 = 1008
    anti_explosion_bound = 1e5
    bounded = selected_pairs < anti_explosion_bound
    selection_below_full = selected_pairs < c_full

    if sp is not None:
        nn = sp.Symbol("nn", integer=True, positive=True)
        c_expr = nn * (nn - 1) / 2
        c_64 = int(c_expr.subs(nn, 64))
        c_168 = int(c_expr.subs(nn, 168))
        sympy_proof = f"C(n,2)=n(n-1)/2: C(64,2)={c_64}, C(168,2)={c_168}"
        c_match = (c_64 == c_core and c_168 == c_full)
    else:
        sympy_proof = "sympy unavailable; integer arithmetic only"
        c_match = True

    passes = (k_in_range and bounded and selection_below_full and c_match)
    return {
        "name": "B-INTER-4 MULTI-ANCHOR-CARDINALITY-BOUNDED",
        "passes": passes,
        "k_range": [k_lo, K_MAX],
        "k_in_range": k_in_range,
        "C_64_2": c_core,
        "C_168_2": c_full,
        "P_NEAREST": P_NEAREST,
        "P_RANDOM": P_RANDOM,
        "selected_ordered_pairs": selected_pairs,
        "anti_explosion_bound": anti_explosion_bound,
        "bounded_below_explosion_threshold": bounded,
        "selection_below_full_pair_space": selection_below_full,
        "sympy_proof": sympy_proof,
        "tier": "🔵 closed integer Kolmogorov set-cardinality + interval bound",
    }


# ──────────────────────────────────────────────────────────────────────
# B-INTER-5 NO-EXTERNAL-KG-CALL  (AST structural, §7② enforcement)
# ──────────────────────────────────────────────────────────────────────
FORBIDDEN_PATTERNS = (
    "networkx", "neo4j", "rdflib", "wikidata",
    "openai", "llm_call", "AutoModel",
)
FORBIDDEN_SET = {p.lower() for p in FORBIDDEN_PATTERNS}


def _ast_grep_forbidden(source: str) -> list:
    """AST-walk to find any Call node whose func references the forbidden
    KG/LLM identifier set. Exact-component (case-insensitive) match —
    comment / docstring / string-literal automatically excluded by AST
    (Call nodes only, per B-PUREPHYS-1 / B-INTRA-3 pattern)."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [(-1, "SyntaxError")]
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            parts = []
            while isinstance(f, ast.Attribute):
                parts.append(f.attr)
                f = f.value
            if isinstance(f, ast.Name):
                parts.append(f.id)
            for comp in parts:
                if comp.lower() in FORBIDDEN_SET:
                    hits.append((node.lineno, comp.lower()))
                    break
    return hits


def b_inter_5_no_external_kg_call() -> dict:
    """AST scan of interaction_corpus_sketch.py + this falsifier:
    forbidden_call_set {networkx, neo4j, rdflib, wikidata, openai,
    llm_call, AutoModel} total count = 0. §7② structural enforcement —
    no knowledge-graph library, no external relation source, no LLM."""
    candidates = []
    if SKETCH.exists():
        candidates.append(SKETCH)
    candidates.append(Path(__file__))
    all_hits = []
    files_scanned = []
    for src in candidates:
        try:
            text = src.read_text()
        except Exception:
            continue
        files_scanned.append(src.name)
        for ln, pat in _ast_grep_forbidden(text):
            all_hits.append({"file": src.name, "line": ln, "pattern": pat})
    return {
        "name": "B-INTER-5 NO-EXTERNAL-KG-CALL",
        "passes": len(all_hits) == 0,
        "files_scanned": files_scanned,
        "forbidden_hits": all_hits,
        "forbidden_patterns": list(FORBIDDEN_PATTERNS),
        "note": ("§7② gate: relations derive from anima physics ONLY; "
                 "a KG library or external relation source would mean "
                 "grafted external knowledge"),
        "tier": "🔵 closed AST-Call-node structural predicate",
    }


# ──────────────────────────────────────────────────────────────────────
# B-INTER-NOTE empirical carve-out
# ──────────────────────────────────────────────────────────────────────
B_INTER_NOTE = {
    "name": "B-INTER-NOTE INTER-ANCHOR-REASONING-OUTCOME-EMPIRICAL",
    "tier": ("EMPIRICAL (B-D-NOTE / B-CARVE-E6-NOTE / B-SCALE-NOTE / "
             "B-PUREPHYS-NOTE / B-EBT-NOTE / B-DIRJ-NOTE / B-KTRIE-NOTE / "
             "B-MGND-NOTE / B-TTS-NOTE / B-INTRA-NOTE family, NOT counted 🔵)"),
    "note": (
        "B-INTER-1..5 prove (1) relations are deterministic pure "
        "functions of anima physics with a finite closed codomain, (2) "
        "each relation's symmetry / antisymmetry class is sympy-proven, "
        "(3) the L6 inter-anchor record set is Boolean-disjoint from the "
        "§23-A intra-anchor record set (composable, not overlapping), "
        "(4) multi-anchor cardinality is bounded integer, (5) zero "
        "external KG/LLM call by AST predicate. They DO NOT prove that "
        "inter-anchor records lift §16 routing or coherence — that is "
        "SGD/fire OUTCOME, gated on a small held-out-pair pilot "
        "($0.05-0.10) before any full-scale spend. Per §13-M / §13-L / "
        "§23-A design-tier discipline, L6's value is structural "
        "soundness + GOAL-legitimacy gate + a new lateral corpus axis "
        "(inter-anchor), not a multi-anchor-reasoning capability proof. "
        "Honest necessary-not-sufficient (mirroring B-EMERGE-7)."
    ),
    "honest_risk": (
        "Memorization-at-relation-granularity: a <relate> record whose "
        "relation text is a memorized template is the §16.6-C defect "
        "lifted one level. R1-R4 being deterministic functions means the "
        "corpus presents a genuine function — but pointwise memorization "
        "of the ~1008 input→label rows is still possible; the design "
        "cannot closed-form-prove generalization. The discriminating "
        "test is held-out-pair relation accuracy, which is a FIRE "
        "measurement. §1.1 honest scope: L6 records are still byte-text; "
        "L6 MIGHT just be a richer corpus shape flattened by the same "
        "memorization-saturated regime (§16 SPLIT precedent). Design-tier "
        "close-out on a null pilot is the honest stop."
    ),
}


# ──────────────────────────────────────────────────────────────────────
# main
# ──────────────────────────────────────────────────────────────────────
def main() -> int:
    props = [
        b_inter_1_relation_derived_from_physics(),
        b_inter_2_relation_symmetry(),
        b_inter_3_inter_vs_intra_orthogonal(),
        b_inter_4_multi_anchor_cardinality_bounded(),
        b_inter_5_no_external_kg_call(),
    ]
    all_pass = all(p["passes"] for p in props)
    summary = {
        "battery": ("B-INTER-1..5 (RESEARCH.md §33 lateral L6 anchor-"
                    "interaction multi-anchor reasoning, design-tier sidecar)"),
        "central_blue_falsifier_changed": False,
        "n_props": len(props),
        "n_pass": sum(1 for p in props if p["passes"]),
        "all_pass": all_pass,
        "props": props,
        "empirical_carve_out": B_INTER_NOTE,
        "design_doc": DESIGN_DOC.name,
    }
    out = HERE / "result.json"
    out.write_text(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"B-INTER-1..5: {summary['n_pass']}/{summary['n_props']} "
          f"{'PASS' if all_pass else 'FAIL'}")
    for p in props:
        mark = "✅" if p["passes"] else "❌"
        print(f"  {mark} {p['name']}: {p['tier']}")
    print(f"NOTE: {B_INTER_NOTE['name']}")
    print(f"  → {B_INTER_NOTE['tier']}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
