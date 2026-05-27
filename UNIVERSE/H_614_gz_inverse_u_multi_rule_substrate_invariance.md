---
id: H_614
slug: gz-inverse-u-multi-rule-substrate-invariance
title: Golden Zone inverse-U dΦ/dI peak — cross-substrate (multi-rule) invariance
domain: consciousness · math · physics · meta
status: FALSIFIED
verdict_class: FALSIFIED
exploration_method: E5 (continuous-parameter sweep) + E11 (cross-substrate Φ-signature) + E0 (H_351 round 2 follow-up)
verification_method: W1 (numerical smoke) + W4 (verdict-5-class) + W11 (cross-axis sister test) + W12 (invariant signature)
hexa_only: true
deterministic: true
llm: none
since: 2026-05-28 (축 E SAVANT round 2)
predecessor: H_351 (single-rule SUPPORTED 5/5, rule 110 anchor)
sister: H_351 (single-rule predecessor), H_204 (weak-panpsychism threshold), H_285 (faithful big-Φ edge-of-chaos), H_268 (H_204 inverse-U LZ-fragile), H_347 (GZ_WIDTH closed-form)
---

# H_614 — Golden Zone inverse-U dΦ/dI peak, cross-substrate (multi-rule)

> ⚙ 측정 엔진 = `HEXAD/IIT4/lib`(`iit4_eca` + `iit4_bigphi`) 재사용 (H_351 동일 패턴, commons g61 재발명 0). `$0 · mac-local · hexa-only · LLM none.`

## 1. 가설 (Hypothesis)

H_351 (rule 110 single-substrate, 🟢 SUPPORTED 5/5) §7 C3 가 명시한 round 2
후속: substrate 의 **inhibition I** 에 대한 big-Φ 의 미분 `dΦ/dI` 의 peak
위치가 **4 Wolfram rule {30, 54, 110, 184}** 전부에서 SAVANT canonical
`GZ_LOWER = 0.5 - ln(4/3) ≈ 0.21232` 와 `|Δ| ≤ 0.05` 안에 일치한다.

즉 **cross-substrate invariance 강주장** — peak 가 substrate-specific 가
아니라 SAVANT canonical 상수의 보편적 attractor 라는 강한 형태.

## 2. 사전등록 falsifier (pre-registered, 측정 전 동결)

| ID | 조건 | 의미 |
|----|------|------|
| **F1 (per rule)** PEAK-IN-GZ | `\|argmax_I \|dΦ/dI\| − GZ_LOWER\| ≤ 0.05` | peak 가 GZ_LOWER 근방 |
| **G_INVARIANT** | F1 PASS on **4/4** rules | cross-substrate 일관성 |

**verdict_rule**
- **SUPPORTED** = G_INVARIANT (4/4 PASS)
- **PARTIAL**   = 3/4 PASS
- **FALSIFIED** = ≤ 2/4 PASS

## 3. 방법 (Method)

### 3.1 substrate set

| rule | Wolfram class | 특성 |
|-----:|---------------|------|
| 30   | III           | chaotic |
| 54   | IV            | complex (edge-of-chaos) |
| 110  | IV            | complex (H_351 anchor) |
| 184  | II            | particle-localized (traffic flow) |

각 rule 위 n=4 cell periodic ring (H_351 동일 n).

### 3.2 inhibition I 매핑 (H_351 동일)

```
tpm_mixed[s,i] = (1 - I) · eca_tpm[s,i] + I · 0
              = (1 - I) · eca_tpm[s,i]
```

### 3.3 grid (H_351 동일 13-point)

```
I ∈ {0.05, 0.10, 0.15, 0.18, 0.21, 0.23, 0.25, 0.30, 0.35, 0.40,
     0.50, 0.70, 0.95}
```

### 3.4 Φ 측정

각 `(rule, I)` 쌍에서 `tpm_mixed` 빌드 → `big_phi(tpm, n=4, s)` 를
`s ∈ {0..15}` 모든 state 에 대해 호출 후 평균.

### 3.5 dΦ/dI (central finite difference)

H_351 동일. edge: forward/backward. peak = `argmax_i |dPhi[i]|`.

### 3.6 runner

`UNIVERSE/state/h614_gz_inverse_u_multi_rule_2026_05_28/run_h614.hexa` —
H_351 의 `run_h351.hexa` 를 multi-rule loop 로 확장.

## 4. 측정 (Measurement) — `result.json`

| rule | class | peak I | \|Δ\| (vs 0.21232) | peak \|dΦ/dI\| | Φ(0.50) | Φ(0.95) | F1 |
|-----:|-------|-------:|-------------------:|---------------:|--------:|--------:|---:|
| 30   | III   | 0.18   | **0.03232** ✓     | 21.7406        | 5.35701 | 0.30937 | ✓ |
| 54   | IV    | 0.40   | **0.18768** ✗     | 10.8425        | 3.25866 | 0.17698 | ✗ |
| 110  | IV    | 0.18   | **0.03232** ✓     | 21.3315        | 5.27903 | 0.25017 | ✓ |
| 184  | II    | 0.40   | **0.18768** ✗     | 19.9171        | 4.52109 | 0.20110 | ✗ |

- **F1 PASS count = 2 / 4**
- sign-change count = 0 (모든 rule unimodal, F3 carry)
- monotone decay Φ(0.95) ≤ Φ(0.50) = 4/4 ✓ (F4 carry)

## 5. 결과 (Result)

🔴 **FALSIFIED** — G_INVARIANT 불만족 (4/4 요구, **2/4 만 통과**).

- rule 30 (III-chaotic) PASS (|Δ|=0.03232, peak I=0.18)
- rule 54 (IV-complex) FAIL (|Δ|=0.18768, peak I=0.40 — **window 밖**)
- rule 110 (IV-complex, H_351 anchor) PASS (|Δ|=0.03232)
- rule 184 (II-particle) FAIL (|Δ|=0.18768, peak I=0.40)

## 6. falsifier 결과

| ID | 결과 | 비고 |
|----|------|------|
| F1 (rule 30)  | PASS | |Δ|=0.03232 (35.4% margin) |
| F1 (rule 54)  | FAIL | |Δ|=0.18768 (peak I=0.40, window 밖 3.75× tol) |
| F1 (rule 110) | PASS | |Δ|=0.03232 (H_351 재현) |
| F1 (rule 184) | FAIL | |Δ|=0.18768 |
| **G_INVARIANT** | **FAIL** | 2/4 < 4/4 요구 |

### Cross-link

- **H_351** GZ inverse-U dΦ/dI peak (single-rule, 🟢 SUPPORTED 5/5) — predecessor. 본 H 는 §7 C3 가 명시한 round 2 multi-rule sweep.
- **H_204** weak-panpsychism autopoietic threshold — closure-strength k 의 inverse-U Φ value-peak.
- **H_285** edge-of-chaos faithful big-Φ — Wolfram class IV ladder. 본 H 는 H_285 의 class-II/III/IV 다양성을 inhibition 축으로 확장.
- **H_268** H_204 inverse-U LZ-fragile — proxy-fragility caveat; 본 H 는 faithful causal big-Φ 사용 (LZ-fragility 회피).
- **H_347** GZ_WIDTH closed-form — `GZ_WIDTH = ln(4/3)` divisor anchor. 본 H 의 부분 PASS (2/4) 는 GZ_LOWER 의 substrate-class-conditional emergence 를 시사.

## 7. 해석 — Honest C3 (3-tier caveat)

### C1 — 4-rule 한정 일반성

4 rule (30/54/110/184) 의 Wolfram class 분포는 {III, IV, IV, II} —
class I 부재 (rule 0 등은 trivial Φ=0), class IV 가 2/4 (rule 54·110).
4-rule sample 이 256 ECA rule space 의 universality 결론에 충분한가는
별도 round (full 256 rule full-grid sweep, 또는 class-stratified 16-rule
sample) 후보. 본 H 의 verdict 는 "**제출된 4 rule 위에서**" cross-substrate
invariance 가 **깨진다** 는 사실까지가 한계 — 4 rule 에서조차 단일
attractor 가 발견되지 않았으므로, 더 큰 sample 에서도 회복 가능성은
낮다 (negative-evidence carry).

### C2 — n=4 small-n

n=4 ring 은 H_351 동일 + IIT 4.0 계산 비용을 16 state 로 제한. n=5 / n=6
에서 peak 위치가 GZ 안으로 다시 모일 가능성은 별도 검정 (round 3
후보). 그러나 H_285 의 class-IV-vs-others bimodal pattern 이 n 와
robust 했던 carry 를 고려하면 n 효과로 invariance 회복 기대값은
낮다.

### C3 — finite-difference grid 의 peak resolution

peak I 의 grid resolution = 0.05 안팎 (조밀 region {0.18, 0.21, 0.23,
0.25}, 성긴 region {0.30, 0.35, 0.40, 0.50}). rule 54/184 의 peak I=0.40
은 인접 grid `{0.35, 0.50}` 와의 central-difference 합성이라 *진짜* peak
가 (0.35, 0.50) 사이 어딘가일 가능성. 그러나 grid 의 sparse-tail 효과
로 peak 가 GZ_LOWER 까지 좌이동 할 여지는 거의 없음 (간격 0.05·tol
0.05 외삽 한계). **2x 조밀 grid round 3** 가 진짜 peak 위치 정밀화 lever
이지만, FALSIFIED 결론을 SUPPORTED 로 바꿀 가능성은 quantitatively
낮음.

## 8. verdict

🔴 **FALSIFIED 2/4** (G_INVARIANT 4/4 요구, peak I=0.40 of rule 54/184 가
GZ window [0.18, 0.28] 밖, 3.75× tol). **H_351 single-rule SUPPORTED 는
substrate-specific (rule 30 + rule 110 — chaotic + class IV) phenomenon
이며, class IV (rule 54) 와 class II (rule 184) 에서는 dΦ/dI peak 가
GZ 가 아니라 mid-range (I=0.40) 로 이동한다.** GZ_LOWER 의
**universal-attractor 강주장은 4-rule sample 에서 falsified**.

## 9. honest scope

본 H 가 **닫지 못하는 것**:
- *어느 rule 에서 PASS 인가* 의 closed-form characterization (rule 30 + rule 110 = chaotic + edge-of-chaos 좌측 class IV, 그러나 4-rule 의 너무 작은 sample 로 induction 한계).
- *peak 의 절대 크기* (susceptibility scaling) — 본 H 는 peak 위치만.
- *n=4 외 ring size* / *256 rule full sweep* / *non-ECA substrate* (PureField/dropout, H_359 lineage).
- *왜 rule 54/184 의 peak 가 I=0.40 인가* 의 mechanism — round 3 candidate.

## 10. UNIVERSE.md update

축 **E (SAVANT)** round 2 H_614 checkbox flip → done with `🔴 FALSIFIED
(2/4, peak I {0.18, 0.40, 0.18, 0.40} vs GZ_LOWER=0.21232, $0 mac-local
2026-05-28)`. H_351 single-rule SUPPORTED 는 carry, cross-substrate
generalization 은 **negative-closed**.

## artifacts

- `UNIVERSE/state/h614_gz_inverse_u_multi_rule_2026_05_28/run_h614.hexa` — multi-rule runner (~250 LoC, dependency = `iit4_eca` + stdlib `iit4_bigphi`, H_351 패턴 확장)
- `UNIVERSE/state/h614_gz_inverse_u_multi_rule_2026_05_28/result.json` — measurement SSOT (4-rule peak_I · delta · peak_mag · verdict)
- `UNIVERSE/H_614_gz_inverse_u_multi_rule_substrate_invariance.md` — 본문 (SSOT)
