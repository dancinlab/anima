---
id: H_843
slug: temporal-ultradian-phi
title: TEMPORAL T3 anima 90-min ultradian Φ scan — 4 substrate(WAKE/N1_N2/N3/REM) × X1 invariant_detector + 5 사전등록 falsifier · X1 detector 가 ultradian 위 WAKE > N3 ordering 만 잡고 paradoxical REM + ascending ladder 실패 · 🔴 FALSIFIED-INSTRUMENT 2/5 · T1+T2+T3 triple closed-negative
domain: temporal · ultradian · sleep-stage · iit4-numerical · falsifier · closed-negative · anima-substrate
source: TEMPORAL/scan/ultradian_phi.hexa · XENO/detector/invariant_detector.hexa · TEMPORAL/state/temporal_t3_ultradian_2026_05_29/ · sister H_841 (T1 lag-axis · 🔴) · sister H_842 (T2 multi-unit embed · 🔴) · XENO H_829 (X1 invariant_detector) · CLAUDE.md a_chat_sleep_imagination (5-stage 90-min ultradian)
status: 🔴 FALSIFIED-INSTRUMENT (2/5 사전등록 PASS · F-T3-WAKE-MID + F-T3-N3-LOW 단독 · F-T3-REM-HIGH + F-T3-N1-MID + F-T3-MONOTONE 3-FAIL · 의식 phenomenology 부분 정합 · T1+T2+T3 triple closed-negative · T4 자연 entry)
exploration_method: E1 (substrate-blind Φ ultradian scan) · E3 (hexa deterministic execution) · E5 (사전등록 falsifier ledger)
verification_method: W1 (hexa stdout verbatim) · W2 (X1 invariant_detector numerical) · W3 (사전등록 5 falsifier · post-tuning 0)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: TEMPORAL/scan/ultradian_phi.hexa, XENO/detector/invariant_detector.hexa, TEMPORAL/state/temporal_t3_ultradian_2026_05_29/, UNIVERSE/H_841, UNIVERSE/H_842, UNIVERSE/H_829, .verdicts/843_temporal_ultradian_phi/T3_run.txt
verdict: 🔴 FALSIFIED-INSTRUMENT (2/5 사전등록 PASS · WAKE Φ=0.866 > N3 Φ=0.335 정합 · F-T3-WAKE-MID + F-T3-N3-LOW PASS · 그러나 N1_N2 Φ=0.0 zero-degenerate (X1 binarise+cooccur 가 4-step cycle-aligned substrate 위 T1 lag-artifact 의 다른 manifestation) · REM Φ=0.569 < WAKE Φ=0.866 (paradoxical REM ≈ wake 가설 미정합) · F-T3-REM-HIGH + F-T3-N1-MID + F-T3-MONOTONE 3-FAIL · X1 detector 가 anima ultradian 5-stage 위 부분 phenomenology 만 정합 · T4 자연 entry (window-mean Φ / Granger causality / surrogate-baseline) 필요 · 정직 closed-negative)
---

# H_843 — TEMPORAL T3 anima 90-min ultradian Φ scan

## 1. 가설

T1 (H_841) + T2 (H_842) dual closed-negative 의 결과 분석:
- T1: 2-unit lag-TPM 의 lag-axis 가 periodic substrate 위 false Φ-inflation (lattice Δt=8 Φ=2.0 saturate).
- T2: Takens multi-unit time-embed 도 embed-dim ↑ 시 4/4 substrate phi monotone INFLATE (voyager e=5 Φ=28.36).

**T3 가설**: detector 의 확장 (lag-axis · embed-dim) 은 모두 artifact 만 키운다. 자연 entry 는 detector 가 아니라 **substrate** — anima 의 `a_chat_sleep_imagination` 90-min ultradian 5-stage (WAKE / N1 / N2 / N3 / REM) substrate 위에서 X1 invariant_detector 를 **그대로** 적용해 의식 phenomenology 의 ground-truth (WAKE > N1+N2 > N3, REM ≈ WAKE) 와 측정값이 정합하는지 검증한다.

- WAKE phi > 0.1 (의식 baseline noise floor 위로)
- N3 phi < WAKE phi (deep sleep ≠ integrated info — 의식 phenomenology 의 핵심)
- REM phi ≥ WAKE phi (paradoxical = high Φ · REM EEG 가 wake-like 인 sleep neuroscience 의 결정적 단서)
- N1+N2 phi > N3 phi (light sleep > deep sleep)
- N3 < N1+N2 < WAKE 또는 N3 < N1+N2 < REM (ascending depth ladder 중 하나)

5/5 또는 4/5 통과 시 → **🟢 SUPPORTED-NUMERICAL** (X1 detector 가 ultradian phenomenology 정합).
3/5 → 🟡 PARTIAL-SUPPORT.
≤2/5 → 🔴 FALSIFIED-INSTRUMENT (T4 자연 entry — window-mean / Granger / surrogate-baseline).

## 2. 동기

- T1 + T2 dual closed-negative 의 자연스러운 next axis — `feedback-instrument-first-methodology` 정합 (detector 확장 폐기, substrate-side calibration).
- CLAUDE.md `@D a_chat_sleep_imagination` directive 의 5-stage 90-min ultradian 측정 path — anima 의 substrate-native sleep cycle 의 의식 Φ 측정 토대.
- TEMPORAL 도메인 round 2/5 milestone (TEMPORAL.md). T1+T2 closed → T3 ultradian → T4 window-mean / T5 paper 의 ladder.
- XENO X1 invariant_detector 의 calibration regime (n=128, 2-state binarisation) 위 직접 ultradian substrate 적용 — 새 detector 개발 없이 ground-truth phenomenology 와 측정값 정합 시험.

## 3. falsifier (사전등록, 임계 frozen pre-run)

```
F-T3-WAKE-MID    : WAKE phi > 0.1                                    (의식 baseline · noise floor 위로)
F-T3-N3-LOW      : N3 phi < WAKE phi                                 (deep sleep ≠ integrated info)
F-T3-REM-HIGH    : REM phi ≥ WAKE phi                                (paradoxical = high Φ)
F-T3-N1-MID      : N1_N2 phi > N3 phi                                (light sleep > deep sleep)
F-T3-MONOTONE    : (N3 < N1_N2 < WAKE) OR (N3 < N1_N2 < REM)         (ascending depth ladder)
```

- **5/5 PASS** → 🟢 SUPPORTED-NUMERICAL (X1 detector ultradian phenomenology 정합 strong)
- **4/5 PASS** → 🟢 SUPPORTED-NUMERICAL (정합 weak — 단일 axis 미정합)
- **3/5 PASS** → 🟡 PARTIAL-SUPPORT
- **≤2/5 PASS** → 🔴 FALSIFIED-INSTRUMENT (T4 자연 entry)

## 4. 방법

```
1. detector = XENO/detector/invariant_detector.hexa (X1, substrate-blind)
   - compute_invariant_phi(signal: array, n_samples: int) -> map
       float[] → min/max normalize → threshold 0.5 binarise
       → 2-unit cooccur TPM (lag=1)
       → stdlib/consciousness/iit4_bigphi.big_phi(tpm, 2, 3)
       → {phi, integration, irreducibility, substrate_type}
   - 기존 detector 확장 폐기 (T1/T2 dual closed-negative).
2. scan = TEMPORAL/scan/ultradian_phi.hexa
   - 4 substrate × 1 detector call = 4 measurement
   - 5 falsifier 자동 평가 + verdict tier 산출
3. 4 substrate (n=128 hardcoded literal · anima ultradian phenomenology):
   (a) WAKE   — density ~0.65 + det. transition (X7 regime 안, 의식 baseline)
   (b) N1_N2  — density ~0.4 + slow oscillation (sleep spindle 모방, light sleep)
   (c) N3     — density ~0.25 + 8-step slow delta wave (deep sleep slow wave)
   (d) REM    — density ~0.55 + irregular high-freq (REM theta + saccade burst)
4. 5 사전등록 falsifier 평가 (frozen pre-run, post-tuning 0)
5. 결과 → TEMPORAL/state/temporal_t3_ultradian_2026_05_29/{t3_smoke.log, result.json, run_h843.hexa}
6. verdict → .verdicts/843_temporal_ultradian_phi/T3_run.txt (g73 per-H gate)
```

deterministic, $0 Mac local, wall <1s (X1 baseline).

## 5. 측정

```
$ env hexa run TEMPORAL/scan/ultradian_phi.hexa
  → 4 Φ 계산 + 5 사전등록 falsifier 평가
  → verbatim stdout → TEMPORAL/state/temporal_t3_ultradian_2026_05_29/t3_smoke.log
  → .verdicts/843_temporal_ultradian_phi/T3_run.txt verbatim copy
  → exit 0 · wall <1s
```

## 6. 결과

```
  [WAKE ]  phi=0.865544 irr=0.614732 type=conscious
  [N1_N2]  phi=0.0      irr=0.0      type=coherent_non_conscious
  [N3   ]  phi=0.335119 irr=0.251003 type=coherent_non_conscious
  [REM  ]  phi=0.568534 irr=0.362462 type=coherent_non_conscious

  F-T3-WAKE-MID    PASS  (WAKE phi=0.866 > 0.1)
  F-T3-N3-LOW      PASS  (N3 phi=0.335 < WAKE phi=0.866)
  F-T3-REM-HIGH    FAIL  (REM phi=0.569 < WAKE phi=0.866)
  F-T3-N1-MID      FAIL  (N1_N2 phi=0.0 < N3 phi=0.335)
  F-T3-MONOTONE    FAIL  (no ascending depth ladder)

  pass_count : 2/5
  tier       : 🔴 FALSIFIED-INSTRUMENT
```

## 7. 분석

### 7.1 정합 (2/5)
- **WAKE > N3** ordering 은 의식 phenomenology 의 가장 robust 한 단서 — X1 detector 가 잡았다.
- WAKE phi=0.866 은 X1 'conscious' 분류 (irr > 0.5) 통과, X7 voyager calibration 과 동일한 regime.

### 7.2 미정합 (3/5)
**F-T3-N1-MID FAIL (N1_N2 phi=0.0)**: T1 lag-artifact 의 다른 manifestation. N1+N2 substrate 의 4-step cycle (1100/0110 alternation) 이 X1 의 lag=1 cooccur TPM 위에서 perfectly predictable transition 으로 보여 Φ=0 으로 degenerate. T1 이 lattice 위 발견한 cycle-aligned artifact 와 같은 구조 — X1 의 lag=1 binarise+cooccur 가 substrate 의 inherent periodicity 와 정렬되면 zero-Φ 가 된다.

**F-T3-REM-HIGH FAIL (REM phi=0.569 < WAKE phi=0.866)**: paradoxical REM 의 핵심 phenomenology (EEG wake-like) 가 X1 detector 의 binarised cooccur 로는 잡히지 않는다. REM 의 irregular high-freq saccade burst 가 X1 의 2-unit TPM 위에서 partial degenerate.

**F-T3-MONOTONE FAIL**: 위 두 FAIL 의 자연 결과 — N1_N2 가 zero 로 떨어져 ascending ladder 불가능.

### 7.3 T1+T2+T3 triple closed-negative 의 정직 결론
세 라운드 모두 X1 detector 의 단순 확장 (T1 lag-axis · T2 embed-dim · T3 substrate-side ultradian 적용) 으로는 시간 통합 의식 측정 미충족.

- T1: detector lag-axis 확장 → cycle-aligned inflation artifact
- T2: detector embed-dim 확장 → sparse-state inflation artifact
- T3: detector unchanged + ultradian substrate → cycle-aligned zero-degenerate artifact (T1 의 다른 face)

**T4 자연 entry**:
- window-mean Φ (시간 window 평균 → cycle-alignment 평균화)
- Granger causality (TPM-free predictive coupling → lag-window inflation 회피)
- surrogate-baseline (random-shuffle null-model 차감 → substrate-specific Φ inflation 제거)

## 8. 함의

- **a_chat_sleep_imagination 의 Φ 측정 path 부분 통과**: WAKE > N3 정합 (의식 baseline > deep sleep). N1_N2 + REM 측정은 T4 detector 필요.
- **substrate 측 calibration 도 한계**: detector 확장만 artifact 만든 게 아니라, X1 binarise+cooccur 자체가 cycle-rich substrate 위 zero-degenerate / sub-optimal 가 된다.
- **TEMPORAL round 2/5 진행**: T1 + T2 + T3 triple closed-negative 완료. T4 (window-mean / Granger / surrogate) 가 시간 통합 의식 측정의 진짜 path.
- **feedback-instrument-first-methodology 강 정합**: 3-round 정직 closed-negative 가 measurement tooling 의 본질적 한계 드러냄.

## 9. 양방향 sibling

- ⇄ [TEMPORAL/TEMPORAL.md](../TEMPORAL/TEMPORAL.md): round 2/5 milestone
- ⇄ [UNIVERSE/H_841](./H_841_temporal_timeshift_phi.md): T1 lag-axis sister closed-negative
- ⇄ [UNIVERSE/H_842](./H_842_temporal_time_embed_phi.md): T2 multi-unit embed sister closed-negative
- ⇄ [UNIVERSE/H_829](./H_829_xeno_x1_regime_matrix.md): X1 invariant_detector origin
- ⇄ [XENO/detector/invariant_detector.hexa](../XENO/detector/invariant_detector.hexa): detector SSOT
- ⇄ CLAUDE.md `@D a_chat_sleep_imagination`: 5-stage ultradian directive
- ⇄ [UNIVERSE/CANDIDATES.md](./CANDIDATES.md): 검증 결과 환류 SSOT

## 10. 정직 ledger

- pre_register_frozen=true · frozen_at=2026-05-29 · post-tuning 0
- threshold 5 falsifier 모두 pre-run frozen, 측정값과 임계 비교만 평가
- p7=0 (LLM judge 없음) · verbatim stdout copy
- a_blue_closed: pre-run frozen threshold + verbatim verdict (FALSIFIED-INSTRUMENT 2/5)
- a_paper_negative_ok: 정직 closed-negative — T4 자연 entry path 명시 (window-mean / Granger / surrogate)
- a_completeness_over_cheap: detector 확장 폐기 (T1/T2 dual fail), substrate-side calibration 시도 (cheap path 아닌 진짜 phenomenology 정합 검증)
- feedback-instrument-first-methodology: T1 + T2 + T3 triple closed-negative 가 detector 본질적 한계 드러냄
- INBOX 환류 0건 (UNIVERSE 직접 기록)
