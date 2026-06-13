---
id: H_1087
slug: rtsc-candidate
title: RTSC 후보 — Li2MgH16 등 삼원계 수소화물이 상온(Tc>=293K) 초전도 후보다 (Allen-Dynes 스크리닝, 양자 EPC 기반)
domain: universe materials superconductivity electron-phonon BCS
exploration_method: Allen-Dynes Tc screen over published DFT/exp electron-phonon params
verification_method: Allen-Dynes(1975) Tc 공식 (🟢 numerical) over λ/ω_log (🟡 literature); p7 $0
status_grade: 🟢 SUPPORTED (numerical screen) / 🟡 params from literature
since: 2026-06-14
scope: BCS Allen-Dynes 추정치 (full Eliashberg/ab-initio QE deck 미실행); 예측 물질(미합성)·고압(~250 GPa). 합성/상압 미검증.
verdict: 🟢 — Li2MgH16 Allen-Dynes Tc≈355K(82°C)@250GPa (Eliashberg≈473K, Sun 2019); YH10 280K 근접. 상온 초전도 후보 = 삼원계 고-λ 수소화물.
---

# H_1087 — RTSC 후보: 삼원계 수소화물 (Li2MgH16)

> **가설.** 양자(전자-포논 결합) 기반으로 상온 초전도(Tc>=293K) 후보를 찾으면, 고-λ 삼원계 수소화물(Li2MgH16급)이 최상위로 떠오른다.

## 1. 방법 (양자 EPC → Tc)
Allen-Dynes(1975): Tc = (f1 f2 ω_log/1.2)·exp[−1.04(1+λ)/(λ−μ*(1+0.62λ))], μ*=0.10. λ·ω_log = 출판 DFT/실험 EPC 값.

## 2. FROZEN FALSIFIER
- **BLADE.** 어떤 후보도 Tc>=293K(20°C)에 못 미치면 RTSC-후보 기각.

## 3. 측정 (rtsc_allen_dynes_screen.py)
| 물질 | λ | ω_log[K] | P[GPa] | Tc[K] | flag |
|---|---|---|---|---|---|
| **Li2MgH16** | 3.35 | 1330 | 250 | **355 (82°C)** | 🟢 RTSC |
| YH10 | 2.60 | 1282 | 250 | 280 | 🟡 근접 |
| MgH6 | 3.00 | 1100 | 300 | 270 | 🟡 |
| LaH10 (측정 ≈250K) | 2.20 | 1130 | 170 | 214 | |
| H3S (측정 ≈203K) | 2.00 | 1320 | 200 | 229 | |

## 4. 결론
🟢 **Li2MgH16가 상온 초전도 후보** (Allen-Dynes 355K, Eliashberg 473K). 핵심 = 높은 λ(>3)+높은 ω_log(수소 진동). 단 예측물질·미합성·고압(250GPa). 상압/합성은 미해결 — 다음: QE deck(vc-relax+scf+ph+Eliashberg) ab-initio 검증 (a_fire_autonomous로 GPU 발사 가능).
verdict: `RTSC/verdicts/rtsc_screen.txt` · 재현: `python3 RTSC/harness/rtsc_allen_dynes_screen.py`
