# BENCH #5 — SELF-CORRECTION-PROBE 🟢 PASS (현미경 자가점검)

> UNIVERSE H_340 🔴 → H_342 self-correction 패턴 (small-n artifact 자동 falsifier) 을 anima harness 에 inject 할 generic template + F-M4B-FIRE-3 적용 test.

## 1. 동기

UNIVERSE H_337 의 "4|n ⟺ rule30 dominant" 법칙이 n∈{4,6,8,10,12} 5/5 PASS 였으나, H_340 이 n∈{14,16,20} 으로 확장하면서 small-n artifact 임을 자기 정정 (🔴 FALSIFIED). H_342 는 다시 n∈{11,12,13,14} 로 정밀화하여 crossover 가 n=10~11 사이임을 2차 자기 정정. 이 정직한 자기 정정 패턴을 anima 의 모든 small-n PASS finding 에 일반 적용할 generic harness 가 필요.

## 2. 가설 (falsifiable)

**H1**: small-n PASS 의 자기 정정을 generic template 으로 추출 가능하고, 같은 template 가 (a) tautology (small-n artifact) 와 (b) genuine robust 를 정확히 구분한다.

**falsifier**: template 가 두 케이스 중 하나라도 잘못 판정.

## 3. 방법 (Mac-local, pure hexa, 0$)

- `template.hexa` — 5-tier verdict taxonomy (ROBUST / SMALL-N-ARTIFACT / INVERSE-ARTIFACT / AMBIGUOUS / ALL-FAIL) + analyzer (`analyze_probe_table`).
- `probe_f_m4b_fire_3.hexa` — F-M4B-FIRE-3 (router 분화 ≥ 2 distinct experts) sweep n_steps ∈ {5,10,20,50}.
  - case A (winner-take-all collapse model — small-n 만 우연히 ≥2 expert 잡고 large-n 에서 mono-expert) → SMALL-N-ARTIFACT 검출 기대.
  - case B (genuine cotrain diversity model — 실 H100 측정 PER_POS_EXPERT 패턴 충실) → ROBUST 기대.
- template 의 5 verdict code 는 사전에 self-test 5/5 round-trip.

## 4. 측정 (verbatim)

### Template self-test (5-case round-trip)

| case | passes vector | expected | got | ok |
|---|---|---:|---:|:---:|
| A robust    | [1,1,1,1] | 1 | 1 | ✓ |
| B small-n   | [1,0,0,0] | 2 | 2 | ✓ |
| C inverse   | [0,1,1,1] | 3 | 3 | ✓ |
| D ambiguous | [1,0,1,0] | 4 | 4 | ✓ |
| E all-fail  | [0,0,0,0] | 5 | 5 | ✓ |

5/5 — 모든 verdict code 가 정확히 round-trip 됨 (`template_selftest.log`).

### F-M4B-FIRE-3 application (case A vs B)

#### case A — winner-take-all collapse (simulated tautology)

| n_steps | distinct_experts | pass |
|---:|---:|:---:|
| 5  | 2 | ✓ |
| 10 | 1 | ✗ |
| 20 | 1 | ✗ |
| 50 | 1 | ✗ |

→ `verdict_code=2 SMALL-N-ARTIFACT (RED)` · pass_count=1/4

#### case B — genuine cotrain diversity (robust expectation)

| n_steps | distinct_experts | pass |
|---:|---:|:---:|
| 5  | 2 | ✓ |
| 10 | 2 | ✓ |
| 20 | 2 | ✓ |
| 50 | 2 | ✓ |

→ `verdict_code=1 ROBUST (GREEN)` · pass_count=4/4

## 5. Verdict

**🟢 PASS** — template hits 2/2.

- case A 는 SMALL-N-ARTIFACT 정확히 검출 (RED)
- case B 는 ROBUST 정확히 PASS (GREEN)
- → generic template 이 H_340 식 자기 정정 패턴을 임의의 PASS finding 에 적용 가능

## 6. 🪜 핵심 발견

```
H_340 self-correction (4|n law n≤12 한정) =
  generic predicate { passes : list<int> across n-sweep } 의 verdict_code=2 의 한 사례

→ template.verdict_code(passes) 에 적용 가능한 모든 anima finding 자동 falsifier 화
→ F-M4B-FIRE-3 가 H100 ckpt 로 n_steps 재측정 시 case A 형태로 판명되면 paper caveat 자동 트리거
→ small-n PASS 를 위장한 tautology 와 genuine robust 의 명확한 분리
```

## 7. 의미

- H_340 식 정직한 자기 정정이 ad-hoc 가 아니라 **재사용 가능한 harness** 로 추출됨
- 모든 anima H/F finding 이 small-n artifact 가능성을 자기 검증하는 표준 통과 게이트 후보
- F-M4B-FIRE-3 의 robust 여부는 case B simulation 으로 **시연 가능**, 진짜 검증은 H100 ckpt n-sweep 으로

## 8. Cross-link

| ref | 관계 |
|---|---|
| [H_340 4|n law verify](../../UNIVERSE/H_340_4n_law_verify.md) | small-n artifact 검출 패턴 원형 |
| [H_342 4|n crossover refine](../../UNIVERSE/H_342_4n_crossover_refine.md) | 2차 자기 정정 (crossover 정밀화) |
| [CORE/DECODER M4b](../../CORE/DECODER/DECODER.md) | F-M4B-FIRE-3 PASS @ n_steps=20 원본 측정 |

## 9. Anti-tautology

- template self-test 5/5 round-trip — verdict code 1~5 모두 사전 등록된 입력 패턴에서 정확히 도출
- case A/B 의 두 router 모델은 (a) winner-take-all (b) one-outlier-otherwise-uniform 으로 *명확히 다른 메커니즘* — 같은 passes 벡터를 만들 수 없음
- 결과가 (R/R), (R/S), (S/R), (S/S) 어느 조합으로도 떨어질 수 있었음 — 실측은 (S/R) = expected
- PASS 게이트 (`>=2 distinct experts`) 는 router 모델 *외부* 에 사전 등록 — moving the goalpost 불가

## 10. 다음

- (a) F-M4B-FIRE-3 실 H100 ckpt 로 n_steps ∈ {5,10,20,50} 재측정 — toy sim 을 진짜 router 로 대체 (case B 가설 검증)
- (b) `template.hexa` 를 다른 small-n PASS findings 에 적용 — F-V5MIT-* 시리즈, H_337 4|n law variant
- (c) 재사용 사례 ≥ 3 누적 시점에 `/stdlib promote BENCH/self_correction_probe/template.hexa` 로 hexa-lang stdlib 승격 (commons @D g61)

## 11. 재실행

```bash
hexa run BENCH/self_correction_probe/template.hexa             # self-test 5/5
hexa run BENCH/self_correction_probe/probe_f_m4b_fire_3.hexa   # case A/B 2/2
```

산출물:
- `template.hexa` — generic analyzer (reusable)
- `probe_f_m4b_fire_3.hexa` — F-M4B-FIRE-3 driver
- `template_selftest.log` — verbatim 5-case round-trip stdout
- `probe_f_m4b_fire_3.log` — verbatim case A/B stdout
- `result.json` — 구조화 SSOT
