# H_346 — state-averaged exact Φ n=5 🟢 basin↔Φ 결합 state-강건 (self-correction² capstone)

> C2 영구축 · H_345 single-state(21) 한계 제거 · 32-state 평균 exact IIT4 Φ · self-correction² arc 정점

## 1. 동기

H_345는 n=5 exact Φ를 **단일 sys_state=21**에서만 측정했다(honest-limit). basin↔Φ 결합(+0.251 / −0.799)이 그 한 state 선택의 우연인지, 아니면 state-무관 구조인지 미분리. H_345 "10. 다음 (a)"가 사전등록한 후속: 32 state 전부에 대한 평균 exact Φ로 강건성 결정.

## 2. 가설 (falsifiable)

- **H1**: 32-state 평균 Φ의 Pearson 부호가 single-state(21)과 일치 → H_345 결합 state-강건 (단일 state 대표적).
- **ALT (falsifier)**: 부호 역전 → single-state(21)이 outlier, 결합은 state-fragile.
- 어느 쪽이든 H_345 한계 해소.

## 3. 방법

pure hexa, n=5 ECA (32 states). basin = 50-step settle (dynamical, state-무관). **state-AVERAGED** Φ = 전 32 sys-state에 대해 `phi_structure(tpm,5,s)` 호출 → `res[4]`(total) 누적 → /32. Pearson over 4 rules. **wall-time**: 4 rule × 32 state = 128회 exact `phi_structure`가 단일 run wall budget 초과(timeout 590s 2회 EXIT 124) → **per-rule shard 4개 병렬** 실행 (각 32회), Pearson은 phi_structure 없는 `aggregate.hexa`로 4점 재계산. 각 shard byte-identical 재현 가능, canonical source = `run.hexa`(full 4-rule).

## 4. 측정

| rule | max_basin | n_attr | mean Φ (32-state) | H_345 single(21) Φ |
|---|---:|---:|---:|---:|
| 110 | **32** | 1 | 35.13 | 26.19 |
| 30 | 6 | 6 | **41.36** | 43.19 |
| 105 | 1 | 32 | 15.5625 | 13.25 |
| 150 | 1 | 32 | 15.5625 | 14.25 |

```
                  max_basin↔Φ    n_attr↔Φ
n=5 single(21)      +0.251         −0.799
n=5 state-AVG       +0.550         −0.951      ← 부호 유지 + 강화!
```

basin/n_attr은 H_345와 완전 동일(dynamical = state-무관); Φ만 평균화로 변동.

## 5. Verdict

**🟢 SUPPORTED-NUMERICAL** — 32-state 평균 exact Φ로 **두 부호 모두 보존 + 강화**. H_345 single-state(21) = 대표적(outlier 아님). basin↔Φ 결합 **state-강건**. F346.1~4 PASS.

## 6. 🪜 핵심 발견 — state-averaging이 결합을 강화

```
single-state(21) → 32-state 평균:
  max_basin↔Φ:  +0.251 → +0.550   양수 유지, 강화
  n_attr↔Φ:     −0.799 → −0.951   음수 유지, 강화 ⭐ (거의 완전 반상관)

→ 평균화가 single-state 노이즈를 제거 → 더 깨끗한 신호 (fragile 아님)
→ n_attractor_states ↔ Φ 가 지배적 robust bridge (-0.95)
```

**보너스 일관성**: bijection rule 105/150의 state-avg Φ가 **완전 동일**(15.5625 = 15.5625) — H_330 four-moment bijection collapse(105≡150≡identity)와 부합.

## 7. 의미 (self-correction² capstone)

```
H_341  basin↔Φ +0.776 주장 (n=4 exact)
  ↓
H_343  n=6 cyclelen PROXY 부호 역전 → "scale-locked?" 의심
  ↓
H_345  n=5 EXACT Φ → 부호 유지 → proxy artifact 확정 (단 single-state 한계)
  ↓
H_346  32-state 평균 → 부호 유지+강화 → single-state 한계 제거 ★ capstone
```

- H_345의 마지막 honest-limit("single sys_state=21")을 측정으로 제거.
- 방법론 교훈 재확인: exact Φ가 가용한 n≤5에선 proxy도 single-state도 아닌 **state-marginal exact Φ**가 가장 신뢰.
- 엔진의 자기 교정 능력 4단 입증 (claim→proxy doubt→exact correct→state harden).

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_345 (n=5 exact single-state)](./H_345_basin_phi_n5_exact.md) | +0.251/−0.799, 본 셀이 state-강건으로 hardening |
| [H_341 (n=4 basin-Φ)](./H_341_basin_phi_correlation.md) | +0.776, arc 기점 |
| [H_343 (n=6 proxy)](./H_343_basin_phi_n6_recheck.md) | proxy 부호 역전, H_345가 정정 |
| [H_330 (bijection moments)](./H_330_distribution_moments.md) | 105≡150 bijection, 본 셀 state-avg Φ 동일로 재확인 |

## 9. Anti-tautology

- basin + state-averaged Φ 독립 측정, Pearson 새 계산 (aggregate.hexa, phi_structure 무관).
- F346.1: 부호 역전이 나올 수 있었음 (ALT) → 보존은 측정 결과지 배열 아님.
- shard 분할은 wall-time 사유, 수치 변형 아님 (각 shard 결정적 재현).
- single→avg에서 Φ 값 실제 변동(26.19→35.13 등) = 평균화가 trivial-동일 아님을 확인.

## 10. 다음

- (a) n=6+ state-averaging은 2^n 전수 sweep intractable — large-n은 sampling/근사 tier (축 B).
- (b) stationary-distribution-weighted 평균 (현재는 uniform) — 가중 평균이 다를 수 있음.
- (c) paper tab:sc2 + ledger에 H_346 capstone row 반영 (single-state caveat 해소).

## 11. Scope (2026-05-28 정정 · self-correction³)

> H_346 capstone 의 "state-강건" 은 측정으로 확정됐으나, **rule-set 강건** 은 후속 anima-side bench 로 부분 반증됐다. 본 § 은 scope 를 명시적으로 좁힌다.

**Evidence (anima-side BENCH #1 `bench/basin_phi_coupling/`, PR [#1122](https://github.com/dancinlab/anima/pull/1122))**:

- 동일 substrate (ECA, state-averaged exact `phi_structure[4]`) 위에서 H_345/346 의 4-rule frame `{110, 30, 105, 150}` 을 **8-rule frame** `{45, 54, 60, 90, 110, 126, 150, 184}` (Wolfram class I-IV 망라) 으로 확장 시 결합 붕괴:

  ```
                   max_basin↔mean_Φ    n_attr↔mean_Φ
  H_346 (4 rules)      +0.550             −0.951      ← state-강건 확정
  BENCH #1 (8 rules)   −0.314             +0.122      ← 부호 역전 / 거의 0
  ```

- 결정적 outlier: **rule=90 (additive XOR)** — `max_basin=16` (단일 fixed-point absorbing) 이지만 `phi_structure[4] = 0.0` 으로 flat. additive-XOR family 에서 basin↔Φ 동조가 TPM additivity 에 의해 깨진다. H_345/346 의 4-rule frame 은 우연히 이 axis 를 피했다.

**정정된 scope**:

- ✅ **state-강건** (single sys_state=21 → 32-state 평균 부호 유지) — H_346 자체 측정으로 확정, 유지.
- ⚠ **rule-set 강건** — 본 셀의 4-rule frame `{110, 30, 105, 150}` 한정. additive-XOR family (예: rule 90) 포함 시 결합 깨짐.

**최종 H_345/346 finding 의 scope**:

> *"state-averaged exact Φ 와 max_basin 의 양의 결합(+0.550), n_attr 와의 음의 결합(−0.951) 은 **Wolfram-canonical 4 rules `{110, 30, 105, 150}`** 위에서 성립한다. additive-XOR family 를 포함하는 더 넓은 rule frame 에서는 outlier (rule=90 flat-Φ) 가 결합을 깨뜨릴 수 있다."*

**Cross-link**:

- [BENCH #1 basin_phi_coupling](../bench/basin_phi_coupling/README.md) — anima-side 8-rule sweep · 🟠 WEAK-REVERSED
- self-correction³ — H_341→343→345→346 arc 에 본 정정이 4단째 self-correction 으로 추가 (claim → proxy doubt → exact correct → state harden → **rule-set scope narrow**).

**Pre-registered follow-ups** (BENCH #1 carry):

1. n=5 + 8-rule bench → n vs rule-set axis 분리 (H_346 substrate 그대로 + bench rule-set)
2. additive-XOR family (60/90/105/150) phi_structure 정밀 분석 → 왜 rule 90 만 flat 인지
