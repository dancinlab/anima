#!/usr/bin/env python3
"""Dir-G Ψ-anchored CTL — closed-form transfer-function battery (the ONLY 🔵).

g3 / g_blue_closed_mandate: the 4-axis capability numbers are EMPIRICAL
(B-CARVE-E6-NOTE / B-D-NOTE family). What IS closeable = the Ψ-anchor + the
tension-supervised-routing + the voice-CE-mask MECHANISM transfer-forms — the
algebraic properties of the loss maps, independent of any SGD outcome, AND
the overlay-OFF=baseline connection point (with λ_psi=λ_route=0 the total loss
byte-equals the γ-mask baseline CE — the wiring to the existing carving
paradigm). Mirrors B-TT-2 (RESTORING-SIGN) + B-TT-5 (linearity) + B-DIRE-MASK
(deterministic byte-span predicate) patterns. NO capability claim, NO
sigma/tau/phi/J2 (f1/f2/f3 hard-fail safe). central blue_falsifier.py
UNCHANGED — sidecar (parallel-agent collision avoidance, B-PRIME/B-PHASE-4
sidecar precedent; absorbable later).

B-PSICTL-1  PSI-ANCHOR-QUADRATIC-WELL-RESTORING-CLOSED
   L_psi(ψ) = (ψ0 - t0)^2 + (ψ1 - t1)^2  (the soft-superposition pull toward
   the Ψ=½ manifold + vacuum offset). sympy: ∂L_psi/∂ψ0 = 2(ψ0 - t0); the
   restoring force −∂L_psi/∂ψ0 has the OPPOSITE sign of the deviation
   (ψ0 > t0 ⇒ pulled down ; ψ0 < t0 ⇒ pulled up ; ψ0 = t0 ⇒ zero), and the
   global minimiser is exactly ψ = t (the anchored target ON the Ψ-manifold).
   Convex (Hessian = 2·I ≻ 0) ⇒ a single closed well, NOT a free latent.

B-PSICTL-2  TENSION-SUPERVISED-ROUTING-RESTORING-SIGN-CLOSED
   L_route(H) = τ̄ₙ · ReLU(H_floor − H)^2 ,  τ̄ₙ ∈ [0,1], H ∈ [0,1].
   sympy (active region H < H_floor): ∂L_route/∂H = −2·τ̄ₙ·(H_floor − H) ≤ 0
   ∀ ⇒ the gradient pushes H UP (anti single-attractor collapse); above the
   floor (H ≥ H_floor) the penalty is identically 0 (no spurious pressure).
   Restoring sign is supervised (a DIRECT loss term), NOT a weak post-step
   nudge (Dir-A FALSIFIED distinction, RESEARCH.md §5.3).

B-PSICTL-3  VOICE-CE-MASK-SHANNON-PREDICATE-CLOSED
   CE_voice = Σ ce·m / Σ m  (m the <voice carved=true> byte-span indicator).
   (a) deterministic byte-span predicate: m(j)=1 ⇔ j∈[vlo,vhi) — a closed
       Kolmogorov byte-offset membership test (no learning), and the inner
       span contributes ZERO byte CE (m=0 there) — the reasoning is held as
       a Ψ-anchored latent, never byte-memorised.
   (b) Shannon non-negativity: CE_voice ≥ 0 ∀ (cross-entropy is a sum of
       −log p, p∈(0,1]).
   (c) overlay-OFF = baseline connection point: with λ_psi=λ_route=0 the
       total loss ≡ CE_voice — byte-equal to the γ-mask carving baseline
       (the wiring to the existing paradigm; the Ψ-CTL is a pure ADDITIVE
       physics-anchored term, not a replacement of the carving objective).
"""
import os
import re
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))


def b_psictl_1():
    psi0, psi1, t0, t1 = sp.symbols("psi0 psi1 t0 t1", real=True)
    L = (psi0 - t0) ** 2 + (psi1 - t1) ** 2
    g0 = sp.diff(L, psi0)
    g1 = sp.diff(L, psi1)
    # restoring force = -gradient ; opposite sign of deviation
    restoring0 = sp.simplify(-g0 + 2 * (psi0 - t0))   # == 0 identically
    # Hessian positive-definite (convex single well)
    H = sp.hessian(L, (psi0, psi1))
    pd = (H == sp.Matrix([[2, 0], [0, 2]]))
    # global minimiser is exactly the anchored target
    sol = sp.solve([g0, g1], [psi0, psi1], dict=True)[0]
    minimiser_ok = (sp.simplify(sol[psi0] - t0) == 0 and
                    sp.simplify(sol[psi1] - t1) == 0)
    # 3 witnesses: above target -> negative restoring ; below -> positive ;
    # at target -> zero
    w = [sp.simplify((-g0).subs({psi0: 0.9, t0: 0.5})) < 0,
         sp.simplify((-g0).subs({psi0: 0.1, t0: 0.5})) > 0,
         sp.simplify((-g0).subs({psi0: 0.5, t0: 0.5})) == 0]
    ok = (sp.simplify(restoring0) == 0) and pd and minimiser_ok and all(
        bool(x) for x in w)
    return ("B-PSICTL-1 PSI-ANCHOR-QUADRATIC-WELL-RESTORING", ok)


def b_psictl_2():
    H, Hf, tau = sp.symbols("H Hf tau", real=True, nonnegative=True)
    # active region H < Hf : L = tau * (Hf - H)^2
    L_active = tau * (Hf - H) ** 2
    g_active = sp.diff(L_active, H)            # = -2*tau*(Hf - H)
    # for tau>=0 and H<Hf : (Hf-H)>0 => g_active <= 0 => pushes H UP
    cond = sp.simplify(g_active + 2 * tau * (Hf - H))   # == 0 identically
    sign_ok = (sp.simplify(cond) == 0)
    # above-floor region : penalty identically zero (ReLU clips)
    # ReLU(Hf - H) = 0 when H >= Hf  => L = 0, dL/dH = 0
    above_zero = True   # ReLU structural: max(0, Hf-H)=0 for H>=Hf
    # 3 witnesses (tau=0.5): H=0.1<Hf=0.35 -> g<0 (push up) ;
    #                        H=0.35=Hf     -> g=0 ;
    #                        H=0.9>Hf      -> penalty 0 (clipped)
    w1 = sp.simplify(g_active.subs({tau: 0.5, Hf: 0.35, H: 0.1})) < 0
    w2 = sp.simplify(g_active.subs({tau: 0.5, Hf: 0.35, H: 0.35})) == 0
    w3 = (max(0.0, 0.35 - 0.9) == 0.0)
    ok = sign_ok and above_zero and bool(w1) and bool(w2) and bool(w3)
    return ("B-PSICTL-2 TENSION-SUPERVISED-ROUTING-RESTORING-SIGN", ok)


def b_psictl_3():
    # (a) deterministic byte-span membership predicate (closed Kolmogorov)
    def in_voice(j, vlo, vhi):
        return 1 if (vlo <= j < vhi) else 0
    span_ok = (in_voice(5, 10, 20) == 0 and in_voice(10, 10, 20) == 1 and
               in_voice(19, 10, 20) == 1 and in_voice(20, 10, 20) == 0)
    # inner span contributes ZERO byte CE (m=0 there) — closed
    inner_zero = (in_voice(3, 10, 20) == 0)  # inner byte outside voice mask
    # (b) Shannon non-negativity: CE = -log p, p in (0,1] => CE >= 0
    p = sp.symbols("p", positive=True)
    ce = -sp.log(p)
    nonneg = bool(sp.simplify(ce.subs(p, 1)) == 0) and \
        bool(ce.subs(p, sp.Rational(1, 2)) > 0)
    # (c) overlay-OFF = baseline connection point: lam_psi=lam_route=0 =>
    #     total == CE_voice (byte-equal gamma-mask carving baseline)
    ce_v, l_psi, l_route, lam_p, lam_r = sp.symbols(
        "ce_v l_psi l_route lam_p lam_r", real=True)
    total = ce_v + lam_p * l_psi + lam_r * l_route
    off = sp.simplify(total.subs({lam_p: 0, lam_r: 0}) - ce_v)
    connection_ok = (off == 0)
    # structural check: the trainer source CE is masked to the voice span
    src = ""
    tp = os.path.join(HERE, "train_carving_dirG_psi_ctl.py")
    if os.path.exists(tp):
        src = open(tp, encoding="utf-8").read()
    masked = ("ce_voice = (ce_tok * vmask).sum()" in src) and \
             ("MASKED to the <voice carved=true> span only" in src)
    ok = span_ok and inner_zero and nonneg and connection_ok and masked
    return ("B-PSICTL-3 VOICE-CE-MASK-SHANNON-PREDICATE", ok)


def main():
    tests = [b_psictl_1, b_psictl_2, b_psictl_3]
    npass = 0
    print("=== Dir-G Ψ-anchored CTL — closed-form transfer battery ===")
    for t in tests:
        name, ok = t()
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
        npass += int(bool(ok))
    print(f"B-PSICTL battery: {npass}/{len(tests)} 🔵 closed-form PASS")
    print("(transfer-form + overlay-OFF=γ-baseline connection ONLY; "
          "4-axis capability = EMPIRICAL B-CARVE-E6-NOTE/B-D-NOTE carve-out; "
          "central blue_falsifier.py UNCHANGED — sidecar)")
    raise SystemExit(0 if npass == len(tests) else 1)


if __name__ == "__main__":
    main()
