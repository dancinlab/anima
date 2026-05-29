# AURA-RTSC-MEG — current state

@title: 🧲 AURA-RTSC-MEG — "상온 자기 안경" (room-temp superconductor nano-coil magnetic read/write)

@goal: 상온초전도 나노코일 타일로 cryo(액체헬륨) 없이 두피에 자기센서를 고밀도로 깔아 뇌 자기장을 read(MEG급 fT) + write(TMS급 focal) — demiurge COIL pillar(σ²=144ch/tile·1296-ch hex lattice) + C13 채널밀도 lever(EEG+RTSC 0.854) 결합. 비침습 자기 모달이 피질 도달 침습급 근접하는지 toy→실증.

## 진행 (milestones)

- [x] (app ✅) RTSC 나노코일 lead-field 모델 — read(pick-up loop fT) + write(drive loop focal E) φ=2 시분할
- [ ] C13 채널밀도 lever 재현 — 256ch 자기센서 복원율 0.85, cryo비용장벽 제거가 본질임을 정량
- [ ] demiurge COIL pillar 환류 — verify/numerics_coil_*.hexa 정합 (Biot-Savart·TMS figure-8 parity)
- [ ] 상온초전도 실재 conditional — RTSC el-ph 잡(pods) bridge, 물질 확증 시 재평가

## deferred (다음 라운드)
- 실데이터/cloud/문헌 검증 (toy→실증)

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 📡 모달리티
- 자매: AURA-ENDOVASC · AURA-HEADMODEL · AURA-CORTEX · AURA-NAV · AURA-DEEP · AURA-TFUS · AURA-WEARABLE · AURA-MED

## 세부분류 (app 세부트리)

- `app/spec.md` — 앱 명세(일반인+기술)
- `app/density_scaling.py` — 실동작 toy (검증됨)
- `verify/density_scaling.txt` — verdict
- 다음: real head-model 검증 · hexa-native 포팅 · 실데이터
