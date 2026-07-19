---
id: H_9733
group: faction-lateral-axis-r3
series: R4 divergence (lab full · Fable 5 λ3) · 2026-07-17
date: 2026-07-17
slug: faction_partition_content_transfer
title: 발견 partition 의 내용-전이 — learned 특화는 내용이 바뀌어도 같은 분할을 예측한다
status: PROPOSED · DIRECTIONAL design only (lab-full divergence)
tier: 🧭 R4 제3렌즈(보조) · $0(pool)
cost: $0
source: Fable 5 divergence — H_9676(not-layout)과 직교하는 partition-vs-partition 안정성 축
related: H_9674, H_9676, H_9731
---

# H_9733 — partition 내용-전이 (structure 가 내용에 물려있는가, 표본에 물려있는가)

## 프레임

learned 기능 특화라면 발견 partition 은 **프롬프트 내용이 바뀌어도** 같아야 한다(소유권은 가중치에
있으므로). 표본-상관 artifact 라면 프롬프트셋을 갈아끼우는 순간 partition 이 흩어진다. H_9676 은
partition↔index-layout 정렬(ARI≈0)을 쟀고, 이 카드는 **partition↔partition**(내용 A vs 내용 B)을
잰다 — 다른 축.

**비충돌 증명**: py303_full.clm 만 사용 · trained ckpt 불요 · lesion lane 무접촉.
**kill-list 차별화**: 재구성-manifest 아님(신규 EN 프롬프트셋 2개 · `--lang en` EN-FIRST 준수) ·
구조-존재 재증명 아님(존재는 전제·안정성의 출처가 질문).

## 레버 (engine-native — flag 확장)

```
anima-py evaluate py303_full.clm --faction-block-transfer <promptsA.json> <promptsB.json> \
  [--n-factions-sweep 4,8,12] [--win 24] [--seed 12345]
```
- 구현: `faction_block_provenance_run`(cli/evaluate.py:10763) 의 clusterer-assignment 재사용
  (:10819 "returns the ASSIGNMENT") — A/B 각각 발견 후 일치도 산출. 프롬프트셋은
  `anima-py corpus --lang en` 산출 도메인-분리 2셋(내용 겹침 0).

## DV · bar · 우연(실측)

- DV = NMI(assign_A, assign_B) (K 셀별 · ARI 병기).
- 우연 = ① 라벨-perm null 200회의 null95 ② pedestal-쌍(두 i.i.d. 셋) NMI — **둘 다 실측**,
  bar = max(①,②) 초과 (우연 가정 금지 · chance-level-must-be-derived-per-metric).

## 양성통제 (계기-킬)

1. planted 공유-블록 합성쌍(같은 latent 블록 · 다른 잡음 실현)이 이 N/d 에서 전이 bar 를 넘어야
   한다 — 실패 ⟹ INSTRUMENT-DEAD · 판정 미발행.
2. 같은-내용 반분(A₁ vs A₂) NMI 가 null95 이하 ⟹ clusterer 자체 불안정 = 계기사망
   (H_9731 PC-C 와 공유 게이트).

## 사망조건

- D1: 양성통제 실패 ⟹ 계기사망(음성 아님).
- D2: NMI(A,B) ≤ bar ∧ 같은-내용 반분 NMI > bar ⟹ partition 은 내용-표본 산물 = learned-구조
  읽기 약화(artifact 쪽 1표).
- D3: 같은-내용 반분도 불안정 ⟹ H_9674 블록의 '실재' 자체가 clusterer-실현 의존 — 상위 lane 에 보고.

## Honest scope

제3렌즈·보조. 전이 성공은 learned 와 '안정적 비-layout artifact' 를 완전히 못 가른다(H_9676 이
layout 을 이미 배제했으므로 지지 증거로만) — 단독 cement 불가, H_9731/H_9732 와 합산 판독.
