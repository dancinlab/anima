# RTSC — 캠페인 전체 기록 (anima, demiurge로 완전 이관·동결)

> **상태: 2026-06-15 demiurge로 완전 이관 완료. anima `RTSC/` 폴더는 폐기됨.**
> 이 문서가 anima에 남는 **유일한 RTSC 기록(SSOT)**이다. 실제 진행/소유는 demiurge `dancinlab/demiurge`.
> 원본 `RTSC/`(가설 29 + verdict + deck + harness, 90파일)는 git 이력 + demiurge 핸드오프에 보존.

## 이관처 (demiurge)
- 축 SSOT: `domains/RTSC/research/anima_flatband_handoff.md` (PR #623, RTSC_29 fold PR #624)
- 이관 deck: `exports/rtsc/decks/anima_{csv3sb5,rbos2o6,csos2o6}`
- 레저: `RTSC_LEDGER.jsonl` (CoSn·CsV3Sb5·RbOs2O6 measured, CsOs2O6 queued)
- 레지스트리: `sidecar handoff ls demiurge` (id d5483415)
- 엔진: demiurge canonical = QFORGE (QE cross-val)

---

## 1. 캠페인 한 줄 결론

**무냉각(상온·상압) 초전도체의 관문 = "전자 정체차선(flat band)이 페르미 준위 E_F에 정렬 + 비자성 + 상압".**
고압 수소화물은 Tc는 높아도 250 GPa라 실용 불가. flat-band 경로가 유일한 상압 길이며, 실 DFT로
**병목 = flat band의 E_F-어긋남(ΔE) + 경쟁 자성/CDW**임을 확정. 최종 단계에서 **RbOs₂O₆(β-pyrochlore)가
flat band을 E_F에 처음 정렬(ΔE 축 돌파)** — 단 ideal-PBE 자성(아티팩트 추정)이 남아 demiurge가 SOC/비-PBE로 후속.

## 2. 가설 전체 (RTSC_01–29)

| # | 제목 | grade | 핵심 |
|---|---|---|---|
| 01 | 후보 스크린(Allen-Dynes) | 🟢/🟡 | Li2MgH16 Tc≈355K@250GPa |
| 02 | 무시드 자유탐색(ANU) | 🟢 | 최경량 초수소화물 ~400K(proxy) |
| 03 | 압력 프런티어 | 🟢/🔴 | RTSC는 >250GPa; 상압 미해결 |
| 04 | 양자+텐션 확정탐색 | 🟡/🔴 | P↔Tc 트레이드오프 못 깸 |
| 05 | LANE A 호버보드 | 🟢/🔴 | 냉각형만 가능, 무냉각 미해결 |
| 06 | LANE B 핵융합 자석 | 🟢/🟠 | RTSC=비용급감 최대수혜 |
| 07 | LANE C UFO | 🔴/🟠 | 반중력 무근거; SC자석 추진만 |
| 08 | 무냉각 전클래스 소진 | 🔴 | 알려진 11종 전부 미달 |
| 09 | flat-band 경로 | 🟢/🔴 | 메커니즘 유망, 물질 미실현 |
| 10 | quantum-metric 위상 flat | 🟢/🔴 | 상온가능 메커니즘, 물질 미실현 |
| 11 | flat-band 실격자(Lieb) | 🟢/🔴 | 현실 U면 Tc~100K 한계 |
| 12 | kagome 고-q-metric 리드 | 🟢/🟠 | 상온 U≈1.24eV 현실적 |
| 13 | 실물질 역대입 진단 | 🟢/🔴 | 병목=flat band E_F-어긋남+경쟁질서 |
| 14 | 도핑+strain 처방 | 🟢/🟠 | ~184-200K, 상온은 strain-detune 캡 |
| 15 | base 물질 역설계 | 🟢/🟠 | 깨끗 base+E_F도핑 ~237K |
| 16 | pyrochlore 프런티어 | 🟢/🟠 | 다중오비탈 ⟨g⟩↑, 상온 design point |
| 17 | 역주입(물질→텐션→양자) | 🟢 | ANU 탐색 가속(거울방향) |
| 18 | 전 타깃 일괄 역주입 | 🟢/🟠 | 단일 설계점으로 수렴 |
| 19 | UFO 호버크래프트 | 🟢/🔴 | maglev식 부상 가능, 자유비행 불가 |
| 20 | 냉각금지 3-레인 통합 | 🔴/🟢 | 한 물질이 호버/핵융합/UFO 셋 다 연다 |
| **21** | **QE 실DFT CoSn** | 🟢 | **flat band ΔE=−0.44eV, 자성 0.43μB** |
| 22 | QFORGE 실엔진 검증 | 🟢/🔴 | LaH10 292-393K 재현; CoSn 차단 |
| 23 | CoSn 정밀 DOS | 🟠 | 레이트리밋, 값은 24가 커버 |
| 24 | CoSn 도핑 sweep(BZ) | 🟠 | 정렬에 ~4.72홀/cell(비현실), N(E_F)×3.26 |
| 25 | CoSn DFPT λ/Tc | 🟠 | 2-패스 필요·자성은 DFPT 안 막음(반증) |
| **26** | **QE 실DFT CsV3Sb5** | 🟢 | **ΔE=+0.92eV, 비자성 확정(0.01μB)** |
| 28 | flat-band@E_F 스크린 | 🟡 | MP API → RbOs2O6/CsOs2O6/LaRu2 + deck |
| **29** | **QE 실DFT RbOs2O6** | 🟠/🔴 | **flat band AT E_F(ΔE 첫 돌파)·ideal-PBE 자성(아티팩트 추정)** |

## 3. 실 DFT 3종 — 병목과 돌파

| 물질 | 격자 | flat-band ΔE | 자성 | 판정 |
|---|---|---|---|---|
| CoSn | Co-kagome | −0.4435 eV (깊음) | 0.43 μB ❌ | 자성+깊음 탈락 |
| CsV3Sb5 | V-kagome | +0.923 eV (깊음) | 0.01 μB ✅ | 깊이 탈락 |
| **RbOs2O6** | β-pyrochlore | **~AT E_F** (Os-5d +0.377, O2p/Os5d 혼성 |ΔE|<0.07, band39 E_F교차) | ideal-PBE ~5μB(아티팩트?) | **ΔE 축 돌파 · 자성 후속** |

**돌파**: RbOs2O6가 "flat band을 E_F에 정렬"이라는 캠페인이 못 찾던 레버를 처음 깸. ideal 고대칭 PBE 셀의
큰 모멘트는 실험적 비자성 6.3K 초전도체란 사실과 모순 → **SOC/비-PBE/rattling 왜곡 미반영 아티팩트일 가능성 높음.**
**자성이 아티팩트로 확인되면 = 지금까지 최고의 무냉각 RTSC base 후보.** (demiurge 후속.)

## 4. 응용 3-LANE (RTSC_05/06/07/19/20, 상세 원본 RTSC/LANES.md → git 이력)
무냉각 RTSC 하나면 세 응용을 동시에 연다: **호버보드**(상온 maglev) · **핵융합 자석**(REBCO 비용급감) ·
**UFO 호버크래프트**(자속고정 부상, 반중력 아님). RTSC_20: "냉각형 금지면 세 레인이 한 물질에 의존."

## 5. in-flight (이관 시점) — RTSC_27
- **RTSC_27 CsV3Sb5 DFPT λ/Tc** — anima aiden에서 진행 중(pass-1, ~8h+). 캠페인 첫 실측 DFPT Tc(실험 ~0.9–2.5K 대조용).
- 착지 시: λ/ω_log/Tc를 **demiurge RTSC_LEDGER로 직접 fold**. anima `RTSC/`는 이미 폐기되므로 anima측 재생성 없음.
  (CsV3Sb5는 이미 깊은 차선으로 탈락한 후보 → Tc는 파이프라인 검증값. demiurge가 QFORGE로 자체 재산출도 가능.)

## 6. 정직 메모 (campaign-wide)
- **양자(ANU)는 RTSC 발견에 미사용** — H_6026이 "양자는 미계산 물리의 오라클이 아님" 증명. 발견은 오직 실 DFT/QE.
- **MP `total_magnetization` 신뢰 불가** — CoSn을 0으로 보고하나 실 QE 0.43μB. 비자성은 반드시 nspin=2 SCF로 확인.
- 모든 수치 p7(실 QE 출력 파싱). summer rbfe·aiden 테넌트 전 fire에서 무손상 유지.

---
*원본 `RTSC/`(90파일)는 이 커밋 직전 git 이력 + demiurge 핸드오프에 완전 보존. 이후 RTSC 진행 = demiurge 소유.*
