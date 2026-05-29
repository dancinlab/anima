# AURA-NAV 앱 — 🧭 "뇌 속 내비" (V5/V6 AR 네비게이션 오버레이)

> AURA-NAV 도메인의 첫 실동작 앱. 시각피질 V5/V6(운동·공간 영역)에 길안내 턴-화살표를 직접 write — AR 안경 없이 실제 거리 위에 화살표가 떠 보인다. 앱 세부트리 = `app/`(코드) + `verify/`(검증). honest 🟡 toy.

## 무엇 (일반인)

```
🧭 뇌 속 내비 — "AR 안경 없는 길안내"
- 하는 일: GPS 턴 신호(좌/우/직진...)를 시각피질에 직접 그려 거리 위에 화살표가 보이게
- 비유: 자동차 HUD가 유리창에 길 띄우듯, 뇌가 시야에 직접 화살표를 띄움
- vs 구글맵 AR: 안경 화면이 아니라 V5/V6에 직접 = 디바이스 0, V1(1차시각)은 안 건드려 실제 시야 보존
```

## 파이프라인

```
GPS 턴(8방향) ──encode──▶ V5/V6 화살표 활성맵(12×12 retinotopic)
                              │ write (모달 focality σ + 잡음)
                              ▼
                         지각된 활성맵 ──decode──▶ 방향 분류 + 지각 충실도 R²
```

## 핵심 결과 (verify/nav_write_fidelity.txt)

| 모달(write focality) | σ | 8방향 정확도 | 지각 충실도 R² |
|---|---|---|---|
| EEG-class (blurry) | 2.6 | 100% | 0.766 |
| OPM-MEG | 1.6 | 100% | 0.839 |
| tFUS focal | 0.9 | 100% | 0.867 |
| RTSC-MEG 고밀도 | 0.7 | **0.980** |

→ **거친 방향 분류는 어떤 비침습 모달도 가능(100%)** — 좌/우/직진 길안내는 EEG급으로도 OK. 단 **화살표 선명도(지각 충실도)는 focal write 필요**(RTSC-MEG 0.98 ≫ EEG 0.77). 정밀 AR(차선·정확한 각도)엔 고밀도 자기/음향 write.

## 세부트리

```
AURA-NAV/
├── AURA-NAV.md            도메인 스냅샷
├── app/
│   ├── spec.md            이 문서
│   ├── nav_overlay.py     실동작 toy (encode→write→decode, 검증됨)
│   └── nav_overlay.hexa   hexa-native 동반 스켈레톤
└── verify/
    └── nav_write_fidelity.txt   verdict (verbatim)
```

## honest
- 🟡 toy: 12×12 합성 화살표·가우시안 focality·nearest-template 디코더. 절대 σ/R²는 toy-specific.
- 정성 robust: blurry write=각도 뭉개짐(저충실), focal write=또렷. 깊이=피질 표면(V5/V6 비침습 도달, C16).
- 다음: 실 retinotopy 매핑 · phosphene 지각 모델 · 동적 경로(연속 턴) · V1 보존 검증.

## sibling
- 도메인: [AURA-NAV.md](../AURA-NAV.md) · 모달: AURA-RTSC-MEG·AURA-TFUS(focal write) · 응용: AURA-WEARABLE(AR안경 대체)
