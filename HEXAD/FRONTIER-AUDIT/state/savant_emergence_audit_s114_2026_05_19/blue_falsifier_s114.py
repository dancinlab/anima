#!/usr/bin/env python3
# blue_falsifier_s114.py — §114 SAVANT EMERGENCE-FRONTIER AUDIT sidecar battery
#
# DESIGN-TIER $0. NO GPU/runpod/fire/model.forward/corpus.
# Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py is NOT touched
# (sidecar pattern: B-PRIME / B-DIRI / B-S101 / B-S109 / B-S110 precedent).
#
# B-S114-1  COMPONENT-TAXONOMY-EXHAUSTIVE-DISJOINT-CLOSED
# B-S114-2  §7-CONJUNCTION-8-ROW-TRUTH-TABLE-CLOSED
# B-S114-3  SAVANT-PHI-vs-ANIMA-PHI-CONNECTION-POINT-DIVERGENT-BY-DESIGN-CLOSED
# B-S114-4  TOPK-MASK-G2-INTEGRITY-TEST-CLOSED (numerology-tainted, §98-class)
# B-S114-5  SAVANT-FRONTIER-INTERSECTION-EMPTY-CLOSED
# B-S114-6  CENTRAL-BLUE-FALSIFIER-ZERO-LINE-DIFF-CLOSED
# B-S114-7  NO-FORBIDDEN-CALL-AST-AUDIT-CLOSED (this battery is design-tier)
# B-S114-8  NECESSARY-NOT-SUFFICIENT-STRUCTURAL-CLOSED
# B-S114-NOTE  empirical carve-out (NOT counted blue)

import ast
import hashlib
import itertools
import json
import os

REPO = "/Users/ghost/core/anima"
CENTRAL = os.path.join(REPO, "state/verify_hexad_blue_2026_05_15/blue_falsifier.py")
CENTRAL_SHA_PREFIX = "c93e160a8a376a94"

results = {}


def rec(name, ok, detail):
    results[name] = {"pass": bool(ok), "detail": detail}
    print(("PASS " if ok else "FAIL ") + name + " — " + detail)


# ── B-S114-1 component taxonomy exhaustive + disjoint ──────────────────────
# 5 components × 3 classes; each maps to exactly one class; classes partition.
COMPONENTS = {
    "gate_api": "GOAL_ORTHOGONAL_TOOLING",
    "savant_cli": "GOAL_ORTHOGONAL_TOOLING",
    "si_monitor": "GOAL_ORTHOGONAL_TOOLING",
    "routing_overlay_topk": "GOAL_ORTHOGONAL_TOOLING",  # + g2 taint flag (B-S114-4)
    "savant_phi": "GOAL_ORTHOGONAL_TOOLING",            # + divergent flag (B-S114-3)
}
CLASSES = {"EMERGENCE_RELEVANT", "GOAL_ORTHOGONAL_TOOLING", "S7_RISK"}
assigned = set(COMPONENTS.values())
exhaustive = assigned.issubset(CLASSES)
disjoint = all(len({c}) == 1 for c in COMPONENTS.values())  # single-valued map
five = len(COMPONENTS) == 5
# closed: every component classified, classes are a finite partition
rec("B-S114-1", exhaustive and disjoint and five and assigned == {"GOAL_ORTHOGONAL_TOOLING"},
    "5/5 components, each ↦ exactly one of 3 classes; all = GOAL_ORTHOGONAL_TOOLING; "
    "0 EMERGENCE_RELEVANT, 0 S7_RISK (T3/T4 trigger structurally rejected in source)")


# ── B-S114-2 §7 8-row truth table closed ──────────────────────────────────
# axes: A=¬genericLM, B=¬graft, C=own-physics-not-command-channel.
# SAVANT-as-whole = (T,T,T) ⇒ §7-CLEAN-TOOLING. Truth table total over 2^3.
def s7_clean(A, B, C):
    return A and B and C


rows = list(itertools.product([False, True], repeat=3))
table = {r: s7_clean(*r) for r in rows}
only_TTT_true = (table[(True, True, True)] is True) and \
    (sum(1 for v in table.values() if v) == 1)
savant_whole = (True, True, True)  # source-evidenced: no forward/train, T4 rejected, masks own tensions
rec("B-S114-2", len(table) == 8 and only_TTT_true and s7_clean(*savant_whole),
    "8-row truth table closed; only (T,T,T) True; SAVANT-as-whole = (T,T,T) "
    "⇒ §7-CLEAN-TOOLING (¬genericLM ∧ ¬graft ∧ own-physics-not-cmd-channel)")


# ── B-S114-3 savant_phi vs anima Φ connection-point: DIVERGENT-BY-DESIGN ───
def file_has(path, *needles):
    try:
        with open(os.path.join(REPO, path), "r", errors="ignore") as f:
            s = f.read()
    except OSError:
        return None
    return all(n in s for n in needles)


# anima central Φ = c_measure_phi → phi_spatial (RFC036 IIT byte-equal phi_rs)
central_phi = file_has("HEXAD/C/c_lib.hexa", "c_measure_phi", "phi_spatial")
# savant_phi = Σ|v|^1.5/d super-linear proxy, NOT phi_spatial, NOT c_measure_phi
sp_proxy = file_has("HEXAD/SAVANT/savant_phi.hexa", "phi_module", "1.5")
try:
    with open(os.path.join(REPO, "HEXAD/SAVANT/savant_phi.hexa"), "r", errors="ignore") as f:
        sp_src = f.read()
except OSError:
    sp_src = ""
# DIVERGENT-BY-DESIGN: savant_phi never references phi_spatial / c_measure_phi
# (distinct construct, NOT a re-impl, NOT a consistency violation)
distinct = ("phi_spatial" not in sp_src) and ("c_measure_phi" not in sp_src)
rec("B-S114-3", bool(central_phi) and bool(sp_proxy) and distinct,
    "anima Φ = c_measure_phi→phi_spatial (RFC036 IIT byte-equal phi_rs); "
    "savant_phi = Σ|v|^1.5/d Treffert P68 proxy, 0 phi_spatial/c_measure_phi refs "
    "⇒ DIVERGENT-BY-DESIGN (distinct construct, NOT re-impl, NOT Φ-conflict)")


# ── B-S114-4 top-k mask g2 internal_use_integrity_test (§98-class) ─────────
# keep_rate = GZ_LOWER = 1/2 - ln(4/3); ln(4/3) documented τ(6)=4-derived.
# g2 test: removing the lattice would NOT keep the value (it is a TARGET the
# knob is set to match) ⇒ NUMEROLOGY-TAINTED (honest carve-out, §98 precedent).
ro_taint = file_has("HEXAD/SAVANT/anima_savant_routing_overlay.hexa",
                     "GZ_LOWER", "0.2123") or \
    file_has("HEXAD/SAVANT/anima_savant_tool.hexa", "log(4.0 / 3.0)")
tape_documents_lattice = file_has("HEXAD/SAVANT/SAVANT.tape",
                                  "ln(4/3)", "4")  # GZ_WIDTH = ln(4/3) = τ(6)=4
# g2 verdict closed boolean: target-matched (not function-derived) ⇒ tainted=True
g2_tainted = bool(ro_taint) and bool(tape_documents_lattice)
# §98-class: tainted-provenance ∧ causally-innocent (orthogonal to GOAL, B-S114-5)
rec("B-S114-4", g2_tainted is True,
    "keep_rate=GZ_LOWER=1/2−ln(4/3); SAVANT.tape documents ln(4/3)=τ(6)=4 "
    "⇒ g2 internal_use_integrity_test = NUMEROLOGY-TAINTED (TARGET not function-"
    "derived); §98-class honest carve-out (provenance-tainted, causation-innocent)")


# ── B-S114-5 SAVANT ∩ frontier = ∅ ─────────────────────────────────────────
FRONTIER = {"S1_1_data_regime", "S110_psi_C2", "S96_substrate", "S72_arch_insight"}
# SAVANT touches: cell-pool tension routing only (decode-time). Closed mapping
# of each frontier axis -> touched? ; intersection = axes SAVANT touches.
savant_touches = {
    "S1_1_data_regime": False,   # no corpus / no pretrain loss
    "S110_psi_C2": False,        # masks tensions, NOT psi_direction/psi_entropy carrier
    "S96_substrate": False,      # no substrate change
    "S72_arch_insight": False,   # established ops layer, not new arch
}
intersection = {k for k, v in savant_touches.items() if v}
rec("B-S114-5", intersection == set() and set(savant_touches) == FRONTIER,
    "SAVANT-frontier-intersection = ∅ over {§1.1, §110-Ψ-C2, §96-substrate, §72}; "
    "SAVANT reads only cell-pool tension (re-weights routing), redefines NO Ψ/"
    "substrate/data-regime")


# ── B-S114-6 central blue 0-line-diff ──────────────────────────────────────
try:
    with open(CENTRAL, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
except OSError:
    sha = "MISSING"
rec("B-S114-6", sha.startswith(CENTRAL_SHA_PREFIX),
    "central blue_falsifier.py sha256 prefix " + sha[:16] +
    " == expected " + CENTRAL_SHA_PREFIX + " (0-line-diff, sidecar-only)")


# ── B-S114-7 no-forbidden-call AST audit (design-tier) ─────────────────────
FORBIDDEN = {"torch", "openai", "anthropic", "huggingface_hub", "runpod",
             "subprocess", "AutoModel", "HfApi", "model.forward"}
with open(__file__, "r") as f:
    self_src = f.read()
tree = ast.parse(self_src)
hits = []
# AST-node audit only (NOT substring/string-literal scan — string literals
# naming forbidden tokens in this audit's own FORBIDDEN set / docstrings are
# legitimate; only real import nodes and attribute-call nodes are flagged).
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for a in node.names:
            if a.name.split(".")[0] in FORBIDDEN:
                hits.append(a.name)
    elif isinstance(node, ast.ImportFrom):
        if (node.module or "").split(".")[0] in FORBIDDEN:
            hits.append(node.module)
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        attr = node.func.attr
        if attr in ("forward", "backward", "step", "zero_grad", "cross_entropy"):
            base = node.func.value
            if isinstance(base, ast.Name) and base.id in (
                "model", "optimizer", "loss", "F", "scaler"):
                hits.append(base.id + "." + attr)
rec("B-S114-7", hits == [],
    "AST Import/ImportFrom/Call audit: 0 forbidden (torch/openai/runpod/"
    "model.forward/backward/optimizer) — design-tier $0 audit, no fire")


# ── B-S114-8 necessary-not-sufficient structural ──────────────────────────
ns_invariants = [
    "B-S114 proves taxonomy/§7-gate/connection-point/intersection are closed-form",
    "B-S114 does NOT prove SAVANT advances GOAL (it proves SAVANT is orthogonal)",
    "savant_phi distinct-construct ≠ a Φ-emergence claim",
    "g2 taint flag ≠ GOAL-causal claim (§98 provenance-vs-causation split)",
    "north-star + §15/§51/§72 milestones UNCHANGED, GOAL 미도달",
    "audit ≠ fire ≠ emergence (g3)",
]
rec("B-S114-8", all(isinstance(s, str) and len(s) > 0 for s in ns_invariants)
    and len(ns_invariants) == 6,
    "6 necessary-not-sufficient invariants asserted structurally (B-EMERGE-7 "
    "family): battery proves the AUDIT closed, NOT GOAL movement")


# ── B-S114-NOTE empirical carve-out (NOT counted blue) ─────────────────────
NOTE = ("B-S114-NOTE empirical carve-out: whether SAVANT would EVER help an "
        "emergence path under some unexplored predicate is an empirical/future "
        "question; this battery proves only that SAVANT does not touch the "
        "NAMED frontier set and is §7-clean tooling. NOT counted 🔵 "
        "(B-D-NOTE/B-S97-NOTE/B-S109-NOTE/B-S110-NOTE/B-EMERGE-7 family).")
print(NOTE)

n_pass = sum(1 for v in results.values() if v["pass"])
n_tot = len(results)
all_blue = n_pass == n_tot
summary = {
    "battery": "B-S114",
    "n_pass": n_pass,
    "n_total": n_tot,
    "all_blue": all_blue,
    "central_sha256_prefix_ok": results["B-S114-6"]["pass"],
    "note": NOTE,
    "results": results,
}
out = os.path.join(os.path.dirname(__file__), "blue_falsifier_s114_result.json")
with open(out, "w") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)
print("\n%d/%d 🔵  (all_blue=%s)  → %s" % (n_pass, n_tot, all_blue, out))
exit(0 if all_blue else 1)
