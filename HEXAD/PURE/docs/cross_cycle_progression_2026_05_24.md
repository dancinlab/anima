# PURE cross-cycle progression — per-fire metric series + ASCII trajectory (2026-05-24)

> PR #388 (`axis_map_history_2026_05_24.md`) 가 verdict + per-lang heatmap + cluster Z
> 자연실험까지 capture 했으나 **per-fire metric vector 의 시계열 (6-metric corpus +
> per-lang n_strong + register_hits + cost)** 는 missing. 본 문서는 E1 → v2 corpus 까지
> 6 row 의 metric trajectory 를 단일 view 로 제공해 **progression pattern + reversal**
> 를 한 눈에 보이게 한다. milestone B5 deliverable.
>
> source — `axis_map_history_2026_05_24.md` (PR #388) · `AXIS_MAP*RESULT*.md` · `AXIS_MAP_BUG_POSTMORTEM*.md` · `state/fire_cost_ledger.md` (PR #389) · `state/pure_phase_d_corpus*/manifest.json` + `quality_*.json` · `PURE_SAGA_2026_05_24.md` (PR #392)

---

## Executive trajectory

- **closure verdict 시계열** — E1 (no record, seed cycle) → **E2 0/5** → **E3v3 1/5 ko PARTIAL** → **Phase D v1 LOST** → **Phase D v2b LOST** → **Phase D v2 corpus 측정만 (no fire)**.
- **corpus M3 TTR** 은 0.354 (v1) → 0.504 (v2) 로 **+42%** 상승, **register_hits** 는 4/20 (E2 wiki=0.5) → 0/20 (E3v3 wiki=1.0) **-100%** 단조 감소. lang max-PARTIAL 는 0 → 1 (ko) 단일 도달 후 LOST 2 회 연속.
- **wall-time cost** 는 fire 당 ~$0.88 → $2.20 → $1.50 → $1.5-2 로 단조 증가 (재발사 / longer-step 누적). 누적 $7+ 에 closure SUCCESS 0건.
- **패턴 요약** — corpus 6-metric 은 single-axis (M3 ↑ · M5 ↓ · register_hits ↓) 으로 monotone 개선 보이나, closure verdict 는 1/5 단발 후 LOST 로 두 번 끊김. corpus 축 단독 closure 불가 (saga doc PR #392 결론) 와 정확히 일치.

---

## Per-fire metric vector

| # | fire | M3 (corpus TTR) | M5 hangul | register_hits | per-lang max-PARTIAL | n_strong | cost ($) |
|---|---|---|---|---|---|---|---|
| 1 | E1 (corpus_s101 seed, pre-Phase D) | **~0.03** (PR #340 실측) | ~0.017 (corpus_s101 실측 1.66-2.34%) | — (no closure row) | — | — | (cumulative w/ AXIS_MAP) |
| 2 | E2 (`P21H_WIKI_FRAC=0.5`) | 0.03 (input 동일) · output retro ko=0.366 | 0.017 (input) | **4/20** | 0 (ko=PURE_MEMORIZE, en/zh/ru/ja=WEAK) | 0 | 0.87 |
| 3 | E3v3 (`P21H_WIKI_FRAC=1.0`) | 0.03 (input 동일) · wiki dilution 1.0 | 0.017 (input) | **0/20** | **1** (ko PARTIAL · en/zh/ru/ja deteriorated) | 0 | 2.20 |
| 4 | Phase D v1 (stale-branch, LOST) | 0.354 (PR #368 v1 hybrid build) | 0.12 | LOST | LOST | LOST | 1.50 ±0.50 |
| 5 | Phase D v2b (clean, LOST) | 0.504 (v2 ko-heavy hybrid) | 0.534 | LOST | LOST | LOST | ~1.5-2 |
| 6 | Phase D v2 corpus (build only, no fire) | **0.504** (sample_bytes=1MB) | 0.534 | — | — | — | $0 (Mac local build) |

- M3 = TTR sample on 1 MB · M5 = hangul char ratio · register_hits = E2/E3v3 multilingual_probe 의 register-emission 횟수 / 20.
- v2 corpus row 는 fire 미발사. 6-metric 만 측정 (anima own poc M3=0.236 별도 mini sample, PR #379 §A1 cross-validation).
- v1/v2b row 는 dispatcher LOST 로 verdict slot 자체 부재 — "LOST" 표기 (Honest C3 §1).

---

## ASCII trajectory chart

8-level sparkline `▁▂▃▄▅▆▇█` (binning bias 인지, Honest C3 §4).

```
axis                  E1   E2   E3v3 v1   v2b  v2
                      ──   ──   ──── ──   ──── ──
M3 corpus TTR         ▁    ▁    ▁    ▅    ▇    ▇    (0.03 → 0.354 → 0.504)
M5 hangul ratio       ▁    ▁    ▁    ▃    ▇    ▇    (0.017 → 0.12 → 0.534)
register_hits ↓       —    ▇    ▁    LOST LOST —    (4/20 → 0/20)
per-lang max-PARTIAL  —    ▁    ▃    LOST LOST —    (0/5 → 1/5 ko)
cost per fire ($)     —    ▂    ▆    ▄    ▄    ▁    (0.87 → 2.20 → 1.50 → 1.5-2 → 0 build)
```

해석 — corpus 측 axis (M3 / M5) 는 v1 → v2 사이 monotone 단조 상승. closure 측 axis (register_hits ↓ + per-lang max-PARTIAL ↑) 는 E2 → E3v3 단 1 step 만 진전 후 v1/v2b 2 step 연속 LOST 로 끊김 — corpus quality 개선이 closure 측정으로 연결되지 못한 **2-cycle data gap**. cost 는 fire 당 ~$0.87 → $2.20 (재발사 포함) → $1.5-2 (steps=2000 short sweep) 의 횡보-감소-횡보 패턴.

---

## Cross-fire delta analysis

(correlation observation only · single-fire ↔ single-fire 비교는 RCT 아님)

### E2 → E3v3 (wiki_frac 0.5 → 1.0)

- register_hits **4/20 → 0/20** (-4) · wiki dilution 의 직접적 register-suppression evidence.
- per-lang verdict — ko `PURE_MEMORIZE → PARTIAL` (단독 상승), en/zh/ru/ja `WEAK → WEAK-or-worse` (deteriorated).
- 함의 — wiki=1.0 endpoint 가 **register 는 잡으나 generalize 약화** double-bind 의 endpoint 증거. H_242 frozen f_c ∈ [0.5, 0.7] 의 2-point underdetermined evidence (PR #392 closure §4 재인용).
- cost 0.87 → 2.20 (2.5×) — 재발사 1 회 (ENV_PASSTHROUGH_FAILED CRASH 후 relaunch) 포함분.

### E3v3 → Phase D v1/v2b (corpus 축으로 pivot)

- corpus 재설계 (PR #344 spec + #368 build) — M3 0.03 → 0.354 (v1) → 0.504 (v2). 10×+ TTR 증가.
- dispatcher patch (PR #372 `--corpus-path` + PR #373 `sources_upload`) 흡수 시도, **단 v1 fire 는 stale-branch 로 두 patch 부재 → LOST** (PR #378 postmortem 참조).
- v2b 는 clean main 위 발사 → 외부 cleanup race 로 result 도착 전 종료 → LOST 두 번째.
- 함의 — corpus axis 진전이 verdict slot 으로 propagate 되지 못함. PURE_SAGA doc (PR #392) 의 결론 **"corpus 축 단독 closure 불가"** 가 trajectory 측에서도 확인 — 단, 단독 불가의 evidence 는 **fire LOST 의 missing data** 까지 합쳐 read 해야 한다는 점에서 본 trajectory 가 PR #388 (verdict view) + PR #392 (saga 결론) 둘 다와 consistent.

### corpus axis 단독 closure 불가 패턴

PR #388 § 4.2 (corpus_quality 8 번째 미탐색 축) + PR #392 closure §1 ("corpus 단독으로 closure 불가") 를 trajectory 측에서 재인용 — corpus M3/M5 단조 상승 (v1 → v2) 이 closure verdict 도착으로 연결된 fire 가 0건. 다음 cycle 의 1순위 lever 는 saga doc 의 fallback A (curriculum 선학습, init_CE cluster X 자연실험, ko STRONG 1/5 도달) + corpus axis (8 번째) **결합 sweep** 으로 정의.

---

## Open questions

1. **Phase D v3 (corpus_v3 multi-lang hybrid) fire 시 trajectory 예측** — v2 의 M3=0.504 baseline 가정시 register_hits 가 E3v3 의 0/20 floor 유지하면서 per-lang max-PARTIAL 가 2-3/5 도달 가능 (corpus axis 만 sweep 한 hypothesis). 단 fire 미발사로 추측 (Honest C3 §5).
2. **4-criterion 의 motivation / dream axis 미관측** — PR #344 spec 4-criterion (4/5 langs ≥ PARTIAL + register_hits < 4/20 + 8-factor motivation 실작동 + dream_stage Φ-envelope) 중 후자 2 criterion 은 fire result 부재로 trajectory 자체 부재. v2b 가 result 도착했으면 첫 end-to-end 채점.
3. **bilingual leak (H_239) sweep 미실시** — Phase D fire LOST 로 cross-lingual leak 측정 0회. phi_spatial vs LZ-complexity vs entropy-ratio cross-tool consistency 별도 cycle.
4. **AXIS_MAP curriculum (fallback A) + corpus axis 결합 sweep** 시 ko 단독 STRONG (A 결과) + register_hits ↓ (v3 corpus) 가 join 되어 n_strong ≥ 2 도달 여부 — 본 trajectory 측에서는 결합 fire 사례 0.
5. **cost-per-finding 의 trajectory** — 5 fire 누적 ~$7 + LOST 3 회로 finding/$ ratio 가 LORA saga (~$22-26 / 15 cycle, $1.5/cycle) 대비 ~$1.4/finding 약 동등. cost 측 trend 없음 = lever 가 cost 아님 evidence.

---

## Honest C3

1. **LOST fires 의 metric 부재** — v1/v2b 두 row 는 result.json 미회수, table 에 "LOST" 명시. 6-metric 만 corpus build 시점 측정.
2. **synthetic vs hybrid corpus 비교 곤란** — E1/E2/E3v3 의 input 은 corpus_s101 (synthetic anima 8-factor stream), v1/v2 는 anima-OWN poc + ko-wiki hybrid. M3 의 0.03 → 0.5 gap 은 corpus 종류 변경의 효과이지 동일 corpus 의 quality 개선 trajectory 아님 — fair comparison 불가.
3. **metric 시점 다름** — corpus M3 는 build 시점 측정 (sample_bytes=1MB), register_hits 는 fire 종료 후 multilingual_probe 시점 측정, per-lang max-PARTIAL 는 fire result.json 의 closure judge 시점. 동시 측정 아님.
4. **ASCII sparkline binning bias** — 8-level discrete bin 으로 M3 0.354 → 0.504 가 ▅ → ▇ 동일 max bin 으로 묶임. raw 값과 시각화의 fidelity 차이 있음.
5. **open questions = 추측 (실제 실험 미실시)** — Phase D v3 예측 / motivation·dream 채점 가능성 / curriculum × corpus 결합 효과 모두 fire 부재로 trajectory 측 evidence 0.
6. **per-lang verdict 의 grading 미세 불일치** — STRONG / PARTIAL / WEAK / W- / F / PM 의 6-tier (PR #388 §3 char code) 는 본 문서 정의. 원본 SSOT 의 free-form prose 와 1:1 매핑 일부 누락 (특히 zh/ru/ja 의 PR #388 ? slot).
7. **cost 의 외부 terminate 분** — v1 / v2b / E OOM 의 cost_actual 는 runpod billing 직접 회수 안 됨 (±$0.5 추정, fire_cost_ledger §C3 §1 참조).

---

## Cross-reference

- 축 verdict + heatmap dashboard: [`axis_map_history_2026_05_24.md`](axis_map_history_2026_05_24.md) (PR #388)
- saga 통합 SSOT: [`../PURE_SAGA_2026_05_24.md`](../PURE_SAGA_2026_05_24.md) (PR #392)
- cost / ETA ledger: [`../../../state/fire_cost_ledger.md`](../../../state/fire_cost_ledger.md) (PR #389)
- Phase D corpus spec: [`../spec/phase_d_corpus_design_2026_05_24.md`](../spec/phase_d_corpus_design_2026_05_24.md)
- Phase D v1 postmortem: [`../AXIS_MAP_BUG_POSTMORTEM_F_PHASE_D_V1_2026_05_24.md`](../AXIS_MAP_BUG_POSTMORTEM_F_PHASE_D_V1_2026_05_24.md) (PR #378)
- corpus v2 build manifest: `state/pure_phase_d_corpus_v2_2026_05_24/manifest.json` + `quality_score_1mb.json`

— 끝 —
