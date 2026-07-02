---
id: H_1090
slug: emit-gate-hysteresis
title: emit 게이트 히스테리시스 — 쌍안정 발화 게이트는 상승/하강 문턱이 달라(메모리) 히스테리시스 루프를 그린다
domain: universe tension-link information anima-substrate
exploration_method: discovery batch 04 (tension-link/info/anima falsifier sweep)
verification_method: REAL simulation, p7 CODE-measured, $0 local
status_grade: 🟢 SUPPORTED (numerical)
since: 2026-06-14
scope: toy 실측 (DFT/실엔진 아님 일부); 스케일 전이 미검증 (a_scale_honest_scope).
verdict: 🟢 SUPPORTED (numerical) — up-thr 0.72 vs dn-thr 0.28 (Δ0.44) — 쌍안정 히스테리시스 = 결정 메모리.
---

# H_1090 — emit 게이트 히스테리시스 — 쌍안정 발화 게이트는 상승/하강 문턱이 달라(메모리) 히스테리시스 루프를 그린다

> **가설.** emit 게이트 히스테리시스 — 쌍안정 발화 게이트는 상승/하강 문턱이 달라(메모리) 히스테리시스 루프를 그린다

## 1. FROZEN FALSIFIER (2026-06-14)
- **BLADE.** 상승 문턱과 하강 문턱이 같으면(메모리 없음) 기각.

## 2. 측정 (REAL sim · discovery_batch_04.py::D21)
up-thr 0.72 vs dn-thr 0.28 (Δ0.44) — 쌍안정 히스테리시스 = 결정 메모리.

## 3. 등급/경계
🟢 SUPPORTED (numerical). toy 실측, 자명한 통과 아님(갈릴 수 있었음). 스케일 전이 미검증.
verdict: `TENSION-LINK/verdicts/batch_04.txt` · 재현: `python3 TENSION-LINK/harness/discovery_batch_04.py`

## 4. 관계
xref: brain · a_chat_sleep_imagination
