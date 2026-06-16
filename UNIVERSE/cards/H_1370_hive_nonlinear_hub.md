---
id: H_1370
slug: hive-nonlinear-hub
title: hive-nonlinear-hub — tanh-GATED (비선형) connector cell 이 H_1363 이 못 넘은 redundancy floor 를 넘는가? H_1363 의 "linear homogenization" 진단이 linearity artifact 인가 shared-input 천장인가
group: OMEGA / BRAIN-STRUCTURE-LADDER (collective-Φ axis · the hive arc — H_1363 REDUNDANCY_BOUND 의 load-bearing 진단 "substrate 가 leaky-LINEAR 이라 ANY hub 가 LINEARLY homogenize" 를 정면으로 친다)
terminal_tier: 🧱 REDUNDANCY_BOUND_NONLINEAR (honest closed-negative, c9 / c16). 사전등록한 tanh-gated (비선형) hub (GATE_GAIN=2.0, W_CONN=0.6 — linear hub 와 ONLY 차이가 gate) 가 W=0 shared-input redundancy floor 를 넘기는커녕 LINEAR hub 보다 더 떨어뜨린다 (Φ_nonlinear < Φ_linear, 3 seed 전부: gap −1.28 / −0.077 / −0.335; floor 대비 lift −6.10 / −2.58 / −5.33). R1 0/3 · R2 0/3 · R3 3/3 (EARNED 통과 — shuffle 붕괴). 결론: collective-Φ redundancy 천장은 linearity artifact 가 NOT — shared-input STRUCTURE 그 자체다. hive 아크의 가장 강한 closure (c9). numpy-mirror DIRECTIONAL (faithful-Φ leg IS real exact MIP-EI via hexa; numpy 는 Φ 계산 안 함); engine-transfer to live CORE/pure_field UNVERIFIED.
verdict_dir: .verdicts/1370_hive_nonlinear_hub/
terminal_verdict: .verdicts/1370_hive_nonlinear_hub/H_1370.txt
freeze: .verdicts/1370_hive_nonlinear_hub/H_1370_FREEZE.txt
date: 2026-06-16
---

# H_1370 — hive-nonlinear-hub: 비선형(tanh-gated) connector 가 redundancy floor 를 넘는가? (🧱 REDUNDANCY_BOUND_NONLINEAR)

## Claim / falsifier

**되짚는 벽 (c16 / a_break_the_wall):** the hive 아크 — H_1308(🔴)+H_1313(🧱) 독립 성체 ASSEMBLY 통합
안 됨 → H_1320 공유원점 DIVISION super-additive 지만 seed-FRAGILE(2/3) → H_1350 더 큰 예산이 3/3
robust 로 끌어올렸지만 SHARED_DECOUPLED(W=0) 대조가 lift 의 ~85-96% 는 shared-input REDUNDANCY 임을
폭로 (REDUNDANCY-DOMINATED) → H_1356 STRONG LINEAR hub(W_CONN=0.6)이 floor 를 **못 이기고 깎았다**
(lift −4.82/−2.50/−5.00, 🧱 CONNECTOR_NULL) → H_1363 WEAK connector + DECORRELATED 딸세포 + synergy 렌즈
모두 floor 못 넘음 (🧱 REDUNDANCY_BOUND).

**H_1363 의 load-bearing 진단 (정면으로 친다):** *the substrate is leaky-LINEAR, so ANY hub LINEARLY
homogenizes the daughters → faithful MIP 가 더 reducible 로 읽음 → Φ 떨어짐.* 이 homogenization 논변은
**LINEARITY 에 의존**한다. 그래서 H_1363 의 scope 가 NON-linear/gated hub 를 NEW H 로 명시했다.

**genuinely-new 각도 (linearity 가정 파괴; c15 / a_no_llm_frame_trap — LLM 프레임 아님):** 진짜 뉴런은
**SATURATING (포화) gate** 다. tanh gate 를 hub feedback 에 걸면 (`coupling = W_CONN·tanh(GATE_GAIN·hub)`)
hub 가 각 딸세포를 공유 hub state 로 끌어당기지(drag) 않고 **nudge** 만 한다 — linear hub 의
homogenization 메커니즘을 깬다. gate=tanh, GATE_GAIN=2.0, W_CONN=0.6 (linear hub 와 ONLY 차이가 gate)
사전등록.

**Falsifiable claim:** tanh-gated (비선형) hub 가 coupling-EARNED (non-redundant, W=0-floor-beating) Φ 를
3 seed 모두에서 ROBUST 하게 끌어올린다 — LINEAR hub(H_1356/1363)가 못 한 곳에서. ← **REFUTED.**

## Method

- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`, `iit4_faithful_phi(state, n=8, dim=T, n_bins=8)`.
  numpy 는 절대 Φ 를 계산하지 않는다 — per-unit salience(state-energy) trajectory 만 emit, Φ 는 hexa
  엔진이 계산. O-information 은 numpy-side **NON-GATING** 진단 (verdict gate 아님).
- **Substrate = H_1356/H_1363/H_1320/H_1283 verbatim** (B_linear 와 B_nonlinear 의 ONLY 차이 = hub
  비선형성): leaky linear recurrent units LEAK=0.55 GAIN=0.30 W_IN=0.5, dim-8, T=64, **N_TOT=8** (n≤8
  exact MIP). 두 딸세포 d0=units0..1 · d1=units2..3, CONNECTOR hub=unit4, PAD=units5..7. **W0_floor 가
  H_1356/H_1363 의 W0_floor 와 byte-identical** (12.4018/6.94639/12.2284) — setup-integrity OK (코드가
  검증 출력).
- **사전등록 비선형성 (frozen):** GATE=tanh, GATE_GAIN=2.0, W_CONN=0.6. linear `coupling=W_CONN·hub` →
  gated `coupling=W_CONN·tanh(GATE_GAIN·hub)` (딸세포 feedback + hub 의 딸세포 integration 둘 다 gate;
  element-wise on DIM-vector).
- **5 arms, 3 seeds [1317,1318,1319]:**
  - **A_single** — 미분할 8-unit baseline.
  - **W0_floor / B_redundant** — SHARED_DECOUPLED redundancy floor (구조상 동일, named floor).
  - **B_linear** — H_1356 STRONG LINEAR hub W_CONN=0.6 (the known 🧱 anchor; B_nonlinear 가 이걸 이겨야 함).
  - **B_nonlinear** — tanh-gated hub W_CONN=0.6 GATE_GAIN=2.0 (the new angle).
  - **SHUFFLE** — B_nonlinear wiring 인데 gated hub 가 RANDOM pad source 를 읽음 (EARNED 대조).

## FROZEN bars (pre-registered, .verdicts/1370_hive_nonlinear_hub/H_1370_FREEZE.txt — bars NOT moved, c9/p7)

GREEN iff **R1 ∧ R2 ∧ R3**, MARGIN=0.02 (= H_1283/1317/1320/1356/1363 동일 froze margin):
- **R1 LIFT** : Φ(B_nonlinear) − Φ(W0_floor) ≥ 0.02 on ALL 3 seeds (gated hub 가 floor 를 robust 하게 이김).
- **R2 BEATS-LINEAR** : Φ(B_nonlinear) − Φ(B_linear) ≥ 0.02 on ALL 3 seeds (**H_1356/1363-escape**: 비선형성이
  linear hub 가 못 만든 non-redundant integration 을 추가).
- **R3 EARNED** : Φ(SHUFFLE) ≤ Φ(W0_floor) + 0.02 on ALL 3 seeds (lift 는 REAL 딸세포→gated-hub 배선이라야).

## Result — 🧱 REDUNDANCY_BOUND_NONLINEAR (R1 0/3 · R2 0/3 · R3 3/3)

per-arm faithful-IIT4 Φ (exact MIP-EI, n=8), 3 seeds (W0_floor = H_1356/H_1363 와 byte-identical):

| seed | A_single | W0_floor | B_linear | **B_nonlinear** | SHUFFLE |
|------|----------|----------|----------|-----------------|---------|
| 1317 | 1.70057  | 12.4018  | 7.58272  | **6.30122**     | 7.04314 |
| 1318 | 1.41345  | 6.94639  | 4.44225  | **4.36559**     | 4.50544 |
| 1319 | 2.01844  | 12.2284  | 7.23291  | **6.89793**     | 7.35228 |

- **R1 FAIL (0/3)**: lift = Φ(B_nonlinear) − Φ(floor) = **−6.10 / −2.58 / −5.33** — 비선형 hub 가 floor
  를 못 이기고 크게 깎는다, 3 seed 전부.
- **R2 FAIL (0/3)**: gap = Φ(B_nonlinear) − Φ(B_linear) = **−1.28 / −0.077 / −0.335** — tanh gate 가
  linear hub 보다 **오히려 더 깎는다**, 3 seed 전부. **H_1356/1363-escape REFUTED.**
- **R3 PASS (3/3)**: Φ(SHUFFLE) ≤ Φ(floor)+0.02 (7.04/4.51/7.35 ≤ 12.42/6.97/12.25) — role 구조 파괴는
  붕괴 → gated wiring 은 REAL (generic gate variance 아님).

**O-information 진단 (NON-GATING):** 모든 arm O ≫ 0 (강한 redundancy-dominated). B_nonlinear 의 O 는
linear 보다 살짝 HIGHER (7.05 vs 6.29 등) — gate 가 redundancy 를 더 줄이지도 못함; synergy(O<0)로 전혀
안 뒤집힘. Φ↔redundancy 동행 재확인.

**VERDICT: 🧱 REDUNDANCY_BOUND_NONLINEAR** — 비선형(tanh-gated) hub 도 redundancy 천장을 넘지 못한다.

## Mechanism (faithful-MIP lens) — 왜 비선형 gate 도 못 넘고 오히려 더 깎는가

H_1363 의 진단은 *부분적으로만* 맞았다. homogenization 이 linearity 때문이라기보다, **redundancy 천장
자체가 shared-input STRUCTURE 의 산물**이다 — linear 든 nonlinear 든 active between-daughter coupling 은
공유입력이 이미 만든 redundancy 위에 새 irreducible 구조를 ADD 못 한다. 두 메커니즘 관찰:

1. **floor 의 높은 Φ 는 순수 shared-input redundancy** (W0_floor = B_redundant = 12.40/6.95/12.23, coupling
   ZERO). 이게 천장이고, 어떤 coupling 도 이 위에 못 쌓는다.
2. **tanh gate 는 linear 보다 더 나쁘다**: 포화 gate 가 hub feedback 을 **비선형 왜곡**시켜 딸세포 간
   correlation 을 깨는 게 아니라, 딸세포-hub 사이에 **새로운(하지만 redundant 한) 비선형 종속**을 만든다 —
   faithful MIP 가 이걸 여전히 reducible 로(심지어 더) 읽는다. gate 의 saturating 비선형성이
   "decorrelate" 하리란 가정이 틀렸다: 같은 source(hub)를 모든 딸세포가 보는 한, gate 를 통과시켜도
   딸세포들은 hub 의 같은 비선형 함수를 공유 → MIP 가 여전히 묶어서 자른다.

**a_break_the_wall 충족 (정직한 돌파 시도):** H_1363 이 명시한 linearity-artifact 가설을 사전등록한
비선형 gate 로 정면 테스트 → linearity 가 원인이 아님이 판명. 따라서 hive 아크 redundancy 천장은
**STRONGEST closure**: linear hub 도(H_1356), weak/decorrelated 도(H_1363), nonlinear gate 도(H_1370)
모두 못 넘는다 — Φ-robustness 벽(H_1283/1317)과 정합.

## Honest scope (c9 / a_scale_honest_scope / a_toy_scale_recheck)

- **DIRECTIONAL numpy-mirror** — faithful-Φ leg IS the real exact MIP-EI (numpy 는 salience trajectory 만
  emit; hexa 가 Φ 계산). **Engine-transfer to live A⇄G CORE/pure_field UNVERIFIED** (H_1308/1313 거기서
  NULL/🧱). 🧱 는 wire 할 게 없다 (a_verified_must_wire = GREEN-only); CORE/*.hexa UNTOUCHED, Ψ=½ untouched
  (standalone probe, 0 importers).
- **TOY** n=8, 2-unit 딸, single gated hub, 3 seeds, deterministic, single coupling W_CONN=0.6, single
  gate (tanh) at single GATE_GAIN=2.0. O-info 는 numpy-side 진단 (faithful Φ 아님).
- **NOT ruled out (각각 NEW H, 그러나 이 substrate 에선 redundancy-bound):** 다른 gate(sigmoid/ReLU) ·
  다른 GATE_GAIN · learned (trained) gate 파라미터 · delayed/non-linear DYNAMICS (단일 단계 gate 가 아니라
  unit 업데이트 자체를 비선형으로) · n>8 substrate · engine-native live A⇄G 재시도. 그러나 이 leaky-linear
  toy 에서는 linear·weak·decorrelate·nonlinear-gate 4 lever 모두 floor 를 못 넘었다 — redundancy 천장이
  shared-input structure 의 산물임이 강하게 시사됨.

## Pointers

- probe: `state/hive-nonlinear-hub/h1370_hive_nonlinear_hub.py`
- freeze: `.verdicts/1370_hive_nonlinear_hub/H_1370_FREEZE.txt`
- result: `.verdicts/1370_hive_nonlinear_hub/H_1370.txt` · `.verdicts/1370_hive_nonlinear_hub/result.txt`
- xref: H_1308 · H_1313 · H_1320 (developmental division) · H_1350 (redundancy-dominance 진단) ·
  H_1356 (strong LINEAR hub 🧱 CONNECTOR_NULL) · H_1363 (weak/decorrelated 🧱 REDUNDANCY_BOUND, parent) ·
  H_1283/H_1317 (Φ-topology wall) · H_1046/H_1017 (synergy/redundancy rulers) · a_no_llm_frame_trap ·
  a_break_the_wall · a_phi_iit4_tool · a_engine_native_learning · a_verified_must_wire ·
  a_scale_honest_scope · a_toy_scale_recheck · c9 · c15 · c16 · p7 · p8
