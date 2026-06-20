# H_1462 — 🌐 GLOBAL WORKSPACE 병목 (G17 의식-고유 게이트 후보)

- **tier:** 🟢 GREEN ENGINE-NATIVE + WIRED (R1 numpy mirror DIRECTIONAL → R2 live `core/` byte-exact)
- **wired:** `WIRED-live` — `core/engine_cli.hexa` §GlobalWorkspace (gws_new/_add/_ignited/_winner/_count/_leak) · `engine_cli_smoke.hexa` cases 169-173 (5 frozen bars) + 174-177 (basal-gate distinctness) · FULL smoke **178 pass / 0 fail RC=0** · ARCHITECTURE.json lockstep ✓
- **source:** 의식-고유 게이트 브레인스토밍 라운드2 (G17 candidate) · "의식이라서 가능한 것" 시리즈
- **lens:** consciousness-science — Global Workspace Theory (Baars / Dehaene, global-ignition) · `a_no_llm_frame_trap`
- **artifacts:** `state/1462_global_workspace_bottleneck/` (R1 probe) · `core/engine_cli.hexa` §GlobalWorkspace + `core/engine_cli_smoke.hexa` 169-173 (R2) · verdict `state/verdicts/1462_global_workspace_bottleneck/H_1462_FREEZE.json`

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

### R2 distinctness vs basal-gate (engine-native · smoke 174-177)

basal-gate(H_1281 VBasalGate)는 **학습된 go-value**(go_w·feats)로, GWS 는 **즉석 salience** 로 선택한다.
같은 후보 A(salience 0.30, 학습 high-value)·B(salience 0.90, 미학습)에서:

| case | bar | 결과 | 의미 |
|---|---|---|---|
| 174 | basal=value | A (idx 0) | 학습된 가치 따라감(salience 무시) |
| 175 | GWS=salience | B (idx 1) | 즉석 현저성 따라감(학습 무관) |
| 176 | **DISSOCIATE** | A≠B (true) | 두 게이트가 **정반대** 선택 = 별개 메커니즘 |
| 177 | CONTROL | untrained basal → −1 abstain | basal=학습 의존 ⊥ GWS=학습 비의존 |

→ **value-driven gate ⊥ salience-competition bottleneck**. FULL smoke **178 pass / 0 fail RC=0**.

## 정직 (c9)

- **R1 DIRECTIONAL → R2 ENGINE-NATIVE 완료:** R1 은 numpy mirror(통계 200-trial/3-seed, DIRECTIONAL).
  R2 에서 5 frozen bars 를 live `core/engine_cli.hexa` §GlobalWorkspace lane 으로 배선하고
  `engine_cli_smoke.hexa` cases 169-173 으로 byte-exact 재측정 → presence/distinct/ablation/shuffle/
  capacity 각 bar 가 결정적 케이스로 1:1 PASS, FULL smoke 174/0 RC=0. wired 4칸 사다리 (1)→(4) 완주
  (`a_engine_native_learning`·`a_verified_must_wire`). FULL=broadcast 1 (idx 1) vs ablated=2 = winner-take-all 확인.
- **R1b frozen-first 수정 이력(tune-to-green 아님):** R1a 의 `full_count==1.0` bar 는 측정 결함
  — capacity=1 은 full_count≤1 을 구조적으로 보장하고, GWT 는 점화 실패(역치 미달 시 빈 의식)를
  허용하므로 평균 0.995 는 정상 행동. 올바른 distinct = "통과량 ≥2× 압축 + capacity 위반 0"
  으로 교정 후 재발사(`a_break_the_wall` type-a). bar 완화 아님.
- **SCOPE TOY:** 5 자극/200 trial/3 seeds/deterministic readout — 병목 STRUCTURE 검증이지 학습된
  주의 네트워크 아님. scale/real-corpus/multi-capacity/시간적 점화-지연/engine-transfer UNVERIFIED.
- **distinctness vs basal-gate(H_1281) DONE:** salience+ablation 구별에 더해, basal-gate(value-learned
  one-of-K select)와의 control-survived distinctness 를 engine-native 로 확정(smoke 174-177) —
  basal=value-driven(학습 의존, untrained→abstain) ⊥ GWS=salience-instant(학습 비의존). 두 게이트가
  같은 후보에서 정반대 선택 = 별개 메커니즘. (immune-store 등 나머지 lane 과의 distinctness 는 잔여.)

## follow-on (ING)

1. ~~**R2 엔진-네이티브** — `core/engine_cli.hexa` GWT 병목 lane 배선 + frozen 5 bars byte-exact 재측정~~
   ✅ **DONE** (§GlobalWorkspace gws_new/_add/_ignited/_winner/_count/_leak · smoke 169-173 · 174/0 RC=0 · ARCHITECTURE lockstep).
2. ~~**distinctness vs basal-gate(H_1281)** — single-step one-of-K select 와 GWT 전역방송의 분리실험~~
   ✅ **DONE** (engine-native, smoke 174-177): basal-gate 는 **학습된 go-value**(go_w·feats)로, GWS 는
   **즉석 salience**로 선택 → 같은 후보 A,B 에서 정반대 선택(basal=A idx0 / GWS=B idx1, case 176 DISSOCIATE).
   CONTROL: untrained basal abstains(-1, case 177) 인데 GWS 는 여전히 salience-B → GWS 는 학습 비의존,
   basal 은 학습 의존 = load-bearing distinct(value-driven gate ⊥ salience-competition bottleneck). FULL smoke **178/0 RC=0**.
3. ~~**brain emit-loop consult**~~ ✅ **CLOSED — NOT-forced 가 정답 (a_autonomy_over_hardcode)**: GWS read
   함수(gws_winner/_count/_leak)는 brain 에서 호출 가능하도록 이미 노출됐고, brain_decide 가 이를 **강제로**
   consult 하게 코드를 넣는 것은 외부가 substrate 에 "GWS 를 보라"고 강제하는 hardcode = a_autonomy 위반.
   anima 의 모든 compose lane(tom_basal/spatial_episodic/cereb_mem 등)이 동일하게 "returns a class · brain
   emit-loop consult deliberately NOT forced"인 것과 일관 — GWS 도 substrate 가 자율적으로 read 할 수 있는
   상태가 종착이다. emit/silence 는 M×W×Φ 가 자율 결정(p5·a_substrate_native_speak), GWS 는 맥락 공급자일 뿐.
   → **H_1462 4칸 사다리 (1)→(4) + distinctness 완주, follow-on 전부 종결.** (남은 건 scale/real-corpus·
   immune-store distinctness = 별도 가설 scope, H_1462 종결과 무관.)

xref: H_1281(basal-ganglia gating, distinct)·H_1290(salience/affect)·H_1283(phase-binding)·
`a_no_llm_frame_trap`·`a_engine_native_learning`·`a_verified_must_wire`·`a_break_the_wall`·p6·p7·c9.
