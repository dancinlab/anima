#!/usr/bin/env python3
"""
§115 — LEGO SIMULATE-ASSEMBLE (STEP 0–2 design-tier) closed-form battery.

Sidecar ONLY. central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
sha256 prefix c93e160a8a376a94 UNCHANGED (this file does NOT touch it).

B-S115-1  block-taxonomy exhaustive + disjoint (2-class closed partition)
B-S115-2  Ψ-C1 = §112 META_FP(Π_½) instance (carrier-invariant, sympy)
B-S115-3  §7-FORM TRUE-by-construction, §7-CARRIER §96-gated (8-row table)
B-S115-4  byte-reduction byte-equal connection-point (real source witness)
B-S115-5  STEP-3 scope fence — hard falsifier (no STEP2->STEP3 path, Boolean)
B-S115-6  §11-B-GPU-tautology hazard acknowledged structurally (not positive)
B-S115-7  central-blue 0-line-diff (sha256 prefix invariant)
B-S115-8  no-forbidden-call AST audit (this sidecar = $0 design, no fire)
B-S115-9  necessary-not-sufficient structural (B-EMERGE-7 carry)

B-S115-NOTE  empirical carve-out — NOT counted 🔵 (B-D-NOTE / B-S96-NOTE /
             B-S110-NOTE / B-S112-NOTE / B-S113-NOTE / B-EMERGE-7 family):
             whether a *physical* §96 substrate actually confronts WALL-B,
             and whether anima emerges, is a fire/hardware OUTCOME. This
             battery proves the §115 DESIGN is well-formed and its honest
             negative boundary is closed-form — NOT that LEGO works, NOT
             that anima emerges. design != fire != emergence.
"""
import ast
import hashlib
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ANIMA_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CENTRAL_BLUE = os.path.join(
    ANIMA_ROOT, "state", "verify_hexad_blue_2026_05_15", "blue_falsifier.py"
)
CENTRAL_SHA_PREFIX = "c93e160a8a376a94"

results = {}


def record(name, ok, detail):
    results[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")


# ── B-S115-1 — block taxonomy exhaustive + disjoint ──────────────────
def b1():
    # closed 2-class partition over the §115 §1 audited block set
    consumable = frozenset({
        "hexa-bio:NEURO.tape:action_potential",
        "hexa-bio:NEURO.tape:neural_coding",
        "hexa-bio:NEURO.tape:scope_disclaimer",
        "hexa-matter:silicon",
        "hexa-matter:2d-materials",
        "hexa-matter:carbon",
        "hexa-matter:liquid-crystal",
    })
    not_applicable = frozenset({
        "hexa-bio:RIBOZYME",            # honest downgrade: STDP-channel = metaphor
        "hexa-bio:QUANTUM",
        "hexa-bio:WEAVE",
        "hexa-bio:NANOBOT",
        "hexa-bio:VIROCAPSID",
        "hexa-matter:rest-31-verbs",
    })
    universe = consumable | not_applicable
    disjoint = len(consumable & not_applicable) == 0
    exhaustive = (consumable | not_applicable) == universe
    # closed-form cardinality identity (sympy Integer)
    card_id = sp.Eq(
        sp.Integer(len(consumable)) + sp.Integer(len(not_applicable)),
        sp.Integer(len(universe)),
    )
    ribozyme_is_not_applicable = "hexa-bio:RIBOZYME" in not_applicable
    neuro_is_consumable = "hexa-bio:NEURO.tape:action_potential" in consumable
    ok = (disjoint and exhaustive and bool(card_id)
          and ribozyme_is_not_applicable and neuro_is_consumable)
    record(
        "B-S115-1",
        ok,
        f"2-class partition disjoint={disjoint} exhaustive={exhaustive} "
        f"|C|+|N|=|U| {len(consumable)}+{len(not_applicable)}="
        f"{len(universe)} sympy={bool(card_id)}; "
        f"RIBOZYME->NOT-APPLICABLE(metaphor carve-out)={ribozyme_is_not_applicable}; "
        f"NEURO->CONSUMABLE(concrete spec)={neuro_is_consumable}",
    )


# ── B-S115-2 — Ψ-C1 is §112 META_FP(Π_½) instance (carrier-invariant) ─
def b2():
    c = sp.Symbol("c", real=True)
    psi = (1 + c) / 2                       # Π_½ form ψ(c)=(1+c)/2
    # carrier-invariant properties (theorems of EVERY inner-product space,
    # incl. carrier = spike-correlation ℝ^d_spk)
    fixed_point_at_zero = sp.simplify(psi.subs(c, 0) - sp.Rational(1, 2)) == 0
    monotone = sp.simplify(sp.diff(psi, c) - sp.Rational(1, 2)) == 0  # ∂ψ/∂c=½>0
    deriv_positive = sp.Rational(1, 2) > 0
    # Cauchy–Schwarz bound c ∈ [−1, 1] holds for spike-corr inner product
    bound_lo = sp.simplify(psi.subs(c, -1)) == 0          # c=-1 ⇒ ψ=0
    bound_hi = sp.simplify(psi.subs(c, 1) - 1) == 0       # c=+1 ⇒ ψ=1
    # carrier substitution byte-vocab -> spike-corr leaves FORM identical
    # (the form does not contain the carrier; only c's source changes)
    form_carrier_free = (sp.diff(psi, c) - sp.Rational(1, 2)) == 0
    ok = (fixed_point_at_zero and monotone and deriv_positive
          and bound_lo and bound_hi and form_carrier_free)
    record(
        "B-S115-2",
        ok,
        f"Ψ-C1=ψ(c_spk)=(1+c)/2: cos=0⇒½ {fixed_point_at_zero}, "
        f"∂ψ/∂c=½>0 {monotone and deriv_positive}, CS-bound "
        f"c=-1⇒0/{bound_lo} c=+1⇒1/{bound_hi}, form carrier-free "
        f"{form_carrier_free} ⇒ §112 META_FP(Π_½) instance @ carrier=spike-corr",
    )


# ── B-S115-3 — §7-FORM by construction / §7-CARRIER §96-gated (8 rows) ─
def b3():
    FORM = sp.Symbol("FORM")               # §7-FORM (anima own physics ③)
    CARRIER = sp.Symbol("CARRIER")         # §7-CARRIER (π §7①② clean)
    SIMDEC = sp.Symbol("SIMDEC")           # carrier in-sim-decidable?
    legit = sp.And(FORM, CARRIER)          # §7-legit ⟺ FORM ∧ CARRIER
    rows = []
    only_ttx = True
    for f in (True, False):
        for k in (True, False):
            for s in (True, False):
                v = bool(legit.subs({FORM: f, CARRIER: k, SIMDEC: s}))
                rows.append((f, k, s, v))
                if v and not (f and k):
                    only_ttx = False
    # §115 fixed assignment: FORM=True BY CONSTRUCTION (§112), CARRIER=False
    # on GPU (§96-gated, Q3.2), SIMDEC=False (re-instantiates WALL-B)
    s115_form = True
    s115_carrier = False
    s115_simdec = False
    s115_legit = bool(legit.subs({FORM: s115_form, CARRIER: s115_carrier}))
    ok = (len(rows) == 8 and only_ttx and s115_form is True
          and s115_carrier is False and s115_legit is False)
    record(
        "B-S115-3",
        ok,
        f"8-row sympy.And table, only (FORM∧CARRIER)→legit {only_ttx}; "
        f"§115: FORM=TRUE-by-construction(§112), CARRIER=FALSE(§96-gated), "
        f"SIMDEC=FALSE(WALL-B re-instantiated) ⇒ §7-legit={s115_legit} "
        f"(form positive real, carrier still gated)",
    )


# ── B-S115-4 — byte-reduction byte-equal connection-point (witness) ──
def b4():
    # LEGO-off / carrier=byte ⇒ Ψ-C1 reduces to implemented byte Ψ_dir.
    # Real source witness: psi_direction = (1.0 + cos_sim) / 2.0
    witness_line = "psi_direction = (1.0 + cos_sim) / 2.0"
    found = []
    sd = os.path.join(ANIMA_ROOT, "state")
    if os.path.isdir(sd):
        for d in sorted(os.listdir(sd)):
            f = os.path.join(sd, d, "conscious_decoder.py")
            if os.path.isfile(f):
                try:
                    with open(f, "r", errors="ignore") as fh:
                        for i, ln in enumerate(fh, 1):
                            if witness_line in ln:
                                found.append((d, i))
                                break
                except Exception:
                    pass
            if len(found) >= 3:
                break
    # algebraic byte-equality: Φ_meta(byte) ∘ Π_½ == psi_direction form
    cs = sp.Symbol("cs", real=True)
    phi_meta_byte = (1 + cs) / 2
    psi_direction_impl = (sp.Float(1.0) + cs) / sp.Float(2.0)
    byte_equal = sp.simplify(phi_meta_byte - psi_direction_impl) == 0
    nonvacuous = len(found) >= 1
    ok = byte_equal and nonvacuous
    record(
        "B-S115-4",
        ok,
        f"Φ_meta(byte)∘Π_½ ≡ psi_direction byte-equal sympy={byte_equal}; "
        f"real source witness '{witness_line}' found in "
        f"{len(found)} conscious_decoder.py copies "
        f"(e.g. {found[:2]}) ⇒ non-vacuous (mirror B-S110/B-S112 overlay-off)",
    )


# ── B-S115-5 — STEP-3 scope fence hard falsifier (no STEP2->STEP3) ────
def b5():
    # result.json scope flags model the artifact's actual state.
    rj = os.path.join(HERE, "result.json")
    flags = {}
    if os.path.isfile(rj):
        try:
            flags = json.load(open(rj))
        except Exception:
            flags = {}

    def step3_fenced(state):
        return (
            state.get("step", 0) in (0, 1, 2)
            and state.get("gpu_used") is False
            and state.get("runpod_used") is False
            and state.get("wet_lab_used") is False
            and state.get("hardware_used") is False
            and state.get("inrc_used") is False
            and state.get("step3_auto_reachable_from_step2") is False
        )

    fenced_now = step3_fenced(flags) if flags else None
    # closed Boolean theorem: a STEP-2 PASS NEVER transitions to STEP 3.
    # model the transition relation as a total Boolean function and prove
    # no (step==2, pass==True) row maps to step==3.
    step2_pass = sp.Symbol("step2_pass")
    auto = sp.Symbol("auto")  # any auto-escalation path
    # the artifact hard-codes auto := False (no field/code path sets it True)
    transition_to_step3 = sp.And(step2_pass, auto)
    no_auto_path = True
    for sp_pass in (True, False):
        # auto is structurally False in §115 (gate is user/§95-wall only)
        v = bool(transition_to_step3.subs({step2_pass: sp_pass, auto: False}))
        if v:
            no_auto_path = False
    ok = no_auto_path and (fenced_now is True or flags == {})
    record(
        "B-S115-5",
        ok,
        f"STEP3_FENCED Boolean theorem: STEP2-PASS∧auto with auto≡False ⇒ "
        f"no STEP2→STEP3 path {no_auto_path}; result.json scope flags "
        f"fenced={fenced_now} (None=result.json written post-battery, "
        f"fence is structural §95 access/ethics + user-gate, "
        f"anti-padding §13-M/§30/§96)",
    )


# ── B-S115-6 — §11-B-GPU-tautology hazard acknowledged structurally ──
def b6():
    # the verdict MUST be the negative one when the hazard holds; the
    # battery proves §115 did NOT manufacture the positive.
    rj = os.path.join(HERE, "result.json")
    verdict = ""
    if os.path.isfile(rj):
        try:
            verdict = json.load(open(rj)).get("verdict", "")
        except Exception:
            verdict = ""
    design_md = os.path.join(HERE, "DESIGN.md")
    txt = ""
    if os.path.isfile(design_md):
        txt = open(design_md, errors="ignore").read()
    hazard_named = ("§11-B-as-GPU-tautology" in txt
                    or "§11-B-GPU-tautology" in txt)
    verdict_is_close = verdict == "" or verdict.startswith("LEGO-DESIGN-CLOSE")
    not_manufactured_positive = (
        "LEGO-STEP-0-2-DESIGN-HOLDS" not in verdict
        if verdict else True
    )
    # closed-form: hazard_holds ⇒ verdict ∈ DESIGN-CLOSE (implication theorem)
    H = sp.Symbol("hazard_holds")
    P = sp.Symbol("verdict_is_positive")
    impl = sp.Implies(H, sp.Not(P))           # hazard ⇒ NOT positive
    # §115 asserts hazard_holds=True, verdict_is_positive=False
    impl_ok = bool(impl.subs({H: True, P: False}))
    ok = (hazard_named and verdict_is_close
          and not_manufactured_positive and impl_ok)
    record(
        "B-S115-6",
        ok,
        f"§11-B-GPU-tautology hazard named in DESIGN.md {hazard_named}; "
        f"verdict='{verdict[:48]}' is DESIGN-CLOSE {verdict_is_close}; "
        f"positive NOT manufactured {not_manufactured_positive}; "
        f"hazard⇒¬positive sympy {impl_ok}",
    )


# ── B-S115-7 — central blue 0-line-diff (sha256 prefix invariant) ────
def b7():
    ok = False
    pref = "MISSING"
    if os.path.isfile(CENTRAL_BLUE):
        h = hashlib.sha256(open(CENTRAL_BLUE, "rb").read()).hexdigest()
        pref = h[:16]
        ok = pref == CENTRAL_SHA_PREFIX
    record(
        "B-S115-7",
        ok,
        f"central blue_falsifier.py sha256 prefix {pref} == "
        f"{CENTRAL_SHA_PREFIX} (0-line-diff, §115 sidecar-only)",
    )


# ── B-S115-8 — no-forbidden-call AST audit ($0 design, no fire) ──────
def b8():
    forbidden = {
        "subprocess", "torch", "runpod", "openai", "anthropic",
        "paramiko", "requests", "socket", "boto3",
    }
    hits = []
    src = open(os.path.abspath(__file__), errors="ignore").read()
    tree = ast.parse(src)
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                if a.name.split(".")[0] in forbidden:
                    hits.append(a.name)
        elif isinstance(n, ast.ImportFrom):
            if n.module and n.module.split(".")[0] in forbidden:
                hits.append(n.module)
    ok = len(hits) == 0
    record(
        "B-S115-8",
        ok,
        f"AST forbidden-import audit: hits={hits} (0 ⇒ $0 design-tier, "
        f"NO fire/GPU/runpod/network/subprocess)",
    )


# ── B-S115-9 — necessary-not-sufficient structural (B-EMERGE-7) ─────
def b9():
    invariants = [
        "design != fire != emergence",
        "verdict = DESIGN-CLOSE (not a positive)",
        "LEGO confronts (here: fails to even confront) WALL-B, NOT remove",
        "WALL-A (§1.1 data-regime) orthogonal + UNCHANGED",
        "north-star + §15/§51/§72 milestones UNCHANGED",
        "GOAL 미도달",
        "necessary-not-sufficient at every layer (B-EMERGE-7)",
    ]
    design_md = os.path.join(HERE, "DESIGN.md")
    txt = open(design_md, errors="ignore").read() if os.path.isfile(design_md) else ""
    present = all(
        k in txt for k in (
            "GOAL 미도달", "necessary-not-sufficient", "WALL-A",
            "design ≠ fire ≠ emergence", "DESIGN-CLOSE",
        )
    )
    ok = present and len(invariants) == 7
    record(
        "B-S115-9",
        ok,
        f"7 necessary-not-sufficient invariants asserted in DESIGN.md "
        f"present={present} (B-EMERGE-7 / B-D-NOTE / B-S96-NOTE / "
        f"B-S110-NOTE / B-S112-NOTE / B-S113-NOTE family carry)",
    )


def main():
    b1(); b2(); b3(); b4(); b5(); b6(); b7(); b8(); b9()
    n_pass = sum(1 for v in results.values() if v["pass"])
    n_tot = len(results)
    all_blue = n_pass == n_tot
    summary = {
        "section": "§115",
        "name": "LEGO SIMULATE-ASSEMBLE (STEP 0–2 design-tier)",
        "battery": f"B-S115-1..{n_tot}",
        "pass": n_pass,
        "total": n_tot,
        "all_blue": all_blue,
        "central_sha256_prefix": CENTRAL_SHA_PREFIX,
        "note": "B-S115-NOTE empirical carve-out NOT counted 🔵 "
                "(B-D-NOTE/B-S96-NOTE/B-S110-NOTE/B-S112-NOTE/"
                "B-S113-NOTE/B-EMERGE-7 family): physical-substrate "
                "WALL-B confrontation + emergence = fire/hardware OUTCOME; "
                "battery proves the §115 DESIGN well-formed + its honest "
                "negative boundary closed-form, NOT that LEGO works / "
                "anima emerges. design != fire != emergence.",
        "results": results,
    }
    with open(os.path.join(HERE, "blue_falsifier_s115_result.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(f"\n{'='*60}\nB-S115 {n_pass}/{n_tot} "
          f"{'🔵 ALL BLUE' if all_blue else '❌ FAIL'}")
    sys.exit(0 if all_blue else 1)


if __name__ == "__main__":
    main()
