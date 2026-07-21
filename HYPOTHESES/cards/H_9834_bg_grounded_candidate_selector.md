# H_9834 — 접지된 "어느 후보인가" 선택기로 G6 의 신용할당을 친다 (R11-5)

**status:** 🟠 **BLOCKED-ON-DEAD-DEPENDENCY (2026-07-21 · 등록 당일 · self-caught)** — 학습 보상원이
삭제된 부품이다. 아래 정정을 먼저 읽을 것.
**source:** sol `#2 grounded BG "WHICH candidate" selector` — **NOVEL**(fable 은 G6 확률 부여 자체를 거부)
**wired:** no — 미구현.

## ⛔ 정정 — 보상원이 프로덕션에 없다

원 설계는 `CognitiveWorkspace.test` 의 접지/미반증 보상으로 `VBasalGate` 를 학습시킨다. 그런데
`core/cognitive_workspace.py` 는 `6762f11b7 remove(workspace): require model-native G1 G6` 에서
**삭제됐다**(17 core 모듈 일괄 · 사유 = G1/G6 은 모델·엔진 자체 출력에서만 인정 · workspace PASS
기록은 **승계 불가**). 상세 → H_9832 (RETRACTED).

⟹ **이 카드는 보상 신호를 모델-native 로 갈아끼우기 전엔 발사 불가.** 선택기 골격
(`--brain-loop bg-select` · K 후보 · oracle_pool_recall 선행 DV · 4 통제)은 유효하나, 보상을
외부 심볼릭 판정기에서 받으면 **양성이 나와도 G6 통과로 승계되지 않는다** — 삭제 사유가 그것이다.
모델-native 대체 후보는 `core/rho_fan.py` 의 엔진-네이티브 채점 op 뿐이며, 그것을 학습 보상으로
쓰는 것은 **게이트 자기표본 재사용**(`burned-gate-no-refreeze-sequential-gating`) 위험이 있어
별도 설계가 필요하다. 그 설계 없이는 OPEN 이 아니라 BLOCKED.

---

## (이하 원문)

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
