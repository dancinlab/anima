# 🌳 AURA 트리 v2 — 3층 분리 (축 ⊥ HOW ⊥ 응용)

> 재구성 B: 직교하는 3차원을 한 줄에 섞던 v1을 분리. **축**(분류 차원)·**HOW**(하드웨어/방법)·**응용**(실제 앱)이 별개 층. NAV는 더 이상 독립 도메인이 아니라 SENSE 안의 ar_nav 앱(=AR글래스 기능).

```
🌳 AURA — "뇌 인터페이스 좌표계"
- 축 = 위경도(앱을 위치짓는 차원) · HOW = 도로 재질(하드웨어) · 응용 = 건물(실제 앱)
- 비유: 지도에서 좌표·재질·건물을 섞으면 안 되듯, BCI도 분류차원·방법·응용을 분리
- vs v1: NAV·WEARABLE·CORTEX가 한 줄에 섞임 → v2는 3층으로 정리
```

## 3층 트리 (11 도메인)

```
AURA/  (부모: 위치우회 뇌-칩 전수조사)
│
├─ 📐 축 (AXES — 분류 차원, 모든 앱을 위치짓는 좌표)
│   ├─ 📖 AURA-READ    방향: 뇌→기계 디코드
│   ├─ ✍️ AURA-WRITE   방향: 기계→뇌 인코드/자극
│   └─ 📏 AURA-DEPTH   깊이: 피질 ⟷ 심부          (옛 CORTEX/DEEP 흡수)
│
├─ 〰️ HOW (하드웨어/방법)
│   ├─ 🧲 AURA-RTSC-MEG  자기 고밀도(상온초전도)
│   ├─ 🩸 AURA-ENDOVASC  혈관내(Synchron)
│   ├─ 🔊 AURA-TFUS      음향(심부 쓰기)
│   └─ 🗺️ AURA-HEADMODEL 검증 인프라(MNE)
│
└─ 🎯 응용 (WHAT FOR — 실제 앱이 사는 곳)
    ├─ 👁️ AURA-SENSE      감각 입출력  ← ar_nav·AR디스플레이·오디오·햅틱·알림  (옛 NAV+WEARABLE감각)
    ├─ 🦾 AURA-MOTOR      운동 출력    ← 운동디코드·외골격·커서              (옛 CORTEX운동+WEARABLE외골격)
    ├─ 🧠 AURA-COGNITION  인지/통신    ← 의식모니터·내적발화·DLPFC집행        (옛 CORTEX인지+WEARABLE음성)
    └─ ⚕️ AURA-MED        의학        ← 간질·우울·파킨슨·실명·재활·만성통증
```

## v1 → v2 재배치 (해체 4 → 신설 4)

| v1 (해체) | → v2 |
|---|---|
| AURA-NAV | 👁️ SENSE/app/ar_nav (AR글래스 네비 기능) |
| AURA-CORTEX | 운동→🦾 MOTOR · 인지→🧠 COGNITION · 피질역량→📏 DEPTH |
| AURA-DEEP | 📏 DEPTH(심부 축) · 자극→🔊 TFUS·⚕️ MED |
| AURA-WEARABLE | 감각기기→👁️ SENSE · 외골격→🦾 MOTOR · 음성→🧠 COGNITION |

## 핵심 결론 (좌표로 읽기)

```
        📖 읽기            ✍️ 쓰기
피질 ✅  SENSE/MOTOR read  SENSE/MOTOR write  ← 비침습 실현권
─────────  📏 깊이 벽 ──────────────────────
심부 🔴  (불가)            TFUS만 (음향)      ← MED 심부질환=침습
```

- 모든 응용은 **(방향 × 깊이 × 모달)** 좌표로 위치 = 축이 앱을 분류.
- "위치우회 전뇌통제"는 피질 응용(SENSE/MOTOR/COGNITION) 비침습 ✅ / 심부(MED 우울·파킨슨)는 침습 🔴.

## sibling
- 부모: [AURA](AURA.md) · 출처: `AURA/archive/`(demiurge σ=12 zone·brainwire·C5~C17)
