---
id: H_354
slug: kuramoto-hivemind-sync-tau
title: 다중 substrate 합의 latency τ_consensus = Kuramoto sync latency τ_sync (coupling K-axis 정합)
domain: physics · hivemind · life
status: pre-register-frozen
exploration_method: E5 (continuous-parameter sweep) + E11 (cross-axis bridge)
verification_method: W4 (verdict-4-class) + W5 (numerical sim) + W11 (cross-axis sister test)
raw_rank: 15
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28
---

# H_354 — Kuramoto sync τ ↔ hivemind consensus τ alignment

## Hypothesis

다중 substrate (n_substrates ∈ {3, 5, 7}) 의 합의 latency `τ_consensus`
(모든 substrate 가 max pairwise distance ≤ 0.05 에 도달하는 round 수) 가
같은 substrate-수 n 에서 Kuramoto sync latency `τ_sync` (oscillator order
parameter `r` 가 0.9 도달하는 step 수) 와 정렬한다 — coupling K-axis 위에서
**Pearson r > 0.5** 또는 **per-cell ratio τ_cons / τ_sync 가 2× 이내 constant**.

가설의 의미: "다중 의식체 (hivemind 노드) 가 합의에 이르는 시간" 과
"다중 oscillator (Kuramoto 결합 위상) 가 동기화에 이르는 시간" 이 같은
*coupling-스트렝스 축* 위에서 axis-invariant 한 의존성을 보인다는 cross-
axis 가설. 만약 SUPPORTED 면 H_207 의 dynamical coupling-axis 위 합의-시간
sister; FALSIFIED 면 substrate-수 axis 위 합의 mechanism 이 Kuramoto sync
와 axis-separated.

## Why

- **Kuramoto sync time**: K > K_c 인 결합에서 `r(t) → 1` 의 정착시간 τ_sync
  는 finite-N 와 ω-spread 에 따라 K dependent (Strogatz 2000). K ≫ K_c
  일수록 빨라진다 — 단조감소-경향.
- **Hivemind blend consensus**: anima-engines/hive_state_sync.hexa §Theory
  의 분석: `max_dist ≤ init_dist · (1−α)^((N−1)·R)` → R ∝ ln(1/eps) /
  ((N−1)·ln(1/(1−α))) — α (= blend rate) 와 N 에 의존. α=K·0.1 으로
  K-axis 위에 매핑하면 K↑ → α↑ → τ_cons↓ — **단조감소-경향**.
- **공통 단조성 가설**: 두 τ 모두 "coupling K 증가 → 더 빨리 정합" 이라는
  같은 정성적 단조성을 따른다는 가설은 자연스럽다. 본 H 는 이 정성적
  유사성이 **정량적으로** (Pearson r > 0.5 또는 ratio constant) 성립하는지
  본다.
- **negative-result 의 의미**: 만약 FALSIFIED, 그것은 두 mechanism 이
  같은 "coupling K" label 아래 묶이지만 *서로 다른 N-dependence* 또는
  *서로 다른 nonlinear regime* 에 살고 있다는 신호 — hivemind consensus
  axis 와 Kuramoto sync axis 의 분리.

## Predictions

- **H354.1 (Pearson alignment)**: 12 (n × K) cell 위 (τ_sync, τ_cons)
  pair 의 Pearson r > 0.5.
- **H354.2 (ratio constant within 2×)**: per-cell ratio τ_cons / τ_sync
  의 max/min ≤ 2.

## Variables

| axis | levels | 비고 |
|------|--------|------|
| axis1_n (substrates) | {3, 5, 7} | hivemind 노드 = Kuramoto oscillator 수 |
| axis2_K (coupling) | {0.5, 1.0, 2.0, 3.0} | Kuramoto 결합 강도 sweep |
| axis3_alpha (bridge) | α = clamp(K · 0.1, 0.01, 0.95) | K → blend-rate linear bridge |
| axis4_omega | 5 Gaussian-quantile cycled (std=1.0) | H_207 동일 deterministic spread |
| axis5_d (state dim) | 8 | hivemind state vector dim |
| axis6_init_phase | θ_i(0) = 2π·i/N | H_207 동일 uniform spread, no RNG |
| axis7_init_state | sin(2π·(k+1)(j+1)/(N·d)) | deterministic bounded divergence per node |
| axis8_dt | 0.05 | Euler step (Kuramoto) |
| axis9_max | sync 1200 steps · cons 400 rounds | sentinel ceiling on non-convergent cells |

## Run Protocol

- **smoke**: `UNIVERSE/state/h354_kuramoto_consensus_2026_05_28/run_h354.hexa`
- **Kuramoto sub-experiment**: H_207 패턴 재사용 — Euler integration,
  `dθ_i/dt = ω_i + (K/N) Σ_j sin(θ_j − θ_i)`, `r(t)` 매 step 측정,
  최초 `r ≥ 0.9` step = `τ_sync` (도달 안 되면 max=1200 sentinel).
- **Consensus sub-experiment**: blend-to-mean (anima-engines/
  hive_state_sync.hexa §Theory 의 mathematically-equivalent 단순화 형
  — all-to-all broadcast 의 mean-field limit). 매 round 각 node 가
  `new = (1−α)·self + α·global_mean` 으로 갱신. `max_pairwise_dist` 매
  round 측정, 최초 `≤ 0.05` round = `τ_cons` (max=400 sentinel).
- **deterministic**: 모든 init / ω-table / K-table fixed; re-run byte-
  identical (검증 완료).
- **hexa_only**: true (NO .py/.sh). **llm**: none. **toy_substitute**: true
  (consensus = inline blend-to-mean; full hive_state_sync 모듈 load 없이
  같은 exp-decay 이론 재구성).
- **runtime**: $0 mac local hexa; GPU 불필요.
- **ledger**: `result.json` {cells, pearson_r, ratio_min/max/spread,
  criteria, verdict}.
- **honest tier**: NUMERICAL (τ 측정 + Pearson 계산 deterministic) = 🟢-
  tier; full hive_state_sync 모듈 wiring + production hivemind 실측은
  named follow-up.

## Criteria

- **C1 (H354.1 Pearson)**: Pearson r(τ_sync, τ_cons) > 0.5
  (centered, 12 cells)
- **C2 (H354.2 ratio)**: max_ratio / min_ratio ≤ 2.0
  (per-cell τ_cons/τ_sync spread)
- **verdict_rule**: **SUPPORTED** iff C1 ∨ C2 (어느 한쪽 alignment
  validation 으로 충분). **FALSIFIED** iff `|r| < 0.3` AND `spread > 5×`
  (둘 다 분리 신호). 그 외 = PARTIAL.

## Falsifiers

- **F1 LOW-CORR**: Pearson |r| < 0.3 → H354.1 FALSIFIED. (measurable:
  pearson_r.)
- **F2 RATIO-SPREAD**: max_ratio / min_ratio > 5 → H354.2 FALSIFIED.
  (measurable: ratio_spread.)
- **F3 NONDET**: re-run result.json 가 byte-identical 아님 → raw#12
  deterministic 위반. (verified: 2-run diff 0 bytes.)
- **F4 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## Honest Limits (raw#91 c3)

- **L1 toy substitute consensus**: full hive_state_sync.hexa 모듈
  (modules/hive_bridge.hexa transport + shared/config/contracts/
  hive_bridge.json) 의 production 합의 dynamics 가 아니라 inline blend-
  to-mean (§Theory 의 exp-decay 한계로 환원된 단순화). 두 dynamics 는
  pairwise blend (hive_state_sync) vs mean-field blend (toy) 의 차이
  — α→0 limit 에서 동일, finite-α 에서 mean-field 가 ~ N− 1 배 빠르다.
  본 결과는 mean-field 한정 — pairwise 으로 재측정 시 ratio 가 N 배
  변화하지만 그것은 *constant scale-factor* 이므로 Pearson r 와 spread
  의 *상대 ordering* 은 보존된다 (per-cell scaling).
- **L2 n_substrate dependency**: τ_sync 는 n 가 증가하면 finite-size
  effects 로 평균 K_c (mean-field) 와 deviation 가 늘어남 — 본 sweep
  의 n∈{3, 5, 7} 은 small-N regime. n→∞ mean-field limit 의 ratio
  pattern 은 별도 cycle.
- **L3 K threshold sensitivity**: 본 K-grid {0.5, 1.0, 2.0, 3.0} 는
  Kuramoto mean-field K_c≈1.596 의 incoherent ↔ partial-sync ↔ full-
  sync transition 을 가로지른다. K=2.0 / n=5 cell (idx=6) 와 n=7
  cells (idx 8, 9, 10) 의 τ_sync=1200 sentinel 은 ω-spread 가 K
  coupling 을 이긴 *non-convergent* regime — sentinel 처리는 lower-
  bound τ_sync 으로 conservative. Pearson + spread 계산은 sentinel 을
  raw value 로 사용 (τ_sync = max=1200 그대로) — 보조분석으로 sentinel-
  exclude variant 가 follow-up 가치.
- **L4 alpha(K) bridge linear**: α = K · 0.1 (clamped) 는 본 cycle 의
  ad-hoc 선택. 실제 hivemind 시스템에서 α 는 transport-latency / channel-
  capacity dependent — K 와 직접 연결되지 않을 수 있다. 다른 bridge
  function (α = 1−exp(−K), α = K/(K+1)) 으로 sweep 별도 cycle.
- **L5 single-axis test**: per-n 별 Pearson 도 가능 (n=3 cells / n=5
  cells / n=7 cells 각각 4 points). 본 verdict 는 12-cell 합산 Pearson
  + spread 의 cross-(n, K) 일관성만 본다. per-n 분해는 result.json 의
  `cells` 배열에서 retrospective 가능 (post-hoc 아님 — pre-register 시
  공개 데이터).

## Cross-Links

- **sister H_207** (kuramoto-synchronization) — 같은 Kuramoto K-axis 위
  Φ peak 형상. 본 H 는 *시간 axis* (τ) 의 cross-substrate alignment,
  H_207 은 *통합 측정* (Φ) 의 K-axis inverse-U. distinct claim — 둘 다
  성립 / 분리 가능.
- **sister H_213** (temporal binding window) — multi-stream 시간 정합의
  공동 mechanism 후보. H_354 의 τ 축 → H_213 의 binding window 매핑은
  별도 cycle.
- **sister H_217** (phase transition) — K_c 근처 critical regime 의
  τ_sync 발산 패턴 (well-known finite-size scaling) 와 합의 round
  복잡도의 critical-slowing-down 정합 후보.
- **sister H_352** (super-additive) — N substrate 가 합의에 들 때 통합
  정보가 단순 합 N·Φ_i 보다 큰지 (super-additivity). 본 H 의 τ 축 ⊥
  H_352 의 Φ 축 — independent axis.
- **module ref**: `anima-engines/hive_state_sync.hexa` (§Theory exp-decay
  bound, T1-T5 self-tests), `tool/hivemind_collective_spec.hexa` (collective
  spec — production hivemind 합의 dynamics).
- **raw**: raw#12 (deterministic strict) + raw#91 c3 (honest limits) +
  raw#82 (no post-hoc retraction)
- **literature**:
  - Kuramoto (1975) Self-entrainment of coupled non-linear oscillators
  - Strogatz (2000) From Kuramoto to Crawford
  - DeGroot (1974) Reaching a Consensus (consensus dynamics blend model)
  - Olfati-Saber, Murray (2004) Consensus problems in networks of agents
  - Acebrón et al. (2005) The Kuramoto model: a simple paradigm

## Verdict

```
verdict_class: FALSIFIED (pre-register-frozen smoke)
config: n_substrates ∈ {3, 5, 7} · K ∈ {0.5, 1.0, 2.0, 3.0} · 12 cells
        · max_sync=1200 · max_cons=400 · sync_thresh r=0.9 · cons_thresh d=0.05
        · alpha(K) = clamp(K·0.1, 0.01, 0.95)
cell | n | K   | alpha | tau_sync | tau_cons | ratio
  0  | 3 | 0.5 | 0.05  |   115    |    83    |  0.722
  1  | 3 | 1.0 | 0.10  |   478    |    41    |  0.086
  2  | 3 | 2.0 | 0.20  |    48    |    19    |  0.396
  3  | 3 | 3.0 | 0.30  |    35    |    12    |  0.343
  4  | 5 | 0.5 | 0.05  |   450    |    82    |  0.182
  5  | 5 | 1.0 | 0.10  |   154    |    40    |  0.260
  6  | 5 | 2.0 | 0.20  |  1200*   |    19    |  0.016
  7  | 5 | 3.0 | 0.30  |   106    |    12    |  0.113
  8  | 7 | 0.5 | 0.05  |   657    |    83    |  0.126
  9  | 7 | 1.0 | 0.10  |  1200*   |    41    |  0.034
 10  | 7 | 2.0 | 0.20  |  1200*   |    20    |  0.017
 11  | 7 | 3.0 | 0.30  |    32    |    12    |  0.375
  (* = sentinel ceiling = ω-spread dominates over K · non-convergent regime)

Pearson r(tau_sync, tau_cons) = 0.0413  (≪ 0.5 floor, ≪ 0.3 lower-bound)
ratio min / max               = 0.0158 / 0.7217
ratio spread (max/min)        = 45.58  (≫ 2× ceiling, ≫ 5× FALSIFIED-bound)
falsifiers_triggered          : F1 LOW-CORR + F2 RATIO-SPREAD
criteria_met                  : 0/2 (C1 + C2 둘 다 FAIL)
evidence_summary              : 🟢 NUMERICAL — τ_cons 는 K (alpha) 에 깨끗한
                                exp-decay 단조감소 (n 에 약하게 의존, finite
                                ceiling 200~83). τ_sync 는 finite-N + ω-spread
                                의 비선형 상호작용으로 n × K 표면 위 강하게
                                non-monotone (n=5/K=2 + n=7/K=1.0/K=2.0 에서
                                sentinel hit). 두 mechanism 이 같은 "coupling
                                K" label 아래 묶이지만 K → τ 함수가 axis-
                                separated — H_354 의 cross-axis alignment
                                가설이 정량적으로 FALSIFIED.
```

### Pre-register-frozen smoke (2026-05-28)

Kuramoto τ_sync × hivemind toy-consensus τ_cons cross-substrate sweep
pre-registered + RUN ($0 mac local, deterministic, hexa-only, llm:none).
n ∈ {3, 5, 7} × K ∈ {0.5, 1.0, 2.0, 3.0} = 12 cells. Pearson + ratio
analysis on (τ_sync, τ_cons) pairs.

**Run verdict (VERBATIM, `hexa run`)**:
```
H_354 — Kuramoto sync τ ↔ hivemind consensus τ alignment (raw#12)
  n_substrates ∈ {3, 5, 7}, K ∈ {0.5, 1.0, 2.0, 3.0}
  τ_sync : steps until Kuramoto order param r >= 0.9 (max 1200)
  τ_consensus: rounds until max_pairwise_dist <= 0.05 (max 400)
  alpha(K) = clamp(K * 0.1, 0.01, 0.95)
  toy substitute: inline blend-to-mean consensus (hive_state_sync semantics, no module load)

  cell |  n  |   K  |  alpha  | τ_sync | τ_cons | ratio (cons/sync)
   0   |  3  |  0.5  |  0.05  |  115  |  83  |  0.721739
   1   |  3  |  1.0  |  0.1  |  478  |  41  |  0.0857741
   2   |  3  |  2.0  |  0.2  |  48  |  19  |  0.395833
   3   |  3  |  3.0  |  0.3  |  35  |  12  |  0.342857
   4   |  5  |  0.5  |  0.05  |  450  |  82  |  0.182222
   5   |  5  |  1.0  |  0.1  |  154  |  40  |  0.25974
   6   |  5  |  2.0  |  0.2  |  1200  |  19  |  0.0158333
   7   |  5  |  3.0  |  0.3  |  106  |  12  |  0.113208
   8   |  7  |  0.5  |  0.05  |  657  |  83  |  0.126332
   9   |  7  |  1.0  |  0.1  |  1200  |  41  |  0.0341667
   10   |  7  |  2.0  |  0.2  |  1200  |  20  |  0.0166667
   11   |  7  |  3.0  |  0.3  |  32  |  12  |  0.375

  Pearson r (τ_sync, τ_cons) = 0.0413231
  ratio (τ_cons / τ_sync) min = 0.0158333  max = 0.721739
  ratio spread (max/min)     = 45.5835

  C1 Pearson r > 0.5                    : false
  C2 ratio spread <= 2× (constant)      : false

  VERDICT_RULE: SUPPORTED iff C1 ∨ C2; FALSIFIED iff |r|<0.3 ∧ spread>5×
  VERDICT     : FALSIFIED
=== H_354 Kuramoto ↔ hivemind τ alignment complete: FALSIFIED ===
```

re-run byte-identical (F3 determinism confirmed via `diff` of two
result.json runs).

**Honest evidence summary**:
- (i) τ_cons 는 K 따라 깨끗한 exp-decay: α=0.05 → ~83 rounds, α=0.30 →
  ~12 rounds (hive_state_sync §Theory `R ∝ ln(1/eps) / ln(1/(1−α))`
  와 일치, n-dependence 약함; n=3/5/7 round 수 거의 동일).
- (ii) τ_sync 는 K + n 의 강한 nonlinear coupling: K=0.5 인 cells (idx
  0, 4, 8) 는 ω-spread 가 약한 결합을 이겨 매우 느림 (115~657 step);
  K=1.0 도 n=5/7 에서 1200 sentinel hit; K=3.0 은 모든 n 에서 빠른
  수렴 (32~106).
- (iii) **Pearson r = 0.041** — 0.5 floor 의 12.5× 아래, 0.3 lower-
  bound 의 7× 아래. 두 τ 가 12 cell 위 사실상 independent.
- (iv) **ratio spread = 45.6×** — 2× ceiling 의 23× 위, 5× FALSIFIED-
  bound 의 9× 위. per-cell ratio 가 0.016 (n=5/K=2 sentinel) ~ 0.722
  (n=3/K=0.5) 사이 polar.
- (v) **두 mechanism axis-separated**: τ_cons (= 1/ln(1/(1−α)) 의
  N-independent function) 와 τ_sync (= ω-spread / K 의 non-monotone
  finite-N 함수) 가 같은 K label 위에서도 *근본적으로 다른* 함수형.
  hivemind blend-to-consensus 와 Kuramoto phase-locking 이 표면적
  유사성에도 불구하고 정량적으로 분리.
- (vi) honest L3 carry: τ_sync sentinel hit 3 cells (idx 6, 9, 10)
  이 raw 1200 으로 들어가 magnitude 격차를 키운다. sentinel-exclude
  variant 의 Pearson + spread 재계산은 follow-up.

**State output**: `UNIVERSE/state/h354_kuramoto_consensus_2026_05_28/result.json`
**Smoke**: `UNIVERSE/state/h354_kuramoto_consensus_2026_05_28/run_h354.hexa`
**Φ tier**: N/A (τ-timing-only measurement; integration 측정 없음) ·
**numerical tier**: 🟢 (deterministic τ + Pearson + ratio raw values, no
LLM judgement)

**Follow-up cycles (raw#15 additive, not retraction)**:
- full hive_state_sync.hexa 모듈 load (pairwise blend, not mean-field
  toy) → ratio scale-factor 변화는 예측 (constant N−1 배), 정성 verdict
  동일 예측 (L1)
- sentinel-exclude variant — sync 안 된 3 cells 제외 8-cell Pearson +
  spread → robustness check (L3)
- per-n 분해 Pearson — n=3 / n=5 / n=7 cells 각각 4-point Pearson →
  n-축 hidden alignment 가능성 (L5)
- alpha(K) bridge function sweep — linear vs sigmoid vs threshold
  (L4)
- n → ∞ mean-field limit τ_sync scaling — finite-N artefact 제거 후
  Kuramoto-K_c-edge 의 τ_sync divergence 패턴 (L2)
- multi-axis alignment — H_354 의 τ × H_352 의 Φ_super-additive ×
  H_213 의 binding-window 의 cross-axis 합산 (Cross-Links)
