# AURA-MED 앱 — ⚕️ 질병 통제 sub-app 모음

> AURA-MED 도메인은 단일 앱이 아니라 **여러 sub-app**의 묶음 — 질환 하나하나가 독립 앱. 각 app/<이름>.py 실동작 toy(ubu-1 검증). honest 🟡 toy(공유 LF·zone 깊이).

## sub-app 목록 (6개)

| sub-app | 타깃 zone | 깊이 | 방향 | 도달 R² |
|---|---|---|---|---|
| ⚡ 간질 | 피질 focus 발작 감지/억제 — N1 고샘플링 빠른 검출+GABA/anti-phase 억제 | d1.5 | read+stim | 0.203 |
| 🌊 우울증 | raphe 5HT 심부 신경조절 — 심부라 비침습 read 불가, DBS/tFUS stim | d6.5 | stim | 0.076 |
| 🎚️ 파킨슨 | STN 심부 운동게이팅 — DBS 확립 임상, 심부 침습 | d5.5 | stim | 0.092 |
| 🦿 마비 재활 | M1 운동복원 — 피질 표면 read, 비침습 도달 높음 | d1.0 | read | 0.428 |
| 👁️ 실명 복원 | V1 시각피질 write — 시각 복원, 피질 표면 도달 | d1.2 | write | 0.393 |
| 🩹 만성통증 | S1/대상피질 통증 modulate — sulcal 깊어 부분도달 | d2.5 | modulate | 0.114 |

## 실 임상 현황 (침습 outcome — toy 비침습 R²와 modality 다름 ⚠)
- ⚡ 간질: RNS System 9년 median 발작 75%↓ (FDA승인) · 🌊 우울: SCC-DBS TRD response ≥50% 2–8년 유지
- 🎚️ 파킨슨: STN-DBS UPDRS 25–41%↑ (표준치료) · 🦿 마비: BrainGate Utah-array 커서/로봇팔 제어 (feasibility)
- 👁️ 실명: Orion 피질보철 5/5 위치탐지 (early-feasibility) · 🩹 통증: MCS/DBS 장기 responder ~39%
- 상세·출처·toy↔실임상 갭 = [CLINICAL-GROUNDING.md](../CLINICAL-GROUNDING.md)

## 패턴
- 피질질환(간질·마비·실명)=비침습 ✅ / 심부질환(우울 raphe·파킨슨 STN)=침습 필요 🔴(0.08~0.09)
- ⚠ 정직: 실 임상 효능은 거의 전부 **침습**(DBS·피질 implant) — toy R²(비침습)와 직교. toy 낮은 우울·파킨슨이 침습 임상선 오히려 강함.
- 각 sub-app = `app/<이름>.py`(실동작) — `python3 app/<이름>.py` 실행

## sibling
- 도메인: [AURA-MED.md](../AURA-MED.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
