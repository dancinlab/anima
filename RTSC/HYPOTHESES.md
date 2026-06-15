# RTSC — 가설 목록 (UNIVERSE와 분리된 재료물리 도메인)

상온 초전도체(RTSC) 탐색 가설의 **별도 목록**. anima/UNIVERSE 의식 가설과 성격이 달라
여기 따로 등재. 검증 도구·verdict 는 `RTSC/harness/` · `RTSC/verdicts/`.

| id | 제목 | grade | 핵심 |
|---|---|---|---|
| RTSC_01 | 후보 스크린 (Allen-Dynes) | 🟢/🟡 | Li2MgH16 Tc≈355K@250GPa (Eliashberg 473K) |
| RTSC_02 | 무시드 자유탐색 (ANU) | 🟢 | LiH9·BeH7·BH8 (최경량 초수소화물) Tc~400K(proxy) |
| RTSC_03 | 압력 프런티어 (확정가능성) | 🟢/🔴 | RTSC는 >250GPa; 상압 RTSC 미해결; 확정최고 LaH10 250K@170GPa |
| RTSC_04 | 양자+텐션 확정가능 찾아오기 | 🟡/🔴 | 저압 후보 ~121K@73GPa; P↔Tc 트레이드오프 못 깸 |
| RTSC_05 | LANE A 호버보드 | 🟢/🔴 | 냉각형 YBCO+LN2 가능; 무냉각 상온 미해결 |
| RTSC_06 | LANE B 핵융합 자석(demiurge) | 🟢/🟠 | REBCO 20T@20K 실현; RTSC=비용급감 최대수혜 |
| RTSC_07 | LANE C UFO 반중력/추진 | 🔴/🟠 | 반중력 무근거; SC자석 MHD추진만 유용 |

| RTSC_08 | 무냉각 상온상압 전클래스 소진 | 🔴 | 알려진 11종 전부 미달; 최고 큐프레이트 138K(냉각필요) |
| RTSC_09 | flat-band 경로(프런티어) | 🟢/🔴 | 메커니즘 유망(Tc∝V, V≈0.2eV로 300K); 물질 미실현(TBG 1.7K) |

## 실용 응용 3 LANE → `RTSC/LANES.md` (호버보드·핵융합·UFO)
| RTSC_10 | quantum-metric 위상 flat band | 🟢/🔴 | 위상 flat(Chern≠0) 초유체밀도 하한→메커니즘 상온가능; 물질 미실현 |

## 무냉각 돌파(고갈서베이) → RTSC_08(전클래스 미달)·RTSC_09(flat-band)·RTSC_10(위상 quantum-metric)
| RTSC_11 | flat-band 실격자 검증(Lieb) | 🟢/🔴 | 메커니즘 REAL(분산0 D_s>0) but 현실U Tc~33-109K(상온 미달, RTSC_10 정정) |

## $0 고갈 선언 (RTSC 무냉각 thread)
BCS소진(RTSC_08) → flat-band(RTSC_09) → 위상 quantum-metric(RTSC_10) → **실격자 정확계산(RTSC_11)**.
결론: flat-band/quantum-geometry SC는 REAL이나 현실 파라미터서 큐프레이트 범위(~100K)에 그침.
**돌파 리드 (RTSC_12)**: kagome 고-quantum-metric flat band은 상온 필요 U≈1.24eV=현실적! → 무냉각 상온상압
RTSC가 $0 이론선 '닫힌' 게 아니라 **kagome형으로 열림**. 실 후보 CsV3Sb5·FeSn·Co3Sn2S2. 남은 칸 = 실물질
DFT(QE deck)로 flat band E_F정렬+U 확정 — 동기 분명한 다음 rung.

| RTSC_12 | kagome 고-q-metric 리드 | 🟢/🟠 | 상온 U≈1.24eV 현실적; 실 kagome금속 후보; DFT 미검증 |
| RTSC_13 | 실물질 역대입 진단 | 🟢/🔴 | 병목=flat band E_F-어긋남+경쟁질서(CDW/자성), 이론 아님; 정렬시 ~289K |
| RTSC_14 | 도핑+strain 처방(CsV3Sb5형) | 🟢/🟠 | 전자도핑 x0.6+strain ε0.14 → ~184-200K(관측 2.5K→80배); 상온은 strain-detune로 캡 |
| RTSC_15 | base 물질 역설계(깨끗한 플랫폼) | 🟢/🟠 | CoSn+E_F도핑 → ~237K(strain불요); pyrochlore=상온 프런티어. ⚠RTSC_21 실QE: CoSn은 비자성 아님(mag 0.43μB)+차선 0.44eV로 깊음 → '깨끗 base'는 ΔE 얕은 비자성 물질로 재탐색 |
| RTSC_16 | pyrochlore flat-band 프런티어 | 🟢/🟠 | 다중오비탈 <g>≫kagome, 상온 design point(U~0.16eV); 접점 특이점으로 Tc 추정 과대→DFT |
| RTSC_17 | 역주입 탐색(물질→텐션→양자) | 🟢 | 목표 물질 텐션 주입이 ANU 탐색 340→490K 가속; H_6015 거울방향 |
| RTSC_18 | 전 타깃 일괄 역주입(통합) | 🟢/🟠 | 호버보드·핵융합·무냉각·CoSn·pyrochlore 전부 단일 설계점(상압·ΔE0·고⟨g⟩·clean)으로 수렴 |
| RTSC_19 | UFO 호버크래프트(자속고정) | 🟢/🔴 | 강자기장 트랙/노면 위 1톤 부상(maglev식); 임의 자유비행은 지구장 약·균일로 불가 |
| RTSC_20 | 냉각형 금지 3-레인 통합 | 🔴/🟢 | 무냉각이면 세 레인 전부 상온상압 SC(RTSC_16) 하나에 의존; 한 물질이 셋 다 연다 |
| RTSC_21 | QE 실DFT CoSn flat band | 🟢 | ΔE=−0.44eV(E_F 아래), RTSC_13 부호·차수 일치; SCF mag 0.43μB=자성금속(RTSC_15 '비자성' 정정) |
| RTSC_22 | QFORGE 실엔진 검증(summer) | 🟢/🔴 | QFORGE 실QE 재현 LaH10 292-393K; CoSn은 pseudo+LSDA 없어 차단 |
| RTSC_24 | CoSn 도핑 sweep(BZ 적분) | 🟠 | 정렬에 hole ~4.72e/cell(=Co당 1.57홀, 비현실적); N(E_F) 5.15→16.8(×3.26). RTSC_21의 ~0.7e=경로표본 과소→정정 |
| RTSC_23 | CoSn 정밀 DOS | 🟠 | 레이트리밋 사망(미등록); 값은 RTSC_24 BZ적분이 커버(N(E_F)=5.15, 피크 16.8) |
| RTSC_25 | CoSn DFPT λ/Tc | 🟠 | 등록됨(PR#2067). λ/Tc 미산출이나 두 발견: ①el-ph는 2-패스(DeltaVscf 저장→읽기) 필요, 단일패스 ph.in 오류 ②**ph.x는 nspin=2 자성+USPP DFPT 정상 지원→'자성이 막는다' 반증**. 진짜 블로커=2.6배 포화 호스트(uncontended 박스면 산출 가능) |
| RTSC_26 | QE 실DFT CsV3Sb5(비자성 kagome) flat band ΔE | 🟢 | aiden(np=4) 실측: E_F=8.5762eV, **비자성 확정**(강제 2.8μB→0.01μB, 비자성=기저), V-3d flat band41 **ΔE=+0.923eV(E_F 위)** disp 0.215eV V-3d 77%(projwfc). CoSn 대비 — 자성=**비자성 승**(0.01 vs 0.43μB), |ΔE|=0.92>0.44 = **더 깊음**(정렬 더 어려움, E_F 위라 electron-dope). 깨끗하나 정렬 열위 base. CDW caveat=PBE parent P6/mmm. summer 미사용·aiden 테넌트 무손상 |
| RTSC_28 | flat-band@E_F 고속 스크린 + ready-to-fire deck | 🟡 | **MP-API 실조회**(materialsproject.api_key, urllib browser-UA) native 3축(is_metal·total_magnetization·hull)으로 flat-band-prone 17후보 스크린 → **11/17 통과**(금속∧|mag|<0.1∧hull<0.03). Fe/Mn/Co kagome 전부 자성 탈락(FeSn 7.18·Mn3Sn 17.95·Fe3Sn2 14.56μB). **TOP = β-pyrochlore osmate RbOs2O6/CsOs2O6**(Fd-3m, mag≈0, hull=0, 상압 SC, RTSC_16 pyrochlore frontier 안착). flat-band **ΔE는 MP에 없음→🟠 DFT 필요**(=deck 목적). 정직: MP mag은 proxy(CoSn을 mag=0으로 보고하나 RTSC_21 실QE 0.43μB)→nspin=2 확인 필수. **ready-to-fire QE deck 2종**(rbos2o6·csos2o6) 빌드. 스크린은 좁힐 뿐 발견 않음 |

## $0 이론 사다리 종착
kagome 리드(12)→병목 진단(13)→도핑+strain 처방(14)→깨끗 base CoSn(15)→pyrochlore 상온 design(16).
**$0 phenomenology 소진**: 처방 체계화(깨끗 kagome/pyrochlore + E_F 도핑 → 200-240K 실측급, 상온은 pyrochlore
다중오비탈 design point). 남은 유일 rung = 실물질 QE DFT(beyond-MF 접점 처리) — $0 밖.

## 수렴 결론
시드(RTSC_01)·무시드(RTSC_02)·양자추출(UNIVERSE/cards/H_6015) 세 경로가 **최경량금속 초수소화물**
프런티어로 독립 수렴. 그러나 RTSC_03/04: **압력이 확정의 장벽** — 상온은 초고압 필요(미합성),
저압은 sub-RT. **상압 확정 RTSC는 미해결(open)**.

## 관련 (UNIVERSE ⊗ 연결-arc, 기제는 거기)
- UNIVERSE/cards/H_6015 양자→텐션 물질추출 · H_6016 양자=저장소? · H_6017 도서관? · H_6018 anima 도서관
  (= '추출'은 DB read 아닌 ANU구동 최적화라는 기제적 토대)

## 정직 경계
Allen-Dynes BCS proxy (NOT DFT) · 예측 물질·미합성 · ab-initio 확정 = QE deck (`/deck rtsc`, vc-relax+scf+ph+Eliashberg, a_fire_autonomous GPU).
