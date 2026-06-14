---
id: RTSC_11
slug: lieb-real-calc
title: flat-band SC 실격자 검증 — Lieb 평탄밴드 quantum metric을 Bloch 상태서 정확 계산(<tr g>=0.60, 밴드폭 0). D_s>0로 분산 없이도 SC 실증(메커니즘 REAL). 단 현실 U(0.3-1eV)서 Tc~33-109K(큐프레이트 범위, 상온 아님) — RTSC_10 proxy 과대 정정.
domain: rtsc flat-band quantum-geometry exact-calc ambient
status_grade: 🟢 (mechanism verified by exact calc) / 🔴 (room-temp NOT reached at realistic U)
since: 2026-06-14
verification_method: exact tight-binding Bloch quantum metric + Törmä–Peotta D_s + BKT Tc; numpy ED; p7 $0
sister: RTSC_09, RTSC_10
verdict: 🟢 Lieb flat band <tr g>=0.601(밴드폭 0) → D_s>0(분산 없이 SC 실증, quantum-geometry SC REAL). 🔴 그러나 현실 U=0.3/0.5/1.0eV → Tc 33/54/109K(큐프레이트 범위, 상온 미달). RTSC_10 proxy(1995K) 과대 → 정직 하향. 무냉각 상온은 이 경로로도 미달.
---
# RTSC_11 — flat-band SC 실격자 검증 (Lieb quantum metric)
> **검증.** RTSC_10의 위상/평탄밴드 메커니즘을 proxy 아닌 실제 격자 계산으로.
## 측정 (rtsc_lieb_quantum_metric.py · numpy 정확대각화)
Lieb 3-band, 평탄밴드 폭=0.00(정확), Bloch 상태서 quantum metric <tr g>=0.601. 초유체밀도 D_s=U·n(1-n)·<g>/2π → U=0.3eV:D_s 0.0072eV Tc33K · U=0.5:54K · U=1.0:109K.
## 결론
🟢 **메커니즘 REAL 검증** — 분산 0(완전 평탄)인데도 quantum metric이 유한해 D_s>0 = 초전도 가능(Törmä quantum-geometry SC, 실격자 확인). 🔴 **그러나 현실 상호작용서 Tc~33-109K(큐프레이트 범위), 상온 미달** — RTSC_10의 proxy 1995K는 과대였음(정직 정정). 무냉각 상온상압은 이 최선 경로로도 $0 파라미터선 미달.
verdict: `RTSC/verdicts/lieb_quantum_metric.txt`
