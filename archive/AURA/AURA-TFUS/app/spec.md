# AURA-TFUS 앱 — 🔊 "초음파 손가락"

> AURA-TFUS 도메인 첫 실동작 앱. 집속초음파 비침습 심부 *쓰기*(자극) — 음향이 전기보다 깊이서 덜 감쇠(d5서 역전). honest 🟡 toy(ubu-1 numpy, 공유 LF 모델). 세부트리=app/(코드)+verify/(검증).

## 무엇 (일반인)

```
🔊 초음파 손가락
- 하는 일: 집속초음파 비침습 심부 *쓰기*(자극) — 음향이 전기보다 깊이서 덜 감쇠(d5서 역전)
- 비유: 뇌 표면을 센서로 읽고/쓰는 BCI 앱 — AURA 깊이×방향 지형도의 한 칸
```

## 결과 (verify/acoustic_write.txt)

| 깊이 | tFUS 음향 | MEG 전기 |\n|---|---|---|\n| 1.5 | 0.201 | 0.320 |\n| 3.0 | 0.132 | 0.142 |\n| 5.0 | **0.102** | 0.066 |

## 세부트리

```
AURA-TFUS/
├── AURA-TFUS.md          도메인 스냅샷
├── app/
│   ├── spec.md        이 문서
│   └── acoustic_write.py  실동작 toy (공유 LF 헬퍼 + 도메인 실험)
└── verify/
    └── acoustic_write.txt verdict (verbatim)
```

## honest
- 🟡 toy(10×10 합성 소스·가우시안 lead-field·ridge). 절대 수치 toy-specific, 정성 robust.
- 다음: real head-model(AURA-HEADMODEL) · 실 데이터 · hexa-native 포팅(handoff f125d45c).

## sibling
- 도메인: [AURA-TFUS.md](../AURA-TFUS.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
