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
- 📐 **앱 × 방향 × 깊이 × 모달 one-page 매트릭스** = [AURA-AXES-INDEX.md](AURA-AXES-INDEX.md) (17 응용 앱 전수 분류 SSOT).

## 3-shell 검증 결과 — 📏 깊이 벽은 실재 물리경계 (가우시안 인공물 아님)

위 좌표계의 "📏 깊이 벽" 가로선이 **toy 가우시안 커널 인공물인지 실재 물리경계인지**를 3-shell(Ary 1981 radial-dipole) 물리로 결판냈다. 결과: **실재 물리경계 — 가우시안은 오히려 벽을 *과소평가*했다.**

| 모델 | cortex→deep 감쇠 배율 | 판정 |
|---|---|---|
| **3-shell (물리)** | **×15.4** (R² 0.239→0.016) | 더 가파름 = 벽 실재 |
| 가우시안 (C15 published) | ×8.4 (0.82→0.10) | — |

- 🧱 **C15 "가우시안 깊이벽" → 정정**: 깊이 벽은 가우시안 인공물이 아니라 **3-shell로 확증된 실재 물리경계**다(radial dipole g_n∝b^(2n), b→0서 두피 흔적 소멸). 가우시안 toy는 벽을 과장한 게 아니라 **오히려 과소평가**했다. 상세 = [DEPTH-3SHELL-CORRECTION](AURA-DEPTH/DEPTH-3SHELL-CORRECTION.md).
- ✅ **C16/C17 결론 강화됨**: 피질 비침습 도달 ✅(C16) / 심부핵 비침습 불가 = 침습 필요 🔴(C17) — 두 결론 모두 물리 모델로 **약화가 아니라 강화**. 심부<피질 방향은 가우시안·3-shell 두 모델에서 robust.
- ⚠ **전극포화는 여전히 가우시안 인공물**: 깊이 벽과 달리 C10 "전극포화=가우시안 인공물"은 3-shell서 *재확증*(3-shell 미포화, 전극 증설 계속 이득) — 깊이 벽(실재)과 전극포화(인공물)는 별개 결론.
- 📝 이력 각주: PR#1514(HEADMODEL)는 잠정적으로 "가우시안이 깊이 벽 ×8을 과장(3-shell ×1.5)"이라 보고했으나, 이는 **얕은-창 인공물**(소스 반경 b 0.85~1.0·r1 = 전부 피질)이었음이 PR#1517(DEPTH 전구간 재계산)에서 밝혀져 부호 반전 정정됨 — 트리는 **최신 PR#1517 결론(과소평가)만 반영**.

## sibling
- 부모: [AURA](AURA.md) · 출처: `AURA/archive/`(demiurge σ=12 zone·brainwire·C5~C17)
