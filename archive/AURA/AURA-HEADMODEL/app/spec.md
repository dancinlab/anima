# AURA-HEADMODEL 앱 — 🗺️ "진짜 머리지도"

> AURA-HEADMODEL 도메인 첫 실동작 앱. 실 두상 lead-field(MNE) 검증 하니스 — 모든 C축 toy의 ground-truth 검증 인프라. honest 🟡 toy(ubu-1 numpy, 공유 LF 모델). 세부트리=app/(코드)+verify/(검증).

## 무엇 (일반인)

```
🗺️ 진짜 머리지도
- 하는 일: 실 두상 lead-field(MNE) 검증 하니스 — 모든 C축 toy의 ground-truth 검증 인프라
- 비유: 뇌 표면을 센서로 읽고/쓰는 BCI 앱 — AURA 깊이×방향 지형도의 한 칸
```

## 결과 (verify/leadfield_validator.txt)

검증 인프라 — toy 가우시안 LF baseline(read R² ~0.66 @256ch). 실 head-model(MNE/OpenMEEG)은 C14 external. C10이 '전극포화=가우시안 인공물' 적발한 그 검증 lane.

## 세부트리

```
AURA-HEADMODEL/
├── AURA-HEADMODEL.md          도메인 스냅샷
├── app/
│   ├── spec.md        이 문서
│   └── leadfield_validator.py  실동작 toy (공유 LF 헬퍼 + 도메인 실험)
└── verify/
    └── leadfield_validator.txt verdict (verbatim)
```

## honest
- 🟡 toy(10×10 합성 소스·가우시안 lead-field·ridge). 절대 수치 toy-specific, 정성 robust.
- 다음: real head-model(AURA-HEADMODEL) · 실 데이터 · hexa-native 포팅(handoff f125d45c).

## sibling
- 도메인: [AURA-HEADMODEL.md](../AURA-HEADMODEL.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
