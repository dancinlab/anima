# AURA-TFUS — current state

@title: 🔊 AURA-TFUS — "초음파 손가락" (focused-ultrasound non-invasive deep write)

@goal: 읽기/쓰기 비대칭의 유일 비침습 심부 갈래 — 집속초음파는 음향(전기 아님)이라 두개골 우회해 심부 *자극*(write) 가능, but read는 C15 벽. C6서 tFUS가 두개골 전기-LPF 우회 돌파(+0.317) 입증. brainwire beyond-electrical-stimulation 모달.

## 진행 (milestones)

- [x] (app ✅) tFUS 심부 자극 모델 — 음향 focal write, 심부 도달 + FDA tFUS 강도 한계
- [ ] 읽기 벽 vs 쓰기 가능 — 비침습 심부 폐루프 불가, open-loop 자극만
- [ ] 성인 비침습 음향-imaging 성숙도 문헌 — fUS read는 신생아/동물 주력 (honest gap)
- [ ] 안전성·심부 심도 한계 — 음향 감쇠·열(Pennes) 문헌

## deferred (다음 라운드)
- 실데이터/cloud/문헌 검증 (toy→실증)

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 🧬 심부(🔴침습)
- 자매: AURA-RTSC-MEG · AURA-ENDOVASC · AURA-HEADMODEL · AURA-CORTEX · AURA-NAV · AURA-DEEP · AURA-WEARABLE · AURA-MED

## 세부분류 (app 세부트리)

- `app/spec.md` — 앱 명세(일반인+기술)
- `app/acoustic_write.py` — 실동작 toy (검증됨)
- `verify/acoustic_write.txt` — verdict
- 다음: real head-model 검증 · hexa-native 포팅 · 실데이터
