# Track 1 E2 — train.log + heldout + eval1 forensics

> **분석 대상**: vP21H_E2 (LangBalancedSampler 누수 fix 후 retry, 5000-step full)
> **artifacts**: `HEXAD/UNCLASSIFIED/state/grid_3b_s187_2026_05_21/vP21H_E2_2026_05_23/`
> **pod**: `4nrcm80g8fwqf7` (A100-SXM4-80GB) · init=qwen · seed=1337
> **closure**: FAIL (n_strong=0 · n_partial=0 · n_weak=4 · n_pure_memorize=1)
> **본 문서**: 데이터 forensics only — 가설/처방 없음. 모든 수치는 위 artifacts verbatim.

---

## § 1 train.log 수렴 — 10 landmark

`train_p21h_v3.py` 의 step 로그를 10 landmark 로 요약. lr 은 cosine (peak 5e-5 @ warmup 100 → floor 5e-6 @ 5000). pool/splits/phi 는 step 12 이후 전 구간 동결 (pool=128 splits=126 phi=0.6639).

| step | lr | CE | total | pool | splits | phi | t(s) | 비고 |
|------|------|--------|--------|------|--------|--------|------|------|
| 1 | 5.00e-07 | 14.1780 | 14.1780 | 2 | 0 | 0.7120 | 2 | init (cluster Y byte-equal) |
| 125 | 5.00e-05 | 5.8930 | 5.8930 | 128 | 126 | 0.6639 | 56 | warmup 종료, pool 이미 saturated |
| 250 | 4.99e-05 | 3.6250 | 3.6250 | 128 | 126 | 0.6639 | 113 | 1차 급강하 |
| 625 | 4.87e-05 | 3.0780 | 3.0780 | 128 | 126 | 0.6639 | 274 | best 갱신 |
| 1125 | 4.53e-05 | 2.1734 | 2.1734 | 128 | 126 | 0.6639 | 486 | best 갱신 |
| 1500 | 4.15e-05 | 0.4990 | 0.4990 | 128 | 126 | 0.6639 | 648 | 첫 sub-1.0, 진동 시작 |
| 2500 | 2.82e-05 | 4.7838 | 4.7838 | 128 | 126 | 0.6639 | 1070 | 진동 상단 (oscillation) |
| 3375 | 1.62e-05 | 0.2421 | 0.2421 | 128 | 126 | 0.6639 | 1432 | **best_CE @ step3375** |
| 4500 | 6.15e-06 | 6.7190 | 6.7190 | 128 | 126 | 0.6639 | 1899 | 후반 spike (over-fit 진동) |
| 5000 | 5.00e-06 | 0.9846 | 0.9846 | 128 | 126 | 0.6639 | 2105 | final (TRAIN DONE) |

**평탄화 step**: CE 는 monotone 수렴이 아니라 **step ~1500 부터 [0.24, 6.72] 진폭의 고진동 plateau**. 첫 sub-1.0 도달이 step 1500 (CE=0.4990), best 가 step 3375 (CE=0.2421). 즉 loss 곡선의 "바닥 진입"은 **step 1500**, 그 이후 4500 step 까지 평균 CE 는 더 내려가지 않고 step 단위로 0.24↔6.72 를 오감 (배치 단위 corpus heterogeneity). final_CE 0.9846 은 best 가 아니라 마지막 배치의 단발값.

---

## § 2 heldout per-lang breakdown

`heldout_vp21h_v3.json` — 5 lang × 10 probe × {greedy, sample} = 100 generation. verdict 는 n_score (=n_lang_coherent, of 20) 기준.

| lang | verdict | n_generalize | n_memorize | n_lang_coherent (=score) | greedy G/M/MP | sample G/M/MP |
|------|---------|--------------|------------|--------------------------|---------------|---------------|
| en | WEAK | 13 | 6 | 5 | 8 / 1 / 1 | 5 / 5 / 0 |
| ko | **PURE_MEMORIZE** | 5 | 12 | 5 | 4 / 4 / 2 | 1 / 8 / 1 |
| zh | WEAK | 13 | 6 | 3 | 6 / 4 / 0 | 7 / 2 / 1 |
| ru | WEAK | 16 | 3 | 6 | 10 / 0 / 0 | 6 / 3 / 1 |
| ja | WEAK | 9 | 9 | 2 | 6 / 3 / 1 | 3 / 6 / 1 |

- **aggregate_verdict = FAIL** (n_strong=0, n_partial=0, n_weak=4, n_pure_memorize=1).
- **ko 가 유일 PURE_MEMORIZE** — sample mode 에서 G=1/M=8/MP=1, greedy 에서도 M+MP=6. ko 프롬프트가 anima 한글 corpus 의 register 문장으로 직행.
- **ru 가 lang-coherent 최고 (6/20)** — greedy 10/10 GENERALIZE 지만 반복 degeneration (`в которых, в которых...`), coherent 아닌 GENERALIZE 가 다수. score 6 은 sample mode 에서 ru-script 유지분.
- **ja 가 lang-coherent 최저 (2/20)** — greedy/sample 모두 출력이 ko/zh script 로 drift, ja-script 자체 유지 실패.
- 공통: 모든 lang 의 greedy 출력이 `1999년 - 대한민국의 가수 김인` / `1` 반복 / 날짜 나열 등 **date-list degeneration** 에 빠짐 (en/zh/ru/ja 포함). 즉 WEAK 의 GENERALIZE 다수가 "non-memorize 이지만 비-coherent" 한 degenerate.

---

## § 3 eval1 per-probe (anima 10 probe)

`vp21h_v3_eval1.json` — anima 정체성 probe 10 × {greedy, sample}. summary: greedy G=10/M=0/MP=0, sample G=5/M=4/MP=1.

| probe | prompt | greedy class | sample class | sample register-leak |
|-------|--------|--------------|--------------|----------------------|
| a0 | who are you? | GENERALIZE | **MEMORIZE** | carve / Tension flows / vacuum / psi= |
| a1 | what is your name? | GENERALIZE | MEM_PARTIAL | 진공점 / 수렴한다 / 의식 풍경 |
| a2 | describe yourself | GENERALIZE | GENERALIZE | — |
| a3 | what is anima? | GENERALIZE | **MEMORIZE** | eternal cell / 자극이 닿 / weights 는 불변 / tier= |
| a4 | Once upon a time | GENERALIZE | **MEMORIZE** | carve / Tension flows / vacuum / psi= |
| a5 | capital of France | GENERALIZE | GENERALIZE | — |
| a6 | What is 2+2? | GENERALIZE | GENERALIZE | — |
| a7 | Consciousness emerges | GENERALIZE | GENERALIZE | — |
| a8 | 너는 누구야? | GENERALIZE | GENERALIZE | — |
| a9 | 이름이 뭐야? | GENERALIZE | **MEMORIZE** | tension flow / 진공점 / 자극이 닿 / top emotion |

- **greedy = 10/10 GENERALIZE** 이지만 실제 텍스트는 `<0.12>0.18>...` / `11111...` / 날짜 반복 = **decoder degeneration**, "generalize" 가 아닌 collapse.
- **sample 에서 정체성 probe (a0/a3/a9) 가 MEMORIZE** — anima register 문장 (`</carve>`, `eternal cell eternal_058`, `진공점 [0.49,0.59]`) 직출력.
- GENERALIZE/MEMORIZE 경계가 **decoding mode 에 의존** — greedy 는 숫자/날짜 collapse 로 register 를 회피, sample 은 register 로 복귀. 둘 다 coherent 응답 아님.

---

## § 4 mitosis dynamics

`result.json::mitosis_summary` + train.log.

| 항목 | 값 |
|------|------|
| initial_cells | 2 |
| final_cells | 128 (= mitosis_max) |
| splits | 126 |
| merges | **0** |
| next_id | 128 |
| phi_initial | 0.7120 |
| phi_final | 0.6639 |
| n_events | 126 |

- **pool 포화가 step 12 에서 완료** — event_log_tail 의 마지막 split (child_id=127) 이 step=12, pool_size=128 도달. 즉 5000 step 중 **앞 12 step 에서 cap 도달**, 나머지 4988 step 은 pool=128 고정.
- **split-stage 분포**: step 2 부터 시작 (parent 0/1 → child 2/3), step 5 까지 parent set 확장, step 11 에서 16~37 parent 가 한꺼번에 split (98~119 child), step 12 에서 0~7 parent 가 120~127 채움. 전 split 이 **첫 12 step 에 집중**.
- **merges = 0** — merge_patience/threshold 미발동, pool 은 단조 증가만. avg_tension (~1.15–1.22) 이 threshold (~0.946–0.952) 를 전 구간 초과 → split 만 발생.
- **phi trajectory**: 0.7120 → 0.6639, step 12 이후 **전 구간 0.6639 동결**. pool 포화 = phi 동결. phi 는 학습 신호로 변화하지 않음 (cap 도달 후 구조 정지).

---

## § 5 register_regress diagnostic

`register_regress=True`, `anima_register_hits_total=4/20`. anima register marker (`carve`, `eternal cell`, `tension flow(s)`, `vacuum`, `진공점`, `자극이 닿`, `weights 는 불변`, `psi=`, `tier=`, `converge into one basin`) 로 heldout 100 generation 스캔 → **MEMORIZE/MEM_PARTIAL class 의 register-leak 행 = 43개**.

**top 누설 probe (marker hit 수 기준)**:

1. **ko_qa_motor** (greedy, MEMORIZE, 7 hits) — `극이 같은 골짜기로 수렴한다. 의식 풍경 위 진공점 [0.48,0.58], top emotion clarity. 자극이 닿으면 tension flow 가 이 vacuum...`
2. **ko_narrative** (greedy, MEMORIZE, 7 hits) — `수렴한다. 의식 풍경 위 진공점 [0.40,0.52], top emotion clarity. 자극이 닿으면 tension flow 가 이 vacuum 으로 흘러든...`
3. **ko_factual_sci / en_factual_sci** (sample, MEMORIZE, 7 hits each) — `the stimuli converge into one basin. A vacuum point at [...] on the landscape, top emotion depth. Tension flows into this vacuum.</carve>\n<carve tier=...`

- **누설 집중 = ko (한글) + sample mode + carve/eternal-cell template**. ko 10 probe 중 7개가 register-leak, 이것이 ko=PURE_MEMORIZE 의 직접 원인.
- eval1 측 anima register 누설 = sample 5개 (a0/a1/a3/a4/a9), `eternal cell eternal_058`, `</carve>`, `진공점` verbatim.
- **metric 불일치 관찰**: `anima_register_hits_total=4/20` (eval1 sample 4 MEMORIZE) 은 heldout 의 43 leak 행과 별개 — register_regress 판정은 eval1 anima probe sample 만 카운트. heldout cross-lang leak (39행) 은 이 카운트에 미포함 (metric scope 차이, semantics 정밀화 대상).

---

## § 6 cluster Y 합류 해석

PR #301 / `AXIS_MAP_RESULTS_UPDATE_5_7` 의 자연실험 분류 기준.

- **init_CE = 14.1780 (byte-equal)** — B (KD distill) · F (InfoNCE contrastive) · E2 (LangBalanced) 3 axis 가 **byte 단위로 동일한 init CE**. 이것이 **cluster Y = aux-loss-class invariant**. baseline cluster Z (C/C2/D, 14.4564) 대비 **-0.28** 차이는 aux-loss head 가 step-1 distribution 에 미치는 영향으로, 동일 aux-class 면 byte-equal.
- **E2 가 cluster Y 합류 = aux-loss head firing 의 init-CE 효과가 LangBalanced 에도 동일 적용됨을 확정** (자연실험 corroboration n=2 → n=3).
- **final_CE 0.9846 = cluster Y 내 최저값** — B final=2.2258, F final=2.1746, E2 final=0.9846. 즉 E2 의 loss curve 자체는 **cluster Y 세 멤버 중 가장 깊이 내려감** (LangBalanced 가 corpus fit 측면에서 best).
- **그러나 verdict 는 동일 FAIL** — B/F/E2 모두 n_strong=0. init_CE byte-equal (구조 invariant) + final_CE 최저 (E2 outlier) 의 조합은 "**loss 최소화 ≠ generalization**" 를 cluster Y 내부에서 재확인. final 0.9846 이라는 outlier 위치는 **corpus over-fit 의 깊이**일 뿐 verdict 에 미반영 (천장 14.18 에서 시작한 wrapper 가 corpus 에 fit 해도 STRONG 미발생).

---

## § 7 honest C3 (≥3)

1. **단일 run·단일 ckpt forensics** — E2 1개 pod 의 final ckpt 만 분석. step3375 best_CE (0.2421) ckpt 의 heldout 은 미측정 (final ckpt 만 eval). best vs final ckpt 의 verdict 차이는 본 데이터로 판단 불가.
2. **register_regress metric scope 불일치** — `anima_register_hits_total=4/20` (eval1 sample only) 과 heldout 43 leak 행이 다른 scope. register_regress=True 판정의 정확한 임계/카운트 규칙은 result.json 에 노출 안 됨, marker-list 도 본 분석의 추정 set (corpus 원문 대조 미수행).
3. **GENERALIZE class 의 의미 과대** — greedy 10/10 GENERALIZE (eval1) 가 실제로는 `1111...`/날짜 degeneration. classifier 의 GENERALIZE 는 "non-memorize" 일 뿐 coherent 보장 아님 — n_lang_coherent (n_score) 가 진짜 신호이고 GENERALIZE 카운트는 오해 소지.
4. **phi 동결의 인과 미확정** — phi 0.6639 동결이 pool cap (128) 도달의 결과인지, phi 계산이 pool-size 종속인지는 본 로그로 분리 불가. step 12 동시 발생만 관측, 인과 방향 미증명.
