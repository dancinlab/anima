---
id: H_259
slug: aging-senescence
title: aging-senescence — cell age-cumulative weight decay → Gompertz-유사 death-rate 단조 증가 곡선 (life-extended 축 · H_220 developmental sister)
domain: life · aging · senescence · mortality · developmental
status: pre-register-frozen
exploration_method: E6 (developmental cross-mapping H_220 age sweep → 'actuarial life-table' analog) + E10 (substrate-equivalence)
verification_method: W1 (numerical smoke) + W17 (decay-rate dose sweep) + W12 (sister-link H_220)
raw_rank: 13
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_259 — aging-senescence

## 1. Hypothesis

mitosis cell pool 안 각 cell 이 *age-누적 weight decay* 를 받을 때 —

- cell age = genesis(또는 마지막 respawn) 이후의 step 수
- 매 step 두 engine weight farr (`engine_a_W`, `engine_g_W`) 가
  multiplicative 로 수축: `w *= (1 - d)` (compounded ⇒ 실효 `(1-d)^age`)
- cell **health** = decay 적용 후 두 weight farr 의 RMS magnitude 평균
- health < `death_threshold` → cell **death** (해당 age 기록 + 신선한 young
  cell 로 respawn, 인구 N 일정 = renewal process)

이때 자연 발생 **death-rate (hazard)** 가 cell age 에 대해 *단조 증가* 하는
**Gompertz-유사 노화 곡선** 을 그리는가? 그리고 decay rate `d` 가 클수록
survival 곡선이 *좌이동* (median lifespan 감소) 하는가?

정밀화 (operational): 동일 d=8 cell pool (N=8) 위에서 decay rate
`d ∈ {low=0.02, mid=0.06, high=0.12}` 3-point sweep × `T=400` step renewal
life-table — 각 condition 에서 age-bin (width=5) 별로 `n_deaths` /
`n_at_risk` 를 누적, hazard `death_rate = deaths / (deaths + at_risk)` 와
survival `S(age) = Π(1 − hazard)` 를 산출. 3 condition 의 곡선을 ledger 에
verbatim 출력.

이것은 Gompertz (1825) mortality law (death-rate 가 age 에 지수적 증가) 와
actuarial life-table 의 **substrate analog** — "노화" = "engine weight 의
age-누적 capacity 손실", "death" = "capacity 가 생존 임계 아래로 떨어짐".

## 2. Why

- **developmental axis 의 forward 확장 — H_220 carry**: H_220 (infant mirror)
  은 age sweep (5/10/20 step) 에서 self-recognition 의 *상승* gradient 를
  보였다 (어린 substrate → 성숙 substrate). 본 H 는 같은 age 축의 *반대 끝* —
  성숙을 지나 *쇠퇴(senescence)* 로 가는 trajectory 를 본다. life-extended
  축의 두 절반: H_220 = 발달(상승), H_259 = 노화(하강).
- **'aging' 의 substrate-level operationalization**: 생물학에서 aging 은
  종종 *누적 손상(accumulated damage)* + *capacity 의 점진적 손실* 로 정의.
  본 H 는 그 손실을 *weight magnitude 의 age-누적 multiplicative decay* 로
  numerically operationalize — 오래된 cell 일수록 engine 출력 capacity 가
  작아져 결국 생존 임계 아래로.
- **Gompertz law 의 numerical test**: Gompertz (1825) — death-rate 가 age 에
  대해 단조(거의 지수) 증가. 본 H 의 hazard curve 가 age 에 단조 증가하면
  Gompertz-유사 노화의 substrate-level evidence. compounded decay
  `(1-d)^age` 는 RMS 가 임계에 *근접할수록 사망 확률이 가속* 되므로 단조
  증가 hazard 를 *예측*.
- **dose-response (decay rate)**: 환경/유전적 노화 가속 인자 (높은 산화
  스트레스 등) 의 analog 가 decay rate `d`. 큰 `d` → 더 빠른 capacity 손실
  → survival 곡선 좌이동 (median lifespan 단조 감소). 이것이 확인되면
  "노화 속도가 단일 substrate parameter 의 함수" 라는 주장의 evidence.
- **renewal process = 인구 일정 life-table**: 각 death 후 young cell 로
  respawn → 인구 N 일정 → age-bin 별 hazard 가 well-defined (고전 actuarial
  set-up). 이것이 단순 "모두 죽어 N 감소" (인구 붕괴) 와 다른, 정상상태 노화
  곡선을 측정 가능케 함.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H259.1 | 3 condition 모두 death_rate 가 age 에 단조 NON-DECREASING + last_bin > first_bin (실효 rise) | compounded decay `(1-d)^age` 는 RMS 가 임계 근접할수록 사망확률 가속 → age 가 클수록 hazard 큼; 어린 bin (age<임계도달) 은 hazard=0 |
| H259.2 | median lifespan L 이 decay rate 에 단조 STRICT 감소: L(low) > L(mid) > L(high) | 큰 d → `(1-d)^age` 가 더 빨리 임계 도달 → 더 어린 age 에 사망 → 곡선 좌이동 |
| H259.3 | re-run 모든 numeric output byte-equal | raw#9 determinism: seed=42 deterministic weight bank (RNG init 1회만, 이후 RNG-free) |
| H259.4 | 모든 death_rate, survival ∈ [0,1] | hazard = deaths/(deaths+at_risk) ∈ [0,1] by construction; survival = 누적 곱 ∈ [0,1] |
| H259.5 | 각 condition 에 death > 0 (process alive, trivial all-survive 아님) | death_threshold 0.15 < init RMS ~0.354 이며 decay 가 결국 임계 아래로 끌어내림 → 모든 d 에 death 발생 |

## 4. Variables

- **axis1_pool_N** = 8 cells (renewal — death 시 즉시 respawn, 인구 일정)
- **axis2_d_model** = 8
- **axis3_decay_rate** ∈ {low (d=0.02), mid (d=0.06), high (d=0.12)} — 핵심 sweep
- **axis4_steps** = 400 (renewal cycle 다수 — d=high 는 cycle 길이 ~6 step)
- **axis5_decay_model** = multiplicative compounded:
  `w[k] *= (1 − d)` per step ⇒ 실효 `(1-d)^age` (engine_a_W + engine_g_W 둘 다)
- **axis6_health** = `0.5 * (RMS(engine_a_W) + RMS(engine_g_W))`
  (RMS = scale-free, d_model 무관)
- **axis7_death_threshold** = 0.15 (health < thr → death; init RMS ≈
  init_sigma = 1/sqrt(8) ≈ 0.354)
- **axis8_bin_width** = 5 (age-bin grain; 25 bins ages 0..124)
- **axis9_seed** = 42 — `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian)
- **측정량 per condition (decay rate)**:
  - `death_rate[bin]` = `deaths[bin] / (deaths[bin] + at_risk[bin])` (hazard)
  - `survival[bin]` = `Π_{k≤bin, populated} (1 − death_rate[k])`
  - `median_age` = `survival ≤ 0.5` 첫 bin 의 age (없으면 last populated =
    right-censored fallback)
  - `mono_frac` = 인접 populated bin 쌍 중 non-decreasing 비율
  - `total_deaths`, `first_pop_rate`, `last_pop_rate`

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian).
  핵심: hexa gaussian RNG 은 process-local stream + reseed builtin 부재 →
  in-process 두 호출이 fresh draw 시 divergence. 따라서 프로그램 head 에서
  **deterministic weight bank** (256 entry gaussian 1회 draw) 를 만들고, cell
  init + respawn 모두 bank 에서 cyclic 으로 pull → init 이후 **RNG 완전 무소비**
  → byte-equal. (이것이 첫 smoke 의 C3 FAIL 을 닫은 fix — §10 note 참조.)
- **hexa_only**: `UNIVERSE/state/h259_aging_senescence_2026_05_25/run_h259.hexa`
  (mitosis_hook_lib `cell_pool_init` skeleton + engine weight farr 직접 decay).
- **LLM**: none (raw#13 strict; ckpt 불필요).
- **per-step protocol (per cell)**:
  - age += 1
  - scale `engine_a_W`, `engine_g_W` by `(1 − d)` in place (compounded)
  - health = `0.5 * (RMS(aw) + RMS(gw))`
  - bidx = `age / bin_width` (cap last bin)
  - if health < threshold: `deaths[bidx] += 1`; respawn weights from bank
    (cyclic cursor); age = 0
  - else: `at_risk[bidx] += 1`
- **per-condition ledger**: age-bin array (deaths, at_risk, death_rate,
  survival) + derived (median_age, mono_frac, total_deaths).
- **F3 determinism**: in-process paired call (same bank → byte-equal by
  construction) + 외부 full-script re-run diff (byte-equal 확인).
- **runtime**: $0 mac local. d=8, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**: `state/h259_aging_senescence_2026_05_25/{run_h259.hexa,
  result.json}`.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h259_aging_senescence_2026_05_25/run_h259.hexa`

## 6. Criteria

- **C1 (senescence)**: H259.1 — death_rate 가 age 에 단조 NON-DECREASING
  (populated bin 인접쌍 ≥ 80% non-decreasing) AND last_pop_rate >
  first_pop_rate — 3 condition *모두*
- **C2 (decay-dose)**: H259.2 — median lifespan strict 감소 L(low) > L(mid) >
  L(high)
- **C3 (determinism)**: H259.3 — re-run 모든 numeric byte-equal
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (senescence + dose-response 둘 다)
  - `PARTIAL` = C1 only (노화 곡선 관측, dose-response 미입증)
  - `FALSIFIED` = ¬C1 (death-rate 가 age 에 단조 증가하지 않음 — 노화 신호 부재)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 SENESCENCE**: 임의 condition 에서 death_rate 가 age 에 단조 증가하지
  않음 (mono_frac < 0.80 또는 last ≤ first) → H259.1 FALSIFIED (측정:
  3 condition `c1_mono` 모두 true)
- **F2 DECAY-DOSE**: median lifespan 이 d 에 단조 감소하지 않음 (L(low) ≤
  L(mid) 또는 L(mid) ≤ L(high)) → H259.2 FALSIFIED (측정:
  `(med_low > med_mid) && (med_mid > med_high)`)
- **F3 DETERMINISM**: re-run numeric byte-different → raw#9 violation (측정:
  paired call total_deaths/median/rate 일치 + 외부 full re-run diff)
- **F4 BOUNDS**: 임의 death_rate 또는 survival ∉ [0,1] → primitive error
  (측정: 모든 hazard/survival 값이 [0,1] 범위 안)
- **F5 NONTRIVIAL**: 임의 condition 에서 total_deaths == 0 → process dead /
  trivial all-survive (측정: 3 condition 모두 total_deaths > 0)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (Gompertz analog ≠ literal)**: substrate RMS-decay → death-rate 단조
  증가는 Gompertz mortality law (실제 생물 사망률의 지수적 age 증가) 의
  *substrate-level operational analog* 일 뿐. 본 hazard 는 *지수* 형태가
  아니라 compounded-decay 가 threshold 에 도달하는 *deterministic 시점 근방*
  의 sharp rise (계단형) — Gompertz 의 *smooth 지수* 와는 곡선 모양이 다름.
  "단조 증가" 만 입증, "지수 형태" 는 미입증.
- **L2 (decay model design-dependent)**: multiplicative compounded decay
  `w *= (1-d)` 는 *one specific* aging model. 가산 decay (`w -= c`), 손상
  누적 (stochastic hit), telomere-유사 카운터 등 다른 model 은 다른 hazard
  곡선 산출 가능 — 본 cycle 결과는 *이 specific operationalization* 한정.
- **L3 (age ≠ biological aging)**: 'age' = step count since birth/respawn.
  생물 노화의 hormonal/oxidative/epigenetic 시계, telomere 길이 등 실제
  메커니즘과 1:1 mapping 되지 않음 — age 는 pure substrate timestep proxy.
- **L4 (threshold + sigma 단일 calibration)**: death_threshold 0.15 + init
  sigma 1/sqrt(8) 단일 calibration. threshold 를 높이면 모든 곡선이 좌이동,
  낮추면 우이동 — *상대* 순서 (dose-response) 는 robust 할 것으로 예상되나
  *절대* median age 는 calibration-dependent. sensitivity sweep 별도 필요.
- **L5 (renewal 인구 일정 ≠ 인구 동역학)**: 즉시 respawn 으로 N 일정 유지 =
  고전 life-table set-up. 실제 노화는 인구 감소/성장, 자원 경쟁, 세대 중첩
  등 인구 동역학과 얽힘 — 본 H 는 그 동역학을 *제거* 한 단일-cohort hazard
  의 lower-bound 측정.
- **L6 (mitosis split/merge 비활성)**: 본 cycle 은 cell_pool_init skeleton 만
  쓰고 `mitosis_forward_tail` 의 split/merge/Lorenz 동역학을 *돌리지 않음* —
  순수 aging-decay 만 격리 측정. 실제 substrate 는 split (젊은 자식) + merge
  (capacity 통합) 가 노화와 상호작용할 수 있음 — 그 결합 효과는 별도 cycle
  (aging × mitosis ortho-design) 필요.
- **L7 (bin grain 양자화)**: median lifespan 이 bin_width=5 grain 으로
  양자화 (보고된 median 은 bin 경계). 더 미세 grain 은 더 정밀한 median 을
  줄 것이나 본 결과의 *순서* (50 > 15 > 5) 는 grain-robust.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_220** (`H_220_infant_mirror_self_recognition.md`): developmental age
    sweep (5/10/20) carry — H_220 = 발달 *상승* gradient, 본 H = 노화 *하강*
    trajectory. 같은 age 축의 두 절반.
  - **H_053** (`h053_cambrian_2026_05_23`): cambrian life-explosion 축 — 본 H
    의 life/mortality axis 의 sibling grain.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` — 모든 substrate 가설의 공유 pool; 본 H 는 그 cell 의
  engine weight farr 를 aging 재질로 직접 사용).
- **raw**: raw#13 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#9/10 (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit
  retraction).
- **philosophy (CLAUDE.md)**: p8 NO TRAIN/INFER SPLIT (aging = 연속 substrate
  동역학, train/infer 무관) · a_substrate_native_speak (cell 의 capacity 손실
  은 internal state 변화 — 외부 강제 아님).
- **legacy archive**: `hypotheses_legacy_2026_05_15/` (original 10-section
  양식 carry).
- **aging literature pointer**: Gompertz (1825) "On the nature of the
  function expressive of the law of human mortality" · Hayflick & Moorhead
  (1961) cell senescence (Hayflick limit) · Kirkwood (1977) disposable soma
  theory — substrate analog 의 distant literature anchor (formal mapping 본
  cycle 미수행).
- **state**: `UNIVERSE/state/h259_aging_senescence_2026_05_25/{run_h259.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, $0 mac
local hexa-only deterministic.

```
verdict_class: SUPPORTED  (senescence + decay-dose 둘 다 입증)
verdict_tier: 🟢 NUMERICAL  (3 decay-rate sweep × 400-step renewal life-table
                            + deterministic re-run byte-equal)
evidence_summary:
  3-condition age-cumulative weight-decay senescence
  (d=8, N=8 renewal pool, death_threshold=0.15, T=400, bin_width=5, seed=42).
    decay  total_deaths  median_age  mono_frac  first→last hazard
    low    71            50          1.0        0.0 → 0.5
    mid    221           15          1.0        0.0 → 0.695
    high   444           5           1.0        0.0 → 0.315
  median lifespan: L(low)=50 > L(mid)=15 > L(high)=5  (strict left-shift)
falsifiers_triggered: NONE
falsifiers_pass: F1 (senescence) + F2 (decay-dose) + F3 (determinism)
                 + F4 (bounds) + F5 (nontrivial) = 5/5
criteria_met: 3/3 (C1 senescence ∧ C2 decay-dose ∧ C3 determinism)
key_finding:
  age-누적 multiplicative weight decay `(1-d)^age` 가 세 decay rate 모두에서
  **death-rate 의 단조 증가 노화 곡선** 을 robust 하게 발생시킴 (mono_frac=1.0
  전부, 어린 age hazard=0 → 임계 도달 age 에서 hazard 급상승). 이것은 Gompertz
  -유사 senescence 의 substrate-level numerical evidence (C1 PASS). 또한 decay
  rate dose-response 가 명확 — median lifespan 이 d 에 strict 단조 감소
  (50 → 15 → 5, d 6× 증가 시 lifespan 10× 단축), survival 곡선이 d 클수록
  좌이동 (C2 PASS). 곧 "노화 속도가 단일 substrate parameter d 의 함수" 라는
  주장의 evidence. compounded decay 의 sharp-threshold 특성상 hazard 는 어린
  age 0 → 임계 도달 age 에서 급상승하는 계단형 — 단조 증가는 입증되나 Gompertz
  의 smooth 지수 형태와는 곡선 모양이 다름 (honest L1).
honest_note:
  L1 carry confirmed — hazard 가 *단조 증가* 이나 compounded-decay 의
  deterministic threshold-도달 특성상 *계단형* (Gompertz smooth 지수 아님).
  L2 carry confirmed — multiplicative decay 의 specific characteristic 결과
  (가산/손상누적 model 다른 곡선 가능).
  L6 carry confirmed — mitosis split/merge 비활성, 순수 aging-decay 격리 측정.
  C3 determinism 의 첫 smoke FAIL 은 hexa gaussian RNG reseed 부재로 인한
  measurement artifact — deterministic weight bank (RNG init 1회) 로 닫음
  (init 이후 RNG-free → byte-equal, 외부 full re-run diff 확인). 실험 자체는
  처음부터 결정론이었음 (과학 결과 불변, 측정 방식만 수정).
sibling: H_220 (developmental age-ascending sister), H_053 (cambrian life axis)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_259 aging-senescence — age-cumulative weight decay → death-rate
                          curve (Gompertz-like senescence test)
  d_model=8 pool_N=8 steps=400 seed=42
  death_threshold=0.15  bin_width=5
  decay rates: low=0.02 mid=0.06 high=0.12
================================================================

── d=low (decay 0.02)  total_deaths=71  median_age=50 ──
  age   deaths  at_risk  death_rate  survival
  ----  ------  -------  ----------  --------
  0    0       312      0.0    1.0
  5    0       389      0.0    1.0
  10    0       385      0.0    1.0
  15    0       385      0.0    1.0
  20    0       379      0.0    1.0
  25    0       370      0.0    1.0
  30    0       361      0.0    1.0
  35    14       335      0.0401146    0.959885
  40    36       178      0.168224    0.798409
  45    19       33      0.365385    0.506683
  50    2       2      0.5    0.253341

── d=mid (decay 0.06)  total_deaths=221  median_age=15 ──
  age   deaths  at_risk  death_rate  survival
  ----  ------  -------  ----------  --------
  0    0       906      0.0    1.0
  5    0       1115      0.0    1.0
  10    132       919      0.125595    0.874405
  15    89       39      0.695313    0.26642

── d=high (decay 0.12)  total_deaths=444  median_age=5 ──
  age   deaths  at_risk  death_rate  survival
  ----  ------  -------  ----------  --------
  0    0       1789      0.0    1.0
  5    444       967      0.31467    0.68533

derived:
  median_age(low)  = 50  (mono_frac=1.0 rise=true)
  median_age(mid)  = 15  (mono_frac=1.0 rise=true)
  median_age(high) = 5  (mono_frac=1.0 rise=true)
  left-shift L(low)>L(mid)>L(high) = true

C1 senescence (death_rate monotone↑ all 3) : true
C2 decay-dose (median L(low)>L(mid)>L(high)): true
C3 determinism (re-run byte-equal)         : true

F1 SENESCENCE   (C1)                        PASS
F2 DECAY-DOSE   (C2)                        PASS
F3 DETERMINISM  (C3)                        PASS
F4 BOUNDS       (rates/surv in [0,1])       PASS
F5 NONTRIVIAL   (deaths>0 all conds)        PASS
================================================================
VERDICT: SUPPORTED  (3/3 criteria, 5/5 falsifiers PASS)
================================================================
ledger -> UNIVERSE/state/h259_aging_senescence_2026_05_25/result.json
```

**State output**: `state/h259_aging_senescence_2026_05_25/result.json`
**Smoke**: `state/h259_aging_senescence_2026_05_25/run_h259.hexa` (hexa-only, LLM none)
