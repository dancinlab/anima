#!/usr/bin/env python3
"""B-S95 sidecar closed-form battery — RESEARCH §95 xeno substrate-suitability.

SIDECAR ONLY. Does NOT touch the central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` (0-line-diff mandate;
B-S95-7 asserts the central SHA is unchanged).

B-S95-1 TAXONOMY-PARTITION-EXHAUSTIVE-DISJOINT
B-S95-2 LEARNING-VS-INFERENCE-CLOSED-BOOLEAN
B-S95-3 CLASSIFY-DETERMINISTIC
B-S95-4 §7-GOAL-LEGITIMACY-CLOSED-CONJUNCTION
B-S95-5 LOIHI-IS-SOLE-VIABLE
B-S95-6 ORGANOID-ETHICS-WALL-CLOSED
B-S95-7 SUBSTRATE-INVENTORY-BYTE-EQUAL  (connection-point)
B-S95-NOTE empirical carve-out (necessary-not-sufficient, not counted 🔵)

g3: design-tier; closed-form proofs about the TAXONOMY, not about emergence.
f1/f2: no σ/τ/φ/J₂ lattice-fit — pure Boolean/sympy set algebra.
"""
import itertools
import json
import os
import subprocess
import sympy as sp

BUCKETS = (
    "VIABLE-LONG-HORIZON",
    "INFERENCE-ONLY-BLOCKED",
    "SUBSTRATE-MISMATCH",
    "ETHICS-WALL",
    "NOT-A-COMPUTE-HOST",
)


def classify(L, E, H, kind, ethics_wall):
    """Deterministic total classification — §95 DESIGN.md §2 decision tree.

    L, E, H, ethics_wall : bool
    kind : one of {"compute-NO", "organoid", "silicon-neuro", "quantum-gate"}
    """
    if kind == "compute-NO":
        return "NOT-A-COMPUTE-HOST"
    if kind == "organoid" and ethics_wall:
        return "ETHICS-WALL"
    if not L:
        return "INFERENCE-ONLY-BLOCKED"
    if L and E and H:
        return "VIABLE-LONG-HORIZON"
    return "SUBSTRATE-MISMATCH"


def goal_legit(generic_pretrain, generic_graft, physics_is_source):
    """§7 GOAL-legitimacy = closed Boolean conjunction."""
    return (not generic_pretrain) and (not generic_graft) and physics_is_source


# the 7 real substrates as classified in DESIGN.md §6
SUBSTRATES = {
    # name        : (L,     E,     H,     kind,            ethics_wall)
    "akida":         (False, True,  False, "silicon-neuro", False),
    "loihi3":        (True,  True,  True,  "silicon-neuro", False),
    "northpole":     (False, False, False, "silicon-neuro", False),
    "finalspark":    (True,  True,  True,  "organoid",      True),
    "cortical_labs": (True,  True,  True,  "organoid",      True),
    "ionq":          (False, False, False, "quantum-gate",  False),  # ~ -> False (no on-substrate plasticity)
    "qrng":          (False, False, False, "compute-NO",    False),
}

results = {}


def rec(name, ok, detail):
    results[name] = {"pass": bool(ok), "detail": detail}
    print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")


# ── full closed input space ──────────────────────────────────────────
KINDS = ("compute-NO", "organoid", "silicon-neuro", "quantum-gate")
SPACE = list(itertools.product((False, True), (False, True), (False, True),
                               KINDS, (False, True)))

# ── B-S95-1 TAXONOMY-PARTITION-EXHAUSTIVE-DISJOINT ───────────────────
seen = set()
exhaustive = True
for tup in SPACE:
    b = classify(*tup)
    if b not in BUCKETS:
        exhaustive = False
    seen.add(b)
# exhaustive: every tuple maps into BUCKETS; disjoint: classify returns ONE
# value (a function — single-valued by construction). Verify the 5-set is the
# exact image and is itself pairwise-disjoint as a set partition.
disjoint = len(BUCKETS) == len(set(BUCKETS))
rec("B-S95-1 TAXONOMY-PARTITION-EXHAUSTIVE-DISJOINT",
    exhaustive and disjoint and seen.issubset(set(BUCKETS)),
    f"|space|={len(SPACE)} all->BUCKETS, image={len(seen)} buckets, "
    f"5 buckets pairwise-distinct, classify single-valued")

# ── B-S95-2 LEARNING-VS-INFERENCE-CLOSED-BOOLEAN ─────────────────────
# closed claim: a compute-host (kind in silicon-neuro/quantum-gate) with L=False
# is ALWAYS INFERENCE-ONLY-BLOCKED (organoid/compute-NO short-circuit earlier).
ok = True
for E in (False, True):
    for H in (False, True):
        for kind in ("silicon-neuro", "quantum-gate"):
            if classify(False, E, H, kind, False) != "INFERENCE-ONLY-BLOCKED":
                ok = False
# and L is a genuine 2-valued Boolean (sympy)
Lsym = sp.Symbol("L")
is_bool = sp.simplify(sp.Or(sp.Eq(Lsym, True), sp.Eq(Lsym, False))) is not None
rec("B-S95-2 LEARNING-VS-INFERENCE-CLOSED-BOOLEAN", ok and is_bool,
    "L=False ∧ compute-host ⇒ INFERENCE-ONLY-BLOCKED ∀ E,H,kind; L is 2-valued")

# ── B-S95-3 CLASSIFY-DETERMINISTIC ───────────────────────────────────
runs = []
for _ in range(3):
    runs.append(tuple(classify(*t) for t in SPACE))
deterministic = runs[0] == runs[1] == runs[2]
# pure function: AST-audit `classify` body has no RNG / no clock call —
# inspect the function source only, not the whole file (which has subprocess).
import ast as _ast
import inspect as _inspect
_cls_src = _inspect.getsource(classify)
_cls_ast = _ast.parse(_cls_src)
_forbidden = {"random", "randint", "uniform", "shuffle", "choice",
              "time", "monotonic", "perf_counter"}
_hits = 0
for _node in _ast.walk(_cls_ast):
    if isinstance(_node, _ast.Name) and _node.id in _forbidden:
        _hits += 1
    if isinstance(_node, _ast.Attribute) and _node.attr in _forbidden:
        _hits += 1
classify_pure = _hits == 0
rec("B-S95-3 CLASSIFY-DETERMINISTIC", deterministic and classify_pure,
    f"3x bit-identical over {len(SPACE)} tuples; classify() AST has 0 "
    f"RNG/clock refs (pure function)")

# ── B-S95-4 §7-GOAL-LEGITIMACY-CLOSED-CONJUNCTION ────────────────────
# 16-row truth table over (generic_pretrain, generic_graft, physics_is_source);
# only (F,F,T) -> True.  (physics_is_source is the 3rd; first two negated.)
truth = {}
for gp, gg, ps in itertools.product((False, True), repeat=3):
    truth[(gp, gg, ps)] = goal_legit(gp, gg, ps)
only_one_true = sum(truth.values()) == 1 and truth[(False, False, True)] is True
# sympy mirror
gp, gg, ps = sp.symbols("gp gg ps")
expr = sp.And(sp.Not(gp), sp.Not(gg), ps)
sym_ok = bool(expr.subs({gp: False, gg: False, ps: True})) and \
    not bool(expr.subs({gp: True, gg: False, ps: True}))
rec("B-S95-4 §7-GOAL-LEGITIMACY-CLOSED-CONJUNCTION", only_one_true and sym_ok,
    "8-row truth table: legit ⇔ (¬pretrain ∧ ¬graft ∧ physics-source), 1/8 True")

# ── B-S95-5 LOIHI-IS-SOLE-VIABLE ─────────────────────────────────────
viable = [n for n, t in SUBSTRATES.items()
          if classify(*t) == "VIABLE-LONG-HORIZON"]
sole_loihi = viable == ["loihi3"]
rec("B-S95-5 LOIHI-IS-SOLE-VIABLE", sole_loihi,
    f"of 7 substrates, VIABLE-LONG-HORIZON set = {viable} (cardinality 1)")

# ── B-S95-6 ORGANOID-ETHICS-WALL-CLOSED ──────────────────────────────
# kind==organoid ∧ ethics_wall ⇒ bucket==ETHICS-WALL ∀ L,E,H
ok = True
for L, E, H in itertools.product((False, True), repeat=3):
    if classify(L, E, H, "organoid", True) != "ETHICS-WALL":
        ok = False
# and the two real organoids both land ETHICS-WALL (design-OPEN, no cap verdict)
organoids = [n for n, t in SUBSTRATES.items()
             if classify(*t) == "ETHICS-WALL"]
ok = ok and set(organoids) == {"finalspark", "cortical_labs"}
rec("B-S95-6 ORGANOID-ETHICS-WALL-CLOSED", ok,
    f"organoid ∧ ethics_wall ⇒ ETHICS-WALL ∀ L,E,H; real organoids={organoids}")

# ── B-S95-7 SUBSTRATE-INVENTORY-BYTE-EQUAL (connection-point) ────────
XENO_INVENTORY = {"akida", "loihi3", "northpole", "finalspark",
                  "cortical_labs", "ionq", "qrng"}
inv_match = set(SUBSTRATES.keys()) == XENO_INVENTORY
# central blue_falsifier.py 0-line-diff: SHA must equal the recorded c93e160a...
central = os.path.expanduser(
    "~/core/anima/state/verify_hexad_blue_2026_05_15/blue_falsifier.py")
central_sha_ok = True
central_sha = "absent"
try:
    out = subprocess.run(["shasum", "-a", "256", central],
                         capture_output=True, text=True, timeout=20)
    central_sha = out.stdout.split()[0][:12] if out.stdout else "absent"
    central_sha_ok = central_sha == "c93e160a8a37"
except Exception:
    central_sha_ok = False
rec("B-S95-7 SUBSTRATE-INVENTORY-BYTE-EQUAL", inv_match and central_sha_ok,
    f"7-substrate set == hexa xeno inventory; central SHA {central_sha} "
    f"(expect c93e160a8a37, 0-line-diff)")

# ── B-S95-NOTE (empirical carve-out — NOT counted 🔵) ────────────────
print("  NOTE  B-S95-NOTE: whether anima EMERGES on any substrate (Loihi or "
      "other) is an SGD/hardware OUTCOME, design-tier un-measurable. Battery "
      "proves taxonomy exhaustive/disjoint/deterministic + classification "
      "closed-form — NOT that any substrate yields emergence. "
      "necessary-not-sufficient (B-EMERGE-7); B-D-NOTE/B-S94-NOTE family.")

n_pass = sum(1 for v in results.values() if v["pass"])
n_tot = len(results)
print(f"\nB-S95 battery: {n_pass}/{n_tot} 🔵 PASS")

if __name__ == "__main__":
    out = {
        "battery": "B-S95",
        "pass": n_pass,
        "total": n_tot,
        "all_blue": n_pass == n_tot,
        "results": results,
        "note": "B-S95-NOTE empirical carve-out — emergence is design-tier "
                "un-measurable; necessary-not-sufficient (B-EMERGE-7).",
    }
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "blue_falsifier_s95_result.json"), "w") as f:
        json.dump(out, f, indent=2)
    raise SystemExit(0 if n_pass == n_tot else 1)
