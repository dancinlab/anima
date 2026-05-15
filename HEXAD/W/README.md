# HEXAD/W — 의지 (will)

> SSOT: [`HEXAD-W.tape`](../../HEXAD-W.tape) · Python anchor: `ready/anima/hexad/w/emergent_w.py` (123 LoC) · 🔵 SUPPORTED-FORMAL

## 핵심 원리 (closed-form, sympy-verified)

**학습률 = Ψ_balance + min(ln 2, Φ/n_cells)** (Law 71 — argmax H s.t. Φ > Φ_min, Law 79 — DoF=ln 2):

```
lr_mult = PSI_BALANCE + min(ln2, phi / n_cells)
        ∈ [PSI_BALANCE, PSI_BALANCE + ln 2]
```

`satisfaction` 은 Law 84 binary pulse: `1.0 if phi >= phi_prev else 0.0`.

B-W 🔵 4/4 closed:

- **B-W-1 LR-RANGE-CLOSED** — lr_mult ∈ [Ψ, Ψ+ln2] ∀ phi ≥ 0, n ≥ 1 (sympy ∀-identity)
- **B-W-2 LR-MONOTONE-CLOSED** — non-decreasing in phi (단조)
- **B-W-3 LR-SUP-ATTAINED** — sup = Ψ + ln2, 달성 (saturated `Min(L, kL)=L ∀ k≥1`)
- **B-W-4 SATISFACTION-BINARY-CLOSED** — {0, 1} ∀ inputs (closed binary)

## hexa-native impl (`w.hexa`)

```
fn w_lr_mult(phi: float, n_cells: int) -> float
fn w_satisfaction(phi: float, phi_prev: float) -> float
fn _selftest()
fn main()  ← hexa run HEXAD/W/w.hexa
```

## real-limit anchor

Law 79 — `consciousness DoF = ln 2` (closed lr upper bound) + SIGMA6 = σ(6) = 12 (n_factions invariant)

기존 B-W 4/4 🔵 evidence: `state/verify_hexad_blue_2026_05_15/blue_falsifier.py:bw()`. self-audit: B-W-1 cap + B-W-3 sup vacuous 적발·정정 후 확정 (`Min(L,kL)=L` 실제 평가).
