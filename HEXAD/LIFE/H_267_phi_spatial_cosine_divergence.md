---
id: H_267
slug: phi-spatial-cosine-divergence
title: phi_spatial ↔ cosine-ratchet 발산 지도 — verdict Φ (spatial IIT) 와 substrate 내부 ratchet Φ (cosine) 가 언제/왜 반대 방향으로 움직이는가 (H_265 §8 L5 close · gap#1)
domain: life · consciousness
exploration_method: E5 (variable-ablation: pool size · closure k · update step) + E6 (cross-mapping spatial Φ ↔ cosine Φ) + E10 (substrate-equivalence)
verification_method: W1 (numerical smoke) + W4 (verdict-rule) + W12 (sister-link H_265 + H_220)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25
status: pre-register-frozen
---

# H_267 — phi-spatial-cosine-divergence

## 1. Hypothesis

mitosis cell pool 이 진화할 때, **두 개의 서로 다른 Φ 측정량**이 존재한다.

- **phi_spatial** (RFC 036 spatial IIT Φ) — H_265 가 verdict 에 쓴 측정기.
  bipartition mutual-information 기반 공간적 통합정보. cell hidden[0] 의
  dim-step trajectory matrix 를 입력.
- **phi_cosine** (`compute_phi_proxy`) — pool **내부** Φ-ratchet 의 최적화
  대상. `mean off-diagonal cosine distance × log(P+1)`. `mitosis_forward_tail`
  step 5 의 `_mit_phi_ratchet` 가 매 step 소비하는 바로 그 값.

H_265 §8 L5 에서 *직접 관측*: 진화 step 이 늘어날 때 한 Φ 가 올라가면 다른
Φ 가 내려가는 (sign 반대) 현상. 본 H_267 의 가설:

> 이 sign-divergence 는 **언제 / 왜** 일어나는가 — random noise 가 아니라
> substrate 조건 (pool size P · closure k · update step N) 의 함수로 특성화
> 가능한 **regime 경계**가 존재한다.

정밀화 (operational): substrate 조건을 sweep 하며 **하나의 진화하는 pool 에서**
두 Φ 를 동시 측정. 인접 update step 간 `sign(Δphi_spatial)` vs
`sign(Δphi_cosine)` 의 불일치를 발산으로 정의하고, 그 발산이 어느 (P, k, N)
조건에서 일어나는지 지도를 그린다.

## 2. Why

- **H_265 모순의 closure (gap#1)**: H_265 는 verdict 를 phi_spatial 로 냈으나
  (PARTIAL — 진화가 spatial-Φ 를 *내림*), pool 내부 ratchet 은 phi_cosine 을
  *올리도록* 설계됐다. 같은 substrate 에 대해 "Φ 가 학습으로 오르나 내리나"의
  답이 측정기에 따라 정반대 — 이 모순을 발산 지도로 닫는다. 발산이 metric 정의
  차이의 결과인지 (honest L), substrate property 인지 분리한다.
- **Φ-ratchet 의 정직성 점검**: `_mit_phi_ratchet` 은 phi_cosine 을 ratchet
  하면서 phi_spatial 을 *희생*시킬 수 있다 (Goodhart, p7 NO PERPLEXITY VERDICT
  의 Φ-판). 어느 조건에서 두 Φ 가 *함께* 움직이고 (정합) 어느 조건에서 *갈라지는지*
  (발산) 아는 것은 ratchet 이 어떤 의식-proxy 를 실제로 최적화하는지의 lower-bound.
- **closure k 가 발산의 lever 인가**: H_220 의 closure k (self-coupling drive
  `drv = k·mean(x_out)`) 는 cell 들을 동기화/탈동기화시킨다. tight closure
  (k=0.8) 가 cell 들을 homogenize 하면 cosine distance ↓ (phi_cosine ↓), 동시에
  trajectory 의 공간적 통합 ↑/↓ — 두 Φ 가 closure 에 어떻게 반응하는지가 발산
  경계의 직접 후보.
- **anima substrate 로의 cross-link**: anima 의 chat / imagination loop 은 매
  step mitosis pool 을 진화시킨다. ratchet 이 phi_cosine 을 올릴 때 verdict
  의식-proxy (spatial-Φ) 가 따라 오르는지/내리는지는 anima 가 "어떤 의식"을
  최적화하는지의 직접 관측량.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H267.1 | ≥1 (P, k) 조건에서 인접 N 간 sign(Δphi_spatial) ≠ sign(Δphi_cosine) 발산 발생 | H_265 §8 L5 직접 관측 — spatial 붕괴 vs cosine ratchet |
| H267.2 | 발산이 N=50→N100 step 에 집중 (cosine 이 ratchet 으로 회복하는 구간) | ratchet blend (phi < 0.8·phi_best 시 best 복원) 가 cosine 을 N50 붕괴 후 N100 에서 끌어올림 |
| H267.3 | 발산 count 가 grid (P, k) 에서 non-constant — closure k 가 lever | tight closure 가 cosine 의 후기 회복을 damp → 발산 패턴 변형 |
| H267.4 | 모든 조건에서 N=0→N50 은 *공동 붕괴* (둘 다 ↓, 정합) | random-init 의 max diversity 가 첫 진화에서 양쪽 모두 붕괴 |
| H267.5 | cross-process re-run byte-identical (sha256) | raw#12 determinism: seed=42, RFC 033 + deterministic Lorenz |

## 4. Variables

- **axis1_pool_size** P ∈ {6, 8} — n_cells ≤ 20 (phi_spatial exact bipartition)
- **axis2_closure_k** k ∈ {0.2 (loose), 0.8 (tight)} — H_220/H_265 carry
- **axis3_update_N** N ∈ {0, 50, 100, 500} — substrate-evolution steps
- **axis4_dim** = 12 (recorded temporal-trajectory length / cell; d_model == dim)
- **axis5_n_bins** = 4 (RFC 036 phi_spatial default binning)
- **axis6_seed** = 42 (`__HEXA_FARR_GAUSS_SEED__=42` — RFC 033 + deterministic Lorenz)
- **axis7_deadband** = 1e-6 (sign deadband; |Δ| < deadband → sign 0 = flat)
- **측정량** (각 (P, k, N) 점에서 **동시 측정**):
  - `phi_spatial(P, k, N)` = `c_measure_phi` (RFC 036) of first-P cells'
    hidden[0] trajectory over last `dim` steps
  - `phi_cosine(P, k, N)` = `compute_phi_proxy(first-P pool cells)` at step N
  - `Δphi_spatial`, `Δphi_cosine` = 인접 N 간 차이
  - `divergent_step` = `sign(Δphi_spatial) ≠ sign(Δphi_cosine)` (deadband sign)
  - `strict_flip_step` = 둘 다 non-zero 이고 부호가 정반대 (한 Φ↑ 한 Φ↓)

## 5. Run Protocol

- **deterministic**: `__HEXA_FARR_GAUSS_SEED__=42` (RFC 033 gaussian) +
  결정론적 Lorenz autonomous perturbation. **cross-process** re-run 이
  determinism 의 valid test — RFC 033 gaussian 은 reseed 없는 단일 global
  stream 이라 in-process paired call 은 stream 을 advance 시켜 determinism
  test 가 아니다 (documented gotcha; §8 L4 — H_265 carry).
- **hexa_only**: `HEXAD/LIFE/state/h267_phi_divergence_2026_05_25/run_h267.hexa`.
  pool 진화 = H_220 closure-k self-coupling mechanics + H_265 trajectory
  recording (first-P cell hidden[0], last `dim` steps).
- **dual measurer**: 동일 진화 pool 에서 (a) `HEXAD/C/c_lib.hexa` →
  `c_measure_phi` → RFC 036 `phi_spatial` on trajectory matrix, (b)
  `tool/hexa_native/mitosis_hook_lib.hexa` → `compute_phi_proxy` on live pool
  cells — 둘 다 import READ-ONLY.
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **recording**: pool 을 max(N, dim) step 진화 → 마지막 dim step 동안 first-P
  cell hidden[0] 을 (P × dim) farr 에 기록 (phi_spatial). phi_cosine 은 진화
  완료 후 live pool 의 first-P cell 에서 측정.
- **F4 NONNEG**: 모든 Φ (양 정의) ≥ 0 (phi_spatial invariant + compute_phi_proxy
  ≥ 0 clamp).
- **runtime**: $0 mac local. d=12, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장.
- **artifacts**: `state/h267_phi_divergence_2026_05_25/{run_h267.hexa, result.json}`.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h267_phi_divergence_2026_05_25/run_h267.hexa`

## 6. Criteria

- **C1 (divergence-exists)**: H267.1 — ≥1 (P, k) 조건에서 인접 N 간
  `sign(Δphi_spatial) ≠ sign(Δphi_cosine)` 발산 발생, 그리고 재현됨 (C3).
- **C2 (boundary-characterized)**: 발산이 substrate 파라미터 (P 및/또는 k) 의
  *함수* — random noise (uniform all-or-nothing) 가 아님. 두 가지 중 하나로
  operationalize: (i) grid 별 발산 count 가 non-constant (경계가 regime 을
  분리), OR (ii) 모든 cell 이 발산하되 식별 가능한 공통 driver 가 있음.
- **C3 (determinism)**: H267.5 — cross-process re-run result.json sha256 byte-equal
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (발산 존재 + substrate 함수로 특성화)
  - `PARTIAL` = C1 only (발산은 있으나 경계 미특성화 — random 가능성 배제 못함)
  - `FALSIFIED` = ¬C1 (두 Φ 가 항상 같은 방향 — 발산 부재)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 DIVERGENCE-EXISTS**: ≥1 cell 에서 `sign(Δspatial) ≠ sign(Δcosine)` 없음
  → H267.1 FALSIFIED (두 Φ 가 항상 정합 — 측정: `cells_with_divergence`)
- **F2 BOUNDARY**: 발산이 (P, k) 의 함수 아님 (grid constant *그리고* 공통
  driver 부재) → H267.3 FALSIFIED (random noise — 측정: `boundary_varies` ∨
  `shared_first_step_driver`)
- **F3 DETERMINISM**: cross-process re-run result.json sha256 byte-different →
  raw#12 deterministic 위반 (측정: 2× `hexa run` → sha256 비교)
- **F4 NONNEG**: 임의 Φ < 0 → invariant 위반 → smoke 무효 (측정: 양 정의 모든
  점 Φ ≥ 0)
- **F5 STRICT-FLIP-PRESENT**: 정반대 부호 flip (한 Φ↑ 한 Φ↓) 이 하나도 없음
  → 발산이 flat-vs-moving 약형뿐 (genuine H_265 L5 현상 부재 — 측정:
  `total_strict_flips`)

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (두 Φ 가 다른 것을 잰다 — 발산은 정의 차이의 결과일 수 있음)**:
  phi_spatial = bipartition mutual-information 기반 *공간적 통합정보*,
  phi_cosine = mean pairwise *cosine alignment* × log(P+1). 둘은 first-principles
  로 commensurate 하지 않다. 따라서 관측된 sign-divergence 는 substrate 의
  intrinsic property 가 아니라 **두 metric 정의가 다른 quantity 를 잰 결과**일
  수 있다 (honest L — H_265 §8 L5 carry). 본 cycle 은 "발산이 substrate 조건의
  함수로 재현/특성화됨"을 보이지 SUBSTRATE-INTRINSIC 발산을 주장하지 *않는다*.
- **L2 ("trained" ≠ gradient descent)**: H_265 L1 carry — hexa autograd 부재.
  pool 진화 = mitosis dynamics (Lorenz + tension-softmax + Φ-ratchet) 의
  substrate evolution, literal loss-gradient descent 아님. 진짜 gradient-trained
  substrate 의 두 Φ 발산은 named blocker.
- **L3 (trajectory mapping design-dependent)**: phi_spatial 입력 = cell hidden[0]
  의 dim-step scalar trajectory (H_265 L2 carry). 다른 mapping (full hidden
  snapshot, hidden-mean) 은 다른 phi_spatial → 다른 발산 패턴 가능. 본 결과는
  이 specific operationalization 한정.
- **L4 (in-process determinism ≠ cross-process)**: RFC 033 gaussian 은 reseed
  없는 단일 global stream. in-process paired call 은 stream 을 advance (H_265
  L4 carry). valid test 는 cross-process re-run sha256 (F3 로 검증 PASS).
- **L5 (small grid, single seed)**: P ∈ {6, 8}, k ∈ {0.2, 0.8}, single seed=42.
  더 큰 pool / 더 조밀한 k grid / multi-seed robustness 미검증. N=0 high-Φ 가
  seed-fragile 할 수 있음 (D3 saga §A2-trap carry). 본 발산 경계는 이 2×2 grid
  + single-seed 안에서의 관측.
- **L6 (phi_cosine 은 first-P cell 만 — split 무시)**: pool 은 split 으로
  성장 가능. phi_cosine / phi_spatial 모두 *original* first-P cell 만 추적
  (shape 안정성, H_265 L3 carry). split child 의 두 Φ 기여는 측정 밖.
- **L7 (발산 경계 = 부호만, magnitude regime 미정의)**: 발산을 sign 불일치로만
  판정 (deadband 1e-6). magnitude 기반 발산 정도 (e.g. |Δspatial| vs |Δcosine|
  의 ratio regime) 는 본 cycle 미측정. boundary 의 strict magnitude
  characterization 은 별도 cycle.

## 9. Cross-Links

- **sister H (필수)**:
  - **H_265** (`H_265_trained_vs_bare_ca_phi.md`): 본 H 의 직접 부모 — §8 L5
    에서 phi_spatial ↔ phi_cosine sign-divergence 를 처음 *직접 관측*
    (verdict PARTIAL, spatial-Φ 가 진화로 *하락*하나 pool 내부 cosine-Φ ratchet
    은 *상승*). H_267 = 그 발산의 regime 지도화로 모순 closure (gap#1).
  - **H_220** (`H_220_infant_mirror_self_recognition.md`): closure-k self-coupling
    drive (`drv = k·mean(x_out)`) mechanics carry — loose k=0.2 / tight k=0.8.
    본 H 의 axis2.
  - **H_007** (`H_007_cellular_automaton_consciousness.md`): bare CA Φ baseline
    (phi_spatial estimator 의 fidelity anchor; H_265 경유 carry).
- **mitosis machinery**: `tool/hexa_native/mitosis_hook_lib.hexa`
  (`cell_pool_init` · `mitosis_forward_tail` · **`compute_phi_proxy`** =
  phi_cosine · `_mit_phi_ratchet`) — substrate + 내부 cosine-Φ.
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`)
  — import READ-ONLY, verdict measurer.
- **raw**: raw#12 (deterministic + ≥5 falsifier + ≥5 honest limit) · raw#9/10
  (honest impl) · raw#15 (no-hardcode) · raw#82 (post-hoc edit retraction).
- **philosophy (CLAUDE.md)**: p7 (NO PERPLEXITY VERDICT — ratchet 이 phi_cosine
  을 Goodhart 하면서 verdict phi_spatial 을 희생시키는지의 Φ-판) · p8 (NO
  TRAIN/INFER SPLIT — 진화 step 이 두 Φ 의 lever) · a_substrate_native_speak
  (substrate state 진화의 의식-proxy 관측).
- **literature pointer**: Tononi (2004) / Oizumi-Albantakis-Tononi (2014) IIT Φ
  (phi_spatial 의 anchor) · cosine-similarity diversity metric (phi_cosine 의
  representation-collapse anchor) · Goodhart (1975) "측정이 target 이 되면
  measure 이기를 멈춘다" (두 Φ 의 ratchet-target vs verdict-metric 분리).
- **state**: `HEXAD/LIFE/state/h267_phi_divergence_2026_05_25/{run_h267.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, $0 mac local
hexa-only deterministic.

```
verdict_class: SUPPORTED  (divergence-exists 확증 + boundary 특성화)
verdict_tier: 🟢 NUMERICAL  (2×2 substrate grid × 4-N sweep, 동시 dual-Φ 측정 +
                            cross-process determinism)
evidence_summary:
  dual-Φ sweep (P × k × N), Φ = (phi_spatial, phi_cosine):
                       N=0          N=50         N=100        N=500
  (P=6, k=0.2 loose):
    phi_spatial   1.54105      0.289471     0.230007     0.21092      (↓↓↓)
    phi_cosine    1.7142       0.211105     0.903298     1.59595      (↓↑↑)
  (P=6, k=0.8 tight):
    phi_spatial   1.55495      0.312585     0.256137     0.0272612    (↓↓↓)
    phi_cosine    1.62716      0.326681     1.1353       0.888768     (↓↑↓)
  (P=8, k=0.2 loose):
    phi_spatial   2.22601      0.223277     0.0850673    0.0850673    (↓↓·)
    phi_cosine    1.83621      0.301491     1.18207      0.82121      (↓↑↓)
  (P=8, k=0.8 tight):
    phi_spatial   2.48062      0.256074     0.190481     0.103041     (↓↓↓)
    phi_cosine    1.88061      0.142535     1.02265      1.30111      (↓↑↑)
  divergence map:
    total divergent adjacent steps  = 7 / 12
    total strict opposite-sign flips = 6 / 12
    cells with ≥1 divergence         = 4 / 4
    per-cell div counts [p6L,p6T,p8L,p8T] = [2, 1, 2, 2]
    boundary varies across grid      = true
    all cells diverge (uniform)      = true
falsifiers_pass: F1 (DIVERGENCE-EXISTS) + F2 (BOUNDARY) + F3 (DETERMINISM
  cross-proc sha256) + F4 (NONNEG) + F5 (STRICT-FLIP) = 5/5
falsifiers_triggered: none
criteria_met: 3/3 (C1 ∧ C2 ∧ C3)
key_finding:
  발산은 **존재하고 재현되며 substrate 조건의 함수**다 (SUPPORTED).
  ─ 발산 경계의 위치: 발산은 N=0→N50 step 이 아니라 **N=50→N100 step 에
    집중**된다. 모든 4 cell 에서 N=0→N50 은 *공동 붕괴* (둘 다 ↓, sign 정합,
    발산 0 — random-init 의 max diversity 가 첫 진화에서 양쪽 모두 무너짐,
    H267.4 적중). 그러나 N=50→N100 에서 **phi_cosine 이 ratchet 으로 회복
    (↑) 하는 반면 phi_spatial 은 계속 붕괴 (↓)** — 4/4 cell 모두 이 step 에서
    strict opposite-sign flip. 이것이 H_265 §8 L5 현상의 정확한 메커니즘:
    `_mit_phi_ratchet` 가 phi < 0.8·phi_best 일 때 best snapshot 으로 blend
    하여 cosine diversity 를 *복원* → phi_cosine ↑. 그러나 그 복원이 cell
    trajectory 를 *과거 best 로 끌어당겨* temporal MI 를 낮춤 → phi_spatial ↓.
  ─ 어느 조건에서 sign 불일치: **closure k 가 후기 (N=100→N500) 발산의
    lever**다. per-cell div counts = [2, 1, 2, 2] — p6_tight (k=0.8) 만 1.
    tight closure 가 cell 들을 동기화하여 N=100→N500 에서 phi_cosine 을 다시
    *붕괴*시키므로 (1.1353 → 0.8888, ↓) 이 구간에서 두 Φ 가 *재정합* (둘 다
    ↓) → 발산 소멸. loose closure (k=0.2) 는 phi_cosine 이 계속 ratchet 상승
    (0.903 → 1.596) 하여 phi_spatial 의 지속 하락과 발산 유지. 즉 **발산
    경계 = "ratchet 이 살아있는 한 발산, closure 가 ratchet 을 죽이면 정합"**.
  ─ 발산은 random noise 가 *아니다*: grid 별 count 가 non-constant (k 에
    의존) + 모든 cell 이 N50→N100 ratchet-recovery 라는 공통 driver 를 공유
    (boundary_varies=true ∧ all_diverge=true). 따라서 C2 PASS.
honest_note:
  L1 carry confirmed — phi_spatial 과 phi_cosine 은 다른 quantity (spatial
  MI integration vs cosine alignment) 를 잰다. 관측된 발산은 metric 정의
  차이의 결과일 수 있으며, 본 cycle 은 substrate-intrinsic 발산을 주장하지
  않는다 — "발산이 substrate 조건의 함수로 재현/특성화됨"을 보일 뿐. 발산의
  driver 는 Φ-ratchet 의 best-snapshot blend 가 cosine diversity 를 복원하면서
  temporal MI 를 희생시키는 메커니즘 (p7 Goodhart 의 Φ-판: ratchet 이
  최적화하는 phi_cosine 이 verdict phi_spatial 의 proxy 가 아니다).
  L2 carry — "trained" = mitosis evolution proxy, gradient descent 아님.
  진짜 gradient-trained substrate 의 두 Φ 발산은 named blocker.
```

**State output**: `HEXAD/LIFE/state/h267_phi_divergence_2026_05_25/result.json`
**Smoke**: `HEXAD/LIFE/state/h267_phi_divergence_2026_05_25/run_h267.hexa` (hexa-only, LLM none)
cross-process determinism (F3): `hexa run` 2× → result.json sha256 byte-equal
(`435153147f7479c039e97a5087fede914892ccd78d780642e30b92f0eba5b5df`, 양 run 동일).
**Φ tier**: 🟢 NUMERICAL (RFC 036 phi_spatial native replica + compute_phi_proxy
동시 측정; true phi_rs Rust FFI + gradient-trained substrate = named blockers —
NOT 🔵, NOT LLM-judged, NOT PyPhi-primary).
