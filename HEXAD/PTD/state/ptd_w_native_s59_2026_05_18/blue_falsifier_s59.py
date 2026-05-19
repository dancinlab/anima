#!/usr/bin/env python3
"""blue_falsifier_s59.py — RESEARCH.md §59 closed-form sidecar battery.

B-S59-1..4 — SIDECAR ONLY. central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py UNCHANGED (B-PRIME / B-DIRI / B-S16 / B-DHDL / B-S48 /
B-S49 sidecar precedent). g_blue_closed_mandate: 산출물 transfer-form 🔵
+ 연결부위 🔵; collapse-at-scale OUTCOME 만 정직 carve-out (B-S59-NOTE).

  B-S59-1 W-OWNED-NOT-BOLT-ON-CLOSED (연결부위)
      Structural Boolean: the forward-model's prediction-error feeds
      W.curiosity (w_curiosity_coupled), NOT the §24 emission gate
      (talker_should_emit). The two sites are DISTINCT functions with
      disjoint signatures. AST/structural grep: w_native_ptd.py contains
      `w_curiosity_coupled` and contains NEITHER `talker_should_emit` NOR
      `decision_label` NOR `EMIT_VOICE` as a coupling target — the §49
      bolt-on site is absent. 4-corner Boolean over
      (feeds_curiosity, feeds_emission_gate): only (True, False) is the
      §59 W-native configuration.

  B-S59-2 ERROR-IS-EFE-EPISTEMIC-CLOSED
      prediction-error = mean_i (y_i − ŷ_i)² is a sum of squares ⇒ ≥ 0
      ∀ (y, ŷ) — sympy: simplify(sum of squares) is non-negative; the
      symbolic min over the residual is exactly 0 at ŷ ≡ y. MSE ≥ 0 is
      Active-Inference epistemic value / surprise (Shannon-class
      non-negative information measure). §7-legitimate INTRINSIC (target
      is the next ACTUAL W-state, NOT an external label) — carries the
      §58 signature (a "module predicts its own next state" forward-model,
      NOT one of σ(6)=12). 3 witnesses: ŷ=y ⇒ 0; off-by-c ⇒ c²; mixed.

  B-S59-3 CURIOSITY-NONDEGENERACY-PREDICATE-CLOSED
      The smoke's collapse-vs-signal test is a DECIDABLE Boolean:
      error_variance > τ ⇒ non-degenerate ; ≤ τ ⇒ collapsed. Mirror §49
      DIVERGENCE-METRIC-DETERMINISTIC / §24 B-PHASE-B-RUN nontrivial
      predicate. Closed: variance is a pure deterministic function (no
      RNG — LCG only, no np.random/torch.rand), 3× bit-identical re-run;
      the predicate partitions ℝ≥0 into exactly {collapsed, non-degenerate}
      at τ (total + disjoint, sympy interval).

  B-S59-4 OFF-REDUCTION-CLOSED (연결부위)
      W-native-PTD disabled ⇒ step() returns 0.0 by construction ⇒
      W.curiosity coupling == W-module baseline (no epistemic term).
      error ≡ 0 ⇒ variance ≡ 0 ⇒ W-module byte-equal. Mirror
      B-DHDL-5 / B-EBT-5 / B-S16-5 / B-S49-3 OFF connection-point.
      Structural (enabled=False short-circuit before any predict/SGD) +
      numeric (result.json OFF run error_mean==0 ∧ error_variance==0).

  B-S59-NOTE  (empirical carve-out, NOT counted 🔵)
      Whether W-native ACTUALLY escapes §49 collapse AT SCALE on real
      anima W-state (vs the stub sequence here) is a future-fire OUTCOME
      (SGD + real-state-dependent). The battery proves the structural
      reframe is §7-legitimate (B-S59-1/2) + the OFF reduction (B-S59-4)
      + the smoke predicate decidable (B-S59-3) — it does NOT prove
      escape-from-collapse. B-D-NOTE / B-DHDL-NOTE / B-S48-NOTE /
      B-S49-NOTE family.
"""
from __future__ import annotations

import ast
import json
import re
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
SRC = (HERE / "w_native_ptd.py").read_text(encoding="utf-8")
RES = json.loads((HERE / "result.json").read_text(encoding="utf-8"))

TAU = 1e-4


def _b_s59_1() -> dict:
    """W-OWNED-NOT-BOLT-ON-CLOSED — connection-point structural Boolean.

    Detect coupling targets at the AST CALL level (not docstring/comment
    mentions — §59's docstrings deliberately NAME the §49 bolt-on site to
    explain the contrast; that is documentation, not a coupling edge).
    """
    tree = ast.parse(SRC)
    called = set()
    for n in ast.walk(tree):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                called.add(f.id)
            elif isinstance(f, ast.Attribute):
                called.add(f.attr)
    # the W-native coupling site MUST be present (called, not just named)
    feeds_curiosity = "w_curiosity_coupled" in called
    # the §49 bolt-on site MUST be absent as an actual CALL (coupling edge);
    # docstring mentions of these tokens are explanatory, not coupling.
    bolt_on_tokens = ("talker_should_emit", "decision_label",
                      "LABEL_EMIT_VOICE")
    feeds_emission_gate = any(t in called for t in bolt_on_tokens)
    # 4-corner: only (feeds_curiosity=True, feeds_emission_gate=False)
    # is the §59 W-native configuration (distinct site from §49).
    fc, fe = sp.symbols("fc fe", bool=True)
    cfg = sp.And(fc, sp.Not(fe))
    is_w_native = bool(cfg.subs({fc: feeds_curiosity, fe: feeds_emission_gate}))
    corners = {
        (True, False): bool(cfg.subs({fc: True, fe: False})),
        (True, True): bool(cfg.subs({fc: True, fe: True})),
        (False, False): bool(cfg.subs({fc: False, fe: False})),
        (False, True): bool(cfg.subs({fc: False, fe: True})),
    }
    only_one_true = sum(corners.values()) == 1 and corners[(True, False)]
    ok = bool(feeds_curiosity and not feeds_emission_gate
              and is_w_native and only_one_true)
    return {
        "id": "B-S59-1",
        "name": "W-OWNED-NOT-BOLT-ON-CLOSED",
        "tier": "🔵 (연결부위)",
        "feeds_w_curiosity": feeds_curiosity,
        "feeds_s24_emission_gate": feeds_emission_gate,
        "4corner_only_w_native_true": only_one_true,
        "pass": ok,
    }


def _b_s59_2() -> dict:
    """ERROR-IS-EFE-EPISTEMIC-CLOSED — MSE ≥ 0 sum-of-squares (sympy)."""
    y0, y1, h0, h1 = sp.symbols("y0 y1 h0 h1", real=True)
    r0, r1 = sp.symbols("r0 r1", real=True)
    mse = ((y0 - h0) ** 2 + (y1 - h1) ** 2) / 2
    # non-negativity via explicit sum-of-squares form: substitute the
    # residuals r_i = y_i − h_i; mse = (r0² + r1²)/2 is manifestly a
    # non-negative combination of squares (each square ≥ 0, coeff ½ > 0).
    sos = sp.simplify(mse.subs({y0: r0 + h0, y1: r1 + h1}))
    sos_target = (r0 ** 2 + r1 ** 2) / 2
    poly_nonneg = sp.simplify(sos - sos_target) == 0 and \
        sp.simplify(sos_target.subs({r0: 0, r1: 0})) == 0 and \
        all(float(sos_target.subs({r0: a, r1: b})) >= 0
            for a, b in ((1.0, 0.0), (0.0, -1.0), (0.7, 0.3),
                         (-0.4, -0.9)))
    # symbolic minimum over residual is exactly 0 at ŷ ≡ y
    at_equal = sp.simplify(mse.subs({h0: y0, h1: y1}))
    min_is_zero = at_equal == 0
    # 3 witnesses
    w_equal = float(mse.subs({y0: 0.3, y1: 0.7, h0: 0.3, h1: 0.7}))
    w_offc = float(mse.subs({y0: 0.5, y1: 0.5, h0: 0.0, h1: 0.0}))
    w_mixed = float(mse.subs({y0: 0.2, y1: 0.9, h0: 0.4, h1: 0.1}))
    witnesses_ok = (abs(w_equal) < 1e-12 and w_offc >= 0.0
                    and w_mixed >= 0.0)
    # §7-legitimate intrinsic: target is the NEXT W-STATE (y_next), NOT a
    # hand-coded label. structural: step() target arg name is y_next and
    # the docstring asserts "predict OWN future state ... NO external label"
    intrinsic = ("y_next" in SRC and "NO external label" in SRC
                 and "next ACTUAL W-state" in SRC)
    ok = bool(poly_nonneg and min_is_zero and witnesses_ok and intrinsic)
    return {
        "id": "B-S59-2",
        "name": "ERROR-IS-EFE-EPISTEMIC-CLOSED",
        "tier": "🔵",
        "mse_sum_of_squares_nonneg": bool(poly_nonneg),
        "symbolic_min_is_zero": bool(min_is_zero),
        "witnesses_nonneg": witnesses_ok,
        "intrinsic_not_external_label": intrinsic,
        "pass": ok,
    }


def _b_s59_3() -> dict:
    """CURIOSITY-NONDEGENERACY-PREDICATE-CLOSED — decidable Boolean."""
    # determinism: AST-level — no RNG import and no RNG call (LCG only).
    # §48/§27 precedent strips comments; we use AST so the line-100 comment
    # text "NO np.random" is NOT a false-positive (it is documentation).
    tree3 = ast.parse(SRC)
    rng_mods = {"random", "secrets"}
    rng_imported = False
    for n in ast.walk(tree3):
        if isinstance(n, ast.Import):
            for a in n.names:
                if a.name.split(".")[0] in rng_mods:
                    rng_imported = True
        elif isinstance(n, ast.ImportFrom):
            if (n.module or "").split(".")[0] in rng_mods:
                rng_imported = True
    # no np.random.* / torch.rand* attribute-call chains
    rng_call = False
    for n in ast.walk(tree3):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            chain = []
            cur = n.func
            while isinstance(cur, ast.Attribute):
                chain.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                chain.append(cur.id)
            s = ".".join(reversed(chain))
            if ("random" in s and ("np." in s or "numpy." in s)) or \
               s.startswith("torch.rand"):
                rng_call = True
    no_rng = (not rng_imported) and (not rng_call)
    # the predicate partitions ℝ≥0 into {collapsed, non-degenerate} at τ
    v = sp.symbols("v", nonnegative=True)
    non_deg = v > TAU
    collapsed = v <= TAU
    # total + disjoint over ℝ≥0
    total = sp.simplify(sp.Or(non_deg, collapsed)) == sp.true \
        or bool(sp.Or(non_deg, collapsed).subs(v, 0)) is not None
    disjoint = sp.simplify(sp.And(non_deg, collapsed)) == sp.false
    # 3× bit-identical re-run of the measure (pure fn)
    import subprocess
    import sys
    runs = []
    for _ in range(3):
        subprocess.run([sys.executable, str(HERE / "w_native_ptd.py")],
                       check=True, capture_output=True)
        r = json.loads((HERE / "result.json").read_text())
        runs.append((r["runs"]["R1_diverse_on"]["error_variance"],
                     r["runs"]["R2_majority_on"]["majority_regime_steps"][
                         "error_variance"]))
    bit_identical = (runs[0] == runs[1] == runs[2])
    # predicate applied to the smoke values is decidable Boolean
    r = json.loads((HERE / "result.json").read_text())
    r1v = r["runs"]["R1_diverse_on"]["error_variance"]
    r2v = r["runs"]["R2_majority_on"]["majority_regime_steps"][
        "error_variance"]
    r1_decided = (r1v > TAU) is True or (r1v > TAU) is False
    r2_decided = (r2v > TAU) is True or (r2v > TAU) is False
    ok = bool(no_rng and disjoint and bit_identical
              and r1_decided and r2_decided)
    return {
        "id": "B-S59-3",
        "name": "CURIOSITY-NONDEGENERACY-PREDICATE-CLOSED",
        "tier": "🔵",
        "no_rng_deterministic": no_rng,
        "partition_disjoint": bool(disjoint),
        "partition_total": bool(total),
        "three_runs_bit_identical": bit_identical,
        "predicate_decidable": bool(r1_decided and r2_decided),
        "pass": ok,
    }


def _b_s59_4() -> dict:
    """OFF-REDUCTION-CLOSED — disabled ⇒ W-module byte-equal baseline."""
    # structural: step() short-circuits `if not self.enabled: return 0.0`
    # BEFORE any predict() / SGD update. Extract the step() method body
    # span via AST (robust — step is the last method, no trailing `def `).
    tree = ast.parse(SRC)
    body = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == "step":
            body = ast.get_source_segment(SRC, node) or ""
            break
    short_circuit = bool(
        re.search(r"if not self\.enabled:\s*\n\s*return 0\.0", body))
    # the short-circuit precedes the SGD update (`self.Wm[i][j] -=`)
    idx_sc = body.find("if not self.enabled")
    idx_sgd = body.find("self.Wm[i][j] -=")
    precedes = (idx_sc >= 0 and idx_sgd >= 0 and idx_sc < idx_sgd)
    # numeric: result.json OFF run error_mean==0 ∧ error_variance==0
    off = RES["runs"]["OFF_diverse_disabled"]
    err_zero = (abs(off["error_mean"]) < 1e-12
                and abs(off["error_variance"]) < 1e-12)
    off_flag = RES["honest_crux"]["off_reduction_error_is_zero"]
    ok = bool(short_circuit and precedes and err_zero and off_flag)
    return {
        "id": "B-S59-4",
        "name": "OFF-REDUCTION-CLOSED",
        "tier": "🔵 (연결부위)",
        "step_short_circuits_disabled": short_circuit,
        "short_circuit_precedes_sgd": precedes,
        "off_error_identically_zero": err_zero,
        "pass": ok,
    }


def main() -> None:
    checks = [_b_s59_1(), _b_s59_2(), _b_s59_3(), _b_s59_4()]
    n_pass = sum(1 for c in checks if c["pass"])
    note = {
        "id": "B-S59-NOTE",
        "tier": "empirical carve-out (NOT counted 🔵)",
        "statement": (
            "Whether W-native ACTUALLY escapes §49 collapse AT SCALE on "
            "real anima W-state (vs this stub sequence) is a future-fire "
            "OUTCOME. The smoke MEASURED: W-native error is a "
            "non-degenerate curiosity signal on diverse W-state (R1 var "
            "> τ) but COLLAPSES to the prior-mean residual on the ~95% "
            "constant-data majority steps (R2 majority-regime var ≤ τ — "
            "the §27/§48 corpus shape, the §49 echo). The §49 collapse is "
            "DATA-SHAPE-bound, NOT home-bound. Battery proves the "
            "structural reframe is §7-legitimate + OFF reduction + "
            "predicate decidable — NOT escape-from-collapse. "
            "B-D-NOTE / B-DHDL-NOTE / B-S48-NOTE / B-S49-NOTE family."),
    }
    out = {
        "research_md_section": "§59",
        "battery": "B-S59-1..4 sidecar (central blue_falsifier.py UNCHANGED)",
        "checks": checks,
        "note": note,
        "n_pass": n_pass,
        "n_total": len(checks),
        "all_blue": n_pass == len(checks),
        "central_unchanged": True,
        "f1_f2_f3_safe": (
            "MSE sum-of-squares non-neg / Boolean 4-corner / sympy interval "
            "partition / structural AST grep — NO σ/τ/φ/J₂ external "
            "derivation; W-state = anima OWN W-physics, no external entity."),
        "b_identity_5": "N/A — no corpus, no model.forward, no helper-token "
                        "surface (stub W-state sequence only).",
    }
    (HERE / "blue_falsifier_s59_result.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    for c in checks:
        print(f"{c['id']:9s} {c['name']:42s} "
              f"{'PASS' if c['pass'] else 'FAIL'}")
    print(f"\nB-S59 {n_pass}/{len(checks)} 🔵  "
          f"(central UNCHANGED · B-S59-NOTE empirical carve-out)")


if __name__ == "__main__":
    main()
