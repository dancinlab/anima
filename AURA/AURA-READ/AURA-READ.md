# AURA-READ — current state

@title: 📖 AURA-READ — "뇌 읽기 (디코드)"

@goal: 뇌→기계 **디코드 축** — 모든 read 앱(motor_decode·dbs_reach·의식모니터·통신·nav decode·seizure 감지)을 묶는 횡단 축. read 깊이 한계: 피질 ✅(0.79) / 심부 🔴(0.06, 전기/자기 LPF 붕괴). ⚠ CORE/DECODER(의식엔진 콘텐츠생성)와 무관.

## 왜 (핵심 축)

```
📖 뇌 읽기 (디코드)
- 하는 일: 두피 밖 센서로 뇌 활동을 읽어 기계로 — 운동의도·의식수준·발화 디코드
- 비유: 뇌를 마이크로 듣기 — 깊을수록 소리 묻힘
```

읽기/쓰기는 AURA 깊이 벽(C15)의 **비대칭** 축 — 피질선 읽기 우위, 심부선 쓰기(음향)만 도달.

## 진행 (milestones)

- [x] (app ✅) read/write × 깊이 비대칭 toy — `app/read_depth.py` 실동작, verify
- [ ] 횡단 인덱스 — 다른 도메인의 read 앱 통합 대시보드
- [ ] real head-model 깊이감쇠 실측 (AURA-HEADMODEL 연계)

## 세부분류 (횡단 인덱스)

이 축에 속한 앱: motor_decode(CORTEX)·dbs_reach(DEEP)·의식모니터·통신디코드·nav decode·seizure 감지(MED)·endovasc read

- `app/read_depth.py` — read × 깊이 비대칭 실동작 toy
- `verify/read_depth.txt` — verdict

## sibling
- 부모: [AURA](../AURA.md) · 짝 축: AURA-WRITE · 트리: [AURA-TREE.md](../AURA-TREE.md)
