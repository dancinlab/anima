# AURA-DEEP 앱 — 🧬 "심해 탐지기"

> AURA-DEEP 도메인 첫 실동작 앱. 심부핵(보상·각성·기분) read 도달성 — 비침습 read는 깊이서 붕괴 확인(침습 필요). honest 🟡 toy(ubu-1 numpy, 공유 LF 모델). 세부트리=app/(코드)+verify/(검증).

## 무엇 (일반인)

```
🧬 심해 탐지기
- 하는 일: 심부핵(보상·각성·기분) read 도달성 — 비침습 read는 깊이서 붕괴 확인(침습 필요)
- 비유: 뇌 표면을 센서로 읽고/쓰는 BCI 앱 — AURA 깊이×방향 지형도의 한 칸
```

## 결과 (verify/dbs_reach.txt)

| 깊이 | read R² |\n|---|---|\n| M1 피질 1.0 | 0.884 |\n| 시상 5.5 | 0.128 |\n| VTA/LC 7.0 | 0.072 |

## 세부트리

```
AURA-DEEP/
├── AURA-DEEP.md          도메인 스냅샷
├── app/
│   ├── spec.md        이 문서
│   └── dbs_reach.py  실동작 toy (공유 LF 헬퍼 + 도메인 실험)
└── verify/
    └── dbs_reach.txt verdict (verbatim)
```

## honest
- 🟡 toy(10×10 합성 소스·가우시안 lead-field·ridge). 절대 수치 toy-specific, 정성 robust.
- 다음: real head-model(AURA-HEADMODEL) · 실 데이터 · hexa-native 포팅(handoff f125d45c).

## sibling
- 도메인: [AURA-DEEP.md](../AURA-DEEP.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
