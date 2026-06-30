# AURA-HEADMODEL.log

## 2026-05-30 — 도메인 신설 (AURA 트리 하위)
- AURA C16/C17 역량지도 + demiurge archive 기반 분리

## 2026-05-30 — 🟡 실 MNE head-model lead-field 측정 (real ground-truth)
- MNE 1.12.1 (pool ubu-1 사전설치, $0 — pip/pod 불필요) fsaverage 3-layer BEM forward.
- gain 343×2052 (standard_1005 343ch + oct5 피질 2052 + volume 1821 voxel). 가우시안도 구체도 아닌 실 메시.
- 3대 toy 결론 실 두상 검증: 심부<피질 ✅ 방향확증(||G|| ×1.27 감소) · 전극포화=가우시안 인공물 ✅ 확정(미포화 R²·||G|| 256ch↑) · ⚠ toy R² 절대값 비전이 발견(simple-ridge R² 실 BEM서 노이즈바닥 0.0~0.05/저-λ 음수).
- 정직: toy 0.2~0.8 R²는 매끄러운 합성커널 인공물(cf toy-scale 비전이). robust 신호=gain-column ||G|| magnitude. dSPM PSF는 MNE 1.12.1 resolution_metrics 버그로 deferred.
- paper NOT-MEASURED #1 ground-truth 닫음. → MNE-REAL-VALIDATION.md · verify/mne_real_leadfield.txt
