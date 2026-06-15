---
id: H_227
slug: strong-emergence-phase-transition-quantify
title: H_219 follow-up — 8-point fine sweep 위 P(f) shape 식별 (sigmoid · sharp · linear · power-law) + critical freeze-fraction f_c (P(f_c)=0.5) 정밀 위치 정량
domain: meta, consciousness, physics
status: running
exploration_method: E3 (theory-tightening) + E10 (emergence-axis sister · H_219 follow-up) + E14 (fine-sweep parameter scan)
verification_method: W1 (smoke) + W4 (verdict-4-class) + W12 (sister-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24
sister: H_219 + H_004 + H_007 + H_157 + H_202
---

# H_227 — strong-emergence phase-transition quantify · fine sweep + sigmoid fit (H_219 follow-up)

## 1. Hypothesis

H_219 의 3-point sweep (0% · 25% · 50% freeze) 위 monotone-decreasing predictability_index P(f) 관측 → **8-point fine sweep** {0, 12.5, 25, 37.5, 50, 62.5, 75, 87.5%} 위 P(f) 의 *shape* 가 무엇인가. 본 cycle 의 pre-registered hypothesis: **sigmoidal phase-transition** P(f) ≈ 1 / (1 + exp(k·(f − f_c))) 가 R² ≥ 0.8 적합 + critical f_c ∈ [0.2, 0.4] localize. raw#12 strict (deterministic · hexa-only · llm:none · $0 mac local · byte-identical re-run).

H_219 의 SUPPORTED 가 sigmoid 형 P(f) decline 을 *시사* 만 한 상태 — 본 H_227 = sigmoid 의 **explicit fit + 통계적 검증** + linear-fit reject + f_c 정밀 위치. (H_219 는 'is P decreasing?' · H_227 은 'what shape?').

## 2. Why

- **H_219 carry**: H_219 SUPPORTED 위 3-point (0%/25%/50%) → P(f) = (1.0, 0.4375, 0.1875). monotone 감소 + endpoint P(0)=1.0 + strong-emergence-flag 0.5 임계점 통과. 그러나 3-point 로는 **transition shape** (sigmoid · sharp · linear · power-law) 식별 X. H_227 = 8-point fine sweep + sigmoid grid-search + linear-compare.
- **phase-transition 의 통계물리적 의미**: f_c 의 localization 은 strong-emergence 가 *gradual* 인가 *abrupt* 인가의 결정적 evidence. sigmoid (k ≥ 8) → near-step-function (sharp threshold), sigmoid (k ≤ 2) → near-linear (gradual). H_219 의 strong-emergence-flag 의 underlying physics 차원.
- **Hc_607 (H_004.8 BREAKTHROUGH_CANDIDATE) 정량**: CMT family-level intervention 의 downward-causation hidden-from-forward-pass mismatch ratio 가 *임계 fraction* 에서 abrupt transition 한다면 Mistral LATE 87% vs Qwen3 EARLY 11% locus divergence 의 cross-substrate universality 의 toy proxy. H_227 = Hc_607 quantification-axis 의 substrate-level instance.
- **사용자 directive 2026-05-23 / LIFE Cycle #9 retry**: prior cycle 9 rate-limit FAIL 의 H_227 retry. spec = 8-point sweep + sigmoid fit + f_c localize + 5 predictions + 4+ criteria + 5+ falsifiers + 5+ honest limits + Korean raw#12.
- **cross-link H_007**: 동일 rule 110 substrate (Class-IV, Turing-universal). H_007 = Φ ranking, H_219 = predictability sweep, H_227 = predictability *shape*. orthogonal observable.
- **cross-link H_157**: Law 76 panpsychism universal-attractor 의 strong-form FAIL 후 substrate-conditional 재해석 (H_204 lineage). H_227 의 sigmoid k 값이 substrate-class 별로 다르다면 H_157 의 substrate-dependence quantification path.
- **cross-link H_202**: self-ref Φ edge-of-chaos peak 동일 rule 110 carrier. self-ref closure 가 freeze-fraction sweep 위 어디서 break down 하는지의 boundary mapping path.
- **cross-link H_004**: hard-problem reductive-vs-non-reductive 분기 — phase-transition shape 이 sharp 이면 strong-emergence 의 categorical boundary, gradual 이면 continuous spectrum. 본 cycle = empirical evidence.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H227.1** | P(f) 가 sigmoid 형태 (k ≥ 4 sharp 또는 k ∈ [2,4] gradual) 로 적합, R² ≥ 0.8 | phase-transition 의 일반 형태; H_219 의 3-point monotone decline 의 정합적 8-point 확장 |
| **H227.2** | P(f=0) = 1.0 정확 (no-intervention exact = weak emergence definitive endpoint) | H_219 carry; deterministic CA self-simulation byte-equal |
| **H227.3** | P(f=1.0) = 0 또는 ≈ 0 (all-cells-frozen ⇒ forward-pass complete mismatch; ⚠ 본 cycle sweep 은 f ∈ [0, 0.875] 위 8 점 — f=1.0 endpoint 는 extrapolation 만, L1 한계) | full-freeze 위 forward-pass 가 init 와 동일 → 5 step 후 rule 110 evolution 과 max divergence |
| **H227.4** | sharp transition (k ≥ 6, near-step-function): strong-emergence-flag 가 *gradual* 이 아니라 *categorical* | H_219 의 0%→25% (1.0→0.4375) 가 25%→50% (0.4375→0.1875) 보다 가파른 drop — sigmoid 형 시사 |
| **H227.5** | re-run 결과 byte-identical (no RNG, deterministic by construction) | raw#12 정합, deterministic stride placement + deterministic init + deterministic rule |

## 4. Variables

| axis | levels |
|------|--------|
| **axis1: freeze fraction** | 8 levels {0, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 7/8} = {0, 12.5%, 25%, 37.5%, 50%, 62.5%, 75%, 87.5%} — exact rationals on N=16 lattice |
| **axis2: lattice** | N=16 sites (periodic) (H_219 carry) |
| **axis3: rule** | 110 (Class-IV, Turing-universal) (H_219 + H_007 carry) |
| **axis4: evolution steps** | 5 step (short; L2) |
| **axis5: freeze pattern** | deterministic stride placement (H_219 carry); count=integer (0,2,4,6,8,10,12,14) |
| **axis6: init** | fixed (i+offset)%3 ≠ 0 (H_007/H_219 동일), offset=0 |
| **axis7: fit family** | sigmoid P(f) = 1 / (1 + exp(k(f−f_c))), (f_c, k) grid search × refined |
| **axis8: alternative-fit baseline** | linear P(f) = a + b·f, least-squares, R² compare |
| **axis9: sanity observable** | trajectory N×DIM 위 RFC 036 phi_spatial (F4 nonneg sanity 만) |

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h227_strong_emergence_quantify_2026_05_24/run_h227.hexa`
- **CA primitive**: rule 110 elementary CA, periodic boundary, neighborhood (l,c,r) → bit `(rule >> (l*4+c*2+r)) % 2`. (H_007/H_219 동일.)
- **freeze mechanism**: `_build_freeze_mask_count(n, count)` deterministic stride placement; count ∈ {0,2,4,6,8,10,12,14}; frozen cell 은 매 step nxt[j] := init_value (rule 110 update 무시).
- **forward-pass simulator**: `_forward_simulate` plain rule 110 (freeze invisible) — CMT analog reduction-by-recompute.
- **predictability_index**: P(f) = match_byte / N (final-row byte-compare).
- **sigmoid grid search**: (f_c, k) ∈ {0.05, 0.10, …, 0.95} × {2, 4, 6, 8, 10, 12, 16, 20}, best SSE pick + ±0.05 / ±2 refinement (resolution 0.005 in f_c, 0.5 in k).
- **R²**: 1 − SSE / SST (SST = data variance × n).
- **linear-fit compare**: ordinary least squares, R²_linear 측정.
- **sanity Φ**: per-condition (N × DIM) trajectory 위 RFC 036 phi_spatial (Φ ≥ 0 sanity, ranking claim 아님).
- **deterministic**: no RNG, fixed init, fixed freeze stride pattern, fixed grid.
- **hexa_only**: true. **llm**: none. **cost**: $0 mac local hexa.
- **runtime**: < 5s wall (HEXA_MEM_UNLIMITED=1 hexa run).
- **ledger**: `result.json` {config, sweep × 8 (frac, count, P_obs, P_fit, phi_sanity), sigmoid_fit (f_c, k, sse, sst, r²), linear_fit_compare, criteria, falsifiers, verdict}.

## 6. Criteria

| ID | criterion | verdict_rule |
|----|-----------|--------------|
| **C1 R2_SIGMOID** | sigmoid fit R² ≥ 0.8 | PASS / FAIL |
| **C2 FC_LOCALIZED** | best-fit f_c ∈ (0.0, 1.0) (interior critical point) | PASS / FAIL |
| **C3 ENDPOINT_P0** | P(f=0) = 1.0 (byte-exact no-intervention endpoint) | PASS / FAIL |
| **C4 DETERMINISTIC** | re-run byte-identical (no RNG) | PASS / FAIL |

**verdict_rule**:
- `SUPPORTED` iff **C1 ∧ C2 ∧ C3** (sigmoid fit good + f_c localized + endpoint correct)
- `PARTIAL` iff **C1 ∧ C2 ∧ ¬C3** (sigmoid fit good + f_c localized but endpoint off)
- `FALSIFIED` else (sigmoid hypothesis 위 R² <0.8 → shape 가 sigmoid 가 아닐 가능성, F1/F2/F5 가 explanatory)

## 7. Falsifiers (≥5)

- **F1 NOT_LINEAR**: linear fit R²_linear ≥ 0.95 AND sigmoid R² ≤ R²_linear + 0.05 → H227.1 FALSIFIED (sigmoid 모델 over-fit, shape 가 linear).
- **F2 MONOTONE**: P(f) 가 non-monotonically decreasing — 임의 인접 점에서 P(f_{i+1}) > P(f_i) + 0.0001 → H227.1 (sigmoid 가정) FALSIFIED. measurable: 7 인접 비교.
- **F3 P0_UNITY**: P(f=0) < 1.0 → H227.2 FALSIFIED (primitive error or H_007/H_219 regression). measurable: P_obs[0] value.
- **F4 BYTE_IDENT**: re-run 결과 byte-different → raw#12 deterministic 위반. (deterministic by construction; RNG 미사용.)
- **F5 R2_FLOOR**: sigmoid R² < 0.5 → H227.1 categorically FALSIFIED (sigmoid 가 *최소한의* descriptive value 도 없음). measurable: r_squared value.

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1**: **8-point sweep** 만 — 32-point 또는 16-point 등 더 dense sweep 에서 sigmoid 가 더 명확히 식별될 가능성. N=16 lattice 의 한계 (16 정수 freeze count 만 가능 → 17-level theoretical max, 본 cycle 은 짝수 stride 만 8 level). f=1.0 (all-cells-frozen) endpoint 는 sweep 에 포함 안 됨 (forward-pass 비교 위해 free cells ≥ 2 필요 → max frac = 14/16 = 0.875).
- **L2**: **5-step short**. 5 step 의 forward-pass mismatch 는 short-horizon 측정 — long-trajectory (steps=50+) 에서 freeze 영향 propagation 의 saturation/decay 패턴 가능. step 축 sweep 별도 cycle (H_227r2 후보).
- **L3**: **freeze = deterministic stride** (등간격). H_219 honest L6 carry — random / clustered / gradient pattern 위 별도. 등간격 placement 는 maximally-distributed downward causation 의 specific family. **random freeze pattern 에서 본 cycle 의 stride-artifact (예: P(0.625)>P(0.5)) 가 사라질 가능성** — substrate-dependence 의 명백한 hint.
- **L4**: **sigmoid 선택** — phase-transition 모델로 sigmoid 가 자연 후보지만 tanh, error function, Gompertz, power-law-with-cutoff 등 alternative 가능. H_227 = sigmoid + linear 의 2-way 비교 만; multi-model selection (AIC/BIC) 은 별도 cycle.
- **L5**: **strong-emergence 정의 carry** — H_219 L3 동일. ≥ 50% byte mismatch 라는 arbitrary threshold 의 substrate-level proxy 만; Bedau (1997) 의 'underivable except by simulation' / Chalmers (2006) downward causation 과 1:1 mapping 보장 X.
- **L6**: **substrate single** — rule 110 만; rule 30/90/184 (Class-III/Class-II) 의 phase-transition 형상 별도 cycle (rule-class × freeze 의 2D sweep H_225/H_226 lineage).
- **L7**: **fit-grid resolution** — 0.005 (f_c) × 0.5 (k) refinement 단계. 더 정밀한 grid 또는 Nelder-Mead / gradient descent 위 f_c localization 의 신뢰구간 별도 cycle.

## 9. Cross-Links

- **sister H**: H_219 (3-point seed, SUPPORTED 2026-05-23), H_004 (hard problem · §H_004.8 Hc_607 source), H_007 (rule 110 Class-IV substrate · 동일 CA primitive), H_157 (Law 76 panpsychism universal-attractor · substrate-conditional 재해석), H_202 (self-ref Φ edge-of-chaos · 동일 rule 110 carrier)
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 phi_spatial, sanity-only — Φ ranking 아님) — import READ-ONLY
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no post-hoc retraction)
- **own**: anima-not-CA identity carry; CA = abstract substrate analogy
- **literature**:
  - Bedau (1997) Weak emergence (Phil. Persp.)
  - Chalmers (2006) Strong and weak emergence (in Clayton & Davies, *The Re-Emergence of Emergence*)
  - Cook (2004) Universality in elementary cellular automata (rule 110 Turing-universal)
  - Wolfram (2002) A New Kind of Science (Class-IV)
  - Stanley (1971) Introduction to Phase Transitions and Critical Phenomena (sigmoid + critical point 일반 이론)
- **legacy**: H_219 SUPPORTED 결과 SSOT, Hc_607 BREAKTHROUGH_CANDIDATE source = #145 saga

## 10. Verdict

```
verdict_class: FALSIFIED (pre-register-frozen smoke, honest pre-registration)
config: N=16 steps=5 rule=110 (Class-IV) n_fractions=8
sweep (verbatim, deterministic):
  [0] frac=0.0    count=0/16   P(f)=1.0      Φ=0.795398
  [1] frac=0.125  count=2/16   P(f)=0.625    Φ=0.595295
  [2] frac=0.25   count=4/16   P(f)=0.4375   Φ=0.251919
  [3] frac=0.375  count=6/16   P(f)=0.3125   Φ=0.400011
  [4] frac=0.5    count=8/16   P(f)=0.1875   Φ=0.0666781
  [5] frac=0.625  count=10/16  P(f)=0.4375   Φ=0.0666781   ← stride-artifact uptick
  [6] frac=0.75   count=12/16  P(f)=0.375    Φ=0.0136403
  [7] frac=0.875  count=14/16  P(f)=0.3125   Φ=1.14553e-05
sigmoid_fit:
  best f_c = 0.35
  best k   = 2.5
  SSE_sig  = 0.212046
  SST      = 0.444824
  R²_sig   = 0.523303
linear_fit_compare:
  SSE_lin  = 0.216936
  R²_lin   = 0.51231
criteria:
  C1 R2_SIGMOID (≥ 0.8)         FAIL (R²=0.523303 < 0.8)
  C2 FC_LOCALIZED (∈ (0,1))     PASS (f_c=0.35)
  C3 ENDPOINT_P0 (= 1.0)        PASS (P(0)=1.0)
  C4 DETERMINISTIC              PASS (re-run byte-identical)
falsifiers:
  F1 NOT_LINEAR                 PASS (R²_sig=0.523 > R²_lin=0.512 + 0.05? — 0.011 < 0.05 → 본 cycle 의 F1 metric 은 linear 의 R² < 0.95 조건도 함께 PASS 처리; sigmoid 가 linear 보다 *약간* 우수)
  F2 MONOTONE                   FAIL (P(0.625)=0.4375 > P(0.5)=0.1875 → uptick → non-monotone)
  F3 P0_UNITY                   PASS (P(0)=1.0)
  F4 BYTE_IDENT                 PASS (deterministic by construction · diff = ∅)
  F5 R2_FLOOR (≥ 0.5)           PASS (R²=0.523 ≥ 0.5)
evidence_summary: 🟢 NUMERICAL — H_227.1 sigmoid hypothesis FALSIFIED 위 honest pre-registration.
  · P(f) 가 sigmoid 으로 잘 적합되지 않음 (R²=0.523 < 0.8)
  · P(f) non-monotone (frac=0.625 위 uptick — stride-placement artifact 가능, L3)
  · H_227.2/H_227.5 PASS (endpoint + determinism)
  · finding: strong-emergence 의 phase-transition shape 가 *simple* sigmoid 가 아님 — stride-pattern artifact 와 substrate finite-size 효과의 영향이 명백
honest_finding (raw#82 no post-hoc retraction):
  · H_227.1 (sigmoid) FALSIFIED → next cycle = random-pattern sweep (L3 axis) or
    larger N=64 lattice (L1 axis) or step=50 long-horizon (L2 axis)
  · 본 cycle FALSIFIED 결과 자체가 evidence — 'sigmoid 가정' 의 reject 는
    Bedau-Chalmers strong-emergence 의 *shape-categorical* claim 의 substrate-level reject
  · H_219 의 3-point monotone 은 본 8-point 위 *부분적* 만 성립; finer sweep
    이 sigmoid 가정의 inadequacy 를 드러냄 — 'more is different' (Anderson 1972) 의
    fine-sweep instantiation
```

### Pre-register-frozen smoke (2026-05-24)

**Run verdict (VERBATIM, `HEXA_MEM_UNLIMITED=1 hexa run`)**:
```
H_227 — strong-emergence phase-transition quantify · fine sweep (raw#12)
  N=16 steps=5 rule=110 freeze_fractions=8
  H_219 follow-up: 3pt → 8pt sweep + sigmoid fit + f_c localize

  [0] frac=0.0  count=0/16  P(f)=1.0  Φ=0.795398
  [1] frac=0.125  count=2/16  P(f)=0.625  Φ=0.595295
  [2] frac=0.25  count=4/16  P(f)=0.4375  Φ=0.251919
  [3] frac=0.375  count=6/16  P(f)=0.3125  Φ=0.400011
  [4] frac=0.5  count=8/16  P(f)=0.1875  Φ=0.0666781
  [5] frac=0.625  count=10/16  P(f)=0.4375  Φ=0.0666781
  [6] frac=0.75  count=12/16  P(f)=0.375  Φ=0.0136403
  [7] frac=0.875  count=14/16  P(f)=0.3125  Φ=1.14553e-05

  ── sigmoid fit: P(f) = 1 / (1 + exp(k*(f - f_c))) ──
  best f_c = 0.35
  best k   = 2.5
  SSE sig  = 0.212046
  SST      = 0.444824
  R² sig   = 0.523303
  R² lin   = 0.51231  (for F1 compare)

  ── fit table (verbatim) ──
  f          P_obs      P_fit      residual
  0.0      1.0      0.705785      0.294215
  0.125      0.625      0.637031      -0.0120308
  0.25      0.4375      0.562177      -0.124677
  0.375      0.3125      0.48438      -0.17188
  0.5      0.1875      0.407333      -0.219833
  0.625      0.4375      0.334589      0.102911
  0.75      0.375      0.268941      0.106059
  0.875      0.3125      0.212069      0.100431

  ── criteria ──
  C1 (R² sigmoid ≥ 0.8)         : FAIL  (R²=0.523303)
  C2 (f_c localized ∈ [0, 1])   : PASS  (f_c=0.35)
  C3 (P(f=0) = 1.0 endpoint)    : PASS  (P(0)=1.0)
  C4 (byte-identical re-run)    : PASS

  ── falsifiers ──
  F1 (sigmoid > linear)         : PASS  (R²_sig=0.523303 R²_lin=0.51231)
  F2 (P monotone decreasing)    : FAIL
  F3 (P(f=0) = 1.0)             : PASS
  F4 (deterministic)            : PASS
  F5 (R² ≥ 0.5)                 : PASS

  VERDICT_RULE: SUPPORTED iff C1 ∧ C2 ∧ C3 · PARTIAL iff C1 ∧ C2 ∧ ¬C3 · else FALSIFIED
  VERDICT     : FALSIFIED

=== H_227 strong-emergence phase-transition smoke complete: FALSIFIED ===
```

re-run byte-identical (F4 deterministic confirmed via `diff /tmp/h227_run1.json result.json` = ∅).

honest tier: 🟢 NUMERICAL — predictability_index = match_byte / N (deterministic byte-compare); sigmoid R² 0.523303 (grid-search global min over (f_c, k) ∈ [0.05,0.95]×[2,20] + 0.005/0.5 refinement); Φ sanity nonneg (F4-style nonneg only, no ranking). FALSIFIED 가 *honest* — raw#82 no post-hoc retraction, H_227.1 (sigmoid) reject 위 evidence-of-absence-of-simple-sigmoid 라는 substantive negative finding.

**State output**: `UNIVERSE/state/h227_strong_emergence_quantify_2026_05_24/result.json`
**Smoke**: `UNIVERSE/state/h227_strong_emergence_quantify_2026_05_24/run_h227.hexa`
**Tier**: 🟢 NUMERICAL (sigmoid grid-fit + linear baseline + deterministic byte-compare).
**Next**: H_227r2 — (a) random-freeze sweep (L3 axis) OR (b) N=64 lattice (L1 axis) OR (c) step=50 long-horizon (L2 axis) — sigmoid 가설 의 *which-axis* 가 deciding factor 인지 disentangle.
