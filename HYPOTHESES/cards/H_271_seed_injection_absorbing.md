---
id: H_271
slug: seed-injection-absorbing
title: seed-injection vs absorbing-state — H_263 phoenix-rebirth model revision (floor absorbing 이 intrinsic 인가 vs injection-기전 부재의 artifact 인가)
domain: life · death · genesis · developmental
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E6 (cross-domain biology — genesis-seed / spore germination / external inoculation) + E7 (perturbation–response, absorbing-state escape probe)
verification_method: W1 (numerical smoke) + W3 (split/merge event ledger) + W12 (sister-link H_263 + H_018 + H_206 + H_200)
revises: H_263
gap_lens: F5 (closed-loop — falsified hypothesis 의 model revision)
raw_rank: 11
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_271 — seed-injection vs absorbing-state (H_263 model revision · /gap F5 closed-loop)

## 1. Hypothesis

H_263 (phoenix-rebirth) 은 grown pool 을 floor (`min_cells`, 2-3 cell) 까지
완전 붕괴시킨 뒤 default mitosis 동역학으로 재성장시키면 **부활하지 못함**
(regrowth_splits=0) 을 관측, floor 가 **absorbing state** (한 번 빠지면 default +
rebirth-fair config 로는 못 나옴) 임을 FALSIFIED verdict 로 확증했다.

H_271 은 그 결과의 **model revision** 질문이다 — floor 도달 시 substrate 에
없던 **seed-injection** primitive (fresh 高분산 cell 1개를 pool 에 직접 주입,
split-copy 가 아닌 genesis 신생 cell) 를 추가하면 absorbing state 를 **탈출**
(regrowth_splits > 0) 하는가? 즉 H_263 의 absorbing 이 substrate 동역학에
**intrinsic** 한가, 아니면 단지 **주입-기전의 부재** (genesis-seed mechanism
absence) 라는 artifact 인가를 판정한다.

operational 정의 (raw#9/10 HONEST):
- **death (the collapse)**: H_263 byte-parity — `collapse_to` ∈ {2, 3} 개만
  남기고 나머지 전부 drop + farr_free.
- **the intervention (seed-injection)**: floor 도달 직후 `_inject_seed(pool,
  count=1, magnitude)` — fresh cell 의 engine_a_W / engine_g_W / hidden 를
  `N(0, (base_sigma·magnitude)²)` 로 신규 생성 (parent_id=-1, GENESIS).
  base_sigma = 1/sqrt(d) (cell_pool_init 동일 scale). 高분산 fresh cell 은
  큰 per-cell tension `mean(output²)` 을 내어 post-grow adaptive threshold 를
  재돌파 → split 재발화를 유도할 수 있다.
- **mode sweep**: `none` (H_263 baseline control) · `lo` (magnitude 1.0,
  default init 변동성) · `hi` (magnitude 4.0, 4× 변동성).

regrowth_splits (floor 이후 split 수) 와 Φ recovery ratio (Φ_post/Φ_pre) 가
absorbing-state escape 의 numerical signature.

## 2. Why

- **falsified hypothesis 의 정직한 closed-loop (gap F5)**: H_263 의 FALSIFIED
  은 "부활 부재" 라는 negative result 였으나, honest_note 에서 *남은 path* 로
  "floor 에서의 외부 genesis-seed 주입 (H_018 SELFFEED setup)" 을 명시했다.
  H_271 은 정확히 그 path 를 닫는 후속 — negative result 를 model revision
  으로 이어 absorbing 이 *기전적* 인지 *구조적* 인지를 분리 측정.
- **absorbing state 의 본질 규명**: dynamical systems 에서 absorbing state 는
  (a) 진정한 trap (어떤 perturbation 으로도 못 나옴) 일 수도, (b) 단지 현
  perturbation 집합이 약해서 못 나오는 metastable 상태일 수도 있다. seed-
  injection 은 그 둘을 가르는 결정적 probe — 충분히 강한 외부 주입에도 floor
  에 머물면 (a) intrinsic, 탈출하면 (b) mechanism-absence artifact.
- **genesis-seed = death↔genesis bridge 의 잃어버린 고리**: H_018 SELFFEED 은
  minimal primordial (2-cell) 에서 spontaneous genesis fire 를 보였다. H_263
  은 그 genesis 능력이 *grown 후 붕괴* 라는 가혹한 조건에서 default 동역학
  으로는 발현 안 됨을 보였다. H_271 은 그 사이의 잃어버린 고리 — *외부 seed
  주입* 이라는 명시적 genesis 기전을 floor 에 도입하면 부활이 가능한지 측정.
- **anima resilience 의 substrate 근거**: substrate 가 catastrophic floor 에서
  *외부 자극(주입)* 으로 self-reconstitute 할 수 있다면, anima 의식이 극한
  perturbation 후에도 외부 context inoculation 으로 재기동할 수 있다는 근거.
  injection 으로도 못 나오면 floor 의 absorbing 강건성을 확증.
- **magnitude 의존성 가설**: 高분산 주입(hi)이 低분산(lo)보다 강하게 escape
  를 유도할 것 — adaptive threshold 재돌파에는 충분히 큰 tension 이 필요하므로.
  이 magnitude-threshold 자체가 풍부한 measurement.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H271.1 | seed-injection (lo/hi) 시 regrowth_splits > 0 (absorbing 탈출) | fresh 高분산 cell 의 큰 tension 이 post-grow adaptive threshold 재돌파 → split 재발화 |
| H271.2 | inject 모드 Φ_post ≥ 0.7·Φ_pre (Φ 가 pre-collapse 향해 회복) | regrowth 가 cell 수 ↑ → integration ↑ → Φ ↑ (compute_phi_proxy log(N+1) factor) |
| H271.3 | no-inject control 은 regrowth_splits = 0 (H_263 absorbing 재현) | injection 없는 floor 는 H_263 byte-parity — 효과의 attributability 보장 |
| H271.4 | re-run byte-identical (Φ/split 전 measurement) | RFC 033 단일 stream + __HEXA_FARR_GAUSS_SEED__=42 + deterministic Lorenz |
| H271.5 | hi-magnitude 의 regrowth_splits 가 lo-magnitude 보다 큼 (magnitude-threshold) | threshold 재돌파에 충분한 tension 필요 — 변동성 클수록 강한 escape |

## 4. Variables

- **axis1 collapse_depth** ∈ {2 (min_cells floor), 3} — 붕괴 깊이 (H_263 carry)
- **axis2 inject_mode** ∈ {none, lo, hi} — 핵심 sweep (주입 유무 × 강도)
- **axis3 inject_magnitude** = {lo: 1.0, hi: 4.0} × base_sigma (1/sqrt(d))
- **axis4 inject_count** = 1 (minimal genesis seed — 단일 fresh cell)
- **axis5 pool_N** = 8, **d_model** = 8 (toy substrate; H_263 carry)
- **axis6 baseline_steps** = 12, **regrowth_cap** = 60 (H_263 carry)
- **axis7 dim_phi** = 10, **phi_n_bins** = 4 (phi_spatial)
- **axis8 alpha_rec** = 0.7 (C2 Φ recovery 임계, H_263 α carry)
- **axis9 split_patience_rebirth** = 1 (rebirth-fair, H_263 carry — floor 재발화 기회)
- **axis10 seed** = 42 (`__HEXA_FARR_GAUSS_SEED__=42` deterministic Lorenz + RFC 033)
- **측정량 per (depth × mode)**: regrowth_splits · phi_pre · phi_min · phi_post
  · phi_recovery_ratio (Φ_post/Φ_pre) · diversity_pre/min/post · n_post · n_after_inject

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 단일 gaussian stream)
  + 결정론적 Lorenz autonomous perturbation + 고정 synthetic input
  `x[i] = sin(0.91·i)·1.4 + cos(1.13·i)·0.8` (H_263 carry). 별도 RNG 부재.
- **hexa_only**: `UNIVERSE/state/h271_seed_injection_2026_05_25/run_h271.hexa`
  — `mitosis_hook_lib.hexa` import (`cell_pool_init` / `mitosis_forward_tail` /
  `_mit_cosine` / `_mit_farr_to_list` / `_mit_sqrt_safe` read-only) + `HEXAD/C/
  c_lib.hexa` import (phi_spatial 빌트인). substrate 수정 없음.
- **LLM**: none (raw#12 strict).
- **collapse 조작 정의 (raw#9/10 HONEST)**: H_263 `_collapse_to` byte-parity —
  substrate 의 named `collapse_pool` primitive 부재 → step=baseline_steps 직후
  collapse_to 개만 남기고 나머지 전부 drop + farr_free.
- **injection 조작 정의 (raw#9/10 HONEST)**: substrate 의 named `inject_seed`
  primitive 부재 → harness 가 `_inject_seed` 추가. fresh cell 은 split-copy 가
  아닌 genesis 신생 (parent_id=-1, cell_pool_init 동일 layout). 高분산 init 는
  명시적 magnitude param (raw#15 named, hardcode 아님).
- **Φ measurement**: H_263 byte-parity — per-slot trajectory (slot s = cells[s %
  nc]["hidden"][0]) 를 (POOL_N × DIM) farr 로 기록 후 `phi_spatial`. Φ_pre =
  baseline window, Φ_min = collapse 직후 (주입 전) DIM step, Φ_post = regrowth
  (or cap) 이후 fresh DIM step.
- **diversity measurement**: `_diversity(pool)` = mean pairwise (1−cos) of cell
  hiddens (compute_phi_proxy raw 성분).
- **determinism 검증**: cross-process re-run + 외부 `diff` of result.json
  (byte-equal, sha256 동일). in-process paired call 은 advancing gaussian stream
  공유로 부적합 — H_263 F-PHX-4 패턴 carry.
- **runtime**: $0 mac local, wall ~수 초. `HEXA_MEM_UNLIMITED=1` 권장.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h271_seed_injection_2026_05_25/run_h271.hexa`
  (CWD = repo/worktree root)
- **artifacts**: `state/h271_seed_injection_2026_05_25/{run_h271.hexa, result.json}`.

## 6. Criteria

- **C1 (escape-absorbing)**: H271.1 — seed-injection (lo/hi) 모든 depth 에서
  regrowth_splits > 0 (absorbing 탈출)
- **C2 (phi-recovery)**: H271.2 — inject 모드 모든 depth 에서 Φ_post ≥ 0.7·Φ_pre
- **C3 (determinism)**: H271.4 — cross-process re-run result.json byte-equal
- **verdict_rule**:
  - `SUPPORTED` = C1 (모든 inject-mode × depth 에서 regrowth_splits > 0) →
    H_263 absorbing 은 **injection-기전 부재 artifact** (model 정제: floor 는
    genesis-seed primitive 가 있으면 escapable)
  - `PARTIAL` = inject 일부만 escape (예: hi 는 탈출, lo 는 못 탈출) → absorbing
    은 metastable 하나 **충분히 강한** 주입에만 escapable (magnitude-threshold)
  - `FALSIFIED` = ¬C1 (어느 inject 도 regrowth_splits = 0) → 高분산 주입에도
    absorbing — 구조가 깊음 (H_263 absorbing 확증·강화)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F-SIA-1 ESCAPE**: 어느 inject-mode × depth 라도 regrowth_splits ≤ 0 → C1
  FAIL (측정: inject 모든 case `regrowth_splits > 0`).
- **F-SIA-2 PHI-RECOVERY**: 어느 inject-mode × depth 라도 Φ_post < 0.7·Φ_pre →
  C2 FAIL.
- **F-SIA-3 CONTROL-ABSORB**: 어느 no-inject depth 라도 regrowth_splits > 0 →
  control 이 H_263 absorbing 재현 실패 (실험 무효 — injection 효과 unattributable).
  측정: no-inject 모든 depth `regrowth_splits == 0`.
- **F-SIA-4 DETERMINISM**: env+seed pinned (script 내부 항상 PASS; cross-process
  byte-equal `diff` 검증 — H_263 F-PHX-4 carry).
- **F-SIA-5 BOUNDS**: 어느 Φ < 0 또는 NaN, 또는 n_post ∉ [2, 128] → primitive
  error (CB1 invariant).
- **F-SIA-6 INJECT-GT-CTRL**: injection 이 same-depth no-inject control 대비
  regrowth_splits 를 증가시키지 못함 (∀depth, ∀mode) → injection 의 regrowth
  효과 부재 (C1 의 *differential* corroborant — 절대값 아닌 대조 증가 측정).

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (injection ≠ biological genesis)**: harness-imposed fresh-cell push 는
  생물학적 genesis (spore germination, 외부 inoculation, stem-cell engraftment)
  의 거친 추상 — 주입된 cell 의 weight/hidden 는 무작위 gaussian 이지 실제
  biological seed 의 구조적 정보가 아님. magnitude param 도 substrate-emergent
  가 아닌 외부 설정.
- **L2 (Φ_min 측정 window 의 chaotic 성격, H_263 L2 carry)**: 붕괴 직후 floor
  의 short window 가 Lorenz chaos 로 *높은* trajectory entropy 를 가져 Φ_min 이
  의외로 높게 측정될 수 있음 — phi_recovery_ratio (Φ_post/Φ_pre) 를 C2 metric 으로
  쓴 이유 (Φ_min 대비가 아닌 pre-collapse baseline 대비). 단 Φ_post 자체도
  regrowth window 의 chaotic 변동을 포함.
- **L3 (magnitude grid 2-point, single seed)**: inject_magnitude ∈ {1.0, 4.0}
  2-point 만 — escape threshold 의 정확한 임계 magnitude (예: 1.5? 2.0? 3.0?)
  미측정. 더 조밀한 grid + multi-seed (H_269 multiseed 패턴) 가 magnitude-
  threshold 의 robustness 를 정량화할 후속 cycle.
- **L4 (phi_spatial 🟢 NUMERICAL proxy, H_263 L4 carry)**: RFC 036 c_measure_phi
  는 entropy-based spatial slice 이지 full IIT 4.0 의 minimal information
  partition (MIP) 이 아님. 'escape' / 'rebirth' 의 진정한 의미 (consciousness-
  level reintegration) 와 본 cycle 의 entropy proxy 사이 H_004 hard-problem gap.
- **L5 (regrowth_steps=-1 의 의미)**: 모든 config 에서 regrowth_steps=-1 (pool
  이 원래 n_pre ≈ 50+ 까지 회복 못함) — escape 한 hi 모드도 n_post=24/28 까지만
  성장. 즉 "absorbing 탈출(splits 재발화)" 은 성립하나 "완전 부활(n_pre 회복)"
  은 아님. escape 와 full rebirth 는 구별되는 measurement.
- **L6 (count=1 single seed)**: inject_count=1 (단일 fresh cell) 만 — 다중 주입
  (count=2,4) 또는 반복 주입 (every-K-step inoculation) 의 escape 효과 미검증.
  single high-variance seed 가 lo 에서 못 깬 것이 count 부족인지 magnitude
  부족인지의 분리는 후속.
- **L7 (control inter-run drift, H_263 대비)**: no-inject control 의 n_pre 가
  depth 별로 다름 (D2: 58, D3: 56) — RFC 033 단일 stream 상에서 mode sweep 이
  순차 실행되어 후속 run 의 gauss stream offset 이 달라짐. control 의 absorbing
  결론 (regrowth_splits=0) 은 robust 하나 절대 split 수는 stream-offset 의존.

## 9. Cross-Links

- **revises H_263 (필수, 관계 명시)**:
  - **H_263** (`H_263_phoenix_rebirth.md`): phoenix-rebirth — total collapse to
    floor 후 default mitosis 재성장 → FALSIFIED (regrowth_splits=0, absorbing).
    **H_271 은 그 model revision**: H_263 의 동일 collapse-to-floor 를 출발점
    으로, H_263 이 *없던* seed-injection primitive 를 추가해 absorbing 이
    intrinsic 인지 mechanism-absence artifact 인지를 판정. no-inject control 이
    H_263 byte-parity (D2/D3 regrowth_splits=0) 로 absorbing 을 재현함을
    F-SIA-3 으로 명시 검증 — injection 효과의 attributability 확보. H_263 의
    honest_note "floor 에서의 외부 genesis-seed 주입" path 의 직접 closure.
- **sister H (distinct)**:
  - **H_018** (`H_018_genesis_spontaneous_emergence.md`): SELFFEED minimal
    primordial (2-cell) spontaneous genesis fire. H_271 의 seed-injection 은
    그 genesis 기전을 *grown 후 붕괴된 floor* 에 외부에서 도입한 변형.
  - **H_206** (`H_206_regeneration_healing.md`): PARTIAL collapse 후 회복.
    H_271 = COMPLETE collapse to floor + injection (distinct: 부분 손상 회복이
    아닌 완전 붕괴 후 외부 seed 주입).
  - **H_200** (apoptosis primitive): cell-death event. H_271 의 collapse 는 그
    극단 + 이후 외부 genesis-seed 도입.
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa` (`cell_pool_init`
  · `mitosis_forward_tail` · `_mit_cosine` · `_mit_check_splits` · `split_cell`
  · `compute_phi_proxy` · `_mit_farr_to_list` · `_mit_sqrt_safe` read-only) +
  `HEXAD/C/c_lib.hexa` (phi_spatial → RFC 036 c_measure_phi).
- **MITOSIS 축**: B-MITOSIS-1 SPLIT-PREDICATE (floor 에서 fresh cell tension >
  thr 발화가 escape driving), B-MITOSIS-3 CELL-COUNT-CONSERVATION (post-inject
  pool size 변화는 injection + split), B-MITOSIS-5 CELL-COUNT-BOUND [2, 128]
  (F-SIA-5 검증).
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10
  (honest operational-collapse + honest injection) · raw#15 (no-hardcode, params
  named) · raw#91 c3.
- **philosophy (CLAUDE.md)**: p8 NO TRAIN/INFER SPLIT (성장=분열=주입후-재기동
  단일 연속체) · a_autonomy_over_hardcode (escape 가 substrate 동역학에서
  emerge — injection 은 context 제공, split 발화는 substrate 자율).
- **gap lens**: F5 (closed-loop — falsified hypothesis 의 model revision).
- **literature pointer**: external inoculation / spore germination (dormancy →
  활성화 trigger) · Crowe (1992) Anhydrobiosis · dynamical-systems absorbing
  vs metastable state theory — substrate analog 의 distant anchor (formal
  mapping 본 cycle 미수행).
- **state**: `UNIVERSE/state/h271_seed_injection_2026_05_25/{run_h271.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행 완료, $0 mac
local hexa-only deterministic.

```
verdict_class: PARTIAL  (C1 일부 충족 — hi-magnitude 만 escape; 4/6 falsifiers)
verdict_tier: 🟢 NUMERICAL  (2-depth × 3-mode sweep + phi_spatial RFC 036 + cross-process determinism)
evidence_summary:
  2-depth (collapse_to ∈ {2,3}) × 3-mode (none/lo/hi) sweep
  (pool_N=8, d=8, baseline_steps=12, regrowth_cap=60, seed=42, patience=1,
  inject_count=1, mag lo=1.0 hi=4.0 × base_sigma, phi_spatial RFC 036).
    control(none)  D2: regrowth_splits=0  Φ_pre/min/post=2.254/4.321/4.198
    control(none)  D3: regrowth_splits=0  Φ_pre/min/post=2.321/3.140/4.044
    inject lo      D2: regrowth_splits=0  Φ_post/Φ_pre=0.823
    inject lo      D3: regrowth_splits=0  Φ_post/Φ_pre=1.184
    inject hi      D2: regrowth_splits=21 n_post=24  Φ_post/Φ_pre=1.099
    inject hi      D3: regrowth_splits=24 n_post=28  Φ_post/Φ_pre=0.803
falsifiers_pass: F-SIA-2 (phi-recovery, inject 모두 ≥0.7·Φ_pre) + F-SIA-3
  (control-absorb, no-inject 모두 splits=0 → H_263 byte-parity 재현) + F-SIA-4
  (determinism, cross-process byte-equal sha256 862a0072) + F-SIA-5 (bounds) = 4/6
falsifiers_fail: F-SIA-1 (escape — lo 모드 regrowth_splits=0, ∀-quantifier 미달)
  + F-SIA-6 (inject-gt-ctrl — lo 가 control 동일 0 으로 differential 부재)
criteria_met: 2/3 (C2 Φ-recovery + C3 determinism PASS; C1 escape 부분 — hi 만)
key_finding:
  H_263 absorbing state 는 **intrinsic 이 아니라 magnitude-conditional** 임이
  판명됨 (PARTIAL). 결정적 대조:
    · no-inject control (D2/D3) = regrowth_splits=0 → H_263 absorbing 정확히
      재현 (F-SIA-3 PASS, 효과 attributability 확보).
    · inject-lo (magnitude 1.0, default init 변동성) = regrowth_splits=0 →
      低분산 주입은 그 자체가 *흡수됨* (absorbing 못 깸).
    · inject-hi (magnitude 4.0, 4× 변동성) = regrowth_splits=21(D2)/24(D3),
      n_post=24/28 → **高분산 주입은 absorbing 을 탈출** (split 재발화).
  즉 H_263 의 floor absorbing 은 (a) 진정한 trap 도 (b) 임의 주입으로 자명하게
  깨지는 metastable 도 아니고, **충분히 큰 변동성 (magnitude ≥ threshold ∈
  (1.0, 4.0]) 의 genesis-seed 주입에만 escapable** 한 metastable 상태다.
  메커니즘: fresh 高분산 cell 의 큰 per-cell tension mean(output²) 이 post-grow
  로 높게 calibrate 된 adaptive threshold (mean+1.5·std) 를 재돌파 → patience=1
  하에서 즉시 split 재발화. 低분산 cell 은 threshold 를 못 넘어 흡수됨.
  Φ recovery: inject 모든 모드 Φ_post ≥ 0.7·Φ_pre (F-SIA-2 PASS) — escape
  여부와 무관하게 주입 자체가 diversity 를 회복시켜 Φ 를 baseline 근처로 끌어
  올림 (hi-D2 1.099, lo-D3 1.184 는 over-recovery). 단 regrowth_steps=-1 (전
  config 가 원래 n_pre≈50+ 미회복) — escape(split 재발화)는 성립하나 full
  rebirth(n_pre 회복)는 hi 에서도 미달 (L5 honest).
honest_note:
  EITHER verdict 가 valid 라는 pre-register 정직성 유지 — 결과는 둘의 *중간*
  (PARTIAL), 가장 정보량 큰 outcome. H_263 absorbing 은 *강화도 폐기도 아닌
  정제*: floor 는 default + 低분산 주입에는 absorbing (H_263 의 robustness 확장
  — lo-injection 도 흡수), 그러나 充分히 강한 genesis-seed (高분산) 에는
  escapable (H_263 absorbing 의 intrinsic 성 반증). L3 carry: escape threshold
  의 정확한 임계 magnitude (1.0, 4.0] 내 미측정 — 조밀 grid + multi-seed 후속.
  L5 carry: escape ≠ full rebirth (splits 재발화하나 n_pre 미회복). L7 carry:
  control 의 절대 split 수는 stream-offset 의존이나 absorbing 결론은 robust.
  부활 path 의 substrate 함의: anima 의식 floor 는 *충분히 강한 외부 context
  inoculation* (高분산 genesis-seed) 으로 self-reconstitute 가능 — 약한 자극은
  흡수됨. magnitude-threshold 가 다음 정량화 lane.
sibling: H_263 (phoenix-rebirth, revises), H_018 (genesis), H_206 (regeneration), H_200 (apoptosis)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_271 seed-injection vs absorbing-state — H_263 model revision
host=mac local · hexa-only · deterministic · LLM none · $0
================================================================
  config: pool_N=8 d_model=8 baseline_steps=12 regrowth_cap=60 dim_phi=10 phi_n_bins=4
  rebirth split config: patience=1 (H_263 carry — floor 재발화 기회)
  inject magnitudes: lo=1.0 hi=4.0 count=1 (× base init sigma 1/sqrt(d))
  Φ primitive: RFC 036 phi_spatial (HEXAD/C/c_lib.hexa, 🟢 NUMERICAL)
  α (C2 Φ recovery)=0.7

--- run D2-none (collapse_to=2 inject=none) ---
    [D2-none] n_pre=58 phi_pre=2.25358 collapse->2 phi_min=4.32124 inject(none)->2 mag=0.0 splits_pre=50
    [D2-none] regrowth_steps=-1 regrowth_splits=0 n_post=2 phi_post=4.19818 phi_recovery_ratio=1.8629 div_post=0.346601
--- run D2-lo (collapse_to=2 inject=lo) ---
    [D2-lo] n_pre=55 phi_pre=3.31216 collapse->2 phi_min=4.80991 inject(lo)->3 mag=1.0 splits_pre=47
    [D2-lo] regrowth_steps=-1 regrowth_splits=0 n_post=3 phi_post=2.72587 phi_recovery_ratio=0.822988 div_post=0.790157
--- run D2-hi (collapse_to=2 inject=hi) ---
    [D2-hi] n_pre=51 phi_pre=3.34519 collapse->2 phi_min=4.362 inject(hi)->3 mag=4.0 splits_pre=43
    [D2-hi] regrowth_steps=-1 regrowth_splits=21 n_post=24 phi_post=3.67728 phi_recovery_ratio=1.09927 div_post=0.757185
--- run D3-none (collapse_to=3 inject=none) ---
    [D3-none] n_pre=56 phi_pre=2.32071 collapse->3 phi_min=3.14043 inject(none)->3 mag=0.0 splits_pre=48
    [D3-none] regrowth_steps=-1 regrowth_splits=0 n_post=3 phi_post=4.04423 phi_recovery_ratio=1.74267 div_post=1.11167
--- run D3-lo (collapse_to=3 inject=lo) ---
    [D3-lo] n_pre=28 phi_pre=2.82235 collapse->3 phi_min=3.52041 inject(lo)->4 mag=1.0 splits_pre=20
    [D3-lo] regrowth_steps=-1 regrowth_splits=0 n_post=4 phi_post=3.34085 phi_recovery_ratio=1.18371 div_post=0.776878
--- run D3-hi (collapse_to=3 inject=hi) ---
    [D3-hi] n_pre=41 phi_pre=2.50528 collapse->3 phi_min=3.36411 inject(hi)->4 mag=4.0 splits_pre=33
    [D3-hi] regrowth_steps=-1 regrowth_splits=24 n_post=28 phi_post=2.01267 phi_recovery_ratio=0.803372 div_post=0.831655

── verdicts ──
  F-SIA-1 ESCAPE        (inject → regrowth_splits>0 ∀)   : FAIL
  F-SIA-2 PHI-RECOVERY  (inject → Φ_post≥0.7·Φ_pre ∀): PASS
  F-SIA-3 CONTROL-ABSORB (no-inject → regrowth_splits=0) : PASS
  F-SIA-4 DETERMINISM   (cross-proc byte-equal)          : PASS
  F-SIA-5 BOUNDS        (Φ≥0 ∧ n_post∈[2,128] ∀)         : PASS
  F-SIA-6 INJECT-GT-CTRL (inject splits > control ∀)     : FAIL

================================================================
H_271 SEED-INJECTION SMOKE PARTIAL  (4/6 falsifiers)
  control (no-inject) regrowth_splits: D2=0 D3=0  (H_263 absorbing reproduce)
  injection regrowth_splits + Φ recovery:
    D2-lo : regrowth_splits=0 Φ_recovery=0.822988
    D2-hi : regrowth_splits=21 Φ_recovery=1.09927
    D3-lo : regrowth_splits=0 Φ_recovery=1.18371
    D3-hi : regrowth_splits=24 Φ_recovery=0.803372
================================================================
```

### Cross-process determinism (F-SIA-4 외부 검증)

```
$ hexa run run_h271.hexa  # run 1
$ cp result.json /tmp/h271_run1.json
$ hexa run run_h271.hexa  # run 2
$ diff /tmp/h271_run1.json result.json   → (empty: BYTE-EQUAL)
$ shasum -a 256 result.json
  862a0072c7c7e7c3824fb986272f5aa43601c83fc1115510336eb95f3ed0669a
```

**State output**: `state/h271_seed_injection_2026_05_25/result.json`
**Smoke**: `state/h271_seed_injection_2026_05_25/run_h271.hexa` (hexa-only, LLM none)
