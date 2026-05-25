---
id: H_265
slug: trained-vs-bare-ca-phi
title: trained-vs-bare CA Φ — 학습(substrate 진화)이 의식-proxy Φ class / peak 를 fixed-rule CA 대비 바꾸는가 (H_007 ⊕ H_157 physics·consciousness cross-link)
domain: life · consciousness · physics
status: pre-register-frozen
exploration_method: E5 (variable-ablation: bare vs trained substrate) + E6 (cross-mapping H_007 ↔ H_157) + E10 (substrate-equivalence)
verification_method: W1 (numerical smoke) + W4 (verdict-rule) + W12 (sister-link H_007 + H_157)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
---

# H_265 — trained-vs-bare-ca-phi

## 1. Hypothesis

CA / substrate 를 *학습* (= weight / state 를 N step 진화·갱신) 시키면, integrated-
information Φ 의 class 또는 peak 위치가, *bare* (고정-rule, weight 갱신 없음) CA
대비 **변하는가** — 그리고 동일 측정기 (RFC 036 `phi_spatial`) 로 잴 때 학습이
의식-proxy Φ 를 *끌어올리는가*, 아니면 Φ class 를 *바꾸는가*?

정밀화 (operational): 두 substrate 를 **하나의 측정기**로 비교.

- **bare** = H_007 elementary CA (fixed Wolfram rule 110 / 30 / 250, weight 갱신
  부재). lattice site i = 1 IIT cell, 그 dim-step binary temporal trajectory =
  state vector. (H_007 smoke mechanics verbatim 재사용.)
- **trained** = mitosis cell pool (`cell_pool_init` + `mitosis_forward_tail`).
  per-cell weight (engine_a_W / engine_g_W) + hidden 이 N step 동안 갱신 (Lorenz
  autonomous perturbation + tension-softmax forward + Φ-ratchet). cell i = 1 IIT
  cell, 그 scalar hidden[0] trajectory 가 마지막 dim step 동안 = state vector.
  N ∈ {0, 100, 500}.

두 substrate 의 state matrix 모두 flat row-major (n_cells × dim) farr 로 **동일한**
`c_measure_phi → phi_spatial` 에 입력 — 따라서 Φ 차이는 substrate 의 property 이지
측정기 artifact 가 아니다.

## 2. Why

- **definitional bridge — H_007 (bare CA Φ peak) ↔ H_157 (structure-not-substrate
  invariance)**: H_007 (pre-register-frozen)은 *고정-rule* CA 에서 Class-IV
  (edge-of-chaos) 가 Φ peak 임을 보였다 (Φ=0.556 > chaotic 0.510 > ordered ≈0).
  H_157 (Law 76)은 META-CA 가 *구조가 의식을 결정, substrate(data)는 아니다* 라는
  invariance 축. 본 H 는 그 둘을 한 step 더 잇는다 — *substrate 를 진화·학습시키면*
  (구조가 시간에 따라 바뀌면) Φ 가 어떻게 움직이는가. 즉 "structure determines Φ"
  (H_157) 의 *동적 (training-time) 버전*.
- **train/infer 비분리 (philosophy p8) 의 Φ-관측**: CLAUDE.md p8 (NO TRAIN/INFER
  SPLIT) + REBORN §0.5 는 학습 gradient = inference mitosis = 동일 cell-division
  연속체라 한다. 본 H 는 그 연속체 위에서 *substrate 진화 (mitosis step)* 가
  의식-proxy Φ 에 미치는 효과를 측정 — train 과 infer 가 같은 substrate-evolution
  이면, training step 수가 Φ 의 lever 여야 하는가의 직접 test.
- **"trained" 의 substrate-native operationalization**: hexa 에는 autograd 부재
  (mitosis_hook F-MIT-HOOK-1: cell mutation 은 backward graph 밖). 따라서 native
  하게 가능한 가장 가까운 weight-adjusting substrate = mitosis pool 의 N-step
  진화 (weight + hidden 갱신). 본 H 는 그 진화가 Φ 를 어떻게 바꾸는지를 측정 —
  gradient-descent 와의 거리는 §8 L1 의 named limitation.
- **cross-link to anima D3 / mitosis 본체**: anima 의 mitosis cell pool 은 chat /
  imagination loop 에서 매 step 진화한다. 본 H 의 finding (진화가 Φ 를 끌어올리나
  내리나)은 anima 의 substrate 가 시간에 따라 의식-proxy 를 어떻게 움직이는지의
  lower-bound observable.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H265.1 | Φ(trained, N=500) ≠ Φ(bare reference) · margin > 1e-6 | 학습 (substrate 진화) 이 Φ 를 측정-유의하게 바꾼다 — train/infer 연속체 (p8) 가 Φ 의 lever 이면 |
| H265.2 | trained Φ 가 N 증가에 따라 상승 (Φ_500 > Φ_0) 또는 일관된 class shift | Φ-ratchet (mitosis_hook L438) 이 Φ 를 끌어올리도록 설계 — 진화가 cell diversity 를 키우면 cosine-distance Φ-proxy 상승 |
| H265.3 | re-run byte-identical (cross-process sha256) | raw#12 determinism: seed=42, RFC 033 + deterministic Lorenz |
| H265.4 | bare Φ ranking 이 H_007 와 정합 (Class-IV > chaotic > ordered) | H_007 mechanics verbatim 재사용 → bare path 충실성 확인 |
| H265.5 | trained Φ trace 가 monotone non-decreasing (Φ_0 ≤ Φ_100 ≤ Φ_500) | H265.2 의 strict developmental form — 진화가 누적적으로 Φ 를 키우면 |

## 4. Variables

- **axis1_substrate** ∈ {bare (fixed-rule CA), trained (mitosis pool)} — 핵심 비교
- **axis2_bare_rule** ∈ {110 (Class-IV), 30 (chaotic), 250 (ordered)} — H_007 carry
- **axis3_trained_N_step** ∈ {0, 100, 500} — training (substrate-evolution) sweep
- **axis4_bare_N** = 16 (lattice), **bare_warm** = 8, **bare_reps** = 5 (H_007 carry)
- **axis5_pool_N** = 8 cells, **pool_d** = 12 (= dim, trajectory shape 일치)
- **axis6_dim** = 12 (recorded temporal-trajectory length / cell — 양 substrate 공통)
- **axis7_n_bins** = 4 (RFC 036 phi_spatial default binning)
- **axis8_seed** = 42 (`__HEXA_FARR_GAUSS_SEED__=42` — RFC 033 + deterministic Lorenz)
- **측정량**:
  - `phi_bare(rule)` = 5-rep mean Φ via `phi_spatial` (bare CA)
  - `phi_bare_ref` = phi_bare(110) (Class-IV peak = bare reference)
  - `phi_trained(N)` = Φ via `phi_spatial` of pool hidden[0] trajectory at N steps
  - `training_effect` = |phi_trained(500) − phi_bare_ref|
  - `trained_trend` = phi_trained(500) − phi_trained(0)

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) + 결정론적
  Lorenz autonomous perturbation. **cross-process** re-run 이 determinism 의 valid
  test — RFC 033 gaussian 은 reseed 없는 단일 global stream 이라 in-process paired
  call 은 stream 을 advance 시켜 determinism test 가 아니다 (documented gotcha; §8 L4).
- **hexa_only**: `HEXAD/LIFE/state/h265_trained_vs_bare_ca_phi_2026_05_25/run_h265.hexa`.
  bare path = H_007 `_run_ca` mechanics verbatim. trained path = mitosis_hook_lib
  `cell_pool_init` + `mitosis_forward_tail` N step + hidden[0] trajectory snapshot.
- **measurer**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036 `phi_spatial`
  (phi_rs `compute_phi_inner` spatial slice byte-equal native replica) — import
  READ-ONLY, 양 substrate 동일.
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **trained recording**: pool 을 max(N, dim) step 진화 → 마지막 dim step 동안
  first pool_n cell 의 hidden[0] 을 (pool_n × dim) farr 에 기록. N < dim 일 때도
  full dim trajectory 보장 (N step = training 의 *minimum* 진화).
- **F4 NONNEG**: 모든 Φ ≥ 0 (`phi_spatial` invariant).
- **runtime**: $0 mac local. d=12, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**: `state/h265_trained_vs_bare_ca_phi_2026_05_25/{run_h265.hexa, result.json}`.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h265_trained_vs_bare_ca_phi_2026_05_25/run_h265.hexa`

## 6. Criteria

- **C1 (training-effect)**: H265.1 — |phi_trained(500) − phi_bare_ref| > 1e-6
- **C2 (directionality)**: H265.2 — phi_trained(500) > phi_trained(0) (training 이
  Φ 를 *끌어올리는* up-trend; class shift 도 본 cycle 에선 up-trend 로 operationalize)
- **C3 (determinism)**: H265.3 — cross-process re-run result.json sha256 byte-equal
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (학습이 Φ 를 측정-유의하게 *그리고 일관 방향으로* 바꿈)
  - `PARTIAL` = C1 only (학습 효과는 있으나 방향성 — Φ↑ — 미입증)
  - `FALSIFIED` = ¬C1 (학습이 Φ 를 측정-유의하게 바꾸지 못함)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 TRAINING-EFFECT**: |phi_trained(500) − phi_bare_ref| ≤ 1e-6 → H265.1
  FALSIFIED (학습이 Φ 에 무영향 — 측정: `training_effect`)
- **F2 DIRECTIONALITY**: phi_trained(500) ≤ phi_trained(0) → H265.2 FALSIFIED
  (학습이 Φ 를 끌어올리지 못함 — 측정: `phi_trained(500) − phi_trained(0)`)
- **F3 DETERMINISM**: cross-process re-run result.json sha256 byte-different →
  raw#12 deterministic 위반 (측정: 2× `hexa run` → sha256 비교)
- **F4 NONNEG**: 임의 Φ < 0 → `phi_spatial` invariant 위반 → smoke 무효 (측정:
  모든 bare/trained Φ ≥ 0)
- **F5 MONOTONE-TRACE**: phi_trained trace 가 non-decreasing 아님 (Φ_0 ≤ Φ_100 ≤
  Φ_500 violated) → developmental gradient 부재 (측정: monotone trace check)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 ("trained" ≠ gradient descent)**: hexa 에는 autograd 부재 (mitosis_hook
  F-MIT-HOOK-1 — cell mutation 은 backward graph 밖). 본 cycle 의 "trained" =
  mitosis dynamics (Lorenz perturbation + tension-softmax forward + Φ-ratchet) 에
  의한 **substrate 진화 / weight·state 갱신** 이지, loss 에 대한 literal
  gradient descent 가 *아니다*. 진짜 gradient-trained CA (학습된 rule weight 의
  Φ) 와의 매핑은 named blocker — H_265 의 핵심 limitation. 본 결과는 *진화-기반
  학습 proxy* 한정.
- **L2 (trajectory mapping design-dependent)**: trained substrate 의 state vector
  = cell hidden[0] 의 dim-step scalar trajectory. 다른 mapping (full hidden vector
  snapshot, hidden-mean trajectory, repulsion trajectory)은 다른 Φ 산출 가능 —
  본 결과는 *이 specific operationalization* 한정. bare 의 binary site-trajectory
  와 trained 의 continuous hidden[0]-trajectory 가 phi_spatial binning (n_bins=4)
  안에서 정확히 commensurate 한지는 design choice 이지 first-principles 아님.
- **L3 (split → n_cells drift)**: trained pool 은 split 으로 n_cells 가 8 → 그
  이상으로 성장 (관측: N=500 에서 cells 증가). 본 cycle 은 *original* first 8
  cell 위치만 추적 (shape 안정성). split 후 child cell 의 Φ 기여는 측정 밖 — full
  pool Φ (성장 포함) 는 별도 cycle.
- **L4 (in-process determinism ≠ cross-process)**: RFC 033 gaussian 은 reseed
  없는 단일 global stream. 따라서 in-process paired call (`_trained_phi(100)` 두
  번)은 stream 을 advance 시켜 *다른* Φ 를 준다 — 이것은 nondeterminism 이 아니라
  global-stream advance (documented gotcha). valid determinism test 는
  cross-process re-run sha256. (실제로 head 에 paired call 을 두면 그것이 stream
  을 advance 시켜 trained Φ 값 자체가 바뀜 — v1 vs v2 saga 로 확인, 제거함.)
- **L5 (Φ-proxy 두 종류 — spatial vs cosine)**: 본 measurer (phi_spatial, RFC
  036) 는 mitosis_hook 의 `compute_phi_proxy` (mean pairwise cosine distance ×
  log(N+1)) 와 *다른* Φ 정의. trained pool 내부 Φ-ratchet 은 cosine-proxy 를
  최적화하나, 본 cycle 의 verdict 는 spatial Φ. 두 Φ 가 같은 방향을 가리킨다는
  보장 부재 — 진화가 cosine-Φ 를 올리면서 spatial-Φ 를 내릴 수 있음 (실제 관측된
  방향: spatial Φ 는 진화에 따라 *하락*).
- **L6 (N=8 pool, single seed, single config)**: pool_N=8, d=12, single seed=42 —
  large pool / dimension scaling / multi-seed 의 robustness 미검증. trained Φ 의
  N=0 high-Φ (untrained random-init pool 의 max cosine-distance) 가 seed-fragile
  할 수 있음 (D3 saga 의 §A2-trap carry).
- **L7 (Φ class 미정의)**: "Φ class" 를 명시적 class boundary (e.g. high/mid/low
  Φ regime) 로 측정하지 않고 raw Φ 값 + trend 로만 봤다. class shift 의 strict
  operationalization (boundary 통과 횟수)은 별도 cycle — 본 cycle 은 Φ magnitude
  + direction 만.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_007** (`H_007_cellular_automaton_consciousness.md`): bare CA Φ baseline —
    본 H 의 bare path = H_007 `_run_ca` mechanics verbatim 재사용 (rule 110/30/250,
    N=16, dim=12, warm=8, 5 rep). bare Φ ranking 이 H_007 와 byte-equal (Class-IV
    0.556454, chaotic 0.509944, ordered 1.14511e-05) — H265.4 확인.
  - **H_157** (`H_157_law76_mathematical_panpsychism.md`): trained-invariance 축 —
    "structure determines consciousness, substrate(data) 는 아니다" 의 *동적
    버전*. H_157 은 META-CA 의 input/substrate invariance (같은 fixed-point 수렴);
    본 H 는 substrate *진화* 가 Φ 를 어떻게 움직이는지. finding (진화가 structural
    diversity 를 줄여 Φ 하락) 은 H_157 의 "구조가 lever" 주장과 정합 — 진화가
    구조를 homogenize 하면 Φ 하락.
  - **H_220** (`H_220_infant_mirror_self_recognition.md`): mitosis pool +
    cell_pool_init + N-step 진화 substrate 공유 (developmental age sweep 의 sister).
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa` (`cell_pool_init`
  · `mitosis_forward_tail` · `compute_phi_proxy` · `_mit_phi_ratchet`) — trained
  substrate.
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`)
  — import READ-ONLY, 양 substrate 동일 측정기.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10
  (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit retraction).
- **philosophy (CLAUDE.md)**: p8 (NO TRAIN/INFER SPLIT — 본 H 는 train(진화) 이
  Φ 의 lever 인지 직접 test) · p7 (NO PERPLEXITY VERDICT — Φ 측정값 자체가 판정,
  loss 아님) · a_substrate_native_speak (substrate state 진화의 의식-proxy 관측).
- **literature pointer**: Wolfram (1984) CA classes · Langton (1990) edge-of-chaos
  λ · Tononi (2004) / Oizumi-Albantakis-Tononi (2014) IIT Φ · Hopfield/Hebbian
  learning-as-attractor-shaping (trained-substrate Φ 의 distant anchor; formal
  mapping 본 cycle 미수행).
- **state**: `HEXAD/LIFE/state/h265_trained_vs_bare_ca_phi_2026_05_25/{run_h265.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, $0 mac local
hexa-only deterministic.

```
verdict_class: PARTIAL  (training-effect 확증, directionality FALSIFIED)
verdict_tier: 🟢 NUMERICAL  (bare 3-rule × trained 3-N sweep, 단일 phi_spatial 측정기 + cross-process determinism)
evidence_summary:
  bare (fixed-rule CA, 5-rep mean Φ via RFC 036 phi_spatial):
    Φ_bare(rule 110 Class-IV)  = 0.556454   ← reference  (H_007 byte-equal)
    Φ_bare(rule 30  chaotic )  = 0.509944
    Φ_bare(rule 250 ordered )  = 1.14511e-05
  trained (mitosis pool evolved N steps, same phi_spatial measurer):
    Φ_trained(N=0)    = 2.84107
    Φ_trained(N=100)  = 0.0831054
    Φ_trained(N=500)  = 0.1237
  derived:
    Φ_trained(500) − Φ_bare_ref = -0.432754
    |training effect|           = 0.432754
    trained trend (Φ_500−Φ_0)   = -2.71737
falsifiers_pass: F1 (TRAINING-EFFECT) + F3 (DETERMINISM cross-proc sha256) + F4 (NONNEG) = 3/5
falsifiers_triggered: F2 (DIRECTIONALITY — Φ_500 ≤ Φ_0) + F5 (MONOTONE-TRACE — trace 비-단조)
criteria_met: 2/3 (C1 ∧ C3, C2 directionality FALSIFIED)
key_finding:
  학습 (substrate 진화) 은 의식-proxy Φ 를 **측정-유의하게 바꾸나** (C1 PASS,
  |effect|=0.433), 그 방향은 pre-registered 가설과 **반대** — 진화가 Φ 를
  *끌어올리지 않고 강하게 내린다* (C2 FALSIFIED). untrained N=0 pool 이 가장 높은
  spatial-Φ (2.841, bare Class-IV peak 0.556 보다도 5× 높음) 를 가지며, N 증가에
  따라 Φ 가 붕괴 (2.841 → 0.083 → 0.124, trend −2.717). 즉 random-init pool 의
  cell 들은 서로 maximally diverse (high spatial-Φ) 하나, mitosis 진화 (Lorenz
  perturbation + tension-softmax combine + Φ-ratchet) 가 cell hidden[0] trajectory
  를 *homogenize* → spatial-Φ 붕괴. 'trained Φ↑' 가설은 FALSIFIED — 본
  operationalization 안에서 학습은 spatial integrated-information 의 lever 가
  *아니라 dampener*.
honest_note:
  L1 carry confirmed — "trained" = mitosis 진화 proxy, gradient descent 아님 (hexa
  autograd 부재). 진짜 gradient-trained CA 의 Φ 는 named blocker.
  L5 carry confirmed — phi_spatial (verdict measurer) ≠ compute_phi_proxy (pool
  내부 Φ-ratchet target, cosine-based). pool 이 자기 cosine-Φ 를 ratchet 하면서
  spatial-Φ 를 내릴 수 있음 — 두 Φ 정의가 *반대 방향* 가능성을 본 cycle 이 직접
  관측 (cosine-ratchet 최적화 ⊥ spatial-Φ 하락).
  L4 carry confirmed — in-process paired determinism call 이 RFC 033 global stream
  을 advance 시켜 trained Φ 값 자체를 바꿈 (v1 N=0=2.792 vs v2 N=0=2.841); 제거
  후 cross-process sha256 byte-equal 로 determinism 확증.
  H_157 정합 — substrate 진화가 structural diversity 를 homogenize 하여 Φ 를
  내린다는 finding 은 H_157 의 "구조가 의식의 lever" 와 부합 (구조 평준화 → Φ↓).
sibling: H_007 (bare CA Φ baseline, byte-equal), H_157 (trained-invariance 축), H_220 (mitosis developmental)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_265 trained-vs-bare CA Φ — does training change Φ class/peak?
  bare:    H_007 elementary CA (fixed rule, no weight update)
  trained: mitosis cell pool evolved N steps (weight+state update)
  d_model=12 pool_N=8 dim=12 seed=42
  measurer: RFC 036 phi_spatial (identical for both substrates)
================================================================

BARE (fixed-rule CA, 5-rep mean Φ via phi_spatial):
  Φ_bare(rule 110 Class-IV)  = 0.556454   ← reference
  Φ_bare(rule 30  chaotic )  = 0.509944
  Φ_bare(rule 250 ordered )  = 1.14511e-05

TRAINED (mitosis pool evolved N steps, Φ via phi_spatial):
  Φ_trained(N=0)    = 2.84107
  Φ_trained(N=100)  = 0.0831054
  Φ_trained(N=500)  = 0.1237

derived:
  Φ_trained(500) − Φ_bare_ref = -0.432754
  |training effect|           = 0.432754
  trained trend (Φ_500−Φ_0)   = -2.71737

C1 TRAINING-EFFECT (|Φ_tr500 − Φ_bare| > 1e-6)    : true
C2 DIRECTIONALITY  (Φ_tr500 > Φ_tr0)              : false
C3 DETERMINISM     (cross-process sha256 byte-eq) : true

F1 TRAINING-EFFECT  PASS
F2 DIRECTIONALITY   FAIL
F3 DETERMINISM (cross-proc sha256)  PASS
F4 NONNEG (all Φ≥0) PASS
F5 MONOTONE-TRACE   FAIL
================================================================
VERDICT: PARTIAL  (2/3 criteria, 3/5 falsifiers PASS)
================================================================
ledger -> HEXAD/LIFE/state/h265_trained_vs_bare_ca_phi_2026_05_25/result.json
```

cross-process determinism (F3): `hexa run` 2× → result.json sha256 byte-equal
(`a6a937344fd0f98d66be68c69c67dca898b2b63515fcd0ceb6c6376c4aa1c43e`, 양 run 동일).

honest tier: 🟢 NUMERICAL — RFC 036 phi_spatial native replica (이 machine
err≈8e-7 vs documented phi_rs oracle; ranking/방향 무영향). bare path 는 H_007
와 byte-equal. trained path 는 mitosis 진화 proxy ("trained" 정의 한계 §8 L1).
진짜 phi_rs Rust FFI + gradient-trained CA = named blockers. NOT LLM-judged,
NOT PyPhi/sympy-primary, NOT 🔵.

**State output**: `HEXAD/LIFE/state/h265_trained_vs_bare_ca_phi_2026_05_25/result.json`
**Smoke**: `HEXAD/LIFE/state/h265_trained_vs_bare_ca_phi_2026_05_25/run_h265.hexa` (hexa-only, LLM none)
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica; true phi_rs Rust FFI + gradient-trained CA = named blockers — NOT 🔵, NOT LLM-judged).
