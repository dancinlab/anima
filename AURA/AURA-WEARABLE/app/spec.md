# AURA-WEARABLE 앱 — 🎯 대체 가능 기기 sub-app 모음

> AURA-WEARABLE 도메인은 단일 앱이 아니라 **여러 sub-app**의 묶음 — 기기 하나하나가 독립 앱. 각 app/<이름>.py 실동작 toy(ubu-1 검증). honest 🟡 toy(공유 LF·zone 깊이).

## sub-app 목록 (6개)

| sub-app | 타깃 zone | 깊이 | 방향 | 도달 R² |
|---|---|---|---|---|
| 🥽 AR글래스 | V1-6 시각피질에 디스플레이 write — 안경 없이 시야에 영상 | d1.2 | write | 0.393 |
| 🎧 이어버드 | A1 청각피질에 오디오 inject + 의도 read — 이어폰 사라짐 | d1.5 | 양방 | 0.203 |
| 🦾 외골격/의수 | M1 운동의도 read + S1 고유감각 write — 외골격 제어 | d1.0 | read+write | 0.428 |
| ✋ 햅틱/e-skin | S1 체감각피질에 촉각 write — 인공피부 사라짐 | d1.3 | write | 0.234 |
| ⌚ 스마트워치 | S1/A1에 알림 write — 손목 진동 없이 직접 인지 | d1.4 | write | 0.217 |
| 🎙️ 음성비서 | subvocal M1 read — 말 안 해도 명령 인식 | d1.1 | read | 0.412 |

## 패턴
- 표면 zone(V1-6·M1·A1·S1)=비침습 도달 ✅(0.20~0.43)
- 각 sub-app = `app/<이름>.py`(실동작) — `python3 app/<이름>.py` 실행

## sibling
- 도메인: [AURA-WEARABLE.md](../AURA-WEARABLE.md) · 트리: [AURA-TREE.md](../../AURA-TREE.md)
