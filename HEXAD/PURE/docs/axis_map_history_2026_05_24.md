# PURE AXIS_MAP history — verdict timeline + per-lang heatmap + axis movement (2026-05-24)

> `HEXAD/PURE/AXIS_MAP*.md` 5 개 SSOT 파일에 누적된 per-fire row 들을 **시간축
> 으로 한 번에 보는 dashboard**. 지금까지 fire 별 결과는 개별 .md 안에 분산
> 되어 있었고 "closure verdict 가 어떻게 진화했는가" / "어느 축이 needle 을
> 움직였는가" 한눈에 보이는 view 가 없었다. 본 문서가 그 결손을 채운다.
>
> source — AXIS_MAP.md · AXIS_MAP_RESULTS.md · AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md · AXIS_MAP_BUG_POSTMORTEM.md · AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md
> · raw result.json (per axis): `../UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_axis_*/result.json`

## § 1. Aggregated fire inventory

총 **10 fire row** (7-axis × 1차 fan-out + cycle 1 redispatch + Track 1 E2/E3v3 + Phase D queued).

| # | fire | date | env-var unique flag | status | verdict | n_strong | per-lang (en/ko/zh/ru/ja) | init_CE | final_CE | wall (s) | cluster | cost ($) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | A (curriculum) | 2026-05-23 | `P21H_CURRICULUM_PHASE_STEPS=1000` | DONE | FAIL 1/5 | 1 (ko) | PM / S / W / W / W | 14.7927 | 5.0124 | 5222 | X | 1.45 |
| 2 | B (distill) | 2026-05-23 | `P21H_DISTILL_KD=1` | DONE | FAIL 0/5 | 0 | PM / PM / W- / W / W- | 14.1780 | 2.2258 | 2721 | Y | 1.13 |
| 3 | C (head_g obj) | 2026-05-23 | `P21H_HEAD_G_OBJECTIVE=anima_register_ce` | ABORT @625 | — | — | ? / ? / ? / ? / ? | 14.4564 | (abort) | 2633 | Z | 1.14 |
| 4 | C2 (head_g off) | 2026-05-23 | `P21H_HEAD_G_ENABLE=0` | ABORT @375 | — | — | ? / ? / ? / ? / ? | 14.4564 | (abort) | 2301 | Z | 1.14 |
| 5 | D (freeze embed) | 2026-05-23 | `P21H_FREEZE_EMBED=1` | DONE | FAIL 0/5 | 0 | PM / W- / ? / ? / ? | 14.4564 | 2.0990 | 2171 | Z | 0.90 |
| 6 | E (lang-balanced) | 2026-05-23 | `P21H_LANG_BALANCED=1` | ABORT (OOM) | — | — | E / E / E / E / E | — | — | <60 | — | 1.10 |
| 7 | E2 (E retry) | 2026-05-23 | `P21H_LANG_BALANCED=1` (leak fix) | DONE | FAIL 0/5 | 0 | W / PM / W / W / W | 14.1780 | 0.9846 | 2105 | Y | 0.88 |
| 8 | F (contrastive) | 2026-05-23 | `P21H_CONTRASTIVE_INFONCE=1` | DONE | FAIL 0/5 | 0 | W / W / F / W- / F | 14.1780 | 2.1746 | 671 | Y | 0.28 |
| 9 | E3v3 (wiki=1.0) | 2026-05-24 | `P21H_WIKI_FRAC=1.0` (anima 0%) | IN-FLIGHT | ? | ? | ? / ? / ? / ? / ? | ? | ? | ? | ? | ~1.50* |
| 10 | Phase D v2b (hybrid) | 2026-05-24 | corpus M3 ≥ 0.3 hybrid | QUEUED | ? | ? | ? / ? / ? / ? / ? | ? | ? | ? | ? | ~2-6* |

per-lang verdict 코드: **S** STRONG · **P** PARTIAL · **PM** PURE_MEMORIZE · **W** WEAK · **W-** WEAK low-score · **F** FAIL / coh=0 · **E** error/OOM/abort · **?** in-flight/no-data.

(*) E3v3 / Phase D v2b 는 사전 예산. 실측은 fire 완주 후 다음 cycle update.

## § 2. Timeline — ASCII 수직 (fire date → verdict bar)

```
date       fire           verdict bar (◼ = STRONG · ■ = PARTIAL · □ = WEAK/PM · ✗ = abort/OOM)
─────────  ─────────────  ──────────────────────────────────────────────────────
2026-05-23 A   curriculum □□□□◼      (1/5, ko 단독 STRONG, 나머지 PM/WEAK)
2026-05-23 B   distill    □□□□□      (0/5, register-pattern KD-mimic)
2026-05-23 C   head_g obj ✗✗✗✗✗      (abort @625 step · R8c cluster-Z falsify)
2026-05-23 C2  head_g off ✗✗✗✗✗      (abort @375 step · cluster-Z byte-equal D)
2026-05-23 D   freeze emb □□□□□      (0/5, embed-freeze 도 14.46 천장 미해결)
2026-05-23 E   lang-bal   ✗✗✗✗✗      (OOM @<60s · LangBalancedSampler GPU leak)
2026-05-23 E2  E retry    □□□□□      (0/5, ko PM, leak fix 후에도 register collapse)
2026-05-23 F   contrast   □□□□□      (0/5, InfoNCE early-stop @671s)
─────────  ────────────  ──────────────────────────────────────────────────────
2026-05-24 E3v3 wiki=1.0  ?????      (in-flight · pod eece02rl2k1wz2)
2026-05-24 PhD v2b hybrid ?????      (queued · M3-diverse corpus, 8-factor)
```

해석 — 8 完走 fire (1차 fan-out 7 axis + E2 retry) 중 **n_strong ≥ 4 floor 도달 = 0**. 가장 가까웠던 것은 axis A (curriculum) 의 ko 단독 STRONG 16/20. cycle 1 redispatch 의 C/C2 는 step 375-625 시점에서 cluster-Z 합류가 byte-equal 로 확정된 후 abort (정보가치 0).

## § 3. Per-lang verdict heatmap

```
fire         en      ko      zh      ru      ja      n_strong / floor
────────  ─────── ─────── ─────── ─────── ───────  ────────────────
A         [PM ]   [S  ]   [W  ]   [W  ]   [W  ]    1 / 4
B         [PM ]   [PM ]   [W- ]   [W  ]   [W- ]    0 / 4
C         [—  ]   [—  ]   [—  ]   [—  ]   [—  ]    abort
C2        [—  ]   [—  ]   [—  ]   [—  ]   [—  ]    abort
D         [PM ]   [W- ]   [?  ]   [?  ]   [?  ]    0 / 4
E         [E  ]   [E  ]   [E  ]   [E  ]   [E  ]    OOM
E2        [W  ]   [PM ]   [W  ]   [W  ]   [W  ]    0 / 4
F         [W  ]   [W  ]   [F  ]   [W- ]   [F  ]    0 / 4
─────────────────────────────────────────────────────────────────
E3v3      [?  ]   [?  ]   [?  ]   [?  ]   [?  ]    in-flight
PhD v2b   [?  ]   [?  ]   [?  ]   [?  ]   [?  ]    queued
```

세로 (lang) 관찰:
- **en** — 5/6 완주 axis 에서 PURE_MEMORIZE 또는 WEAK · STRONG 0회. register-collapse 의 1차 피해자.
- **ko** — A 단독 STRONG, E2 단독 PURE_MEMORIZE, 나머지 WEAK 또는 W-. ko 는 STRONG 도달 가능 (A 증거) 이나 PM 으로도 빠지기 쉬움 (E2 증거) — anima-OWN corpus 의 ko 편중이 양방향 효과.
- **zh / ru / ja** — 거의 모든 axis 에서 WEAK 또는 worse. 5-lang 중 가장 낮은 score band, anima-OWN corpus 에서 record 수가 적은 (~500-1000 vs en 17078) 직접 반영.

## § 4. Axis movement analysis — 어느 축이 needle 을 움직였나

### 4.1 init_CE cluster 자연실험 (cycle 1 redispatch 의 결정적 증거)

```
        init_CE
14.79 ┤ ● A                ← Cluster X — curriculum (wiki-only 1000 step 선학습)
      │
14.46 ┤ ● C  ● C2  ● D     ← Cluster Z — baseline (head_g enable/disable/freeze_embed)
      │
14.18 ┤ ● B  ● F  ● E2     ← Cluster Y — aux-loss head (KD distill / InfoNCE / lang-bal)
      │
0     ┤
```

**핵심 발견** — head_g 의 enable/objective/disable 토글 (C vs C2 vs D) 이 init_CE 14.4564 에서 **byte-equal**. R8c head_g random output 가설 (init_CE 천장의 원인이 head_g) 이 자연실험으로 **falsified**.

| 축 group | init_CE 효과 | final verdict 효과 |
|---|---|---|
| aux loss head firing (B/F/E2) | -0.28 (14.46→14.18) | 0 — 여전히 n_strong=0 |
| curriculum 선학습 (A) | +0.34 (14.46→14.79) | +1 — ko STRONG 단독 도달 |
| head_g 토글 (C/C2/D) | 0 — byte-equal | (abort 또는 0/5 FAIL) |

### 4.2 corpus_quality 축의 사후 발견 (Track 1 retro · PR #340/#350)

cycle 1 의 7-axis 는 corpus 비율 (`wiki_frac=0.5`) 을 고정한 상태에서 **how to train** 만 sweep 했다. Track 1 E2 retro 측정 (PR #340) 으로 corpus_s101 input 의 **M3 TTR ≈ 0.03** (extreme repetition) 이 register-sink 의 dominant predictor 라는 가설이 등재 (PR #350 H_241.6 / H_242.6). 이는 본 AXIS_MAP 7-axis 가 corpus repetition 축을 미탐색했음을 사후로 노출.

함의 — Phase D v2b 의 hybrid corpus (M3 ≥ 0.3 design) 가 본 AXIS_MAP 의 **8 번째 축** (corpus diversity) 으로 들어옴.

### 4.3 register collapse 의 mitosis_max / scale 무영향

7 axis 모두 mitosis_max=16, 3B Qwen warm-init 으로 고정. final_CE 가 2.10-5.01 분포로 떨어졌으나 n_strong 은 0-1. **scale / mitosis cap 은 needle 미동**, 학습 dynamics 자체의 corpus / curriculum 축이 1차 lever.

## § 5. Best / worst fire highlights

**Best** — **A (curriculum)**: ko STRONG 16/20, 유일하게 n_strong ≥ 1. 1000-step wiki-only 선학습이 Korean head-start 를 만들었으나 다른 4-lang 으로 전이 안 됨 (cross-lingual generalize 불성공). final_CE 5.01 = 가장 높음 (loss 압축은 가장 적게 한 셈) — "loss 압축 ≠ STRONG 도달" 의 깨끗한 evidence.

**Worst (operational)** — **E (lang-balanced 1차)**: <60 s 만에 OOM 종료, no result, $1.10 sunk + 50min wall. LangBalancedSampler 의 GPU mem leak (per-lang corpus segment 가 resident 누적, 60 GiB unaccounted) 이 root cause. E2 retry 가 leak fix 후 완주했으나 ko=PM 으로 FAIL.

**Worst (verdict)** — **B (distill)**: final_CE 2.23 (3축 중 최저) **임에도** n_strong=0, en=PM coh=17/17 mem=17 (teacher mimicry 극단). teacher (vP21M LoRA 4/5 PARTIAL) 자체가 register-emission 영향권이라 KD 가 generalize 가 아닌 register pattern 을 distill — "최저 loss 가 최악 verdict" inverse 사례.

**Wasteful (saga cost)** — env-var-concat anti-pattern 사가 (`AXIS_MAP_BUG_POSTMORTEM.md`): caller 가 `P21H_STEPS="5000 P21H_BSZ=2 ..."` 단일 quoted string 으로 묶어 argparse rejection 반복, 1차/2차 fan-out 7-axis 낭비 + cycle 1 redispatch 비용 합산 **~$14** sunk. dispatcher 무결, caller 만 fix (PR #204 CALLER WARNING block).

## § 6. Cumulative cost ledger (이 dashboard 기준)

| 카테고리 | cost ($) | 비고 |
|---|---|---|
| 1차 fan-out 7 axis 정상 완주 (A+B+F) | 2.86 | A 1.45 + B 1.13 + F 0.28 |
| cycle 1 redispatch (C/C2/D) | 3.18 | C 1.14 + C2 1.14 + D 0.90 |
| E2 retry (leak fix) | 0.88 | 2105 s × H100 |
| E 1차 OOM | 1.10 | <60s + 50min idle |
| env-var-concat bug saga | ~14.00 | 1st/2nd fan-out 낭비 + cycle 1 redispatch 합산 |
| **누적 (E3v3 / Phase D v2b 미포함)** | **~22.02** | — |

E3v3 (in-flight) + Phase D v2b (queued) ~$3.5-7.5 추가 예상.

## § 7. C3 (missing data, inferences made)

1. **per-lang verdict 매핑** — 원본 SSOT 가 "n_strong=1 (ko)" / "en/ko PURE_MEMORIZE" / "en/zh/ru/ja WEAK" 같은 자연어 요약 위주. zh/ru/ja 의 정확한 per-lang score 가 다수 row 에서 누락 — heatmap 에 `?` 처리 (A/D/B 의 zh/ru/ja 일부). 정밀화하려면 `vP21H_axis_*/result.json` 의 `n_score` field 5-lang 전수 dump 필요.
2. **C / C2 abort 시점 verdict** — abort @625 / @375 step 이므로 verdict row 자체가 부재. cluster-Z init_CE byte-equal 만 결정적 신호 (R8c falsify) — verdict 칸은 `—` 로 표기.
3. **E3v3 in-flight** — pod `eece02rl2k1wz2` 작성 시점 IN-PROGRESS, result row 는 placeholder. wiki_frac=1.0 endpoint (anima 0%) 측정 후 cycle update 필요.
4. **Phase D v2b queued** — Monitor `bwjvpbkog` 결과 wait. corpus build 완료 + dispatch 후 row 갱신.
5. **axis movement causal claim 은 correlation only** — cluster X/Y/Z 가 init_CE 에 결정적이라는 것은 byte-equal 자연실험 (높은 strength) 이지만, "curriculum 이 ko STRONG 의 cause" / "KD 가 register-pattern 의 cause" 는 single-fire correlation. RCT 가 아니므로 axis × axis 조합 (cell-4) 미측정.
6. **per-lang verdict char code** (S/P/PM/W/W-/F/E/?) 는 본 문서가 정의 — 원본 SSOT 에는 free-form prose. 향후 fire 의 row 갱신은 본 코드를 따르면 heatmap 자동 확장 가능.

## § 8. Cross-reference

- 축 spec: [`../AXIS_MAP.md`](../AXIS_MAP.md)
- 3/7 partial baseline: [`../AXIS_MAP_RESULTS.md`](../AXIS_MAP_RESULTS.md)
- 5/7 + 2 abort 업데이트: [`../AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md`](../AXIS_MAP_RESULTS_UPDATE_5_7_2026_05_23.md)
- env-var-concat bug postmortem: [`../AXIS_MAP_BUG_POSTMORTEM.md`](../AXIS_MAP_BUG_POSTMORTEM.md)
- E OOM addendum: [`../AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md`](../AXIS_MAP_BUG_POSTMORTEM_E_OOM_ADDENDUM_2026_05_23.md)
- E2 retro (output 6-metric): [`track1_e2_retro_corpus_quality_2026_05_24.md`](track1_e2_retro_corpus_quality_2026_05_24.md)
- Phase D goal SSOT: [`../PHASE_D_corpus_fire_goal.md`](../PHASE_D_corpus_fire_goal.md)

— 끝 —
