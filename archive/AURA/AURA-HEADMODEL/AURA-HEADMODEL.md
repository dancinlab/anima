# AURA-HEADMODEL — current state

@title: 🗺️ AURA-HEADMODEL — "진짜 머리 지도" (real head-model lead-field validation)

@goal: MNE/OpenMEEG 실 두상 lead-field로 C5~C17 toy(가우시안-blur)의 깊이감쇠·전극포화를 실측 검증 — C10이 "전극포화는 가우시안 전용 인공물"임을 보였고 C14에서 real head-model이 결정적이라 판정. 모든 C축 toy의 ground-truth 검증 도메인.

## 진행 (milestones)

- [x] (app ✅) MNE/OpenMEEG 3-shell·FEM lead-field 구축 — 가우시안-blur 대체
- [x] **🟡 real head-model — 실 MNE fsaverage BEM lead-field 측정** ($0, MNE 1.12.1 pool ubu-1 사전설치): 가우시안도 구체도 아닌 **삼각메시 3층 BEM** forward (gain 343×2052, standard_1005 343ch + oct5 피질 2052 + volume 1821 voxel). 3대 toy 결론 실 두상 검증 — (1) 심부<피질 ✅ 방향확증(||G|| 1.09e3→8.57e2 ×1.27 감소, R² 깊이서 노이즈바닥) (2) 전극포화=가우시안 인공물 ✅ **확정**(실 두상 미포화, R²·||G|| 256ch까지 단조↑, λ-robust) (3) ⚠ **toy R² 절대값 비전이 발견**: simple-ridge R²는 실 ill-conditioned BEM서 노이즈바닥(0.0~0.05)/저-λ 음수 — toy 0.2~0.8은 매끄러운 합성커널 인공물(cf toy-scale 비전이). paper NOT-MEASURED #1 ground-truth 닫음. → `MNE-REAL-VALIDATION.md`·`verify/mne_real_leadfield.txt`
- [x] C10 strawman 검증 — **C10 SUPPORTED**: 3-shell 구체 lead-field(Ary1981, $0 numpy)서 전극 미포화(R² 0.19→0.40 계속 상승), 가우시안만 평탄 → "전극포화=가우시안 인공물" 확증. **실 MNE BEM서 확정**(위 milestone — 실 두상 R²·||G|| 256ch까지 단조증가). 깊이 방향 일치, 두개골비 1/20~1/80 평탄. → `SPHERE-VALIDATION.md`·`verify/sphere_leadfield.txt`
- [x] C15 깊이 벽 실측 — 3-shell 구체 물리(Ary1981 radial-dipole, $0 numpy)서 피질표면→심부핵 감쇠곡선 실측: R² 0.239→0.016 (×15.4) → [DEPTH-3SHELL-CORRECTION.md](../AURA-DEPTH/DEPTH-3SHELL-CORRECTION.md) (PR#1514/1517). ⚠ 비구형/tangential dipole 잔여 = **실 MNE BEM서 측정**(위 milestone — 실 두상 깊이 신호크기 ×1.27 매우 완만, 방향만 robust; toy R² 비 ×8.4/×15.4는 매끄러운 커널 inverse 행태)
- [x] C11 현실 prior 복원율 — 실 두상선 piece 측정: 실 MNE BEM(평균 두상 fsaverage)서 깊이별 ||G||·R² 실측. ⚠ 발견: toy oracle 0.80 류 절대 R²는 실 BEM서 simple-ridge로 재현 안 됨(노이즈바닥). 잔여=proper sparse/Bayesian inverse·피험자별 개인 MRI·두개골 이방성.

## deferred (다음 라운드)
- proper sparse/Bayesian inverse(절대 R² 의미화) · 피험자별 개인 MRI forward (fsaverage=평균 두상) · 두개골 전도도 이방성 · MNE dSPM PSF resolution(MNE 1.12.1 버그) · 측정 EEG inverse 벤치마크

## 양방향 sibling
- 부모: AURA(`./AURA/AURA.md`) · 그룹: 📡 모달리티
- 자매: AURA-RTSC-MEG · AURA-ENDOVASC · AURA-CORTEX · AURA-NAV · AURA-DEEP · AURA-TFUS · AURA-WEARABLE · AURA-MED

## 세부분류 (app 세부트리)

- `app/spec.md` — 앱 명세(일반인+기술)
- `app/leadfield_validator.py` — 실동작 toy (검증됨)
- `app/mne_leadfield.hexa` — 실 MNE BEM lead-field companion (logic mirror)
- `verify/leadfield_validator.txt` · `verify/sphere_leadfield.txt` · `verify/mne_real_leadfield.txt` — verdict
- `MNE-REAL-VALIDATION.md` — 실 MNE vs 가우시안 vs 3-shell 3열 대조 + 결론
- 다음: proper sparse inverse · 피험자별 개인 MRI forward · 두개골 이방성
