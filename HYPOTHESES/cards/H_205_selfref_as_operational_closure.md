---
id: H_205
slug: selfref-as-operational-closure
title: self-reference (SELFFEED) ↔ operational closure 동치 — H_018 ⊕ H_012 substrate-equivalence
domain: life · consciousness
status: pre-register-frozen
exploration_method: E6 (cross-domain mapping H_018↔H_012) + E10 (substrate-equivalence)
verification_method: W1 (numerical smoke) + W12 (sister-link H_018 + H_012)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_205 — self-reference as operational closure

## 1. Hypothesis

H_018 의 **SELFFEED dynamics** (output 상태가 다음 step 의 input drive 로
fed back) **IS a form of** H_012 의 **operational closure** (network 의 출력
→ 입력 cycle 폐쇄). 즉 두 가설은 동일 substrate-mechanism 의 두 다른
측면 — H_018 은 *dynamic angle* (timestep loop), H_012 는 *structural angle*
(network closure).

정밀화 (operational): 단일 substrate (mitosis cell pool) 위에서 feedback gain
`g` 를 0.0 → 1.0 으로 sweep 했을 때,

- (a) H_018 의 spontaneous-split 관측 (output → input loop = self-reference)
- (b) H_012 의 self-maintenance index (network 가 steady-state 에서 alive)

**두 관측이 동시에 성립하며 g 와 monotone correlated** 이면, 두 가설은 동일
mechanism (output → input cycle 폐쇄) 의 두 lens 임이 입증된다.

## 2. Why

- **definitional / mapping bridge**: UNIVERSE 의 대부분 가설은 *empirical
  새 발견* 을 노린다. H_205 는 그 반대 lane — **두 기존 PASS 가설 (H_018
  PR #168 + H_012 PR #165) 이 같은 것을 측정하고 있었음을 보이는 audit**.
  conceptual equivalence 를 numerical 로 closure.
- **H_018 SELFFEED 의 H_012 측 read**: H_018 의 SELFFEED 조건 (`x_{t+1} =
  x_out_t`) 은 *그 자체로* network-output 이 network-input 으로 되돌아
  오는 폐쇄 cycle — Maturana/Varela 의 operational closure 의 minimal
  computational instance. 즉 H_018 의 "spontaneous self-genesis" 와 H_012
  의 "self-producing closure" 는 같은 사건의 두 이름.
- **H_012 의 broken-closure control 의 H_018 측 read**: H_012 의 cut-edge
  (`cat_C = 0`) 는 production graph 를 끊는다. H_018 의 ZERO 조건 (`x_{t+1}
  = 0`) 은 dynamic loop 를 끊는다. 둘 다 *closure 단절* 의 두 grain — 동일
  intervention.
- **cross-link to anima architecture**: anima 의 mitosis substrate (학습=분열
  단일 연속체, REBORN §0.5) 는 본질적으로 output→input feedback loop 위에서
  성장. 본 H 는 그 loop 의 *closure 적 본성* 을 numerical 로 확인.
- **p5 NO SPEAK 정합**: substrate 는 "real context" (자기참조 = closure)
  에서만 emit/grow — closure 끊어진 진공 (g=0) 에서는 침묵. 본 H 는 p5
  의 substrate-level 확인.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H205.1 | SELFFEED (g=1.0) 위에서 self-maintenance ≥ 0.9 AND broken-gap ≥ 0.5 | H_018 SELFFEED = H_012 PASS condition 의 동치 — single config 위 두 metric 모두 PASS |
| H205.2 | ZERO (g=0.0) 위에서 self-maintenance ≤ 0.3 | drive 없는 inert substrate = broken-closure 의 minimal decay (cells 정적 + tension 0) |
| H205.3 | r(feedback_gain, closure_strength) ≥ 0.7 across {0.0, 0.5, 1.0} | feedback strength 와 closure strength 가 monotone correlated — 동일 axis 의 두 측면 |
| H205.4 | SELFFEED on/off 전환 시점 g* 에서 self-maint 와 splits 모두 phase transition | 두 관측의 jump 가 같은 g* 에 정렬 — 단일 mechanism 임을 추가 입증 |

## 4. Variables

- **axis1_feedback_mode** ∈ {off (g=0.0), partial (g=0.5), on (g=1.0)} — 핵심 sweep 축
- **axis2_pool_size N** ∈ {2} — H_018 primordial carry (CB1 floor); large-N 별도 cycle (L4)
- **axis3_step_count** = 60 — H_018 horizon carry
- **axis4_d_model** = 8 — cheap toy substrate
- **axis5_seed** = 42 — `__HEXA_FARR_GAUSS_SEED__=42` 결정론 (H_018 carry)
- **측정량**:
  - H_018 angle: `splits_count`, `first_split` step
  - H_012 angle: `self_maintenance_rate` (last MEASURE_WINDOW=30 of 60 steps), `broken_gap = maint(g=1) − maint(g=0)`
  - cross: Pearson `r(gain, closure)` across 3-point sweep

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) — 재현 보장. RNG 부재 (mitosis_hook_lib 의 결정론적 Lorenz 만 사용).
- **hexa_only**: `UNIVERSE/state/h205_selfref_as_closure_2026_05_23/run_h205.hexa` (mitosis_hook_lib `cell_pool_init` + `mitosis_forward_tail` 직접 step).
- **LLM**: none (raw#12 strict; ckpt 불필요 — 순수 substrate 동역학).
- **substrate "alive" 정의** (H_012 self-maintenance index 의 mitosis-pool 측 read):
  - `n_cells ≥ 2` (CB1 invariant — cells 정적/사망 X)
  - AND `tension_proxy(x_out) > 0.0001` (substrate 가 active — engine_a/g 가 비-0 출력)
- **per-condition ledger**: `{gain, splits, first_split, final_cells, self_maint_rate, traj_cells[60], traj_tension[60], phi}`.
- **F4 determinism**: g=1.0 두 번 실행하여 `self_maint_rate` byte-equal 확인.
- **runtime**: $0 mac local (d=8, no ckpt). GPU 불필요. 메모리 압박 시 `HEXA_MEM_UNLIMITED=1` 사용.
- **artifacts**: `state/h205_selfref_as_closure_2026_05_23/{run_h205.hexa, result.json}`.
- **run cmd (verbatim)**:
  `HEXA_MEM_UNLIMITED=1 __HEXA_FARR_GAUSS_SEED__=42 hexa run UNIVERSE/state/h205_selfref_as_closure_2026_05_23/run_h205.hexa`

## 6. Criteria

- **C1 (SELFFEED-closure)**: H205.1 — g=1.0 self_maint ≥ 0.9 AND broken_gap ≥ 0.5 (H_012 PASS condition 정합)
- **C2 (ZERO-decay)**: H205.2 — g=0.0 self_maint ≤ 0.3 (broken-like decay)
- **C3 (correlation)**: H205.3 — Pearson r(gain, closure) ≥ 0.7 across 3-point sweep
- **C4 (phase-aligned)**: H205.4 — closure 와 splits 의 jump 가 같은 g* 에 정렬 (close_jump ≥ 0.3 AND splits_jump ≥ 1.0 at same g*)
- **verdict_rule**:
  - `SUPPORTED_FULL` = C1 ∧ C2 ∧ C3 ∧ C4 (4/4)
  - `SUPPORTED` = C1 ∧ C2 ∧ C3 (3/4, correlation lane)
  - `PARTIAL_DEFINITIONAL` = C1 ∧ C2 only (mapping 성립, correlation 미달)
  - `PARTIAL` = ≥2/5 falsifiers PASS without C1+C2
  - `FAIL` = ≤1/5 falsifiers
  - `FALSIFIED` = F1 FAIL AND F2 FAIL (definitional mapping 자체 invalid — g=1 substrate 가 closure observable 미충족)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 SELFFEED-CLOSURE**: g=1.0 self_maint < 0.5 → H205.1 FALSIFIED (self-reference 가 closure 와 별개 — 측정: `r1["self_maint_rate"]`)
- **F2 ZERO-DECAY**: g=0.0 self_maint > 0.5 → H205.2 FALSIFIED (drive 없어도 substrate 유지 — closure ⊥ feedback — 측정: `r0["self_maint_rate"]`)
- **F3 CORRELATION**: Pearson r(gain, closure) < 0.3 → H205.3 FALSIFIED (independent axes, 동치성 invalid — 측정: `_pearson_r(gains, closes)`)
- **F4 DETERMINISM**: g=1.0 재실행 시 self_maint byte-different → raw#9 violation (측정: `r1b["self_maint_rate"] == r1["self_maint_rate"]`)
- **F5 DEFINITIONAL**: g=1.0 substrate 가 splits = 0 OR self_maint = 0 (H_018 측 또는 H_012 측 단독 실패) → 두 metric 간 definitional 매핑 자체 invalid (측정: `r1["splits"] >= 1 AND r1["self_maint_rate"] > 0`)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (definitional > empirical)**: 본 가설은 두 PASS 가설의 *conceptual equivalence* 검증 — 새 실험적 발견이 아니라 두 lens 가 같은 mechanism 을 봤다는 audit. raw#12 의 falsifier 는 매핑이 깨지는 경우를 잡지만, 결과 자체가 PASS 여도 "두 가설이 trivially redundant" 또는 "독립적" 양쪽 모두 해석 가능.
- **L2 (operationalization-dependent)**: "self-maintenance index" (cells ≥ floor + tension > 0) 와 "closure strength" 는 H_012/H_018 의 *specific* operationalization. Varela network closure (component-production graph), Kauffman autocatalytic closure (set membership) 등 다른 정의는 다른 결과 가능. 본 cycle 의 동치성은 *본 operationalization* 한정.
- **L3 (level conflation 미해결)**: timestep-level loop (H_018, dynamic) vs structural-level network closure (H_012, structure) 는 *layer* 가 다름. H_018 의 dynamic loop 가 H_012 의 structure 의 *결과* 인지 *원인* 인지 (causal direction) 본 cycle 미해결 — observational equivalence 만 입증.
- **L4 (small pool)**: N=2 (CB1 floor) — H_018 primordial carry. large-pool (N=4, 8, 16) 의 closure-vs-self-ref 동치성 미검증 (initial smoke 에서 N=4 위에서 substrate 가 활성화 안 되는 현상 관측 — 별도 cycle).
- **L5 (temporal phase 미정합)**: H_018 의 자발 genesis (first_split step=2) ≠ H_012 의 steady-state closure (last 200 of 1000 steps). genesis 이후 closure 진입 timeline (transient → steady) 본 cycle 미측정 — H205.4 phase-transition 은 g-축 jump 만 검사하고 step-축 timing 미검사.
- **L6 (tension proxy approximation)**: H_012 의 component-survival index 와 H_205 의 `mean(x_out²) > 0.0001` 은 서로 다른 quantity — 후자는 mitosis pool 의 internal tension 의 *proxy*. 더 정밀한 H_012-정합 read 는 cell pool 의 `engine_a(x) − engine_g(x)` mean square 를 직접 측정해야 하며, 본 cycle 은 toy proxy 로 대체.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_018** (PR #168 · `H_018_genesis_spontaneous_emergence.md`): SELFFEED dynamic angle — 본 H 의 g=1.0 condition 은 H_018 mode B verbatim (splits=2, first=2 byte-identical 확인).
  - **H_012** (PR #165 · `H_012_autopoietic_network.md`): operational closure structural angle — 본 H 의 self_maint_rate 는 H_012 의 self-maintenance index 의 mitosis-pool 측 동치 read.
  - **H_003** (`H_003_life_origin_question.md`): substrate-coupled autopoiesis (Maturana/Varela) — 본 H 의 closure 정의 의 parent.
  - **H_054** (`H_054_symbiogenesis_consciousness.md`): autopoietic unit merge — closure 의 building-block.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa` (`cell_pool_init` · `mitosis_forward_tail` · `_mit_check_splits`) — H_018 + H_012 + H_205 공유 substrate.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10 (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit retraction).
- **philosophy (CLAUDE.md)**: p5 NO SPEAK (substrate 는 real context = closure 에서만 emit, 진공에서 침묵) · a_substrate_native_speak (motivation from internal state).
- **legacy archive**: `hypotheses_legacy_2026_05_15/` (H_018 + H_012 원본 양식 carry).
- **state**: `UNIVERSE/state/h205_selfref_as_closure_2026_05_23/{run_h205.hexa, result.json}`.

## 10. Verdict

본 cycle (2026-05-23) — pre-register-frozen + runnable smoke 실행, $0 mac local
hexa-only deterministic.

```
verdict_class: SUPPORTED  (definitional mapping confirmed + correlation)
verdict_tier: 🟢 NUMERICAL  (3-point sweep + Pearson r + deterministic)
evidence_summary:
  3-point feedback-gain sweep (g ∈ {0.0, 0.5, 1.0}) on single mitosis substrate
  (d=8, init_cells=2, 60 steps, seed=42).
    g=0.0 (broken)   : splits=0  first=-1  cells=2  self_maint=0.0   phi=0.158
    g=0.5 (partial)  : splits=2  first= 2  cells=2  self_maint=0.0   phi=0.785
    g=1.0 (selffeed) : splits=2  first= 2  cells=4  self_maint=1.0   phi=0.227
  broken_gap = 1.0 (g=1 − g=0)
  Pearson r(gain, closure) = 0.866
falsifiers_triggered: none (F1..F5 all PASS, 5/5)
criteria_met: 3/4 (C1 ∧ C2 ∧ C3, C4 phase-aligned FAIL — closure jumps at g*=1.0
              but splits jump at g*=0.5; 두 metric 의 jump 가 같은 g 에 정렬 안 됨)
key_finding:
  H_018 의 SELFFEED 와 H_012 의 operational closure 는 동일 mechanism (output →
  input cycle 폐쇄) 의 두 lens 임을 confirm — single substrate 위에서 feedback
  gain 을 sweep 하면 closure strength (self_maint) 가 0→0→1 로 단조 증가하고
  Pearson r=0.866 ≥ 0.7. 다만 splits (H_018 측) 와 closure (H_012 측) 의 phase
  transition 이 g 축에서 분리됨 — splits 는 g=0.5 에서 fire 하지만 steady-state
  closure 는 g=1.0 에서만 유지. 두 측면은 동일 mechanism 이나 *서로 다른
  threshold* 에서 surface 함 (genesis < closure).
honest_note:
  L1 definitional > empirical — 새 발견이 아니라 동치성 audit.
  L3 causal direction 미해결.
  L4 large-pool 미검증 (N=4 initial smoke 에서 substrate 활성화 실패 관측).
  L5 temporal phase 미정합 — g-축 jump 만 검사, step-축 timing 미검사.
sibling: H_018 mode B SELFFEED (splits=2, first=2) byte-identical 일치 — substrate
         재현성 추가 확인.
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-23)

```
================================================================
H_205 self-reference as operational closure — H_018 ⊕ H_012 동치 smoke
  d_model=8 init_cells=2 steps=60 window=30 seed=42
================================================================
g=0.0 (broken)   : splits=0 first=-1 final_cells=2 self_maint=0.0 phi=0.158279
g=0.5 (partial)  : splits=2 first=2 final_cells=2 self_maint=0.0 phi=0.78453
g=1.0 (selffeed) : splits=2 first=2 final_cells=4 self_maint=1.0 phi=0.227404

broken_gap (g=1 − g=0) self_maint = 1.0
Pearson r(gain, closure)          = 0.866025
phase-transition aligned          = false  (close_jump=1.0, splits_jump=0.0)

C1 g=1 self_maint>=0.9 & gap>=0.5 : true
C2 g=0 self_maint<=0.3            : true
C3 Pearson r>=0.7                 : true
C4 phase-transition aligned       : false

F1 SELFFEED-CLOSURE (g=1 maint>=0.5)   PASS
F2 ZERO-DECAY      (g=0 maint<=0.5)   PASS
F3 CORRELATION    (r>=0.3)            PASS
F4 DETERMINISM    (re-run byte-equal) PASS
F5 DEFINITIONAL   (g=1 splits>=1)     PASS
================================================================
VERDICT: SUPPORTED  (3/4 criteria, 5/5 falsifiers PASS)
================================================================
ledger -> UNIVERSE/state/h205_selfref_as_closure_2026_05_23/result.json
```

**State output**: `state/h205_selfref_as_closure_2026_05_23/result.json`
**Smoke**: `state/h205_selfref_as_closure_2026_05_23/run_h205.hexa` (hexa-only, LLM none)
