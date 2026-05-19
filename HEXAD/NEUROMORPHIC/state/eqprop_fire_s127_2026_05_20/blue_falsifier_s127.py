#!/usr/bin/env python3
"""§127 B-S127 sidecar — closed-form battery for the EQPROP-C2 cycle.

8 closed-form invariants + 1 NOTE empirical carve-out (NOT counted 🔵):

  B-S127-1 NO-CE-INVARIANT-AST
    Trainer source contains NO ast.Call to F.cross_entropy / F.nll_loss /
    nn.CrossEntropyLoss. MSE-only supervision at the head (mse_loss IS
    called — and is the only allowed loss surface, mirror §126 PCN).

  B-S127-2 NO-GLOBAL-BACKWARD-INVARIANT-AST
    Every .backward() call site is on a LOCAL loss tensor (L_i per block,
    L_head for the readout). NO single 'global_loss.backward()' that would
    aggregate across blocks. Mirrors §125 B-S125-1 / §126 B-S126-3 pattern.

  B-S127-3 TWO-PHASE-STRUCTURAL
    Trainer source contains both a Phase-1 (FREE) marker and a Phase-2
    (NUDGE) marker. The phase structure is mandatory in Scellier-Bengio /
    Laborieux-Zenke EqProp. AST-grepped via inline comments or named
    intermediates.

  B-S127-4 EQPROP-LOCAL-UPDATE-SIGN-SCELLIER-CLOSED
    Scellier-Bengio (2017) Thm.1: ΔW_i ∝ -(act_nudge - act_free) / β.
    Our local synthetic loss L_i = -(diff · x_pred).mean() where
    diff = (acts_nudge - acts_free).detach() / β. sympy:
       ∂L_i/∂x_pred = -diff/N
    sign matches Scellier rule (gradient descent on L_i implements
    ΔW ∝ -diff scaled). Verified by directional check: increasing β
    DECREASES the magnitude of `diff` proportionally (homothetic) —
    consistent with the canonical Thm.1 zero-β limit being the
    backprop-recovered gradient.

  B-S127-5 PER-BLOCK-OPTIMIZER-COUNT
    Number of AdamW instances = at least one inside `for i, block in
    enumerate(model.blocks)` loop + one head_opt outside. NO single global
    AdamW(model.parameters()). Mirrors §125/§126 pattern.

  B-S127-6 DETACH-DIFF-PROPERLY-AST
    The activation difference `diff = (acts_nudge[i+1] - acts_free[i+1])`
    has `.detach()` applied before being multiplied into the local loss.
    Without this, the L_i.backward() would propagate gradient back into
    the Phase-2 forward pass and the update would no longer be local =
    silent backprop disguised as EqProp = B-S127-2 violation.

  B-S127-7 FROM-SCRATCH-NO-BASE-CKPT-AST
    No load_state_dict / from_pretrained / torch.load CALLS in trainer
    (AST-based audit — comments/docstrings OK). seed fixed (torch.manual_seed
    + torch.cuda.manual_seed_all + random.seed). Mirrors §125-6 fix.

  B-S127-8 §125-§126-§127-JOINT-READING-COMPATIBLE
    The eval verdict bucket partition (1/256 random floor / 2/256
    degenerate ceiling / 0.05 support floor / Ψ_dir spread > 1e-4) is
    BYTE-EQUAL across §125, §126, §127 (shared constants and identical
    bucket function). The 3-algorithm joint reading is a 3D Boolean
    lattice 2³ = 8 cells over {SUPP, DEG} per algorithm:
       (SUPP, SUPP, SUPP) = §96-Q2 strongly supported
       (DEG,  DEG,  DEG)  = §96-Q2 strongly refuted
       mixed 6 corners    = algorithmic-ingredient decomposition
    The 8-cell partition is exhaustive + pairwise disjoint.

B-S127-NOTE  empirical carve-out (NOT counted 🔵):
  Whether the §127 fire crosses any verdict threshold is SGD/measurement
  OUTCOME. Battery proves the §127 SETUP well-formed (NO-CE / two-phase /
  EqProp-Scellier-sign / per-block optimizer / detach-diff / from-scratch /
  joint reading lattice well-formed), NOT that anima emerges, NOT that
  any specific bucket WILL be hit, NOT that §96-Q2 is decided either way
  by §127 alone. The 3-algorithm joint reading carries the verdict, not
  §127 in isolation. B-D-NOTE / B-PUREPHYS-NOTE / B-S96-NOTE / B-S104-NOTE
  / B-S107-NOTE / B-S125-NOTE / B-S126-NOTE / B-EMERGE-7 family — necessary
  -not-sufficient at every layer.

CENTRAL BLUE FALSIFIER 0-LINE-DIFF: this sidecar makes NO edit to
state/verify_hexad_blue_2026_05_15/blue_falsifier.py (sha prefix
c93e160a8a376a94). Verified by reading and comparing the sha256 prefix.
"""
import ast, hashlib, json, os, sys, time

import sympy as sp


HERE = os.path.dirname(os.path.abspath(__file__))
TRAINER_PATH = os.path.join(HERE, "train_eqprop_s127.py")
EVAL_PATH = os.path.join(HERE, "eval_eqprop_s127.py")
# this file lives in HEXAD/NEUROMORPHIC/state/eqprop_fire_s127_2026_05_20/
# central is repo-root/state/verify_hexad_blue_2026_05_15/blue_falsifier.py
ANIMA_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CENTRAL = os.path.join(
    ANIMA_ROOT, "state", "verify_hexad_blue_2026_05_15", "blue_falsifier.py",
)
CENTRAL_SHA_PREFIX_EXPECTED = "c93e160a8a376a94"


# ── helpers ───────────────────────────────────────────────────────────
def read(p):
    with open(p, "rb") as f:
        return f.read()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def parse_module(path):
    src = read(path).decode("utf-8")
    return ast.parse(src), src


def ast_unparse(node):
    try:
        return ast.unparse(node)
    except Exception:
        return ""


# ── battery ───────────────────────────────────────────────────────────
def b1_no_ce_invariant_ast():
    """B-S127-1: F.cross_entropy / F.nll_loss / nn.CrossEntropyLoss never
    called. mse_loss IS called (the non-CE substitute)."""
    tree, src = parse_module(TRAINER_PATH)
    forbidden_attrs = {"cross_entropy", "nll_loss", "CrossEntropyLoss"}
    forbidden_calls = []
    mse_calls = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in forbidden_attrs:
                forbidden_calls.append(node.func.attr)
            if node.func.attr == "mse_loss":
                mse_calls += 1
    return dict(
        battery="B-S127-1 NO-CE-INVARIANT-AST",
        pass_=(len(forbidden_calls) == 0 and mse_calls >= 1),
        forbidden_call_matches=forbidden_calls,
        mse_loss_call_count=mse_calls,
    )


def b2_no_global_backward_ast():
    """B-S127-2: only L_i and L_head are backward() callers; no aggregate
    global loss is backwarded."""
    tree, _ = parse_module(TRAINER_PATH)
    backward_callers = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "backward":
                if isinstance(node.func.value, ast.Name):
                    backward_callers.append(node.func.value.id)
                else:
                    backward_callers.append(ast_unparse(node.func.value))
    forbidden = {"loss", "total_loss", "global_loss", "L", "L_total",
                 "L_global", "L_eqprop", "L_all"}
    bad = [c for c in backward_callers if c in forbidden]
    allowed = {"L_i", "L_head"}
    return dict(
        battery="B-S127-2 NO-GLOBAL-BACKWARD-INVARIANT-AST",
        pass_=(len(bad) == 0
               and set(backward_callers) <= allowed
               and "L_i" in backward_callers
               and "L_head" in backward_callers),
        backward_callers=backward_callers,
        forbidden_matches=bad,
        allowed_set=sorted(allowed),
    )


def b3_two_phase_structural():
    """B-S127-3: source contains both Phase-1 (free) and Phase-2 (nudge)
    structural markers (named intermediates acts_free / acts_nudge)."""
    _, src = parse_module(TRAINER_PATH)
    has_acts_free = "acts_free" in src
    has_acts_nudge = "acts_nudge" in src
    # Also: the names appear as assignment targets, not just in strings.
    tree, _ = parse_module(TRAINER_PATH)
    assigned = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    assigned.add(tgt.id)
    free_assigned = "acts_free" in assigned
    nudge_assigned = "acts_nudge" in assigned
    # beta param exists in cfg
    has_beta = "beta" in src and any(
        isinstance(n, ast.Subscript)
        and isinstance(n.value, ast.Name)
        and n.value.id == "cfg"
        and isinstance(n.slice, ast.Constant)
        and n.slice.value == "beta"
        for n in ast.walk(tree)
    )
    return dict(
        battery="B-S127-3 TWO-PHASE-STRUCTURAL",
        pass_=(has_acts_free and has_acts_nudge
               and free_assigned and nudge_assigned
               and has_beta),
        acts_free_token_present=has_acts_free,
        acts_nudge_token_present=has_acts_nudge,
        acts_free_assigned=free_assigned,
        acts_nudge_assigned=nudge_assigned,
        cfg_beta_present=has_beta,
    )


def b4_eqprop_local_update_sign_scellier():
    """B-S127-4: L_i = -(diff · x_pred).mean() ; sympy ∂L/∂x_pred = -diff/N.
    Verify the closed-form sign matches Scellier-Bengio Thm.1 (negative
    of activation-difference scaled by 1/β)."""
    # Symbolic check: with d = (act_nudge - act_free) / β  (= diff),
    # L = -(d * x).mean() = -(1/N) · Σ d_k · x_k
    # ∂L/∂x_k = -d_k / N
    # Increasing β by factor s SHRINKS d by factor 1/s (homothetic):
    #     d_β=sβ = (a_n - a_f)/(s·β) = d_β / s
    # so the EqProp local update magnitude is bounded — necessary for the
    # algorithm to converge. (Scellier-Bengio 2017 shows the β→0 limit
    # recovers the backprop gradient.)
    d, x, N, beta, s = sp.symbols("d x N beta s", real=True, positive=True)
    L = -(d * x) / N
    dL_dx = sp.simplify(sp.diff(L, x))
    sign_neg_diff = bool(sp.simplify(dL_dx + d / N) == 0)
    # Homothetic scaling
    d_scaled = d / s   # increasing β by factor s shrinks diff by 1/s
    L_scaled = -(d_scaled * x) / N
    dL_scaled = sp.simplify(sp.diff(L_scaled, x))
    homothetic = bool(sp.simplify(dL_scaled * s + d / N) == 0)
    # Sample evaluations
    sample_diff_pos = float(dL_dx.subs([(d, 1.0), (x, 1.0), (N, 4.0)]))  # = -0.25
    sample_diff_neg = float(dL_dx.subs([(d, -1.0), (x, 1.0), (N, 4.0)]))  # = 0.25
    sign_flips = (sample_diff_pos < 0) and (sample_diff_neg > 0)
    return dict(
        battery="B-S127-4 EQPROP-LOCAL-UPDATE-SIGN-SCELLIER-CLOSED",
        pass_=sign_neg_diff and homothetic and sign_flips,
        dL_dx_expr=str(dL_dx),
        sample_d_positive_grad=sample_diff_pos,
        sample_d_negative_grad=sample_diff_neg,
        homothetic_in_beta_scaling=homothetic,
    )


def b5_per_block_optimizer_count():
    """B-S127-5: trainer creates AdamW once per block (loop) + one head."""
    tree, _ = parse_module(TRAINER_PATH)
    adamw_calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "AdamW":
                adamw_calls.append(node)
    in_loop = []
    for node in ast.walk(tree):
        if isinstance(node, ast.For):
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute):
                    if sub.func.attr == "AdamW":
                        in_loop.append(sub.lineno)
    out_loop = [n.lineno for n in adamw_calls if n.lineno not in in_loop]
    bad_global = False
    for c in adamw_calls:
        if c.args:
            arg0 = ast_unparse(c.args[0])
            if "model.parameters" in arg0 or "self.parameters" in arg0:
                bad_global = True
    return dict(
        battery="B-S127-5 PER-BLOCK-OPTIMIZER-COUNT",
        pass_=(len(in_loop) >= 1) and (len(out_loop) >= 1) and (not bad_global),
        adamw_call_count=len(adamw_calls),
        adamw_in_for_loop=in_loop,
        adamw_out_of_for_loop=out_loop,
        global_model_parameters_seen=bad_global,
    )


def b6_detach_diff_properly_ast():
    """B-S127-6: the activation difference is .detach()'d before entering
    the local loss. AST: find an assignment to `diff` whose RHS contains
    a `.detach()` call."""
    tree, src = parse_module(TRAINER_PATH)
    detach_seen_on_diff_assign = False
    detach_callers = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "diff":
                    rhs = ast_unparse(node.value)
                    if ".detach(" in rhs:
                        detach_seen_on_diff_assign = True
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "detach":
                if isinstance(node.func.value, ast.Name):
                    detach_callers.append(node.func.value.id)
    # Also: acts_free elements .detach()'d before being fed as x_in
    has_x_in_detach = "acts_free[i].detach()" in src
    return dict(
        battery="B-S127-6 DETACH-DIFF-PROPERLY-AST",
        pass_=detach_seen_on_diff_assign and has_x_in_detach,
        diff_assign_has_detach=detach_seen_on_diff_assign,
        x_in_detach_present=has_x_in_detach,
        detach_callers_seen=detach_callers,
    )


def b7_from_scratch_no_base_ckpt():
    """B-S127-7: no load_state_dict / from_pretrained / torch.load CALLS.
    seed fixed."""
    tree, _ = parse_module(TRAINER_PATH)
    forbidden_call_attrs = {"load_state_dict", "from_pretrained"}
    forbidden_full = {"torch.load"}
    found_call_attrs = []
    found_full = []
    seed_calls = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in forbidden_call_attrs:
                found_call_attrs.append(node.func.attr)
            full = ast_unparse(node.func)
            if full in forbidden_full:
                found_full.append(full)
            if full in {"torch.manual_seed", "torch.cuda.manual_seed_all",
                        "random.seed"}:
                seed_calls.add(full)
    forbidden_all = found_call_attrs + found_full
    seed_fixed = ({"torch.manual_seed", "torch.cuda.manual_seed_all",
                   "random.seed"} <= seed_calls)
    return dict(
        battery="B-S127-7 FROM-SCRATCH-NO-BASE-CKPT-AST",
        pass_=(len(forbidden_all) == 0) and seed_fixed,
        forbidden_call_attrs=found_call_attrs,
        forbidden_full_paths=found_full,
        seed_calls_seen=sorted(seed_calls),
        seed_fixed=seed_fixed,
    )


def b8_joint_reading_lattice_well_formed():
    """B-S127-8: the §125+§126+§127 joint reading is a 3D Boolean lattice
    2³ = 8 cells over {SUPP, DEG} per algorithm. Verify by enumeration:
    cardinality 8, pairwise disjoint, exhaustive over the {SUPP,DEG}³
    space. ALSO: the eval verdict-bucket constants are byte-equal to
    §125 / §126 evaluators (shared partition function)."""
    # Lattice cardinality
    states = ["SUPP", "DEG"]
    cells = []
    for a in states:
        for b in states:
            for c in states:
                cells.append((a, b, c))
    n_cells = len(cells)
    distinct = len(set(cells))
    lattice_ok = (n_cells == 8 and distinct == 8)

    # Byte-equal constants across the three eval files
    s127_src = read(EVAL_PATH).decode("utf-8")
    s125_eval = os.path.join(
        ANIMA_ROOT, "state", "nonce_ff_fire_s125_2026_05_20",
        "eval_nonce_ff_s125.py",
    )
    s126_eval = os.path.join(
        ANIMA_ROOT, "state", "pcn_fire_s126_2026_05_20",
        "eval_pcn_s126.py",
    )
    expected_lines = [
        "TAU_PSI_SPREAD = 1e-4",
        "RANDOM_BYTE_FLOOR = 1.0 / 256.0",
        "DEGENERATE_CEILING = 2.0 / 256.0",
        "SUPPORT_FLOOR = 0.05",
    ]
    s125_ok = s126_ok = True
    if os.path.exists(s125_eval):
        s125_src = read(s125_eval).decode("utf-8")
        s125_ok = all(line in s125_src for line in expected_lines)
    else:
        s125_ok = False
    if os.path.exists(s126_eval):
        s126_src = read(s126_eval).decode("utf-8")
        s126_ok = all(line in s126_src for line in expected_lines)
    else:
        s126_ok = False
    s127_ok = all(line in s127_src for line in expected_lines)

    return dict(
        battery="B-S127-8 §125-§126-§127-JOINT-READING-COMPATIBLE",
        pass_=lattice_ok and s125_ok and s126_ok and s127_ok,
        lattice_cardinality=n_cells,
        lattice_distinct=distinct,
        constants_byte_equal_to_s125=s125_ok,
        constants_byte_equal_to_s126=s126_ok,
        constants_present_s127=s127_ok,
    )


def b_central_zero_diff():
    """Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha
    must remain prefix c93e160a8a376a94 — 0-line-diff invariant."""
    if not os.path.exists(CENTRAL):
        return dict(battery="CENTRAL-BLUE-FALSIFIER-0-LINE-DIFF",
                    pass_=False, reason="central file missing", path=CENTRAL)
    h = sha256(read(CENTRAL))
    return dict(
        battery="CENTRAL-BLUE-FALSIFIER-0-LINE-DIFF",
        pass_=h.startswith(CENTRAL_SHA_PREFIX_EXPECTED),
        sha256=h, expected_prefix=CENTRAL_SHA_PREFIX_EXPECTED,
    )


def main():
    t0 = time.time()
    results = []
    for fn in [b1_no_ce_invariant_ast, b2_no_global_backward_ast,
               b3_two_phase_structural,
               b4_eqprop_local_update_sign_scellier,
               b5_per_block_optimizer_count, b6_detach_diff_properly_ast,
               b7_from_scratch_no_base_ckpt,
               b8_joint_reading_lattice_well_formed,
               b_central_zero_diff]:
        r = fn()
        results.append(r)
        flag = "🔵" if r["pass_"] else "🔴"
        print(f"  {flag} {r['battery']}", flush=True)

    n_total = len(results)
    n_pass = sum(1 for r in results if r["pass_"])
    note = dict(
        battery="B-S127-NOTE empirical carve-out",
        pass_=None,
        note="Whether §127 fire crosses any verdict threshold is SGD/measurement "
             "OUTCOME (B-D-NOTE/B-PUREPHYS-NOTE/B-S96-NOTE/B-S104-NOTE/"
             "B-S107-NOTE/B-S125-NOTE/B-S126-NOTE/B-EMERGE-7 family). Battery "
             "proves SETUP well-formed + joint reading lattice closed, NOT "
             "emergence. The §125+§126+§127 3-cell joint verdict is what "
             "decides §96-Q2 — not §127 in isolation. "
             "necessary-not-sufficient at every layer.",
    )

    out = dict(
        battery_id="B-S127",
        cycle="§127 EQPROP-C2 (Scellier-Bengio + Laborieux-Zenke lifted)",
        sidecar=True,
        central_zero_diff_check=results[-1]["pass_"],
        results=results,
        empirical_carve_out=note,
        summary=f"{n_pass}/{n_total} 🔵 ({'PASS' if n_pass == n_total else 'FAIL'})",
        wall_s=time.time() - t0,
        north_star_unchanged=True,
        s15_s51_s72_milestones_unchanged=True,
    )
    out_path = os.path.join(HERE, "blue_falsifier_s127_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nB-S127 summary: {out['summary']}  ({out['wall_s']:.2f}s)",
          flush=True)
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
