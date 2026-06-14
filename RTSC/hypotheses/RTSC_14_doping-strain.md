---
id: RTSC_14
slug: doping-strain
title: kagome 도핑+strain 처방 — 전자도핑 x≈0.6(flat band를 E_F로)+적정 strain/압력 ε≈0.14(CDW 억제)로 CsV3Sb5형서 예측 Tc~184-200K(관측 2.5K→큰 점프). 상온엔 strain-detune로 미달, sweet spot 존재.
domain: rtsc kagome doping strain CDW-suppression CsV3Sb5 material-engineering
status_grade: 🟢 (concrete prescription, ~200K predicted) / 🟠 (room-temp capped by strain-detune; DFT 미검증)
since: 2026-06-14
verification_method: phenomenological doping/strain model (E_F-alignment + CDW suppression) + ANU search; p7 $0
sister: RTSC_12, RTSC_13
verdict: 🟢 전자도핑 x≈0.6(ΔE 0.30→0.02eV E_F 정렬)+strain ε≈0.14(CDW supp 0.20→0.98) → 예측 Tc≈184-200K(관측 2.5K 대비 ~80배). CsV3Sb5 압력→CDW억제→SC증가 실측과 방향 일치. 🟠 상온(300K)엔 strain-detune 트레이드오프로 미달; 더 높은 Tc=native ΔE 작은/⟨g⟩ 큰 base 물질 필요.
---
# RTSC_14 — kagome 도핑+strain 처방 (E_F 정렬 + CDW 억제)
> **가설.** CsV3Sb5형 kagome를 전자도핑(flat band를 E_F로)+strain/압력(CDW 억제)하면 SC Tc가 급등한다.
## 측정 (rtsc_doping_strain.py · ANU paid)
격자: x=0.6서 ΔE→0(flat band 정렬) → Tc 58K(dry); +strain ε0.05-0.1로 CDW 억제 → **192-200K**. ANU 최적 x≈0.60·ε≈0.14 → ΔE 0.022eV, supp 0.98, **Tc≈184K**.
## 결론
🟢 **구체 처방 확보** — 전자도핑으로 flat band를 E_F에 정렬(ΔE 0.30→0.02eV) + 적정 strain/압력으로 CDW 억제(supp 0.20→0.98) → CsV3Sb5형서 예측 **~184-200K**(관측 2.5K의 ~80배). 실제 CsV3Sb5 가압 실험(CDW 억제+SC 돔 증가)과 방향 일치. 🟠 **상온(300K)엔 미달** — strain 과하면 flat band 재이탈(detune)이라 캡. 상온 도달엔 native ΔE 작고 ⟨g⟩ 큰 base 물질(RTSC_13 표적) 필요. 다음: QE DFT로 도핑/strain별 ΔE·CDW 정밀.
verdict: `RTSC/verdicts/doping_strain.txt`
