# AURA-MOTOR — current state

@title: 🦾 AURA-MOTOR — "운동 출력"  [응용층]

@goal: 운동 read+write 응용 — M1 운동의도 디코드(커서·의수·외골격) + S1 고유감각 피드백. 옛 CORTEX motor_decode·WEARABLE exoskeleton 통합. 피질 표면 ✅(M1 d1.0 최고 도달).

## 진행 (milestones)

- [x] (app ✅) 세부 앱 3종 실동작 toy — app/ + verify/
- [ ] real head-model 깊이감쇠 실측 (AURA-HEADMODEL 연계)
- [ ] hexa-native 포팅 (handoff f125d45c)

## 세부분류 (sub-app)

- `app/motor_decode.py` — 🕹️ 운동의도 디코드(M1 5-class)
- `app/exoskeleton.py` — 🦿 외골격/의수 제어
- `app/cursor.py` — 🖱️ 커서/포인터
- `verify/` verdict · 분류: 응용층

## sibling
- 부모: [AURA](../AURA.md) · 트리: [AURA-TREE.md](../AURA-TREE.md) · 축: AURA-READ·AURA-WRITE·AURA-DEPTH
