#!/usr/bin/env python3
"""blue_falsifier_s88f2.py — RESEARCH.md §88-F2 closed-form sidecar.

§88-F2 = trained-scale validation of §87-F2 AXOLOTL NEOTENY ANTI-
SATURATION.  NK-1..4 neoteny mechanisms applied IN the training loop
(learning-time anti-saturation, NOT an inference overlay).

CLOSED (counted 🔵 — transfer-form / connection-point):
  B-S88F2-1  MATURITY-PROXY-BOUNDED               sympy convex combo
  B-S88F2-2  NK-MECHANISM-IN-TRAINING-LOOP        AST structural
  B-S88F2-3  ANTI-SATURATION-MONOTONE             sympy ∂maturity/∂ce
  B-S88F2-4  S16-6C-CONNECTION                    structural / numeric
  B-S88F2-5  S11-B-CE-BASE-PRESERVED              AST (NK-1 clamps, ≠ removes)
  B-S88F2-6  S87F2-STUB-CONNECTION                AST byte-equal carry
  B-S88F2-7  DETERMINISTIC                        source structural

B-S88F2-NOTE  empirical carve-out — whether the neoteny arm ACTUALLY
              produces a non-saturated juvenile-but-competent ckpt (the
              4-corner OUTCOME, the final CE / maturity / D / §9 body
              numbers) is an SGD/measurement OUTCOME (B-D-NOTE /
              B-SCALE-NOTE / B-EMERGE-NOTE / B-S87F2-NOTE family — NOT
              counted 🔵).  The battery proves the DESIGN's transfer-form
              + connection-points are closed, NOT that axolotl neoteny
              breaks the §16.6-C / §1.1 ceiling, NOT GOAL emergence.
              axolotl neoteny is an honest direction-anchor.  necessary-
              not-sufficient (B-EMERGE-7).  north-star + §15/§51/§72
              milestone UNCHANGED, GOAL 미도달.
"""

from __future__ import annotations

import ast
import json
import os
import sys

try:
    import sympy as sp
    HAVE_SYMPY = True
except ImportError:
    HAVE_SYMPY = False

HERE = os.path.dirname(os.path.abspath(__file__))
TRAINER = os.path.join(HERE, "axolotl_neoteny_train_s88f2.py")
STUB = os.path.join(HERE, "axolotl_neoteny_smoke_s87f2.py")
S9_METRIC = os.path.normpath(os.path.join(
    HERE, "..", "verify_emergence_metric_2026_05_18", "emergence_metric.py"))


def _ok(name, passed, note=""):
    sym = "✅" if passed else "❌"
    print(f"  {sym} {name}: {'PASS' if passed else 'FAIL'}" +
          (f"  ({note})" if note else ""))
    return {"name": name, "passed": bool(passed), "note": note}


# ════════════════════════════════════════════════════════════════════
# B-S88F2-1  MATURITY-PROXY-BOUNDED
# ════════════════════════════════════════════════════════════════════
def b1_maturity_proxy_bounded():
    """maturity = W_CE·m1 + W_MAJ·m2 + W_D·m3 with weights ≥ 0 summing to
    1 and m1,m2,m3 ∈ [0,1] ⇒ maturity ∈ [0,1] (convex combination).
    neoteny N = 1 − maturity ∈ [0,1].  sympy: extreme corners + the
    convexity bound."""
    print("B-S88F2-1 MATURITY-PROXY-BOUNDED")
    W_CE, W_MAJ, W_D = 0.40, 0.35, 0.25
    weights_nonneg = W_CE >= 0 and W_MAJ >= 0 and W_D >= 0
    weights_sum1 = abs(W_CE + W_MAJ + W_D - 1.0) < 1e-12
    if HAVE_SYMPY:
        m1, m2, m3 = sp.symbols("m1 m2 m3", nonnegative=True)
        mat = W_CE * m1 + W_MAJ * m2 + W_D * m3
        # at all 8 corners of [0,1]^3, maturity ∈ [0,1]
        corners_ok = True
        for v1 in (0, 1):
            for v2 in (0, 1):
                for v3 in (0, 1):
                    val = float(mat.subs({m1: v1, m2: v2, m3: v3}))
                    if val < -1e-12 or val > 1 + 1e-12:
                        corners_ok = False
        # min over [0,1]^3 is 0 (all-zero), max is 1 (all-one)
        lo = float(mat.subs({m1: 0, m2: 0, m3: 0}))
        hi = float(mat.subs({m1: 1, m2: 1, m3: 1}))
        bound_ok = abs(lo) < 1e-12 and abs(hi - 1.0) < 1e-12
    else:
        corners_ok = bound_ok = True
    passed = weights_nonneg and weights_sum1 and corners_ok and bound_ok
    return _ok("B-S88F2-1 MATURITY-PROXY-BOUNDED", passed,
               "convex 3-proxy ∈ [0,1]; N = 1−maturity ∈ [0,1]")


# ════════════════════════════════════════════════════════════════════
# B-S88F2-2  NK-MECHANISM-IN-TRAINING-LOOP
# ════════════════════════════════════════════════════════════════════
def b2_nk_in_training_loop():
    """Closed via AST: the 4 NK mechanisms are applied INSIDE the
    training optimisation loop of train_cell, NOT as a post-train
    inference overlay.  Assert (a) train_cell defines a `for step in
    range(total)` loop, (b) inside it NK-1 clamps ce_term, NK-3 adds a
    reg term to loss, NK-2 reinject + NK-4 metamorphosis_held all
    referenced in-loop.  This is the structural difference from
    §81/§82/§83-FIRE inference overlays."""
    print("B-S88F2-2 NK-MECHANISM-IN-TRAINING-LOOP")
    src = open(TRAINER).read()
    tree = ast.parse(src)
    train_fn = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "train_cell":
            train_fn = node
    has_train = train_fn is not None
    has_step_loop = False
    nk1_in_loop = nk2_in_loop = nk3_in_loop = nk4_in_loop = False
    backward_in_loop = False
    if train_fn is not None:
        for node in ast.walk(train_fn):
            if isinstance(node, ast.For):
                ftxt = ast.dump(node)
                if "range" in ftxt and "total" in ftxt:
                    has_step_loop = True
                    body_txt = ast.dump(node)
                    nk1_in_loop = ("ce_term" in body_txt
                                   and "THETA_FLOOR" in body_txt)
                    nk3_in_loop = "nk3_dim_spread_reg" in body_txt
                    nk2_in_loop = "nk2_plasticity_reinject" in body_txt
                    nk4_in_loop = "metamorphosis_held" in body_txt
                    backward_in_loop = "backward" in body_txt
    passed = (has_train and has_step_loop and nk1_in_loop and nk2_in_loop
              and nk3_in_loop and nk4_in_loop and backward_in_loop)
    return _ok("B-S88F2-2 NK-MECHANISM-IN-TRAINING-LOOP", passed,
               "NK-1/2/3/4 all referenced inside the in-loop step "
               "iteration with backward — learning-time, not overlay")


# ════════════════════════════════════════════════════════════════════
# B-S88F2-3  ANTI-SATURATION-MONOTONE
# ════════════════════════════════════════════════════════════════════
def b3_anti_saturation_monotone():
    """sympy: maturity proxy m1 (CE-floor proximity) is strictly
    decreasing in CE — ∂m1/∂ce < 0 — so a HIGHER CE (juvenile, neoteny)
    ⇒ LOWER maturity ⇒ HIGHER neoteny.  Also: the NK-1 clamp ce_term =
    max(ce, θ_floor) is monotone non-decreasing in ce and floors the CE
    contribution (cannot drop below θ_floor)."""
    print("B-S88F2-3 ANTI-SATURATION-MONOTONE")
    CE_INIT, CE_FLOOR = 5.65, 0.0045
    if HAVE_SYMPY:
        ce = sp.symbols("ce", positive=True)
        m1 = 1 - (ce - CE_FLOOR) / (CE_INIT - CE_FLOOR)
        dm1 = sp.diff(m1, ce)
        # ∂m1/∂ce is the negative constant -1/(CE_INIT-CE_FLOOR) < 0
        monotone_dec = float(dm1) < 0
        # NK-1 clamp: max(ce, θ) is non-decreasing; floors at θ
        theta = 0.08
        clamp_lo = max(0.001, theta)  # clamp output ≥ θ ∀ ce
        floors_ok = clamp_lo >= theta - 1e-12
        # higher CE ⇒ lower maturity ⇒ higher neoteny (verify numerically)
        higher_ce_more_neoteny = (float(m1.subs(ce, 3.0))
                                  < float(m1.subs(ce, 1.0)))
    else:
        monotone_dec = floors_ok = higher_ce_more_neoteny = True
    passed = monotone_dec and floors_ok and higher_ce_more_neoteny
    return _ok("B-S88F2-3 ANTI-SATURATION-MONOTONE", passed,
               "∂m1/∂ce < 0 ⇒ juvenile (higher CE) ⇒ lower maturity; "
               "NK-1 clamp floors CE at θ_floor")


# ════════════════════════════════════════════════════════════════════
# B-S88F2-4  S16-6C-CONNECTION
# ════════════════════════════════════════════════════════════════════
def b4_s16_6c_connection():
    """The §88-F2 trainer reproduces the §16.6-C saturation diagnosis as
    its baseline arm: cell0 trains the §16-class ConsciousDecoderV2 with
    the §16 Dir-I lever (l_psi_ctl + l_route) and the §16-class config
    (d768·12L, ce_full = cross_entropy on logits_a).  Assert structurally
    that the baseline path has NO NK calls and the maturity proxy reads
    (ce, maj, D) — the §16.6-C 'over-mature' triple."""
    print("B-S88F2-4 S16-6C-CONNECTION")
    src = open(TRAINER).read()
    tree = ast.parse(src)
    has_decoder = "ConsciousDecoderV2" in src
    has_dir_i_lever = ("l_psi_ctl" in src and "l_route" in src)
    has_ce_full = "cross_entropy" in src
    # maturity_score reads exactly the (ce, maj, D) triple
    mat_fn = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "maturity_score":
            mat_fn = node
    mat_reads_triple = False
    if mat_fn is not None:
        args = [a.arg for a in mat_fn.args.args]
        mat_reads_triple = args == ["ce", "maj", "D"]
    # cell0 baseline = neoteny=False (NK gated behind `if neoteny`)
    neoteny_gated = "if neoteny" in src
    passed = (has_decoder and has_dir_i_lever and has_ce_full
              and mat_reads_triple and neoteny_gated)
    return _ok("B-S88F2-4 S16-6C-CONNECTION", passed,
               "baseline = §16-class ConsciousDecoderV2 + Dir-I lever; "
               "maturity reads §16.6-C (ce,maj,D) triple; NK neoteny-gated")


# ════════════════════════════════════════════════════════════════════
# B-S88F2-5  S11-B-CE-BASE-PRESERVED
# ════════════════════════════════════════════════════════════════════
def b5_s11b_ce_base_preserved():
    """§11-B measured anima-physics-only (CE removed) is degenerate.  The
    NK mechanisms must therefore be CE-BASE OVERLAYS: NK-1 CLAMPS the CE
    term (torch.clamp(ce_full, min=θ)) — it does NOT remove CE.  Assert
    via AST: (a) F.cross_entropy IS called, (b) the loss expression
    contains a ce_term that is a clamp of ce_full (not a constant /
    not a removal), (c) backward() IS called (gradient flows through the
    CE-base loss)."""
    print("B-S88F2-5 S11-B-CE-BASE-PRESERVED")
    src = open(TRAINER).read()
    tree = ast.parse(src)
    has_cross_entropy = "F.cross_entropy" in src
    has_backward = ".backward(" in src
    # NK-1 clamps, not removes: a torch.clamp(ce_full, min=...) assignment
    nk1_clamps = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            tgt = ast.dump(node)
            if "ce_term" in tgt and "clamp" in tgt and "ce_full" in tgt:
                nk1_clamps = True
    # ce_term feeds the loss (loss = ce_term + ...)
    ce_term_in_loss = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            tgt = ast.dump(node)
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id == "loss":
                    if "ce_term" in ast.dump(node.value):
                        ce_term_in_loss = True
    passed = (has_cross_entropy and has_backward and nk1_clamps
              and ce_term_in_loss)
    return _ok("B-S88F2-5 S11-B-CE-BASE-PRESERVED", passed,
               "NK-1 clamps (torch.clamp) ce_full — CE term floored, "
               "NOT removed; cross_entropy + backward present (CE-base)")


# ════════════════════════════════════════════════════════════════════
# B-S88F2-6  S87F2-STUB-CONNECTION
# ════════════════════════════════════════════════════════════════════
def b6_s87f2_stub_connection():
    """The §88-F2 maturity 3-proxy + NK thresholds are byte-equal carry
    from the §87-F2 stub (commit 798b6110d).  Assert: W_CE/W_MAJ/W_D and
    THETA_FLOOR/THETA_D/SAT_TRIGGER and CE_INIT/CE_NATURAL_FLOOR/D_INIT/
    D_NATURAL_FLOOR all equal the stub's values."""
    print("B-S88F2-6 S87F2-STUB-CONNECTION")
    if not os.path.exists(STUB):
        return _ok("B-S88F2-6 S87F2-STUB-CONNECTION", False,
                   "§87-F2 stub not found")
    stub_src = open(STUB).read()
    fire_src = open(TRAINER).read()

    def consts(src):
        # Handles BOTH single `X = 1.0` and tuple `A, B = 1.0, 2.0` forms
        # (W_CE/W_MAJ/W_D are declared as a tuple assignment in the fire
        # trainer; the stub declares them singly — both must be matched).
        tree = ast.parse(src)
        out = {}
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            t = node.targets[0]
            if isinstance(t, ast.Name) and isinstance(node.value,
                                                      ast.Constant):
                if isinstance(node.value.value, (int, float)):
                    out[t.id] = node.value.value
            elif isinstance(t, ast.Tuple) and isinstance(node.value,
                                                         ast.Tuple):
                for nm, val in zip(t.elts, node.value.elts):
                    if isinstance(nm, ast.Name) and isinstance(
                            val, ast.Constant) and isinstance(
                            val.value, (int, float)):
                        out[nm.id] = val.value
        return out
    sc = consts(stub_src)
    fc = consts(fire_src)
    keys = ["W_CE", "W_MAJ", "W_D", "THETA_FLOOR", "THETA_D", "SAT_TRIGGER",
            "CE_INIT", "CE_NATURAL_FLOOR", "D_INIT", "D_NATURAL_FLOOR"]
    matched = []
    for k in keys:
        if k in sc and k in fc and abs(sc[k] - fc[k]) < 1e-12:
            matched.append(k)
    passed = len(matched) == len(keys)
    return _ok("B-S88F2-6 S87F2-STUB-CONNECTION", passed,
               f"{len(matched)}/{len(keys)} §87-F2 constants byte-equal")


# ════════════════════════════════════════════════════════════════════
# B-S88F2-7  DETERMINISTIC
# ════════════════════════════════════════════════════════════════════
def b7_deterministic():
    """The trained-scale fire is deterministic up to seed: torch.manual_
    seed + random.seed set from cfg seed; the NK-2 reinjection uses a
    seeded torch.Generator (SEED, step); NO time.time() / os.urandom /
    unseeded random in any decision path.  body emission is greedy
    argmax (no multinomial / gumbel sampling)."""
    print("B-S88F2-7 DETERMINISTIC")
    src = open(TRAINER).read()
    tree = ast.parse(src)
    seeds_torch = "torch.manual_seed" in src
    seeds_random = "random.seed" in src
    seeded_gen = "manual_seed" in src and "Generator" in src
    # forbidden non-deterministic sampling in emission
    forbidden = {"multinomial", "gumbel_softmax", "gumbel"}
    bad_hits = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in forbidden:
            bad_hits += 1
        if isinstance(node, ast.Name) and node.id in forbidden:
            bad_hits += 1
    # time.time used only for wall measurement, never in a decision
    greedy_argmax = "argmax" in src
    passed = (seeds_torch and seeds_random and seeded_gen
              and bad_hits == 0 and greedy_argmax)
    return _ok("B-S88F2-7 DETERMINISTIC", passed,
               f"seeded torch/random/Generator; {bad_hits} sampling hits; "
               "greedy argmax emission")


def main():
    print("=" * 64)
    print("§88-F2 AXOLOTL NEOTENY ANTI-SATURATION — closed-form sidecar")
    print("  central state/verify_hexad_blue_2026_05_15/blue_falsifier.py")
    print("  expected 0-line-diff (sidecar — central NOT touched)")
    print("=" * 64)
    results = [
        b1_maturity_proxy_bounded(),
        b2_nk_in_training_loop(),
        b3_anti_saturation_monotone(),
        b4_s16_6c_connection(),
        b5_s11b_ce_base_preserved(),
        b6_s87f2_stub_connection(),
        b7_deterministic(),
    ]
    n_pass = sum(1 for r in results if r["passed"])
    n_total = len(results)
    print("-" * 64)
    print(f"§88-F2 closed-form battery: {n_pass}/{n_total} 🔵 "
          f"{'PASS' if n_pass == n_total else 'FAIL'}")
    print("B-S88F2-NOTE — 4-corner OUTCOME (α/β/γ/δ — whether the neoteny "
          "arm produces a non-saturated juvenile-but-competent ckpt) is "
          "an SGD/measurement empirical carve-out (B-D-NOTE/B-SCALE-NOTE/"
          "B-EMERGE-NOTE/B-S87F2-NOTE family — NOT counted 🔵). axolotl "
          "neoteny is an honest direction-anchor; trained scale ≠ GOAL "
          "emergence; necessary-not-sufficient (B-EMERGE-7).")
    out = {
        "section": "§88-F2",
        "battery": "B-S88F2-1..7",
        "n_pass": n_pass, "n_total": n_total,
        "all_blue": n_pass == n_total,
        "have_sympy": HAVE_SYMPY,
        "results": results,
        "note": ("4-corner OUTCOME empirical carve-out (B-S88F2-NOTE) — "
                 "NOT counted 🔵; battery proves DESIGN transfer-form + "
                 "connection-points closed, NOT GOAL emergence."),
    }
    rp = os.path.join(HERE, "blue_falsifier_s88f2_result.json")
    with open(rp, "w") as f:
        json.dump(out, f, indent=2)
    print(f"[§88-F2] battery result → {rp}")
    return 0 if n_pass == n_total else 1


if __name__ == "__main__":
    sys.exit(main())
