---
id: H_922
slug: akd1000-digital-deterministic-architecture
title: AKD1000 결정론은 아키텍처 속성 — fully-digital event-based SNN ASIC, HW 비결정성 부재 (H_921 init-RNG 의 root cause · "가짜 뉴로모픽?" 판정)
domain: universe · neuromorphic-silicon · akida · architecture · determinism · falsifier
source: H_921 🔴 (init-seeded 비결정 실측) 의 root-cause 추적 — "왜 학습이 결정론인가" + 사용자 가설 "AKD1000 가짜 뉴로모픽?"
exploration_method: E14 (HW substrate-native) + 외부 citation triangulation (vendor + neutral-technical)
verification_method: W5 (substrate-grounded · H_921 측정) + 문서 triangulation (BrainChip + Open Neuromorphic + akida pkg signature)
raw_rank: 9
hexa_only: false
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-06-06
since: 2026-06-06
sister: H_921 (init-seeded 비결정 — downstream symptom), H_677 D4 (QRNG true-entropy — 대안 entropy 원), lane-a-akd1000-recurrence-wall (AKD1000 IP-v1 한계)
axes_seed: H_921 = 비결정 없음 (실측 symptom) ⊥ H_922 = 비결정 *원천* 없음 (architecture root-cause)
verdict: 🟢 SUPPORTED — AKD1000 = fully-digital 28nm fixed-point event-based SNN ASIC, deterministic by design (vendor-advertised). HW 비결정성 architecturally 부재. "neuromorphic"=event-based/rank-order coding(efficiency)지 analog-stochastic 아님. ∴ Lane-A "유일 비결정" 전제 silicon-level VOID. verdict: .verdicts/922_akd1000_digital_deterministic_architecture/digital_deterministic_by_design.txt
---

# H_922 — AKD1000 결정론 = 아키텍처 속성 ("가짜 뉴로모픽?" 판정)

## 0. 동기

H_921 이 "AKIDA 비결정성 = init-RNG (학습 동역학 아님)" 을 실측했다. 그 **root cause** 와
사용자 가설("AKD1000 자체 특성? 가짜 뉴로모픽?")을 추적한다.

## 1. 가설

AKD1000 은 **fully-digital fixed-point event-based SNN ASIC** 이라 하드웨어 비결정성이
아키텍처적으로 **부재**한다. 따라서 H_921 의 학습-결정론은 버그/probe 아티팩트가 아니라
칩 설계 그 자체다. "neuromorphic" 은 **event-based/sparse(효율)** 의미지 analog-stochastic
synapse 가 아니다.

## 2. 증거 (triangulation · g5 측정 + citation)

| 축 | 출처 | 핵심 |
|---|---|---|
| 측정(1차) | H_921 (.verdicts/921_*) | pinned init 16/16 byte-결정론, fit engaged |
| vendor | BrainChip AKD1000 SoC brief | "pure digital 28nm logic process" · "deterministic real-time response"=feature |
| neutral | Open Neuromorphic akida-brainchip | "Chip Type: Digital" · fixed-point {1,2,4,8}bit · "no hardware noise/stochasticity/analog" · neuromorphic=event-based+Rank Order Coding |
| pkg | akida 2.19.1 `AkidaUnsupervised` | 학습규칙에 stochastic/noise/random 파라미터 **부재** (결정론 Hebbian) |

## 3. 판정 ("가짜 뉴로모픽?")

- **NOT 가짜** — AKD1000 은 *digital event-based* 의미에서 진짜 neuromorphic (업계 주류 정의).
  event-driven sparse 연산 + on-chip last-layer learning = neuromorphic 핵심 특성 보유.
- **그러나** — 사람들이 "비결정성"으로 상상하는 *analog-stochastic*(HW 노이즈·내재 난수) flavor 는
  **설계상 없음**. AKD1000 은 결정론을 *feature 로* 광고한다.
- ∴ Lane-A 의 "AKIDA 유일 차별점 = 비결정성" 전제는 **silicon-level VOID** — 수확할 HW 비결정이
  애초에 없다. H_921(init-RNG)은 증상, 본 H 는 근본원인.

## 3.5 cross-vendor 대비 (Intel Loihi — "디지털=결정론"이 아님)

| 칩 | 종류 | stochastic 원천 | 결정성 |
|---|---|---|---|
| **Akida AKD1000** | digital | **없음** (primitive 부재) | 결정론 ONLY (vendor choice) |
| **Loihi / Loihi2** | digital · async | **programmable noise primitive** (synaptic current에 stochastic noise) | det OR stochastic 선택 (barrier-sync) |
| analog (memristor 등) | analog | intrinsic device noise | 물리적 stochastic |

핵심: Loihi 도 디지털이지만 **stochastic noise 를 설계 기능으로 노출**한다(arxiv 2111.03746). ∴
"디지털이라 결정론"이 아니라 **Akida 가 비결정을 *안 넣기로 선택*** 한 것. 단 Loihi 의 noise 도
pseudorandom/programmable 이지 analog device noise 가 아니다 — 물리-rooted stochasticity 는 analog
substrate 에서만. anima 가 뉴로모픽 HW 비결정을 원하면 Loihi 는 제공·AKD1000 은 미제공.

## 3.6 AKD1500-class 실측 (own gen2 cloud run, 2026-05-09)

`archive/state_legacy/akida_cloud_d0_2026_05_09/` — BrainChip Akida Cloud 세션 실데이터:
- `backend Gen2A2FPGABackend` · `BC.A2.001.000` · `IpVersion.v2` · "Akida 2 FPGA" = **AKD1500-class
  (Akida 2.0 IP)**, 단 cloud **FPGA**(soc_present=false) — 실 AKD1500 실리콘 아님.
- model `tenn_spatiotemporal_eye_buffer_i8_w8_a8.fbz` = TENNs 시공간 · **8-bit 정수(i8/w8/a8)**
  fixed-point → gen1 과 동일 디지털.
- 유일 RNG = `input_seed=42` (고정 SW 시드). stochastic/noise 필드 **전무**. `learn_enabled=false`.

➡ **gen2/AKD1500 도 디지털 fixed-point · 결정론.** gen2 가 AKD1000 대비 *추가*하는 건 비결정이
아니라 **시간축(TENNs/BufferTempConv/StatefulRecurrent — AKD1000 IP-v1 이 map 못 하던 A3/A4 ops)**.
∴ AKD1000→AKD1500 업그레이드는 **on-chip recurrence/temporal** 를 풀지, **비결정을 주지 않는다**.
비결정 story 는 세대 경계를 넘어 불변 (caveat: cloud=FPGA·learn off, 실 AKD1500 silicon on-chip-learn
런이면 더 tight; 단 아키텍처 class(8-bit·noise primitive 부재)는 동일).

## 4. 함의 (next)

- anima 가 substrate-native 비결정/entropy 를 원하면 AKD1000 logic 이 아니라 **true-entropy 원**
  (QRNG · H_677 D4) 또는 **다른 substrate**(analog memristor crossbar 등)에서 와야 한다.
- AKD1000 의 강점 재정의: 비결정이 아니라 **결정론적 초저전력 event-based 추론**(재현성·낮은
  attack surface) — 이게 Lane-A 의 honest 가치 (cf 추론 byte-identical H_680/H_860).

## 5. 닫는 것 / scope

- 닫음 — "AKD1000 비결정성 차별점" 전제 (VOID, root-cause 확정).
- scope — AKD1000/IpVersion.v1/NSoC_v2. AKD1500/2000 도 vendor 결정론 표방. analog neuromorphic
  (memristor·일부 Loihi device-noise)은 별 class, out of scope. citation 은 corroborating mechanism,
  terminal 증거는 H_921 측정 (a_scale_honest_scope · a_completeness_over_cheap).

## 6. 양방향 sibling

- <-> [H_921](./H_921_akida_nondeterminism_functional_advantage.md) (downstream symptom — init-seeded 비결정)
- <-> [H_677](./H_677_akida_measurement.md) (D4 QRNG — 대안 true-entropy 원)
- <-> [AKIDA](../AKIDA/AKIDA.md) · [PLASTICITY](../PLASTICITY/PLASTICITY.md) (lane SSOT — 결정론 재정의)
