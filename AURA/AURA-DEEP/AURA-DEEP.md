# AURA-DEEP — current state

@title: 🧬 AURA-DEEP — "심해 무대감독" (deep-nuclei neuromodulation)

@goal: relocate-N1 "전뇌통제"의 정체 — 심부핵 상태제어(보상 VTA·각성 LC·기분 raphe·의식 시상·기억 해마). 비침습 read는 벽(C15 R²<0.2), 침습 N1/DBS만 닿음. "위치 우회→투사경로 심부 간접도달"(A6/A7 구조축) 검증.

## 진행 (milestones)

- [x] (app ✅) DBS 타깃 역량 카탈로그 — STN(파킨슨 확립)·VTA(보상)·raphe(기분)·시상(의식)
- [ ] 읽기/쓰기 비대칭 정량 — decode 벽(R²<0.2) vs stim 가능
- [ ] N1-relocate 투사경로 심부 간접도달 — A6/A7 구조축(DLPFC→VTA) 재검
- [ ] 의식 게이트(시상) — 혼수 각성·마취 역전 시나리오

## deferred (다음 라운드)
- 실데이터/cloud/문헌 검증 (toy→실증)

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 🧬 심부(🔴침습)
- 자매: AURA-RTSC-MEG · AURA-ENDOVASC · AURA-HEADMODEL · AURA-CORTEX · AURA-NAV · AURA-TFUS · AURA-WEARABLE · AURA-MED

## 세부분류 (app 세부트리)

- `app/spec.md` — 앱 명세(일반인+기술)
- `app/dbs_reach.py` — 실동작 toy (검증됨)
- `verify/dbs_reach.txt` — verdict
- 다음: real head-model 검증 · hexa-native 포팅 · 실데이터
