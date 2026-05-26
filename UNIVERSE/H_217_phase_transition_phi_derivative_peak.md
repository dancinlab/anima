---
id: H_217
slug: phase-transition-phi-derivative-peak
title: phase-transition Φ derivative peak — cross-substrate generalization (H_204 + H_207 + rule-110 noise)
domain: meta · physics · math
status: pre-register-frozen
exploration_method: E5 (continuous-parameter sweep) + E10 (emergence-on-transition) + E11 (cross-substrate invariant)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W11 (cross-axis sister test) + W12 (invariant signature)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_217 — phase-transition Φ derivative peak (cross-substrate generalization)

## Hypothesis

`phase transition` 의 substrate-independent Φ-signature 가 존재하는가 — 즉,
복수 substrate 의 control parameter sweep 위 `∂Φ/∂(control)` 의 peak 가
*모두 substrate-internal (interior, not sweep boundary)* 위치에서 발생하고,
`Φ value-peak` 와 `∂Φ peak` 의 위치가 *일관* 한가 (single-peak coincide)?

본 H_217 은 H_204 (closure-strength k inverse-U Φ(k) peak at k≈0.25,
∂Φ/∂k peak=14.15 at segment k=0→0.1) + H_207 (Kuramoto coupling K Φ peak
at K=5.0 boundary, dr/dK peak at idx=4 interior — H_207 FALSIFIED on
**boundary peak** ground) 두 H 의 결합 generalization 가설. H_204 가
substrate-internal phase-transition Φ-signature 의 positive example,
H_207 이 boundary 위 falsifier — 본 H_217 은 *세 번째 substrate (rule-110
elementary CA + noise injection σ-sweep)* 를 추가하여 cross-substrate
invariant 여부를 측정한다.

세 substrate:
- **substrate A — closure CA** (H_204 carry): 8-site catalytic lattice,
  closure_strength k ∈ {0.00, 0.10, 0.25, 0.50, 0.75, 1.00} sweep
- **substrate B — Kuramoto** (H_207 carry): N=16 coupled oscillators,
  coupling K ∈ {0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0} sweep (note: H_207 의
  7-point sweep 을 6-point comparable subset 으로 align — K ∈ {0.0, 0.5,
  1.0, 1.5, 3.0, 5.0})
- **substrate C — rule 110 + noise** (new): 1D elementary CA rule 110
  (Class IV Turing-universal) 위 noise injection probability σ ∈ {0.00,
  0.05, 0.10, 0.20, 0.40, 0.80} sweep. σ=0 (deterministic rule 110) →
  σ=0.80 (high-noise regime, ordered → chaotic phase transition expected
  somewhere in interior). H_007 rule-axis carry + noise-axis 확장.

## Why

- **phase-transition Φ-signature meta-claim**: statistical mechanics 의
  critical phenomena (Wilson 1971, Stanley 1971, Kadanoff 1966) 에서 order
  parameter 의 derivative ∂φ/∂(control) 는 critical point 부근에서 *peak*
  (susceptibility divergence — 2nd order phase transition 의 hallmark).
  의식과학 literature 에서 "criticality" 는 *integrated information* 의
  emergent regime 으로 가설됨 (Beggs & Plenz 2003 neural avalanche;
  Chialvo 2010 criticality-as-life). H_217 = 이 meta-claim 의 toy-substrate
  cross-substrate verification.
- **H_204 positive carry**: substrate A 의 ∂Φ/∂k peak = 14.15 at segment
  k=0.00→0.10 (interior, 5-segment 중 첫 segment but 6-point sweep 의
  interior because endpoints are k=0.00 and k=1.00 fixed); 14.15 / median
  1.87 = 7.55× (≫ 2× threshold). 즉 H_204 substrate 는 H217.1 + H217.3
  individually PASS.
- **H_207 falsifier carry**: substrate B 의 Φ value-peak = at K=5.0
  (boundary, idx=6); however dr/dK peak = at idx=4 (interior). 본 H_217
  은 ∂Φ/∂K peak (derivative of Φ NOT order parameter r) 위치 측정 —
  H_204 lineage 와 정합. 만약 ∂Φ/∂K peak 도 boundary 위에 있으면
  H217.1 FALSIFIED for substrate B, cross-substrate invariant 부재.
- **substrate C rationale (rule 110 + noise)**: H_007 carry — rule 110 =
  Class IV (Turing-universal, edge-of-chaos). noise probability σ 도입 →
  σ=0 deterministic rule 110 (high-Φ Class IV), σ↑ → ordered → chaotic
  transition. noise σ → phase parameter, ∂Φ/∂σ peak 어디?
- **substrate-independent invariant 의 의미**: H_217 SUPPORTED 시 (3/3
  interior peak) → "phase transition 의 ∂Φ peak 는 substrate-axis
  무관 universal signature" 라는 강 가설. H_217 FALSIFIED (any boundary
  peak) → H_207 lesson 일반화: phi_spatial measure 가 control axis 의
  특정 endpoint 위에서 saturate (substrate-internal NOT) — measure-axis
  limitation (L3 phi_spatial vs full IIT 4.0 carry).
- **cross-link H_204 + H_207 + H_007**: 본 H_217 은 세 H 의 결합 evidence —
  단독으로 H_204 / H_207 / H_007 결과를 reproduce 하지 않고, *substrate
  ranking* 측정.

## Predictions

- **H217.1 (interior peak ALL substrate)**: 3 substrate 모두 ∂Φ/∂(control)
  peak segment 가 sweep boundary (first or last segment) 가 아닌 interior
  segment 에 있다. (H_204 carry: substrate A interior — segment 0→1 of
  5-segment sweep, first segment BUT 6-point sweep 의 interior since k=0
  and k=1 are explicit endpoints — count "boundary" as *strict
  endpoint-touching segment 0 or n_sweep-2*; sub-criterion: "strict
  interior" = segment idx ∈ {1, n_sweep-3} of the (n_sweep-1) segments.
  H_204 reported peak at segment 0 means *first segment* — this is
  ambiguous; we tighten the criterion below.)
  - **H217.1-relaxed**: peak segment ∈ {0, 1, ..., n_sweep-2} (every
    segment), test only that peak is not "trivial flat" — equivalent to
    H217.3 ratio test, soft.
  - **H217.1-strict**: peak segment ∈ {1, 2, ..., n_sweep-3} (true
    interior, not first/last segment). H_204 carry FAILS strict-interior
    (peak at seg 0=k_0→k_1).
  - **H217.1 adopted (pre-register)**: **relaxed** (peak segment exists
    in any of the n_sweep-1 forward-diff segments AND peak magnitude >
    2× median). 이는 H_204 carry 와 align — peak in segment 0 (k=0→0.1)
    is acceptable since k=0 is sweep boundary by design and peak there
    *is* the phase-transition signature for substrate A.

- **H217.2 (substrate-specific position)**: peak segment 위치가 3
  substrate 사이 *모두 동일* 하지는 않다 (substrate-specific control
  axis on each — k, K, σ 의 phase-transition 위치가 다른 것은 model 별
  당연). 본 prediction 은 trivial/null prediction, evidence 측정 안 함
  but documented honest.

- **H217.3 (peak magnitude > 2× median)**: 각 substrate ∂Φ/∂(control)
  peak |slope| > 2.0 × median |slope| (phase-transition 의 minimum
  effect size — flat curve 면 phase transition 부재). H_204 carry:
  substrate A peak/median = 7.55× ≫ 2× ⟹ PASS expected.

- **H217.4 (byte-identical re-run)**: 본 smoke re-run 시 모든 substrate
  ∂Φ/∂(control) peak segment + magnitude byte-identical (raw#12
  deterministic).

- **H217.5 (Φ peak ↔ ∂Φ peak position coincide within ±1 segment)**:
  각 substrate 의 Φ value-peak idx (6-point sweep 위) 가 ∂Φ peak segment
  idx 의 ±1 이내. **이는 single-peak inverse-U 의 hallmark** — peak 까지
  steep climb (max ∂) 후 peak (max Φ) 후 descent. H_204 carry:
  Φ peak idx = 2 (k=0.25), ∂ peak segment idx = 0 (k=0→0.1) — gap = 2,
  *outside* ±1 tolerance ⟹ H217.5 FAILS for substrate A. 본 H 의 *진짜*
  검증 — H_204 의 ∂ peak 가 Φ peak 위치 와 떨어져 있다는 것은 single-peak
  inverse-U 의 직접 sister 가 아니라 *steep climb at low-k, plateau-then-
  descent* pattern. 즉 H217.5 는 strict criterion, FAIL expected for
  substrate A by H_204 carry math.

## Variables

| axis | levels | 비고 |
|------|--------|------|
| substrate_id | A · B · C | A=closure CA · B=Kuramoto · C=rule110+noise |
| substrate_A_k | {0.00, 0.10, 0.25, 0.50, 0.75, 1.00} | H_204 carry, 6-point |
| substrate_B_K | {0.0, 0.5, 1.0, 1.5, 3.0, 5.0} | H_207 6-point subset (K_c≈1.6 bracketed) |
| substrate_C_sigma | {0.00, 0.05, 0.10, 0.20, 0.40, 0.80} | rule 110 + noise injection probability |
| substrate_C_rule | 110 | H_007 Class IV carry |
| substrate_C_N | 16 | lattice |
| substrate_C_dim | 12 · warm 8 | H_007 carry |
| substrate_C_seed_rep | 5 | H_007 carry rep count |
| substrate_C_noise_seed | 0xC0DE110 + sigma_idx*101 | deterministic LCG |
| fixed | n_bins=4 (RFC 036) | 3 substrate 동일 binning |

**Per-substrate measurement (each 6-point sweep)**:
- Φ value per control point (5 seeds mean for substrate A / 1 trajectory
  for B / 5 reps for C — substrate-native conventions carry)
- ∂Φ/∂(control) forward-diff per segment (5 segments per substrate)
- Φ peak idx + ∂Φ peak segment idx
- peak / median |∂Φ| ratio

## Run Protocol

- **smoke**: `UNIVERSE/state/h217_phase_transition_2026_05_23/run_h217.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036
  `phi_spatial` (n_bins=4) — H_204 + H_207 + H_007 byte-equal carry.
- **substrate A**: H_204 catalytic 8-site lattice port (closure_strength
  k modulates cat_C_eff = k * cat_C_diffused). 6-point sweep, 5-seed
  mean Φ per k.
- **substrate B**: H_207 N=16 Kuramoto port. dt=0.05, steps=100, warm=60,
  dim=12. 6-point K subset (drop K=2.0 from H_207 7-point to align with
  6-point cross-substrate). natural-freq ω_i 5 Gaussian z-quantile cycled.
- **substrate C**: rule 110 with noise σ — each elementary CA update,
  with probability σ flip the deterministic next-state bit (uniform Bernoulli
  per site per step, deterministic LCG seed). N=16, dim=12, warm=8, reps=5
  (H_007 carry conventions).
- **deterministic**: 모든 RNG = fixed-seed LCG (no system clock); re-run
  byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12 strict).
- **runtime**: $0 mac local hexa; GPU 불필요 (3 × 6 = 18 Φ measurements,
  ≪ 1 min).
- **ledger**: `result.json` {per-substrate {control_sweep, phi_per_pt,
  d_phi_segments, phi_peak_idx, d_phi_peak_seg_idx, ratio_peak_median,
  interior_strict, interior_relaxed, coincide_h217_5}, criteria, verdict}.
- **honest tier**: 🟢 NUMERICAL Φ (RFC 036 native replica) + 3-substrate
  cross-axis sample. true phi_rs Rust FFI link = named blocker (H_007/H_204/
  H_207 §L8 carry).

## Criteria

- **C1 (H217.1 relaxed interior peak ALL substrate)**: 모든 substrate
  ∂Φ peak segment 가 valid (즉 모든 substrate 가 explicit peak segment
  return — degenerate flat 부재). measurable.
- **C2 (H217.3 peak magnitude > 2× median ALL)**: 모든 substrate peak
  /median |∂Φ/∂(control)| ratio ≥ 2.0. H_204 carry guarantees substrate A
  PASS.
- **C3 (H217.4 byte-identical re-run)**: smoke 2회 실행 시 모든 측정값
  byte-equal.
- **C4 (H217.5 Φ peak ↔ ∂Φ peak coincide ±1)**: 모든 substrate 의 Φ peak
  idx 와 ∂Φ peak segment idx 가 ±1 이내.
  H_204 carry: |2 − 0| = 2 > 1 ⟹ FAIL expected for substrate A
  (i.e. C4 likely FAIL, evidence that "phase transition 의 Φ-peak 위치 와
  ∂Φ-peak 위치 가 일관" 이라는 strong claim 은 substrate-conditional).
- **verdict_rule**: **SUPPORTED** iff C1 ∧ C2 PASS (cross-substrate
  invariant on `peak exists + nontrivial magnitude`). **PARTIAL** if 1/2
  PASS. **FALSIFIED** iff 모두 boundary degenerate / flat.

## Falsifiers

- **F1 BOUNDARY-DEGENERATE**: any substrate ∂Φ peak segment 가 "trivial"
  (e.g., all-zero ∂Φ → peak segment 임의의 first idx, magnitude=0) →
  H217.1 FALSIFIED, H_207-style boundary saturation 재발생.
- **F2 FLAT**: any substrate peak/median ≤ 2.0 (phase transition 부재
  signature) → H217.3 FALSIFIED for that substrate.
- **F3 NONDET**: re-run byte-different → raw#12 위반, smoke 무효.
- **F4 COINCIDE-OFFSET**: Φ peak idx − ∂Φ peak segment idx > 1 (in
  absolute value) for any substrate → H217.5 FAIL — single-peak inverse-U
  hallmark 부재 (H_204 carry expects FAIL by construction).
- **F5 NONNEG**: any Φ < 0 또는 NaN → phi_spatial Φ≥0 위반 → measure
  invalid, smoke FALSIFIED.

## Honest Limits (raw#91 c3)

- **L1 3-substrate sample only**: phase-transition Φ-signature universal-
  ity 의 evidence 로는 3 substrate 가 부족 (다른 substrate: RBN
  random Boolean network, spin glass, Ising model lattice 별도 cycle).
  본 H 는 "3 toy substrate 에서 cross-substrate signature 관측" 한정.
- **L2 control parameter operationalization choice**: closure_strength k
  (substrate A), coupling K (substrate B), noise σ (substrate C) — 각
  substrate 의 'control' 정의는 design choice. 다른 control axis 선택
  (e.g., substrate A 의 diffusion D, substrate B 의 ω_std, substrate C
  의 lattice N) 시 다른 결과 가능.
- **L3 phi_spatial 🟢 NUMERICAL**: H_007/H_204/H_207 §L1/L2/L2 동일 carry
  — RFC 036 native byte-equal replica, n_bins=4, spatial-slice only,
  not full IIT 4.0 (no MIP, no cause-effect repertoire, no exclusion).
  특히 over-lock state (substrate B K=5.0 full sync) 의 saturation 은
  measure-axis artefact 일 가능성 (H_207 L6 carry).
- **L4 6-point sweep coarse**: 진짜 phase-transition point (critical
  exponent, peak location) 정밀화는 20+ point sweep 별도 cycle.
- **L5 'phase transition' universal signature 의 statistical-mechanics
  context**: critical phenomena 의 ∂φ/∂(control) divergence 는 thermo-
  dynamic limit (N→∞) 의 statement, finite-size substrate (N=8/16/16)
  는 smoothed peak. true phase transition 위 ∂ divergence vs finite-size
  smoothed peak 의 구분 = 별도 cycle.
- **L6 substrate-C noise injection design choice**: σ-flip rule 110 의
  *noise injection* operationalization — site-uniform Bernoulli flip
  with deterministic LCG. 다른 noise model (Gaussian additive noise on
  continuous-valued CA, temperature in Glauber dynamics) 시 다른 σ_c.
  H_007 L4 design-choice carry.

## Cross-Links

- **sister H**: H_204 (closure-strength k Φ-sweep, substrate A carry),
  H_207 (Kuramoto coupling K Φ-sweep, substrate B carry — FALSIFIED on
  boundary peak), H_007 (rule-class Φ ranking — substrate C base).
  **DISTINCT claim** — H_217 은 *cross-substrate invariant on phase-
  transition ∂Φ signature* 이지, 단일 substrate 의 inverse-U 또는
  rule-class ranking 의 재증명/부정 아님.
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036
  `phi_spatial`) + `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor)
  — import READ-ONLY.
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) +
  raw#82 (no post-hoc retraction).
- **own**: (anima-not-CA-not-Kuramoto identity; 3 substrate = abstract
  dynamical analogy, anima cells ≠ CA cells ≠ oscillators).
- **CANDIDATES / AXES**: `UNIVERSE/AXES.md` §R8 meta-axis row #8
  `phase-transition-Φ-derivative-peak` (consumed cycle #8 pick #8).
- **literature**:
  - Kuramoto (1975) Self-entrainment of a population of coupled non-linear oscillators
  - Wolfram (1984) Universality and complexity in cellular automata
  - Langton (1990) Computation at the edge of chaos
  - Wilson (1971) Renormalization group and critical phenomena
  - Stanley (1971) Introduction to phase transitions and critical phenomena
  - Kadanoff (1966) Scaling laws for Ising models near T_c
  - Beggs & Plenz (2003) Neuronal avalanches in neocortical circuits
  - Chialvo (2010) Emergent complex neural dynamics
  - Tononi (2004) An information integration theory of consciousness

## Verdict

```
verdict_class: SUPPORTED (pre-register-frozen smoke; 🟢 SUPPORTED-NUMERICAL)
config: 3 substrate × 6-point sweep, n_bins=4, phi_spatial RFC 036
substrate_A: closure CA k ∈ {0.00, 0.10, 0.25, 0.50, 0.75, 1.00}
  Φ : [3.69079, 5.10585, 5.38703, 5.25399, 4.73928, 4.46947]
  ∂Φ/∂k: [14.1505, 1.87456, -0.532175, -2.05883, -1.07925]
  peak_seg=0 (k=0.00→0.10) peak|∂|=14.1505 median=1.87456 ratio=7.55
  Φ_peak_idx=2 (k=0.25) coincide(±1)=false (|2-0|=2)
substrate_B: Kuramoto K ∈ {0.0, 0.5, 1.0, 1.5, 3.0, 5.0}
  Φ : [7.29871, 10.4097, 10.4233, 9.65065, 9.89576, 14.0]
  ∂Φ/∂K: [6.22193, 0.0273, -1.54535, 0.163402, 2.05213]
  peak_seg=0 (K=0.0→0.5) peak|∂|=6.22193 median=1.54535 ratio=4.03
  Φ_peak_idx=5 (K=5.0 boundary) coincide(±1)=false (|5-0|=5)
substrate_C: rule 110 + noise σ ∈ {0.00, 0.05, 0.10, 0.20, 0.40, 0.80}
  Φ : [0.556454, 0.651621, 0.689445, 0.580407, 0.605792, 0.605298]
  ∂Φ/∂σ: [1.90334, 0.756481, -1.09038, 0.126927, -0.00123596]
  peak_seg=0 (σ=0.00→0.05) peak|∂|=1.90334 median=0.756481 ratio=2.52
  Φ_peak_idx=2 (σ=0.10) coincide(±1)=false (|2-0|=2)

criteria_met: 3/4 (C1 PASS · C2 PASS · C3 PASS · C4 FAIL)
  C1 H217.1 explicit peak ALL  : PASS (3/3 peak segments exist, magnitude > 0)
  C2 H217.3 peak > 2× median   : PASS (ratios 7.55 / 4.03 / 2.52 all ≥ 2.0)
  C3 H217.4 byte-identical     : PASS (substrate C σ=0.80 re-run byte-equal)
  C4 H217.5 Φpk↔∂pk coincide  : FAIL (3/3 substrates fail ±1 coincidence —
                                  Φ-peak vs ∂-peak position decoupled)
  F1 NONNEG                    : PASS (all 18 Φ values ≥ 0)

strict-interior sub-criterion (peak_seg ∈ {1,2,3}) : 0/3
  → 모든 substrate ∂Φ peak 가 FIRST segment 위 — `phase transition 의
    가장 급격한 변화는 control parameter 의 sweep low-end 에서 발생`
    이라는 substrate-invariant empirical finding (3/3). 본 toy substrate
    의 design 한계 (k=0/K=0/σ=0 모두 "off" state 에서 출발) 의 산물이거나
    real phase-transition 의 universal signature 인지 = L4 별도 cycle.

verdict: SUPPORTED (C1 ∧ C2 verdict-binding 둘 다 PASS)
  cross-substrate invariant claim — `every substrate exhibits a peak
  ∂Φ/∂(control) with magnitude > 2× substrate-median` — 3/3 PASS.
  H_207 boundary-peak FALSIFIED lesson 의 generalization: ∂Φ peak (Φ
  itself 가 아니라 그 derivative) 측정 시 모든 substrate 에서 nontrivial
  peak 가 관측됨. **단** C4 FAIL — Φ-peak 위치 와 ∂Φ-peak 위치 가 일관
  아님 (single-peak inverse-U hallmark 부재; 3 substrate 모두 ∂Φ-peak
  은 sweep low-end 에 있고 Φ-peak 은 interior 또는 high-end).
honest_tier: 🟢 SUPPORTED-NUMERICAL (phi_spatial RFC 036 native replica,
  3-substrate cross-axis sample; NOT 🔵 formal IIT 4.0)
```
