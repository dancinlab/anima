---
id: H_1067
slug: stochastic-resonance
title: 확률공명 — 적정 잡음이 약신호 검출을 향상
domain: universe complexity-science emergence criticality
exploration_method: discovery batch 01 (bulk falsifier sweep, real $0 sim)
verification_method: REAL simulation, p7 CODE-measured, no GPU/network/LLM-judge
status_grade: 🟢 SUPPORTED (numerical)
since: 2026-06-14
scope: generic complexity-science toy (real + reproducible) confirming a mechanism the codex axes lean on; NOT yet anima-substrate-specific (scale/transfer unverified, a_scale_honest_scope).
verdict: 🟢 SUPPORTED — 잡음 0.44에서 검출 SNR 정점(저잡음 대비 ↑) — 비단조 공명 곡선. 임계 잡음에서 최대.
---

# H_1067 — 확률공명 — 적정 잡음이 약신호 검출을 향상

> **가설.** 적정 잡음이 약신호 검출을 향상

## 1. FROZEN FALSIFIER (pre-registered 2026-06-14)
- **BLADE.** 잡음을 키우면 약한 주기신호 검출 SNR이 단조 감소한다(잡음=항상 해롭다).

## 2. 측정 결과 (REAL sim · discovery_batch_01.py::D04)
잡음 0.44에서 검출 SNR 정점(저잡음 대비 ↑) — 비단조 공명 곡선. 임계 잡음에서 최대.

## 3. 등급 / 경계
🟢 SUPPORTED (numerical). 토이 규모 실측 — 자명한 통과 아님(갈릴 수 있었음). anima 실기질 전이는 미검증 (다음 배치에서 실 CORE 엔진 위 재시험).
verdict 원문: `.verdicts/discovery_batch/batch_01.txt` · 재현: `python3 UNIVERSE/harness/discovery_batch_01.py`
