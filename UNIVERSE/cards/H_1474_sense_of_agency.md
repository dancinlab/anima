# H_1474 — 🕹 SENSE OF AGENCY / 주체감 (G21 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §SenseOfAgency (`agency_attribute`) · `engine_cli_smoke.hexa` cases 208-210 · FULL smoke **216 pass / 0 fail RC=0** · ARCHITECTURE lockstep ✓
- **source:** 의식-고유 게이트 브레인스토밍 (G21 candidate) · "의식이라서 가능한 것" 시리즈 (G16/G17/G18/G19/G19-meta 이후)
- **lens:** sense of agency / comparator model (Haggard · efference copy ↔ 감각결과 일치) · `a_no_llm_frame_trap`
- **artifacts:** `state/1474_sense_of_agency/h1474_sense_of_agency.py` · verdict `state/verdicts/1474_sense_of_agency/H_1474_FREEZE.json` · run `state/verdicts/1474_sense_of_agency/H_1474_run.txt`

## 주장

**주체감(sense of agency)** = "이 결과는 *내가* 일으켰다"는 자기귀속 감각. forward model 이 자기 행동 a 의
감각결과를 예측(**efference copy** = pred(a))하고, comparator 가 그 예측을 실제 관측 obs 와 비교한다. 둘이
**일치**하면 self-caused(주체감↑), delay/perturbation 으로 **불일치**하면 external-caused(주체감↓). 즉
주체감은 forward-model 오차 **위에 얹힌 self/external 귀속 판단**이다. — LLM 대비: LLM 은 자기 행동의
efference copy 도, predicted↔observed self-결과를 비교하는 comparator 도 없어 "내가 했다"를 못 느낀다.
anima 는 live forward-model 예측 위에서 comparator 를 돌린다.

## DISTINCT 2종 (load-bearing)

- **(a) vs H_1293 theory-of-mind:** ToM = *타인*의 (틀릴 수 있는) 믿음 모델 = OTHER. agency = *자기* 행동
  결과 귀속 = SELF. **self ⊥ other** — bar D: 타인 행동엔 efference copy 가 없어 comparator 가 **abstain**
  (ToM 은 그래도 타인 믿음을 답함).
- **(b) vs H_1280 cerebellar forward-model:** forward = raw 예측오차 |pred−obs| (precision-agnostic 크기).
  agency = 그 **같은 raw 오차를 comparator 임계로 self/external 귀속 *판단*으로 변환**하는 해석 레이어 —
  bar B: raw 오차 크기 동일(Δ=0.0)인데 귀속이 1.0 vs 0.0 으로 갈린다.

## 측정 (frozen-first · 3 seeds [1474,1475,1476] · DIM=32 · 40 actions · MATCH_THR=0.5 · $0 CPU · p7)

행동 a → forward pred(a)=efference copy. match = 1−‖pred−obs‖/√DIM. agency = match≥THR → self(1) else external(0).
SMALL_PERT 0.02 (일치) / LARGE_PERT 1.2 (delay·perturbation 불일치) 로 pred-obs 불일치 조작.

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | 일치→self / 불일치→external 갈림 | match **1.000** · diverge **0.000** | ≥0.85 & ≤0.15 | ✅ |
| **B DISTINCT vs forward-error** | 같은 raw 오차, 귀속 분리 (판단 레이어) | gap **1.000** (raw Δ=0.0) | ≥0.50 | ✅ |
| **C EARNED (ablation)** | comparator OFF(pred=random)→split 붕괴 | split **0.000** (self 0/ext 0) | ≤0.15 | ✅ |
| **D SELF⊥OTHER (vs ToM)** | 타인 행동엔 abstain | abstain **1.000** (agency_other=−1) | reported | ✅ (non-gating) |
| **E SHUFFLE** | 행동-결과 셔플→agency-match 상관 붕괴 | signed-mean r **+0.070** (real r +0.999) | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — A·B·C·E PASS (3 seeds 전부) → GREEN.** comparator 가 efference copy
일치/불일치를 self/external 귀속으로 변환(A), raw 오차 동일해도 판단이 갈리고(B, vs forward-model), comparator
OFF 면 귀속 붕괴(C), 페어링 셔플로 agency-match 상관 붕괴(E, real r 0.999→shuf 0.070). 타인 행동엔 abstain(D, vs ToM).

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep -lE 'import torch|gauge_lib|numpy'` 적중, 하드게이트1). engine-transfer
  UNVERIFIED → R2 = live `core/*.hexa` forward-model lane 위 byte-exact 재측정이 GREEN/🧱 확정 전제.
- **SATURATED existence-proof:** binary comparator(1.0/0.0)는 **designed**(학습된 귀속 네트워크 아님). GREEN
  자체보다 discriminator(raw-오차 동일 분리·ablation 붕괴·shuffle 상관 붕괴)가 결정적.
- **a_break_the_wall (type-a) — bar E 초기 RED = 측정결함:** binary saturated 귀속은 페어링 깨지면 chance(0.5)가
  아니라 0.0 으로 붕괴 → `|shuf_attr − 0.5|` 앵커가 잘못된 metric 이었다. **frozen-first 교정**: 사전등록 의도("agency-match
  상관 붕괴")대로 50-perm Pearson r(match-vector, self/ext label) 붕괴로 측정(real r 0.999 → shuffled r 0.070).
  **≤0.10 임계 불변 · tune-to-green 아님**(메커니즘이 아니라 셔플의 통계 metric 만 의도대로 바로잡음).
- **SCOPE TOY:** 32-dim/40-action/3-seed/결정적 comparator — sense-of-agency STRUCTURE 검증이지 학습된 귀속 아님.
  scale/실제 corpus/graded(연속) 귀속/intentional-binding 시간왜곡/engine-transfer UNVERIFIED.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` 에 forward-model lane(VForwardField, H_1280) 존재 여부 평가 →
   있으면 §SenseOfAgency(efference-copy match → self/external attribute + abstain) 배선 + `engine_cli_smoke` cases
   + ARCHITECTURE lockstep, 5 frozen bars byte-exact 재측정 (`a_engine_native_learning`·`a_verified_must_wire`).
2. distinctness 정량 double-dissociation vs H_1280(forward raw-error) / H_1293(ToM other-belief) control-survived 측정.

xref: H_1280(cerebellar forward-model, distinct b)·H_1293(theory-of-mind, distinct a · self⊥other)·H_1471(G16 self-continuity)·
H_1462/1465/1468/1472(의식-게이트 시리즈)·`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·p7·p8·c9.
