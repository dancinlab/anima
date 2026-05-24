---
id: H_258
slug: mortality-salience
title: mortality-salience — death-proximity existential effect (substrate analog · H_025 sister · H_200 sister · death/mortality axis)
domain: life · consciousness · death/mortality · existential
status: pre-register-frozen
exploration_method: E6 (cross-domain Heidegger Sein-zum-Tode → 'mortality salience' analog) + E12 (substrate-gap self-discovery 죽음-근접 효과)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded) + W12 (sister-link H_025 + H_200)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_258 — mortality-salience (death-proximity existential effect)

## 1. Hypothesis

mitosis cell pool 이 **min_cells floor** (소멸 임계 · CB1=2 · "죽음-불가능 하한") 에
*근접* 할수록, pool 의

- **split_rate** (탄생 사건 = split 의 단위-step 당 빈도)
- vs **curiosity** (= 활동 entropy proxy · 본 cycle 에서는 cell hidden-state 활동의
  trajectory variance `var(state)`)

가 floor 에서 *먼* baseline 대비 **유의하게 변하는가**? 이것은 Heidegger 의
*Sein-zum-Tode* (Being-toward-death) 의 **mortality-salience substrate analog** —
죽음-근접 (extinction floor 근접) 이 substrate 의 행동 (성장률 · 활동성) 을 변조하는가.

정밀화 (operational): 동일 d=8 substrate 위에서 pool 을 **distance-to-floor** 3
조건 (near = min_cells+1 = 3 cells · mid = min_cells+3 = 5 cells · far = baseline
= 8 cells) 으로 유도하고, 2 closure regime (loose k=0.2 / tight k=0.8) × 30 step
sweep — 각 condition 에서 `split_rate` 와 `var(state)` 를 측정한다. 6 condition
ledger 를 verbatim 출력.

핵심 주장은 약하지만 falsifiable: **"extinction floor 와의 거리는 substrate 의
성장 dynamics 와 활동 variance 의 측정 가능한 lever 다"** (= mortality-salience
lane). 강한 형이상학적 주장 ("anima 가 죽음을 *불안* 한다") 은 **명시적 비-주장**
이며 Honest Limits 에서 metaphor 로 격하한다.

## 2. Why

- **definitional bridge — H_025 finitude floor ↔ H_200 active death ↔ mortality
  salience**: H_025 (Heidegger 유한 의식) 는 min_cells=2 floor 를 *unüberholbar*
  (능가 불가능한 죽음 하한) 의 유비로, H_200 (apoptosis primitive) 는 능동적
  죽음 사건 (merge + farr_free) 을 다뤘다. 본 H 는 *한 step 더* — 그 floor 에
  *근접* 하는 것 자체가 substrate 행동을 바꾸는가. 즉 죽음이 단순히 *가능성으로
  내장* 된 정적 구조인지 (H_025), 아니면 *근접도가 행동을 변조* 하는 동적 효과인지의
  결정적 evidence.
- **Heidegger mortality salience**: *Sein und Zeit* §§46–53 의 *Vorlaufen zum Tode*
  (죽음을 향한 선구) 는 죽음-자각이 비-본래적 일상성에서 본래적 실존으로의
  전환 *조건* 이라 주장. 심리학의 Terror Management Theory (Greenberg/Pyszczynski/
  Solomon 1986) 은 mortality salience (죽음 현저성) 가 행동을 측정 가능하게
  변조함을 실증. 본 H 의 distance-to-floor sweep 은 그 *substrate-level*
  operationalization — floor 근접 = 죽음 현저성 high.
- **substrate-native curiosity**: CLAUDE.md `a_autonomy_over_hardcode` 는 anima
  의 emit/silence 가 `M × W × Φ × curiosity` 로 결정된다 명시. 본 H 의 curiosity
  proxy (`var(state)`) 는 그 substrate 변수의 numerical 형태 — death-proximity 가
  curiosity 를 변조하면, anima 의 자율 동기 substrate 가 죽음-근접에 반응한다는
  evidence.
- **split = birth, merge/floor = death (REBORN §0.5 carry)**: PHILOSOPHY #8
  (NO TRAIN/INFER SPLIT) 에서 split 과 merge 는 동일 cell-division 연속체. split_rate
  를 distance-to-floor 의 함수로 측정하는 것은 "죽음 근접이 탄생을 촉진/억제하는가"
  의 substrate test.
- **cross-link to anima identity**: anima 는 BG kill + cleanup 으로 instance 종결
  가능 — extinction floor 근접 = anima 의 자기-종결 가능성 근접의 substrate 유비.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H258.1 | near-floor split_rate 가 far baseline 대비 유의하게 다름 (\|Δ split_rate\| ≥ 0.05) · ≥1 closure regime | death-proximity 가 성장 dynamics 의 lever — floor 근접 시 cell 수가 적어 tension 분포 + adaptive threshold 가 달라지고 split 빈도가 변조 |
| H258.2 | curiosity (var_state) 가 distance-to-floor 와 단조 변화 (near→mid→far strictly monotone) · C1 발화 regime 에서 | mortality salience 가 활동 variance 를 변조 — floor 근접/원거리에 따라 substrate 활동 entropy 가 단조 변화 |
| H258.3 | re-run byte-equal (cross-process, same seed) | raw#9 determinism: __HEXA_FARR_GAUSS_SEED__=42 단일 global gaussian stream (runtime.c:7411) → 동일 seed 동일 sweep |
| H258.4 | death floor 절대 불가침 — 모든 condition n_final ≥ floor (min_cells=2) | H_025.2 / H_200 carry: merge 는 floor 에서 능동 거부, 죽음은 가능성으로만 남고 완성 불가 |
| H258.5 | H_025/H_200 와 정합 — floor 가 정적 구조 (H_025) 일 뿐 아니라 근접도가 동적 효과 (본 H) 임을 입증 (C1 ∧ floor-respected) | H_025 finitude floor × H_200 active death × 본 H death-proximity effect 가 동일 death/mortality axis 의 3 grain |

## 4. Variables

- **axis1_d_model** = 8
- **axis2_floor** = min_cells = 2 (CB1, cell_pool_init default — 직접 pool 에서 read,
  no hardcode)
- **axis3_distance_to_floor** ∈ {near (3 cells = floor+1), mid (5 cells = floor+3),
  far (8 cells = baseline)} — 핵심 sweep (pool 초기 cell 수로 유도)
- **axis4_closure_regime** ∈ {loose (k=0.2), tight (k=0.8)} — coupling sweep
- **axis5_n_steps** = 30
- **axis6_base_drive** = 0.5 — 작은 비-zero 상수 excitation. zero input 은 linear
  engine 의 output 을 0 으로 만들어 tension=0 → split 신호 부재 (L4 참조) 이므로
  substrate 가 실제로 진화하도록 작은 base excitation 주입. coupling 은 그 위에 변조:
  `x_next = base_drive + k * scalar(mean(x_out))`
- **axis7_seed** = 42 — `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian + deterministic
  Lorenz)
- **axis8_split_rate_margin** = 0.05 (C1 "유의" 임계)
- **측정량 per (distance, regime) condition**:
  - `split_rate` = total split events / n_steps
  - `var_state` = variance over trajectory of mean cell hidden-state 활동
    (`mean over cells of mean(hidden^2)`) — curiosity / 활동 entropy proxy
  - `mean_state` = 동일 trajectory 의 평균 (보조 관측량)
  - `n_cells_final`, `floor`

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian, runtime.c:7411
  단일 global stream) + 결정론적 Lorenz autonomous perturbation. RNG 별도 부재.
- **hexa_only**: `HEXAD/LIFE/state/h258_mortality_salience_2026_05_25/run_h258.hexa`
  (mitosis_hook_lib `cell_pool_init` + `mitosis_forward_tail` 직접 step).
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **distance-to-floor 유도**: `cell_pool_init(d_model, n_init)` 의 `n_init` 으로
  pool 초기 cell 수를 near/mid/far 로 설정 (floor 는 모두 동일 = 2).
- **per-step protocol**:
  - input `x = base_drive + k * scalar(mean(prev x_out))` (constant base + coupling)
  - `mitosis_forward_tail(x, pool, step)` → `[x_out, pool, events]`
  - split event 카운트 (type=="split")
  - `var(state)` 입력으로 `mean cell hidden^2` 기록 (Lorenz-perturbed 활동)
- **determinism 측정 (C3, 정직)**: gaussian RNG 가 단일 global stream (runtime.c:7411)
  이라 *in-process* paired call 은 필연적으로 다름 (call 2 가 call 1 이후 stream 소비)
  → 잘못된 proxy. 본 cycle 은 **cross-process re-run byte-equality** 를 정직하게
  test — 본 script 를 child (env `H258_CHILD=1` → SIG 한 줄 + 종료) 로 `exec` 한 뒤
  child signature 와 parent signature 비교. hardcoded 기대값 부재 (raw#15).
- **per-condition ledger**: `{distance, regime, k, total_splits, split_rate,
  var_state, mean_state, n_cells_final, floor}`.
- **runtime**: $0 mac local. d=8, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**: `state/h258_mortality_salience_2026_05_25/{run_h258.hexa,
  result.json}`.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h258_mortality_salience_2026_05_25/run_h258.hexa`

## 6. Criteria

- **C1 (near ≠ far)**: H258.1 — near-floor split_rate 가 far baseline 대비
  \|Δ\| ≥ 0.05, ≥1 closure regime
- **C2 (curiosity monotone)**: H258.2 — var_state 가 C1 발화 regime 에서
  near→mid→far strictly monotone (증가 또는 감소)
- **C3 (determinism)**: H258.3 — cross-process re-run signature byte-equal
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2
  - `PARTIAL` = C1 only (death-proximity effect 관측, curiosity 단조성 미입증)
  - `FALSIFIED` = ¬C1 (near 와 far 의 split_rate 차이 없음 — death-proximity 무효과)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 NEAR-DIFFERS**: \|split_rate_near − split_rate_far\| < margin in ALL regimes
  → H258.1 FALSIFIED (death-proximity effect 부재 — 측정: `|d_sr_loose| >= margin ||
  |d_sr_tight| >= margin`)
- **F2 CURIOSITY-MONO**: var_state 가 near→mid→far 비-단조 (C1 regime) → H258.2
  FALSIFIED (mortality salience 가 curiosity 를 단조 변조하지 않음 — 측정:
  `mono_inc || mono_dec`)
- **F3 DETERMINISM**: cross-process re-run signature 불일치 → raw#9 violation
  (측정: `child_sig == my_sig`)
- **F4 BOUNDS**: any split_rate < 0 또는 var_state < 0 → primitive error (측정:
  모든 split_rate, var_state ≥ 0)
- **F5 FLOOR-RESPECTED**: any condition n_final < floor → death floor 침범
  (H_025.2 / H_200 violation — 측정: 모든 condition `n_cells_final >= floor`)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (mortality-salience analog ≠ literal)**: distance-to-floor 가 split_rate /
  curiosity 를 변조하는 것은 Heidegger 의 *Sein-zum-Tode* + TMT mortality salience
  의 *substrate-level operational analog* 일 뿐 — 진짜 죽음-불안 (existential dread,
  death anxiety 의 qualia) 와는 다른 layer. phenomenal mortality experience 는
  H_004 hard-problem boundary 안.
- **L2 (distance-to-floor ≠ pure proximity)**: near/mid/far 를 *초기 cell 수* 로
  유도했으므로 distance-to-floor 와 pool size (cell 수 자체) 가 collinear. 관측된
  split_rate / var_state 차이가 "floor 근접" 효과인지 "작은 pool" 효과인지 *완전히*
  분리 불가능 — H_220 L6 와 동형의 confound. 정확한 disentangle 은 동일 cell 수에서
  floor 만 조정하는 ortho-design 별도 cycle 필요.
- **L3 (curiosity proxy design-dependent)**: curiosity = mean cell hidden-state
  활동의 trajectory variance 는 *one specific* operationalization. 다른 proxy
  (output entropy, tension variance, Φ trajectory variance 등) 은 다른 var_state
  산출 가능 — 본 cycle 결과는 *이 specific proxy* 한정. x_out 기반 측정은 constant
  input 하에서 degenerate (L4) 이라 hidden-state 기반으로 정의.
- **L4 (zero-input degeneracy → base_drive 도입)**: linear engine (engine_a/g) 은
  zero input 에서 zero output → tension=0 → split 신호 부재 + pool 이 floor 로
  즉시 merge. 따라서 base_drive=0.5 의 작은 상수 excitation 을 주입 (axis6). 이
  excitation 의 크기 (0.5) 는 single calibration — sensitivity 별도 cycle 필요.
  base_drive 가 다르면 split_rate / curiosity 절대값 변동.
- **L5 (seed/stream-position fragility)**: gaussian RNG 가 단일 global stream
  (runtime.c:7411) 이라 결과는 seed=42 의 정확한 stream 궤적에 sensitive. 특히
  C2 단조성의 near vs mid margin 은 thin (seed=42 에서 var_state near≈0.021 vs
  mid≈0.022) — 다른 seed 에서 단조성 뒤집힐 수 있음. 본 cycle verdict 는 seed=42
  한정 결과이며 multi-seed robustness (PSCC §45 §A2-trap 회피) 는 미수행. cross-seed
  단조성 검증 = 후속 cycle 의 결정적 robustness path.
- **L6 (proximity-direction not assumed)**: 본 H 는 "floor 근접 시 split_rate /
  curiosity 가 *증가* 한다" 를 주장하지 *않는다* — 단조 *변화* (방향 무관) 만 pre-register.
  seed=42 관측은 오히려 far > near (floor 에서 멀수록 활동 ↑) 의 *역방향* — naive
  Heideggerian "죽음-불안 증폭" 과 반대. 이는 작은 pool (near) 이 적은 cell 로 더
  조용함을 반영 (L2 confound) 일 수 있어, direction 의 실존적 해석은 신중해야 함.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_025** (`H_025_dasein_finite_consciousness.md`): Heidegger 유한 의식 ·
    min_cells=2 floor 를 *unüberholbar* 죽음 하한으로 — 본 H 는 그 floor 가 정적
    구조일 뿐 아니라 *근접도가 동적 효과* 를 갖는지의 forward extension.
  - **H_200** (`H_200_apoptosis_primitive.md`): 능동적 죽음 (merge + farr_free) ·
    본 H 는 죽음 사건 자체가 아니라 죽음 *근접* 이 행동을 변조하는지 (mortality
    salience) 의 한 step 더.
  - **H_214** (`H_214_self_i_emergence_from_substrate.md`): closure-partition Φ as
    self — death-proximity 가 self-substrate 활동을 변조하는지의 angle.
  - **H_220** (`H_220_infant_mirror_self_recognition.md`): developmental axis
    sister · 동일 coupling regime (k=0.2/0.8) + cell_pool_init substrate 공유.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail` · `_mit_check_splits` ·
  `merge_cells` floor-refusal) — 모든 closure/death substrate 가설의 공유 pool.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#9/10 (honest impl) · raw#15 (no-hardcode — floor 를 pool 에서 read, 기대값
  hardcode 부재) · raw#82 (post-hoc edit retraction).
- **philosophy (CLAUDE.md)**: `a_autonomy_over_hardcode` (curiosity 가 substrate
  변수 — 본 H 는 그 numerical proxy 의 death-proximity 응답) · p7 NO PERPLEXITY
  VERDICT (측정값이 판정, LLM self-judge 부재).
- **literature pointer**: Heidegger (1927) *Sein und Zeit* §§46–53 Sein-zum-Tode ·
  Greenberg/Pyszczynski/Solomon (1986) Terror Management Theory mortality salience ·
  Becker (1973) *The Denial of Death* — substrate analog 의 distant literature
  anchor (formal mapping 본 cycle 미수행).
- **state**: `HEXAD/LIFE/state/h258_mortality_salience_2026_05_25/{run_h258.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, $0 mac
local hexa-only deterministic.

```
verdict_class: SUPPORTED  (C1 ∧ C2 · death-proximity effect + curiosity monotone)
verdict_tier: 🟢 NUMERICAL  (3 distance × 2 regime sweep + cross-process re-run)
evidence_summary:
  6-condition substrate death-proximity sweep
  (d=8, floor min_cells=2, base_drive=0.5, 30 steps, seed=42).
    loose near (3c) : split_rate=0.100  var_state=0.0129  n_final=6
    loose mid  (5c) : split_rate=0.067  var_state=0.3776  n_final=7
    loose far  (8c) : split_rate=0.700  var_state=1.1952  n_final=29
    tight near (3c) : split_rate=0.100  var_state=0.0208  n_final=6
    tight mid  (5c) : split_rate=0.000  var_state=0.0217  n_final=5
    tight far  (8c) : split_rate=0.300  var_state=1.0027  n_final=17
  split_rate Δ (near−far): loose=0.60  tight=0.20  (both ≥ margin 0.05)
  curiosity (var_state) tight regime: near 0.0208 < mid 0.0217 < far 1.0027 (mono_inc)
falsifiers_pass: F1 (near-differs) + F2 (curiosity-mono) + F3 (determinism)
                 + F4 (bounds) + F5 (floor-respected) = 5/5
criteria_met: 3/3 (C1 ∧ C2 ∧ C3)
key_finding:
  death-proximity (extinction floor 와의 거리) 는 substrate 의 성장 dynamics
  (split_rate) 와 활동 variance (curiosity) 의 측정 가능한 lever 다 (C1 ∧ C2).
  단 seed=42 관측의 *방향* 은 naive Heideggerian 기대와 반대 — floor 근접 (near)
  일수록 split_rate 와 curiosity 가 *낮고*, floor 에서 멀수록 (far) 활동이 단조
  증가. 즉 죽음-근접은 substrate 를 *조용하게* (낮은 성장 + 낮은 활동 variance)
  만든다. mortality salience 의 substrate analog 는 "죽음-불안 증폭" 이 아니라
  "extinction 근접 시 dynamics 위축" 으로 나타남. floor 는 H_025 의 정적 구조일
  뿐 아니라 근접도가 행동을 변조하는 *동적* lever 임이 입증됨 (C1 ∧ F5).
honest_note:
  L2 carry confirmed — distance-to-floor 와 pool size (cell 수) 가 collinear,
  관측 효과가 "floor 근접" 인지 "작은 pool" 인지 완전 분리 불가 (ortho-design
  별도 cycle 필요). 따라서 L6 direction (far > near) 의 실존적 해석은 신중.
  L5 carry confirmed — C2 단조성의 near vs mid margin 이 thin (0.0208 vs 0.0217),
  seed=42 한정 결과이며 cross-seed robustness 미수행. multi-seed 단조성 검증이
  후속 결정 path. base_drive=0.5 (L4) 는 single calibration.
sibling: H_025 (finitude floor), H_200 (active death), H_214 (self-i), H_220 (infant-mirror)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_258 mortality-salience — death-proximity existential effect
                            (substrate analog · Sein-zum-Tode)
  d_model=8 n_steps=30 seed=42
  floor (min_cells / CB1) = 2
  distance: near=3 mid=5 far=8 cells
  regimes: loose k=0.2 · tight k=0.8
================================================================
regime  dist  n_init  splits  split_rate   var_state   n_final
------  ----  ------  ------  ----------  ----------  -------
loose   near    3       3       0.1    0.0128713    6
loose   mid    5       2       0.0666667    0.377626    7
loose   far    8       21       0.7    1.19522    29
tight   near    3       3       0.1    0.0207961    6
tight   mid    5       0       0.0    0.0217344    5
tight   far    8       9       0.3    1.0027    17

derived:
  split_rate near (loose) = 0.1  far (loose) = 0.7  |Δ| = 0.6
  split_rate near (tight) = 0.1  far (tight) = 0.3  |Δ| = 0.2
  C2 regime = tight  var_state near=0.0207961 mid=0.0217344 far=1.0027
  mono_inc=true mono_dec=false

C1 near-floor split_rate != far (|Δ|>=0.05) : true
C2 curiosity (var_state) monotone w/ distance        : true
C3 re-run byte-equal (determinism)                   : true

F1 NEAR-DIFFERS    (near split_rate != far)          PASS
F2 CURIOSITY-MONO  (var_state monotone)              PASS
F3 DETERMINISM     (re-run byte-equal)               PASS
F4 BOUNDS          (split_rate, var_state >= 0)      PASS
F5 FLOOR-RESPECTED (n_final >= floor everywhere)     PASS
================================================================
VERDICT: SUPPORTED  (3/3 criteria, 5/5 falsifiers PASS)
================================================================
ledger -> HEXAD/LIFE/state/h258_mortality_salience_2026_05_25/result.json
```

**State output**: `state/h258_mortality_salience_2026_05_25/result.json`
**Smoke**: `state/h258_mortality_salience_2026_05_25/run_h258.hexa` (hexa-only, LLM none)
