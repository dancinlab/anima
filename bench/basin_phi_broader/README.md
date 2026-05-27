# BENCH #1-broader — BASIN-PHI-BROADER-RULES ("공명 측정자 — 광역 rule-set")

> Follow-up of [BENCH #1 BASIN-PHI-COUPLING](../basin_phi_coupling/README.md) (PR #1122, 🟠 WEAK-REVERSED, 8 rules) — 광역 16 rules × 4 Wolfram classes 검증.

## Verdict

**🔴 FAIL-REVERSED** (overall `max_basin ↔ mean_Φ`, 16 rules, `r = −0.896`, t = −7.55, df = 14)

H_346 capstone (`+0.550 max_basin↔Φ` on 4 curated rules) 의 **부호가 광역 16-rule frame 에서 강하게 역전** 된다. 그러나 **per-class 측정** 에서 다른 그림이 드러난다.

| Wolfram class | rules | `max_basin↔Φ` | `n_attr↔Φ` |
|---|---|---:|---:|
| I (fixed)    | 0, 8, 32, 40           | −0.600 | +0.600 |
| II (periodic)| 4, 56, 178, 184        | −0.920 | +0.706 |
| III (chaotic)| 18, 30, 90, 126        | −0.968 | +0.998 |
| IV (complex) | 54, 110, 124, 137      | **0.000** | **−0.998** |
| **overall (16)** | — | **−0.896** | **+0.641** |
| **class-avg r** | mean of 4 per-class r | −0.622 | +0.326 |

H_346 reference (n=5, 4 rules `{110, 30, 105, 150}`): `+0.550 / −0.951`.

## 핵심 발견

1. **overall sign reversal**: 8 rules (BENCH#1) `−0.314` → 16 rules `−0.896`. broader sweep 일수록 H_346 의 `+` sign 이 더 강하게 무너진다.
2. **class IV `max_basin↔Φ` degenerate**: tested 4 class IV rules 모두 `max_basin=4` (constant) → 분산 0 → r=0. 측정 불가능. 그러나 같은 class IV 안에서 `n_attr↔Φ = −0.998` 은 H_346 의 `−0.951` sign 과 매우 정합.
3. **class III `max_basin↔Φ = −0.97`** — rule=90 outlier (additive XOR, Φ=0 at max basin=16) 가 강한 sign 의 driver.
4. **`n_attr↔Φ` 부호가 class 별로 다르다**:
   - I/II/III: **positive** (더 많은 attractor → 더 높은 Φ)
   - IV: **negative** (더 많은 attractor → 더 낮은 Φ, H_346 sign 정합)
5. H_346 의 4 rules `{110, 30, 105, 150}` 분포: 110 ∈ IV, 30 ∈ III, 105 ∈ III, 150 ∈ III. **3 III + 1 IV** mix 가 우연히 `+0.55 max_basin↔Φ` 를 만들었다.

## H_345/346 scope 정정 권장

**원래 (H_346 abstract):**

> "basin size and exact Φ are monotonically coupled, sign-robust across sys-state averaging."

**정정 권장 1줄:**

> "**`n_attr↔Φ` 결합의 magnitude (\|r\| > 0.6) 는 Wolfram-class 별로 강건하나, `max_basin↔Φ` 의 + sign 은 H_346 의 curated 4-rule {110, 30, 105, 150} 의 우연한 정렬을 반영하며 광역 16-rule frame 에서 부호 역전된다.**"

## Files

- `bench.hexa` — pure hexa entrypoint, n=4 ECA + state-averaged exact Φ, 16-rule × 4-class sweep + per-class Pearson
- `result.json` — measurements verbatim + per-class r + overall r + class-avg + verdict + caveats
- `bench.log` — captured stdout
- `README.md` — this file

## Notes (post-merge)

- 2026-05-28 — `iit4_eca` 의존성이 hexa-lang stdlib (`stdlib/consciousness/iit4_eca`) 로 승격됨 (hexa-lang PR #1706). 본 bench 는 abs-path import → stdlib import 로 swap 완료 (anima g61 advisory 해소). 측정값 동일 (모듈 본문 무변동, import path 만 교체).

## Re-run

```
hexa run bench/basin_phi_broader/bench.hexa
```

Mac-local, ~57s wall, 256 `phi_structure` calls, 0 USD.

## Method

1. **Substrate**: n=4 ECA (4-cell periodic ring, 16 states).
2. **Rule set (committed BEFORE measurement, in source)**:
   - class I:   `{0, 8, 32, 40}`
   - class II:  `{4, 56, 178, 184}`
   - class III: `{18, 30, 90, 126}`
   - class IV:  `{54, 110, 124, 137}`
3. **Basin**: 50-step settle from each of 16 starts; `max_basin` = largest basin size, `n_attr` = number of attractors.
4. **Φ**: state-averaged exact `phi_structure(eca_tpm(rule, 4), 4, s)[4]` over `s ∈ 0..15`, returning `total = sum_phi_d + sum_phi_r` per H_321 convention.
5. **Pearson r**: computed (a) overall on 16 rules, (b) per-class on 4 rules each (df=2), (c) class-averaged as mean of 4 per-class r.
6. **Verdict thresholds pre-registered** in `bench.hexa` source before measurement.

## Anti-tautology

- 16-rule list + Wolfram class assignments committed in source ahead of measurement
- Wolfram class assignments follow Wolfram (2002) / Wuensche-Lesser atlas
- basin/Φ independently computed (dynamics vs TPM structure)
- pre-registered verdict thresholds honored even when primary axis (class IV `max_basin↔Φ`) is degenerate
- all 16 measurements reported verbatim including outliers (rule 90 Φ=0)

## Cross-link

- [UNIVERSE H_341](../../UNIVERSE/H_341_basin_phi_correlation.md) — n=4 exact, 4 rules, +0.776
- [UNIVERSE H_345](../../UNIVERSE/H_345_basin_phi_n5_exact.md) — n=5 single sys_state=21, 4 rules, +0.251/−0.799
- [UNIVERSE H_346](../../UNIVERSE/H_346_phi_state_sweep.md) — n=5 state-avg, 4 rules, +0.550/−0.951 🟢 capstone
- [BENCH #1](../basin_phi_coupling/README.md) — n=4 state-avg, 8 mixed rules, −0.314/+0.122 🟠
- [BENCH #1-broader (이 문서)](./README.md) — n=4 state-avg, **16 rules × 4 classes**, overall −0.896/+0.641 🔴-REVERSED

## Honest caveats

- `n_rules_per_class = 4` → df=2 per class; 3-point Pearson can hit |r| ≈ 1 by chance. Class-resolved certainty 는 8 rules per class (df=6) 필요.
- class IV 의 canonical 한 두 rule (54, 110) + Wolfram Atlas quasi-class-IV (124, 137) 모두 `max_basin = 4` — 같은 class 안에서 basin 축 분산 0. 작은 n=4 의 degeneracy 가능성.
- n=4 (16 states) 는 n=5 (32 states) 보다 Φ 해상도 낮음. n 축과 rule-set 축이 confound — follow-up 은 n=5 + 16-rule.
- rule 90 (additive XOR) 가 다시 class III outlier 로 작용 (max_basin=16, Φ=0) — class III r=−0.97 의 driver. outlier 제거 follow-up 권장.
- class-averaged r-of-r 는 표준 추론이 아닌 descriptive heuristic.
- verdict label 은 pre-registered tier; class IV degenerate basin 진단은 post-hoc 표기.

## Follow-ups (pre-registered for self-correction³)

1. **8 rules per class** (32 rules total, df=6 per class) — class III/IV r borderline 제거
2. **n=5 + 16 rules** — n 축과 rule-set 축 분리. class IV basin 축 variance 가 n=5 에서 회복되는지 검증
3. **outlier ablation**: rule 90 → rule 122 또는 146 으로 swap, class III r=−0.97 가 outlier driven 인지 확인
4. **class IV 의 max_basin=4 degeneracy 원인 조사** — n=4 small-n artifact vs class IV signature

## Significance vs H_346

H_346 abstract 가 주장한 "state-강건 monotonic coupling" 의 두 축 중:

- ✅ **`n_attr↔Φ` magnitude robust** (\|r\| > 0.6 in 3/4 classes; sign class-specific)
- ❌ **`max_basin↔Φ` + sign rule-set-dependent** — 16-rule broadening 에서 −0.896 으로 강하게 역전. H_346 의 4 rules `{110, 30, 105, 150}` 의 우연한 정렬.

본 bench 는 anima-side 결과로서 H_346 의 capstone 주장 중 `max_basin↔Φ +sign` 부분을 **광역 falsify**, `n_attr↔Φ magnitude` 부분은 **per-class basis 에서 유지** 됨을 측정으로 분리.
