# H_9904 — lane head 를 mouth 없이 직접 채점한다 (포맷 캠페인 개시 여부의 판별기)

**status:** 🔧 계기 착륙 (과학 판정 0 · **DIRECTIONAL 전용**)
**wired:** yes — `train --comp-lane --comp-probe-panel <panel.json>`
**source:** [[H_9903]] 포맷 계약이 합류를 막음 · [[H_9901]] ①과 ④의 배타성

## 왜 필요한가

[[H_9903]] 이 확정했다: lane head 는 serialize 에서 **버려지므로** `evaluate` 의 mouth 가
영원히 읽지 못하고, `ρ·weave` 는 lane 이 무엇을 배우든 **구조적으로 눈이 멀어 있다.**
그 경로를 여는 것은 `.clm` 포맷 변경(**별도 캠페인** · 2-production parity 포함)이다.

⟹ **그 캠페인을 열 가치가 있는가?** 는 *'lane 이 조성을 배우긴 했는가'* 로 결정된다.
이 계기가 포맷 없이 그것만 답한다.

## 설계 — teacher-forced, mouth 미경유

단서를 문맥으로 넣고 **답 위치마다 lane head 의 argmax** 를 정답 바이트와 대조한다.
`--comp-probe-panel <weavepanel.json>` 로 held-out 패널을 그대로 재사용한다.

## ⚠️ DIRECTIONAL 전용 — 이 수치로는 아무것도 못 박는다

엔진 디코드의 **거울**이므로 `a_engine_native_learning` 상 **DIRECTIONAL** 이다.
이 카드는 그 제약을 계기 자체에 적어 넣었다(출력 문자열이 매번
`DIRECTIONAL · teacher-forced · not a verdict` 를 찍는다).

**이 수치가 결정하는 것은 단 하나** — [[H_9903]] 이 스코핑한 포맷 캠페인을 열지 말지.
- `byte_acc` 가 높다 ⟹ lane 은 배웠고 **막는 것은 배선뿐** ⟹ 포맷 캠페인 정당
- `byte_acc` 가 0 근처 ⟹ 분리 축은 **읽기 이전에** 죽었다 ⟹ 포맷 캠페인 **불필요**

## 검증 (토이 e2e)

```
comp-lane: ON · d=32 V=256 · 8 step
comp-lane HELD-OUT (DIRECTIONAL · teacher-forced · not a verdict): byte_acc=0.0000 over 126 bytes
```
8 step 토이에서 `0.0000` 은 **정상**이다(배울 시간이 없다) — 계기가 끝까지 도는 것을 확인한다.
플래그 부재 = 기존 경로 그대로.

## Cross-links

[[H_9903]] 포맷 블로커 · [[H_9901]] 배선 실패 · [[H_9900]] lane · [[H_9883]] 조성 실재
