# H_9832 — workspace 의 typed compose/falsify 를 **입의 전방경로**에 넣는다 (R11-3)

**status:** 🔴 **RETRACTED (2026-07-21 · 등록 당일 · self-caught)** — 이 카드가 딛고 선 부품이
**프로덕션에 없다**. 죽은 계보 재생성.
**source:** sol `#3 typed workspace compose/falsify forward lane` (fable 의 data-face 논거가 지지 · NOVEL-to-fable)
**wired:** no — 미구현.

## ⛔ 철회 사유 (먼저 읽을 것)

`core/cognitive_workspace.py` 는 **origin/main 에 존재하지 않는다.** 커밋
`6762f11b7 remove(workspace): require model-native G1 G6` 이 workspace 계층 **17개 core 모듈**과
chat/evaluate/corpus 의 모든 workspace 플래그·전용 테스트·CI·문서를 삭제했다. CHANGELOG 원문:

> "G1/G6 성공을 **모델·엔진 자체 출력에서만** 인정하기 위해 Python 이 통제 문법, typed 후보,
> 반증 대안, structured renderer/fallback, 증거 ledger 와 proof 를 생성·선택하던 workspace 계층을
> 제거했다. (…) 이전 0.20.58–0.20.87 의 workspace PASS 기록은 **시스템 orchestration 의 역사일 뿐
> 모델-native G1/G6 통과로 승계하지 않는다.**"

즉 오너는 **바로 이 각도를 이미 실행하고 죽였다.** 그리고 그 사유는 lab full 의 두 모델이
독립적으로 경고한 자기반론과 **동일하다** — "바깥의 typed 실행기가 답을 계산했다".

**내 오류 3단:** ① lab full 브리프의 kill-list 에 workspace 제거를 넣지 않았다(census 누락 ·
`lab-full-killlist-must-sweep-adjacent-dead-lineage` 가 경고한 바로 그 실패) → ② sol 이
**34 커밋 뒤처진 로컬 체크아웃**의 파일을 읽고 설계했다(stale-branch 함정) → ③ 나는 그 인용을
검증 없이 카드로 승격했다. 계보 census 는 브리프 작성 시점이지 사후가 아니다.

**살릴 수 있는 잔여물:** typed 2항 join 자체는 H_9830 이 **모델-native 경로**(CLMS store lane)로
이미 담고 있다. workspace 를 되살리는 각도는 **금지** — 되살리면 G1/G6 통과가 정의상 승계 불가다.

---

## (이하 철회된 원문 — 기록 보존)

## Question

뇌 부품 중 **`CognitiveWorkspace` 만이** 실제 2항 typed join(`CompositionRule.apply`)과 **명시적
반증 테스트**(`.test`)를 갖고 있다 — sol 이 `core/cognitive_workspace.py` 로 확인(A⇄G 는 emit 스칼라
게이트, dream 은 빈 기하 중점). 그렇다면 이 typed 결과를 **입의 전방경로에 넣고**, 반사실 손실이
추출기와 공유 trunk 까지 흐르게 하면 G1(합성)과 G6(반증가능 생성) 양쪽에 동시에 닿는다.

## Intervention (flag 형태 · 미구현)

```
anima-py train --brain-loop workspace-claim \
               --brain-workspace-task {compose,falsify,both} \
               --brain-credit-route {lane-only,l3-shared} \
               --brain-runtime required --lang en
```

학습된 EN 추출기가 `(subject, relation, object, falsifier, ground)` 를 만들고, workspace 가
compose/test/select 한 typed 결과를 mouth forward 에 주입. 같은-entity/wrong-relation 반사실
손실이 추출기와 공유 trunk 로 역전파.

## Arms + controls

| arm | 무엇 | 읽는 법 |
|---|---|---|
| LIVE | `--brain-workspace-task both` | ρ·weave Δ + ρ·fan 반증가능 rate |
| **relation-shuffle** | 관계 라벨만 치환 | 붕괴해야 함 |
| **falsifier-shuffle** | 반증자만 문서 간 셔플 | 붕괴해야 함 |
| **ce-mass** | 동일 바이트질량 plain CE | "손실이 하나 늘었다" 배제 |
| **lane-only** vs **l3-shared** | 신용 경로 분리 | trunk 가 실제로 바뀌는가 |
| **오라클 추출기** | 손으로 만든 typed 튜플 | 양성통제. 학습된 추출기가 실패하고 이것만 성공하면 **H_9359 는 안 뚫린 것** |

## kill-list 비중복

read-side / post-hoc 탈출이 아니라 **train+serialize+runtime 전방 lane** 이다. workspace 는
veto(H_9269)·affect(H_9411)·tension(H_9630/33) 죽은 계보와 별개 부품 —
`lab-full-killlist-must-sweep-adjacent-dead-lineage` 대조로 재생성 아님을 확인.

## $0 스크리너

H_9815 토이 + 합성 typed 튜플. 오라클 추출기 arm 이 xor ≥0.80 을 못 내면 **INSTRUMENT-DEAD**
(음성 판독 금지 · `positive-control-before-reading-a-negative`).

## 판독가능성

- workspace relation/intervention 민감도 = **오늘 (b)**.
- 실제 G1 = **(a) H_9827 수리 선행** · 실제 G6 = **(a) H_9828/H_9829 수리(249 draws) 선행**.

## 미결정 위험

typed declaration/derivation 타깃을 **넣어줄 때만** 데이터 벽을 공격한다 — 자연 corpus 에서 정보를
창조하지 않는다. 따라서 양성이 나와도 진짜 레버가 뇌가 아니라 **새 supervision/데이터**일 수 있다.
이 분해를 사전등록하지 않으면 판정이 뒤집힌다.

**related:** H_9359 · H_9304 · H_9828 · H_9829 · H_9830 · H_9834
