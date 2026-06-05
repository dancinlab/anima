---
id: H_925
slug: akd1500-nondeterminism-doc-only
title: AKD1500(gen2 · IP-v2)가 AKD1000 에 부재한 HW 비결정성을 *복원*하는가 — DOC-ONLY 사전등록 falsifier (AKD1500 실리콘 미보유 · 측정 없음 · 아키텍처-grounded PREDICTION)
domain: universe · neuromorphic-silicon · akida · akd1500 · gen2 · determinism · non-determinism · falsifier · doc-only
source: H_922 (AKD1000 결정론=아키텍처, terminal-supported) 의 AXIS-5(gen2/AKD1500-class cloud data) 가 남긴 "실 AKD1500 silicon on-chip-learn 은 미측정" caveat 을 사전등록 가설로 승격
exploration_method: E14 (HW substrate-native) · DOC-ONLY (장비 미보유 · 문서/falsifier 사전등록만 · 디바이스 런 없음)
verification_method: W2 (사전등록 falsifier) — 단 본 H 는 PREDICTION 이지 측정이 아님 · 실 AKD1500 silicon A/B 런 PENDING
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06 (new — gen2 비결정 caveat 사전등록)
sister: H_921 (init-seeded 비결정 source-probe — pinned-init A/B 의 형판), H_922 (AKD1000 결정론 root-cause + AXIS-5 gen2 data), H_923 (AKIDA × QRNG 결합), H_924 (qentropy substrate-agnostic)
axes_seed: AKD1000 비결정 부재 (H_922 닫힘) ⊥ AKD1500 비결정 *복원* 여부 (본 H — 미측정 · PREDICTED closed-negative)
verdict: "PREDICTED (doc-only) — closed-negative-by-architecture; no AKD1500 silicon measurement (PENDING)"
---

# H_925 — AKD1500(gen2/IP-v2)가 비결정성을 복원하는가 (DOC-ONLY 사전등록)

> ⚠ 본 문서는 **PREDICTION** 이다. 측정이 아니다. anima 는 AKD1500 실리콘을
> **보유하지 않으며**, 디바이스 런을 돌리지 않았다. 여기 적힌 결론은 기존 증거
> (H_922 AXIS-5 gen2 cloud data + Loihi 대비)에서 **아키텍처적으로 추론한 예측**이고,
> terminal 판정 token 을 의도적으로 쓰지 않는다 — 실 AKD1500 실리콘 on-chip-learning
> A/B 측정 전까지는 PENDING 이다.

## 0. 동기

H_922 가 "AKD1000 결정론 = 아키텍처 속성" 을 닫으면서(terminal-supported), AXIS-5 에서
own gen2 cloud 데이터를 근거로 **gen2/AKD1500-class 도 디지털 fixed-point 결정론**임을
보였다. 그러나 그 AXIS-5 는 명시적 caveat 을 달았다: cloud 런은 **FPGA 에뮬레이션**이었고
`learn_enabled=false` 라 **on-chip 학습 비결정은 gen2 에서 미측정**이다. 본 H 는 그 빈틈
("AKD1000→AKD1500 세대 업그레이드가 비결정성을 *복원*하는가?")을 사전등록 falsifier 로
승격한다 — 단 장비 미보유로 **DOC-ONLY**.

## 1. §hypothesis (falsifier)

**가설:** AKD1500(gen2 · Akida 2.0 IP · IpVersion.v2)은 AKD1000(IP-v1)에 **부재**한
하드웨어 비결정성을 복원하지 **않는다**. 세대 차이가 추가하는 것은 시간축(TENNs/
recurrence)이지 비결정성이 아니다.

**사전등록 falsifier (측정 가능한 형태):**

> 실 AKD1500 *실리콘* 에서, **pinned non-degenerate init** 하에 on-chip 학습(AkidaUnsupervised
> 또는 gen2 등가 on-chip rule)을 N-episode 반복했을 때,
> **run-to-run weight diversity > 1 또는 output diversity > 1** 이면 → 가설 거짓(FALSIFIED)
> — gen2 가 gen1 과 달리 HW 비결정을 가짐.
> **`weight_div == 1 AND output_div == 1` (byte-결정론)** 이면 → 가설 유지 방향
> — gen2 도 결정론 · AKD1000 과 동일 class.

이 형판은 H_921 의 source-probe(pinned init → init-RNG 가 유일 변이원임을 분리)와
**동일 구조**다. 차이는 substrate 가 AKD1000(측정됨) → AKD1500(미측정)으로 바뀐 것뿐.

## 2. §evidence-base (H_922 AXIS-5 gen2 data + Loihi 대비 · VERBATIM)

### 2.1 own gen2/AKD1500-class cloud run (`archive/state_legacy/akida_cloud_d0_2026_05_09/`)

H_922 AXIS-5 / `.verdicts/922_*/digital_deterministic_by_design.txt` 에서 verbatim:

- backend `"Gen2A2FPGABackend"`, device `"BC.A2.001.000"`, marketing `"Akida 2 FPGA (BrainChip Cloud)"`,
  `ip_version IpVersion.v2`, `generation 2` == **AKD1500-class (Akida 2.0 IP)**, run on a CLOUD FPGA
  (`soc_present=false`, `silicon_equivalent_power=false` → FPGA emulation, **실 AKD1500 실리콘 아님**).
- `learn_enabled=false`, `online_learning=false` (이 세션에서 **on-chip 학습 미실행**).
- model `tenn_spatiotemporal_eye_buffer_i8_w8_a8.fbz` → TENNs spatiotemporal, 8-bit int weights/acts
  (**i8/w8/a8**) = DIGITAL FIXED-POINT, gen1 과 동일.
- ONLY RNG present: `inference.raw.input_seed=42` (fixed SOFTWARE seed). 12개 measure 파일·spike
  trace 어디에도 stochastic/noise 필드 **전무**.
- spike trace = per-step LATENCY only (`out_sum/out_nonzero=null`) → run-to-run output 결정성 캡처
  아님; 비결정 신호 없음, 기대도 없음(digital fixed-point).

➡ H_922 결론(verbatim): "gen2 / AKD1500-class is STILL digital fixed-point, deterministic-by-design.
The ONLY thing gen2 adds over AKD1000 is the TEMPORAL axis (TENNs / BufferTempConv / StatefulRecurrent —
exactly the A3/A4 ops AKD1000 IP-v1 could not map). Upgrading AKD1000 → AKD1500 unlocks on-chip
RECURRENCE/temporal coding, NOT non-determinism."

### 2.2 cross-vendor 대비 (Intel Loihi — "디지털 ≠ 결정론" · verbatim)

H_922 AXIS-4 에서: Loihi/Loihi2 도 **digital · asynchronous** (analog 아님). 그러나 Loihi 는
"the computational primitive of adding **STOCHASTIC NOISE** to the neuron's synaptic current response"
를 **programmable feature 로 노출** (arxiv 2111.03746). Loihi2 는 deterministic mode 도 제공
("complete barrier synchronization … deterministic global timesteps"). → Loihi 는 det OR stochastic
**선택가능**.

| 칩 | 종류 | stochastic 원천 | 결정성 |
|---|---|---|---|
| Akida AKD1000 (IP-v1) | digital | 없음 (primitive 부재) | 결정론 ONLY (vendor choice) |
| Akida AKD1500 (IP-v2) | digital · i8/w8/a8 | **관측된 cloud data 에 없음** (input_seed only) | (예측) 결정론 — PENDING silicon |
| Loihi / Loihi2 | digital · async | programmable noise primitive | det OR stochastic (선택) |
| analog (memristor 등) | analog | intrinsic device noise | 물리적 stochastic |

핵심: Loihi 가 증명하듯 "디지털이라 결정론"은 아니다 — 디지털 칩도 stochastic primitive 를
*넣을 수* 있다. 따라서 AKD1500 결정성 여부는 **8-bit fixed-point class + noise primitive 부재**
라는 *관측된* 아키텍처 속성에서 추론하는 것이지, "디지털이니까"로 자동 단정하지 않는다.

## 3. §prediction (closed-negative-by-architecture · doc-only · unmeasured)

**예측:** AKD1500 은 AKD1000 과 **동일 결정론 class** 다 — 비결정성을 복원하지 않는다.
즉 §1 falsifier 는 실 AKD1500 silicon 에서도 **`weight_div==1, output_div==1` (byte-결정론)**
으로 떨어질 것으로 예측한다. ∴ "AKD1500 이 HW 비결정을 복원" 가설은
**PREDICTED closed-negative-by-architecture** (doc-only · unmeasured).

**근거 사슬:**
1. 관측된 gen2 데이터(§2.1): i8/w8/a8 digital fixed-point, noise/stochastic 필드 전무, 유일 RNG=SW seed.
2. gen2 가 *추가*하는 것은 시간축(TENNs/recurrence — A3/A4 ops)이지 비결정성이 아님(H_922 + lane-a 메모).
3. vendor 가 gen2(AKD1500)도 "deterministic real-time response" 를 **feature 로** 광고(H_922 AXIS-2).
4. noise primitive 를 노출하는 디지털 칩(Loihi)은 존재하나, gen2 Akida 관측 데이터엔 그 primitive 부재.

**honest caveat (핵심):** 관측된 gen2 cloud 런은 **FPGA 에뮬레이션**이었고
**`learn_enabled=false`** 였다. 즉 **on-chip 학습 동역학의 비결정성은 gen2 에서 아직
한 번도 측정된 적이 없다.** 본 예측은 *추론 경로(inference)* 의 fixed-point 결정성 +
아키텍처 class 동일성에서 끌어온 것이고, *학습 경로(on-chip plasticity)* 비결정성에 대한
직접 증거는 gen1(H_921, AKD1000)에만 있다. 따라서 본 H 는 측정이 아니라 **PENDING
AKD1500-silicon probe** 상태의 PREDICTION 이다.

## 4. §what-would-falsify-the-prediction

본 예측을 **틀리게** 만드는 단 하나의 결과:

> 실 AKD1500 *실리콘*(FPGA 에뮬 아님)에서 **pinned non-degenerate init** 하에
> on-chip 학습을 N-episode 돌렸을 때 **run-to-run weight diversity > 1** (또는 output
> diversity > 1) 이 관측되면 → 예측 WRONG. gen2 가 gen1 과 *다르게* HW 비결정을 가지며,
> 비결정 story 가 Akida 세대 경계에서 **불변이 아님**을 의미.

부차 falsifier: gen2 silicon 펌웨어/문서에 AKD1000 엔 없던 **stochastic/noise primitive**
(Loihi 식 synaptic-noise programmable feature)가 노출되면 → 예측의 아키텍처 전제가 깨짐.

이 falsifier 는 **장비(실 AKD1500 silicon) 입수 + pinned-init A/B 런** 으로만 해소된다 —
H_921 의 source-probe 를 gen2 substrate 에 그대로 이식하면 됨.

## 5. §scope

- **DOC-ONLY.** anima 는 AKD1500 실리콘을 **보유하지 않는다**. 디바이스 런 없음. 본 문서는
  falsifier 사전등록 + 아키텍처-grounded 예측일 뿐이다.
- 측정된 것: AKD1000(gen1) on-chip-learn 비결정 부재(H_921 16/16) + gen2 *cloud FPGA inference*
  fixed-point(H_922 AXIS-5). 미측정: gen2 **실리콘 on-chip-learning** run-to-run.
- terminal verdict token 의도적 부재 — 실 측정 전까지 PENDING. 실 AKD1500 A/B 가 들어오면
  본 H 를 측정-backed verdict 로 승격(또는 예측이 틀리면 재작성)한다.
- out of scope: analog neuromorphic(memristor crossbar) · Loihi device-noise 레짐 — 별 class.
- 양자/QRNG 비결정은 substrate(AKD1000/1500 실리콘)이 아니라 *seed 지점* 의 성질(H_924) —
  본 H 의 silicon-비결정 질문과 직교(quantum 언급은 #123-A non-claim: 여기서 양자성을 주장하지 않음).

## 6. 양방향 sibling

- <-> [H_921](./H_921_akida_nondeterminism_functional_advantage.md) (init-seeded source-probe — pinned-init A/B 형판)
- <-> [H_922](./H_922_akd1000_digital_deterministic_architecture.md) (AKD1000 결정론 root-cause + AXIS-5 gen2 data 원천)
- <-> [H_923](./H_923_akida_qrng_coupling.md) (AKIDA × QRNG 결합 — 결정론 칩에 양자 엔트로피 주입)
- <-> [H_924](./H_924_qentropy_substrate_agnostic.md) (qentropy substrate-agnostic — 비결정은 seed 지점 성질)
- <-> [AKIDA](../AKIDA/AKIDA.md) · [PLASTICITY](../PLASTICITY/PLASTICITY.md) (lane SSOT)
