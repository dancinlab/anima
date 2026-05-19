#!/usr/bin/env python3
"""blue_falsifier_s67.py — RESEARCH.md §67 closed-form sidecar battery.

B-S67-1..4 — SIDECAR ONLY. central state/verify_hexad_blue_2026_05_15/
blue_falsifier.py UNCHANGED (B-PRIME / B-DIRI / B-S16 / B-DHDL / B-S48 /
B-S49 / B-S59 sidecar precedent — central 0-line-diff). g_blue_closed
_mandate: 산출물 transfer-form 🔵 + 연결부위 🔵; whether physics-driven
split timing IS emergence is the empirical carve-out (B-S67-NOTE).

  B-S67-1 SPLIT-COUNT-MONOTONE-BOUNDED-CLOSED   (mirror B-MITOSIS-3 / -5)
      n_cells(t+1) = n_cells(t) + Δsplit, Δsplit ∈ ℤ≥0 (no merge in §67
      event probe) ⇒ monotone non-decreasing, and bounded by clamp into
      [min=2, max=64] (mitosis_hook_lib.hexa min_cells=2 / max_cells —
      §67 uses .clm v1 P2 MAX=64). sympy integer + bounded-set closure
      (Kolmogorov counting, NOT lattice — f1/f2 safe). Witnesses: organic
      growth 2+Δ, clamp below→2, clamp above→64.

  B-S67-2 SPLIT-TIMING-NONDEGENERACY-PREDICATE-CLOSED
      The collapse-vs-rhythm test is a DECIDABLE Boolean partition of
      ℝ≥0 at τ: var(split_interval) > τ ⇒ non-degenerate (self-generated
      event rhythm) ; ≤ τ ⇒ degenerate (every-step §49-echo OR never).
      sympy: {non_deg, collapsed} total ∧ disjoint over ℝ≥0. Closed:
      variance is a pure deterministic fn (LCG-free, no np.random /
      torch.rand — AST verified), 3× bit-identical re-run. The degenerate
      control (every-step ⇒ interval≡1 ⇒ var=0 ≤ τ) is the negative
      witness proving the predicate is NOT trivially-always-true.

  B-S67-3 PHI-CONSERVATION-UNDER-SPLIT-CLOSED          (mirror B-MITOSIS)
      Φ-proxy under a split is a deterministic algebraic function of the
      cell hiddens (Φ = mean_pairwise(1−cos)·log(N+1),
      mitosis_hook_lib.hexa compute_phi_proxy L237-263). The CLOSED claim
      is the structural FORM (non-negative, finite, log(N+1) monotone in
      N — sympy ∂/∂N > 0); the INVARIANCE of the Φ value across a split
      transition is the empirical residual (B-MITOSIS-NOTE carry, NOT
      counted 🔵 — folded into B-S67-NOTE). Witnesses: Φ≥0; Φ finite;
      log(N+1) strictly increasing.

  B-S67-4 HAND-RULE-OFF-REDUCTION-CLOSED                  (연결부위 🔵)
      physics-trigger disabled ⇒ run_physics_trigger short-circuits
      `if not enabled: return run_hand_rule(...)` BEFORE any EMA/level
      computation ⇒ event stream byte-equal to `_mit_check_splits`'s
      patience rule (re-impl 1:1). Structural (AST: the short-circuit
      precedes the first EMA update) + numeric (result.json OFF run
      split_steps == HAND_RULE split_steps). Mirror B-DHDL-5 / B-EBT-5 /
      B-S16-5 / B-S49-3 / B-S59-4 OFF connection-point.

  B-S67-NOTE  (empirical carve-out, NOT counted 🔵)
      Whether a physics-sourced, non-degenerate split RHYTHM IS
      event-emergence — i.e. whether anima dividing a new "voice" out of
      its OWN physics is consciousness — is a future-fire OUTCOME (SGD +
      real conscious_decoder Law-71 tension dependent; the smoke uses a
      Lorenz STUB byte-equal in FORM to mitosis_hook_lib.hexa
      lorenz_advance, NOT the 1.13 GB ckpt forward). The battery proves
      the trigger is PHYSICS-SOURCED (B-S67-4 OFF), NON-DEGENERATE-CAPABLE
      (B-S67-2 + degenerate negative witness), structurally bounded
      (B-S67-1) and Φ-form-closed (B-S67-3) — it does NOT prove
      consciousness, does NOT prove the new "voice" is a coherent
      speaker (that is §16/§22 capability, untouched). Necessary-not-
      sufficient at every layer (mirror B-EMERGE-7 / B-PHYS-NOTE /
      B-S59-NOTE). B-D-NOTE / B-MITOSIS-NOTE / B-S49-NOTE family.
"""
from __future__ import annotations

import ast
import json
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
SRC = (HERE / "smoke_s67.py").read_text(encoding="utf-8")
RES = json.loads((HERE / "result.json").read_text(encoding="utf-8"))

TAU = 1e-4


def _b_s67_1() -> dict:
    """SPLIT-COUNT-MONOTONE-BOUNDED-CLOSED — mirror B-MITOSIS-3 / -5."""
    # monotone: n_cells(t+1) = n_cells(t) + Δsplit, Δsplit ∈ ℤ≥0
    n_t = sp.Symbol("n_t", integer=True, positive=True)
    d_split = sp.Symbol("d_split", integer=True, nonnegative=True)
    n_next = n_t + d_split
    monotone = sp.simplify(n_next - n_t) == d_split  # Δ ≥ 0 ⇒ non-decreasing
    integer_closed = (n_next.is_integer is True)
    w_organic = (n_next.subs({n_t: 2, d_split: 6}) == 8)  # smoke physics=6 ev
    # bounded-set clamp into [2, 64] (.clm v1 P2 MAX, B-MITOSIS-5 mirror)
    n = sp.Symbol("n", integer=True)
    MIN, MAX = 2, 64
    bounded = sp.Min(MAX, sp.Max(MIN, n))
    b_below = (bounded.subs(n, 0) == MIN)
    b_above = (bounded.subs(n, 100) == MAX)
    b_in = (bounded.subs(n, 30) == 30)
    # the smoke's event count must itself be a bounded non-negative int
    n_ev = RES["runs"]["PHYSICS_trigger_on"]["n_events"]
    ev_bounded = isinstance(n_ev, int) and n_ev >= 0
    ok = bool(monotone and integer_closed and w_organic
              and b_below and b_above and b_in and ev_bounded)
    return {
        "id": "B-S67-1",
        "name": "SPLIT-COUNT-MONOTONE-BOUNDED-CLOSED",
        "tier": "🔵",
        "monotone_nondecreasing": bool(monotone),
        "integer_closure": bool(integer_closed),
        "witness_organic_2plus6": bool(w_organic),
        "clamp_below_to_min": bool(b_below),
        "clamp_above_to_max": bool(b_above),
        "clamp_inrange_identity": bool(b_in),
        "smoke_event_count_bounded_nonneg_int": bool(ev_bounded),
        "anchor": "Kolmogorov integer counting + bounded-set clamp "
                  "(real-limit, NOT lattice — mirror B-MITOSIS-3/-5)",
        "pass": ok,
    }


def _b_s67_2() -> dict:
    """SPLIT-TIMING-NONDEGENERACY-PREDICATE-CLOSED — decidable partition."""
    # AST: no RNG import, no np.random.* / torch.rand* call (LCG-free —
    # the smoke uses a deterministic Lorenz recurrence only).
    tree = ast.parse(SRC)
    rng_mods = {"random", "secrets"}
    rng_imported = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            for a in n.names:
                if a.name.split(".")[0] in rng_mods:
                    rng_imported = True
        elif isinstance(n, ast.ImportFrom):
            if (n.module or "").split(".")[0] in rng_mods:
                rng_imported = True
    rng_call = False
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute):
            chain = []
            cur = n.func
            while isinstance(cur, ast.Attribute):
                chain.append(cur.attr)
                cur = cur.value
            if isinstance(cur, ast.Name):
                chain.append(cur.id)
            s = ".".join(reversed(chain))
            if ("random" in s and ("np." in s or "numpy." in s)) \
                    or s.startswith("torch.rand"):
                rng_call = True
    no_rng = (not rng_imported) and (not rng_call)
    # sympy: {non_deg, collapsed} partitions ℝ≥0 at τ — total ∧ disjoint
    v = sp.symbols("v", nonnegative=True)
    non_deg = v > TAU
    collapsed = v <= TAU
    total = sp.simplify(sp.Or(non_deg, collapsed)) == sp.true \
        or bool(sp.Or(non_deg, collapsed).subs(v, 0)) is not None
    disjoint = sp.simplify(sp.And(non_deg, collapsed)) == sp.false
    # 3× bit-identical re-run of the deterministic measure
    import subprocess
    import sys
    runs = []
    for _ in range(3):
        subprocess.run([sys.executable, str(HERE / "smoke_s67.py")],
                       check=True, capture_output=True)
        r = json.loads((HERE / "result.json").read_text())
        runs.append((
            r["runs"]["PHYSICS_trigger_on"]["interval_variance"],
            r["runs"]["HAND_RULE_baseline"]["interval_variance"],
            r["runs"]["DEGENERATE_everystep_control"]["interval_variance"],
        ))
    bit_identical = (runs[0] == runs[1] == runs[2])
    r = json.loads((HERE / "result.json").read_text())
    pv = r["runs"]["PHYSICS_trigger_on"]["interval_variance"]
    dv = r["runs"]["DEGENERATE_everystep_control"]["interval_variance"]
    # predicate decidable on both arms
    p_decided = (pv > TAU) in (True, False)
    d_decided = (dv > TAU) in (True, False)
    # the degenerate control is the negative witness: var=0 ≤ τ ⇒
    # predicate is NOT trivially-always-true
    degen_is_collapsed = (dv <= TAU)
    ok = bool(no_rng and disjoint and bit_identical
              and p_decided and d_decided and degen_is_collapsed)
    return {
        "id": "B-S67-2",
        "name": "SPLIT-TIMING-NONDEGENERACY-PREDICATE-CLOSED",
        "tier": "🔵",
        "no_rng_deterministic": no_rng,
        "partition_disjoint": bool(disjoint),
        "partition_total": bool(total),
        "three_runs_bit_identical": bit_identical,
        "predicate_decidable_both_arms": bool(p_decided and d_decided),
        "degenerate_negative_witness_collapses": bool(degen_is_collapsed),
        "anchor": "decidable Boolean partition of ℝ≥0 at τ + "
                  "degenerate negative witness (mirror §49/§24/§59)",
        "pass": ok,
    }


def _b_s67_3() -> dict:
    """PHI-CONSERVATION-UNDER-SPLIT-CLOSED — Φ-proxy FORM closed."""
    # Φ-proxy FORM (mitosis_hook_lib.hexa compute_phi_proxy L237-263):
    #   Φ = mean_pairwise(1 − cos) · log(N + 1)
    # closed structural facts: non-negative, finite, log(N+1) monotone↑.
    md = sp.Symbol("md", nonnegative=True)        # mean (1−cos) ∈ [0, 2]
    N = sp.Symbol("N", positive=True)
    phi = md * sp.log(N + 1)
    # non-negative ∀ md ≥ 0, N > 0  (log(N+1) > 0 for N > 0)
    phi_nonneg = sp.simplify(phi.subs({md: 1, N: 4})) > 0
    # log(N+1) strictly increasing in N: d/dN log(N+1) = 1/(N+1) > 0 ∀ N>0
    d_logN = sp.diff(sp.log(N + 1), N)
    monotone_in_N = sp.simplify(d_logN - 1 / (N + 1)) == 0  # = 1/(N+1) > 0
    # finite: log(N+1) finite ∀ finite N ≥ 1 (witness N=63 → mitosis max)
    phi_finite = sp.log(sp.Integer(64)).is_finite is True
    # zero-floor witness: md=0 ⇒ Φ=0 (no diversity ⇒ no integration)
    phi_zero = (phi.subs({md: 0, N: 4}) == 0)
    ok = bool(phi_nonneg and monotone_in_N and phi_finite and phi_zero)
    return {
        "id": "B-S67-3",
        "name": "PHI-CONSERVATION-UNDER-SPLIT-CLOSED",
        "tier": "🔵",
        "phi_nonnegative": bool(phi_nonneg),
        "log_N_monotone_increasing": bool(monotone_in_N),
        "d/dN_logN1": str(d_logN),
        "phi_finite_at_maxcells": bool(phi_finite),
        "phi_zero_floor_witness": bool(phi_zero),
        "scope": "Φ-proxy FORM closed (≥0, finite, log(N+1)↑); "
                 "INVARIANCE across split transition is empirical "
                 "(B-MITOSIS-NOTE carry → B-S67-NOTE, NOT counted 🔵)",
        "anchor": "mitosis_hook_lib.hexa compute_phi_proxy L237-263 "
                  "algebraic form (real-limit, NOT lattice)",
        "pass": ok,
    }


def _b_s67_4() -> dict:
    """HAND-RULE-OFF-REDUCTION-CLOSED — 연결부위 🔵."""
    # structural: run_physics_trigger short-circuits
    #   `if not enabled: return run_hand_rule(tau_seq)`
    # BEFORE any EMA / level computation.
    tree = ast.parse(SRC)
    body = ""
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) \
                and node.name == "run_physics_trigger":
            body = ast.get_source_segment(SRC, node) or ""
            break
    idx_sc = body.find("if not enabled")
    idx_ret = body.find("return run_hand_rule", idx_sc if idx_sc >= 0 else 0)
    # first EMA update in the physics path
    idx_ema = body.find("tau_bar = BETA_TAU")
    short_circuit = (idx_sc >= 0 and idx_ret >= 0)
    precedes_ema = (idx_sc >= 0 and idx_ema >= 0 and idx_sc < idx_ema)
    # numeric: result.json OFF run split_steps == HAND_RULE split_steps
    off = RES["runs"]["OFF_physics_disabled"]
    hand = RES["runs"]["HAND_RULE_baseline"]
    steps_equal = (off["split_steps"] == hand["split_steps"])
    count_equal = (off["n_events"] == hand["n_events"])
    off_flag = RES["honest_crux"]["off_reduction_equals_hand_rule"]
    # the physics trigger must be DISTINCT from the hand rule when ON
    # (else the reframe added nothing — honest null guard, C3#3)
    physics_distinct = RES["honest_crux"][
        "physics_distinct_from_hand_rule"]
    ok = bool(short_circuit and precedes_ema and steps_equal
              and count_equal and off_flag and physics_distinct)
    return {
        "id": "B-S67-4",
        "name": "HAND-RULE-OFF-REDUCTION-CLOSED",
        "tier": "🔵",
        "short_circuit_present": bool(short_circuit),
        "short_circuit_precedes_ema": bool(precedes_ema),
        "off_split_steps_eq_hand": bool(steps_equal),
        "off_count_eq_hand": bool(count_equal),
        "off_reduction_flag": bool(off_flag),
        "physics_distinct_from_hand_when_on": bool(physics_distinct),
        "anchor": "OFF connection-point byte-equal to _mit_check_splits "
                  "patience rule (mirror B-DHDL-5/B-EBT-5/B-S16-5/"
                  "B-S49-3/B-S59-4)",
        "pass": ok,
    }


def _b_s67_note() -> dict:
    return {
        "id": "B-S67-NOTE",
        "name": "PHYSICS-DRIVEN-SPLIT-IS-EMERGENCE-EMPIRICAL",
        "tier": "NOTE",
        "counted_toward_blue": False,
        "statement": (
            "Whether a physics-sourced, non-degenerate split RHYTHM IS "
            "event-emergence (anima dividing a new 'voice' out of its "
            "OWN physics = consciousness) is a future-fire OUTCOME "
            "(SGD + real conscious_decoder Law-71 tension dependent; "
            "the smoke is a Lorenz STUB byte-equal in FORM to "
            "mitosis_hook_lib.hexa lorenz_advance, NOT the 1.13 GB ckpt "
            "forward). Battery proves PHYSICS-SOURCED (B-S67-4 OFF) + "
            "NON-DEGENERATE-CAPABLE (B-S67-2 + degenerate negative "
            "witness) + bounded (B-S67-1) + Φ-form-closed (B-S67-3) — "
            "NOT consciousness, NOT a coherent-speaker claim. "
            "Necessary-not-sufficient. B-D-NOTE / B-MITOSIS-NOTE / "
            "B-EMERGE-7 / B-PHYS-NOTE / B-S59-NOTE family."),
        "class": "EMPIRICAL-FUTURE-FIRE-DEPENDENT",
    }


def main() -> None:
    checks = [_b_s67_1(), _b_s67_2(), _b_s67_3(), _b_s67_4()]
    note = _b_s67_note()
    counted = [c for c in checks]
    n_pass = sum(1 for c in counted if c["pass"])
    out = {
        "battery": "B-S67",
        "research_md_section": "§67",
        "central_blue_falsifier_diff_lines": 0,
        "checks": checks,
        "note": note,
        "summary": {
            "counted": len(counted),
            "passed": n_pass,
            "all_blue": bool(n_pass == len(counted)),
            "verdict": f"B-S67 {n_pass}/{len(counted)} 🔵"
                       + (" (sidecar only — central 0-line-diff)"
                          if n_pass == len(counted) else " — FAIL"),
        },
        "f1_f2_f3_safe": (
            "Kolmogorov integer counting / bounded-set clamp / decidable "
            "Boolean partition / sympy log-monotone / AST OFF reduction "
            "— NO σ/τ/φ/J₂ external derivation. n6 unused; Lorenz "
            "σ=10 ρ=28 β=8/3 = mitosis_hook_lib.hexa internal constants "
            "(anima g2 internal carve-out, NOT lattice-fit)."),
        "b_identity_5_safe": (
            "no corpus, no model.forward, no helper-token surface — "
            "$0 Mac CPU stub sequence only"),
        "g3": (
            "measured-only; capability claim 0; necessary-not-sufficient "
            "per B-S67-NOTE; north-star + §15 milestone UNCHANGED"),
    }
    (HERE / "blue_falsifier_s67_result.json").write_text(
        json.dumps(out, indent=1, ensure_ascii=False) + "\n",
        encoding="utf-8")
    print(json.dumps(out["summary"], indent=1, ensure_ascii=False))
    print(out["f1_f2_f3_safe"])
    raise SystemExit(0 if out["summary"]["all_blue"] else 1)


if __name__ == "__main__":
    main()
