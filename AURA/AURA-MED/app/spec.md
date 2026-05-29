# AURA-MED 앱 — ⚕️ "뇌 치료실"

> AURA-MED 도메인 첫 실동작 앱. 간질 발작 감지/억제 — N1 고샘플링이 RNS보다 빠른 검출(의학 응용). honest 🟡 toy(ubu-1 numpy, 공유 LF 모델). 세부트리=app/(코드)+verify/(검증).

## 무엇 (일반인)

```
⚕️ 뇌 치료실
- 하는 일: 간질 발작 감지/억제 — N1 고샘플링이 RNS보다 빠른 검출(의학 응용)
- 비유: 뇌 표면을 센서로 읽고/쓰는 BCI 앱 — AURA 깊이×방향 지형도의 한 칸
```

## 결과 (verify/seizure_detect.txt)

발작 감지 지연: 전 샘플링서 window 해상도 내 즉시검출(toy 한계). 실측 우위는 N1 고샘플링(20kHz)서 RNS 대비 ~15× 빠른 검출(brainwire) — 실 데이터 필요.

## 세부트리

```
AURA-MED/
├── AURA-MED.md          도메인 스냅샷
├── app/
│   ├── spec.md        이 문서
│   └── seizure_detect.py  실동작 toy (공유 LF 헬퍼 + 도메인 실험)
└── verify/
    └── seizure_detect.txt verdict (verbatim)
```

## honest
- 🟡 toy(10×10 합성 소스·가우시안 lead-field·ridge). 절대 수치 toy-specific, 정성 robust.
- 다음: real head-model(AURA-HEADMODEL) · 실 데이터 · hexa-native 포팅(handoff f125d45c).

## sibling
- 도메인: [AURA-MED.md](../AURA-MED.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
