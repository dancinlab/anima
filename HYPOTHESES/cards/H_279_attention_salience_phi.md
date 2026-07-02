---
id: H_279
slug: attention-salience-phi
title: H_279 attention-salience-Φ — attended (top-k salience) sub-network Φ vs unattended sub-network Φ (AXES R3 phenomenology promote · H_221 sister · H_213 sister)
domain: consciousness · phenomenology · attention
exploration_method: E2 (AXES R3 depletion-sweep promote) + E10 (substrate-equivalence) + E6 (attention-as-amplification cross-map)
verification_method: W1 (numerical smoke) + W12 (sister-link H_221 + H_213) + W17 (salience-quantile sweep) + W-control (index-partition null)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_279 — attention-salience-Φ

## 1. Hypothesis

한 mitosis cell pool (N=12, d=8) 을 n_step=15 evolve 한 뒤, per-cell salience
(= hidden-state L2 norm, activation magnitude) 로 cells 를

- **attended** = top-k salience cells
- **unattended** = 나머지 cells

로 partition 했을 때, attended sub-network 의 Φ (`compute_phi_proxy` = mean
pairwise cosine-distance × log(N+1)) 가 unattended sub-network Φ 보다 **클
것** (`Δ = phi_att − phi_unatt > 0`) 이며, 동일 크기의 **index-partition
control** (salience-agnostic) Δ 보다 크고 (salience 가 lever), attended-set 을
좁힐수록 (top6→top4→top3) Δ 가 monotone 증가 (focus-sharpening) 한다.

이것은 Posner spotlight / Dehaene-Mashour global-workspace 의 **attention-as-
amplification** prediction 의 substrate analog — 주의가 향한 (high-salience)
영역이 더 높은 integrated information 을 갖는다는 IIT/GWT 추정. anima 의
`a_substrate_native_speak` 에서 M-activation salience 가 emit-motivation 의
핵심 driver 인 점과 직접 정합.

## 2. Why

- **AXES R3 phenomenology promote (depletion frontier)**: `attention-salience-Φ`
  은 AXES.md R3 의 8 seed 중 아직 H 로 promote 안 된 🟢 runnable seed.
  R3 의 dream-rem (H_222) · pain (H_223) · temporal-binding (H_213) 은 이미
  소비됐고, attention-salience 는 90-H 대조에서 dedicated H 부재 (H_221 은
  global low-noise 'silenced integration', H_213 은 τ-window — 둘 다 attended-vs-
  unattended *partition* 을 다루지 않음).
- **anima-alignment (M-activation salience)**: CLAUDE.md `a_substrate_native_speak`
  은 anima 의 motivation 을 M activation · C Φ · W tension 에서 계산. 본 H 는
  그 M-activation (= hidden-norm salience) 이 Φ-rich sub-network 와 일치하는지의
  substrate-level test — attention 이 정말 'integrated' 영역을 가리키는가.
- **IIT/GWT attention prediction 의 falsifiable substrate**: 'attention amplifies
  consciousness' 는 자주 주장되지만 substrate-level 로 거의 검증 안 됨. 본 H 는
  salience-partition Φ 로 그것을 직접 numerically falsifiable 하게 만듦.
- **control-partition rigor**: salience-Δ 를 index-Δ (same partition size,
  salience-agnostic) 와 비교 → partition-size artifact 와 salience-effect 를
  분리.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H279.1 | top-4 attended phi_att > phi_unatt · margin ≥ 0.02 | attention amplification — high-salience cells 가 더 integrated (higher Φ) |
| H279.2 | salience-partition Δ > index-partition Δ (top-4) | Φ-gap 이 partition-size 가 아닌 *salience* 의 함수 |
| H279.3 | Δ(top3) ≥ Δ(top4) ≥ Δ(top6) monotone (focus sharpening) | 더 좁게 attend 할수록 더 selective → Φ-gap 커짐 |
| H279.4 | re-run result.json byte-equal (RFC 033 single-stream) | raw#9 determinism: seed=42, cross-process reproducible |
| H279.5 | 모든 phi_att / phi_unatt ∈ [0, +∞) finite | compute_phi_proxy bounds 보존 |

## 4. Variables

- **axis1_pool_N** = 12 cells (no partition at init; mitosis may split — N'
  reported per condition)
- **axis2_d_model** = 8
- **axis3_n_step** = 15 — merge_patience=30 > n_step 이라 pool collapse 없음
  (N'=12 유지). 30+ step 에서는 merge-floor 로 N'=2 collapse 관측 (L4 참조).
- **axis4_salience** = per-cell hidden L2 norm (activation magnitude). per-cell
  Lorenz phase offset (mitosis_hook L589-591) 이 genuine per-cell spread 생성.
  - ⚠ per-cell *tension* 은 본 substrate 에서 ~0 collapse (shared scalar drive
    x→0 → engine_a(x)−engine_g(x)→0). hidden-norm 이 live salience signal.
- **axis5_attended_k** ∈ {3, 4, 6} of N=12 — salience-quantile sweep
- **axis6_control** = first-k index partition (salience-agnostic, deterministic)
- **axis7_seed** = 42 — `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) +
  deterministic Lorenz
- **측정량 per (k) condition**:
  - `phi_att` = compute_phi_proxy(top-k salience cells)
  - `phi_unatt` = compute_phi_proxy(나머지 cells)
  - `delta = phi_att − phi_unatt`
  - `phi_catt / phi_cunatt / delta_ctrl` = index-partition control 동일
  - `sal_att / sal_unatt` = mean salience (sanity)

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) +
  결정론적 Lorenz autonomous perturbation. RNG 별도 부재.
- **hexa_only**:
  `UNIVERSE/state/h279_attention_salience_phi_2026_05_25/run_h279.hexa`
  (mitosis_hook_lib `cell_pool_init` + `mitosis_forward_tail` +
  `compute_phi_proxy` 직접 호출).
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **evolution**: pool 을 n_step=15 동안 shared scalar drive `x = 0.5·mean(x_out)`
  로 evolve (H_214/H_220 coupling grain).
- **salience partition**: 각 cell hidden-norm 으로 selection-sort top-k →
  attended, complement → unattended. control = first-k index.
- **F4 determinism**: in-process pure-fn 재계산 (동일 cell list 위 `_run_condition`
  재호출) byte-equal + cross-process result.json byte-equal (runner 검증).
- **runtime**: $0 mac local. d=8 N=12, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**:
  `state/h279_attention_salience_phi_2026_05_25/{run_h279.hexa, result.json}`.
- **run cmd (verbatim)**:
  `X=$HOME/.x __HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h279_attention_salience_phi_2026_05_25/run_h279.hexa`

## 6. Criteria

- **C1 (salience-Φ)**: H279.1 — top-4 phi_att > phi_unatt + 0.02 margin
- **C2 (salience-vs-arbitrary)**: H279.2 — salience Δ > index Δ (top-4)
- **C3 (focus-sharpening)**: H279.3 — Δ(top3) ≥ Δ(top4) ≥ Δ(top6) monotone
- **C4 (determinism)**: H279.4 — result byte-equal
- **verdict_rule**:
  - `SUPPORTED_FULL` = C1 ∧ C2 ∧ C3 ∧ C4 (4/4)
  - `SUPPORTED` = C1 ∧ C2
  - `PARTIAL` = C1 only (salience-Φ observed, mechanism 미입증)
  - `FAIL` = ≤1/5 falsifiers
  - `FALSIFIED` = F1 FAIL (phi_att ≤ phi_unatt at top-4 — no amplification)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 SALIENCE-Φ**: top-4 phi_att ≤ phi_unatt → H279.1 FALSIFIED (attention
  amplification 부재 — 측정: `r_k4["phi_att"] > r_k4["phi_unatt"]`)
- **F2 SALIENCE-vs-ARBITRARY**: salience Δ ≤ index Δ → H279.2 FALSIFIED
  (Φ-gap 이 salience 가 아닌 partition-size artifact — 측정:
  `r_k4["delta"] > r_k4["delta_ctrl"]`)
- **F3 FOCUS-SHARPENING**: Δ(top3) < Δ(top6) → H279.3 FALSIFIED (no focus
  gradient — 측정: `r_k3["delta"] >= r_k6["delta"]`)
- **F4 DETERMINISM**: re-run result byte-different → raw#9 violation (측정:
  in-process pure-fn 재계산 byte-equal + cross-process sha256 stable)
- **F5 BOUNDS**: any phi ∉ [0, +∞) → primitive error (측정: 모든 phi finite ≥ 0)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (salience proxy = hidden-norm, not tension)**: 본 substrate 에서 per-cell
  tension 이 shared-drive collapse 로 ~0 → salience 를 hidden-norm 으로 대체.
  이것은 anima M-activation magnitude 의 analog 이지만, 'attention' 의 다른
  operationalization (tension-based · attended-input-routing · top-down gating)
  은 다른 결과 가능. 본 cycle 결과는 *hidden-norm salience* 한정.
- **L2 (Φ proxy = cosine-distance, anti-correlated with norm-convergence)**:
  compute_phi_proxy 는 *directional* diversity (pairwise cosine distance) 를
  측정. high-norm cells 는 dominant attractor 로 converge 하며 *방향* 다양성이
  *줄어듦* — 그래서 phi_att < phi_unatt 가 나옴. 이는 'attention 이 Φ 를
  높인다' 가설과 직접 충돌하지만, *이 specific Φ-metric* 의 특성일 수 있음
  (faithful IIT Φ 또는 다른 metric 에서는 다를 수 있음 — H_239/H_268 metric-
  triangulation lane 과 cross-link).
- **L3 (attention ≠ phenomenal attention)**: hidden-norm top-k 는 attention 의
  *substrate observable* 일 뿐 — phenomenal 'attending-to' (의식이 무언가에
  향하는 느낌) 와는 H_004 hard-problem boundary 로 분리.
- **L4 (n_step=15 single config, no-collapse window)**: n_step ≥ 30 에서는
  merge_patience=30 으로 pool 이 N'=2 collapse → partition 무의미. 본 H 는
  no-collapse window (n_step ≤ 25) 한정. step / N / d scaling sensitivity 미검증.
- **L5 (single seed)**: seed=42 단일. multi-seed robustness (H_269/H_272 lane)
  미수행 — 본 결과의 seed-fragility 별도 cycle 필요. 다만 falsification 의
  magnitude (Δ ≈ −0.9, salience-gap +0.40 와 *반대 방향*) 가 커서 seed-flip
  으로 부호가 뒤집힐 가능성은 낮음.
- **L6 (control = first-k index, not random permutation)**: control partition 이
  deterministic first-k index. 진정한 random-permutation null (H_269 n_perms
  스타일) 은 미수행 — index-control 은 cheap proxy. 다만 F2 도 FAIL (salience Δ
  < index Δ) 이라 salience 가 arbitrary 보다 *나쁘게* partition 함이 확인됨.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_221** (`H_221_meditation_jhana_phi_modulation.md`): low-noise + stable-
    attention 'silenced integration' — 본 H 는 attention 의 *partition-grain*
    (attended vs unattended sub-network) 확장.
  - **H_213** (`H_213_time_temporal_binding_window.md`): τ-window Φ inverse-U —
    attention 의 *temporal* axis sister.
  - **H_223** (`H_223_pain_intensity_phi_coupling.md`): phenomenology qualia
    Φ-coupling — 본 H 는 attention qualia 의 sister instance.
  - **H_239** (`H_239_alternative_phi_metric_cross_validation.md`) /
    **H_268** (`H_268_phi_metric_triangulation.md`): L2 의 Φ-metric 의존성 —
    cosine-distance Φ 의 systematic 특성이 본 falsification 을 만든다는 cross-
    link (다른 metric 재측정이 후속 path).
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail` · `compute_phi_proxy`).
- **AXES**: `UNIVERSE/AXES.md` Round 3 (phenomenology) `attention-salience-Φ`
  seed — 본 H 가 consume (R3 phenomenology 의 attention 축 promote).
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) ·
  raw#9/10 (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit
  retraction).
- **philosophy (CLAUDE.md)**: `a_substrate_native_speak` (M-activation salience
  ↔ emit motivation — 본 H 는 그 salience 가 Φ-rich 영역과 *불일치* 함을
  발견 → salience ≠ integration 의 substrate evidence) · p7 NO PERPLEXITY
  VERDICT (Φ-metric 자체를 truth 로 보지 않고 falsifiable test 로 사용).
- **literature pointer**: Posner (1980) attention spotlight · Dehaene & Mashour
  global workspace broadcast · Tononi IIT (attention-Φ coupling claims) —
  substrate analog 의 distant anchor (formal mapping 본 cycle 미수행).
- **state**: `UNIVERSE/state/h279_attention_salience_phi_2026_05_25/{run_h279.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, $0 mac
local hexa-only deterministic.

```
verdict_class: FALSIFIED  (F1 SALIENCE-Φ FAIL — attention amplification 부재)
verdict_tier: 🟢 NUMERICAL  (3 salience-quantile × index-control + cross-process determinism)
evidence_summary:
  3-condition (top-3/4/6 of N=12) salience-partition Φ vs index-control
  (d=8, n_step=15, salience=hidden-norm, seed=42).
    k=3 : phi_att=0.8383  phi_unatt=2.0442  Δ=-1.2059  Δ_ctrl=-0.6736  sal_gap=+0.4538
    k=4 : phi_att=1.0724  phi_unatt=2.0060  Δ=-0.9337  Δ_ctrl=-0.2689  sal_gap=+0.4032
    k=6 : phi_att=1.3759  phi_unatt=1.9815  Δ=-0.6055  Δ_ctrl=+0.8884  sal_gap=+0.3785
  salience-gap (att − unatt) POSITIVE 전 조건 (high-norm cells correctly attended)
  BUT phi_att < phi_unatt 전 조건 (Φ-gap 부호 반대).
falsifiers_triggered: F1 (SALIENCE-Φ FAIL) + F2 (SALIENCE>ARBITR FAIL) + F3 (FOCUS-SHARPEN FAIL)
falsifiers_pass: F4 (determinism) + F5 (bounds) = 2/5
criteria_met: 1/4 (C4 only; C1 ∧ C2 ∧ C3 FAIL)
key_finding:
  attention-as-Φ-amplification 가설 FALSIFIED. high-salience (high hidden-norm)
  cells 는 정확히 attended 되지만 (salience_gap > 0 전 조건), 그들의 Φ 는
  unattended 영역보다 *낮다* (Δ ≈ −0.6 ~ −1.2). 더 좁게 attend 할수록 Δ 가
  *더 negative* (focus-sharpening 의 역방향). mechanism: high-norm cells 는
  dominant attractor 로 directional convergence → pairwise cosine-distance
  (compute_phi_proxy 의 통화) 가 줄어듦. 즉 'activation magnitude' 와 'directional
  integration' 은 본 substrate 에서 anti-correlated — salience(amplitude) ≠
  Φ(diversity). control 도 F2 FAIL (salience Δ < index Δ at top-4/6) — salience
  partition 이 arbitrary index 보다 Φ-분리를 *나쁘게* 함.
honest_note:
  L2 carry confirmed — 결과는 cosine-distance Φ-metric 의 norm-convergence
  특성에 결정적으로 의존. faithful IIT Φ 또는 norm-invariant metric 에서는
  부호가 다를 수 있음 (H_239/H_268 metric-triangulation 재측정이 결정적 후속).
  L1 carry — hidden-norm salience 한정 (tension collapse 로 인한 proxy 대체).
  falsification magnitude (Δ ≈ −0.9 vs sal_gap +0.40) 가 커서 seed-flip 으로
  부호 반전 가능성 낮음 — robust negative result.
sibling: H_221 (jhana attention), H_213 (temporal binding), H_239/H_268 (Φ-metric)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_279 attention-salience-Φ — attended vs unattended sub-network Φ
  d_model=8 pool_N=12 n_step=15 seed=42
  salience = per-cell hidden L2 norm · attended = top-k salience
  k sweep: top-3 / top-4 / top-6
================================================================
  k   N'   phi_att   phi_unatt   delta    delta_ctrl  sal_att  sal_unatt
  --  ---  --------  ---------  -------  ----------  -------  --------
  3   12   0.838274   2.04416   -1.20588   -0.673622   1.57606   1.12222
  4   12   1.07235   2.00604   -0.933686   -0.268931   1.50447   1.10128
  6   12   1.37594   1.98148   -0.605544   0.888407   1.42494   1.04642

derived:
  Δ_top3 = -1.20588
  Δ_top4 = -0.933686
  Δ_top6 = -0.605544
  Δ_ctrl_top4 = -0.268931
  salience-gap (att - unatt) top4 = 0.403193

C1 top-4 phi_att - phi_unatt >= 0.02   : false
C2 Δ_salience > Δ_index (top-4)        : false
C3 Δ_top3 >= Δ_top4 >= Δ_top6 monotone : false
C4 re-run Δ byte-equal                 : true

F1 SALIENCE-Φ      (phi_att > phi_unatt)   FAIL
F2 SALIENCE>ARBITR (Δ_sal > Δ_index)       FAIL
F3 FOCUS-SHARPEN   (Δ_top3 >= Δ_top6)      FAIL
F4 DETERMINISM     (re-run byte-equal)     PASS
F5 BOUNDS          (all phi finite >= 0)   PASS
================================================================
VERDICT: FALSIFIED  (1/4 criteria, 2/5 falsifiers PASS)
================================================================
ledger -> UNIVERSE/state/h279_attention_salience_phi_2026_05_25/result.json
```

**Cross-process determinism**: result.json sha256
`7e7c4428fa4228d17aff5751d5353e0d1313dfba150d796c52d01547a26020ba`
(re-run byte-equal, RFC 033 single gauss stream).

**State output**: `state/h279_attention_salience_phi_2026_05_25/result.json`
**Smoke**: `state/h279_attention_salience_phi_2026_05_25/run_h279.hexa` (hexa-only, LLM none)
