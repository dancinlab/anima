# H_311 — rule 110 의 32 distinct Φ 의 algebraic structure: bit-complement / rotation orbit 검정

> arc 회귀: H_301 rule 110 → 32 distinct Φ (all unique). H_305 가 distinct=32 가 Turing-complete universality 가 모든 algebraic symmetry 깬다고 해석. 직접 검정 — bit-complement 와 D_5 rotation orbit 에서 Φ-equality 존재? 정말 0 인가?

## 1. 동기

- H_301 cycle#39: rule 110 n=5 cap=4 의 32 state Φ 가 *32 distinct* (all unique).
- H_305 cycle#43: distinct count = rule signature, rule 110 (class 4 Turing-complete) 이 모든 symmetry 깬다고 해석.
- 그러나 *bit-complement* (s ↔ ~s mod 32) 와 *rotation* (5-cyclic shift) 모두 ECA conservation 의 자연 symmetry.
- 만약 32 distinct 라면: rule 110 이 *진정으로* 모든 algebraic symmetry 위반 → universality 의 강한 증명.
- 만약 *near*-distinct (=29 or 30) 라면: rule 110 가 일부 symmetry 보존 — H_305 해석 수정.

## 2. 가설

**H1 BIT-COMPLEMENT-SYMMETRY**: 32 state 중 s 와 ~s mod 32 (=31-s) 가 Φ 같은 pair 가 존재 (이상적으로 16 pairs).

**H2 ROTATION-SYMMETRY**: 32 state 중 5-cyclic rotation (s_rot = ((s << 1) | (s >> 4)) & 31) 가 Φ 같은 pair 존재.

**H3 32-DISTINCT-IS-EXACT**: H_301 의 "32 distinct" 가 *exact* — 어떤 algebraic symmetry 도 Φ-equivalence 만들지 못함.

H1+H2 의 PASS 가 H3 FALSIFY. H1+H2 의 FAIL 이 H3 SUPPORTED.

## 3. 측정 방법

rule 110 n=5 cap=4 의 32 Φ values 측정 (H_301/H_305 재사용 OR 새로 측정). 그 다음:

- 16 bit-complement pair: (s, 31-s) for s ∈ {0..15} 의 Φ 값 비교 → count pairs with |Φ(s) - Φ(31-s)| < 0.001
- 32 rotation orbit: 각 state 의 5-rotation 4 회 iterate 해서 5-elt orbit, intra-orbit Φ variance 측정
- distinct value count re-verify (H_301 의 32)

## 4. 사전등록 falsifier

- **F311.1 BIT-COMPLEMENT-PAIRS**: rule 110 의 16 bit-complement pairs 중 ≥1 pair 가 Φ 같음 (|Δ|<0.001)
- **F311.2 ROTATION-INVARIANT-ORBITS**: 32 state / 5-rotation 의 ≥1 orbit (5 state) 가 모두 같은 Φ
- **F311.3 DISTINCT-COUNT-RECONFIRM**: rule 110 n=5 cap=4 32-state distinct count = 32 (H_301 cycle#39 reproduce)
- **F311.4 CONTROL-RULE-90-SYMMETRY**: rule 90 (XOR, D_5+complement 대칭 의심) 의 bit-complement pair 수 ≥10 (rule 110 과 sharp 대비)
- **F311.5 BOUND**

H3 SUPPORTED = F311.1 FAIL AND F311.2 FAIL AND F311.3 PASS. H3 PARTIAL = F311.1 PASS OR F311.2 PASS.

## 5. 비용

- $0 mac-local · 32 calls × n=5 cap=4 (~3-5min wall, H_301 와 동일)

## 6. 가능한 결과

| 시나리오 | 의미 |
|---|---|
| H3 SUPPORTED | rule 110 가 진짜 모든 algebraic symmetry 깸 — Turing-complete universality 의 강한 증명 |
| H3 PARTIAL (bit-pair) | bit-complement 만 부분 보존, rotation 깨짐 |
| H3 PARTIAL (rotation) | rotation orbit 일부 보존, distinct count 32 실은 over-count |
| H3 FALSIFIED | H_305 의 distinct=32 해석 수정 필요 |

## 7. honest limits

1. L1 cap=4 lower bound — true Φ 가 다를 수 있음, but binary symmetry classification robust
2. L2 single N=5 — n=6/7 의 symmetry pattern 변동 가능 (H_312)
3. L3 bit-complement = 1 specific symmetry, ECA 의 다른 symmetry (5-cyclic + reflection = D_5) 도 cover
4. L4 SPECULATION-FENCED
5. L5 rule 90 control = H_301 distinct=3 prediction; 정합 시 method 검증

## 8. 폐쇄

F311.1-5 결판.

## 9. 산출물

- state/h311_rule110_algebraic_structure_2026_05_26/{run_h311.hexa, result.json, run.log}

## 10. 후속

- H_315: rule 110 의 n=6 32→64 state extension symmetry 분석
- H_316: rule 30/60/90 의 ortbit decomposition 정량 (rule-signature 의 group-theoretic 해석)
