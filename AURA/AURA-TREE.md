# 🌳 AURA 트리 — 위치 우회 뇌-칩, 어디까지 닿나 (일반인 지도)

> AURA 부모 도메인이 답한 핵심 질문 — "뉴럴링크 칩을 위치만 바꿔 전체 뇌를 통제할 수 있나?" — 의 결론(피질은 비침습 도달 ✅, 심부는 침습 필요 🔴)을 9개 하위 도메인으로 묶은 지도. ANIMA가 채널 트리로 묶듯 `AURA/<NAME>/` 중첩.

```
🌳 AURA — "뇌에 닿는 모든 길"
- 하는 일: 뇌의 어느 부위까지, 어떤 방법으로, 무엇을 위해 닿을 수 있나를 한 지도로
- 비유: 산(뇌)을 오르는 등산 지도 — 어떤 장비(모달)로 어느 고도(깊이)까지, 정상에서 뭘 하나(응용)
- vs 단일 BCI 논문: 한 경로만 / AURA는 장비×고도×목적 전체 지형도
```

## 트리 (4그룹 × 9 하위 도메인)

```
AURA/  (부모: 위치 우회 뇌-칩 전수조사)
│
├─ 📡 모달리티 — 어떻게 닿나 (하드웨어)
│   ├─ AURA-RTSC-MEG   🧲 상온초전도 나노코일 자기 read/write
│   ├─ AURA-ENDOVASC   🩸 Synchron 혈관내 정맥동 (개두술 0)
│   └─ AURA-HEADMODEL  🗺️ 진짜 머리모델 — toy 검증의 ground-truth
│
├─ 🧠 피질 역량 — ✅ 비침습 도달 (reach 0.82~0.91)
│   ├─ AURA-CORTEX     🧠 운동·통신·집행·의식 모니터 I/O
│   └─ AURA-NAV        🧭 시각 네비(V5/V6 AR)·공간 항법
│
├─ 🧬 심부 역량 — 🔴 침습 필요 (전뇌통제 본질)
│   ├─ AURA-DEEP       🧬 보상·각성·기분·의식·기억 신경조절
│   └─ AURA-TFUS       🔊 초음파 — 유일 비침습 심부 *쓰기*
│
└─ 🎯 응용 — 무엇을 위해
    ├─ AURA-WEARABLE   📱 사라지는 기기 (18-wearable → 0)
    └─ AURA-MED        ⚕️ 의학 (간질·우울·파킨슨·재활·실명)
```

## 한눈 요약 (깊이 × 방향)

```
          읽기(decode)              쓰기(stim)
피질 ✅   CORTEX·NAV(V5/V6)         WEARABLE(AR/오디오/햅틱)
─────────  깊이 벽(C15) ───────────────────────────────
심부 🔴   DEEP(침습 필요)           TFUS(유일 비침습 쓰기)
모달 인프라: RTSC-MEG(자기) · ENDOVASC(혈관) · HEADMODEL(검증)
의학 응용:  MED — 위 역량을 질환 치료로 (간질·우울·파킨슨·재활)
```

## 결론 (AURA 부모 도메인 답)

- relocate-N1 "전뇌통제"는 **비침습 불가**(심부 깊이 벽 C15) — 침습 N1/DBS 영역(AURA-DEEP).
- but 비침습이 닿는 **피질 역량은 크다**(AURA-CORTEX/NAV) + 모든 웨어러블 흡수(AURA-WEARABLE) + 의학 응용(AURA-MED).
- 유일 비침습 심부 갈래 = tFUS *자극*(AURA-TFUS, 읽기는 벽).

## sibling
- 부모: [AURA](AURA.md) · 9 하위 도메인: 위 트리 · 출처: `AURA/archive/`(demiurge cortex pillar σ=12 zone · brainwire seizure/medical · C13 RTSC)
