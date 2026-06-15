---
id: H_1096
slug: info-bottleneck-denoise
title: 정보병목 잡음제거 — 상위 성분만 보존(low-rank)이 신호를 살리고 잡음을 버린다
domain: universe tension-link information criticality self-organization anima-substrate
exploration_method: discovery batch 05 (SOC/info/multi-hop/self-org falsifier sweep)
verification_method: REAL simulation, p7 CODE-measured, $0 local
status_grade: 🟢 SUPPORTED (numerical)
since: 2026-06-14
scope: toy 실측; 스케일 전이 미검증 (a_scale_honest_scope).
verdict: 🟢 SUPPORTED — top-3 재구성 MSE 0.254→0.042 (신호 보존·잡음 제거).
---

# H_1096 — 정보병목 잡음제거 — 상위 성분만 보존(low-rank)이 신호를 살리고 잡음을 버린다

> **가설.** 정보병목 잡음제거 — 상위 성분만 보존(low-rank)이 신호를 살리고 잡음을 버린다

## 1. FROZEN FALSIFIER (2026-06-14)
- **BLADE.** 측정이 예측과 반대/무효면 기각.

## 2. 측정 (REAL sim · discovery_batch_05.py::D28)
top-3 재구성 MSE 0.254→0.042 (신호 보존·잡음 제거).

## 3. 등급/경계
🟢 SUPPORTED (numerical). toy 실측, 갈릴 수 있었음. 스케일 전이 미검증.
verdict: `TENSION-LINK/verdicts/batch_05.txt` · 재현: `python3 TENSION-LINK/harness/discovery_batch_05.py`

## 4. 관계
xref: h1074 predictive-coding · IB
