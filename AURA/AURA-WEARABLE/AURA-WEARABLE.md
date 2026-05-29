# AURA-WEARABLE — current state

@title: 📱 AURA-WEARABLE — "사라지는 기기" (18-wearable → 0 collapse)

@goal: demiurge cortex pillar σ=12 zone에 직접 read/write하면 모든 웨어러블이 사라진다 — AR안경(V1~V6)·이어버드(A1)·외골격(M1)·e-skin(S1)·스마트워치·음성비서가 피질 직접 인터페이스로 흡수. 피질 도달(C16)이 실현권 보장. 각 기기↔zone↔방향 매트릭스.

## 진행 (milestones)

- [x] (app ✅) 18-wearable → 0 매트릭스 — 기기↔σ=12 zone↔read/write 완성 (demiurge 표 정량화)
- [ ] AR/VR 안경 → V1~V6 write(48 px-class) — 디스플레이 없는 증강현실
- [ ] 이어버드/보청기 → A1·A2 — 오디오 inject + 의도 read
- [ ] 지각 대역폭 vs 기기 — 흡수 가능 경계(피질 도달 reach 기준)

## deferred (다음 라운드)
- 실데이터/cloud/문헌 검증 (toy→실증)

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 🎯 응용
- 자매: AURA-RTSC-MEG · AURA-ENDOVASC · AURA-HEADMODEL · AURA-CORTEX · AURA-NAV · AURA-DEEP · AURA-TFUS · AURA-MED

## 세부분류 (sub-app 모음)

- `app/ar_glasses.py` — 🥽 AR글래스 (V1-6 시각피질에 디스플레이 write — 안경 없이 시야에 영상, R²=0.393)
- `app/earbuds.py` — 🎧 이어버드 (A1 청각피질에 오디오 inject + 의도 read — 이어폰 사라짐, R²=0.203)
- `app/exoskeleton.py` — 🦾 외골격/의수 (M1 운동의도 read + S1 고유감각 write — 외골격 제어, R²=0.428)
- `app/haptics.py` — ✋ 햅틱/e-skin (S1 체감각피질에 촉각 write — 인공피부 사라짐, R²=0.234)
- `app/smartwatch.py` — ⌚ 스마트워치 (S1/A1에 알림 write — 손목 진동 없이 직접 인지, R²=0.217)
- `app/voice_assistant.py` — 🎙️ 음성비서 (subvocal M1 read — 말 안 해도 명령 인식, R²=0.412)
- `app/spec.md` 개요 · `verify/subapps.txt` verdict

