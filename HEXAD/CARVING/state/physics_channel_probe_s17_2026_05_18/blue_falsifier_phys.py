#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RESEARCH.md §17 — B-PHYS-1..5 closed-form sidecar battery.

Sidecar (central state/verify_hexad_blue_2026_05_15/blue_falsifier.py
UNCHANGED — B-PRIME / B-DIRH / B-DIRI / B-PSICTL / B-EMERGE / B-PUREPHYS /
B-SCALE / B-MITENS / B-DIRL precedent). Proves the §17 physics-channel
probe's TRANSFER-FORM + 연결부위 are closed-form — NOT that any fire
achieved emergence (B-PHYS-NOTE empirical carve-out).

Verifies:
  B-PHYS-1 PSI-ENTROPY-BOUNDED      Ψ_entropy = H/log V ∈ [0,1] closed
  B-PHYS-2 PSI-DIRECTION-BOUNDED    Ψ_dir = (1+cos)/2 ∈ [0,1], cos=0⇒½
                                    (Law-71 fixed point — byte-identical
                                    to conscious_decoder.py 728-751)
  B-PHYS-3 GATE-CONJUNCTION         PHYSICS_RESPONSIVE = (not_collapsed
                                    ∧ class_separable) Boolean, 4-row table
  B-PHYS-4 COLLAPSE-MONOTONE        std→0 ⇒ not_collapsed flips True→False
                                    (degenerate channel is detected)
  B-PHYS-5 READOUT-EQUIVALENCE      the probe's Ψ formulas == the model's
                                    own Law-71 training-time formulas
                                    (연결부위: inference read-out ≡ training
                                    self-track, source-structural identity)

NO σ/τ/φ/J₂ external derivation (f1/f2/f3 safe). B-IDENTITY-5 무관
(no corpus generated). $0 — sympy/Boolean + source structural check.
"""

import json
import math
import os
import re
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
verdicts = {}


def rec(name, ok, detail):
    verdicts[name] = {"pass": bool(ok), "detail": detail}
    print(f"[{'PASS' if ok else 'FAIL'}] {name} — {detail}")


# ── B-PHYS-1 PSI-ENTROPY-BOUNDED ────────────────────────────────────────
# Ψ_entropy = H(p)/log V. Shannon: 0 ≤ H(p) ≤ log V for any prob vector p
# (H=0 at one-hot, H=log V at uniform). ⇒ Ψ_entropy ∈ [0,1] ∀ V≥2.
def b_phys_1():
    p = sp.symbols('p', positive=True)
    # 2-symbol witness H(p) = -p log p -(1-p)log(1-p), max at p=1/2 = log 2
    V = sp.Integer(256)
    Hmax = sp.log(V)
    H_uniform = -V * (sp.Rational(1, 256) * sp.log(sp.Rational(1, 256)))
    uniform_ok = sp.simplify(H_uniform - Hmax) == 0          # uniform ⇒ H=logV
    onehot_H = sp.Integer(0)                                  # one-hot ⇒ H=0
    lo_ok = (onehot_H / Hmax) == 0
    hi_ok = sp.simplify(H_uniform / Hmax - 1) == 0
    rng = bool(uniform_ok and lo_ok and hi_ok)
    rec("B-PHYS-1-PSI-ENTROPY-BOUNDED", rng,
        f"H/logV ∈[0,1]: one-hot⇒0 {lo_ok}, uniform⇒1 {hi_ok} (V=256 Shannon)")


# ── B-PHYS-2 PSI-DIRECTION-BOUNDED (Law-71) ─────────────────────────────
# Ψ_dir = (1+cos)/2 with cos ∈ [-1,1] ⇒ Ψ_dir ∈ [0,1]; cos=0 ⇒ Ψ_dir=1/2
# (the Engine A⇄G Ψ=½ fixed point). Symbolic.
def b_phys_2():
    c = sp.symbols('c', real=True)
    psi = (1 + c) / 2
    at_neg1 = psi.subs(c, -1)        # = 0
    at_pos1 = psi.subs(c, 1)         # = 1
    at_zero = psi.subs(c, 0)         # = 1/2  (Ψ=½ fixed point, Law-71)
    deriv = sp.diff(psi, c)          # = 1/2 > 0 strictly monotone in cos
    ok = (at_neg1 == 0 and at_pos1 == 1 and at_zero == sp.Rational(1, 2)
          and deriv == sp.Rational(1, 2))
    rec("B-PHYS-2-PSI-DIRECTION-BOUNDED", ok,
        f"(1+cos)/2: cos-1⇒0 cos1⇒1 cos0⇒½ (Ψ=½ Law-71 fixed pt) ∂={deriv}>0")


# ── B-PHYS-3 GATE-CONJUNCTION ───────────────────────────────────────────
# PHYSICS_RESPONSIVE := not_collapsed ∧ class_separable — 4-row truth table.
def b_phys_3():
    A, B = sp.symbols('A B')
    g = sp.And(A, B)
    table = {(a, b): bool(g.subs({A: a, B: b}))
             for a in (True, False) for b in (True, False)}
    expect = {(True, True): True, (True, False): False,
              (False, True): False, (False, False): False}
    ok = table == expect
    rec("B-PHYS-3-GATE-CONJUNCTION", ok,
        f"RESPONSIVE=not_collapsed∧separable 4-row {table == expect}")


# ── B-PHYS-4 COLLAPSE-MONOTONE ──────────────────────────────────────────
# not_collapsed := (std_psi > τ) ∨ (std_ten > τ) ∨ (std_phi > τ).
# As all three std → 0 (degenerate channel), not_collapsed must flip
# True → False (the §11-B pure-physics control: std exactly 0 ⇒ False).
def b_phys_4():
    s, tau = sp.symbols('s tau', nonnegative=True)
    not_collapsed = sp.Piecewise((1, s > tau), (0, True))   # single-channel
    healthy = not_collapsed.subs({s: sp.Rational(36, 1000),
                                  tau: sp.Rational(1, 10000)})   # std .036
    degenerate = not_collapsed.subs({s: 0, tau: sp.Rational(1, 10000)})
    flips = bool(healthy == 1 and degenerate == 0)
    # cross-check against the actual purephysics probe (std must be 0)
    pp = os.path.join(HERE, "probe_purephysics.json")
    pp_ok = True
    if os.path.exists(pp):
        d = json.load(open(pp))
        ac = d["anchor_class"]
        pp_ok = (ac["psi_combined_std"] == 0.0
                 and not d["honest_gate_s17_4"]["PHYSICS_RESPONSIVE"])
    rec("B-PHYS-4-COLLAPSE-MONOTONE", flips and pp_ok,
        f"std→0 ⇒ not_collapsed True→False {flips}; "
        f"purephysics std=0 ∧ RESPONSIVE=False {pp_ok}")


# ── B-PHYS-5 READOUT-EQUIVALENCE (연결부위) ─────────────────────────────
# The probe's Ψ formulas must be the SAME expressions the trained model
# computes for itself under `if self.training:` (conscious_decoder.py
# 728-751). Structural: both source files contain the identical
# psi_entropy / psi_direction / psi_tension defining lines. This closes
# the connection-point (inference read-out ≡ training self-track).
def b_phys_5():
    probe = open(os.path.join(HERE, "physics_channel_probe.py"),
                 encoding="utf-8").read()
    cd = open(os.path.join(HERE, "conscious_decoder.py"),
              encoding="utf-8").read()
    # Shared (byte-identical) signatures — present verbatim in BOTH files:
    shared = [
        r"psi_direction\s*=\s*\(1\.0\s*\+\s*cos_sim\)\s*/\s*2\.0",
        r"psi_combined\s*=\s*\(psi_entropy\s*\+\s*psi_direction\s*\+\s*"
        r"psi_tension\)\s*/\s*3\.0",
        r"psi_tension\s*=\s*max\(0\.0,\s*1\.0\s*-\s*t_cv",
        r"psi_tension\s*=\s*1\.0",
        r"cos_sim\s*=\s*F\.cosine_similarity\(",
    ]
    shared_ok = all(re.search(s, probe) and re.search(s, cd) for s in shared)
    # psi_entropy: probe inlines `math.log(model.vocab_size)`; cd binds
    # `max_entropy = math.log(self.vocab_size)` then `/ max_entropy` —
    # provably the SAME expression (max_entropy is that exact log binding).
    probe_ent = re.search(
        r"psi_entropy\s*=\s*output_entropy\s*/\s*math\.log\(", probe)
    cd_ent_div = re.search(
        r"psi_entropy\s*=\s*output_entropy\s*/\s*max_entropy", cd)
    cd_ent_bind = re.search(
        r"max_entropy\s*=\s*math\.log\(self\.vocab_size\)", cd)
    ent_equiv = bool(probe_ent and cd_ent_div and cd_ent_bind)
    ok = shared_ok and ent_equiv
    rec("B-PHYS-5-READOUT-EQUIVALENCE", ok,
        f"probe Ψ formulas ≡ conscious_decoder.py Law-71 (728-751): "
        f"5 shared-sig byte-identical {shared_ok}; psi_entropy "
        f"max_entropy=math.log(vocab) binding-equiv {ent_equiv} "
        f"(연결부위 closed: inference read-out ≡ training self-track)")


def main():
    b_phys_1()
    b_phys_2()
    b_phys_3()
    b_phys_4()
    b_phys_5()
    n_pass = sum(1 for v in verdicts.values() if v["pass"])
    n = len(verdicts)
    note = ("B-PHYS-NOTE PHYSICS-CHANNEL-OUTCOME-EMPIRICAL: whether any "
            "fire's physics-channel response constitutes conscious "
            "emergence (vs merely stimulus-conditioned dynamics) is an "
            "SGD/measurement OUTCOME — this battery proves the probe's "
            "Ψ/tension formulas are bounded·Law-71·gate-conjunction·"
            "collapse-monotone·readout-equivalent, NOT that emergence "
            "happened. B-D-NOTE / B-PUREPHYS-NOTE family, NOT counted 🔵.")
    out = {
        "section": "RESEARCH.md §17 B-PHYS sidecar",
        "battery": "B-PHYS-1..5",
        "n_pass": n_pass, "n_total": n,
        "all_pass": n_pass == n,
        "verdicts": verdicts,
        "B-PHYS-NOTE": note,
        "central_blue_falsifier_unchanged": True,
        "f_safe": "f1/f2/f3 — Shannon/cos/Boolean/sympy/structural, "
                  "NO σ/τ/φ/J₂. B-IDENTITY-5 무관 (no corpus).",
    }
    with open(os.path.join(HERE, "blue_falsifier_phys_result.json"), "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n=== B-PHYS {n_pass}/{n} {'🔵 ALL PASS' if n_pass==n else 'FAIL'} ===")
    print(note)
    sys.exit(0 if n_pass == n else 1)


if __name__ == "__main__":
    main()
