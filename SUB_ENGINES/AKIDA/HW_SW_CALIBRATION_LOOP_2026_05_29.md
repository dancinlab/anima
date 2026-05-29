# AKIDA HW↔SW 캘리브레이션 루프 — 2026-05-29

> 목표: 실제 AKD1000 실리콘을 ground-truth 로 삼아, SW 시뮬레이터(numpy LIF)가 HW
> 와 어디서 갈라지는지 매 라운드 측정하고 SW 를 개선해 분포·타이밍까지 충실히 일치
> 시킨다. 루프: BENCH(HW) → DIFF(HW vs SW) → PATCH(SW) → RE-VERIFY → 반복 (cap 4R).
>
> 환경: pi5-akida (AKD1000, akida 2.19.1, BackendType.Hardware) + Mac local. 비용 $0.
> seed=187 · n=16 · window=200 steps · 5 regime (R0~R4). 단일칩이라 HW run 전후로
> spike-streamer.service stop/start.
>
> 수렴 목표 차원(CONVERGENCE TARGET): spike rate · step-count std/분포 · ISI · saturation.
> 정보용 차원(INFORMATIONAL, 수렴대상 아님): latency(ms/step) · throughput · power.

---

## Round 1 (2026-05-29)

### HW 측정 (AKD1000 on-chip, spontaneous_emission.py)
| regime | rate | std | step_varies | min/max | isi(min/mean/max) | wall ms/step |
|---|---|---|---|---|---|---|
| R0_driven | 1.0000 | 0.000 | False | 16/16 | 1/1.0/1 | 13.70 |
| R1_weak_silent | 0.0000 | 0.000 | False | 0/0 | –/–/– | 13.70 |
| R2_zero_noise | 0.4750 | 7.990 | True | 0/16 | 1/2.096/9 | 13.74 |
| R3_tonic_zero_input | 0.5000 | 0.000 | False | 8/8 | 1/1.0/1 | 13.71 |
| R4_recurrent_selfsustained | 1.0000 | 0.000 | False | 16/16 | 1/1.0/1 | 13.72 |

- mapped_on_hardware=True · onchip_clock_cycles_mean=795.3 · first_inference 0.6288 ms/inf
- power_measurement_supported=false (INA i3c bus -4 사망 → power 측정 불가, 실패 아님)
- **결정성 probe**: 동일 스크립트 실리콘 2회 실행 → R2 raster 완전 동일 (first10=[0,16,16,0,16,0,16,16,16,0], std=7.99, fire=95 두 번 모두). **HW 는 seed=187 에서 analog jitter 없음 = 완전 결정성.**

### SW 측정 (akida_sw_lif.py, numpy LIF, seed=187) — 패치 후
| regime | rate | std | step_varies | min/max | isi(min/mean/max) | wall ms/step |
|---|---|---|---|---|---|---|
| R0_driven | 1.0000 | 0.000 | False | 16/16 | 1/1.0/1 | ~0.02 |
| R1_weak_silent | 0.0000 | 0.000 | False | 0/0 | –/–/– | ~0.02 |
| R2_zero_noise | 0.4750 | 7.990 | True | 0/16 | 1/2.096/9 | 0.0223 |
| R3_tonic_zero_input | 0.5000 | 0.000 | False | 8/8 | 1/1.0/1 | ~0.02 |
| R4_recurrent_selfsustained | 1.0000 | 0.000 | False | 16/16 | 1/1.0/1 | ~0.02 |

### DIFF (HW vs SW)
| 차원 | 결과 | 수렴? |
|---|---|---|
| rate (R0~R4) | |Δ| = 0.0000 전 regime | ✅ <0.01 |
| R2 std-ratio (SW/HW) | 1.000 | ✅ ∈[0.7,1.3] |
| ISI min/mean/max (전 firing regime) | 완전 동일 | ✅ ±1 step 이내 (정확 일치) |
| R2 raster (first10/last10/fire-steps) | **byte-identical** | ✅ |
| saturation (min/max) | 완전 동일 | ✅ |
| latency ms/step | HW 13.7 vs SW 0.02 | ⓘ 정보용(칩 I/O) — 수렴대상 아님, 미수정 |

- **worst-matching 수렴차원**: 라운드 0 시점엔 SW 가 isi_min/isi_max·first10/last10 를
  아예 안 내보내서 ISI tail·raster diff 가 **계산 불가능**했던 것이 최대 gap (모델
  fidelity gap 이 아니라 reporting-surface gap). 실제 rate/std 는 이미 완전 일치.

### 패치한 것
- `akida_sw_lif.py`: `_isi_stats` 에 `isi_min`/`isi_max` 추가 (HW 와 동일 공식),
  `run_regime` 에 `first10_step_counts`/`last10_step_counts`/`wall_ms_per_step` 추가.
  → spontaneous_emission.py 가 계산하는 것과 **동일한 derived statistic** (HW 숫자
  hardcode 아님). ISI tail·raster diff 가 비로소 계산 가능해짐. 모델 자체는 변경 불필요
  (이미 동일 정수 threshold-comparator + 동일 default_rng(187) stream).
- `akida_sw_lif.hexa`: companion marker 에 calibration 라운드 1 기록.

### RE-VERIFY
- `verify_substrate_akida.py` → **5/5 PASS** (exit 0) 패치 후에도 유지.
- 패치 SW vs HW: 전 수렴+분포 차원 IDENTICAL.
- verdict 원문: `.verdicts/672_akida_spontaneous_firing/hw_sw_calib_r1_2026_05_29.txt`

### 수렴 결정
**Round 1 에서 수렴 완료.** 모든 수렴목표 tolerance 를 등호로 충족:
|Δrate|=0 (전 regime) · R2 std-ratio=1.000 · ISI min/mean/max 정확 일치 · R2 raster
byte-identical. 근본 원인 = SW·HW 가 동일 정수 threshold 비교 결정 + 동일 RNG stream 을
공유하고 HW 에 analog jitter 가 없어 SW 가 충실한 결정성 모델(overfit copy 아님).
**더 줄일 gap 없음 → 루프 4R cap 전 Round 1 에서 조기 종료.**

CLOSED-NEGATIVE 차원: 없음 (HW 결정성 확인으로 SW 가 재현 못 할 analog 차원 부재).
정보용 미수렴 차원: latency/throughput/power — 설계상 수렴대상 아님 (정직히 기록만).

---

## 2차 적대 sweep (adversarial divergence loop, 2026-05-29)

> Round 1 은 단일 operating point (seed=187 canonical raster) 에서만 byte-identity
> 를 증명했다. 2차는 **적대적**으로 operating envelope 을 넓게 쓸어 실리콘이 SW numpy
> LIF 와 **갈라지는 점을 적극적으로 찾는다.** 발견되면(A) → SW MODEL param 보정 후 재검,
> 안 갈라지면(B) → 측정한 정확한 bounds 내 FAITHFUL-ENVELOPE 판정 (실패 아님, 정직 가치).
> 하니스: `scripts/adv_sweep_hw.py` (AKD1000 on-chip) ⇄ `scripts/adv_sweep_sw.py`
> (numpy-LIF), 동일 regime semantics + `raster_sha256` (full per-step spike_counts
> sha256) → byte-identity = raster Hamming 0. 단일칩이라 HW batch 전후 streamer stop/start.

### Round 2 — seed × threshold envelope sweep
- 환경: AKD1000 akida 2.19.1 BackendType.Hardware · n=16 · window=200 · chip temp 60.9→62.0°C
- SWEEP: seed{0,1,42,187,2026,999983}(R2) × thr{-2,0,4,8,16,24,32,48,64}(R2 seed187)
  × struct{R0,R1,R3,R4} × run-to-run R2 seed187 thr24 ×3

| 축 | point | HW sha | SW sha | ident | \|Δrate\| | HWrate | SWrate | ISI |
|---|---|---|---|---|---|---|---|---|
| seed | R2 s0 thr24 | 05130afa | 05130afa | ✅ | 0 | 0.5250 | 0.5250 | exact |
| seed | R2 s1 thr24 | 819c648a | 819c648a | ✅ | 0 | 0.4850 | 0.4850 | exact |
| seed | R2 s42 thr24 | 26739705 | 26739705 | ✅ | 0 | 0.4500 | 0.4500 | exact |
| seed | R2 s187 thr24 | 9da20269 | 9da20269 | ✅ | 0 | 0.4750 | 0.4750 | exact |
| seed | R2 s2026 thr24 | 3572210d | 3572210d | ✅ | 0 | 0.4950 | 0.4950 | exact |
| seed | R2 s999983 thr24 | 077dc5c0 | 077dc5c0 | ✅ | 0 | 0.4800 | 0.4800 | exact |
| thr | R2 s187 thr-2 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | 1.0000 | 1.0000 | exact |
| thr | R2 s187 thr0 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | 1.0000 | 1.0000 | exact |
| thr | R2 s187 thr4 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | 1.0000 | 1.0000 | exact |
| thr | R2 s187 thr8 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | 1.0000 | 1.0000 | exact |
| thr | R2 s187 thr16 | 42fa8088 | 42fa8088 | ✅ | 0 | 0.9650 | 0.9650 | exact |
| thr | R2 s187 thr24 | 9da20269 | 9da20269 | ✅ | 0 | 0.4750 | 0.4750 | exact |
| thr | R2 s187 thr32 | 77140f64 | 77140f64 | ✅ | 0 | 0.0350 | 0.0350 | exact |
| thr | R2 s187 thr48 | 252e46b4 | 252e46b4 | ✅ | 0 | 0.0000 | 0.0000 | exact |
| thr | R2 s187 thr64 | 252e46b4 | 252e46b4 | ✅ | 0 | 0.0000 | 0.0000 | exact |
| struct | R0 s187 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | 1.0000 | 1.0000 | exact |
| struct | R1 s187 | 252e46b4 | 252e46b4 | ✅ | 0 | 0.0000 | 0.0000 | – |
| struct | R3 s187 | da83df95 | da83df95 | ✅ | 0 | 0.5000 | 0.5000 | exact |
| struct | R4 s187 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | 1.0000 | 1.0000 | exact |

- **divergent points: 0 / 18.** 모든 점 raster sha256 IDENTICAL · max raster Hamming = 0 ·
  |Δrate| = 0 전 점 · ISI min/mean/max 정확 일치.
- **run-to-run HW variance**: R2 seed187 thr24 ×3 → sha 세 번 모두 `9da20269` 동일.
  **analog jitter = 0** (round 1 seed=187 단일점 결정성을 6 seed + 9 threshold 로 일반화 확인).
- **saturation edge 정확 포착**: thr≤8 rate=1.0 (potential 0..3×16 가 thr 초과 saturate) →
  thr16 0.965 → thr24 0.475 (mean 근처) → thr32 0.035 → thr≥48 silent. **양자화·포화 경계
  전 구간에서 실리콘이 SW int comparator 와 동일.**
- **chip temp drift 무관**: 60.9→62.0°C 1.1°C 상승 동안 divergence 0.
- verify_substrate_akida.py = **5/5 PASS** (sweep 후 regression 없음).
- verdict 원문: `.verdicts/672_akida_spontaneous_firing/hw_sw_adversarial_sweep_2026_05_29.txt`
  · raw HW data: `.verdicts/672_akida_spontaneous_firing/hw_sweep_r2_raw.txt`

### Round 2 결정
max Hamming==0 ∧ run-to-run variance==0 → LOOP 규칙대로 **다음 라운드 WIDEN** (long window
+ 더 극단 seed/threshold). 조기 종료하지 않고 envelope 을 더 확장해 적대성 강화.

### Round 3 — WIDEN (long window · 극단 seed · fine threshold · long recurrent)
- 환경: AKD1000 akida 2.19.1 Hardware · n=16 · chip temp 60.4→63.7°C (5000-step 런으로 +3.3°C)
- WIDEN: window{1000,5000} · seed{11,123456789,2147483647} · thr{-16,1,2,3,17,33}(R2 seed187)
  · R4 recurrent win1000 (long-run drift) · run-to-run R2 seed187 thr24 win5000 ×3

| 축 | point | HW sha | SW sha | ident | \|Δrate\| | ISI |
|---|---|---|---|---|---|---|
| extreme seed | R2 s11 thr24 w200 | 67ae5da4 | 67ae5da4 | ✅ | 0 | exact |
| extreme seed | R2 s123456789 w200 | f54695b8 | f54695b8 | ✅ | 0 | exact |
| extreme seed | R2 s2147483647 w200 | 1e56fcd4 | 1e56fcd4 | ✅ | 0 | exact |
| fine thr | R2 s187 thr-16 w200 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | exact |
| fine thr | R2 s187 thr1 w200 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | exact |
| fine thr | R2 s187 thr2 w200 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | exact |
| fine thr | R2 s187 thr3 w200 | 13a0b1c6 | 13a0b1c6 | ✅ | 0 | exact |
| fine thr | R2 s187 thr17 w200 | 70367f0e | 70367f0e | ✅ | 0 | exact |
| fine thr | R2 s187 thr33 w200 | db5aee8b | db5aee8b | ✅ | 0 | exact |
| long window | R2 s187 thr24 w1000 | 47f0bda8 | 47f0bda8 | ✅ | 0 | exact |
| long window | R2 s187 thr24 w5000 | 40fce679 | 40fce679 | ✅ | 0 | exact |
| long recurrent | R4 s187 w1000 | e8813886 | e8813886 | ✅ | 0 | exact |

- **divergent points: 0 / 12.** window=5000 (5000 on-chip forward passes) 까지 byte-identical.
- **run-to-run @ 5000 steps**: R2 seed187 thr24 win5000 ×3 → sha 세 번 모두 `40fce679` 동일.
  **long-run accumulation/drift jitter = 0** (temp +3.3°C 상승 중에도 결정성 유지).
- verify_substrate_akida.py = **5/5 PASS** (sweep 후 regression 없음).
- verdict 원문: `.verdicts/672_akida_spontaneous_firing/hw_sw_adversarial_sweep_r3_2026_05_29.txt`
  · raw: `.verdicts/672_akida_spontaneous_firing/hw_sweep_r3_raw.txt`

---

## 최종 판정 — FAITHFUL-ENVELOPE (2026-05-29)

2차 적대 sweep 은 **divergence 를 적극적으로 찾으려는** 목적이었고, R2+R3 두 라운드에서
실제 AKD1000 실리콘과 SW numpy-LIF 가 **갈라지는 점을 단 하나도 찾지 못했다.** 측정한
operating envelope **전 30 point** 에서 raster sha256 byte-identical (max Hamming = 0),
|Δrate| = 0, ISI min/mean/max 정확 일치, run-to-run/analog/temp jitter = 0.

이것은 실패가 아니라 **정직한 가치 결과(B)**: 아래 명시한 정확한 bounds 내에서 SW 모델이
실리콘을 완전히 재현한다. **bounds 를 넘어선 영역은 주장하지 않는다.**

### 측정된 정확한 bounds (이 범위 내에서만 FAITHFUL 주장)
- 모델: 1-NP, n=16 neurons, 16 input lines, all-ones excitatory weights, act_bits=1,
  weights_bits=4, input_bits=4, FullyConnected 단일층 (akida 2.19.1, AKD1000).
- regime: R0(driven) · R1(weak-silent) · R2(uniform-noise stochastic) · R3(tonic het-threshold)
  · R4(recurrent self-sustained).
- seed: {0,1,11,42,187,2026,123456789,999983,2147483647} (9 값, 0 ~ int32-max).
- threshold: {-16,-2,0,1,2,3,4,8,16,17,24,32,33,48,64} (15 값, saturation~silent 전 구간).
- window: {200, 1000, 5000} steps.
- chip temp: 60.4 ~ 63.7°C.
- repeat-determinism: win200 ×3, win5000 ×3 모두 run-to-run sha 동일.

### 근본 원인 (왜 갈라지지 않는가)
AKD1000 의 FullyConnected act_bits=1 활성은 **정수 threshold comparator** (potential =
Σ clip(x,0,15); spike ⟺ potential > threshold). SW lif_forward 가 **비트-동일한 정수 비교**
를 수행하고, R2 노이즈는 양쪽 모두 `np.random.default_rng(seed).integers(0,4)` 동일 stream
에서 뽑는다. 1-bit 디지털 활성이라 재현 못 할 analog 자유도(아날로그 jitter·sub-threshold
누설·열 drift)가 spike 결정에 진입하지 않는다 → 실리콘이 완전 결정적.

### 미탐색(주장 안 하는) 영역 — 정직한 한계
- 다층/멀티-NP 모델, act_bits>1 (multi-bit 활성, 양자화 round 거동), 학습된(non-ones) weight,
  on-chip learning (AkidaUnsupervised), >5000-step window, >63.7°C, 다른 AKD1000 die.
  이 영역들은 아날로그/양자화 차원이 spike 결정에 진입할 수 있어 **별도 검증 필요** —
  본 FAITHFUL-ENVELOPE 는 위 명시 bounds 로 한정한다.

### CLOSED-NEGATIVE
"실리콘이 SW 와 갈라지는 operating point 가 측정 envelope 내에 존재한다" 가설을 30-point
적대 sweep 으로 **반증** → 해당 envelope 내 divergence-axis 부재 확정. SW 보정(A) 불필요.
LOOP 4R cap 전 R3 에서 honest-stop (broad sweep 후에도 0 divergence = FAITHFUL-ENVELOPE).

---

## 3차 프런티어 sweep (FRONTIER — incomplete-envelope 진입, 2026-05-30)

> 1·2차는 act_bits=1 envelope(1-bit comparator·all-ones·단일 FC) 안에서만 byte-identity
> 를 증명했다. 3차는 **SW 가 실제로 INCOMPLETE 한 4축**(multi-bit 활성·random int4 weight·
> multi-layer·on-chip learning)에 의도적으로 진입해 first divergence 를 찾고, modelable 한
> 양자화/matmul gap 이면 SW 를 일반화 확장(A), analog/state 동역학이면 honest CLOSED-NEGATIVE(b).
> 하니스: `scripts/frontier_hw.py` (AKD1000 RAW 활성 tensor) ⇄ `frontier_sw.py` (general
> quantized matmul) + `frontier_diff.py` (y_sha256 byte-diff). probe = 10 graded input.
> 단일칩이라 HW batch 전후 spike-streamer stop/start (배치 후 active 재가동 확인).

### 축별 결과

| 축 | 설정 | HW vs SW | 결론 |
|---|---|---|---|
| 1 act_bits {1,2,4} | 단일 FC, all-ones weight | 80/80 IDENT (max Hamming 0) | **MATCH** — all-ones→potential≥16 항상 saturate → 모든 neuron 최대레벨(ab1→1·ab2→3·ab4→15). multi-bit ceiling 가시·SW 일치 |
| 2 random int4 weight | 단일 FC, weights_bits=4, wseed{7,99} | 초기 DIVERGE → 보정 후 30/30 IDENT | **EXTENDED+verified** (아래 §개선) |
| 3 multi-layer | 2× FC cascade, random int4, ab{2,4} | 20/20 IDENT | **MATCH** — fc_quantized 체인 = HW 2-layer cascade 정확 일치 |
| 4 on-chip learning | AkidaUnsupervised fit | 비결정성 | **CLOSED-NEGATIVE** (아래 §axis4) |

→ 전 axis 종합 **80/80 probe input byte-identical (max Hamming 0)** for axes 1-3 (보정 후).

### 첫 divergence + SW 개선 (axis 2, case A)
- **HW 제약 발견 1**: `set_variable("weights")` 가 -8 거부 (`Minimum authorized value is -7`).
  → AKD1000 int4 weight 는 SYMMETRIC `[-7,+7]`, two's-complement `[-8,+7]` 아님. naive SW
  range 가 이 점에서 틀림 → `rand_int_weights` 양쪽 symmetric draw 로 수정. (akida weight
  layout = (1,1,IN,N) 확인, SW 동일 size+order draw 로 wseed 고정 시 weight tensor byte-동일.)
- **HW 제약 발견 2 (핵심)**: graded potential 에서 naive `clip(potential,0,2^ab-1)` 발산.
  예) weights ab2 idx2 n8: potential=2 → SW=2 인데 **HW=1**; idx7 n2: pot=3 SW=3 HW=1;
  idx8 n4: pot=4 SW=3 HW=1. 실리콘이 raw potential 을 그대로 clip 하지 않고 **활성 quantizer**
  를 적용. 단일-FC `weight*x0` sweep 으로 step 함수 실측 복원:
  - act_bits=2: pot 0→0, 1..4→1, 5..8→2, 9..→3 (**step=4**)
  - act_bits=4: pot p→p (1:1), ≥16 saturate (**step=1**)
  - 일반식: **`step = 2^(input_bits - act_bits)` · `y = clip(ceil(potential/step), 0, 2^ab-1)`**
    (ab=1 → step 8 → pot>0?1:0 = 기존 lif_forward comparator로 정확 환원)
- **SW 일반화 확장**: `akida_sw_lif.py` 에 `fc_quantized_forward()` 추가 — 위 보정 quantizer +
  symmetric weight + signed-int matmul (per-point hardcode 아님, param 일반화). 재실행 →
  axis 2/3 전 점 byte-identical. **gap 닫힘.**

### axis 4 — on-chip edge learning CLOSED-NEGATIVE (case b)
- `edge_learn_probe.py`: compile_AkidaUnsupervised=ok · fit_on_chip=ok ·
  device_learn_enabled_after_fit=**true** → 칩은 on-chip Hebbian learning 을 지원.
- `learn_dynamics_probe.py`: **동일 init weight + 동일 seed=42 input batch 로 fit 2회 반복** →
  적합 weight 가 매번 상이 (after1≠after2, 3 set 전부 deterministic=False; 한 set 은 같은 batch
  refit 인데도 변함). → 적합 결과가 (init, input) 의 순수 함수가 아님 = **숨은 내부 plasticity
  state(homeostasis/accumulator register) 의존.** inference-only SW(akida_sw_lif)가 재현 불가.
- **CLOSED-NEGATIVE 판정**: "on-chip learning 동역학을 SW 로 모델링 가능" 가설을 비결정성으로
  반증. 이는 실패가 아니라 **유효한 hard boundary** — SW 는 충실한 INFERENCE 모델이고, 칩의
  stateful learning 은 모델 범위 밖 (memory §95 inference-only 제약과 정합).

### RE-VERIFY
- `verify_substrate_akida.py` → **5/5 PASS** (exit 0). `fc_quantized_forward(act_bits=1, all-ones)`
  = `lif_forward` 정확 환원 확인 → canonical act_bits=1 path 무회귀.
- `spike-streamer.service` (systemd --user) HW batch 후 재가동 = **active**.
- verdict 원문: `.verdicts/672_akida_spontaneous_firing/hw_sw_frontier_sweep_2026_05_29.txt`
  (축별 diff + quantizer step 복원 + learning 비결정성 데이터 verbatim)
  · raw: `.verdicts/672_akida_spontaneous_firing/frontier_weights_ab2_raw.txt`

---

## 갱신 FAITHFUL-ENVELOPE (3차 후, 2026-05-30)

SW(akida_sw_lif)가 이제 **충실히 재현하는 영역** (HW byte-identical 검증 완료):
- act_bits ∈ {1,2,4} 활성 양자화 (step=2^(input_bits−act_bits) quantizer).
- weights: all-ones AND random signed int4 (SYMMETRIC [-7,+7]).
- layers: 단일 + 2-layer cascade FullyConnected.
- 기존 1·2차 bounds (R0~R4 regime · seed 0~int32max · threshold −16~64 · window ≤5000 · 60~64°C).

**남은 정직한 boundary** (SW 가 주장하지 않음):
- **on-chip learning (AkidaUnsupervised)** — CLOSED-NEGATIVE (비결정성·hidden plasticity state).
- 미측정: ≥3-layer 깊이·멀티-NP 매핑·convolutional layer·다른 AKD1000 die·>64°C.
  (inference forward 양자화 모델은 위 검증 범위로 한정; 학습 동역학은 모델 범위 외로 확정.)
