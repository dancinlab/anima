# AURA-CORTEX — current state

@title: 🧠 AURA-CORTEX — "산호초 다이버" (cortical non-invasive I/O capability)

@goal: AURA 깊이 벽(C15)의 양성 절반 — 비침습 도달 피질 역량(reach R² 0.82~0.91)을 실현권으로 확정. 異種모달 고밀도 스택(RTSC-MEG+tFUS+동적시간)으로 운동·통신·집행상태·의식수준을 침습급 근접 디코드. demiurge σ=12 zone(M1·A1·PFC) 정량판.

## 진행 (milestones)

- [x] (app ✅) 운동 디코드(M1) — in-silico 0.91 → 실 EEG/MEG 운동의도 분류
- [ ] 통신 디코드 — 내적발화/언어피질(A1) decode, 락트인 통신
- [ ] 의식수준 모니터 — big-Φ/α 피질 통합 (anima BRAIN/UNIVERSE 연계, 마취심도)
- [ ] 집행상태(DLPFC, A3 golden-zone) — 인지부하/작업기억 모니터

## deferred (다음 라운드)
- 실데이터/cloud/문헌 검증 (toy→실증)

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 🧠 피질(✅비침습)
- 자매: AURA-RTSC-MEG · AURA-ENDOVASC · AURA-HEADMODEL · AURA-NAV · AURA-DEEP · AURA-TFUS · AURA-WEARABLE · AURA-MED

## 세부분류 (app 세부트리)

- `app/spec.md` — 앱 명세(일반인+기술)
- `app/motor_decode.py` — 실동작 toy (검증됨)
- `verify/motor_decode.txt` — verdict
- 다음: real head-model 검증 · hexa-native 포팅 · 실데이터
