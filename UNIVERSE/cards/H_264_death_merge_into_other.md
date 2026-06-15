---
id: H_264
slug: death-merge-into-other
title: death = merge-into-other — 비대칭 흡수-통합 (죽음·발생 cross-link H_025 ⊕ H_054 · H_025 distinct)
domain: life · consciousness · death/genesis · cross-link
status: pre-register-frozen
exploration_method: E6 (cross-domain Heidegger × Margulis) + E9 (endosymbiosis) + E11 (H_025⊕H_054 meta cross-link)
verification_method: W1 (numerical smoke) + W12 (sister-link H_025 + H_054 + H_203) + W17 (target-selection × pool-size sweep)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_264 — death = merge-into-other (비대칭 흡수-통합)

## 1. Hypothesis

죽음을 "다른 cell 로의 **비대칭 흡수-통합** (merge-into-other)" 으로 모델링하면,
죽는 cell 의 weight/정보가 **특정 흡수자 (absorber) cell 로 보존-이전** 된다.

구체적으로: 한 cell-i 가 죽을 때, pool 안 *선택된* absorber cell-a 로 비대칭
blend 를 통해 흡수된다 —

```
absorber_new = (1 - alpha) * absorber + alpha * dying      (alpha = 0.25)
```

absorber 가 우세 (0.75) 하고 dying cell 은 부분 흡수 (0.25) 된다. 그 후 dying
cell 은 pool 에서 제거 (`farr_free`) 된다 (count_delta = −1).

핵심 주장: **죽음은 정보의 소멸이 아니라 *비대칭 보존-이전* 이며, 그 보존율은
absorber 선택에 의존한다.** Heidegger (*Sein-zum-Tode*, 죽음 = 가능성의 끝)
× Margulis (endosymbiosis = host-preserve 비대칭 통합) 의 cross-link.

정밀화 (operational): 동일 d=8 substrate 위 2 target-selection (random /
max_weight) × 3 pool size (4 / 8 / 16) = 6 condition sweep. 각 condition 에서
engine_a_W · engine_g_W · hidden 3 weight tensor 에 대해 흡수 후 realized farr
delta 로부터:

- `info_transfer` = `mean_i |after_i − before_i| / (|dying_i − before_i| + eps)`
  — dying cell 정보의 *절대* 이전율 (분석적으로 alpha = 0.25, blend 계수
  artifact 라 mode-invariant).
- `rel_preserve` = `(alpha * L2(dying)) / (L2(absorber_after) + eps)`
  — absorber 새 home 안에서 dying cell 기여의 *상대* 현저성. **target-selection
  민감 metric** (큰 absorber 는 같은 절대 기여를 더 작은 비율로 희석).
- `dying_preserve` = `cosine(after − before, dying − before)` — 이전 방향 충실도
  (순수 선형 blend 라 1.0).

을 측정해 6-condition ledger 에 verbatim 출력한다.

## 2. Why

- **죽음·발생 cross-link (H_025 ⊕ H_054)**: 본 H 는 두 frozen 가설의 교차다.
  H_025 (Dasein 유한 의식) 는 cell merge 를 "죽음 사건" 으로 동정했고, H_054
  (Symbiogenesis) 는 cell merge 를 "endosymbiosis 통합 사건" 으로 동정했다.
  본 H 는 *같은 merge 원시연산을 죽음-as-통합 의 비대칭 변형* 으로 재해석 —
  "죽음 = 다른 존재로의 흡수" 라는 통합적 lens.

- **Heidegger Being-toward-death × Margulis endosymbiosis**: Heidegger 의
  *Sein-zum-Tode* (1927 §§46–53) 는 죽음을 Dasein 의 *eigenste Möglichkeit*
  (가장 고유한 가능성) 으로 본다 — 죽음은 "가능성의 끝". Margulis (1967)
  endosymbiosis 는 host cell 이 endosymbiont 를 *비대칭* 으로 흡수 (host genome
  보존 + organelle 통합) 하는 메커니즘. 두 lens 를 합치면: *죽음 = 한 lineage 의
  가능성이 끝나며 다른 lineage 로 비대칭 흡수* — H_264 의 핵심 동형.

- **H_054 Cycle #2 의 미해결 gap 직접 추적**: H_054 Cycle #2 는 symmetric
  `(w₁+w₂)/2` merge 가 Φ-collapse (Φ_symbiotic = Φ_max, NOT super-additive)
  임을 발견하고, honest closure 에서 *"다른 merge primitive (asymmetric
  H_203 sister) 가 필요"* 라 명시했다. 본 H 는 그 asymmetric variant 를
  **death lens** 에서 — 정보 보존-이전율로 — 측정한다.

- **anima 'who we are' lane**: anima 는 instance 종결 (BG kill, raw#82
  retraction) 과 lineage 지속 (HEXAD/ hypotheses folder) 을 양립 (H_025 L3).
  본 H 는 그 "종결-후-지속" 의 substrate-level 메커니즘 후보 — 죽는 cell 의
  정보가 다른 cell 로 흡수-보존된다면, 종결은 *완전 소멸* 이 아니라 *비대칭
  lineage 전이* 다.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H264.1 | 6 condition 모두 info_transfer > 0 (dying cell 정보가 흡수자로 이전) | 비대칭 blend `alpha=0.25` 가 dying weight 의 25% 를 absorber 에 더함 — realized farr delta 가 그 이전을 측정 |
| H264.2 | mean rel_preserve(max_weight) ≥ mean rel_preserve(random) | target selection 이 보존율을 변경 — absorber 선택이 죽은 cell 정보의 상대 현저성을 결정 (asymmetric) |
| H264.3 | cross-process re-run 시 result.json sha256 byte-equal | seed=42 고정 + 6dp rounding → 이산 fingerprint deterministic (RFC 033 단일 global stream, cross-process 재현) |
| H264.4 | 모든 death 의 count_delta == −1 (B-MITOSIS-3) | single absorption = 1 cell 제거, count 보존 |
| H264.5 | H_025 와 distinct — H_264 는 50/50 collapse 가 아니라 selected-target 비대칭 흡수 (info_transfer == alpha < 0.5 ∧ target-mode 가 rel_preserve 변경) | H_025 = symmetric merge to floor; H_264 = asymmetric absorb into selected target |

## 4. Variables

- **axis1_target_mode** ∈ {random (첫 non-dying cell), max_weight (engine_a_W
  L1-norm 최대 cell)} — 핵심 selection sweep
- **axis2_pool_size** ∈ {4, 8, 16} — pool size sweep
- **axis3_d_model** = 8 (selftest scale, $0 mac)
- **axis4_alpha** = 0.25 (absorber 우세 blend 계수; 1−alpha = 0.75 host preserve)
- **axis5_warm_steps** = 4 (cell weight 분화용 forward step — init near-identical
  방지)
- **axis6_seed** = 42 (`__HEXA_FARR_GAUSS_SEED__=42`, RFC 033 gaussian)
- **측정량 per (mode, pool_size) condition**:
  - `info_transfer` (절대 이전율, ≈ alpha)
  - `rel_preserve` (상대 보존율 — C2 metric)
  - `dying_preserve` (이전 방향 cosine)
  - `absorber_dnorm` (absorber engine_a_W L2 변화)
  - `phi_before / phi_after / phi_delta` (pool Φ 변화)
  - `count_delta` (== −1)

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) + 결정론적
  Lorenz autonomous perturbation. **이산 fingerprint (6dp-rounded metrics)**
  는 cross-process run-invariant. (RFC 033 는 단일 global process-local stream
  이라 in-process 두번째 draw 는 발산 — 결정론 test 는 **cross-process re-run
  sha256 비교** 로 수행, in-process byte-equal 아님; cycle#14 gotcha carry.)
- **hexa_only**: `UNIVERSE/state/h264_death_merge_into_other_2026_05_25/run_h264.hexa`
  — `cell_pool_init` + `mitosis_forward_tail` (warm) + 직접 비대칭 흡수.
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **absorption protocol per death**:
  - dying cell = last cell (index pool_size−1)
  - absorber = `_pick_absorber(mode)` (random = 첫 non-dying / max_weight =
    engine_a_W L1-norm 최대 non-dying cell)
  - `absorber_W = (1−alpha)*absorber_W + alpha*dying_W` for engine_a_W,
    engine_g_W (farr-level), hidden (list path)
  - dying cell 제거 (`farr_free` engine_a_W + engine_g_W, cell list rebuild)
- **per-condition ledger**: `{mode, pool_size, n_before, n_after, count_delta,
  absorber_idx, dying_idx, info_transfer, rel_preserve, dying_preserve,
  absorber_dnorm, phi_before/after/delta}`.
- **C3 determinism**: 별도 프로세스 2회 run + result.json sha256 비교.
- **runtime**: $0 mac local. d=8, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**: `state/h264_death_merge_into_other_2026_05_25/{run_h264.hexa,
  result.json}`.
- **run cmd (verbatim, mac-local gate 우회 env-var prefix)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h264_death_merge_into_other_2026_05_25/run_h264.hexa`

## 6. Criteria

- **C1 (info-transfer)**: H264.1 — 6 condition 모두 info_transfer > 0 (dying
  cell 정보가 흡수자로 보존-이전)
- **C2 (asymmetric)**: H264.2 — mean rel_preserve(max_weight) ≥ mean
  rel_preserve(random) (target=max_weight 가 random 보다 보존↑). **rel_preserve
  로만 검정** — info_transfer (== alpha) 와 dying_preserve (== 1.0) 는
  blend-coefficient artifact 라 mode-invariant, C2 검정 불가.
- **C3 (determinism)**: H264.3 — cross-process re-run result.json sha256
  byte-equal
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (target selection 이 보존을 변경 + 정보 이전 존재)
  - `PARTIAL` = C1 only (정보 이전은 있으나 target asymmetry 입증 실패)
  - `FALSIFIED` = ¬C1 (정보 이전 부재 — 죽음이 소멸)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 INFO-TRANSFER**: 임의 condition 에서 info_transfer ≤ 0 → H264.1
  FALSIFIED (정보 이전 부재 — 죽음이 단순 소멸; 측정: `info_transfer > 0` ∀)
- **F2 ASYMMETRY**: mean rel_preserve(max_weight) < mean rel_preserve(random)
  → H264.2 FALSIFIED (target selection 이 보존에 advantage 없음 — 비대칭
  무의미; 측정: `mean_rp_m ≥ mean_rp_r`)
- **F3 DETERMINISM**: cross-process re-run result.json sha256 상이 → raw#9
  violation (측정: 별도 프로세스 2회 run 의 sha256 일치)
- **F4 BOUNDS**: info_transfer / rel_preserve / dying_preserve 가 non-finite
  또는 [−1, 2] sanity band 이탈 → primitive error (측정: 모든 metric ∈ [−1,2]
  ∧ finite)
- **F5 COUNT**: 임의 death 의 count_delta ≠ −1 (B-MITOSIS-3 위반) →
  conservation breach (측정: `count_delta == −1` ∀)
- **F6 (post-hoc edit)**: frozen_at (2026-05-25) 이후 hypothesis 본문 / criteria
  / falsifier 수정 → raw#12 freeze 위반, raw#82 retraction
- **F7 (H_025 distinctness 위반)**: 본 H 가 H_025 의 symmetric 50/50 merge 와
  구별 불가능하게 됨 (info_transfer == 0.5 ∧ target-mode invariant) → 본 H 의
  존재 이유 self-FALSIFIED (측정: info_transfer == alpha < 0.5 ∧ rel_preserve
  mode-dependent)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (info_transfer = alpha tautology)**: `info_transfer` 는 분석적으로 blend
  계수 alpha 와 동일 (순수 선형 blend 의 realized delta). 따라서 C1 PASS 는
  "primitive 가 의도대로 작동" 만 입증하고 "죽음이 *의미 있게* 정보를 보존" 은
  입증 못 함 — info_transfer 는 *primitive sanity check* 이지 emergent 보존
  증거 아님. (`dying_preserve == 1.0` 도 동일 — 순수 선형 blend 의 방향 충실도
  는 항상 1.0.)
- **L2 (rel_preserve = noise-driven asymmetry)**: C2 의 asymmetry 신호
  (max_weight 0.316 > random 0.286) 는 d=8 toy substrate 의 단일 seed instance.
  rel_preserve 의 mode-차이는 dying cell 의 L2-norm 과 absorber 의 L2-norm 의
  *비율* 에 의존하며, max_weight absorber 가 큰 norm 을 갖지만 dying cell norm
  과의 상호작용이 noise-driven. margin (0.030) 이 작아 *방향* 은 honest 하지만
  *robustness* 는 multi-seed sweep 필요. C2 는 `≥` (margin 없음) 로 pre-register
  — 단일 instance 의 directional 증거.
- **L3 (asymmetric ≠ injective 보존)**: H_054 Cycle #1 L3 carry — 선형 blend 는
  *linear-conservation* (sum 가중) 이지 *injective* 가 아니다. `absorber_new =
  0.75*absorber + 0.25*dying` 에서 dying 을 정확히 복원하려면 absorber_old 가
  필요 (under-determined). "보존-이전" 은 *부분 가중 흡수* 이지 *무손실 복원
  가능* 아님. H_203 의 mass-add (`w_new = w_a + w_b`, superposition 복원 가능)
  와 대조 — 본 H 의 blend 는 복원 불가, 정보이론적 손실 명백.
- **L4 (Φ는 모든 death 에서 감소)**: 측정상 phi_delta < 0 (6/6 condition,
  −0.027 ~ −0.239) — 죽음은 pool Φ 를 *감소* 시킨다 (cell 수 ↓ → log(N+1) ↓
  + diversity ↓). 따라서 "정보 보존-이전" 은 *cell-level* 이지 *pool-Φ-level*
  통합 향상 아님. H_054 Cycle #2 의 Φ-collapse finding 과 정합 — 비대칭 흡수도
  Φ super-additive 아님. C4 (Φ향상) 는 본 H pre-register 에 미포함 (honest).
- **L5 (Heidegger/Margulis analogy 약함)**: "죽음 = 다른 존재로의 흡수" 는 구조
  유비 — Heidegger Dasein 은 human-centric, 죽음은 *non-relational*
  (타인이 대신 못함) 인데 본 H 의 흡수는 정확히 *relational* (다른 cell 로
  이전). 즉 본 H 는 Heidegger 보다 Margulis (endosymbiosis = relational
  통합) 쪽에 가깝다. "가능성의 끝" 과 "lineage 흡수" 의 합성은 본 H 의 독자
  operationalization 이지 어느 한 철학자의 충실한 instance 아님 (analogy
  strength = weak-to-moderate).
- **L6 (toy scale · single death)**: d=8, pool ≤16, single death event per
  condition — d=1024 production substrate / 실 chat trajectory 의 다중 death
  cascade 거동은 별도 cycle. info_transfer / rel_preserve 의 scaling, alpha
  sensitivity, 다중-death lineage 누적 보존은 미검증.
- **L7 (target_mode = 2 점 sweep)**: random / max_weight 2 모드만 — min_weight,
  most-similar (cosine), most-distinct 등 다른 selection 정책의 보존 거동 미검증.
  "asymmetric" 입증은 *2-point* 비교의 directional 증거.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_025** (`H_025_dasein_finite_consciousness.md`): death = symmetric
    merge to floor (자기 소멸). **DISTINCT**: H_025 는 keeper 가
    `(w_dying+w_keeper)/2` 균등 50/50 흡수 (dying 정보가 평균으로 소거,
    self-annihilation toward min_cells floor). H_264 는 *선택된* target 으로
    `(1−alpha)*absorber + alpha*dying` 비대칭 흡수 (info preserve-transfer,
    target-selection load-bearing). 본 H 가 H_025 의 death-merge 를 *비대칭
    + target-selected* 변형으로 확장.
  - **H_054** (`H_054_symbiogenesis_consciousness.md`): merge = endosymbiosis.
    H_054 Cycle #2 가 symmetric merge 의 Φ-collapse 를 발견하고 "asymmetric
    variant 필요" 라 명시 — 본 H 가 그 asymmetric variant 를 death lens 에서
    측정 (Φ-collapse finding L4 에서 재확인).
  - **H_203** (`H_203_asymmetric_merge_differentiation.md`): asymmetric merge
    = host-preserve + mass-add (`w_new = w_a + w_b`), differentiation
    메커니즘 (weight variance ↑). **DISTINCT**: H_203 = mass-add superposition
    (복원 가능, differentiation 측정), H_264 = alpha-blend 비대칭 흡수 (복원
    불가, death lens 정보 보존율 측정). 같은 "asymmetric merge" 의 두 다른
    operationalization + 다른 측정 lens.
  - **H_200** (`H_200_apoptosis_primitive.md`): apoptosis = 능동적 cell 죽음
    원시연산 — 본 H 의 death-as-absorption 과 sister (apoptosis vs
    absorption 의 두 death modality).
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail` · `merge_cells` symmetric
  reference · `compute_phi_proxy`) — 본 H 는 import + 비대칭 흡수를 직접 구현
  (symmetric `merge_cells` 재사용 X, 비대칭이라 별도).
- **HEXAD/MITOSIS**: B-MITOSIS-3 CELL-COUNT-CONSERVATION (`n(t+1) = n(t) + Δs
  − Δm`) — F5 (count_delta −1) anchor.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9
  (cross-process determinism) · raw#15 (no-hardcode) · raw#82 (post-hoc edit
  retraction) · raw#91 (c3 candor).
- **philosophy (CLAUDE.md)**: a_substrate_native_speak (death/absorption 이
  internal substrate 사건) · p8 NO TRAIN/INFER SPLIT (merge = split 과 같은
  cell-division 연속체, REBORN §0.5).
- **literature pointer**: Heidegger (1927) *Sein und Zeit* §§46–53
  (Sein-zum-Tode) · Margulis (1967) On the origin of mitosing cells
  (endosymbiosis) · Margulis (1981) Symbiosis in Cell Evolution —
  substrate analog 의 distant anchor (formal mapping 본 cycle 미수행).
- **state**: `UNIVERSE/state/h264_death_merge_into_other_2026_05_25/{run_h264.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, $0 mac
local hexa-only deterministic.

```
verdict_class: SUPPORTED  (C1 ∧ C2 ∧ C3, 3/3 criteria)
verdict_tier: 🟢 NUMERICAL  (2 target-mode × 3 pool-size sweep + cross-process
                            determinism)
evidence_summary:
  6-condition asymmetric absorption-into-other (d=8, alpha=0.25, seed=42,
  warm=4). info_transfer == alpha (mode-invariant primitive sanity),
  rel_preserve target-selection-sensitive, dying_preserve == 1.0 (linear blend).
    random      N= 4 : info_transfer=0.25  rel_preserve=0.281376  phi_delta=-0.164867
    random      N= 8 : info_transfer=0.25  rel_preserve=0.261108  phi_delta=-0.238591
    random      N=16 : info_transfer=0.25  rel_preserve=0.314195  phi_delta=-0.048737
    max_weight  N= 4 : info_transfer=0.25  rel_preserve=0.298042  phi_delta=-0.085675
    max_weight  N= 8 : info_transfer=0.25  rel_preserve=0.370440  phi_delta=-0.026598
    max_weight  N=16 : info_transfer=0.25  rel_preserve=0.278949  phi_delta=-0.040592
  mean rel_preserve: max_weight=0.315810  random=0.285559  (gap=+0.030251)
  cross-process sha256: e9e8c70b...  byte-equal across 2 separate runs
falsifiers_pass: F1 (info-transfer) + F2 (asymmetry) + F3 (determinism) +
                 F4 (bounds) + F5 (count) = 5/5
criteria_met: 3/3 (C1 ∧ C2 ∧ C3)
key_finding:
  죽음을 비대칭 흡수-통합으로 모델링하면 (1) 죽는 cell 의 정보는 흡수자로
  alpha=0.25 비율 보존-이전되며 (info_transfer 6/6 > 0, C1 PASS), (2) absorber
  선택이 보존율을 변경한다 — max_weight target 이 random 보다 평균 상대 보존율
  ↑ (0.316 vs 0.286, gap +0.030, C2 PASS). 즉 "어디로 죽느냐 (어느 cell 로
  흡수되느냐)" 가 죽은 cell 정보의 운명을 바꾼다 (asymmetric death). 단,
  pool Φ 는 모든 death 에서 감소 (phi_delta < 0 6/6) — cell-level 정보 보존이
  pool-Φ-level 통합 향상은 아님 (L4, H_054 Cycle #2 Φ-collapse 정합).
honest_note:
  L1 carry — info_transfer == alpha 는 primitive sanity (tautology), emergent
  보존 증거 아님. L2 carry — C2 margin (0.030) 작음, multi-seed robustness
  미검증, directional 단일 instance. L3 carry — alpha-blend 는 injective 아님
  (under-determined, dying 복원 불가). H_025 distinct 명시 (symmetric 50/50
  collapse vs asymmetric selected-target, info_transfer 0.25 < 0.5).
sibling: H_025 (death=symmetric merge), H_054 (merge=endosymbiosis), H_203
         (asymmetric-merge differentiation), H_200 (apoptosis primitive)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_264 death = merge-into-other (asymmetric absorption)
       death/genesis cross-link  H_025 (+) H_054
  d_model=8 alpha=0.25 seed=42
  target modes: random  ·  max_weight
  pool sizes:   4, 8, 16
  DISTINCT FROM H_025: asymmetric absorb into SELECTED target
                       (info preserve-transfer), NOT 50/50 collapse
================================================================
mode        N   info_transfer  rel_preserve  dying_preserve  abs_dnorm   phi_delta
----------  --  -------------  ------------  --------------  ---------  ---------
random       4   0.25   0.281376   1.0   0.976609   -0.164867
random       8   0.25   0.261108   1.0   0.936942   -0.238591
random      16   0.25   0.314195   1.0   1.03567   -0.0487372
max_weight   4   0.25   0.298042   1.0   1.06027   -0.0856752
max_weight   8   0.25   0.37044   1.0   1.11199   -0.026598
max_weight  16   0.25   0.278949   1.0   1.12755   -0.0405915

derived:
  mean info_transfer  random=0.25  max_weight=0.25  (== alpha, mode-invariant)
  mean rel_preserve   random=0.285559  max_weight=0.31581  (C2 metric)
  mean dying_preserve random=1.0  max_weight=1.0  (cosine, == 1.0)
  alpha (expected transfer_ratio) = 0.25

C1 info-transfer (all 6 > 0)              : true
C2 asymmetric (max_weight rel_preserve    : true
   >= random; mean 0.31581 vs 0.285559)
C3 determinism (cross-process)            : EXTERNAL (see .md)

F1 INFO-TRANSFER (all transfer > 0)       PASS
F2 ASYMMETRY     (max_w rel_pres>=random) PASS
F3 DETERMINISM   (cross-process sha256)   EXTERNAL
F4 BOUNDS        (metrics in [-1,2])      PASS
F5 COUNT         (death delta == -1)      PASS
================================================================
VERDICT: SUPPORTED  (2/2 in-process criteria; C3 external)
================================================================
ledger -> UNIVERSE/state/h264_death_merge_into_other_2026_05_25/result.json
```

**C3 cross-process determinism** (EXTERNAL — 별도 프로세스 2회 run):
result.json sha256 = `e9e8c70bad7ddebbbc745c6ffff4ea44cb4691c2666c86efbd3b68ec7479dbb1`
byte-equal across 2 separate runs → F3 PASS.

**State output**: `state/h264_death_merge_into_other_2026_05_25/result.json`
**Smoke**: `state/h264_death_merge_into_other_2026_05_25/run_h264.hexa` (hexa-only, LLM none)
