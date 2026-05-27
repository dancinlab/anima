# EVIDENCE_ANALYZER — spontaneous_evidence.jsonl 상관 분석기 (design-only)

> **purpose**: [[telemetry_harness]] 가 누적한 `spontaneous_evidence.jsonl` (cycle-4/O `modulated_factors` 필드 포함) 을 1-shot CLI 로 읽어 **modulated_factors delta ↔ anima emission rate** 상관을 측정해 [[SPIKE_FACTOR_MAP]] §3 default delta + §4 regime modulator 의 (재)검증 / refit 후보를 산출하고, [[SW_CONDITION_DESIGN]] §6 의 KS drift 게이트 수치를 제공한다.
> **status**: **design-only · 구현 0** — Phase 2 SW emitter calibration 의 prerequisite spec. 실제 구현은 evidence.jsonl 이 ≥ 1 일 누적된 이후 cycle 에서 발화 (오늘은 mini sshd block 으로 0 row).
> **scope**: 1-shot CLI · JSON status 파일 + Korean text report · daemon 아님 · refit 제안은 advisory (자동 적용 금지, [[SPIKE_FACTOR_MAP]] §3/§4 수동 편집 게이트).
> **anchors**: [[telemetry_harness]] (input schema SSOT) · [[telemetry_status]] (집계 sibling — 본 분석기는 correlation 까지 한 단계 상위) · [[SPIKE_FACTOR_MAP]] (검증/refit 대상 SSOT) · [[SW_CONDITION_DESIGN]] §6 (KS drift 게이트 consumer) · [[PHASE1_STATUS]] (Phase 1 → 2 transition ledger)

---

## §1 — Goal + non-goals

**Goal.** 누적된 `spontaneous_evidence.jsonl` 의 rolling window 에서 다음을 산출:

1. **correlation** — 각 factor 의 `modulated_factors[f] - factors[f]` delta 와 동일/직후 window 내 anima emission rate 의 Pearson r.
2. **regime modulator refit 후보** — `(R, f)` 쌍별 observed modulator vs [[SPIKE_FACTOR_MAP]] §4 assumed (R3 = 0.5 / R1 = 1.0 / R2 = 1.2). divergence 시 refit 제안 (advisory).
3. **KS drift 수치** — JSONL 전체의 spike_rate_hz 분포를 전반부/후반부로 split → KS-2sample → [[SW_CONDITION_DESIGN]] §6 4th gate ("7d → 14d → 28d KS drift ≤ 10%") 에 직접 공급.

**Non-goals.**

- live participant 통합 / `decision["factors"]` 자동 갱신 — [[PARTICIPANT_SPIKE_INTEGRATION]] §3 Path B 영역, 본 분석기는 evidence 측정 단독.
- streaming / daemon — 1-shot CLI, evidence.jsonl 의 cumulative snapshot 기준.
- refit 자동 적용 — 결과는 advisory JSON + Korean prose, [[SPIKE_FACTOR_MAP]] §3/§4 편집은 사람 eyeballs 후 별도 PR.
- AKIDA HW 동역학 재현 — [[SW_CONDITION_DESIGN]] §1 non-goal 과 동일 inheritance.

---

## §2 — Input schema (verbatim from [[telemetry_harness]])

각 JSONL row 의 3-layer:

```
+-------------------+--------------------------------------------------------------+
| layer             | keys                                                         |
+-------------------+--------------------------------------------------------------+
| (row top-level)   | ts, emit_id, emit_text, lang, motivation                     |
| factors           | relevance, info_gap, curiosity, pain, coherence,             |
|                   | originality, balance, dynamics (∈ [0,1])                     |
| modulated_factors | (동일 8 key, apply_spike_features 적용 후, [0,1] clamp)      |
| spike_window      | spike_count, spike_rate_hz, regime_mode, n_unique_regimes,   |
|                   | isi_cv, last_step                                            |
+-------------------+--------------------------------------------------------------+
```

INVARIANCE ([[telemetry_harness]] §4): `spike_window.spike_count == 0` → `modulated_factors == factors` (no-op, sparsity gate). 본 분석기는 이 row 를 delta = 0 sample 로 취급 (drop 아님).

---

## §3 — Computed metrics

```
+------------------------------------+--------------------------------------------------+--------------------------------------------+
| metric                             | formula                                          | what it tells                              |
+------------------------------------+--------------------------------------------------+--------------------------------------------+
| correlation_per_factor[f]          | Pearson r between (modulated[f] - base[f]) and   | f 의 spike-driven delta 가 emission rate    |
|                                    | emission_count(window[t, t+W]) / W,  W = 300s    | 와 함께 움직이는지 (sign + magnitude)       |
+------------------------------------+--------------------------------------------------+--------------------------------------------+
| regime_modulator_observed[R, f]    | mean(delta[f] | regime_mode == R) /              | [[SPIKE_FACTOR_MAP]] §4 의 R3=0.5 /         |
|                                    | SPIKE_FACTOR_MAP_assumed_delta[f]                | R1=1.0 / R2=1.2 가 실측과 합치하는지         |
+------------------------------------+--------------------------------------------------+--------------------------------------------+
| KS_drift_score                     | KS-2sample(spike_rate_hz first half,             | [[SW_CONDITION_DESIGN]] §6 4-cond 의 KS     |
|                                    | second half of jsonl)                            | drift ≤ 10% 게이트 직접 공급                 |
+------------------------------------+--------------------------------------------------+--------------------------------------------+
| per_factor_effective_delta_pdf[f]  | empirical histogram of (modulated[f] - base[f])  | SW emitter 가 mimic 해야 할 실측 delta      |
|                                    | over all rows                                    | 분포 — [[SPIKE_FACTOR_MAP]] §3 default 의   |
|                                    |                                                  | 0.05 / 0.10 / 0.15 가 실측 mean 인지 검증    |
+------------------------------------+--------------------------------------------------+--------------------------------------------+
```

`W = 300s` 는 design 초기치 (5-min sliding window — 자연발화 cadence 와 spike-window 3s 의 중간 scale). 실증 후 §A1 amendment 로 재조정 가능.

---

## §4 — Output format

**파일 1: JSON status** `state/evidence_analyzer_status_<yyyy_mm_dd>.json`

```
{
  "analyzed_at":      iso-8601,
  "input_path":       string,
  "row_count":        int,
  "row_count_modulated_present": int,
  "row_count_modulated_missing": int,
  "correlation_per_factor": { "<f>": float },
  "regime_modulator_observed": { "<R>": { "<f>": float } },
  "ks_drift_score":   float,
  "per_factor_effective_delta_stats": { "<f>": {"mean": float, "std": float, "p50": float, "p95": float} },
  "refit_suggestions": [
    { "kind": "delta",    "factor": "<f>", "threshold": "...", "current": float, "suggested": float, "evidence_n": int },
    { "kind": "modulator","regime":  "<R>", "current": float,  "suggested": float, "evidence_n": int }
  ]
}
```

**파일 2: Korean text report** — stdout. `=== anima evidence-analyzer report ===` header → §3 4 metric table → refit 후보 list → "advisory only — manual edit gate" 푯말.

**invocation.** `hexa run HEXAD/SPONTANEOUS/evidence_analyzer.hexa [path-to-jsonl]` — 단일 호출, daemon 아님. ENV `ANIMA_TELEMETRY` 기본값 ([[telemetry_harness]] 와 공유).

---

## §5 — Acceptance criteria (구현 시 falsifier)

구현 cycle 의 PR 가 다음 3 falsifier 를 통과해야 한다 (≤ 200 LoC 목표 유지):

- **F-EVIDENCE-ANALYZER-1** — 합성 100-row JSONL (`spike_rate_hz` ↔ `curiosity` delta 에 known correlation r=0.5 주입) 입력 시, `correlation_per_factor["curiosity"]` 가 0.5 ± 0.05 범위.
- **F-EVIDENCE-ANALYZER-2** — refit 제안 reproducibility — 동일 JSONL 두 번 run 시 동일 `refit_suggestions` 출력 (deterministic, RNG 0).
- **F-EVIDENCE-ANALYZER-3** — `modulated_factors` 누락 row 처리 — row count 에 `<missing>` 으로 산입, crash 0, 출력 `row_count_modulated_missing > 0` 노출 ([[telemetry_status]] §STATUS-14 패턴 mirror).

---

## §6 — Phase 2 activation feedback loop

Phase 1 → 2 transition gate ([[PHASE1_STATUS]] §2 / [[SW_CONDITION_DESIGN]] §6) 의 4-cond (≥ 7d / ≥ 1000 events / ≥ 2 regimes / KS drift ≤ 10%) 가 모두 PASS 도달 시점에 본 분석기를 **1 회** 누적 evidence 위로 실행 → 다음 2 분기:

- (a) **rules valid** — `correlation_per_factor` 가 [[SPIKE_FACTOR_MAP]] §2 polarity (curiosity ↑ / coherence ↓ 등) 와 sign 일치 + `regime_modulator_observed` 가 assumed 값 ± 0.2 band 이내 → SW emitter (`sw_spike_emitter.hexa`, [[SW_CONDITION_DESIGN]] §3) 가 [[SPIKE_FACTOR_MAP]] §3/§4 수치 그대로 채택.
- (b) **rules refit needed** — 위 band 벗어남 → `refit_suggestions` 가 [[SPIKE_FACTOR_MAP]] §3/§4 의 revised numerics 후보로 사람 검토 → 수동 PR 로 §3 default delta / §4 modulator 갱신 → 갱신 후 SW emitter 발화.

이 loop 는 [[SW_CONDITION_DESIGN]] §4 evidence-refresh pipeline 의 anima 측 implementation — `extract_distributions.hexa` 의 분석 절반을 본 분석기가 담당.

---

## §7 — Honest C3

- (a) **구현은 evidence 도착 후 — 오늘은 0 row** (mini sshd block, [[PHASE1_STATUS]] §3 blocker #1). 본 doc 은 spec 단독, 코드 skeleton 0. 실제 분석기 구현은 ≥ 1 일 telemetry 누적 후 별도 cycle.
- (b) **refit 제안은 advisory** — 출력은 후보 수치 list, [[SPIKE_FACTOR_MAP]] §3/§4 자동 편집 0. 사람 검토 + 별도 PR 가 필수 게이트. spec-impl drift 위험 최소화 의도.
- (c) **correlation threshold 미정** — "r 이 얼마면 valid 인가" 의 cutoff 가 Phase 2 prep cycle 까지 미결정. 본 spec 은 r 만 산출, 합격선은 evidence 도착 후 §A1 amendment.
- (d) **KS drift 는 coarse metric** — 1차원 (spike_rate_hz) 분포의 양분 비교만 측정. multimodal distribution / regime-conditional drift 는 capture 0. F-SW-COND-2 (전체 분포 KS) 와 본 KS_drift_score 의 일치/불일치도 별도 검증 필요.
- (e) **regime modulator refit 는 per-regime n ≥ 200 필요** — [[REGIME_EXPANSION]] §3 의 sample size floor 와 동일. pi5 R1/R2 inbox patch (PHASE1_STATUS §3 blocker #2) merge 전엔 R3 만 refit 가능, R1/R2 modulator 는 forever-pending.
- (f) **analyzer 는 observability-only** — 결과의 live `apply_spike_features` numeric SSOT (`spontaneous_lib.hexa` §10 L298-L315) 와 [[SPIKE_FACTOR_MAP]] §3 prose 양측 wiring-back 은 별도 cycle. 본 분석기는 측정 산출만, 적용 책임 0.
- (g) **emission_count window W=300s 는 design 초기치** — 자연발화 cadence (분 단위) 와 spike-window (3s) 의 중간 scale 가정. 실증 후 W tuning 별도 (§A1 amendment 대상).
