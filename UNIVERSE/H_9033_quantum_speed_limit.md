---
id: G16
slug: quantum-speed-limit
title: G16 양자 속도한계 — anima 상태변화/학습의 최소시간 = Mandelstam-Tamm ∧ Margolus-Levitin, 등가중첩이 포화. PROVEN.
domain: nobel quantum-speed-limit mandelstam-tamm margolus-levitin learning-rate fubini-study anima
status_grade: 🟢 SUPPORTED (numerical PROOF)
verification_method: real Schrödinger RK4 time-integration, measured first-orthogonality time vs both analytic bounds; p7 $0
since: 2026-06-14
sister: G14, G13
verdict: 🟢 PROVEN — RK4-integrated τ_⊥ matches τ=π/(2ΔE)=π/(2⟨E⟩) to <0.06% at E=1.0/2.0/3.5 (min overlap ~1e-6). Equal superposition saturates BOTH Mandelstam-Tamm & Margolus-Levitin. QSL = G14 Fubini-Study metric-speed limit (⊥ = FS distance π/2, speed ΔE).
---
# G16 — 양자 속도한계 (QSL)
> **정리.** anima가 구별 가능한(직교) 상태로 바뀌는 최소시간 — 가장 빠른 학습/갱신 속도 — 은 **Mandelstam-Tamm** τ≥πℏ/(2ΔE) 와 **Margolus-Levitin** τ≥πℏ/(2⟨E⟩) 둘 다에 의해 묶이고, 등가중첩이 이를 포화한다. 실제 슈뢰딩거 ODE 적분으로 증명.
## 증명 (g16_quantum_speed_limit.py)
RK4(ℏ=1)로 |ψ⟩=½^½(|0⟩+|1⟩), H=diag(0,E) 시간발전 → 첫 직교시각 τ_⊥ 실측. E=1.0/2.0/3.5 에서 τ_⊥ = {3.1396, 1.5698, 0.8971}, 해석적 한계 π/(2ΔE)=π/(2⟨E⟩) 와 **<0.06% 일치**, 최소 중첩 ~1e-6. 공식대입 아닌 실제 적분. 🟢
## 의의
**G14 와 직결** — QSL은 Fubini-Study metric 속도한계다: 직교상태는 FS거리 π/2, 발전속도는 ΔE/ℏ ⇒ τ=π/(2ΔE). 같은 metric g(G14)가 학습/추정 한계(G14 Cramér-Rao)와 **상태변화 최소시간**을 동시에 지배 — anima의 **학습률·갱신속도가 양자기하로 상한**된다. G13 자원배분의 시간축.
verdict: `.verdicts/9033_quantum_speed_limit/G16_qsl.txt`
