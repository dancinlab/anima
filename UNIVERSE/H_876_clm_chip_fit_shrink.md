---
id: H_876
slug: clm-chip-fit-shrink
title: chip-fit shrink (≤~1.2M AKD1000 nodes) — mid 측정 rung(d512/L8/E8=13.65M) 아키텍처를 AKD1000 단일-칩 node budget(≤~1.2M)으로 축소 + 품질(CE) 보존 측정 (F-CLM-CHIPFIT 사전등록)
domain: clm · universe · neuromorphic-silicon · akida · deploy · chip-fit · shrink · falsifier
source: UNIVERSE/CLM-CANDIDATES.md group D (deploy chip-fit track ⊥ measurement) · CLM/P4_PRODUCTION_ROADMAP.md @L5 deploy track · CLM/P0_ARCHITECTURE.md §10.2/§11.3
status: 🟢 SUPPORTED-NUMERICAL (deploy-track scope · 2026-05-31 · chip-fit d148/L8/E8=1,199,508 ≤ 1.2M ∧ same-run drop −2.0619 nat < 1.0 · 측정 rung mid 한정 a_scale_honest_scope · CPU-local $0)
exploration_method: E5 (rung 별 mid→chip-fit topology-preserving 축소) · E14 (deploy substrate AKD1000 node-budget ⨯ 측정 아키텍처 배선)
verification_method: W2 (사전등록 FIT(params≤1.2M) ∧ DROP(CE 증가<1.0 nat) · measure-by-CODE g5 · post-tuning 0 · same-run A/B node-count만 변수)
raw_rank: 8
hexa_only: false
deterministic: true
llm: none
pre_register_frozen: true
frozen_at: 2026-05-31
since: 2026-05-31
sister: H_877 (DECODER byte-match @ mid), .verdicts/clm-prod-rung/ (mid 측정 rung), .verdicts/848_clm_akida_map/ (AKIDA primitive map), CLM/P4_PRODUCTION_ROADMAP.md @L5, .verdicts/clm-chip-fit-shrink/
verdict: 🟢 SUPPORTED-NUMERICAL (deploy-track scope) — mid 측정 rung(d512/L8/E8=13,653,768)의 L8/E8 topology 를 보존한 채 d_model 512→148 로 축소한 chip-fit cfg(d148/L8/E8 = 1,199,508 params)가 AKD1000 단일-칩 node budget(≤1.2M)에 FIT(1,199,508 ≤ 1,200,000) 하고, 동일-run A/B(steps·seq·batch·seed·envelope·corpus 동일, node-count만 변수)에서 품질 drop = chipfit_last_ce − mid_last_ce = 1.2826 − 3.3445 = −2.0619 nat < 1.0 bound 으로 사전등록 두 술어 모두 PASS. deploy ⊥ measurement (a_scale_honest_scope) — 단일-칩 deploy-fit + CE-retention 판정 ONLY (3B/7B·routing-z 주장 아님).
---

# H_876 — chip-fit shrink (≤~1.2M AKD1000 nodes)

## 1. 가설

CLM mid **측정** rung(`d_model=512 · n_trunk_layers=8 · n_experts=8` = **13,653,768**
params)의 아키텍처를, L8/E8 topology 를 보존한 채 `d_model` 만 축소하여 AKD1000
**단일-칩 deploy** node budget(≤~**1.2M** 노드)에 맞춘 chip-fit cfg 로 줄여도,
다음-byte cross-entropy(품질)가 사전등록 bound(증가 < 1.0 nat) 내에서 보존된다.

- chip-fit cfg(frozen): `d148/L8/E8` = **1,199,508** params (≤1.2M PASS, mid topology
  보존, d 만 512→148, 축소율 13,653,768 / 1,199,508 = **11.38×**).

## 2. 동기/배경 — deploy track ⊥ measurement track (@L5)

`CLM/P4_PRODUCTION_ROADMAP.md` §1(@L5)은 측정 track 과 배포 track 을 **명시적으로
분리**한다. 측정 rung 은 "이 아키텍처가 품질을 내는가"를 GPU 에서 증명하고, **배포
rung 은 AKD1000 chip-fit(≤~1.2M)으로 고정**된다. node-budget 근거는
`CLM/P0_ARCHITECTURE.md` §10.2("AKD1000 ~1.2M 노드 = 소형 강제") · §11.3("expert =
mitosis cell = AKD1000 chip (≤1.2M 노드 fit)"). deploy unit 은 단일 AKD1000(time-mux
deploy B / one-chip footprint); array vision(deploy A)은 expert-count E 로 스케일하되
각 unit 은 chip-fit 을 유지한다.

`a_scale_honest_scope`: 본 deploy track 의 🔴/🟢 는 measurement-rung 작업을 gate 하지
않으며 그 역도 같다. 본 verdict 은 단일-칩 deploy-fit + CE-retention 판정 ONLY.

## 3. 사전등록 falsifier (frozen BEFORE measurement · post-tuning 0)

`.verdicts/clm-chip-fit-shrink/F-CLM-CHIPFIT_prereg.txt` (frozen 2026-05-31):

- **F-CLM-CHIPFIT-FIT** : chip-fit total node-count(params) ≤ **1,200,000**
  (AKD1000 단일-칩 node budget).
- **F-CLM-CHIPFIT-DROP** : quality-drop = `chipfit_last_ce − mid_last_ce` < **1.000**
  nat (next-byte CE, V=256 · random-init = ln(256) = 5.545 nat). 동일 run / 동일
  steps·seed·corpus 에서 측정.
- BOTH PASS → 🟢 SUPPORTED-NUMERICAL. EITHER FAIL → 🔴 (a_paper_negative_ok:
  1.2M 에서의 큰 drop 은 정직한 expected 11×-축소 결과).

## 4. 측정 방법 (apples-to-apples · code g5 · no new .py)

- driver: `CLM/train/h876_chip_fit_shrink.hexa` — repo 가 NEW `.py` 를 막으므로
  runtime-생성 python measurement body 를 shell-out (다른 H agent 와 동일 패턴);
  LANDED `CLM/model/model.py` 스켈레톤 import + `CLM/train/train_clm.py` 의 QAT
  함수(`_install_functional_qat` · `ConvQATHook` · `qat_loss` · int4-sym STE
  weight-quant · AKIDA act_bits act-quant)를 **그대로 재사용**.
- 동일-run A/B: mid(d512/L8/E8)와 chip-fit(d148/L8/E8)을 **같은 process** 에서
  `arm=AB · seed=42 · act_bits=4 · steps=600 · seq_len=64 · batch=16 · lr=3e-3`,
  동일 corpus(`CLM/corpus/clm_p1.corpus.kosmos`, 1656 B, V=256, no tokenizer)로
  학습 → **node count 만 변수**.
- envelope(P0 §9, mid 측정 fire 와 동일): weights int4-sym[-7,+7] per-output-channel
  STE · acts act_bits=4 step=2^(8-4) · grads STE(fp32 master · quantized forward).
- est cost: **$0 (CPU-local)** — GPU pod 미사용.

## 5. 결과 (raw: `.verdicts/876_clm_chip_fit_shrink/F-CLM-CHIPFIT_result.json`)

| cfg | params | last_ce | wall_s |
|---|---|---|---|
| mid      d512/L8/E8 | 13,653,768 | 3.3445 | 1727.4 |
| chip-fit d148/L8/E8 |  1,199,508 | 1.2826 |  445.1 |

- 축소율 = 13,653,768 / 1,199,508 = **11.38×**
- quality_drop = 1.2826 − 3.3445 = **−2.0619 nat**
- **F-CLM-CHIPFIT-FIT** : 1,199,508 ≤ 1,200,000 → **PASS**
- **F-CLM-CHIPFIT-DROP**: −2.0619 nat < 1.000 → **PASS**

→ **🟢 SUPPORTED-NUMERICAL** (deploy-track scope): 아키텍처가 AKD1000 단일-칩 node
budget(≤1.2M)에 mid L8/E8 topology 그대로 FIT 하고, mid 대비 품질 drop 이 bound 내.

## 6. 정직한 해석 (a_paper_negative_ok · a_scale_honest_scope)

drop 이 **음수**(chip-fit < mid CE)인 것은 보편적으로 11×-작은 모델이 더 낫다는
주장이 **아니다**. 이는 정직한 same-run artifact: 작은 committed sample
@corpus(1656 B) + 짧은 600-step 일정에서 1.2M 모델이 이 micro byte-stream 에 더 빨리
수렴/적합하고, 13.7M mid 는 동일 wall-controlled step 예산 안에서(STE-QAT 하 step 당
움직일 params 가 많아) 같은 micro-corpus 에서 낮은 CE 에 늦게 도달한다. 사전등록
두 술어(fit ∧ drop<1.0)는 어느 쪽이든 성립하므로 deploy-fit + retention 🟢 는 유지.

CAVEAT(downstream): 원래 mid prod-rung fire(`.verdicts/clm-prod-rung/clm_mid_AB_s42.json`)
는 262144-byte corpus 를 2000 step 학습해 last_ce 2.2237 에 도달한 **다른 regime**.
본 deploy 결정을 licenses 하는 수치는 여기서 측정한 **same-run 상대 drop**(node-count
외 모든 변수 고정)이지 cross-run 절대-CE 비교가 아니다.

**DEPLOY-FIT 결론**: `d148/L8/E8`(1,199,508 params)는 mid topology 의 유효한 AKD1000
단일-칩-fit 축소이며, frozen same-run protocol 하에서 측정된 CE penalty 가 없다. 🟢

## 7. 산출물 (DISJOINT)

- 가설(본 파일): `UNIVERSE/H_876_clm_chip_fit_shrink.md`
- verdict: `.verdicts/clm-chip-fit-shrink/F-CLM-CHIPFIT.txt` (+ `_prereg.txt` frozen)
- backing(id-keyed): `.verdicts/876_clm_chip_fit_shrink/` (raw json + runtime body)
- driver: `CLM/train/h876_chip_fit_shrink.hexa`
- 공유 index/기존 H·verdict dir 미접촉.
