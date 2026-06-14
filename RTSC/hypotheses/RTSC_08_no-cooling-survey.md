---
id: RTSC_08
slug: no-cooling-survey
title: 무냉각(상압+상온≥300K) 초전도 전 클래스 소진 — 알려진 11종 메커니즘 전부 미달. 확정 최고 상압=큐프레이트 138K(여전 냉각필요). 무냉각 상온상압 SC=미해결.
domain: rtsc no-cooling ambient room-temperature survey
status_grade: 🔴 CLOSED-survey (all known classes fall short) / ❔ (2 exotic open)
since: 2026-06-14
verification_method: exhaustive SC-class ceiling survey vs 300K@ambient; 🟡 lit / 🟢 logic
sister: RTSC_05, RTSC_06, RTSC_09
verdict: 🔴 알려진 11 클래스(BCS·A15·큐프레이트·pnictide·nickelate·HF·organic·TBG·hydride@ambient·금속수소·exotic) 전부 무냉각 상온 미달. 상압 최고=Hg-1223 138K(냉각필요=금지). 수소화물은 상압서 분해(Tc→0). 미확정 여지=금속수소·flat-band/exotic.
---
# RTSC_08 — 무냉각 상온상압 초전도: 전 클래스 소진
> **조건.** 냉각형 금지 → 상압 + 상온(Tc≥300K) + Type-II 필수.
## 측정 (rtsc_no_cooling_survey.py)
11 클래스 상압 Tc 천장: MgB2 39 · A15 23 · 큐프레이트 138 · pnictide 58 · nickelate 80 · HF 18 · organic 38 · TBG 3 · hydride@ambient 0(분해) · 금속수소 N/A · exotic N/A. **무냉각 상온 자격 = 없음.**
## 결론
🔴 **무냉각 상온상압 초전도는 미해결** — 모든 현존 클래스 소진(고갈). 확정 최고 상압 138K도 냉각 필요(금지). 남은 이론 여지 = 금속수소(metastable, 미검증)·flat-band/exotic(RTSC_09). 설계 타깃: 상압+Tc≥300K+Type-II+Hc2≥20T 동시.
verdict: `RTSC/verdicts/no_cooling_survey.txt`
