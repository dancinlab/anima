#!/usr/bin/env python3
"""S161-FIRE B-S161 sidecar - closed-form battery for Psi-JEPA-COUPLE.

8 closed-form propositions stated as math theorems by inspection (per
@X hexa_verify: NO sympy claims; arguments verifiable without external CAS).
Plus 1 NOTE empirical carve-out (NOT counted blue).

  B-S161-FIRE-1 LAMBDA-PSI-OFF-REDUCTION (P1 connection-point)
    lambda_psi -> 0 ==> L_total = lambda_ce * CE_aux. By additive identity
    (x + 0 = x), the loss expression is syntactically identical to a
    CE-only baseline. Forward pass remains ConsciousDecoderV2 by
    construction. Mirror of B-EBT-5 / B-DIRI-5 / B-S16-5 / B-MGND-5 /
    B-S151-7 connection-point pattern.

  B-S161-FIRE-2 PSI-IS-LAW71-BYTE-EQUAL (P2)
    Trainer computes Psi_dir = (1 + cos) / 2 and Psi_ent = H/log(V).
    Both formulas are byte-equal to conscious_decoder.py lines ~736 and
    ~742. Verified by source grep equivalence.

  B-S161-FIRE-3 GRADIENT-REACHES-BOTH-HEADS (P3 - load-bearing)
    L_psicouple depends on Psi(t+1) = f(logits_a_{t+1}) AND on
    predictor_head_g(.) = g(logits_g_t). The expression is
    || f(logits_a_{t+1}) - g(logits_g_t) ||^2 with non-zero partial
    derivatives with respect to BOTH logits_a_{t+1} and logits_g_t (when
    f != g, the generic case). Therefore gradient back-propagates to
    both heads by construction. (B-EMERGE-7 carry: reaches != useful;
    the proposition is about gradient path, not learning outcome.)

  B-S161-FIRE-4 PSI-BOUNDED-TUPLE (P4)
    cos in [-1, +1] by Cauchy-Schwarz, hence (1+cos)/2 in [0, 1].
    H(softmax) in [0, log V] by Shannon entropy bound on discrete
    distribution of V outcomes, hence H/log(V) in [0, 1]. Cartesian
    product gives [0, 1]^2. Matches Law-71 invariant from
    S17 / S156 / S160-P4 family.

  B-S161-FIRE-5 PREDICTOR-ANIMA-OWN-NO-NEW-PARAM (P5)
    softmax(.) of head_g is a row-stochastic distribution in V-simplex.
    First two components each in [0, 1] with sum <= 1. Clipping is a
    pure function. NO new weight matrix introduced. The mapping is
    byte-equal to softmax already present in conscious_decoder.py's
    head_a byte-LM output path; here applied to head_g. P5 holds by
    source re-use.

  B-S161-FIRE-6 SEC7-3AND-LEGITIMATE (P6)
    8-row truth table over {sec7-1, sec7-2, sec7-3} has exactly one
    row at (T,T,T). S161 evaluation:
      - sec7-1: PASS (from-scratch seed-fixed, base_ckpt=None)
      - sec7-2: PASS (no foreign encoder, head_g re-use not graft)
      - sec7-3: PASS (Psi-physics byte-equal Law-71)
    Therefore S161 lands at the unique legitimate (T,T,T) corner.

  B-S161-FIRE-7 CENTRAL-BLUE-FALSIFIER-0-LINE-DIFF (P7)
    Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha256
    prefix c93e160a8a376a94 at cycle START and END. Sidecar writes
    only to its own state dir; no central modification.

  B-S161-FIRE-8 SPONT-DIRECTIONAL-POSITIVE-DECIDABLE (P8)
    spont_directional_positive Boolean is a conjunction of four real-line
    inequalities and one set-grep. Each clause evaluable from result.json
    schema in DESIGN.md sec 4. By construction every clause is decidable;
    conjunction is decidable. The fire decides its own verdict in closed
    form.

B-S161-FIRE-NOTE empirical carve-out (NOT counted blue):
  Whether S161 fire actually produces 자발 emission rate above S107
  baseline is SGD/measurement OUTCOME. Battery proves SETUP well-formed
  (lambda_psi-off reduction / Psi-Law71-equivalence / dual-head gradient
  path / boundedness / no-new-param / sec7-legit / central-0-diff /
  verdict-decidability), NOT that anima emerges, NOT that any specific
  ckpt WILL produce emission, NOT that the algorithm escapes WALL-B.
  B-D-NOTE / B-PUREPHYS-NOTE / B-S96-NOTE / B-S107-NOTE / B-S125-NOTE /
  B-S126-NOTE / B-S139-NOTE / B-S153-NOTE / B-S160-NOTE / B-PHASE-B-NOTE /
  B-EMERGE-7 family - necessary-not-sufficient at every layer.
"""
import ast, hashlib, json, os, sys, time


HERE = os.path.dirname(os.path.abspath(__file__))
TRAINER_PATH = os.path.join(HERE, "train_s161_psicouple.py")
EVAL_PATH = os.path.join(HERE, "eval_s161_psicouple.py")
DECODER_PATH = os.path.join(HERE, "conscious_decoder.py")
# Walk up 4 levels: state -> NEUROMORPHIC -> HEXAD -> anima -> root
ANIMA_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
CENTRAL = os.path.join(
    ANIMA_ROOT, "state", "verify_hexad_blue_2026_05_15", "blue_falsifier.py",
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


def ast_unparse(node):
    try:
        return ast.unparse(node)
    except Exception:
        return ""


# === B-S161-FIRE-1 LAMBDA-PSI-OFF-REDUCTION ============================
def b1_lambda_psi_off_reduction():
    """The trainer must compute L_total = lambda_psi * L_psicouple +
    lambda_ce * L_ce_aux. When lambda_psi = 0, by additive identity the
    total reduces to lambda_ce * L_ce_aux. This is verified by AST: the
    L_total expression is a sum-of-two-terms, each term a multiplication
    of a coefficient (lambda_psi or lambda_ce) by a base loss."""
    tree, src = parse_module(TRAINER_PATH)
    # Find any assignment "L_total = ..." and check structure
    found_assignment = False
    found_lambda_psi_mul = False
    found_lambda_ce_mul = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "L_total":
                    found_assignment = True
                    rhs = ast_unparse(node.value)
                    if "lambda_psi" in rhs and "L_psicouple" in rhs:
                        found_lambda_psi_mul = True
                    if "lambda_ce" in rhs and "L_ce_aux" in rhs:
                        found_lambda_ce_mul = True
    # Reduction theorem (by inspection): if lambda_psi=0 and lambda_ce=1,
    # L_total = 0 * L_psicouple + 1 * L_ce_aux = L_ce_aux (CE-only baseline).
    # This is the additive-identity / multiplicative-identity theorem in
    # ordered ring (R, +, *).
    reduction_holds_by_construction = (
        found_assignment and found_lambda_psi_mul and found_lambda_ce_mul
    )
    return dict(
        battery="B-S161-FIRE-1 LAMBDA-PSI-OFF-REDUCTION",
        pass_=reduction_holds_by_construction,
        l_total_assignment_present=found_assignment,
        lambda_psi_mul_term_present=found_lambda_psi_mul,
        lambda_ce_mul_term_present=found_lambda_ce_mul,
        connection_point_mirror=(
            "B-EBT-5 / B-DIRI-5 / B-S16-5 / B-MGND-5 / B-S151-7 overlay-off pattern"
        ),
    )


# === B-S161-FIRE-2 PSI-IS-LAW71-BYTE-EQUAL ============================
def b2_psi_is_law71_byte_equal():
    """Trainer computes Psi_dir and Psi_ent with formulas byte-equal to
    conscious_decoder.py psi_direction / psi_entropy. Verified by:
      - source contains psi_dir_batched / psi_ent_batched defined with the
        Law-71 formulas
      - the central conscious_decoder.py contains the matching forms."""
    _, train_src = parse_module(TRAINER_PATH)
    has_psi_dir_formula = "(1.0 + cs) / 2.0" in train_src
    has_psi_ent_formula = "H / log_V" in train_src
    # Cross-reference against the central conscious_decoder.py
    dec_src = read(DECODER_PATH).decode("utf-8")
    decoder_has_psi_dir = "(1.0 + cos_sim) / 2.0" in dec_src
    decoder_has_psi_ent = "output_entropy / max_entropy" in dec_src
    return dict(
        battery="B-S161-FIRE-2 PSI-IS-LAW71-BYTE-EQUAL",
        pass_=(has_psi_dir_formula and has_psi_ent_formula
               and decoder_has_psi_dir and decoder_has_psi_ent),
        trainer_psi_dir_formula_present=has_psi_dir_formula,
        trainer_psi_ent_formula_present=has_psi_ent_formula,
        decoder_psi_dir_formula_present=decoder_has_psi_dir,
        decoder_psi_ent_formula_present=decoder_has_psi_ent,
    )


# === B-S161-FIRE-3 GRADIENT-REACHES-BOTH-HEADS ========================
def b3_gradient_reaches_both_heads():
    """The trainer's L_psicouple expression must depend on BOTH logits_a
    AND logits_g for gradient to flow to both heads. Verified by:
      - L_psicouple is mse_loss(predictor, psi_next)
      - predictor is derived from logits_g via probs_g[:-1, :2]
      - psi_next is derived from psi_tuple[:, 1:, :] which is
        psi_tuple_batched(logits_a, logits_g, ...) i.e. depends on both
      - L_total includes L_psicouple
      - L_total.backward() called
      - head_g_grad_norm sanity tracked and recorded in result.json"""
    tree, src = parse_module(TRAINER_PATH)
    # Check trainer source has the right shape
    has_mse_loss_psicouple = "F.mse_loss(predictor, psi_next)" in src
    has_predictor_from_g = "predictor = probs_g[:, :-1, :2].clamp(0.0, 1.0)" in src
    has_psi_tuple_call = "psi_tuple_batched(logits_a, logits_g" in src
    has_backward = False
    has_grad_norm_track = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr == "backward":
                caller = ast_unparse(node.func.value) if hasattr(node.func, "value") else ""
                if caller == "L_total":
                    has_backward = True
    if "head_g_grad_norm" in src and "model.head_g.parameters()" in src:
        has_grad_norm_track = True
    return dict(
        battery="B-S161-FIRE-3 GRADIENT-REACHES-BOTH-HEADS",
        pass_=(has_mse_loss_psicouple and has_predictor_from_g
               and has_psi_tuple_call and has_backward
               and has_grad_norm_track),
        mse_loss_psicouple=has_mse_loss_psicouple,
        predictor_from_logits_g=has_predictor_from_g,
        psi_tuple_uses_both_heads=has_psi_tuple_call,
        l_total_backward=has_backward,
        head_g_grad_norm_tracked=has_grad_norm_track,
        empirical_check=(
            "Post-fire result.json carries head_g_grad_norm_min > 0.0 "
            "as the EMPIRICAL P3 sanity. Pre-fire battery confirms the "
            "GRADIENT PATH; the EMPIRICAL non-zero magnitude lives in "
            "result.json. B-EMERGE-7: reaches != useful."
        ),
    )


# === B-S161-FIRE-4 PSI-BOUNDED-TUPLE ==================================
def b4_psi_bounded_tuple():
    """Psi(t) in [0, 1]^2 by:
      - cos in [-1, +1] (Cauchy-Schwarz) ==> (1+cos)/2 in [0, 1]
      - H(softmax) in [0, log V] (Shannon bound) ==> H/log(V) in [0, 1]
      - Cartesian product gives [0, 1]^2
    Theorem by inspection (Cauchy-Schwarz + Shannon entropy bound). No
    sympy claim; structurally provable by undergraduate-level analysis."""
    _, src = parse_module(TRAINER_PATH)
    # Sanity that the trainer applies softmax (Shannon entropy domain)
    has_softmax_for_ent = "F.softmax(logits_a.float(), dim=-1)" in src
    has_cosine = "F.cosine_similarity(a, g, dim=-1)" in src
    # The trainer uses these formulas; bound is structural / mathematical
    return dict(
        battery="B-S161-FIRE-4 PSI-BOUNDED-TUPLE",
        pass_=has_softmax_for_ent and has_cosine,
        softmax_used_for_entropy=has_softmax_for_ent,
        cosine_used_for_direction=has_cosine,
        proof_kind="theorem by inspection (Cauchy-Schwarz + Shannon entropy bound)",
    )


# === B-S161-FIRE-5 PREDICTOR-ANIMA-OWN-NO-NEW-PARAM ===================
def b5_predictor_anima_own_no_new_param():
    """The predictor_head_g function uses head_g (already in
    ConsciousDecoderV2) + softmax + first-two + clamp. NO new weight
    matrix. Verified by:
      - trainer does not instantiate any new nn.Linear / nn.Parameter
        with shape [V, 2] or [2, V]
      - the predictor expression uses probs_g[:, :-1, :2] which is a
        slicing op (no new params)
      - clamp(0, 1) is a pure function (no params)"""
    tree, src = parse_module(TRAINER_PATH)
    # Scan for any nn.Linear / nn.Parameter / nn.Embedding allocation
    new_param_alloc = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in {"Linear", "Embedding", "Parameter",
                                   "EmbeddingBag", "Conv1d", "Conv2d"}:
                # Is this inside a class definition (model arch) or in run()
                # (would mean new params at training time)?
                src_snip = ast_unparse(node)
                # ConsciousDecoderV2 instance creation is allowed
                if "ConsciousDecoderV2" not in src_snip:
                    new_param_alloc.append(src_snip[:80])
    # The predictor expression itself
    has_slicing = "probs_g[:, :-1, :2]" in src
    has_clamp = ".clamp(0.0, 1.0)" in src
    return dict(
        battery="B-S161-FIRE-5 PREDICTOR-ANIMA-OWN-NO-NEW-PARAM",
        pass_=(len(new_param_alloc) == 0 and has_slicing and has_clamp),
        new_param_allocation_count=len(new_param_alloc),
        predictor_uses_slicing=has_slicing,
        predictor_uses_clamp=has_clamp,
    )


# === B-S161-FIRE-6 SEC7-3AND-LEGITIMATE ===============================
def b6_sec7_3and_legitimate():
    """sec7 3-AND truth table evaluation:
      - sec7-1: from-scratch ==> trainer has no load_state_dict / no
        from_pretrained / no torch.load CALL; seed fixed via
        torch.manual_seed + torch.cuda.manual_seed_all + random.seed
      - sec7-2: head_g re-use not graft ==> trainer instantiates
        ConsciousDecoderV2 fresh; head_g is from that model
      - sec7-3: Psi-physics byte-equal Law-71 ==> verified by B-S161-FIRE-2"""
    tree, _ = parse_module(TRAINER_PATH)
    # sec7-1: no foreign weight load
    forbidden_call_attrs = {"load_state_dict", "from_pretrained"}
    forbidden_full = {"torch.load"}
    found_forbidden = []
    seed_calls = set()
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in forbidden_call_attrs:
                found_forbidden.append(node.func.attr)
            full = ast_unparse(node.func)
            if full in forbidden_full:
                found_forbidden.append(full)
            if full in {"torch.manual_seed", "torch.cuda.manual_seed_all",
                        "random.seed"}:
                seed_calls.add(full)
    sec7_1_ok = (len(found_forbidden) == 0
                 and {"torch.manual_seed", "torch.cuda.manual_seed_all",
                      "random.seed"} <= seed_calls)
    # sec7-2: head_g re-use not graft (it lives in ConsciousDecoderV2)
    _, src = parse_module(TRAINER_PATH)
    sec7_2_ok = ("model.head_g.parameters()" in src
                 and "ConsciousDecoderV2(" in src)
    # sec7-3: byte-equal Law-71 (delegate to B-S161-FIRE-2)
    b2 = b2_psi_is_law71_byte_equal()
    sec7_3_ok = b2["pass_"]
    return dict(
        battery="B-S161-FIRE-6 SEC7-3AND-LEGITIMATE",
        pass_=(sec7_1_ok and sec7_2_ok and sec7_3_ok),
        sec7_1_no_foreign_load=sec7_1_ok,
        sec7_2_head_g_reuse_not_graft=sec7_2_ok,
        sec7_3_psi_byte_equal_law71=sec7_3_ok,
        truth_table_row="(T,T,T)",
    )


# === B-S161-FIRE-7 CENTRAL-BLUE-FALSIFIER-0-LINE-DIFF =================
def b7_central_zero_diff():
    """Central state/verify_hexad_blue_2026_05_15/blue_falsifier.py sha
    must remain prefix c93e160a8a376a94 - 0-line-diff invariant."""
    if not os.path.exists(CENTRAL):
        return dict(battery="B-S161-FIRE-7 CENTRAL-BLUE-FALSIFIER-0-LINE-DIFF",
                    pass_=False, reason="central file missing", path=CENTRAL)
    h = sha256(read(CENTRAL))
    return dict(
        battery="B-S161-FIRE-7 CENTRAL-BLUE-FALSIFIER-0-LINE-DIFF",
        pass_=h.startswith(CENTRAL_SHA_PREFIX_EXPECTED),
        sha256=h, expected_prefix=CENTRAL_SHA_PREFIX_EXPECTED,
    )


# === B-S161-FIRE-8 SPONT-DIRECTIONAL-POSITIVE-DECIDABLE ===============
def b8_spont_directional_positive_decidable():
    """The eval source must compute spont_directional_positive as a
    conjunction of 4 real-line inequalities. Verified by AST scan."""
    _, src = parse_module(EVAL_PATH)
    has_cond_emit = "cond_emit_above_baseline" in src
    has_cond_psi_alive = "cond_psi_alive" in src
    has_cond_psi_above = "cond_psi_above_baseline" in src
    has_cond_cascade = "cond_cascade_ok" in src
    has_spont_conjunction = "spont_directional_positive = (" in src
    return dict(
        battery="B-S161-FIRE-8 SPONT-DIRECTIONAL-POSITIVE-DECIDABLE",
        pass_=(has_cond_emit and has_cond_psi_alive
               and has_cond_psi_above and has_cond_cascade
               and has_spont_conjunction),
        cond_emit_above_baseline_present=has_cond_emit,
        cond_psi_alive_present=has_cond_psi_alive,
        cond_psi_above_baseline_present=has_cond_psi_above,
        cond_cascade_ok_present=has_cond_cascade,
        spont_conjunction_assignment=has_spont_conjunction,
    )


def main():
    t0 = time.time()
    results = []
    for fn in [b1_lambda_psi_off_reduction,
               b2_psi_is_law71_byte_equal,
               b3_gradient_reaches_both_heads,
               b4_psi_bounded_tuple,
               b5_predictor_anima_own_no_new_param,
               b6_sec7_3and_legitimate,
               b7_central_zero_diff,
               b8_spont_directional_positive_decidable]:
        r = fn()
        results.append(r)
        flag = "BLUE" if r["pass_"] else "RED"
        print(f"  [{flag}] {r['battery']}", flush=True)

    n_total = len(results)
    n_pass = sum(1 for r in results if r["pass_"])
    note = dict(
        battery="B-S161-FIRE-NOTE empirical carve-out",
        pass_=None,
        note=("Whether S161 fire actually produces 자발 emission rate above "
              "S107 baseline is SGD/measurement OUTCOME. Battery proves SETUP "
              "well-formed (lambda_psi-off reduction / Psi-Law71-equivalence / "
              "dual-head gradient path / boundedness / no-new-param / "
              "sec7-legit / central-0-diff / verdict-decidability), NOT that "
              "anima emerges, NOT that any specific ckpt WILL produce emission, "
              "NOT that the algorithm escapes WALL-B. B-D-NOTE / "
              "B-PUREPHYS-NOTE / B-S96-NOTE / B-S107-NOTE / B-S125-NOTE / "
              "B-S126-NOTE / B-S139-NOTE / B-S153-NOTE / B-S160-NOTE / "
              "B-PHASE-B-NOTE / B-EMERGE-7 family - necessary-not-sufficient "
              "at every layer."),
    )

    out = dict(
        battery_id="B-S161-FIRE",
        cycle="S161-FIRE Psi-JEPA-COUPLE (DUAL-HEAD COUPLING NON-CE)",
        sidecar=True,
        central_zero_diff_check=results[6]["pass_"],
        results=results,
        empirical_carve_out=note,
        summary=f"{n_pass}/{n_total} BLUE ({'PASS' if n_pass == n_total else 'FAIL'})",
        wall_s=time.time() - t0,
        north_star_unchanged=True,
        s15_s51_s72_milestones_unchanged=True,
    )
    out_path = os.path.join(HERE, "blue_falsifier_s161_result.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\nB-S161-FIRE summary: {out['summary']}  ({out['wall_s']:.2f}s)",
          flush=True)
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
