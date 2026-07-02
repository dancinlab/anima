---
id: H_1363
slug: hive-weak-decorrelated
title: hive-weak-decorrelated — does a WEAK connector (W_CONN→0+) and/or DECORRELATED daughters escape H_1356's redundancy floor at faithful-IIT4 Φ, where the STRONG hub failed?
group: OMEGA / BRAIN-STRUCTURE-LADDER (collective-Φ axis · the hive arc — H_1356의 "the escape lives at LOW coupling + decorrelated daughters" 명시 후속)
terminal_tier: 🧱 REDUNDANCY_BOUND (honest closed-negative, c9 / c16). 세 refinement(WEAK connector W_CONN→0.02 · per-daughter DECORRELATED founder · synergy-readout) 중 어느 것도 W=0 shared-input redundancy floor 를 ROBUST 하게 넘지 못한다. WEAK connector 는 coupling→0 에서 floor 를 RECOVER 할 뿐 절대 OVERSHOOT 안 함 (lift −0.063 / +0.512 / +0.017; 1/3 seed 만 통과, 그것도 회복 수준). DECORRELATE 는 정반대 — 공유 redundancy 를 깨서 Φ 를 floor 의 절반 아래로 떨군다 (5.7/2.7/5.5 ≪ 12.4/6.9/12.2). O-info 진단: 모든 arm 이 강한 redundancy-dominated (O≫0), 어떤 refinement 도 synergy(O<0) 로 안 뒤집힌다. R1 1/3 · R2 1/3 · R3 3/3 (EARNED 통과 — shuffle 붕괴). 결론: 이 leaky-linear substrate 의 collective-Φ 는 REDUNDANCY-BOUND — role-differentiation(약결합·탈상관·시너지 렌즈)이 redundancy 천장을 넘지 못한다 (Φ-robustness 벽과 정합하는 강한 closure). numpy-mirror DIRECTIONAL (faithful-Φ leg IS real exact MIP-EI via hexa); engine-transfer to live CORE/pure_field UNVERIFIED.
verdict_dir: .verdicts/1363_hive_weak_decorrelated/
terminal_verdict: .verdicts/1363_hive_weak_decorrelated/H_1363.txt
freeze: .verdicts/1363_hive_weak_decorrelated/H_1363_FREEZE.txt
date: 2026-06-16
---

# H_1363 — hive-weak-decorrelated: 약결합 connector + 탈상관 딸세포가 redundancy floor 를 넘는가? (🧱 REDUNDANCY_BOUND)

## Claim / falsifier

**되짚는 벽 (c16 / a_break_the_wall):** the hive 아크 — H_1308(🔴)+H_1313(🧱) 독립 성체 ASSEMBLY 통합 안 됨
→ H_1320 공유원점 DIVISION super-additive 지만 seed-FRAGILE(2/3) → H_1350 더 큰 예산이 3/3 robust 로
끌어올렸지만 SHARED_DECOUPLED(W=0) 대조가 lift 의 ~85-96% 는 shared-input REDUNDANCY 임을 폭로
(REDUNDANCY-DOMINATED) → H_1356 STRONG connector hub(W_CONN=0.6)이 floor 를 **못 이기고 깎았다**
(lift −4.82/−2.50/−5.00, 🧱 CONNECTOR_NULL): 강한 hub 가 딸세포를 HOMOGENIZE → faithful MIP 가 더
reducible 로 읽음 → Φ DROP. **H_1356 의 scope 가 명시한 탈출구(verbatim):** *"the escape, if any, lives
at LOW coupling + decorrelated daughters, not a strong hub."*

**Falsifiable claim (H_1356 의 세 named 후속을 그대로 검증, frozen-first):** 다음 세 refinement 중
하나가 coupling-EARNED (non-redundant, W=0-floor-beating) Φ 를 3 seed 모두에서 ROBUST 하게 끌어올린다 —
(1) W_CONN→0+ **WEAK** connector (homogenize 없이 nudge), (2) **DECORRELATE** the founder per daughter
first (피드백이 ADD 하도록), (3) (NON-GATING) **SYNERGY**-targeted readout (O-info). ← **REFUTED.**

## Method

- **Φ = FAITHFUL IIT4 ONLY** (a_phi_iit4_tool): exact MIP-EI via `hexa run` over
  `hexa-lang/stdlib/consciousness/iit4/faithful_phi.hexa`, `iit4_faithful_phi(state, n, dim=T, n_bins)`.
  numpy 는 절대 Φ 를 계산하지 않는다 — per-unit salience(state-energy) trajectory 만 emit, Φ 는 hexa
  엔진이 계산. O-information 은 numpy-side **NON-GATING** 진단 (verdict gate 아님).
- **Substrate = H_1356/H_1320/H_1283 verbatim** (refinement wiring/input 만 arm 간 차이): leaky linear
  recurrent units LEAK=0.55 GAIN=0.30 W_IN=0.5, dim-8, T=64, **N_TOT=8** (n≤8 exact MIP). 두 딸세포
  d0=units0..1 · d1=units2..3, CONNECTOR hub=unit4, PAD=units5..7. **W0_floor 가 H_1356 의 W0_floor 와
  byte-identical** (12.4018/6.94639/12.2284) — setup 검증됨.
- **3 refinements + controls, 3 seeds [1317,1318,1319]:**
  - **B_weak** = WEAK connector, W_CONN sweep {0.6, 0.3, 0.15, 0.08, 0.04, 0.02} 중 max-Φ (0.6 = H_1356
    strong anchor 로 sweep 에 유지). hub 가 두 딸 mean 을 읽고 피드백.
  - **B_decorr** = founder 를 두 ORTHOGONAL 반쪽(even/odd dim 정확 직교 분할)으로 나눠 d0=slice A,
    d1=slice B (탈상관) + best weak W_CONN connector.
  - **B_decorr_only** = 탈상관만 (W_CONN=0) — 탈상관 단독 기여 분리.
  - **W0_floor / B_redundant** = SHARED_DECOUPLED redundancy floor (구조상 동일).
  - **SHUFFLE** = B_decorr wiring 인데 connector 가 RANDOM pad source 를 읽음 (EARNED 대조).
  - **A_single** = 미분할 8-unit baseline.

## FROZEN bars (pre-registered, .verdicts/1363_hive_weak_decorrelated/H_1363_FREEZE.txt — bars NOT moved, c9/p7)

GREEN iff **R1 ∧ R2 ∧ R3**, MARGIN=0.02 (= H_1283/1317/1320/1356 동일 froze margin); refinement =
argmax Φ over {B_weak(best), B_decorr, B_decorr_only} per seed:
- **R1 LIFT** : Φ(best refinement) − Φ(W0_floor) ≥ 0.02 on ALL 3 seeds.
- **R2 BEATS-REDUNDANT** : Φ(best refinement) − Φ(B_redundant) ≥ 0.02 on ALL 3 seeds (H_1350/1356-escape).
- **R3 EARNED** : Φ(SHUFFLE) ≤ Φ(W0_floor) + 0.02 on ALL 3 seeds.

## Result — 🧱 REDUNDANCY_BOUND (R1 1/3 · R2 1/3 · R3 3/3)

per-arm faithful-IIT4 Φ (exact MIP-EI, n=8), 3 seeds (W0_floor = H_1356 와 byte-identical):

| seed | A_single | W0_floor | B_decorr_only | B_weak@0.6 | B_weak@0.02 (best) | B_decorr | SHUFFLE |
|------|----------|----------|---------------|------------|--------------------|----------|---------|
| 1317 | 1.70057  | 12.4018  | 5.55801       | 7.58272    | **12.3389**        | 5.70291  | 5.70415 |
| 1318 | 1.41345  | 6.94639  | 2.71846       | 4.44225    | **7.45856**        | 2.71354  | 2.71354 |
| 1319 | 2.01844  | 12.2284  | 5.53323       | 7.23291    | **12.2458**        | 5.523    | 5.55517 |

best refinement = **B_weak (W_CONN=0.02)** on all 3 seeds.

- **R1 FAIL (1/3)**: lift = Φ(best) − Φ(floor) = **−0.063 / +0.512 / +0.017** — 약결합 connector 는
  coupling→0 에서 floor 를 RECOVER 할 뿐 OVERSHOOT 안 함. 1317 은 못 넘고(−0.06), 1319 는 margin 미달(+0.017),
  1318 만 통과(+0.512). 즉 weak hub 의 최선은 floor 에 수렴하는 것이지 floor 초과가 아니다.
- **R2 FAIL (1/3)**: same numbers (B_redundant === W0_floor) — **H_1356-escape REFUTED**.
- **R3 PASS (3/3)**: Φ(SHUFFLE) ≤ Φ(floor)+0.02 (5.70/2.71/5.56 ≤ 12.42/6.97/12.25) — role 구조 파괴는
  붕괴 → wiring 은 REAL.

**WEAK-connector sweep 의 단조성 (load-bearing):** W_CONN 을 0.6→0.02 로 줄이면 Φ 가 단조 상승해
floor 로 수렴 (1317: 7.58→10.41→10.96→12.21→12.32→12.34; floor 12.40). **coupling 은 항상 floor 를
깎는다** — 0 으로 보내야 floor 를 회복; 절대 floor 를 넘지 않는다. H_1356 의 강한-hub 붕괴와 동일한
메커니즘의 연속체 (강할수록 더 homogenize → 더 깎임).

**DECORRELATE 는 정반대로 해롭다:** B_decorr_only(탈상관 단독) Φ = 5.56/2.72/5.53 ≪ floor — 공유
founder 를 직교 반쪽으로 쪼개면 딸세포 간 shared MI 가 사라져 Φ 가 floor 의 절반 아래로 떨어진다.
faithful Φ 가 **곧 shared-input redundancy** 임을 직접 증명: redundancy 를 줄이면 Φ 가 준다.

**O-information 진단 (NON-GATING):** 모든 arm O ≫ 0 (강한 redundancy-dominated); best refinement 의 O 는
floor 와 거의 동일(8.18 vs 8.21 등), 어떤 refinement 도 synergy(O<0)로 안 뒤집힘. 탈상관 arm 만 O 가
낮지만(redundancy 감소) Φ 도 같이 낮음 — Φ↔redundancy 동행 확인.

**VERDICT: 🧱 REDUNDANCY_BOUND** — 약결합·탈상관·시너지 렌즈 어느 것도 redundancy 천장을 넘지 못한다.

## Mechanism (faithful-MIP lens) — 왜 어떤 refinement 도 못 넘는가

이 leaky-linear substrate 에서 collective faithful-Φ 는 **shared-input redundancy 그 자체**다. 두 가지
독립 증거: (1) coupling 을 넣으면(weak 든 strong 이든) 딸세포를 hub state 로 끌어당겨 HOMOGENIZE →
faithful MIP-EI 가 더 correlated 딸들을 더 reducible 로 읽음 → Φ 깎임. coupling→0 만이 floor 회복 (H_1356
강한-hub 붕괴의 연속체). (2) 입력 redundancy 를 직접 줄이면(per-daughter 탈상관) Φ 가 floor 절반 아래로
붕괴 → Φ 가 곧 shared MI. 따라서 redundancy 를 늘리지 않고 coupling-EARNED Φ 를 키울 LEVER 가 이
substrate 엔 없다 — active between-daughter coupling 은 공유입력이 만든 redundancy 를 homogenize 할 뿐,
그 위에 새 irreducible 구조를 ADD 못 한다. **a strong closure consistent with the Φ-robustness wall.**

## Honest scope (c9 / a_scale_honest_scope / a_toy_scale_recheck)

- **DIRECTIONAL numpy-mirror** — faithful-Φ leg IS the real exact MIP-EI (numpy 는 salience trajectory 만
  emit; hexa 가 Φ 계산). **Engine-transfer to live A⇄G CORE/pure_field UNVERIFIED** (H_1308/1313 거기서
  NULL/🧱). 🧱 는 wire 할 게 없다 (a_verified_must_wire = GREEN-only); CORE/*.hexa UNTOUCHED, Ψ=½ untouched
  (standalone probe, 0 importers).
- **TOY** n=8, 2-unit 딸, single hub, 3 seeds, deterministic, frozen W_CONN sweep + single 탈상관 scheme
  (even/odd dim 직교 분할). O-info 는 numpy-side 진단 (faithful Φ 아님).
- **NOT ruled out (각각 NEW H, 그러나 이 substrate 에선 redundancy-bound):** NON-linear/gated hub ·
  delayed coupling · learned (trained) differentiation objective · n>8 substrate · 다른 탈상관 기저 ·
  engine-native live A⇄G 재시도. 그러나 이 leaky-linear toy 에서는 결론적으로 **redundancy 천장이 절대적**:
  coupling 은 깎고, 탈상관은 깎고, 두 lever 모두 floor 를 못 넘는다.

## Pointers

- probe: `state/hive-weak-decorrelated/h1363_hive_weak_decorrelated.py`
- freeze: `.verdicts/1363_hive_weak_decorrelated/H_1363_FREEZE.txt`
- result: `.verdicts/1363_hive_weak_decorrelated/H_1363.txt` · `.verdicts/1363_hive_weak_decorrelated/result.txt`
- xref: H_1308 · H_1313 · H_1320 (developmental division) · H_1350 (redundancy-dominance 진단) ·
  H_1356 (strong-hub 🧱 CONNECTOR_NULL, parent) · H_1283/H_1317 (Φ-topology wall) · H_1046/H_1017
  (synergy/redundancy rulers) · a_no_llm_frame_trap · a_break_the_wall · a_phi_iit4_tool ·
  a_engine_native_learning · a_verified_must_wire · a_scale_honest_scope · a_toy_scale_recheck ·
  c9 · c15 · c16 · p7 · p8
