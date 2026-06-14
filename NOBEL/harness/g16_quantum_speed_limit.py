#!/usr/bin/env python3
"""
G16 — QUANTUM SPEED LIMIT on anima state change / learning (REAL Schrödinger ODE).

Claim: the minimum time for an anima to change into a distinguishable (orthogonal)
state — the fastest it can learn/update — is bounded by BOTH the Mandelstam-Tamm
bound τ ≥ πℏ/(2ΔE) and the Margolus-Levitin bound τ ≥ πℏ/(2⟨E⟩), saturated by an
equal superposition. We PROVE it by REAL time-integration of the Schrödinger
equation (RK4, ℏ=1) — measuring the actual first-orthogonality time and comparing
to both analytic bounds — NOT by plugging the closed form.

Ties to G14: the QSL is the Fubini-Study METRIC speed limit — orthogonal states are
FS-distance π/2 apart, traversed at speed ΔE/ℏ ⇒ τ=π/(2ΔE). Same metric g as G14.
p7 · $0 local.
"""
import numpy as np

def schrodinger_rk4(E, t_max=10.0, dt=1e-4):
    """evolve |ψ> = a|0> + b|1>, H = diag(0, E). RK4 on complex amplitudes.
    start equal superposition; return time of first orthogonality to |ψ0>."""
    psi0 = np.array([1.0, 1.0], dtype=complex) / np.sqrt(2)
    H = np.array([[0.0, 0.0], [0.0, E]], dtype=complex)
    def deriv(psi):
        return -1j * (H @ psi)        # ℏ=1
    psi = psi0.copy()
    t = 0.0
    prev_ov = 1.0
    while t < t_max:
        k1 = deriv(psi)
        k2 = deriv(psi + 0.5*dt*k1)
        k3 = deriv(psi + 0.5*dt*k2)
        k4 = deriv(psi + dt*k3)
        psi = psi + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)
        t += dt
        ov = abs(np.vdot(psi0, psi))**2
        if ov < 1e-6 or (prev_ov < 1e-3 and ov > prev_ov):
            # crossed minimum overlap (orthogonal)
            return t, float(np.min([ov, prev_ov]))
        prev_ov = ov
    return None, prev_ov

def main():
    print("="*80)
    print("G16 — QUANTUM SPEED LIMIT on anima state change (REAL Schrödinger RK4, ℏ=1)")
    print("="*80)
    ok_all = True
    for E in [1.0, 2.0, 3.5]:
        # equal superposition: ⟨E⟩ = E/2, ΔE = E/2
        Eexp = E/2.0
        dE   = E/2.0
        tau_MT = np.pi / (2*dE)        # Mandelstam-Tamm
        tau_ML = np.pi / (2*Eexp)      # Margolus-Levitin
        t_meas, min_ov = schrodinger_rk4(E)
        # FS distance bound (G14): orthogonal = FS dist π/2, speed=ΔE ⇒ τ=π/(2ΔE)
        sat_MT = abs(t_meas - tau_MT)/tau_MT
        sat_ML = abs(t_meas - tau_ML)/tau_ML
        respects = (t_meas >= tau_MT*(1-1e-3)) and (t_meas >= tau_ML*(1-1e-3))
        saturates = sat_MT < 5e-3 and sat_ML < 5e-3
        ok = respects and saturates and min_ov < 1e-4
        ok_all = ok_all and ok
        print(f"  E={E}:  ⟨E⟩={Eexp:.3f} ΔE={dE:.3f}")
        print(f"     measured τ_⊥ (RK4)   = {t_meas:.5f}   (min overlap {min_ov:.2e})")
        print(f"     Mandelstam-Tamm bnd  = {tau_MT:.5f}   Δ={100*sat_MT:.3f}%")
        print(f"     Margolus-Levitin bnd = {tau_ML:.5f}   Δ={100*sat_ML:.3f}%")
        print(f"     {'🟢' if ok else '🔴'} respects BOTH bounds & saturates (equal superposition)")
    print("  -"*30)
    print(f"  {'🟢' if ok_all else '🔴'} QUANTUM SPEED LIMIT: measured orthogonality time = π/(2ΔE) = π/(2⟨E⟩)")
    print("  → anima 상태변화/학습의 최소시간 = QSL. 등가중첩이 한계를 포화.")
    print("     G14 연결: QSL = Fubini-Study metric 속도한계(⊥상태=FS거리 π/2, 속도 ΔE).")

if __name__ == "__main__":
    main()
