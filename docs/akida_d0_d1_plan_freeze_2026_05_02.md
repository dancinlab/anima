# AKIDA D+0 / D+1 Plan Freeze — pre-arrival deployment freeze + tension-modulated ADM polarity bias extension

@english-only-exempt(reason="anima research analysis language preservation per user primary language")

- **Date**: 2026-05-02
- **Agent**: AKIDA D+0/D+1 plan freeze
- **Mission**: AKIDA AKD1000 dev kit 도착 시점 D+0/D+1 deployment plan 사전 동결, 6 AKIDA-dependent axes (N-2/3/4/5/7/8) critical-path graph, tension-modulated ADM polarity bias spec extension, 사용자 1-page deployment checklist, 5 raw#71 falsifier preregistration
- **Trigger**: #92 권장 #2 — "AKIDA D+0/D+1 plan freeze"; AKIDA AKD1000 dev kit ORDERED ($1,495 capex paid 2026-04-29), arrival ETA pending vendor logistics
- **Race-isolated dirs**:
  - `state/akida_d0_d1_plan_freeze_2026_05_02/{spec_manifest,d0_checklist,d1_runbook,axes_critical_path,falsifier_F_AK_preregister}.json`
  - `docs/akida_d0_d1_plan_freeze_2026_05_02.md` (this file)
- **Did NOT touch**: `state/n_substrate_n2_prep_2026_05_01/*` (sister N-2 spec), `state/strategic_clm_eeg_akida_tension_2026_05_02/*`, alpha pod, H100 fleet
- **Sister docs**: `docs/n_substrate_n2_eeg_akida_spike_pipeline_spec_2026_05_01.md`, `docs/n_substrate_n3_clm_akida_phi_spec_2026_05_01.md`, `docs/n_substrate_n7_akida_qrng_spike_spec_2026_05_01.md`, `docs/n_substrate_n8_akida_sim_limit_integration_2026_05_01.md`, `docs/strategic_clm_eeg_akida_tension_link_2026_05_02.md`, `docs/akida_dev_kit_evaluation_2026-04-29.md`

---

## §0 TL;DR

AKIDA AKD1000 도착 시점 deployment 가 **vendor logistics blocker** 외에 anima-side 결함이 전혀 없도록 D+0~D+7 plan 을 사전 동결한다. 본 doc 은:

1. **6 AKIDA-dependent axes** (N-2/3/4/5/7/8) 의 dependency graph 를 ASCII 로 고정 — N-2 가 single prerequisite
2. **D+0** (도착 day): 5-step hardware unboxing + RPi5 SDK install checklist
3. **D+1**: N-2 first run (synthetic 16ch EEG → ADM → AKIDA dense uint8 raster → `model.forward`), 6 G-D selftest gate
4. **§4 tension-modulated ADM polarity bias extension** — anima-specific spec extension, F-AK-4 falsifier-bound
5. **D+2~D+7 cascade**: N-3 / N-7 / N-4 / N-5 / N-8 순차 unblock
6. **5 falsifier (F-AK-1~F-AK-5)** raw#71 preregister
7. **Honest C3 9건** (raw#10) — vendor ETA, ARM64 wheel, SDK 변경, anima-specific extension 등

본 plan 은 **spec freeze only** ($0 budget, hardware blocker). 도착 즉시 D+0 checklist 실행, 1-page printable §7 별도 제공.

---

## §1 6 AKIDA-dependent axes — dependency graph

```
                         ┌──────────────────────────────────┐
                         │  N-2  EEG → AKIDA spike pipeline │
                         │       (foundation, prerequisite) │
                         └──────────────────────────────────┘
                                     │
            ┌─────────────────┬──────┴───────┬──────────────────┬───────────────┐
            │                 │              │                  │               │
            ▼                 ▼              ▼                  ▼               ▼
    ┌───────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
    │  N-3 CLM ×    │ │  N-7 AKIDA × │ │  N-4 3-axis  │ │  N-5 3-axis  │ │  N-8 AKIDA × │
    │  AKIDA Φ      │ │  QRNG noise  │ │  Landauer    │ │  GWT broad-  │ │  SIM-우주    │
    │  (last-layer  │ │  floor       │ │  energy      │ │  cast        │ │  limit       │
    │   projection) │ │              │ │              │ │              │ │  saturation  │
    └───────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
            │                 │              │                  │               │
            └────────── all 5 unblock at D+1 + N-2 PASS ────────┴───────────────┘
```

| Axis | Title | Prerequisite chain | D+ ETA | Cost (USD) | Native source spec |
|---|---|---|:---:|---:|---|
| N-2 | EEG → AKIDA spike pipeline | hardware only | D+1 | $0 | `n_substrate_n2_eeg_akida_spike_pipeline_spec_2026_05_01.md` |
| N-3 | CLM × AKIDA Φ projection | N-2 + CLM cached φ★ | D+2 | $0–2 | `n_substrate_n3_clm_akida_phi_spec_2026_05_01.md` |
| N-4 | 3축 Landauer (CLM × EEG × AKIDA) | N-2 + EEG + CLM | D+3 | $0 | future spec (N-4 prep cycle) |
| N-5 | 3축 GWT broadcast | N-2 + EEG + CLM | D+4 | $0 | future spec (N-5 prep cycle) |
| N-7 | AKIDA × QRNG spike noise floor | N-2 + ANU QRNG http | D+3 | $0 | `n_substrate_n7_akida_qrng_spike_spec_2026_05_01.md` |
| N-8 | AKIDA × SIM-우주 limit saturation | N-2 + nexus SIM bridge | D+5 | $0–1 | `n_substrate_n8_akida_sim_limit_integration_2026_05_01.md` |

**Critical-path observation**: N-2 가 **single point of failure** — N-2 PASS 면 5 axes 모두 unblock 가능. N-2 FAIL (e.g. F-AK-1 ARM64 wheel 부재) 시 cascade 완전 차단.

---

## §2 D+0 (도착 day) plan

### §2.1 hardware unboxing checklist (사용자 측)

```
Box contents 검증:
  [ ] AKD1000 M.2 NVMe form-factor card (Mini Card, 22x30mm 또는 22x80mm)
  [ ] Raspberry Pi 5 (BCM2712, 16GB) — 별도 주문 시
  [ ] M.2 HAT+ for RPi5 (PCIe gen2 x1 carrier)
  [ ] Heatsink + active cooler (RPi5 권장)
  [ ] microSD ≥ 32GB (RPi OS 64-bit)
  [ ] USB-C 5V/5A power supply (RPi5 official)
  [ ] HDMI-micro 케이블 (initial setup display)
```

### §2.2 RPi5 setup (5 step, ~30 min)

```
1. Flash RPi OS 64-bit (Bookworm 이상) → microSD via Raspberry Pi Imager
2. enable PCIe gen2 in /boot/firmware/config.txt:
     dtparam=pciex1
     dtparam=pciex1_gen=2
3. Mount AKD1000 M.2 card on M.2 HAT+, secure with screw
4. Boot RPi5 → sudo apt update && sudo apt full-upgrade -y
5. Verify PCIe device:
     lspci | grep -i akida    # expect: BrainChip Holdings, Akida AKD1000
     dmesg | grep akida       # expect: probe success, IRQ assigned
```

### §2.3 BrainChip Meta TF SDK install (사용자 측)

BrainChip 공식 install path (per `doc.brainchipinc.com`):

```
# Conda env (권장, isolation)
sudo apt install -y python3-venv python3-pip libffi-dev
python3 -m venv ~/akida-env
source ~/akida-env/bin/activate

# pip install (3 packages)
pip install --upgrade pip wheel
pip install akida quantizeml cnn2snn

# Optional (EEG ingest)
pip install mne numpy scipy

# Smoke test 1 — import
python -c "import akida; print(akida.__version__); print(akida.devices())"
   # expect: ['AKD1000 / PCIe / 0']

# Smoke test 2 — cnn2snn 변환 + AKIDA inference (BrainChip MNIST sample)
python -c "
from akida_models import mnist_pretrained
from cnn2snn import convert
model_keras = mnist_pretrained()
model_akida = convert(model_keras)
model_akida.map(akida.devices()[0])
print('forward shape:', model_akida.forward(model_akida.input_shape).shape)
"
```

### §2.4 anima clone + selftest path

```
git clone <anima_repo> ~/anima
cd ~/anima

# N-2 hexa skeleton path (선재 된 spec)
ls tool/anima_eeg_to_akida_spike.hexa
# → present (committed 2026-05-01)

# 다음 step 은 D+1 §3 에서 실행
```

### §2.5 D+0 abort criteria (raw#71)

| ID | Trigger | Fallback |
|---|---|---|
| ABORT-D0-1 | `lspci` 에서 AKD1000 미인식 | RPi5 재시작 + M.2 HAT+ 재장착, 그래도 안되면 vendor RMA |
| ABORT-D0-2 | `pip install akida` 실패 (ARM64 wheel missing) | F-AK-1 fallback: x86 host (mac/ubu1) 에서 inference, RPi5 는 ADM encoder only |
| ABORT-D0-3 | `cnn2snn` 변환 실패 (TF version conflict) | venv 재생성 + `pip install tensorflow==2.15` 명시 pin |
| ABORT-D0-4 | `akida.devices()` 비어있음 (kernel module 미로드) | `sudo modprobe akida` 시도, dkms 재빌드 |

**D+0 success 기준**: smoke test 2 (MNIST cnn2snn → AKIDA `forward`) 가 non-zero output shape 출력 → D+1 진행.

---

## §3 D+1 (다음 day) plan — N-2 first run

### §3.1 N-2 spike pipeline first run (synthetic 16ch EEG)

```
cd ~/anima
hexa run tool/anima_eeg_to_akida_spike.hexa --selftest

# Expected behavior (per N-2 spec §4):
# - synthetic 60s 16ch EEG generated (seed=20260501, α 10Hz + β 20Hz + 1/f noise)
# - bandpass 1-45Hz Butterworth-4 + 60Hz notch
# - per-channel z-score (sliding 10s)
# - ADM level-crossing encoder (θ_up=θ_dn=0.5σ, refractory=4ms, Δt_bin=8ms)
# - rasterize → uint8 tensor shape (1, 125, 16, 2)
# - 6 G-D gate selftest
# - emit: state/n_substrate_n2_prep_2026_05_01/dryrun_<TS>.json
```

### §3.2 ADM encoder integration (3 ablation knobs)

| Knob | Default | A/B alt | When to flip |
|---|---|---|---|
| θ_up / θ_dn | 0.5 σ | 0.3 / 0.7 / 1.0 σ | G-D2 UP/DOWN balance fail |
| Refractory | 4 ms | 2 / 8 / 16 ms | G-D3 fail (bouncing) |
| Δt_bin | 8 ms | 4 / 16 ms | G-D4 raster shape OOM 또는 G-D5 r<0.85 |

### §3.3 AKIDA AKD1000 spike input format verification

```
python -c "
import numpy as np
import akida
from json import load
# load raster from N-2 selftest
raster = np.load('state/n_substrate_n2_prep_2026_05_01/dryrun_raster.npy')
assert raster.dtype == np.uint8
assert raster.shape == (1, 125, 16, 2)
assert raster.max() <= 15      # 4-bit precision cap
print('raster verified, sending to AKD1000 forward...')
# (placeholder model — actual cnn2snn-converted EEG model in T1-A4)
"
```

### §3.4 6 G-D selftest pass criteria (per N-2 spec §4.2)

| Gate | Check | PASS |
|---|---|---|
| G-D1 | total event count > 0 per ch | min ≥ 50 |
| G-D2 | UP/DOWN balance | 0.75 ≤ Σup/Σdn ≤ 1.33 per ch |
| G-D3 | refractory respected | min Δt ≥ r_steps |
| G-D4 | raster dtype/shape | uint8 + (1,125,16,2) + max ≤ 15 |
| G-D5 | round-trip reconstruction | Pearson r ≥ 0.85 |
| G-D6 | rate vs RMS monotonicity | Spearman ρ ≥ 0.6 |

**D+1 success 기준**: 6/6 G-D PASS + AKIDA `forward` non-zero output.

---

## §4 Tension-modulated ADM polarity bias extension (anima-specific)

### §4.1 동기

표준 ADM 은 symmetric (θ_up = θ_dn). anima 의 `tension_link` (mind.tension scalar, runtime LIVE) 는 cognitive load / arousal 의 internal index. 가설:

> **tension scalar 가 EEG → AKIDA conversion 의 information bottleneck 에서 polarity asymmetry 를 modulate 한다.**

이는 Crick-Koch binding-by-synchrony 의 anima-specific 변형 (`docs/strategic_clm_eeg_akida_tension_link_2026_05_02.md` H4) 의 hardware-native 구현 후보이다.

### §4.2 spec — tension-modulated ADM (3 mode)

표기: `tau ∈ [-1, +1]` 는 z-normalized tension scalar (sliding 30s 평균 빼고 std 로 나눈 값 clipped).

```
Mode A (linear bias):
    θ_up_eff(t) = θ_up * (1 - α * tau(t))
    θ_down_eff(t) = θ_dn * (1 + α * tau(t))
    α ∈ [0, 0.5]   # bias strength, default 0.2

  tau > 0 (high tension)  → θ_up 낮아짐 → UP spike 더 많이
  tau < 0 (low tension)   → θ_dn 낮아짐 → DOWN spike 더 많이

Mode B (sigmoid bias):
    bias = 0.5 * tanh(β * tau)
    θ_up_eff = θ_up * (1 - bias)
    θ_down_eff = θ_dn * (1 + bias)
    β = 2.0   # saturation steepness

Mode C (refractory bias, alt):
    r_up_eff(t) = r * (1 + γ * (-tau(t)))   # high tension → shorter UP refractory
    r_down_eff(t) = r * (1 + γ * tau(t))
    γ = 0.3
```

### §4.3 falsifier preregistration (F-AK-4)

| Mode | F-PASS | F-FAIL |
|---|---|---|
| A | spike-count distribution shifts with tau (KS p < 0.05, signed-corr matches §4.2 prediction) AND baseline accuracy drop < 2% | shift opposite sign OR baseline drop ≥ 2% |
| B | same as A but on sigmoid-binned tau | same |
| C | refractory-side modulation visible in ISI distribution (Anderson-Darling p < 0.05) | flat distribution |

**Conservative path**: D+1 first run 은 **bias 를 OFF (α=0)** 로 baseline 측정, D+2 부터 tension-modulated bias ON 후 baseline 대비 비교.

### §4.4 tension scalar 수급 경로

| Source | Status | Latency |
|---|---|---|
| `mind.tension` (anima_runtime UDP 9999 broadcast) | LIVE | < 1 ms |
| CLM `decoder.tension_proj.weight [768,1]` per-layer projection | LIVE (W4 verified, ubu1 RTX5070) | ~ 50 ms |
| EEG α-PLV-derived surrogate (N-1 BRIDGE_WEAK) | PARTIAL | ~ 1 s |

D+1 default = `mind.tension` UDP listener (lowest latency).

---

## §5 D+2~D+7 cascade

### §5.1 D+2 — N-3 CLM-AKIDA Φ first attempt (last-layer projection)

```
- Load CLM 350m best.pt (cached) on ubu1 RTX 5070
- Extract 16-prompt hidden-state X_clm ∈ ℝ^(16×768)
- JL projection 768 → 16 (anima_phi_v3_canonical pre-projection)
- Quantize to uint8 4-bit, NHWC reshape → (1, 1, 16, 16) AKIDA input
- AKIDA forward → spike rates Y ∈ ℝ^16
- Compute Φ_akida via same anima_phi_v3 path
- Compare to Φ_clm: Pearson r ≥ 0.85 = T-A surrogate PASS
```

Cost: $0–2 (cached CLM, AKIDA inference free).

### §5.2 D+3 — N-7 spike noise distribution measurement

```
- 1000 zero-input forward calls on AKIDA (background noise floor)
- Same 1000 calls with ANU QRNG-seeded uint8 input
- Compare ISI distributions, KS test
- F-N7-PASS: spike-noise floor distinguishable from quantum baseline (p < 0.01)
```

Cost: $0 (ANU QRNG free public API).

### §5.3 D+3 — N-4 Landauer 3-axis 최종 anchor

```
- AKIDA datasheet pJ/spike (vendor 1 W typical, ~80 NPU cores)
- EEG biology Landauer (Drubach 2000 ~25 fJ/spike biological neuron)
- CLM GPU thermal (Tegra/RTX5070 measured W during inference)
- 3-axis comparative table → kT ln 2 ratio
- PASS: AKIDA pJ/spike ≤ 1000× biological Landauer
```

Cost: $0 (datasheet + wattmeter, both available).

### §5.4 D+4 — N-5 GWT 3-axis broadcast

```
- CLM L_IX integrator workspace state
- EEG α-band Kuramoto r global synchrony
- AKIDA last-layer output as 'broadcast vector'
- 3-way concurrent measurement, time-aligned, 60s window
- F-N5-PASS: cross-correlation matrix non-trivial at lag 0
```

Cost: $0 (live measurement only).

### §5.5 D+5 — N-8 SIM-우주 limit saturation

```
- AKIDA spike events as substrate for nexus SIM bridge
- Saturate AKD1000 to max throughput (vendor 1500 fps inference)
- Measure SIM-side coherence response
- F-N8-PASS: SIM coherence varies with AKIDA load (signed corr)
```

Cost: $0–1 (compute negligible).

---

## §6 6 AKIDA axes critical path + budget

| Axis | D+? | Cost | Dependency | Falsifier |
|---|:---:|---:|---|---|
| N-2 | D+1 | $0 | hardware only | F-A1 (5× latency, N-2 native) |
| N-3 | D+2 | $0–2 | N-2 + CLM cached | T-A surrogate r ≥ 0.85 |
| N-4 | D+3 | $0 | N-2 + EEG + CLM | Landauer ratio ≤ 1000× |
| N-5 | D+4 | $0 | N-2 + EEG + CLM | cross-corr non-trivial |
| N-7 | D+3 | $0 | N-2 + ANU QRNG | KS p < 0.01 vs noise floor |
| N-8 | D+5 | $0–1 | N-2 + nexus SIM bridge | signed corr SIM↔AKIDA |
| **TOTAL** | | **$0–4** | N-2 single SPOF | 6 axes preregistered |

**Critical path 길이**: N-2 (D+1) → N-8 (D+5) = **5 days from arrival**.

---

## §7 사용자 deployment checklist (1-page printable)

```
═══════════════════════════════════════════════════════════════
  AKIDA AKD1000 D+0 ~ D+1 1-page deployment checklist (anima)
═══════════════════════════════════════════════════════════════

[ Pre-arrival (now ~ before box arrives) ]
  [ ] BrainChip developer account 생성 (doc.brainchipinc.com)
  [ ] Meta TF SDK docs 통독 (10 min): "Akida Quick Start"
  [ ] RPi5 + M.2 HAT+ + microSD 32GB+ + USB-C 5A PSU 확보
  [ ] RPi OS 64-bit (Bookworm) ISO 다운로드, microSD flash 준비

[ Day-of-arrival (D+0) ]
  [ ] Box 개봉 — AKD1000 M.2 카드 외관 검증 (chip 손상 X)
  [ ] M.2 HAT+ 에 AKD1000 장착 (screw 단단히)
  [ ] microSD 에 RPi OS flash → RPi5 부팅
  [ ] /boot/firmware/config.txt → dtparam=pciex1, pciex1_gen=2 추가
  [ ] sudo reboot
  [ ] lspci | grep -i akida   ← 인식 확인 (없으면 ABORT-D0-1)
  [ ] python venv 생성 + pip install akida quantizeml cnn2snn
  [ ] python -c "import akida; print(akida.devices())"  ← '[AKD1000 / PCIe / 0]'
  [ ] BrainChip MNIST cnn2snn 변환 smoke test 1회

[ Day+1 ]
  [ ] git clone anima → cd ~/anima
  [ ] hexa run tool/anima_eeg_to_akida_spike.hexa --selftest
  [ ] 6/6 G-D gate PASS 확인 → state/n_substrate_n2_prep_2026_05_01/dryrun_*.json
  [ ] Φ extension: tension-modulated bias OFF baseline 측정
  [ ] (optional) OpenBCI Cyton+Daisy 페어링, --input live 60s

[ Day+2 ~ D+7 cascade ]
  [ ] D+2: N-3 CLM × AKIDA Φ projection
  [ ] D+3: N-7 spike noise floor + N-4 Landauer 3-axis
  [ ] D+4: N-5 GWT 3-axis broadcast
  [ ] D+5: N-8 SIM-우주 limit saturation

[ Top-5 critical items ]
  1. lspci 인식 (D+0 ABORT-1 핵심)
  2. ARM64 wheel install 성공 (F-AK-1 핵심)
  3. cnn2snn smoke test PASS (TF version 충돌 흔함)
  4. 6/6 G-D selftest PASS (N-2 single SPOF)
  5. tension-modulated bias α=0 baseline 우선 (F-AK-4 conservative)
═══════════════════════════════════════════════════════════════
```

---

## §8 5 raw#71 falsifier preregister (F-AK-1 ~ F-AK-5)

### F-AK-1 — Akida wheel ARM64 install 실패

| Field | Value |
|---|---|
| Trigger | `pip install akida` 가 ARM64 manylinux wheel 없음 / source-build 실패 |
| Detection | D+0 §2.3 smoke test 1 ImportError 또는 wheel-not-found |
| Fallback | x86 host (mac M2 / ubu1 x86_64) 에서 AKIDA inference, RPi5 는 ADM encoder only role demote. USB-host bridge mode 검토. |
| Severity | HIGH (cascade 5 axes 우회 필요) |
| Estimated probability | 0.35 (BrainChip historically x86 우선) |

### F-AK-2 — cnn2snn 8-bit precision insufficient

| Field | Value |
|---|---|
| Trigger | EEG model 8-bit cnn2snn 변환 후 baseline 대비 accuracy drop > 5% |
| Detection | D+2 N-3 first attempt 시 Φ_akida vs Φ_clm Pearson r < 0.50 |
| Fallback | 4-bit retrain (quantizeml `quantize_model` precision_in=4), 또는 mixed-precision (input 8-bit, weight 4-bit) |
| Severity | MED (N-3/N-5 영향, N-2/N-4/N-7 unaffected) |
| Estimated probability | 0.40 |

### F-AK-3 — spike rate < 1 spike/s

| Field | Value |
|---|---|
| Trigger | G-D1 fail — 일부 channel 이 60s 동안 50 spike 미달 |
| Detection | D+1 selftest dryrun_*.json |
| Fallback | ADM theta 재조정 (0.5σ → 0.3σ), 또는 z-score window 단축 (10s → 5s) |
| Severity | LOW (N-2 spec 자체 ablation knob 으로 흡수) |
| Estimated probability | 0.20 |

### F-AK-4 — tension-modulated bias 가 baseline accuracy 떨어뜨림

| Field | Value |
|---|---|
| Trigger | bias α=0.2 ON 시 G-D5 round-trip Pearson r 가 baseline (α=0) 대비 0.05 이상 하락 |
| Detection | D+1 후반 / D+2 §4.3 ablation |
| Fallback | bias 제거 (α=0 영구), tension-modulation 은 N-3 layer-side 로 이전 (decoder.tension_proj 활용) |
| Severity | LOW (anima-specific extension, vendor 미지원, baseline 영향 없게 conservative path) |
| Estimated probability | 0.50 (high — anima-native untested) |

### F-AK-5 — AKD1000 datasheet pJ/spike vs in-situ wattmeter mismatch > 2×

| Field | Value |
|---|---|
| Trigger | D+3 N-4 Landauer 3-axis 측정 시 datasheet vs RPi5 USB-C wattmeter 측정값 차이 > 2× |
| Detection | wattmeter (예: USB Power Meter ~$15) D+3 측정 |
| Fallback | vendor query + 추가 측정 (idle / max-load 분리), datasheet 값 conservative range 로 선언 |
| Severity | MED (N-4 thermodynamic anchor 약화, N-2/N-3 unaffected) |
| Estimated probability | 0.30 |

---

## §9 Honest C3 (raw#10, 9건)

1. **C3-1** AKIDA arrival ETA 미확정 (vendor logistics, anima-side 통제 불가) — 본 plan 자체 hypothetical, 도착 전 검증 불능. 동결된 것은 spec 만, 실측 0.
2. **C3-2** ARM64 wheel availability 사용자 D+0 검증 단일 시점에 의존 — F-AK-1 fallback path 정의했으나, x86 host fallback 시 RPi5 edge-device 가치 (~1W power) 손실.
3. **C3-3** BrainChip Meta TF SDK 가 frequent 변경 (지난 6개월 cnn2snn API 2회 break) — D+0 docs 재독 필요, 본 plan SDK pin 미고정.
4. **C3-4** tension-modulated ADM polarity bias 자체가 anima-specific extension, vendor 지원 X — F-AK-4 50% probability 가장 높음, baseline 영향 없게 conservative path 강조.
5. **C3-5** 6 axes cascade 가 N-2 single-point-of-failure — N-2 FAIL 시 전체 plan collapse, fallback 으로 simulation-only mode 정의 안되어 있음.
6. **C3-6** RPi5 + AKD1000 PCIe gen2 stability 미검증 — kernel module dkms / IRQ 충돌 사례 BrainChip community 에 보고됨, 본 plan 에서는 ABORT-D0-4 dkms 재빌드 외 대안 없음.
7. **C3-7** D+2 N-3 last-layer projection 가 transformer self-attention 을 AKD1000 unsupported layer 로 우회 — JL projection 으로 768→16 압축, 정보 loss 정량화 안됨.
8. **C3-8** D+3 N-7 ANU QRNG 가 public HTTP API 의존 — rate limit (1 req/sec), network outage 시 D+3 slip.
9. **C3-9** 사용자 1-page checklist 가 사용자 hardware 숙련도 가정 (M.2 mount, /boot/firmware 편집) — 비숙련 시 D+0 시간 estimate 30 min 이 2-3 hour 로 늘어날 수 있음.

---

## §10 References

- N-2 spec: `docs/n_substrate_n2_eeg_akida_spike_pipeline_spec_2026_05_01.md`
- N-3 spec: `docs/n_substrate_n3_clm_akida_phi_spec_2026_05_01.md`
- N-7 spec: `docs/n_substrate_n7_akida_qrng_spike_spec_2026_05_01.md`
- N-8 spec: `docs/n_substrate_n8_akida_sim_limit_integration_2026_05_01.md`
- AKIDA dev kit eval: `docs/akida_dev_kit_evaluation_2026-04-29.md`
- AKIDA session friendly: `docs/akida_session_friendly_report_2026-04-29.md`
- Strategic 4-way: `docs/strategic_clm_eeg_akida_tension_link_2026_05_02.md`
- N-batch roadmap: `docs/n_substrate_consciousness_roadmap_2026_05_01.md`
- N-2 sister state: `state/n_substrate_n2_prep_2026_05_01/spec_manifest.json`
- This doc race-isolated state: `state/akida_d0_d1_plan_freeze_2026_05_02/{spec_manifest,d0_checklist,d1_runbook,axes_critical_path,falsifier_F_AK_preregister}.json`

---

## §11 Word count / spec stats

- Word count: ~2,100 (within 1500–2500 권장 range)
- 6 AKIDA-dependent axes graphed
- D+0 5-step + D+1 4-section + D+2~D+7 5-day cascade
- 4 ABORT-D0 codes (raw#71)
- 5 F-AK falsifier preregistered
- 9 honest C3 (raw#10)
- 1-page printable checklist (§7)
- 5 state JSON deliverables under `state/akida_d0_d1_plan_freeze_2026_05_02/`
