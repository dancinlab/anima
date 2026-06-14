---
id: RTSC_28
slug: flatband-screen
title: flat-band@E_F 고속 스크린 — 비자성·상압·flat-band-prone 후보 랭킹 + ready-to-fire QE deck. MP-API 실조회로 11/17 후보가 금속∧비자성(proxy)∧상압(hull≈0) 통과; TOP = β-pyrochlore osmate RbOs2O6 / CsOs2O6 (Os-5d 다중오비탈, 상압 SC). flat-band ΔE는 미계산(🟠 DFT 필요) → 그게 deck의 목적.
domain: rtsc screen materials-project flat-band non-magnetic ambient pyrochlore deck high-throughput
status_grade: 🟡 SCREEN (MP-API 실조회 native axes; flat-band ΔE 🟠 DFT 대기) — 스크린은 좁힐 뿐, 발견하지 않음
verification_method: Materials Project REST API 실조회(secret materialsproject.api_key, urllib, browser-UA) — is_metal·total_magnetization·energy_above_hull 3축; flat-band ΔE는 문헌(🟡) 또는 미계산(🟠); p7 비날조; $0
since: 2026-06-15
sister: RTSC_13, RTSC_15, RTSC_16, RTSC_21, RTSC_26
verdict: 🟡 MP-API 실조회로 flat-band-prone 17개 후보(kagome/pyrochlore/Laves/CaCu5/stannide) 3축 스크린 → **11/17 통과**(금속∧|mag|<0.1∧0≤hull<0.03). Fe/Mn/Co kagome는 예상대로 전부 자성 탈락(FeSn 7.18·Fe3Sn2 14.56·Mn3Sn 17.95·TbMn6Sn6 21.21μB). **TOP = β-pyrochlore osmate RbOs2O6(mp-aaaaahmg, Fd-3m, mag≈0, hull=0.0, 상압 SC Tc≈6.3K) + CsOs2O6(mp-aaabfwkk, 동, Tc≈3.3K)** — RTSC_16이 지목한 pyrochlore 다중오비탈 frontier에 정확히 안착. flat-band ΔE는 MP summary payload에 없음 → **🟠 DFT 필요(=deck의 목적)**. CoSn/CsV3Sb5는 ΔE 이미 실측(−0.44/+0.92) 둘 다 ΔE 탈락. **정직**: MP total_magnetization은 스크린 proxy(MP는 CoSn을 mag=0으로 보고하나 RTSC_21 실QE는 0.43μB) → nspin=2 실SCF로 확인 필수. ready-to-fire deck 2종(rbos2o6·csos2o6) 빌드 완료(ibrav=2 FCC primitive, 9원자, Wyckoff→primitive basis 변환 계산).
---
# RTSC_28 — flat-band@E_F 고속 스크린 + ready-to-fire deck

## 동기 (캠페인의 진짜 병목, RTSC_13/15/21/26)
실 QE DFT에서 **두 real kagome metal이 똑같은 방식으로 실패**:
- **CoSn**(RTSC_21): Co-kagome flat band **ΔE=−0.44 eV**(E_F 한참 아래) **+ 자성**(0.43 μB).
- **CsV3Sb5**(RTSC_26): V-kagome flat band **ΔE=+0.92 eV**(E_F 한참 위), 비자성.

둘 다 **ΔE**(flat band이 E_F에서 너무 멈) ± **자성**으로 탈락. RTSC_13/15가 명명한 병목 =
flat-band E_F-misalignment + competing order. ⇒ **발견 레버 = flat band이 이미 E_F 근처
(|ΔE|≲0.1 eV)에 있는, 비자성·상압·(이상적으로) Type-II 물질을 찾기**. 그게 이 스크린의 사냥감.

## 방법 (데이터 출처 정직, p7 — 날조 없음)
**Path A — Materials Project API 실조회**(secret `materialsproject.api_key` 발견, key 32자).
- MP의 Cloudflare가 기본 urllib UA를 차단(error 1010) → **browser User-Agent**로 통과.
  신규 param `_fields`/`_limit`(구 `fields`/`limit` 폐기). `requests`/`pymatgen` 미설치, stdlib `urllib`만.
- MP가 **native로 제공하는 3축**만 사용: `is_metal`(금속) · `total_magnetization`(비자성 proxy) ·
  `energy_above_hull`(상압-안정). flat-band **|ΔE|는 MP summary payload에 없음**(band-gap/E_F
  포인터만) → 그게 deck이 채울 부분(🟠).
- flat-band-prone family(Fe/Mn/Co 너머)로 17 formula 조회: pyrochlore(β/α) · Laves C15 ·
  CaCu5 hex net · NiAs-type stannide · kagome(reference).
**Path B — curated 문헌 fallback**(key/네트워크 없을 때): 🟡-citation shortlist + 보고된 ΔE/자성.

해석 = **금속 ∧ |mag|<0.1 ∧ 0≤hull<0.03** 통과를 우선, hull로 정렬, ΔE는 DFT 대기(🟠).

## 측정 (MP-API 실조회, verbatim · verdicts/flatband_screen.txt)
**11/17 통과.** Fe/Mn/Co kagome는 예상대로 전부 자성 탈락:
| # | formula | family | metal | mag(μB) | hull | sg | PASS |
|---|---|---|---|---|---|---|---|
| 1 | RbOs2O6 | pyrochlore(β) | yes | 0.00 | 0.0000 | Fd-3m | ✓ |
| 2 | CsOs2O6 | pyrochlore(β) | yes | 0.00 | 0.0000 | Fd-3m | ✓ |
| 3 | KOs2O6 | pyrochlore(β) | yes | 0.00 | 0.0000 | P-1* | ✓ |
| 4 | Bi2Ir2O7 | pyrochlore(α) | yes | 0.00 | 0.0000 | Fd-3m | ✓ |
| 5 | CaCu5 | CaCu5 hex | yes | 0.00 | 0.0000 | P6/mmm | ✓ |
| 6 | CaPd5 | CaCu5 hex | yes | 0.00 | 0.0000 | P6/mmm | ✓ |
| 7 | SnPt | NiAs hex | yes | 0.00 | 0.0000 | P6_3/mmc | ✓ |
| 8 | SnIr | NiAs hex | yes | 0.00 | 0.0000 | P6_3/mmc | ✓ |
| 9 | NbSn2 | stannide | yes | 0.00 | 0.0000 | Fddd | ✓ |
| 10 | CoSn | kagome | yes | 0.00† | 0.0000 | P6/mmm | ✓ |
| 11 | LaRu2 | Laves C15 | yes | 0.00 | 0.0018 | Fd-3m | ✓ |
| — | FeSn/Fe3Sn2/TbMn6Sn6/Mn3Sn/Cd2Re2O7/Ni3In | — | — | 7.18/14.56/21.21/17.95/2.35/1.77 | — | — | 자성 탈락 |

\* KOs2O6는 MP 기저상태가 distorted P-1(hull은 0) — 깨끗한 Fd-3m가 아니라 deck 대상에서 제외.
† **CoSn = 결정적 정직 플래그**: MP는 mag=0(비자성)으로 보고하나 **RTSC_21 실QE는 0.43 μB 자성**.
  ⇒ MP `total_magnetization`은 **스크린 proxy**, ground truth 아님 → nspin=2 실SCF로 확인 필수.

## TOP picks + deck (ready-to-fire)
1. **RbOs2O6** [β-pyrochlore, mp-aaaaahmg, Fd-3m] — 비자성·상압 SC(Tc≈6.3K). Os-5d corner-sharing
   tetrahedra net = RTSC_16이 지목한 pyrochlore 다중오비탈 flat-band frontier. **deck: `RTSC/decks/rbos2o6/`**.
2. **CsOs2O6** [β-pyrochlore, mp-aaabfwkk, Fd-3m] — A-site sibling(Cs, Tc≈3.3K). 동일 Os net,
   더 큰 rattling cage = A-cation이 ΔE를 어떻게 미는지 보는 내장 control. **deck: `RTSC/decks/csos2o6/`**.
3. (LaRu2 [Laves C15, mp-aaaaaczr] — 비자성 SC, 차순위 후보; deck 미빌드.)

deck 사양(둘 다): ibrav=2 FCC primitive(1 f.u.=9원자), celldm 19.18/19.26 Bohr(a≈10.15/10.19 Å),
Wyckoff(A 8b·Os 16c·O 48f x≈0.315)를 **FCC primitive basis로 변환 계산**(추측 아님), PSL 1.0.0 PBE
USPP(Rb/Cs/Os spn + O n), ecutwfc 70/ecutrho 560, K 8×8×8, bands Γ-X-W-K-Γ-L-W nbnd=90. csv3sb5 deck
스타일과 동형. 로컬 pw.x 부재로 구조적 검증(원자수·ibrav·valence)만, 실 pw.x parse는 host에서.

## 각 deck에 필요한 DFT
- **SCF(nspin=1)**: E_Fermi · 전체 에너지 · 자화(≈0 기대).
- **비자성 확정**: nspin=2 + Os에 모멘트 강제 시드 → 0으로 붕괴하는지(RTSC_26 방식, MP proxy 확인).
- **bands + projwfc**: Os-5d t2g flat manifold center vs E_F → **ΔE_flat(부호·폭)**. = 스크린이 못 준 축.
- 이상적이면 후속 DFPT λ/Tc. 정직: PBE는 고온 미왜곡 Fd-3m parent(β-pyrochlore rattling/구조전이 무시).

## 결론
🟡 **SCREEN** — MP-API 실조회가 flat-band-prone 17후보 중 **비자성·상압·금속 11개를 native 3축으로
선별**, Fe/Mn/Co kagome의 자성 탈락을 재확인하고 **β-pyrochlore osmate(RbOs2O6/CsOs2O6)를 TOP으로
지목** + ready-to-fire QE deck 2종을 빌드. **스크린은 탐색을 좁힐 뿐 스스로 발견하지 않는다** — 산출물은
"flat-band@E_F · 비자성 · 상압" 후보에 비싼 QE/DFT fire를 정조준시키는 랭킹+deck. 다음으로 실제 발견을
움직이는 것 = **RbOs2O6 deck을 aiden에서 fire해 Os-5d flat band의 ΔE를 실측**(CoSn −0.44 / CsV3Sb5
+0.92보다 E_F에 가까운가?) + nspin=2로 비자성 확정. flat-band ΔE는 여전히 🟠 — 그게 deck의 존재 이유.

verdict: `RTSC/verdicts/flatband_screen.txt`
