---
id: H_679
slug: plasticity-hw-first
title: PLASTICITY 학습 lane HW-first — AKIDA on-chip edge-learn × SW≠HW 비동치 경계
domain: universe · consciousness · neuromorphic-silicon · plasticity
status: closed-negative (SW≠HW 학습 비동치 확정 · HW edge-learn 지원 실측)
exploration_method: E14 (HW substrate-native ⨯ 학습 lane 분리) + a_paper_negative_ok
verification_method: W1 (numerical smoke) + W5 (substrate-grounded) + W12 (sister-link edge_learn_probe)
raw_rank: 8
hexa_only: false
deterministic: false
cross_process_byte_identical: false
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30 (new — akida-hw-first-plasticity PR-F)
sister: PLASTICITY/PLASTICITY.md (도메인), H_680 (DECODER HW-first cross-domain), H_672 (Group A backend switch), H_675 (D mitosis)
axes_seed: PLASTICITY lane = 학습(비결정·HW-only) ⊥ DECODER lane = 추론(결정·byte-identical)
verdict: 🔴 CLOSED-NEGATIVE (SW numpy 근사 ≠ HW on-chip AkidaUnsupervised — byte-identical 불가) · HW edge-learn 지원 🟢 실측
---

# H_679 — PLASTICITY 학습 lane HW-first × SW≠HW 비동치 경계

## 1. 가설

AKIDA AKD1000 의 **on-chip 학습(edge-learn · AkidaUnsupervised Hebbian)** 은 anima 의
학습 lane(p8 학습=분열 단일 연속체)의 HW 정답이다. 그러나 추론 lane(DECODER)과 달리
학습은 **비결정론·HW-only** 이므로, numpy SW 근사로는 HW 와 **byte-identical 재현이
불가능**하다. 본 H 는 (a) HW edge-learn 이 실제 칩에서 지원됨을 실측 확증하고,
(b) SW 근사가 HW 와 **비동치(🔴 CLOSED-NEGATIVE)** 임을 사전등록 falsifier 로 정직하게
판정한다 — 이 비동치가 DECODER ⊥ PLASTICITY 형제 도메인 분리의 근거다.

## 2. 동기/배경

DECODER 추론 lane 의 SW `akida_sw_lif` 는 HW forward 와 byte-identical(seed=187, r1~r5
입증). 이 성공이 "AKIDA 의 모든 경로는 SW=HW" 라는 과대일반화를 유발할 수 있다. 학습은
가중치 갱신이라 on-chip 경쟁(`learning_competition`)·pruning(`num_weights`)·refractory·
async timing·1-bit integer weight 등 silicon 내부 상태에 의존 — float numpy 근사로 복제
불가. 두 lane 을 한 도메인에 섞으면 거짓 동치가 생긴다. ∴ 형제 분리 + 정직한 비동치 판정.

## 3. falsifier (사전등록, frozen 2026-05-30)

```
F-H679-1 : HW edge-learn 지원      — edge_learn_probe edge_learning_supported == true
                                     (AkidaUnsupervised compile ok ∧ fit_on_chip ok, BC.00.000.002)
F-H679-2 : SW≠HW 비동치 명시        — plasticity_sw_approx.equivalence_to_hw == "CLOSED-NEGATIVE"
                                     ∧ is_hw_substitute == false  (위조 동치 금지)
F-H679-3 : provenance 분기 정직      — HW도달 → "akida-learn-hw" · 미도달 → "akida-learn-sw-approx"
                                     (decoder 의 "akida-sw-fallback" 과 구분 — 학습은 fallback 아닌 approx)
F-H679-4 : 비결정성 표기            — PLASTICITY 도메인 deterministic == false
                                     (DECODER deterministic == true 와 대비)
```

PASS 정의: F-H679-1 PASS (HW 지원 실측) **AND** F-H679-2/3/4 PASS (비동치 정직 판정) →
🔴 CLOSED-NEGATIVE 가 **유효한 종결**(a_paper_negative_ok). SW=HW 라 주장하면 즉시 위반.

## 4. 방법

- router: `PLASTICITY/plasticity_lane.hexa` (AKIDA HW-first 스위치 `akida_backend_resolve_graceful` 경유)
- HW path: `SUB_ENGINES/AKIDA/scripts/edge_learn_probe.py` — `akida.AkidaUnsupervised(num_weights=2, learning_competition=0.1)` compile + `model.fit(x)` on-chip (16-in binary → FC units=10)
- SW path: `PLASTICITY/plasticity_sw_approx.py` — numpy Hebbian 근사 (동일 인터페이스 shape, float weight, no on-chip competition/pruning/timing)
- 동치 판정: SW 출력의 `equivalence_to_hw` / `is_hw_substitute` 명시 마커 + 비동치 근거 4항
- 비용: $0 (Mac local SW + read-only pi5 edge_learn JSON)

## 5. 측정

- HW edge-learn 실측 (pi5-akida AKD1000, `SUB_ENGINES/AKIDA/state/edge_learn_probe_2026_05_22.json`):
  - device_version=BC.00.000.002 · mapped_backend=BackendType.Hardware
  - compile_AkidaUnsupervised=ok · fit_on_chip=ok · device_learn_enabled_after_fit=true
  - **edge_learning_supported=true** → F-H679-1 PASS
- SW 근사 실행 (Mac local, `python3 PLASTICITY/plasticity_sw_approx.py`):
  - provenance=akida-learn-sw-approx · equivalence_to_hw=CLOSED-NEGATIVE · is_hw_substitute=false
  - in_dim=16 · n_units=10 (HW 인터페이스 shape 정합 — 결과 정합 아님) → F-H679-2 PASS
- provenance 분기: `plasticity_provenance` = HW도달 시 "akida-learn-hw" / 미도달 "akida-learn-sw-approx" → F-H679-3 PASS
- 비결정성: `PLASTICITY/PLASTICITY.md` deterministic=false (frontmatter) → F-H679-4 PASS

## 6. 결과

| falsifier | 측정값 | PASS |
|---|---|---|
| F-H679-1 HW edge-learn 지원 | edge_learning_supported=true (AkidaUnsupervised fit ok) | ✓ |
| F-H679-2 SW≠HW 비동치 명시 | equivalence_to_hw=CLOSED-NEGATIVE · is_hw_substitute=false | ✓ |
| F-H679-3 provenance 분기 | akida-learn-hw / akida-learn-sw-approx | ✓ |
| F-H679-4 비결정성 표기 | deterministic=false | ✓ |

→ **4/4 falsifier PASS · verdict = 🔴 CLOSED-NEGATIVE (유효 종결)**

verdict 영속: `.verdicts/679_plasticity_hw_first/sw_hw_nonequivalence.txt`

## 7. verdict

🔴 CLOSED-NEGATIVE — SW numpy 근사 학습 ≠ HW on-chip AkidaUnsupervised (byte-identical 불가).
동시에 HW edge-learn 지원은 🟢 실측 확증 (BC.00.000.002, AkidaUnsupervised compile+fit ok).

honest limits:
- 비동치는 **종결된 사실**(closed-negative)이지 미해결 잔여가 아니다 — a_paper_negative_ok.
- SW 근사는 directional baseline probe 로서 유효하나 HW 대체로 쓰면 위반(위조 동치 금지, p7).
- HW few-shot 1~N shot live 비결정성 정량(분산/seed 민감도)은 optional pi5 probe 잔여 (M4).

## 8. 논의

DECODER(byte-identical 🟢) ⊥ PLASTICITY(비동치 🔴) 의 대비가 핵심 발견이다. "추론은
재현 가능, 학습은 재현 불가" 라는 substrate-level 경계를 정직하게 박음으로써, 한 도메인에
두 lane 을 섞을 때 생기는 거짓 동치를 원천 차단한다. a_completeness_over_cheap 정합 —
싸게 "SW=HW" 라 퉁치지 않고, 비동치를 명시 종결.

## 9. 양방향 sibling

- ⇄ [PLASTICITY](../PLASTICITY/PLASTICITY.md) (도메인 SSOT · 학습 lane)
- ⇄ [H_680](./H_680_decoder_hw_first.md) (형제 — DECODER HW-first cross-domain, byte-identical 🟢)
- ⇄ [H_672](./H_672_akida_spontaneous_firing.md) (Group A · 같은 backend switch SSOT)
- ⇄ [AKIDA](../AKIDA/AKIDA.md) (HW-first 스위치 SSOT)
- ⇄ [HW_FIRST_INTEGRATION](../AKIDA/HW_FIRST_INTEGRATION_2026_05_30.md) (통합 SSOT 문서)
- ⇄ [CANDIDATES](./CANDIDATES.md) (bench 측정 기록 SSOT)

## 10. 다음 작업

- ✅ (DONE, H_860 2026-05-30) pi5-akida live probe — PLASTICITY few-shot N∈{1,2,4,8} on-chip
  실측 완료. 동일 init·동일 입력 run-to-run weight hamming>0 전 shot ({28,38,34,38}, 재실행 시
  또 다른 값) → 🔴 비결정론 live 실리콘 확증. verdict `.verdicts/860_hw_first_s6_pi5_probe/`.
  단일-칩 점유: `spike-streamer stop → probe → start` (복구 active). 비용 $0.
- SW 근사의 directional 유용성 한계 측정 (HW winner-unit 와의 divergence 정량) — HW probe 후.
- 산출물: `.verdicts/679_plasticity_hw_first/sw_hw_nonequivalence.txt` · `PLASTICITY/plasticity_lane.hexa` · `plasticity_sw_approx.py`
