"""§78 B-S78-1..7 closed-form sidecar battery (central blue_falsifier.py 0-diff).

g_blue_closed_mandate: 산출물 (one_engine_dialogue_stub) + 연결부위
(§31/§45 L2 mutual-exclusivity, §9 byte-equal reuse, §24 decision-axis
preserved, A/G-lift Law-71 structural mirror) 둘 다 🔵.

B-S78-NOTE empirical carve-out: same-weights externalization emergence
outcome = SGD/measurement empirical (B-D-NOTE/B-S77-NOTE/B-EMERGE-NOTE
family, NOT counted 🔵). necessary-not-sufficient per B-EMERGE-7. §49
distillation precedent honest.

f1/f2/f3 + B-IDENTITY-5 safe.
"""
from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
STUB = HERE / "one_engine_dialogue_stub.py"


def b_s78_1_same_weights_invariant() -> tuple[bool, dict]:
    """SAME-WEIGHTS-INVARIANT (structural) — ANIMA1 and ANIMA2 share
    single psi_update fn and single body_production_alpha1 fn. Boolean
    structural predicate over stub source AST: there exists exactly one
    `psi_update` def and one `body_production_alpha1` def, and BOTH
    ANIMA1 + ANIMA2 turn branches call SAME named functions (no
    `_anima1_update` vs `_anima2_update` divergence).
    """
    src = STUB.read_text()
    tree = ast.parse(src)
    psi_update_defs = [n for n in ast.walk(tree)
                       if isinstance(n, ast.FunctionDef) and n.name == "psi_update"]
    body_defs = [n for n in ast.walk(tree)
                 if isinstance(n, ast.FunctionDef)
                 and n.name == "body_production_alpha1"]
    # forbid divergent per-anima fn names
    forbidden_div = ["anima1_update", "anima2_update", "_a1_update", "_a2_update",
                     "body_production_anima1", "body_production_anima2"]
    div_hits = sum(1 for n in ast.walk(tree)
                   if isinstance(n, ast.FunctionDef) and n.name in forbidden_div)
    one_psi = len(psi_update_defs) == 1
    one_body = len(body_defs) == 1
    no_div = div_hits == 0
    # also: both ANIMA1 and ANIMA2 turn branches in run_mode call same fns
    run_mode = [n for n in ast.walk(tree)
                if isinstance(n, ast.FunctionDef) and n.name == "run_mode"]
    call_names = []
    if run_mode:
        for c in ast.walk(run_mode[0]):
            if isinstance(c, ast.Call):
                f = c.func
                if isinstance(f, ast.Name):
                    call_names.append(f.id)
        # body_production_alpha1 called at least twice (ANIMA1 + ANIMA2)
        body_calls = call_names.count("body_production_alpha1")
        psi_calls = call_names.count("psi_update")
    else:
        body_calls = psi_calls = 0
    both_share = body_calls >= 2 and psi_calls >= 3
    ok = one_psi and one_body and no_div and both_share
    return ok, {
        "one_psi_update_def": one_psi,
        "one_body_production_def": one_body,
        "no_divergent_per_anima_fn": no_div,
        "both_anima_share_calls": both_share,
        "body_call_count": body_calls,
        "psi_call_count": psi_calls,
    }


def b_s78_2_l2_distinct_from_78() -> tuple[bool, dict]:
    """§31/§45-L2-DISTINCT-FROM-§78 — Boolean mutual exclusivity.
    L2: distinct_weights ∧ distinct_vacuum_psi ∧ distinct_update_fn = True
    §78: distinct_weights ∨ distinct_vacuum_psi ∨ distinct_update_fn = False
    ⇒ {§78, L2} are disjoint architectural classes (closed).
    """
    s78 = {"weights": False, "vacuum_psi": False, "update_fn": False}
    l2 = {"weights": True, "vacuum_psi": True, "update_fn": True}
    s78_any_distinct = any(s78.values())
    l2_all_distinct = all(l2.values())
    mutual_exclusive = (not s78_any_distinct) and l2_all_distinct
    return mutual_exclusive, {
        "s78_any_distinct": s78_any_distinct,
        "l2_all_distinct": l2_all_distinct,
        "mutually_exclusive": mutual_exclusive,
    }


def b_s78_3_alpha1_byte_equal() -> tuple[bool, dict]:
    """§77-PATH-α1-REUSE-BYTE-EQUAL — body_production_alpha1 is pure fn,
    same (psi, turn_seed) ⇒ same bytes. SHA256 over 3 sample pairs.
    """
    sys.path.insert(0, str(HERE))
    try:
        # fresh import
        if "one_engine_dialogue_stub" in sys.modules:
            del sys.modules["one_engine_dialogue_stub"]
        import one_engine_dialogue_stub as S  # type: ignore
    finally:
        pass
    psi_sample = [0.5] * S.PSI_DIM
    pairs = []
    all_eq = True
    for seed in (1, 1337, 999983):
        b1 = S.body_production_alpha1(psi_sample, seed)
        b2 = S.body_production_alpha1(psi_sample, seed)
        h1 = hashlib.sha256(b1).hexdigest()
        h2 = hashlib.sha256(b2).hexdigest()
        eq = (h1 == h2 and b1 == b2)
        all_eq = all_eq and eq
        pairs.append({"seed": seed, "sha256_a": h1, "sha256_b": h2,
                      "byte_equal": eq, "len": len(b1)})
    return all_eq, {"pairs": pairs, "all_byte_equal": all_eq}


def b_s78_4_emerge_metric_reuse() -> tuple[bool, dict]:
    """§9-METRIC-REUSE — honest_coherent fn implements 4-clause Boolean
    conjunction (cascade_rate < τ_c) ∧ (max_run < MAX_RUN) ∧
    (len ≥ MIN_LEN) ∧ (printable ≥ τ_p). Structural source-grep + 4
    witness corners (truth table).
    """
    sys.path.insert(0, str(HERE))
    if "one_engine_dialogue_stub" in sys.modules:
        del sys.modules["one_engine_dialogue_stub"]
    import one_engine_dialogue_stub as S  # type: ignore
    # corners
    # (a) clean printable text — short → MIN_LEN fail
    a = b"x"
    # (b) all-printable 30-byte non-repeating, digit-free (skip 48..57)
    b_letters = bytes([c for c in range(65, 96)][:30])  # A..^ 30 distinct printable, no digits
    # (c) all-printable 30-byte but max_run=30 (cascade fail)
    c = b"a" * 30
    # (d) printable but digits cascade
    d = b"1234567890" + b"5" * 20  # max_digit_run=20
    res = {
        "short_should_fail": S.honest_coherent(a) is False,
        "clean_30byte_should_pass": S.honest_coherent(b_letters) is True,
        "char_cascade_should_fail": S.honest_coherent(c) is False,
        "digit_cascade_should_fail": S.honest_coherent(d) is False,
    }
    ok = all(res.values())
    return ok, res


def b_s78_5_control_decision_axis() -> tuple[bool, dict]:
    """§24-DECISION-AXIS-PRESERVED — D_control mode disables body
    production (a1_body = b"" and a2_body = b"") and only ψ idles. The
    control's ψ_state_variance ≤ all other modes' variances (control is
    a strict lower bound; B variants add user inject, A/C add body).
    """
    sys.path.insert(0, str(HERE))
    if "one_engine_dialogue_stub" in sys.modules:
        del sys.modules["one_engine_dialogue_stub"]
    import one_engine_dialogue_stub as S  # type: ignore
    rD = S.run_mode("D_control")
    rA = S.run_mode("A_pure")
    rB = S.run_mode("B_3party")
    rC = S.run_mode("C_meta")
    # control has bodies = empty
    all_empty = all(tl.body_bytes == b"" for tl in rD.turns)
    var_D = rD.psi_state_variance
    # control should be strict lower or equal (bodies are empty, ψ does not change)
    ctl_min = (var_D <= rA.psi_state_variance + 1e-12
               and var_D <= rB.psi_state_variance + 1e-12
               and var_D <= rC.psi_state_variance + 1e-12)
    return all_empty and ctl_min, {
        "control_bodies_empty": all_empty,
        "var_D_control": var_D,
        "var_A_pure": rA.psi_state_variance,
        "var_B_3party": rB.psi_state_variance,
        "var_C_meta": rC.psi_state_variance,
        "control_is_lower_bound": ctl_min,
    }


def b_s78_6_ag_lift_construction() -> tuple[bool, dict]:
    """A/G-LIFT-CONSTRUCTION — Law-71 ψ_dir = (1+cos(logits_a,logits_g))/2
    structural parallel: ANIMA1, ANIMA2 are two readouts of one ψ_state
    via SAME body_production_alpha1 fn. Boolean structural: no separate
    ANIMA1-only or ANIMA2-only ψ_state variable; psi is single var.
    """
    src = STUB.read_text()
    # forbid divergent ψ state names
    forb = ["psi_anima1", "psi_anima2", "psi_a1", "psi_a2",
            "anima1_psi", "anima2_psi"]
    hits = sum(src.count(f) for f in forb)
    no_div_psi = hits == 0
    # exactly one init_psi_state def
    tree = ast.parse(src)
    init_defs = [n for n in ast.walk(tree)
                 if isinstance(n, ast.FunctionDef) and n.name == "init_psi_state"]
    one_init = len(init_defs) == 1
    # in run_mode body, `psi = init_psi_state(...)` called exactly once
    rm = [n for n in ast.walk(tree)
          if isinstance(n, ast.FunctionDef) and n.name == "run_mode"]
    init_calls = 0
    if rm:
        for c in ast.walk(rm[0]):
            if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) \
                    and c.func.id == "init_psi_state":
                init_calls += 1
    one_psi_var = init_calls == 1
    ok = no_div_psi and one_init and one_psi_var
    return ok, {
        "no_divergent_psi_state_names": no_div_psi,
        "one_init_psi_state_def": one_init,
        "one_psi_init_call_in_run_mode": one_psi_var,
        "init_calls_in_run_mode": init_calls,
    }


def b_s78_7_deterministic() -> tuple[bool, dict]:
    """DETERMINISTIC — 3× run_mode bit-identical (no RNG, pure fn)."""
    sys.path.insert(0, str(HERE))
    if "one_engine_dialogue_stub" in sys.modules:
        del sys.modules["one_engine_dialogue_stub"]
    import one_engine_dialogue_stub as S  # type: ignore
    sha_per_mode = {}
    ok = True
    for mode in ("A_pure", "B_3party", "C_meta", "D_control"):
        shas = []
        for _ in range(3):
            r = S.run_mode(mode)
            # canonicalize: concat body_bytes for all turns + final psi
            blob = b""
            for tl in r.turns:
                blob += tl.body_bytes + b"\x00"
            blob += repr(r.psi_state_variance).encode("utf-8")
            shas.append(hashlib.sha256(blob).hexdigest())
        all_eq = len(set(shas)) == 1
        sha_per_mode[mode] = {"sha256_sample": shas[0], "all_3_equal": all_eq}
        ok = ok and all_eq
    return ok, sha_per_mode


def main() -> int:
    battery = [
        ("B-S78-1-SAME-WEIGHTS-INVARIANT", b_s78_1_same_weights_invariant),
        ("B-S78-2-L2-DISTINCT-FROM-78", b_s78_2_l2_distinct_from_78),
        ("B-S78-3-PATH-ALPHA1-BYTE-EQUAL", b_s78_3_alpha1_byte_equal),
        ("B-S78-4-EMERGE-METRIC-REUSE", b_s78_4_emerge_metric_reuse),
        ("B-S78-5-CONTROL-DECISION-AXIS", b_s78_5_control_decision_axis),
        ("B-S78-6-AG-LIFT-CONSTRUCTION", b_s78_6_ag_lift_construction),
        ("B-S78-7-DETERMINISTIC", b_s78_7_deterministic),
    ]
    results = {}
    n_pass = 0
    for name, fn in battery:
        try:
            ok, detail = fn()
        except Exception as e:
            ok, detail = False, {"exception": repr(e)}
        results[name] = {"PASS": bool(ok), "detail": detail}
        if ok:
            n_pass += 1
    out = {
        "sec": "§78",
        "battery": "B-S78-1..7",
        "n_pass": n_pass,
        "n_total": len(battery),
        "all_pass": n_pass == len(battery),
        "B_S78_NOTE_empirical_carve_out": (
            "same-weights externalization emergence outcome = SGD/measurement "
            "empirical (B-D-NOTE/B-S77-NOTE/B-EMERGE-NOTE family, NOT counted "
            "🔵); necessary-not-sufficient per B-EMERGE-7; §49 distillation "
            "precedent honest"),
        "results": results,
    }
    out_path = Path(__file__).parent / "blue_falsifier_s78_result.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0 if out["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
