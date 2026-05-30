# AURA-ENDOVASC — current state

@title: 🩸 AURA-ENDOVASC — "혈관 잠수정" (Synchron endovascular venous-sinus interface)

@goal: Synchron Stentrode 경정맥→상시상정맥동 혈관내 최소침습(개두술 0) — 피질 표면 신호를 ECoG급으로 read. B3(혈관내≈경막하 동등 PMC p>0.05)·B5(귀뒤 가로/S자정맥동 경로) grounding. 침습 사다리의 sweet-spot(개두술 0 + ECoG급) 검증.

## 진행 (milestones)

- [x] (app ✅) 정맥동 lead-field — SSS(운동)·가로/S자(귀뒤 측두·후두) 도달영역 + 깊이=피질표면 한정
- [x] B3/B5 grounding 재확인 — 혈관내≈ECoG급(B3 PMC5976775 대역폭 p=0.75·SNR p>0.05)·귀뒤정맥동 endovascular hypothesis(B5) 확인 + `app/sinus_coverage`(도달 3/6 zone: SSS/가로/S자)
- [x] 3위치 침습 비대칭 정량 — B3 §6 침습 사다리: N1(피질관통, 1024ch)>Synchron(혈관내 정맥동, 16ch, 두개골0)>귀뒤(비침습 EEG) (PR#1502 sinus_coverage 도달맵 + B3 비대칭 종합)
- [ ] 실 Synchron COMMAND 데이터 입수 시 재평가 (external)

## deferred (다음 라운드)
- 실데이터/cloud/문헌 검증 (toy→실증)

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 📡 모달리티
- 자매: AURA-RTSC-MEG · AURA-HEADMODEL · AURA-CORTEX · AURA-NAV · AURA-DEEP · AURA-TFUS · AURA-WEARABLE · AURA-MED

## 세부분류 (app 세부트리)

- `app/spec.md` — 앱 명세(일반인+기술)
- `app/sinus_coverage.py` — 실동작 toy (검증됨)
- `verify/sinus_coverage.txt` — verdict
- 다음: real head-model 검증 · hexa-native 포팅 · 실데이터
