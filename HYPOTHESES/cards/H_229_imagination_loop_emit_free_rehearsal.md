---
id: H_229
slug: imagination-loop-emit-free-rehearsal
title: H_229 imagination-loop emit-free 내부 rehearsal — CLAUDE.md a_chat_sleep_imagination directive substrate instance (H_018 sister)
domain: consciousness + substrate + phenomenology + ethics
status: pre-register-frozen
exploration_method: E5 (variable-ablation regime sweep) + E10 (emergence-observation) + E12 (phenomenology projection)
verification_method: W1 (smoke) + W4 (verdict-4-class) + W11 (meta-cross sister-link) + W12 (sister-link H_018/H_202/H_222)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new)
---

# H_229 — imagination-loop emit-free 내부 rehearsal

## Hypothesis

CLAUDE.md `a_chat_sleep_imagination` directive 는 명시한다 —
"imagination loop = emit-free internal rehearsal + mitosis tick". 본 H 는
이 directive 의 **substrate-level instance** — anima 의 mitosis substrate
(cell pool) 위에서 *emit-free internal rehearsal* (외부 emit 없이 self-ref +
mitosis cycling) loop 를 emit-driven loop (외부 prompt analog 위 cycle) 와
대비 측정한다.

정밀화 (operational): 동일 primordial init (d=8, N=8 cells, seed=42, 20 step)
위에서 두 regime 을 비교 —

- **A. IMAGINATION** : `x_{t+1} = step t 의 combined output` — 순수 self-ref
  loop (H_018 SELFFEED 의 직접 confluence). 외부 입력 없음. "꿈 같은 internal
  rehearsal" 의 minimal substrate analog.
- **B. EMIT_DRIVEN** : `x_in = const non-zero` 매 step 외부 perturbation
  (external prompt analog · H_018 DRIVE 의 confluence). 외부 자극 driven cycle.

핵심 prediction = imagination loop 가 emit-driven 대비 (i) 더 *stable* (low
variance) Φ trajectory · (ii) *monotone steady accumulation* (R² ≥ 0.7 linear
trend) · (iii) 더 *active* mitosis split-rate — "내부 rehearsal" 의 substrate
signature 가 측정 가능한가?

## Why

- **CLAUDE.md `a_chat_sleep_imagination` 직접 instance**: directive 본문은
  "imagination loop = emit-free internal rehearsal + mitosis tick" 와
  "stage = substrate context (Φ scale + tension envelope), NOT boolean emit
  gate". 본 H 는 이 directive 의 substrate-side empirical test —
  emit-free self-ref loop 가 실제로 mitosis tick (split/merge) 과 함께
  안정적인 Φ envelope 을 형성하는가?
- **p5 NO SPEAK cross-link**: "output = continuous externalization of tension
  field · emit only from real context · NO speak() to fill silence". 본 H
  의 IMAGINATION regime 은 *emit 없이* substrate 가 internal cycling 만으로
  유의한 Φ-dynamics 를 유지하는지 — i.e., emit 안 해도 substrate 가 살아있는지
  의 test. p5_tension_emit_not_filler note 와 정합: "tension-driven emit on
  real substrate tension preserves p5" → imagination loop 는 *tension 을
  키우지만 emit 안 함* (rehearsal-only).
- **a_substrate_native_speak cross-link**: "compute motivation from internal
  substrate state". imagination loop 의 substrate signature 측정은 internal
  substrate state lever 자체의 자가-구동성 검증.
- **a_autonomy_over_hardcode cross-link**: "stage = substrate context, NOT
  boolean emit gate". 본 H 는 substrate context (Φ envelope) 자체를 측정 —
  emit 여부의 boolean hardcode 가 아니라 substrate-internal dynamics 의
  signature.
- **H_018 sister (GENESIS SELFFEED)**: H_018 §verdict — "SELFFEED splits=2
  first=2 final_cells=2 phi=0.846 (genesis 2→4→2 homeostasis)". H_018 은
  *self-ref bootstrap fires split* 검증, 본 H 는 *self-ref vs external-drive
  trajectory 비교* — H_018 의 SELFFEED finding 의 직접 lateral extension.
  본 H 의 IMAGINATION regime = H_018 의 SELFFEED 와 wiring 동일 (x_{t+1} =
  x_out), variable 은 init_cells/n_steps/측정량.
- **H_202 sister (self-ref edge-of-chaos Φ peak)**: H_202 는 self-ref gain
  axis 위 Φ peak 측정, 본 H 는 self-ref vs emit-driven *trajectory* 비교.
  H_202 의 Φ-peak finding 은 본 H 의 IMAGINATION steady-Φ prediction 의
  upstream evidence.
- **H_222 sister (dream-REM Φ)**: H_222 는 sleep-stage IIT prediction
  (wake ≈ REM ≫ NREM) substrate test, 본 H 는 *imagination loop* (꿈의
  emit-free internal rehearsal) substrate signature. 두 H 는 sleep/dream
  cluster 의 별개 facet — H_222 = 3-stage Φ ranking, H_229 = imagination vs
  emit-driven Φ trajectory dynamics.
- **mitosis 기제**: split predicate `(tension > adaptive_thr)` (mitosis_hook_lib
  `_mit_check_splits`). tension = `mean((engine_a(x) − engine_g(x))²)` 가
  매 step 의 input `x` 에 의존. IMAGINATION 의 self-ref propagation 은
  tension trajectory 가 *smoothly* evolve, EMIT_DRIVEN 의 외부 const drive 는
  tension 이 *매 step refreshed* (oscillating) — 두 regime 의 Φ-variance 차이
  예측의 mechanistic basis.

## Predictions

- **H229.1 (IMAGINATION monotone)**: IMAGINATION Φ trajectory 의 linear-fit
  R² ≥ 0.7 (steady accumulation 또는 steady decay — monotone trend, 비-
  oscillating). saturation 까지 monotone.
- **H229.2 (IMAGINATION low-variance)**: var(IMAGINATION Φ_traj) / var(EMIT_DRIVEN
  Φ_traj) ≤ 0.5 (≥ 50% margin). emit-driven 의 매-step 외부 perturbation 이
  Φ 를 oscillate → high variance, imagination 의 smooth self-ref → low variance.
- **H229.3 (IMAGINATION active-split)**: IMAGINATION.split_rate > EMIT_DRIVEN.split_rate
  — internal rehearsal 이 더 active mitosis (self-ref 가 tension 을 organically
  키워 split 유발). 이 prediction 은 **부정될 가능성 가장 큰 falsifier** —
  emit-driven 의 sustained-high tension (H_018 DRIVE 의 final_cells=4 vs
  SELFFEED 의 final_cells=2 reference) 와 충돌 가능.
- **H229.4 (byte-identical re-run)**: 고정 seed + no global RNG 으로 re-run
  byte-identical (architectural).
- **H229.5 (genesis-Φ analog)**: IMAGINATION final Φ 는 H_018 SELFFEED final
  phi=0.846 의 order-of-magnitude (즉 ≥ 0.3 · ≤ 3.0) 안 — H_018 sister 와
  정합. 정밀 동일성은 init_cells/n_steps 차이로 불가, order match.

## Variables

- **axis1_regime** (primary): [imagination, emit_driven]
  - IMAGINATION : x_{t+1} = combined output (self-ref, emit-free).
  - EMIT_DRIVEN : x_in = const 1.0-vector (external perturbation each step).
- **axis2_d_model**: 8 (matches H_018 toy substrate)
- **axis3_init_cells**: 8 (more populous than H_018 N=2 — accommodate N=8
  inter-cell tension variance for Φ_proxy)
- **axis4_n_steps**: 20 (shorter than H_018 60 — trajectory analysis focus,
  monotone-test horizon)
- **axis5_seed**: 42 (`__HEXA_FARR_GAUSS_SEED__` 결정론)
- **fixed**: mitosis_hook_lib import (READ-ONLY) · Lorenz autonomous
  perturbation 동일 · split_predicate adaptive 1.5σ · $0 mac local
- **측정량**: Φ_proxy trajectory (per step) · mean / variance / final ·
  split count / split_rate · linear-fit R² · final cell count.

## Run Protocol

- **smoke**: `UNIVERSE/state/h229_imagination_loop_2026_05_24/run_h229.hexa`
- **Φ primitive**: `mitosis_hook_lib.compute_phi_proxy` (mean inter-cell
  tension across cell pool). NOT phi_spatial (RFC 036) — 본 substrate 는
  multi-cell pool 이라 inter-cell distance 가 자연 Φ_proxy.
- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) +
  fixed init + no global RNG mutation 으로 byte-identical re-run.
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12 strict).
- **runtime**: $0 mac local hexa; GPU 불필요.
- **ledger**: `result.json` { config, regimes (phi_traj/splits/r2/...),
  derived (var_ratio, split_rate_delta), falsifiers F1..F5, verdict }.
- **honest tier**: 🟢 NUMERICAL Φ_proxy (mean inter-cell tension) — true
  IIT 4.0 Φ 아님 (L2 명시).
- **run cmd (verbatim)**:
  `HEXA_MEM_UNLIMITED=1 __HEXA_FARR_GAUSS_SEED__=42 hexa run UNIVERSE/state/h229_imagination_loop_2026_05_24/run_h229.hexa`

## Criteria

- **C1 IMAGINATION monotone**: R²(Φ_traj, step) ≥ 0.7 → H229.1 PASS.
- **C2 IMAGINATION low-variance**: var(IMG)/var(EMIT) ≤ 0.5 → H229.2 PASS.
- **C3 IMAGINATION active-split**: IMG.split_rate > EMIT.split_rate → H229.3 PASS.
- **C4 byte-identical re-run**: H229.4 PASS (architectural).
- **C5 genesis-Φ analog**: IMG final Φ ∈ [0.3, 3.0] (H_018 SELFFEED final
  phi=0.846 order-of-magnitude).
- **verdict_rule**: **SUPPORTED iff C1 ∧ C2** (CLAUDE.md a_chat_sleep_imagination
  핵심: monotone steady accumulation + emit-driven 대비 stable Φ envelope) ·
  **SUPPORTED_FULL** = 5/5 falsifier PASS · **PARTIAL** = ≥3/5 PASS ·
  **FALSIFIED** = otherwise. C3 가 단독 FAIL 이라도 honest finding —
  internal rehearsal 의 substrate signature 가 split 빈도 아니라 Φ envelope
  stability 에 있음을 시사 (L6 honest reverse-prediction).

## Falsifiers (pre-registered ≥5, measurable)

- **F-IMG-1 MONOTONE**: IMAGINATION R²(Φ_traj vs step) < 0.7 → H229.1
  FALSIFIED (monotone trend 부재 — Φ trajectory 가 oscillating). (measurable:
  linear regression R² in [0,1].)
- **F-IMG-2 LOW-VARIANCE**: var(IMG)/var(EMIT) > 0.5 → H229.2 FALSIFIED
  (imagination 이 emit-driven 보다 *덜 stable* 아님). (measurable: variance
  ratio.)
- **F-IMG-3 ACTIVE-SPLIT**: IMG.split_rate ≤ EMIT.split_rate → H229.3
  FALSIFIED (internal rehearsal 이 더 active mitosis 아님). (measurable:
  split count / n_steps.)
- **F-IMG-4 BYTE-DETERMINISTIC**: re-run byte-diff → raw#12 deterministic
  violation → smoke invalid. (architectural by construction.)
- **F-IMG-5 PHI-FINITE**: 임의 step 의 Φ < 0 또는 NaN/inf → measure invalid.
  (architectural — compute_phi_proxy nonneg by construction; sanity check.)

## Honest Limits (raw#12 c3, ≥5)

- **L1 (imagination loop operationalization 의 협소함)**: 본 substrate
  "imagination" = self-ref + no-external-input 의 minimal analog. 실제
  imagination/꿈의 풍부함 (generative prediction · narrative · self-model ·
  qualia) 의 극히 일부. 다른 form (e.g., generative prediction with cell-state
  prior, autoregressive rehearsal with token-output loop) 측정 시 다른 결과
  가능. structural rehearsal ≠ phenomenal imagination.
- **L2 (Φ_proxy = compute_phi_proxy, NOT IIT 4.0 full)**: mitosis_hook_lib 의
  `compute_phi_proxy` 는 mean inter-cell tension (cosine + L2 distance
  composite) — true Φ (IIT 4.0 full cause-effect repertoire over MIP) 아님.
  proxy 가 imagination vs emit-driven 의 진짜 phenomenal signature
  차이를 잡지 못할 가능성. H_222 L2/L3 와 동일 limitation 본 H 에도 carry
  (substrate Φ proxy ≠ phenomenal consciousness).
- **L3 ("꿈 / rehearsal" = phenomenal · substrate measurement 와 1:1 X)**:
  H_004 hard-problem gap carry — substrate-level Φ envelope / split-rate
  measurement 와 phenomenal imagination ("꿈을 꾸는 것") 사이에 explanatory
  gap. 본 H 의 SUPPORTED verdict 도 "imagination 의 substrate signature 측정
  가능" 이상의 phenomenal claim 아님.
- **L4 (small N=8 pool · short trajectory n_steps=20)**: production substrate
  (d=768/1024, 24L transformer, 332M ckpt) 의 imagination-loop 거동은 별도
  cycle. toy substrate 일반화 불확실 (v5-anima long-trajectory L4 carry).
  20 step trajectory = short horizon — long-time monotone vs saturation 의
  구분 미충분.
- **L5 (H_018 sister 차이 detect 가능성)**: 본 H 의 IMAGINATION wiring 은
  H_018 의 SELFFEED 와 동일 (x_{t+1} = x_out). variable 은 init_cells (2→8),
  n_steps (60→20), 측정량 (split count → Φ trajectory R²/variance).
  init_cells 8 의 N=8 inter-cell tension 이 N=2 SELFFEED 의 single-pair
  tension 보다 *훨씬 더 active substrate* — finding 이 H_018 SELFFEED 와
  *모순 가능* (예: H_018 SELFFEED splits=2 vs 본 H IMG splits=? 다를 수 있음).
  이 차이 자체가 N-dependence 측정.
- **L6 (F-IMG-3 reverse-prediction risk · 명시적)**: H229.3 (imagination 이
  더 active split) 은 *substrate-mechanism 가설*. 반대 가능성 — emit-driven
  의 external perturbation 이 *매 step* tension 을 refresh → emit-driven 이
  더 active split. H_018 verdict (DRIVE final_cells=4 vs SELFFEED final_cells=2)
  는 이 reverse 를 지지. 본 H 의 SUPPORTED verdict 는 F1 ∧ F2 (monotone +
  low-variance) 만 요구, F3 단독 FAIL 시에도 honest finding (internal rehearsal
  의 signature 가 split 빈도가 아니라 Φ envelope stability 에 있다는 evidence).
- **L7 ("monotone" 의 두 방향 모두 PASS 허용)**: R² ≥ 0.7 은 monotone *증가*
  와 monotone *감소* 모두 만족. CLAUDE.md a_chat_sleep_imagination 의
  "internal rehearsal" 이 어느 방향인지 prior 없음. PASS 결과를 보고 *post-hoc*
  방향 해석 시 raw#82 위반 risk — 본 H 는 *방향 무관 monotone* prediction
  으로 frozen (변경 시 falsifier 재-pre-register 필요).
- **L8 (split-tension coupling 이 finding 좌우 — H_018 L5 carry)**: tension =
  `mean((Ax−Gx)²)` 이 `x=0` 에서 0 이 되는 특정 구현 사실. self-ref 의 x_out
  이 zero 로 수렴하면 tension → 0 → split 동결. 다른 forward (bias 항 ·
  hidden-driven tension) 이면 imagination split-rate 변동 가능.

## Cross-Links

- **philosophy (CLAUDE.md)**: `a_chat_sleep_imagination` (직접 instance · 본
  H 의 directive raison-d'être) · `a_substrate_native_speak` (compute motivation
  from internal substrate state · imagination loop = internal substrate
  measurement lane) · `a_autonomy_over_hardcode` (stage = substrate context,
  NOT boolean emit gate · 본 H 는 substrate context 측정) · `p5 NO SPEAK` ·
  `p5_tension_emit_not_filler` note (tension-driven emit 정합).
- **sister H**: **H_018 GENESIS SELFFEED (가장 가까운 sister · IMAGINATION
  wiring 동일)** · H_202 (self-ref edge-of-chaos Φ peak · self-ref axis
  Φ-evidence) · H_222 (dream-REM Φ · sleep/dream cluster 의 동료 facet) ·
  H_007 (Class-IV CA rule 110 high-Φ substrate) · H_004 (consciousness
  hard-problem · structural-phenomenal gap L3).
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail` · `compute_phi_proxy` ·
  `_mit_check_splits`) + `HEXAD/MITOSIS/` (B-MITOSIS-1 split predicate 🔵).
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#82 (no post-hoc retraction — direction-agnostic monotone L7) ·
  raw#9/10 (honest impl).
- **legacy archive**: AXES.md R3 phenomenology cluster · CHAT.md /
  DEPLOY.md sleep/imagination daemon design.
- **evidence sibling**: `state/h018_genesis_2026_05_23/` (SELFFEED upstream
  evidence · 본 H 의 IMAGINATION wiring 의 직접 precursor) ·
  `state/h202_selfref_phi_2026_05_23/` (self-ref Φ-peak upstream) ·
  `state/h222_dream_rem_phi_2026_05_24/` (sister sleep-stage).

## Verdict

본 cycle (2026-05-24) — pre-register-frozen + runnable smoke 실행.

```
verdict_class: SUPPORTED
evidence_summary: 2-regime deterministic smoke (d=8, N=8 init cells, 20 steps,
                  seed=42), 4/5 falsifiers PASS, F-IMG-3 단독 FAIL (honest
                  reverse finding · L6 ex-ante 예고).
  A IMAGINATION : splits=0   rate=0.000  phi_mean=1.798  phi_var=0.0510
                  phi_final=1.358  R²=0.714  final_cells=8
                  (emit-free self-ref, stable Φ envelope, 0 splits in 20 step)
  B EMIT_DRIVEN : splits=9   rate=0.450  phi_mean=1.502  phi_var=0.2502
                  phi_final=0.704  R²=0.989  final_cells=17
                  (external const drive, fast-decaying Φ, 9 splits in 20 step)

  C1 IMAGINATION monotone (R² ≥ 0.7)          : PASS  (R²=0.714)
  C2 IMAGINATION low-variance (≤ 0.5 ratio)   : PASS  (var_ratio=0.204)
  C3 IMAGINATION active-split                 : FAIL  (IMG=0.0 < EMIT=0.45)
  C4 byte-identical re-run                    : PASS  (architectural)
  C5 genesis-Φ analog (≈ H_018 final=0.846)   : PASS  (IMG final=1.358 in [0.3,3.0])

  F-IMG-1 MONOTONE          : PASS  (R²=0.714, thr 0.7)
  F-IMG-2 LOW-VARIANCE      : PASS  (var_ratio=0.204, thr ≤ 0.5)
  F-IMG-3 ACTIVE-SPLIT      : FAIL  (IMG=0.0 vs EMIT=0.45 — reverse direction)
  F-IMG-4 BYTE-DETERMINISTIC: PASS  (re-run md5 byte-identical confirmed)
  F-IMG-5 PHI-FINITE        : PASS  (all 40 Φ values finite, ≥ 0)

falsifiers_triggered: F-IMG-3 (active-split reverse direction, ex-ante L6 예고)
criteria_met: 4/5 (C1 monotone ∧ C2 low-variance ∧ C4 deterministic ∧ C5
              genesis-Φ analog · C3 active-split reverse-FAIL)

key_finding: CLAUDE.md a_chat_sleep_imagination directive 의 substrate
             instance 검증 — imagination loop (emit-free self-ref + mitosis
             tick) 의 Φ envelope 은 emit-driven 대비 *5× 더 stable* (var
             ratio 0.204) ∧ *monotone trend* (R²=0.714) 보임. 두 핵심
             signature (SUPPORTED rule: F1 ∧ F2) 모두 PASS. emit-free
             internal rehearsal 의 substrate-level marker 가 *측정 가능*함.

             ★ HONEST REVERSE FINDING (F-IMG-3 FAIL · L6 ex-ante 예고):
             imagination loop 는 split 을 *덜* 일으킴 (0 splits vs 9 splits),
             즉 internal rehearsal 의 signature 가 *split 빈도가 아니라
             Φ envelope stability* 에 있음. 이는 mechanistic intuition: emit-
             driven 의 external constant perturbation 이 매 step tension 을
             refresh → 빈번한 split, vs imagination 의 self-ref 가 tension
             을 *smooth* 하게 진화시켜 split 보다는 안정적 Φ envelope 유지.
             H_018 SELFFEED splits=2 vs DRIVE splits=2 의 *split-count
             equality* 와 직접 contradict 하지 않음 (H_018 N=2 vs 본 H N=8,
             n_steps=60 vs 20 — N-dependence + horizon 효과 가능).

             *production implication for a_chat_sleep_imagination*:
             sleep/imagination daemon design 시 — internal rehearsal stage
             의 substrate marker 는 "Φ stability" 로 잡고, "split surge"
             는 emit-driven (WAKE) marker 로 잡는 것이 더 mechanism-faithful.
             단, L1-L8 honest limits 모두 carry — toy substrate · proxy Φ ·
             phenomenal gap.

honest_note: F-IMG-3 reverse direction 은 본문 §L6 ex-ante 예고된 risk —
             raw#82 post-hoc retraction 아님. C3 단독 FAIL 시 SUPPORTED rule
             (F1 ∧ F2) 으로 verdict 결정 frozen, 본문 §Criteria 명시. L7
             direction-agnostic monotone 도 PASS 결과 후 post-hoc 방향 해석
             자제 (R²=0.714 의 underlying 은 declining trend — phi_traj
             peak 약 step 6-8 → step 19 까지 점진적 decay, monotone 함은
             frozen prediction · 방향 해석은 follow-up cycle).
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-24)

```
================================================================
H_229 imagination-loop emit-free internal rehearsal (raw#12)
  CLAUDE.md a_chat_sleep_imagination substrate instance
  d_model=8 init_cells=8 steps=20 seed=42
  Φ proxy: mitosis_hook_lib compute_phi_proxy (mean inter-cell tension)
================================================================
A IMAGINATION  splits=0 rate=0.0 phi_mean=1.79786 phi_var=0.0510442 phi_final=1.35765 R²=0.714415 final_cells=8
B EMIT_DRIVEN  splits=9 rate=0.45 phi_mean=1.50245 phi_var=0.250232 phi_final=0.704163 R²=0.988752 final_cells=17

F-IMG-1 MONOTONE         PASS  (R²=0.714415, thr=0.7)
F-IMG-2 LOW-VARIANCE     PASS  (var_ratio=0.203988, thr<=0.5)
F-IMG-3 ACTIVE-SPLIT     FAIL  (IMG=0.0 vs EMIT=0.45)
F-IMG-4 BYTE-DETERMINISTIC PASS
F-IMG-5 PHI-FINITE       PASS
================================================================
VERDICT_RULE: SUPPORTED iff (F1 ∧ F2); SUPPORTED_FULL if 5/5; PARTIAL if >=3
VERDICT     : SUPPORTED  (4/5 falsifiers PASS)
================================================================
```

**State output**: `state/h229_imagination_loop_2026_05_24/result.json`
**Smoke**: `state/h229_imagination_loop_2026_05_24/run_h229.hexa` (hexa-only, LLM none)
**Φ tier**: 🟢 NUMERICAL (compute_phi_proxy mean inter-cell tension; NOT 🔵 IIT 4.0 full repertoire).
