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
