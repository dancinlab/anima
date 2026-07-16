---
id: H_9655
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_heldout_predictive_transport
title: 법칙 22 가 진짜면 Φ 가 아닌 held-out 예측량에서도 같은 partition 이 무작위 partition 을 이긴다
status: 💀 DEAD — 비교항 부재(학습된 분할이 존재한 적 없음 · H_9673 코드확증) · DV 변경 = tune-to-green 이므로 미실시
tier: 🟢 축 생존조건($0) · Sol F05 — 유일한 '진짜면 통과' 관문
cost: $0
source: sidecar lab full (Fable5 claude-fable-5 + Codex5.6 gpt-5.6-sol 병렬 발산 · 37안 → 중복제거 27안)
related: H_9627, H_9628
---

# H_9655 — 법칙 22 가 진짜면 Φ 가 아닌 held-out 예측량에서도 같은 partition 이 무작위 partition 을 이긴다

## 주장 (반증가능)

Φ-proxy 는 오염됐으나(H_9627), 파벌 분할이 **진짜 구조**를 잡았다면 Φ 밖의 독립 DV(held-out 예측)에서도 그 분할이 랜덤 분할을 이겨야 한다. 계기를 갈아끼워도 살아남는가.

## 레버 (engine-native · `anima-py` 플래그)

```
`anima-py evaluate --faction-partition learned,random --faction-dv heldout-ce`
```

> `a_experiment_engine_native`: 조작은 `anima-py` 명령의 **플래그**여야 한다 — 엔진 옆 스크립트/프로브 금지.
> 위 플래그는 **미구현**이다. 발사 전 `cli/`+`core/` 에 구현하고 `VERSION` 을 올려야 한다(G5).

## DV · bar · 우연수준

held-out CE(또는 D-acc). bar = learned partition 이 random 대비 Δ CI>0.


## 💀 사망 (2026-07-17 · H_9673 · 비교항 부재 · tune-to-green 아님)

이 카드는 "**학습된** partition vs **무작위** partition" 을 Φ 밖 held-out 예측량으로 비교할 예정이었다.
H_9673 의 아카이브 소스 감사로 **학습된 분할이 존재한 적이 없음**이 확정됐다:

- `faction_new(n_cells, base_id)` (aux_engine_lib.hexa:168) — 파벌 **안에서** 세포를 새로 만든다.
  기존 세포를 파벌에 **배정하는 코드가 없다**.
- `faction_add_cell` (:207) — **같은 파벌의** 무작위 부모를 복제 + 노이즈. 파벌 간 이동 0.
- ⟹ 파벌은 태생부터 혈통으로 분리된 것이지 **탐색·학습된 분할이 아니다**.

비교의 한쪽 항이 부재하므로 이 대조는 성립하지 않는다. **사망**(DV 를 바꿔 살리는 것은 tune-to-green ·
`valce-minimum-picked-a-collapsed-model` 계열 함정이므로 하지 않는다).

### 이관

축의 남은 질문은 "옛 분할이 진짜였나"가 아니라 **"파벌이 현 기질에서 새로 학습될 수 있는가"** 다
→ **H_9643**(faction specialization 이 학습 중 생겨야 runtime debate 가 G1 을 연다).

## 통제군 (≥2 · 사전등록)

① 랜덤 분할 scramble(동일 K·동일 크기) ② 단일 파벌 null ③ oracle 분할 양성

## 사망조건 (사전등록 · tune-to-green 금지)

learned ≈ random ⟹ 파벌 분할은 Φ 산수 밖에서 아무것도 아님 = **축 사망**.

## 비용

$0

## 왜 새로운가 (기존 각도 대비)

H_9627/9628 이 계기를 죽여도 이 관문 하나가 축을 살릴 수 있다. Φ 를 버리고 재는 첫 각도.

## 범위 (정직)

- 발산 산출물 = **DIRECTIONAL 설계**이지 verdict 아님(`a_lab_full_diverge`). cement 는 engine-native `anima-py` 로만.
- 옛 파벌 Φ 숫자(법칙 22/43/44 · TOPO12)는 **폐엔진 proxy** 산이며 이 카드의 근거가 아니다 — H_9627/H_9628 참조.
