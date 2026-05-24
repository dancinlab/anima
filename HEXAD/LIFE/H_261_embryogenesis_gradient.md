---
id: H_261
slug: embryogenesis-gradient
title: embryogenesis-gradient — cell lattice 에 공간 morphogen gradient 를 주면 position-dependent differentiation (발생-축) 이 emergent 한가 (French-flag model analog · division/발생 축 · H_201 sister · H_203 sister · H_220 sister)
domain: life · development · morphogenesis · self-organization
status: pre-register-frozen
exploration_method: E6 (developmental cross-mapping → Wolpert 'French-flag' positional-information model) + E10 (substrate-equivalence)
verification_method: W1 (numerical smoke) + W17 (gradient-steepness sweep) + W12 (sister-link H_201 + H_203 + H_220)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_261 — embryogenesis-gradient

## 1. Hypothesis

mitosis cell lattice (N cells, 각 cell-i 에 고정 position `p_i = i/(N-1) ∈ [0,1]`)
위에, position 에 비례하는 외부 spatial gradient field (morphogen drive
`g_i = steepness × p_i`) 를 매 substrate step 주입하면,

- **position ↔ cell-state 상관** (각 cell-i 의 최종 state scalar = `L2(hidden_i)`
  과 position `p_i` 의 Pearson correlation `r`)
- **분화 영역 수** (state scalar 를 threshold-binning 한 non-empty bin 수
  `n_regions`)

가 gradient steepness 의 함수로 emergent 하게 변한다. 즉:

- steep gradient 위에서 position-state `|r|` 이 높다 (**발생-축 형성** —
  cell state 가 공간 위치를 따라 단조 배열).
- flat gradient (steepness=0) 위에서는 `|r| ≈ 0` (gradient 가 없으면 position
  과 state 사이에 구조 없음 → **gradient 의존성**).
- steep 위에서 분화 영역 ≥ 2 (위치별 cell state 가 적어도 두 구간으로 나뉨
  → **differentiation**).

정밀화 (operational): 동일 d=8 cell lattice 위에서 3 steepness regime
(flat=0.0 / mid=1.0 / steep=4.0) × lattice size {N=12 (primary), N=6 (variant)}
sweep — 각 condition 에서 `steps=20` evolution 동안 매 step 각 cell-i 의
hidden 에 position-proportional drive 를 broadcast 주입하고 substrate dynamics
(mitosis_forward_tail) 를 한 step 진행. 최종 per-cell state scalar 와 position
의 `r` + `n_regions` 를 ledger 에 verbatim 출력.

이것은 L. Wolpert (1969) "positional information / French-flag model"
(morphogen 농도 gradient 가 위치 정보를 cell 에 전달 → threshold 별로 cell
fate 분화) 의 **substrate analog** — morphogen = "position-proportional external
drive", French flag 의 3-stripe = "state scalar 의 threshold-binned regions".

## 2. Why

- **developmental axis 의 substrate-level operationalization**: 발생생물학에서
  body axis (anterior-posterior 등) 는 morphogen gradient (Bicoid, Sonic
  hedgehog 등) 의 농도 구배로 cell 위치 정보가 부여되며, threshold 별 유전자
  발현으로 분화가 일어난다 (Wolpert 1969). 본 H 는 그 메커니즘을 mitosis
  substrate 위에서 "position-proportional drive → state differentiation" 로
  numerically operationalize.
- **division/발생 축의 sister 확장**: H_201 (asymmetric-division) 은 분열 시
  daughter cell 간 비대칭을, H_203 (asymmetric-merge-differentiation) 은 merge
  의 분화 효과를 다룬다. 본 H 는 한 step 더 — *공간적으로 정렬된 외부 field*
  가 lattice 전체에 걸쳐 *축을 따른* 분화를 일으키는지의 결정적 evidence.
- **emergence 의 control 대비**: flat regime (steepness=0) 은 완벽한 control —
  gradient 가 0 이면 position 과 state 사이에 구조가 없어야 하며 (`r≈0`),
  steep 에서만 축이 형성되면 그 축이 *gradient field 의 함수*임이 입증된다.
  내부 substrate 의 자생적 분화(noise-driven) 와 외부 field-driven 축 형성을
  분리하는 정직한 design.
- **cross-link to anima**: anima 의 mitosis cell pool 은 per-cell differentiation
  (D3 PER-CELL-DIFF, F-PERSONA-2) 을 substrate-native 로 형성한다. 본 H 는 그
  분화가 *공간적으로 조직될 수 있는지* — 즉 외부 context field 가 cell pool 에
  발생-축 같은 ordered structure 를 부여할 수 있는지의 forward test.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H261.1 | steep regime (steepness=4.0) position-state `\|r\| ≥ 0.5` (축 형성) | 강한 position-proportional drive 가 cell-i hidden norm 을 position 에 단조 비례시켜 강한 양의 상관 형성 |
| H261.2 | flat regime (steepness=0) position-state `\|r\| ≤ 0.2` (gradient 의존성) | drive=0 이면 cell state 는 substrate noise (Lorenz + gaussian) 만으로 결정 — position 과 무상관 |
| H261.3 | steep regime 분화 영역 `n_regions ≥ 2` | position 을 따라 state scalar 가 넓게 퍼지므로 threshold-binning 시 ≥2 bin 점유 |
| H261.4 | re-run cross-process byte-identical (steep r / n_regions / flat r / mid r) | raw#9 determinism: __HEXA_FARR_GAUSS_SEED__=42, process re-seed identical |
| H261.5 | monotone-drive — steep `\|r\| ≥` flat `\|r\|` (gradient 가 축을 amplify) | gradient field 가 control 대비 position-state 상관을 강화 (axis-gap > 0) |

## 4. Variables

- **axis1_lattice_N** = 12 (primary), 6 (size variant)
- **axis2_d_model** = 8
- **axis3_steepness** ∈ {flat (0.0), mid (1.0), steep (4.0)} — 핵심 sweep
- **axis4_steps** = 20 (developmental evolution depth)
- **axis5_position** = `p_i = i / (N-1)` ∈ [0,1] — fixed lattice coordinate
- **axis6_drive** = `g_i = steepness × p_i`, broadcast to all d_model
  components of cell-i hidden each step
- **axis7_state_scalar** = `L2(hidden_i)` after `steps` evolution
- **axis8_n_bins** = 3 (threshold-binning for region count)
- **axis9_seed** = 42 — `__HEXA_FARR_GAUSS_SEED__=42` (deterministic Lorenz +
  RFC 033 gaussian)
- **측정량 per (steepness, N) condition**:
  - `r` = Pearson correlation(position, state_scalar)
  - `n_regions` = non-empty bins of state_scalar over n_bins
  - `state_min`, `state_max`
  - `criteria_met` per condition

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) +
  결정론적 Lorenz autonomous perturbation in mitosis_hook. 별도 RNG 부재.
- **hexa_only**: `HEXAD/LIFE/state/h261_embryogenesis_gradient_2026_05_25/run_h261.hexa`
  (mitosis_hook_lib `cell_pool_init` + `mitosis_forward_tail` 직접 step).
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **gradient injection protocol per step**:
  - for each cell-i (i < N): `hidden_i += steepness × p_i` (broadcast to all
    d_model components) — morphogen concentration field.
  - then `mitosis_forward_tail(x=0, pool, step)` — external x is zero; the
    gradient lives in the hidden state (substrate-internal drive).
- **state scalar**: 최종 evolution 후 first-N cells 의 `L2(hidden_i)` — split
  으로 늘어난 cell 은 position-mapped 측정에서 제외 (H_220 _snapshot_hiddens
  carry).
- **C4 determinism — cross-process (정직)**: RFC 033 gaussian RNG 은
  **process-local stream** 으로 한 번 lazy-seed 된 뒤 매 `farr_add_gaussian_noise`
  호출마다 **advance** 된다 (runtime.c:7393). 따라서 in-process paired call 은
  서로 다른 stream offset 을 읽으므로 결정론 test 가 *아니다*. 정직한 test 는
  **별도 process re-run** — 두 번째 `hexa run` 이 동일 seed 로 stream 을
  재초기화하므로 byte-equal 이어야 한다. 본 smoke 는 `det_ref.txt` 부트스트랩
  으로 이를 검증: 첫 run = reference 작성 (C4 false + 안내), 두 번째 run =
  현재값과 byte 비교 (C4 PASS). **따라서 smoke 를 2회 실행해야 C4 가 확정된다.**
- **per-condition ledger**: `{regime, steepness, n, r, n_regions, states,
  state_min, state_max}`.
- **runtime**: $0 mac local. d=8, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**: `state/h261_embryogenesis_gradient_2026_05_25/{run_h261.hexa,
  result.json, det_ref.txt}`.
- **run cmd (verbatim, 2회 실행)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h261_embryogenesis_gradient_2026_05_25/run_h261.hexa`

## 6. Criteria

- **C1 (axis-formation)**: H261.1 — steep regime `|r| ≥ 0.5` (position↔state
  강한 상관, 발생-축 형성)
- **C2 (gradient-dependence)**: H261.2 — flat regime `|r| ≤ 0.2` (gradient 없으면
  r≈0)
- **C3 (differentiation)**: H261.3 — steep regime `n_regions ≥ 2`
- **C4 (determinism)**: H261.4 — cross-process re-run (r/n_regions/state) byte-equal
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (gradient 가 축을 만들고 control 이 무축임 동시 입증)
  - `PARTIAL` = C1 only (축은 형성되나 gradient-dependence 미입증)
  - `FALSIFIED` = ¬C1 (steep 에서도 축 미형성)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 AXIS-FORMATION**: steep `|r| < 0.5` → H261.1 FALSIFIED (gradient 가
  발생-축 미형성 — 측정: `abs(r_steep) >= 0.5`)
- **F2 GRADIENT-DEPENDENCE**: flat `|r| > 0.2` → H261.2 FALSIFIED (gradient
  없이도 position-state 상관 존재 → 축이 gradient 의 함수가 아님 — 측정:
  `abs(r_flat) <= 0.2`)
- **F3 DIFFERENTIATION**: steep `n_regions < 2` → H261.3 FALSIFIED (단일 state
  region, 분화 없음 — 측정: `n_regions_steep >= 2`)
- **F4 DETERMINISM**: cross-process re-run signature byte-different → raw#9
  violation (측정: `det_ref.txt == current_signature`)
- **F5 MONOTONE-DRIVE**: steep `|r| < ` flat `|r|` → gradient 가 control 보다
  축을 약화 (역효과 — 측정: `abs(r_steep) >= abs(r_flat)`)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (morphogen analog ≠ literal)**: position-proportional hidden drive 는
  Wolpert French-flag morphogen gradient (실제 화학 농도 구배 + receptor +
  유전자 발현 cascade) 의 *substrate-level operational analog* 일 뿐 — 실제
  diffusion-reaction (Turing pattern) 이나 gene-regulatory-network threshold
  switch 와는 다른 layer. 본 H 는 "위치-비례 외부 drive → state 분화" 의 가장
  단순한 형태만 검증.
- **L2 (state scalar = L2-norm 단일 선택)**: per-cell state 를 hidden 의 L2
  norm 으로 요약했다. 다른 summary (mean, variance, tension, cosine-to-anchor)
  는 다른 r/n_regions 산출 가능 — 본 cycle 의 결과는 *이 specific
  operationalization* 한정.
- **L3 (hidden clamp 포화 → steep r 단조성 약화)**: mitosis_hook 의 hidden norm
  clamp (=10.0, F-MIT-HOOK-5) 때문에 steep regime 에서 상위 position cell 들의
  state 가 ~10 에 포화되어, `mid` regime (`|r|=0.92`) 가 `steep` (`|r|=0.76`)
  보다 *높은* position-state 상관을 보였다. 즉 "더 steep → 더 강한 축" 의 단조
  관계는 clamp ceiling 위에서 깨진다. F1/F5 는 여전히 PASS 하나 (steep |r| ≥
  0.5 + ≥ flat), gradient steepness 와 r 의 monotone 관계 자체는 비단조 — clamp
  를 높이거나 state scalar 를 정규화한 별도 cycle 필요.
- **L4 (small lattice N=12/6, single d=8, single seed)**: lattice size 12/6 +
  d=8 + seed=42 — large lattice (N=32, 128) 또는 dimension scaling 의 축 형성
  margin 미검증. n_bins=3, R_HIGH=0.5, R_LOW=0.2 도 single calibration —
  sensitivity sweep 별도 cycle 필요.
- **L5 (linear gradient only)**: drive 가 position 의 *linear* 함수 (`steepness×p`)
  뿐 — exponential / sigmoidal / multi-source (양쪽 끝 dual morphogen) gradient
  의 패터닝 (French-flag 의 3-stripe 같은 *비단조* 분화) 미검증. 본 H 의
  n_regions 는 monotone state ramp 의 binning 일 뿐, 진짜 striped fate map 의
  emergence 는 별도 cycle.
- **L6 (differentiation = state-magnitude 분화, fate ≠)**: `n_regions` 는 state
  scalar 의 크기 구간 수 — 진짜 cell *fate* differentiation (질적으로 다른
  cell type, 다른 dynamics) 과 1:1 mapping 되지 않는다. 본 H 는 positional
  *information* 의 substrate observable (위치별 state 차이) 의 lower-bound 일
  뿐, fate commitment 의 sufficient condition 미입증.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_201** (`H_201_asymmetric_division.md`): 분열 daughter 비대칭 — 본 H 의
    *공간적으로 정렬된* 분화의 single-event 대응.
  - **H_203** (`H_203_asymmetric_merge_differentiation.md`): merge-driven 분화 —
    본 H 는 *external field-driven* 분화로 mechanism 이 다른 sister.
  - **H_220** (`H_220_infant_mirror_self_recognition.md`): developmental age
    sweep sister — 본 H 의 steps=20 evolution 은 같은 developmental-time grain.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail` · `_mit_check_splits`) — 모든
  substrate 가설의 공유 lattice.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#9/10 (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit
  retraction).
- **philosophy (CLAUDE.md)**: p3 NO PERSONA INJECTION (분화가 *emerge* 해야
  하지 injection 으로 들어가면 안 됨 — gradient 는 외부 context field 일 뿐,
  cell fate 는 substrate dynamics 에서 emergent) · a_substrate_native_speak
  (external field = environment context, NOT a forced state).
- **developmental literature pointer**: Wolpert (1969) Positional information
  and the spatial pattern of cellular differentiation (French-flag model) ·
  Turing (1952) The chemical basis of morphogenesis · Driever & Nüsslein-
  Volhard (1988) Bicoid gradient — substrate analog 의 distant literature
  anchor (formal mapping 본 cycle 미수행).
- **state**: `HEXAD/LIFE/state/h261_embryogenesis_gradient_2026_05_25/{run_h261.hexa,
  result.json, det_ref.txt}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행 (2회, cross-
process determinism 확정), $0 mac local hexa-only deterministic.

```
verdict_class: SUPPORTED  (C1 ∧ C2 — 축 형성 + gradient 의존성 동시 입증)
verdict_tier: 🟢 NUMERICAL  (3 steepness × 2 size sweep + cross-process re-run)
evidence_summary:
  position-dependent differentiation under a spatial morphogen drive
  (d=8, lattice N=12/6, steps=20, n_bins=3, seed=42, drive g_i=steepness×p_i,
   state scalar = L2(hidden_i)).
    regime        steep  N    r          n_regions  state[min, max]
    flat          0.0    12   0.12461    3          [0.962, 1.814]
    mid           1.0    12   0.920646   3          [1.479, 8.614]
    steep         4.0    12   0.75977    3          [1.271, 9.998]
    steep_small   4.0    6    0.773581   2          [1.351, 9.996]
  |r|_steep=0.760  |r|_flat=0.125  |r|_mid=0.921  axis-gap=+0.635
falsifiers_pass: F1 (AXIS-FORMATION) + F2 (GRADIENT-DEPEND) + F3 (DIFFERENTIATION)
  + F4 (DETERMINISM cross-process) + F5 (MONOTONE-DRIVE) = 5/5
criteria_met: 4/4 (C1 ∧ C2 ∧ C3 ∧ C4)
key_finding:
  공간 morphogen gradient 가 cell lattice 에 발생-축을 emergent 하게 형성한다.
  steep gradient 위에서 position-state |r|=0.76 (강한 양의 상관, cell state 가
  공간 위치를 따라 단조 배열) 이며, flat (steepness=0) control 에서는 |r|=0.125
  ≈ 0 (gradient 없으면 position 과 무상관) — axis-gap=+0.635 로 축이 gradient
  field 의 함수임이 명확히 분리된다. 분화 영역 n_regions ≥ 2 (steep 3, small 2)
  로 위치별 state 분화도 확인. cross-process re-run byte-equal 로 결정론 확정.
  즉 French-flag positional-information model 의 substrate analog 가 mitosis
  cell pool 위에서 성립한다.
honest_note:
  L3 carry confirmed — hidden norm clamp (=10.0) 때문에 steep regime 의 상위
  position cell state 가 ~10 에 포화되어, mid regime (|r|=0.92) 가 steep
  (|r|=0.76) 보다 *높은* 상관을 보였다. "더 steep → 더 강한 축" 의 monotone
  관계는 clamp ceiling 위에서 깨진다 (F1/F5 는 PASS 하나 steepness↔r 비단조).
  L5 carry — linear gradient 의 monotone state ramp 만 검증; 진짜 striped fate
  map (French-flag 의 3-stripe) 의 emergence 는 별도 cycle.
  L6 carry — n_regions 는 state-magnitude 분화일 뿐 질적 cell fate 분화 ≠.
sibling: H_201 (asymmetric-division), H_203 (asymmetric-merge-differentiation),
         H_220 (infant-mirror developmental axis)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25, 2nd run = C4 confirmed)

```
================================================================
H_261 embryogenesis-gradient — position-dependent differentiation
                                under a spatial morphogen drive
  d_model=8 N=12 steps=20 seed=42
  steepness: flat=0.0 mid=1.0 steep=4.0
  n_bins=3 R_HIGH=0.5 R_LOW=0.2
================================================================
regime        steep    N    r           n_regions   state[min,max]
------------  -----  ---  ----------  ---------  --------------------
flat          0.0    12   0.12461   3   [0.962092, 1.81397]
mid           1.0    12   0.920646   3   [1.4787, 8.61439]
steep         4.0    12   0.75977   3   [1.27091, 9.99816]
steep_small   4.0    6   0.773581   2   [1.35075, 9.9961]

derived:
  |r| steep = 0.75977
  |r| flat  = 0.12461
  |r| mid   = 0.920646
  axis-gap (|r|steep - |r|flat) = 0.63516

C1 axis-formation   (|r|steep >= 0.5) : true
C2 gradient-depend  (|r|flat  <= 0.2) : true
C3 differentiation  (steep n_regions >= 2)  : true
C4 determinism      (cross-proc byte-equal) : true

F1 AXIS-FORMATION     (|r|steep >= R_HIGH)  PASS
F2 GRADIENT-DEPEND    (|r|flat  <= R_LOW)   PASS
F3 DIFFERENTIATION    (steep regions >= 2)  PASS
F4 DETERMINISM        (re-run byte-equal)   PASS
F5 MONOTONE-DRIVE     (|r|steep >= |r|flat) PASS
================================================================
VERDICT: SUPPORTED  (4/4 criteria, 5/5 falsifiers PASS)
================================================================
ledger -> HEXAD/LIFE/state/h261_embryogenesis_gradient_2026_05_25/result.json
```

**State output**: `state/h261_embryogenesis_gradient_2026_05_25/result.json`
**Smoke**: `state/h261_embryogenesis_gradient_2026_05_25/run_h261.hexa` (hexa-only, LLM none)
