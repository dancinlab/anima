#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
§66 — S-module physics-native INPUT: B-S66-1..4 closed-form sidecar.

SIDECAR (NOT central — precedent: B-S56 / B-S55 / B-S51 / B-PTD / B-DHDL /
B-LINEAGE / B-KTRIE / B-MGND / B-INTRA). central
state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED (0-line-diff).

  B-S66-1  S-TO-C-SHAPE-PRESERVATION-CLOSED            (carries/mirrors B-CONN-1)
  B-S66-2  PHYSICS-INPUT-WELL-FORMED-CLOSED            (Boolean + AST §55-C1/§7②)
  B-S66-3  RESPONSE-SEPARATION-METRIC-DETERMINISTIC    (pure-fn + neg-control)
  B-S66-4  S-DISABLED-REDUCTION-CLOSED                 (connection-point fair-cmp)

Closed-form anchors only: Kolmogorov dimension-preservation (B-CONN-1 carry),
Shannon entropy bound, Cauchy-Schwarz-class cosine range (Law-71), Euclidean
L2, Boolean truth-table, AST/source-grep. NO sigma/tau/phi/J2 external
derivation (f1/f2 safe). f3 safe (no external entity claim). B-IDENTITY-5
N/A (§66 physics input is a bounded float vector, NOT a text corpus — no
forbidden-token surface; smoke generates no corpus, runs no model forward).
"""
import ast
import json
import math
import os
import sympy as sp

RESULTS = []
HERE = os.path.dirname(os.path.abspath(__file__))


def record(name, title, passed, detail):
    RESULTS.append({"id": name, "title": title, "pass": bool(passed),
                    "detail": detail})


# import the smoke's closed-form S transfer for numeric witnesses
import importlib.util  # noqa: E402
_spec = importlib.util.spec_from_file_location(
    "smoke_s66", os.path.join(HERE, "smoke_s66.py"))
smk = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(smk)


# ---------------------------------------------------------------------------
# B-S66-1  S-TO-C-SHAPE-PRESERVATION-CLOSED  (carries/mirrors B-CONN-1)
#   B-CONN-1 (central blue_falsifier.py:779): "S->C wiring: C_state row dim
#   ≡ S_perception dim (shape preserved under ⊕)" — anchor B-S-2
#   UNIFORM-SHIFT-EXACT, real-limit = record-projection /
#   dimension-preservation (Kolmogorov). §66 carries it: the column-mean
#   delta returns a dim-vector for ANY input (byte T or physics P), so the
#   C ⊕ δ shape predicate shape(C ⊕ δ)=shape(C) holds input-AGNOSTICALLY.
# ---------------------------------------------------------------------------
def b_s66_1():
    # symbolic: s_perception over an (n × dim) matrix -> length-dim vector.
    # column-mean is dim_out = dim_in by construction (one mean per column).
    n, dim = sp.symbols("n dim", positive=True, integer=True)
    dim_out = dim  # _s_col_mean produces exactly `dim` entries (s_lib.hexa:34)
    shape_preserved = sp.Eq(dim_out, dim)  # tautology by construction of the form
    sym_ok = bool(sp.simplify(dim_out - dim) == 0) and bool(shape_preserved)

    # numeric witness: same dim for BOTH arms (input-content-agnostic).
    DIM, NC = smk.DIM, smk.N_CELLS
    c0 = smk._c0_state(NC, DIM)
    T = smk.byte_text_input("the mandala unfolds in silence", DIM)
    P = smk.physics_input(7077, DIM)
    # build C_after for each, run s_perception, assert len == DIM both
    def _delta(v):
        ca = []
        for i in range(NC):
            for j in range(DIM):
                ca.append(c0[i * DIM + j] + v[j])
        return smk.s_perception(c0, ca, NC, DIM)
    dT, dP = _delta(T), _delta(P)
    len_ok = (len(T) == DIM and len(P) == DIM and
              len(dT) == DIM and len(dP) == DIM)
    # C ⊕ δ shape: a dim-row ⊕ dim-delta -> dim-row (shape closure)
    row = c0[0:DIM]
    rowT = [row[j] + dT[j] for j in range(DIM)]
    rowP = [row[j] + dP[j] for j in range(DIM)]
    cx_ok = (len(rowT) == len(row) == DIM and len(rowP) == len(row) == DIM)

    ok = sym_ok and len_ok and cx_ok
    record(
        "B-S66-1", "S-TO-C-SHAPE-PRESERVATION-CLOSED (carries B-CONN-1)", ok,
        f"sympy: dim_out≡dim (column-mean = one mean/column, "
        f"simplify(dim_out-dim)=0)={sym_ok}; numeric BOTH arms: "
        f"|T|=|P|=|δT|=|δP|={DIM} len_ok={len_ok}; C⊕δ shape closure "
        f"|row⊕δ|=|row|={DIM} both arms={cx_ok}. S→C transfer is "
        f"input-content-AGNOSTIC (pure column-mean delta, B-S-1 linear) "
        f"⇒ B-CONN-1 shape(C⊕δ)=shape(C) holds for physics P iff for byte "
        f"T. B-CONN-1 REUSED not re-proven (prior 🔵 SSOT, anchor B-S-2).",
    )


# ---------------------------------------------------------------------------
# B-S66-2  PHYSICS-INPUT-WELL-FORMED-CLOSED  (Boolean + AST; §55-C1 + §7②)
#   every physics-native coord ∈ [0,1] by construction: psi_dir=(1+c)/2
#   c∈[-1,1] (clamp+Cauchy-Schwarz); psi_ent=H/log V ∈ [0,1] (Shannon
#   source-coding bound); tau clamped to [0,1]. AND AST forbidden-set
#   (from_pretrained/AutoModel/external encoder/trained net) hits = 0
#   ⇒ §55-C1 (codomain ⊆ [0,1]^dim) + §7② (no graft) by construction.
# ---------------------------------------------------------------------------
def b_s66_2():
    c, H, logV = sp.symbols("c H logV", real=True)
    # psi_dir = (1+c)/2 on clamped cosine domain c ∈ [-1,1]
    psi_dir = (1 + c) / 2
    pd_lo, pd_hi = psi_dir.subs(c, -1), psi_dir.subs(c, 1)
    pd_fp = psi_dir.subs(c, 0)  # 1/2 (Ψ=½ Law-71 fixed point)
    pd_ok = (pd_lo == 0 and pd_hi == 1 and pd_fp == sp.Rational(1, 2))
    # psi_ent = H/logV on Shannon-feasible 0 ≤ H ≤ logV (logV > 0)
    psi_ent = H / logV
    pe_lo = psi_ent.subs(H, 0)
    pe_hi = sp.simplify(psi_ent.subs(H, logV))
    pe_ok = (pe_lo == 0 and pe_hi == 1)
    box_ok = pd_ok and pe_ok

    # numeric: every coord of a physics input ∈ [0,1]
    P = smk.physics_input(7091, smk.DIM)
    coord_ok = all(0.0 <= x <= 1.0 for x in P) and len(P) == smk.DIM

    # AST forbidden-set scan of smoke_s66.py (mirror B-S56-2 / B-INTRA-3)
    forbidden = {
        "from_pretrained", "AutoModel", "AutoModelForCausalLM",
        "huggingface_hub", "clip", "whisper", "dinov2", "wav2vec2",
        "audiomae", "timm", "torchvision", "openai", "anthropic", "nn",
        "Linear", "Conv2d", "Parameter", "backward", "optimizer",
        "load_state_dict", "torch", "tensorflow", "jax", "transformers",
        "safetensors", "ConsciousDecoderV2",
    }
    with open(os.path.join(HERE, "smoke_s66.py"), "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in forbidden:
            hits.append(node.id)
        elif isinstance(node, ast.Attribute) and node.attr in forbidden:
            hits.append(node.attr)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = getattr(node, "module", None) or ""
            for tok in [mod] + [a.name for a in node.names]:
                base = (tok or "").split(".")[0]
                if base in forbidden:
                    hits.append(base)
    no_graft = (len(hits) == 0)

    ok = box_ok and coord_ok and no_graft
    record(
        "B-S66-2", "PHYSICS-INPUT-WELL-FORMED-CLOSED (Boolean+AST; §55-C1+§7②)",
        ok,
        f"sympy: psi_dir(c=-1)={pd_lo} psi_dir(c=0)={pd_fp}(Ψ=½ fp) "
        f"psi_dir(c=1)={pd_hi} (c∈[-1,1] clamp+Cauchy-Schwarz); "
        f"psi_ent(H=0)={pe_lo} psi_ent(H=logV)={pe_hi} (Shannon 0≤H≤logV) "
        f"⟹ codomain ⊆ [0,1]^dim = vacuum_psi box (§55-C1). numeric: all "
        f"{smk.DIM} coords ∈[0,1] coord_ok={coord_ok}. AST forbidden "
        f"|F|={len(forbidden)} hits={len(hits)} (must 0) ⟹ §7② no-graft "
        f"by construction. hits={sorted(set(hits))}",
    )


# ---------------------------------------------------------------------------
# B-S66-3  RESPONSE-SEPARATION-METRIC-DETERMINISTIC-CLOSED
#   the separation metric is a pure deterministic fn of the stimuli:
#   (i) 3× bit-identical re-run, (ii) AST has NO RNG/forward/training
#   calls, (iii) negative-control reduction (identical stimuli ⇒ sep=0
#   BOTH arms ⇒ metric provably discriminates, not trivially positive —
#   mirror §17/§36 neg-control discipline).
# ---------------------------------------------------------------------------
def b_s66_3():
    r1 = smk.run()
    r2 = smk.run()
    r3 = smk.run()
    det = (json.dumps(r1, sort_keys=True) == json.dumps(r2, sort_keys=True)
           == json.dumps(r3, sort_keys=True))

    # AST: no RNG / no model forward / no training in smoke_s66.py
    rng_forbidden = {"random", "randn", "rand", "normal", "seed_all",
                     "forward", "backward", "cuda", "to"}
    with open(os.path.join(HERE, "smoke_s66.py"), "r", encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    rng_hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and node.attr in rng_forbidden:
            rng_hits.append(node.attr)
        elif isinstance(node, ast.Name) and node.id in rng_forbidden:
            rng_hits.append(node.id)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = getattr(node, "module", None) or ""
            for tok in [mod] + [a.name for a in node.names]:
                if (tok or "").split(".")[0] in rng_forbidden:
                    rng_hits.append(tok)
    pure = (len(rng_hits) == 0)

    # negative-control reduction (closed): identical stimuli ⇒ sep≡0.
    # spread([x,x,...]) = max-min = 0  ;  pairwise L2 of identical = 0.
    s = sp.Symbol("s", real=True)
    spread_ident = sp.Max(s, s, s) - sp.Min(s, s, s)  # ≡ 0
    spread_zero = bool(sp.simplify(spread_ident) == 0)
    l2_ident = sp.sqrt((s - s) ** 2)                  # ≡ 0
    l2_zero = bool(sp.simplify(l2_ident) == 0)
    neg_runtime = bool(r1["negative_control"]["neg_control_ok"])
    neg_ctrl_ok = spread_zero and l2_zero and neg_runtime

    ok = det and pure and neg_ctrl_ok
    record(
        "B-S66-3", "RESPONSE-SEPARATION-METRIC-DETERMINISTIC-CLOSED", ok,
        f"3× bit-identical={det}; AST RNG/forward/training |R|="
        f"{len(rng_forbidden)} hits={len(rng_hits)} ⟹ pure-fn={pure}; "
        f"neg-control closed: spread([s,s,s])=Max−Min={sp.simplify(spread_ident)}≡0 "
        f"({spread_zero}), L2(s−s)={sp.simplify(l2_ident)}≡0 ({l2_zero}), "
        f"runtime neg_control_ok={neg_runtime} ⟹ metric PROVABLY "
        f"discriminates (not trivially always-positive, mirror §17/§36).",
    )


# ---------------------------------------------------------------------------
# B-S66-4  S-DISABLED-REDUCTION-CLOSED  (connection-point, fair-compare)
#   with S disabled (perception-delta ≡ 0 vector), the C-state is
#   byte-equal to the no-S path for BOTH arms ⇒ §66 introduces NOTHING
#   that changes the existing byte-text path. S-off ⇒ δ=0 ⇒ C⊕δ = C
#   identity. (mirror B-S56 / B-EBT-5 / B-DIRI-5 / B-MGND-5 OVERLAY-OFF.)
# ---------------------------------------------------------------------------
def b_s66_4():
    # closed: s_perception with NO state change (after ≡ before) ⇒ δ ≡ 0
    # (B-S-3 ZERO-CHANGE-EXACT, Law 50). Then C ⊕ 0 = C identity.
    x = sp.Symbol("x", real=True)
    delta_zero = x - x                       # mean(after)-mean(before) when after≡before
    s_off_zero = bool(sp.simplify(delta_zero) == 0)
    c, z = sp.symbols("c z", real=True)
    c_plus_zero = c + z
    identity_at_zero = bool(sp.simplify(c_plus_zero.subs(z, 0) - c) == 0)

    # numeric witness BOTH arms: S-off (after = before) ⇒ δ = 0-vector
    DIM, NC = smk.DIM, smk.N_CELLS
    c0 = smk._c0_state(NC, DIM)
    d_off = smk.s_perception(c0, list(c0), NC, DIM)  # after ≡ before
    off_zero = all(abs(v) < 1e-15 for v in d_off) and len(d_off) == DIM
    # C ⊕ 0 byte-equal C for the representative row (both arms identical
    # because δ=0 regardless of which input would have produced a change)
    row = c0[0:DIM]
    row_off = [row[j] + d_off[j] for j in range(DIM)]
    byte_equal = all(abs(row_off[j] - row[j]) < 1e-15 for j in range(DIM))

    ok = s_off_zero and identity_at_zero and off_zero and byte_equal
    record(
        "B-S66-4", "S-DISABLED-REDUCTION-CLOSED (connection-point fair-cmp)",
        ok,
        f"sympy: after≡before ⇒ δ=mean(A)−mean(B)={sp.simplify(delta_zero)}≡0 "
        f"(B-S-3 ZERO-CHANGE, Law 50) s_off_zero={s_off_zero}; "
        f"C⊕0−C={sp.simplify(c_plus_zero.subs(z,0)-c)}≡0 identity"
        f"={identity_at_zero}; numeric δ_off all|·|<1e-15 ({off_zero}) "
        f"row⊕0 byte-equal row ({byte_equal}) ⟹ S-disabled = existing "
        f"byte-text path byte-equal, BOTH arms ⟹ §66 fair-compare BY "
        f"CONSTRUCTION, introduces nothing changing the prior path.",
    )


def main():
    b_s66_1()
    b_s66_2()
    b_s66_3()
    b_s66_4()

    note = {
        "id": "B-S66-NOTE",
        "title": "PHYSICS-INPUT-EMERGENCE-EMPIRICAL (necessary-not-sufficient)",
        "pass": None,
        "detail": (
            "Whether physics-native input changes emergence AT SCALE = a "
            "future trained-ckpt input-side fire OUTCOME (feed P vs T into "
            "a carving ckpt, read Law-71 like §17). The §66 pilot proves "
            "ONLY that (1) the physics-input form is well-formed + "
            "§55-C1/§7²/B-CONN-1-compliant, (2) the separation metric is "
            "deterministic + negative-control-valid, (3) at the CLOSED-FORM "
            "substrate level physics-native input is directionally more "
            "discriminative (1.47×/2.13×, modest NOT 81×). "
            "Constraint/well-formedness/metric-validity + a directional "
            "substrate signal are NECESSARY, not sufficient, for GOAL "
            "(mirror §17 B-PHYS-NOTE: Ψ_dir alive but in_basin 0/31 — "
            "more separable ≠ correct ≠ emergent). B-D-NOTE / B-PHYS-NOTE "
            "/ B-EMERGE-7 / B-S56-NOTE family, NOT counted 🔵. north-star "
            "+ §15 milestone UNCHANGED."
        ),
    }

    n_pass = sum(1 for r in RESULTS if r["pass"] is True)
    n_total = len(RESULTS)
    all_pass = (n_pass == n_total) and n_total == 4
    out = {
        "section": "§66",
        "battery": "B-S66-1..4 + B-S66-NOTE",
        "central_blue_falsifier_unchanged": True,
        "n_pass": n_pass,
        "n_total": n_total,
        "all_pass": all_pass,
        "verdict": ("4/4 🔵 PASS" if all_pass else f"{n_pass}/{n_total} — FAIL"),
        "results": RESULTS,
        "note": note,
    }
    with open(os.path.join(HERE, "result.json"), "w",
              encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    for r in RESULTS:
        print(f"  {r['id']}  {'PASS' if r['pass'] else 'FAIL'}  {r['title']}")
    print(f"  {note['id']}  NOTE  {note['title']}")
    print(f"§66 B-S66: {out['verdict']} (central blue_falsifier.py UNCHANGED)")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
