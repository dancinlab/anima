# AURA-RTSC-MEG 앱 — 🧲 "상온 자기안경"

> AURA-RTSC-MEG 도메인 첫 실동작 앱. 상온초전도 고밀도 자기센서 read — 채널밀도가 복원율 lever(cryo 비용장벽 제거). honest 🟡 toy(ubu-1 numpy, 공유 LF 모델). 세부트리=app/(코드)+verify/(검증).

## 무엇 (일반인)

```
🧲 상온 자기안경
- 하는 일: 상온초전도 고밀도 자기센서 read — 채널밀도가 복원율 lever(cryo 비용장벽 제거)
- 비유: 뇌 표면을 센서로 읽고/쓰는 BCI 앱 — AURA 깊이×방향 지형도의 한 칸
```

## 결과 (verify/density_scaling.txt)

| 채널수 | read R² |\n|---|---|\n| 32 | 0.168 |\n| 64 | 0.438 |\n| 128 | 0.567 |\n| 256 | 0.663 |\n| 512 | **0.745** |

## 세부트리

```
AURA-RTSC-MEG/
├── AURA-RTSC-MEG.md          도메인 스냅샷
├── app/
│   ├── spec.md        이 문서
│   └── density_scaling.py  실동작 toy (공유 LF 헬퍼 + 도메인 실험)
└── verify/
    └── density_scaling.txt verdict (verbatim)
```

## honest
- 🟡 toy(10×10 합성 소스·가우시안 lead-field·ridge). 절대 수치 toy-specific, 정성 robust.
- 다음: real head-model(AURA-HEADMODEL) · 실 데이터 · hexa-native 포팅(handoff f125d45c).

## sibling
- 도메인: [AURA-RTSC-MEG.md](../AURA-RTSC-MEG.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
