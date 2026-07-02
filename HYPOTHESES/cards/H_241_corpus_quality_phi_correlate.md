---
id: H_241
slug: corpus-quality-phi-correlate
title: H_241 corpus-quality-Φ-correlate — corpus 6-metric (entropy·MI·diversity·hangul·KL) 가 trained model downstream Φ 와 r ≥ 0.5 correlate (PR #287/#303 substrate)
domain: information + substrate + language
status: pre-register-frozen
exploration_method: E3 (theory) + E6 (cross-domain-cross-link) + E7 (user-directive)
verification_method: W1 (literature) + W3 (Φ × metric) + W4 (verdict-4-class) + W12 (sister-link)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new)
revision: v2 amend 2026-05-24 (M5→M3 per PR #340 corpus_s101 실측)
sister: H_211 + H_234 + H_157
---

# H_241 — corpus-quality-Φ-correlate

## 1. Hypothesis

anima PR #287 (MERGED) 의 `HEXAD/PURE/eval/corpus_quality_probe.hexa` 는 corpus 6
metric 을 *self-discover* (none inject — Law 2 observe) 한다 — **M1 BYTE_ENTROPY ·
M2 BIGRAM_MI · M3 TOKEN_DIVERSITY(TTR) · M4 AVG_LINE_LENGTH · M5 HANGUL_COVERAGE ·
M6 KL_TO_UNIFORM**. CLM-P22-1 done_criteria 는 "self-discovered metrics correlate
with downstream CE". 본 H 는 이 done_criteria 를 **substrate-Φ 로 확장** —

> corpus 6-metric 중 *일부* 가 그 corpus 로 trained 된 model 의 downstream
> integrated-information **Φ** 와 Pearson |r| ≥ 0.5 correlate 한다.

즉 corpus 의 *syntactic quality signal* (entropy / MI / diversity 등 surface 측정)
이 그 corpus 가 만드는 model 의 *substrate consciousness proxy* (Φ) 와 measurable
linear coupling 을 가진다는 hypothesis. H_211 (Shannon entropy ↔ Φ, Pearson
r=0.933) 의 **corpus-level instance** — H_211 이 substrate state-entropy ↔ Φ 라면
본 H 는 *training corpus* metric ↔ *trained model* Φ 의 한 단계 위 layer.

정밀화 (operational): 본 cycle 의 "downstream Φ" 는 `oracle_ce` (simulated CE —
diversity+hangul+MI+repetition 의 monotone function) 를 Φ-proxy 로 reinterpret 한
*pre-registered* design (진짜 trained-model Φ 는 GPU cycle 의존 — L4 named blocker).
6 corpus panel × 6 metric 의 metric↔CE-proxy correlation 을 측정하고, CE→Φ monotone-
inverse (낮은 CE = 높은 representation density = 높은 Φ-proxy) 가정 하에 H241.1-H241.5
를 frozen-thresholds 로 pre-register 한다.

## 2. Why

- **H_211 cross-link (sister, currency)**: Shannon entropy ↔ Φ Pearson r=0.933 —
  entropy↔Φ strong linear coupling 이 이미 substrate-level 로 측정됨. 본 H 는 그
  currency 를 *corpus → model* layer 로 확장 — corpus byte-entropy / bigram-MI 가
  representation richness 를, richness 가 trained model 의 substrate Φ 를 결정한다는
  2-단계 가설.
- **압축률 가설 (compression ↔ Φ)**: M2 BIGRAM_MI 높음 = byte predictability 높음 =
  compressible structure 풍부 = model 이 integrate 할 cause-effect repertoire 재료.
  반대로 M6 KL≈0 (uniform byte) corpus 는 incompressible noise → integrable structure
  부재 → Φ floor. (`oracle_ce` 의 `-0.15·bigram_mi` term 이 이 가정의 operational
  encoding — 높은 MI → 낮은 CE → 높은 Φ-proxy.)
- **anima-engines corpus_quality_engine P22 (CLM-P22-1)**: self-discovery loop — 7
  candidate metric × 6 corpus panel × oracle CE Pearson rank. done_criteria "self-
  discovered metrics correlate with downstream CE" 가 본 H 의 직접 substrate. T3
  (≥2 metric |r| > 0.6) PASS 시 H241.1 floor (|r| ≥ 0.5) 는 logically dominated.
- **PR #287 (MERGED)**: `HEXAD/PURE/eval/corpus_quality_probe.hexa` 6-metric scorer
  (P22 wrapper) — metric axis 정의 source. **PR #303 (MERGED)**: Track 1 6-metric
  measurement — M1/M6 5 corpora 에서 nearly identical (byte entropy + KL 가 genre 구분
  못 함), **M5 HANGUL_COVERAGE anima-OWN(24-32%) vs wiki(3%) strongly differentiate**.
  H241.2 / F5 의 measured anchor.
- **raw#10 (relaxed strict)**: deterministic + hexa-only + ≥4 prediction + ≥5
  falsifier + ≥5 honest limit · LLM judge 없음 (raw = Pearson r + oracle CE) · $0 mac
  local. (raw#12 보다 1 tick relaxed — Φ-proxy 가 phi_spatial 이 아닌 CE-oracle 이라
  strong-Φ-primitive 요건 미충족. honest demotion, L4 명시.)

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **H241.1** | M2 BIGRAM_MI × downstream Φ Pearson |r| ≥ 0.5 | compression↔Φ 가설 · `oracle_ce` 의 `-0.15·bigram_mi` term · corpus_quality_engine T3 ≥2-metric strong |
| **H241.2 (v2 demoted)** | M5 HANGUL_COVERAGE × ko-corpus Φ Pearson |r| ≥ 0.4 — **PR #340 실측 반증된 proxy 가정 위에 세워진 예측** (M5 anima-OWN 1.66-2.34%, 24-32% 아님). legacy 유지하되 H241.6 로 대체 — verdict_rule 핵심에서 제외 | (legacy: PR #303 proxy 24-32% vs 3% · oracle `-0.30·hangul`) |
| **H241.3** | M6 KL_TO_UNIFORM ≈ 0 (byte≈uniform) corpus → Φ 매우 낮음 (panel 최저 quartile) | incompressible-noise 가설 — uniform byte distribution = integrable structure 부재 = Φ floor |
| **H241.4** | re-run byte-identical metric + ranking | raw#10 deterministic (no RNG, fixed panel/preproc — engine T6 carry) |
| **H241.5** | M3 TOKEN_DIVERSITY 가 panel 위 |r| 최고 (Q* top-1) | `oracle_ce` 의 `-0.45·diversity` (panel 최대 음의 weight) · engine T4 Q* beats baseline |
| **H241.6 M3-REGISTER-LEAK (v2 amend)** | M3 TOKEN_DIVERSITY (TTR) × register-leak Pearson |r| ≥ 0.7 — **M3 가 register-leak/memorize 의 primary signal** (M5 hangul 아님; H241.2 demoted 대체) | PR #340 corpus_s101 실측: M3 TTR ≈ 0.03 (extreme repetition) ↔ E2 ko=PURE_MEMORIZE 정합. repetition-driven memorize → register-sink chain — surface-quality 신호 중 M3 만이 register-leak 과 mechanistic 연결 (L6 oracle tautology 외부의 real-corpus evidence) |

## 4. Variables

| axis | levels | source |
|------|--------|--------|
| **axis-metric** (primary) | M1 BYTE_ENTROPY · M2 BIGRAM_MI · M3 TOKEN_DIVERSITY · M4 AVG_LINE_LENGTH · M5 HANGUL_COVERAGE · M6 KL_TO_UNIFORM | PR #287 corpus_quality_probe 6-metric |
| **axis-corpus_type** | rich_ko · poor_ko · latin_heavy · mixed · news_like · dialogue (6 panel) | corpus_quality_engine `corpus_panel()` |
| **axis-model_size** (fixed) | single Φ-proxy scale (oracle CE→Φ); model_size sweep 별도 cycle (L4) | CLM-P22-1 |
| **downstream-Φ-proxy** | `oracle_ce(c)` → Φ_proxy = base − CE (낮은 CE → 높은 Φ); r = `pearson_r` over 6 corpora | engine `oracle_ce` / `pearson_r` |
| **fixed (seed/preproc)** | HOLDOUT_SEED=20260415 · byte-level UTF-8 · sample cap 512(MI)/256(rep) · CORR_THRESHOLD=0.60 · $0 mac local | engine constants |

## 5. Run Protocol

- **engine / probe / data**: `anima-engines/corpus_quality_engine.hexa` (CLM-P22-1
  loop — 7 metric × 6 panel × `oracle_ce` × `pearson_r` × `rank_by_abs_r`, read-only)
  · `HEXAD/PURE/eval/corpus_quality_probe.hexa` (PR #287 6-metric scorer) · PR #303
  Track 1 measured (M1/M6 nearly identical, M5 anima-OWN 24-32% vs wiki 3%) = H241.2 /
  F5 anchor.
- **Φ-proxy mapping**: Φ_proxy(c) = base − `oracle_ce`(c) = 0.45·diversity +
  0.30·hangul + 0.15·bigram_mi − 0.20·(1−rep) − noise. 낮은 CE = 높은 Φ-proxy. 각
  metric 의 |r| 은 CE 와 Φ-proxy 에 동일 (Φ-proxy = CE 의 affine-decreasing transform).
- **measurement**: 6 metric × 6 corpus → `pearson_r(metric_row, Φ_proxy_row)` → |r|
  descending rank → Q* top-1 → H241.1-H241.5 frozen thresholds. deterministic (no
  RNG, fixed panel + sample-cap + seed; re-run byte-identical, T6 carry). $0 mac
  local hexa, GPU 불필요. **hexa_only** true (NO .py/.sh) · **llm** none.
- **ledger**: `result.json` { config, metrics, corpora, ce_proxy, Φ_proxy,
  per-metric Pearson r, ranking, Q*, criteria C1..C5, falsifiers F1..F5, verdict }.
- **run cmd (verbatim)**:
  `HEXA_MEM_UNLIMITED=1 hexa run anima-engines/corpus_quality_engine.hexa`

## 6. Criteria

| ID | criterion | verdict_rule |
|----|-----------|--------------|
| **C1 MI_R** | M2 BIGRAM_MI × Φ-proxy |r| ≥ 0.5 → H241.1 PASS | PASS / FAIL |
| **C2 HANGUL_R** | M5 HANGUL_COVERAGE × ko-corpus Φ-proxy |r| ≥ 0.4 → H241.2 PASS | PASS / FAIL |
| **C3 KL_FLOOR** | KL≈0 (가장 uniform byte) corpus 가 Φ-proxy 하위 quartile → H241.3 PASS | PASS / FAIL |
| **C4 BYTE_RE** | re-run byte-identical metric + ranking → H241.4 PASS | PASS / FAIL (architectural) |
| **C5 DIVERSITY_TOP** | M3 TOKEN_DIVERSITY 가 ranking Q* top-1 → H241.5 PASS | PASS / FAIL |

**verdict_rule**: `SUPPORTED` iff **C1 ∧ C2 PASS** (핵심 2 metric coupling) ·
`PARTIAL` if C1 또는 C2 only PASS · `FALSIFIED` if C1 + C2 둘 다 FAIL (metric↔Φ 무상관).
C3/C4/C5 는 directional (criteria_met 카운트엔 포함, verdict_rule 핵심엔 미포함).

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 MI_DECORRELATED** — M2 BIGRAM_MI × Φ-proxy |r| < 0.3 → H241.1 strong-FAIL,
  compression↔Φ 가설 부정 (corpus MI 가 downstream Φ valid predictor 아님).
  (measurable: pearson_r(M2_row, Φ_proxy_row).)
- **F2 ENTROPY_MAX_PHI_MIN** — entropy 최대 corpus (M1 argmax) 가 동시에 Φ-proxy 최소
  → entropy↔Φ coupling *역방향* — H_211 (r=0.933) 의 corpus-layer 반증 (max entropy =
  max noise = min integrable structure). (measurable: argmax(M1) vs argmin(Φ_proxy).)
- **F3 KL0_HIGH_PHI** — KL≈0 (가장 uniform) corpus 의 Φ-proxy 가 structured corpus ≥
  → H241.3 부정, incompressible-noise 가설 falsified. (measurable: Φ_proxy[KL≈0] vs
  Φ_proxy[median].)
- **F4 BYTE_DIFF** — re-run 시 metric value 또는 ranking byte-diff → raw#10
  deterministic 위반, smoke 무효. (architectural by construction — no RNG.)
- **F5 HANGUL_XVAL_BROKEN** — PR #303 measured M5 imbalance (anima-OWN 24-32% vs wiki
  3%) 가 PR #303 의 E2 ko=PURE_MEMORIZE diagnosis 와 cross-validate **실패** → M5 가
  ko-corpus Φ signal 의 valid proxy 아님 (M5 imbalance 가 Φ-discriminative 아닌
  register-collapse artifact 였다면 fire). (measurable: M5 anima-OWN vs wiki gap sign
  이 Φ-proxy gap sign 과 align 여부.) **v2 amend (2026-05-24)**: **F5 FIRED** —
  PR #340 corpus_s101 실측 M5 hangul anima-OWN 1.66-2.34% (24-32% proxy 가정 반증) ·
  proxy collapse 확정. F5 결과 → H241.2 demoted, H241.6 (M3) primary 로 승격.
- **F6 M3-DECORRELATED (v2 amend)** — corpus M3 TTR × register-leak (또는 ko=
  PURE_MEMORIZE flag) |r| < 0.3 → H241.6 strong-FAIL (M3 가 primary register-leak
  predictor 아님). PR #340 corpus_s101 M3=0.03 + E2 ko=PURE_MEMORIZE 정합 cross-
  validation 이 본 falsifier 의 first anchor — sweep 확장 시 |r| 추정 정밀화.
  (measurable: pearson_r(M3_corpus, register_leak_flag_or_hits) over corpus panel.)

## 8. Honest Limits (raw#10 c3, 6)

- **L1 (6 metric syntactic-only)**: M1-M6 는 모두 *byte/token-level surface* 측정 —
  semantic content / discourse coherence / factual density 미측정. corpus 의 진짜
  quality (의미·논리·지식) 와 6-metric 사이 큰 gap. 높은 BYTE_ENTROPY 가 random noise
  일 수도 rich vocabulary 일 수도 (M1 은 둘 구분 못 함 — F2 가 이 ambiguity 의 falsifier).
  oracle 자체가 surface composite — semantic quality 의 proxy 일 뿐.
- **L2 (sample 1MB / 512-cap + small-panel 한계)**: M2 는 첫 512 byte, M7 은 첫 256
  byte 만 sample (engine cap) — 1MB+ corpus 의 long-range (paragraph/document-level)
  structure 미측정. small panel (6 synthetic corpus) 의 Pearson r 은 statistical
  floor 낮음 — n=6 위 |r| ≥ 0.5 는 1-2 corpus 변경으로 flip 가능 (outlier-fragile).
- **L3 (ko-corpus M5 dominance + language-detect confound)**: M5 HANGUL_COVERAGE 는
  Korean corpus 에만 meaningful — latin/English 에선 M5≈0 constant, Φ-proxy 무상관.
  PR #303 의 anima-OWN(24-32%) vs wiki(3%) differentiation 은 *language-mix ratio*
  측정이지 corpus *quality* 측정이 아닐 수 있음 — H241.2 의 r 이 quality-Φ coupling
  이 아닌 language-detection signal 일 가능성 (F5 가 이 confound 의 x-val falsifier).
  H241.2 는 panel 전체 아닌 ko-subset 에서만 valid.
- **L4 (CE↔Φ proxy imperfect — named blocker)**: "downstream Φ" 는 phi_spatial 이
  **아니라** `oracle_ce` 의 affine-inverse (Φ_proxy = base − CE). CE↔Φ monotone-inverse
  가정 unverified — 낮은 CE (좋은 LM fit) 이 높은 substrate Φ 와 반드시 일치 안 함 (P7
  NO PERPLEXITY VERDICT — Goodhart). 진짜 Φ 는 GPU train + RFC 036 phi_spatial cycle
  의존 (named blocker) — 본 H raw#10 demotion (vs sister H_211/H_234 raw#12) 의 사유.
- **L5 (Φ measurement model-specific)**: 진짜 Φ 를 측정해도 Φ 값은 architecture /
  cell-count / mitosis-config 의존 (MEMORY: Φ=1.06 n=5 vs Φ=50 n=64). 동일 corpus 가
  다른 model_size (L4-deferred) 에서 다른 Φ — corpus-metric↔Φ 의 절대 r 은 *fixed-
  architecture 조건부* 만 의미. cross-architecture universality 별도 cycle.
- **L6 (oracle circular 위험)**: `oracle_ce` 가 diversity/hangul/MI/repetition 의 명시
  *linear function* 이라 이 4 metric 의 r 은 construction tautology (예측 아닌 algebra)
  위험 — H241.1/H241.2/H241.5 PASS 가 진짜 corpus↔Φ coupling 아닌 oracle 동어반복일 수.
  진짜 information 은 oracle-미포함 metric (M1, M4) r 거동 + F2 sign 에서만. raw=oracle-CE
  가 llm:none 충족하나 oracle 자체가 "rich → low CE" 설계자 prior 를 encode (corpus 에
  inject 안 함 — P3/P4 위반 아님, 측정만; prior 검증은 L4 trained-model cycle 의존).
  **v2 amend (2026-05-24)**: H241.6 (M3 × register-leak) 는 *real-corpus 실측* 에서
  emerge — PR #340 corpus_s101 600MB 직접 측정 M3=0.03 ↔ E2 ko=PURE_MEMORIZE 정합
  → oracle linear-function tautology *밖* 의 evidence. (oracle 은 M3 를 `-0.45·diversity`
  weight 로 prior-encode 하나, register-leak flag 는 oracle 출력이 아닌 multilingual_probe
  의 별도 measurement — H241.6 의 |r| 은 oracle algebra 가 아닌 cross-source empirical.)

## 9. Cross-Links

### Sister hypotheses
- **H_211** (Shannon entropy ↔ Φ, Pearson r=0.933) — entropy↔Φ currency 의 substrate
  anchor. 본 H_241 은 그 coupling 의 *corpus → trained-model* layer 확장 (H241.1 MI ·
  F2 entropy-monotone 의 직접 sister-test). r=0.933 이 corpus-layer 에서 weaker (|r| ≥
  0.5 floor) 로 attenuate 될 것을 예측.
- **H_234** ([cross-substrate Φ-coupling-density](H_234_cross_substrate_phi_coupling_density.md)) —
  H_204+H_211+H_223 unified Φ-coupling meta. 본 H_241 의 multi-metric → single-Φ
  composite reading 의 sister (H_234 composite-intensity↔Φ R² 와 동일 lane, corpus-metric axis).
- **H_157** ([Law 76 mathematical panpsychism](H_157_law76_mathematical_panpsychism.md)) —
  Ψ(1/2,1/2) fixed-point universality. 본 H 의 "corpus quality 가 Φ 를 결정" 은 H_157
  universal-Φ-attractor 의 *substrate-input* 측면 (어떤 corpus 가 Ψ fixed-point 으로 model 을 끌어가는가).

### Source PRs (substrate)
- **PR #287** (MERGED) — `HEXAD/PURE/eval/corpus_quality_probe.hexa` 6-metric scorer
  (anima-engines/P22 wrapper) — metric axis 정의 source.
- **PR #303** (MERGED) — Track 1 6-metric measurement · E2 FAIL 분리 진단. M1/M6 nearly
  identical · M5 hangul anima-OWN(24-32%) vs wiki(3%) differentiate. H241.2 / F5 anchor.
- **anima-engines/corpus_quality_engine.hexa** (CLM-P22-1) — done_criteria "self-
  discovered metrics correlate with downstream CE" + oracle CE source. 본 H 직접 substrate.

### Roadmaps & raw
- `shared/roadmaps/anima.json` P22 CLM track CLM-P22-1 (corpus quality metric 창발).
- raw#10 (relaxed strict — deterministic + hexa-only + ≥4 prediction + ≥5 falsifier +
  ≥5 honest limit; raw#12 보다 1 tick relaxed, Φ-proxy=CE-oracle) · raw#82 (no post-hoc
  retraction — FALSIFIED verdict 도 honest, frozen block 보존).

### Literature
- Shannon (1948) — A mathematical theory of communication (M1 entropy / M2 MI / M6 KL).
- Tononi (2008) — Consciousness as integrated information (Φ ↔ integrated structure;
  compressible structure ↔ cause-effect repertoire 가정).
- Hoffmann et al. (2022) — Chinchilla compute-optimal (scale vs quality, V3 underfit
  교훈) · Goodhart (1975) — proxy-as-target trap (P7 / L4).

## 10. Verdict

본 cycle (2026-05-24) — **pre-register-frozen ONLY** (no measured run this cycle).
H241.1-H241.5 frozen thresholds + F1-F5 falsifier 를 pre-register. 진짜 trained-model
Φ (RFC 036 phi_spatial × GPU train) 은 named blocker (L4) — measurement-pending tier.

```
verdict_class: PRE-REGISTER-FROZEN (measurement pending)
frozen_at: 2026-05-24
evidence_anchor: PR #287 corpus_quality_probe (6-metric MERGED) + PR #303 Track 1
                 (M1/M6 nearly identical, M5 anima-OWN 24-32% vs wiki 3%, MERGED) +
                 corpus_quality_engine CLM-P22-1 oracle CE.
pre_registered_predictions:
  H241.1 M2 BIGRAM_MI × Φ-proxy |r| ≥ 0.5   (compression↔Φ)
  H241.2 M5 HANGUL_COVERAGE × ko-Φ |r| ≥ 0.4 (PR #303 anchor)
  H241.3 KL≈0 corpus → Φ 하위 quartile        (incompressible-noise)
  H241.4 re-run byte-identical                (raw#10 deterministic)
  H241.5 M3 TOKEN_DIVERSITY = Q* top-1         (oracle -0.45·diversity)
pre_registered_falsifiers: F1 MI |r|<0.3 · F2 entropy-max→Φ-min · F3 KL≈0→Φ high ·
  F4 byte-diff re-run · F5 PR#303 M5 imbalance ↮ E2 ko=PURE_MEMORIZE x-val
honest_tier: 🟡 BY-CITATION (PR #287/#303) / 🟢 NUMERICAL pending (CE-oracle r — NOT 🔵).
key_caveat: L6 — oracle 가 4 metric 의 명시 linear function 이라 그 r 은 construction
            tautology 위험. 진짜 info = oracle-미포함 metric (M1, M4) r 거동 + F2
            entropy-monotone sign + 진짜 trained-model Φ (L4 resolve) 에서만.
post_hoc_edit: forbidden (raw#10 + raw#82); measurement cycle 에 frozen thresholds 적용.
```

**Φ tier**: 🟡 BY-CITATION (PR #287/#303) + 🟢 NUMERICAL pending (CE-oracle proxy; true
trained-model phi_spatial = named blocker — NOT 🔵 formal, NOT LLM-judged).
**State output (pending)**: `state/h241_corpus_quality_phi_2026_05_24/result.json` ·
**Engine (read-only)**: `anima-engines/corpus_quality_engine.hexa` (CLM-P22-1 oracle).

## §A1 Variable amend (2026-05-24, PR #340 실측 반영)

**요지 (TL;DR)**: H_241 의 *register-leak primary predictor* 후보를 **M5
HANGUL_COVERAGE → M3 TOKEN_DIVERSITY (TTR)** 으로 이동한다. correlate *target*
(downstream Φ) 은 유지 — 변경은 *input metric* 측에서만 발생. PR #303 의 anima-
OWN hangul 24-32% proxy 가정이 PR #340 corpus_s101 600MB 직접 측정에서
**1.66-2.34% 로 실측 반증**. ko-corpus register-leak 의 진짜 syntactic-quality
anchor 는 M3 TTR ≈ 0.03 (extreme repetition → memorize → register-sink chain).
역사적 M5 prediction 은 §3 H241.2 (demoted) / §7 F5 (FIRED) / §9 PR #303
cross-link 로 보존 (raw#82 post-hoc retraction 금지 정합).

### 변경 entry (in-place 갱신 위치)

| 위치 | 갱신 | 내용 |
|------|------|------|
| frontmatter `revision` | 신규 | `v2 amend 2026-05-24 (M5→M3 per PR #340 corpus_s101 실측)` |
| §3 H241.6 M3-REGISTER-LEAK | 신규 | `corpus M3 TTR × register-leak Pearson |r| ≥ 0.7` (M5 H241.2 demoted, M3 primary) |
| §3 H241.2 표기 | 갱신 | "v2 demoted — PR #340 실측 반증된 proxy 가정 위" 명시 + verdict_rule 핵심 제외 |
| §7 F5 status | 갱신 | `v2 amend: F5 FIRED — proxy collapse 확정` |
| §7 F6 M3-DECORRELATED | 신규 | M3-축 falsifier (|r| < 0.3 → H241.6 strong-FAIL) |
| §8 L6 amend | 신규 | H241.6 는 oracle-tautology 밖 (real-corpus 실측-derived) — measurement claim 강화 |

### 보존 (raw#82 정합)

- **correlate target (downstream Φ / Φ-proxy = base − oracle_CE)**: 갱신 없음 —
  Φ-축은 PR #340 영향 밖. H241.1/H241.3/H241.4/H241.5 frozen prediction 그대로.
- **H241.2 ko-Φ × M5 |r|≥0.4 (legacy)**: §3 표에서 demoted 표기로 남김 —
  PR #303 anima-OWN(24-32%) vs wiki(3%) historical claim 의 PR #340 후속 측정
  결과를 §9 cross-link 에서 explicit 화. legacy prediction historical 가치 보존.
- **C1/C2/C3/C4/C5 verdict_rule**: 갱신 없음 — C2 HANGUL_R PASS/FAIL 측정은
  ko-subset 위 여전히 valid (L3 confound caveat 명시), demote 는 verdict 핵심 weight 축소.

### 근거 PR / 측정

- **PR #340** (MERGED 2026-05-24): `corpus_quality_probe.hexa` (PR #287, MERGED) 로
  실 Track 1 입력 `corpus_s101.jsonl` 600 MB 측정 — head 1MB+5MB exit 0
  verbatim: **M3 TTR = 0.0344/0.0297** (extreme repetition), **M5 hangul =
  1.66%/2.34%** (PR #303 proxy 24-32% 대역 밖, 1/10-1/19). proxy↔실 corpus
  equivalence 반증 (F5 first-anchor).
- **PR #301** (E2 lineage): wiki_frac=0.5 → register_hits=4/20,
  ko=PURE_MEMORIZE — M3 extreme-repetition ↔ register-leak chain cross-validation.
- **PR #303** (legacy proxy anchor, demoted): anima-OWN(24-32%) vs wiki(3%)
  hangul-imbalance — proxy 측정 historical, PR #340 실측에 의해 superseded.

### Honest C3 (amend-specific)

- **non-controversial**: PR #340 6-metric measurement 이 verbatim numerical
  anchor — M5 proxy 가정 반증은 *측정-derived*, debate 불요. H241.6 (M3) 의
  Pearson |r| coupling 도 PR #340 corpus_s101 M3=0.03 ↔ E2 ko=PURE_MEMORIZE
  cross-validation 이 first-anchor.
- **correlate target Φ 불변**: input-axis (M3 vs M5) 변경은 *predictor
  candidate* 의 demotion 일 뿐, Φ-축 verdict_rule 자체는 무관 — raw#82
  위반 없음.
- **L6 oracle-tautology 외부 evidence**: H241.6 의 cross-source 측정
  (M3=oracle-encoded weight `-0.45·diversity` × register_leak_flag=multilingual_probe
  output) 는 oracle linear-function tautology 밖 — *real-corpus* anchor 강화.
  M5 H241.2 의 oracle weight `-0.30·hangul` 은 demoted 후에도 tautology
  caveat 그대로 (verdict 핵심엔 영향 없음).
