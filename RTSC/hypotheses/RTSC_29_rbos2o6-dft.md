---
id: RTSC_29
slug: rbos2o6-dft
title: QE 실DFT — β-pyrochlore RbOs2O6. Os-5d flat band ΔE=+0.377eV(band43, E_F 위, disp 0.048eV, Os-5d 0.44) + E_F에 평탄 O-p/Os-d 혼성 manifold(band38-40, |ΔE|<0.07eV) — CoSn(−0.44)·CsV3Sb5(+0.92)보다 얕음(ΔE축 승). 그러나 nspin=2 정직검사가 "비자성" 반증 — 이상격자 PBE가 큰 모멘트(total~5μB/abs~9μB, 비붕괴, 자성解가 비자성보다 0.16Ry 낮음). ΔE 문제를 자성 문제로 교환.
domain: rtsc qe dft rbos2o6 pyrochlore osmate flat-band magnetism real-engine
status_grade: 🟠/🔴 (real QE 7.5 PBE — ΔE_flat 얕음 🟠 ∧ 이상격자 비자성 반증 🔴; 모멘트는 PBE/구조 artifact 가능성 플래그)
verification_method: QE 7.5 pw.x scf(nspin=1)+scf(nspin=2 mag-test)+bands+bands.x+projwfc.x on aiden; PSL 1.0.0 PBE USPP; verbatim; p7
since: 2026-06-15
sister: RTSC_28, RTSC_26, RTSC_21, RTSC_16
verdict: 🟠/🔴 aiden(np=3→4, RTSC_27 DFPT와 공존·무손상)서 QE 7.5 PBE RbOs2O6 실측. SCF(nspin=1) 24iter 수렴, **E_Fermi=−0.4290eV**(USPP 내부기준), E=−644.80193Ry, 77전자, 150 irreducible k. **자성 정직검사 충격**: Os에 0.3μB 시드한 nspin=2가 0으로 **붕괴 안 함** — total mag이 1.7→5.6μB로 **성장·진동**(absolute ~9.4μB), 자성解 E=−644.96Ry로 비자성보다 **~0.16Ry(≈2.2eV) 낮음** → **이상 Fd-3m PBE에선 자성이 기저상태**. CsV3Sb5(2.8μB→0.01 붕괴)와 정반대. ⇒ MP "비자성" proxy **반증**(RTSC_21 CoSn 재현). **정직 caveat**: 실물 RbOs2O6은 실험적 비자성 SC(Tc≈6.3K) — ~5μB는 frustrated 5d 금속의 이상격자 PBE **과대자화**(알려진 PBE 병리; 실제론 rattling 왜곡+SOC가 quench) 가능성 큼 → 실물 자성 증거 아님, 함수/구조 artifact 플래그. bands+projwfc: **Os-5d 성격 최강 평탄밴드 = band43 ΔE_flat=+0.377eV(E_F 위) disp 0.048eV Os-5d 0.44**; 추가로 **E_F에 평탄 혼성 manifold band38-40(|ΔE|=0.02-0.07eV)** 존재하나 O-2p 84%/Os-5d 12%(공유결합 Os-O가 순Os-5d 무게를 band42-44로 밀어올림), band39는 E_F를 가로지름. **CoSn(−0.44)·CsV3Sb5(+0.92) 대비**: |ΔE| 가장 얕음(band43 +0.377 < 둘 다; 혼성 manifold는 E_F에 위치) = **ΔE축 승**, 그러나 **자성축 최악**(이상격자 PBE 자성). RTSC_27 ph.x(4랭크 98%) 내내 진행·무손상, milksad/bitcoind/forge/summer-rbfe 무손상.
---
# RTSC_29 — QE 실DFT β-pyrochlore RbOs2O6 (flat-band ΔE + 자성 정직검사 🟠/🔴)

## 동기 (RTSC_28 top pick의 실DFT)
RTSC_28 MP-API 스크린이 **비자성·상압·flat-band-prone** β-pyrochlore osmate **RbOs2O6**를
top으로 골랐고(Fd-3m, MP mag≈0, hull=0, 상압 SC), 열린 질문 = **Os-5d flat band의 ΔE가
실패한 두 kagome 금속(CoSn ΔE=−0.44eV 자성 · CsV3Sb5 ΔE=+0.92eV 비자성)보다 E_F에 가까운가**,
그리고 **정말 비자성인가**(MP mag은 proxy — RTSC_21이 CoSn을 mag=0.43으로 잡아 MP=0을 반증).

## 측정 (QE 7.5 PBE, aiden host, verbatim · verdicts/rbos2o6_dft.txt)
- host: **aiden**(12코어, load~10), mpirun **np=3→4**(idle 코어 ~4 확인 후에만 4로 상향).
  QE 한 스텝씩: SCF(nspin=1)→mag-test SCF(nspin=2)→bands→bands.x→projwfc.x.
  **RTSC_27 ph.x DFPT(4랭크 98%)와 내내 공존** — ph_pass1.out 계속 iter 출력(무손상),
  테넌트(milksad·bitcoind·forge·summer rbfe) 무손상.
- pseudos(PSL 1.0.0 PBE USPP scalar-rel, **헤더 z_valence 검증**): Rb.pbe-spn z=9 · **Os.pbe-spn z=16**
  (5d6s+semicore 5p, l_max=2, 신규 다운로드·헤더 정상) · O.pbe-n z=6.
- **SCF(nspin=1)** 24iter 수렴: **E_Fermi=−0.4290 eV**(USPP 내부 0점; bands가 동일 기준 사용),
  E=−644.80192507 Ry, 77전자(=9+32+36 ✓), 150 irreducible k(8×8×8 MP, degauss 0.025).
  **수렴 정직**: 배포 deck의 local-TF beta=0.3은 charge-sloshing **발산**, plain 0.7은 더 나쁨(→126Ry);
  안정解 = **local-TF + beta=0.2 + mixing_ndim=12 + degauss 0.025**(24iter→5e-8Ry). ΔE 물리는 mixing 무관.
- **자성 정직검사(nspin=2 mag-test)**: Os에 starting_magnetization=0.3 시드 → SCF가 **0으로 붕괴 안 함**.
  total mag 궤적(μB/cell, verbatim): 1.72→1.76→1.98→1.90→2.52→3.65→3.35→2.68→2.96→3.49→4.52→4.23→5.81→5.00→**5.58**;
  absolute mag: …→**9.39**. 모멘트가 시드에서 **멀어지며 성장·진동**(total<absolute = Os 사면체의
  frustrated up/down 스핀밀도). **자성解 E=−644.96089Ry**(kill 시점도 하강 중) = 비자성보다 **~0.16Ry(≈2.2eV) 낮음**
  ⇒ **이상 Fd-3m PBE에선 자성이 기저상태**(강하게 선호, 한계적 artifact 아님). CsV3Sb5(2.8μB→0.01 붕괴)와 **정반대**.
- **bands(121 k-pt, Γ-X-W-K-Γ-L-W, nbnd=55) + bands.x + projwfc.x**(E_F=−0.4290eV 기준):
  - **Os-5d 성격 최강 평탄밴드 = band43**: **ΔE_flat=+0.377eV(E_F 위), disp 0.048eV, Os-5d weight 0.44**.
  - **E_F에 평탄 manifold = band38-40**(|ΔE|=0.02-0.07eV)나 **O-2p 84%/Os-5d ~12%**(공유 Os-O 결합이
    순Os-5d 무게를 band42-44로 밀어올림); **band39는 E_F를 가로지름**.
  - band별(min/max/width/mean, E_F기준): 38(−0.090/−0.017/0.074/−0.067) 39(−0.041/+0.016/0.057/−0.018)
    40(+0.015/+0.071/0.056/+0.048) 42(+0.247/+0.351/0.103/+0.305) 43(+0.350/+0.398/0.048/+0.377) 44(+0.407/+0.483/0.076/+0.458).

## CoSn / CsV3Sb5 비교 결론
- **ΔE 얕음 축**: |ΔE_flat| — CoSn 0.44 · CsV3Sb5 0.92 · **RbOs2O6 band43 +0.377** → **가장 얕음**(둘 다보다 작음);
  게다가 평탄 혼성 manifold가 **E_F에 위치**(|ΔE|<0.07) → 셋 중 **가장 E_F에 가까움**. **RbOs2O6 승**.
- **자성 축**: CoSn 0.43μB(자성) · CsV3Sb5 0.01μB(비자성, 깨끗) · **RbOs2O6 ~5μB total/~9μB abs(이상격자 PBE 자성)**
  → **RbOs2O6 최악**(비붕괴 큰 모멘트).
- **종합**: RbOs2O6는 캠페인이 놓치던 lever(**ΔE→0, flat band이 E_F에**)를 **해결**하나, 그 대가로 **큰 모멘트**를 도입 —
  이상격자 PBE 계산상으론 kagome보다 **더 나은 무냉각 RTSC base 아님**(ΔE 문제 ↔ 자성 문제 교환).
  **단**, 모멘트가 PBE/이상구조 artifact라면(실물 비자성 6.3K SC라 매우 유력) RbOs2O6는 **역대 최고 base**
  (비자성 ∧ flat band이 E_F에)가 됨 — 그러나 그건 **non-PBE/왜곡셀/SOC 재검사**가 필요(이번 fire는 미실시).

## 정직 caveat
- 실물 RbOs2O6 = 실험적 **비자성 초전도체**(Tc≈6.3K, Yonezawa+ 2004). ~5μB PBE 모멘트는 frustrated 5d 금속의
  **이상 고대칭 격자 과대자화**(알려진 PBE 병리; 실제론 rattling 비조화 왜곡 + 더 강한 SOC가 quench) 가능성 큼.
  ⇒ **DFT-PBE 이상격자 결과는 자성**(p7로 보고)이나 실험과 충돌 → 함수/구조 artifact로 플래그, 실물 자성 증명 아님.
  어느 쪽이든 CsV3Sb5식 nspin=2→0 깨끗 붕괴는 **아님**.
- nspin=2는 aiden 공존 contention 때문에 conv_thr 1e-5 + 6×6×6 cap(자성 verdict는 robust; 모멘트는 kill 시점도 상승 중 → ~5μB는 PBE 모멘트의 **하한**).
- bands2 = nbnd55/20pt(배포 90/40 deck의 wall-time trim, 동일 manifold 해상). PBE·이상 Fd-3m·scalar-rel USPP(**SOC 없음**).

## 결론
🟠/🔴 — 실 DFT가 RbOs2O6의 **Os-5d flat band이 E_F에 가장 가까움**(band43 ΔE=+0.377eV, 혼성 manifold는 E_F에;
CoSn·CsV3Sb5보다 얕음)을 확인, 그러나 **이상격자 nspin=2 정직검사가 "비자성"을 반증**(비붕괴 ~5μB, 자성解가 비자성보다 0.16Ry 낮음).
RbOs2O6는 ΔE lever를 해결하나 자성 결함을 도입 — 이상격자 PBE상 kagome보다 나은 base 아님. 단 모멘트가 artifact면(유력) 최고 base 후보.
다음: non-PBE(SCAN/+SOC) 또는 저온 왜곡셀로 모멘트 quench 여부 재검사 → 비자성이면 DFPT λ/Tc; CsOs2O6(RTSC_28 deck) 동일 검사.

verdict: `RTSC/verdicts/rbos2o6_dft.txt`
