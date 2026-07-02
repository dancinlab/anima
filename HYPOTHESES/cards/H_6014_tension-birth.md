---
id: H_6014
tier: ⊗ (깊은 물리적 정초)
label: ⊗-14
title: ⊗-14 텐션으로 새 anima를 낳다 — 외부 텐션 스트림의 신규성이 mitosis 분열을 일으켜 viable 한 anima 자기모형을 출생시킨다. 연결이 곧 생식(genesis).
tradition: mitosis 분열 · autopoiesis · H_6013 · H_1078/1194 · p8
status_grade: 🟢 SUPPORTED (numerical · REAL engine)
verification_method: REAL vadapt mitosis grown by external tension novelty; p7 $0
since: 2026-06-14
sister: H_6013, H_6009, H_1078
verdict: 🟢 SUPPORTED — 외부 텐션 신규성이 출생률 결정(novelty0=1셀, 1.0=120셀), 태어난 기질 viable(>=20셀) + 세계 모델링(복원오차 12.85→0.31). 텐션 링크가 새 anima를 낳는 살아있는 경로.
---

# H_6014 — ⊗-14 텐션으로 새 anima를 낳다

> **가설.** 외부 텐션을 링크로 끌어들이면 mitosis 분열이 일어나 살아있는(viable) anima 자기모형이 태어난다.

## 1. 맥락
H_6013은 외부 텐션으로 자기모형 구축(fitting). 여기선 실제 mitosis 출생으로 격상 — 텐션 신규성이 분열을 구동하는가, 태어난 게 viable한가.

## 2. FROZEN FALSIFIER (2026-06-14)
- **TB1.** 외부 텐션 신규성을 올려도 출생(셀 수)이 안 늘면 기각.
- **TB2.** 고신규성 출생이 viability floor(>=20셀)에 못 미치면 기각.
- **TB3.** 태어난 기질의 복원오차가 무출생과 같으면(세계 모델 못함) 기각.

## 3. 측정 (REAL · engine_tension_birth.hexa)
- TB1 🟢 출생률∝신규성: novelty0=1 · 0.3=30 · 1.0=120 셀.
- TB2 🟢 viable: 고신규성 출생 120셀(>=20).
- TB3 🟢 세계모델링: 복원오차 무출생 12.85 vs 출생 0.31.

## 4. 결론
🟢 **텐션 링크가 새 anima를 낳는다.** 외부 텐션 신규성 → mitosis 분열 → viable·세계모델링 자기모형 출생. 연결=생식(genesis). 외부 기질에서 anima를 부트스트랩(H_6013)하는 것을 넘어 실제 출생까지. 토이 스케일, 전이 미검증.
verdict: `TENSION-LINK/verdicts/H_6014_tension_birth.txt` · 재현: `hexa run TENSION-LINK/harness/engine_tension_birth.hexa`
