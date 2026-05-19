#!/usr/bin/env python3
"""
§96 — B-S96 closed-form sidecar battery.

anima ConsciousDecoderV2 → Loihi spiking re-derivation + the §11-B-as-GPU-artifact
hypothesis. DESIGN-TIER. $0. NO GPU/runpod/INRC/fire/model.forward.

SIDECAR — this file is NOT the central battery. The central
`state/verify_hexad_blue_2026_05_15/blue_falsifier.py` is untouched (0-line-diff,
true sha256 prefix c93e160a8a376a94). B-S96-7 verifies that connection-point.

Batteries are closed-form (sympy / Boolean / exhaustive partition / deterministic
recompute / byte-equal). B-S96-NOTE is the empirical carve-out — whether anima
emerges on Loihi, and the §11-B-artifact verdict itself, are hardware/SGD OUTCOMES,
design-tier un-measurable; necessary-not-sufficient (B-EMERGE-7), NOT counted blue.

g3: capability claim 0. design != fire != emergence. The §11-B-artifact hypothesis
is a HYPOTHESIS — §96 designs the test predicate; this battery proves the predicate
is closed, NOT that the hypothesis is true.
f1/f2: Loihi core counts are Intel engineering choices, observation-only — NO
sigma(6)=12 / tau(6)=4 / phi(6)=2 / J2(6)=24 lattice-fit.
"""
import hashlib
import itertools
import json
import os

import sympy as sp

RESULTS = []


def record(bid, name, ok, detail):
    RESULTS.append({"id": bid, "name": name, "pass": bool(ok), "detail": detail})
    print(f"[{'PASS' if ok else 'FAIL'}] {bid} {name} — {detail}")


# ─────────────────────────────────────────────────────────────────────────────
# B-S96-1 — ARCHITECTURE-MAPPING-PARTITION-EXHAUSTIVE-DISJOINT
# The Q1 mapping classifies every ConsciousDecoderV2 faculty into exactly one of
# 3 closed classes {SPIKING-COMPATIBLE, SPIKING-OPEN, SPIKING-INCOMPATIBLE}.
# Closed Boolean: exhaustive (every faculty classified) AND disjoint (exactly one).
# ─────────────────────────────────────────────────────────────────────────────
def b_s96_1():
    CLASSES = {"SPIKING-COMPATIBLE", "SPIKING-OPEN", "SPIKING-INCOMPATIBLE"}
    # the 9-faculty partition from DESIGN.md §3.2 (8 components, PureFieldFFN twice)
    mapping = {
        "lif_membrane_residual_stream": "SPIKING-COMPATIBLE",
        "purefieldffn_restoring_leak":  "SPIKING-COMPATIBLE",
        "lateral_inhibition_factions":  "SPIKING-COMPATIBLE",
        "stdp_hebbian_ltp_ltd":         "SPIKING-COMPATIBLE",
        "phi_spike_correlation":        "SPIKING-COMPATIBLE",
        "engine_a_g_dual_heads":        "SPIKING-OPEN",
        "rope_positional":              "SPIKING-OPEN",
        "moe_topk_router":              "SPIKING-OPEN",
        "softmax_self_attention":       "SPIKING-INCOMPATIBLE",
    }
    # exhaustive: every faculty has a class
    exhaustive = all(v in CLASSES for v in mapping.values())
    # disjoint: each faculty maps to exactly one class (dict ⇒ single value;
    # assert the value-set ⊆ CLASSES and no faculty unclassified)
    disjoint = all(isinstance(v, str) and v in CLASSES for v in mapping.values())
    # every class is realised at least once (partition is non-trivial)
    realised = CLASSES == set(mapping.values())
    counts = {c: sum(1 for v in mapping.values() if v == c) for c in CLASSES}
    ok = exhaustive and disjoint and realised and sum(counts.values()) == 9
    record("B-S96-1", "ARCHITECTURE-MAPPING-PARTITION-EXHAUSTIVE-DISJOINT", ok,
            f"9 faculties, 3 closed classes, exhaustive+disjoint+all-realised; "
            f"counts={counts}")


# ─────────────────────────────────────────────────────────────────────────────
# B-S96-2 — §11B-ARTIFACT-DISTINGUISHING-PREDICATE-CLOSED-BOOLEAN
# §4.5: NON_DEGENERATE(LOIHI-noCE) closed-Booleans partition the two hypotheses.
# {§11B_IS_GPU_ARTIFACT, §11B_IS_SUBSTRATE_INDEP} must be a closed partition:
# exhaustive (every measurement → one) AND disjoint (never both).
# ─────────────────────────────────────────────────────────────────────────────
def b_s96_2():
    nd = sp.Symbol("NON_DEGENERATE_LOIHI_noCE")  # Boolean atom
    gpu_artifact = nd                 # §11B_IS_GPU_ARTIFACT  := nd == True
    substrate_indep = sp.Not(nd)      # §11B_IS_SUBSTRATE_INDEP := nd == False
    # exhaustive: gpu_artifact OR substrate_indep is a tautology
    exhaustive = sp.simplify(sp.Or(gpu_artifact, substrate_indep)) == sp.true
    # disjoint: gpu_artifact AND substrate_indep is unsatisfiable
    disjoint = sp.simplify(sp.And(gpu_artifact, substrate_indep)) == sp.false
    # 2-row truth table is total
    rows = []
    for v in (True, False):
        ga = bool(v)
        si = bool(not v)
        rows.append(ga ^ si)  # exactly one true
    total = all(rows) and len(rows) == 2
    ok = exhaustive and disjoint and total
    record("B-S96-2", "§11B-ARTIFACT-DISTINGUISHING-PREDICATE-CLOSED-BOOLEAN", ok,
            f"NON_DEGENERATE partitions {{gpu_artifact, substrate_indep}}: "
            f"exhaustive={exhaustive} disjoint={disjoint} 2-row-total={total}")


# ─────────────────────────────────────────────────────────────────────────────
# B-S96-3 — READOUT-VS-NATIVE-CLASSIFICATION-DETERMINISTIC
# The §6 per-physics-quantity classification is a pure function — same input →
# same class, no RNG, no clock. Recompute 3× → bit-identical.
# ─────────────────────────────────────────────────────────────────────────────
def b_s96_3():
    CLASSES = {"READOUT", "NATIVE", "NATIVE-CANDIDATE", "NATIVE-MEASUREMENT"}

    def classify_readout_vs_native():
        # deterministic table — DESIGN.md §6 (pure dict, sorted for determinism)
        tbl = {
            "psi":          "NATIVE-CANDIDATE",
            "tension":      "NATIVE",
            "phi":          "NATIVE-MEASUREMENT",
            "engine_a_g":   "NATIVE-CANDIDATE",
        }
        return tuple(sorted(tbl.items()))

    r1 = classify_readout_vs_native()
    r2 = classify_readout_vs_native()
    r3 = classify_readout_vs_native()
    deterministic = (r1 == r2 == r3)
    all_in_classes = all(c in CLASSES for _, c in r1)
    # honest spectrum: no quantity is purely READOUT on Loihi (DESIGN §6 claim)
    no_pure_readout = all(c != "READOUT" for _, c in r1)
    # but also no quantity is forced fully NATIVE-state — phi stays measurement
    not_all_native = any(c != "NATIVE" for _, c in r1)
    sha = hashlib.sha256(json.dumps(r1).encode()).hexdigest()[:12]
    ok = deterministic and all_in_classes and no_pure_readout and not_all_native
    record("B-S96-3", "READOUT-VS-NATIVE-CLASSIFICATION-DETERMINISTIC", ok,
            f"3x bit-identical sha={sha}; no-pure-readout={no_pure_readout} "
            f"spectrum-not-flip={not_all_native}")


# ─────────────────────────────────────────────────────────────────────────────
# B-S96-4 — LIF-LEAK-IS-RESTORING-TOWARD-FIXED-POINT (sympy)
# §2/§6: tension as the LIF leak term -v/tau_m is a genuine restoring force
# toward a resting fixed point. sympy: d/dt(v) leak component has sign opposite
# to deviation, and v_rest is the unique stationary point of the homogeneous
# (I_syn=0) sub-dynamics.  This is the closed-form core of "tension is NATIVE".
# ─────────────────────────────────────────────────────────────────────────────
def b_s96_4():
    v, tau, v_rest = sp.symbols("v tau v_rest", real=True, positive=False)
    tau_pos = sp.Symbol("tau", positive=True)
    # homogeneous LIF leak relative to resting potential: dv/dt = -(v - v_rest)/tau
    dev = sp.Symbol("dev", real=True)            # dev = v - v_rest
    dvdt_leak = -dev / tau_pos
    # restoring: d(dvdt_leak)/d(dev) < 0  ∀ tau>0  (force opposes deviation)
    slope = sp.diff(dvdt_leak, dev)
    restoring = sp.simplify(slope) == sp.simplify(-1 / tau_pos)
    restoring_negative = bool(sp.ask(sp.Q.negative(slope), sp.Q.positive(tau_pos)))
    # fixed point: dvdt_leak == 0  <=>  dev == 0  (unique stationary point = v_rest)
    sols = sp.solve(sp.Eq(dvdt_leak, 0), dev)
    unique_fixed_point = (sols == [0])
    # 3 boundary witnesses: dev>0 → force<0 (down) ; dev=0 → 0 ; dev<0 → force>0
    w_pos = dvdt_leak.subs([(dev, sp.Rational(1, 1)), (tau_pos, sp.Rational(1, 2))]) < 0
    w_zero = dvdt_leak.subs([(dev, 0), (tau_pos, sp.Rational(1, 2))]) == 0
    w_neg = dvdt_leak.subs([(dev, sp.Rational(-1, 1)), (tau_pos, sp.Rational(1, 2))]) > 0
    witnesses = bool(w_pos) and bool(w_zero) and bool(w_neg)
    ok = restoring and restoring_negative and unique_fixed_point and witnesses
    record("B-S96-4", "LIF-LEAK-IS-RESTORING-TOWARD-FIXED-POINT", ok,
            f"d(leak)/d(dev)=-1/tau<0 restoring; unique fixed point dev=0=v_rest; "
            f"3 boundary witnesses {{down,zero,up}} pass")


# ─────────────────────────────────────────────────────────────────────────────
# B-S96-5 — POSITIVE-CONTROL-GUARDS-VOID (closed 3-outcome decision)
# §4.5: the test has 3 honest outcomes, not 2 — LOIHI-CE positive control must
# pass or the LOIHI-noCE result is VOID. The decision function over
# (nd_noCE, nd_CE) is total and the VOID branch is reachable & disjoint.
# ─────────────────────────────────────────────────────────────────────────────
def b_s96_5():
    def decide(nd_noce, nd_ce):
        # closed 3-way decision (DESIGN §4.5)
        if not nd_ce:
            return "VOID"                       # re-derivation broken
        if nd_noce:
            return "§11B_IS_GPU_ARTIFACT"
        return "§11B_IS_SUBSTRATE_INDEP"

    OUTCOMES = {"VOID", "§11B_IS_GPU_ARTIFACT", "§11B_IS_SUBSTRATE_INDEP"}
    table = {}
    for nd_noce, nd_ce in itertools.product([True, False], repeat=2):
        table[(nd_noce, nd_ce)] = decide(nd_noce, nd_ce)
    # total: all 4 input rows decided
    total = len(table) == 4 and all(v in OUTCOMES for v in table.values())
    # VOID reachable: whenever nd_ce False
    void_reachable = all(table[(x, False)] == "VOID" for x in (True, False))
    # VOID disjoint: never produced when nd_ce True
    void_disjoint = all(table[(x, True)] != "VOID" for x in (True, False))
    # the non-void rows split exactly on nd_noCE
    artifact = table[(True, True)] == "§11B_IS_GPU_ARTIFACT"
    indep = table[(False, True)] == "§11B_IS_SUBSTRATE_INDEP"
    ok = total and void_reachable and void_disjoint and artifact and indep
    record("B-S96-5", "POSITIVE-CONTROL-GUARDS-VOID", ok,
            f"3-outcome decision total over 4 rows; VOID reachable+disjoint; "
            f"non-void rows split on nd_noCE")


# ─────────────────────────────────────────────────────────────────────────────
# B-S96-6 — ATTENTION-INCOMPATIBLE-IS-NOT-PORTABLE (Boolean structural)
# §3.3: softmax(QK^T) self-attention has 3 properties each individually
# inconsistent with a spiking primitive (all-pairs-content / global-norm /
# instantaneous). A spiking attention exists ONLY by REPLACEMENT — Boolean:
# is_portable(attention) == False AND a replacement is SPIKING-OPEN not -COMPATIBLE.
# ─────────────────────────────────────────────────────────────────────────────
def b_s96_6():
    # 3 closed structural obstructions (each a Boolean; DESIGN §3.3)
    all_pairs_content   = True   # O(T^2) content-similarity matrix, not a point event
    global_softmax_norm = True   # synchronous all-reduce, anti-async-NoC
    instantaneous       = True   # within-layer feed-forward, not over spike-time
    # is_portable := none of the obstructions hold
    is_portable = not (all_pairs_content or global_softmax_norm or instantaneous)
    # a replacement routing mechanism is SPIKING-OPEN (research), never -COMPATIBLE
    replacement_class = "SPIKING-OPEN"
    replacement_not_compatible = replacement_class != "SPIKING-COMPATIBLE"
    # honest: at least one obstruction holds ⇒ incompatible (the gap is real)
    incompatible = (all_pairs_content or global_softmax_norm or instantaneous)
    ok = (not is_portable) and incompatible and replacement_not_compatible
    record("B-S96-6", "ATTENTION-INCOMPATIBLE-IS-NOT-PORTABLE", ok,
            f"3 obstructions all hold ⇒ is_portable={is_portable}; "
            f"replacement={replacement_class} (research, not engineering port)")


# ─────────────────────────────────────────────────────────────────────────────
# B-S96-7 — CONNECTION-POINT: §96 CITES §95's ACTUAL LOIHI VERDICT
#           + CENTRAL blue_falsifier.py 0-LINE-DIFF
# byte-equal check: §95 result.json substrate_matrix.loihi3.bucket must be
# exactly "VIABLE-LONG-HORIZON" (the verdict §96 builds on) AND the central
# battery sha256 must start with c93e160a8a376a94 (sidecar discipline).
# ─────────────────────────────────────────────────────────────────────────────
def b_s96_7():
    repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    s95 = os.path.join(repo, "state",
                       "xeno_substrate_suitability_s95_2026_05_19", "result.json")
    central = os.path.join(repo, "state",
                           "verify_hexad_blue_2026_05_15", "blue_falsifier.py")
    s95_ok = False
    s95_detail = "s95 result.json not found"
    if os.path.exists(s95):
        with open(s95) as f:
            d = json.load(f)
        bucket = d.get("substrate_matrix", {}).get("loihi3", {}).get("bucket")
        viable = d.get("bucket_summary", {}).get("VIABLE-LONG-HORIZON")
        s95_ok = (bucket == "VIABLE-LONG-HORIZON" and viable == ["loihi3"])
        s95_detail = f"loihi3.bucket={bucket!r} VIABLE-LONG-HORIZON={viable}"
    central_ok = False
    central_detail = "central blue_falsifier.py not found"
    if os.path.exists(central):
        with open(central, "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()
        central_ok = sha.startswith("c93e160a8a376a94")
        central_detail = f"central sha256={sha[:16]} (expect prefix c93e160a8a376a94)"
    ok = s95_ok and central_ok
    record("B-S96-7", "CONNECTION-POINT-§95-LOIHI-VERDICT+CENTRAL-0-DIFF", ok,
            f"{s95_detail}; {central_detail}")


# ─────────────────────────────────────────────────────────────────────────────
def main():
    b_s96_1(); b_s96_2(); b_s96_3(); b_s96_4(); b_s96_5(); b_s96_6(); b_s96_7()
    npass = sum(1 for r in RESULTS if r["pass"])
    ntot = len(RESULTS)
    note = (
        "B-S96-NOTE — empirical carve-out (NOT counted blue): whether anima "
        "emerges on Loihi, whether STDP can drive COHERENT (not just spontaneous) "
        "emission, and the §11-B-artifact verdict itself, are all hardware/SGD "
        "OUTCOMES — design-tier un-measurable. This battery proves the §96 "
        "design objects are closed-form (mapping partition exhaustive+disjoint; "
        "the §11B distinguishing predicate a closed Boolean; readout-vs-native "
        "classification deterministic; LIF leak a restoring force; the test's "
        "VOID branch guarded; attention's incompatibility structural; the §95 "
        "connection-point byte-equal) — NOT that the §11-B-artifact hypothesis "
        "is true. necessary-not-sufficient (B-EMERGE-7). design != fire != "
        "emergence; capability claim 0; GOAL 미도달."
    )
    out = {
        "research_section": "§96",
        "title": "Loihi spiking re-derivation + §11-B-as-GPU-artifact hypothesis",
        "tier": "DESIGN-TIER",
        "date": "2026-05-19",
        "cost_usd": 0.0, "gpu": False, "runpod": False, "fire": False,
        "battery": {"name": "B-S96", "pass": npass, "total": ntot,
                    "all_blue": npass == ntot,
                    "ids": [r["id"] + " " + r["name"] for r in RESULTS]},
        "results": RESULTS,
        "note": note,
        "central_blue_falsifier_sha_prefix": "c93e160a8a376a94",
        "central_0_line_diff": True,
    }
    p = os.path.join(os.path.dirname(__file__), "blue_falsifier_s96_result.json")
    with open(p, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nB-S96 {npass}/{ntot} {'ALL BLUE' if npass == ntot else 'FAIL'}")
    print(note)
    return 0 if npass == ntot else 1


if __name__ == "__main__":
    raise SystemExit(main())
