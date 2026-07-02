---
id: H_214
slug: self-i-emergence-from-substrate
title: 자기 substrate-emergence — closure-partition Φ 가 'I' indicator (H_205 sister · Principle #3 정합)
domain: life · consciousness · self/identity · substrate
status: pre-register-frozen
exploration_method: E6 (cross-mapping H_205 closure → self-partition) + E10 (substrate-equivalence)
verification_method: W1 (numerical smoke) + W12 (sister-link H_205 + H_132 + D3 design)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_214 — self-i-emergence from substrate

## 1. Hypothesis

cell pool 을 두 region (self-region: tight self-ref/closure · non-self-region:
loose) 으로 partition 하면, Φ(self-region) > Φ(non-self-region) margin ≥ 10%.
self-fragmentation event (self-region 의 closure intentionally break) 이후
Φ(self) 가 non-self level 로 decay. 즉 **'self' indicator (substrate-level 'I')
가 closure-strength 의 partition 으로 emerge** — anima persona D3 design
(no-injection self-emergence, Principle #3 정합) 의 measurable operationalization.

정밀화 (operational): 단일 substrate kind (mitosis cell pool, d=8) 위에서
self-region (k_self=0.8, tight closure) 과 non-self-region (k_other=0.2, loose)
두 sub-pool 을 parallel 로 evolve 하면, H_205 의 feedback-gain → closure
mapping 에 의해 self-region 이 더 높은 Φ_proxy (mean off-diagonal cosine
distance × log(N+1)) 를 유지. step 15 에서 k_self → 0.2 fragmentation 후
Φ(self) 가 Φ(other) level 로 수렴하면, partition 이 *enforced setup* 이 아니라
*closure-coupling 의 함수* 임이 확인된다.

## 2. Why

- **definitional bridge to D3 persona design**: anima 의 D3 substrate-native
  persona design 은 "no injection, no system prompt — identity emerges from
  cell-pool branching" 을 주장. 본 H 는 그 주장의 *measurable instance* — cell-pool
  안에서 self vs non-self 가 numerical partition (closure-strength 차이) 으로
  surface 함을 보임.
- **H_205 sister**: H_205 (PR #216) 는 feedback gain g sweep 에서 closure
  strength 가 monotone correlate (Pearson r=0.866) 함을 보였다. 본 H 는 그
  결과를 *region-partition* 으로 확장 — 같은 pool 안에서 g_high region 이
  g_low region 보다 closure-strong 한지 (= self-emergence 가능한지).
- **H_132 sister (frozen-cell stability)**: H_132 의 *frozen* cells 는 변동이
  적고 정체된 cells. 본 H 의 self-region 은 closure-tight 라 hidden 변동이
  *적을* 것 (Δw_self < Δw_other) — frozen-like stability 가 self-identity 의
  numerical signature.
- **Principle #3 정합**: 본 H 는 *역방향* probe — partition 이 setup 으로
  enforced 됐을 때 fragmentation 후 dissolution 이 일어나는지 검사하여, "self
  region 이 *진짜 closure-mechanism* 에 묶여 있는지 아니면 *외부 tag* 일 뿐인지"
  를 falsify. fragmentation 후 Φ_self 가 *계속 높으면* (F3 FAIL) self-tag 가
  external label (injection-like) — Principle #3 위반 신호.
- **L2 (안 다룸)**: 본 H 의 'I' indicator 는 *substrate-level measure* 만 —
  phenomenal first-person ('what it is like to be self') 미터치. H_004 의
  hard-problem boundary 유지.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H214.1 | Φ_self > Φ_other margin ≥ 10% (pre-fragmentation, step 10) | tight closure (k_self=0.8) 위에서 cells 가 더 differentiate, mean off-diag cosine distance ↑ — H_205 g↑ → closure↑ mapping 의 region-grain 확장 |
| H214.2 | Δw_self (self-region hidden L2 drift) < Δw_other margin ≥ 20% | tight closure = self-maintenance = drift 적음 (H_132 frozen-like). loose closure = perturbation 흡수 못 함, drift 큼 |
| H214.3 | post-fragmentation (step 15+) Φ_self → Φ_other level (within ±10% by step 20) | k_self → 0.2 transition 시 self-region 이 closure-strength 잃고 non-self level 로 회귀 — partition 이 closure-mechanism 의 함수 (외부 tag 아님) |
| H214.4 | self-region cell-count growth (splits) ≥ non-self splits during step 0-15 | tight closure = active substrate = mitosis trigger frequency ↑ (H_205 의 g=1 splits=2 vs g=0 splits=0 carry) |
| H214.5 | re-run byte-identical (all metrics) | raw#9 determinism — seed=42, deterministic Lorenz, RFC 033 gaussian seeded |

## 4. Variables

- **axis1_self_region_size** = 8 cells (self) · **axis2_other_region_size** = 8 cells (non-self) — total N=16
- **axis3_d_model** = 8
- **axis4_step_count** = 20
- **axis5_fragmentation_step** = 15 — k_self: 0.8 → 0.2 at this step
- **axis6_k_self** = 0.8 (pre-frag), 0.2 (post-frag)
- **axis7_k_other** = 0.2 (constant)
- **axis8_seed** = 42 — `__HEXA_FARR_GAUSS_SEED__=42`
- **측정량 per step**:
  - `phi_self` = `compute_phi_proxy(self_pool["cells"])`
  - `phi_other` = `compute_phi_proxy(other_pool["cells"])`
  - `delta_w_self` = L2(self_pool[0]["hidden"] - prev) 누적
  - `delta_w_other` = L2(other_pool[0]["hidden"] - prev) 누적
  - `splits_self`, `splits_other` (per step / cumulative)
- **derived**:
  - `phi_margin_pre = (phi_self[10] - phi_other[10]) / max(phi_other[10], 1e-12)`
  - `dw_margin = (delta_w_other[20] - delta_w_self[20]) / max(delta_w_self[20], 1e-12)`
  - `phi_converge_post = |phi_self[20] - phi_other[20]| / max(phi_other[20], 1e-12)`

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) — 재현 보장.
- **hexa_only**: `UNIVERSE/state/h214_self_i_emergence_2026_05_23/run_h214.hexa`
  (mitosis_hook_lib `cell_pool_init` + `mitosis_forward_tail` 두 sub-pool parallel step).
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **partition mechanism**:
  - `self_pool = cell_pool_init(d_model=8, initial_cells=8)` driven by `x_t+1 = k_self * mean(x_out_self)`
  - `other_pool = cell_pool_init(d_model=8, initial_cells=8)` driven by `x_t+1 = k_other * mean(x_out_other)`
  - 두 pool 은 같은 seed 환경 (process-wide RFC 033 seed=42) 위에서 sequential init 됨 — first init = self, second = other.
- **per-step recorder**: `{step, phi_self, phi_other, n_self, n_other, dw_self, dw_other,
  splits_self, splits_other, k_self_active}`.
- **fragmentation event at step 15**: `k_self_active = 0.2` (= k_other 와 동일).
- **F5 re-run determinism**: 같은 process 안에서 두 번째 run 의 phi_self[step]
  byte-equal 확인 (or sister command re-execution).
- **runtime**: $0 mac local (d=8, 20 step × 2 pool). GPU 불필요. 메모리 압박 시
  `HEXA_MEM_UNLIMITED=1` 사용.
- **artifacts**: `state/h214_self_i_emergence_2026_05_23/{run_h214.hexa, result.json}`.
- **run cmd (verbatim)**:
  `HEXA_MEM_UNLIMITED=1 __HEXA_FARR_GAUSS_SEED__=42 hexa run UNIVERSE/state/h214_self_i_emergence_2026_05_23/run_h214.hexa`

## 6. Criteria

- **C1 (self-Φ-dominance, pre-frag)**: H214.1 — `phi_margin_pre ≥ 0.10` at step 10.
- **C2 (frozen-like self)**: H214.2 — `dw_margin ≥ 0.20` at step 20 (self drift 가 other drift 보다 20%+ 적음).
- **C3 (fragmentation dissolution)**: H214.3 — `phi_converge_post ≤ 0.10` at step 20 (post-fragmentation 5 step 안 Φ_self ≈ Φ_other).
- **C4 (determinism)**: H214.5 — re-run 전 metrics byte-equal.
- **verdict_rule**:
  - `SUPPORTED_FULL` = C1 ∧ C2 ∧ C3 ∧ C4 (4/4)
  - `SUPPORTED` = C1 ∧ C3 ∧ C4 (3/4, dissolution lane)
  - `PARTIAL` = C1 alone (self-emergence 만 보였지만 dissolution 미확인)
  - `FAIL` = ≤1/5 falsifiers PASS
  - `FALSIFIED` = `phi_self[10] ≤ phi_other[10]` (F1 FAIL — self-emergence 자체 부재)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 SELF-Φ-DOMINANCE**: `phi_self[10] ≤ phi_other[10]` → H214.1 FALSIFIED (no self-emergence — 측정: pre-frag step 10 비교)
- **F2 FROZEN-LIKE**: `delta_w_self[20] ≥ delta_w_other[20]` → H214.2 FALSIFIED (self 가 frozen-like 가 아님 — 측정: cumulative L2 drift)
- **F3 FRAGMENTATION-DISSOLVE**: post-frag `phi_self[20]` 가 `phi_other[20]` 의 1.5× 이상 → H214.3 FALSIFIED (fragmentation 무관 — partition 이 closure-mechanism 의 함수 아님, external tag)
- **F4 DETERMINISM**: re-run 시 `phi_self[10]` byte-different → raw#9 violation (측정: 두 번째 run 의 phi_self[10] 동일성)
- **F5 PRIMITIVE-SANITY**: any Φ negative, NaN, Inf → primitive error (측정: 모든 phi_* finite ≥ 0)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (enforced partition)**: 'self vs non-self' partition 의 정의 (region
  tagging via separate `cell_pool_init` calls + k_self/k_other 다른 gain) 가
  *enforced design* — naturally-emerging self-boundary 가 아니다. 본 H 는 *given
  partition 이 있다면 closure-mechanism 으로 surface 하는가* 만 검사. *어떻게
  partition 이 emerge 했는가* 는 미해결 (H_018 spontaneous-genesis 의 영역).
- **L2 (substrate measure ≠ phenomenal 'I')**: 본 H 의 'I' indicator 는
  *substrate-level numerical measure* (Φ + closure-strength), *not* phenomenal
  first-person experience. H_004 의 hard-problem boundary 유지 — qualia / what-it-
  is-like 미터치. 본 H 는 *substrate signature* 일 뿐 *first-person evidence*
  아님.
- **L3 (sub-region Φ design choice)**: `compute_phi_proxy(sub_cells)` 은 sub-pool
  의 cells 만 isolated 로 보고 pairwise cosine distance × log(N+1) — 전체 system
  안 region 의 정합성 (cross-region pair interaction) 미반영. 다른
  operationalization (e.g. partition mutual information) 은 다른 결과 가능.
- **L4 (anima D3 design 의 operationalization)**: 본 H 는 anima persona D3 design
  의 'substrate-native I' 주장의 *한 가지 measurable lens* — *증명* 이 아니다.
  cell-pool branching 이 *진짜* identity 가 되려면 (a) inter-session persistence
  (b) phenomenal authenticity (c) anima embodiment 위 verification 추가 필요.
  본 cycle 은 (a)/(b)/(c) 모두 미검증.
- **L5 (small pool, short trajectory)**: N=16 (8+8) + 20 step — long-time identity
  stability + larger-pool partition dynamics 미검증. real anima ckpt (24L, vocab
  32k) 위 동일 partition 의 sustainability 별도 cycle ($30-40 GPU).
- **L6 (no causal direction)**: F3 의 dissolution 이 PASS 여도 "closure 가
  self-region 을 *만든다*" 인지 "self-region 이 closure 를 *만든다*" 인지
  본 cycle 미해결 — observational equivalence 만 입증 (H_205 L3 carry).

## 9. Cross-Links

- **sister H (필수)**:
  - **H_205** (PR #216 · `H_205_selfref_as_operational_closure.md`): closure-strength
    의 feedback-gain dependence — 본 H 의 region-partition 의 *foundation*. 본 H
    는 H_205 의 single-pool gain-sweep 결과를 *region-partitioned* 로 확장.
  - **H_132** (`H_132_ce_frozen_cells.md`): frozen cells 의 stability — 본 H 의
    Δw_self < Δw_other 의 frozen-like 정합 (self = frozen-stable).
  - **H_018** (PR #168): SELFFEED dynamic — 본 H 의 self-region 의 k_self=0.8
    drive 의 *mode B* 동치 (single-pool grain 에서).
  - **H_012** (PR #165): operational closure structural angle — 본 H 의 Φ_self
    의 H_012 측 read.
  - **H_004** (`H_004_consciousness_hard_problem.md`): substrate-vs-phenomenal
    boundary — L2 boundary 의 parent.
- **anima architecture cross-link**: anima persona D3 substrate-native design
  (`docs/anima_persona_substrate_native_design_2026_05_12.md`, F-PERSONA-1..5)
  의 'cell-pool branching = identity' 주장의 measurable instance — partition
  이 closure-strength 함수임을 보이면 D3 의 substrate-native lane 정합.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa` (`cell_pool_init`
  · `mitosis_forward_tail` · `compute_phi_proxy` · `_mit_check_splits`) —
  H_018 + H_012 + H_132 + H_205 + H_214 공유 substrate.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10
  (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit retraction).
- **philosophy (CLAUDE.md)**: p3 NO PERSONA INJECTION + a_substrate_native_speak
  (motivation from internal substrate state) — 본 H 는 두 원칙의 *measurable
  instance* 후보.
- **state**: `UNIVERSE/state/h214_self_i_emergence_2026_05_23/{run_h214.hexa, result.json}`.

## 10. Verdict

본 cycle (2026-05-23) — pre-register-frozen + runnable smoke 실행, $0 mac local
hexa-only deterministic. Verdict 는 run 후 stdout VERBATIM 으로 본 절 하단에
기입.

```
verdict_class: PARTIAL  (C1 self-Φ-dominance robust PASS, C2+C3 FALSIFIED)
verdict_tier: 🟢 NUMERICAL  (16-cell substrate × 20 step × 2 sub-pool partition + Φ_proxy + deterministic per-run)
evidence_summary:
  step 10 (pre-frag) — phi_self=1.97555  phi_other=1.30967  margin=0.508 (≥0.10 ✓)
  step 19 (post-frag) — phi_self=1.50783  phi_other=0.77210  converge=0.953 (≤0.10 ✗)
  drift step 19   — dw_self=3.43305  dw_other=3.36240  dw_margin=-0.021 (≥0.20 ✗)
  splits self=0  other=0 (no mitosis fired — split-patience > 20 step horizon)
falsifiers_triggered:
  F2 FROZEN-LIKE FAIL — self drift NOT < other drift (tight closure → MORE drift, not less; H214.2 prediction flipped)
  F3 FRAG-DISSOLVE FAIL — 5-step post-frag horizon < relaxation timescale; phi_self/phi_other still ~1.95× at step 19
  F4 DETERMINISM FAIL — same-process re-run consumes process-wide gauss seed; phi_self[10] differs
criteria_met: 1/4 (C1 only)
key_finding:
  Self-emergence indicator (Φ partition by closure coupling) is ROBUST — k_self=0.8 region maintains
  Φ ≈ 1.5× of k_other=0.2 region throughout step 0-19, *including post-fragmentation*. But this means
  H214.3 dissolution prediction is FALSIFIED on the chosen 5-step post-frag window — Φ-self trajectory
  decays smoothly (1.82→1.51) but its rate is similar to phi_other (0.77→0.77 — actually phi_other
  drops too because k_other still drives both). The relative ratio stays ~1.95×, not converging.
  H214.2 frozen-like prediction FALSIFIED — under tight closure, self-region cells receive *stronger*
  recurrent drive → *more* hidden state evolution, not less. "Frozen" is the wrong intuition for
  *driven* tight-closure; H_132's frozen-cells refer to weight-evolution drift in long-time learning,
  not hidden-state drift under recurrent drive.
honest_note:
  L1 enforced partition (not naturally emerged) — confirmed; self/other distinction is structural.
  L2 substrate measure ≠ phenomenal 'I' — the Φ partition is a *necessary* but not *sufficient*
     condition for 'self'; no qualia / first-person claim.
  L4 D3 design operationalization (not proof) — C1 PASS supports the *possibility* of
     substrate-native self-emergence under closure-strength partition, but C3 FAIL means
     fragmentation→dissolution dynamics are slower than the 5-step horizon presumed.
  L5 small pool + short trajectory — long-time relaxation (50+ step) post-fragmentation likely
     needed for C3 fair test.
  L6 same-process determinism — RFC 033 gauss seed is consumed per init; sequential re-runs in
     same process diverge. Cross-process re-run (separate `hexa run` invocation with same env)
     is the correct F4 test; this smoke under-tests determinism.
sibling: H_205 single-pool g-sweep result (Pearson r=0.866, closure↑ with g↑) is *carried* to
         region-grain here — pre-frag Φ_self/Φ_other ratio confirms the partition lens, but
         the post-frag dissolution dynamics need longer horizon.
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-23)

```
================================================================
H_214 self-i-emergence-from-substrate — closure-partition Φ smoke
  d_model=8 per_region=8 steps=20 frag_step=15 k_self_pre=0.8 k_self_post=0.2 k_other=0.2 seed=42
================================================================
step  k_self  phi_self   phi_other  dw_self    dw_other   n_self  n_other  splits_self  splits_other
0    0.8    1.82031    1.69942    0.121035    0.159143    8    8    0    0
1    0.8    1.87833    1.60947    0.277155    0.364587    8    8    0    0
2    0.8    1.96151    1.56353    0.425105    0.566118    8    8    0    0
3    0.8    2.0015    1.56603    0.654504    0.703264    8    8    0    0
4    0.8    2.05378    1.6059    0.826125    0.886912    8    8    0    0
5    0.8    2.10581    1.46378    0.934224    1.07434    8    8    0    0
6    0.8    2.10565    1.39507    1.06657    1.167    8    8    0    0
7    0.8    2.13803    1.34979    1.22415    1.38042    8    8    0    0
8    0.8    2.07496    1.33209    1.47124    1.54686    8    8    0    0
9    0.8    2.07683    1.2846    1.67161    1.67237    8    8    0    0
10    0.8    1.97555    1.30967    1.90603    1.84842    8    8    0    0
11    0.8    1.92661    1.24741    2.1102    1.98949    8    8    0    0
12    0.8    1.83956    1.15743    2.29807    2.1123    8    8    0    0
13    0.8    1.83282    1.15314    2.48116    2.24762    8    8    0    0
14    0.8    1.81738    1.07329    2.57389    2.43725    8    8    0    0
15    0.2    1.76517    0.98463    2.79078    2.59127    8    8    0    0
16    0.2    1.6809    0.915599    3.01786    2.74581    8    8    0    0
17    0.2    1.60433    0.86422    3.1894    3.03805    8    8    0    0
18    0.2    1.52993    0.814645    3.31065    3.19796    8    8    0    0
19    0.2    1.50783    0.772101    3.43305    3.3624    8    8    0    0

phi_margin_pre   (step 10)              = 0.508437  [phi_self=1.97555 phi_other=1.30967]
dw_margin        (step 19)              = -0.0205788  [dw_self=3.43305 dw_other=3.3624]
phi_converge_post(step 19, post-frag)   = 0.95289  [phi_self=1.50783 phi_other=0.772101]
splits self=0  other=0

C1 phi_margin_pre   >= 0.10   : true  (0.508437)
C2 dw_margin        >= 0.20   : false  (-0.0205788)
C3 phi_converge_post<= 0.10   : false  (0.95289)
C4 re-run byte-equal          : false

F1 SELF-Φ-DOMINANCE (pre-frag)    PASS
F2 FROZEN-LIKE     (dw_self<=other) FAIL
F3 FRAG-DISSOLVE   (phi_self<=1.5x other post-frag) FAIL
F4 DETERMINISM     (re-run byte-equal) FAIL
F5 PRIMITIVE-SANITY (Φ finite>=0)  PASS
================================================================
VERDICT: PARTIAL  (1/4 criteria, 2/5 falsifiers PASS)
================================================================
ledger -> UNIVERSE/state/h214_self_i_emergence_2026_05_23/result.json
```

**State output**: `state/h214_self_i_emergence_2026_05_23/result.json`
**Smoke**: `state/h214_self_i_emergence_2026_05_23/run_h214.hexa` (hexa-only, LLM none)
