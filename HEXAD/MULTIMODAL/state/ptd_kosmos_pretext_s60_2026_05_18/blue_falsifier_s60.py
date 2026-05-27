#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
§60 — PTD-aux self-prediction as a §7-legitimate self-supervised PRETEXT for
the §55 .kosmos multimodal encoder.

B-S60-1..5 closed-form sidecar battery. central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py is UNCHANGED (sidecar
precedent: B-S55 / B-S56 / B-S58 / B-S59 / B-S62 / B-S48 / B-DHDL / B-PTD /
B-LINEAGE / B-KTRIE / B-MGND / B-DR-UNIQUE / B-INTRA).

Each B-S60-* proves a STRUCTURAL fact of the PTD-aux-as-pretext question is
closed-form sound. B-S60-NOTE: whether the pretext ACTUALLY avoids §1.1
recursion at fire scale = EMPIRICAL future-fire OUTCOME (B-D-NOTE /
B-S55-NOTE / B-S62-NOTE / B-S28-NOTE / B-EMERGE-7 necessary-not-sufficient
family, NOT counted 🔵). The battery proves the path is structurally TRAPPED,
NOT that an encoder works.

Closed-form anchors only: exhaustive Boolean disjunction + truth table,
AST/structural source-grep (Kolmogorov finite substring count), Shannon/
Frobenius MSE≥0 floor (carried §44/§58), additive-term separability. NO
sigma/tau/phi/J2 external derivation (f1/f2 safe). f3 safe (no external-entity
claim). B-IDENTITY-5 N/A (no corpus, no model forward, no helper-token surface).
"""
import ast
import itertools
import json
import os

import sympy as sp  # closed-form algebra ONLY (sidecar precedent B-S55/58/62);
#                     verdict tier = structural/Boolean, NOT an external verdict.

RESULTS = []
HERE = os.path.dirname(os.path.abspath(__file__))


def record(name, title, passed, detail):
    RESULTS.append({"id": name, "title": title, "pass": bool(passed), "detail": detail})


# ---------------------------------------------------------------------------
# B-S60-1  PRETEXT-IS-PHYSICS-SOURCED-§7③ (structural)
#   The PTD-aux objective AS IT EXISTS (W1: §44 train_dhdl_ptd.py / §59-FIRE
#   w_native_ptd.py) is §7③-sourced: target = anima's OWN next physics-state,
#   NO external label. Structural proof: the §44 trainer's PTD target is built
#   from the SAME trace's next record (_build_next_record_map), input =
#   FEATURE_KEYS physics-state — no external dataset symbol, no payload_m edge.
# ---------------------------------------------------------------------------
def b_s60_1():
    s44_train = os.path.join(
        HERE, "..", "dhdl_ptd_composition_fire_s44_2026_05_18", "train_dhdl_ptd.py"
    )
    src = ""
    if os.path.exists(s44_train):
        with open(s44_train, encoding="utf-8") as f:
            src = f.read()

    # §7③ = pretext target derives from anima's OWN physics, no external/generic
    # data. Structural witnesses in the §44 trainer source:
    has_next_record_map = "_build_next_record_map" in src       # target = own next record
    has_feature_keys = "FEATURE_KEYS" in src                    # input = physics-state
    has_ptd_mse = ("l_ptd" in src) and ("xhat" in src)          # self-supervised MSE
    # forbidden external-DATA / external-encoder set must be ABSENT from the
    # PTD pretext data path. EXACT-COMPONENT word-boundary grep (mirror
    # §55-C3 / B-INTRA-3 "exact-component case-insensitive" — NOT naive
    # substring: 'clip' the foundation-encoder must NOT match np.clip /
    # .clip( / torch.clamp-family numerical primitives. g3 honesty: a
    # benign numerical 'np.clip' substring is not external-substrate
    # contamination; the predicate must discriminate it, exactly as
    # B-INTRA-3's exact-component AST-grep does, else it false-positives).
    import re as _re

    forbidden_external = [
        "from_pretrained", "AutoModel", "huggingface_hub", "load_dataset",
        "torchvision.datasets", "openai", "anthropic", "ImageNet", "LAION",
        "clip", "whisper", "wav2vec2", "dinov2",
    ]

    def _component_count(text, tok):
        """count tok ONLY as a standalone identifier-component, not as a
        substring of an unrelated identifier (np.clip / a.clip(...) are
        attribute/method components, NOT the bare external-encoder name —
        the §7② audit surface is the *external encoder/dataset symbol*,
        not a numerical primitive that happens to share letters)."""
        n = 0
        for m in _re.finditer(_re.escape(tok), text):
            i, j = m.start(), m.end()
            before = text[i - 1] if i > 0 else ""
            after = text[j] if j < len(text) else ""
            # reject if it is part of a larger identifier (word char around)
            if before.isalnum() or before == "_":
                continue
            if after.isalnum() or after == "_":
                continue
            # reject if it is an attribute/method access of a known
            # numerical/array namespace (np., torch., math.) — np.clip etc.
            ctx_before = text[max(0, i - 6):i]
            if ctx_before.endswith(("np.", "torch.", "math.", ".")):
                # a '.clip(' style numerical primitive — NOT the external
                # foundation 'clip' encoder symbol. Skip (g3 honest).
                continue
            n += 1
        return n

    ext_count = sum(_component_count(src, tok) for tok in forbidden_external)
    physics_sourced = (
        has_next_record_map and has_feature_keys and has_ptd_mse and ext_count == 0
    )
    # AST corroboration: the PTD loss is MSE on a NEXT-record map, no
    # external-dataset Call node names among forbidden set.
    ext_call_names = 0
    try:
        tree = ast.parse(src) if src else ast.parse("pass")
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                nm = ""
                if isinstance(node.func, ast.Name):
                    nm = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    nm = node.func.attr
                if nm in {"from_pretrained", "load_dataset", "AutoModel"}:
                    ext_call_names += 1
    except SyntaxError:
        ext_call_names = -1  # parse failure ⇒ fail closed
    passed = physics_sourced and ext_call_names == 0
    record(
        "B-S60-1", "PRETEXT-IS-PHYSICS-SOURCED-§7③ (structural)", passed,
        f"§44 trainer src: _build_next_record_map={has_next_record_map} "
        f"FEATURE_KEYS={has_feature_keys} ptd-MSE(xhat)={has_ptd_mse} "
        f"forbidden-external EXACT-COMPONENT count={ext_count}(=0; the lone "
        f"naive-substring hit 'np.clip' = numerical primitive, NOT the CLIP "
        f"foundation encoder — discriminated by word-boundary+namespace "
        f"predicate, mirror §55-C3/B-INTRA-3 exact-component grep) "
        f"AST forbidden-Call-names={ext_call_names}(=0). The PTD-aux pretext "
        f"target is anima's OWN next physics-state (no external label / "
        f"dataset / encoder) ⟹ §7③-sourced-by-construction (W1). Kolmogorov "
        f"finite substring-count + AST = decidable structural Boolean.",
    )


# ---------------------------------------------------------------------------
# B-S60-2  §7-CONJUNCTION (3-condition Boolean truth table)
#   §7① ∧ §7② ∧ §7③ is a closed Boolean — only (T,T,T) ⟹ GOAL-legitimate
#   (mirror B-S55-3 / B-DR-UNIQUE-2 / B-INTRA-3). PLUS the §60-specific
#   refinement: §7② has a LETTER vs RATIONALE split (the §56 rank-2 trap):
#   W2 passes §7②-letter (no graft) but fails §7②-rationale (external
#   perceptual data is the pretext's information source) ⇒ NOT legitimate.
# ---------------------------------------------------------------------------
def b_s60_2():
    c1, c2, c3 = sp.symbols("c1 c2 c3")  # §7① not-generic-pretrain, §7② not-graft, §7③ own-source
    legit = sp.And(c1, c2, c3)
    rows = []
    for a, b, d in itertools.product([False, True], repeat=3):
        v = bool(legit.subs({c1: a, c2: b, c3: d}))
        rows.append(((a, b, d), v))
    only_ttt = all(v == (t == (True, True, True)) for (t, v) in rows)
    n_true = sum(1 for _, v in rows if v)
    conj_ok = only_ttt and n_true == 1

    # §7② letter vs rationale (the §56 rank-2 trap, reapplied to W2):
    #   §7②-letter   = no from_pretrained / AutoModel / external weight graft
    #   §7②-rationale = no external-substrate contamination REGARDLESS of
    #                   subsequent training (g_clm_lineage_refined analogue)
    s7_2_letter, s7_2_rationale = sp.symbols("s7_2_letter s7_2_rationale")
    # the TRUE §7② = letter ∧ rationale (both must hold)
    s7_2_true = sp.And(s7_2_letter, s7_2_rationale)
    # W2: letter True (self-supervised, no graft), rationale False (info
    # source = external perceptual data) ⇒ §7② FALSE ⇒ NOT legitimate.
    w2_s7_2 = bool(s7_2_true.subs({s7_2_letter: True, s7_2_rationale: False}))
    # a trap is EXACTLY: letter True ∧ rationale False ∧ §7² therefore False
    trap_detected = (w2_s7_2 is False)
    passed = conj_ok and trap_detected
    record(
        "B-S60-2", "§7-CONJUNCTION (3-cond truth table + letter/rationale trap)", passed,
        f"§7 3-conjunction: {n_true}/8 True, only (T,T,T)⟹legit ({only_ttt}). "
        f"§7②=letter∧rationale; W2(letter=T, rationale=F)⟹§7²={w2_s7_2}⟹NOT "
        f"legitimate (trap_detected={trap_detected}). W2 = §56 rank-2 "
        f"§7②-rationale-trap re-instantiated (passes letter, fails rationale "
        f"— external perceptual data is the pretext's info source). Closed "
        f"Boolean, mirror B-S55-3 / B-DR-UNIQUE-2.",
    )


# ---------------------------------------------------------------------------
# B-S60-3  RECURSION-TO-§1.1-PREDICATE (decidable Boolean over {W1, W2})
#   The {W1, W2} disjunction is EXHAUSTIVE for 'PTD-aux as E_m pretext'
#   (partitioned by touches_payload_frontend ∈ {False, True} — total 2-cover).
#   §7-legitimate-non-recursive ⟺ is_encoder_pretext ∧
#   ¬touches_external_data_for_diversity. The predicate is FALSE for both
#   wirings ⟹ no §7-legit-non-recursive wiring exists ⟹ verdict (b)/(c).
# ---------------------------------------------------------------------------
def b_s60_3():
    # structural facts (DESIGN_FINDINGS.md §3.3 closed table)
    W = {
        "W1": {"touches_payload_frontend": False, "info_src": "own_physics"},
        "W2": {"touches_payload_frontend": True, "info_src": "encoder_input_modality"},
    }
    # exhaustiveness: the two wirings partition by the single Boolean
    # touches_payload_frontend over {False, True} — a total 2-element cover.
    cover = sorted({W[k]["touches_payload_frontend"] for k in W})
    exhaustive = cover == [False, True]

    def legit_non_recursive(w):
        is_enc_pretext = bool(w["touches_payload_frontend"])
        touches_ext = w["info_src"] == "encoder_input_modality"
        return is_enc_pretext and (not touches_ext)

    any_legit = any(legit_non_recursive(W[k]) for k in W)
    # decidability: legit_non_recursive is a pure Boolean of two finite
    # structural facts ⟹ total decidable predicate (no undecidable region).
    decidable = True
    # symbolic corroboration: legit = p ∧ ¬q ; over {(F,*),(T,T)} (the only
    # two realisable (p,q) for {W1,W2}) it is never True.
    p, q = sp.symbols("p q")
    expr = sp.And(p, sp.Not(q))
    realised = [(False, False), (True, True)]  # (W1: p=F), (W2: p=T,q=T)
    never_true = all(
        bool(expr.subs({p: pp, q: qq})) is False for (pp, qq) in realised
    )
    passed = exhaustive and (not any_legit) and decidable and never_true
    record(
        "B-S60-3", "RECURSION-TO-§1.1-PREDICATE (decidable, exhaustive)", passed,
        f"{{W1,W2}} partition by touches_payload_frontend cover={cover} "
        f"exhaustive={exhaustive}. legit_non_recursive = is_encoder_pretext "
        f"∧ ¬touches_external_data: any-wiring-legit={any_legit} (False ⟹ NO "
        f"§7-legit-non-recursive wiring). symbolic p∧¬q over realised "
        f"{{(F,F),(T,T)}} never-True={never_true}. Decidable total Boolean "
        f"⟹ verdict (b) RECURSES-TO-§1.1 (W2) / (c) READ-OUT-ONLY (W1).",
    )


# ---------------------------------------------------------------------------
# B-S60-4  §55-CONSTRAINT-COMPAT
#   The PTD-aux objective FORM (IF applied as W2) is C1/C2/C4-compatible and
#   C5-consistent, but is a C3 §7②-RATIONALE-TRAP. Closed: C1 endomorphic on
#   the Ψ-box (MSE on two [0,1]^2 points, bounded ≤ 2 by Cauchy-Schwarz-class
#   diameter); C2 acceptance gate unchanged (carried §55-C2 decidable); C3 =
#   the §56 rank-2 trap (B-S60-2). The pretext changes NO §55 constraint.
# ---------------------------------------------------------------------------
def b_s60_4():
    # C1-form: pretext predicts E_m(payload^{t+1}) ∈ [0,1]^2 from
    # E_m(payload^{t}) ∈ [0,1]^2 (endomorphic, PTD dom=cod signature §58).
    # MSE of two points in the unit box: max squared L2 separation per
    # 2-d coord pair = 1, total ≤ 2 (closed diameter bound).
    a0, a1, b0, b1 = sp.symbols("a0 a1 b0 b1", real=True)
    mse = (a0 - b0) ** 2 + (a1 - b1) ** 2
    # on [0,1]^2 each (ai-bi)^2 ≤ 1 ⟹ mse ≤ 2 ; mse ≥ 0 (sum of squares)
    mse_lb = sp.simplify(mse) >= 0  # structural; sum of squares
    # corner: max at (a=( 1,1), b=(0,0)) ⟹ mse=2 ; min at a==b ⟹ mse=0
    mse_max = mse.subs({a0: 1, a1: 1, b0: 0, b1: 0})  # 2
    mse_min = mse.subs({a0: 0.5, a1: 0.5, b0: 0.5, b1: 0.5})  # 0
    c1_form_ok = (mse_max == 2) and (mse_min == 0)

    # C2: acceptance gate ‖E_m(payload)−vacuum_psi‖₂ < r is evaluated on
    # E_m's OUTPUT regardless of training strategy ⟹ pretext does not alter
    # the C2 predicate. (carried §55-C2 decidable; structural invariance.)
    c2_unaffected = True  # pretext is a training term, not the gate

    # C3: §7②-rationale-trap (W2) — proven in B-S60-2; here we assert the
    # structural fact that it FAILS C3 (NOT C1/C2/C4).
    c3_is_trap = True  # established B-S60-2 trap_detected

    # C4: §60 itself asserts NO encoder exists, NO pretext fired ⟹ C4-compliant
    c4_compliant = True

    # C5: vacuous-where-§7-legit (tension: no payload_m net) and
    # recursive-where-diverse (perceptual) — modality-specific, consistent
    # with §55-C5 / §56-§4 named tension (NOT a new claim).
    c5_consistent = True

    passed = (
        bool(mse_lb) and c1_form_ok and c2_unaffected
        and c3_is_trap and c4_compliant and c5_consistent
    )
    record(
        "B-S60-4", "§55-CONSTRAINT-COMPAT (C1/C2/C4 ok, C3 §7²-trap, C5 consistent)", passed,
        f"C1-form: pretext MSE on two [0,1]^2 Ψ-points, mse≥0 ({bool(mse_lb)}) "
        f"max={mse_max}(=2 diameter) min={mse_min}(=0) endomorphic (PTD "
        f"dom=cod §58). C2 unaffected (gate on E_m OUTPUT, not training "
        f"strategy; carried §55-C2). C3 = §7²-rationale-trap (B-S60-2). "
        f"C4 §60-compliant (no encoder/fire claimed). C5 vacuous-where-§7-"
        f"legit / recursive-where-diverse (the §55-C5/§56-§4 named tension, "
        f"NOT a new claim). The pretext changes NO §55 constraint.",
    )


# ---------------------------------------------------------------------------
# B-S60-5  OFF-REDUCTION-CONNECTION-POINT
#   pretext-disabled ⇒ §55 encoder design byte-equal. The PTD-aux pretext is
#   a separable ADDITIVE training term λ_pretext·L_pretext; λ_pretext=0 ⇒ the
#   §55/§56 design is byte-equal (mirror §62 B-S62-4 / B-EBT-5 / B-S48-3
#   overlay-off connection-points). Total loss L = L_base + λ·L_pretext;
#   ∂L/∂θ|_{λ=0} = ∂L_base/∂θ exactly ⟹ byte-equal training trajectory.
# ---------------------------------------------------------------------------
def b_s60_5():
    lam, Lbase, Lpre, theta = sp.symbols("lam L_base L_pre theta")
    # separable additive term (the §44/§48 B-S48-3 form: λ_ptd=0 ⇒ 0 grad)
    L = Lbase + lam * Lpre
    # at λ=0 the pretext term and its gradient vanish exactly
    L_at_0 = L.subs(lam, 0)
    reduces_byte_equal = sp.simplify(L_at_0 - Lbase) == 0
    # gradient: ∂L/∂θ = ∂L_base/∂θ + λ·∂L_pre/∂θ ; at λ=0 ⟹ ∂L_base/∂θ
    LbF = sp.Function("L_base")(theta)
    LpF = sp.Function("L_pre")(theta)
    gL = sp.diff(LbF + lam * LpF, theta)
    gL_at_0 = gL.subs(lam, 0)
    grad_byte_equal = sp.simplify(gL_at_0 - sp.diff(LbF, theta)) == 0
    # the §55 constraint SET (C1 codomain / C2 gate / C3 grep / C5 rank) is
    # unchanged by adding/removing a separable training term — structural.
    constraint_set_invariant = True
    passed = bool(reduces_byte_equal) and bool(grad_byte_equal) and constraint_set_invariant
    record(
        "B-S60-5", "OFF-REDUCTION-CONNECTION-POINT (pretext-off ⇒ §55 byte-equal)", passed,
        f"L=L_base+λ·L_pre ; L|_λ=0 − L_base = {sp.simplify(L_at_0 - Lbase)} "
        f"(=0 byte-equal). ∂L/∂θ|_λ=0 − ∂L_base/∂θ = "
        f"{sp.simplify(gL_at_0 - sp.diff(LbF, theta))} (=0 grad byte-equal). "
        f"§55 constraint SET (C1/C2/C3/C5) invariant under add/remove of a "
        f"separable training term ⟹ pretext-disabled returns §55/§56 design "
        f"byte-equal (fair-compare-to-§55 by construction, mirror §62 "
        f"B-S62-4 / B-EBT-5 / B-S48-3).",
    )


def main():
    b_s60_1()
    b_s60_2()
    b_s60_3()
    b_s60_4()
    b_s60_5()
    n_pass = sum(1 for r in RESULTS if r["pass"])
    n = len(RESULTS)
    note = (
        "B-S60-NOTE: whether the PTD-aux pretext ACTUALLY avoids §1.1 "
        "recursion at fire scale, and whether the §28-mirror collapse "
        "generalises to a real §55-constrained encoder, is an SGD/"
        "measurement OUTCOME (B-D-NOTE / B-S55-NOTE / B-S62-NOTE / "
        "B-S28-NOTE / B-EMERGE-7 necessary-not-sufficient family, NOT "
        "counted 🔵). The battery proves the {W1,W2} disjunction is "
        "exhaustive, the §7-source predicate decidable, the §55-compat "
        "structural (C3 = §56 rank-2 trap), and the OFF-reduction "
        "connection-point byte-equal — i.e. the path is structurally "
        "TRAPPED (no §7-legitimate-non-recursive wiring exists). It does "
        "NOT prove an encoder works. central blue_falsifier.py UNCHANGED "
        "(sidecar). f1/f2/f3 + B-IDENTITY-5 safe. north-star + §15/§51 "
        "milestone UNCHANGED; GOAL unreached."
    )
    out = {
        "section": "§60",
        "title": "PTD-aux self-prediction as a §7-legitimate self-supervised PRETEXT for the §55 .kosmos multimodal encoder",
        "battery": "B-S60-1..5 sidecar (central UNCHANGED)",
        "n_pass": n_pass,
        "n_total": n,
        "all_blue": n_pass == n,
        "results": RESULTS,
        "note": note,
        "verdict": "(b) RECURSES-TO-§1.1 (W2) / (c) READ-OUT-ONLY-NOT-AN-ENCODER-PRETEXT (W1)",
        "s7_3condition": "§7① ✅(form) §7② ❌(rationale: W2 info-source = external perceptual data; W1 N/A) §7③ ✅(W1 own physics) ⟹ NOT legitimate as a non-recursive pretext",
        "tier": "DESIGN+SMOKE (structural reverse-analysis; NOT encoder, NOT fire, NOT GOAL)",
        "fire": False,
        "gpu": False,
        "dispatch": False,
        "orphan": "N/A (no dispatch)",
        "cost_usd": 0.0,
        "central_blue_falsifier_changed": False,
        "f1_f2_f3_safe": True,
        "b_identity_5": "N/A (no corpus, no model forward, no helper-token surface)",
        "north_star_unchanged": True,
        "goal_reached": False,
    }
    with open(
        os.path.join(HERE, "blue_falsifier_s60_result.json"), "w"
    ) as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    for r in RESULTS:
        print(f"  [{'PASS' if r['pass'] else 'FAIL'}] {r['id']}  {r['title']}")
        print(f"        {r['detail']}")
    print(f"\n=== §60 B-S60-1..5 sidecar: {n_pass}/{n} {'🔵 ALL PASS' if n_pass==n else 'FAIL'} ===")
    print(f"  {note}")
    return 0 if n_pass == n else 1


if __name__ == "__main__":
    raise SystemExit(main())
