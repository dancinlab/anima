---
id: H_287
slug: shannon-entropy-phi-correlate
title: faithful IIT 4.0 big-Φ 는 Shannon 엔트로피로 환원되는가 — ECA substrate panel 에서 통합(Φ) ⊥ 정보(엔트로피) 이중 dissociation 검정
domain: information · consciousness · substrate · meta
status: closed-negative
exploration_method: E5 (foundational-distinction probe) + E16 (cross-substrate consistency) + E0 (reductive-null 검정 — IIT 핵심 주장의 self-substrate 확증)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link IIT4 M6 / H_281 / H_278)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26 (new)
sister: IIT4 M6 (ECA→TPM faithful re-measure, engine 공급), H_281 (life-vs-consciousness Φ-structure, 동일 substrate panel), H_278 (faithful Φ small-N), H_279 (salience⊥Φ-diversity, 同 "X⊥Φ" 서명 계열)
axes_seed: AXES.md R5 (information) rank-2 `shannon-entropy-Φ-correlate`
---

# H_287 — faithful IIT 4.0 big-Φ 는 Shannon 엔트로피로 환원되는가

## 1. Hypothesis

IIT 의 정전(canonical) 핵심 주장 중 하나: **통합정보 Φ 는 Shannon 정보(엔트로피)와
같은 것이 아니다**. 서로 독립적인 N 개의 무작위 비트 더미는 엔트로피가 *최대*지만
통합은 *제로*다 (쪼개도 아무것도 잃지 않음). 본 H 는 이 주장을 LIFE lane 자신의
substrate 가족(elementary CA ring)에서, **faithful 인과 IIT 4.0 엔진**으로 검정한다.

검정 대상은 **환원(reductive) 가설** — 즉 "Φ 는 결국 엔트로피를 따라간다" 쪽이다:

**가설 H1 (reductive, 검정 대상 — 기각될 수 있음)**: ECA substrate panel 전반에서
faithful state-평균 big-Φ 가 Shannon 출력-엔트로피와 공변한다 —
`Pearson r(H_out, Φ_mean) ≥ 0.5`.

H1 이 **SUPPORTED** 면 Φ 는 정보량의 단조 함수에 가깝다 (IIT 의 구별 주장 약화).
H1 이 **FALSIFIED** (r < 0.5) 면 Φ 는 엔트로피로 환원되지 않는다 — IIT 의 구별이
자기 substrate 에서 성립하는 **closed-negative** 다 (a_paper_negative_ok: 닫힌 부정은
유효한 발견).

## 2. Why

- **IIT 토대의 self-substrate 검정**: LIFE lane 은 H_266/H_278/H_281 에서 faithful
  big-Φ 를 substrate 분리·calibration 에 써왔으나, "그 Φ 가 그냥 엔트로피 아니냐"는
  **환원 우려**를 정면으로 닫은 적이 없다. 본 H 는 그 우려를 pre-register 된 null
  로 세우고 측정으로 처리한다. proxy(상관 MI) 시절엔 불가능했던 검정 — faithful
  인과 엔진이 있어야 "정보는 있는데 통합은 없는" substrate 를 깨끗이 만들 수 있다.

- **engine 재사용 (reuse-existing-libs, g61)**: IIT4 엔진을 **재발명하지 않는다**.
  `HEXAD/IIT4/lib` 의 검증된 `eca_tpm` (ECA→TPM) · `big_phi` (faithful big-Φ) 만
  import. 새 IIT4 코드 0 줄. 엔트로피·Pearson 은 generic stat (per-experiment 하네스
  inline, H_281 의 `check`/`approx` 와 동일 관례).

- **결정적 witness 가 존재하도록 설계**: 항등규칙 204 는 *완전 단사(bijection)* 라
  출력-엔트로피가 *최대*(=log2 16=4 bit)인데, 각 셀이 독립이라 big-Φ=0 이어야 한다
  (M6/H_281 에서 이미 big-Φ=0 확인됨). 이 한 점만으로 "Φ 는 엔트로피의 단조 함수"가
  깨진다. 본 H 는 이 witness 가 panel 안에서 실제로 r 을 끌어내리는지 정량한다.

- **"X ⊥ Φ" 서명 계열의 연장**: H_265(학습 dampen) · H_275(cyclic<undir) ·
  H_279(attention⊥Φ-diversity) 는 모두 "어떤 양 X 가 Φ 와 직교한다"는 cross-H
  서명을 누적해왔다. 본 H 는 그 X 에 **Shannon 엔트로피** 자체를 넣는, 가장 근본적인
  instance 다.

- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit +
  LLM none + $0 mac-local + NO GPU.

## 3. Predictions

- **H287.1 (dissociation witness)**: 항등규칙 204 가 H_out ≥ 3.99 bit (near-max) 이면서
  Φ_mean < 1e-9 (제로 통합) — *정보 최대, 통합 제로* substrate 가 panel 에 존재. 그리고
  같은 high-엔트로피 영역에서 통합 룰의 Φ_mean > 0.5.
- **H287.2 (r-verdict)**: 10-룰 panel 의 `Pearson r(H_out, Φ_mean)`. r ≥ 0.5 면 H1
  SUPPORTED, r < 0.5 면 FALSIFIED. (예측: FALSIFIED — 204·51 의 max-H/zero-Φ 와 통합
  룰의 sub-max-H/high-Φ 가 vertical spread 를 만들어 r 을 끌어내린다.)
- **H287.3 (anchors)**: 상수 룰 0/255 → H_out=0 AND Φ_mean=0 (null); 단사 룰 204·51 →
  H_out=4.0 정확 (엔트로피 보존).
- **H287.4 (bound)**: 모든 룰에서 0 ≤ H_out ≤ 4 AND Φ_mean ≥ 0.
- **H287.5 (determinism)**: 룰 204 의 (H_out, Φ_mean) re-run byte-identical.

## 4. Variables

- **axis1_rule** (primary, 10-panel — 엔트로피 × Φ 평면을 가로지름):
  - **상수/null**: 0 (전부→0), 255 (전부→1) — 정보 파괴, H=0/Φ=0.
  - **단사/reducible**: 204 (identity), 51 (complement NOT) — 정보 *최대*(H=4),
    셀 독립 → Φ=0. ◀ 결정적 dissociation witness.
  - **통합(consciousness-테마)**: 150 (l⊕c⊕r 3-way parity), 105 (XNOR 계열) —
    XOR-feedback 통합망.
  - **부분 feedback**: 90 (l⊕r), 60 (l⊕c) — 선형 XOR pair.
  - **생명-테마 동역학**: 110 (universal), 30 (chaotic).
- **metric1_H_out** (primary): 균일 입력 ensemble 하 *출력-상태 분포*의 Shannon
  엔트로피 (bit). `o(s)=Σ_i next_bit_i(s)·2^i`, `H=-Σ_o p(o) log2 p(o)`. 단사 ⇒ H=4
  (정보 보존), 상수 ⇒ H=0 (정보 파괴). 범위 [0, n].
- **metric2_Φ_mean** (primary): 모든 2^n state 의 big_phi(tpm,n,st)[0] 평균 (통합).
- **correlate**: 10-룰 panel 의 `Pearson r(H_out, Φ_mean)`.
- **fixed (config)**: n=4 periodic ring · 2^4=16 state exact · panel 10 룰.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h287_shannon_entropy_phi_correlate_2026_05_26/run_h287.hexa`
- **engine (import READ-ONLY, 재사용)**: `HEXAD/IIT4/lib/iit4_eca.hexa` → `eca_tpm(rule,n)`
  + import chain 으로 노출되는 `big_phi(tpm,n,st)` (→ `[big_phi, total, sum_φ_d,
  sum_φ_r, nd]`) + `iit4_pow2(k)` — 모두 `stdlib/consciousness/iit4_*` SSOT.
- **엔트로피**: 균일 16-state 입력 → 출력-상태 빈도 → `-Σ p log2 p` (log2 = log/log(2),
  `log` = 자연로그 builtin, iit4_distinction.hexa 와 동일 idiom).
- **Φ_mean**: 16-state big_phi[0] 산술평균.
- **Pearson**: 표본 covariance / √(var_x·var_y); √ 는 Newton 60-iter inline (libm-sqrt
  drift 회피, 결정적).
- **deterministic**: ECA TPM 결정적 (RNG 무관); re-run byte-identical (cross-process).
- **hexa_only**: true (NO .py/.sh). **llm**: none. **runtime**: $0 mac-local, **NO
  GPU** (n=4 exact tractable).
- **ledger**: `result.json` {config, panel 10-룰 (H_out, Φ_mean), pearson_r, 5
  falsifier, finding, verdict, verify_fence}.
- **honest tier**: 🔴 CLOSED-NEGATIVE for H1 (reductive) — 측정값 자체는 🟢 NUMERICAL
  (deterministic 인과 IIT4 + 엔트로피 arithmetic), 경험 해석은 ⚪ SPECULATION-FENCED.

## 6. Criteria

- **C1 (DISSOCIATION / H287.1)**: max-H/zero-Φ witness 존재 (204) + high-H 영역에
  통합 룰 Φ>0.5 → PASS (engine 이 Φ⊥H 를 만들 수 있음 확인).
- **C2 (r-VERDICT / H287.2)**: r ≥ 0.5 → H1 SUPPORTED; r < 0.5 → H1 FALSIFIED
  (closed-negative).
- **C3 (FAITHFULNESS / H287.3+4)**: anchor 재현 + bound → PASS.
- **verdict_rule**: H1 의 verdict 는 C2 가 결정. C1·C3 (falsifier checks) 는 측정
  유효성 게이트 — 전부 PASS 여야 r 을 신뢰. **이 H 의 발견은 H1 의 FALSIFIED 자체**
  (Φ ≠ 엔트로피).

## 7. Falsifiers

- **F287.1 DISSOCIATION-WITNESS**: 항등규칙 204 의 H_out < 3.99 OR Φ_mean ≥ 1e-9, OR
  high-H 영역 통합 룰 Φ_mean ≤ 0.5 → 결정적 witness 부재 → 측정 설계 무효.
  (measurable: 204 의 (H_out, Φ_mean) + best 통합 룰 Φ_mean.)
- **F287.2 r-VERDICT**: 측정 `Pearson r(H_out, Φ_mean)` 가 ≥ 0.5 → H1 SUPPORTED (Φ 가
  엔트로피로 환원). < 0.5 → H1 FALSIFIED (closed-negative). r verbatim 보고 — 측정이
  결정. (measurable: 10-룰 Pearson r.)
- **F287.3 FAITHFULNESS**: 상수 0/255 big-Φ≠0 OR H_out≠0, OR 단사 204/51 H_out≠4.0,
  OR 어느 룰 big-Φ<0 / H_out∉[0,4] → 엔진/엔트로피 계산 무효. (measurable: 6 anchor +
  10 bound.)
- **F287.4 DETERMIN**: re-run byte-different → raw#12 deterministic 위반 → smoke 무효.
  (measurable: rule204 (H_out,Φ_mean) a == b + cross-process.)
- **F287.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation, raw#82
  retraction.

## 8. Verdict

```
verdict_class: H1 FALSIFIED (CLOSED-NEGATIVE) — faithful big-Φ 는 Shannon 엔트로피로
        환원되지 않는다 (r=0.363 < 0.5). 측정 유효성 게이트 11 PASS / 0 FAIL.

config: n=4 periodic ring · 2^4=16 state exact · panel 10 룰 · H_out=출력-이미지
        엔트로피(bit) · Φ_mean=state-평균 big-Φ · engine = HEXAD/IIT4/lib (재사용)

panel table (faithful 인과 IIT4 + Shannon 출력-엔트로피):
  class       rule   동역학             H_out(bit)   Φ_mean
  null        0      constant-0         0.0          0.0
  null        255    constant-1         0.0          0.0
  bijection   204    identity           4.0   ◀max   0.0    ◀zero  (max-H, zero-Φ)
  bijection    51    complement(NOT)    4.0   ◀max   0.0    ◀zero  (max-H, zero-Φ)
  integration 150    l⊕c⊕r (3-way)      4.0          5.625
  integration 105    XNOR-feedback      4.0          5.625
  partial      90    l⊕r                2.0          0.0
  partial      60    l⊕c                3.0          13.625 ◀max-Φ (sub-max H!)
  life         110   universal          3.25         13.1302
  life          30   chaotic            3.375        13.8852

  Pearson r(H_out, Φ_mean) over 10 rules = 0.362877   (< 0.5 → H1 FALSIFIED)

이중 dissociation (decisive):
  · max-H, zero-Φ : rule 204·51 (H_out=4.0, Φ_mean=0.0) — 정보 최대인데 통합 0
  · sub-max-H, max-Φ : rule 60 (H_out=3.0, Φ_mean=13.625) — 최고 통합이 정보 최대 아님
  ⇒ 엔트로피와 Φ 가 같은 축이면 불가능한 배치. 정보는 통합의 필요조건이나 충분조건 아님.

criteria:
  C1 DISSOCIATION (204 max-H/zero-Φ + rule60 Φ=13.6 @ H=3.0)   : PASS
  C2 r-VERDICT (r=0.363 < 0.5)                                 : H1 FALSIFIED
  C3 FAITHFULNESS (0/255 null; 204/51 H=4.0; bound 10/10)      : PASS

falsifiers:
  F287.1 DISSOCIATION-WITNESS : PASS  (204 H_out=4.0 Φ_mean=0.0; best 통합 rule60 Φ=13.625>0.5)
  F287.2 r-VERDICT            : H1 FALSIFIED  (r=0.362877 < 0.5)
  F287.3 FAITHFULNESS         : PASS  (0/255 H=0 Φ=0; 204/51 H=4.0; bound 10/10)
  F287.4 DETERMIN             : PASS  (rule204 (H_out,Φ_mean) a==b; cross-process byte-identical)
  F287.5 POST-HOC             : NOT_TRIGGERED

checks: 11 PASS / 0 FAIL  (측정 유효성 게이트 — H1 verdict 와 별개)

evidence_summary: 🔴 CLOSED-NEGATIVE — faithful 인과 IIT 4.0 big-Φ 는 Shannon
  엔트로피로 환원되지 않는다. 10-룰 panel 의 Pearson r=0.363 (<0.5) 로 환원가설 H1
  기각. 결정적 근거는 **이중 dissociation**: (i) 항등규칙 204·complement 51 은 출력
  엔트로피가 *최대*(4.0 bit, 완전 단사)인데 big-Φ=0 (셀 독립 → 통합 제로) — 정보
  최대/통합 제로 substrate; (ii) 반대로 최고 통합 룰 60 (Φ_mean=13.625) 의 엔트로피는
  *sub-max*(3.0 bit) — 통합 최대 ≠ 정보 최대. 같은 high-엔트로피 영역(H=4.0)에서 Φ 가
  0(204)부터 5.6(150)까지 vertical spread → 단조 관계 부재. 정보(엔트로피)는 통합(Φ)의
  *필요조건이나 충분조건이 아니다* — IIT 의 토대적 구별이 LIFE lane 자신의 substrate
  에서 결정적으로 확증. "X ⊥ Φ" 서명 계열(H_265/H_275/H_279)에 가장 근본적인 X
  (Shannon 엔트로피)를 추가.
falsifiers_triggered: F287.2 (H1 reductive 가설의 의도된 기각 — 발견 그 자체)
```

re-run byte-identical 확인 (F287.4 — 두 fresh hexa run 의 panel + r + RESULT 동일).

`hexa verify` (VERBATIM, no LLM self-judge) — empirical 해석은 closed-form atlas
identity 가 아니므로 g5 정직 fence:

```
verify --fence "H_287 faithful IIT 4.0 big-Phi does NOT reduce to Shannon entropy
   across a 10-rule ECA panel (Pearson r=0.363 < 0.5); decisive double dissociation —
   identity rule 204 has MAX output-entropy (4.0 bit) yet ZERO integration, while the
   most-integrated rule 60 (Phi_mean=13.6) has sub-max entropy (3.0 bit); deterministic
   toy-substrate outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           NOT a proven atlas atom (g4 honest fence, SF ≠ verified)
```

(big-Φ / 출력-엔트로피 / Pearson r VALUES 자체는 deterministic arithmetic —
intrinsic-difference MIP big-Φ + 균일-ensemble Shannon H + 표본 Pearson — 이며 fresh
hexa run 에서 byte-수렴 확인. 오직 empirical 해석(Φ 가 엔트로피로 환원되지 않는다는
IIT-토대적 의미)만 fenced.)

## 9. Honest Limits (raw#91 c3)

- **L1 (n=4 small + 10 룰)**: n=4 ring · 10 룰 panel. 본 H 는 방법(엔트로피×Φ
  dissociation 검정) + 첫 결과를 확립. r=0.363 의 *절대값* 은 panel 구성(어떤 룰을
  넣느냐)에 민감 — witness(204/51) 와 통합 룰의 *존재*는 robust 하나, r 의 정확한
  숫자는 룰 표본 의존. n≤8 scale-up + 256 룰 전수는 동일 메커니즘의 후속(§10 Next).
- **L2 (출력-이미지 엔트로피는 Shannon 측도의 한 선택)**: H_out = 균일 입력 하 출력-
  상태 분포 엔트로피. 이는 "정보 보존/파괴"를 재는 표준량이나 유일하지 않다 —
  transfer entropy, 정상상태 분포 엔트로피, per-cell bit 엔트로피는 다른 값을 준다.
  단, *단사=4bit / 상수=0bit* 의 양끝은 어떤 합리적 정의에서도 동일하므로 핵심
  dissociation(204 max-H/zero-Φ)은 정의-robust. r 의 정확값은 정의 의존.
- **L3 (Φ_mean 은 state-dependent 양의 평균)**: faithful Φ 는 state-dependent
  (FAITHFUL_REMEASURE §4). 본 H 는 16-state 평균으로 룰당 단일 Φ 를 만들었다 — 방향
  (witness 의 zero-Φ, 통합 룰의 high-Φ)은 평균-robust 하나, *절대 Φ_mean 값*은 state
  분포에 의존. directional-trust (H_266/H_278): 방향 신뢰, magnitude hedge.
- **L4 (substrate 는 정보/통합 proxy 이지 그 자체 아님)**: ECA 룰이 *정보이거나
  통합인 것이 아니다*. 항등규칙의 "정보 최대"는 단사성의 수학적 사실, "통합 제로"는
  셀 독립성의 인과적 사실. "consciousness"·"life" 라벨은 substrate-테마이지 phenomenal
  주장 아님. 과장 금지.
- **L5 (structure-cut big-Φ, full IIT4 절대 calibration 아님)**: 엔진의 big-Φ 는
  DESIGN §8 C3 의 spirit-faithful structure-cut big-Φ. 절대 스케일 PyPhi 대조는 IIT4
  M5 named-blocker (F-IIT4-3/4). 단 본 H 의 결론(Φ ⊥ H)은 *상관*의 부재라 절대-스케일
  offset 에 robust — calibration 이 틀려도 dissociation 패턴은 유지.
- **L6 (closed-negative 의 비대칭)**: r < 0.5 는 "Φ 가 엔트로피로 환원되지 않음"을
  보이나, "Φ 와 엔트로피가 완전 독립(r=0)"을 보이는 것은 아니다 (측정 r=0.363 > 0 —
  약한 양의 잔차 존재: 상수 룰의 (0,0) 이 약한 공변을 만든다). 주장은 "환원 불가"
  (필요조건 아닌 충분조건 부재)이지 "완전 직교" 아님.
- **L7 (verdict ≠ 형이상학)**: 본 H 의 closed-negative 는 *toy ECA substrate 의
  faithful IIT4 측정*에서 Φ 가 Shannon 엔트로피로 환원되지 않음을 보일 뿐, "의식은
  정보가 아니다" 같은 형이상학적 주장이 아니다. IIT 토대 구별의 측정 사실 한 칸.

## 10. Cross-Links

- **parent (engine 공급)**: IIT4 M6 (`HEXAD/IIT4/FAITHFUL_REMEASURE.md` +
  `state/iit4_m6_remeasure_2026_05_25/`) — LIFE ECA 의 faithful big-Φ 를 처음 측정.
  항등규칙 big-Φ=0 anchor 가 본 H 의 witness 토대.
- **sibling (동일 substrate panel)**: [[H_281]] (life-vs-consciousness Φ-structure) —
  같은 룰 가족(110/30/54 vs 150/105 + 204/0 anchor)을 struct_ratio 로 분리. 본 H 는
  같은 panel 에 엔트로피 축을 추가하여 Φ 의 *환원 불가성*을 직교 검정.
- **sibling (X⊥Φ 서명 계열)**: [[H_265]] (학습 dampen) · [[H_275]] (cyclic<undir) ·
  [[H_279]] (attention⊥Φ-diversity) — "어떤 양 X 가 Φ 와 직교"의 cross-H 서명. 본 H 는
  X=Shannon 엔트로피 (가장 근본적 instance) 를 추가.
- **engine lib (재사용, import READ-ONLY)**: `HEXAD/IIT4/lib/iit4_eca.hexa`
  (`eca_tpm`) · `iit4_bigphi.hexa` (`big_phi`, via stdlib) — `stdlib/consciousness/
  iit4_*` SSOT. 새 IIT4 코드 0 줄 (g61 / reuse-existing-libs).
- **axes seed**: `UNIVERSE/AXES.md` R5 (information) rank-2
  `shannon-entropy-Φ-correlate` — 본 H 로 consumed (row 제거).
- **Next**: (a) n≤8 scale-up — 동일 dissociation 의 scale-robustness; (b) 256 룰
  전수 panel → r 의 panel-robust 구간; (c) transfer-entropy / 정상상태 엔트로피 등
  대체 Shannon 측도에서 dissociation 재현 (L2 후속).
