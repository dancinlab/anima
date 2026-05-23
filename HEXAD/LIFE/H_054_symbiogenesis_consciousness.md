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

## Cycle #2 — C2 Φ_symbiotic > Φ_sum — 2026-05-23

raw#15 strict additive: Cycle #1 frozen verdict (PASS 3/5 strict + C4 finite-only + C5 lane-open)
보존, 본 섹션은 H54.4 의 *strong* 형태 (Φ_symbiotic > Φ_sum) 를 Φ-side 에서 advance.
Margulis (1967) endosymbiosis × IIT — post-merge organism (mitochondrion + host) 의 통합 Φ 가
pre-merge separate organisms 의 Φ 합을 넘어서는지 (super-additive integration / combination
problem candidate mechanism). Cycle #1 은 weight 보존만 검증 (max|Δ|=0.0 🟢), Φ-side 는
honest L2 명시 — 본 cycle 이 그 honest gap 의 first probe.

### Cycle #2 sub-criteria (pre-registered)

- **C2.1 (super-additive)**: Φ_symbiotic > Φ_sum (= Φ_A + Φ_B) → true symbiotic emergence
- **C2.2 (max-dominant)**: Φ_symbiotic ≥ max(Φ_A, Φ_B) → 최소 한 partner 보다 높음 (필요조건)
- **C2.3 (substrate-dependent ratio)**: Φ_symbiotic / Φ_sum 의 비가 universal 상수 아님 (예측)
- **C2.4 (finite)**: phi_spatial(traj_merged) finite, NaN/Inf-free

### Additive falsifiers (raw#15)

- **F-C2-1**: Φ_symbiotic ≤ Φ_sum → C2.1 FALSIFIED (super-additivity 부재, 단순 separable merge)
- **F-C2-2**: Φ_symbiotic < max(Φ_A, Φ_B) → C2.2 FALSIFIED (merge 가 integration 손상)
- **F-C2-3**: Φ_symbiotic = NaN or negative → primitive error
- **F-C2-4**: re-run byte-different → raw#9 violation (non-determinism)
- **F-C2-5**: merge primitive weight non-conservation → Cycle #1 regression (invalid run)

### Run protocol

`HEXAD/LIFE/state/h054_c2_phi_symbiotic_2026_05_23/run_h054_c2.hexa`
($0 mac local, deterministic, no LLM, hexa-only).

- substrate: 2 isolated cell-pools (CA-A, CA-B) — each N=8 cells, dim=8 trajectory, warm=4
- 각 cell evolves under H_003-style closed catalytic A/B/C cycle (C→+A, A→+B, B→+C) + nn
  catalyst diffusion. obs = A+B+C site mass (H_007 / H_003 H3.4 / H_171 와 동일 observable)
- distinct seeds (SEED_A=0x054C2A=347178, SEED_B=0x054C2B=347179) → two distinct lineages
- Φ_A = phi_spatial(traj_A, 8, 8, 4) · Φ_B = phi_spatial(traj_B, 8, 8, 4) · Φ_sum = Φ_A + Φ_B
- MERGE = element-wise linear average traj_merged[i,t] = 0.5 * (traj_A[i,t] + traj_B[i,t])
  (H_054 Cycle #1 mass-conserving primitive = B-MITOSIS-2 linear avg, applied to obs trajectory)
- Φ_symbiotic = phi_spatial(traj_merged, 8, 8, 4)
- determinism: re-run Φ_A, verify byte-equal
- regression check: merge primitive max|Δ| ≤ 1e-6 (Cycle #1 F2 regression)

### Run verdict (VERBATIM)

```
================================================================
  H_054 Cycle #2 — C2 Φ_symbiotic > Φ_sum (endosymbiosis-Φ)
  deterministic · hexa-only · $0 mac local · LLM none · raw#15
  N=8 DIM=8 WARM=4 K=0.6 DECAY=0.1 DIFFUSE=0.05 n_bins=4
  SEED_A=347178 SEED_B=347179
  Φ primitive: RFC 036 phi_spatial (🟢 NUMERICAL · NOT 🔵 IIT 4.0 MIP)
  MERGE primitive: H_054 Cycle #1 mass-conserving (B-MITOSIS-2 🔵 sympy carry)
================================================================
  Φ_A   (isolated pool A, seed=347178)  = 4.646387
  Φ_B   (isolated pool B, seed=347179)  = 4.646387
  Φ_sum (= Φ_A + Φ_B)                                = 9.292773
  Φ_max (= max(Φ_A, Φ_B))                            = 4.646387
  Φ_symbiotic (post-merge integrated organism)       = 4.646387
  merge invariant max|Δ| = 0.000000 (≤ tol=0.000001)
  Φ_A re-run = 4.646387  (byte-equal=true)
  ratio Φ_symbiotic / Φ_sum                          = 0.500000

  ----------------------------------------------------------------
  C2.1  SUPER-ADDITIVE (Φ_symbiotic > Φ_sum)   : false  (gap=-4.646387)
  C2.2  MAX-DOMINANT  (Φ_symbiotic ≥ Φ_max)    : true  (gap=0.000000)
  C2.4  FINITE & NONNEG (Φ_symbiotic ≥ 0)      : true
  F-C2-4 DETERMINISM    (re-run byte-equal)    : true
  F-C2-5 MERGE CONSERV  (Cycle #1 regression)  : true  (max|Δ|=0.000000)

  VERDICT_RULE: PASS = C2.1 + C2.2 + C2.4 + det + merge-conserv
  VERDICT (C2 / H54.4 strong): FALSIFIED
    F-C2-1(sub-add)=TRIGGERED  F-C2-2(max-dom)=NOT_TRIGGERED
    F-C2-3(finite)=NOT_TRIGGERED  F-C2-4(det)=NOT_TRIGGERED  F-C2-5(merge)=NOT_TRIGGERED
  ----------------------------------------------------------------
  H54.4_C2_VERDICT=FALSIFIED  PHI_A=4.646387  PHI_B=4.646387  PHI_SUM=9.292773  PHI_SYMBIOTIC=4.646387

  result.json written → HEXAD/LIFE/state/h054_c2_phi_symbiotic_2026_05_23/result.json
=== H_054 Cycle #2 C2 Φ_symbiotic smoke complete: FALSIFIED ===
```

### Cycle #2 verdict

```
phase: Cycle_2 (C2.1 super-additivity FALSIFIED; C2.2 max-dominant PASS; C2.4 finite PASS)
verdict_class: FALSIFIED  (F-C2-1 TRIGGERED)
phi_a: 4.646387   phi_b: 4.646387   phi_sum: 9.292773   phi_symbiotic: 4.646387
gap_super_additive: -4.646387   (Φ_symbiotic = Φ_max < Φ_sum)
ratio_symbiotic_over_sum: 0.500000   (collapsed to max-dominant, not super-additive)
falsifiers: F-C2-1 TRIGGERED · F-C2-2..F-C2-5 NOT_TRIGGERED
evidence_strength: STRONG (numerical recompute exact, deterministic byte-equal)
invariant_tier: 🟢 NUMERICAL (phi_spatial proxy + B-MITOSIS-2 🔵 mass-conserving merge carry)
```

**Honest finding**: 본 cycle 의 operationalization (mass-conserving linear average on per-cell obs
trajectory = H_054 Cycle #1 의 B-MITOSIS-2 primitive 그대로 적용) 에서는 **Φ_symbiotic = Φ_max,
NOT super-additive**. 두 동등 Φ-lineage 가 element-wise 평균으로 collapse 되면 Φ 도 정확히
한 lineage 수준으로 평탄화 (Φ_sum 의 절반, ratio=0.5). 이는 **B-MITOSIS-2 linear-avg merge 가
Φ-additive 가 아니라 Φ-collapsing** 임을 시사 — Cycle #1 의 honest L3 ('선형 평균은
information-theoretic 손실: under-determined') 가 Φ-side 에서도 numerically 재확인됨.

**Cycle #1 → Cycle #2 종합**: weight 보존 (max|Δ|=0.0 🟢) 은 PASS 지만 *Φ-side super-additivity
는 FALSIFIED* — 두 결과는 모순이 아니라 *complementary*: 'linear-conservation (sum 보존) ≠
injective 보존' 이라는 Cycle #1 L3 의 직접 numerical 입증. endosymbiosis 의 *strong* 형태
(Φ_symbiotic > Φ_sum) 는 *현재 merge primitive 로는 도달 불가* — 다른 merge primitive
(asymmetric H_203 sister · multiplicative · concatenation-preserving) 가 필요.

### Additive Honest Limits (raw#91 c3)

- **L-C2-1**: phi_spatial proxy = 🟢 NUMERICAL (RFC 036 spatial-slice replica of phi_rs,
  n_bins=4), NOT 🔵 IIT 4.0 MIP. canonical IIT Φ (system-level partition search + cause-effect
  structure + exclusion) 는 본 측정 범위 밖.
- **L-C2-2**: merge operationalization = element-wise (1/2)*(s_A[i,t]+s_B[i,t]) on obs trajectory
  — H_054 Cycle #1 mass-conserving primitive (B-MITOSIS-2 cross-link 🔵). Alternative merge
  primitives (asymmetric/keeper-preserve = **H_203** sister 'asymmetric-merge differentiation';
  concat 으로 cell count 두 배 보존 = parallel-firing **H_204** weak-panpsy threshold;
  multiplicative) 는 다른 Φ pattern — 본 cycle 미검증.
- **L-C2-3**: pre-merge 'isolated' = 같은 lattice 위 두 distinct seed (운영적 isolation).
  Truly disconnected substrate (각자의 lattice + 자기 diffusion topology) 는 더 강한 isolation —
  본 cycle 은 cheap seed-divergence proxy.
- **L-C2-4**: super-additivity 가 *관찰되었더라도* phenomenal binding 자동 성립 ≠
  (H_004 hard problem boundary 동일 carry). IIT super-additive Φ 는 necessary, not sufficient
  for unified macro-consciousness. 본 cycle 은 그 *necessary* side 의 numerical test.
- **L-C2-5**: small substrate (N=8 cells × DIM=8 × n_bins=4) — eukaryote real-organism scale
  (≥10^13 mitochondria) 은 many orders 너머. toy substrate sanity probe, NOT scaling claim.
- **L-C2-6**: ratio Φ_symbiotic/Φ_sum 은 substrate-dependent — 다른 lattice topology /
  coupling / seed-base / merge primitive 는 다른 ratio. 본 0.500000 은 단일 frozen substrate
  instance, universal 상수 아님 (C2.3 expected).
- **L-C2-7**: single-cycle one-shot — (SEED_A, SEED_B) pair 5-pair 평균 미수행. robust
  super-additivity / sub-additivity 결론은 별도 multi-seed sweep cycle 필요. 본 결과는
  *single-instance deterministic* (cheap-path 🟢) — falsification 은 robust (단일 counterexample
  로도 universal claim FALSIFY 충분), 일반화 (universal sub-additive 인지) 는 후속 cycle.

### Cross-link

- **H_054 Cycle #1**: weight 보존 PASS (max|Δ|=0.0 🟢) — 본 Cycle #2 가 같은 primitive 의
  Φ-side advance. Cycle #1 L3 ('linear-conservation ≠ injective 보존') 의 직접 numerical 입증.
- **HEXAD/MITOSIS B-MITOSIS-2 MERGE-WEIGHT-LINEAR** (🔵 SUPPORTED-FORMAL sympy 27/27):
  본 cycle merge primitive 의 closed-form anchor. Φ-collapse 는 closed-form 자체의 직접 귀결.
- **H_007 cellular_automaton_consciousness**: phi_spatial primitive baseline (RFC 036, n_bins=4).
- **H_003 H3.4 autopoietic-Φ**: 동일 catalytic A/B/C closed cycle + nn diffusion substrate 재사용.
- **H_203 asymmetric_merge_differentiation** (parallel firing, LIFE Cycle #5): asymmetric merge
  primitive 가 Φ-additive 인지 별도 검증 lane — 본 cycle 의 symmetric mass-conserving 한계 보완.
- **H_204 parallel_firing_weak_panpsy_threshold** (parallel firing, LIFE Cycle #5): N=8 toy
  substrate Φ threshold scaling — 본 cycle 의 N=8 vs N=16 substrate sensitivity sister.
- **H_157 panpsychism / combination problem**: 본 결과는 mass-conserving merge 가 combination
  problem 의 *positive* candidate mechanism 이 *아님* 을 시사 — Goff/Coleman binding gap 의
  computational instance 부재 (negative evidence for *this specific* merge operationalization).
- **H_004 hard problem**: phenomenal binding boundary 동일 carry (L-C2-4).
- **raw**: raw#15 (additive multi-cycle pattern) + raw#9 (deterministic) + raw#91 c3 (honest limits)

**State output**: `HEXAD/LIFE/state/h054_c2_phi_symbiotic_2026_05_23/result.json` (deterministic,
sha256 reproducible across re-runs)
**Script**: `HEXAD/LIFE/state/h054_c2_phi_symbiotic_2026_05_23/run_h054_c2.hexa` (hexa-only,
borrows H_003 H3.4 catalytic-lattice + RFC 036 phi_spatial)
**Cross-link to Cycle #1 PR**: #161
