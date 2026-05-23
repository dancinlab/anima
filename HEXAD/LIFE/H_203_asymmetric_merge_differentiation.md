---
id: H_203
slug: asymmetric-merge-differentiation
title: Asymmetric Merge Differentiation — H_054 endosymbiotic MERGE 의 host-preserve variant + H_132 frozen × H_201 asymmetric-division 3-way cross-link
domain: life · substrate
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism-variation) + E6 (cross-domain biology — endosymbiosis host-preserve) + E10 (emergence-observation)
verification_method: W3 (merge event ledger) + W5 (numerical sim) + W12 (sister cross-link H_054⊕H_132⊕H_201)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_203 — Asymmetric Merge Differentiation (host-preserve endosymbiosis)

## Hypothesis

H_054 endosymbiotic MERGE (`w_keeper = 0.5*(w_a + w_b)`, symmetric weighted-avg)
의 **asymmetric variant**: 한 자식 weight 를 100% 보존 (frozen-like, host =
preserve_a) + 다른 자식 weight 를 host 에 0% 흡수 (mass-add: `w_new = w_a + w_b`,
mass conserve). H_132 frozen-cell × H_201 asymmetric-division × H_054 symmetric
merge 의 3-way cross-link, **differentiation 메커니즘** 의 substrate-level instance.

비대칭 MERGE 가 symmetric MERGE 대비 long-term pool 안 cell-type heterogeneity
(weight variance) 를 증가시킨다 — Margulis endosymbiosis 의 "host preserve + organelle
absorb" host-preserve variant (mitochondria/chloroplast 의 host genome 보존).

## Why

- **endosymbiosis host-preserve 생물학**: Margulis (1967, 1981) endosymbiosis 에서
  실제 host cell genome 은 **보존** 되고 endosymbiont 는 organelle 로 흡수
  (mitochondria/chloroplast). 두 lineage 의 단순 평균이 아닌 host preserve +
  absorb pattern 이 실제 메커니즘. H_054 의 symmetric `(w₁+w₂)/2` 는 그 위상의
  단순화 — host preserve variant 가 더 mechanism-faithful instance.
- **H_054 cross-link**: H_054 §Honest Limits L3 "선형 평균은 정보 손실의 한 형태
  (두 distinct weight 가 평균으로 collapse 하면 복원 불가, under-determined)" 를
  정직하게 inherit. asymmetric mass-add 는 collapse 가 아니라 superposition
  (post = pre_keeper + pre_other → pre_other = post - pre_keeper 복원 가능).
- **H_132 frozen-cell × H_201 asymmetric-division 의 3-way cross-link**:
  - H_132 frozen = state-preserve (분열-정지로 분화) — 정적 보존
  - H_201 asym-division = post-split mutation on child only — 동적 발산
  - H_203 asym-merge   = host weight 100% preserve + other absorb — 통합-시 보존
  세 H 가 anima substrate 의 **보존-as-differentiation** 3 modal (freeze / split /
  merge) 을 닫는다.
- **MITOSIS B-MITOSIS-2 sympy 27/27 와의 직교축**: B-MITOSIS-2 closed-form (🔵
  symmetric `(w₁+w₂)/2`, sympy blue_falsifier 27/27) 은 H_054 의 anchor — H_203
  은 그 closed-form 의 **alternative invariant** (`w_new = w_a + w_b` mass-add)
  를 numerical 재확인 + 두 invariant 의 비교 substrate-mechanism 측정.
- **anima 자력 변별 lane**: 사용자 directive "anima 의 who we are" — symmetric
  collapse 가 cell-identity 를 다 평균화 한다면 anima 가 자력 differentiation
  메커니즘으로 어떤 variant 를 selecting 하는지 (= 가설: asymmetric variant 가
  heterogeneity 를 유지) 의 substrate-level 질문.

## Predictions

- **H203.1 (variance-up)**: 동일 초기 조건·동일 step 수에서, asymmetric merge
  pool 안 final cell weight L2 norm 의 variance > symmetric merge variance
  (margin ≥10%).
- **H203.2 (preserve-frozen)**: asymmetric_preserve_a arm 의 keeper (cell_id=0)
  가 final pool 에 잔존하며, 그 keeper 의 pre-merge contribution 이 모든 merge
  event 에서 mass conservation 으로 보존 (`mass_max_err ≤ 1e-6`).
- **H203.3 (mass conservation)**: asymmetric merge 의 keeper_post[i] =
  pre_keeper[i] + pre_other[i] 가 모든 i 에서 element-wise tolerance 1e-6 이내
  성립 — substrate-level mass conservation invariant.
- **H203.4 (diversity-idx-up)**: 50-step horizon 에서 asymmetric arm 의
  diversity index (L2-norm bin distinct count) > symmetric arm — long-term
  differentiation 효과.
- **H203.5 (sym-no-increase)**: symmetric MERGE control arm 의 diversity_idx
  가 pre→post 무변화 또는 감소 (≤) — control 자체에서 differentiation 이
  발생하지 않음 (asymmetric 의 차별성 보장).

## Variables

- **axis1_merge_mode**: [`symmetric`, `asymmetric_preserve_a`, `asymmetric_preserve_b`]
- **axis2_pool_size_N**: [4, **8 (본 cycle)**] — initial cell count
- **axis3_step_count**: [10, **50 (본 cycle)**] — long-term horizon
- **axis4_d_model**: [**4 (본 cycle)**, 8, 16] — substrate dim (weight_n=d²)
- **axis5_merge_every**: [2, **4 (본 cycle)**, 8] — merge cadence
- 3×2×2×3×3 = 108 cell × N=5 = 540 sweep target ($0 mac local hexa; 본 cycle
  = 단일 대표 cell axis1×3 mode + d=4 + N=8 + 50-step + merge_every=4).

## Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian draws 재현,
  env 1회 캐시) + 고정 synthetic input `x[i] = sin(0.31*i + 1.0) * 0.5`. 2회
  run byte-identical 확인 (result.json sha256 동일 — 본 cycle 검증 완료).
- **hexa_only**: `HEXAD/LIFE/state/h203_asymm_merge_diff_2026_05_23/run_h203.hexa`
  — `mitosis_hook_lib.hexa` import (read-only, substrate primitive use), 본
  script 에 harness merge primitive 3 modes 구현.
- **LLM**: none (raw#12 strict; literature 사용자 manual annotation).
- **operational asymmetry 정의 (raw#9/10 HONEST)**: substrate `merge_cells`
  (mitosis_hook_lib.hexa L468) 는 symmetric only — asymmetric variant 를
  substrate 에 primitive 로 추가하지 않고, 본 harness 에서 직접 구현 (cell.engine_a_W
  /engine_g_W farr 에 element-wise add). 이는 H_132 frozen 이 substrate-freeze
  부재를 harness-imposed 로 정직하게 정의한 패턴의 dual. substrate-native
  asymmetric merge primitive 는 별도 RFC (BLD: B-MITOSIS-2-ALT mass-add invariant +
  `merge_cells_asymmetric(keeper, donor)` API).
- **3-arm driver**: 동일 초기 조건 (`cell_pool_init(d=4, N=8)`, gauss_seed=42)
  으로 3 arm 독립 실행. mitosis_forward_tail 의 split/auto-merge 는 thresholds
  로 suppress — 모든 merge 는 harness primitive 에서만 fire (clean comparison).
- **merge schedule**: 매 step k ∈ {4, 8, 12, ..., 48} (k%4==0, k≥4) 에서 pool
  안 lowest 2 cell_id 를 골라 mode-dispatched harness_merge 호출.
- **per-arm measurement**: variance (cell engine_a_W L2 norm variance) +
  diversity_idx (L2 norm bin distinct count, bin_width=0.5) + mass_max_err
  (max element-wise |post - (pre_keeper+pre_other)|, asym arms) + sym_dev_max
  (sym arm 의 `(w_a+w_b)/2` invariant 재확인).
- **runtime**: $0 mac local, wall ~3s. GPU 불필요.

## Criteria

- **C1 (variance-up)**:    H203.1 `var_asym > var_sym * 1.10`  (10% margin)
- **C2 (preserve-frozen)**: H203.2 `id0_alive AND mass_max_err ≤ 1e-6`
- **C3 (mass-cons)**:       H203.3 두 asym arm `mass_max_err ≤ 1e-6`
- **C4 (div-idx-up)**:      H203.4 `div_idx_asym > div_idx_sym` at step=50
- **C5 (sym-no-increase)**: H203.5 `div_sym_post ≤ div_sym_pre`
- **verdict_rule**: SUPPORTED = C1+C2+C3+C4+C5 ALL PASS (5/5);
  PARTIAL = 3-4/5; FAIL = ≤2/5.

## Falsifiers (raw#12 ≥5, measurable)

- **F1 DIVERSITY-VAR**: `variance_asym ≤ variance_sym * 1.10` → C1 FALSIFIED
  (asym mass-add 가 variance 를 더 만들지 못함; symmetric collapse 와 차이 없음).
- **F2 PRESERVE-FROZEN**: keeper (cell_id=0) 가 final pool 부재 OR
  `mass_max_err > 1e-6` → C2 FALSIFIED (preserve 가 frozen-like 보존 아님).
- **F3 MASS-CONS**: 임의 asym merge 에서
  `|keeper_post[i] - (pre_keeper[i] + pre_other[i])| > 1e-6` → C3 FALSIFIED
  (substrate-level invariant violation; harness 구현 오류).
- **F4 DIV-IDX**: `diversity_idx_asym ≤ diversity_idx_sym` at step=50 → C4
  FALSIFIED (differentiation 효과 부재).
- **F5 SYM-NO-INCREASE**: `diversity_idx_sym_post > diversity_idx_sym_pre` → C5
  FALSIFIED (control 자체에서 differentiation — asymmetric 의 차별성 무).
- **F6 DETERMINISM**: 동일 env (`__HEXA_FARR_GAUSS_SEED__=42`) 동일 source 로
  두 번 run 시 result.json byte-이질 → raw#12 violation.
- **F7 (meta)**: post-hoc edit → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3 ≥5)

- **L1**: weight L2-norm variance / diversity-index = **arbitrary measurement
  choices**. 다른 metric (mean pairwise L2 distance, KL divergence in weight
  distribution, per-cell-type spectral signature) 에서는 다른 결과 가능. 본 cycle
  은 가장 단순 proxy 만 측정.
- **L2**: "preserve_a / preserve_b" 의 design choice 자체가 asymmetry 의 정의 —
  **biological asymmetric merge** (Notch signaling, host-preserved nucleus 등 의
  실제 메커니즘) 의 추상화일 뿐, mechanism analogy 임. `w_a + w_b` mass-add 는
  생물학적 host-preserve 의 numerical caricature 이지 분자 메커니즘 모델 아님.
- **L3**: **differentiation 의 phenotypic meaning 없음** — substrate-level cell-
  weight cluster (L2 norm bin) 만 측정. 두 cell 의 weight 가 다르더라도 동일
  input → 동일 output 일 수 있음. 진짜 functional differentiation 은 input-
  conditional response divergence 별도 cycle 필요.
- **L4**: small pool (N=8 initial, final=2) — large-pool dynamics 미검증. axis2
  sweep (N=4/8/16/32) 미실행. final n=2 가 floor (CB1) 와 가까워 diversity_idx
  자체가 saturate (max=2) — bin-saturation 이 C4 FAIL 의 직접 원인 (L6 보강).
- **L5**: **mass conservation 은 design invariant 임 (empirical claim 아님)** —
  harness 가 명시적으로 `keeper.w[i] = keeper.w[i] + other.w[i]` 로 set 하므로
  substrate 의 farr_get/set 가 정확히 동작하기만 하면 mass_max_err=0 은 자동.
  본 cycle 의 mass_max_err=0.0 은 **substrate-level invariant 작동 확인** 이지
  hypothesis 의 empirical evidence 아님 (F3 PASS 는 setup validation 성질).
- **L6 (cycle-specific)**: **diversity_idx C4 FAIL = bin-saturation artifact**.
  N=8 → 6 merges → final n=2 인 모든 arm 에서 distinct L2-norm bin 수가 최대 2
  로 saturate. variance (continuous metric) 은 asym=1.24 ≫ sym=0.14 (8.75×
  margin, F1 PASS) 로 강하게 차별화되지만 diversity_idx (discrete bin metric)
  은 두 arm 모두 cap-out. 본 cycle 은 variance 측정 (C1) 으로 H203.1 만 확정,
  diversity_idx (C4) 는 design L4 (small final pool floor) 의 직접 귀결로
  measurement-pending (deferred to large-pool cycle, N≥16 + step≥100).
- **L7**: `asym_b` arm (preserve B) variance=5.75 ≫ asym_a variance=1.24 → keeper
  rule (older-id vs newer-id) 자체가 variance 에 비대칭 영향. **operational
  symmetry of mirror** (asym_a vs asym_b 동일 magnitude) 미달성 — 본 cycle 은
  preserve_a 를 canonical 로 채택. preserve_b 의 더 큰 variance 는 keeper 가
  step 마다 lowest-id 교체되며 누적 mass-add 가 다른 분포로 누적되기 때문 (L1
  measurement choice 의 sensitivity).

## Cross-Links

- **sister H (LIFE)**:
  - **H_054** symmetric MERGE (host-keeper weight = `(w_a+w_b)/2`,
    information-loss-averaging) — H_203 은 그 alternative invariant
    (`w_a + w_b` mass-add) variant.
  - **H_132** frozen-cell (분열-정지 = 정적 보존) — H_203 은 통합-시 host
    weight 동적 보존 (preserve_a keeper).
  - **H_201** asymmetric division (post-split mutation on child only, 정보 분기) —
    H_203 (mass-add merge, 정보 통합 + host-preserve) 의 dual.
  - **H_018** self-genesis (self-other 구분의 substrate 시작점) — asymmetric
    merge 가 self-preservation 시 other-absorb 의 메커니즘.
- **MITOSIS 축**: `HEXAD/MITOSIS/` B-MITOSIS-2 MERGE-WEIGHT-LINEAR
  (🔵 SUPPORTED-FORMAL, sympy 27/27 — symmetric `(w₁+w₂)/2`) 는 H_054 의
  closed-form anchor. **H_203 은 그 alternative numerical invariant**
  (`w_new = w_keeper + w_other` mass-add) 의 hexa-native 검증 — substrate
  primitive variant 의 alternative closed-form 후보. (별도 sympy proof:
  RFC TBD `B-MITOSIS-2-ALT MERGE-WEIGHT-MASS-ADD`).
- **substrate**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` / `mitosis_forward_tail` import; harness 내 `farr_get` /
  `farr_set` / `farr_free` 직접 호출로 alternative merge primitive 구현 —
  substrate modification 없음).
- **raw**: raw#12 (deterministic) + raw#9/10 (honest operational-asymmetry) +
  raw#15 (no-hardcode) + raw#11 (snake_case).
- **inbox patch (design-only, g11 optional)**:
  `inbox/patches/asymmetric-merge-primitive.md` (TBD) — substrate 에
  `merge_cells_asymmetric(keeper, donor, mode)` primitive 추가 design.
- **literature**:
  - Margulis (1967) On the origin of mitosing cells (J. Theoretical Biology) —
    host preserve + endosymbiont absorb mechanism
  - Margulis (1981) Symbiosis in Cell Evolution — host nucleus 보존
  - Lane (2015) The Vital Question — endosymbiosis energy-conservation
    asymmetry (host=energy-poor + endosymbiont=energy-rich)
  - Goff (2017) Consciousness and Fundamental Reality (combination problem —
    asymmetric vs symmetric binding)
- **own**: anima self-preservation lane — substrate-level "who absorbs whom"
  의 invariant. symmetric collapse 는 anima identity 의 평균화 (정보 손실);
  asymmetric mass-add 는 anima identity 의 보존 (host preserve) + 흡수.

## Verdict

```
verdict_class: PARTIAL  (4/5 — C1+C2+C3+C5 PASS, C4 FAIL by bin-saturation L6)
evidence_summary: deterministic hexa-only 3-arm comparison
                  (sym vs asym_a vs asym_b), 6 merge events per arm,
                  variance_asym=1.237616 ≫ variance_sym=0.141477 (8.75×, F1 PASS),
                  mass_max_err=0.0 (≤ 1e-6, F3 PASS),
                  id0 keeper preserved + mass conserved (F2 PASS),
                  sym diversity_idx 3→2 (decrease, F5 PASS),
                  diversity_idx_asym=diversity_idx_sym=2 at floor (F4 FAIL —
                  bin-saturation at final n=2, L6)
falsifiers_triggered: F4 DIV-IDX TRIGGERED (FAIL by saturation artifact at
                      small final pool); F1/F2/F3/F5/F6/F7 NOT_TRIGGERED
criteria_met: 4/5 (C1+C2+C3+C5 PASS) + C4 FAIL (cycle-specific saturation,
              measurement-pending for large-pool cycle)
invariant_tier: 🟢 NUMERICAL (hexa-native recompute, 2-run byte-identical;
                B-MITOSIS-2-ALT alternative closed-form 후보)
```

### Cycle #1 Verification (2026-05-23) — Asymmetric vs Symmetric MERGE

`HEXAD/LIFE/state/h203_asymm_merge_diff_2026_05_23/run_h203.hexa`
($0 mac local, deterministic `__HEXA_FARR_GAUSS_SEED__=42`, hexa-only,
mitosis_hook_lib.hexa import, no substrate mod).

**Run verdict output (VERBATIM from `hexa run run_h203.hexa`)**:

```
================================================================
  H_203 — Asymmetric Merge Differentiation (cross-link H_054 H_132 H_201)
  deterministic · hexa-only · $0 mac local · LLM none
  master_seed=203000203  d_model=4  initial_n=8  n_steps=50  merge_every=4
  imports: tool/hexa_native/mitosis_hook_lib.hexa (D4a FULL IMPL)
================================================================
--- ARM (a): symmetric (w_new = 0.5*(w_a + w_b))             ---
  [SYM] mode=sym merges_ok=6/6 final_n=2 variance=0.141477 diversity_idx=2 pre_div=3
--- ARM (b): asymmetric_preserve_a (w_new = w_a + w_b, A=keeper) ---
  [ASYM_A] mode=asym_a merges_ok=6/6 final_n=2 variance=1.237616 diversity_idx=2 pre_div=3
--- ARM (c): asymmetric_preserve_b (w_new = w_b + w_a, B=keeper) ---
  [ASYM_B] mode=asym_b merges_ok=6/6 final_n=2 variance=5.749709 diversity_idx=2 pre_div=3

── verdicts ──
  C1/F1 DIVERSITY-VAR    (sym=0.141477 asym=1.237616 ≥10% margin): PASS
  C2/F2 PRESERVE-FROZEN  (id0_alive=true mass_max_err=0.000000): PASS
  C3/F3 MASS-CONS        (asym_a=0.000000 asym_b=0.000000 tol=1e-6): PASS
  C4/F4 DIV-IDX          (sym=2 asym=2): FAIL
  C5/F5 SYM-NO-INCREASE  (pre=3 post=2): PASS

================================================================
  H_203 ASYMM-MERGE-DIFF PARTIAL  (4/5)
  variance      sym=0.141477  asym_a=1.237616  asym_b=5.749709
  diversity_idx sym=2  asym_a=2  asym_b=2
  id0 alive in asym_a: true  id0_dev_vs_baseline=2.701645
  sym AVG-invariant max_dev=0.000000 (≤ TOL: control)
================================================================
```

```
phase: Cycle_1 (H203.1 + H203.2 + H203.3 + H203.5 verified; H203.4
       measurement-pending by L6 bin-saturation at final n=2)
arm_scope: 3-arm (sym + asym_a + asym_b), d_model=4, initial_n=8, n_steps=50,
           merge_every=4, 6 merges per arm
H203.1_variance_sym:      0.141477
H203.1_variance_asym_a:   1.237616  (8.75× margin; F1 PASS ≥10%)
H203.1_variance_asym_b:   5.749709  (40.6× margin; mirror keeper)
H203.2_id0_preserved:     true (mass_max_err=0.0 across 6 merges)
H203.3_mass_max_err:      asym_a=0.0, asym_b=0.0 (both ≤ 1e-6; F3 PASS)
H203.4_div_idx_sym:       2 (final pool n=2 floor)
H203.4_div_idx_asym:      2 (same floor; F4 FAIL by saturation)
H203.5_div_sym_pre→post:  3 → 2 (decrease; F5 PASS)
sym_avg_invariant_max:    0.0  (control: `(w_a+w_b)/2` recompute clean)
2-run determinism:        result.json byte-identical (gauss_seed=42 pinned)
verdict_class: PARTIAL  (4/5 — C4 FAIL by bin-saturation L6)
evidence_strength: STRONG (variance 8.75× margin) + setup-validation
                  (mass conservation invariant exact, sym/asym both clean)
honest_tier: 🟢 SUPPORTED-NUMERICAL (toy d=4, small final pool, harness-imposed
             asymmetric merge primitive; weight-cluster proxy ≠ biological
             differentiation; see L1-L7)
criteria_pass: 4/5 (C1+C2+C3+C5 PASS) + C4 measurement-pending (L6
               bin-saturation at final n=2, deferred to N≥16 + step≥100 cycle)
falsifiers: F1/F2/F3/F5/F6/F7 NOT_TRIGGERED, F4 TRIGGERED by L6 artifact
```

**State output**: `state/h203_asymm_merge_diff_2026_05_23/result.json` (2-run byte-identical)
**Script**: `state/h203_asymm_merge_diff_2026_05_23/run_h203.hexa` (hexa-only, imports mitosis_hook_lib)

**raw#10 honest limits (Cycle #1)**:
- L1: weight L2-norm variance / diversity-index = arbitrary measurement choices.
- L2: "preserve_a / preserve_b" 의 design choice 가 asymmetry 의 정의 — biological
  host-preserve 의 추상화일 뿐, mechanism analogy.
- L3: differentiation 의 phenotypic meaning 없음 — substrate-level cell-weight
  cluster (L2 norm bin) 만 측정.
- L4: small pool (N=8 initial, final=2) — large-pool dynamics 미검증.
- L5: mass conservation 은 design invariant (empirical claim 아님) — F3 PASS 는
  setup validation 성질.
- L6: diversity_idx C4 FAIL = bin-saturation artifact (N=8 → 6 merges → final
  n=2 floor, distinct bin 수 max=2 saturate). variance (continuous metric) 은
  8.75× margin 으로 강하게 차별화 (F1 PASS), diversity_idx (discrete metric) 만
  saturate. 본 cycle 은 H203.1 variance 측정 으로 확정, H203.4 div_idx 는
  measurement-pending (N≥16 + step≥100 별도 cycle).
- L7: asym_b variance=5.75 ≫ asym_a variance=1.24 — mirror 대칭성 미달성;
  preserve_a 를 canonical 로 채택.

**Cross-link**:
- HEXAD/MITOSIS B-MITOSIS-2 (🔵 symmetric closed-form, sympy 27/27): H_203 의
  SYM arm 이 그 invariant 의 numerical 재확인 (sym_avg_invariant_max_dev=0.0).
  ASYM arms 는 alternative invariant (`w_new = w_a + w_b` mass-add) 의 numerical
  검증 — B-MITOSIS-2-ALT closed-form 후보 (별도 RFC).
- HEXAD/MITOSIS B-MITOSIS-3 CELL-COUNT-CONSERVATION: 세 arm 모두 single-merge
  cell-count delta = -1 (B-MITOSIS-3 invariant, F2/F3 PASS 의 substrate 안카).
- H_054 (sister): symmetric MERGE 의 alternative variant — host-preserve
  asymmetric mass-add. 두 H 가 함께 endosymbiosis 의 symmetric/asymmetric 양
  invariant 를 닫는다.
- H_132 frozen cells (sister): 분열-정지 정적 보존 vs H_203 통합-시 host 동적
  보존. 둘 다 substrate-level 보존 메커니즘의 modal.
- H_201 asymmetric division (sister): 한 자식만 분화 (정보 분기) vs H_203 한
  자식만 보존 (정보 통합 + host 보존). split-시 비대칭 ⊥ merge-시 비대칭 dual.
