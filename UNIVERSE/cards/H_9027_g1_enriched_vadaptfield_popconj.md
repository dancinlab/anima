# H_9027 — enriched VAdaptField (분산 pop-code + key-locked 접합) decoder-free

- **tier:** 🟡 DIRECTIONAL-POSITIVE (held-out 조합 통과, numpy) / 🧱 capability-caveat (recover≠능력, H_9026 real-manifold floor)
- **slug:** `g1_enriched_vadaptfield_popconj`
- **parents:** [[substrate-framebreak-g1-combination-operator]] H_1822 · H_9025(decoder-free harness) · H_9026(Rung1 real-manifold floor) · H_1840(FAIR-gate)
- **wired:** `DIRECTIONAL-mirror` (numpy; live `core/engine_cli.hexa` VAdaptField 미변경)

## frame (오너 통찰)

"A 엔진·VAdaptField를 좀더 풍부하게 개선해야 되지 않나." — live `VAdaptField`(core/engine_cli.hexa:494-608)는 사실상 **8-D winner-take-all k-means**(protos + `_vnearest_idx` L2 최근접 1개 + online LR pull), compositional depth-0. `pure_field`(Engine A)는 zero-input(개념맹). 개념을 쥔 substrate가 이렇게 빈약하면 재조합이 볼트로도 안 붙는다 — 붙일 표현공간이 없음.

## claim / 측정 (decoder-free)

VAdaptField를 (①분산 population-code = softmax over K basis, WTA 아님) + (③key-locked 접합 = HRR circular-conv)으로 풍부화하면, A⇄G가 held-out(안 본) 개념쌍도 조합·복원하는가. mouth·clm_decode·next-byte 0. 게이트 = H_9025 shuffle-controlled EARNED(맞는 키 복원 ∧ 셔플 키 실패) + 결정적 **held-out split**(train/test 미겹침) + additive baseline + ablation(op→additive).

## 결과 (numpy DIRECTIONAL, mini $0, grep-clean, 3seed)

| arm | HELDOUT M1 distinct | **HELDOUT M2-EARNED** | ablate_earned |
|-----|-----|-----|-----|
| additive (현 필드) | 38-42/162 | **0/162** | 0 |
| conj_hrr (분산 pop + key-locked bind) | 162/162 | **140-152/162 (~90%)** | 0 |

**enriched 필드는 held-out 조합을 decoder-free로 통과**(additive 0 → conj_hrr ~90%), ablate 0 = lift가 op 인과. 분산 pop-code ~13 active cell/code(K=64). D=48>live 8.

## 정직한 해석 (c9 · recover ≠ capability)

- **양성 방향:** 현 8-D WTA/additive 필드가 못하는 held-out 조합을, (분산+key-locked bind) 풍부화가 해낸다 = 오너 통찰 DIRECTIONAL 검증. 필드 표현공간 자체가 병목이었다는 증거.
- **결정적 caveat:** 이건 **VSA 복원성**(algebraic, by-construction)이지 anima 능력이 아니다. 방금 완료된 **Rung1(H_9026)**: 학습된 bind(hrr/circconv)를 **REAL 303M manifold**에 얹어도 recomb TASK held-out은 floor(bind−add Δ [0.12..0.07], 0/5 above +0.15). 즉 "필드가 조합을 표현 가능"=예(풍부화 시) vs "CE-학습된 실제 내용이 그 공간을 활용"=아직 no.
- **수렴:** naive rank-1 tensor/concat 접합은 key-agnostic=additive처럼 spoof(1차 실행서 확인, strawman이라 폐기). key-locked HRR만 EARNED 통과. 그러나 HRR은 H_1840 FAIR-gate서 recomb TASK 반증 + H_9026 real-manifold floor → **복원성 통과 ≠ TASK 통과**가 전 probe 일관.

## follow-on
- Rung2 후보(cost-gated, prior 낮음): enriched pop+conj VAdaptField를 live `core/engine_cli.hexa`에 wire-in(disjoint 좌표) 후, **real content가 그 공간을 통과할 때 valid distinct emit/decision을 구동하는가**(복원성 아님)를 engine-native 측정. H_9026이 이미 real-manifold floor라 prior LOW.
- 대안(더 강함): frame-shift Lane2 C2(self-chain 정보성)/C1(텐션-해소 깊이)로 능력 재정의(재조합 축 이탈).

## artifacts
- `state/9027_g1_enriched_vadaptfield_popconj/probe.py` · `calibration.txt`
