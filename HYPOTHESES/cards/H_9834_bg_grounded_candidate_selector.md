# H_9834 — 접지된 "어느 후보인가" 선택기로 G6 의 신용할당을 친다 (R11-5)

**status:** 🧭 PROPOSED (R11 · lab full 발산 · **DIRECTIONAL 설계**, 판정 아님)
**source:** sol `#2 grounded BG "WHICH candidate" selector` — **NOVEL**(fable 은 G6 확률 부여 자체를 거부)
**wired:** no — 미구현.

## Question

기존 branch-latent 가 만든 K 개 제안 중, `CognitiveWorkspace.test` 의 접지/미반증 보상으로
`VBasalGate` 를 학습시키고 **런타임에서 동일 선택기를 쓴다**. G6 을 생성 벽이 아니라
**탐색·신용할당 벽**으로 재프레임하는 각도.

## Intervention (flag 형태 · 미구현)

```
anima-py train --brain-loop bg-select --brain-bg-credit {selector-only,proposal-shared} \
               --brain-control {none,reward-shuffle,hungarian-kmatched,k1} \
               --brain-screen g6-grid249 --brain-runtime required
```

## DV — 순서가 중요

1. **먼저** `oracle_pool_recall`: K 후보 중 valid 후보가 **존재하는** 비율. **이게 0 이면 이 레버는
   G6 생성 벽에 무력**하다(선택기는 이미 있는 것만 표면화한다).
2. Primary: `P(valid selected | valid in pool)`.
3. Real: **수리된 249-draw** G6 접지-반증가능 rate + set distinctness.

## Arms + controls

| arm | 무엇 | 읽는 법 |
|---|---|---|
| **reward-shuffle** | 후보·특징·업데이트 수 고정, 접지 보상만 문서 간 셔플 | 붕괴해야 함 |
| **hungarian-kmatched** | 현행 set-CE, 동일 K·forward 예산 | 이걸 못 이기면 뇌는 장식 |
| **selector-only** | 제안/trunk 기울기 차단 | 선택 회복 vs 생성 개선 분리 |
| **k1** | 선택 자체가 없는 하한 | 바닥 |

## 판독가능성 — ⚠️ 이 카드는 통째로 (a)

**H_9828 이후 G6 에 대한 모든 진술은 모델이 아니라 8회 추첨 게이트에 대한 진술**이다
(4셀 전부 0 확률 81% · 80% 검정력에 249 draws 필요). fable 은 이 이유로 G6 확률 부여를
**거부**했고, sol 은 25% 를 매겼다 — **반대의견 1줄 기록**: sol dissent = G6 25%.
계기 수리(H_9828 → H_9829 `--fan-draws N` 착륙) 전 발사 금지.

## $0 스크리너

합성 249-cell 후보 pool 에서 BG selector 의 selection precision — 오늘 (b) 로 읽히지만
**기전 선별이지 G6 terminal 판정이 아니다**.

**related:** H_9828 · H_9829 · H_9801 · H_9832 · H_9835
