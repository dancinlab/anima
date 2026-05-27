# BENCH #1 — BASIN-PHI-COUPLING ("공명 측정자")

> anima-side benchmark of UNIVERSE H_345/346 capstone — basin ↔ exact Φ coupling on a **broadened** rule set.

## Verdict

**🟠 WEAK-REVERSED** (primary signal `max_basin ↔ mean_Φ`, Pearson `r = −0.314`, t = −0.81, df = 6)
**🔴 FAIL (near-zero)** (aux signal `n_attractors ↔ mean_Φ`, Pearson `r = +0.122`)

- pre-registered: `r ≥ +0.5` → 🟢 · `0.2 ≤ r < 0.5` → 🟠 · `r < 0.2` → 🔴.
- Sign 역전 + |r| < 0.5 → 🟠 WEAK-REVERSED (primary), 🔴 FAIL (aux).

## 핵심 발견

H_346 capstone의 basin↔Φ 결합(`+0.550 / −0.951`)은 **rule-set fragile** 이다. anima-side bench는 같은 n=4 substrate 위에서 H_345/346의 4-rule frame `{110, 30, 105, 150}` 을 8-rule frame `{45, 54, 60, 90, 110, 126, 150, 184}` (Wolfram class I-IV 망라)로 넓혔을 때:

- `max_basin ↔ mean_Φ` 부호가 `+ → −` 로 역전 (`+0.550 → −0.314`)
- `n_attr ↔ mean_Φ` 부호는 유지되나 강도가 `−0.951 → +0.122` 으로 거의 0 으로 붕괴

두 outlier 가 결합을 깨뜨린다:

| rule | max_basin | n_attr | mean_Φ | 노트 |
|---:|---:|---:|---:|---|
| 60 | 16 | 1 | 14.125 | additive but tilt-shift only (Φ ≠ 0) |
| **90** | **16** | **1** | **0.0** | additive XOR — flat phi_structure |

rule 90 같은 additive-XOR family 에서 basin은 최대(16)지만 phi_structure 가 0 — basin과 Φ의 동조가 TPM additivity 에서 깨진다. H_345/346 가 고른 4 rule 은 우연히 이 axis 를 피했다.

## Files

- `bench.hexa` — pure hexa entrypoint, n=4 ECA + state-averaged exact phi_structure, 8-rule sweep + Pearson
- `result.json` — measurements verbatim + Pearson r/t + verdict + caveats
- `bench.log` — captured stdout
- `README.md` — this file

## Re-run

```
hexa run bench.hexa
```

Mac-local, ~30s wall, 128 `phi_structure` calls, 0 USD GPU cost.

## Method

1. **Substrate**: n=4 ECA (4-cell periodic ring, 16 states).
2. **Basin**: 50-step settle from each of 16 starts (H_345 protocol); `max_basin` = largest basin size, `n_attr` = number of attractors.
3. **Φ**: state-averaged exact `phi_structure(eca_tpm(rule, 4), 4, s)[4]` over `s ∈ 0..15`, returning `total = sum_phi_d + sum_phi_r` per H_321 convention.
4. **Pearson r**: computed over 8 rules between (max_basin, mean_Φ) and (n_attr, mean_Φ).
5. **Verdict thresholds pre-registered** in `bench.hexa` source before measurement.

## Anti-tautology

- basin/Φ independently computed (dynamics vs TPM structure)
- Pearson computed on 8 measurements without post-hoc rule pruning
- pre-registered thresholds honored (result is allowed to be negative)
- rule list committed in source ahead of measurement

## Cross-link

- [UNIVERSE H_341](../../UNIVERSE/H_341_basin_phi_correlation.md) — n=4 exact, 4 rules, +0.776
- [UNIVERSE H_345](../../UNIVERSE/H_345_basin_phi_n5_exact.md) — n=5 single sys_state=21, 4 rules, +0.251/−0.799
- [UNIVERSE H_346](../../UNIVERSE/H_346_phi_state_sweep.md) — n=5 state-averaged, 4 rules, +0.550/−0.951 🟢 capstone
- [BENCH #1 (이 문서)](./README.md) — n=4 state-averaged, **8 rules**, −0.314/+0.122 🟠/🔴

## Honest caveats

- 8 rules → df=6 의 t-stat |0.81| 은 통계적 유의수준 미달 (양측 p > 0.4 at df=6)
- n=4 (16 states) 와 n=5 (32 states) 가 다르므로 n axis 와 rule-set axis 가 confound — follow-up (1) 은 n=5 + 8 rules
- rule=90 outlier 가 r 를 단독으로 끌어내림 — 제외시 r 추정은 다른 follow-up 의 범위
- 본 bench는 anima M-tensor 가 아닌 ECA substrate proxy 를 사용 — H_002/H_278/H_345 lineage 와 동일한 proxy 이므로 anima-side 적용 의의는 *조건적 의존성* (substrate proxy 가 anima M-tensor 와 같은 통계를 따른다는 추측 하)

## Follow-ups (pre-registered for self-correction³)

1. n=5 + 8-rule bench → n vs rule-set axis 분리
2. n=4 + H_345 4-rule {110, 30, 105, 150} → rule-set이 dominant axis 인지 확인
3. additive XOR family (60/90/105/150) phi_structure 정밀 분석 → 왜 90만 flat 인지

## Significance vs H_346

H_346 abstract 가 주장한 "state-강건" 은 본 bench로 정정될 부분이 있다:

- ✅ **state-강건** (single sys_state → 32-state 평균 부호 유지) — H_346 자체 측정으로 확정
- ❌ **rule-set 강건** — 본 bench로 부분 반증 (4 rules → 8 rules 부호 역전)

따라서 H_345/346 finding 은 "**state-averaged**, but **on the 4 Wolfram-canonical rules {110, 30, 105, 150}**" 로 scope 가 좁혀져야 한다. 본 bench 는 anima-side 적용 결과로서 그 scope 를 측정으로 확정.
