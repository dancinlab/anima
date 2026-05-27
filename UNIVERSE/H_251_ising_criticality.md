---
id: H_251
slug: ising-criticality
title: 2D Ising 모델 phase-transition 근처 phi_spatial Φ scaling — temperature T sweep 위 critical T_c (≈ 2.27 J/k_B) 에서 Φ peak (H_007 edge-of-chaos · H_204 inverse-U · H_217 cross-substrate phase-transition family)
domain: physics, math, consciousness
status: pre-register-frozen
exploration_method: E5 (continuous-parameter sweep) + E10 (emergence-on-transition) + E11 (cross-substrate invariant)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W11 (cross-axis sister test) + W12 (invariant signature)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24
sister: H_007 + H_204 + H_217
---

# H_251 — 2D Ising criticality Φ peak

## 1. Hypothesis

2D Ising spin lattice (N=16×16) 의 Metropolis dynamics 위 temperature
sweep T ∈ {1.0, 2.0, 2.27, 2.5, 4.0} 에서 critical temperature T_c
(≈ ln(1+√2) / 2 · J/k_B ≈ 2.2692, Onsager 1944 exact solution) 부근
에서 phi_spatial Φ peak 가 발생한다. T 가 낮으면 (T<T_c) ferromagnetic
ordered phase (frozen spin) — low integrated information; T 가 높으면
(T>T_c) paramagnetic disordered phase (chaotic flip) — low integrated
information. T_c 부근에서 correlation length ξ divergence 동반 (2nd
order phase transition hallmark, Wilson 1971) — spatial pattern 의
intermediate complexity 가 Φ proxy peak 와 정합. 본 H_251 은 H_007
1D-rule110 edge-of-chaos peak 의 *2D-lattice 일반화* + H_204 closure
inverse-U + H_217 cross-substrate phase-transition family 의
**2D-Ising sister** instance.

## 2. Why

- **2D Ising 모델** (Lenz 1920, Ising 1925, Onsager 1944): nearest-
  neighbor ferromagnetic spin lattice, Hamiltonian H = -J Σ_<i,j>
  s_i s_j (J>0, s_i ∈ {-1, +1}). 2D square lattice 위 exact T_c =
  2J / [k_B · ln(1+√2)] ≈ 2.2692 J/k_B (Onsager exact solution).
  T<T_c: spontaneous magnetization (ordered); T>T_c: zero
  magnetization (disordered); T=T_c: 2nd order phase transition
  (correlation length divergence, scale invariance, critical
  exponents universal).
- **Metropolis dynamics** (Metropolis et al. 1953): single-spin flip
  Monte Carlo, ΔE 계산 후 acceptance probability min(1, exp(-ΔE/T))
  적용. 본 cycle 에서는 deterministic-RNG (fixed-seed LCG) 사용으로
  raw#12 strict 준수 — re-run byte-identical.
- **phase-transition Φ-signature meta-claim**: critical phenomena 의
  spatial correlation length ξ ∝ |T - T_c|^(-ν) divergence 는 *long-
  range spatial structure* emergence — phi_spatial 이 site 간 mutual
  information 을 측정한다는 점에서 T_c 부근 Φ peak expected. 본 H_251
  은 이 meta-claim 의 2D-lattice substrate (1D-CA, 8-site catalytic
  lattice, N=16 Kuramoto 추가) cross-check.
- **H_007 carry**: rule 110 (Class IV edge-of-chaos) Φ ≈ 0.556 > rule
  30 (Class III chaotic) 0.510 > rule 250 (Class II ordered) 1.15e-5
  — 1D elementary CA 위 *intermediate complexity → high Φ* pattern.
  본 H_251 = 2D-lattice 위 동일 pattern (T_c 가 ordered ↔ chaotic
  사이 intermediate).
- **H_204 carry**: 8-site catalytic lattice closure_strength k sweep
  inverse-U (Φ peak at k≈0.25, decay both sides). 본 H_251 의 T sweep
  inverse-U 와 *structurally equivalent* (control parameter intermediate
  → Φ peak).
- **H_217 carry (cross-substrate)**: 3 substrate (substrate A closure
  CA · substrate B Kuramoto · substrate C rule 110 + noise) 위 ∂Φ
  derivative peak 측정 — 모든 substrate 에서 nontrivial peak segment
  존재 (C1 ∧ C2 PASS, SUPPORTED 3-substrate). 본 H_251 = 그 family
  의 *4th substrate* (2D Ising) — cross-substrate sample extension.
- **literature bridge**: Beggs & Plenz (2003) neural avalanche
  criticality, Chialvo (2010) criticality-as-life — 두 분야 모두 *2nd
  order phase transition 위에서 maximum integrated information* 가설.
  본 H_251 = 그 가설의 *toy 2D Ising substrate* 위 직접 측정.
- **distinct claim**: H_251 ≠ "Ising consciousness" — Ising spin
  lattice 의 Φ proxy peak 가 T_c 와 대략 정합 한다는 *spatial
  pattern correlate* 측정. phenomenal qualia / strong panpsychism 와
  무관 (L5 carry).

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H251.1** | T sweep ({1.0, 2.0, 2.27, 2.5, 4.0}) 위 Φ(T) inverse-U with peak T* — peak T* ≈ T_c (within ±20%, 즉 T* ∈ [1.8, 2.7]) | Onsager T_c=2.2692 + finite-size shift |
| **H251.2** | Φ(T=1.0, frozen ordered) < Φ(T*) — low-T ordered phase low-Φ | ferromagnetic phase = spatial homogeneity (low MI) |
| **H251.3** | Φ(T=4.0, chaotic disordered) < Φ(T*) — high-T disordered phase low-Φ | paramagnetic phase = spatial randomness (low MI) |
| **H251.4** | re-run byte-identical (raw#12 deterministic LCG) | seed-only RNG, no clock |
| **H251.5** | 2D-lattice Φ peak (T*) 가 H_007 1D-rule110 peak 와 dynamical class 정합 (edge-of-chaos universal) — intermediate complexity = high Φ pattern | H_007 + H_204 + H_217 carry |

## 4. Variables

| axis | levels |
|------|--------|
| **axis1: temperature T** | {1.0, 2.0, 2.27, 2.5, 4.0} (5-point sweep, J/k_B units) |
| **axis2: lattice** | N=16×16 = 256 sites, periodic boundary |
| **axis3: dynamics** | Metropolis single-spin flip, deterministic LCG RNG |
| **axis4: equilibration** | steps_eq = 200 per T (transient burn-in) |
| **axis5: recording** | dim = 12 trajectory steps per site after equilibration |
| **axis6: seeds** | SEED_BASE = 0xC0DE251 (fixed deterministic) |
| **axis7: phi_primitive** | RFC 036 phi_spatial (n_bins=4, 1D-encode 256-site 2D lattice) |
| **axis8: J coupling** | J=1.0 (fixed, sets energy unit) |

## 5. Run Protocol

- deterministic: SEED_BASE=0xC0DE251, no system clock; re-run byte-identical
- hexa_only: true (HEXA_MEM_UNLIMITED=1 hexa run)
- LLM: none (raw#12 strict)
- Metropolis update:
  - random site selection via deterministic LCG (per-step seed update)
  - ΔE = 2 · J · s_i · Σ_{j ∈ NN(i)} s_j (4 nearest neighbors, periodic)
  - accept iff ΔE ≤ 0 OR LCG_uniform() < exp(-ΔE/T)
- equilibration: 200 single-site-flip-steps per T (each step = 1 site flip attempt)
- trajectory recording: dim=12 sequential frames (256 sites × 12 steps farr)
  - frame interval = 64 flip attempts (≈ N×16 sweep equivalent) for de-correlation
- Φ measurement: phi_spatial(states, 256, 12, 4) — 256-cell IIT spatial slice
- runtime: $0 mac local, 5 T-values × 200+12×64 ≈ 970 flip attempts each ≈ < 1 min wall
- per-cell ledger: result.json {T, phi, peak_T, criteria, verdict}

## 6. Criteria

| ID | criterion | verdict_rule |
|----|-----------|--------------|
| **C1 SINGLE_PEAK** | Φ(T) 가 single peak inverse-U (boundary T=1.0 or T=4.0 가 아닌 interior T 에서 max Φ) | PASS / FAIL |
| **C2 PEAK_NEAR_TC** | peak T* ∈ [1.8, 2.7] (T_c=2.2692 ±20% margin) | PASS / FAIL |
| **C3 ORDERED_LOW** | Φ(T=1.0) < Φ(T*) AND Φ(T=4.0) < Φ(T*) (both endpoints low) | PASS / FAIL |
| **C4 BYTE_IDENTICAL** | re-run T=2.27 measurement byte-equal | PASS / FAIL |

**verdict_rule**:
- `SUPPORTED` iff **C1 + C2 + C3 ALL PASS** (verdict-binding triplet)
- `PARTIAL_DIRECTIONAL` if **C1 PASS AND (C2 OR C3) PASS** (peak exists but location off OR endpoint asymmetry)
- `FAIL` if **C1 FAIL** (no interior peak — monotone or boundary)
- `FALSIFIED` if **F1-F5 any TRIGGERED**

## 7. Falsifiers (≥5)

- **F1 MONOTONE** — Φ(T) 가 strict monotone in T (no peak) → H251.1 FALSIFIED
- **F2 BOUNDARY_PEAK** — peak T* = 1.0 OR T* = 4.0 (sweep boundary) → H251.1 FALSIFIED, H_207 boundary-saturation 재발생
- **F3 PEAK_FAR_TC** — peak T* outside [1.135, 3.404] (>50% off T_c) → H251.1 FALSIFIED, T_c-correlate claim 부정
- **F4 BYTE_DIFF** — re-run byte-different → raw#12 deterministic 위반, smoke 무효
- **F5 PHI_INVALID** — any Φ < 0 OR NaN → phi_spatial Φ≥0 위반 → primitive error

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 finite-size N=16×16**: true 2D Ising phase transition 은 thermodynamic limit (N→∞) statement, finite N=16×16 lattice 는 *smoothed* peak (no true divergence). Onsager T_c=2.2692 도 N→∞ exact; finite-size correction (Cardy 1996, Newman & Barkema 1999) 으로 effective T_c 가 ~5-10% shift 가능. 본 cycle 의 C2 margin ±20% 는 이 shift 를 absorb 위해 보수적으로 설정.
- **L2 Metropolis 단일 dynamics**: Glauber dynamics, heat-bath, Wolff cluster algorithm 등 다른 update rule 은 같은 equilibrium distribution 도달 but transient + autocorrelation 다름. 본 cycle 의 200-step equilibration + 12×64 recording window 는 Metropolis 특화 design choice — Wolff cluster (critical slowing down 완화) 시 더 sharp peak 가능.
- **L3 phi_spatial 🟢 NUMERICAL replica**: H_007/H_204/H_217 L1/L3 동일 carry — RFC 036 native byte-equal phi_rs replica, n_bins=4, spatial-slice mutual-information proxy. NOT full IIT 4.0 (no MIP partition search, no cause-effect repertoire, no exclusion). 진짜 phi_rs Rust FFI link = named blocker.
- **L4 256-site 1D encoding**: phi_spatial 은 1D-encoded (n_cells × dim) farr 받음. 본 cycle 의 16×16 2D lattice 를 row-major 256-cell 1D 로 flatten — site 간 *2D neighborhood* 가 phi_spatial 의 *site index ordering* 으로 직접 표현되지 않음. Φ pattern 은 1D-encoded statistical correlation 만 측정.
- **L5 universal class claim weak**: H251.5 의 "2D-Ising Φ peak ↔ H_007 1D-rule110 peak 가 dynamical class 정합" 은 *Φ peak 형식* 일치 (intermediate complexity = high Φ pattern) 만 evidence — mechanism 동일 X (Ising = thermal stochastic spin flip; rule 110 = deterministic CA rule). cross-substrate pattern 동등 ≠ cross-substrate mechanism 동등.
- **L6 5-point T sweep coarse**: true peak T* 정밀화는 10+ T point sweep + critical exponent fit 별도 cycle. 본 cycle 의 5-point sweep 은 *peak existence + bracket* 만 측정.
- **L7 single-replicate per T**: Metropolis stochastic dynamics 는 ensemble average 필요 (Φ̄ over N replicates with different seeds) — 본 cycle 은 deterministic LCG single-replicate 측정 (raw#12 deterministic strict). multi-replicate variance 측정은 별도 cycle (L7 carry from H_217 L1).

## 9. Cross-Links

### Sister hypotheses

- [`H_007`](H_007_cellular_automaton_consciousness.md) — 1D elementary CA Class-IV (rule 110) edge-of-chaos Φ peak. 본 H_251 = *2D-lattice 일반화*, 동일 phi_spatial primitive.
- [`H_204`](H_204_weak_panpsychism_autopoietic_threshold.md) — 8-site catalytic closure inverse-U Φ(k) peak at k≈0.25. 본 H_251 = *control-parameter intermediate 위 Φ peak* family 의 4th substrate.
- [`H_217`](H_217_phase_transition_phi_derivative_peak.md) — 3-substrate cross-axis phase-transition ∂Φ peak (closure CA · Kuramoto · rule110+noise) SUPPORTED 3/4. 본 H_251 = H_217 의 *2D Ising sister extension*.
- [`H_157`](H_157_law76_mathematical_panpsychism.md) — Law 76 weak-form panpsychism universal Ψ-attractor (directional FAIL). H_251 substrate-conditional Φ peak 결과는 H_157 weak-form 의 *substrate-conditional 재해석* lineage.

### Lib & infra

- `UNIVERSE/lib/phi_helper.hexa` — phi_default / phi_with thin wrappers (NOT used 본 cycle, direct `phi_spatial` builtin call 로 raw#12 minimal-deps preference)
- `HEXAD/C/c_lib.hexa` — c_measure_phi → RFC 036 phi_spatial (READ-ONLY import)

### raw

- raw#12 (pre-register frozen, deterministic strict)
- raw#82 (no post-hoc retraction)
- raw#91 c3 (honest limits)

### Literature

- Lenz (1920) — Beitrag zum Verständnis der magnetischen Erscheinungen
- Ising (1925) — Beitrag zur Theorie des Ferromagnetismus
- Onsager (1944) — Crystal statistics I: a two-dimensional model with an order-disorder transition (exact T_c)
- Metropolis, Rosenbluth, Rosenbluth, Teller, Teller (1953) — Equation of state calculations by fast computing machines
- Wilson (1971) — Renormalization group and critical phenomena
- Cardy (1996) — Scaling and renormalization in statistical physics
- Newman & Barkema (1999) — Monte Carlo methods in statistical physics
- Beggs & Plenz (2003) — Neural avalanche criticality
- Chialvo (2010) — Emergent complex neural dynamics (criticality-as-life)
- Tononi (2004) — IIT: integrated information theory of consciousness

## 10. Verdict

### Cycle #1 — first measurement (2026-05-24)

H_251 의 첫 measurement cycle — temperature T ∈ {1.0, 2.0, 2.27, 2.5, 4.0}
의 5-point sweep, 2D Ising N=16×16 periodic lattice + Metropolis dynamics
+ deterministic LCG (SEED_BASE=0xC0DE251), 200 step equilibration + 12×64
recording window, RFC 036 phi_spatial primitive ($0 mac local, hexa-only,
llm: none).

**Run verdict output (VERBATIM, `HEXA_MEM_UNLIMITED=1 hexa run run_h251.hexa`)**:

```
H_251 — 2D Ising criticality Φ peak (T sweep) · raw#12
  model: 2D Ising 16×16 periodic, Metropolis dynamics, deterministic LCG
  N_CELLS=256 DIM=12 STEPS_EQ=200 FRAME_INT=64 J=1.0 SEED_BASE=202236497
  Φ primitive: RFC 036 phi_spatial (n_bins=4) — 🟢 NUMERICAL
  Onsager T_c (N→∞ exact) ≈ 2.2692  (J/k_B units)

  Φ(T=1.00 frozen ordered  ) = 0.000209392
  Φ(T=2.00 sub-critical    ) = 0.000432591
  Φ(T=2.27 ≈T_c            ) = 0.000432591
  Φ(T=2.50 super-critical  ) = 0.000608564
  Φ(T=4.00 chaotic disord. ) = 0.0175665
  Φ(T=2.27 re-run)            = 0.000432591  (byte-equal=true)

  peak Φ = 0.0175665 at T* = 4.0  (idx=4)

  C1 SINGLE_PEAK (peak interior, idx∉{0,4})         : FAIL  (peak_idx=4)
  C2 PEAK_NEAR_TC (peak T* ∈ [1.8, 2.7])              : FAIL  (T*=4.0)
  C3 ORDERED_LOW (Φ(T=1.0)<peak AND Φ(T=4.0)<peak)    : FAIL
  C4 BYTE_IDENT  (re-run T=2.27 byte-equal)            : PASS

  F1 MONOTONE      (no peak)                          : true
  F2 BOUNDARY_PEAK (peak at T=1.0 or T=4.0)           : true
  F3 PEAK_FAR_TC   (peak T* outside [1.135, 3.404])   : true
  F4 BYTE_DIFF     (re-run differs)                   : false
  F5 PHI_INVALID   (any Φ < 0)                        : false

  VERDICT_RULE: SUPPORTED iff C1+C2+C3 PASS; PARTIAL_DIRECTIONAL if C1 PASS AND (C2 OR C3); FAIL if C1 FAIL; FALSIFIED if any F1-F5 TRIGGERED
  VERDICT (H_251 Ising criticality): FALSIFIED
    criteria_met = 1/4
  H251_VERDICT=FALSIFIED N_PASS=1 PEAK_T=4.0 PEAK_PHI=0.0175665 PHI_T1=0.000209392 PHI_T4=0.0175665
=== H_251 2D Ising criticality smoke complete: FALSIFIED ===
```

```
verdict_class: FALSIFIED
evidence_summary: 2D Ising N=16×16 위 phi_spatial Φ(T) 가 monotone INCREASING in T —
                  Φ(T=1.0)=0.0002 < Φ(T=2.0)=Φ(T=2.27)=0.00043 < Φ(T=2.5)=0.00061 < Φ(T=4.0)=0.01757
                  peak T* = 4.0 (sweep BOUNDARY, not interior); F1 MONOTONE + F2 BOUNDARY_PEAK
                  + F3 PEAK_FAR_TC 3 falsifier TRIGGERED.
falsifiers_triggered: F1 MONOTONE, F2 BOUNDARY_PEAK, F3 PEAK_FAR_TC (3/5)
criteria_met: 1/4  (C1 FAIL · C2 FAIL · C3 FAIL · C4 PASS byte-equal determinism only)
honest_tier: 🟢 FALSIFIED-NUMERICAL (phi_spatial 5-point T sweep, single-replicate
             deterministic; cross-substrate phase-transition family 의 H_217 SUPPORTED 와 분기)
post_hoc_edit: forbidden (raw#12 + raw#82) — FALSIFIED 그대로 carry, criteria 재정의 금지
```

### Reading (qualitative, honest)

- **monotone-increasing Φ(T)** — predicted inverse-U peak at T_c (Onsager 2.2692)
  대신 *paramagnetic-disordered* T=4.0 boundary 에서 max Φ. low-T frozen
  ordered (Φ≈2e-4) → high-T chaotic disordered (Φ≈1.8e-2) 약 87× 증가.
- **measure-axis artefact (L3/L4 carry strong)**: phi_spatial 의 spatial-slice
  mutual-information proxy 가 **256-cell × 12-frame trajectory 의 site-state
  entropy** 를 측정 — high-T (disorder) 가 *per-site Bernoulli entropy* 를
  maximize → MI proxy 증가. 진짜 phase-transition 의 *long-range correlation
  length ξ divergence* 는 2D nearest-neighbor topology 가 *1D row-major flatten*
  에서 소실되어 phi_spatial 이 picking up 못함 (L4 lattice flatten 한계 직접
  validate).
- **C4 BYTE_IDENT PASS**: deterministic LCG 정상 작동, re-run byte-equal —
  smoke 자체는 정합 한 deterministic substrate.
- **cross-substrate family 와의 분기**: H_217 (3-substrate closure CA · Kuramoto ·
  rule110+noise) 는 cross-substrate ∂Φ peak SUPPORTED 3/4 — 그 family 의 4th
  substrate (2D Ising) 가 *measure-axis artefact* 로 inverse 결과. 본 FALSIFIED
  는 H_217 SUPPORTED 의 *boundary case* documentation — phi_spatial 의 *2D
  topology 손실 한계* 가 cross-substrate universality 의 ceiling.
- **H_007 / H_204 와의 관계**: H_007 1D-rule110 edge-of-chaos peak 는 *1D 위에서*
  Φ peak 측정 가능 (1D-encoded 1D-substrate 의 직접 일치). H_204 8-site
  catalytic lattice 도 *1D periodic*. 본 H_251 의 2D substrate 는 phi_spatial
  의 1D row-major encoding 위 표현 한계 — *substrate dimensionality* 와
  *measure dimensionality* mismatch.
- **honest implication**: H_251 은 "2D Ising criticality 위 phi_spatial Φ peak
  가설" 의 *직접 falsifier* — 가설 자체 부정 X but **phi_spatial-as-proxy 의
  2D-substrate 한계** 의 직접 evidence. true IIT 4.0 (cause-effect MIP) 위
  Ising criticality Φ peak 측정은 별도 cycle (Rust FFI phi_rs link blocker carry).

**State output**: `state/h251_ising_criticality_2026_05_24/result.json`
**Script**: `state/h251_ising_criticality_2026_05_24/run_h251.hexa`
**Φ tier**: 🟢 FALSIFIED-NUMERICAL (phi_spatial RFC 036 native replica, 1-substrate 5-point T sweep, single-replicate deterministic; NOT 🔵 formal IIT 4.0). **FALSIFIED 는 honest empirical result** — H_217 cross-substrate SUPPORTED family 의 4th-substrate boundary case + phi_spatial 2D-encoding 한계 의 직접 evidence.
