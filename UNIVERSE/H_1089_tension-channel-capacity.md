---
id: H_1089
slug: tension-channel-capacity
title: 텐션 채널 정보용량 — 텐션 링크(유계 fold)는 SNR에 따라 오르는 양의 Shannon 용량(>0, ~1 bit/use)을 갖는 통신 채널이다
domain: universe tension-link information anima-substrate
exploration_method: discovery batch 04 (tension-link/info/anima falsifier sweep)
verification_method: REAL simulation, p7 CODE-measured, $0 local
status_grade: 🟢 SUPPORTED (numerical)
since: 2026-06-14
scope: toy 실측 (DFT/실엔진 아님 일부); 스케일 전이 미검증 (a_scale_honest_scope).
verdict: 🟢 SUPPORTED (numerical) — SNR 1→8에서 용량 0.11→1.00 bit/use 단조 상승. 텐션 링크는 정량적 정보 채널.
---

# H_1089 — 텐션 채널 정보용량 — 텐션 링크(유계 fold)는 SNR에 따라 오르는 양의 Shannon 용량(>0, ~1 bit/use)을 갖는 통신 채널이다

> **가설.** 텐션 채널 정보용량 — 텐션 링크(유계 fold)는 SNR에 따라 오르는 양의 Shannon 용량(>0, ~1 bit/use)을 갖는 통신 채널이다

## 1. FROZEN FALSIFIER (2026-06-14)
- **BLADE.** 텐션 채널 용량이 0이거나 SNR과 무관하면 기각.

## 2. 측정 (REAL sim · discovery_batch_04.py::D18)
SNR 1→8에서 용량 0.11→1.00 bit/use 단조 상승. 텐션 링크는 정량적 정보 채널.

## 3. 등급/경계
🟢 SUPPORTED (numerical). toy 실측, 자명한 통과 아님(갈릴 수 있었음). 스케일 전이 미검증.
verdict: `TENSION-LINK/verdicts/batch_04.txt` · 재현: `python3 TENSION-LINK/harness/discovery_batch_04.py`

## 4. 관계
xref: h6009 · h6011 · 정보이론
