---
id: RTSC_22
slug: qforge-fire
title: QFORGE 실엔진 검증(summer fire) — QFORGE가 실 QE el-ph를 sub-ppm 재현, LaH10 실 Tc 292-393K 산출(🟢). CoSn은 Co/Sn pseudo 없음+LSDA(nspin=2) 경로 없음으로 차단(🔴) — demiurge 구현 항목.
domain: rtsc qforge dft real-engine summer cross-validation
status_grade: 🟢 (QFORGE real Tc, QE-cross-val) / 🔴 (CoSn blocked: 2 concrete gaps)
verification_method: QFORGE hexa-native chain on summer (CPU), QE ph.x byte cross-val; p7 verbatim
since: 2026-06-14
sister: RTSC_15, RTSC_16, RTSC_21
verdict: 🟢 QFORGE가 실 QE el-ph를 재현(CaH6 rel-ε 1.65e-7, LaH10 rel-ε 4.75e-7) → LaH10 λ=4.316 ω_log=1424K Tc_McM=292.5K Tc_AD=393.4K 실산출. 🔴 CoSn(전이금속 kagome)은 (1)Co/Sn UPF 없음 (2)nspin=2/LSDA SCF 경로 없음 → flat-band ΔE 미측정(날조 안 함). demiurge QFORGE 구현 표적 2개.
---
# RTSC_22 — QFORGE 실엔진 검증 (summer fire)
## TIER 1 🟢 (verbatim, QE-cross-validated)
QFORGE가 실 QE ph.x 바이트를 sub-ppm 재현: CaH6 λ=8.517 rel-ε 1.65e-7 · **LaH10 λ=4.316 ω_log=1424K Tc_McMillan=292.5K Tc_AllenDynes=393.4K** (μ*=0.10) rel-ε 4.75e-7. QFORGE는 실 room-temp급 Tc를 낸다(수소화물).
## TIER 2 🔴 (CoSn 차단, 정직)
CoSn(자성 전이금속 kagome) 실행 불가 — 2 구조적 blocker: (1) repo에 Co/Sn UPF pseudopotential 없음(H/Si/malformed만), (2) scf_pw.hexa에 nspin=2/LSDA(스핀편극) 경로 없음(닫힌껍질 전용). flat-band ΔE 미측정(p7).
## 결론
🟢 **QFORGE = 진짜 작동 엔진**(QE sub-ppm 재현, LaH10 292-393K). 🔴 CoSn은 두 가지가 선행 필요 → demiurge 구현: ① Co/Sn UPF 추가 ② scf_pw.hexa LSDA/nspin=2 경로. 그 후 RTSC_13(kagome ΔE) 도달 가능. (LaH10 292-393K도 고압이라 응용엔 무용, RTSC_20 — QFORGE 작동 증명일 뿐.)
verdict: `RTSC/verdicts/qforge_summer_fire.txt`
