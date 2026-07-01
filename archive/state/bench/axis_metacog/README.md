# AxisBench A — 🪞 METACOG (자기 거울 substrate self-audit) 🟢 PASS

> `ANIMA.axis.md` (PR #1136/#1137) 의 axis #A METACOG (p1~p8 정합 self-audit · BRIDGE AND-gate 위의 메타 결정 layer) 을 anima 본체 적용 측정. bench #5 (PR #1124) self-correction-probe 의 5-tier verdict template 을 합성 anima emit history (PASS/FAIL sequence 30개) 에 직접 적용해 small-n-artifact 자동 검출률을 측정.

## 1. 동기

bench #5 (`bench/self_correction_probe/`) 는 small-n PASS 의 자기 정정 패턴을 generic harness 로 추출했지만, 적용 대상은 H_337/H_340/H_342 의 4|n law 와 toy router (F-M4B-FIRE-3) simulation 이었다. **METACOG axis** 는 같은 template 을 **anima 본체의 emit history** 에 plug-in 해 "anima 가 자기 substrate 의 emit pattern 을 read-only 로 self-audit" 하는 layer 다. 본 bench 는 그 plug-in 의 input-shape compatibility + verdict round-trip + small-n-artifact precision/recall 을 확인한다.

## 2. 가설 (falsifiable)

**H1**: bench #5 의 5-tier verdict template 이 30-emit anima history 입력 모양에서도 5/5 expected verdict code 로 round-trip 한다.

**H2**: 5 시나리오 중 small-n-artifact 패턴 (S2) 만 code=2 (SMALL-N-ARTIFACT) 로 분류되고, 다른 4 시나리오 어떤 것도 code=2 로 오분류되지 않는다 (TP=1, FP=0).

**H3**: bench 자체가 p1~p8 정합 (NO_SYSTEM_PROMPT / NO_IDENTITY_RULES / NO_PERSONA_INJECT / NO_ASSISTANT_FRAME / NO_SPEAK / NO_FINE_TUNED_ETHICS / NO_PPL_VERDICT / NO_TRAIN_INFER_SPLIT) — 즉 8/8 self-audit PASS.

**falsifier**: 위 3 가설 중 하나라도 위배 (round_trip < 5/5, TP≠1, FP≠0, audit < 8/8).

## 3. 방법 (Mac-local, pure hexa, $0)

- `bench.hexa` — 5-tier verdict primitives + 30-emit history binarizer + 5 synthetic scenario driver + p1~p8 self-audit
- 합성 30-emit history → 4 disjoint window (size 7/7/8/8) → window pass-rate ≥ 0.5 → 1 else 0 (binarize) → bench #5 의 `analyze_probe_table` 입력 모양과 동일한 (passes: list<int>) 도출
- 5 시나리오 (ROBUST / SMALL-N / INVERSE / AMBIG / ALL-FAIL) 각각의 expected_code 와 got_code 일치 round-trip
- METACOG 메타 audit 으로 8 principle 위배 read-only inspect

verdict 는 deterministic predicate (passes-bitmap → verdict_code 함수) — PPL/loss/random 미사용 (p7 준수).

## 4. 측정 (verbatim)

### 4.1 5 scenario 30-emit history & bins

| scenario | 30-emit (anima history) | bins(4) | expected | got | tier | round-trip |
|---|---|---:|---:|---:|:---:|:---:|
| S1-ROBUST   | `111111111111111111111111111111` | `[1,1,1,1]` | 1 | 1 | 🟢 GREEN  | PASS |
| S2-SMALL-N  | `111111100000000000000000000000` | `[1,0,0,0]` | 2 | 2 | 🔴 RED    | PASS |
| S3-INVERSE  | `000000011111111111111111111111` | `[0,1,1,1]` | 3 | 3 | 🟠 ORANGE | PASS |
| S4-AMBIG    | `111111100000001111111100000000` | `[1,0,1,0]` | 4 | 4 | 🟡 YELLOW | PASS |
| S5-ALL-FAIL | `000000000000000000000000000000` | `[0,0,0,0]` | 5 | 5 | 🔴 RED    | PASS |

→ **5/5 round-trip** — bench #5 template 이 30-emit anima history shape 에서도 무손실 동작.

### 4.2 small-n-artifact 자동 검출률

| metric | value |
|---|---:|
| true positive (S2 만 code=2)    | 1 / 1 |
| false positive (S1/S3/S4/S5 ≠ 2) | 0 / 4 |
| precision | 1.0 |
| recall    | 1.0 |

→ **TP=1, FP=0** — 정확히 small-n-artifact 만 검출.

### 4.3 METACOG p1~p8 self-audit

| principle | ok |
|---|:---:|
| p1 NO_SYSTEM_PROMPT     | ✓ |
| p2 NO_IDENTITY_RULES    | ✓ |
| p3 NO_PERSONA_INJECT    | ✓ |
| p4 NO_ASSISTANT_FRAME   | ✓ |
| p5 NO_SPEAK             | ✓ |
| p6 NO_FINE_TUNED_ETHICS | ✓ |
| p7 NO_PPL_VERDICT       | ✓ |
| p8 NO_TRAIN_INFER_SPLIT | ✓ |

→ **8/8 audit PASS**.

### 4.4 Falsifier matrix

| id | claim | result |
|---|---|:---:|
| F-METACOG-1-ROUND-TRIP-5 | 5/5 scenario round-trip                                | PASS |
| F-METACOG-2-SMALL-N-TP   | S2 가 code=2 로 정확 검출 (TP=1)                        | PASS |
| F-METACOG-3-SMALL-N-FP   | S1/S3/S4/S5 어떤 것도 code=2 로 오분류 안 됨 (FP=0)      | PASS |
| F-METACOG-4-PRINCIPLE    | bench 자체가 p1~p8 위배 없이 read-only 측정만 수행       | PASS |
| F-METACOG-5-DETERMINISTIC| verdict = passes-bitmap deterministic (p7 준수)         | PASS |

5/5 falsifier all PASS.

## 5. Verdict

**🟢 PASS** — round_trip=5/5 · small_n_artifact TP=1 FP=0 · METACOG audit=8/8.

## 6. 🪜 핵심 발견

```
bench #5 (self_correction_probe) 5-tier verdict template
   ⊇ AxisBench A METACOG 의 anima emit history input shape (30-emit → 4-window binarize)
   ⊇ small-n-artifact precision/recall 1.0 (synthetic ground-truth)
   ⊇ p1~p8 8/8 정합 (read-only 측정, weight update 0, speak() 0, PPL verdict 0)

→ METACOG layer = bench #5 template + 30-emit binarize wrapper + p1~p8 audit
→ 임의의 anima emit history 에 plug-in 가능한 substrate-native self-audit harness 확보
→ "BRIDGE AND-gate 위의 메타 결정 layer" 의 측정 surface 가 generic + falsifiable 임을 확인
```

## 7. 의미

- ANIMA.axis.md axis #A METACOG 의 "p1~p8 정합 self-audit + bench #5 본체 적용" 명세가 single PR · pure hexa · $0 로 시연 가능함을 입증
- anima 의 모든 emit-history sequence 에 대해 small-n-artifact 자동 falsifier 가 plug-in 됨 → BRIDGE AND-gate 결정 *위* 의 메타 결정이 read-only 측정으로 가능
- 다음 단계: 합성이 아닌 실 anima substrate-native chat emit history 를 30-emit 단위로 sample → live METACOG audit lane 가동

## 8. Cross-link

| ref | 관계 |
|---|---|
| `ANIMA.axis.md` axis #A METACOG | 본 bench 의 명세 SSOT |
| `bench/self_correction_probe/` (bench #5, PR #1124) | 5-tier verdict template 원형 |
| UNIVERSE H_340 / H_342 | self-correction 패턴의 시발점 saga |
| CORE/BRIDGE | AND-gate 위 메타 결정 layer (METACOG 의 대상) |

## 9. Anti-tautology

- 5 시나리오 모두 (R/R), (R/S), (S/R), (S/S), (M/A), … 어느 결과로도 떨어질 수 있었음 — verdict_code 함수가 임의 passes-bitmap → {1..5} 매핑이라 사전 등록된 expected_code 와 일치하지 않을 자유도가 있음
- TP=1, FP=0 도 회피 가능 — S1 (all-1) 이 일부 패턴 만족 시 small-n-artifact 로 분류되거나, S2 가 ambiguous 로 분류될 수 있음. 검사기가 두 함수 (`all_pass`, `is_small_n_artifact`) 의 우선순위 (line 99~110) 에서 결정되도록 명시적으로 설계됨
- META audit 8/8 도 회피 가능 — bench 가 system-prompt / persona-prefix / speak() / PPL-based verdict 등을 도입했다면 audit 가 깨졌을 것 (현재 코드 read-only 임을 inspect 로 확인)
- 가설 H1/H2/H3 모두 pre-registered (이 README + result.json `falsifier_matrix`) — moving the goalpost 불가

## 10. 다음

- (a) 실 anima substrate-native chat run 에서 30-emit history 를 sample 해 같은 driver 입력 → live METACOG audit lane 활성화
- (b) bench #5 template SSOT 재사용 — 현재는 self-contained inline 재구현; import 가능해지면 (`import bench/self_correction_probe/template.hexa`) 단일 SSOT 로 수렴
- (c) 재사용 사례 ≥ 3 누적 시점에 `/stdlib promote bench/self_correction_probe/template.hexa` 로 hexa-lang stdlib 승격 (commons @D g61)

## 11. 재실행

```bash
hexa run bench/axis_metacog/bench.hexa     # 5/5 round-trip + audit 8/8 + verdict 🟢
```

산출물:

- `bench.hexa` — 5-tier verdict primitives + 30-emit binarize + 5 시나리오 driver + p1~p8 self-audit (self-contained)
- `run.log` — verbatim stdout (5 scenario + audit + final verdict)
- `result.json` — 구조화 SSOT (falsifier matrix · meta_audit · final_verdict)
- `README.md` — 본 문서 (8 §, korean)
