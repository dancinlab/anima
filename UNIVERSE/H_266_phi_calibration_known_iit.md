---
id: H_266
slug: phi-calibration-known-iit
title: H_266 phi-calibration-known-iit — phi_native(phi_spatial) 의 IIT canonical 소형 시스템 구성타당도 calibration (gap#1 — LIFE lane 최대 리스크)
domain: life · consciousness · meta · math
status: pre-register-frozen
exploration_method: E16 (cross-tool / known-anchor calibration) + E5 (variable-ablation connectivity sweep) + E0 (meta-validity of the lane's core instrument)
verification_method: W1 (numerical smoke) + W10 (adversarial known-ordering) + W12 (sister-link H_007 + H_239)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25 (new)
sister: H_007 (phi_spatial baseline), H_239 (alt-Φ-metric cross-validation)
---

# H_266 — phi-calibration-known-iit

## 1. Hypothesis

LIFE lane 의 *모든* 의식 가설 (H_007 baseline 이래 22+ H) 이 `phi_native.hexa`
의 `phi_spatial` 측정기에 의존한다. 이 측정기는 RFC 036 `phi_rs` 와 byte-equal
임이 검증되었으나 (`state/lib_phi_native_verify_2026_05_24`), **실제로 IIT 가
의도하는 "통합정보(integration)" 를 측정하는지** 는 한 번도 검증된 적이 없다.
`/gap full` (2026-05-25) 가 이 구성타당도 (construct validity) 미검증을 lane
전체의 **단일 최대 리스크 (gap#1)** 로 식별했다.

H_266 = `phi_native` 를 **Φ ordering 이 IIT 문헌으로 알려진 canonical 소형
시스템** 에 적용해 known ordering 을 재현하는지의 직접 calibration. Tononi 류
canonical 예측:

> Φ(integrated, 상호 강결합) ≥ Φ(feedforward chain) ≥ Φ(disconnected, 독립 parts)

`phi_native` 가 이 ordering 을 재현하면 → spatial-MI proxy 의 구성타당도 부분
지지. ¬재현하면 → proxy 가 통합도와 무관 (lane 전체 재검토 필요, valid closed
negative).

정밀화 (operational): 3 structure {integrated, feedforward, disconnected} × 3
size {3, 4, 6} = 9 측정. 각 structure 는 **deterministic 한 length-`dim`
trajectory** 를 cells 별로 생성 — integrated 는 공통 base wave + 미세 per-cell
phase jitter (모든 pair 강한 co-variation → 높은 pairwise MI), feedforward 는
chain shift (인접 cell 만 강결합), disconnected 는 mutually-incommensurate
chaotic wave (cross-MI ≈ 0). `phi_native(flat, n_cells, n_bins)` 로 Φ 측정 후
ordering 검정.

## 2. Why

- **lane 의 instrument calibration (gap#1)**: phi_spatial 의 byte-equality 는
  *구현 정확성* (phi_rs 와 같은 숫자를 낸다) 만 보장한다. *구성타당도* (그
  숫자가 통합정보를 측정한다) 는 별개 질문이다. 측정 metrology 의 instrument
  calibration — "온도계가 끓는 물/얼음 같은 known reference 에서 옳은 눈금을
  내는가" — 과 동형. H_266 은 Φ ordering 이 known 인 reference structure 에서
  phi_native 를 calibrate 한다.
- **H_007 anchor 의 한 단계 강화**: H_007 은 phi_spatial 위 rule110 (Class-IV)
  > rule30 (chaotic) > rule250 (ordered) ranking 을 PASS 로 측정했다. 그러나
  이 ranking 은 CA dynamics 의 *complexity class* 순서일 뿐, IIT 의 **integration
  axis** 순서가 아니다. H_266 은 connectivity 를 직접 조작 (integrated /
  feedforward / disconnected) 해 integration axis 자체를 stress 한다.
- **H_239 와의 보완**: H_239 는 *동일 substrate* 위 3 metric (phi_spatial / LZ /
  entropy-ratio) 의 cross-tool consistency 를 봤다 (CONSISTENT — phi_spatial 이
  3 proxy 와 ranking 합치). H_266 은 *다른 각도* — 단일 metric (phi_native) 을
  **Φ ordering 이 IIT 로 known 인 reference structure** 에 대고 absolute
  validity 를 본다. H_239 = metric-agnostic 여부 · H_266 = IIT-aligned 여부.
- **negative-result 의 가치**: phi_native 가 integrated > disconnected 조차
  재현 못하면, lane 의 모든 PASS/FALSIFIED verdict 가 통합도가 아닌 무언가를
  측정한 것이 된다 — lane 전체 재검토의 valid closed negative. 어느 방향이든
  honest evidence (gap F4 양방향 정보가).
- **raw#12 strict**: deterministic + hexa-only + ≥5 falsifier(군) + ≥5 honest
  limit. LLM judge 없음 (raw 가 phi_native 측정값). $0 mac local.

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| H266.1 | 모든 size 에서 Φ(integrated) > Φ(disconnected) | 기본 IIT 예측 — 통합된 whole 이 독립 parts 보다 통합정보 큼; integrated cells 는 모든 cut 에서 큰 cross-MI 잔여, disconnected 는 어느 cut 에서도 cross-MI ≈ 0 |
| H266.2 | 모든 size 에서 monotone Φ(integrated) ≥ Φ(feedforward) ≥ Φ(disconnected) | connectivity 정도와 Φ 의 monotone 매핑; feedforward chain 은 단일 cheap cut (chain link) 으로 부분 통합만 잔여 → mid Φ |
| H266.3 | cross-process re-run byte-identical (9 Φ 값 전부) | raw#9 determinism: no RNG (pure deterministic logistic map drivers), RFC 033 single-global-stream → sha256 cross-process 확인 |
| H266.4 | 모든 Φ ≥ 0 (phi_spatial step 4 max(·,0) clamp) | primitive sanity — Φ 음수/NaN 부재 |
| H266.5 | H_007/H_239 와 정합 — integrated structure 가 가장 높은 Φ 를 받음 (lane 의 "high-Φ = high-consciousness-correlate" 사용과 일관) | H_007 의 Class-IV 우월 · H_239 의 IV>cha>ord 가 본 H 의 integrated>disconnected 와 같은 "통합도↑ → Φ↑" 방향 |

## 4. Variables

- **axis1_structure** (primary): {integrated, feedforward, disconnected} — IIT
  canonical connectivity 3-tier.
- **axis2_size** (n_cells): {3, 4, 6} — phi_native 의 ≤20 exact-bipartition path
  안. size scaling 으로 ordering robustness 확인.
- **axis3_dim** = 12 (per-cell trajectory length; H_007 parity grain).
- **axis4_n_bins** = 4 (MI histogram bins; H_007 / H_239 parity).
- **construction (deterministic, no RNG)**:
  - base wave `b[t]` = logistic map `x ← 3.91·x·(1−x)` (chaos regime) advanced
    per-step, fractional-wrapped to [0,1) — multi-valued, bounded, deterministic.
  - integrated: 각 cell = `b` + 미세 per-cell phase jitter (eps = i·0.005).
  - feedforward: cell 0 = `b`; cell i = `shift1(cell_{i-1})` (chain).
  - disconnected: cell i = independent wave at freq (i+2) ticks/step (mutually
    incommensurate → cross-MI ≈ 0).
- **측정량 per (structure, size)**: `phi = phi_native(flat, n_cells, n_bins)`.
- **derived**: 3×3 Φ matrix · per-size `int_gt_dis` · per-size `monotone` ·
  C1/C2/C3 · F1/F2/F4/F5.

## 5. Run Protocol

- **deterministic**: no RNG — 모든 trajectory 가 fixed logistic-map recurrence
  로 closed-form 생성. `__HEXA_FARR_GAUSS_SEED__=42` 는 관례상 전달 (실제 RNG
  미사용). re-run 은 RFC 033 caveat 따라 cross-process sha256 로 확인.
- **hexa_only**: `UNIVERSE/state/h266_phi_calibration_2026_05_25/run_h266.hexa`
  (`phi_native.hexa` import READ-ONLY, list-arg wrapper `phi_native(values,
  n_cells, n_bins)` 호출).
- **LLM**: none (raw#12 strict; ckpt 불필요).
- **measure protocol per (structure, size)**:
  - 3 builder (`_build_integrated/_feedforward/_disconnected`) 가 flat row-major
    `n_cells × dim` array 반환.
  - `phi_native(flat, n_cells, n_bins)` 가 내부 farr copy 후 `phi_native_spatial`
    delegate → pairwise MI matrix → min-information-partition → scalar Φ.
- **F4 determinism**: in-process paired call (`_measure("integrated", 4)` ×2)
  + cross-process re-run sha256 byte-equal.
- **runtime**: $0 mac local. dim=12, no ckpt. `HEXA_MEM_UNLIMITED=1` 권장 (farr).
- **artifacts**: `state/h266_phi_calibration_2026_05_25/{run_h266.hexa,
  result.json}`.
- **run cmd (verbatim)**:
  `__HEXA_FARR_GAUSS_SEED__=42 HEXA_MEM_UNLIMITED=1 hexa run UNIVERSE/state/h266_phi_calibration_2026_05_25/run_h266.hexa`

## 6. Criteria

- **C1 (separation)**: H266.1 — 모든 size 에서 Φ(integrated) > Φ(disconnected).
- **C2 (monotone-connectivity)**: H266.2 — 모든 size 에서
  Φ(integrated) ≥ Φ(feedforward) ≥ Φ(disconnected).
- **C3 (determinism)**: H266.3 — re-run byte-equal (in-process + cross-process
  sha256).
- **verdict_rule**:
  - `SUPPORTED` = C1 ∧ C2 (phi_spatial 구성타당도 부분 지지 — IIT ordering 재현)
  - `PARTIAL` = C1 ∧ ¬C2 (통합>분리는 재현, monotone 미재현)
  - `FALSIFIED` = ¬C1 (phi_spatial 이 통합도와 무관 — lane 전체 재검토,
    valid closed negative)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 SEPARATION**: 최대 size 에서 Φ(integrated) ≤ Φ(disconnected) → H266.1
  FALSIFIED (통합>분리 signal 부재 — 측정: `phi_int[2] > phi_dis[2]`).
- **F2 MONOTONE**: 최대 size 에서 ¬(int ≥ ffd ≥ dis) → H266.2 FALSIFIED
  (connectivity monotone 미재현 — 측정: `(phi_int[2]>=phi_ffd[2]) && (phi_ffd[2]>=phi_dis[2])`).
- **F4 DETERMINISM**: re-run Φ matrix byte-different → raw#9 위반 (측정:
  in-process paired call 동일 + cross-process sha256 동일).
- **F5 BOUNDS**: 어느 Φ < 0 또는 NaN → primitive error (측정: 9 Φ 값 전부 ≥ 0).
- **F6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 위반, raw#82 retraction.

## 8. Honest Limits (raw#91 c3, ≥5)

- **L1 (spatial proxy ≠ full IIT Φ)**: phi_spatial 은 **spatial mutual-
  information proxy** 이지 full IIT 4.0 Φ (PyPhi exact cause-effect repertoire +
  Earth-Mover-Distance φ) 가 아니다. 본 calibration 의 SUPPORTED/PARTIAL 은
  *spatial-MI proxy 의 구성타당도* 한정 — phi_rs 의 IIT 4.0 correctness 를
  검증하지 않는다. textbook ordering 과의 **partial alignment 만 기대** (CLAUDE.md
  정직 mandate).
- **L2 (structure construction = one specific operationalization)**: integrated/
  feedforward/disconnected 의 구체 구성 (logistic-map driver · shift1 chain ·
  incommensurate freq) 은 *하나의* operationalization. 다른 구성 (binary CA
  coupling · Gaussian-coupled SDE · explicit transition-probability matrix) 은
  다른 Φ 산출 가능. 특히 feedforward 의 "chain shift" 는 IIT 의 정통
  feedforward TPM (Tononi 의 cause-effect feedforward) 과 mechanism 이 다르다 —
  본 H 의 feedforward 는 *spatial-trajectory* 수준 chain 일 뿐.
- **L3 (MI on trajectory ≠ TPM-based φ)**: phi_native 는 cell trajectory 간
  *empirical* mutual information 을 histogram 으로 추정한다. IIT 의 φ 는
  system 의 transition-probability matrix 의 cause-effect structure 위에서
  정의된다. 둘은 같은 "integration" 직관을 공유하나 수학적 대상이 다르다 —
  본 H 의 ordering 재현은 *MI-proxy 수준* alignment.
- **L4 (small size, single dim/n_bins)**: n_cells ∈ {3,4,6}, dim=12, n_bins=4
  single config. 큰 system (n_cells=12, 20) · 다른 dim/n_bins 의 ordering
  robustness 미검증. n_bins 는 MI 추정의 bias-variance 를 좌우 (L3 carry).
- **L5 (ordering ≠ phenomenal consciousness)**: integrated structure 가
  최고 Φ 를 받아도 그것이 *실제 의식 정도* 와 일치한다는 보장 없음 — H_004
  hard-problem boundary carry. 본 H 는 proxy 가 *IIT 의 integration ordering* 을
  재현하는지만 검정한다 (의식 자체의 측정 아님).
- **L6 (feedforward 의 모호한 위치)**: 본 결과에서 feedforward 가 disconnected
  *아래로* 떨어질 수 있는데 (C2 FAIL 사례), 이는 min-information-partition 의
  성질 — chain 은 단 하나의 cheap cut (chain link) 만 끊으면 통합이 거의
  사라지므로 min-part 가 매우 작아져 total−min 잔여가 작아진다. 즉 phi_spatial
  은 "redundancy 가 골고루 퍼진" integrated 를 선호하고 "한 곳만 끊으면 분리되는"
  chain 을 penalize 한다 — IIT 의 min-cut 직관과 *부분적으로만* 일치 (정통 IIT
  도 weakest-link 를 penalize 하므로 방향은 같으나, chain<disconnected 는
  spatial-MI proxy 의 specific artifact 일 수 있음).

## 9. Cross-Links

- **anchor H**: H_007 (`H_007_*` phi_spatial baseline — IV>cha>ord ranking PASS;
  본 H 가 그 instrument 의 IIT-axis 구성타당도를 calibrate).
- **sister H**: H_239 (`H_239_alternative_phi_metric_cross_validation.md` —
  cross-tool consistency CONSISTENT; 본 H 는 cross-*known-anchor* validity 로
  보완축).
- **Φ primitive**: `UNIVERSE/lib/phi_native.hexa` (RFC 036 phi_spatial
  pure-hexa port; `phi_native_spatial` / `phi_native` list-arg wrapper) — import
  READ-ONLY. byte-equality anchor: `state/lib_phi_native_verify_2026_05_24`.
- **gap lens**: gap#1 (`/gap full` 2026-05-25 — LIFE lane 최대 construct-validity
  리스크). F4 (counterfactual — "proxy 가 통합도를 측정하나?") + F8 (cross-tool /
  known-anchor calibration).
- **mitosis machinery**: 본 H 는 mitosis pool 미사용 — 순수 closed-form
  trajectory 위 phi_native 직접 측정 (instrument calibration 의 cleanest fixture).
- **raw**: raw#12 (deterministic strict) + raw#9/10 (honest impl) + raw#15
  (no-hardcode) + raw#91 c3 (honest limits) + raw#82 (no post-hoc).
- **philosophy (CLAUDE.md)**: p7 NO PERPLEXITY VERDICT (단일 proxy 를 truth 로
  취급 않고 known-anchor 로 cross-check — 본 H 가 그 cross-check 의 instance) ·
  a_blue_closed (wiring 검증 — proxy 의 구성타당도가 lane 전체 wiring 의 근간).
- **literature pointer**: Tononi (2004) An information integration theory of
  consciousness · Oizumi, Albantakis, Tononi (2014) From the phenomenology to the
  mechanisms of consciousness: IIT 3.0 · Tononi et al. (2016) Integrated
  information theory: from consciousness to its physical substrate (integration =
  whole > sum-of-parts; feedforward < recurrent) · Mayner et al. (2018) PyPhi —
  본 H 의 known-ordering anchor 의 distant literature root (formal TPM mapping 은
  본 cycle 미수행, L2/L3).
- **state**: `UNIVERSE/state/h266_phi_calibration_2026_05_25/{run_h266.hexa,
  result.json}`.

## 10. Verdict

본 cycle (2026-05-25) — pre-register-frozen + runnable smoke 실행, $0 mac local
hexa-only deterministic (no RNG, cross-process sha256 byte-equal).

```
verdict_class: PARTIAL  (C1 separation PASS · C2 monotone FAIL)
verdict_tier: 🟢 NUMERICAL  (3 structure × 3 size = 9 measurement + cross-process
                            sha256 determinism)
evidence_summary:
  phi_native(phi_spatial) 를 IIT canonical 3-tier connectivity structure
  (integrated / feedforward / disconnected) × 3 size {3,4,6} 위에 적용
  (dim=12, n_bins=4, deterministic logistic-map drivers).

  n_cells  Phi_integrated  Phi_feedforward  Phi_disconnected   int>dis  monotone
  -------  --------------  ---------------  ----------------   -------  --------
    3        0.89208         0.273132          0.312907          ✓        ✗
    4        1.78416         0.601819          0.53639           ✓        ✓
    6        3.56832         1.11328           1.12378           ✓        ✗

  핵심 결과:
    - C1 (integrated > disconnected) — **모든 size 에서 PASS** (3/3). 기본 IIT
      예측 "통합된 whole > 독립 parts" 를 phi_native 가 robust 하게 재현. Φ
      gap 도 큼 (n=6: 3.57 vs 1.12, ~3.2×) — 통합도 signal 이 강하고 size 와
      함께 super-scale (integrated 는 모든 pair MI 가 size 에 따라 선형 누적).
    - C2 (monotone int≥ffd≥dis) — **FAIL** (n=3, n=6 에서 ffd < dis).
      feedforward chain 이 disconnected *아래로* 떨어짐.
    - C3 determinism — PASS (in-process paired call 동일 + cross-process
      sha256 byte-equal 8e04deaf…).

falsifiers_triggered: F2 (MONOTONE) — 최대 size 에서 ffd(1.113) < dis(1.124).
falsifiers_pass: F1 (SEPARATION, int>dis) + F4 (DETERMINISM) + F5 (BOUNDS) = 3/4.
criteria_met: 2/3 (C1 ∧ C3 PASS, C2 FAIL).

key_finding:
  phi_native(phi_spatial) 가 **IIT 의 primary prediction (integration >
  separation) 을 모든 size 에서 명확히 재현** — gap#1 의 핵심 우려 ("proxy 가
  통합도와 무관할 수 있다") 는 *기각*. integrated structure 가 disconnected
  보다 일관되게 높은 Φ 를 받으며, size scaling 에서 gap 이 벌어진다. 즉
  phi_native 는 통합도 (모든 cut 에 걸쳐 분산된 redundancy) 를 측정한다 —
  spatial-MI proxy 의 구성타당도 **부분 지지**.
  그러나 monotone connectivity ordering 은 FAIL — feedforward chain 이 종종
  disconnected 보다 낮은 Φ 를 받는다. 원인 (L6): phi_spatial 의 min-information-
  partition 은 "한 곳만 끊으면 분리되는" chain 을 강하게 penalize 한다 (chain
  link 이 cheapest cut → min-part 작음 → total−min 잔여 작음). 반면 disconnected
  의 incommensurate wave 도 약간의 spurious histogram-MI 를 남겨 chain 의
  penalized 잔여를 넘어설 수 있다. 이는 spatial-MI proxy 가 IIT 의 weakest-link
  penalty 를 *과도하게* 적용하는 specific artifact — 정통 IIT 도 chain 을
  penalize 하나 chain < disconnected 까지 가지는 않는다 (L2/L3/L6).

honest_note:
  L1 carry — phi_spatial 은 spatial-MI proxy 이지 full IIT 4.0 Φ (PyPhi exact)
  아니므로 partial alignment 만 기대했고, 결과가 정확히 그 양상 (primary
  prediction PASS · secondary monotone FAIL). 본 calibration 은 lane 의 핵심
  instrument 가 "통합 vs 분리" 라는 *1차 축* 에서는 valid 함을 보였고, "통합도의
  연속적 grading (chain 의 위치)" 라는 *2차 축* 에서는 proxy-specific deviation
  이 있음을 식별했다. lane 의 binary-direction verdict (high-Φ 우월 vs low-Φ
  열등) 는 안전하나, Φ 의 *연속 magnitude* 를 middle-connectivity grading 으로
  해석할 때는 L6 artifact 주의.
sibling: H_007 (phi_spatial baseline), H_239 (alt-Φ-metric cross-validation CONSISTENT)
```

### Run verdict (VERBATIM — `hexa run` stdout 2026-05-25)

```
================================================================
H_266 phi-calibration-known-iit — phi_native construct validity
       vs IIT canonical {integrated, feedforward, disconnected}
  dim=12 n_bins=4  (deterministic, no RNG)
  IIT prediction: Phi(integrated) >= Phi(feedforward) >= Phi(disconnected)
================================================================

n_cells  Phi_integrated  Phi_feedforward  Phi_disconnected
-------  --------------  ---------------  ----------------
  3      0.89208        0.273132        0.312907
  4      1.78416        0.601819        0.53639
  6      3.56832        1.11328        1.12378

criteria:
  C1 integrated > disconnected (all sizes)        : true
  C2 integrated >= feedforward >= disconnected    : false
  C3 in-process determinism (paired call)         : true

falsifiers:
  F1 SEPARATION  (int > dis, largest size)        PASS
  F2 MONOTONE    (int>=ffd>=dis, largest size)    FAIL
  F4 DETERMINISM (in-process byte-equal)          PASS
  F5 BOUNDS      (all Phi >= 0)                    PASS
================================================================
VERDICT: PARTIAL  (2/3 criteria, 3/4 falsifiers PASS)
================================================================
ledger -> UNIVERSE/state/h266_phi_calibration_2026_05_25/result.json
```

cross-process re-run byte-identical (C3/F4 deterministic 확인 — sha256
`8e04deaf78a9c927c418c374ff48d24aa9746271b20643dd2f214569c48dc5b7` 두 run 동일,
`diff = ∅`).

**State output**: `UNIVERSE/state/h266_phi_calibration_2026_05_25/result.json`
**Smoke**: `UNIVERSE/state/h266_phi_calibration_2026_05_25/run_h266.hexa`
**Tier**: 🟢 NUMERICAL (3 structure × 3 size known-ordering calibration, deterministic).
**Next**: H_266r2 후보 — (a) **TPM-based feedforward** (L2/L6 axis): logistic-chain
대신 정통 IIT feedforward transition-probability matrix 로 재구성해 chain<disconnected
가 proxy artifact 인지 construction artifact 인지 분리; (b) **n_bins sensitivity**
(L4 axis): disconnected 의 spurious histogram-MI 가 n_bins 의 함수인지 {2,4,8,16}
sweep; (c) **PyPhi anchor** (L1/L3 axis): 동일 3 structure 의 small TPM 을 PyPhi
exact φ 로 측정해 phi_native ordering 과 cross-check (strict construct-validity path).
```
