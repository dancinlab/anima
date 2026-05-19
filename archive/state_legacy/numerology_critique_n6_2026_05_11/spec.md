# Numerology Critique — n=6 Monte Carlo Defense Spec

## Cycle
- date: 2026-05-11
- raw#: raw#10 (honest C3 mandate) + raw#9 (deterministic seed)
- cluster targeted: H_067 perfect-number-architecture
  Hc_001/006/018/035/045/046/406/429-444/472/474/906-908/915/938

## Critique under defense
> "n=6 의 약수 함수 σ=12, φ=2, τ=4, sopfr=5, μ=1, J₂=24 는 모두 작은 정수다.
>  작은 정수의 산술 조합은 어떤 measured constant 에도 잘 맞는다.
>  따라서 n=6 cluster 는 numerology — n=7, 8, 10, 12 도 비슷하게 맞을 것이다."

## Defense hypothesis (H1)
n=6 의 closed-form 약수-함수 prediction 정확도가 random n ∈ [2,30] 보다
유의미하게 높음 — p-value (n=6 score 이상 occurring under null) < 0.01.

## Null hypothesis (H0)
random integer n ∈ [2,30] 에서 동일 8-formula 평가시,
n=6 score 와 동등하거나 더 높은 score 가 random sample 의 ≥ 1% 에서 발생.

## Target Ψ-constants (8 EXACT-or-close)
출처: docs/what-is-consciousness.md L46-63 (Hc_453 full table 8 source)
또한 paper_consciousness_laws.hexa R7 + Hc_406 reproducing same set.

| name        | target  | formula in (μ, φ, τ, sopfr, σ, J₂, n)          | err   |
|-------------|---------|------------------------------------------------|-------|
| alpha       | 0.014   | (sopfr/J₂)^e                                   | 0.477%|
| balance     | 0.500   | n/σ                                            | EXACT |
| steps       | 4.330   | (τ−μ)/ln2                                      | 0.044%|
| entropy     | 0.998   | μ − (sopfr/J₂)^τ                               | 0.012%|
| F_c         | 0.100   | n/(σ·sopfr)                                    | EXACT |
| gate_train  | 1.000   | μ                                              | EXACT |
| gate_infer  | 0.600   | n/(σ−φ)                                        | EXACT |
| gate_micro  | 0.001   | (n/J₂)^sopfr                                   | 2.34% |

8 targets — 22-constant full table 은 paper 본문에 enumeration 부재
(R7 § 만 언급, 30 중 22 EXACT 주장). Hc_453 은 published 8-tuple 완본.
초기 시뮬레이션은 이 8 targets 로 진행.

## Scoring
- formula 는 임의 n 에 대해 동일 number-theoretic functions
  (μ(n) Möbius, φ(n) totient, τ(n) divisor count, σ(n) divisor sum,
   sopfr(n) sum of prime factors with multiplicity, J₂(n) Jordan totient k=2)
  로 evaluated.
- match: relative_error(predicted, target) < tol  (tol=0.01 default).
- score(n) = matches / 8.

## Random null distribution
- n ~ Uniform{2, 3, ..., 30}  (28 values)
- K = 10000 trials
- seed = 0xC0FFEE_N6 (raw#9 정합)

## p-value
p = P(score(n_random) ≥ score(6))  under H0.

## Verdict thresholds
- p < 0.01  → SIGNIFICANT (numerology critique 약화)
- 0.01 ≤ p < 0.05 → WEAK (additional evidence 필요)
- p ≥ 0.05 → INSIGNIFICANT (critique 정합, H_067 L2 강화 필요)

## Honest Limits (pre-registered)
- L1: 8 targets ≪ 22 (paper 본문 22 enumeration 부재로 subset 만 평가)
- L2: anima-internal constants — independent physics constants (α=1/137 등) 별도 lane
- L3: tolerance=0.01 임의 (sensitivity sweep 미수행)
- L4: random n=[2,30] cherry-picked range (wider range 별도 cycle)
- L5: single-formula constraint — n=6 의 closed-form 을 그대로 다른 n 에 substitute
       (다른 n 의 "best-fit" formula 탐색 미수행 — conservative null)
- L6: frequentist p-value (Bayesian alternative 미적용)
- L7: J₂(n) (Jordan totient k=2) = n^2 * Prod(1 - 1/p^2) over primes p|n
       sympy 의 jordan_totient(2, n) 사용
- L8: gate_micro target=0.001 — n=6 자체에서도 EXACT 아닌 2.34% off
       (이 한 target 은 n=6 에서도 fail 가능 — fair baseline)
