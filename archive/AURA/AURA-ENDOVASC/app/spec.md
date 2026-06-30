# AURA-ENDOVASC 앱 — 🩸 "혈관 잠수정"

> AURA-ENDOVASC 도메인 첫 실동작 앱. Synchron 정맥동 혈관내 도달 zone 매핑 — 표면 피질 yes, 심부 no(B3/B5). honest 🟡 toy(ubu-1 numpy, 공유 LF 모델). 세부트리=app/(코드)+verify/(검증).

## 무엇 (일반인)

```
🩸 혈관 잠수정
- 하는 일: Synchron 정맥동 혈관내 도달 zone 매핑 — 표면 피질 yes, 심부 no(B3/B5)
- 비유: 뇌 표면을 센서로 읽고/쓰는 BCI 앱 — AURA 깊이×방향 지형도의 한 칸
```

## 결과 (verify/sinus_coverage.txt)

도달 3/6 zone: M1(SSS)·측두A1(가로동)·후두V1(S자동) | 미도달: DLPFC·섬엽·심부핵

## 세부트리

```
AURA-ENDOVASC/
├── AURA-ENDOVASC.md          도메인 스냅샷
├── app/
│   ├── spec.md        이 문서
│   └── sinus_coverage.py  실동작 toy (공유 LF 헬퍼 + 도메인 실험)
└── verify/
    └── sinus_coverage.txt verdict (verbatim)
```

## honest
- 🟡 toy(10×10 합성 소스·가우시안 lead-field·ridge). 절대 수치 toy-specific, 정성 robust.
- 다음: real head-model(AURA-HEADMODEL) · 실 데이터 · hexa-native 포팅(handoff f125d45c).

## sibling
- 도메인: [AURA-ENDOVASC.md](../AURA-ENDOVASC.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
