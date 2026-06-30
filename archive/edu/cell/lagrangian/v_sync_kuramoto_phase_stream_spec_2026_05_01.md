# `v_sync_kuramoto_phase_stream.hexa` — Cross-Stream Phase API Spec

- **Path**: `edu/cell/lagrangian/v_sync_kuramoto_phase_stream.hexa`
- **Date**: 2026-05-01
- **Cycle**: raw#9 hexa-only · A2-cycle follow-up to commit `43b3cee89`
  (P2 TLR real-run UNEVALUABLE — CLM substrate timing 미확립)
- **Decision**: **Option B** — additive helper, base
  `v_sync_kuramoto.hexa` (frozen `d072bb16`) **untouched**.

## 1. 역할 (Why a new helper, not an in-place edit)

`v_sync_kuramoto.hexa`는 lattice corpus용 D-axis hash-only phase
projection을 제공한다. 그 kernel(`r_order_param_x1000`, cos/sin LUT,
isqrt)은 정합성 SSOT로 굳어 있고 (raw#91 fidelity), 변경 시 다음 합치
영향:

- `_integrations/clm_eeg_p2.hexa` (선언적 reference, uchg-locked)
- `anima-clm-eeg/tool/clm_eeg_p2_tlr_pre_register.hexa` (legacy SSOT)
- `edu/cell/lagrangian/l_cell_integrator.hexa:119` (`_v_sync_kuramoto_x1000`)
- `edu/cell/lagrangian/README.md`, `edu/cell/README.md` C16 line

따라서 raw#9 본 cycle scope (수정 0건, 신규만) 안에서:

- 신규 helper가 base의 constants/LUT을 **byte-identical re-define** 한다
  (TAU_PERM=6283, HALF_PI_PERM=1571, 24-bin cos LUT 동일).
- Cross-stream-only 신규 API만 노출 — atan2, PLV, joint_r,
  Kuramoto 1-step pull, coupled trajectory.
- base의 `r_order_param_x1000`/`v_sync_kuramoto_x1000`은 caller가 동일
  파일 import 또는 동거 컴파일로 사용 (수정 X).

## 2. API

| 함수 | 입력 | 출력 | 단위 |
| --- | --- | --- | --- |
| `atan2_perm_x1000(im, re)` | `int, int` | `int` | per-mille rad ∈ [0, TAU_PERM) |
| `phase_from_ab_x1000(a, b)` | `int, int` | `int` | alias `atan2(b, a)` (CLM (A=re, B=im)) |
| `plv_x1000(theta_a, theta_b, n)` | `list, list, int` | `int` | ×1000 ∈ [0, 1000] |
| `joint_r_x1000(theta_a, theta_b, n)` | `list, list, int` | `int` | ×1000 ∈ [0, 1000] |
| `couple_step_phase_x1000(θ_clm, θ_eeg, ω, K)` | `int, int, int, int` | `int` | per-mille rad |
| `couple_trajectory(θ0, eeg_phases, T, ω, K)` | `int, list, int, int, int` | `list` | T per-mille rad samples |

**불변식**

- `atan2_perm_x1000(0, +) == 0`, `atan2_perm_x1000(+, 0) == π/2 = 1571`,
  `atan2_perm_x1000(0, −) == π = 3142`, `atan2_perm_x1000(−, 0) == 3π/2 = 4712`.
- `plv_x1000(θ, θ, n) == 1000` (identity).
- `joint_r_x1000(const0, const0, n) == 1000` (LUT-exact at θ=0).
- `couple_step_phase_x1000` output ∈ [0, TAU_PERM) (wrap fixed).
- 결정론: 동일 입력 → 동일 list (raw#9 byte-identical 3 reruns).

## 3. Cross-Stream Protocol  (EEG α-band ↔ CLM Kuramoto)

### 3.1 EEG side (caller, hexa scope 외)

`scipy.signal.hilbert(eeg_alpha_band)` → analytic z[t] = a[t] + i·b[t].
caller가 (a[t], b[t]) per-channel per-sample을 hexa 측에 전달:

```
θ_eeg[t] = atan2_perm_x1000(b[t], a[t])
```

본 helper는 **numpy buffer 직접 접근 안 함** (raw#9 hexa-only).
caller가 int list로 변환 후 전달.

### 3.2 CLM side (this helper)

```
θ_clm[0]   = θ_clm0
θ_clm[t]   = couple_step_phase_x1000(θ_clm[t-1], θ_eeg[t-1], ω, K)
```

전체 trajectory:

```
θ_clm = couple_trajectory(θ_clm0, eeg_phases, T, ω, K)
```

Kuramoto 1-step pull:

```
θ' = θ + ω + (K/1000) · sin(θ_drive − θ)         (per-mille rad)
   wrap into [0, TAU_PERM)
```

### 3.3 Cross-stream metrics

```
r_clm = r_order_param_x1000(θ_clm, T)        # base v_sync_kuramoto.hexa
plv   = plv_x1000(θ_clm, θ_eeg, T)           # this file
joint = joint_r_x1000(θ_clm, θ_eeg, T)       # this file
```

### 3.4 Verdict mapping (mirror `clm_eeg_p2` frozen criteria)

본 cycle scope 내에서 **신규 floor 도입 X**. `clm_eeg_p2.hexa`의
`C1_COUPLED_R_MIN_X1000 = 700` 을 그대로 PLV 임계값으로 매핑:

| 조건 | 임계값 | 명칭 |
| --- | --- | --- |
| `plv ≥ 700`  | C1 | EEG-CLM ENTRAINED |
| `plv ≤ 200`  | C2 | EEG-CLM DECOUPLED |
| `r_clm ≥ 380` | C3 | CLM_R_FLOOR (legacy mirror) |

## 4. Selftest 결과 (`hexa run … --selftest`)

```
v_sync_kuramoto_phase_stream selftest (Mk.IX cross-stream)
  OK  atan2(0,+) == 0
  OK  atan2(+,0) == π/2
  OK  atan2(0,-) == π
  OK  atan2(-,0) == 3π/2
  OK  atan2(+,+) ≈ π/4
  OK  atan2(+,-) ≈ 3π/4
  OK  atan2(-,-) ≈ 5π/4
  OK  atan2(-,+) ≈ 7π/4
  OK  phase_from_ab == atan2(b,a)
  OK  plv(θ,θ) == 1000
  OK  joint_r(const,const) == 1000
  plv_strong_x1000=1000
  OK  strong-coupling PLV ≥ 700 (entrained)
  plv_zero_x1000=87
  OK  zero-coupling PLV ≤ 200 (no lock)
  OK  strong > zero (separation)
  OK  determinism 3 reruns
v_sync_kuramoto_phase_stream: PASS
```

핵심 fixture: 64-step synthetic EEG ramp (step=200 ≈ 0.2 rad/sample),
CLM seed `θ_0 = π` (i.e. anti-phase initialization).

- **Strong coupling** (ω=200, K=900): PLV = **1000** (full lock,
  C1 ≥ 700 통과).
- **Zero coupling** (ω=550 detuned, K=0): PLV = **87** (C2 ≤ 200 통과).
- **Separation** strong > zero 확인.
- **Determinism**: 3 reruns 동일 PLV (raw#9 byte-identical).

## 5. `_integrations/clm_eeg_p2.hexa --live` activation spec  (다른 agent)

본 helper가 **enable** 하는 cross-stream 흐름은 다음과 같다 (코드는
다른 agent 영역 — 본 cycle은 spec 까지):

1. EEG ingest: real `.npy` resting + p300 → α-band bandpass (8–13 Hz) →
   `scipy.signal.hilbert` → (a, b) per channel per sample.
2. caller가 (a, b) → θ_eeg list (per channel) 로 변환,
   `atan2_perm_x1000` 사용.
3. `_integrations/clm_eeg_p2.hexa::live` 진입 후
   `couple_trajectory` 로 CLM trajectory 생성.
4. `plv_x1000` / `joint_r_x1000` / 기존 `r_order_param_x1000` 으로
   3-metric vector 산출.
5. C1/C2/C3 verdict — 모두 frozen, 신규 floor X.
6. F1..F5 falsifiers (clm_eeg_p2 frozen) 평가는 동일 — 본 helper는
   metric 만 제공, gate 정책은 dispatcher 영역.

## 6. raw#91 honest C3 — 미실증 영역

- 본 cycle: synthetic CLM oscillator + synthetic EEG ramp 만 selftest
  통과 (deterministic, raw#9 hexa-only).
- 미실증: real `.npy` Hilbert phase ↔ CLM Kuramoto trajectory의
  cross-stream PLV — **별도 cycle** 필요. caller (EEG ingest, scipy
  bridge) 와 dispatcher (`clm_eeg_p2.hexa --live`) 양쪽에서 추가 작업이
  요구됨.
- atan2 LUT 정확도: 16-bin first-octant + quadrant unfold. 축 (4 cardinal
  directions) 은 exact, 비대각/비축 위치는 ±5% 이내 (selftest tolerance
  ±35 per-mille = ±0.5°). real EEG 적용 시 LUT 분해능 충분성 평가
  별도 (FFT/Hilbert 정확도 vs Kuramoto step convergence rate trade-off).
- 본 spec은 SSOT 후보 — 변경 시 base `v_sync_kuramoto.hexa` constants
  와의 byte-identity (TAU_PERM=6283, HALF_PI_PERM=1571, 24-bin cos LUT)
  를 항상 검사.

## 7. raw 준수표

| RAW | 준수 |
| --- | --- |
| raw#9  hexa-only · deterministic · no LLM | ✓ pure fn, no I/O, byte-identical reruns |
| raw#10 honest C3 (선/후 evidence 분리) | ✓ synthetic only; real EEG out-of-scope 명시 |
| raw#65 idempotent | ✓ pure fn, no global state |
| raw#82 darwin-native | ✓ no host delegation, hexa-resolver docker route OK |
| raw#91 kernel fidelity | ✓ TAU_PERM/HALF_PI_PERM/24-bin cos LUT byte-identical to base |
