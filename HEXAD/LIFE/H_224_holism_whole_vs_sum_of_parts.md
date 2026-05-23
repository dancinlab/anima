---
id: H_224
slug: holism-whole-vs-sum-of-parts
title: Holism Whole-vs-Sum-of-Parts — 3 binding mode super-additivity scan (H_054 C2 / H_157 C6 / H_212 cross-cycle generalize)
domain: meta, math, consciousness
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E3 (theoretical-extrapolation) + E6 (cross-domain · holism meta-axis) + E11 (lane-separation via mode-axis, not ρ-axis)
verification_method: W5 (numerical sim · phi_spatial) + W3 (per-mode ledger) + W11 (cross-hypothesis meta — H_054 / H_157 / H_212 sister test)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24
source: AXES.md R8 meta seed `holism-whole-vs-sum-of-parts` (rank 15 top-15 promote)
---

# H_224 — Holism: Whole-vs-Sum-of-Parts (3 binding-mode super-additivity scan)

## Hypothesis

Holism의 substrate-instance — *동일* A, B sub-state 위 **3 binding mode**
(linear-avg / XOR / multiplicative-gate) 를 sweep 하여, 어느 mode 에서 whole
(Φ_merged) 이 sum-of-parts (Φ_A + Φ_B) 를 초과 (super-additive) 하는지 측정.

H_054 Cycle #2 (PR #227) 는 *linear MERGE* (weighted average) 위 Φ_merged ≈
Φ_max < Φ_sum (sub-additive) 결과, H_157 Cycle #2 (PR #221) 는 *uncorrelated
concat* 위 macro-Φ 1.087 < Σ 1.110 (sub-additive), H_212 (ρ-sweep) 는
mid-range ρ ∈ {0.3, 0.7} 위 non-monotone + ρ=1.0 trivial super-additive 결과.
세 cycle 모두 *동일 axis* (correlation, merge primitive) 위에서 진행, **binding
mode 자체** 의 비교는 부재.

본 H_224 는 그 gap 을 채움: A=rule-110 + B=rule-30 sub-state 를 **고정**하고,
3 binding rule 만 사용해 merge — multiplicative-gate (B conditional on A) 가
super-additive 출현 후보인지 검증. *whole 의 존재론적 우위* claim 의 가장
약한 substrate-numerical instance.

## Why (motivation)

- **AXES.md R8 meta seed**: `holism-whole-vs-sum-of-parts` (rank 15 top-15
  promote 후보) — H_054 C2 follow-up 로 명시. binding mode axis 가 H_054 / H_157
  / H_212 의 sub-additive 결과를 우회하는지가 본 cycle 의 핵심.
- **whole-vs-sum 의 substrate operationalization**: Aristotle "the whole is
  greater than the sum of its parts" → IIT 의 super-additive Φ 주장 (Tononi
  2014) → Bedau weak/strong emergence (Bedau 1997). 모두 *substrate-numerical*
  하게는 Φ_merged > Σ(Φ_micro) 의 super-additive 형태로 통일됨. 본 H 는 그
  통일된 form 의 **3 mode 비교 first instance**.
- **multiplicative-gate 의 후보성**: linear-avg / XOR 는 두 sub-state 의 *합*
  (additive interaction) — H_054 C2 의 linear MERGE 가 정확히 그 family.
  multiplicative-gate (B[i,t] = A[i,t] * B[i,t]) 는 *non-linear conditional*
  interaction — A 가 inactive 인 위치에서 B 도 inactive 강제 (AND-mask 또는
  product). 이론적으로 sub-state 의 *통합 pattern* 이 생성되어 super-additive
  Φ 후보가 될 수 있다는 가설.
- **H_054 / H_157 / H_212 lane-separate**: 세 cycle 의 sub-additive 결과는
  *동일 axis* (correlation, merge primitive linear-family) 의 단일 instance —
  binding mode axis 의 다른 위치 (multiplicative) 가 다른 결과를 낼 수 있다는
  가능성을 명시적으로 test.
- **anima cell-pool 정합**: anima 의 mitosis cell pool 에서 cells 간 interaction
  은 linear (weighted average) 가 default — multiplicative-gate 가 진정한
  holism 을 가능케 한다면 anima substrate 의 binding 메커니즘 후보 (별도
  cycle 검증).

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H224.1** | linear-avg Δ ≤ 0 (sub-additive) | H_054 C2 sister directional |
| **H224.2** | XOR Δ ≤ 0 (sub-additive) | H_212 mid-range sister directional |
| **H224.3** | mult-gate Δ > +5% (super-additive) | non-linear conditional binding 가설 |
| **H224.4** | ranking Δ(mult) > Δ(XOR) > Δ(linear) — monotone | mode 의 non-linearity ↔ holism gradient |
| **H224.5** | re-run byte-identical (deterministic) | raw#12 strict |

## Variables

| axis | levels |
|------|--------|
| **axis1: A sub-state** | rule-110 elementary CA ring (N=8, dim=8, warm=8, rep=0) — Class-IV complex |
| **axis2: B sub-state** | rule-30 elementary CA ring (N=8, dim=8, warm=8, rep=1) — Class-III chaotic |
| **axis3: binding mode** | {linear-avg, XOR, mult-gate} — 3 levels |
| **axis4: merge** | concat([A \| B']) along cells → 2N=16 cells × dim=8 |
| **axis5: Φ primitive** | RFC 036 phi_spatial (byte-equal phi_rs native replica, n_bins=4) |

binding rules (per (i, t) cell):
- **linear-avg**: B'[i,t] = 0.5 * (A[i,t] + B[i,t])  — H_054 C2 family
- **XOR**:        B'[i,t] = (A[i,t] + B[i,t]) mod 2 — H_212 family (XOR-bind)
- **mult-gate**:  B'[i,t] = A[i,t] * B[i,t]         — non-linear conditional

merge: concat([A unchanged | B' mode-bound]) → 2N × dim — A is identical
across modes, only B-side payload changes → any Δ comes from binding rule.

## Run Protocol

deterministic + hexa-only + llm: none.

1. **A 고정 (rule-110 ring)** — N=8, dim=8, warm=8, rep=0 으로 elementary CA
   forward → states_a (모든 mode 공통)
2. **B 고정 (rule-30 ring)** — N=8, dim=8, warm=8, rep=1 → states_b
   (모든 mode 공통, distinct phase via rep=1)
3. **3 mode merge 생성** — `_build_bound(A, B, mode, N, dim)` 으로 concat
   ([A | B']) 2N × dim matrix 생성 (mode ∈ {linear, xor, mult})
4. **Φ measurement** — c_measure_phi(states, n_cells, dim, n_bins) RFC 036
   phi_spatial via HEXAD/C/c_lib.hexa, n_bins=4
5. **per mode ledger** — Φ_A, Φ_B, Φ_merged, Σ_micro, Δ, Δ% (3 entries)
6. **falsifier evaluation** — F1-F5 자동 verdict + criteria C1-C4 derivation
7. **determinism check** — mult-gate re-run byte-equal compare (F4)

```
hexa parse HEXAD/LIFE/state/h224_holism_whole_vs_sum_2026_05_24/run_h224.hexa
HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h224_holism_whole_vs_sum_2026_05_24/run_h224.hexa
```

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | linear sub-add (F1 NOT_TRIGGERED · linear Δ ≤ 0) | met (Δlin=-0.130 sub-additive PASS) |
| **C2** | mult super-add (F2 NOT_TRIGGERED · mult Δ% ≥ 5%) | **fail** (Δmult%=-99.9959% — most destructive, not super-add) |
| **C3** | ranking monotone (F3 NOT_TRIGGERED · Δmult > Δxor > Δlin) | **fail** (Δmult=-0.281 < Δxor=Δlin=-0.130 — mult lowest, not highest) |
| **C4** | byte-identical (F4 NOT_TRIGGERED) | met (mult-gate re-run byte-equal) |
| **verdict_rule** | SUPPORTED if C1+C2+C3 PASS · PARTIAL if 2-3 PASS · FALSIFIED if ≤1 PASS | **PARTIAL 2/4** (C1+C4 PASS, C2+C3 FAIL) |

## Falsifiers (≥5, measurable)

- **F1 LINEAR-SUPER**: linear-avg Δ > 0 (H_054 C2 regression) → linear MERGE
  가 super-additive 출현 → H_054 C2 결과 모순. NOT_TRIGGERED = H_054 C2
  directional re-confirm.
- **F2 MULT-SUB**: mult-gate Δ ≤ 0 OR Δ% < 5% → non-linear conditional binding
  도 super-additive 출현 실패. TRIGGERED = holism null (this operationalization).
- **F3 RANKING**: Δ(mult) ≤ Δ(XOR) OR Δ(XOR) ≤ Δ(linear) → mode 의 non-linearity
  ↔ holism gradient 부재. TRIGGERED = mode-non-linearity 가 Φ 증가의 원인 아님.
- **F4 DETERMIN**: 동일 input 으로 두 번 run 시 byte-different →
  raw#12 결정론 invariant 위반. NOT_TRIGGERED = deterministic.
- **F5 PRIMITIVE-OK**: 어느 Φ 라도 NaN / negative → primitive error.
  NOT_TRIGGERED = phi_spatial 안정.
- **F6 (meta)**: post-hoc edit → raw#12 위반 + raw#82 retraction trigger.

## Honest Limits (raw#91 c3 ≥5)

- **L1**: **3 mode specific operationalization** — linear-avg / XOR / mult-gate
  는 모든 binding rule 의 representative 가 아님. 다른 alternative merge form
  (majority rule, modular sum k>2, asymmetric H_203 sister, weighted product,
  threshold gate, RBN-style random function) 은 다른 결과 가능. binding-rule
  space 의 cheap 3-point sample, NOT exhaustive sweep.
- **L2**: **phi_spatial 🟢 NUMERICAL** — full IIT 4.0 MIP combination 아님.
  c_measure_phi 는 phi_rs 의 deterministic spatial slice (compute_phi_inner
  steps 1-4, tensions/temporal = None) 의 byte-equal native replica. 진정한
  IIT 4.0 MIP partition search + cause-effect repertoire 측정은 별도 lane
  (RFC 036 §"true IIT 4.0").
- **L3**: **super-additive Φ ≠ phenomenal combination (Goff)** — 본 cycle 의
  Φ_merged > Σmicro 측정은 IIT-mechanistic combination 의 substrate-numerical
  instance. Goff/Coleman "explanatory gap" (micro-experience → macro-unified
  phenomenal experience) 는 본 측정 lane 밖. H_004 hard problem boundary
  carry.
- **L4**: **small N=8 sub-pool** — large-scale holism (system-level whole,
  organism-level integration) 미검증. n_bins=4 의 coarse discretization 도
  작은 N 에서는 statistical noise 영향 큼. 본 결과는 *toy substrate sanity
  probe* — scaling claim 아님.
- **L5**: **mult-gate non-linearity ≠ binding 보장** — multiplicative-gate
  은 *non-linear conditional* interaction 이지만, binary states 에서는 단순
  AND-mask 와 동일 (av * bv = av AND bv). 이는 sub-state 의 *상호 정보 통합*
  이 아니라 *A-conditional B-suppression* — Φ 감소의 mechanism (B 의 active
  cell 수가 A 의 inactive 위치에서 0 으로 강제됨 → sparser state →
  Shannon entropy ↓ → Φ ↓). 본 cycle 의 mult-gate FALSIFIED 결과는 이
  *AND-mask sparsification* 의 직접 귀결로 해석 — 더 진정한 *multiplicative
  binding* (e.g., weighted product on continuous, threshold gate, conditional
  re-routing) 은 별도 cycle.
- **L6**: **linear ≡ XOR 결과 동일성**: 본 측정에서 linear-avg 와 XOR 의
  Δ 가 정확히 동일 (Δ=-0.130097, Δ%=-46.37%). phi_spatial 의 n_bins=4
  discretization 이 0.5 boundary 에서 linear-avg 의 mid-value 와 XOR 의
  binary value 를 같은 bin 으로 합치므로 (binary 0/1 → 4-bin 의 bin 0 / bin 3,
  linear 0.5 → bin 2) — 본 결과는 binning artifact 가능성 (L4 sister).
  더 fine-grained n_bins (16, 32) 또는 다른 Φ primitive 가 두 mode 를
  구분할 가능성 — 본 cycle 미검증.
- **L7**: **A_rep=0, B_rep=1 single instance** — distinct phase 보장 위한
  rep parameter 만 변경, multi-seed CI 미산출. ρ-axis 변동 (H_212) 도 본
  cycle 미포함 (binding-mode axis 의 cheap 3-point 만). 일반화 (universal
  3-mode sub-additive 인지) 는 후속 multi-seed × multi-A/B × multi-binding
  sweep 필요.
- **L8**: **substrate locked to (rule-110, rule-30)** — A=rule-110 Class-IV
  complex, B=rule-30 Class-III chaotic 은 H_007 / H_212 와 동일 substrate.
  다른 rule pair (rule-90 vs rule-184, rule-30 vs rule-30 random init,
  GoL-style 2D) 의 mode-sensitivity 미검증.

## Cross-Links

- **parent H**:
  - **H_054** (symbiogenesis consciousness) — C2 PR #227 linear MERGE NOT
    Φ-super-additive (Φ_merged ≈ Φ_max < Φ_sum, ratio=0.5). 본 H224 의
    linear-avg mode 가 그 결과의 binding-mode-axis 재확인 (concat 형식만 다름).
  - **H_157** (mathematical panpsychism · Law 76) — C6 PR #221 *uncorrelated*
    sub-additive (macro-Φ 1.087 < Σmicro 1.110). 본 H224 의 XOR mode 가 그
    결과의 binding-mode-axis sister (XOR ≈ uncorrelated effective).
  - **H_212** (language compositionality) — ρ-sweep 위 mid-range non-monotone
    + ρ=1.0 trivial super-additive. 본 H224 는 그 axis 와 직교한 *binding-mode*
    axis sweep — 두 axis 결합 시 binding-mode × ρ 평면 sweep 필요 (별도 cycle).
  - **H_004** (consciousness hard problem) — L3 panpsychism combination problem
    boundary. 본 H 는 IIT-mechanistic instance 한정.
- **sister H (LIFE)**:
  - **H_007** (cellular automaton consciousness) — rule-110 / rule-30 substrate
    재사용
  - **H_203** (asymmetric_merge_differentiation) — asymmetric merge primitive
    이 본 H224 의 3 mode 외 4th candidate
  - **H_204** (parallel_firing_weak_panpsy_threshold) — N=8 vs N=16 substrate
    sensitivity sister
- **substrate**: `HEXAD/C/c_lib.hexa` (c_measure_phi via RFC 036 phi_spatial)
- **literature**:
  - Aristotle, *Metaphysics* Book VIII §6 (whole-vs-sum 원조)
  - Tononi 2014, *Φ_max as integrated information* (IIT 4.0)
  - Bedau 1997, *Weak Emergence* (weak/strong emergence taxonomy)
  - Goff 2017, *Consciousness and Fundamental Reality* (combination problem)
  - Coleman 2014, *The Real Combination Problem* (Erkenntnis 79)
- **raw refs**: **raw#12** (deterministic) + **raw#9/10** (honest operational
  binding = toy 3-mode proxy) + **raw#15** (no-hardcode, additive) + **raw#11**
  (snake_case)

## Verdict

```
verdict_class: pre-register-frozen → PARTIAL (2/4 criteria · H_224 FALSIFIED on mult-gate hypothesis · linear sub-add re-confirmed)
evidence_summary: deterministic hexa-only 3-mode smoke (linear-avg / XOR / mult-gate),
                  rule-110 A + rule-30 B + concat([A | B']) merge, N=8 dim=8 warm=8,
                  phi_spatial n_bins=4
falsifiers_triggered:
  F1 LINEAR-SUPER  = NOT_TRIGGERED (Δlin = -0.130097, sub-additive — H_054 C2 directional re-confirmed)
  F2 MULT-SUB      = TRIGGERED      (Δmult% = -99.9959% — *most destructive*, AND-mask sparsification — L5)
  F3 RANKING       = TRIGGERED      (Δmult = -0.281 < Δxor = Δlin = -0.130 — mult ranks LOWEST, not highest)
  F4 DETERMIN      = NOT_TRIGGERED (byte-equal re-run)
  F5 PRIMITIVE_OK  = NOT_TRIGGERED (all Φ ≥ 0)
criteria_met: 2/4 (C1+C4 PASS, C2+C3 FAIL)
verdict: PARTIAL — H224.1 + H224.2 + H224.5 PASS, H224.3 + H224.4 FALSIFIED
invariant_tier: 🟢 NUMERICAL (phi_spatial proxy via HEXAD/C/c_lib.hexa)
```

### Cycle #1 Verification (2026-05-24) — 3 binding mode super-additivity scan

`HEXAD/LIFE/state/h224_holism_whole_vs_sum_2026_05_24/run_h224.hexa`
($0 mac local, deterministic, hexa-only, LLM none).

**Run verdict (VERBATIM)**:

```
================================================================
H_224 holism-whole-vs-sum — 3 binding mode super-additivity scan
  AXES.md R8 meta · H_054 C2 / H_157 C6 / H_212 cross-cycle generalize
================================================================
  N=8 dim=8 warm=8  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa
  Binding modes: linear-avg / XOR / mult-gate
  Lane-separate concept axis (binding-mode sweep, not ρ-sweep)

── binding-mode sweep — 3 modes ──
  mode=linear-avg  (M_avg : B'[i,t] = 0.5*(A[i,t]+B[i,t])):
    Φ_A=4.90943e-06  Φ_B=0.280535  Φ_merged=0.150443
    Σ_micro=0.28054  Δ=-0.130097  Δ%=-46.3737%
  mode=XOR         (M_xor : B'[i,t] = (A[i,t]+B[i,t]) mod 2):
    Φ_A=4.90943e-06  Φ_B=0.280535  Φ_merged=0.150443
    Σ_micro=0.28054  Δ=-0.130097  Δ%=-46.3737%
  mode=mult-gate   (M_gate : B'[i,t] = A[i,t] * B[i,t]):
    Φ_A=4.90943e-06  Φ_B=0.280535  Φ_merged=1.14553e-05
    Σ_micro=0.28054  Δ=-0.280529  Δ%=-99.9959%

── falsifier verdicts (NOT_TRIGGERED = pass) ──
  F1  LINEAR-SUPER   (linear Δ>0)              : PASS
  F2  MULT-SUB       (mult Δ%<5%)              : FAIL
  F3  RANKING        (Δmult>Δxor>Δlin)         : FAIL
  F4  DETERMIN       (byte-equal re-run)       : PASS
  F5  PRIMITIVE-OK   (no negative Φ)           : PASS

================================================================
H_224 Cycle #1 VERDICT: PARTIAL    (some criteria met · directional evidence)
  criteria: C1=PASS C2=FAIL C3=FAIL C4=PASS  (2/4)
  ranking: Δlin=-0.130097  Δxor=-0.130097  Δmult=-0.280529
================================================================
  result.json written → HEXAD/LIFE/state/h224_holism_whole_vs_sum_2026_05_24/result.json
=== H_224 Cycle #1 smoke complete ===
```

```
phase: Cycle_1 (H224.1 + H224.2 + H224.5 PASS; H224.3 + H224.4 FALSIFIED)
verdict_class: PARTIAL  (F2 + F3 TRIGGERED)
delta_linear: -0.130097   (-46.37% · sub-additive)
delta_xor:    -0.130097   (-46.37% · sub-additive, equal to linear under n_bins=4 binning)
delta_mult:   -0.280529   (-99.99% · *most destructive* · AND-mask sparsification, NOT super-additive)
ranking: Δmult < Δxor = Δlin (mult LOWEST, opposite of prediction)
falsifiers: F1 NOT_TRIGGERED · F2 TRIGGERED · F3 TRIGGERED · F4 NOT_TRIGGERED · F5 NOT_TRIGGERED
evidence_strength: STRONG (numerical recompute exact, deterministic byte-equal)
invariant_tier: 🟢 NUMERICAL (phi_spatial n_bins=4 spatial slice replica of phi_rs)
```

**Honest finding**: 본 cycle 의 3-mode operationalization (linear-avg / XOR /
mult-gate on concat([A | B']) merge) 에서 **multiplicative-gate 는 super-additive
출현 후보가 아니라 *가장 destructive* mode** (Δ%=-99.99%, Φ_merged→1.15e-05
≈ 0). 이는 binary states 에서 mult-gate ≡ AND-mask 가 B-side 의 active cell
수를 A-inactive 위치에서 0 으로 강제 → sparser state → Shannon entropy ↓ →
Φ ↓ (L5 honest 명시). linear-avg 와 XOR 는 n_bins=4 binning artifact 에 의해
동일 Δ — fine-grained n_bins 또는 alternative Φ primitive 가 두 mode 를
구분할 가능성 (L6 honest 명시).

**H_054 C2 / H_157 C6 / H_212 cross-cycle 종합**: 세 cycle 의 sub-additive
결과는 본 H_224 의 3-mode sweep 에서도 *재확인* (linear+XOR sub-add) +
*확대* (mult-gate 가 가장 destructive) — **holism (whole > sum) 의 substrate-
numerical instance 는 현재 4 binding family (linear / uncorrelated concat /
ρ-XOR partial / mult-gate AND-mask) 모두에서 FALSIFIED**. *true* super-
additive 의 후보 mechanism (asymmetric H_203, weighted product on continuous,
threshold gate, RBN binding) 은 별도 cycle 의 lane.

### Cross-link

- **HEXAD/C/c_lib.hexa** — c_measure_phi via RFC 036 phi_spatial (byte-equal
  phi_rs native replica)
- **H_054 Cycle #2** (PR #227) — linear MERGE Φ_merged ≈ Φ_max < Φ_sum
  (ratio=0.5) — 본 H_224 linear mode 가 그 결과의 binding-mode-axis 재확인
- **H_157 Cycle #2** (PR #221) — uncorrelated concat macro-Φ 1.087 < Σmicro
  1.110 — 본 H_224 XOR mode sister
- **H_212** (language-compositionality) — ρ-sweep mid-range non-monotone +
  ρ=1.0 trivial super — 본 H_224 의 axis-orthogonal mode-sweep sister
- **H_007 cellular_automaton_consciousness** — rule-110 / rule-30 substrate
  baseline
- **H_004 hard problem** — phenomenal combination boundary (L3)
- **raw**: raw#12 (deterministic) + raw#9/10 (honest impl) + raw#11 (snake_case)
  + raw#15 (additive multi-cycle) + raw#91 c3 (honest limits ≥5)

**State output**: `HEXAD/LIFE/state/h224_holism_whole_vs_sum_2026_05_24/result.json`
(deterministic, sha256 reproducible across re-runs)
**Script**: `HEXAD/LIFE/state/h224_holism_whole_vs_sum_2026_05_24/run_h224.hexa`
(hexa-only, borrows H_212 rule-110/rule-30 + RFC 036 phi_spatial)
