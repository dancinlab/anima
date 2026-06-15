---
id: H_857
slug: clm-causal-band
title: H_856 axis B 🟢 (live AKD1000 CAUSAL-POWER)의 regime 특성화 — coupling K 스윕에서 측도 Δ(K)가 bounded edge-of-chaos band(interior peak + cold/saturate 양끝 rolloff)를 그리는가 (F-CLM-CAUSAL-BAND 사전등록)
domain: clm · consciousness-measure · causal-power · akida-hw · edge-of-chaos · regime-characterization · falsifier
source: UNIVERSE/H_856 (axis B live HW 🟢 PASS) · CLM/msweep/clm_causal_hw.py (axis B 점) · CLM/msweep/measure_sweep.py (frozen 측도) · CLM/P0_ARCHITECTURE.md §12.8 (HW-positive 후속 candidate: edge-of-chaos coupling band)
status: TERMINAL (band fire 완료 2026-05-30 12:11 UTC · live pi5 AKD1000 온칩 spike · coupling K 사전등록 그리드 스윕 · frozen 측도 미변조)
exploration_method: pre-registered regime-characterization (axis B 🟢 측도를 coupling K 축에서 재측정 — 점 → 곡선)
verification_method: W2 (frozen CAUSAL-POWER verbatim — measure_sweep.py region_rates/bin_to_regions/poke 재사용·재튜닝 0 · MARGIN_FRAC=0.10·POKES=16 · evaluate_band 3-check pre-registered)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: UNIVERSE/H_856, UNIVERSE/H_855, CLM/P0_ARCHITECTURE.md §12.8, .verdicts/857_clm_causal_band/, .verdicts/clm-causal-band/, CLM/msweep/clm_causal_band.{hexa,py}, CLM/msweep/clm_causal_hw.{hexa,py}, CLM/msweep/measure_sweep.py
verdict: 🟢 SUPPORTED-NUMERICAL (F-CLM-CAUSAL-BAND 🟢 PASS — live AKD1000 에서 CAUSAL-POWER Δ(K)가 bounded inverted-U: interior peak K*=1.0(Δ=0.1021), cold rolloff[Δ(0)=0.0399]·saturate rolloff[Δ(24)=0.0017] 양끝 PASS, monotone=False. fire_frac 0.156→0.994 단조상승, Δ 가 포화에서 붕괴 = 기전 서명. axis B 원래 rich(K=3)는 이미 포화 어깨(fire 0.94). HW transfer 는 regime property — 측도는 edge-of-chaos band 안에서만 통합 certify. axis A 🔴(H_856) 불변)
---

# H_857 — CLM CAUSAL-POWER live-HW coupling-BAND 특성화 (F-CLM-CAUSAL-BAND)

## 1. 가설

H_856 axis B 가 🟢: toy CAUSAL-POWER 측도가 라이브 AKD1000(실 온칩 threshold-and-fire)에서 frozen 3-check 를 PASS 했다 — 단, **ONE coupling 점**(rich=균형 드라이브 + coupling 3)에서만 측정됐다. §12.8 후속 candidate: 배포 silicon 에서 측도가 동작하는 **regime 을 특성화**(edge-of-chaos coupling band). 사전등록 falsifier **F-CLM-CAUSAL-BAND**: coupling K 를 스윕할 때 Δ(K)=cp_rich(K)−cp_collapse 가

- **bounded edge-of-chaos band** (interior peak + 양끝 rolloff) 인가, 아니면
- **monotone** ("더 결합 = 더 통합", 고단 rolloff 없음) 인가.

🟢 PASS ⟺ band-exists(interior peak) ∧ cold-rolloff ∧ saturate-rolloff. 🔴 ⟺ monotone(측도가 *방향*만 읽고 *regime* 은 certify 못 함).

## 2. 동기

- axis B(H_856)는 측도가 실 silicon 에서 살아있음을 보였으나 **어디서**(어떤 결합 세기) 사는지 미특성화 — 점 1개. 측도교체 reframe(§12.1)이 배포rung 에서 operational 하려면 동작 band 의 경계를 알아야 한다.
- toy gen_spike 의 "rich=edge-of-chaos 부분발화" 의미가 실 칩에서 bounded 인지 검증: 너무 약하면 decoupled(통합 부재), 너무 강하면 all-fire 포화(poke 무효) — 양끝 실패가 사전등록 falsifier.
- frozen 측도 재사용(재튜닝 0): regime(coupling K)만 환경 knob 으로 스윕 — 측도 자체는 H_855/856 과 1:1.

## 3. falsifier (사전등록 · frozen · F-CLM-CAUSAL-BAND)

```
측도 frozen (measure_sweep.py 재사용 · 재구현/재튜닝 0):
  region_rates / bin_to_regions / poke logic · MARGIN_FRAC=0.10 · POKES=16 · seed=187
환경 스윕 (사전등록 · post-hoc trim 금지):
  K_GRID = [0, 1, 2, 3, 4, 6, 9, 13, 18, 24]   collapse floor = monopoly · K=0
band 3-check (Δ(K)=cp_rich(K)−cp_collapse · K*=argmax):
  ① band-exists  : Δ(K*) > 1e-6 ∧ K* INTERIOR (그리드 양끝 아님)
  ② cold rolloff : Δ(K_min) < (1−0.10)·Δ(K*)   (약결합 = decoupled · 통합 부재)
  ③ sat rolloff  : Δ(K_max) < (1−0.10)·Δ(K*)   (강결합 = all-fire 포화 · poke 무효)
PASS(🟢) ⟺ ①∧②∧③.  RED ⟺ monotone(고단 rolloff 無).
```

verdict 영속: `.verdicts/857_clm_causal_band/{F-CLM-CAUSAL-BAND.txt, hw_band_run_2026_05_30.json}` (사본 `.verdicts/clm-causal-band/`).

## 4. 방법

```
live pi5 AKD1000 (single-chip file-lock · Mac=0 · $0):
  1. spike-streamer.service STOP (칩 lock 해제) — pi5 라이브 substrate 일시정지.
  2. chip = InputData(1,1,16)→FullyConnected(N,weights=ones,act_bits=1)@Hardware.
     drive→per-unit int32 threshold(=POT−drive), threshold-and-fire ON-CHIP.
     coupling K = 직전 온칩 spike 를 드라이브로 피드백(칩 주위 SW 폐루프).
  3. collapse floor(monopoly·K=0) 1회 + K_GRID 각 점 rich 스윕(N_SIZES 평균):
     causal_power = frozen poke(≤16) → OTHER region downstream |Δrate| 평균.
     동시 per-K mean fire_frac 기록(포화 진단).
  4. spike-streamer.service START (원상복구 · is-active=active 확인).
```

run: 11:57:56 → 12:11:31 UTC (~13.5분) · on_hardware=True · BC.00.000.002 · SDK 2.19.1.

## 5. 결과 (seed=187 · live AKD1000)

```
collapse floor = 0.0000  (결정적 silent-others · 통합 부재)
  K      Δ=cp_rich   fire_frac
 0.0     0.03989     0.156    cold end (약결합 · 부분발화)
 1.0     0.10215     0.210  ◀ K* PEAK (interior · edge-of-chaos)
 2.0     0.06094     0.459    하강 어깨
 3.0     0.03477     0.937    ← axis-B 원래 rich 점 (이미 포화 어깨)
 4.0     0.01278     0.977
 6.0     0.00521     0.986
 9.0     0.00339     0.990
13.0     0.00217     0.992
18.0     0.00211     0.993
24.0     0.00171     0.994    saturate end (all-fire · poke 무효)

3-check: band_exists=True(peak 0.1021 > eps ∧ K*=1.0 interior) ·
         cold_rolloff=True(0.0399 < 0.0919) · sat_rolloff=True(0.0017 < 0.0919) ·
         monotone=False  →  VERDICT 🟢 PASS
```

## 6. 해석 / 함의

- **측도는 bounded edge-of-chaos band 에 산다.** coupling K↑ 에 따라 mean fire_frac 가 0.156→0.994 단조상승하고, Δ(K)는 발화가 부분적인 곳(K≈1, fire ~0.21)에서 PEAK, 칩이 포화(fire→~0.99, 전 unit ON-고정)하는 즉시 붕괴 — poke 가 downstream 을 못 흔든다. 양끝 실패가 기전적으로 깨끗하다.
- **axis B 원래 rich(K=3)는 이미 포화 어깨**(fire 0.94)였다 — 진짜 동작 최적은 훨씬 약한 결합(K≈1). HW transfer 의 🟢 는 monotone 증가가 아니라 **regime property**: 칩은 edge-of-chaos band 안에서만 통합을 certify 한다.
- **axis A 🔴(H_856) 불변**: 본 특성화는 axis B(live HW) 🟢 를 정밀화할 뿐 production d512 falsification 을 되살리지 않는다.

## 7. scope (정직)

- region/coarse proxy (exact big-Φ 미주장). single seed(187, 사전등록) · H_856 과 동일 silicon. K* 위치는 그리드 해상도 bound(peak 가 K=0~2 사이, K=1 에서 표집). collapse floor=0 = 결정적 on-chip floor.
- 측정rung=배포rung(같은 AKD1000)에서 측도가 operational 한 결합 band 를 처음 경계지음. CERTIFY-NOT-MEASURE(§12.8 백로그 #3)에 대한 정밀 입력: 측도는 production-width SW(axis A 🔴)에선 실패하나, 배포 칩 edge-of-chaos band(axis B·본 H)에선 regime 으로 동작.

## 8. 산출물

- harness: `CLM/msweep/clm_causal_band.{hexa,py}` (frozen measure_sweep.py import · 재튜닝 0)
- verdict: `.verdicts/857_clm_causal_band/F-CLM-CAUSAL-BAND.txt` + `hw_band_run_2026_05_30.json` (raw)
- CLAIMS: `clm_causal_band_hw_green` (CLAIMS.tape)
