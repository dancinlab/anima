# AURA-SENSE — current state

@title: 👁️ AURA-SENSE — "감각 입출력"  [응용층]

@goal: 감각 read/write 응용 — 시각(AR네비·디스플레이)·청각(오디오)·체감각(햅틱)·알림. demiurge σ=12 zone 중 V1-6·A1·S1. NAV(AR네비)·옛 WEARABLE 감각기기가 여기로 통합. 피질 표면 비침습 ✅.

## 진행 (milestones)

- [x] (app ✅) 세부 앱 5종 실동작 toy — app/ + verify/
- [x] real head-model 깊이감쇠 실측 (AURA-HEADMODEL 연계) — HEADMODEL 3-shell(Ary1981, PR#1514/1517) 깊이 envelope R² 0.239→0.016로 부분 해소 (3-shell 해소·실 MNE 비구형/tangential은 external 잔여)
- [ ] hexa-native 포팅 (handoff f125d45c)

## 세부분류 (sub-app)

- `app/ar_nav.py` — 🧭 AR 네비(V1-6 턴화살표)
- `app/ar_display.py` — 🥽 AR 디스플레이(V1-6)
- `app/audio_io.py` — 🎧 오디오 입출력(A1)
- `app/haptics.py` — ✋ 햅틱/e-skin(S1)
- `app/notify.py` — ⌚ 알림(S1/A1)
- `verify/` verdict · 분류: 응용층

## sibling
- 부모: [AURA](../AURA.md) · 트리: [AURA-TREE.md](../AURA-TREE.md) · 축: AURA-READ·AURA-WRITE·AURA-DEPTH
