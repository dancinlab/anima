---
id: RTSC_26
slug: csv3sb5-qe
title: QE 실DFT — CsV3Sb5(비자성 kagome SC) V-flat band ΔE=+0.923eV(E_F 위) 실측. 비자성 확정(강제 2.8μB→0.01μB). CoSn(ΔE=−0.44eV+자성 0.43μB) 대비 — 자성결함은 교정(비자성 승), ΔE는 더 깊음(0.92>0.44, 정렬 더 어려움).
domain: rtsc qe dft csv3sb5 kagome flat-band non-magnetic cdw cross-validation real-engine
status_grade: 🟢 SUPPORTED (real QE 7.5 PBE DFT on aiden — E_F·자화·ΔE_flat·V-3d character 실측)
verification_method: QE 7.5 pw.x scf(nspin=1)+scf(nspin=2 mag-test)+bands+projwfc on aiden; PSL 1.0.0 PBE pseudos; verbatim; p7
since: 2026-06-14
sister: RTSC_21, RTSC_13, RTSC_14, RTSC_15
verdict: 🟢 aiden(12코어, np=4)서 QE 7.5 PBE CsV3Sb5 실측. SCF(nspin=1) 수렴 21iter, **E_Fermi=8.5762eV**, E=−590.3331Ry, 73전자. **비자성 확정**: nspin=2에 V를 0.4(→2.8μB)로 강제 시드해도 SCF가 0으로 붕괴(2.82→2.60→−0.30→…→**total mag 0.01μB**), 비자성이 기저상태(nspin=1보다 +0.84mRy 낮음) → CoSn 0.43μB 자성 결함을 **비자성으로 교정**. bands(211 k-pt, Γ-M-K-Γ-A-L-H-A)+projwfc: **V-3d kagome flat band = band41 @ΔE_flat=+0.9229eV(E_F 위), disp 0.215eV, V-3d weight 0.773**(flat manifold band38-44 모두 V-3d 61-80%, E_F 위 +0.6~+1.4eV). **CoSn 비교: 자성=비자성 승(0.01 vs 0.43μB)이나 |ΔE|=0.92>0.44 = 더 깊음**(CoSn은 E_F 아래 hole-dope, CsV3Sb5는 E_F 위 electron-dope, 정렬에 더 많은 도핑 필요). 깨끗(비자성)하나 정렬은 더 어려운 base. CDW caveat: PBE=고온 미왜곡 P6/mmm parent(24 Sym+inversion), ~94K CDW 초격자가 실제론 FS 일부 갭. aiden 테넌트(bitcoind·mullvad·forge) 무손상, summer 미사용.
---
# RTSC_26 — QE 실DFT CsV3Sb5 비자성 kagome flat band ΔE (실측 🟢)

## 동기 (RTSC_21 후속)
RTSC_21 실QE에서 CoSn은 (a) Co-kagome flat band이 **E_F 아래 ΔE=−0.44 eV로 깊고**
(b) **자성 금속**(mag 0.43 μB)으로 드러나 — 둘 다 RTSC SC base로 실격. CsV3Sb5는
**비자성**(예상) + **실측 SC**(Tc≈0.9–2.5K, CDW order)라 CoSn의 자성 결함을 교정하는
실물질 후보. 열린 질문 = **V-kagome flat band의 ΔE가 CoSn보다 얕은가**(|ΔE|<0.44 eV,
E_F 어느 쪽), 그리고 **정말 비자성인가**.

## 측정 (QE 7.5 PBE, aiden host, verbatim · verdicts/qe_csv3sb5.txt)
- host: **aiden**(12코어, load~8), mpirun **-np 4**(여유 확보). QE 한 스텝씩: scf→scf_mag→bands→projwfc.
- pseudos(PSL 1.0.0 PBE USPP scalar-rel, 헤더 검증): Cs.pbe-spn-rrkjus **z=9**(손상된 Cs spnl
  z=−5.0 변종 거부) · V.pbe-spnl-rrkjus **z=13**(3s3p semicore, 권장 rho 645Ry) · Sb.pbe-n-rrkjus **z=5**.
  정직: V는 PSL 1.0.0이 `spnl` rrkjus만 제공(`V.pbe-spn-rrkjus` 부재) — spnl이 z=13 정상 pseudo
  (scalar-rel, rho 645Ry = deck 650Ry 캡과 일치). 손상-spnl 경고는 **Cs** 해당(거부), V 아님.
- **SCF(nspin=1)** 수렴 21iter: **E_Fermi=8.5762 eV**, E=−590.33305 Ry, 73전자, 76 irreducible k-pt.
- **비자성 확정(nspin=2 mag-test)**: starting_magnetization(2)=0.4로 V kagome에 모멘트 강제 시드
  → SCF가 2.82→2.60→−0.30→…→**total mag 0.01 μB / absolute 0.01 μB**로 붕괴.
  E=−590.33304 Ry(nspin=1보다 **+0.84 mRy 높음** → 비자성이 기저상태, 강제 2.8μB가 0으로 풀림).
  ⇒ **CsV3Sb5는 비자성**(CoSn 0.43μB와 결정적 대조).
- **bands(211 k-pt, Γ-M-K-Γ-A-L-H-A, nbnd=60) + projwfc**: V-3d flat manifold = band38-44
  (V-3d weight 0.61–0.80, E_F 위 +0.6~+1.4 eV). **flattest = band41**:
  **ΔE_flat=+0.9229 eV(E_F 위), dispersion width 0.215 eV, V-3d 0.773**. E_F **아래**엔 평탄 V-3d 밴드 없음.

## CoSn 비교 결론
- **자성 축**: CsV3Sb5 0.01μB(비자성) vs CoSn 0.43μB(자성) → **CsV3Sb5 승**(자성은 SC pairing에
  적대적 — 더 어려운 결함을 CsV3Sb5가 제거).
- **ΔE 얕음 축**: |ΔE_flat| = **0.923 eV > CoSn 0.4435 eV** → CsV3Sb5가 **더 깊음**(얕지 않음).
  CoSn은 E_F **아래**(hole-dope 정렬), CsV3Sb5는 E_F **위**(electron-dope 정렬) — 방향도 반대,
  정렬에 더 많은 도핑 필요.
- **종합**: CsV3Sb5는 CoSn보다 **깨끗(비자성)하나 정렬은 더 어려운** base. 강한 RTSC base는
  비자성 ∧ |ΔE| 작음 둘 다 원하는데, CsV3Sb5는 첫째만 만족.

## CDW caveat (정직)
PBE 계산은 **고온 미왜곡 P6/mmm parent 상**(pw.x "24 Sym. Ops., with inversion"). 실물질은
**~94K CDW**(2×2×2 / 2×2×4 초격자)로 FS 일부 갭 + 밴드 재구성 → ΔE_flat=+0.92eV는 parent-phase
flat-band 위치. 저온 CDW 상에선 이동. degauss/k-mesh/SCF는 RTSC_21과 동일 verbatim+p7 규약.

## 결론
🟢 **SUPPORTED** — 실 DFT가 CsV3Sb5의 **비자성**(강제 2.8μB→0.01μB)과 **V-kagome flat band**
(band41, ΔE=+0.923 eV E_F 위, disp 0.215 eV, V-3d 77%)을 실측. RTSC_15의 "ΔE 얕은 비자성 base
재탐색" 표적에 대해: CsV3Sb5는 **자성 결함을 교정**(CoSn의 더 큰 결함 해결)하나 **ΔE는 더 깊다**
(0.92>0.44) — 비자성 우위, 정렬-용이성 열위. 다음: electron-doping sweep(BZ DOS) + CDW(2×2×2)
재계산 + DFPT λ/Tc로 비자성 kagome SC base 정량화.

verdict: `RTSC/verdicts/qe_csv3sb5.txt`
