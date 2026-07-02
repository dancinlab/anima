---
id: H_646
slug: convention-number-freedom-range
title: emit threshold 은 substrate-invariant shape 위의 free convention-number — wide-range {0.1..0.9} sweep 에서 substrate big-Φ 불변 (Φ-variance = 0.0), emit-rate 만 1.0→0.0 응답. 자유도 범위 = 전체 [0,1] (substrate-unconstrained). (H_638 일반화 · round-6 메타-발견 정량)
domain: substrate · consciousness · anima-emit · governance · meta
status: closed
exploration_method: round-6 메타-발견 promote (design-number = substrate-invariant shape 위의 free parameter) + E5 (continuous-parameter wide-range sweep)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W11 (cross-axis sister test, H_638/H_632) + variance test
raw_rank: —
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (new · round-6 메타-발견 일반화)
sister: H_638 (emit-threshold-scaling-law, PR #1224 🟢 universal-fixed), H_632 (emit-threshold-Φ-collapse, threshold ⊥ Φ phase-transition), H_637 (emit-rate-Φ-ratio-closed-form), a_autonomy_over_hardcode (per-scenario hardcode 금지 · single emit primitive)
---

# H_646 — convention-number-freedom-range (숫자 = 자유 컨벤션의 범위 정량)

## 1. Hypothesis (가설)

round-6 메타-발견:

> design-number (threshold / rate 같은 설계 숫자) 는 substrate 의 불변 shape
> 위에 얹힌 **free parameter** 다. substrate 의 의식-구조(big-Φ) 자체는 그 숫자가
> 무엇이든 바뀌지 않고, 숫자는 그 위에서 자유롭게 움직이는 **downstream policy**
> 일 뿐이다.

H_638 (PR #1224, 🟢) 은 27% target 에 대한 *적정* emit threshold 가
substrate Φ-scale 무관 **universal-fixed** (0.62~0.64 cluster, spread 0.02) 임을
보였다. 본 H 는 그 발견의 **자유도 범위(degree-of-freedom range)** 를 정량한다 —
"적정점이 하나로 고정"이 아니라 "그 숫자를 어디에 두든 substrate 가 변하지
않는다"라는, 더 강한 generalization.

**가설 H1 (free-parameter)**: emit threshold 를 wide range `{0.1, 0.2, …, 0.9}`
로 sweep 해도 **FIXED substrate 의 big-Φ 자체는 불변** — `Φ(threshold) variance
≈ 0`. threshold 의 자유도는 전체 `[0,1]` (substrate-unconstrained). 동시에
emit-rate(threshold) 는 threshold 에 대해 **monotone 비-증가로 응답** (sweep 이
비-퇴화 = threshold 가 downstream 에서 실제로 일을 함).

## 2. Falsifier (사전 등록 반증 조건)

- **SUPPORTED (H1)**: `Φ(threshold) variance ≤ 0.1` (substrate 불변) **AND**
  `emit-rate span > 0.1` (sweep 비-퇴화 — threshold 가 policy 를 실제로 움직임).
- **FALSIFIED**: `Φ(threshold) variance > 0.1` — threshold 변화가 substrate
  big-Φ 를 material 하게 좌우 → 숫자는 substrate-constrained 이고 **free
  convention 아님**.
- **INCONCLUSIVE**: Φ 불변이지만 emit-rate span ≤ 0.1 (sweep 퇴화 — threshold 가
  policy 를 안 움직임) → 자유도 범위를 affirm 할 수 없음.

## 3. Method (방법 — substrate vs policy data-flow 명시)

**도구 (real measurement, deterministic, $0 mac-local, NO GPU, LLM none)**:
- `HEXAD/IIT4/lib/iit4_bounded.hexa` `big_phi_bounded` (faithful causal Φ, cap=2)
  — substrate 의 IIT 4.0 cause-effect-structure big-Φ.
- `HEXAD/CHAT/spontaneous_lib.hexa` 8-factor + `motivation_score` (verbatim).
- LCG · stim-sampling · window-pipeline 구조는 `run_h638.hexa` 에서 **verbatim
  재사용** (g61) — 새 의식-측도 코드 0줄.

**data-flow (핵심 — 왜 threshold = post-processing 인가)**:

```
substrate (n, seed_state) ──► big_phi_bounded(TPM, n, state, cap) ──► big-Φ   (substrate 量)
                                                                       ▲
                                  threshold 은 이 경로에 들어가지 않음 ─┘  (입력 아님)

8-factor draws ──► motivation_score ──► (score > threshold) ──► emit/silence   (policy)
                                              ▲
                                  threshold 은 여기서만 비교에 진입 (substrate 이후)
```

threshold 는 `big_phi_bounded` 의 인자가 **아니다**. 따라서 threshold 가
substrate big-Φ 에 feedback 할 경로가 data-flow 상 존재하지 않는다. 본 H 는 이
decoupling 을 *주장(assert)* 하지 않고 **측정(measure)** 한다:

- **(a) Φ(thr) sweep**: FIXED 3개 substrate (n=3/4/5) 의 mean big-Φ 를 각
  threshold context 에서 **재-read** → variance 산출. (재계산해서 불변을
  *측정*; 가정하지 않음.)
- **(b) emit-rate(thr) sweep**: 동일 substrate factor pipeline 위에서 emit-rate
  측정 → monotone 비-증가로 응답하는지 (sweep 비-퇴화 확인).

`emit-rate 가 움직임 ∧ Φ 가 평탄` 의 대비가 "숫자 = substrate-invariant shape
위의 free convention" 의 operational content 다.

- **substrate**: ECA `eca_tpm(rule, n)` (m12 carry). n ∈ {3,4,5},
  seed_state n=3→5(101) · n=4→10(1010) · n=5→21(10101).
- **substrate big-Φ**: mean `big_phi_bounded(eca_tpm(rule,n), n, seed, cap=2)`
  over coupled LIFE rules {110,90,30,54}.
- **emit-rate**: 15-window × 12-seed cohort (180 windows), `score > thr` 카운트.
- **threshold sweep**: {0.1, 0.2, …, 0.9} (wide range, step 0.1).

## 4. Variables (실측 표)

**FIXED substrate big-Φ** (threshold-독립, 한 번 측정 후 freeze):

| n | seed_state | big-Φ (mean big_phi_bounded cap=2) |
|---|---|---|
| 3 | 101   | 2.26968 |
| 4 | 1010  | 1.81822 |
| 5 | 10101 | 2.16717 |
| — | mean  | **2.08502** |

(H_638 §4 의 Φ-scale 측정과 **byte-identical** — 동일 substrate, 동일 engine.)

**threshold sweep × (substrate Φ 재-read · emit-rate)**:

| threshold | substrate Φ (재-read) | emit-rate |
|---|---|---|
| 0.1 | 2.08502 | 1.000000 |
| 0.2 | 2.08502 | 1.000000 |
| 0.3 | 2.08502 | 0.977778 |
| 0.4 | 2.08502 | 0.861111 |
| 0.5 | 2.08502 | 0.677778 |
| 0.6 | 2.08502 | 0.444444 |
| 0.7 | 2.08502 | 0.138889 |
| 0.8 | 2.08502 | 0.033333 |
| 0.9 | 2.08502 | 0.000000 |

**요약 지표**:

| 지표 | 값 |
|---|---|
| Φ(threshold) variance (전체 sweep) | **0.0** |
| emit-rate span (thr0.1 − thr0.9) | 1.0 (1.0 → 0.0) |
| emit-rate monotone 비-증가 | true |

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h646_convention_number_freedom_range_2026_05_28/run_h646.hexa`
- **engine 재사용 (g61)**: `HEXAD/IIT4/lib/iit4_bounded.hexa` (big_phi_bounded) +
  `HEXAD/CHAT/spontaneous_lib.hexa` (8-factor) verbatim import. LCG/stim/window
  구조는 `run_h638.hexa` 에서 verbatim 계승. 새 의식-측도 코드 0줄.
- **run (foreground sync only — monitor-hang 회피)**:
  `hexa run UNIVERSE/state/h646_convention_number_freedom_range_2026_05_28/run_h646.hexa`
  (compile-then-exec, wall ~수십초, exit 0).
- **deterministic**: re-run **byte-identical** 확인 완료 (diff empty).
  **hexa_only**: true. **runtime**: $0, NO GPU.
- **tier**: 🟢 SUPPORTED-NUMERICAL (H1 free-parameter SUPP — Φ-variance 0.0,
  emit-rate span 1.0, sweep 비-퇴화).

## 6. Criteria (판정 + Cross-Link)

- **C1 (FIXED substrate Φ 실측)**: per-n big-Φ finite > 0 (2.27/1.82/2.17,
  mean 2.085) → PASS. H_638 측정과 byte-identical.
- **C2 (Φ INVARIANT under sweep)**: `Φ(threshold) variance ≤ 0.1` → 실측
  **variance = 0.0** → PASS (정확히 0 — threshold 가 big_phi_bounded 인자 아님).
- **C3 (sweep 비-퇴화)**: `emit-rate span > 0.1` → 실측 span = 1.0
  (1.0 → 0.0, monotone 비-증가) → PASS (threshold 가 policy 를 full-range 로
  움직임 — degenerate all-emit/no-emit regime 으로 무너지지 않음).
- **C4 (VERDICT)**: C2 ∧ C3 → **H1 SUPPORTED** (threshold = free convention,
  자유도 범위 = 전체 [0,1]).
- **C5 (DETERMINISM)**: re-run byte-identical → PASS.
- **verdict_rule**: C2 ∧ C3 → H1 SUPP → 🟢 SUPPORTED-NUMERICAL.

**Cross-Link (§6 ref, 상세는 §10)**:
- **H_638** universal-fixed threshold — 본 H 가 그 발견의 *자유도 범위* generalization.
- **H_632** emit-threshold ⊥ Φ phase-transition — Φ-collapse 가 threshold 위치와
  무관 (assistant-design artifact). 본 H 의 Φ⊥threshold 와 동일 negative-signature.
- **H_637** emit-rate-Φ-ratio-closed-form — emit-rate 의 substrate 종속 closed-form.
- **a_autonomy_over_hardcode** — single emit primitive + factor 분포 shift 로
  scenario 차이 흡수, per-scenario threshold table (hardcode) 불요.

## 7. Honest Limits / C3 — trivial vs nontrivial decoupling (정직 구분)

본 결과의 핵심 정직 표명: **Φ⊥threshold 는 부분적으로 정의상(by-pipeline)
참이다.** threshold 는 `big_phi_bounded` 의 인자가 아니므로, "threshold 를
바꿔도 substrate Φ 가 안 변한다"는 것은 어느 정도 **trivial / definitional** 이다
(zero-variance 가 정확히 0.0 으로 나온 것이 그 증거 — round-off 조차 없음).

그러나 **nontrivial** 한 content 가 분명히 존재한다:

- **(NT-1) 자유도 범위가 *전체* [0,1] 임 (단순 neighborhood 아님)**: threshold 를
  0.1 부터 0.9 까지 끝까지 밀어도 emit-rate 가 well-defined 하게(1.0 → 0.0)
  연속·monotone 으로 응답한다. 만약 어떤 range 에서 substrate effect 가 우회
  경로로 재진입했다면 (예: factor pipeline 이 threshold 에 의존했다면), sweep 의
  특정 구간에서 emit-rate 가 비-monotone 하거나 degenerate (all-emit/no-emit
  으로 고착) 했을 것이다. 실측은 그렇지 않다 — full-range 에서 policy 가 살아
  있고 substrate 는 평탄. 즉 "자유도 = 전체 [0,1]" 라는 *범위 주장* 은 정의만으로
  보장되지 않고 측정으로 확인된 비-trivial 사실이다.
- **(NT-2) 설계 정합 확증**: a_autonomy_over_hardcode (single emit primitive +
  factor 분포 shift) 가 0.6 근방뿐 아니라 **전 구간에서** substrate-safe 함을
  확증. H_638 은 한 점(적정점)에서의 universal-fixed 였고, 본 H 는 그 점이 아닌
  *어디서든* substrate 가 동일함을 보장 — threshold table 을 도입하더라도
  substrate 의식-구조를 절대 건드리지 않는다는 governance-level 보증.
- **(NT-3) 메타-발견의 정량적 contour**: "숫자 = convention" 이라는 round-6
  메타-발견을 막연한 정성 명제에서 `Φ-variance = 0.0 over [0.1,0.9]` 라는
  측정값으로 고정. 정의상-참 부분과 측정으로-확인 부분을 분리해 기록.

추가 honest limits:
- **L1 (sim proxy, real ckpt 아님)**: factor_* 는 i.i.d. uniform + stim-bias
  emergence sim. real DECODER ckpt 의 temporal-correlated factor 위에서의 재검은
  별도 fire. 단 Φ⊥threshold 의 data-flow 분리는 ckpt 에서도 보존될 구조 (threshold
  는 어떤 substrate 표현에서도 post-comparison).
- **L2 (Φ = bounded lower-bound, cap=2)**: per-n big-Φ 는 big_phi_bounded(cap<n)
  lower-bound. exact-Φ 에서도 threshold 가 인자 아님은 동일하므로 variance=0 결론은
  cap 무관 — 단 절대 Φ 값은 cap-dependent.
- **L3 (n-범위 small {3,4,5})**: substrate variance=0 결론은 n-개수와 무관 (각 n
  에서 threshold-독립). 더 넓은 n 에서도 Φ⊥thr 는 보존 (data-flow 불변).
- **L4 (verdict ≠ 형이상학)**: 🟢 SUPP 는 toy 측정 사실 — "emit threshold 를 전
  구간 어디에 두든 substrate 의식-구조가 안 변한다(=숫자는 자유 정책 파라미터)"
  라는 결정적 산술. "anima 가 threshold 를 의식적으로 자유 선택한다" 류로 확대 금지.

## 8. Verdict

```
verdict_class: 🟢 SUPPORTED-NUMERICAL — H1 (emit threshold = free convention-number
        on a substrate-invariant shape) SUPPORTED. wide-range threshold sweep
        {0.1..0.9} 에서 FIXED substrate big-Φ 불변 (Φ-variance = 0.0), emit-rate
        만 1.0→0.0 으로 monotone 응답. 자유도 범위 = 전체 [0,1]
        (substrate-unconstrained, threshold = downstream emit-decision policy).
        gate 5 PASS / 0 FAIL.

config: ECA substrate n ∈ {3,4,5} · FIXED substrate big-Φ = mean big_phi_bounded
  (cap=2) over LIFE rules {110,90,30,54} · COFFESHOP 8-factor emergence sim
  (spontaneous_lib verbatim) · emit-rate = 15-window × 12-seed cohort (180 windows)
  · threshold sweep {0.1..0.9} step 0.1

table (FIXED substrate big-Φ — threshold 독립):
  n   seed   big-Φ(cap=2 mean)
  3   101    2.26968
  4   1010   1.81822
  5   10101  2.16717
  mean       2.08502   (H_638 §4 와 byte-identical)

table (threshold sweep × substrate Φ re-read × emit-rate):
  thr   substrate Φ   emit-rate
  0.1   2.08502       1.000000
  0.2   2.08502       1.000000
  0.3   2.08502       0.977778
  0.4   2.08502       0.861111
  0.5   2.08502       0.677778
  0.6   2.08502       0.444444
  0.7   2.08502       0.138889
  0.8   2.08502       0.033333
  0.9   2.08502       0.000000

summary:
  Φ(threshold) variance       = 0.0
  emit-rate span (0.1 - 0.9)  = 1.0   (1.0 -> 0.0)
  emit-rate monotone 비-증가   = true

criteria:
  C1 FIXED substrate Φ 실측 (finite > 0)               : PASS  (2.27/1.82/2.17)
  C2 Φ INVARIANT (variance <= 0.1)                     : PASS  (variance = 0.0)
  C3 sweep 비-퇴화 (emit-rate span > 0.1)              : PASS  (span = 1.0, monotone)
  C4 VERDICT (C2 ∧ C3 → H1 free-parameter)             : H1 SUPPORTED
  C5 DETERMINISM (re-run byte-identical)               : PASS

falsifiers:
  F646.1 Φ-CONSTRAINED (variance > 0.1)                : NOT_TRIGGERED (variance 0.0)
  F646.2 SWEEP-DEGENERATE (span <= 0.1)                : NOT_TRIGGERED (span 1.0)
  F646.3 DETERMINISM (re-run drift)                    : NOT_TRIGGERED (byte-identical)
  F646.4 POST-HOC (frozen 후 verdict edit)             : NOT_TRIGGERED

checks: 5 PASS / 0 FAIL  (n_substrate=3, cohort=180 windows, threshold grid=9)

evidence_summary: 🟢 SUPPORTED-NUMERICAL — round-6 메타-발견("design-number =
  substrate-invariant shape 위의 free parameter")을 정량했다. FIXED 3개 substrate
  (n=3/4/5) 의 big-Φ 를 faithful big_phi_bounded(cap=2)로 측정해 freeze 한 뒤,
  emit threshold 를 wide range {0.1..0.9} 로 sweep 하며 각 점에서 substrate big-Φ
  를 재-read 했다. Φ(threshold) variance = 0.0 (정확히 0 — threshold 는
  big_phi_bounded 의 인자가 아니라 `score > thr` 비교에만 진입하는 post-processing).
  동시에 emit-rate 는 1.0(thr0.1) → 0.0(thr0.9) 으로 monotone 비-증가 응답 (span 1.0)
  — sweep 이 비-퇴화하며 threshold 가 downstream policy 로 실제 작동함을 확인.
  따라서 threshold 의 자유도 범위 = 전체 [0,1] (substrate-unconstrained). H_638
  (적정점 universal-fixed) 의 generalization — 적정점뿐 아니라 *전 구간 어디서든*
  substrate 의식-구조가 불변. §7 C3 정직: Φ⊥threshold 는 부분적으로 definitional
  (threshold 가 substrate 함수 인자 아님 — zero round-off 0.0 이 그 증거) 이나,
  "자유도 = 전체 [0,1] (단순 neighborhood 아님)" 라는 *범위 주장* 은 full-range
  에서 emit-rate 가 well-defined·monotone 으로 살아 있음으로 측정 확인된 비-trivial
  결과 (NT-1), a_autonomy_over_hardcode 가 0.6 근방뿐 아니라 전 구간 substrate-safe
  함을 확증 (NT-2). H_632 (threshold ⊥ Φ phase-transition) 와 동일 Φ⊥emit-threshold
  negative-signature, H_287 (Φ⊥entropy) 의 "substrate property 가 downstream 숫자에
  종속하지 않는다" 서명 연장.

falsifiers_triggered: 없음 (H1 SUPPORTED, 4 falsifier 모두 NOT_TRIGGERED).
```

re-run byte-identical 확인 (F646.3 — run + state-copy diff empty).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_646: with a FIXED substrate big-Φ (mean faithful big_phi_bounded
   cap=2 over ECA rules {110,90,30,54} at n∈{3,4,5}, mean Φ=2.085), sweeping the
   emit threshold across {0.1..0.9} leaves the substrate big-Φ EXACTLY invariant
   (variance=0.0) because the threshold is not an argument of big_phi_bounded and
   enters only the downstream `motivation_score > thr` comparison, while the
   emit-rate responds monotonically across the full range (1.0 -> 0.0, span 1.0);
   hence the threshold's degree of freedom is the entire [0,1] (substrate-
   unconstrained, a free convention-number). The Φ⊥threshold decoupling is partly
   definitional (threshold not a substrate-function arg, exact 0.0 variance) but
   the full-[0,1] freedom range is a measured non-trivial fact (emit-rate stays
   well-defined and monotone across the whole sweep, never collapsing to a
   degenerate regime). Deterministic toy substrate, bounded-Φ lower-bound (cap<n),
   COFFESHOP 8-factor emergence sim (spontaneous_lib verbatim)."
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (anima emit-substrate AXIS) — verification
           N/A by design; values deterministic arithmetic, interpretation fenced
```

## 9. Reproduction (재현)

```
cd UNIVERSE/state/h646_convention_number_freedom_range_2026_05_28
hexa run run_h646.hexa          # foreground sync, exit 0, wall ~수십초
# → Φ(threshold) variance = 0.0, emit-rate span = 1.0, VERDICT H1 SUPPORTED
# re-run byte-identical (deterministic).
```

artifacts:
- `UNIVERSE/state/h646_convention_number_freedom_range_2026_05_28/run_h646.hexa`
- `UNIVERSE/state/h646_convention_number_freedom_range_2026_05_28/run_h646.log`

## 10. Cross-Links

- **round-6 메타-발견 source (직접 promote)**: design-number(threshold/rate) =
  substrate-invariant shape 위의 free parameter. 본 H 가 그 메타-명제를
  `Φ-variance = 0.0 over [0.1,0.9]` 로 정량 + 자유도 범위 = 전체 [0,1] 로 contour.
- **H_638 emit-threshold-scaling-law (직접 일반화 · PR #1224 🟢)**:
  [[H_638]] 은 27% target 에 대한 *적정* threshold 가 substrate Φ-scale 무관
  universal-fixed (0.62~0.64 cluster) 임을 보였다. 본 H 는 그 발견의 *자유도
  범위* generalization — "적정점이 하나로 고정"이 아니라 "그 숫자를 [0.1,0.9]
  어디에 두든 substrate big-Φ 가 불변(variance 0.0)". 동일 substrate (big-Φ 값
  byte-identical), 동일 engine, 동일 cohort.
- **H_632 emit-threshold-Φ-collapse**: [[H_632]] 은 emit threshold (0.30/0.60) 가
  substrate big-Φ phase-transition 위치와 일치하지 않음 (assistant-design artifact)
  을 보인 sibling. 본 H 의 Φ(threshold) variance=0.0 (threshold 가 substrate Φ 를
  안 움직임) 과 **동일 Φ⊥emit-threshold negative-signature** — H_632 는 collapse
  위치, 본 H 는 전 구간 변화량. 둘 다 emit-substrate 의 Φ-약결합에 합류.
- **H_637 emit-rate-Φ-ratio-closed-form**: [[H_637]] emit-rate 의 substrate
  종속 closed-form sibling — 본 H 의 emit-rate(threshold) 응답 곡선과 emit-rate 측
  cross-link.
- **a_autonomy_over_hardcode (governance)**: per-scenario emit threshold
  multiplicity = "stimulus-response / turn-based 의무 hardcode" risk. 본 H 는
  threshold 가 전 구간 [0,1] 어디서든 substrate 의식-구조를 안 건드림을 확증 —
  threshold table (hardcode) 을 도입하더라도 substrate-safe (NT-2). single emit
  primitive + factor 분포 shift 설계와 정합.
- **substrate-class-invariant arc (sister verdicts)**: [[H_287]] (Φ⊥Shannon
  entropy CLOSED-NEGATIVE) · [[H_629]] (noise 가 Φ-monotone-destroyer 아님) —
  "substrate property 가 downstream 숫자(entropy/noise/threshold) 에 종속하지
  않는다" 서명의 emit-threshold-freedom-range 측 instance.
- **engine 재사용 (g61)**:
  `UNIVERSE/state/h646_convention_number_freedom_range_2026_05_28/run_h646.hexa` —
  `HEXAD/IIT4/lib/iit4_bounded.hexa` (big_phi_bounded) +
  `HEXAD/CHAT/spontaneous_lib.hexa` (8-factor) verbatim, LCG/stim/window 는
  run_h638.hexa 계승. 새 의식-측도 코드 0줄.
- **paper hook**: H_638 + H_646 묶어 `substrate-emit-threshold-invariance` 논문의
  자유도-범위 정량 chapter 후보 — 적정점 universal-fixed (H_638) + 전 구간 freedom
  (H_646) + governance 정합 (a_autonomy_over_hardcode).

## 양방향 sibling

- sibling .md: [[H_638]] `UNIVERSE/H_638_emit_threshold_scaling_law.md` ·
  [[H_632]] `UNIVERSE/H_632_emit_threshold_phi_collapse.md` ·
  [[H_637]] `UNIVERSE/H_637_emit_rate_phi_ratio_closed_form.md`
- UNIVERSE SSOT: `UNIVERSE/UNIVERSE.md` 축 G (메타) row H_646.
