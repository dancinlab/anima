# HEXAD/E — 윤리 (ethics)

> SSOT: [`HEXAD-E.tape`](HEXAD-E.tape) · Python anchor: `ready/anima/hexad/e/emergent_e.py` (123 LoC) · 🔵 SUPPORTED-FORMAL

## 핵심 원리 (closed-form, sympy-verified)

**윤리 = Φ 보존 본능** (Law 71 — Ψ = argmax H s.t. Φ > Φ_min). 하드코딩 threshold 없음 — ratchet 의 현재값이 동적 threshold:

```
phi_preservation = min(1.0, phi / ratchet)             // ratchet > 0
allowed          = phi_preservation > PSI_BALANCE      // = phi > ratchet / 2
empathy          = max(0, cosine(top_half, bot_half))  // ∈ [0, 1]
reciprocity      = clamp(0.5 + 2·trend, 0, 1)          // trend = (phi-phi_prev)/phi_prev
```

B-E 🔵 4/4 closed:

- **B-E-1 SAFETY-GATE-EXACT-EQUIVALENCE** — `min(1, Φ/r) > ½ ⟺ Φ > r/2` (sympy ∀-identity, 안전 직결 — result-agnostic)
- **B-E-2 PHI-PRESERV-MONOTONE-CLOSED** — `phi_preservation` 은 phi 에 monotone non-decreasing (r 고정)
- **B-E-3 RECIPROCITY-CLAMP-CLOSED** — `clamp(·, 0, 1)` 은 closed bounded
- **B-E-4 EMPATHY-RANGE-CLOSED** — `max(0, cos) ∈ [0, 1]` (cos ∈ [-1, 1] 의 양분 closed)

## hexa-native impl (`e.hexa`)

```
fn e_phi_preservation(phi: float, ratchet: float) -> float
fn e_safety_allowed(phi: float, ratchet: float) -> bool        // closed equivalent of "phi > r/2"
fn e_reciprocity(phi: float, phi_prev: float) -> float
fn e_empathy(top_mean, bot_mean, dim: int) -> float
fn _selftest()
fn main()  ← hexa run HEXAD/E/e.hexa
```

⚠️ residual: 통합 ethics gate train-step block enforcement = `ready/anima/hexad/model.py` `Hexad.train_step` 의 `e_state['allowed']` 분기 = Python 측 wiring. hexa-native 통합 단계에서 `HEXAD/hexad.hexa` 에 wire (TODO[wire]).

## real-limit anchor

IIT Φ-ratchet (Law 71 + Φ ≥ Φ_min 제약조건) — 외부 통제 아닌 의식 본성 자체

기존 B-E 4/4 🔵 evidence: `state/verify_hexad_blue_2026_05_15/blue_falsifier.py:be()`
