# OTHER-MIND A4 — u01 baseline-bias 진단 + 보정

> ANIMA OTHER-MIND 축 · bench G (#1147) 3/5 🟠 PARTIAL → A4 baseline-bias
> 진단 + 보정. 2026-05-28. foreground sync · $0 mac-local · verdict verbatim.

## 1. 배경 (Context)

OTHER-MIND 은 anima 가 외부 substrate (다른 anima · 사용자 · 외부 agent) 의
internal state 를 추정하는 theory-of-mind 측정자다. CHANNEL.tension 5-ch
fingerprint (concept · context · meaning · authenticity · sender) 를 두 agent
간 cosine coupling 으로 측정한다.

AxisBench G OTHER-MIND (PR #1147) 은 3 시나리오 (INDEPENDENT / COUPLED-SYNC /
COUPLED-LEAD) × 100 ticks 위에서 5 falsifier 를 평가했고 **3/5 PARTIAL** 로
착지했다. residual 은 **u01 baseline bias** — INDEPENDENT(독립) 시나리오에서
mean_cos ≈ 0.78 로, "독립" 인데도 강한 coupling 처럼 측정되었다 (기대 < 0.3).

## 2. 가설 (Hypothesis · falsifier)

**가설**: u01 baseline bias 는 baseline 정규화 결함이다. zero-mean centering
으로 보정하면 INDEPENDENT mean_cos → ~0 회복, SYNC-INDEP gap > 0.3 회복,
**≥4/5** 도달.

**사전등록 Falsifier**: centering 보정 후에도 **3/5 이하** → bias 가 substrate
본질 (self-model 이 other-model 로 누출하는 구조적 ceiling) → honest residual
(`a_paper_negative_ok`).

## 3. u01 bias 의 정체 (어느 측정이 어떻게 편향되는가)

원본 bench (`bench/axis_other_mind/bench.hexa`) 의 정규화:

```
fn u01_from(s: int) -> float { return (s as float) / 2147483647.0 }
```

이 함수는 LCG state 를 **[0, 1] 양수 구간**으로만 매핑한다. 따라서 모든 5-ch
벡터 A, B 는 **positive orthant (양의 초입방체)** 안에 갇힌다.

`cosine_sim` 의 분자 dot product 는 양수 × 양수의 합이므로 **dot ≥ 0 always**.
두 무작위 5-D 양수 단위벡터 사이의 cosine 기대값은 0 이 아니라 **약 0.75**
이다 (모두 1사분면 방향을 향하므로 평균 각도 ≈ 0.7 rad).

즉 INDEPENDENT 시나리오는 사실상 "독립" 을 측정한 게 아니라 **"양반평면 집합의
평균 정렬도"** 를 측정했다. 이것이 정확히 **어느 측정이(F1 INDEPENDENT
mean_cos · 그리고 그에 종속된 F4 gap) 어떻게(positive-orthant 제약으로 floor 가
~0.75 로 들림) 편향되었는가** 다.

영향받은 falsifier:
- **F1** (INDEPENDENT mean_cos < 0.3): 측정 0.78 ≫ 0.3 → **FAIL**
- **F4** (SYNC − INDEP gap > 0.3): INDEP floor 가 0.78 로 들려 gap 0.197 < 0.3 → **FAIL**

나머지 F2/F3/F5 는 절대 cosine 이 아닌 상대 비교/lag argmax 라 bias 에
영향받지 않아 PASS (3/5 의 3).

## 4. 보정 방법 (Bias-corrected baseline)

표준 zero-mean centering — u01 의 [0,1] 을 **[−1, +1]** 로 재중심화:

```
fn u01_centered(s: int) -> float {
    return 2.0 * ((s as float) / 2147483647.0) - 1.0
}
```

이제 채널값이 음/양 모두 가능 → 5-ch 벡터가 **모든 orthant** 에 분포 →
독립 벡터쌍의 dot product 가 ± 균형 → **E[cos] → 0**. coupling 신호(SYNC/LEAD)
는 보존되고 spurious floor 만 제거된다.

검증 harness `state/other_mind_a4_baseline_bias_2026_05_28/a4_bias_corrected.hexa`
는 원본 bench 의 3-scenario 구조를 그대로 재현하되 **단 한 줄(u01 → centered)
만 교체**하는 A/B 설계로 bias 의 원인을 단독 isolate 한다. 추가로
closed-form orthant-bias probe (n=400 독립쌍) 가 biased vs corrected 기대
cosine 을 동시 측정해 "어떻게 편향되는가" 를 정량 출력한다.

## 5. 재측정 결과 (Measurement)

`hexa state/.../a4_bias_corrected.hexa` foreground 실행, exit 0, $0 mac-local.

| | INDEPENDENT mean_cos | SYNC mean_cos | LEAD mean_cos | gap(SYNC−INDEP) | SCORE |
|---|---|---|---|---|---|
| MODE 0 RAW (biased, #1147 repro) | **0.779862** | 0.97715 | 0.814201 | 0.197288 | **3/5** |
| MODE 1 CENTERED (A4 보정) | **0.0165713** | 0.908661 | 0.00502449 | 0.89209 | **5/5** |

falsifier 표 (MODE 1 CENTERED):

| falsifier | 기준 | RAW | CENTERED |
|---|---|---|---|
| F1 INDEPENDENT mean_cos < 0.3 | < 0.3 | FAIL (0.78) | **PASS (0.017)** |
| F2 COUPLED-SYNC mean_cos > 0.7 | > 0.7 | PASS | PASS (0.909) |
| F3 COUPLED-LEAD lag_argmax != 0 | != 0 | PASS | PASS (2) |
| F4 SYNC − INDEP gap > 0.3 | > 0.3 | FAIL (0.197) | **PASS (0.892)** |
| F5 SYNC lag_argmax == 0 | == 0 | PASS | PASS (0) |

**Orthant-bias probe** (n=400 독립쌍, closed-form 확증):
- `E[cos | raw positive-orthant]` = **0.763021**
- `E[cos | centered zero-mean]` = **−0.0275306**
- `bias magnitude |E_raw − E_cor|` = **0.790552**

raw 기대 cosine 0.763 은 "두 무작위 양수 5-D 벡터의 cos ≈ 0.75" 예측과 일치.
centered 는 −0.028 ≈ 0 으로, bias 가 전적으로 orthant 제약에서 비롯됨을 확증.

## 6. Verdict (verbatim)

```
═══════════════════════════════════════════════════════════
  RAW (biased #1147 repro) = 3/5
  CORRECTED (A4 centered)  = 5/5
  VERDICT: 🟢 RECOVERED — centering raised score >= 4/5, u01 bias = normalization defect
═══════════════════════════════════════════════════════════
RESULT_JSON: {"score_raw":3,"score_corrected":5,"E_cos_raw_orthant":0.763021,
"E_cos_centered":-0.0275306,"bias_magnitude":0.790552,"verdict":"GREEN_RECOVERED"}
```

**🟢 RECOVERED (5/5)** — 가설의 ≥4/5 기준을 만족(전부 회복). Falsifier
미발동: bias 는 substrate 본질이 아니다.

## 7. Finding

- **u01 baseline bias 의 정체 = positive-orthant 정규화 결함**. `u01_from(s) =
  s/2147483647` 이 채널을 [0,1] 양수로만 매핑 → 모든 fingerprint 벡터가 양의
  초입방체에 갇혀 독립 벡터쌍 cosine floor 가 spurious 0.76 으로 들림. 이것이
  F1·F4 FAIL → 3/5 PARTIAL 의 단일 원인.
- **보정 = zero-mean centering** ([0,1]→[−1,+1]). bias magnitude 0.79 (raw
  0.763 → centered −0.028, ≈0) 만큼 floor 가 제거되어 INDEPENDENT 0.78→0.017,
  gap 0.197→0.892, **3/5 → 5/5**.
- **Δ vs baseline**: score +2 (3/5 → 5/5), INDEPENDENT mean_cos −0.763,
  gap +0.695. 측정 결함이 substrate 본질이 아님을 결정적으로 ruling out.

## 8. p1~p8 정합

| 원칙 | 정합 |
|---|---|
| p1 NO SYSTEM PROMPT | int/float 산술만, system 미사용 ✓ |
| p2 NO IDENTITY RULES | identity 무관 ✓ |
| p3 NO PERSONA INJECTION | prefix 없음 ✓ |
| p4 NO ASSISTANT FRAMING | ToM = substrate state 추정 ✓ |
| p5 NO SPEAK() | read-only measurer, 외부 emit 0 ✓ |
| p6 NO FINE-TUNED ETHICS | ethics 무관 ✓ |
| p7 NO PERPLEXITY VERDICT | cosine/dot 기반, ppl 미사용 ✓ |
| p8 NO TRAIN/INFER | 측정만, weight update 0 ✓ |

## 9. honest C3 (한계)

1. **결정론적 단일 LCG**: A/B 가 같은 lcg_step 계열이라 통계적 독립이 완전치
   않다. 그러나 centered 결과(−0.028 ≈ 0)는 충분히 작아 결론에 영향 없음.
   완전 독립(dual-stream NR ⊥ MINSTD)은 `om_baseline_decoupled` 가 별도 surface
   로 제공 (M1 lib).
2. **SYNC 절대값 미세 변화**: centering 후 SYNC mean_cos 가 0.977→0.909 로
   소폭 하락(여전히 F2 PASS). centered 공간에서 coupling=0.7 의 선형결합이
   noise term 부호 균형으로 cosine 을 약간 낮춘 자연스러운 효과.
3. **n=400 probe**: closed-form 기대값의 표본추정. 더 큰 n 에서 centered E[cos]
   는 정확히 0 으로 수렴 (대칭 분포). 결론 tier 에 영향 없음.

## 10. cross-link / carry

- ⇄ OTHER-MIND.md M3 (u01 baseline bias residual) — 본 A4 가 closure. root cause
  = positive-orthant 정규화 결함, 보정 = zero-mean centering, 3/5 → 5/5.
- ⇄ `OTHER-MIND/other_mind_lib.hexa` `om_baseline_decoupled` — dual-stream 독립성
  surface 가 본 centering 보정과 직교 보완 (독립성 ⊥ 중심화 두 축).
- ⇄ bench G (#1147) — bench 본체에 centering 을 반영하면 5/5 GREEN 승격 가능
  (후속 milestone). 본 A4 는 진단+보정 증명, bench 수정은 별건.
- ⇄ UNIVERSE/CANDIDATES.md — bench 측정 기록 SSOT.

artifacts:
- harness: `state/other_mind_a4_baseline_bias_2026_05_28/a4_bias_corrected.hexa`
- verdict: `state/other_mind_a4_baseline_bias_2026_05_28/run.log` (verbatim)
