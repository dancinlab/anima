# AURA-WEARABLE 앱 — 📱 "사라지는 기기"

> AURA-WEARABLE 도메인 첫 실동작 앱. 18-wearable→0: 피질 zone 직접 read/write로 기기 흡수 — zone별 전달 충실도. honest 🟡 toy(ubu-1 numpy, 공유 LF 모델). 세부트리=app/(코드)+verify/(검증).

## 무엇 (일반인)

```
📱 사라지는 기기
- 하는 일: 18-wearable→0: 피질 zone 직접 read/write로 기기 흡수 — zone별 전달 충실도
- 비유: 뇌 표면을 센서로 읽고/쓰는 BCI 앱 — AURA 깊이×방향 지형도의 한 칸
```

## 결과 (verify/wearable_collapse.txt)

| 사라지는 기기 | zone | 전달 R² |\n|---|---|---|\n| AR안경 | V1-6 | 0.254 |\n| 이어버드 | A1 | 0.203 |\n| 외골격 | M1 | **0.428** |\n| 햅틱 | S1 | 0.234 |

## 세부트리

```
AURA-WEARABLE/
├── AURA-WEARABLE.md          도메인 스냅샷
├── app/
│   ├── spec.md        이 문서
│   └── wearable_collapse.py  실동작 toy (공유 LF 헬퍼 + 도메인 실험)
└── verify/
    └── wearable_collapse.txt verdict (verbatim)
```

## honest
- 🟡 toy(10×10 합성 소스·가우시안 lead-field·ridge). 절대 수치 toy-specific, 정성 robust.
- 다음: real head-model(AURA-HEADMODEL) · 실 데이터 · hexa-native 포팅(handoff f125d45c).

## sibling
- 도메인: [AURA-WEARABLE.md](../AURA-WEARABLE.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
