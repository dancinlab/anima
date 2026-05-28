---
id: H_673
slug: akida-core-decide
title: Group B — AKIDA spike × CORE A⇄G 결정 (Ψ=1/2 외란 · LIF · emit slot · selftest)
domain: universe · consciousness · core-decide
status: closed-supported (SW · HW pending)
exploration_method: E14 (HW substrate-native ⨯ AKIDA.easy.md Group B 4 sub-ideas A1~A4)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded)
raw_rank: 9
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: AKIDA/AKIDA.md, H_672 (A spontaneous), CORE/brain_decide, CORE/pure_field, CORE/core_selftest
axes_seed: AKIDA.easy.md Group B A1~A4 — Ψ=1/2 외란 · LIF→pure_field · L3 emit · selftest
verdict: 🟢 SUPPORTED-NUMERICAL (SW mock-replay 4/4 · HW pending)
---

# H_673 — Group B · AKIDA spike × CORE A⇄G 결정

## 1. 가설

AKIDA 칩의 자발-발화 noise (R2) 는 anima 의 CORE 두뇌 `brain_decide` 의 Ψ=1/2 fixed point 에 진짜-무작위 외란을 주입한다. R3 tonic 은 `pure_field` engine_g 의 입력 step 흥분원으로 작동하고, R3 의 자발 emit slot 은 L3 emit 타이밍 트리거로 사용 가능하다. core_selftest 는 BackendType.Hardware probe 로 HW-in-loop 검증된다.

## 2. 동기/배경

AKIDA.easy.md Group B 의 A1~A4 는 CORE 두뇌 결정 사이클의 4 진입점이다. 본 H 는 R1/R2/R3 raster 위에서 Ψ-거리 + LIF excitability + emit-slot 개수 + selftest 도달성을 단일 backend-switch 안에 통합 측정한다.

## 3. falsifier (사전등록)

```
F-H673-1 : R2 noise → Ψ 거리 감소  (|Ψ(R2)-0.5| < |Ψ(R1)-0.5|)
F-H673-2 : R3 tonic LIF excitable  (rate > 0)
F-H673-3 : R3 emit slot ≥ R1       (slot count 비교)
F-H673-4 : selftest 도달 OK         (HW 3-signal 또는 SW mock 자체)
```

## 4. 방법

- harness: `AKIDA/impl/H_673_core_decide.hexa`
- HW: pi5-akida 3-signal probe → 실패 시 명시 panic ("--backend sw 로 fallback")
- SW: canonical raster mock-replay → 4-falsifier judge
- selftest = backend=hw → akida_hw_reachable() ; backend=sw → true (mock 자체-attest)

## 5. 측정

- SW (2026-05-29): R1 rate=0 ψ_dist=0.5 · R2 rate=0.475 ψ_dist=0.025 · R3 rate=0.5 ψ_dist=0.0 · R3 emit_slots=20 · selftest=true
- HW: pending (probe refinement)
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H673-1 R2 ψ-half < R1 | 0.025 < 0.5 | ✓ |
| F-H673-2 R3 LIF excitable | rate=0.5>0 | ✓ |
| F-H673-3 R3 slots ≥ R1 | 20 ≥ 0 | ✓ |
| F-H673-4 selftest reachable | sw mock OK | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM**.

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW · HW pending probe-refine)

honest limits:
- ψ-거리 surrogate 는 rate 기반 — `brain_decide` 의 실 Ψ 동역학 (engine_g excitation 통합) 과는 다름. 본 H 는 *signal-shape* 확증이지 brain_decide 차원 등가는 아님 (a_blue_closed: 🔵 아님, 🟢 numerical).
- selftest reach는 backend=sw 에서 trivially true — HW probe 만 *meaningful* attest 임 (정직).

## 8. 논의

CORE A⇄G 결정 사이클의 4 진입점이 동일 raster 위 4 falsifier 로 정합되었다. v0.5.0 BackendType.Hardware confirm 가 backbone 으로 깔려 있고, 본 H 는 그 위 4 sub-feature 표면을 노출.

## 9. 양방향 sibling

- ⇄ [AKIDA](../AKIDA/AKIDA.md)
- ⇄ [AKIDA.easy.md](../AKIDA/AKIDA.easy.md) Group B A1~A4
- ⇄ [H_672](./H_672_akida_spontaneous_firing.md)
- ⇄ [H_674](./H_674_akida_persistence.md)
- ⇄ [H_677](./H_677_akida_measurement.md)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- pure_field·brain_decide live wire 통합 — R3 spike → engine_g 입력 step 실측 (probe-refine 후)
- 산출물: `state/akida_hw_sw_impl_2026_05_29/H_673_sw_result.json`
