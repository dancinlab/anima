# PURE BENCHMARK — Phase B/C/D + sleep/dream + mitosis baseline SSOT (2026-05-24)

> PURE saga (V3 rebrand) 가 오늘까지 산출한 **모든 측정된 baseline metric**
> 을 한 화면에 모은 단일 reference 문서. 지금까지 layer 별/PR 별 산출물에
> 분산돼 있던 metric 들 (Track 1 E2/E3v3 register_hits · Phase D v1/v2 hybrid
> 6-metric · M9b anima-OWN PoC · saga 통계 · cluster 자연실험 · runpod $ 합산)
> 을 cross-ref. milestone **B1 (pure-baseline-metric-publish)** 의 deliverable.
>
> 본 문서는 **no new fact discovery** — 기존 PR/doc artifact 를 인용/요약만.
> 모든 metric row 에 PR # cite (traceability). 측정 시점 모두 **as-of 2026-05-24 KST**.
>
> source —
> [`PURE.md`](../../PURE.md) · [`PURE.log.md`](../../PURE.log.md) ·
> [`HEXAD/PURE/PURE_SAGA_2026_05_24.md`](PURE_SAGA_2026_05_24.md) (PR #392) ·
> [`HEXAD/PURE/docs/axis_map_history_2026_05_24.md`](docs/axis_map_history_2026_05_24.md) (PR #388) ·
> [`state/fire_cost_ledger.md`](../../state/fire_cost_ledger.md) (PR #389) ·
> [`HEXAD/PURE/docs/track1_corpus_quality_2026_05_24.md`](docs/track1_corpus_quality_2026_05_24.md) (PR #340) ·
> [`HEXAD/PURE/docs/track1_e2_retro_corpus_quality_2026_05_24.md`](docs/track1_e2_retro_corpus_quality_2026_05_24.md) (PR #350) ·
> [`HEXAD/PURE/docs/phase_d_result_schema_2026_05_24.md`](docs/phase_d_result_schema_2026_05_24.md) (PR #371) ·
> `state/pure_phase_d_corpus_{2026_05_24, v2_2026_05_24, anima_own_poc_2026_05_24}/manifest.json`

---

## § 1. Executive baseline

| 항목 | 값 | 근거 |
|---|---|---|
| Saga closure 상태 | **OPEN** (5/5 ckpt-bearing fire 모두 4-criterion 미달) | PURE_SAGA § Executive (PR #392) |
| 완주 fire 중 n_strong ≥ 4/5 도달 | **0 / 8 axis** (1차 fan-out 7 + E2 retry) | axis_map_history § 2 (PR #388) |
| 최고 단일-axis verdict | **A (curriculum)** — ko STRONG 16/20, n_strong=1 | axis_map_history § 5 (PR #388) |
| 최악 verdict (closure) | **B (distill)** — final_CE 2.23 (최저) but n_strong=0, en=PURE_MEMORIZE coh=17/17 | axis_map_history § 5 (PR #388) |
| 최악 operational (LOST) | **Phase D v1 stale-branch** — ckpt 미회수, ~$1.50 sunk + 1.5 h wall | PR #378 postmortem · ledger entry |
| 최고 corpus M3 (Phase D 계열) | **0.504** (v2 ko-heavy hybrid 1 MB sample) | manifest `pure_phase_d_corpus_v2_2026_05_24` (PR #390) |
| 누적 PURE GPU cost (today) | **~$6-7** (E2 0.87 + E3v3 2.20 + Phase D v1 ~1.50 + rogue <0.10 + v2b ~1.5-2) | fire_cost_ledger § Cycle PURE today (PR #389) |
| 4-criterion empirical satisfaction | **0 / 4** (spec ready, fire result 미도착) | PR #371 § 6 · PURE_SAGA § Closure |

해석 — engine 4 layer (Phase B/C/sleep/mitosis) 는 모두 LANDED 상태. corpus + fire layer 에서 register-collapse double-bind (E2 wiki=0.5 → register_hits=4/20, E3v3 wiki=1.0 → 0/20 but generalize 약화) 가 root cause. Phase D 다음 fire 가 4-criterion auto-judge wiring 의 first end-to-end 사례 후보.

---

## § 2. Layer baselines

### 2.1 Phase B — 8-factor motivation engine (LANDED)

| metric | 값 | 근거 |
|---|---|---|
| 위치 | `HEXAD/CHAT/spontaneous_lib.hexa` | PURE.md L20 |
| smoke 결과 | **7/7 PASS** (B-SPONT-1..7) | PURE.md L20 |
| 8 factor + weights (Σ=1.00) | relevance 0.20 · gap 0.10 · curiosity 0.15 · pain 0.10 · coherence 0.10 · originality 0.10 · balance 0.15 · dynamics 0.10 | PR #371 § 5 표 |
| motivation_score range | ∈ [0, 1] (B-SPONT-FACTOR-1..8 clamp) | PR #371 § 5 |
| closure threshold | `motivation_score ≥ 0.30` (default emit threshold) | PR #371 § 6 #3 |
| 실 fire 측정 | **0건** — dry-run synthetic only (F-DISP-MOT 8/8 PASS, PR #366) | PR #371 § 9 #3 |

### 2.2 Phase C — interaction model (LANDED)

| metric | 값 | 근거 |
|---|---|---|
| 위치 | `HEXAD/CHAT/{channel_mux, anima_chat_v2_lib}.hexa` | PURE.md L21 |
| blue closure | **83 / 83 🔵** (anima_chat_v2 + channel_mux 통합) | PURE.md L21 |
| backend coverage | thinker-talker dual-track + IPC dream stage reader | grep `anima_chat_v2_lib.hexa` |

### 2.3 sleep/dream 5-stage (LANDED, autonomy-reshaped)

| stage | Φ envelope | tension envelope | 근거 |
|---|---|---|---|
| WAKE | **1.0** | 1.0 | `anima_dream_stage.hexa` const table · PR #371 § 4 |
| N1   | **0.7** | 0.7 | 동상 |
| N2   | **0.4** | 0.4 | 동상 |
| N3   | **0.15** | 0.2 | 동상 (deep slow-wave, 비-zero) |
| REM  | **0.95** | 0.9 | F-DREAM-3: \|Φ_REM − Φ_WAKE\| ≤ 0.05 (P47 finding) |

IPC live (`$HOME/.cache/anima/dream_stage.current`, PR #307). **stage = context** (Φ-envelope + tension-envelope), **emit gate 아님** (`@D a_autonomy_over_hardcode` · `@N p5_tension_emit_not_filler`, PR #325).

### 2.4 mitosis / imagination (LANDED)

| metric | 값 | 근거 |
|---|---|---|
| 가설 anchor | **H_229** (imagination loop · emit-free internal rehearsal) | PURE.md L23 |
| mitosis_lib closure | **W8** (8-section closed) | PURE.md L23 |
| cap default | **16** (R6 사후 권고: 32 이상 시 step12 동결 risk; AXIS_MAP 7-axis 모두 cap=16 고정) | axis_map_history § 4.3 (PR #388) |
| live split observation | **21 split events** in synthetic chat_generate (cells 2→23 in 40 steps) | memory `project_anima_chat_multitoken_split_merge_2026_05_12` |

---

## § 3. Corpus baselines — 6-metric (M1-M6)

`HEXAD/PURE/eval/corpus_quality_probe.hexa` (PR #287) `score_corpus_jsonl(path, sample_bytes=1 MB)` 산출.

| corpus | M1 ENTROPY | M2 BIGRAM_MI | **M3 TTR** | M4 AVG_LINE | M5 HANGUL | M6 KL_UNIF | 출처 PR / state |
|---|---|---|---|---|---|---|---|
| **corpus_s101** (anima-OWN seed, 600 MB) | n/a (payload .gitignore) | n/a | **0.03** (실측 PR #340 sub-sample) | n/a | 1.66-2.34% (proxy alm_r14 0.32) | n/a | PR #340 · `state/pure_track1_corpus_quality_2026_05_24/` |
| alm_r14 (anima seed proxy) | 5.7835 | 2.0058 | 0.2294 | 1181.0 | 0.3217 | 2.2332 | PR #340 § 2 |
| tier1_low (proxy) | 5.7156 | 2.6618 | 0.2458 | 1165.5 | 0.2370 | 2.2954 | PR #340 § 2 |
| multi_wiki (5-lang, 51 MB) | n/a (pod-side build only) | n/a | n/a | n/a | n/a | n/a | PR #340 § 1 |
| **Phase D v1** (synthetic, 31 MB) | 6.1513 | 3.1379 | **0.3539** | 339.95 | 0.120 | 1.8548 | `state/pure_phase_d_corpus_2026_05_24/quality_score_1mb.json` |
| **Phase D v2** (hybrid + kowiki 0.2 weight, 109 MB) | 6.1258 | 3.1379 | **0.5040** | 1025.70 | 0.534 | 1.8874 | `state/pure_phase_d_corpus_v2_2026_05_24/quality_score_1mb.json` |
| **M9b anima-OWN PoC** (~/.claude/projects extract, 1.12 MB) | 6.1727 | 3.6469 | **0.2355** | 769.73 | 0.334 | 1.8447 | `state/pure_phase_d_corpus_anima_own_poc_2026_05_24/manifest.json` (PR #393) |

### 3.1 E2 output retro propagation (PR #350)

E2 ko output (20 sample concat, 2,833 byte) M3 = **0.366** vs input s101 0.03 (12.2× rebound, base-Qwen 회복). **relative rank propagation 확인** — ko output M3 가 5-lang 중 최저 (ko 0.366 < ru 0.411 < ja 0.482 < zh 0.539 < en 0.575) ↔ ko 단독 PURE_MEMORIZE 평가.

### 3.2 사후 발견 — 8 번째 미탐색 axis

cycle 1 의 AXIS_MAP 7-axis 는 `wiki_frac=0.5` 고정 + **how to train** 만 sweep. Track 1 E2 retro (PR #340) 가 corpus M3 ≈ 0.03 (extreme repetition) 을 register-sink dominant predictor 로 식별 → **M3 TTR (corpus diversity) 가 8 번째 미탐색 axis**. Phase D v2b hybrid (M3 ≥ 0.3 design) 가 이 axis 의 fire entry (axis_map_history § 4.2, PR #388).

---

## § 4. Closure criterion — 4-axis (verbatim from spec)

PURE.md L39 + Phase D 설계 (PR #344 spec) + result schema (PR #371 § 6) 의 자동 판정 mapping.

| # | 기준 | source field | 통과 임계 | 실 fire 측정 |
|---|---|---|---|---|
| 1 | register collapse 부재 | `n_anima_register_hits_total` | **< 4** (20 probe 中) | E2=4 (경계 fail) · E3v3=**0** (PASS) · Phase D 부재 |
| 2 | 다국어 closure | `per_lang_verdicts[].verdict` | **≥ 4 / 5** ≥ PARTIAL | 8/8 axis 모두 ≤ 1 · max=A 1/5 (ko) |
| 3 | substrate-native motivation | `motivation_8factor.motivation_score` | **≥ 0.30** | **0 measured** (dry-run synthetic only, PR #366) |
| 4 | sleep/dream context | `dream_stage_at_eval.phi_envelope` | block 존재 + Φ ∈ canonical | **0 measured** (Phase D fire 결과 부재) |

empirical: **0/4** (모든 ckpt-bearing fire LOST 또는 result 부재). spec ready · wiring 가능 · 실 측정 0.

---

## § 5. Fire baseline — 5-fire saga summary

`fire_cost_ledger.md` (PR #389) § Cycle PURE today 기준.

| variant | date | GPU | cost ($) | result | key metric | ref |
|---|---|---|---|---|---|---|
| **E1 baseline** | 05-23 (새벽) | (saga ref only) | — | seed cycle (Phase D 설계 전) | corpus_s101 M3 사후 인지 | PR #340 |
| **E2 wiki=0.5** | 05-23 | A100-SXM-80GB | 0.87 | FAIL closure 0/5 · ko=PM | register_hits **4/20** · init→final CE 14.18→0.98 | PR #301 · #310 |
| **E2 E-axis OOM** (sibling) | 05-23 | A100-SXM-80GB | 1.10 | CRASH (LangBalancedSampler GPU leak ~60 GiB) | <60 s + 50 min idle | PR #248 |
| **E3v3 wiki=1.0** | 05-24 (새벽) | A100-SXM-80GB | 2.20 | FAIL closure 1/5 (ko PARTIAL) | register_hits **0/20** · double-bind 확인 | PURE.log.md closure |
| **Phase D v1** stale-branch | 05-24 | A100-SXM-80GB | ~1.50 ±0.5 | **LOST** (ckpt 미회수, scp FATAL) | corpus M3 0.354 design · stale merge-base 8de602c07 | PR #378 |
| **Phase D v1 rogue** | 05-24 | A100-SXM-80GB | <0.10 | CRASH (idle cleanup) | — | PR #378 § 부가 (a) |
| **Phase D v2b** hybrid | 05-24 | A100-SXM-80GB | ~1.5-2 | **LOST** (외부 cleanup · result 도착 전) | corpus v2 M3 0.504 design · steps=2000 | ledger v2b · PR #390 |

LOST/TIMEOUT 비율 = **3/20 (15%)** (cumulative 20 fire 중, ledger § Cumulative). 모두 dispatcher / env / branch hygiene 원인 — training-side bug 아님.

---

## § 6. Verdict distribution — per-lang heatmap

axis_map_history § 3 (PR #388) verbatim mirror — 8 완주 axis (1차 fan-out 7 + E2 retry):

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
```

코드 — **S** STRONG · **P** PARTIAL · **PM** PURE_MEMORIZE · **W** WEAK · **W-** WEAK low · **F** FAIL/coh=0 · **E** error/OOM · **?** in-flight.

세로 관찰 (PR #388 § 3):
- **en** — 5/6 완주 axis 에서 PM 또는 WEAK · STRONG 0회. register-collapse 1차 피해자.
- **ko** — A 단독 STRONG · E2 단독 PM · 나머지 WEAK. anima-OWN corpus 의 ko 편중 양방향 효과.
- **zh / ru / ja** — 거의 모든 axis 에서 WEAK 이하. 5-lang 중 record 수 ~500-1000 vs en 17078 직접 반영.

axis movement (PR #388 § 4.1) — head_g enable/disable/freeze_embed (C / C2 / D) 가 init_CE 14.4564 byte-equal → R8c "head_g 가 init_CE 천장 cause" 가설 **falsified**.

---

## § 7. Cross-references — 본 saga 산출 PR list (compact)

**Phase B/C/sleep/mitosis (engine layer)** — #220 (V3→PURE rename) · #325 (H_244 autonomy reframe) · LANDED 사전 PR 다수 (CHAT lib + dream stage IPC + mitosis_lib W8)

**Corpus + eval (PR #287/#340/#350 lineage)** — #287 (corpus_quality_probe) · #340 (s101 M3 실측) · #350 (H_241/H_242 M5→M3 amend) · #344 (Phase D corpus spec) · #368 (Phase D corpus build M3=0.354) · #390 (corpus_v2 hybrid M3=0.504) · #393 (M9b anima-OWN PoC M3=0.236)

**Fire dispatch + auto-judge** — #295/#308 (dispatch_p21h_v3 hexa-port + stdlib v0.2) · #355/#363/#366 (axis_map auto-append + dream_stage IPC + motivation_8factor) · #370 (auto-append meta) · #371 (result schema SSOT) · #372 (--corpus-path) · #373 (sources_upload) · #380 (M6 dispatcher wait-loop) · #381 (PREFIRE_WIRING_AUDIT_CHECKLIST)

**Postmortem + dashboard** — #211 (envbug saga) · #248 (E OOM addendum) · #378 (Phase D v1 stale-branch postmortem) · #379 (M4 pure-debt-cleanup) · #388 (axis_map history dashboard) · #389 (fire_cost_ledger) · #392 (PURE_SAGA SSOT)

**hexa-lang inbox** — #629 (cloud bootstrap verbs) · #646 (cloud-guard UX + pod-lock)

**LIFE 가설 cross-ref** — H_242 (register-collapse-wiki-frac-sigmoid) · H_241 (corpus-quality-phi-correlate) · H_244 (sleep-stage-gated-emit-phi) · H_239 (bilingual-integration-phi-cross-lingual-leak) · H_246 (substrate-autonomy-emit-ratio)

---

## § 8. Honest C3 (≥ 7)

1. **시점 mismatch** — 본 doc 의 모든 metric 은 **as-of 2026-05-24 KST snapshot**. 각 source PR 시점이 #287 (2026-05-23) ~ #393 (2026-05-24) 분포. 후속 PR (corpus_v3, ckpt-bearing fire result 도착 등) 발생 시 본 doc 도 sync 필요 — 자동 sync 메커니즘 없음 (`@D a1` SSOT 수동 절차).
2. **ckpt baseline 부재** — Phase D fire 5건 모두 LOST (v1 stale-branch · v1 rogue · v2b 외부 cleanup) 또는 closure FAIL (E2 · E3v3). **단일 SUCCESS ckpt baseline 0건**. § 4 의 4-criterion empirical 0/4 의 직접 원인. M1 (phase-d-postfire-closure) + M2 (phase-d-ckpt-hf-upload) + M7 (self-verify-loop) 모두 동일 dependency 에 묶임.
3. **corpus baseline 의 synthetic vs hybrid vs real** — Phase D v1 = 100% synthetic (M3 0.354) · v2 = synthetic 80% + ko-wiki 20% hybrid (M3 0.504) · M9b PoC = anima-OWN ~/.claude/projects extract (M3 0.236, 1.12 MB cap). 3 corpus 의 **schema + lang balance 가 다름** (v2 ko-heavy 80% vs v1 5-lang uniform vs PoC 75.6% mixed). cross-corpus M3 비교는 같은 probe (`corpus_quality_probe.hexa`) 이지만 register-sink propagation 의 mechanism 차이는 미측정.
4. **closure-criterion empirical 부재** — § 4 표의 임계 4건 모두 spec only (PR #371 § 6 mapping). 실 fire 측정 0건이므로 "criterion #3 motivation ≥ 0.30 가 적절한 임계인가" 자체가 untested. dry-run synthetic (F-DISP-MOT 8/8 PASS) 만으로는 calibration 부족.
5. **per-lang verdict 매핑 누락** — heatmap § 6 의 D / B / A 일부 row 에서 zh/ru/ja 정확 verdict 부재 (`?` 처리). 원본 SSOT (PR #388 § 3) 가 자연어 요약 위주이고 raw `n_score` 5-lang 전수 dump 미수행 — heatmap 정밀화는 `vP21H_axis_*/result.json` re-read 필요.
6. **corpus_s101 M3 0.03 의 sub-sample 한계** — PR #340 측정은 probe default 1 MB sample (corpus_s101 600 MB 의 1/600). raw scalar 0.03 이 full 600 MB 의 M3 와 동일하다는 보장 없음 (sample 이 head-prefix 만 보면 register repetition 이 과대평가될 수 있음). 본 M3 값은 **anima-OWN register 의 envelope 지표**로만 해석 (PR #340 § 4 honest C3).
7. **cost 추정 ±$0.5** — Phase D v1 / rogue / v2b 는 외부 terminate 로 runpod billing 직접 회수 안 됨. § 5 의 cost column 은 dispatcher exit time − pod create time wall × $1.49/hr 추정. 사용자 cleanup intent 단정 회피 (PR #378 § Honest C3 §7).
8. **8-factor smoke 7/7 vs 실 fire 측정 0** — Phase B engine 의 `B-SPONT-1..7` smoke 는 synthetic input 기반 unit-level 통과. 실 model state (phi_final · curiosity_ema · split_event_recent 등) 가 cell 흐름과 어떻게 propagate 하는지는 ckpt-bearing fire result 가 도착해야 측정 가능 — Phase B 의 **production 가동 evidence 는 아직 0 layer**.
9. **AXIS_MAP envbug ~$8 sunk** vs **본 BENCHMARK saga $6-7** — § 1 의 누적 cost 는 PURE today (E1/E2/E3v3/Phase D x3) 만. envbug 1차/2차 fan-out + LORA 15-wave 등 sibling saga 는 별도 ledger (#389 § Cycle entries — LORA backfill). 본 doc 의 "PURE baseline" scope 는 saga 본류만.

— 끝 —
