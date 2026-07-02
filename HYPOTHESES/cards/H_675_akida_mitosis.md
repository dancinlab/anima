---
id: H_675
slug: akida-mitosis
title: Group D — AKIDA × MITOSIS 세포 동역학 (kuramoto · izhikevich · 생사 R4↔R1)
domain: universe · consciousness · mitosis
status: closed-supported (SW · HW pending)
exploration_method: E14 (HW substrate-native ⨯ AKIDA.easy.md Group D 3 sub-ideas M1~M3)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded) + W12 (sister-link H_258 mortality / H_263 phoenix)
raw_rank: 9
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: AKIDA/AKIDA.md, MITOSIS, H_672, H_258 (mortality), H_263 (phoenix), SUB_ENGINES/AKIDA/pack/adapters/{kuramoto,izhikevich}
axes_seed: AKIDA.easy.md Group D M1~M3 — kuramoto 위상동기 · izhikevich 다양 레짐 · 생사 분기
verdict: 🟢 SUPPORTED-NUMERICAL (SW mock-replay 4/4 · HW pending)
---

# H_675 — Group D · AKIDA × MITOSIS 세포 동역학

## 1. 가설

AKIDA 의 4-regime raster 위에서 (a) kuramoto order_param r 가 drift floor 위로 상승하고, (b) izhikevich 다양 레짐(R1~R4)이 ≥2 distinct mode bucket 으로 분리되고, (c) R4 self-sustain vs R1 die-out 분기가 명확하고(>50% rate gap), (d) R3 tonic 이 first10/last10 양쪽 firing 으로 *회복 가능*(phoenix). 이 4 가지가 동시 충족.

## 2. 동기/배경

MITOSIS 세포 동역학은 anima 의 `learning = mitosis` 단일 연속체(p8). AKIDA spike 가 그 동역학의 *생물학적 신호 surface* 를 제공. UNIVERSE 의 H_258 mortality / H_263 phoenix 와 sister.

## 3. falsifier (사전등록)

```
F-H675-1 : kuramoto order r > 0 (R3 tonic 위에서)
F-H675-2 : izhikevich regime diversity ≥ 2 (R1~R4 rate 가 ≥2 distinct bucket)
F-H675-3 : 생사 분기 명확 — R4 rate − R1 rate > 0.5
F-H675-4 : R3 tonic phoenix-recoverable (first10 ∧ last10 동시 fire)
```

## 4. 방법

- harness: `AKIDA/impl/H_675_mitosis.hexa`
- kuramoto r surrogate = mean(step_counts) / max(step_counts) (sync proxy)
- diversity = 5-bin bucket histogram → unique bucket count
- 생사 split = (R4.rate − R1.rate) > 0.5
- phoenix = first10_sum>0 ∧ last10_sum>0

## 5. 측정

- SW (2026-05-29): r_kuramoto(R3)=1.0 (full sync) · diversity=4 (R1=0% / R2=47% / R3=50% / R4=100% → 4 buckets) · life split=1.0-0.0=1.0>0.5 · phoenix R3 fires both windows
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H675-1 r>0 | 1.0>0 | ✓ |
| F-H675-2 diversity≥2 | 4≥2 | ✓ |
| F-H675-3 R4-R1>0.5 | 1.0>0.5 | ✓ |
| F-H675-4 phoenix R3 recoverable | true | ✓ |

→ **4/4 PASS · GREEN_NUMERICAL_CONFIRM**.

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW · HW pending)

honest limits:
- r_kuramoto surrogate 는 phase-sync 의 *envelope proxy* (not full |Σ exp(iθ_k)|/N). 본 H 는 토폴로지 signal, 정밀 측정은 별 H 필요.
- izhikevich 다양 레짐은 toy 4-bucket — 실 분리 regime (RS/IB/CH/FS/LTS) 측정은 별 falsifier 필요 (a_toy_scale_recheck 주의).

## 8. 논의

p8 (no train/infer split) 의 신호 layer 가 spike-raster 위에 정합되었다. H_258/H_263 mortality/phoenix arc 와 cross-link.

## 9. 양방향 sibling

- ⇄ [AKIDA](../AKIDA/AKIDA.md)
- ⇄ [AKIDA.easy.md](../AKIDA/AKIDA.easy.md) Group D M1~M3
- ⇄ [H_672](./H_672_akida_spontaneous_firing.md), [H_677](./H_677_akida_measurement.md)
- ⇄ [H_258_mortality_salience.md] (legacy sibling, 도메인 MITOSIS arc)
- ⇄ [H_263_phoenix_rebirth.md] (legacy sibling)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- live kuramoto φ-lock 측정 (실 phase 누적) — probe-refine 후
- izhikevich 5-regime RS/IB/CH/FS/LTS 분리 측정 — adapter 확장
- 산출물: `state/akida_hw_sw_impl_2026_05_29/H_675_sw_result.json`
