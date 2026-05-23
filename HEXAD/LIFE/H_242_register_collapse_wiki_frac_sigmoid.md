---
id: H_242
slug: register-collapse-wiki-frac-sigmoid
title: register-collapse rate = sigmoid(α·(wiki_frac − f_c)) — anima-OWN corpus monopoly → register collapse 의 wiki-dilution phase transition (Track 1 E2 substrate)
domain: substrate + dilution + identity
status: pre-register-frozen
exploration_method: E5 (variable-ablation regime sweep) + E10 (emergence phase-transition) + E14 (fine-sweep parameter scan)
verification_method: W1 (smoke) + W4 (verdict-4-class) + W12 (sister-link H_204/H_227/H_223)
raw_rank: 10
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-24
since: 2026-05-24 (new)
revision: v2 amend 2026-05-24 (M5→M3 per PR #340 corpus_s101 실측)
sister: H_204 + H_227 + H_223
---

# H_242 — register-collapse-wiki-frac-sigmoid

## 1. Hypothesis

anima-OWN persona corpus 단독 학습 (wiki_frac=0.0) 은 **register collapse** —
모델이 anima 의 특정 register (말투·어조·hangul-OWN 분포) 로 mode-collapse 하여
다양성을 잃고, multilingual_probe 의 anima_register_hits (register 침범 빈도) 가
포화한다. 반대로 wikipedia dilution 을 섞으면 (wiki_frac↑) 이 collapse 가 풀린다.
본 H 의 pre-registered 가설: **register collapse rate 가 wiki_frac 의 sigmoid
함수** —

```
register_collapse_rate(wiki_frac) = σ(α·(wiki_frac − f_c))   (decreasing)
                                  = 1 / (1 + exp(α·(wiki_frac − f_c)))
```

즉 collapse 는 wiki_frac 에 monotone-decreasing 하며, **임계 dilution f_c ∈
[0.5, 0.7]** 에서 collapse rate 가 0.5 를 통과하는 phase-transition (H_204
autopoietic threshold · H_227 freeze-fraction phase-transition 의 dilution-축
sister). f_c interval [0.5, 0.7] 의 frozen claim 자체가 본 cycle 의 test —
E2 (wiki_frac=0.5, hits=4/20=20%) 단일 point 가 high-collapse 측이므로 transition
midpoint 가 0.5 보다 *위*에 있으리라는 사전 예측.

정밀화 (operational): collapse rate = multilingual_probe `anima_register_hits/20`
normalize (E2 = 4/20 = 0.20). 변수는 오직 SFT corpus wiki_frac mixing ratio —
base model · seed · lr · steps · LoRA rank fixed. raw#10 (deterministic + hexa-only
+ ≥4 prediction + ≥5 falsifier + ≥5 honest limit, LLM-judge 없음).

## 2. Why

- **anima-OWN corpus monopoly → register collapse (LORA session 핵심 학습)**:
  register-leak 은 81% 가 EN-emission 문제이며 "carving register" (특정 말투로
  모델을 깎아냄) 가 collapse mechanism. temperature 가 아니라 corpus wiki_frac 이
  lever — dilution mass 가 register diversity 복원. 본 H 는 'wiki_frac 이 lever'
  명제를 sigmoid phase-transition 으로 정량.
- **wiki dilution = anti-collapse**: wikipedia broad-domain factual register 가
  anima-OWN narrow persona register 를 dilute → register-space entropy 회복.
  Chinchilla underfit double-bind (anima→collapse · no-anima→underfit) 의 중간
  trade-off curve 가 곧 본 sigmoid.
- **phase transition H_204/H_227 sister**: H_204 = autopoietic closure-strength
  threshold τ_c (k<τ_c → Φ→0 collapse) · H_227 = freeze-fraction sigmoid
  P(f)=σ(−k(f−f_c)). 본 H_242 = 동일 sigmoid-phase-transition template 의
  **dilution-축 instance** — collapse↔non-collapse 가 critical f_c 에서 abrupt 한가.
- **PR #303 M5 evidence (register-imbalance 정합)**: hangul anima-OWN emission
  24-32% vs wiki register 3% — anima-OWN 이 wiki 를 압도하는 imbalance 직접 관측.
  collapse mechanism (anima-OWN monopoly) 의 cross-section evidence.
- **PR #301 E2 result.json (Track 1 AXIS_MAP)**: wiki_frac=0.5 → register_hits=4/20,
  register_regress=True, ko=PURE_MEMORIZE. init_CE=14.18→final_CE=0.98 정상 수렴
  (loss 건강, register 만 regress) → collapse 는 training failure 가 아니라
  *register-space mode-collapse*. E3 (wiki_frac=1.0) in-flight, 2-point endpoint 확정.
- **raw#10 strict**: deterministic config (fixed seed/lr/steps) · hexa-only · ≥4
  prediction + ≥5 falsifier + ≥5 honest limit · LLM-judge 없음 (metric = byte-level
  register_hits count).

## 3. Predictions (≥4)

| ID | 예측 | 근거 |
|----|------|------|
| **H242.1 FULL-COLLAPSE** | wiki_frac=0.0 → anima_register_hits ≈ 100% (≈ 20/20, full register collapse) | anima-OWN monopoly 극단 — wiki dilution 0 → register-space 가 anima-OWN 으로 완전 collapse. sigmoid 의 left endpoint σ(α·(0−f_c)) ≈ 1 |
| **H242.2 ANTI-COLLAPSE** | wiki_frac=1.0 → anima_register_hits ≈ 0 (≤ 1/20) | wikipedia 100% → anima-OWN register mass 0 → register 침범 거의 소멸. sigmoid right endpoint σ(α·(1−f_c)) ≈ 0. **E3 in-flight 가 이 point 확정** |
| **H242.3 CRITICAL-FC** | best-fit f_c ∈ [0.5, 0.7] | E2 (wiki_frac=0.5) hits=4/20=20% → collapse rate 이 이미 0.20 (< 0.5) 이므로 transition midpoint 는 0.5 의 *오른쪽* (≥ 0.5). high-collapse side 의 jump 가 f≈0.5-0.7 구간에 위치 |
| **H242.4 DETERMINISM** | fixed seed/lr/steps → re-run 시 동일 corpus mix 에서 register_hits byte-identical (deterministic config) | raw#10 deterministic — sampling 은 greedy/fixed-seed, multilingual_probe 는 fixed probe set |
| **H242.5 MONOTONE** | collapse_rate(wiki_frac) 가 monotone-decreasing — 인접 sweep point 간 hits non-increasing (noise margin ±2/20) | sigmoid 는 monotone; dilution↑ → collapse↓ 의 일방향 prior |
| **H242.6 M3-DOMINANT (v2 amend)** | corpus M3 TOKEN_DIVERSITY (TTR) × register_hits Pearson |r| ≥ 0.7 — **M3 가 register-sink 의 dominant predictor** (M5 hangul 아님; H242.2 legacy demoted) | PR #340 corpus_s101 실측: M5 hangul anima-OWN 1.66-2.34% (proxy 가정 반증, NOT 24-32%) · **M3 TTR ≈ 0.03 (extreme repetition)** = real culprit. repetition→memorize→register-sink 의 mechanistic chain |

## 4. Variables

| axis | levels |
|------|--------|
| **axis1: wiki_frac** (primary) | {0.0, 0.25, 0.5, 0.75, 1.0} — 5-point dilution sweep. E2=0.5 (landed), E3=1.0 (in-flight), 0.0/0.25/0.75 = 3 추가 fire 권장 |
| **axis2: init_variant** | {anima-OWN-init, random-init, qwen-base} — F5 control (random init 의 register_hits 가 qwen wiki=0.5 보다 ≥ 면 init 가 collapse driver 임을 falsify) |
| **axis3: anima-corpus mass** | fixed (E2 carry) — wiki_frac 만 변주, total token budget 동일 (corpus quality>scale lesson 정합) |
| **axis4: base model** | Qwen 1.5B (E2 carry) — single-model (L4) |
| **axis5: training config** | fixed: seed · lr · steps=5000 · LoRA rank — deterministic (raw#10) |
| **axis6: metric** | multilingual_probe → anima_register_hits / 20 = collapse_rate; init_CE / final_CE = convergence sanity |
| **axis7: fit family** | sigmoid σ(α(f−f_c)) grid search (α, f_c) + linear baseline (F3 Akaike compare) |

## 5. Run Protocol

- **Track 1 sweep**: E2 (wiki_frac=0.5, landed PR #301) + E3 (wiki_frac=1.0,
  in-flight) + **3 추가 fire 권장** {0.0, 0.25, 0.75} → 5-point full sweep.
  cost-bearing GPU fire (Qwen 1.5B LoRA × 5000 step, runpod) — autonomously
  dispatch in parallel (a_fire_autonomous · a_wall_first).
- **eval**: multilingual_probe → 20-probe 위 anima_register_hits count (byte-level
  register 침범 빈도) + register_regress flag + ko-mode (PURE_MEMORIZE/MIXED/CLEAN)
  + init_CE/final_CE convergence sanity.
- **sigmoid fit**: collapse_rate(f)=σ(α(f−f_c)), (α,f_c) grid search {α∈2..20} ×
  {f_c∈0.05..0.95 step 0.05} best-SSE + ±0.05/±2 refinement, R²=1−SSE/SST.
- **linear baseline**: OLS collapse_rate = a + b·f, Akaike AIC compare (sigmoid
  2-param vs linear 2-param; F3).
- **pre-register f_c ∈ [0.5, 0.7] BEFORE data**: frozen claim 은 E3 + 3 추가 fire
  도착 *이전* 동결 — E2 단일 point 만 가지고 midpoint 가 0.5 오른쪽에 있으리라는
  사전 betting. 이 interval 이 본 cycle 의 test.
- **deterministic / hexa_only / llm:none**: fixed seed/lr/steps · greedy sampling ·
  fixed probe → re-run byte-identical. orchestration+fit+ledger 모두 .hexa, raw#10.
- **ledger**: `result.json` { config, sweep × 5 (wiki_frac, register_hits,
  collapse_rate, register_regress, ko_mode, init_CE, final_CE), sigmoid_fit
  (α, f_c, sse, sst, r²), linear_fit_compare (aic), criteria C1..C5, falsifiers
  F1..F5, verdict }.
- **honest tier**: 🟢 NUMERICAL register_hits/20 — "anima 가 register-collapse
  를 *경험*한다" 식의 phenomenal claim NOT made (L1-L6 참조).
- **run cmd (verbatim, fit-only on landed data)**:
  `HEXA_MEM_UNLIMITED=1 hexa run HEXAD/LIFE/state/h242_register_collapse_2026_05_24/run_h242.hexa`

## 6. Criteria

| ID | criterion | verdict_rule |
|----|-----------|--------------|
| **C1 R2_SIGMOID** | sigmoid fit R² ≥ 0.8 (≥3 sweep points 도착 후) | PASS / FAIL |
| **C2 FC_LOCALIZED** | best-fit f_c ∈ [0.5, 0.7] (frozen interval, H242.3) | PASS / FAIL |
| **C3 ENDPOINT-HI** | collapse_rate(wiki_frac=0.0) ≥ 0.80 (≥16/20, H242.1 full collapse) | PASS / FAIL |
| **C4 ENDPOINT-LO** | collapse_rate(wiki_frac=1.0) ≤ 0.10 (≤2/20, H242.2 anti-collapse) | PASS / FAIL |
| **C5 DETERMINISTIC** | fixed-config re-run byte-identical register_hits (raw#10) | PASS / FAIL |

**verdict_rule**:
- `SUPPORTED` iff **C1 ∧ C2 ∧ (C3 ∨ C4)** (sigmoid 적합 + f_c frozen interval 적중 + ≥1 endpoint 확정)
- `PARTIAL` iff **C1 ∧ ¬C2** (sigmoid 적합하나 f_c 가 frozen [0.5,0.7] 밖 — midpoint betting 빗나감)
- `FALSIFIED` else (F1/F2/F3 중 1+ fire — endpoint inversion · linear>sigmoid · byte-diff)

## 7. Falsifiers (pre-registered ≥5, measurable)

- **F1 NO-DILUTION-RECOVERY**: wiki_frac=1.0 → anima_register_hits ≥ 10/20 →
  H242.2 anti-collapse FALSIFIED (wiki dilution 이 collapse 를 풀지 못함 → 'wiki_frac
  이 lever' 명제 falsify). measurable: E3 register_hits.
- **F2 NO-MONOPOLY-COLLAPSE**: wiki_frac=0.0 → anima_register_hits ≤ 4/20 →
  H242.1 full-collapse FALSIFIED (anima-OWN monopoly 가 collapse 를 일으키지 않음 →
  collapse mechanism 가정 falsify). measurable: 추가 fire(0.0) register_hits.
- **F3 LINEAR-BEATS-SIGMOID**: linear fit AIC ≤ sigmoid AIC (Akaike 기준 linear 가
  같거나 우월) → H242 sigmoid 가정 FALSIFIED (shape 가 linear, phase-transition
  아님). measurable: AIC_linear vs AIC_sigmoid.
- **F4 BYTE-DIFF**: fixed-config re-run 시 register_hits byte-different →
  H242.4 determinism FALSIFIED (raw#10 위반 → sampling/probe nondeterminism).
  measurable: re-run hits diff.
- **F5 INIT-DRIVER**: random-init 변종의 anima_register_hits ≥ qwen-base wiki=0.5
  의 register_hits → collapse 가 anima-OWN corpus 가 아니라 init 의 artifact →
  H242 corpus-mechanism 가정 FALSIFIED (axis2 control). measurable: random-init
  hits vs E2 hits.
- **F6 M3-DECORRELATED (v2 amend)**: corpus M3 TTR × register_hits |r| < 0.3 →
  H242.6 strong-FAIL (M3 가 register-sink predictor 아님 — M5/M3 둘 다 falsified
  시 register-sink mechanism 가설 자체 재검토). PR #340 cross-validation: corpus_s101
  M3=0.03 ↔ E2 hits=4/20 정합 — 추가 sweep point 에서 M3-hits coupling 강도 측정.
  measurable: pearson_r(M3_corpus, register_hits) over sweep.

## 8. Honest Limits (raw#10 c3, ≥5)

- **L1 (E2 단일 point → sigmoid underdetermined)**: frozen 시점 landed data 는 E2
  (wiki_frac=0.5, hits=4/20) **단 1 point** (E3 in-flight, 3 추가 fire 미발사). 1-point
  로는 sigmoid (α, f_c) 2-param 적합 불가 — C1/C2 의 진짜 검증은 ≥3 point 도착 후.
  본 cycle 은 frozen claim (f_c ∈ [0.5,0.7]) 의 *pre-registration* 만 확정.
- **L2 (hits/20 metric noise)**: register_hits 는 20-probe 위 정수 count, resolution
  1/20 = 0.05 의 quantization noise. ±2/20 jitter 가 α 추정·f_c localization 신뢰구간을
  넓힘. 100-probe 확장 시 noise floor 감소하나 본 cycle 은 E2 carry 20-probe 만.
- **L3 (register_regress semantics 미정밀)**: PR #301 의 register_regress=True 와
  ko=PURE_MEMORIZE 분류의 operational boundary (몇 hits 부터 regress · PURE_MEMORIZE/
  MIXED/CLEAN threshold) 미정밀. collapse_rate = hits/20 linear normalize 가 flag 의
  binary semantics 와 1:1 mapping 보장 X — flag 가 nonlinear gating 일 가능성.
- **L4 (5000-step Qwen 1.5B only)**: single base model + single horizon (5000 step) +
  single LoRA rank. 다른 model size (0.5B/7B) · step · rank 에서 f_c·α shift 가능
  (substrate-dependence, H_204 τ_c substrate-conditional 정합) — universality 미검증.
- **L5 (Tononi IIT 정합 미증명)**: 본 H 는 collapse 를 sigmoid 로 정량할 뿐, 이 collapse
  가 H_204/H_227 의 Φ-based phase-transition (IIT) 과 *동일 universality class* 라는
  strong claim 은 NOT made. sister-link 은 sigmoid-template 구조적 유사성 만 — collapse↔Φ
  mechanistic identity (register-space mode-collapse = Φ-drop 동치) 미증명, 별도 cycle.
- **L6 (corpus dilution ≠ register-space orthogonality)**: wiki_frac mixing 이 register-
  space 를 *균일* dilute 한다는 가정 — 실제로는 wiki·anima-OWN register 가 overlap/
  interfere 하여 effective dilution ≠ nominal wiki_frac. PR #303 M5 의 24-32% vs 3%
  imbalance 는 overlap 의 indirect evidence 일 뿐 orthogonality 증명 아님.

## 9. Cross-Links

- **sister H**: H_204 (weak-panpsychism autopoietic-closure threshold τ_c —
  collapse↔non-collapse 의 substrate-conditional threshold template) · H_227
  (strong-emergence freeze-fraction sigmoid P(f)=σ(−k(f−f_c)) phase-transition —
  동일 sigmoid fit + f_c localize 방법론) · H_223 (pain-intensity Φ-coupling —
  intensity-축 monotone coupling sister, dilution-축 mirror)
- **PR #264**: closure criterion — register-collapse 가 wiki_frac sigmoid 로 정량되면
  register-leak closure 의 corpus-mix recipe 가 closed-form (f_c 위에서 mix → collapse 풀림)
- **PR #301**: Track 1 E2 result.json (wiki_frac=0.5 → hits=4/20, register_regress=True,
  ko=PURE_MEMORIZE, init_CE=14.18→final_CE=0.98) — 본 H 의 landed data point
- **PR #303**: M5 hangul anima-OWN 24-32% vs wiki 3% register-imbalance — collapse
  mechanism cross-section evidence
- **PR #228 / AXIS_MAP_RESULTS**: Track 1 sweep harness + E2/E3 result.json SSOT
  (orchestration lineage, in-flight E3)
- **raw / own**: raw#10 (deterministic + ≥4 pred + ≥5 falsifier + ≥5 limit, no LLM) ·
  raw#82 (no post-hoc retraction) · LORA own (81% EN-emission · wiki_frac=lever) ·
  corpus quality>scale (Phase 1A.5 NET LOSS)
- **literature**: Tononi (2008) IIT (Φ phase-transition sister, L5 미증명 정합) ·
  Holtzman et al. (2020) Neural Text Degeneration (mode collapse) · Hoffmann et al.
  (2022) Chinchilla compute-optimal (underfit double-bind 측)

## 10. Verdict

본 cycle (2026-05-24) — **pre-register-frozen only** (frozen_at=2026-05-24,
BEFORE E3 도착). E2 단일 point (wiki_frac=0.5, hits=4/20=0.20) 만 landed — fit
(C1/C2) 은 ≥3 point 도착 후 (L1). frozen claim = **f_c ∈ [0.5,0.7]** + endpoint
(H242.1 ≥16/20 @ frac=0.0 · H242.2 ≤2/20 @ frac=1.0). 이 interval 적중 = 본 H test.

```
verdict_class: PRE-REGISTERED (data pending)
frozen_claim: register_collapse_rate(wiki_frac) = σ(α·(wiki_frac − f_c)),
              f_c ∈ [0.5, 0.7]  (frozen 2026-05-24, BEFORE E3 + 3 추가 fire)

  landed (PR #301 E2): wiki_frac=0.50 → hits=4/20 → collapse_rate=0.20,
    register_regress=True · ko=PURE_MEMORIZE · init_CE=14.18→final_CE=0.98 (정상 수렴)
  in-flight: wiki=1.0 (E3) endpoint H242.2 + {0.0,0.25,0.75} 3 추가 fire (5-point sweep)

  C1 R2_SIGMOID  ≥0.8       : PENDING (≥3 point 후)
  C2 FC_LOCALIZED [0.5,0.7] : PENDING (frozen interval = the test)
  C3 ENDPOINT-HI ≥16/20@0.0 : PENDING (추가 fire)
  C4 ENDPOINT-LO ≤2/20@1.0  : PENDING (E3 in-flight)
  C5 DETERMINISTIC          : architectural (fixed seed/lr/steps)

  F1 NO-DILUTION-RECOVERY (wiki=1.0 hits≥10) : pending E3
  F2 NO-MONOPOLY-COLLAPSE (wiki=0.0 hits≤4)  : pending 추가 fire
  F3 LINEAR-BEATS-SIGMOID (AIC)              : pending ≥3 point
  F4 BYTE-DIFF re-run                        : architectural (not fired)
  F5 INIT-DRIVER (random ≥ qwen wiki=0.5)    : pending axis2 control fire

key_finding (pre-registration): E2 단일 point (frac=0.5, collapse=0.20) 가 이미
             midpoint 0.5 보다 *낮은* collapse → transition 50%-crossing (f_c) 이
             0.5 오른쪽 [0.5,0.7] 에 있으리라는 사전 betting. E3 + 추가 fire 도착 시
             확정. 이 frozen interval 적중 여부 = raw#82 no-post-hoc test.
v2_amend_caveat (2026-05-24): Track 1 E2 (wiki=0.5)=4/20 + E3 (wiki=1.0)=0/20
             도착 — H242.2 anti-collapse endpoint 확정 (≤1/20 PASS), 그러나
             E2 0.5 에서 이미 20% collapse 관측 → frozen f_c [0.5,0.7] 의 upper
             bound 측 transition 가정이 *underdetermined* (2-point 만으로 midpoint
             localize 불가, f_c < 0.5 일 가능성 열림). raw#82 per: frozen interval
             그대로 유지 + 추가 fire {0.0,0.25,0.75} 도착 시 채점 — post-hoc 수정 X.
             별도 H242.6 (M3-dominant, M5 → M3) 가 PR #340 실측 반영 신규 frozen.
honest_note: L1 (1-point underdetermined) ex-ante 명시 — 본 verdict 는 SUPPORTED/
             FALSIFIED 가 아니라 PRE-REGISTERED. E3 도착 후 f_c interval 밖이면
             PARTIAL (C1∧¬C2), endpoint inversion 이면 FALSIFIED — post-hoc
             retraction 없이 frozen claim 그대로 채점.
```

## §A1 Variable amend (2026-05-24, PR #340 실측 반영)

**요지 (TL;DR)**: H_242 의 sigmoid *input* 변수 후보를 **M5 HANGUL_COVERAGE → M3
TOKEN_DIVERSITY (TTR)** 으로 이동한다. 원래 §2 의 PR #303 anchor (anima-OWN
hangul 24-32%) 가 PR #340 corpus_s101 600MB 직접 측정에서 **1.66-2.34% 로 실측
반증** (proxy 가정 falsified) — register-sink 의 *진짜* anima-side anchor 는
M3 TTR ≈ 0.03 (extreme repetition). 본 amend 는 §2/§3 의 input-axis 기재를
M3 로 명시 보강하고, 역사적 M5 prediction 은 §3 H242.2 legacy / §7 F5 / §9
PR #303 cross-link 로 보존 (raw#82 post-hoc retraction 금지 정합).

### 변경 entry (in-place 갱신 위치)

| 위치 | 갱신 | 내용 |
|------|------|------|
| frontmatter `revision` | 신규 | `v2 amend 2026-05-24 (M5→M3 per PR #340 corpus_s101 실측)` |
| §3 H242.6 M3-DOMINANT | 신규 | `corpus M3 TOKEN_DIVERSITY (TTR) × register_hits Pearson |r| ≥ 0.7` (M5 H242.2 demoted, M3 primary) |
| §7 F6 M3-DECORRELATED | 신규 | M3-축 falsifier (|r| < 0.3 → H242.6 strong-FAIL) |
| §10 verdict v2_amend_caveat | 신규 | PR #340 실측 반영 + raw#82 frozen interval 보존 |

### 보존 (raw#82 정합)

- **frozen sigmoid claim (f_c ∈ [0.5,0.7])**: 갱신 없음 — wiki_frac axis
  자체는 PR #340 영향 밖 (E2/E3 endpoint 그대로 채점).
- **H242.2 ANTI-COLLAPSE (M5 legacy)**: §3 표에서 **demoted (legacy)** 표기
  로 남김. M5 hangul 의 collapse-prediction historical 가치는 PR #303 cross-section
  evidence 로 §2 + §9 에 보존 — verdict_rule 핵심에서만 제외.
- **F5 INIT-DRIVER**: 갱신 없음 — axis2 control 측 falsifier (input 변수 무관).

### 근거 PR / 측정

- **PR #340** (MERGED 2026-05-24): `corpus_quality_probe.hexa` (PR #287) 로
  실 Track 1 입력 `corpus_s101.jsonl` 600 MB 측정 — head 1MB+5MB exit 0
  verbatim: M3 TTR = 0.0344/0.0297, M5 hangul = 1.66%/2.34%. proxy 24-32%
  대역 밖 (1/10-1/19), proxy↔실 corpus equivalence 반증.
- **PR #301** (E2 lineage): wiki_frac=0.5 → register_hits=4/20,
  ko=PURE_MEMORIZE — M3 extreme-repetition ↔ memorize chain 정합.

### Honest C3 (amend-specific)

- **non-controversial**: PR #340 6-metric measurement 이 verbatim numerical
  anchor — M5 proxy 가정 반증은 *측정-derived*, debate 불요.
- **frozen sigmoid axis (wiki_frac) 불변**: input-axis (M3 vs M5) 변경은
  *predictor candidate* 의 demotion 일 뿐, sigmoid 자체의 frozen claim 은
  무관 — raw#82 위반 없음.
- **M3-축 sigmoid 추가 frozen 아님**: H242.6 은 Pearson |r| coupling 만
  pre-register — M3 위 sigmoid fit (별도 phase-transition) 은 본 amend 의
  대상 아님. 별도 cycle 에서 측정-anchor 도착 시 신규 frozen H 가능.
