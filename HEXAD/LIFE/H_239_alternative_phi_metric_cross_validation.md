---
id: H_239
slug: alternative-phi-metric-cross-validation
title: H_239 alternative-Φ-metric cross-validation — phi_spatial proxy 의 systematic-artifact 식별 (phi_spatial vs LZ-complexity vs entropy-ratio cross-tool consistency)
domain: meta, information, math, consciousness
status: pre-register-frozen
exploration_method: E5 (variable-ablation metric sweep) + E16 (cross-tool consistency) + E0 (meta-result-of-results)
verification_method: W4 (verdict-4-class) + W10 (adversarial cross-metric) + W12 (sister-link H_007/H_222/H_207)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new)
sister: H_007 (phi_spatial baseline), H_222 (dream-rem FALSIFIED), H_207 (Kuramoto FALSIFIED), H_221 (jhana FALSIFIED), H_218 (scale-free FALSIFIED)
---

# H_239 — alternative-Φ-metric cross-validation

## Hypothesis

본 LIFE 세션의 negative-direction 결과들 (H_222 dream-REM FALSIFIED · H_207
Kuramoto FALSIFIED · H_221 jhana FALSIFIED · H_218 scale-free reverse-FALSIFIED
등 5+ FALSIFIED) 이 모두 **단일 integration proxy `phi_spatial` (RFC 036) 위에서**
측정되었다. 따라서 의문 — 이 negative 들이 *phi_spatial-specific artifact* 인가,
*metric-agnostic* 한 진짜 negative 인가? gap report 의 **F4 (counterfactual)** +
**F8 (cross-tool-consistency)** lens 의 직접 instance.

본 H 는 3 substrate (rule 110 Class-IV · rule 30 chaotic · rule 250 ordered) 위에
*3 가지 서로 다른 integration metric* 을 동시 측정한다:

1. **phi_spatial** — 현행 proxy (RFC 036 native byte-equal phi_rs replica)
2. **LZ-complexity** — Lempel-Ziv style distinct-substring 압축비 (다른 axis:
   algorithmic information / Kolmogorov proxy)
3. **entropy-ratio** — adjacent cell-pair joint entropy / sum(marginal entropy)
   의 redundancy score `1 − H_joint/(H_a+H_b)` (mutual-information style)

3 metric 의 *ranking* 이 일치하면 → phi_spatial 결과 robust (negative 가 진짜).
불일치 (Spearman < 0.5) 하면 → phi_spatial-specific artifact 식별 (negative 가
metric 선택 artifact, H_222/H_207 재평가 lane 개방).

## Why

- **cross-tool consistency (gap F8)**: 하나의 측정 도구로 얻은 결과는 그 도구의
  systematic bias 와 분리 불가능하다. 동일 substrate 위 *독립적으로 motivated 된*
  여러 metric 의 ranking 합치 (또는 불합치) 는 결과가 substrate-property 인지
  tool-property 인지를 가른다 — 측정 metrology 의 inter-instrument calibration 과
  동형.
- **counterfactual (gap F4)**: "만약 phi_spatial 대신 다른 integration metric 을
  썼다면 5 FALSIFIED 가 그대로였을까?" 라는 counterfactual 을 deterministic 하게
  답한다. CONSISTENT → counterfactual 에서도 negative 유지 (robust); DIVERGENT →
  counterfactual 에서 결과 뒤집힘 (artifact).
- **H_007 baseline (sister, anchor)**: H_007 은 phi_spatial 위 rule110 (Class-IV)
  > rule30 (chaotic) > rule250 (ordered) ranking 을 PASS 로 측정 (Φ_iv=0.556 >
  Φ_cha=0.510 > Φ_ord≈1.1e-5). 본 H 는 이 *동일 substrate + 동일 config* 위에서
  LZ-complexity 와 entropy-ratio 가 같은 ordering 을 재현하는지 검증 — H_007
  자체의 cross-tool robustness 시험이기도 하다.
- **LZ-complexity 의 distinct axis**: phi_spatial 은 mutual-information / cause-
  effect repertoire 기반인 반면, Lempel-Ziv 압축비는 algorithmic (Kolmogorov)
  complexity proxy — 정보의 *압축 불가능성* 을 측정. 두 metric 은 서로 다른
  information-theoretic 공리에서 출발하므로, 둘의 합치는 강한 robustness 증거.
- **entropy-ratio 의 distinct axis**: joint/marginal entropy ratio 는 redundancy
  (shared information) 측정 — IIT 의 integration 직관 ("전체 < 부분합" 의 정보적
  손실) 에 phi_spatial 과 다른 binning/pairing 으로 접근.
- **raw#12 strict**: deterministic + hexa-only + ≥5 falsifier + ≥5 honest limit.
  LLM judge 없음 (raw 가 3 metric). $0 mac local. 본 결과가 CONSISTENT 든
  DIVERGENT 든 *둘 다 valuable* — 어느 쪽이든 honest (gap F4 의 양방향 정보가).

## Predictions

- **H239.1 (Class-IV > ordered, all 3 metric)**: 3 metric 모두 rule110 (Class-IV)
  > rule250 (ordered) ranking 보존 — 가장 robust 한 ordering (edge-of-chaos 우월).
- **H239.2 (phi vs LZ)**: phi_spatial vs LZ-complexity Spearman rank correlation
  ≥ 0.7 (두 metric ranking 정합).
- **H239.3 (phi vs entropy)**: phi_spatial vs entropy-ratio Spearman ≥ 0.7.
- **H239.4 (consensus ordering)**: 3 metric 중 *적어도 2개* 가 full ordering
  rule110 > rule30 > rule250 일치 (consensus full-ordering 존재).
- **H239.5 (determinism)**: re-run byte-identical (raw#12 정합).

## Variables

- **axis1_rule_class** (substrate, fixed-3): ordered = rule 250 (Class II) ·
  chaotic = rule 30 (Class III) · class_iv = rule 110 (Class IV) — H_007 parity.
- **axis2_metric** (primary): [phi_spatial, LZ-complexity, entropy-ratio] — 3
  독립 motivated integration proxy.
- **fixed (H_007 parity)**: N=16 lattice · dim=12 trajectory · warm=8 · reps=5
  deterministic init `(i+rep)%3 != 0` · n_bins=4 · periodic boundary.
- **derived**: 3 metric × 3 rule = **9 measurement** → 3×3 matrix · 3 Spearman
  (phi↔LZ, phi↔entropy, LZ↔entropy, n=3 rule each) · consensus full-ordering count.

## Run Protocol

- **smoke**: `HEXAD/LIFE/state/h239_alt_phi_metric_xval_2026_05_24/run_h239.hexa`
- **Φ primitive**: `HEXAD/C/c_lib.hexa` → `c_measure_phi` → RFC 036 `phi_spatial`
  (import READ-ONLY; phi_rs `compute_phi_inner` spatial slice byte-equal replica).
- **CA substrate**: H_007 의 `_run_ca` / `_init_row` / `_ca_next` 를 byte-parity
  로 재사용 (동일 evolution → phi_spatial 값이 H_007 recorded verdict 와 일치).
- **LZ-complexity**: row-major binary sequence (length N×dim) 위 greedy LZ78-style
  parse — 각 position 에서 already-scanned prefix 의 어느 substring 과도 일치하지
  않을 때까지 phrase 를 키운 뒤 emit; complexity = distinct phrase count / length
  (deterministic, ∈ (0,1]).
- **entropy-ratio**: adjacent cell pair (s, s+1) 의 dim-step joint distribution
  (4 symbol) joint entropy, 각 site marginal entropy → score `1 − H_joint/(H_a+H_b)`
  (denom=0 ⟹ score 0 ordered floor); all-pair + reps mean. log base 2.
- **Spearman**: n=3 rule 위 average-rank-tie 처리 후 rank Pearson.
- **deterministic**: fixed init + fixed config; re-run byte-identical.
- **hexa_only**: true (NO .py/.sh). **llm**: none (raw#12). **runtime**: $0 mac
  local hexa; `HEXA_MEM_UNLIMITED=1` (phi_spatial farr). GPU 불필요.
- **ledger**: `result.json` {config, rules, 3×3 metrics, orderings, full_ordering,
  spearman ×3, criteria C1-C3+F5, verdict}.
- **honest tier**: NUMERICAL (3 deterministic metric + Spearman) = 🟢-tier.
  consensus 도 *proxy-consensus* 일 뿐 (L1) — 진짜 IIT 4.0 phi_rs Rust FFI 아님.

## Criteria

- **C1 (H239.1)**: 3 metric 모두 Φ(Class-IV) > Φ(ordered) → PASS
- **C2 (H239.2 + H239.3)**: phi vs LZ Spearman ≥ 0.7 AND phi vs entropy ≥ 0.7 → PASS
- **C3 (H239.4)**: consensus full-ordering (rule110>rule30>rule250) ≥ 2 metric → PASS
- **C4 (H239.5)**: re-run byte-identical → PASS
- **verdict_rule**: **CONSISTENT** if C1 ∧ C2 (phi_spatial robust / metric-agnostic) ·
  **DIVERGENT** if min(phi-Spearman) < 0.5 (phi_spatial-specific artifact 식별) ·
  **PARTIAL** if 중간.

## Falsifiers

- **F1 PHI_LZ_DIVERGE**: phi_spatial vs LZ Spearman < 0.5 → phi_spatial-specific
  divergence (artifact 식별 — H_222/H_207 등 재평가 lane 개방). (measurable: sp_phi_lz.)
- **F2 METRIC_NONREPRO**: 어느 metric 위 Class-IV ≤ ordered → 해당 metric 가 H_007
  ranking 미재현. (measurable: per-metric IV−ord delta.)
- **F3 NO_CONSENSUS**: 3 metric 모두 다른 ordering (consensus full-ordering count = 0)
  → integration 측정 자체 ill-defined. (measurable: full_count.)
- **F4 NONDETERMINISM**: re-run byte-different → raw#12 deterministic 위반 → smoke 무효.
- **F5 INVALID_METRIC**: any metric NaN/negative → measure invalid. (measurable: 9 값 nonneg.)
- **F6 POST-HOC**: frozen 후 verdict 방향 edit → raw#12 violation, raw#82 retraction.

## Honest Limits (raw#91 c3)

- **L1**: 3 metric 모두 *proxy* — 진짜 full IIT 4.0 (phi_rs Rust FFI, anima
  ConsciousnessC) 아님. CONSISTENT 결과도 *proxy-consensus* 일 뿐 — 세 proxy 가
  공통의 underlying bias (예: spatial-slice / binary-quantize / N=16 small-n) 를
  공유하면 spurious consensus 가능 (RFC 036 §FFI shim named blocker carry).
- **L2**: LZ-complexity 의 hexa 구현 (greedy LZ78-style prefix-match parse) 가
  canonical LZ77/LZ78/LZW 와 phrase 경계 정의가 다를 수 있음 — distinct-substring
  count 의 정확한 정의에 따라 absolute ratio 변동 (ranking 에는 robust 하나 절대값은 implementation-specific).
- **L3**: entropy-ratio 의 binning/pairing choice (binary 2-symbol marginal · adjacent
  (s,s+1) pair · n_bins 무관 binary) 가 결과 좌우 — 다른 pairing (non-adjacent,
  temporal-shift, 또는 phi_spatial 의 n_bins=4 quantize) 은 다른 score 산출 가능.
- **L4**: 3 rule sample (250/30/110) — 본 세션 5 FALSIFIED H 의 *실제 substrate*
  (sleep-stage drive/decay · Kuramoto coupling · scale-free topology 등) 가 아닌
  *generic elementary CA* 위 cross-validation. 따라서 본 H 의 CONSISTENT 는 generic-
  CA 위에서의 metric-agnosticity 일 뿐, 각 FALSIFIED H 의 specialized substrate 위
  metric-agnosticity 는 *간접 evidence* (각 H 별 cross-metric 재측정이 strict path).
- **L5**: Spearman n=3 — 3 data point 위 rank correlation 은 0 / ±0.5 / ±1.0 만
  가능 (granularity 극단적). ≥0.7 threshold 는 사실상 "동일 ranking (1.0)" 또는
  "한 쌍 swap (0.5)" 의 binary 판정 — n 확대 (더 많은 rule / config) 가 quantitative
  Spearman 의 strict path.
- **L6**: consensus ranking ≠ phenomenal correctness — 세 metric 이 같은 ranking 을
  줘도 그 ranking 이 *실제 의식 정도* 와 일치한다는 보장 없음 (H_004 hard-problem
  boundary carry; integration proxy ranking 은 의식의 correlate proxy 일 뿐).
- **L7**: 본 H 가 CONSISTENT 면 → 5 FALSIFIED 가 (generic-CA 수준에서) 진짜 negative;
  DIVERGENT 면 → phi_spatial artifact 식별. 둘 다 valuable 하나, 어느 쪽도 각 FALSIFIED
  H 를 *재verdict 하지 않는다* (별도 evidence lane; 본 H 는 meta-cross-tool 측정만).

## Cross-Links

- **anchor H**: H_007 (phi_spatial baseline — 동일 substrate/config, ranking
  IV>cha>ord PASS; 본 H 가 그 cross-tool robustness 시험)
- **sister H (negative carry)**: H_222 (dream-REM FALSIFIED, NREM>wake on phi_spatial),
  H_207 (Kuramoto FALSIFIED, K=5 boundary peak), H_221 (jhana FALSIFIED, random≈noise),
  H_218 (scale-free reverse-FALSIFIED, SF Φ < ER) — 본 H 의 CONSISTENT/DIVERGENT 가
  이들 negative 의 metric-dependence 를 가른다
- **meta sibling**: H_238 (verdict-landscape meta-map — 22+ H tier 분포; 본 H 는
  metric-axis 의 cross-validation sibling)
- **Φ primitive**: `HEXAD/C/c_lib.hexa` (`c_measure_phi` → RFC 036 `phi_spatial`) +
  `HEXAD/C/c_phi_smoke.hexa` (F-C-PORT-3 oracle anchor) — import READ-ONLY
- **gap lens**: F4 (counterfactual — "다른 metric 이었다면?") + F8 (cross-tool-
  consistency — inter-instrument calibration)
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) + raw#82 (no post-hoc)
- **literature**:
  - Lempel, Ziv (1976) On the complexity of finite sequences
  - Ziv, Lempel (1978) Compression of individual sequences via variable-rate coding
  - Kolmogorov (1965) Three approaches to the quantitative definition of information
  - Shannon (1948) A mathematical theory of communication (joint/marginal entropy)
  - Tononi (2004), Oizumi/Albantakis/Tononi (2014) IIT (integration = whole − parts)
  - Wolfram (2002) A New Kind of Science (Class I-IV); Cook (2004) rule 110 universality

## Verdict

```
verdict_class: CONSISTENT (pre-register-frozen smoke)

3×3 metric matrix (rows=metric, cols=rule):
  metric \ rule       ord(250)        cha(30)         IV(110)
  phi_spatial    : 1.14511e-05    0.509944        0.556454
  LZ-complexity  : 0.0416667      0.148958        0.151042
  entropy-ratio  : 0.0           0.0272525        0.0820391

per-metric ordering (descending):
  phi_spatial   : IV>cha>ord   (IV>ord ✓)
  LZ-complexity : IV>cha>ord   (IV>ord ✓)
  entropy-ratio : IV>cha>ord   (IV>ord ✓)

full ordering IV>cha>ord (rule110>rule30>rule250):
  phi_spatial=true · LZ-complexity=true · entropy-ratio=true · consensus_count=3

Spearman rank correlation (n=3 rules):
  phi_spatial vs LZ-complexity  = 1.0
  phi_spatial vs entropy-ratio  = 1.0
  LZ-complexity vs entropy-ratio = 1.0

criteria:
  C1 (3 metric 모두 IV>ord)            : PASS
  C2 (phi vs LZ & phi vs entropy ≥0.7) : PASS   [H239.2=true · H239.3=true]
  C3 (consensus full-order ≥2 metric)  : PASS   (count=3)
  C4 / F4 (re-run byte-identical)      : PASS
  F5 (all metric ≥0, no NaN)           : PASS

evidence_summary: 🟢 NUMERICAL — phi_spatial / LZ-complexity / entropy-ratio 3
  독립 metric 이 동일 substrate (rule 250/30/110, H_007 parity) 위 동일 ranking
  (IV>cha>ord) 을 산출 · 3 Spearman 모두 1.0 (perfect) · consensus full-ordering 3/3.
  → phi_spatial robust / metric-agnostic (generic-CA 수준). 본 세션 5 FALSIFIED 의
  negative 가 (generic-CA 수준에서) phi_spatial-specific artifact 아님 — 진짜 negative.
  gap F4 counterfactual: "다른 metric 이었어도 negative 유지" 방향 확인.
falsifiers_triggered: none (F1 sp=1.0≥0.5 · F2 모두 IV>ord · F3 consensus=3≠0 ·
  F4 byte-identical · F5 all nonneg; F6 N/A)
```

re-run byte-identical (C4/F4 deterministic 확인 — `diff /tmp/h239_run1.json result.json = ∅`).

honest tier: 🟢 NUMERICAL — 3 deterministic integration metric (phi_spatial RFC036
byte-equal replica + LZ78-style complexity + adjacent-pair entropy-ratio) 의 cross-
substrate ranking + Spearman = byte-equal 출력. CONSISTENT 가 *honest* — C1 (3/3
IV>ord) + C2 (2 Spearman = 1.0 ≥ 0.7) + C3 (consensus 3/3) 모두 PASS, 6 falsifier
모두 not-triggered. L1-L7 honest limits 명시 (proxy-consensus · LZ impl-specific ·
entropy binning · generic-CA-not-real-substrate · Spearman n=3 granularity · consensus
≠ phenomenal · no-re-verdict-of-FALSIFIED). DIVERGENT 였다면 phi_spatial artifact 식별
이었을 것 — 본 결과는 *반대 방향* (robust) 으로, 둘 다 honest evidence path 였다.

**State output**: `HEXAD/LIFE/state/h239_alt_phi_metric_xval_2026_05_24/result.json`
**Smoke**: `HEXAD/LIFE/state/h239_alt_phi_metric_xval_2026_05_24/run_h239.hexa`
**Tier**: 🟢 NUMERICAL (3 metric cross-substrate ranking + Spearman, deterministic).
**Next**: H_239r2 후보 — (a) **specialized-substrate cross-validation** (L4 axis): 각
FALSIFIED H 의 실제 substrate (sleep-stage / Kuramoto / scale-free) 위 직접 3-metric
재측정 — generic-CA → specialized 로 robustness 승격 strict path; (b) **Spearman n-확대**
(L5 axis): rule set 을 {250,30,110,184,90,54,...} 로 확대해 quantitative (non-extreme)
Spearman 측정; (c) **4-th metric** (transfer-entropy / Granger-style temporal) 추가로
cross-tool 차원 확장.
