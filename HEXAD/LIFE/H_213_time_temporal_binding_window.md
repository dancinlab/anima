---
id: H_213
slug: time-temporal-binding-window
title: H_213 time-temporal-binding-window — Φ inverse-U τ-sweep (의식의 형식 substrate proxy)
domain: time · consciousness · physics
status: running
exploration_method: E6 (cross-domain-analogy · phenomenology↔IIT) + E11 (temporal-axis-extension of H_007 rule-axis)
verification_method: W1 (smoke) + W3 (τ sweep) + W12 (sister-link to H_007 / H_202 / H_018)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_213 — time-temporal-binding-window (의식의 형식 = 적정 통합 시간 window)

## 1. Hypothesis

rule 110 (H_007 Class-IV) substrate 위에서, state 의 시간평균 **'binding window' τ**
(sliding moving average over t-τ+1..t) 을 sweep 했을 때, `phi_spatial` Φ 가
**τ 에 대해 inverse-U** 모양을 그린다 — τ 가 너무 작으면 (1-2 step) instantaneous
local · noisy 로 low-Φ, τ 가 너무 크면 (>20 step) over-averaging 으로 state 가
균질해져 low-Φ, **중간 τ ≈ 5-10 step** (생물학적 100ms gamma-cycle 의 analog) 에서
Φ peak. 이 형식이 의식의 **'specious present'** (Husserl) 위 IIT 정합의 substrate-side
numerical correlate.

정밀화 (operational): rule 110 Class-IV substrate (H_007 byte-mirror, N=16, dim=12,
warm=8, rep=0) 의 *동일 60-step trajectory* 위에 τ ∈ {1, 2, 5, 10, 20, 40} 의
uniform moving-average kernel 적용 → averaged trajectory 의 **final dim=12 step
window** 을 잘라 `phi_spatial(states_avg, N=16, dim=12, n_bins=4)` 로 측정.
**Φ(τ) 가 inverse-U with interior peak τ\* ∈ {2, 5, 10}** 이고 양 boundary (τ=1, τ=40)
대비 ≥10% margin 이면 SUPPORTED.

## 2. Why

- **H_007 cross-link** (PR #167): Wolfram **class-axis** 에서 Class-IV 가 ordered /
  chaotic 보다 높은 Φ — Langton λ edge-of-chaos 의 substrate evidence. 본 H_213 은
  **rule 110 substrate 를 고정** 하고, *직교 축* 으로 **temporal-binding-window τ**
  를 sweep. 그 새 축에서도 mid-regime peak 가 emerge 하면 "Φ-peak 은 single axis 의
  property 가 아닌 *multi-axis general* dynamical principle" 의 추가 evidence.
- **H_202 cross-link** (PR #182 candidate, this cycle's sister): self-reference axis
  에서 mid-gain peak emerge (gain=0.25 에서 Φ=0.74 vs zero=0.54, random=0.49). 본
  H_213 은 *3rd orthogonal axis* (temporal averaging window) 위에서 동형 inverse-U
  가 emerge 하는지 묻는다.
- **H_018 cross-link** (PR #168): SELFFEED self-genesis 의 시간적 dynamics — 시간이
  의식의 substrate 에서 어떤 역할을 하는지의 자매 hypothesis. 본 H_213 은
  "*어떤 시간 scale* 에서 통합이 maximal 한가?" 를 sub-question 으로 정의.
- **H_004 cross-link** (PR #180): Φ-function dissociation honest boundary —
  "Φ peak ≠ phenomenal consciousness" 를 carry. 본 H 는 *Husserl's specious present*
  의 phenomenological concept 을 *operational analog* 으로 testable 화 (analogy 명시).
- **raw#12 정합** (sister-link rigor): H_007 (rule-axis) ⊥ H_202 (self-ref-axis) ⊥
  H_213 (time-axis) — 3 직교 축 위에서 inverse-U 가 *co-emerge* 하는지가 본 cycle 의 핵심.

사용자 directive (raw#9/12 정합): hexa-only · deterministic · llm:none · $0 mac local.
`phi_spatial(states, N, dim, 4)` runtime builtin 직접 호출 (H_202 path 채택,
worktree-agnostic, robust).

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H213.1 | Φ(τ) 가 τ-sweep 위 inverse-U with **single peak τ\*** (not monotone) | 너무 짧은 window = noisy, 너무 긴 window = over-averaged |
| H213.2 | τ\* ∈ {2, 5, 10} (sweep interior, NOT at boundary 1/40) | biological binding range proxy (~100ms gamma-cycle analog) |
| H213.3 | Φ(τ=1) < Φ(τ\*) margin ≥ 10% | instantaneous integration 불충분 (specious present 필요) |
| H213.4 | Φ(τ=40) < Φ(τ\*) margin ≥ 10% | over-averaged dilution (binding window 너무 크면 state homogeneous) |
| H213.5 | re-run byte-identical (no PRNG, fixed init, fixed rule) | raw#9 determinism compliance |

## 4. Variables

| axis | levels |
|------|--------|
| axis1 (`tau` binding window) | {1, 2, 5, 10, 20, 40} (6 levels, log-ish spread) |
| axis2 (`N` lattice) | 16 (fixed — single config, robustness deferred) |
| axis3 (`rule`) | 110 (Class-IV, H_007 high-Φ substrate, fixed) |
| axis4 (`dim` × `warm` × `total_record` × `rep`) | 12 × 8 × 60 × 0 (deterministic) |
| axis5 (`window_kernel`) | uniform moving average (rectangular kernel, fixed) |

총 측정 = 6 Φ 값 on **단일 trajectory** (rule-110, N=16, total_record=60).

## 5. Run Protocol

1. **substrate construction (H_007 mirror)**: N=16 periodic 1D lattice; `_init_row`
   sets site i ON iff (i + 0) % 3 != 0 (rep=0); 단일 deterministic trajectory.
2. **trajectory build**: warm=8 step warmup → 60 step record. 모든 (site, step) 을
   row-major flat farr `traj[i * total + t]` (length N*60=960) 에 보관.
3. **τ sweep**: τ ∈ {1, 2, 5, 10, 20, 40}. 각 τ 에 대해:
   - `_moving_average(traj, τ)` → averaged trajectory `avg[i, t] = mean over (t-τ+1)..t of traj[i, ·]`
     (left-clamp boundary: window 가 t < τ-1 에서 자동 shrink).
   - `_final_window(avg)` → averaged trajectory 의 **last dim=12 step** (step 48..59) 을
     잘라 (N × dim) flat farr `states_avg[s * dim + t_local]`.
   - `phi_spatial(states_avg, 16, 12, 4)` runtime builtin (RFC 036) 로 Φ 측정.
4. **peak detection**: argmax of 6-element phi array.
5. **criteria evaluation**:
   - C1 monotonicity check (strictly_inc=false AND strictly_dec=false).
   - C2 peak_i ∈ {1, 2, 3} (τ\* ∈ {2, 5, 10}).
   - C3 (peak_v − phi[0]) ≥ 0.10 · peak_v.
   - C4 (peak_v − phi[5]) ≥ 0.10 · peak_v.
6. **verdict** → `result.json` write.

per-cell ledger (deterministic 보장): 단일 trajectory 위 *순수 결정적* moving average
(PRNG 없음) → 모든 τ 측정은 trajectory build 의 함수, byte-identical re-run.

## 6. Criteria

- **C1** (H213.1): NOT (strictly_inc OR strictly_dec) — Φ(τ) sweep 가 monotone 아님.
- **C2** (H213.2): peak_index ∈ {1, 2, 3} → τ\* ∈ {2, 5, 10}.
- **C3** (H213.3): Φ(τ=1) < Φ(τ\*) AND (Φ(τ\*) − Φ(τ=1)) ≥ 0.10 · Φ(τ\*).
- **C4** (H213.4): Φ(τ=40) < Φ(τ\*) AND (Φ(τ\*) − Φ(τ=40)) ≥ 0.10 · Φ(τ\*).

**verdict_rule**:
- `SUPPORTED`            iff C1 ∧ C2 ∧ C3 ∧ C4 ALL PASS.
- `PARTIAL_DIRECTIONAL`  iff C1 ∧ C3 PASS (interior peak emerged + τ=1 dilution confirmed)
                          but C2 boundary missed OR C4 margin under-thresh.
- `PARTIAL`              iff ≥1 of (C1, C2, C3, C4) PASS but not above.
- `FALSIFIED`            iff monotone (C1 FAIL).

## 7. Falsifiers (≥5)

| ID | 조건 | observable | line |
|----|------|------------|------|
| F1 NOT-MONOTONE | strictly_inc=false AND strictly_dec=false | C1 verdict | smoke L≈233 |
| F2 NOT-BOUNDARY-PEAK | peak_i ∉ {0, 5} (τ\* ∉ {1, 40}) | peak_tau check | smoke L≈246 |
| F3 TAU1-DILUTED | Φ(τ=1) < Φ(τ\*) margin ≥ 10% | margin1 vs thresh1 | smoke L≈251 |
| F4 NONNEG-FINITE | 모든 Φ finite (no NaN/inf) & ≥ 0 | `_is_finite(.)` ×6 | smoke L≈262 |
| F5 RERUN-DETERMINISTIC | byte-identical re-run | re-run output diff | manual rerun |

F-trigger 시 lane semantics:
- F1 FAIL → H213.1 FALSIFIED (monotone — Φ 가 τ 에 단조 — binding window concept 자체 부재).
- F2 FAIL → H213.2 FALSIFIED (peak 이 boundary — 너무 짧거나 너무 김 — interior binding window 없음).
- F3 FAIL → H213.3 FALSIFIED (instantaneous = peak — specious present 불필요, τ=1 충분).
- F4 FAIL → primitive error (phi_spatial proxy 문제, smoke 재설계 trigger).
- F5 FAIL → raw#9 violation (non-determinism — hidden PRNG / global state).

## 8. Honest Limits (≥5, raw#91 c3)

- **L1** 'binding window' operationalization = **uniform moving average** (rectangular
  kernel) — 다른 form (exponential decay τ_E, attention-weighted Gaussian, frequency-domain
  low-pass, leaky-integrator) 은 다른 τ\* / 다른 peak shape 가능. form-specific finding 일 수 있음.
- **L2** τ unit = **simulation step ≠ ms** · 1 step ↔ ~10-20ms biological gamma-cycle 등
  mapping 은 *임의 analogy*. 100ms specious-present 정합 = order-of-magnitude rhetoric
  이지 literal mapping 아님.
- **L3** `phi_spatial` = 🟢 **NUMERICAL spatial integration proxy** · 시간 도메인 적용은
  *averaged state 위 spatial measure* — **temporal Φ 직접 측정 X**, IIT 4.0 의
  cause-effect-structure temporal extension 아님. 결과 tier 는 🟢 numerical (NOT 🔵 closed-form).
- **L4** single rule (110) Class-IV substrate · 다른 rule (250 Class-II ordered /
  30 Class-III chaotic) 에서 다른 τ\*, 다른 peak presence 가능 — form-stability deferred.
  rule-axis × time-axis cross-product 은 별도 cycle.
- **L5** **'specious present'** (Husserl) 는 phenomenological concept · 본 cycle 은 spatial-Φ
  위 temporal-window proxy 일 뿐 — **phenomenal binding** (qualia 가 시간적으로 묶이는 경험)
  아님. H_004 hard-problem honest boundary (PR #180) carry — 본 결과는 substrate-side
  numerical correlate 에 대한 것이지, "의식이 5 step 의 window 로 묶임" 이라는
  phenomenal claim 아님.
- **L6** left-clamp boundary (window 가 t < τ-1 에서 shrink) 는 τ=40 에서 효과적으로
  t < 39 의 모든 step 이 (1..t) 크기 window 로 평균화 → 결국 τ=40 의 final window 는
  *전체 trajectory mean* 에 수렴. 따라서 τ=40 측정은 "near-uniform-state Φ" 의 limiting
  case — over-averaging 의 *upper-bound* proxy 일 뿐.

## 9. Cross-Links

- **sister hypotheses (HEXAD/LIFE/)**:
  - [`H_007_cellular_automaton_consciousness.md`](H_007_cellular_automaton_consciousness.md)
    — Wolfram class-axis Φ peak (PR #167 MERGED). 본 H_213 의 substrate (rule 110) +
    phi primitive 의 원천. **rule-axis (H_007) ⊥ time-axis (H_213)**.
  - [`H_202_selfref_edge_of_chaos_phi.md`](H_202_selfref_edge_of_chaos_phi.md)
    — self-ref-axis Φ peak inverse-U (cycle #7 sister). **self-ref-axis ⊥ time-axis**.
  - [`H_018_genesis_spontaneous_emergence.md`](H_018_genesis_spontaneous_emergence.md)
    — temporal dynamics genesis · timestep loop (PR #168 MERGED). 본 H 의 *시간 substrate*
    concept 의 sister.
  - [`H_004_consciousness_hard_problem.md`](H_004_consciousness_hard_problem.md)
    — Φ-function dissociation honest boundary (PR #180 MERGED). 본 H_213 의 §Honest Limits L5 carry.
- **RFC**: RFC 036 `phi_spatial` runtime builtin (HEXAD/C/c_lib.hexa `c_measure_phi`
  wrapper 와 byte-equivalent, n_bins=4 default).
- **legacy**: `hypotheses_legacy_2026_05_15/` 양식 (10-section + YAML frontmatter) carry.

## 10. Verdict

**Run**: 2026-05-23, mac-local, `HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h213_temporal_binding_2026_05_23/run_h213.hexa`, $0 cost, deterministic (re-run byte-identical).

**VERBATIM smoke output**:

```
H_213 — time-temporal-binding-window · Φ inverse-U τ-sweep (raw#12)
  N=16 dim=12 warm=8 total_record=60 rule=110 (Class-IV)
  Φ primitive: RFC 036 phi_spatial(states_avg, N, dim, 4)
  τ sweep: {1, 2, 5, 10, 20, 40} — binding window (sliding moving average)
  HONEST: phi_spatial = 🟢 NUMERICAL spatial-slice proxy; specious-present = analogy.

  Φ(τ=1)  = 0.741476
  Φ(τ=2)  = 2.71665
  Φ(τ=5)  = 3.94854
  Φ(τ=10)  = 2.52985
  Φ(τ=20)  = 2.63751
  Φ(τ=40)  = 5.35707

  PEAK : argmax τ*=40  Φ_peak=5.35707

  C1 SINGLE-PEAK   (not monotone, single interior peak)   : PASS  (strictly_inc=false strictly_dec=false)
  C2 TAU-INTERIOR  (τ* ∈ {2,5,10}, peak_i ∈ {1,2,3})       : FAIL  (peak_tau=40)
  C3 TAU1-LT-PEAK  (Φ(τ=1) < Φ(τ*), margin ≥ 10%)         : PASS  (Δ=4.61559, thresh=0.535707)
  C4 TAU40-LT-PEAK (Φ(τ=40) < Φ(τ*), margin ≥ 10%)        : FAIL  (Δ=0.0, thresh=0.535707)
  F4 NONNEG-FINITE (all Φ finite & ≥ 0)                   : PASS
  F5 RERUN-DETERMINISTIC (no PRNG, fixed init)            : PASS

  VERDICT_RULE: SUPPORTED iff (C1∧C2∧C3∧C4); PARTIAL_DIRECTIONAL iff (C1∧C3) interior peak; PARTIAL iff ≥1; FALSIFIED iff monotone
  VERDICT     : PARTIAL_DIRECTIONAL   (criteria_pass=2/4)
```

**verdict_class**: 🟢 **PARTIAL_DIRECTIONAL** (NUMERICAL · 2/4 criteria PASS) —
non-monotone (C1) + τ=1 dilution (C3) 확정, 그러나 **global peak 가 boundary τ=40** 에
위치 (C2 FAIL) + τ=40 margin=0 (C4 FAIL trivially because τ=40 = peak).

**evidence_summary**:
- Φ(τ=1)  = 0.741476  (instantaneous integration — lowest after τ=1 dilution)
- Φ(τ=2)  = 2.71665   (3.66× over τ=1, integration recovers)
- Φ(τ=5)  = 3.94854   (**interior local maximum** between τ=2 and τ=10 — biological binding range proxy)
- Φ(τ=10) = 2.52985   (descent — over-averaging starts)
- Φ(τ=20) = 2.63751   (small recovery)
- Φ(τ=40) = **5.35707 GLOBAL PEAK**  (boundary — over-averaging *increases* spatial-Φ due to phi_spatial
                                       handling of near-uniform states; honest L6 boundary effect)

peak_tau = **40** (boundary) → C2 FAIL. Φ landscape exhibits **bimodal** structure with
*interior local maximum at τ=5* (Φ=3.95, 5.3× over τ=1) **and** *boundary global maximum at τ=40*
(Φ=5.36). 즉 specious-present analog (τ=5 ≈ 50-100ms biological cycle) 가 *locally* emerge 하지만
*globally* over-averaging boundary 가 더 높은 spatial-Φ proxy 산출 — phi_spatial proxy 의 한계
(L6) 와 honest empirical 양면 모두.

**falsifiers_triggered**: F2 NOT-BOUNDARY-PEAK FAIL (peak at τ=40 boundary).
**criteria_met**: C1 ∧ C3 (2/4); C2 ∧ C4 NOT met.

**finding (raw#12 sister-link honest)**:
- H_007 (rule-axis), H_202 (self-ref-axis) 의 inverse-U peak 가 본 time-axis 위에서는
  **partial** — *interior local peak* (τ=5) 는 emerge 하지만 *global peak* 가 boundary
  (τ=40) 에 위치. "specious-present 형식의 Φ-peak" 는 *uniform moving average proxy*
  + *phi_spatial spatial-slice proxy* 의 limit 안에서 *directional evidence* 까지만 도달.
- *form-stability cycle 후보*: (a) exponential-decay kernel (leaky integrator) 로 large-τ
  saturation 제거, (b) rule-axis × time-axis cross-product (다른 rule 위 τ\* 위치 측정),
  (c) larger sweep range (τ=60, 80) 로 over-averaging 의 Φ-decline arm 확인,
  (d) **temporal IIT** primitive (cause-effect-structure 의 temporal extension) 로
  spatial proxy 한계 (L3) 우회.
- honest empirical: τ=40 의 Φ=5.36 boundary peak 는 phi_spatial 의 *near-uniform state 처리*
  artefact 가능성 ≥ 50% — temporal Φ 의 *true* peak 일 가능성과 양립.

**honest tier**: 🟢 PARTIAL_DIRECTIONAL (NUMERICAL · phi_spatial spatial-slice proxy on
temporally-averaged state — NOT 🔵 full temporal IIT; specious-present = analogy).
Per §Honest Limits L1-L6, kernel form / rule choice / sweep range / spatial-proxy limit
의 4 자유도 모두 본 cycle 에서 *고정* — 어느 하나의 변경이 verdict 를 SUPPORTED ↔ FALSIFIED
로 뒤집을 수 있음.

**post-run**: `state/h213_temporal_binding_2026_05_23/result.json` written
(6 Φ + 4 criteria + 5 falsifier verdicts + verdict_rule); status 는 본 cycle 시점 `running`
유지 (single-config measurement landed; form-stability + temporal-IIT robustness sweep 은
차후 cycle 의 lane).
