# AURA-READ — current state

@title: 📖 AURA-READ — "뇌 읽기 (디코드)"

@goal: 뇌→기계 **디코드 축** — 모든 read 앱(motor_decode·dbs_reach·의식모니터·통신·nav decode·seizure 감지)을 묶는 횡단 축. read 깊이 한계: 피질 ✅(0.79) / 심부 🔴(0.06, 전기/자기 LPF 붕괴). ⚠ CORE/DECODER(의식엔진 콘텐츠생성)와 무관.

## 왜 (핵심 축)

```
📖 뇌 읽기 (디코드)
- 하는 일: 두피 밖 센서로 뇌 활동을 읽어 기계로 — 운동의도·의식수준·발화 디코드
- 비유: 뇌를 마이크로 듣기 — 깊을수록 소리 묻힘
```

읽기/쓰기는 AURA 깊이 벽(C15)의 **비대칭** 축 — 피질선 읽기 우위, 심부선 쓰기(음향)만 도달.

## 진행 (milestones)

- [x] (app ✅) read/write × 깊이 비대칭 toy — `app/read_depth.py` 실동작, verify
- [x] 횡단 인덱스 — 다른 도메인의 read 앱 통합 대시보드 ✅ → [AURA-AXES-INDEX.md](../AURA-AXES-INDEX.md) (앱×방향×깊이×모달 SSOT)
- [x] real head-model 깊이감쇠 실측 (AURA-HEADMODEL 연계) — HEADMODEL 3-shell(Ary1981, PR#1514/1517) 깊이 envelope R² 0.239→0.016로 부분 해소 (3-shell 해소·실 MNE 비구형/tangential은 external 잔여)

## 세부분류 (횡단 인덱스)

**read 방향 앱 전수** (응용 4 도메인 횡단 — 분류 SSOT = [AURA-AXES-INDEX.md](../AURA-AXES-INDEX.md)):

| 앱 | 도메인 | 깊이 | 비고 |
|---|---|---|---|
| `motor_decode` | 🦾 MOTOR | 피질 (M1 d1.0) | 운동의도 5-class, 최고 도달 |
| `cursor` | 🦾 MOTOR | 피질 (M1) | 커서/포인터 |
| `exoskeleton` | 🦾 MOTOR | 피질 (M1+S1) | read/write 양방향 |
| `consciousness_monitor` | 🧠 COGNITION | 피질 (전역) | big-Φ/α 의식수준 |
| `subvocal` | 🧠 COGNITION | 피질 (A1/언어) | 내적발화/락트인 통신 |
| `executive_dlpfc` | 🧠 COGNITION | 피질 (DLPFC) | 집행상태 |
| `audio_io` | 👁️ SENSE | 피질 (A1) | read/write 양방향 |
| `epilepsy` | ⚕️ MED | 피질 focus | 발작 감지(+억제 write) |
| `paralysis_rehab` | ⚕️ MED | 피질 (M1) | 운동복원(read/write) |

→ **read는 전부 피질 ✅** (15/17 응용 앱이 피질). **비침습 심부 read = 공집합** — 깊이 벽(C15·3-shell §확증)이 심부 read를 원천 차단(R²<0.07). write 축은 음향(tFUS)으로 심부 갈래 있음(AURA-WRITE 대조).

- `app/read_depth.py` — read × 깊이 비대칭 실동작 toy
- `verify/read_depth.txt` — verdict

## sibling
- 부모: [AURA](../AURA.md) · 짝 축: AURA-WRITE · 트리: [AURA-TREE.md](../AURA-TREE.md)
