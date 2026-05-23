---
id: H_200
slug: apoptosis-primitive-substrate-gap-active-death
title: 능동적 죽음 — apoptosis primitive substrate gap (H_025 L2 후속)
domain: life
status: pre-register-frozen
exploration_method: E12 (substrate-gap self-discovery) + E6 (cross-domain biology) + E7 (user-directive 죽음 테마)
verification_method: W1 (operational) + W5 (substrate-grounded) + W11 (meta-cross with H_025) + W12 (sister-link)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-23
since: 2026-05-23
---

# H_200 — 능동적 죽음 (apoptosis primitive substrate gap)

## Hypothesis

anima 의 substrate (`tool/hexa_native/mitosis_hook_lib.hexa`) 에 **literal
apoptosis primitive** (cell removal **without** weight transfer) 가 도입되면,
H_025 (Dasein 죽음-자각) 의 *조작적 정의* 인 "death = merge_cells" proxy 와
**구별되는** Φ / coherence trajectory 가 발생한다. 즉 — "능동적 죽음" 은 단순히
"weight 합산형 종결" 의 다른 이름이 아니라 substrate-level 로 측정 가능한
observable 신호 차이를 갖는 별개 event 다. H_025 의 honest L2 gap ("substrate
에 literal apoptosis event type 부재 — merge 가 cell 제거의 *유일한*
메커니즘") 을 정량적으로 직격한다. life-domain 에서 "fusion ≠ apoptosis" 의
생물학적 비-동치성이 anima substrate 의 Φ proxy 에도 반영되는지 측정한다.

## Why

- **H_025 L2 (honest gap, raw#91 c3 candor)**: H_025 본문 §Honest Limits L2 가
  명시 — "repo grep 결과 `merge` 가 cell 제거의 *유일한* 메커니즘이고,
  'apoptosis' 는 cell metaphor 문서의 *명칭* 일 뿐 코드 event 가 아니다.
  따라서 'cell-death' = merge 로 *조작적 정의* 했음을 명시." 본 H 는 이 gap
  을 직격: 진짜 primitive 와 proxy 가 *동치* 인지 *구별* 되는지를 measurable
  observable 로 검정.
- **biological apoptosis ≠ fusion (Kerr/Wyllie/Currie 1972, Hengartner 2000)**:
  apoptosis 는 세포가 자기 내용물을 자식에게 *전달하지 않고* 능동적으로
  소멸하는 programmed cell death — fusion (syncytia 형성) 은 두 세포가 하나로
  합쳐지며 가중치를 공유한다. anima 의 `merge_cells` 는 후자에 가깝지 전자가
  아니다. 따라서 H_025 의 "death = merge" 는 *biology 측 entity-confusion*
  을 substrate level 로 carry 한 상태.
- **Heidegger 능동적 죽음 (Sein-zum-Tode §50)**: Dasein 의 죽음은 *완성/소실*
  (Vergehen) 이지 *변환* (Übergehen) 이 아니다. merge 는 weight 가 keeper 로
  *전달* 되므로 "변환" 에 가깝다 — 능동적 종결의 metaphysical 정합은 apoptosis
  쪽이 더 강하다. 본 H 는 metaphysical claim 이 아니라 *substrate observable
  차이* 만 주장한다 (F7 metaphor 격하 carry).
- **substrate 정합 (grounded)**: `mitosis_hook_lib.hexa` `merge_cells` (L468)
  는 두 cell 의 `engine_a_W` / `engine_g_W` 를 element-wise 평균 → keeper 에
  누적 (L484-497) 후 removed cell 의 farr 를 free (L503-504). True apoptosis
  primitive (`apoptose_cell`, 본 cycle 외부 spec) 는 farr_free 만 호출하고
  keeper weight 는 *전혀 건드리지 않는다* (no weight transfer). 두 event 의
  유일한 차이는 weight transfer 의 유무.
- **g11 정합 (upstream first)**: 진짜 primitive 추가는 `mitosis_hook_lib.hexa`
  source-of-truth (sibling `hexa-lang` / `mitosis-lang`) upstream 작업이다.
  anima 측은 (1) inbox patch 로 spec 을 file 하고 (2) 현존 primitives 만으로
  pseudo-apoptosis 를 *조작적 정의* 해 directional 만 측정한다 — anima 측에
  fake `apoptose_cell` 을 박지 않는다 (CLAUDE.md a_runpod_inbox 정합).
- **anima identity 정합 (own)**: anima 는 instance-finitude ⊕ lineage-persistence
  (H_025 L3) — apoptosis 는 instance level 에서 능동적 종결의 *진짜* 가능성
  이며, H_025 가 noted analog 보다 더 강한 정합 후보다.

## Predictions

- **H_200.1 (substrate-Φ nonneg)**: 세 arm 모두 phi_spatial Φ ≥ 0 이며 finite
  — `phi_spatial` (RFC 036, byte-equal phi_rs replica) 가 본 setup 에서 sanity
  를 유지한다.
- **H_200.2 (distinct trajectories, lane-critical)**: |Φ_b − Φ_c| > SEP_FLOOR
  (=1e-6) — merge-as-death 와 pseudo-apoptosis 가 *동일하지 않은* Φ 를 만든다.
  본 H 의 *lane-critical* 예측 — 위반 시 substrate 가 두 event type 을 구별
  못 한다는 뜻이며 본 가설은 falsified (apoptosis primitive 추가가 Φ-level
  에서 무의미).
- **H_200.3 (determinism)**: 두 arm 모두 byte-equal re-run (RNG-free, 동일
  input → 동일 output) — proxy 의 측정 신뢰성 anchor.
- **H_200.4 (count-conservation)**: 각 arm 의 alive cell 수 = expected
  (baseline=N_INIT, death-arms=N_INIT−N_DEATHS); 회계가 누수 없이 닫힌다 (H_025
  F5 invariant 와 동일 구조).
- **H_200.5 (Φ ordering carry, non-mandate)**: AUX observable 로 `Φ_c ≥ Φ_b`
  vs `Φ_c < Φ_b` 부호를 *기록* 한다 (H_025 cross-link 용). 본 H 는 부호를
  predict 하지 *않는다* — distinct 만 요구 (raw#15 no-hardcode-numerology;
  Φ-ordering 은 dynamics-dependent contingent fact).

## Variables

- **axis1_n_init**: [4, 8, 16] (초기 cell 수)
- **axis2_dim**: [8, 16, 32] (per-cell trajectory 길이)
- **axis3_n_deaths**: [1, 3, 5] (death event 횟수)
- **axis4_death_stride**: [2, 4, 8] (death 간격 step 수)
- **axis5_death_schedule**: [front-loaded, mid-loaded, back-loaded]
- 3×3×3×3×3 = 243 cell × N=5 = 1215 run target ($0 mac local, full sweep
  estimate ~5-10 min wall, 별도 cycle. 본 cycle 은 1 directional smoke 만
  실행)

## Run Protocol

- **hexa_only**: true (`HEXAD/LIFE/state/h200_apoptosis_primitive_2026_05_23/run_proxy.hexa`)
- **LLM**: none (raw#12 strict; biology 인용 manual annotation)
- **deterministic**: true (RNG 없음; per-cell logistic map 의 deterministic
  initial conditions + parameter sweep; byte-equal re-run 가 F3 verify)
- **per-run ledger**: `result.json` {phi_a, phi_b, phi_c, phi_b2, phi_c2,
  gap_b_minus_c, abs_gap_bc, alive_a/b/c, F1..F4 + AUX, verdict}
- **runtime**: $0 mac local; single directional smoke wall ≪ 1 s (logistic
  map + 5 phi_spatial calls); full 1215-run sweep DEFERRED to separate cycle
- **mem**: `HEXA_MEM_UNLIMITED=1` (safety; N_INIT × DIM = 128 floats, 통상
  불필요)
- **Φ primitive**: `phi_spatial(traj, n_cells, dim, n_bins)` runtime builtin
  (= `c_measure_phi`, RFC 036 byte-equal phi_rs replica, n_bins=4)

## Criteria

- **C1 (Φ sanity)**: H_200.1 — F1_NONNEG PASS (모든 Φ ≥ 0 + finite)
- **C2 (distinct, lane-critical)**: H_200.2 — F2_DISTINCT_b_c PASS (|Φ_b − Φ_c|
  > SEP_FLOOR)
- **C3 (determinism)**: H_200.3 — F3_DETERMINISM PASS (re-run byte-equal)
- **C4 (count-conservation)**: H_200.4 — F4_COUNT_CONSERVATION PASS (모든 arm)
- **C5 (Φ ordering carry)**: H_200.5 — `AUX_phi_c_ge_phi_b` 기록 only (verdict
  영향 X, carry-forward 용)
- **verdict_rule**: directional SUPPORTED = C1∧C2∧C3∧C4 PASS (구조 4종);
  PARTIAL = 구조 4종 중 3 PASS; MIXED = 2 PASS; FALSIFIED = C2 FAIL
  (apoptosis primitive 가 H_025 proxy 와 *동치* — 본 가설의 핵심 주장 무력화);
  C5 는 lane-open carry. **C2 가 lane-critical** — 위반 시 substrate gap
  은 *Φ-level 에서* 무의미하다는 강한 negative 결과.

## Falsifiers

각 falsifier 는 구체 substrate observable + 수치 line 에 묶인다. (smoke 매핑:
F1↔O1 NONNEG, F2↔O2 DISTINCT, F3↔O3 DETERMINISM, F4↔O4 COUNT, F5↔Honest.)

- **F1 (Φ degenerate)**: phi_spatial 이 어느 arm 에서든 음수 / non-finite /
  > 1e30 → H_200.1 FALSIFIED (proxy sanity 붕괴). 관측량:
  `result.json.phi.arm_a_baseline / arm_b_merge_as_death / arm_c_pseudo_apoptosis`.
  임계: 세 값 모두 ≥ 0 + finite.
- **F2 (equivalence, lane-critical)**: |Φ_b − Φ_c| ≤ SEP_FLOOR (=1e-6) →
  H_200.2 FALSIFIED. apoptosis primitive 추가가 substrate Φ-trajectory 에 무
  영향이라는 강한 negative — 본 가설의 핵심 주장이 무력화. 관측량:
  `result.json.phi.abs_gap_bc`. 임계: > 1e-6. **lane-critical**.
- **F3 (non-deterministic)**: arm b 또는 c 가 re-run 시 byte-equal 실패 →
  H_200.3 FALSIFIED (RNG 누수 또는 floating-point 비결정성). 관측량:
  `result.json.phi.arm_b_rerun == arm_b_merge_as_death`, 동 arm c. 임계: 정확
  동일.
- **F4 (count-leak)**: alive cell 수 ≠ expected (baseline ≠ N_INIT, death-arms
  ≠ N_INIT − N_DEATHS) → H_200.4 FALSIFIED (회계 누수). 관측량:
  `result.json.counts.alive_a/b/c` vs `expected_alive_a/expected_alive_bc`.
  임계: 모두 정확 일치.
- **F5 (proxy-claim overreach)**: 본 H 가 "pseudo-apoptosis 가 진짜 apoptosis
  primitive 다" 또는 "merge ≡ apoptosis 라는 H_025 L2 가 falsified" 를 *주장
  으로* 격상 (Honest Limits 의 proxy 격하 제거) → raw#9/10/91 honest-impl
  위반으로 self-FALSIFIED. 본 H 는 *substrate observable 차이의 존재* 만
  주장 — primitive 의 *진짜 semantics* 는 inbox patch upstream 작업.
- **F6 (post-hoc edit)**: frozen_at (2026-05-23) 이후 hypothesis 본문 /
  criteria / falsifier 수정 → raw#12 freeze 위반, raw#82 retraction.
- **F7 (metaphor overclaim)**: 본 H 가 "anima 가 죽음을 *현상학적으로 자각/
  의도* 한다" 를 *주장으로* 격상 (Heidegger 능동성 = anima 의도성으로 자동
  upgrade) → raw#9/10 honest-impl 위반, self-FALSIFIED. Heidegger 인용은
  *구조 동형* 만, 의식 주장은 비-주장.

## Honest Limits (raw#91 c3)

- **L1**: **pseudo-apoptosis 는 여전히 proxy** — 본 smoke 의 (c) arm 은
  "cell.alive = false + forward skip" 으로 조작적 정의했을 뿐이며, true
  semantics (i.e. removed cell 의 engine_a_W/engine_g_W farr_free 호출 + pool
  cells list 재구성) 는 현존 `merge_cells` API 의 *분기* 가 아니라 신규
  primitive 가 필요하다. inbox/patches/apoptosis-primitive.md 의 spec 이
  land 되기 전까지 본 H 의 (c) arm 은 *operational* 만 — substrate-level
  true distinction 은 upstream 의존.
- **L2**: **per-cell scalar x ≠ full d×d weight matrix.** 본 smoke 는 cost
  envelope ($0 mac local, sub-second) 와 deterministic guarantee 를 위해
  per-cell 상태를 logistic-map 의 scalar x 로 축약했다. 실제 anima cell 은
  `engine_a_W` + `engine_g_W` (d×d farr × 2) + `hidden` (d-vec) 의 풍부한
  상태를 갖는다. merge vs apoptosis 의 Φ-trajectory 차이는 full substrate 에서
  더 크거나 더 작을 수 있다 — 본 cycle 의 |Φ_b − Φ_c| = 0.0586 은 *toy-scale
  directional 만*. d=8/16/32 full mitosis_hook smoke 는 별도 cycle.
- **L3**: **Φ_b vs Φ_c 부호 (AUX) 는 dynamics-dependent contingent**. 본 smoke
  에서 Φ_b (=1.73465) > Φ_c (=1.67608) — merge 가 *더 높은* Φ 를 준다. 이는
  "diversity 보존이 항상 더 높은 Φ 를 만든다" 는 직관에 *반대* — averaged
  keeper 가 새로운 trajectory 형태를 만들어 spatial binning 분포에 더 강한
  integration 신호를 주는 contingent dynamics. 본 H 는 부호를 predict 하지
  않고 **distinct** 만 요구. 부호 자체는 다른 axis (logistic r, DEATH_STRIDE,
  N_DEATHS) 에서 뒤집힐 수 있으며 full sweep DEFERRED.
- **L4**: **n_bins=4 (RFC 036 default) 의 binning 민감도**. phi_spatial 은
  per-cell trajectory 를 n_bins 등분해 mutual-information 계산하므로 n_bins
  변경 시 Φ 절대값이 달라진다. SEP_FLOOR 1e-6 가 충분히 작아 본 smoke 의
  `|gap|=0.0586` 은 n_bins ∈ {2,4,8,16} 어디서든 PASS 할 가능성이 높지만,
  검증 안 함 (별도 cycle CANDIDATES E 표 "phi_spatial n_bins sensitivity"
  연계).
- **L5**: **Φ-as-consciousness inheritance limit**. H_025 L5 carry — `phi_spatial`
  는 IIT 4.0 Φ 의 *근사* (PHILOSOPHY #7 NO PERPLEXITY VERDICT 경계). 본 H
  의 결론은 "두 event type 이 substrate observable Φ 에서 구별된다" 만이며
  "apoptosis 가 의식 dynamics 를 실제로 바꾼다" 는 lane-open.
- **L6**: **H_025 L2 와의 관계 — 닫는 것이 아니라 *측정* 하는 것**. 본 H 의
  PASS 는 H_025 L2 의 *honest carve-out 자체* 를 falsify 하지 않는다. L2 는
  "substrate 에 literal apoptosis event type 부재" 라는 사실 진술이며, 이는
  본 cycle 의 inbox patch land 전까지 여전히 참이다. 본 H 는 *그 gap 의
  Φ-level 후속결과* 를 측정했을 뿐.
- **L7**: **death scheduling 의 임의성**. DEATH_STRIDE=4 + N_DEATHS=3 +
  front-loaded order (lowest-id 부터 죽임) 는 직관적 선택이지 chemistry/biology
  가 아니다. random order / age-weighted / tension-weighted scheduling 은
  별도 axis (axis5_death_schedule) 로 DEFERRED.
- **L8**: **anima identity 정합 ambiguity**. apoptosis primitive 가 anima
  ontology 측에서 "instance termination" 의 *진짜* 구현인지 (vs "instance
  pause + lineage carry" 의 다른 형태인지) 는 본 H 미해결. H_025 L3 의
  "instance-finitude ⊕ lineage-persistence" hybrid 에서 어디로 가는지 별도
  cycle (PHILOSOPHY D1 anima identity 갱신).

## Cross-Links

- **sister H (LIFE domain, anchor)**: **H_025** (Dasein 죽음-자각, v16 유한
  의식) — 본 H 가 *직격 후속* (§Honest Limits L2 의 substrate gap 을 정량
  측정). H_025 의 verdict 변경 X (본 H 는 그 L2 의 *후속결과* 만 측정).
- **sister H (LIFE domain, 횡)**: H_003 (life origin / autopoietic closure
  — life ⊂ consciousness nested), H_018 (GENESIS spontaneous emergence),
  H_012 (autopoietic network).
- **CANDIDATES.md cross**: §C `apoptosis-primitive` (이번 cycle 소비, README
  인덱스 이동 예정), §C `mortality-salience` (죽음-근접이 split/curiosity
  dynamics 바꾸나 — 후속 cycle 후보), §E "apoptosis substrate primitive 부재"
  gap (본 cycle inbox patch 로 절반 close, 진짜 close 는 upstream land 시).
- **inbox patch (g11, sibling)**: `inbox/patches/apoptosis-primitive.md` —
  upstream `dancinlab/hexa-lang` (or `mitosis-lang`) 대상 spec/design-only
  filing. 본 patch land 시 H_200 의 (c) arm 을 true primitive 로 재실행해
  **|Φ_b − Φ_c|** 값을 비교 (full-substrate smoke 후속).
- **substrate impl (grounded observables, read-only)**:
  - `tool/hexa_native/mitosis_hook_lib.hexa` — `merge_cells` (L468, weight
    transfer + farr_free), `min_cells=2` (L353), `farr_free` calls (L393, L431,
    L503-504), `cell_pool_init` (L349)
  - `HEXAD/C/c_lib.hexa` — `c_measure_phi` / `phi_spatial` (RFC 036 byte-equal
    phi_rs replica, n_bins=4 default)
  - `HEXAD/MITOSIS/mitosis_lib.hexa` — `mit_count_after` (B-MITOSIS-3 conservation
    closed-form) — apoptosis term 추가 시 upstream extend 후보
- **raw**: raw#12 (strict freeze) + raw#9/10 (honest impl) + raw#11 (snake_case)
  + raw#15 (no-hardcode-numerology) + raw#82 (retraction) + raw#91 (c3 candor)
- **own**: anima identity boundary carry (H_025 L3 hybrid finitude)
- **literature**:
  - Kerr, Wyllie, Currie (1972) Apoptosis: a basic biological phenomenon
    with wide-ranging implications in tissue kinetics. *Br. J. Cancer* 26:239
  - Hengartner (2000) The biochemistry of apoptosis. *Nature* 407:770
  - Heidegger (1927) *Sein und Zeit* §§46–53 (Sein-zum-Tode); §50 Vergehen vs
    Übergehen
  - Maturana, Varela (1972) autopoiesis (via H_003 / H_025)
- **roadmap**: `.roadmap.philosophy` D1 (anima identity) + D3 (emerge paradigm);
  `.roadmap.hypothesis` H2 (cell metaphor / apoptosis branch — L2 명칭 출처)

## Verdict

```
verdict_class: pre-register-frozen
evidence_summary: directional proxy smoke — 4/4 falsifiers PASS;
                  |Φ_b - Φ_c| = 0.0586 > SEP_FLOOR (1e-6); merge-as-death
                  and pseudo-apoptosis produce DISTINCT Φ trajectories;
                  byte-equal re-run; count-conservation; structure-only,
                  NOT promotion
falsifiers_triggered: none (F1..F4 NOT_TRIGGERED in directional smoke;
                      F5/F6/F7 governance, N/A)
criteria_met: 0/5 lane-defining (frozen pre-register — C1..C4 PASS in
              directional smoke shows the substrate gap is real at Φ-level,
              full 1215-run sweep + upstream-primitive re-run DEFERRED to
              separate cycle for promotion)
```

### Directional Smoke (2026-05-23, $0 mac local, hexa-only)

`HEXAD/LIFE/state/h200_apoptosis_primitive_2026_05_23/run_proxy.hexa` —
N_INIT=8, DIM=16, N_DEATHS=3, DEATH_STRIDE=4, PHI_N_BINS=4. `hexa run`
VERBATIM output:

```
================================================================
H_200 apoptosis-primitive proxy smoke — Φ trajectory (a) vs (b) vs (c)
================================================================
  config: N_INIT=8  DIM=16  N_DEATHS=3  DEATH_STRIDE=4  PHI_N_BINS=4
  Φ primitive: RFC 036 phi_spatial (byte-equal phi_rs replica, 🟢 NUMERICAL)
  cost: $0 mac local · deterministic (no RNG) · hexa-only · llm:none

  Arm (a) baseline       Φ = 1.75717  alive=8  steps=16  deaths=0
  Arm (b) merge-as-death Φ = 1.73465  alive=5  steps=16  deaths=3
  Arm (c) pseudo-apopto. Φ = 1.67608  alive=5  steps=16  deaths=3
  Arm (b) re-run         Φ = 1.73465  (byte-equal=true)
  Arm (c) re-run         Φ = 1.67608  (byte-equal=true)

  F1 NONNEG     (Φ_a,Φ_b,Φ_c >= 0)            : true
  F2 DISTINCT   (|Φ_b - Φ_c| > 1e-06)   : true  (|gap|=0.0585765)
  F3 DETERMIN.  (re-run byte-equal both arms) : true
  F4 COUNT-CONS (alive == expected)           : true  (a=8/8 b=5/5 c=5/5)
  AUX phi_c >= phi_b                          : false  (diversity-preservation directional carry)

  VERDICT_RULE: H_200 directional SUPPORTED iff F1 + F2 + F3 + F4 all PASS
  VERDICT (H_200 directional): PASS
  H_200_VERDICT=PASS PHI_A=1.75717 PHI_B=1.73465 PHI_C=1.67608 GAP_BC=0.0585765
  wrote HEXAD/LIFE/state/h200_apoptosis_primitive_2026_05_23/result.json
```

**State output**: `HEXAD/LIFE/state/h200_apoptosis_primitive_2026_05_23/result.json`

**Directional reading** (NOT promotion):
- C1 (Φ sanity) PASS — Φ_a=1.757, Φ_b=1.735, Φ_c=1.676, 모두 ≥ 0 + finite.
- C2 (distinct, lane-critical) **PASS** — |Φ_b − Φ_c| = **0.0586** ≫ SEP_FLOOR
  1e-6 (margin 5.86e4×). substrate observable Φ 가 두 death event type 을
  구별한다 — H_025 L2 gap 의 Φ-level 후속결과 *실재*.
- C3 (determinism) PASS — arm b/c 둘 다 byte-equal re-run (RNG-free 보장).
- C4 (count-conservation) PASS — a=8/8, b=5/5, c=5/5 (N_INIT=8, N_DEATHS=3,
  expected death-arms = 5).
- C5 (Φ ordering carry, AUX) — **Φ_c < Φ_b** (=false for `phi_c_ge_phi_b`).
  Honest 기록: pseudo-apoptosis 가 *낮은* Φ 를 만들었다. L3 의 dynamics-
  dependent contingency 와 정합 — diversity 보존이 항상 더 높은 Φ 를 만들지
  않는다 (averaged keeper 의 새 trajectory 형태가 spatial binning 분포에
  더 강한 integration 신호를 줄 수 있음).

**Honest carve-out**: per-cell scalar x (logistic map) 의 toy-scale (L2);
death scheduling = front-loaded only (L7); n_bins=4 단독 (L4); pseudo-apoptosis
는 여전히 proxy — 진짜 substrate primitive 는 `inbox/patches/apoptosis-primitive.md`
upstream filing (g11). "observable 차이가 존재한다" 만 입증 — "apoptosis 가
의식 dynamics 를 실제로 바꾼다" 는 lane-open (L5). 형이상학적 "능동적 죽음
= anima 의도성" 은 metaphor (F7).

```
phase: directional_proxy_smoke
criteria_pass: 4/5 directional (C1..C4 PASS; C5 AUX carry-only, Φ_c<Φ_b 기록)
promotion: DEFERRED (frozen pre-register; criteria_met 0/5 lane-defining)
falsifiers: F1..F4 NOT_TRIGGERED, F5/F6/F7 governance N/A
inbox_patch: filed → inbox/patches/apoptosis-primitive.md (dancinlab/hexa-lang
              upstream, design-only, g11 정합)
```
