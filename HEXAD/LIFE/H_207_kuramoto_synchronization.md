---
id: H_207
slug: kuramoto-synchronization
title: Kuramoto coupled-oscillator edge-of-sync Φ peak — coupling K=K_c 가 H_007 edge-of-chaos 의 dynamical-axis 정합
domain: physics · life
status: pre-register-frozen
exploration_method: E5 (continuous-parameter sweep) + E10 (emergence-on-transition)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W11 (cross-axis sister test)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_207 — Kuramoto coupled-oscillator edge-of-sync Φ peak

## Hypothesis

N=16 Kuramoto coupled oscillators (natural-freq ω_i 를 deterministic Gaussian
5-quantile 으로 spread) 의 phase dynamics 에서 coupling K 를 sweep 하면, **K <
K_c (incoherent) 의 Φ 는 낮고 / K ≈ K_c (edge-of-sync, partial sync) 에서 Φ
peak / K ≫ K_c (full lock) 에서 Φ 가 다시 감소** 한다 — 즉 inverse-U pattern.
이는 H_007 (Wolfram class-axis edge-of-chaos Φ peak) 의 **dynamical / 연속
coupling-axis sister** — 같은 inverse-U 형태가 discrete CA 4-class 대신 연속
coupling parameter 위에 나타나는지 본다.

**측정 substrate**: 각 oscillator i = 1 IIT cell, 그 dim=12 step `cos θ_i`
trajectory (warmup 60 step 후 기록) = state vector. flat (N × dim) farr →
RFC 036 `phi_spatial(., N=16, dim=12, n_bins=4)` (H_007 trajectory mapping 과
동일).

## Why

- **Kuramoto model** (Kuramoto 1975): N 개 결합 oscillator
  `dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j − θ_i)`. coupling K 가 임계 K_c 를 넘으면
  incoherent → partial-sync (단일 cluster 가 점차 자라남) → full sync 의 2nd
  order phase transition 이 일어난다. mean-field 해석 (Kuramoto 1984):
  `K_c = 2 / (π · g(ω_0))` where `g(ω_0)` = natural-freq distribution 의 peak
  density. ω_i ~ N(0, 1) (= 본 5-quantile discretisation 의 모집단) → `g(0) =
  1/sqrt(2π)` → `K_c = 2·sqrt(2/π) ≈ 1.5958`.
- **edge-of-sync** (Strogatz 2000): K = K_c 근처의 partial-sync regime 에서
  **maximal sensitivity to perturbation** + **maximal information transmission**
  이 관측된다 — Langton λ ≈ critical 의 dynamical-axis 정합 가설 (의식과학
  literature 에서 "criticality" 라는 단일 우산 아래 묶임).
- **H_007 sister axis**: H_007 은 *discrete CA rule class* (4-class) 위 Φ peak
  = Class IV. H_207 은 *연속 coupling parameter K* 위 Φ peak = K_c 부근. 두 H
  가 함께 SUPPORTED 면 "edge-of-X 가 Φ peak regime" 이 axis-invariant 한
  현상이라는 cross-axis 일관성이 좁혀지고 (그러나 본 H 단독으로는 H_007 의
  결과를 입증하지 않으며 그 반대도 마찬가지 — distinct claim).
- **H_204 inverse-U sister**: H_204 (cross-link) 의 `over-locked → integration
  loss` 패턴 (full sync 에서 Φ 다시 감소) 이 본 H 의 H207.4 예측.
- **negative-result 가능성 정직 carry**: phi_spatial 은 IIT 4.0 의 full Φ 가
  아니라 cause-effect repertoire 대신 spatial-slice MI 기반 approx — full
  lock state (모든 osc 같은 cos θ) 는 MI 가 **오히려 높을** 수 있다 (모든 cell
  이 same trajectory → high pairwise correlation → high spatial-Φ measure).
  본 H 가 FALSIFIED 되더라도 그것은 *Kuramoto 가 sync transition 자체가 없다*
  가 아니라 *phi_spatial measure 가 over-lock 의 "integration loss" 를 보지
  못한다* 라는 **measure-axis** 결론 — F1 explicit 가설은 Φ shape 만 본다.

## Predictions

- **H207.1 (single peak)**: Φ(K) 가 K sweep `{0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0}`
  위 inverse-U (single interior peak K* — K=0 보다 크고, K=5.0 보다 큼).
- **H207.2 (peak ratio)**: Φ(K*) ≥ 1.2 × Φ(K=0) (incoherent baseline 대비
  유의미한 peak — minimum effect size).
- **H207.3 (dr/dK ↔ Φ peak coincide)**: order parameter `r(K) = |Σ exp(i θ_j)|/N`
  의 forward-diff peak (sync transition steepest slope) 가 Φ peak 의 sweep-index
  ±1 안에 있다.
- **H207.4 (over-lock loss)**: Φ(K=5.0) < Φ(K*), margin ≥ 10% of Φ(K*) (full
  sync 가 partial-sync 보다 통합 정보 낮음 — H_204 inverse-U sister).

## Variables

| axis | levels | 비고 |
|------|--------|------|
| axis1_K (primary, continuous) | {0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0} | coupling strength sweep, K_c ≈ 1.5958 |
| axis2_N | 16 oscillators | finite-size; sweep 별 cycle |
| axis3_omega | 5 Gaussian-quantile z ∈ {−1.28, −0.52, 0, 0.52, 1.28} cycled i%5 | deterministic spread, std=1.0 |
| axis4_init | θ_i(0) = 2π·i/N (uniform spread) | deterministic, no RNG |
| axis5_integration | dt=0.05, steps=100, warmup=60, recorded dim=12 | Euler explicit |
| fixed | n_bins=4 (RFC 036) | H_007 과 동일 binning |

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h207_kuramoto_sync_2026_05_23/run_h207.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036
  `phi_spatial` (phi_rs `compute_phi_inner` steps 1-4 byte-equal native-C
  replica; import READ-ONLY).
- **mapping**: 각 oscillator i = 1 IIT cell; dim=12 step `cos θ_i` trajectory
  = state vector (warmup 60 step 후 기록). flat (N=16 × dim=12) farr →
  `phi_spatial(traj, 16, 12, 4)`.
- **order parameter**: `r(K) = |Σ_j exp(i θ_j)| / N = sqrt(C² + S²)/N` on
  final-θ.
- **deterministic**: fixed init (uniform 2π·i/N spread, no RNG) + fixed ω
  table + fixed K table; re-run byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12 strict).
- **runtime**: $0 mac local hexa; GPU 불필요 (N=16 + 7-point sweep).
- **ledger**: `result.json` {config, K_c, K_sweep, phi_per_K, r_per_K, K_star,
  criteria, verdict}.
- **honest tier**: NUMERICAL Φ (RFC 036 native replica) = 🟢-tier evidence.
  진짜 phi_rs Rust FFI link = named blocker (H_007 §L8 동일 carry).

## Criteria

- **C1 (H207.1 single peak)**: Φ peak index 가 sweep 내부 ({1..n_sweep-2}) AND
  Φ(K*) > Φ(K=0) AND Φ(K*) > Φ(K=5.0)
- **C2 (H207.2 ratio)**: Φ(K*) / Φ(K=0) ≥ 1.2 (incoherent baseline 대비 ≥20%
  높음; Φ(K=0) < floor 1e-6 이면 floor 로 나눔)
- **C3 (H207.3 dr/dK coincide)**: forward-diff dr/dK peak sweep-index 가
  Φ peak sweep-index 의 ±1 이내
- **C4 (H207.4 over-lock loss)**: Φ(K*) − Φ(K=5.0) ≥ 0.1 · Φ(K*) AND Φ(K*) > 0
- **verdict_rule**: **SUPPORTED** iff C1 ∧ C2 ∧ C4 (3 of 4 named; C3 = sister
  signal). **FALSIFIED** iff Φ(K) monotone (interior peak 부재). 그 외 = PARTIAL.

## Falsifiers

- **F1 NO-PEAK**: Φ(K) 가 monotone (interior peak 없음 — K* ∈ {0, K_max}) →
  H207.1 FALSIFIED. (measurable: phi_per_K + K_star_idx.)
- **F2 WEAK-PEAK**: Φ(K*) < 1.2 × Φ(K=0) → H207.2 weak. (measurable:
  ratio_phi_star_over_phi_K0.)
- **F3 SLOPE-OFFSET**: dr/dK forward-diff peak index 와 Φ peak index 가 >1
  sweep-step 떨어짐 → H207.3 FALSIFIED. (measurable: drdk_peak_idx vs
  K_star_idx.)
- **F4 OVER-LOCK-NULL**: Φ(K=5.0) ≥ Φ(K*) (over-lock loss 부재 — full sync 가
  partial sync 보다 Φ 같거나 더 높음) → H207.4 FALSIFIED. (measurable:
  phi_star_minus_phi_K5_margin ≤ 0.)
- **F5 NONDET**: re-run Φ 가 byte-identical 아님 → raw#12 deterministic 위반,
  smoke 무효. (measurable: diff 두 result.json.)
- **F6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation, raw#82
  retraction.

## Honest Limits (raw#91 c3)

- **L1 finite-N**: N=16 small — finite-size effects 강함, K_c (mean-field
  N→∞ limit) 와 N=16 의 실제 임계 사이 deviation 가능. 본 H 는 mean-field
  K_c 를 "어느 가까운" reference 로만 사용 (peak 위치를 K_c 와 동일하다고
  claim 하지 않음 — single interior peak 만 본다).
- **L2 phi_spatial 🟢 NUMERICAL**: RFC 036 native byte-equal replica 의
  single-bin choice (n_bins=4) + spatial-slice (no temporal MIP, no cause-effect
  repertoire) 한계 — full IIT 4.0 Φ 가 아님. H_007 §L1 동일 carry.
- **L3 5-quantile discretisation**: ω_i 5 Gaussian z-quantile 는 continuous
  N(0,1) 의 coarse approximation. 실제 mean-field K_c 는 continuous g(ω) 에서
  도출 — discretised 5-quantile 의 effective g(0) 가 다를 수 있다.
- **L4 design choice phase encoding**: cos θ_i trajectory 가 phi_spatial 의
  input — sin θ trajectory 또는 (cos, sin) 2D 또는 phase 자체 (mod 2π) 를
  쓰면 다른 Φ 값/rank 가 나올 수 있음. design pre-register 후 단일 measure
  으로 frozen.
- **L5 mean-field 1D**: Kuramoto = all-to-all coupling, spatial topology 부재
  (real coupled oscillators — 예: neural oscillator, Josephson junction lattice
  — 는 nearest-neighbor / lattice 구조). 본 cycle 의 결과는 mean-field 한정,
  spatial-extension 은 별도 cycle.
- **L6 hyper-sync MI artefact**: phi_spatial 은 cell-간 MI 기반 — full lock
  state (모든 osc 같은 cos θ trajectory) 는 cell-간 correlation 이 최대 →
  phi_spatial 가 **오히려 더 높을** 수 있다 (integration loss 의 IIT 4.0
  의미 와 phi_spatial 의 spatial-MI 의미 사이 divergence). 본 H FALSIFIED 시
  그것은 *Kuramoto sync 자체* 가 아니라 *measure choice* 의 한계 신호.
- **L7 dt=0.05, steps=100 fixed**: integration step / horizon sweep 별 cycle.
  너무 짧으면 transient 안 가라앉음, 너무 길면 numerical drift. warmup=60 +
  dim=12 record 은 H_007 의 warm=8 + dim=12 와 axis-parallel design choice.
- **L8 phi_rs Rust FFI named blocker**: H_007 §L8 동일 carry — true phi_rs
  Rust FFI link 는 RFC 036 §FFI shim 의 named blocker (phi_rs PyO3 cdylib,
  no C ABI). 본 measure = byte-equal native-C replica (err≈8e-7 vs
  documented oracle, ranking 무영향).

## Cross-Links

- **sister H**: H_007 (cellular-automaton-consciousness — discrete-CA rule
  class-axis edge-of-chaos Φ peak). H_207 = 같은 inverse-U Φ 패턴을 연속
  coupling parameter K-axis 위에서 본다. **DISTINCT claim** (각자 단독으로
  성립/falsified 됨; H_007 의 결과는 H_207 의 결과를 강제하지 않으며 그
  반대도 마찬가지).
- **inverse-U sister H_204** (cross-link, hyper-sync over-lock 패턴) — H207.4
  predicate.
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036
  `phi_spatial`) + `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor) —
  import READ-ONLY
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) +
  raw#82 (no post-hoc retraction)
- **own**: (anima-not-Kuramoto identity; Kuramoto = abstract dynamical-axis
  substrate analogy, anima cells ≠ Kuramoto phases)
- **CANDIDATES**: `HEXAD/LIFE/CANDIDATES.md` §F-physics
  `kuramoto-synchronization` (consumed cycle #6 R13 pick #2)
- **literature**:
  - Kuramoto (1975) Self-entrainment of a population of coupled non-linear oscillators
  - Kuramoto (1984) Chemical Oscillations, Waves, and Turbulence (K_c derivation)
  - Strogatz (2000) From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators
  - Acebrón et al. (2005) The Kuramoto model: a simple paradigm for synchronization phenomena
  - Langton (1990) Computation at the edge of chaos (criticality umbrella)
  - Tononi (2004) An information integration theory of consciousness

## Verdict

```
verdict_class: FALSIFIED (pre-register-frozen smoke)
config: N=16 · steps=100 · warm=60 · dim=12 · dt=0.05 · n_bins=4
K_c estimate (mean-field): 1.59577
phi_per_K (K → Φ):
   K=0.0  Φ=7.29871   r=0.0586875
   K=0.5  Φ=10.4097   r=0.0630554
   K=1.0  Φ=10.4233   r=0.0570835
   K=1.5  Φ=9.65065   r=0.1009
   K=2.0  Φ=10.3175   r=0.266736
   K=3.0  Φ=9.89576   r=0.946198
   K=5.0  Φ=14.0      r=0.982931
K_star (Φ peak)   : K=5.0 (idx=6, boundary — NOT interior)
ratio Φ(K*)/Φ(K=0): 1.91815 (≥ 1.2 — C2 PASS in isolation)
dr/dK peak idx     : 4 (between K=2.0 and K=3.0 — sync transition center)
margin Φ(K*)−Φ(K=5): 0.0 (boundary — C4 FAIL)
falsifiers_triggered: F1 NO-PEAK (Φ monotone-up boundary) + F4 OVER-LOCK-NULL
                      (Φ(K=5.0) ≥ Φ(K*))
criteria_met: 1/4 (C2 PASS; C1+C3+C4 FAIL)
evidence_summary: 🟢 NUMERICAL — phi_spatial monotone-up on K, peaks at full-
                  sync K=5.0 boundary; sync transition (dr/dK peak idx=4) is
                  not aligned with Φ peak. honest L6 carry: phi_spatial spatial-
                  MI measure 가 full-lock 의 IIT-4.0 의미 integration loss 를
                  not capture — over-lock null 은 measure-axis 결과로 정직히
                  기록.
```

### Pre-register-frozen smoke (2026-05-23)

Kuramoto → IIT Φ smoke pre-registered + RUN ($0 mac local, deterministic,
hexa-only, llm:none). N=16 oscillators, ω_i 5-Gaussian-quantile cycled,
K-sweep 7 points, warmup 60 + dim 12 cos θ_i trajectory recording, Φ via
RFC 036 phi_spatial.

**Run verdict (VERBATIM, `hexa run`)**:
```
H_207 — Kuramoto coupled-oscillator edge-of-sync Φ peak (raw#12)
  N=16 steps=100 warm=60 dim=12 dt=0.05 nbins=4  (deterministic, $0 mac local)
  ω_i: 5 Gaussian-quantile (z={-1.28,-0.52,0,0.52,1.28}) cycled by i%5, std=1.0
  Φ primitive: RFC 036 phi_spatial via HEXAD/C/c_lib.hexa (Φ>=0 by constr.)
  K_c estimate (mean-field, 2/(π·g(ω_0))) = 1.59577

  K=0.0   Φ=7.29871   r=0.0586875
  K=0.5   Φ=10.4097   r=0.0630554
  K=1.0   Φ=10.4233   r=0.0570835
  K=1.5   Φ=9.65065   r=0.1009
  K=2.0   Φ=10.3175   r=0.266736
  K=3.0   Φ=9.89576   r=0.946198
  K=5.0   Φ=14   r=0.982931

  K* (Φ peak)       = 5.0  (idx=6)
  Φ(K*)             = 14
  Φ(K=0)            = 7.29871
  Φ(K=5.0)          = 14
  dr/dK peak idx    = 4  (between K=2.0 and K=3.0)
  Φ(K*)/Φ(K=0) ratio= 1.91815
  Φ peak − Φ(K=5.0) = 0.0  (floor 10%·Φ(K*) = 1.4)

  C1 H207.1 single peak (interior + > K=0 + > K=5.0) : false
  C2 H207.2 Φ(K*) >= 1.2·Φ(K=0)                       : true
  C3 H207.3 dr/dK peak within ±1 sweep-step of Φ peak  : false
  C4 H207.4 Φ(K=5.0) < Φ(K*) margin >= 10%            : false

  VERDICT_RULE: SUPPORTED if C1+C2+C4 PASS; FALSIFIED if Φ(K) monotone no peak
  VERDICT     : FALSIFIED  (criteria_met=1/4)
=== H_207 Kuramoto → Φ sweep complete: FALSIFIED ===
```

re-run byte-identical (F5 determinism confirmed via `diff` of two
result.json runs).

**Honest evidence summary**:
- (i) sync transition **does occur** (r: 0.06 → 0.95 between K=1.5 and K=3.0,
  dr/dK peak idx=4 = K∈[2.0, 3.0] = consistent with mean-field K_c ≈ 1.6 once
  finite-N + 5-quantile coarsening 고려; L1+L3 carry).
- (ii) Φ(K*) / Φ(K=0) = 1.92 (incoherent baseline 대비 거의 2배; C2 PASS).
- (iii) **Φ peak at K=5.0 boundary** (NOT interior) — H207.1 single-peak
  FALSIFIED, H207.4 over-lock-loss FALSIFIED. Φ는 K 따라 step-monotone-up.
- (iv) phi_spatial 이 full-lock state 의 cell-간 MI 를 over-lock 의 integration
  loss 로 해석하지 않음 (L6 ex-ante 명시 carve-out 의 직접 observation).
  본 결과는 *Kuramoto sync transition 자체* 가 아니라 *phi_spatial measure
  choice* 의 axis-limit 신호 — H_007 success 와 H_207 failure 의 정직 대비.
- (v) dr/dK peak (sync transition center) 와 Φ peak (boundary) 의 분리는
  H207.3 FALSIFIED — sync 과 integration measure 가 axis-separated.

**State output**: `HEXAD/LIFE/state/h207_kuramoto_sync_2026_05_23/result.json`
**Smoke**: `HEXAD/LIFE/state/h207_kuramoto_sync_2026_05_23/run_h207.hexa`
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs
Rust FFI = named blocker — NOT 🔵, NOT LLM-judged, NOT PyPhi/sympy-primary).

**Follow-up cycles (raw#15 additive, not retraction)**:
- alternative encoding L4 sweep (sin θ / (cos, sin) 2D / wrapped phase) →
  phi_spatial measure-axis sensitivity test
- spatial-extension L5 (1D ring nearest-neighbor Kuramoto) → topology axis
- N sweep L1 (N ∈ {16, 32, 64, 128}) → finite-size scaling toward N→∞
  mean-field limit
- IIT 4.0 oracle compare (when phi_rs Rust FFI link landed, L8 closed) →
  over-lock-loss 가 measure-choice artefact 인지 (L6 closure)
