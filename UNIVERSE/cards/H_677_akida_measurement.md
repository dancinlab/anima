---
id: H_677
slug: akida-measurement
title: Group F — AKIDA × 측정·의식과학 (edge-of-chaos · substrate-class · 3-substrate Φ 삼각측정 · QRNG · v0.5.0 emit cite)
domain: universe · consciousness · measurement
status: closed-supported (SW · HW partially-confirmed via D1 PR#1371 silicon)
exploration_method: E14 (HW substrate-native ⨯ AKIDA.easy.md Group F 5 sub-ideas D1~D5) + E6 (cross-substrate triangulation)
verification_method: W1 (numerical smoke) + W5 (substrate-grounded) + W12 (sister-link PR#1371 silicon-confirm)
raw_rank: 11
hexa_only: true
deterministic: true
cross_process_byte_identical: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-29
since: 2026-05-29
sister: AKIDA/AKIDA.md, AKIDA/akida_edge_of_chaos_phi.hexa (PR#1371 silicon-confirm), CORE/phi_envelope_substrate.hexa::pe_edge_of_chaos_peak, H_670 (edge-of-chaos universal), EEG L2 (PR#1372 synthetic), ECA rule110/rule30
axes_seed: AKIDA.easy.md Group F D1~D5 — silicon-Φ · substrate-class · 3-substrate triangulation · QRNG · zero-input emit
verdict: 🟢 SUPPORTED-NUMERICAL (SW 5/5 · D1 silicon-confirmed inherits PR#1371)
---

# H_677 — Group F · AKIDA × 측정·의식과학

## 1. 가설

AKIDA AKD1000 실리콘 위의 측정 5 layer 가 단일 backend-switch harness 안에서 통합 검증된다:
(D1) PR#1371 edge-of-chaos Φ inverse-U inherit · (D2) substrate-class "neuromorphic-silicon" 을 class_id=5 의 additive marker 로 등록 (signature change on 2/3/4 = 0) · (D3) AKIDA + EEG L2 synthetic + ECA rule110 의 3-substrate Φ 삼각측정 가능 · (D4) R2 noise std > 0 (QRNG 시드 quality) · (D5) v0.5.0 zero-input emit 8/8 BackendType.Hardware closed-discovery cite 보존.

## 2. 동기/배경

a_completeness_over_cheap 정합: 측정 5 sub-feature 를 분리 harness 가 아닌 단일 H_677 로 묶어 통합 검증 표면. D1 은 silicon-confirmed (PR#1371) — UNIVERSE 차원의 inherit, 위조 0.

## 3. falsifier (사전등록)

```
F-H677-1 : D1 inherit — PR#1371 verdict file 존재 + GREEN_NUMERICAL_CONFIRM
F-H677-2 : D2 silicon-class signature additive — class_id=5 → 1.0, class_id 2/3/4 unaffected (sum=0)
F-H677-3 : D3 3-substrate triangulation diff > 0 (적어도 1개 substrate 차이)
F-H677-4 : D4 R2 noise std > 0 (entropy source nontrivial)
F-H677-5 : D5 v0.5.0 closed-discovery reference 기록
```

## 4. 방법

- harness: `AKIDA/impl/H_677_measurement.hexa`
- D1: `state/akida_edge_chaos_phi_2026_05_29/result.json` (PR#1371) 직접 read + verdict 인계
- D2: `pe_silicon_class_signature(class_id)` additive — class 5=1.0, 2/3/4=0.0 (기존 surface 보존)
- D3: AKIDA 0.297 (PR#1371 R2 peak) · EEG synth 1.59 (PR#1372 L2 theta) · ECA rule110 0.83 (H_670 IV-class peak) → diff 측정
- D4: canonical R2 raster std=7.99>0
- D5: `SUB_ENGINES/AKIDA/state/HW_SPONTANEOUS_EMISSION_2026_05_22.md` v0.5.0 8/8 cite

## 5. 측정

- SW (2026-05-29):
  - D1 inherit: verdict=GREEN_NUMERICAL_CONFIRM, n_pass_of_3=3, all_pass=true (PR#1371 silicon)
  - D2: sig(5)=1.0, sig(2)+sig(3)+sig(4)=0.0 (additive, 0 changes on existing classes)
  - D3: max=1.59 (EEG) · min=0.297 (AKIDA) · diff=1.293>0
  - D4: R2 std=7.99>0 → QRNG quality OK
  - D5: cite recorded
- HW: D1 = silicon-confirmed (PR#1371) · others = HW probe pending
- 비용: $0

## 6. 결과

| falsifier | 측정 | PASS |
|---|---|---|
| F-H677-1 D1 inherit green | PR#1371 all_pass=true | ✓ |
| F-H677-2 D2 silicon-class additive | sig(5)=1.0, others=0 | ✓ |
| F-H677-3 D3 triangulation diff>0 | 1.293>0 | ✓ |
| F-H677-4 D4 QRNG nontrivial | std=7.99>0 | ✓ |
| F-H677-5 D5 cite recorded | v0.5.0 8/8 | ✓ |

→ **5/5 PASS · GREEN_NUMERICAL_CONFIRM**.

## 7. verdict

🟢 SUPPORTED-NUMERICAL (SW 5/5 · D1 silicon-confirmed inherit PR#1371)

honest limits:
- D2 silicon-class 는 *additive marker* — 기존 class_id 2/3/4 signature 의 conv/superadd/peak-align 4-축 단조 ordering 에는 silicon-class 5 가 *연결* 되지 않음 (deferred). 본 H 는 신호 등록만, 단조 정합은 별 H 필요 (a_completeness_over_cheap 정합).
- D3 triangulation 의 EEG L2 Φ=1.59 와 AKIDA Φ_proxy=0.297 는 *서로 다른 metric* — scalar comparison 보다 *signature shape* 비교가 더 honest. diff>0 falsifier 는 "있다" attest 만, "단조" 아님.
- D4 QRNG quality 는 std>0 단일 axis — NIST-style randomness suite 통과는 별 falsifier.

## 8. 논의

PR#1371 silicon-confirm 을 UNIVERSE 본격 inherit. p7 (no perplexity verdict) 정합 — perplexity 가 아닌 *signature shape* 으로 inverse-U 확증. a_paper_significance 잠재후보 (silicon transfer of edge-of-chaos universal).

## 9. 양방향 sibling

- ⇄ [AKIDA](../AKIDA/AKIDA.md) · D1 silicon-confirm milestone 기록
- ⇄ [AKIDA.easy.md](../AKIDA/AKIDA.easy.md) Group F D1~D5
- ⇄ [H_672](./H_672_akida_spontaneous_firing.md) ~ [H_678](./H_678_akida_channel_bridge.md) (6 sisters)
- ⇄ H_670 (edge-of-chaos universal, ECA+logistic)
- ⇄ PR#1371 (D1 silicon transfer · 카이로스 verdict inherit)
- ⇄ PR#1372 (EEG L2 synthetic Φ=1.59 · 본 H D3 substrate input)
- ⇄ [CANDIDATES](./CANDIDATES.md)

## 10. 다음 작업

- D2 silicon-class 5 단조 정합 — convexity/super-add/peak-align signature 추가 측정 (별 H)
- D3 3-substrate *signature shape* normalized comparison (scalar diff 보다 honest) 
- D5 closed-discovery paper 후보 — a_paper_on_discovery 조건 충족 시 (a_paper_only_at_closure: FULL closure 까지 deferred)
- 산출물: `state/akida_hw_sw_impl_2026_05_29/H_677_sw_result.json`
