# AURA-HEADMODEL — 실 MNE head-model lead-field로 toy ground-truth 검증

> 🟡 **real head-model**. fsaverage 3-layer BEM forward (가우시안도 구체도 아닌 **실제 삼각메시 두상**).
> $0, MNE 1.12.1 (pool ubu-1 사전설치, pip/pod 불필요). verdict 원문 = `verify/mne_real_leadfield.txt`.

## 일반인 설명 — "진짜 머리 모양으로 직접 재본다"

```
🗺️ 두피 전극으로 뇌 속 신호 위치를 되찾는 문제 — 마지막 ground-truth
- AURA의 C5~C17 toy는 전부 "가우시안 흐림" 가정.
- C18은 한 단계 올라가 "3층 구체(sphere)" 물리.
- 하지만 구체도 진짜 머리가 아니다 — 두개골 구멍·곡률·비대칭이 없다.
- MNE는 FreeSurfer 평균 두상(fsaverage)을 삼각형 메시로 깎아 뇌/두개골/두피
  3층 경계요소(BEM)로 전기를 푼다 = 실측에 가장 가까운 비침습 lead-field.
- 이게 paper가 NOT-MEASURED로 남긴 #1 ground-truth. toy 3대 결론이 살아남나?
```

## 기술 설명 — fsaverage 3-layer BEM forward

- `mne.datasets.fetch_fsaverage()` → FreeSurfer 평균 두상 (763MB, 1회).
- BEM: `fsaverage-5120-5120-5120-bem-sol.fif` — 뇌/두개골/두피 각 5120 삼각형 경계요소.
- 전극: `standard_1005` 표준 고밀도 EEG 몽타주 **343채널**.
- 소스: 피질 표면 `oct5` 2052 dipole + **volume source space 1821 voxel**(피질하).
- lead-field = `mne.make_forward_solution(...)` gain matrix **(343 × 2052)**.
- **두 측도** (방법론 발견에 따른 의도적 이중측정):
  - **M1 = ||G[:,s]||** 소스별 두피 신호 크기 — 검출가능성을 결정하는 물리량(결정론·well-conditioned).
  - **M2 = R² active-source recovery** ridge inverse — toy와 동일 추정기(8-seed·snr20dB·K=6).

## 🎯 3대 toy 결론 — 실 MNE 판정

### (1) 심부 < 피질 (깊이 벽) — ✅ 방향 확증

| 측도 | 얕음 | 깊음 | 감쇠 |
|---|---|---|---|
| **||G|| 신호크기** (피질) | 1.087e3 | 8.568e2 | **×1.27 감소** |
| R²(M=128) (피질) | 0.040 | 0.000 | 노이즈바닥 붕괴 |

피질 깊이 따라 신호크기 단조감소(×1.27). 방향(심부<피질)은 가우시안 toy(C15)·
3-shell 구체(C18)와 일치 → 깊이 벽은 **실재 물리경계**. C16(피질 도달)·C17(심부 불가) 생존.

### (2) 전극 포화 — ✅ C10 확정: 실 두상서도 **미포화**

| M | R²_real | Δ | 포착 ||G|| |
|---|---|---|---|
| 16 | 0.005 | | 2.03e2 |
| 32 | 0.007 | +0.002 | 2.90e2 |
| 64 | 0.014 | +0.007 | 4.17e2 |
| 128 | 0.021 | +0.007 | 5.91e2 |
| 256 | 0.026 | +0.004 | 8.41e2 |

전극 늘릴수록 R²·포착신호 둘 다 256ch까지 단조증가. λ-sweep서도 M32→M256 climb가
well-conditioned λ 전부 양수(λ1e-1 +0.010, λ1e-2 +0.018). 실 BEM은 3-shell·C10
지수커널과 동류(미포화), **C5 가우시안 strawman**(평탄)과 다름. → **"전극포화=가우시안
전용 인공물" C10 주장이 실제 메시 두상으로 확정.**

### (3) 깊이 벽 가파름 — 실 두상이 훨씬 완만 (방향만 robust)

### (⚠) 방법론 발견 — toy R² 절대값은 실 두상으로 transfer 안 됨

**toy의 simple-ridge R² 측도는 실 BEM gain으로 전이되지 않는다.** 실 ill-conditioned
343×2052 gain서 ridge-R²는 well-conditioned λ(1e-2)서도 노이즈바닥(0.0~0.05), λ 낮추면
음수로 붕괴(λ1e-3 → −0.05/−0.34, λ1e-4 → −0.26/−0.34). toy가 보고한 0.2~0.8 R²는
**매끄러운 합성 커널의 인공물** — 실 두상 simple-ridge서 살아남지 못함 (cf MEMORY:
toy-scale는 production scale로 자동 transfer 안 됨). 실 두상의 robust 신호는 gain-column
**크기**(||G||)이지 toy R²가 아니다. MNE-native dSPM PSF localization-error 경로는 시도했으나
MNE 1.12.1 `resolution_metrics` loose-orientation 인덱싱 버그(IndexError)로 deferred.

## 📊 실 MNE vs 가우시안 vs 3-shell 3열 대조표

| 축 | 가우시안 toy (C5/C15) | 3-shell 구체 (C18) | **실 MNE BEM (본 라운드)** | 판정 |
|---|---|---|---|---|
| 모델 본질 | exp(−d²/2σ²) blur 가정 | Ary1981 해석 구체 | **fsaverage 삼각메시 3층 BEM** | 실측 최근접 |
| 전극 위치 | 추상 1D 각도 | 추상 1D 각도 | **실 standard_1005 343ch** | 실측 |
| 깊이 방향 | 피질>심부 | 피질>심부 | **피질>심부** (||G|| & R²) | ✅ 3모델 일치 |
| 깊이 감쇠 | R² ×8.4 (0.82→0.10) | R² ×15.4 (0.239→0.016) | **||G|| ×1.27** (1.09e3→8.57e2) | ⚠ 다른 축·실 두상 완만 |
| 전극 포화 | **포화** (Δ→+0.022) | 미포화 (Δ→+0.093) | **미포화** (R²·||G|| 256ch까지↑) | ❌ 가우시안만 인공물 |
| 절대 R² | 0.1~0.8 | 0.02~0.4 | **0.0~0.05** (simple ridge 바닥) | ⚠ toy R² transfer 실패 |

## 결론 — toy 정성 방향은 살아남고, toy 절대수치는 실 두상서 무너진다

- ✅ **심부<피질**: 3모델 방향 robust (실 두상 ||G|| ×1.27 감소). 깊이 벽 실재.
- ✅ **전극 미포화**: C10 확정 — 가우시안만 포화하는 인공물.
- ⚠ **깊이 벽 가파름**: 실 두상 신호크기 축서 매우 완만(×1.27); toy R² 비(×8.4/×15.4)는
  매끄러운 커널 inverse 행태이지 실 두상 신호물리 아님.
- ⚠ **toy R² 절대값 비전이**(load-bearing): simple-ridge R²는 실 BEM서 노이즈바닥/음수.
  toy 0.2~0.8은 합성 커널 인공물. 정성(방향·미포화)이 핵심, 절대수치는 toy-specific.

## NOT-MEASURED (정직)
- 피험자별 개인 MRI 해부 (fsaverage = FreeSurfer **평균** 두상).
- 두개골 전도도 이방성 (radial≠tangential — MNE BEM 기본 등방).
- MNE-native dSPM/PSF resolution 측도 (MNE 1.12.1 `resolution_metrics` 버그).
- volume(피질하) 깊이는 비단조(×0.96, cortical-centroid 기준 양반구 혼입) — 피질하 단조 주장 안 함.
- 실 BEM 절대 R²는 proper sparse/Bayesian inverse 필요(toy ridge 아님).

## 양방향 sibling
- 부모: [AURA-HEADMODEL](AURA-HEADMODEL.md) · [AURA](../AURA.md)
- 검증 대상: [C10](../C10-gap-closure-levers.md)(전극포화=가우시안 인공물 — **실 두상 확정**)
  · [C15](../C15-depth-wall-terminal.md)(깊이 벽 — 방향 확증, 실 두상 완만)
  · [C18 / SPHERE-VALIDATION](SPHERE-VALIDATION.md)(3-shell 구체 — 실 두상이 구체보다 완만)
  · [DEPTH-3SHELL-CORRECTION](../AURA-DEPTH/DEPTH-3SHELL-CORRECTION.md)
