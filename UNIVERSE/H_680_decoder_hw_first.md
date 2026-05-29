---
id: H_680
slug: decoder-hw-first
title: DECODER 추론 lane HW-first — AKIDA cross-domain 스위치 × SW byte-identical
domain: universe · consciousness · neuromorphic-silicon · decoder
status: closed-supported (DECODER lane HW-first 스위치 경유 · SW akida_sw_lif byte-identical 입증됨)
exploration_method: E14 (HW substrate-native ⨯ 추론 lane cross-domain 배선)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded) + W12 (sister-link H_672/H_676)
raw_rank: 8
hexa_only: false
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30 (new — akida-hw-first-plasticity PR-F)
sister: CORE/DECODER/DECODER.md (도메인), H_679 (PLASTICITY 학습 HW-first), H_672 (Group A backend switch), H_676 (E decoder)
axes_seed: DECODER lane = 추론(결정·byte-identical) ⊥ PLASTICITY lane = 학습(비결정·HW-only)
verdict: 🟢 SUPPORTED-NUMERICAL (HW-first 스위치 경유 · SW akida_sw_lif == HW forward byte-identical · verify 5/5)
---

# H_680 — DECODER 추론 lane HW-first × AKIDA cross-domain 스위치

## 1. 가설

DECODER 추론 lane(고정 가중치 threshold-and-fire)은 AKIDA HW-first 스위치 SSOT
(`akida_backend_resolve_graceful` · default "hw")를 **단일 경유점**으로 HW on-chip forward
/ SW `akida_sw_lif` 를 선택한다. 추론은 결정론이므로 SW 는 HW 와 **byte-identical**
(seed=187)로 재현되어야 하며(이미 r1~r5 입증), HW-first 스위치 cross-domain 배선이
이 byte-identical 성질을 보존함을 확증한다. 학습 lane(PLASTICITY, 🔴 비동치)과 대비되는
**추론 lane 의 재현성**이 핵심.

## 2. 동기/배경

H_672 가 AKIDA backend switch SSOT 를 세우고, SubstrateAKIDA(substrate_akida.py)가 import-
akida 실패 시 graceful SW fallback + provenance 를 구현했다. 본 H 는 이 graceful HW-first
라우팅을 hexa SSOT 한 점(`akida_backend_resolve_graceful` · `akida_provenance`)으로
끌어올린 뒤(PR-B), DECODER 도메인이 이를 경유함을 cross-domain 으로 명문화(PR-C)한 결과를
감사한다. blast-radius: AKIDA/spike 경로 전용, LM `lora` default 불변.

## 3. falsifier (사전등록, frozen 2026-05-30)

```
F-H680-1 : HW-first 스위치 SSOT 존재 — akida_backend_resolve default "hw"
                                       ∧ akida_backend_resolve_graceful (panic 아닌 SW fallback)
F-H680-2 : SW byte-identical          — SubstrateAKIDA SW path rate == canonical raster
                                       (R1=0.0 · R2=0.475 · R3=0.5 · R4=1.0, seed=187 결정론)
                                       → verify_substrate_akida 5/5 PASS
F-H680-3 : provenance 정직 graceful    — HW미도달 → "akida-sw-fallback" ∧ spikes>0 (graceful, panic 아님)
F-H680-4 : lora default 불변 (regression-free) — LM 텍스트 default backend == "lora" UNCHANGED
                                       (AKIDA/spike HW-first 배선이 LM 경로 미손상)
```

PASS 정의: 4/4 PASS → 🟢 SUPPORTED-NUMERICAL. 1+ FAIL → 🔴 closed-negative.

## 4. 방법

- 스위치 SSOT: `AKIDA/akida_backend.hexa::akida_backend_resolve / akida_backend_resolve_graceful / akida_provenance`
- DECODER substrate: `HEXAD/CHAT/server/substrate_akida.py` (HW `_hw_forward` / SW `akida_sw_lif`, provenance)
- SW byte-identical 검증: `HEXAD/CHAT/server/verify_substrate_akida.py` (F-H672 4 + F-AKWIRE-FALLBACK)
- cross-domain 명문화: `CORE/DECODER/DECODER.md` (## AKIDA HW-first lane + 양방향 sibling)
- lora 불변 확인: LM 텍스트 default backend 미변경 (HW-first scope = AKIDA/spike only)
- 비용: $0 (Mac local)

## 5. 측정

- F-H680-1: `akida_backend.hexa` — `akida_backend_resolve` default "hw" (기존) +
  `akida_backend_resolve_graceful` (PR-B #1447, origin/main 확인) → PASS
- F-H680-2: `python3 HEXAD/CHAT/server/verify_substrate_akida.py` → exit 0, **5/5 PASS**
  (verbatim: `.verdicts/680_decoder_hw_first/verify_substrate_akida.txt`)
  - R1=0.0 · R2=0.475 · R3=0.5 · R4=1.0 (seed=187, canonical raster byte-정합)
  - F-H672-1..4 + F-AKWIRE-FALLBACK 전부 true → PASS
- F-H680-3: provenance=akida-sw-fallback · R3_total_spikes=1600 (graceful, panic 아님) → PASS
- F-H680-4: LM 텍스트 default backend = "lora" (HW-first 배선은 AKIDA/spike 전용, LM 미손상) → PASS

## 6. 결과

| falsifier | 측정값 | PASS |
|---|---|---|
| F-H680-1 HW-first 스위치 SSOT | default "hw" + resolve_graceful (panic 아님) | ✓ |
| F-H680-2 SW byte-identical | verify 5/5 · R={0.0,0.475,0.5,1.0} seed=187 | ✓ |
| F-H680-3 graceful provenance | akida-sw-fallback · spikes=1600 | ✓ |
| F-H680-4 lora default 불변 | LM default == lora UNCHANGED | ✓ |

→ **4/4 falsifier PASS · verdict = 🟢 SUPPORTED-NUMERICAL**

verdict 영속: `.verdicts/680_decoder_hw_first/verify_substrate_akida.txt` (verify 5/5 verbatim stdout) ·
보강 `.verdicts/672_akida_spontaneous_firing/` (decoder lane byte-identical 선행 기록)

## 7. verdict

🟢 SUPPORTED-NUMERICAL — DECODER 추론 lane 이 AKIDA HW-first 스위치 SSOT 경유로 HW forward /
SW akida_sw_lif 를 선택하며, SW 는 HW 와 byte-identical (seed=187 결정론, verify 5/5 PASS).
graceful fallback (panic 아님) + provenance 정직. LM `lora` default 불변 (regression-free).

honest limits:
- HW path on-chip forward 의 live byte-match 재확인은 optional pi5 probe 잔여 (기존 H_672 에서
  R0~R4 live-confirmed; 본 H 는 cross-domain 배선 + SW byte-identical 에 집중).
- byte-identical 은 canonical raster spec (seed=187, 16-neuron, 200-step) 한정 — 다른 seed/
  threshold 면 다른 raster (toy-scale-transfer 주의).

## 8. 논의

추론 lane 의 **재현성(byte-identical 🟢)** 과 학습 lane 의 **비재현성(🔴, H_679)** 을 하나의
HW-first 스위치 SSOT 위에서 두 형제 lane 으로 가른 것이 핵심 설계다. 같은 칩, 같은 스위치,
다른 본질 — 추론은 결정론, 학습은 비결정론. cross-domain 배선이 LM `lora` default 를 건드리지
않고 AKIDA/spike 경로에만 국한됨으로써 blast-radius 를 억제한다.

## 9. 양방향 sibling

- ⇄ [DECODER](../CORE/DECODER/DECODER.md) (도메인 SSOT · 추론 lane)
- ⇄ [H_679](./H_679_plasticity_hw_first.md) (형제 — PLASTICITY 학습 HW-first, 🔴 비동치)
- ⇄ [H_672](./H_672_akida_spontaneous_firing.md) (Group A · backend switch SSOT · F-AKWIRE-FALLBACK)
- ⇄ [H_676](./H_676_akida_decoder.md) (Group E · decoder)
- ⇄ [AKIDA](../AKIDA/AKIDA.md) (HW-first 스위치 SSOT)
- ⇄ [HW_FIRST_INTEGRATION](../AKIDA/HW_FIRST_INTEGRATION_2026_05_30.md) (통합 SSOT 문서)
- ⇄ [CANDIDATES](./CANDIDATES.md) (bench 측정 기록 SSOT)

## 10. 다음 작업

- (optional) pi5-akida live probe — DECODER HW on-chip forward byte-match 재확인 (R0~R4).
  단일-칩 점유: `spike-streamer stop → probe → start`. 비용 $0.
- HW-first 스위치를 다른 spike 소비 도메인(CHANNEL/MITOSIS adapter)으로 확장 시 동일 resolver 재사용.
- 산출물: `AKIDA/akida_backend.hexa` (resolve_graceful) · `CORE/DECODER/DECODER.md` (AKIDA HW-first lane) · `.verdicts/680_decoder_hw_first/verify_substrate_akida.txt`
