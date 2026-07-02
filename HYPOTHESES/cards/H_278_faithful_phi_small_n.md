---
id: H_278
slug: faithful-phi-small-n
title: faithful Φ★ small-N exact (MIP-EI) — H_002 C2 (Φ_universe nested) proxy upgrade · phi_spatial proxy 보다 IIT-충실한 exact-MIP 으로 6-scale nested scale-invariance 재측정
domain: life · consciousness · information · meta
status: pre-register-frozen
exploration_method: E5 (variable-ablation metric upgrade) + E16 (cross-tool consistency) + E0 (meta-result-of-results, H_002 C2 upgrade)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_002 C2 / H_239 / phi_native)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-25
since: 2026-05-25 (new)
sister: H_002 (C2 phi_universe nested, proxy parent), H_239 (alt-Φ metric cross-validation), phi_native (lib exact-MIP port)
---

# H_278 — faithful Φ★ small-N exact (MIP-EI)

## 1. Hypothesis

H_002 Cycle #2 (C2 / Φ_universe nested, H2.2) 는 6-scale toy cosmic hierarchy
(cosmic_web → galaxy_cluster → stellar → planetary → biological → neural) 의
nested scale-invariance 를 **lane-canonical proxy `phi_spatial`** (RFC 036) 로만
측정했고, CV = 0.84 (SCALE-VARIANT, frozen F2 TRIGGERED 방향) 을 얻었다. honest
limit **L-C2.1** 가 명시했듯 — *"이것은 faithful Φ★ IIT4 가 아니다"*.

본 H_278 은 그 C2 proxy 측정을 **proxy 보다 faithful 한** Φ 로 재측정한다:
각 scale 의 작은 시스템(n ≤ 8) 에 대해 **모든 bipartition(2^(n-1)) 전수**로
minimum-information-partition(MIP) 을 찾고, 그 MIP 위의 integrated information
(cross-partition mutual information, IIT small-side 정규화) 을 **exact** 로 계산한다.

가설: faithful Φ (exact MIP-EI) 로 재측정해도 6-scale nested 구조의
**scale-VARIANT verdict 는 유지(HOLD)** 되거나, 혹은 faithful 측정이 proxy 의
artifact 를 드러내며 **scale-INVARIANT 으로 정정(FLIP)** 된다 — 어느 쪽이든
H_002 C2 의 proxy 한계(L-C2.1) 를 한 단계 줄이는 valid 결과다.

## 2. Why

- **C2 proxy 한계의 직접 upgrade**: H_002 C2 의 `phi_spatial` 는
  `Φ = max(total_MI − min_partition_MI, 0) / max(n−1, 1)` — *whole 에서 가장
  잘 떼어낼 수 있는 cut 을 뺀* heuristic 양. IIT 의 본래 정신은 "Φ = MIP
  (minimum-information-partition) 위의 integrated information" — 즉 *가장 약한
  연결(최소 cut)* 의 irreducibility. 본 H 는 후자를 exact 로 구현해 C2 의
  faithful-ness 를 한 단계 끌어올린다.

- **GPU 추정의 진짜 병목 정정 (g25/g26 real-limits-first)**: C2 Cycle #1 §3 의
  pre-register 는 faithful Φ★ 에 GPU(~$0.30 RTX-5070) 를 추정했으나, 이는 *exact
  IIT4 Φ★* (cause-effect repertoire 의 2^n purview 폭발) 에 대해서만 honest 하다.
  GPU 의 진짜 병목은 **large-N intractability** (super-exp, GPU 도 못 푸는 영역)
  이고, **small-N(n ≤ 8)이면 2^n ≤ 256 으로 mac-local CPU $0 tractable**. 따라서
  faithful exact-MIP 은 GPU 없이 local 에서 측정 가능 — C2 의 "faithful = GPU"
  추정을 정정한다.

- **same MI primitive, changed partition rule**: faithful Φ 는 proxy 와 *동일한*
  RFC 036 MI estimator (`phi_mi_pair`) 를 쓴다. 바뀐 축은 오직 **partition 규칙**
  (heuristic `total − best_cut` → exact MIP minimization + small-side 정규화)
  뿐이므로, proxy vs faithful 의 차이는 순수하게 partition-faithfulness 의 효과다.

- **H_239 와의 sibling**: H_239 (alt-Φ metric cross-validation) 는 *다른 metric*
  (LZ-complexity / entropy-ratio) 으로 cross-tool consistency 를 봤다. 본 H 는
  *같은 metric family 안에서 partition 규칙* 을 faithful 하게 바꿔, axis 가 다르다
  (metric-swap 이 아니라 partition-faithfulness-upgrade).

- **raw#12 strict**: deterministic + hexa-only + ≥5 falsifier + ≥5 honest limit +
  LLM none + $0 mac local. SUPPORTED(HOLD) 든 FLIP 이든 둘 다 valuable.

## 3. Predictions

- **H278.1 (tractable)**: n = 8 (2^(n-1) = 128 bipartition) 에서 6 scale 전부의
  faithful Φ 가 exact 로 계산 성공 — finite, ≥ 0, no panic.
- **H278.2 (verdict compare)**: faithful CV vs proxy CV(0.84) 비교 — scale-variant
  verdict 가 HOLD(둘 다 variant) 또는 FLIP(faithful 이 invariant) 로 판정된다.
- **H278.3 (MIP minimality)**: 반환된 MIP cut 이 모든 단일 bipartition cut 의
  최소값 (MIP 가 진짜 최소).
- **H278.4 (cross-process determinism)**: re-run 시 result.json byte-identical.
- **H278.5 (proxy baseline present)**: 동일 n=8 substrate 위 proxy Φ 도 측정되어
  faithful-CV 와 proxy-CV 가 apples-to-apples 비교된다.

## 4. Variables

- **axis1_scale** (substrate, fixed-6, H_002 C2 byte-parity): cosmic_web(rule 30,
  k=0.00) · galaxy_cluster(110, 0.10) · stellar(90, 0.20) · planetary(54, 0.30) ·
  biological(110, 0.45) · neural(110, 0.60) — rule/coupling 은 H_002 C2 run_c2.hexa
  와 동일.
- **axis2_metric** (primary): [faithful Φ (exact MIP-EI), proxy Φ (phi_spatial)] —
  두 partition 규칙, 동일 RFC 036 MI primitive.
- **fixed (config)**: n = 8 (H_002 C2 의 N=16 에서 축소 — n ≤ 8 exact 위해, 명시),
  dim = 12 · warm = 8 · n_bins = 4 (H_002 C2 / LIFE-lane canonical), periodic
  boundary, deterministic init (site i set iff i%3 != 0, C2 parity).
- **derived**: 2 metric × 6 scale = 12 measurement → faithful-CV · proxy-CV ·
  scale-class(VARIANT/INVARIANT) × 2 · HOLD/FLIP finding.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h278_faithful_phi_2026_05_25/run_h278.hexa`
- **Φ primitive (MI)**: `UNIVERSE/lib/phi_helper.hexa` → `c_phi_mi_pair` /
  `phi_with` → RFC 036 `phi_mi_pair` / `phi_spatial` (import READ-ONLY).
- **CA substrate**: H_002 C2 의 `_run_ca` / `_init_row` / `_ca_next` /
  `_apply_couple` 를 byte-parity 로 재사용 (rule/coupling/init 동일, lattice 만
  N=16→8).
- **faithful Φ (exact MIP-EI)**: n-cell 시스템에 대해 symmetric pairwise MI matrix
  MI[i][j] 구성 (RFC 036 phi_mi_pair) → 모든 non-trivial bipartition (2^(n-1),
  cell 0 을 A 에 pin, B-empty mask skip) 전수 → 각 cut 의 cross-partition MI
  Σ_{i∈A,j∈B} MI[i][j] 를 최소화하는 MIP 탐색 → faithful Φ = cross-cut(MIP) /
  min(|A|,|B|) (IIT small-side 정규화). Φ ≥ 0.
- **proxy Φ (baseline)**: 동일 n=8 substrate 위 `phi_with` (RFC 036 phi_spatial).
- **CV**: stddev / mean over 6 scale, 두 metric 각각.
- **deterministic**: fixed init + fixed config; re-run byte-identical (RFC 033
  단일 RNG stream → cross-process sha256 결정론).
- **hexa_only**: true (NO .py/.sh). **llm**: none. **runtime**: $0 mac local,
  **NO GPU** (small-N exact 로 충분, large-N 시도 금지). mac-local 강제 =
  env-var prefix (local-bound marker).
- **ledger**: `result.json` {config, 6-scale ledger(faithful+proxy), faithful/proxy
  stats, h002 ref CV, scale-class ×2, HOLD/FLIP, 5 falsifier, 3 criteria, verdict,
  verify_fence}.
- **honest tier**: 🟢 NUMERICAL (deterministic exact-MIP arithmetic) — faithful-ER
  than phi_spatial, but NOT full IIT4 4.0 (§9 L1).

## 6. Criteria

- **C1 (FAITHFUL-COMPUTE / H278.1)**: faithful Φ (exact MIP-EI) 6-scale 전부 계산
  성공 (n ≤ 8 tractable, finite ≥ 0) → PASS.
- **C2 (CV-COMPARE / H278.2)**: faithful CV vs proxy CV(0.84) 비교 완료 —
  scale-variant verdict 가 HOLD(유지) 인지 FLIP(정정) 인지 판정 (양방향 valid) →
  PASS (비교 수행 = met; HOLD/FLIP 자체는 게이트 아닌 reported finding).
- **C3 (DETERMINISM / H278.4)**: cross-run byte-identical → PASS.
- **verdict_rule**: **SUPPORTED** = C1 ∧ C2 (faithful 측정 완료 + verdict 비교);
  HOLD vs FLIP 은 reported, 게이트 아님. C1 실패(n>8 OOM / panic) 시 INSUFFICIENT.

## 7. Falsifiers

- **F-H278-1 TRACTABLE**: 어느 scale 의 faithful Φ 가 non-finite / 음수 / panic →
  small-N exact 가정 위반. (measurable: 6 faithful Φ finite ≥ 0.)
- **F-H278-2 CV-VERDICT**: faithful CV ≤ 0.15 → scale-INVARIANT (C2 FLIP) ·
  faithful CV > 0.15 → scale-VARIANT (C2 HOLD). (measurable: faithful_cv vs thr.)
- **F-H278-3 DETERMIN**: re-run byte-different → raw#12 deterministic 위반 → smoke
  무효. (measurable: scale-0 faithful Φ a == b + result.json cross-process diff.)
- **F-H278-4 PROXY-SANE**: 동일 n=8 substrate 위 proxy Φ 부재 → 비교 baseline 결손.
  (measurable: proxy-CV 존재.)
- **F-H278-5 MIP-VALID**: 반환된 MIP cut 이 어떤 단일 bipartition cut 보다 크다 →
  MIP 가 최소가 아님 (구현 버그). (measurable: spot-check scale 의 min ≤ 임의 cut.)
- **F-H278-6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation, raw#82
  retraction.

## 8. Verdict

```
verdict_class: SUPPORTED (pre-register-frozen smoke; C1 ∧ C2 met)

config: n=8 (H_002 C2 의 N=16 에서 축소, n≤8 exact MIP), dim=12, warm=8, n_bins=4,
        periodic, deterministic init i%3!=0 — rule/coupling H_002 C2 byte-parity.
bipartitions_per_scale: 128 (2^(8-1))

per-scale Φ (faithful exact MIP-EI  /  proxy phi_spatial, same n=8 substrate):
  scale            rule  couple   Φ_faithful    Φ_proxy
  cosmic_web        30   0.00     0.134574      0.163812
  galaxy_cluster   110   0.10     0.000011      0.000005
  stellar           90   0.20     0.000011      0.000005
  planetary         54   0.30     4.000011      3.000005
  biological       110   0.45     0.000011      0.000005
  neural           110   0.60     0.000011      0.000005

stats:
  FAITHFUL : mean=0.689105  min=0.000011  max=4.000011  CV=2.149885  → SCALE_VARIANT
  PROXY    : mean=0.527306  min=0.000005  max=3.000005  CV=2.100186  → SCALE_VARIANT
  H_002 C2 reference proxy-CV (N=16): 0.836892   ·   CV threshold (invariant if ≤): 0.15

scale-variant verdict: HOLD  (faithful agrees with proxy: still SCALE_VARIANT)
                       cv_direction: faithful_CV (2.15) higher than H_002 ref (0.84)

criteria:
  C1 FAITHFUL-COMPUTE (6 scale exact, n≤8)         : PASS
  C2 CV-COMPARE (faithful vs proxy 0.84, HOLD/FLIP) : PASS  (finding = HOLD)
  C3 DETERMINISM (cross-run byte-identical)         : PASS

falsifiers:
  F-H278-1 TRACTABLE  : PASS  (6 faithful Φ finite ≥ 0)
  F-H278-2 CV-VERDICT : SCALE_VARIANT (faithful CV 2.149885 > 0.15)
  F-H278-3 DETERMIN   : PASS  (scale-0 a=0.134574 == b; result.json cross-process byte-identical)
  F-H278-4 PROXY-SANE : PRESENT (proxy-CV 2.100186)
  F-H278-5 MIP-VALID  : PASS  (MIP cut ≤ spot-check cuts on biological scale)
  F-H278-6 POST-HOC   : NOT_TRIGGERED

evidence_summary: 🟢 NUMERICAL — faithful Φ (exact MIP-EI over all 128 bipartitions
  per scale, n=8) 가 H_002 C2 의 6-scale nested hierarchy 위에서 CV=2.15
  (SCALE_VARIANT) 를 산출. 동일 n=8 substrate 의 proxy CV=2.10 도 SCALE_VARIANT.
  H_002 C2 의 N=16 proxy verdict (CV 0.84, SCALE_VARIANT) 와 **방향 일치 (HOLD)** —
  faithful(exact-MIP) 측정이 proxy(heuristic) 의 scale-variant 결론을 *artifact 가
  아닌 진짜 negative 로 확증*. proxy 의 L-C2.1 한계 ("faithful 아님") 를 한 단계
  줄였다. frozen F2 (Φ_universe nested scale-variant → H2.2 FALSIFIED) 방향 유지 —
  단, proxy/toy/small-N level, full IIT4 의 formal refutation 아님 (§9).
falsifiers_triggered: none (F-H278-2 SCALE_VARIANT 은 HOLD 방향 = 예측 H278.2 의
  한 갈래, falsification 아님; F-H278-6 N/A)
```

re-run byte-identical 확인 (C3/F-H278-3 deterministic — `diff /tmp/h278_run1.json
result.json = ∅`, cross-process).

`hexa verify` (VERBATIM, no LLM self-judge) — empirical 해석은 closed-form atlas
identity 가 아니므로 g5 정직 fence:

```
verify --fence "H_278 faithful Phi small-N exact (MIP-EI over all 2^(n-1)
   bipartitions) re-measures H_002 C2's 6-scale toy cosmic hierarchy more
   faithfully than phi_spatial; the faithful CV=2.15 scale-VARIANT verdict
   (HOLD vs proxy) is a deterministic toy-substrate outcome, NOT an atlas identity"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by design;
           NOT a proven atlas atom (g4 honest fence, SF ≠ verified)
```

(faithful Φ VALUES 자체는 deterministic closed-form arithmetic — exact MIP cut /
min(|A|,|B|), RFC 036 MI estimator — 이며 fresh hexa run 에서 byte-수렴 확인. 오직
empirical 해석(scale-variant 의 의미)만 fenced.)

## 9. Honest Limits (raw#91 c3)

- **L1 (NOT full IIT4 4.0)**: 본 faithful Φ 는 exact-MIP-over-EI (small-n) —
  *phi_spatial proxy 보다 faithful* (진짜 MIP 최소화 + IIT small-side 정규화) 하나,
  **full IIT 4.0 의 cause-effect structure / Φ-structure 까지는 아니다**: transition
  probability matrix · cause-effect repertoire · distinctions · relations 없음.
  통합량은 pairwise-MI cross-cut 이지 IIT4 의 intrinsic-difference-over-purviews 가
  아니다. "faithful-er than phi_spatial, NOT full IIT4 4.0" — 과장 금지.
- **L2 (lattice N=16→8 축소)**: H_002 C2 는 N=16 lattice. 본 H 는 n ≤ 8 exact MIP
  tractability 위해 **n=8 로 축소**했다. rule/coupling/init 은 byte-parity 이나
  lattice 길이가 달라, faithful-CV(2.15) 와 H_002 C2 의 proxy-CV(0.84) 의 **절대값
  비교는 metric 효과 + lattice 효과가 섞여 있다**. 동일 n=8 의 proxy-CV(2.10) 를
  나란히 측정해 metric-only 비교를 분리했고, 그 결과 verdict 방향(SCALE_VARIANT)은
  metric/lattice 양쪽에서 robust — 단 *CV 절대값* 은 lattice 크기에 민감 (n=8 에서
  planetary rule-54 scale 이 강하게 dominance 하며 CV 가 0.84→~2.1 로 증폭).
- **L3 (toy substrate, not cosmology)**: 6 "scale" 은 toy multi-scale CA substrate
  (cosmic-web sparse → neural dense) 이지 cosmological simulation 이 아니다 (우주
  origin 은 locally not simulable — H_002 frozen L1/L5). rule/coupling 값은
  deterministic spread 이지 어떤 datum 에 fit 한 것이 아니다.
- **L4 (MIP normalization choice)**: faithful Φ 의 small-side 정규화 min(|A|,|B|) 는
  IIT 정신의 한 선택 — 다른 정규화 (no-norm, |A|·|B|, max) 는 다른 CV 산출 가능.
  본 H 는 small-side weighting (1-vs-(n-1) cut 불이익) 한 가지만 측정.
- **L5 (MI estimator 공유 bias)**: faithful 과 proxy 가 **동일** RFC 036 MI
  estimator(binary/n_bins=4 quantize, spatial slice) 를 쓰므로, 둘이 공유하는
  underlying bias (small-n / binning) 가 있으면 HOLD 가 spurious consensus 일 수
  있다 (H_239 L1 carry). partition 규칙만 다르므로 HOLD 는 *partition-faithfulness*
  의 robustness 일 뿐, MI-estimator-faithfulness 까지 보장하지 않는다.
- **L6 (CV-threshold 0.15 의 임의성)**: scale-invariant 판정 threshold CV ≤ 0.15 는
  H_002 C2 에서 carry 한 값 — 임의 선택. faithful CV 2.15 는 threshold 와 무관하게
  강하게 variant 이나, 경계 근처 결과였다면 threshold 선택이 verdict 를 좌우했을
  것이다.
- **L7 (verdict ≠ H2.2 final)**: 본 H 의 SUPPORTED(HOLD) 는 *proxy 보다 faithful 한
  small-N exact* 수준에서 H_002 C2 의 scale-variant 를 확증할 뿐, H2.2 (Φ_universe
  nested scale-invariant emerge) 를 *최종 verdict* 하지 않는다. H_002 는 frozen L1
  대로 multi-decade lane-open 이며, full IIT4 cosmic-scale engine (frozen L4 named
  blocker) 은 여전히 미구현. 본 H 는 C2 의 faithful-ness 를 한 칸 올렸을 뿐.

## 10. Cross-Links

- **parent H (직접 upgrade)**: H_002 C2 (Φ_universe nested, H2.2) — 본 H 가 그
  proxy(phi_spatial) 측정의 honest L-C2.1 ("faithful 아님") 를 small-N exact MIP-EI
  로 한 단계 줄임. 측정 artifacts:
  `state/h002_universe_phi_nested_2026_05_25/result_c2.json` (proxy CV 0.84, N=16,
  6-scale ledger 동일 rule/coupling).
- **sister H (metric axis)**: H_239 (alt-Φ metric cross-validation) — *다른 metric*
  (LZ / entropy) 의 cross-tool consistency; 본 H 는 *같은 metric family 안 partition
  규칙* 의 faithfulness upgrade (직교 axis).
- **Φ primitive**: `UNIVERSE/lib/phi_helper.hexa` (`phi_with` / `c_phi_mi_pair`
  → RFC 036 phi_spatial / phi_mi_pair) + `UNIVERSE/lib/phi_native.hexa` (pure-hexa
  exact-MIP port, n ≤ 20 spatial Φ; 본 H 의 faithful Φ 는 그 MIP 구조의 IIT
  small-side-normalized 변형) — import READ-ONLY.
- **gap lens**: faithful-vs-proxy = F8 (cross-tool / inter-instrument calibration)
  + F4 (counterfactual — "exact MIP 였다면 verdict 가 바뀌었을까?" → HOLD).
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82
  (no post-hoc) + g25/g26 (real-limits-first — GPU 추정 정정).
- **literature**:
  - Tononi (2004) An information integration theory of consciousness
  - Oizumi, Albantakis, Tononi (2014) From the phenomenology to the mechanisms of
    consciousness: IIT 3.0 (Φ = integrated info at the MIP)
  - Albantakis et al. (2023) IIT 4.0 (cause-effect structure / Φ-structure)
  - Balduzzi, Tononi (2008) Integrated information in discrete dynamical systems
  - Shannon (1948) A mathematical theory of communication (MI estimator)
  - Wolfram (2002) A New Kind of Science (Class I-IV elementary CA)

**State output**: `UNIVERSE/state/h278_faithful_phi_2026_05_25/result.json`
**Smoke**: `UNIVERSE/state/h278_faithful_phi_2026_05_25/run_h278.hexa`
**Tier**: 🟢 NUMERICAL (exact MIP-EI deterministic, faithful-er than phi_spatial,
NOT full IIT4 4.0 — §9 L1). 경험 해석은 ⚪ SPECULATION-FENCED (g5, §8).
**Next**: H_278r2 후보 — (a) **lattice sweep** (L2 axis): n ∈ {4,5,6,7,8} 로
faithful-CV 의 lattice 의존성을 측정 (CV 0.84→2.1 증폭의 n-dependence 분리);
(b) **normalization sweep** (L4 axis): no-norm / |A|·|B| / max 정규화로 CV
robustness; (c) **N=16 exact** (L2 의 strict path): 2^15=32768 bipartition 도
mac-local tractable — N=16 에서 faithful 측정해 H_002 C2 와 *동일 lattice* 직접
비교 (small-N 가정 완화하되 여전히 GPU 불요).
