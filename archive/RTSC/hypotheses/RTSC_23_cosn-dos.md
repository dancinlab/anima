---
id: RTSC_23
slug: cosn-dos
title: CoSn (kagome P6/mmm) 수렴 DOS — DOS(E_F)·Co-kagome flat-band peak·hole-doping Δn 측정 시도 (summer QE 7.5). 수렴 SCF(E_F=14.7132 eV, mag 0.43 μB) + prior bands(flat band ~0.44 eV below E_F) 까지 verifiable; dense-mesh nscf+dos.x 는 host 과부하(load 60-72, sibling jobs) + ecutrho=520 고비용 으로 미완료 (🟠, p7 no fabricated DOS).
domain: rtsc cosn kagome flat-band dos qe summer hole-doping
status_grade: 🟠 PARTIAL — SCF/bands verifiable; dense nscf+DOS in-progress/blocked (host contention)
verification_method: QE PWSCF v.7.5 on summer pool (CPU-native, GPU/rbfe co-tenant untouched); p7 verbatim, no fabricated numbers
since: 2026-06-15
sister: RTSC_21, RTSC_22
verdict: 🟠 verifiable QE facts 확보 — 수렴 SCF E_Fermi=14.7132 eV, total magnetization 0.43 μB/cell, 93 electrons, ecutwfc=65/ecutrho=520, nspin=2; prior bands.x = Co-kagome FLAT BAND ~0.44 eV BELOW E_F (E_flat~14.27 eV). dense-mesh nscf(tetrahedra, nspin=2)+dos.x 는 미완료: 24³(793 irred k)→16³(270)→12³(133) 로 축소했으나, ecutrho=520 dense FFT(75×75×60)×nspin=2 의 단일-pass band 계산이 본질적으로 무겁고, 공유 summer host 가 sibling 세션 작업(560%-CPU python h1163/h1165 + orphaned /tmp/test_array_methods_base ×2 @99.9% + 보호 대상 rbfe @100%)으로 load 60-72 에 2시간+ 고정되어 wall-clock 진행이 starve 됨. 12³ serial nscf 가 ~250 min CPU(897% threaded) 까지 band sweep 내부에 머물러 JOB DONE 미도달 → DOS(E_F)·flat-band peak height·hole-doping Δn 적분 측정 불가(p7: 날조 안 함). dos.x input 준비됨(emin10 emax18 deltae0.01). nscf 프로세스는 background Monitor 하에 summer 에서 계속 live (kill 안 함, a_dont_kill_live_compute). 완료에는 비혼잡 host 또는 summer load 하락 필요.
---
# RTSC_23 — CoSn 수렴 DOS 측정 시도 (summer QE 7.5)

RTSC_22(CoSn QE 차단 → Co/Sn UPF + nspin=2 LSDA 경로 필요)의 후속. 이제 Co/Sn UPF + nspin=2 SCF 가
실재하고 (수렴), 본 H 는 그 위에서 **DOS** 를 떠서 (a) DOS(E_F), (b) Co-kagome flat-band peak(E,높이),
(c) E_F 를 flat band 위로 내리는 데 필요한 **hole-doping Δn** 을 측정하려 시도.

## TIER 1 🟢 (verbatim, verifiable — 기존 수렴 SCF + bands)
- PWSCF v.7.5, ibrav=4, celldm(1)=9.9760, celldm(3)=0.80680, nat=6 (Co 3f kagome + Sn 1a/2d), nspin=2.
- **the Fermi energy is 14.7132 eV** · convergence achieved in 25 iterations.
- number of electrons = 93.00 · KS states = 56 · ecutwfc=65 Ry · ecutrho=520 Ry.
- **total magnetization = 0.43 Bohr mag/cell** (LSDA).
- prior bands.x: **Co-kagome FLAT BAND ~0.44 eV BELOW E_F** (E_flat ≈ 14.27 eV).

## TIER 2 🟠 (DOS 미완료 — 정직, p7)
- nscf.in 정상 구성: calculation='nscf', occupations='tetrahedra', nspin=2, ecut/celldm/positions/pseudos
  SCF 와 동일, smearing 블록 제거. 24³→793 irred k(과중)→spec 따라 16³(270)→12³(133) 축소.
- pw.x 가 healthy 하게 (~897% multithreaded BLAS) 단일-pass Band Structure Calculation 을 돌았으나
  **JOB DONE 미도달**: ecutrho=520 의 dense 75×75×60 FFT × nspin=2 k-loop 가 본질적으로 무겁고,
  공유 summer host 가 sibling 세션(560%-CPU python h1163/h1165 + orphaned test 바이너리 ×2 + rbfe)으로
  load 60-72 에 2시간+ 고정 → wall-clock starve. 12³ serial 이 ~250 min CPU 까지 band sweep 내부.
- nscf 는 band sweep 완료 시점에만 eigenvalues+Fermi 를 일괄 출력 → 중간 DOS 판독 불가.
- dos.x input 준비됨(&dos prefix='cosn' outdir='./out' fildos='cosn.dos' emin=10 emax=18 deltae=0.01 /),
  nscf save 확정 후 실행 대기.

## 결론
🟢 CoSn 수렴 LSDA SCF + flat-band(~0.44 eV below E_F) 는 verifiable. 🟠 **DOS(E_F)·flat-band peak·
hole-doping Δn 은 미측정** — dense-mesh nscf 가 ecutrho=520 고비용 + summer host 과부하로 미완료
(p7: 날조 안 함). nscf 는 background 에서 계속 live. 완료에는 비혼잡 host(또는 summer load 하락) 필요;
그 후 dos.x → cosn.dos 에서 (a)(b)(c) 판독 가능. (a_dont_kill_live_compute 준수, rbfe co-tenant 무손상,
GPU 무사용.)

verdict 파일: `RTSC/verdicts/cosn_dos.txt`
