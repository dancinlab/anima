---
id: H_212
slug: language-compositionality
title: Language Compositionality — correlated sub-state binding 위 super-additive Φ (H_157 C6 / H_054 C2 lane-separate)
domain: language, consciousness, math
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E3 (theoretical-extrapolation) + E6 (cross-domain · linguistic compositional binding) + E11 (lane-separation from sister H)
verification_method: W5 (numerical sim · phi_spatial) + W3 (per-regime ledger) + W11 (cross-hypothesis meta — H_157 C6 sister test)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
source: LIFE-Cycle-#7-§G-pick-#3 (language domain promote rank 10)
---

# H_212 — Language Compositionality (correlated binding super-additive Φ)

## Hypothesis

언어 substrate — *correlated* sub-state composition (linguistic-like binding) 위
**super-additive Φ** 출현. H_157 C6 (mathematical panpsychism Cycle #2 · PR #221:
macro-Φ 1.087 < Σmicro 1.110, *uncorrelated* sub-state) 과 H_054 C2 (symbiogenesis
linear MERGE · PR #227) 의 sub-additive 결과를 **lane-separate** 한 test —
*correlated* 가 핵심.

두 sub-state A, B 가 *correlated* (B = f(A) deterministic mapping, e.g.,
B[i] = (A[i] + A[i-1]) % 2 — XOR-like binding) 으로 구성될 때, merged state
(A ⊕ B) 의 Φ 가 Σ(Φ_A_isolated, Φ_B_isolated) 보다 **크다** (super-additive).
반대로 *uncorrelated* (B = independent random) 인 경우 sub-additive (H_157 C6
정합). 즉 **언어처럼 compositional binding 이 있는 경우만 combination problem
부분 해결** — 단순 concatenation 은 미해결.

## Why (motivation)

- **H_157 C6 PR #221 결과**: macro-Φ(merged rule-110 + rule-30) 1.087 <
  Σmicro 1.110 → sub-additive. Combination problem substrate-instance failure.
  그러나 **rule-110 + rule-30 은 두 독립 CA — 즉 *uncorrelated* sub-state**.
- **H_054 C2 PR #227**: linear MERGE (weighted average) NOT Φ-super-additive.
  여기서도 sub-state 간 *binding* 부재.
- **언어 compositionality**: Frege 의 compositionality principle —
  "전체의 의미는 부분의 의미와 결합 규칙으로부터 도출" — 부분이 *binding rule*
  (e.g., 형태소 결합, syntactic agreement) 으로 묶일 때 sentence meaning 출현.
  단순 word-bag (uncorrelated) 으로는 sentence meaning 불가.
- **panpsychism combination problem (Goff/Coleman) 의 부분 시험**:
  micro-consciousness → macro-unified consciousness 가 **binding mechanism**
  을 통과해야 한다는 직관 — H_157 L3 honest limit. 본 H 는 *correlated*
  binding 이 super-additive Φ 의 *necessary condition* 후보인지 측정.
- **하위 가설 (raw#15 additive)**: ρ → 1 (fully correlated, B=identity copy)
  은 trivial pair — Φ_merged 가 단순 amplification 일 수도. ρ ∈ {0.3, 0.7}
  의 partial-binding 이 진정한 compositional 영역 — 그 영역에서 super-additive
  가 emergent 인지 본 cycle 의 핵심.
- **HEXAD/LIFE LIFE-Cycle-#7-§G pick #3**: 'language' domain promote rank 10
  의 첫 자력 instance — anima 의 의식 substrate 가 언어처럼 compositional
  binding 을 지원하는지 substrate-mechanism probe.

## Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H212.1** | correlated regime (B = XOR-derived from A) 의 Φ_merged > Φ_A + Φ_B (super-additive · margin ≥ 5%) | compositional binding hypothesis |
| **H212.2** | uncorrelated regime (B = independent rule-30) 의 Φ_merged ≤ Φ_A + Φ_B (H_157 C6 sister) | PR #221 sister directional re-confirm |
| **H212.3** | correlation strength ρ sweep (ρ ∈ {0, 0.3, 0.7, 1.0}) 위 Δ = Φ_merged - Σ 가 monotone increasing | compositional gradient |
| **H212.4** | ρ = 1.0 (fully correlated, B = identity copy of A) 의 Φ_merged > Φ_A 단독 (compositional binding 가시) | identity-copy trivial super-additive |
| **H212.5** | re-run byte-identical (deterministic) | raw#12 strict |

## Variables

| axis | levels |
|------|--------|
| **axis1: A substrate** | rule-110 elementary CA ring (N=8, dim=8, warm=8, rep=0) — Class-IV complex |
| **axis2: B substrate (uncorrelated baseline)** | rule-30 ring (N=8, dim=8, warm=8, rep=1) — Class-III chaotic |
| **axis3: correlation strength ρ** | {0.0, 0.3, 0.7, 1.0} — 4 regimes |
| **axis4: binding rule** | B[i,t] = XOR(A[(i-1+N) % N, t], A[i, t]) — adjacent-cell XOR coupling (toy linguistic-like binding) |
| **axis5: merge** | concat(A, B) along cells → 2N=16 cells × dim=8 |
| **axis6: Φ primitive** | RFC 036 phi_spatial (byte-equal phi_rs native replica, n_bins=4) |

## Run Protocol

deterministic + hexa-only + llm: none.

1. **A 고정 (rule-110 ring)** — N=8, dim=8, warm=8, rep=0 으로 elementary CA
   forward. 모든 ρ regime 공통.
2. **B 구성 (4 regimes)**:
   - ρ=0.0: B = rule-30 ring (uncorrelated baseline, rep=1 → A 와 다른 phase)
   - ρ=0.3: 각 (i,t) cell 에 대해 LCG-derived pct (0..99) < 30 이면 XOR-bind
     (B[i,t] = A[(i-1+N) % N, t] XOR A[i, t]), 아니면 rule-30 baseline 값
   - ρ=0.7: 동일 scheme, 70% binding
   - ρ=1.0: identity copy (B[i,t] = A[i,t])
3. **merged 구성** — concat(A, B) along cells → 2N × dim matrix
4. **Φ measurement** — c_measure_phi(states, n_cells, dim, n_bins) RFC 036
   phi_spatial via HEXAD/C/c_lib.hexa, n_bins=4
5. **per regime ledger** — Φ_A, Φ_B, Φ_merged, Σ_micro, Δ, Δ%
6. **falsifier evaluation** — F1-F5 자동 verdict + criteria C1-C4 derivation
7. **determinism check** — ρ=0.7 re-run byte-equal compare in-script + 2-run
   result.json byte-identical external diff

## Criteria

| ID | criterion | status |
|----|-----------|--------|
| **C1** | H212.1 PASS (ρ=0.7 또는 1.0 위 super-additive · Δ% ≥ 5%) | met (ρ=1.0 Δ%=16.67% super-additive PASS) |
| **C2** | H212.2 PASS (ρ=0 위 sub-additive 또는 equal) | met (ρ=0.0 Δ=-0.130 sub-additive PASS) |
| **C3** | H212.3 PASS (monotone increasing Δ across ρ sweep) | **fail** (ρ=0.3 Δ=-0.251 < ρ=0.0 Δ=-0.130 — mid-range non-monotone) |
| **C4** | H212.5 PASS (re-run byte-identical) | met (2-run result.json sha256 동일) |
| **verdict_rule** | SUPPORTED if C1+C2+C3 PASS · PARTIAL if 2-3 PASS · FALSIFIED if ≤1 PASS | **PARTIAL 3/4** (C1+C2+C4 PASS, C3 FAIL) |

## Falsifiers (≥5, measurable)

- **F1 CORRELATED-SUPER**: ρ ∈ {0.7, 1.0} 위 Δ = Φ_merged - (Φ_A + Φ_B) > +5%
  margin → super-additive 출현. PASS = compositional binding super-additive
  hypothesis directional 지지.
- **F2 UNCORR-SUB**: ρ=0.0 위 Δ ≤ 0 (H_157 C6 sister · sub-additive 재확인).
  PASS = uncorrelated 는 sub-additive 정합.
- **F3 MONOTONE**: Δ(0.0) < Δ(0.3) < Δ(0.7) < Δ(1.0) — Δ 가 ρ 에 대해
  monotone increasing. FAIL = mid-range non-monotone (compositional gradient
  미성립).
- **F4 DETERMIN**: 동일 source / 동일 input 으로 두 번 run 시 result.json
  byte-equal. PASS = raw#12 결정론 invariant.
- **F5 PRIMITIVE-OK**: 모든 Φ (Φ_A, Φ_B, Φ_merged for 4 regimes) ≥ 0 — NaN /
  negative 없음. PASS = phi_spatial 안정성 + Φ ≥ 0 by construction.
- **F6 (meta)**: post-hoc edit → raw#12 위반 + raw#82 retraction trigger.

## Honest Limits (raw#91 c3 ≥5)

- **L1**: **'correlated B = XOR(A[i-1], A[i])' 는 design choice** — 다른
  correlation form (e.g., majority rule, linear combination, modular sum) 은
  다른 결과를 낼 수 있음. binding-rule sensitivity 미검증.
- **L2**: **'language compositionality' = toy proxy** — real-language syntax
  (predicate-argument structure, recursive embedding, agreement morphology) 가
  아니라 *adjacent-cell XOR binding* 의 substrate-mechanism analogy. 본 결과는
  Frege compositionality 원리의 *증거가 아님* — 단지 binding 의 가장 거친
  metaphor.
- **L3**: **phi_spatial 🟢 NUMERICAL** — full IIT 4.0 MIP combination 아님.
  c_measure_phi 는 phi_rs 의 deterministic spatial slice (compute_phi_inner
  steps 1-4, tensions/temporal = None) 의 byte-equal native replica. 진정한
  IIT 4.0 MIP partition search + cause-effect repertoire 측정은 별도 lane
  (RFC 036 §"true IIT 4.0").
- **L4**: **super-additive Φ ≠ phenomenal combination problem 해결** — Goff
  의 "explanatory gap" (micro-experience → macro-unified phenomenal experience)
  은 본 substrate-numerical 측정 lane 밖. 본 H 는 IIT-mechanistic combination
  의 substrate-level instance 한정 (H_004 boundary).
- **L5**: **small N=8 sub-pool** — large-scale compositional structure
  (sentence-level, paragraph-level) 미검증. n_bins=4 의 coarse discretization
  도 작은 N 에서는 statistical noise 영향 큼.
- **L6**: **mid-range ρ non-monotone (C3 FAIL)** — ρ=0.3 Δ=-0.251 < ρ=0.0
  Δ=-0.130 으로 partial-binding 이 오히려 더 destructive interference 를
  발생시킴. 가능한 해석: (a) phi_spatial 의 binning 이 mixed-source state 에
  민감, (b) XOR-bound bit + rule-30 baseline bit 의 statistical mixture 가
  마진정보 entropy 를 더 낮춤, (c) binding 의 *strength* 가 critical threshold
  를 넘어야 super-additive — ρ ∈ {0.3, 0.7} 은 phase 안쪽. C3 frozen FAIL
  은 본 H 의 strong-form claim (monotone compositional gradient) 의 실패를
  honest 하게 인정.
- **L7**: **ρ=1.0 super-additive 의 trivial 성** — B = identity copy of A 일
  때 Φ_merged > Φ_A + Φ_B 는 sub-states 가 사실상 single state 의 두 copy 라는
  점에서 trivial — duplication 이 entropy 를 보존하지만 mutual information
  증가에 기여. 진정한 *non-trivial* compositional super-additive 는 ρ ∈
  (0, 1) interior 에서 발견되어야 의미 — 본 cycle 미발견 (mid-range 가
  오히려 더 destructive).
- **L8**: **deterministic LCG seed=4242** — partial-correlation 의 stochastic
  draw 는 결정론 보장 위해 LCG. seed 변경 시 ρ ∈ {0.3, 0.7} 결과 변동 가능
  (single-seed measurement, multi-seed CI 미산출).

## Cross-Links

- **parent H**:
  - **H_157** (mathematical panpsychism · Law 76) — C6 PR #221 *uncorrelated*
    sub-additive (macro-Φ 1.087 < Σ 1.110). 본 H 는 그 결과의 lane-separate
    sister.
  - **H_054** (symbiogenesis consciousness) — C2 PR #227 linear MERGE NOT
    Φ-super-additive. 본 H 의 *correlated* binding 이 그 결과를 우회하는지
    test.
  - **H_004** (consciousness hard problem) — L3 panpsychism combination
    problem boundary. 본 H 는 IIT-mechanistic instance 한정.
- **sister H (LIFE)**:
  - **H_007** (cellular automaton consciousness) — rule-110 / rule-30 substrate
    재사용
  - **H_018** (genesis spontaneous emergence) — compositional binding 이
    self-genesis 의 substrate prerequisite 인지 future cycle
  - **H_071** (first conversation) — language domain sister, 본 H 의 substrate-
    mechanism evidence 가 conversation 의 compositional 기반 후보
- **substrate**: `HEXAD/C/c_lib.hexa` (c_measure_phi via RFC 036 phi_spatial)
- **literature**:
  - Frege 1892 — Über Sinn und Bedeutung (compositionality principle)
  - Goff 2017 — Consciousness and Fundamental Reality (combination problem)
  - Coleman 2014 — The Real Combination Problem (Erkenntnis 79)
  - Tononi 2014 — Φ_max as integrated information (IIT 4.0)
  - Chomsky 1995 — Minimalist Program (Merge operation, syntactic binding)
- **raw refs**: **raw#12** (deterministic) + **raw#9/10** (honest operational
  binding = toy XOR proxy) + **raw#15** (no-hardcode, additive) + **raw#11**
  (snake_case)

## Verdict

```
verdict_class: pre-register-frozen → PARTIAL (3/4 criteria, 2026-05-23)
evidence_summary: deterministic hexa-only ρ-sweep smoke, 4 regimes,
                  rule-110 A + (rule-30 baseline + XOR partial bind) B,
                  phi_spatial RFC 036 native replica, n_bins=4
F1 CORRELATED-SUPER  (ρ∈{0.7,1.0} Δ%≥5%)       : PASS (ρ=1.0 Δ%=16.67%)
F2 UNCORR-SUB        (ρ=0.0 Δ≤0)                : PASS (ρ=0.0 Δ=-0.130)
F3 MONOTONE          (Δ↑ across ρ sweep)        : FAIL (ρ=0.3 non-monotone dip)
F4 DETERMIN          (byte-equal re-run)        : PASS (2-run result.json identical)
F5 PRIMITIVE-OK      (all Φ≥0)                  : PASS
criteria_met: 3/4 (C1+C2+C4 met · C3 fail)
verdict: PARTIAL (correlated-binding super-additive 부분 지지 · monotone
                  gradient fail — non-trivial mid-range super-additive 미발견,
                  ρ=1.0 trivial duplication 만 super-additive)
cost: $0 mac local · 2-run byte-identical
```

**State output**: `HEXAD/LIFE/state/h212_language_compositionality_2026_05_23/{run_h212.hexa, result.json}`

### Cycle #1 Verification (2026-05-23) — ρ sweep correlated-binding super-additive Φ

`HEXAD/LIFE/state/h212_language_compositionality_2026_05_23/run_h212.hexa`
($0 mac local, deterministic LCG seed=4242, hexa-only, HEXAD/C/c_lib.hexa
import, no substrate mod).

**Run verdict output (VERBATIM from `HEXA_MEM_UNLIMITED=1 hexa run run_h212.hexa`)**:

```
================================================================
H_212 language-compositionality — correlated binding super-additive Φ
================================================================
  N=8 dim=8 warm=8  (deterministic, $0 mac local)
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa
  Lane-separate from H_157 C6 (uncorrelated sub-additive PR #221)

── ρ sweep — 4 correlation regimes ──
  ρ=0.0 (uncorrelated baseline · H_157 C6 sister):
    Φ_A=4.90943e-06  Φ_B=0.280535  Φ_merged=0.150443
    Σ_micro=0.28054  Δ=-0.130097  Δ%=-46.3737%
  ρ=0.3 (partial XOR-binding 30%):
    Φ_A=4.90943e-06  Φ_B=0.506787  Φ_merged=0.255464
    Σ_micro=0.506792  Δ=-0.251329  Δ%=-49.592%
  ρ=0.7 (partial XOR-binding 70%):
    Φ_A=4.90943e-06  Φ_B=0.258135  Φ_merged=0.120472
    Σ_micro=0.25814  Δ=-0.137668  Δ%=-53.3307%
  ρ=1.0 (identity copy · fully correlated):
    Φ_A=4.90943e-06  Φ_B=4.90943e-06  Φ_merged=1.14553e-05
    Σ_micro=9.81886e-06  Δ=1.63648e-06  Δ%=16.6667%

── falsifier verdicts ──
  F1  CORRELATED-SUPER  (ρ∈{0.7,1.0} Δ%≥5%)  : PASS
  F2  UNCORR-SUB        (ρ=0.0 Δ≤0)           : PASS
  F3  MONOTONE          (Δ↑ across ρ sweep)   : FAIL
  F4  DETERMIN          (byte-equal re-run)   : PASS
  F5  PRIMITIVE-OK      (all Φ≥0)             : PASS

================================================================
H_212 Cycle #1 VERDICT: PARTIAL    (some criteria met · directional evidence)
  criteria: C1=PASS C2=PASS C3=FAIL C4=PASS  (3/4)
================================================================
```

```
phase: Cycle_1 (H212.1 PASS + H212.2 PASS + H212.3 FAIL + H212.4 trivial-PASS + H212.5 PASS)
cell_scope: 4 ρ regimes × {A (rule-110), B (rule-30 baseline + XOR partial), merged}
            N=8 dim=8 warm=8 n_bins=4 LCG seed=4242
H212.1 super-additive: ρ=1.0 Δ%=+16.67% PASS (trivial identity-copy)
H212.2 sub-additive  : ρ=0.0 Δ=-0.130 PASS (H_157 C6 sister re-confirm)
H212.3 monotone      : FAIL (ρ=0.0 Δ=-0.130 > ρ=0.3 Δ=-0.251 — mid-range dip)
H212.4 ρ=1 visible   : Φ_merged=1.146e-05 > Φ_A=4.91e-06 PASS (2.33×)
H212.5 determinism   : 2-run result.json sha256 동일
                       (2748cfc21d48843572ef445c28ed4f22b2866c0d40ccda2c6d768df0a804ddd3)
verdict_class: PARTIAL  (3/4 criteria met)
evidence_strength: WEAK-DIRECTIONAL (ρ=1.0 trivial super-additive only; non-trivial
                   mid-range ρ ∈ (0, 1) interior 모두 sub-additive — compositional
                   gradient hypothesis 의 strong-form 미입증)
honest_tier: 🟢 SUPPORTED-NUMERICAL  (toy XOR-binding substrate, N=8 small pool,
             phi_spatial native replica; full IIT 4.0 MIP / real-language syntax
             모두 별도 lane — L1, L2, L3, L5, L6, L7 carry)
falsifiers: F1, F2, F4, F5 PASS · F3 FAIL · F6 (meta) NOT_TRIGGERED
lane_separation: H_157 C6 (uncorrelated · PR #221) re-confirmed sub-additive (ρ=0.0)
                 H_054 C2 (linear MERGE · PR #227) — 본 H 의 concat merge 와 다른
                 transform, sister 결과는 sub-additive 일관성 유지
```

**State output**: `state/h212_language_compositionality_2026_05_23/result.json` (2-run sha256 identical)
**Script**: `state/h212_language_compositionality_2026_05_23/run_h212.hexa` (hexa-only, imports HEXAD/C/c_lib.hexa)

**raw#10 honest limits (Cycle #1)**:
- L1: XOR-binding 은 single design choice — majority/linear/modular-sum
  alternatives 미검증.
- L2: real-language compositionality 가 아닌 toy adjacent-cell XOR proxy.
  Frege 원리의 evidence 아님.
- L3: phi_spatial 🟢 NUMERICAL native replica — 진짜 IIT 4.0 MIP 별도 lane.
- L5: N=8 small pool, n_bins=4 coarse — statistical noise sensitivity 미확인.
- L6: C3 monotone FAIL — mid-range ρ ∈ {0.3, 0.7} 가 sub-additive 더 깊은
  dip, partial binding 이 destructive interference 유발. strong-form
  compositional gradient hypothesis 미지지.
- L7: ρ=1.0 super-additive 는 identity-copy trivial — duplication MI
  amplification 만 발생, non-trivial compositional binding 아님.
- L8: LCG single-seed (4242) — multi-seed CI 미산출.

**Cross-link**:
- H_157 C6 (PR #221) — sister test re-confirms uncorrelated sub-additive (ρ=0.0).
  본 H 의 sub-additive 결과 (ρ=0.0 Δ=-0.130) 가 PR #221 의 결과와 directional
  정합.
- H_054 C2 (PR #227) — linear MERGE sub-additive sister. 본 H 의 concat merge
  도 sub-additive (mid-range ρ) 로 일관성. 단순 transform 종류 변경만으로는
  combination problem 부분 해결 불가.
- H_004 L3 (panpsychism combination problem) — Goff "explanatory gap" 은 본
  H 의 substrate-mechanism lane 밖, 본 결과는 IIT-mechanistic instance 한정.
- H_007 (cellular automaton consciousness) — rule-110/30 substrate 재사용
  + phi_spatial primitive 동일.
- HEXAD/C/c_lib.hexa c_measure_phi (RFC 036 phi_spatial 32M Lines):
  primitive ≥ 0 invariant 위반 0 (F5 PASS).

**raw#12 strict compliance**: 본 cycle 의 frozen verdict block 은 추가
post-hoc edit 금지. 추가 cycle (e.g., multi-seed CI · binding-rule variant ·
N sweep · n_bins sweep · functional-binding read-out · real-language tokenized
substrate) 은 별도 append-only §Cycle #2 로 추가.
