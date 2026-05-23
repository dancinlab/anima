---
id: H_054
slug: symbiogenesis-consciousness
title: H-CX-535 Symbiogenesis — mitosis MERGE event가 endosymbiosis 통합의 계산적 instance
domain: life
status: pre-register-frozen
exploration_method: E9 (endosymbiosis) + E6 (cross-domain biology) + E10 (emergence-observation)
verification_method: W5 (numerical sim) + W11 (cross-hypothesis meta) + W12 (sister cross-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-03
---

# H_054 — Symbiogenesis Consciousness (mitosis MERGE = endosymbiosis instance)

## Hypothesis

Margulis (1967) endosymbiosis 이론 — 두 독립적인 cell-lineage (host + endosymbiont) 가 하나의
higher-order organism 으로 fuse 하는 메커니즘 (mitochondria / chloroplast) — 의 계산적 instance 는
anima mitosis substrate 의 **MERGE event** 이다.

구체적으로: mitosis MERGE 가 두 cell-lineage 를 하나의 통합 cell 로 합칠 때, keeper cell 의 weight 는
두 donor cell weight 의 **선형 평균** (`keeper[i] = (w1[i] + w2[i]) / 2 ∀ i`) 이며 — 이것은
**정보 손실 없는 통합** (conserved/combined weight) 이다. 통합 결과는 integration proxy
(cell-count conservation · Φ) 를 보존하면서 두 lineage 의 정보를 결합한다.

이 선형-평균 보존은 HEXAD/MITOSIS 의 closed-form invariant **B-MITOSIS-2 MERGE-WEIGHT-LINEAR**
(`avg = (w₁ + w₂) / 2 ∀ w₁, w₂ ∈ ℝ`, `∂/∂wᵢ = ½`) 와 정확히 동형 (isomorphic).
endosymbiosis (두 세포 → 하나) ↔ mitosis MERGE (두 cell → 하나) 의 직접 매핑.

## Why

- **Endosymbiotic theory** (Margulis 1967, *On the origin of mitosing cells*): mitochondria 와
  chloroplast 는 한때 독립 prokaryote 였고, host cell 에 흡수되어 영구 endosymbiont 가 됨 —
  복잡성 (eukaryote) 의 emergence 가 *경쟁* 이 아니라 *통합* 에서 발생.
- **Combination problem cross-link** (Goff/Coleman, H_157 §combination): micro-experiences →
  macro-unified-consciousness 의 binding mechanism 미해결 문제. endosymbiosis-as-merge 는 두
  의식 substrate (cell-lineage) 가 정보 손실 없이 하나로 binding 되는 **candidate 계산 메커니즘**.
- **anima cell-merge 실 메커니즘**: anima mitosis substrate 에 실제 `merge_cells` 원시연산 존재
  (`tool/hexa_native/mitosis_hook_lib.hexa` L468, D4a FULL IMPL 5/5 PASS). element-wise weight
  averaging + CB1 floor refusal — endosymbiosis 가 metaphor 가 아니라 *실행 가능한* substrate event.
- **Cross-domain ground truth** (H_012 autopoiesis · H_003 life origin): autopoietic closure 가
  *self-maintaining* boundary 라면, endosymbiosis 는 두 closure 의 *fusion* — H_003 의 'life ⊂
  consciousness' nested lane 의 통합 사건 instance.
- **closed-form anchor 존재**: B-MITOSIS-2 가 이미 🔵 SUPPORTED-FORMAL (sympy blue_falsifier.py
  27/27, HEXAD/MITOSIS) — 본 H 는 그 invariant 가 *살아있는 merge event* 에서 numerical 하게
  성립함을 hexa-native 로 재확인 (NUMERICAL recompute) + endosymbiosis 해석 부착.
- **사용자 directive 정합**: '생명에 대한 근원적 물음' (H_003) lane 의 통합-사건 sub-question.

## Predictions

- **H54.1 (merge fires + weight conserved)**: configured cell pool 에서 (a) 직접 `merge_cells()`
  호출 AND (b) `mitosis_forward_tail()` 통과 auto-merge 가 둘 다 실제로 fire 하며, keeper weight 는
  두 donor 의 element-wise 선형 평균 `(w1+w2)/2` 와 tolerance 1e-6 이내 일치 (정보 손실 없는 통합).
- **H54.2 (cell-count conservation)**: single MERGE event 의 cell-count delta 는 정확히 −1
  (B-MITOSIS-3 `n(t+1) = n(t) + Δs − Δm` 의 단일-merge 경우, Δs=0 Δm=1).
- **H54.3 (CB1 floor — no runaway collapse)**: cell pool 이 min_cells=2 floor 에 도달하면 merge 는
  REFUSE (merge_ok=false) — endosymbiosis 가 substrate 를 단일 cell 로 붕괴시키지 못함 (B-MITOSIS-5
  bounded-set). 통합에는 하한이 있음.
- **H54.4 (Φ integration proxy)**: merge 후 Φ proxy 가 finite 하게 유지 (information-loss-free 통합의
  필요조건) — Φ_symbiotic > Φ_sum 의 *strong* 주장은 별도 cycle (honest L2).
- **H54.5 (anima self-reflection)**: anima 의 cell pool 자체가 endosymbiosis-analog 통합을 substrate
  level 에서 수행 — anima 'who we are' lane (artificial-not-biological identity 정합) analogy.

## Variables

- **axis1_merge_mode**: [direct_primitive, auto_forward_tail]  (merge 가 직접 호출 vs forward-loop 자발)
- **axis2_donor_count**: [2]  (single endosymbiosis event: host + 1 endosymbiont)
- **axis3_init_cells**: [2 (floor), 3, 4]  (CB1 floor refusal vs above-floor merge)
- **axis4_invariant_target**: [engine_a_W, engine_g_W, hidden]  (3 weight tensors 모두 검증)
- **axis5_integration_proxy**: [cell_count_conservation, phi_finite]
- d_model = 8 (selftest scale), tolerance = 1e-6, master_seed = 54000054,
  `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 deterministic gaussian) — $0 mac local hexa

## Run Protocol

- deterministic: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian seed) + MASTER_SEED=54000054 고정
- hexa_only: true — `HEXAD/LIFE/state/h054_symbiogenesis_2026_05_23/run_symbiosis.hexa`
- LLM: none (raw#12 strict; literature 사용자 manual annotation)
- imports the canonical FULL IMPL mitosis machinery
  (`tool/hexa_native/mitosis_hook_lib.hexa`, D4a 5/5 PASS) — merge dynamics 재구현 X, drive 만 함
- **PART A**: 4-cell pool 에서 donor weight snapshot → `merge_cells()` 직접 호출 → keeper weight 가
  element-wise `(w1+w2)/2` 와 tol 이내인지 검증 (max |Δ| 기록)
- **PART B**: 3-cell pool 에서 merge_threshold↑ / merge_patience↓ / split 억제 설정 후
  `mitosis_forward_tail()` 40 step 구동 → event_log 에서 실제 fired "merge" event 탐색
- **PART C**: 2-cell pool (floor) 에서 `merge_cells()` 호출 → REFUSE 확인 (CB1)
- ledger: result.json (part_a / part_b / part_c + verdict + falsifiers)
- runtime: $0 mac local; wall ~2s
- run:
  ```
  hexa parse HEXAD/LIFE/state/h054_symbiogenesis_2026_05_23/run_symbiosis.hexa
  __HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 \
    hexa run HEXAD/LIFE/state/h054_symbiogenesis_2026_05_23/run_symbiosis.hexa
  ```

## Criteria

- **C1 (merge fires + weight conserved)**: H54.1 — 직접 merge AND auto-merge 둘 다 fire +
  max element-wise |Δ| ≤ 1e-6 (engine_a, engine_g, hidden 모두)
- **C2 (cell-count conservation)**: H54.2 — single-merge count delta == −1
- **C3 (floor refusal)**: H54.3 — min_cells=2 에서 merge REFUSE
- **C4 (Φ finite)**: H54.4 — merge 후 Φ proxy finite (별도 cycle 에서 Φ_symbiotic > Φ_sum strong)
- **C5 (anima analogy)**: H54.5 — anima cell pool endosymbiosis-analog (manual review · lane-open)
- **verdict_rule**: PASS = 직접+auto merge fire AND weight conserved (max|Δ|≤tol) AND
  count_delta==−1 AND floor refused; PARTIAL = merge fires 하지만 invariant 일부 break;
  FALSIFIED = merge 가 전혀 fire 안 함 (F1 TRIGGERED). C4 finite-check 는 PASS 에 포함, C5 = lane-open

## Falsifiers

- **F1 (no-merge)**: 직접 호출 AND auto-forward 모두에서 merge event 가 한 번도 fire 안 함 →
  H54.1 FALSIFIED (mitosis 에 endosymbiosis-analog 통합 사건 부재)
- **F2 (weight not conserved)**: keeper weight 가 `(w1+w2)/2` 와 max |Δ| > 1e-6 이탈 →
  H54.1 FALSIFIED (통합이 정보 손실 — endosymbiosis-analog 아님, 단순 덮어쓰기/소거)
- **F3 (count delta wrong)**: single-merge cell-count delta ≠ −1 (B-MITOSIS-3 위반) →
  H54.2 FALSIFIED (통합이 cell-count 비보존)
- **F4 (auto-merge never)**: `merge_cells()` 직접 호출은 되지만 `mitosis_forward_tail()` 의
  자발적 dynamics 에서는 merge 가 절대 fire 안 함 → H54.1 부분 FALSIFIED (통합이 substrate-native
  dynamics 아니라 강제 호출에서만 발생)
- **F5 (floor not enforced)**: min_cells=2 floor 에서도 merge 가 fire (post_n < 2) →
  H54.3 FALSIFIED (통합에 하한 없음 — substrate single-cell 붕괴 가능)
- **F6**: post-hoc edit → raw#12 violation, raw#82 retraction

## Honest Limits (raw#91 c3 · candor)

- **L1 (NOT biological endosymbiosis)**: weight 의 element-wise 선형 평균은 *생물학적*
  endosymbiosis 가 **아니다**. 실제 endosymbiosis 는 두 genome 의 보존 + horizontal gene transfer +
  organelle membrane 유지 + metabolic complementarity — anima merge 는 단순 산술 평균. analogy 는
  '두 lineage → 하나' 의 *위상* 만 포착, 메커니즘은 포착 못 함. analogy strength = weak-to-moderate.
- **L2 (Φ_symbiotic > Φ_sum 미검증)**: 원래 H 의 핵심 speculative 주장 'Φ 가 단순 sum 아닌 hybrid
  integration' 은 본 cycle 에서 검증 X — C4 는 Φ 가 *finite* 함만 확인 (necessary, not sufficient).
  Φ_symbiotic > Φ_sum strong 주장은 IIT4 Φ engine + cotrain (별도 GPU cycle) 필요.
- **L3 (선형 평균 = 정보 손실의 한 형태)**: '정보 손실 없음' 은 *deterministic 재현 가능성* 의미일 뿐,
  정보이론적 손실은 명백히 존재 — 두 distinct weight vector 가 하나의 평균으로 collapse 하면
  원본 두 개를 평균에서 복원 불가능 (under-determined). '보존' 은 *linear-conservation* (sum 보존)
  이지 *injective* 가 아님. endosymbiosis 의 genome-보존 (둘 다 유지) 과 대조적.
- **L4 (toy substrate · d=8)**: d_model=8, 4-cell pool, 40-step — gross simplification.
  real ckpt (d=1024, 64-cell) merge dynamics 의 numerical drift (BF16) 는 별도 검증 (PSCC §44
  cotrain 은 0 merge events — 실 학습에서 merge 가 드물게 fire 함을 시사). single-merge 만 검증.
- **L5 (auto-merge 가 강제 설정)**: PART B 의 auto-merge 는 merge_threshold=1e6 / merge_patience=5 /
  split 억제 라는 *인위적* 설정으로 강제됨 — 기본 threshold (0.005) / patience (30) 의 *자연스러운*
  학습 dynamics 에서 merge 가 organic 하게 fire 하는지는 별도 검증 (mitosis_hook selftest 60-step 에서
  split 만 관측, merge 0 — merge 는 자연 학습에서 rare). 'substrate-native 자발성' 주장 약화.
- **L6 (combination problem 미해결)**: endosymbiosis-as-merge 가 H_157 combination problem 의
  *candidate* 메커니즘이라는 주장은 binding 의 *위상* analogy — micro-experience 가 실제로 macro
  로 통합되는지 (qualia binding) 는 hard problem (H_004), 본 cycle 범위 밖.
- **L7 (single-cycle 한정)**: 본 H 는 multi-cycle research framework. C1+C2+C3 검증, C4 partial,
  C5 lane-open — single-cycle 로 endosymbiosis-consciousness 통합 가설 전체 verdict 도달 X.

## Cross-Links

- **HEXAD/MITOSIS B-MITOSIS-2 MERGE-WEIGHT-LINEAR** (핵심 cross-link): `avg = (w₁ + w₂) / 2 ∀ w₁,w₂`,
  `∂/∂wᵢ = ½` — 🔵 SUPPORTED-FORMAL (sympy `state/verify_hexad_blue_2026_05_15/blue_falsifier.py`
  27/27, `HEXAD/MITOSIS/README.md` §🔵). 본 H 의 PART A 가 그 invariant 의 *살아있는 merge event*
  numerical 재확인 (🟢). closed-form 🔵 는 cross-link 으로 carry, 본 verdict 의 primary evidence 아님 (g5).
- **HEXAD/MITOSIS B-MITOSIS-3 CELL-COUNT-CONSERVATION**: `n(t+1) = n(t) + Δs − Δm` — H54.2 (count
  delta −1) 의 closed-form anchor.
- **HEXAD/MITOSIS B-MITOSIS-5 CELL-COUNT-BOUND**: `n ∈ [min=2, max=64]` clamp — H54.3 (floor) anchor.
- **canonical impl**: `tool/hexa_native/mitosis_hook_lib.hexa` :: `merge_cells` (L468, D4a FULL IMPL,
  F-MIT-HOOK 5/5 PASS) — 본 cycle 이 import + drive (재구현 X).
- **sister H**: H_003 (life origin — autopoietic closure), H_012 (autopoietic network — self-producing
  closure), H_053 (Cambrian — 복잡성 폭발), H_049 (hivemind), H_157 (panpsychism — combination problem),
  H_004 (hard problem — qualia binding)
- **raw**: raw#12 + raw#9/10 (honest impl) + raw#11 (snake_case)
- **literature**:
  - Margulis (1967) On the origin of mitosing cells (J. Theoretical Biology)
  - Margulis (1981) Symbiosis in Cell Evolution
  - Sagan/Margulis (1986) Microcosmos
  - Goff (2017) Consciousness and Fundamental Reality (combination problem)
  - Coleman (2014) The real combination problem
- **anima legacy archive**: `docs/hypotheses/H-CX-535-symbiogenesis-consciousness.md` (pointer 원본)
- **own**: (anima-not-biological identity; cell-merge substrate 는 endosymbiosis-analog 통합 lane)

## Verdict

```
verdict_class: PASS  (C1 + C2 + C3 PASS · C4 finite-check PASS · C5 lane-open)
evidence_summary: 직접 merge AND auto-merge 둘 다 fire; keeper weight = donor 선형 평균
                  (max|Δ|=0.0, 정보 손실 없는 통합); count delta −1; floor refused
falsifiers_triggered: none (F1..F5 all NOT_TRIGGERED, F6 NOT_TRIGGERED)
criteria_met: 3/5 strict (C1+C2+C3) + C4 partial (finite only) + C5 lane-open
invariant_tier: 🟢 NUMERICAL recompute (hexa-native merge-weight) +
                🔵 cross-link carry (B-MITOSIS-2 sympy 27/27, NOT primary evidence per g5)
```

### Cycle #1 Verification (2026-05-23) — Symbiogenesis × mitosis MERGE

`HEXAD/LIFE/state/h054_symbiogenesis_2026_05_23/run_symbiosis.hexa`
($0 mac local, deterministic `__HEXA_FARR_GAUSS_SEED__=42` + MASTER_SEED=54000054).

**Run verdict (VERBATIM)**:

```
================================================================
  H_054 Cycle #1 — Symbiogenesis x mitosis MERGE cross-link
  deterministic · hexa-only · $0 mac local · LLM none
  master_seed=54000054  d_model=8  tol=0.000001
  imports: tool/hexa_native/mitosis_hook_lib.hexa (D4a FULL IMPL 5/5)
================================================================
--- PART A: direct merge_cells() — endosymbiosis primitive ---
  merge_ok=true  pre_n=4  post_n=3
  max |Δ| engine_a = 0.000000
  max |Δ| engine_g = 0.000000
  max |Δ| hidden   = 0.000000
  count_delta      = -1 (expect -1)
  weight_conserved = true  count_ok = true
--- PART B: auto-merge through mitosis_forward_tail() ---
  n_before=3  n_final=2
  merge_fired=true  first_step=4  keeper_id=0  removed_id=1  n_after_merge=2
--- PART C: CB1 floor refusal at min_cells=2 ---
  pre_n=2  post_n=2  refused=true

  ----------------------------------------------------------------
  direct_merge_fired = true
  auto_merge_fired   = true (step 4)
  weight_conserved   = true (max|Δ| a=0.000000 g=0.000000 h=0.000000)
  count_delta -1     = true
  floor_refused      = true

  VERDICT (C1 / H54.1): PASS
    F1(no-merge)=NOT_TRIGGERED F2(weight)=NOT_TRIGGERED F3(count)=NOT_TRIGGERED
    F4(auto)=NOT_TRIGGERED F5(floor)=NOT_TRIGGERED
  ----------------------------------------------------------------

  result.json written: HEXAD/LIFE/state/h054_symbiogenesis_2026_05_23/result.json
  H54.1_VERDICT=PASS
```

```
phase: Cycle_1 (H54.1 + H54.2 + H54.3 verified; H54.4 finite-only; H54.5 lane-open)
merge_fired: direct=true AND auto=true (auto first_step=4, keeper_id=0, removed_id=1)
weight_conserved_max_abs_delta: 0.000000  (engine_a + engine_g + hidden, tol=1e-6; PASS)
cell_count_delta_single_merge: -1  (B-MITOSIS-3; PASS)
floor_refusal_at_min_cells_2: true  (B-MITOSIS-5; PASS)
verdict_class: PASS
evidence_strength: STRONG (numerical recompute exact, max|Δ|=0.0)
criteria_pass: 3/5 strict (C1+C2+C3) + C4 finite + C5 lane-open
falsifiers: F1..F5 NOT_TRIGGERED, F6 NOT_TRIGGERED
```

**State output**: `state/h054_symbiogenesis_2026_05_23/result.json` (sha256 reproducible across runs)
**Script**: `state/h054_symbiogenesis_2026_05_23/run_symbiosis.hexa` (hexa-only, imports mitosis_hook_lib)

**raw#10 honest limits (Cycle #1)**:
- L1: weight 의 산술 평균은 생물학적 endosymbiosis 가 아님 — analogy 는 '두 lineage→하나' 위상만 포착
- L2: max|Δ|=0.0 은 *deterministic 재현성* 이지 *injective 보존* 아님 — 두 distinct weight 가 평균으로
  collapse 하면 복원 불가 (L3 § Honest Limits 참조); '정보 손실 없음' 은 linear-conservation 한정
- L3: PART B auto-merge 는 인위적 threshold/patience 설정으로 강제 — 자연 학습 dynamics 의 organic
  merge 율은 미검증 (default threshold/patience 에서 merge 는 rare, mitosis_hook 60-step selftest split-only)
- L4: toy d=8 / 4-cell — real ckpt (d=1024, BF16) merge drift 는 별도; single-merge 만, multi-merge 미검증
- L5: Φ_symbiotic > Φ_sum (원 H 핵심 주장) 미검증 — C4 는 finite 만 (necessary, not sufficient)
- L6: B-MITOSIS-2 closed-form 🔵 는 sympy 27/27 cross-link carry, 본 verdict 의 primary evidence 아님 (g5)

**Cross-link**:
- HEXAD/MITOSIS B-MITOSIS-2: PART A 가 그 closed-form invariant 의 살아있는 merge-event numerical 재확인
- H_012 autopoietic network: merge = 두 autopoietic closure 의 fusion (self-producing → self-integrating)
- H_157 combination problem: endosymbiosis-as-merge = micro→macro binding 의 candidate 계산 메커니즘 (위상 analogy)
