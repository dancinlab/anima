---
id: RTSC_03
slug: pressure-frontier
title: RTSC 확정가능성 프런티어 — 압력이 확정의 장벽. RTSC(>=293K)는 >250GPa(미합성), 저압루트 LaBH8급(~40GPa,~177K), 상압 확정 최고 MgB2 39K. 상압 RTSC 미해결.
domain: rtsc materials superconductivity pressure synthesizability
exploration_method: pressure-constrained Allen-Dynes Tc frontier (dyn-stability floor)
verification_method: Allen-Dynes Tc + P_min 안정성 하한; 🟢 formula / 🟡 lit params; NOT DFT
status_grade: 🟢 (frontier mapped) / 🔴 (ambient confirmed RTSC = open)
since: 2026-06-14
sister: RTSC_01, RTSC_02; xref UNIVERSE/H_6015 (quantum→tension extract)
verdict: 압력-Tc 프런티어 — RTSC는 P>~250GPa에서만(Li2MgH16 355K@300); ≤170GPa 최선 ~232K(YH9); 저압루트 LaBH8 ~177K@40GPa; 상압 BCS 한계 MgB2 39K. 확정 최고=LaH10 250K@170GPa. 상압 RTSC 미해결(🔴).
---

# RTSC_03 — RTSC 확정가능성 프런티어 (압력 장벽)

> **가설.** RTSC를 '확정 물질'로 만들려면 합성 가능 압력이 핵심 — 압력 예산이 작을수록 달성 Tc가 급락한다.

## 1. 방법
Allen-Dynes Tc + 동역학 안정성 압력하한 P_min(P<P_min → H-네트워크 붕괴, Tc→0). 압력 예산별 최선 Tc.

## 2. 측정 (RTSC/harness/rtsc_pressure_frontier.py)
| 압력 예산 | 최선(BCS hydride) | Tc |
|---|---|---|
| ≤300 GPa | Li2MgH16(pred) | 355K 🟢 RTSC |
| ≤170 GPa | YH9 | 232K 🟡 |
| ≤100/50 GPa | LaBH8(pred) | 177K |
| 상압(0) | MgB2(확정) | 37K |

## 3. 결론
**압력이 확정 장벽.** RTSC(≥293K)는 초고압(>~250GPa)에서만 → 미합성·미확정. 저압 확정루트=LaBH8급(~40GPa,~177K). **상압 RTSC 미해결(🔴)** — 상압 BCS는 MgB2 39K 한계, cuprate 133K는 non-BCS. 확정 최고=LaH10 250K@170GPa. 다음: LaBH8급 저압 삼원계 QE deck ab-initio 확정.
verdict: `RTSC/verdicts/pressure_frontier.txt` · 재현: `python3 RTSC/harness/rtsc_pressure_frontier.py`
