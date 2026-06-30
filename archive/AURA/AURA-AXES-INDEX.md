# 📐 AURA 축 횡단 인덱스 — 앱 × 방향 × 깊이 × 모달 (one-page matrix)

> AURA 트리 v2의 3 축(📖 READ · ✍️ WRITE · 📏 DEPTH)을 한 장에 교차. 응용 4 도메인(👁️ SENSE · 🦾 MOTOR · 🧠 COGNITION · ⚕️ MED)의 모든 실동작 앱을 **(방향 read/write × 깊이 피질/심부 × 모달)** 좌표로 위치짓는 SSOT. 각 축 도메인의 "횡단 인덱스" 마일스톤이 이 표를 가리킨다. 🟡 toy(앱은 toy 실동작, 분류는 정성).

## 1. 응용 앱 전수 매트릭스 (17 앱)

| 앱 | 도메인 | 방향 | 깊이 | 모달(자극/센서) | 비침습 도달 | 비고 |
|---|---|---|---|---|---|---|
| `ar_nav` | 👁️ SENSE | ✍️ write | 피질 (V1) | 시각 디스플레이(외부) | ✅ | AR 턴화살표 — 뇌 직접 write 아닌 감각 채널 |
| `ar_display` | 👁️ SENSE | ✍️ write | 피질 (V1) | 시각 디스플레이(외부) | ✅ | AR 디스플레이 |
| `audio_io` | 👁️ SENSE | 📖+✍️ read/write | 피질 (A1) | 음향(외부 청각) | ✅ | 오디오 입출력 |
| `haptics` | 👁️ SENSE | ✍️ write | 피질 (S1) | 촉각(e-skin) | ✅ | 햅틱 피드백 |
| `notify` | 👁️ SENSE | ✍️ write | 피질 (S1/A1) | 촉각/음향 | ✅ | 알림 |
| `motor_decode` | 🦾 MOTOR | 📖 read | 피질 (M1, d1.0) | 전기(EEG) | ✅ | 운동의도 5-class — 최고 도달 |
| `exoskeleton` | 🦾 MOTOR | 📖+✍️ read/write | 피질 (M1+S1) | 전기 + 고유감각 | ✅ | 외골격/의수 폐루프 |
| `cursor` | 🦾 MOTOR | 📖 read | 피질 (M1) | 전기(EEG) | ✅ | 커서/포인터 |
| `consciousness_monitor` | 🧠 COGNITION | 📖 read | 피질 (전역) | 전기(EEG big-Φ/α) | ✅ | 의식수준 모니터 |
| `subvocal` | 🧠 COGNITION | 📖 read | 피질 (A1/언어) | 전기(EEG) | ✅ | 내적발화/통신(락트인) |
| `executive_dlpfc` | 🧠 COGNITION | 📖 read | 피질 (DLPFC, A3 golden) | 전기(EEG) | ✅ | 주의·작업기억·집행상태 |
| `epilepsy` | ⚕️ MED | 📖+✍️ read/write | 피질 focus | 전기(감지+억제) | ✅(피질 focus) | 발작 감지/억제 (R²=0.203) |
| `paralysis_rehab` | ⚕️ MED | 📖+✍️ read/write | 피질 (M1) | 전기 | ✅ | 마비 운동복원 (R²=0.428) |
| `blindness` | ⚕️ MED | ✍️ write | 피질 (V1) | 전기(시각피질 write) | ✅ | 실명 복원 (R²=0.393) |
| `chronic_pain` | ⚕️ MED | ✍️ write | 피질→심부 (S1/대상) | 전기 | 🟡 부분(sulcal) | 만성통증 modulate (R²=0.114) |
| `depression` | ⚕️ MED | ✍️ write | 🔴 심부 (raphe 5HT) | 전기(DBS) | 🔴 침습 | 우울 (R²=0.076) — 비침습 벽 |
| `parkinson` | ⚕️ MED | ✍️ write | 🔴 심부 (STN) | 전기(STN-DBS) | 🔴 침습 | 파킨슨 (R²=0.092) — 비침습 벽 |

## 2. 방향 × 깊이 2×2 좌표 (응용 앱 배치)

```
              📖 READ                          ✍️ WRITE
        ┌──────────────────────────┬──────────────────────────────┐
  피질  │ motor_decode · cursor     │ ar_nav · ar_display · haptics │
  ✅    │ consciousness_monitor     │ notify · blindness            │
        │ subvocal · executive_dlpfc│ + read/write: audio_io ·      │
        │ + read/write: exoskeleton ·  epilepsy · paralysis_rehab   │
        │   audio_io · epilepsy ·   │   exoskeleton                 │
        │   paralysis_rehab         │                               │
        ├────────────── 📏 깊이 벽 (C15·3-shell 확증) ──────────────┤
  심부  │ (없음 — 비침습 read 불가) │ chronic_pain(부분 sulcal)     │
  🔴    │                           │ depression(raphe)·parkinson(STN)│
        │                           │ ← 전부 침습(DBS) 또는 tFUS만   │
        └──────────────────────────┴──────────────────────────────┘
```

- **피질 사분면(✅)**: 15/17 앱. 비침습 실현권 — SENSE·MOTOR·COGNITION 전부 + MED 피질질환(간질·마비·실명).
- **심부 read(공집합)**: 비침습 심부 *읽기*는 앱이 없음 — C15/3-shell 깊이 벽이 read를 원천 차단(R²<0.07).
- **심부 write(🔴)**: depression·parkinson = 심부 신경조절핵 *쓰기*. 전기로는 전부 침습(DBS); 비침습 갈래는 음향(tFUS)만 — write가 read를 d2.5+서 추월(AURA-WRITE).

## 3. 모달리티 × 깊이 (HOW 도메인 결합)

| 모달 | HOW 도메인 | 피질 read | 심부 read | 피질 write | 심부 write |
|---|---|---|---|---|---|
| 전기(EEG/ECoG) | — | ✅ | 🔴 (LPF 붕괴) | ✅ | 🔴 침습(DBS) |
| 자기(MEG·상온초전도) | 🧲 RTSC-MEG | ✅ 표면 최강 | 🔴 1/r² 역전 | — | — |
| 혈관내(Stentrode) | 🩸 ENDOVASC | ✅ 정맥동 근접 | 🟡 정맥 경로 한정 | — | — |
| 음향(focused US) | 🔊 TFUS | 🔴 (성인 read 미성숙) | 🔴 read | ✅ | ✅ **유일 비침습 심부 write** |
| 검증 인프라 | 🗺️ HEADMODEL | (3-shell lead-field 검증자) | | | |

→ 심부 칸은 **음향 write 1개를 빼면 전부 🔴** — 깊이 벽이 모달 무관 실재(§4).

## 4. 축 도메인 앱(분류기 자체) — 응용 아닌 축 toy

| 앱 | 축 도메인 | 역할 |
|---|---|---|
| `read_depth.py` | 📖 READ | read × 깊이 비대칭 toy (피질 0.79 / 심부 0.06) |
| `write_depth.py` | ✍️ WRITE | write × 깊이 비대칭 toy (음향이 d2.5+서 read 추월) |
| `depth_envelope.py` | 📏 DEPTH | 가우시안 깊이 포락선 toy |
| `sphere_depth_envelope.hexa` | 📏 DEPTH | 3-shell(Ary1981) 깊이 envelope 재계산 — §5 핵심 |

## 5. 3-shell 검증 결과가 이 매트릭스에 거는 것

§2의 "📏 깊이 벽" 가로선은 **가우시안 커널 인공물이 아니라 실재 물리 경계**임이 3-shell(Ary 1981) 재계산으로 확증됐다(부호 반전: 3-shell 감쇠 ×15.4 > 가우시안 ×8.4). → 심부 사분면이 🔴인 것은 toy 가정이 만든 게 아니라 두피-전극 물리(radial dipole g_n∝b^(2n) 소멸)의 귀결. 상세 = [DEPTH-3SHELL-CORRECTION](AURA-DEPTH/DEPTH-3SHELL-CORRECTION.md) · [AURA §3-shell 검증 결과](AURA.md).

## sibling
- 부모: [AURA](AURA.md) · 트리: [AURA-TREE.md](AURA-TREE.md) · 축: [READ](AURA-READ/AURA-READ.md)·[WRITE](AURA-WRITE/AURA-WRITE.md)·[DEPTH](AURA-DEPTH/AURA-DEPTH.md)
