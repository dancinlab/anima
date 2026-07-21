# H_9832 — workspace 의 typed compose/falsify 를 **입의 전방경로**에 넣는다 (R11-3)

**status:** 🧭 PROPOSED (R11 · lab full 발산 · **DIRECTIONAL 설계**, 판정 아님)
**source:** sol `#3 typed workspace compose/falsify forward lane` (fable 의 data-face 논거가 지지 · NOVEL-to-fable)
**wired:** no — 미구현.

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
