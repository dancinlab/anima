---
id: RTSC_21
slug: qe-cosn
title: QE 실DFT — CoSn Co-kagome flat band 확정, ΔE = −0.44 eV (E_F 아래). RTSC_13 예측(~0.2eV 아래) 부호·차수 일치. 정렬=hole-dope ~0.6-0.8 e/cell (RTSC_14 electron 방향 정정).
domain: rtsc qe dft cosn kagome flat-band cross-validation real-engine
status_grade: 🟢 SUPPORTED (real QE 7.5 PBE DFT, flat band + ΔE measured)
verification_method: QE 7.5 pw.x scf(nspin=2)+bands on summer; PSL PBE pseudos; verbatim; p7
since: 2026-06-14
sister: RTSC_13, RTSC_14, RTSC_15, RTSC_22
verdict: 🟢 QE 7.5 PBE CoSn SCF 수렴(E_F=14.7132eV, mag 0.43μB) + bands → Co-3d kagome flat band band45 14.2697eV disp 0.167eV, **ΔE=−0.4435eV(E_F 아래 0.44eV)** band44 −0.55eV, 풀경로 평탄(진짜 localized kagome flat band). RTSC_13(~0.2eV 아래) 부호·차수 일치(2× 깊음). 정렬=hole-dope ~0.6-0.8 e/cell(DOS path-sampled, RTSC_14 electron-dope 방향 정정). Co/Sn pseudo+nspin=2 = QFORGE 미지원분(RTSC_22)을 QE가 메움.
---
# RTSC_21 — QE 실DFT CoSn flat band (실측 ΔE)
## 측정 (QE 7.5 PBE, summer, verbatim · verdicts/qe_cosn.txt)
- pseudos: Sn.pbe-dn-rrkjus_psl.1.0.0 · Co.pbe-spn-rrkjus_psl.0.3.1 (93 val e⁻).
- SCF(nspin=2) 수렴 25 iter, **E_Fermi=14.7132 eV**, E=−1363.808 Ry, mag 0.43 μB/cell.
- bands Γ-K-M-Γ-A: **Co-kagome flat band band45 @14.2697eV (disp 0.167eV) → ΔE=−0.4435eV**; band44 −0.5546eV. 풀경로(Γ-A 포함) 평탄 = 진짜 국소 flat band.
## 결론
🟢 **실 DFT가 CoSn kagome flat band 확정** — E_F 아래 ~0.44-0.55 eV. RTSC_13의 "~0.2eV 아래" 예측을 **부호·차수로 corroborate**(2× 깊음). 정렬엔 **hole-doping ~0.6-0.8 e/cell**(flat band이 E_F 아래라 — RTSC_14의 electron-dope 방향을 실DFT가 정정). QFORGE가 막힌 Co/Sn pseudo+nspin=2를 QE가 처리 → CoSn 경로 실측 가능 확인. 정직: degauss/k-mesh 완화·SCF 1회 재시작, DOS는 path-sampled(BZ 미수렴) → 도핑량 order-of-mag. 다음: 정밀 tetrahedron DOS + 도핑 sweep + DFPT λ/Tc.
verdict: `RTSC/verdicts/qe_cosn.txt`
