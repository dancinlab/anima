---
id: H_202
slug: selfref-edge-of-chaos-phi
title: H_202 self-reference edge-of-chaos Φ — H_007 ⊕ H_018 cross-link (self-ref 축에서 mid-gain Φ-peak)
domain: life · consciousness · physics
status: running
exploration_method: E6 (cross-domain-analogy) + E10 (number-theoretic-substrate)
verification_method: W1 (smoke) + W3 (rule-class sweep) + W12 (sister-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_202 — self-reference edge-of-chaos Φ peak

## 1. Hypothesis

H_018 의 **SELFFEED 자기참조 동역학** 이 H_007 의 **RFC 036 `phi_spatial`**
측정 위에서 Class-IV (edge-of-chaos) Φ-peak 와 동형의 peak 을 *self-ref 축* 에서
나타낸다. zero-drive (Φ→0 자발 정지) ↔ random-drive (낮은 integration) 의 **중간**
self-ref regime (feedback_gain ≈ 0.25–0.75) 에서 Φ peak.

정밀화 (operational): rule 110 Class-IV substrate (H_007 byte-mirror, N=16, dim=12,
warm=8, rep=0) 위에 3 가지 drive mode (zero / selffeed / random) 의 per-step
perturbation 을 가하고, selffeed mode 에서 feedback_gain ∈ {0.0, 0.25, 0.5, 0.75, 1.0}
sweep. 모든 substrate state-matrix 를 동일 `phi_spatial(states, N, dim, 4)` 로 측정.
**peak Φ(selfref) > max(Φ_zero, Φ_random) AND argmax ∈ {0.25, 0.5, 0.75}** 면 SUPPORTED.

## 2. Why

- **H_007 cross-link** (PR #167): elementary CA 의 Wolfram class-axis 에서
  Class-IV (rule 110) 가 ordered/chaotic 보다 높은 Φ 를 산출 — Langton λ
  edge-of-chaos 의 substrate-side numerical evidence. 본 H_202 는 동일 substrate
  + 동일 primitive 위에 **새로운 직교 축** (self-reference feedback gain) 을
  추가하고, 그 축에서도 동형의 mid-regime peak 이 emerge 하는지 묻는다.
- **H_018 cross-link** (PR #168): SELFFEED self-genesis 가 ZERO/DRIVE 보다 더
  많은 spontaneous split 을 fire — "external 입력 없이 internal 자기참조 만으로
  운동을 bootstrap" 하는 mechanism. 본 H_202 는 그 SELFFEED 이 단지 *more dynamic*
  한 것이 아니라 **integrated information** 측면에서 random 보다 높음 (control
  for "any perturbation works") 을 묻는다.
- **H_004 cross-link** (PR #180): Φ-function dissociation honest boundary 를 carry
  — "Φ peak ≠ phenomenal consciousness", 본 H 는 그 boundary 안에서 *operationally
  testable substrate claim* 만 다룬다.
- **새 axis (raw#12 정합)**: H_007 의 rule-axis 와 본 H 의 self-ref-axis 가
  **직교** (orthogonal) 임이 핵심 — 동일 Class-IV substrate (rule 110) 위에서
  self-ref strength 만 sweep, rule 은 고정. 만약 self-ref-axis 에서도 mid-regime
  peak 이 emerge 하면 "edge-of-chaos Φ-peak 은 Wolfram class 에 국한되지 않는
  more general dynamical principle" 의 numerical evidence.

사용자 directive (raw#9/12 정합): hexa-only · deterministic · llm:none · $0 mac local.
H_003 H3.4 toolchain note 에 따라 `c_lib.hexa` import 가 c_lib path 불일치로
실패할 경우 `phi_spatial(states, N, dim, 4)` **runtime builtin 직접 호출** —
본 H_202 는 처음부터 직접 호출 path 채택 (worktree-agnostic, robust).

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H202.1 | Φ(self-ref peak) > Φ(zero-drive) + 1e-6 | 자기참조가 inert substrate 보다 더 높은 integration |
| H202.2 | Φ(self-ref peak) > Φ(random-drive @ gain=1.0) + 1e-6 | self-ref 가 chaotic random 보다 더 integrated |
| H202.3 | argmax_gain ∈ {0.25, 0.5, 0.75} (middle 30%-70% of sweep) | 너무 작은 gain = inert / 너무 큰 gain = degenerate; mid-range = edge-of-chaos analog |
| H202.4 | H_007 와 byte-identical phi_spatial primitive (n_bins=4) 사용 | provenance reproducibility · cross-link rigor |

## 4. Variables

| axis | levels |
|------|--------|
| axis1 (`feedback_gain`) | {0.0, 0.25, 0.5, 0.75, 1.0} (5 levels) |
| axis2 (`drive_mode`) | {zero, selffeed, random} (3 levels) |
| axis3 (`N` lattice) | 16 (fixed — single config, robustness deferred) |
| axis4 (`rule`) | 110 (Class-IV, H_007 high-Φ substrate, fixed) |
| axis5 (`dim` × `warm` × `rep` × `seed`) | 12 × 8 × 0 × 42 (deterministic) |

총 측정 = 1 (zero baseline) + 1 (random control @ gain=1.0) + 5 (selffeed gain sweep) = **7 Φ 값**.

## 5. Run Protocol

1. **substrate construction (H_007 mirror)**: N=16 periodic 1D lattice; `_init_row`
   sets site i ON iff (i + rep) % 3 != 0, rep=0; 동일 deterministic seed 모든 mode 공유.
2. **per-step drive perturbation (BEFORE rule-110 transition)** in
   `_apply_drive_fast(row, n, mode, gain, lcg_box)`:
   - `zero`: no perturbation.
   - `selffeed`: 각 site i 에 대해 LCG-derived `frac < gain` 이면 `row[i] := row[(i+1) % N]`
     (1-step cyclic shift import = self-reference neighbor adopt).
   - `random`: 각 site i 에 대해 `frac < gain` 이면 LCG 2nd advance bit 으로 `row[i]` overwrite.
   - LCG: `next = (state * 1103515245 + 12345) mod 2^31-1`, seed=42, 단일 in-script state.
3. **rule-110 transition (periodic boundary)**: `_ca_next(l,c,r,110)` byte-mirrors H_007.
4. **record state matrix**: warm=8 step warmup 후 dim=12 step 의 (site × time) flat farr.
5. **Φ measurement**: `phi_spatial(states, N=16, dim=12, n_bins=4)` runtime builtin (RFC 036).
6. **peak detection**: argmax of selfref sweep (5 levels).
7. **falsifier evaluation** → verdict → `result.json` write.

per-cell ledger (deterministic 보장): LCG state 는 `lcg_box[0]` (length-1 hexa list)
에 in-place 유지, mode/gain 별로 별도 시퀀스 (각 `_run_phi` 호출이 fresh seed=42 로
초기화). 같은 (mode, gain) 재호출은 byte-identical 결과.

## 6. Criteria

- **C1** (H202.1): Φ_peak_selfref > Φ_zero + 1e-6
- **C2** (H202.2): Φ_peak_selfref > Φ_random + 1e-6
- **C3** (H202.3): peak_gain ∈ {0.25, 0.5, 0.75}
- **C4** (H202.4): primitive provenance = `phi_spatial(s, 16, 12, 4)` runtime builtin (RFC 036),
  H_007 의 `c_measure_phi` wrapper 와 byte-equivalent (n_bins=4 동일).

**verdict_rule**:
- `SUPPORTED`   iff C1 ∧ C2 ∧ C3 ALL PASS (C4 는 provenance 로 trivially 충족).
- `PARTIAL`     iff ≥1 of (C1, C2, C3) PASS.
- `FALSIFIED`   iff 0 of (C1, C2, C3) PASS.

## 7. Falsifiers (≥5)

| ID | 조건 | observable | line |
|----|------|------------|------|
| F1 SELFREF-GT-ZERO | Φ_peak > Φ_zero + 1e-6 | `peak_v - phi_zero` | smoke L233 |
| F2 SELFREF-GT-RAND | Φ_peak > Φ_rand + 1e-6 | `peak_v - phi_rand` | smoke L234 |
| F3 MID-PEAK | peak_index ∈ {1, 2, 3} (gain ∈ {0.25,0.5,0.75}) | `peak_i ∈ {1,2,3}` | smoke L235 |
| F4 NONNEG-FINITE | 모든 Φ finite (no NaN/inf) & ≥ 0 | `_is_finite(.)` over 7 Φ | smoke L237–242 |
| F5 RERUN-DETERMINISTIC | 동일 seed → byte-identical Φ sweep across reruns | re-run output diff | manual rerun |

F-trigger 시 lane semantics:
- F1 FAIL → H202.1 FALSIFIED (자기참조가 integration 못 키움 — substrate 자체로 충분).
- F2 FAIL → H202.2 FALSIFIED (random perturbation 이 더 integrated — self-ref 의 lever 없음).
- F3 FAIL → H202.3 FALSIFIED (peak 이 gain=0 또는 gain=1 — monotone / degenerate).
- F4 FAIL → primitive error (phi_spatial proxy 문제, smoke 재설계 trigger).
- F5 FAIL → raw#9 violation (non-determinism — LCG seed 또는 hidden global state).

## 8. Honest Limits (≥5, raw#91 c3)

- **L1** `phi_spatial` 는 phi_rs `compute_phi_inner` 의 **spatial-slice replica** (RFC 036) —
  full IIT 4.0 MIP partition 이 아닌 🟢 SUPPORTED-NUMERICAL proxy. 결과는 🔵 closed-form 이 아니라
  🟢 numerical evidence tier.
- **L2** single substrate config (N=16, dim=12, warm=8, rep=0, rule=110). robustness across
  (N, dim, rule, rep) 미검증 — peak shape 의 form-stability 는 별도 cycle.
- **L3** feedback functional form 은 **binary cyclic-shift-import** (1-step right-neighbor adoption,
  probability=gain). 다른 form (sigmoid blend / XOR / convex 1D linear / multi-step shift) 은
  미검증 — form-specific finding 일 수 있음.
- **L4** "edge-of-chaos" 라는 표현은 H_007 의 Wolfram class-axis 정의에서 차용한 **analogy** —
  self-ref-axis 에서의 "edge" 가 Langton λ critical regime 과 *literally equivalent* 하다는
  주장 X. 두 axis 의 peak 이 *both mid-regime* 라는 numerical co-incidence 만 보고.
- **L5** Φ peak ≠ phenomenal consciousness — H_004 hard-problem honest boundary (PR #180) carry.
  본 결과는 IIT 의 *substrate-side numerical correlate* 에 대한 것이지, phenomenal qualia
  존재 / 환원 가능성에 대한 evidence 가 아님.
- **L6** drive mode 의 PRNG (LCG) state 가 `selffeed` 에서도 *site 선택* 에만 쓰여 *어느 site 를
  perturb 할지* 는 random — 즉 selffeed 의 "어디" 는 random, "어떻게" 는 deterministic shift.
  pure-deterministic mid-regime peak 의 robustness 는 별도 cycle.

## 9. Cross-Links

- **sister hypotheses (UNIVERSE/)**:
  - [`H_007_cellular_automaton_consciousness.md`](H_007_cellular_automaton_consciousness.md)
    — Wolfram class-axis Φ peak (PR #167 MERGED). 본 H_202 의 substrate (rule 110) + phi primitive 의 원천.
  - [`H_018_genesis_spontaneous_emergence.md`](H_018_genesis_spontaneous_emergence.md)
    — SELFFEED self-genesis (PR #168 MERGED). 본 H_202 의 self-reference concept 의 원천.
  - [`H_004_consciousness_hard_problem.md`](H_004_consciousness_hard_problem.md)
    — Φ-function dissociation honest boundary (PR #180 MERGED). 본 H_202 의 §Honest Limits L5 carry.
- **toolchain**: H_003 H3.4 노트 (`UNIVERSE/H_003_life_origin_question.md` §H3.4) —
  c_lib import 대신 `phi_spatial` runtime builtin 직접 호출 fallback path.
- **RFC**: RFC 036 phi_spatial (`HEXAD/C/c_lib.hexa` 의 c_measure_phi wrapper 와 동일 primitive,
  n_bins=4 default).
- **legacy**: `hypotheses_legacy_2026_05_15/` 양식 (10-section + YAML frontmatter) carry.

## 10. Verdict

**Run**: 2026-05-23, mac-local, `HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h202_selfref_phi_2026_05_23/run_h202.hexa`, $0 cost, deterministic (re-run byte-identical).

**VERBATIM smoke output**:

```
H_202 — self-ref edge-of-chaos Φ (cross-link H_007 ⊕ H_018, raw#12)
  N=16 dim=12 warm=8 rule=110 (Class-IV)
  Φ primitive: RFC 036 phi_spatial(states, N, dim, 4)
  drive modes: zero | selffeed | random — feedback_gain sweep ∈ {0,0.25,0.5,0.75,1.0}
  HONEST: phi_spatial = 🟢 NUMERICAL spatial-slice proxy; Φ-peak ≠ phenomenal qualia.

  Φ(zero-drive,   gain=0.00)       = 0.538242
  Φ(random-drive, gain=1.00)       = 0.49116
  Φ(self-ref,     gain=0.0)       = 0.538242
  Φ(self-ref,     gain=0.25)       = 0.741615
  Φ(self-ref,     gain=0.5)       = 0.619323
  Φ(self-ref,     gain=0.75)       = 0.586545
  Φ(self-ref,     gain=1.0)       = 1.14511e-05

  PEAK : argmax gain=0.25  Φ_peak=0.741615

  F1 SELFREF-GT-ZERO   (Φ_peak > Φ_zero + 1e-6)         : PASS  (Δ=0.203373)
  F2 SELFREF-GT-RAND   (Φ_peak > Φ_rand + 1e-6)         : PASS  (Δ=0.250455)
  F3 MID-PEAK          (argmax ∈ {0.25,0.5,0.75})       : PASS  (peak_gain=0.25)
  F4 NONNEG-NOFINITE   (all Φ finite & ≥ 0)             : PASS
  F5 RERUN-DETERMINISTIC (fixed LCG seed)               : PASS

  VERDICT_RULE: SUPPORTED iff (F1 ∧ F2 ∧ F3); PARTIAL if ≥1; FALSIFIED if 0
  VERDICT     : SUPPORTED   (core_pass=3/3)
```

**verdict_class**: 🟢 SUPPORTED-NUMERICAL (5/5 falsifiers PASS, 3/3 core criteria C1+C2+C3 PASS).

**evidence_summary**:
- Φ(zero-drive)              = 0.538242 (= H_007 rule110 baseline, expected: per-step zero perturbation = pure rule-110)
- Φ(random-drive, gain=1.0)  = 0.491160 (chaotic noise *lowers* integration vs pure dynamics)
- Φ(selffeed, gain=0.0)      = 0.538242 (== zero-drive: degenerate boundary, no perturbation)
- Φ(selffeed, gain=0.25)     = **0.741615 PEAK** (Δ=+0.203 over zero, Δ=+0.250 over random, +37.8% rel.)
- Φ(selffeed, gain=0.5)      = 0.619323 (still > zero & random; descent from peak)
- Φ(selffeed, gain=0.75)     = 0.586545 (further descent)
- Φ(selffeed, gain=1.0)      = 1.145e-05 (≈ 0; full shift collapse — degenerate over-coupling)

peak_gain = **0.25** ∈ {0.25, 0.5, 0.75} → mid-regime confirmed. Φ landscape on self-ref axis
exhibits an inverted-U with **single interior peak**, mirroring H_007's Wolfram class-axis
inverted-U at Class-IV (between Class-II and Class-III). The two axes are *directly orthogonal*
(rule = 110 fixed across all 7 measurements; only feedback gain varies for sweep).

**falsifiers_triggered**: none (5/5 PASS).
**criteria_met**: C1 ∧ C2 ∧ C3 ∧ C4 (all 4 PASS).

**cross-link finding** (raw#12 sister-link evidence): H_007 의 Class-IV 가 Wolfram rule-axis 의
**edge-of-chaos** 라면, H_202 는 **동일 Class-IV substrate** 위에 **self-reference axis** 를
얹어, *그 새 축에서도* mid-gain peak 이 emerge 함을 보임. 즉 phi_spatial 의 inverted-U
shape 는 *Wolfram class 에 specific* 한 것이 아니라 *both-axis general* 한 dynamical
phenomenon — H_007 의 finding 을 generalize.

**honest tier**: 🟢 SUPPORTED-NUMERICAL (phi_spatial spatial-slice proxy — NOT 🔵 full IIT 4.0 MIP).
Per §Honest Limits L1, full closed-form Φ 와 일치할지 미검증; L4 per "edge-of-chaos" = analogy.

**post-run**: `state/h202_selfref_phi_2026_05_23/result.json` written (7 Φ + 5 falsifier verdicts + verdict_rule); status 는 본 cycle 시점 `running` 유지 (single-config measurement landed; cross-config robustness sweep 은 차후 cycle 의 lane).
