---
id: RTSC_15
slug: base-material
title: base 물질 역설계 — 가장 깨끗한 플랫폼 = CoSn(비자성·CDW無 kagome): E_F 정렬(전자도핑)만으로 ~237K 예측, strain 불필요. pyrochlore형(⟨g⟩1.40)이 상온 프런티어. CsV3Sb5보다 적은 공정.
domain: rtsc kagome CoSn pyrochlore base-material reverse-design clean-platform
status_grade: 🟢 (clean platform CoSn → ~237K with only E_F doping) / 🟠 (room-temp needs native ΔE→0 + higher ⟨g⟩; DFT 미검증)
since: 2026-06-14
verification_method: clean-platform scorecard (native ΔE, ⟨g⟩, competing-order-free, U) + E_F-aligned Tc; p7 $0 (🟡 lit)
sister: RTSC_13, RTSC_14, RTSC_12
verdict: 🟢 깨끗한 base 역설계 — CoSn(비자성·CDW無, ⟨g⟩1.25)이 경쟁질서 최저 → E_F 정렬(도핑)만으로 예측 ~237K(strain 불필요, RTSC_14 CsV3Sb5 ~200K보다 적은 공정). pyrochlore-metal(⟨g⟩1.40) 최고 quantum-metric=상온 프런티어. 🟠 상온(300K)엔 native ΔE 더 작고 ⟨g⟩ 더 큰 base 필요.
---
# RTSC_15 — base 물질 역설계 (깨끗한 플랫폼)
> **가설.** 경쟁질서 없는 깨끗한 flat-band base를 고르면 E_F 정렬만으로 최소 공정에 고-Tc 도달.
## 측정 (rtsc_base_material.py)
| base | family | ⟨g⟩ | native ΔE | Tc(E_F정렬) |
|---|---|---|---|---|
| **CoSn** | kagome (clean) | 1.25 | 0.20 | **237K** |
| pyrochlore-metal | pyrochlore | 1.40 | 0.10 | 195K |
| Ni3In | kagome | 0.90 | 0.10 | 98K |
| CsV3Sb5 | kagome (CDW) | 1.33 | 0.30 | 72K |
| ideal(ΔE0+clean+⟨g⟩1.4) | — | 1.40 | 0.00 | 330K |
## 결론
🟢 **깨끗한 base가 열쇠** — CoSn(비자성·CDW無)은 억제할 경쟁질서가 없어 **E_F 정렬(전자도핑)만으로 ~237K** 예측, RTSC_14(CsV3Sb5 도핑+strain ~200K)보다 공정 단순. quantum metric 최고는 pyrochlore형(⟨g⟩1.40)=상온 프런티어. 🟠 **상온(300K)엔 native ΔE 더 작고 ⟨g⟩ 더 큰 base** 필요(이상 base=330K). 핵심 처방: 깨끗한 base(CoSn/pyrochlore) + E_F 도핑. 다음: QE DFT로 CoSn 도핑 밴드 확정.
verdict: `RTSC/verdicts/base_material.txt`
