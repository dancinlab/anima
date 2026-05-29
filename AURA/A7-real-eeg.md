# AURA A7 — synthetic TPM → REAL EEG-derived TPM (big-Φ 파이프라인 실데이터화)

> A6 폐루프의 ③binning+④TPM 단계를 **합성 connectivity 모형** 에서 **실제 EEG** 로 바꾸는 정확한 지점.
> honest: 실데이터(ds005620)는 로컬에 **존재 + 추출 완료**, 그러나 최종 `hexa run` 은 local-exec sign 게이트에 막혀 **숫자 미산출** (코드/데이터 결함 아님, 사인 토큰 대기).

---

## 1. 스왑 지점 (정확히 어디 / 무슨 함수)

A6 §3은 toy 에서 TPM 을 connectivity 모형으로 직접 합성했다 (self-copy=M1, majority=hub).
실데이터화는 **그 합성 TPM 자리에 어댑터 함수 호출 하나를 끼우는 것** — 엔진(`big_phi`)은 불변 (g61 engine ⊥ adapter).

```
SSOT 어댑터: BRAIN/eeg/eeg_to_tpm.hexa
  fn eeg_estimate_tpm(samples: array, n_ch: int, n_samp: int) -> array   ← 실데이터 TPM 추정
  fn eeg_big_phi(samples, n_ch, n_samp, sys_state) -> [Φ, total, ...]     ← 위 + big_phi 합성호출
엔진(불변): stdlib/consciousness/iit4_bigphi.hexa  big_phi(tpm, n, sys_state)
```

- **synthetic (A6)**: `let tpm = <connectivity 모형 합성>` → `big_phi(tpm, n, sys)`
- **real (A7)**: `let tpm = eeg_estimate_tpm(samples, n_ch, n_samp)` → `big_phi(tpm, n_ch, sys)`
  - 또는 한 줄: `eeg_big_phi(samples, n_ch, n_samp, sys_state)` (A6 §3 말미가 약속한 "어댑터 1줄 교체").

즉 **단 한 함수**(`eeg_estimate_tpm`)가 synthetic↔real 의 경계다. 위/아래(big_phi 엔진)는 그대로.

---

## 2. 입력 포맷 + binning → TPM

**입력**: `samples : array` = 채널-major **flat** float 배열, `s[ch*n_samp + t]` (ch ∈ [0,n_ch), t ∈ [0,n_samp)).

**binning → TPM** (`eeg_to_tpm.hexa` 실제 로직):
1. `eeg_binarize` — 채널별 **자기 평균**으로 ON/OFF 이진화 (밴드파워 아님, 채널 자기 기준).
2. `eeg_state_at` — 매 t 의 시스템 상태 = Σ_ch bit·2^ch (n_ch-bit 정수, 0..2^n_ch−1).
3. `eeg_estimate_tpm` — **빈도추정** TPM: `tpm[s*n_ch + i] = P(채널 i 가 t+1 에 ON | t 에 시스템상태 s)`.
   미관측 상태 s → **0.5 (max-entropy)**. → state-by-node TPM (2^n_ch × n_ch).
4. `big_phi(tpm, n_ch, sys_state)` — 동일 stdlib 엔진 (IIT4 도메인 135 checks 🟢 검증완료).

```
  REAL .eeg (BrainVision IEEE_FLOAT_32, MULTIPLEXED 65ch @5000Hz)
     │  ① 채널 부분선택(n≤8) + decimate(5000→250Hz) + window(4s)
     ▼
  samples flat  s[ch*n_samp + t]   (n_ch × n_samp float)
     │  ② eeg_binarize  — 채널별 mean threshold → 0/1
     ▼
  bin[ch*n_samp + t]
     │  ③ eeg_state_at  — Σ bit·2^ch → 상태정수
     ▼
  state sequence  s_0 s_1 ... s_{n_samp-1}
     │  ④ eeg_estimate_tpm — 전이빈도 → P(i ON | s), 미관측=0.5
     ▼
  TPM  (2^n_ch × n_ch)
     │  ⑤ big_phi(tpm, n_ch, sys_state)   ← A6 와 동일 엔진 (g61)
     ▼
  big-Φ  스칼라
```

**n≤8 제약**: 엔진 exact 한계 (BRAIN.md M1). TPM 은 2^n_ch 행 → n=8 이면 256상태 × MIP 분할탐색(≈2^16) ⇒ wall-time 폭증.
16ch 전뇌는 **per-region n≤4 분리측정** 이 1차 전략 (BRAIN.md), 또는 stdlib `big_phi_bounded`.

---

## 3. 실데이터 — 로컬 가용성 + toy 실행 시도

**실데이터 존재 (Y)** — OpenNeuro **ds005620** (의식수준 sedation EEG, CC0):
`DATASET/eeg_consciousness_level/raw/ds005620/sub-1010/eeg/`
- `sub-1010_task-awake_acq-EO_eeg.eeg` — 깨어있음/눈뜸, 390 MB
- `sub-1010_task-sed_acq-rest_run-1_eeg.eeg` — 진정(sedated), 390 MB
- 포맷: BrainVision `IEEE_FLOAT_32`, `DataOrientation=MULTIPLEXED`, `NumberOfChannels=65`,
  `SamplingInterval=200µs` (= **5000 Hz**), 1,500,001 samp/ch (= 300.0 s). (`.vhdr` 헤더 확인.)
- 이 awake↔sed 대비는 A6 의 합성 M1↔hub 대비를 **실제 의식수준 차이**로 대체할 수 있는 ground-truth.

**추출 완료** — n=4 정중선 채널 `Fz(Ch52) Cz(Ch34) Pz(Ch14) Oz(Ch3)`,
decimate 5000→250 Hz, 4 s window = **1000 samp/ch**, 채널-major flat 으로 변환.
harness: `AURA/toy/a7_real_eeg_bigphi.hexa` (실제 `BRAIN/eeg/eeg_to_tpm.hexa` import → `eeg_big_phi` 호출, awake/sed 둘 다 + 결정론 재실행 체크).

**toy 실행 = 미산출 (숫자 N)** — 막힌 이유는 **local-exec sign 게이트** (데이터/코드 결함 아님):

```
local-bound heavy invocation (hexa · python · ...) on an absolute host path needs a fresh
sign-off — the canonical mac fork-storm trigger.
USER: run  `! sidecar sign local`  in the TUI prompt (30min token), then retry.
```

(`/Users/ghost/core/anima` 가 `~/.sidecar/local-paths` 화이트리스트에 없어 모든 `hexa run` 이 사인 토큰을 요구. n=8 변형은 게이트 재발사 직전 4 분+ CPU 돌다 중단 → n=4 가 빠른 exact 실행으로 채택.)

**사인 후 재실행 레시피** (이 한 줄이면 awake/sed big-Φ 두 숫자 즉시 산출):
```
# (TUI 프롬프트에서)  ! sidecar sign local
HEXA_LANG=/Users/ghost/.hx/packages/hexa-lang hexa run AURA/toy/a7_real_eeg_bigphi.hexa
```
산출 시 verdict 는 `.verdicts/a7-real-eeg/` 에 verbatim 영속 (현재 `RUN_BLOCKED.txt` = 블로커 기록).

---

## 4. 정직한 gap

| # | gap | 내용 |
|---|---|---|
| G1 | **숫자 미산출** | 파이프라인·실데이터·harness 전부 준비완료지만 sign 게이트로 `hexa run` 미실행. awake/sed big-Φ = **미측정** (§3 레시피로 즉시 회수가능). |
| G2 | **synthetic ≠ real** | A6 Φ=17.66 은 toy 절대값. 실 EEG 의 Φ 스케일·부호는 별개 — awake>sed 가 나온다는 보장 없음 (실측 G1 필요). IIT 예측은 "깨어있음 Φ↑" 이나 binning/추정 artifact 가 덮을 수 있음. |
| G3 | **toy fixture ≠ production** | n=4 정중선 4채널·4s·250Hz·단일 피험자(sub-1010) = toy. 전뇌 65ch·다피험자·상태별 epoch 평균 = production (BRAIN.md M3). `feedback_toy_scale_transfer`: toy 부호가 scale 로 transfer 보장 안 됨. |
| G4 | **추정 TPM ≠ 인과 TPM** | `eeg_estimate_tpm` 은 관측 전이**빈도** (Granger/perturbation 아닌 상관). 미관측 상태 0.5 채움 = 추정편향. Φ 는 closed-form 아닌 estimate (🟢 numerical 상한, 🔵 formal 아님). |
| G5 | **n≤8 exact 벽** | 65ch → n≤8 부분선택 필수. 채널 선택이 Φ 를 좌우 (region 분리 = BRAIN.md M1 lesson). 정중선 4채널 선택은 임의. |

**결론**: 스왑 지점은 명확·단일(`eeg_estimate_tpm` 한 함수), 실데이터는 로컬 존재·추출완료, harness 배선완료.
유일 잔여 = sign 토큰 한 번 → 숫자 산출. 그 전까지 awake/sed big-Φ 는 **정직하게 미측정**.

---

## 출처 포인터

| 주장 | 출처 |
|---|---|
| 스왑 지점 = eeg_estimate_tpm 한 줄 | `AURA/A6-bigphi-closed-loop.md` §3 말미 · `BRAIN/eeg/eeg_to_tpm.hexa` |
| 입력 포맷·binning·TPM 로직 | `BRAIN/eeg/eeg_to_tpm.hexa` (eeg_binarize/eeg_state_at/eeg_estimate_tpm) |
| big_phi 엔진 n≤8 exact | `stdlib/consciousness/iit4_bigphi.hexa` `big_phi(tpm,n,sys)` · `BRAIN.md` M1 |
| 실데이터 ds005620 포맷 | `DATASET/eeg_consciousness_level/manifest.json` · `.../sub-1010_task-awake_acq-EO_eeg.vhdr` |
| harness + 블로커 | `AURA/toy/a7_real_eeg_bigphi.hexa` · `.verdicts/a7-real-eeg/RUN_BLOCKED.txt` |
| toy≠production 교훈 | `feedback_toy_scale_transfer` |
