---
id: RTSC_04
slug: confirmable-search
title: 양자+텐션링크로 '확정가능' RTSC 찾아오기 — confirmability(=Tc·저압보상) 최적화는 저압 합성가능 후보(~121K@73GPa, LaBH8급)를 찾아오나, P↔Tc 트레이드오프로 상온은 못 잡는다.
domain: rtsc materials superconductivity quantum-search synthesizability
exploration_method: ANU paid QRNG + tension-link optimizer over (composition,pressure), confirmability objective
verification_method: ANU-driven annealing on Allen-Dynes+stability landscape; p7 $0; NOT DFT
status_grade: 🟡 (확정가능 sub-RT 후보) / 🔴 (확정가능 상온은 트레이드오프로 불가)
since: 2026-06-14
sister: RTSC_01, RTSC_02, RTSC_03; xref UNIVERSE/H_6015, H_6016, H_6017
verdict: 양자+텐션 confirmability 최적화가 저압 후보 Tc≈121K@73GPa(stability 0.84) 찾아옴 — 확정 유리하나 sub-RT. P↔Tc 트레이드오프(저압→Tc↓, 상온→고압)는 못 깸. DB read 아닌 ANU구동 최적화(H_6016/17).
---

# RTSC_04 — 양자+텐션링크로 '확정가능' RTSC 찾아오기

> **가설.** 양자(ANU)+텐션링크 옵티마이저로 합성가능(저압·안정) RTSC를 찾아올 수 있는가.

## 1. 방법
ANU paid QRNG = 탐색 무작위, 텐션링크 수렴 = 옵티마이저, 목적함수 = confirmability = Tc·exp(−P/120) (저압 보상) over (H분율·강성·DOS·압력), 안정성 P_min 게이트.

## 2. 측정 (RTSC/harness/rtsc_confirmable_search.py · ANU sha 2592b58118f6)
찾아온 후보: H분율 0.00·강성 1.00·DOS 1.00 → λ=1.70 ω_log=820K **P=73 GPa** stability 0.84 → **Tc≈121K(−152°C)**. 🟡 sub-RT @ 저압(확정 유리).

## 3. 결론
양자+텐션이 **확정가능 최적점(저압 ~121K)** 을 찾아온다 — LaBH8급 저압 루트와 정합. 그러나 **P↔Tc 트레이드오프**(저압이면 안정성 부족→Tc↓, 상온이면 고압 필요)를 물리적으로 못 깬다 → **확정가능+상온 동시 달성은 불가(🔴)**, RTSC_03과 정합. '찾아오기'는 DB read(H_6017 🔴)가 아니라 ANU구동 최적화(H_6016). 다음: 찾아온 저압 후보를 QE deck ab-initio 확정.
verdict: `RTSC/verdicts/confirmable_search.txt` · 재현: ANU prep 후 `python3 RTSC/harness/rtsc_confirmable_search.py`
