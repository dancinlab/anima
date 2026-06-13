---
id: RTSC_06
slug: lane-fusion-magnet
title: LANE B 핵융합 고자기장 자석(demiurge) — 기준은 상압+고Hc2(≥20T)+Jc@field. REBCO가 20T@20K로 이미 실현(SPARC); RTSC는 필수 아니나 냉각제거로 비용급감 = RTSC 최대 수혜처.
domain: rtsc application fusion magnet REBCO demiurge
status_grade: 🟢 (REBCO buildable now) / 🟠 (RTSC = upgrade not requirement)
since: 2026-06-14
verification_method: application-criteria screen (ambient + Hc2≥20T + Jc@field, 20K ok); 🟡 lit / 🟢 logic
sister: RTSC_05, RTSC_07
verdict: 🟢 핵융합 자석 가능(REBCO Tc93K, Hc2>100T, 20T@20K, SPARC/ITER급). Nb3Sn 25T·Nb-Ti 12T 보조. 고압 RTSC는 코일에 불가. RTSC(상온상압)면 냉각제거→핵융합 비용·크기 급감 = RTSC 1순위 실용 타깃.
---
# RTSC_06 — LANE B 핵융합 고자기장 자석 (demiurge)
> **기준.** 토카막 자석엔 상압 + 고임계자기장(Hc2≥20T) + Jc@field. 온도는 20K cryocooler 허용.
## 측정 (rtsc_3lane_applications.py::LANE B)
REBCO(YBCO tape) Hc2>100T, 20T@20K → 🟢 SPARC/ITER급. Nb3Sn 25T(4K) · Nb-Ti 12T. Li2MgH16 250GPa → 🔴 코일 불가.
## 결론
🟢 **핵융합 자석은 REBCO로 이미 실현**(20T@20K). RTSC는 필수 아님 — 그러나 **상온상압 RTSC면 거대 냉각계 제거 → 핵융합로 비용·크기 급감**. demiurge fusion이 RTSC의 가장 큰 실용 수혜처. 미해결 핵심 = 상온+상압+고Hc2 동시.
verdict: `RTSC/verdicts/3lane_applications.txt`
