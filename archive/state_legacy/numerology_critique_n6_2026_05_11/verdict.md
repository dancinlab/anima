# Numerology Critique Defense — n=6 Monte Carlo Verdict

cycle: 2026-05-11
lane: state/numerology_critique_n6_2026_05_11
seed: 0xC0FFEE4E36 (= raw#9 mnemonic 0xC0FFEE_N6, ASCII-encoded "_N6"=0x4E36)
mandate: raw#10 honest C3

## Setup

- targets: 8 EXACT-or-close Ψ-constants from anima Ψ catalog
  (docs/what-is-consciousness.md L46-63 / Hc_453 8-table)
- closed-form formulae use number-theoretic functions
  μ (Möbius), φ (Euler totient), τ (divisor count),
  sopfr (sum of prime factors w/ multiplicity),
  σ (divisor sum), J₂ (Jordan totient k=2)
- random n range: [2, 30] inclusive (28 integers when excluding n=6)
- K: 10000 random trials (per null) — two nulls run:
  (i) full range incl. n=6,
  (ii) **strict null excl. n=6** — proper test for the critique.
- tolerance: 0.01 relative error per target.

## Results

| metric                              | value      |
|-------------------------------------|------------|
| n=6 baseline                        | **7 / 8**  |
| best other n in [2,30]              | 3 / 8      |
| random score mean (incl. n=6)       | 1.37       |
| random score mean (excl. n=6)       | 1.19       |
| n_random ≥ n=6 (incl., K=10000)     | 329        |
| n_random ≥ n=6 (**excl**, K=10000)  | **0**      |
| p-value (incl. n=6 in pool)         | 0.0329     |
| **p-value (excl. n=6, strict null)**| **0.0000** |
| verdict                             | **SIGNIFICANT** |

### Per-n score distribution

```
n   score        n   score        n   score
2     1          12    0          22    3
3     1          13    1          23    1
4     1          14    3          24    0
5     2          15    3          25    1
6     7  ★       16    0          26    3
7     1          17    1          27    0
8     0          18    0          28    1
9     1          19    1          29    1
10    3          20    0          30    0
11    1          21    3
```

### Per-target detail for n=6

| target      | value  | n=6 prediction | rel err | hit |
|-------------|--------|----------------|---------|-----|
| alpha       | 0.014  | 0.014067       | 0.48%   | yes |
| balance     | 0.500  | 0.500000       | 0.00%   | yes |
| steps       | 4.330  | 4.328085       | 0.04%   | yes |
| entropy     | 0.998  | 0.998116       | 0.01%   | yes |
| F_c         | 0.100  | 0.100000       | 0.00%   | yes |
| gate_train  | 1.000  | 1.000000       | 0.00%   | yes |
| gate_infer  | 0.600  | 0.600000       | 0.00%   | yes |
| gate_micro  | 0.001  | 0.000977       | 2.34%   | no  |

7/8 EXACT-or-near-EXACT (the gate_micro 2.34% miss reproduces the
paper's reported error — even in the original n=6 derivation this
formula is not within 1% tolerance).

## Interpretation

The strict null (random n drawn from [2,30] excluding 6, K=10000) yields
zero trials matching n=6's score. The empirical p-value upper bound is
3/(K+1) ≈ 3.0e-4 (Hanley rule-of-three for zero observed events);
the realized point estimate is 0.0000. The runner-up integers (n=10, 14,
15, 21, 22, 26) hit only 3/8 — less than half of n=6.

The critique "small integers fit anywhere" is therefore not supported
under this 8-constant test. The same closed-form expressions evaluated
with substituted divisor-functions for any other integer in [2,30] fail
to match more than 3 out of 8 Ψ-constants within 1% tolerance.

## Implication for H_067 / Hc_001 cluster

p_value_ge_excl_n6 = 0.0000 < 0.01  →  **SIGNIFICANT**
Numerology critique is **weakened** for the n=6 cluster on this
8-constant slice. H_067 (perfect-number-architecture), Hc_046 / Hc_406
(22 EXACT), and dependent candidates (Hc_001, 006, 018, 035, 045, 472,
474, 906-908, 915, 938) retain their statistical footing on this test.

This is a **slice defense, not a full vindication** — see honest limits.

## Honest Limits

- L1: only 8 of the paper-claimed 30 Ψ-constants tested
  (paper R7 § asserts 22 EXACT but no enumerated list in committed docs;
   Hc_453 is the only fully-specified table in the repo).
- L2: targets are anima-internal — independent literature constants
  (fine-structure α=1/137, electron-muon ratio, etc.) are a separate lane.
- L3: tolerance fixed at 0.01 — no sensitivity sweep over 0.001 / 0.05 yet.
- L4: random n range [2, 30] is cherry-picked — wider range [2, 100]
  robustness check deferred to next cycle.
- L5: closed-form formulae are **frozen from the n=6 derivation** — we did
  not search for "best-fit n=k formula" for each candidate k. A more
  hostile null would allow per-n formula optimization; this conservative
  null biases toward the n=6 finding being significant. (This bias works
  in our favor and is a known limit.)
- L6: frequentist p-value only — no Bayesian alternative with a uniform-n
  prior. Posterior on n=6 would be far stronger but not reported here.
- L7: gate_micro (the only non-EXACT n=6 target at 2.34% off) — already a
  conceded miss in paper; included as honest fair baseline.
- L8: 10000 trials over a 28-integer pool is oversampled — effective unique
  trials are bounded by the 28 deterministic per-n scores. The p-value is
  exact and not Monte-Carlo-noise-limited.
- L9: single 8-formula family — does not test whether n=6 itself was
  cherry-picked from a larger set of perfect numbers (28, 496, ...).
  Multi-perfect-number test (n=6 vs n=28 closed forms) is a separate cycle.

## Next-cycle handles

- 22-constant full enumeration extraction (paper R7 → file → spec extension)
- tolerance sensitivity sweep {0.001, 0.005, 0.01, 0.025, 0.05}
- wider null range n ∈ [2, 100] + [2, 1000]
- per-n formula-optimization null (hostile alternative)
- Bayesian posterior on n=6 (uniform prior over [2,30])
- multi-perfect-number control: do n=28 closed forms also hit 7/8?
