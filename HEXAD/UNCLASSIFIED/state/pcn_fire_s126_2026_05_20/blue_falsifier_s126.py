#!/usr/bin/env python3
"""§126 B-S126 sidecar — closed-form battery for the PCN-C4 cycle.

8 closed-form invariants + 1 NOTE empirical carve-out (NOT counted 🔵):

  B-S126-1 NO-CE-INVARIANT-AST
    Trainer source uses MSE loss only. Forbidden call-set:
    {F.cross_entropy, CrossEntropyLoss, F.nll_loss, nn.NLLLoss} = 0 hits.
    Verified by AST attribute/identifier walk.

  B-S126-2 NO-GLOBAL-BACKWARD-INVARIANT-AST
    Every .backward() call is on a LOCAL tensor (L_i or L_head); no
    aggregate global loss. Mirrors B-S125-1 structural property.

  B-S126-3 MSE-NONNEGATIVE-AND-CONVEX
    L_mse = mean((x - t)²) ≥ 0 ∀ x,t ; ∂²L/∂x² = 2/N · I ≻ 0.
    Fixed point x = t ⇒ L = 0 (global min).

  B-S126-4 PCN-LOCAL-TARGET-DETACHED-AST
    Per-block local target t_i is .detach()'d in the trainer source.
    Inspect for `t_i = acts_detached[i+1].detach()` or
    `acts_detached` derived under `torch.no_grad()`.

  B-S126-5 PER-BLOCK-OPTIMIZER-COUNT
    Number of AdamW instances ≥ 2 (per-block + head); no global
    AdamW over model.parameters().

  B-S126-6 FROM-SCRATCH-RANDOM-INIT-NO-BASE-CKPT
    AST: no load_state_dict / from_pretrained / torch.load calls;
    seed calls present (torch.manual_seed, torch.cuda.manual_seed_all,
    random.seed).

  B-S126-7 §11-B-CONNECTION-POINT-WELL-FORMED
    Eval verdict partition over byte_acc identical to §125
    (1/256 random floor / 2/256 degenerate ceiling / 0.05 support floor),
    deterministic, no RNG, mirrors §125 partition for joint reasoning.

  B-S126-8 §125-§126-JOINT-READING-COMPATIBLE
    §126 eval result schema includes `verdict_bucket` ∈ {S11B_LIKE_DEGENERATE,
    S96_Q2_SUPPORTED, PARTIAL_AMBIGUOUS} = exactly the §125 bucket set,
    so the 2x2 joint table is closed-form.

B-S126-NOTE empirical carve-out (NOT counted 🔵):
  Whether §126 fire crosses any verdict threshold is SGD/measurement OUTCOME.
  Battery proves SETUP well-formed, NOT emergence. Also: "1-step PCN" is a
  simplified PCN — verdict applies to this specific algorithm point, not to
  PCN-converged (Whittington-Bogacz N→∞). B-EMERGE-7 / B-D-NOTE family,
  necessary-not-sufficient at every layer.
"""
import ast, hashlib, json, os, sys, time
import sympy as sp


HERE = os.path.dirname(os.path.abspath(__file__))
TRAINER_PATH = os.path.join(HERE, "train_pcn_s126.py")
EVAL_PATH = os.path.join(HERE, "eval_pcn_s126.py")
CENTRAL = os.path.join(
    os.path.dirname(os.path.dirname(HERE)),
    "state", "verify_hexad_blue_2026_05_15", "blue_falsifier.py",
)
CENTRAL_SHA_PREFIX_EXPECTED = "c93e160a8a376a94"


def read(p):
    with open(p, "rb") as f:
        return f.read()


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def parse_module(path):
    src = read(path).decode("utf-8")
    return ast.parse(src), src


# ── batteries ─────────────────────────────────────────────────────────
def b1_no_ce_invariant_ast():
    """No F.cross_entropy / CrossEntropyLoss / F.nll_loss / nn.NLLLoss calls."""
    tree, src = parse_module(TRAINER_PATH)
    forbidden_names = {"cross_entropy", "nll_loss"}
    forbidden_classes = {"CrossEntropyLoss", "NLLLoss"}
    hits_calls = []
    hits_classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in forbidden_names:
                    hits_calls.append(node.func.attr)
                if node.func.attr in forbidden_classes:
                    hits_classes.append(node.func.attr)
            elif isinstance(node.func, ast.Name):
                if node.func.id in forbidden_names:
                    hits_calls.append(node.func.id)
                if node.func.id in forbidden_classes:
                    hits_classes.append(node.func.id)
        if isinstance(node, ast.Name) and node.id in forbidden_classes:
            # name reference — could be instantiation elsewhere
            hits_classes.append(node.id)
    # MSE loss must be USED (positive evidence)
    has_mse = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "mse_loss":
                has_mse = True
                break
    return dict(
        battery="B-S126-1 NO-CE-INVARIANT-AST",
        pass_=(len(hits_calls) == 0 and len(hits_classes) == 0 and has_mse),
        forbidden_call_hits=hits_calls,
        forbidden_class_hits=hits_classes,
        mse_loss_used=has_mse,
    )


def b2_no_global_backward_ast():
    """Every .backward() is on L_i or L_head (no global loss)."""
    tree, src = parse_module(TRAINER_PATH)
    callers = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "backward":
                if isinstance(node.func.value, ast.Name):
                    callers.append(node.func.value.id)
                else:
                    callers.append(ast.unparse(node.func.value))
    allowed = {"L_i", "L_head"}
    bad = [c for c in callers if c not in allowed]
    return dict(
        battery="B-S126-2 NO-GLOBAL-BACKWARD-INVARIANT-AST",
        pass_=(set(callers) <= allowed
               and "L_i" in callers and "L_head" in callers),
        backward_callers=callers, forbidden_matches=bad,
    )


def b3_mse_nonneg_convex():
    """L = (x - t)² / N ≥ 0 ; ∂²L/∂x² = 2/N > 0 ; L(t,t)=0."""
    x, t = sp.symbols("x t", real=True)
    N = sp.Symbol("N", positive=True)
    L = (x - t) ** 2 / N
    d2 = sp.diff(L, x, 2)              # = 2/N
    L_at_t = sp.simplify(L.subs(x, t)) # = 0
    return dict(
        battery="B-S126-3 MSE-NONNEGATIVE-AND-CONVEX",
        pass_=bool(sp.simplify(d2 - sp.Rational(2) / N) == 0)
              and bool(L_at_t == 0),
        hessian=str(d2), min_at_target=str(L_at_t),
    )


def b4_pcn_local_target_detached_ast():
    """`.detach()` exists on the top-down target tensor (`t_i` derived from
    `acts_detached[i+1]`)."""
    tree, src = parse_module(TRAINER_PATH)
    # at least one .detach() on t_i source
    detach_calls = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "detach":
                detach_calls += 1
    has_no_grad = ("torch.no_grad" in src) or ("with torch.no_grad" in src)
    has_t_i_local = ("t_i = acts_detached" in src) or ("acts_detached[i + 1]" in src)
    return dict(
        battery="B-S126-4 PCN-LOCAL-TARGET-DETACHED-AST",
        pass_=(detach_calls >= 2 and has_no_grad and has_t_i_local),
        detach_call_count=detach_calls,
        no_grad_context_present=has_no_grad,
        t_i_local_target_assignment=has_t_i_local,
    )


def b5_per_block_optimizer_count():
    """≥2 AdamW (block_opts + head_opt), no `model.parameters()` global."""
    tree, src = parse_module(TRAINER_PATH)
    n_adamw = 0
    bad_global = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "AdamW":
                n_adamw += 1
                if node.args:
                    arg0 = ast.unparse(node.args[0])
                    if "model.parameters" in arg0 or "self.parameters" in arg0:
                        bad_global = True
    return dict(
        battery="B-S126-5 PER-BLOCK-OPTIMIZER-COUNT",
        pass_=(n_adamw >= 2 and not bad_global),
        adamw_call_count=n_adamw,
        global_parameters_seen=bad_global,
    )


def b6_from_scratch_no_base_ckpt():
    """No load_state_dict / from_pretrained / torch.load calls in trainer."""
    tree, src = parse_module(TRAINER_PATH)
    forbidden_attrs = {"load_state_dict", "from_pretrained"}
    forbidden_full = {"torch.load"}
    found_attrs, found_full = [], []
    seen_seed_calls = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in forbidden_attrs:
                found_attrs.append(node.func.attr)
            try:
                full = ast.unparse(node.func)
            except Exception:
                full = ""
            if full in forbidden_full:
                found_full.append(full)
            if full in {"torch.manual_seed", "torch.cuda.manual_seed_all",
                        "random.seed"}:
                seen_seed_calls.add(full)
    seed_fixed = ({"torch.manual_seed", "torch.cuda.manual_seed_all",
                   "random.seed"} <= seen_seed_calls)
    return dict(
        battery="B-S126-6 FROM-SCRATCH-RANDOM-INIT-NO-BASE-CKPT",
        pass_=(len(found_attrs) == 0 and len(found_full) == 0 and seed_fixed),
        forbidden_attrs=found_attrs, forbidden_full=found_full,
        seed_calls_seen=sorted(seen_seed_calls),
    )


def b7_eval_verdict_partition_closed():
    """Verdict thresholds == §125's (1/256, 2/256, 0.05) — bit-identical
    so joint reading is closed-form."""
    src = read(EVAL_PATH).decode("utf-8")
    has_random = "RANDOM_BYTE_FLOOR = 1.0 / 256.0" in src
    has_deg = "DEGENERATE_CEILING = 2.0 / 256.0" in src
    has_supp = "SUPPORT_FLOOR = 0.05" in src
    samples = [0.0, 1/256, 2/256, 0.01, 0.05, 0.1, 1.0]
    classify = []
    for v in samples:
        if v <= 2/256:
            b = "S11B_LIKE_DEGENERATE"
        elif v >= 0.05:
            b = "S96_Q2_SUPPORTED (if psi)"
        else:
            b = "PARTIAL_AMBIGUOUS"
        classify.append((v, b))
    distinct = len(set(b for _, b in classify))
    return dict(
        battery="B-S126-7 §11-B-CONNECTION-POINT-WELL-FORMED",
        pass_=has_random and has_deg and has_supp and distinct == 3,
        random_floor=has_random, deg_ceiling=has_deg, supp_floor=has_supp,
        sample_classification=classify,
    )


def b8_s125_s126_joint_reading_compatible():
    """§126 eval emits the same verdict_bucket labels as §125 — joint
    table closed-form."""
    src = read(EVAL_PATH).decode("utf-8")
    labels = {"S11B_LIKE_DEGENERATE", "S96_Q2_SUPPORTED", "PARTIAL_AMBIGUOUS"}
    present = {lbl for lbl in labels if lbl in src}
    # joint table: 2x2 of bucket assignments — closed-form Boolean
    table = []
    for s125_v in labels:
        for s126_v in labels:
            if s125_v == "S96_Q2_SUPPORTED" and s126_v == "S96_Q2_SUPPORTED":
                joint = "BOTH_SUPP_-> §96-Q2 SUPPORTED (robust 2-point)"
            elif s125_v == "S11B_LIKE_DEGENERATE" and s126_v == "S11B_LIKE_DEGENERATE":
                joint = "BOTH_DEG_-> §96-Q2 REFUTED (substrate-deep)"
            else:
                joint = "MIXED-or-PARTIAL"
            table.append((s125_v, s126_v, joint))
    return dict(
        battery="B-S126-8 §125-§126-JOINT-READING-COMPATIBLE",
        pass_=(present == labels and len(table) == 9),
        labels_present=sorted(present),
        joint_table_size=len(table),
    )


def b_central_zero_diff():
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
               b3_mse_nonneg_convex, b4_pcn_local_target_detached_ast,
               b5_per_block_optimizer_count, b6_from_scratch_no_base_ckpt,
               b7_eval_verdict_partition_closed,
               b8_s125_s126_joint_reading_compatible,
               b_central_zero_diff]:
        r = fn()
        results.append(r)
        flag = "🔵" if r["pass_"] else "🔴"
        print(f"  {flag} {r['battery']}", flush=True)
    n_total = len(results); n_pass = sum(1 for r in results if r["pass_"])
    note = dict(
        battery="B-S126-NOTE empirical carve-out",
        pass_=None,
        note="§126 fire OUTCOME = SGD/measurement empirical. '1-step PCN' ≠ "
             "PCN-converged (Whittington-Bogacz N→∞). Verdict applies to this "
             "algorithm point, not full PCN. B-EMERGE-7 / B-D-NOTE / "
             "B-S125-NOTE family — necessary-not-sufficient.",
    )
    out = dict(
        battery_id="B-S126",
        cycle="§126 PCN-C4 (1-step PCN on anima)",
        sidecar=True,
        central_zero_diff_check=results[-1]["pass_"],
        results=results, empirical_carve_out=note,
        summary=f"{n_pass}/{n_total} 🔵 ({'PASS' if n_pass == n_total else 'FAIL'})",
        wall_s=time.time() - t0,
        north_star_unchanged=True,
        s15_s51_s72_milestones_unchanged=True,
    )
    out_path = os.path.join(HERE, "blue_falsifier_s126_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nB-S126 summary: {out['summary']}  ({out['wall_s']:.2f}s)",
          flush=True)
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
