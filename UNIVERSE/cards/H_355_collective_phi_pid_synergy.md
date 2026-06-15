---
id: H_355
slug: collective-phi-pid-synergy
title: 다중 substrate collective-Φ 의 PID 분해는 synergy 우세 — 8 permutation × 4 K-bucket 모두 synergy_ratio = 1.0, K-monotonic (H_293/H_294 hivemind sister)
domain: information · consciousness · collective · hivemind · substrate · meta
status: supported-numerical
exploration_method: E5 (component decomposition) + E0 (axis F1 round-1 seed) + E16 (synergy vs redundancy ratio)
verification_method: W1 (numerical smoke) + W4 (verdict-4-class) + W12 (sister-link H_293/H_294 ECA arc)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-28
since: 2026-05-28 (new)
sister: H_293 (multivariate-TE synergy ECA), H_294 (PID synergy ECA — synergy ⊥ Φ closed-negative), H_290 (transfer-entropy-Φ correlate r=0.883), H_352 (collective-Φ super-additive — F1 mirror)
---

# H_355 — 다중 substrate collective-Φ 의 PID 분해는 synergy 우세

## 1. Hypothesis

H_294 는 *단일* ECA substrate 의 흐름을 PID 분해해 흐름의 어떤 성분도 Φ 를
추종하지 않음을 보였다 (synergy ⊥ Φ, r=0.030). 본 H 는 그 sister 를 **hivemind**
축으로 옮긴다 — *다중* substrate (3 binary substrates × 1 cell, 8-state) 의
collective 흐름을 3-source PID 로 분해해 synergy 와 redundancy 비율을 묻는다.
H_294 의 ECA cell-flow PID 는 *substrate 내부* 의 흐름 분해였고, 본 H 는
*substrate 간 cross-flow* 의 분해다.

**가설 H1 (검정 대상)**: collective-Φ 흐름의 PID 에서 synergy 가 redundancy 보다
우세 — `mean synergy_ratio = synergy_total / (synergy_total + redundancy_total) > 0.5`
across coupling K ∈ {0.33, 0.67, 1.0} (비-trivial K).

## 2. Why

- **hivemind 축 F1 seed**: UNIVERSE.md 축 F (HIVE-MIND Collective Φ) round 1 의
  H_293/H_294 sister — ECA single-substrate PID 결과가 hivemind multi-substrate
  PID 에서 보존되는지/뒤집히는지를 묻는 자연스러운 후속.
- **3-source net co-information**: net McGill 3-variate interaction information
  `II_3 = ΣI(T;S_i) - ΣI(T;S_i,S_j) + I(T;S_0,S_1,S_2)`. **부호 규약은 H_294 의
  2-source II_c 와 반대**: 3-source (odd parity) 에서 `II_3 > 0 ⇒ synergy`,
  `II_3 < 0 ⇒ redundancy` (Bell & Sejnowski 2003 / Williams-Beer 2010 §3).
- **engine-light (g61)**: 16-bin (T,S0,S1,S2) joint histogram + bitmask marginal
  entropy inline. 새 IIT4 코드 0줄, big_phi 의존 0줄 (collective-Φ 측정 아닌 PID
  구조 측정만).
- **raw#12 strict**: deterministic + hexa-only + ≥3 falsifier + ≥5 honest limit +
  LLM none + $0.

## 3. Predictions

- **H355.1 (pure-synergy anchor)**: K=1 (mask=[1,1,1], all-XOR cells) →
  synergy>0 AND redundancy=0 (XOR_3 sources 가 joint 로만 T 결정).
- **H355.2 (pure-identity anchor)**: K=0 (mask=[0,0,0], all-identity cells) →
  synergy=0 AND redundancy=0 (각 cell next = 자기 source → 순수 unique-info,
  net co-info=0).
- **H355.3 (synergy-ratio verdict)**: mean synergy_ratio over non-trivial K
  {0.33, 0.67, 1.0} > 0.5 → H1 SUPPORTED; ≤ 0.5 → FALSIFIED. 결과 verbatim.
- **H355.4 (K-monotonic)**: synergy_total 이 K 에 대해 단조증가 (more XOR
  cells ⇒ more synergy), bound 0 ≤ synergy ≤ 3.
- **H355.5 (determinism)**: K=1 synergy_total re-run byte-identical.

## 4. Variables

- **substrate**: 3 binary substrates × 1 cell each (collective state = 3 bits = 8
  states). per-cell next-state 함수는 XOR cell 또는 identity cell.
- **coupling density K** ∈ {0.0, 0.33, 0.67, 1.0} = (XOR cells) / 3. 결정적
  enumeration (permutation seeds): K=0 → 1 mask, K=0.33 → 3 masks, K=0.67 → 3
  masks, K=1 → 1 mask. 총 8 permutations.
- **metric_synergy** per cell = max(0, II_3); **metric_redundancy** per cell =
  max(0, −II_3); hivemind total = Σ across 3 cells.
- **synergy_ratio** = synergy_total / (synergy_total + redundancy_total).

**측정 표** (PID 분해, 8 permutations):

| K | mask | synergy | redundancy | synergy_ratio |
|---|---|---|---|---|
| 0.00 | [0,0,0] | 0.0 | 0.0 | 0.0 (trivial — pure unique-info) |
| 0.33 | [1,0,0] | 1.0 | 0.0 | 1.0 |
| 0.33 | [0,1,0] | 1.0 | 0.0 | 1.0 |
| 0.33 | [0,0,1] | 1.0 | 0.0 | 1.0 |
| 0.67 | [1,1,0] | 2.0 | 0.0 | 1.0 |
| 0.67 | [1,0,1] | 2.0 | 0.0 | 1.0 |
| 0.67 | [0,1,1] | 2.0 | 0.0 | 1.0 |
| 1.00 | [1,1,1] | 3.0 | 0.0 | 1.0 |

**K-bucket 평균**:

| K | mean_synergy | mean_redundancy | mean_ratio |
|---|---|---|---|
| 0.00 (anchor) | 0.0 | 0.0 | 0.0 |
| 0.33 | 1.0 | 0.0 | 1.0 |
| 0.67 | 2.0 | 0.0 | 1.0 |
| 1.00 (anchor) | 3.0 | 0.0 | 1.0 |

**mean synergy_ratio over non-trivial K {0.33, 0.67, 1.0} = 1.0** (1.0 + 1.0 +
1.0) / 3 = 1.0.

## 5. Run Protocol

- **smoke**: `UNIVERSE/state/h355_collective_phi_pid_synergy_2026_05_28/run_h355.hexa`
- **engine-light**: 16-bin (T,S0,S1,S2) joint histogram + bitmask marginal entropy
  (inline, ~280 LoC). big_phi/eca_tpm 의존 없음 — 본 H 는 PID 구조 자체에 대한
  주장이지 collective-Φ 의 절대값에 대한 주장이 아님.
- **build/run (selfhosted, fix-1180 우회)**: `HEXA_MAC_BUILD_OK=1 HEXA_LANG=<root>
  hexa.real.bak-2026-05-22-pre-no-hxc build <src> -o /tmp/h355.bin && bin` —
  [[reference-life-cycle-hexa-run-gotchas]]
- **deterministic**: re-run byte-identical. **hexa_only**: true. **runtime**:
  $0, NO GPU, wall ~0.1s.
- **tier**: 🟢 SUPPORTED-NUMERICAL.

## 6. Criteria

- **C1 (PURE-SYNERGY ANCHOR / H355.1)**: K=1 synergy=3, redundancy=0 → PASS.
- **C2 (PURE-IDENTITY ANCHOR / H355.2)**: K=0 synergy=0, redundancy=0 → PASS.
- **C3 (SYNERGY-RATIO VERDICT / H355.3)**: mean ratio non-trivial K > 0.5 →
  H1 SUPPORTED; else FALSIFIED.
- **C4 (K-MONOTONIC / H355.4)**: synergy(K=0) ≤ synergy(K=0.33) ≤
  synergy(K=0.67) ≤ synergy(K=1) → PASS.
- **C5 (BOUND + DET / H355.5)**: 0 ≤ synergy ≤ 3, redundancy ≥ 0 ; K=1 re-run
  identical → PASS.
- **verdict_rule**: C3 결정. mean ratio = 1.0 ≫ 0.5 → 🟢 SUPPORTED-NUMERICAL.

## 7. Falsifiers

- **F355.1 PURE-SYNERGY ANCHOR**: K=1 synergy ≤ 0 OR redundancy > 0 → witness 무효.
- **F355.2 PURE-IDENTITY ANCHOR**: K=0 synergy > 0 OR redundancy > 0 → 측정 무효.
- **F355.3 SYNERGY-RATIO VERDICT**: mean synergy_ratio (비-trivial K) ≤ 0.5 →
  H1 FALSIFIED (redundancy 우세 또는 trivial 평탄).
- **F355.4 K-MONOTONIC**: synergy_total non-monotone in K → coupling-density 모형
  실패.
- **F355.5 BOUND/DETERMINISM**: synergy < 0 OR > 3 OR re-run drift → 산술 무효.
- **F355.6 POST-HOC**: frozen 후 verdict 방향 edit → raw#82 retraction.

## 8. Verdict

```
verdict_class: 🟢 SUPPORTED-NUMERICAL — collective-Φ flow의 PID 는 synergy 우세.
        mean synergy_ratio (non-trivial K {0.33, 0.67, 1.0}) = 1.0 ≫ 0.5.
        gate 5 PASS / 0 FAIL.

config: 3 binary substrates × 1 cell · 8-state · 8 permutation seeds (full
  enumeration of XOR-cell masks) · K ∈ {0.0, 0.33, 0.67, 1.0} · net 3-source
  McGill co-information II_3 (sign: >0 = synergy, <0 = redundancy)

table (mask permutation):
  K      mask        synergy   redundancy   synergy_ratio
  0.00   [0,0,0]     0.0       0.0          0.0  (trivial — pure unique-info)
  0.33   [1,0,0]     1.0       0.0          1.0
  0.33   [0,1,0]     1.0       0.0          1.0
  0.33   [0,0,1]     1.0       0.0          1.0
  0.67   [1,1,0]     2.0       0.0          1.0
  0.67   [1,0,1]     2.0       0.0          1.0
  0.67   [0,1,1]     2.0       0.0          1.0
  1.00   [1,1,1]     3.0       0.0          1.0

K-bucket means:
  K=0.00 (anchor)   mean_syn=0.0  mean_red=0.0  mean_ratio=0.0
  K=0.33            mean_syn=1.0  mean_red=0.0  mean_ratio=1.0
  K=0.67            mean_syn=2.0  mean_red=0.0  mean_ratio=1.0
  K=1.00 (anchor)   mean_syn=3.0  mean_red=0.0  mean_ratio=1.0

mean synergy_ratio over non-trivial K = (1.0 + 1.0 + 1.0) / 3 = 1.0.
K-dependency: synergy strictly monotone increasing — 0 → 1 → 2 → 3 in lockstep
  with XOR-cell count. Each XOR cell contributes +1 to net synergy; each
  identity cell contributes 0 (pure unique-info, net co-info=0).

criteria:
  C1 PURE-SYNERGY ANCHOR (K=1 synergy=3, red=0)          : PASS
  C2 PURE-IDENTITY ANCHOR (K=0 synergy=0, red=0)         : PASS
  C3 SYNERGY-RATIO VERDICT (mean=1.0 > 0.5)              : H1 SUPPORTED
  C4 K-MONOTONIC (0 ≤ 1 ≤ 2 ≤ 3 in K)                    : PASS
  C5 BOUND + DETERMINISM                                  : PASS

falsifiers:
  F355.1 PURE-SYNERGY ANCHOR     : PASS  (K=1 synergy=3.0, redundancy=0.0)
  F355.2 PURE-IDENTITY ANCHOR    : PASS  (K=0 synergy=0.0, redundancy=0.0)
  F355.3 SYNERGY-RATIO VERDICT   : H1 SUPPORTED  (mean ratio = 1.0 ≫ 0.5)
  F355.4 K-MONOTONIC             : PASS  (synergy 0 ≤ 1 ≤ 2 ≤ 3)
  F355.5 BOUND + DETERMINISM     : PASS  (0 ≤ syn ≤ 3 all perms; K=1 re-run identical)
  F355.6 POST-HOC                : NOT_TRIGGERED

checks: 5 PASS / 0 FAIL  (n_perms=8)

evidence_summary: 🟢 SUPPORTED-NUMERICAL — 다중 substrate 의 cross-substrate
  collective 흐름을 3-source net McGill co-information 으로 분해했을 때
  **synergy 가 redundancy 를 완전히 압도** (mean ratio = 1.0 across 모든
  비-trivial K). XOR coupling 이 켜진 모든 cell 은 순수 synergy 기여
  (per-cell II_3 = +1), identity coupling cell 은 zero 기여 (net co-info=0,
  순수 unique-info). redundancy 는 모든 8 permutation 에서 동일하게 0 — XOR
  family substrate 에서 sources 는 uniform ensemble 하에 독립이라
  shared-information 항이 0. K-monotonic (0 → 1 → 2 → 3): coupling density 가
  synergy 의 결정자. 이 결과는 H_293/H_294 의 ECA single-substrate 결과와
  **방향이 일치하면서 강도가 강함** — H_294 는 ECA cell-flow 의 synergy 가 Φ 를
  추종하지 *못함* 을 보였으나 (synergy ⊥ Φ, r=0.030), 본 H 는 hivemind cross-
  substrate flow 자체의 PID 구조 가 압도적 synergy 임을 보임. 단 둘은 다른
  질문: H_294 = 측정 가능한 흐름 성분이 의식 적분(Φ)을 추종하는가; H_355 =
  hivemind cross-flow 가 어떤 PID 형태인가. **두 결론의 결합**: hivemind 흐름은
  synergy 우세이나 (H_355), 그 synergy 가 collective-Φ 를 추종한다는 보장은 없다
  (H_294 의 ECA 교훈 hivemind 외삽 시 — 별도 검정 필요, §10 Next).

falsifiers_triggered: 없음 (모든 5 falsifier PASS).
```

re-run byte-identical 확인 (F355.5b).

`hexa verify` (VERBATIM) — g5 정직 fence:

```
verify --fence "H_355 in a 3-binary-substrate hivemind toy under XOR-density
   coupling K ∈ {0, 1/3, 2/3, 1}, the net 3-source McGill co-information of
   the cross-substrate flow is synergy-dominant: across all 8 cell-permutation
   seeds and the 3 non-trivial K buckets, synergy_total / (synergy_total +
   redundancy_total) = 1.0 (synergy strictly monotone in K: 0,1,2,3; redundancy
   identically 0 — XOR-family sources are independent under uniform ensemble);
   deterministic toy substrate, net co-info NOT full Williams-Beer 18-atom PID
   lattice; PID-structure claim, NOT a collective-Φ tracking claim (sister to
   H_293/H_294 which closed the ECA case at synergy ⊥ Φ)"
  tier   = ⚪ SPECULATION-FENCED
  reason = imagination/metaphor class (hexa-bio AXIS) — verification N/A by
           design; values deterministic arithmetic, interpretation fenced
```

## 9. Honest Limits (raw#91 c3)

- **L1 (net co-information ≠ full PID)**: II_3 는 3-source synergy/redundancy 의
  *net* 요약 (McGill co-information). full Williams-Beer 18-atom 3-variate PID
  lattice 는 더 세밀한 분해를 준다 — 특히 redundancy 와 unique-info 의 명시 분리.
  본 H 의 결론(net synergy 우세 + K-monotonic + identity=0 net)은 net 수준에서
  이미 결정적이나, redundancy 의 *positive* 항을 보려면 redundancy>0 substrate
  필요 (L2 참조).
- **L2 (XOR-family ⇒ redundancy = 0)**: 본 substrate (XOR cells + identity cells)
  의 sources 는 uniform ensemble 하에 모두 독립 — 따라서 shared-information 항이
  identically 0. redundancy 가 Φ 와 어떻게 관계되는지는 redundancy>0 substrate
  (copy/majority hivemind 또는 noise-correlated sources) 에서 별도 검정 필요.
  본 H 의 verdict (synergy 우세) 는 한쪽이 정확히 0 인 비대칭 경우이므로
  symmetric redundancy 영역 검정은 미수행.
- **L3 (PID 정의 sensitivity — MMI vs Idtxl vs Bertschinger)**: PID 부호 규약은
  컨벤션에 민감 (특히 2-source vs 3-source 부호 반전 — 본 H 의 핵심 함정이었음).
  McGill net co-info 를 H_294 와의 0-axiom 연속성 위해 선택. 대안 정의 (MMI 기반
  Williams-Beer Imin, Bertschinger 등) 는 net synergy 의 절대값 (raw counts) 을
  relabel 할 수 있으나 K-monotone 방향과 identity=0 anchor 는 정의 무관 robust.
- **L4 (small substrate)**: 3 substrates × 1 cell = 8-state. 큰 N hivemind (e.g.
  10 substrates × 4 cell) 에서 같은 PID 구조가 보존되는지는 별도 검정. 본 H 의
  결론은 minimal hivemind 의 결정적 PID 구조 statement.
- **L5 (deterministic permutation, not RNG seeds)**: "multi-seed" 가 RNG 가 아닌
  permutation enumeration (8 XOR-cell masks 전체). robustness 는 mask 다양성
  (K-bucket 내 mask 위치 변화) 에 대한 covariance 로 측정 — 모든 mask 가 동일한
  synergy_ratio=1.0 을 주므로 permutation invariance robust. RNG seed 와 다른
  의미의 "multi-seed".
- **L6 (collective-Φ 직접 측정 아님)**: 본 H 는 cross-substrate 흐름의 PID
  *구조* 에 대한 주장. collective-Φ 의 *절대값* 이 synergy_total 과 같다는
  주장 아님. H_294 의 ECA single-substrate 교훈 — synergy ≠ Φ — 은 hivemind
  으로 외삽시 별도 검정 필요 (§10 (a) Next).
- **L7 (substrate proxy)**: 3-binary toy = collective flow proxy, phenomenal
  collective consciousness 주장 아님. ECA H_287-294 와 동일한 honest scope.
- **L8 (verdict ≠ 형이상학)**: SUPPORTED-NUMERICAL 은 toy 측정 사실 — 다중
  substrate 흐름의 PID structure 가 XOR coupling 영역에서 synergy 우세라는
  결정적 산술. "hivemind 의식이 synergy 다" 같은 주장으로 확대 금지.

## 10. Cross-Links

- **sister (ECA arc, 직접 모방)**: [[H_293]] (multivariate-TE synergy ECA —
  PARTIAL: synergy 회복하나 r 악화) · [[H_294]] (PID synergy ECA — CLOSED-NEGATIVE:
  synergy ⊥ Φ, r=0.030). 본 H 는 둘의 *hivemind 측* sister — substrate 내부 cell-
  flow 가 아닌 substrate 간 cross-flow 의 PID 구조.
- **sister (TE arc)**: [[H_290]] (transfer-entropy-Φ correlate ECA, r=0.883) —
  본 H 의 axis F1 mirror H_356 (`hivemind-transfer-entropy-align`) 가 같은
  hivemind 외삽 추적 예정.
- **mirror (F1 round 1)**: [[H_352]] (collective-Φ super-additive — F1 첫 H) —
  H_352 가 collective-Φ 의 *크기* (Φ_collective vs Σ Φ_i) 를 묻는다면, 본 H 는
  같은 hivemind 흐름의 *PID 형태* 를 묻는다. 둘은 직교 측정 (크기 ⊥ 분해 형태).
- **next round (F2 cross-link 후보)**:
  - (a) **collective-Φ ∥ PID synergy?** — H_294 의 ECA 교훈을 hivemind 으로
    외삽 — 본 H 의 synergy_total 이 (별도 측정된) collective-Φ 를 추종하는가?
    H_294 는 ECA 에서 r=0.030 으로 직교 — hivemind 에서 보존되는지 검정.
  - (b) **redundancy>0 substrate** — copy/majority hivemind 또는 correlated
    noise sources 로 symmetric redundancy 영역 검정 (L2).
  - (c) **full 18-atom Williams-Beer trivariate PID lattice** — net co-info net
    조각이 아닌 unique×3 + redundancy×4 + synergy×4 + … 18-atom 분리 (L1).
  - (d) **larger N hivemind** — 10 substrates × 4 cell scale-up — XOR-coupling
    이 multi-cell substrate 위에서도 동일 PID 구조를 유지하는지 (L4).
- **engine-light (g61)**: `UNIVERSE/state/h355_collective_phi_pid_synergy_2026_05_28/run_h355.hexa`
  inline 16-bin joint histogram + bitmask marginal entropy. 새 lib 코드 0줄, 기존
  HEXAD/IIT4 lib 미의존 (PID 구조 측정은 big_phi 의존 없음).
- **paper hook**: H_293/H_294 ECA arc 의 hivemind 확장 — `PAPER/phi-information-
  triangulation` §future 의 "PID across substrate scales" prediction 의 hivemind
  측 첫 측정.
