---
id: RTSC_19
slug: ufo-hover
title: UFO = 호버크래프트(초전도 자속고정 부상, 반중력 아님) — 강한 외부 자기장(트랙/자성노면) 위에선 1톤 크래프트도 부상(🟢, maglev·호버보드 대형판); 임의 지면 자유비행은 지구장(5e-5T) 약·균일로 불가(🔴).
domain: rtsc application ufo hovercraft flux-pinning levitation maglev
status_grade: 🟢 (hover over a strong-field track/surface) / 🔴 (free flight over arbitrary ground)
verification_method: flux-pinning lift force vs gravity across field environments; p7 $0
since: 2026-06-14
sister: RTSC_05, RTSC_07, RTSC_15, RTSC_16
verdict: 🟢 UFO 호버 = 초전도 자속고정 부상(반중력 아님): 영구자석노면 0.5T/트랙 1T 위 1톤 크래프트 양력 2e7-4e7N ≫ 9810N → 부상(maglev·호버보드 원리). 🔴 임의 지면 자유비행 = 지구장 5e-5T 약+거의 균일(순양력 ~2N) → 불가. RTSC_07(반중력 🔴)을 호버 방식으로 재구성: 강자기장 환경+상온 Type-II SC(RTSC_15/16)면 무냉각 호버크래프트.
---
# RTSC_19 — UFO = 호버크래프트 (자속고정 부상)
> **가설.** UFO를 반중력 아닌 '대형 초전도 호버보드'(자속고정 부상)로 보면 실현 가능한가.
## 측정 (rtsc_ufo_hover.py · 1톤 크래프트, 필요 양력 9810N)
| 자기장 환경 | B | 양력 | 판정 |
|---|---|---|---|
| 지구장(자유비행) | 5e-5 T | 2 N | 🔴 부족 |
| 영구자석 노면 | 0.5 T | 2e7 N | 🟢 부상 |
| 자기 트랙(maglev) | 1 T | 4e7 N | 🟢 부상 |
| 초전도 트랙 | 5 T | 2e8 N | 🟢 부상 |
## 결론
🟢 **호버 방식 UFO 성립** — 강한 외부 자기장(자성 노면/트랙) 위에선 초전도 자속고정으로 1톤도 부상(maglev·호버보드 대형판). 🔴 **임의 공간 자유비행은 불가** — 지구 자기장은 약(5e-5T)하고 거의 균일이라 순양력 ~0. 즉 UFO 호버는 **반중력(RTSC_07 🔴)이 아니라 '강자기장 환경 + Type-II SC'**. 무냉각 상온 Type-II(RTSC_15/16 pyrochlore/CoSn)면 냉각 없이 실현. 자체 자기장+지면 도체 반발(inductrack)도 경로. 한계: 자기 인프라(노면/트랙) 필요 — 진정한 '아무데나 떠다니는 UFO'는 SC로 불가.
verdict: `RTSC/verdicts/ufo_hover.txt`
