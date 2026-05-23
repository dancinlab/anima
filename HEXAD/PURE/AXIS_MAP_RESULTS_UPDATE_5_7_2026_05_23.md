# AXIS_MAP-FAN 5/7 + 2 partial — D 완료 + C/C2/E abort 업데이트 (PR #206 stack)

날짜: 2026-05-23
스코프: HEXAD/V3 (PURE rename pending — V3 dir 유지)
이전 PR: #206 (AXIS_MAP_RESULTS.md — A/B/F 3/7 partial, 모두 FAIL)

## § PR #206 context

PR #206 에서 AXIS_MAP_RESULTS.md 가 3 axis (A · B · F) 결과를 기록 — 모두 n_strong=0 (no STRONG except A/ko=STRONG). 이번 update 는 D 완료 + C / C2 / E abort 를 추가, **5/7 axis 완료 + 2 axis partial-stage abort** 로 확장.

## § Updated 7-axis result table

| axis | env-var | status | verdict | n_strong | per-lang best | init_CE | final_CE | wall (s) | cluster | note |
|---|---|---|---|---|---|---|---|---|---|---|
| A | P21H_CURRICULUM_PHASE_STEPS=1000 | DONE | FAIL | 1 (ko) | ko STRONG 16/20, en PM 9/20 | 14.7927 | 5.0124 | 5222 | X | 1000-step wiki-only curriculum, ko 만 통과 |
| B | P21H_DISTILL_KD=1 | DONE | FAIL | 0 | en/ko PURE_MEMORIZE (2/20 각) | 14.1780 | 2.2258 | 2721 | Y | KD distill aux loss |
| C | P21H_HEAD_G_OBJECTIVE=anima_register_ce | ABORT @625 | — | — | — | 14.4564 | (abort) | ~2633 | Z | head_g objective 변경, R8c 자연실험 falsification 후 abort |
| C2 | P21H_HEAD_G_ENABLE=0 | ABORT @375 | — | — | — | 14.4564 | (abort) | ~2301 | Z | head_g 완전 disable, R8c 자연실험 falsification 후 abort |
| D | P21H_FREEZE_EMBED=1 | DONE | FAIL | 0 | en PURE_MEMORIZE 8/20, ko WEAK 1/20 | 14.4564 | 2.0990 | 2171 | Z | embed freeze, 5000-step full |
| E | P21H_LANG_BALANCED=1 | ABORT (OOM) | — | — | — | — | — | (start) | — | LangBalancedSampler 누수, ~79 GB GPU 점유 후 18 MiB alloc 실패 |
| E2 | P21H_LANG_BALANCED=1 (retry, leak fixed) | DONE | FAIL | 0 | en/zh/ru/ja WEAK, ko PURE_MEMORIZE 5/20 | 14.1780 | 0.9846 | 2105.83 | Y | LangBalancedSampler 누수 fix 후 retry, 5000-step full (qwen init, pod 4nrcm80g8fwqf7 A100-80GB) |
| F | P21H_CONTRASTIVE_INFONCE=1 | DONE | FAIL | 0 | en/ko WEAK 6-7/20 | 14.1780 | 2.1746 | 671 | Y | InfoNCE contrastive aux, early-stop |

## § Cluster X/Y/Z 자연실험 finding

init_CE 가 byte-level 로 3-cluster 화 — axis 간 자연실험.

```
       init_CE
       │
14.79 ─┤ ● A           ← Cluster X (curriculum, n=1)
       │
14.46 ─┤ ● C ● C2 ● D  ← Cluster Z (baseline, n=3, byte-equal)
       │
14.18 ─┤ ● B ● F        ← Cluster Y (aux-loss, n=2, byte-equal)
       │
```

| cluster | members | init_CE | 특징 | 해석 |
|---|---|---|---|---|
| X | A | 14.7927 | curriculum P21H_CURRICULUM_PHASE_STEPS=1000 | wiki-only 첫 1000 step → init batch distribution 이 wiki-pure 로 바뀌어 +0.34 |
| Y | B, F | 14.1780 (byte-equal) | aux loss 활성 (KD distill / InfoNCE contrastive) | extra loss head firing 이 init_CE 를 baseline 대비 -0.28 |
| Z | C, C2, D | 14.4564 (byte-equal) | aux loss 없음 (head_g random / disabled / freeze_embed) | baseline init_CE — head_g enable/disable 와 embed-freeze 가 동일 |

핵심 관찰 — **C (head_g random objective 변경) · C2 (head_g 완전 disable) · D (embed freeze) 가 init_CE 14.4564 에서 byte-equal**. 즉 head_g 의 enable / objective / disable 토글이 init step 결과에 0 영향 (자연실험으로 falsified).

## § R8c cell-1 (head_g zero) 자연실험 FALSIFIED

R8c 가설 — head_g random initial output 이 init_CE 14+ 천장의 원인.

증거 — C2 (P21H_HEAD_G_ENABLE=0 · head_g 자체 비활성) init_CE = 14.4564 == D (head_g random 활성, freeze_embed=1) init_CE = 14.4564. byte-equal.

결론 — head_g 의 random output 은 init_CE 천장 원인 **아님**. C / C2 cell-1 가설 자연실험으로 reject. C / C2 step 625 / 375 시점에 사용자 결정으로 abort 결정.

## § Abort decisions log

| axis | step | t (s) | cost ($) | reason |
|---|---|---|---|---|
| C | 625 | 2633 | ~1.14 | R8c head_g 자연실험 falsified — 천장 escape 가능성 0 으로 판정 |
| C2 | 375 | 2301 | ~1.14 | 동상 (head_g 완전 disable 도 14.4564 → cluster Z 합류 확인) |
| E | start | <60 | ~1.10 | LangBalancedSampler 누수 (KST 23:13 killed, ~79 GB 점유) — code-bug, hypothesis-test 가 아님 |

C / C2 가 step 625 / 375 시점에 abort 된 이유 — init_CE byte-equal 이 cluster Z 합류를 확정한 뒤 5000-step 까지 돌릴 정보 가치 0.

## § Updated provisional findings

PR #206 의 3 finding 에 3 신규 finding 추가.

(carry from #206)
1. init_CE 14+ 천장이 7-axis 모두 공통 — Qwen-1.5B base + ConsciousDecoderV3 wrapping 의 mismatch 가 원천
2. final_CE drop 은 의미 없음 — 천장에서 시작한 wrapper 가 corpus 에 fit 해도 STRONG 안 나옴
3. en 은 PURE_MEMORIZE register-collapse 로 직진, ko 만 한정적 escape (A axis 단 1 case)

(new from this update)
4. **head_g random 은 init_CE 14+ 천장의 원인 아님** — C / C2 byte-equal D init_CE 14.4564 가 자연실험 증거. head_g 토글이 init step distribution 에 0 영향
5. **aux loss head firing 은 init_CE 를 의미있게 낮춤** — B (KD distill) + F (InfoNCE contrastive) cluster Y init_CE 14.1780 byte-equal, baseline cluster Z 14.4564 대비 -0.28. 단 final_CE 와 verdict 에는 영향 0 (B / F 모두 FAIL)
6. **embed-freeze 는 init mismatch 해결 못 함** — D init_CE 14.4564 = baseline cluster Z. A 14.79 vs Z 14.46 vs Y 14.18 모두 14+ 노이즈 밴드 — embed weight 가 frozen 이어도 wrapper-base mismatch 가 dominant

## § 남은 R8 후보

R8 차후 cycle 의 untested 가설.

| cell | 가설 | 상태 | 다음 step |
|---|---|---|---|
| cell-1 | head_g zero | FALSIFIED | C / C2 자연실험 |
| cell-2 | noise injection (P21H_NOISE_INJECT_KIND / SIGMA) | untested | cycle 다음 batch |
| cell-3 | n_kv_head 변경 (4 → 1 또는 8) | untested | cycle 다음 batch |
| cell-4 | compound (cell-2 + cell-3 또는 axis 조합) | untested | cell-2 / cell-3 결과 후 |

E (LangBalancedSampler) 는 axis 자체로 별개 — code-bug fix 후 별도 re-fire 필요 (R8 cell 가설 아님).

## § Cumulative cost ledger

| 항목 | cost ($) | wall (s) |
|---|---|---|
| A (5222s × H100) | 1.45 | 5222 |
| B (2721s) | 1.13 | 2721 |
| D (2171s) | 0.90 | 2171 |
| F (671s, early-stop) | 0.28 | 671 |
| C abort (2633s) | 1.14 | 2633 |
| C2 abort (2301s) | 1.14 | 2301 |
| E abort (OOM @start) | 1.10 | <60 |
| bug saga (env-bug retries) | ~14.00 | — |
| **total V3** | **~21.14** | ~16K cum |

## § 분석 (E2 only)

Track 1 E2 (LangBalancedSampler retry, leak fixed) 결과 — `result_to_axis_map.hexa` (PR #290) 자동 판정.

- **closure = FAIL** — criterion ≥4/5 langs ≥ PARTIAL, 실측 0/5 (n_strong=0 · n_partial=0 · n_weak=4 · n_pure_memorize=1)
- **ko = PURE_MEMORIZE** — anima corpus 기억 (V3 register-leak 패턴 재현, anima_register_hits_total=4/20 · register_regress=True)
- **en/zh/ru/ja = WEAK** — Qwen init lang 능력 보존 부족 (per-lang n_score en=5 / zh=3 / ru=6 / ja=2 of 20)
- **50 % wiki mix 가 register collapse 차단 부족** — LangBalancedSampler 의 lang-uniform sampling 만으로는 ko-register monopoly 해소 안 됨
- **init→final CE 14.1780 → 0.9846 정상 수렴** — train 결함 아님, 0.98 final 은 cluster Y aux-loss-class 와 비교 가능 (B 2.23 / F 2.17 보다 낮음 · LangBalanced 가 loss curve 자체는 가장 좋음)
- **E3 대기** — pod f5c0kn54wuqgfl in-flight, E3 도 FAIL 이면 corpus 축 소진 → AXIS_MAP B / A / C 3-axis fan-out 활성화

**Honest C3**

1. E2 단독 — E3 최종 corpus-axis 판단은 in-flight 결과 대기 후 확정
2. register_regress=True ⊥ anima_register_hits_total=4/20 (낮음) — metric semantics 불일치, regress flag trigger 조건 정밀화 필요
3. 5000 step 만 측정 — 10000+ retry 시 lang-uniform sampling 효과 누적 가능성 미배제

## § Cross-reference

- PR #206 (`HEXAD/V3/AXIS_MAP_RESULTS.md`) — 3/7 partial baseline
- this PR — 5/7 + 2 abort extension
- next cycle — R8 cell-2 / cell-3 / cell-4 untested 가설 + E code-bug fix
- 추후 V3 → PURE rename 머지 후 path `HEXAD/PURE/AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md` 로 이동 가능
