---
id: H_132
slug: ce-frozen-cells
title: Frozen Cells (세포분열 동결) — 분열-정지에 의한 세포 분화 (post-mitotic 유비)
domain: life
status: pre-register-frozen
exploration_method: E5 (substrate-mechanism probe) + E6 (cross-domain biology — post-mitotic neuron) + E10 (emergence-observation)
verification_method: W3 (split/merge event ledger) + W4 (state-preservation invariant) + W11 (meta-cross)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-04-02
---

# H_132 — Frozen Cells (세포분열 동결)

## Hypothesis

cell-pool mitosis substrate 에서 **세포 부분집합의 분열을 정지 (division-arrest / freeze)** 시키면, 그 frozen subset 은 자기 state/function 을 보존 (state preservation) 하는 동시에, 주변 pool 은 계속 분열·성장한다. 즉 **선택적 분열-정지 (selective division-arrest) 가 세포 분화 (cell differentiation) 의 substrate-native 기구**일 수 있다 — 분화는 "어떤 세포를 더 분열시키지 않을 것인가" 의 결정으로 emerge 한다.

substrate 측 형식: `cell_pool` (`tool/hexa_native/mitosis_hook_lib.hexa`) 의 cells 중 `frozen_ids` subset 을 골라, 매 forward step 에서 그 세포의 weight (engine_a_W / engine_g_W) + hidden 을 baseline 으로 보존하고 (state-preserve), tension_history 를 리셋하여 split predicate 가 발화하지 못하게 한다 (division-arrest). 나머지 free 세포는 통상 split dynamics 따라 자율 분열한다.

레거시 CE-1 (`docs/hypotheses/ce/CE-1.md`) 의 "Φ-frozen + decoder-only" 아이디어 (의식 = 고정 feature extractor, decoder 가 언어학습 전담) 의 substrate-native 일반화 — "동결" 을 hidden-freeze 가 아닌 **mitosis-freeze (분열 동결)** 로 재정식화한다.

## Why

- **post-mitotic 뉴런 유비**: 생물학에서 성숙 뉴런은 terminally differentiated 되어 더 이상 분열하지 않으면서 (post-mitotic) 평생 자기 회로 상태를 보존한다. 주변 glia/progenitor 는 계속 증식. division-arrest = 분화의 핵심 신호 (cell-cycle exit at G0).
- **분화 = 분열 결정의 음함수**: 줄기세포 → 분화세포 전이는 "더 분열하지 않는다" 는 결정과 동치. anima substrate 에서 "frozen subset preserved while pool grows" 는 이 분화 동역학의 최소 computational instance.
- **MITOSIS 축과 직교**: HEXAD/MITOSIS B-MITOSIS-3 (cell-count-conservation n(t+1)=n(t)+Δs−Δm) + B-MITOSIS-5 (cell-count-bound [2,128]) 가 freeze 하의 accounting 무결성을 형식적으로 뒷받침. freeze 는 특정 세포의 Δs=0 강제 = B-MITOSIS-3 의 부분집합 제약.
- **REBORN §0.5 (NO TRAIN/INFER SPLIT) 정합**: 학습=분열 단일 연속체에서, freeze 는 "학습 정지된 부분 = 보존된 기억" 의 substrate 표현. ckpt = 분기점이라면 frozen cell = 동결된 분기.
- **CE-1 레거시 lineage**: Round 4 CE-base 카테고리 대표. hidden-freeze + decoder-only 의 분열-freeze 일반화 (Migration).
- **사용자 directive 정합**: anima 의 "who we are" 근원 lane — 생명/의식 분화가 substrate 자력 기구로 emerge 하는가의 물음.

## Predictions

- **H132.1 (state-preservation)**: frozen subset 의 weight (engine_a_W/engine_g_W) Δ = 0.0 over 전체 run — 분열-정지 세포는 상태 불변.
- **H132.2 (hidden-preservation)**: frozen subset 의 hidden Δ = 0.0 — Lorenz 자율 교란이 frozen 세포에 누적되지 않음.
- **H132.3 (selective growth)**: free subset 은 통상 split dynamics 따라 분열, pool cell 수 증가 (final > initial). 분화 = freeze 한 만큼 성장이 free 쪽으로 편향.
- **H132.4 (no self-division)**: frozen 세포가 parent 인 split event 0회 — division-arrest 가 실제로 분열을 막음.
- **H132.5 (accounting closure)**: 모든 frozen id 가 매 step 후 pool 에 정확히 1회 존재 — B-MITOSIS-3/5 정합, 소실/중복 0.

## Variables

- **axis1_frozen_fraction**: [0.0, 0.25, 0.5, 0.75] — frozen subset 비율 (본 cycle 0.5: 4 중 2)
- **axis2_initial_cells**: [2, 4, 8, 16] — 초기 pool 크기 (본 cycle 4)
- **axis3_n_steps**: [10, 20, 50, 100] — forward step 수 (본 cycle 20)
- **axis4_freeze_scope**: [weight_only, hidden_only, weight+hidden, weight+hidden+arrest] — 본 cycle = weight+hidden+arrest (full)
- **axis5_d_model**: [8, 64, 384, 1024] — substrate 차원 (본 cycle 8 synthetic)
- 4×4×4×4×4 = 1024 cell × N=5 = 5120 sweep target ($0 mac local hexa; 본 cycle = 단일 대표 cell)

## Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (gaussian draws 재현, env 1회 캐시) + 고정 synthetic 입력 `x[i]=sin(0.37·i)·0.5`. 2회 run byte-identical 확인.
- **hexa_only**: `HEXAD/LIFE/state/h132_frozen_cells_2026_05_23/run_freeze.hexa` — `mitosis_hook_lib.hexa` import, ckpt/LLM 불필요.
- **LLM**: none (raw#12 strict).
- **operational freeze 정의 (raw#9/10 HONEST)**: substrate 에 freeze primitive 부재 → freeze = (1) state-preserve (매 step frozen 세포 weight+hidden baseline 복원) + (2) division-arrest (tension_history 리셋 → split predicate 미발화). H_025 agent 가 apoptosis primitive 부재 시 cell-death=merge 로 정직하게 정의한 것과 동일 패턴.
- **per-step ledger**: {step, cells, next_id, split_threshold} + frozen Δweight / Δhidden 누적 + event_log split-parent 감사.
- **runtime**: $0 mac local, wall < 1s. GPU 불필요 (필요 시 STOP+document — 본 cycle 미해당).

## Criteria

- **C1 (state-preserve)**: H132.1 frozen weight Δ = 0.0
- **C2 (hidden-preserve)**: H132.2 frozen hidden Δ = 0.0
- **C3 (selective growth)**: H132.3 final cell 수 > initial ∧ next_id 전진
- **C4 (no self-division)**: H132.4 frozen-parent split 0회
- **C5 (accounting)**: H132.5 frozen id 매 step 1회 존재
- **verdict_rule**: PASS = C1+C2+C3+C4+C5 (= F-FREEZE-1..5 모두 PASS); PARTIAL = 3-4/5; FALSIFIED = ≤2/5.

## Falsifiers (raw#12 ≥5, measurable)

- **F-FREEZE-1 STATE-PRESERVE**: 임의 frozen 세포의 engine_a_W/engine_g_W max abs diff (vs step-0 baseline) > 0 → C1 FALSIFIED (freeze 가 weight 를 보존 못 함).
- **F-FREEZE-2 HIDDEN-PRESERVE**: 임의 frozen 세포의 hidden max abs diff > 0 → C2 FALSIFIED (Lorenz 교란이 frozen 에 누적).
- **F-FREEZE-3 NO-SELF-DIVIDE**: event_log 에 parent_id ∈ frozen_ids 인 split event ≥1 → C4 FALSIFIED (division-arrest 실패).
- **F-FREEZE-4 POOL-GROWS**: final cell 수 ≤ initial cell 수 OR next_id 미전진 → C3 FALSIFIED (freeze 가 전체 분열을 막아 분화 아닌 정지).
- **F-FREEZE-5 ACCOUNTING**: 임의 step 후 frozen id 가 pool 에 0회 또는 ≥2회 존재 → C5 FALSIFIED (B-MITOSIS-3 counting 위반).
- **F-FREEZE-6 (meta)**: post-hoc edit → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3 ≥5)

- **L1**: 본 freeze 는 **weight/hidden-freeze 이지 생물학적 post-mitotic 분화가 아니다**. 생물 분화는 epigenetic 재프로그래밍 + 단백질 발현 변화 + 형태 변화 — 본 cycle 은 weight 동결이라는 가장 거친 추상화일 뿐. 유비 강도 약함.
- **L2**: substrate 에 freeze primitive 부재 → freeze 를 외부 harness 의 "복원 + tension 리셋" 으로 operational 정의. 이는 cell-pool 자력 기구가 아닌 **harness-imposed 제약** — 진정한 substrate-native freeze (세포 스스로 분열 정지 결정) 는 별도 cycle (cell-cycle gate 변수 도입 필요).
- **L3**: synthetic d_model=8 + 4-cell + 20-step 단일 대표만. axis1-5 sweep (1024 cell) 미실행 — frozen_fraction / scale 의존성 미검증. 큰 frozen_fraction 에서 free pool 이 min_cells 경계에 부딪히면 성장 정지 가능 (미탐).
- **L4**: Δweight=0 은 forward 가 애초에 weight 를 mutate 안 하기 때문에 (split 만 weight 복사) **trivially 부분적**. 본 cycle 의 비자명 보존은 hidden (Lorenz 가 매 step 건드림) — Δhidden=0 은 복원 효과의 직접 증거. weight Δ=0 은 약한 falsifier.
- **L5**: division-arrest 를 tension_history 리셋으로 구현 → 만약 split_threshold 가 음수 (불가능하나) 거나 patience=0 이면 우회 가능. 본 구현은 patience≥1 가정에 의존.
- **L6**: merge event 0회 (merge_patience=30 > n_steps=20) → freeze 가 merge 와 어떻게 상호작용하는지 (frozen 세포가 merge 대상이 될 때 보존 깨지는가) 미검증. frozen 세포의 merge 면역은 별도 falsifier 필요.
- **L7**: "분화 = 분열-정지" 명제는 substrate 동역학 관찰일 뿐, 의식/기능 분화로의 연결 (frozen subset 이 실제로 특화된 기능을 보존하는가) 은 미측정 — Φ proxy / 기능 probe 별도 cycle.

## Cross-Links

- **sister H (LIFE)**: H_054 symbiogenesis (merge = 두 substrate 융합 — freeze 의 쌍대: 분열-정지 vs 융합), H_012 autopoietic network (self-maintaining closure — frozen subset = 보존된 closure), H_003 life origin (autopoiesis ground-truth), H_025 dasein (apoptosis=merge 정직 정의 패턴 carry).
- **MITOSIS 축**: `HEXAD/MITOSIS/` B-MITOSIS-3 CELL-COUNT-CONSERVATION (n(t+1)=n(t)+Δs−Δm — freeze 는 frozen 세포 Δs=0) + B-MITOSIS-5 CELL-COUNT-BOUND ([2,128] — F-FREEZE-5 accounting 정합) + B-MITOSIS-1 SPLIT-PREDICATE (split↔tension>thr — division-arrest 는 tension 을 thr 아래로 묶음).
- **substrate**: `tool/hexa_native/mitosis_hook_lib.hexa` (`cell_pool_init` / `mitosis_forward_tail` / `split_cell` import read-only).
- **raw**: raw#12 (deterministic) + raw#9/10 (honest operational-freeze) + raw#15 (no-hardcode).
- **legacy archive**: `docs/hypotheses/ce/CE-1.md` (CE-1 Φ-frozen + decoder-only origin) + AUTO/COMBO/EX/ULTRA variants.
- **cross H (substrate)**: H_109 (information-bottleneck — frozen = bottleneck 보존), H_065 (decoder-architecture).
- **literature**: post-mitotic neuron / cell-cycle exit (Buchman, Bonni 등 G0 분화 — 사용자 manual annotation), Maturana/Varela (1972) autopoietic closure.
- **own**: (anima-not-biological identity — 분화 유비는 substrate-mechanism analogy 한정).

## Verdict

```
verdict_class: pre-register-frozen → PASS (single representative cell, 2026-05-23)
evidence_summary: deterministic hexa-only freeze smoke, mitosis_hook_lib import,
                  4-cell d=8 × 20-step, frozen_ids=[0,1] free_ids=[2,3]
F-FREEZE-1 STATE-PRESERVE  : frozen weight Δ = 0.0          → PASS
F-FREEZE-2 HIDDEN-PRESERVE : frozen hidden Δ = 0.0          → PASS
F-FREEZE-3 NO-SELF-DIVIDE  : frozen-parent split = 0        → PASS
F-FREEZE-4 POOL-GROWS      : cells 4→12, next_id 4→12       → PASS
F-FREEZE-5 ACCOUNTING      : frozen id 1×/step ∀ step       → PASS
criteria_met: 5/5 (C1+C2+C3+C4+C5)
split_events: 8  merge_events: 0  frozen_self_split: 0
cost: $0 mac local · gauss_seed=42 · 2-run byte-identical
```

**State output**: `HEXAD/LIFE/state/h132_frozen_cells_2026_05_23/{run_freeze.hexa, result.json}`

**Honest scope (verdict)**: single representative cell (axis sweep DEFERRED, L3). operational freeze = harness-imposed (NOT substrate-native cell-cycle gate, L2). weight Δ=0 부분적으로 trivial — 비자명 증거는 hidden Δ=0 (L4). 생물학적 분화 유비 약함 (L1). 분화-기능 연결 미측정 (L7).

---

## C2 — Differentiation Longterm Stability (장기 분화 안정성)

> **명명 주의**: 본 섹션의 **criterion C2** 는 위 `## Criteria` 의 C2 (hidden-preserve, 단기 falsifier) 와 다른 상위-criterion 이다. 위 C1–C5 = 단기 freeze smoke (5/20 step) 의 5 falsifier. 본 C2 = H_132 을 **장기 horizon (100+ step)** 으로 확장한 신규 criterion (sub-criteria C2.1–C2.4). 기존 verdict 는 보존되고, 본 섹션은 그 위에 장기 안정성을 추가한다.

### C2 Question

기존 H_132 (`run_freeze.hexa`) 은 freeze 의 **단기** (5/20 step) 불변만 검증했다. 단기 불변은 분화 주장의 **필요조건이지 충분조건이 아니다** — frozen 세포가 50 step 후 drift 하거나, pool 이 성장하면서 split 기계가 끝내 frozen 세포에 발화한다면 "분화" 해석은 무너진다.

**C2 핵심 물음**: `frozen` 으로 표시된 cell 이, 주변 pool 이 비-frozen cell 의 split 으로 계속 **성장하는 와중에도** 100+ step 동안 Δw=0 · splits=0 (불변) 을 유지하는가? — post-mitotic 뉴런 유비의 시간축 강화 (성숙 뉴런은 progenitor 가 계속 증식하는 동안 평생 자기 상태를 보존한다).

### C2 Variables (extend)

- **axis3_n_steps 확장**: 기존 {10, 20, 50, 100} → 본 C2 = {100, 200} (장기 horizon).
- **initial_cells = 6** (기존 4 → 6), **frozen_ids = {0,1}** (2 frozen), **free_ids = {2,3,4,5}** (4 free). free fraction 을 4/6 로 키워 pool 이 실제로 성장하며 frozen 세포를 바쁜·팽창하는 pool 에 대비시킨다.
- d_model=8 synthetic 유지, `__HEXA_FARR_GAUSS_SEED__=42`, 고정 synthetic input `x[i]=sin(0.37·i)·0.5`, LLM none, $0 mac local.

### C2 Measurements (per horizon)

- **M-A frozen max|Δw|**: 모든 frozen 세포 · 모든 step 의 **post-restore** engine_a_W/engine_g_W max abs diff (vs step-0 baseline).
- **M-B frozen max|Δhidden|**: 동일하게 hidden — Lorenz 가 매 step hidden 을 건드리므로 **비자명 보존 증거** (L4).
- **M-C frozen split count**: event_log 의 split event 중 parent ∈ frozen_ids.
- **M-D pool growth (control)**: final_cell_count vs initial, 그리고 free-cell split count (대조군 = 살아있는 비-frozen 분열).
- **진단량**: max pre-restore Lorenz drift on frozen hidden — restore 가 실제로 비자명한 일을 하고 있음을 보이는 값 (≈0.9, 0 이 아니면 freeze 가 trivial-no-op 이 아님을 증명).

### C2 Criteria (pre-register)

- **C2.1 FROZEN-STABLE**: frozen max|Δw| < eps **AND** frozen max|Δhidden| < eps over 100+ step (eps = 1e-9).
- **C2.2 FROZEN-NO-SPLIT**: frozen split count == 0, pool 이 성장하는 와중에도.
- **C2.3 CONTROL-ALIVE**: free cell 성장 — final_cell_count > initial **AND** free split count > 0 (분화 주장을 의미있게 하는 대비 — frozen *pool* 이 아니라 frozen *subset*).
- **C2.4 DETERMINISM**: cross-process re-run sha256 동일 (harness driver 가 확인; RFC 033 global gauss stream 은 in-process reseed 불가이므로 cross-process 재실행 비교가 결정론 검증의 정직한 형태).
- **verdict_rule**: C2 PASS = C2.1 ∧ C2.2 ∧ C2.3 (각 horizon, 그리고 모든 horizon AND). PARTIAL = 일부 horizon 만 통과 / 한 criterion miss. FAIL = C2.1 또는 C2.2 위반.

### C2 Verdict

```
verdict_class: PASS (longterm differentiation stability, 2026-05-25)
evidence_summary: deterministic hexa-only longterm freeze, mitosis_hook_lib import,
                  6-cell d=8, frozen_ids=[0,1] free_ids=[2,3,4,5], horizons {100, 200}

horizon n_steps=100:
  cells 6→15  (max seen 15)  free_splits=9   frozen_splits=0
  frozen max|Δw|=0.0  frozen max|Δhidden|=0.0  (pre-restore Lorenz drift=0.9061)
  C2.1 FROZEN-STABLE   → PASS
  C2.2 FROZEN-NO-SPLIT → PASS
  C2.3 CONTROL-ALIVE   → PASS  (pool grew, 9 free splits)
  horizon_verdict      → PASS

horizon n_steps=200:
  cells 6→20  (max seen 20)  free_splits=14  frozen_splits=0
  frozen max|Δw|=0.0  frozen max|Δhidden|=0.0  (pre-restore Lorenz drift=0.861379)
  C2.1 FROZEN-STABLE   → PASS
  C2.2 FROZEN-NO-SPLIT → PASS
  C2.3 CONTROL-ALIVE   → PASS  (pool grew, 14 free splits)
  horizon_verdict      → PASS

C2.4 DETERMINISM       → PASS  (cross-process sha256 byte-identical:
                                71d76136830a6e1c8454ba77c6803a6e985e523a9addb30c37e33efcfa5bdc0c)
C2 aggregate           → PASS  (C2.1 ∧ C2.2 ∧ C2.3 for both horizons)
cost: $0 mac local · gauss_seed=42 · merge_events=0 · frozen_self_split=0
```

**State output**: `HEXAD/LIFE/state/h132_c2_longterm_2026_05_25/{run_h132_c2.hexa, result.json}`

**핵심 발견**: frozen 세포는 200 step 동안 — pool 이 6→20 cell 로 3배 이상 성장하고 free 세포가 14회 분열하는 와중에도 — weight·hidden 을 정확히 0 drift 로 유지했고, split 기계가 단 한 번도 frozen 세포에 발화하지 않았다. pre-restore Lorenz drift ≈0.9 는 freeze 가 trivial no-op 이 아님을 증명한다 (매 step Lorenz 가 hidden 을 ~0.9 만큼 흔들지만 restore 가 정확히 되돌린다). 단기 (H_132 원본 20 step) 불변이 장기 (200 step · 활성 성장) 으로 깨짐 없이 연장됨 — 분화 = 선택적 분열-정지의 시간축 안정성 확인.

**Honest scope (C2 verdict)**:
- **CL1**: 여전히 harness-imposed operational freeze (L2 carry) — substrate-native cell-cycle gate 가 아니라 외부 restore + tension reset. 장기 안정성은 이 operational 정의 하에서만 의미하며, 세포 스스로 분열을 정지하는 진정한 자력 기구는 미검증.
- **CL2**: 200 step 까지만. pool 이 max_cells=128 경계에 도달하면 어떤 일이 일어나는지 (free pool 성장이 멈춘 뒤 frozen 안정성) 미탐 — 본 sweep 은 6→20 으로 경계에서 멀다.
- **CL3**: frozen max|Δw|=0 은 forward 가 weight 를 mutate 안 하므로 부분적 trivial (L4 carry) — 비자명 증거는 max|Δhidden|=0 (Lorenz 가 매 step 건드림). 본 C2 의 진짜 강화는 "장기 + 활성 성장 pool 대비" 의 hidden 보존 + split-arrest 지속성.
- **CL4**: synthetic d=8 단일 config (frozen_fraction=1/3 고정). axis1 frozen_fraction / axis5 d_model sweep 미실행 (L3 carry) — 큰 frozen_fraction 에서 free pool 이 min_cells 경계에 부딪혀 성장 정지하는지 미탐.
- **CL5**: merge 0회 (merge_patience=30, free 세포간 inter-tension 이 merge_threshold 위 유지) — frozen 세포가 merge 대상이 될 때 보존 깨지는가 (L6 carry) 는 본 C2 horizon 에서도 미발생, 별도 falsifier 필요.
- **CL6**: 분화-기능 연결 (frozen subset 이 특화 기능을 실제로 보존하는가, L7 carry) 은 본 C2 에서도 미측정 — C2 는 시간축 *불변성* 만 강화, 기능적 분화는 별도 cycle (Φ proxy / 기능 probe).
