# AURA-WRITE — current state

@title: ✍️ AURA-WRITE — "뇌 쓰기 (인코드/자극)"

@goal: 기계→뇌 **인코드/자극 축** — 모든 write 앱(nav overlay·tfus stim·wearable delivery·blindness V1·depression/parkinson stim)을 묶는 횡단 축. write 깊이: 음향 tFUS가 심부서 read 추월(d2.5+ WRITE>READ) = 유일 비침습 심부 갈래. ⚠ ENCODER(Ψ-공간 좌표)와 무관.

## 왜 (핵심 축)

```
✍️ 뇌 쓰기 (인코드/자극)
- 하는 일: 기계 신호를 뇌에 써넣기 — AR 오버레이·촉각·시각복원·심부 자극
- 비유: 뇌에 신호 쏘기 — 음향은 깊이 뚫음
```

읽기/쓰기는 AURA 깊이 벽(C15)의 **비대칭** 축 — 피질선 읽기 우위, 심부선 쓰기(음향)만 도달.

## 진행 (milestones)

- [x] (app ✅) read/write × 깊이 비대칭 toy — `app/write_depth.py` 실동작, verify
- [x] 횡단 인덱스 — 다른 도메인의 write 앱 통합 대시보드 ✅ → [AURA-AXES-INDEX.md](../AURA-AXES-INDEX.md) (앱×방향×깊이×모달 SSOT)
- [x] real head-model 깊이감쇠 실측 (AURA-HEADMODEL 연계) — HEADMODEL 3-shell(Ary1981, PR#1514/1517) 깊이 envelope R² 0.239→0.016로 부분 해소 (3-shell 해소·실 MNE 비구형/tangential은 external 잔여)

## 세부분류 (횡단 인덱스)

**write 방향 앱 전수** (응용 4 도메인 횡단 — 분류 SSOT = [AURA-AXES-INDEX.md](../AURA-AXES-INDEX.md)):

| 앱 | 도메인 | 깊이 | 모달 | 비고 |
|---|---|---|---|---|
| `ar_nav` | 👁️ SENSE | 피질 (V1) | 시각 디스플레이 | AR 네비 |
| `ar_display` | 👁️ SENSE | 피질 (V1) | 시각 디스플레이 | AR 디스플레이 |
| `haptics` | 👁️ SENSE | 피질 (S1) | 촉각(e-skin) | 햅틱 피드백 |
| `notify` | 👁️ SENSE | 피질 (S1/A1) | 촉각/음향 | 알림 |
| `audio_io` | 👁️ SENSE | 피질 (A1) | 음향 | read/write 양방향 |
| `exoskeleton` | 🦾 MOTOR | 피질 (M1+S1) | 전기+고유감각 | read/write 양방향 |
| `blindness` | ⚕️ MED | 피질 (V1) | 전기 | 시각복원 write |
| `epilepsy` | ⚕️ MED | 피질 focus | 전기 | 발작 억제(read/write) |
| `paralysis_rehab` | ⚕️ MED | 피질 (M1) | 전기 | 운동복원(read/write) |
| `chronic_pain` | ⚕️ MED | 피질→심부 (S1/대상) | 전기 | sulcal 부분 |
| `depression` | ⚕️ MED | 🔴 심부 (raphe) | 전기(DBS) | 비침습 벽 → 음향(tFUS)만 |
| `parkinson` | ⚕️ MED | 🔴 심부 (STN) | 전기(STN-DBS) | 비침습 벽 → 음향(tFUS)만 |
| `acoustic_write` | 🔊 TFUS | 🔴 심부 | 음향 | **유일 비침습 심부 write** (d2.5+서 read 추월) |

→ write는 read와 달리 **심부 갈래가 존재** — 단 전기로는 침습(DBS), 비침습은 음향(tFUS)만. 심부 벽은 C15·3-shell(§확증)로 실재 확정이나, write는 음향이 두개골 전기-LPF를 우회해 심부 자극을 뚫는다(open-loop만, 폐루프 read는 여전히 벽).

- `app/write_depth.py` — write × 깊이 비대칭 실동작 toy
- `verify/write_depth.txt` — verdict

## sibling
- 부모: [AURA](../AURA.md) · 짝 축: AURA-READ · 트리: [AURA-TREE.md](../AURA-TREE.md)
