---
id: H_9737
group: faction-lateral-axis-r3
date: 2026-07-17
slug: faction_fitmatched_k1_negative_control
title: fit-matched K=1 음성대조 — 같은 낮은-CE·파벌구조 없음이면 --faction-lesion S ≤ null95 (낮은 분모서도 FPR 통제)
status: 🟢 PASS (격리 인증 완료 · perm=200) — K=1 fit-matched(loss 0.0128) + --faction-split 4: S 0.406 ≤ null95 1.221 p=0.86 결정적 clean. 낮은-CE 분모(v1 폭발 스케일)서도 log-ratio 가 적합품질을 특화로 오인 안 함 = 계기 v2 SOUND 3번째 다리. random-init K=4 의 경계(p=.0448 grouped-conv 블록 confound)를 대체하는 깨끗한 음성. 계기 `--faction-split N` 신설(lesion 분할을 ckpt n_factions 와 독립 강제)로 측정.
tier: 🟢 계기 인증 음성대조 (toy · $0)
cost: $0/pool
source: sidecar lab full (Fable5+Sol · H_9643 계기 v2 판정 분석)
related: H_9643, H_9731, H_9733
---

## 왜 (빠진 인증 셀)

계기 `--faction-lesion` v2 인증 삼각대: ① random-init 음성(높은-CE 4.8 스케일서 FPR 통제 ✅) ② ORACLE 양성(학습-스케일 검정력). **빠진 3번째 다리 = 적합-정합 음성대조**.

random-init 음성은 base_CE~4.8(무학습) 스케일서만 FPR 을 통제한다. 학습 ckpt 는 base_CE~0.01 — log-ratio 로 고쳤지만 **낮은-분모 스케일서 FPR 이 통제되는지는 미인증**. 참값이 "파벌 구조 없음"이면서 base_CE 가 학습 스케일인 대조가 필요하다.

## 설계 ($0/pool · toy 학습 1회)

- **K=1(groups=1)** 로 같은 마르코프 4소스 toy 를 같은 낮은 CE(~0.01)까지 학습 → CLMF 없는 단일 trunk.
- 그 ckpt 에 **contiguous 4-분할**을 사후 부과해 `--faction-lesion` (v2 log-ratio).
- 참값 = "파벌 구조 없음"(K=1 은 채널 칸막이 없음)인데 base_CE 는 학습 스케일.

## 판정

- **PASS(격리 인증)**: S ≤ null95 ⟹ 낮은-분모 스케일서도 FPR 통제됨 = log-ratio 정규화가 적합품질을 특화로 오인하지 않음. → 계기 v2 SOUND 4다리 중 3번째 완성.
- **FAIL**: S > null95 ⟹ log-ratio 여도 낮은-CE 서 거짓양성 = 계기 v2 아직 미완, 정규화 재수리.
- D5(교란): H_9731 처럼 S_contig 도 병행 — conv 국소성이 index-연속 블록에 구조를 줄 수 있으니 contiguity 교란 배제 전 cement 금지.

## 병렬 세션 (a_parallel_session_compare)

H_9731(발견-partition)·H_9733(content-transfer)이 안 덮는 NOVEL 셀 (그들은 K>0 ckpt 의 발견블록/content 를 다룸 · 이건 K=1 ckpt 의 적합-정합 FPR). CONFLICT 없음.


## 🟢 결과 (perm=200 · 2026-07-17)

K=1 fit-matched ckpt(같은 마르코프 4소스 · groups=1 · loss 0.0128) + `--faction-split 4` → **S 0.406 ≤ null95 1.221 (p=0.86, null 한복판) = PASS(clean)**. 참값 '파벌구조 없음'인데 base_CE 는 학습 스케일 → log-ratio 가 낮은-분모서 거짓양성 안 냄 격리 확증. 계기 v2 SOUND 4다리 완성(H_9643).
