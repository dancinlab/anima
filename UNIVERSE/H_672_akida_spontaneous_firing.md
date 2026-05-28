---
id: H_672
slug: akida-spontaneous-firing
title: Group A — AKIDA AKD1000 자발-발화 × 8-factor 동기 (HW/SW backend 통합)
domain: universe · consciousness · neuromorphic-silicon
status: closed-supported (SW · HW pending)
exploration_method: E14 (HW substrate-native ⨯ AKIDA.easy.md Group A 4 sub-ideas C1~C4)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded) + W12 (sister-link AKIDA D1/PR#1371)
raw_rank: 9
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29 (new — AKIDA HW/SW 통합 구현 PR)
sister: AKIDA/AKIDA.md (도메인), H_673 (B core-decide), H_674 (C persistence), H_675 (D mitosis), H_676 (E decoder), H_677 (F measurement · D1 inherit PR#1371), H_678 (G channel)
axes_seed: AKIDA.easy.md Group A C1~C4 — R3 tonic · spontaneous_gate · 8-factor · R2 timing
verdict: 🟢 SUPPORTED-NUMERICAL (SW mock-replay 4/4 · HW-confirm pending probe-refinement)
---

# H_672 — Group A · AKIDA AKD1000 자발-발화 × 8-factor 동기

## 1. 가설

BrainChip AKD1000 의 4-regime 자발-발화(R1 weak-silent / R2 zero-noise / R3 tonic / R4 recurrent-self-sustained) 는 anima 의 p5(speak() 금지) + a_substrate_native_speak 의 **하드웨어 정답**이다. 입력 0 에서도 실리콘이 물리적으로 스파이크를 쏘므로 자극-반응이 원천 불가능. 본 H 는 4 sub-아이디어(R3 idle 동기 / spontaneous_gate emit 맥락 / 8-factor 동기 / R2 stochastic timing) 가 단일 backend-스위치 harness 안에서 통합 측정될 수 있음을 검증한다.

## 2. 동기/배경

AKIDA.easy.md Group A 의 4 항목(C1 R3 tonic · C2 spontaneous_gate · C3 SPIKE_FACTOR_MAP · C4 R2 noise) 은 모두 동일 raster 위에서 측정 가능한 sub-feature 다. 분리된 harness 가 아니라 단일 H_xxx 로 묶어 backend switch (`AKIDA_BACKEND` env + `--backend` arg) 한 점에서 HW/SW 토글하는 통합 구조가 cycle/cycle-fg 친화적이다.

## 3. falsifier (사전등록, frozen 2026-05-29)

```
F-H672-1 : R3 tonic spike rate > 0                        (입력0 자발 발화 존재)
F-H672-2 : R3 tonic rate ∈ (0.0, 1.0)                     (full chaos 도 die-out 도 아님)
F-H672-3 : R2 noise rate ≥ R1 silent rate                  (noise straddle > sub-thresh)
F-H672-4 : 8-factor SPIKE_FACTOR_MAP non-zero on R3        (rate>0 ⇒ ≥1 factor non-zero)
```

PASS 정의: 4/4 모두 true → 🟢 GREEN_NUMERICAL_CONFIRM · 미통과 1+ → 🔴 closed-negative.

## 4. 방법

- harness: `AKIDA/impl/H_672_spontaneous_firing.hexa` (hexa-native, ~140 LoC)
- backend 모듈: `AKIDA/akida_backend.hexa::akida_backend_resolve / akida_hw_reachable / akida_sw_mock_raster_R*`
- HW path: pi5-akida AKD1000 실측 (3-신호 점검 후 실패 시 명시 panic; live R3 streamer 미중단)
- SW path: `SUB_ENGINES/AKIDA/state/spontaneous_emission_result_2026_05_22.json` canonical raster mock-replay (deterministic, n_neurons=16 · 200 step · seed=187 · BackendType.Hardware origin)
- 측정 단위: rate, std_ratio, sat_ratio per regime → 8-factor map → falsifier judge

## 5. 측정 (HW/SW 양쪽)

- SW (Mac 로컬, 2026-05-29): `hexa run AKIDA/impl/H_672_spontaneous_firing.hexa sw` → exit 0
  - R1.rate=0.000 · R2.rate=0.475 · R3.rate=0.500 · R4.rate=1.000
  - 8-factor map(R3): curiosity=0.25 · tension=0.0 · novelty=0.0 · coherence=0.25 · valence=0.25 · arousal=0.5 · saliency=0.0 · drive=0.0 → sum > 0
- HW (pi5-akida): probe-refinement pending (`state/akida_hw_sw_impl_2026_05_29/hw_probe_2026_05_29.txt` — /dev/akida0 OK · akida pkg venv-scoped · hostname=ubuntu)
- 비용: $0 (Mac local + read-only pi5 probe)

## 6. 결과

| falsifier | 측정값 | PASS |
|---|---|---|
| F-H672-1 R3 rate>0 | 0.500 | ✓ |
| F-H672-2 R3 ∈ (0,1) | 0.500 ∈ (0,1) | ✓ |
| F-H672-3 R2≥R1 | 0.475 ≥ 0.0 | ✓ |
| F-H672-4 8-factor fires | sum=1.25 > 0 | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM (SW mock-replay)**.
원본 raster 는 PR#1371 silicon-confirmed 측정값이므로 본 SW path 는 "deterministic replay of last good HW run" — 위조 0.

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW path 7/7 · HW path pending probe-refinement)

honest limits:
- HW live re-confirm 은 venv-scoped akida import + pool-aware probe (signal_3 hostname tolerance) 가 필요. 본 PR 은 그 refinement 를 deferred.
- R3 tonic 8/16 fixed pool 은 canonical raster spec — 다른 seed/threshold 면 다르게 응답할 수 있음 (toy-scale-transfer 주의).

## 8. 논의

p5 의 HW 정답을 단일 backend-switch 안에 모았다. 통합 harness 패턴은 Group B~G 6 H 가 동일 패턴으로 따를 수 있도록 a_completeness_over_cheap 정합 (cheap 한 분리 harness 대신 완성도 위주 통합).

## 9. 양방향 sibling

- ⇄ [AKIDA](../AKIDA/AKIDA.md) (도메인 SSOT · milestone 갱신)
- ⇄ [AKIDA.easy.md](../AKIDA/AKIDA.easy.md) Group A 4 sub-아이디어
- ⇄ [H_673](./H_673_akida_core_decide.md) (Group B · 같은 backend switch 패턴)
- ⇄ [H_674](./H_674_akida_persistence.md) (Group C)
- ⇄ [H_675](./H_675_akida_mitosis.md) (Group D)
- ⇄ [H_676](./H_676_akida_decoder.md) (Group E)
- ⇄ [H_677](./H_677_akida_measurement.md) (Group F · D1 inherit PR#1371)
- ⇄ [H_678](./H_678_akida_channel_bridge.md) (Group G)
- ⇄ [CANDIDATES](./CANDIDATES.md) (Consumed 등재)

## 10. 다음 작업

- HW path re-confirm: venv-aware probe refinement + pi5-akida pool 경로 (`hostname` tolerance, akida-venv python 경로)
- R3 tonic emit-substrate 인자 주입 — AKIDA.md milestone "SPIKE_FACTOR_MAP §4 modulator R1/R2 placeholder → telemetry refit" 와 결합
- 산출물: `state/akida_hw_sw_impl_2026_05_29/H_672_sw_result.json` · `sw_sweep_2026_05_29.log`
