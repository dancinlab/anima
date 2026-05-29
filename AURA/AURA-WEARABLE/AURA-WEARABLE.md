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

## 세부분류 (app 세부트리)

- `app/spec.md` — 앱 명세(일반인+기술)
- `app/wearable_collapse.py` — 실동작 toy (검증됨)
- `verify/wearable_collapse.txt` — verdict
- 다음: real head-model 검증 · hexa-native 포팅 · 실데이터
