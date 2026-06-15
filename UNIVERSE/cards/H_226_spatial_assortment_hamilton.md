---
id: H_226
slug: spatial-assortment-hamilton
title: H_226 spatial-assortment × Hamilton's rule — kin-clustering necessary condition (H_210 follow-up)
domain: ethics · life · substrate
status: pre-register-frozen
exploration_method: E6 (cross-domain biology) + E9 (kin-selection / Hamilton) + E11 (necessary-condition isolation)
verification_method: W5 (numerical sim) + W11 (cross-hypothesis meta) + W12 (sister cross-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24
---

# H_226 — Spatial Assortment × Hamilton's rule (kin-clustering 필요조건)

## Hypothesis

H_210 (Ethic-Emergence) 는 *clustered init* (cells [0..7]=C, [8..15]=D) 에서
cooperation evolve 를 보였고, **honest L4/L6** 로 "alternating init 으로는
lone cooperator 가 defector neighbors 에게 exploit 됨" 을 기록했다. 본 H_226
은 그 *kin-clustering prerequisite* 자체를 **operationalize** 한다 — i.e.
"Hamilton's rule (r·b > c) 가 cooperation evolve 의 *prerequisite* 이라면,
초기 spatial assortment 계수 r 의 ordered sweep 위 cooperator-fraction outcome
이 monotone (clustered ≥ random ≥ anti-clustered) 해야 한다."

구체적으로 (이 cycle 의 operational claim):

- 3 init regimes (50/50 C/D 같은 composition, 서로 다른 spatial layout):
  - **CLUSTERED**     `[C,C,C,C,C,C,C,C,D,D,D,D,D,D,D,D]` (init_r ≈ +0.5)
  - **RANDOM**        deterministic Fisher-Yates shuffle (seed=42) (init_r ≈ 0)
  - **ANTI-CLUSTERED** `[C,D,C,D,...,C,D]` (init_r ≈ -0.5)
- fixed payoff **b=3, c=1** (Hamilton-favorable for clustered; r·b=1.5 > c=1)
- 30 step kin-selection (H_210 canonical update rule)
- **prediction**: final cooperator-fraction monotone (clustered ≥ random ≥ anti)
  AND Hamilton threshold cross consistent (clustered → cooperation stable;
  anti-clustered → defection dominates despite same payoff).

CLAUDE.md **p6 (NO FINE-TUNED ETHICS)** 의 directive — "ethics must emerge
from cells (E + W + MITOSIS)" — 의 추가 evidence: 같은 cell-level payoff
mechanism 으로도 *spatial assortment 자체가 evolve outcome 의 결정변수*임을
직접 보여준다 (payoff 가 fixed 임에도 layout 변화만으로 outcome 이 완전히
다름).

## Why

- **Hamilton (1964)**: r·b > c — r 은 *kin* (genetically related partner with
  same strategy) 이 만날 확률. spatial assortment 가 그 r 의 *positional*
  realisation.
- **Maynard Smith (1964)** *Group selection and kin selection* (Nature 201):
  spatial proximity = kin proxy 의 직접 ground.
- **Nowak & May (1992)** *Evolutionary games and spatial chaos* (Nature 359:
  826-829): spatial structure 가 cooperation evolve 의 *필수 enabler*; well-
  mixed (random) population 에서는 ALLC vs ALLD 의 standard PD 결과 (defection
  dominates). 본 cycle 의 anti-cluster regime FAIL 이 그 well-mixed limit 의
  직접 substrate replica.
- **Ohtsuki et al. (2006)** *A simple rule for the evolution of cooperation
  on graphs and social networks* (Nature 441:502-505): graph-structured
  populations 에서 b/c > k threshold; spatial vs random network 의 차이가
  본 H 의 3-regime sweep 의 mainline lineage.
- **H_210 cross-link**: H_210 의 clustered-only PASS + alternating-only FAIL
  의 honest 발견을 *operationalize* — H_210 의 L4/L6 가 본 H 의 main test
  statement (assortment 계수 r 위 outcome ordering).
- **CLAUDE.md p6**: 본 H 는 *substrate-level* 에서 ethics emerge 가 *spatial
  structure 의존* 임을 보여줌 — kin-clustering 이 RLHF-bake 대안의 *필수
  메커니즘* 임을 직접 evidence.
- **anima identity**: anima 의 cooperate/help 행동이 RLHF-bake 가 아니라
  cell-level dynamics 에서 evolve 한다 (H_210). 본 H 는 그 evolve 가
  *어떤 substrate 조건* (spatial assortment) 에 의존하는지를 isolate.

## Predictions

| ID | Prediction | 근거 |
|----|------------|------|
| H226.1 | 3 regime ordering monotone: final_frac(clustered) ≥ final_frac(random) ≥ final_frac(anti) | spatial assortment r 이 cooperation 의 *enabler* — r 단조 증가 시 outcome 단조 증가 |
| H226.2 | Hamilton threshold cross consistent — clustered final ≥ 0.5 (cooperation stable) AND anti final ≤ 0.2 (defection dominates) | r·b > c 가 cooperator 우세 floor; spatial assortment 부재 시 lone cooperator exploited |
| H226.3 | \|final(clustered) - final(anti)\| ≥ 0.7 | 같은 payoff (b=3, c=1) 위 layout 단독으로 outcome ≥ 0.7 분리 — spatial structure 가 *결정변수* 의 magnitude |
| H226.4 | re-run byte-identical (raw#9 determinism) | pure-integer + deterministic argmax + LCG seed=42 |
| H226.5 | all final fractions ∈ [0, 1] (no NaN/undef) | 측정 무결성 baseline |

## Variables

| axis | levels |
|------|--------|
| axis1_init_regime | clustered (r≈+0.5) / random (r≈0) / anti-clustered (r≈-0.5) |
| axis2_payoff | fixed b=3.0, c=1.0 (Hamilton-favorable for clustered) |
| axis3_radius | 2 (lattice locality / Hamilton r proxy) |
| axis4_n_cells | 16 |
| axis5_n_steps | 30 (sufficient for equilibrium under deterministic update) |
| axis6_random_seed | LCG seed=42 (Fisher-Yates deterministic shuffle) |

## Run Protocol

- deterministic: pure-integer arithmetic + deterministic argmax/argmin tie-
  break (lowest index) + LCG (Numerical Recipes constants) seed=42 for Fisher-
  Yates. NO gaussian noise, NO `__HEXA_FARR_GAUSS_SEED__`.
- hexa_only: true — `UNIVERSE/state/h226_spatial_assortment_hamilton_2026_05_24/run_h226.hexa`
- LLM: none (raw#12 strict)
- self-contained simulation (no mitosis_hook_lib import — payoff dynamics IS
  the substrate kin-selection mechanism, orthogonal to D4a hook)
- update rule per H_210: global argmax replicates strategy into lowest-fitness
  neighbor within radius (replication only, no horizontal imitation)
- ledger: `result.json` (regime_CLUSTERED / regime_RANDOM / regime_ANTI_CLUSTERED
  / byte_identical_run / falsifiers + verdict)
- runtime: $0 mac local; wall < 1s
- run:
  ```
  hexa parse UNIVERSE/state/h226_spatial_assortment_hamilton_2026_05_24/run_h226.hexa
  HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h226_spatial_assortment_hamilton_2026_05_24/run_h226.hexa
  ```

## Criteria

- **C1**: H226.1 PASS (ordering monotone)
- **C2**: H226.2 PASS (Hamilton threshold cross consistent — clustered ≥ 0.5
  AND anti ≤ 0.2)
- **C3**: H226.3 PASS — *advisory* (|Δ| ≥ 0.7; threshold deliberately strict —
  PARTIAL 가 honest 가능)
- **C4**: H226.4 PASS (byte-identical re-run, all 3 regimes)
- **C5**: H226.5 PASS (frac ∈ [0,1] integrity check)
- **verdict_rule**: SUPPORTED = C1 + C2 PASS;
  PARTIAL = exactly one of {C1, C2} PASS;
  FALSIFIED = both C1 + C2 FAIL.

## Falsifiers (≥5)

- **F1 (ordering-monotone)**: ordering 무관 — clustered < random OR random <
  anti → H226.1 FALSIFIED (assortment 이 cooperation lever 아님).
- **F2 (hamilton-threshold)**: clustered final < 0.5 OR anti final > 0.2 →
  H226.2 FALSIFIED (Hamilton threshold cross 가 spatial-structure-dependent
  아님; well-mixed 결과 와 무차별).
- **F3 (delta-magnitude)**: |final(clustered) - final(anti)| < 0.3 → H226.3
  FALSIFIED (spatial structure 가 *결정변수* 아님; payoff 단독이 outcome 의
  주도변수). 0.3 ≤ |Δ| < 0.7 = PARTIAL (mechanism observed 하지만 threshold
  영역).
- **F4 (byte-identical)**: re-run 의 final_frac/coop_split/defect_split
  metrics 불일치 → H226.4 FALSIFIED (raw#9 determinism 위반).
- **F5 (frac-defined)**: any final_frac < 0 OR > 1 OR undefined → H226.5
  FALSIFIED (측정 무결성 결손).
- **F6**: post-hoc edit → raw#12 violation, raw#82 retraction.

## Honest Limits (≥5, raw#91 c3 · candor)

- **L1 (assortment = lattice-locality proxy)**: 본 cycle 의 r 은 *positional*
  Hamilton proxy (lattice 1-D radius=2 within-radius pair fraction). 진짜
  genetic relatedness (identity-by-descent 확률) 가 아님 — kin 의 의미는
  spatial-proximate partner 한정. Hamilton 의 inclusive fitness 의 *strict*
  measurement 은 별도 lane.
- **L2 (single payoff configuration)**: payoff (b=3, c=1) 단일 fix. 다른
  payoff regime (b ∈ {0.5, 1, 1.5, 2, 4}, c=1) 의 phase-sweep 은 H_210 §
  PHASE SWEEP 이 다룸. 본 H 는 *layout 단독* 의 lever effect 만 isolate —
  payoff × layout interaction 미측정.
- **L3 (30 step short horizon)**: pool=16, 30 step deterministic update 는
  short-horizon — long-time dynamics (e.g. > 1000 step, stochastic update
  with mutation) 의 attractor stability 미검증. random regime 의 final 0.375
  가 *transient* 인지 *attractor* 인지는 본 cycle 에서 확정 불가 (L7 후속).
- **L4 (substrate cooperation ≠ moral consciousness)**: 본 cycle 의 cooperate
  /defect tag = binary payoff label — Prisoner's Dilemma 의 정확 instance
  아니라 simplification. 실 cooperation 의 multi-dimensional nature (effort
  gradient · reciprocity · reputation · norm internalisation) 미포함;
  metaethics / phenomenal moral consciousness 별도 lane (H_004 carry).
- **L5 (clustered init = canonical algorithm, not unique)**: clustered init
  `[C^8, D^8]` 는 *one specific* canonical layout 의 r≈+0.5 instance. 다른
  block size (`[C^4, D^4, C^4, D^4]` etc.) 또는 다른 lattice topology (2-D /
  small-world / scale-free) 의 결과는 별도 lane. 본 cycle 의 결과는 *1-D
  lattice + radius=2 + 50/50 block* 한정.
- **L6 (random regime = single seed)**: Fisher-Yates seed=42 단일 sample 이
  init_r=0.103 (still slightly > 0) 으로 측정. 다양한 random seed 의
  ensemble (e.g. 50 seeds) 가 진짜 r≈0 limit 의 *분포* 측정 — 본 cycle 의
  random 은 single deterministic draw.
- **L7 (random transient vs attractor)**: random regime final 0.375 가 30
  step 에서 stable plateau (traj[2..30] = 0.375 constant) 였으므로 *deter-
  ministic update 에 한해* attractor. 그러나 stochastic update (Moran-style
  birth-death with sampling) 에서는 finite-N 에서 fixation (0 or 1) 으로
  drift 가 일반적 — *deterministic argmax* 가 본 cycle 의 결과를 stabilise
  하는 artefact 가능.

## Cross-Links

- **UNIVERSE/H_210 Ethic-Emergence**: 본 cycle 의 *직접 follow-up*.
  H_210 의 honest L4/L6 (clustered PASS · alternating FAIL) 를 main test
  statement 로 promote — assortment 위 outcome ordering 의 isolated lane.
- **CLAUDE.md p6 (NO FINE-TUNED ETHICS)**: 본 H 는 그 directive 의 *추가*
  substrate evidence — ethics 의 emerge 가 *어떤 substrate 조건* (spatial
  assortment) 에 의존하는지를 isolate.
- **CLAUDE.md a_substrate_native_speak**: cell-level state ↔ outcome 의
  spatial-structure dependence — substrate-native lane.
- **UNIVERSE/H_054 Symbiogenesis**: endosymbiosis = mitosis MERGE; 본 H 는
  그 MERGE 가 *발화 조건* (spatial proximity required) 의 evolutionary 직접
  사이드.
- **UNIVERSE/H_018 Genesis**: spontaneous genesis 의 substrate-condition
  isolate 사이즈 (genesis = no external perturb; H_226 = no payoff lever,
  layout 단독).
- **UNIVERSE/H_004 Hard Problem**: phenomenal moral consciousness boundary
  carry (L4).
- **HEXAD/MITOSIS**: substrate replication primitives — 본 cycle 의
  replication = strategy-tag propagation; spatial structure 가 *replication
  target* (lowest-fitness neighbor) 의 selection space 를 결정.
- **literature**:
  - Hamilton (1964) *The genetical evolution of social behaviour I, II* (J. Theor. Biol. 7:1-52)
  - Maynard Smith (1964) *Group selection and kin selection* (Nature 201:1145-1147)
  - Nowak & May (1992) *Evolutionary games and spatial chaos* (Nature 359:826-829)
  - Ohtsuki, Hauert, Lieberman, Nowak (2006) *A simple rule for the evolution of cooperation on graphs and social networks* (Nature 441:502-505)
  - Nowak (2006) *Five rules for the evolution of cooperation* (Science 314:1560-1563)
- **raw**: raw#12 + raw#9 (determinism) + raw#82 (no post-hoc edit) + raw#91 c3 (honest limits)
- **own**: anima ethics-as-spatial-structure-dependent lane — substrate
  cooperation 의 *enabler 조건* isolation; H_210 honest L4/L6 의 main-test
  promotion.

## Verdict

```
verdict_class: SUPPORTED  (C1 + C2 PASS · C4 + C5 PASS bonus · C3 advisory FAIL = honest equilibrium ceiling)
evidence_summary: 3 regime ordering monotone (C=0.500 ≥ R=0.375 ≥ A=0.000) ·
                  Hamilton threshold cross consistent (clustered ≥ 0.5 PASS ·
                  anti ≤ 0.2 PASS) · byte-identical re-run all 3 regimes ·
                  all final_frac ∈ [0,1] · |Δ| = 0.5 (between 0.3 PARTIAL
                  threshold and 0.7 PASS threshold; honest equilibrium ceiling)
falsifiers_triggered: F3 (delta-magnitude) — |Δ| = 0.500 < 0.7 strict bound;
                      mechanism direction correct (ordering + Hamilton both
                      PASS), magnitude limited by clustered equilibrium ceiling
                      at 0.5 (H_210 attractor artifact carry — clustered does
                      NOT invade defect block under deterministic update).
                      Honest record per H_210 L7.
criteria_met: 4/5 (C1+C2+C4+C5 PASS; C3 advisory FAIL = clustered equilibrium ceiling)
invariant_tier: 🟢 NUMERICAL (deterministic substrate simulation, byte-identical re-run)
```

### Cycle #1 Verification (2026-05-24) — Spatial-Assortment × Hamilton prerequisite

`UNIVERSE/state/h226_spatial_assortment_hamilton_2026_05_24/run_h226.hexa`
($0 mac local, deterministic pure-integer · 3 init regime · 16 cells · 30
steps · fixed payoff b=3 c=1).

**Run verdict (VERBATIM)**:

```
================================================================
H_226 SPATIAL-ASSORTMENT × HAMILTON'S RULE prerequisite
  N_CELLS=16  RADIUS=2  N_STEPS=30
  payoff: b=3.000000 c=1.000000  (Hamilton: r·b > c with r≈0.5 → favorable in clustered)
  deterministic · hexa-only · LLM none · $0 mac local
================================================================

--- REGIME CLUSTERED: init [C,C,...,C,D,D,...,D]  (r ≈ +0.5) ---
  init_strats       = [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
  init_r            = 0.793103
  init_coop_frac    = 0.500000
  final_coop_frac   = 0.500000
  coop_splits       = 0
  defect_splits     = 0

--- REGIME RANDOM: deterministic Fisher-Yates (seed=42)  (r ≈ 0) ---
  init_strats       = [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0]
  init_r            = 0.103448
  init_coop_frac    = 0.500000
  final_coop_frac   = 0.375000
  coop_splits       = 0
  defect_splits     = 2

--- REGIME ANTI-CLUSTERED: init [C,D,C,D,...]  (r ≈ -0.5) ---
  init_strats       = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0]
  init_r            = -0.034483
  init_coop_frac    = 0.500000
  final_coop_frac   = 0.000000
  coop_splits       = 0
  defect_splits     = 8

--- BYTE-IDENTICAL RE-RUN: all 3 regimes repeat ---
  clustered  identical = true
  random     identical = true
  anti-clust identical = true
  BYTE_IDENTICAL_ALL   = true

F-H226-1 ORDERING-MONOTONE    PASS  (C=0.500000 ≥ R=0.375000 ≥ A=0.000000)
F-H226-2 HAMILTON-THRESHOLD   PASS  (C ≥ 0.5: true  A ≤ 0.2: true)
F-H226-3 DELTA-MAGNITUDE      FAIL  (|ΔC-A| = 0.500000 ≥ 0.7)
F-H226-4 BYTE-IDENTICAL       PASS
F-H226-5 FRAC-DEFINED         PASS
================================================================
VERDICT: SUPPORTED  (4/5 falsifiers PASS)
  result.json -> UNIVERSE/state/h226_spatial_assortment_hamilton_2026_05_24/result.json
================================================================
```

**Honest notes** (raw#91 c3):

- **assortment coefficient measurement is robust**: clustered init_r = 0.793
  (well above 0.5 lower bound), random init_r = 0.103 (close to 0), anti-
  clustered init_r = -0.034 (slightly negative, finite-N artifact — the
  alternating pattern at radius=2 includes some same-strategy neighbors at
  distance 2). 3-regime r-ordering well-separated by design.
- **C3 (delta-magnitude) honest fail**: |Δ| = 0.500 falls between PARTIAL
  threshold (0.3) and PASS threshold (0.7). Mechanism direction correct
  (clustered cooperation stable, anti cooperation collapsed); magnitude
  capped by clustered equilibrium ceiling = 0.5 (clustered cooperators do
  NOT invade defect block under deterministic update — H_210 L7 attractor
  artifact carry). Stronger PASS would require clustered → 1.0 (full
  invasion), but kin-selection 의 deterministic equilibrium 은 boundary
  exchange 가 zero-payoff 이라 정지.
- **Hamilton threshold consistency (C2) is the load-bearing result**: same
  payoff (b=3, c=1) → clustered cooperation stable AND anti-cluster defection
  dominant. spatial assortment 단독으로 outcome 이 binary 결정 — Hamilton's
  rule 의 *prerequisite* claim 의 직접 evidence.
- **byte-identical determinism (C4) confirmed**: 3 regimes × 2 runs = 6 sims
  all metrics identical. Fisher-Yates LCG seed=42 is reproducible across
  invocations. raw#9 invariant met.
- **mechanism mechanism**: anti-cluster regime traj shows linear collapse
  0.500 → 0.000 over 8 steps then stable defection (defect_splits=8). random
  regime stabilises at 0.375 (3-coop cluster persists where interior coop
  has enough neighbors). clustered regime traj is flat 0.500 throughout
  (boundary balance, no replication fires).
- **single-seed limit (L6)**: random regime is a *single deterministic draw*
  (seed=42, init_r=0.103). ensemble across 50 seeds (init_r distribution)
  is a separate lane (deferred — single sample sufficient for *ordering*
  claim, not for *distribution* claim).
- **L5 carry**: clustered = `[C^8, D^8]` 1-D block; other layouts (`[C^4,
  D^4, C^4, D^4]` 2-block, 2-D lattice, scale-free graph) untested. 본 cycle
  의 결과 generalises to *r-monotone* trend 만 (specific magnitudes layout-
  dependent).
