# AURA-CORTEX 앱 — 🧠 "생각 리모컨"

> AURA-CORTEX 도메인 첫 실동작 앱. 운동 의도(손/발/혀/휴식 등 5-class)를 피질 표면 read로 분류 — 커서·의수 제어 BCI. honest 🟡 toy(ubu-1 numpy, 공유 LF 모델). 세부트리=app/(코드)+verify/(검증).

## 무엇 (일반인)

```
🧠 생각 리모컨
- 하는 일: 운동 의도(손/발/혀/휴식 등 5-class)를 피질 표면 read로 분류 — 커서·의수 제어 BCI
- 비유: 뇌 표면을 센서로 읽고/쓰는 BCI 앱 — AURA 깊이×방향 지형도의 한 칸
```

## 결과 (verify/motor_decode.txt)

| 모달 | 5-class 정확도 |\n|---|---|\n| EEG-64 | 100% |\n| RTSC-MEG-256 | 100% |\n| tFUS-64 | 100% |

## 세부트리

```
AURA-CORTEX/
├── AURA-CORTEX.md          도메인 스냅샷
├── app/
│   ├── spec.md        이 문서
│   └── motor_decode.py  실동작 toy (공유 LF 헬퍼 + 도메인 실험)
└── verify/
    └── motor_decode.txt verdict (verbatim)
```

## honest
- 🟡 toy(10×10 합성 소스·가우시안 lead-field·ridge). 절대 수치 toy-specific, 정성 robust.
- 다음: real head-model(AURA-HEADMODEL) · 실 데이터 · hexa-native 포팅(handoff f125d45c).

## sibling
- 도메인: [AURA-CORTEX.md](../AURA-CORTEX.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
