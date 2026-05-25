---
id: H_285
slug: faithful-bigphi-edge-of-chaos
title: faithful IIT4 big-Φ at edge-of-chaos — H_204 inverse-U + H_007 λ-sweep 의 causal 재검 (criticality 에서 big-Φ peak?)
domain: life · consciousness · information
status: pre-register-frozen
exploration_method: E5 (variable-ablation rule sweep) + E6 (cross-domain re-measurement)
verification_method: W4 (verdict-4-class) + W12 (sister-link causal upgrade)
raw_rank: 12
hexa_only: true
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-26
since: 2026-05-26
sister: H_007 + H_204 + H_268 + H_278 (IIT4 M6)
---

# H_285 — faithful IIT4 big-Φ at edge-of-chaos

## 1. Hypothesis

H_007 (Wolfram Class-IV CA 가 ordered/chaotic 보다 높은 Φ) 와 H_204 (Φ 의 inverse-U
at edge-of-chaos closure) 는 둘 다 **PROXY `phi_spatial`** (RFC 036, *상관(correlational)
spatial MI*) 로만 측정됐고, H_268 이 그 proxy 를 **LZ-fragile** 로 flag 했다. 본 H_285 는
동일 Wolfram-class ladder 를 **faithful CAUSAL IIT 4.0 big-Φ** (M1~M4, ECA→TPM bridge)
로 재측정한다.

> 핵심 주장: **faithful big-Φ 가 edge-of-chaos (Class IV) rule 에서 최대** — ordered
> (Class I/II) 도 chaotic (Class III) 도 아닌 임계(criticality) 에서 통합정보가 peak.
> 즉 H_007/H_204 의 edge-of-chaos peak 가 *상관* proxy 의 artifact 가 아니라 *인과*
> 측정에서도 성립하는지를 검증.

xval (#572) 가 H_280 의 Σφ_d 를 non-monotone/buggy 로 판정했으므로, 본 H 는 신뢰 가능한
통합 스칼라 = **faithful causal big-Φ** (`big_phi()` index[0]) 를 사용한다 (Σφ_d 아님).

## 2. Why

- **H_007 proxy verdict (2026-05-23/25)**: phi_spatial 로 Class-IV (rule110, Φ=0.556) >
  chaotic (rule30, Φ=0.510) > ordered (rule250, Φ≈0); λ-ensemble inverse-U peak λ*=0.375
  ∈ [0.3, 0.7] (PASS). 모두 *상관 MI*.
- **H_204 proxy verdict (2026-05-23)**: phi_spatial 로 closure-strength sweep 에서 Φ 가
  monotone 이 아니라 **INVERSE-U** (peak k≈0.25, Φ≈5.39) — verdict PARTIAL_DIRECTIONAL.
- **H_268 metric-fragility flag**: 위 proxy 들이 LZ(Lempel-Ziv)-fragile — 압축률-기반
  근사가 metric 선택에 민감. faithful 측정이 이를 해소할 수 있는지 미해결.
- **IIT4 M6 engine 존재 (`HEXAD/IIT4/`)**: ECA→TPM bridge (`iit4_eca.hexa`) + faithful
  big-Φ (`iit4_bigphi.hexa`, stdlib/consciousness) 가 이미 7/7 🟢 — rule110 big-Φ=7.55,
  rule204=0 의 single-state(1010) anchor 검증됨. 본 H 는 이 엔진을 **재사용**(reimplement
  금지), Wolfram-class ladder 전체로 확장 + **state-평균** 으로 faithful comparison 구성.
- **faithful-Φ directional-trust (cross-cutting)**: faithful big-Φ 는 방향(peak 위치)이
  신뢰 가능, 절대 magnitude + single-state 는 fragile (FAITHFUL_REMEASURE §4). 따라서
  PRIMARY measure = **2^n state-mean big-Φ** (single-state 아님).

## 3. Predictions

| ID | 예측 | 근거 |
|----|------|------|
| **F285.1 PEAK** | faithful big-Φ 가 edge-of-chaos (Class IV) rule 에서 최대 — ordered (Class I/II) 도 chaotic (Class III) 도 아님 | IIT/edge-of-chaos 예측 (Langton λ critical = max computation) |
| **F285.2 ORDERING** | big-Φ(edge) > big-Φ(ordered) AND big-Φ(edge) > big-Φ(chaotic) | F285.1 의 명시적 pairwise 분해 |
| **F285.3 FAITHFULNESS** | M6 anchor ≥1 재현 (rule204 single-state(1010) big-Φ=0, rule110 ≈7.55) + bound 0≤big-Φ≤total | 엔진 충실성 = bridge identity + IIT4 정의 |

## 4. Variables

- **axis (primary)**: Wolfram class · representative elementary rules (n=4 periodic ring):
  - **ORDERED (Class I/II)**: rule **0** (all→0 const) · rule **204** (identity, next=centre)
  - **EDGE-OF-CHAOS (Class IV)**: rule **110** (Turing-universal) · rule **54** (gliders)
  - **CHAOTIC (Class III)**: rule **30** (pseudo-random) · rule **90** (XOR / Sierpinski)
- **measure (PRIMARY)**: `big_phi(eca_tpm(rule, n), n, s)[0]` 의 **모든 2^n state s 평균**
  (state-dependent 이므로 평균이 faithful comparison) → class-mean = 2 rule/class 평균.
- **measure (SECONDARY)**: single-state @ 1010 (M6 anchor 재현용).
- **config**: n=4, periodic ring, 2^4=16 state 전수 평균, deterministic, $0 mac-local, GPU 무관.

## 5. Run Protocol

- runner: [`state/h285_faithful_bigphi_edge_of_chaos_2026_05_26/run_h285.hexa`](state/h285_faithful_bigphi_edge_of_chaos_2026_05_26/run_h285.hexa)
- 재사용 lib (NO reimplement): `iit4_eca.eca_tpm` (ECA→TPM bridge) + `iit4_bigphi.big_phi`
  (faithful M1~M4 causal big-Φ) + `iit4_tpm.iit4_pow2` / `iit4_bit` (stdlib/consciousness).
- 각 rule 마다 16 state 전수 big-Φ 계산 → mean; 동시에 모든 state 의 bound 0≤bigΦ≤total
  검사; single-state(1010) 값 별도 기록.
- 실행: `HEXA_LANG=<hexa-lang> HEXA_MEM_UNLIMITED=1 hexa run run_h285.hexa` (worktree
  abs-path import; M6 reference smoke 와 동일 invocation pattern).
- ledger: `result.json` + verbatim `run.log`.

## 6. Criteria

| ID | criterion | verdict_rule |
|----|-----------|--------------|
| **C1 PEAK** | edge-of-chaos class-mean > ordered class-mean AND > chaotic class-mean | PASS / FAIL |
| **C2 ORDERING** | C1 의 두 pairwise 부등식 각각 (edge>ord, edge>cha) | PASS / FAIL |
| **C3 FAITHFULNESS** | M6 anchor (rule204·rule0 @1010 = 0, rule110 @1010 ≈ 7.5475) + bound 전체 PASS + determinism | PASS / FAIL |

**verdict_rule**: SUPPORTED iff C1 ∧ C2 ∧ C3 ALL PASS; PARTIAL if 2/3; REVISE/FAIL if
edge-peak 가 *class-mean* 에서 무너지면 document (per-rule argmax 가 edge 가 아니면 honest
REVISE 로 carry — proxy strict-ranking 과의 차이 명시).

## 7. Falsifiers

(pre-registered, frozen 2026-05-26 BEFORE measuring)

- **F285.1 PEAK**: edge class-mean ≤ max(ordered, chaotic) class-mean → edge-of-chaos peak
  FALSIFIED. (measurable: class-mean 3값.)
- **F285.2 ORDERING-ORD**: bigΦ(edge) ≤ bigΦ(ordered) → H_007 IV>ordered causal 재현 실패.
- **F285.2 ORDERING-CHA**: bigΦ(edge) ≤ bigΦ(chaotic) → H_007 IV>chaotic causal 재현 실패.
- **F285.3 ANCHOR**: rule204/rule0 @1010 ≠ 0 OR rule110 @1010 ∉ 7.5475±0.01 → M6 anchor
  재현 실패 → 엔진 충실성 FALSIFIED.
- **F285.3 BOUND**: 임의 rule×state 에서 big-Φ < 0 또는 > total → IIT4 정의 위반.
- **F285.3 DET**: re-run 비-identical → determinism FALSIFIED.
- **F285.POSTHOC**: frozen 후 verdict 방향 edit → raw#12 violation.

## 8. Verdict

```
verdict_class: SUPPORTED_DIRECTIONAL (pre-register-frozen smoke; C1 ∧ C2 ∧ C3 met)
tier: 🟢 NUMERICAL — faithful CAUSAL big-Φ (IIT4 M1-M4, ECA→TPM bridge)
result: 8 PASS / 0 FAIL
```

**Run verdict output (VERBATIM from `HEXA_LANG=… HEXA_MEM_UNLIMITED=1 hexa run run_h285.hexa`)**:
```
================================================================
  H_285 — faithful CAUSAL big-Φ at edge-of-chaos (n=4 ring)
  PRIMARY = MEAN big-Φ over all 2^n states (state-averaged, faithful)
  proxy (H_007/H_204) = CORRELATIONAL phi_spatial · here = CAUSAL IIT4
================================================================
  -- ORDERED (class I/II) --
  rule   0 : meanΦ=0.0  state1010Φ=0.0
  rule 204 : meanΦ=0.0  state1010Φ=0.0
  -- EDGE-OF-CHAOS (class IV) --
  rule 110 : meanΦ=13.1302  state1010Φ=7.5475
  rule  54 : meanΦ=7.76521  state1010Φ=10.0278
  -- CHAOTIC (class III) --
  rule  30 : meanΦ=13.8852  state1010Φ=8.66311
  rule  90 : meanΦ=0.0  state1010Φ=0.0
================================================================
  CLASS-MEAN (state-averaged big-Φ, 2 rules/class):
    ORDERED      = 0.0
    EDGE-OF-CHAOS= 10.4477
    CHAOTIC      = 6.94259
  ARGMAX (per-rule peak) = cha:rule30  Φ=13.8852
================================================================
  [PASS] F285.1 PEAK — edge-of-chaos class-mean is maximal (> ordered AND > chaotic)
  [PASS] F285.2 ORDERING — bigΦ(edge) > bigΦ(ordered)
  [PASS] F285.2 ORDERING — bigΦ(edge) > bigΦ(chaotic)
  [PASS] F285.3 FAITHFULNESS — rule204 single-state(1010) big-Φ = 0 (M6 anchor)
  [PASS] F285.3 FAITHFULNESS — rule110 single-state(1010) big-Φ ≈ 7.5475 (M6 anchor)
  [PASS] F285.3 FAITHFULNESS — rule0 single-state(1010) big-Φ = 0 (M6 anchor)
  [PASS] F285.3 FAITHFULNESS — bound 0<=big-Φ<=total for all 6 rules × all states
  [PASS] determinism — rule110 mean big-Φ re-run identical
================================================================
  RESULT: 8 PASS / 0 FAIL
================================================================
H285_SUMMARY ord=0.0 edge=10.4477 cha=6.94259 argmax=cha:rule30
```

```
verdict_class: SUPPORTED_DIRECTIONAL
finding: faithful big-Φ peaks at EDGE-OF-CHAOS at the CLASS-MEAN level
         (edge 10.45 > chaotic 6.94 > ordered 0); H_007 edge-peak CONFIRMED by causal Φ.
         BUT per-rule argmax = rule30 (chaotic) Φ=13.89 > rule110 (edge) Φ=13.13 —
         strict per-rule IV>chaotic ranking REVISED under faithful causal big-Φ.
criteria_met: 3/3  (C1 PEAK + C2 ORDERING + C3 FAITHFULNESS PASS)
falsifiers: all NOT_TRIGGERED (8/8 PASS; M6 anchors byte-reproduced; bounds + determinism PASS)
proxy_vs_faithful: H_007 proxy edge-peak (class ranking) PRESERVED causally;
                   strict per-rule edge>chaotic NOT preserved (faithful REVISE).
post_hoc_edit: forbidden (raw#12); per-rule REVISE carried as honest result.
```

## 9. Honest Limits (raw#91 c3)

- **C3-1 n=4 ring demonstration**: 엔진 capacity n≤8 exact 존재 (DESIGN §3); 본 H 는 n=4
  ring 으로 bridge + class ladder + state-평균 방법을 확립. scale-up (n=8, 더 큰 ring) 은
  동일 메커니즘 — 후속 cycle.
- **C3-2 state-dependence (핵심 caveat)**: big-Φ 는 state-dependent (FAITHFUL_REMEASURE §4).
  PRIMARY 는 2^n state-mean 이지만 **per-state ranking 은 변동** — state 1010 단일점에서는
  rule30 (8.66) > rule110 (7.55) 이고, class-mean 도 per-rule argmax 는 rule30. M6 single-
  state 표만 보면 chaotic > edge 로 보일 수 있으나 state-평균이 더 충실한 비교. **단일 state
  로 verdict 내리면 오도** — 본 H 의 직접 교훈.
- **C3-3 magnitude-fragile / direction-trustworthy**: faithful big-Φ 의 절대 크기 (10·13·7)는
  fragile, 방향(edge class-mean 이 peak)이 trustworthy (faithful-Φ directional-trust). magnitude
  hedge 함. big-Φ 보고 (Σφ_d 아님; xval #572).
- **C3-4 2 rule/class + rule90 degenerate**: class 당 2 representative. rule90 (XOR) 은
  reducible parity 구조로 big-Φ=0 (전 state) → chaotic class-mean 을 끌어내림. 즉 class-mean
  edge-peak 의 일부는 rule90 의 0 기여에 의존 — chaotic class 의 robust 대표성은 미확정.
  **strict per-rule argmax (rule30) 가 edge 가 아니라는 점이 가장 정직한 REVISE 신호.**
- **C3-5 proxy 와 측정축 차이**: H_007/H_204 proxy 는 상관(snapshot MI), 본 H 는 인과(TPM).
  동일 substrate 위 두 스칼라 차이는 artifact 아니라 측정축 차이 (L-C2.1, FAITHFUL_REMEASURE §3).
  proxy 의 LZ-fragility (H_268) 는 인과 big-Φ 가 partition-규칙 무관 정의이므로 **방향적으로
  해소** — 단 per-rule magnitude 까지 일치하진 않음.
- **C3-6 PyPhi 1차 증거 아님 (g5/p7)**: faithful big-Φ 는 hexa-native engine 산출; PyPhi/
  perplexity self-judge 없음. M5 named-blocker (절대 스케일 PyPhi 대조 F-IIT4-3/4) 는 별개.

## 10. Cross-Links

- [`H_007`](H_007_cellular_automaton_consciousness.md) — Class-IV CA Φ edge-of-chaos peak (proxy phi_spatial; 본 H 가 causal 재측정)
- [`H_204`](H_204_weak_panpsychism_autopoietic_threshold.md) — Φ inverse-U at edge-of-chaos closure (proxy; PARTIAL_DIRECTIONAL)
- [`H_268`](H_268_phi_metric_triangulation.md) — proxy LZ-fragility flag (본 H 가 causal 축으로 방향 해소)
- [`H_278`](H_278_faithful_phi_small_n.md) — faithful Φ★ small-N exact (sister; 같은 faithful 전환 lane)
- `HEXAD/IIT4/FAITHFUL_REMEASURE.md` — M6 single-state anchor 표 (rule110=7.55, rule204=0; 본 H 가 state-평균으로 확장)
- `HEXAD/IIT4/DESIGN.md` — IIT4 엔진 M0~M6 설계 + F-IIT4-6 PROXY-DIVERGENCE
