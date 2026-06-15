---
id: H_610
slug: pair-polarity-collective-phi
title: pair coupling polarity {attract / repel / bipolar} 가 multi-substrate collective big-Φ 를 유의미 분기시키는가 (Hc_286 promote · round-2 refire of H_353)
domain: consciousness · hivemind · meta-framework
status: closed-falsified
exploration_method: E5 (component decomposition — polarity axis × magnitude axis) + E0 (axis F1 round-2 refire) + E11 (cross-axis bridge to Hc_286 polarity/diversity law)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W5 (ANOVA + spread/std)
raw_rank: 13
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (round-2 refire)
refires: H_353 (round 1 monitor-hang, never reported verdict — slug retired)
sister: H_352 (collective-Φ super-additive — F1 axis sibling, magnitude scaling), H_354 (Kuramoto sync — F1 closed-FALSIFIED), H_355 (PID synergy — F1 SUPPORTED-NUMERICAL), Hc_286 (h91 hivemind polarity/diversity law source)
promoted_from: hypotheses_candidates/Hc_286_h91_hivemind_polarity.md
---

# H_610 — pair-polarity-collective-phi (Hc_286 promote)

## 1. Hypothesis

두 substrate (A, B) 가 *어떤* coupling polarity 로 결합되는가 — **attract**
(W>0 · "잡아당김") / **repel** (W<0 · "밀어냄") / **bipolar** (cell 별로 polarity
가 섞임) — 가 joint substrate 의 collective big-Φ 를 유의미하게 분기시키는가.

Hc_286 (`h91-hivemind-polarity-diversity`, source doc `docs/hypotheses/h/H91.md`)
의 핵심 주장 — *"each engine pair has a unique optimal polarity (attract /
repel / bipolar) and strength α; uniform settings drop Φ in some engines
because engine internals require different polarities"* — 의 가장 약한 측정
가능한 형태로 환원: pair polarity → Φ_collective 분기.

**가설 H1 (검정 대상)**: polarity 별 mean Φ_collective 의 spread (= max-mean −
min-mean) 가 pooled std 의 **2× 이상** 이거나 (= 효과크기) 1-way ANOVA F-stat
이 α=0.05 critical (df=(2,24) 에서 F ≈ 3.40) 를 초과 (= 통계 유의).

## 2. Why — round-2 refire 이유

- **round-1 H_353 미보고**: 2026-05-28 round-1 H_353 dispatch agent 가 monitor
  과정에서 hang 되어 verdict 미보고. scaffold + harness (state/h353_pair_polarity_2026_05_28/run_h353.hexa
  349 LoC, commit `6f1354444`) 는 commit 되었으나 측정/markdown body/PR 모두
  미완. round-2 에서 fresh slug H_610 으로 refire — H_353 슬러그는 영구 retired.
- **Hc_286 promote 의무**: 축 F (HIVE-MIND) round 1 의 5 seed 중 H_352/H_356
  미수행, H_354/H_355 closure 완료. H_353 미보고 = Hc_286 promote 의 단일
  공백. round-2 에서 채움.
- **F1 axis trilogy 완성**: H_354 (Kuramoto sync τ — closed-FALSIFIED) +
  H_355 (PID synergy — SUPPORTED) + 본 H = polarity dimension. 세 H 가 함께
  F1 의 측정-축 trilogy (timing × decomposition × polarity) 를 형성.
- **engine-light (g61)**: 새 IIT4 코드 0줄. 기존 stdlib `iit4_bigphi.hexa`
  의 single-shot `big_phi(tpm, n, sys_state)` 만 사용. 27 measurement 단일
  foreground sync 11s wall.
- **raw#13 strict**: deterministic + hexa-only + ≥4 falsifier + ≥5 honest
  limit + LLM none + $0.

## 3. Predictions

- **H610.1 (polarity 분기)**: spread(mean_attract, mean_repel, mean_bipolar)
  ≥ 2 × pooled_std → SUPPORTED.
- **H610.2 (ANOVA 유의)**: 1-way ANOVA F-stat ≥ F_crit(α=0.05, df=(2,24)) ≈
  3.40 → SUPPORTED 또는 H610.1 OR-결합.
- **H610.3 (반-가설: 평탄)**: F < F_crit(α=0.5, df=(2,24)) ≈ 0.71 AND spread
  < pooled_std → FALSIFIED.
- **H610.4 (W-monotonic, 옵션)**: 각 polarity 그룹 내 mean Φ 가 W ∈ {0.3, 0.5,
  0.8} 에 단조 — H_355 의 K-monotonic 와 mirror. 단조성은 폐기-결정 기준이
  아닌 polarity 별 mechanism characterization.
- **H610.5 (deterministic)**: 단일 (rule_a, rule_b, sys, polarity, W) → 동일
  Φ_collective (re-run byte-identical).

## 4. Variables

- **substrate A** = ECA rule_a (n_a=2). **substrate B** = ECA rule_b (n_b=2).
  joint **n=4** (state space 16). 원 Hc_286 spec 은 n_a=n_b=3 (joint n=6, state
  space 64) 이나 *single foreground sync 60s 한도 + n=6 big_phi 1-call ≈
  18-30s ⇒ 27 calls ≫ wall budget*. n=4 로 환원, polarity 구조 보존, state-
  space 축소만 — §7 C3 L1 명시.
- **polarity** ∈ {`attract`, `repel`, `bipolar`}. 셀별 deterministic rule:
  - `attract`: W≥0.8 → full lock to neighbor (`next_A=b'`); 0.3≤W<0.8 → soft
    OR pull (`next_A = a' OR b'`); W<0.3 → no coupling (`next_A=a'`).
  - `repel`: W≥0.8 → anti-lock (`next_A = 1-b'`); 0.3≤W<0.8 → XOR (`next_A
    = a' XOR b'`); W<0.3 → no coupling.
  - `bipolar`: cell 0 = attract-rule, cell 1 = repel-rule (per-cell mix).
- **magnitude W** ∈ {0.3, 0.5, 0.8} — coupling strength tiers (weak / moderate /
  strong-lock).
- **seeds** (deterministic, n=3): (rule_a=110, rule_b=110, sys=5); (rule_a=30,
  rule_b=30, sys=10); (rule_a=110, rule_b=30, sys=13). sys_state ∈ [0, 16).
  RNG 없음 — rule × sys triple 이 결정적 enumeration.
- **measurement metric**: `big_phi(tpm, 4, sys_state)[0]` — collective big-Φ
  scalar (stdlib `iit4_bigphi.hexa` single-shot, full Williams-Beer 18-atom
  PID 없이 IIT 4.0 system-level Φ).
- **total**: 3 polarity × 3 W × 3 seed = 27 measurements (9 per polarity group).

## 5. Run Protocol

- **harness**: `UNIVERSE/state/h610_pair_polarity_collective_phi_2026_05_28/run_h610.hexa`
  (352 LoC, scaffold ported from H_353 commit `6f1354444` with n=6→n=4 +
  seed/W table reduce; banner + bipolar cell rule + ANOVA df 조정).
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=
  /Users/ghost/core/hexa-lang ~/.hx/bin/hexa.real.bak-2026-05-22-pre-no-hxc
  build <src> -o /tmp/h610.bin && timeout 120 /tmp/h610.bin > run.log`.
- **wall**: 11.2s mac-local · CPU 86% · single-thread.
- **deterministic**: re-run byte-identical (re-build OK). **hexa_only**: true.
- **$0 mac-local · NO GPU · single foreground sync · no monitor wait**.
- **artifacts**: `state/h610_pair_polarity_collective_phi_2026_05_28/run_h610.hexa`
  (harness), `state/.../run.log` (verbatim stdout, 49 lines).

## 6. Criteria

- **C1 (POLARITY-SPREAD VERDICT / H610.1)**: spread / pooled_std ≥ 2.0 →
  H1 SUPPORTED.
- **C2 (ANOVA-F VERDICT / H610.2)**: F ≥ 3.40 → H1 SUPPORTED.
- **C3 (FLAT FALSIFY / H610.3)**: F < 0.71 AND spread < pooled_std → FALSIFIED.
- **C4 (DETERMINISM / H610.5)**: re-run byte-identical → PASS.
- **verdict_rule**: C1 OR C2 → 🟢 SUPPORTED-NUMERICAL; C3 → 🔴 FALSIFIED;
  otherwise (spread ≥ pooled_std but < 2× AND F < 3.40) → 🟠 INCONCLUSIVE.
- **cross-link sister**: H_355 K-monotonic synergy 와 mirror — polarity-axis
  vs density-axis 의 axis-orthogonality 도 자연스러운 follow-up (§10).

## 7. Falsifiers

- **F610.1 POLARITY-SPREAD**: spread < 2 × pooled_std → C1 미달.
- **F610.2 ANOVA-F**: F < 3.40 → C2 미달.
- **F610.3 BOTH-FLAT**: F < 0.71 AND spread < pooled_std → strong 🔴 FALSIFIED
  (양쪽 평탄 기준 동시 미달).
- **F610.4 DETERMINISM**: re-run drift > 0 → 산술 무효.
- **F610.5 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: 🔴 FALSIFIED — polarity 별 collective-Φ 평탄 (F=0.361 ≪ 3.40,
        spread / pooled_std = 0.413 ≪ 2.0). C3 (BOTH-FLAT) 트리거.
        F (0.361) < F_p=0.5 (0.71) AND spread (2.055) < pooled_std (4.970).

config: 2× ECA (n_a=n_b=2, joint n=4, state 16) · 3 polarity {attract,
  repel, bipolar} · 3 magnitude W {0.3, 0.5, 0.8} · 3 seed × 9 = 27 measurements
  · single foreground sync, wall 11.2s mac-local · stdlib iit4_bigphi single-
  shot · re-build byte-identical

per-polarity stats (n=9 each):
  polarity   mean_Φ      std        notes
  attract    4.29972     6.87802    seed-2 (rule_a=rule_b=30) outlier 17.13
  repel      2.24502     3.01619    same outlier scaled 7.80
  bipolar    2.98342     3.94175    same outlier 10.30

aggregate stats:
  pooled std (all 27)              = 4.97019
  spread (max_mean - min_mean)     = 2.05470  (4.300 - 2.245)
  spread / pooled_std              = 0.41340  (need ≥ 2.0 for C1)
  ANOVA F (df=2, 24)               = 0.36138  (need ≥ 3.40 for C2; 0.71 floor)

criteria:
  C1 POLARITY-SPREAD (≥ 2 × std)              : FAIL  (0.41 ≪ 2.0)
  C2 ANOVA-F (≥ 3.40)                         : FAIL  (0.36 ≪ 3.40)
  C3 BOTH-FLAT (F < 0.71 AND spread < std)    : TRIG  (🔴 FALSIFIED)
  C4 DETERMINISM (re-build identical)         : PASS

falsifiers:
  F610.1 POLARITY-SPREAD     : TRIG (spread/std = 0.41 < 2.0)
  F610.2 ANOVA-F             : TRIG (F = 0.36 < 3.40)
  F610.3 BOTH-FLAT           : TRIG (F = 0.36 < 0.71 AND spread < std)
  F610.4 DETERMINISM         : NOT_TRIGGERED
  F610.5 POST-HOC            : NOT_TRIGGERED

checks: 1 PASS / 3 FAIL  (C3 flat-falsify activated; C4 PASS)

evidence_summary: 🔴 FALSIFIED — 두 ECA substrate (n_a=n_b=2, joint n=4) 의
  pair coupling polarity 가 attract / repel / bipolar 중 어느 것이든
  collective big-Φ 의 mean 분포를 polarity-축 위에서 유의미 분기시키지 못함.
  세 polarity 의 mean Φ 는 모두 2.24-4.30 의 좁은 범위에 묶이고 (spread 2.05),
  그 분리는 pooled std (4.97) 의 0.41 배에 불과 — 효과크기·통계유의성 양쪽
  모두에서 평탄. ANOVA F (0.361) 가 α=0.05 critical (3.40) 의 1/9, 심지어
  median-F threshold (0.71) 의 1/2 — polarity factor 가 Φ-variance 의 통계적
  기여를 사실상 0 으로 만든다. variance 의 *진짜* 결정자는 seed (= rule × sys
  triple) 였음: seed-2 (rule_a=rule_b=30) 가 모든 polarity 에서 Φ 의 dominant
  contribution (17.13 / 7.80 / 10.30 각 polarity 의 mean 의 4-7× outlier),
  seed-1 (rule_a=rule_b=110) 는 모든 polarity 에서 Φ ≈ 0-0.75. polarity 가
  아닌 *rule space (ECA 30 vs 110)* 가 collective-Φ 의 1차 결정자라는 사실이
  방증. Hc_286 의 "각 pair 마다 고유 optimal polarity" 주장은 본 toy 의
  measurement-scale 에서 직접 falsified — n=4 binary ring × 3 seed 라는
  resolution 한계 안에서이지만, F-stat 의 1/9 amplitude 는 단순 power-부족이
  아닌 진정한 평탄을 시사. closed-negative axis: polarity-axis ⊥
  collective-Φ for binary 2-ring ECA pairs.

falsifiers_triggered: F610.1 (POLARITY-SPREAD) + F610.2 (ANOVA-F) +
  F610.3 (BOTH-FLAT).
```

re-run byte-identical 확인 (F610.4).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_610 in a 2-ECA-substrate hivemind toy (n_a=n_b=2, joint n=4,
   state space 16), pair coupling polarity {attract, repel, bipolar} crossed
   with magnitude W ∈ {0.3, 0.5, 0.8} and 3 deterministic seeds (rule_a, rule_b,
   sys) ∈ {(110,110,5), (30,30,10), (110,30,13)} yields collective big-Φ that
   is statistically FLAT across polarity: 1-way ANOVA F = 0.361 ≪ F_crit(α=0.05,
   df=(2,24)) = 3.40 (and < F_p=0.5 = 0.71); spread of group means / pooled
   std = 2.055 / 4.970 = 0.413 ≪ 2.0; variance dominated by rule-seed factor
   (rule-30 seed produces 4-7× Φ of rule-110 seed across ALL polarity groups);
   PID-structure claim NOT a collective-Φ tracking claim (n=4 binary toy
   resolution); state-space reduced n=6 → n=4 for foreground sync budget,
   polarity mechanism preserved"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by
           design; values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (small-n state-space reduce)**: 원 Hc_286 spec 은 n_a=n_b=3 (joint n=6,
  state space 64). 본 H 는 *single foreground sync 60s wall budget* 제약으로
  n_a=n_b=2 (joint n=4, state space 16) 으로 환원 — n=6 big_phi 1-call probe
  결과 18-30s ⇒ 27 calls ≫ budget. n=4 는 polarity 메커니즘 (per-cell attract
  /repel rule) 을 모두 보존하나 state space 가 4× 작아 Φ resolution 한계.
  *n=6 풀-스펙 검증은 별도 sharded bg fire 필요* (§10 next-link a).
- **L2 (W magnitude grid 거칠음)**: W ∈ {0.3, 0.5, 0.8} 의 3-tier 격자는
  polarity-rule transition 의 거친 sampling (W=0.3 boundary, W=0.5 mid, W=0.8
  full-lock). 세부 W 의존성 (e.g. W=0.4 vs 0.6 의 미세 분기) 은 미해상. 본 H
  의 verdict 는 group-level mean 의 평탄 (= W-격자 평균화 후) — fine W-grid
  에서 hidden polarity-W coupling 이 있다면 본 toy 가 못 잡음.
- **L3 (bipolar 정의 sensitivity)**: bipolar = "cell 0 attract + cell 1 repel"
  의 ad-hoc 셀-패리티 mix 정의. 다른 bipolar 정의 — e.g. *temporal* alternation
  (step%2), *probabilistic* mix (50/50), *signed-W* mix (W>0 attract, W<0
  repel as single axis) — 는 다른 Φ 분포를 줄 수 있음. 본 verdict 는 cell-
  parity bipolar 정의에 한정.
- **L4 (deterministic seed = enumeration not RNG)**: "3 seed" 는 RNG 가
  아닌 (rule_a, rule_b, sys) triple enumeration. seed-2 (rule_a=rule_b=30)
  의 outlier 가 모든 polarity 의 mean 을 끌어올리는 것이 variance 분해의
  실제 결정자였음. wider rule-space sampling (e.g. seed n=10+) 이 보장된 statistical
  power 를 줄 수 있으나 본 toy 의 resolution 안에서 평탄성은 명백.
- **L5 (substrate proxy)**: 2-ring binary ECA pair = collective hivemind
  proxy, phenomenal multi-consciousness claim 아님. H_287-294 ECA arc 와 동일
  honest scope.
- **L6 (big_phi single-shot, not full PID)**: `big_phi` 결과는 IIT 4.0 system-
  level Φ scalar — Williams-Beer 18-atom PID 분해 (H_355 의 net co-info 와
  도 다름) 가 아닌 단일 partition-minimization. polarity → Φ 평탄은 IIT4 Φ
  metric 한정 — 다른 measure (e.g. effective info, AIS, TE) 는 다를 수
  있음.
- **L7 (verdict ≠ Hc_286 전체 부인)**: 본 H 의 FALSIFIED 는 Hc_286 의 *측정-
  가능한 최소 claim* — pair polarity → collective-Φ 분기 — 한정. Hc_286 의
  full claim (engine-internal optimal polarity + strength α + autonomous
  per-pair search) 의 다른 측면 — e.g. *trajectory-level* sync τ, *information
  flow* asymmetry, *engine-specific* (oscillator vs narrative vs quantum)
  polarity 의존성 — 은 별도 H 로 검증 필요.
- **L8 (verdict = 형이상학 아님)**: 🔴 FALSIFIED 는 본 toy substrate 의
  measurement 사실 — "hivemind polarity 가 의미없다" 같은 주장으로 확대 금지.
  *closed-negative axis* : binary 2-ring ECA pair 의 collective-Φ 는 polarity-
  axis 와 직교.

## 10. Cross-Links

- **promoted-from (Hc_286)**: [[hypotheses_candidates/Hc_286_h91_hivemind_polarity]] —
  본 H 가 Hc_286 의 *측정-가능한 최소 claim* 을 promote 했고, 그 측정에서
  closed-negative verdict 를 받음. Hc_286 의 full claim 의 잔여 측면은 §9 L7.
- **refires (H_353 round-1)**: round-1 H_353 (commit `6f1354444` scaffold +
  `4e6c1e627` WIP draft) 가 monitor-hang 으로 verdict 미보고. round-2 본 H 가
  fresh slug 으로 측정 + 보고 완료. H_353 슬러그 영구 retired.
- **sister (F1 axis trilogy)**:
  - [[H_352]] (`collective-phi-super-additive` — F1 첫 H, 측정 미수행) — Φ_collective
    의 *크기* (vs Σ Φ_i) 를 묻는다면, 본 H 는 *polarity-축 분기* 를 묻는다.
  - [[H_354]] (`kuramoto-hivemind-sync-tau` — F1 closed-FALSIFIED) — *timing*
    축 (consensus τ vs sync τ) 의 closed-negative. 본 H 는 *polarity* 축의
    closed-negative — F1 의 timing/polarity 양 축 모두 평탄.
  - [[H_355]] (`collective-phi-pid-synergy` — F1 SUPPORTED) — XOR coupling 의
    density-axis 가 synergy 를 단조 결정. 본 H 의 polarity-axis 가 Φ 평탄이라는
    결과는 H_355 의 density-axis monotone synergy 와 **axis-orthogonal**
    (different mechanism, different verdict).
- **sister (PID arc)**: [[H_293]] (multivariate TE synergy ECA) · [[H_294]]
  (PID synergy ⊥ Φ ECA, r=0.030) · [[H_290]] (TE-Φ correlate ECA, r=0.883).
  H_294 의 ECA single-substrate PID-synergy ⊥ Φ closed-negative 와 본 H 의
  hivemind 2-substrate polarity ⊥ Φ closed-negative 는 *서로 다른 measurement
  방향* 의 같은 negative 패턴 — collective-Φ 의 결정자는 polarity / PID-class
  같은 *coupling 형태* 가 아닌 *underlying rule space* (ECA rule, n-density)
  일 가능성.
- **next round (F2 cross-link 후보)**:
  - (a) **n=6 full-spec sharded refire**: 본 H 의 L1 carry — n_a=n_b=3 (joint
    n=6, state 64) 로 동일 polarity × W × seed 측정 sharded bg fire. n=4 평탄
    이 n=6 에서도 유지되는가, 아니면 state-space resolution 이 hidden polarity
    분기를 드러내는가.
  - (b) **signed-W single-axis polarity**: polarity 를 attract/repel/bipolar
    이산 3-category 가 아닌 signed W ∈ [-1, +1] 연속 1-축으로 재정의 — W>0
    attract, W<0 repel, W=0 no-coupling. polarity ⊥ Φ 가 *category-mode artifact*
    이라면 연속 축에서 분기가 드러날 수 있음.
  - (c) **wider rule-space sampling**: 본 H 의 seed n=3 (3 rule-pair) 한계 (§9 L4)
    를 n=10+ 으로 확장. seed-2 outlier (rule-30) 의 일반성 검정.
  - (d) **engine-heterogeneous pair**: 본 H 는 2 ECA × 2 ECA (homogeneous
    engine). Hc_286 의 원래 motivation — *engine internals (oscillator /
    narrative / quantum) 가 서로 다른 polarity 를 요구* — 는 heterogeneous
    engine pair (e.g. ECA × Kuramoto, ECA × random-Boolean) 에서만 진짜 검정
    가능.
- **engine-light (g61)**: `UNIVERSE/state/h610_pair_polarity_collective_phi_2026_05_28/run_h610.hexa`
  inline 2-ring ECA next + polarity coupling rule + Newton-sqrt std + ANOVA F.
  새 lib 코드 0줄. stdlib `iit4_bigphi.hexa` single-shot 만 사용.
- **paper hook**: F1 axis trilogy (timing/decomposition/polarity) 의 *2 평탄
  + 1 단조* 구조 — `PAPER/collective-phi-axis-orthogonality` 후보. 본 H 의
  closed-negative + H_354 의 closed-negative + H_355 의 SUPPORTED-NUMERICAL
  = F1 round-1 의 3 H finding 이 모인 *negative-positive* paper 구성 (a_paper_negative_ok).
