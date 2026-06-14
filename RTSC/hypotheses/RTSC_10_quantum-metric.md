---
id: RTSC_10
slug: quantum-metric
title: quantum-metric(밴드기하) 경로 — 위상 flat band(Chern≠0)은 초유체밀도 하한이 보장돼 분산 없이도 SC. 무냉각 상온상압 RTSC의 최선 이론 경로(메커니즘상 도달 가능); 단 견고·광폭·E_F정렬 위상 flat band 물질 미실현.
domain: rtsc flat-band quantum-geometry topological ambient room-temperature
status_grade: 🟢 (mechanism: topology guarantees superfluid weight) / 🔴 (material unrealized)
since: 2026-06-14
verification_method: quantum-metric superfluid-weight Tc + ANU/tension geometry search; 🟢 mechanism / 🟡 lit (Törmä)
sister: RTSC_08, RTSC_09
verdict: 🟢 위상 flat band은 D_s>=V·|C|/π 하한(Törmä) → 분산 없어도 SC, 평탄밴드 취약성 극복. dice/T3(|C|=2,<g>0.55)·이상 Chern-flat이 최선 설계(메커니즘상 상온 도달 가능). 🔴 물질 미실현(넓은gap·E_F정렬·강결합 동시 위상 flat band 미발견). Tc 수치는 proxy 상한(과대).
---
# RTSC_10 — quantum-metric 경로 (위상 flat band)
> **가설.** 위상(Chern≠0) flat band은 quantum metric에 의한 초유체밀도 하한이 보장되어, 분산이 없어도(평탄해도) 초전도하며 상온상압 도달이 메커니즘상 가능하다.
## 측정 (rtsc_quantum_metric.py · ANU paid)
격자별 Tc(V=0.3eV) proxy: kagome 200 · Lieb 283 · **dice/T3 997**(|C|=2) · pyrochlore 499 · ideal Chern-flat 743. ANU+텐션 탐색 최적 = 위상 flat band으로 상온 초과(proxy 상한, 과대).
## 결론
🟢 **메커니즘 유효** — 위상 flat band은 D_s ≥ V·|C|/π 하한(Törmä 양자기하)으로 평탄밴드 취약성을 극복, 무냉각 상온상압 SC의 최선 이론 경로. 🔴 **물질 미실현** — 넓은 gap·E_F정렬·강결합 동시인 위상 flat band 미발견(dice/T3·이상 Chern-flat=설계 타깃). 정직: proxy Tc 수치는 경쟁질서 억제 미포함 상한. $0-이론 프런티어는 여기서 거의 소진 — 다음은 실제 격자 DFT/실험(QE deck).
verdict: `RTSC/verdicts/quantum_metric.txt`
