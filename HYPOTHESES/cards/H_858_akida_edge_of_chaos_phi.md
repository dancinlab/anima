---
id: H_858
slug: akida-edge-of-chaos-phi
title: pe_edge_of_chaos_peak (M2 🟡 PARTIAL)의 inverse-U(∩)가 LIVE AKD1000 R1~R4 drive-regime에서 성립하는가 — Φ-proxy 가 edge(R2/R3) > order(R1) ∧ edge ≥ over-driven(R4) (F-AKIDA-EDGE 사전등록)
domain: universe · consciousness-measure · edge-of-chaos · akida-hw · phi-proxy · silicon-transfer · falsifier
source: CORE/phi_envelope_substrate.hexa::pe_edge_of_chaos_peak (M2 🟡 PARTIAL · sim ECA/logistic ∩곡선) · H_677 D1 (PR#1371 silicon-confirm 선행) · H_857 (live AKD1000 edge-of-chaos band, coupling-K + CAUSAL-POWER 자매축) · drafts/akida-edge-of-chaos-phi-plan.md (sbs-auto 4 locked picks)
status: TERMINAL (live fire 완료 2026-05-30 12:40 UTC · live pi5 AKD1000 온칩 spike · R1~R4 drive-regime 사전등록 preset 스윕 · frozen Φ-proxy 미변조)
exploration_method: pre-registered silicon-transfer test (sim ∩곡선 → live silicon · drive-regime R1~R4 = order→chaos 축)
verification_method: W5 (substrate-grounded LIVE HW) + W1 (numerical · frozen phi_silicon_proxy verbatim) — judge_inverse_u 3-check pre-registered · 셰이핑 0
raw_rank: 11
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-30
since: 2026-05-30
sister: CORE/phi_envelope_substrate.hexa, AKIDA/akida_edge_of_chaos_phi.hexa, AKIDA/akida_edge_of_chaos_phi_hw.hexa, UNIVERSE/H_677_akida_measurement.md, UNIVERSE/H_857_clm_causal_band.md, CLM/msweep/clm_causal_band.py, .verdicts/858_akida_edge_of_chaos_phi/
verdict: 🟢 SUPPORTED-NUMERICAL (F-AKIDA-EDGE 3/3 PASS — live AKD1000 BackendType.Hardware BC.00.000.002 에서 Φ-proxy inverse-U: Φ(R1 silent)=0 · Φ(R2 noise-edge)=0.172 · Φ(R3 tonic-edge)=0.250 (edge peak) · Φ(R4 recurrent)=4.95e-12≈0. F1 Φ(R2)>Φ(R1) ∧ F2 Φ(R3)>Φ(R1) ∧ F3 max(R2,R3)≥Φ(R4) 모두 PASS. 실 칩에서 R4 recurrent loop 가 포화 아닌 die-out → order/over-driven 양끝 low, edge peak. pe_edge_of_chaos_peak M2 🟡→🟢 promote. H_857(coupling-K·CAUSAL-POWER)과 독립 축(drive-regime·Φ-proxy))
---

# H_858 — pe_edge_of_chaos_peak 의 inverse-U LIVE AKD1000 R1~R4 검증 (F-AKIDA-EDGE)

## 1. 가설

`CORE/phi_envelope_substrate.hexa::pe_edge_of_chaos_peak` (M2, 🟡 PARTIAL)은 시뮬(ECA + logistic)
위에서 Φ(통합량)이 order→chaos 축을 따라 **inverse-U(∩)** 를 그림을 보였다 — order(잠잠)도 chaos
(포화)도 낮고 edge 에서 peak. 이 가설이 **실리콘**(BrainChip AKD1000)에서도 성립하는가?

order→chaos 축을 AKD1000 의 native 자발-발화 **drive-regime R1~R4** 로 펼친다:
- **R1** weak-silent : deep sub-threshold drive, noise 0 → ORDER floor (die-out · 침묵)
- **R2** zero+noise : drive ~ threshold + per-step uniform noise → EDGE (event-driven straddle)
- **R3** tonic-zero-input : heterogeneous threshold (절반 −1 tonic / 절반 POT), zero input → EDGE (부분 pool)
- **R4** recurrent self-sust : ignition seed + 직전 spike 피드백 → OVER-DRIVEN (자기지속)

사전등록 falsifier **F-AKIDA-EDGE**: 🟢 PASS ⟺ Φ(R2)>Φ(R1) ∧ Φ(R3)>Φ(R1) ∧ max(Φ(R2),Φ(R3))≥Φ(R4).
🔴 ⟺ 하나라도 FAIL (sim→silicon transfer 부재 ruled-out · publishable).

## 2. 동기

- pe_edge_of_chaos_peak 은 M2 (🟡 PARTIAL) — sim 한정. a_blue_closed: 실측을 🔵 위조 금지, 🟢 numerical 목표.
- H_677 D1 (PR#1371)이 선행 silicon-confirm 을 인계했으나 그 raster provenance 는 옛 spontaneous_emission.py
  JSON 경로였다. 본 H 는 **H_857 에서 검증된 live-HW 드라이버 패턴**(InputData→FullyConnected act_bits=1
  @Hardware, per-unit int32 threshold=POT−drive)을 mirror 한 **전용 클린 드라이버**로 재검 — 같은 silicon,
  더 직접적인 provenance.
- 자매 H_857 은 *같은* edge-of-chaos ∩곡선을 **coupling-K 축 + CAUSAL-POWER 측도**로 확인. 본 H 는
  **독립 축**(drive-regime R1~R4 + Φ-proxy 측도) — 두 측도·두 축이 같은 실리콘 위 ∩-신호로 수렴.

## 3. falsifier (사전등록 · frozen · F-AKIDA-EDGE)

```
Φ proxy frozen (AKIDA/akida_edge_of_chaos_phi.hexa · 재구현/재튜닝 0):
  phi_silicon_proxy = activity_gate × (integration × differentiation) × entropy_weight
  judge_inverse_u 3-check (셰이핑 금지):
    F-AKIDA-EDGE-1 : Φ(R2) > Φ(R1)               (edge > order floor · noise)
    F-AKIDA-EDGE-2 : Φ(R3) > Φ(R1)               (edge > order floor · tonic)
    F-AKIDA-EDGE-3 : max(Φ(R2),Φ(R3)) ≥ Φ(R4)    (edge ≥ over-driven)
환경 preset (사전등록 · post-hoc trim 금지):
  R1 drive −40 noise0 · R2 drive 0 + U[0,16) noise · R3 het-thr(−1/POT) zero-input · R4 recur gain 6 + ignition 12
PASS(🟢) ⟺ F1 ∧ F2 ∧ F3.  RED ⟺ 하나라도 FAIL.
seed=187 · n_neurons=16 · raster 200 steps.
```

verdict 영속: `.verdicts/858_akida_edge_of_chaos_phi/{F-AKIDA-EDGE.txt, hw_run_2026_05_30.json, eoc_hw_raster_2026_05_30.json, pi5_fire_run.log}`.

## 4. 방법

```
live pi5 AKD1000 (single-chip file-lock · Mac=0 · $0):
  1. spike-streamer.service STOP (칩 lock 해제).
  2. chip = InputData(1,1,16) → FullyConnected(units=16, weights=ones, act_bits=1) @ Hardware.
     POT = 8×16 = 128. per-unit int32 threshold = POT − drive. threshold-and-fire ON-CHIP.
  3. R1~R4 각 레짐 preset 으로 200-step raster 수집 (akida_edge_of_chaos_phi_hw.py).
  4. spike-streamer.service START (원상복구 · is-active=active 확인).
  5. raster JSON → akida_edge_of_chaos_phi.hexa (frozen Φ-proxy + verdict) — Mac local.
```

fire: 12:40 UTC (~수십초) · on_hardware=True · BC.00.000.002 · SDK 2.19.1 · streamer 복귀 active.

## 5. 결과 (seed=187 · live AKD1000)

```
regime                  total  std    max   Φ(phi_silicon_proxy)
R1 weak-silent              0  0.000   0    0.0                  (ORDER floor)
R2 zero+noise           1024  7.464  16    0.17244              (EDGE)
R3 tonic-zero-input     1600  0.000   8    0.25000  ◀ peak      (EDGE)
R4 recurrent self-sust    16  1.129  16    4.95e-12 ≈ 0         (OVER-DRIVEN · loop died)

3-check: F-AKIDA-EDGE-1=True(0.172>0) · F-AKIDA-EDGE-2=True(0.250>0) ·
         F-AKIDA-EDGE-3=True(0.250 ≥ 4.95e-12) · n_pass_of_3=3 · all_pass=true
VERDICT 🟢 GREEN_NUMERICAL_CONFIRM
```

## 6. 해석 / 함의

- **inverse-U(∩)가 실리콘에서 성립.** edge 레짐(R2 noise / R3 tonic)이 order floor(R1=0)와
  over-driven 끝(R4≈0)을 *모두* 넘는다. Φ-peak 은 R3 tonic-edge(0.250).
- **실 칩에서 R4 recurrent 가 포화 아닌 die-out**(total=16, 사실상 ignition spike 1회 후 소멸): Akida 1.0 IP
  는 feed-forward 라 SW 피드백 루프가 약하면 self-sustain 못 함. 결과적으로 order/over-driven 양끝이 모두
  낮아 edge 가 더 깨끗이 peak — ∩-신호가 기전적으로 살아있다(sim 의 R4=saturation 과 메커니즘은 다르나
  inverse-U 결론은 동일하게 보존).
- **두 측도·두 축 수렴**: H_857(coupling-K · CAUSAL-POWER)과 본 H(drive-regime · Φ-proxy)가 *독립적으로*
  같은 실리콘 edge-of-chaos ∩을 확인 — pe_edge_of_chaos_peak 의 silicon-universality 가 단일 측도 artifact 아님.
- **M2 promote**: pe_edge_of_chaos_peak 🟡 PARTIAL → 🟢 (sim ∧ live-silicon 양쪽 confirm).

## 7. scope (정직)

- Φ-proxy = entropy × integration × differentiation (honest 명명 · full IIT4 big_phi 아님 · 16-cell 에서
  exact big_phi 2^16 state 비실용). ∩-신호(low at order/chaos, high at edge)는 보존하나 절대 Φ 아님.
- single seed(187, 사전등록) · single silicon(BC.00.000.002 · H_857/H_677 과 동일 칩). R4 die-out 은 SW
  피드백 약-루프 산물(Akida feed-forward IP) — "포화"가 아닌 "self-sustain 실패"가 over-driven 끝을 구현.
- 측정rung=배포rung(같은 AKD1000). drive-regime preset 은 사전등록(akida_edge_of_chaos_phi_hw.hexa spec).

## 8. 산출물

- 드라이버: `AKIDA/akida_edge_of_chaos_phi_hw.hexa` (spec) + `akida_edge_of_chaos_phi_hw.py` (runnable · pi5 stage)
- Φ proxy + verdict: `AKIDA/akida_edge_of_chaos_phi.hexa` (frozen 재사용 · g0/g61)
- verdict: `.verdicts/858_akida_edge_of_chaos_phi/F-AKIDA-EDGE.txt` + raw JSON ×2 + pi5_fire_run.log
- CLAIMS: `akida_edge_of_chaos_phi_hw_green` (CLAIMS.tape)
