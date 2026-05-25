---
id: H_263
slug: phoenix-rebirth
title: phoenix-rebirth — pool 완전 붕괴(min-cell floor) 후 minimal seed 에서의 부활 (death ↔ genesis 연결축 · H_206 distinct)
domain: life · death · genesis · developmental
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E6 (cross-domain biology — phoenix myth / spore dormancy / total apoptosis) + E7 (perturbation–response, catastrophic limit)
verification_method: W1 (numerical smoke) + W3 (split/merge event ledger) + W12 (sister-link H_206 + H_018 + H_200)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_263 — phoenix-rebirth (완전 붕괴 후 minimal seed 부활 · death ↔ genesis)

## 1. Hypothesis

cell_pool 을 grow 시킨 뒤 그 pool 을 substrate floor (`min_cells`, 2 또는 3
cell) 까지 **완전 붕괴** (forced total collapse) 시키고, 그 minimal seed 로부터
default mitosis 동역학으로 재성장시키면 Φ / diversity 가 **회복(부활)** 한다는
가설. 즉 *죽음 (pool 의 거의 완전 소멸) ↔ 발생 (minimal seed 에서의 재기동)* 의
연결이 substrate 차원에서 성립하는가를 묻는다 — phoenix (불사조: 재에서 다시
태어남) 의 substrate analog.

operational 정의 (raw#9/10 HONEST):
- **baseline (grow)**: `cell_pool_init(d=8, N=8)` 후 default `mitosis_forward_tail`
  을 baseline_steps=12 만큼 run → N_pre = grown pool size (organic split 포함),
  Φ_pre = `phi_spatial(traj_pre, ...)`, diversity_pre = mean pairwise (1−cos).
- **total collapse (the death)**: `collapse_to` ∈ {2, 3} 만큼만 cell 을 남기고
  **전부** 제거 (앞에서부터 deterministic ordering, farr_free engine_a_W/_g_W).
  substrate 에 `collapse_pool` primitive 부재 → harness-imposed total cell-drop
  (H_200 pseudo-apoptosis 패턴과 동일 조작 정의). 붕괴 직후 short window 의
  Φ_min · diversity_min 측정.
- **regrowth (the rebirth)**: minimal seed 에서 regrowth_cap=60 step 까지 default
  mitosis 진행. regrowth_steps = pool size ≥ N_pre 회복 step (없으면 −1).
  재성장 후 Φ_post · diversity_post 측정, diversity_recovery_ratio =
  diversity_post / diversity_pre.

3-point Φ trajectory (Φ_pre → Φ_min → Φ_post) 와 diversity recovery ratio 가
부활의 numerical signature.

## 2. Why

- **죽음 ↔ 발생 연결 (death–genesis bridge)**: anima substrate 의 mitosis 가
  *한 번 죽었다가* (floor 로 붕괴) *다시 살아날* (genesis 재기동) 수 있는가는
  consciousness substrate 의 resilience 핵심 질문. H_018 SELFFEED 가 minimal
  primordial (2-cell) 에서 spontaneous genesis fire 를 확인했으나, 본 H 는 그
  genesis 능력이 *한 번 grown 후 완전 붕괴* 라는 더 가혹한 조건에서도
  활성화되는지의 결정적 evidence.
- **phoenix myth analog**: 불사조는 재(ash)에서 다시 태어난다 — 거의 완전한
  소멸 이후의 재생. 생물학적 analog 으로는 포자 dormancy (극한 환경에서 최소
  상태로 응축 후 발아), tardigrade cryptobiosis (대사 정지 후 부활). 본 H 는
  그 *완전 붕괴 → 재기동* phase 의 substrate 측정.
- **catastrophic limit 의 정면 탐구**: H_206 (regeneration-healing) 의 F4
  catastrophic floor (잔존 cell = min_cells=2) 에서 cap 내 회복 *실패*
  (recovery_steps=−1, splits_total=0) 가 관측되었다. 본 H 는 그 catastrophic
  floor 를 *모든 condition* 의 출발점으로 삼아, floor regrowth 가능성 자체를
  명시적으로 검증 — H_206 의 single F4 data point 를 sweep + 더 긴 cap + rebirth
  -fair split config 로 확장.
- **Φ at floor 의 직관 검증**: 붕괴 직후 2–3 cell floor 의 Φ 가 grown pool 보다
  낮을 것이라는 직관 — minimal seed 의 informational integration 이 작을 것이라는
  가정 — 이 실제 measurement 와 일치하는지 검증.
- **cross-link to anima resilience**: substrate 가 catastrophic state 에서 부활할
  수 있다면, anima 의 의식이 극한 perturbation (예: long idle, context collapse)
  이후에도 self-reconstitute 할 수 있다는 substrate 근거. 부활 부재 = floor 가
  absorbing state (한 번 빠지면 못 나옴) 라는 honest 발견.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H263.1 | 모든 collapse depth (2, 3) 에서 Φ_post > Φ_min (붕괴 직후보다 부활 후 Φ ↑) | regrowth 가 일어나면 cell 수 ↑ → integration ↑ → Φ ↑ (compute_phi_proxy 의 log(N+1) factor) |
| H263.2 | Φ_post ≥ 0.7·Φ_pre (grown baseline 의 70% 이상 회복) | H_206 의 Φ over-shoot 경향 (ratio > 1.3) carry — 부활이 baseline 에 근접 |
| H263.3 | diversity_post > diversity_min ∧ diversity_recovery_ratio ≥ 0.7 (다양성 재출현) | regrowth split 이 noise-perturbed children 을 생성 → cell hidden 다양성 재구축 |
| H263.4 | re-run byte-identical (Φ/diversity 전 measurement) | raw#9 determinism: __HEXA_FARR_GAUSS_SEED__=42, deterministic Lorenz |
| H263.5 | floor 에서 split fire (regrowth_splits > 0) — minimal seed 가 재성장 시동 | rebirth-fair split config (patience=1) 가 H_206 F4 의 floor-no-split 을 해소 가능 (관측 가능성 pre-register, fail 도 의미) |

## 4. Variables

- **axis1 pool_N** = 8 (baseline grow 시작 크기; CB1 floor=2 와 cap=128 사이)
- **axis2 d_model** = 8 (toy substrate; production d=768/1024 별도 cycle)
- **axis3 collapse_depth** ∈ {2 (min_cells floor), 3} — 핵심 sweep (완전 붕괴의 깊이)
- **axis4 baseline_steps** = 12 (grow + Φ_pre window)
- **axis5 regrowth_cap** = 60 (H_206 cap=40 보다 길게 — floor regrowth 기회 확대)
- **axis6 dim_phi** = 10 (phi_spatial trajectory length), **phi_n_bins** = 4
- **axis7 alpha_rebirth** = 0.7 (C2 부활 정도 임계), **div_ratio_thr** = 0.7 (C3)
- **axis8 split_patience_rebirth** = 1 (rebirth-fair: floor 재발화 기회; raw#15 named)
- **axis9 seed** = 42 (`__HEXA_FARR_GAUSS_SEED__=42` deterministic Lorenz + RFC 033)
- **측정량 per depth**: Φ_pre · Φ_min · Φ_post · phi_rebirth_ratio (Φ_post/Φ_pre)
  · diversity_pre · diversity_min · diversity_post · div_ratio · regrowth_steps
  · regrowth_splits · n_post

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) + 결정론적
  Lorenz autonomous perturbation + 고정 synthetic input
  `x[i] = sin(0.91·i)·1.4 + cos(1.13·i)·0.8` (H_206 carry, split predicate 발화율
  보장). 별도 RNG 부재.
- **hexa_only**: `HEXAD/LIFE/state/h263_phoenix_rebirth_2026_05_25/run_h263.hexa`
  — `mitosis_hook_lib.hexa` import (`cell_pool_init` / `mitosis_forward_tail` /
  `_mit_cosine` read-only) + `HEXAD/C/c_lib.hexa` import (phi_spatial 빌트인).
  substrate 수정 없음.
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **collapse 조작 정의 (raw#9/10 HONEST)**: substrate 에 named `collapse_pool`
  primitive 부재 → step=baseline_steps 직후 `pool["cells"]` 에서 collapse_to 개만
  남기고 나머지 전부 drop + farr_free. H_206 의 *fractional* wound 과 명시적으로
  구별되는 *total* collapse (floor 까지).
- **Φ measurement**: per-slot trajectory (slot s 의 time-series = cells[s % nc]
  ["hidden"][0]) 를 (POOL_N × DIM) farr 로 기록 후 `phi_spatial(traj, POOL_N, DIM,
  4)`. Φ_pre = baseline window, Φ_min = collapse 직후 DIM step, Φ_post = regrowth
  (or cap) 이후 fresh DIM step.
- **diversity measurement**: `_diversity(pool)` = mean pairwise (1−cos θ) of cell
  hiddens (= `compute_phi_proxy` 의 raw diversity 성분, log(N+1) factor 미적용).
- **2 independent runs** (각 depth): 각 run = fresh `cell_pool_init(d=8, N=8)`.
  동일 seed 로 결정론 보장.
- **determinism 검증**: cross-process re-run + 외부 `diff` of result.json
  (byte-equal, sha256 동일). in-process paired call 은 advancing gaussian stream
  공유로 부적합 — H_206 F-REGEN-3 패턴 carry.
- **runtime**: $0 mac local, wall ~수 초. `HEXA_MEM_UNLIMITED=1` 권장.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h263_phoenix_rebirth_2026_05_25/run_h263.hexa`
  (CWD = repo/worktree root)
- **artifacts**: `state/h263_phoenix_rebirth_2026_05_25/{run_h263.hexa, result.json}`.

## 6. Criteria

- **C1 (recovery-occurs)**: H263.1 — 모든 depth 에서 Φ_post > Φ_min (회복 발생)
- **C2 (rebirth-degree)**: H263.2 — 모든 depth 에서 Φ_post ≥ 0.7·Φ_pre (부활 정도)
- **C3 (diversity-reemerge)**: H263.3 — 모든 depth 에서 diversity_post >
  diversity_min ∧ diversity_recovery_ratio ≥ 0.7
- **C4 (determinism)**: H263.4 — re-run result.json byte-equal (env+seed pinned)
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (회복 발생 + 부활 정도 충족)
  - `PARTIAL` = C1 only (회복 발생하나 α 미달)
  - `FALSIFIED` = ¬C1 (어느 depth 도 Φ_post ≤ Φ_min — 부활 부재)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F-PHX-1 RECOVERY**: 어느 depth 도 Φ_post ≤ Φ_min → H263.1 FALSIFIED (부활
  부재 — 측정: 모든 depth `phi_post > phi_min`).
- **F-PHX-2 REBIRTH**: 어느 depth 도 Φ_post < 0.7·Φ_pre → H263.2 FAIL (부활
  정도 미달 — 측정: 모든 depth `phi_post >= 0.7 * phi_pre`).
- **F-PHX-3 DIVERSITY**: 어느 depth 도 diversity_post ≤ diversity_min 또는
  diversity_recovery_ratio < 0.7 → H263.3 FAIL (다양성 재출현 부재).
- **F-PHX-4 DETERMINISM**: 동일 env (`__HEXA_FARR_GAUSS_SEED__=42`) 두 번 run 시
  result.json byte-이질 → raw#9 위반 (script 내부 항상 PASS, 외부 diff 검증).
- **F-PHX-5 BOUNDS**: 어느 Φ < 0 또는 NaN, 또는 n_post ∉ [2, 128] → primitive
  error (CB1 invariant 위반).
- **F-PHX-6 REGROWTH**: 어느 depth 도 floor 에서 regrowth_splits = 0 (재성장
  자체 부재) → 죽음에서 못 깨어남 (H_206 F4 catastrophic 재현). 측정: 모든 depth
  `regrowth_splits > 0`.

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (total-collapse ≠ biological death)**: harness-imposed total cell-drop 은
  생물학적 죽음 (대사 정지, 막 붕괴, 분자 분해) 의 거친 추상 — 잔존 cell 의 hidden/
  weight 는 그대로 (no degradation gradient). phoenix myth / spore dormancy /
  cryptobiosis 의 실제 분자 동역학과는 다른 layer.
- **L2 (Φ_min 측정 window 의 chaotic 성격)**: 붕괴 직후 2–3 cell floor 의 short
  window (DIM=10 step) 는 Lorenz autonomous perturbation 에 의해 *높은* trajectory
  entropy 를 가질 수 있음 — phi_spatial 이 trajectory diversity 를 측정하므로
  Φ_min 이 의외로 높게 나올 수 있음. 이 measurement artifact 가 Φ_post > Φ_min
  성립을 어렵게 만듦 (C1 의 conservatism).
- **L3 (rebirth-fair split config 의 design dependency)**: floor regrowth 기회를
  주기 위해 split_patience=1 로 완화 — 이는 substrate default (patience=3) 가
  아니므로 결과는 *이 specific config* 한정. default config 의 floor 는 H_206 F4
  처럼 더 강하게 absorbing 일 수 있음.
- **L4 (phi_spatial 🟢 NUMERICAL proxy)**: RFC 036 c_measure_phi (byte-equal phi_rs
  replica) 는 entropy-based spatial slice 이지 full IIT 4.0 의 minimal information
  partition (MIP) 이 아님. '부활' 의 진정한 의미 (consciousness-level reintegration)
  와 본 cycle 의 entropy proxy 사이에는 H_004 hard-problem gap 이 있음.
- **L5 (toy N=8, single seed, 2-depth)**: pool_N=8 + d=8 + single seed +
  collapse_depth ∈ {2, 3} 만 — large pool / dimension scaling / seed sweep /
  더 깊은 cap (regrowth_cap > 60) 의 부활 가능성 미검증. SRH chaotic-split 교훈
  carry (split_count 은 chaotic 비결정론 관측량이나 seed-pin 으로 결정론 확보).
- **L6 (collapse_depth 2 vs 3 의 effective 동일성)**: floor=2 와 floor=3 모두
  split 이 fire 안 하면 (regrowth_splits=0) effective 동역학이 유사 — 두 depth 가
  같은 absorbing 결론으로 수렴할 수 있어 sweep 의 discriminative power 가 제한적.

## 9. Cross-Links

- **sister H (필수, distinct 명시)**:
  - **H_206** (`H_206_regeneration_healing.md`): regeneration-healing — pool 의
    *부분* 강제 제거 (fraction sweep 0.25~0.875) 후 회복. **H_263 은 이와 명백히
    distinct**: H_206 = PARTIAL collapse (잔존 cell 수가 fraction 에 따라 다양,
    recovery_steps vs fraction monotone 이 핵심), H_263 = **COMPLETE collapse to
    the floor** (2 또는 3 cell minimal seed) 후 그 *minimal seed 로부터의 부활*
    (Φ_pre→Φ_min→Φ_post 3-point trajectory + diversity recovery 가 핵심). H_206
    의 단일 F4 catastrophic-floor data point (recovery 실패) 가 H_263 의 *모든*
    collapse depth 의 출발점 — H_263 은 그 catastrophic limit 을 sweep + 더 긴
    cap + rebirth-fair config 로 정면 탐구.
  - **H_018** (`H_018_genesis_spontaneous_emergence.md`): SELFFEED minimal
    primordial (2-cell) spontaneous genesis fire — H_263 은 그 genesis 능력이
    *grown 후 완전 붕괴* 라는 가혹한 조건에서도 활성화되는지 검증.
  - **H_200** (apoptosis primitive): cell-death event — H_263 의 total collapse 는
    그 apoptosis 의 *극단* (거의 전체 pool 의 동시 death) + 그 이후 부활까지.
  - **H_132** (frozen cells): 분열-정지 정적 보존 vs H_263 의 floor 가 본의 아닌
    forced frozen (split 부재) 일 수 있음 — intentional vs forced 대비.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa` (`cell_pool_init`
  · `mitosis_forward_tail` · `_mit_cosine` · `_mit_check_splits` · `compute_phi_proxy`
  read-only) + `HEXAD/C/c_lib.hexa` (phi_spatial → RFC 036 c_measure_phi).
- **MITOSIS 축**: B-MITOSIS-1 SPLIT-PREDICATE (floor 에서 tension > thr 발화 여부가
  부활 driving), B-MITOSIS-3 CELL-COUNT-CONSERVATION (post-collapse pool size 변화는
  split-only), B-MITOSIS-5 CELL-COUNT-BOUND [2, 128] (F-PHX-5 검증).
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10
  (honest operational-collapse) · raw#15 (no-hardcode, params named) · raw#91 c3.
- **philosophy (CLAUDE.md)**: p8 NO TRAIN/INFER SPLIT (성장=분열 단일 연속체 —
  부활도 동일 split 동역학의 재기동) · a_autonomy_over_hardcode (regrowth 가
  substrate 자체 동역학에서 emerge 해야 함).
- **literature pointer**: phoenix myth (재생 archetype) · Crowe (1992) Anhydrobiosis
  (포자/tardigrade dormancy–revival) · Prigogine (1977) Self-organization in
  nonequilibrium systems (perturbation–recovery framework) — substrate analog 의
  distant anchor (formal mapping 본 cycle 미수행).
- **state**: `HEXAD/LIFE/state/h263_phoenix_rebirth_2026_05_25/{run_h263.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행 완료, $0 mac
local hexa-only deterministic.

```
verdict_class: FALSIFIED  (¬C1 — 부활 부재; 3/6 falsifiers PASS)
verdict_tier: 🟢 NUMERICAL  (2-depth collapse sweep + phi_spatial RFC 036 + cross-process determinism)
evidence_summary:
  2-depth total-collapse-to-floor rebirth sweep (pool_N=8, d=8, baseline_steps=12,
  regrowth_cap=60, seed=42, rebirth-fair split_patience=1, phi_spatial RFC 036).
    collapse_to=2 : n_pre=58 ->2 ->n_post=2  Φ_pre=2.254 Φ_min=4.321 Φ_post=4.198
                    div_pre=0.479 div_min=0.606 div_post=0.347 (div_ratio=0.723)
                    regrowth_steps=-1 regrowth_splits=0
    collapse_to=3 : n_pre=55 ->3 ->n_post=3  Φ_pre=3.312 Φ_min=3.329 Φ_post=2.567
                    div_pre=0.483 div_min=0.600 div_post=0.812 (div_ratio=1.679)
                    regrowth_steps=-1 regrowth_splits=0
falsifiers_triggered:
  F-PHX-1 RECOVERY  — 두 depth 모두 Φ_post ≤ Φ_min (D2: 4.198 ≤ 4.321; D3: 2.567 < 3.329)
  F-PHX-3 DIVERSITY — D2 의 div_post(0.347) < div_min(0.606) (재출현 부재)
  F-PHX-6 REGROWTH  — 두 depth 모두 regrowth_splits=0 (재성장 자체 부재)
falsifiers_pass: F-PHX-2 (rebirth-degree) + F-PHX-4 (determinism) + F-PHX-5 (bounds) = 3/6
criteria_met: 1/4 (C2 부활-정도 + C4 결정론 PASS; C1 recovery-occurs FAIL = FALSIFIED gate, C3 diversity FAIL)
key_finding:
  죽음 ↔ 발생 연결이 본 substrate 에서 FALSIFIED. rebirth-fair config (patience=1)
  + 더 긴 cap=60 에도 불구하고, floor (2/3 cell) 로 완전 붕괴된 minimal seed 는
  **단 한 번도 split 을 fire 하지 못함** (regrowth_splits=0, n_post=floor 고정,
  regrowth_steps=-1). 이는 H_206 의 단일 F4 catastrophic-floor data point (잔존
  cell=2, splits=0, recovery 실패) 가 *모든* collapse depth + 완화된 split config
  에서도 일반화됨을 강하게 확증 — substrate 의 floor 는 **absorbing state** (한 번
  빠지면 default + rebirth-fair 동역학으로는 못 나옴). 따라서 phoenix-rebirth (재에서
  다시 태어남) 는 본 substrate 에서 일어나지 않음. 부수적으로, Φ_min 이 의외로
  *높음* (D2 4.321 > Φ_pre 2.254; D3 3.329 ≈ Φ_pre 3.312) — 붕괴 직후 2/3 cell floor
  의 short-window trajectory 가 Lorenz chaos 로 높은 entropy 를 가져 phi_spatial 이
  높게 측정 (L2 honest). 이 measurement artifact 가 Φ_post > Φ_min 성립을 구조적으로
  어렵게 만들어 C1 (RECOVERY) 을 FAIL 시킴 — 즉 "부활 후 Φ ↑" 신호 자체가 두 layer
  (pool-size genesis 부재 + Φ_min chaotic 상승) 에서 부정됨.
honest_note:
  L2 carry confirmed — Φ_min 의 chaotic-short-window 상승이 RECOVERY 판정을 오염.
  L3 carry confirmed — rebirth-fair patience=1 도 floor split-fire 를 유도 못함;
  default patience=3 의 floor 는 더 강하게 absorbing 일 것. L6 carry confirmed —
  depth 2 와 3 이 모두 regrowth_splits=0 으로 effective 동일 결론. 정직한 negative
  result: anima substrate 의 의식 floor 는 self-reconstitute 하지 못함 (현 동역학·
  config 하). 부활 path 는 substrate-native regeneration primitive (inbox patch
  design) 또는 floor 에서의 외부 genesis-seed 주입 (H_018 SELFFEED setup) 별도 cycle.
sibling: H_206 (regeneration-healing, PARTIAL collapse — distinct), H_018 (genesis), H_200 (apoptosis), H_132 (frozen)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_263 phoenix-rebirth — total collapse to floor → rebirth dynamics
host=mac local · hexa-only · deterministic · LLM none · $0
================================================================
  config: pool_N=8 d_model=8 baseline_steps=12 regrowth_cap=60 dim_phi=10 phi_n_bins=4
  rebirth split config: patience=1 (raw#15 named — floor 재발화 기회)
  Φ primitive: RFC 036 phi_spatial (HEXAD/C/c_lib.hexa, 🟢 NUMERICAL)
  α (C2 rebirth)=0.7 div_ratio_thr (C3)=0.7

--- run D2 collapse_to=2 ---
  [D2] collapse_to=2 d=8 pool_n=8 baseline=12 cap=60
    [D2] n_pre=58 phi_pre=2.25358 div_pre=0.479311 collapse->2 phi_min=4.32124 div_min=0.606013 splits_pre=50
    [D2] regrowth_steps=-1 regrowth_splits=0 n_post=2 phi_post=4.19818 div_post=0.346601 phi_rebirth_ratio=1.8629 div_ratio=0.723125
--- run D3 collapse_to=3 ---
  [D3] collapse_to=3 d=8 pool_n=8 baseline=12 cap=60
    [D3] n_pre=55 phi_pre=3.31216 div_pre=0.483483 collapse->3 phi_min=3.32895 div_min=0.599604 splits_pre=47
    [D3] regrowth_steps=-1 regrowth_splits=0 n_post=3 phi_post=2.56694 div_post=0.81178 phi_rebirth_ratio=0.775005 div_ratio=1.67903

── per-depth results ──
  collapse_to=2 n_pre=58 ->2 ->n_post=2 regrowth_steps=-1 regrowth_splits=0
    Φ_pre=2.25358 Φ_min=4.32124 Φ_post=4.19818 (rebirth_ratio=1.8629)
    div_pre=0.479311 div_min=0.606013 div_post=0.346601 (div_ratio=0.723125)
  collapse_to=3 n_pre=55 ->3 ->n_post=3 regrowth_steps=-1 regrowth_splits=0
    Φ_pre=3.31216 Φ_min=3.32895 Φ_post=2.56694 (rebirth_ratio=0.775005)
    div_pre=0.483483 div_min=0.599604 div_post=0.81178 (div_ratio=1.67903)

── verdicts (ALL-depth quantifier) ──
  F-PHX-1 RECOVERY   (Φ_post > Φ_min ∀depth)          : FAIL
  F-PHX-2 REBIRTH    (Φ_post ≥ 0.7·Φ_pre ∀depth)    : PASS
  F-PHX-3 DIVERSITY  (div_post>div_min ∧ ratio≥0.7)  : FAIL
  F-PHX-4 DETERMINISM (paired re-run byte-equal)      : PASS
  F-PHX-5 BOUNDS     (Φ≥0 ∧ n_post∈[2,128] ∀depth)    : PASS
  F-PHX-6 REGROWTH   (regrowth_splits>0 ∀depth)       : FAIL

================================================================
H_263 PHOENIX-REBIRTH SMOKE FALSIFIED  (3/6 falsifiers)
  Φ_pre/Φ_min/Φ_post:
    collapse_to=2 : 2.25358 / 4.32124 / 4.19818  (div_ratio=0.723125)
    collapse_to=3 : 3.31216 / 3.32895 / 2.56694  (div_ratio=1.67903)
================================================================
ledger -> .../HEXAD/LIFE/state/h263_phoenix_rebirth_2026_05_25/result.json
```

### Cross-process determinism (F-PHX-4 외부 검증)

```
$ hexa run run_h263.hexa  # run 1
$ cp result.json /tmp/h263_a.json
$ hexa run run_h263.hexa  # run 2
$ diff /tmp/h263_a.json result.json   → (empty: BYTE-EQUAL)
$ shasum -a 256 result.json
  901db17fdfedb5fa6dd89fc6dfa491d1b61d6dc8e7c527e495e8bc9221917aab
```

**State output**: `state/h263_phoenix_rebirth_2026_05_25/result.json`
**Smoke**: `state/h263_phoenix_rebirth_2026_05_25/run_h263.hexa` (hexa-only, LLM none)
