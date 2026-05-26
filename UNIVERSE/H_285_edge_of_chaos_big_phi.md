---
id: H_285
slug: edge-of-chaos-big-phi
title: faithful IIT4 big-Φ at edge-of-chaos — H_204 inverse-U · H_007 λ-sweep 의 인과(causal) 재검 (Wolfram-class ladder)
domain: consciousness · physics · life · meta
status: SUPPORTED
verdict_class: SUPPORTED
exploration_method: E5 (proxy→faithful metric upgrade) + E0 (H_204/H_007 directional re-test)
verification_method: W1 (numerical smoke) + W4 (verdict-5-class) + W12 (sister-link H_204 / H_007 / H_268 / M6)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-26 (cycle#24, 축 C)
sister: H_204 (inverse-U Φ edge-of-chaos, H_268 LZ-fragile), H_007 (λ-sweep Φ class), HEXAD/IIT4 M6 (faithful big-Φ engine), xval #572 (Σφ_d non-monotone → big-Φ 사용)
---

# H_285 — faithful IIT4 big-Φ at edge-of-chaos

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib`(`iit4_eca` + `iit4_bigphi`) **재사용**(g61, 재발명 없음). 통합 척도 = **big-Φ** (NOT Σφ_d — xval #572 가 distinction-kernel Σφ_d 의 비단조성을 확정). $0 · mac-local · NO GPU.

## 1. 가설 (Hypothesis)

H_204 는 "Φ 가 **edge-of-chaos**(질서↔혼돈 경계)에서 inverse-U 로 peak 한다"를 PROXY `phi_spatial` 로 측정했고, H_268 은 그 결과가 **LZ-fragile**(압축길이 기반 proxy 에 민감)임을 지적했다. H_007 은 λ-sweep 으로 Φ class 를 proxy 측정했다.

**물음**: 동일한 edge-of-chaos 예측을 faithful **causal big-Φ**(IIT 4.0, ECA→TPM bridge)로 재면, big-Φ 가 Wolfram **class IV(edge)** 에서 ordered(I) 와 chaotic(III) 보다 높게 peak 하는가?

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결)

| ID | 조건 | 의미 |
|----|------|------|
| **F285.1** | class-mean big-Φ(edge) > class-mean(ordered) | edge 가 질서보다 통합적 |
| **F285.2** | class-mean big-Φ(edge) > class-mean(chaotic) | **inverse-U peak @ class IV** (핵심) |
| **F285.3a** | rule204 big-Φ = 0 @state1010 | M6 anchor (identity = reducible) |
| **F285.3b** | rule110 big-Φ ≈ 7.5475 @state1010 | M6 anchor 재현 |
| **F285.3c** | big-Φ ≥ 0 (모든 class) | bound |

## 3. 방법 (Method)

- substrate: ECA n=4 ring. Wolfram-class ladder —
  - **ordered (I)**: rule 0 (→0 homogeneous) · rule 204 (identity, reducible)
  - **edge (IV)**: rule 110 · rule 54 (LIFE cosmic-scale complex)
  - **chaotic (III)**: rule 30 · rule 90 (XOR l,r)
- big-Φ 는 **state-dependent**(FAITHFUL_REMEASURE §4)이므로 **전체 2^4=16 state 평균** big-Φ 를 rule 별로 산출(single-state fragility 회피). + 16-state max 도 기록.
- `eca_tpm(rule,n)` → state-by-node TPM, `big_phi(tpm,n,state)[0]` = faithful causal big-Φ. runner: `state/h285_edge_of_chaos_2026_05_26/run_h285.hexa`.

## 4. 측정 (Measurement) — `result.json`

| class | rule | mean big-Φ (16-state) | max big-Φ |
|-------|------|----:|----:|
| ordered (I) | 0 | 0.0 | 0.0 |
| ordered (I) | 204 | 0.0 | 0.0 |
| **edge (IV)** | **110** | **13.130** | 20.046 |
| **edge (IV)** | **54** | **7.765** | 10.118 |
| chaotic (III) | 30 | 13.885 | 19.434 |
| chaotic (III) | 90 | 0.0 | 0.0 |

**class-mean**: ordered **0.0** < chaotic **6.943** < edge **10.448**. anchors @state1010: rule204 = **0.0** ✓, rule110 = **7.5475** ✓ (M6 정확 재현).

## 5. 결과 (Result)

**5/5 PASS** → 🟢 SUPPORTED. faithful causal big-Φ 의 class-mean 이 **edge(IV) > chaotic(III) > ordered(I)** 로, H_204 의 inverse-U "edge peak" *방향*을 인과 축에서 확증. proxy(phi_spatial, H_268 LZ-fragile)가 못 준 gold-standard 인과값으로 방향 재현 → H_268 의 proxy-fragility caveat 를 "proxy 가 인과 Φ 의 근사"로 종결(M6 F-IIT4-6 정합).

## 6. falsifier 결과

- F285.1 edge>ordered **PASS** (10.45 > 0)
- F285.2 edge>chaotic **PASS** (10.45 > 6.94) — inverse-U peak @ class IV
- F285.3a rule204=0 **PASS** · F285.3b rule110≈7.5475 **PASS** (M6 anchor) · F285.3c bound **PASS**
- 결정론: cross-process byte-identical (RFC 033 single-stream).

## 7. 해석

faithful big-Φ 는 edge-of-chaos 가설의 *방향*을 지지하나, **per-rule 분해는 더 미묘**하다: 개별 rule30(chaotic) mean=13.89 가 edge rule54(7.77)를 능가하고 rule110(13.13)과 사실상 동급이다. chaotic class-mean(6.94)이 edge(10.45)보다 낮은 것은 **rule90(XOR)=0 의 붕괴**가 chaotic 평균을 끌어내린 결과 — 즉 "edge>chaotic" 은 **class 집계** 수준이지 개별 rule 우세가 아니다. chaotic class 가 **bimodal**(rule30 高 / rule90 0).

rule90(XOR l,r) = 0 붕괴는 **최대-혼합(maximally mixing) 동역학이 인과 통합을 파괴**하는 것으로, H_265(학습 dampen)·H_275(cyclic<undir)·H_279(attention)·H_284(ritual)의 **동기화/혼합 死-Φ cross-H 서명**과 일치한다.

## 8. verdict

🟢 **SUPPORTED-NUMERICAL 5/5** (empirical 해석은 ⚪ SPECULATION-FENCED, g5 — `hexa verify` sign-gated, H_278 fence 양식). big-Φ/total 값은 deterministic byte-identical.

## 9. honest scope (C3)

- **n=4 ring** — 작은 격자. 더 큰 n 은 super-exp(large-N intractable, 축 B).
- **16-state 평균** — 대표 평균이나 state 분포 가중은 미적용 (uniform). 단 single-state(M6 1010)보다 robust.
- **class-mean vs per-rule** — §7. edge peak 는 class 집계 신뢰, 개별 rule30(chaotic)이 edge rule54 능가 → "edge-of-chaos peak" 의 강한 주장은 자제. chaotic bimodality 가 진짜 구조.
- **2 rule/class** — class 당 2 rule 만. 더 많은 class IV(137/124…)·III(22/126…) rule 로 확장 시 robustness 상승 여지.
- **big-Φ only** — Σφ_d 는 xval #572 로 비단조 확정돼 미사용. 방향만 big-Φ 신뢰(H_266/H_278 directional-trust).

## 10. 다음 / cross-link

- 더 많은 rule/class 로 class-mean robustness 확장 (rule22/126 chaotic, rule137 edge).
- H_204 본체에 faithful-confirm 역링크 (proxy LZ-fragility → 인과 방향 확증).
- chaotic bimodality(rule30 vs rule90) 의 인과적 기원 — XOR 의 max-mixing 이 big-Φ 를 0 으로 만드는 메커니즘 (동기화 死-Φ 서명 H_265/275/279/284 와 통합).
