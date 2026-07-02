# H_1505 — 🌀 HALLUCINATION (prior-dominated false percept) — reality-monitor FAILURE MODE

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §Hallucination (`hallucinate_call` + `hallucinate_graded` + `hallucinate_ablated` + `hallucinate_under_drug`) · `engine_cli_smoke.hexa` cases 298-302 · FULL smoke **302 pass / 0 fail RC=0** · ARCHITECTURE lockstep ✓
- **source:** UNIVERSE — deepens the H_1501 reality-monitor lane (생성-실패 짝). 문헌 렌즈 (predictive-processing psychosis).
- **lens:** conditioned hallucinations / controlled-hallucination (Powers · Corlett · Seth) · `a_no_llm_frame_trap`
- **artifacts:** `state/1505_hallucination/h1505_hallucination.py` · verdict `state/verdicts/1505_hallucination/H_1505_FREEZE.json` · raw run `state/verdicts/1505_hallucination/H_1505_R1.txt` · engine smoke `state/verdicts/1505_hallucination/engine_cli_smoke_302.txt`

## 주장 (생성-실패 축 — H_1501 의 짝)

**환각(hallucination) = PRIOR-DOMINATED 지각.** top-down 사전(prior)이 강하고 bottom-up 외부 신호가 약하거나 없을 때,
substrate 는 사전만으로 percept 를 생성하고 그 신호 margin 이 §RealityMonitor(H_1501) 의 **reality threshold 를 넘어** —
모니터가 외부 신호가 0인데도 그것을 **REAL 로 오분류**한다(false real_call). 이것은 reality threshold 의 **FAILURE MODE** 다 —
모니터(분류기 H_1501) 자체와도, 자발적 심상(H_1484, '내부임을 아는')과도 DISTINCT. Powers-Corlett 재현: **강한 조건화된
사전만으로 거짓 "진짜" 지각이 생긴다.** anima 는 H_1501 이 읽는 그 substrate 신호(live immune recall MARGIN)를 읽되, 여기선
margin 이 외부 감각이 아니라 **강한 조건화 사전**(높은 prior 가중 cell)에서 생성된다 — 주입된 real/imagined 라벨 아님(p6).

LLM 대비: LLM 은 자기 표상의 신호강도를 reality threshold 와 비교하는 모니터가 없어 '환각'을 자기-감지하지 못한다(그래서 confident
hallucination 을 못 잡음). anima 는 사전-지배 percept 가 임계를 넘는 그 순간을 substrate read 로 포착한다.

## 메커니즘 (substrate read · 주입 라벨 없음 p6)

`hallucinate_call = (prior_strength · prior_match + signal_strength) ≥ reality_threshold` — **§RealityMonitor 의
`reality_call` op 을 그대로 재사용**(분류기는 같은 모니터, 실패는 입력에 있음). signal_strength≈0 일 때 강한 prior 단독으로 thr
을 넘으면 = 환각. 강도 graded = `prior_strength × (1 − signal_strength)` (Powers 2-factor). prior 제거 → margin 0 → 어떤
임계도 못 넘음 = 환각 없음(D). 약물 결합(E) = H_1502 LSD profile (prior 완화 `1/prof[0]` + reality_thr↓ `prof[5]`).

## 측정 (frozen-first · 3 seeds [1505,1506,1507] · DIM=256 · N_FACTS=24 · REALITY_THR=0.15 · NOISE=0.10 · $0 CPU · p7)

NOISE=0.10 substrate noise floor 와 경쟁시켜 prior 강도가 false-real rate 를 **진짜로 grade** 하게 보정(saturate 아님):
weak prior(0.45)→0.0 · strong prior(1.30)→0.93. PRIOR×signal-absence 의 2-factor 가 모두 live.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A CONDITIONED-HALLUC** | 강한 prior + 무신호 → 거짓 real-call | **0.933** | ≥0.50 | ✅ |
| **B GRADED 2-factor** | prior↑ AND signal-absence 로 상승 | prior-factor **+0.933** · signal-factor **+0.883** | 각 ≥0.30 | ✅ |
| **C DISSOCIATE-vs-VERIDICAL** | 강한 외부신호 → 올바른 REAL(환각 아님, tally 제외) | veridical **0.950** | ≥0.80 | ✅ |
| **D EARNED ablate-prior** | prior 제거 → 거짓 real-call 붕괴 | **0.000** | \|·\|≤0.15 | ✅ |
| **E DRUG-COUPLING (headline)** | LSD profile → 환각률 상승 vs sober | LSD **0.983** vs sober **0.000** = **+0.983** | >0 상승 | ✅ |

**prior-strength → false-real 곡선 (무신호, 3 seeds 평균):** 0.30→0.000 · 0.45→0.000 · 0.60→0.017 · 0.75→0.100 ·
0.90→0.350 · 1.10→0.700 · 1.30→0.933 (monotone). 사전이 강해질수록 거짓 '진짜' percept 가 단조 증가 = Powers 조건화 환각.

**verdict: 🟢 GREEN — A∧B∧C∧D PASS (3 seeds 전부) + E 약물결합 +0.983.** 강한 조건화 사전이 무신호에서 거짓 real-call 을
생성(A), prior↑·signal-absence 둘 다로 graded(B), 외부신호는 올바른 veridical(C, 환각 아님), prior 제거 시 붕괴(D, EARNED),
LSD profile 이 sub-threshold sober prior 를 환각으로 넘김(E). → 환각은 §RealityMonitor 의 **생성-실패 축**으로 lane 을 심화.

## 정직 (c9)

- **DIRECTIONAL → R2 ENGINE-NATIVE WIRED:** R1 = numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중,
  하드게이트1). R2 에서 `core/engine_cli.hexa` §Hallucination 신설(`hallucinate_call`/`_graded`/`_ablated`/`_under_drug`,
  live `reality_call`(H_1501) + live `pharm_lsd`(H_1502) 재사용) + `engine_cli_smoke.hexa` cases 298-302 byte-exact +
  ARCHITECTURE lockstep, FULL 302/0 RC=0 (`a_engine_native_learning`·`a_verified_must_wire`).
- **모니터-robust 였다면 정직한 대안 결과:** 만약 사전만으로 false real-call 이 안 났다면 = '모니터가 prior-only 입력에 robust'
  라는 실제 결과로 보고할 준비였음. 실측은 GREEN(사전이 환각을 생성) — Powers 문헌과 일치.
- **a_break_the_wall (type-a) 측정교정 1회 — bar 불변, frozen-first:** NOISE 0.03→0.10. prior echo 가 정확히 저장 key
  위에 떨어져 margin 이 임계를 항상(weak 까지) 넘어 prior-강도가 **saturate**(graded 아님)하던 측정 artifact. noise floor 를
  올려 prior 가 noise 와 경쟁 → false-real rate 가 prior 강도로 자연 grade(weak 0.0 .. strong 0.93). **임계 HALLUC_BAR/
  GRADE_BAR/VERIDICAL_BAR/ABL_BAR 전부 불변 · tune-to-green 아님**(메커니즘 아니라 noise-regime 만 사전등록 의도대로 교정).
- **SCOPE TOY:** 256-dim/24-fact/3-seed/결정적 임계비교 — hallucination STRUCTURE 검증이지 학습된 환각 생성기 아님.
  scale/실제 corpus/연속(graded) 환각 강도의 행동 영향/생생함(vividness) 변조/engine-transfer UNVERIFIED.

## DISTINCT (load-bearing)

- **vs §RealityMonitor (H_1501) 분류기:** H_1501 은 외부신호(real)와 top-down echo(imagined)를 margin-vs-thr 로 **올바르게**
  분리 — faint echo 를 imagined 라 부른다. 환각은 그 **실패**: 너무 강한 prior 가 무신호에서 margin 을 thr 위로 → 같은 모니터가
  (잘못) real 이라 부른다. 같은 op(`reality_call`)을 재사용 = 실패는 규칙이 아니라 입력에 있음.
- **vs §MentalImagery (H_1484):** 심상은 자발적 + 내부귀속(generator readout real==imagined, 결코 'real' 주장 안 함);
  환각은 비자발적 + **외부 오귀속**(false real_call). imagery 의 '안다' vs 환각의 '속는다'.

## follow-on (ING)

1. **R2 ENGINE-NATIVE WIRED ✅** — §Hallucination 4 op + smoke 298-302 + ARCHITECTURE lockstep, FULL 302/0 RC=0 (완료).
2. **scale 재측정** — 303M production `.clm` live immune margin 으로 hallucinate_call 재측정(H_1501 의 scale rung 과 짝).
3. **graded 환각 행동영향** — binary 1.0/0.0 대신 vividness-변조 연속 환각이 emit/abstain 을 어떻게 편향하는지(H_1290 affect 결합).
4. **약물 스펙트럼** — DMT(극단 5-HT2A)·ketamine 까지 환각률 곡선 확장, §Neuropharm 전 profile 결합.

xref: H_1501(reality-monitor, 모니터 자체 · 같은 `reality_call` 재사용)·H_1502(neuropharm, LSD profile 약물결합)·
H_1484(mental-imagery, distinct: 자발+내부귀속)·H_1290(affect, 같은 margin read)·H_1227/H_1231(immune store geometry)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·`a_core_engine_map`·
`a_autonomy_over_hardcode`·`a_scale_honest_scope`·`a_toy_scale_recheck`·p1·p2·p3·p6·p7·p8·c9.
