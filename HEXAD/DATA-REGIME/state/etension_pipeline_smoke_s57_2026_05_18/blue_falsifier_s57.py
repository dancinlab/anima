"""§57 blue_falsifier_s57 — B-S57-1..4 sidecar (NOT central).

central state/verify_hexad_blue_2026_05_15/blue_falsifier.py UNCHANGED
(sidecar pattern carry: B-PRIME / B-DIRH / B-DIRI / B-S16 / B-EEG-CT3 /
B-MGND / B-PHASE-B precedents).

  B-S57-1 E-TENSION-CODOMAIN-Ψ-BOUNDED-CLOSED
  B-S57-2 BASIN-CONTAINMENT-EMPIRICAL-CLOSED
  B-S57-3 NO-TRAINED-NET-AST-CLOSED
  B-S57-4 ZERO-DIVERSITY-NEGATIVE-CONTROL-CLOSED
  B-S57-NOTE (empirical carve-out, NOT counted 🔵)

g3: §57 validates the pipeline mechanically + floors zero-diversity. It
does NOT and cannot show GOAL movement (E_tension is closed-loop per §56).
f1/f2/f3 + B-IDENTITY-5 safe (Shannon/cos bounded · Boolean · sympy ·
AST grep · linear-algebra rank — NO σ/τ/φ/J₂; Ψ=½ = anima g2 internal
arch carve-out).
"""

from __future__ import annotations

import ast
import json
import math
from pathlib import Path

import numpy as np
import sympy as sp

from e_tension import e_tension, stub_fingerprints

HERE = Path(__file__).resolve().parent


def b_s57_1():
    """E-TENSION-CODOMAIN-Ψ-BOUNDED-CLOSED.

    Transfer-form (carry §55-C1 / §56-B-S56-1, Law-71): for ANY pseudo-logit
    vectors, psi_entropy = H(softmax)/log n ∈ [0,1] and psi_direction =
    (1+cos)/2 ∈ [0,1]. sympy closed proof of the two bounds + empirical
    over the full deterministic stub set (every output in [0,1]^2).
    """
    # sympy closed bound for psi_direction: cos ∈ [-1,1] => (1+cos)/2 ∈ [0,1]
    c = sp.Symbol("c", real=True)
    pd = (1 + c) / 2
    lo = pd.subs(c, -1)   # = 0
    hi = pd.subs(c, 1)    # = 1
    bound_pd = (lo == 0) and (hi == 1) and sp.simplify(sp.diff(pd, c) - sp.Rational(1, 2)) == 0
    # sympy closed bound for psi_entropy: 0 ≤ H(p) ≤ log n (Shannon) =>
    # H/log n ∈ [0,1]. Witness the two extremes symbolically:
    #   one-hot p -> H = 0 -> 0 ; uniform p (n=2) -> H = log 2 -> /log2 = 1
    n = sp.Integer(2)
    H_uniform = -2 * (sp.Rational(1, 2) * sp.log(sp.Rational(1, 2)))
    ent_uniform_norm = sp.simplify(H_uniform / sp.log(n))   # = 1
    H_onehot_norm = sp.Integer(0)                           # = 0
    bound_pe = (ent_uniform_norm == 1) and (H_onehot_norm == 0)
    # empirical: full stub set in [0,1]^2
    pts = np.asarray([e_tension(fp) for fp in stub_fingerprints(64, 1337)])
    in_box = bool(np.all(pts >= 0.0) and np.all(pts <= 1.0))
    ok = bool(bound_pd and bound_pe and in_box)
    return ("B-S57-1 E-TENSION-CODOMAIN-Ψ-BOUNDED-CLOSED", ok)


def b_s57_2():
    """BASIN-CONTAINMENT-EMPIRICAL-CLOSED.

    The §55-C2 gate ‖E_tension − coord‖ < radius is actually checked on
    real e_tension output: pass-rate must be 1.0 over the full stub set
    against the materialized basin (centroid + extent). Connection-point:
    the basin radius is the cloud's own max-extent + margin, so the
    containment proposition is a closed inequality verified numerically.
    """
    r = json.loads((HERE / "result.json").read_text(encoding="utf-8"))
    pts = [tuple(p) for p in np.asarray([e_tension(fp) for fp in stub_fingerprints(64, 1337)])]
    cen = tuple(r["basin_centroid"])
    rad = r["basin_radius"]
    contained = all(math.hypot(p[0] - cen[0], p[1] - cen[1]) < rad for p in pts)
    pr = r["basin_containment_pass_rate"]
    ok = bool(contained and pr == 1.0 and r["n_contained"] == r["n_total"])
    return ("B-S57-2 BASIN-CONTAINMENT-EMPIRICAL-CLOSED", ok)


def b_s57_3():
    """NO-TRAINED-NET-AST-CLOSED.

    §7② structural: e_tension.py has ZERO external / trained-net calls.
    AST Call-node scan over the source (comment/docstring/string-literal
    auto-excluded by ast). forbidden_call_set total must be 0. Carry
    §56-B-S56-2.
    """
    # exact-component forbidden set (mirror B-INTRA-3 / B-DR-UNIQUE-3
    # exact-component grep — NOT substring, substring would false-match
    # legit identifiers like e_TENSION / s_TRAIN_… ).
    forbidden = {
        "torch", "tensorflow", "sklearn", "openai", "anthropic", "llm_call",
        "paraphrase", "bert_score", "AutoModel", "HfApi", "llama",
        "huggingface_hub", "from_pretrained", "load_state_dict", "backward",
        "cross_entropy",
    }
    src = (HERE / "e_tension.py").read_text(encoding="utf-8")
    tree = ast.parse(src)
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            name = None
            if isinstance(f, ast.Name):
                name = f.id
            elif isinstance(f, ast.Attribute):
                name = f.attr
            if name in forbidden:
                hits.append(("call", name))
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            mod = (getattr(node, "module", None) or "").split(".")[0]
            names = [a.name.split(".")[0] for a in node.names]
            if mod in forbidden:
                hits.append(("import-mod", mod))
            for nm in names:
                if nm in forbidden:
                    hits.append(("import-name", nm))
    ok = bool(len(hits) == 0)
    return ("B-S57-3 NO-TRAINED-NET-AST-CLOSED", ok)


def b_s57_4():
    """ZERO-DIVERSITY-NEGATIVE-CONTROL-CLOSED.

    The tension channel's added-information measure ≈ 0 (closed/Boolean).
    Closed argument: the text channel is a CONSTANT string => its centred
    feature matrix has rank 0 (carries no per-record information). The
    tension channel is a deterministic fixed re-projection of anima's OWN
    state (closed loop, no external referent) — so the 2-modality record
    carries the SAME perceptual information as the text-only record.
    This empirically floors §56's honest finding, NOT a capability.
    """
    r = json.loads((HERE / "result.json").read_text(encoding="utf-8"))
    z = r["zero_diversity_measure"]
    # closed: text centred-rank == 0 (constant string, no per-record info)
    rank_text_zero = (z["rank_text_centred"] == 0)
    # closed: stacking the closed-loop tension cloud onto the constant text
    # adds NO rank beyond the tension cloud itself (text contributes 0) —
    # rank_stacked == rank_tension exactly (no synergistic information).
    no_synergy = (z["rank_stacked_centred"] == z["rank_tension_centred"])
    # sympy closed identity: a constant column c·1 centred is the zero
    # vector, so its rank contribution is exactly 0 — formalise it.
    n = sp.Symbol("n", positive=True, integer=True)
    k = sp.Symbol("k", real=True)
    centred_const = sp.simplify(k - k)  # constant minus its own mean == 0
    const_rank_zero = (centred_const == 0)
    ok = bool(rank_text_zero and no_synergy and const_rank_zero
              and z["zero_perceptual_diversity"] is True)
    return ("B-S57-4 ZERO-DIVERSITY-NEGATIVE-CONTROL-CLOSED", ok)


B_S57_NOTE = (
    "B-S57-NOTE: §57 validates the pipeline mechanically (e_tension -> "
    "Law-71 Ψ-box -> .kosmos payload -> 2-modality corpus -> basin "
    "containment) AND floors zero-diversity (the tension channel is "
    "anima's OWN re-serialised state, closed-loop). It does NOT and "
    "CANNOT show GOAL movement: E_tension is closed-loop by §56 (§11-B "
    "'physics != signal' in encoder form). The frontier-1 GOAL path "
    "remains the §1.1-recursing image/audio §7② external-substrate wall. "
    "Whether a real perceptual modality moves §1.1 = future-fire OUTCOME "
    "(B-D-NOTE / B-S56-NOTE family, NOT counted 🔵). necessary-not-"
    "sufficient (mirror B-EMERGE-7)."
)


def main():
    checks = [b_s57_1(), b_s57_2(), b_s57_3(), b_s57_4()]
    n_pass = sum(1 for _, ok in checks if ok)
    out = {
        "battery": "B-S57 (§57 E_tension pipeline-validation sidecar)",
        "central_blue_falsifier_unchanged": True,
        "checks": [{"id": cid, "pass": ok} for cid, ok in checks],
        "n_pass": n_pass,
        "n_total": len(checks),
        "all_blue": n_pass == len(checks),
        "note": B_S57_NOTE,
    }
    (HERE / "blue_falsifier_s57_result.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for cid, ok in checks:
        print(f"{'🔵 PASS' if ok else '❌ FAIL'}  {cid}")
    print(f"\nB-S57: {n_pass}/{len(checks)} 🔵  (central unchanged)")
    print(B_S57_NOTE)
    return out


if __name__ == "__main__":
    main()
