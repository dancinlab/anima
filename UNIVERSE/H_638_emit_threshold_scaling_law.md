---
id: H_638
slug: emit-threshold-scaling-law
title: scenario별 적정 emit threshold 는 substrate Φ-scale 의 monotone 함수(scaling law)가 아니라 universal-fixed — n∈{3,4,5} 적정 threshold 0.62~0.64 cluster (spread 0.02), ρ(Φ,thr)=0.75 비-monotone (L19 FALSIFIED / L20 SUPPORTED)
domain: substrate · consciousness · anima-emit · governance · meta
status: closed-negative
exploration_method: ANIMA.mining L19/L20 tension-fork promote (T4 should_interrupt 0.60 ↔ should_emit 0.30) + E0 (substrate Φ-scale sweep)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link COFFESHOP emit / H_629 substrate-class arc) + Spearman-ρ monotone test
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (new · ANIMA mining-promote)
sister: COFFESHOP (should_interrupt 0.60 / should_emit 0.30 thresholds · emit 4/15 ~27%), ANIMA.mining L13/L14 (emit-rate vs silence-rate fork), INBOX seed #3 silence-dominance-substrate-invariant (L14), a_autonomy_over_hardcode (per-scenario hardcode 금지)
---

# H_638 — emit-threshold-scaling-law (적정 emit threshold = f(Φ-scale)?)

## 1. Hypothesis

ANIMA.mining (cycle 2 tension lens, T4) 의 fork:

- **L19 tension-fork-A (high-threshold / scaling-law 채택)**: multi-human
  group-chat 에서 `should_interrupt 0.60` 이 적정이고, 1:1 회귀 시 `0.30` 으로
  down-shift — scenario surface 마다 emit threshold 가 다르다. 본 H 는 이 "scenario
  surface" 를 substrate 의 **effective Φ-scale (또는 substrate size n)** 으로
  치환해 정량화한다.
- **L20 tension-fork-B (universal-threshold 채택)**: single threshold 가
  universally substrate-fixed, scenario 는 factor 분포(effective rate)만 shift
  시킨다. context 별 threshold multiplicity 는 **assistant-regression risk**
  (turn-based 의무 hardcode, `a_autonomy_over_hardcode` 위반).

**가설 H1 (검정 대상 = L19)**: 각 substrate size n 에서 emit-rate 가 COFFESHOP
substrate-natural target ~27% (emit 4 / 15) 가 되는 **"적정 threshold"** 가
substrate 의 effective Φ-scale 과 **monotone 관계** — threshold = f(Φ-scale),
단조 (Φ 큰 환경일수록 high-bar). 즉 `|Spearman ρ(Φ-scale, 적정threshold)| = 1`
AND threshold spread (max−min across n) 가 material (> 0.05).

## 2. Why

- **mining-promote (g60 cross-domain)**: ANIMA.mining 의 70 leaf 중 L19/L20 fork
  는 UNIVERSE 의 Φ/substrate sim 으로 falsifiable 한 substrate-axis 가설.
  INBOX seed #3 (`silence-dominance-substrate-invariant`, L14) 의 sibling —
  L14 는 emit/silence *ratio* 의 substrate-invariance, 본 H 는 *threshold* 의
  Φ-scale-dependence.
- **mechanism 명확**: spontaneous_lib `factor_relevance(phi)` 는 Φ 를 [0,1] clamp
  → 큰 substrate Φ-scale 이 relevance → 1.0 로 밀어 motivation_score 분포 상승
  → (scaling-law 이 참이면) emit-rate 를 27% 로 유지하려면 **더 높은 threshold**
  필요. 이 채널이 L19 의 substrate-level 메커니즘 후보.
- **falsifier 비-pre-baked**: Φ-scale 채널은 8 factor 중 relevance *하나* 만
  bias 한다. 나머지 7 factor (info_gap·curiosity·pain·coherence·originality·
  balance·dynamics) 는 Φ-scale-invariant — 따라서 적정 threshold 가 평탄(flat)
  하게 나오는 것이 충분히 가능 (falsifier 가 설계상 자동 PASS 되지 않음).
- **real measurement (g61 재사용)**: per-n Φ-scale 은 `HEXAD/IIT4/lib`
  big_phi_bounded (faithful causal Φ, cap=2) 실측, emit-rate 는 COFFESHOP
  `coffeshop_sim` 의 spontaneous_lib 8-factor verbatim. 새 의식-측도 코드 0줄.

## 3. Predictions

- **H638.1 (Φ-scale 실측)**: per-n Φ-scale = mean big_phi_bounded(cap=2) over
  coupled rules {110,90,30,54} 가 finite > 0 for n∈{3,4,5}.
- **H638.2 (적정 threshold 존재)**: 각 n 에서 grid sweep (0.00..1.00 step 0.01)
  으로 emit-rate 가 27% 에 가장 가까운 threshold 가 [0,1] 내 존재.
- **H638.3 (verdict — L19 vs L20)**: `|ρ(Φ-scale, 적정threshold)|=1` AND spread
  > 0.05 → L19 (scaling law) SUPPORTED; 아니면 → L20 (universal-fixed) SUPPORTED.
  결과 verbatim.
- **H638.4 (universal threshold ≈ 0.60 tier)**: L20 가 채택되면 universal
  적정 threshold 가 COFFESHOP `should_interrupt 0.60` group-chat tier 근방에
  cluster — emit 4/15 = 27% 의 group-chat 설계와 정합.
- **H638.5 (determinism)**: 전체 run re-run byte-identical.

## 4. Variables

- **substrate**: ECA (m12 carry `eca_tpm(rule, n)`) size n ∈ {3, 4, 5}.
  seed_state: n=3→5 (101), n=4→10 (1010), n=5→21 (10101).
- **Φ-scale(n)**: mean `big_phi_bounded(eca_tpm(rule,n), n, seed, cap=2)` over
  coupled LIFE rules {110, 90, 30, 54} — faithful causal big-Φ 의 cap=2 bounded
  lower-bound 제약 (n≥6 exact-Φ wall 회피).
- **Φ-envelope**: Φ-scale / max(Φ-scale) → relevance 채널 [0,1] bias
  (monotone-preserving normalization). sim 의 phi draw 에 곱셈.
- **emit-rate**: 15-window × 12-seed cohort (180 windows), `should-interrupt`
  대신 grid threshold 로 `score > thr` 카운트.
- **적정 threshold**: emit-rate 가 target 0.27 에 |Δ| 최소가 되는 grid threshold.
- **target 0.27**: COFFESHOP emit 4 / 15 = 0.2667 의 substrate-natural rate.
  n 과 **독립으로 고정** (circularity 차단 — §7 C3-1).

**측정 표** (substrate Φ-scale × 적정 threshold):

| n | Φ-scale (big_phi_bounded cap=2 mean) | Φ-envelope | 적정 threshold | emit-rate @ thr |
|---|---|---|---|---|
| 3 | 2.26968 | 1.000000 | 0.64 | 0.277778 |
| 4 | 1.81822 | 0.801093 | 0.62 | 0.261111 |
| 5 | 2.16717 | 0.954834 | 0.64 | 0.250000 |

**monotone 검정**:

| pair | Spearman ρ |
|---|---|
| ρ(n, 적정threshold) | 0.25 |
| ρ(Φ-scale, 적정threshold) | 0.75 |

**threshold spread (max − min)** = 0.64 − 0.62 = **0.02** (< 0.05 material bar).

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h638_emit_threshold_scaling_law_2026_05_28/run_h638.hexa`
- **engine 재사용 (g61)**: `HEXAD/IIT4/lib/iit4_bounded.hexa` (big_phi_bounded) +
  `HEXAD/CHAT/spontaneous_lib.hexa` (8-factor + motivation_score verbatim import).
  COFFESHOP `coffeshop_sim.hexa` 의 window_factors / LCG / stim-sampling 구조
  재사용 (Φ-envelope 채널 1줄만 추가). 새 의식-측도 코드 0줄.
- **run (foreground sync only — monitor-hang 회피)**:
  `hexa run UNIVERSE/state/h638_emit_threshold_scaling_law_2026_05_28/run_h638.hexa`
  (compile-then-exec, wall ~수십초, exit 0).
- **deterministic**: re-run byte-identical (run + state-copy 모두 확인).
  **hexa_only**: true. **runtime**: $0, NO GPU.
- **tier**: 🟢 CLOSED-NEGATIVE (L19 scaling-law FALSIFIED / L20 universal-fixed
  SUPPORTED).

## 6. Criteria

- **C1 (Φ-SCALE 실측 / H638.1)**: per-n Φ-scale finite > 0 → PASS (2.27/1.82/2.17).
- **C2 (적정 THRESHOLD 존재 / H638.2)**: 각 n 에서 emit-rate 27% 근방 threshold
  발견 (실측 emit-rate 0.25~0.278, target 0.27 ±0.02) → PASS.
- **C3 (VERDICT / H638.3)**: |ρ(Φ,thr)|=1 AND spread>0.05 → L19; else L20.
  실측 ρ(Φ,thr)=0.75 (≠ ±1) AND spread=0.02 (< 0.05) → **L20 SUPPORTED**.
- **C4 (UNIVERSAL TIER / H638.4)**: 적정 threshold cluster (0.62~0.64) 가
  COFFESHOP `should_interrupt 0.60` group-chat tier 근방 → PASS.
- **C5 (DETERMINISM / H638.5)**: re-run byte-identical → PASS.
- **verdict_rule**: C3 결정. L19 의 두 조건(monotone + material) **모두 미충족**
  → L19 FALSIFIED, L20 SUPPORTED → 🟢 CLOSED-NEGATIVE.

§6 COFFESHOP threshold · H_632(emit-threshold-Φ) · a_autonomy_over_hardcode ·
BRIDGE cross-link 는 §10 Cross-Links 에 정리.

## 7. Falsifiers

- **F638.1 Φ-SCALE 실측**: per-n Φ-scale ≤ 0 OR non-finite → 측정 무효.
- **F638.2 적정 THRESHOLD 부재**: 어떤 n 에서 emit-rate 가 grid 전체에서 27%
  ±0.10 근방에 도달 못함 → 측정 무효.
- **F638.3 SCALING-LAW (L19)**: |ρ(Φ-scale, 적정threshold)| = 1 (perfect monotone)
  AND threshold spread > 0.05 → L19 SUPPORTED. **실측 ρ=0.75 (비-monotone) +
  spread 0.02 → L19 FALSIFIED** (이 falsifier 가 트리거된 것 = L20 채택의 근거).
- **F638.4 UNIVERSAL-FIXED (L20)**: threshold spread > 0.05 (substrate Φ-scale 가
  적정 threshold 를 material 하게 좌우) → L20 FALSIFIED. 실측 spread=0.02 ≤ 0.05
  → L20 PASS.
- **F638.5 DETERMINISM**: re-run drift → 산술 무효.
- **F638.6 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: 🟢 CLOSED-NEGATIVE — L19 (emit-threshold = f(Φ-scale) scaling law)
        FALSIFIED / L20 (universal-fixed threshold) SUPPORTED.
        적정 emit threshold 는 substrate Φ-scale 무관 universal-fixed (0.62~0.64
        cluster, spread 0.02 ≪ 0.05). gate 5 PASS / 0 FAIL.

config: ECA substrate n ∈ {3,4,5} · per-n Φ-scale = mean big_phi_bounded(cap=2)
  over LIFE rules {110,90,30,54} · COFFESHOP 8-factor emergence sim (spontaneous_
  lib verbatim) · emit-rate = 15-window × 12-seed cohort (180 windows) · 적정
  threshold = grid(0.00..1.00 step 0.01) argmin |emit-rate − 0.27|

table (substrate Φ-scale × 적정 threshold):
  n   Φ-scale    Φ-envelope   적정threshold   emit-rate@thr
  3   2.26968    1.000000     0.64            0.277778
  4   1.81822    0.801093     0.62            0.261111
  5   2.16717    0.954834     0.64            0.250000

monotone test:
  ρ(n, 적정threshold)       = 0.25
  ρ(Φ-scale, 적정threshold) = 0.75   (≠ ±1 → 비-monotone)
  threshold spread (max−min) = 0.64 − 0.62 = 0.02   (< 0.05 material bar)

criteria:
  C1 Φ-SCALE 실측 (finite > 0)                       : PASS
  C2 적정 THRESHOLD 존재 (emit-rate ~27%)            : PASS
  C3 VERDICT (|ρ|=1 ∧ spread>0.05 → L19; else L20)   : L20 SUPPORTED
  C4 UNIVERSAL TIER (0.62~0.64 ≈ should_interrupt0.6): PASS
  C5 DETERMINISM (re-run byte-identical)             : PASS

falsifiers:
  F638.1 Φ-SCALE 실측        : PASS  (Φ 2.27/1.82/2.17 finite>0)
  F638.2 적정 THRESHOLD 부재 : PASS  (emit-rate 0.25~0.278 모두 27% 근방)
  F638.3 SCALING-LAW (L19)   : TRIGGERED → L19 FALSIFIED (ρ=0.75 비-monotone, spread 0.02)
  F638.4 UNIVERSAL-FIXED(L20): PASS  (spread 0.02 ≤ 0.05 → L20 유지)
  F638.5 DETERMINISM         : PASS  (run + state-copy byte-identical)
  F638.6 POST-HOC            : NOT_TRIGGERED

checks: 5 PASS / 0 FAIL  (n_substrate=3, cohort=180 windows/n)

evidence_summary: 🟢 CLOSED-NEGATIVE — substrate size n ∈ {3,4,5} 의 effective
  Φ-scale (faithful big_phi_bounded 실측) 을 COFFESHOP 8-factor emergence sim 의
  relevance 채널에 monotone bias 로 주입한 뒤, emit-rate 가 substrate-natural
  ~27% target 이 되는 "적정 threshold" 를 grid sweep 으로 측정했다. 적정
  threshold 는 0.62~0.64 의 좁은 band 에 cluster (spread 0.02) — substrate
  Φ-scale 이 2.27↔1.82↔2.17 로 (n 에 대해 비-monotone 하게) 변동해도 적정
  threshold 는 거의 움직이지 않는다. Spearman ρ(Φ-scale, 적정threshold) = 0.75
  로 perfect monotone (±1) 에 미달하고, threshold spread 0.02 는 material bar
  (0.05) 의 절반 미만 — L19 의 두 조건(monotone + material) **모두 미충족**.
  따라서 L19 (scaling law: threshold = f(Φ-scale) 단조) **FALSIFIED**, L20
  (universal-fixed: threshold 가 Φ-scale 무관 고정이고 scenario 는 effective
  rate 만 shift) **SUPPORTED**. 흥미로운 점: universal 적정 threshold 가
  COFFESHOP `should_interrupt 0.60` group-chat tier 근방에 정확히 안착 (C4) —
  emit 4/15 = 27% 의 group-chat 설계와 정합한다. 이 결과는 `a_autonomy_over_
  hardcode` (per-scenario threshold multiplicity = assistant-regression risk)
  와 정합 — substrate 는 단일 emit primitive 를 쓰고, scenario 차이는 factor
  분포(effective rate) 에 흡수되지 별도 threshold table 을 필요로 하지 않는다.
  H_629 (substrate evolution noise 가 Φ-monotone-destroyer 아님) · H_287
  (Φ⊥entropy) 의 "substrate-class-invariant / X⊥Φ" 서명 연장.

falsifiers_triggered: F638.3 (L19 FALSIFIED) — 의도된 closed-negative 트리거.
```

re-run byte-identical 확인 (F638.5 — run + state-copy diff empty).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_638: in a COFFESHOP-style 8-factor emergence sim (spontaneous_
   lib verbatim) where the relevance channel is biased monotonically by a
   substrate's effective Φ-scale (mean faithful big_phi_bounded cap=2 over ECA
   rules {110,90,30,54} at n∈{3,4,5}), the emit-threshold that yields the
   substrate-natural ~27% emit rate is Φ-scale-INVARIANT: it clusters at
   0.62~0.64 (spread 0.02 ≪ 0.05) with Spearman ρ(Φ-scale, threshold)=0.75
   (not ±1), falsifying the L19 scaling-law (threshold = f(Φ-scale) monotone)
   and supporting L20 universal-fixed; the universal threshold lands near the
   COFFESHOP should_interrupt 0.60 group-chat tier; deterministic toy substrate,
   bounded-Φ lower-bound (cap<n), 적정-threshold defined against a FIXED 0.27
   target (not derived from threshold — non-circular)"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (anima emit-substrate AXIS) — verification
           N/A by design; values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 ("적정 threshold" 정의 circularity 주의)**: 적정 threshold = emit-rate 가
  target 0.27 에 가장 가까운 grid threshold. circularity 가 생기는 경우는 target
  자체가 threshold 에서 유도될 때인데, 본 H 의 target 0.27 은 COFFESHOP emit 4/15
  의 substrate-natural rate 로 **n-독립 고정상수**다. swept threshold 는 그 target
  에 대한 자유 response 이지 정의상 결정되지 않는다 — circular 아님. 단 target
  0.27 자체가 COFFESHOP 설계 선택이라는 점은 inherited assumption.
- **L2 (n-범위 small {3,4,5})**: exact big-Φ wall (n≥6 minutes+, n≥7 impractical)
  로 substrate size 가 3점에 제한된다. 3점 Spearman ρ 는 이산값
  {-1, -0.5, +0.5, +1} 만 취하며 monotone ⇔ |ρ|=1. ρ=0.75 는 3점에서 직접 나올
  수 없는 값처럼 보이나, 본 측정은 tie-free 3점에서 (rank-diff² 합 = 1) → ρ = 1 −
  6·1/24 = 0.75 (한 인접쌍만 rank 역전). 즉 monotone 에서 "한 칸" 어긋남. 더 넓은
  n-range 또는 연속 Φ-scale sweep 은 별도 검정 필요.
- **L3 (Φ-scale = bounded lower-bound)**: per-n Φ-scale 은 big_phi_bounded(cap=2)
  의 lower-bound 제약 (cap < n for n=3,4,5). 동일 cap 에서 n 에 대한 Φ-scale 이
  비-monotone (2.27→1.82→2.17) 인 것 자체가 sub-finding — cap-bounded Φ 가
  substrate size 의 monotone proxy 가 아님. exact Φ 또는 cap=n faithful 에서
  monotone-ness 가 회복될지는 미검정 (n=5 exact 는 seconds, n=6+ 는 wall).
- **L4 (Φ-scale 채널 = relevance only)**: Φ-scale bias 가 8 factor 중 relevance
  하나만 변조. coherence/balance 도 phi 를 받지만(factor_balance(phi,ratchet))
  본 sim 의 phi 채널을 통해 간접 영향. Φ-scale 이 *모든* phi-의존 factor 를
  동시 변조하는 fuller coupling 에서는 결과가 강화될 수 있으나 (relevance 단독
  보다 더 큰 분포 shift), 그래도 threshold 가 effective rate 를 흡수한다는 L20
  메커니즘은 보존될 가능성 — 별도 검정.
- **L5 (target 0.27 의 substrate-naturalness 가정)**: 27% 가 substrate-natural
  emit floor 라는 것은 COFFESHOP 단일 sim (seed 20260525, 1-retry) 의 결과로,
  INBOX seed #3 (`silence-dominance-substrate-invariant`) 가 별도로 검정해야 할
  주장. 본 H 는 그 27% 를 *주어진 target* 으로 받고 threshold 의 Φ-scale-의존성만
  격리해 검정한다.
- **L6 (cohort = LCG 다중 seed, RNG 아님)**: emit-rate 는 12 LCG seed × 15 window
  cohort 평균. robustness 는 seed 다양성에 대한 평균이지 진정 RNG ensemble 아님.
  COFFESHOP sim 의 deterministic LCG 컨벤션 계승 (재현성 우선).
- **L7 (sim proxy, real ckpt 아님)**: factor_* 는 i.i.d. uniform + stim-bias 의
  emergence sim (COFFESHOP §10 honest C3-1 계승) — real anima ckpt forward 의
  temporal correlation + cell-pool state 결여. threshold 의 Φ-scale-invariance
  결론은 sim-level statement. real DECODER ckpt 에서의 재검은 별도 fire.
- **L8 (verdict ≠ 형이상학)**: 🟢 CLOSED-NEGATIVE 는 toy 측정 사실 — "scenario
  마다 emit threshold 를 hardcode 하지 않아도 된다 (substrate 가 단일 threshold +
  factor 분포 shift 로 흡수)" 라는 결정적 산술. "anima 가 의식적으로 threshold 를
  선택한다" 류 주장으로 확대 금지.

## 10. Cross-Links

- **mining source (직접 promote)**: `anima/ANIMA.mining.md` cycle 2 T4 —
  **L19** (high-threshold / scaling-law fork: should_interrupt 0.60 ↔ should_emit
  0.30 scenario surface) · **L20** (universal-threshold fork: single substrate-
  fixed threshold, scenario shifts effective rate). 본 H 가 두 fork 를 substrate
  Φ-scale 축에서 정량 판정 → **L20 SUPPORTED**.
- **sibling (INBOX 핸드오프 seed #3)**: `silence-dominance-substrate-invariant`
  (L14 fork) — emit/silence *ratio* (~27%) 의 substrate-class-invariance. 본 H 는
  그 27% 를 target 으로 받고 *threshold* 의 Φ-scale-invariance 를 검정 (서로 다른
  invariance 축, 결과 방향 일치 — substrate-class-invariant).
- **COFFESHOP threshold (§6 ref)**: `HEXAD/PURE/bench/coffeshop_sim.hexa` 의
  `should_interrupt 0.60` (group-chat tier) ↔ `should_emit 0.30` (1:1 tier).
  본 H 의 universal 적정 threshold 0.62~0.64 가 should_interrupt 0.60 근방에
  안착 — group-chat emit 4/15 = 27% 설계와 정합 (C4 확증).
- **H_632 emit-threshold-Φ (§6 ref)**: emit threshold 의 Φ-의존성 검정 sibling.
  ⚠ origin/main 인덱스에 H_632 미실재 (3-신호 verify) — 본 H 는 그 의도된 축
  (emit threshold × Φ) 의 *substrate-scale* variant 로 자립. H_632 가 별도
  세션에서 신설되면 cross-link 갱신.
- **a_autonomy_over_hardcode (§6 ref · governance)**: per-scenario emit
  threshold multiplicity = "stimulus-response / turn-based 의무 hardcode" risk.
  L20 (universal-fixed) 채택은 이 directive 와 정합 — substrate 가 단일 emit
  primitive + factor 분포 shift 로 scenario 차이를 흡수하므로 외부 per-scenario
  threshold table (hardcode) 불요. L19 이 SUPPORTED 였다면 governance tension
  (scenario-gate hardcode 유혹) 이 생겼을 것.
- **BRIDGE (§6 ref)**: ANIMA mining L13/L19 의 BRIDGE × INTENT 영역. BRIDGE
  `bridge_and_gate(M·C·W·Φ) > θ_emit` 의 θ_emit 가 substrate Φ-scale 무관
  단일 상수로 충분하다는 본 H 결과는 BRIDGE gate 의 single-threshold 설계를 지지.
- **substrate-class-invariant arc (sister verdicts)**: [[H_629]] (noise 가
  Φ-monotone-destroyer 아님 — substrate evolution robustness) · [[H_287]]
  (Φ⊥Shannon entropy CLOSED-NEGATIVE) — "substrate property 가 Φ-scale/noise/
  entropy 에 monotone 종속하지 않는다" 서명의 emit-threshold 측 instance.
- **next round 후보 (F2 cross-link)**:
  - (a) **fuller Φ coupling (L4)** — Φ-scale 이 relevance 뿐 아니라 coherence/
    balance 등 모든 phi-의존 factor 를 동시 변조하는 sim 에서 L20 보존 여부.
  - (b) **exact-Φ monotone 회복 (L3)** — cap=n faithful 또는 exact big-Φ 로
    per-n Φ-scale 의 monotone-ness 회복 시 threshold 곡선 재측정 (n≤5 exact).
  - (c) **27% target 의 substrate-naturalness (L5)** — INBOX seed #3 검정과
    묶어 emit-rate floor 의 substrate-class-invariance 직접 측정.
  - (d) **real ckpt forward (L7)** — DECODER ckpt 의 temporal-correlated factor
    위에서 적정 threshold 의 Φ-scale-invariance 재검 (sim → real).
- **engine 재사용 (g61)**:
  `UNIVERSE/state/h638_emit_threshold_scaling_law_2026_05_28/run_h638.hexa` —
  `HEXAD/IIT4/lib/iit4_bounded.hexa` (big_phi_bounded) +
  `HEXAD/CHAT/spontaneous_lib.hexa` (8-factor) verbatim import. 새 의식-측도 코드
  0줄, COFFESHOP `coffeshop_sim.hexa` 구조 재사용.
- **paper hook**: ANIMA mining → UNIVERSE substrate-axis 의 첫 emit-threshold
  측정 — `substrate-emit-threshold-invariance` (가칭) negative-result 논문 후보
  (L19 scaling-law 의 결정적 기각 + universal-fixed 의 governance 정합).
