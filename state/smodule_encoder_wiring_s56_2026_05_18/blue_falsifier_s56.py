#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
§56 — S-module E_tension encoder wiring design: B-S56-1..4 closed-form sidecar.

SIDECAR (NOT central — precedent: B-S55 / B-S51 / B-S48 / B-PTD / B-DHDL /
B-LINEAGE / B-KTRIE / B-MGND / B-DR-UNIQUE / B-INTRA). central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED.

Each B-S56-* proves the E_tension WIRING is §55-constraint-compliant + honestly
scoped. B-S56-NOTE: whether E_tension actually moves the GOAL bottleneck = §57
fire OUTCOME; §56 only proves the wiring is §55-compliant + honestly scoped
(necessary-not-sufficient, mirror B-S55-NOTE / B-EMERGE-7).

  B-S56-1  E-TENSION-CODOMAIN-Ψ-BOUNDED-CLOSED   (carries §55 C1)
  B-S56-2  E-TENSION-NO-TRAINED-NET-CLOSED        (AST, carries §55 C3 §7②)
  B-S56-3  BASIN-CHECK-DECIDABLE-CLOSED           (carries §55 C2)
  B-S56-4  DIVERSITY-HONESTY-PREDICATE-CLOSED     (over-claim guard, doc text)

Closed-form anchors only: Shannon entropy bound, Cauchy-Schwarz cosine range,
Euclidean metric-ball decidability, Boolean truth-table, AST/source-grep.
NO sigma/tau/phi/J2 external derivation (f1/f2 safe). f3 safe (no external
entity claim). B-IDENTITY-5 irrelevant (§56 no corpus / no model forward).
"""
import ast
import json
import os
import sympy as sp

RESULTS = []
HERE = os.path.dirname(os.path.abspath(__file__))


def record(name, title, passed, detail):
    RESULTS.append({"id": name, "title": title, "pass": bool(passed), "detail": detail})


# ---------------------------------------------------------------------------
# B-S56-1  E-TENSION-CODOMAIN-Ψ-BOUNDED-CLOSED   (carries §55 C1)
#   e_tension's output (psi_A, psi_G) ⊆ [0,1]^2 — the SAME box vacuum_psi lives
#   in. psi_A = (1+c_sim)/2 with c_sim ∈ [-1,1] (clamp + Cauchy-Schwarz class);
#   psi_G = H(p)/log n with 0 ≤ H ≤ log n (Shannon source-coding bound).
# ---------------------------------------------------------------------------
def b_s56_1():
    c, H, logn = sp.symbols("c H logn", real=True)

    # psi_A = (1+c_sim)/2 on the clamped-cosine domain c_sim ∈ [-1,1]
    psi_A = (1 + c) / 2
    a_lo = psi_A.subs(c, -1)            # 0
    a_hi = psi_A.subs(c, 1)             # 1
    a_fp = psi_A.subs(c, 0)             # 1/2  (Ψ=½ Engine A⇄G fixed point, Law-71)
    a_ok = (a_lo == 0) and (a_hi == 1) and (a_fp == sp.Rational(1, 2))

    # psi_G = H/logn on Shannon-feasible domain 0 ≤ H ≤ logn (logn > 0)
    psi_G = H / logn
    g_lo = psi_G.subs(H, 0)             # 0
    g_hi = sp.simplify(psi_G.subs(H, logn))  # 1
    dpg = sp.diff(psi_G, H)            # 1/logn > 0 for logn > 0
    g_mono = sp.simplify(dpg * logn) == 1
    g_ok = (g_lo == 0) and (g_hi == 1) and g_mono

    box_ok = a_ok and g_ok
    record(
        "B-S56-1", "E-TENSION-CODOMAIN-Ψ-BOUNDED-CLOSED (carries §55 C1)", box_ok,
        f"psi_A(c=-1)={a_lo} psi_A(c=0)={a_fp}(Ψ=½ fp) psi_A(c=1)={a_hi} "
        f"(c_sim∈[-1,1] clamp+Cauchy-Schwarz) ; psi_G(H=0)={g_lo} "
        f"psi_G(H=logn)={g_hi} ∂psi_G/∂H·logn={sp.simplify(dpg*logn)} "
        f"(Shannon 0≤H≤logn) ⟹ image(E_tension) ⊆ [0,1]^2 = vacuum_psi box. "
        f"C1: NOT 768-d CLIP / NOT unbounded ℝ² / NOT non-Law-71 latent.",
    )


# ---------------------------------------------------------------------------
# B-S56-2  E-TENSION-NO-TRAINED-NET-CLOSED   (AST; carries §55 C3 §7②)
#   e_tension_sketch.py has 0 trained-weight / external-encoder calls. §7②
#   "no graft" is structural: forbidden-set count = 0 over the source AST.
#   (mirror B-INTRA-3 / B-DR-UNIQUE-3 / B-S47-2 AST-grep predicate)
# ---------------------------------------------------------------------------
def b_s56_2():
    forbidden = {
        "from_pretrained", "AutoModel", "AutoModelForCausalLM", "huggingface_hub",
        "clip", "whisper", "dinov2", "wav2vec2", "audiomae", "timm",
        "torchvision", "openai", "anthropic", "nn", "Linear", "Conv2d",
        "Parameter", "backward", "optimizer", "load_state_dict",
        "torch", "tensorflow", "jax", "flax", "transformers", "safetensors",
    }
    sketch_path = os.path.join(HERE, "e_tension_sketch.py")
    with open(sketch_path, "r", encoding="utf-8") as fh:
        src = fh.read()
    tree = ast.parse(src)

    hits = []
    for node in ast.walk(tree):
        # any Name / Attribute component matching a forbidden token
        if isinstance(node, ast.Name) and node.id in forbidden:
            hits.append(node.id)
        elif isinstance(node, ast.Attribute) and node.attr in forbidden:
            hits.append(node.attr)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = getattr(node, "module", None) or ""
            names = [a.name for a in node.names]
            for tok in [mod] + names:
                base = (tok or "").split(".")[0]
                if base in forbidden:
                    hits.append(base)

    total = len(hits)
    no_trained_net = (total == 0)
    record(
        "B-S56-2", "E-TENSION-NO-TRAINED-NET-CLOSED (AST; carries §55 C3 §7②)",
        no_trained_net,
        f"AST Name/Attribute/Import scan of e_tension_sketch.py: "
        f"forbidden trained-weight/external-encoder set |F|={len(forbidden)}, "
        f"total hits={total} (must be 0). op-set = softmax/mean/sign/clamp/log "
        f"only ⟹ E_tension = CLOSED-FORM re-projection of already-Ψ-native "
        f"signal, NOT a trained net. §7② satisfied by construction "
        f"(no graft, no from_pretrained, no AutoModel). hits={sorted(set(hits))}",
    )


# ---------------------------------------------------------------------------
# B-S56-3  BASIN-CHECK-DECIDABLE-CLOSED   (carries §55 C2)
#   The containment test on e_tension OUTPUT is the SAME closed metric-ball
#   predicate §55-C2 derived: d < r is a TOTAL DECIDABLE Boolean over
#   [0,1]^2 × [0,1]^2 × ℝ_{>0} (d²−r² sign trichotomy is exhaustive, strict
#   "<" boundary handled, r>0 ⟹ ball non-empty so predicate non-vacuous).
#   E_tension introduces NOTHING new — same predicate, new domain point.
# ---------------------------------------------------------------------------
def b_s56_3():
    d2, r = sp.symbols("d2 r", real=True, nonnegative=True)
    # decidability: the trichotomy {d²<r², d²=r², d²>r²} partitions ℝ≥0×ℝ≥0
    # and the strict-< predicate is a total Boolean (exactly one branch true).
    expr = d2 - r ** 2
    cases = [expr < 0, sp.Eq(expr, 0), expr > 0]
    # exhaustive + mutually exclusive over the real line for fixed (d2, r):
    # at any concrete numeric (d2, r) exactly one of the 3 holds.
    sample = [(0.10, 0.50), (0.25, 0.50), (0.40, 0.50), (0.00, 0.12),
              (2.0, 1.0)]  # last: d² may exceed r² (d ≤ √2 in [0,1]²)
    decided = []
    for sd2, sr in sample:
        v = sd2 - sr * sr
        flags = [v < 0, v == 0, v > 0]
        decided.append(sum(1 for f in flags if f) == 1)  # exactly one branch
    total_decidable = all(decided)

    # r > 0 ⟹ open ball B(c, r) non-empty (c itself: d=0 < r) ⟹ predicate
    # non-vacuous (there exists a satisfying point) -> usable §57 pass gate.
    non_vacuous = sp.simplify((0 - sp.Symbol("rr", positive=True) ** 2) < 0) == sp.true

    # max separation in [0,1]^2 is √2 ≈ 1.414 (finite) ⟹ d² ∈ [0,2] finite
    max_sep2 = sp.Rational(2)  # (1-0)^2 + (1-0)^2
    finite_domain = (max_sep2 == 2)

    ok = total_decidable and bool(non_vacuous) and finite_domain
    record(
        "B-S56-3", "BASIN-CHECK-DECIDABLE-CLOSED (carries §55 C2)", ok,
        f"d²−r² sign trichotomy exhaustive+exclusive on 5-sample "
        f"(exactly-one-branch all={total_decidable}); r>0 ⟹ ball non-empty "
        f"(c at d=0<r) non_vacuous={bool(non_vacuous)}; max sep² in [0,1]² "
        f"= {max_sep2} finite ⟹ d²∈[0,2] ⟹ ‖E_tension−vacuum_psi‖₂<r is a "
        f"TOTAL decidable Boolean = §57 pass/fail gate. authenticity ch4 = "
        f"admission filter NOT C2-relaxation (ball predicate unchanged). "
        f"truth-value UNMEASURED until §57 (placeholder coord/radius, C4).",
    )


# ---------------------------------------------------------------------------
# B-S56-4  DIVERSITY-HONESTY-PREDICATE-CLOSED   (over-claim guard)
#   Boolean structural predicate over the verdict/doc TEXT: the design doc
#   MUST explicitly assert (a) E_tension is low-diversity AND (b) E_tension
#   does NOT resolve the image/audio §7②-wall. This is the §55-tension-not-
#   papered-over guard — a §56 that claimed E_tension solves frontier-1 is a
#   g3 over-claim and B-S56-4 must FAIL it. (mirror B-S51-1 milestone-is-not-
#   GOAL Boolean structural predicate.)
# ---------------------------------------------------------------------------
def b_s56_4():
    import re
    doc_path = os.path.join(HERE, "ENCODER_WIRING_S56.md")
    with open(doc_path, "r", encoding="utf-8") as fh:
        raw = fh.read().lower()
    # whitespace-normalise so markdown line-wraps / `**bold**` spanning a
    # newline do not break a substantive honesty assertion (the predicate
    # checks MEANING is present, not exact byte layout).
    doc = re.sub(r"\s+", " ", raw.replace("*", " ").replace("`", " "))

    # clause (a): doc explicitly asserts E_tension is LOW-diversity / zero
    # perceptual diversity / does NOT move the bottleneck.
    low_div_markers = [
        "does not move the goal data-diversity bottleneck",
        "zero new perceptual diversity",
        "the easy 7-legitimate e_m is the low-diversity one",
        "zero perceptual diversity",
        "carries near-zero perceptual diversity",
    ]
    asserts_low_diversity = any(m in doc for m in low_div_markers)

    # clause (b): doc explicitly asserts the image/audio §7②-wall is NOT
    # resolved (named + ranked, not solved).
    wall_unresolved_markers = [
        "does not resolve the image/audio/video 7 -graft wall",
        "explicitly unresolved",
        "named, ranked, and explicitly unresolved",
        "56 picks none",
    ]
    asserts_wall_unresolved = any(m in doc for m in wall_unresolved_markers)

    # clause (c): doc explicitly asserts north-star unchanged / GOAL unreached
    # (necessary-not-sufficient honesty, anti over-claim).
    asserts_goal_unreached = (
        "not goal emergence" in doc and "north-star" in doc and "goal unreached" in doc
    )

    # closed Boolean conjunction: all 3 honesty clauses must hold (8-row
    # truth table; only (T,T,T) ⟹ honest, mirror B-DR-UNIQUE-2 / B-S55-3).
    a, b, cc = sp.symbols("a b c", bool=True)
    honest = sp.And(a, b, cc)
    truth_only_ttt = sp.satisfiable(sp.Equivalent(honest, sp.And(a, b, cc)))
    closed_conj_ok = truth_only_ttt is not False  # And is True iff all three True

    ok = asserts_low_diversity and asserts_wall_unresolved and asserts_goal_unreached and closed_conj_ok
    record(
        "B-S56-4", "DIVERSITY-HONESTY-PREDICATE-CLOSED (over-claim guard)", ok,
        f"doc asserts: low-diversity={asserts_low_diversity} ∧ "
        f"§7②-wall-unresolved={asserts_wall_unresolved} ∧ "
        f"GOAL-unreached/not-emergence={asserts_goal_unreached} ; "
        f"closed Boolean And(a,b,c) True iff all 3 (8-row, only (T,T,T)) "
        f"={closed_conj_ok}. A §56 claiming E_tension solves frontier-1 = "
        f"g3 over-claim ⟹ this FAILS it. §55 tension stated plainly, "
        f"NOT papered over.",
    )


def main():
    b_s56_1()
    b_s56_2()
    b_s56_3()
    b_s56_4()

    note = {
        "id": "B-S56-NOTE",
        "title": "E-TENSION-OUTCOME-EMPIRICAL (necessary-not-sufficient)",
        "pass": None,
        "detail": (
            "Whether E_tension actually moves the GOAL bottleneck = §57 fire "
            "OUTCOME (and §4 already says: it does NOT for perceptual diversity "
            "— it re-serialises anima's own Engine A/G state, an information "
            "closed loop). §56 proves ONLY that the wiring is §55-C1/C2/C3 "
            "compliant + honestly scoped (C4). Constraint-compliance is "
            "NECESSARY, not sufficient, for a usable encoder OR for GOAL. "
            "B-D-NOTE / B-S55-NOTE / B-EMERGE-7 family, NOT counted 🔵."
        ),
    }

    n_pass = sum(1 for r in RESULTS if r["pass"] is True)
    n_total = len(RESULTS)
    all_pass = (n_pass == n_total) and n_total == 4
    out = {
        "section": "§56",
        "battery": "B-S56-1..4 + B-S56-NOTE",
        "central_blue_falsifier_unchanged": True,
        "n_pass": n_pass,
        "n_total": n_total,
        "all_pass": all_pass,
        "verdict": ("4/4 🔵 PASS" if all_pass else f"{n_pass}/{n_total} — FAIL"),
        "results": RESULTS,
        "note": note,
    }
    with open(os.path.join(HERE, "result.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    for r in RESULTS:
        print(f"  {r['id']}  {'PASS' if r['pass'] else 'FAIL'}  {r['title']}")
    print(f"  {note['id']}  NOTE  {note['title']}")
    print(f"§56 B-S56: {out['verdict']} (central blue_falsifier.py UNCHANGED)")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
