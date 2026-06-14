---
id: RTSC_26
slug: csv3sb5-qe
title: QE 실DFT — CsV3Sb5(비자성 kagome SC) flat band ΔE 측정. CoSn(ΔE=−0.44eV+자성)의 자성 결함을 비자성(nspin=1)으로 교정한 실물질. 🟠 DEFERRED — deck 빌드+QE입력검증 완료, SCF는 summer 과부하(타 QE 동시실행)로 미실행.
domain: rtsc qe dft csv3sb5 kagome flat-band non-magnetic cdw cross-validation real-engine
status_grade: 🟠 DEFERRED (deck built + pw.x input-validated; SCF/bands blocked by summer oversubscription)
verification_method: QE 7.5 pw.x scf(nspin=1)+bands on summer; PSL 1.0.0 PBE pseudos; verbatim; p7
since: 2026-06-14
sister: RTSC_21, RTSC_13, RTSC_14, RTSC_15
verdict: 🟠 CsV3Sb5 deck(ibrav=4, a=5.45/c=9.31Å, 9원자, 73 val e⁻, nspin=1, Cs1a/V3g-kagome/Sb1-1b/Sb2-4h, ecut 65/650Ry — V USPP rho 645Ry가 캡)를 **빌드+QE입력검증**(pw.x: 9원자·73전자·24 Sym.Ops P6/mmm·card 통과). pseudo 3종 PSL1.0.0 PBE 다운로드(Cs spnl변종 z헤더 손상→spn z=9로 정정). **SCF는 미실행** — summer가 타 세션 CoSn QE bands(nscf, 6랭크) + 기타 무거운 테넌트로 ~25분 내내 과부하(load 60–72/12코어). HARD CONSTRAINT(QE 동시 1개·과부하시 STOP·thrash 금지) 준수해 2번째 동시 QE를 쌓지 않고 🟠 deferred. E_Fermi·자화·ΔE_flat 미측정. rbfe(PID 2140) 전후 ALIVE·UNTOUCHED. deck = RTSC/decks/csv3sb5/ 에 1커맨드 실행대기.
---
# RTSC_26 — QE 실DFT CsV3Sb5 비자성 kagome flat band ΔE (🟠 DEFERRED)

## 동기 (RTSC_21 후속)
RTSC_21 실QE에서 CoSn은 (a) Co-kagome flat band이 **E_F 아래 ΔE=−0.44 eV로 깊고**
(b) **자성 금속**(mag 0.43 μB)으로 드러나 — 둘 다 RTSC SC base로 실격. CsV3Sb5는
**비자성**(nspin=1로 처리) + **실측 SC**(Tc≈0.9–2.5K, CDW order)라 CoSn의 자성 결함을
교정하는 실물질. 열린 질문 = **V-kagome flat band의 ΔE가 CoSn보다 얕은가**(|ΔE|<0.44 eV,
E_F 어느 쪽인가).

## 진행 (QE 7.5 PBE, summer, verbatim · verdicts/qe_csv3sb5.txt)
- pseudos(PSL 1.0.0 PBE USPP scalar-rel): Cs.pbe-spn-rrkjus(z=9) · V.pbe-spnl-rrkjus(z=13,
  3s3p semicore) · Sb.pbe-n-rrkjus(z=5). **정직 발견**: Cs `spnl`(f-semicore) 변종은
  공식사이트 UPF 헤더가 손상(z_valence=−5.0 파싱)→ `spn`(z=9 정상)으로 정정.
- deck: ibrav=4, a=5.45/c=9.31Å, nat=9, ntyp=3, **nspin=1**(CoSn nspin=2 대비 핵심 대조),
  ecutwfc=65/ecutrho=650Ry(**V USPP rho 645Ry가 하한 캡** — flat band 정밀도 위해 8×wfc 초과).
  Wyckoff: Cs 1a(0,0,0)·V 3g(kagome z=1/2)·Sb1 1b(0,0,1/2)·Sb2 4h(z≈0.74). K 12×12×6.
- **pw.x 입력검증 통과**(verbatim): "number of atoms/cell=9" · "number of electrons=73.00" ·
  ibrav=4 · "24 Sym. Ops., with inversion, found"(완전 P6/mmm). (초기 ntyp=4→card_atomic_species
  5010 에러: CsV3Sb5는 원소 3종(Sb 2사이트=동원소) → ntyp=3 정정.)

## 미측정 (차단)
E_Fermi · total magnetization(≈0 기대, CoSn 대조점) · ΔE_flat(부호 포함) · dispersion width ·
CoSn 비교 — **전부 SCF/bands 미실행으로 미측정**.

## 차단 사유 (정직)
summer가 타 세션의 **CoSn QE bands(nscf, mpirun -np 6 pw.x, PID 127435, 22:40 시작)** +
기타 무거운 테넌트(python h1163 G5 verify @621%, 2× test_array_methods @100% 15h, rbfe @100%)로
~25분 내내 load 60–72/12코어 과부하. HARD CONSTRAINT = **QE 동시 1개**(과부하가 잡을 굶김) +
**과부하시 STOP·재발사 thrash 금지**. 22:45에 probe SCF(4랭크) 1회 발사→saturated box(load 16→71)
확인 즉시 내 랭크만 kill(타 nscf·rbfe 무손상), 추가 동시발사 안 함 → 🟠 deferred 정직 보고.

## 결론
🟠 **DEFERRED** — CsV3Sb5 deck는 빌드+QE입력검증 완료(실행 1커맨드 대기, RTSC/decks/csv3sb5/),
SCF는 summer 과부하로 미실행. CoSn 자성 결함을 비자성 실물질로 교정하는 표적은 유효;
**ΔE_flat 실측은 summer load 해소 후(QE 동시 1개) 재개**. CDW caveat: PBE는 고온 미왜곡
P6/mmm parent 상(~94K CDW 초격자 없음) → ΔE는 parent-phase flat-band 위치. RTSC_21과 동일
verbatim+p7 규약. NEXT: load 클리어 시 scf→bands→ΔE_flat→CoSn(−0.44eV) 비교.

verdict: `RTSC/verdicts/qe_csv3sb5.txt`
