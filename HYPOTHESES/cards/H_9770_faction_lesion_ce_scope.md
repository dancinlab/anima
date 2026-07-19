---
id: H_9770
group: faction-lateral-axis-r3
series: R9 divergence (lab full · Fable 5 λ2 · H_9643 de-risk 후속) · 2026-07-18
date: 2026-07-18
slug: faction_lesion_ce_scope
title: CE-scope 파벌 lesion — G0-fail artifact 위에서 teacher-forced 특화가 실재하는가 (신규 협소 claim · $0)
status: PROPOSED · DIRECTIONAL design (lab-full divergence — cement 는 engine-native anima-py 실측 후)
tier: ⭐⭐ R9-2 · $0 (pool GPU decode) · KILL 이면 파벌-303M 질문 전체가 $0 TERMINAL
cost: $0
source: Fable 5 divergence — 브리핑 Q3. 원 게이트(G0 PASS 요구)는 소각·불변; 이 카드는 **새 H·새 사전등록**이다
related: H_9643, H_9737, H_9769, H_9771
---

# H_9770 — CE-scope faction lesion (G0-fail artifact · 재조준이지 게이트 재동결이 아님)

## Q3 판정 (설계 논거)
- lesion 계기는 **teacher-forced 도메인별 held-out ΔCE** 를 잰다 (evaluate.py:12032 · mask-chans 경로) — 자유생성 무관. G0 는 이 추정기의 타당성 조건이 아니었다.
- 진짜 타당성 조건: ①CE substrate 비퇴화 — val_CE pooled 1.332(K=1 1.340 과 parity)+DESCENT 4/4 로 충족, 단 `valce-minimum-picked-a-collapsed-model` 가드로 per-register CE vs 상수예측기 floor 명시 확인 ②null 적법성(아래).
- ⛔ 단, 소각된 G0 게이트를 같은 H 에서 조용히 삭제하면 `burned-gate-reanchor-is-tune-to-green` — 그래서 **새 H id + 명시적 천장**: 이 카드의 GREEN 은 "CE-scope 파벌 특화" 까지만. 원 claim("G0-sound 303M 파벌")은 G0-passing artifact 없이는 영원히 OPEN.

## 설계 ($0 · 3-arm · 계기 전부 실재)
- arm L: `k8_s7.clm --faction-lesion <domains.json> --perm 200 --win 24` — 학습된 K=8 분할의 S(=‖R‖²_F).
- arm N1(구조-무 null): `clm303_clean.clm --faction-lesion … --faction-split 8` — K=1 ckpt 에 8-way 분할 **강제**(H_9737 선례 · evaluate.py:12075). 파벌-무학습 모델의 S 분포.
- arm N2(순열 null): 각 arm 의 `--perm 200` null95 (`chance-level-must-be-derived-per-metric` — 지표별 유도).
- 통제 정합: clm303_clean 은 val_CE 1.340 vs 1.332 로 **매개 공변량(CE) 일치** — CE-기반 readout 엔 param-match 보다 이것이 옳은 짝(`control-must-match-mediating-covariate`). param-matched arm 은 H_9771 이 공급(보강용).
- domains.json = 4-cell held-out (ko-gen·en-gen·ko-sns·en-sns) — corpus 분할 기존 자산 재사용.

## 사전등록 bar
- GREEN(CE-scope): S_L > null95(perm_L) **AND** S_L > max(S_N1 분포) — 두 null 동시 초과.
- KILL: S_L ≤ null95 — 보고 시 검정력 필수(S 분포 sd·MDE·toy 효과크기 대비). KILL = "K=8/4-cell/303M 서 파벌 미학습" **TERMINAL** → lane 전체 $0 종결(coherence 논쟁 무의미화).
- 우연-아래 칸: S_L < S_N1 중앙값이면 별도 기록(역-구조 신호 = 계기 결함 의심 재소환).

## 판정 분기
- KILL → 파벌-303M $0 TERMINAL. H_9771/H_9772 fire 불요.
- GREEN → "파벌은 303M CE-공간서 학습되는 레버(G0-fail artifact 한정)" — coherence 귀속은 H_9771 로.
