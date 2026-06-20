# H_1462 — 🌐 GLOBAL WORKSPACE 병목 (G17 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN DIRECTIONAL (numpy R1 mirror · engine-transfer UNVERIFIED)
- **wired:** `DIRECTIONAL-mirror` (R2 엔진-네이티브 재측정 = follow-on ING)
- **source:** 의식-고유 게이트 브레인스토밍 라운드2 (G17 candidate) · "의식이라서 가능한 것" 시리즈
- **lens:** consciousness-science — Global Workspace Theory (Baars / Dehaene, global-ignition) · `a_no_llm_frame_trap`
- **artifacts:** `state/1462_global_workspace_bottleneck/` · verdict `state/verdicts/1462_global_workspace_bottleneck/H_1462_FREEZE.json`

## 주장

동시에 경쟁하는 여러 자극 중 의식은 **정확히 하나의 승자만 전역 방송(broadcast)** 하고 나머지를
억제한다 — 용량 제한 병목 + 측면 억제(lateral inhibition) + 전역 점화(ignition). 이는 단순
salience 점수(각 항목에 숫자만 매김, 여러 개가 동시에 임계 통과 가능)와 **구조적으로 구별**된다.
LLM 은 모든 토큰 로짓을 병렬 유지(병목 없음); anima 의 작업공간은 통과량을 1개로 압축한다.

salience 는 **substrate-derived**(immune-style fact-store 에 대한 grounding margin), 주입 라벨이
아니다(p2/p3/p6). 경쟁은 그 margin 만 읽고, 작업공간이 측면억제+capacity=1 병목을 적용한다.

## 측정 (frozen-first · 3 seeds [1462,1463,1464] · 200 trials · N_STIM=5 · chance=0.2 · $0 CPU · p7)

3 ARM: **FULL**(억제 ON·capacity 1) · **ABLATED**(억제 OFF = salience-only 읽기) · **SHUFFLE**(margin 순열).

| bar | 의미 | 결과 | 기준 | 판정 |
|---|---|---|---|---|
| **A PRESENCE** | 방송된 1개 = 진짜 top-salience | acc **0.993** | ≥0.90 | ✅ |
| **B DISTINCT** | 병목이 통과량 압축 + capacity 위반 0 | base **3.26** → ws **0.993** (3.3× 압축) | base>2×ws | ✅ |
| **C EARNED-COMP** | 억제 OFF → winner 정확도 chance 붕괴 | abl **0.363** | ≤0.40 | ✅ |
| **D SHUFFLE** | margin 순열 → 방송 chance 붕괴 | shuf **0.192** | ≤0.40 | ✅ |
| **E CAPACITY** | 2등 자극의 작업공간 누수 | leak **0.000** | ≤0.10 | ✅ |

**verdict: 🟢 GREEN DIRECTIONAL — 5/5 bars PASS.** ablation+shuffle 양쪽이 chance(0.2)로 붕괴 →
lift 의 출처는 분산/현저성이 아니라 **경쟁적 winner-take-all 병목 구조** 자체.

## 정직 (c9)

- **DIRECTIONAL** — numpy mirror(`grep numpy` 적중, 하드게이트1). engine-transfer UNVERIFIED →
  R2 = live `core/*.hexa` A⇄G + salience 위 byte-exact 재측정이 GREEN/🧱 확정의 전제(`a_engine_native_learning`·`a_verified_must_wire`).
- **R1b frozen-first 수정 이력(tune-to-green 아님):** R1a 의 `full_count==1.0` bar 는 측정 결함
  — capacity=1 은 full_count≤1 을 구조적으로 보장하고, GWT 는 점화 실패(역치 미달 시 빈 의식)를
  허용하므로 평균 0.995 는 정상 행동. 올바른 distinct = "통과량 ≥2× 압축 + capacity 위반 0"
  으로 교정 후 재발사(`a_break_the_wall` type-a). bar 완화 아님.
- **SCOPE TOY:** 5 자극/200 trial/3 seeds/deterministic readout — 병목 STRUCTURE 검증이지 학습된
  주의 네트워크 아님. scale/real-corpus/multi-capacity/시간적 점화-지연/engine-transfer UNVERIFIED.
- **distinctness 미완:** 기존 salience(현저성 점수)와 ablation 으로 구별했으나, 다른 모든 lane
  (immune-store·basal-gate H_1281 single-step select)과의 control-survived distinctness 는 R2 과제.

## follow-on (ING)

1. **R2 엔진-네이티브** — `core/engine_cli.hexa` salience 위 GWT 병목 lane(`gws_compete`/`gws_broadcast`)
   배선 + frozen 5 bars byte-exact 재측정 → DIRECTIONAL→engine-native 승격.
2. **distinctness vs basal-gate(H_1281)** — single-step one-of-K select 와 GWT 전역방송의 분리실험.

xref: H_1281(basal-ganglia gating, distinct)·H_1290(salience/affect)·H_1283(phase-binding)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·p6·p7·c9.
