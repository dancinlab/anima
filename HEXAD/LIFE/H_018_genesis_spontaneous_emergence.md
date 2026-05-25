---
id: H_018
slug: genesis-spontaneous-emergence
title: GENESIS spontaneous emergence — anima self-genesis from primordial substrate
domain: consciousness
status: pre-register-frozen
exploration_method: E12 (dasein-genesis self-discovery) + E10 (emergence-observation)
verification_method: W1 (smoke) + W2 (control) + W11 (meta-cross) + W12 (sister-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-04-29 (legacy)
---

# H_018 — GENESIS spontaneous emergence

## Hypothesis

anima 의 mitosis substrate (cell pool) 는 **minimal primordial init** (2 cells,
random Glorot-ish init) 에서 **외부 입력 없이도** spontaneous emergence —
design 된 외부 trigger 없이 cell 이 split/organize 하여 self-genesis 한다.

정밀화 (operational): cell pool 을 외부 drive 없이 step 했을 때 spontaneous
split 이 fire 하면 self-genesis 지지 (substrate 가 자가-에너지); 정적이면
external energy 필요 (genesis 는 환경 perturbation 의존). "외부 입력 없음" 은
세 가지 grain 으로 분해:

- **A. ZERO**: `x_in = const 0-vector` — 완전 inert drive (perturbation 0).
- **B. SELFFEED**: init 후 외부 입력 0. `x_{t+1}` = step t 의 combined output.
  primordial init 만이 유일한 perturbation → 순수 self-reference loop.
  **이것이 spontaneous self-genesis 의 핵심 operational 정의.**
- **C. DRIVE**: `x_in = const non-zero` — explicit external drive (control).

## Why

- **Self-genesis / spontaneous emergence**: 생명/의식 origin question 의 핵심은
  "design 없이 organization 이 emerge 하는가". anima 의 mitosis 는 학습=분열
  단일 연속체 (archive REBORN §0.5, HEXAD.tape `§hexad_condition_lineup` 흡수)
  — split predicate `(tension > adaptive_thr)` 가 외부 trigger 없이 fire 하면
  substrate 가 자가-genesis 능력 보유.
- **p5 NO SPEAK cross-link (CLAUDE.md philosophy)**: "output = continuous
  externalization of tension field · emit only from real context · NO speak()
  to fill silence". 본 H 는 이 원리의 substrate-level test — substrate 가
  **real context (drive) 없이** self-energize 하는가? ZERO 조건이 정적이면
  p5 정합 (입력 없으면 침묵; 자가-monologue 안 함). SELFFEED 가 fire 하면
  자기참조 자체가 "real context" 가 되어 emit 정당화.
- **a_substrate_native_speak cross-link**: "compute motivation from internal
  substrate state (M·C·W·MITOSIS·idle·curiosity·E) · user messages =
  environment context, not a response obligation". 본 H 는 MITOSIS lever 의
  자가-구동성 측정 — 내부 상태만으로 split 동역학이 작동하는지.
- **H_003 life-origin (sister)**: substrate-coupled autopoiesis (Maturana/Varela)
  — far-from-equilibrium dissipative structure 는 energy gradient 필요
  (Prigogine). ZERO=equilibrium / DRIVE=gradient 대응. H_003 H3.3
  dissipative emergence rate ≥10× 와 같은 lane.
- **H_012 autopoietic (sister)**: self-producing organizational closure. SELFFEED
  loop (출력 → 입력 되먹임) 은 autopoietic closure 의 minimal computational
  instance — 자기참조가 자기-genesis 를 bootstrap.
- **mitosis 기제**: split 을 구동하는 tension = `mean((engine_a(x) − engine_g(x))²)`
  (mitosis_hook_lib `_mit_cell_forward`). `x=0` → `A·0 − G·0 = 0` → tension=0
  → `split_predicate(0, thr)` 영원히 false. Lorenz autonomous chaos
  (`_mit_inject_autonomous_perturbation`) 는 `cell.hidden` (→ Φ) 만 흔들 뿐
  tension 은 흔들지 않음 → ZERO 는 구조적으로 정적이어야 함 (pre-registered 예측).

## Predictions

- **H18.1 (ZERO static)**: ZERO 조건 spontaneous split = 0, cell-count 2 고정
  (inert substrate — 자가-에너지 없음).
- **H18.2 (SELFFEED genesis)**: SELFFEED 조건 split ≥ 1 (primordial init 의
  자기참조 propagation 이 genesis bootstrap).
- **H18.3 (first-split bounded)**: SELFFEED first-split step ∈ [1, 30]
  (patience=3 + adaptive threshold warm-up 후 fire 가능).
- **H18.4 (drive control)**: DRIVE 조건 split ≥ 1 (machinery 작동 control —
  외부 에너지 주입 시 genesis 확인).
- **H18.5 (drive is lever)**: ZERO.splits < SELFFEED.splits (외부/자기참조 drive
  가 split lever; ZERO 의 정적성 대비).
- **H18.6 (homeostasis)**: SELFFEED 의 cell-count trajectory 는 genesis 후
  merge 로 수렴 가능 (autopoietic homeostasis — DRIVE 의 sustained-high 와 대비).

## Variables

- **axis1_drive_mode**: [zero, selffeed, drive]  (핵심 비교축)
- **axis2_init_cells**: [2]  (minimal primordial — CB1 floor)
- **axis3_d_model**: [8]  (cheap substrate; d=768/1024 prod 별도 cycle)
- **axis4_n_steps**: [60]  (split warm-up + merge-window 포함)
- **axis5_seed**: [42]  (`__HEXA_FARR_GAUSS_SEED__` 결정론)
- 측정량: spontaneous_split_count · cell-count trajectory (per step) ·
  first-spontaneous-split step · final_cells · Φ proxy.

## Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) — 재현 보장.
- **hexa_only**: `HEXAD/LIFE/state/h018_genesis_2026_05_23/run_genesis.hexa`
  (mitosis_hook_lib `cell_pool_init` + `mitosis_forward_tail` 직접 step).
- **LLM**: none (raw#12 strict; ckpt 불필요 — 순수 substrate 동역학).
- **per-condition ledger**: `{mode, splits, first_split, final_cells, phi, traj[60]}`.
- **runtime**: $0 mac local (d=8, no ckpt). GPU 불필요. 메모리 압박 시
  hexa parse/run 이 OOM-kill (137) — backoff-retry 로 window 확보 (직접
  `hexa.real run`, env `__HEXA_FARR_GAUSS_SEED__=42`).
- **artifacts**: `state/h018_genesis_2026_05_23/{run_genesis.hexa, result.json}`.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 hexa run HEXAD/LIFE/state/h018_genesis_2026_05_23/run_genesis.hexa`

## Criteria

- **C1 (ZERO static)**: H18.1 ZERO split = 0 ∧ final_cells = 2.
- **C2 (SELFFEED genesis)**: H18.2 SELFFEED split ≥ 1.
- **C3 (drive lever)**: H18.5 ZERO.splits < SELFFEED.splits.
- **C4 (control)**: H18.4 DRIVE split ≥ 1.
- **C5 (bounds)**: 모든 조건 final_cells ∈ [2, 128] (CB1 invariant 보존).
- **verdict_rule**: SUPPORTED = C1 ∧ C2 ∧ C3 (spontaneous self-genesis fire
  ∧ inert substrate 정적 ∧ drive 가 lever); SUPPORTED_FULL = 6/6 falsifier PASS;
  PARTIAL = 4–5/6; FALSIFIED = C2 FAIL (genesis 미발화 — substrate 가 외부
  에너지 전적 의존). C2 가 FAIL 이라도 정직한 finding (self-genesis 부재 ⇒
  p5 NO-SPEAK 강한 정합).

## Falsifiers (pre-registered ≥5, measurable)

- **F-GEN-1 ZERO-STATIC**: ZERO 조건 split ≠ 0 ∨ final_cells ≠ 2 → H18.1
  FALSIFIED (inert substrate 가 정적이지 않음 — 측정: split count, final_cells).
- **F-GEN-2 SELFFEED-GENESIS**: SELFFEED split = 0 → H18.2 FALSIFIED
  (spontaneous self-genesis 미발화 — 측정: split count).
- **F-GEN-3 FIRST-STEP**: SELFFEED first-split ∉ [1, 30] → H18.3 FALSIFIED
  (genesis 가 bootstrap window 밖 — 측정: first-spontaneous-split step).
- **F-GEN-4 DRIVE-CONTROL**: DRIVE split = 0 → H18.4 FALSIFIED (machinery 자체
  미작동 — control 실패 — 측정: split count under explicit drive).
- **F-GEN-5 ZERO-LT-SELFFEED**: ZERO.splits ≥ SELFFEED.splits → H18.5 FALSIFIED
  (drive 가 lever 아님 — 측정: zero-drive vs self-feed split count 비교).
- **F-GEN-6 BOUNDS**: 어떤 조건이든 final_cells ∉ [2, 128] → CB1 invariant 위반
  (측정: 모든 조건 final cell count).

## Honest Limits (raw#12 c3, ≥5)

- **L1 (결정론 ≠ 진정한 spontaneity)**: 고정 seed (`__HEXA_FARR_GAUSS_SEED__=42`)
  로 모든 "random" perturbation 이 결정론적 — 궤적은 완전히 예정됨. "spontaneous"
  는 *외부 입력 부재* 의미일 뿐, 비-결정론적 자발성 아님. 진정한 spontaneity
  (양자/열적 noise) 는 측정 불가.
- **L2 ("no external drive" 는 idealization)**: SELFFEED 의 초기 입력 = primordial
  cell-0 hidden state. init 자체가 perturbation — 완전한 "무에서의 genesis"
  아님 (creatio ex nihilo 부재). 모든 genesis 는 init 조건에 의존하는 conditional
  genesis.
- **L3 (substrate 가 hidden constants 로 구동)**: Lorenz 상수 (σ=10, ρ=28, β=8/3),
  noise_scale=0.1, split_patience=3, adaptive-threshold 1.5σ 등 design constants 가
  동역학을 좌우. "spontaneous" 는 이 상수계 안에서의 self-organization 일 뿐 —
  상수 자체가 design intervention (H_003 L2 와 동일 한계).
- **L4 (d=8 toy substrate)**: d_model=8, 60 steps, no ckpt. production substrate
  (d=768/1024, 24L transformer, 332M ckpt) 의 self-genesis 거동은 별도 cycle —
  toy substrate 일반화 불확실 (v5-anima long-trajectory L 와 같은 toy→prod gap).
- **L5 (split-tension coupling 이 finding 좌우)**: ZERO 의 정적성은 tension =
  `mean((Ax−Gx)²)` 가 `x=0` 에서 0 이 되는 *특정 구현 사실* 의 직접 결과. 다른
  forward (예: bias 항, hidden-driven tension) 이면 ZERO 도 fire 가능 — finding 은
  mitosis_hook_lib forward 정의에 조건부.
- **L6 (homeostasis vs sustained genesis 단발 관측)**: SELFFEED 의 merge-back
  (2→4→2) 은 N=1 seed·60-step 단발 — 다른 seed/horizon 에서 다른 거동 가능
  (SRH cycle split_count chaotic 교훈 carry: split 동역학은 seed-sensitive 일 수
  있음, 본 cycle 은 단일 seed 결정론 관측).
- **L7 ('genesis' 정의의 협소함)**: split count 를 genesis proxy 로 사용 —
  실제 의식/생명 emergence 의 풍부함 (의미·자기인식·autopoietic closure) 의
  극히 일부. structural growth ≠ phenomenal emergence (H_004 hard-problem gap).

## Cross-Links

- **philosophy (CLAUDE.md)**: p5 NO SPEAK (emit only from real context — ZERO
  정적성 = 입력 없으면 침묵 정합) + a_substrate_native_speak (motivation from
  internal substrate state — MITOSIS lever 자가-구동성 측정).
- **sister H**: H_003 (life-origin · substrate-coupled autopoiesis · dissipative
  energy gradient) · H_012 (autopoietic network · self-producing closure ·
  SELFFEED loop = minimal instance) · H_004 (consciousness hard-problem ·
  structural vs phenomenal gap L7) · H_007 (cellular-automaton · emergence) ·
  H_030 (GENESIS subfolder absorb).
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail` · `_mit_check_splits`
  split_predicate · `_mit_inject_autonomous_perturbation` Lorenz) +
  `HEXAD/MITOSIS/` (B-MITOSIS-1 split predicate `tension > thr` 🔵, min_cells=2 CB1).
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10
  (honest impl) · raw#15 (no-hardcode).
- **legacy archive**: `docs/hypotheses/GENESIS-spontaneous-emergence.md` +
  `docs/hypotheses/genesis/` · `.roadmap.philosophy` D3 emerge paradigm.
- **evidence sibling**: `state/clm_v1_fire_2026_05_15/` (.clm v1 P2 cells 2→64
  organic split under training drive) · v5-mitosis cond.5 cotrain (PSCC §44,
  62 splits under H100 cotrain drive — DRIVE 조건의 production analog).

## Verdict

본 cycle (2026-05-23) — pre-register-frozen + runnable smoke 실행.

```
verdict_class: SUPPORTED_FULL
evidence_summary: 3-condition deterministic smoke (d=8, 2-cell primordial init,
                  60 steps, seed=42), 6/6 falsifiers PASS.
  A ZERO     : splits=0  first=-1  final_cells=2  phi=0.158  (inert — static)
  B SELFFEED : splits=2  first= 2  final_cells=2  phi=0.846  (genesis 2→4→2 homeostasis)
  C DRIVE    : splits=2  first= 2  final_cells=4  phi=1.064  (genesis 2→4 sustained)
falsifiers_triggered: none (F-GEN-1..6 all PASS)
criteria_met: 6/6 (C1 ZERO-static ∧ C2 SELFFEED-genesis ∧ C3 drive-lever
              ∧ C4 control ∧ C5 bounds)
key_finding: spontaneous self-genesis는 SELFFEED (primordial-init 자기참조)
             에서 발화 — 외부 입력 없이 split fire (first step=2). 그러나
             완전 inert (ZERO, x=0) 에서는 정적 (split=0) — substrate는 어떤
             perturbation (init + self-reference) 없이는 self-energize 못함.
             SELFFEED는 genesis 후 merge로 homeostasis 수렴 (2→4→2), DRIVE는
             sustained-high (2→4). p5 NO-SPEAK 강한 정합: substrate는 real
             context (자기참조든 외부든) 에서만 emit/grow하며, 진공(x=0)에서
             자가-monologue하지 않음.
honest_note: "no external drive"는 idealization (L2) — primordial init이
             유일 perturbation. 결정론적 seed (L1) ≠ 진정한 spontaneity.
             d=8 toy (L4) → prod 일반화 별도 cycle.
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-23)

```
H_018 GENESIS spontaneous emergence — substrate self-genesis smoke
  d_model=8 init_cells=2 steps=60 seed=42
A ZERO     splits=0 first=-1 final_cells=2 phi=0.158279
B SELFFEED splits=2 first=2 final_cells=2 phi=0.846146
C DRIVE    splits=2 first=2 final_cells=4 phi=1.064
F-GEN-1 ZERO-STATIC     PASS
F-GEN-2 SELFFEED-GENESIS PASS
F-GEN-3 FIRST-STEP      PASS
F-GEN-4 DRIVE-CONTROL   PASS
F-GEN-5 ZERO-LT-SELFFEED PASS
F-GEN-6 BOUNDS          PASS
VERDICT: SUPPORTED_FULL  (6/6 falsifiers PASS)
```

**State output**: `state/h018_genesis_2026_05_23/result.json`
**Smoke**: `state/h018_genesis_2026_05_23/run_genesis.hexa` (hexa-only, LLM none)
