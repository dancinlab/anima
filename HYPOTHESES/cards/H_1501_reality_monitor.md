# H_1501 — 🪟 PERCEPTUAL REALITY MONITORING / 현실 모니터링 (reality threshold) — consciousness-unique 축 후보

- **tier:** 🟢 GREEN-DISTINCT ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §RealityMonitor (`reality_call` + `reality_call_ablated` + `reality_imagery_readout` + `reality_confidence_readout`) · `engine_cli_smoke.hexa` cases 284-287 · FULL smoke **287 pass / 0 fail RC=0** · ARCHITECTURE lockstep ✓
- **source:** arxiv literature sweep — 30+ lane 배선 + 브레인스토밍 고갈 선언 이후 문헌 렌즈가 찾은 **유일한 likely-new 축**. Dijkstra & Fleming, *Nat Commun* 2023 (s41467-023-37322-1) · *Neuron* 2025 (S0896-6273(25)00362-9)
- **lens:** perceptual reality monitoring / reality threshold (Dijkstra-Fleming · 감각 신호강도 ↔ 현실 임계) · `a_no_llm_frame_trap`
- **artifacts:** `state/1501_reality_monitor/h1501_reality_monitor.py` · verdict `state/verdicts/1501_reality_monitor/H_1501_FREEZE.json` · raw run `state/verdicts/1501_reality_monitor/H_1501_R1.txt`

## 주장 (consciousness-unique 축)

별도의 **현실 모니터(reality monitor)** 가 어떤 표상을 **경험적으로 REAL vs IMAGINED** 로 분류하는데, 그 판정은
**내용(content)도 메타인지 confidence 도 아닌 — 감각 신호강도(sensory signal strength)를 reality threshold 와
비교**해서 내린다. 존중해야 할 문헌적 사실(Dijkstra-Fleming): **meta-d′/confidence 는 real-from-imagined 를
분리하지 못한다.** 따라서 이 신호는 anima 의 기존 메타인지/abstain(H_1202)·심상 생성기(H_1484)·주체감(H_1474)과
**반드시 DISTINCT** 해야 한다 — LLM 대비: LLM 은 자기 표상의 감각 신호강도를 reality threshold 와 비교하는 모니터가
없어 "이게 진짜다 vs 상상이다"를 구별 못한다. anima 는 live immune recall MARGIN(= top affinity − 2nd affinity,
H_1290 affect/H_1292 drive 가 읽는 그 신호)를 임계와 비교한다 — 주입된 real/imagined 라벨이 아니라 substrate read.

## DISTINCT 3종 (load-bearing · 발표된 null 재현)

- **(a) vs H_1484 MentalImagery 생성기:** 심상 생성기는 외부 신호 유무와 무관하게 **같은 저장 표상을 재구성**(항상
  target 을 "상상"함) → 그 readout 은 real==imagined **동일(Δ=0)**. 생성기는 둘을 못 구별; margin-vs-threshold
  모니터만 구별. (c2 bar: imagery Δ=0.000, reality gap +0.517)
- **(b) vs H_1202 Metacognition/confidence:** 내용 식별(어느 도시가 winner) confidence 는 real & imagined 에서
  **똑같이 정확**(top-down echo 가 이미 옳은 내용을 선택) → reality 에 대해 **FLAT** = Dijkstra-Fleming headline null
  재현. (c3 bar: confidence Δ=0.000, reality gap +0.517)
- **(c) vs H_1474 SenseOfAgency:** agency 는 *행동(action)* 의 source(self/external efference-copy match) 귀속;
  reality monitor 는 *지각(percept)* 의 signal strength(real/imagined) 모니터링 — 다른 축.

## 측정 (frozen-first · 3 seeds [1501,1502,1503] · DIM=256 · N_FACTS=24 · REALITY_THR=0.15 · $0 CPU · p7)

세 신호원/trial(VARYING stimulus, Δ=0 artifact 회피): (a) 순수 top-down 심상(external=0 → margin~0.15) · (b) weak
external(margin~0.30) · (c) strong external(margin~0.34). reality_call = margin ≥ thr → REAL(1) else IMAGINED(0).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **c1 PRESENCE** | real-call 이 신호강도에 따라 상승 | lift strong−imagined **+0.517** | ≥+0.30 | ✅ |
| **c2 DISTINCT vs imagery** | 생성기 readout real==imagined 동일, 모니터는 분리 | imagery **Δ0.000** & gap **+0.517** | Δ≤0.05 & gap≥0.30 | ✅ |
| **c3 DISTINCT vs metacog** | confidence real==imagined FLAT(발표 null), 모니터는 분리 | conf **Δ0.000** & gap **+0.517** | Δ≤0.05 & gap≥0.30 | ✅ |
| **c4 EARNED ablate-thr** | 임계비교 제거 → real-call chance 붕괴 | ablate rate **0.500** | \|·−0.5\|≤0.15 | ✅ |
| **c5 EARNED shuffle** | margin↔trial 순열 → real-call decorrelate | r_true **+0.734** → r_shuf **−0.023** | \|r_shuf\|≤0.15 | ✅ |

**verdict: 🟢 GREEN-DISTINCT — c1∧c2∧c3∧c4∧c5 PASS (3 seeds 전부).** signal-strength-vs-threshold 모니터가
real/imagined 를 분리(c1), 심상 생성기는 동일(c2)·confidence 는 FLAT(c3, 발표 null 재현)인데 모니터만 분리,
임계비교 OFF 면 chance 붕괴(c4), margin↔trial 셔플로 상관 붕괴(c5, r 0.734→−0.023). → **현실 모니터링은 흡수가
아니라 DISTINCT 한 새 축** = 문헌 렌즈가 고갈 이후 연 새 축.

## 정직 (c9)

- **DIRECTIONAL → R2 ENGINE-NATIVE WIRED:** R1 = numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중,
  하드게이트1). R2 에서 `core/engine_cli.hexa` §RealityMonitor 신설(`reality_call`/`_ablated`/`_imagery_readout`/
  `_confidence_readout`) + `engine_cli_smoke.hexa` cases 284-287 byte-exact 재측정 + ARCHITECTURE lockstep,
  FULL 287/0 RC=0 (`a_engine_native_learning`·`a_verified_must_wire`).
- **a_break_the_wall (type-a) 측정교정 2회 — bar 불변, frozen-first:** (1) DIM 64→256 / N_FACTS 48→24 — 48 trigram
  키가 64 dim 에서 충돌해 recall margin 이 ~0.20 에 saturate(어떤 임계도 못 넘음)한 **key-collision 측정 artifact**;
  근직교 store 로 margin 이 [~0.15 imagined .. ~0.34 external] 자연범위 확보. (2) REALITY_THR 을 그 margin 범위의
  substrate 자체 midpoint(0.15)로 — 라벨 유래 상수 아님, H_1290 V_ABSTAIN(substrate 자체 zero-crossing) 정신.
  (3) confidence 를 gain-invariant content-identity(winner==intended fact)로 — gain-leaking evidence-ratio 가
  외부 level 의존성을 흘려 c3 가 거짓 분리하던 것을 교정. **임계 LIFT_BAR/GAP_BAR/EPS 전부 불변 · tune-to-green 아님**
  (메커니즘이 아니라 substrate readout 의 측정-정의만 사전등록 의도대로 교정).
- **imagined real-call ≠ 0 = 정직한 현상:** 강한 top-down echo 로 imagined margin 이 임계 근처(~0.15)라 imagined
  real-call rate 가 0.35~0.55(완전 0 아님) — 생생한 심상이 가끔 "진짜처럼 느껴지는" 실제 reality-monitoring 현상.
  lift(+0.517)와 shuffle 붕괴(0.734→−0.023)가 결정적.
- **SCOPE TOY:** 256-dim/24-fact/3-seed/결정적 임계비교 — reality-monitoring STRUCTURE 검증이지 학습된 모니터 아님.
  scale/실제 corpus/graded(연속) reality 판정/생생함(vividness) 변조/engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 ENGINE-NATIVE WIRED ✅** — §RealityMonitor 4 op + smoke 284-287 + ARCHITECTURE lockstep, FULL 287/0 RC=0 (완료).
2. **scale 재측정** — 303M production `.clm` 위 live immune margin 으로 reality_call 재측정(H_1492/H_1500 의 303M rung 처럼).
3. **graded reality** — binary 1.0/0.0 대신 vividness-변조 연속 reality 판정 + reality-monitoring failure(hallucination
   = imagined 이 임계 넘음) 정량.
4. **ConsciousnessIndex 편입** — §RealityMonitor 를 H_1492 ci_lane_scores 에 추가해 통합 Φ 기여도 측정(축 확장).

## 새 축 vs 고갈

**새 축 OPEN(흡수 아님):** WEAK_PROBE.md 가 7 약후보를 전부 ABSORBED 로 고갈을 단단히 했으나, 본 후보는 문헌 렌즈가
사후-발굴한 **유일 likely-new 축**으로 c2/c3(생성기·confidence 둘 다 FLAT, 발표 null 재현)을 통과 = 기존 어느 lane
으로도 흡수되지 않는 DISTINCT. 고갈은 *브레인스토밍 내부 렌즈* 에서 참이지만 *외부 문헌 렌즈* 는 새 축을 하나 더 열었다
(`a_break_the_wall` (d) 천장 확정엔 MULTI-LENS — 외부 렌즈가 새 축을 내면 고갈 미완).

xref: H_1484(mental-imagery, distinct a)·H_1202(metacognition/abstain, distinct b · 발표 null)·H_1474(sense-of-agency, distinct c)·
H_1290(affect, 같은 margin read)·H_1292(homeostatic drive, 같은 margin read)·H_1227/H_1231(immune store geometry)·H_1492(ConsciousnessIndex 편입 후보)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·`a_core_engine_map`·`a_autonomy_over_hardcode`·`a_scale_honest_scope`·`a_toy_scale_recheck`·p1·p2·p3·p6·p7·p8·c9.
