---
id: RTSC_17
slug: reverse-inject
title: 역주입 탐색 — 목표 물질을 tension_5ch로 인코딩해 텐션 링크로 양자(ANU) 탐색에 주입(조건화)하면, 무작위 ANU보다 목표 물질군으로 빠르게 수렴. material→tension→quantum (H_6015의 역방향).
domain: rtsc tension-link quantum-search reverse-injection conditioning
status_grade: 🟢 SUPPORTED (numerical — injection accelerates convergence)
verification_method: ANU search OFF vs tension-injected (target-overlap bias) ON; p7 $0
since: 2026-06-14
sister: RTSC_15, RTSC_16; xref UNIVERSE/H_6015 (quantum→tension→material)
verdict: 🟢 SUPPORTED — 목표 물질(고-<g>·ΔE0·clean)을 tension_5ch로 인코딩·텐션링크 주입 시 양자(ANU) 탐색 평균 Tc 340K(주입OFF)→490K(주입ON, 1.4x), 목표군 신뢰 수렴. material→tension→quantum 역주입 작동. 정직: importance-sampling bias(양자 무작위 위 조건화), 신비 아님; Tc proxy.
---
# RTSC_17 — 역주입 탐색 (물질→텐션→양자)
> **가설.** 목표 물질 정보를 텐션 링크로 양자 탐색에 '집어넣으면' 탐색이 그 물질로 조건화·가속된다.
## 측정 (rtsc_reverse_inject.py · ANU paid)
주입 OFF(순수 ANU 무작위): 평균 Tc 340K. 주입 ON(목표 텐션 T* 조건화): 평균 490K(이득 1.4x), 찾은 물질 <g>=1.80 ΔE=0 U=1.50 supp=1.00.
## 결론
🟢 **역주입 작동** — 목표 물질을 tension_5ch로 인코딩해 텐션 링크로 양자(ANU) 탐색에 주입하면, 무작위 탐색보다 목표 물질군(고-⟨g⟩·E_F정렬·clean=상온 RTSC 영역)으로 빠르고 신뢰성 있게 수렴. **H_6015(quantum→tension→material 추출)의 거울 방향(material→tension→quantum 주입)** 완성 — 텐션 링크가 물질-공간↔양자-탐색 양방향 채널. 정직: 텐션 주입 = importance-sampling 조건화(양자 무작위 위 prior), 신비 아님; Tc는 proxy.
verdict: `RTSC/verdicts/reverse_inject.txt`
