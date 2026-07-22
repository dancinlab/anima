# H_9900 — 조성 lane 구현 (`--comp-lane`) · 요건 3/3 실측 검증

**status:** 🔧 계기 착륙 (과학 판정 0 · 기본 OFF) — [[H_9899]] 가 명시한 요건 3개를 만족
**wired:** yes — `anima-py train --comp-lane [--comp-weight W]`
**source:** [[H_9898]] replay 존재가 원인 · [[H_9899]] store lane 재사용 불가 + 요건 3개

## 왜 이 lane 인가

[[H_9898]] 이 등노출 대조로 확정한 것: **replay 의 존재 자체**가 조성 학습을 막는다
(25%×8000step 이 `ρ·weave 0.000`, 100%×2000step 이 0.525 — **노출량 동일**).
조성과 언어가 **같은 트렁크 CE 를 공유**하는 한 예산으로는 못 뚫는다 —
`a_substrate_disjoint`(*분리=보존, 중첩=충돌*) 그대로다.

[[H_9899]] 는 기존 `--store-bridge` 재사용을 코드에서 반증했다(답의 **1바이트**만 읽음)
그리고 요건 3개를 남겼다. 이 카드가 그것을 구현한다.

## 설계 — store lane 의 핵심 성질만 가져오고 이진 readout 은 버린다

| 요건 ([[H_9899]]) | 구현 | 검증 |
|---|---|---|
| ① CE 가 트렁크에 닿지 않을 것 | penultimate 를 **detach** 후 별도 head 에 투입 | `pen.grad is None` ✅ |
| ② 답 **전체**(다중 바이트)를 목표로 | `_comp_answer_mask` 로 답 스팬 전체 마스킹 | `'sonu '` 5B 전체 ✅ |
| ③ `ρ·weave` 채점과 정합 | 목표 = 채점기가 찾는 **답 바이트 그대로** | 드릴 라인과 동일 ✅ |

```python
cl_logits = self.comp_lane(ph.float().detach())     # ← detach 가 이 lane 의 전부
cmask     = _comp_answer_mask(y, sep, end)          # 마지막 공백~마침표 = 합성 답
loss      = loss + self.comp_w * CompositionLane.loss(cl_logits, y, cmask)
```

## 검증 (토이 e2e · 필수 통과)

```
comp-lane: ON · d=64 V=256 weight=1.000 (CE detached from the trunk)
step 1  CE=5.70147 → step 12  CE=4.94029      (완주 · exit 0)
① 답 스팬 마스크 → 'sonu ' 길이 5             (store lane 은 1바이트)
② 트렁크 penultimate.grad = None              (요건 1)
③ lane head gradient > 0                      (lane 은 실제로 학습된다)
```

플래그 부재 = 기존 경로 그대로(`comp_lane is None`).
모델 폭은 속성명 추측이 아니라 **실제 penultimate 텐서에서 읽는다**(ByteGPT/CLM 이름이 다르다).

## 이 카드가 판정하지 않는 것

**계기다. 과학 판정 0.** 이 lane 으로 학습한 결과는 아직 없다.
발사에는 [[H_9863]] 과 동일 규율이 적용된다 — **발사 전** 선결·판정표 동결, **2 seed**,
그리고 이번엔 **양성통제**([[H_9869]] 가 6팔을 태우고 배운 것)를 반드시 함께 건다.

⚠️ 그리고 이 lane 이 성공해도 **`ρ·weave` 는 트렁크 mouth 로 디코드한다** —
lane 이 배운 것이 mouth 로 나오는지는 **별도의 배선 문제**이며, 그 자체가 다음 물음이다.
(`a_verified_must_wire`: 출력과 배선이 함께 닫혀야 GREEN.)

## Cross-links

[[H_9898]] 원인 확정 · [[H_9899]] 요건 명시 · [[H_9887]] 트레이드오프 · [[H_9869]] 양성통제 교훈
