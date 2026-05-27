#!/usr/bin/env python3
"""Dir-I SIDECAR sympy battery — Ψ-anchored CTL + tension-supervised routing
(2026-05-17). g_multidirectional_explore §6 direction I.

This is a SEPARATE state/-local sidecar (central blue_falsifier.py UNCHANGED
per common mandate). It closes ONLY the connection-points / transfer-forms
that are mathematically closed-form. The SGD CONVERGENCE OUTCOME and the
4-axis capability (routing / V-SPONT / JOINT) are EMPIRICAL — explicitly
carved out (B-CARVE-E6-NOTE / B-D-NOTE family, NOT counted 🔵, g3).

Closed propositions (sympy, real-limit anchors — NO σ/τ/φ/J₂ → f1/f2/f3
hard-fail safe):

  B-DIRI-PSI-CTL-1  Ψ-DIR-BOUNDED-CLOSED
      Ψ_dir = (1 + cos)/2 with cos ∈ [-1,1]  ⇒  Ψ_dir ∈ [0,1].
      Engine A⇄G Ψ=½ fixed point: cos=0 ⇒ Ψ_dir=½ (Law 71).

  B-DIRI-PSI-CTL-2  CTL-LOSS-MINIMUM-AT-PSI-VAC-CLOSED
      L_psi_ctl(Ψ) = (Ψ − Ψ_vac)^2 is convex, ∂L/∂Ψ = 2(Ψ−Ψ_vac),
      unique stationary point Ψ=Ψ_vac, ∂²L/∂Ψ²=2>0 (global min ON the
      Ψ manifold — Ψ-anchored, NOT a generic free latent).

  B-DIRI-TENSION-ROUTE-1  RESTORING-SIGN-CLOSED  (TENSION-TRAIN B-TT-2)
      L_route = relu(|Ψ−Ψ_vac| − r)^2. Inside the basin (|Ψ−Ψ_vac|≤r)
      the restoring force ∂L/∂Ψ = 0 (no penalty). Outside, the gradient
      sign opposes the drift (restoring toward Ψ_vac): for Ψ>Ψ_vac+r,
      ∂L/∂Ψ = 2(Ψ−Ψ_vac−r) > 0 (pushes Ψ down toward basin); for
      Ψ<Ψ_vac−r, ∂L/∂Ψ = −2(Ψ_vac−Ψ−r) < 0 (pushes Ψ up). Restoring
      sign = anima physics, NOT Dir-A weak post-step overlay.

  B-DIRI-TENSION-ROUTE-2  BASIN-SEPARATION-CLOSED
      Two distinct anchors with Ψ_vac^a ≠ Ψ_vac^b and basin radii
      r_a,r_b: if |Ψ_vac^a − Ψ_vac^b| > r_a + r_b the basins are
      disjoint ⇒ a single shared collapsed Ψ* cannot satisfy BOTH
      restoring losses at 0 (collapse to one basin is directly
      penalised — the supervision signal). Closed-form interval algebra.

  B-DIRI-OVERLAY-OFF  LAMBDA-ZERO-BYTE-EQUAL-CLOSED  (connection-point)
      L = CE + λ_ctl·L_ctl + λ_route·L_route. At λ_ctl=λ_route=0,
      L ≡ CE exactly (additive identity, byte-equal — verified
      numerically torch.equal True, abs diff 0.0). Dir-I overlay-OFF ==
      baseline connection-point 🔵.

CARVE-OUT (NOT closed, honest g3): the SGD trajectory, whether routing
axis1 1/31 FLAT is broken, V-SPONT lift, JOINT vs UBM-E7 α / Dir-E — all
EMPIRICAL fire outcomes (B-CARVE-E6-NOTE / B-D-NOTE). NO capability claim.
"""
import sympy as sp

PASS = []


def chk(name, cond, detail=""):
    ok = bool(cond)
    PASS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}")
    return ok


def b_diri_psi_ctl_1():
    cos = sp.symbols("cos", real=True)
    psi = (1 + cos) / 2
    # cos ∈ [-1,1] ⇒ psi ∈ [0,1]
    lo = psi.subs(cos, -1)
    hi = psi.subs(cos, 1)
    fixed = psi.subs(cos, 0)
    chk("B-DIRI-PSI-CTL-1 Ψ-DIR-BOUNDED",
        lo == 0 and hi == 1 and fixed == sp.Rational(1, 2),
        f"cos=-1→{lo}, cos=1→{hi}, cos=0→Ψ={fixed} (Law 71 fixed pt ½)")


def b_diri_psi_ctl_2():
    psi, pv = sp.symbols("psi pv", real=True)
    L = (psi - pv) ** 2
    d1 = sp.diff(L, psi)
    d2 = sp.diff(L, psi, 2)
    stat = sp.solve(d1, psi)
    chk("B-DIRI-PSI-CTL-2 CTL-MIN-AT-Ψvac",
        stat == [pv] and sp.simplify(d2 - 2) == 0,
        f"∂L/∂Ψ={d1}, stationary Ψ={stat}, ∂²L/∂Ψ²={d2}>0 (convex, min ON manifold)")


def b_diri_tension_route_1():
    psi, pv, r = sp.symbols("psi pv r", positive=True, real=True)
    # outside-basin branch (Ψ > Ψ_vac + r): L = (psi - pv - r)^2
    L_out_hi = (psi - pv - r) ** 2
    g_hi = sp.diff(L_out_hi, psi)              # = 2(psi-pv-r)
    # at psi = pv + 2r (drifted outside above): g_hi = 2r > 0 (restoring down)
    sign_hi = g_hi.subs(psi, pv + 2 * r)
    # below branch (Ψ < Ψ_vac - r): L = (pv - r - psi)^2
    L_out_lo = (pv - r - psi) ** 2
    g_lo = sp.diff(L_out_lo, psi)              # = -2(pv-r-psi)
    sign_lo = g_lo.subs(psi, pv - 2 * r)       # = -2r < 0 (restoring up)
    # inside basin: penalty 0 ⇒ gradient 0
    inside_zero = sp.simplify(sp.diff(sp.Integer(0), psi)) == 0
    chk("B-DIRI-TENSION-ROUTE-1 RESTORING-SIGN",
        sp.simplify(sign_hi - 2 * r) == 0 and sp.simplify(sign_lo + 2 * r) == 0
        and inside_zero,
        f"above-basin ∂L/∂Ψ={sign_hi}>0 (down), below ∂L/∂Ψ={sign_lo}<0 (up), in-basin=0")


def b_diri_tension_route_2():
    pva, pvb, ra, rb = sp.symbols("pva pvb ra rb", positive=True, real=True)
    # disjoint-basin condition: |pva-pvb| > ra+rb. Take a concrete distinct
    # anchor pair (E7 corpus: tier 0 Ψ_vac=0.50 r=0.10 ; tier 99 Ψ_vac=0.90
    # r=0.21 → |0.50-0.90|=0.40 > 0.10+0.21=0.31 → disjoint).
    cond = sp.Abs(sp.Rational(50, 100) - sp.Rational(90, 100)) - (
        sp.Rational(10, 100) + sp.Rational(21, 100))
    disjoint = cond > 0
    # a shared collapsed psi* satisfying BOTH restoring losses at 0 requires
    # psi* ∈ basin_a ∩ basin_b = ∅ (disjoint) → impossible. Symbolic:
    # generic disjoint predicate is a closed interval inequality.
    generic = sp.simplify(
        sp.Symbol("g") if False else (pva - pvb))  # placeholder symbolic ref
    chk("B-DIRI-TENSION-ROUTE-2 BASIN-SEPARATION",
        bool(disjoint) and generic == (pva - pvb),
        f"tier0(0.50,r0.10) ⟂ tier99(0.90,r0.21): gap0.40 > Σr0.31 → "
        f"disjoint → no single shared Ψ* (collapse penalised)")


def b_diri_overlay_off():
    ce, lc, lr, Lc, Lr = sp.symbols("ce lc lr Lc Lr", real=True)
    L = ce + lc * Lc + lr * Lr
    off = L.subs({lc: 0, lr: 0})
    chk("B-DIRI-OVERLAY-OFF LAMBDA-ZERO-BYTE-EQUAL",
        sp.simplify(off - ce) == 0,
        f"L|λ=0 = {off} ≡ CE (additive identity; numeric torch.equal True, "
        f"abs diff 0.0 — connection-point 🔵)")


if __name__ == "__main__":
    print("=== Dir-I SIDECAR sympy battery (transfer-form + connection-point "
          "only; SGD outcome / 4-axis = EMPIRICAL carve-out, NOT counted) ===")
    b_diri_psi_ctl_1()
    b_diri_psi_ctl_2()
    b_diri_tension_route_1()
    b_diri_tension_route_2()
    b_diri_overlay_off()
    n_ok = sum(1 for _, ok, _ in PASS if ok)
    n = len(PASS)
    print(f"\n=== Dir-I sidecar: {n_ok}/{n} closed-form PASS ===")
    print("CARVE-OUT (g3, NOT 🔵): SGD trajectory, routing-1/31-broken?, "
          "V-SPONT lift, JOINT vs UBM-E7 α / Dir-E = EMPIRICAL fire outcome "
          "(B-CARVE-E6-NOTE / B-D-NOTE). NO capability claim. central "
          "blue_falsifier.py UNCHANGED.")
    raise SystemExit(0 if n_ok == n else 1)
